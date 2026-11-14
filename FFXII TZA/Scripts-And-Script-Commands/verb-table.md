---
title: "Script verb table: every call id with its name, callbacks, shape, argument count, what it reaches and how often the US scripts use it"
kind: "reference"
category: "Scripts and script commands"
addresses: "0x01EED700, 0x01F281B0, 0x01F29418, 0x01F29440, 0x01F26720, 0x0016D6A0, 0x005C5230, 0x00267E10, 0x00267DB0, 0x0026B4E0, 0x00263D00, 0x00355940, 0x00355E80, 0x0050C910"
---

## What it lists

One row per command record in the five command tables the verb dispatcher reads: 1,496 in family
0, 147 in family 3, 1 in family 5, 104 in family 7 and 212 in the shared table that family 2's
debug verbs and eleven aliased families use. The callbacks are read from the shipping executable
at `table + 8 + 32 × command`; the names come from the ff12-script catalogue where it has one, and
from other authored sources otherwise; the argument counts come from the handler bodies.

[verb-table-inputs.tsv](verb-table-inputs.tsv) gives one row per verb name, 1,942 in all, with what a call of
it does:

- `input` (the name), `label` (its call ids) and `domain` (its arguments);
- `precedence` (which source wins when another one sets the same state) and `takes_effect` (when the effect
  starts, from the shape);
- `consumers` (the callbacks), `visible_effect` (what the player sees or which state changes, with the address of
  the code that does it) and `inert_when`.

Of the 773 verbs that no `us` script calls, 678 read "no visible change in the shipped game: no step calls it": no script of any
tree calls them. Another 94 read "nothing in story play" and name the developer menus (`bin/ctrl`, `bin/btlctrl`,
`bin/evctrl`, `bin/mapctrl`) that call them, and `musicfadeoutall` names the `ch`, `cn` and `kr` story scripts
that call it. The row named `-` holds the 19 call ids that have no name.

### The staff-roll loader

The loader is the `0xC8`-byte task at `0x02CA8A78` with procedure `0x0053EB90` that `0x0053ED10` starts for `fsroll_initialize`.

`StaffRollLoader` (`0xC8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x0053EB90` |
| `+0xC0` | `u32` | logoLoaded | set to 1 by message 16 (a resource batch has loaded), the logo picture sf_logo_c.tm2 the construct message requested (`0x0053EBCF`); each tick (message 2) waits until the six font slots 7-12 are ready (`0x003657E0`), texts `0x19` and `0x1A` are resident (`0x002F8040`) and this is set (`0x0053EC2B`), then clears the task pointer `0x02CA8A78` and releases itself (`0x0053EC3A`, `0x0053EC41`), which lets the fsroll_initialize poll go on |
| `+0xC4` | `u8[4]` | pad0C4 | read and written by no function; nothing fixes its width |

The logo picture outlives the loader. The loader's message 1 requests `sf_logo_c` (`0x00D22E80`) through `0x002493D0`
when `0x02CA8A88` is still 0 (`0x0053ECA6`-`0x0053ECE7`). Command 6 of `0x0053F0D0` puts the picture in the next line of the
roll's table, with line kind 3 (`0x0053F1EA`-`0x0053F209`). The finaliser task `0x0053EEA0`, on its message 1, releases the
picture (`0x0024A680(picture, 1)`) and clears the pointer (`0x0053EF15`-`0x0053EF32`).

So `fsroll_initialize` holds the script until six font slots, two texts and the `sf_logo_c` logo picture are all
loaded. The logo then appears as one line of the staff roll, and a finishing task releases it afterwards.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02CA8A88` | `void*` | 0 (zero-filled tail of `.data`) | the staff roll's logo picture | `0x0053EB90` (`0x0053ECE7`); `0x0053EEA0`, 0 (`0x0053EF32`) | `0x0053EB90` (`0x0053ECA6`); `0x0053EEA0` (`0x0053EF15`); `0x0053F0D0` (`0x0053F1EA`) |

## Columns

| Column | Meaning |
|---|---|
| `call_id` | the sixteen-bit id a script instruction carries: `family << 12 \| command` |
| `family`, `command` | the two halves |
| `verb` | the authored name; `unkCall_xxx` is the catalogue's own placeholder |
| `name_source` | `catalogue` for the ff12-script list, `other` for a name from another authored source, empty when the verb has no name |
| `cat_args`, `cat_ret`, `cat_act`, `param_types` | the catalogue's declared argument count, whether it returns a value, whether it takes an actor, and its parameter type bytes in the order the handler pops them, last argument first (`04A2`: `0x30` is the float popped first, `0x00352BA8`, the second argument); blank when the name is not the catalogue's |
| `begin`, `poll`, `result` | the three callbacks of the record, empty when null |
| `stub` | which of `begin` and `result` holds the bare `ret` at `0x0016D6A0` |
| `shape` | which callbacks the record has, the `ret` stub not counting: `result`, `begin+poll`, `begin`, `begin+poll+result`, `poll`, `poll+result`, `begin+result`, `empty`, or `stub` when nothing but the stub and the zero-returning poll `0x005C5230` is left; that poll counts as a poll in every other shape, as it does in the population table of [native commands](native-commands.md) |
| `arg_callback` | the callback that pops the arguments (`begin` or `result`); blank when that callback is the stub or the record is empty |
| `pops_int`, `pops_float`, `pushes`, `result_writes` | counted direct calls of `0x00267E10`, `0x00267DB0`, the two push helpers and the two result writers in that callback, a tail jump to a pop helper counting as a call (`0x00267DB0` in the four callbacks of `009A`, `0168`, `205C` and `2068`, at `0x00345514`, `0x0034F86B`, `0x0050EE21`, `0x0050C853`; `0x00267E10` at `0x0050C7F3` and `0x0050E999`); a handler that pushes constants and delegates to a shared body pops there, so these are not the argument count, which `arity` carries |
| `guard` | the predicate that makes a pop conditional, where one exists (`0x00263D00` for the class-3 forms) |
| `arity`, `arity_status`, `net_or_sums` | the measured argument count; `CONFIRMED` equals the catalogue, `CONFLICT` differs from it, `DERIVED` has no catalogue value, `GUARDED` and `CONDITIONAL` take two values (`lo\|hi`) depending on the guard |
| `result_body` | the result handler's control flow: `CONST`, `TAILJUMP`, `CALL1`, `LINEAR` (several calls, no branch) or `BRANCHING`; carried over from the earlier handler list, not read again for this table |
| `reach` | the engine subsystems the callbacks call directly, with hit counts, ignoring helpers with more than twenty callers; carried over from the earlier call-graph map |
| `us_calls` | calls of the verb in the 1,114 decompiled US scripts, under its name and under the `sys` spelling the listings give a special call form of the same command (`sysTurna(` is `turna`); a script function that shares a verb's name (`function mapjump(`) is not a call |

## Data

| Fact | Value |
|---|---|
| rows | 1,960 |
| shapes | result only 1,571; begin and poll 202; begin only 76; all three 48; poll only 28; poll and result 6; begin and result 1; stub 24; empty 4 |
| names | 1,270 from the catalogue (54 of them `unkCall` placeholders), 671 from other sources, 19 without a name (the 19 `DERIVED-UNNAMED` rows) |
| argument count | 1,229 confirmed against the catalogue, 653 derived, 34 guarded, 24 conditional, 19 derived without a name, 1 conflict |
| the conflict | `unkCall_5c7` (`0x05C7`): the catalogue declares two arguments, the result is the `ret` stub and pops no argument |
| verbs called in the US corpus | 1,169 of 1,960; 1,850,846 calls in all |
| most called | `setmapidfloor` 84,066; `wait` 83,795; `setmapidwall` 76,134; `nowmap` 63,695 |
| `setforcefightmode` (`0x0334`) | 177 calls in 83 scripts, every one `setforcefightmode(0)` |
| the four empty records | `setnorecovertelepostatus` `0x0330`, `battlemembersync` `0x0356`, `restartbattle` `0x03B0`, `debug_meswin_3e` `0x203E`; no script in the corpus calls them |

The poll-only rows are the waits on something an earlier verb started: `movesync`, `turnsync`,
`stdmotionreadsync`, `crossfadesync`, `gaugeshowsync`, `resumebehindcamerasync`,
`summonreadsync`, `summontopartyreadsync`, `behindcamerafovyrollsync`, `vibsync`, `lookatsync`,
`spattackwindowsync`, `actoriopvoicereadsync`, `entryreadsync`, `behindtoeventcamerasync`,
`moviestandbysync`, `movieplaysync`, `bgmstreamreadsync`, `bgmstreamplaysync`, `gillwinsync`,
`ucmovesync`, `initsync`, `musicfadeoutsync`, `unkCall_5a6`, `fsmenu_syncopenchip`,
`fsttl_opencommandsync` and `fsttl_closecommandsync`.

`moveblurfadesync` (`0x03BD`) also counts as poll only: its begin and result are the stub and its
poll `0x00345100` is live.

The 24 stub rows hold only the `ret` at `0x0016D6A0` and the poll `0x005C5230`, which returns 0, so a
stubbed verb completes on its first call: `hddmount`, `atrac3cancel`, `btlAtelRemoveAllEquip` and the debug
verb `0x20D3` have a stub begin with that poll; `atrac3standbysync` and `atrac3playsync` have that poll
alone; `atrac3play`, `unkCall_5c7`, `btlAtelSetUnique`, `btlAtelChangeAllBtlCharaFlag_DontMoveDebug`,
the tag and setup verbs `0x3054` to `0x305A` and seven debug verbs have a stub result.

`disposesummon`, `changetonormalparty`, `hddinstall` and `networkhddinstall` have the same stub begin and
poll, but a live result, so they are poll and result rows: `0x0034FB20` (calls `0x00314D40(1)`, then jumps to
`0x003B6F60`), `0x00350F30`, and `0x003447F0` for both install verbs (jumps to `0x00408EC0` with 1).

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
| `0x002E7DD0(actor, run)`, `0x002E7E10(actor, run)` | `getdefaultwalkthresholdspeed` `0x0272`, `getdefaultrunspeed` `0x0246` | the model parameter (`0x003E6150`) `0x09000707`, or `0x09000101` for a positive second argument; and `0x09000808` or `0x09000202`; a negative argument counts as 0 (`0x002E7DEC`, `0x002E7E2C`) and both verbs pass −1 (`0x0034D30F`, `0x0034CB3F`), so scripts get `0x09000707` and `0x09000808`; 0 without a model |
| `0x002E9B10(actor)` | `raturn` `0x025D`, `raturna` `0x025F`, `raturnya` `0x02D5` and their relatives | the model parameter `0x09000909`, or pi/30 (`0x00D0F8E4`) without a model |
| `0x002E30D0(actor, on, a, b)` | `unkCall_5bd` `0x05BD` | `0x00382B50(render index, a, b)`, or `0x00382B50(-1, 0, 0)` when `on` is 0 or there is no model |
| `0x002EC860(actor, on)` | `motionloop` `0x003B` | bit `0x8` of the binding's byte `+0x11` |
| `0x002EC940(actor, v)`, `0x002EC960(binding, v)` | `motionlooppreset` `0x04B4`, `puppetmotionlooppreset` `0x04E6` | the binding's `+0x2A` |
| `0x002ECC60`, `0x002EC970`, `0x002EC8B0` | `motionstartframe` `0x00F5`, `motionloopframe` `0x00F4` | the binding's `+0x14`, `+0x18` and `+0x1C` from a frame number; a positive frame passes through `0x003DA190`, which returns its argument |
| `0x002EC890(binding, on)` | `puppetmotionloop` `0x042C` (`0x0034C900`) | the bit `0x8` of the puppet binding's byte `+0x11`, the bit `0x002EC860` sets for `motionloop`; the binding is `0x003EB720(id)`: the record that entry `id` (0 to 31) of the pointer table `0x02B5EA20` points to, plus `0x10`, when the entry is set and that record's byte `+0x40` is set |
| `0x002EC9C0(binding, f)`, `0x002EC900(binding, f)`, `0x002ECCB0(binding, f)` | `puppetmotionloopframe` `0x0422` (`0x00348580`), `puppetmotionstartframe` `0x0423` (`0x00348A90`) | the puppet binding's `+0x18` from the first frame and `+0x1C` from the second, the second raised to at least the first when it is 0 or more; and `+0x14` from a frame raised to at least 0. A positive frame passes through `0x003DA190` as for `motionloopframe` |
| `0x002ECDC0(actor, on)`, `0x002ECE00(actor, on)` | `shows_3a` `0x003A`; `showw_39` `0x0039`, `hidew` `0x0035` | for a kind-`0x60` actor that is not a captured member (bind state `+0x18` is not 1; [party during scenes](party-during-scenes.md)): bit `0x1` of the binding's `+0x70` or `+0x40`, then the visibility refresh `0x002E8FD0`; with no binding (`+0xC0` null) both write byte `+0x10` of address 0 instead (`0x002ECDEF`, `0x002ECE2F`) |
| `0x003EB470(bind)` | `puppetbind` `0x041B`, `puppetbindoff` `0x041A`, `debug_modelinfobindoff` `0x20A8` | releases a puppet bind: the model (`0x002ED470`), the user count `+0x1C` of the bound record (`0x002EB870`), the binding reset (`0x00265F90`), and the record goes back to the free list `0x02B5EB70` |
| `0x003590B0()` | `ucmove` `0x009A`, `ucmove_52b` `0x052B` | the average of `0x022C7FF0` and `0x022C7FF4` |
| `0x0035A8D0(v)`, `0x00363B00(mode, pos, v)` | `ucon` `0x000D`, `ucon_4a5` `0x04A5` (through `0x0026C5D0`); `0x00363B00` also `set_microphone_pos` `0x056A` | `0x0035A8D0` sets bit `0x20` of `+9` on the four party actors (`0x00263750`) for an argument of 0 and clears it for any other (`0x0035A8F2`-`0x0035A91E`) and refreshes their models and bindings; `0x00363B00` stores the mode at `0x022CBA9A` and, for mode 1, the position at `0x022CBB10` and `v` at `0x022CBAAC` |
| `0x00378F90(on, group, n)`, `0x00379C50(map, group, n)`, `0x00379BD0(map, group, n)` | `setbgnpcstatus` `0x0406` | set or clear the flag of every background NPC whose id (16-byte entries at `[0x0209A670] + 0x1A0`, count `+0x22C`) has `id / 100` = group and `id % 100` = n, or any n for a negative one (12-byte flags at `+0x1D8`): `0x00378F90` passes `[0x0209A670]` to `0x00379C50`, which stores 1, when `on` is non-zero (`0x00378F99`) and to `0x00379BD0`, which stores 0, otherwise |
| `0x003DF790(v)` | `fieldsign` `0x0176` | 0 gives 3, 1 gives 2, anything else 1 |
| `0x003DF7B0(bit, show)`, `0x003DF810()` | `showfieldsign` `0x0172`, `hidefieldsign` `0x0173` | `0x003DF7B0` clears the hide bit of index `bit` in `0x02B59D18` when `show` is non-zero (`btr`, `0x003DF7BE`) and sets it when `show` is 0 (`bts`, `0x003DF7C3`): `showfieldsign` passes 1 and `hidefieldsign` 0, both with index 2 from manager 0 and 3 from the others, so bit `0x4` or `0x8` (`0x003546D0`-`0x003546D6`, `0x00354B0B`-`0x00354B13`). With no hide bit left it jumps to `0x003DF810`, which hands the highest live slot of 8 (`0x02B59CC0`) to `0x002900C0`, or clears the sign; otherwise it calls `0x0029CAB0(0, 0, 0, 0)` and zeroes the 24 bytes from `0x02B59D00` (`0x003DF7D9`-`0x003DF7FE`) |
| `0x003E88C0(mode, id)`, `0x003E8900(mode, id)` | `animeplay` `0x0213`, `animeplaytiming` `0x0280` | on the `ACTL` record of the id ([MPK map pack](../World-Areas-And-Travel/mpk-map-pack.md)): `+0x15` = mode, state bit `0x10` set and bit `0x8` cleared; the mode nibble of `+0x12` becomes 0, or 1 for the timing form |
| `0x003E8890`, `0x003E8860` | `animepause` `0x0218`, `animepauseclear` `0x0219` | set or clear the record's state bit `0x8` |
| `0x003E8BF0`, `0x003E82F0` | `animestop` `0x0215`, `animesync` `0x0214` | run `0x003E8C50`, or return the test `0x003E8350`, on the record with the aux table and the weather slot (`0x00265920`) |
| `0x003E8AA0(mode)` | `animesync`, `skipexec` `0x0539` | hands every record whose `+0x15` is the mode (any for a negative one) and whose light `+0x08` is set to `0x0037A500` |
| `0x003E8F70(type)` | `setgaugecountertype` `0x01C1`, `setgaugetimertype` `0x01C2`, `setgaugeracetype` `0x0348` | `0x00408A20` with 1 to 4, or 0 for any other type |
| `0x003E9120(i, r, g, b, a)` | `setgaugecolor` `0x01CC` | stores the colour in entry i (0 to 3) of `0x02B5D098` and passes all four to `0x00408780` |
| `0x003E9190()` | `setgaugeraceiconparty` `0x0371` | `0x002E9FE0` on each of the four party actors |
| `0x003E9480`, `0x003E95E0`, `0x003E9640` | `setshapeclut` `0x0184`, `setshapeprior` `0x018C`, `setshapesampling` `0x0185` | on shape i of the map's shape list (`0x002E1040`, `0x60`-byte entries): the palette nibble `+0x0D`, the priority `+0x0E` (marking the list dirty, `+0x3F2` and `+0x3F3` bit `0x20`), or bit `0x20` of `+0x08` |
| `0x003EA5C0`, `0x003EA4B0` | `voicechangevolume` `0x00B3`, `voicechangepan` `0x00B4` | for a voice slot in state 3 (`0x02B5D0B4` + `0x40` x slot), entry i of its table for the current language (`0x002DEBB0`) goes to `0x001DC350` or `0x001DC240` |
| `0x003944D0()`, `0x00394500()` | `fsttl_opencommandsync` `0x705F`, `fsttl_initialize` `0x7055` | 0 while `0x01EFAC12` is 2 and bit `0x2` of `[0x02AEE4C8] + 0xC4` is clear, else 1; and bit `0x1` of `[0x02AEE4C0] + 0xC0`, 0 when `[0x02AEE4C0]` is null |
| `0x00233D50()` | `unkCall_3091` `0x3091` | whether world lock 10 is free (`0x00226BD0`) |
| `0x00235DD0(unit, x, z)`, `0x00237460(point, unit)` | `btlAtelGetAngleDiff` `0x3063`, `btlAtelIsPcOnPoint` `0x3045` | for the unit (`0x0031B810`, or `0x003272A0` for a negative one): the angle in degrees from its facing `+0x160` to the point (`0x0031AC90`, `0x0031A930`), -1.0 without a unit; and `0x002374E0` on its position and the point `0x003209C0` gives, -1 without one |
| `0x00237D60()` | `callgameover` `0x04D8` | `0x0035C7A0(0xB)` unless `0x0035C700` answers non-zero; returns 1 |
| `0x0035EA00(v)` | `debug_set_syncv_mode` `0x20C4` | `0x00368AA0(2, v = 0)` and `0x022CA608` = v |
| `0x0036F050()` | `debug_recoveriopvoice` `0x20B6` | for each of the two banks in state 2 (`0x022D9B40`, `0x022D9B41`): state 1, `0x001DC0C0(bank)` and `0x0036ED50` on its slots in state 3 |
| `0x00377560(n)`, `0x002637B0(i)` | `debug_setmapdefaultpos` `0x202A` | puts party slot n's actor (`0x002637B0`: the id at `[0x0209A1F0 + 8 x i]`, -1 for i of 4 or more) at the map's default position (`[[0x0209A678]] + 0x28`, `+0x2C`) through `0x0026AF80` |
| `0x002593D0()`, `0x00259470()` | `setinterventioncamera` `0x02B9` (through `0x00359410`) | copy the `0x860`-byte block at `0x02097D20` to `0x02098580`, and back |
| `0x002EAA30(i)` | `set_summon_effect_filter_status` `0x0508` (through `0x003B7130`) | `0x003B5180` with entry i of the table `0x01EEBAA0`, which `0x002EA030(i)` returns for `0x003B4B60`, `0x003B50E0`, `0x003B5180` and `0x003B5470` |
| `0x003B7130(kind, on)` | `set_summon_effect_filter_status` | with `on`: the actor of `0x0032A060()` for kind 1, else of `0x00313590()`, goes to `0x002EA9D0(actor, kind)`, with kind -1 when it does not resolve; without `on`, `0x002EAA30` |
| `0x0032A060()` | the same verb, and `0x00359B10` | the id `+0x08` of the last battle unit with first-byte bits `0x1` and `0x8`, an enemy stats record (`+0x05` = 1) without KO, Stone or X-Zone (unless `0x00377C20()`), and `0x002EAA10(actor, 1)` non-zero (`0x0032A0AA`) |
| `0x002EAA10(actor, slot)` | `0x0032A060` (`0x0032A0AF`) | the byte `+0xCD` when `0x002EA030(slot)` equals `0x002EA030(0)`, or `+0xCE` when it equals `0x002EA030(1)`, of the character object (`0x003E56C0`) of the actor's render record (dword 0 of `[actor+0xC0]` indexes the `0x740`-byte records at `[0x022C6F28]`); 0 otherwise |
| `0x0053F460()` | `fsroll_start` `0x703E` (through `0x005115D0`) | when the staff roll `[0x02CA8A80]` exists: places it (`0x0053E580`), re-attaches it (`0x00246AC0`) and sets its running byte `+0xFC` |
| `0x0053E580(roll)` | `fsroll_start` | with the start mode `+0x104` 1 or 2 (commands `0xC` and `0xD` of `0x0053F0D0`), finds the first line of the table `+0xC0` (count `+0xC8`, 0x20 bytes each) with id `+0x0C` equal to `+0x10C` and kind `+0x18` below 3 (mode 1) or equal to 3 (mode 2), and starts the roll at `[+0x10E] - (screen height 0x01E0C1DC - [line + 0x16]) / 2 + [line + 0x10]` (`+0xF0`) |
| `0x0053EDB0()` | `fsroll_refresh` `0x704E` (through `0x00511D00`) | frees the roll's line table and clears `+0xC0` to `+0x1497`, then takes a new 0x10000-byte table (`0x00249810(2)`) and resets the start `+0xF0` to the screen height, `+0x1494` to `0x80`, `+0xFF` and `+0x102` to 1, and the three faces' words `+0xCE`, `+0xD6`, `+0xDE` to `0x202` with scales `+0xD0`, `+0xD8`, `+0xE0` of 1.0 |
| `0x0053DD20(line, roll, face, id)` | `fsroll_nameA` `0x7046`, `fsroll_nameB` `0x7047`, `fsroll_nameC` `0x7048` (command 5 of `0x0053F0D0`, faces 0, 1 and 2) | fills the next 0x20-byte line of the table `+0xC0`: the text `0x002F9860(id + 0x6590)`, or `0x002F9860((id & 0x7FFF) + 0x61A8)` when bit `0x8000` of the id is set, the face's scale `+0xD0 + 8 x face` and the size `0x003656A0` measures. The column count `+0x102` (`fsroll_linedisp`) places it: one column aligned by `+0x100` (`fsroll_layout`: 0 left at the margin `+0xF4`, 1 right, 2 centred on the width `+0x9C`, else x = 0); two columns on either side of the centre by turns (`+0x103`); three columns at x = 16, then half the width less and plus half the margin. It returns the height the start `+0xF0` advances by: the measured height plus the face's `+0xCC + 8 x face`, but 0 for the second and third of three columns and the difference of the two heights for the second of two |
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

The two lists have head records of the same shape: the bound list at `0x02B5EB20` and the free list at `0x02B5EB70`.
Each record links through `+0x00` (next) and `+0x08` (previous). `0x003EB750` zeroes both heads' links (`0x02B5EB20`
and `0x02B5EB28` at `0x003EB77A` and `0x003EB773`, `0x02B5EB70` and `0x02B5EB78` at `0x003EB79B` and `0x003EB794`), their words
`+0x40` (`0x02B5EB60` at `0x003EB781`, `0x02B5EBB0` at `0x003EB7A2`) and their bindings at `+0x10`.

`0x003EB750` then pushes the 32
records onto the free list (`0x003EB81B`-`0x003EB83C`). The bind `0x003EB250` takes the free list's first record and
puts it on the bound list. `0x003EB470`, `0x003EB500` and `0x003EB5F0` put records back on the free list.

The field signs are 8 slots in four arrays: a text pointer at `0x02B59C40 + 8 x n`, a second pointer at
`0x02B59C80 + 8 x n`, the live word at `0x02B59CC0 + 4 x n` and the first argument at `0x02B59CE0 + 4 x n`.
`0x003DF760(a, n, live, text, second)` fills slot n (`0x003DF76F`-`0x003DF787`), and `0x003DF5B0` zeroes every slot
(`0x003DF5BC`-`0x003DF65D`). `0x003DF810` passes the highest live slot to `0x0029CAB0`, a jump to `0x002900C0`, or clears the
sign when no slot is live. The 12 callers of `0x003DF760` pass slots 1 to 7:

- 1 and 2: the contact passes `0x0025C230` and `0x0025C830`;
- 3: the interaction pass `0x00268D10`;
- 1 to 5: the clears in `0x00314020`;
- 6 and 7: `setfieldsign`;
- 4 and 5: `setfieldsignonce`;
- 7: the area unload `0x002628B0`, a clear.

None of them passes slot 0, so slot 0 stays clear.

`0x003DF810` keeps a copy of the slot it shows: the text pointer at `0x02B59D00` (`0x003DF8B1`), the second pointer at
`0x02B59D08` (`0x003DF8BD`), the live word at `0x02B59D10` (`0x003DF8D4`) and the first argument at `0x02B59D14`
(`0x003DF8C9`). It sets all four to 0 when no slot is live (`0x003DF852`-`0x003DF866`). `0x003DF7B0` (`0x003DF7EA`-`0x003DF7FE`)
and `0x003DF670` (`0x003DF6BD`-`0x003DF6D0`) do the same when they hide the sign because the mask `0x02B59D18` is non-zero.
`0x003DF5B0` sets `0x02B59D10` to 1 (`0x003DF5B2`) and clears the mask `0x02B59D18` (`0x003DF664`).

No instruction reads the copy: every reference to `0x02B59D00`-`0x02B59D17` is one of these stores, no instruction
reaches it through a base register or the image base, and the file holds no pointer to it.

The mask's bit `0x1` belongs to `0x003DF670`, which the frame update runs after `0x003DEB30`
([frame update order](../Engine-Core/frame-update-order.md)). It clears the bit (`0x003DF691`) when the
party-focus actor (`0x003590D0`, resolved by `0x003588B0`) passes `0x002EA6A0`, and sets it (`0x003DF69A`) otherwise.

`0x002EA6A0` answers 1 for an actor whose byte `+0x04` is 1 and whose binding `+0xC0` has a render index other than
-1 and a non-null pointer `+0x08` to a record with bit `0x2` in its byte `+0x18`. While the mask is non-zero,
`0x003DF670` hides the sign (`0x0029CAB0(0, 0, 0, 0)`, `0x003DF6AC`-`0x003DF6B6`); when it is 0, it jumps to `0x003DF810`
(`0x003DF6A7`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02B59C40` | `void*` | 0 (zero-filled tail of `.data`) | slot 0's text pointer | `0x003DF5B0`, 0 (`0x003DF656`), from the area unload `0x002628B0` (`0x00262CE5`) and the jump at `0x003DF6E0`; `0x003DF760` writes through the slot index (`0x003DF76F`), and its callers pass slots 1 to 7 | `0x003DF810` (`0x003DF895`, through the slot index), when slot 0 is the highest live slot; it passes the pointer to `0x0029CAB0` |
| `0x02B59C48` | `void*` | 0 (zero-filled tail of `.data`) | slot 1's text pointer | `0x003DF5B0`, 0 (`0x003DF63A`); `0x003DF760`, through the slot index (`0x003DF76F`) | `0x003DF810` (`0x003DF895`, through the slot index), when slot 1 is the highest live slot |
| `0x02B59C50` | `void*` | 0 (zero-filled tail of `.data`) | slot 2's text pointer | `0x003DF5B0`, 0 (`0x003DF62C`); `0x003DF760`, through the slot index (`0x003DF76F`) | `0x003DF810` (`0x003DF895`, through the slot index), when slot 2 is the highest live slot |
| `0x02B59C58` | `void*` | 0 (zero-filled tail of `.data`) | slot 3's text pointer | `0x003DF5B0`, 0 (`0x003DF610`); `0x003DF760`, through the slot index (`0x003DF76F`) | `0x003DF810` (`0x003DF895`, through the slot index), when slot 3 is the highest live slot |
| `0x02B59C60` | `void*` | 0 (zero-filled tail of `.data`) | slot 4's text pointer | `0x003DF5B0`, 0 (`0x003DF602`); `0x003DF760`, through the slot index (`0x003DF76F`) | `0x003DF810` (`0x003DF895`, through the slot index), when slot 4 is the highest live slot |
| `0x02B59C68` | `void*` | 0 (zero-filled tail of `.data`) | slot 5's text pointer | `0x003DF5B0`, 0 (`0x003DF5E6`); `0x003DF760`, through the slot index (`0x003DF76F`) | `0x003DF810` (`0x003DF895`, through the slot index), when slot 5 is the highest live slot |
| `0x02B59C70` | `void*` | 0 (zero-filled tail of `.data`) | slot 6's text pointer | `0x003DF5B0`, 0 (`0x003DF5D8`); `0x003DF760`, through the slot index (`0x003DF76F`) | `0x003DF810` (`0x003DF895`, through the slot index), when slot 6 is the highest live slot |
| `0x02B59C78` | `void*` | 0 (zero-filled tail of `.data`) | slot 7's text pointer | `0x003DF5B0`, 0 (`0x003DF5BC`); `0x003DF760`, through the slot index (`0x003DF76F`) | `0x003DF810` (`0x003DF895`, through the slot index), when slot 7 is the highest live slot |
| `0x02B59C88` | `void*` | 0 (zero-filled tail of `.data`) | slot 1's second pointer | `0x003DF5B0`, 0 (`0x003DF641`); `0x003DF760`, through the slot index (`0x003DF777`) | `0x003DF810` (`0x003DF88D`, through the slot index), when slot 1 is the highest live slot |
| `0x02B59C90` | `void*` | 0 (zero-filled tail of `.data`) | slot 2's second pointer | `0x003DF5B0`, 0 (`0x003DF633`); `0x003DF760`, through the slot index (`0x003DF777`) | `0x003DF810` (`0x003DF88D`, through the slot index), when slot 2 is the highest live slot |
| `0x02B59C98` | `void*` | 0 (zero-filled tail of `.data`) | slot 3's second pointer | `0x003DF5B0`, 0 (`0x003DF617`); `0x003DF760`, through the slot index (`0x003DF777`) | `0x003DF810` (`0x003DF88D`, through the slot index), when slot 3 is the highest live slot |
| `0x02B59CA0` | `void*` | 0 (zero-filled tail of `.data`) | slot 4's second pointer | `0x003DF5B0`, 0 (`0x003DF609`); `0x003DF760`, through the slot index (`0x003DF777`) | `0x003DF810` (`0x003DF88D`, through the slot index), when slot 4 is the highest live slot |
| `0x02B59CA8` | `void*` | 0 (zero-filled tail of `.data`) | slot 5's second pointer | `0x003DF5B0`, 0 (`0x003DF5ED`); `0x003DF760`, through the slot index (`0x003DF777`) | `0x003DF810` (`0x003DF88D`, through the slot index), when slot 5 is the highest live slot |
| `0x02B59CB0` | `void*` | 0 (zero-filled tail of `.data`) | slot 6's second pointer | `0x003DF5B0`, 0 (`0x003DF5DF`); `0x003DF760`, through the slot index (`0x003DF777`) | `0x003DF810` (`0x003DF88D`, through the slot index), when slot 6 is the highest live slot |
| `0x02B59CB8` | `void*` | 0 (zero-filled tail of `.data`) | slot 7's second pointer | `0x003DF5B0`, 0 (`0x003DF5C3`); `0x003DF760`, through the slot index (`0x003DF777`) | `0x003DF810` (`0x003DF88D`, through the slot index), when slot 7 is the highest live slot |
| `0x02B59CC8` | `u32[2]` | 0 (zero-filled tail of `.data`) | the live words of slots 2 and 3 | `0x003DF5B0`, 0 with one 8-byte store (`0x003DF61E`); `0x003DF760`, through the slot index (`0x003DF77F`) | `0x003DF810`, which walks the live words down from slot 7's `0x02B59CDC` (`0x003DF81B`) to `0x02B59CC0` (`0x003DF822`) |
| `0x02B59CD0` | `u32[2]` | 0 (zero-filled tail of `.data`) | the live words of slots 4 and 5 | `0x003DF5B0`, 0 with one 8-byte store (`0x003DF5F4`); `0x003DF760`, through the slot index (`0x003DF77F`) | `0x003DF810`, which walks the live words down from slot 7's `0x02B59CDC` (`0x003DF81B`) to `0x02B59CC0` (`0x003DF822`) |
| `0x02B59CD8` | `u32[2]` | 0 (zero-filled tail of `.data`) | the live words of slots 6 and 7 | `0x003DF5B0`, 0 with one 8-byte store (`0x003DF5CA`); `0x003DF760`, through the slot index (`0x003DF77F`) | `0x003DF810`, which walks the live words down from slot 7's `0x02B59CDC` (`0x003DF81B`) to `0x02B59CC0` (`0x003DF822`) |
| `0x02B59CE8` | `u32[2]` | 0 (zero-filled tail of `.data`) | the first arguments of slots 2 and 3 | `0x003DF5B0`, 0 with one 8-byte store (`0x003DF625`); `0x003DF760`, through the slot index (`0x003DF787`) | `0x003DF810` (`0x003DF8A0`, through the slot index) |
| `0x02B59CF0` | `u32[2]` | 0 (zero-filled tail of `.data`) | the first arguments of slots 4 and 5 | `0x003DF5B0`, 0 with one 8-byte store (`0x003DF5FB`); `0x003DF760`, through the slot index (`0x003DF787`) | `0x003DF810` (`0x003DF8A0`, through the slot index) |
| `0x02B59CF8` | `u32[2]` | 0 (zero-filled tail of `.data`) | the first arguments of slots 6 and 7 | `0x003DF5B0`, 0 with one 8-byte store (`0x003DF5D1`); `0x003DF760`, through the slot index (`0x003DF787`) | `0x003DF810` (`0x003DF8A0`, through the slot index) |

## Related

- [Verb dispatch](verb-dispatch.md): how a call id reaches these records.
- [Native commands](native-commands.md): what the three callbacks and the shapes mean.
- [Script interpreter](script-interpreter.md): the call opcodes.
