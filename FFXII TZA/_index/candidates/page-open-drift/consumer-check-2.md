# Affected-consumer check, second pass — pages calling ANSWERED questions open (FABLE, Claude Opus 5.5, 2026-09-26)

**Why a second pass.** `page_open_drift.py` compared each register status cell with `startswith("ANSWERED")`. About
130 rows carry a bold `**ANSWERED …**` cell, so their consumers were never scanned: the first run reported 34 hits,
and with the emphasis stripped the scan reports 165. The VBF page's "AS-2 remains open" was one of the missed hits
(fixed in `58e96bd2c`). Two fixes are in the scanners (`page_open_drift.py`, `contract_drift.py`):
- the status cell is stripped of `*`, `~` and spaces before the compare;
- a `~~strike~~` that spans lines now covers its middle lines too.

**How the 129 new hits were read.** A classification pass read each hit in context: 24 LIVE, 57 HISTORY, 44
OTHER-QUESTION, 3 SUBSCOPE and 1 UNSURE. FABLE re-read every LIVE row's register cell before writing its note. A LIVE
hit is undated body text that tells a reader today the question is open, with no strike and no following answer.

**Corrected here (strike of the exact old text, plus a dated supersession note):**

| consumer | id | state |
|---|---|---|
| `00-Engine-Core-Runtime/README.md` l.27 | BH-1 | revised-here |
| `00-Engine-Core-Runtime/Application-Root/game-application.md` §8 | BE-1 | revised-here |
| `00-Engine-Core-Runtime/Shared-Transform-Workbench/the-shared-transform-workbench.md` l.104 | BQ-16 | revised-here |
| `00-Engine-Core-Runtime/Startup-Data-Construction/generated-float-table-builders.md` §8 | BH-1 | revised-here |
| `01-Script-VM-Native-Bridge/verbs-that-only-wait-and-verbs-that-do-nothing.md` §2 | CR-1 | revised-here |
| `06-Movement-And-Navigation/Movement-Mode-Selection/setting-the-movement-mode-and-which-way-a-character-turns.md` | DP-1 | revised-here |
| `08-Combat-Formula/Recipe-System/ranged-weapon-recipes.md` status line | E-2, E-3 | revised-here |
| `08-Combat-Formula/Steal/the-steal-roll.md` evidence row and §2 | FK-4 | revised-here |
| `13-Rewards-Progression-Economy/CONTRACT-level-advance-and-growth.md` §14 | UQ-134, UQ-135 | revised-here |
| `13-Rewards-Progression-Economy/loot-drops-and-enemy-chain.md` "the tables are not read" | AE-1, AE-2, AE-3 | revised-here |
| `15-Input/Input-Stack/input-stack-device-channel-and-bindings.md` (three places) | AU-5, AV-6 | revised-here |
| `16-UI/Dynamic-Geometry-Instances/dyngeo-instance-family.md` (a dated 2026-09-14 narrowing) | BG-11 | revised-here (note appended; history kept) |
| `16-UI/Widget-Object-Model/the-widget-message-protocol.md` l.1337 | DL-1 | revised-here |
| `17-Presentation-Rendering/Model-And-Motion-Formats/README.md` (a dated 2026-09-13 entry) | MA-1 | revised-here (note appended; history kept) |
| `17-Presentation-Rendering/Render-Command-List/the-ordered-render-command-list.md` | GA-4 | revised-here |
| `19-Save-Load-Settings/Language-And-Locale/language-selection-and-locale-ids.md` (three places) | AV-8, AU-5 | revised-here |
| `20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md` | AB-3 | revised-here |
| `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md` | UQ-293 | revised-here |
| `23-Third-Party-Libraries/PostEffects-Yebis-PPFX/yebis-ppfx-source-map.md` §7 list | BQ-30 (BQ-29 stays open) | revised-here |
| `99-Unresolved-Residual/Largest-Unclassified-Code/the-largest-unclassified-functions.md` §8 | BI-2 (partly), BI-3, BI-4 | revised-here |
| `_index/OPEN-QUESTIONS.md` rows above | all | agrees (already ANSWERED) |

**Not corrected here, with the reason:**
- `04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md` l.254 and l.434 (FB-3): the file
  carries a peer's uncommitted overlay (`status: AUDITED -> DOCUMENTED`, `last_reviewed 2026-09-22`). FABLE does not
  write over it; the two edits are ready in `drift_batch_edit.py` for when the file is free.
- FE-6 on `the-battle-stats-record-field-map.md` l.197: a note dated eight days after the answer says it "stays open"
  with an argument about direct-state arms. It may be a deliberate reopening, so it is left for the page owner.
- `where-the-games-memory-comes-from.md` l.705 / l.1230 call `B-2/a` open while the register closed it on 2026-09-07.
  Flagged under B-2, not in this batch; next pass.
- HISTORY, OTHER-QUESTION and SUBSCOPE hits: dated passes, struck text, a different question on the line, or a residue
  the register itself leaves open (EX-3, AA-2).

**Regression:** the re-run of `page_open_drift.py` no longer reports any corrected line. The 24 LIVE rows are now gone
except FB-3, which was deferred (see above). The hits left for the same ids are the lines the classification put in
the other classes.
