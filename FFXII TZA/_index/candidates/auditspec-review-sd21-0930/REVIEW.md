# SWE2-AUDIT-SPEC review of SD-21 (sd21-mix-path-remainder-0930 at 819bda0de): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75, 2026-09-30). Producer: OPUS. Reviewed
commit `819bda0de`, record [sd21-mix-path-remainder-0930](../sd21-mix-path-remainder-0930/README.md). Static,
checked at HEAD `cb5b622f2`.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD21-0930 | sd21-mix-path-remainder-0930 | `819bda0de` | ACCEPT |

**Re-run.** `sd21_mix_remainder.py`: V1-V7, F1-F3 and K1-K3 PASS, `FAILS 0`. Output
([rerun_sd21_mix_remainder.out](rerun_sd21_mix_remainder.out)) is identical to the committed `.out` ignoring CR.
The record directory stayed clean.

**Re-derived independently** ([sd21_rederive.py](sd21_rederive.py) / [.out](sd21_rederive.out), `tk.py`, not retool):
- **The factory's selector is the 10th argument.** From the prologue of `007AEA20`, 4 homing stores then `push r14`
  and `sub rsp, 0x50` give a frame of `0x58`. The selector `cmp byte [rsp + 0xa8], 0` at `007AEA3A` is therefore entry
  `+0x50`, which is argument 10.
- **Flag 0 path.** Pool take `007DF750` on `02EAD250`, construct with `007E0650`, second take on `02EAD200`, open with
  `007E0980`. Then `007AF380` under lock `02EAD138` into list `02EAD2A0`.
- **Flag set path.** `007AD460(0x10, 0x2B8, 1)`, zeroed by `00861EC0`, then `007E0650`, the `02EAD200` take,
  `007E0980`, and `007AF490` under lock `02EAD160` into list `02EAD300`.

  Every address matches F2.
- **Per-caller flag, re-read.** The last store to `[rsp + 0x48]` before each call is `007B91BC mov byte [rsp+0x48], 1`
  (ExternalSourceVoice: heap), `007ED303 mov byte [rsp+0x48], 0` (Voice: pool) and `007DCF5B mov byte [rsp+0x48], bpl`
  (HCAMixerVoice: a variable). That agrees with the record.
- **Vtables read directly.** `01CB8290` has 7 slots, and its slot 7 is the next vtable's COL pointer. `01CB82D0` has 7
  (null after). `01CB8360` has 17, with slot 3 = `007E2710` and slot 9 = `007E0A40`. The Master vtable's slots 1 and 4
  are the same stub `007BD590`, which is consistent with "type id 1" and "returns 1".
- **Start/queue callers.** My own census over the listed functions in `007A0000..00800000` looked for
  `call [reg+0x18|0x48]` on a vtable loaded from `[x+0x68|0x48]`. Its first pass had a census-only extra, `007DD600`.
  That was my defect: it was not flow-aware, and a reused `rcx` whose calls actually go through `[rbx+0x30]` counted as
  a hit. With register kills added, it gives exactly the record's lists: start `007B9050 007B9AF0 007DCE20 007EDA60
  007EDAB0` and queue `007B9590 007DCE20 007EAA60`.

**Controls.** V1-V7, F1 and F2 assert exact slot addresses, offsets and constants, so they are sensitive to a wrong
slot or a wrong path. F3 is a list equality built from the same load-then-call pattern, so it cannot see a caller that
holds the voice somewhere other than `owner+0x68` / `+0x48`. My census shares that blind side and so is a
reproduction, not independent evidence of completeness. The record states this limit ("pattern-found callers").
K1-K3 identify the other kernel variants by dispatch compare and store count. Only K2 is read instruction by
instruction, as stated.

**Not checked.** The kernel variants other than K2, instruction by instruction, and the meaning of `+0x100` / `+0x104` /
`+0x108`, which the record does not claim.
