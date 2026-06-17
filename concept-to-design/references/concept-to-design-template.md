# CONCEPT_TO_DESIGN.md template

The derivation record — the part the Google `DESIGN.md` spec does **not** capture. Its job: make the design *non-arbitrary and reviewable*. Anyone reading it sees why each token follows from the concept, and which decisions were deliberate free choices. This file is the durable artifact; the Google `DESIGN.md` is its compiled output, and each token there cites an axiom id defined here.

Write it at the repo root (or `docs/`). Use the structure below verbatim.

---

```markdown
# Concept → Design

> Derived from: <concept docs read — CONTEXT.md, PRODUCT.md, ADRs…>
> Compiles to: DESIGN.md (Google Labs open spec)
> Generated: <YYYY-MM-DD>

## The concept in one paragraph

<2–4 sentences: the product's single job, its audience and emotional state,
its stated values. The referent for everything below.>

## Subject world

<The materials, instruments, artifacts, and vocabulary of this domain — the raw
material for distinctive (non-generic) choices. E.g. "a person is a flow of
nodes; trajectories; path-independence; one diary entry at a time.">

## Axioms

One row per design decision. `Forced` = the concept leaves no reasonable
alternative. `Free` = the concept constrains the quality, not the value, and the
choice is deliberate. `Forced→Free` = quality forced, specific value free (name
both). The `Token` column is the `DESIGN.md` path this axiom produces.

| ID | Decision | Concept evidence (quote/cite) | Forced / Free | The choice & why | Token(s) |
|----|----------|-------------------------------|---------------|------------------|----------|
| A1 | Result pacing | "1件ずつ表示…大量の情報を浴びる負担を避ける" | Forced | Swipe one card at a time; no enumerated list. | components.logCard |
| A2 | Number honesty | "足りないものは足りないと言える誠実さ" | Forced | CI + "insufficient data"; never a lone %. mono data type. | typography.data-sm |
| A3 | Hero thesis | Job: relativize fear via others' trajectories | Forced | Hero = faint paths fanning from one "now" point. | (signature) |
| A4 | Palette mood→hue | Audience anxious; value = quiet honesty | Forced→Free | Mood forced calm/warm; **hue free** → ink ground + warm bone + one lamp-amber. | colors.* |
| A5 | Display personality→face | Content is diary-like life logs | Forced→Free | Personality forced literary; **face free** → humanist mincho. | typography.display-lg |
| A6 | Signature element | Subject world: person = flow of nodes | Free | Node-and-trajectory marker, reused 3×. | components.* |

(Add rows until every `DESIGN.md` token has a source.)

## Free-axis bets

The deliberate, riskier choices and their justification, so they aren't later
mistaken for arbitrary. One short paragraph each.

- **<bet>**: chosen because <subject-world reason>. The restraint that pays for
  it: <what is kept quiet>.

## Forbidden moves

Things the concept rules out, with the rule that forbids them. These become the
`## Do's and Don'ts` section of `DESIGN.md`.

- <e.g. No prescriptive CTAs / urgency banners — the product "doesn't tell users
  what to do".>

## Open questions

Anything the concept didn't settle that a human should decide before implementation.
```

---

## Quality bar

- Every `DESIGN.md` token traces to an axiom id here (the `Token` column closes the loop).
- No decision marked `Forced` that another reasonable designer could have made differently — those are `Free` (or `Forced→Free`).
- At least one genuine `Free`-axis bet with a subject-world justification.
- The forbidden-moves list is concrete and maps to `## Do's and Don'ts`.
