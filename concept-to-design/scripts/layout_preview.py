#!/usr/bin/env python3
"""Validate a concept-derived LAYOUT.md and emit an HTML+Tailwind structure preview.

Usage:
    python3 layout_preview.py <path/to/LAYOUT.md>            # validate + write preview HTML
    python3 layout_preview.py <path/to/LAYOUT.md> --stdout   # print HTML instead of writing
    python3 layout_preview.py <path/to/LAYOUT.md> --json     # parsed structure as JSON

The preview is structure-only: each region is a labelled, dashed box placed on a
real CSS grid (Tailwind), so region spans render accurately — no visual design,
just the skeleton. Layout is CONCEPT-derived: a region exists because the concept
demands it.

Validates (deterministic, no dependencies):
    - every region in `## Regions` cites a non-empty axiom
    - every id used in a ```layout-grid block is defined in the table
    - every grid row in a block has the same column count
    - each region's footprint in a grid is a rectangle (CSS-grid-area rule)
    - regions defined but used in no grid are warned

Exit: 0 valid · 1 invalid · 2 usage/file error.
"""
import sys
import os
import re
import json
import html

GRID_RE = re.compile(r"```layout-grid\s+(\S+)\s*\n(.*?)\n```", re.DOTALL)
TABLE_ROW_RE = re.compile(r"^\s*\|(.+)\|\s*$")
# widen the preview container per breakpoint label so it reads like that width
WIDTH = {"base": "max-w-sm", "narrow": "max-w-sm", "mobile": "max-w-sm",
         "wide": "max-w-4xl", "desktop": "max-w-4xl"}


def front_name(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            for line in text[3:end].splitlines():
                if line.strip().startswith("name:"):
                    return line.split(":", 1)[1].strip()
    return None


def parse_regions(text):
    m = re.search(r"##\s+Regions\s*\n(.*?)(?:\n##\s|\Z)", text, re.DOTALL)
    regions = {}
    if not m:
        return regions, "missing '## Regions' table"
    rows = []
    for line in m.group(1).splitlines():
        rm = TABLE_ROW_RE.match(line)
        if rm:
            rows.append([c.strip() for c in rm.group(1).split("|")])
    if not rows:
        return regions, "no table rows under '## Regions'"
    header = [h.lower() for h in rows[0]]
    if "id" not in header:
        return regions, "Regions table header must include an 'id' column"
    i_id = header.index("id")
    idx = {k: (header.index(k) if k in header else None) for k in ("role", "axiom", "binds")}
    for cells in rows[1:]:
        if all(set(c) <= {"-", ":"} for c in cells):
            continue
        if i_id >= len(cells) or not cells[i_id]:
            continue
        regions[cells[i_id]] = {
            k: (cells[i] if i is not None and i < len(cells) else "")
            for k, i in idx.items()
        }
    return regions, None


def parse_grids(text):
    grids = {}
    for label, body in GRID_RE.findall(text):
        grids[label] = [line.split() for line in body.splitlines() if line.strip()]
    return grids


def bbox(rows, rid):
    pts = [(r, c) for r, row in enumerate(rows) for c, x in enumerate(row) if x == rid]
    r0 = min(p[0] for p in pts); r1 = max(p[0] for p in pts)
    c0 = min(p[1] for p in pts); c1 = max(p[1] for p in pts)
    rect = len(pts) == (r1 - r0 + 1) * (c1 - c0 + 1)
    return (r0, c0, r1, c1, rect)


def validate(name, regions, grids):
    errors, warnings = [], []
    if not name:
        errors.append("missing front matter field: name")
    for rid, meta in regions.items():
        if not meta["axiom"]:
            errors.append(f"region '{rid}' cites no axiom (decoration — give it one or cut it)")
    used = set()
    for label, rows in grids.items():
        if not rows:
            errors.append(f"grid '{label}' is empty"); continue
        ncols = len(rows[0])
        if any(len(r) != ncols for r in rows):
            errors.append(f"grid '{label}': rows have unequal column counts"); continue
        seen = set()
        for row in rows:
            for rid in row:
                used.add(rid)
                if rid not in regions:
                    errors.append(f"grid '{label}': undefined region id '{rid}'")
                elif rid not in seen:
                    seen.add(rid)
                    if not bbox(rows, rid)[4]:
                        errors.append(f"grid '{label}': region '{rid}' is not a rectangle")
    for rid in regions:
        if rid not in used:
            warnings.append(f"region '{rid}' is defined but used in no grid")
    if not grids:
        errors.append("no ```layout-grid blocks found")
    return errors, warnings


def render_html(name, regions, grids):
    def esc(s):
        return html.escape(s or "")

    boards = []
    for label, rows in grids.items():
        if not rows:
            continue
        nrows, ncols = len(rows), len(rows[0])
        cells = []
        for rid in dict.fromkeys(x for row in rows for x in row):
            r0, c0, r1, c1, _ = bbox(rows, rid)
            meta = regions.get(rid, {})
            cls = (f"col-start-[{c0 + 1}] col-span-[{c1 - c0 + 1}] "
                   f"row-start-[{r0 + 1}] row-span-[{r1 - r0 + 1}] "
                   "border border-dashed border-slate-400 rounded-lg p-3 "
                   "flex flex-col gap-1 bg-white/60")
            ax = f'<span class="ml-auto text-[10px] font-mono text-amber-600">{esc(meta.get("axiom"))}</span>'
            cells.append(
                f'<div class="{cls}">'
                f'<div class="flex items-center gap-2"><span class="font-semibold text-slate-800">{esc(rid)}</span>{ax}</div>'
                f'<div class="text-xs text-slate-500">{esc(meta.get("role"))}</div>'
                f'</div>')
        grid_style = (f"[grid-template-columns:repeat({ncols},minmax(0,1fr))] "
                      f"[grid-template-rows:repeat({nrows},minmax(72px,auto))]")
        maxw = WIDTH.get(label, "max-w-2xl")
        boards.append(
            f'<section class="mb-10">'
            f'<h2 class="text-xs font-mono uppercase tracking-widest text-slate-400 mb-2">{esc(label)}</h2>'
            f'<div class="mx-auto {maxw} border border-slate-200 rounded-xl p-3 bg-slate-100">'
            f'<div class="grid gap-3 {grid_style}">{"".join(cells)}</div>'
            f'</div></section>')

    return (
        "<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        f"<title>{esc(name)} — layout structure</title>"
        "<script src=\"https://cdn.tailwindcss.com\"></script></head>"
        "<body class=\"bg-slate-50 text-slate-900 p-8 font-sans\">"
        f"<h1 class=\"text-lg font-semibold mb-1\">{esc(name)} — layout structure</h1>"
        "<p class=\"text-sm text-slate-500 mb-8\">Structure only. Each box is a region "
        "(id, role, axiom) placed on a real CSS grid; spans are accurate. "
        "Derived from the concept, not the tokens.</p>"
        f"{''.join(boards)}</body></html>\n")


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    flags = {a for a in argv[1:] if a.startswith("--")}
    if len(args) != 1:
        sys.stderr.write(__doc__)
        return 2
    try:
        with open(args[0], encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        sys.stderr.write(f"error: cannot read {args[0]}: {e}\n")
        return 2

    name = front_name(text)
    regions, rerr = parse_regions(text)
    grids = parse_grids(text)
    errors, warnings = validate(name, regions, grids)
    if rerr:
        errors.insert(0, rerr)

    if "--json" in flags:
        json.dump({"name": name, "regions": regions, "grids": grids,
                   "errors": errors, "warnings": warnings, "valid": not errors},
                  sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0 if not errors else 1

    if errors:
        print(f"INVALID  {args[0]}", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    doc = render_html(name, regions, grids)
    if "--stdout" in flags:
        sys.stdout.write(doc)
    else:
        out = os.path.join(os.path.dirname(os.path.abspath(args[0])), "layout-preview.html")
        with open(out, "w", encoding="utf-8") as f:
            f.write(doc)
        print(f"OK  '{name}', {len(regions)} regions, {len(grids)} grid(s)")
        for w in warnings:
            print(f"note: {w}")
        print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
