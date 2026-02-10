---
name: link-to-textbook
description: Use for turning a list of tech articles (scientific or popular) into a concise Markdown mini-textbook for engineers. Extract key questions, separate core ideas from narrative/ anecdotes, and write a connected, question-driven summary with inline source links.
---

# Link To Textbook

## Overview

Turn a list of URLs into a compact, engineer-focused Markdown textbook. The output is a connected narrative that answers extracted key questions in order, while keeping anecdotes and narrative fragments in a separate section. Important claims include inline links to sources.

## Workflow

### 1. Inputs and Scope

Collect:
- List of URLs (articles, papers, blog posts, press, reports)
- Optional: topic name, desired depth (default: concise summary), any exclusions

Assume audience: technical, time-constrained engineers.

### 2. Fetch and Normalize Sources

For each URL:
- Fetch the main article content (skip nav, ads, comments, boilerplate).
- If paywalled or inaccessible, note the limitation in the final output.
- Track source title, author/org, and date if available.

### 3. Extract Key Questions (Before Summarizing)

Derive 5–12 questions the sources collectively answer. These drive the narrative order.

Use engineering-friendly question templates as a baseline:
- What problem is being solved and why now?
- What is the core idea / mechanism?
- How does it work (architecture, algorithm, process)?
- What are the tradeoffs, limits, or failure modes?
- What evidence supports the claims (benchmarks, studies)?
- What is required to implement or adopt it?
- How does it compare to prior art or alternatives?

Merge and deduplicate questions across sources. Keep them in a logical learning order.

### 4. Separate Core Ideas vs Narrative

Classify content into:
- **Core ideas**: definitions, mechanisms, results, constraints, methods.
- **Narrative**: anecdotes, historical stories, personal commentary, case stories.

Do not lose narrative content, but keep it out of the main explanatory flow.

### 5. Build the Markdown Textbook

Write a connected narrative that answers the key questions sequentially. Keep it concise and technical.

Rules:
- Provide inline Markdown links to sources for important claims or facts.
- Prefer precise, minimal phrasing. No filler.
- Keep structure minimal and consistent.

Use this template (adapt titles if the user provided a topic):

```markdown
# <Topic Title>

## Ключевые вопросы
- Q1
- Q2
- Q3

## Связное объяснение
Параграфы идут в порядке вопросов и отвечают на них последовательно.
Вставляй важные ссылки прямо в текст: [Источник](URL).

## Ключевые идеи (кратко)
- Идея 1 (1–2 строки)
- Идея 2

## Определения
- Термин: определение

## Методы/архитектуры
- Метод/блок: кратко, по сути

## Нарратив и кейсы (отдельно)
- Кейс/история: 1–2 строки, только если важны для контекста

## Вопросы для самопроверки
- Вопрос 1
- Вопрос 2

## Источники
- [Название источника](URL)
```

### 6. Quality Checklist

Before finalizing:
- Все ключевые утверждения имеют ссылки.
- Нарратив не смешан с сутью.
- Вопросы покрыты и ответы идут по порядку.
- Текст лаконичен и полезен инженеру.
