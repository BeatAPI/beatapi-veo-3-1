# Veo 3.1 Video Generator

Create affordable 8 second videos with audio using Veo 3.1 Lite, Fast or Quality. From $0.15 at 720p. Connect your own BeatAPI key and confirm the price before generating.

[Open the Grok Bot template](https://x.ai/bot/CAflVtH2t2gHnS7mRMMHa) · [Get an API key](https://beatapi.io/dashboard/apikeys) · [See current prices](https://beatapi.io/pricing)

## What you can do

Choose from the complete model family, compare the current specification and price, and generate only after approving one request. The bot resumes the same task after interruption and delivers the actual output file and link.

[Complete model catalogue and price tiers](MODELS.md)

## Get started

Install this plugin with stdio MCP support and Python 3.10+. Follow [SETUP.md](SETUP.md) to create your own BeatAPI key and supply it through the host's secure credential facility. No pip dependencies, creator key or creator workspace files are needed.

Four skills cover getting started, models and prices, generation and delivery, and the execution protocol. The bundled MCP server scopes discovery and execution to this family and never starts a demo automatically.

## Try asking

“Show me the models and current prices.”

“Help me connect my BeatAPI account securely.”

“Recommend a model for my brief, quote the price, and wait for my approval.”

## Verification

See [VERIFICATION.md](VERIFICATION.md) for real image evidence and package checks, and [GROK_APP_VERIFICATION.md](GROK_APP_VERIFICATION.md) for passed nonbillable Grok installation/host checks and their limits. Image tests do not certify every model or video generation. This is an independent BeatAPI integration.

Run the nonbillable, no-network bridge checks with `python3 -m unittest discover -s tests`.
