# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-the-encoded-id-class-registry-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-THE-ENCODED-ID-CLASS-REGISTRY-100` · Package: `_index/candidates/fable-home-the-encoded-id-class-registry-1003/` (committed in `5a7a7f97e`, reviewed at HEAD `e0e99b7c6`; the package is unmodified in the working tree) · Page: `00-Engine-Core-Runtime/the-encoded-id-class-registry.md`

## SWE2-AUDIT-SPEC verdict: REJECT

All three sentences, sites and anchors are exact.

- **One of the three hosts is wrong.** `00243EE0` is a UI layout pass. It copies position words into child records and into widget `+0x98`/`+0x9A`. Its caller, the battle-menu action-list reader `002C4720`, appears on this page only as one of the classes that `0035D330` is called with ("`002C38B0` / `002C4720` class 2", line 329). Nothing in the body touches the encoded-id registry.
- The two comparator rows (`002CFDA0`, `002D01A0`) fit. They look up class-1 records through `0035D330(1, …)`, and this page names their callers as the class-1 users.

Same disposition as the 1002 `contract-ui-request-router` record: one mis-homed row in three rejects the package, and the repair moves that row.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 3 functions, 15 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The section heading is at page line 654 and the three rows (lines 660-662) match `rows.json` byte for byte.
- **rows.json.** 3 rows, 15 anchors. Rejected 0, skipped 0, missing 0.
- **`00243EE0` (0x85 B), read in full.**
  - `test dword [rcx], 0x3FFFC` / `jbe ret`. `test` clears CF, so this is `je`: bits 2-17 are zero.
  - The loop re-reads `[r11+0x10]` and `dword [r11]` on every pass (`shr eax, 2` / `movzx eax, ax`, unsigned `jb`). The kind is `(dword [entry+8] >> 2) & 0xF`, and the `sub 2` / `sub 3` / `sub 3` / `cmp 1` ladder maps 2, 5 and 9 to `00243F16` and 8 to `00243F3F`.
  - The 2/5/9 arm copies words `+4`/`+6` of `[entry]` to the entry's `+0xC`/`+0xE`. The 8 arm copies the same words to `+0x98`/`+0x9A` of `[entry+0x18]` when that is non-null. `movsx r10d` then a 16-bit store keeps the bits.
  - Every clause holds.
- **`002CFDA0` (0x92 B), read in full.**
  - `0035D330(1, word [rcx] << 0x10)`, then `0035D330(1, word [rdx] << 0x10)`. `[rax+0x38]` of the first is read before the second call, and `sub edi, [rax+0x38]` / `jne` returns first minus second.
  - Otherwise both are looked up again, and `sub ebx, [rax+0x30]` / `cmovne esi, ebx` returns that, or `word - word` (zero-extended).
  - Exact.
- **`002D01A0` (0x52 B), read in full.** The same pattern on `+0x30` alone, then the word difference. Exact.
- **entered_from.**
  - `002C4720` + 0x8D5 = `002C4FF5`, `call 00243EE0`, with `rcx = [rsp+0x70] + 0x50`. It is the only caller.
  - `002D0100` + 0x73 = `002D0173`. The raw index also has `002CFD7A` (in `002CFD30`) and a tail `jmp` at `002D0015` (in `002CFFE0`).
  - `002CFEE0` + 0xA2 = `002CFF82`, the only caller.
- **Host fit.**
  - `002CFDA0` and `002D01A0`: line 329 names `002CFEE0` / `002D0100` as the class-1 callers of `0035D330`, and the comparators make exactly those class-1 lookups. They fit.
  - `00243EE0` is the defect. `002C4720` is the `ActionList…` mist reader. It is read on `16-UI/Battle-Hud/the-battle-hud-layout-readers.md` (line 82, whose offsets are "`add`ed to the anchor widget's `+0x9A`/`+0x9E` pair") and on `16-UI/Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md` (lines 268 and 314, interior anchor `002C4731`). The UI pages treat `+0x98`/`+0x9A` as the widget's position pair (for example `002CA0E0`, ui-layout-parameters line 1632: "`word[+0x98] += dx`, `word[+0x9A] += r8w`"). On this page the caller is cited only as a client of the class registry, and the body has nothing to do with classes or ids.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.

## SWE2-AUDIT-SPEC repair

1. Remove the `00243EE0` row from this package and from the section already on the page (the applier prints `ALREADY`).
2. Re-home it **unchanged** on `16-UI/Battle-Hud/the-battle-hud-layout-readers.md`, which cites `002C4720` in its own reader table, row 82. `16-UI/Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md` is the alternative.
3. The `002CFDA0` and `002D01A0` rows are exact and stay.

## SWE2-AUDIT-SPEC advisories (not defects)

- The section intro says "Functions no page cited until now". `002CFDA0` already has its own `SWE2-EC7-64 update` section, with interior anchor `002CFDC9` (the same first anchor as this row), on `00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md` (line 921, since `f25702b2e`). `002D01A0` is named there at line 895. That page's `status:` is PARTIAL, which is not evidence-bearing, so the F gate still counted both bodies as frontier, and the homing is legitimate. But the sentence is literally false for this row. "no evidence-bearing page" would be accurate, and a pointer to the query-record page's notes would help.
