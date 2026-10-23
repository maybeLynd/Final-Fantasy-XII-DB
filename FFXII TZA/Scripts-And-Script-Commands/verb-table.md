---
title: "Script verb table: every call id with its name, callbacks, shape, argument count, what it reaches and how often the shipped scripts use it"
kind: "reference"
category: "Scripts and script commands"
addresses: "0x01EED700, 0x01F281B0, 0x01F29418, 0x01F29440, 0x01F26720, 0x0016D6A0, 0x005C5230, 0x00267E10, 0x00267DB0, 0x0026B4E0, 0x00263D00, 0x00355940, 0x00355E80, 0x0050C910"
---

## What it lists

One row per command record in the five command tables the verb dispatcher reads: 1,496 in family
0, 147 in family 3, 1 in family 5, 104 in family 7 and 212 in the shared table that family 2's
debug verbs and eleven aliased families use. The callbacks are read from the shipping executable
at `table + 8 + 32 × command`; the names come from the ff12-script catalogue where it has one, and
from other authored sources otherwise; the argument counts are measured on the handler bodies.

## Columns

| Column | Meaning |
|---|---|
| `call_id` | the sixteen-bit id a script instruction carries: `family << 12 \| command` |
| `family`, `command` | the two halves |
| `verb` | the authored name; `unkCall_xxx` is the catalogue's own placeholder |
| `name_source` | `catalogue` for the ff12-script list, `other` for a name from another authored source, empty when none |
| `cat_args`, `cat_ret`, `cat_act`, `param_types` | the catalogue's declared argument count, whether it returns a value, whether it takes an actor, and its parameter type bytes; blank when the name is not the catalogue's |
| `begin`, `poll`, `result` | the three callbacks of the record, empty when null |
| `stub` | which of `begin` and `result` holds the bare `ret` at `0x0016D6A0` |
| `shape` | which callbacks the record has, the `ret` stub not counting: `result`, `begin+poll`, `begin`, `begin+poll+result`, `poll`, `poll+result`, `begin+result`, `empty`, or `stub` when nothing but the stub and the zero-returning poll `0x005C5230` is left; that poll counts as a poll in every other shape, as it does in the population table of [native commands](native-commands.md) |
| `arg_callback` | the callback that pops the arguments (`begin` or `result`); blank when that callback is the stub or the record is empty |
| `pops_int`, `pops_float`, `pushes`, `result_writes` | counted direct calls of `0x00267E10`, `0x00267DB0`, the two push helpers and the two result writers in that callback; a handler that pushes constants and delegates to a shared body pops there, so these are not the argument count, which `arity` carries |
| `guard` | the predicate that makes a pop conditional, where one exists (`0x00263D00` for the class-3 forms) |
| `arity`, `arity_status`, `net_or_sums` | the measured argument count; `CONFIRMED` equals the catalogue, `CONFLICT` differs from it, `DERIVED` has no catalogue value, `GUARDED` and `CONDITIONAL` take two values (`lo\|hi`) depending on the guard |
| `result_body` | the result handler's control flow: `CONST`, `TAILJUMP`, `CALL1`, `LINEAR` (several calls, no branch) or `BRANCHING`; carried over from the earlier census, not re-measured for this table |
| `reach` | the engine subsystems the callbacks call directly, with hit counts, ignoring helpers with more than twenty callers; carried over from the earlier call-graph map |
| `us_calls` | calls of the verb in the 1,114 decompiled US scripts; a script function that shares a verb's name (`function mapjump(`) is not a call |

## Data

| Fact | Value |
|---|---|
| rows | 1,960 |
| shapes | result only 1,571; begin and poll 202; begin only 76; all three 48; poll only 28; poll and result 6; begin and result 1; stub 24; empty 4 |
| names | 1,270 from the catalogue (54 of them `unkCall` placeholders), 671 from other sources, 19 without a name (the 19 `DERIVED-UNNAMED` rows) |
| argument count | 1,229 confirmed against the catalogue, 653 derived, 34 guarded, 24 conditional, 19 derived without a name, 1 conflict |
| the conflict | `unkCall_5c7` (`0x05C7`): the catalogue declares two arguments, the result is the `ret` stub and pops none |
| verbs called in the US corpus | 1,135 of 1,960; 1,843,441 calls in all |
| most called | `setmapidfloor` 84,066; `wait` 83,795; `setmapidwall` 76,134; `nowmap` 63,695 |
| `setforcefightmode` (`0x0334`) | 177 calls in 83 scripts, every one `setforcefightmode(0)` |
| the four empty records | `setnorecovertelepostatus` `0x0330`, `battlemembersync` `0x0356`, `restartbattle` `0x03B0`, `debug_meswin_3e` `0x203E`; none is called in the corpus |

The poll-only rows are the waits on something an earlier verb started: `movesync`, `turnsync`,
`stdmotionreadsync`, `crossfadesync`, `gaugeshowsync`, `resumebehindcamerasync`,
`summonreadsync`, `summontopartyreadsync`, `behindcamerafovyrollsync`, `vibsync`, `lookatsync`,
`spattackwindowsync`, `actoriopvoicereadsync`, `entryreadsync`, `behindtoeventcamerasync`,
`moviestandbysync`, `movieplaysync`, `bgmstreamreadsync`, `bgmstreamplaysync`, `gillwinsync`,
`ucmovesync`, `initsync`, `musicfadeoutsync`, `unkCall_5a6`, `fsmenu_syncopenchip`,
`fsttl_opencommandsync` and `fsttl_closecommandsync`.

`moveblurfadesync` (`0x03BD`) also counts as poll only: its begin and result are the stub and its
poll `0x00345100` is live.

The stub rows hold only the `ret` at `0x0016D6A0` and the poll `0x005C5230`, which returns 0, so a
stubbed verb completes on its first call: `disposesummon`, `changetonormalparty`, `hddinstall`,
`networkhddinstall`, `hddmount`, `atrac3cancel`, `btlAtelRemoveAllEquip` and the debug verb
`0x20D3` have a stub begin with that poll; `atrac3standbysync` and `atrac3playsync` have that poll
alone; `atrac3play`, `unkCall_5c7`, `btlAtelSetUnique`, `btlAtelChangeAllBtlCharaFlag_DontMoveDebug`,
the tag and setup verbs `0x3054` to `0x305A` and seven debug verbs have a stub result.

Two placeholder names have a known meaning: `unkCall_5be` (`0x05BE`, start `0x00355940`) returns the
after-load flag `0x0209AC10` through `0x00286000`, and `unkCall_5bf` (`0x05BF`, start `0x00355E80`)
clears it through `0x00287D00`; in the US corpus only the Trial Mode map scripts (`tri_a01` to `tri_b05`
and their siblings, 100 files) call them, 200 and 100 times. `debug_setfightstatusbyevent`
(`0x206B`, `0x0050C910`) pops one int and stores it through `0x003BA300`, so its argument count is 1.

### Helpers behind the handlers

Several handlers do their work through small helpers. An actor's presentation binding is `[actor + 0xC0]`;
its first word is the render index, -1 when the actor has no model.

| Helper | Verbs | Does |
|---|---|---|
| `0x002E7DD0(actor, run)`, `0x002E7E10(actor, run)` | `getdefaultwalkthresholdspeed` `0x0272`, `getdefaultrunspeed` `0x0246` | the model parameter (`0x003E6150`) `0x09000707`, or `0x09000101` for a non-zero second argument; and `0x09000808` or `0x09000202`; 0 without a model |
| `0x002E9B10(actor)` | `raturn` `0x025D`, `raturna` `0x025F`, `raturnya` `0x02D5` and their relatives | the model parameter `0x09000909`, or pi/30 (`0x00D0F8E4`) without a model |
| `0x002E30D0(actor, on, a, b)` | `unkCall_5bd` `0x05BD` | `0x00382B50(render index, a, b)`, or `0x00382B50(-1, 0, 0)` when `on` is 0 or there is no model |
| `0x002EC860(actor, on)` | `motionloop` `0x003B` | bit 3 of the binding's byte `+0x11` |
| `0x002EC940(actor, v)`, `0x002EC960(binding, v)` | `motionlooppreset` `0x04B4`, `puppetmotionlooppreset` `0x04E6` | the binding's `+0x2A` |
| `0x002ECC60`, `0x002EC970`, `0x002EC8B0` | `motionstartframe` `0x00F5`, `motionloopframe` `0x00F4` | the binding's `+0x14`, `+0x18` and `+0x1C` from a frame number; a positive frame passes through `0x003DA190`, which returns its argument |
| `0x002EC890(binding, on)` | `puppetmotionloop` `0x042C` (`0x0034C900`) | the bit `0x8` of the puppet binding's byte `+0x11`, the bit `0x002EC860` sets for `motionloop`; the binding is `0x003EB720(id)`: record `id` (0 to 31) of `0x02B5EA20` plus `0x10`, when that record's byte `+0x40` is set |
| `0x002EC9C0(binding, f)`, `0x002EC900(binding, f)`, `0x002ECCB0(binding, f)` | `puppetmotionloopframe` `0x0422` (`0x00348580`), `puppetmotionstartframe` `0x0423` (`0x00348A90`) | the puppet binding's `+0x18` from the first frame and `+0x1C` from the second, the second raised to at least the first when it is 0 or more; and `+0x14` from a frame raised to at least 0. A positive frame passes through `0x003DA190` as for `motionloopframe` |
| `0x002ECDC0(actor, on)`, `0x002ECE00(actor, on)` | `shows_3a` `0x003A`; `showw_39` `0x0039`, `hidew` `0x0035` | for a kind-`0x60` actor not in mode 1 (`+0x18`): bit 0 of the binding's `+0x70` or `+0x40`, then the visibility refresh `0x002E8FD0` |
| `0x003EB470(bind)` | `puppetbind` `0x041B`, `puppetbindoff` `0x041A`, `debug_modelinfobindoff` `0x20A8` | releases a puppet bind: the model (`0x002ED470`), the user count `+0x1C` of the bound record (`0x002EB870`), the binding reset (`0x00265F90`), and the record goes back to the free list `0x02B5EB70` |
| `0x003590B0()` | `ucmove` `0x009A`, `ucmove_52b` `0x052B` | the average of `0x022C7FF0` and `0x022C7FF4` |
| `0x0035A8D0(on)`, `0x00363B00(mode, pos, v)` | `ucon` `0x000D`, `ucon_4a5` `0x04A5` (through `0x0026C5D0`); `0x00363B00` also `set_microphone_pos` `0x056A` | `0x0035A8D0` sets or clears bit 5 of `+9` on the four party actors (`0x00263750`) and refreshes their models and bindings; `0x00363B00` stores the mode at `0x022CBA9A` and, for mode 1, the position at `0x022CBB10` and `v` at `0x022CBAAC` |
| `0x00378F90(on, group, n)`, `0x00379C50(map, group, n)`, `0x00379BD0(map, group, n)` | `setbgnpcstatus` `0x0406` | set or clear the flag of every background NPC whose id (16-byte entries at `[0x0209A670] + 0x1A0`, count `+0x22C`) has `id / 100` = group and `id % 100` = n, or any n for a negative one (12-byte flags at `+0x1D8`): `0x00378F90` passes `[0x0209A670]` to `0x00379C50`, which stores 1, when `on` is non-zero (`0x00378F99`) and to `0x00379BD0`, which stores 0, otherwise |
| `0x003DF790(v)` | `fieldsign` `0x0176` | 0 gives 3, 1 gives 2, anything else 1 |
| `0x003DF7B0(bit, off)`, `0x003DF810()` | `showfieldsign` `0x0172`, `hidefieldsign` `0x0173` | set or clear a bit of `0x02B59D18`; `0x003DF810` hands the highest live slot of 8 (`0x02B59CC0`) to `0x002900C0`, or clears the sign |
| `0x003E88C0(mode, id)`, `0x003E8900(mode, id)` | `animeplay` `0x0213`, `animeplaytiming` `0x0280` | on the `ACTL` record of the id ([MPK map pack](../World-Areas-And-Travel/mpk-map-pack.md)): `+0x15` = mode, state bit 4 set and bit 3 cleared; the mode nibble of `+0x12` becomes 0, or 1 for the timing form |
| `0x003E8890`, `0x003E8860` | `animepause` `0x0218`, `animepauseclear` `0x0219` | set or clear the record's state bit 3 |
| `0x003E8BF0`, `0x003E82F0` | `animestop` `0x0215`, `animesync` `0x0214` | run `0x003E8C50`, or return the test `0x003E8350`, on the record with the aux table and the weather slot (`0x00265920`) |
| `0x003E8AA0(mode)` | `animesync`, `skipexec` `0x0539` | hands every record whose `+0x15` is the mode (any for a negative one) and whose light `+0x08` is set to `0x0037A500` |
| `0x003E8F70(type)` | `setgaugecountertype` `0x01C1`, `setgaugetimertype` `0x01C2`, `setgaugeracetype` `0x0348` | `0x00408A20` with 1 to 4, or 0 for any other type |
| `0x003E9120(i, r, g, b, a)` | `setgaugecolor` `0x01CC` | stores the colour in entry i (0 to 3) of `0x02B5D098` and passes all four to `0x00408780` |
| `0x003E9190()` | `setgaugeraceiconparty` `0x0371` | `0x002E9FE0` on each of the four party actors |
| `0x003E9480`, `0x003E95E0`, `0x003E9640` | `setshapeclut` `0x0184`, `setshapeprior` `0x018C`, `setshapesampling` `0x0185` | on shape i of the map's shape list (`0x002E1040`, `0x60`-byte entries): the palette nibble `+0x0D`, the priority `+0x0E` (marking the list dirty, `+0x3F2` and `+0x3F3` bit 5), or bit 5 of `+0x08` |
| `0x003EA5C0`, `0x003EA4B0` | `voicechangevolume` `0x00B3`, `voicechangepan` `0x00B4` | for a voice slot in state 3 (`0x02B5D0B4` + `0x40` x slot), entry i of its table for the current language (`0x002DEBB0`) goes to `0x001DC350` or `0x001DC240` |
| `0x003944D0()`, `0x00394500()` | `fsttl_opencommandsync` `0x705F`, `fsttl_initialize` `0x7055` | 0 while `0x01EFAC12` is 2 and bit 1 of `[0x02AEE4C8] + 0xC4` is clear, else 1; and bit 0 of `[0x02AEE4C0] + 0xC0`, 0 with none |
| `0x00233D50()` | `unkCall_3091` `0x3091` | whether world lock 10 is free (`0x00226BD0`) |
| `0x00235DD0(unit, x, z)`, `0x00237460(point, unit)` | `btlAtelGetAngleDiff` `0x3063`, `btlAtelIsPcOnPoint` `0x3045` | for the unit (`0x0031B810`, or `0x003272A0` for a negative one): the angle in degrees from its facing `+0x160` to the point (`0x0031AC90`, `0x0031A930`), -1.0 without a unit; and `0x002374E0` on its position and the point `0x003209C0` gives, -1 without one |
| `0x00237D60()` | `callgameover` `0x04D8` | `0x0035C7A0(0xB)` unless `0x0035C700` answers non-zero; returns 1 |
| `0x0035EA00(v)` | `debug_set_syncv_mode` `0x20C4` | `0x00368AA0(2, v = 0)` and `0x022CA608` = v |
| `0x0036F050()` | `debug_recoveriopvoice` `0x20B6` | for each of the two banks in state 2 (`0x022D9B40`, `0x022D9B41`): state 1, `0x001DC0C0(bank)` and `0x0036ED50` on its slots in state 3 |
| `0x00377560(n)`, `0x002637B0(i)` | `debug_setmapdefaultpos` `0x202A` | puts party slot n's actor (`0x002637B0`: the id at `[0x0209A1F0 + 8 x i]`, -1 for i of 4 or more) at the map's default position (`[[0x0209A678]] + 0x28`, `+0x2C`) through `0x0026AF80` |
| `0x002593D0()`, `0x00259470()` | `setinterventioncamera` `0x02B9` (through `0x00359410`) | copy the `0x860`-byte block at `0x02097D20` to `0x02098580`, and back |
| `0x002EAA30(i)` | `set_summon_effect_filter_status` `0x0508` (through `0x003B7130`) | `0x003B5180` with entry i of the table `0x01EEBAA0`, which `0x002EA030(i)` returns for `0x003B4B60`, `0x003B50E0`, `0x003B5180` and `0x003B5470` |
| `0x003B7130(kind, on)` | `set_summon_effect_filter_status` | with `on`: the actor of `0x0032A060()` for kind 1, else of `0x00313590()`, goes to `0x002EA9D0(actor, kind)`, with kind -1 when it does not resolve; without `on`, `0x002EAA30` |
| `0x0032A060()` | the same verb, and `0x00359B10` | the id `+0x08` of the last battle unit with first-byte bits 0 and 3, an enemy stats record (`+0x05` = 1) without KO, Stone or X-Zone (unless `0x00377C20()`), and `0x002EAA10(actor, 1)` non-zero (`0x0032A0AA`) |
| `0x002EAA10(actor, slot)` | `0x0032A060` (`0x0032A0AF`) | the byte `+0xCD` when `0x002EA030(slot)` equals `0x002EA030(0)`, or `+0xCE` when it equals `0x002EA030(1)`, of the character object (`0x003E56C0`) of the actor's render record (dword 0 of `[actor+0xC0]` indexes the `0x740`-byte records at `[0x022C6F28]`); 0 otherwise |
| `0x0053F460()` | `fsroll_start` `0x703E` (through `0x005115D0`) | when the staff roll `[0x02CA8A80]` exists: places it (`0x0053E580`), re-attaches it (`0x00246AC0`) and sets its running byte `+0xFC` |
| `0x0053E580(roll)` | `fsroll_start` | with the start mode `+0x104` 1 or 2 (commands `0xC` and `0xD` of `0x0053F0D0`), finds the first line of the table `+0xC0` (count `+0xC8`, 0x20 bytes each) with id `+0x0C` equal to `+0x10C` and kind `+0x18` below 3 (mode 1) or equal to 3 (mode 2), and starts the roll at `[+0x10E] - (screen height 0x01E0C1DC - [line + 0x16]) / 2 + [line + 0x10]` (`+0xF0`) |
| `0x0053EDB0()` | `fsroll_refresh` `0x704E` (through `0x00511D00`) | frees the roll's line table and clears `+0xC0` to `+0x1497`, then takes a new 0x10000-byte table (`0x00249810(2)`) and resets the start `+0xF0` to the screen height, `+0x1494` to `0x80`, `+0xFF` and `+0x102` to 1, and the three faces' words `+0xCE`, `+0xD6`, `+0xDE` to `0x202` with scales `+0xD0`, `+0xD8`, `+0xE0` of 1.0 |
| `0x0053DD20(line, roll, face, id)` | `fsroll_nameA` `0x7046`, `fsroll_nameB` `0x7047`, `fsroll_nameC` `0x7048` (command 5 of `0x0053F0D0`, faces 0, 1 and 2) | fills the next 0x20-byte line of the table `+0xC0`: the text `0x002F9860(id + 0x6590)`, or `0x002F9860((id & 0x7FFF) + 0x61A8)` when bit 15 of the id is set, the face's scale `+0xD0 + 8 x face` and the size `0x003656A0` measures. The column count `+0x102` (`fsroll_linedisp`) places it: one column aligned by `+0x100` (`fsroll_layout`: 0 left at the margin `+0xF4`, 1 right, 2 centred on the width `+0x9C`, else x = 0); two columns on either side of the centre by turns (`+0x103`); three columns at x = 16, then half the width less and plus half the margin. It returns the height the start `+0xF0` advances by: the measured height plus the face's `+0xCC + 8 x face`, but 0 for the second and third of three columns and the difference of the two heights for the second of two |
| `0x0053EB70()` | `fsroll_isend` `0x703F` (`0x005116A0`), `fsroll_getstatus` `0x7040` (`0x00511710`) | the roll's state byte `+0xFC`, or 4 with no roll; `fsroll_isend` answers whether that is 4 |
| `0x0053ED60()` | the poll `0x00511590` of `fsroll_initialize` `0x703C` and `fsroll_finalize` `0x703D` | whether the task pointer `0x02CA8A78` (written by `0x0053EB90` and `0x0053EEA0`) is null; the poll holds the script while it is not |
| `0x0053ED70(on)` | `fsroll_pause` `0x704F` (`0x00511D10`) | with `on`, saves the state `+0xFC` in `+0xFD` and sets it to 3; without, restores it and clears `+0xFD` |
| `0x0053F3F0(which, v)` | `fsroll_fontscaleA` `0x7063`, `fsroll_fontscaleB` `0x7064`, `fsroll_fontscaleC` `0x7065` (`0x00511C10`, `0x00511C60`, `0x00511CB0`, with 8, 9 and 10) | the face scale `+0xD0`, `+0xD8` or `+0xE0` = v clamped to 0 to 2.0 |
| `0x0053EFC0(a, b, c, d)` | `fsroll_fade` `0x7066` (`0x00511E00`) | while the state `+0xFC` is 0, adds a 20-byte entry at `+0xA90` (count `+0x1492`): the start `+0xF0`, then `c x [0x01DFE0B4]` as its length and plus 3 as its end, `b` at `+0x08` and `+0x0C`, `d` at `+0x0A` and `+0x0E`, and `a` at `+0x10`; a `b` or `d` of 0 or more is stored times `[0x01DFE0B4]` and added to the end. The start `+0xF0` then advances by `a + 3` |
| `0x00253C20()` | `debug_isopen_triangle_menu` `0x2030` (through `0x002E05C0`) | 1 when `0x00290410` answers non-zero and `0x02092730` is 0 or 3 |
| `0x0025A830()` | `tutorial_clear_eyemove` `0x039C` (through `0x0034ED20`) | zeroes the float `0x02098348`, which `0x0025A860` returns for `tutorial_get_eyemove` `0x039D` (`0x0034EFC0`) |

The puppet binds are a pool of 32 records of `0x48` bytes from `0x02B5E120`: `0x003EB750`, run by the boot
`0x00266D10`, links them into the free list; `0x003EB500`, run by the area unload `0x002628B0`, releases every bound
one and `0x003EB5F0(v)` those whose byte `+0x41` is v. `0x00265F90(binding)` resets a binding: render
index -1, the three floats at `+0x14`-`+0x1C` to -1.0 and the default flags.

## Related

- [Verb dispatch](verb-dispatch.md): how a call id reaches these records.
- [Native commands](native-commands.md): what the three callbacks and the shapes mean.
- [Script interpreter](script-interpreter.md): the call opcodes.
