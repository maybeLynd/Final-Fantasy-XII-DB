---
title: "Script verb table: every call id with its name, callbacks, shape, argument count, what it reaches and how often the shipped scripts use it"
kind: "reference"
category: "Scripts and script commands"
addresses: "01EED700, 01F281B0, 01F29418, 01F29440, 01F26720, 0016D6A0, 005C5230, 00267E10, 00267DB0, 0026B4E0, 00263D00, 00355940, 00355E80, 0050C910"
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
| `stub` | which of `begin` and `result` holds the bare `ret` at `0016D6A0` |
| `shape` | which callbacks the record has, the `ret` stub not counting: `result`, `begin+poll`, `begin`, `begin+poll+result`, `poll`, `poll+result`, `begin+result`, `empty`, or `stub` when nothing but the stub and the zero-returning poll `005C5230` is left; that poll counts as a poll in every other shape, as it does in the population table of [native commands](native-commands.md) |
| `arg_callback` | the callback that pops the arguments (`begin` or `result`); blank when that callback is the stub or the record is empty |
| `pops_int`, `pops_float`, `pushes`, `result_writes` | counted direct calls of `00267E10`, `00267DB0`, the two push helpers and the two result writers in that callback; a handler that pushes constants and delegates to a shared body pops there, so these are not the argument count, which `arity` carries |
| `guard` | the predicate that makes a pop conditional, where one exists (`00263D00` for the class-3 forms) |
| `arity`, `arity_status`, `net_or_sums` | the measured argument count; `CONFIRMED` equals the catalogue, `CONFLICT` differs from it, `DERIVED` has no catalogue value, `GUARDED` and `CONDITIONAL` take two values (`lo\|hi`) depending on the guard |
| `result_body` | the result handler's control flow: `CONST`, `TAILJUMP`, `CALL1`, `LINEAR` (several calls, no branch) or `BRANCHING`; carried over from the earlier census, not re-measured for this table |
| `reach` | the engine subsystems the callbacks call directly, with hit counts, ignoring helpers with more than twenty callers; carried over from the earlier call-graph map |
| `us_calls` | occurrences of `verb(` in the 1,114 decompiled US scripts |

## Data

| Fact | Value |
|---|---|
| rows | 1,960 |
| shapes | result only 1,571; begin and poll 202; begin only 76; all three 48; poll only 28; poll and result 6; begin and result 1; stub 24; empty 4 |
| names | 1,270 from the catalogue (54 of them `unkCall` placeholders), 671 from other sources, 19 without a name (the 19 `DERIVED-UNNAMED` rows) |
| argument count | 1,229 confirmed against the catalogue, 653 derived, 34 guarded, 24 conditional, 19 derived without a name, 1 conflict |
| the conflict | `unkCall_5c7` (`05C7`<sub>h</sub>): the catalogue declares two arguments, the result is the `ret` stub and pops none |
| verbs called in the US corpus | 1,135 of 1,960; 1,843,441 calls in all |
| most called | `setmapidfloor` 84,066; `wait` 83,795; `setmapidwall` 76,134; `nowmap` 63,695 |
| `setforcefightmode` (`0334`<sub>h</sub>) | 177 calls in 83 scripts, every one `setforcefightmode(0)` |
| the four empty records | `setnorecovertelepostatus` `0330`<sub>h</sub>, `battlemembersync` `0356`<sub>h</sub>, `restartbattle` `03B0`<sub>h</sub>, `debug_meswin_3e` `203E`<sub>h</sub>; none is called in the corpus |

The poll-only rows are the waits on something an earlier verb started: `movesync`, `turnsync`,
`stdmotionreadsync`, `crossfadesync`, `gaugeshowsync`, `resumebehindcamerasync`,
`summonreadsync`, `summontopartyreadsync`, `behindcamerafovyrollsync`, `vibsync`, `lookatsync`,
`spattackwindowsync`, `actoriopvoicereadsync`, `entryreadsync`, `behindtoeventcamerasync`,
`moviestandbysync`, `movieplaysync`, `bgmstreamreadsync`, `bgmstreamplaysync`, `gillwinsync`,
`ucmovesync`, `initsync`, `musicfadeoutsync`, `unkCall_5a6`, `fsmenu_syncopenchip`,
`fsttl_opencommandsync` and `fsttl_closecommandsync`.

`moveblurfadesync` (`03BD`<sub>h</sub>) also counts as poll only: its begin and result are the stub and its
poll `00345100` is live.

The stub rows hold only the `ret` at `0016D6A0` and the poll `005C5230`, which returns 0, so a
stubbed verb completes on its first call: `disposesummon`, `changetonormalparty`, `hddinstall`,
`networkhddinstall`, `hddmount`, `atrac3cancel`, `btlAtelRemoveAllEquip` and the debug verb
`20D3`<sub>h</sub> have a stub begin with that poll; `atrac3standbysync` and `atrac3playsync` have that poll
alone; `atrac3play`, `unkCall_5c7`, `btlAtelSetUnique`, `btlAtelChangeAllBtlCharaFlag_DontMoveDebug`,
the tag and setup verbs `3054`<sub>h</sub> to `305A`<sub>h</sub> and seven debug verbs have a stub result.

Two placeholder names have a known meaning: `unkCall_5be` (`05BE`<sub>h</sub>, start `00355940`) returns the
after-load flag `0209AC10` through `00286000`, and `unkCall_5bf` (`05BF`<sub>h</sub>, start `00355E80`)
clears it through `00287D00`; in the US corpus only the Trial Mode map scripts (`tri_a01` to `tri_b05`
and their siblings, 100 files) call them, 200 and 100 times. `debug_setfightstatusbyevent`
(`206B`<sub>h</sub>, `0050C910`) pops one int and stores it through `003BA300`, so its argument count is 1.

### Helpers behind the handlers

Several handlers do their work through small helpers. An actor's presentation binding is `[actor + C0h]`;
its first word is the render index, -1 when the actor has no model.

| Helper | Verbs | Does |
|---|---|---|
| `002E7DD0(actor, run)`, `002E7E10(actor, run)` | `getdefaultwalkthresholdspeed` `0272`<sub>h</sub>, `getdefaultrunspeed` `0246`<sub>h</sub> | the model parameter (`003E6150`) `09000707`<sub>h</sub>, or `09000101`<sub>h</sub> for a non-zero second argument; and `09000808`<sub>h</sub> or `09000202`<sub>h</sub>; 0 without a model |
| `002E9B10(actor)` | `raturn` `025D`<sub>h</sub>, `raturna` `025F`<sub>h</sub>, `raturnya` `02D5`<sub>h</sub> and their relatives | the model parameter `09000909`<sub>h</sub>, or pi/30 (`00D0F8E4`) without a model |
| `002E30D0(actor, on, a, b)` | `unkCall_5bd` `05BD`<sub>h</sub> | `00382B50(render index, a, b)`, or `00382B50(-1, 0, 0)` when `on` is 0 or there is no model |
| `002EC860(actor, on)` | `motionloop` `003B`<sub>h</sub> | bit 3 of the binding's byte `+11`<sub>h</sub> |
| `002EC940(actor, v)`, `002EC960(binding, v)` | `motionlooppreset` `04B4`<sub>h</sub>, `puppetmotionlooppreset` `04E6`<sub>h</sub> | the binding's `+2A`<sub>h</sub> |
| `002ECC60`, `002EC970`, `002EC8B0` | `motionstartframe` `00F5`<sub>h</sub>, `motionloopframe` `00F4`<sub>h</sub> | the binding's `+14`<sub>h</sub>, `+18`<sub>h</sub> and `+1C`<sub>h</sub> from a frame number; a positive frame passes through `003DA190`, which returns its argument |
| `002ECDC0(actor, on)`, `002ECE00(actor, on)` | `shows_3a` `003A`<sub>h</sub>; `showw_39` `0039`<sub>h</sub>, `hidew` `0035`<sub>h</sub> | for a kind-`60`<sub>h</sub> actor not in mode 1 (`+18`<sub>h</sub>): bit 0 of the binding's `+70`<sub>h</sub> or `+40`<sub>h</sub>, then the visibility refresh `002E8FD0` |
| `003EB470(bind)` | `puppetbind` `041B`<sub>h</sub>, `puppetbindoff` `041A`<sub>h</sub>, `debug_modelinfobindoff` `20A8`<sub>h</sub> | releases a puppet bind: the model (`002ED470`), the user count `+1C`<sub>h</sub> of the bound record (`002EB870`), the binding reset (`00265F90`), and the record goes back to the free list `02B5EB70` |
| `003590B0()` | `ucmove` `009A`<sub>h</sub>, `ucmove_52b` `052B`<sub>h</sub> | the average of `022C7FF0` and `022C7FF4` |
| `0035A8D0(on)`, `00363B00(mode, pos, v)` | `ucon` `000D`<sub>h</sub>, `ucon_4a5` `04A5`<sub>h</sub> (through `0026C5D0`); `00363B00` also `set_microphone_pos` `056A`<sub>h</sub> | `0035A8D0` sets or clears bit 5 of `+9` on the four party actors (`00263750`) and refreshes their models and bindings; `00363B00` stores the mode at `022CBA9A` and, for mode 1, the position at `022CBB10` and `v` at `022CBAAC` |
| `00378F90(on, group, n)`, `00379BD0(map, group, n)` | `setbgnpcstatus` `0406`<sub>h</sub> | set or clear the flag of every background NPC whose id (16-byte entries at `[0209A670] + 1A0h`) has `id / 100` = group and `id % 100` = n, or any n for a negative one (12-byte flags at `+1D8`<sub>h</sub>) |
| `003DF790(v)` | `fieldsign` `0176`<sub>h</sub> | 0 gives 3, 1 gives 2, anything else 1 |
| `003DF7B0(bit, off)`, `003DF810()` | `showfieldsign` `0172`<sub>h</sub>, `hidefieldsign` `0173`<sub>h</sub> | set or clear a bit of `02B59D18`; `003DF810` hands the highest live slot of 8 (`02B59CC0`) to `002900C0`, or clears the sign |
| `003E88C0(mode, id)`, `003E8900(mode, id)` | `animeplay` `0213`<sub>h</sub>, `animeplaytiming` `0280`<sub>h</sub> | on the `ACTL` record of the id ([MPK map pack](../World-Areas-And-Travel/mpk-map-pack.md)): `+15`<sub>h</sub> = mode, state bit 4 set and bit 3 cleared; the mode nibble of `+12`<sub>h</sub> becomes 0, or 1 for the timing form |
| `003E8890`, `003E8860` | `animepause` `0218`<sub>h</sub>, `animepauseclear` `0219`<sub>h</sub> | set or clear the record's state bit 3 |
| `003E8BF0`, `003E82F0` | `animestop` `0215`<sub>h</sub>, `animesync` `0214`<sub>h</sub> | run `003E8C50`, or return the test `003E8350`, on the record with the aux table and the weather slot (`00265920`) |
| `003E8AA0(mode)` | `animesync`, `skipexec` `0539`<sub>h</sub> | hands every record whose `+15`<sub>h</sub> is the mode (any for a negative one) and whose light `+08`<sub>h</sub> is set to `0037A500` |
| `003E8F70(type)` | `setgaugecountertype` `01C1`<sub>h</sub>, `setgaugetimertype` `01C2`<sub>h</sub>, `setgaugeracetype` `0348`<sub>h</sub> | `00408A20` with 1 to 4, or 0 for any other type |
| `003E9120(i, r, g, b, a)` | `setgaugecolor` `01CC`<sub>h</sub> | stores the colour in entry i (0 to 3) of `02B5D098` and passes all four to `00408780` |
| `003E9190()` | `setgaugeraceiconparty` `0371`<sub>h</sub> | `002E9FE0` on each of the four party actors |
| `003E9480`, `003E95E0`, `003E9640` | `setshapeclut` `0184`<sub>h</sub>, `setshapeprior` `018C`<sub>h</sub>, `setshapesampling` `0185`<sub>h</sub> | on shape i of the map's shape list (`002E1040`, `60`<sub>h</sub>-byte entries): the palette nibble `+0D`<sub>h</sub>, the priority `+0E`<sub>h</sub> (marking the list dirty, `+3F2`<sub>h</sub> and `+3F3`<sub>h</sub> bit 5), or bit 5 of `+08`<sub>h</sub> |
| `003EA5C0`, `003EA4B0` | `voicechangevolume` `00B3`<sub>h</sub>, `voicechangepan` `00B4`<sub>h</sub> | for a voice slot in state 3 (`02B5D0B4` + `40`<sub>h</sub> x slot), entry i of its table for the current language (`002DEBB0`) goes to `001DC350` or `001DC240` |
| `003944D0()`, `00394500()` | `fsttl_opencommandsync` `705F`<sub>h</sub>, `fsttl_initialize` `7055`<sub>h</sub> | 0 while `01EFAC12` is 2 and bit 1 of `[02AEE4C8] + C4h` is clear, else 1; and bit 0 of `[02AEE4C0] + C0h`, 0 with none |
| `00233D50()` | `unkCall_3091` `3091`<sub>h</sub> | whether world lock 10 is free (`00226BD0`) |
| `00235DD0(unit, x, z)`, `00237460(point, unit)` | `btlAtelGetAngleDiff` `3063`<sub>h</sub>, `btlAtelIsPcOnPoint` `3045`<sub>h</sub> | for the unit (`0031B810`, or `003272A0` for a negative one): the angle in degrees from its facing `+160`<sub>h</sub> to the point (`0031AC90`, `0031A930`), -1.0 without a unit; and `002374E0` on its position and the point `003209C0` gives, -1 without one |
| `00237D60()` | `callgameover` `04D8`<sub>h</sub> | `0035C7A0(Bh)` unless `0035C700` answers non-zero; returns 1 |
| `0035EA00(v)` | `debug_set_syncv_mode` `20C4`<sub>h</sub> | `00368AA0(2, v = 0)` and `022CA608` = v |
| `0036F050()` | `debug_recoveriopvoice` `20B6`<sub>h</sub> | for each of the two banks in state 2 (`022D9B40`, `022D9B41`): state 1, `001DC0C0(bank)` and `0036ED50` on its slots in state 3 |
| `00377560(n)`, `002637B0(i)` | `debug_setmapdefaultpos` `202A`<sub>h</sub> | puts party slot n's actor (`002637B0`: the id at `[0209A1F0 + 8 x i]`, -1 for i of 4 or more) at the map's default position (`[[0209A678]] + 28h`, `+2C`<sub>h</sub>) through `0026AF80` |
| `002593D0()`, `00259470()` | `setinterventioncamera` `02B9`<sub>h</sub> (through `00359410`) | copy the `860`<sub>h</sub>-byte block at `02097D20` to `02098580`, and back |
| `002EAA30(i)` | `set_summon_effect_filter_status` `0508`<sub>h</sub> (through `003B7130`) | `003B5180` with entry i of the table `01EEBAA0`, which `002EA030(i)` returns for `003B4B60`, `003B50E0`, `003B5180` and `003B5470` |
| `0053F460()` | `fsroll_start` `703E`<sub>h</sub> (through `005115D0`) | when the staff roll `[02CA8A80]` exists: places it (`0053E580`), re-attaches it (`00246AC0`) and sets its running byte `+FC`<sub>h</sub> |
| `0053E580(roll)` | `fsroll_start` | with the start mode `+104`<sub>h</sub> 1 or 2 (commands `C`<sub>h</sub> and `D`<sub>h</sub> of `0053F0D0`), finds the first line of the table `+C0`<sub>h</sub> (count `+C8`<sub>h</sub>, `20`<sub>h</sub> bytes each) with id `+0C`<sub>h</sub> equal to `+10C`<sub>h</sub> and kind `+18`<sub>h</sub> below 3 (mode 1) or equal to 3 (mode 2), and starts the roll at `[+10Eh] - (screen height 01E0C1DC - [line + 16h]) / 2 + [line + 10h]` (`+F0`<sub>h</sub>) |
| `0053EDB0()` | `fsroll_refresh` `704E`<sub>h</sub> (through `00511D00`) | frees the roll's line table and clears `+C0`<sub>h</sub> to `+1497`<sub>h</sub>, then takes a new `10000`<sub>h</sub>-byte table (`00249810(2)`) and resets the start `+F0`<sub>h</sub> to the screen height, `+1494`<sub>h</sub> to `80`<sub>h</sub>, `+FF`<sub>h</sub> and `+102`<sub>h</sub> to 1, and the three faces' words `+CE`<sub>h</sub>, `+D6`<sub>h</sub>, `+DE`<sub>h</sub> to `202`<sub>h</sub> with scales `+D0`<sub>h</sub>, `+D8`<sub>h</sub>, `+E0`<sub>h</sub> of 1.0 |
| `00253C20()` | `debug_isopen_triangle_menu` `2030`<sub>h</sub> (through `002E05C0`) | 1 when `00290410` answers non-zero and `02092730` is 0 or 3 |

The puppet binds are a pool of 32 records of `48`<sub>h</sub> bytes from `02B5E120`: `003EB750`, run by the boot
`00266D10`, links them into the free list; `003EB500`, run by the area unload `002628B0`, releases every bound
one and `003EB5F0(v)` those whose byte `+41`<sub>h</sub> is v. `00265F90(binding)` resets a binding: render
index -1, the three floats at `+14`<sub>h</sub>-`+1C`<sub>h</sub> to -1.0 and the default flags.

## Related

- [Verb dispatch](verb-dispatch.md): how a call id reaches these records.
- [Native commands](native-commands.md): what the three callbacks and the shapes mean.
- [Script interpreter](script-interpreter.md): the call opcodes.
