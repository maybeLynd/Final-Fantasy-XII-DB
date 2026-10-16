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
poll `00345100` is live.

The stub rows hold only the `ret` at `0016D6A0` and the poll `005C5230`, which returns 0, so a
stubbed verb completes on its first call: `disposesummon`, `changetonormalparty`, `hddinstall`,
`networkhddinstall`, `hddmount`, `atrac3cancel`, `btlAtelRemoveAllEquip` and the debug verb
`0x20D3` have a stub begin with that poll; `atrac3standbysync` and `atrac3playsync` have that poll
alone; `atrac3play`, `unkCall_5c7`, `btlAtelSetUnique`, `btlAtelChangeAllBtlCharaFlag_DontMoveDebug`,
the tag and setup verbs `0x3054` to `0x305A` and seven debug verbs have a stub result.

Two placeholder names have a known meaning: `unkCall_5be` (`0x05BE`, start `00355940`) returns the
after-load flag `0209AC10` through `00286000`, and `unkCall_5bf` (`0x05BF`, start `00355E80`)
clears it through `00287D00`; in the US corpus only the Trial Mode map scripts (`tri_a01` to `tri_b05`
and their siblings, 100 files) call them, 200 and 100 times. `debug_setfightstatusbyevent`
(`0x206B`, `0050C910`) pops one int and stores it through `003BA300`, so its argument count is 1.

## Related

- [Verb dispatch](verb-dispatch.md): how a call id reaches these records.
- [Native commands](native-commands.md): what the three callbacks and the shapes mean.
- [Script interpreter](script-interpreter.md): the call opcodes.
