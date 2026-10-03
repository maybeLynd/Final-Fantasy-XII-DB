# SWE2-AUDIT-SPEC re-review: OPUS repairs of the two REJECTed rows (opus-reject-repairs-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-REJECT-REPAIRS-REREVIEW-1003` · Package: `_index/candidates/opus-reject-repairs-1003/` (published at `c49f03691`, checked at HEAD `33eb7192f`) · Earlier records: [`auditspec-review-opus-sab-sound-bank-container-cloudint-1002`](../auditspec-review-opus-sab-sound-bank-container-cloudint-1002/REVIEW.md) (REJECT, `001FB770`) and [`auditspec-review-opus-contract-widget-object-homing-1002`](../auditspec-review-opus-contract-widget-object-homing-1002/REVIEW.md) (REJECT, `00568BB0`)

## SWE2-AUDIT-SPEC verdict: ACCEPT

Both repairs are exact. `001FB770` carries the REJECT's replacement clause verbatim, and `00568BB0` now states all three corrected facts (the `+0x48` colour rule, the base colour and `002DD7E0(6)` replacement for elements `+0x20`/`+0x28`, and one `+0x33E` value per `002CC8D0` gate). Both were re-read clause by clause against the full bodies.

## SWE2-AUDIT-SPEC checks

- **Instruments re-run (read-only).**
  - `reject_rows_check.py`: exit 0, `rows 2  FAILS 0`, identical to the committed `.out`.
  - `reject_rows_check.py --rejected`: `rows 2  FAILS 8`, failing both rejected texts (2 for `001FB770`, 6 for `00568BB0`), identical to `reject_rows_check.rejected.out`. The control is sensitive.
  - Both records' `interior_applier.py` (verify mode, writes nothing): `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0` and `VERIFY 3 functions, 15 anchors / ALREADY / FAILS 0`.
  - `rows.json` of both records and the repair package are unchanged between `c49f03691` and HEAD. On the pages, the rejected clauses ("the low byte of the fifth (stack) argument", "equal to 0, 1 or 2") occur 0 times, and the repaired clauses occur once each.
- **`001FB770` (0x85 B, read in full).**
  - The frame is `push rbx` plus `sub rsp,0x40`, so 0x48 bytes. `001FB7BD movzx eax, byte [rsp+0x60]` reads entry `rsp+0x18`, the r8 home slot. Nothing in the body writes it. The byte is passed in the fifth-argument slot (`001FB7CC mov [rsp+0x20], al`).
  - `r8 = lea [rsp+0x50]`, the slot that `001FB7B3` filled with the node, so the third argument is the address of a slot holding the node. `r9 = lea [rsp+0x30]`, with dword K at `+0x30` and qword 0 at `+0x38`, the address of the pair (K, 0). `rdx = lea [rsp+0x58]` is the result slot, and `rcx = r11 = rcx + 8`.
  - The rest of the row also holds:
    - K is `lea r10d, [r9 + r8*2]`.
    - The header is `rcx + 0x10` and the root is qword `[rcx+0x20]`.
    - At `001FB795`, `jl` steps to qword `+0` when the key is below K. Otherwise the node becomes the candidate and the walk steps to qword `+8`.
    - The insert happens when the result is the header or `jge` at `001FB7B1` is not taken, which means key > K (signed).
    - `001FB7E6` reloads the node from the result slot. `001FB7EB` stores `rdx` at `+0x28`, and the function returns the node.
  - **Exact.**
- **`00568BB0` (0x423 B, read in full).** Clause by clause:
  - The entry is `rcx + 0x160 + 32*r9d` (`lea rsi,[rbp+0xb]; shl 5; add rcx`).
  - The `r9d` = 0 path calls `00243580(rdx, 0)`.
  - Element `+0x48` (`00568C87`..`00568CF6`): dword `+0x354` when byte `+0x353` is 0. Otherwise its colour, with top byte `+0x343` when word `+0x350` is non-zero (`00568C90`/`je 0x568cc4`), or byte `+0x350` when that word is zero (`00568CC4`).
  - The other path: elements `+0/+8/+0x10` take `002DD7E0(byte +0x15 + 0x77)`, or `0x79` when byte `+0x14` is 0 (`00568CFB`..`00568D20`).
  - Elements `+0x20`/`+0x28`:
    - Base colour: dword `+0xC` of the element's first qword, or `002DD7E0(2)` when byte `+0x14` is 0 or byte `+0x15` is 2 (`00568E2B`..`00568E41`, `00568F05`..`00568F1B`).
    - The gates: bit 0 of byte `+0x340` of the `02CA96E0[dword +0x35C]` record clear, plus a slot-index compare with `ebp`. Each gate tests its own `+0x33E` value: 0 with `ecx` = 0x60 (`00568D3F`, `00568D96`), 1 with 0x80 (`00568E5E`, `00568EB5`), and 2 with 0x80 (`00568F3D`, `00568F98`). Each `002CC8D0` call passes `edx` = 0x20, `r8d` = dword `+0x344` and `r9d` = 4.
    - Replacement: `002DD7E0(6)` when byte `+0x17` is 1 (`00568EC5`..`00568ED5`) or 2 (`00568FA8`..`00568FB8`).
  - The function returns 1.
  - **Exact.**
- Limits hold: body statements only, static evidence. OPUS's repair plus its own regression is not independent review; this record is.

## SWE2-AUDIT-SPEC narrowing / notes

None blocking. Two omissions remain in `00568BB0`. They are not falsehoods, and the original review did not ask for them:
- The unconditional `00568BDE and dword [elem+0x48 +8], ~1` hides element `+0x48` on every path, so it stays hidden whenever `r9d` ≠ 0.
- "shows elements `+0x40`, `+0x38` and `+0x48` with the entry's byte `+0x14` and first qword" applies byte `+0x14` to `+0x40` and the qword to `+0x38` only. Element `+0x48` takes neither.
