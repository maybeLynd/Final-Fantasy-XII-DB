#!/usr/bin/env bash
# SWE2-AUDIT-SEM: replay EC7's R1 test 2 (and tests 1/3) on a clean git-archive extract of 2c840bfe4 - the tree EC7 ran
# on, before the R1 rows existed - using EC7's committed scripts copied into the extract so their relative imports
# resolve to the extract's own Tools. Output in <extract>/r1 ; compared with the committed files.
X=/c/Users/Kristian/AppData/Local/Temp/claude/C--Users-Kristian-source-repos/3a61f91a-d548-44f0-9263-41c874c92e7e/scratchpad/x2c840
REC="/c/Users/Kristian/source/repos/XIIOnline/Database/FFXII TZA/_index/candidates/ec7-uc1-span-rows-0929"
D="$X/Database/FFXII TZA"
C="$D/_index/candidates/ec7-uc1-span-rows-0929"
W="$X/r1"
mkdir -p "$C" "$W"
cp "$REC/uc1_span_tests.py" "$REC/t2_compare.py" "$REC/t2_scratch_selector.py" "$C/"
cd "$C" || exit 2
python -B uc1_span_tests.py --root "$X" --out "$W" > "$W/t13.txt" 2>&1; echo "uc1_span_tests exit $?"
echo "tsv diff lines vs committed: $(diff <(tr -d '\r' < "$REC/uc1-span-tests.tsv") <(tr -d '\r' < "$W/uc1-span-tests.tsv") | grep -c '^[<>]')"
echo "t13 diff lines vs committed: $(diff <(tr -d '\r' < "$REC/t13-run.txt" | grep -v '^wrote') <(tr -d '\r' < "$W/t13.txt") | grep -c '^[<>]')"
run() {
  local tag=$1 sel=$2 span=$3
  python -B t2_scratch_selector.py "$sel" "$W/$tag.out" --write > "$W/$tag.out.txt" 2>&1; echo "$tag out exit $?"
  UC1IN=$span python -B t2_scratch_selector.py "$sel" "$W/$tag.in" --write > "$W/$tag.in.txt" 2>&1; echo "$tag in exit $?"
}
run ppfx "$D/23-Third-Party-Libraries/PostEffects-Yebis-PPFX/members/select_ppfx.py" 006DA880:007911E0
run sead "$D/18-Audio/members/select_audio_libraries.py" 007A4380:007F41A0
run vpx "$D/23-Third-Party-Libraries/members/select_libvpx.py" 0016DDD0:0017C890
run vorbis "$D/18-Audio/members/select_audio_libraries.py" 008800C0:008958B0
python -B t2_compare.py "$W" > "$W/t2-compare.txt" 2>&1; echo "t2_compare exit $?"
echo "t2-compare diff vs committed:"
diff <(tr -d '\r' < "$REC/t2-compare.txt") <(tr -d '\r' < "$W/t2-compare.txt") && echo "IDENTICAL"
