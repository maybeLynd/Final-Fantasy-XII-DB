# Affected-consumer check: who writes the element row's parentSlot (HM-1, OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

Corrects: `_types/fields.tsv` CharacterRenderRecord `+0x3CC` (was `linkedRecordIndex3CC`, "sibling link word of
+0x3CE") and `+0x3CE` (was `linkedRecordIndex3CE`, "record-pool link index"). It also corrects RenderStrideC0Element
`+0x0C`, whose "every writer" list named three writers where there are five, and the matching sentence in OPUS's own
HM-1 narrowing of the same day. Two more element rows are corrected:
- RenderStrideC0Element `+0x20` (was `unobservedSpan020`, "no access anywhere");
- RenderStrideC0Element `+0xB0` (was `index0B0`, "what it indexes is unread").

**Question.** The earlier pass (`hm1-parent-skeleton/`) found only `-1` writers of the element row's `+0x08`
parentSlot. So which parent does a row such as `hc1006_03` get? The discriminator is whether a positive writer exists.
If one exists, the next question is whether its parent comes from shipped skeleton/model data or from a runtime
attach.

**Result** (`_index/candidates/hm1-parent-writer/hm1_parent_writer.py`, A1–A7):

**The writers.**
- Two attach bodies store the parent row's `+0x04` slot into the child row's `+0x08`: `00370180` and `00373160` (A1).
  The earlier search missed them because they are not in the field-access census.
- `00373160` is entered only by a conditional tail jump in `00370390`, so a call-graph query sees no caller (A2).
- Both bodies are reached only through the bank wrappers `0046E590` / `0046E640`. Those wrappers also write `+0x0C`
  by the rule the store states, which makes five `+0x0C` writers, not three (A2).

**Where the parent comes from.**
- The wrappers' callers are the render-record attach helpers `004218A0`, `004215A0`, `004219C0` and `004211B0` (A3).
- The dirty-state pass drives the first two. It takes the parent as the record indexed by the child record's
  `+0x3CE`, and the attach point from `+0x3CC` (A4).
- `+0x3CC` is a code that `004215A0` dispatches on. No pool index is formed from it (A5), so "sibling link word" was
  wrong.
- Only `0042F310` / `0042F3B0` store the two words (A6).
- The movement page traces those two setters to script verb `00D9` `attach` and the chocobo mount.

**Conclusion.** The parent is chosen by a runtime attach, not by skeleton or model data.

**The map is chosen by the child's own name (A8, A9).**
- The element create path `0046E4D0` runs the constructor, then `00372820(element, …, name)`.
- `00372820` copies the 32-byte name into `+0x20`. It goes through `lea r11, [rsi + 0x20]`, which is why the
  displacement census saw no access there.
- It then sets `+0xB0` to the index of the `SkeletonMapping.bin` entry with the same name, or −1 if none. That table
  is at `02AD9E30`, loaded by `0036FFF0`, 0x30 bytes per entry.
- `003703A0` indexes the table by `+0xB0`.
- The batch receiver census listed other `+0x20` sites, but those act on objects with fields past `+0xC0`, so they
  are not this type.

**Where hc1006_03 appears.** It is c1006's high variant `C:22`. Only four US event manifests list it: `dgl_g0102`,
`gol_a0200`, `hne_b0102` and `rsn_z0200` (`c1006_join.py`, section_012). The attach calls in those maps are made by
prop scripts (`c22_scripts.py`): Reddas's sword, a manufactured nethicite, and six shackles. None is made by c1006's
own actor.

**The attach is authored.** Shipped scripts call `attach` at 3,042 sites and `attachoff` at 2,394, in 981 of the
10,036 `.ebp` files; the count includes every language copy (`attach_census.py`, reusing FABLE's verb-census
decoder).

**Still open.** What attaches hc1006_03's actor in those four maps. The other callers of the attach setters are not
traced: `002EDAA0` (reached through `002E3110` and `002EE290`), `00426C90`, `00427320` and `0042DC10`.

**Regressions.**
- A7 fails on the pre-fix store (`linkedRecordIndex3CC` / `linkedRecordIndex3CE`, three-writer list).
- A10 fails on it too (`unobservedSpan020`, `index0B0`).
- Both pass after `Tools/work/OPUS/hm1e/patch_store.py`, tested on a copy through the `FIELDS_PATH` variable.

**Consumers:**

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` CharacterRenderRecord `+0x3CC` / `+0x3CE`, RenderStrideC0Element `+0x08` / `+0x0C` / `+0x20` / `+0xB0` | corrected or extended; history kept in each evidence cell | revised-here |
| `_index/OPEN-QUESTIONS.md` HM-1 | narrowing prepended; it corrects the earlier narrowing's three-writer sentence | revised-here |
| `17-Presentation-Rendering/Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md` (the "Not claimed: which parent" bullet) | narrowed in place | revised-here |
| `06-Movement-And-Navigation/Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md` ("parent's render-record index at `+0x3CE` and the bone at `+0x3CC`") | already reads the words this way | agrees |
| `17-Presentation-Rendering/Character-Render-Records/how-a-character-fades-the-ten-channels.md` §3a ("owner's record index at `+0x3CE`", "attachment slot id at `+0x3CC`") | already reads the words this way | agrees |
| `00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md` (the `0042F310` measurement) | a measurement of the same stores; no role claimed | agrees |

Run receipt: executed at bbd3af82a - `hm1_parent_writer.py` A1–A6, A8, A9 PASS; A7, A10 FAIL on the pre-fix store and PASS on the patched copy (FIELDS_PATH).
