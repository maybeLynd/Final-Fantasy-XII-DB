# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-fef-and-motion-entries-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-FEF-AND-MOTION-ENTRIES-1003` · Package: `_index/candidates/fable-home-fef-and-motion-entries-1003/` (committed in `5a7a7f97e`, reviewed at HEAD `c6de67245`; the package and the page are unchanged since that commit and unmodified in the working tree) · Page: `17-Presentation-Rendering/Model-And-Motion-Formats/fef-and-motion-entries.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The one row is exact against the bytes, and the body is a gate inside the motion starter `00423B10` that this page documents.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python, without `--apply`. It exited 0 and printed `VERIFY 1 functions, 5 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The committed `.out` says `VERIFY 1 functions, 5 anchors` / `DRY (verified; --apply writes)` / `FAILS 0` (pre-apply). The section heading is at page line 1021 and the row at line 1027 matches `rows.json` byte for byte.
- **rows.json.** 1 row, 5 anchors. Rejected 2 (`0025C130`, `003CD7F0`, both "already cited by" this page). Skipped 0, missing 0, corrections 0.
- **Semantic pass.** The row was read clause by clause against the full `disr.py` listing of `00422FD0` (0x78 B).
  - `test rdx, rdx` / `je 0042303B` (the `xor eax, eax` exit): null `rdx` returns 0.
  - `00422FE5 mov rcx, rdx` / `00422FE8 call 003AB7F0` (= +0x18). Its `rax` goes to `rcx` at `00422FFB`.
  - `ecx = r8d AND 0xF000`, `cmp ecx, 0x5000`: equal gives `xor edx, edx`; otherwise `edx = r8d AND 0xFFF` (`00423004`). Then `0042300C call 00408F80` (= +0x3C).
  - `test rax, rax` / `je` exit; `test dword [rdi + 0x284], 0x10000` with `rdi` = incoming `rcx`; `test dword [rax + 4], 0x30000`. Each `je` goes to the return-0 exit; only all three passing reach `mov eax, 1`. Exact.
- **entered_from.** Raw byte scan (E8/E9, `0F 8x`, absolute pointers) finds exactly one reference: `00423C4F call 00422FD0` = `00423B10` + 0x13F. There `rcx` = `rbx`, `rdx` = `[rsp+0x40]`, `r8d` = `esi`; a zero result skips the tail into the start path.
- **Host fit.** `00423B10` is cited in body statements on this page: line 456 names it the starter (`00423B10(rbx = motion request, rdx = ctx, esi = motion index)`), and line 718 is the consumer hand-off in its motion-start path. Both callees are this page's resolvers: `003AB7F0` (lines 213, 656) and `00408F80`, the entry-index resolver (lines 97, 105, 479). The body has one caller. It stays with its caller. `00422FD0` is cited on no other page (repo-wide grep, `_experiments` copies aside).
- **Advisory (tool, not a defect of this package).** The applier's "the page cites the caller" test is a substring test on the page text. Once the section is applied, the row's own "entered from" cell satisfies it, so an `ALREADY` re-run no longer tests host fit. Here the caller is also cited at lines 14, 453, 456, 718 and 830, outside the section.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
