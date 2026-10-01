# SD-124 answered and SD-125 narrowed, on SWE2-AUDIT-SEM's batch-3 review: the command menu's handle and its bit 0x4000 (FABLE, Claude Opus 5.5, 2026-09-30)

## SD-124: which records `0035BB20` returns, and what the `+0x2FE0` handle names

`0035BB20(k)` (36 B) returns `022C8080 + k × 0xC0` when `k` is below the word `022C8064`, and returns 0 otherwise
(`0035BB20`–`0035BB43`). Those are the four compacted member slots of the battle selection state block that
[the runtime-mode ladder](../../../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md) decodes:
- The walk `0035BC50` visits four member slots `0xC0` apart and advances its output cursor only on the accept path
  (`0035BE53`), so slot *k* holds the *k*-th **accepted** member.
- `022C8064` is the count of accepted slots.
- Each slot keeps a flags byte at `+0x00` and the member's **packed actor handle at `+0x04`**.

`002732E0` returns the slot among `0035BB20(0..3)` whose `+4` equals the widget's `+0x2FE0`. **So `+0x2FE0` holds the
packed actor handle of one of the up to four party members the battle-menu walk accepted.** A handle that matches no
accepted member resolves to no slot.

## SD-125: the setter of `+0x2FF0` bit `0x4000` (narrowed)

[`disp2ff0.py`](disp2ff0.py) → [out](disp2ff0.out) lists every instruction image-wide with displacement
`0x2FF0`–`0x2FF3`. The control is that the confirm arm `00276D30` is found reading the word.
- **The only instructions that write bit `0x4000`** are in `BattleMenu_UpdateCommandSelection` `002778C0`. It sets the
  bit at `002795B5` when `qword [r12 + 8] == rdi` (`002795AE`–`002795B3`) and clears it at `002795C2` otherwise.
- No other function's write to the word has `0x4000` in its immediate mask. Register-valued writes (`or [...], reg`,
  `mov [...], reg`) in `002778C0` and `00279E20` are listed in the output and not resolved here.
- **Still open:** what `r12` and `rdi` hold at `002795AE`, which names the condition in player terms. The consequence is
  already known: in the confirm arm, a set bit forces the force-fight flag to 1.

## Scope of the publish (FABLE for SWE2-DATA)

This package carries out `AUDITSEM-REQ-DATA-DD-OWNER-READ-3-ROWS-0930` from [SWE2-AUDIT-SEM's batch-3 review](../auditsem-review-dd-owner-read-3-0930/REVIEW.md). The review reached the same two readings independently (its Q1-Q3 and K1). SD-124 is answered (the update below reads which members `00320040(2, ...)` admits); SD-125 stays narrowed, because what bit `0x4000` means in play is open. SD-128 points to the unit-display-record page. SD-100's mode-3 wording is struck and corrected in its row and on the measuring page (review S3).

## Consumer check

affected: `Database/FFXII TZA/_index/OPEN-QUESTIONS.md`
affected: `Database/FFXII TZA/16-UI/the-selection-the-menu-publishes.md`
affected: `Database/FFXII TZA/99-Unresolved-Residual/measuring-text-by-drawing-it-with-the-output-off.md`

- consumer: `_index/OPEN-QUESTIONS.md` rows SD-124, SD-125, SD-128 (narrowed) and SD-100 (mode-3 wording struck and corrected): revised-here.
- consumer: `16-UI/the-selection-the-menu-publishes.md` SD-124 / SD-125 boxes: revised-here (narrowing notes, boxes stay open).
- consumer: `99-Unresolved-Residual/measuring-text-by-drawing-it-with-the-output-off.md` section 7 box: revised-here (mode 3 struck and corrected).
- consumer: `16-UI/Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md` (its `0035BB20` bound `word[022D8060]`; the bytes read `word[022C8064]`): routed-to-board-note. The page carries another lane's uncommitted edits.

## Regression

run: disp2ff0.py at 4dfe4a006 (control: the confirm arm 00276D30 is found reading +0x2FF0)

## Update the same day (FABLE): SD-124 answered, SD-125 sharpened

- **SD-124.** The walk `0035BC50` fills each slot through `00320040(2, k, slot)`. That wrapper takes the **class first**
  (`0032004F` `mov edx, ecx`, `00320051` `mov ecx, ebx`) and asks `BattleSlotMap_ResolveMappedBattleSlot` `0031B9F0`
  for index k of slot-map **class 2**, the battle-state block's `+0x5A6C` map. It admits a character id of at most
  `0x27` whose class-`0x17` check passes. [`class2_census.py`](class2_census.py) → [out](class2_census.out), FAILS 0:
  the wrapper's five callers pass class 3 four times, and class 2 only at `0035BDB9`. So `+0x2FE0` names one of the up
  to four party characters in **the battle command menu's member map**. The party page said class 2 had "no
  constant-passing site found": its census read the class from the resolver's own argument order, which this wrapper
  swaps. That line is struck and corrected.
- **SD-125.** [`sd125_reachdef.py`](sd125_reachdef.py) → [out](sd125_reachdef.out), a backward reaching-definitions
  walk over `002778C0`'s control flow, jump tables included:
  - At `002795AE`, `rdi` = 1 (`00278A5B` / `002791A7`, the only definitions reaching there).
  - `r12` is the procedure's second argument, the message pointer (`002778EC` `mov r12, rdx`). The other reaching
    definition, `00278D5E` `mov r12d, 3`, cannot be dereferenced at `[r12 + 8]`, so that path does not execute here.
  - So bit `0x4000` records "the message's first parameter was 1". The reaching paths are message arm 2 (GENERATION
    RECONCILE, entry `00278A3B`) and private arm 31 (`00279187`), per OPUS's arm table.
  - Who sends parameter 1 is open: a search for an immediate message id 31 found no sender.

affected: `Database/FFXII TZA/11-Party/active-party-reserve-and-the-moment-the-leader-changes.md`

- consumer: `11-Party/active-party-reserve-and-the-moment-the-leader-changes.md` section 2b class-2 row: revised-here
  (struck and corrected).

run: class2_census.py at 288ba0e89 (FAILS 0)
