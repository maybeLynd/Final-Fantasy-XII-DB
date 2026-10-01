# RC-18 and RC-19: party slot map 1 against the followers, and the two standard-motion blend arms (ORACLE, 2026-09-30)

Static answers for two rows SWE2-CONTRACT registered on 2026-09-30 from the batch-2 residue
(`../swe2contract-ddres-b2-0930/`). Shipping image `73461d08...`. Every script runs from this folder.
`img.py` is the shared image helper copied from `../rc5-event-slot-routes-0930/`, and `d.py` prints a function by its
`.pdata` chain root. Pages, the register and TEAM.json were not edited.

## The questions

- **RC-18.** Is party slot map 1 (`[02EBF190] + 0x5A5A`, which the appearance verbs `040D`-`0413` collect) the same
  membership as the characters the player sees following, in every state? This is SP-1's second half.
- **RC-19.** When `002EB0D0` starts a standard motion with the blend consulted, what do the character render record's
  two arms do? `004272E0` is taken for a blend below 0.0, which is the party verbs' `-1.0f`. `004270A0` is taken
  otherwise.

## Method

### RC-18

1. **Writers of map 1: `rc18_map1_writers.py`, output `rc18_map1_writers.out`.**
   - Engine: `../k14-closure-stores-0930/k14_actorflow.py`, subclassed as `rc4_flow.py` does.
   - Roots and tracking: the block pointer is followed from all 176 functions that load `02EBF190`, plus the
     functions that return it. Tracking goes through registers, the stack, offsets, callees and tail jumps.
   - Two additions to the engine:
     - Capstone marks the memory destination of `movups` and `movaps` as a read, so SSE moves are handled as
       stores. Without this, the base engine misses `00326717` and `00329DF6`.
     - `imul r64, s, C` followed by `add` onto the block is kept as "element k of a C-stride array at a known
       offset" (`A*C`), rather than being flattened to an unknown offset.
   - Positive control: the four known map-1 copy stores `00326717`, `0032671B`, `00329DF6` and `00329DFD`. PASS.
2. **Residue slices: `slice.py`, output `slice.out`.** For every store the flow could not place, this prints the
   base-register slice. The residue is classified by hand in the table under the RC-18 result.
3. **Map contents by mode: `rc18_modes_emu.py`, output `rc18_modes_emu.out`.**
   - This is isolated execution, not a live run: `BattleGroup_RefreshFourActorDefinitions` `003266C0` is run under
     unicorn for battle runtime modes 0 to 5.
   - Every callee is stubbed, and the value each stub returns is printed.
   - Map 0 is filled with three playables, a guest-band row, then three reserves.
   - Control: mode 0 must leave map 1 equal to map 0's slots 0 to 3 followed by five `0xFFFF`. PASS.
4. **Which map each consumer reads: `rc18_follow_path.py`, output `rc18_follow_path.out`.** Byte checks F1 to F6,
   plus a control on the read site `0031B841`. All PASS.
5. **The mode-change idiom in shipped scripts: `rc18_mode_idiom.py`, output `rc18_mode_idiom.out`.**
   - Corpus: FABLE's decompiled US corpus, 1,114 scripts.
   - Control: `seteventpartymode(1)` followed by `partyallread()`. PASS.

### RC-19

- **`rc19_blend_arms.py`, output `rc19_blend_arms.out`.** Checks R, N, Z, P, D, C and T, each against the shipped
  bytes. Positive control: the database's `17-Presentation-Rendering/Character-Render-Records/members/dirty-bits.tsv`
  must list the same setters for dirty bits 5 and 8. FAILS 0.
- **`rc19_rate_readers.py`, output `rc19_rate_readers.out`.** Every float access at `+0x354` in the image.

## Result

### RC-18: ANSWERED

**Map 1 is the engine's own follower source.** Both halves of the follow machinery walk it:
- `PartyFollow_SolveFormation` (`00338490`) walks map-1 slots 0 to 3 through
  `BattleUnit_FindMappedDefinitionSelectorByIndex` (`0031B810`). That function reads `byte [[02EBF190] + 2i + 0x5A5A]`
  at `0031B841`.
- `PartyFollow_ApplyGoal` (`003246C0`) collects its units through `0030A880(buf, 1)` → `0030A8A0`, which walks the
  same `0031B810`.

The end of every rebuild of map 1 also binds the roster to it. At the end of `003266C0` (`00326A40`-`00326B18`), each
roster slot's battle unit is compared with map-1 word i (`[r15]`, with `r15 = block + 0x5A5A`, set at `003266FC`). A
unit that differs is re-bound through `BattleUnit_ApplyUnitDefinition` (`0023A570`), and a `0xFFFF` word unbinds it.

So nobody follows the leader except through map 1. The sets differ only by these exact exclusions:

| in map 1 (slots 0-3) but not following | why (static) |
|---|---|
| the leader | `00338490` skips the unit equal to `BattleUnit_GetPartyLeader` (`003385EC`); `PartyFollow_LookupDestination` `00339A60` refuses it |
| a member with KO, Stone or X-Zone (`(+0x64 or +0x3C) & 0x80000003`) | the solver skips it unconditionally (`003385E0`). The applier keeps it when field record bit 15 holds (`0030A903`-`0030A911`), but it then has no formation slot and gets no destination |
| any member while the leader is not a party-kind unit | `00339A60` gate `cmp byte [leaderStats+5], 1` |

The appearance collector `0031B5A0` reads the same map-1 slots 0 to 3. It includes the leader and status-afflicted
members. It drops units whose flag bit 4 is clear or whose record `+5` is non-zero. The follow path tests neither of
those bits.

**The map-1 membership is mode-dependent** (`rc18_modes_emu.out`). The rebuild `003266C0` copies map 0 into map 1,
clears slots 4 to 8, and then rewrites slots 0 to 3 per runtime mode:

| mode | map 1 slots 0-3 | so the followers are |
|---|---|---|
| 0 (no mode bit) | map 0's four active slots (the guest in slot 3 included) | those four minus the leader and KO/Stone/X-Zone |
| 1 (summon) | the summoner (party index from `+0x5AD5`, `00313800`) in its own slot, and the summoned Esper's row (`+0x5AD4`, `003137E0`) in slot 3; the rest `0xFFFF` | at most the one who is not the leader |
| 2 (chocobo) | only `0x1A`, the Chocobo, in slot 3 | none (the mode-2 focus is `0x1A`) |
| 3 (field record bit 15) | one character: the field record's 3-bit value `00377C70` (or the focus slot), in its map-4 slot or slot 3 | none (the mode-3 focus is the same value) |
| 4 (event party) | the leader alone, in its own slot | none |
| 5 (event party 2) | the leader alone, in its own slot | none |

**Timing.**
- Map 1 changes only when `003266C0` runs.
- `003266C0` is called from the reconcile functions `003261D0` / `003273D0` and from `00233CF0`. `00233CF0` is the
  synchronous part of the read-in verbs `partyallread`, `partyallread2`, `summonread` and `summontopartyread`, and of
  `0026CE60`.
- The four mode setters only flip a bit of `+0x5B04`: `00307240`, `00307200`, `00313550` and the chocobo setter.
- In the shipped scripts, **all 1,045 mode changes are followed at once by a read-in verb**. The breakdown is 511
  `seteventpartymode`, 325 `seteventparty2mode` and 209 `setchocobomode` (`rc18_mode_idiom.out`). So no script leaves
  a frame between the mode and map 1.
- The known non-refresh windows are:
  - SP-2's one-sided roster writes.
  - The block reset `002370C0`, which memsets the block and leaves map 1 all zero. New game (`00237DF0`) runs the
    copy `00329CC0` right after it. The SetSaveData preset path `00239960` runs the reset after `00237DF0`, so its
    map 1 stays zero until the next rebuild.
  - A save load or the old-format import `002EF4A0`. These replace the block's bytes, so map 1 is as saved.

**Beyond following: who has a visible model.** The read-in machine gives a roster actor its definition through
`0031C250`, which reads map 4 (`+0x5A90`), not map 1 (F6).
- Map 4 equals map 1 on slots 0 to 3 in modes 0, 1 and 4.
- In mode 2, map 4 keeps map 0's slots 0 to 2 beside the Chocobo.
- In mode 3, map 4 keeps its previous words except the one slot.
- In mode 5, map 4 is restored whole to its value before the rebuild.

So in modes 2, 3 and 5, a roster slot can keep a model definition while its battle unit is unbound and it does not
follow.

**Writer census (map 1 = `+0x5A5A..+0x5A6B`):**
- **Exact-offset writers:** `003266C0` (the rebuild), `00329CC0` (the initial copy) and `002370C0` (the whole-block
  memset of `0x7410` bytes).
- **Stores into strided arrays of the block, all outside map 1:**
  - 140 into the forty `0x1C8` stats records, at record offsets `+0x8..+0x1D0`.
  - 16 into the `0x34` / `0x9C` gambit-bank arrays at `+0x5B10` and above.
- **Residue:** 120 store sites in 19 functions carry an unknown offset. They are classified from `slice.out`:

| functions | why they cannot reach `+0x5A5A` |
|---|---|
| `003266C0`, `00329CC0` | the known writers (loop cursors over maps 1, 2, 4) |
| `00329080` | map-0 index validated by class `0x17` (literal bound 9, `003290B0`), so `+0x5A48..+0x5A59` |
| `0030B180`, `0030B270` | byte array `+0x59C8 + (bazaar id & 0xFFF)`, index validated by class 18 (`02EBF058`, 128 shipped rows), so it ends at `+0x5A47`; it would reach map 1 only with more than 146 authored rows |
| `0030FBE0` | word arrays `+0x4F84 + 2k` and `+0x5004 + 2k`, with k below the image constants 64 (`01EEBCD0`) and 420 (`01EEBD28`), so they end at `+0x5003` / `+0x534B` |
| `00235AF0`, `00326030`, `003279B0`, `005691E0` | the `+0x5B10` bank arrays and the `+0x7370` selector dwords, with non-negative indexes: cursors from 0, or a zero-extended byte or word from each caller (`0023AF01`, `00328D04`) |
| `002FEF30`, `00300BC0`, `0030C650`, `0030E060`, `0030E130`, `0030E360`, `0030FED0`, `003112F0` | stats-record bodies. Their pointer argument is a record (`A*1C8` in the other contexts), and the untyped contexts come from record walks (`002342F0` steps by `0x1C8`) and pass-throughs (`0031B860`, `00385BA0`). Every store displacement is inside a `0x1C8` record |

### RC-19: ANSWERED

The start is `00427320(record, motion)` (`002EB154`). With the fourth argument zero, the blend (the fifth argument) is
compared with 0.0 (`002EB271`-`002EB2C9`). A **negative blend is a hard cut**, and a **positive blend is a cross-fade
of that length**:

| blend | arm | what it writes now | what the next dirty pass does |
|---|---|---|---|
| **< 0.0** (the party verbs' `-1.0f`, and the default that four start entries hard-code) | `004272E0` | only the record's dirty word `+0x294` (`dirtyFlags`): clear bits 7, 8, 10 and 17; set bit 5 (N) | bit 5 → `0042A890`. For the record, or its owner `+6` when `+0x284` bit 27 is set, and each linked record `+8` / `+0xA` that gate `00426220` accepts: `0041FC80` sets bit 24 of the active presentation entry (`00422D50`) when `+0x3FA < 0x1000`, then `00423A10` stops the alternate entry `+0xC8` and cuts to the pending entry `+0xC4` through `00424C40`. The cut commits the staged triple `+0x2B0..+0x2B8`, marks the entry started (`+0x24 = 1`) and publishes it (`0041D790`), with **no blend rate** (C) |
| **= 0.0** | `004270A0`, first arm | calls `00426FA0` at once: on the record and its linked records, set `objectFlags` `+0x284` bit 20 and clear `+0xC0` bit 6. Then the same bit-5 request (Z) | the same cut. `00424C40` turns the bit-20 mark into entry `+0xC` bits 17 and 26 |
| **> 0.0** | `004270A0`, second arm | stores the blend at `+0x308` (the field `paramFloat308` is this pending blend). Clears bits 5, 7, 10 and 17 of `+0x294`, and sets bit 8 (P) | bit 8 → `00429F70`, which carries `+0x308` (T) to `0042DF10` per record. That calls `00422E40` → `00424870` when the record's current event `+0xCC` is below `0x1000`, or `00422E50` → `00424A40` otherwise (special parented case: `00423FC0`). Each commits the staged triple, marks the entry started, **sets entry `+0xC` bit 11 and stores `1.0 / blend` at entry `+0x354`** (C), and sets bit 17. `00424A40` leaves an entry that is already started alone, while `00424870` restarts it (`0041CFC0`). A pending bit-20 mark turns either into the cut |

- Dirty bits 5, 7 and 8 are one exclusive request: each setter clears the other two, and `00427DE0` serves bit 5
  first, then 7, then 8 (D).
- The `-1.0f` therefore means **"switch to the new standard motion without interpolation"**. It differs from `0.0`
  only by not taking `00426FA0`'s reset mark.
- The positive arm's rate `1.0 / blend` shows the blend is a length. The one reader of an entry's `+0x354` in the
  image, `0041D560`, turns such a rate back into a step count `max(1, trunc(1 / rate))` for `003B5D40`. It is reached
  from the presentation command `00417F40` (`rc19_rate_readers.out`).

In player terms: when a script's party standard-motion verb plays a motion, each character snaps straight into it
rather than easing over from what it was doing.

## Not claimed

- **RC-18:**
  - Whether the roster actors that keep a map-4 model in modes 2, 3 and 5 are drawn. The mode hook table `01EECFC0`
    run by `0030D8B0` was not read.
  - Whether the engine-side mode changes are followed by a rebuild: the summon presentation's own bit set and clear
    (`00306946` / `00306A7E`), and field bit 15 on area entry (only reachability through `0026CE60` is shown).
  - The residue bounds rest on:
    - the stats-record index bound `0x27` guarded at the sites read;
    - the shipped class-18 row count (128);
    - non-negative indexes at `00326030` and `005691E0`.
  - The 15 escape sites and the 7 indirect calls in `rc18_map1_writers.out` are listed, not individually typed.
- **RC-19:**
  - Which consumer turns the standard-motion entry's `+0x354` into frames. `0041D560` is the only reader found, and
    it is reached from `00417F40`, so the unit of `blend` on this path is inferred from the rate form, not proven.
  - What entry bits 11, 17, 24 and 26 do downstream.
  - What `00426FA0`'s `+0x284` bit 20 means beyond being the zero arm's mark.
- Nothing here was observed in a running game.
