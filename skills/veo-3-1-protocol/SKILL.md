---
name: veo-3-1-protocol
description: "Secure MCP access, explicit cost approval and reliable task delivery."
---

# BeatAPI Generation Protocol

Use the configured BeatAPI MCP connection. Never put an API key into a tool argument, prompt, export, URL, log or source file. Authentication is supplied by the host as the installing user’s BEATAPI_API_KEY in the MCP subprocess environment through approved secure entry. The bundled family-scoped stdio bridge performs the authenticated HTTP request. The remote endpoint is exactly https://beatapi.io/mcp. If using REST explicitly instead, the only API origin is https://api.beatapi.io. Reject redirects for authenticated calls and never send credentials to a media download URL.

Discover and inspect

Call capabilities_search and copy its returned reference exactly. Restrict model selection to this plugin's family catalogue. Call capabilities_inspect before running the chosen model. Read readiness, input_schema, execution, pricing and all x-beatapi-rules. A reference must match input.model exactly. Do not execute unavailable models or unsupported fields. A published contract is not a successful generation test.

Confirm the cost

Show the exact model, resolution, quality, duration if relevant, reference inputs, currency and quoted billing basis. Starting prices in descriptions are dated examples for the stated specification. For videos do not extrapolate from an 8 second example or ignore reference-input billing. If the current cost cannot be established, stop. Obtain explicit approval for one paid task; an installed key alone is never approval. Read-only review, installation, discovery and pricing requests never authorize a paid start, upload, demo or test.

Start once and resume

Use capabilities_run with operation start, the inspected reference, validated input and one unique idempotency_key. Before sending, persist a record of that reference, input and idempotency key in the host's approved task storage, without credentials. Stop on unreadable/corrupt state. Save the returned task_id before taking other action. Never create a new paid task after an uncertain response. Resume operation status with the same reference and task_id, respecting poll_after_seconds. Retry an uncertain start only with the identical idempotency_key and identical input.

Deliver a real result

Only report success when status is succeeded and output.media contains actual returned media. Download through the host's approved file facility without API authorization headers, validate the file is nonempty and decodes as the expected media, attach it and include its real hosted URL. Do not fabricate files, results or links. If download/attachment is unsupported, state exactly which part is incomplete. Explain customer-facing failures without exposing private account data or raw supplier errors. A failed request never justifies another paid run without approval.

Reference material

Use public HTTPS reference URLs supported by the inspected model. A local file upload requires separate user approval after explaining its destination and storage. Do not read unrelated creator files or inherit the creator's key. No local adapter is bundled or required. If the host cannot configure credentials or deliver files securely, pause and explain the missing step.
