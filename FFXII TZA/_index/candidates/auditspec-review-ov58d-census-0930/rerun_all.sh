#!/bin/bash
# SWE2-AUDIT-SPEC rerun of OPUS's ov58d-pointer-flow-0930 scripts; stdout into this dir; diff vs committed .out ignoring CR.
# Any tracked file a script rewrites is copied here and restored to HEAD if it was clean before the run.
C="/c/Users/Kristian/source/repos/XIIOnline/Database/FFXII TZA/_index/candidates"
D="$C/ov58d-pointer-flow-0930"
R="$C/auditspec-review-ov58d-census-0930"
export PYTHONDONTWRITEBYTECODE=1
: > "$R/rerun_summary.txt"
cd "$D"
for s in ov58d_mirror ov58d_residue ov58d_flow; do
  before="$(git status --short -- .)"
  start=$(date +%s)
  timeout 5400 python "$s.py" > "$R/rerun_$s.out" 2>&1; rc=$?
  secs=$(( $(date +%s) - start ))
  if diff <(tr -d '\r' < "$s.out") <(tr -d '\r' < "$R/rerun_$s.out") > /dev/null; then v=IDENTICAL; else v=DIFFERS; fi
  after="$(git status --short -- .)"
  echo "$s.py rc=$rc ${secs}s stdout-vs-committed-out=$v | dirty-before=[${before}] dirty-after=[${after}]" >> "$R/rerun_summary.txt"
  for f in $(git diff --name-only --relative -- . ); do
    b="$(basename "$f")"
    if [ -z "$before" ]; then
      cp "$D/$b" "$R/rerun_written_$b"
      if diff <(git show "HEAD:Database/FFXII TZA/_index/candidates/ov58d-pointer-flow-0930/$b" | tr -d '\r') <(tr -d '\r' < "$D/$b") > /dev/null; then vv=IDENTICAL; else vv=DIFFERS; fi
      echo "  $s.py rewrote $b: vs HEAD $vv; restored" >> "$R/rerun_summary.txt"
      git checkout -- "$D/$b"
    fi
  done
done
echo DONE >> "$R/rerun_summary.txt"
