# AO-4 — what the script command families 3, 5 and 7 contain

FABLE, Claude Opus 5.5, 2026-09-27. **NATIVE/STATIC. Nothing was executed.**
Control: `ao4_families.py` (6 checks, FAILS 0).

The records are the dispatch-table page's `0x20`-byte records: begin at `+0`, poll at `+8`, result at `+0x18`, from
table `+ 8`. Names come from the authored catalogue (`CScriptContainerInitializers.cpp`). Family 7 joins that catalogue
one to one (the lifecycle page's AO-6 census). A name is a label. What each group does is read from the handlers.

## Family 7 (104 records): the front end — fullscreen menu, staff roll, title screen

The catalogue names fall into five prefixes, and each prefix runs on its own native cluster (**F1**, **F2**):

| prefix | records | ids | native cluster |
|---|---:|---|---|
| `fsmenu_` | 55 | `7000`–`702C`, `7032`–`703B` | the fullscreen-menu object. 65 of family 7's 131 callbacks open with the menu-present guard `00280120` (the verb-dispatch page, mechanism 2). |
| `fs_` | 6 | `702D`–`7031`, `7061` | by name, the stone and food windows (`002A7E20`, `002A1D40`, with the shared close `002A1D20`); `fs_setclanrank` and `fs_reloadmrp` are inert (below) |
| `fsroll_` | 31 | `703C`–`7054`, `705E`, `7062`–`7066` | the staff roll: every handler reaches only `0053D000`–`0053F800` and the inert stubs |
| `fsttl_` | 11 | `7055`–`705D`, `705F`, `7060` | the title screen: every handler reaches only `00394000`–`00394700` — the title-asset singleton's code ([its page](../../../16-UI/Widget-Object-Model/the-title-asset-singleton-and-its-distinct-consumer.md)) |
| `unkCall_7067` | 1 | `7067` | the same title range: it writes the load-mode byte ([the version-stamps page](../../../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/version-stamps-and-what-loading-normalises.md)) |

F2 is an exclusion check. No `fsmenu_` or `fs_` handler reaches the roll or title ranges, and no roll or title handler
reaches outside its own range. It has three positive controls:
- `fsroll_start` reaches `0053F460`;
- `fsttl_newgamestart` reaches `00394640`;
- `fsmenu_openmenu` reaches `002D75F0`.

**The staff roll is a list of typed lines (F3).** Fifteen `fsroll_` verbs append through one appender, `0053F0D0`, and
nothing else calls it: a raw rel32 sweep of `.text` finds exactly their 15 call sites. The appender:
- reads the singleton `02CA8A80`;
- accepts kinds 1–14 only;
- caps the list at `0x800` lines of `0x20` bytes (count at `+0xC8`, array at `+0xC0`).

The fixed-kind verbs pass these kinds:

| kind | verbs |
|---:|---|
| 1 | `speed` |
| 2 | `linedisp` |
| 3 | `layout` |
| 4 | `blank` |
| 5 | `nameA` / `nameB` / `nameC`, with column 0 / 1 / 2 |
| 6 | `data` |
| 7 | `stop` |
| 8 / 9 / 10 | `fontA` / `fontB` / `fontC` |
| 11 | `setend` |
| 14 | `moviewait` |

`fsroll_setparam` passes a kind it pops, so kinds 12 and 13 are reachable only through it. The font scales go through
the sibling `0053F3F0` with the same 8/9/10, and `fsroll_fade` through `0053EFC0`.

**Six records do nothing observable (F4):**
- `fs_setclanrank`, `fsroll_setcounternow` and `fsroll_setdouble` pop their operands, then jump to the ret-0 stub
  `0016D6A0`.
- `fsroll_getcounternow` and `fsroll_getcountermax` share `0050F100`, which returns `005C5230`'s constant 0.
- `fsroll_getdouble` returns `0053DD10`'s constant 1.
- `fs_reloadmrp`'s begin is the stub. Its poll reports finished on the first call: `0053DD10` returns 1, so `sete`
  gives 0.

## Family 5 (1 record): a copy of family 7's first record

Its one record is identical to `fsmenu_wait` (`7000`): begin `003567F0`, poll `005114F0`, no result (**F5**; the
lifecycle page's earlier finding, re-measured).

## Family 3 (147 records): the battle-actor verbs

140 of the 147 records are catalogued (**F6**):
- 133 are battle names: `btlAtel*` 121, `btlGet*` 6, `btlSet*` 6;
- the other 7 are `unkCall_*`;
- the lifecycle page lists the seven uncatalogued ids.

75 of the family's 141 non-stub handler slots are already cited on database pages outside `_index`. The `btlAtel*`
names recur on the spawn and encounter pages (`05-Spawn-Encounter-Lifecycle`) and the battle-unit pages
(`04-Actor-Entity`), and the auto-status rebuild reads `btlAtelSetAbility` and `btlAtelSetStatus`. That count is a
grep of the handler addresses and is not part of the control.

The row's earlier word "spawn" fits only part of the family. `btlAtelSetUnit` (`0x3001`) is the spawn entry, but the
family as a whole is the battle-side actor and encounter set.

## What this does not claim

- **Per-verb semantics.** This record does not give them for the 55 menu verbs. They drive the menu object's methods,
  which belong to the UI pages.
- **Whether the fullscreen menu can be absent while a script runs.** BQ-10 already covers that case.
- **Anything live.** All of this is static.
