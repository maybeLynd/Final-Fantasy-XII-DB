"""apply_10status.py [--apply] - 10-Status-Periodic-Terminal readiness map (readiness-10-status.md), section 2.4
contradictions 1-46 and the two section 2.5 image findings, settled on the pages (OPUS, 2026-10-02).

Each edit strikes the DISFAVOURED side only (the side the map's dated correction, the bytes or the shipped data
refute) and restates it, tagged *(corrected 2026-10-02, OPUS: ...)* or *(answered: see ...; 2026-10-02, OPUS)*.
Code-block lines get a trailing comment instead of a strike; their OLD runs into the next line so NEW never
contains OLD. Headings that change carry OPUS (publish heading gate).
Exact substrings, each once; tag-guarded; dry run unless --apply; FAILS n.
"""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
F = "10-Status-Periodic-Terminal/"
R = F + "README.md"
S32 = F + "the-thirty-two-statuses.md"
MP = F + "where-mp-comes-from.md"
L2 = F + "Status-And-Augment-Layers/two-layer-effect-model.md"
SW = F + "Status-Write/the-status-write-and-its-side-effects.md"
PT = F + "Periodic-Tick/what-the-periodic-tick-does.md"
CEL = F + "CONTRACT-effect-layers.md"
CPT = F + "CONTRACT-periodic-tick.md"
CSW = F + "CONTRACT-status-write.md"
CASR = F + "CONTRACT-auto-status-rebuild.md"

EDITS = [
    # C1: 0030E360 does reach the applier (status 28 removal, +0x48 != 0); bytes 00386A94-00386AC2, 0030E610-0030E638.
    (CSW, "> **`003112F0` IS STRUCK FROM THIS LIST: IT CAN NEVER FIRE THROUGH `0030E360`.**",
     "> ~~**`003112F0` IS STRUCK FROM THIS LIST: IT CAN NEVER FIRE THROUGH `0030E360`.**~~ **`003112F0` stays on this "
     "list: it fires through `0030E360` for exactly one transition, removing status 28 with a non-zero `+0x48`** "
     "*(corrected 2026-10-02, OPUS: for id `0x1C` with `[rsi+0x48]` non-zero, `00386A70` returns at `00386AC2` "
     "without reaching `00386AC3`, so bit 0 stays set and `0030E610` lets `0030E638 call 003112F0` run; §13's "
     "builder table gives the same mask, `0x109`)*."),
    (CSW, "builder B CLEARS it\n> ```",
     "builder B CLEARS it, except for status 28 with +0x48 non-zero, which returns at 00386AC2 first (corrected 2026-10-02, OPUS)\n> ```"),
    (CSW, "> **Both builders clear the one bit the setter sets**, and every path to the applier runs through a\n"
          "> builder, so the gate is closed before it is ever tested. **A static call graph shows the edge and\n"
          "> the edge is dead**",
     "> ~~**Both builders clear the one bit the setter sets**, and every path to the applier runs through a\n"
     "> builder, so the gate is closed before it is ever tested. **A static call graph shows the edge and\n"
     "> the edge is dead**~~ Both builders clear the bit on every path but one: the remove builder leaves it set "
     "for status 28 with a non-zero `+0x48`, so the gate is open for that removal and the edge is live "
     "*(corrected 2026-10-02, OPUS: `00386A94`–`00386AC2`, `0030E610`–`0030E638`)*"),
    (CSW, "grant); what is false is listing it\n> among the callees a reimplementation of **this** operation must provide.",
     "grant); ~~what is false is listing it\n> among the callees a reimplementation of **this** operation must provide.~~ "
     "a reimplementation of **this** operation must provide it for the status-28 removal *(corrected 2026-10-02, "
     "OPUS: see the correction above)*."),

    # C2: the 32 statuses are not in the merged layers; 003847C0 ORs only +0x68/+0x78 (00384820-00384858), status words go to +4/+8.
    (CEL, "meanings — bit 2 is *Petrify* in the mutable layer and\n*AccuracyBoost* in the derived, bit 16 is *Disease* and "
          "*Weatherproof*. Because L-3 merges them, **a\nunit with Disease satisfies the early-out intended for "
          "Weatherproof.**",
     "meanings — ~~bit 2 is *Petrify* in the mutable layer and\n*AccuracyBoost* in the derived, bit 16 is *Disease* and "
     "*Weatherproof*. Because L-3 merges them, **a\nunit with Disease satisfies the early-out intended for "
     "Weatherproof.**~~ bits 2 and 16 of the mutable layer are effect ids, aliased by L-3 with *AccuracyBoost* and "
     "*Weatherproof* of the derived layer. The battle statuses Petrify and Disease are not in either layer: they live "
     "in the status words `+0x64` / `+0x3C` (§3), which `003847C0` copies to context `+4` / `+8`, not `+0x1A`, so a "
     "unit with the Disease status does not satisfy the Weatherproof early-out unless something writes id 16 into "
     "`+0x68`, and no such writer is shown *(corrected 2026-10-02, OPUS: checked at `00384820`–`00384858` and "
     "`0030E360`, which has no call to `0030E130`; two-layer-effect-model.md §5, clarified 2026-09-29)*."),
    (L2, "consequence\n\nBecause the layers merge, a combatant with **Disease** (status bit 16) satisfies the same\n"
         "early-out as one with **Weatherproof** (augment bit 16). The intended identity is\n"
         "Weatherproof; the alias is a real, observable engine property.",
     "consequence\n\n~~Because the layers merge, a combatant with **Disease** (status bit 16) satisfies the same\n"
     "early-out as one with **Weatherproof** (augment bit 16). The intended identity is\n"
     "Weatherproof; the alias is a real, observable engine property.~~ The merge aliases only what the two layers "
     "hold: effect id 16 in `+0x68` with Weatherproof in `+0x78`. The battle status Disease lives in the status "
     "words `+0x64` / `+0x3C`, which `003847C0` copies to context `+4` / `+8`, not into the merged `+0x1A`, so a "
     "combatant with the Disease status does not satisfy the Weatherproof early-out unless something writes id 16 "
     "into `+0x68`, and no such writer is shown *(corrected 2026-10-02, OPUS: checked at `00384820`–`00384858`; "
     "`0030E360` has no call to `0030E130`; §5's 2026-09-29 clarification)*."),
    (S32, "imply.** `BattleFormula_BuildEvaluationContext` ORs the status layer\nand the augment layer into one bitmap per id "
          "(`00384820`–`00384858`), so a calculator that tests\nmerged id 9 cannot tell Silence from Brawler, nor id 16 "
          "Disease from Weatherproof, nor id 17 Lure\nfrom Thievery. Slot 72's half-formula is therefore reachable by a "
          "**Silenced** unarmed attacker as\nwell as by one with Brawler — a consequence of the merge as read, not "
          "observed.",
     "imply.** ~~`BattleFormula_BuildEvaluationContext` ORs the status layer\nand the augment layer into one bitmap per id "
     "(`00384820`–`00384858`), so a calculator that tests\nmerged id 9 cannot tell Silence from Brawler, nor id 16 "
     "Disease from Weatherproof, nor id 17 Lure\nfrom Thievery. Slot 72's half-formula is therefore reachable by a "
     "**Silenced** unarmed attacker as\nwell as by one with Brawler — a consequence of the merge as read, not "
     "observed.~~ `BattleFormula_BuildEvaluationContext` ORs the two effect-id layers `+0x68` / `+0x78` into one "
     "bitmap (`00384820`–`00384858`). The 32 statuses are in neither layer: they are the status words, copied to "
     "context `+4` / `+8`, so a merged-id test does not see Silence, Disease or Lure, and this merge does not open "
     "slot 72's half-formula to a Silenced attacker *(corrected 2026-10-02, OPUS: checked at `003847C0`; "
     "two-layer-effect-model.md §5, clarified 2026-09-29)*."),

    # C3: the status write never calls the layer mutator (0030E360 has no call to 0030E130).
    (CEL, "— the *operation*; it calls the mutate body and states nothing about the layers |",
     "— the *operation*; ~~it calls the mutate body and~~ it does not call the mutate body *(corrected 2026-10-02, "
     "OPUS: checked at `0030E360`, whose call targets do not include `0030E130`; two-layer-effect-model.md §5)* and "
     "states nothing about the layers |"),
    (CEL, "`0030E360`, this category's own status write, is the\n  principal caller of the mutate operation.",
     "`0030E360`, this category's own status write, ~~is the\n  principal caller of the mutate operation~~ does not "
     "call the mutate operation; its callers are `003112F0` (applier step 14), `002FDDA0` and `0030FED0` "
     "*(corrected 2026-10-02, OPUS: checked at `0030E360`)*."),

    # C4: context +0x08 is the target's status words (0038485F-00384868); bits 12/16/23 = Reverse, Disease, Reflect.
    (CEL, "  +0x08  u32      flag word (bits 12, 16 and 23 participate in §4's revocation)\n  +0x18  u16",
     "  +0x08  u32      flag word (bits 12, 16 and 23 participate in §4's revocation)   <- corrected 2026-10-02, OPUS: "
     "not a flag word; the TARGET's status words +0x64 | +0x3C (0038485F-00384868), so bits 12, 16, 23 are Reverse, "
     "Disease, Reflect\n  +0x18  u16"),
    (CEL, "- What the flag bits 12, 16 and 23 of context `+0x8` mean, and what effect id 15 is named.",
     "- ~~What the flag bits 12, 16 and 23 of context `+0x8` mean,~~ *(answered: see the-thirty-two-statuses.md §4 — "
     "context `+0x8` is the target's status words `+0x64` / `+0x3C`, `0038485F`–`00384868`, so bits 12, 16 and 23 "
     "are Reverse, Disease and Reflect; 2026-10-02, OPUS)* and what effect id 15 is named."),

    # C5: the stage-3 slot index is byte +6 of the effect table 02EBF040, not of status_data (whose +6 is the flag word).
    (CPT, "factor, `+6` effect-timer slot index, `0xFF` meaning none), the effect table at `02EBF040` that keys",
     "factor~~, `+6` effect-timer slot index, `0xFF` meaning none~~ — its `+6` is the flag word; the effect-timer "
     "slot index, `0xFF` meaning none, is byte `+6` of the effect table's rows *(corrected 2026-10-02, OPUS: "
     "`00385585`, `003855FD`–`00385604`; checked against `status_data.bin`)*), the effect table at `02EBF040` that keys"),
    (PT, "  it is a byte at `+6` of the status's own record, not the status id.",
     "  it is a byte at `+6` of ~~the status's own record~~ the id's row in the effect table `02EBF040`, not of "
     "`status_data` (whose `+6` is the flag word) *(corrected 2026-10-02, OPUS: `00385585`, `003855FD`–`00385604`; "
     "§13's 2026-09-12 correction)*, not the status id."),
    (PT, "- **A status record whose byte `+6` is `0xFF` never expires.**",
     "- ~~**A status record whose byte `+6` is `0xFF` never expires.**~~ **An effect id whose effect-table row "
     "(`02EBF040`) has byte `+6` = `0xFF` has no stage-3 timer**; in the shipped table only rows 55, 56 and 57 "
     "carry a slot (3, 4 and 5) *(corrected 2026-10-02, OPUS: `003855FD`–`00385604`; checked against "
     "`battle_pack.bin` slot 29)*."),

    # C6: effect-table +6 is the stage-3 slot index, 0xFF except rows 55-57 (checked against battle_pack.bin slot 29).
    (MP, "bytes `{u16 nameId, u16 0x5000 + row, u16 parameter, u16 0xFF}`",
     "bytes `{u16 nameId, u16 0x5000 + row, u16 parameter,` ~~`u16 0xFF}`~~ `u16}` whose low byte `+6` is the "
     "stage-3 timer-slot index: `0xFF` in 126 rows, `03` / `04` / `05` in rows 55 / 56 / 57 *(corrected 2026-10-02, "
     "OPUS: checked against `battle_pack.bin` slot 29; the periodic tick reads it at `00385619`)*"),

    # C7: slot-22 +4..+7 are non-zero on rows 20-24 (25, 50, 100, 200, 1000), checked against battle_pack.bin 0x1B58.
    (MP, "own shape. Bytes `+4`–`+7` of every row are zero.",
     "own shape. ~~Bytes `+4`–`+7` of every row are zero.~~ Bytes `+4`–`+7` are zero in rows 0–19 only; rows 20–24 "
     "hold 25, 50, 100, 200 and 1,000 there, the `mpThreshold` column *(corrected 2026-10-02, OPUS: checked against "
     "`battle_pack.bin` at `0x1B58`; §2, walking recovery)*."),

    # C8: the 64-byte records start at 0208D480 / 0208DE80; stage 5's word is field +0x14; +0x18 (walk carry) is read.
    (PT, "one array at `0208D494` — forty 64-byte records\n      indexed by a kind-0 record's type byte `+4`, then from "
         "`0208DE94` records indexed by the",
     "one array ~~at `0208D494`~~ based at `0208D480` (stage 5 addresses field `+0x14` of each record, hence "
     "`0208D494`) — forty 64-byte records\n      indexed by a kind-0 record's type byte `+4`, then from ~~`0208DE94`~~ "
     "`0208DE80` (field `+0x14` at `0208DE94`) records indexed by the"),
    (PT, "and word `+0` of the\n      record is the unit's **out-of-combat tick counter**",
     "and word ~~`+0` of the\n      record~~ `+0x14` of the record is the unit's **out-of-combat tick counter**"),
    (PT, "rest of stage 5\"). The other 62 bytes are unread.",
     "rest of stage 5\"). ~~The other 62 bytes are unread.~~ The other bytes are not all unread: `+0x18` is the "
     "walk-MP carry, read and written by `002F9400` *(corrected 2026-10-02, OPUS: `00386885` / `003868AD` and "
     "`002F9439` / `002F9461` / `002F9474`; where-mp-comes-from.md §5, CS-6)*."),
    (CPT, "- The other 62 bytes of stage 5's 64-byte records.",
     "- ~~The other 62 bytes of stage 5's 64-byte records.~~ The rest of those records: they are the per-combatant "
     "records based at `0208D480` / `0208DE80` (where-mp-comes-from.md §5, CS-6); stage 5's counter is their field "
     "`+0x14` and `+0x18` is the walk-MP carry, so not 62 unread bytes; the remaining fields are not mapped here "
     "*(corrected 2026-10-02, OPUS: `00386885` / `003868AD`, `002F9474`)*."),

    # C9: the tick does more than one record and one apply (00310DB0: three 003112F0 calls, 00300CE0, 00321530, 003138D0).
    (CPT, "flag bit. Everything else the unit receives comes through `003112F0`.",
     "flag bit. ~~Everything else the unit receives comes through `003112F0`.~~ The unit also receives two further "
     "`003112F0` applies, each built by `00385F60` (`003110AB`, `0031126C`), walk MP through `00300CE0` "
     "(`003110D7`), enmity decay `00321530` (`003112A4`) and, before the record, the Esper dismiss `003138D0` "
     "(`00310EF8`) *(corrected 2026-10-02, OPUS: checked at `00310DB0`)*."),
    (CPT, "stage 1..5 → apply*.",
     "stage 1..5 → ~~apply~~ apply → the rest of the body, which this order omitted: 26 more calls after "
     "`00310FAC`, among them two further `00385F60` builds applied through `003112F0` (`003110AB`, `0031126C`), "
     "walk MP (`003110C3` / `003110D7`) and enmity decay (`003112A4`)*. *(corrected 2026-10-02, OPUS: checked at "
     "`00310DB0`)*"),

    # C10: status_data +9 is the beat; +8 is the duration (003876D0 reads +9; 00387730 reads +8 at 0038788D/0038792C).
    (S32, "Timer units are `status_data.bin` `+9`; the frame count is",
     "~~Timer units are `status_data.bin` `+9`~~ The beat is `status_data.bin` `+9` and the duration is `+8` "
     "*(corrected 2026-10-02, OPUS: `003876D0` reads `+9`, `00387730` reads `+8` at `0038788D` / `0038792C`; §2.1 "
     "and the status write §2.4a, 2026-09-12)*; the beat's frame count is"),
    (S32, "- **The timers are in `status_data.bin` `+9`**, in units",
     "- ~~**The timers are in `status_data.bin` `+9`**~~ **The beats are in `status_data.bin` `+9`** (the durations "
     "are `+8`, §2.1) *(corrected 2026-10-02, OPUS: `003876D0` reads `+9`, `00387730` reads `+8`)*, in units"),
    (SW, "`+9` = duration unit, `+0x0C` = the mask",
     "~~`+9` = duration unit~~ `+9` = beat, `+8` = duration base (§2.4a) *(corrected 2026-10-02, OPUS: `003876D0` "
     "reads `+9`, `00387730` reads `+8`)*, `+0x0C` = the mask"),
    (SW, "- **The duration unit is data too**: byte `+9`, scaled by `01DFE0B4` and `× 30`. A status with\n"
         "  byte 9 = 0 gets timer 0.",
     "- ~~**The duration unit is data too**: byte `+9`, scaled by `01DFE0B4` and `× 30`. A status with\n"
     "  byte 9 = 0 gets timer 0.~~ **The beat is data too**: byte `+9`, scaled by `01DFE0B4` and `× 30` "
     "(`003876D0`); a status with byte 9 = 0 gets beat 0. The duration is byte `+8` (`00387730`, §2.4a) "
     "*(corrected 2026-10-02, OPUS: §2.4a, 2026-09-12)*."),

    # C11: the stage-4 drain lands per beat (frame base x 10 ticks), not per tick.
    (PT, "the drain is max MP / 50 per tick.",
     "the drain is max MP / 50 per ~~tick~~ beat, every `frame base × 10` ticks *(corrected 2026-10-02, OPUS: §5 and "
     "CONTRACT-periodic-tick.md §11)*."),

    # C12: the stage-4 gate tests masks 2 (MP) and 1 (HP) = bits 1 and 0 (the contract's own T12 at 00385CCE/00385D6A).
    (CPT, "has bit 2, MP drains by max MP / 50 per beat (at least 1)**; on one with",
     "has ~~bit 2~~ mask 2 (bit 1, counting from zero), MP drains by max MP / 50 per beat (at least 1)**; on one with"),
    (CPT, "bit 1, HP drains by 1 % of max HP per beat",
     "~~bit 1~~ mask 1 (bit 0), HP drains by 1 % of max HP per beat *(corrected 2026-10-02, OPUS: §T12's narrowing, "
     "`00385CCE` passes mask 1 and `00385D6A` mask 2)*"),
    (CPT, "gated by bits 1 and 2 of the active field's word",
     "gated by ~~bits 1 and 2~~ masks 1 and 2, bits 0 and 1, of the active field's word"),

    # C13: 0030E360's mode range is 0..5 (0030E4CB cmp eax, 5 / ja).
    (PT, "The caller also passes a mode (`0`–`3`)",
     "The caller also passes a mode (~~`0`–`3`~~ `0`–`5` *(corrected 2026-10-02, OPUS: `0030E4CB cmp eax, 5` / `ja`)*)"),

    # C14: stage 2 does reach the duration array and writes a word array (00386E84, 00386EEC).
    (PT, "\n**They are not the same, and stage 2 does not touch the duration array at all.**",
     "\n~~**They are not the same, and stage 2 does not touch the duration array at all.**~~ **They are not the same "
     "arrays, but stage 2 does reach the duration array**: it addresses the target's `+0xBC[s]` through `r14` "
     "(`00386EEC`) and writes the result's `+0xDC[s]` word array through `r15` (`00386E84 mov word ptr [r15], ax`) "
     "*(corrected 2026-10-02, OPUS: see \"Corrected 2026-09-12\" below; only the heading had been struck)*."),
    (PT, "| 2 — `AdvanceStatusTimersAndBuildResult` | **no** | none | **yes** |",
     "| 2 — `AdvanceStatusTimersAndBuildResult` | **no** | ~~none~~ result `+0xDC[s]` through `r15` (`00386E84`) "
     "*(corrected 2026-10-02, OPUS)* | **yes** |"),

    # C15: 002373C0 sets 0x800 only; request 0x17 is the party-focus test's (003010C5-003010F1).
    (SW, "carries a terminal status — request `0x17` |",
     "carries a terminal status — ~~request `0x17`~~ latch `0x800` only (`003010CE`); request `0x17` belongs to the "
     "party-focus test, with `0x100` (`003010D8`–`003010F1`) *(corrected 2026-10-02, OPUS: checked at "
     "`003010C5`–`003010F1`; §2.7)* |"),

    # C16: the default Petrify/Doom count is 11 stored, 10 displayed (00387740-00387759, mov eax, 0xB).
    (S32, "| 2 | Petrify | — (count 10) |",
     "| 2 | Petrify | — (count ~~10~~ 11 stored, shown as 10 *(corrected 2026-10-02, OPUS: `00387740`–`00387759`)*) |"),
    (S32, "| 6 | Doom | — (count 10) |",
     "| 6 | Doom | — (count ~~10~~ 11 stored, shown as 10 *(corrected 2026-10-02, OPUS: `00387740`–`00387759`)*) |"),

    # C17: +6 bit 0x20 is on exactly fourteen statuses, not every buff (checked against status_data.bin).
    (S32, "`+0x06`..`+0x07` is a flag word with `0x0020` on every buff,",
     "`+0x06`..`+0x07` is a flag word with ~~`0x0020` on every buff~~ `0x0020` (bit 5) on exactly fourteen rows — "
     "Stop, Sleep, Confuse, Lure, Protect, Shell, Haste, Bravery, Faith, Reflect, Invisible, Regen, Float and "
     "Bubble — and not on Berserk (`0x0040`) or Libra (`0x0100`) *(corrected 2026-10-02, OPUS: checked against "
     "`status_data.bin`; CONTRACT-status-write.md §4, invariant 3)*,"),

    # C18: "Vanish" for id 31; bank 5 names id 31 X-Zone (bit 5's "Vanish" is id 24, Invisible).
    (MP, "- **KO, Stone and Vanish stop passive recovery**",
     "- **KO, Stone and ~~Vanish~~ X-Zone stop passive recovery** *(corrected 2026-10-02, OPUS: the predicate is "
     "`0x80000003`, ids 0, 1 and 31; id 31 is X-Zone in the thirty-two statuses §2, and \"Vanish\" there is id 24, "
     "Invisible)*"),
    (MP, "the KO / Stone / Vanish predicate from",
     "the KO / Stone / ~~Vanish~~ X-Zone (id 31) *(corrected 2026-10-02, OPUS)* predicate from"),
    (CSW, "| 6 | `0030E85E` | **31** Vanished |",
     "| 6 | `0030E85E` | **31** ~~Vanished~~ X-Zone *(corrected 2026-10-02, OPUS: id 31 is X-Zone in the "
     "thirty-two statuses §2; \"Vanish\" is id 24, Invisible)* |"),

    # C19: kind 0 is the party-definition-table record (MP CS-6, PT AL-3, C-ASR §7); 02EBF130 is the party table.
    (CASR, "- **Foe arm** (`b[rec+5]==0`):",
     "- **~~Foe arm~~ Kind-0 (party-table) arm** (`b[rec+5]==0`) *(corrected 2026-10-02, OPUS: kind 0 is the "
     "record of the 40-row party definition table `02EBF130`, byte `+4` its row — where-mp-comes-from.md §5 CS-6; "
     "kind 1 is the spawn-backed, enemy-table record — §7 here and the periodic tick §13; the `foed` / `memd` "
     "labels in this block follow the struck reading and are not re-checked here)*:"),
    (CASR, "- **Member arm** (`b[rec+5]==1`):",
     "- **~~Member arm~~ Kind-1 (spawn-backed) arm** (`b[rec+5]==1`) *(corrected 2026-10-02, OPUS: see the kind-0 "
     "arm above)*:"),
    (CASR, "kind-2 is the\n**FOED** descriptor `q[02EBF130]` — the foe-table range bound,",
     "kind-2 is the\n~~**FOED** descriptor `q[02EBF130]` — the foe-table range bound,~~ descriptor `q[02EBF130]`, the range bound "
     "of the 40-row party definition table *(corrected 2026-10-02, OPUS: where-mp-comes-from.md §5 CS-6 — a "
     "kind-0 record's byte `+4` is its row)*,"),

    # C20: 002FA560 is the MMSG text-bank switch (GE-1) with 28 cases 0..0x1B (pass 22); checked at 002FA560 / 002F7800.
    (S32, "`002FA560` (476 B) is the status-handler dispatch:",
     "`002FA560` (476 B) is ~~the status-handler dispatch~~ the MMSG text-bank switch of §4 `GE-1` *(corrected "
     "2026-10-02, OPUS: checked at `002FA560` and `002F7800`, which sets `ecx = 0xC`, stores `02EC3DE0` and jumps "
     "to `00238640`)*:"),
    (S32, "out-of-range returns - the effect-id to executor switch the statuses callers share.",
     "out-of-range returns ~~- the effect-id to executor switch the statuses callers share~~ - a bank selector, "
     "not an effect-id executor switch *(corrected 2026-10-02, OPUS)*."),
    (S32, "`002F7800` is one of **27 sibling stubs** (`002F7680`–`002F79C0`, `0x20` stride,\n        one per bank 1–27",
     "`002F7800` is one of ~~**27 sibling stubs** (`002F7680`–`002F79C0`, `0x20` stride,\n        one per bank 1–27~~ "
     "**28 case bodies** (`002F7660`–`002F79C0`, one per bank `0..0x1B`: case 0 → `002F7660`, case 4 → "
     "`002F7680`, … *(corrected 2026-10-02, OPUS: checked at `002FA560`, as pass 22 below reads it)*"),

    # C21: 0030AB40 returns (computed == expected) + 1, in {1,2} (C-ASR 13f, EXP-197).
    (CPT, "- What values above 1 `0030AB40` returns — this caller reduces it to `> 1`, which constrains `Z-13`\n"
          "  without answering it.",
     "- ~~What values above 1 `0030AB40` returns — this caller reduces it to `> 1`, which constrains `Z-13`\n"
     "  without answering it.~~ *(answered: see CONTRACT-auto-status-rebuild.md §13f, EXP-197 — `0030AB40` returns "
     "`(computed == expected) + 1`, 1 or 2; 2026-10-02, OPUS)*"),
    (PT, "so **whatever\nvalues above 1 exist, this caller only distinguishes \"1 or less\" from \"more than 1.\"** That is a\n"
         "constraint on Z-13 from a second subsystem, not an answer to it.",
     "so ~~**whatever\nvalues above 1 exist, this caller only distinguishes \"1 or less\" from \"more than 1.\"** That is a\n"
     "constraint on Z-13 from a second subsystem, not an answer to it.~~ `> 1` means the classifier returned 2 "
     "*(answered: see CONTRACT-auto-status-rebuild.md §13f, EXP-197 — it returns `(computed == expected) + 1`, 1 or "
     "2; 2026-10-02, OPUS)*."),

    # C22: byte[stats+0x1C2] is the unit level (SW 2.4a; C-ASR 13al).
    (CPT, "- What `byte[stats + 0x1C2]` is — it bounds Regen's random heal and divides without a guard in that\n"
          "  arm. Named here as a field, not as a meaning.",
     "- ~~What `byte[stats + 0x1C2]` is~~ *(answered: see the status write §2.4a — `(rand % level) + 1`, the unit "
     "level at `+0x1C2` — and CONTRACT-auto-status-rebuild.md §13al; 2026-10-02, OPUS)* — it bounds Regen's random "
     "heal and divides without a guard in that\n  arm. ~~Named here as a field, not as a meaning.~~"),

    # C23: r14 is zero on the rebuild's fallback paths (0030FF07 xor r14d, r14d; 003100DF, 0031018F).
    (CASR, "gate call. What `r14` holds at that point was not established.",
     "gate call. ~~What `r14` holds at that point was not established.~~ *(answered: `r14` is zero there — "
     "`0030FF07 xor r14d, r14d`, used at `003100DF` / `0031018F` — and §13's table shows the gate receiving row "
     "address 0; 2026-10-02, OPUS)*"),
    (CASR, "- What `r14` holds on the fallback paths.",
     "- ~~What `r14` holds on the fallback paths.~~ *(answered: zero — `0030FF07 xor r14d, r14d`; see §10 and §13; "
     "2026-10-02, OPUS)*"),

    # C24: with the applier real, +0x78 equals the accumulation on return (C-ASR 4, 2026-09-25).
    (CASR, "| `+0x78` holds the accumulation afterwards | **nothing writes it back**;",
     "| `+0x78` holds the accumulation afterwards | ~~**nothing writes it back**~~ this function's own instructions "
     "do not write it back, but the applier `0030E130` does, so `+0x78` equals the accumulation on return "
     "*(corrected 2026-10-02, OPUS: this run scripted `0030E130`; §4, 2026-09-25)*;"),
    (CASR, "| nothing writes the accumulation back into +0x78 |",
     "| ~~nothing writes the accumulation back into +0x78~~ this function's own instructions do not write the "
     "accumulation back into +0x78; the applier `0030E130` does, so `+0x78` equals it on return *(corrected "
     "2026-10-02, OPUS: §4, 2026-09-25)* |"),

    # C25: the rebuild was executed (isolated original-code under Unicorn, 13 and 13ak).
    (CASR, "them.\n**This function has never been executed** (§13), so no row claims more than static evidence.",
     "them.\n~~**This function has never been executed** (§13), so no row claims more than static evidence.~~ The function "
     "has been executed as isolated original code under Unicorn (§13, 2026-09-12; §13ak, EXP-228); each row's tier "
     "says what its evidence is, and none is live *(corrected 2026-10-02, OPUS)*."),
    (CASR, "image — nothing here has\nbeen executed (§13).",
     "image — ~~nothing here has\nbeen executed (§13).~~ *(answered: see §13 — the whole function ran as isolated original "
     "code under Unicorn, and §13ak re-ran it, EXP-228; 2026-10-02, OPUS)*"),

    # C26: the apply-tail calls run from shipped bytes (13b, 13d).
    (CASR, "`0030E060` — were not read, so *\"no stat work happens anywhere in `0030FED0`\"* is **not** claimed;",
     "`0030E060` — ~~were not read, so *\"no stat work happens anywhere in `0030FED0`\"* is **not** claimed;~~ have "
     "since run from shipped bytes, and `002FEF30` is the derived-stat rebuild of `rec+0x24..0x47`, so stat work "
     "does happen in `0030FED0`, through that call at `003103AD` *(answered: see §13b, §13d and §13al; 2026-10-02, "
     "OPUS)*;"),
    (CASR, "- The four calls in the apply tail: `0030E130` (specified only by its two argument shapes here) and\n"
           "  `0030E060`.",
     "- ~~The four calls in the apply tail: `0030E130` (specified only by its two argument shapes here) and~~\n"
     "  ~~`0030E060`.~~ *(answered: see §13d — APPLY `0030E130` and TAIL `0030E060` run from shipped bytes; "
     "2026-10-02, OPUS)*"),
    (CASR, "`00307D10`) still scripted and therefore still owed.",
     "`00307D10`) ~~still scripted and therefore still owed.~~ *(answered: see §13d — SINK `00307D10` and RESET `003105D0` run "
     "from shipped bytes too; 2026-10-02, OPUS)*"),

    # C27: the stat contribution lives in 002FEF30, called by 0030FED0 at 003103AD (13al, 7).
    (CASR, "- Where the **stat** contribution lives, if the referenced page's description is accurate.",
     "- ~~Where the **stat** contribution lives, if the referenced page's description is accurate.~~ *(answered: "
     "see §13al and §7 — `002FEF30`, called by `0030FED0` at `003103AD`, zeroes and rebuilds `rec+0x24..0x47`; "
     "2026-10-02, OPUS)*"),
    (CASR, "§1: this function does not compute a stat\ncontribution, and a reader sent to it for one will not find it.",
     "§1: ~~this function does not compute a stat\ncontribution, and a reader sent to it for one will not find it.~~ "
     "this function's own loops compute no stat contribution, but its call to `002FEF30` at `003103AD` rebuilds the "
     "derived stats `rec+0x24..0x47` *(corrected 2026-10-02, OPUS: §13al and §7)*."),

    # C28: both siblings fault on the null table (REFUTED 2026-09-16); not only memset is scripted (2026-09-25).
    (CSW, "| the timer default faults when the table is absent while the cascade degrades |",
     "| the timer default faults when the table is absent ~~while the cascade degrades~~ and so does the cascade "
     "(`0030E686`–`0030E68A`) *(corrected 2026-10-02, OPUS: §10's REFUTED note of 2026-09-16)* |"),
    (CSW, "155 cases, 0 mismatches, only `memset` scripted |",
     "155 cases, 0 mismatches, ~~only `memset` scripted~~ not only `memset` scripted *(corrected 2026-10-02, OPUS: "
     "§13, 2026-09-25)* |"),

    # C29: the tick does not call the status write (00310DB0 has no call to 0030E360).
    (CSW, "from the HP write's lethal transition, and\nfrom the tick.",
     "from the HP write's lethal transition~~, and\nfrom the tick~~ *(corrected 2026-10-02, OPUS: `00310DB0` has no "
     "call to `0030E360`; the two meet only at `003112F0`, CONTRACT-periodic-tick.md §6, and §6's caller list here "
     "has no tick)*."),

    # C30: GA-1 answered 2026-09-27: +0x11, +0x12, +0x14..+0x1D are read by no code.
    (S32, "Still open: what the twelve rankings rank, a reader that resolves class 26 without naming the slot, and "
          "which on-screen list each key kind drives.",
     "~~Still open: what the twelve rankings rank, a reader that resolves class 26 without naming the slot, and~~ "
     "*(answered: see GA-1 at the top of §4, 2026-09-27 — the band is read by no code, authored and unread; "
     "2026-10-02, OPUS)* Still open: which on-screen list each key kind drives."),
    (S32, "offered.\n      **Still open: `+0x11` … `+0x25`**, twenty-one bytes per row.",
     "offered.\n      ~~**Still open: `+0x11` … `+0x25`**, twenty-one bytes per row.~~ *(answered: see GA-1 at the top of §4 — "
     "`+0x11`, `+0x12` and `+0x14`–`+0x1D` are read by no code, and the narrowings below decode the rest; "
     "2026-10-02, OPUS)*"),
    (S32, "eighteen-body result bounds where a consumer is not, it does not prove there is none.**",
     "eighteen-body result bounds where a consumer is not~~, it does not prove there is none~~.** *(answered: see "
     "GA-1 at the top of §4 — the later census of 44 status rows across the 18 users of the slot finds no reader "
     "of `+0x11`, `+0x12`, `+0x14`–`+0x1D`; 2026-10-02, OPUS)*"),
    (S32, "- `+0x11`–`+0x1D`, which none of these readers touch, stay open.",
     "- `+0x11`–`+0x1D`, which none of these readers touch, ~~stay open~~ are read by no code *(answered: see "
     "GA-1 at the top of §4; 2026-10-02, OPUS)*."),

    # C31: SW-3 is stale against the readers the thirty-two statuses page found.
    (CSW, "shipped table. Only `+0x20` has a known consumer (calculator slot 118's exclusion test).",
     "shipped table. ~~Only `+0x20` has a known consumer (calculator slot 118's exclusion test).~~ *(answered: see "
     "the-thirty-two-statuses.md §4 — the query arm copies `+0x10`, `+0x26`, `+0x27` and `+0x13` into its record, "
     "and `+0x02` and `+0x24` are read too; `+0x20` remains calculator slot 118's exclusion test; 2026-10-02, "
     "OPUS)*"),

    # C32: stage 2 reads the status words of the stats record, not the unit.
    (PT, "It reads the combined status words\n`[unit+0x3C] | [unit+0x64]`, and per status",
     "It reads the combined status words\n~~`[unit+0x3C] | [unit+0x64]`~~ `[stats+0x3C] | [stats+0x64]` of the "
     "stats record, not the unit *(corrected 2026-10-02, OPUS: \"Still not established\" below and "
     "CONTRACT-periodic-tick.md §5)*, and per status"),
    (PT, "; rsi = the UNIT\n00386DC0",
     "; rsi = the UNIT  <- corrected 2026-10-02, OPUS: rsi is the stats record, not the unit (see below)\n00386DC0"),
    (PT, "; the unit's two status words\n0030E410",
     "; the unit's two status words  <- corrected 2026-10-02, OPUS: rsi is the target's stats record, which holds them (§13)\n0030E410"),

    # C33: +0x28 is max MP, resolved 2026-09-11.
    (PT, "drain. **What the field at `+0x28` is has not been\nestablished**, so \"one-fiftieth of *what*\" is not claimed here.",
     "drain. ~~**What the field at `+0x28` is has not been\nestablished**, so \"one-fiftieth of *what*\" is not claimed here.~~ "
     "*(answered: see §10 and §13 \"Still not established\" — the base is the stats record and `+0x28` is max MP, "
     "resolved 2026-09-11; 2026-10-02, OPUS)*"),
    (PT, "observed live. `+0x28` — \"one-fiftieth of *what*\" —\nremains unestablished, as §5 says;",
     "observed live. ~~`+0x28` — \"one-fiftieth of *what*\" —\nremains unestablished, as §5 says;~~ *(answered: `+0x28` is max MP — "
     "see §10 and §13, resolved 2026-09-11; 2026-10-02, OPUS)*;"),

    # C34: SW's own "not read" labels, answered by FA-1 / FA-2 (2026-09-12), 2.7a and the 0x217 note.
    (SW, "645 B)\nis not read here (`FA-1`).",
     "645 B)\n~~is not read here (`FA-1`).~~ *(answered: see §2.4a and §7 `FA-1` — the default duration; 2026-10-02, OPUS)*"),
    (SW, "`+0x50`. What reads `+0xBC` and `+0x13C` is `FA-2`.",
     "`+0x50`. ~~What reads `+0xBC` and `+0x13C` is `FA-2`.~~ *(answered: see §2.4a and §7 `FA-2` — the periodic tick's "
     "stage 2, `00386C70`; 2026-10-02, OPUS)*"),
    (SW, "| the defeat-condition predicates and the two unread steps |",
     "| the defeat-condition predicates and the two ~~unread~~ steps *(answered: see §2.7a; 2026-10-02, OPUS)* |"),
    (SW, "`BattleStats_RemoveStatusesFromMaskAndRecompute` — a caller, unread |",
     "`BattleStats_RemoveStatusesFromMaskAndRecompute` — a caller, ~~unread~~ *(answered: see §4 — it passes the "
     "flags literal `0x217` at `0030F721` and recomputes once itself; 2026-10-02, OPUS)* |"),

    # C35: what the two builders do is established (2.6 row 1; C-SW SW-2 answered 2026-09-12).
    (SW, "| What the two builders do beyond the initialiser | **not established** | — | UNKNOWN |",
     "| What the two builders do beyond the initialiser | ~~**not established**~~ the add builder clears `+0x2C` bit "
     "0; the remove builder, for status 28 with HP non-zero, sets `0x108` and halves HP into `+0x24` (§2.6 row 1) "
     "— `00386A50`, `00386A70`, executed in CONTRACT-status-write.md §13 *(corrected 2026-10-02, OPUS: checked at "
     "`00386A70`; CONTRACT-status-write.md `SW-2`, answered 2026-09-12)* | ~~—~~ 1 | ~~UNKNOWN~~ PROVEN |"),

    # C36: status 28 is Bubble (the thirty-two statuses, row 28).
    (SW, "and the name is still not attached here (`EY-1`) |",
     "~~and the name is still not attached here (`EY-1`)~~ and status 28 is **Bubble** *(answered: see the "
     "thirty-two statuses §2, row 28; 2026-10-02, OPUS)* |"),
    (SW, "says. `EY-1` remains open.",
     "says. ~~`EY-1` remains open.~~ *(answered: status 28 is Bubble — see the thirty-two statuses §2, row 28; "
     "2026-10-02, OPUS)*"),

    # C37: the shortcut is the Esper one; a party member takes the full path (C-SW 10 row 3, corrected 2026-09-26).
    (R, "the gates, the party-side\n  terminal shortcut,",
     "the gates, the ~~party-side\n  terminal shortcut~~ Esper terminal shortcut *(corrected 2026-10-02, OPUS: a "
     "party member takes the full path; only a summoned Esper, type `0x1B..0x27`, is short-cut — "
     "CONTRACT-status-write.md §10 row 3)*,"),
    (SW, "### 2.2 The gates, and the party-side shortcut",
     "### 2.2 The gates, and the ~~party-side~~ Esper shortcut *(corrected 2026-10-02, OPUS)*"),
    (SW, "- **the party-side shortcut**: a target unit",
     "- **the ~~party-side~~ Esper shortcut** *(corrected 2026-10-02, OPUS: type `0x1B..0x27` is the thirteen "
     "Esper rows; §1 and CONTRACT-status-write.md §10 row 3)*: a target unit"),
    (SW, "**The party shortcut**:",
     "**The ~~party~~ Esper shortcut** *(corrected 2026-10-02, OPUS: §2.2)*:"),
    (CSW, "the party collecting rewards (foe) or not (party-side);",
     "the party collecting rewards (foe) or not (~~party-side~~ a summoned Esper; a party member takes the full "
     "path of reaction, defeat and rewards, §10 row 3 *(corrected 2026-10-02, OPUS)*);"),
    (CSW, "| the party-side shortcut, the gates",
     "| the ~~party-side~~ Esper shortcut *(corrected 2026-10-02, OPUS: §10 row 3)*, the gates"),

    # C38: the shared tail 0030E816 runs the recompute unless flags bit 9 (0030E816-0030E828).
    (SW, "| all others | `0030E816` | nothing |",
     "| all others | `0030E816` | ~~nothing~~ the shared tail: `0030FED0` runs unless `flags` bit 9 is set "
     "*(corrected 2026-10-02, OPUS: `0030E816`–`0030E828`; \"Falsification pass 1\" below)* |"),
    (CSW, "| 7 | `0030E816` | the other 24 | nothing |",
     "| 7 | `0030E816` | the other 24 | ~~nothing~~ the shared tail only: `0030FED0` unless `flags` bit 9 "
     "*(corrected 2026-10-02, OPUS: `0030E816`–`0030E828`; §15a)* |"),

    # C39: 0046AB10 is the battle event poster, not a periodic-effect spawn.
    (PT, "`0046AB10(unit, 0x4E, &block)` — the kind-8 periodic-effect spawn |",
     "`0046AB10(unit, 0x4E, &block)` — ~~the kind-8 periodic-effect spawn~~ a post through the battle event "
     "poster *(corrected 2026-10-02, OPUS: the status write §2.6 row 5 names `0046AB10` the battle event poster; "
     "§13 \"Still not established\" ties category 8 to the post-result \"steals your loot\" message)* |"),

    # C40: 002ECEC0 is read (SW interior citation, 2026-09-18).
    (SW, "What `003E6B40` and `002ECEC0` do on the render record and the actor is not read.",
     "What `003E6B40` ~~and `002ECEC0` do~~ does on the render record ~~and the actor~~ is not read *(`002ECEC0` "
     "answered: see \"Interior citation — frontier hub `002ECEC0`\" below, 2026-09-18 — a context-to-render-record "
     "resolve that tails to `003AEEF0`; 2026-10-02, OPUS)*."),
    (SW, "What remains open under that id is only `003E6B40` / `002ECEC0`, as §7 already",
     "What remains open under that id is only `003E6B40` ~~/ `002ECEC0`~~ *(`002ECEC0` answered: see \"Interior "
     "citation — frontier hub `002ECEC0`\" below; 2026-10-02, OPUS)*, as §7 already"),

    # C41: every 5 item of the MP page is ticked.
    (MP, "re-censused; and the four functions\nlisted as unread in §5, which remain unread.",
     "re-censused; ~~and the four functions\nlisted as unread in §5, which remain unread.~~ *(answered: see §5 — every item there "
     "is ticked, CS-1 to CS-6 and FV-4 among them; 2026-10-02, OPUS)*"),

    # C42: README labels against the pages' own front matter, and the six pages it omitted.
    (R, "terminal table, and the defeat cleanup with its four `02089340` latches - **DOCUMENTED**",
     "terminal table, and the defeat cleanup with its four `02089340` latches - ~~**DOCUMENTED**~~ **AUDITED** "
     "*(corrected 2026-10-02, OPUS: the page's front matter says `status: AUDITED`)*"),
    (R, "where the database has read the engine acting on each - **DOCUMENTED**",
     "where the database has read the engine acting on each - ~~**DOCUMENTED**~~ **AUDITED** *(corrected "
     "2026-10-02, OPUS: the page's front matter says `status: AUDITED`)*\n\n"
     "- [`where-mp-comes-from.md`](where-mp-comes-from.md) - MP gain, walk recovery, cost and Mist Charges - "
     "**AUDITED**\n\n"
     "- [`Periodic-Tick/what-the-periodic-tick-does.md`](Periodic-Tick/what-the-periodic-tick-does.md) - the gated "
     "per-unit tick and its five-stage result builder - **AUDITED**\n\n"
     "- Contracts: [`CONTRACT-status-write.md`](CONTRACT-status-write.md), "
     "[`CONTRACT-effect-layers.md`](CONTRACT-effect-layers.md) and "
     "[`CONTRACT-periodic-tick.md`](CONTRACT-periodic-tick.md) - **CONTRACT READY**; "
     "[`CONTRACT-auto-status-rebuild.md`](CONTRACT-auto-status-rebuild.md) - **BEHAVIORALLY UNDERSTOOD** *(six "
     "pages added to this list 2026-10-02, OPUS, each with the status its front matter states)*"),
    (R, "- Periodic/tick effect processing",
     "- ~~Periodic/tick effect processing~~ *(now documented: the periodic tick page and its contract, listed above; "
     "2026-10-02, OPUS)*"),
    (R, "- Status side effects processed by `0030E130`",
     "- ~~Status side effects processed by `0030E130`~~ *(now documented: two-layer-effect-model.md §11 reads the "
     "body and CONTRACT-effect-layers.md specifies it; 2026-10-02, OPUS)*"),

    # C43: listhelp_status.bin has 34 offsets (entry 0 not a string); the three codes were decoded 2026-09-15.
    (S32, "120,031, 33 string offsets from +0xAC of which entries 1-32 are the statuses in id order and 33 is empty",
     "120,031, ~~33 string offsets from +0xAC of which entries 1-32 are the statuses in id order and 33 is empty~~ 34 u32 "
     "offsets from +0xAC, entry 0 not a string, entries 1-32 the statuses in id order and entry 33 empty "
     "(corrected 2026-10-02, OPUS, as the evidence table and section 9 count them)"),
    (S32, "three codes are left undecoded below (`<85>` where a count would print, `<AE>` / `<AF>` around "
          "*Requires the proper license*) |",
     "~~three codes are left undecoded below (`<85>` where a count would print, `<AE>` / `<AF>` around "
     "*Requires the proper license*)~~ the three codes are decoded in §3 and §4 `GA-2` (2026-09-15): `<85>` is the "
     "digit 0, `<AE>` / `<AF>` are `(` / `)` *(corrected 2026-10-02, OPUS)* |"),

    # C44: the read is of the +0x0A word ([rsi + 0x0A] at 0031E288).
    (S32, "(the page locates the read of the status row's `+0x0B` word inside it)",
     "(the page locates the read of the status row's ~~`+0x0B`~~ `+0x0A` word inside it — `[rsi + 0x0A]` at "
     "`0031E288`, §4 *(corrected 2026-10-02, OPUS)*)"),

    # C45: 229E40 reads d[01E02814], per 13t's correction of record.
    (CASR, "`d[01E02E14]==7 ? 0x1A : int(24ABA0·10.0)` for tag 7",
     "~~`d[01E02E14]==7 ? 0x1A : int(24ABA0·10.0)`~~ `d[01E02814]==7 ? 0x1A : int(24ABA0·10.0)` *(corrected "
     "2026-10-02, OPUS: §13t's correction of record — `229E40` reads `d[01E02814]`)* for tag 7"),

    # C46: heading counts against their own lists.
    (MP, "### Five new entries for the effect namespace",
     "### ~~Five~~ Nine new entries for the effect namespace *(count corrected 2026-10-02, OPUS: the table has nine rows)*"),
    (CASR, "### Four things the static read got wrong, and the run found",
     "### ~~Four~~ Five things the static read got wrong, and the run found *(count corrected 2026-10-02, OPUS: five "
     "rows, as the paragraph after the table says)*"),
    (CASR, "**Four\nmore were wrong, and only executing them showed it:**",
     "**~~Four~~ Five\nmore were wrong, and only executing them showed it:**"),
    (CASR, "## 7a. And then it keeps going — four stages this contract did not have",
     "## 7a. And then it keeps going — ~~four~~ three stages this contract did not have *(count corrected "
     "2026-10-02, OPUS: three numbered items follow)*"),

    # F1 (2.5): stage 5 overwrites result +0x24 (00386A23 mov [r13+0x24], edx) and can write 0 (003869AF jl 003869EB).
    (PT, "and **stages 2, 4 and 5 all add into it**; stage 3 never does.",
     "and ~~**stages 2, 4 and 5 all add into it**~~ **stages 2 and 4 add into it and stage 5 overwrites it**: "
     "`00386A23 mov dword ptr [r13 + 0x24], edx` whenever its gates pass and the counter is a multiple of "
     "`fb × 30`, storing 0 when the beat count is below 10 (`003869AF jl 003869EB`), so the stage order matters "
     "for `+0x24` *(corrected 2026-10-02, OPUS: checked at `00386A23`)*; stage 3 never does."),
    (PT, "| 5 — `BuildRuntimeCounterPeriodicHpCredit` | **no** | none | **yes** |",
     "| 5 — `BuildRuntimeCounterPeriodicHpCredit` | **no** | none | ~~**yes**~~ **overwrites** it (`00386A23`) "
     "*(corrected 2026-10-02, OPUS)* |"),
    (PT, "and stages 2 and 5 accumulate the HP delta besides.",
     "and stages 2 and 5 ~~accumulate~~ write the HP delta besides, stage 5 by overwriting it (`00386A23`) "
     "*(corrected 2026-10-02, OPUS)*."),
    (CPT, "/ `+0x140`. Three stages\nadd to one accumulator, and the sum does not depend on the order in which they do — *but the\n"
          "generator's stream position does*,",
     "/ `+0x140`. ~~Three stages\nadd to one accumulator, and the sum does not depend on the order in which they do — *but the\n"
     "generator's stream position does*,~~ Stages 2 and 4 add to the accumulator and stage 5 overwrites it "
     "(`00386A23 mov dword ptr [r13 + 0x24], edx`, which can store 0: `003869AF jl 003869EB`), so the order "
     "matters for `+0x24` — *and so does the generator's stream position* *(corrected 2026-10-02, OPUS: checked at "
     "`00386A23`)*,"),
    (CPT, "may not reorder the stages even though the arithmetic would survive it.**",
     "may not reorder the stages~~ even though the arithmetic would survive it~~.** *(The arithmetic would not "
     "survive it either: stage 5 overwrites `+0x24`; corrected 2026-10-02, OPUS.)*"),

    # F2 (2.5): the "index 0x14" is a raw pointer value (003868BD mov ebx, 0x14; read at 003869A2).
    (PT, "`+0xEA9`, `0x14` when no owning unit is found",
     "`+0xEA9`, ~~`0x14` when no owning unit is found~~ and, when no owning unit is found, the raw address `0x14` as the "
     "record pointer, not an index (`003868BD mov ebx, 0x14`, read by `movzx eax, word ptr [rbx]` at `003869A2`) "
     "*(corrected 2026-10-02, OPUS)*"),
    (PT, "index `0x14` when no owner (`003868BD`) |",
     "~~index `0x14`~~ the raw pointer value `0x14`, not an index, when no owner (`003868BD`; read through at "
     "`003869A2`) *(corrected 2026-10-02, OPUS)* |"),
]


def main():
    apply = "--apply" in sys.argv
    fails = 0
    texts = {}
    for rel, old, new in EDITS:
        t = texts.get(rel) or open(os.path.join(DB, rel), "rb").read().decode("utf-8")
        if new in t or new.replace("\n", "\r\n") in t:
            print("ALREADY", rel.split("/")[-1]); texts[rel] = t; continue
        hit = [c for c in (old, old.replace("\n", "\r\n")) if t.count(c) == 1]
        if not hit:
            print("REFUSING", rel.split("/")[-1], old[:40]); fails += 1; texts[rel] = t; continue
        n = new.replace("\n", "\r\n") if "\r\n" in hit[0] else new
        texts[rel] = t.replace(hit[0], n, 1)
        print(("PATCHED " if apply else "WOULD PATCH ") + rel.split("/")[-1])
    if apply and not fails:
        for rel, t in texts.items():
            open(os.path.join(DB, rel), "wb").write(t.encode("utf-8"))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
