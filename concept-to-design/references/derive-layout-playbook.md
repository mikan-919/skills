# Derive-Layout Playbook

**This is CONCEPT → LAYOUT, not DESIGN → LAYOUT.** Layout is derived *directly from
the concept*, in parallel with the tokens — it is a sibling of `DESIGN.md`, both
children of the concept, **not** a downstream product of the tokens. A region
exists because the concept demands it, not because a token is available. Binding a
region to a token/component (a `stat` region uses `components.statBlock`) is a
*late, incidental* step; it never drives the structure.

Layout is axiomatized exactly like tokens: every structural decision is either
*forced* by the concept or a deliberate *free* choice — never arbitrary. Google's
DESIGN.md formalizes tokens but not spatial structure, so layout lives in a
companion **`LAYOUT.md`** (format: [layout-md-template.md](layout-md-template.md)),
and its axioms are recorded in the same concept-axiom ledger
(`CONCEPT_TO_DESIGN.md`) as everything else — the ledger is concept→everything.

Read this during the **derive** subcommand. It can run *before or alongside* token
derivation — neither depends on the other; both depend only on the concept.

## Step 1 — Read the concept for spatial signal

| Signal in the concept | What it forces about layout |
|---|---|
| **The single job / thesis** | What occupies the hero region — the most characteristic thing in the subject's world, in whatever form fits (figure, demo, headline). Not a default "big number + label". |
| **Audience + emotional state** | Density and focus. Anxious → single column, one focus per view, generous whitespace. Expert/fast → dense, multi-pane, keyboard regions. |
| **True shape of the content** | A *sequence* justifies an ordered, numbered stack; a *distribution* wants a chart region, not a flowchart; *one-at-a-time* content forbids an enumerated list region. Match the region to the data's real shape. |
| **Stated values / forbidden moves** | "We don't tell users what to do" → no urgency/CTA banner region. Privacy → no region that enumerates others' data. |
| **Reading order** | The order regions are *encountered* (DOM/scroll order) is itself an axiom — it encodes what the product wants understood first. |

## Step 2 — Classify each layout decision: forced vs free

Ask, per decision: **does the concept leave a reasonable alternative?**

- **Forced**: hero content; single- vs multi-column for this audience; whether results are one-at-a-time vs listed; reading order of regions; which regions are present at all.
- **Free**: the exact grid proportions, which side a secondary region sits on, gutter rhythm, where the signature element is placed.

Disguising a free choice as forced is how layouts converge on the generic
dashboard (sidebar + topbar + card grid). Forced axioms fix the regions and
order; free axes shape the grid.

## Step 3 — Define regions, then place them

1. **Enumerate regions** — each a role, not a component. `hero`, `search`, `results`, `stat`, `nav`. Every region must cite the axiom that justifies its existence (a region with no axiom is decoration — cut it).
2. **Order them** by the reading-order axiom (this is the `base`/narrow grid — a single column, top to bottom).
3. **Place them on a grid per breakpoint.** Narrow (`base`) is usually one column; wider breakpoints (`wide`) may span/pair regions. Each region's footprint must be a **rectangle** (the script enforces this).
4. **(Late, incidental) bind regions to tokens/components** from `DESIGN.md` where one happens to fit (a `stat` region uses `components.statBlock`). This binding is recorded for the implementer's convenience — it must never be the *reason* a region exists or is shaped a certain way. If a region needs a token that doesn't exist yet, that's a signal the token derivation missed an axiom, not a reason to reshape the layout.

## Step 4 — Responsive as an axiom, not an afterthought

How regions collapse from `wide` to `base` encodes priority: what stacks under
what, what hides, what stays. Derive it from the focus axiom — the single most
important region keeps its prominence at every width. Record both grids in
`LAYOUT.md`; the script renders each as an ASCII wireframe for review.

## Anti-checklist

- [ ] Could this layout serve a different product? If yes, under-derived — push regions/order onto concept evidence.
- [ ] Does every region cite an axiom? (No orphan decoration regions.)
- [ ] Did everything come out "forced"? Find the free axes (grid proportions, placement) and choose deliberately.
- [ ] Does the hero hold the subject's most characteristic thing, not a template default?
- [ ] Is the reading order justified by what the product wants understood first?
- [ ] Does the responsive collapse preserve the one forced focus at every width?
