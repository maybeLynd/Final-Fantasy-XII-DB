# RC-12, RC-13 and RC-14: footer slots, request channels and the run-state promoters (ORACLE, 2026-09-30)

SWE2-ORACLE's independent derivation (a non-author review) of SWE2-CONTRACT's rows RC-12, RC-13 and RC-14. FABLE answered
the same rows in [`../rc121314-fable-0930/`](../rc121314-fable-0930/README.md). This record **refutes FABLE's RC-12 slot
table** (every slot is off by one) and **corrects half of FABLE's RC-13 census** (the `sysReqchg` operand is a slot,
not a channel). It **confirms and closes RC-14**.

Scripts run from this folder with `python -B <script>.py` and exit 0 when their controls pass. They read:
- the shipping image `Database/Tools/work/exe/FFXII_TZA.exe` (sha256 `73461d0896204b1c…`), through `img.py`, a copy of
  `../rc8-cascade-count-0930/img.py` (.pdata chain-root extents, raw rel32 call index);
- the raw script images and the decompiled US corpus in `Database/Tools/work/FABLE/pub140-scratch/corpus/us` (1,114
  images).

Run at HEAD `6690d0b9f`.

## RC-12: which special-function slot each footer reader asks for

### The question

Which footer word each of the seventeen other readers of an actor entry's `+0x18` block reads. The wait resolver
`0025DF00` is the control, and the page says its word is the `mapjump` slot.

### Method

[`rc12_slots.py`](rc12_slots.py), with its output in [`rc12_slots.out`](rc12_slots.out), has three parts.

**Part A (image).** For each named function and each resolve call `0020E600` on `[entry + 0x18]`, the script reads three
operands:
- **D**, the footer byte offset of the word read;
- **C**, the bound constant compared with the count word;
- **O**, the record override word read first.

The footer is the tool's `tFuncFooter {u16 count; u16 special[18]}`, so word `k` is at `+2 + 2k`.

**Part B (authored data).** For all 26,390 actors in the 1,114 raw images, the script joins each footer word `k` to the
name of the function it indexes. The name comes from the image's own name pool (header `+0x4C`, entry `+0x10`), not from
the decompiler's printed number.

**Part C (image-wide).** Every resolve of `[entry + 0x18]` in the image, where the entry was loaded from `[.. + 0x40]`.

Controls:
- A: `0025DF00` reads D = `0x18` with C = 11.
- B: for all 14,081 declarations, the decompiler's printed `function NAME(n)` has `n` equal to the raw index `k`.
- C: every Part A site is found by the image-wide sweep.

All three PASS.

### Result: ANSWERED, and FABLE's table and the page's `mapjump` reading are both off by one

The raw footers name each word directly (Part B):

| k | byte | function the shipped footers point at |
|---|---|---|
| 0 | `+0x02` | never set in a footer (it is the spawn table's `entry` override, below) |
| 1 | `+0x04` | `main` |
| 2 | `+0x06` | `talk` |
| 3 | `+0x08` | `touch` |
| 4 | `+0x0A` | `touchon` |
| 5 | `+0x0C` | `touchoff` |
| 6 | `+0x0E` | `across` |
| 7 | `+0x10` | `spawn` |
| 8 | `+0x12` | `fieldsign1` |
| 9 | `+0x14` | `initevent` |
| 10 | `+0x16` | never set in a footer (it is the spawn table's `talk` override, below) |
| 11 | `+0x18` | **`parameter`** |
| 12 | `+0x1A` | **`mapjump`** |
| 13 | `+0x1C` | `fieldsign2` (and `touch2`) |
| 14 | `+0x1E` | `respawn` |
| 15 | `+0x20` | never set |
| 16 | `+0x22` | `talkhold` |
| 17 | `+0x24` | `talkterm` |

**The wait resolver `0025DF00` (read `0025E186`) asks for `parameter` (k = 11), not `mapjump`.** Its word is `+0x18`,
bound 11, and override `+0xDE`. The page's "`special[t]` at `+2t`, 1-based" reading shifts every slot up by one. The
tool numbers the array from 0 (`separator.special[function.specialType]`, `CScriptCompileAsmWrite.cpp`), and the raw
names above settle the question without relying on that.

Three facts confirm the numbering independently:
- **The override array agrees.** At every site the record override word read first is `0xC8 + 2k` (Part A column O), so
  the override slot equals the footer index.
- **The script-side writer agrees.** `REQCHG` writes override slot `s` through `0025AF60`
  (`mov word [rax + rbx*2 + 0xC8], di`). The shipped `sysReqchg(s, X::fn)` calls pass:
  - slot 2 with `talk*` (1,734 calls);
  - slot 3 with `touch*`;
  - slot 4 with `touchon`;
  - slot 5 with `touchoff`;
  - slot 16 with `talkhold*`;
  - slot 17 with `talkterm*`.

  This is [`rc13_script_channels.out`](rc13_script_channels.out).
- **The `parameter` functions fit the resolver.** They are persistent loops, for example `while (true) { wait(1);
  file_var = getmapid(); }` in `gil_b01`. The resolver's use sets record `+0x0C` bit 0 when the running function is the
  actor's `parameter` function.

The seventeen listed sites:

| reader | site(s) | slot(s) |
|---|---|---|
| `0025AE00` | `0025AEF9` | 10: the talk-list override (see `00263D40`) |
| `0025B820` | `0025B977`; `0025B9C6`, `0025BA62` | 10; 2 `talk` (twice) |
| `0025BAD0` | `0025BD19` | 16 `talkhold` |
| `0025C230` | `0025C4BE`, `0025C58B`, `0025C63B`, `0025C755`, `0025C7BC` | 3 `touch`, 13 `fieldsign2`, 8 `fieldsign1`, 5 `touchoff`, 4 `touchon` |
| `0025C830` | `0025CFD7`, `0025D087`, `0025D154`, `0025D2A7`, `0025D356` | the same five: 3, 13, 8, 5, 4 |
| `00263050` | `002631E8` | 17 `talkterm` |
| `00263D40` | `00263D72` | no fixed slot: the spawn-table accessor |

**`00263D40` reads the spawn table, not the footer.**
- It skips the footer plus `esi` more count-prefixed lists (`00263D90`–`00263D9F`), then returns item `rdi`
  (`00263DA8`). The lists after the footer are ff12-script's spawn table: `entry`, `spawn`, `talk`, `touch`,
  `respawn` (`_writeSpawnTable`, `_loadSpawnData`).
- Its only two callers, `0025AD10` (`0025AD3F`) and `0025AE00` (`0025AE6B`), pass list selector `r8d` in 0..4 (refused
  above 4) and item `r9d`.
- They store the function they get into the target record's override slot:

  | list | override slot |
  |---|---|
  | `entry` (0) | slot 0 |
  | `spawn` (1) | slot 7 |
  | `talk` (2) | slot 10 |
  | `touch` (3) | none |
  | `respawn` (4) | slot 14 |

  This is `0025AE77`–`0025AEC2`: `edi` = 0, 7, `r13` = 10, or `edx + 0xC` = 14. That is why footer words 0 and 10
  are never authored: those slots are filled from the spawn table.

**The listed readers are not all of them.** Part C finds 43 actor-entry footer resolves in 19 functions. The others
include:
- `0025B2E0` (k = 6 `across`);
- `0025B600` (12 `mapjump`);
- `00266530`, the record initialiser: 15, 9, 1, 2, 10;
- `002675C0` (2, 10);
- `00268EA0` (17, 16);
- `00269640` (0, 11);
- `00269860` (7, and a variable slot);
- `0026A660` (5);
- `0026CE60` (spawn-list walks and 10);
- `002652D0`, a variable-slot getter bounded to 0x11.

The full list is in `rc12_slots.out`.

## RC-13: what a request channel means to a script author

### The question

What each actor request channel means to a script author beyond its priority (highest channel runs first). The register
names the static step as a census of the channel operand the shipped `REQ` family passes, per function kind.

### Method

Two scripts:
- [`rc13_script_channels.py`](rc13_script_channels.py), with [`rc13_script_channels.out`](rc13_script_channels.out),
  tallies the first operand of every shipped call per call form. It separates `REQCHG`, whose first operand is an
  override slot (`0025AF60`, slot ≤ `0x11`). Control: the parsed count equals a plain count for every form.
- [`rc13_engine_channels.py`](rc13_engine_channels.py), with [`rc13_engine_channels.out`](rc13_engine_channels.out),
  resolves the channel at every native submit. The two native descriptor builders are `003DBB60` (channel `dl`) and
  `003DBBE0` → `003DBBF0` (channel `r8b`). The script also names the footer slot of the function filed. Controls: touch
  → channel 3 at `0025C4F4`, main → channel 0 at `002669F5`.

Sites whose value arrives through a join were read by hand. The readings are cited in the next section.

The per-channel mechanics were read in the insert `003DB7A0` (`003DB7A7`–`003DB894`, `003DB995`, `003DBA88`–`003DBAA2`,
`003DBABB`), in the chain unlink `003DB2A0` (`003DB3B8`–`003DB3CD`) and in the channel-count initialiser (`002667B6`,
`003DB594`).

### Result: NARROWED. The engine attaches fixed meanings to channels 0 to 7; FABLE's `sysReqchg` rows are not channels

**1. The engine files each special function it triggers on a fixed channel.** This is read at every native submit:

| channel | what the engine files there | sites |
|---|---|---|
| 0 | `main` (k 1) at record start; `parameter` (k 11) | `002669F5`; `00269766` |
| 1 | the `entry` function (override slot 0, from the spawn table) | `00269700` |
| 2 | `touchoff` (k 5); `spawn` (k 7), or `respawn` (k 14, which reverts to 7 when the image header word is below 6) | `0025C7E7` via `0025C770`, `0025D2E0`; `002699AB` |
| 3 | `touch` (k 3), `fieldsign1` (k 8); `talkterm` (k 17) for sequence-7 records | `0025C4F4`, `0025C669`, `0025D005`, `0025D182`; `00269033` |
| 4 | `touchon` (k 4); `talkhold` (k 16) for sequence-7 records | `0025C7E7`, `0025D39B` (`edx` = `r13 + 5` with `r13` = -1 at `0025D208`); `0025BD65`, `00268FF2` |
| 5 | `across` (k 6); `talkterm` (k 17) for every other sequence | `0025B3C3`; `00269033` (`ebx` = 5) |
| 6 | `mapjump` (k 12); `fieldsign2` (k 13); `talkhold` (k 16) for every other sequence | `0025B72B`; `0025C5B9`, `0025D0B5`; `0025BD65`, `00268FF2` |
| 7 | the engine-initiated talk: the slot in `0209A2BC` (bit 2 of record `+0x1C` when it is 2, else bit 10), filed from the world tick | `00268DD4` (`00268D10`, from `003141F7`) |
| top (count - 1) | function 0 and `initevent` (k 9) at record start; override slot 15; the setup actor's spawn-order list (header `+0x58`) | `00266957`, `002669A6`; `00266935`; `00266CD2` |

- "Sequence" is record `+3 & 0x1F`. The `talkhold` / `talkterm` choice is `0025BD32`–`0025BD44` and
  `00268FBC`–`00269011`.
- The channel count is 8, or 6 for sequences 2, 4 and 7. It is chosen at `0026655C` / `00266596` and stored at
  `003DB594`; `_types/fields.tsv` `ActorStorageRecord +0x88` holds it.
- A channel at or above the count is clamped from above only (`003DB7C1`–`003DB7C5`).
- Script-chosen channels reach native code through `REQALL` / `REQIALL` (`00268A80` → `00268B10`) and the verb `0AB`
  `sysreqall` (`0034F380` → `00269AD0`, whose channel and slot are both popped).

**2. A channel holds one request at a time for the only request kind shipped scripts use.**
- Record word `+6` is a per-channel occupancy mask:
  - the insert sets bit `ch` whenever it links an entry onto channel `ch` (`003DBA9F`);
  - the chain unlink clears it when the chain empties (`003DB3C5`, together with the same bit of `+0x24` and `+0x26`).
- A kind-0 descriptor (`REQ`) is refused when its channel's bit is set (`003DB888`–`003DB890`): the insert returns 3
  (`003DBABB`).
  - The interpreter's `REQ` tail ignores the result (`0025F7D5`).
  - `REQSW` / `REQEW` enter their wait only on result 1 (`002602E6`–`002602EE`).
- Kind 2 (`FREQ`) always files. Kind 4 (`TREQ`) files unless the same function id is already on that channel
  (`003DB7F6`–`003DB867`).
- The shipped bytecode has 0 `FREQ*` and 0 `TREQ*` opcodes against 198,401 `REQ`, 27,898 `REQSW`, 115,766 `REQEW`,
  46,637 `REQALL` and 3,691 `REQIALL` (`../fable-astra-live-facts-0930/ov16_opcode_histogram.out`).

So for an author: **a `REQ` onto a target channel that already holds a pending or running request is dropped
silently.** This includes a request the engine filed there, for example a pending `touch` on channel 3.

**3. The authored channels (script census) are 0 to 7 only:**

| channel | calls |
|---|---|
| 0 | 4 |
| 1 | 30,724 |
| 2 | 6,057 |
| 3 | 2,175 |
| 4 | 1,646 |
| 5 | 955 |
| 6 | 41 |
| 7 | 293 |

This counts every channel-taking form (`sysReq`, `sysReqi`, `sysReqsw`, `sysReqswi`, `sysReqew`, `sysReqewi`,
`sysReqall`, `sysReqiall`); the per-form split is in the output.

**Corrections to FABLE's RC-13 table:**
- **FABLE's rows "16" and "17", and its clamp explanation, are wrong.** They are the `REQCHG` slots `talkhold` (16) and
  `talkterm` (17), not channels.
- **FABLE's channel 2 ("most `sysReqchg` calls") is inflated.** It includes the 1,804 `REQCHG` slot-2 (`talk`) calls.
  The same applies to channels 3, 4 and 5, which include 14, 8 and 8 `REQCHG` calls.
- FABLE's per-function-name conventions for the true channel calls are not contradicted here.

**Residue (why NARROWED, not ANSWERED):** "meaning to an author" now rests on the engine's fixed per-channel filings and
the occupancy rule above. What an author *intended* by using, say, channel 1 for its own logic is a convention, not an
engine fact. No further static fact decides it. This is not an ASTRA question either: no run-time observation would add
an intent.

## RC-14: who moves an entry's `+0x11` run state from 1 to 2

### The question

Whether any code outside the functions the §2.5 displacement sweep covered moves an entry's run state from 1 to 2.

### Method

[`rc14_sweep.py`](rc14_sweep.py), with [`rc14_sweep.out`](rc14_sweep.out), sweeps the whole image:
- all 24,360 `.pdata` chain roots;
- a linear sweep of every `.text` run no `.pdata` entry covers (leaf code): 42,487 streams in all.

It looks for these shapes:

| shape | what it matches |
|---|---|
| S1 | `mov byte [R+0x11], 2` |
| S2 | the same store from a register whose last write is 2 |
| S3 | a store of 2 through a register advanced by `0x11` |
| S4 | `cmp byte [P],1 … mov byte [P],2` on one operand |
| S5 | any variable store at `+0x11` in an entry-array function |
| S6 | a variable store at `+0x11` anywhere else |

A function counts as an entry-array function when it loads `[.. + 0xA0]` and uses the `0x14` stride. The controls
`003DBB35`, `003DB245`, `003DBCAC`, `003DB8E9` and `003DB9E4` all PASS.

### Result: ANSWERED. Exactly three promoters and the insert, image-wide; FABLE's two additions confirmed

- **S1 and S2: none anywhere in the image.**
- **S3 and S4: exactly three stores reach an entry's `+0x11`.** All three are the same loop over
  `*(record + 0xA0) + 0x11`, stride `0x14`, gated by record `+0x63` and followed by the channel walk:

  | store | function | what calls it |
  |---|---|---|
  | `003DBB35` | the `003DBAE0` insert | the REQ submit `00268A18` |
  | `003DB245` | the per-manager sweep `003DB1F0` | `0026D365` and `World_UpdateSimulationTick` at `00314124` / `00314211` |
  | `003DBCAC` | the `003DBBF0` insert | the native submitter `003DBBE0`; runs only when target and issuer differ (`003DBC84`) |

  The other three S4 hits are not entry stores:
  - `0026A839` stores through `[.. + 0xC0] + 0x152`;
  - `00298BCC` and `00298C1C` store through `[.. + 0xC0] + 0xA`.
- **S5:** the insert's `003DB8E9` / `003DB9E4` store the caller's state argument:
  - 1 from `003DB790` and from the native special-function builder `003DBB60` (`003DBBB4`);
  - 2 from `003DBAE0` (`003DBAF8`) and from `003DBBF0` when an issuer is passed (`003DBC6D`).

  `003DB754` stores the record's own `+0x11`. The `003DC233` gap hit stores 0 (free).
- **S6: 21 variable stores, none on an entry.** By value or by base:
  - Eleven are read-modify-writes that cannot produce 2: `or al, 6` (bit 2 set), `or al, 1` (odd), `and al, 0xFD`
    (bit 1 clear). They are `0025DD8F`, `00265BA4`, `00265CD8`, `00265D40`, `0026CBF6`, `002E32FE`, `002E366B`,
    `002E3738`, `002E37EC`, `002E38AD`, `002E3A98` and the gap run at `00265FB8`.
  - The rest have non-entry bases:
    - `003332FC`: a fresh `0x170` allocation from `0036A190`;
    - `00333EF1`: an object from the table at `02EBEFA8`, or a `0x2C`-byte copy;
    - `003B04D2`: the result of `003B0980`;
    - `00404B4D`: a `0x50`-stride table;
    - the `003DF076` gap run: a `0x38`-stride table;
    - `002FF8B6`: the caller's object whose dword `+0x24` it just wrote, or that object `+ 0x24`. A dword store at
      `+0x24` is outside a `0x14`-byte entry;
    - `0065FA08`: a `{dword, qword, byte, byte}` copy that omits an entry's function id;
    - `006651F7` / `006655C7`: a `0x18`-stride base;
    - `00844107` / `00844661`: a base of `[rbx + 0x80] + r8`.

So besides the page's two writers of 2, the only promoters are FABLE's `003DB245` (the world-tick sweep) and
`003DBCAC` (the native insert with a distinct issuer), and FABLE's RC-14 answer stands. The mechanism is:
- every native special-function submit (`003DBB60`) files in state 1;
- the world-tick sweep `003DB1F0` promotes it on the manager's next pass.

This closes FABLE's stated limit, a pointer that is both passed in and pre-advanced: no store of 2 through a pointer
advanced by `0x11` exists outside these three functions.

## Not claimed

- What record `+0x0C` bit 0 does downstream, now that the wait resolver's test is `parameter`, not `mapjump`.
- The intent behind authored channel conventions (RC-13's residue).
- Whether both `World_UpdateSimulationTick` call sites of `003DB1F0` run every tick.
- The S6 base verdicts for `002FF8B6`, `0065FA08`, `006651F7`, `006655C7` and the two `00844090` stores are by
  structure shape, stride or caller object. They are not a full pointer-escape proof. No entry-array function passes an
  entry pointer to any of them in the code read here.

## Consumers to route (not edited here)

These places carry the off-by-one reading and will need SWE2-CONTRACT's correction, with `rc12_slots.py` Controls A and
B as the rejecting regression:
- the scheduling page §2.2, the `+0x18` table row;
- the scheduling page §2.6 and the §7 RC-12 box;
- `04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md` line 353 ("`+0x0C` … is the `mapjump` special
  function");
- `_types/fields.tsv` `ActorStorageRecord +0x0C8` (`overrideSlots`): it says "what each slot index selects is not
  claimed". This record now claims it: slot k = footer word k = special type k.
