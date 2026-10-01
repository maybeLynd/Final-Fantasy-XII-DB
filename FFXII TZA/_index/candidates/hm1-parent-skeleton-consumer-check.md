# Affected-consumer check: HM-1's second skeleton, and two RenderStrideC0Element store rows (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

**The ruling** (`_index/candidates/hm1-parent-skeleton/hm1_parent_skeleton.py`, 4 checks):
- `RenderStrideC0Element +0x0C` is the encoded pointer to the row's parent row. Every writer (`0046E300`, `0046E370`,
  `0046E420`) stores `0020E620(bank[row +0x08])`, or encoded null (`0046E420`'s -1 arm; the constructor `003721E0`).
- `+0xA8` is the row's character-render-record index. All five u16 readers take `0xFFFF` as none, else
  `[022C6F28] + index x 0x740`, and a record whose `+0x284` is 0 counts as none.
- So HM-1's mapped pose path (`003703A0`, state 2) takes its second skeleton from the element's parent row: the model
  the mapped element is attached to.

**Not a correction.** The two store rows keep their widths and extents. They gain a proven role and a name, and
their earlier names and meanings stay in the evidence cell as history:

| offset | was | now |
|---|---|---|
| `+0x0C` | `encodedRef00C`: "a 32-bit relative pointer in ENCODED form" | `parentRowRef` |
| `+0xA8` | `word0A8`: "four accesses, all movzx, so read unsigned" | `renderRecordIndex` |

**Not claimed:** who writes `parentSlot` `+0x08`, and so which parent the `hc1006_03` row has in shipped data;
`+0xA8`'s writer.

**Consumers:**

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` RenderStrideC0Element `+0x0C`, `+0xA8` | renamed and meaning added; history kept | revised-here |
| `_index/OPEN-QUESTIONS.md` HM-1 | narrowing prepended; earlier text kept | revised-here |
| the add-motion tables page, HM-1 notes | narrowing added; the not-claimed line now names the parent's writer | revised-here |
| `_index/candidates/hm1-pose-mode2/hm1_pose_mode2.py` (P4: the other record comes through `[skeleton+0xC]` and `+0xA8`) | unchanged; S3 here names what P4 reached | agrees |
| pages naming `encodedRef00C` / `word0A8` | none found (grep of the database's `.md`/`.tsv` outside the store and its access index) | agrees |

Run receipt: executed at a2017baec - `hm1_parent_skeleton.py` (4 checks, FAILS 0), `types_index.py --validate` (0
errors), `check_type_refs.py` (0 dangling).
