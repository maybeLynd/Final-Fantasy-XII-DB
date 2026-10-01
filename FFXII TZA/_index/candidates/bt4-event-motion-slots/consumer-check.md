# Affected-consumer check: BT-4 answered - the speed-rule indices are motion slots (FABLE, Claude Opus 5.5, 2026-09-27)

affected: 17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md (frontmatter status, section 6 modding notes, the BT-4 box)
run: bt4_event_slots.py at c07423604 (worktree = that HEAD plus this package), 5 image checks FAILS 0; with D:/FFXII_TZA_extract/ps2data/obj_finish/in as argument, 8 checks FAILS 0. C1 is the check that measures the slot-name table; P1 the posters.

| consumer | what it said | state |
|---|---|---|
| `17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md`, BT-4 box | "Still open: what each index is on screen. No name table for the event indices has been found." | revised-here: answered beneath, box ticked |
| same page, frontmatter `status` | "the subtype meanings (BT-4) are open" | revised-here |
| same page, section 6 "Mod compatibility" | "the subtype values ... are authored per object; changing an object's subtype changes which speed rule it gets, with no code change" | revised-here: struck. The engine posts the indices (and script verbs can); what is authored is the motion each container holds at that slot. Replacing an object's `revive` / `active` / `deact` / `c_turbo` block changes what plays under the rule, not the rule |
| `17-Presentation-Rendering/CONTRACT-coast-down-latch.md` line 231 | "The subtype at `+0x0CC` comes from authored data, but this operation only compares it." | routed to OPUS (the contract's author) in `FABLE-REQ-OPUS-COASTDOWN-SUBTYPE-SOURCE`: the value is a posted event index (engine posters and script verbs), which the contract's own claim does not depend on |
| `07-Combat-Action/Action-Definition-Row/the-action-definition-row.md`, the `+0x30` row | "an id-shaped word; reader not found" | pending: applied by FABLE's `bt4a` runner after UQ-107's publish, because that page carries FABLE's staged UQ-107 hunks and a publish takes a path's whole working-tree state. Its own record is `consumer-check-action-row.md` |
| `17-Presentation-Rendering/Character-Render-Records/render-event-selection-evidence.md`, UQ-195 (answered 2026-09-17) | the priority table is `0x60` bytes of values 0..4 | agrees; the name table indexes the same low 12 bits |
| `_index/OPEN-QUESTIONS.md` BT-4 | PARTIAL | revised-here: ANSWERED |

Regenerated with it: `event-slot-names.tsv` (new).
