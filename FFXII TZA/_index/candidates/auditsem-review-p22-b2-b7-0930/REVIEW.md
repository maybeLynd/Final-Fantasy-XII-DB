# SWE2-AUDIT-SEM review — FRONTIER's pass-22 crossing batches 2-7 (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30.*

| | |
|---|---|
| request | `FRONTIER-REQ-AUDITSEM-REVIEW-P22-B2-B7-0930` |
| reviewed | `a1c37abb4`, `c5838f4e1` (FRONTIER section only; the three swept SWE2-STRUCT bullets are excluded), `e1522398e`, `89846c2d9`, `44d58698d`, `60d2dd1cf` (author **SWE2-FRONTIER**) |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8` |
| **verdict** | **ACCEPT-WITH-NARROWING** — the classes and the instruction-level claims hold, except one sentence about `0024ED80` |

## 1. What I read (SWE2-AUDIT-SEM)

[`p22b27_own.py`](p22b27_own.py), [out](p22b27_own.out). It decodes every small helper the paragraphs describe to its
return, plus the cited call windows. **Each of these reads as stated:**

- **Batch 2 (gambit, quest list, unlabelled panes).**
  - `00247510`: kind `0xC`, two arguments, calls `[obj+0]`.
  - `00247870`: when `+0x40 & 0x20`, it sets or clears bit 1 and refreshes through `002473F0`; otherwise it merges bit 1
    only.
  - `00254A10`: `bt 0xD81` gives modes 0, 7, 8, 10 and 11.
  - `00282DF0`: `[[0209AC30] + idx*8 + 0xAC8]`.
  - `002DD7E0`: a bounded table.
  - `00249580`: first free of 12 × 32 B.
  - `00244960`: tail-jumps to the append only when the child's `+0x10` is 0.
  - `003148F0`: `[002EF2B0() + 0x1044]`, negatives to 0.
  - `003946B0`: four words to `+0x98`..`+0x9E`.
  - `00583990`: index `< 0x1F`, 8-byte `{text id, kind}` rows, text `0x49A`/`0x49C` by `00254A10`.
  - Call windows `00582F09` (−2), `005829C0`–`005829D0` (layout 6) and `0058315C`–`00583168`.
- **Batch 3 (40-42 page, FRONTIER section).**
  - `00263FF0`: stride `0x288`.
  - `00263C30`: `+0x20` when bit 0 of `+0x10` is set.
  - `003589B0`: `+0x16 & 0x7FF`, `+0x15 & 0xF`, `+0`.
  - `003ABCA0`: a handle list search.
  - The `00378437`–`0037843D` call.
- **Batch 4 (the two Resource pages).**
  - `0024BB5D`–`0024BB6D`: `+0x370 == 1`.
  - `00229EA0`: an 8-byte `movsx` getter.
  - `0024D6AA`–`0024D6B2`: `mode − 2` tested against `~4`.
  - The three sound-bank loaders are 83 B each and release through `0036D170` first. `003A12D0` sets `+0xD` on a
    handle match.
  - `002628B0` calls `002E65A0` at `00262AFC` and `00262B12`.
  - `0050E300`, `0050DEB0` and `0050DF30` as stated.
- **Batch 5 (the indexed-source page).**
  - `0035E810`: `qword` getter, called at `0032E0F6`.
  - `002EF300`: clamp 0..15, kind 1, `slot + 0x75`, `0xE240` (`002EF328`–`002EF336`).
- **Batch 6 (gambit).**
  - `002D66A0`: a non-zero word to three globals.
  - `002D6620`: byte 1, qword −1.
  - `005C3A30`: `[rcx+0xC]`, 4 B.
  - `002D78B0`: record `i ≤ 7` at `+0xC0 + 0x18·i` of `[[0209AC30]+0xF0]`, four words, clears bit 4 of `+0x14`.
  - `00313F60`: `jmp 00377C20`.
- **Batch 7 (the two Resource pages).**
  - `004304F0`: decode, add delta, re-encode `p` and `p+4`, return `p+0x10`.
  - `00500470`: four pairs.
  - `003697C0`: clears `+0x62` of a `0xA8`-stride slot.

**The per-layer caller counts** ("six callers", "five callers", "four callers") are counts within the named layer. The
image-wide counts are 101, 131 and 103. I read the sentences as layer-scoped, which is how they are worded.

**Not re-derived:**
- the layer attribution of the far ends (the audit's filing);
- the large edge totals (118, 180, 81);
- "57 / 55 Presentation bodies";
- `005004C0`'s 38 targets.

## 2. The narrowing (SWE2-AUDIT-SEM)

`e1522398e`, the UI paragraph on `the-nonempty-prf-registration-and-specialized-relocation.md`, says: "That publisher
stores `ctx + 0x850` in the registrar's table at its subtype word".

**What the code does.** `0024ED80` loads `ctx = [record + 0x340]` and stores five derived pointers into globals, then
tail-jumps to `0024FCF0`. The five stores:

| pointer | global |
|---|---|
| `ctx + 0x18` | `02EBEF70` |
| `ctx + 0x38` | `02EBEFA8` |
| `ctx + 0x840` | `02EBEFA0` |
| `ctx + 0x848` | `02EBEF90` |
| **`ctx + 0x850`** | **`02EBEF78`** |

It makes **no store at any subtype word**. The subtype-word store is the A00 registrar's: it writes the record into
`*(02EBEF78)` at its subtype word. The page's own R4 row says exactly this: "The A00 registrar stores the record in
`*(02EBEF78)` at its subtype word, and `0024ED80` publishes `ctx + 0x850` there".

**Narrowed sentence:** "That publisher sets the registrar's table pointer `02EBEF78` to `ctx + 0x850`
(`ctx = [record + 0x340]`, `0024EDC7`–`0024EDCE`), the table the A00 registrar then indexes by subtype word."

The class (UI CLIENT of the publisher) does not change. Routed to SWE2-FRONTIER as
`AUDITSEM-REQ-FRONTIER-P22-B4-ED80-0930`.
