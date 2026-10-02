---
system: SQEX::Sd sound driver — architecture
category: 18-Audio
status: DOCUMENTED — every register row is closed (owner re-status 2026-09-30, OPUS): the Sab/Mab/AudioBinaryFile layouts (G-2) are SUPERSEDED 2026-09-27 (OPUS, class-1 ruling; the Sequence payload's reader is not found) and Magi::Music transitions (G-5) are ANSWERED 2026-09-27; the slot-43 selections (G-1) answered 2026-09-17, Lay spatial evaluation (G-4) answered 2026-09-17 by cross-reference, and ConfigFile routing (G-3) answered 2026-09-27 (WC-1 verification); the mix path is read at tier 1 (§2a–2e) and its remainder (SD-20 / SD-21) and which options rows send the three volume commands (SD-22) answered 2026-09-30
owner_layer: PrimaryOwner:Audio / CodeDomain:Audio.SQEXSd
evidence_tier: 4
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 22 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-30
audit:
  passes: 1
  last_pass: 2026-09-02
  last_pass_state: falsification-pass
  crossref_clean: false
  reopened_count: 0
---

# SQEX::Sd sound driver — architecture

> FFXII's audio is not generic middleware. It runs on **SQEX::Sd**, Square Enix's own sound
> driver, and the shipping binary names its classes.

~~**Status is PARTIAL and the scope limit is important.**~~ *(Superseded: the status is DOCUMENTED, owner re-status 2026-09-30; the scope note below is history. Struck 2026-10-01, OPUS.)* This document establishes the
**class architecture** from recovered RTTI — which classes exist, how they inherit, how many
virtual methods each has. ~~It does **not** yet document mechanism: no function body in this
subsystem has been read. Everything here is structure, at evidence tier 4. Mechanism claims
must wait for tier-1 body evidence and will be added as separate documents.~~
*(Corrected 2026-09-30, SWE2-DATA: the banner predates the body reads. The mix path — the source voice render, its buffer queue, the three voice classes, the voice lifecycle and the voice factory — is read at tier 1 in §2a–§2e, and the selection, spatial, routing and music questions of §7 are answered on the pages it links. The class inventory, the family counts and the method counts stay tier 4.)*

## 1. What the player sees

Sound in FFXII does more than play clips.

Attack the same enemy repeatedly and the impact sound **varies** rather than repeating
identically. Walk across a zone and the ambience **shifts** — a river gets louder as you
approach it, a cave has its own tone, and the change tracks where you actually are, not just
which map you loaded. Music **transitions** between exploration and battle rather than
cutting. The Config menu's separate volume sliders behave independently because the driver
genuinely routes sound through ~~separate buses~~ separate Categories.

~~All of that is the driver's structure showing through: there are distinct kinds of sound
object, and which one an effect uses determines how it behaves in play.~~

*(Corrected 2026-09-30, SWE2-DATA: each of these is now traced, and three are not what the class names suggested. (1) Weapon-swing and voice variety comes from the character's sound emitter choosing which trigger to ask for, with the presentation PRNG ([how an animation makes a sound](how-an-animation-makes-a-sound.md) §2); every shipped sound record builds the base `Sound`, so the Random / Order / Cycle / Switch objects are never constructed ([the variant-selection page](Sound-Selection/sound-variant-selection.md) §12). (2) Positional ambience is the `Lay` sources' evaluation against the one listener (G-4, §7). (3) The battle music change is a track substitution with a 2.0 s volume fade, not a `Magi` transition (G-5, §7). (4) The three Config sliders set the volume layer of Categories 1 / 2 / 3 — music, sound effect, voice (G-3, §7); the `bus ` chunk builds one shipped `Master` root bus, so the sliders do not select buses ([sead.win.config](Sound-Bank-And-Voice-Formats/sead-win-config.md) §6d).)*

## 2. Native mechanism

~~**Not yet read.** No body evidence exists for this subsystem.~~ What follows is the recovered
class architecture and what it structurally implies — clearly separated from proven mechanism. *(Corrected 2026-09-30, SWE2-DATA: body evidence exists; see the note below and §2a–§2e.)*

> **Superseded for the mix path, 2026-09-20 (FABLE, Claude Opus 5): body evidence now exists.** The driver's
> device-clock tick, its two mixers, both destination finishes and the **source voice render** are read from the
> shipping bytes — the tick and the mixers on
> [the identification page](sead-function-identification.md), the render in section 2a below. The paragraph above
> still holds for everything else on this page; it no longer holds for how a voice reaches the output buffer.

### 2a. What a source voice does in one tick — `007E0B60`, 6,716 B (FABLE, Claude Opus 5, 2026-09-20)

*Read for its control flow and its record access, not for its two SIMD decode kernels. `rbx` is the voice.*

**It refuses twice, then computes its step.** `dword[+0x80]` must be **3** — the playing state; 4 is the retire state
the tick unlinks on — and `dword[+0xB0]` must be positive. Then the resampling step is the voice's own sample rate
`dword[+0x94]` divided by the device rate (exactly `1.0` when they match, no division), multiplied by the pitch
`float[+0x108]`. **A step of zero or less makes it `memset` its output buffer `[+0x210]` and return**
(`007E0C0D`–`007E0C32`): a stopped voice emits silence, never stale samples.

**It starts sample-accurately, and it can start in a later tick.** The position it uses is `double[+0x98]` when
`double[+0xA0]` is non-negative, and `[+0xA0]` itself when that is negative — so **`+0xA0` is a start offset
counted in source samples, negative until the voice is due**:

- if `[+0xA0]` is still below `-frames × step`, the voice is not due anywhere in this tick: it adds
  `frames × step` to `[+0xA0]`, zeroes the whole output buffer and returns (`007E0DE3`–`007E0E18`);
- otherwise, while `[+0xA0]` is negative it advances it by one step per frame and **writes one frame of silence**
  (`rep stosd` of the channel count) before decoding anything (`007E0E34`–`007E0E6F`).

**It fires one marker callback.** Under its own critical section at `+0x30`, if the object at `[+0x88]` exists and
`dword[+0xA8]` is a non-negative sample index that **this tick's span will cross** — the test is
`[+0xA8] <= position + frames × step` — it calls that object's slot 2 and **disarms the marker by storing `-1`**
(`007E0C81`–`007E0CC5`). So a marker fires once, in the tick that reaches it, not after the samples are heard.

**It ramps its gain across the tick.** `float[+0x104]` is the current gain and `float[+0x100]` the target; the
per-frame increment is `([+0x100] − [+0x104]) / frames` (`007E0E71`–`007E0EBE`), and the gain actually reached is
stored back to `+0x104` at the end (`007E23D1`). *The ramp is per tick, so a volume change lands over one device
buffer rather than as a step.*

**Its source format is a two-way switch.** `dword[+0x90]` equal to **1** selects one decode path and a sample
scale of `1 / 32768` — 16-bit integer source — and anything else selects the other path with a scale of `1.0`
(`007E0CD8`–`007E0CEF`, `007E0EC3`). Those two paths are most of the body's 6,716 bytes and are **not read here** (their control flow is read in §2b; the SIMD arithmetic is residue `SD-21`).
A per-channel gain table of `dword[+0xAC]` entries is built from `+0x10C` with that scale folded in
(`007E0CEF`–`007E0D40`).

**Then it hands the buffer on**, exactly as a destination does: zero-fill the unwritten tail, run its own effect
chain (`dword[+0x290]` entries from `+0x270`), and walk its sends (`dword[+0x268]` records of `0x10` bytes from
`+0x218`, each a destination and a `float` gain at `+8`), letting each destination's own kind pick the mixer. That
half is on [the identification page](sead-function-identification.md).

**The voice record, as this one body uses it.** *These are the fields `007E0B60` touches — a census of one
function, not the record's layout:*

| field | width | role |
|---|---|---|
| `+0x30` | — | the voice's own critical section |
| `+0x80` | dword | state; **3** plays, 4 retires |
| `+0x88` | qword | the marker callback object |
| `+0x90` | dword | source sample format; **1** is 16-bit |
| `+0x94` | dword | source sample rate |
| `+0x98` | double | play position, in source samples |
| `+0xA0` | double | start offset; negative until the voice is due |
| `+0xA8` | dword | marker sample index, `-1` once fired |
| `+0xAC` | dword | the per-channel gain table's entry count |
| `+0xB0` | dword | a count that must be positive for the voice to render |
| `+0xB4`, `+0xB8` | dword | running indices the decode paths advance by the channel count |
| `+0x100`, `+0x104` | f32 | gain target and current gain |
| `+0x108` | f32 | pitch |
| `+0x10C` | — | the per-channel gain table |
| `+0x210` | qword | the voice's output buffer |
| `+0x218`, `+0x268` | —, dword | the send records and their count |
| `+0x270`, `+0x290` | —, dword | the effect chain and its count |
| `+0x294` | f32 | the decode paths' hottest state — 31 reads, 13 writes — **not named here** |

### 2b. Where a voice's samples come from, and how they become output (FABLE, Claude Opus 5, 2026-09-20)

*Closing the previous section's own "not read": the decode paths' control flow, the four fields they carry, and
what `+0xB4` / `+0xB8` / `+0x58` are.*

**The source is a two-slot queue of buffer descriptors.** `+0xC0` is an array of `0x20`-byte descriptors — the
render addresses it as `rbx + (dword[+0xB4] + 6) × 0x20` (`007E0DA9`–`007E0DCC`), which is `+0xC0` plus the slot
index times the stride. A descriptor holds the data pointer at `+0x00`, its size in bytes at `+0x08`, and a tag at
`+0x18` that is handed back to the owner. The queue's state is three fields:

| field | role |
|---|---|
| `dword[+0xB0]` | **how many buffers are still queued** — the same field the render refuses on when it is not positive |
| `dword[+0xB4]` | the **current slot**, advanced as `(index + 1) & 1` with a sign fixup — so exactly **two** slots |
| `dword[+0xB8]` | the **byte offset** into the current buffer |

**Exhausting a buffer is what asks for the next one.** When `size − offset` yields no whole frames the render takes
the queue lock at `+0x58`, and if `+0xB0` is positive it decrements it, zeroes `+0xB8`, toggles `+0xB4`, releases
that lock, takes the **callback** lock at `+0x30` and calls `[+0x88]`'s **slot 1** with the retired descriptor's
`+0x18` tag (`007E0F21`–`007E0F99`, repeated verbatim in the resampling path at `007E1282`–`007E12E0`). *So `+0x30`
and `+0x58` are two different critical sections — one for the owner callback, one for the queue — and the callback
is made with the queue lock released.* The same object's **slot 2** is the marker callback of §2a.

**Frames per buffer come from the source channel count, not the device's.** The divisor is
`dword[+0xAC] × 2` in the 16-bit path (`007E0EE6`–`007E0EF9`) — two bytes per sample per source channel.

**Unity rate is a special case.** The render compares the step against `1.0` (`007E0EDC`) and takes a separate path
when they are equal, which also **stores `1.0` into `float[+0x294]`** (`007E11F9`). Everything else resamples.

**The resampler is linear, and it carries state across ticks.** `float[+0x294]` is the **fractional position inside
the current source frame**; the loop runs while it is below `1.0` and advances it by the step each output frame,
adding the step to `double[+0x98]` at the same time. The sample it interpolates from is the array at `+0x298` —
**one entry per source channel**, `word` in the 16-bit path (`+0x298`, `+0x29A`, …) and `float` in the other
(`007E1F0F`–`007E1F1C`) — and the arithmetic is exactly

```asm
007E1399  movsx ecx, word ptr [rbx + 0x298]   ; previous
007E13A3  movsx eax, word ptr [r10]           ; current
007E13AC  sub   eax, ecx
007E13C8  mulss xmm1, dword ptr [rbx + 0x294] ; (current - previous) x fraction
007E13D0  addss xmm1, xmm0                    ; ... + previous
```

**and the array is refilled from the tick's last source frame before returning** — a word loop at
`007E1221`–`007E1230` and a dword one at `007E237F` — so interpolation continues across the tick boundary instead
of restarting. **The three decode paths are specialisations by source channel count**: `1`, `2`, and a general
loop (`007E1378`, `007E143A`, `007E154A`).

**The output is always eight floats per frame.** Each frame stores two `xmm` rows to the voice buffer and advances
by the device channel count, multiplying by the per-channel gain vectors built from `+0x10C` **and** by the ramped
gain of §2a, which the same loop advances by its per-frame increment (`addss xmm6, xmm12`). *So the per-channel
table, the tick-long ramp and the sample scale are all applied in one multiply chain, and the `1 / 32768` of the
16-bit format is folded into the table rather than applied per sample.*

**Not read here:** the SIMD bodies of the three paths beyond the arithmetic above (`SD-21`); where a voice's buffers, sends
and markers are filled in — all of that is on the producer side of `[+0x88]` (`SD-20`); ~~whether the two queue slots are ever
resized.~~ *(Corrected 2026-09-30, SWE2-DATA: the depth is fixed, not resizable: the enqueue `007E0A40` refuses a third buffer when `dword[+0xB0]` stands at 2, §2c.)*

### 2c. The three voice classes are named, and the graph is theirs (FABLE, Claude Opus 5, 2026-09-20)

*The RTTI this page recovered from vtables answers what §2a and §2b read from bodies — and it settles the
identification page's `CoreSourceVoice::Render` anomaly outright.*

**Three complete-object locators, three vtables, and each one's slot 2 is a getter that names its class's
counter:**

| vtable | class | slots | slot 2 | which makes it |
|---|---|---:|---|---|
| `01CB8360` | **`CoreSourceVoice`** | 17 | — | the source §2a and §2b read; its slot 9 is `007E0A40`, the buffer enqueue |
| `01CB82D0` | **`CoreSubmixVoice`** | 7 | `007E0050` = `word[rcx + 0xCC]` | the **`+0xCA`** destination class |
| `01CB8290` | **`CoreMasterVoice`** | 7 | `007DFA60` = `word[rcx + 0x74]` | the **`+0x72`** destination class |

*The cross-check is independent of the offsets themselves:* `CoreSubmixVoice`'s slot 5, `007E0100`, bounds an
index against `dword[rcx + 0x88]` — the send count the identification page reads on the same object at `+0x38` /
`+0x88`.

**So the mix graph is a three-level one, and the tick walks it outside in:**

```
CoreSourceVoice  --send kind 2, mixer 007E0550-->  CoreSubmixVoice  --its own sends-->  CoreMasterVoice
       |                                                                                      ^
       +-------------------- send kind 1, mixer 007DFE30 -------------------------------------+
```

reset master (`007DFA50`) → reset submixes (`007E0040`) → render sources (`007E0B60`) → finish submixes
(`007E01F0`) → finish master (`007DFBB0`). *A source may address the master directly, which is what the send
record's kind-1 arm is for.*

**And the buffer enqueue is `CoreSourceVoice` slot 9.** `007E0A40(voice, data, sizeBytes, tag, startSample)`
refuses a voice whose state is 0 or 4, refuses when `dword[+0xB0]` already stands at **2** — so the queue depth of
§2b is a hard limit, not an observation — and refuses a size that is not a whole number of source frames, the
frame being `(format == 1 ? 2 : 4) × dword[+0xAC]` bytes. When it is the **first** buffer it seeds
`double[+0x98]` from the fifth argument, so a voice starts at a caller-chosen sample. Then, under the queue lock
`+0x58`, it fills slot `(+0xB4 + +0xB0) & 1` and increments the count.

**Not read here:** which class implements `ICoreSourceVoiceCallback` in practice — `ExternalSourceVoice`
(`01CB5238`) derives from it, but that this is the object at a voice's `+0x88` is not shown here. Registered as `SD-20`.

### 2d. The `CoreSourceVoice` lifecycle, from its own vtable (FABLE, Claude Opus 5, 2026-09-20)

*Five of the seventeen slots plus the constructor account for the whole life of a voice, and they explain the two
state values §2a and the tick read off each other.*

| slot | body | what it does |
|---:|---|---|
| — | `007E0650` | **construct**: install the vtable, **initialise three critical sections** at `+8`, `+0x30` and `+0x58`, disarm the marker with `dword[+0xA8] = -1`, zero the state, the callback, the position, the queue fields, the buffer and both list counts, and set **`float[+0x100]`, `float[+0x104]`, `float[+0x108]` and `float[+0x294]` all to `1.0`** — gain target, current gain, pitch and the resampler's fraction. The previous-sample array `+0x298`–`+0x2B7` is zeroed as four qwords, which bounds it at `0x20` bytes |
| — | `007E0980` | **open**: refuses a channel count above **8** or a zero fifth argument, stores the caller's callback into `+0x88` and the caller's output buffer into `+0x210`, and sets the state to **1** |
| 3 | `007E2710` | **start**: under the `+8` lock, `state ← 3` |
| 4 | `007E2760` | **pause**: under the same lock, `state ← 2` |
| 9 | `007E0A40` | **queue a buffer**, with the validation above |
| 5 | `007E07F0` | **stop**: under `+0x30` and then `+8`, `state ← 4`, callback cleared, effect count cleared |
| 10 | `007E0970` | a getter for `float[+0x100]` — which is what makes that field the **volume**, not an internal |

**So the state field is a five-value machine**, and three different entry points share one guard for it:

```
0  constructed           start, pause and queue all test  state & ~4 != 0
1  opened                - true for 1, 2 and 3, false for 0 and 4 -
2  paused                so a voice can only be driven once opened and before it is closed
3  playing   <- the only state the tick renders
4  closed    <- the only state the tick retires
```

*That is why `007E07F0` is the whole of "stop": setting 4 hands the voice to the tick, which unlinks it, calls its
deleting destructor and decrements the list count.* **The stop takes both locks and the render's retire path takes
only the list's**, so the two cannot race over the same voice.

### 2e. Where a voice comes from — the factory `007AEA20` (FABLE, Claude Opus 5, 2026-09-20)

**One function builds every `CoreSourceVoice`**, and it is the only caller of both the constructor and the open of
§2d (`007AEA6C` / `007AEAD7`, and again at `007AEB43` / `007AEBAE` for its second path). A byte argument on the
stack picks between the two paths. On each one it:

1. takes an object from a **pool** — `007DF750(02EAD250)` — and returns failure if the pool is empty;
2. constructs it in place with `007E0650`;
3. takes a **second** object from another pool, `007DF750(02EAD200)`, and passes it to open as the voice's output
   buffer — so the buffer at `+0x210` is pool-owned, not the caller's own memory;
4. opens it with the caller's channel count, format and callback plus that buffer;
5. and then, **under the same critical section `02EAD138` the tick uses for its source walk**, links the new voice
   into the list at `02EAD2A0`.

*So a voice is visible to the tick the moment the factory returns, and the factory takes the tick's own lock to
make it so.* Its three callers are `007B9050`, `007DCE20` and `007EBAD0` — the last of which the assert-string
table names **`Voice::Initialize`**.

**Not read here:** the other eleven `CoreSourceVoice` slots and the six each on `CoreSubmixVoice` and
`CoreMasterVoice`; the pool allocator `007DF750` and what distinguishes the factory's two paths; who calls start
and queue once the factory has returned. Registered as `SD-21` (with §2a's SIMD kernels).

### The sound-object hierarchy — proven by shared vtable pointers

Six classes form one family. Each has a **44-slot vtable**, and the variants share most of
their implementations with `Sound`:

| Class | Vtable slots | Slots shared with `Sound` | Overridden |
|---|---:|---:|---:|
| `SQEX::Sd::Driver::Sound` | 44 | — (base) | — |
| `SQEX::Sd::Driver::RandomSound` | 44 | 42 | 2 |
| `SQEX::Sd::Driver::OrderSound` | 44 | 42 | 2 |
| `SQEX::Sd::Driver::SwitchSound` | 44 | 42 | 2 |
| `SQEX::Sd::Driver::CycleSound` | 44 | 39 | 5 |
| `SQEX::Sd::Driver::VariationSound` | 44 | 39 | 5 |

Per-slot detail — which variant overrides what (`*` = differs from the `Sound` base):

```
slot | Sound     RandomSound  OrderSound   CycleSound   SwitchSound  VariationSound
-----|------------------------------------------------------------------------------
   0 | 007BD020  007E50F0*    007E5860*    007E5D30*    007E6750*    007E5740*
  36 | 007BD990  =            =            =            =            007E57C0*
  37 | 007BD0A0  =            =            =            =            007E57B0*
  38 | 007E57B0  =            =            =            =            007E5800*
  39 | 007E5800  =            =            007E57B0*    =            =
  40 | 007BDDA0  =            =            007E65B0*    =            007E57D0*
  41 | 007BD4E0  =            =            =            =            =
  42 | 007BF0A0  =            =            007E6620*    =            =
  43 | 007BD370  007E5160*    007E58D0*    007E6360*    007E67C0*    =   (base)
```

**Slot 43 is the selection method.** `RandomSound`, `OrderSound`, `CycleSound` and
`SwitchSound` each replace it with their own implementation — that single slot is what makes
them different kinds of sound. Slot 0 is the destructor, overridden per-class as always.

`VariationSound` is structurally the odd one: it **keeps the base slot 43** and instead
overrides 36, 37, 38 and 40. Whatever it varies, it does not vary by replacing the selection
method. ~~That asymmetry is proven and unexplained.~~ **Explained 2026-09-12 (FABLE):** its
slot 37 override returns false — no candidates — so the base select never walks; it stores a
parameter at bind and reports it through slot 36. Slot bodies on [the variant-selection page](Sound-Selection/sound-variant-selection.md).

`CycleSound` also overrides 39, 40 and 42 — more state than the other three variants need,
consistent with something that must remember a position between calls, ~~though that reading is
not yet proven from bodies~~. *(Corrected 2026-09-30, SWE2-DATA: proven from the bodies 2026-09-12 — slot 40 rolls a re-trigger interval, slot 42 counts it down and re-selects, slot 39 returns false (G-9, §7).)*

**This is inheritance demonstrated, not guessed.** The variants are not six independent
classes with similar names — they are one base class whose subclasses replace only a small
tail of behaviour. Everything a sound does in common (the 39–42 shared slots) is implemented
once.

The names indicate *how each variant chooses what to play* — random, ordered, cycling,
switched, varied. That reading is consistent with the structure but is **name-derived and
therefore unproven**; slot 43 is where that logic lives for four of the five variants~~, and
reading those bodies is the next step~~. *(Corrected 2026-09-30, SWE2-DATA: the bodies are read — G-1, §7 — and in the shipped banks none of the four variant classes is ever built: every sound record's class byte `+4` is 0 or 1, the base `Sound` ([the variant-selection page](Sound-Selection/sound-variant-selection.md) §12).)*

### Class families

| Family | Classes | Apparent role |
|---|---:|---|
| `SQEX::Sd::Driver` | 73 | core engine: sounds, tracks, voices, banks |
| `SQEX::Sd::ConfigFile` | 20 | buses, categories, curves, effects |
| `SQEX::Sd::MabFile` | 17 | a container format |
| `SQEX::Sd::Lay` | 14 | spatial placement of sound in the world |
| `SQEX::Sd::SabFile` | 10 | a container format |
| `SQEX::Sd::Magi` | 7 | music |
| `SQEX::Sd::AudioBinaryFile` | 6 | binary asset chunks |

### Spatial audio — `SQEX::Sd::Lay`

The family that most directly explains what a player hears while moving:

| Class | Methods | Apparent role |
|---|---:|---|
| `SQEX::Sd::Lay::DynamicSound` | 33 | |
| `SQEX::Sd::Lay::PolygonSound` | 30 | sound bound to a region |
| `SQEX::Sd::Lay::PointSound` | 30 | sound at a world point |
| `SQEX::Sd::Lay::AmbientSound` | 29 | |
| `SQEX::Sd::Lay::DirectionSound` | 28 | |
| `SQEX::Sd::Lay::SoundSourceObject` | 26 | |

A driver distinguishing *point* from *polygon* from *direction* sources is placing audio
geometrically in the world ~~— which is why ambience tracks your position rather than the map~~. *(Corrected 2026-09-30, SWE2-DATA: that was an inference from class names; the evaluation itself is read — each source class's slot 34 computes its effective position against the one `Lay::Listener` at `[02EADE08]` — `PointSound` and `DynamicSound` by distance gated on the audible range, `PolygonSound` by the nearest-edge distance, `AmbientSound` and `DirectionSound` without a distance (G-4, §7; [the spatial-audio page](the-spatial-audio-object-model.md)).)*

### Other notable classes

| Class | Methods |
|---|---:|
| `SQEX::Sd::Magi::Music` | 32 |
| `SQEX::Sd::Driver::SoundTrack` | 16 |
| `SQEX::Sd::Driver::MaterialTrack` | 16 |
| `SQEX::Sd::Driver::Core::CoreSourceVoice` | ~~16~~ 17 *(the vtable `01CB8360` has slots 0-16; corrected 2026-10-01, OPUS)* |
| `SQEX::Sd::Driver::StreamingBank` | 14 |

`ConfigFile` exposes `Bus`, `BusChunk`, `BusEffect`, `Category`, `CategoryChunk`,
`CategoryLayerChunk`, `Curve`, `CurveChunk` — bus/category routing with curves, consistent
with independent volume categories.

## 3. Key addresses

~~Deliberately empty. This document makes no per-function claims yet; the recovered
`address → class::slot` mapping lives in `Tools/work/rtti/methods.tsv` and has not been
applied to the GZF. Adding addresses here before reading bodies would imply mechanism
evidence that does not exist.~~ *(Corrected 2026-09-30, SWE2-DATA: §2a–§2e read bodies, so their addresses are listed; every row is an address this page already cites, with the section that reads it.)*

| Address | What | Where read |
|---|---|---|
| `01CB5A30` | `Sound` vtable, 44 slots (`01CB87A8` Random, `01CB8AD8` Order, `01CB8C70` Cycle, `01CB8E08` Switch, `01CB8940` Variation) | §9, tier 1 |
| `007BD370` | `Sound` slot 43, the base select (kept by `VariationSound`) | §2 table |
| `01CB8360` / `01CB82D0` / `01CB8290` | `CoreSourceVoice` / `CoreSubmixVoice` / `CoreMasterVoice` vtables | §2c |
| `007E0B60` | `CoreSourceVoice` render: one voice, one tick | §2a, §2b |
| `007E0A40` | `CoreSourceVoice` slot 9: queue a buffer (depth 2) | §2c |
| `007E0650` / `007E0980` | construct / open | §2d |
| `007E2710` / `007E2760` / `007E07F0` | slots 3 / 4 / 5: start / pause / stop | §2d |
| `007E0970` | slot 10: the volume getter (`float[+0x100]`) | §2d |
| `007AEA20` | the voice factory, the only caller of construct and open | §2e |
| `007DF750` | the pool take the factory calls (`02EAD250` voices, `02EAD200` output buffers) | §2e, not read |
| `007DFA50` / `007E0040` / `007E01F0` / `007DFBB0` | reset master / reset submixes / finish submixes / finish master | §2c |
| `007E0550` / `007DFE30` | the send mixers for kind 2 (submix) and kind 1 (master) | §2c |
| `007E0050` / `007DFA60` / `007E0100` | `CoreSubmixVoice` slot 2 / `CoreMasterVoice` slot 2 / `CoreSubmixVoice` slot 5 | §2c |

## 4. Data structures and formulas

~~None proven. No formulas have been recovered from this subsystem — no body has been read.~~ *(Corrected 2026-09-30, SWE2-DATA: the voice-side structures and formulas below are read in §2a–§2d; this section collects them.)*

```
CoreSourceVoice (fields the render, the enqueue and the lifecycle bodies touch - §2a-§2d; a census, not the full record)
  +0x08 / +0x30 / +0x58   three critical sections: state / owner callback / buffer queue
  +0x80  dword   state: 0 constructed, 1 opened, 2 paused, 3 playing (the only rendered state), 4 closed (retired by the tick)
  +0x88  qword   the owner callback object (slot 1 per retired buffer, slot 2 at the marker)
  +0x90  dword   source sample format, 1 = 16-bit
  +0x94  dword   source sample rate
  +0x98  double  play position (source samples);  +0xA0 double start offset, negative until due
  +0xA8  dword   marker sample index, -1 once fired
  +0xAC  dword   channel count (the per-channel gain table's entries); open refuses more than 8
  +0xB0 / +0xB4 / +0xB8   queued-buffer count (max 2) / current slot (& 1) / byte offset
  +0xC0  0x20-byte descriptors x 2: +0x00 data, +0x08 size in bytes, +0x18 tag returned to the owner
  +0x100 / +0x104 / +0x108   volume target / current gain / pitch (all 1.0 at construction)
  +0x210  output buffer (pool-owned, 02EAD200)
  +0x218 / +0x268   send records {destination, +8 f32 gain}, 0x10 bytes each, and their count
```

**Resampling step** (§2a): `step = (sourceRate == deviceRate ? 1.0 : sourceRate / deviceRate) × pitch`; a step ≤ 0 renders silence. **Gain ramp** (§2a): per-frame increment `(target − current) / frames`, reached value stored back to `+0x104`. **Frame size** (§2c): `(format == 1 ? 2 : 4) × channels` bytes. The device mixes eight-channel interleaved float, a fixed number of frames per tick ([the identification page](sead-function-identification.md), the tick's units).

The container formats are placed elsewhere: the `.sab` chunk directory on [the SAB container page](Sound-Bank-And-Voice-Formats/sab-sound-bank-container.md), the `SabFile::Sequence` / `SoundSequenceInfo` / `Sound` fields and every version threshold on [the variant-selection page](Sound-Selection/sound-variant-selection.md) §12 (G-2 SUPERSEDED, G-13), and the `ConfigFile` chunks on [sead.win.config](Sound-Bank-And-Voice-Formats/sead-win-config.md).

The container formats (`SabFile`, `MabFile`, `AudioBinaryFile`) have named chunk classes
(`ChunkTableElement`, `Material`, `MaterialChunk`, `SoundZeroOneParam`, `ZeroOne`,
`USABTRACKHEADER`, `USABTRACKCHUNKHEADER`, `USABSOUNDSEQUENCEINFO`) which imply a chunked
layout, but no offsets or widths are established.

## 5. Call chain

~~Not established. No call chain for this subsystem has been derived.~~ *(Corrected 2026-09-30, SWE2-DATA: two chains are read; every edge below is a direct call found by the raw `E8`/`E9` index, except the two virtual calls marked.)*

```
the mix path (runs on the device clock)
  007AEF30  device init: installs 007AF740 as a device callback (lea at 007AEFEC)
    007AF740 -> 007B0000                      the per-tick voice pass (call 007AF8A4)
      walk 1  007DFA50  reset master          (007B004C)
      walk 2  007E0040  reset submixes        (007B0086)
      walk 3/4  007E0B60  render each source  (007B01D8, 007B02CD); state 4 is retired instead
      walk 5  007E01F0  finish submixes       (007B0306)
      walk 6  007DFBB0  finish master         (007B034C)

where a voice comes from
  007B9050 (007B91E7) | 007DCE20 (007DCF92) | 007EBAD0 Voice::Initialize (007ED332)
    -> 007AEA20  factory -> 007E0650 construct (007AEA6C / 007AEB43), 007E0980 open (007AEAD7 / 007AEBAE)

how a sound picks and arms what plays (the Driver::Sound family)
  007BDFA0 (007BE080) | 007BF0A0 slot 42, the per-update (007BF8CB)
    -> 007BD120  the sound-instance stepper -> call [vtable + 0x158] = slot 43 (007BD205; virtual)
      -> 007BD370 / 007E5160 / 007E58D0 / 007E6360 / 007E67C0   the selects
        -> 007BD240  the trigger (14 call sites, all in the selects and 007E5E80)
          -> 007E7300  the sequence arm (007BD333)
```

The game side above `007BDFA0` is on [how a sound request becomes a voice](Audio-Boundary/how-a-sound-request-becomes-a-voice.md) and [the sound trigger](Sound-Selection/sound-trigger.md); the chain from an armed sequence down to a voice (the per-sequence update and the voice pass) is G-19 in the register *(answered; OPUS 2026-09-30 pointer)*.

**Known boundary:** `Boundary.Audio.NativeSupport` carries 177 functions and
`Boundary.CrossSubsystem.NativeSupport` 35, so the audio boundary into the rest of the engine
is substantial and already partially classified. Mapping it is a prerequisite for any
multiplayer audio work.

## 6. Modding notes

Provisional — structure only. *(2026-09-30, OPUS: no longer structure only; the notes below rest on the §2a–§2e body
reads and the answered §7 rows.)*

- **Sound-variant behaviour lives in vtable slots 36–43.** If you want to change how a sound
  picks what to play, that is where the family differs; the other 36+ slots are shared and
  changing them affects every sound. *(Corrected 2026-09-30, SWE2-DATA: in the shipped banks only the base `Sound` is built, so only its slots 36–43 run; which class is built is the sound record's byte `+4` ([the variant-selection page](Sound-Selection/sound-variant-selection.md) §12).)*
- **A voice's volume and pitch are two floats** (`CoreSourceVoice` `+0x100` target, `+0x108` pitch, §2a / §2d): a volume change reaches the output over one device buffer, never as a step.
- **`Lay` classes are the spatial layer.** Positional audio behaviour belongs there, not in
  `Driver`.
- **Do not assume generic middleware.** This is not FMOD or Wwise; conventions from those do
  not transfer.
- **XIIOnline:** untouched territory. Audio is local presentation and almost certainly should
  not be networked — but that is a reasoned expectation, not a finding, and the boundary has
  not been mapped.

## 7. What is not known

Nearly everything about mechanism. Specifically:

- [x] ~~What the four selection implementations at **slot 43** actually do. Open question **G-1**.~~ **Answered 2026-09-17 (FABLE)** — `SwitchSound` a half-open range match (2026-09-02); Random, Order and Cycle read whole: sets of consecutive candidates sharing a group byte, Random's weighted roll with an anti-repeat, Order's cursor over the unweighted sets, Cycle's refusal of groups still sounding; the class comes from the sound record's byte `+4` ([the variant-selection page](Sound-Selection/sound-variant-selection.md) §12).
- [x] ~~Why `VariationSound` keeps the base slot 43 and overrides 36/37/38/40 instead. **G-8**.~~ **Answered 2026-09-12** — no candidates (slot 37 false), a stored parameter instead ([the variant-selection page](Sound-Selection/sound-variant-selection.md)).
- [x] ~~Why `CycleSound` additionally overrides 39, 40 and 42. **G-9**.~~ **Answered 2026-09-12** — the timed re-trigger: slot 40 rolls the interval, slot 42 counts it down and re-selects ([the variant-selection page](Sound-Selection/sound-variant-selection.md)).
- [x] Layout of the `SabFile` / `MabFile` / `AudioBinaryFile` container formats. **G-2**. *(closed — the register row is ~~WITHDRAWN~~ **SUPERSEDED** 2026-09-27 (OPUS, class-1 ruling): every `Sequence` field is placed or profiled over all 11,165 records and the payload's `+0x28` / `+0x2C` reader is not found; the register word corrected 2026-09-30, SWE2-DATA.)*
      *Narrowed 2026-09-17 (FABLE): the accessors' descriptors are the RTTI classes `SabFile::SoundSequenceInfo`, `SabFile::Sequence` and `SabFile::Sound`; the fields each reader consumes, and every version threshold per class including the `MabFile` records, are tabled on [the variant-selection page](Sound-Selection/sound-variant-selection.md) §12; the sequence payload's readers are not found.*
- [x] ~~How `ConfigFile` bus/category/curve routing works, and its relationship to the Config
      menu's volume options. **G-3**.~~ **Answered 2026-09-27** — WC-1 verified
      ([sead-win-config.md](Sound-Bank-And-Voice-Formats/sead-win-config.md) §6d/§7,
      record `../_index/candidates/wc1-eps-preset-fields/`).
      *Narrowed 2026-09-14 (FABLE), not answered: the volume options are read; the `ConfigFile` chunk format is not.*
      *Correction 2026-09-27 (SWE2-DATA): the chunk format **is** read — [sead-win-config.md](Sound-Bank-And-Voice-Formats/sead-win-config.md)
      (re-derived and its one gap closed this pass: `007AE410` validates `scnf` before the copy, §6b). What stays unread is the
      routing semantics the row asks about — `bus `/`eps `/`curv` field meanings and the bus→category graph.*
      *Update 2026-09-27 (SWE2-DATA): `mcr ` is decoded — a bytecode bank of same-key collision
      policies executed by `007B31A0` from descriptor macro slots at start/stop/teardown; its action
      opcodes resolve `02EAD008[]` (the Category table built from `ctgr`) — sead-win-config.md §6c.*
      *Update 2026-09-27 (SWE2-DATA): the routing semantics are now read too — §6d: `hcam` seeds the
      mixer (rate 44,100, `+1` = 16); `bus ` builds the mixer graph (one shipped `Master` root bus,
      sends + nine dormant insert-effect classes); `eps `/`epsp` are the effect-parameter and
      bus-automation preset chunks (`epsp` empty but live — driven by action type `0x30`;
      stream B = `{busIdx, fxSlot, epsPresetIdx}` records); `curv` is dead-authored — bound into ramp
      `+0x38` by nine Sound binders but never sampled (fades run the fixed six-kind `007A9E50`
      easing table on `slot+0x1C`, tick `007CD000`); `ctgr +0x06` is dead-authored; the macro descriptor is
      the `.sab` `SabFile::Sound` record (only six `se000` records bind macros — all start-mode);
      `02EAD560` is the live-object list populated by registrar `007B2CB0`.*
      - **Three Category volumes.** Settings commands **`0x13` / `0x14` / `0x15`** (`002407F0` arms `002408F1` /
        `00240902` / `00240913`) call `002DE0B0` / `002DE290` / `002DE310`. Each clamps the value to `0..100`, stores it
        as a word at `+0x08` / `+0x0A` / `+0x0C` of the saved options record `*(0215E6E0)`, and passes `value / 100.0`
        with category **1 / 2 / 3** to `001DBA60` (thunk `002DF2B0`) → `00210ED0`. `00210ED0` queues SEAD action
        type 3 with layer 0 and fade 0 through `007A45C0`.
      - **The category numbers are named.** The debug menu labels its three category mute toggles (`001D1660` cases
        `0xCD` / `0xCE` / `0xCF` → `001DBB00` with categories 1 / 3 / 2) **`Music`**, **`Voice`** and **`Sound
        Effect`** (`008FF0B0` / `008FF0C0` / `008FF0C8`, stored at `+0x798` / `+0x7A0` / `+0x7A8` by `001D0390`).
        The label offset is `0x130 + 8 × case`, checked against `Master Volume Ratio` (`+0x950`, case `0x104`) and
        `Camera Revise Enable` (`+0x9A8`, case `0x10F`, which reads `setting[0x16]`). So **command `0x13` is
        music, `0x14` sound effects, `0x15` voice.**
      - **Load and defaults.** `002DDA30` re-applies all three from the record (`002DDBB8`–`002DDC25`). `002DDE60`
        resets them to 100 before calling it (`002DDFC7`–`002DE024`).
      - **In the driver.** The type-3 arm (`007AB6F3`) resolves the category (`007AAA20`) and ramps element **index + 1**
        of the volume ramp array `+0x38` (`007AA570`). The menu therefore drives element 1, and element 0 is left to
        whatever else sets it. That array's product `007A9F40` × the Category master `+0x48` reaches each sound through
        slot 5 (`DQ-2`, [how a sound fades](Audio-Boundary/how-a-sound-fades-the-ramp-and-its-six-curves.md) §5).
        Every Category update `007AAEA0` also advances a process-wide volume ramp (fields `01F403E0`–`01F403F8`, set by
        action type 5 → `007AAD90`) and a pitch ramp (`01F40410`–`01F40428`, type 6 → `007AAC80`). It pushes them into
        each category's `+0x48` / `+0x4C` (`007AB01B` / `007AB02B`).
      - **Authored cross-check (added the same day).** `sead.win.config`'s `ctgr` chunk lists `dummy0`, `music`, `se`,
        `voice` in that order, so indices 1 / 2 / 3 are music / se / voice from the data as well as from the debug
        labels. The element's `+0x04` sizes each Category's sound list (4 / 48 / 8), and `ctgl`'s count + 1 sizes the
        volume layers ([sead.win.config](Sound-Bank-And-Voice-Formats/sead-win-config.md) §7, `WC-1`).
      - ~~**Still open:** how the `ConfigFile` `Category` / `CategoryLayer` chunks (RTTI `CategoryChunk@ConfigFile`,
        `CategoryLayerChunk@ConfigFile`) fill a Category's layers, references (`+0x58`, `007AA320`) and curves; and~~
        *(Corrected 2026-09-30, SWE2-DATA: the chunk half is read on [sead.win.config](Sound-Bank-And-Voice-Formats/sead-win-config.md) §6d: `007AAA40` builds each Category from its `ctgr` element (`+0`/`+2` name, `+4` capacity), the alias fixup `007AA320` reads `+4` only, `ctgl` is routed through `007AAA40` → `007AA110`, which names the layers and sizes them from the element count, and `curv` is bound but never sampled.)* ~~**Still open:**
        which rows of the options screen send commands `0x13`–`0x15` (the row procedures behind `00240750`) — `SD-22`.~~ *(Superseded: `SD-22` ANSWERED 2026-09-30 - options rows 0x13-0x15 send the Music / Sound Effect / Voice volume commands. Struck 2026-10-01, OPUS.)*
- [x] ~~How `Lay` spatial sources are evaluated against listener position. **G-4**.~~
      ***ANSWERED 2026-09-17 (FABLE), by cross-reference: the evaluation is read on [the spatial-audio page](the-spatial-audio-object-model.md).** Every source class overrides vtable slot 34, the spatial computation, and what it computes there is the source's effective position against the single `SQEX::Sd::Lay::Listener` at `[02EADE08]` (accessor `007BB610`; position `+0x30`, orientation matrix `+0x60`..`+0x9C`, written by the `Lay` action consumer `007BAEC0`): `AmbientSound` writes the origin and no distance (`007F1D10`), `DirectionSound` copies its stored vector (`007F1F80`), `PointSound` (`007F1A50`) and `DynamicSound` (`007F1340`) take the listener-to-source distance with one square root each, gated on the audible range at `+0xE4` and setting ~~the ready byte~~ the audibility byte *(C-SP `SA-3`; corrected 2026-10-01, OPUS)* `+0xE0` when the distance is inside it, and `PolygonSound` (`007F25E0`) measures the distance to the nearest edge with seven; slot 39 marks the three geometric classes. The page's 2026-09-07 extension extracts the polygon algorithm with its constant. Static, bodies read there.*
- [x] ~~How `Magi::Music` handles transitions between exploration and battle.~~ **G-5** - **ANSWERED 2026-09-27 (OPUS, G-5 ANSWERED 2026-09-27)**: the exploration-battle change is a track substitution with a 2.0 s fade, not a Magi transition; the only Magi mode switch the game drives is the Config soundtrack setting (command 0x26, 4.0 s, timed to the music); and no authored command sequence can post Magi SetMode / Start / End, because nothing posts the command (0x33) that starts one. Control [`g5_sequences_and_sync.py`](../_index/candidates/g5-sequences-and-sync/g5_sequences_and_sync.py). *Narrowed 2026-09-13 (FABLE): the game side is read on [the music-change page](how-the-music-changes-when-you-change-area.md) §7 (battle modes substitute `0x5B` / `0x5A`, `0x78` fade); the middleware's own sequencing is not.*
  **NARROWED 2026-09-27 (OPUS): the exploration-battle change is not a Magi transition; Magi's own mode switch is the soundtrack version. The game's change substitutes the track and ramps a volume. The setter 002DEE50 (called with 0x78 / 0x7F) runs through the MusicAudioController (00210A50 -> 00218E50, the instance whose +0x50 is the track) to 00222B70. That calls 007A81F0(handle, level / 127.0, duration / 60.0), which posts driver command 0xE, the SetVolume with a fade in seconds. So 0x78 is 2.0 seconds (read, not inferred) and 0x7F is 1.0. Magi::Music's sync-timed mode switch is driven from exactly one game place, the Config 'Music' row (Original / Reorchestrated / OST). Its setter 002DE110 stores options +0x0E (OST only when 0017E490, the 'Extra BGM status' query, allows it) and calls Audio_SetMode 002DF530. Through 00222AD0, 007A9650 posts command 0x26 {handle, mode, 4.0}, whose driver arm calls 007CAB80, the function its own diagnostics call Music::SyncTo, a mode change timed to the music by CalcSampleDelay. The other Magi transition commands, 0x21 SetMode, 0x27 Start and 0x28 End, are posted only by SEAD's record-driven wrapper 007EEA00; no game function reaches their posters. ~~Still open: what 007EEA00's records are, i.e. whether authored data drives a Magi mode change by itself, and what the 4.0 measures.~~ *(Corrected 2026-09-30, SWE2-DATA: both closed by the ANSWERED entry above — no authored command sequence can post a Magi mode change, because nothing posts the command 0x33 that starts one, and the 4.0 is the mode change's duration in seconds, timed to the music.)* Control _index/candidates/g5-music-transitions/g5_music_transitions.py (M1-M4, FAILS 0).**
- [x] ~~The audio boundary: which 177 `Boundary.Audio.NativeSupport` functions the rest of the
      engine calls to make sound happen.~~ **DISSOLVED 2026-09-02 - the premise is wrong; none
      of them does, by construction.** `Boundary.Audio.NativeSupport` is a **rejection bucket**,
      not an interface: functions considered for Audio ownership and refused, and the GFZ says so
      on them - *"owns no independent Audio state or behavior"*, *"do not count toward Audio
      owner denominator"*. Seven read from the set settle it: `00584730` is
      `if (p) _aligned_free(p)` with **2,307 non-Audio callers** *(the register recorded 2,306 on
      2026-09-02; re-derived from `edges.tsv` on 2026-09-14 it is 2,309 callers of which 2 are
      Audio-owned. The one-caller difference is a graph change, not a correction to the
      argument — at either figure the function is free(), not an audio interface.)*, `00203080` a four-float
      subtract, `00202C70` a 64-byte copy, `002E9B80` an actor-handle accessor, `003601B0` a
      bitmask set, `0036DD80` a 16-byte constant copy, `007B8C80` an empty `return`. The
      register recorded this on 2026-09-02 and this page did not; closure copied here
      2026-09-14 (OPUS) per the register's own rule that a closure is recorded on both.
      **G-6**.
- [x] ~~Whether the remaining ~1,115 Audio-owned functions without RTTI identity are internals,
      helpers, or a further unnamed layer.~~ **G-7 ANSWERED 2026-09-13 (FABLE):** neither one layer nor all SEAD — the `Audio` owner spans four upstreams and FFXII's own code: SEAD internals inside the SEAD link span, the libogg `framing.c` object inside it, Tremor with `vorbisfile.c` after it, the CRI HCA decoder at the start of `.text`, and FFXII's audio layer (`AudioController` family, `0021xxxx`), each bounded by evidence on [SEAD function identification §13](sead-function-identification.md). **G-7**.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The driver is `SQEX::Sd` | MSVC RTTI type descriptors in the shipping binary, 212 `SQEX` classes | 4 |
| Six-class sound family with 44-slot vtables | **the six vtables read directly from `.rdata`** at `01CB5A30` / `01CB87A8` / `01CB8940` / `01CB8AD8` / `01CB8C70` / `01CB8E08`, 44 slots each (§9) | **1** |
| Slot 43 is the point of specialisation | four variants each carry a distinct function pointer there; `VariationSound` alone retains the base | 4 |
| They are a base + subclasses, not siblings | **42 of 44 function pointers shared** with `Sound` for three variants, 39 of 44 for two more; only slot 0 and 36–43 differ — **all six figures reproduced slot-by-slot from the binary** (§9) | **1** |
| Family/class inventory and method counts | `Tools/work/rtti/classes.tsv`, `methods.tsv` | 4 |
| 949 Audio-owned functions are RTTI virtual methods across 244 classes | join of the RTTI mapping against the GFZ owner table | 4 |
| RTTI mapping is trustworthy | challenged 2026-09-02: 99.1 % agreement with independently derived GFZ classifications; 2,612 linker-folded addresses excluded | 4 |
| A source voice renders only in state 3, resamples by rate ratio × pitch, starts sample-accurately, fires one marker and ramps gain per tick (§2a) | body of `007E0B60` (`007E0C0D`–`007E0C32`, `007E0DE3`–`007E0E6F`, `007E0C81`–`007E0CC5`, `007E0E71`–`007E0EBE`) | 1 |
| The buffer queue is two slots, and exhausting a buffer calls the owner's slot 1 (§2b) | `007E0F21`–`007E0F99`, `007E1282`–`007E12E0` | 1 |
| Three voice classes form a source → submix → master graph walked outside-in each tick (§2c) | the three vtables and their slot-2 getters; the per-tick pass `007B0000`'s six walks (identification page) | 1 |
| The voice state is a five-value machine (§2d) | `007E0650`, `007E0980`, `007E2710`, `007E2760`, `007E07F0` | 1 |
| One factory builds every source voice and links it under the tick's lock (§2e) | `007AEA20`; its constructor / open calls `007AEA6C`, `007AEAD7`, `007AEB43`, `007AEBAE` | 1 |

**Scope honesty:** ~~every claim above is *structural*. None asserts what any function does.~~ *(Corrected 2026-09-30, SWE2-DATA: the first six rows are structural; the last five assert what the mix-path bodies do, at tier 1.)*
The class names are strong hints and are recorded as hints, not conclusions — the naming
discipline in `_index/EVIDENCE-STANDARD.md` forbids promoting a name to a mechanism claim
without an internal bridge.

~~**Why this document exists at PARTIAL:**~~ *(History - the status is DOCUMENTED since 2026-09-30; struck 2026-10-01, OPUS.)* **Why this document was first written at PARTIAL:** Audio is 2,064 functions — the second-largest owner
category — and had no documentation at all. Recording the proven architecture now gives later
mechanism work a frame to hang on, provided the scope limit is respected.

## 9. Related

- [`README.md`](README.md) — category overview
- [`../22-Middleware-PhyreEngine/README.md`](../22-Middleware-PhyreEngine/README.md) — the other RTTI-rich subsystem
- [`../_index/EVIDENCE-STANDARD.md`](../_index/EVIDENCE-STANDARD.md) — why names are not conclusions

## 9. Falsification pass 2026-09-02 — the vtable claims re-derived at tier 1

**Attack chosen.** The structural heart of this document — six classes, 44-slot vtables, *"42 of 44
shared for three variants, 39 of 44 for two more, only slot 0 and 36–43 differ"* — is recorded at
**tier 4** (recovered vtables). Every one of those numbers is checkable by reading the vtables out of
`.rdata`, so a claim that precise should not rest on tier 4.

### Locating the vtables without a symbol table

Each variant's `Select` is **vtable slot 43**, so scanning `.rdata` for a qword equal to a known
`Select` address and subtracting `43 * 8 = 0x158` gives the vtable base. That found five bases
immediately, plus a **second** table carrying the base `Sound::Select` — which is exactly what §2
predicts, since `VariationSound` keeps the base slot 43. The base was then identified as the table
sharing most slots with the other five (204 vs 189).

| Class | vtable | Shared with `Sound` | Differing slots |
|---|---|---:|---|
| `Sound` (base) | `0x01CB5A30` | — | — |
| `RandomSound` | `0x01CB87A8` | **42 / 44** | `0, 43` |
| `OrderSound` | `0x01CB8AD8` | **42 / 44** | `0, 43` |
| `SwitchSound` | `0x01CB8E08` | **42 / 44** | `0, 43` |
| `CycleSound` | `0x01CB8C70` | **39 / 44** | `0, 39, 40, 42, 43` |
| `VariationSound` | `0x01CB8940` | **39 / 44** | `0, 36, 37, 38, 40` |

**Every figure in §2 is reproduced.** Three variants at 42/44, two at 39/44, and **every differing
slot is either 0 or inside 36–43**. The five family vtables are contiguous, spaced `0x198` apart.

### The two 39/44 classes differ for opposite reasons

The counts match, but the *shape* is worth stating because the document treats the pair as one
category:

- **`VariationSound`** differs at `36, 37, 38, 40` and **keeps base slot 43** — precisely the
  behaviour §2 flags as structurally odd, now confirmed rather than inferred.
- **`CycleSound`** differs at `39, 40, 42, 43` — it overrides slot 43 **and three more**. So §2's
  *"slot 43 is where that logic lives for four of the five variants"* is right about Cycle including
  43, but Cycle is not a slot-43-only override the way Random, Order and Switch are.

They share a count and nothing else: one keeps the selection slot and changes its surroundings, the
other changes the selection slot *and* its surroundings. **`Sound` + `RandomSound` / `OrderSound` /
`SwitchSound` is a clean base-and-override family; the other two are not.**

### What this does not settle

**G-1** — what the four slot-43 implementations do — is untouched here; the vtable proves only which
slots differ. **G-8** — why `VariationSound` overrides 36/37/38/40 — is now precisely posed rather
than answered: those four slots are confirmed, and the question is what they are.

*(These vtable addresses sit above `0x00FFFFFF` and would have been invisible to the address checker
before it was widened earlier the same day.)*

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL.*

**Input — SERVICE, not read.** `002DDA30` calls three small Input-filed helpers (41–46 B), and `002DDE60` calls two
(46 B). What they read is not traced here.
