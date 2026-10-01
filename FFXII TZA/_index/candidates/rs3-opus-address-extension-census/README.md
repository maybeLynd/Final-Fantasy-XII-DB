# RS-3: the sign / zero split after `0020E600` is per call site and general (OPUS, 2026-09-26)

**Evidence class: STATIC. `live_game: false`.**

**The question.** Three sites that decode a reference through `0020E600` then compute an address in 32-bit registers.
Two sign-extend and one zero-extends. RS-3 asked whether that split belongs to the encoding scheme or to one file's
helpers.

**3 / 3 pass. `run_output.txt` and `result.json` are byte-identical over two runs (md5 `ea083453f65f9fa213d7bbe2f3f99b09`).**

| case | observed |
|---|---|
| `R1` | `0020E600` is `mov eax, ecx ; add rax, [01F83530] ; ret`. Its result is the 64-bit sum of the base global and the zero-extended 32-bit reference. |
| `R2` | **All 4,371 call sites are classified** by following `rax` / `eax` after the call. 2,957 use the full 64-bit result and 747 pass it on (together 85 %). **565 zero-extend**: 53 through a 32-bit `mov`, and 512 through 32-bit arithmetic whose result is then used as an address. **60 sign-extend**: 58 by `cdqe` / `movsxd` directly and 2 after 32-bit arithmetic. 6 are tail jumps and 36 are named as unclassified. |
| `R3` | **The split is general, not one file's helpers.** The sign-extending sites sit in Movement, WorldAreaField, Script_VM_Native_Bridge, Presentation and Audio. The zero-extending ones sit mostly in CombatFormula, CombatAction, Items_Equipment_Shops_License, Status_Periodic_Terminal, CombatAI and ActorEntity. |

**Answer.** The split is neither the encoding's nor one helper file's. The encoding is a single 32-bit value added to a
64-bit base. What varies is each caller's own 32-bit typing of the result, compiled site by site across a dozen
subsystems, which is the 32-bit address arithmetic a PS2-era codebase carries.

**What a reimplementation must preserve.**
- The three forms agree exactly when the final address is below 2 GiB. At or above that, sign-extending sites produce
  `FFFFFFFF8…` while zero-extending sites keep a value below 4 GiB, and both differ from the 85 % that use the full
  result.
- So the choice of extension is harmless only while referenced data lives below 2 GiB. A reimplementation should either
  keep that arena low, or use full-width pointers at every site. Picking one extension everywhere is not enough.
- Where the arena lands at run time is J-C's and ASTRA's EXP-077 / EXP-078. The image initialises the base global
  `01F83530` to zero, and the one in-image route that could write it (`00210570`) is undriven (J-C, CD-2).

**Run:** `python check.py` (about a minute). It needs `Tools/work/exe/FFXII_TZA.exe` and `Tools/work/graph/functions.tsv`.
