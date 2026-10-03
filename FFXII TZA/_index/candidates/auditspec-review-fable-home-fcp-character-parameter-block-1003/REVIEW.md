# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-fcp-character-parameter-block-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-FCP-CHARACTER-PARAMETER-BLOCK-100` · Package: `_index/candidates/fable-home-fcp-character-parameter-block-1003/` (committed in `5a7a7f97e`, reviewed at HEAD `c6de67245`; the package and the page are unchanged since that commit and unmodified in the working tree) · Page: `17-Presentation-Rendering/Model-And-Motion-Formats/fcp-character-parameter-block.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

Both rows are exact against the bytes. Each body has one caller, and that caller is a function this page names. One host is thin; that is recorded as an advisory below, not as a defect.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python, without `--apply`. It exited 0 and printed `VERIFY 2 functions, 8 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The committed `.out` is the pre-apply `DRY` run with the same counts. The heading is at page line 805, and the rows at lines 811 and 812 match `rows.json` byte for byte.
- **rows.json.** 2 rows, 8 anchors. Rejected 0, skipped 0, missing 0, corrections 0.
- **`003B4750` (0x1E B):**
  - `003B4754 mov rdx, [01FD4A78]` (the qword at that cell, not its address), then `003B475B call 003B4A50` (= +0xB) with `rcx` as passed.
  - `xor ecx, ecx` / `test eax, eax` / `setne cl` / `mov eax, ecx`: 1 when the 32-bit result is non-zero, else 0. Exact.
  - entered_from: the raw byte scan finds one reference, `0042CD20 call 003B4750` = `0042CBF0` + 0x130. Its `ecx` is `movsx` of word `[rdi]`, and a non-zero result runs `CharacterRenderRecord_UpdateViewDependentPresentationFactors` (`0042CD2C`).
- **`004096F0` (0x1D B):**
  - `mov edx, [rcx+4]`. Zero takes `00409704 add rcx, 0x10` / `00409708 jmp 006B5C70` (+0x18, a tail jump). One takes `mov rax, [rcx+0x30]` / `ret`. Any other value goes to `xor eax, eax` / `ret`. Exact.
  - entered_from: one reference, `00429360 call 004096F0` = `004292B0` + 0xB0. It takes the `00409F50` result and passes its own result as `rdx` to `00423B10` at `0042936E`.
- **Host fit.**
  - `004096F0`: `004292B0` is cited in a body statement on this page, line 188, the loader-contract event map. That statement cites the span `0042933F`–`0042936E`, and the call site `00429360` lies inside it. The body produces the motion entry that this page's event map starts through `00423B10`. It fits.
  - `003B4750`: `0042CBF0` is cited on this page only in passing: line 397 ("What is not known") and line 750 (a section-8 italic line naming "the LOD updates `0042CBF0` and `0042D050`"). Those lines do make it one of the section-8 runtime-copy readers that the page's status line counts ("a LOD scale"). So the body has a single caller that is inside the page's subject, and this is not a hub link.
- **Advisory (not a defect): a closer home for `003B4750`.** `003B4A50` is the character colour-filter collector of element `0x41` (`the-element-types-40-42-a0-ab-d0-d1.md` line 138: it "collects the records whose scope matches a character"). So `003B4750` asks whether any colour filter targets this character before `0042CBF0` runs `CharacterRenderRecord_UpdateViewDependentPresentationFactors`. `how-a-character-fades-the-ten-channels.md` reads `0042CBF0` whole (section 4a; table row at line 496) and would carry this row more naturally. If FABLE prefers to move it, that page cites the caller, so the applier would pass there. A one-clause gloss would also help the reader here: "(`003B4A50` is the element-0x41 colour-filter collector)".
- **Advisory (tool).** The applier's caller test is a substring test. After the apply, the row's own "entered from" cell satisfies it. Both callers are also cited outside the section (`0042CBF0` at lines 397 and 750; `004292B0` at line 188).
- Neither body is cited on any other page (repo-wide grep).
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
