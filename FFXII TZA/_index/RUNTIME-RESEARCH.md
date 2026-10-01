---
system: Autonomous runtime research — the operating model, the harness, and what it cannot do yet
category: _index
status: PARTIAL
owner_layer: none — this is project methodology, not a game subsystem
evidence_tier: 1
level: L1
readiness: IMPLEMENTED
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-08
falsification_passes: 0
audit:
  passes: 0
  crossref_clean: false
  reopened_count: 0
---

# Autonomous runtime research — the operating model, the harness, and what it cannot do yet

## 1. The change

**`"needs runtime observation"` no longer means `"wait for the operator to play FFXII"`.**

It means the running game is an evidence source this project drives itself: resolve a clean
reference install, launch it, wait for its own controls to pass, observe, capture, close. Manual
gameplay is the **fallback**, used only when a state genuinely cannot be reached any other way —
and when it is used, everything around it is still automated.

**This is an extension, not a relaxation.** Every existing standard applies unchanged: banned
evidence, positive controls, denominators, honest unknowns, provenance. **Automation does not lower
the evidence bar** — it raises the cost of sloppiness, because a harness can produce a hundred
confident wrong numbers in the time a person produces one.

## 2. Capability audit — what already existed

| capability | where | state before this block |
|---|---|---|
| attach to a live `FFXII_TZA.exe` | `runtime_probe.py` | **present** |
| base control — module at `ImageBase 0x00120000` | `runtime_probe.py` | **present** |
| read control — `LUAC_TAIL` at `0x01CCD300` | `runtime_probe.py` | **present** |
| typed field dump driven by `_types/` | `runtime_probe.py --type` | **present** |
| declarative check lists | `runtime_probe.py --check <tsv>` | **present** |
| experiment record format | charter §15, `_experiments/` | **present** |
| live memory read/write, scans, pointer chains | Cheat Engine MCP | present, registered in `.mcp.json` |
| breakpoints, watchpoints, tracing, call stacks | Ghidra debugger MCP | present, needs its debugger process up |
| in-process instrumentation | `XIIOnlineNet.dll` | present — **and disqualifying as a reference** |
| log hygiene, live-log reset | `Collaboration/tools/Reset-LiveLogs.ps1` | present |
| **find and verify a reference install** | — | **missing** |
| **launch / wait-for-ready / close** | — | **missing** |
| **prove the process is uncontaminated** | — | **missing** |
| **capture evidence with provenance** | — | **missing** |

> **The gap was never "how do we read the game" — it was "how do we get a trustworthy one running".**
> One designed experiment (`EXP-001`) sat unrun for months of blocks because of exactly that.

## 3. The reference environment, and why it is not the modding install

Two copies of the certified build exist on this machine and they are **not interchangeable**:

| install | build hash | verdict |
|---|---|---|
| `D:\SteamLibrary\…\FINAL FANTASY XII THE ZODIAC AGE\x64` | authority match | **CLEAN** — loaders renamed `.modbak`, no `modules\`, no `hook.ini` |
| `D:\FFXII MP Mod\FFXII_TestClient1\x64` | authority match | rejected — 4 loaders, 11-file `modules\`, `hook.ini` |
| `…\FFXII_TestClient2\x64` | authority match | rejected — 4 loaders, 10-file `modules\`, `hook.ini` |
| `…\FFXII_TestClient3\x64` | authority match | rejected — `xinput1_3.dll`, 1-file `modules\` |

**All four executables hash to the authority SHA-256 and three of them are still invalid
references**, because `XIIOnlineNet.dll` writes engine state — which `EXP-001`'s own control
variables forbid. **A matching hash is a build control, not an environment control.**

`ffxii_runtime.py env` prints the verdict for every candidate **with its reason**, so a rejection is
legible rather than a silent absence.

## 4. Four controls, all mandatory before any number is reported

1. **Build control** — the executable's SHA-256 equals the authority hash.
2. **Environment control** — an **allowlist** of the 13 files the game ships, no `modules\`, no
   `hook.ini`, **and no Steam launch-option wrapper**.
3. **Process control** — the **complete** live module list is captured as evidence; watched
   instrumentation modules are called out by name.
4. **Read control** — inherited from `runtime_probe`: module at `ImageBase`, and a known `.rdata`
   constant reading back exactly. Without it a failing read returning zeroes is indistinguishable
   from a field that is genuinely zero.

> ### CORRECTED 2026-09-08 — control 2 was a blocklist, and it missed the real contaminant
>
> It read *"no loader DLL, `modules\` or `hook.ini` on disk, and no mod module in the live module
> list"*. That is a blocklist, and it could not see what was actually there: FFXII's **Steam launch
> options** were set to `drrun.exe -c dr_spawn_trace.dll -- %command%`, so **every Steam launch ran
> the game under DynamoRIO**. Nothing in the game's directory says so, and **reinstalling the game
> does not clear it** — the wrapper lives in Steam's user config.
>
> The same blocklist also produced a **false positive** on `xinput1_3.dll`, which a verified
> reinstall proved the game ships.
>
> **A blocklist answers *"is this one of the contaminants I already know?"*. An allowlist answers
> *"is anything here that should not be?"*** — and only the second question is safe. The
> launch-options reader then shipped **broken**, returning empty for a fixture that plainly
> contained the wrapper; `ffxii_runtime.py self-test` exists because an empty result from a broken
> check is indistinguishable from a clean machine. `EP-1`.

**The harness fails closed.** No clean environment → it refuses to launch. A contaminated process →
it refuses to report. A control row fails → every non-control row is voided. **A harness that
reports numbers from an unverified process manufactures evidence.**

## 5. The loop, as it actually ran

```text
resolve + verify environment
        ↓
launch FFXII_TZA.exe
        ↓
wait until THE HARNESS'S OWN CONTROLS PASS   (not "a window appeared")
        ↓
optionally wait for a named singleton to be non-null
        ↓
settle, then observe -- one or more passes, timestamped from ready
        ↓
write evidence JSON: build hash, environment, live modules, every pass verbatim
        ↓
close, and verify exit
```

Timing is a first-class control, and **it had to be**: see §7.

## 6. What is not automated yet

- [x] **Detecting which state the game is in** — `ffxii_runtime.py state`, keyed on the
      script-entity free list: all 128 slots chained means no map is loaded. Baselines from
      `EXP-002`/`EXP-003`.
- [ ] **Establishing a game state beyond startup.** No save loading and no scripted navigation.
      Input automation was **attempted and is negative**: the window focuses, and scan-code
      `SendInput` over five candidate confirm keys changed nothing. **It is not diagnosable**,
      because the observable separates *title* from *map loaded* and a menu cursor moves between
      them invisibly. `ES-1`, blocked on `ET-1`.
- [x] **State snapshot and diff** — `snapshot` / `diff` / `churn`. 8,454,144 bytes in 0.66 s,
      page-chunked with unreadable pages counted. It carries **two controls**: the game's own
      background churn (7,818 bytes per 3 s at the title screen) and the subtraction's **noise
      floor** (~240–320 bytes window-to-window), and it prints a **symmetry check** — a real effect
      is one-directional, noise is not. `ET-1`, `EXP-004`.
- [ ] **Breakpoints, watchpoints and call tracing.** The MCP servers can do this; the harness does
      not drive them, so *"who wrote this field, and from where"* is still manual.
- [ ] **Typed runtime inspection wired to experiments.** `runtime_probe --type` exists and no
      experiment format uses it.
- [ ] **Original-vs-reconstruction comparison.** The six differential pilots still compare against
      shipped bytes under emulation, not against a live process. `INTEGRATION` parity remains
      `NOT COVERED` for all six.

**Nothing above is claimed as working. Each is the honest next capability**, in roughly the order
its leverage justifies.

## 7. The first run, and the lesson it taught immediately

`EXP-001` ran twice on 2026-09-08.

- **Run 1**, observing at the first readable instant, produced what looked like a **live
  falsification** of a contract claim labelled `PROVEN`.
- **Run 2**, observing 30 seconds after the same readiness gate, **confirmed the claim exactly.**

> **The first autonomous experiment this project ever ran would have published a wrong result.**
> The cause was that "the object exists" is not "the writer has run", and the fix — `--settle` and
> `--repeat` — is now part of the harness. **Every runtime conclusion must state when it was
> observed relative to a named readiness condition.**

It also produced a genuine finding no static reading could: **the settings object holds
`FrameLimit` before the engine switches its time base**, so the two are not applied atomically.

## 8. Manual gameplay is the fallback, and this is the test

Ask, in order:

```text
can the harness reach this state?              -> run it
can a deterministic input sequence reach it?   -> automate that
can a known save reach it?                     -> load it
can a validated native operation reach it?     -> exercise it, and RECORD that it was induced
                                                  rather than naturally reached
otherwise                                      -> name the missing capability, and build it
only then                                      -> ask the operator, for the irreducible steps only
```

**A "requires the operator" status must now say what automation cannot do and why.** The operator is
never asked to read memory, copy an address, compare a structure, drive a debugger or transcribe a
log — tooling does all of that.

> ### 2026-09-08 — the fallback was reached for one step too early, and it cost four negatives
>
> `EXP-005` ended by naming *“one genuinely irreducible manual step — the operator holds a
> key while the harness polls.”* **It was not irreducible.** The operating system can hold
> the key (`SendInput`) and the harness can hold the foreground (`window_focus.py`).
>
> Worse, the missing capability was **the reason the earlier answers were wrong**. Windows
> delivers keyboard input to the foreground window, and every measurement in `EXP-004` and
> `EXP-005` was taken with the harness in front. Same instrument, same keys:
>
> | | NEW bytes | the REVERSAL |
> |---|---:|---:|
> | unfocused | 319 | 311 |
> | focused | **17,584** | **31** |
>
> **The rule earns its keep here.** *“Name the missing capability and build it”* sits one line
> above *“ask the operator”* for exactly this reason. [`EXP-006`](../_experiments/EXP-006-the-array-is-written-on-transition.md).

## 8b. Two more tools, and a blocker that closes one route

| tool | what it does | why it is separate |
|---|---|---|
| `window_focus.py` | takes the game's foreground **and verifies it with `GetForegroundWindow`** | `SetForegroundWindow` fails **silently** for a process that does not own the foreground. A probe that assumes it worked measures its own terminal and reports a confident negative |
| `runtime_input_probe.py` | presses real keys, polls the input array, re-checks focus every poll | it is **read-only on the game** — there is no write path in the file. The writing tool stays `runtime_poke.py` |

> **`runtime_input_probe.py` runs its own controls.** A no-key polling window of the same
> length sets the noise floor and disqualifies any index that moves in it; focus losses are
> counted per poll rather than averaged away. It **refuses to run** if the array is not clean
> at rest or if it cannot take the foreground, because either would make every result
> ambiguous.

### The blocker: a dbgeng attach freezes the game (`EW-2`)

```text
attach   -> 99 modules, state "stopped"
continue -> state "running"
measure  -> 0.000 CPU seconds over 2.0 s wall   (control process: 1.984)
detach   -> 0.391 CPU seconds over 2.0 s wall   -- it resumes
```

**Breakpoints, watchpoints and function traces are unusable through this server**, and a trace
reporting zero hits is reporting a frozen process, not a quiet one. The address map itself is
fixable — `POST /debugger/sync_modules` with `{"FFXII_TZA": "0x120000"}` populates it, because
`DYNAMIC_BASE` is clear and the Ghidra base **is** the runtime base — but that only gets as far
as installing a trace that cannot run.

> **A control on the instrument is what caught this.** The target trace reported 0 hits; so did
> a control trace on a hot function. Two zeroes meant *the instrument*, not *the game* — and
> CPU time, with a positive control that burned 1.984 s, said which.

## 8c. Sight — and the verdict it corrected

| tool | what it does |
|---|---|
| `window_capture.py` | photographs the game window; tries `PrintWindow`, falls back to a screen `BitBlt`, and **reports which path worked and how close to one flat colour the result is** |

**A Direct3D swap chain does not draw itself through GDI**: `PrintWindow` came back 93.8 %
black at the main menu. A capture tool that cannot tell *“the screen is black”* from *“the
capture failed”* manufactures confident negatives, so this one reports both.

> **Declare DPI awareness before asking for any window rectangle.** The first run photographed
> a neighbouring window: a DPI-unaware process is handed **logical** coordinates while the
> screen DC is in **physical** pixels. The game window is **1938 × 1089**, not the 1292 × 726
> every earlier tool recorded.

### It immediately caught the harness lying to itself

`state` reported `TITLE` while **Vaan was rendered on screen**. `0215FDA0` is the **script
VM's** entity-name table, and *“on the free list”* and *“has content”* are independent — with a
map loaded all 128 records are still linked **and** all 128 carry a body. The verdict now
reads the save buffer and the area id, and **refuses to name a screen**:

```text
just launched   area id  -1   save buffer empty       -> UNKNOWN
front-end       area id  12   save buffer empty       -> MENU
save loaded     area id 227   save buffer populated   -> IN-WORLD
```

**Every state verdict this harness prints is now falsifiable by a photograph**, which is the
property it lacked. [`EXP-007`](../_experiments/EXP-007-navigating-the-front-end.md).

## 8d. Breakpoints, at last — and the one thing they cost

`EW-2` blocked every causality experiment: the dbgeng-based MCP server **froze the game**,
and a trace reporting zero hits was reporting a frozen process rather than a quiet one.
**The fix was to stop debugging someone else's engine** and drive the Win32 debug API
directly.

`hwbp.py` uses **hardware** breakpoints — the DR registers of every thread — so **no code
byte is modified**. An `INT3` patch would be a write into the reference environment; a debug
register is not, and it also survives any code the game checksums.

```text
target CPU while attached : 5.062 s over 6.0 s wall   IT KEPT RUNNING
threads armed             : 105
control 0020E600          : 133,679 hits, with arguments
```

**It refuses to let a negative stand alone.** `--control <addr>` arms a second breakpoint on
a function that must be called; if the control does not fire, the run says the instrument is
unproven and that a zero on the target means nothing. It also samples the target's **CPU
time** before, during and after, so a run that froze the game is reported as frozen rather
than as quiet — which is exactly the failure `EW-2` was.

### RETRACTED 2026-09-08 — it was never the attach, and the negative it produced was false

The section below said *attaching* disabled input permanently. The historical control
contradicted that conclusion in its tested state: input stayed at **3 of 3** before,
during and after. **Correction 2026-09-10:** this control arms no breakpoints but still
clears thread DR0–DR3/DR6/DR7 with `SetThreadContext`; it is not an event-loop-only control.

| run | breakpoints armed | input | `003EAA70` hits |
|---|---|---|---:|
| `--no-arm` | none (DR registers still cleared) | **3 of 3** | — |
| cold | `003EAA70` alone, at the front-end | **3 of 3** | 0 |
| hot | `0020E600` alone (255,944 hits / 12 s) | **0 of 3** | — |
| three at once, in-world | `003EAA70` + `00265270` + `0020E600` | not measured | **0** |
| **alone, in-world** | **`003EAA70` only** | worked during navigation | **1,130,002** |

These runs demonstrate a hit-rate effect, not the cause of every stall. Later loaded-state
armed failures include a bounded 60-hit run (PROGRAM-STATE §4bk). The matched loaded-save
[EXP-010 control](../_experiments/EXP-010-loaded-state-no-arm.md) now survives 30 seconds of
no-arm and a 45-second visual follow-up in area 227, with before/during/after input,
repeated CPU windows, unchanged live code and externally verified detach. Narrow the next
test to bounded armed capture; do not generalize survival to every state or instrument.
EXP-010's full receipts include Steam/NVIDIA/Discord overlay modules in every window. The
wrapper's watched-module `clean` verdict does not establish an overlay-free process; the result
is restricted to the recorded environment despite matching live game code.

> ### And this retracts a finding, not just an explanation
>
> The previous block recorded *“field music is not selected per frame — 0 hits in-world
> beside a control firing 127,578 times”*. **That measurement had two hot breakpoints armed
> beside the target.** Armed **alone** in the same state, `003EAA70` fires **1,130,002 times
> in 75 seconds**.
>
> **A hot breakpoint does not merely slow the program down; it changes which of its code
> runs.** The control fired, so the instrument was “proven” — and the negative was still an
> artifact. **A positive control proves the instrument can see. It does not prove the
> instrument left the program alone.**

### Superseded text follows

### The cost: attaching makes the game deaf

Measured with the game's own keypress counter, three presses per sample:

```text
BEFORE attach        3 of 3 presses counted
DURING the session   0 of 3
AFTER detach         0 of 3
```

**It is the attach, not the detach, and it does not recover.** The game runs normally
throughout — 6.7 CPU seconds over 8.1 s wall, control firing 127,578 times. **Alive,
rendering, and deaf.**

> ### The operating rule
>
> **Establish the state first. Attach second. The state cannot be changed afterwards.**
> Any experiment needing a keypress *while* tracing is not possible through this tool, and
> the game must be relaunched before input-driven work. **Why is not established** —
> alive-but-deaf fits an anti-tamper response and an OS input-queue effect equally, and
> nothing here separates them. `EW-7`.

### The first two measurements it made

> **Historical timing conclusion superseded 2026-09-10:** the count/zero evidence below
> does not establish caller scheduling. See the dated correction in §8e and EXP-009.


| target | state | hits in 8 s | with a control at |
|---|---|---:|---|
| `003EAA70` `FieldMusic_Select` | front-end | **0** | 133,679 |
| `003EAA70` `FieldMusic_Select` | **in-world, save loaded** | **0** | 127,578 |
| `00265270` `FieldData_GetVariable0` | in-world | **114,204** | 127,578 |

**Field music is not selected per frame.** Standing in Dalmasca Estersand for eight seconds
with a proven-positive instrument, `FieldMusic_Select` is **never called** — so it is
event-driven, presumably on a field change. That is a behavioural fact no static reading
gives you, and it is a **real** negative because the control fired 127,578 times beside it.

**And `FieldData_GetVariable0` is one of the hottest functions in the game** — 114,204 calls
in eight seconds. `diff_field_music.py` stubs it as the field-music progress source; it is
plainly used far more widely than that.

## 8e. RETRACTION 2026-09-08 — every hit count above was the instrument reporting itself

**A hardware breakpoint re-fires on the instruction it just reported** unless the debugger sets
`EFLAGS.RF` and clears `DR6` before continuing. `hwbp.py` did neither. It looped on a single
address at the speed of the debug-event round trip, and every count it produced is retracted:
**133,679**, **127,578**, **255,944**, **114,204**, **1,130,002**.

```text
60 consecutive recorded hits on 0020E600  ->  1 distinct (thread, rcx, rdx) triple
after the fix, 300 recorded hits          ->  161 distinct triples
```

### And that retracts a retraction

§8d said the finding *“field music is not selected per frame in-world”* was **false**, because
`003EAA70` armed alone during a map load reported 1,130,002 hits. **That reasoning is void.**
The 1.13M was storm-inflated, and the run that produced it **spanned a map load** while the
runs reporting zero did not.

**CORRECTED 2026-09-10:** the original zero-hit records do not prove load-only selection.
The storm correction invalidates inflated counts, but does not validate the zeroes' execution
window or prove that attachment left the relevant caller progressing. The later EXP-009 traces
also lack timestamps and frame/phase counters. Scheduling remains unestablished by these captures;
see [EXP-009's correction](../_experiments/EXP-009-the-games-own-answer.md#corrected-2026-09-10--timing-and-observer-effect-conclusions-withdrawn).

> **Three guards passed and the number was still wrong.** The instrument had a positive control
> that fired, it was run with the target alone, and it reported its own load. [`EVIDENCE-STANDARD.md`](EVIDENCE-STANDARD.md)
> now carries a second amendment: **show that repeated events are distinct** before writing a
> count down.

### Two more bugs found on the way to fixing the first

| bug | how it showed |
|---|---|
| writing a full thread context on **every** debug event, not just the trapping thread's trap | the target's CPU fell to **0.062 s over 8.1 s wall** and it stopped responding |
| the CPU liveness check used an **absolute** threshold | a `--stop-after` run finishing in 0.1 s wall was reported **FROZEN**; it is now a rate |

**What was not completed:** re-measuring `003EAA70` in-world with the **fixed** tool. The
navigation could not be re-established after the tool runs, and no measurement is claimed that
was not taken.

## 9. What is deliberately not claimed

- [ ] **That the harness makes any pilot parity-certifiable.** It does not yet observe the original
      game *through the caller the game uses*, which is what `INTEGRATION` requires.
- [ ] **That the reference session is stable.** It is not — it **crashes**, and the crash survived
      a clean reinstall *and* the removal of the DynamoRIO wrapper, on **both** launch routes:
      `0xC0000005`, a **read** access violation at **`003845F0 + 0x10`**
      (`AreaData_BindAndRebaseSectionDescriptor`, 252 B, `WorldAreaField`), dereferencing
      `[rdx+0xC]` with **`rdx = 0xFFFFFFFF82AD88C0`** — a sign-extended 32-bit offset used as a
      pointer, inside the function that exists to rebase such offsets. **What supplies it is not
      established**, and the wrapper is excluded as the cause. `EO-2`.
- [ ] **That a clean directory guarantees a clean process.** It does not — and the module check has
      still never fired on a real contamination, so it stays unproven in the direction that
      matters. What *is* proven is the launch-options reader, by a four-case self-test, **because
      that one shipped broken.**
- [ ] **That the earlier `EXP-001` runs were uncontaminated.** They almost certainly were — a
      direct launch does not pick up Steam launch options — but those runs recorded blocklist
      misses rather than the module list, so it is **not establishable from the evidence**. `EP-1`.

## 9a. Contract §13 audited against the experiment corpus, both directions — 2026-09-13 (OPUS)

`OPUS-CONTRACT-RUNTIME-AUDIT` asked one question in two directions: **does any contract claim a
validation its experiment record does not support, and does any experiment record test a contract
that never hears about it?** The answer to the first is **no**, and that is the result worth having.
The answer to the second was **16**, now **0**.

**Instrument:** [`check_contract_runtime_links.py`](../../Tools/analysis-kit/gfz-scripts/check_contract_runtime_links.py),
run over 47 contracts and 82 experiment records. It reads the *declared* `method:` field, never
prose.

### Controls first, because every number here is a property of two extractors

| control | result |
|---|---|
| C1 — the `## 13.` extractor must find the section | **42 of 47** contracts carry one. The five without are named below and are the finding, not a blind spot |
| C2 — the `EXP-0NN` regex must find ids in a record known to carry them | finds `[15, 80]` in `EXP-080` |
| C3 — both directions must actually fire | they did: Direction A raised two `ONE-WAY`s and Direction B raised 16, and Direction B now reads 0 after the repair |

### Direction A — no contract overstates its evidence

**Not one contract claims live validation that its experiment record does not support.** Eight
contracts say *"Live capture: still absent"* in §13 while a `COMPLETE` experiment record names them;
**every one of those records declares method A or B**, so none of them contradicts the statement. The
audit's primary finding is a negative, and it is the one that matters.

`ONE-WAY` is **advisory, not a defect**, and both instances are explained rather than repaired:

- `CONTRACT-save-image-buffers` → `EXP-080`: the link was added to the contract on 2026-09-13; the
  record predates it and declares `contract: none`. One-way by construction.
- `CONTRACT-gameplay-generators` → `EXP-013`: a **methodological precedent** — *"`EXP-013` has already
  demonstrated the harness for exactly this shape"* — not a claim that `EXP-013` tested this contract.

> **My first cut of this check would have called both defects.** A back-reference is owed when a
> contract rests an argument on an experiment, not when it cites one as precedent — the same
> distinction the inbox rules already draw between a passing reference and a load-bearing one. The
> checker now says so in its own docstring, because a rule that lives only in the reviewer is a rule
> that gets re-derived wrongly.

### Direction B — 16 records tested a contract that never cited them; now 0

25 of the 82 records name a contract in frontmatter. **16 of those 25 links were not reflected in the
contract's §13** — 13 absent from the contract file entirely, 3 present but filed under §10 or §15.
All 16 are now cited in §13 of the 11 contracts concerned, each **with its declared method spelled
out** and an explicit line that an A/B record does not move the evidence class.

### What the audit found that it was not looking for

1. **Five contracts have no §13 at all** — `CONTRACT-efx-source-rebase`, `CONTRACT-resource-entry-tree`,
   `CONTRACT-authored-command-ramp-channels`, `CONTRACT-save-container-transform`,
   `CONTRACT-storage-read-completion`. A contract with no runtime-validation section cannot be audited
   in either direction, so these are invisible to the check rather than passing it.
2. **The corpus is weakly linked in both directions.** Of 47 contracts, **9 cite any experiment
   anywhere in the file**; of 82 records, 25 name a contract, 39 say `contract: none` and **18 have no
   `contract:` field at all**.
3. **`method:` is a mid-era convention.** Only **39 of 82** records declare it — present through
   `EXP-037`–`EXP-074`, absent from `EXP-001`–`EXP-036` and from `EXP-075` onward. The Direction-A
   negative above is sound only because all thirteen unlinked records fall inside the declaring range;
   **it could not have been established for the early live experiments from frontmatter alone.**
4. **Exactly one record in the corpus declares `live_game: true`** (`EXP-082`). 38 declare `false` and
   43 omit the field. The corpus cannot currently answer *"which contracts have live evidence"* by
   query, which is precisely what a readiness gate needs to ask.

> **A methodological note on how nearly this went wrong.** My first classifier guessed live-vs-isolated
> from keywords in the prose and labelled `EXP-041` **LIVE**. The record declares `live_game: false` in
> its own frontmatter. **The field was already there and I was inferring around it** — and had I not
> checked, the audit would have reported a contract claiming "live capture absent" while a live
> experiment tested it, which is exactly the false defect this audit exists to avoid raising.

### Routed, not closed

Items 1–4 are corpus-schema gaps, not contract defects, and none is repaired here. They are the
prerequisite for making *"which contracts have live evidence"* a query rather than a reading, and
that belongs to the readiness gate rather than to any one contract.

### §9a corrected the next day, on two of its own four findings — 2026-09-13 (OPUS)

**Finding 1 was true and its implication was false.** §9a said *"five contracts have no §13 at all …
so these are invisible to the check rather than passing it."* The fact is right; the conclusion is
not. All five — `CONTRACT-efx-source-rebase`, `CONTRACT-resource-entry-tree`,
`CONTRACT-authored-command-ramp-channels`, `CONTRACT-save-container-transform`,
`CONTRACT-storage-read-completion` — use a **short-form contract template**: a handful of numbered
mechanism sections, a section named *"What this contract does not establish"*, and §15 Evidence.
**Their runtime statement is named rather than numbered**, and they were invisible to my checker, not
to auditing. *A missing section number is not a missing section.*

`check_contract_runtime_links.py` now resolves the short form, and its control reads
**47/47 contracts expose a runtime-validation section (42 numbered 13, 5 short-form)** — up from
42/47. Nothing about the Direction-A or Direction-B results changes; the five carried no experiment
citation either way.

**Finding 3 was much worse than the corpus deserves.** §9a said `method:` is declared by only 39 of 82
records and called it *"a mid-era convention"*. Measured by contiguous run rather than by count:

| records | `method:` |
|---|---|
| `EXP-001` – `EXP-036` | absent — **they predate the convention** |
| `EXP-037` – `EXP-074` | **present, unbroken, 38 records** |
| `EXP-075` – `EXP-081` | **absent — a seven-record lapse** |
| `EXP-082` | **present again** |

**The convention was not abandoned. It lapsed for seven records and has already resumed.** So the
distance between the audit's Direction-A negative and a queryable *"which contracts have live
evidence"* is **seven records**, not forty-three — and those seven have authors who know the answer,
which is why they are routed rather than inferred. `EXP-001`–`036` predate the schema and are a
separate, larger decision that should not be made by backfilling.

> **I did not backfill any of them**, and the reason is the retraction two entries above: inferring a
> method from prose is exactly what put `EXP-041` in the wrong column earlier today. **A field whose
> author did not declare it is undeclared, not derivable.**

## 9b. "Which contracts have live evidence" answers **1**, and the answer is an artefact — 2026-09-13 (OPUS)

`OPUS-EXP-CORPUS-SCHEMA` exists to make that question a **query** rather than a reading. It now is
one — [`check_experiment_schema.py`](../../Tools/analysis-kit/gfz-scripts/check_experiment_schema.py)
runs it over all 82 records — and the first run returns **one contract**:
`CONTRACT-authored-table-row-lookup.md`.

**That number is false, and it is false by construction.** The query reads `live_game:`, and
**35 of the 82 records do not have the field**:

| population | `method:` / `live_game:` | who |
|---|---|---|
| `EXP-037`..`074` | present, 38 records | recovered by ASTRA, `experiment-metadata-recovery` |
| `EXP-075`..`081` | present, 7 records | recovered 2026-09-13 by OPUS from each record's own body |
| **`EXP-001`..`036`** | **absent, 35 records** | **never recovered — the recovery instrument's population started at 037** |

**The missing 35 are not the quiet ones.** They are where the live work is. **Thirteen name a PID in
their own text** — `EXP-003`, `010`, `015`, `016`, `018`, `019`, `023`, `024`, `025`, `026`, `027`,
`028`, `029` — and five more assert a live reading without naming one: `EXP-001` (*the first genuinely
live one*, by `PROGRAM-STATE`'s own account), `004`, `005`, `008` (*"read out of the running game"*)
and `009` (*"the running game as the oracle"*). **Eighteen of the thirty-five, counted rather than
estimated, and every one of them is invisible to the query.**

> **An absent field is not a neutral blank.** Any filter that treats absence as the default reads
> `live_game:` missing as **false**, so an unlabelled live record does not merely go uncounted — it is
> counted on the wrong side. That is the same shape as every other finding in today's sweep: the
> instrument was clean where it measured, and the population it did not measure was the interesting
> one.

**What is NOT being fixed by this section, deliberately.** Labelling the 35 needs a vocabulary value
that does not exist. The established words are `A` (offline preparation, retained-evidence assessment,
offline tool reproduction), `B` (isolated original-code execution) and `C` (**ordinary UI input and
read-only process observation**). `EXP-009`, `010`, `015`, `016` and `017` are none of those: they set
**hardware breakpoints**, armed and disarmed them, and attached a debugger. That is not read-only
observation and it is not isolated execution, and inventing a fourth letter across 35 of another
agent's records, while that agent is in a usage window, is exactly the unsupported bulk disposition
this role is supposed to refuse. **One question is routed for ASTRA's return; the census, the gate and
the finding do not wait on it.**

## 9c. The schema closed on two keys, and the third is declined in writing — 2026-09-13 (OPUS)

[§9b](#9b-which-contracts-have-live-evidence-answers-1-and-the-answer-is-an-artefact--2026-09-13-opus)
recorded that *"which contracts have live evidence"* answered **1**, and that the answer was an
artefact of 35 records carrying no `live_game:` at all. Those 35 are labelled and the query now
answers **4**.

| key | before | after |
|---|---|---|
| `method:` | 47 of 82 | **82 of 82** — A 12, B 41, C 28, native-instrument 1 |
| `live_game:` | 47 of 82 | **82 of 82** — true 28, false 54 |
| `contract:` | 64 of 82 | **70 of 82** — and the remaining 12 are declined below |

**The unblocking ruling was ASTRA's**, given before its usage window closed
(`OPUS-REQ-ASTRA-METHOD-VOCAB-FOURTH`): *"C includes observing the actual running FF12 with
breakpoints/watchpoints/debugger instrumentation… No fourth game-evidence method is needed… Missing
`live_game` means unknown, never default false… OPUS/SWE2 can classify from primary published bodies
while ASTRA is unavailable."* Every one of the 35 was then classified from a sentence in its **own
body**, with the matched line receipted in
[`EXP-001-036-method-receipt.json`](../_experiments/evidence/experiment-metadata-recovery/EXP-001-036-method-receipt.json).

### The twelve `contract:` rows are DECLINED, not forgotten

Six of the eighteen were declared `none` on a **checkable** basis: they are Method A tooling records —
a checker, an extractor, a ledger instrument, two preparations and a census — that execute no
shipping game code, and a both-directions check confirms they name no contract and no contract names
them.

**The other twelve are live game-behaviour records, and assigning their contracts is a per-record
judgement rather than a lookup.** `EXP-023` camera input, `EXP-027` an ordinary kill, `EXP-030` a
deadline integration: each *could* bear on a contract nobody has linked yet, and the bidirectional
check proves only that no link exists **today**, not that none should. ASTRA made exactly this call
by hand for `EXP-037`..`074`, one record at a time, with a written reason each — *"No existing
contract specifies linked-list loot selection `00319850`; experience and licence award is a different
operation."* That is the standard, and pattern-matching twelve records to `none` would not meet it.

> **So they stay unset and this is the declined change, with its reason.** `OPUS-EXP-CORPUS-SCHEMA`'s
> completion condition allows exactly that — *"or each is recorded as a declined change with its
> reason"* — and an absent `contract:` that is **explained here** is worth more than twelve
> `none`s that were guessed. The records are ASTRA's; the judgement is ASTRA's; the queue for it is
> already open.

## 10. Related

- [`../_experiments/EXP-001-gamesetting-frametimebase.md`](../_experiments/EXP-001-gamesetting-frametimebase.md) — the first autonomous run
- [`PARITY-STATUS.md`](PARITY-STATUS.md) — the dimensions this capability is aimed at
- [`../../../Reconstruction/PARITY-STANDARD.md`](../../../Reconstruction/PARITY-STANDARD.md) — why `INTEGRATION` needs the running game
- [`EVIDENCE-STANDARD.md`](EVIDENCE-STANDARD.md) — the tiers this evidence must still satisfy
