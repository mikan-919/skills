---
name: concept-distill
description: Boil a fuzzy product idea down to a sharp CONCEPT.md by interrogating it one question at a time, grill-me style, until every load-bearing field is sharp enough to force a design decision. Use when the user wants to clarify or sharpen a product concept, distill a vague idea into something buildable, forge a CONCEPT.md, or prepare input for the concept-to-design skill.
---

# Concept Distill

Interrogate the user's product idea one question at a time — grounding each question in their own words — until all six fields are sharp enough to force a design decision. Use [references/interrogation-guide.md](references/interrogation-guide.md) as a question-pattern bank, never verbatim.

**The six fields:**
1. **Single job** — one sentence; what this does that nothing else does.
2. **Audience & state** — who, and their emotional state at the moment of use (not a demographic).
3. **Values** — 2–3 commitments, each phrased to **forbid** something (honesty → no fake numbers).
4. **Subject world** — domain vocabulary, materials, metaphors, artifacts.
5. **Forbidden moves** — what the concept rules out, and which value rules it out.
6. **Content shape** — sequence? distribution? one-at-a-time? Drives layout.

Offer a recommended answer drawn from what the user already said. Write only what they said — unsourced text gets deleted or turned into a question. A blank field beats an invented one.

When every field forces a downstream decision, write `CONCEPT.md`:

```markdown
---
name: <product>
---
# <Product> — Concept

## Single job
<one sentence>

## Audience & state
<who, and their emotional state at the moment of use>

## Values
- <value> — forbids <what>.

## Subject world
<vocabulary, materials, metaphors, artifacts of the domain>

## Forbidden moves
- <move> — ruled out by <which value/rule>.

## Content shape
<sequence | distribution | one-at-a-time | …> — <one line on why>
```

## When NOT to Use

- Concept already well-defined → use `concept-to-design` directly
- User wants to implement UI from an existing `DESIGN.md` → use `concept-to-design implement`
- User wants to critique an existing design → use `concept-to-design review`
