# Affected-consumer check: T-9 answered - the twelve are the static CRT's `.gfids$y` data (FABLE, Claude Opus 5.5, 2026-09-27)

affected: 24-Compiler-And-CRT-Runtime/Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md (the T-9 section: "which functions they index still needs the objects' symbol tables, which do not ship")
run: t9_crt_gfids.py with the MSVC v140 x64 libs (build 24237) and the Windows SDK lib root, at 6c92d15b2; C4 is the chance control (8 positions matched; 0.0 % of 2,000 random twelves).

| consumer | what it said | state |
|---|---|---|
| hardening page, T-9 section (2026-09-26 narrowing) | which functions they index needs objects that do not ship | revised-here: answered beneath - the objects are the public static runtime's; eight positions named, three inferred |
| hardening page, "The debug directory" (VC_FEATURE: 49 guard-aware objects, only the CRT consults the slot) | agrees | not revised |
| `_index/candidates/nas-lost-build-opus-review/README.md` (OPUS) | T-9 declined: the source exists in the public toolset | agrees; this is the test it named |
| _index/OPEN-QUESTIONS.md T-9 | OPEN | revised-here: ANSWERED with limits |

Regenerated with it: nothing.
