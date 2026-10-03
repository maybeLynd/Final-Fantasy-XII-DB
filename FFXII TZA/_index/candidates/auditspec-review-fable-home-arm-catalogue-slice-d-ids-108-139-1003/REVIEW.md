# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-arm-catalogue-slice-d-ids-108-139-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-ARM-CATALOGUE-SLICE-D-IDS-108-139` · Package: `_index/candidates/fable-home-arm-catalogue-slice-d-ids-108-139-1003/` (committed in `410ec4476`, reviewed at HEAD `f49bb4021`; the package and the page are unchanged since that commit and unmodified in the working tree) · Page: `00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-D-ids-108-139.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The one row is exact, and its tree-walk polarity is right. The body is a keyed-map "contains" check that the arm runner `001BF8B0` makes, and this page reads `001BF8B0` in body statements.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python, without `--apply`. It exited 0 and printed `VERIFY 1 functions, 5 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The committed `.out` is the pre-apply `DRY` run with the same counts. The heading is at page line 490, and the row at line 496 matches `rows.json` byte for byte.
- **rows.json.** 1 row, 5 anchors. Rejected 0, skipped 0, missing 0, corrections 0.
- **`001A7990` (0x71 B):**
  - `001A7999 call 001A76D0` (+0x9) with `rcx` as passed. A zero result returns it, and it is 0.
  - Otherwise `rax = [rbx+0x460]`, `r8 = rcx = rbx+0x450`. The loop is `cmp [rax+0x20], rdx` / `jb` to `rax = [rax]`. In the else branch, `rcx = rax` (remembered) and `rax = [rax+8]`.
  - After the loop, a remembered node equal to `rbx+0x450` resets nothing. Otherwise `cmp rdx, [rcx+0x20]` / `jae` keeps the node, and the else branch resets `rcx` to `rbx+0x450`.
  - It returns `setne (rcx != rbx+0x450)`.
  - The sentence matches clause by clause: unsigned compares, `+8` when the key is not below k, `+0` otherwise, the slot starting at `rcx+0x450`, and 1 only when k is not below the remembered key.
- **entered_from.** The raw byte scan finds one reference: `001BFA49` = `001BF8B0` + 0x199. There `rcx` = `001A9930()` (the console state) and `rdx` = `[rbp-0x60]`, and a zero result skips to `001C0038`.
- **Host fit.**
  - `001BF8B0` is the slice-D arm runner that this page reads at lines 461, 465 and 469.
  - Line 469 reads: "`001A9CD0` (147 B) is the `+0x448` keyed-record insert `001BF8B0` runs … `001A76D0` resolves `rdi`/`xmm3` into a key, `001A2F70(rbx+0x448)` finds-or-makes the slot".
  - `001A7990` uses the same key function `001A76D0` and walks the tree whose head node sits at `+0x450`, inside that `+0x448` map. It is that map's membership test. It fits, and it is cited on no other page (repo-wide grep).
- **Advisory (not a defect).** One clause would tie the row to its neighbour: "(the `+0x448` map that `001A9CD0` inserts into; the key is `001A76D0`'s)".
- **Advisory (tool).** The applier's caller test is a substring test that the applied row satisfies by itself. Here the caller is also cited at lines 201, 461, 465, 469 and 488.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
