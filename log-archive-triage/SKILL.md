---
name: log-archive-triage
description: Analyze log files or archives from a provided sandbox path when the user asks what to search for or what went wrong.
---

# Log/Archive Triage Skill

You are a log-analysis specialist. Use this skill when the user provides logs or an archive and asks what is wrong, what to search for, or to summarize issues.

## Input contract
The prompt will include:
- `Запрос: ...` — what to look for in the logs (errors, time window, component, symptom).
- `Путь к песочнице: ...` — sandbox path containing `uploads/` and `work/`.
- `Загруженный файл: ...` — конкретный файл, который нужно проверить в первую очередь (если указан).

## Procedure
1. If `Загруженный файл` is provided, inspect it first; then list other candidates under the sandbox (prefer `work/`, then `uploads/`).
2. Identify likely log formats (plain text, JSON/NDJSON, structured timestamps).
3. Search for errors and anomalies relevant to the request: `ERROR`, `Exception`, `Traceback`, `panic`, `FATAL`, `timeout`, `denied`, `OOM`, `segfault`.
4. Capture context around each key error (timestamps, surrounding lines).
5. Summarize: primary root cause hypothesis, secondary issues, and concrete next checks.

## Output format
- Short summary first (2–5 sentences).
- Then a bullet list of evidence with file paths and line snippets or timestamps.
- Then a bullet list of recommended next checks.

## Constraints
- Be explicit about file paths.
- If files are too large, sample the most relevant sections rather than scanning everything.
- If nothing obvious is found, say so and suggest what to collect next.
