#!/usr/bin/env python3
"""Validate a Google-spec DESIGN.md — offline fallback for `npx @google/design.md`.

Usage:
    python3 validate_design.py <path/to/DESIGN.md>          # validate, human report
    python3 validate_design.py <path/to/DESIGN.md> --json   # parsed tokens + errors as JSON

Checks (a subset of the official linter, no dependencies):
    - YAML front matter present and parses (2-space-indented subset)
    - `name` is set
    - a `primary` color is defined under `colors:`
    - every "{a.b.c}" token reference resolves to a defined path
    - required prose sections present (Overview/Colors/Typography), others warned

Exit: 0 valid · 1 invalid · 2 usage/file error. Not a full YAML parser — it
handles the indentation subset the DESIGN.md spec uses. When in doubt, the
official CLI is authoritative.
"""
import sys
import re
import json

REQUIRED_SECTIONS = ["Overview", "Colors", "Typography"]
SECTION_ALIASES = {"Overview": ["Brand & Style"]}
HEADING_RE = re.compile(r"^##\s+(.*?)\s*#*\s*$", re.MULTILINE)
REF_RE = re.compile(r"\{([A-Za-z0-9_.\-]+)\}")


def parse_frontmatter(text):
    """Parse the leading --- ... --- block as a nested dict (2-space indent subset)."""
    if not text.startswith("---"):
        return None, "no YAML front matter (file must start with '---')"
    end = text.find("\n---", 3)
    if end == -1:
        return None, "front matter not closed with '---'"
    block = text[3:end].strip("\n").splitlines()

    root = {}
    # stack of (indent, container_dict)
    stack = [(-1, root)]
    for raw in block:
        if not raw.strip() or raw.strip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key, val = key.strip(), val.strip()
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if val == "":
            child = {}
            parent[key] = child
            stack.append((indent, child))
        else:
            if (val.startswith('"') and val.endswith('"')) or (
                val.startswith("'") and val.endswith("'")
            ):
                val = val[1:-1]
            parent[key] = val
    return root, None


def all_paths(d, prefix=""):
    """Every dotted path (mappings and leaves) — reference targets."""
    out = set()
    for k, v in d.items():
        p = f"{prefix}{k}"
        out.add(p)
        if isinstance(v, dict):
            out |= all_paths(v, p + ".")
    return out


def validate(text):
    errors = []
    warnings = []

    fm, fm_err = parse_frontmatter(text)
    if fm_err:
        return {"valid": False, "errors": [fm_err], "warnings": [],
                "frontmatter": {}, "sections": []}

    if not fm.get("name"):
        errors.append("missing required field: name")

    colors = fm.get("colors")
    if not isinstance(colors, dict) or "primary" not in colors:
        errors.append("missing required color: colors.primary")

    # reference resolution
    defined = all_paths(fm)
    body_after = text[text.find("\n---", 3) + 4:]
    for ref in REF_RE.findall(text):
        if ref not in defined:
            errors.append(f"unresolved token reference: {{{ref}}}")

    # prose sections
    headings = [h.strip() for h in HEADING_RE.findall(body_after)]
    for sec in REQUIRED_SECTIONS:
        names = [sec] + SECTION_ALIASES.get(sec, [])
        if not any(any(n.lower() in h.lower() for n in names) for h in headings):
            errors.append(f"missing required section: ## {sec}")

    result = {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "frontmatter": fm,
        "sections": headings,
    }
    return result


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

    result = validate(text)

    if "--json" in flags:
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0 if result["valid"] else 1

    fm = result["frontmatter"]
    if result["valid"]:
        ncolors = len(fm.get("colors", {}) or {})
        ntype = len(fm.get("typography", {}) or {})
        print(f"OK  {args[0]}  — '{fm.get('name', '(unnamed)')}', "
              f"{ncolors} colors, {ntype} type scales")
        return 0
    print(f"INVALID  {args[0]}", file=sys.stderr)
    for e in result["errors"]:
        print(f"  - {e}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
