---
experiment: EXP-001
title: Does FrameLimit actually drive the engine time base in a live process?
status: RUN 2026-09-08 — CONTROLLED A/B; the biconditional is CAUSAL, not merely co-occurring
contract: ../19-Save-Load-Settings/Game-Settings-Config/CONTRACT-game-setting-config.md
checks: EXP-001-gamesetting-frametimebase.tsv
tool: Database/Tools/analysis-kit/gfz-scripts/runtime_probe.py
method: C - ordinary UI input and read-only process observation
live_game: true
date_designed: 2026-09-08
date_run: 2026-09-08
harness: Database/Tools/analysis-kit/gfz-scripts/ffxii_runtime.py
evidence: Database/FFXII TZA/_experiments/evidence/EXP-001-gamesetting-frametimebase-*.json
---

# EXP-001 — `FrameLimit` and the engine time base

**Charter §15 experiment record.** Designed and run 2026-09-08; retained observations and failures
are below. The current check's E8 expectation was corrected on 2026-09-11 under §E8 below.

## Question

Does the `GameSetting.ini` `FrameLimit` setting actually select the engine's time base at runtime,
as the contract claims — and are the two states genuinely mutually exclusive?

## Hypothesis

From static analysis only (`CONTRACT-game-setting-config.md`, `DH-1`/`DH-2`):

| | `FrameLimit=30` | `FrameLimit=60` |
|---|---|---|
| `setting[18]` at `[0x01F82D20]+0x48` | `0` | `1` |
| `0x01DFE0B4` time base | **`1`** | **`2`** |
| `0x01DFE0B8` / `0x01DFE0BC` | `1.0f` / `1.0f` | `2.0f` / `0.5f` |
| `0x01F82E38` 60 Hz gate | **`0`** | **`1`** |

**The falsifiable prediction is the biconditional:** `setting[18] == 1` **if and only if**
`0x01DFE0B4 == 2`, and the gate at `0x01F82E38` is `1` on exactly the same condition. Nothing in the
database has ever been checked against a running process, so this is the first test of whether a
statically-derived chain survives contact with the game.

## Initial state

Game launched to any point past the CRT static initialisers — the title screen is sufficient, since
the config object is constructed before `main` and the frame-limit decision is the first call in
`0022A0B0`. **No save, no specific area, no combat required.**

## Variable being changed

> **CHANGED 2026-09-08 — this experiment is no longer an observation.** A third run varied
> `FrameLimit` in the installed `GameSetting.ini` and restarted the game. See §*The controlled
> arm* below.

None on the first run — this is an **observation**, not an intervention. A second run after changing
`FrameLimit` in the options and restarting would turn it into a controlled experiment; the settings
object is only read at startup, so a restart is required for the change to take effect.

## Control variables

Same build (`73461D08…`), same machine, no mods loaded, `XIIOnlineNet.dll` **not** injected — the
DLL writes engine state and would contaminate the reading.

## Instrumentation

```
runtime_probe.py --check "Database/FFXII TZA/_experiments/EXP-001-gamesetting-frametimebase.tsv"
```

**Read-only by construction.** The harness opens the process with `PROCESS_VM_READ |
PROCESS_QUERY_INFORMATION` and never requests write access, so it cannot perturb what it measures.

**Two mandatory controls run before any row is reported:**

1. **Base control** — module load address must equal PE `ImageBase` `0x00120000`. The image has
   `DYNAMIC_BASE` clear, so database VAs are runtime addresses; if that ever stops being true every
   address here is wrong and the tool refuses.
2. **Read control** — `0x01CCD300` must read back `19 93 0D 0A 1A 0A` (Lua's `LUAC_TAIL`). Without
   it, a failing read returning zeroes is indistinguishable from a field that is genuinely zero —
   and "the field is 0" is exactly what several rows below assert.

`C1` in the check file repeats the read control as a row, so it appears in the results table too.

## Expected result

All thirteen rows readable; `E9` in `0..8`; and the biconditional in the hypothesis holding across
`E1`, `E2`, `E3`, `E4`, `E5`. The original check also expected `E8` exactly `81`; that unconditional
expectation was incorrect. The current E8 row records the value without asserting initialization.

## Observed result

**RUN 2026-09-08, autonomously**: the harness resolved the clean reference environment, launched
`FFXII_TZA.exe`, waited for its own controls to pass, read every row, wrote the evidence file and
closed the game. **No human touched the game.**

**Reference environment:** `D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64`,
SHA-256 `73461d08…21f8` (authority match), no loader DLL, no `modules\`, no `hook.ini`; the live
module list contained **none** of the mod stack. The three `FFXII MP Mod` clients were **rejected by
name with reasons** — `mod-client-1` carries four loaders, an 11-file `modules\` and a `hook.ini`.

### Two runs, and the second is the one that counts

| row | address | run 1 — at the first readable instant | run 2 — 30 s after ready | contract's prediction for `FrameLimit=60` |
|---|---|---:|---:|---|
| `C1` | `0x01CCD300` | `0x0A0D9319` PASS | `0x0A0D9319` PASS | control |
| `E1` | `[0x01F82D20]+0x48` | **1** | **1** | 1 |
| `E2` | `0x01DFE0B4` | **1** | **2** | **2** |
| `E3` | `0x01DFE0B8` | **1.0** | **2.0** | 2.0 |
| `E4` | `0x01DFE0BC` | **1.0** | **0.5** | 0.5 |
| `E5` | `0x01F82E38` | **0** | **1** | 1 |
| `E6` | `+0x658` | 0 | 0 | 0 after a file load |
| `E7` | `+0x65A` | 0 | 0 | 0 after a file load |
| `E8` | `+0x448` | **0** | **0x69705F70** | 81 |
| `E9` | `+0x00` Language | 1 | 1 | 0..8 |
| `E10` | `+0x0C` Quality | 3 | 3 | — |
| `E11` | `+0x1C` Shadow | 2 | 2 | — |
| `E12` | `+0x64` DecideButton | 1 | 1 | 0 or 1 |

> ### The biconditional HOLDS
>
> At 30 s: **`setting[18] == 1` and `0x01DFE0B4 == 2`**, with `2.0` / `0.5` beside it and the 60 Hz
> gate at `0x01F82E38` reading **1** on the same condition. **Every element of the predicted
> `FrameLimit=60` column is present simultaneously in a live process.** The statically-derived
> chain survives contact with the game.

### The first run would have published a false falsification

Run 1 observed at the first instant the harness's controls passed and the singleton was non-null.
At that moment `E1` was **already 1** while `E2`/`E3`/`E4`/`E5` still read **1 / 1.0 / 1.0 / 0** —
the `FrameLimit=30` column. Taken alone that reads as **the biconditional failing**, and it would
have been written up as a live falsification of a claim the contract labels `PROVEN`.

> **It was a timing artefact, and the harness could not have known that without being asked.**
> `--settle` and `--repeat` were added for exactly this, and the answer changed the moment the
> question was asked properly. **A single observation cannot distinguish "the claim is wrong" from
> "we looked before the writer ran."**

### And that artefact is itself a new fact about the engine

**The settings object holds `FrameLimit` before the time base is switched.** There is a real window
in which `setting[18] == 1` and `0x01DFE0B4 == 1`, so **applying `FrameLimit` is not atomic with
constructing the settings** — the engine starts on the 30 fps time base and moves to the 60 fps one
later in startup. Static analysis showed the chain; only the running process showed the **order**.

Recorded as **PROBABLE** rather than proven: two runs establish that the window exists, not how
long it is or what closes it.

### `E8` was the experiment's error, not the database's

The historical TSV asserted `+0x448 == 81` unconditionally. **The contract does not say that.** It says
`+0x448` is *"unset until `001DF240`"* (§4) and that `valueTableCount == 81` **"whenever the tables
are initialised"** (§4). Observed **0** early and **`0x69705F70`** at 30 s — the latter is the ASCII
bytes `p_pi`, which is text, not a count.

> **The expectation was written stronger than the claim it was testing.** The correct disposition
> is to fix the expectation, not the contract — and to leave *what `+0x448` holds at these moments*
> **unresolved**, because two non-81 readings prove the row is not a count then and prove nothing
> about whether it is ever 81. `EO-1`.

**Later resolution and check correction (2026-09-11).** The quotation above records the initial
disposition, now superseded by the [contract's initialization analysis](../19-Save-Load-Settings/Game-Settings-Config/CONTRACT-game-setting-config.md#4a-initialisation-extent--what-construction-leaves-undefined).
Construction zeroes only `+0x07C..+0x447`; `+0x448` is uninitialised heap until `001DF240` writes
`81` at `001DF2A0`. Non-81 startup bytes therefore do not refute the field's later count role.
The current TSV changes E8's expectation to `*`, because this experiment's readiness check does
not prove that writer has executed. A readable E8 row is now an observation, not validation of
`valueTableCount == 81`; a future post-writer test must establish that boundary before asserting 81.

The original TSV is retained in Git at `e1fc2df`; the raw 2026-09-08 captures and their E8 failures
are unchanged. They are not rerun or relabeled as passes. This is propagation of the existing
initialization correction, not new runtime evidence. [EXP-041](EXP-041-config-pointer-closure.md)
separately assessed those captures' pointer expressions before this current-TSV change.

### The controlled arm — one line changed, five values moved

The first two runs observed the machine's existing configuration. A third run **changed the input**:
`FrameLimit=60` → `FrameLimit=30` in
`Documents\My Games\FINAL FANTASY XII THE ZODIAC AGE\76561198045890736\GameSetting.ini`, then
relaunched — the settings are read once at startup, so a restart is required.

| row | `FrameLimit=60` | `FrameLimit=30` | contract's prediction |
|---|---:|---:|---|
| `E1` `setting[18]` | **1** | **0** | 1 / 0 |
| `E2` `0x01DFE0B4` time base | **2** | **1** | 2 / 1 |
| `E3` `0x01DFE0B8` scale | **2.0** | **1.0** | 2.0 / 1.0 |
| `E4` `0x01DFE0BC` inverse | **0.5** | **1.0** | 0.5 / 1.0 |
| `E5` `0x01F82E38` 60 Hz gate | **1** | **0** | 1 / 0 |
| `E9` Language *(not varied)* | 1 | 1 | — |
| `E10` Quality *(not varied)* | 3 | 3 | — |
| `E11` Shadow *(not varied)* | 2 | 2 | — |
| `E12` DecideButton *(not varied)* | 1 | 1 | — |

> **Every predicted value flipped, and every unrelated field held still.** One input varied; five
> outputs moved together in the predicted direction; four control fields did not move. That is the
> difference between *these values co-occur* and **`FrameLimit` drives the time base**.

**The reference environment was restored and the restoration verified**: the settings file was
hashed before the change (`36A6BE8D…0EEB`), rewritten, and after the run restored from that copy and
**re-hashed to the same value**. Charter-directive §13 — record, isolate, restore, verify.

### The installed file is being read — `DH-6` answered

The live values match the **account-scoped** file, field by field, under the contract's own
encodings:

| `GameSetting.ini` | field | live | contract's encoding |
|---|---|---:|---|
| `FrameLimit=60` | `+0x48` | 1 | boolean-reduced; only exactly `1` counts |
| `Quality=VQ_CUSTOM` | `+0x0C` | 3 | *"`001DE4F0` with `quality == 3` (`VQ_CUSTOM`)"* |
| `Shadow=High` | `+0x1C` | 2 | LOW `0`, MEDIUM `1`, HIGH `2` |
| `DecideButton=Cross` | `+0x64` | 1 | `0` = Circle, `1` = Cross |

> **There are three `GameSetting.ini` files on this machine and the game reads exactly one.** The
> unscoped `…\FINAL FANTASY XII THE ZODIAC AGE\GameSetting.ini` says `FrameLimit=30`,
> `Quality=VQ_MEDIUM`, `Shadow=Medium`, `DecideButton=Circle` — **none of which the process held.**
> The Steam-ID-scoped file matched on all four, and it is the one the game rewrote on exit
> (mtime moved during these runs). `DH-6`: **the installed ini is read, and it is the account-scoped
> one.**

## Interpretation

**`GameSettingConfig`'s `FrameLimit` chain is runtime-validated.** The four values the contract ties
together were observed together, in a clean process, with a control proving the read path. This is
the first claim in this database to be confirmed against a running game rather than against the
bytes it was derived from.

**And a third run changed the input**, which turns co-occurrence into causation: one edited line
moved all five predicted values and left four control fields untouched. The contract's
`FrameLimit drives the time base` claim was `PROVEN` from a static read of the chain; it is now
**also** proven against the running game, by intervention rather than observation.

## Confidence

| claim | confidence | why |
|---|---|---|
| the module loads at `ImageBase`, so database VAs are runtime addresses | **PROVEN** | control 1, both runs |
| the read path is sound | **PROVEN** | control 2, `LUAC_TAIL`, both runs |
| `setting[18] == 1` co-occurs with time base `2`, scales `2.0`/`0.5`, gate `1` | **PROVEN** | observed together, run 2 |
| `FrameLimit` *causes* the time base | **PROVEN** | A/B: one input varied, five outputs moved as predicted, four controls held |
| the installed account-scoped ini is what the process reads | **PROVEN** | four fields match its values under the contract's encodings; the unscoped file matches none. `DH-6` |
| the settings hold `FrameLimit` before the time base switches | **PROBABLE** | run 1 vs run 2; the window exists, its length is unmeasured |
| `+0x448` is `81` | **CONDITIONAL; not established in these captures** | 81 only after `001DF240`; construction leaves it uninitialised (contract §4a). The original three non-81 observations remain unchanged; current E8 is observational. |

## Follow-up

- If the biconditional holds, `GameSettingConfig` advances from `CONTRACT READY` to
  **`RUNTIME VALIDATED`**, and the four candidate systems get a template for cheap confirmation.
- If it fails, the failure is **evidence that the static reading is wrong**, and the contract, the
  type store and `DH-1`/`DH-2` are all corrected from the binary — not the observation explained away.
- `E10`/`E11` together test the **`VQ_LOW` / `VQ_MEDIUM` startup mismatch** recorded in the contract
  §10: if `Quality` reads `1` while `Shadow` reads `0`, the mismatch is real and observable, which
  would answer `AX-6`/`AX-6a` from the runtime side.
- `E6`/`E7` distinguish "loaded from file" from "created from defaults" and would settle whether the
  installed `GameSetting.ini` is being read at all (`DH-6`).

## Reproduction

```
ffxii_runtime.py run EXP-001-gamesetting-frametimebase.tsv \
    --ready-ptr 0x01F82D20 --timeout 300 --settle 30
```

For the controlled arm, edit `FrameLimit` in the account-scoped `GameSetting.ini`, hash it first,
run the same command, then restore from the hashed copy and re-hash to confirm.

Raw evidence, with build hash, environment, live module list and both passes:
[`evidence/`](evidence/) — tracked, not in the gitignored `Tools/work/`.

> **Observed limitation, not yet explained.** In run 2 the game **exited on its own between 30 s and
> 60 s after readiness**, with Steam running; passes 2 and 3 found no process and the harness
> refused to report rather than inventing values. So the usable observation window on this machine
> is currently **bounded and short**, which every future experiment must design around. `EO-2`.

## What this experiment cannot settle

Whether the *shipped* installation's ini says 30 or 60 — that is a property of the file on disk, not
of the process, and reading the file directly answers it more cheaply. And nothing here observes the
**thirteen `0x01F82E38` readers** (`DH-3`) actually branching; the gate's value is visible, its
consumers' behaviour is not.
