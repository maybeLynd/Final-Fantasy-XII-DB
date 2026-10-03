#!/usr/bin/env bash
# e2e_control.sh KITDIR - end-to-end control for the stale pre-image gate through publish_paths.sh, in a throwaway repo
# (never the live repository or board). Reproduces the 95b1f3a4c shape: a peer (FABLE:) corrects a page, then another
# lane (SWE2-CONTRACT) publishes the page from the pre-correction text.
#   E1 the stale pre-image publish is REFUSED (exit 9) and HEAD does not move
#   E2 the same publish with 'reverts: <sha>' in the message commits
#   E3 a clean publish (the peer's text kept, own line added) commits
set -u
KIT=$1
T=$(mktemp -d); cd "$T"; git init -q .; git config user.email t@t; git config user.name t; git config commit.gpgsign false
mkdir -p "Database/Tools/analysis-kit/gfz-scripts" "Database/FFXII TZA/16-UI"
for f in publish_paths.sh publish_correction_gate.py check_stale_preimage.py; do cp "$KIT/$f" "Database/Tools/analysis-kit/gfz-scripts/"; done
P="Database/FFXII TZA/16-UI/CONTRACT-fixture.md"
L() { for i in 1 2 3 4 5; do echo "$1 sentence $i - long enough to be a substantive database line for the stale gate"; done; }
{ echo "# page"; L ORIGINAL; echo "tail"; } > "$P"
git add -A; git commit -qm "OPUS: base page"
{ echo "# page"; L CORRECTED; echo "tail"; } > "$P"
git add -A; git commit -qm "FABLE: correction of the five sentences"
PEER=$(git rev-parse --short=9 HEAD)
fails=0
run() { XII_PUBLISH_NO_BOARD_CHECK=1 TEAM_AGENT=SWE2-CONTRACT bash Database/Tools/analysis-kit/gfz-scripts/publish_paths.sh "$1" "$P" > out.txt 2>&1; echo $?; }
# E1
{ echo "# page"; L ORIGINAL; echo "tail"; } > "$P"
printf 'SWE2-CONTRACT: batch\n' > m1.txt
h0=$(git rev-parse HEAD); rc=$(run m1.txt); h1=$(git rev-parse HEAD)
if [ "$rc" = 9 ] && [ "$h0" = "$h1" ] && grep -q 'STALE PRE-IMAGE' out.txt; then echo "PASS  E1 stale pre-image refused (exit 9, HEAD unchanged)"; else echo "FAIL  E1 rc=$rc"; sed 's/^/      /' out.txt | tail -5; fails=$((fails+1)); fi
# E2
printf 'SWE2-CONTRACT: deliberate revert\n\nreverts: %s\n' "$PEER" > m2.txt
rc=$(run m2.txt); h2=$(git rev-parse HEAD)
if [ "$rc" = 0 ] && [ "$h2" != "$h1" ]; then echo "PASS  E2 declared revert commits"; else echo "FAIL  E2 rc=$rc"; tail -5 out.txt; fails=$((fails+1)); fi
# E3 (reset the page to the peer's text first)
git checkout -q "$PEER" -- "$P"; git commit -qm "FABLE: restore" -- "$P"
{ echo "# page"; L CORRECTED; echo "tail"; echo "an added sentence by the publisher, long enough to count as substantive text"; } > "$P"
printf 'SWE2-CONTRACT: add one line\n' > m3.txt
h3=$(git rev-parse HEAD); rc=$(run m3.txt); h4=$(git rev-parse HEAD)
if [ "$rc" = 0 ] && [ "$h4" != "$h3" ]; then echo "PASS  E3 clean publish commits"; else echo "FAIL  E3 rc=$rc"; tail -5 out.txt; fails=$((fails+1)); fi
cd /; rm -rf "$T"
echo "FAILS $fails"
exit $fails
