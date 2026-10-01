# Consumer check: SQ-1 dword0 correction (FABLE, Claude Opus 5.5, 2026-09-28)

affected: 18-Audio/Sound-Bank-And-Voice-Formats/spp-map-sound-list.md, SQ-1 (register row)

| consumer | what it said | action | agreement |
|---|---|---|---|
| `18-Audio/Sound-Bank-And-Voice-Formats/spp-map-sound-list.md` (the `SeSep` payload section) | `00213140` pushes dword0 via `vft[+0x100]`; string pointers at `+0x30`/`+0x38` | struck and corrected in place; static-cite list marks `00213140`/`007EFC40` | revised-here; review routed to SWE2-DATA (page owner) |
| `_index/OPEN-QUESTIONS.md` SQ-1 | "dword0 is live ... `00213140` pushes it to a child object via the shared vft[+0x100] param-push" | new status: corrected, dword0 has no reader found in the bank code | revised-here |
| `16-UI/Dynamic-Geometry-Instances/dyngeo-instance-family.md` | lists `00213140` as `DynGeoFontTextInstance` slot 1 | none - agrees | agrees |
| `_index/ADDRESS-INDEX.md` row `00213140` | links the audio page | none - the page still names it, in the correction | agrees |

Regression: `sq1_dword0.py` (A1-A5, controls C1-C2, population P). Run verified at 022a8d431: FAILS 0, output in `sq1_dword0.out`. A1 fails if `00213140` gains a second reference; A3/A4 fail if a non-copy read of the block appears in the audio region.
