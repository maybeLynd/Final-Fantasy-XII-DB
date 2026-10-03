# The battle-unit field map's suspend / restore copy sites re-filed (OPUS, 2026-10-03)

Answers SWE2STRUCT-REQ-OPUS-FIELDMAP-SUSPCOPY-SITES-1003. SWE2-STRUCT's census fix
([`swe2struct-suspcopy-census-1003`](../swe2struct-suspcopy-census-1003/consumer-check.md)) found that the
suspend / restore copy loop's 7-move tail addresses `+0xB30`..`+0xB90`, not `+0x730`..`+0x790`. The field map's
`+0x730`..`+0x790` rows still cited those tail sites.

OPUS re-read both loops at the bytes:
- `0030EDA0` (restore) and `0030EFF0` (snapshot) each run nine 0x80-byte passes from `+0x6B0`.
- After the ninth pass the pointer sits at `+0xB30`, so the tail moves `0030EE13`..`0030EE44` and `0030F0A9`..`0030F0DD`
  address `+0xB30`..`+0xB90`.
- `+0x730`..`+0x790` are reached by the loop body on its second pass, with the pointer at `+0x7B0`:
  - writes `0030EDC7`..`0030EDF7` (`[rcx-0x80]`..`[rcx-0x20]`);
  - reads `0030F05D`..`0030F093`.

[`apply_suspcopy.py`](apply_suspcopy.py) strikes each tail site in the seven rows, gives the body site, and corrects
the `+0x790` row's sentence. `0030F0DD` reads `+0xB90`, so `+0x790` is not "reached by immediate displacement".
The rows' address-forming `lea` sites (`0030F060`, `0030EDB6`) match the census and are kept. It applies 11 edits;
a re-run skips all 11, FAILS 0 ([`.out`](apply_suspcopy.out)).

**Also published here.** The page's earlier uncommitted lines also go in this commit:
- OPUS's 04-Actor readiness corrections (`00861EC0` is a `memset` thunk; `00383670` is 204 B; the `+0x48` bit
  writes);
- FABLE's slot-label fixes (`0030CFB0` is 185 B; `0030D070`'s `r8b` is the slot index).

All of them were applied in the tree and waiting in SWE2FRONTIER-PUB-READINESS-BATCH-1002. FRONTIER is told to drop
the page from its batch.

**One mechanical fix to a waiting line.** FABLE's `0030D070` slot-label line struck "not a found flag", which the
page never said. The publish gate refuses a strike of unsaid text. The strike now covers the page's former words
("`r8b = 0` found flag"). FABLE's correction and attribution are unchanged.
