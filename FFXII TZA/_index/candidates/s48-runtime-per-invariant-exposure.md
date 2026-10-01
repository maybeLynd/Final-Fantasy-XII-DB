# S-48 runtime: per-invariant stub exposure for EXP-108 / 109 / 113 / 114 / 117 / 119 / 120 (OPUS, 2026-09-25, block 301)

*Drafted by a delegated OPUS pass and reviewed before publication (block 301): its concrete address claims were spot-checked against the image; see the block-301 inbox entry for which.*

**Row:** S-48, authored command ramp channels.
- **Runtime verdict:** MIXED, with the qualifier *"isolated original-code execution under disclosed stubs — no
  per-invariant stub-exposure analysis yet"*. The cell lists channel consumers `003B6020`/`003B62D0` (EXP-108),
  pool lifecycle (109), 113/114, slot-handle algebra (117), and T51/E20 plus tail resolvers (119/120).
- **Binding gap:** *"types PARTIAL, runtime ASTRA/ORACLE's gap"*.
- **Contract:** one, `17-Presentation-Rendering/CONTRACT-authored-command-ramp-channels.md`. Its §4 holds five
  properties, labelled I1–I5 here in §4 order.

This note scores nothing.

**The headline: no record in the cell executes any function that I1–I5 are about.** The invariants are properties
of these functions:
- the four setters `003B6A90`, `003B69B0`, `003B6A10`, `003B6950`;
- the per-tick advance `003B5890`.

None of the seven harnesses has any of these five in `bodies.json` `real` or `scripted`. Neither does the gate
writer `003B6930`. A grep of every `_experiments/evidence/*/bodies.json` and `check.py` for these VAs returns
nothing. So every invariant is a **coverage** item, not an exposure item.

The setters and the advance are also leaves: `disasm_fn.py` shows no `call` or `jmp` out of any of the five bodies,
and `003B6930` is a 7-instruction leaf. **In any harness that runs them, no stub can sit inside them.**

## Substitutions per record

Sources:
- the `real` and `scripted` lists in each `evidence/<dir>/bodies.json`;
- each record's execution table and method notes;
- IAT names resolved with `iat.py`.

| record (frontmatter contract) | runs as shipped | substituted |
|---|---|---|
| **EXP-108** `ramp-channel-consumers-exec` (ramp contract) | PASS `003B6020`; BLD `003B62D0`; SWAP `003A1DB0`; FIN `0036F360`; K3F `00264670`; RLUT `0046FAE0`; RES1 `003B6BF0`; GATE `003E6F70`; RES2 `00421FF0`; BASE `0020E600` | application stubs: `003E56A0`, `002ED570`, `00370F60`. All three run real later: 120, 117, 120. Fixtures: slot/record tables, draw buffers, ring, templates, and the gate cell `02B40524` |
| **EXP-109** `render-pool-lifecycle-exec` (**render-record-pool-lifecycle** contract) | 29 bodies, including the ramp-table allocator SLTI `003B6890`, CLR `0041F730`, and HC1 `003B6000` (clear-enable of a ramp slot) | application stubs: RINIT `00420480`, PTD `0041FCF0`, **HID `003B56D0`** (the ramp slot allocator, real in EXP-117), PHOOK `0042C410`, TDOWN `004200A0`, `0042F4C0`, `003E56A0`, MIDS `002ED570`, T51 `0051B9E0`, `00512EF0`, `0040DB70`, `0032E400`/`620`/`520`, and the allocator trio `0036C1D0`/`0036A100`/`0036C140`. Import bridge: `00861EC0` → IAT `008C2A60` = `VCRUNTIME140!memset`, implemented as a real fill |
| **EXP-113** `shadow-sync-stage-exec` (ramp contract) | GATE `00428E40`, WALK `00426420`, SYNC `00426340`, V1 `003B6900` (writes slot `+0x41`), V2 `003AFD00`, LODS `003B6B80`, THUNK `00521440` | application stubs: LODC `003B5980` (real in 114) and PASS `003B6020` (real in 108) |
| **EXP-114** `shadow-lod-compute-exec` (ramp contract) | LODC `003B5980`, **ACC `003B5C00`**, CPY `003B5CE0`, **INIT `003B5D40`**, **FSYNC `003B5E20`**, CLRE `003B6000`, LEAF `0036DD80` | application stubs: RES2 `00421FF0` and GATE `003E6F70`, both real in 108. Import bridge: `00861F14` → IAT `008C2BB8` = `api-ms-win-crt-math!sqrtf`, answered with `math.sqrt` |
| **EXP-117** `slot-handle-algebra-exec` (**render-record-pool-lifecycle** contract) | **HID `003B56D0`**, FLDR `003E5AD0`, RES `003AB7F0`, MIDS `002ED570`, D6A `003E6DA0`, BASE `0020E600` | application stubs: `0036B130` (real in EXP-084) and `00370E20` (real in 119). HID's own two calls go to FLDR, which is real |
| **EXP-119** `t51-tail-resolvers-exec` (**render-record-pool-lifecycle** contract) | `0051B9E0`, `0051F240`, `00370E20`, `003AB7F0`, `0020E600` | application stub: `0036B130` (real in EXP-084) |
| **EXP-120** `exp108-tail-resolvers-exec` (**render-record-pool-lifecycle** contract) | `003E56A0`, `00370F60`, `0020E600` | **none** (`scripted: []`) |

**Four of the seven records name a different contract.** EXP-109, 117, 119 and 120 carry
`contract: CONTRACT-render-record-pool-lifecycle.md` in their frontmatter. That is S-38's contract. The row cell
counts them toward S-48.

## Per invariant

| invariant (§4) | functions it is about | executed by (cell records) | can a substitution reach it? |
|---|---|---|---|
| **I1** the identity guard writes nothing (`rec[0x10] != id` returns before any store) | setters `003B6A90`/`003B69B0`/`003B6A10`/`003B6950` | **none**. EXP-117 runs the identity's producer, HID `003B56D0`, stub-free (`d[+0x10] = gen<<8 \| slot`). The guard itself never runs | **not executed: coverage, not exposure** |
| **I2** `steps == 0` is immediate and clears the counter | setters | **none** | **not executed** |
| **I3** the value is never clamped to the target | setters + advance `003B5890` | **none** | **not executed** |
| **I4** a paused slot does not accumulate; the counter is decremented only on ticks that pass both gates | advance `003B5890` | **none**. EXP-113 runs the per-slot `+0x41` writer V1 `003B6900` real. That is the gate's input, not the gated decrement | **not executed**. See the scope finding below |
| **I5** counters are bytes, with no saturation check in the setter | setters | **none** | **not executed** |

**On the exposure question, the set is empty**, and the reason is coverage: no substitution in the seven records
touches `003B5890`, `003B6930` or the four setters, because none of these runs at all.

The substitutions that do exist, and where their effects land:
- **application resolvers:** `002ED570`, `003E56A0`, `00370F60`, `0036B130`, `00370E20`, `00421FF0`,
  `003E6F70`. Their returns feed BLD's and LODC's object pointers, which the consumers read. The ramp
  counter/value/delta fields are not written through them.
- **HID stubbed inside EXP-109** only. It runs real in EXP-117.
- **the allocator trio** under SLTI `003B6890`. `0036A100` returns the table pointer that is stored at `02B40528`.
  That is the table's address, not any I1–I5 value.
- **imports:** `memset`, `sqrtf`.

## Findings

1. **Executions of I1–I5 exist outside the cell.** Contract §13 cites `diff_ramp_channels.py`
   (`Reconstruction/Tests/Differential/`, SWE2-CONTRACT 2026-09-13, `a27b5cc5`). It is not an EXP record.
   - **What it runs at their real VAs:** the four setters, the advance `003B5890` and the allocator `003B6890`
     (constants at lines 162–167).
   - **What it hooks:** only the allocator's three externs, `0036C1D0` lock, `0036A100` alloc and `0036C140` unlock
     (lines 31–34, 169–171).
   - **Reach:** those hooks can reach none of I1–I5. They supply the table address and a lock trace. The five
     subject bodies are call-free.
   - **Gate writer:** `003B6930` is described in the harness prose (line 46) and is **not** one of its six driven
     entries.
   - Read here from the harness source only; the harness was **not run**.
2. **I4's §4 wording is scoped more narrowly by the contract's own §5/§6.** `003B5C00` (ACC) applies the same
   five-channel step to one slot:
   - **Gates it tests:** only the identity (`cmp [rax+0x10],ecx` at `003B5C11`) and enable
     (`test byte [rax+0x40],1` at `003B5C1A`). It does not test `+0x41` or `02B40524` (full 214-byte disassembly).
   - **Callers:** `0041C850` and `PresentationEntry_RebuildAndFastForwardToTime` `0041D820`.
   - **The contract already says so in §5/§6:** "a paused slot still advances on that route". §4 item 4 does not
     carry that qualifier.
   - **Execution:** EXP-114 runs ACC real (cases `acc-on`/`-gen-bad`/`-off`/`-idle`/`-ch0`/`-ch43`). No case plants
     `+0x41` or the gate cell.

   The pause-independence is therefore a static reading, confirmed by disassembly here and not by a pause-varying
   case. MEANING NOT CLAIMED: whether the fast-forward route matters in play is not read.
3. **Other shipped writers of the channel fields, executed real in EXP-114** (all confirmed by disassembly):
   - **INIT `003B5D40`** writes the fifth channel: `mov [r9+0x43],dl` at `003B5DB0`, `[+0x98]=0` at `003B5DB4`,
     `[+0x9C]` at `003B5DEF`, and a first step at `003B5DFC`–`003B5E0B`.
   - **FSYNC `003B5E20`** zeroes counters `+0..+3` with `mov dword [r9],0` at `003B5FE9`, and copies values into
     `+0x50/54/58/5C/70`.

   The contract names both in §5/§6. They are not stubs, and they do not bear on the exposure question. They are
   listed because they are the only channel-field **writers** any cell record executes.
4. **Contract §13's "Still not executed. The consumers — `003B6020`'s bit-1 arm and the shadow draw…" is stale**
   against EXP-108 (PASS/BLD real) and EXP-113 (shadow stage real). This is contract text, not a cell, and is noted
   only.
5. **The binding gap is consistent with the row's cells.** The types cell reads PARTIAL. The runtime attribution
   ("ASTRA/ORACLE's gap") agrees with the finding that no cell record runs the invariants' functions. The cell's
   phrase "the ramp surface executed" covers consumers, allocator, slot allocator and resolvers, **not** the setter
   and tick that §4 constrains.

## For the scorer

- **Stub exposure on I1–I5: empty.** No substitution in EXP-108/109/113/114/117/119/120 can reach an I1–I5 value
  or ordering.
- **Why it is empty: coverage.** None of the seven records executes a setter (`003B6A90`, `003B69B0`, `003B6A10`,
  `003B6950`), the advance `003B5890` or the gate writer `003B6930`. Confirmed by `bodies.json` lists and an
  evidence-wide grep. **All five invariants are unexecuted by the cell's records.**
- **Substitution classes present:**
  - application stubs on resolvers and allocators, each run real in another record: HID in 117; `002ED570` in 117;
    `003E56A0`/`00370F60` in 120; `0036B130` in EXP-084; `00370E20` in 119; `00421FF0`/`003E6F70` in 108;
    LODC in 114; PASS in 108;
  - the allocator trio `0036C1D0`/`0036A100`/`0036C140`, run real in no cell record;
  - import bridges `memset` (IAT `008C2A60`) and `sqrtf` (IAT `008C2BB8`);
  - fixtures: planted slot and record tables and the gate cell.
- **Four of the seven cell records name `CONTRACT-render-record-pool-lifecycle.md`**, not this row's contract:
  EXP-109, 117, 119, 120.
- **The only execution of I1–I5 found is `diff_ramp_channels.py`.** It is a differential harness with no EXP record
  and is not named in the cell. It hooks only the three allocator externs, which cannot reach I1–I5. Not re-run here.
- **I4 as worded in §4 is narrower than the shipped behaviour the contract itself documents in §5/§6.**
  ACC `003B5C00` steps without the pause gates. It is executed real in EXP-114, but without a pause-varying case.
- **Evidence class:** original-code replay (NATIVE-REPLAY) and static. `live_game: false` in all seven records.
  Nothing live.
