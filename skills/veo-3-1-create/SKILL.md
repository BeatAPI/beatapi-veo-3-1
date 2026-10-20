---
name: veo-3-1-create
description: "Turn your brief into a downloadable video, with the model and cost confirmed before generation."
---

# Create Veo 3.1 Videos

Plan the video

Clarify the subject, style, format and any reference material. Use the model selected with the user and follow its current BeatAPI input contract.

Confirm the request

Show the exact model, specification, reference inputs and price. Use only the key deliberately supplied by this installing user through secure entry. Never use an inherited account key. Get explicit approval for this paid request. Uploading a local reference file also requires explaining where it will be stored and getting permission.

Create once

Use the veo-3-1-protocol skill included in this plugin. Do not rely on files on the original creator's computer. Start one task, record its reference and idempotency key before sending it, and record the returned task identifier. If the response is uncertain or interrupted, reuse that record and resume the same task. Never create a second paid task silently.

Deliver the result

Wait for the existing task to finish. Use only the real output returned by BeatAPI, download it when supported, attach the file and provide its hosted link. If generation fails or the output is missing, explain that plainly. Never invent a file, link or successful result.

Respect the boundary

A request to connect an account or check current prices authorizes only the necessary nonbillable MCP connection and discovery checks with that user’s configured key. It never authorizes generation or an upload. Do not run tests or demos automatically.

Use only this host-configured MCP connection for execution. Do not call an old adapter from the original creator workspace.
