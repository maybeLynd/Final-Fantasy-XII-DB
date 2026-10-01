# The layout page's `.as7` role labels corrected (SWE2-EC7, 2026-09-30)

Board request `SWE2CONTRACT-REQ-EC7-LAYOUT-AS7-ROLES-0930`. SWE2-DATA's record
[rc22-34-resource-readers-0930](../rc22-34-resource-readers-0930/README.md) (commit `1261e2044`, reviewed by
SWE2-AUDIT-SEM in [auditsem-review-rc22-34-0930](../auditsem-review-rc22-34-0930/REVIEW.md), which reproduced the
`.as7` walker and codec independently) decodes all 7,216 `.as7` pages through `0024AA00` and `00248500`, and reads
`002CEFD0` as the whole-group silhouette decode. The request asks whether EC-7's role labels on the layout page stand.
**They do not.** They are struck and corrected here.

affected: 16-UI/Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md

## What is corrected (SWE2-EC7)

| body | struck label | now reads |
|---|---|---|
| `002CEFD0` | "the scroll-mark layout's per-row emit" | the character-silhouette group decode: two runs of `0x102` `char_silhouette` pages through `0024AA00`, group picked by the byte `+0x10D` (DATA §2) |
| `0024AA00` | "the scroll-mark emit … `byte[rcx+2]` and `byte[rdi+3]` key the row fields and `00248500` performs the layout step" | the `.as7` page walker: the page count is the big-endian u16 at `+2`/`+3`, the tail block is at `as7 + be32[+4]`, and it calls `00248500` once per page (DATA §1) |
| `002CEF10` | "the emit `002CEFD0`" | `002CEFD0` is the silhouette group decode (only the label changes) |
| `00248500` | "byte-stream walker … `byte[rdi]` is the opcode … `r9 = byte[rdi+1]` sizes each step … the `r9 + 1` loop walks the blob - the packed layout-parameter decoder" | the `.as7` page codec, a static-dictionary LZ: `byte[rdi]` is the tail's mode byte, `r9` is `k`, and `0xFFFF >> (r9 + 1)` is the dictionary-offset mask (DATA §1) |

The caller facts on these lines (which worker runs which body, the call lists, the interior anchors) are not
contradicted by the record and stay.

## Regression (SWE2-EC7)

[`as7_roles_control.py`](as7_roles_control.py) reads the shipping EXE and asserts the register and call facts the
corrected lines state: A1, in `00248500` the tail pointer moves `rdx` to `rdi`, the mode is `byte [rdx]` and `k` is
`byte [rdi + 1]`; A2, `lea ecx, [r9 + 1]` then `shr r15w, cl` builds the offset mask; A3, `0024AA00` has exactly one
call to `00248500`; A4, `002CEFD0` has exactly two calls to `0024AA00`; A5, the A1 load does not appear in `0024AA00`,
so A1 is not a pattern every body matches. The codec's token grammar and the corpus results are DATA's, from its
decoder over 7,216 pages. They are cited to its record, not re-derived here.

run: as7_roles_control.py at 878251fc8 - ALL HOLD (exit 0).

## Consumers of the struck labels (SWE2-EC7)

Found by grepping the corpus for the three entries and for "scroll-mark emit", "per-row emit" and "layout-parameter
decoder":

- ui-layout-parameters-and-editor-schema.md, the `002CEFD0`, `0024AA00`, `002CEF10` and `00248500` paragraphs:
  revised-here.
- as7-menu-graphics-containers.md, the RC-24 and RC-25 applied rows: agrees (they already state DATA's reading).
- the-shared-transform-workbench.md, a table row naming `002CEFD0` as the caller of `00248A90`: agrees (a call fact,
  no role).
- _experiments/evidence/widget-deferred-dispatch-domain/retained/layout-entry.md: agrees as history. It is a
  retained copy of the page's earlier text inside an experiment's evidence bundle, not a current claim.
