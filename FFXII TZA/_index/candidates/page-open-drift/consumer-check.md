# Affected-consumer check — topic-page sentences still calling answered questions open (FABLE, Claude Opus 5.5, 2026-09-26)

This is the page-wide companion of `_index/candidates/contract-open-drift/`. `page_open_drift.py` lists topic-page lines
that call a question id open or unestablished while the register row reads ANSWERED. Each of its 35 first-run hits was
read in context.

**Three live drifts, corrected here:**
- **`00-Engine-Core-Runtime/README.md`** said "Open: `SM-1`–`SM-5`", but all five were answered on 2026-09-17/18.
- **`18-Audio/Sound-Selection/sound-trigger.md` "Bind and dispatch"** said "`G-14` stays open on that link", but
  `G-14`'s 2026-09-17 answer maps the named setters' ramp blocks to the applicators (pitch `007BFDB0`, panning
  `007BFD00`, lowpass `007BFC30`, layered volume `007BFE30`).
- **`05-Spawn-Encounter-Lifecycle/.../when-a-group-is-wiped-and-when-it-comes-back.md` §8** said "The box stays open,
  and it must", but `EE-12` was answered on 2026-09-19 by the `@FMC` command census on the authored-presentation page.

**Left as they are, with the reason:**
- **Dated falsification passes** (`O-4` in the runtime-mode ladder's 2026-09-02 pass, `FT-4` in the scratch block's
  2026-09-12 pass, `P-2` in the item-encoding 2026-09-02 pass, and `V-12` in a dated 2026-09-13 section). These are
  history in dated sections.
- **Boxes followed immediately by their ANSWERED text** (`G-1`, `FS-2`).
- **A related but different question** (`AY-5`'s pattern cited for another table).
- **A sub-scope the page itself names** (`EY-1`: "what remains open under that id is only …").
- **A dirty peer overlay** (`EX-9`'s world-tick page).
- **Experiment receipts**, which are never reworded.
- **Table cells and closure notes** that merely mention an id.

**Regression:** `_index/candidates/page-open-drift/page_open_drift.py`. After the fix, a re-run no longer reports
SM-1..SM-5, `G-14` on sound-trigger, or `EE-12` on the respawn page.

| consumer | state |
|---|---|
| `00-Engine-Core-Runtime/README.md` category summary | revised-here |
| `18-Audio/Sound-Selection/sound-trigger.md` "Bind and dispatch" | revised-here |
| `05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md` §8 `EE-12` box | revised-here |
| `_index/OPEN-QUESTIONS.md` SM-1..SM-5, G-14, EE-12 rows | agrees (already ANSWERED) |
