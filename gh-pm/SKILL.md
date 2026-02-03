---
name: gh-pm
description: Project-management triage plus GitHub Issues operations using GitHub CLI (gh). Use for chat-to-issue triage, backlog grooming, deduplication, and when creating/editing/closing/reopening/commenting/listing issues via gh.
---

# gh-pm

Merge PM triage rules with GitHub issue operations using `gh`.

## Use the PM prompt

- Use `PROMPT.md` as the system/initial instruction set when running the Telegram PM bot.
- Keep replies in Russian and output MarkdownV2 only (as specified in the prompt).

## Use GitHub CLI for issues

- Prefer `gh issue` commands for create/edit/close/reopen/list/comment.
- Run from the repo root or pass `-R owner/repo`.
- Use `gh issue comment` to attach rationale after edits, closes, and reopens.

### Common commands

```bash
gh issue list

gh issue create --title "Title" --body "Body" --label "bug" --assignee "octocat"

gh issue edit 123 --title "New title" --body "New body"

gh issue close 123

gh issue reopen 123

gh issue comment 123 --body "Reason for change"
```
