# SD-127: no battle-HUD layout key is read through a base pointer; the only pointer route is the tuning console (OPUS, 2026-09-30)

Register row SD-127 was registered by SWE2-DATA ([the-battle-hud-layout-readers.md](../../../16-UI/Battle-Hud/the-battle-hud-layout-readers.md),
What is not known). It asks which battle-HUD layout keys are also read through a base pointer rather than a
rip-relative load. The page's reader census is rip-relative only. Readers reached through the `002778C0` subtree's
jump tables could carry base-pointer reads it does not see.

This record is static. The checker is `sd127_keys.py` (output `sd127_keys.out`, `FAILS 0`). It sweeps all 38,161
bodies of the `pe` module, including every body a jump table reaches.

## The key set

The battle-HUD keys are the rows of [layout-key-readers.tsv](../../../16-UI/Layout-Parameter-System/members/layout-key-readers.tsv)
whose rip-relative reader is a function the battle-HUD page cites. That gives **86 keys, read by 22 functions**.

## The answer (OPUS)

- **C1: controls.** The sweep decodes the image-base-relative form (SD-121's `0036E3B0` on `022D97B0`) and finds
  `004001D0`'s `lea` of `01E0C590`.
- ~~**K1: none of the 86 keys is read by any of three non-rip routes.** Image-wide:~~
  - ~~**R1:** no image-base-relative operand has a displacement of key − `0x120000`.~~
  - ~~**R2:** there are 37 `lea`s of a layout-block address outside the console installer, and no read through such a
    register lands on a HUD key.~~
  - ~~**R3:** no stored qword holds a key's address.~~

  *K1 narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd127-0930/REVIEW.md); it becomes:*

  > No battle-HUD key is read by an image-base-relative operand at its own displacement, by a stored pointer, or
  > through a block lea followed in its function and two callees deep, apart from the indirect calls `00267A79`
  > (`[r15 + 0x88]`, `rdx = 01E0C32E`) and `00244EF5` / `00246C09` (`call rax`), which are not resolved.
  >
  > Indexed table reads next to the keys are not excluded by code:
  > - `00266530` (`00266588`) and the code at `00266B83` index the 8-entry `01E0C328` table with a 5-bit field, so
  >   entries 8..31 would read HUD-key bytes up to `01E0C3A5`;
  > - `002AEB20` (`002AECA3`, `002AEE26`) indexes the 32-byte tables `01E0CE30` / `01E0CE10` with a text byte − 0x40
  >   that is not bounded below `TargetInfoMoveY` (`01E0CE94`).
  >
  > Whether authored data reaches those indices is not checked.

- **K2: the one pointer route is the development console.**
  - `001AF470` `lea`-installs 85 of the keys into the tuning console's slot-pointer array (`[01F811E8]+0x3B00`).
  - The 86th, `FontItalicScale` (`01E0CF94`), is installed by `001B44A0` into its object's `+0x300`, beside
    `01E0CF90` (`+0x2F8`) and `FontShadowAlphaMuti` (`+0x308`). That is the route the Y-1 check covered for the 13
    keys without a reader.
  - The console reads and writes the keys through those pointers. No battle-HUD function does.
- **K3: two near misses, which are not key reads.**
  - **The `01E0C590` record.** `004001D0` passes this 0x20-byte record to `004006A0`, `004017D0` and `00401D40`. They
    read it at `+0`, `+2`, `+4`, `+8`, `+0x10` and `+0x18` only. The `BossGaugeExColor{R,G,B,A}` keys right after it
    (`01E0C5B0`…, i.e. `+0x20`) are never reached through it.
  - **The `01E0C328` table.** `002679F0` walks an 8-entry table (byte, byte, word) at `01E0C328`–`01E0C347`. Its end
    is exactly the first HUD key, `mScrollListHeight` (`01E0C348`). The walk count is an authored word, not bounded
    in code: a count above 8 would read HUD keys as table entries. That would be an overrun, not a key read.
  - **Two more readers of the `01E0C328` table:** `00266530` (`00266588`) and the code at `00266B83`, each indexing
    it with a 5-bit field. *(narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd127-0930/REVIEW.md))*

**For modding:** ~~editing a battle-HUD key's global, or the instruction that reads it, is enough. No HUD code reaches
a key through a copied pointer, so there is no second read to patch.~~ No HUD code reaches a key through a copied pointer; the open cases are the indexed table
reads above. *(narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd127-0930/REVIEW.md))*

## Limits (OPUS)

- **The key set** is bounded by the page's cited readers and the readers TSV. A HUD key the TSV lacks is not
  covered.
- ~~**R2** follows a `lea`'d address within the same function only. Handed-on addresses are covered for the two cases
  in K3, which are the only `lea` targets within 0x40 bytes of a HUD key. The other `lea` targets have no HUD key
  within 0x40.~~ R2 swept `01E0C000`..`01E0D100`. Outside the console installer, the lea targets within 0x40 below a HUD
  key are K3's two, `001B44A0`'s two (K2), and, outside the block, `0209E608` (+0x10, read to +6 by `00285F00`) and
  `0209E610` (+0x8, index 0..4 at `002BDB3B`). Neither reaches a key. *(narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd127-0930/REVIEW.md))*
- **The `002679F0` overrun** depends on authored counts, which are not checked here.
- **Static only.**

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register row belongs to SWE2-DATA's page.
