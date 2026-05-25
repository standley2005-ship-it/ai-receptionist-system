# AI Receptionist System

Prototype AI receptionist workflow for handling inbound business calls, collecting caller details, answering common questions, and preparing structured follow-up data for a CRM or booking system.

> Status: Prototype. This repository documents the system design, prompts, workflow logic, and webhook examples. It does not claim to be connected to a live phone system.

## Project Overview

This project shows how an AI receptionist could support small businesses by answering calls, qualifying the reason for the call, capturing contact information, and routing the request to the right follow-up workflow.

The goal is to demonstrate AI automation, prompt design, backend webhook thinking, and workflow documentation in a clean portfolio format.

## Features

- Receptionist system prompt for professional inbound call handling.
- Call intake workflow for new leads, existing customers, appointment requests, and missed-call follow-up.
- Example webhook payloads for appointment requests and lead intake.
- Architecture notes showing how a Vapi/OpenAI-style voice agent could connect to backend services.
- Safety notes for handling private customer data and avoiding secrets in source control.

## Tech Stack

- Prompt design
- Vapi/OpenAI-style voice agent architecture
- Webhooks and JSON payloads
- Python example webhook handler
- Markdown documentation

## Folder Structure

```text
ai-receptionist-system/
  README.md
  .gitignore
  docs/
    architecture.md
    security-notes.md
  prompts/
    receptionist-system-prompt.md
  workflows/
    call-flow.md
    intake-workflow.md
  webhooks/
    examples/
      appointment_request_payload.json
      lead_intake_payload.json
      python_webhook_example.py
  screenshots/
    .gitkeep
```

## Setup Instructions

1. Clone the repository.
2. Review `prompts/receptionist-system-prompt.md`.
3. Review the call workflow in `workflows/call-flow.md`.
4. Use the JSON examples in `webhooks/examples/` as templates for a future backend integration.
5. Run the local webhook example:

```bash
python webhooks/examples/python_webhook_example.py
```

6. Add environment variables locally if connecting to real services later. Do not commit API keys.

## Screenshots

Screenshots will be added after a live demo, dashboard mockup, or call-flow visualization is available.

## Future Improvements

- Add a small Flask or FastAPI webhook service.
- Add CRM integration examples.
- Add automated tests for webhook payload validation.
- Add a demo call transcript.
- Add dashboard screenshots once a UI exists.
