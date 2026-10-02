# RC-5 residue: does `main` of the six counter actors start more than once per image load? (FABLE, 2026-10-02)

Static: the shipping image and the shipped bytecode. This record edits no page and no register row.

## The question

FABLE's record [`rc5-counter-loops-fable-1002`](../rc5-counter-loops-fable-1002/README.md) found six increment-only
`startscene` counters (54 variables over the nine language copies). None of them has a reset. Their bound holds only if
each actor's `main` starts once per image load. That record's "Not claimed (limits)" calls this the one open
premise. The six are:

| file | actor | variable | increments in `main` (per copy) |
|---|---|---|---:|
| `enw_a0580` | `読込監督` | class-1 `+0xe98` | 13 |
| `mnt_c0100` | `監督` | class-1 `+0x13` | 8 |
| `rwf_d0100` | `監督` | class-1 `+0x13` | 5 |
| `rwf_d0101` | `監督` | class-1 `+0x13` | 3 |
| `rwg_a0181` | `監督` | class-1 `+0x20` | 1 |
| `str_z0000` | `監督` | class-1 `+0x2a` | 1 |

The question has two halves:
- **(a) the engine.** SWE2-ORACLE's [RC-12 / RC-13 record](../rc12-footer-channels-runstate-0930/README.md) says the
  engine files footer slot 1 (`main`) on channel 0 "at record start". Which paths reach that filing? Can a respawn,
  re-initialisation or `reqenable` repeat reach it? Does any other native site file slot 1? When record start repeats,
  are the class-1 variables fresh?
- **(b) the bytecode.** Can any shipped script request `main` of these actors, or of any actor?

## Answer

**The bound holds for all six: `main` of each actor is filed once per load of its script image, and every load
starts the counter from its declared value.**

- **The engine files `main` in one place, once per bind.** That place is the record initialiser.
  - Record start is entered only from the manager initialiser.
  - The manager initialiser works only on a manager slot that the binder armed. It disarms the slot at once.
  - The binder is reached only from the load completion of a newly allocated payload buffer, filled from the file or
    from a resident copy.
  - Each record start therefore comes with a fresh copy of the class-1 area.
- **The repeat routes file other slots.** These are the respawn, `reqenable` and unit-refresh routes. No other native
  site files slot 1.
- **No shipped script asks for `main`.** The census covers 673,688 filing operations in all language copies, each
  resolved to a function name through the image's own name pool. None names `main`, for these actors or for any
  other.
- **No image table names `main` in another slot.** The footer, the spawn table and the setup spawn-order list put no
  `main` into a slot the engine files.
- **Only `main` reaches the increments.** In each of the six actors, no other function's entry reaches an increment.

For `str_z0000` this settles re-entry only. Its increment lies on a loop inside one pass of `main` (the earlier
record's "(a) The one loop"), so its upper end still fails, as published there.

## Method

Two scripts, each with its output in this folder:

| script | output | what it covers | time |
|---|---|---|---|
| [`rc5m_engine.py`](rc5m_engine.py) | [`rc5m_engine.out`](rc5m_engine.out) | part (a), from the image | about 2 minutes |
| [`rc5m_requests.py`](rc5m_requests.py) | [`rc5m_requests.out`](rc5m_requests.out) and [`rc5m_requests.tsv`](rc5m_requests.tsv) | parts (b) to (d), from the VBF | about 1 minute |

Each exits 0 only when all its checks pass. Both report `FAILS 0`.

`rc5m_engine.py` uses ORACLE's shared helpers from the RC-12 folder:
- `img.py`, for `.pdata` extents and the raw rel32 index;
- `rc12_slots.partC`;
- `rc14_sweep.streams`: every `.pdata` chain root, plus a linear sweep of the `.text` that no `.pdata` entry
  covers.

Its raw reference index takes every kind of reference:
- `E8`/`E9` rel32;
- `0F 8x` rel32 and `EB`/`7x` rel8 jumps;
- rip-relative `lea`;
- 8-byte absolute and 4-byte RVA words in every section but `.text` and `.pdata`. An RVA word is classed as an unwind
  chain copy when the 12 bytes there equal a `.pdata` entry.

`rc5m_requests.py` walks every `.ebp` in the shipped VBF (10,036 images). It uses the kit decoder
[`gen_req_channel_census.py`](../../../25-EBP-Script-Container/Bytecode-And-Opcodes/members/gen_req_channel_census.py)
and its backward stack resolver, as ORACLE's
[`rc5b_operands.py`](../rc5b-event-slot-residue-0930/rc5b_operands.py) does. It reuses ORACLE's `const_of`.

**Operand order is read from the handlers.**
- **`REQ` family** (`0x21`–`0x29`). The submit `00268850` pops the function id first (`00268870`), then the target
  (`002688B0`), then the channel (`002688D8`). So the pushes are channel, target, function id, the decoder's
  `args[0..2]`.
- **`REQCHG`** (`0x34`). The interpreter pops function id, target and slot at `002615BD`–`002615D9`, then calls
  `0025AF60`. That function writes override slot `edx` (at most 17). This confirms RC-12/13's correction: the first
  operand is a footer slot, not a channel.
- **The kit decoder's arity for `REQCHG` is wrong.** Its `NARGS` table gives `0x34` seven arguments; this census
  uses the handler's three.
- **`REQALL` / `REQIALL`.** The operand indexes the payload's list table (header `+0x30`), per
  [section-000](../../../25-EBP-Script-Container/Bytecode-And-Opcodes/section-000-bytecode.md) §"`REQALL`, `REQIALL`,
  `REQWAITALL`". Every `{ordinal, functionId}` pair is a request.
- **The verbs `sysreq` (`0x0AA`), `sysreqall` (`0x0AB`) and `sysreqf` (`0x228`).** They pop a footer slot first, so
  the slot is the last value pushed.

**Resolution follows RC-12 Part B.**
- target ordinal → directory entry (section `+0x18`, 48-byte entries);
- function id → that entry's function table (`+0x10`);
- name offset → the image's name pool (header `+0x4C`).

A request "targets `main`" when that name is `main`. Independently, it also counts when the function id equals the
target's footer word k = 1. A target produced by verb `0x072 getmyid` is the issuer itself.

## Controls

All pass.

| id | what | result |
|---|---|---|
| E0 | RC-12 Part C reproduces | 43 actor-entry footer resolves in 19 functions |
| R1 | RC-12 Part B reproduces (us copy) | 1,114 images, 26,390 actors, footer k = 1 names `main` 6,765 times |
| R2 | RC-13's `REQCHG` census reproduces (us copy), with the three-pop reading | 1,884 calls: slot 2: 1,804; 3: 14; 4: 8; 5: 8; 16: 24; 17: 26 |
| R3 | the raw resolver agrees with the decompiler | constant `REQ`/`REQSW`/`REQEW`/`REQCHG` pairs in 847 us files: 38,000 raw, 38,002 decompiled, 37,928 agree (99.81%) |
| R4 | positive: the census finds commonly requested named functions | `talk*` through `REQCHG` 16,047; `logic_main` 3,555; `repos_main` 2,232; other names containing "main" 5,976 (all copies) |
| R5 | positive: the detector fires on a constructed case | `PUSHII 1; PUSHII 0; PUSHII 1; REQ` in `str_z0000` resolves to director 0, function 1, `main` (by name and by footer) |
| D2 | the spawn-table walk is aligned | the commonest items of lists 0, 1, 2 and 4 are `entry00`, `spawn00`, `btalk00` and `respawn00` |
| C-entry | the entry test is complete | all 54 actor copies are found, with every increment of the earlier record at an instruction boundary |

The decompiled us corpus agrees independently: no `sysReq*` call and no `reqa` list there names `X::main`.

## Result (a): the engine files `main` once per bind

**1. The filing site.** `002669F5` lies in `00266530`, `ActorStorage_InitializeRecord` (E1).
- It reads the record's override slot 1 (`+0xCA`) first, at `002669AE`.
- Otherwise it reads footer word `+4` (k = 1) at `002669D7`.
- It files that function on channel 0: `xor edx, edx` at `002669F0`, then `003DBB60`.

**2. Who reaches it** (E2, full raw index; unwind chain copies excluded):
- `00266530` has one reference: `002679F0` at `00267B79`. That is a loop over record indices, once per index
  (`00267B70`–`00267B82`).
- `002679F0` has one reference: `0026CE60`, the manager initialiser, at `0026CEB0`.
- `0026CE60` has two references:
  - the world tick's manager-request drain `0025BFB0`, at `0025BFF6`;
  - `0032F1B0`, at `0032F227`, which 17 pack-section handlers call.

  No jump, `lea` or data word reaches any of the three otherwise.

**3. The gate** (E3).
- `0026CE60` leaves at once when manager `+0x10` bit 0 is set (`0026CE94`). That bit means "initialised".
- It also leaves when the arm byte `+0x13` is zero (`0026CE9E`).
- Otherwise it builds the record pool, so record start fires.
- It then sets the arm byte back to 0 (`0026D2E3`) and sets bit 0 (`0026D305`).

So **each arming yields one record start, whichever caller arrives first.**

**4. Only the binder arms** (E4, E5).
- `ActorManager_BindLoadedDefinitionPayload` `0026C8C0` arms the slot:
  - it clears bit 0 (`0026CB1B`, stored at `0026CB67` / `0026CC45`);
  - it stores `+0x13` = 1 (`0026CC6C`).
- The image-wide sweep found exactly three writes of a manager slot's `+0x13`, over 42,487 streams:
  - the binder's arm;
  - the initialiser's disarm;
  - the unload `002628B0`'s clear (`00262DB3`, beside its bit-0 clear at `00262DA8`).
- The other non-stack hits were checked by hand, and none is a slot. The bases are listed in the output: an 8-byte
  stride table, a foreign 0x860-stride array, a 0x1C-stride table, and argument outputs of two vector routines.
- Five folded slot bases exist:
  - three read-only getters (`0026419A`, `002671FA`, `002673FA`);
  - a bit test (`00262FBD`);
  - the area initialiser's per-slot zeroing (`00266EE0`).

**5. Every bind takes a freshly filled buffer** (E6).
- The binder has one caller: `0032F850`, which binds the payload it is handed (`0032F961`).
- `0032F850` is reached two ways:
  - from `003304A0`;
  - as the completion of a read that `003306E0` files into a buffer it has just allocated (`00330FA6`).
- `003304A0` is reached only from `00330310`. That function allocates a new buffer (`003303AD`), then either:
  - copies the resident image into it (`00330407`, the pack-212 case), then dispatches;
  - or files a read whose completion is `003304A0` (`0033041B`, `00330444`).
- The resident copy `022C6F10` is written only by its loader `0032F430`, which allocates it and fills it by a read.
  No script binds it directly.

**6. Class-1 variables restart with the bind** (E9).
- The binder stores the new payload as manager `+0x00` (`0026C95A`).
- It zeroes the class-1 base `+0x40` (`0026CAF4`).
- The armed initialiser then points `+0x40` at payload + header `+0x38` (`0026D2F0`–`0026D2F6`), inside the fresh
  buffer.

This matches [the storage-classes page](../../../01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md)
§2.3 (class 1 is "a data area inside the loaded script image"). It adds who refills it: every record start's
`main` sees the declared values.

**7. The repeat routes do not file slot 1** (E7, E8).
- **The route functions file other slots.** `0026B4A0` (`reqenable` tail), `00267CC0`, `00269FE0`, the unit refresh
  `00238BF0`, `00268EA0`, `00269860`, `00269640`, `0025AD10` and `0025AE00` file the `talkhold`/`talkterm`, spawn,
  respawn, entry, parameter and talk-list slots.
- **Following calls does not separate them.** Through tail jumps and jcc forwarders, seven of these routes reach
  `0026CE60` in 30 to 32 hops through the world machinery and a loader, always by way of `0032F1B0`. What separates
  them is the gate of point 3, not reachability.
- **Footer word k = 1 has one fixed reader.** In RC-12 Part C it is `002669C5`, in the record initialiser.
- **The two variable-slot readers never take slot 1 from the engine:**
  - `00269860` takes slot 14 or 7 (`00269932`, `0026993F`, `0026994D`).
  - `002652D0` has five references, with these slot arguments:
    - `002E2E68`: 2;
    - `00268D94`: the cell `0209A2BC`. Its writers store 2 (`0025AB06`, `0025D67B`, `00267102`), or at `0025BDE6`
      the value 10 or 2 that `0025BAD0` receives (`0025B8C7`, `0025B9BB`, `0025B9D0`);
    - the leaf `00265380`: slot 0 from `entrysync` (`0034B37F`), and from `sysreqwait`'s begin `0034C630`, which
      stores the function id and files nothing;
    - `00269B48` and `00269BE3`: the slot that `sysreqall` / `sysreq` / `sysreqf` pop. That is part (b).

## Result (b): no shipped request names `main`

There are 673,688 filing operations over all copies:
- single requests: `REQ` 196,868, of which 234 are self requests through `getmyid`; `REQSW` 27,686; `REQEW` 101,380;
  `REQCHG` 16,956;
- list pairs, counted per site: `REQALL` 312,870 and `REQIALL` 17,253;
- 675 `sysreq` calls.

**None targets `main`,** by name or by footer word.
- `sysreq` passes slots 2, 7, 11 and 14 only.
- `sysreqall` and `sysreqf` have no shipped site.
- `REQWAITALL` (53,310 pairs) files nothing.

**270 single requests do not resolve.** In each one the target is computed, and in 18 the function id is too.
- **None is in the six files.** Every request issued inside those files resolves, and none names their counter
  actor.
- **Three distinct sites have a constant function id that is `main` for some actor of their own file.** They have
  nine copies each:
  - `fon_b01` `+A320`. Target 27 plus a variable; actor 79 has `main` at that id.
  - `glf_a02` `+6C70`. Target 13 plus a variable; no actor at ordinal 13 or above has `main` there.
  - `rbn_b01` `+17F78`. Target 16 plus a variable; actors 47 to 49 have `main` there.

  These variables were not bounded. "Any actor's `main` anywhere" is therefore **0 resolved, plus at most these three
  computed sites**.
- **No target reaches another manager.** No constant target anywhere sets the other-manager bit 14. The computed
  targets are ordinal arithmetic or `PUSHACT` forms.

## Result (c) and (d): only `main` reaches the increments, and no image table names `main`

**(c) Only `main`'s entry reaches the increments.** Each of the six actors has two functions, `init` (index 0) and
`main` (index 1). In the whole-actor control-flow graph (the earlier record's CFG, copied), `init`'s entry reaches no
increment, in all 54 copies. So a filing of any other function cannot advance the counter. Record start's
function-0 filing (`00266957`) files `init` (D1).

**(d) No image table puts `main` into another slot:**
- No footer word other than k = 1 names `main`, anywhere.
- No spawn-table item names `main`, anywhere. These are the lists `00263D40` reads: entry, spawn, talk, touch and
  respawn. The spawn-verb writers `0025AD10` / `0025AE00` store them into override slots 0, 7, 10 and 14.
- No setup spawn-order id (header `+0x50` / `+0x58`, filed by `00266C50` once per arm) names `main`. That is 5,591
  lists with 44,728 ids.
- The six directors' spawn tables are empty. Their footer sets only k = 1.

## Per variable

| file | variable | engine filings of `main` per load | script requests of `main` | other image slots naming `main` | bound |
|---|---|---:|---:|---:|---|
| `enw_a0580` | class-1 `+0xe98` | 1 | 0 | 0 | **holds** |
| `mnt_c0100` | class-1 `+0x13` | 1 | 0 | 0 | **holds** |
| `rwf_d0100` | class-1 `+0x13` | 1 | 0 | 0 | **holds** |
| `rwf_d0101` | class-1 `+0x13` | 1 | 0 | 0 | **holds** |
| `rwg_a0181` | class-1 `+0x20` | 1 | 0 | 0 | **holds** |
| `str_z0000` | class-1 `+0x2a` | 1 | 0 | 0 | re-entry **holds**; the upper end still **fails** through its own in-`main` loop |

So for the five non-looping variables, ORACLE's interval (declared value up to the declared value plus the file's
increments) is now unconditional on re-entry. It is still subject to the limits below.

## Not claimed (limits)

- **Static only.** How often a field loads is the player's choice. The claim is per bind.
- **Bulk writes.** The `+0x13` census is a displacement and folded-base sweep. A bulk copy onto a live manager slot
  (`memcpy`, other than the area initialiser's zeroing) would not be seen.
- **By-shape verdicts.** The `003A4290` / `003A56F0` argument stores were judged by shape, not by tracing each
  caller's pointer.
- **Computed targets.** The three computed-target sites above were not bounded. Nor were cross-manager requests
  whose target is computed with bit 14 when the request is issued.
- **Concurrency.** Two records for one directory entry, and a second bind of the same manager while the first payload's
  actors are still active, are not modelled. A rebind rebuilds the pool from a fresh buffer.
- **Retail reachability.** Not claimed for any of the six events.
- **Decoder scope.** The bytecode census uses the kit decoder's linear decode of cut actor bodies. Its R3 agreement
  with the decompiler is 99.81%, not 100%.

## Side findings (for the owners, not edited here)

- **F1. The kit decoder's `REQCHG` arity is wrong.** `gen_req_channel_census.py`'s `NARGS` gives `0x34` seven
  arguments; the handler pops three (`002615BD`–`002615D9`). Any census that used that table for `REQCHG` operands
  misattributes them. RC-13 used the decompiled text and is unaffected; R2 reproduces it with the three-pop reading.
- **F2. Engine filings by slot skip function id 0.** `sysreq`'s filer `00269BA0` and `sysreqall`'s `00269AD0` both
  skip a slot whose function id is 0 (`test ax, ax` after the getter). They also need bit `slot` of record `+0x1C`, the
  mask that `reqenable` sets (`0026B4AC`).

## Routing (not edited here)

- **FABLE's own record.** [`rc5-counter-loops-fable-1002`](../rc5-counter-loops-fable-1002/README.md), "Not claimed
  (limits): Re-entry", is answered by this record for the six increment-only variables. The two constant+increment
  variables of its (b) table, whose re-entry premise also involves `開始c58`, are not covered.
- **Register row RC-5.** Its owner, SWE2-CONTRACT, can cite this record for the re-entry premise.
- **The kit decoder's owner** gets F1.
- **Review.** FABLE authored this record; it goes to SWE2-AUDIT-SEM for a non-author verdict.

run: rc5m_engine.py at 31f29775a, rc5m_requests.py at 31f29775a

## Consumer check (FABLE)

affected: `Database/FFXII TZA/_index/OPEN-QUESTIONS.md`

- consumer: register row RC-5, FABLE's 2026-10-02 narrowing: revised-here (the "only if `main` runs once per load" premise struck and restated as settled; the row stays OPEN on ORACLE's array re-run and the review).
- consumer: [`rc5-counter-loops-fable-1002`](../rc5-counter-loops-fable-1002/README.md): agrees (its limit is the premise answered here; not edited).
- consumer: the kit decoder `gen_req_channel_census.py` (REQCHG argument count 7 vs the handler's 3): routed-to-SWE2-DATA.
- consumer: SWE2-AUDIT-SEM's pending review of the loops record: routed-to-SWE2-AUDIT-SEM as a second item of the same review.
