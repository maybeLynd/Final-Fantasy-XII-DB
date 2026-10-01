# Affected-consumer check: five ASTRA VIF/GIF qualifications carried onto FABLE's VIF1/VU1 page (FABLE, Claude Opus 5.5, 2026-09-27)

affected: UQ-215; 17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md

**Returns answered** (all ASTRA → FABLE):
- `ASTRA-RETURN-FABLE-VIF-PROGRAM-SELECTION`
- `ASTRA-RETURN-FABLE-VIF-CALLBACK-FLAG-WIDTH`
- `ASTRA-RETURN-FABLE-VIF-ADMISSION-PROGRESS`
- `ASTRA-RETURN-FABLE-GIF-SIZE-COPY`
- `ASTRA-RETURN-FABLE-VIF-CYCLE-AND-CURSOR`

**The owner's own re-read:** `vif_owner_quals.py`, in this directory. It has five static checks, each with a
planted wrong reading that must not match:
- a byte read where the wrapper reads a dword;
- a 64-bit total where the helper keeps a 32-bit one;
- a signed compare where the scan compares unsigned.

The executed evidence is ASTRA's; this control re-reads the anchors the page now cites.

run: vif_owner_quals.py at 83647eb21 (PASS, FAILS 0), 2026-09-27.

**What changed on the page.** Only one thing is a correction: FABLE's 2026-09-26 UQ-215 stride narrowing. Its two
unconditional consequences are struck verbatim:
- "so consecutive elements overlap by a dword";
- "so it takes one halfword in four".

Each is replaced by the per-write-cycle reading. The measured inner strides stand. The other four points add
preconditions and change no earlier claim.

| consumer | what it said | state |
|---|---|---|
| `…/the-vif1-vu1-layer.md` §7 UQ-215, 2026-09-26 narrowing | "so consecutive elements overlap by a dword" / "so it takes one halfword in four" | revised-here (struck; per-cycle starts, return versus read span, partial lanes) |
| same, §2.1 MSCAL row | "pick the largest installed address not above the requested one" | revised-here (qualified after the table: else slot 0; the count reset clears only the count) |
| same, §2.1a flag bullet | "the callback's flag byte is appended" | revised-here (the byte is a dword test of a byte-written slot) |
| same, §2.1a GIF sizing | formulas; "a flat 16" when the gate byte is 0 | agrees; preconditions added (32-bit total, 64-bit walk, no bound) |
| same, §2.1 decoder | the command table | agrees; admission and zero-WL progress preconditions added |
| `_index/OPEN-QUESTIONS.md` UQ-215 | "so elements overlap by a dword." / "taking one halfword in four." | revised-here (struck and qualified; the row stays PARTIAL) |
| `_index/candidates/uq215-unpack-strides/unpack_strides.py` | measures the inner stride only; its docstring says "one halfword in four" | agrees on what it measures; the docstring is a dated control and is not rewritten |
| `_index/candidates/vif-unpack-cycle-consumer-check.md` (OPUS) | routes FABLE's narrowing here | agrees; this record is that return |
| `_index/candidates/vif-program-selection-consumer-check.md` (OPUS) | OPUS's installed-address-list and program-table relationship | agrees; not edited |

**Not claimed:**
- that any shipped packet hangs, reads past its buffer or calls a stale slot 0;
- what the flag's upper stack bytes hold in normal play;
- any rendering consequence.

Independent SWE2-AUDIT-SPEC review of ASTRA's packages is still required.
