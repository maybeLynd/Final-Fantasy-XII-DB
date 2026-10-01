# UQ-68: battle window kind 5 is the Foecraft command's list, and no shipped command list opens it (FABLE, Claude Opus 5.5, 2026-09-27)

**Question (UQ-68):** "`bwin`: what entry 4 is, and what the two numbers measure."

The two numbers were read on 2026-09-18: the window's authored minimum width and its row count. Entry 4 is the
kind-5 battle window, the only entry authored `(150, 8)`; every other entry is `(10, 8)`. The open part was which
window kind 5 is.

**Answer.** Kind 5 is the list window of battle command **7, Foecraft** (class-21 row 7 on
[the encoded-id page](../../../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md)). The menu code
that would open it is complete. **No command list the PC build ships offers command 7**, so the 150-wide window is
not reachable through the battle menu (static; limits below).

## The chain (`uq68_kind5.py`, 9 checks, FAILS 0; output `uq68_kind5.out`)

1. **Kind → list (W1, W2).**
   - The window-kind switch `0027E050` indexes its 20-dword table `0027E384` by **kind − 1** (`0027E06B`), so it covers
     kinds 1–20.
   - Kind 5 stores list code `0xB` at `+0x4C0` and sub-selector **7** at `+0x4D4`.
   - List code `0xB`'s arm of `BattleMenu_BuildCommandEntryList` `0031EB20` (`0031ED58`) validates that sub-selector as
     a class-`0x15` (21) encoded id (`0031ED5E`–`0031ED73`), that is, a battle command.
2. **Command → kind (W3).**
   - In the command lists (codes 6 and 9), the next-kind function `0027C3D0` switches on a row's command word `+0x50`
     through the table `0027C6D0`.
   - Command 7 lands on `0027C532`, which returns 5. No other command reaches that arm.
3. **The two tables agree (W4).** Commands 3, 5, 6 and 7 (Items, Summon, Quickening, Foecraft) open kinds 4, 6, 7
   and 5. Those are exactly the kinds whose sub-selector is the same command.
4. **Into the window's kind word (W5).** The dispatch `002778C0`:
   - takes the kind from `0027C3D0` (`00278423`);
   - pushes the current kind onto the navigation stack at `[+0x2FE8] + 0x70` (`00278542`–`0027854A`) and raises its
     depth `+0x68` (`002785C8`);
   - for an ordinary kind, calls its own procedure with **message 31** and the kind as payload
     (`00278870`–`00278895`).

   Its message-31 arm `00279187` holds the only word store to `+0xD8` (`002791AC`). That is the word `0027DED0` sizes
   the window from.
5. **Nothing else produces 5 (W6).**
   - The controller's message-33 senders pass 1 (`0027AA70`, constant `00915BB0`) or `0027C730`'s result, which is
     one of `0x10`–`0x13`.
   - The back path (`0027881F`) only restores a kind the stack saved.
6. **bwin (W7).** `0027BDE0` maps kind 5 to entry 4 (table `0027BE88`). The `us` file's entry 4 is `(150, 8)`.
7. **The lists (W9).** The command lists `0027C3D0` reads are built by `0031EB20`'s codes 6–9 arm from static
   `{flag, command}` byte tables. That arm's only row-id store is `0031ED35`.
   - Code 6, the top list (`00D10650` / `00D10660`, picked by `[02EBF190]+4` bit `0x800`): Attack, Magicks &
     Technicks, Mist, Dismiss, Gambits, Items.
   - Code 9, the Mist list (`00D1065C`): Summon, Quickening.

   The other six image-wide writers of a row's command word are other list codes' arms.

## What this corrects

- **UQ-68's 2026-09-26 narrowing (FABLE's own)** said the window kind is the payload of the command widget's
  message 1, which the controller fills from `+0x61BA`, set by the controller's message 34. That is wrong.
  - Its control `uq68-kind-source/uq68_kind_source.py` K1 checks the right store, `002791AC`. But the arm holding
    it, `00279187`, is `002778C0`'s **message 31**, not message 1.
  - `002778C0`'s message 1 (`00277925`) stores `+0xD0` (the parent) and `+0xDC`. The `+0x61BA` → message-34 chain
    feeds `+0xDC`, not the kind.

  The receipt stays as committed; the register row carries the correction.
- **[The selection page](../../../16-UI/the-selection-the-menu-publishes.md), 2026-09-18 (FABLE's own)** read
  `0027E050`'s table as kinds 0–19. It is kinds 1–20: kind 1 → code 6, kind 2 → code 8, kind 3 → code 9, kinds 4–8 →
  code `0xB` with sub-selectors 3, 7, 5, 6, `0xD`, kind 9 → code `0x18`, and so on. W8 shows the kind-indexed reading
  breaks the W4 join for all four commands.

## Limits

- **Static.** Nothing was executed.
- **"Not reachable through the battle menu" is bounded by:**
  - the one `+0xD8` store in the dispatch family;
  - the message-31 and message-33 senders to this widget chain (immediate-id census of `00275440` / `002753F0` sites
    in `00270000`–`00280000`, plus the dispatch's own `call rax` at `00278895`);
  - the row-id writer census.

  A message-31 sender outside the family that reaches this widget by another route is not excluded.
- **What Foecraft is** in game terms is not read here. The name is the authored class-21 row text. Command 7 also
  appears in no code-7 or code-8 table (`00D10670`, `00D10680`).
- **Not read:** the other orphan kinds. For example, command 20 → kind 20 (class-21 row 20 is unused), the same
  shape as kind 5.

## Files

- `uq68_kind5.py` and `uq68_kind5.out`.
- `consumer-check.md`.
