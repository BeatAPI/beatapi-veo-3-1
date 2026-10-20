#!/usr/bin/env python3
"""Family-scoped stdio MCP client. Python 3.10+, standard library only."""
import argparse
import copy
import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.request

ENDPOINT = 'https://beatapi.io/mcp'
ROOT = Path(__file__).resolve().parent.parent
MAX_MESSAGE = 4 * 1024 * 1024


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def text_error(message):
    return {'isError': True, 'content': [{'type': 'text', 'text': message}]}


class FamilyServer:
    def __init__(self, root=ROOT, transport=None):
        self.root = Path(root)
        self.catalogue = json.loads((self.root / 'catalogue.json').read_text())
        self.refs = {item['reference']: item for item in self.catalogue}
        self.manifest = json.loads((self.root / 'plugin.json').read_text())
        self.definitions = json.loads((self.root / 'tool-definitions.json').read_text())
        self.transport = transport or self.remote

    def remote(self, method, params):
        key = os.environ.get('BEATAPI_API_KEY', '').strip()
        if not key or any(ord(c) < 32 for c in key):
            return text_error('Connect your own BeatAPI key through the host secure credential facility as BEATAPI_API_KEY. Never paste it in chat. No API call was sent. See SETUP.md.')
        request = urllib.request.Request(ENDPOINT,
            data=json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': method, 'params': params}).encode(),
            headers={'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream',
                     'Authorization': 'Bearer ' + key, 'User-Agent': 'BeatAPI-Family-MCP/0.1.0'})
        try:
            with urllib.request.build_opener(NoRedirect).open(request, timeout=100) as response:
                blob = response.read(MAX_MESSAGE + 1)
            if len(blob) > MAX_MESSAGE:
                return text_error('Response exceeded the supported size; do not start another task.')
            # Do not emit the credential even if a remote error unexpectedly includes it.
            answer = json.loads(blob.decode().replace(key, '[REDACTED]'))
            if 'error' in answer:
                return text_error('BeatAPI returned an MCP error. Check the contract or connection; do not automatically create another task.')
            result = answer['result']
            if not isinstance(result, dict):
                return text_error('Unexpected BeatAPI response; preserve the existing task record.')
            return result
        except urllib.error.HTTPError as error:
            if error.code == 401:
                return text_error('BeatAPI authentication failed. Check your own key in secure settings; never share it in chat.')
            return text_error('BeatAPI HTTP ' + str(error.code) + '. Check your account or request. Do not silently start another task.')
        except (OSError, ValueError, KeyError):
            return text_error('BeatAPI response is uncertain. Preserve the same task and idempotency key; do not start a replacement.')

    def list_tools(self):
        tools = copy.deepcopy(self.definitions)
        for tool in tools:
            name = tool['name']
            tool['description'] = {
                'capabilities_search': 'List this plugin\'s complete model family with the current public contracts and prices. Free. Contains no models from other families.',
                'capabilities_inspect': 'Inspect one model in this plugin\'s family before generation. Free. Use the exact returned reference.',
                'capabilities_run': 'Start one explicitly approved paid image/video task or poll the same task. Only this plugin\'s model family is accepted. Never start a test automatically.'}[name]
            props = tool['inputSchema']['properties']
            if 'reference' in props:
                props['reference']['enum'] = list(self.refs)
            if name == 'capabilities_run':
                props['operation']['enum'] = ['start', 'status']
                tool['inputSchema']['required'] = ['reference', 'operation']
            tool['annotations'] = {'readOnlyHint': name != 'capabilities_run',
                                   'destructiveHint': False, 'openWorldHint': True}
        return tools

    def call(self, params):
        if not isinstance(params, dict):
            return text_error('Invalid tool request.')
        name, args = params.get('name'), params.get('arguments', {})
        if not isinstance(args, dict):
            return text_error('Tool arguments must be an object.')
        if name == 'capabilities_search':
            # Inspect each allowlisted reference, instead of forwarding an unrestricted search.
            # This returns the complete family, including matches the upstream search may rank lower.
            cards = []
            for reference in self.refs:
                result = self.transport('tools/call', {'name': 'capabilities_inspect', 'arguments': {'reference': reference}})
                if result.get('isError'):
                    return result
                contract = result.get('structuredContent')
                if contract is None:
                    try:
                        contract = json.loads(next(c['text'] for c in result['content'] if c['type'] == 'text'))
                    except (KeyError, ValueError, StopIteration):
                        return text_error('Unable to read the live model contract. No generation was started.')
                data = contract.get('data', {})
                if data.get('reference') != reference:
                    return text_error('Model contract reference mismatch; no generation was started.')
                cards.append(data)
            output = {'data': {'data': cards, 'total': len(cards)}, 'scope': self.manifest['name']}
            return {'content': [{'type': 'text', 'text': json.dumps(output)}], 'structuredContent': output}
        if name not in ('capabilities_inspect', 'capabilities_run'):
            return text_error('This plugin exposes only its three model capability tools.')
        reference = args.get('reference')
        if reference not in self.refs:
            return text_error('Choose a reference from this plugin\'s model family. No API call was sent.')
        if name == 'capabilities_run':
            operation = args.get('operation')
            if operation not in ('start', 'status'):
                return text_error('Specify operation start or status explicitly. No API call was sent.')
            if operation == 'start':
                inp = args.get('input')
                if not isinstance(inp, dict) or inp.get('model') != self.refs[reference]['id']:
                    return text_error('input.model must match the inspected reference exactly. No API call was sent.')
                idem = args.get('idempotency_key')
                if not isinstance(idem, str) or not idem.strip() or len(idem) > 255:
                    return text_error('Persist one idempotency_key before starting a paid task. No API call was sent.')
            elif not isinstance(args.get('task_id'), str) or not args['task_id'].strip():
                return text_error('Poll the original task_id. No API call was sent.')
        return self.transport('tools/call', {'name': name, 'arguments': args})

    def handle(self, message):
        if not isinstance(message, dict) or message.get('jsonrpc') != '2.0':
            return {'jsonrpc': '2.0', 'id': None, 'error': {'code': -32600, 'message': 'Invalid request'}}
        if 'id' not in message:
            return None  # Notifications never execute a tool or read a credential.
        ident, method = message['id'], message.get('method')
        if method == 'initialize':
            version = message.get('params', {}).get('protocolVersion', '2025-06-18')
            if version not in ('2024-11-05', '2025-03-26', '2025-06-18'):
                version = '2025-06-18'
            result = {'protocolVersion': version, 'capabilities': {'tools': {}},
                      'serverInfo': {'name': self.manifest['name'], 'version': self.manifest['version']}}
        elif method == 'ping':
            result = {}
        elif method == 'tools/list':
            result = {'tools': self.list_tools()}
        elif method == 'tools/call':
            result = self.call(message.get('params', {}))
        else:
            return {'jsonrpc': '2.0', 'id': ident, 'error': {'code': -32601, 'message': 'Method not found'}}
        return {'jsonrpc': '2.0', 'id': ident, 'result': result}


def main():
    try:
        server = FamilyServer()
    except (OSError, ValueError, KeyError):
        print('Plugin files are incomplete. Reinstall the full plugin package.', file=sys.stderr)
        return 1
    while True:
        line = sys.stdin.buffer.readline(MAX_MESSAGE + 1)
        if not line:
            return 0
        if len(line) > MAX_MESSAGE:
            return 1
        try:
            response = server.handle(json.loads(line))
        except (ValueError, KeyError, TypeError, AttributeError):
            response = {'jsonrpc': '2.0', 'id': None, 'error': {'code': -32600, 'message': 'Invalid request'}}
        if response is not None:
            print(json.dumps(response, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    raise SystemExit(main())
