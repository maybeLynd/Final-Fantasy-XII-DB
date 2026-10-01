#!/usr/bin/env bash
# SWE2-AUDIT-SEM GCR-UNIFY re-run: the committed selector at HEAD, writes redirected to scratch (EC7's own
# t2_scratch_selector.py redirector), then a set comparison against the committed members file, the two pre-unification
# files at 090f74f38^, and FABLE's form_split.out.
R=/c/Users/Kristian/source/repos/XIIOnline
W=$R/Database/Tools/work/SWE2-AUDIT-SEM/gcr
P="$R/Database/FFXII TZA/22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/members"
REDIR="$R/Database/FFXII TZA/_index/candidates/ec7-uc1-span-rows-0929/t2_scratch_selector.py"
cd "$W" || exit 2
python -B "$REDIR" "$P/select_guarded_class_registrars.py" "$W/out" --write > "$W/selector_run.txt" 2>&1; echo "selector exit $?"
git -C $R show "090f74f38^:Database/FFXII TZA/22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/members/guarded-class-registration-stubs.tsv" > "$W/old_stubs.tsv"
git -C $R show "090f74f38^:Database/FFXII TZA/22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/members/guarded-class-registration-orchestrators.tsv" > "$W/old_orch.tsv"
python -B "$W/gcr_compare.py" "$P/guarded-class-registration-stubs.tsv" "$W/out" "$W/old_stubs.tsv" "$W/old_orch.tsv"
