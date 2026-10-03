# FABLE: homed rows moved to the hosts SWE2-AUDIT-SPEC named (batch 4)

*Draft record, FABLE, 2026-10-03. Not applied and not published. It repairs the ten REJECT reviews of FABLE homing
records in SWE2-AUDIT-SPEC commit `95d495604` (`auditspec-review-fable-home-*-1002`). Each review found the row's
sentence, site and anchors exact and rejected only the host. The package follows each review's **Repair:** block:
it moves a row unchanged to the page the review names, or drops it when another page already binds the body. It is
built on OPUS's template (`opus-fable-home-host-moves-1003`, published `39bcb329b`), and `move_rows.py` is that
script plus a `drops` step.*

## FABLE headline

| measure | count |
|---|---:|
| rows moved (`moves`) | **32** |
| rows dropped, already bound elsewhere (`drops`) | **2** (`0026B480`, `00379D40`) |
| rows deferred, not mechanically mappable (`deferred` in `moves.json`) | **3** (`004EB910`, `00361480`, `00314D60`) |
| rows the reviews accept, left in place | `004E7980` (boot-fixups), `0035A250` (equipment) |
| overlap with `opus-fable-home-host-moves-1003` | none (no fn appears in both) |
| target pages | 10 |
| source pages | 8 (4 sections withdrawn whole, 2 more by the drops) |
| `move_rows.py` verify on the real tree | `VERIFY 32 functions, 143 anchors, 10 target pages, 2 drops` / `FAILS 0` ([`move_rows.out`](move_rows.out)) |
| `--apply --root` on a clean `HEAD` worktree, run twice | first run: 100 `PATCHED` (32 x 3 + 2 x 2), `FAILS 0`; second run: 100 `ALREADY`, `FAILS 0` |

## FABLE: the rows

`from` and `to` are page paths below `FFXII TZA/`, with prefixes shortened (`00/` = `00-Engine-Core-Runtime/`, and so
on). `moves.json` has the full paths, the evidence quotes with line numbers, and the anchors.

| fn | from | to / drop | why (review) | review |
|---|---|---|---|---|
| `0036F510` | `11/active-party-reserve-and-the-moment-the-leader-changes.md` | `00/Battle-Frame/the-world-tick-and-the-field-frame.md` | "never treats the field-frame body as one of its functions"; target owns the `0022A770` subtree (L479) | [review](../auditspec-review-fable-home-active-party-reserve-and-the-moment-the-1002/REVIEW.md) |
| `0044D460`, `0044ED90`, `0044F930`, `00451140`, `00451890`, `00453CB0`, `004548F0`, `0045BF50`, `0045C920`, `0045D290`, `0045DCA0`, `0045E8C0` (12) | `00/CONTRACT-boot-fixups.md` | `17/Effect-File-Formats/effect-element-type-dispatch.md` | `002F3BC0` named only "on that layer"; target reads it as its "§2.1 birth-step dispatcher" (L53, L61) | [review](../auditspec-review-fable-home-contract-boot-fixups-1002/REVIEW.md) |
| `0035D070` | `00/CONTRACT-boot-fixups.md` | `00/CONTRACT-per-frame-update-gate.md` | "an outbound edge to a UI body"; target reads `003C6000` as the state-bit driver (L1670, L1672) | [review](../auditspec-review-fable-home-contract-boot-fixups-1002/REVIEW.md) |
| `004CF230` | `00/CONTRACT-boot-fixups.md` | `17/Legacy-PS2-GS/the-vif1-vu1-layer.md` | "No boot code calls either caller"; target names `004C8320` among its microprograms (L412, L513) | [review](../auditspec-review-fable-home-contract-boot-fixups-1002/REVIEW.md) |
| `00272400`, `0027C220` | `12/equipment-slots-and-the-single-stat-rebuild.md` | `16/Widget-Object-Model/CONTRACT-widget-object.md` | "Neither touches equipment slots or the stat rebuild"; target reads `0027D740`'s interior (L633, L1198, L1202) | [review](../auditspec-review-fable-home-equipment-slots-and-the-single-stat-reb-1002/REVIEW.md) |
| `001941F0`, `00194490` | `15/Binding-Profiles/keymap-ini-file-format-and-default-controls.md` | `00/Application-Root/game-application.md` | "Not a keymap responsibility"; target reads `00189CE0` as the renderer update (L530, L2282) | [review](../auditspec-review-fable-home-keymap-ini-file-format-and-default-cont-1002/REVIEW.md) |
| `00285FE0` | `15/Binding-Profiles/keymap-ini-file-format-and-default-controls.md` | `99/Glyph-Run-Rendering/the-shared-drawing-context.md` | "not a keymap fact"; target reads `002B5C90` as its body (L192, L613) | [review](../auditspec-review-fable-home-keymap-ini-file-format-and-default-cont-1002/REVIEW.md) |
| `00314820` | `15/Binding-Profiles/keymap-ini-file-format-and-default-controls.md` | `00/Battle-Frame/the-world-tick-and-the-field-frame.md` | "disclaims exactly the kind of edge it is"; target reads `00377520` as the `0022A770` gate (L2579) | [review](../auditspec-review-fable-home-keymap-ini-file-format-and-default-cont-1002/REVIEW.md) |
| `0026AB60`, `0026BB00`, `0026BDD0`, `0026BFF0`, `003DF790` | `07/Command-And-Action-Seam/native-command-seam.md` | `04/Actor-Storage-Record/the-record-behind-every-actor.md` | "This page never reads" `fieldsign`; target reads `00355A00` (L1016, L1087) | [review](../auditspec-review-fable-home-native-command-seam-1002/REVIEW.md) |
| `0026B480` | `07/Command-And-Action-Seam/native-command-seam.md` | **drop**: bound on `04/Actor-Storage-Record/the-record-behind-every-actor.md` L1013 | "the row's premise is false ... already bound there" | [review](../auditspec-review-fable-home-native-command-seam-1002/REVIEW.md) |
| `00379D40` | `01/Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md` | **drop**: bound on `02/the-resource-request-queue.md` L875 (its `00379D40` exclusive-subtree section) | "Do not re-home it ... already binds it" | [review](../auditspec-review-fable-home-scriptvm-verb-dispatch-and-parameter-en-1002/REVIEW.md) |
| `00310D30` | `07/the-moment-an-action-is-committed.md` | `06/Battle-Locomotion/battle-locomotion-steering-and-recovery.md` | "not this page's subject"; target reads `00310920` as the facing-publish record loop (L880) | [review](../auditspec-review-fable-home-the-moment-an-action-is-committed-1002/REVIEW.md) |
| `00231F20`, `0033CBF0`, `003EC5B0`, `003EC720`, `003EC770` | `13/world-loot-pickups-the-ten-slot-pool-and-the-despawn.md` | `14/persistent-flag-banks.md` | "the page itself says the caller is **not** one of its functions"; target reads `002FB560` as trap-marker placement (L752) | [review](../auditspec-review-fable-home-world-loot-pickups-the-ten-slot-pool-an-1002/REVIEW.md) |
| `004EB910` | `00/CONTRACT-boot-fixups.md` | **deferred** | page at HEAD still has the false "1.0 (`01E0283C`)" clause (correction is `fable-corr-004eb910-1003`, not yet on HEAD), and the VIF1 page does not cite `004EBE80` ("Otherwise park it") | [review](../auditspec-review-fable-home-contract-boot-fixups-1002/REVIEW.md) |
| `00361480` | `15/CONTRACT-input-subsystem.md` | **deferred** | "the row cannot be caller-hosted": `18/Audio-Boundary/how-a-sound-request-becomes-a-voice.md` does not cite `00342770` | [review](../auditspec-review-fable-home-contract-input-subsystem-1002/REVIEW.md) |
| `00314D60` | `19/Game-Settings-Config/ff12config-and-debglobal.md` | **deferred** | "No page reads `0050C8A0` as its own"; `01/verbs-that-only-wait-and-verbs-that-do-nothing.md` does not cite it | [review](../auditspec-review-fable-home-ff12config-and-debglobal-1002/REVIEW.md) |

*Line numbers are from the shared tree at 765ec764d. `move_rows.py` checks each quote by text, not by line.*

## FABLE: target pages, state and lead

The lead is the identity with the most commits on the page, counted from commit-subject prefixes
(`git log --format=%s`; `SWE2-EC7-NN` counted as `SWE2-EC7`; unprefixed subjects not counted). State is
`git status --short` in the shared tree at 765ec764d.

| target page | rows | lead | state |
|---|---:|---|---|
| `00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md` | 2 | **SWE2-EC7** (84) | **` M`, content** (+7 / -3: an uncommitted "Corrected 2026-09-26, FABLE" edit on bit 7 -> bit 0). **Hold.** |
| `17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md` | 12 | **SWE2-EC7** (68) | clean |
| `00-Engine-Core-Runtime/CONTRACT-per-frame-update-gate.md` | 1 | **SWE2-EC7** (45) | **` M`, EOL-only** (CRLF in the worktree, LF at HEAD, bytes equal without CR). **Hold.** |
| `17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md` | 1 | FABLE (19) | **` M`, EOL-only** (as above). **Hold.** |
| `16-UI/Widget-Object-Model/CONTRACT-widget-object.md` | 2 | **SWE2-EC7** (18), OPUS 14 | clean |
| `00-Engine-Core-Runtime/Application-Root/game-application.md` | 2 | **SWE2-EC7** (84) | clean |
| `99-Unresolved-Residual/Glyph-Run-Rendering/the-shared-drawing-context.md` | 1 | FABLE (11) | clean |
| `04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md` | 5 | OPUS (7), FABLE 5 | clean |
| `06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md` | 1 | OPUS (3) | clean |
| `14-Story-Event-Quest-Hunt/persistent-flag-banks.md` | 5 | FABLE (12) | clean |

Seven of the eight source pages are clean. `00-Engine-Core-Runtime/CONTRACT-boot-fixups.md` (lead FABLE 9 /
SWE2-EC7 9) went **` M`** at 02:15 during this build: +1 / -1, the `004EB910` row only, which is the
`fable-corr-004eb910-1003` correction applied but not committed. None of this package's 14 boot-fixups rows touches
that line, and `move_rows.py` re-verified with `FAILS 0` after it. `004EB910` stays deferred: HEAD still has the old
clause, and the VIF1 page still does not cite `004EBE80`. When it is moved later, take the row from the current page
(the struck-through form), not from `rows.json`.

**Second "re-homed here" section on three pages.** `effect-element-type-dispatch.md` and `game-application.md`
already carry the OPUS-drafted section `(FABLE, 2026-10-03; move drafted by OPUS)` from `39bcb329b`. The OPUS
package's `003EBD70` move to `the-world-tick-and-the-field-frame.md` is still unpublished, held for the same dirty
page. This package writes its own heading `(FABLE, 2026-10-03; AUDIT-SPEC batch 4)`, so those three pages end with
two adjacent sections. The headings differ after `2026-10-03;`, so neither script matches the other's section.
Merging them is a manual edit if wanted.

**Run without the held pages** (28 moves and both drops):

```
--only 0044D460,0044ED90,0044F930,00451140,00451890,00453CB0,004548F0,0045BF50,0045C920,0045D290,0045DCA0,0045E8C0,00272400,0027C220,001941F0,00194490,00285FE0,0026AB60,0026BB00,0026BDD0,0026BFF0,003DF790,00310D30,00231F20,0033CBF0,003EC5B0,003EC720,003EC770,0026B480,00379D40
```

The four held rows are `0036F510` and `00314820` (world-tick), `0035D070` (per-frame gate) and `004CF230` (VIF1).
One caveat: with `0036F510` held, `active-party-reserve...md` keeps its section until it runs. With `00314820` held,
the keymap section keeps one row.

## FABLE: source side

- **Sections withdrawn whole** (the `--apply` run printed `(section withdrawn)`):
  - `11-Party/active-party-reserve-and-the-moment-the-leader-changes.md`;
  - `15-Input/Binding-Profiles/keymap-ini-file-format-and-default-controls.md`;
  - `07-Combat-Action/the-moment-an-action-is-committed.md`;
  - `13-Rewards-Progression-Economy/world-loot-pickups-the-ten-slot-pool-and-the-despawn.md` (the OPUS section that
    follows it is kept);
  - `07-Combat-Action/Command-And-Action-Seam/native-command-seam.md` (the last row removed is the drop `0026B480`);
  - `01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md` (by the drop).
- **Sections kept:**
  - `CONTRACT-boot-fixups.md` keeps `004E7980` (accepted) and `004EB910` (deferred);
  - `equipment-slots-and-the-single-stat-rebuild.md` keeps `0035A250` (accepted);
  - `CONTRACT-input-subsystem.md` and `ff12config-and-debglobal.md` are not touched (their only rows are deferred).
- **Records.** A moved row goes to rows.json `moved`, with `moved_by: FABLE` and `moved_record` naming this folder.
  A dropped row goes to a new `dropped` list, with `already_bound_on`. The file is written `indent=1`, ASCII, with no
  trailing newline; a re-dump of each current record reproduces it byte for byte.
- **Hazard after apply.** Six records are left with no rows: `active-party`, `keymap`, `native-command-seam`,
  `scriptvm-verb-dispatch`, `the-moment-an-action-is-committed` and `world-loot`. Their `homing_applier.py --apply`
  would re-add an empty FABLE section, so mark them withdrawn.

## FABLE: notes

- **No text edits.** `0027C220` says "bit 1 (mask 2)" and "bit 0 (mask 1)", which gives both the index and the
  value. OPUS's package rewrote two such texts as values only; this one is left as homed, as its review says
  "unchanged".
- **Deferred rows stay on their source page**, although their reviews call them host-fit defects. Each needs a page
  edit first: `004EB910` needs the correction on HEAD and a cite of `004EBE80` on the VIF1 page. `00361480` and
  `00314D60` need their target page to cite the caller, or need a non-caller homing stream.

## Consumer check (FABLE)

affected: Database/FFXII TZA/00-Engine-Core-Runtime/CONTRACT-boot-fixups.md
affected: Database/FFXII TZA/12-Items-Equipment-Shops-License/equipment-slots-and-the-single-stat-rebuild.md
affected: Database/FFXII TZA/15-Input/Binding-Profiles/keymap-ini-file-format-and-default-controls.md
affected: Database/FFXII TZA/07-Combat-Action/Command-And-Action-Seam/native-command-seam.md
affected: Database/FFXII TZA/01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md
affected: Database/FFXII TZA/07-Combat-Action/the-moment-an-action-is-committed.md
affected: Database/FFXII TZA/13-Rewards-Progression-Economy/world-loot-pickups-the-ten-slot-pool-and-the-despawn.md
affected: Database/FFXII TZA/17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md
affected: Database/FFXII TZA/16-UI/Widget-Object-Model/CONTRACT-widget-object.md
affected: Database/FFXII TZA/00-Engine-Core-Runtime/Application-Root/game-application.md
affected: Database/FFXII TZA/99-Unresolved-Residual/Glyph-Run-Rendering/the-shared-drawing-context.md
affected: Database/FFXII TZA/04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md
affected: Database/FFXII TZA/06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md
affected: Database/FFXII TZA/14-Story-Event-Quest-Hunt/persistent-flag-banks.md

run: move_rows.py at 765ec764d (verify-only on the shared tree: VERIFY 32 functions, 143 anchors, 10 target pages, 2 drops / FAILS 0; `--apply --root` on a detached 765ec764d worktree: 100 PATCHED then 100 ALREADY, FAILS 0 both runs)

`git -C C:/w71 diff --stat` after the two `--apply` runs: 26 files changed, 484 insertions(+), 277 deletions(-).
The files are the 18 pages above and 8 source `rows.json` records. `CONTRACT-input-subsystem.md`,
`ff12config-and-debglobal.md` and their records are not among them.

Held or deferred in this publish (FABLE), so not touched by it and not declared above; each goes in its own later publish with its own consumer check:

- `Database/FFXII TZA/11-Party/active-party-reserve-and-the-moment-the-leader-changes.md`
- `Database/FFXII TZA/00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md`
- `Database/FFXII TZA/00-Engine-Core-Runtime/CONTRACT-per-frame-update-gate.md`
- `Database/FFXII TZA/17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md`

## FABLE: files

| file | what |
|---|---|
| `moves.json` | 32 `moves`, 2 `drops` (with `already_bound_on` page, line and quote), 3 `deferred` (with why) |
| `build_moves.py` | rebuilds `moves.json` from the source records (texts copied, not retyped) |
| `move_rows.py` | OPUS's script plus `drops`; verify-only by default; `--apply`, `--root`, `--only` |
| `move_rows.out` | the verify-only run on the shared tree at 765ec764d |
