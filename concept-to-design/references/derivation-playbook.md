# Derivation Playbook

How to get from a product concept to design axioms without either (a) making arbitrary choices or (b) collapsing into the generic AI-default look. Read this during the **derive** subcommand.

## Step 1 — Read the concept for design signal

Mine the concept docs (`CONTEXT.md`, `PRODUCT.md`, PRDs, ADRs, README framing) for these specific signals. Each is a lever on design:

| Signal in the concept | What it constrains |
|---|---|
| **The single job** of the product | The hero / first thing the eye lands on. The page's thesis. |
| **Audience + their emotional state** | Density, pace, tone, contrast. Anxious → calm, one-at-a-time. Expert/fast → dense, keyboard-first. |
| **Stated values & tradeoffs** | Honesty, privacy, restraint, playfulness — these become hard constraints (e.g. "honesty" forbids fabricated numbers). |
| **The subject's own world** | Its materials, instruments, artifacts, vernacular. This is where *distinctive* (non-generic) choices come from. A trajectory app → node/line motifs. A ledger → ruled columns. |
| **Forbidden moves** | Things the concept rules out (e.g. "we don't tell users what to do" → no prescriptive CTAs, no urgency banners). |
| **Information structure** | Sequences justify numbering (01/02/03); non-sequences don't. Distributions want charts, not flowcharts. Match the device to the true shape of the content. |

If a signal isn't in the docs, infer it explicitly and label it an assumption — don't silently invent.

## Step 2 — Classify every decision: forced vs free

For each design dimension (color, type, spacing, layout, motion, signature), ask: **"Does the concept leave a reasonable alternative?"**

- **Forced** — no reasonable alternative given the concept. These are your constraints. Examples:
  - audience is anxious → *one item at a time* (forced), not an enumerated list.
  - value is honesty → *show confidence intervals / "insufficient data"*, never a lone fabricated percentage.
  - product job is "relativize fear with others' trajectories" → the hero shows *many faint paths from one point*, not a marketing headline.
- **Free** — the concept constrains the *quality* but not the *value*. Examples:
  - "calm, warm" constrains the palette's mood, but the specific hue (lamp-amber vs muted sage vs dusk-rose) is free.
  - the typeface must read as "honest/literary," but which serif is free.
  - the signature motif must embody the subject, but its exact form is free.

**Rule of thumb:** if you can name two designs that both satisfy the concept, the dimension is *free* — and that's where you make a deliberate, opinionated, justifiable choice. Do not disguise a free choice as forced; that is exactly how derivations rationalize the templated default.

## Step 3 — Spend boldness on the free axes

The failure mode: deriving everything as "forced" and landing on a default look that appears regardless of subject (cream + high-contrast serif + terracotta; near-black + single acid accent; broadsheet hairlines + zero radius). These are legitimate only when the concept actually forces them — which is almost never.

For each **free axis**, take one real, justifiable aesthetic risk grounded in the subject's world. Restraint elsewhere: let one signature element be the memorable thing and keep the rest quiet. Record the justification — "chosen because the subject is X" — so it survives to `DESIGN.md` and isn't second-guessed as arbitrary.

## Step 4 — Derive the token set from the axioms

Map axioms down to concrete tokens, named per the Google `DESIGN.md` groups
(`colors` / `typography` / `spacing` / `rounded` / `components`). Every token's
prose entry cites the axiom that produced it.

- **colors**: 4–6 hex values, including a required `primary`. Ground/surface/muted from the mood axiom; one `accent` from the "single focus signal" axiom (resist a second accent unless an axiom demands it). Use palette steps (`primary-60`) only if a component needs them.
- **typography**: 2–3 named scales (e.g. `display-lg`, `body-md`, `data-sm`). Each scale's *personality* comes from a value axiom (literary, scientific, neutral) — set `fontFamily`/`fontSize`/`fontWeight`/`lineHeight`. Name the role's job, not just a font.
- **spacing & rounded**: dimension scales, density set by the audience axiom.
- **components**: map recurring elements (stat block, log card, entry) to token references (`"{colors.accent}"`) — this is where composite references are allowed.
- **Motion & signature** are not first-class Google token groups: record motion policy and the one signature element in the prose sections (`## Overview`, `## Components`), still citing axioms. The signature must embody a forced axiom *through* a free-axis form. Always gate motion on reduced-motion.

## Anti-checklist (review your own derivation)

- [ ] Could this exact design serve a different product? If yes, you under-derived — push more decisions onto concept evidence.
- [ ] Did everything come out "forced"? If yes, you're rationalizing a default — find the free axes and make real choices there.
- [ ] Does each token cite an axiom id?
- [ ] Is there exactly one signature element, with the rest disciplined and quiet?
- [ ] Does any structural device (numbering, dividers, eyebrows) encode something true, or just decorate?
