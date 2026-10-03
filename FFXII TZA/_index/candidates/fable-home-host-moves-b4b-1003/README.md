# Batch-4 host-fit repairs, part 2: the four held rows (FABLE, 2026-10-03)

*FABLE. These are the four rows that [`fable-home-host-moves-b4-1003`](../fable-home-host-moves-b4-1003/README.md)
held when it published at `fe0f671b7`, because their target pages were dirty then. The moves use that record's
`move_rows.py` and `moves.json`, run with `--only`.*

## FABLE: why they can go now

- **`the-world-tick-and-the-field-frame.md`** is clean at HEAD. SWE2-CONTRACT's restoration landed at `18ebb00d9`, and
  the `003EBD70` move at `c76e449dc`.
- **`CONTRACT-per-frame-update-gate.md` and `the-vif1-vu1-layer.md`** differ from HEAD only in line endings
  (`git diff --numstat` is empty). `move_rows.py` keeps each file's line endings.

## FABLE: the moves

| fn | from | to | review |
|---|---|---|---|
| `0036F510` | `11/active-party-reserve-and-the-moment-the-leader-changes.md` | `00/Battle-Frame/the-world-tick-and-the-field-frame.md` | [review](../auditspec-review-fable-home-active-party-reserve-and-the-moment-the-1002/REVIEW.md) |
| `00314820` | `15/Binding-Profiles/keymap-ini-file-format-and-default-controls.md` | `00/Battle-Frame/the-world-tick-and-the-field-frame.md` | [review](../auditspec-review-fable-home-keymap-ini-file-format-and-default-cont-1002/REVIEW.md) |
| `0035D070` | `00/CONTRACT-boot-fixups.md` | `00/CONTRACT-per-frame-update-gate.md` | [review](../auditspec-review-fable-home-contract-boot-fixups-1002/REVIEW.md) |
| `004CF230` | `00/CONTRACT-boot-fixups.md` | `17/Legacy-PS2-GS/the-vif1-vu1-layer.md` | [review](../auditspec-review-fable-home-contract-boot-fixups-1002/REVIEW.md) |

Each row moves unchanged. Two source sections lose their last row and are withdrawn by `move_rows.py`:
`0036F510` on the active-party page and `00314820` on the keymap page.

**Still deferred** (no host cites the caller yet, as the b4 record says): `004EB910`, `00361480`, `00314D60`.

## Consumer check (FABLE)

affected: `Database/FFXII TZA/11-Party/active-party-reserve-and-the-moment-the-leader-changes.md`
affected: `Database/FFXII TZA/15-Input/Binding-Profiles/keymap-ini-file-format-and-default-controls.md`
affected: `Database/FFXII TZA/00-Engine-Core-Runtime/CONTRACT-boot-fixups.md`
affected: `Database/FFXII TZA/00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md`
affected: `Database/FFXII TZA/00-Engine-Core-Runtime/CONTRACT-per-frame-update-gate.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md`

- consumer: each source page's FABLE homed section: revised-here (row removed; section withdrawn where it was the last).
- consumer: each target page's re-homed section: revised-here (row added, unchanged text).
- consumer: the three source records' `rows.json`: revised-here (rows marked moved).
- consumer: the b4 record's "held" list: agrees; this record completes it.

run: move_rows.py at a3d7433c2 (`--only 0036F510,00314820,0035D070,004CF230`, verify: VERIFY 4 functions, 10 anchors, 3 target pages, 0 drops / FAILS 0)
