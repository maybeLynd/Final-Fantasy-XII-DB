# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-ui-request-router-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-UI-REQUEST-ROUTER-1003` · Package: `_index/candidates/fable-home-ui-request-router-1003/` (committed in `60f3e63b3`, reviewed at HEAD `33eb7192f`; the package is unmodified in the working tree) · Page: `16-UI/Request-Router/ui-request-router.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

Both rows are exact against the bytes. Both entered_from sites are direct calls to the body. Both hosts cite the caller in a body statement.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 2 functions, 8 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The section is on the page at line 994, and both rows match `rows.json` byte for byte.
- **rows.json.** 2 rows, 8 anchors. Rejected 0, skipped 0.
- **Semantic pass.** Both rows were read clause by clause against the full `disr.py` listing (rip targets resolved).
- **`002D5060` (0x43 B):**
  - Dword `01E0C1DC` (u32 0x1C0) goes through `cdq / sub eax, edx / sar eax, 1` to `r9d` and then `edx` (`mov edx, r9d` at `002D5083`).
  - Dword `01E0C1D8` (u32 0x200) goes through the same sequence to `ecx`, and `r8d` = 1.
  - `cdq` then `sub eax, edx` adds 1 to a negative value before the `sar`, so the halving is a signed division that rounds toward zero.
  - The call at +0x2A (`002D508A`, `002899A0`) returns `rax`. That value is passed in `rcx` to the call at +0x35 (`002D5095`, `00246AC0`), kept in `rbx`, and returned (`002D509A` `mov rax, rbx`).
  - All 5 anchors are on these instructions.
- **`002F8B90` (0x19 B):**
  - `mulss xmm1, [01CEBB70]` (0.5), then `addss xmm1, xmm0`, then `movss xmm0, [01CEBC70]` (4.0), then `minss xmm0, xmm1`.
  - MINSS returns the second (source) operand when either operand is NaN, so a NaN sum is returned unchanged. "4.0 as the first operand and the sum as the second" is exact.
- **entered_from:**
  - `00290740` + 0x1A = `0029075A`, `call 002D5060`. Its result is stored to `[0209BE80]` + 0x10FB8.
  - `00309E40` + 0x18 = `00309E58`, `call 002F8B90`, with `xmm0` = float `022C2184` and `xmm1` = `022C2188` − `022C2184`.
- **Host fit.**
  - Both callers are cited on this page only by their own homed rows (`ui-request-router-1002`, page lines 972 and 975). Those rows are body statements, not neighbour, boundary or out-of-scope lines. Both rows were accepted by the 1002 review.
  - Neither body is cited on any other page (repo-wide grep of `002D5060` and `002F8B90`).
  - `002D5060` makes the object that its caller stores in the `0209BE80` manager. `002F8B90` is the clamp for its caller's `022C2188` store. Both stay with their callers.
- **Note (non-blocking).** In `002F8B90`, "`xmm0` plus `xmm1` times 0.5" means `xmm0 + 0.5·xmm1`, which is what the code does. Writing "`xmm0` plus half of `xmm1`" would remove the precedence reading `(xmm0+xmm1)·0.5`.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
