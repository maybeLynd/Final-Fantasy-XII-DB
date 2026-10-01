# Affected-consumer check, fourth pass — pages behind today's register closures (FABLE, Claude Opus 5.5, 2026-09-26)

`page_open_drift.py` was rerun at HEAD `e81346e7d` (152 hits) and filtered to ids the register closed or restated today.
Each hit was read in context. A dated falsification sentence, a box already ticked with its narrowing, or a line the
same page answers further down is history and stays. The lines below stated a current status that the register no longer
holds. Each one gets a dated status note beside it. Nothing is struck and no sentence is rewritten, except two
frontmatter `status:` fields, which are current-state fields by design.

| consumer | stale statement | register now | state |
|---|---|---|---|
| `14-Story-Event-Quest-Hunt/event-memory-at-actor-bind.md` §5 | `AA-2` and the `+0x1394` gap "remain open" | `AA-2` ANSWERED (filed as `UQ-138`); `AA-5` ANSWERED (SWE2-CONTRACT, 2026-09-21) | revised-here (dated note) |
| `14-Story-Event-Quest-Hunt/persistent-flag-banks.md` payload table, "the tail" row | "meaning open (`AA-8`)" | `AA-8` ANSWERED `631161918` | revised-here (dated note in the cell) |
| `24-Compiler-And-CRT-Runtime/Generated-Families/generated-function-families.md` frontmatter | lists `UQ-319` among the open items | `UQ-319` ANSWERED `89b9edce6` | revised-here (status field; `UQ-317` / `UQ-318` still open, and the page's boxes already agree) |
| `99-Unresolved-Residual/Largest-Unclassified-Code/the-largest-unclassified-functions.md` frontmatter | `BI-3b` and `BI-3c` "not established" | both ANSWERED (restated 2026-09-26); the page's only open `BI-` row is `BI-11` | revised-here (status field names `BI-11`) |
| same page, the typed-slot-table section | "`BI-8` stays open with a defined shape" | `BI-8` ANSWERED 2026-09-14, on this same page further down | revised-here (pointer note; the answer was already on the page) |
| `22-Middleware-PhyreEngine/README.md` | "Highest-leverage task … Tracked as open question `B-3`" | `B-3` ANSWERED (class set applied 2026-09-02); the remaining placement is `AQ-2`, and the folded bodies are `BA-1` | revised-here (dated note) |
| `22-Middleware-PhyreEngine/Subsystem-Map/phyre-subsystem-map.md` `AQ-2` box | "(open question `B-3`)" | `B-3` ANSWERED; `AQ-2` PARTIAL, and the box stays unticked | revised-here (dated note) |
| `05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md` §17 | "the config-page/PC-2 consumer review remains open" | OPUS adjudicated the review 2026-09-13 in the config page §6 with the narrower wording; `PC-2` ANSWERED at that scope | revised-here (dated note; the conditional form on the spawn page is unchanged) |
| `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/CONTRACT-phyre-class-descriptor.md` evidence row and "Not claimed" | `PCD-1`…`PCD-4` "not established" / "stay open" | `PCD-2`, `PCD-3`, `PCD-4` ANSWERED; `PCD-1` SUPERSEDED, with its `+0xB0` residue carried by `BL-8` | revised-here (dated notes; §13's no-execution statement stands) |
| `19-Save-Load-Settings/Game-Settings-Config/ff12config-and-debglobal.md` §6 | — | carries OPUS's 2026-09-13 adjudication | agrees |
| `_index/OPEN-QUESTIONS.md` rows named above | — | — | agrees (no row edited in this pass) |

**Left as history after reading:**
- `persistent-flag-banks.md` "AA-2 stays OPEN", from an older falsification pass;
- `gambit-evaluation-and-enmity.md` `Z-3` on the unit;
- the input-stack page's `AP-6` "contents still open", inside a ticked box with narrowings;
- the verb-population page's `DO-1`, inside a "Not claimed" note;
- `vtable-method-index.md`;
- the dated `UQ-156` "still open" lines on the map-screens page;
- the evidence READMEs under `_experiments/evidence/` (dated review records).

**Regression.** `page_open_drift.py` now treats a line as history when a `*Status YYYY-MM-DD` note carrying an answer word
sits within two lines of it. Before the notes, the rerun listed every consumer above. After them, the total is 141 (it
was 144 with the one-line window). Two contract lines remain listed, both read and kept:
- line 543, the evidence row. Its dated answer notes sit on the row's continuation line, inside the same table cell, and
  are not in the `*Status` form the scanner recognises.
- line 590, "`PCD-5` was read 2026-09-14 — open item 5". This is correct as written.

The other remaining hits are the history lines above, plus older-pass material outside this batch.
