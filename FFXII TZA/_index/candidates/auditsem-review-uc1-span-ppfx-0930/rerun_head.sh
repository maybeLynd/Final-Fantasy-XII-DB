#!/usr/bin/env bash
# SWE2-AUDIT-SEM: re-run EC7's R1 tests at HEAD into scratch - tests 1/3 (uc1_span_tests.py --out) and test 2 (each
# family's committed selector out/in through t2_scratch_selector.py, then t2_compare.py) - and diff against the commit.
REC="/c/Users/Kristian/source/repos/XIIOnline/Database/FFXII TZA/_index/candidates/ec7-uc1-span-rows-0929"
DB="/c/Users/Kristian/source/repos/XIIOnline/Database/FFXII TZA"
W=/c/Users/Kristian/source/repos/XIIOnline/Database/Tools/work/SWE2-AUDIT-SEM/uc1span/rerun
PY=python
mkdir -p "$W"
cd "$REC" || exit 2
$PY -B uc1_span_tests.py --out "$W" > "$W/t13.txt" 2>&1; echo "uc1_span_tests exit $?"
echo "tsv diff lines: $(diff <(tr -d '\r' < uc1-span-tests.tsv) <(tr -d '\r' < "$W/uc1-span-tests.tsv") | grep -c '^[<>]')"
echo "t13 diff lines: $(diff <(tr -d '\r' < t13-run.txt) <(tr -d '\r' < "$W/t13.txt") | grep -c '^[<>]')"
run() { # tag selector span
  local tag=$1 sel=$2 span=$3
  $PY -B t2_scratch_selector.py "$sel" "$W/$tag.out" --write > "$W/$tag.out.txt" 2>&1; echo "$tag out exit $?"
  UC1IN=$span $PY -B t2_scratch_selector.py "$sel" "$W/$tag.in" --write > "$W/$tag.in.txt" 2>&1; echo "$tag in exit $?"
}
run ppfx "$DB/23-Third-Party-Libraries/PostEffects-Yebis-PPFX/members/select_ppfx.py" 006DA880:007911E0
run sead "$DB/18-Audio/members/select_audio_libraries.py" 007A4380:007F41A0
run vpx "$DB/23-Third-Party-Libraries/members/select_libvpx.py" 0016DDD0:0017C890
run vorbis "$DB/18-Audio/members/select_audio_libraries.py" 008800C0:008958B0
$PY -B t2_compare.py "$W" > "$W/t2-compare.txt" 2>&1; echo "t2_compare exit $?"
echo "t2-compare vs committed (families run here only):"
diff <(tr -d '\r' < t2-compare.txt | grep -v -i vorbis) <(tr -d '\r' < "$W/t2-compare.txt" | grep -v -i vorbis) | head -20
