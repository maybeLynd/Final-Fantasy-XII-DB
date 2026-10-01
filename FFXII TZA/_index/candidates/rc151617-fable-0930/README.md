# Static answers for SWE2-CONTRACT's RC-15, RC-16 and RC-17 (FABLE, Claude Opus 5.5, 2026-09-30)

SWE2-CONTRACT registered these rows on 2026-09-30 and holds their pages. FABLE did the research
(`FABLE-RC-15-16-17-STATIC-0930`, target keys only) and routes the answers for incorporation. This builds on FABLE's T5
(`../fable-astra-live-facts-0930/t5_regfile_reuse.md`), which found that no native store reaches ActorStorageRecord
`+0x64..+0x83` between a record's release and its reuse. The only native clear is the pool-allocation memset `00267A8B`.

## RC-16: can a new occupant read a register before its own first write? Answered: yes, in shipped scripts, with visible effect

[`rc16_regfile_reads.py`](rc16_regfile_reads.py) ([output](rc16_regfile_reads.out)) reads every actor script's bytecode
in the 7,565 distinct shipped `.ebp` files (198,302 scripts). Control: its register-opcode totals equal the full opcode
histogram's, which is in `../fable-astra-live-facts-0930/ov16_opcode_histogram.out`.
- **I0, I2, I3:** every script that reads them also writes them.
- **I1:** always written somewhere, but ~~in the decompiled US corpus **67 actors touch `regI1` first with a read**. 66 of
  them are monster scripts' `init()`, which on a fresh spawn (`btlAtelGetRespawnCause() == -1`) runs:~~
  *(corrected 2026-09-30, FABLE, on SWE2-AUDIT-SEM's auditsem-review-rc151617-0930 §5 N1:)* `rc16_regfile_reads.py` finds 434 bytecode scripts whose first linear `regI1` touch is a read. In the decompiled US corpus the dominant case is the monster spawn-group functions, `fn_spawn spawnNN()` and `fn_respawn respawnNN()` (516 instances), which on a fresh spawn (`btlAtelGetRespawnCause() == -1`) run:

  ```
  regI0 = 1;
  while ((regI1 != -1 && regI0 < 64)) {
      regI1 = btlAtelGetDeadCountMax(regI0);
      if (regI1 != -1) { file_var_s26_1 += regI1; file_var_s26_2 += btlAtelGetDeadCountNow(regI0); }
      regI0 = regI0 + 1;
  }
  ```

  The loop tests `regI1` before this path writes it. The value it sees depends on where the record came from:
  - **freshly allocated pool:** `regI1` is 0, so the loop runs and sums the dead counts;
  - **reused record:** if ~~the previous occupant~~ *(corrected 2026-09-30, FABLE, on OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930 and ORACLE's [rc15-regfile-skipmask-0930](../rc15-regfile-skipmask-0930/README.md):)* an earlier spawn or respawn function of the same authored actor, on the same record, left `regI1 = -1` (within one pool a record is initialised once, for one authored actor: `00266530` has one caller, `00267B79` in the pool allocator `002679F0`, whose one caller is `0026CEB0` in `0026CE60`; the pool memset is `00267A8B`), which is exactly how this loop exits, the loop does not
    run at all and the sums are not accumulated.

  ~~The 67th is `ＳＥＴＴＵＲＮxyz()`.~~ *(corrected 2026-09-30, FABLE, on SWE2-AUDIT-SEM's auditsem-review-rc151617-0930 §5 N1:)* no committed output counts this case, so it is dropped. On OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930: the 516 loops are in 12 scripts, in `spawn00`..`spawn09` and `respawn00`..`respawn09` (ORACLE's `rc16_check.py` D1, re-run by FABLE).
- **F0..F3:** one shipped script reads them and never writes them. It is `rbn_a03` (nine language copies of one script),
  actor **`SND_WOMAN_A`**, function `エントリキャラ乗っ取り解除` ("entry-character takeover release"), which does
  `setpos(regF0, regF1, regF2); dir(regF3)`. Its neighbour `TWN_BANGA_A` has the matching save (`regF0..F3 = getx() ..
  getrotangzx()` in `エントリキャラ乗っ取り２`); `SND_WOMAN_A` has only the release. ~~It restores a position its own code
  never stored: zeros in a fresh pool, or the previous occupant's saved position in a reused record.~~
  *(corrected 2026-09-30, FABLE, on OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930 and ORACLE's [rc15-regfile-skipmask-0930](../rc15-regfile-skipmask-0930/README.md):)* This read is not shown to run: no script in the corpus requests `エントリキャラ乗っ取り解除` or `エントリキャラ乗っ取り２` by name, and `rbn_a03`'s three computed-target requests are unresolved (ORACLE's D2, re-run by FABLE).

**So the register file does persist across occupants, and shipped scripts read it before their own first write in
ways the player can see.** The monster dead-count sums ~~and one actor's restored position~~ *(corrected 2026-09-30, FABLE, on OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930:)* (the `SND_WOMAN_A` read is not shown to run) differ between a fresh and a
reused record. A reconstruction that zeroes the register file on spawn diverges from the original; one that never clears
it matches. ~~The run-time fact left is **which case a given spawn is**, same pool or new pool. That is the identity
question of `FABLE-REQ-ASTRA-REGFILE-REUSE`, which this narrows to that one fact.~~ *(corrected 2026-09-30, FABLE, on OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930 and ORACLE's [rc15-regfile-skipmask-0930](../rc15-regfile-skipmask-0930/README.md):)* A different authored actor never inherits a record's registers inside one pool, and across pools the memset zeroes the file. The fact left is which record a spawn entry's `spawnNN` / `respawnNN` function runs on: the actor's own record, with several spawn entries sharing one register file, or a record of each spawned unit's own. It is static and was not traced, so RC-16 is NARROWED, as ORACLE rates it.

Limits:
- The I1 finding reads source order in the decompiled scripts, not the bytecode's execution order. ~~`init()` is the entry
  function, and the loop is its first `regI1` touch on the respawn-cause -1 path.~~ *(corrected 2026-09-30, FABLE, on SWE2-AUDIT-SEM's auditsem-review-rc151617-0930 §5 N1:)* the loop is the actor's first `regI1` touch on that path; `fn_entry` does not touch it.
- Registers carried across calls within one occupant are not at issue here.

## RC-17: is the actor-manager skip mask set in shipped play? Answered: yes, when the player skips an event cutscene

- **The shipped use** (decompiled US corpus): `skipexec(1)` appears 7 times in 7 event scripts (`alc_z0200`,
  `bhm_a0200`, `bhm_y0101`, `bhm_z0100`, `byu_y0100`, `ene_a0200`, `fon_b0100`), and `skipexec(0)` 12 times in 12 others.
  ~~All sit in the cutscene-skip idiom:~~ *(corrected 2026-09-30, FABLE, on OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930 and ORACLE's [rc15-regfile-skipmask-0930](../rc15-regfile-skipmask-0930/README.md):)* the sites share the shape `skipstart(n); if (<test>) { skipexec(n); }`, but the test varies. Of the seven `skipexec(1)` sites, `alc_z0200` tests `skipcheck(1)`, five test `skipcheck(0)`, and `bhm_y0101` tests `file_var_s0_2 == 1` alone. Some `skipexec(0)` sites test a file variable alone (`alc_z0100`: `if (file_var_s0_1 == 1) { skipexec(0); }`). `alc_z0200`'s form:

  ```
  skipstart(1);
  if ((skipcheck(1) || file_var_s0_1 == 1)) { skipexec(1); }
  ```

  ~~So the skip begins when the player skips the cutscene, or a file variable asks for it.~~ *(corrected 2026-09-30, FABLE, on OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930 and ORACLE's [rc15-regfile-skipmask-0930](../rc15-regfile-skipmask-0930/README.md):)* `skipexec` is the script-forced begin. The player's skip reaches the same begin through the pause menu and `00360880` (below), with or without `skipexec`.
- **The handler** `0034ECF0` pops the argument into `ecx` and passes `byte [rdx+0x15]` as `edx`, tail-calling `00360710`
  (`0034ECFC`-`0034ED0C`). A verb callback's `rdx` is the owner actor record (verb-dispatch page section 2.5). A record's
  `+0x15` is its **manager index**: `ActorStorage_InitializeRecord` copies it from the manager's `+0x28` (`00266616` /
  `00266624`; the manager arrives in `rcx`, `00266561`, from `ActorStorage_AllocateAndInitializeRecords` `00267B76`). The
  field census counts 18 reads and no other write.
- **The skip begin** `00360710(n = ecx, m = edx)` returns 0 at once when `m` is 0 (`00360728`-`0036073E`), so a manager-0
  caller is refused. Otherwise it addresses entry `022CB730 + (n + m*8)*16` (`00360744`-`00360755`). It proceeds only
  when `00267330(m)` returns 0 and the entry's `+0xC` is non-zero (`00360758`-`0036076B`). It then sets `+8` = 1 and
  `+2` = 2 and applies the bit shift of `byte [entry]` (`003607A9`-`003607C9`).
- **The engine route** `00360880` (called from `00228130` at `002281B7`) ~~runs `00360710(bit, m)` for `m` = 1 to 3 over
  each set bit of `022CB9C4` (`0036088A`-`003608B0`).~~ *(corrected 2026-09-30, FABLE, on OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930 and ORACLE's [rc15-regfile-skipmask-0930](../rc15-regfile-skipmask-0930/README.md):)* for `m` = 1 to 3 reads that manager's own registered word (`022CB9C4`, `022CB9C8`, `022CB9CC`, stepping 4 at `003608B7`) and calls `00360710(n, m)` once, for its lowest set bit `n` below 8 (`003608A0`-`003608B0`).

- **The registration** (`skipstart`, verb `0x51A`, handler `0034D3A0`, per `scriptvm-verb-table.tsv`) calls
  `00360980(n, m)`. It refuses `m == 0` (`00360980` `test edx, edx`) and registers the entry: `+0xC` = 1 and `+2` = 1
  (`003609E9` / `003609ED`). It also sets the entry's bit in the word at `022CB9C0 + m*4` (`003609F3`); for manager 1 that
  word is `022CB9C4`, the mask the engine loop `00360880` walks. ~~`skipcheck` (`0x51C`, `0034F160`) is the idiom's test.~~ *(corrected 2026-09-30, FABLE, on OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930 and ORACLE's [rc15-regfile-skipmask-0930](../rc15-regfile-skipmask-0930/README.md):)* `skipcheck` (`0x51C`, `0034F160`) returns `003604A0(n, m)` (`0034F17E`), the entry's begun word `[022CB738 + (n + m*8)*16]`, which `00360710` sets: it reports that a skip has begun, not a raw input.
- **The manager:** event scripts run in managers 1 to 3, the event managers. The audio and voice pages map managers 1-3
  to kind 8, the event-script table (`0032F170`), and the field runtime pass stages them in order 1, 2, 3
  (`CONTRACT-field-runtime-pass.md`). So `m` is not 0 for these scripts' actors.

~~**So the skip mask is set in shipped play whenever a player skips one of these event cutscenes.**~~ *(corrected 2026-09-30, FABLE, on OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930 and ORACLE's [rc15-regfile-skipmask-0930](../rc15-regfile-skipmask-0930/README.md):)* **So the skip mask is set in shipped play whenever the player confirms the pause-menu skip while an entry is registered, which any of the 257 scripts that call `skipstart` can arrange, or when a script forces a skip with `skipexec`.** The chain is:
- `skipstart(1)` registers the entry and sets its bit;
- ~~`skipcheck(1)` reports the player's skip, or `file_var_s0_1 == 1`;~~ *(corrected 2026-09-30, FABLE, on OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930:)* `skipcheck(n)` reports a skip already begun, or a file variable forces one;
- `skipexec(1)` begins the skip through `00360710`, which proceeds on the registered entry.

~~The engine route `00360880` (from `00228130`) re-issues the begin for each set bit of `022CB9C4`.~~ *(corrected 2026-09-30, FABLE, on OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930:)* The engine route `00360880` (from `00228130`) begins the lowest registered entry of each event manager 1 to 3. Whether a given
session contains such a skip is the player's choice, not a question for static evidence.

Limits: the 12 `skipexec(0)` uses (request slot 0) follow the same route with `n = 0`, and were not traced separately.
~~`00228130`'s own trigger was not read.~~ *(corrected 2026-09-30, FABLE, on OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930 and ORACLE's [rc15-regfile-skipmask-0930](../rc15-regfile-skipmask-0930/README.md):)* `00228130`'s trigger is bit 13 of `[[0209AC30] + 0x400]`, which the pause menu `00228C70` sets through `00285EA0` when the player confirms the skip (ORACLE's K5, K6, re-run by FABLE).

## RC-15: native access to the register file — answered: only the interpreter reads or writes it

- **Stores (T5, `../fable-astra-live-facts-0930/t5_regfile_reuse.md`):** only the interpreter stores through a record
  into `+0x64..+0x83`, and the only native clear is the pool memset `00267A8B`.
- **Loads (T6, [`t6_regfile_loads.py`](t6_regfile_loads.py), [output](t6_regfile_loads_h2.out)):**
  - It is T5's census with loads in place of stores, over the 1,146 functions that reach a record through the getter
    `00358940`, the manager array or the initialisers, plus 2 hops of callees.
  - Control: the interpreter's register loads `002616AF`..`0026172C` are found.
  - 43 functions load somewhere in the range. **Every base is typed, in [`rc15_typing.md`](rc15_typing.md); no row is
    unresolved.**
- **The typing:**
  - Record-register reads come only from the interpreter.
  - Every other load reads a different object:
    - the script image header through the manager (`[manager+0]`, word or offset reads);
    - the actor manager itself (qword region pointers; `00262440` / `00265770` / `0026D3E0`, whose `rcx` is the manager);
    - widgets from the `00244F50` factory (a `+0x7C` flag word);
    - a battle-stats slot (a status mask);
    - the battle unit;
    - static tables (`02EC0B81`, `02EBF9E0`);
    - an element of a `0xA0`-stride array;
    - a sub-object's vector (`002ED6A0`: `[[owner+0xC0]+0x138]`, a 16-byte copy from `+0x60`);
    - a local float box in a frame (`003A4290`, `rbp` = the frame pointer);
    - the sub-objects already typed.
  - Three linear-slice labels in `t6_basedefs_h2.out` were wrong: `002ED6A0`, `003A4290`, and the manager functions.
    The typing corrects them with evidence addresses.
  - The VM's indexed variable path, the other native route near the record, resolves its "local" class through
    `00264E30` to `[slot+0x50] + [[record+0x40]+0x1C]`, inside the script image, not the record.

**So, within the census reach (2 hops), no native code other than the interpreter reads or writes the VM register
file.** This agrees with FZ-21 and closes the route RC-15 asked about.

Limit: a record pointer held longer than 2 call hops, or reached only through an indirect call, is outside the census.
Both are stated in T5 and T6.

**Incorporation (SWE2-CONTRACT):**
- ~~RC-16 ANSWERED;~~ *(corrected 2026-09-30, FABLE, on OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930 and ORACLE's [rc15-regfile-skipmask-0930](../rc15-regfile-skipmask-0930/README.md):)* RC-16 NARROWED (the residue is which record a spawn entry's function runs on);
- RC-17 ANSWERED;
- RC-15 ANSWERED (no native access but the interpreter, within 2 hops);
- the interpreter page section 13.3 and the native-command lifecycle page.
