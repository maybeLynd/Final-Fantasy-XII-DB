---
system: SEAD function identification (string cross-reference)
category: 18-Audio
status: AUDITED
owner_layer: PrimaryOwner:Audio
evidence_tier: 2
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN158 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). Of the functions classified since GN158 this document cites none of batch R109's 109; the 21 classified before GN160 are named in AUDIT-LOG's batch records and not in a tracked machine-readable list, so identity is not claimed. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md, lineage extension (twenty ledger figures across five generations)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-02
audit:
  passes: 2
  last_pass: 2026-09-02
  last_pass_state: falsification-pass
  crossref_clean: false        # 2026-09-30 (SWE2-DATA): false until the pass-22 UNACCOUNTED NEIGHBOUR findings are accounted (FRONTIER-REQ-SWE2-DATA-PASS22-DEBT; OPUS-REQ-DATA-PASS30-CROSSREF-CLEAN-0930)
  reopened_count: 0
function_families:
  - "SQEX SEAD sound library span | C | members/sead-library-span.tsv | 1122 | Square Enix SEAD sound runtime (SQEX::Sd - Driver, Lay, Magi, ConfigFile, MabFile, SabFile, WASAPI and Core backends), statically linked, not FFXII code. Members = every census entry in the link span from 007A4380 up to (not including) 007F41A0 (members/select_audio_libraries.py) less the libogg framing object inside it (own row on the middleware inventory), one entry whose RTTI class is outside SQEX::Sd, five ICF-folded bodies shared with other classes, A-measured entries and OPUS's forwarder family, plus nine SEAD entries just past the span that RTTI or their only callers prove SEAD's (sec.13). Lower edge follows the PhyreEngine framework object, upper edge is the start of Tremor's vorbisfile (sec.13). Controls: the span's 53 outbound call targets are CRT, the CRI HCA decoder and the Xiph code past the edge - none is game code - and no .data global is shared with game code (outside referencers are static-lifetime thunks and the Xiph allocator hooks only). Boundary: the SEAD bodies in the span; FFXII's audio layer (AudioController family at 0021xxxx), Tremor/vorbisfile, the CRI HCA decoder and SEAD entries outside the span are NOT covered 11 members left the family 2026-09-17, since measured as A (A beats a declaration): 007AC4F0 and ten more, dropped by re-running members/select_audio_libraries.py; a twelfth member, 007F20E0, went A on the 2026-09-18 re-sweep, and four more — 007CF6B0, 007CFF90, 007D0210, 007D0580 — left on the same date's selector re-run. 26 member(s) left the family 2026-09-20, since measured as A (A beats a declaration): 007A78B0 and 25 more 33 member(s) left the family 2026-09-29, since measured as A (A beats a declaration); every removed address and its reason is in _index/candidates/ec7-refused-family-repair-0929/removed-members.tsv. Re-derived by re-running members/select_audio_libraries.py, which now leaves the UC-1 frontier bodies out of its population (unpatched it failed its libvorbis closure assertion); its SEAD output equals this file and its five other lists are unchanged. The declared 1144 set on 2026-09-20 had subtracted 26 A departures without regenerating the file (1,170 lines), which refused the row; file and count now agree. One more member left because the UC-1 series break adjudicated it a false entry and removed it from the population (uc1_band), so it is no longer a census entry. 2026-09-30 (SWE2-EC7, DD re-status A-drift, record _index/candidates/ec7-dd-adrift-pairing-0930): 6 member(s) left the family, since measured as A (A beats a declaration) after OPUS re-statused the two SEAD audio architecture pages (d39c8ccbd, 4) and the EASTL strings page (8c8406bfd, 2) DOCUMENTED; select_audio_libraries.py re-run on a clean HEAD export drops exactly these six, admits nothing and leaves its five other library files unchanged; the members file is the selector's output; addresses and causing pages in the record. 2026-09-30 (SWE2-EC7, DD re-status A-drift round 3, record _index/candidates/ec7-dd-adrift-pairing-0930): 7 member(s) left the family, since measured as A (A beats a declaration) after OPUS re-statused sound-variant-selection.md (e54b8e670) DOCUMENTED; select_audio_libraries.py re-run on a clean HEAD export drops exactly these seven, admits nothing and leaves its five other library files unchanged; the members file is the selector's output; addresses and causing pages in the record (pairing-round3.tsv). 2026-10-01 (OPUS for SWE2-EC7, A-drift paired with owner re-status batch 15, record _index/candidates/opus-dd-restatus-15-1001): 1 member(s) left the family, since measured as A (A beats a declaration) after OPUS re-statused the text-element dispatch table page DOCUMENTED (owner batch 15); exact A removal in the same publish (selector not re-run); addresses and causing pages in the record."
  - "SQEX SEAD, UC-1 body in its span | C | members/sead-span-uc1.tsv | 1 | not this game's code: a SEAD body in the span, declared apart from the parent row under FABLE family ruling R1 (4e32dd8df) by SWE2-EC7, record _index/candidates/ec7-uc1-span-rows-0929. 1 UC-1 bodies admitted to frontier 2026-09-28, dispositioned by span 2026-09-29. TEST 1: strictly inside 007A4380 up to 007F41A0 between two listed SEAD members. TEST 2: select_audio_libraries.py re-run with it in its population admits it, every assertion holds, and the outbound and globals controls are unchanged. TEST 3: its one reference is a rip-relative operand inside the span, and it reaches nothing outside the span that the listed SEAD members do not. Generator: _index/candidates/ec7-uc1-span-rows-0929/uc1_span_tests.py --write."
---

# SEAD function identification

> **90 previously anonymous audio functions** now have names — because the code tells you
> which method it is when it fails.

## 1. What the player sees

Nothing. This is a naming result, not a behaviour.

Its value is downstream: every future finding about FFXII's sound — why an effect cuts out,
how panning works, what happens when too many sounds play at once — has to be pinned to a
specific function. Ninety of those functions just stopped being anonymous.

## 2. Native mechanism

SEAD's diagnostics name the method that raised them
(`Sound::SetPitch failed range over %f`). Each string is referenced by a RIP-relative `LEA`
in the function that emits it, so scanning `.text` for those references attributes each
string to a function.

```
48 8D /r disp32     REX.W    -> lea r64, [rip + disp32]
4C 8D /r disp32     REX.WR   -> r8..r15
  modrm.mod == 00 and modrm.rm == 101
  target = address_of_next_instruction + disp32
```

Matching those targets against the 159 `[sead]` string addresses and resolving each
instruction to its containing function gives:

| Result | Value |
|---|---:|
| `[sead]` strings | 159 |
| LEA references found | **208** |
| Functions attributed | **90** |
| References not inside any known function | **0** |
| Functions still named `FUN_*` before this | **90 (100 %)** — **guaranteed by the population: all 2,064 `Audio`-owned functions are `FUN_*`. Section 12.** |

Tooling: `Tools/analysis-kit/gfz-scripts/string_xref.py`, output
`Tools/work/rtti/sead_xrefs.tsv`. It needs no Ghidra project, so it runs alongside headless work.

### Cross-validation against RTTI — the load-bearing result

**17 of the 90 also appear in the independently recovered RTTI vtable mapping.** Those two
derivations share no method: one reads vtables and type descriptors, the other reads authored
strings and instruction encodings. Every overlapping case agrees:

| Address | RTTI class | Emitted string |
|---|---|---|
| `007B93E0` | `SQEX::Sd::Driver::ExternalSourceVoice` | `ExternalSourceVoice::QueueBuffer failed. queue overflow!!` |
| `007B9770` | `SQEX::Sd::Driver::ExternalSourceVoice` | `ExternalSoureVoice::Resume not available %d id buffer` |
| `007BE3F0` | Sound family *(shared across all six)* | `Sound::SetLowpassValue failed range over %f` |
| `007BE590` | Sound family *(shared)* | **three** strings, not one — `Sound:*SetPanning pan range over! %f`, `…frpan…`, `…udpan…` (the single slashed line here was a composite; corrected §9) |
| `007BE8A0` | Sound family *(shared)* | `Sound::SetPitch failed range over %f` |

**Zero contradictions.** That is the strongest corroboration available in this database:
two methods, no shared assumptions, same answer.

Note `ExternalSoureVoice` — a typo in Square Enix's own string. Preserved verbatim; it is a
useful authenticity marker, and a reminder that authored evidence carries authored mistakes.

The Sound-family rows also explain something the vtable data alone could not: `007BE3F0`,
`007BE590` and `007BE8A0` appear under **all six** Sound classes because they are shared base
methods — and the strings confirm they are `Sound::Set*` parameter setters, exactly the kind
of method a base class would implement once.

### Named methods recovered

Directly stated by the strings:

| Method | Function |
|---|---|
| `Voice::Initialize` | `007EBAD0` — 27 strings, also all the `HCADecoder_*` errors |
| `Sound::SetLowpassValue` | `007BE3F0` |
| `Sound::SetPanning` *(pan, frpan, udpan)* | `007BE590` |
| `Sound::SetPitch` | `007BE8A0` |
| `ExternalSourceVoice::QueueBuffer` | `007B93E0` |
| `ExternalSourceVoice::Resume` | `007B9770` |
| `Category::InitializeRefCategory` | `007AA320` |
| `CreateStreamingBank` | `007B1AB0` |
| `CreateStreamingMusicBank` | `007B1E10` |
| *(sequence init)* `seq data invalid` | `007E71F0` |

`007EBAD0` is `Voice::Initialize` and is where HCA decoding is set up — it emits
`Voice::Initialize memory allocate failed`, `no support format`, `couldn't find loading
audioStream`, and eight distinct `HCADecoder_*` failures. It is the single richest diagnostic
site in the subsystem. Interior read 2026-09-17 (SWE2-FRONTIER): `007B2470`/`007D0890` head the
body at [`007EBB51`](../_index/ADDRESS-INDEX.md); the decoder calls land at the CRI HCA band
(`001221B0`/`00123A50`/`00123870` ×2 each), the `007AD550` member-registration helper ×11, and
the `0019C5D0` logger carries all 27 `[sead][!!error!!]` strings.

`Sound::SetPanning` reporting three separate ranges — `pan`, `frpan`, `udpan` — indicates
~~**three panning axes**, not one: left/right, front/rear, and up/down.~~ three ranges, but not three axes: the driver turns `pan` into an azimuth and `frpan` into a distance factor, and carries `udpan` down to `007B8430` without using it *(corrected 2026-10-02, OPUS, from UQ-242's dated answer - the request page's geometry)*.

## 3. Key addresses

The full mapping is `Tools/work/rtti/sead_xrefs.tsv` (208 rows: function, name, owner,
instruction, string). Highest-yield sites:

| Function | Strings | Identity |
|---|---:|---|
| `007EBAD0` | 27 | `Voice::Initialize` + HCA decode setup |
| `007DE2F0` | 10 | unidentified |
| `007EAA60` | 9 | unidentified |
| `007DEFB0` | 6 | unidentified |
| `007C92F0` | 6 | unidentified |
| `007C23C0` | 6 | unidentified |

### The diagnostics are visible at runtime

`Sound::SetVolume` formats its message then calls:

```c
OutputDebugStringA(msg);
FUN_007a5570(1, msg);          // severity-tagged logger, 1 = warn
```

**SEAD's 159 diagnostics go to `OutputDebugStringA`.** They are therefore observable live in
any debugger or in DebugView — no patching required. For anyone diagnosing FFXII audio, the
engine already narrates its own failures; you just have to listen.

`FUN_007a5570(severity, msg)` is the internal sink, called alongside, with the severity as
its first argument.

### A worked setter

```c
Sound::SetVolume(this, float volume, ...)
    if (volume < 0.0f || volume > DAT_01cebba8)
        warn "[sead][!warn!]Sound::SetVolume failed range over %f"
```

The upper bound is a global (`DAT_01cebba8`), not a literal — ~~so the volume ceiling is
configurable rather than hardcoded.~~ but that global is the float constant 1.0, which no instruction writes (1,488 reads), so the ceiling is fixed at 1.0 *(corrected 2026-10-02, OPUS, at the bytes)*.

## 4. Data structures and formulas

**Reference resolution:**

```
target_va = insn_va + 7 + disp32          (7 = length of a REX.W LEA r64,[rip+disp32])
```

**Attribution:**

```
function(addr) = the f with  f.entry <= addr < f.entry + f.body_bytes
```

**Sound::SetVolume range gate:**

```
valid  iff  0.0 <= volume <= DAT_01cebba8      (upper bound is a global, not a literal)
```

No behavioural formula — this document produces identity, not mechanism.

## 5. Call chain

Not applicable. This is a naming result. Each named function's chain belongs in its own
document.

## 6. Modding notes

- **Start any SEAD investigation from `sead_xrefs.tsv`.** Ninety named functions beat any
  amount of inference, and the naming is authored rather than derived.
- **`007EBAD0` (`Voice::Initialize`) is the diagnostic hub.** If audio fails to start, its 27
  failure modes are the checklist.
- **Panning has three axes** (`pan`, `frpan`, `udpan`) — a mod assuming stereo will be wrong.
- **The technique generalises — proven, not hoped.** `string_xref.py` takes any literal
  prefix. Run against post-processing prefixes it attributes **299 references to 137
  functions with 0 unattributed**, the same clean result as audio. 67 classes are named in
  strings binary-wide.

## 7. What is not known

- [x] The other 73 attributed functions have a string but no recovered *method* name — many
      strings describe a condition rather than naming a method. **G-25.**
      *SUPERSEDED 2026-09-26 (FABLE, Claude Opus 5.5) under FRONTIER's class-1 ruling: a population-coverage statement; the population is carried by 18-Audio/sead-function-identification.md. See the register row.*
- [x] Identity of the high-yield sites `007DE2F0`, `007EAA60`, `007DEFB0`, `007C92F0`,
      `007C23C0`. **G-26.**
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (G-26):* all five are named, three of them by
      RTTI slot position:

      | site | identity | evidence |
      |---|---|---|
      | `007DE2F0` | **`SQEX::Sd::Driver::WASAPI::WASAPIDevice` slot 1, the WASAPI output open**: device enumerator → default console device → `IAudioClient` activate, `GetMixFormat`, `Initialize`, `IsFormatSupported`, `GetDevicePeriod`, `GetBufferSize` → render client and session control | slot 1 of vtable `01CB7B80`, whose locator `01D451D8` names `WASAPIDevice`; its ten strings follow that call order. Interior (2026-09-17, SWE2-FRONTIER): the enumerator-instantiate failure path loads its GUID pair `01CB7C70`/`01CB7C80` and the `"Unable to instantiate device enumerator: %x"` string at `007DE328`–`007DE349`, reported via `0019C5D0` at [`007DE35A`](../_index/ADDRESS-INDEX.md) |
      | `007DEFB0` | **`WASAPIDevice`'s `IAudioSessionEvents::OnSessionDisconnected`** | slot 9 of the sub-vtable `01CB7C20` at object `+0x18`. RTTI lists `IAudioSessionEvents` at `mdisp 24`. Slots 3–7 are the `xor eax, eax ; ret` stub `007AD440` and slot 8 is `007DF1F0`, exactly the interface's order. Its six strings are the six `AudioSessionDisconnectReason` values in enum order. |
      | `007EAA60` | **a voice's decode-and-submit step**: HCA through `HCADecoder_*` and Ogg Vorbis through `sead_ov_read`, then `sourcesubmit` | strings. Its callers are `007ED4C0` and `007EDA60` in the voice code; the class and method name are not recovered. Interior read 2026-09-17 (SWE2-FRONTIER): `007B2470` at [`007EAAD1`](../_index/ADDRESS-INDEX.md) heads the body, `007F7350`/`007F6FB0` follow — all nine error strings verified in-body (`HCADecoder_DecodeBlockFloat32`, `IsDataEmpty`, `IsEndOfDecodeRegion`, `SetFrameData`, `sead_ov_read`, `sourcesubmit`). |
      | `007C92F0` | **`Magi::Music::SetMode`** | its own string `"Music::SetMode fromModeIndex == targetModeIndex == %d"` (loaded at [`007C95E0`](../_index/ADDRESS-INDEX.md), reported via `0019C5D0`); called twice from `007CC4A0`. Interior: installs vtables `01CB4440`/`01CB5DA8`, drives the `007D01E0`–`007D0600` driver-accessor family + `007B2470`/`007B5E50`/`007E3040`/`007E4F10`/`007EBA40`/`007EE670`, with vtable dispatches `[rax+0x30]` (`007C9443`) and `[rdx+0x20]` (`007C96C0`) |
      | `007C23C0` | **the `Music` section-transition request (`SetNextSection`)** | `"SetNextSection canceled! Transitioning to next music..."` and `"Invalid section index"`; called from `007C4790`. Interior (2026-09-17, SWE2-FRONTIER): all five of its error strings verified in-body — plus `"Invalid custom point index = %d, numCustomPoints = %d"` (`007C2725`), `"There is no custom points!"` (`007C279B`), `"Transition state is invalid!"` (`007C27FE`) — and the `01CB5D88` vtable (RTTI `007C1410`) is installed at [`007C2554`](../_index/ADDRESS-INDEX.md); helper fan-out `0019C5D0` ×6, `007D0600` ×5, `007B5E50` ×4 |

      `WASAPIDevice`'s bases per RTTI are `AudioDevice`, `SeadObject<1,8>` (RTTI `$00$07`), `IMMNotificationClient` (at `+0x10`) and
      `IAudioSessionEvents` (at `+0x18`).
- [x] ~~Whether other subsystems carry authored diagnostics worth the same treatment.~~
      **CLOSED — yes.** 67 classes are named in strings binary-wide; the post-processing
      subsystem alone yields **137 nameable functions from 299 references**. Tracked as
      **H-1**.
- [x] **UQ-265.** None of the 90 has had its *body* read. These are identities, not mechanisms.
      *SUPERSEDED 2026-09-26 (FABLE, Claude Opus 5.5) under FRONTIER's class-1 ruling: a population-coverage statement; the population is carried by 18-Audio/sead-function-identification.md. See the register row.*

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| 208 references across 90 functions | `string_xref.py` over the authorized EXE joined to the 38,161-function table | 2 |
| The scan is correct | `007E71F0` was independently decompiled in a prior block and read to emit `seq data invalid!`; the scanner attributes exactly that string to exactly that function | 1 + 2 |
| No spurious matches | **all 208** references land in `Audio`-owned functions; a faulty scan would scatter across owners. **Quantified in section 12: `Audio` is 5.41 % of the binary, so a scattering scan would put ~11 of 208 there. This is the document's strongest single result.** | 2 |
| Attribution is complete | 0 references fell outside a known function body | 2 |
| RTTI and strings agree | 17 functions appear in both mappings, **zero contradictions**, e.g. `007B93E0` is an `ExternalSourceVoice` method by RTTI and emits `ExternalSourceVoice::QueueBuffer` | 2 + 4 |
| Sound `Set*` methods are shared base methods | they appear under all six Sound classes in RTTI *and* name themselves `Sound::` in strings | 2 + 4 |
| Panning has three axes | `Sound:*SetPanning` reports `pan`, `frpan`, `udpan` separately | 2 |

**Scope honesty:** this document assigns *identities*, not behaviour. `007BE8A0` is
`Sound::SetPitch` because it says so when it fails — that does not mean its body has been read
or that its range-clamping is understood.

## 9. Related

- [`sead-engine-identity-and-diagnostics.md`](sead-engine-identity-and-diagnostics.md) — the 159 strings and what they establish
- [`sqex-sd-sound-driver-architecture.md`](sqex-sd-sound-driver-architecture.md) — the RTTI mapping this corroborates
- [`Sound-Selection/sound-trigger.md`](Sound-Selection/sound-trigger.md) — the trigger's parameter ops, likely `Sound::Set*` siblings

## 9. Falsification pass 2026-09-02

**Attack chosen.** This document is a count and an attribution table, both produced by a tool this
database still has. Every figure in §2 can therefore be **regenerated from scratch** rather than
re-read — the strongest form of check available for a claim of this kind.

### SURVIVED exactly — every figure reproduced

`string_xref.py` re-run against the authorized EXE for the pattern `[sead]`:

| Figure | Document | Re-derived |
|---|---:|---:|
| LEA references found | 208 | **208** |
| Functions attributed | 90 | **90** |
| References not inside any known function | 0 | **0** |
| `007EBAD0` | 27 | **27** |
| `007DE2F0` | 10 | **10** |
| `007EAA60` | 9 | **9** |
| `007DEFB0` / `007C92F0` / `007C23C0` | 6 each | **6 each** |

**Nothing drifted.** The distinct-string count also agrees with the sibling document
[`sead-engine-identity-and-diagnostics.md`](sead-engine-identity-and-diagnostics.md): 159
matched here against the 159 distinct `[sead]` strings counted there.

### SURVIVED: all five cross-validated attributions, verbatim

Each of the five RTTI cross-checks in §2 was confirmed against the regenerated reference table —
the named function does reference the quoted string:

```
007B93E0  [sead][!!error!!]ExternalSourceVoice::QueueBuffer failed. queue overflow!!
007B9770  [sead][!warn!]ExternalSoureVoice::Resume not available %d id buffer
007BE3F0  [sead][!warn!]Sound::SetLowpassValue failed range over %f
007BE590  [sead][!warn!]Sound:*SetPanning pan range over! %f
007BE8A0  [sead][!warn!]Sound::SetPitch failed range over %f
```

### CORRECTED: one table cell was a composite, not a quotation

`007BE590` references **three** distinct strings, and the document rendered them as a single line
with slashes — `Sound:*SetPanning pan / frpan / udpan range over! %f`. No such string exists. The
three that do are:

```
[sead][!warn!]Sound:*SetPanning pan range over! %f
[sead][!warn!]Sound:*SetPanning frpan range over! %f
[sead][!warn!]Sound:*SetPanning udpan range over! %f
```

The summary is accurate in substance — the function does handle three panning ~~axes~~ ranges *(only two are used; see §2, corrected 2026-10-02, OPUS)* — but it sat in a
column of otherwise **verbatim** quotations, where a reader has no way to tell a synthesis from a
literal. In a database that treats an authored string as tier-2 evidence, **a quoted string must be
quotable**. Corrected in §2, and it also strengthens the attribution: three separate diagnostics all
naming `SetPanning` bind that function harder than one would.

### Two shipped typos, worth noting because they are load-bearing

Both are verbatim in the retail binary:

- **`ExternalSoureVoice`** — missing the `c`, while the RTTI class is `ExternalSourceVoice`.
- **`Sound:*SetPanning`** — an asterisk where every sibling string has `::`.

They matter beyond curiosity: a search for `ExternalSourceVoice` or `Sound::SetPanning` **will not
find these strings**. Anyone extending this identification by grepping for a correctly spelled method
name will silently miss both functions — which is the same instrument-shaped blind spot this database
has recorded repeatedly, in a new guise.

## 12. Audit — one 100 % is worthless and the other is decisive

This document contains two saturated figures. **Checking them against their base rates separates them
completely**, and the difference is entirely the denominator.

### `90 (100 %) still named FUN_*` — could not have come out otherwise

```
PrimaryOwner:Audio    2,064 functions    100.0 % still named FUN_*
```

**Every `Audio`-owned function in the image is named `FUN_*`** — all 2,064 of them. The 90 functions
this scan attributed are `Audio`-owned, so **the figure was fixed before the scan ran**. It is not a
finding about the scan; it is a fact about how V120 tagged audio code. **A metric that returns its
value by construction is not a measurement** — this is a clean instance.

### `all 208 land in Audio-owned functions` — real discriminating power

The same document's control is the opposite case, and it is **the strongest result here**:

| | |
|---|---:|
| `Audio` share of the binary | **5.41 %** (2,064 of 38,161) |
| references a scattering scan would put in `Audio` | **~11 of 208** |
| **observed** | **208 of 208** |

**The null is 11 and the observation is 208.** The concentration cannot be produced by a faulty
scan, by folded code, or by chance. Unlike the naming figure, this one **could easily have come out
otherwise** — which is exactly what makes it evidence.

### The distinction worth carrying

Both rows read "100 %". One is guaranteed by the population and one is 19x its null. **The percentage
is the same and the evidential content is completely different**, and nothing on the face of either
number says which is which — only the base rate does.


## 13. The library boundary — which functions are SEAD, and what is linked beside it (2026-09-13, FABLE)

> **1,216 functions are declared as the SEAD library** (1,207 in the span, 9 just past it) (EC-7 letter C, frontmatter
> `function_families`). The `Audio` tag that grouped 2,020 undispositioned functions was a *topic*,
> not a provenance: it spans **four upstream codebases and FFXII's own audio layer**, and only an
> address-and-evidence boundary separates them.

### What the `Audio` tag actually covers

| Address range | What it is | Evidence | Disposition |
|---|---|---|---|
| `00121000` up to `00125740` (exclusive) | **CRI HCA decoder** (CRI Middleware) | `00121DB0` references `Copyright (c) 2009-2010 CRI Middleware Co., Ltd.` at `01CBA610`; `00123140` / `00123250` / `001234A0` read the tables that follow it; SEAD's `Voice::Initialize` `007EBAD0` and the voice code `007EAA60` / `007ED580` / `007DC730`–`007DD040` are its callers. `007ED580` interior read 2026-09-17 (SWE2-FRONTIER): 1,182 B — `001221E0` first at [`007ED617`](../_index/ADDRESS-INDEX.md), carries `"HCADecoder_IsDataEmpty error !! %d"`/`"HCADecoder_IsEndOfDecodeRegion error !! %d"`, `007A5570`/`0019C5D0` ×4 — the decode-loop's status-check member | ~~not yet declared~~ **C, 53 members** (`00121000` up to `00125740` (exclusive) less the folded `001243B0`, [inventory](../23-Third-Party-Libraries/third-party-middleware-inventory.md)) |
| `002106E0`–`00212xxx` (and scattered `0022xxxx`) | **FFXII's audio layer** — `AudioCallback` (derives `SQEX::Sd::Driver::SeadCallback`), `AudioFileLoadManager`, `AudioController` / `MusicAudioController` / `SebAudioController` / `SepAudioController` | unnamespaced RTTI; EASTL containers; these are the callers of SEAD's API (e.g. `002110C0` scales a 0–127 volume to float and calls `007A4380` / `007A4C40` / `007A47A0` / `007A46F0`) | **architectural** — game code, stays in the frontier |
| **`007A4380` up to `007F41A0` (exclusive)** | **SEAD** (`SQEX::Sd`) | 481 members sit at `SQEX::Sd` vtable slots, the `[sead]` diagnostics of §2 land here, controls below | **C, 1,207 members** (+ 9 past the span, below) |
| `007B9D70`–`007BA970` (inside the span) | **libogg 1.3 `framing.c`** | body-by-body identification on the [middleware inventory](../23-Third-Party-Libraries/third-party-middleware-inventory.md) | **C, 22 members** (own row) |
| `007F41A0`–≈`007FF1C0` | **Tremor** — `vorbisfile.c` first, then the decoder | `007F41A0` is self-recursive and drives libogg (`_bisect_forward_serialno`); `007F7FF0` / `007F8140` compare the `vorbis` signature at `01CEBB50`; the classifier's four `ThirdParty.Audio.Tremor.*` bodies sit at `007FB180`–`007FF1C0`; allocation through the `_ogg_` hooks | ~~not yet declared~~ **C, 106 members** (`007F41A0` up to `007F6FB0` (exclusive) and `007F7680` up to `007FFBC0` (exclusive), [inventory](../23-Third-Party-Libraries/third-party-middleware-inventory.md)); the 14 entries between are SEAD objects and an MS ADPCM decoder |

**`007FF1C0` (2,553 B) read to interior anchors, 2026-09-17 (SWE2-FRONTIER).** The band's last
member and one of the three decoder-core bodies the CF-2 reachability result names. Its shape is
fixed-point, table-driven decode work: entry scans a flag bitmask — `test cl,0x40` at `007FF1F6`
then a `rol eax,6` / `test ebp,eax` loop at `007FF200`–`007FF20A` that walks set bits and derives
`0xD − count` (`007FF20C`–`007FF215`); the middle consults the `.rdata` qword constant tables at
`01CC4810` (`007FF218`, `007FF3DA`, `007FF5A1`) and `01CC5820` (`007FF5B1`, `007FF731`, `007FF908`
— Tremor's packed fixed-point lookups, e.g. `7FFFFD88001921FB`); it calls decoder-core siblings
`007FE530` (`007FF561`) and `007FE0F0` (`007FF576`; interior read 2026-09-17, SWE2-FRONTIER:
1,077 B, call-free — an eight-register-save leaf in the floor/codebook decode path,
packed-index arithmetic at [`007FE154`](../_index/ADDRESS-INDEX.md)); and the tail (`007FFB80`–`007FFBA6`) is a
descending 0x10-stride store loop copying `[r14-0x10]` pairs into `[rcx+8]`/`[rcx+0xC]` — the
sorted-post-list build of a floor/codebook decode pass rather than a vorbisfile API. Which exact
Tremor routine is naming-grade semantic adjudication (queued); the member-TSV and call targets
place it inside the band either way.

### The edges

- **Lower edge `007A4380`.** The preceding object is the PhyreEngine framework: `PApplication`,
  `PInputDevice*` and `VTS::ScreenState*` RTTI up to `007A4150`, `PhyreFrameworkApplicationUpdateThread`
  at `007A4250`, a platform helper at `007A4310`. `007A4380` opens SEAD's handle API: `007A4390` /
  `007A45C0` allocate a command (`007AB460`), stamp a type (2, 3), fill it and commit it (`007AB550`);
  the first `SQEX::Sd::ConfigFile` vtable bodies follow at `007A47D0`, and `007A4D50` prints
  `[sead][info]%s version %X.%X.%X.%X`.
- **Upper edge `007F41A0`.** The last `[sead]` emitter is `007F3950` (music timing — interior read 2026-09-17, SWE2-FRONTIER: 1,165 B, `"Can't find original meter index:%d"`/`"Invalid meter index:%d"`, `007D0400` ×4 first at [`007F39C6`](../_index/ADDRESS-INDEX.md)); `007F3DE0`–`007F40B0`
  carry no string but are SEAD by their calls (callers `007C36C0` / `007E7A90` / `007E8410`, callee
  `007A9E50`). `007F41A0` is the first `vorbisfile` body.
- ~~**SEAD entries outside the span, not declared:**~~ **SEAD entries past the span — declared 2026-09-13 on OPUS-REQ-FABLE-TREMOR-RESIDUE (9):** the vtable installers `007F7360` (vtable `01CBAB68`, whose first slot
  is the `SoundObject` method `007F7390`) and `007F7380` (vtable `01CB9888`, whose first slot is `SQEX::Sd::SeadObject<3,16>`'s `007EF160`), the `SQEX::Sd::Lay::SoundObject` vtable bodies `007F7390` / `007F73D0` / `007F7400` / `007F7420`, and the SSE geometry helpers `007F7440` / `007F74E0` / `007F7570`, whose only callers are the
  `SQEX::Sd::Lay::PolygonSound` methods `007F20E0` / `007F25E0` (`007F20E0` interior read 2026-09-17, SWE2-FRONTIER: 1,032 B — `007BB610` first at [`007F2149`](../_index/ADDRESS-INDEX.md), `007F7570`/`007F0320` — the polygon-voice update member). **Still not declared:** the Microsoft ADPCM block decoder `007F6FB0` and its samples-per-block helper `007F7350` — library code SEAD's voice path calls, but whose upstream is not established — and SEAD's static initialisers and teardowns in the `0016xxxx` / `008B8xxx`
  thunk zones.

### Excluded from the row (stay in the frontier)

| Entries | Why |
|---|---|
| `007A5AA0` | RTTI class `SoundObjectManagerCallbackHandler` is **outside** `SQEX::Sd` (it shares the folded body `007A5AC0` with `SQEX::Sd::Lay::SoundObjectManagerCallback`, so it is most likely that interface's implementation). Its position says SEAD; its namespace does not — not decided by position alone |
| `007A5AC0`, `007AD440`, `007B6C40`, `007BD590`, `007E3260` | ICF-folded bodies whose vtable appearances include classes outside `SQEX::Sd` (`007B6C40` is shared with `mkvparser`) — one body, several owners |
| 18 A-measured, 6 in OPUS's *internal tail-call forwarders* family | already dispositioned elsewhere; the checker refuses a function in two families |
| the 22 libogg entries | their own row |

### Controls — instruments that could have found game code inside the span

Both are printed by `members/select_audio_libraries.py`.

1. **Outbound calls.** Every `E8`/`E9` from a span body to an entry outside the span: **53 distinct
   targets**, and every one is library or runtime — the security cookie `00808C40` (236 callers),
   `__report_rangecheckfailure` `00809728`, `free` `00809950`, the CRT imports at `00861xxx` (`memcpy`,
   `memset`, `strcmp`, `pow`, `exp`, `log`, `log10`, `atan2`), `__local_stdio_printf_options`
   `0016D670`, `_guard_check_icall` `0016D6A0`, the `vsnprintf` wrapper `0019C5D0`, the 5- and 11-byte
   CRT thunks `00210EB0` (→ `free`) and `00210EC0` (→ `0085E730`), the ICF-folded `ret 0` body `001243B0`,
   the CRI HCA decoder (`00121000`–`001242F0`), and the Xiph / SEAD code just past the upper edge
   (`007F5850`–`007F7570`). **No call from the span reaches FFXII game code.**
2. **Shared globals.** Every `.data` location referenced rip-relatively (capstone-exact) from inside
   the span *and* from outside it, security cookie removed: **120**. The outside referencers are
   **only** the static-lifetime thunk zones (`0016xxxx` alone 22, `008B8xxx` alone 18, both 76) and
   `007Fxxxx` (4 — the `_ogg_` allocator hooks `01F41CF8` / `01F41D00` / `01F41D08` / `01F41D10`, which
   `007A4D50` writes and libogg / Tremor call through). **No global is shared with FFXII's audio layer
   or any other game code.**

**Positive control.** The same evidence did find foreign code where it exists: the hook users
exposed the libogg object *inside* the span (and Tremor outside it), and the outbound scan exposed the
CRI HCA dependency. The instruments are not blind to non-SEAD code.

**Limitation, stated rather than hidden.** A third-party C object that neither allocates through the
hooks nor carries a provenance constant would not be separated from SEAD by these scans. It would still
be linked library code, not FFXII code — which is what the letter C asserts — but its upstream name on
this row would be wrong. The row's upstream claim is exactly as strong as the two controls.

**What this does not establish:** the behaviour of any of the 1,216 bodies. A C disposition says
*whose code this is and where it ends*, not what it does; §7's open items are unchanged.

## The `007EAA60` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`007EAA60` (~926 B) — a large SEH-style frame: `r11 = rsp`, `rbp =
r11-0x168`, `rsp -= 0x258` (`007EAA60`/`007EAA66`/`007EAA6D`), saving
`rbp`/`r14` before the body.

| member | role | interior |
| --- | --- | --- |
| `007F6FB0` | body | [`007F6FB0`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## SWE2-EC7-33 update (2026-09-19) - `007F41A0`

`007F41A0` (**1,314 B** — *corrected 2026-09-19 (SWE2-EC7); this line printed 1,135 B, a wrong literal in the batch-33 append — the body is 1,314 B per the function list*) is Tremor `vorbisfile`'s `_bisect_forward_serialno` driver - self-recursive bisection with `007BA0D0`/`007F4DF0`/`007BA270`/`007BA230`/`007B9F70`/`007F8EE0`/`007BA970`/`007BA950`, exactly the libogg-driving body the span boundary names. Interior anchor `007F4269` (a `007F5020` call).

## SWE2-EC7-34 update (2026-09-19) - `007F6FB0`

`007F6FB0` (926 B) is a Tremor init/lookup body - the `0xE6000000E6` pair magic, `01CEBCE0`/`01CBAAE0` `movdqa` tables, `00808C40`, `007F7331`/`007F7292` internal arms. Interior anchor `007F7338` (the `00808C40` call).

## 25 more functions the assert strings name (2026-09-19, OPUS)

*The image carries **38** strings of the form `[sead][!!error!!]Class::Method`. This page already
identifies functions from other evidence and carries 21 distinct `Class::Method` names, mostly
`Sound::`, `SQEX::`, `Sd::` and `Driver::` — a different set. The assert strings reach classes this
page does not mention at all: `Music` (21 methods against the 2 named here), `IAudioClient`,
`AudioDevice`, `CoreSourceVoice`, `OnMemoryBank`, `StreamingBank`, `AudioStream`,
`MaterialVorbisExtraData`, `Category`.*

**The method is simple and the discrimination is the whole of it.** A `sead` assert string is
referenced from the function that asserts, so a function referencing **exactly one** such name is
that method. A function referencing **several** is a CALLER of them. That distinction is not
cosmetic: `007DE2F0` references five — `IAudioClient::GetBufferSize`, `::GetDevicePeriod`,
`::GetMixFormat`, `::Initialize`, `::IsFormatSupported` — and is therefore the code that *calls* the
WASAPI `IAudioClient` interface and asserts on each result, **not** any one of those methods. It is
excluded.

**Twenty-five functions reference exactly one name, and every one of them is currently `FUN_*`:**

| function | the assert names it | | function | the assert names it |
|---|---|---|---|---|
| `007AA320` | `Category::InitializeRefCategory` | | `007C92F0` | `Music::SetMode` |
| `007B93E0` | `ExternalSourceVoice::QueueBuffer` | | `007C9C20` | `Music::SetNextMusic` |
| `007C1830` | `Music::CalcSampleDelay` | | `007CA7C0` | `Music::Start` |
| `007C2A60` | `Music::CheckTransitionTime` | | `007CAB80` | `Music::SyncTo` |
| `007C30C0` | `Music::CheckVersion` | | `007CAF70` | `Music::TryLoad` |
| `007C4030` | `Music::ReverbEnd` | | `007CC880` | `Music::UpdateNonLoopVoiceReplay` |
| `007C4790` | `Music::CoreSetNextSection` | | `007CCDD0` | `Music::UpdateRemainingLoopCount` |
| `007C5760` | `Music::End` | | `007CDC20` | `Music::UpdateTransition` |
| `007C6490` | `Music::GetPlaySec` | | `007DD9F0` | `AudioDevice::SetEventHandle` |
| `007E01F0` | `CoreSourceVoice::Render` | | `007E2AD0` | `OnMemoryBank::Initialize` |
| `007E0B60` | `CoreSourceVoice::Render` | | `007E32E0` | `StreamingBank::Initialize` |
| `007E4410` | `AudioStream::MarkAsUnused` | | `007E48D0` | `MaterialVorbisExtraData::GetSeekOffset` |
| `007EBAD0` | `Voice::Initialize` | | | |

**One anomaly, not resolved here:** `CoreSourceVoice::Render` is named by two different functions,
`007E01F0` and `007E0B60`. An overload, a wrapper and its implementation, or two builds of the same
routine — the assert cannot tell which, and naming both identically would assert something the
evidence does not support.

### The `CoreSourceVoice::Render` anomaly narrowed — both are live, and one caller runs both (FABLE, Claude Opus 5, 2026-09-20)

*The assert still cannot tell which; the call graph can rule two of the three readings out.*

**They are not two builds of the same routine, and neither wraps the other.** `007E01F0` (852 B) and `007E0B60`
(6,716 B) are **both called, from the same function**, `007B0000` — `007E0B60` at `007B01D8` and `007B02CD`,
`007E01F0` at `007B0306` — and **neither calls the other** (every direct `call`/`jmp` target of each body
enumerated: 12 and 20 distinct targets, with the other's address in neither set).

**They read disjoint object fields.** Over each body's first sixty instructions, `007E01F0` touches `+0xCA`,
`+0xCC`, `+0xB8`, `+0xC8`, `+0xC0`; `007E0B60` touches `+0x80`, `+0x88`, `+0x94`, `+0x98`, `+0xA0`, `+0xB0`,
`+0x108`, `+0x210`. Only `+0x30` is common — and that is the buffer pointer the shared mixer below reads. **So
they are two classes' `Render`, not one routine seen twice**, which leaves the overload reading and rules out the
other two.

**The tick's units, and they cross-check.** Four seven-byte accessors read one block of globals that the device
init `007AEF30` fills from the device descriptor (`007AEFDC`–`007AF074`): `007AED00` → `02EAD348` = the
descriptor's `dword[+0]`, `007AECF0` → `02EAD354` = its `dword[+8]`, `007AECE0` → `02EAD34C` = the constant
**8**, and `007AECD0` → `02EAD350` = `dword[+8] << 5`. **The two consumers name them without ambiguity:**
`007E0550`'s mix loop runs `007AECF0()` iterations of `0x20` bytes — two `xmm` rows, eight floats — so `02EAD354`
is the **frame count** and 8 the **channel count**; and `007E01F0` uses `007AECD0()` as a `memset` length and
`007AECE0()` as the length of two per-channel `dword` arrays, so `02EAD350` is the **buffer size in bytes** and
`frames << 5 = frames × 8 channels × 4 bytes` closes the arithmetic. **The engine mixes in eight-channel
interleaved float, a fixed number of frames per tick.** `007AEF30` also installs `007AF740` — `007B0000`'s only
caller — as one of the device's two callbacks, so the pass below runs on the device's clock, not the frame's.

**What `007B0000` is: the driver's per-tick voice pass.** Called once from `007AF740`, it runs **six** walks over
four intrusive lists, under four critical sections:

| order | list head | per node | what runs | locking |
|---:|---|---|---|---|
| 1 | `02EAD358`, two slots | `[slot+8]` | `007DFA50` | inside CS `02EAD1B0` |
| 2 | `02EAD2F0` | `[node+0x20]` | **`007E0040`** — `word[obj + 0xCA] = 0` | inside CS `02EAD188` |
| 3 | `02EAD2C0` | `[node+0x20]` | `dword[voice+0x80] == 4` → **retire**, else **`007E0B60(voice)`** | head read under CS `02EAD138`, **walk unlocked** |
| 4 | `02EAD310` | `[node+0x18]` | the same test, the same **`007E0B60(voice)`** | head read under CS `02EAD160`, **walk unlocked** |
| 5 | `02EAD2F0` again | `[node+0x20]` | **`007E01F0(obj)`** | inside CS `02EAD188` |
| 6 | `02EAD358`, two slots | `[slot+8]` | `007DFBB0` | inside CS `02EAD1B0` |

**The two render walks are the only unlocked ones, and that is deliberate.** Walks 3 and 4 take the lock just long
enough to read the list head (`007B00AE`–`007B00C2`, `007B01F7`–`007B020B`), release it, and then render outside
it — re-taking the same lock only when a voice has to be unlinked (`007B00E2`, `007B0239`). *The expensive work is
done off the lock; only list surgery is inside it.* Walks 1, 2, 5 and 6 are short and stay locked throughout.

**`dword[voice + 0x80] == 4` is the retire state.** A voice in it is unlinked from its list (`+8` previous, `+0x10`
next, `+0x1C` bit 0 "has next"), released back to the `0x28`-stride slot array at `02EAD2B0` by the index at
`[node+0x18]` — bounds-checked against `02EAD2A8` — its deleting destructor is called through **slot 0** with `(node, 1)` and the
list counter (`02EAD2AC` or `02EAD308`) is decremented. **Retirement therefore happens in the same walk as
rendering, before the voice would have been rendered.**

**And the order of the walks is the whole point: `007E0040` and `007E01F0` bracket the renders.** A
whole-region sweep of the offset finds every access to `+0xCA` in `007A0000`–`00800000`: `007E0040` zeroes it,
`007E01F0` reads it, `007DFF20` clears it with `+0xCC` in one `dword` store at construction, and **`007E0550`
both reads and writes it**:

```asm
007E0550(dest, src, gain):
    007E0568  call 007AECF0             ; eax = the frame count
    007E056D  movzx r8d, word [dest + 0xCA]
    007E0578  mov   r9, [dest + 0x30]   ; the destination buffer
    007E0583  test  r8w, r8w / jg       ; already written this tick?
      n == 0:  dst[i]  = src[i] * gain  ; mulps, movaps            (007E05A0-007E05BF)
      n >  0:  dst[i] += src[i] * gain  ; mulps, addps, movaps     (007E05D0-007E05F5)
    007E05FC  inc r8w                   ; ... and the count advances
```

**So `word[+0xCA]` counts how many sources have mixed into that destination this tick, and zero means "overwrite
rather than add".** Walk 2 resets it on every `02EAD2F0` object, walks 3 and 4 render voices that accumulate
through `007E0550`, and walk 5 reads the counter back. `007E0550` is called by **both** `007E01F0` and `007E0B60`,
which is why the two share `+0x30`.

**And `007E01F0`, read whole (852 B), is the destination's end-of-tick pass.** It is the reason the counter
exists:

1. **it publishes the count** — `word[obj + 0xCC] = word[obj + 0xCA]` (`007E0214`–`007E0222`), so `+0xCC` is
   last tick's writer count and `+0xCA` the one being accumulated;
2. **if nothing wrote** (`word[+0xCC] <= 0`) it **`memset`s the output buffer `[obj + 0x30]` to zero**
   (`007E0249`–`007E0252`) and then, under the object's **own** lock at `obj + 8`, zeroes the per-channel arrays at
   `[obj + 0xB8]` and `[obj + 0xC0]` and clears `byte[obj + 0xC8]`. *A destination nobody mixed into outputs
   silence, not last tick's samples — that is what the counter buys;*
3. **it runs an effect chain.** `dword[obj + 0xB0]` entries from `obj + 0x90`, each polymorphic: **slot 1**
   non-zero **skips** the entry; on a silent tick an entry additionally has to answer **slot 2** non-zero to run
   at all; otherwise **slot 3** processes the buffer in place, taking `{buffer, frames}` (`007E0363`–`007E0391`).
   *So an effect is bypassed on a silent bus unless it says it still produces output* — the rule a reverb tail
   needs;
4. **and it dispatches the result.** If anything wrote or an effect produced output, it walks `dword[obj + 0x88]`
   destinations from `obj + 0x38`, branching on each one's **slot 1** kind — 1 and 2 are handled and **any other
   value formats a `[sea…` diagnostic through `0019C5D0`**, which is the same assert machinery this page is built
   from.

So the destination object's shape is: buffer `+0x30`, own lock `+8`, destination list `+0x38` with count `+0x88`,
effect list `+0x90` with count `+0xB0`, channel arrays `+0xB8` and `+0xC0`, a flag `+0xC8`, and the writer counter
pair `+0xCA` / `+0xCC`. **`007E01F0` never mixes; it finishes.** That is a different job from `007E0B60`, which is
called per voice and feeds `007E0550`.

**What this does not settle:** which class each `Render` belongs to, and therefore whether the assert's name is
right for both; the bodies of `007E01F0` and `007E0B60` beyond their opening field reads; what `007AECF0` returns;
what `+0xCC` carries beside the counter. *The three readings the paragraph above offered are now two ruled out and
one standing, which is as far as the call graph can take it — a vtable that installs one of them as slot `Render`
of a named class would finish it.*

### The tick is two symmetric halves, and the anomaly is one shape at two levels (FABLE, Claude Opus 5, 2026-09-20)

*`007E0B60`'s gates and tail, and the two walks left unnamed above.*

**`007E0B60` is a source render.** It refuses twice — `dword[voice + 0x80] != 3` (3 is playing, 4 the retire state
above) and a count at `+0xB0` that must be positive — and then forms its **resampling step**: the voice's own rate
`dword[+0x94]` over the device rate `007AED00()`, exactly `1.0` when they match, multiplied by the pitch
`float[+0x108]`. **A step of zero or less makes it `memset` its own buffer `[voice + 0x210]` and return**
(`007E0C1F`–`007E0C32`) — a stopped voice outputs silence rather than stale samples, the same discipline the
destination's counter enforces one level up.

**Its tail mirrors `007E01F0` field for field.** It zero-fills the unwritten tail of `[+0x210]`, then under a lock
runs **its own** effect chain — `dword[+0x290]` entries from `+0x270`, the same slot-1-skips / slot-3-processes
protocol, the same `{buffer, frames}` pair — and then walks its **sends**: `dword[+0x268]` records of `0x10` bytes
from `+0x218`, each holding a destination pointer and a **`float` gain at `+8`**.

**The destination's own kind picks the mixer, and there are two mixers:**

| the destination's slot 1 returns | mixer | its counter | its buffer |
|---|---|---|---|
| 1 | `007DFE30` (194 B) | `word[dest + 0x72]` | `[dest + 0x30]` |
| 2 | `007E0550` (197 B) | `word[dest + 0xCA]` | `[dest + 0x30]` |
| anything else | a `[sea…` diagnostic built by `0019C5D0` and reported through `007A5570(2, msg)` | | |

**`007DFE30` and `007E0550` are the same routine at two offsets** — same `007AECF0()` frame count, same `0x20`-byte
stride of two `xmm` rows, same *overwrite when the counter is zero, add when it is not*, same increment. Only the
counter's offset differs.

**Which makes the six walks two nested halves.** Walks 1 and 6 — `007DFA50` and `007DFBB0` — are the `+0x72`
class's reset and finish, and they are the `+0xCA` class's `007E0040` and `007E01F0` at the other offsets:
`007DFA50` is `xor eax, eax ; mov word [rcx + 0x72], ax ; ret`, and `007DFBB0` opens by publishing
`word[+0x72]` into `+0x74`, fetching the channel count, `memset`ting `[+0x30]` when nothing wrote, and taking the
object's own lock at `+8`.

| class | reset | rendered by | finish | mixer | counter |
|---|---|---|---|---|---|
| `+0x72` | `007DFA50` — walk 1 | its sources' sends | `007DFBB0` — walk 6 | `007DFE30` | `+0x72` → `+0x74` |
| `+0xCA` | `007E0040` — walk 2 | walks 3 and 4 | `007E01F0` — walk 5 | `007E0550` | `+0xCA` → `+0xCC` |

**So the walk order is nested, not arbitrary: reset the outer class, reset the inner, render the voices, finish the
inner, finish the outer.** What feeds the outer is the inner's own send walk — `007E01F0`'s `+0x38` list, whose
entries are dispatched by the same slot-1 kind and would reach `007DFE30` for a kind-1 destination.

**What this adds to the anomaly.** The two asserted `Render`s are a **source** render and an **inner destination's**
finish, and there is a third of the same shape, `007DFBB0`, for the outer. ~~*One name fits all of them in the source
because they are one protocol at two or three levels of a mix graph* — which is also why none of them should take
the name here on its own.~~

### The anomaly is answered: one of the two is right and the other inherited the string (FABLE, Claude Opus 5, 2026-09-20)

*The class hierarchy settles it, and the evidence is this page's own kind — vtables, not asserts.* Three
complete-object locators cover these bodies, and **each destination class's vtable slot 2 is a getter for exactly
the counter its half of the tick uses**:

| vtable | class | slot 2 | the counter it returns |
|---|---|---|---|
| `01CB8360` | `SQEX::Sd::Driver::Core::CoreSourceVoice` (17 slots) | — | slot 9 is `007E0A40`, the buffer enqueue |
| `01CB82D0` | `SQEX::Sd::Driver::Core::CoreSubmixVoice` (7 slots) | `007E0050` | `word[+0xCC]` — **the `+0xCA` class** |
| `01CB8290` | `SQEX::Sd::Driver::Core::CoreMasterVoice` (7 slots) | `007DFA60` | `word[+0x74]` — **the `+0x72` class** |

An independent cross-check that does not use the counters: `CoreSubmixVoice`'s slot 5, `007E0100`, bounds an index
against `dword[+0x88]`, which is the send count this page reads on the same object at `+0x38` / `+0x88`.

**And the mechanical cause is measurable, not inferred.** `CoreSourceVoice::Render` occurs **exactly once in the
image** — one string at `01CB8310`, `[sead][!!error!!]CoreSourceVoice::Render unknown type rendermix!!! %d` — and
a RIP sweep of it finds **two** referencing sites: `007E03EC` inside `007E01F0` and `007E2492` inside `007E0B60`.
*It is one string object with two referencing functions, not two strings.* Its text is the **else arm of the
send-kind dispatch** that both bodies run: when a destination's slot 1 returns neither 1 nor 2, each formats this
message with the kind as `%d`. So the middleware's own source carries the same diagnostic line in a
`CoreSubmixVoice` method as in `CoreSourceVoice::Render`, and the linker merged the literal. **That is the
exception this census's "37 strings referenced by exactly one function" leaves room for**, and it is why the rule
"a string proves which method asserts" needs the qualifier *when only one function references it*.

**Therefore `007E0B60` is `CoreSourceVoice::Render` and the assert is right about it; `007E01F0` is a
`CoreSubmixVoice` method that carries the source voice's assert string.** The third of the same shape,
`007DFBB0`, is `CoreMasterVoice`'s. *So the anomaly is not an overload after all — it is one assert string reused
across a class boundary in the middleware's own source, and applying `CoreSourceVoice::Render` to `007E01F0` would
record the wrong class.* **Still not applied as names**, per this page's rule; this is the evidence for whoever
does apply them, and it says the collision must be resolved in favour of `007E0B60`.

The mix graph these three form, and what `007E0A40` validates when a buffer is queued, are in
[the driver architecture](sqex-sd-sound-driver-architecture.md) §2c.

**Its front half is read too, on the architecture page.** `007E0B60`'s gates, its sample-accurate start offset,
its marker callback, its per-tick gain ramp and the record fields it touches are in
[the driver architecture](sqex-sd-sound-driver-architecture.md) §2a, which also records that this subsystem's
"no body evidence exists" is superseded for the mix path.

**Not read here:** the two decode kernels `007E0B60` switches between on `dword[+0x90]` — most of its 6,716 bytes,
with only ten outward calls; `007DFBB0` past its opening; what distinguishes the `+0x72` and `+0xCA` classes
beyond their layouts; where a source's sends are filled in.

**NOT APPLIED AS NAMES.** This is evidence handed to the page that owns audio function identity, not
a rename. An assert string proves which method asserts, and that is a strong claim; whether each
becomes the function's recorded name is this page's call, and two of the twenty-five would collide
if applied mechanically.

*Static evidence: every `[sead][!!error!!]` string in the image, resolved to its VA, matched against
every RIP-relative operand in all listed bodies. 38 strings, 37 referenced by exactly one function,
26 distinct referencing functions — 25 with a single name and `007DE2F0` with five.*

## SWE2-EC7-78 update (2026-09-20) - `007F7350` ratio-to-offset helper measured

`007F7350` (15 B) is the three-instruction arithmetic helper the sead
callers use: `eax = (2*ecx) / edx` (unsigned divide), then `-0xC` -
a doubled-count-to-offset conversion with a fixed 12 bias.
Interior anchor `007F7358` (the `div r8d`).

## SWE2-EC7-113 update (2026-09-21) - `007A4250` / `007A42E0` measured

`007A4250` (118 B) is the
`PhyreFrameworkApplication
UpdateThread` spawner
`0079F150` runs - the body
this page's lower edge names
by its string: `005CC8C0`
builds the thread descriptor
on the stack
(`+0x28 = 0x100000` stack
size, `+0x38 = 1`, `+0x40`
the name), `0016D6A0` runs,
`005CD1E0` creates the
thread on `rdi + 0x30`, and
`byte[+0x48] = 1`,
`byte[+0x28] = 0`,
`dword[+0x50] = 1` latch the
owner's state - the
framework's update thread
living on the application
object's `+0x30` block.
Interior anchor `007A42AE`
(the `005CD1E0` create
call).

`007A42E0` (48 B) is the
matching teardown
`0079EDD0` runs on the same
`+0x30` block:
`dword[+0x50]` zeroes,
`005CD330` and `005C5230`
run on the block with a
stack local, and
`byte[+0x18]` clears - the
destroy half of the pair.
Interior anchor `007A4306`
(the `+0x18` clear).
The callers' own fan-out is
mechanical and recorded
here: `0079EDD0` and
`0079F150` reach the Input
domain, and `005CC8C0` /
`005CD1E0` answer Resource-
domain callers - shared-
service edges, not SEAD
subjects.

## SWE2-EC7-114 update (2026-09-21) - `007A12B0` / `007A0180` measured

`007A12B0` (104 B) is the
drain `0079EDD0` runs before
the update-thread teardown:
`005CD6D0` first, then
`006B64C0(qword[+0x40],
+0x48)` retries with
`005CCB80(1)` sleeps until
the `+0x40`/`+0x48` pair
agrees or the call succeeds,
and `+0x28`/`+0x30`/`+0x38`/
`+0x40`/`+0x48` all zero -
the queue-empty wait that
`007A42E0`'s destroy
depends on.
Interior anchor `007A12EF`
(the retry call).

`007A0180` (363 B) is the
developer-console command
table `00792760` and
`0079F150` run: seventeen
`007A0090` registrations
bind handler bodies to the
names `"Frames"`,
`"Timestep"`, `"Framerate"`,
`"MinFramerate"`,
`"RenderFrame"`, `"Keypress"`,
`"KeyDown"`, `"KeyUp"`,
`"Buttonpress"`,
`"ButtonDown"`, `"ButtonUp"`,
`"Mousepress"`,
`"InputSource"`, `"Expect"`,
`"Echo"` and `"Quit"` - the
framework's built-in console
vocabulary, each handler a
`.text` body in the
`00795xxx`..`00798xxx` band
(`005C5230` twice as a
no-op slot).
Interior anchor `007A0197`
(the `"Frames"` register).

## SWE2-EC7-115 update (2026-09-21) - `007A0090` / `0079E3D0` / `00799860` / `0079A120` measured

`007A0090` (229 B) is the
registrar `007A0180` calls
seventeen times: a
`+0x30`-count/`+0x34`-capacity
table of `0x50`-stride
records at `+0x28` grows by
doubling (minimum `0x10`)
through `00584740` alloc /
`00861EBA` copy /
`00584730` free; each record
takes the handler pointer at
`+0`, the name via IAT
`008C2F70` (a `0x40`-byte
bounded copy at `+8`), and a
zero flag at `+0x48`.
Interior anchor `007A0150`
(the name-copy call).

`0079E3D0` (195 B) is the
bank populate `0079F150`
runs after `0079A430` and
`0079AF20`: it walks the
`01F401E8` intrusive list
(nodes at `link - 8`) calling
`vtable[+8]` on each, and
files the ones answering 1
into the `+0x118`+`i*8`
seven-slot bank until the
bank or the match count
runs out; `dword[+0x194]`
is set to 1 after. The bank
`007A0B50` copies into and
`0079AE40` consumes.
Interior anchor `0079E436`
(the `vtable[+8]` call).

`00799860` (115 B) is the
`01F401E8` list drain
`0079EDD0` runs on teardown:
each node unlinks itself
(the `+8`/`+0x10` pointer
fixup), self-links, and gets
`vtable[+0]` invoked; the
loop re-reads the head until
the sentinel, then tails
`007998E0`.
Interior anchor `007998C0`
(the destroy call).

`0079A120` (771 B) is the
`INPUT` console command -
the executor for the
`007A0180` table: switch on
`dword[cmd]` gives a
key/button write
(`byte[cmd+8]` bank slot,
`byte[cmd+9]` row minus
`0x1C`, `byte[cmd+0xA]`
stored into `bank+row+0x30`
on the `+0xDF8` object's
`+0x118` table - live input
injection), an
`"INPUT %d"`/`+`/`-`/`IK`
argument parse
(`01CB28EC`..`01CB28F8`),
and a name lookup that
scans the `+0x58` command
table (`0x50` records via
IAT `008C3000`) and calls
the matched handler; the
`+0xDF8` object's list
iterates through `0079CFF0`
/`00873C50`/`00873C40` with
`+0x28`/`+0x2C` row writes,
and a miss prints
`"Couldn't"` (`01CB2920`).
Interior anchor `0079A1D7`
(the name-compare call).

## SWE2-EC7-116 update (2026-09-21) - `0079CFF0` / `007998E0` / `00792760` measured

`0079CFF0` (13 B) is the
two-head accessor
`0079A120` calls on the
`+0xDF8` object: returns
`qword[rcx]` or, when that
is null, `qword[rcx + 8]` -
the list-head fallback the
INPUT command iterates.
Interior anchor `0079CFF8`
(the fallback load).

`007998E0` (145 B) is the
second-stage teardown
`00799860` tails into:
`vtable[+8]` releases
`[02EA9508]`,
`vtable[+0x10]` releases
`[02EA5370]` and the cell
is NULLed, then the
`01F401F8` list drains with
the same unlink /
self-link / `vtable[+0]`
destroy loop `00799860`
runs on `01F401E8`.
Interior anchor `0079994A`
(the unlink store).

`00792760` (88 B) is the
constructor `0079F150`
runs for the console
object: `00792690(this,
r8)` base-init,
`+0x28`/`+0x30`/`+0x40`
zeroed, `+0x38` takes the
`rdx` argument, vtable
`01CB24B8` ([0] =
`00793FC0`, RTTI
`01D3E430`) is stamped,
and `007A0180(this)`
registers the seventeen
commands. The object the
`"Frames"`..`"Quit"` table
lives on.
Interior anchor `00792797`
(the vtable load).

## SWE2-EC7-116/117 update (2026-09-21) - `006B64C0` measured

`006B64C0` (45 B) is the
skip-marked drain
`007A12B0` runs before its
`+0x40`/`+0x48` teardown
wait: while `dword[node +
8]` is zero it advances
`[rdx]` past the node, so
marked entries survive the
drain.
Interior anchor `006B64E2`
(the relink store).

## SWE2-EC7-120 update (2026-09-21) - the `0079EDD0` pool helpers measured

`0064AD60` (308 B) is the
pool reconfigure `0079EDD0`
runs: `00671B10` tests and
`00674230` drains
`02D351F0` and `02D35278`,
`00673860` clears
`02D35170`, `00610350`
re-arms `01F2E8E0`, then
each pool's `[+0]*[+4]`
product compares against
its cached `02D35268`/
`02D352F0` cell and a
mismatch re-drains and
re-initializes through
`00671690`; the
`02D34734 >> 7` and
`02D3515C >> 7` bit-0 flags
gate `0062BA00` on
`02D34718`/`02D35140`.
Interior anchor `0064AD6D`
(the first `00671B10`).

`0063E3D0` (62 B) is the
small-vector clear the same
caller uses: when `+0x10`
is nonzero and its bit-31
ownership flag is clear,
`00584730` frees `+0x18`;
both cells zero either way.
Interior anchor `0063E3F2`
(the `00584730` call).

## SWE2-EC7-121 update (2026-09-21) - `0062B5A0` measured

`0062B5A0` (513 B) is the
teardown `0079EDD0` calls:
`[+0x118]`'s
`vtable[+0x50]` release,
the `0065E5D0`/`0065E6C0`/
`005FE200` chain, then
`[+0x110]`'s
`vtable[+0x108]`,
`vtable[+0x370]` and
`vtable[+0x378]`.
`006CAFC0` drains
`+0x18C0`, `0062B290` and
`0062B340` run `+0x7D8`
and `+0xB50`, `0062B890`
drains `+0x480`/`+0x4D0`
when their `+0x18`/`+0x28`
pair is non-empty, and
`0062BA30` runs `+0x9C0`.
The `vtable[+0x10]`
release then runs on
`+0x1840`, `+0x7B8`,
`+0x118`, `+0x110`,
`+0x108`, `+0x1880` and
`+0x1878`, `00618FD0`
frees the `+0x700` run
under its `+0x6F8` count,
`+0x183C` clears bit 7,
and a `02CF2544`-gated
IAT call
`008C2AA0(02CF2540)`
closes the body.
Interior anchor `0062B61A`
(the `006CAFC0` call).

## SWE2-EC7-122 update (2026-09-21) - the `0062B5A0` teardown helpers measured

`006CAFC0` (734 B) is the
`+0x18C0` sub-object's full
drain `0062B5A0` calls:
`0062BA30` empties the four
embedded lists at `+0x6B8`,
`+0x398`, `+0x208` and
`+0x528`, then a straight
`vtable[+0x10]` release-and-
null sweep walks 26 pointer
slots (`+0x98`, `+0x90`,
`+0xA8`, `+0x158`, `+0x180`,
`+0x188`, `+0x178`, `+0xC8`,
`+0xE8`, `+0x110`, `+0x118`,
`+0x120`, `+0x128`, `+0x130`,
`+0x140`, `+0x148`, `+0xD0`,
`+0xD8`, `+0xE0`, `+0x200`,
`+0x138`, `+0xF8`, `+0xF0`,
`+0x150`, `+0x100`, `+0x108`)
and returns 0.
Interior anchor `006CB00E`
(the first `vtable[+0x10]`
call).

The four sibling drains
`0062B5A0` calls on the
other sub-objects:
`0062B4E0` (185 B) releases
`+0x760`'s six slots in
three 2-iteration loops
(`+0x38`/`+0x40`, `+0x48`/
`+0x50`, `+0x0`/`+0x10`);
`0062B430` (169 B) frees
`+0x708`'s four buffers
with `00584730` (`+0x28`/
`+0x38`/`+0x30`/`+0x40`)
then releases `+0x0` and
`+0x10`; `0062B340` (233 B)
releases `+0xB50`'s eight
0x190-stride records at
`+0x1C0` (four pointers
each: `-8`/`+0`/`+0x10`/`+8`),
then `+8`, then eight slots
at `+0x10`, then `[r14]`;
`0062B290` (168 B) runs
`0062BA30` on `+0x7D8`'s
`+0x58` list then releases
seven slots (`+0x0`/`+0x10`/
`+0x20`/`+0x28`/`+0x30`/
`+0x38`/`+0x18`).
Interior anchor `0062B51B`
(`0062B4E0`'s first
release); interior anchor
`0062B469` (`0062B430`'s
first `00584730` free);
interior anchor `0062B37C`
(`0062B340`'s record-loop
release); interior anchor
`0062B2B3` (`0062B290`'s
first release).

## SWE2-EC7-124 update (2026-09-21) - `006176B0` and `00610350` measured

`006176B0` (110 B) is the
alloc-and-copy `00624780`,
`006635F0`, `00681A00`,
`0079F150` share: `0017D260`
allocates `ecx` bytes, then
`esi` bytes are copied
byte-wise from `rdx`;
returns the buffer (0 when
`ecx` is 0).
Interior anchor `006176F0`
(the byte-copy `movzx`).

`00610350` (204 B) is the
four-buffer clear
`0064AD60` runs: for each
of `+0x18`/`+0x50`/`+0xA8`/
`+0xB8` (counts `+0x10`/
`+0x48`/`+0xA0`/`+0xB0`),
when the count is nonzero
and bit-31 clear the buffer
is freed - `00584730` for
three of them, `001B70E0`
for the `+0x50` one - and
both fields zeroed.
Interior anchor `006103A3`
(the `001B70E0` free).

## SWE2-EC7-125 update (2026-09-21) - the static-pool teardown and the heap buffer assign measured

`005FE200` (325 B) is the
pool teardown `00610630` and
`0062B5A0` call: under
`005CD6D0`'s guard on
`02CB8480` it frees the
`02CB8450` buffer through
`005F03A0`, walks the
`02CB8478` record table
(count at `02CB8470` under
`btr 0x1f`, 0x50-stride
records) running
`00625EC0`/`0062B7B0`/
`00616420` per entry, frees
the table through
`00584730`, and zeroes the
counts and pointers.
Interior anchor `005FE30B`
(the `00616420`
per-record call).

`005DE8C0` (139 B) is the
copy-assign for the
`{count|flag, ptr}` pair
`005DEBA0`, `00607340`,
`00663720` and `00681A00`
share: it allocates
`count*8` through `0017D260`,
`001C19A0`-copies the source
run, frees the old heap
pointer with `001C2720` when
the old count's bit 31 says
owned, then stores
`{count & 0x7fffffff,
newptr}` into the pair.
Zero count leaves the
pointer null. Interior anchor `005DE8F3` (the
`0017D260` alloc).

## Cross-subsystem neighbours - SWE2-DATA (pass-22 dispositions, 2026-10-02)

- **Application - CLIENT (1 edge).** `00584740` is also called by bodies filed to application: `001A98B0` - shared machinery across the layer boundary, no shared ownership.
- **Input - CLIENT and SERVICE (27 edges).** `00584740`, `0079A430`, `0079AE40` are also called by bodies filed to input: `0079A120`, `0079E3D0`, `007A2440` (+10 more); `0079F150`, `0079E3D0`, `00799860` reach bodies filed to input: `007998E0`, `00796FC0`, `0079A430` (+5 more) - shared machinery across the layer boundary, no shared ownership.
- **Platform - CLIENT and SERVICE (5 edges).** `00584740`, `0065E5D0` are also called by bodies filed to platform: `00650D40`, `006253D0`; `0079F150` reaches bodies filed to platform: `005CC930`, `005CD0A0`, `006253D0` - shared machinery across the layer boundary, no shared ownership.
- **Presentation - CLIENT (4 edges).** `005F03A0`, `00671690`, `00671B10` are also called by bodies filed to presentation/rendering: `001B72B0`, `005FD2A0` - shared machinery across the layer boundary, no shared ownership.
- **Resource - CLIENT and SERVICE (11 edges).** `00584740`, `005CD6D0`, `005CC8C0` are also called by bodies filed to resource: `001DAAC0`, `001A11B0`, `001DAD60` (+3 more); `00792690` reaches bodies filed to resource: `00597970`, `00598100`, `0059BD80` (+1 more) - shared machinery across the layer boundary, no shared ownership.
