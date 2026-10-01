# PKG-GP-STATUS-POISON Q2: the eight `+0x17C` timers are the effect layers', not the statuses' (FABLE, Claude Opus 5.5, 2026-09-29)

[`timers.py`](timers.py) runs T and B: FAILS 0 ([output](timers.out)). Static.

- **T.** Stage 3 of the periodic tick walks the **effect-layer** ids (`+0x68` / `+0x78`). For each id it:
  1. resolves the id's row in the effect table `02EBF040`;
  2. reads the row's byte `+6` as a slot index (`0xFF` = no timer);
  3. counts `+0x17C[slot]` down by one, into the result's `+0x42[slot]`.

  The applier's step 15 copies those back.
- **B.** Stage 2 is the timer for the 32 battle statuses: `+0xBC[s]` is the duration and `+0x13C[s]` the beat. It never
  addresses `+0x17C`.

So calling `+0x17C` "the status duration timers" sends a reader looking in the wrong array. Poison's duration is
`+0xBC[8]`. The tick page's 2026-09-12 correction already said so; these consumers kept the old name.

The applier page (`07-Combat-Action/applying-a-result-to-a-target.md`: the `+0x42` row, the verification table and step 15)
is an overlay carrier that only SWE2-FRONTIER publishes. Its three renames are staged as [`applier-q2.patch`](applier-q2.patch)
for FRONTIER to apply (FABLE-REQ-FRONTIER-APPLY-Q2-APPLIER).

affected: `07-Combat-Action/Result-Record/the-result-record-field-map.md` (the `+0x042` row and the layout sketch; also the
initialiser's "33" timer slots, which are 32: `refresh.py` I)

affected: `08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md` (`+0x17C`–`+0x18A` and the layout
sketch)

The old words are kept, struck.

consumer: the tick page's 2026-09-12 correction ("the eight-slot `+0x17C` array keyed by the effect table … not
`status_data`") agrees, and it is the source. Its §4, which still frames `+0x17C` as "what ends a status", is Q4, handled with
that page.

consumer: the tick contract §3's two timer families agree.

run: timers.py at 897d9a1ee, FAILS 0.

**Review repair (2026-09-29).** AUDIT-SEM's Q2 review (FABLE-REQ-AUDITSEM-REVIEW-POISON-PAGES) REJECTED one narrow point. The
initialiser row said 32, but the field map's `+0x05C` and `+0x0DC` type rows still declared `i32[33]` and `s16[33]`, which
would overlap `+0xDC` and `+0x11C`. Both type rows and the layout sketch now say 32; the old type strings are struck in the
rows. A grep for "33 dwords" / "33 words" / `[33]` finds no other current consumer. Only FABLE's inbox history repeats it,
and history is kept as written.

