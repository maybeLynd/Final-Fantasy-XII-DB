#!/bin/sh
# Re-runs of the three OPUS retool checkers and the SD-191 checker (a copy in this folder, so its census output and
# temp file land here, not in the package). Outputs go into the review folders.
export PYTHONDONTWRITEBYTECODE=1 TMP='C:\t' TEMP='C:\t'
C="/c/Users/Kristian/source/repos/XIIOnline/Database/FFXII TZA/_index/candidates"
python -B "$C/sd180-181-emitter-walk-0930/sd180_walk.py" > "$C/auditspec-review-sd180-181-0930/rerun_sd180_walk.out" 2> "$C/auditspec-review-sd180-181-0930/rerun_sd180_walk.err"
python -B "$C/sd181-sp1-loader-0930/sd181_check.py" > "$C/auditspec-review-sd181-0930/rerun_sd181_check.out" 2> "$C/auditspec-review-sd181-0930/rerun_sd181_check.err"
python -B "$C/sd23-state7-dynamicsound-0930/sd23b_check.py" > "$C/auditspec-review-sd23b-0930/rerun_sd23b_check.out" 2> "$C/auditspec-review-sd23b-0930/rerun_sd23b_check.err"
python -B "$C/auditspec-review-sd191-0930/rerun_sd191_check_copy.py" > "$C/auditspec-review-sd191-0930/rerun_sd191_check.out" 2> "$C/auditspec-review-sd191-0930/rerun_sd191_check.err"
echo ALLDONE
