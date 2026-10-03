# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-the-six-vfx-display-layers-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-THE-SIX-VFX-DISPLAY-LAYERS-1003` · Package: `_index/candidates/fable-home-the-six-vfx-display-layers-1003/` (committed in `5a7a7f97e`, reviewed at HEAD `c6de67245`; the package and the page are unchanged since that commit and unmodified in the working tree) · Page: `17-Presentation-Rendering/Effect-File-Formats/the-six-vfx-display-layers.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

All three rows are exact. Each body has a single caller that this page cites in body statements.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python, without `--apply`. It exited 0 and printed `VERIFY 3 functions, 10 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The committed `.out` is the pre-apply `DRY` run with the same counts. The heading is at page line 283, and the rows at lines 289–291 match `rows.json` byte for byte.
- **rows.json.** 3 rows, 10 anchors. Rejected 0, skipped 0, missing 0, corrections 0.
- **`001868A0` (0x42 B):**
  - `mov rbx, rcx` / `001868A9 call 001EDE70` (+0x9) / `test eax, eax` / `je`.
  - `001868B2 call 001EDDA0` (+0x12) runs only when the first result is non-zero.
  - Then `cmp byte [rbx+0xDBB], 0` / `mov eax, [rbx+0xDD0]`. A non-zero byte gives `mov rax, [rbx + rax*8 + 0xB50]`; zero gives `[... + 0xB48]`. Exact, including "the incoming `rcx`, kept in `rbx`".
- **`00186A50` (0x21 B):** the same select on `rcx` with no calls. Exact.
- **`00862C00` (0xE B):** `mov rax, [01F7F4D8]` / `mov eax, [rax+0x90]`. Exact. There is no null check, and the sentence claims none.
- **entered_from.** The raw byte scan finds one reference to each:
  - `0017FE70` = `0017FE60` + 0x10;
  - `0017FEF0` = `0017FEE0` + 0x10;
  - `003A3832` = `003A3740` + 0xF2.
  In both getters, `rcx` is the `00189120` result.
- **Host fit.**
  - `001868A0` and `00186A50`: OPUS's interior rows for `0017FE60` and `0017FEE0` (lines 278 and 279) describe exactly these bodies, as "a 66-byte helper" and "a 33-byte helper". Lines 230–232 make the two getters the emit-layer writer's first-emit choice. They fit.
  - `00862C00` reads dword `+0x90` of the `01F7F4D8` singleton. This page names that singleton as the one `00862C30` loads (line 166). Line 232 has the emit-layer writer `001B2530` storing `+0x90 = ebp`. The caller `003A3740` is "the drain of the depth-sorted display list" (line 46; V2 at line 261). The body reads back a field this page writes, inside this page's drain. It fits.
  - None of the three bodies is cited on any other page (repo-wide grep).
- **Advisory (not a defect).** The page could say that `00862C00` reads back the `+0x90` that `001B2530` stores (line 232). The row is correct without it.
- **Advisory (tool).** The applier's caller test is a substring test that the applied row satisfies by itself. Here every caller is also cited outside the section.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
