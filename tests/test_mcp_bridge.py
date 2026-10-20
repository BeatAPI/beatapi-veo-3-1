"""No-network checks for the plugin's security and MCP protocol boundaries."""
from pathlib import Path
import importlib.util
import io
import json
import os
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('beatapi_mcp',ROOT/'scripts'/'beatapi_mcp.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.calls=[]
        def remote(method,params):
            self.calls.append((method,params))
            ref=params['arguments'].get('reference')
            return {'structuredContent':{'data':self.server.refs.get(ref,{})},'content':[]}
        self.server=module.FamilyServer(ROOT,remote)
        self.ref=next(iter(self.server.refs))
        self.model=self.server.refs[self.ref]['id']

    def test_initialize_and_list_are_local(self):
        for method in ['initialize','tools/list','ping']:
            self.assertIn('result',self.server.handle({'jsonrpc':'2.0','id':1,'method':method}))
        self.assertEqual(self.calls,[])
        self.assertEqual(len(self.server.list_tools()),3)

    def test_notifications_never_execute(self):
        self.assertIsNone(self.server.handle({'jsonrpc':'2.0','method':'tools/call','params':{'name':'capabilities_search'}}))
        self.assertEqual(self.calls,[])

    def test_outside_family_blocked_before_network(self):
        for name in ['capabilities_inspect','capabilities_run']:
            self.assertTrue(self.server.call({'name':name,'arguments':{'reference':'model:unrelated-model','operation':'start'}})['isError'])
        self.assertEqual(self.calls,[])

    def test_mismatch_and_missing_idempotency_blocked(self):
        for inp,idem in [({'model':'wrong'},'saved'),({'model':self.model},None)]:
            args={'reference':self.ref,'operation':'start','input':inp,'idempotency_key':idem}
            self.assertTrue(self.server.call({'name':'capabilities_run','arguments':args})['isError'])
        self.assertEqual(self.calls,[])

    def test_operation_and_status_id_required(self):
        for args in [{'reference':self.ref},{'reference':self.ref,'operation':'status'},{'reference':self.ref,'operation':'result'}]:
            self.assertTrue(self.server.call({'name':'capabilities_run','arguments':args})['isError'])
        self.assertEqual(self.calls,[])

    def test_approved_start_and_status_forward_unchanged(self):
        for args in [{'reference':self.ref,'operation':'start','input':{'model':self.model,'prompt':'fixture'},'idempotency_key':'fixture-only'},
                     {'reference':self.ref,'operation':'status','task_id':'fixture-only'}]:
            self.server.call({'name':'capabilities_run','arguments':args})
            self.assertEqual(self.calls[-1][1]['arguments'],args)

    def test_search_returns_complete_family_only(self):
        result=self.server.call({'name':'capabilities_search','arguments':{'query':'other family'}})
        refs={c['reference'] for c in result['structuredContent']['data']['data']}
        self.assertEqual(refs,set(self.server.refs))

    def test_missing_key_sends_no_request(self):
        with patch.dict(os.environ,{},clear=True),patch('urllib.request.build_opener') as opener:
            self.assertTrue(self.server.remote('tools/call',{})['isError'])
            opener.assert_not_called()

    def test_redirects_rejected(self):
        self.assertIsNone(module.NoRedirect().redirect_request(None,None,None,None,None,None))

    def test_key_only_to_fixed_endpoint_and_redacted_response(self):
        credential='unit-test-credential-not-real'
        payload={'result':{'content':[{'type':'text','text':credential}]}}
        def opener(req,timeout):
            self.assertEqual(req.full_url,'https://beatapi.io/mcp')
            self.assertEqual(req.get_header('Authorization'),'Bearer '+credential)
            return io.BytesIO(json.dumps(payload).encode())
        with patch.dict(os.environ,{'BEATAPI_API_KEY':credential,'BEATAPI_BASE':'https://wrong.invalid'}),patch('urllib.request.OpenerDirector.open',side_effect=opener):
            result=self.server.remote('tools/call',{})
            self.assertNotIn(credential,json.dumps(result))


if __name__=='__main__':
    unittest.main()
