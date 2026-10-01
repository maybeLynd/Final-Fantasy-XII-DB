# GR-12 narrowed: where the battle menu offers and issues actions 0x9C / 0x9D, and what their rows hold (FABLE, Claude Opus 5.5, 2026-09-30)

Task `FABLE-GR19-GR12-0930`. GR-12 asks what battle actions `0x9C` and `0x9D` do. This pass reads the whole menu side
and the rows. The execution side stays open. Static only; [`gr12_facts.py`](gr12_facts.py)
([out](gr12_facts.out)) pins every instruction and row byte below, FAILS 0.

## What is read (FABLE)

1. **Two containers issue them.** `BattleMenu_ClassifySelectedEntryAndHandleImmediateCommands` (`0027C3D0`) switches on
   the container kind (`0027C40C` `add eax, -6`, 23 kinds, byte table `0027C6B8`, dword table `0027C6A0`). Only kind 11
   reaches `0027C584`, and only kind 24 reaches `0027C613`.
   - **Kind 11:** an entry whose own id is `0x9C` or `0x9D` (`0027C596`-`0027C5A8`, `id - 0x9C <= 1`) is issued at once
     as that action: `00311CD0(unit, unit, id, 0)` (`0027C5FE`), answer `0x17`, with no target step.
   - **Kind 24:** the entry's id is compared with `00273270`, the actor's stashed slot-0 item. An equal or `0xFFFF` entry
     issues `0x9D`, any other `0x9C` (`0027C625`-`0027C665`), answer `0x17`.
2. **Offered only with a stash.** The list body at `0027CF2A` keeps a `0x9C` / `0x9D` entry (`0027D131`-`0027D145`)
   only while `00273270` answers something other than `0xFFFF` (`0027D14D`-`0027D156`). That is, only while the actor
   carries a takeaway backup ([the equipment page](../../../12-Items-Equipment-Shops-License/equipment-slots-and-the-single-stat-rebuild.md)
   section 11).
3. **The rows are shells.** `0x9B`, `0x9C` and `0x9D` are the only action rows with category byte `+0x1E` = 13. Each has
   `+0x22` = `0xFFFF` (no magick / technick / item id) and `+0x1C` = 3, and `+0x34` names the *Reserve* placeholder.
   Every other byte of the 60 is zero except `+0x00`/`+0x01` (`1c`-`1e`, `10`), `+0x0C`/`+0x0D` (`10 02`), `+0x24`/`+0x25`
   (`ff ff`), `+0x2D` (`0x20`) and `+0x38`-`+0x3A` (`ff`). Row bytes are in the output. The control is that the same reader
   names row `0x95` "Dismount".
4. **Nothing else names them.** A linear sweep of `.text` ([`gr12_sweep.py`](gr12_sweep.py),
   [filtered out](gr12_sweep.out)) lists every operand `0x9B`-`0x9D`. It finds the four menu sites above, which is the
   positive control, plus the command-list builder `0031EB20`. That builder names only `0x9B`: it exempts `0x9B` and
   `0x113` (Dismiss) from `00317BC0` (`0031EFB3`, `0031EFBB`) and sets flag `0x20` on a `0x9B` entry (`0031F17F`). The
   sweep also finds no `cmp ..., 0xd` within three instructions after a byte read of `+0x1E`. The other filtered hits
   (displacements and constants, listed in the output) are not read here.

## What stays open (FABLE)

- What an issued `0x9C` / `0x9D` changes when it executes. The sweep finds no test of the ids outside the menu and no
  category-13 compare, and the rows are near-empty. So the effect, if any, is decided either by data the row names indirectly or by the issuing context.
  Reading `00311CD0`'s queue through to the unit's action start would settle it.
- Which screens containers of kind 11 and kind 24 are. The kind numbers are not tied to a named menu.

## Consumer check (FABLE)

affected: `Database/FFXII TZA/_index/OPEN-QUESTIONS.md`
affected: `Database/FFXII TZA/12-Items-Equipment-Shops-License/equipment-slots-and-the-single-stat-rebuild.md`

- consumer: GR-12 - revised-here (narrowed; stays OPEN).
- consumer: the equipment page's section 11.3 - revised-here (the narrowing note after "stays open as GR-12").
- consumer: the action-definition-row page's `+0x1E` row - agrees (13 is not among the values it tabulates as common,
  and nothing there contradicts three category-13 rows).

## Controls (FABLE)

run: gr12_facts.py at 3cae47364 (FAILS 0)
