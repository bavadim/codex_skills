---
name: ics-meeting-generator
description: Generate valid .ics calendar invite files from natural language or structured details. Use when the user asks to create a meeting, calendar invite, or .ics file, or to prepare an update/cancellation .ics (no direct calendar API).
---

# ICS Meeting Generator

## Overview

Generate valid `.ics` files for calendar events with minimal dependencies. The workflow is: clarify missing details, convert the request into structured event fields, and call the generator script to write the `.ics` file.

## Workflow

1. Collect required fields

Required: `start`, `end` (or `duration_minutes`), `timezone`.
Suggested: `summary`, `location`, `description`, `attendees`, `reminders`.

If any required field is missing, ask a short, targeted question. Keep it to one question at a time.

2. Handle edit/cancel intent (planning only)

If the user asks to edit/cancel an existing meeting, you still generate an `.ics` update. Ask for the original `UID` (or the original `.ics` file). If the `UID` is unknown, tell the user this will create a new event instead of updating.

3. Generate the .ics

Use `scripts/create_ics.py`. Provide a JSON object with the event fields. The script writes the file and prints the output path.

## Script Usage

Generate from stdin JSON:

```bash
cat <<'JSON' | python3 scripts/create_ics.py --outdir ./out
{
  "summary": "Team Sync",
  "start": "2026-02-10T14:00:00",
  "duration_minutes": 30,
  "timezone": "Europe/Moscow",
  "location": "Zoom",
  "description": "Weekly sync",
  "attendees": ["alice@example.com", {"email":"bob@example.com","name":"Bob"}],
  "reminders": [15]
}
JSON
```

Generate from a JSON file:

```bash
python3 scripts/create_ics.py --input event.json --outdir ./out
```

Explicit output filename:

```bash
python3 scripts/create_ics.py --input event.json --outdir ./out --outfile custom.ics
```

## Edit/Cancel Guidance (for future capability)

- Update: reuse the same `UID`, increment `SEQUENCE`, update `DTSTAMP`.
- Cancel: use `METHOD:CANCEL` with the same `UID`.
- If no `UID` is available, confirm to the user that a new event will be created.

For detailed field rules, see `references/ics.md`.
