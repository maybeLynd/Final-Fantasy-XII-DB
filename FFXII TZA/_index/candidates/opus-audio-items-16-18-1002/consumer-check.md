# Consumer check: 18-Audio readiness items 16-18 settled - pan ranges, the volume ceiling, the output count (OPUS, 2026-10-02)

These are the three items of the 18-Audio reconstruction-readiness map (RE repo `docs/readiness/18-audio.md` §2.4,
items 16-18) that waited on `sead-function-identification.md`. That page was held by a READY, unclaimed SWE2-EC7
publish task, which holds no resources, and the page is clean.

- **Corrects:**
  - sead-function-identification.md §2: "three panning axes: left/right, front/rear, up/down" becomes three ranges, of
    which the driver uses two (UQ-242's dated answer). Its §6 summary line follows.
  - sead-function-identification.md §3: the volume ceiling is not configurable. `01CEBBA8` is the float 1.0 and no
    instruction writes it (1,488 reads).
  - how-a-sound-request-becomes-a-voice.md UQ-242 answer: the output count is always 8 (`02EAD34C`'s one writer
    stores 8), so only the eight-output ring is used (an added note).
- **Affected:** 18-Audio/sead-function-identification.md, 18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | sead-function-identification.md §2, §3, §6 | revised-here |
  | how-a-sound-request-becomes-a-voice.md UQ-242 geometry | revised-here |
  | how-a-sound-fades-the-ramp-and-its-six-curves.md (`01CEBBA8` as +1.0, range 0.0-1.0) | agrees |
  | sead-win-config.md §3 (`02EAD34C` = 8) | agrees |
  | RE repo readiness map items 16-18 | routed-to-OPUS (updated from this commit) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-audio-items-16-18-1002/items_check.py, verified at 1ff7875c4: the 8-store, the accessor, 01CEBBA8 = 1.0 with 0 writers and 02EAD34C with 1 writer, FAILS 0 ([`items_check.out`](items_check.out)). `apply_items.py` re-runs as ALREADY, FAILS 0.
