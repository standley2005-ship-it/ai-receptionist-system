# Architecture

## Prototype Flow

```text
Inbound caller
  -> AI voice receptionist
  -> scripted intent and information capture
  -> webhook payload
  -> backend validation
  -> CRM, calendar, or follow-up queue
```

## Core Components

- Voice agent: Handles the conversation and follows the receptionist prompt.
- Prompt layer: Defines tone, business rules, intake questions, and escalation rules.
- Workflow layer: Separates lead intake, appointment requests, support requests, and missed-call follow-up.
- Webhook layer: Sends structured data to a backend service.
- Storage or CRM layer: Saves the request for human review or automation.

## Current Scope

This repository currently contains the design and examples for the workflow. It is not connected to a live Vapi account, OpenAI API key, phone number, CRM, or calendar.

