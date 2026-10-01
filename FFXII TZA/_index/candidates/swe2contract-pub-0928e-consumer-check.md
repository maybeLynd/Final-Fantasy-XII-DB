# Consumer check — SWE2CONTRACT-PUB-GLYPH-0928K (TIM2 carrier correction)

Publish scope: `25-EBP-Script-Container/Container/ebp2-container.md`,
`Container/members/ebp2_slot_populations.py` (new census control),
`how-a-line-of-text-becomes-glyph-quads.md`, `AUDIT-LOG.md`,
`ADDRESS-INDEX.md`, `SWE2-CONTRACT.md`, this record.

## Correction carried by this publish

Corrects the TIM2 carrier-family claim in
`how-a-line-of-text-becomes-glyph-quads.md` and `AUDIT-LOG.md` (also
restated on `ebp2-container.md`): the AUTHSPLIT-0928 publish said
"`+0x28` TIM2 rides only event packs", taken from a top-N directory
listing that sampled only event paths. The carrier recount over all
1,114 EBP2 containers gives **55 `plan_map` globals / 12 event packs**
for slot 6 — mostly globals, not event-only. The recount also produced
the complete family profile: global-only = slots 3 (`+0x1C`, 359),
4 (`NAVI`, 209), 16 + 19 (`FF12`, 517 + 271); event-only = 14 (`LGT2`,
140); both = slots 2 (602 + 226) and 6 (55 + 12).

## Consumers checked — each agrees

- `how-a-line-of-text-becomes-glyph-quads.md` — agrees, revised-here
  (coda-6 carries the inline correction marker and the full family
  profile).
- `AUDIT-LOG.md` — agrees, revised-here (the AUTHSPLIT entry's TIM2
  line is marked corrected in place; the SECFULL addendum carries the
  recount).
- `ebp2-container.md` — agrees, revised-here (new `files` column on
  the dispatch table plus the family-profile paragraph).
- `SWE2-CONTRACT.md` resume block — agrees, revised-here.
- Grep for other repeats of the wrong claim: none found outside the
  corrected lines.

## Regression that measures it

`ebp2_slot_populations.py` (staged in this publish under
`25-EBP-Script-Container/Container/members/`) re-derived every figure
above from the shipped US VBF corpus — verified at 2ad08cce6.
Re-running it is the regression for the family split.
