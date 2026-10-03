# SWE2-AUDIT-SPEC review: FABLE cloud-drafted F-homing rows (fable-ebp2-container-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-EBP2-CONTAINER-HOMING-1003` · Package: `_index/candidates/fable-ebp2-container-homing-1003/` · Page: `25-EBP-Script-Container/Container/ebp2-container.md` (commit `eea05327e`, reviewed at HEAD `db98e3d59`; the package is unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- **Applier.** `interior_applier.py` was re-run fresh without `--apply`. It printed `VERIFY 1 functions, 5 anchors`, `ALREADY`, `FAILS 0`, and wrote nothing. The section is on the page at line 758, and the sentence is on the page verbatim.
- **rows.json.** 1 row, 5 anchors. Rejected 0, skipped 0, missing 0, corrections 0.
- **Semantic pass.** The row was read clause by clause against `disr.py` output of the certified image.
  - `003545B0`: `call 002640C0` gets the incoming registers (`mov rbx, r9` changes none of them), and its result p is kept in `rdi`.
  - Five pops follow at +0x2C, +0x36, +0x40, +0x4B and +0x56 (a in `esi`, b in `ebp`, c in `r14d`, d in `r15d`, e in `ebx`), each with `rcx` = the saved `r9`.
  - `00264D60(p, e)` goes to `r12`, then `002673A0(p, e)` and `test eax, eax` / `jne`, which skips the last call.
  - The last call is at +0x94 (`00474070`) with `rcx` = `r12`, `edx` = d, `r8d` = c, `r9d` = b, `[rsp+0x20]` = a and `[rsp+0x28]` = qword `[p+0xB0]`.
  - Every argument slot matches the sentence.
- Limits: body statements only, static evidence. The cloud draft and FABLE's re-read are not independent review; this record is.
