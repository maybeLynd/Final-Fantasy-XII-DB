# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-effect-element-type-dispatch-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-EFFECT-ELEMENT-TYPE-DISPATCH-1003` · Package: `_index/candidates/fable-home-effect-element-type-dispatch-1003/` (committed in `5a7a7f97e`, reviewed at HEAD `c6de67245`; the package and the page are unchanged since that commit and unmodified in the working tree) · Page: `17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 8 rows were read. Seven sentences are exact, and one (`00623D70`) states a write that the body does not make. Three rows need repair:

- `00366A30` is mis-homed. Its caller is a UI label widget procedure that this page lists only as a queue entry pointing to another page.
- `004FF230` was not a frontier body. `efx-and-efb-effect-containers.md` has cited it since `cea938e19` (2026-09-30), and its sibling `004FE4A0` belongs there with it.
- `00623D70` needs one clause reworded.

The other four rows stand: `003769F0`, `004FF1B0`, `004FF1F0`, `00524790`.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python, without `--apply`. It exited 0 and printed `VERIFY 8 functions, 38 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The committed `.out` is the pre-apply `DRY` run with the same counts. The heading is at page line 2385, and the rows at lines 2391–2398 match `rows.json` byte for byte.
- **rows.json.** 8 rows, 38 anchors. Rejected 1 (`003A9AD0`, "already cited by" this page). Skipped 0, missing 0. Corrections 1 (`00366A30`, the B + 0x12 index-word wording; the corrected text is the one on the page).
- **Raw references.** A byte scan of the image (E8/E9, `0F 8x`, absolute pointers) confirms every entered_from site as a direct call:
  - `00366A30`: `00366E26` and `00366E8B`, both in `00366B80`;
  - `003769F0`: `0046158D`;
  - `004FE4A0`: `00538389`, plus `005387E9` and `005387F7` in `005387B0`;
  - `004FF1B0`: `0052F76A`;
  - `004FF1F0`: `0052F6B4`;
  - `004FF230`: `00537C8F`, plus `00537FAF`, `0053835F` and `005387BF`;
  - `00524790`: `005245FB`, plus an `.rdata` qword at `01DAEFA0`;
  - `00623D70`: `0062B049` and `0062B063`.

**Semantic pass, row by row:**

- **`00366A30` (0x14B B): exact.**
  - `movsx r11, word [rdx+0xA]` indexes the 8-byte entries at `[rdx+0x20]`. They become four words at `rsp+0x68`: `+0`, `+2`, `+4 AND 0xFFF`, and `(dword +4 >> 12) AND 0xFFF`.
  - The 5th argument is `[rsp+0x80]` after `push` + `sub 0x50`, and the 6th and 7th are `[rsp+0x88]` and `[rsp+0x90]`.
  - The lerp is `sub` / `imul` / `shr 8` / `add r8w`. The logical shift and the arithmetic shift give the same low word.
  - The nibble store is `[rdi+0x5C]`. The call at +0x13B (`00366B6B`, `002D8D10`) takes `r8 = rsp+0x68` and `r9 = rsp+0x60`. Its 5th argument is `rsp+0x30`, a block holding dword 0, 0.0 and `rdx+0x28`, and its 6th is 1.0 from `01CEBBA8`.
- **`003769F0` (0x25 B): exact.** `movzx edx, cl` indexes the table at stride 0x90 (`rdx*9*2*8`) from `02ADBB40`. `test ecx, ecx` checks the full register. Then `cmp [entry], ecx` and `movss xmm0, [entry+8]`; otherwise `xorps`.
- **`004FE4A0` (0x3C B): exact.** Three `call 004304F0` at +0xF, +0x1A and +0x25 on `rcx`, `+0x10` and `+0x20`, with `edx` restored from `ebx`. It returns `rdi+0x80`.
- **`004FF1B0` (0x3B B): exact.**
  - The selector is `movzx r8d, byte [[rcx+0xE0]+0xC2]`.
  - 0 → +0x35 `jmp 005382F0`; 1 → +0x30 `jmp 00537F10`; 2 → +0x2B `jmp 005382F0`; 3 → +0x26 `jmp 005382F0`; any other value → `ret`.
- **`004FF1F0` (0x3B B): exact.**
  - 0 → +0x35 `jmp 005382F0`; 1 → +0x30 `jmp 00537F70`; 2 → +0x2B and 3 → +0x26, both `jmp 00538320`.
- **`004FF230` (0x3F B): exact.** Three `call 00430AF0` at +0xF, +0x1A and +0x28 on `rcx`, `+0x40` and `+0x80`. It returns `rdi+0xD0`.
- **`00524790` (0x2E B): exact.**
  - `cmp cx, -1` returns `0xFFFF`.
  - Otherwise `movsx rax, cx` / `imul 0x740` / `add rcx, [022C6F28]`. A zero sum (`je` on the `add`'s ZF) or dword `+0x284` = 0 returns `0xFFFF`.
  - Otherwise +0x29 `jmp 00421D70`.
- **`00623D70` (0x39 B): one clause overstates the body.**
  - `mov eax, [rcx+0x18]` / `btr eax, 0x1F` clears bit 31 in the register copy only. Nothing is written back.
  - The text says "clears bit 31 of dword `rcx+0x18`", which reads as a store. See N1.
  - The three returns are exact. `jbe` is unsigned. The `> 1` branch uses qword `[rcx+0x20]`. The `== 1` branch uses address `rcx+0x20`. The `== 0` branch uses a null base through `cmove rcx, r8`. The index is `edx` zero-extended (`mov eax, edx`).

**Host fit:**

- **`003769F0`.** It fits. `00461270` is cited at line 2010. That line says `00377100` indexes `02ADBB40` with the same `cl*0x90` and `dword == ecx` guard. `003769F0` is its float reader.
- **`004FF1B0` and `004FF1F0`.** They fit. `0052F560` is the shared publish tail of `00442170`'s eight post-pass arms (lines 2046–2070). The bodies switch on the same `+0xC2` subtype byte as `004FF270`.
- **`00524790`.** It fits. `00524320` closes the element field commit `00523C30` (line 2186).
- **`00623D70`.** It fits. `0062B020` "runs first" in the element-list reset at line 1572. Count `[+0x18]` masked, inline-or-heap 0x10-stride array at `+0x20`: this body is that array's indexed fetch.
- **`00366A30`: the defect.**
  - This page cites `00366B80` only twice. Line 669 is in the table "39 large bodies cited only at their entry", where the row names `Widget-Object-Model/the-widget-constructor-and-object-sizes.md` as the page that documents it. Line 1020 is a pass-22 neighbour sentence ("the shader-material body `00366B80` calls `0024A5A0`").
  - `00366B80` is the 0xE0-byte label-widget procedure that `00366740` installs. `15-Input/Modal-Toggles/r2-force-fight-toggle.md` documents it in body statements: line 226 (the `022CBE08` store at `003670B7`), line 300 (its table row) and line 429 ("builds a `0xE0`-byte widget with procedure `00366B80`").
  - `00366A30` packs a layout-sheet entry's 12-bit fields and an alpha-scaled position into a draw call. It is UI drawing, not effect-element dispatch.
- **`004FF230` and `004FE4A0`: the defect.**
  - `004FF230` was already cited before this package, contrary to the README's "No page cited these functions". `efx-and-efb-effect-containers.md` line 246 reads "Each body runs `004FF230` (three `0x40`-byte blocks at `+0x00`, `+0x40` and `+0x80`)", added in `cea938e19` (2026-09-30). That page also states the operation both helpers perform (`00430AF0`, `004304F0`: decode, add the delta, re-encode).
  - Its §2b subtype table cites the callers `00537C80` (line 240) and `00538350` (line 242).
  - On this page the callers appear only as tail targets inside the `004FF270` interior row (line 2330).
  - Both helpers belong with the `0x700` relocator on the efx page.
- **Advisory (tool).** The homing pack's frontier list missed a prose citation in backticks (`004FF230`). Also, the applier's caller test is a page substring test that the applied row satisfies by itself.

## SWE2-AUDIT-SPEC narrowing

1. **N1, `00623D70`.** Replace "clears bit 31 of dword `rcx+0x18`; when the result is above 1 (unsigned)" with "takes dword `rcx+0x18` with bit 31 masked off in a register (memory is not written); when that value is above 1 (unsigned)". Also replace each "`edx` * 0x10" with "zero-extended `edx` * 0x10". The rest of the sentence stands.
2. **N2, `00366A30`.** Re-home it unchanged to `15-Input/Modal-Toggles/r2-force-fight-toggle.md`, entered from `00366B80` + 0x2A6. That page cites `00366B80` at lines 226, 300 and 429. Note the second site, `00366B80` + 0x30B. Remove the row from this page.
3. **N3, `004FF230` and `004FE4A0`.** Move both rows unchanged to `17-Presentation-Rendering/Effect-File-Formats/efx-and-efb-effect-containers.md`, after §2b. Keep entered_from `00537C80` + 0xF and `00538350` + 0x39. Both callers are in its subtype table. Then correct the package README: `004FF230` was already cited at line 246, so it is a re-cite with interior anchors, not a newly homed body.
4. Regenerate `homing_applier.out` after the edits.

Limits: static evidence only. A cloud draft plus FABLE's re-read is not independent review; this record is.
