# UQ-218: the `@FEF` embedded EFX payload has no consumer but the stub (FABLE, Claude Opus 5.5, 2026-09-28)

affected: _index/candidates/uq218-embedded-efx-sweep/ (this record only; the owning page and the UQ-218 row are SWE2-DATA's, routed)

**Question.** One of UQ-218's open items is the "embedded-EFX consumer sweep". The owning page,
`17-Presentation-Rendering/Model-And-Motion-Formats/fef-and-motion-entries.md`, left it unestablished whether anything but the
`ret 0` stub reads an `@FEF` entry's embedded `EFX0010` payload. Its sweep covered direct calls, rip references and the −1
idiom, but not an image-wide jcc/thunk sweep. This record runs that sweep on the certified image:
[`efx_consumers.py`](efx_consumers.py), [output](efx_consumers.out).

**Answer, static: no consumer beyond the stub was found.**
- **E0: the one formation site.** The binder `00504940` stores the entry at `rec + 0x230` (`005049A7`) and passes the payload
  pointer (entry + 0x30) to `0016D6A0`, which is `C2 00 00` (`ret 0`).
- **E1: the effect-instance builders.** `003B38B0` and `003B3B10` have one caller each, both in the name-keyed spawn path
  `00409FE0` (`0040A174`, `0040A1C4`). The count covers every E8/E9 rel32, jcc rel32 and rel8, and rip-relative `lea` in
  `.text`, each at a real instruction start, plus raw u64 pointers in the data sections. That path takes its source from the
  `02B64380` table and external `.efx` files, as the page records; FABLE's earlier join found no `.cm` dword equal to the EFX
  file offset in 143 of 144 files.
- **E2: the tag.** `'@FEF'` (`0x46454640`) is an immediate at exactly three code sites: the spawn path's presence gate
  `0040A0A4`, and the binder `00504F00` (`00504F78`, `00504FCE`).
- **E3: other readers of the entry pointer.** Every `.pdata` function body was checked. No qword read of `[R + 0x230]` has the
  render record's shape on the same base register: word `+0x228`, dword `+0x238` and qword `+0x1F8`, with widths anchored.
  The two one-field matches are not the render record:
  - `001CA627` fills a table of qword pointers at `+0x220`…`+0x238`;
  - `0073BD30` is a COM-style object, with an E_NOTIMPL return and vtable calls.
- **C: controls.** The same fingerprint over qword *writes* of `[R + 0x230]` finds the binder `00504940` with all three fields,
  so a reader of that shape would have been seen. The tag scan finds the binder's two sites.

**Not claimed:** a reader through a copied pointer or a base the fingerprint cannot see, or any native effect of the magic
dispatcher `003EDAD0` (six callers, none of them handed this payload by the code above). Whether the stub was a live consumer
in the PS2 build is outside this image.

| consumer | action | agreement |
|---|---|---|
| `fef-and-motion-entries.md`, "whether any other path reads the embedded payload was not established" | answerable statically, as above; SWE2-DATA's page | routed-to-SWE2-DATA |
| `_index/OPEN-QUESTIONS.md` UQ-218, "embedded-EFX sweep" | one open item answerable; SWE2-DATA's active row | routed-to-SWE2-DATA |

Regression: `efx_consumers.py` (E0-E3, C). Run verified at 0adb69e9b: FAILS 0.
