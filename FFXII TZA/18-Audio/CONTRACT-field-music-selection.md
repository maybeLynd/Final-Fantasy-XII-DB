---
contract: Field music selection — which track plays in an area, given story progress
category: 18-Audio
scope: operation
level: L2   # calculation parity only; INTEGRATION untested, so not L3
readiness: DIFFERENTIAL TESTED
confidence: PROVEN
implements: how-the-music-changes-when-you-change-area.md
entries: [003EAA70, 00265270]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 32 addresses cited - 3 data, 14 entry, 15 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-10
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-field-music-selection-pass-1  # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — field music selection

> **The database's second behavioural contract, and the first that is a pure function.** It takes a
> field id and the story-progress variable and returns a track id, touching no allocation, no RNG and
> no thread state. **That makes it the first entity in the program that could be reimplemented and
> calculation-parity tested without the game running** — see §16 for exactly how far that goes.
>
> Formalises [`how-the-music-changes-when-you-change-area.md`](how-the-music-changes-when-you-change-area.md),
> whose structural claims were re-derived from the binary for this contract and **all confirmed**.

## 1. Purpose

Chooses the background track for an area. The same field entered at two points in the story plays
different music, and this is where that is decided — not by a script, but by a small authored ladder
attached to the area, keyed on one story-progress number.

## 2. Interface

| | |
|---|---|
| entry | `003EAA70` (229 B) |
| convention | MS x64 |
| parameter | `ecx` — `int fieldId` |
| returns | `eax` — `int trackId`, or **`-1`** |
| reads | `FieldData_GetVariable0` (`00265270`) for the progress value; the table pointer at `0x02B5E0D0` |

**`-1` is the only failure value and it means four different things** — field id out of range, no page,
no covering run, or a resolved track of `0`. **The caller cannot distinguish them**, which is a real
constraint on any reimplementation that wants to log why an area went silent.

## 3. Types

```c
struct MusicTable {              /* pointed to by *(void**)0x02B5E0D0 */
    int32_t  unknown_00;         /* +0x00  read by nothing on this path */
    int32_t  maxFieldId;         /* +0x04  inclusive upper bound */
    uint32_t page[];             /* +0x08  one 32-bit word per 128 field ids: ABSOLUTE once rebased */
                                 /* the reader may select page maxFieldId/128; the callback rebases */
                                 /* (maxFieldId+127)/128 pages - one fewer when maxFieldId is a     */
                                 /* positive multiple of 128 (MC-5, 2026-09-27 (OPUS, on ASTRA's musicctrl-page-boundary)) */
};

struct MusicRun {                /* variable length; runs are chained within a page */
    uint16_t packed;             /* +0x00  start = packed & 0x7FF, len = packed >> 11 */
    uint8_t  count;              /* +0x02  number of ladder entries */
    uint8_t  defaultTrack;       /* +0x03  used when no entry is passed */
    struct { uint16_t threshold; uint8_t track; } entry[count];   /* +0x04, 3 bytes each */
};                               /* next run = this + 4 + 3*count */
```

**Page entries are absolute addresses after load, not offsets — but table-relative on disk** —
the load callback `003EAB90` walks the page words and adds the low 32 bits of the table's own
address to each non-zero entry (`add ecx, r9d` at `003EABBE`, `movsxd` count from the header);
the reader's `movsxd rax, dword [r8 + page*4 + 8]` then sign-extends the rebased value, so the
table can only live in the low 2 GB. (Corrected 2026-09-25, OPUS-REQ-CONTRACT-THREE-STATE-CORRECTIONS-BLOCK-214.)

**The 11/5 bit split caps the format**: a run covers at most **32** consecutive field ids and no field
id above **2,047** is representable.

## 4. Preconditions · postconditions · invariants

**Preconditions.** `*(void**)0x02B5E0D0` must be non-NULL — **the function does not check it** and
will fault if the table has not been populated. Everything after that is validated.

**Postconditions.** Returns a track id in `1..255`, or `-1`. **No state is written; the object graph
is unchanged.**

**Invariants.**
- Runs within a page are **ordered by `start`**, and the walk relies on it: `start > fieldId` ends the
  search immediately.
- Ladder entries are **ordered by threshold**, and the walk takes the **last one passed**.
- `trackId == 0` can never be returned; it is folded to `-1` by a `cmove`.

## 5. State

| | detail |
|---|---|
| **read** | `0x02B5E0D0` (the table pointer), the table, the page, the run chain; `FieldData_GetVariable0`'s value |
| **written** | **nothing** |
| **allocated / deallocated** | **none** |

## 6. Relationships

**Callees:** `FieldData_GetVariable0` (`00265270`) — the only call, made **first**, before any
validation. **Callers:** not traced by this contract (`DG-4`).

## 7. State transitions

**None.** This is a query.

## 8. Script · resource · event interactions

The progress value is the first `u16` of the current field's authored variable block — the same number
the persistent flag banks compare against, through the same threshold-ladder idiom. **One authored
number drives both systems.**

## 9. Determinism

**RNG:** none in the local lookup. With fixed, valid table/progress inputs, the scalar result
has no frame parameter. Caller scheduling, concurrent input changes and allocation lifetime are
not established by that fact. The body reads shared state without synchronization; being a reader
does not by itself prove safety against a concurrent writer or release.

## 10. Failure paths and edge conditions

| condition | result |
|---|---|
| `fieldId > table->maxFieldId` | `-1` |
| page entry is `0` | `-1` |
| first run's `start > fieldId` | `-1` — runs are ordered, so this means "past it" |
| run chain exhausted without covering `fieldId` | `-1` |
| covering run found, `count == 0` | `defaultTrack` (or `-1` if that is `0`) |
| resolved track is `0` | **`-1`** — silence, indistinguishable from "not found" |
| progress `> 0x7FFF` | reads **negative**; no threshold is passed; `defaultTrack` stands |

**The progress value is fetched before the bounds check**, so an out-of-range field id still costs the
call to `00265270`.

## 11. Observable behaviour

The track that plays on entering an area, and the fact that it changes at story beats without any
script running. **A field whose run resolves to `0` is silent rather than falling back to anything.**

## 12. Reproduction formula

```c
int FieldMusic_Select(int fieldId)
{
    int16_t progress = (int16_t)FieldData_GetVariable0();     /* signed, 16-bit */
    MusicTable *t = *(MusicTable **)0x02B5E0D0;

    if (fieldId > t->maxFieldId) return -1;

    int page = fieldId >> 7;                    /* arithmetic: (fieldId + (fieldId>>31 & 0x7F)) >> 7 */
    uint8_t *run = (uint8_t *)(intptr_t)(int32_t)t->page[page];
    if (run == NULL) return -1;

    for (;;) {
        unsigned packed = run[0] | (run[1] << 8);
        unsigned start  = packed & 0x7FF;
        unsigned len    = packed >> 11;
        unsigned count  = run[2];
        if (start > (unsigned)fieldId)          return -1;    /* ordered: overshot */
        if (start + len >= (unsigned)fieldId)   break;        /* covers it */
        run += 4 + 3 * count;
    }

    int track = run[3];                          /* the default */
    uint8_t *e = run + 4;
    for (unsigned i = 0, n = run[2]; i < n; i++, e += 3) {
        uint16_t threshold = e[0] | (e[1] << 8);
        if (progress <= threshold) break;         /* stop at the first not passed */
        track = e[2];                             /* otherwise take it and continue */
    }
    return (track == 0) ? -1 : track;
}
```

**Note the two extensions of the progress value**: it is **zero**-extended from the 16-bit return at
`003EAA84` and **sign**-extended at `003EAB10`, immediately before the ladder. The comparison is
therefore **signed 16-bit against a zero-extended `uint16` threshold** — which is why a progress above
`0x7FFF` passes nothing.

**The coverage test is `start + len >= fieldId`, not `>`** — a run with `len = 0` still covers exactly
`start`.

## 13. Runtime validation

**Bounded captures exist; producer and integration evidence remain incomplete.**
[`EXP-008`](../_experiments/EXP-008-the-real-music-table.md) captured the table's contents.
The earlier claim that this answered `DG-1` is withdrawn: no writer or lifetime was observed.

`*(void**)0x02B5E0D0` resolves to a `MUS0`-tagged buffer: **max field id 1311, exactly 11 page
pointers** (`ceil(1312/128)`), **no empty page, and 291 runs — not the 316 first recorded here.**
The correction is FABLE's (`FABLE-REQ-OPUS-MUSIC-CONTRACT`, `ec57443`): a **page-bounded** walk of the
extracted file gives 291, and `EXP-008`'s walk ran past page ends, counting bytes beyond a page's own
chain as further runs. **I have not reproduced the count** — the extracted `musicctrl.bin` is not in
this repository — so it is recorded on FABLE's corpus evidence, not re-measured here. Everything below
that rests on *parsing* rather than on the total is unaffected. It parses cleanly under the format §3
documents, and every page's chain ends above its own top field id — a property this project first
inferred from a *crash in a synthetic table* and then observed in the real one.

The differential was run over that data: **400 cases, 112 resolving a track, 288 resolving `-1`, 35
distinct tracks, 0 mismatches**, plus a no-state check in which **80 of 400 cases re-read the whole
table image and the table pointer afterwards and 0 showed any byte changed** — which is §5's *"writes
no state"* checked in isolated execution over captured data, not a live no-write observation.

**Reproduced 2026-09-08 on a fresh launch with the table at `651C9FC0`**, where `EXP-008` had it at
`653B0FC0`. Identical counts at a different allocation base, which matters because the `page[]`
entries are absolute and `EXP-008`'s own finding was a driver bug in placing them.

**The game has also been used as the oracle**, in
[`EXP-009`](../_experiments/EXP-009-the-games-own-answer.md): hardware breakpoints on this function's
entry and exits while two saves were loaded, **126 entry->exit pairs per run with 0 unpairable
rows**, and for both areas the game, the emulated shipped bytes and the reconstruction returned the
same track — field 227 -> 100, field 253 -> 20. The inputs were the game's, the table was the game's,
and the answer compared against was **the game's own return value**, not an emulator's.

**`INTEGRATION` remains untested.** The reconstruction runs in a driver, and substitution
through the native caller has not been exercised. That is not the only remaining requirement:
table production, binding/lifetime, shared-state stability and scheduling consequences need
appropriate evidence. The preserved traces contain 252 pairs over exactly two input conditions,
not 252 states, and no frame or time columns. See EXP-009's dated correction.

### 13a. The callee executed, and a corroboration worth recording as one — 2026-09-18 (OPUS, consuming SWE2-ORACLE's EXP-099)

`00265270` — `FieldData_GetVariable0`, this function's **only** call (§4) — had been modelled
everywhere it appears here. EXP-099 ran it as shipped bytes alongside `003EAA70`, **22/22 cases and
10/10 mutants killed, zero stubs**. That is an evidence-class change for the callee and nothing else:
`INTEGRATION` is still untested and the table-production, binding and lifetime requirements in §13
are untouched.

**Seven of its eight findings corroborate sections that already say the same thing**, several at the
same instruction addresses this contract already cites, and that is recorded as corroboration rather
than rewritten as news:

| EXP-099 finding | already in this contract |
|---|---|
| bound check refuses `[tab+4] < arg`, `arg == bound` proceeds | §3's *"inclusive upper bound"* |
| page index is a biased signed `arg/128`, pointer sign-extended, null → −1 | §3's absolute-address note |
| run coverage inclusive at both ends | §12: ***"The coverage test is `start + len >= fieldId`, not `>`"*** |
| ladder takes the last threshold passed, equal stops | §12's `<=` walk |
| result 0 maps to −1 | §10 |
| stride `4 + 3·count` | §15, `PROVEN`, at `003EAACB`/`003EAACF` |
| the 11-bit start carries values ≥ `0x400` | §3's 11/5 split and its 2,047 cap |

Re-read from the image while checking: `003EAAB6`–`003EAABB` splits the first two bytes into
`start = packed & 0x7FF` and `len = packed >> 11`; `003EAAC1 cmp ecx, ebx` / `ja` refuses only when
`start > arg`; `003EAAC5 add ecx, edx` / `003EAAC7 cmp ecx, ebx` / `003EAAC9 jae` takes the run
whenever `start + len >= arg`; and `003EAACB lea edx, [r10 + 2]` / `003EAACF lea edx, [r10 + rdx*2]`
computes `3·count + 4`. All as documented.

#### What is genuinely new, and it is a composition result

**The callee's own refusals arrive as progress `0`, not as a refusal.** ~~A dead actor
(`liveness & 1 == 0`)~~ A clear bit 0 in ActorManager slot 0's flag byte (`02098E20`, `ActorManagerSlot +0x10`, the
slot-live bit) or a null variable-bank pointer (`02098E58`, slot 0 `+0x48`) makes `00265270` return zero, and **the ladder still
runs** — zero compares `<=` any threshold, so the run's `defaultTrack` is what comes back. *A field
whose music depends on story progress therefore plays its default track ~~for a dead actor~~ while manager slot 0 is not
live or has no variable bank, rather than selecting nothing.*

> **Corrected 2026-09-27 (OPUS, on ASTRA's field-music-gate-scope).** `00265270` takes no actor argument and has no health, death or actor
> operand in its 28 bytes: it tests the fixed global `02098E20` bit 0 and reads the fixed pointer `02098E58`. EXP-099's
> case named `dead-actor` writes that flag to 0 in supplied state; it executes no death. So the supported statement is
> *gate off or null bank → getter 0 → the run's default track*. Whether an actor's death ever clears that slot bit, and
> whether the default track is then heard, are **not established** here - neither observed nor excluded. The gate and
> ladder results, the 22 cases and 20 mutants stay as recorded. Regression:
> `_experiments/evidence/field-music-gate-scope/check.py` (ASTRA; four corrupted-derivation controls, one of them an
> actor-pointer substitution for the fixed global). Neither half of that is visible from either function alone, which is why it took
the composition to see it.

**And the sign mechanism behind §10's `> 0x7FFF` row is now pinned rather than inferred:** the `u16`
is zero-extended at the callee's return and **`movsx`'d at `003EAB10`** before the ladder compares
it, so `0x8000` and above enter the comparison negative and pass no threshold. `m-movsx` flips
exactly that and dies.

*Method note for the experiment record: finding 8 already carries its own address correction — the
`0x7FF` mask patch site moved from `0x3EABBE` to `0x3EAABE`, the immediate's second byte. That is the
same convention as EXP-093's and EXP-098's mutation tables, where the sites named are patched BYTES
rather than instruction boundaries.*

<!-- OPUS-MUT-S13-RESTATE -->
### Mutation surface, checked 2026-09-12 — unchanged, no re-run owed

**Recorded as UNCHANGED, 2026-09-12 (`OPUS-CONTRA-MUTATION-LIT-SUFFIX`).** The generator defect that made every pre-2026-09-12 mutation count a floor — a literal pattern that could not match a `u`, `U`, `l`, `L` or `f` suffix — does not affect this pilot: re-measuring its `.c` and `.h` with the corrected pattern gives the SAME surface, so its published campaign was already complete and no re-run was owed. `quality_preset` is the other pilot in that position.

## 14. Unresolved

1. ~~**What populates the table**~~ — **ANSWERED 2026-09-11 (`DG-1`)**, by FABLE and verified here
   against the image. The chain is `00379D20` → `003EAB60` → `0051ED10(9, 0x20, 003EAB90)`, loading
   **`in/common/musicctrl.bin`**, and `003EAB60` **stores the result into `02B5E0D0`** — the very
   pointer §13 dereferences. Read at `003EAB64`–`003EAB78`: `edx = 0x20`, `r8 = 003EAB90` (the rebase
   callback), `ecx = rdx - 0x17` which is **9**, then `mov qword ptr [rip + 0x2773551], rax` resolving
   to `02B5E0D0`. So the table is a **file**, and this contract's "nothing on this path writes it" was
   true of this path and misleading about the system.
2. ~~**What a track id indexes** — a number is returned; the sound bank it selects is not established
   (`DG-2`). **Still open.**~~ **ANSWERED 2026-09-11 (`DG-2`)** on [the area-music page](how-the-music-changes-when-you-change-area.md), section *DG-2 answered*:
   the id names `musicNNN.win.mab`, and the flag table is `musicinfo.bin`. *(This item was not updated when the answer landed; corrected 2026-09-14, FABLE.)*
3. ~~**Whether any shipped run uses more than one ladder entry**~~ — **ANSWERED (`DG-3`)**: **48 of
   the 291 runs carry a ladder**. FABLE's count over the extracted file; not re-measured here. The
   ladder is exercised by a sixth of the data, not a vestige.
4. ~~**Who calls `003EAA70`**~~ — **ANSWERED (`DG-4`) and verified here from the call graph**: exactly
   four callers — `ActorManager_RunFieldRuntimePass` (`0025D9E0`, site `0025DBC1`), `00261F90`
   (`00262034`), `0026DE20` (`0026DE4C`) and `0026DEF0` (`0026DEF6`).

## 15. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| Signature and return convention | body `003EAA70` disassembled whole | 1 | PROVEN |
| Table layout, page stride 128, absolute page addresses | `sar eax,7` at `003EAA96`; `movsxd rax, dword [r8+rcx*4+8]` at `003EAA9C` then immediate deref | 1 | PROVEN |
| Run header 11/5 split, stride `4 + 3*count` | `and 0x7FF` / `shr 0xB` at `003EAABB`/`003EAAB8`; `lea edx,[r10+2]` / `lea edx,[r10+rdx*2]` at `003EAACB`/`003EAACF` | 1 | PROVEN |
| Ladder takes the last threshold passed | `cmp r11d,ecx / jle` at `003EAB2C`/`003EAB2F` then `movzx r9d, byte [rax+2]` at `003EAB31` | 1 | PROVEN |
| **What fills the table** | `in/common/musicctrl.bin` via `0051ED10(9, 0x20, 003EAB90)`, stored to `02B5E0D0` at `003EAB78` | 1 | PROVEN |
| **The four callers of `003EAA70`** | call graph, four edges, each site cited in §14.4 | 1 (static) | PROVEN |
| 291 runs, 48 with a ladder | FABLE's page-bounded walk of the extracted file (`ec57443`) | 1 (corpus) | **not re-measured here** |

**The loader is shared by exactly three authored files, and one of them is not rebased.** `0051ED10`
has three callers image-wide, and `00379D20` calls all three:

| site | kind | file id | rebase callback | table pointer |
|---|---|---|---|---|
| `003EAC40` | 9 | `0x1F` | `003EAC70` | `02B5E0D8` |
| `003EAB60` | 9 | `0x20` | `003EAB90` — **this contract's** | `02B5E0D0` |
| `00473D20` | 9 | `0x21` | **`0016D6A0`** | `02CA6C60` |

All three pass **kind 9** — each computing it from a different `lea` off the size register, which is
the compiler reusing `edx`, not three different values. The third's callback is `_guard_check_icall`,
a bare `ret` in this build, so **file `0x21` is loaded and deliberately not fixed up**: its contents
carry no addresses to rebase. The two that are rebased use the same loop shape — walk `[table+8]`
entries from `table+0xC` adding the block base to each word (`003EAC82`, and `003EAB90`).

Naming files `0x1F` and `0x21` is semantic and is FABLE's; what is established here is that the
rebase-or-not decision is **per file, at the call site**, and a reimplementation that applies one
policy to all three corrupts one of them.

**The page addresses are rebased on load, and that is why they are absolute at runtime.** The loader's
callback `003EAB90` adds the block's address to each page word (`page[i] += (u32)block`), and the
reader sign-extends on use (`movsxd rax, dword [r8+rcx*4+8]`). A reimplementation that stores the file
words unmodified and then dereferences them reads from near zero; one that rebases twice reads from
twice the block. This is the same hazard the authored-table registry has at its `+0x0C`.
| Track `0` folds to `-1` | `test r9d,r9d / cmove r9d, eax` at `003EAB45`/`003EAB48` with `eax = -1` from `003EAB42` | 1 | PROVEN |
| Progress is compared as **signed 16-bit** | `movzx` at `003EAA84`, `movsx r11d, r11w` at `003EAB10` | 1 | PROVEN |
| Writes no state | no store to any non-stack operand in the body `003EAA70` | 1 | PROVEN |
| Who writes and binds the table at runtime | one writer of `02B5E0D0` image-wide — the load path `0051ED10(9, 0x20, 003EAB90)` stores the block at `003EAB78`, so the table has one writer ~~and is **bound once per process**~~ (*Qualified 2026-09-27 (OPUS, on ASTRA's musicctrl-binding-provenance): the binder has no guard and the framework's dispatch count of its init job is not established; see MC-1*) (FABLE-MUSICCTRL-BGMSTREAM, DG-1 answered); the row above names the file, this one the writer — they were one claim string until 2026-09-12 (OPUS-CONTRA-FIELDMUSIC-S15-DOUBLE) | 1 | PROVEN |
| The table's lifetime after binding — release, reload on a language change, reuse of the block | **UNKNOWN / NOT EXERCISED.** EXP-008 observes MUS0-tagged contents at a capture point; a captured input cannot exercise its producer, and no release of the block was read | — | UNKNOWN |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

### "Writes no state", exhaustively — and a `nop` is not a write

`003EAA70` is 229 bytes / **73 instructions**. Every instruction whose destination is memory:

* **0** stack writes,
* **0** real stores anywhere else,
* and **2** instructions my detector flagged before I read them — `nop dword ptr [rax]` and
  `nop dword ptr [rax + rax]`, the multi-byte alignment NOPs, which **write nothing at all**.

**The claim holds exactly.** The `nop` artefact is the fourth trap of this shape in the sweep — after
`test` counted as a store, `r8` ceasing to be the third argument, and a `bswap` open-coded as
shift-and-mask. **An instruction is not its operand shape**, and a detector keyed on "first operand is
memory" will call a padding NOP a write every time.

### The arithmetic and the comparisons, read where they stand

| claim | image |
|---|---|
| page stride 128 | `003EAA96 sar eax, 7` |
| run header **11/5** split | `003EAAB8 shr edx, 0xb` / `003EAABB and ecx, 0x7ff` — and the identical pair again at `003EAAE9`/`003EAAEC` |
| track `0` folds to `−1` | `003EAB48 cmove r9d, eax` |
| progress is compared as **signed 16-bit** | `003EAA84 movzx r11d, ax` loads it zero-extended, and `003EAB10 movsx r11d, r11w` **re-extends it as signed** before the comparison |

That last pair is the interesting one: the value is widened **twice, in opposite senses** — zero-
extended when read and sign-extended before it is compared. A reconstruction that kept the first
widening and skipped the second would agree on every non-negative progress value and diverge on
exactly the ones the ladder exists to order.

### One writer image-wide

A whole-image scan of `02B5E0D0`: **1 writer** — `003EAB78 mov qword [rip → 02B5E0D0], rax`, inside
`003EAB60`, the load path §15 names — and **2 reading functions**. The binding really is
single-sourced.

### `0016D6A0` again, in a third subsystem

§14.4's site table gives `00473D20`'s rebase callback as **`0016D6A0`** — the same three-byte `ret 0`
this sweep found standing in for an absent verb-dispatch callback and for the save-image clear's tail
jump. **Three unrelated subsystems share one no-op stub**; a reconstruction that gives each its own
would triple a function the engine has once.

**Not claimed:** the 291/48 run census is FABLE's and was **not re-measured here**; the table's
lifetime after binding stays `UNKNOWN / NOT EXERCISED`.

## 16. Parity plan

**Testable today, without the game — and this is the first contract for which that is true:**

- **`CALCULATION` parity.** The formula in §12 is a pure function of `(fieldId, progress, table)`.
  Build synthetic tables, run both implementations, compare. **Every branch in §10 is reachable from
  a hand-built table**, including the `len = 0`, `count = 0`, `track = 0` and `progress > 0x7FFF`
  cases.
- **`STRUCTURAL` parity** against the layout in §3.
- **`EDGE-CASE` parity** for the four distinct routes to `-1`.

**Requires further original-game evidence:** the table producer and lifetime (`DG-1`),
caller/state/scheduling behavior, and native substitution with observed consequences. EXP-008
provides captured input bytes; EXP-009 provides two input/return conditions. Neither closes
these remaining requirements. The former claim that nothing remains blocked on knowledge is
withdrawn.

> **The distinction that must not be blurred:** passing calculation parity on synthetic tables proves
> **the algorithm** is reimplemented correctly. It says nothing about whether the reconstruction picks
> the same track as the shipped game, because that depends on data this contract cannot reach. **A
> parity claim from synthetic tables alone must say "algorithm, not data".**

**Local fixed-input scope:** `RNG`, `TIMING`, `SERIALIZATION`, `STATE-TRANSITION` are not
exercised dimensions of this scalar lookup. This does not establish caller scheduling, table
lifetime or integrated transition behavior.

## 17. Implemented and differential-tested — 2026-09-08

**Reconstruction:** [`../../../Reconstruction/Game/Audio/field_music.c`](../../../Reconstruction/Game/Audio/field_music.c)
**Test:** [`../../../Reconstruction/Tests/Differential/diff_field_music.py`](../../../Reconstruction/Tests/Differential/diff_field_music.py)

**Result: 1,200 cases over 20 synthetic tables, 0 mismatches** — 575 resolving a real track, 625
resolving `-1`.

**The reference side is the shipped machine code**, not a second reading of the disassembly: the 229
bytes at `003EAA70` are mapped at their real virtual address and executed under Unicorn, with
`FieldData_GetVariable0` stubbed at its own address as `mov eax, imm32 ; ret`. Both sides receive the
same table image at the same base, which §3 makes mandatory — the page entries are absolute addresses.

### Two things the test had to be fixed to be worth anything

**The first run crashed the driver with an access violation**, and the cause is a property of the
format worth recording here: **there is no chain terminator.** The walk ends only when a run's `start`
exceeds the query, so a page whose chain stops short runs on into whatever follows it in memory. The
shipped data must therefore always end a page with a run whose `start` is above every field id that
can reach it. **A generator that does not do the same produces crashes rather than test failures** —
which is how this was found.

**The first green result was weak and was not reported as a pass.** 313 of 396 cases resolved `-1`,
so "0 mismatches" was mostly two implementations agreeing on the same *failure*. Biasing field ids
toward spans a run actually covers moved the split to 575/625, and only then was the result
meaningful.

### ⚠ This entity skipped two rungs of the ladder, deliberately

`readiness` moves from `CONTRACT READY` to **`DIFFERENTIAL TESTED`**, passing over `RUNTIME
VALIDATED` and `RECONSTRUCTION READY`. That is not an oversight and it should not become a precedent
by accident:

> **For a pure function with an emulatable reference, running the original's own bytes substitutes
> for runtime validation *of the algorithm*.** There is no state, no ordering and no RNG for a live
> process to reveal that emulation does not already show.
>
> **It substitutes for nothing about the data.** *(Written when the real table was unread. It has
> since been read and the reconstruction run against it — `DG-1`, `EXP-008`, and §13 above. The
> shortcut's logic stands; its example no longer does.)* `INTEGRATION` parity remains **untested — though no longer untestable**, since `EXP-009`
> demonstrated the game can be used as an oracle for this function. **An entity with state, timing or RNG cannot take this
> shortcut** — for those, the ladder's ordering is load-bearing.

### Parity status, by dimension

| dimension | status |
|---|---|
| `CALCULATION` | **PARITY over synthetic tables** — 1,200 cases, 0 mismatches |
| `STRUCTURAL` | parity — the layout in §3 drives both sides |
| `EDGE-CASE` | parity — all four routes to `-1`, plus `len = 0`, `count = 0`, `track = 0`, `progress > 0x7FFF` |
| `INTEGRATION` | **NOT TESTED** — captured bytes and two input/return conditions do not prove native substitution, producer/lifetime, state-transition or scheduling consequences |
| `RNG`, `TIMING`, `SERIALIZATION`, `STATE-TRANSITION` | not applicable |

**Known intentional divergence, excluded from comparison:** a NULL table pointer faults in the
original and returns `FIELD_MUSIC_NONE` in the reconstruction. The test names it in its output rather
than skipping it silently.

## CORRECTED 2026-09-10 — captured contents are not producer evidence

ASTRA-ORACLE-SCOPE withdraws the EXP-008-derived 8/8 contract coverage claim and the statement
that substitution was the whole remaining integration gap. The source map now marks the producer
row NOT EXERCISED (7/8), preserving it in the denominator. The known table contents and two
captured return conditions remain supported at their recorded scope. Neither capture supplies
producer, ownership or frame-scheduling evidence. Historical numerical results and raw files
are retained. Operation calculation readiness does not promote subsystem or integration readiness.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL.*

The field-music selection cites shared lookups, and nearly all of this page's crossings are their other callers:

- **CombatFormula, CombatAction and Movement — MECHANICAL.** `BattleStats_FindOwningBattleUnit` (`0031B860`) has dozens
  of CombatFormula callers, including `BattleFormula_ApplyTargetResult`, `BattleStats_ModifyHPAndProcessLethalState`
  and the roll functions. It also has four CombatAction callers, among them the target-preview functions, and two locomotion callers.
- **CombatAI, CombatAction, CombatFormula, Movement, Presentation and Spawn_Encounter_Lifecycle — MECHANICAL.** The
  selector lookup `BattleUnit_FindMappedDefinitionSelectorByIndex` (`0031B810`) is also read by:
  - `AiOrder_EvaluateTargetSelector` and `AiOrder_BuildCandidateTargetBufferFromStored…`;
  - `Battle_BuildActionTargetSet` and `BattleUnit_IssueCommandByFocusHandlesWithOpt…`;
  - `PartyFollow_SolveFormation`;
  - `PartyCombat_UpdateStanceState` and `BattleUnit_BroadcastPartyCombatTargetRelatio…`;
  - `Spawn_ValidateCandidateDistanceToPlayers` and `SpawnLifecycle_CheckAndRetireByNativeRange`.
- **PlatformOnlineAchievements, Presentation and CoreRuntimeScheduling — CLIENT.** `FieldData_GetVariable0` (`00265270`)
  is also read by two achievement-side bodies (308 B and 367 B), the debug-menu renderer, and a 2,232-byte core body.
  The boot initialiser (978 B) calls `00379D20`.
- **Movement — SERVICE.** The field runtime pass `ActorManager_RunFieldRuntimePass` (`0025D9E0`) runs
  `WorldActor_UpdateRuntimeAndScriptExecutionState`.

These are the lookups' other clients.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Gameplay — SERVICE.** `0025D9E0` on this page calls `FUN_00234150`, owned by that layer. What it reaches is a 104-byte registration helper that takes the `.text` address `002FED60` as a callback and gates on `byte[+0] & 0x10` of what `0031B810` returns; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Items_Equipment_Shops_License — CLIENT.** `Inventory_QueryOwnedCountIncludingReservedActionItems`, owned by that layer, calls `0031B810` on this page. That caller is the owned-count query for an item id, which returns `-1` for the sentinel id `0xFFFF`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Party — SERVICE.** `0025D9E0` on this page calls `PartyFocus_GetCurrentPackedActorHandle`, owned by that layer. What it reaches is a seven-byte getter returning the packed handle at `022C7FE0`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Rewards_Progression_Economy — CLIENT.** `Reward_ComputeExperienceForRecipient`, owned by that layer, calls `0031B810` on this page. That caller is the experience computation for one recipient: it needs `byte[rec+5] == 0` and takes its context from `0031B860`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).
