---
name: map-sync
description: Keep a repo's MAP.md in sync with its actual documentation. MAP.md is a routing index loaded into every agent session via `@MAP.md` in CLAUDE.md; it tells the agent which doc to read for which question. Use when the user wants to update, sync, regenerate, or fix MAP.md, says docs have moved/been added/removed, asks to refresh the doc routing table, or mentions `@MAP.md` / the MAP.md pattern.
---

# MAP.sync

**MAP.md is a routing index for agents, not prose for humans.** It is loaded into context at the start of every session (via `@MAP.md` in `CLAUDE.md`), so an agent can answer "which file do I read for X?" without searching. This skill's one job is to bring an **existing** MAP.md back in line with the docs that actually exist in the repo now.

Because it loads every session, MAP.md must stay **lean and accurate**: one terse line per document, stale entries are worse than missing ones, and bloat costs tokens on every turn.

## Workflow

1. **Locate the files.** Find `MAP.md` (repo root, or the path the user named) and `CLAUDE.md`. If MAP.md is missing, treat this as a sync from empty: bootstrap one — but say so, since the normal job is updating an existing map.

2. **Learn the existing map.** Read the current MAP.md first. Adopt its grouping, ordering, heading style, and line format — sync preserves the author's conventions, it does not impose new ones.

3. **Scan the doc set.** Walk the repo for routable docs: `*.md`, `docs/`, `design/`, `adr/`, runbooks, specs. **Exclude** noise (`node_modules`, `vendor`, `build`/`dist`, `.git`) and the files that aren't routing targets — MAP.md itself, and CLAUDE.md (it points *to* the map). For each doc, derive its "when to read" line from its title, top headings, and opening lines — what question sends a reader here.

4. **Diff, don't rewrite.** Compare the live doc set against the current map and compute the delta:
   - **Add** docs that exist but aren't listed.
   - **Fix** paths for docs that moved or were renamed.
   - **Remove** entries whose target file no longer exists.
   - **Refresh** a one-liner only when the doc's purpose has clearly drifted from its description.
   Leave accurate entries untouched.

5. **Show the delta, then write.** Present the changes as a short +/–/~ list and let the user confirm before writing MAP.md. Keep each entry to a single line; group related docs under short headings.

6. **Verify the hook.** Confirm `CLAUDE.md` contains an `@MAP.md` line so the map is actually loaded. If it's missing, point it out and offer to add it — a perfect MAP.md that nothing references is dead weight.

## MAP.md shape

Routing lines, grouped by domain. Path first (clickable), then the trigger:

```md
# Repository Map
_Routing index for agents. Read the matching doc before working in that area._

## Architecture & decisions
- `docs/architecture.md` — system overview; read before cross-cutting changes.
- `docs/adr/` — accepted decisions and their rationale; check before reversing a choice.

## Operations
- `docs/runbooks/deploy.md` — how to ship; read before any release step.
```

Write the trigger as *when to read it*, not a summary of contents.

## When NOT to use

- No MAP.md and the user wants a full from-scratch authoring pass with interviews → this skill is sync-focused; it bootstraps silently but won't interrogate.
- The user wants to write or restructure the underlying docs themselves → use `documentation`; sync the map afterward.
- A one-off "what doc covers X?" question → just answer it; don't rewrite the map.

## Notes

- One confirmation round on the delta, then write — don't drip changes file by file.
- Prefer linking a directory (`docs/adr/`) over enumerating every file inside it when they share one purpose.
- If the repo has no `@MAP.md` reference and no MAP.md, confirm the user wants the pattern before introducing it.
