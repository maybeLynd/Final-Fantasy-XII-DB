# OV-5 / OV-8 (d): the state-pointer flow census T3b left unrun (OPUS, 2026-09-30)

FABLE's T3b (`../fable-astra-live-facts-0930/t3b_ov58d_region_a.md`) answered (d) statically: over-reservation in
region A (the packed class words, state `+0x4748..+0x4F0F`) can enter only through save-file bytes. Its stated limit
was the unrun pointer-flow census. This record runs that census. It is OPUS production, routed to SWE2-AUDIT-SPEC.

## Correction before publication (OPUS)

The first runs of this census rooted the state only on loads of the state pointer `[02EBF190]`. So a write that
addresses the state block by its **static address** was invisible to it. SWE2-AUDIT-SEM's REJECT of T3b (`837cdd743`)
found one: `002EF4A0` copies `0x6000` bytes from `02166480` into `021B290C` using two `lea`s. That copy covers region A,
and it runs on every post-load (`00233C10` → `00235AF0` → `002EF4A0`, before the magic check).

An earlier draft of this README said "every flow that reaches region A at a known offset is one of FABLE's writers".
That claim came from the unrooted runs and is withdrawn. The census now also roots every rip-relative address inside
the static image `02164280..021BA910`, at its offset from the state (`021B290C`). Control C6 requires `002EF4A0`.

## Method (OPUS, `ov58d_flow.py`, output `ov58d_flow.out`, rows `ov58d_flow.tsv`)

The engine is the value-flow engine of `../k14-closure-stores-0930/k14_actorflow.py`: registers, own stack, lea/add
offsets, switch tables, and callees analysed under their argument values, memoised, to depth 10. It is extended with:
- a caller's stack structure passed by reference;
- SIMD moves carrying two 8-byte halves;
- pointer + index keeping its base offset as a lower bound (token `A@K`);
- registry-row pointers read at an unknown row (token `AR`);
- rip-relative addresses in the static image (token `A` at `address − 021B290C`).

Roots, iterated to a fixpoint:
- every function referencing `[02EBF190]`, the registry cells and rows, or the static image;
- the image getter `002EF640`;
- every global an escape stores a state pointer into;
- every caller of a function returning a state pointer.

The scan runs over the v4 extents (chained tails) plus the UC-1 frontier bodies.

## Controls (OPUS)

| control | what it must find |
|---|---|
| C5 | T3's 318 references to `[02EBF190]` |
| C1 | the state memset `002370D3` as a REGION store |
| C2 | the packed handler `002FD150` writing region A through the registry storage pointer |
| C3 | the zeroing loop `003047F0` writing region A, the pointer in the index register |
| C4 | the save packet's image pointer escaping at the enqueue's `movups` copy `005825A0` |
| C6 | the mirror copy `002EF4A0` as a state writer (the static-image root class) |

Also added after the first re-rooted run (so its INDEXED-UNKNOWN count fell from 33 functions to 12):
- **Escape globals carry the offsets stored into them.** `00253970` stores image + `0x8200` into `020927C0`. A later
  `[020927C0] + 0x47B8` is therefore image + `0xC9B8`, in the image head, not state + `0x47B8`.
- **An indexed store into a global makes it a table.** `022C1740` holds up to nine record pointers
  (`003058C0`, `00304180`, ...).
- **The record getter `00320AB0(i, kind)` returns the token REC.** It computes state + 8 + `0x1C8`·k after
  `cmp al, 0x27`, so k ≤ 39. ~~The 40 records end at state + `0x4728`, below region A (`+0x4748`).~~ *(Corrected 2026-09-30
  on SWE2-AUDIT-SPEC's review `auditspec-review-ov58d-census-0930`:)* The 40 records end at state + `0x4748` (exclusive),
  exactly where region A begins (8 + 40 × `0x1C8`; the checker's `REC_END` always computed this). A store at
  REC + d with 0 ≤ d and d + size ≤ `0x1C8` is RECORD and cannot reach region A.
- **A pass is rerun from scratch when a global is first learnt mid-pass.** Bodies memoised earlier loaded it as
  non-state. Three passes ran; the third was stable.

Controls C7 (`020927C0` carries state − `0x4648C`) and C8 (`00305927` through a `022C1740` entry is RECORD) were added.

## Result (OPUS, run of 2026-09-30, `ov58d_flow.out`, 2,296 s)

All eight controls PASS. 1,138 root functions, 11,197 bodies reached, 100,820 contexts. Escape globals, stable in
pass 3:
- `02092758` = the image, state − `0x4E68C`;
- `020927C0` = image + `0x8200`;
- `0215E6E0` = state − `0x46484`;
- `022C1740` = a table of REC;
- `00120000` = ~~unknown (an image-base-relative table).~~ the image base, deliberately not tracked *(corrected 2026-09-30, AUDIT-SPEC review)*.

| class | stores (unique) | what bounds it |
|---|---|---|
| REGION (known offset overlapping region A) | 4 | All four write **zero**. `002370D3` is the state memset. `002EF603` / `002EF663` clear the whole image (`0x56690` bytes from `02164280`). `00253A93` is a `0x58`-byte header clear (`memset([02092758], 0, 0x58)`) that the engine sized as unknown: a false overlap, read by hand. |
| REGISTRY-STORAGE | 8 | T3b's packed handler `002FD150` and zeroing loop `003047F0` (controls C2, C3) |
| RECORD | 297 | inside one battle-stats record, so below ~~`+0x4728`~~ `+0x4748` *(corrected 2026-09-30)*: **excluded** |
| INDEXED-UNKNOWN | 70 in 12 functions | see below |
| RECORD-INDEXED | 9 in 5 functions | record + an index: `0030E130`, `0030E360`, `0030FED0`, `0030EA40`, `0031A630` |
| INDEXED-BELOW, base below the records (< +0x8) | 100 in 38 functions | index not yet bounded |
| INDEXED-BELOW, base inside the record array | 158 in 31 functions | index not yet bounded |

The **INDEXED-UNKNOWN** functions, read by hand:
- **Fixed-count block copies**, which propagate words and create none:
  - `002EF4A0`: mirror → state, `0x6000` bytes;
  - `00229B40` / `005844A0`: state → mirror (`0xC0` × `0x80` from image + `0x4E68C` to image + `0x2200`), and
    `00229B40` also state → capture image;
  - `00583C00`: controller buffer → image head.
- **The rebase `0030B6A0`**, which is in T3b's list.
- **Not yet read:** `003266C0` (10), `00583D60` (7), `00252D40` / `00254E00` (`[r9 + 0x3244]` / `+0x32C4`),
  `003112F0` (2), `0030B180` (`[rsi + 0x59C8]`) and `003279B0` (`[rdx + 0x5B42]`).

The record pre-copy fixup `00234ED0` is bounded by hand: eight iterations (`r9` `0x7374` → `0x7414`, step `0x14`), with
stores at state `+0x90` .. `+0x463C`, below region A.

## Independent cross-check: SWE2-AUDIT-SEM's inlined copy-loop census (OPUS reading of `d998217e2`)

`../auditsem-review-livefacts-0930/inline_bulk.tsv` lists 3,895 compiler-inlined store loops across the binary,
including bodies with no unwind entry.
- **Constant base inside the images:** of its loops whose base is a constant address there, one writes the active
  state: `002EF4B3` (`002EF4A0`, base `021B290C`, `0xC0` × `0x80`). The others (`002EF760`, `002EF7E0`) write the
  capture image beyond its state block.
- **Whole-image-sized copies:** each of its `0x56680`-byte copies has a destination that is not the active image.
  - `002EF570`: active → `022676C0`.
  - `002EF690`: capture `021BA940` → `02211000`.
  - `0057E310`: `02211000` (getter `002EF630`) → capture (getter `002EF620`).
- **`0x9400`-byte copies:** `002334D6` / `00233955` / `00233566` write heap buffers `[0208E690]` / `[0208E698]`.
  Those are allocated by `00384510(0x9400)` at `00236982`, stored at `00236989`.
- **Agreement:** every block copy of this census appears in AUDIT-SEM's (`00229B91`, `00229BF0`, `00584521`,
  `00583C30`, `00583CE0`, `002EF4B3`), and AUDIT-SEM's census adds no loop writing the active state.

## Conclusion for (d) (OPUS)

- **What stands:** no store into region A found here creates a word.
  - The known-offset stores write zeros.
  - The block copies carry the save file's words or the game's own earlier words.
  - The registry-storage stores are T3b's writers.
  - T3b's statement survives, with its writer list corrected: over-reservation enters region A only from save-file
    bytes, now by two routes (the file's region-A words, and the file's mirror words through `002EF4A0`).
- **What is not closed:** 12 INDEXED-UNKNOWN / RECORD-INDEXED functions not yet read, and 69 INDEXED-BELOW functions
  whose index is not yet bounded. Each can reach region A only if its index runs past the record array or past the
  field it addresses. Bounding those indices is the residue, routed to SWE2-STRUCT.
- **The census's own limits** are listed in `ov58d_flow.out`, and none of them is closed here:
  - 437 depth/recursion cuts carrying a state value;
  - 15 indirect calls receiving one;
  - 26 escapes;
  - *(added 2026-09-30 on the AUDIT-SPEC review)* image-base-relative loads of the REC table `022C1740` (`003111D0`,
    `00311245`, `00311252` in `00310DB0`) are not followed, so `0031E800`, `00385F60` and `003112F0` are not analysed
    with those arguments from that site.

**Review:** SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The T3b writer-list correction goes to FABLE.

## The mirror copy and the controller backup: a new route, not a new source (OPUS)

- `002EF4A0` copies the image's mirror section (`02166480` = image + `0x2200`, `0x6000` bytes) over the state's first
  `0x6000` bytes. Region A is therefore also written from mirror + `0x4748..0x4F0F`.
- The image head `02164280 + 0xE240` is the part the save/load controller backs up and restores. Its constructor
  `00582860` allocates `0xE240` at `[02CA99B8]+0x588` and calls `00583CB0` (image → buffer). On a failed load,
  `00583C00` (buffer → image) restores it (`spawn-placement-and-retirement.md` status rows; `ui-request-router.md`,
  `SaveUI_RestoreActiveHeaderFromControllerBackup`).
- So the buffer holds only an earlier copy of the game's own image head. The mirror holds whatever the image head held,
  which after a load is the save file's bytes (the kind-9 copy writes the whole image).
- **For (d):** these copies propagate words; they do not create them. T3b's conclusion, that over-reservation can
  enter only from save-file bytes, survives with two routes: the file's region-A words directly, and the file's mirror
  words through `002EF4A0`. T3b's writer list must add `002EF4A0`, `00583C00` and `00583CB0`. The mirror-writer census
  (`ov58d_mirror.py`) finds three known-offset stores into the mirror's copy of region A. `002EF603` / `002EF663`
  are the whole-image zero fills, and `00253A93` is the `0x58`-byte header clear (a false overlap, above). The
  state → mirror copies `00229B40` / `005844A0` are the only other writers, so the mirror holds zeros, the game's own
  state words or the save file's words.
