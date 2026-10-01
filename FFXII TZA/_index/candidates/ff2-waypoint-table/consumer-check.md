# Affected-consumer check: FF-2 answered; the field map's "node pointer" and "reserved or padding" readings corrected (FABLE, Claude Opus 5.5, 2026-09-26)

**Control:** `ff2_waypoint_table.py` beside this file (4 checks, FAILS 0).

The battle-unit field map named `+0x290` a `ptr[] pathNodes` read as a node pointer. It also concluded that
`+0x298`–`+0x68F`, reached by no swept displacement, reads as reserved or padding. Both are wrong. The path builder
writes the navigation path record's `+0x90` table by index, and the waypoint reader uses each entry as
`{f32 x, f32 z}`. The table holds 128 entries, so it spans unit `+0x290`–`+0x68F`. The navigation-mesh page already
had the layout right.

| consumer | what it said | state |
|---|---|---|
| `04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md` §2.6.3 | "takes the node pointer from `+0x290 + index × 8`"; `+0x290` `ptr[] pathNodes` | revised-here (struck; `waypointXZ[region]` beside it) |
| same page §7 `FF-2` | "reads as reserved or padding rather than an embedded object"; the path state `+0x200`–`+0x297` | revised-here (struck; the answer and the corrected extent beneath) |
| same page §2.3 "What nobody reaches" | `+0x298`–`+0x68F` (1016 B) in the unreached list | revised-here (dated note: reached by index) |
| `06-Movement-And-Navigation/how-a-unit-finds-its-way-across-the-navigation-mesh.md` §3 | the path record at `unit + 0x200`, `0x490` bytes, `+0x90 xz[128]` | agrees (the answer cites it) |
| `06-Movement-And-Navigation/CONTRACT-corridor-query-family.md` §14 item 1 (the `0x610`-byte block copy of `unit+0x80`) | the copy's extent | agrees (it ends at `+0x690`, as the table does) |
| `_index/OPEN-QUESTIONS.md` FF-2 | OPEN; left `+0x298`–`+0x68F` | revised-here (ANSWERED; the previous status kept as history) |
