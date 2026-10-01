# Affected-consumer check 2: S-2 answered by reconstruction; the 2026-09-22 model corrected (FABLE, Claude Opus 5.5, 2026-09-26)

**Control:** `24-Compiler-And-CRT-Runtime/Binary-Hardening-And-Hooking/members/cfg_link_matrix.py` (4 checks, FAILS 0). It
builds on `debug_directory.py` from the first check.

**Evidence class:** reconstruction with linker 14.51, kept distinct from the page's static reading. The game's linker
is 14.0.24215.

| consumer | what it said | state |
|---|---|---|
| hardening page, section 7 `S-2` box | "`/guard:cf` compile without `/guard:cf` link is the likely cause but is not proven here" | revised-here (ticked, answered with the combination) |
| hardening page, "`S-2` narrowed", the best-supported-model blockquote | "`/guard:cf` together with ASLR disabled, and CFG cannot operate on a non-relocating image" | revised-here (struck; X3 shows a `/guard:cf` link with `/DYNAMICBASE:NO` builds the table) |
| hardening page, "What IS missing" (`DYNAMIC_BASE` clear, `HIGH_ENTROPY_VA` inert) | ASLR switched off | agrees. X1's `0x8120` is exactly what `/DYNAMICBASE:NO` leaves. |
| hardening page, section 9a | only the static CRT is instrumented | agrees. X2 shows the CRT alone sets `CF_INSTRUMENTED`. |
| hardening page, "The debug directory", first open bullet | "whether a link without `/guard:cf` still writes `CF_INSTRUMENTED`…" | revised-here (settled by X1 and X2) |
| `_index/OPEN-QUESTIONS.md` S-2 | OPEN, with the 2026-09-22 narrowing and today's correction | revised-here (ANSWERED; the previous status kept as history) |
| `_index/OPEN-QUESTIONS.md` T-9 | the twelve dwords are an unconverted `.gfids$y` pass-through | agrees; stays in NAS package 2 for its lost-build residue (which symbols) |
