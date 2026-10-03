---
system: Sound trigger (FUN_007bd240)
category: 18-Audio
status: AUDITED — the trigger, its slots, the seven parameter operations and the state-2 consumer (answered 2026-09-17), the policy/list pairing (UQ-260) and the key byte (UQ-259) read; whether +0x4C slotCount is bounded (G-17: no check, one slot per pass, compaction is the guard) answered 2026-09-18; every section-7 box is ticked; the key byte (UQ-259, the entry's group id) answered 2026-09-17
owner_layer: PrimaryOwner:Audio / CodeDomain:Audio.SQEXSd
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-02
audit:
  passes: 1
  last_pass: 2026-09-02
  last_pass_state: falsification-pass
  crossref_clean: true
  reopened_count: 0
---

# Sound trigger

> The single point where a chosen sound is **armed** for playback. Every selection variant
> funnels through here — but nothing is audible yet when it returns.

## 1. What the player sees

Everything before this decides *which* sound. This hands it over to be played — but does not
play it. The request is queued and something else turns it into audio a moment later.

Three consequences a player can notice. A sound can arm **several sequences at once**, which
is how layered effects work — one "sound event" is not one stream. A sound in the wrong state
is **silently refused**: nothing plays, nothing complains, so an effect that intermittently
fails to fire has almost certainly been refused here. And because the hand-off is deferred, a
sound can be requested and still never be heard if it is torn down before the consumer runs.

## 2. Native mechanism

`FUN_007bd240(this, entry)` — the common trigger called by all five selection variants.

### The state gate

```c
if ((this->state != 0) && (1 < (unsigned)(this->state - 6)))   // state at +0x54
```

Unsigned arithmetic makes this less obvious than it looks. `state - 6` is `> 1` for every
value **except** 6 and 7 (which give 0 and 1), and `state == 0` is excluded separately:

```
proceed  iff  state != 0  &&  state != 6  &&  state != 7
```

States 6 and 7 are refusal states. On refusal the function writes the header vtable to the
out-parameter and **returns −1** — no sound, no error path.

### Sequence slot allocation

```c
int slot = this->slotCount;      // +0x4C
this->slotCount = slot + 1;      // post-increment, NO bounds check here
void* p = this + slot * 8 + 0x400;
```

The object holds an array of 8-byte slots beginning at `+0x400`, with the count at `+0x4C`.
**This function performs no bounds check** — nothing in the body caps `slotCount`.

The array's structural capacity is **32 slots**: slot 32 would write at `+0x500`, a field this
same function reads a few lines later. Since the selection loops call the trigger **once per
qualifying candidate**, a sound authored with more than 32 qualifying candidates would run off
the end. Whether a caller bounds it is unproven — see **G-17**.

### Bind and dispatch

```c
localSeq  = this->+0x18;
localVt   = SQEX::Sd::SabFile::Sequence::vftable;
int rc = FUN_007b4ef0(p + 0x400, &localSeq, &localVt);      // bind a SabFile::Sequence

if (rc >= 0) {
    handle = FUN_007b5070(&seq);

    FUN_007bfe30(this);            // fixed parameter application, order preserved
    FUN_007bfdb0(this);
    FUN_007bfd00(this);
    for (int i = 0; i < 2; i++)
        FUN_007bfeb0(this, i);     // twice, index 0 then 1
    FUN_007bfba0(this);
    FUN_007bfc30(this);

    param = ((unsigned)(this->state - 1) < 2) ? this->+0x500 : 0;
    FUN_007e7300(handle, param, this->+0x51c);             // ARM the sequence (see below)
}
*entry = SQEX::Sd::AudioBinaryFile::BaseClass<SQEX::Sd::SABSEQUENCEHEADER>::vftable;
return rc;
```

Seven parameter operations run in a fixed order before dispatch — six distinct functions, one
(`FUN_007bfeb0`) called twice with indices 0 and 1.

**All six are applicators over the slot array.** Each reads `slotCount` at `+0x4C`, walks the
slots at `+0x400`, and pushes **one distinct stored parameter** onto every live sequence:

| Function | Parameter source |
|---|---|
| `007BFE30` | `+0xD0` |
| `007BFDB0` | `+0xD8` |
| `007BFD00` | `+0xE0` |
| `007BFEB0(i)` | ~~`+0x254 + i*0x30`~~ the ramp record at `+0x248 + i*0x30` (G-14), i = 0, 1 *(corrected 2026-10-01, OPUS)* |
| `007BFBA0` | `+0x3F8`, `+0x400` |
| `007BFC30` | `+0x2B0`, `+0x2B4`, `+0x2B8`, `+0x2C4` |

> *Corrected 2026-09-17 (FABLE, `G-14`): `+0xD0`, `+0xD8` and `+0xE0` in the first three rows are not fields of the
> sound — they are the VTABLE slot offsets (slots 26, 27, 28) of the getters those operations call: `007BDBB0`,
> `007BD900` and `007BD6F0`, which evaluate the ramp blocks at `+0x88`.., `+0x188` and `+0x1B8`/`+0x1E8`/`+0x218`.*

So the pattern is **store then apply**: the public `Sound::Set*` methods (now named — see
[function identification](../sead-function-identification.md)) validate and store a value on
the Sound object; these six push whatever is stored onto every sequence the trigger has
allocated. That is why they must run *after* the slot allocation and *before* the arm.

~~Which applicator carries which named parameter is **not yet proven** — the setters' storage
offsets have not been matched to these read offsets. **G-14** stays open on that link.~~ *Corrected 2026-09-26
(FABLE): `G-14` was answered on 2026-09-17, and the answer makes this link. The named setters' ramp blocks identify
the applicators: `007BFDB0` pushes the pitch (`SetPitch`'s `+0x188` block), `007BFD00` the panning triple
(`SetPanning`'s `+0x1B8`/`+0x1E8`/`+0x218`), `007BFC30` the lowpass value (`SetLowpassValue`'s `+0x2A8`), and
`007BFE30` a layered volume (four blocks from `+0x88`; its setter is not among the named three). The full mapping,
with the dirty bytes, is in the register row.*

The final dispatch takes a state-dependent argument:

```
param = (state == 1 || state == 2) ? this[0x500] : 0
```

So states 1 and 2 pass a stored value that every other state replaces with zero. Combined
with the refusal states 6 and 7, **`+0x54` is a lifecycle state machine with at least four
behavioural classes**: refuse (0, 6, 7), pass-stored-value (1, 2), and pass-zero (everything
else).

### The dispatch is an arm-and-defer, not a play

`FUN_007e7300` is small and complete:

```c
int FUN_007e7300(Sequence* seq, u32 a, u32 b)
{
    if (seq->state /* +0x9C */ != 1)
        return -1;                  // refuse unless in state 1
    seq->+0xAC   = a;
    seq->+0xC0   = b;
    seq->state   = 2;               // 1 -> 2
    seq->+0xA9   = 1;               // flag
    return 0;
}
```

**Nothing plays here.** It stores two values, advances the sequence from state 1 to state 2,
and raises a byte flag. Something else — an audio thread or a per-frame update — consumes
that state and produces sound. The whole trigger path is therefore **deferred**: it arms a
sequence and returns.

That matters for tooling. Hooking `007BD240` or `007E7300` tells you a sound was *requested*,
not that it was heard. A sequence armed into state 2 and then torn down never reaches output.

Note the second refusal: the trigger already refused on its own state gate, and this refuses
again on the *sequence's* state. Two independent state machines must both agree before a sound
proceeds.

### The parameter operations walk the slot array

`FUN_007bfeb0(this, index)` — the one called twice, with 0 and 1:

```c
if (this->slotCount > 0) {                       // +0x4C
    for (each slot in this + 0x400) {
        seq = FUN_007b5070(&slot);
        if (seq != 0) {
            float a = this[0x25C + index * 0x30];
            float b = (a == 0.0f) ? this[0x254 + index * 0x30] : ...;
            ...
        }
    }
}
```

So the parameter ops are **per-slot**: each walks every allocated sequence and applies a
block of floats selected by index. The blocks are **0x30 bytes apart**, ~~starting at `+0x254`,
so index 0 reads `+0x254`/`+0x25C` and index 1 reads `+0x284`/`+0x28C`.~~ *(Corrected 2026-10-01, OPUS, per G-14: each is a ramp record at `+0x248 + i*0x30` - `+0x250` start, `+0x254` target, `+0x258` elapsed, `+0x25C` duration, `+0x264` curve mode; `007BFEB0` reads the duration and, when it is 0, returns the target.)*

This independently confirms the slot array at `+0x400` bounded by `slotCount` at `+0x4C` —
the same fields the trigger uses — and it is the reason those seven ops must run *after* the
slot is allocated.

## 3. Key addresses

| Address | Working name | Role |
|---|---|---|
| `007BD240` | *(sound trigger)* | the common entry — state gate, slot alloc, bind, dispatch |
| `007B4EF0` | *(bind sequence)* | binds a `SabFile::Sequence`; returns < 0 on failure |
| `007B5070` | *(sequence handle)* | produces the handle passed to dispatch |
| `007E7300` | *(sequence arm)* | state 1 → 2, stores two args, raises flag |
| `007BFE30` | *(applicator)* | walks slots, pushes `+0xD0` |
| `007BFDB0` | *(applicator)* | walks slots, pushes `+0xD8` |
| `007BFD00` | *(applicator)* | walks slots, pushes `+0xE0` |
| `007BFEB0` | *(indexed parameter op)* | walks the slot array; blocks at `+0x254 + i*0x30` |
| `007BFBA0` | *(applicator)* | walks slots, pushes `+0x3F8`/`+0x400` |
| `007BFC30` | *(applicator)* | walks slots, pushes `+0x2B0`/`+0x2B4`/`+0x2B8`/`+0x2C4` |

## 4. Data structures and formulas

```
Sound object
  +0x18   ptr    sequence source, passed to the binder
  +0x4C   i32    slotCount        post-incremented per trigger, unbounded here
  +0x54   i32    lifecycle state  see the classes below
  +0x400  ...    slot array, 8-byte stride, indexed by slotCount
  +0x248  ramp record, index 0: +0x250 start, +0x254 target, +0x258 elapsed, +0x25C duration,
          +0x264 curve mode; index 1 at +0x278 (stride 0x30; G-14, corrected 2026-10-01, OPUS)
  +0x500  f32    start offset (seconds) - the arm request's second float; see G-18
  +0x51C  f32    start delay (seconds) - written by the trigger's own event-script opcode 165; see G-18

Sequence object (the bound SabFile::Sequence)
  +0x9C   i32    state      arm requires 1, sets 2
  +0xA9   u8     flag       raised by the arm
  +0xAC   f32    start offset  - fed once, as the first time step, to the opcode stepper 007E6DD0
  +0xC0   f32    start delay   - counted down by the audio tick's frame delta before the first step
```

**Slot array capacity — structural bound:**

```
slot address = this + slot*8 + 0x400
next known live field = +0x500   (read by this same function)
=> (0x500 - 0x400) / 8 = 32 slots before slot 32 writes over +0x500
```

**Sequence arm:**

```
if seq.state != 1        -> refuse, return -1
seq[0xAC] = a ; seq[0xC0] = b ; seq.state = 2 ; seq[0xA9] = 1 ; return 0
```

**Parameter block selection:**

```
ramp(i) at this + 0x248 + i*0x30      (i = 0, 1; G-14, corrected 2026-10-01)
```

**Trigger gate:**

```
proceed  iff  state != 0  &&  state != 6  &&  state != 7
```

**Slot address:**

```
slot     = slotCount++
slotAddr = this + slot * 8 + 0x400
```

**Dispatch argument:**

```
param = (state == 1 || state == 2) ? this[0x500] : 0
```

**Observed state classes at `+0x54`:**

| State | Behaviour |
|---|---|
| 0, 6, 7 | refuse — return −1, nothing plays |
| 1, 2 | proceed, dispatch with `this[0x500]` |
| all others | proceed, dispatch with `0` |

## 5. Call chain

```
selection variant (vtable slot 43)
  -> per qualifying candidate:
       FUN_007bd240(this, entry)          <- THIS
         -> state gate at +0x54
         -> slotCount++ , slot at +0x400
         -> FUN_007b4ef0   bind SabFile::Sequence
         -> FUN_007b5070   handle
         -> 7 parameter ops in fixed order
         -> FUN_007e7300   dispatch to playback   (read, §2: arms state 1 -> 2)
```

**Upstream:** all five selection variants — see
[sound-variant-selection](sound-variant-selection.md).
**Downstream:** `FUN_007e7300`, ~~unread~~ read in §2 *(corrected 2026-10-01, OPUS)*.

**Do not confuse with:** the selection methods. Those choose; this starts. A sound that picks
correctly but never plays failed *here*, most likely on the state gate.

## 6. Modding notes

- **This is the interception point.** Anything that needs to observe, log or veto sound
  playback should attach at `007BD240` — it is the single funnel for all five variants.
- **The state gate fails silently.** Return −1, no diagnostic. A sound not playing is more
  likely a state problem than a data problem.
- **Slot count is not bounded in this function.** If you add candidates to a sound, you add
  slot allocations per trigger. Whether anything caps that is unproven — check before
  authoring many candidates.
- **The seven parameter ops run in a fixed order.** Reordering or skipping them is unlikely to
  be safe; the two-call `FUN_007bfeb0(this, 0/1)` pattern in particular looks like paired
  channels.
- **XIIOnline:** sound triggering is local. Nothing here suggests it should be networked.
  Not yet investigated.

## 7. What is not known

- [x] ~~What the seven parameter operations do (`007BFE30`, `007BFDB0`, `007BFD00`,
      `007BFEB0`×2, `007BFBA0`, `007BFC30`).~~ **G-14**.
      **ANSWERED 2026-09-17 (FABLE) - all seven read, and they are one operation applied to seven parameters.** Each walks the live slots (`+0x4C` count, handles at `+0x400`), resolves each handle through `007B5070`, and pushes one value of the SOUND into every SEQUENCE through a two-instruction setter that stores it and raises a per-parameter dirty byte. The value comes from a ramp block - the `{+8 start, +0xC target, +0x10 elapsed, +0x14 duration, +0x1C curve mode}` record that the shared helper `007CA560` writes and the curve `007A9E50` evaluates - and the named `Set*` siblings say which block is which: `SetPitch` (`007BE8A0`) hands the helper `this+0x188`, `SetLowpassValue` (`007BE3F0`) `this+0x2A8`, `SetPanning` (`007BE590`) the triple `+0x1B8` / `+0x1E8` / `+0x218`. So: **`007BFE30`** pushes vtable slot 26's value (`007BDBB0`: the product of four ramp blocks at `+0x88`, `+0xC8`, `+0x108`, `+0x148` with the factor `[this+0x30]+0xC` - the shape of a layered VOLUME, its setter not among the three named) → sequence `+0x38`, dirty `+0xA1`; **`007BFDB0`** pushes slot 27 (`007BD900`: the `+0x188` block × `[this+0x68]`) - **the pitch** → `+0x40`, dirty `+0xA2`; **`007BFD00`** pushes slot 28 (`007BD6F0`: the three blocks `SetPanning` writes, as three floats) - **the panning triple** → `+0x48`/`+0x4C`/`+0x50`, dirty `+0xA3`; **`007BFBA0`** pushes the flag byte `this+0x3F8 != 0` → `+0x5C`, dirty `+0xA4`; **`007BFC30`** evaluates the `+0x2A8` block itself (`+0x2B0`..`+0x2C4`) - **the lowpass value** → `+0x54`, dirty `+0xA5`; **`007BFEB0(i)`**, i = 0, 1, evaluates the indexed block at `+0x248 + i×0x30` (`+0x250` start, `+0x254` target, `+0x258` elapsed, `+0x25C` duration, `+0x264` mode) → `+0x60 + i×4` through `007E7430`, which then resolves the sequence's owner `[+0x18]` and, when its slot-1 state is 2 (armed), continues into it. **The dirty bytes `+0xA1`..`+0xA5` sit beside the `+0xA9` arm flag `G-19` asks about: whatever consumes state 2 must also clear these, which is the next handle on G-19.** Static, bodies read.
- [x] ~~What `FUN_007e7300` does~~ — **CLOSED 2026-09-02**: it arms a sequence
      (state 1 → 2, stores two args, raises a flag). It does not play; playback is deferred to
      an unidentified consumer.
- [x] ~~**Who consumes sequence state 2 / the `+0xA9` flag** and actually produces sound.
      **G-19** — this is now the end of the traced chain.~~
      **ANSWERED 2026-09-17 (FABLE): the consumer was already on this page; the producer is the VOICE, two layers down, and the chain between them is now read.** *Consumer:* the per-sequence update `007E7540` (`G-18`) - the audio tick `007A5400` runs the sequence pass `007B52B0` and then the voice pass `007B5AD0`, in that order. *The link:* `007E7540` resolves the sequence's voice from `[seq+0x18]` through `007B58C0` (`r14`) and, for each dirty byte the parameter operations raised (`G-14`: `+0xA1`..`+0xA5`), pushes the value into the voice through the setters `007E8B30` (`voice+0x30`, dirty `+0x1ED`), `007E8B20`, `007E8AF0`, `007E8AA0` (`+0x1AC`, dirty `+0x1F1`), `007E8AB0`, `007E8AD0`, `007E8A60` (`+0x1B4+i`, dirty `+0x1F5`), `007E8A80` - the same value-plus-dirty-byte shape one level down - and clears the sequence's byte. *The voice update* `007E8BB0` (1,137 B, the only reader of `+0x1ED`..`+0x1F5`, called only from the voice pass) tests and clears each voice dirty byte and applies the value through the voice's OWN virtual methods - `[vtable+0x38]`..`[vtable+0x58]`, slots 7–11 (`007E8F0E`, `007E8F4E`, `007E8F70`, `007E8F8F`, `007E8FC8`) - and pushes the ramp at `+0x2D8` through `007F40B0`. *The producer:* the voice's class is `SQEX::Sd::Driver::Voice` (vtable `01CB92B8`), whose **slot 1 is `007ED4C0`, the function that calls `007EAA60` - the decode-and-submit step the sead page names: HCA through `HCADecoder_*`, Ogg through `sead_ov_read`, then `sourcesubmit`** into the WASAPI device (`G-26`). So sound is produced when the voice's slot 1 runs; the sequence never produces it, it only parameterises the voice. *Bound, stated:* slot 1 has no direct caller - it is reached by vtable dispatch - and the site that dispatches it (the tick's voice pass or the render callback) is not enumerated here; on the music side `007EAA60` is also reached through `007EDA60` from `MaterialTrack` slot 13 (`007E9340`) and four `007Cxxxx` bodies. None of the eleven non-main thread bodies reaches any of these by direct call (`UQ-40`'s walk), so by direct calls the whole chain runs on the tick. Static, bodies read.
- [x] ~~What the `+0x54` lifecycle states *mean*; only their behavioural classes are proven.~~
      **G-16 ANSWERED from the writers 2026-09-12 (FABLE)** — every store of a small immediate to
      `+0x54` in the audio range read (the eight sites, `007BDDA0`–`007BF18D`); the names are
      behavioural, from what each transition does:

      | state | written by | on what | reading |
      |---:|---|---|---|
      | 1 | `007BDDA0` (**bind**, slot 40) at `007BDE05`, after `007D0890` | a record has been copied in and its `+0x30` bank reference exists | **bound** — requested, not yet armed |
      | 2 | `007BDFA0` at `007BE072` | the object's vcall `+0x128` returned ~~true~~ **0** *(corrected 2026-09-26, FABLE, Claude Opus 5.5: `test al, al` / `jne` at `007BE06E` skips this store when the call answers 1, and runs the stepper `007BD120` at once from state 1 instead; the call, `007BD0A0`, answers 1 once the referenced object is ready)* | **armed** — the sequence side accepted it |
      | 3 | the stepper `007BD120` at `007BD19E` | in states 1–3: the bank `007AAA20(+0x30 → byte +6)` resolves and `007A9A10(+0x18)` returns **2** | **bank ready** — the referenced bank's status is 2 |
      | 4 | `007BD120` at `007BD1EC` | past 3: `007B2470(+0x20)`'s vcall `+8` == 2 and `007E4D50(obj, this) < 0`, **or** the mode `+0x58 == 2` | **dispatched (held)** — the first of two dispatch outcomes |
      | 5 | `007BD120` at `007BD20F` | otherwise: vcall `+0x158(this)`, then the `+0x38` listener's vcall `+8` with `+0x40` | **dispatched (live)** — the trigger fired and the listener was told |
      | 6 | `007BED30` at `007BEEF7` | with `+0x58 == 2`, after `007E74A0` on every slot's sequence handle (`007B5070`) | **stopping** — every slot's sequence released |
      | 7 | `007BD120` at `007BD13F` / `007BD16D` (states 1–3: `007B31A0(this, 0) == 4`, a missing bank, or `007A9A10` returning `< 0` or 1); `007BF0A0` (the per-update, slot 42) at `007BF18D` (state outside 2–4, no slots pending, and state 6 or vcall `+0x138` true) | **finished / failed** — terminal either way |

      So the gate `state == 0 || state ∈ {6, 7}` refuses **unbound, stopping and finished** objects;
      1–2 dispatch with `+0x500` because they are the pre-ready states; 3–5 dispatch with 0. The
      state names are FABLE's readings of the transitions, not authored labels. **G-16.**
- [x] ~~Whether `slotCount` at `+0x4C` is bounded anywhere.~~ **G-17.** Structurally the array
      holds **32 slots** before slot 32 would overwrite `+0x500`, a field this same function
      reads. Every comparison against `+0x4C` found so far is an *iteration* bound
      (`i < slotCount`, `0 < slotCount`), never a capacity check. **Absence of a bound in the
      ~40 functions read is not proof of absence** — a caller may bound it. Unresolved.
      *Widened 2026-09-12 (FABLE):* a scan of **every** function in the audio range
      (`007B0000`–`007FFFFF`) for a `+0x4C` compared against an immediate above 2 finds one site,
      `007E409E` (`cmp [rdi+0x4C], 0x10`) — in `007E3CF0`, an object that touches neither `+0x400`
      nor `+0x54`, so not this class. The trigger's `slotCount` has no capacity check anywhere in
      the audio code; only a caller outside it could bound it.
      *Narrowed 2026-09-14 (FABLE): no check, but two things limit it, and neither is a capacity.*
      - **It shrinks.** The per-update slot `007BF0A0` walks the slots. When a slot's handle no longer resolves
        (`007B5070` returns 0), it shifts the tail down one and runs `dec [this+0x4C]` (`007BF11F`–`007BF142`). So
        `slotCount` counts live sequence slots, not triggers ever made.
      - **The per-object initialiser `007E7A90` zeroes it** (`007E7B99`).
      - **One selection pass adds at most the authored candidate count.** Checked in the variant `007E67C0`: it loops
        `i < byte [record+5]` (`007E68FC`–`007E6902`) and calls the trigger for each candidate whose range brackets
        the current value.
      - **So an overwrite of `+0x500` needs more than 32 slots live at once.** That means one authored sound with more
        than 32 simultaneously qualifying candidates (the count is a `u8`, up to 255), or re-triggers faster than
        slots finish.
      - **Not read:** the other four selection variants' loop bounds, and the authored candidate counts. Both belong
        to a data census.
      ***ANSWERED 2026-09-18 (FABLE): nothing bounds it, and nothing needs to within one pass, because the authored candidate count is never above one.** *The code half, image-wide.* A sweep of every `.text` function that writes a dword at `+0x4C` and also touches the class's own fields (`+0x400`, `+0x54`, `+0x500`) finds one growth site: `007BD266`..`007BD276` in the trigger `007BD240` (`movsxd r8, [rcx+0x4C]`; `lea eax, [r8+1]`; the slot at `rcx + r8*8`), reached only past the state gate (`add eax, -6; cmp eax, 1; jbe` at `007BD25A`..`007BD260`) and never past a compare of the count. Its six callers (`007BD370` and the five policy walkers `007E5160`, `007E58D0`, `007E5E80`, `007E6360`, `007E67C0`) contain no reference to `+0x4C` at all; the other writers in the audio range are the initialiser `007E7A90` (zero), the compactor `007BF0A0` (`dec`) and two unrelated classes. *The loop bounds.* All five walkers loop the same way: the record at `this+0x30` is wrapped as the accessor context (`007E681D`..`007E682F`, vtable `01CB43E0` over the same pointer) and the walk runs `i < byte [record+5]` (`007E51F5`, `007E5961`, `007E5F38`, `007E63CB`, `007E6841` and the loop tails), so the earlier sample (`007E67C0`) speaks for all five. *The data half.* Reading every `.sab` in the archive (4,609 files, seq and snd chunks: `u16 0, u16 0x10, u32 count, u32 offsets[]`), byte `+5` is **0 or 1** in all 11,165 version-4 sequence records (428 ones among the 9,836 `win` records, none in the 1,329 `orb`) and in all 11,821 `win` version-16 sound records (9,836 ones). So one selection pass triggers at most one candidate, and the 32-slot array can be exceeded only by accumulation: thirty-three sequences bound and still resolving between two compactions of `007BF0A0`, which no code prevents. That is the whole answer: no capacity check exists, the per-pass growth is one, and the guard is the per-update compaction. Static sweep plus DATA from the archive.*
- [x] ~~Meaning of the dispatch arguments `+0x500` and `+0x51C`.~~ **G-18 ANSWERED from the writers
      and the consumer 2026-09-12 (FABLE): both are floats in seconds — a start offset and a start
      delay.** The names are behavioural (what the consumer does with them), not authored labels.

      **The consumer.** The sequence per-update `007E7540(seq, xmm1 = dt)` is called from
      `007B52B0` at `007B5313`, itself called by the audio tick `007A5400` at `007A54CA` with a
      frame delta computed as a QPC difference divided by the frequency (`007A5488`, `cvtpd2ps`) —
      **seconds**. It first tests `+0xC0`: while it is above zero it subtracts `dt` and skips the whole
      step (`007E7573`–`007E75AC`) — a **countdown before the sequence starts**. Once it reaches zero,
      on the first pass (`+0xA9` raised by the arm) it calls the opcode stepper `007E6DD0(seq,
      xmm1 = +0xAC, r8b = 1)` and clears the flag (`007E75B7`–`007E75C7`); every later pass calls the
      same stepper with `xmm1 = dt` and `r8b = 0` (`007E75D0`). So `+0xAC` stands in for the frame
      delta exactly once: the stepper scales it by the tempo pair `+0x44 × +0x40`, subtracts it from
      the wait accumulator `+0x34`, and if the accumulator is at or below zero walks the sequence's
      opcode stream (cursor `+0x30`, base from `007CF740(seq + 0x20)`) until the accumulated waits
      (opcode 3 = fixed wait, opcode 5 = random wait, both in milliseconds × 0.001, `007E6F38`–
      `007E6FC2`) catch up — a **seek**: a positive `+0xAC` advances the sequence through as much
      authored time as it names before anything is heard. In "first" mode (`r8b = 1`) the random wait
      is skipped (`007E6F85`) and the loop marker (opcode 2) records the elapsed origin as
      `−(+0x34)` (`007E6F19`–`007E6F22`) instead of zero. In state 2 the per-update also
      accumulates `+0xB8 += dt` (`007E7A5C`), the elapsed clock the loop marker seeds.

      **Where `+0x500` (→ `+0xAC`, the offset) comes from.** The arm step `007BDFA0(trigger,
      xmm1 = fade, xmm2 = offset, r9d)` — the state 1 → 2 writer of G-16 — stores its **xmm2** to
      `+0x500` at `007BE060` (the writer the G-16 census missed) after starting the ramp
      `007CA560(trigger + 0xC8, 1.0, fade, r9d, 0)` with its xmm1. It has two callers: the audio
      command-queue consumer `007AB5C0`, kind **10** (`007AB7E9`: xmm1 = record `+0x10`, xmm2 =
      record `+0x14`, r9d = record `+0x18`), and the handle-interface method `007E9AE0` (vtable slot
      `01CB9250`; no static caller), which passes fade 0, its own xmm1 as the offset and −1. Kind 10
      is enqueued by `007A78B0(handle, fade, offset, r9d)` (`007A790C`–`007A793F`, for handle kind 2;
      kind 8 becomes queue kind 0x1C and kind 7 goes straight to `007BAE50`). **Every game-side
      caller of `007A78B0` passes offset 0 and fade 0 with r9d = −1**: `00223190` (`002232AF`–
      `002232C1`, which loads an authored fade of **4.8** and then zeroes it — a dead load),
      `00224570`, `00224E40`, `00224F10` and `002252C0`. Only the audio layer's own re-issue wrappers
      pass stored values: `007EEA00` from a record's `+0xC` / `+0x10` (`007EEB50`) and `007F0820` from
      an object's `+0xB4` / `+0xB8` (`007F0F61`). The constructor `007D2150` zeroes `+0x500`
      (`007D26A1`) beside `+0x504 = 10.0`; `007BC8D0` zero-fills it; `007BFFA0` copies it between two
      triggers (`007BFFA6`). It is dispatched only in states 1–2 (§ above) because those are the
      states in which the arm request's offset has not yet been consumed.

      **Where `+0x51C` (→ `+0xC0`, the delay) comes from.** One writer in the image: the trigger's
      **own event-script interpreter `007B31A0(trigger, mode)`** at `007B408E`, in the arm for
      script **opcode 165** (two-level table at image base + `0x6943D0` / `0x694374`, `007B33C9`–
      `007B33DD`; siblings 161–166 are the compare-conditioned opcodes, 164 = `007BE4D0`, a second
      ramp on `+0x148`). The interpreter walks the script that the bound record `+0x30` names for
      the mode — byte `+0xA` for mode 0, `+0xB` for mode 1, `+0x4F` for mode 3 when the record's
      version byte is ≥ 0xE (`007B31FC`–`007B3226`) — through `007AE1D0` / `007AE1A0`. Opcode 165's
      entry carries a flag byte `+0`, a compare op `+4`, an operand byte `+5`, a float step `+8` and a
      float base `+0xC`; the arm evaluates `007B2BD0(op, G, operand)` (six integer compares,
      `007B2BEC`–`007B2C15`) against the global **`02EAD57C`**, derives a count (op 0 → 1; op 2 →
      `G − operand`; op 3 → `G + 1 − operand`; otherwise `G`) and stores **`count × step + (flag ?
      base : 0)`** to `+0x51C`. `02EAD57C` has exactly two writers image-wide, both zero (`007B4840`
      at `007B4876`, the audio reset; the CRT initialiser `008B8A10`), so in the shipped build the
      count is 0 or 1 and the delay is `step` or `base` (or their sum) from the authored script
      entry — what the compare global was meant to count is not in the image. The constructor
      zeroes `+0x51C` (`007D26C8`).

      **Not established:** which shipped `.sab` records carry an opcode-165 entry with a non-zero
      step or base (a data census, not read here), and whether the two audio-layer wrappers ever
      re-issue a non-zero offset in play. Neither changes the field meanings. **G-18.**

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Single common trigger for all five variants | called on the success path of every slot-43 body read in the previous block | 1 |
| State gate excludes 0, 6, 7 | `(state != 0) && (1 < (unsigned)(state - 6))` — unsigned wrap makes 6→0 and 7→1 the only excluded values | 1 |
| Slot allocation is unbounded in this body | complete body contains no comparison against a capacity | 1 |
| Binds a `SabFile::Sequence` | `SQEX::Sd::SabFile::Sequence::vftable` written before the bind call | 1 + 3 |
| Seven parameter ops in fixed order | complete body, straight-line sequence | 1 |
| State-conditional dispatch argument | `((unsigned)(state - 1) < 2) ? this[0x500] : 0` | 1 |
| Out-parameter receives the header vtable on both paths | `SQEX::Sd::AudioBinaryFile::BaseClass<SQEX::Sd::SABSEQUENCEHEADER>::vftable` assigned before each return | 1 + 3 |

**Scope honesty:** the parameter operations and the dispatch target are named by address only.
~~Nothing here claims what they adjust — calling them "volume" or "pitch" would be a guess, and
the naming discipline forbids it without an internal bridge.~~ *(Superseded: G-14 (2026-09-17) names them through the `Set*` siblings - pitch, panning and lowpass; `007BFE30`'s is volume-shaped, its setter unnamed. Struck 2026-10-01, OPUS.)*

## 9. Related

- [`sound-variant-selection.md`](sound-variant-selection.md) — what chooses the candidate
- [`../sqex-sd-sound-driver-architecture.md`](../sqex-sd-sound-driver-architecture.md) — the class hierarchy

## 9. Falsification pass 2026-09-02

**Attack chosen.** Three claims here are exactly countable: that the trigger is *"the common trigger
called by all five selection variants"*, that `007B4EF0` *"returns < 0 on failure"*, and the
parameter-operation count — which reads "seven" in the prose and shows six rows in the table.

### The parameter count was the suspicion, and the document was right

The table lists six functions while the text says seven operations. That looked like an internal
inconsistency of the kind this pass has found elsewhere. It is not: §2 states it plainly —
*"seven parameter operations … six distinct functions, one (`FUN_007bfeb0`) called twice with
indices 0 and 1."* Seven operations from six functions. **No defect; the writing already accounts
for it**, and it is recorded here so the same false suspicion is not raised again.

### SURVIVED: the bind-failure convention

`007B4EF0` returns `0xFFFFFFFF` when its lookup yields null — **`-1` as an unsigned, so `< 0`
signed**, exactly as documented.

### REFINED: six callers at fourteen call sites, not five variants

A caller census plus a per-caller count of direct `E8` calls to `007BD240`:

| Caller | Call sites | |
|---|---:|---|
| `007BD370` `Sound::Select` (base) | 1 | documented variant |
| `007E5160` `RandomSound::Select` | **4** | documented variant |
| `007E58D0` `OrderSound::Select` | **4** | documented variant |
| `007E6360` `CycleSound::Select` | 2 | documented variant |
| `007E67C0` `SwitchSound::Select` | 1 | documented variant |
| **`007E5E80`** | **2** | **not listed — the Cycle helper** |
| **total** | **14** | across **6** functions |

All five documented variants are present, so the claim holds. Two refinements:

1. **There is a sixth caller.** `007E5E80` is the helper `CycleSound::Select` delegates to — the one
   carrying the `rand()` draw (see
   [`sound-variant-selection.md`](sound-variant-selection.md) §10). The Cycle path therefore triggers
   from **both** `007E6360` and its helper.
2. **The trigger is not called once per variant.** Fourteen sites across six functions, and the
   distribution is informative: the base and `SwitchSound` trigger from **one** site each — a single
   range match, one sound — while `RandomSound` and `OrderSound` trigger from **four** each. That
   matches the two-pass shape those variants have: a first qualifying entry, then a continuation
   loop over further entries sharing its key. §2's statement that the loops call the trigger *"once
   per entry"* is confirmed by the site count rather than merely asserted.

## 10. `007E67C0` and `007E6360` — the third and fourth policies over the same descriptor

Both were on the *leaned on and never opened* cut, cited by the same three documents. **Taken as a
pair, because two entries from one document are one under-described document counted twice, not two
independent gaps.**

**Extents checked**: `007E67C0` is 97 instructions ending `ret` at `007E695F`; `007E6360` is 138
ending `ret` at `007E65A5`. **Neither has a `jmp` leaving its extent.**

Both walk the same structure as the two policies already read — the list at `object + 0x30`, whose
**count is a byte at `+5`**, through the same five-function accessor family (`007CF9A0`, `9C0`, `9E0`,
`A30`, `AC0`). **What differs between all four is only the rule for which entries are emitted.**

### `007E67C0` — select by a float range

```asm
007E6833  call  0x7bd9d0            ; -> xmm0, the query value
007E683E  movaps xmm6, xmm0
...per entry...
007E68BE  call  0x7cfbf0            ; -> the entry's LOW bound
007E68C3  comiss xmm0, xmm6
007E68C6  ja     skip               ; low > value  -> skip
007E68CC  call  0x7cfbc0            ; -> the entry's HIGH bound
007E68D1  comiss xmm6, xmm0
007E68D4  jae    skip               ; value >= high -> skip
007E68E9  call  0x7bd240            ; emit
```

**An entry is emitted when `low <= value < high`** — an **inclusive low and exclusive high**, so
adjacent ranges tile without overlap and a value exactly on a boundary belongs to the upper range.
**The query value is fetched once before the loop**, so every entry is tested against the same number.

**Two accessors return the bounds** (`007CFBF0` low, `007CFBC0` high), which are not used by any of
the other three policies.

### `007E6360` — group consecutive entries by a key

Two nested loops over the same list. The outer resolves an entry and, **when the resolve fails**,
reports it through the `[sead][!!error!!]` descriptor and sets a flag. The inner then advances while a
per-entry byte matches:

```asm
007E64D8  call  0x7cf9a0            ; the key of entry i
007E64E1  movzx edi, al
007E64E4  call  0x7cf9a0            ; the key of the run's first entry
007E64E9  cmp   al, dil
007E64EC  jne   0x7e651f            ; different key -> end of run
007E64EE  test  sil, sil            ; the run's leader failed?
007E64F6  call  0x7bd240            ; ...then report this member too
007E6523  dec   ebx                 ; step back one so the outer loop resumes at the boundary
```

> **Consecutive entries sharing a key form a run, and a failure on the run's first entry is reported
> for every member of it.** The `dec ebx` before breaking is what makes the outer loop resume *at* the
> boundary rather than past it — **without it the first entry of each run after the first would be
> skipped.**

**What the key byte is, is not established** — only that `007CF9A0` returns one byte per entry and that
equality of that byte defines the run.

### Four policies, one format

| function | rule |
|---|---|
| `007BD370` | emit every entry |
| `007E58D0` | emit the unconditional entries, plus **one** from a rotating pool |
| **`007E67C0`** | **emit entries whose `[low, high)` range brackets a queried float** |
| **`007E6360`** | **group consecutive entries by a key byte; report per group** |

> **The descriptor format is one thing and the selection policy is four.** Nothing in the list itself
> says which rule applies — **the policy is the function you call, not a field you read** — so a tool
> that dumps these lists cannot tell how any of them will behave without knowing the caller.

### What is not established

- [x] ~~**UQ-258.** What `007BD9D0` returns as the query value for the range policy, and in what unit.~~ **Answered 2026-09-14 (FABLE):** the range policy `007E67C0` is `SwitchSound`, and its query getter was read whole as **G-11** on [sound-variant-selection.md](sound-variant-selection.md) §7.
      - **What it returns.** It is a named runtime parameter:
        - `"default"`, or no name → the object's float `+0x514`, the value the parameter setters write;
        - `"distance"` → `+0x508`, the listener distance written by the spatial update;
        - any other name → the by-name lookup.
      - **In shipped data.** Every shipped sequence record is version 4, below the version-10 name block, so the shipped banks always switch on `+0x514`. **The getter fixes no unit**: the value is whatever the trigger's parameter push writes.
      - **The by-name path, read 2026-09-14.** `007B0E90` scans a global table of 64-byte entries (base `[02EAD3F8] + 8`, count `[02EAD3EC]`) for a string-equal name. On a hit it returns `[+0x18] + ([+0x1C] − [+0x18]) · curve([+0x20] / [+0x24])`. The curve is picked by `[+0x2C]` through `007A9E50`, a six-entry jump table of polynomial and `powf` easings; an id above 5 makes the curve 0. If `[+0x24]` is 0, it returns `[+0x1C]`. With no match it returns −1, and the getter answers 0.0. In other words, it is a normalised parameter mapped onto a `[lo, hi]` range. What the table's entries are named in shipped data is not read here.
- [x] ~~**UQ-259.** What the key byte from `007CF9A0` is. **Narrowed 2026-09-14 (FABLE):** where it lives is now exact, and what it means is not.~~
      - **Where.** `007CF9A0` (27 B) reads the record at `[ctx + 8]` and returns byte `+5` when the version byte `+0` is at most 2, and byte **`+0x11`** otherwise (`007CF9A7`–`007CF9B6`).
      - **The storage is shared.** Those are the second bytes of the same four-byte fields the bound accessors read as floats (UQ-261): `+4` at version 2 and `+0x10` from version 3. So a record's key byte and its low bound cannot both be meaningful, and the group policy and the range policy read one field two ways.
      - **Not established.** What the byte encodes, and whether shipped lists ever carry keys (UQ-260 asks the list-level half).
      ***ANSWERED 2026-09-17 (FABLE): the key byte is the entry's group id, and the selection policies read it to gather the entries that share a group.** Every caller of `007CF9A0` is one of the five policy walkers `007E5160`, `007E58D0`, `007E5DA0`, `007E5E80` and `007E6360`, and each uses the byte the same way: for entry `i` of the list (the loop bound is the count byte `+5`), it builds the entry context through `007CF9E0(ctx, base, word +4)`, reads the entry's key (`007CF9A0`) and a reference entry's key, and on equality admits the entry to the play set through `007BD240` (`007E52B8`..`007E52EC`, `007E5A38`..`007E5A6D`, `007E64D8`..`007E6506`) or counts it toward the loop (`007E5408`..`007E5435`); `007E5DA0` collects the distinct keys of a list into a byte array, appending a key only when no earlier byte equals it (`007E5E1A`..`007E5E42`), and `007E5E80` matches an entry's key against a stack list of keys already taken (`007E606B`..`007E6083`, `007E6104`..`007E610D`). That is exactly the grouping [the sound-variant page](sound-variant-selection.md)'s Random, Order and Cycle selections run over, whose Sequence record byte `+0x11` that page names the group: `007CF9A0` is the version-aware read of that byte (`+5` up to version 2, `+0x11` from version 3), so a key is the group an entry belongs to, distinct keys are the groups a list offers, and the low-bound float that shares its storage is the other reading of the same field (UQ-261). Static, all five callers read at the call.*
      ***CENSUS 2026-09-18 (SWE2-DATA, [cyclekey-census.tsv](members/cyclekey-census.tsv) via [gen_cyclekey_census.py](members/gen_cyclekey_census.py)): the shipped key byte is always zero, and no CycleSound- or SwitchSound-owned list exists at all.** All 11,165 `SabFile::Sequence` records across all 4,609 `.sab` banks are version 4, carry key byte `+0x11 = 0`, the whole `+0x10` field `0` (so the shared storage reads weight/rangeMin `0.0`), and `+0x14 = 0`; **0** sound records carry class 4 or 5, so the Cycle and Switch policies have no shipped list to walk (the earlier class census's `{0: 1985, 1: 11165}` cross-checks: `11,165` Sequence records = `11,165` class-1 sounds at one candidate each, and seq record `+4` is a **u16 seq-record id dense in the family/bank seq namespace** — *corrected 2026-09-20 (SWE2-DATA, `AUDITSEM-CONTRA-DATA-SEQREC-KEYID-SEMANTICS`)*: it is not the owning sound's in-bank u8 index as this note first read. Multi-record banks run it dense 0..31 (`se200`/`se208`), the one-record banks run it dense across the family (`se001001`=1 … `se010` 0..263 with the file-numbering gaps mirrored, `se010079`=263 — byte `+5` non-zero on 428 records), and 4,078 of 4,097 single-sound banks carry `+4 != 0`; **7,086** of 11,165 equal the chunk position at u16 width only where bank order already agrees — *figure corrected 2026-09-20 (`AUDITSEM-CONTRA-DATA-SEQREC-EQCOUNT-7095`): the first repair quoted 7,095 measured at the old u8 comparison; at u16 the nine `.win.sab` records carrying `+4 = 0x0100` drop out*). Runs are degenerate: every list is length 1 and every bank's key column is a single all-zero run (512 banks have more than one seq record; the longest run is 123, the whole `se000` table). The grouping machinery the five walkers implement is therefore never exercised by authored data — authored banks offer each sound exactly one candidate in group 0. `.mab` ships no `seq ` chunk at all (0 of 116), so the answer covers both bank kinds. Authored-data census, reproducible.*
- [x] ~~**UQ-260.** Whether the four policies are ever applied to the same list, or each list has one policy.~~
      **ANSWERED 2026-09-17 (FABLE): each list has one policy, because the policy is a virtual method of the object that owns the list.** The four have no direct caller in `edges.tsv`; the RTTI places every one at **vtable slot 43** of a `SQEX::Sd::Driver` sound class - `007BD370` in `Sound` (`01CB5A30`) and, unoverridden, `VariationSound` (`01CB8940`); `007E58D0` in `OrderSound` (`01CB8AD8`); `007E6360` in `CycleSound` (`01CB8C70`); `007E67C0` in `SwitchSound` (`01CB8E08`). A list is reached through its owner's slot 43, the owner's class is fixed at construction, and no policy takes a foreign list - each reads the record at `[this+8]`. So *the policy is the function you call* sharpens to *the policy is the class of the sound that carries the list*; which record kinds construct which class is the sound-variant-selection page's business. Static (RTTI + bodies).
- [x] ~~**UQ-261.** What the two bound accessors read from an entry — only that they return floats and are used
      nowhere else in the family.~~ **Answered 2026-09-14 (FABLE):** both read the record at `[ctx + 8]` and dispatch on its version byte `+0`:

      | version | low `007CFBF0` | high `007CFBC0` |
      |---|---|---|
      | 0, 1 | 0.0 | 0.0 |
      | 2 | float `+4` | float `+8` |
      | 3 and above | float `+0x10` | float `+0x14` |

      (`007CFBF7`–`007CFC0B`, `007CFBC7`–`007CFBDB`.) This agrees with the G-2 narrowing on [sound-variant-selection.md](sound-variant-selection.md) §7. A version-0/1 record therefore has the range `[0, 0)`, which admits no value, so `SwitchSound` emits nothing from such an entry.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL.*

**Platform — SERVICE.** `00223190` and `00224570` ask the 78-byte QPC seconds timer (`QueryPerformanceCounter` divided by
the stored frequency). At least one of the trigger's timing inputs is therefore the QPC clock. How it combines with
frame-based timing is not read here.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Platform — SERVICE.** `00224570` on this page calls `FUN_005cc930`, owned by that layer. What it reaches is a high-resolution counter read: it calls the import at `008C2188` and converts the unsigned 64-bit result to double with the `2^64` fixup at `00D27A68`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-sound-trigger-ee-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `007B4EF0` | 203 B | Zeroes the qword at `rcx`, takes an object from the pool at `02EAD5B0` through `007DF750` and returns -1 when it is null; otherwise it obtains a 16-bit id from `007B5580` on `02EAD600` with that object, increments the counter dword at `02EAD5A4` and writes the handle at `rcx` (byte 3, the id as word `+2`, the counter as dword `+4`), constructs the object with `007E6960` and calls `007E71F0` on its result with stack copies of the handle and of the qword at `[rdx]` and a stack record holding `01CB4D58` and the qword at `r8+8`, returning that call's result; both paths store `01CB4D48` to `[r8]` before returning. | `007B4F14`, `007B4F21`, `007B4F4D`, `007B4F9E`, `007B4FAF` |
| `007B5AD0` | 369 B | Walks the node list headed at `02EAD6B0`, returning 0 at once when it is empty: for each node it calls `007E8BB0` on the node's object (`+0x20`) with `xmm1` = the incoming `xmm0`, and when the object's dword `+0x1E8` is not 5 it stops (returns 0) if bit `0x1` of the node's dword `+0x1C` is clear, else moves to the node's `+0x10` successor; when it is 5 it calls the object's vtable slot `+8` (decrementing the dword at `02EAD63C` when that returns 1), and if the node's signed dword `+0x18` indexes an entry below the count `02EAD698` of the 0x28-byte table whose pointer is the qword at `02EAD6A0` whose bit `0x1` of `+0x1C` is set, unlinks that entry from the list (head `02EAD6B0`, tail `02EAD6B8`), clears the bit, pushes it on the list at `02EAD6A8`, decrements `02EAD69C` and moves to the saved successor (otherwise it stays on the same node); it then calls the object's vtable slot `+0` with `edx`=0 and returns the object to `02EAD640` through `007DF8D0`; the walk returns 0 when the next node is null, with the stack cookie checked through `00808C40`. | `007B5B1A`, `007B5B1F`, `007B5B67`, `007B5BB8`, `007B5BFF` |
| `007BC8D0` | 1314 B | Fills the object at `rcx` without calls and returns it in `rax`: pointers `01CB5A30`, `01CB5B98` and `01CB5BA8` at `+0`, `+8`, `+0x10` and `01CB43E0` at `+0x28`, the other qwords `+0x18` to `+0x58` and word `+0x60` zeroed; four 0x40-byte slots from `+0x88` headed by `01CB5A20` with `01CB4890` at slot `+0x30`, qword `+0x38` zero and five fields cleared (qwords `+8`/`+0x10`, dwords `+0x1C`/`+0x24`, byte `+0x20`); thirteen 0x30-byte slots headed by `01CB44A0` (at `+0x188`, three from `+0x1B8`, two from `+0x248`, `+0x2A8`, `+0x2D8`, four from `+0x308` and `+0x3C8`) with the same five fields cleared; the four 0x40-byte entries from `+0x400` zeroed twice and the qwords `+0x500` to `+0x530` zeroed except dword `+0x520` = -1; then dword `+8` = 0, float `+0xC` = 1.0, dwords `+0x10`/`+0x14` = 0 and `+0x1C`/`+0x20`/`+0x24` cleared again in the slots at `+0x88`, `+0x108`, `+0x148`, `+0x188`, `+0x1E8`, `+0x2A8`, `+0x2D8`, `+0x308`, `+0x338`, `+0x368` and `+0x398`, and the five fields cleared again at `+0xC8`, `+0x1B8`, `+0x218`, `+0x248` and `+0x278`; the floats `+0x64` to `+0x7C` set to 1.0, bytes `+0x80` to `+0x83` set to 0xFE and byte `+0x3F8` cleared. | `007BC963`, `007BC976`, `007BCB15`, `007BCB8E`, `007BCD12` |
| `007BD6F0` | 466 B | Zeroes the floats at `[rdx]`, `[r8]` and `[r9]`, then for the parameter blocks at `rcx+0x1C0`, `+0x1F0` and `+0x220` adds to them respectively the block's float `+4` when its float `+0xC` compares equal to 0 or unordered, else the block's float `+0` plus (`+4` minus `+0`) times the result of `007A9E50` called with float `+8` divided by `+0xC` and dword `+0x14`; it then wraps `[rdx]` by adding 2 while it is below -1 (`01CEBC9C`, unordered also looping) and adding -2 (`008F3148`) while it is above 1 (`01CEBBA8`), clamps `[r8]` and `[r9]` to -1 when not at least -1 (unordered included) and otherwise to at most 1 (`minss`), and returns 0 in `eax`. | `007BD730`, `007BD759`, `007BD850`, `007BD870`, `007BD891` |
| `007BDBB0` | 342 B | Starts from 0 when the object's vtable slot `+0x130` returns non-zero `al`, else from the float at `+0xC` of the object at `rcx+0x30`, multiplies it by one factor from each of the four 0x40-byte slots at `rcx+0x88` and finally by the float at `rcx+0x64`, returning the product in `xmm0`; a slot's factor is its float `+0xC` when its float `+0x14` compares equal to 0 or unordered, otherwise, with ratio = `+0x10` / `+0x14`: when its qword `+0x38` is null, `+8` + (`+0xC` - `+8`) times `007A9E50` of the ratio and dword `+0x1C`; when it is set, `007AE260` on the slot's `+0x30` record with 1 minus the ratio gives `+0xC` + (`+8` - `+0xC`) times the result if float `+8` is above `+0xC`, or with the ratio gives `+8` + (`+0xC` - `+8`) times the result otherwise (unordered included). | `007BDBD6`, `007BDC34`, `007BDC50`, `007BDCAB`, `007BDCD8` |
| `007BE3F0` | 215 B | When the float `xmm1` is below 0 or unordered (`comiss`/`jb`) or above 1.0 (`01CEBBA8`), it formats `01CB5CD8` with it as a double through `0019C5D0` into a 256-byte stack buffer with a newline (calling `00809728` if the terminator index reaches 0x100), passes the buffer to the import at `008C2120` and to `007A5570` with 1 and returns -1; otherwise it calls `007CA560` on `rcx+0x2A8` with the incoming `rdx`, `r8` and `xmm1`, `r9`=0 and a zero byte argument and returns its result, both returns checking the stack cookie through `00808C40`. | `007BE40C`, `007BE418`, `007BE429`, `007BE463`, `007BE4A7` |
| `007BE590` | 770 B | Returns 0 at once when the object's vtable slot `+0x130` returns zero `al` and byte `+0x19` of the object at `rcx+0x30` has bit `0x1` or `0x8` set; otherwise it handles three values, each accepted only within -1 (`01CEBC9C`) to 1 (`01CEBBA8`), below or unordered and above both rejected: for `xmm1` it reads the current value with `007A9E00` on `rcx+0x1B8`, wraps that value into -1..1 by steps of 2, wraps the target minus the wrapped value the same way, and calls `007CA560` on `rcx+0x1B8` with the unwrapped current value plus that difference; `xmm2` and `xmm3` go directly to `007CA560` on `rcx+0x1E8` and `rcx+0x218`; each call also gets the fifth (float) argument in `xmm2`, `r9`=0 and a zero byte, and each rejected value is formatted as a double with `01CB5C30`, `01CB5C68` or `01CB5CA0` through `0019C5D0` and logged through the import at `008C2120` and `007A5570` with 1; it then returns 0, checking the stack cookie through `00808C40`. | `007BE5DA`, `007BE62B`, `007BE6AA`, `007BE746`, `007BE7DB` |
| `007ED4C0` | 186 B | Enters the lock at `rcx+0x10` through the import at `008C20B8` and, unless the dword at `rcx+0x68` is 4, looks up a stack copy of the qword at `rcx+0x40` with `007B2470` and calls the result's vtable slot `+8`; when that returns 2 and byte `+5` of the object at `rcx+0x58` is 1 or 2 (byte minus 1 not above 1, unsigned), it calls `007E2EB0` with the looked-up object and `rcx-8` and then `007E4860` on that result with `edx`; it then calls `007EAA60` with `rcx-8` and, when byte `+0x124` is 1, calls vtable slot `+0x10` of the object at `+0x60` and sets `+0x68` to 4 when that result is not greater than zero (signed `jg`); every path ends by tail-jumping to the import at `008C20C0` with `rcx+0x10`. | `007ED4D2`, `007ED4DC`, `007ED510`, `007ED532`, `007ED561` |
| `007F40B0` | 233 B | Returns at once when byte `rcx+0x68` is zero; otherwise, when byte `+0x28` is set it adds `xmm1` to float `+0x18` and, once the sum is at least float `+0x1C`, stores `+0x1C` there and clears the byte (a sum below it or unordered sets the byte to 1), does the same for float `+0x48` against `+0x4C` under byte `+0x58`, then takes a rate equal to float `+0x44` when `+0x4C` compares equal to 0 or unordered, else `+0x40` + (`+0x44` - `+0x40`) times `007A9E50` of `+0x48` / `+0x4C` and dword `+0x54`, adds 1.0 (`01CEBBA8`) divided by that rate times `xmm1` to float `+0`, and when the result is at least 1.0 subtracts its truncated integer part, returning with no result value. | `007F40DE`, `007F40E8`, `007F410D`, `007F4143`, `007F4186` |
