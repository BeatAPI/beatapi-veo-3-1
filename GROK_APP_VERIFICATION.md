# Grok application checks, 2026-10-21

Tested public code commit: `6d69fdb8a7beb1ff9419f6d25fa545a5c866e86b`. Python 3.13.5. Scope: nonbillable installation and MCP host integration.

The Grok Bot application cloned this repository at the exact commit, read plugin.json, mcp.json, SETUP.md and all four skills, verified referenced files and the complete model family, and ran all 10 offline unit checks successfully in a clean environment. initialize and tools/list passed.

The application then temporarily registered the bundled stdio program with BEATAPI_API_KEY explicitly set to an empty string. The actual host reported it connected and discovered exactly capabilities_inspect, capabilities_run and capabilities_search. A family-model inspect returned the intended missing-key setup message. The reference enums stayed within this plugin's family. The temporary registration was removed afterward; existing connections were preserved.

No real credential was requested, read or entered, no paid run was invoked, and no video was generated. These checks do not verify secure key propagation from Grok's encrypted input to a registered stdio subprocess, native paid generation or file attachment. The host exposes both encrypted credential input and stdio registration, but their combination was not tested. Setup must pause if the host cannot securely supply the user's key.

The missing-key observation supports the code's early-return behavior. It is not a kernel-level proof that the whole host opened no network sockets. The owner-authorized authenticated service/image checks and their exact scope are recorded separately in VERIFICATION.md.
