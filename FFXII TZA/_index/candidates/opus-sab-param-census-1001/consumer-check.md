# Consumer check: the `.sab` `+0x0A` census - 267 `se` folders, not 268; the 350 distinct values explained (OPUS, 2026-10-01)

Item 33 of the 18-Audio reconstruction-readiness map (RE repo `docs/readiness/18-audio.md`): the container page's
"350 distinct values in `.sab`" against the map sound list page's "strict ordinal ... one slot per folder ... 268
folders". OPUS read all 4,609 `.sab` headers from the archive (`sab_param_census.py`).
- The archive has **267** `se` folders under `sead_data_win`; there is no `se003`-`se006`.
- Their ordinals run 0-267 with slot 3 unused, one per folder.
- The 132 `shout` folders (66 jp, 66 us) carry 83 more values, `5172`-`5256`.
- 267 + 83 = 350, and every folder holds exactly one value.

So both pages were right about the mechanism, and "268 folders" was a miscount: there are 268 slots and 267 folders.

- **Corrects:**
  - spp-map-sound-list.md: "268 folders" becomes 267 `se` folders (two places);
  - register row SQ-1: the "0–267 over 268 folders" phrase is corrected the same way;
  - sab-sound-bank-container.md: the 350 is explained where it is stated (pointer only), and the OPUS
    supersession note that left it "not re-counted" is resolved.
- **Affected:** 18-Audio/Sound-Bank-And-Voice-Formats/spp-map-sound-list.md, 18-Audio/Sound-Bank-And-Voice-Formats/sab-sound-bank-container.md, _index/OPEN-QUESTIONS.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | spp-map-sound-list.md `+0x0A` paragraph and DATA note | revised-here |
  | sab-sound-bank-container.md `+0x0A` figures (`:148`, `:347`, `:405`) and its §7 struck note | revised-here |
  | OPEN-QUESTIONS row SQ-1 | revised-here |
  | _index/AUDIT-LOG.md entry with "268 folders" (dated history) | agrees (history; not edited) |
  | RE repo `docs/readiness/18-audio.md` item 33 | routed-to-OPUS (the RE repo map is updated from this commit) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-sab-param-census-1001/sab_param_census.py, verified at 518a7f2d8: 16 archive checks, FAILS 0 ([`sab_param_census.out`](sab_param_census.out)); reads the VBF at `D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf` (path argument accepted). `sab_followups.py` re-runs as ALREADY, FAILS 0.
