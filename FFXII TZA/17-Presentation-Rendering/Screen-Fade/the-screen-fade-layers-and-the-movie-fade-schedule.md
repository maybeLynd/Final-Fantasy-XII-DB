---
system: The screen-fade layers — seven fade records, the fade verbs, and the per-movie fade schedule behind registry slot 0
category: 17-Presentation-Rendering
status: AUDITED
owner_layer: CodeDomain — Presentation.ScreenFade
evidence_tier: 1
registry_slots:
  - "0x02EBF008"
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 168 addresses cited - 17 data, 88 entry, 59 interior, 3 literal, 1 text-data, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-13
author: FABLE
corpus_validated: "battle_pack.bin us directory entry +0x118 (st2e, stride 8, 49 rows) dumped whole; every .text reference to 022BDD60-022BDEB8 and to 02EBF008 listed; the verb table rows 00B6-00B8, 00D0-00D2, 008D, 0268-0269"
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-screen-fade-pass-1 - the schedule re-extracted and its st2e header declares count 49 stride 8, byte +0 is the row index in 49 of 49, and the four specific row sets reproduce exactly; NEW: the section is byte-identical in all nine languages; CORRECTED: '1E 1E 3C 3C' is 11 of 49 not most, the six 'instant fade-in' ids have fadeInLength 0 and so do not fade in at all, the all-zero list misses row 0, flags 2 never occurs, and the _d0/_d1/_d2 variants are three FURTHER handlers with arity 2 while 00B6-00B8 have arity 1
  crossref_clean: true
---

# The screen-fade layers — seven fade records, the fade verbs, and the per-movie fade schedule

> **Every fade to black or white the game shows is one of seven 48-byte records at `022BDD60`,
> started by one function, `002EFA70(layer, frames, direction, white)`.** The script verbs
> `fadeout` / `whiteout` / `fadein` are thin wrappers on it, field transitions and the cutscene
> skip call it directly, and movies fade through a 49-row schedule bound at registry slot 0.

## 1. What the player sees

The screen going black between areas, the white flash of a summon, the fade a movie opens and
closes with, the instant cut to black when a cutscene is skipped. All of it is a layer record
being started with a colour and a frame count, then polled to completion once a tick.

## 2. Native mechanism

### 2.1 The records

Seven records of 48 bytes at `022BDD60` (`layer × 0x30`; every accessor clamps the layer to
`0..6`, e.g. `002EFA90`–`002EFAA1`). Read from `002EFA70`, `002EF910` and the small accessors:

| offset | what |
|---|---|
| `+0x00` | the **effect handle** the layer owns — `0x80000000 \| counter`, from `00375900` (below); 0 when free |
| `+0x04` | state: 0 free, **1 running** (set when the handle came back non-zero, `002EFCE7`), **2 finished** (`002EF977`) |
| `+0x05` | direction — the `direction` argument (`002EFC8D`): 1 = fade **in** (to the scene), 0 = fade **out** (to the colour) |
| `+0x08`–`+0x2F` | the ~~0x28-byte~~ descriptor handed to `00375900`, which copies `0x68` bytes from `+0x08`, into the next records *(corrected 2026-10-02, OPUS: `00375900`+0xC9..+0x101)*: `+8 = 1`, `+9` two nibbles from ~~`022BDD57`~~ `022BDEB4` (low) and `022BDD5D` (high) (`002EFC85`–`002EFCC9`), `+0xA = 1`, `+0xB` = byte ~~`022BDD5B`~~ `022BDEB0` *(corrected 2026-10-02, OPUS: `002EFA70`+0x20B and +0x225 for `+0xB`, +0x215 and +0x244 for `+9`)*, `+0x24` flags (bit 0 = direction 1), **`+0x28`–`+0x2B` the colour**, `+0x2C = 2 × frames` (`002EFAF3`, `002EFCB0`) |

**The colour** (`002EFBD5`–`002EFC6F`): when the one-shot byte ~~`022BDD58`~~ `022BDD5C` is set, the four bytes
~~`022BDD59`–`022BDD5C`~~ `022BDD58`–`022BDD5B` *(corrected 2026-10-02, OPUS: `002EFE10`+0x0 `mov byte ptr [022BDD5C], 1`, +0x7..+0x1A the four colour bytes; `002EFA70`+0x165 tests `022BDD5C`)* are copied in and the byte cleared — a scripted colour override
(`002EFE10` sets it); otherwise, when a fade-in follows a running record (`direction == 1` and
the record was in state ≥ 1), the previous colour is kept; otherwise **`0x80000000` (black) or
`0x80FFFFFF` (white)** by the `white` argument (`002EFC5D`, `002EFC67`).

**Starting a layer** (`002EFA70`): if the record is running or finished, its old handle is
released first (`0024CFF0`, `002EFB52` / `002EFBBB`), the double at `022BDD50` is zeroed and two
frame-rate words defaulted to 1 (`002EFB67`–`002EFB90`); then `00375900(&descriptor)` allocates a
**screen-effect descriptor** — a 32-entry, `0x70`-stride pool whose records start at `02EBF9E0`
(`00375999`; the handle dword is `+0x68`, walked from `02EBFA48` by the release `00375470` and
from the record base by the state query `00375AE0`), with a free-slot search in groups of four
(`00375926`–`0037595C`; its `lea` of `02EBFAB8` is record 1's `+0x68`, so it tests `[rax-0x70]` first), the slot chosen by `00375A20(kind nibble, priority)`,
the handle `0x80000000 \| (++counter & 0x0FFFFFFF)` (`003759A3`–`003759BB`, counter `02EC07E8`), the 0x68-byte descriptor copied in
(`003759C9`–`00375A01`) — and `003B0F80(handle, 1)` marks it live in a 36-entry `0x18`-stride
handle list (`003B0F90`–`003B0FBF`). The globals ~~`022BDD56 = 3`~~ `022BDD5D = 3`, `022BDEB0 = 0`, `022BDEB4 = 6` *(corrected 2026-10-02, OPUS: `002EFA70`+0x284 `mov byte ptr [022BDD5D], 3`)*
are reset at the end (`002EFCF4`–`002EFD05`).

**The handle's top nibble is its class**: `0024DE70` (state) and `0024CFF0` (release) dispatch on
`handle >> 28` through nine-arm tables; class 8 is these screen effects (`00375AE0` / `00375470`).

### 2.2 The per-tick walk

`002EF910`, called by `World_UpdateSimulationTick` (`00314020`), polls each of the seven records:
state 3 from `0024DE70(handle)` marks the record running (`002EF9BC`); state 5 — finished —
marks it finished (`+4 = 2`, `002EF977`) unless it was a fade-in (`+5 == 1`), in which case the
handle is released and the record freed, and for layers 0, 2, 4, 5 and 6 (`bt 0x75`,
`002EF9AF`) `001D6C80` is called. *Corrected 2026-09-15 (OPUS), `UQ-237`: `001D6C80` **does not release anything** — it recomputes a path stem when `[obj+0x7C]` has changed. See the `UQ-237` answer below.* So a finished **fade-out stays** (the screen
remains black or white until something starts a fade-in), a finished **fade-in frees its layer**.

### 2.3 The accessors and the verbs

| function | what |
|---|---|
| `002EF840(layer)` | release and free one layer |
| `002EF890()` | release and free all seven — the `mapjump` verb (`008D`, `00355350`) |
| `002EF9F0(layer)` / `002EFD20(layer)` | the layer's handle / state byte |
| `002EFA20()` | reset: state byte ~~`022BDD56 = 3`~~ `022BDD5D = 3` *(corrected 2026-10-02, OPUS: `002EFA20`+0x2 `mov byte ptr [022BDD5D], 3`)*, the seven handles and the two words zeroed, `022BDEB4 = 6` |
| `002EFE10(colour…)` | arm the one-shot colour override ~~at `022BDD58`~~: flag `022BDD5C`, colour `022BDD58`–`022BDD5B` *(corrected 2026-10-02, OPUS: `002EFE10`+0x0..+0x1A)* |
| `002EFE40(n)` / `002EFE50(n)` / `002EFE60(n)` | write `022BDEB4` / `022BDEB0` / `022BDEB8` — the kind and wait words the schedule and the skip set before starting a layer (`5`/`6` and `0xFF` are the values seen) |
| `002EFD50` / `002EFD80(n)` / `002EFDC0(n)` | a single **effect fade** handle beside the layers, through `0036E750(0, 0, &params, n, 9)` — the `efffadein` / `efffadeout` verbs (`0268` / `0269`) |

The layer verbs ~~pop two integers and tail-jump into `002EFA70`~~ *(corrected 2026-10-02, OPUS: §9's correction - that describes the `_d` variants `00D0`–`00D2`, not `00B6`–`00B8`)* with the direction and colour
fixed: **`fadeout`** (`00B6`, `00356650`: direction 0, black), **`whiteout`** (`00B7`, `00356FE0`:
direction 0, white), **`fadein`** (`00B8`, `00355EB0`: direction 1, after `00183070` and
`001D6C20`); the `_d0` / `_d1` / `_d2` variants (`00D0`–`00D2`) are **three further handlers, not the same three** — `00356270` / `00356A50` / `003559B0`, and they are the ones that take **two** integers (§9). The
other direct callers are the three `WorldTransition_*` entries, the runtime pass, the mode
machine `0035CA70`, the skip family (`003601D0`, `003603F0`, `00360480`, `00360710`) and ~~four~~ six *(corrected 2026-10-02, OPUS: six are listed)*
Presentation / UI callers (`00228C70`, `0027EFA0`, `00280140`, `003939B0`, `00394130`, `003EFAA0`).

### 2.4 The movie fade schedule — registry slot 0

Registry slot 0 (`02EBF008`) binds `battle_pack.bin`'s directory entry `+0x118`: an `st2e` table
of **49 rows × 8 bytes** (`the encoded-id page` counted it; the rows are below). `0037DDD0`, under
`MainLoop_UpdateAndRenderFrame`, selects the row for the current movie (`001847D0()` × stride,
`0037DE70`–`0037DE85`) into `02ADED98` when the player's mode (`00184860` = root `+4`) is 1 or 2,
and `0037DEA0(ctx)` applies it against the player context — `ctx+0xC8` the row, `ctx+0x14` the
elapsed frames, `ctx+0xC0 → +0x10` the movie's length, `ctx+0xF0` bits 3 / 4 "fade-in / fade-out
issued":

```
row  +0  id            +1 fadeInStart   +2 fadeInLength   +3 fadeOutLength   +4 fadeOutLead   +7 flags (bit 0 white in, bit 1 white out)   <- corrected 2026-10-02, OPUS - +3 is fadeOutLead and +4 fadeOutLength: 0037DEA0+0x7F gates the fade-out on byte +4, and +0x8E subtracts byte +3 from the length for the frame count
fade in : when elapsed >= fadeInStart and fadeInLength != 0:
          002EFE40(5); 002EFA70(0, fadeInLength - elapsed + fadeInStart, 1, flags & 1)          0037DED0-0037DF0F
fade out: when fadeOutLength != 0 and elapsed >= length - fadeOutLength - fadeOutLead:
          002EFE40(5); 002EFA70(0, length - fadeOutLead - elapsed, 0, (flags & 2) != 0)         0037DF16-0037DF73
```

Shipped rows (ids 0–0x30, and the section is **byte-identical in all nine languages**, §9):
**11 of the 49** carry `1E 1E 3C 3C` (fade in over 30 frames from frame 30, fade out over 60
frames ending 60 before the end) — the commonest pattern, not a majority. **Ids 3, 13, 24, 28,
29, 31 have no fade-in at all** (`fadeInLength == 0`, so the first condition never fires —
corrected §9; the rows that *start* at frame 0 are a different twelve). Ids 4, 10, 42, 48 have no
fade-out lead (`00 0F`); id 25 is the outlier (`1E 0F CD 96`); ids 17, 19, 21 fade to white on
the way ~~out~~ in *(corrected 2026-10-02, OPUS: flags 1 is bit 0, the fade-in's white argument, `0037DEA0`+0x46..+0x4E)* (flags 1), 26, 35, 43 both ways (flags 3), and **flags 2 never occurs**; ids **0**,
32, 37–41, 44–47 are all-zero rows. `002EFE40(5)` before each start marks the fade as the
schedule's.

### 2.5 The cutscene skip

`00360710`, after its eleven notifications, issues `002EFE40(6)`, `002EFE50(0xFF)` and
`002EFA70(4, 0, 0, 0)` when the manager byte is still 0 (`00360832`–`0036084F`): **layer 4 goes
to black in zero frames** — the instant cut a skipped scene shows — with kind 6 and a wait of
`0xFF` ~~recorded in the two words for whoever resumes the scene.~~ in the two words, which this same start copies into its descriptor before resetting them to 6 and 0 *(corrected 2026-10-02, OPUS: `002EFA70`+0x20B and +0x215 read them, +0x284..+0x295 reset them)*.

### 2.6 The mode machine `0035CA70`, decoded (SWE2-FRONTIER, switch-families package)

`0035CA70` (1118 B) is a **14-state sequencer** on a task object's state byte `+0xC0`
(`movsx`/`dec`/`cmp 0xD`/`ja` at `0035CA85`–`0035CA94`, RVA table `0035CED0` indexed
`[rdx+rax*4+0x23CED0]` at site `0035CAA3`). Every arm ends by writing the **next** state into `+0xC0`, so the
object steps once per tick; `+0xC4`/`+0xC8` hold two load handles and `+0xC1` a saved
next-state. The object is a `0xD0`-byte task created by factory `0035CFA0` (`00244F50` with
procedure `0035C960`, gated on `00265680()` — a scan of the `0x288`-stride actor records —
and on singleton `022CA468` being null — `cmp qword[022CA468],0` at `0035CFC0`). `0035C960` is a three-arm message procedure: id 1
initialises (`+0xC0 = 6`, `+0xC2` = message byte `+8`, `0035C9DB`–`0035C9F3`), id 2 ticks the
machine (`0035C9CE`), id `0x12` tears down (`002E1CA0` ×3, `00252D90`). The factory is reached
from `00304440` (a timed trigger writing the `+0x5AE4`/`+0x5AE8` floats under
`[02EB…]+0x5AE0 bit 1`) and from `003CA310`'s message-`0x12` arm gated on `+8 == 0x8102`.

| state (`+0xC0` byte) | arm | work | next state |
|---|---|---|---|
| 1 | `0035CB38` | `0026C3C0(0)`, `00303D90(0)`, `003CA1C0`, `003C58B0`, `003634B0(0xF, 0)` | 9 |
| 2 | `0035CCEB` | `00282F80()` (`*(0209AC30)+0x408` zero, `0x938` B), `00283270(1)`, `002839B0()` | 3 |
| 3 | `0035CD19` | two 9-iteration scans of `00282DF0(i)` — the `*(0209AC30)+0xAC8` slot table — reading `+0x60` words and flag table `+0xB10`; `00283870(arr)` → `003273D0(…,1)` (`PartyConfiguration_SetSelectorsAndReconcileRoster`), `00283840(0)` | 4 |
| 4 | `0035CE66` | `00283980()`; when nonzero: `00283940()`, `0032AB60(0x73, 0)`, `0026C840(0)`, `003634B0(9, 0)` | 7 |
| 5 | `0035CEAC` | `+0xC0 = 0`; `00244F00(rbx)` marks the task `+0x40 \| 0x40` (delete) | — |
| 6 | `0035CAAF` | `002EFA70(0, 0x1E, 0, 0)` — layer-0, 30-frame fade out (`ecx=0`, `edx=0x1E`) | `+0xC0 = 0x108` → 8, `+0xC1 = 1` |
| 7 | `0035CADC` | `002EFA70(0, 0x1E, 1, 0)` — layer-0, 30-frame fade in | 5 |
| 8 | `0035CB08` | `002EFD20(0)` — layer-0 state; exits when it reads 1 | `+0xC0 = +0xC1` (reload saved) |
| 9 | `0035CB74` | `002DEBE0(-1)` → `+0xC4`; if ≥0: `002DEE50(+0xC4, 0x5A, 0)`, `003611F0(0x5A, 1)` | 10 |
| 10 | `0035CBBF` | `002F1A30(1)` wait; then `002DEDE0(+0xC4)` | 11 or 12 (`+0xC4 < 0` picks 12) |
| 11 | `0035CC01` | `002DED60(+0xC4)` wait — exits while nonzero | 12 |
| 12 | `0035CC2E` | `00360D70`/`00360E50(+0xC4)` by sign; `0026DE00(0)` → `+0xC8`; `00361630(+0xC8)` | 13 or 14 (result <0 picks 14) |
| 13 | `0035CCA9` | `00360C20(+0xC8)`; when it reads 5: `002DEC00()`/`002DECE0()` vs `+0xC8` | 2 |
| 14 | `0035CC7C` | `00361630(+0xC8)` — exits while <0 | 13 |

The `state` column above holds the real `+0xC0` selector byte — the RVA table `0035CED0` orders
arms `CB38, CCEB, CD19, CE66, CEAC, CAAF, CADC, CB08, CB74, CBBF, CC01, CC2E, CCA9, CC7C`, so the
table is *not* in arm-address order (an earlier draft numbered arms in address order, which made
the `state` column disagree with the `next state` column; corrected on `AUDITSEM-CONTRA-
FRONTIER-SWFAM-STATEMAP`). The edges form a poll-and-retry graph rather than a straight line:
states 11 and 14 **exit without advancing** while their handle probes report not-ready, state 10
splits to 11 or 12 on the sign of `+0xC4`, state 12 splits to 13 or 14 on its probe, state 8 holds
while layer 0's state byte reads 1, resuming at the saved state `+0xC1` once it clears, and only
state 5 retires the object. The id-1 message enters at state 6. The per-helper bodies (`002DED60`, ~~`00360D70`/`00360E50`~~ *(answered: see the `00360D70` and `00360E50` sections below; 2026-10-02, OPUS)*, `00360C20`,
`00361630`, `00303D90`, `003C58B0`) are named here only by their call sites — their bodies are
**not read** in this pass, and which transition the machine sequences (a party-read, a mode
change, or both) is left open.

## 3. Key addresses

| address | role |
|---|---|
| `002EFA70` | start a fade on a layer — `(layer 0–6, frames, direction, white)` |
| `002EF910` | the per-tick poll from `World_UpdateSimulationTick` |
| `002EF840` / `002EF890` / `002EFA20` | free one / all / reset |
| `002EF9F0` / `002EFD20` / `002EFE10` / `002EFE40` / `002EFE50` / `002EFE60` | handle, state, colour override, the three words |
| `002EFD50` / `002EFD80` / `002EFDC0` | the single effect-fade handle (`efffadein` / `efffadeout`) |
| `00375900` / `00375A20` / `003B0F80` | the screen-effect descriptor pool at `02EBF9E0` (32 × `0x70`, handle at `+0x68`), its slot chooser, the live-handle list |
| `0024DE70` / `0024CFF0` | handle state / release, dispatched on the handle's class nibble |
| `0037DDD0` / `0037DEA0` | the movie fade schedule: row selection into `02ADED98`, and its application |
| `022BDD60` | the seven records; `022BDD50` a double zeroed at each start (read by `001C2F50`); `022BDD56`–`022BDD5D` state, override and nibble bytes; `022BDEB0` / `022BDEB4` / `022BDEB8` the words |
| `02EBF008` | registry slot 0 — the 49 × 8 schedule |

## 4. Data structures and formulas

```
FadeLayer[7] at 022BDD60, stride 0x30
  +0x00  u32   effectHandle        0x80000000 | counter; 0 = free
  +0x04  u8    state               0 free, 1 running, 2 finished
  +0x05  u8    direction           1 = fade in, 0 = fade out
  +0x08  u8[0x28] descriptor       +0x28 u32 colour (0x80000000 black, 0x80FFFFFF white), +0x2C u32 = 2 * frames

MovieFadeRow[49] at registry slot 0 (battle_pack +0x118, st2e, stride 8)
  +0 id  +1 fadeInStart  +2 fadeInLength  +3 fadeOutLength  +4 fadeOutLead  +7 flags (1 white in, 2 white out)
```

## 5. Modding notes

- **Change a movie's fade** by editing its row in the `+0x118` table; the frame counts are the
  authored unit, doubled once into the descriptor.
- **A fade-out never clears itself.** The layer keeps its colour until a fade-in on the same layer
  runs; `mapjump` frees all seven.
- **Layers are independent.** A script fade on layer 0 and a transition fade on another layer
  coexist; the skip's instant black is layer 4.

## 6. What is not known

- [x] **UQ-235.** What the descriptor's nibbles (`022BDD57`, `022BDD5D`) and byte `022BDD5B` select in the
      screen-effect pool, and what `00375AE0` / `00375470` (class-8 state and release) do beyond
      the pool entry.
      **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5).** The first half was restated in the register on 2026-09-16:
      `022BDD57` is the top byte of a double, `022BDD58`–`022BDD5B` are one four-byte parameter block armed by the
      request flag `022BDD5C`, and `022BDD5D` is a mode byte. **The second half: neither body does anything beyond
      the pool.** Both class dispatchers reach them by a bare tail jump in their class-8 slot (`0024DE9F`,
      `0024D01F`). The pool record is the descriptor copied in whole at `+0x00`–`+0x67` (`003759C9`–`00375A01`), the
      handle at `+0x68` and an elapsed counter at `+0x6C`, zeroed at allocation (`003759C2`).
      - **The state query `00375AE0`** finds the record by handle and answers from its kind byte `+0`. Kind 1, the
        layers' own descriptor (`+8 = 1` above), gives **3 while the counter is below the duration `+0x24`**
        (the layer's `+0x2C`, `2 × frames`) **and 5 once it reaches it** (`00375B1B`–`00375B2C`). Kinds 2, 3, 5, 6
        and 13 always give 3; kind 0 gives 0; kinds 4 and 7–12 are passed over, so a handle on one reads as gone. It
        writes nothing.
      - **The release `00375470`** scans the handles only to the first empty one, because the pool is kept packed.
        It moves every later record down one slot (`rep movsq`, `003754DF`) and zeroes `02EC07D8`, which is record
        31's handle (`02EBF9E0 + 31 × 0x70 + 0x68`, `003754E2`), so the tail slot is freed. Those are its only two
        writes.
      - **The counter is advanced by the pool's tick** `00374950`: 1 per tick, or 2 on the first tick and when a
        scheduling predicate answers non-zero. For kind 1 the tick also releases the record itself once
        `00374060` answers 0, which it does when descriptor `+0x1C` bit 1 (the layer's `+0x24` flags) is set and
        the counter has passed the duration.
      Control: `_index/candidates/uq235-effect-pool/effect_pool.py` (9 checks).
- [x] **UQ-236.** What `001C2F50` computes from the double at `022BDD50`.
      *Narrowed 2026-09-14 (FABLE), not answered: it is the auto-test map runner's timer.* `001C2F50` is the per-tick update of
      `MultipleDebugDisplay` (`01F81270`; [game application](../../00-Engine-Core-Runtime/Application-Root/game-application.md)). It
      does nothing unless the platform object's byte `+0x10D4` and the dword `01F8127C` are both set (`001C2F7C`–`001C2F90`).
      - **The timer.** It loads the platform clock double `[platform]+0x40` (`0017D8D0`) and subtracts `022BDD50`
        (`001C3227`). When the difference exceeds **120.0** (`008F9E30`), it runs the branch that opens
        `/Tools/AutoTest/MapIndex.json` (`01DF6E38` → `008F9E00`) and writes its `"MapIndex"` key from `01F81278`
        (`001C3246`–`001C3343`).
      - **The fade link.** The fade-layer start `002EFA70` is the double's only writer, and it zeroes it (`002EFB72`). The
        same instruction run also stores `01F8127C` (`002EFB67`–`002EFB7E`), setting it from `r9d` when it was 0.

      ~~So a started fade arms and re-bases the auto-test step, and the runner advances once 120 s of the platform clock have
      passed since then. With a zero base, the comparison is against the clock itself. Whether that clock restarts per
      fade, and what `r9d` holds, was not read.~~
      **ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5): it computes the application's run time, and the fade does not
      re-base it.**
      - **The fade writes only zero.** The only store to `022BDD50` is `movsd` of an `xorps`-cleared register
        (`002EFB6D` / `002EFB72`). The one other reference is the runner's `subsd` (`001C3227`). So "re-base" is a
        reset to 0, and `clock − [022BDD50]` is the clock itself.
      - **The clock is the `PApplication` run time.** `0017D8D0` reads `+0x40` of the object at `02EA5368`, which
        the `PApplication` constructor `00792350` publishes (`00792550`; vtable `01CB2508`). `+0x40` is written in
        two places:
        - The run start `0079F150` (the body whose error text is *"App failed during initScene"*) zeroes it
          (`0079F19A`) and stores `now − processStart` in `+0x50` (`0079F1A2`–`0079F1AF`). `processStart` is the
          double `02CB60E8`, written once, by `005A0A68`.
        - The per-frame update `0079D920`, called from `PApplication` slot 28 `0079C140`, sets `+0x40` to
          `now − processStart − [+0x50]`, or, when the fixed step `+0x6C` is positive, adds that step. It also
          writes the delta to `+0x48`.
        So the clock counts seconds since the run began, and nothing on the fade path restarts it.
      - **`r9d` is the constant 1** (`002EFAAA`, and again `002EFB57`). The fade start therefore sets `01F8127C`
        to 1 when it is 0 and leaves it otherwise; that is its only writer.
      - **So the runner fires on the first tick after the application has run 120 s**, provided three things
        hold: a fade has started once, the platform byte `+0x10D4` is set, and the flag `01F8127C` is armed.
        It then fires on every tick; nothing in the image clears the flag or moves the base. What the
        `MapIndex` step then triggers is the harness's business, `001C3246`–`001C3343`.
- [x] **UQ-237 ANSWERED 2026-09-15 (OPUS) — all three are 21-byte facades of one shape,
      *fetch a singleton and tail-jump to one method*, and the third does not release anything.**
      - **`00183070`** = `001D8A60()` → **`001D8770`**. The getter is the lazy singleton for
        `[01F82CD8]` whose ensure call is the `/OPT:ICF`-folded no-op `0016D6A0`. The method is
        **26 bytes** and resets a small state block: `[obj+8] = 0`; if `[obj+0x24]` was `0` it sets
        it to `1` and clears `[obj+0x20]`; either way `[obj+0x1D] = 0`.
      - **`001D6C20`** = `001DADA0()` → **`001DA080`**, and `001DADA0` is a 7-byte getter for
        `[01F82CF0]`. **The method is SEVEN BYTES:** `mov byte [obj+0x88], 0; ret`. That is the
        whole of what this call does before a script `fadein` — it clears one flag byte.
      - **`001D6C80`** = the **same** getter `001DADA0()` → **`001DA290`** (881 B). So `001D6C20`
        and `001D6C80` act on the same singleton and differ only in the method.
      - ⚠ **`001DA290` RELEASES NOTHING, which corrects §2.2 above.** Its body, read end to end:
        two gates (`001D6B20` must return non-zero, `001D6B90` must return zero); then a
        **change-detect** — `edx = [obj+0x7C]`, return if `[obj+0x84]` already equals it, return if
        it is negative, otherwise commit `[obj+0x84] = edx`; then `0032F170(0, &a, &b)`, an EASTL
        string built by `001EDF00` (its literal `"EASTL basic_string"` is at `008F6600`), and
        `002DF980(b, a)` returning a C string. It copies that string, NUL-terminates it, scans
        **backwards for `\` (`0x5C`)** and then **backwards for `.` (`0x2E`)**, and calls
        `001A9E50(start = slash+1, length = dot − slash − 1)`. **That is a path *stem*** — the
        filename with its directory and extension removed. Every remaining callee (`001A5760`,
        `001A52A0`, `001A1220`, `001A0BB0`, `001A0A90`, `001DAB30`) is an EASTL string helper, and
        **no free, handle release or refcount appears anywhere in the 881 bytes.**
      - **Neighbour accounting — this page reaches into `Resource`, and that crossing is this
        sentence's doing.** Of those six helpers, **three of them live in the **Resource** subtree**:
        `001A0A90` (93 B), `001A0BB0` (160 B) and `001A1220` (8 B). The crossing is **one-way and this
        page is the client.** Measured on the call graph: those three are called by **15, 14 and 17**
        `Resource` functions respectively and by one `Save_Load_Settings` caller each, `001A1220` also
        by one `CoreRuntimeScheduling` caller — they are **shared string utilities with inbound-heavy
        traffic**, and between them they reach `Resource` on 55 of the edges the auditor counts.
        **None of the three calls anything owned by Presentation, and no function documented on this
        page is called by `Resource`.** So the relationship is: the fade layer's stem recompute
        borrows string helpers that happen to be owned by `Resource`; it does not couple the fade
        schedule to resource loading, and nothing about `Resource`'s behaviour is claimed here.
        *(Recorded 2026-09-15 (OPUS). `audit_crossrefs` reported 0 unaccounted neighbours at the
        parent commit `590929bb` and 1 at `b528a842`, which is mine — the citation above introduced
        it and the pre-publish guard did not catch it because it tests a different rule.)*
      - **The call site in §2.2 is right; the description is not.** `002EF9AF bt r15d, ebx` /
        `002EF9B5 call 001D6C80` does fire for exactly the layers in mask `0x75` — bits 0, 2, 4, 5
        and 6. But what runs there is *“recompute the stem when `+0x7C` has changed”*, not a
        release. **§2.2's clause is corrected in this same commit.**
      - **Not claimed:** what the stem is *used for* after `001DA290` computes it, and what
        `[obj+0x7C]` counts. **UQ-237.**
- [x] ~~**UQ-238.** Which movies the 49 ids are, and why ids 25 and 43 differ.~~ **ANSWERED 2026-09-25 (FABLE,
  Claude Opus 5.5).** Each id is a movie code from the executable's path table, kind `0x1C`: `OPN`, `NAL`,
  `DLS` … `EPL` (25) … `IVT` (43) … `ANX`, and the player opens `<code>.webm`. **The all-zero rows 37–41
  and 44–47 are exactly the ids whose movie does not ship**, either no `.webm` or no path. Id 25 (`EPL`)
  has the table's only long fade-out. Id 43 (`IVT`) has only a 6-frame white fade-in. See
  [§ Which movie each id plays](#which-movie-each-id-plays--the-schedule-joined-to-the-path-table-fable-claude-opus-55-2026-09-25).

## 7. Evidence

| claim | evidence | tier |
|---|---|---|
| Seven 48-byte records, the fields, the colour choice | `002EFA70` read whole; the clamp and stride in `002EF840` / `002EF890` / `002EF9F0` / `002EFD20`; every rip reference into `022BDD50`–`022BDEB8` listed | 1 |
| The verbs | `scriptvm-verb-table.tsv` rows `00B6`–`00B8`, `00D0`–`00D2`, `008D`, `0268`–`0269`; `00356650`, `00356FE0`, `00355EB0` read whole (tail jumps into `002EFA70`) | 1 |
| The per-tick poll and the fade-in / fade-out asymmetry | `002EF910` read whole; its caller from `edges.tsv` | 1 |
| The descriptor pool and the typed handle | `00375900` read whole; `00375A20` and `003B0F80` heads; `0024DE70` / `0024CFF0` dispatch tables | 1 |
| The schedule table and its application | `0037DDD0` and `0037DEA0` read whole; the 49 rows dumped from `battle_pack.bin` `+0x118` | 1 |
| The skip's instant black | `00360832`–`0036084F` | 1 |

## 8. Related

- [`../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md`](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md) — the skip (EX-8) and the tick that polls the layers
- [`../../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md`](../../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md) — registry slot 0 (FY-7)
- [`../../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md`](../../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md) — where the records sit after the fourth save buffer
- [`../../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv`](../../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv)

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

*(Static only — the shipped image and the shipped archive, read never written. Nothing executed.)*

### ✔ The schedule re-extracted, and the header declares its own count

`battle_pack.bin`'s directory pair at `+0x118` is `(000443E8, 00044598)` in the `us` copy — 432
bytes — and the section opens with an **`st2e` header that states the table**: magic `st2e`,
**count 49**, **stride 8**, data at `+0x20`. So "49 rows × 8 bytes" is the file's own declaration and
not an inference, and the rows end at `00044590`, eight bytes short of the section end. **Byte `+0` is
the row index in 49 of 49.**

**Every specific row claim reproduces exactly:**

| the page says | measured |
|---|---|
| ids **4, 10, 42, 48** have no fade-out lead (`00 0F`) | **exactly those four** |
| ids **17, 19, 21** carry flags 1 | **exactly those three** |
| ids **26, 35, 43** carry flags 3 | **exactly those three** |
| id 25 is `1E 0F CD 96` | **`19 1e 0f cd 96 00 00 00`** |

### ✔ New: the schedule does not vary by language

All nine `battle_pack.bin` copies carry the section at different file offsets and **the same 432
bytes** — one SHA-256 across `ch cn de es fr in it kr us`. The page's `corpus_validated` line covers
the `us` copy; the table is the same in all of them.

### ✖ Corrected: three row-set statements

* **"most carry `1E 1E 3C 3C`"** — **11 of 49**. It is the commonest pattern and under a quarter of
  the table.
* **"ids 3, 13, 24, 28, 29, 31 fade in instantly"** — those six have **`fadeInLength == 0`**, and
  §2.4's own pseudocode issues a fade-in only *"when `fadeInLength != 0`"*. **They do not fade in at
  all.** The rows whose fade-in *starts* at frame 0 with a real length are a different and larger
  set — **6, 10, 17, 19, 20, 23, 26, 27, 36, 42, 43, 48**, twelve of them. Two different properties,
  and the label belongs to the other one.
* **the all-zero list misses row 0** — there are **eleven**: **0**, 32, 37–41, 44–47.

And one addition: **flags is only ever 0, 1 or 3** (43 / 3 / 3). **Value 2 never occurs**, so a white
fade-*out* never ships without a white fade-*in*.

### ✖ Corrected: the `_d` variants are different handlers, and it is they that take two integers

§2.3 says the `_d0` / `_d1` / `_d2` variants *"are the same three handlers"*. They are six distinct
addresses, and the verb table's **CONFIRMED** arities separate them:

| verb | id | handler | arity |
|---|---|---|---:|
| `fadeout` | `00B6` | `00356650` | **1** |
| `whiteout` | `00B7` | `00356FE0` | **1** |
| `fadein` | `00B8` | `00355EB0` | **1** |
| `fadeout_d0` | `00D0` | `00356270` | **2** |
| `whiteout_d1` | `00D1` | `00356A50` | **2** |
| `fadein_d2` | `00D2` | `003559B0` | **2** |

And the bodies agree with the table. `00356270` is nine instructions: pop, pop,
`jmp 002EFA70(layer, frames, 0, 0)`. `00356650` pops **one**, calls `00267F90` **twice**, pops again,
and only then tail-jumps with the same fixed `r8d` / `r9d`. **So §2.3's sentence — "the layer verbs
pop two integers and tail-jump into `002EFA70`" — describes `00D0`–`00D2`, not `00B6`–`00B8`.** The
direction-and-colour half of the claim holds for all six.

### The layer machinery, spot-checked

The clamp accessor resolves its base from the image: `002EFAA3 lea r10, [rip + 0x1FCE2B6]` →
**`022BDD60`**, with `[0, r8d]` clamping by `jns` / `cmovg`. The per-tick walk's layer filter is
`002EF9AF bt r15d, ebx` — **a register, not the immediate `0x75` §2.2's shorthand suggests**, though
`0x75` is bits 0, 2, 4, 5 and 6, exactly the layers named.

**Not claimed.** Nothing about the running game. `00375900`'s pool, `003B0F80`'s handle list, the
one-shot colour override and the `0037DEA0` apply were **not re-read** — this pass re-measured the
authored table and the verb wiring. What the movie ids are. Nothing was executed.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Status_Periodic_Terminal — CLIENT.** `BattleUnit_RunPeriodicCombatMaintenance` calls a cited function.
- **ActorEntity - CLIENT and SERVICE (41 edges).** `00183070`, `00225CD0`, `0024CFF0`, `00265680` (+12 more) are called by bodies filed to ActorEntity: BattleUnit_SnapshotWorldActorRuntimeState (`00236300`), ActorSystem_ReleaseManagerRecords (`0025B070`), `0025B600`, ActorManager_RunFieldRuntimePass (`0025D9E0`) (+7 more); `00225CD0`, `0022A0B0`, `0026C3E0`, `0026C840` (+5 more) reach bodies filed to ActorEntity: `00233D70`, BattleUnit_GetBySlotIndex (`00236820`), BattleUnit_GetSlotCount (`00236850`), BattleStorage_InitializeWorkArrays (`002368D0`) (+15 more) - shared machinery across the layer boundary, no shared ownership.
- **Party - CLIENT and SERVICE (23 edges).** `00265680`, `00283270`, `00311E20` are called by bodies filed to Party: PartyFocus_SelectAndRequestDefaultActor (`00326500`), `00328BD0`, PartyControl_ApplyAnalogLocomotionToActor (`00358CB0`), PartyFocus_ProcessActorControlPresentationState (`00358F90`); `00234520`, `0026C3E0`, `00283870`, `00285290` (+9 more) reach bodies filed to Party: PartyControl_RecomputeSuppressionFromLeaderBattleState (`0023B040`), PartyRoster_GetActorBySlot (`00263750`), PartyRoster_AssignActorToSlot (`00269C70`), `00284970` (+10 more) - shared machinery across the layer boundary, no shared ownership.
- **SaveLoad - CLIENT (5 edges).** `00251D50`, `00252D90`, `002EFA70`, `002EFD20` (+1 more) are called by bodies filed to SaveLoad: `00280140` - shared machinery across the layer boundary, no shared ownership.
- **Save_Load_Settings - CLIENT and SERVICE (23 edges).** `001A0A90`, `001A0BB0`, `001A1220`, `00247870` (+4 more) are called by bodies filed to Save_Load_Settings: SaveloadManager_RequestDisableAutosaveList (`001C1810`), `002EF2D0`, SaveWrite_OperationStateCallback (`0057E4D0`), SaveLoad_FullImageStorageCompletionCallback (`00580840`) (+5 more); `00280140`, PersistentFlag_SetPrimary (`0032AB60`), `003601D0`, `00394130` reach bodies filed to Save_Load_Settings: SaveImage_ValidateRuntimeFormatHeader (`00255260`), SaveImage_GetPersistentPayloadBase (`002EF2B0`), SaveImage_ClearActiveRuntimeBuffer (`002EF5F0`), SaveImage_GetActiveRuntimeBuffer (`002EF640`) (+1 more) - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT and SERVICE (81 edges).** `00183070`, `001D6AE0`, `001D6C20`, `0024CFF0` (+33 more) are called by bodies filed to Script_VM_Native_Bridge: `0033F4C0`, `0033FD40`, `00340080`, `00340260` (+49 more); `003559B0`, `00355EB0`, `00356270`, `00356650` (+2 more) reach bodies filed to Script_VM_Native_Bridge: VMValueStack_PopInt32CoerceFloat32 (`00267E10`), VMValueStack_PushInt32 (`00267F90`) - shared machinery across the layer boundary, no shared ownership.
- **World - CLIENT and SERVICE (4 edges).** `00225CD0`, `002EFA20` are called by bodies filed to World: `00266D10`; `0022A0B0`, World_UpdateSimulationTick (`00314020`) reach bodies filed to World: `002623A0`, `00266D10` - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT and SERVICE (39 edges).** `00234520`, `002DF980`, `002EF910`, `002EFA70` (+11 more) are called by bodies filed to WorldAreaField: BattleSystem_RunFieldFrameOrchestrator (`00234590`), World_UpdateSimulationTick (`00314020`), WorldTransition_RequestFieldTransition (`00314440`), WorldTransition_RequeueCurrentFieldForRestore (`00314530`) (+5 more); `0026C3E0`, `0026DE00`, `00280140`, `0030C010` (+7 more) reach bodies filed to WorldAreaField: BattleSystem_RunFieldFrameOrchestrator (`00234590`), WorldTransition_RequeueCurrentFieldForRestore (`00267C90`), WorldPersistence_ResetBanksAndMarkInitializationState (`00268320`), `0026DE00` (+9 more) - shared machinery across the layer boundary, no shared ownership.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAI — SERVICE.** `00283270` on this page calls `GambitConfig_CopyBasePairSetForStatsIndex`, owned by that layer. What it reaches is an 85-byte copy out of the same `0x1C8`-byte stats record: slots `0..0x27` into `[02EBF190] + 8`, then **three 16-byte blocks from `+0x88`, `+0x98` and `+0xA8` and the dword at `+0xB8`** into a `0x34`-byte destination; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatAction — CLIENT.** `FUN_0030c010`, owned by that layer, calls `00253B90` on this page. That caller is a 179-byte predicate that tests two units in turn: the subject's `+0x3C`/`+0x64` pair against `0x8000020`, its `[+0x780]` with bit 10 of `dword[+0x788]`, and then the unit named by `dword[+0x710]` against `0x80000003` and the shared permission bit, ending on `[022C2160]` being `0` or `7`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Developer — CLIENT.** `FUN_001c2f50`, owned by that layer, calls `0017D8D0` on this page. That caller is a string-assembling routine over the EASTL allocator at `008F6600`, the globals at `01F8127C` / `01DF6E38` / `01DF6E40` and the static empty buffer `02EBA2E0`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Gameplay — CLIENT.** `BattleRuntime_GetModeDependentDistanceThreshold`, owned by that layer, calls `00253B90` on this page. That caller is the threshold the mode ladder feeds: mode **1** gets `5.55` plus the shared `0.2`-ish bias, every other mode gets `2.0` plus the same bias, and when the global predicate refuses there is a third constant entirely; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**InputGameplay — CLIENT.** `FUN_00313a00`, owned by that layer, calls `002E1CA0` on this page. That caller is a state query that tests the pointer at `[02089350]` and the global equality predicate `00253B90`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Movement — MECHANICAL (SWE2-CONTRACT 2026-09-15, 9 edges).** `00314020` calls five movement helpers (`0046AFA0`/
`003DAA20`/`00234520`/`003DAA40`/`003DAC70`); `00304440` calls `00311E20`; `0035CA70` calls
`0026C3C0`; `00265680`/`0026C3C0` trade calls with `0026C3E0`. The fade schedule's shared bodies
touch movement helpers — cadence adjacency, no locomotion semantics.

**Story_Event_Quest_Hunt — SERVICE (SWE2-CONTRACT 2026-09-15, 2 edges).** Fade body `0035CA70` calls `PersistentFlag_SetPrimary` `0032AB60` — a screen fade can write a story persistent flag; `PersistentFlag_ApplyAuthoredInitialPrimarySet` `00379160` shares the same setter. Small, real.

## The `00375900` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00375900` (~186 B) — `rdi = qword[rsp+0x2C]` layer-pointer read
(`0037590A`/`00375912`).

| member | role | interior |
| --- | --- | --- |
| `00375A20` | `02EBF9E1`/`02EC07E1` pair-record walk, `r9d = r10d = 0` counters (`00375A28`/`00375A32`) | [`00375A28`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.


## Interior citation — frontier hub `002DEE50` (2026-09-18, SWE2-EC7)

`002DEE50` — 27 B, 6 A-measured callers; the fade-flag publish guarded by the `0215EF44`
counter. Interior verified: a negative `ecx` arg is replaced by the counter value
(`002DEE54`); if that is still negative the call is a no-op (`002DEE5C`). Otherwise `r8b` lands
on the `0215EF4D` byte at [`002DEE5E`](../../_index/ADDRESS-INDEX.md) and `001DBCA0` runs the
follow-up. ~~The write is the layer's armed/visible flag; the counter gate is "no fade state~~
~~loaded".~~ The call is a music volume fade: `0215EF44` is the current track, and `001DBCA0` hands the track, the frame count and the volume to the sound side, which divides them by `60.0` and `127.0` *(corrected 2026-10-02, OPUS: `002DEE50`+0x15 `jmp 001DBCA0`; `00222B70`+0x3A and +0x42 `divss`; the mode machine's state 9 calls it with `0x5A` frames and volume 0)*.


### Interior citation — frontier hub `00252D90` (2026-09-18, SWE2-EC7)

`00252D90` — 71 B, 12 callers: the consume-and-clear step in the id-`0x12`
teardown. `02092730` is latched, masked `& 0x7FFF`, and handed to `00255290` at
[`00252DA4`](../../_index/ADDRESS-INDEX.md); a negative result with the raw
slot `== 0xB` routes to `002260A0`, otherwise `00225CD0(result, -1)` runs, and
both `02092730` and `02092734` are zeroed on exit — the slot is single-shot.

## SWE2-EC7-25 update (2026-09-18) — `00360D70` deferred byte flush

`00360D70` (82 B) sweeps `022CB9F1`-to-`022CBA51` 0x18-stride records:
`byte[-1] == 5` runs `002DEDE0` + `002DEC20` on `byte[0]` and clears the
pending byte; any other nonzero marks `byte[+1] | 1`. The fade/audio
callers run it as the deferred-command drain. Interior anchor `00360D88`
(the `movzx` loop head).

## SWE2-EC7-30 update (2026-09-18) — `002839B0` `+0x318` lazy ensure

`002839B0` (93 B) is the third step of the fade row's `00282F80`/
`00283270(1)`/`002839B0()` triple: while `[0209AC30]+0x318` is null it
allocates a 0xF0-byte record through `00244F50(0xF0, 00283A10)`,
publishes it to `+0x318`, initialises via `00246AC0`, then tails
`00247870(rec, 0)`. The `00283A10` message callback is a kind
dispatch: kind 1 snapshots ten `movsx` words out of the bank's
`+0x468..+0xA68` fields (0xC0-stride apart) into `out+0xC0..+0xE0`
with `+0xE4 = 0` and calls `00247930`; kind 2 runs `00283B30`; kind
`0x12` returns 0; everything else forwards to `005C5230`. Interior
anchor `002839D4` (the `call 00244F50` allocation).

## SWE2-EC7-37 update (2026-09-19) - `003CA310`

`003CA310` (536 B) is the fade message body the page names - `01F44830`/`02092730`/`01E0C1D8`/`01E0C1DC`, `00249C60`/`00303CC0` triples plus `00244F00`/`0035D010` pairs and `005C5230`/`0035CF50`/`0035CFA0`. Interior anchor `003CA356` (a `005C5230` call).

## SWE2-EC7-37 update (2026-09-19) - `001DAB30`

`001DAB30` (512 B) is a call-free CRT vector insert sibling - capacity test `[rdi+0x10]-[rdi+8]` vs the `r9d-r8d` count, in-place shift when the range overlaps the end, memmove path otherwise. Interior anchor `001DABB8` (inside the shift loop).

## SWE2-EC7-44 update (2026-09-19) - `00283A10`

`00283A10` (273 B) is a widget-message body - `00247930`/`00283B30`. Interior anchor `00283A39` (a `00247930` call).

## SWE2-EC7-51 update (2026-09-19) - `00355350`

`00355350` (174 B) is a body - `001D6AE0`/`002640C0`/`00264180`/`00264830`/`002EF890`/`00314440`. Interior anchor `0035536D` (an `001D6AE0` call).


## SWE2-EC7-64 update (2026-09-19) - `00360E50`

`00360E50` (141 B) is a `+0xC4`/`+0xC8` by-sign body - `002DEC20`/`002DEDE0` plus `022CB9F0`. Interior anchor `00360EC2` (a `002DEDE0` call).


## SWE2-EC7-68 update (2026-09-19) - `002DEDE0` fade singleton selector

`002DEDE0` (80 B) maintains the ~~fade-layer singleton~~ current music track *(corrected 2026-10-02, OPUS: the same sound-side chain as `002DEE50`)*
`dword[0215EF44]` the fade-schedule bodies call: `ebx` is the
argument, or the current value when `ecx < 0`; `001DBC30(ebx)`
runs when `ecx < 0` or when the argument equals the current value;
`001DBC50(ebx)` runs whenever `ebx >= 0`; and the slot is written
`-1` exactly when it still equals `ebx` at the end - so `(-1)`
re-runs both callees on the current layer and then clears the
slot, while a new id publishes through `001DBC50` alone. Interior
anchor `002DEE11` (the `001DBC50` call).

## SWE2-EC7-69 update (2026-09-19) - `002DEC20` sign-guard forwarder measured

`002DEC20` (9 B) measured - the sibling sign guard to `002DEDE0` in the same
schedule: `ecx < 0` returns immediately; any nonnegative layer id tails to
`001DBB30` with `ecx` unchanged. Same shape as `002DF050` on the map-screen
side - the negative guard is the "no layer selected" short-circuit.
Interior anchor `002DEC22` (the `jns 001DBB30`).

## SWE2-EC7-69 update (2026-09-19) - `00283840` UI-root flag setter measured

`00283840` (47 B) is the `00283870(0)`-paired helper the fade schedule calls:
it resolves the application root `[0209AC30]` → child `[+0x318]`, returns
silently when that child is absent, then sets `dword[+0xE4] = 1` when the
child is in its idle state - or ORs `dword[+0xE8] |= 1` when `+0xE4` is
already set. Call-free; the two flags are a request/override pair on the
same UI child.
Interior anchor `00283853` (the `cmp dword[rcx+0xE4], 0` state check).

## SWE2-EC7-93 update (2026-09-20) - `00363E40` + `003634B0` measured

`00363E40` (239 B) is the three-arm fade-mode setter `003601D0`
calls: with `02CDBFA6` set, `ecx > 0` runs `002DF190(count, ecx)` and
stages two state dwords; `ecx <= 0` runs `002DF0F0` + `003636A0` and
restores the `0x7F` triple, the -1 dword and the zeroed floats; gate
clear runs `003636A0` with the second default set.
Interior anchor `00363E61` (the `002DF190` call).

`003634B0` (165 B) is the fade-rate computer `0035CA70` calls:
`003691D0()`'s float times the `ecx` integer gives a `cvttss2si`
count that halves-and-increments into `1.0f / n` at `02CDC090`; the
non-positive arm writes the `02CDC09x` defaults and parks `dil` in
`+0x54F` instead.
Interior anchor `003634BE` (the `003691D0` call).

## SWE2-EC7-94 update (2026-09-20) - `003600D0` measured

`003600D0` (42 B) is the fixed init sequence `0034E6D0`, `003603F0`
and `00360710` call: `002EF840` runs for `ebx` 0-6, then `002F1A70`
and `003DE210`, and it tail-calls `003DE0A0`. All three callers are
the fade/movie-schedule entries that re-arm the pass after a stop.
Interior anchor `003600EB` (the `003DE210` call).

## SWE2-EC7-102 update (2026-09-20) - `00283870` measured

`00283870` (206 B) is the stored-record write with
dedupe `00285290` and `0035CA70` call on
`rbx = [0209AC30]+0x318`: a nonnull `rcx` record
is copied whole (`0x20` bytes plus the `+0x20`
dword) into `rbx + 0xC0`; a null `rcx` instead runs
`00284970` on `[rax + 0xF8]` into a stack record,
compares its nine dwords against `rbx + 0xC0`, and
returns 0 when all nine match - otherwise the
record lands at `rbx + 0xC0` too - the
write-if-changed rect the fade paths post.
Interior anchor `002838C3` (the `00284970`
call).

## SWE2-EC7-106 update (2026-09-20) - `00251D50` + `0024F920` measured

`00251D50` (52 B) is the mode-gated
query `00228130` and `00280140` call
on `020927F0`: a null record answers
1; otherwise `byte[+0xE8]` bit 0 must
be armed and `word[+0xE6] <= 8`, then
`bt 0x141, ecx` answers 1 only for
mode bits 0, 6 or 8 - the
mode-in-{0,6,8} probe the fade
schedule consults.
Interior anchor `00251D76` (the `bt`).

`0024F920` (90 B) is the chain-tag
write `0036E700` and `0036E750`
run: `ecx >> 0x1C & 0xF` selects a
row head in the `020910F0` table, the
`[+0x348]` chain is walked for a node
whose `word[+4] == cx` and
`word[+6] == dx`, and on a match
`word[+0x368]` is rewritten as
`(word & 0x7FFF) | (r8w << 0xF)` -
the high-bit flag publish onto the
located chain node.
Interior anchor `0024F96A` (the
`+0x368` mask).

## SWE2-EC7-110 update (2026-09-20) - `001E0FB0` measured

`001E0FB0` (50 B) is the
bool setter `00228C70` and
`003939B0` run: `00198790()`
fetches the fade-layer object,
and only when non-null does
`bl = (ecx != 0)` feed the tail
call `001989D0(object, bl)` -
a null-object call is a silent
no-op, so callers never check
availability themselves.
Interior anchor `001E0FC4` (the
`setne bl` flag fold).

`00284970` (793 B) is the call-free table scan `00283870` runs: `0209AC30 + 0xAC8` bases the record array, `r11 = rcx - r8` carries the caller's pointer delta, and the loop compares `word[rax+0x60]` against `si` with `r9` walking the slots - the fade layer's word-keyed slot finder.

Interior anchor `00284AF5` (function `00284970`).


## Which movie each id plays — the schedule joined to the path table (FABLE, Claude Opus 5.5, 2026-09-25)

**Answers UQ-238.** *Static: the shipping EXE's `.rdata`, the `us` `battle_pack.bin`, and the list of
shipped `.webm` files in the full extract.*

**How an id becomes a file.** The schedule row is selected by `001847D0()`, which returns dword
`+0` of the player object (`001FDF70`, `mov eax, [rcx]`). The player `001B7F30` resolves that same id:
1. It calls `002DF980(0x1C, id × 2)`, which loads `g_pathTables[0x1C]` and then the entry
   (`001B7F8A`–`001B7F93`).
2. It keeps the basename between the last `\` and the last `.` (`strrchr` on `0x5C` and `0x2E`,
   `001B7FA4`–`001B7FC5`).
3. It formats `"%s%s.webm"` with the video directory (`001B7FFD`–`001B8015`).

`g_pathTables[0x1C]` is **`01ECB4D0`**, installed by `ResourcePath_Init` (`002DFAF9` `lea`, `002DFB00`
store). Its even entries are the PS2 `movie_finish\…\<CODE>.md` paths and its odd entries the
matching `.mh` files. Only the basename survives, so the language directory in the path does not matter.

[`members/movie_fade_schedule_names.py`](members/movie_fade_schedule_names.py) →
[`members/movie-fade-schedule-names.tsv`](members/movie-fade-schedule-names.tsv) joins the three.
Its controls: the `st2e` header declares 49 × 8, and byte `+0` equals the row index in all 49 rows.

| ids | movie codes |
|---|---|
| 0–9 | `OPN` `NAL` `DLS` `RLV` `LVB` `ARC` `ENS` `LHO` `CLS` `LWG` |
| 10–19 | `ALX` `VAF` `LVA` `WEN` `DRC` `END` `STR_STA` `DIS` `RAR` `STM` |
| 20–29 | `LRF` `EST` `BAR` `ESC` `BAH` `EPL` `MEM` `VAD` `CHV` `DED` |
| 30–39 | `VNP` `SCB` `WAR` `BLU` `BLB` `GRV` `RBS` `DLB` — — |
| 40–48 | — `OPD` `STF` `IVT` `SE1` `SE2` — `BD2` `ANX` |

**The schedule's all-zero rows are the movies that do not ship.**
- 45 ids have a path, and 4 (38, 39, 40, 46) have none.
- 40 `.webm` files ship, one per code, except for `DLB` (37), `OPD` (41), `SE1` (44), `SE2` (45) and
  `BD2` (47).
- The eleven all-zero rows are 0, 32, 37–41 and 44–47. **Nine of them are precisely the ids with no
  path or no `.webm`.**
- The other two, `OPN` (0) and `WAR` (32), ship and simply take no scheduled fade.

**Why 25 and 43 differ.** In the row's own fields:
- **25, `EPL`: `1E 0F CD 96`**. It fades in over 15 frames from frame 30, then runs a **205-frame
  fade-out ending 150 frames before the movie ends**. Every other fade-out is at most 60 frames
  (`3C`), and every other lead at most 90 (`5A`, `END`).
- **43, `IVT`: `00 06 00 06`, flags 3**. It has only a **6-frame white fade-in from frame 0**, the
  shortest in the table. Its fade-out length is 0, so §2.4's second condition never fires and the
  white-out bit is set but unused.

Both are authored values, and the rows state what they do. **Why** the authors chose them is not in
the image.

**Not established here.** What each code's movie shows. The codes are file names, and only the
`.webm` contents would say what they depict.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (FABLE, Claude Opus 5.5, 2026-09-25)

**Resource — CLIENT.** The movie-id section above cites three things that belong to the resource
path directory: the accessor `002DF980`, its installer `ResourcePath_Init` `002DF9A0`, and the
kind-`0x1C` array `01ECB4D0`. The relationship is one-way, like the string-helper crossing OPUS
recorded in §2.2: **the movie player reads one name from Resource's table and Resource calls
nothing on this page.** The citations establish only which name an id resolves to. Nothing about
how Resource fills or serves its other 40 kinds is claimed here. Those two functions' other callers
and callees are Resource's own traffic, not edges this page's mechanism uses.

**CoreRuntimeScheduling — CLIENT, at one remove.** `ResourcePath_Init` `002DF9A0`, cited above as
the installer of the kind-`0x1C` array, is run by the boot body `0022A0B0`. The page relies only on
the array being installed before any movie plays, which boot ordering gives it. It claims nothing
about the boot body. *This paragraph covers that one edge.* The page's other CoreRuntimeScheduling
edges, from citations in earlier sections, are not dispositioned here.

These two paragraphs cover only the edges the `UQ-236` answer brings in by citing the `PApplication`
clock (`00792350`, `0079F150`, `0079D920`).

**Platform — PROVIDER.** The auto-test runner's clock is the `PApplication` run time. Its constructor, its
run start and its per-frame update read the wall clock through `005CC930` and create a platform object
through `005CD0A0`. This page relies only on what `+0x40` counts. It says nothing else about those helpers.

**Application — PEER.** The `PApplication` constructor `00792350` has one Application-layer caller,
`0015BC40`. It is named here only because the constructor is cited; the page does not describe that
caller.

`0037DEA0` (239 B) is the two-phase schedule notify `0037DDD0` runs on the `[rcx+0xC8]` record: with `+0xF0` ~~bit 8~~ bit 3 (mask `8`) clear and the `[rbp+2]`/`[rbp+1]` window reached by `[rsi+0x14]`, it fires `002EFE40(5)` then `002EFA70(0, edi, 1, [rbp+7]&1)` and sets ~~bit 8~~ that bit; the mirror block under ~~bit `0x10`~~ bit 4 (mask `0x10`) *(corrected 2026-10-02, OPUS: `0037DEA0`+0x1D `test byte ptr [rcx + 0xf0], 8`, +0x6F `or dword ptr [rsi + 0xf0], 8`, +0x76 and +0xD3 for `0x10`)* does the same from `[rbp+4]`/`[rbp+3]` against `[rsi+0xC0]+0x10` with `002EFA70`'s flag from `[rbp+7]&2` - the layer's arrival markers, once each

Interior anchor `0037DF33` (function `0037DEA0`).

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-the-screen-fade-layers-and-the-movie-fad-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00264830` | 50 B | walks a pointer from `02099010` up to and including `02099520` in `0x288` steps (three records) and returns 1 at the first record whose byte `[pointer - 0x1F0]` has bit 0 set and whose byte `[pointer]` has bit 2 set; returns 0 when no record matches | `00264840`, `00264849`, `0026484E`, `00264857`, `0026485C` |
| `0026C3C0` | 30 B | sign-extends `ecx`, multiplies it by `0x288`, adds `02098E10` and tail-jumps to a 475-byte routine with that record address in `rcx` and `edx = 1` | `0026C3C3`, `0026C3C8`, `0026C3CF`, `0026C3D9` |
| `0026DE00` | 27 B | keeps `ecx`, calls `WorldTransition_GetActiveOrPendingFieldId()` and tail-jumps to a 124-byte two-argument routine with the kept `ecx` as the first argument and the returned value in `edx` | `0026DE06`, `0026DE08`, `0026DE0D`, `0026DE16` |
| `00283B30` | 115 B | switches on dword `[rcx + 0xE4]`: when it is 1 and a 23-byte nonzero-to-1 predicate returns nonzero, it calls a 108-byte four-slot byte refresher and stores 2 to `+0xE4`; when it is 2 and the same predicate returns nonzero, it clears bit 0 of dword `+0xE8` and stores 1 to `+0xE4` when that bit was set, else stores 0 to `+0xE4`; any other value, or a zero predicate, returns with no store | `00283B39`, `00283B5F`, `00283B75`, `00283B8E`, `00283B93` |
| `002EFD50` | 34 B | when dword `022BDEB8` is nonzero, passes it in `ecx` to a 58-byte dispatcher keyed on the top four bits of its argument and then stores 0 to `022BDEB8`; otherwise returns without a call | `002EFD54`, `002EFD5C`, `002EFD5E`, `002EFD63` |
| `002EFE10` | 34 B | stores 1 to byte `022BDD5C` and stores `cl`, `dl`, `r8b` and `r9b` to bytes `022BDD58`, `022BDD59`, `022BDD5A` and `022BDD5B` | `002EFE17`, `002EFE1D`, `002EFE23`, `002EFE2A` |
| `0035D010` | 14 B | stores 1 to dword `022CA45C` when `ecx` is zero, else 0 | `0035D012`, `0035D014`, `0035D017` |
