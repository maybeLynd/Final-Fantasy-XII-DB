#!/bin/bash
# build.sh X [REV] - full A-drift repair built on a clean export of REV (default HEAD) at X:
#   exact A removal in every A-refused row, then the selectors (Phyre x3 cascades, ECA fixpoint), verification re-runs of
#   the other selectors (must change no membership), row counts + notes for batches A and B.
# Prints the stage outputs; exits non-zero on any unexpected state.
set -o pipefail
S=/c/Users/Kristian/AppData/Local/Temp/claude/C--Users-Kristian-source-repos/0aca3c35-4792-4b08-9423-be894cfa848b/scratchpad/SWE2-EC7
X=$1; REV=${2:-HEAD}
bash $S/export.sh $X $REV || exit 1
D="$X/Database/FFXII TZA"; K=$X/Database/Tools/analysis-kit/gfz-scripts
cd "$D" && git init -q . && git add -A >/dev/null 2>&1 && git -c user.name=x -c user.email=x@x commit -qm head || exit 1
python -B $S/exact_remove.py $K "$D" > $X/stage1.txt 2>&1 || { cat $X/stage1.txt; exit 2; }
cat $X/stage1.txt
want="ScriptVM.VerbAdapter|SQEX SEAD sound library span|Phyre PAnimation module|Phyre PhyreCore module|Phyre PPostProcessing module|zlib 1.2.11|JsonBox JSON library|PPFX post-effect library|NativeAdapter.ExplainedCalleeForwarder|NativeAdapter.CallResultTailCall|counter-append static-table initialisers|Phyre PSerialization module"
n=$(grep -c " -> " $X/stage1.txt); nw=$(grep -E -c ":: ($want) \|" $X/stage1.txt)
[ "$n" = 12 ] && [ "$nw" = 12 ] || { echo "UNEXPECTED ROW SET: $n rows, $nw expected"; exit 3; }
grep -q "NON-A REFUSALS" $X/stage1.txt && { echo "NON-A refusals present"; exit 3; }
git add -A && git -c user.name=x -c user.email=x@x commit -qm stage1
for s in "22-Middleware-PhyreEngine/members/select_phyre_panimation.py" "22-Middleware-PhyreEngine/members/select_phyre_module.py PPostProcessing" \
         "22-Middleware-PhyreEngine/members/select_phyre_module.py PhyreCore" "22-Middleware-PhyreEngine/members/select_phyre_module.py PSerialization" "24-Compiler-And-CRT-Runtime/Generated-Families/members/select_explained_callee_adapters.py" \
         "23-Third-Party-Libraries/PostEffects-Yebis-PPFX/members/select_ppfx.py" "18-Audio/members/select_audio_libraries.py" \
         "01-Script-VM-Native-Bridge/Verb-Dispatch/members/select_verb_adapters.py" "23-Third-Party-Libraries/members/select_zlib.py"; do
  python -B $s --write > $X/sel.out 2>&1 || { echo "selector failed: $s"; tail -5 $X/sel.out; exit 4; }
done
# the verb selector rewrites its two files with LF only; membership is checked below, content kept from stage 1
git checkout -q -- 01-Script-VM-Native-Bridge/Verb-Dispatch/members/
python $S/memdiff.py "$D" > $X/stage2.txt; cat $X/stage2.txt
grep -v "^22-Middleware-PhyreEngine/members/phyre-panimation.tsv: 194 -> 119  dropped 75 \|^22-Middleware-PhyreEngine/members/phyre-ppostprocessing.tsv: 152 -> 134  dropped 18 \|^24-Compiler-And-CRT-Runtime/Generated-Families/members/explained-callee-adapters.tsv: 480 -> 482  dropped 0   admitted 2 005AA840 005C7930" $X/stage2.txt | grep . && { echo "UNEXPECTED SELECTOR DRIFT"; exit 5; }
git add -A && git -c user.name=x -c user.email=x@x commit -qm stage2
python -B $S/rows_notes.py "$D" A && python -B $S/rows_notes.py "$D" B || exit 6
git add -A && git -c user.name=x -c user.email=x@x commit -qm notes
cd $K && python -B check_dispositions.py > $X/cd.txt 2>&1
grep "frontier  (\|families accepted\|REFUSED" $X/cd.txt
python -B check_family_forms.py --db "$D" > $X/forms.txt 2>&1; grep "MISMATCH" $X/forms.txt | head -1
echo "built $(git -C /c/Users/Kristian/source/repos/XIIOnline rev-parse --short=9 $REV)"
