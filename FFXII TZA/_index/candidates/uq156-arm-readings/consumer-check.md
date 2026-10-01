# Affected-consumer check — UQ-156 arm 10 / arm 14 one-line summaries (FABLE, Claude Opus 5.5, 2026-09-26)

FABLE's 2026-09-18 one-line summaries of arms 10 and 14 are superseded by full readings. The full readings are on the
map-screens page, under the 2026-09-26 narrowings.

Two summaries are wrong:
- **Arm 10, "a cursor step on the track map … and a full list walk on the location map".** The track arm is a close
  and a hand-off to the page's command dispatcher `002B6DB0`, followed by a rescale. Any cursor motion would be inside
  that dispatcher, which is not read. The location arm is confirm-by-marker-kind, cancel, zoom toggle, dispatcher and
  marker step.
- **Arm 14.** Its callee list split `002B7460` / `003BED70` / `00271CB0` onto the track map, but both pages run them.

The arms' extents, sizes, the `TrackMapScale` read and every other part of the 2026-09-18 narrowing hold.

Also closed here: `00254560`'s case 1 is the constant 1, and the location map's path behind it (`002BB785`–`002BB7DC`)
never runs.

**Regression, run by FABLE 2026-09-26:** `_index/candidates/uq156-arm-readings/uq156_arms.py`, 17 checks, FAILS 0.
- It re-derives the case-1 target and its `mov al, 1`.
- It checks that no direct branch or case-table arm start falls inside the dead range.
- It checks each arm's callee set, with a planted negative: the track arm 10 has no marker step.
- It checks the link fields that arm 10 writes and arm 14 reads.

| consumer | state |
|---|---|
| `16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md` §2.3a, the 2026-09-18 narrowing | revised-here (the two clauses struck, pointer to the full readings) |
| `_index/OPEN-QUESTIONS.md` UQ-156 row (the same sentence, copied) | revised-here (struck the same way) |
| the page's 2026-09-26 arm 10 narrowing (track map) | agrees (it is the source of the track-arm reading) |
| `_index/AUDIT-LOG.md`, `_index/_inbox/*` | history; the phrases do not occur there (grepped 2026-09-26) |
