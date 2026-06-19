#!/usr/bin/env bash
# apply.sh — symlink a skill from this repo into ~/.claude/skills
#
#   ./apply.sh <skill-name>     link one skill (a directory here containing SKILL.md)
#   ./apply.sh all              link every skill in this repo
#   ./apply.sh                  list available skills
#
# Re-running is safe: an existing symlink is refreshed; a real directory is never
# overwritten.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"

is_skill() { [[ -f "$REPO_DIR/$1/SKILL.md" ]]; }

list_skills() {
  for d in "$REPO_DIR"/*/; do
    name="$(basename "$d")"
    is_skill "$name" && echo "  $name"
  done
}

link_one() {
  local name="$1"
  local src="$REPO_DIR/$name"
  local dest="$SKILLS_DIR/$name"

  if ! is_skill "$name"; then
    echo "error: '$name' is not a skill here (no $name/SKILL.md)" >&2
    return 1
  fi

  mkdir -p "$SKILLS_DIR"

  if [[ -L "$dest" ]]; then
    rm "$dest"                      # refresh an existing symlink
  elif [[ -e "$dest" ]]; then
    echo "error: $dest exists and is not a symlink — refusing to overwrite" >&2
    return 1
  fi

  ln -s "$src" "$dest"
  echo "linked  $dest -> $src"
}

main() {
  if [[ $# -eq 0 ]]; then
    echo "available skills in $REPO_DIR:"
    list_skills
    echo
    echo "usage: ./apply.sh <skill-name> | all"
    return 0
  fi

  if [[ "$1" == "all" ]]; then
    local rc=0
    for d in "$REPO_DIR"/*/; do
      name="$(basename "$d")"
      is_skill "$name" && { link_one "$name" || rc=1; }
    done
    return $rc
  fi

  link_one "$1"
}

main "$@"
