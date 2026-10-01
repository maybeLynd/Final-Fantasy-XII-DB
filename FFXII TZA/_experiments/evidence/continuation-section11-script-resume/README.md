# Update 11 — script execution, original native commands, and resume state

## Install by ordinary folder merge

This update is based on `FFXII TZA(20260923-205605).zip`, the newest database supplied for this work.
That snapshot already contains Updates01–10 and subsequent Devin edits. Do not first overwrite it
with an older full TSV or reapply old overlays on top of newer peer edits.

1. Back up the affected files or checkpoint them in Git.
2. Extract the ZIP.
3. Copy the extracted **FFXII TZA** folder into the PARENT directory that contains your existing
   **FFXII TZA** folder. Merge folders and replace matching files.
4. Do not delete the existing database and do not put one FFXII TZA folder inside another.

Only changed or new files are delivered. Full TSV files are necessary for ordinary replacement,
but only two target type rows and seven field rows change; all unrelated TSV lines are identical
to the supplied baseline. Newer local changes to any replaced file require a real merge, not blind
replacement. PATCH_MANIFEST.json records exact before/after hashes. The optional verify_overlay.py
is READ ONLY and never merges or overwrites files. No command is required for normal installation.

## Actual work

Original interpreter, original family initialization, real wait/getmyid/getx/nowmap callbacks and
selected full request-driver entries execute together.146 named assertions pass twice identically;
10 wrong private-code variants and8 retained-record corruptions are rejected.58 selected original
body ranges and7 data spans are pinned. There are no application substitutions, import bridges or
planted command callbacks. Synthetic input/state are not a live game session.

The specification now separates shared depth reset from persistent actor/request state, re-fetch
from phase0 initialization, target from result owner, completion from delivery, and actual stop/PC
behavior from assumed progress. An isolated guard-page case establishes a real predecode read;
no live game crash is induced or claimed.

## Changed files

- Three canonical ScriptVM contracts.
- Interpreter and native-lifecycle mechanism pages, marked REOPENED for corrections.
- EXP-085 and EXP-106 writeups: new consumption notes, no changes to their programs/raw results.
- types.tsv and fields.tsv: VmValueStack and ActorWaitSlot only.
- EXTERNAL-CONTINUATION.md: precise continuation state.
- One new connected mechanism page plus this section's evidence and validators.

TEAM tasks, L2 verdicts, global metrics, reconstruction source, historical programs/results, game
EXE and Ghidra annotations are unchanged. No compiled binaries, dependencies, full game image or
unmodified database files are included.

## Status and reproduction

Local production is complete and validated; required independent acceptance remains pending.
This is not a new EXP number or whole-database certification. Remaining opcodes/waits, full field
scheduling, actual resource lifetime, live actor allocation identity and other native services stay
explicitly unresolved.

See REVIEW.md for exact claims, original addresses, limits, native reproduction and subsequent work.
Reproduction requires the authorized original EXE, baseline historical inputs, Linux x86-64,
Python3.10+ and GCC. It downloads nothing. Optional document validation additionally uses PyYAML.
