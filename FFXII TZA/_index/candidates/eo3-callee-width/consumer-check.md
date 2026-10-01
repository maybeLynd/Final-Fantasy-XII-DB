# Affected-consumer check: EO-3 callee width (FABLE, Claude Opus 5.5, 2026-09-26)

affected: 02-Resource-And-Asset-Pipeline/the-resource-request-queue.md (the EO-3 callee sentence)

**Regression:** `eo3_callee_width.py` beside this file (4 checks, FAILS 0).

run: eo3_callee_width.py at 95a2e0bf6 (FAILS 0), 2026-09-26.

ASTRA upheld the `rdi` proof and asked for one literal fix (`ASTRA-RETURN-FABLE-EO3-CALLEE-WIDTH`).
- The helper `0036C140` writes the full `rax` at `0036C17C`, so "writes only `eax`" was too narrow.
- It returns only when its depth counter is positive. Otherwise it spins at `0036C150`, so the conclusion holds on
  the path that arrives at the call's return, which is not proof that the caller ran.

| consumer | what it says | state |
|---|---|---|
| `02-Resource-And-Asset-Pipeline/the-resource-request-queue.md` EO-3 box | "writes only `eax`, `rcx`, `rdx` and five globals" | revised-here (`eax` struck; `rax` / `eax`; the arrival condition added) |
| `24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md` | the pop helper spins when empty (`0036C146`–`0036C150`) | agrees |
