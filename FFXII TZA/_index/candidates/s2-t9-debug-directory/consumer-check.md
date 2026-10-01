# Affected-consumer check: S-2's 2026-09-22 refutation weakened; T-9 narrowed (FABLE, Claude Opus 5.5, 2026-09-26)

The image's debug directory was read for the first time. Control:
`24-Compiler-And-CRT-Runtime/Binary-Hardening-And-Hooking/members/debug_directory.py` (5 checks, FAILS 0).

Its POGO record lists two contributions that bear on the 2026-09-22 argument:
- the `.gfids` content is the input contribution `.gfids$y`;
- the two guard pointers are the CRT's `.00cfg` input.

That argument read both as products that only a `/guard:cf` link emits, and both legs are withdrawn. The third leg,
`GuardFlags` = `CF_INSTRUMENTED`, stands. What sets it is toolchain behaviour this image cannot show.

| consumer | what it said | state |
|---|---|---|
| hardening page, section 7 `S-2` box | "the link **did** have `/guard:cf` — the `.gfids` section and both guard pointers are linker products …" | revised-here (struck, dated correction beside it) |
| hardening page, "`S-2` narrowed" heading and its three-row table | "who emits it: the linker, and only under `/guard:cf`" / "the linker"; "the compile/link mismatch is the wrong axis" | revised-here (two cells and the conclusion struck and corrected; note under the heading) |
| hardening page, "What IS missing" (`DYNAMIC_BASE` clear, `.reloc` present, `HIGH_ENTROPY_VA` inert) | ASLR switched off | agrees (untouched by the debug directory) |
| hardening page, section 9a (only the static CRT consults the guard slot) | CRT-only instrumentation | agrees. VC_FEATURE's 49 guard-aware objects out of 1,296 corroborate it from an independent record. |
| hardening page, `T-9` note | best model: unconverted `.gfids$y` symbol indices | agrees, now image-attested (POGO names the contribution); narrowed in place |
| `_index/OPEN-QUESTIONS.md` S-2 | "The link **did** have `/guard:cf` …" | revised-here (dated correction appended to the question cell; status stays OPEN) |
| `_index/OPEN-QUESTIONS.md` T-9 | best model, needs objects or a map | revised-here (dated narrowing appended; status stays OPEN) |

A search for the phrases "linker products", "link DID have" and "non-`/guard:cf` link" over every `.md` finds no other
consumer.
