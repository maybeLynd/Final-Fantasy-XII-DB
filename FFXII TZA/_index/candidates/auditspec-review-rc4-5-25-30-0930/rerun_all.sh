#!/bin/bash
# SWE2-AUDIT-SPEC rerun of SWE2-ORACLE's four be7c6fcd6 records; stdout into this dir, diff vs committed .out ignoring CR.
C="/c/Users/Kristian/source/repos/XIIOnline/Database/FFXII TZA/_index/candidates"
R="$C/auditspec-review-rc4-5-25-30-0930"
export PYTHONDONTWRITEBYTECODE=1
: > "$R/rerun_summary.txt"
for pair in rc25-party-definition-rows-0930:rc25_rows rc30-cl2-request-bounds-0930:rc30_bounds rc30-cl2-request-bounds-0930:rc30_census rc30-cl2-request-bounds-0930:verb_census rc4b-capture-residue-0930:rc4b_bounds rc4b-capture-residue-0930:rc4b_scan rc4b-capture-residue-0930:rc4b_pass1 rc4b-capture-residue-0930:rc4b_pass2 rc4b-capture-residue-0930:rc4b_pass3 rc5b-event-slot-residue-0930:rc5b_actions rc5b-event-slot-residue-0930:rc5b_evctrl rc5b-event-slot-residue-0930:rc5b_operands; do
  d="${pair%%:*}"; s="${pair##*:}"
  cd "$C/$d"
  before="$(git status --short -- .)"
  start=$(date +%s)
  timeout 1500 python "$s.py" > "$R/rerun_$s.out" 2>&1; rc=$?
  secs=$(( $(date +%s) - start ))
  if diff <(tr -d '\r' < "$s.out") <(tr -d '\r' < "$R/rerun_$s.out") > /dev/null; then v=IDENTICAL; else v=DIFFERS; fi
  after="$(git status --short -- .)"
  echo "$d/$s.py rc=$rc ${secs}s $v | dirty-before=[${before}] dirty-after=[${after}]" >> "$R/rerun_summary.txt"
done
echo DONE >> "$R/rerun_summary.txt"
