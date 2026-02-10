#!/usr/bin/env python3
"""Generate an .ics file from structured JSON input.

Input JSON schema (object):
{
  "summary": "string",
  "start": "YYYY-MM-DDTHH:MM[:SS][+HH:MM|Z]",
  "end": "YYYY-MM-DDTHH:MM[:SS][+HH:MM|Z]",
  "duration_minutes": 30,
  "timezone": "Europe/Moscow",
  "location": "string",
  "description": "string",
  "attendees": ["alice@example.com", {"email":"bob@example.com","name":"Bob"}],
  "organizer": {"email":"host@example.com","name":"Host"},
  "uid": "optional-uid",
  "sequence": 0,
  "method": "PUBLISH|REQUEST|CANCEL",
  "status": "CONFIRMED|CANCELLED"
  "reminders": [15, 60]
}

Writes the .ics file and prints its path to stdout.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover
    ZoneInfo = None  # type: ignore


@dataclass
class Organizer:
    email: str
    name: str | None = None


@dataclass
class Attendee:
    email: str
    name: str | None = None


def parse_datetime(value: str) -> datetime:
    """Parse ISO-8601 datetime string."""
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Invalid datetime: {value}") from exc


def ensure_end(start: datetime, end: datetime | None, duration_minutes: int | None) -> datetime:
    if end:
        return end
    if duration_minutes is None:
        raise ValueError("Either end or duration_minutes must be provided")
    return start + timedelta(minutes=duration_minutes)


def load_input(path: str | None) -> dict:
    if path:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return json.load(sys.stdin)


def normalize_attendees(raw) -> list[Attendee]:
    attendees: list[Attendee] = []
    if not raw:
        return attendees
    for item in raw:
        if isinstance(item, str):
            attendees.append(Attendee(email=item))
            continue
        if isinstance(item, dict) and "email" in item:
            attendees.append(Attendee(email=item["email"], name=item.get("name")))
            continue
        raise ValueError("Invalid attendee format")
    return attendees


def normalize_organizer(raw) -> Organizer | None:
    if not raw:
        return None
    if isinstance(raw, dict) and "email" in raw:
        return Organizer(email=raw["email"], name=raw.get("name"))
    raise ValueError("Invalid organizer format")


def fmt_datetime(dt: datetime, tzid: str | None) -> tuple[str, str | None]:
    """Return (formatted, tzid_used)."""
    if dt.tzinfo is None:
        # floating time
        return dt.strftime("%Y%m%dT%H%M%S"), tzid

    if tzid:
        # Convert to target tz for consistent local time output
        if ZoneInfo is None:
            raise ValueError("zoneinfo is required for timezone output")
        dt = dt.astimezone(ZoneInfo(tzid))
        return dt.strftime("%Y%m%dT%H%M%S"), tzid

    # UTC output
    dt = dt.astimezone(timezone.utc)
    return dt.strftime("%Y%m%dT%H%M%SZ"), None


def line(key: str, value: str) -> str:
    return f"{key}:{value}"


def line_param(key: str, params: dict[str, str], value: str) -> str:
    params_str = "".join([f";{k}={v}" for k, v in params.items()])
    return f"{key}{params_str}:{value}"


def build_ics(data: dict) -> str:
    summary = data.get("summary") or "Meeting"
    start_raw = data.get("start")
    if not start_raw:
        raise ValueError("start is required")

    start = parse_datetime(start_raw)
    end = parse_datetime(data["end"]) if data.get("end") else None
    duration_minutes = data.get("duration_minutes")
    end = ensure_end(start, end, duration_minutes)

    tzid = data.get("timezone")
    if tzid and ZoneInfo is None:
        raise ValueError("timezone provided but zoneinfo is unavailable")

    start_fmt, tzid_used = fmt_datetime(start, tzid)
    end_fmt, _ = fmt_datetime(end, tzid_used)

    uid = data.get("uid") or f"{uuid.uuid4()}@codex"
    sequence = int(data.get("sequence") or 0)
    method = (data.get("method") or "PUBLISH").upper()
    status = (data.get("status") or "CONFIRMED").upper()

    dtstamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    lines: list[str] = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Codex//ICS Meeting Generator//EN",
        line("CALSCALE", "GREGORIAN"),
        line("METHOD", method),
        "BEGIN:VEVENT",
        line("UID", uid),
        line("DTSTAMP", dtstamp),
    ]

    if tzid_used:
        lines.append(line_param("DTSTART", {"TZID": tzid_used}, start_fmt))
        lines.append(line_param("DTEND", {"TZID": tzid_used}, end_fmt))
    else:
        lines.append(line("DTSTART", start_fmt))
        lines.append(line("DTEND", end_fmt))

    lines.append(line("SUMMARY", summary))
    lines.append(line("STATUS", status))

    if data.get("location"):
        lines.append(line("LOCATION", data["location"]))
    if data.get("description"):
        lines.append(line("DESCRIPTION", data["description"]))

    organizer = normalize_organizer(data.get("organizer"))
    if organizer:
        params = {}
        if organizer.name:
            params["CN"] = organizer.name
        lines.append(line_param("ORGANIZER", params, f"mailto:{organizer.email}"))

    for attendee in normalize_attendees(data.get("attendees")):
        params = {"RSVP": "FALSE"}
        if attendee.name:
            params["CN"] = attendee.name
        lines.append(line_param("ATTENDEE", params, f"mailto:{attendee.email}"))

    reminders = data.get("reminders") or []
    for minutes in reminders:
        try:
            minutes = int(minutes)
        except Exception as exc:
            raise ValueError("Invalid reminder minutes") from exc
        lines.extend(
            [
                "BEGIN:VALARM",
                line("ACTION", "DISPLAY"),
                line("DESCRIPTION", "Reminder"),
                line("TRIGGER", f"-PT{minutes}M"),
                "END:VALARM",
            ]
        )

    lines.append("END:VEVENT")
    lines.append("END:VCALENDAR")

    return "\r\n".join(lines) + "\r\n"


def build_filename(summary: str, start: datetime) -> str:
    safe_summary = "".join(ch if ch.isalnum() else "-" for ch in summary).strip("-")
    stamp = start.strftime("%Y%m%d-%H%M")
    if not safe_summary:
        safe_summary = "meeting"
    return f"{safe_summary}-{stamp}.ics".lower()


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate .ics from JSON input")
    parser.add_argument("--input", help="Path to JSON input file. If omitted, read stdin.")
    parser.add_argument("--outdir", default=".", help="Output directory")
    parser.add_argument("--outfile", help="Explicit output filename")
    args = parser.parse_args()

    data = load_input(args.input)
    ics_text = build_ics(data)

    start = parse_datetime(data["start"])
    filename = args.outfile or build_filename(data.get("summary") or "meeting", start)
    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)
    outpath = os.path.join(outdir, filename)

    with open(outpath, "w", encoding="utf-8", newline="\n") as f:
        f.write(ics_text)

    print(outpath)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
