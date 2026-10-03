---
contract: fix the engine's constants before any content loads - seed the generator from a literal, derive the frame-base constant from the frame-limit setting, and allocate the memory budget
category: 00-Engine-Core-Runtime
scope: subsystem
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md
entries: ["0022A0B0", "0022BDF0", "001EDDC0", "00863D30", "0017D8F0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the seeding, the frame-base derivation and the memory budget are the page's reading with
    site citations, including three published corrections. The frame-limit causality is EXP-001's
    LIVE result. OPUS assembled and scoped this contract on 2026-09-20.
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-falsification-1 - the seeds, the reseed callers, the eleven allocations and nine registrations survive; I3's 'evaluated once' is refuted (a setter with an area-transition caller and a script-verb caller)
  by: OPUS
  date: 2026-09-20
---

# Contract — what the engine fixes at boot

> **Provenance, stated once.** **[page]** marks the page's reading. **[EXP-001]** marks a **LIVE**
> controlled A/B experiment — the only live citation in any contract I wrote today, and it is
> scoped to one invariant. **[live]** marks what remains live-only.
>
> **`EXP-071` was considered and declined.** It executes the **procedural** generator's
> initialisation; boot's generator fact is **MT19937** at `00863D30`. Different generator, so it is
> not evidence here.

## 1. Purpose

Before a single asset loads, boot pins down the constants the rest of the engine will assume: how
the random generator starts, what the frame base is, and how much memory each pool gets.

## 2. Interface

| | |
|---|---|
| boot fixer | `0022A0B0` — called from `0017D4C0` **[page]** |
| frame-base selector | `0022BDF0`, tail-calling `001EDDC0` **[page]** |
| generator seed | `00863D30(seed)` via a 5-byte thunk **[page]** |
| the setting | `FrameLimit` in `GameSetting.ini`, read by the 11-byte getter `0017D8F0` **[page]** |

## 3. Types

No type of its own. It writes `DAT_02EB4234` (the generator's first-use latch), `uRam_02064ACC`
(the frame-base constant), `DAT_01DFE0B4` (the frame limit) and nine registered memory pools.

## 4. Preconditions · postconditions · invariants

**I1 — THE GENERATOR IS SEEDED FROM A LITERAL, WITH NO ENTROPY.** On first use `00863D30` seeds with
**`0x1571` = 5489 — the default seed of `std::mt19937`** — then boot re-seeds with **`0x11B9` = 4537**,
a constant in the instruction stream. **No clock read, no entropy source, no player input**
**[page]**.

**I2 — SO THE STREAM IS IDENTICAL ON EVERY LAUNCH, BUT NOT ACROSS A RELOAD — AND THE RESEED IS FROM
THE WALL CLOCK, NOT FROM THE SAVE.** *This is the page's own correction of 2026-09-03, and it is the
interesting half.* `RNG_MT19937_Seed` has **two** callers: boot's constant, and
**`SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG`** at `005843D3`, which calls
`api-ms-win-crt-time-l1-1-0.dll!_time64` and mixes **both halves of the 64-bit clock value** with a
global at `01FD4A80` (`× 600`), clearing the sign bit, before tail-jumping to the same thunk.

> **CORRECTED 2026-09-20 (OPUS). This invariant first read "which reseeds from the save", and that
> was wrong in a way that matters.** *From the save* would mean **loading the same save twice
> yields the same stream**; *from the wall clock* means **it does not**. The conclusion — that the
> stream differs after a load — survives and is in fact stronger, but a reconstruction built from
> my original wording would have keyed the reseed off save data and been deterministic where the
> original is not. Caught while writing S-46's contract, where the same mechanism is stated
> independently.

**"Two players taking the same actions from boot get the same rolls" is true from boot and false
across a reload** **[page]**.

**I3 — THE FRAME-BASE CONSTANT IS AN INTEGER DIVISION, ~~EVALUATED ONCE~~ RE-EVALUATED ON AREA CHANGE AND SETTABLE BY SCRIPT.**
*CORRECTED 2026-09-29 (OPUS, falsification pass 1, `CON-158`): boot computes it first, but it is **not evaluated once**. `02064ACC` has a second writer, the 7-byte setter `00229F10` (`mov [02064ACC], ecx; ret`), and two callers use it. The area transition `002628B0` → `002695A0` recomputes `2 / FrameLimit`. The script verb `mainloopallsyncv` (0x018F, handler `003464B0`) → `0026DB10` stores `arg / FrameLimit`, or `2 / FrameLimit` when the argument is negative. So a script can set the frame-base constant, and every area change restores the default.*
`uRam_02064ACC = 2 / DAT_01DFE0B4`, so it is **2 at 30 fps and 1 at 60**. `0022BDF0` does not write
the frame limit; it computes `(FrameLimit == 1)` and tail-calls `001EDDC0`, **which writes the
triple only on the 60 branch** **[page]**.

**I4 — ELEVEN POOLS ARE ALLOCATED AND NINE ARE REGISTERED**, all before content loads. Registered
total **255.6 MiB**, allocated total **257.1 MiB** **[page]**.

**I5 — the fourth registration argument is a HANDLE-SLOT COUNT, not an alignment.** *Corrected
2026-09-12 (`ASTRA-CONTRA-FABLE-ARENA-SLOT-COUNT`).* Every allocation is its registered size plus a
tail of `+0x10`, `+0x100` or `+0x400`, and the initialiser **aligns everything to 64 bytes by itself
and lays out only `size` bytes** — so ~~**what the extra tail bytes serve is not established**~~
**[page]**.

> **NARROWED 2026-09-21 (FABLE) from execution — the tail is headroom for a ledger that lives at the
> HEAD of the block.** `EXP-142` ran the nine `00369D30` registrations on shipped bytes and recorded
> every write. The registrar's stores span roughly `0` to `0x783C` from the block base — 603 to 6,930
> stores, in proportion to pool size — the first 64 bytes of every registered block come back zeroed,
> and **the last 64 bytes of every allocation are still the fixture's `0xAA` fill**. So the extra
> `0x10` / `0x100` / `0x400` is **not** a region of slot records at the end of the block, which is how
> a static reading of a size-plus-tail allocation naturally reads; it is headroom for a head-resident
> ledger whose extent scales with the pool. **What the tail bytes are *for* is still open** *(answered: see what-the-engine-fixes-at-boot.md, RC-2 answered 2026-09-30; 2026-10-02, OPUS)* — nothing
> observed writes them — but the shape of the answer has changed, and a reimplementation that lays
> records into the tail would be wrong **[EXP-142]**.

## 4a. The archive mount and the startup latch — the two boot operations this contract left out (FABLE, 2026-10-03)

*Added on SWE2-AUDIT-SPEC's L2 expansion (S-01, item 3: the VBF mount `0017CEB0` and the startup latch `+0x113C`
were in no contract). Two provenance tags are new here. **[image]** means read at the bytes of the certified image
(`73461d08…`, base `00120000`), with every caller and every reference taken from a raw index: E8/E9 rel32, 0F 8x rel32,
EB/7x rel8, rip-relative, `[reg+RVA]` and pointer constants. **[exec]** means the original code was run under
Unicorn 2.1.4 by [`check_s01.py`](../_index/candidates/fable-l2exp-s01-mech-1003/check_s01.py) (39 PASS, FAILS 0).
This section adds I6–I9. I1–I5 are unchanged, but I8 says on which thread their code runs.*

**Interface.**

| | |
|---|---|
| the framework's init | `0079F150` (one caller, `0079E5ED`). It calls `GameApplication` vtable `008C5760` slot 2 (`0079F591`), then slot 3 (`0079F69A`), and leaves on the first non-zero return, logging `"App failed during initApplication"` / `"… initScene"` (`0079F598`, `0079F6A1`) **[image]** |
| the archive mount | slot 2 `0017CEB0(this, a, b)`, the framework's *initApplication* **[image]** |
| the mount primitive | `0019B070(ctx, path)` over the mount context `[01F81110]` (ensure `0019B190`, getter `0019B1F0`); the archive open is `001F4340(archive, path)` **[image]** |
| the latch poster | slot 3 `0017CF30`, the framework's *initScene*, which posts the job `{0017D150, this}` **[image]** |
| the latch writer | `0017D000`, reached only as that job (`0017D150` is `jmp 0017D000`) **[image]** |
| the latch readers | slot 4 `0017CCD0` (`0017CCD6`), slot 7 `0017CE50` (`0017CE77`), slot 8 `0017D090` (`0017D094`) **[image]** |

**Cells read and written.** None of these cells is declared in the type store yet. The declarations are routed to SWE2-STRUCT.

- The application is a static object at `01F7E350`, `0x1140` bytes. Its constructor is `0015BC40`, whose only pointer is the
  `.rdata` initialiser slot `008C31F0`. The base constructor it calls at `0015BC40` + 0x14 publishes it to the handle `[02EA5368]`
  (`00792550`), and that handle is how the framework reaches it.
- Slot 2 writes `+0x1130` (qword `a`, `0017CEC2`) and `+0x1138` (dword `b`, `0017CEC9`), and stores the content root
  `"../../.."` into `02CA9D80` through `0059A770`. The pair has three readers:
  - `0017D000` (`0017D012`, `0017D019`), which hands it to `0017D4C0`;
  - the getter `0017D240`, which reads it rip-relative. Its one caller is the FF12CONFIG loader `00408C30`
    (`00408C6A`).

  Nothing in this contract depends on what the pair means.
- `+0x113C` is the latch byte. Its writers are the constructor's word clear `mov word [01F7F48C], 0` (`0015BC68`,
  which clears `+0x113C` and `+0x113D` together) and `0017D000`'s `mov byte [rbx+0x113C], 1` (`0017D074`).
- The job manager is `AsyncJobManager [01F810F8]`. Its ensure is `0019A0A0`, which also creates a second instance at
  `[01F81100]`. The job queue is that object's `+0x50` list, locked at `+0x28`.

**I6 — THE ARCHIVE IS MOUNTED BY SLOT 2, BEFORE SLOT 3 RUNS, AND A FAILED MOUNT IS NOT REPORTED.**
- Slot 2 makes six calls, with no branch (`0017CEDD`–`0017CF11`):
  1. it sets the content root (`0059A770`);
  2. it ensures the mount context (`0019B190`);
  3. it fetches the context (`0019B1F0`);
  4. it mounts `"../FFXII_TZA.vbf"` (`0019B070`, `0017CEF6`);
  5. it calls `0017D6B0`;
  6. it calls `00182F70` with the window size `+0xD24`/`+0xD28`.
- The mount's `al` is never tested. The next instruction is `mov rdx, rbx` (`0017CEFB`).
- Slot 2's only exit returns `xor eax, eax` (`0017CF1B`, `0017CF27`). The framework's `initApplication` failure arm
  (`0079F598`) is therefore unreachable from this override, and init goes on to slot 3 whether or not an archive
  was mounted **[image]**.
- The path is relative. A process whose working directory is not the executable's folder resolves it elsewhere. The
  check resolves it from `x64\` to the shipped archive.

**I7 — AN ARCHIVE IS ACCEPTED ONLY BY ITS MAGIC AND AN MD5 OF ITS HEADER.** `0019B070` takes the first free one of five
context slots (`+0x20..+0x47`, `0019B0A7`), allocates an `0xB0`-byte archive (`0019B0B4`) and calls `001F4340`
(`0019B0E5`). `001F4340` then:
1. `fopen`s the path `"rb"` (`001F43A9`);
2. requires the first dword to be `'SRYK'` (`0x4B595253`, `001F43D7`);
3. reads the header size from offset 4;
4. reads the last 16 bytes of the file (`_fseeki64(-0x10, SEEK_END)`, `001F4424`);
5. reads the header from offset 0 and closes the file (`001F4471`);
6. hashes the header with `CALG_MD5` (`0x8003`, `001F44AB`);
7. requires the 16-byte digest to equal those last 16 bytes (`001F4503`–`001F4535`).

Only then does it build its index, and it returns 1 (`001F4701`).
- **Executed on the shipped archive [exec]:** `001F4340` runs from its entry to the accept point `001F453B`, with
  import stubs doing the real file reads. The header is 11,995,716 bytes with 89,414 entries, and
  MD5 = trailer = `b74187bd5c88f564281dc290ab0ee051`.
- **The same run rejects at `001F4705`** for each of these: one header byte flipped, a wrong magic, and a missing
  file.

**I8 — THE STARTUP LATCH IS SET ON THE ASYNC JOB THREAD, AS THE LAST STORE OF THE INIT JOB, SO I1–I5 RUN ON THAT
THREAD TOO.**
- **Slot 3 sets nothing itself.**
  1. It ensures the `AsyncJobManager` pair. Slot 3 is the only caller of `0019A0A0`, at `0017CF77`. The ensure's
     constructor `001999D0` → `00199F60` starts the thread `"AsyncJobManager Thread"` (proc `0019A190` → `0019A1A0`,
     `CreateThread` at `005CD228`).
  2. It takes a pool node (`0017CF84`) and fills it with `{0017D150, this}` (`0017CF8C`–`0017CF96`).
  3. It enqueues the node (`0019A000`, `0017CFA5`) and returns 0 through `005C5230`.
- **The worker runs the job.** It loops:
  1. `Sleep(5)` (`0019A1D5`);
  2. take the oldest node (`0019A1FF`);
  3. call `fn(arg)` (`0019A24A`).
- **The job is `0017D000`.** It calls, in order:
  1. the init burst `0017D4C0`, which contains this contract's fixer `0022A0B0` (`0017D5CC`);
  2. a `0x80` allocation into `[01F7E340]`, then `0018A840`;
  3. the renderer `00189000`.

  Its last memory write is then `+0x113C = 1` (`0017D074`). Its one branch (`0017D036`) rejoins before that store
  **[image]**.
- **The seeding (I1), the frame base (I3) and the eleven allocations (I4) execute on the job thread, not in the
  framework's init call.** Nothing waits for them. `0079F150` carries on past `0079F69A` without reading `+0x113C`, and the
  census below finds no reader of it outside slots 4, 7 and 8. The only ordering the game imposes is therefore the latch.
- **The latch is published without a lock or fence:** a plain byte `mov`. On x86-64, stores become visible in program
  order, so a reader that sees 1 also sees `0017D000`'s earlier stores. That is an inference from the memory model;
  nothing here observes it.

**I9 — THE LATCH IS CLEARED ONCE AND SET ONCE. IT GATES ALL OF SLOTS 4 AND 8, BUT IN SLOT 7 ONLY AN ARM THAT DOES
NOTHING.**
- **Census [image]:**
  - `[reg+0x113C]` at any width, image-wide, gives exactly four sites: the writer `0017D074` and the readers
    `0017CCD6`, `0017CE77` and `0017D094`.
  - No non-stack access from `+0x1130..+0x113B` overlaps the byte.
  - The only rip-relative reference to the byte is the constructor's word clear `0015BC68`.
  - The static object is named in `.text` only by its constructor, its unwind funclet `00896280` and its `atexit`
    destructor `008A6970`. The last two only tail-jump to the base destructor (`00896280` + 0x7, `008A6970` + 0x15).
- **No code path clears the byte after construction.**
- **Slot 4, latch clear:** jumps to `0017CD84` and tail-calls `005C5230`, so it returns 0 having entered nothing
  **[exec]**.
- **Slot 8, latch clear:** returns 0 (`0017D09D`) **[exec]**. **Latch set:** calls the renderer getter `00189120`
  first **[exec]**, then the render pass list `00187950` (`0017D0B0`).
- **Slot 7 tests `00228480` (`[01FD4948] != 0`) before the latch.** When that holds, it drives the input object
  `[01F7FFE0]` through `001967D0` and returns, latch or not (`0017CE59`–`0017CE76`). Its latched arm calls only
  `0016D6A0`, which is `ret 0` (`0017CE95`).
- **The latch therefore orders the frame tick and the render pass after the init job. It does not order slot 7's
  input step.** The run with the latch clear enters `00228480` first **[exec]**.

**Failure paths and edge conditions.**
- **Any mount failure is silent.** The causes are: five slots full; an allocation failure; a null path; `fopen` NULL;
  a bad magic; a digest mismatch. On each, `0019B070` frees the archive and clears its slot (`0019B0F1`–`0019B10F`).
  Slot 2 still returns 0 (I6). What the game does later with no archive mounted is not established here.
- **A bad magic prints `"BigFile head wrong!"`** (`0017D280`, `001F43E7`) and leaves the `FILE` open. The only
  `fclose` is `001F4471`, past the magic test **[image]**, and the run counts one open and no close **[exec]**.
- **On accept, `001F4340` opens the archive 15 more times**, one per `0x30`-byte stream record (`001F4687`,
  `00215290` → `fopen` at `002152AD`). None of those `fopen` results is tested **[image]**.
- **Slot 3 does not test the job-manager pointer.** `[01F810F8]` goes to `00199F10` without a test
  (`0017CF7C`–`0017CF84`), and `0019A0A0` stores NULL when its allocation fails (`0019A0DA`) **[image]**.
- **If the job never runs, the latch stays 0.** Slots 4 and 8 then return 0 on every frame.
  `005CD1E0`'s behaviour on `CreateThread` failure was not read in full (see Open, below).

**Evidence class.**
- **NATIVE/STATIC [image]:** I6, I8, and I9's census.
- **NATIVE-REPLAY [exec]:**
  - I7, on the shipped archive's own bytes;
  - I9's three slot behaviours.
- **Sensitivity controls.** Each makes its check FAIL as required:
  - the latch store retargeted to `+0x113D`;
  - the magic immediate changed;
  - slot 2 returning `esi`.
- **No live observation exists of the thread on which `0017D000` runs, or of how many frames pass before the latch is
  set.** That count depends on scheduling (a 5 ms poll plus the length of the init burst), so it is not covered by
  §9's "boot is fully deterministic".

**Open.**
- What `005CD1E0` does when `CreateThread` fails. That path calls `GetLastError` (`005CD236`) and `FormatMessageA`
  (`005CD262`), and was not traced to its end. The `RaiseException` at `005CD2D8` raises `0x406D1388`, the
  thread-naming exception; it is not a failure path.
- What reads from the archive when no mount succeeded.
- What `0017D6B0` builds, and what slot 2's argument pair means.
- Whether the first game frame after the latch sees one framework delta or the delta accumulated while it was clear
  (slot 4 reads `+0x48` at `0017CCF0`).

## 5. State

`DAT_02EB4234` first-use latch · `DAT_01DFE0B4` frame limit · `uRam_02064ACC` frame-base constant ·
the nine registered pools and two unregistered allocations.

## 6. Relationships

`0017D4C0` calls the fixer; the RNG seeder is shared with the save-load reseed path (I2); the frame
limit is `GameSetting.ini`'s, whose own contract governs the setting **[page]**.

## 7. State transitions

```
boot:
    0022BDF0 : FrameLimit -> (==1) -> 001EDDC0 writes the triple ONLY on the 60 branch
               uRam_02064ACC = 2 / DAT_01DFE0B4                       (I3)
    seed     : first use -> 5489 (mt19937 default); boot -> 4537      (I1)
    memory   : 11 allocations, 9 registrations                        (I4)
```

## 8. Script · resource · event interactions

None — boot runs before content. `GameSetting.ini` is the one external input **[page]**.

## 9. Determinism

**Boot is fully deterministic, and that is the point.** The generator's stream is fixed by a literal
(I1). **The only thing that changes it is loading a save** (I2) — so a determinism argument that
starts "the RNG is seeded identically every launch" is correct only for a session that never loads.

## 10. Failure paths and edge conditions

* **`FrameLimit != 1`** → the 30 branch, and **`001EDDC0` does not write the triple** (I3).
* **Two allocations are never registered** (0.5 MiB and 1 MiB). They are stored to globals and used
  elsewhere; **what they are is not established by this function** **[page]** *(answered: see what-the-engine-fixes-at-boot.md, RC-3 answered 2026-09-30; 2026-10-02, OPUS)*.
* **Id 10 is absent from the otherwise dense range 2–11.** **Whether it is registered elsewhere or
  does not exist is unanswered** — and a gap in a dense range is either a second registrar or a
  retired pool **[page]**.

## 11. Observable behaviour

Nothing the player sees directly — but every "the game always does X on a fresh boot" observation
rests on I1, and every such observation **stops holding after a load** because of I2.

## 12. Reproduction formula

Seed with 5489 on first use and 4537 at boot (I1). Compute `2 / FrameLimit` as an **integer**
division (I3). Allocate eleven pools and register nine (I4), passing the tail value as the
**handle-slot count** (I5) — **not** as an alignment, which is what it looks like.

## 13. Runtime validation

**LIVE, for one invariant only.** `EXP-001` ran a **controlled A/B in a live process** and concluded
that the FrameLimit-to-time-base relationship is **"CAUSAL, not merely co-occurring"** — which is the
live footing under I3's dependence on `DAT_01DFE0B4` **[EXP-001]**. **This is the only live citation
in any contract I wrote today.**

**Scoped honestly**: EXP-001 establishes that the setting drives the time base. It does **not**
execute boot's `2 / DAT_01DFE0B4` arithmetic, the `001EDDC0` 60-branch asymmetry, the generator
seeding, or any allocation. ~~**I1, I2, I4 and I5 are static readings.**~~

### 13a. NATIVE-REPLAY — the three static invariants now execute (FABLE, 2026-09-21)

**`EXP-142` (`s01-boot-exec`, published `b14925d52`) executed all three bodies this section named as
unexecuted**, in isolation against the shipping image, 10/10 cases stable across three processes.
It was commissioned as three separate FABLE requests against this very gap and it had **not been
cited anywhere in the database** — `L2-VERDICTS.md` referenced it zero times — which is why this
subsection exists.

| invariant | what executed | result |
|---|---|---|
| **I1** seeding | `00863D30` → `00866D60`, five cases | All 624 state dwords equal an **independently computed** MT19937 init-by-seed recurrence in every case, index `0x270`. The implicit `5489` pass fires **once, on the first wrapper call only** — a second call seeds just the caller's value. `00866D60` **never dereferences `rcx`**, so the "object" argument carries no reachability requirement |
| **I3** frame base | `001EDDC0`, both `ecx` branches, four cases | The `B8=2.0f` / `BC=0.5f` / `E38=1` / `B4=2` quadruple is written **only** on the non-zero branch; `ecx==0` leaves all four at their shipped static values on both the WINMM success and failure arms, and never enters the LUT battery that the non-zero branch runs first (named at `EXP-142`, not cited here — this contract asserts no crossing into it). A failed `timeGetDevCaps` skips `E40` / `E3C` and still runs the common tail — no early exit |
| **I4** budget | `0022A0B0`'s eleven `malloc`s through the real thunk chain | All eleven sizes match this contract's table verbatim **and in order**; exactly **nine** `00369D30` calls follow, and the two tail-less blocks get none and are returned entirely unwritten |
| **I5** tail bytes | the nine registrations' write sets | Head-resident, not end-of-block — see the note under I5 |

**The evidence class is `NATIVE-REPLAY`, not `LIVE`, and the difference is load-bearing here.** The
image is mapped from the verified EXE and every non-import callee runs as shipped bytes, but the
memory is synthetic fixture memory and three boundaries are scripted: `malloc` is a bump allocator
(so the *sequence* of returns is real and the *addresses* are not), the WINMM trio is canned at the
call site (so the call order and arguments are real observations and the `TIMECAPS` contents are
not), and unnamed imports return 0. **Nothing in EXP-142 claims initialized-gameplay reachability**,
and this subsection claims none either: it says these four invariants are no longer *unexecuted*, not
that boot has been observed. **The live gap that remains is reachability** — that the shipped boot
path actually reaches these bodies with these arguments — and `EXP-001` is still the only live
citation in this contract.

**This subsection re-scores nothing.** Whether NATIVE-REPLAY over a disclosed boundary satisfies the
runtime cell is a verdict-time judgement, and [`L2-VERDICTS.md`](../_index/L2-VERDICTS.md) is OPUS's.
Routed as `FABLE-REQ-OPUS-RESCORE-S01-RUNTIME-CELL-EXP142-EXECUTED-THE-THREE-STATIC-INVARIANTS`.
**Ruled 2026-09-21 (OPUS, `131910290`): the cell is `MIXED`, the old binding gap was false, and the
gap is re-stated as three items.** §13b answers two of them.

### 13b. Which branch `001EDDC0` takes, and what happens if an allocation fails (FABLE, 2026-09-21)

**The branch is a player setting, it was observed at both values, and the observation was on a
sibling contract all along.** `0022BDF0` does **not** read the frame-limit global. It calls
`0017D8F0`, whose whole body is `mov rax, [01F82D20]` / `mov eax, [rax+0x48]` / `ret` — **the
settings singleton's row 18** — reduces it to a boolean at `0022BE18` (`cmove`, so *any* value that
is not exactly `1` yields `0`), and tail-jumps into `001EDDC0` with that boolean in `ecx`. The
global `01DFE0B4` is the **product** of the branch, not its input: image-wide it has **120 readers
and exactly one writer, `001EDDC0` itself**.

`EXP-001` — the experiment §13 already cites for I3's causality — **also varied that row and
recorded it**, and the table is on
[the game-setting contract](../19-Save-Load-Settings/Game-Settings-Config/CONTRACT-game-setting-config.md):
`setting[18] +0x48` reads **1** at `FrameLimit=60` and **0** at `FrameLimit=30`, with the time base,
scale, inverse and the 60 Hz gate all moving with it and four control fields untouched. So **in the
vanilla install with default settings the answer is the non-zero branch** — `setting[18] = 1`,
quadruple written, `01DFE0B4 = 2` — and the other branch is not hypothetical, it is one edited line
of `GameSetting.ini` away. **This contract has been citing that experiment for one fact while a
second, directly answering its own gap, sat in the same record.**

> **And one ordering fact that belongs here more than where it is recorded.** `EXP-001` observed
> that **at the first instant the settings singleton is non-null, `setting[18]` was already `1`
> while the time base was still `1`** — *the engine starts on the 30 fps base and switches later in
> startup*. That is a boot-ordering statement about the very body this contract is about, it is
> `PROBABLE` rather than proven (the window's length is unmeasured), and a reconstruction that
> applies the frame base at construction would be wrong about the order even while agreeing about
> the value.

**There is no allocation-failure behaviour, because no return is tested.** The eleven `malloc`
thunk calls at `0022A1E1`, `0022A1F2`, `0022A203`, `0022A214`, `0022A225`, `0022A236`, `0022A247`,
`0022A258`, `0022A269`, `0022A27A` and `0022A28B` run as a **straight line**: each is followed only
by `mov ecx, <next size>` and a store of `rax` into its `.data` pointer slot
(`01FD49F0`–`01FD4A90`). **There is no `test rax, rax`, no `cmp`, and no branch anywhere between the
first call and the nine registrations that follow at `0022A2AE`–`0022A394`** — the first test in the
body after them is at `0022A3DF`, and it is not on an allocation result. So a null return is stored
and, for the nine registered blocks, handed straight to `00369D30`, which writes into it; the
failure mode is a fault at first use, not a handled error.

*This is why `EXP-142` could not answer this item and did not claim to*: its `malloc` is a bump
allocator that always succeeds, so the failure path was never reachable in replay. **It is not an
execution question at all** — the absence of a test is visible in the instruction stream, and
nothing can execute a branch that is not there. **A reimplementation must not add error handling
here**: checking the returns would diverge from the original on exactly the input that distinguishes
them.

**What remains of the gap is the third item only** — the class ruling on whether NATIVE-REPLAY over a
disclosed import boundary satisfies the runtime cell, which is OPUS's.

**`EXP-071` declined** — procedural generator, not MT19937 (see the header).

**UNLINKED**: EXP-001's `contract:` names the game-setting contract, correctly, since that is what it
was designed to test. **No exemption added**, consistent with the rest of today's work.

### 13c. What the branch switches — the ~~render-scale~~ **time-base** triple and the three predicates that publish it (FABLE, 2026-09-21) — *name corrected in 13d*

Section 13b establishes *which* branch `001EDDC0` takes and that `01DFE0B4` is its product with 120
readers. It does not say what those 120 readers do with it. They **divide by it**.

`001EDDC0`'s non-zero arm writes **four** cells, not one:

```asm
001EDDC8  movss xmm0, dword ptr [01CEBC08]   ; 2.0f
001EDDD0  movss xmm1, dword ptr [01CEBB70]   ; 0.5f
001EDDD8  movss dword ptr [01DFE0B8], xmm0   ; 1.0f -> 2.0f
001EDDE0  movss dword ptr [01DFE0BC], xmm1   ; 1.0f -> 0.5f
001EDDE8  mov   dword ptr [01F82E38], 1      ; the mode flag
001EDDF2  mov   dword ptr [01DFE0B4], 2      ; 1 -> 2
```

Each of the four has **exactly one writer, this instruction**, and the raw `.data` bytes give the
defaults the zero branch leaves in place: `01DFE0B4 = 1`, `01DFE0B8 = 1.0f`, `01DFE0BC = 1.0f`.
Consumption, from a sweep of every function body:

| cell | value off / on | reader functions | read sites |
|---|---|---|---|
| `01DFE0B4` | `1` / `2` | **120** | 211, of which **21 are `div dword ptr [01DFE0B4]`** |
| `01DFE0B8` | `1.0f` / `2.0f` | 37 | 45 |
| `01DFE0BC` | `1.0f` / `0.5f` | 93 | 182 |

So the setting does not toggle a feature: it publishes an **integer scale, a multiplier and its
reciprocal** that a fifth of the UI and render layer folds into its own arithmetic, and at the default
every one of them is the identity. *A census that reads `div m32` as a store reports 22 writers for
`01DFE0B4` instead of 1* — the memory operand of `div` is a source, and that mistake is what the
single-writer control on this sweep was there to catch.

`01F82E38` is the mode flag the rest of the engine asks about. It is read by 13 functions, three of
which are predicates that hand the answer out:

| | shape | returns |
|---|---|---|
| `001EDDA0` | `01DFE0C0` (suppressor) first, then `01F82E38` (flag) | `0` iff the mode is on and unsuppressed, else `1` |
| `001EDEC0` | ~~the same pair~~ **the flag first, then the suppressor** (`001EDEC0`/`001EDEC9`), then bit 0 of its argument | `1`, unless the mode is on and unsuppressed — then `(~arg) & 1` |
| `001EDE80` | ~~the same pair~~ **the flag first, then the suppressor** (`001EDE84`/`001EDE8D`) | `1`, unless the mode is on and unsuppressed — then `0022A080() + 0022A030()`, a 32-bit sum |
| `001EDE70` | — | the flag itself, verbatim (not normalised to 0/1) |

*Read order restated 2026-09-25 (FABLE, Claude Opus 5.5) after §13f's executed finding, re-read
from the three bodies: only `001EDDA0` tests the suppressor first. Every predicate is a pure
function of the two cells, so the order changes no return value; the row text was wrong, not the
returns.*

`01DFE0C0`, the suppressor those three consult, **ships as `1`** and has one writer, the 7-byte
`001EDEF0` (it stores its argument verbatim), reached only from `00184960`. ~~Set to `1` on entry,
cleared unless the caller's mode argument is `1` and `byte [001EBA40() + 0x118]` is zero.~~
**Restated after §13f (executed):** `00184960` sets it to `1` on entry, then reads the flag.
**If the flag is `0` it keeps the suppressor set** and never consults the mode or the byte.
Otherwise it **clears** the suppressor when the mode argument is not `1`. When the mode is `1` and
`d[02092748]` is non-zero, it runs the `00229EA0` gate, and a failed gate (`00229EA0() != 1`,
`0018498E`) **clears it without reading the byte**. Only when the gate is not armed, or passes, does
`byte [001EBA40() + 0x118] == 0` keep it set (non-zero clears). Both keep paths hand the tail
`ebx = mode`, which is `1` on the byte path. Every clearing path hands it `ebx = 1` (`001849A7`).
That value goes to `00798E90`. It also goes to `005FEA50`'s `r8`, but only when `00189120()` is
non-null (`001849B8`). `00184960` has four callers — `0022A0B0`,
`0022B7E0`, `00250540` and `002507C0`. **What consumes those predicates** is read out for one of them
on [the text-element dispatch table](../99-Unresolved-Residual/Glyph-Run-Rendering/the-text-element-dispatch-table.md),
where `001EDEC0`'s answer is latched into a global for the span of one UI message.

**And the same boot body reads the command line.** `0022BDF0`'s two arguments are `argc` and `argv`
(`0022BE05`, `0022BE02`); between the setting read and the tail-jump it compares the first 8 bytes of
each argument against `"-nologo"` at `00908BD8` and calls `00314DE0(1)` on a match
(`0022BE30`-`0022BE62`). That is the only command-line switch this body honours. *The 8 bytes include
the terminating NUL (`0022BE4E cmp rax, 8`), so the match is exact: `-nologo2` does not trip it
(executed in §13f). The loop starts at index 0 and does not stop at a match.*

**Layers this section's citations reach, and why each is an accessor rather than a crossing.**
The three predicates are shared helpers with fan-in across the image, so naming them pulls in their
callers. **Audio — MECHANICAL:** `003B99D0` calls `001EDDA0`; it asks the scale question, it does
not own it. **Movement — MECHANICAL:** that layer's movement-side pump, the one
the drawing notes elsewhere in this database already trace, calls both `001EDDA0` and `001EDE80` —
two reads of the same flag from one body, which is what a published predicate looks like from the
consumer side. *Its address is deliberately not cited here: it is a hub, and citing it would import
its whole edge set into this contract for a one-line accessor note.* **Developer — MECHANICAL:**
`001EBA40` is the singleton `00184960` reads `+0x118` from before clearing the suppressor; cited to
say what the condition reads, nothing more. None of the three is a shared responsibility with this
contract.

*Static, from the shipping bytes: the four stores, the section-header raw-backing test on each cell,
the reader sweep with a single-writer control, the four predicate bodies and the argv loop.*

### 13d. Correction to 13c — the triple is the FrameLimit TIME BASE, and the database already named it (FABLE, 2026-09-21)

**Section 13c called these cells a "render-scale triple". That name is wrong and everything inferred
from it is withdrawn.** The four stores, the single-writer result on each, and the 120 / 37 / 93
reader counts over 211 / 45 / 182 sites all stand — they were measured. What they are is the
**`FrameLimit` time base**:

- `what-the-engine-fixes-at-boot.md` states `01DFE0B4` as "**frame base: 1 at 30 fps, 2 at 60**";
- `one-word-decides-which-fifteen-subsystems-tick.md` names `01DFE0B8` / `01DFE0BC` as "**the
  `FrameLimit` time-base pair**";
- and **section 13b of this very contract** already records `EXP-001` varying that row and reports
  "the time base, scale, inverse and the 60 Hz gate all moving with it".

So `setting[18]` is `FrameLimit`, `01DFE0B4` is the number of 60 Hz steps per 30 Hz frame, and the
211 `div`-and-read sites are code converting a quantity authored per 30 fps frame into the frame rate
actually running. `10-Status-Periodic-Terminal/Periodic-Tick/what-the-periodic-tick-does.md` §5 is
the clearest downstream use: the periodic drain interval is `[01DFE0B4] × 30 / 3`, **10 ticks at
30 fps and 20 at 60 — a third of a second either way**.

**How the error happened, because it is the instructive part.** The measurement was sound and the
name was invented from its shape: a `2.0f` beside a `0.5f` beside an integer `2` reads like a
resolution scale if you go looking for one. I ran the prior-art grep on the *question's* addresses
(`001EDEC0`, `01E0CDC8`) and not on the *answer's* (`01DFE0B4`), and the answer's addresses were
named in four places, one of them eight lines above where I was typing. **Grep the cells the finding
lands on, not only the cells the question started from.**

*Nothing measured in 13c changes. `001EDDC0`, `0022BDF0`, the `-nologo` scan, the four predicates and
every count are as published.*

### 13d. The replay ruling landed, and applied per invariant (FABLE, 2026-09-22)

S-01's binding gap has read *"one item, and it is not mine: the class ruling on replay"* since OPUS
re-judged the runtime cell. **That ruling returned on 2026-09-22 at 06:51** — on
`OPUS-REQ-FRONTIER-DOES-NATIVE-REPLAY-OVER-A-DISCLOSED-IMPORT-BOUNDARY-SATISFY-THE-RUNTIME-CELL`,
answerable once for the whole L2 table — and it is **per-invariant, with the boundary's role
deciding**:

| the boundary's role | verdict |
|---|---|
| **cannot reach** the invariant | satisfied outright |
| **observes only** — real code computes, stubs watch | satisfied, residue recorded as named debt |
| **load-bearing** — the scripted returns *are* the inputs under test | **NOT satisfied** — needs a fidelity proof of the script against real import behaviour, or live/native execution |

A whole-system runtime MET requires **every** named invariant satisfied under that rule.

**I1 — seeding. Satisfied outright, and the ruling says so itself:** no import participates and the
oracle is external to both the image and this database.

**I4 — the memory budget. Satisfied, and its named debt looks already discharged.** The ruling
records the residue as *"the stub always succeeds so allocation-failure behaviour is
unestablished"*. **§13c already established that no allocation return is ever tested**: the eleven
`malloc` thunk calls at `0022A1E1`, `0022A1F2`, `0022A203`, `0022A214`, `0022A225`, `0022A236`,
`0022A247`, `0022A258`, `0022A269`, `0022A27A` and `0022A28B` run as a straight line, with no
`test rax, rax`, no `cmp` and no branch between the first call and the nine registrations at
`0022A2AE`–`0022A394`; the first test after them, `0022A3DF`, is not on an allocation result. *So
the residue names a behaviour the shipped code does not have. An always-succeeding stub cannot hide
a failure path that was never written.*

**I3 — the frame base. The ruling puts it at load-bearing, and that classification is contested.**
Filed as `FABLE-CONTRA-FRONTIER-S01-I3-THE-WINMM-BOUNDARY-IS-NOT-LOAD-BEARING`. The premise is that
*"the WINMM trio is scripted per case and the branches under test are the responses to those
returns"*. Read at the image, **no frame-base value is produced by, or selected by, any import
return**:

- **The selecting branch is the settings boolean, not an import.** `001EDDC0`'s only top-level
  branch is `001EDDC4 test ecx, ecx` / `je`, and `ecx` arrives from `0022BDF0` as the `cmove`-reduced
  value of settings row 18 — §13c's own finding, and `EXP-001` varied that row **live**.
- **The values are image constants.** The taken arm writes all four globals with no import in the
  path: `001EDDC8` loads `2.0f`, `001EDDD0` loads `0.5f`, `001EDDE8` writes an immediate `1` and
  `001EDDF2` writes an immediate `2` into `01DFE0B4`, whose sole writer this body is.
- **What the imports actually carry is the multimedia timer period.** The three IAT slots resolve —
  from the import directory, not from a name guess — to `timeGetDevCaps`, `timeBeginPeriod` and
  `timeEndPeriod`. **The only branch in the whole body that tests an import return is
  `001EDE2F test eax, eax` / `jne`, on `timeGetDevCaps`, and it sits inside the `ecx == 0` arm — the
  arm that writes no frame-base global at all.** It gates whether the period is recorded and raised,
  nothing more.

> **So under the ruling's own taxonomy the frame-base invariant is case (a): the boundary cannot
> reach it.** If FRONTIER upholds that, all three invariants are satisfied. If FRONTIER rejects it,
> the gap is no longer *"awaiting a ruling"* but the single obligation the ruling names for case (c)
> — a fidelity proof of the scripted returns against real import behaviour, or a live execution —
> which is ASTRA or SWE2-ORACLE work and is routed as such.

### 13e. `I3` upheld, and the other two are classified rather than missing (FABLE, 2026-09-22)

**FRONTIER discharged the contra and the conditional above resolved in the affirmative.** Their
2026-09-22 block (rev 28615) reads: *“S-01 I3 replay contra: **ACCEPTED + verified at the image**.
`001EDDC0`'s frame-base writes are in the settings-boolean arm from image constants; the only
import-return test sits in the other arm writing none. **I3 re-classified SATISFIED by replay**;
S-01 runtime cell amended in `L2-VERDICTS.md`.”* — *and they verified it themselves rather than
taking §13d's reading on trust, which is why it stands.*

**Their block closes with “Other two EXP-142 replay invariants still unclassified.” They are
classified — `I1` and `I4`, immediately above, written the same day.** What they lack is the
adjudication `I3` received, and that is requested as
`FABLE-REQ-FRONTIER-S01-I1-AND-I4-ARE-CLASSIFIED-ADJUDICATE-THEM`.

> **`I4`'s basis was re-verified at the image today rather than cited from §13c.** Over
> `0022A1E1`–`0022A394` there are **zero** `test` / `cmp` / `jcc` instructions. The span holds
> **exactly eleven** `call 0036D240` — the `malloc` thunk — at the eleven addresses §13c lists,
> followed by **nine** `call 00369D30` registrations, as one straight line. **So no allocation
> return is tested anywhere in it**, and the ruling's residue *“the stub always succeeds so
> allocation-failure behaviour is unestablished”* names a behaviour the shipped code does not have.
> *An always-succeeding stub cannot hide a failure path that was never written.*

**NOTHING IS SCORED HERE EITHER.** `I3` is upheld by its adjudicator; `I1` and `I4` await theirs;
the cell remains OPUS's to move.

**NOTHING IS SCORED HERE.** The ruling's own completion clause says *"OPUS applies it to S-01"*, and
S-01's row is not this contract's to move; the re-score is filed as
`FABLE-REQ-OPUS-S01-ROW-IS-STALE-THE-RULING-HAS-LANDED`. *What this section establishes is the
evidence the re-score needs, and that the row's current text — "routed, not assumed" — describes a
question that has been answered since 06:51.*

### 13f. The §13c predicate layer now executes (EXP-147, SWE2-ORACLE, 2026-09-22)

**`EXP-147` (`boot-predicates-exec`, 44 cases, zero failures, stable ×3) executed the predicate
layer §13c described statically**: all four flag/suppressor predicates, the suppressor writer
`001EDEF0`, its gate `00184960`, the singleton getter `001EBA40` (present and lazy paths), and the
`0022BDF0` selector with its `-nologo` scan — on shipped bytes **[EXP-147]**. Executed facts that
refine §13c's prose:

* **`001EDDA0` and `001EDEC0` read the same pair in opposite orders** — DA0 tests the suppressor
  first, EC0 tests the flag first; the table's "the same pair" flattens that.
* **`001EDE70` returns the flag verbatim** (`0x7F → 0x7F`), and **`001EDEF0` writes verbatim**
  (`0x7F → 0x7F`) — neither bool-normalises.
* **`001EDE80`'s live-path sum is `d[02064AD8] + d[02064AA8]`, 32-bit** — `0xFFFFFFFF + 2 → 1`.
* **`00184960` has two conditions §13c's "cleared unless mode==1 and byte==0" misses**: `flag==0`
  keeps the suppressor set without ever consulting mode or the byte, and a **`00229EA0` gate**
  (armed by `d[02092748]`, comparing `movsx b[02064AD3]` against the mode argument) **force-clears
  while bypassing the byte check entirely** — executed: mode==1, byte==0, gate failed → suppressor
  cleared. On the `flag==0` early path the tail gets `ebx = mode` verbatim; every cleared path
  hands `ebx = 1` to `00798E90` (which clamps `[1,3]` into `d[01F3DA18]`) and to `005FEA50`'s
  `r8`.
* **`0022BDF0`'s `-nologo` compare is an exact 8-byte match** — byte 7 must be NUL, so
  `"-nologo2"` and `"-nologoextra"` do **not** trip it (executed); `00314DE0(1)` writes
  `d[022C2528]`; the tail hands `ecx = (settings row 18 == 1)` to `001EDDC0`, executed through the
  real `0017D8F0` leaf reading `d[q[01F82D20]+0x48]`.
* Scripted boundaries, disclosed in the record: `001EDDC0` (ecx recorded — EXP-142's executed
  scope, not re-run), the `005FEA50` registry vtable dispatch (args recorded), the `00210EC0`
  allocator and `001EB190` init on the singleton's lazy path.

## 14. Unresolved

* **What the extra tail bytes on each allocation serve** (I5) — **narrowed 2026-09-21**: they are
  headroom at the *head* end, not records at the tail end, and nothing observed writes them
  **[EXP-142]**.
* **What the two unregistered allocations are** (§10) **[page]** — **sharpened 2026-09-21**: both are
  allocated and then left **entirely unwritten** by the boot battery, so whatever writes them is
  outside `0022A0B0` **[EXP-142]**.
* **Whether pool id 10 exists** (§10) **[page]** — the nine observed registration indices are
  2, 3, 4, 5, 6, 7, 8, 9 and `0xB`, so **id 10 is skipped by this battery** and the question is what
  else claims it **[EXP-142]**.
* ~~**The seeding and the budget have no execution** (§13).~~ **CLOSED 2026-09-21 (FABLE): both
  execute under `EXP-142`, §13a.** What replaces it is narrower: **no execution of boot's own
  reachability** — that the shipped path calls these bodies with these arguments is still read, not
  run.
* ~~**Which branch `001EDDC0` takes in the shipped process**~~ — **ANSWERED 2026-09-21 (FABLE),
  §13b**: it is `settings[18] == 1`, observed live at both values by `EXP-001`; default install
  takes the non-zero branch **[EXP-001]**.
* ~~**Allocation-failure behaviour**~~ — **ANSWERED 2026-09-21 (FABLE), §13b: there is none.** None
  of the eleven returns is tested **[page]**.
* **How long the startup window is** in which the time base is still `1` while `setting[18]` is
  already `1` (§13b) — `PROBABLE`, unmeasured **[EXP-001]**.

## 15. Evidence

The seeding, the frame-base derivation, the budget table and all three corrections are the page's
**[page]**; the causality of the frame-limit link is EXP-001's **[EXP-001]**. This contract's
contribution is I1–I5 stated as a contract, §9's warning that boot determinism does not survive a
load, and §12's note that the handle-slot count must not be implemented as an alignment.

**One note for the address checker, carried forward from the page**: the pool bases are **runtime
addresses, not image addresses**, and `0x03000000` is flagged `unwind-BANNED` only because it falls
inside `.pdata`'s virtual range. **It is a false positive** and nothing here cites unwind data.

## 16. Parity plan

Assert the generator's first hundred outputs from a cold boot, then **assert they differ after a
load — and differ again on a second load of the SAME save**, which is what distinguishes a
clock-sourced reseed from a save-sourced one (I2). A reconstruction that seeds identically in both
cases passes the first and fails the second; one that seeds from save data passes both and fails
the third. Test I3 at both frame limits and assert the triple is
written **only** at 60. Compare all nine registrations and both unregistered allocation sizes (I4).

`0037E0F0` (596 B) is the register battery `0022A0B0` runs inside the boot subtree: ~~46 straight `lea rcx, 02AE9xxx`/`02AEAxxx`/`02AEBxxx`/`02AECxxx` globals each handed to a `004C2040`/`004Dxxxx`/`004Exxxx`/`004Fxxxx` initializer~~ 49 `lea rcx` globals from `02AE8620` to `02AED330`, 48 of them handed by `call` to an initializer (47 distinct, `004E3110` twice; `002EFF50`, `002F0110` and six `0047xxxx` bodies among them) *(corrected 2026-10-02, OPUS: counted over all 596 bytes of `0037E0F0`)*, the last with a lone `jmp 004C3610` - the subtree's static-registration arm, whose targets are Presentation-side module initializers (named at subsystem level, not by address).

Interior anchor `0037E15B` (function `0037E0F0`).

`004FD060` (1104 B) is the largest of the register battery's constructors: `00861EC0` zeroes 0x300, `008631E0` registers callback `004F7070`, `008631D0(0x2E)` fills the `+0x10` array, then sixty-odd constant stores write `+0x18`..`+0x2FF` defaults (`+0x18` = 0x1000404, `+0x1C` = 0x6C2B0000, floats 457FA000/4B7FFF28) - the module record's init.

Interior anchor `004FD083` (function `004FD060`).

`004F4F80` (992 B) is the battery's second big constructor: `00861EC0` zeroes 0x2E0, `008631E0` registers `004EF940`, `008631D0(0x2C)` fills `+0x10`, then the same constant-fill shape (`+0x1C` = 0x6C290000) - a sibling module record's init.

Interior anchor `004F4FA3` (function `004F4F80`).

`004E2930` (863 B) is the battery constructor with the extra call: `00861EC0` zeroes 0x200, `008631E0` registers `004DF440`, `008631D0(0x1E)` fills `+0x10`, `004DC8B0` runs mid-fill, then constants (`+0x1C` = 0x6C1B0000, `+0x3C` = 0x4B189680) - another module record's init.

Interior anchor `004E2953` (function `004E2930`).

`004E2DE0` (814 B) is the battery's pure-fill constructor - no memset or registration arm: straight `008631D0(0x1E)` on `rbx+8`, then the constant block (`+8` = 0x1000404, `+0xC` = 0x6C1E0000, `+0x38` = 0x3FC00000, `+0x50`/`+0x58`/`+0x5C` = 0xFF) - a module record's field init.

Interior anchor `004E2DEE` (function `004E2DE0`).

`004D0880` (720 B) is the battery constructor `0037E0F0` calls on its `02AE8xxx` global: `008631E0` registers `004CF490`, `008631D0(0x19)` fills `+0x10`, `+0x18` = 0x1000404 / `+0x1C` = 0x6C160000 head the constant fill - a module record's init.

Interior anchor `004D089D` (function `004D0880`).

`004E7A90` (707 B) is the battery's pure-fill twin of `004E2DE0`: `008631D0(0x1E)` on `rbx+8`, then constants (`+8` = 0x1000404, `+0xC` = 0x6C1E0000, `+0x38` = 0x3F000000, `+0x50`..`+0x80` = 0x80) - a module record's field init.

Interior anchor `004E7A9E` (function `004E7A90`).

`004DADD0` (650 B) is the battery constructor registering `004DA8A0`: `008631D0(0x17)` fills `+0x10`, `+0x1C` = 0x6C170000, `+0x60`/`+0x64` = -1.0f and `+0x74` = -1.0f mark the signed defaults among the 1.0f/0x80 lanes - a module record's init.

Interior anchor `004DADE3` (function `004DADD0`).

`004DA650` (584 B) is the battery's smallest constructor: `008631D0(0x18)` fills `+0x10`, `+0xC` = 0x6C15001E, `+0x10` = 0xFFFFFF, `+0x28`/`+0x2C` = 100.0f, `+0x7C`/`+0x8C`/`+0x9C` = 0x40 with `0x80` colour lanes - a module record's init.

Interior anchor `004DA65E` (function `004DA650`).

`0047BAF0` (571 B) is a battery constructor `0037E0F0` calls: `008631E0` registers `0047A9C0`, `008631D0(0x15)` fills `+0x10`, then constants - `+8`/`+0xC` = 0x03000000/0x02000000, `+0x18` = 0x1000404, `+0x1C` = 0x6C140000, `+0x24` = 0x302EC000, floats 45000000/43960000/437A0000/C7000000 with `4B7FFF28` colour lanes and `3F800000` scales - a module record's init.

Interior anchor `0047BB03` (function `0047BAF0`).

`004C6BB0` (555 B) is a battery constructor `0037E0F0` calls: `008631E0` registers `004C5DF0`, `008631D0(0x15)` fills `+0x10`, then the same constant shape - `+0xC` = 0x02000000, `+0x18` = 0x1000404, `+0x1C` = 0x6C120000, `+0x20` = 0x8000 - a module record's init.

Interior anchor `004C6BC3` (function `004C6BB0`).

`004C5BD0` (542 B) is a battery constructor `0037E0F0` calls: `008631E0` registers `004C4D20`, `008631D0(0x14)` fills `+0x10`, then constants - `+0xC` = 0x02000000, `+0x18` = 0x1000404, `+0x1C` = 0x6C110000, `+0x20` = 0x8000 - a module record's init.

Interior anchor `004C5BE3` (function `004C5BD0`).

`004C7CF0` (524 B) is a battery constructor `0037E0F0` calls: `008631E0` registers `004C6DE0`, `008631D0(0x14)` fills `+0x10`, then the `0x02000000`/`0x1000404`/`0x6C110000`/`0x8000` head shared with `004C5BD0` - a module record's init.

Interior anchor `004C7D03` (function `004C7CF0`).

`004DB060` (523 B) is the battery's pure-fill constructor `0037E0F0` calls - no `008631E0` registration arm: straight `008631D0(0x14)` on `rcx`, then `+8` = 0x1000404, `+0xC` = 0x6C140003, zero lanes at `+0x14`/`+0x28`/`+0x38`/`+0x48`/`+0x58`/`+0x94`/`+0xA8`/`+0xBC`/`+0xC4`, and +/-1.0f (`3F800000`/`BF800000`) at `+0x1C`/`+0x20`/`+0x24` - a module record's field init.

Interior anchor `004DB06E` (function `004DB060`).

`004EC960` (515 B) is a battery constructor `0037E0F0` calls: `008631E0` registers `004EBE80`, `008631D0(0x11)` fills `+0x10`, then `+0xC` = 0x02000000, `+0x18` = 0x1000404, `+0x1C` = 0x6C0E0000 head the constant fill - a module record's init.

Interior anchor `004EC973` (function `004EC960`).

`004C8080` (509 B) is a battery constructor `0037E0F0` calls: `00861EC0` zeroes first, `008631E0` registers `004C8320`, `008631D0(0x27)` fills `+0x10`, then `+0xC` = 0x02000000, `+0x18` = 0x1000404, `+0x1C` = 0x6C260000 - the largest field count of the family.

Interior anchor `004C8097` (function `004C8080`).

`004DCA00` (507 B) is a battery constructor `0037E0F0` calls: `00861EC0` zeroes, `008631E0` registers `004DCC00`, `008631D0(0x18)` fills `+0x10`, then `+0xC` = 0x02000000, `+0x18` = 0x1000404, `+0x1C` = 0x6C150000 - a module record's init.

Interior anchor `004DCA17` (function `004DCA00`).

`004DC6B0` (498 B) is a battery constructor `0037E0F0` calls: `00861EC0` zeroes, `008631E0` registers `004DB350`, `008631D0(0x11)` fills `+0x10`, `004DC8B0` runs mid-fill, then `+0xC` = 0x02000000, `+0x18` = 0x1000404, `+0x1C` = 0x6C0E0000 - a module record's init.

Interior anchor `004DC6C1` (function `004DC6B0`).

`004C4A50` (494 B) is the battery's memset-only constructor `0037E0F0` calls - `00861EC0` zeroes and constants fill `+0xC` = 0x02000000, `+0x18` = 0x1000404, `+0x1C` = 0x6C100000 with no `008631D0`/`008631E0` arm - a module record's field init.

Interior anchor `004C4A61` (function `004C4A50`).

`00476C80` (494 B) is a battery constructor `0037E0F0` calls: `008631E0` registers `004758E0`, `008631D0(0x43)` fills `+0x10` - the family's deepest field array - then `+0xC` = 0x02000000, `+0x18` = 0x1000404, `+0x1C` = 0x6C420000 - a module record's init.

Interior anchor `00476C93` (function `00476C80`).

`004ED960` (482 B) is a battery constructor `0037E0F0` calls: `008631E0` registers `004ECC50`, `008631D0(0x11)` fills `+0x10`, then `+0xC` = 0x02000000, `+0x18` = 0x1000404, `+0x1C` = 0x6C0E0000 - a module record's init.

Interior anchor `004ED973` (function `004ED960`).

`004D0CB0` (450 B) is a battery constructor `0037E0F0` calls: `008631E0` registers `004D0FA0`, `008631D0(0x17)` fills `+0x10`, then `+0x8` = 0x03000000, `+0xC` = 0x02000000, `+0x18` = 0x1000404, `+0x1C` = 0x6C140000, and the `+0x20`..`+0x68` constant flood (`0x8000`/`0x602E4000`/`0x412412`/`0x457FA000`/`0x4B7FFF28`/`0x80` heads) - a module record's init.

Interior anchor `004D0CC3` (function `004D0CB0`).

`0047A800` (446 B) is a battery constructor `0037E0F0` calls: `008631E0` registers `00479650`, `008631D0(0xF)` fills `+0x10`, then `+0x8` = 0x03000000, `+0xC` = 0x02000000, `+0x18` = 0x1000404, `+0x1C` = 0x6C0E0000, and float heads `0x45000000`/`0x43800000`/`0x43600000` with `+0x40` = 1, `+0x44` = 0x14 - a module record's init.

Interior anchor `0047A813` (function `0047A800`).

`004D3E20` (445 B) is a battery constructor `0037E0F0` calls: `00861EC0` zeroes, `008631E0` registers `004D40E0`, `008631D0(0x17)` fills `+0x10`, then `+0x8` = 0x03000000, `+0xC` = 0x02000000, `+0x18` = 0x1000404, `+0x1C` = 0x6C140000 with the `+0xE0` arm and `0x8000`/`0x602E4000`/`0x412412`/`0x457FA000` constants - a module record's init.

Interior anchor `004D3E37` (function `004D3E20`).

`004C3610` (426 B) is a battery constructor `0037E0F0` calls: `008631E0` registers `004C2160`, `008631D0(0x11)` fills `+0x10`, then `+0x8` = 0x03000000, `+0xC` = 0x02000000, `+0x18` = 0x1000404, `+0x1C` = 0x6C0E0000, `+0x24` = 0x20204000, `+0x28` = 0x41, `+0x30`/`+0x34` = 0x457FA000 - a module record's init.

Interior anchor `004C3623` (function `004C3610`).

`004DA460` (423 B) is a self-initialising battery record `0037E0F0` builds: `00861EC0` zeroes `0x150` bytes, `008631D0(0x14)` fills `+0x10`, then `+0x8` = 0x1000404, `+0xC` = 0x6C140000, `+0x10` = 0x8001, `+0x14` = 0x602E4000, `+0x18` = 0x412412, `+0x1C` = 0x8000, `+0x20`/`+0x24` = 0x457FA000, `+0x28` = 0x4B7FFF28, `+0x30`/`+0x34` = 0x45000000 - the variant without a registered callback.

Interior anchor `004DA471` (function `004DA460`).

`004791E0` (398 B) is a battery constructor `0037E0F0` calls: `008631E0` registers `00478280`, `008631D0(0xD)` fills `+0x10`, then `+0x8` = 0x03000000, `+0xC` = 0x02000000, `+0x18` = 0x1000404, `+0x1C` = 0x6C0C0000, `+0x24` = 0xC02E4000, `+0x28` = 0x12412412, `+0x38` = 0x4B7FFF28, `+0x30`/`+0x34` = 0x45000000, `+0x40` = 0x43800000 - another module record init.

Interior anchor `004791F3` (function `004791E0`).

`00479450` (379 B) is a self-initialising battery record `0037E0F0` builds: `008631D0(0xF)` fills `+0x10` with no registered callback, then `+0x8` = 0x1000404, `+0xC` = 0x6C0C0002, `+0x10` = 1, `+0x14` = 0x14, `+0x1C` = 32768.0f (the `0x8000` constant through `cvtsi2ss`), `+0x20` = 0x430C0000, `+0x24` = 1.0f, `+0x2C` = 0x3F333333 (0.7), `+0x38` = 0x00FFFF28.

Interior anchor `0047945E` (function `00479450`).

`002F0110` (363 B) is a battery constructor `0037E0F0` calls: `008631D0(0x1D)` fills `+0x10`, then `+0x8` = 0x1000404, `+0xC` = 0x6C1A0013, `+0x10` = 0x10, `+0x14` = 8, `+0x20`/`+0x24` = 1.0f, `+0x28` = 0x3DCCCCCD (0.1f), `+0x34`/`+0x78`/`+0x84`/`+0xA4`/`+0x1C` zeroed and `+0xB4` initialised - the widest of the record inits.

Interior anchor `002F011E` (function `002F0110`).

`0037DF90` (344 B) is a registration battery `0022A0B0` calls: ~~thirty~~ 28 `lea rcx, 02ADExxx/02AExxxx` + `call` pairs — 27 calls to distinct bodies and the tail `jmp 004A8860` at `0037DF90+0x153` *(corrected 2026-10-02, OPUS: counted over all 344 bytes of `0037DF90`)* — run `00499850`/`0049B850`/`0049FE90`/`004A1C10`/`004B0B70`/`004978F0`/`0048CE70`/`004B0000`/`004802F0`... over the static object range - the boot table's widest block.

Interior anchor `0037DF9B` (function `0037DF90`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-EC7-163, 2026-09-22)

**Presentation — CLIENT (73 edges).** The boot subtree's registration
batteries hand their `lea`-loaded globals to Presentation-filed VIF-program
state-block initializers — `0037DF90` calls `0047E140`/`0048AB40`/`0048CE70`/
`0048F410`/`004B8F20` — and this page's `001EBA40`/`001EDDA0` are called by
`00187950`/`001F9B20`/`002F2530`/`002F3BC0` on that layer. The fixups
construct Presentation statics; the page's subject is the construction, not
the render layer.

`004B8F20` (2250 B) is the state-block initializer for `02AE4F20`: `008631E0`/`008631D0` open the descriptor (`edx = 0xC5`), then ~212 field writes fix the block - `+8 = 0x03000000`, `+0xC = 0x02000000`, `+0x18 = 0x01000404`, `+0x1C = 0x6C370000`, `+0x38 = 0xDE`, `+0x3C = 0x8000`, `+0x40/+0x44 = 0xB4/0x64`, `+0x48 = 100`, `+0x50 = -4.0f`, `+0x5C = 2.0f`, `+0x60 = 4.0f` - the battery's largest fill.

Interior anchor `004B8F37` (function `004B8F20`).

`0048AB40` (1067 B) is the state-block initializer for `02AE3620`: no helper calls - ~103 direct field writes plus four SSE stores fix the whole record from immediates - the battery's second-largest fill.

Interior anchor `0048AD6E` (function `0048AB40`).

`00485390` (1023 B) is the state-block initializer for `02AE21B0`: `00861EC0` then `008631D0`/`008631E0` open it and ~101 field writes follow - the battery's third-largest fill.

Interior anchor `004853A5` (function `00485390`).

`0048CE70` (965 B) is the state-block initializer for `02AE4160`: `00861EC0` opens it, ~89 field writes plus two SSE stores fix the record.

Interior anchor `0048D20A` (function `0048CE70`).

`0047E140` (943 B) is the state-block initializer for `02AE0B60`: no helper calls - ~96 immediate field writes fix the record outright.

Interior anchor `0047E32B` (function `0047E140`).

`0048F410` (887 B) is the state-block initializer for `02AE6BF0`: no helper calls - ~80 immediate field writes.

Interior anchor `0048F5FF` (function `0048F410`).

`00492D40` (854 B) is the state-block initializer for `02ADEF40`: `00861EC0` opens it, ~91 field writes follow.

Interior anchor `00493024` (function `00492D40`).

`004A6490` (743 B) is the state-block initializer for `02AE1BC0`: no helper calls - ~85 immediate field writes.

Interior anchor `004A65E3` (function `004A6490`).

`004A8860` (660 B) is the state-block initializer for `02AE1EF0`: `00861EC0`/`008631D0`/`008631E0` open it, ~71 field writes follow - the battery's tail-jump arm.

Interior anchor `004A8871` (function `004A8860`).

`004A3150` (603 B) is the state-block initializer for `02AE09A0`: no helper calls - ~70 immediate field writes.

Interior anchor `004A3256` (function `004A3150`).

`004BF2C0` (569 B) is the state-block initializer for `02AE6AA0`: `008631D0`/`008631E0` open it, ~62 field writes follow.

Interior anchor `004BF2D3` (function `004BF2C0`).

`004B0000` (555 B) is the state-block initializer for `02AE31F0`: `00861EC0` then `008631D0`/`008631E0` open it, ~56 field writes follow.

Interior anchor `004B0011` (function `004B0000`).

`004C0C70` (545 B) is the state-block initializer for `02ADFD00`: `008631D0`/`008631E0` open it, ~62 field writes follow.

Interior anchor `004C0C83` (function `004C0C70`).

`0049D310` (545 B) is the state-block initializer for `02AE0390`: no helper calls - ~68 immediate field writes.

Interior anchor `0049D408` (function `0049D310`).

`004A1C10` (536 B) is the state-block initializer for `02AE06B0`: no helper calls - ~63 immediate field writes.

Interior anchor `004A1CF7` (function `004A1C10`).

`004BC120` (510 B) is the state-block initializer for `02AE6950`: `008631D0`/`008631E0` open it, ~58 field writes follow.

Interior anchor `004BC133` (function `004BC120`).

`004956A0` (509 B) is the state-block initializer for `02ADFE90`: `00861EC0`/`008631D0`/`008631E0` open it, ~55 field writes follow.

Interior anchor `004956B1` (function `004956A0`).

`0049FE90` (509 B) is the state-block initializer for `02AE0520`: no helper calls - ~60 immediate field writes.

Interior anchor `0049FF67` (function `0049FE90`).

`004A4220` (495 B) is the state-block initializer for `02AE1910`: no helper calls - ~58 immediate field writes.

Interior anchor `004A42ED` (function `004A4220`).

`00482410` (471 B) is the state-block initializer for `02AE1DA0`: no helper calls - ~55 immediate field writes plus two SSE stores - the battery's smallest fill.

Interior anchor `004824E2` (function `00482410`).

`004978F0` (458 B) is a `0037DF90` constant-fill initializer bound to `02ADFFE0`: 56 field writes (35 immediate) over the registered state block, `[rcx+8] = 0x03000000` head.

Interior anchor `004979C0` (function `004978F0`).

`00499850` (452 B) is a `0037DF90` constant-fill initializer bound to `02AE0130`: 51 field writes (30 immediate), opening the descriptor through `008631D0`/`008631E0` first.

Interior anchor `0049987F` (function `00499850`).

`00487BA0` (445 B) is a `0037DF90` constant-fill initializer bound to `02AE30A0`: 54 field writes (36 immediate), `[rcx+8] = 0x03000000` head.

Interior anchor `00487C67` (function `00487BA0`).

`004802F0` (420 B) is a `0037DF90` constant-fill initializer bound to `02AE1A70`: 51 field writes (36 immediate), `[rcx+8] = 0x03000000` head.

Interior anchor `004803A8` (function `004802F0`).

`004AD840` (409 B) is a `0037DF90` constant-fill initializer bound to `02AE2F70`: 50 field writes (28 immediate), `[rcx+8] = 0x0300001E` head.

Interior anchor `004AD8DC` (function `004AD840`).

`004AAE20` (405 B) is a `0037DF90` constant-fill initializer bound to `02AE2080`: 50 field writes (27 immediate), `[rcx+8] = 0x0300001E` head.

Interior anchor `004AAEB8` (function `004AAE20`).

`0049B850` (393 B) is a `0037DF90` constant-fill initializer bound to `02AE0260`: 48 field writes (25 immediate), `[rcx+8] = 0x0300001E` head.

Interior anchor `0049B8E6` (function `0049B850`).

`004B0B70` (376 B) is a `0037DF90` constant-fill initializer bound to `02AE3330`: 38 field writes (28 immediate) behind an `00861EC0` descriptor open.

Interior anchor `004B0B81` (function `004B0B70`).

`004D0E80` (274 B) is the module-record initializer `0037E0F0`'s battery registers: `008631D0(rcx, 0xC)` fills the head, then the constant image lands - `+8` = `0x1000404`, `+0xC` = `0x6C090046`, `+0x18` = `0.5f`, `+0x1C`/`+0x28`/`+0x2C` = `1.0f`, `+0x30` = 1, `+0x40`..`+0x4C` = `0x80` x4, `+0x50` = `0x8004`, `+0x54` = `0x10000000`, `+0x58` = `0xE`, `+0x68` = 8, `+0x78` = 6, `+0x80` = `0x44`, `+0x88` = `0x42`, `+0x90` = `0x33001`, `+0x98` = `0x47`, `+0xA0` = `0x15000002`, `+0xAC` = `0x50000001`, `+0xB0` = `0x8000`, `+0xC0` = `0x13000000` - the packed-register block `004D0880`'s sibling constructor fills for its own global.

Interior anchor `004D0E8E` (function `004D0E80`).

`004E2CD0` (261 B) is the packet-template initializer `0037E0F0`'s battery registers: `00861EC0` zeroes `0xC0` and `008631D0(rcx, 0xB)` fills the head before the constant image lands - `+8 = 0x1000404`, `+0xC = 0x6C080028`, `+0x10 = 1`, `+0x1C = 0x8000`, `+0x20..+0x2C = 0x80 x4`, `+0x30 = 3.7f`, `+0x34 = 0.5f`, `+0x38 = 0.2f`, `+0x40 = 0x8004`, `+0x44 = 0x10000000`, `+0x48 = 0xE`, `+0x58 = 8`, `+0x68 = 6`, `+0x70 = 0x48`, `+0x78 = 0x42`, `+0x80 = 0x53001`, `+0x88 = 0x47`, `+0x90 = 0x15000000`, `+0x94 = 0x11000000`, `+0x9C = 0x50000001`, `+0xA0 = 0x8000`, `+0xB0 = 0x13000000` - the DMA-tag-flavored template `004D0E80`'s sibling builds for its own global.

Interior anchor `004E2CE1` (function `004E2CD0`).

`004DC8F0` (260 B) is the sibling `0xC0` packet-template fill `0037E0F0`'s battery registers: `008631D0(rcx, 0xB)` heads it, then the constant image lands - `+8 = 0x1000404`, `+0xC = 0x6C080080`, `+0x10`/`+0x14 = 1`, `+0x1C = 0.0f`, `+0x30`/`+0x34 = 0.1f`, `+0x38`/`+0x3C = 2.0f`, `+0x40 = 0x8004`, `+0x44 = 0x10000000`, `+0x48 = 0xE`, `+0x58 = 8`, `+0x68 = 6`, `+0x70 = 0x48`, `+0x78 = 0x42`, `+0x80 = 0x53001`, `+0x88 = 0x47`, `+0x90 = 0x15000000`, `+0x94 = 0x11000000`, `+0x9C = 0x50000001`, `+0xA0 = 0x8000`, `+0xB0 = 0x13000000` - the same GS-tag-shaped template `004E2CD0` fills for its own global.

Interior anchor `004DC8FE` (function `004DC8F0`).

`004D3FE0` (255 B) is the `0xD0` packet-template fill `0037E0F0`'s battery registers: `008631D0(rcx, 0xC)` heads it, then the constant image lands - `+8 = 0x1000404`, `+0xC = 0x6C090046`, `+0x14`/`+0x1C`/`+0x24` zeroed, `+0x28 = 2.0f`, `+0x2C = 1.0f`, `+0x40`/`+0x48 = 0x8000000080`, `+0x50 = 0x8004`, `+0x54 = 0x10000000`, `+0x58 = 0xE`, `+0x68 = 8`, `+0x78 = 6`, `+0x80 = 0x44`, `+0x88 = 0x42`, `+0x90 = 0x33001`, `+0x98 = 0x47`, `+0xA0 = 0x15000002`, `+0xB0 = 0x8000`, `+0xC0 = 0x13000000` - the third GS-tag-shaped template alongside `004DC8F0`/`004E2CD0`.

Interior anchor `004D3FEE` (function `004D3FE0`).

`008631D0` (15 B) is the packet-head writer the template fills open with: `word[rcx] = dx`, `byte[+3] = 0x10`, `dword[+4] = 0` - the tag stamp every GS-tag-shaped template shares.

Interior anchor `008631D3` (function `008631D0`).

`008631E0` (84 B) is the sequenced table committer: `word[rcx] = 1`, `byte[+3] = 0x30`; `r8d | 0x4A000000` and `rdx` land in `02EAF930 + counter*16` under `dword[02EB37B0]++`, then `0020E620` resolves and `dword[rbx+4]` takes the result - the boot fixup's tagged-record publish.

Interior anchor `00863226` (function `008631E0`).

`004E79C0` (199 B) is the display-record default constructor `0037E0F0` calls: `008631D0` with tag 0x25, then literal defaults - `+8` = 0x01000404, `+0xC` = 0x6C22001E, `+0x10` = 0x20, `+0x14` = 0x40, `+0x18` = 0.0f, `+0x1C` = 1, `+0x20` = 60.0f, `+0x2C` = 0.5f - a 0x200-byte zero splat at `+0x34`, and packed header words at `+0x230`/`+0x234`/`+0x23C`/`+0x240`/`+0x250`

Interior anchor `004E7A30` (function `004E79C0`).

`004D3D60` (181 B) is the fixed-record constructor `0037E0F0` runs during fixup: `008631D0(rcx, 7)` clears the base, then the record is stamped - ids `0x01000404`/`0x6C04001E` at `+8`/`+0xC`, count `5` and bound `0x20` at `+0x10`/`+0x14`, floats `30.0, 30.0, 1.0, 3.0, 5.0, 5.0` across `+0x20`..`+0x34` plus `1.0` at `+0x38` and bit-pattern `0x14540545` at `+0x1C`, flag words `0x15000001`/`0x11000000`/`0x50000001`/`0x8000`/`0x13000000` at `+0x50`..`+0x70`, pointer fields zeroed - the default-parameter record the boot path installs verbatim

Interior anchor `004D3D73` (function `004D3D60`).

`00259DF0` (158 B) is the worker spawn `0022A0B0` runs in the boot subtree: `0032E400(9, 3)` supplies the count, a nonpositive answer just clears `02098DF0`, otherwise it arms the `0036C1D0(6, 5)`/`0036C1A0(3)`/`0036A190(count)`/`0036C110`/`0036C140` pool sequence and `0032E620`-spawns with entry `00259370` and the `{0, ebx}` stack packet

Interior anchor `00259DFE` (function `00259DF0`).

`004DA3C0` (157 B) is one of the `0037E0F0` battery's static-record initializers: `00861EC0` zeroes `0x70` and `008631D0(rcx, 6)` lays the base, then the defaults land - `+8 = 0x1000404`, `+0xC = 0x6C030014`, `+0x10`/`+0x14 = 0x16`, `-9.0`/`1.0` float pairs at `+0x20`/`+0x24`/`+0x28`/`+0x2C`, `0x3D3A29C7` at `+0x38`/`+0x3C`, `+0x40 = 0x15000000`, `+0x44 = 0x11000000`, `+0x4C = 0x50000001`, `+0x50 = 0x8000`, `+0x60 = 0x13000000`

Interior anchor `004DA3CF` (function `004DA3C0`).

`004C8280` (157 B) is the sibling initializer `0037E0F0` calls beside `004DA3C0`: `008631D0(rcx, 6)` then `+8 = 0x1000404`, `+0xC = 0x6C050032`, `1.0f` at `+0x18`/`+0x1C`/`+0x38`, `+0x20 = 0x10`, `+0x28 = 1`, `0x3E4CCCCD` at `+0x3C`, `0x80` at `+0x40`/`+0x44`/`+0x48`/`+0x4C`, `-0.5f` at `+0x50`, `+0x54 = 0x3F600000`, `+0x60 = 0x15000002`, `+0x64 = 0x13000000`

Interior anchor `004C828E` (function `004C8280`).

**Batch-164 additions — the `00259DF0` spawn and the `0037E0F0` initializer pair cite the boot subtree's shared machinery, and that machinery's far edges go live here (SWE2-EC7-164).**

- **ActorEntity — SERVICE (8 edges).** `0022A0B0` calls the actor-entity body `002368D0`, and the `0032E400` gate `00259DF0` uses is itself called from actor-layer bodies (`0032FCA0`/`00330310`/`003306E0` among them) — shared machinery consulted from that layer, not boot ownership.
- **Input — SERVICE (5 edges).** `0017D4C0` reaches input helpers `00198750`/`00253C70`-adjacent lanes, and `0022A0B0`/`0022B7E0` call `0035B270`/`0035E9A0` — the input layer's leaves inside the boot chain.
- **Resource — SERVICE (37 edges, one fan).** `0022A0B0`'s subtree calls resource-side bodies including this batch's `00259DF0` and `002DF9A0`, and `0017D4C0` reaches `001A11B0`/`001DB1E0` — the boot chain loads through the resource layer by design.
- **Save_Load_Settings — SERVICE (5 edges).** `0017D4C0` calls the save/settings initializers `001C1710`/`001C18A0`/`001C18E0`, and `001EDEC0` is called from that layer — the settings bank registers during the same subtree walk.
- **Script_VM_Native_Bridge — SERVICE (7 edges).** The pool/spawn helpers `0032E400`, `0032E620`, `0036C110` and the `00229EA0` sibling are also called from script VM / native bridge bodies (`0050DF70`/`0050DFE0`, `00354D00`) — shared machinery, not a crossing this page owns.

`004E3110` (155 B) is the third `0037E0F0` static initializer beside `004DA3C0`/`004C8280`: `008631D0(rcx, 5)` then the field block - `+8 = 0x1000404`, `+0xC = 0x6C02001E`, `+0x10 = 0x20`, `+0x14 = 0x40`, `+0x1C = 1`, `60.0f`/`2.0f`/`5.0f`/`0.5f` at `+0x20`..`+0x2C`, `0x15000000` at `+0x30`, qword `0x11000000` at `+0x34`, `0x50000001` at `+0x3C`, `32.0f` at `+0x18`, `0x8000` at `+0x40`, zero `+0x48`/`+0x58`, `0x13000000` at `+0x50`.

Interior anchor `004E311E` (function `004E3110`).

`004C7FE0` (146 B) is one of `0037E0F0`'s battery initializers - the same record family as `004D0880`'s `0x1000404` head: `008631D0(6)` registers the object, then a straight constant fill writes `+0x08 = 0x1000404`, `+0x0C = 0x6C050028`, `+0x10 = 4`, `+0x14 = 2`, `+0x1C`..`+0x58` zeroed, `+0x20`/`+0x34`/`+0x48`/`+0x5C` at 1.0f, `+0x50` = 100.0f, `+0x60` = 0x15000001 and `+0x64` = 0x13000000 - a defaulted presentation descriptor built at static-registration time.

Interior anchor `004C7FEE` (function `004C7FE0`).
- **Audio — CLIENT and SERVICE (18 edges).** 2 inbound (Audio bodies `003B99D0`, `003638B0` call page-cited `001EDDA0`, `00229EA0`); 16 outbound (page-cited `003B99D0`, `002628B0` call Audio bodies `00360B50`, `003636A0`, `00360DD0`). Substantive edges include `002628B0` calls `00360B50`; `002628B0` calls `003636A0`; `002628B0` calls `00360DD0`; `003B99D0` calls `003617B0`; the remaining edges run through shared helpers the page cites.
- **Developer — CLIENT (1 edge).** 1 inbound (Developer bodies `001C6320` call page-cited `001EBA40`). Substantive edges include `001EBA40` is called by `001C6320`.
- **Movement — CLIENT and SERVICE (9 edges).** 2 inbound (Movement bodies `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00) call page-cited `001EDDA0`, `001EDE80`); 7 outbound (page-cited `002628B0`, `001EDDC0` call Movement bodies `00337A00`, `003DAA20`, `00263560`). Substantive edges include `001EDDC0` calls `00337A00`; `001EDE80` is called by `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00); `002628B0` calls `003DAA20`; `002628B0` calls `00263560`; the remaining edges run through shared helpers the page cites.
- **Platform — CLIENT and SERVICE (2 edges).** 1 inbound (Platform bodies `001DD420` call page-cited `0017D8F0`); 1 outbound (page-cited `001EB190` call Platform bodies `005CD0A0`). Substantive edges include `0017D8F0` is called by `001DD420`; the remaining edges run through shared helpers the page cites.
- **RNG_Random_Selection — MECHANICAL (6 edges).** 3 RNG_Random_Selection-side calls into shared helper(s) the page cites (`RNG_MT19937_SeedState` (00866D60)); 3 calls from page-cited bodies into shared RNG_Random_Selection plumbing (`RNG_MT19937_Seed` (00379CF0), `RNG_MT19937_NextU32_Thunk` (00379CD0), `RNG_MT19937_SeedState` (00866D60)) - the helpers' general call surface, not a RNG_Random_Selection relationship of this page's subjects.
- **UI — CLIENT and SERVICE (22 edges).** 18 inbound (UI bodies `0024B9B0`, `003FA790`, `0035D6B0` call page-cited `001EDEC0`, `00229EA0`, `001EDDA0`); 4 outbound (page-cited `002507C0`, `00250540` call UI bodies `00367200`, `0035BC40`, `003C6000`). Substantive edges include `001EDE80` is called by `003FA790`; `00250540` calls `00367200`; `002507C0` calls `00367200`; `002507C0` calls `0035BC40`; the remaining edges run through shared helpers the page cites.
- **Party — SERVICE (3 edges).** 3 outbound (page-cited `002628B0`, `002695A0` call Party bodies `PartyFocus_ClearCurrentActorIfEligible` (00358B40), `PartyControl_SetMovementSuppressionBit` (00359200), `PartyFocus_ResetState` (003590E0)).
- **Application — SERVICE (1 edge; FABLE, 2026-10-03, §4a).** 1 outbound: page-cited `0017CEB0` (slot 2, the archive mount) calls the Application bootstrap body `0017D6B0` as its fifth call (`0017CEB0` + 0x50, I6), `0017CEB0` -> `0017D6B0`. The mount is this page's subject; what `0017D6B0` builds is open (§4a).
## Falsification pass 1 — 2026-09-29 (OPUS): the seeds and the budget hold; the frame base is not evaluated once

Every static claim was re-derived from the shipping image by
[`falsify_boot_fixups.py`](../../Tools/analysis-kit/gfz-scripts/falsify_boot_fixups.py), whose output is in
[`falsify_boot_fixups.out`](../../Tools/analysis-kit/gfz-scripts/falsify_boot_fixups.out). Killers first.

| check | killer searched for | result |
|---|---|---|
| B0 §2 | another caller of the boot fixer; another tail; another thunk or getter size | survives: `0022A0B0` ← `0017D4C0`; `0022BDF0` ends `jmp 001EDDC0`; `00379CF0` is a 5-byte `jmp 00863D30`; `0017D8F0` is 11 bytes |
| B1 I1 | another first-use or boot seed | survives: `mov edx, 0x1571` (5489) behind the `02EB4234` latch; `mov ecx, 0x11b9` (4537) before the boot reseed |
| B2 I2 | a third caller of the seed thunk; a missing step on the save-load path | survives: exactly `0022A410` and `005843D3`; before the latter, an import call (`_time64`), `imul …, 0x258` (×600) of `01FD4A80` and `btr ecx, 0x1f` |
| B3 I3 | a second writer of `02064ACC` | **refuted: "evaluated once" is false.** The setter `00229F10` is called by `002695A0` (from the area transition `002628B0`: `2 / FrameLimit` again) and by `0026DB10` (the verb `mainloopallsyncv`'s native: `arg / FrameLimit`, `2` for a negative argument) |
| B4 I4, I5 | another allocation or registration count; another total; a registration that is not size plus its fourth argument | survives: 11 allocations totalling 257.1 MiB and 9 registrations totalling 255.6 MiB; each registration's size plus its `0x10` / `0x100` / `0x400` argument is an allocated size |

**Why it was missed.** The page read boot's one division and stopped. The types store already listed both writers
(`FrameBaseConstant`: "written twice and read once"), but the contract never consulted it. I3 is corrected above,
[what the engine fixes at boot](what-the-engine-fixes-at-boot.md) carries the same correction, and `CON-158` records it.
The consumer record is [`boot-fixups-falsification-pass-1-0929`](../_index/candidates/boot-fixups-falsification-pass-1-0929/README.md).

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../_index/candidates/fable-contract-boot-fixups-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00259370` | 35 B | stores `ecx` zero-extended as qword `02098DF0`; when `ecx` is non-zero and the signed dword at `+4` of that zero-extended address is positive, stores dword 0 at `02098DF8` and tail-jumps at `00259370` + 0x1D with `rcx` unchanged; otherwise returns | `00259372`, `0025937D`, `00259383`, `0025938D` |

## Homed frontier bodies called from this page's functions (FABLE, 2026-10-02, cloud-drafted)

*Functions no page cited until now. Each is entered directly from a function this page already cites (the site is given as caller + offset). Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's homing pack and re-read by FABLE against the certified image; verified by [`homing_applier.py`](../_index/candidates/fable-home-contract-boot-fixups-1002/homing_applier.py): every site transfers to its function, the page cites the caller, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors |
|---|---|---|---|---|
| `004E7980` | 52 B | `0037E0F0` + 0x9B | calls `004E7980` + 0x13 with (`rcx`, the address `004E7D90`, 0), then stores 0x3000000 into dword `rcx+8` and 0x2000000 into dword `rcx+0xC` (original `rcx`) and tail-jumps (site `004E7980` + 0x2F) with `rcx+0x10` as `rcx` | Interior anchor `004E7989`; Interior anchor `004E7993`; Interior anchor `004E799C`; Interior anchor `004E79A3`; Interior anchor `004E79AF` |
| `004EB910` | 1387 B | `004EBE80` + 0x74A | increments word `02064DB8`; replaces each float pair (a,b) = (`02064BF0`,`02064BF4`) and (`02064C00`,`02064C04`) by (`02064D00`*a + `02064D10`*b, `02064D04`*a + `02064D14`*b), adds the new pairs to the first two floats of two copies of the 16-byte entry at index word `02064B0C` + 2 of the 0x10-stride table `02064E30` and stores the copies times 16 as truncated int32 vectors at `02064C60` and `02064C70`; when word `02064DBC` differs from word `02064B0C` it first subtracts `02064CF0`/`02064CF4` times `02064C80` from both float pairs; then adds `02064CF0`/`02064CF4` times `02064B60` (first pair) or `02064B64` (second) and subtracts `02064B30`/`02064B34`; every pair update (to `02064C10`/`02064C14` or `02064C20`/`02064C24`) is followed by a call when either float is 0, one when either is negative and one always (`004EB910` + 0x231/0x252/0x257, 0x29A/0x2B9/0x2BE, 0x38F/0x3B0/0x3B5, 0x3F8/0x417/0x41C); finally maps x to x*`02064BA0` + `02064B90` and y to y*`02064BA4` + `02064B94` in both pairs, sets floats `02064C18`, `02064C28` to ~~1.0 (`01E0283C`)~~ the sum of the `.data` floats `01E02838` + `01E0283C` (file values 0.0 and 1.0) *(corrected 2026-10-03, FABLE, on SWE2-AUDIT-SPEC's review: `004EBD39` / `004EBD44` load and add the two cells, `004EBDD6` / `004EBDDE` store the sum)*, copies `02064C10`, `02064B70`, `02064C60`, `02064C20`, `02064B80`, `02064C70` to six entries from index word `02064DB4` and adds 6 to it | Interior anchor `004EB94A`; Interior anchor `004EBAE2`; Interior anchor `004EBB41`; Interior anchor `004EBDF5`; Interior anchor `004EBE69` |
