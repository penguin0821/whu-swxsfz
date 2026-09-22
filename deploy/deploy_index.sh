#!/usr/bin/env bash
# Update the live site (index.html at repo root) on GitHub Pages.
#
# Uses the GitHub Contents API instead of `git push`, so it works even where
# the local git https remote-helper is unavailable. Only touches index.html;
# for a full working-tree sync use deploy/publish_all.py.
#
# Usage:
#   ./deploy/deploy_index.sh [path/to/index.html]
# Env:
#   REPO    owner/repo   (default penguin0821/whu-swxsfz)
#   BRANCH  branch name  (default main)
#   GH      gh binary    (default gh)
# Requires: gh (authenticated), base64.
set -euo pipefail

REPO="${REPO:-penguin0821/whu-swxsfz}"
BRANCH="${BRANCH:-main}"
GH="${GH:-gh}"
FILE="${1:-index.html}"

[ -f "$FILE" ] || { echo "no such file: $FILE" >&2; exit 1; }

echo "deploying $FILE -> $REPO@$BRANCH ..."
B64=$(base64 < "$FILE" | tr -d '\n')

# existing blob sha (needed for updates; empty for first-time create)
SHA=$("$GH" api "repos/$REPO/contents/index.html?ref=$BRANCH" -q .sha 2>/dev/null || true)

TMP=$(mktemp)
if [ -n "$SHA" ]; then
  printf '{"message":"site: rebuild %s","content":"%s","branch":"%s","sha":"%s"}' \
    "$(date +%F)" "$B64" "$BRANCH" "$SHA" > "$TMP"
else
  printf '{"message":"site: publish %s","content":"%s","branch":"%s"}' \
    "$(date +%F)" "$B64" "$BRANCH" > "$TMP"
fi

"$GH" api -X PUT "repos/$REPO/contents/index.html" --input "$TMP" -q '.content.sha' >/dev/null
rm -f "$TMP"

echo "done. GitHub Pages rebuilds in ~30s:"
echo "  https://${REPO%%/*}.github.io/${REPO##*/}/"
echo "check status: $GH api repos/$REPO/pages -q .status   (wait for 'built')"
