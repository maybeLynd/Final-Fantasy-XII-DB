# Audit-spec sweep record: FRONTIER AUDITED eligibility census

Reviewer: SWE2-AUDIT-SPEC - 2026-10-01
Board task: `FRONTIER-REQ-AUDITSPEC-AUDITED-PROMOTION-SWEEP`
Input: `Database/Tools/work/FABLE/audited_eligibility.tsv` (FRONTIER census: `audit.passes>=1`,
mechanical conditions 7+8) + a fresh `audit_crossrefs.py` regeneration at HEAD (446 findings across
519 documents; the census's Sep-29 crossref_audit.json was stale).

## Result

- **29 pages promoted** DOCUMENTED -> AUDITED, commit `058c93e21` (flip + `crossref_clean: true` +
  `reopened_count` + `promoted:` record in each audit block).
- **8 pages blocked** (blocking condition recorded below).
- **63 pages already AUDITED** - no action.
- One retained evidence preimage (`_experiments/evidence/.../retained/03-game-application.md`)
  excluded - never a promotion candidate.

## Per-page judgement applied

Cond 7 (falsification pass recorded naming the state): every promoted page carries a `## ...
Falsification` section whose body names the pass (opus-*/fable-*/swe2struct-* records) and
concrete killers that were searched. Cond 8: 0 unresolved findings in the freshly regenerated
crossref audit. Cond 9: every promoted page either carries a `Crossings into other layers` /
`Cross-subsystem neighbours` section with per-edge CLIENT/MECHANICAL/OUT-OF-SCOPE dispositions,
or (four pages, flagged below) covers its cross-boundary surface inline - the fresh audit finds
zero unaccounted neighbours for all four. Cond 10: each pass records attempted kills with
survives/REFUTED verdicts; refuted items are corrected in place or routed.

Reviewer rule: SWE2-AUDIT-SPEC is not the last substantive author of any promoted page (last
substantive commits are OPUS/FABLE/SWE2-DATA/SWE2-FRONTIER). Two pages' last commits are OPUS
carrying AUDIT-SPEC narrowing-wave corrections - the text is OPUS's; noted for transparency.

## Promoted (29)

- 00-Engine-Core-Runtime/Diagnostics-Logging/the-formatted-log-call-and-its-level-gate.md
- 02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/amap-menumap-area-table.md
- 02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/gmap-menumap-guide-texts.md
- 02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/menuquest-bin-quest-detail-tables.md
- 03-World-Area-Field/choosing-the-field-environment-variant.md
- 06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md
- 06-Movement-And-Navigation/Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md
- 06-Movement-And-Navigation/Movement-Mode-Selection/setting-the-movement-mode-and-which-way-a-character-turns.md
- 06-Movement-And-Navigation/clamping-a-point-into-a-volume.md
- 06-Movement-And-Navigation/how-a-unit-finds-its-way-across-the-navigation-mesh.md
- 07-Combat-Action/how-close-a-unit-must-stand-to-act.md
- 11-Party/active-party-reserve-and-the-moment-the-leader-changes.md
- 12-Items-Equipment-Shops-License/equipment-slots-and-the-single-stat-rebuild.md
- 15-Input/how-a-gamepad-becomes-a-controller-object.md
- 16-UI/Handbook/the-handbooks-monster-viewer.md
- 17-Presentation-Rendering/Model-And-Motion-Formats/frp-object-container.md
- 18-Audio/which-variation-of-a-sound-you-hear.md
- 19-Save-Load-Settings/Game-Settings-Config/the-settings-command-table.md
- 19-Save-Load-Settings/how-a-manual-save-is-committed.md
- 22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/how-a-class-registers-its-array-members-and-annotations.md
- 22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/the-file-schema-against-the-runtime-schema.md
- 23-Third-Party-Libraries/Bullet-Physics-Integration/phyre-to-bullet-rigid-body-materialization.md
- 23-Third-Party-Libraries/EASTL/eastl-strings-containers-and-the-logging-allocator.md
- 24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/the-msvc-ordered-container-runtime.md
- 24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/the-ordered-container-runtime.md
- 99-Unresolved-Residual/Glyph-Run-Rendering/the-shared-drawing-context.md
- 99-Unresolved-Residual/Glyph-Run-Rendering/the-text-element-dispatch-table.md
- 99-Unresolved-Residual/measuring-text-by-drawing-it-with-the-output-off.md
- 99-Unresolved-Residual/the-widget-tree-draw-pass.md

## Blocked (8) - condition recorded, task output requires it

- `00-Engine-Core-Runtime/Developer-Tuning-Console/the-event-slot-panel-and-its-dead-feeder.md` - status CORRECTED - correction landed but page must be re-DOCUMENTED before audit; falsification section exists but status ladder does not skip DOCUMENTED
- `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/chse-character-se-tables.md` - 6 fresh UNACCOUNTED NEIGHBOUR findings (ActorEntity 10, Gameplay 3, Movement 11, Party 2, Script_VM_Native_Bridge 1, WorldAreaField 2 edges) - 0 at the Sep-29 census input; layer edges drifted since
- `05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md` - status REOPENED - standard requires return through DOCUMENTED before AUDITED
- `06-Movement-And-Navigation/the-unit-shape-distance-primitives.md` - 5 fresh UNACCOUNTED NEIGHBOUR findings (Audio 2, Gameplay 2, Party 2, Script_VM_Native_Bridge 4, UI 13 edges) - 0 at census time; the pass-22 sweep on this page predates the drift
- `12-Items-Equipment-Shops-License/the-shop-table-and-its-stock-gates.md` - status PARTIAL - documentation incomplete; not eligible regardless of passes
- `16-UI/Widget-Object-Model/the-title-asset-singleton-and-its-distinct-consumer.md` - status PARTIAL
- `24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md` - status REOPENED
- `99-Unresolved-Residual/Largest-Unclassified-Code/the-largest-unclassified-functions.md` - status PARTIAL

## Caveat on input freshness

Two of the eight blocked pages had 0 findings in the census TSV but acquire findings in the
fresh audit - the census input was two days stale and layer edges drifted. The promoted set was
filtered against the **fresh** audit, not the stale census column. The two drifters need a
neighbour-disposition pass before they can re-enter eligibility.
