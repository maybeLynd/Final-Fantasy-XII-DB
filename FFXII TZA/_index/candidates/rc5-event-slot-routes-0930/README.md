# RC-5: the names and event ids the event-slot routes can store (ORACLE, 2026-09-30)

Input for `RC-5` ([the event slot panel and its feeder](../../../00-Engine-Core-Runtime/Developer-Tuning-Console/the-event-slot-panel-and-its-dead-feeder.md)
section 6). SWE2-CONTRACT registered the row. Static evidence from the shipping image (`73461d08…`) and the shipped
scripts. **Verdict: NARROWED** (the residue is stated at the end).

## The question

The name-classifying setter `0020AC30` is reached from `0032FD64` in `ActorResource_BeginManagerResourceSetLoad`
(`0032FCA0`), and its path comes from `002DF980(kind, id)`. Which `(kind, id)` paths does that load hand the setter?
Which event ids do the pusher sites `0026B775`, `00354B6D` and `00354EDA` pass to `0020AF10`?

## Method

**Original code, read.**
- `0032FCA0` (`0032FD19`..`0032FD64`).
- The setter `0020AC30`, its regex check `0020A800` and its extractor `0020AA50`.
- The pusher `0020AF10`.
- The three pusher callers, and the handlers that reach `0026B750`: `0034C9A0` and `0034CED0`.
- All eight callers of `0032FC30`, the only caller of `0032FCA0`, and the value sources behind them: `003CA140`,
  `00309230` and `0050D0C0`.

**Three scripts.** All report FAILS 0.

- **[`rc5_paths.py`](rc5_paths.py)** (outputs [`rc5_paths.out`](rc5_paths.out), [`rc5_paths.tsv`](rc5_paths.tsv)).
  - It replays `ResourcePath_Init` (`002DF9A0`) for all 13 region arms. It reads the resulting `g_pathTables` arrays
    for kinds 8, 5 and 1, and applies `0032FCA0`'s row formula to each.
  - It then applies the setter's own regex (read from `00905958`) and the extractor's rule. The extractor takes the
    text between the last `\` and the last `.` (`0020AB60`..`0020ABE5`).
  - It classifies each stored name as the setter does, and checks each path against the shipped archive's index.
  - Controls:
    - the regex literal must match the page's text;
    - kind 5 row 0 must end in `tst_a01.ebp`;
    - `0020ADD6` / `0020AE16` must decode as the byte stores to the two flags.
- **[`rc5_verbs.py`](rc5_verbs.py)** (outputs [`rc5_verbs.out`](rc5_verbs.out), [`rc5_verbs.tsv`](rc5_verbs.tsv)).
  - It walks every shipped `.ebp` script with the database's EBP2 walk and bytecode decoder, which it reuses:
    `25-EBP-Script-Container/…/gen_req_channel_census.py`, as `script_award_verb_census.py` does.
  - It resolves the pushed operands of every call to verbs `0xEB`, `0xEC`, `0x11B`, `0x4B3`, `0xE7`, `0xE8` and
    `0x198`.
  - Control: the `0x11B` site count must equal the committed `script-award-verb-census.tsv`, which is 34,125. It does.
- **[`rc5_join.py`](rc5_join.py)** (output [`rc5_join.out`](rc5_join.out)).
  - It joins the authored set ids with the kind-8 names.
  - Control: set id 212 must name `pre_z0000`.

**Decompiler.** `evctrl.ebp` was decompiled once with ff12-script, to read the `summoneventread` operand expression.

## Result

### The setter's `(kind, id)`

`0032FCA0(m, s)` takes the manager index `m` and the set id `s`. It picks `(kind, row)` as follows
(`0032FD19`..`0032FD44`):

| manager index `m` | kind | row | what those rows hold | rows passing the setter's regex |
|---|---|---|---|---|
| 1, 2, 3 | 8 | `4*s` | `PS2Data\plan_master\<locale>\event\<area>\<scene>\<scene>.ebp` | 329 of 329 |
| 0, or 5 and above | 5 | `3*s` | `PS2Data\plan_master\<locale>\plan_map\…\global\<map>.ebp` | 0 of 709 |
| 4 | 1 | `s + 0x6B` | nothing: every region's kind-1 array ends at row 34 (46 in one region) | none |

Two gates come before the setter:
- `0032E400(kind, row) > 0` (`0032FD4D`), the size-table lookup;
- `002DF980`, which returns the row's pointer.

The setter then clears both flags and sets the marker before it validates the path. So:

- **Kind 8 (managers 1 to 3).** This is the only kind whose paths reach the name store.
  - There are 329 event-script paths, for set ids 30 to 740.
  - The `(set id, name)` pairs are identical in all 13 region arms. Only the locale directory differs.
  - 326 of the 329 `us` paths are in the shipped archive. The three that are not: `chb_z0000` (set id 355),
    `msg_z0000` (398) and `men_z0004` (440).
- **The name stored is the file stem**, for example `nal_a0100`. Of the 329 stems:
  - 13 are `sum_<x>0001` (set ids 41, 44, …, 77), which set **flag A** `01F832E8`;
  - 26 are `sum_<x>0000` / `sum_<x>0002`, which read their cutscene JSON and set no flag;
  - 1 is `spc_z0000` (set id 210), which sets **flag B** `01F832E9`;
  - the other 289 set nothing.
- **Kind 5 (manager 0).** Every kind-5 path is a `plan_map` global script, and none matches the `\event\` regex. A
  manager-0 load therefore clears both flags and stores no name. **Slot 0's name is never set.**
- **Manager 4 is never loaded through this route.**
  - No caller of `0032FC30` passes 4. `0050D0C0`, the one that forwards an operand, diverts 4 to `00314410`
    (`0050D0DC`). The other callers pass 0 to 3.
  - If 4 were passed, its kind-1 row would lie past the array.

**Where the set ids come from.** The eight call sites of `0032FC30`:

| call site | manager | set id |
|---|---|---|
| `0025DAED` (`0025D9E0`, manager 0's update) | 1 | literal 212: `pre_z0000` |
| `00306C56` (`00306BD0`) | 3 | `00309230`: the 13-entry table 42, 45, …, 78 by actor type `0x1B`..`0x27` (the `sum_<x>0002` names), or the word at `+0x24` of the record it is given |
| `003CA07C` (`003C9FD0`) | 3 | `[02B4774C]`, set by `003CA140(k)` to 437, 438, 439 or 440 (`men_z0001`..`men_z0004`) |
| `003140BA` (`00314020`) | 0 | `[01EED064]` (kind 5, no name) |
| `00352304` (verb `0xE8` `eventread_e8`) | first operand + 1, clamped to 1..3 | second operand |
| `003530CF` (verb `0xE7` `eventread`) | `[r8]` + 1, clamped to 1..3 | `[r8+4]` |
| `003535A3` (verb `0x198` `summoneventread`) | 3 | the operand |
| `0050D115` (`0050D0C0`, battle-family verb `0x202D` `debug_eventload`) | `[r8]`, with 4 diverted | `[r8+4]` |

**From the authored scripts** (all nine locale copies):
- **`eventread`:** 1,413 sites, all in map scripts. There are 69 distinct constant set ids, and every one names a
  kind-8 event path.
- **`eventread_e8`:** 5,482 sites. There are 256 distinct constant set ids, and 226 of them name event paths. There
  are 40 non-constant sites (script variables), in the controllers `image/ff12/<loc>/bin/ctrl.ebp` and `evctrl.ebp`,
  which ship in two copies (`ch` and `in`).
- **`summoneventread`:** 4 sites, all in `evctrl.ebp` (two per copy). The set id is a menu choice (`aask`) plus 39 on one menu page
  and plus 57 on the next, which lands in the `sum_` run.
- **No constant authored set id selects a `sum_` or `spc_` name.** Such a name can reach the setter by these routes:
  - `summoneventread` in `evctrl.ebp`;
  - the non-constant `eventread_e8` sites;
  - `00306BD0`, which selects the `sum_<x>0002` names from its table (no flag), or a `sum_`/`spc_` name through the
    record word `+0x24`;
  - `debug_eventload`.

### The pusher's event ids

- **`00354B6D` (verb `0xEC` `eventplay_ec`) and `00354EDA` (verb `0xEB` `eventplay`) always pass −1.** Each sets
  `edx` with `or edx, 0xffffffff` (`00354B68`, `00354ED5`), and the pusher refuses −1 (`0020AF66`).
  - The only effects are two stores made before the refusal: the slot's name is copied into `01F832C8`, and the marker
    `01DFE40C` is set to the slot (`0020AF4A`..`0020AF5B`).
  - The slot is the operand + 1, clamped to 1..3. `001EC680` has already set the marker.
  - **These two sites never queue an id.**
- **`0026B775` (in `0026B750`) passes the scene id of verb `0x11B` `startscene` or verb `0x4B3` `startscene_4b3`.**
  - From `startscene`, it is the popped operand (`0034C9A0` → `jmp 0026B750`).
  - From `startscene_4b3`, it is the second pop, which is the first pushed operand (`0034CED0` → `call 0026B750`).
  - The slot is the running script's own manager index, `[[02099D70] + 0x28]`.
  - The id is queued only if the slot is 4 or less, the id is not −1, and the slot has a name. That means only for a
    script running in manager 1, 2 or 3 after a kind-8 event path was loaded into that slot.
  - Authored values (all nine locale copies):
    - **`startscene` in event scripts:** 29,502 sites. 26,073 are constant, with 126 distinct values from 0 to 2000.
      3,429 pass a script variable (`PUSHV`).
    - **`startscene` in map scripts:** 4,623 sites, with 53 distinct constants from 0 to 10000. These run in manager 0,
      whose slot has no name, so the pusher refuses them.
    - **`startscene_4b3`:** 1,260 sites, all in event scripts. There are 36 distinct constants from 1 to 45, and 45
      non-constant sites.
    - No authored site passes −1.

## Residue (why NARROWED)

1. **Runtime values of the non-constant operands:**
   - the event ids at 3,429 `startscene` sites and 45 `startscene_4b3` sites;
   - the set ids at 40 `eventread_e8` sites and 4 `summoneventread` sites (menu choices in `evctrl.ebp`).

   Script dataflow could bound these further. The value a play session takes is runtime.
2. **The authored `+0x24` word of the record `00306BD0` hands to `00309230`.** This is battle data, not enumerated
   here. It is the one non-debug route by which a `sum_<x>0001` name, and so flag A, could be set.
3. **The operands of the battle-family verb `0x202D` `debug_eventload`** (`0050D0C0`). They were not censused.
4. **Which region arm is live, and whether `0032E400`'s size gate passes for a given row.** The names and set ids are
   the same in every arm. The archive holds 326 of the 329 `us` paths.

None of these needs ASTRA as a fact that static code and authored data cannot reach, except the runtime choice in
item 1.

## Not claimed

- **Retail reachability.** That retail play reaches any given route, including whether `evctrl.ebp`'s menu is reachable
  (see `sn1-evctrl-jump-binding` in the evidence tree for that controller).
- **The `eventread` operand.** Reading its single operand as the set id is inferred:
  - the handler reads the manager at `[r8]` and the set id at `[r8+4]`;
  - the catalogue gives the verb one argument;
  - all 69 constants name event paths.
- **Evidence form.** The censuses are over decoded bytecode with the database's stack-walk resolver. They are not a
  decompilation of every script.
