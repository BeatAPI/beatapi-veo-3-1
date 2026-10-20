# Veo 3.1 Video Generator verification

No model in this video family was run. All family model IDs and current contracts were inspected.

# Image verification, 2026-10-21

Three real image tasks succeeded through the configured BeatAPI MCP service. The listed input tier was 1K for each task; actual returned pixel dimensions are recorded below. Total advertised price: USD 0.05. Total final task settlement: 0.05 credits; no refund was recorded for these tasks.

The client performed initialize, tools/list, discovery, inspect, paid start, same-task status polling, HTTPS download and full image decode. Credentials were not sent to the download URLs. Tests used an owner-authorized credential and explicit bounded image-test authorization. No credential or private task receipt is included here.

| Model | Operation | Actual pixels | Settled credits | Result |
| --- | --- | --- | --- | --- |
| gpt-image-2.5-flare | text to image | 1254x1254 | 0.015 | downloaded, decoded and visually checked |
| gpt-image-2.5-sunburst | text to image | 1254x1254 | 0.015 | downloaded, decoded and visually checked |
| nano-banana-2-lite | image editing | 1024x1024 | 0.02 | downloaded, decoded and visually checked |

The Nano Banana task used the first generated image's returned public URL as its reference. No local reference upload was performed. Visual inspection confirmed the requested lavender robot and yellow watering can. The GPT Image still life contains the requested three colored forms. These are functional checks, not a general quality benchmark.

Unverified: fresh Grok Bot installation, host secure key setup, native agent tool selection and file attachment, other model variants, uploads and all video generation. Current contracts for all 18 family model IDs were inspected, which is distinct from generation on each model. The three video plugins have no video runtime pass from these image tests.

## Stdio package checks, 2026-10-21

The bundled Python 3.10+ server passed 10 no-network unit checks covering MCP lifecycle, missing credentials, family isolation, exact model/reference matching, mandatory idempotency, explicit operation, original-task polling, fixed HTTPS destination, redirect rejection and credential redaction. The start-forwarding unit check uses a stub transport only; it does not start a real task.

A separate fresh-process stdio check with the owner's explicitly authorized Social Media credential passed live nonbillable discovery of this complete family and contract inspection. Without a credential, initialize/tools/list work locally, while a capability call fails closed without sending HTTP. No new paid task was started by these stdio connection checks. See stdio-connection-verification.json.

The earlier three real image tests used a direct MCP HTTP client, not this new stdio process or a native Grok agent. Grok fresh-install and secure key entry remain pending; no video runtime pass is claimed. A key must be supplied to the MCP subprocess through a supported secure host facility; installation alone does not connect a paid account.
