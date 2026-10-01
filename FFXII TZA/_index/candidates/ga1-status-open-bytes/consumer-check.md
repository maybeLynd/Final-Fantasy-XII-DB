# Affected-consumer check: GA-1's 2026-09-18 `+0x0A` clause corrected (FABLE, Claude Opus 5.5, 2026-09-27)

affected: 10-Status-Periodic-Terminal/the-thirty-two-statuses.md (the GA-1 box)

run: ga1_open_bytes.py at bbd3af82a (worktree = that HEAD plus this package), 5 checks, FAILS 0; the `+0x0A` read is
the follower's `+0x0A w2 0031E288` line (G1's run prints it).

**The change.** The GA-1 register row's 2026-09-18 narrowing (FABLE) made two claims about `+0x0A`. Both are
corrected in the new status; the old text stays as history in the row.
- **"read as a word at `0031C81A` in `0031C5D0`".** That instruction reads a class-5 row (`02EBF100`). The status
  row's `+0x0A` word is read at `0031E288`.
- **"not a string-pool key … a per-status index in a second space".** The word is passed to `002F9860`, the text-id
  lookup (id / 1000 → group), at `0031E28C`. So it is used as a text id. The string it names was not resolved.

| consumer | what it says | state |
|---|---|---|
| register GA-1 row, 2026-09-18 clause | the two claims above | revised-here (the new status states the correction; the old text is history) |
| the thirty-two statuses page, GA-1 box | OPUS's 2026-09-15 byte reading; no `+0x0A` reader named | agrees; ticked with the answer at publish time |
| `08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md` `+0x0BC` row | `00387730` computes the default duration from `status_data +8` | agrees (cited as the `+0x08` answer) |
| `_index/candidates/ga1-status-order-keys/` (FABLE, 2026-09-26) | kinds 1..4 cached "for kinds 1-4" | agrees, sharpened: the cache is indexed by L, and L maps to record keys differently from `002D02C0`'s kind (kinds.md) |
| `04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md` (EC7) | `00273160` as a flag lookup, `00273BA0` as a link-table build | routed-to-FRONTIER: they are the overhead status-order read and the status order-table builder (kinds.md, last section) |
| `16-UI/Widget-Object-Model/the-widget-message-protocol.md` (EC7) | `00297FE0` "posts message `0x1E`" | routed-to-FRONTIER: `0x1E` is the cycler's period argument (kinds.md) |

Grep of `0031C81A`, "string-pool key", `0x2EE0`, `00273160`, `00273BA0` and `00297FE0` across the database, 2026-09-27.
