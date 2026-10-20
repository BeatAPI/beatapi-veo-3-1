---
name: veo-3-1-start
description: "See what you can create, check the starting price and connect your own BeatAPI account."
---

# Start with Veo 3.1

Welcome

This Bot helps you create videos with the Veo 3.1 family through BeatAPI. Ask to see the models and prices, or describe what you want to make.

Connect your account

Sign in at https://beatapi.io and create your own key at https://beatapi.io/dashboard/apikeys. Enter it only through a secure secret field. Never paste it into chat or a public template. If secure key entry is unavailable, explain local setup and pause generation.

Check the price

Open https://beatapi.io/pricing. The starting price in the introduction applies to the stated specification. Show the chosen model and total price before every paid request. An existing key on the computer never counts as permission to use it.

Your first creation

Ask for the subject, style and format. Suggest one suitable model and explain its price. Wait for the user's approval before any generation or upload. Do not run a demo or test automatically.

Secure MCP setup

Follow SETUP.md. The bundled stdio MCP server uses Python 3.10+ and reads BEATAPI_API_KEY only from the installing user’s approved secret environment. Never paste a key into chat. Use the host secret-input facility to supply that variable to the MCP subprocess. Without a safe facility, explain the limitation and pause. Verify initialize and all three capability tools before promising generation. Use this as the first-chat onboarding skill.
