# GR-12: what battle actions `0x9C` and `0x9D` do (SWE2-CONTRACT for OPUS, 2026-09-30)

Register row GR-12. Page: [equipment-slots-and-the-single-stat-rebuild.md](../../../12-Items-Equipment-Shops-License/equipment-slots-and-the-single-stat-rebuild.md) §11.3.
Method: static. The certified image was read through the kit's `retool.py`. Shipped data: `battle_pack.bin` (the action
table at directory `+0x3C`, text bank 0 in five languages, the weighted pick tables at `+0x2C`), `help_action.bin`, and
the 166 `in` `.ard` order sets. The checker is `gr12_actions_check.py`; its output is `gr12_actions_check.out`, which ends **`FAILS 0`**.

## Answer (SWE2-CONTRACT for OPUS)

**Neither action does anything.** No engine code handles either id. A party unit that is issued one has it
refused before commit, so the action never runs.

- **What they are.** The engine gives these ids no meaning of their own; only the text names them. The us/es/it copies
  of bank 0 hold placeholders (*Reserve* / *DUMMY* / *dummy*). The **de** and **fr** copies keep real names for the
  three category-13 rows (S8):

  | row | de | fr (developer romaji) |
  |---|---|---|
  | 155 = `0x9B` | *Außer Anführer An* | `leaderigaion` ("everyone except the leader: on") |
  | 156 = `0x9C` | *Alle An* | `zeninon` ("everyone: on") |
  | 157 = `0x9D` | *Gambit Aus* | `gambitoff` |

  These are the three entries of a cut **Gambits sub-list** in the battle menu. The rows carry no effect at all:
  recipe `+0x08` 0, both power bytes 0, status mask 0, `+0x22` / `+0x24` `0xFFFF`, no presentation event, flags
  `0x210`, not listed (`+0x38` `0xFFFF`), `+0x1C` 3, `+0x2D` `0x20`, target side 0. The three rows are identical apart
  from the help id (whose texts are empty) and the name word (S7).
- **Contract of the issue** (`0x9C` and `0x9D` alike). Inputs: the action id and the unit's own handle as target.
  `BattleUnit_IssueCommandByFocusHandles` `00311CD0` → `00311B20` single-unit arm → `BattleUnit_IssueCommand`
  `00311CF0` (S1, S1b). If the unit's record passes `(+0x64 | +0x3C) & 0x8800203B == 0` (`00311D72`), the issue writes:
  - `+0xBA0` = id;
  - `+0x6B0` bit 1 cleared;
  - `+0xBB8` = its own handle;
  - `+0xBA4 |= 0x8000`;
  - unit qword `|= 0x4000` (the pending bit);

  and then calls `00317E60` (S11).
- **Completion.** At the unit's next decision, `00305AB0` clears the pending bit (`00305AEB`). Because the id is outside
  `0x4000`–`0x4166`, it goes through `BattleAction_CheckActionAvailabilityReason` `002FFCF0` (`00305B09`) (S12, S13):
  - `0031A7B0` passes category 13 (it returns 0).
  - `BattleAction_CheckDefinitionCategoryAvailability` `003060E0` returns **5** for a kind-0 (party-table) unit
    whose `+0x1E` falls outside `{0,1,2,3,5,6,9,0xFF}`. The arm at `00306300` refuses categories 7, 8, 10, 13, 14,
    16 and 17 (S6, S7).
  - `00306480` collapses that 5 to reason **`0x0F`**.

  `00305AB0` then skips `BattleUnit_CommitAction` and moves on to the unit's own order sets. `+0x714` is never written.
  No phase runs, no target is resolved and nothing changes: no equipment, no stashed item, no gambit flag. The refusal
  gives no feedback, because the menu ignores what the issuer returns and closes (result `0x17`).
- **No path reaches an effect.**
  - The gambit on/off bit (bit 2 of `00320A40(slot)`) changes at run time only through `00311AF0`. Its two callers
    are the menu's per-character Gambits toggle (`0027C512`) and `00567DDD` (S15).
  - Every other `+0xBA0` reader is gated on the pending bit, or compares the word only with `0x113` / `0x95` (S14).
  - Of the 12 image-wide `0x9C` / `0x9D` immediates, only the menu functions `0027C3D0` and `0027CE70` use the value
    as an action id (S9).
  - The order-set path runs the same cascade before it commits (`003014C0` @ `003015FF`, S18).
  - No authored enemy order record (50,050) and no weighted pick-table entry (3,587) names `0x9B`–`0x9D` (S17).
- **The menu never offers them.** The branch GR-12 cites is dead in the shipped build:
  - Submenu 8 is the category-13 list (kind 11, category `0xD`, `0027E2AC`). Its builder drops `0x9C` / `0x9D` for a
    party unit, because `00317BC0` → `00306480` answers `0x0F` (S5, S6).
  - Only `0x9B` bypasses that gate (`0031EFB3`). Its entry gets flag `0x20` (`0031F187`), and selecting it returns 9
    and opens submenu 9 (S2).
  - Submenu 9 is kind 24. `0031EB20` builds nothing for kind 24 (`0031F70C` returns the count it zeroed at
    `0031EB40`), and `0027C3D0` returns `0x16` for an empty container (S4). So the item comparison at
    `0027C613`–`0027C665` never runs with an entry.
  - Submenu 8 itself has no static opener (S10).

**In player terms:** these are the "all gambits on" and "gambits off" commands of a Gambits sub-menu that was cut from
the battle menu. The game never shows them. If one is forced onto a party member, the character ignores it and carries
on with its gambits.

## `00273270` (the second half of the row) (SWE2-CONTRACT for OPUS)

The correction from SWE2-AUDIT-SEM holds, and it can be made sharper (S16):

- `00273270` returns **`0xFFFF`** on both early exits: a zero handle (`0027328F`), or `003588B0` failing (`00273299`).
  Both go to `002732C1`.
- Otherwise it pre-fills `+0xAC` of the stack record with `0x0000FFFF` (`0027329B` / `002732A7`). `0031FF70` always
  tail-jumps to `00329220` with mode 1 (`00320032`), and **`00329220` first memsets the whole 0xC0-byte record**
  (`00329248`). The pre-fill is therefore a dead store.
- When `0031FF70` finds no stats record (`rdi` 0), `00329220` exits at `00329268` with `+0xAC` = 0, and the function
  returns **0**.
- Otherwise `+0xAC` = stats `+0x5A` `<< 16` (`00329740`, the only writer of `+0xAC`), so it returns `saved[0]`.

`saved[0]` is itself 0 until the first takeaway, because it holds only what `0023ACBD`'s memset left there.

So there is no failure answer of 0 alongside an empty marker of `0xFFFF`: the answer is `0xFFFF` when there is no unit,
0 when there is no record or nothing was ever stashed, and the stashed item otherwise. The asymmetry the row asks about
is between a stack pre-fill that can never survive and the memset's 0.

`0027D740` stores the same answer at `+0x1538`, the "current" marker that the kind-24 display `0027BC10` highlights.
That is consistent with the designers' intent for kind 24, but it is moot, because the list is always empty.

## Steps (SWE2-CONTRACT for OPUS)

| step | claim | evidence |
|---|---|---|
| S1 / S1b | the kind-24 arm issues `0x9D` (entry = answer or `0xFFFF`) or `0x9C`, with the target = self | `0027C619`–`0027C665`, `00311CD0`, `00311B20` @ `00311C93` |
| S2 | kind 11 issues an entry id of `0x9C` / `0x9D` at once; flag `0x20` opens submenu 9; an empty container gives `0x16` | table `0x15C6B8` / `0x15C6A0`; `0027C591`–`0027C5FE`; `0027C3E3` |
| S3 | cmd 8 = kind 11 with category 13, cmd 9 = kind 24 | `0027E050` table `0x15E384`; `0027E2AC`, `0027E2B6`, `0027E2D8` |
| S4 | the kind-24 list is always empty | `0031EB20` table `0x1FFBA4`; `0031EB40`, `0031F70C` |
| S5 | the kind-11 builder, the `0x9B` / `0x113` bypass and `0x9B`'s flag `0x20` | `0031EF0D`–`0031EFD3`, `0031F17F` |
| S6 | category 13 → 5 → `0x0F` for a party unit; 0 for another kind | `00306129`, `00306181`–`00306300`, `003064AF`, `00317BF6` |
| S7 | the only `+0x1E` = 13 rows, and they carry no effect fields | `battle_pack.bin` `+0x3C` |
| S8 | the de / fr names; the us / es / it placeholders; empty help texts; controls `0x95` / `0x113` / Cure | bank 0 in five languages; `help_action.bin` |
| S9 | the 12 immediates: action ids only in `0027C3D0` / `0027CE70`; `0x9B` only in `0031EB20` | image-wide scan |
| S10 | no producer of submenu 8 among the classifier returns, `0027C730` (`0x10`–`0x13`), `00276650` (1), or the 11 posters of `0x1F` / `0x21` | `0027C3D0`, `00D10680`, `0027C730`, `002766A3`, `0027A793` |
| S11 | what an issue writes | `00311D72`–`00311DE8` |
| S12 | consumption: the pending bit is cleared, the cascade runs, and commit happens only on 0 | `00305AD0`–`00305B3C` |
| S13 | the cascade returns `0x0F` for category 13 | `002FFE87`–`002FFEA4`, `0031A84E` |
| S14 | all 19 `+0xBA0` sites classified | image scan `00200000`–`00600000` |
| S15 | the gambit-bit setter's callers | `00311AF0` ← `0027C512`, `00567DDD` |
| S16 | the `00273270` contract | `0027328D`–`002732BC`, `00320010` / `00320032`, `00329231`–`00329740` |
| S17 | no authored order or pick entry names `0x9B`–`0x9D` | 166 `.ard`, `battle_pack.bin` `+0x2C`; `00308EC0` |
| S18 | the order-set path gates records through the same cascade | `003015F7`–`00301606`, `00305DD2`–`00305DF4` |

## Limits (what is not settled statically) (SWE2-CONTRACT for OPUS)

- **A non-party (kind ≠ 0) unit.** `003060E0` returns 0 for such a unit (`0030612F`), and the licence leg returns
  "has licence" (`00324002`), so the cascade could pass. `BattleUnit_CommitAction` would then run the standard advancer
  `00304850` with this effect-free row. With a zero recipe, `00385906`–`0038596A` reads the attacker's weapon word.
  What that execution would do is **not read**. No shipped path reaches it: the menu issues only for focus units, and
  S17 / S18 cover the order sets.
- **Submenu 8's openers are not a closed set.** Message 33 copies a payload word into `+0x61B8` (`0027A793`), and the
  menu history stack (`+0x70`) replays earlier submenus. Every direct producer found yields 1, 2–7, 9, 10–14, 15,
  `0x10`–`0x13` or `0x14`, never 8. What was not enumerated: a poster outside `00240000`–`002A0000`, or a history value
  that was never opened.
- **The gambit-editor lists** (`002C4720`, `0056A890`…) were not enumerated for category 13. This does not matter,
  because S18 refuses the id on the order-set path anyway.
- **Runtime.** No live test was run. The one runtime check that would add something is to force `+0xBA0` = `0x9C` with
  the pending bit on a party member, and confirm that `+0x714` is never written and the unit goes on with its gambits.

## Contradictions with the page (§11.3) and the register row (SWE2-CONTRACT for OPUS)

1. The page says *"Both rows point at a Reserve placeholder … so the shipped text gives them no name"*. That is true
   of us / es / it only. The **de and fr** copies name them *Alle An* / *Gambit Aus* and `zeninon` / `gambitoff`, and
   `0x9B` *Außer Anführer An* / `leaderigaion`.
2. The page says *"the failure preset makes the 'nothing to compare' answer 0"*, and the register asks why the failure
   answer is 0. That preset never survives: `00329220`'s memset overwrites it. The early exits return `0xFFFF`. The 0
   comes from the memset, when there is no stats record, or from a `saved[0]` that has never been stashed.
3. The page says the entry id *"chooses command `0x9D` over `0x9C`"*. This is correct as code, but the branch is dead:
   the kind-24 list is always empty (S4), and its only way in is the unopened category-13 list (S5, S10). The framing in
   `eq_action_names.py` ("the battle-menu equip branch") is not supported, because the names are gambit toggles.
4. Nothing on the page contradicts the refusal. The reason-code table already has `0x0F` for "definition category
   unavailable". This package adds that category 13 falls in `003060E0`'s default arm.
