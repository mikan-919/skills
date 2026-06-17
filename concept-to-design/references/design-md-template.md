# DESIGN.md template — Google Labs open spec

`DESIGN.md` follows the **Google Labs / Stitch open specification** (Apache 2.0, alpha). One Markdown file, two layers: a **YAML front matter** block of machine-readable tokens, then **prose sections** explaining the rationale. AI agents (Claude Code, Cursor, Copilot) and the official `@google/design.md` CLI consume it.

This skill adds one discipline on top of the spec: **every token's prose entry cites the axiom id** (`A1`, `A4`…) from `CONCEPT_TO_DESIGN.md`. That keeps the standard artifact non-arbitrary without breaking the format.

Authoritative spec: `https://github.com/google-labs-code/design.md` → `docs/spec.md`. The shape below matches it; when in doubt, the upstream spec wins.

---

## Front matter schema

```yaml
version: alpha           # optional
name: <product name>     # REQUIRED
description: <one line>  # optional
colors:                  # at least `primary` is REQUIRED
  primary: "#0F141B"
  primary-60: "#2A3340"
  surface: "#161C26"
  on-surface: "#ECE6DA"
  muted: "#8B93A1"
  accent: "#F2B872"
typography:
  display-lg:
    fontFamily: "Shippori Mincho"
    fontSize: 46px
    fontWeight: 700
    lineHeight: 1.28
    letterSpacing: 0.01em
  body-md:
    fontFamily: "Zen Kaku Gothic New"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.7
  data-sm:
    fontFamily: "IBM Plex Mono"
    fontSize: 13px
    fontWeight: 500
spacing:
  base: 16px
  xs: 4px
  sm: 8px
  gutter: 24px
rounded:
  sm: 4px
  md: 10px
  full: 9999px
components:
  statBlock:
    color: "{colors.accent}"
    fontFamily: "{typography.data-sm}"
  logCard:
    backgroundColor: "{colors.surface}"
    padding: "{spacing.gutter}"
```

**Rules from the spec:**
- `name` mandatory; at least the `primary` color palette must be defined.
- Token references use brace notation: `"{colors.primary}"`, `"{typography.body-md}"`. Composite (whole-object) references are allowed **only inside `components:`**; elsewhere use primitive values.
- Colors are hex; typography is a named object (`fontFamily`/`fontSize`/`fontWeight`/`lineHeight`/`letterSpacing`); spacing & rounded are dimension values.

## Prose sections (h2, in this order)

Each section explains the *why* and cites axiom ids. Accepted aliases noted.

```markdown
## Overview            (alt: Brand & Style)
The product, its audience, the feel. State the one signature element here.

## Colors
Why this palette. Cite axioms. e.g. "Single warm accent `{colors.accent}` —
the one focus signal for an anxious audience (A4)."

## Typography
Role of each scale and its personality. e.g. "`data-sm` is mono so statistics
read as measured, not marketed (A2)."

## Layout            (alt: Layout & Spacing)
Density, grid intent, max width, breakpoints — density set by the audience axiom.

## Elevation & Depth  (alt: Elevation)
Shadow/elevation policy (or "flat — no elevation" if an axiom calls for it).

## Shapes
Radius language and what it signals.

## Components
What each recurring element is and how it behaves (roles, mapped to the
`components:` tokens above). Cite axioms.

## Do's and Don'ts
The forbidden moves from CONCEPT_TO_DESIGN.md, as concrete rules.
```

## Validation

- Official: `npx @google/design.md` (lints references, missing `primary`, WCAG contrast; can `export` to Tailwind config or W3C DTCG).
- Fallback (offline/alpha): `python3 scripts/validate_design.py <DESIGN.md>` → exit 0.

## Quality floor (carried into `implement`)

Responsive to mobile, visible keyboard focus, reduced-motion respected, AA contrast. The official linter checks contrast; the rest the implementer must honor.
