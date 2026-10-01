#!/usr/bin/env bash
# publish_paths.sh, two properties, in a throwaway repo.
#
# TEST 1 is the one that matters and it is DETERMINISTIC, because it tests the mechanism the fix
# rests on rather than trying to win a timing race: build a commit against a pinned base, move HEAD
# underneath it the way a peer's commit does, then attempt the ref update BOTH ways.
#   - two-argument update-ref (what the script used to do) overwrites and the peer's commit is lost;
#   - three-argument update-ref (the fix) refuses, writes nothing, and the peer survives.
# TEST 2 is an end-to-end smoke test of the whole script.
set -euo pipefail

SCRIPT="$(cd "$(dirname "$0")" && pwd)/publish_paths.sh"
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
cd "$T"; git init -q .; git config user.email t@t; git config user.name t
echo base > mine.md; echo "peer original" > peer.md
git add -A; git commit -qm base

fail=0

# ---------------- TEST 1: the ref update itself ----------------
BASE="$(git rev-parse HEAD)"
# a private index built against BASE, carrying only our own change
IDX="$T/idx"; GIT_INDEX_FILE="$IDX" git read-tree "$BASE"
echo "mine changed" > mine.md
GIT_INDEX_FILE="$IDX" git add -- mine.md
TREE="$(GIT_INDEX_FILE="$IDX" git write-tree)"

# ...and NOW the peer commits, exactly inside the window
echo "peer NEW WORK" > peer.md
git add peer.md; git commit -qm "peer commits inside the window"
PEER="$(git rev-parse HEAD)"

OURS="$(git commit-tree "$TREE" -p "$BASE" -m ours)"

echo "--- TEST 1: three-argument (compare-and-swap) update-ref ---"
if git update-ref -m cas HEAD "$OURS" "$BASE" 2>/dev/null; then
    echo "  FAIL: it wrote even though HEAD had moved"; fail=1
else
    echo "  refused, as it must"
    [ "$(git rev-parse HEAD)" = "$PEER" ] && echo "  HEAD still the peer's commit" \
        || { echo "  FAIL: HEAD changed anyway"; fail=1; }
    git show HEAD:peer.md | grep -q "NEW WORK" && echo "  peer's work intact" \
        || { echo "  FAIL: peer's work gone"; fail=1; }
fi

echo "--- TEST 1b: two-argument update-ref, the old behaviour, for contrast ---"
git update-ref -m old HEAD "$OURS"
if git show HEAD:peer.md 2>/dev/null | grep -q "NEW WORK"; then
    echo "  FAIL: expected the old form to lose the peer's work, but it did not"; fail=1
else
    echo "  peer's work written out, and their commit is $(git merge-base --is-ancestor "$PEER" HEAD \
         && echo 'still an ancestor' || echo 'NO LONGER AN ANCESTOR') -- this is the bug the fix removes"
fi

# ---------------- TEST 2: end-to-end ----------------
git update-ref HEAD "$PEER"; git checkout -q -- . 2>/dev/null || true
echo "mine changed again" > mine.md
printf 'msg\n' > "$T/m"
bash "$SCRIPT" "$T/m" mine.md >/dev/null 2>&1
echo "--- TEST 2: end-to-end publish ---"
[ "$(git show HEAD:mine.md)" = "mine changed again" ] && echo "  named path published" \
    || { echo "  FAIL: named path not published"; fail=1; }
git show HEAD:peer.md | grep -q "NEW WORK" && echo "  peer's file untouched" \
    || { echo "  FAIL: peer's file changed"; fail=1; }

# ---------------- TEST 3: a peer's STAGED file cannot enter our commit ----------------
#
# This is the property the private index exists for, and the one the removed
# `git commit --amend --author=...` used to break: the amend rebuilt the commit from the
# REPOSITORY index, so anything a peer had staged went in with it. The amend is gone - identity
# now goes in through GIT_AUTHOR_* before commit-tree - but "we deleted the call" is not a test.
echo "peer STAGED not committed" > peer_staged.md
git add peer_staged.md                      # peer's work sits in the REPOSITORY index
echo "mine third" > mine.md
printf 'msg3\n' > "$T/m3"
bash "$SCRIPT" "$T/m3" mine.md >/dev/null 2>&1

echo "--- TEST 3: peer-staged file must not enter the publication ---"
if git show --stat --format= HEAD | grep -q peer_staged.md; then
    echo "  FAIL: the peer's staged file was swept into our commit"; fail=1
else
    echo "  peer's staged file is NOT in the commit"
fi
if git ls-files --cached | grep -q peer_staged.md; then
    echo "  peer's staging survived the publish"
else
    echo "  FAIL: the publish destroyed the peer's staging"; fail=1
fi
[ "$(git show HEAD:mine.md)" = "mine third" ] && echo "  our own path did publish" \
    || { echo "  FAIL: our path did not publish"; fail=1; }

# ---------------- TEST 4: the same, on the AUTHOR-OVERRIDE path ----------------
#
# The author override is where the amend used to live, so it is the path worth pinning. It must
# apply the author WITHOUT a second git operation, leave the peer's staging alone, and NOT
# override the committer - the script's documented git-correct split.
echo "mine fourth" > mine.md
printf 'msg4\n' > "$T/m4"
PUBLISH_AUTHOR="maybeLynd <>" bash "$SCRIPT" "$T/m4" mine.md >/dev/null 2>&1

echo "--- TEST 4: author override must not sweep, and must not rewrite ---"
[ "$(git log -1 --format=%an)" = "maybeLynd" ] && echo "  author applied" \
    || { echo "  FAIL: author not applied (got '$(git log -1 --format=%an)')"; fail=1; }
[ "$(git log -1 --format=%cn)" = "t" ] && echo "  committer left as the ambient identity" \
    || { echo "  FAIL: committer was overridden (got '$(git log -1 --format=%cn)')"; fail=1; }
if git show --stat --format= HEAD | grep -q peer_staged.md; then
    echo "  FAIL: author-override path swept the peer's staged file"; fail=1
else
    echo "  peer's staged file still NOT in the commit"
fi
git ls-files --cached | grep -q peer_staged.md && echo "  peer's staging still intact" \
    || { echo "  FAIL: author-override path destroyed the peer's staging"; fail=1; }

echo
[ "$fail" = 0 ] && echo "ALL PASS" || { echo "FAILURES"; exit 1; }
