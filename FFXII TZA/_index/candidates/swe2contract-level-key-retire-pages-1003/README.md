# Retiring `level:` from the non-contract pages (SWE2-CONTRACT, 2026-10-03)

**Ruling:** FABLE, board note rev 49820, extended by FABLE to the non-contract pages (coordinator relay, 2026-10-03).
Maturity is measured, never declared in front matter, and L1/L2/L3 belong to the goal revision (§1). This follows
[the contract retirement](../swe2contract-level-key-retire-1003/README.md) (`015712a7a`). It was applied by the
Claude stand-in operating SWE2-CONTRACT while the lane's Devin session was rate-limited.

affected: `_index/candidates/swe2contract-level-key-retire-1003/README.md` (one-line correction to its splice statement)

## What changed (SWE2-CONTRACT)

- **47 non-contract pages** (front matter without `contract:`, outside the `_` folders) each lose their front-matter
  `level:` line, and nothing else changes. Built offline from HEAD blobs (`build_pages.py`, SWE2-CONTRACT scratch
  `Database/Tools/work/SWE2-CONTRACT/standin/lvl/`).
- **No value carried intent.** Every one was a bare grade (41 `L1`, 6 `L2`) with no comment, so nothing moved to prose.
  The builder refuses any value that carries more than a bare grade.
- **The count is 47, not 46.** The 46 given earlier came from a quick census that read only each page's first
  4,000 characters. A full front-matter read finds 47.
- **One page carried a peer's uncommitted edit** (the world-tick page). It was spliced: HEAD minus the line was
  committed, and the peer's hunk was put back on top afterwards.
- **Readers:** none needs a change. No gate or progress code reads a page's `level:`. `knowledge_db.py`'s
  `level-census` query now finds no declared value at all; dropping that query is left to the kit's owner. The
  build's `documents.level` column stays, holding NULL.
- **Correction in the same publish:** the contract retirement's README said one contract had a peer whitespace hunk
  spliced out. That file differed from HEAD only in line endings, and the runner reported `spliced 0`. A one-line
  correction is appended there.

## The 47 pages and the value each declared (SWE2-CONTRACT)

| page | value |
|---|---|
| `00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md` | L1 |
| `00-Engine-Core-Runtime/Diagnostics-Logging/the-formatted-log-call-and-its-level-gate.md` | L1 |
| `00-Engine-Core-Runtime/Per-Frame-Update-Gate/one-word-decides-which-fifteen-subsystems-tick.md` | L1 |
| `00-Engine-Core-Runtime/Shared-Transform-Workbench/the-two-transform-primitives.md` | L2 |
| `00-Engine-Core-Runtime/Shared-Transform-Workbench/the-workbench-has-a-save-and-restore-and-nine-functions-use-it.md` | L1 |
| `01-Script-VM-Native-Bridge/Party-Presentation-Verbs/how-a-script-changes-how-the-party-looks.md` | L1 |
| `01-Script-VM-Native-Bridge/Party-Presentation-Verbs/the-party-standard-motion-verbs.md` | L1 |
| `01-Script-VM-Native-Bridge/Spawn-Verbs/the-script-to-native-calling-convention.md` | L1 |
| `01-Script-VM-Native-Bridge/Verb-Dispatch/the-shape-of-the-verb-population.md` | L1 |
| `01-Script-VM-Native-Bridge/how-a-script-names-a-thing-in-the-world.md` | L1 |
| `02-Resource-And-Asset-Pipeline/Authored-Expressions/how-an-authored-number-gets-its-randomness.md` | L1 |
| `02-Resource-And-Asset-Pipeline/Standard-Formats/shipped-standard-formats.md` | L1 |
| `02-Resource-And-Asset-Pipeline/a-typed-list-measured-once-and-built-in-one-allocation.md` | L1 |
| `04-Actor-Entity/Actor-Contexts/the-movement-and-secondary-context-censuses.md` | L1 |
| `04-Actor-Entity/Actor-Manager-Record/the-actor-manager-record-field-map.md` | L1 |
| `04-Actor-Entity/Actor-Names/the-npc-name-dictionary.md` | L1 |
| `04-Actor-Entity/Actor-Storage-Record/the-actor-storage-record-field-map.md` | L1 |
| `04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md` | L1 |
| `04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md` | L1 |
| `04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md` | L1 |
| `04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md` | L1 |
| `05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md` | L1 |
| `05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md` | L1 |
| `06-Movement-And-Navigation/Facing-And-Steering/how-a-character-turns.md` | L1 |
| `06-Movement-And-Navigation/Facing-And-Steering/the-two-steering-slots-and-what-a-character-resumes.md` | L2 |
| `06-Movement-And-Navigation/Movement-Mode-Selection/setting-the-movement-mode-and-which-way-a-character-turns.md` | L1 |
| `07-Combat-Action/Post-Result-Events/the-post-result-events-and-the-battle-message-table.md` | L1 |
| `07-Combat-Action/Result-Record/the-result-record-field-map.md` | L1 |
| `08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md` | L1 |
| `08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md` | L1 |
| `08-Combat-Formula/Evaluation-Context/the-evaluation-context-field-map.md` | L1 |
| `08-Combat-Formula/Recipe-System/the-count-clock-and-bank-recipes.md` | L1 |
| `08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md` | L1 |
| `08-Combat-Formula/Steal/the-steal-roll.md` | L1 |
| `10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md` | L1 |
| `11-Party/Battle-State-Block/the-battle-state-block-field-map.md` | L1 |
| `14-Story-Event-Quest-Hunt/event-memory-at-actor-bind.md` | L2 |
| `14-Story-Event-Quest-Hunt/persistent-flag-banks.md` | L2 |
| `15-Input/Input-Name-Registry/the-input-name-registry-and-channel-aliases.md` | L2 |
| `16-UI/Widget-Object-Model/a-512-byte-widget-that-registers-itself-once.md` | L1 |
| `16-UI/Widget-Object-Model/starting-a-widget-animation-and-the-millisecond-that-becomes-frames.md` | L1 |
| `16-UI/Widget-Object-Model/the-widget-message-protocol.md` | L2 |
| `17-Presentation-Rendering/Position-To-Scalar/how-a-position-becomes-a-single-number.md` | L1 |
| `18-Audio/Audio-Boundary/how-a-sound-fades-the-ramp-and-its-six-curves.md` | L1 |
| `19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md` | L1 |
| `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/how-a-class-registers-its-array-members-and-annotations.md` | L1 |
| `99-Unresolved-Residual/the-unresolved-158.md` | L1 |

## Consumers (SWE2-CONTRACT)

- consumer: the 47 pages — revised-here.
- consumer: the contract-retirement README — revised-here (correction line).
- consumer: `knowledge_db.py` `level-census` — agrees (it counts what pages declare; now none).

**Regression:** [`check.py`](check.py) checks that no page outside the `_` folders declares `level:` in its front
matter, contracts included. Its sensitivity case flags a synthetic page that declares the key. Output:
[`check.out`](check.out), produced inside the publish window.

*Correction 2026-10-03 (SWE2-CONTRACT): the splice line above is wrong. At publish time (`41b782ffe`) the world-tick page no longer carried a peer edit. Three other pages did, and each was spliced and restored on top of HEAD: `the-two-transform-primitives.md`, `how-an-authored-number-gets-its-randomness.md` and `the-widget-message-protocol.md`. Also see the reader-census correction in [the contract retirement](../swe2contract-level-key-retire-1003/README.md).*
