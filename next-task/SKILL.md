---
name: next-task
description: Pick up the next task from a project's CONTEXT.md / STATUS.md (or similar), restate it to confirm understanding, and start implementing — but if anything in the task is ambiguous or under-specified, ask the user first and wait before writing code. Use when the user says "do the next task", "pick up the next task", "check and start the next task", "implement what's next", or points at a CONTEXT.md / STATUS.md / TODO file and asks you to proceed.
---

# Next Task

Pull the next task from the project's task source, confirm you understood it, and implement it — but **never start coding while anything is ambiguous**. The whole point of this skill is the clarify-before-build gate: a wrong guess is more expensive than a question.

## Workflow

1. **Find the task source.** Look, in order, for `STATUS.md`, `CONTEXT.md`, then `TODO.md` / `TASKS.md` / `PLAN.md` at the repo root (or a path the user named). The "next task" is the first unchecked / in-progress / top-of-queue item. If several files exist or it's unclear which item is next, ask which one.

2. **Restate the task.** In 1–3 sentences, say back what you believe the task is and what "done" looks like — in your own words, grounded in the file's wording. This surfaces misreadings before they cost anything.

3. **Scan for ambiguity (the gate).** Check the task against the list below. If **any** item is unclear or undefined, **stop and ask the user** — batch all your questions into one message, each with a recommended default drawn from the codebase. Do not write or edit code until every question is resolved.

   Ask first when:
   - The expected behavior, output, or acceptance criteria has more than one reasonable reading.
   - A name, type, signature, schema, file path, or API contract isn't pinned down.
   - It touches an external service, credential, irreversible action, or public-facing change.
   - The task depends on a decision the file doesn't record (which library, which pattern, where it lives).
   - Scope is open-ended ("improve X", "handle errors") without a concrete boundary.

   If nothing is ambiguous, say so in one line and proceed — don't manufacture questions.

4. **Implement.** Once the task is sharp, build it following the surrounding code's conventions. Verify it works (tests / run) before claiming done.

5. **Update the task source.** Mark the item done / move it out of the queue in `STATUS.md` (or wherever you found it), and note the next task if the user wants to continue.

## When NOT to Use

- No task file exists and the user hasn't named a task → ask what to work on, or just take the request directly; there's no "next task" to pick up.
- The user wants a fully autonomous, no-check-in run across many tasks → this skill deliberately gates on questions; that's the opposite of AFK.
- A single, fully-specified task is given inline with no ambiguity → just implement it; no need to route through this skill.
- The user wants to *plan* or break work into tasks rather than execute the next one → use a planning skill (e.g. `to-issues`, `request-refactor-plan`).

## Notes

- One ambiguity-questions round, not a drip-feed — gather everything, ask once, then build.
- A recommended default per question keeps the round cheap for the user to answer.
- If the user already answered the ambiguities in their request, skip step 3's questions and proceed.
