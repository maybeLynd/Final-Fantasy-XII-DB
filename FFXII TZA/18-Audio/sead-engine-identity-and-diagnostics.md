---
system: SEAD engine identity and diagnostic strings
category: 18-Audio
status: AUDITED
owner_layer: PrimaryOwner:Audio / CodeDomain:Audio.SQEXSd
evidence_tier: 2
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 16 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-02
audit:
  passes: 1
  last_pass: 2026-09-02
  last_pass_state: counts-exact-severity-row-relabelled
  crossref_clean: false        # 2026-09-30 (SWE2-DATA): false until the pass-22 UNACCOUNTED NEIGHBOUR findings are accounted (FRONTIER-REQ-SWE2-DATA-PASS22-DEBT; OPUS-REQ-DATA-PASS30-CROSSREF-CLEAN-0930)
  reopened_count: 0
---

# SEAD engine identity and diagnostic strings

> The sound engine names itself, its classes, its codecs and its failure modes — in **159
> authored diagnostic strings** left in the shipping executable.

## 1. What the player sees

Nothing directly. These strings never reach the screen.

They matter because they are the engine **describing itself in its developers' own words**.
Where the rest of this database has to infer what a function does, here the code states it:
which audio device layer it talks to, which compressed formats it decodes, what it calls its
own objects, and precisely which failures it was built to expect. Anything a player hears
passes through the machinery these strings name.

## 2. Native mechanism

The driver is called **SEAD**. Every diagnostic is prefixed `[sead]`, then a severity, then a
message that usually names the class and method that raised it:

```
[sead][!!error!!]CoreSourceVoice::Render unknown type rendermix!!! %d
[sead][!!error!!]AudioStream::MarkAsUnused invalid readState_ = %d
[sead][info]%s version %X.%X.%X.%X
```

`SQEX::Sd` (the RTTI namespace) and `[sead]` (the diagnostics) are the same engine — the
sequence initializer `007E71F0` carries the RTTI class identity *and* emits
`[sead][!!error!!]seq data invalid!`.

| Severity | Count |
|---|---:|
| `[!!error!!]` | 116 |
| **`[!warn!]`** | **25** |
| `[info]` | 18 |
| **total distinct** | **159** |

**Relabelled 2026-09-02 (§9).** The middle row previously read *"other / bare — 25"*. All 25 are
`[!warn!]`, a **third named severity**. **No bare `[sead]` string exists** — every one of the 159
carries a severity bracket, so SEAD has exactly three levels and nothing miscellaneous.

The trailing-underscore convention in messages (`readState_`, `currentMeter_.sampleRate`,
`startSample_`, `endSample_`, `seekType_`) is a member-variable naming style, so several
strings expose **real field names**.

### What the strings establish

**The audio backend is WASAPI.** Ten strings name `IAudioClient` methods:

```
[sead][!!error!!]IAudioClient::Initialize failed! %x
[sead][!!error!!]IAudioClient::GetMixFormat failed! %x
[sead][!!error!!]IAudioClient::GetBufferSize failed! %x
[sead][!!error!!]IAudioClient::GetDevicePeriod failed! %x
[sead][!!error!!]IAudioClient::IsFormatSupported failed! %x
```

Not XAudio2, not DirectSound — the Windows Audio Session API directly.

**Two compressed formats are decoded.** Eight strings name `HCADecoder_*` — CRI Middleware's
**HCA**:

```
HCADecoder_Create / DecodeHeader / DecodeBlockFloat32 / SetFrameData
HCADecoder_SetDecodeRegion / IsEndOfDecodeRegion / IsDataEmpty / GetFrameSequenceInfo
```

and `MaterialVorbisExtraData::GetSeekOffset` names **Vorbis**. `DecodeBlockFloat32` shows
decode output is 32-bit float.

**Music has a musical-time system.** The largest group — 23 strings mentioning `Music` —
includes meter, tempo and timing conversion:

```
[sead][!!error!!]Can't convert time in current meter. currentMeter_.sampleRate = %d
[sead][!!error!!]GetTimingFromSample Invalid Timing! isValid = %d, startSample_ = %d, sample = %d, endSample_ = %d
[sead][!!error!!]GetSampleFromTiming Invalid Timing! isValid = %d, timing =(%d, %d, %d)
[sead][!!error!!]Can't find original meter index:%d
[sead][!!error!!]Invalid meter index:%d
[sead][!!error!!]Invalid section index = %d
```

A `timing` is a **3-tuple** and converts bidirectionally with sample position through a meter
carrying a sample rate. That is bar/beat/tick musical time — the machinery behind music that
transitions on a musical boundary rather than cutting.

**Voice and bank object model.** Named directly:

| Name | Corroborates |
|---|---|
| `CoreSourceVoice::Render` | `SQEX::Sd::Driver::Core::CoreSourceVoice` (RTTI, 16 methods) |
| `ExternalSourceVoice::QueueBuffer` | `ExternalVoice` (RTTI, 2 methods) |
| `StreamingBank`, `OnMemoryBank` | `SQEX::Sd::Driver::StreamingBank` (RTTI, 14 methods) |
| `AudioStream::MarkAsUnused` | streaming lifecycle with a `readState_` |
| `Category::InitializeRefCategory` | `SQEX::Sd::ConfigFile::Category` (RTTI) |
| `AudioDevice::SetEventHandle` | device layer |
| `EventManager` | event layer |

**Independent corroboration of the RTTI recovery.** These names were recovered from *strings*;
the class list came from *RTTI*. They agree — `CoreSourceVoice`, `StreamingBank`, `Category`
and `Music` appear in both, derived by completely different means.

### Failure modes the engine anticipates

Worth reading as a design statement — these are the conditions it was built to survive:

```
[sead][!!error!!]Action exhausted!!
[sead][!!error!!]LayAction exhausted!!
[sead][!!error!!]ExternalSourceVoice::QueueBuffer failed. queue overflow!!
[sead][!!error!!]EventManager alloc failed.
[sead][!!error!!]CreateSourceVoice failed!!
[sead][!!error!!]Category::InitializeRefCategory referenced category is not initialized( or reference is looping )!
[sead][!!error!!]CreateStreamingMusicBank failed! ( 2 or more && less than NUM_MAX_STREAMS ) streams are needed.
```

**"Action exhausted" and "queue overflow" are pool-exhaustion diagnostics.** The engine
expects finite pools to run dry and says so. That is directly relevant to open question
**G-17** — the sound trigger's unbounded slot counter. It does not resolve G-17, but it
establishes that this engine *does* police some resource limits explicitly, which makes the
absence of a check in the trigger more notable, not less.

`NUM_MAX_STREAMS` is a named constant bound on simultaneous music streams.

## 3. Key addresses

| Address | Role |
|---|---|
| `007E71F0` | sequence initializer — emits `[sead][!!error!!]seq data invalid!`, sets state 1 or 4 |
| `0x01B930E0` | file offset of `[sead][info]%s version %X.%X.%X.%X` |
| `0x01B97DB9` | file offset of `seq data invalid` |

Full extraction with file offsets: `Tools/work/rtti/sead_strings.tsv` (159 rows).

## 4. Data structures and formulas

Field names exposed by the messages (member-variable style, trailing underscore):

```
AudioStream        readState_
Music meter        currentMeter_.sampleRate
Music timing       startSample_ , endSample_ , seekType_
                   timing = (a, b, c)          3-tuple, bar/beat/tick shaped
```

**Musical-time conversion** — bidirectional, named but not yet read:

```
GetTimingFromSample(sample)  -> timing (3-tuple)     validity flag isValid
GetSampleFromTiming(timing)  -> sample               validity flag isValid
                                both bounded by startSample_ .. endSample_
                                and by currentMeter_.sampleRate
```

**Streaming music bank constraint** — stated verbatim by the engine:

```
2 <= streamCount < NUM_MAX_STREAMS
```

No formula here is derived from code; all are read from authored strings. They are targets to
confirm at tier 1, not conclusions.

## 5. Call chain

Not derived in this document. The one anchored point:

```
sound trigger (007BD240)
  -> bind sequence
     -> 007E71F0   sequence initializer
        -> if seq data pointer is null:  emit "[sead][!!error!!]seq data invalid!" , state = 4
           else                                                                      state = 1
```

State 4 is therefore the **invalid/error** state, and state 1 the **initialised** state that
the arm (`007E7300`) requires. `007E72E0` gates on `state != 4`.

## 6. Modding notes

- **These strings are the best naming source in the subsystem.** 159 authored names beat any
  amount of inference. Anyone continuing Audio work should start here.
- **The backend is WASAPI**, so device-level behaviour follows Windows audio session rules —
  exclusive/shared mode, mix format, device period.
- **Two codecs**: HCA (CRI) and Vorbis. A tool touching audio assets needs both.
- **Music is bar/beat/tick aware.** Transitions can be authored on musical boundaries; a
  naive sample-offset edit will fight the meter system.
- **`NUM_MAX_STREAMS` bounds simultaneous music streams**, minimum 2.
- **XIIOnline:** all of this is client-local device and decode state. The existing GZF
  annotation on `007E71F0` already records the policy — *"keep sound-library objects, buffers
  and device state client-local."* Nothing here suggests networking any of it.

## The `Music` meter — `G-21` answered (FABLE, 2026-09-22)

§3 said the meter machinery was *"named but not yet read"*. It is four bodies, and the 23 strings
lead straight to them: `007F31F0` (568 B, the converter), `007F3570` (653 B), `007F3800` (301 B)
and `007F3950` (1,165 B, meter selection). Each was found by sweeping the code for rip-relative
references into the `.rdata` band holding this page's own error strings — the `[sead][!!error!!]`
prefix is `0x11` bytes, so `01CBA058` is the start of *"Invalid meter index:%d"* whose text this
page quotes at `01CBA069`.

### `007F31F0` is a bidirectional unit converter with SAMPLES as the pivot (FABLE, 2026-09-22)

`007F31F0(meter, value, fromUnit, toUnit)` runs **two ladders over the same constants**: the first
multiplies `value` into samples, the second divides samples into the output unit. *That is what the
page's phrase "converts bidirectionally with sample position" is, mechanically.*

| unit | meaning | samples per unit **when a meter is loaded** | **fallback when `+0x18 == 0`** |
|--:|---|---|---|
| 0 | **seconds** | — | `sampleRate` |
| 1 | **samples** | — | 1 (the value passes through) |
| 2 | **tick** | `[meter + 0x24]` | `sampleRate × 0.125` |
| 3 | **beat** | `[meter + 0x28]` | `sampleRate × 0.5` |
| 4 | **bar** | `[meter + 0x2c]` | `sampleRate × 2.0` |

The conversion refuses before any of that if `[meter + 0x30]`, the sample rate, is not positive:
`007F3224 test r10d, r10d` / `jg`, and the fall-through emits this page's
*"Can't convert time in current meter. currentMeter_.sampleRate = %d"* with that very value as the
argument. **So `+0x30` is `currentMeter_.sampleRate`, named by the string that prints it.**

> **The fallback grid is a 4/4 bar at 120 BPM, and it is exact rather than inferred.** The three
> multipliers are `0.125`, `0.5` and `2.0` seconds, so a beat is **half a second** (120 BPM), a bar
> is **four beats**, and a beat is **four ticks** — ratios `1 : 4 : 16`. *A reimplementation that
> picks a different default silently retimes every transition authored while no meter is loaded.*

### The two halves interlock, which is the check on both (FABLE, 2026-09-22)

`007F3950` is the selection side and **writes the same fields the converter reads**: `+0x30` from
`esi` (`007F3AF4`), `+0x24` and `+0x28` together as one qword (`007F3BD0 mov [rbx+0x24], rdi`), and
the flag pair at `+0x18` (`007F3BB4 mov word [rbx+0x18], di`). **On the failure path — the one that
emits *"Can't find original meter index"* (`007F3BB8`) and *"Invalid meter index"* (`007F3D5B`) —
it zeroes the flag and the counts**, which is precisely the state `007F31F0` tests for when it
falls back to the default grid.

> *Reader and writer were read independently and agree on every offset.* **A wrong field map would
> have had to be wrong identically in two bodies** — and the failure path explains the fallback
> branch rather than merely coexisting with it.

**What is not read here:** `007F3570` and `007F3800`, which carry the remaining four meter strings;
and what populates a meter in the first place — `007F3950` selects one by index from a table whose
origin this section does not establish.

## 7. What is not known

- [x] Which function emits each of the 159 strings — the string→function mapping would name
      dozens of functions at once. **G-20.**
- [x] ~~The `Music` meter/timing implementation. 23 strings point at it; none of it is read.~~
      **G-21 ANSWERED 2026-09-22 (FABLE)** — four bodies (`007F31F0`, `007F3570`, `007F3800`,
      `007F3950`); `007F31F0(meter, value, fromUnit, toUnit)` converts bidirectionally through
      samples over five units (seconds, samples, tick, beat, bar), with the per-unit sample counts
      at `+0x24`/`+0x28`/`+0x2c` and the sample rate at `+0x30`. See the section above.
- [x] Value of `NUM_MAX_STREAMS`. **G-22.**
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (G-22):* **the compiled bound accepts 2 to
      16 streams.** `CreateStreamingMusicBank`'s check in `007B1E10` loads the stream count as a byte
      (`movzx r12d, byte [rbp+0x100]`, `007B1EC5`) and computes `lea eax, [r12 − 2] ; cmp al, 0xE ; ja error`
      (`007B1ECD`–`007B1ED4`). The error branch `007B2182` formats this page's `CreateStreamingMusicBank failed!` string
      (`007B2186`). So 2–16 pass and everything else fails. If the message's "less than `NUM_MAX_STREAMS`" is literal, the
      constant is **17**; if the source compares with `<=`, it is 16. The binary fixes the range, not the spelling of the
      name.
- [x] ~~Whether the HCA and Vorbis paths are both live in this title or one is vestigial.~~
      **G-23.** *Answered 2026-09-16 (FABLE), in the register, and the box was never ticked; closed 2026-09-25 (FABLE,
      Claude Opus 5.5):* **both are reached by static call edges.** CRI HCA has 26 edges from 11 external callers,
      Tremor 13 from 4, and libvorbis 17 from 5. libvorbis is reached two hops from the movie player through
      `0067A480` → `00679A50`, which contradicts the middleware inventory's *reached by nothing* (filed as
      `FABLE-CONTRA-LIBVORBIS-IS-REACHED-BY-THE-MOVIE-PLAYER`). *Reached* means a caller exists, not that it runs.
- [x] What `Action` and `LayAction` pools are, and their capacities — related to **G-17**.
      **G-24.**
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (G-24):* **they are free lists of fixed-size
      command records, one for the `Sd::Driver` layer and one for `Lay`. The game sizes them at 1,024 and 512.**
      - **The `Action` pool.** Built by `007AB390(n)`. It allocates `n × 40` bytes (`007AD550`, memory category 0) and
        clears them. It then takes a node from the queue object `02EAD010`'s spare-node list `02EAD020` for each record,
        points the node at the record (`+0x08`), and appends it to the free queue: head `02EAD028`, tail `02EAD030`,
        count `02EAD03C`. The allocator `007AB460`, under the critical section `02EAD070`, dequeues the head, returns
        its record, and gives the node back to the spare list. When the head is null it formats
        `"[sead][!!error!!]Action exhausted!!"` (`007AB4A7`), reports it through `007A5570(2, …)`, and returns
        `0x80000001`.
      - **The `LayAction` pool.** Built by `007BAC80(n)` with the same shape: `n × 80` bytes (category 3), queue object
        `02EADD70` (spare nodes `02EADD80`, head `02EADD88`, tail `02EADD90`, count `02EADD9C`). Its allocator `007BAD60`
        runs under `02EADDD0`, with the string at `007BADA7`.
      - **Capacities.** The game's audio start-up `00210760` fills the driver init block at `rsp+0x50`, whose `+0x30` is
        **`0x400`** (`00210855`). `007A4D50` passes that field to `007AB390` (`007A4FAD`–`007A4FB0`). The `Lay` init
        block at `rsp+0x20` has `+0x08` = **`0x200`** (`002108BD`), which `007A5B50` passes to `007BAC80`
        (`007A5C71`–`007A5C7C`).
      - **The containers.** Each builder initialises two queue objects through a shared routine: `007AB390` does
        `02EAD010` and `02EAD040` (`007AB240`), and `007BAC80` does `02EADD70` and `02EADDA0` (`007BAB30`). The free
        list above is `02EAD010 + 0x18`. MSVC RTTI names `02EAD040` `FixedQueue<Driver::ACTION*>` and both `Lay` objects
        `FixedQueue<Lay::ACTION*>`
        ([static initialization, T-8](../24-Compiler-And-CRT-Runtime/Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md)).
        The integer in each template (`0` Driver, `3` Lay) matches the allocator's memory category, `edx` = 0 at
        `007AB39D` and 3 at `007BAC8D`.
      
      **Not established:** what an `ACTION` record holds, and how often either pool comes near exhaustion in play
      (live-only).

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The engine is named SEAD | 159 authored strings prefixed `[sead]`, extracted from the authorized EXE at known file offsets | 2 |
| `SQEX::Sd` and `[sead]` are the same engine | `007E71F0` carries the RTTI class identity and emits `[sead][!!error!!]seq data invalid!` | 1 + 2 + 4 |
| Backend is WASAPI | ten `IAudioClient::*` diagnostics | 2 |
| HCA and Vorbis are decoded | eight `HCADecoder_*` strings; `MaterialVorbisExtraData::GetSeekOffset` | 2 |
| Decode output is 32-bit float | `HCADecoder_DecodeBlockFloat32` | 2 |
| Music uses bar/beat/tick timing | `GetTimingFromSample` / `GetSampleFromTiming` with a 3-tuple and `currentMeter_.sampleRate` | 2 |
| Sequence state 4 = invalid, 1 = initialised | `007E71F0` sets 4 on a null data pointer immediately after emitting the error, 1 otherwise | 1 |
| The engine polices pool limits explicitly | `Action exhausted!!`, `queue overflow!!`, `EventManager alloc failed.` | 2 |

**Method note:** `strings(1)` returned **zero** `[sead]` hits on this binary; a raw byte scan
found all 159. The extraction was verified by locating `[sead][info]%s version...` at file
offset `0x01B930E0` and reading its surrounding bytes. Had the negative `strings` result been
trusted, this entire vein would have been missed — a reminder that a tool returning nothing is
not evidence of nothing.

## 9. Related

- [`sqex-sd-sound-driver-architecture.md`](sqex-sd-sound-driver-architecture.md) — the RTTI class hierarchy these names corroborate
- [`Sound-Selection/sound-trigger.md`](Sound-Selection/sound-trigger.md) — where sequence state 1/4 is consumed

## 9. Falsification pass 2026-09-02

**Attack chosen.** This document is a string census with a stated total and a three-row split — the
table shape that failed in
[`../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`](../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md)
§9, where a correct total sat over a wrong breakdown. The census was therefore re-run from the
shipping EXE **row by row**, not just totalled.

### SURVIVED: every count is exact

| Row | Document | Census |
|---|---:|---:|
| `[!!error!!]` | 116 | **116** |
| third severity | 25 | **25** |
| `[info]` | 18 | **18** |
| **total distinct** | **159** | **159** |

The scan also establishes a property the document did not claim: there are **159 raw occurrences of
`[sead]` in the image and 159 distinct strings**, so **every diagnostic literal appears exactly
once**. No message is duplicated across translation units, which is why the distinct count and the
occurrence count coincide and why "159 authored strings" needs no qualification.

### CORRECTED: the 25 are not "other", they are a named severity

The middle row read *"other / bare"*, which implies a residue of unclassifiable strings. It is not.
**All 25 carry the tag `[!warn!]`**, and a check for strings matching `[sead]` *without* a severity
bracket returns **zero**. SEAD has exactly **three** severity levels:

```
[sead][!!error!!]  116
[sead][!warn!]      25
[sead][info]        18
```

**Why this matters beyond tidiness.** A named warning tier is a statement about what the audio
engine treats as *recoverable*, and the warnings say so explicitly:

```
[sead][!warn!]GetSampleFromTiming timing is before startTiming. assumed it's equal to startTiming
[sead][!warn!]GetSampleFromTiming timing is over endTiming. assumed it's equal to endTiming
[sead][!warn!]Music::CheckTransitionTime Failed to sync to (%d,%d,%d)
[sead][!warn!]ExternalSoureVoice::Resume not available %d id buffer
[sead][!warn!]SeekData no support format!!! %d
```

The first two state the **clamping rule outright**: a seek timing outside the sample's range is
*assumed equal to the nearest bound* rather than rejected. The third shows music transitions are
synchronised on a `(bar, beat, tick)`-style triple and that a failed sync is survivable. Filed as
"other", these read as noise; recognised as a severity tier, they are the engine documenting its own
tolerances — which is precisely what §1 says these strings are for.

*(The misspelling `ExternalSoureVoice` is verbatim from the binary, not a transcription error.)*

## Cross-subsystem neighbours - SWE2-DATA (pass-22 dispositions, 2026-10-02)

- **Resource - SERVICE (4 edges).** `00210760` reaches bodies filed to resource: `001D6E80`, `001D6EE0`, `001D6F20` (+1 more) - shared machinery across the layer boundary, no shared ownership.

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../_index/candidates/opus-sead-engine-identity-and-diagnostics-ee-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `007AB240` | 334 B | Releases the 0x18-byte element array at `rcx+8` when it is non-null (through the first element's vtable slot `+0` with `edx`=3 when the count qword before it is non-zero, else `00210EB0` on the block), zeroes the qwords `+8` to `+0x20` and dword `+0x2C`, and returns 0xF0000000 when `edx` is zero; otherwise it stores `edx` to `+0x28`, allocates the count times 0x18 plus 8 bytes (saturated to -1 on overflow) through `007AD460` with 8 and 0, writes the count to the block's first qword and initialises each element to the pointer `01CB45D8` followed by two zero qwords (using a null array when the allocation fails), stores the array to `+8` and `+0x10`, links each element's qword `+0x10` to the next element, zeroes `+0x18`, `+0x20` and `+0x2C` and returns 0. | `007AB26D`, `007AB293`, `007AB2E6`, `007AB310`, `007AB366` |
| `007BAB30` | 334 B | Releases the 0x18-byte element array at `rcx+8` when it is non-null (through the first element's vtable slot `+0` with `edx`=3 when the count qword before it is non-zero, else `00210EB0` on the block), zeroes the qwords `+8` to `+0x20` and dword `+0x2C`, and returns 0xF0000000 when `edx` is zero; otherwise it stores `edx` to `+0x28`, allocates the count times 0x18 plus 8 bytes (saturated to -1 on overflow) through `007AD460` with 8 and 3, writes the count to the block's first qword and initialises each element to the pointer `01CB57D8` followed by two zero qwords (using a null array when the allocation fails), stores the array to `+8` and `+0x10`, links each element's qword `+0x10` to the next element, zeroes `+0x18`, `+0x20` and `+0x2C` and returns 0. | `007BAB5D`, `007BAB83`, `007BABD7`, `007BAC00`, `007BAC56` |
| `007E71F0` | 234 B | Copies the qword at `[rdx]` to `rcx+8`, the qword at `[r8]` to `rcx+0x10` and the qword at `r9+8` to `rcx+0x28`; when that last value is non-zero it sets dword `+0x9C` to 1, stores the pointer `01CB4D48` to `[r9]` and returns 0, otherwise it formats `01CB8FA8` through `0019C5D0` into a 256-byte stack buffer, appends a newline (calling `00809728` if the terminator index reaches 0x100), passes the buffer to the import at `008C2120` and to `007A5570` with 2, sets `+0x9C` to 4, stores `01CB4D48` to `[r9]` and returns -1, both returns checking the stack cookie from `01F44830` through `00808C40`. | `007E7227`, `007E7241`, `007E7280`, `007E728C`, `007E72A5` |
| `007F31F0` | 568 B | Returns 0.0 in `xmm0` when `xmm1` compares equal to 0 or unordered (`ucomiss`/`je`), and also, after formatting `01CBA280` with the dword `rcx+0x30` through `0019C5D0` and logging it through the import at `008C2120` and `007A5570` with 2, when that dword is not greater than zero; otherwise it converts `xmm1` to a truncated integer by the unit code in `r8d` (0: times dword `+0x30`; 1: as is; 2, 3, 4: times dword `+0x24`, `+0x28` or `+0x2C` when byte `+0x18` is non-zero, else times `+0x30` and 0.125 (`00915508`), 0.5 (`01CEBB70`) or 2; other codes give 0), then converts that integer to the unit code in `r9d` as a float (0: divided by `+0x30`; 1: as is; 2, 3, 4: divided by `+0x24`, `+0x28` or `+0x2C` when byte `+0x18` is non-zero, else by `+0x30` divided by 8, by `+0x30` divided by 2, or by twice `+0x30`; other codes 0.0) and returns it, checking the stack cookie through `00808C40`. | `007F3217`, `007F3227`, `007F32E3`, `007F3321`, `007F33FC` |
| `007F3570` | 653 B | When byte `rcx+0x18` is zero it formats `01CBA220` with 0 and the signed word `+0`, byte `+2` and byte `+3` of the position at `rdx` through `0019C5D0`, logs it through the import at `008C2120` and `007A5570` with 2, and returns the dword at `rcx+0`; otherwise it copies the position to a stack triple and, if that compares greater (signed: word, then byte `+2`, then byte `+3`) than the triple at `+0xC`/`+0xE`/`+0xF`, logs `01CBA140` with word `+0xC` (`007A5570` with 1) and replaces the copy with that triple, or if it compares below the triple at `+8`/`+0xA`/`+0xB`, logs `01CBA1B0` with word `+8` and replaces the copy with that one; it returns the dword `+4` when the copy equals the `+0xC` triple, else calls `007F3140` with the copy, `rcx+8` and `rcx` and returns dword `+0` plus the copy's signed word times dword `+0x2C`, byte `+2` times dword `+0x28` and byte `+3` times dword `+0x24`, checking the stack cookie through `00808C40`. | `007F35BE`, `007F3625`, `007F3694`, `007F374A`, `007F3774` |
| `007F3800` | 301 B | Zeroes the dword at `rdx` and, when byte `rcx+0x18` is zero or `r8d` lies outside the dwords `rcx+0` and `rcx+4` (signed `jg` compares), formats `01CBA0C0` with that byte, both bounds and `r8d` through `0019C5D0`, logs it through the import at `008C2120` and `007A5570` with 2 and returns `rdx`; otherwise it splits `r8d` minus dword `+0` by signed division into a quotient by dword `+0x2C` (added to word `+8`), the remainder's quotient by dword `+0x28` (added to byte `+0xA`) and the rest's quotient by dword `+0x24` (added to byte `+0xB`), stores them as word `+0`, byte `+2` and byte `+3` of the out-record at `rdx`, calls `007F2EA0` with it and `rcx`, and returns `rdx`, checking the stack cookie through `00808C40`. | `007F3822`, `007F3837`, `007F3848`, `007F3891`, `007F389B` |
