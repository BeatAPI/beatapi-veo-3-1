# Connect your BeatAPI account

1. Sign in at https://beatapi.io/sign-in. Open https://beatapi.io/dashboard/apikeys, choose Create API key, give it a name and create it. Copy the key only into the host's secure credential input. Prices are at https://beatapi.io/pricing.
2. Install the complete plugin with an Agent Plugins client supporting stdio MCP and Python 3.10+. There are no pip dependencies. The root mcp.json starts the bundled scripts/beatapi_mcp.py.
3. Ask the host to supply your own key to that MCP subprocess as BEATAPI_API_KEY through its approved secret-input or protected environment facility. Never put the key in chat, command arguments, public mcp.json or this repository. Do not reuse the creator's credential. If your host cannot securely supply that variable to the subprocess, stop and explain the missing secure setup step. A remote MCP URL alone is not a secure key-entry mechanism.
4. initialize and tools/list work without a key and never contact the network. The server exposes capabilities_search, capabilities_inspect and capabilities_run. Without a key, a tool call explains setup and sends no HTTP request. Model discovery/inspection after secure setup is nonbillable.
5. Describe your image or video. The bot lists this plugin's complete family and current prices, inspects your chosen model, and asks approval for one paid request. No generation starts on installation. The bridge enforces the family allowlist, exact reference/input.model match, explicit operation and a nonempty idempotency key before a start.
6. The host keeps a durable task record before starting, polls the original task and downloads/attaches its returned real output. Downloads never receive the API Authorization header. Do not run a video just to check setup.

## Connection security

The stdio program sends authenticated JSON-RPC only to https://beatapi.io/mcp, rejects redirects, does not accept an endpoint override and does not log credentials. No credential is bundled. The existing remote MCP service is shared; each plugin's local bridge exposes only its own allowlisted model family. This is not an account permission restriction outside this bridge. A compatible remote client can separately configure https://beatapi.io/mcp with its own secure Authorization header; that is optional and is not required by this stdio package.

This is an independent BeatAPI integration. Read VERIFICATION.md for exact checks and limitations. Installation does not authorize paid tasks or local media uploads.
