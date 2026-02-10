# ICS Reference (Minimal)

## Required event fields
- `DTSTART`
- `DTEND` (or compute from duration)
- `SUMMARY`

## Update semantics (if user asks to edit)
- Reuse the same `UID`.
- Increment `SEQUENCE`.
- Update `DTSTAMP`.

## Cancellation (conceptual)
- Use `METHOD:CANCEL` and the same `UID`.
- Clients may ignore cancellation if the event was imported manually.

## Timezones
- If a timezone is provided, use `DTSTART;TZID=...` / `DTEND;TZID=...`.
- If no timezone is provided but timestamps include `Z` or offset, output UTC.

## Reminders
- Use `VALARM` with `TRIGGER:-PT{minutes}M` and `ACTION:DISPLAY`.
