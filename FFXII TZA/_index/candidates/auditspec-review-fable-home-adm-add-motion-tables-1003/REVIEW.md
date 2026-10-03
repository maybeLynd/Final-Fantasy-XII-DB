# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-adm-add-motion-tables-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-ADM-ADD-MOTION-TABLES-1003` · Package: `_index/candidates/fable-home-adm-add-motion-tables-1003/` (committed in `410ec4476`, reviewed at HEAD `f49bb4021`; the package and the page are unchanged since that commit and unmodified in the working tree) · Page: `17-Presentation-Rendering/Model-And-Motion-Formats/adm-add-motion-tables.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The one row is exact, and its caller `002E7CE0` is read in this page's section 3. The page already anchors the call site `002E7DAD`.

One advisory follows: the sentence leaves out that the caller's 16-bit value passes through in `edx`. Saying so would answer the page's own "What that value is was not established".

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python, without `--apply`. It exited 0 and printed `VERIFY 1 functions, 5 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The committed `.out` is the pre-apply `DRY` run with the same counts. The heading is at page line 512, and the row at line 518 matches `rows.json` byte for byte.
- **rows.json.** 1 row, 5 anchors. Rejected 1 (`002ECCF0`, "already cited by" `how-the-engine-chooses-3d-or-flat-movement.md`). Skipped 0, missing 0, corrections 0.
- **`002EDB80` (0x48 B): exact.**
  - `cmp cx, -1` / `je ret`. Otherwise `movsx rax, cx` / `imul 0x740` / `add rbx, [022C6F28]` / `je` on a zero sum, then `cmp dword [rbx+0x284], 0` / `je`.
  - Then `002EDBAF call 003E6CE0` (+0x2F) with `rcx` = the record, and `or dword [rbx+0x290], 0x800`. Every other path writes nothing.
- **entered_from.** The raw byte scan finds one reference: `002E7DAD` = `002E7CE0` + 0xCD. There `ecx` = `movzx word [rdi]` and `edx` = `movzx bp`, gated on the record being live and `[+0x6C8] == 1`.
- **Host fit.**
  - Section 3 (line 152) reads `002E7CE0` as the one other body that reads the binding state: "it applies a 16-bit value to the base record and, **only while that record is in state 1**, to the body-model record too". Its interior list includes `002E7D94` and `002E7DAD`, the state test and this call.
  - The body is that second application. It fits, and it is cited on no other page (repo-wide grep).
- **Advisory (not a defect): the value the page could not name.**
  - `002EDB80` never touches `rdx`, so the caller's `edx` (`movzx bp`) reaches `003E6CE0`. That function is `add rcx, 0x580` / `jmp 003E37C0`.
  - `003E37C0` does `movzx eax, dx` / `shl eax, 0x1A` and merges that bit into dword `[rcx]` (`xor` / `and 0x4000000` / `xor`), then `or eax, 0x10` and stores.
  - So bit 0 of the 16-bit value becomes bit 26 of the record's dword `+0x580`, and bit 4 of that dword is set.
  - Suggested wording for the clause: "makes the call at `002EDB80` + 0x2F with the record and the incoming `edx` unchanged (it reaches `003E37C0`, which copies bit 0 of `dx` into bit 26 of dword record`+0x580` and sets bit 4)".
- **Advisory (tool).** The applier's caller test is a substring test that the applied row satisfies by itself. Here the caller is also cited at line 152.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
