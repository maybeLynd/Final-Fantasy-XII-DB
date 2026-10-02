---
system: Native command lifecycle — begin / poll / result
category: 01-Script-VM-Native-Bridge
status: "DOCUMENTED — every register row the page names is answered; owner read and re-status 2026-10-01 (OPUS, batch 23): the SECTION-11 trigger is resolved (accepted by a non-author review 2026-09-29); families 3, 5 and 7 and the default aliasing answered (AO-1, AO-4); the byte the polls test is the manager skip mask (OV-15); a skip is set when the player skips an event cutscene (RC-17, answered by FABLE; ORACLE's two corrections adjudicated by OPUS 2026-10-01, both hold) (status line current 2026-09-30, SWE2-CONTRACT)"
owner_layer: PrimaryOwner:Script_VM_Native_Bridge
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: "snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30"
    verified: "re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS"
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-07
audit:
  passes: 5
  last_pass: 2026-09-07
  last_pass_state: GN160-xiionline-61-all-null-record
  crossref_clean: true
  reopened_count: 0
local_production_date: 2026-09-23
local_production_status: "SECTION-11 locally validated; accepted non-author 2026-09-29 (SWE2-AUDIT-SEM, OV-18)"
---

> **SECTION-11 current production (2026-09-23):** EXP-085 already executed the lifecycle with
> planted callbacks; this section connects the real interpreter, initializer, wait begin/poll and
> selected original result callbacks. The actor-control/request-phase conflation in CE-5 is corrected
> below. Completed phases reset0, full stack can suppress delivery, and target/issuer are distinct.
> [Current contract](../CONTRACT-native-command-lifecycle.md) ·
> [Original-code evidence](../../_experiments/evidence/continuation-section11-script-resume/REVIEW.md). Historical audits do not certify this rewrite.



# Native command lifecycle — begin / poll / result

> How a cutscene says "walk over there" and then *waits* — the three-callback structure behind every
> script command, and the 4-bit family field that organises all 1,960 of them.

**Historical DOCUMENTED assessment; current corrections require review.** The id encoding, the family tables, the three-callback record layout, the phase
machine and the return-value list are all read — the lifecycle end to end. What remains open is the
*contents* of families 3, 5 and 7 and the default-table aliasing, not the mechanism.
*(Reconciled 2026-09-30, SWE2-CONTRACT: the review is done — SWE2-AUDIT-SEM re-executed SECTION-11's
`run_review.py` non-author and accepted it (`FRONTIER-REVIEW-AUDITSEM-OV-ACCEPTANCE-0929`, OV-18); the default aliasing
is AO-1 (answered 2026-09-12) and the families' contents AO-4 (answered 2026-09-27), both in §7.)*

## 1. What the player sees

Every scripted moment in FFXII — a character walking to a mark, a camera move, a line of dialogue
holding until it is dismissed — is a script issuing a command and then **waiting for it to finish**.
The script does not busy-loop and the game does not freeze: the command is started, polled every
frame while it runs, and produces a result when done.

That three-part shape is why cutscenes can interleave, why a scripted walk survives a frame-rate
change, and why a command can be *in progress* as a state the engine tracks.

## 2. Native mechanism

### Command ids are packed: family and command

`VMNativeCommand_ExecuteLifecycle` (`002621D0`) splits the incoming id:

```c
family  = id >> 12;        /* sar r12d, 0xC   -> 0 .. 15 */
command = id & 0xFFF;      /* and r15d, 0xFFF -> 0 .. 4095 */
```

**Four bits of family, twelve of command.** That is why there are exactly sixteen family tables — the
field width decides it.

### Sixteen families, four distinct tables

`VMNativeCommandDispatch_InitializeFamilyTables` (`003DC2D0`) fills an array of 16 pointers at
`0x02B57EF0`: it `rep stosq`s all sixteen with a default, then overwrites four.

| family | id range | table | commands |
|---:|---|---|---:|
| **0** | `0x0000`–`0x0FFF` | `0x01EED700` | **1,496** |
| **3** | `0x3000`–`0x3FFF` | `0x01F281B0` | **147** |
| **5** | `0x5000`–`0x5FFF` | `0x01F29418` | **1** |
| **7** | `0x7000`–`0x7FFF` | `0x01F29440` | **104** |
| 1, 2, 4, 6, 8–15 | — | `0x01F26720` | 212 *(shared)* |

**Twelve families share one table**, so their ids alias — `0x2005` and `0x4005` resolve identically.
Whether that is deliberate aliasing or a fallback for unimplemented families is **not established**
(**AO-1**).

Total distinct commands across the four real tables plus the default: **1,960**. The authored catalog
carries **1,954** verb names. The two figures are close but **not equal**, and no claim is made here
that they should be.

### Three callbacks per command

The three accessors fix the record layout exactly:

```
GetBeginCallback  (003DC270):  *(void **)(tbl +  8 + 32*command)
GetPollCallback   (003DC240):  *(void **)(tbl + 16 + 32*command)
GetResultCallback (003DC2A0):  *(void **)(tbl + 32 + 32*command)
```

All three bounds-check `command` against `*(int *)tbl` — the count — and return `NULL` when the
family table pointer is null or the index is out of range. So:

```
tbl + 0                     int    command count
tbl + 8 + 32*N              ptr    begin  (N)
tbl + 16 + 32*N             ptr    poll   (N)
tbl + 24 + 32*N             ptr    unused - NULL IN ALL 1,960 RECORDS
tbl + 32 + 32*N             ptr    result (N)
```

**Most commands are instantaneous** and carry only a `result` — which is exactly what the
[dispatch-table document](../scriptvm-native-dispatch-table.md) measured when it found 1,155 of
1,496 records with a single non-null field.

> **CORRECTED 2026-09-02.** This document previously described the `+24` slot as *"unused in every
> record but one"*. **It is unused in all 1,960 records of all five tables.** The one exception was a
> read **16 bytes past the end** of family 0, which landed on `0x00000000FFFFFFFF` — filler between
> the command table and the float table that follows it, and not a pointer at all. Full working in
> [the dispatch-table document](../scriptvm-native-dispatch-table.md) §13.

### The executor

`VMNativeCommand_ExecuteLifecycle` (`002621D0`, 461 B) reads a **phase byte** from the command's
state block at `+0x15` and branches three ways — `0`, `1`, and `>= 2` — fetching the poll callback up
front and the begin or result callback per phase. Where a callback is absent it takes an alternative
path rather than failing.

**But `begin`, `poll` and `result` are not three separate visits.** Phase `0` runs `begin` and then
*falls through* to `poll`; if `poll` says the command is not still running, execution falls through
again to `result` **in the same call**. So an instantaneous command — one with only a `result`
callback — completes on its very first invocation even though the phase byte starts at `0`, because
the absent `poll` yields "not running" from a zeroed local. Only a command that polls busy ever
leaves phase `1` behind for the next eligible invocation. Section12 and Section11 distinguish this from measured live frame timing.

It also appends the finished command's **return value** to a 63-entry result list at `rbx`, a
structure-of-arrays with a count, a type tag, and two value words per entry. Read in full in
section 11.

## 3. What this settles elsewhere

**I-3 is answered.** The dispatch-table document asked where the `0x2000+` "developer/debug" verbs
dispatch from, with 468 catalog entries unaccounted. They are **family 2** — `0x2000 >> 12 == 2` —
and family 2 uses the shared default table. They were never missing; they were in a different family,
and that document could only see family 0.

**The dispatch table is family 0's `result` column**, as established in that document's section 12.
This document supplies the frame it was one column inside.

## 4. Key addresses

| Address | Role |
|---|---|
| `0x02B57EF0` | the 16-entry family table array |
| `0x01EED700` | family 0's command table — 1,496 commands |
| `0x01F281B0` | family 3 — 147 |
| `0x01F29418` | family 5 — 1 |
| `0x01F29440` | family 7 — 104 |
| `0x01F26720` | the default table shared by twelve families — 212 |
| `003DC2D0` | `VMNativeCommandDispatch_InitializeFamilyTables` |
| `003DC270` / `003DC240` / `003DC2A0` | Get **Begin** / **Poll** / **Result** callback |
| `002621D0` | `VMNativeCommand_ExecuteLifecycle` — 461 B |

## Call chain (SWE2-CONTRACT, 2026-09-30)

```
field frame -> ActorManager_RunFieldRuntimePass -> 0025DF00 per actor
  -> WorldActorScriptVM_InterpretBytecode 0025E4C0: a CALL / CALLACT / CALLPOPA / CALLACTPOPA opcode (0x58..0x5E)
     -> VMNativeCommand_ExecuteLifecycle 002621D0 (its only caller is the interpreter)    <- THIS SYSTEM
          id >> 12 -> family table 02B57EF0[family] (filled once by 003DC2D0)
          003DC270 begin / 003DC240 poll / 003DC2A0 result (bounds-checked fetch)
          phase 0: begin, then poll; poll not running -> result in the same call
          result -> the 63-entry return-value list; phase reset to 0
          an actor record through ActorManager_GetRecordByOrdinal 00358940
     -> busy: the interpreter rewinds its pc and yields until the next frame
```

**Upstream (who causes this):** a script's native-verb call opcode, once per frame per actor while the verb runs.

**Downstream (what this causes):** whatever the verb's begin / poll / result callbacks do; the result pushed back to the
script.

**Do not confuse with:** the actor request machinery (`REQ` family), which files work on another actor's channel
rather than calling a native verb ([how a script binds to an actor](../Interpreter-Core/how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md)).

- [x] **RC-17.** Which shipped scripts issue `skipexec` (command 1337) or otherwise start a manager skip, and when the
  engine's own loop over managers 1–3 in `00360710` runs — i.e. whether the skip mask the durative polls test is set in
  shipped play. Registered 2026-09-30 (SWE2-CONTRACT); static first (a call-triple census over the shipped `.ebp`
  corpus, as CR-2's was, plus the engine loop's callers).
  *Applied 2026-09-30 (records) RC-17:* **ANSWERED 2026-09-30 by FABLE (`rc151617-fable-0930`, `0870d8b62`): yes — the skip mask is set when the player skips an event cutscene** (`skipexec(1)` in 7 event scripts, `skipexec(0)` in 12, in the cutscene-skip idiom). **ORACLE (`rc15-regfile-skipmask-0930`, commit `1e4537034`) agrees on the chain and corrects two details:** `00360880` calls `00360710(n, m)` once per manager for the lowest set bit, not once per set bit; and `skipcheck` returns the entry's begun word, not the player's skip; `00228130`'s trigger is bit 13 of `[[0209AC30] + 0x400]` (the pause-menu skip confirm writes it through `00228C70` → `00285EA0`); `00228130` then runs `00360880`, which reads each event manager's own registered word (`022CB9C4`, `022CB9C8`, `022CB9CC`) and begins its lowest registered entry through `00360710`. Any of the 257 scripts that call `skipstart` can arrange this *(restated 2026-10-01 on FABLE's adjudication at `a8aed6ca9`)*. ~~**FABLE adjudication pending** on the corrections.~~ *(Corrections adjudicated 2026-10-01 by OPUS for FABLE: both corrections hold at the bytes - `00360880` runs managers 1 to 3 (`ebx`), scans bits 0-7 of each mask from `022CB9C4` (`bt` loop `003608A0`-`003608AA`) and calls `00360710` once, at the first set bit (`003608B0`); `003604A0` returns dword `[022CB738 + (n + 8m)*16]`, the begun word ([record](../../_index/candidates/opus-dd-restatus-23-1001/README.md)).)*

## 5. Data structures and formulas

```
family  = id >> 12                     4 bits, 16 families
command = id & 0xFFF                   12 bits

table   = familyTables[family]         @ 0x02B57EF0 + family*8
count   = *(int *)table
begin (N) = *(void **)(table +  8 + 32N)     valid when 0 <= N < count
poll  (N) = *(void **)(table + 16 + 32N)
result(N) = *(void **)(table + 32 + 32N)

phase   = commandState[0x15]           ON ENTRY:  0 = not started, 1 = running
                                       TRANSIENT, written by the result callback and read a few
                                       instructions later in the SAME call:
                                         2  = finished, return an int
                                         3+ = finished, return a float
                                       reset to 0 at 00262382 before the executor returns
retval  = commandState[0x0C]           read as int or float per phase

result list @ rbx
  +0x00        int    count            (max 63 entries)
  +0x04  + i   byte   type tag         1 = int, 2 = float
  +0x44  + i   byte   6
  +0x84  + i*4 dword  value A
  +0x184 + i*4 dword  value B
```

## 6. Modding notes

- **A command id carries its family.** Reading an id without splitting off the top four bits will
  send you to the wrong table.
- **Only families 0, 3, 5 and 7 have their own commands.** The other twelve share one 212-entry
  table; ids in them alias.
- **A verb with only a `result` callback is instantaneous.** If you want a command that takes time,
  it needs `begin` and `poll` too.
- **All three lookups bounds-check against the table's own count**, so an out-of-range command id
  fails closed with a null callback rather than reading past the table.
- **XIIOnline:** an in-progress command is engine state with a phase, not an instantaneous event.
  Replaying "the script called X" is not equivalent to replaying the command — the begin/poll/result
  progression has to be respected, or two clients will disagree about whether an action is still
  running.

## 7. What is not known

- [x] ~~Whether the twelve families sharing the default table is deliberate aliasing or a fallback for
      unimplemented families.~~ **AO-1 ANSWERED 2026-09-12 (FABLE): the shared table is family 2's,
      and the other eleven are verb-less fallbacks.** The authored verb catalogue ([the verb table](../Verb-Dispatch/scriptvm-verb-table.tsv),
      1,960 ids) names ids in exactly five families — **0** (1,496: `wait`, `setpos` … `hasJobAssigned`),
      **2** (212: `debug_bindp`, `mapload`, `mapdispose` … `debug_getscreenmode`), **3** (147, the
      `btlAtel*` spawn family), **5** (1, unnamed) and **7** (104, `fsmenu_*` / `fsroll_*`) — and its
      family-2 count is the 212 of the "default" table `0x01F26720`. So the `rep stosq` default in
      `VMNativeCommandDispatch_InitializeFamilyTables` is **family 2's table**, and families 1, 4, 6
      and 8–15 — for which no verb exists — merely inherit it: a fallback for families the catalogue
      never uses, not deliberate aliasing. Any authored id in those families would resolve as the
      family-2 command of the same index, but no verb is authored there to do so. **AO-1.**
- [x] ~~The 63-entry structure the executor indexes.~~ **ANSWERED 2026-09-02** — it is the VM's
      **return-value list**: count at `+0`, type tag at `+4+i` (1 = int, 2 = float), a constant `6`
      at `+0x44+i`, and two value words at `+0x84+i*4` and `+0x184+i*4`. Section 11. **AO-2.**
- [x] ~~What the phase byte enumerates.~~ **ANSWERED 2026-09-02, REFINED (section 12)** — the four
      values are right, but `2` and `3+` are **transient within one call**, not states the executor
      leaves behind. On entry the byte is only ever `0` or `1`. Original answer: `0` not started, `1` running,
      **`2` finished-returning-int**, **`3+` finished-returning-float**. The completion states carry
      the return type. Section 11. **AO-3.**
- [x] What families 3, 5 and 7 contain. **PARTLY ANSWERED 2026-09-02** — family **5**'s single
      command is an exact duplicate of family **7**'s command 0 (same `begin` `003567F0`, same `poll`
      `005114F0`), so it is not a distinct feature. Family **3** is **spawn**
      (`VM_Spawn_ApplySelectedUnit` at `0x3001`). Family 7's contents beyond its first four are
      unread. Section 10. **AO-4.**
      *ANSWERED 2026-09-27 (FABLE, Claude Opus 5.5), static: family 7 is the front end. Its 104 records are 55
      fullscreen-menu verbs, 6 stone/food-window and inert verbs, 31 staff-roll verbs (a typed line list built through
      one appender) and 12 title-screen verbs, and each group runs on its own native cluster. Family 3 is the battle-actor
      set, not only spawn. [The family record](../../_index/candidates/ao4-family-contents/README.md), control
      `ao4_families.py`, 6 checks.*
- [x] ~~Why a whole family (5) exists to hold a single duplicate entry.~~ **AO-6 closed 2026-09-12
      (FABLE): not in the image.** The catalogue lists `0x5000` with **no verb name** (one of its 19
      unnamed ids), so nothing authored refers to family 5 by name; its single entry is the same
      `begin` / `poll` pair as `0x7000` `fsmenu_wait`. The bytes carry only that family 5 exists and
      duplicates; the *why* is authoring history. **AO-6.**
- [x] ~~Why the command total (1,960) and the authored verb count (1,954) differ by six.~~ **AO-5.**
      ***ANSWERED 2026-09-18 (FABLE), by census: the six is a net figure, nineteen table entries the catalogue does not name against thirteen catalogue names the tables do not hold.** The authored catalogue is the ff12-script decompiler's command table (`CScriptContainerInitializers.cpp`, 1,954 entries, 1,954 distinct ids and names): 1,499 in family 0 (ids 0..1508), 211 in family 2 (0..210, the shared table's family), 140 in family 3 (0..146) and 104 in family 7 (0..103). Joined to the five tables read from `.data`: family 7 matches exactly (104 = 104); family 0's table holds 1,496 ids, of which ten have no catalogue name (1438, 1439, 1450, 1454, 1455, 1458, 1459, 1472, 1473, 1484), while the catalogue names thirteen ids the table does not hold (1496..1508, all placeholders `unkCall_5d8`..`unkCall_5e4`), which `003DC270` / `003DC240` / `003DC2A0` reject at the count check; family 3's table has seven unnamed ids (134..137, 141..143), family 5's single command (id 0) is unnamed, and the shared table's last id (211) is unnamed. Nineteen unnamed minus thirteen extra is six. Every unnamed table id is a live record, not padding: the ten in family 0 and the seven in family 3 are result-only commands (`0034C340`, `0034C7E0`, `0034C010`, `003526F0`, `00352B30`, `0050C7F0` twice, `0034DAF0`, `003513F0`, `00346620`; `0050F3C0` and `0050F3F0` twice each, `0050F500`, `0050F540`, `0050F5A0`), family 5's is a begin/poll pair (`003567F0`, `005114F0`), and shared 211 pairs the guard stub `0016D6A0` with `005C5230`. So the tables are the authority for this build and the catalogue is a separate listing that under-names nineteen commands and over-lists thirteen; the two counts were never meant to agree. DATA from the tables in the image and the catalogue source.*

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| `family = id >> 12`, `command = id & 0xFFF` | `sar r12d, 0xC` and `and r15d, 0xFFF` in `002621D0` | 1 |
| Sixteen family tables, four overridden | complete body of `003DC2D0`: `mov ecx, 0x10` + `rep stosq`, then four `mov [rip+…], rax` at family indices 0, 3, 5, 7 (machine-resolved) | 1 |
| Per-family command counts | first dword of each table read directly from `.data` | 1 |
| The three-callback record layout | complete bodies of `003DC270`, `003DC240`, `003DC2A0` | 1 |
| All three bounds-check the index | `cmp edx, dword ptr [rcx]` + `jge` in all three accessors | 1 |
| The executor branches on a phase byte at `+0x15` | `movzx esi, byte ptr [rdi+0x15]`, then `test esi, esi` and `cmp esi, 1` | 1 |
| A 63-bounded structure | `cmp eax, 0x3F` at four sites with writes at `[rbx+i+4]`, `[rbx+i+0x44]`, `[rbx+i*4+0x84]`, `[rbx+i*4+0x184]` | 1 |
| The `0x2000+` range is family 2 | `0x2000 >> 12 == 2`, and family 2 is one of the twelve on the default table | 1 |

**Scope honesty:** the *structure* is read exactly. The executor's phase machine is only sketched —
three branches are identified, their contents are not — and no individual command in families 3, 5
or 7 has been identified. *(Stale since: the phase machine is read in §11–§12, and families 3, 5 and 7 are AO-4,
answered 2026-09-27 — `_index/candidates/ao4-family-contents/`. Pointer 2026-09-30, SWE2-CONTRACT.)*

## 9. Related

- [`../scriptvm-native-dispatch-table.md`](../scriptvm-native-dispatch-table.md) — family 0's `result` column, and the 1,224 catalog rows mapped through it
- [`../../00-Engine-Core-Runtime/Force-Fight-Mode/force-fight-mode.md`](../../00-Engine-Core-Runtime/Force-Fight-Mode/force-fight-mode.md) — a runtime flag set by one of these commands
- [`../../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md`](../../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md) — modes 4 and 5 are set the same way

## 10. Falsification pass 2026-09-02 — reading the tables the structure predicts

**Attack chosen.** The document describes a record layout and then names none of the records. If the
layout is right, reading it should produce **coherent** commands; if it is wrong, it should produce
noise. The smallest and most falsifiable target is **AO-4** — family 5 has exactly one command, so
either it is something important or the reading is broken.

### AO-4: family 5 is a duplicate, not a feature

```
family 5, command 0 (id 0x5000):   begin  FUN_003567F0     poll  FUN_005114F0     result —
family 7, command 0 (id 0x7000):   begin  FUN_003567F0     poll  FUN_005114F0     result —
```

**Identical.** Family 5's entire table is a one-entry copy of family 7's first command. It is not a
special feature; it is a table that exists to hold one already-existing entry. Why a family was spent
on it is open, but "family 5 does something singular and important" is **refuted**.

### The layout produces coherent commands, which is the real test

Family 3's records are unmistakably **spawn**:

| id | begin | poll | result |
|---|---|---|---|
| `0x3000` | — | — | `FUN_00510440` — `btlAtelSetAbility`, tail `002390B0`: the foe's innate augment words into unit `+0xE80` (added 2026-09-10; [the auto-status rebuild](../../08-Combat-Formula/the-auto-status-rebuild.md)) |
| `0x3001` | **`VM_Spawn_ApplySelectedUnit`** | `FUN_005101B0` | *(no-op)* |
| `0x3002` | — | — | `FUN_005103B0` — `btlAtelSetStatus`, tail `002394C0`: 32 two-bit status codes into unit `+0xE90` and one-shot adds (added 2026-09-10; same page) |

A recovered name landing exactly on a `begin` slot, with a matching `poll`, is the strongest
available confirmation that the `+8 / +16 / +32` offsets are right — a wrong stride would scatter
names across columns rather than placing a `VM_Spawn_*` function precisely where a durative command's
entry point belongs.

### The two command shapes are visible in the data

- **Durative** — `begin` + `poll`, **no** `result`: `0x5000`, `0x7000`, `0x7002`, `0x7003`
- **Instantaneous** — `result` only: `0x7001`, `0x3000`, `0x3002`

This is the same split the [dispatch-table document](../scriptvm-native-dispatch-table.md) measured
as "1,155 of 1,496 records with exactly one non-null field" — now visible as a design distinction
rather than a statistic.

### Cross-confirmation: the `ret 0` no-op appears in a second table

Family 3's commands `0x3001` and `0x3003` carry **`_guard_check_icall`** as their `result` callback —
the bare `ret 0` at `0016D6A0`.

The [formula step table](../../08-Combat-Formula/Step-Table/combat-formula-step-table.md) records the
same address filling **42 of its 202 slots**, and reads it as identical-COMDAT folding (`/OPT:ICF`)
of every `ret`-only function, the disabled CFG stub among them. **Finding it used the same way in a
completely unrelated table, by a different subsystem, supports that reading** — it is a shared no-op
placeholder convention, not a quirk of one table.

*(That was an inference in the step-table document and remains one here: what is read is that the
body is a bare return and that two independent tables use it where "do nothing" is wanted.)*

### Not changed

The id encoding, the sixteen-family array, the per-family counts, the three accessors and their
bounds checks, and the executor's phase branch were all re-derived and hold.

## 11. Falsification pass 2026-09-02 (second) — AO-2 and AO-3, and a guess of mine was wrong

**Attack chosen.** Section 2 described the executor's `0x3F`-bounded structure as *"the shape of a
63-entry in-flight command table"* and left it at that. That sentence is a **guess dressed as a
description** — it names a purpose from a bound. Reading the rest of the executor settles both it and
the phase machine.

### CORRECTED: it is a return-value list, not an in-flight command table

The four parallel arrays are written together, once per completed command, and the count is
incremented:

```
+0x00          int    entry count            (inc dword ptr [rbx])
+0x04  + i     byte   type tag               1 = integer, 2 = float
+0x44  + i     byte   always 6
+0x84  + i*4   dword  value A
+0x184 + i*4   dword  value B                integer or float, per the tag
```

Index is bounded `< 0x3F`, so **63 usable entries** in arrays sized 64. The two writing paths differ
only in how the command's return value is read:

```c
/* phase == 2 */                          /* phase >= 3 */
ecx = *(int   *)&state[0x0C];             xmm0 = *(float *)&state[0x0C];
tag = 1;                                  tag  = 2;
```

**This is where a native command's return value lands** — a structure-of-arrays result list the VM
reads back, not a registry of running commands. My earlier description inferred "in-flight commands"
from nothing but the presence of a bound and some parallel arrays.

### AO-3 answered: the phase byte encodes progress *and* return type

```c
/* REFINED in section 12: the three arms FALL THROUGH into one another.
   0 -> begin, then poll, then (if not busy) result, all in this call.
   1 ->            poll, then (if not busy) result, in this call.
   >= 2 is not a state this executor can leave behind. */
phase = state[0x15];
if (phase == 0)  { state[0x0C] = 0; begin(...); poll(...); }   /* first call  */
else if (phase == 1) {                          poll(...); }   /* still running */
else             {               result(...);              }   /* finished    */

if (poll returned bit 0 set) { state[0x15] = 1; return 1; }    /* keep running */

/* on completion, the return value is appended to the result list: */
phase == 2  ->  tag 1, integer
phase >= 3  ->  tag 2, float
state[0x15] = 0;                                               /* reset */
```

So the byte is not a plain three-state progress counter:

| phase | meaning |
|---:|---|
| **0** | not started — run `begin`, then `poll` |
| **1** | running — `poll` only |
| **2** | finished, return an **integer** |
| **3+** | finished, return a **float** |

**The completion states carry the return type.** That is why the executor reads `state[0x0C]` twice
in different registers — the same four bytes are the command's return value, interpreted per phase.

`state[0x0C]` is zeroed before `begin`, and `state[0x15]` is reset to `0` at the end, so a command
slot is reusable.

### Why the original sentence was wrong, and the rule it breaks

"The shape of a 63-entry in-flight command table" reads like an observation but is an inference from
**a bound and an array count**. Nothing about `cmp eax, 0x3F` implies "commands in flight" — the same
shape fits a result list, an event queue, or a free list. This database has recorded three variants
of that error today already (constants that looked elemental, function names that looked party-side,
adjacent slots that looked like independent confirmation). **A structure's shape constrains what it
could be; only its writes say what it is.**

### Not changed

The id encoding, the sixteen families and their counts, the three-callback layout, the bounds checks
and the `begin`/`poll`/`result` semantics all stand.

### Status

With AO-2 and AO-3 answered, the lifecycle is read end to end: id decode → family table → callback
fetch → phase machine → result list. The document moves to `DOCUMENTED`; what remains open is the
*contents* of families 3, 5 and 7 and the default-table aliasing, not the mechanism. *(Both answered since: AO-1 and
AO-4, §7.)*

## 12. Refinement 2026-09-02 — the phase byte's completion states are transient, not persistent

**What this document said.** That the executor *"branches three ways — `0`, `1`, and `>= 2`"*, with a
phase table reading `2 = finished, return an integer`, `3+ = finished, return a float`. Written that
way, `2` and `3` read like states a command sits in between frames, and a reader would reasonably
conclude that a finished command waits in phase 2 or 3 until the executor is called again to collect
its result.

**What the complete body shows.** The three arms are not three separate visits. They fall through:

```c
phase = cmdState[0x15];
poll  = GetPollCallback(family, command);           /* fetched up front, always */

if (phase == 0) {                                   /* 2622AF */
    cmdState[0x0C] = 0;
    begin = GetBeginCallback(family, command);
    if (begin) begin(b, owner, cmdState + 0x18, valueStack, a);
}
                                                    /* 2622E1 - phases 0 AND 1 arrive here */
running = poll ? poll(b, owner, cmdState + 0x18) : 0;   /* no poll -> the zeroed local at [rsp+0x88] */
if (running & 1) { cmdState[0x15] = 1; return 1; }      /* 26230B - only exit that keeps state */

/* 262257 - reached by fall-through, not by a phase test */
result = GetResultCallback(family, command);
if (result) result(b, owner, cmdState + 0x18, valueStack);

switch (cmdState[0x15]) {                           /* the result callback just wrote this */
  case 2:            push_int  (valueStack, *(s32   *)&cmdState[0x0C]); break;   /* 262318 */
  case 3: default:   push_float(valueStack, *(float *)&cmdState[0x0C]); break;   /* 26233A */
  case 0: case 1:    push_int  (valueStack, 0);                         break;   /* 262289 */
}
cmdState[0x15] = 0;                                 /* 262382 - unconditional reset */
return 0;
```

**Three consequences.**

1. **A `result`-only command completes on its first call.** With no `poll` callback the "still
   running" flag comes from a local zeroed at entry (`mov dword ptr [rsp+0x88], 0` at `002621F7`), so
   the `test al, 1` fails and execution falls into `result`. This is why **1,573 of the 1,960 commands
   work at all** with a phase byte that starts at `0` — a fact the original three-way reading makes
   look impossible.
2. **Phases 2 and 3 live for a few instructions.** `VMResult_WriteInt32` writes `2` and
   `VMResult_WriteFloat32` writes `3`; the executor reads the byte at `0026227A`, immediately after
   the `call rax` at `00262278`, purely to choose whether to push an int or a float. Then `00262382`
   writes `0` back, unconditionally, on every path that reaches the result stage.
3. **On entry the byte is only ever `0` or `1`.** This executor writes `1` (still running) and `0`
   (finished or never started) and nothing else. Its `>= 2` entry arm is therefore unreachable from
   its own writes.

**What is NOT claimed.** That the `>= 2` arm is dead code. Some other writer of `cmdState[0x15]` could
set it — the byte is at a fixed offset in a record whose base is reachable as
`*(u8 **)(b + 0xA8) + (s8)b[0x11] * 40`, and that has not been swept. **BQ-5** holds that question
open. What is claimed is narrower and provable: *this function never leaves a value above 1 behind.*
*Status 2026-09-26 (FABLE, Claude Opus 5.5): that sweep is done and BQ-5 is answered — no writer
outside the executor's own call leaves 2 or 3 behind; the three result writers run only inside
lifecycle callbacks and no callback changes the current slot, so the `>= 2` arm is unreachable from
any writer in this image. Control: [members/bq5_phase_writers.py](members/bq5_phase_writers.py).*

**What was right and stays.** The four values' meanings, the id encoding, the sixteen families and
their counts, the three accessors and their bounds checks, the result-list layout, and the
`begin`/`poll`/`result` division of labour are all unchanged. The refinement is about the phase
byte's **lifetime**, not its **meaning** — but the lifetime is what a reader needs to predict when
each callback runs, and the original wording predicts it wrongly.

**Why the earlier reading was reachable.** `movzx esi, byte [rdi+0x15]` followed by `test esi, esi`
and `cmp esi, 1` is the classic shape of a three-state machine, and it is genuinely a three-way
branch — the mistake was reading the branch structure and stopping there, instead of following where
each arm *ends*. Two of the three arms have no terminator of their own; they run into the next stage.
**A branch that looks like a dispatch can still be a pipeline.**

## 13. The `begin` scratch slot, read from the bodies — 2026-09-07

`xiionline-61`, GN160 `fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708`.
Nine begin/poll bodies read in full, plus a whole-table census.

### What a player sees

When a zone script says *"walk over there, then talk"*, the native command can retain scratch
state while polling a condition. An authored count and a camera-state predicate use the same
lifecycle but different service conditions. Section11 proves selected count/poll behavior and
scaling predicates; it does not convert an authored wait count into an exact live duration.

### The scratch slot

The begin callbacks examined in this subsection use the VM value stack as their fourth argument
and retain selected state through their third argument. This is not a census proving every begin
ends in one integer write; the executor also supplies a fifth manager argument.

```c
void begin(ctx, actorState, int *slot, VMValueStack *vs)
```

**That `int *slot` is the command's private scratch word**, and the `poll` callback for the same
command receives it as *its* third argument. `begin` initializes it on phase0; `poll` uses it on eligible invocations. Invocation count is not automatically live frame count.

**`wait` (`0x0000`) is the clearest case.** Its begin (`0034CF90`) pops the authored frame count and
stores it; its poll (`0034DCC0`) is a countdown:

```c
*slot = *slot - 1;
if (*slot < 0) return 0;        /* 0 = finished, the script moves on   */
...
return 1;                       /* 1 = still running, poll me again    */
```

**So `wait 90` is literally a counter in a four-byte slot, decremented once per poll.** A modder
changing the argument changes that starting number and nothing else.

### The `*sync` verbs hardcode the slot, and that is why they take no arguments

`camerasync`, `effectsync` and `effectreadsync` **share one begin callback**, `0034C290`:

```c
VMValueStack_PushInt32(vs, 0);                        /* push a literal 0    */
iVar1 = VMValueStack_PopInt32CoerceFloat32(vs);       /* pop it straight back */
*slot = iVar1;                                        /* store 0             */
```

**It pushes a zero and immediately pops it.** The value never came from the script. `fadesync`'s
begin (`0033F4C0`) is the same three lines plus one call; `eventsync` and `eventreadsync` share
`00353E20`, which does the same push/pop and then

```c
v = 0 + 1;                       /* the popped value is always the pushed 0 */
if (v < 1) v = 1;
if (v > 3) v = 3;
*slot = v;                       /* therefore always 1 */
```

— a clamp to `[1,3]` that, given a self-supplied `0`, **always stores exactly 1**.

*Why the clamp is there (CE-6, answered 2026-09-13):* `00353E20` is the zero-operand copy of `00353A10`, the shared `begin` of the one-operand verbs `eventreadsync_ea` (`0x00EA`) and `eventsync_ee` (`0x00EE`): `00353A10` pops the script's operand `n` and stores `clamp(n + 1, 1, 3)` (`00353A1C`–`00353A3E`), and `00353E20` is the same instructions preceded by `VMValueStack_PushInt32(vs, 0)` (`00353E2A`–`00353E35`). So `eventsync()` / `eventreadsync()` are `eventsync_ee(0)` / `eventreadsync_ea(0)` with the operand fixed, and the clamp belongs to the operand-taking form. No other route supplies a stack: the only references to `00353E20` are the `begin` fields of records `0x00E9` and `0x00ED` (data qwords `01EEF428` / `01EEF4A8`) and it has no E8/E9 caller. Shipped `us` scripts pass only 0 or 1 to the operand forms (`eventsync_ee` 381 × 0, 172 × 1; `eventreadsync_ea` 251 × 0, 183 × 1), so slots 1 and 2 are used and the clamp to 3 is never reached by authored data.

> **These verbs are `wait`-shaped commands with the operand nailed down in the handler.**
> `camerasync` waits on camera channel **0**; `eventsync` waits on event slot **1**. The script
> cannot choose, which is precisely why the authored syntax takes no argument.

The poll then uses the slot as a **selector**, not a counter — `camerasync`'s poll (`0034C570`)
passes it straight into the camera query:

```c
mgr = FUN_002640c0();
if (FUN_003da1a0(*(u32 *)(mgr + 0x28), *slot) != 0)
        return FUN_00267310(actorState[0x15]) == 0;   /* still running? */
return false;                                          /* finished */
```

### An early-termination predicate, and its real extent

All three polls read above consult **`FUN_00267310(*(u8 *)(actorState + 0x15))`**, and in all three
a **non-zero** result ends the wait immediately:

| command | on non-zero |
|---|---|
| `wait` | `*slot = 0` — the countdown is forced to completion |
| `camerasync` | poll returns `false` — finished |
| `effectsync` | `FUN_0036ddc0(*slot)` — **cancels the effect**, then finished |

**The census refuses the general claim.** `00267310` has **65 callers**, of which only **19 of the
127 distinct family-0 poll callbacks (15.0 %)** are among them — plus 9 begin callbacks and 37
functions that are neither.

> **So this is not "every durative command checks for a skip."** It is a property of a **subset**,
> and the three commands read here happen to be in it. What the byte at `actorState + 0x15`
> *means* — the obvious guess is the cutscene-skip flag, since forcing every waiting command to
> complete is exactly what skipping looks like — **is not proven and is raised as `CE-5`.**
>
> **CE-5 correction — SECTION-11 (2026-09-23).** The previous answer conflated
> actor storage +15, ActorWaitSlot +15 and an indexed runtime-slot byte. `00267310(idx)` reads
> `02099011 + sign_extend(idx)*0x288`; the poll supplies a byte from the TARGET actor.
> The lifecycle phase lives in the ISSUER's separately selected request. These are not the
> same object or address merely because two displacements are +15.
>
> Original controls keep request phase1 while separately varying the indexed byte. With that
> byte0, wait counts down normally; byte1 forces its scratch to0 but that invocation still
> reports busy, and a later negative decrement completes. The reentrancy-guard explanation
> and universal "no skip input reaches it" exclusion are withdrawn. Actual producer meaning,
> scope of other polls and live reachability remain to be established; this is not a replacement
> unproved claim that the byte universally means cutscene skip.
>
> **Producer and scope answered 2026-09-29 (OV-15, FABLE; pointer 2026-09-30, SWE2-CONTRACT).** `02099011 + idx ×
> 0x288` is the actor-manager slot record's `+0x201`, the per-manager **skip mask**
> ([`ov15-skip-mask-fable`](../../_index/candidates/ov15-skip-mask-fable/README.md), `skip_mask.py`, FAILS 0; the
> world-tick page names the byte). A skip begin — script command 1337 `skipexec`, or the engine's loop over managers 1–3
> in `00360710` — sets bits; the skip end `00360A50` clears them; the bind writes 0. So a non-zero value means the
> target actor's manager is being skipped, and the wait ends by its second poll. `00267310` has 72 `rel32` call sites,
> most of them command handlers passing an actor's manager index; what each of the other 71 does with the mask is not
> claimed. Tier 1. **Which shipped scripts or engine paths actually start a skip in play is RC-17.**
> *(The register's CE-5 row still carries the withdrawn re-entrancy-guard reading as its answer; that row is not this
> lane's to edit, and the correction is routed in the batch record.)*

### For a modder

- **The `begin`/`poll` pair is the whole of a durative command.** `begin` stores one `int`; `poll`
  returns a low-bit running flag. The selected request also contains phase, saved target, result and accumulator; scratch is not all per-command state.
- **A `*sync` verb takes no argument because its handler supplies one.** To make `camerasync` wait
  on a different camera channel you change the constant in `0034C290`, not the script — and because
  that begin is **shared by three verbs**, you would change `effectsync` and `effectreadsync` too.
- **Shared callbacks are the norm, not the exception**: 230 poll slots are served by **127** distinct
  functions and 277 begin slots by **191**. Editing one handler edits every verb that points at it.

## 14. The all-null record, and the branch that completes it — 2026-09-07

**`CR-1` answered — and mostly by this document, which already had it.** The question, filed the same
day against [`../verbs-that-only-wait-and-verbs-that-do-nothing.md`](../verbs-that-only-wait-and-verbs-that-do-nothing.md),
asked what the interpreter does with the three family-0 records that have **no begin, no poll and no
result**: *"whether that is a silent no-op, a fault, or a path guarded upstream."*

**It is a silent no-op, guarded in the dispatcher itself, and §2 of this document already said so** —
*"where a callback is absent it takes an alternative path rather than failing"*, and *"the absent
`poll` yields 'not running' from a zeroed local"*. Re-derived from the instructions, the three guards
compose:

| slot | if null | evidence |
|---|---|---|
| `begin` | **skipped**; falls straight to the poll block | `002622BF test rax,rax` / `je 0x2622E1` |
| `poll` | substitutes the local zeroed at entry, so `& 1` is false and the command is "finished" | `002622E9 test rax,rax` / `je 0x2622FC`, against `002621F7 mov dword [rsp+0x88], 0` |
| `result` | takes the branch at **`00262360`** | `00262262 test rax,rax` / `je 0x262360` |

> **So a command whose record is entirely null runs begin → poll → result in a single call, does
> nothing, and returns 0.** It cannot hang: **the dispatcher's default for a missing poll is
> *finished*, not *busy*.**

### The one piece that was not already written down — `00262360`

A null `result` does **not** simply return. It pushes a default onto the same 63-entry result list
§11 describes:

```asm
00262360  movsxd rcx, [rbx]              ; current count
00262363  cmp    ecx, 0x3F
00262366  jge    0x262382                ; full -> skip the push, still complete
00262368  mov    byte [rcx+rbx+4],    1  ; tag
0026236D  mov    byte [rcx+rbx+0x44], 6  ; kind = 6
00262372  mov    dword [rbx+rcx*4+0x84],  esi   ; value  = 0
00262379  mov    dword [rbx+rcx*4+0x184], esi   ; value2 = 0
00262380  inc    dword [rbx]             ; push
00262382  mov    byte [rdi+0x15], 0      ; phase reset to 0 - finished
00262386  mov    eax, esi                ; return 0
```

**The script still gets a value.** A verb with no result callback yields tag `1`, kind `6`, value
`0`, so an expression consuming it has something to consume rather than reading a stale slot.

**And the 63-entry bound fails closed on the push while the completion fails open**: at 63 entries the
push is skipped by `jge 0x262382` and the command *still* resets its phase and returns finished.
**Losing a result is preferred to wedging a script.**

### What this means for the three empty verbs

`setnorecovertelepostatus` (`0x0330`), `battlemembersync` (`0x0356`) and `restartbattle` (`0x03B0`)
are **safe to call and safe to leave in a script.** They complete on the first invocation and push a
zero. That is the same observable outcome as the retail-stubbed verbs, reached by a different route:
**the stubs complete because their `poll` body returns 0; these complete because there is no `poll`
body and the dispatcher's default is 0.**

> **`CR-2` is not answered by this.** What `restartbattle` *did* remains unknown; this establishes
> only what calling it now does. *(CR-2 is closed as NO ADMISSIBLE SOURCE, reviewed and signed 2026-09-26: the verb has
> no implementation and no shipped script calls `0x03B0` in any of 10,045 `.ebp` files; what it once did is authoring
> history, which no admitted artefact carries. Pointer 2026-09-30, SWE2-CONTRACT.)*

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

- **RNG_Random_Selection — SERVICE.** The status-add tail `002394C0` draws the shared gameplay LCG before
  `BattleStats_AddStatusMode3`. **A script-added status is rolled on the loot stream**
  ([which roll](../../21-RNG-And-Determinism/which-roll-is-on-which-generator.md), §3 challenge).
- **Movement and Presentation — CLIENT.** The manager-slot byte reader `00267310` is also read by
  `Movement_UpdateSteeringTowardTarget`, a 935-byte movement body and a 511-byte Presentation body.
- **CombatAI — SERVICE.** The status-add tail `002394C0` calls `0031B760(rcx)` at `002394CE` to
  resolve the command record; the same resolver is reached by CombatAI callers `00239040`,
  `003014C0`, `00301AD0` and `003087E0` — one shared lookup, not a private path. (edge: `edges.tsv`)
- **CombatAction — SERVICE.** `0030E360` — the command executor reached through `0030EAE0` — calls
  CombatAction's two eligibility gates `0030B8E0` and `0030B9B0`, and is itself called by
  CombatAction bodies `002FDDA0` and `00304850` when the layer needs a command issued rather than
  gated. (edge: `edges.tsv`)
- **CombatFormula — SERVICE, with one dead edge.** `0030E360` calls `0031B860`, the
  record-to-unit resolver, twice per operation (source at `0030E39A`, target at `0030E3A7`), and
  the transition builders `00386A50`/`00386A70`. The sixth edge, `0030E360 callee 003112F0`, is
  **dead**: EXP-086 executed `0030E360` over 67 cases with zero calls to `003112F0`, and the binary
  shows why — `003848E0` sets result `+0x2C` bit 0 at `0038498D` but both transition builders clear
  it (`and dword [rbx+0x2C], 0xFFFFFFFE` at `00386A66`; `and dword [rdi+0x2C], 0xFFFFFFFE` at
  `00386AC3`), so every path to the applier shuts the gate before it is tested. `003112F0` is
  struck from `CONTRACT-status-write.md`'s callee list for the same reason. (edge: `edges.tsv`
  reports it; the body and EXP-086 disprove it)
- **ActorEntity — SERVICE.** The lifecycle is driven *through* the actor layer: ActorEntity's
  `ActorManager_RunFieldRuntimePass` (`0025D9E0`) calls the per-actor pass
  `0025DF00` (`WorldActor_UpdateRuntimeAndScriptExecutionState`, 1,228 B) once per actor, and
  `0025DF00` plus the interpreter `0025E4C0` consume the actor-resource entry family —
  `ActorResource_GetEntryByOrdinal`/`IsChannelBitActive`/`SelectPendingEntryForExecution`/
  `StartEntryScriptExecution`/`FindActiveEntryByIdOrClass`/`FindScriptRequestEntry`/
  `RemoveActiveEntry`/`RecycleEntryRange` (`003DB550`, `003DB640`, `003DB6E0`, `003DBDC0`,
  `003DBF60`, `003DC050`, `003DB2A0`, `003DB420`) and `00359B80`, `00268EA0`, `003587C0` — to
  locate and bind the actor's script-request entry before an opcode runs. `002621D0`'s rebind
  is the same `ActorManager_GetRecordByOrdinal` `00358940` bound in the subtree section below,
  and the `btlAtelSetAbility` tail `002390B0` resolves its unit through `0031B760`
  (`ActorWork_GetBattleUnit`). The actor layer supplies the records the lifecycle works on;
  nothing flows the other way. (edges: `edges.tsv`; roles per the pass-22 ledger)
- **Audio — SERVICE.** The manager-skip scan `00360710` calls Audio's `002DEDD0`, an 11-byte count thunk, as part of
  stopping the audio side when a skip begins ([the world tick page](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md),
  "What a skip is"). The command lifecycle itself has no audio relationship. (edge: `edges.tsv`)
- **CoreRuntimeScheduling — SERVICE.** `0025DF00` calls the scheduling primitives `001EDDA0`
  and `001EDE80` and the runtime-pointer resolver `0020E600`; `0025E4C0` calls `0020E600` and
  its encoder `0020E620`; the family-0 result-only body `0034C010` calls `00229E50`. These are
  the frame's scheduling and pointer utilities the driver, the interpreter and a leaf verb
  share with the rest of the image — utilities consumed, not lifecycle relationships.
  (edges: `edges.tsv`)
- **Party — CLIENT (1 edge).** The Party body `0030BEB0` (63 B) calls `0031B760`, the `ActorWork_GetBattleUnit` resolver this page already names - the shared resolver's caller population, not a second Party relationship. (edge: `edges.tsv`)
- **Rewards_Progression_Economy — SERVICE (1 edge).** `0030E360` (`BattleStats_ChangeStatusAndProcessSideEffects`, 1,323 B) calls `BattleUnit_ProcessDefeatRewardsAndLoot` (`00312280`, 857 B) - a status change reaching the defeat path drops into the loot/rewards processor. (edge: `edges.tsv`)
- **Input — CLIENT (4 edges).** 4 inbound (Input bodies `002E09A0`, `00226BE0` call page-cited `00263FF0`, `00267310`, `ActorManager_GetRecordByOrdinal` (00358940)). Substantive edges include `00267310` is called by `002E09A0`; the remaining edges run through shared helpers the page cites.
## The `002621D0` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`VMNativeCommand_ExecuteLifecycle` (`002621D0`, 119 B exclusive body) splits
the incoming id into `family = id >> 0xC` (`r12d`, `sar` at `00262205`) and
`command = id & 0xFFF` (`r15d`, `0026220C`), then resolves the family table
through `003DC240(r12d, r15d)` (`00262220`) — with the phase byte
`byte[rdi+0x15]` in `esi` (`00262213`). When the record's `word[r14]` no
longer matches `dword[rdi+8]` (`00262230`–`00262234`), `00358940(rbp)` rebinds
the live object (`0026223B`) before dispatch.

| member | role | interior |
| --- | --- | --- |
| `003DC240` (39 B) | `GetPollCallback` — bounds-checks `family` against `dword[02B57EF0]` (`003DC253`), returns `tbl[family]`'s record `+16 + 32*command` field (`shl rax, 5` at `003DC25A`) | [`003DC243`](../../_index/ADDRESS-INDEX.md) |
| `003DC2A0` (41 B) | `GetResultCallback` — same `02B57EF0` bound + `shl rax, 5` (`003DC2B3`/`003DC2BD`), returns the `+32` callback field with `lea 01F26720` (`003DC2D5`) | [`003DC2A3`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00263FF0` and `00358940` — the rebind
wrapper called at `0026223B` (`00358940(rbp)`; compares `edx` to `dword[r8]`
at `0035894D`, calls `00263FF0` at `00358969`) is `ActorManager_GetRecordByOrdinal`'s
family with a wide caller fan-out, so it is not exclusive to this subtree. The third
sibling getter `003DC270` (`GetBeginCallback`, record `+0`) is shared, not exclusive.

## The `002394C0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`002394C0` (~210 B) — `0031B760(rcx)` resolves the record, null → return
(`002394CE`/`002394D9`); the body issues the command through the member.

| member | role | interior |
| --- | --- | --- |
| `0030EAE0` | arg-forward wrapper — repacks two stack args and `0030E360` (`0030EAE8`/`0030EAFC`) | [`0030EAFC`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0031B760`, `0030E360`.

## Cross-subsystem neighbours — pass-22 residue (SWE2-CONTRACT, 2026-10-02)

- **UI — SERVICE (1 edge).** 1 outbound (`00228C70`, cited in the RC-17 box — the pause-menu
  skip-confirm path `00228C70` → `00285EA0` — calls the 174-byte UI body `0029DBE0`); the
  skip path's own cross-layer call.
