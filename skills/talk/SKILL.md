---
name: talk
description: Discussion-only mode. Use when the user invokes /talk followed by a question or topic — they want to talk through an idea or decision before any code is written or action taken.
allowed-tools: Read, Grep, Glob
---

# Discussion-only mode (/talk)

The user has invoked `/talk`. This means: **do not take any action, do not write or edit code, do not run build/test commands.** They want to talk through the idea first and reach a decision together.

## How to respond

1. Treat the rest of the user's message (everything after `/talk`) as a topic for discussion, not a task.
2. **Actually answer the question.** Even if it's phrased as "can you do X" — don't just refuse and say "I'm in discussion mode." Answer it: yes it's doable / no it isn't / here's how it would work / here are the tradeoffs. Engage with substance.
3. Share your honest take — tradeoffs, risks, alternatives, what you'd want to know before deciding.
4. Ask clarifying questions if the right answer depends on context you don't have.
5. Do **not** start implementing, scaffolding, editing files, or running build/test commands. Reading a file or two for context is fine if needed to give a grounded opinion.
6. Do **not** end with offers like "want me to…" or "should I…" — just discuss and stop. Wait for the user to say "ok let's do it" (or similar) before doing anything.

## Examples

- `/talk can we use react here` → Discuss whether React fits this project: what's already in the stack, what the alternatives would be, tradeoffs. Don't install anything.
- `/talk should we split this into two services` → Talk through the architecture tradeoff. Don't refactor.
- `/talk is this test flaky or is there a real bug` → Discuss what the symptoms suggest. Reading the test is fine; don't "fix" it.
