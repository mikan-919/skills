# LAYOUT.md template

The structural spec, **derived from the concept** (not from the tokens) — a sibling
of `DESIGN.md`. It is machine-readable so `scripts/layout_preview.py` can validate
it and render an HTML+Tailwind structure preview deterministically. Every region cites the axiom (from
`CONCEPT_TO_DESIGN.md`) that justifies its existence.

Write at repo root (or `docs/`). Structure below.

---

````markdown
---
name: <product name>
concept_source: CONCEPT_TO_DESIGN.md
---

# <Product> — Layout

> Derived from the concept, in parallel with DESIGN.md. A region exists because
> the concept demands it, not because a token is available.

## Regions

Every region is a role with an axiom. Drop any region whose axiom column is empty —
that's decoration. The optional `binds` column is a late, incidental link to a
DESIGN.md component (never the reason the region exists).

| id      | role                                  | axiom | binds                  |
|---------|---------------------------------------|-------|------------------------|
| nav     | global navigation                     | A0    | —                      |
| hero    | trajectory thesis figure              | A3    | —                      |
| search  | current-situation input               | A7    | components.statBlock   |
| results | one-at-a-time outcome view            | A1    | components.logCard     |
| stat    | achievement rate + confidence interval| A2    | components.statBlock   |

## Reading order

The order regions are encountered (scroll/DOM). Encodes what the product wants
understood first; this is itself an axiom.

`hero → search → stat → results`  (A3: thesis before tool before data)

## Grid — base (narrow / mobile)

One region per row unless an axiom forces otherwise. Each line is a grid row;
space-separated ids are columns; repeating an id spans it. A region's footprint
must be a rectangle.

```layout-grid base
hero
search
stat
results
```

## Grid — wide

```layout-grid wide
nav     nav
hero    hero
search  stat
results results
```

## Responsive note

How `wide` collapses to `base`, and why (cite the focus axiom). e.g. "stat drops
below search rather than beside it; the one forced focus (results, A1) keeps full
width at every breakpoint."
````

---

## Grammar the script expects

- Front matter with `name`.
- A `## Regions` markdown table whose header includes `id` and `axiom` columns (and optionally `role`, `binds`).
- One or more fenced ` ```layout-grid <label> ` blocks. Each line is a row of
  whitespace-separated region ids; every row in a block must have the same column
  count. A repeated id forms a span and **must be rectangular**.
- Every id used in a grid must appear in the Regions table, and every region
  should appear in at least one grid (a region in the table but no grid is warned).
- Every region must cite a non-empty `axiom`.

`python3 scripts/layout_preview.py LAYOUT.md` validates these and writes
`layout-preview.html` — a structure-only HTML+Tailwind skeleton on a real CSS grid
(accurate region spans), one board per breakpoint. `--stdout` prints the HTML;
`--json` emits the parsed structure.
