# RC-15, RC-16 and RC-17: the register file's native access, its persistence, and the skip mask (ORACLE, 2026-09-30)

SWE2-ORACLE's static lane, run by OPUS, for register rows RC-15, RC-16 and RC-17 (`_index/OPEN-QUESTIONS.md`, section RC).
**Every row here is corroboration of FABLE 0870d8b62** ([`../rc151617-fable-0930/`](../rc151617-fable-0930/README.md)),
which answered all three first. OPUS stopped new work on these rows when that commit landed. This record keeps the
independent results already in hand, and states each disagreement with FABLE's answer explicitly: FABLE's claim is
quoted, then the evidence against it. No census was started after the stop. Shipping image `73461d08…`; every script
here runs from this folder with `python -B`.

## The questions

- **RC-15.** Does any native path read or write the script VM's eight per-actor registers (ActorStorageRecord `+0x64`
  to `+0x83`) by a route the FZ-21 census does not see?
- **RC-16.** Does the register file persist across a record's occupants, so that a new logical actor in a reused record
  can read a register before its own first write?
- **RC-17.** Is the actor-manager skip mask (manager slot `+0x201`) set in shipped play? Which scripts issue `skipexec`
  (command 1337) or otherwise start a skip, and when does the engine's loop over managers 1 to 3 run?

## Method

**RC-15** ([`rc15_flow.py`](rc15_flow.py), [output](rc15_flow.out), [every access](rc15_flow.tsv); about 36 minutes)
follows the record pointer itself rather than a hop count. It subclasses the `k14_actorflow.py` engine with the token
`A` = an ActorStorageRecord.

The record's sources:
- the manager array `02098E10`: slot `+0x08` is the pool, and pool `+8+k*8` is a record;
- the first two arguments of all 1,886 verb-handler addresses in `scriptvm-verb-table.tsv`;
- every function found to return a record (77 functions, to a fixpoint);
- every global the flow saw a record stored into (24, iterated over 3 rounds).

`A` is followed through registers, the stack, offsets, direct callees with context (depth up to 14), tail jumps and
switch tables. The census lists every read or write whose bytes can overlap `A+0x64..+0x83`, including accesses at an
unknown offset (`A+?`), and every memcpy / memset / memcmp / `004746F0` call with a record in `rcx` or `rdx`. The
controls C1 and C2 require the interpreter's eight register loads and eight register stores to be reached through the
flow (roots → `0025D9E0` → `0025DF00` → `0025E4C0`), not seeded. Both PASS.

**RC-16** ([`rc16_check.py`](rc16_check.py), [output](rc16_check.out), FAILS 0):
- S1, S2 (image): who initialises a record, and when the pool is zeroed.
- D1, D2 (the decompiled US corpus, 1,114 scripts, `Database/Tools/work/FABLE/pub140-scratch/corpus/us`): every
  `regI1` loop FABLE cites, with the function it sits in (control: `gol_b01` `spawn00`), and every request of the
  `rbn_a03` takeover functions whose F0..F3 read FABLE cites.

**RC-17** ([`rc17_skip_chain.py`](rc17_skip_chain.py), [output](rc17_skip_chain.out), FAILS 0): each link of the chain
is asserted from the decoded image (K1 to K6 below). The script census is a grep of the same decompiled US corpus.
Helpers: [`rd.py`](rd.py) (disassemble a function, list rel32 callers), [`refs.py`](refs.py) (rip references to an
address), [`scan_bit13.py`](scan_bit13.py) ([output](scan_bit13.out)).

## Result

### RC-15: corroboration of FABLE 0870d8b62. Agrees: no native code but the interpreter reads or writes the register file

- **Scale.** 10,787 bodies in 53,342 contexts. C1 and C2 PASS: all 16 interpreter register accesses (`00261624`..`002616A1`
  stores, `002616AF`..`0026172C` loads) are reached through the flow.
- **Every other access with a record base is at an unknown offset, and each is an indexed field above the register
  file:**
  - `[rec + idx*2 + 0xC8]`, the override slots, in `0025AE00` (`0025AEC2`, write), `0025AF60` (`0025AFA1`, write),
    `002652D0` (`0026530B`, read) and `00269860` (`00269951`, read);
  - `[rec + ch + 0x8C]` and `[rec + ch + 0x94]`, the channel tail and head bytes, in `003DB2A0` (`003DB39D`, `003DB3AB`,
    `003DB3D1`, `003DB3E0`), `003DB420` (`003DB4A0`) and `003DB6E0` (`003DB710`).

  None of them reaches `+0x83` unless its index is negative: at most -36 for `+0xC8`, -9 for `+0x8C`, or -17 for
  `+0x94`.
- **Two "BULK-READ" lines are a filter false positive.** At `0034C6DA` and `0037CF71` the mnemonic is `cmovs`, a
  conditional move and not a string instruction; the substring test `"movs" in mnemonic` let them through.
- **No memcpy, memset, memcmp or `004746F0` call receives a record pointer** (0 bulk calls). So no native bulk copy or
  clear touches a record, apart from the pool memset, whose destination is the pool, not a record token.
- **So FABLE's answer holds, beyond FABLE's reach.** FABLE: "within the census reach (2 hops), no native code other than
  the interpreter reads or writes the VM register file." This flow is not hop-bounded, and it finds the same. Its own
  limits are listed under Not claimed.

### RC-16: corroboration of FABLE 0870d8b62, with disagreements. ORACLE's verdict is NARROWED (FABLE: ANSWERED). The file persists for the life of a pool; the reads that could see it are in spawn functions, not init

- **The only native clear is the pool memset, and it runs only when a manager's runtime is built.**
  `ActorStorage_InitializeRecord` `00266530` has one caller, `00267B79` in the pool allocator `002679F0`, and no pointer
  to it exists (S1). `002679F0` has one caller, `ActorSystem_InitializeManagerRuntime` `0026CE60` (`0026CEB0`). It
  allocates `ebx` bytes at `00267A79` and calls `memset(pool, 0, ebx)` at `00267A8B` (S2). `0026CE60` is reached from
  the manager request drain `0025BFB0` (`0025BFF6`) and `ActorResource_FinalizeManagerRuntimeAfterLoads` `0032F1B0`
  (`0032F227`). So the file is zeroed when a manager slot builds its runtime, and at no other time. RC-15's census below
  finds no other native write.
- **Within one pool a record belongs to one authored actor.** The allocator carves one record per authored actor
  ordinal and initialises each exactly once. No other initialiser exists. A "new occupant" of a record inside one pool
  can only be the same authored script actor starting again: a respawn, or a re-key (`002659D0` advances the handle's
  `+0x16`). A different authored actor never inherits a record's registers inside one pool. Across pools the file
  starts at zero.
- **The `regI1` reads FABLE found are in the spawn-group spawn and respawn functions, not in `init()`** (D1). The loop
  `regI0 = 1; while ((regI1 != -1 && regI0 < 64)) { regI1 = btlAtelGetDeadCountMax(regI0); ... }` appears **516
  times in 12 US scripts**, in `spawn00`..`spawn09` and `respawn00`..`respawn09` of 67 actors (67 each of `spawn00`,
  `respawn00`, `spawn01`, `respawn01`; 49 of `spawn02`; down to 1 of `spawn09`). It sits on the
  `btlAtelGetRespawnCause() == -1` path. The loop always leaves `regI1 = -1` unless 63 groups are defined, because
  `btlAtelGetDeadCountMax` returns -1 past the last group. So when several of these functions run on the same record in
  one pool lifetime with cause -1, only the first sums the dead counts into `file_var_s26_1` / `_2`; the rest find
  `regI1 = -1` and skip. `btlAtelGetRespawnCause` (`0050FC90` → `00236670`) returns -1 unless the keep entry's
  activation bit 1 is set and bit 2 (released) clear, so cause -1 means an entry not yet activated since its bank was
  wiped.
- **The `rbn_a03` F0..F3 read is not shown to run.** `SND_WOMAN_A`'s `エントリキャラ乗っ取り解除` reads F0..F3 that its own
  code never writes, as FABLE says. But no script in the corpus requests `エントリキャラ乗っ取り解除` or
  `エントリキャラ乗っ取り２` by name (D2). `rbn_a03`'s only computed-target requests are `sysReq(4, 65 or 38+i, 10)`,
  `sysReq(3, 65 or 38+i, 9)` and `sysReq(1, getmyid(), 4)`; they were not resolved to function names.

**The residue is one fact.** Do a spawn-group actor's `spawnNN` / `respawnNN` functions run on that actor's own record,
several spawn entries sharing one register file, or does each spawned unit run on a record of its own? The first
makes the persistence observable in every pool: the totals are summed once per record, not once per spawn. The second
confines it to a record re-used by the same entry. Either way the fact is static: the record the spawn engine passes
when it requests a spawn entry's function. It was not traced here, so the row is not routed to ASTRA.

**Agreement.** FABLE says "the register file does persist across occupants, and shipped scripts read it before their
own first write". The persistence and the read-before-write hold (S1, S2, D1).

**Disagreements, each with FABLE's claim quoted:**
1. FABLE: "66 of them are monster scripts' `init()`". **Evidence:** the loop is in `fn_spawn` / `fn_respawn` functions,
   **516 times in 12 scripts**, in `spawn00`..`spawn09` and `respawn00`..`respawn09`. Control: `gol_b01` `spawn00`
   (D1). None of them is an `init()`.
2. FABLE: "reused record: if the previous occupant left `regI1 = -1` ... the loop does not run", and the run-time fact
   left is "same pool or new pool". **Evidence:** within one pool a record is initialised once, by the allocator's one
   caller, for one authored actor (S1, S2). So the "previous occupant" is the same authored actor's earlier spawn or
   respawn function on the same record, never a different actor. Across pools the memset zeroes the file. The fact
   left is which record a spawn entry's function runs on (the residue above), not which pool a spawn is in. That is
   why ORACLE's verdict is NARROWED, not ANSWERED.
3. FABLE: `SND_WOMAN_A` "restores a position its own code never stored: zeros in a fresh pool, or the previous
   occupant's saved position in a reused record", and the effect is one "the player can see". **Evidence:** no script
   in the 1,114-script corpus requests `エントリキャラ乗っ取り解除` or `エントリキャラ乗っ取り２` by name (D2), and
   `rbn_a03`'s three computed-target requests are unresolved. A different actor never occupies the record inside one
   pool (S1). So a reachable read and a visible effect are both unproven for this function.

### RC-17: corroboration of FABLE 0870d8b62. Agrees on the chain, with disagreements on the loop and the trigger. ANSWERED. A skip is set when the player confirms the pause-menu skip, or when an event script forces one

The chain, each link asserted by `rc17_skip_chain.py`:

- **K1, the verbs.**
  - `skipstart` is `0x51A`, begin `0034D3A0`. It calls `00360980(n, owner +0x15, owner word +0)`.
  - `skipcheck` is `0x51C`, result `0034F160`. It returns `003604A0(n, m)` = dword `[022CB738 + (n + m*8)*16]`, the
    entry's "begun" word.
  - `skipexec` is `0x539` = **1337**, result `0034ECF0`. It pops `n` and tail-jumps `00360710(n, m = owner +0x15)`.
- **K2, the skip begin `00360710`.**
  - It returns 0 at once when `m == 0`.
  - The entry is `022CB730 + (n + m*8)*16`. It proceeds when `00267330(m)` is 0 and the entry's `+0xC` is set.
  - It moves bit `n` from the registered mask `022CB9C0 + m*4` to the begun mask `022CB9D8 + m*4`, and sets `+8 = 1`
    and `+2 = 2`.
  - It calls `0026A5B0(m, 1, n)`.
- **K3, the mask.**
  - `0026A5B0` sets bit `n` of byte `02098E10 + m*0x288 + 0x201`, the skip mask; `00267310` reads the same byte.
  - `00360980` (skipstart) sets the registered bit.
- **K4, the engine loop `00360880`.** For `m` = 1, 2, 3 it reads the registered word `022CB9C4 + 4(m-1)`. It takes
  the **lowest** set bit `n < 8` and calls `00360710(n, m)` **once per manager**, not once per set bit as FABLE's
  wording has it.
- **K5, when the loop runs.**
  - `00360880`'s only caller is `002281B7` in `00228130`. That is a widget procedure with no direct caller, installed
    by `00228700` through the widget factory `00244F50`; the object is kept at `[0209AC30] + 0xC8`.
  - It runs `00360880` only in its message-18 arm, and only when bit 13 of dword `[[0209AC30] + 0x400]` is set. It then
    clears the bit (`002281C3`).
- **K6, who sets bit 13.**
  - Among the functions that reference `0209AC30`, the only instruction that can set it is `00285EB6` in `00285EA0`,
    which sets bit 13 to its argument's bit 0.
  - `00285EA0`'s only caller is `0022917A` in the pause-menu procedure `00228C70`, message 2, state 4 (jump table
    `002294EC` entry 4), with argument 1. The same arm closes the menu (`00244F00`) and posts the controller's close
    (`00227DD0(1)` sets `[[0209AC30] + 0xC8] + 0xCC = 2`).
  - State 4 is entered from state 3, `mov dword [rbx+0xE6], 0x40003` at `00229342`. That is message 10 (input), taken
    only when the menu's flag bit 1 is set and the pad matches button entry `0x113`. State 4 proceeds when
    `002CCC70(2)`, the status of child widget 2, is non-zero.

So the engine loop runs when the player confirms the pause-menu skip. The menu closes, the pause controller `00228130`
tears down (message 18), and for each event manager 1 to 3 the lowest registered skip entry begins, setting that
manager's `+0x201` bit. The wider writes at displacement `0x400` elsewhere in the image are listed in the output. None
is in a function that reaches `0209AC30`; their bases were not typed one by one.

**What the shipped scripts do** (US corpus):
- `skipstart` appears in **257 scripts**: `skipstart(0)` 277 times, `skipstart(1)` 12, `skipstart(2)` 1,
  `skipstart(3)` 2.
- `skipcheck(0)` appears 229 times and `skipcheck(1)` 8.
- `skipexec(1)` appears 7 times, in `alc_z0200`, `bhm_a0200`, `bhm_y0101`, `bhm_z0100`, `byu_y0100`, `ene_a0200` and
  `fon_b0100`. `skipexec(0)` appears 12 times.
- The common idiom is `skipstart(0)` ... `skipend(0)` around a cutscene. The player's pause-menu skip then begins
  entry 0 of that script's manager through `00360880`. `skipcheck(n)` reads the begun word that `00360710` set.
- `skipexec` is the script-forced form: `if (file_var_s0_1 == 1) skipexec(0);`, or
  `if ((skipcheck(n) || file_var_s0_1 == 1)) skipexec(n);`.

**Agreement.** Every address in FABLE's chain is reproduced (K1 to K3): `0034ECF0` → `00360710`, the `m == 0`
refusal, the entry table `022CB730`, `skipstart` → `00360980`, and the counts of 7 `skipexec(1)` and 12
`skipexec(0)`.

**Disagreements, each with FABLE's claim quoted:**
1. FABLE: "`00360880` ... runs `00360710(bit, m)` for `m` = 1 to 3 over each set bit of `022CB9C4`". **Evidence (K4):**
   it reads a different word for each manager, `022CB9C4`, `022CB9C8` and `022CB9CC`. It stops at the lowest set bit
   (`bt` / `jb` at `003608A0`-`003608A3`) and makes one `00360710` call per manager.
2. FABLE: "`skipcheck(1)` reports the player's skip". **Evidence (K1):** `skipcheck` returns the entry's begun word
   `[022CB738 + (n + m*8)*16]`, which only `00360710` sets. It reports that a skip has already begun: through the
   engine loop after the pause-menu confirmation, or through an earlier `skipexec`. It does not report a raw input.
3. FABLE: "the skip mask is set in shipped play whenever a player skips one of these event cutscenes", the 19
   `skipexec` scripts. **Evidence (K5, K6, K2):** the player's pause-menu confirmation runs `00360880`, which calls
   `00360710` and so `0026A5B0` directly, for any registered entry. The mask is therefore set without any `skipexec`,
   in every one of the **257 scripts** that call `skipstart` (277 of them `skipstart(0)`).
4. FABLE: "All sit in the cutscene-skip idiom: `skipstart(1); if ((skipcheck(1) || file_var_s0_1 == 1))
   skipexec(1)`". **Evidence:** several `skipexec(0)` sites have no `skipcheck` at all: `alc_z0100` line 124 and
   `bhm_d0101` line 165 are `if (file_var_s0_1 == 1) { skipexec(0); }`.
5. FABLE: "`00228130`'s own trigger was not read". It is answered here: bit 13 of `[[0209AC30] + 0x400]`, set only by
   `00285EA0` from the pause menu `00228C70`, message 2, state 4 (K5, K6).

## Not claimed

- RC-15 (the flow's own limits; no census was started after the stop):
  - **Depth cuts.** 16 function-and-depth pairs carry a record and were cut at depth 15 or by recursion: `002482E0`,
    `00265020`, `00265200`, `002693D0` (recursion), `0026A5F0`, `0026B6A0`, `002E5C90`, `002E5E10`, `002E5FB0`,
    `002E7F70`, `002E8EE0`, `002EC3F0`, `003DB650`, `003DB7A0`, `003DC130`. Their bodies under those contexts were not
    re-run.
  - **Record pointers stored in object fields or indexed global arrays** were listed but not followed as new sources:
    - battle unit `+0x10` (`002344EF`);
    - slot-table row `+0x108` (`002E2A15`);
    - `[rbx + rcx + 0x20 / 0x28]` in `002572E0`;
    - the arrays `0209A1F0`, `0209A210`, `022C8060`, `022C8388`, `02AEE0C0`, `02EBCAC0` and `02B58C50` `+0x10`.
  - **Indirect calls that receive a record in `rdx`** were not seeded:
    - `[rec + 0x38]`, called at `0025E222` with target `00233F70` (stored at `00265AA8`);
    - `[manager + 0x98]` = `00264E30` (stored at `0026CB76`, called at `002625AB`, `00262617`, `00265113` and
      `0026D49D`).
    FABLE types `00264E30` as resolving into the script image, not the record. `00233F70` was not read.
  - **Side observation, not this row's.** `0025E217`-`0025E222` calls `[rec + 0x38]` as a function pointer, while
    `_types/fields.tsv` names ActorStorageRecord `+0x38` `boundBattleUnitPtr38`. This is routed, not corrected.
- RC-16: which record a spawn entry's function runs on (the residue above); what `btlAtelGetRespawnCause` is across
  area transitions that rotate rather than wipe the keep banks.
- RC-17: what the pause menu shows for the skip row, and whether child widget 2 is a yes/no confirmation. The input
  condition (flag bit 1, button entry `0x113`) is read, but not mapped to a physical button or a script-side enabler.
  The meaning of `00267330`'s gate (manager `+0x10` bit 0 set and bit 7 clear) is not claimed.
