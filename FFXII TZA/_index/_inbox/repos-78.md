# repos-78 — Audio boundary residue (BR-2, BR-4, BR-5)

Session state: parent fresh-imported into `Tools/work/proj_h78` (`GFZ_H78`) and
`Verify-GfzCheckpoint.ps1` passed — ledger `38,161 / 38,003 / 158 / 99.58596 %`, snapshot
`46f02e26…`, residual `c5d4b7f7…`, embedded EXE `73461d08…`. No GFZ state written.
Scratch in `Tools/work/h78/`.

---

## COVERAGE

**New document** — `18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md`,
status `DOCUMENTED`, all eight sections, evidence tier 1.
*How a sound request becomes a voice — the play call, the two dials, and the bank split.*

**Edited** — `18-Audio/Audio-Boundary/what-the-engine-calls-to-make-a-sound.md`.
`reopened_count` 0 → 1. Four corrections applied with a full trail in its §8; two §7 items closed,
one refuted, three restated. It stays `PARTIAL`. Details under AUDIT-LOG below.

Both pass `check_links.py` (894 links, all resolve) and `verify_doc_addresses.py`
(120 entry + 38 data + 2 interior, 0 ghosts, 0 to confirm). The two interior citations are the
instruction addresses `00249C64` / `00249CA4`, quoted in a disassembly listing to prove both
wrappers read the global gate.

`check_coverage.py` currently reports **five** stale categories, not only mine — I did not touch
`COVERAGE.md`:

```
00-Engine-Core-Runtime      claimed 7  actual 9
17-Presentation-Rendering   claimed 5  actual 6
18-Audio                    claimed 6  actual 8     (7 before my document; it was already under by 1)
22-Middleware-PhyreEngine   claimed 7  actual 6     (over-counting)
24-Compiler-And-CRT-Runtime claimed 5  actual 6
totals: claimed 81  actual 86
```

---

## OPEN-QUESTIONS

### Closures

**BR-2 — CLOSED. `0x40` is a pan and `0x7F` is a volume.** The killer observation you named is
exactly what settled it. `002DF220(id, p2, p3)` masks `p3 & 0x7F` and merely truncates `p2` to a
byte; downstream `00224570` hands `p2` to `002256F0` (writes `voice+0x20`, drives the driver's pan)
and `p3` to `002257E0` (writes `voice+0x1C`, drives the volume). `002256B0`, the voice reset, writes
`[+0x1C] = 0x7F` and `[+0x20] = 0x40` — the same two offsets with the same two literals, so the
wrapper family is passing the voice's own defaults back in explicitly.

**Your hypothesis was half right, and the wrong half matters.** The pair is real and the volume's
0–127 range is real. **The pan is 0–255, not 0–127.** `002256F0` branches at `0x80`: `0x00..0x7F`
maps to `offset = p − 0x40` on a `+1.0` axis, `0x80..0xFF` maps to `offset = 0xBF − p` on a `−1.0`
axis. 64 is the *centre of a full range*, not the mid-scale of a 0–127 field. Exact formulas, all
constants resolved from RIP displacements against the authorized EXE:

```c
/* pan    002256F0 */  Sd_SetPanVector(voice+8, offset * 0.0078125 /*1/128*/, ±1.0f, 0.0f,
                                       fadeFrames / 60.0f);
/* volume 002257E0 */  Sd_SetVolume  (voice+8, clamp(v,0,127) / 127.0f,
                                       fadeFrames / 60.0f, -1);
```

`008C5B34 = 0.0078125`, `00906A44 = 127.0`, `008F6D54 = 60.0`, `01CEBBA8 = +1.0`,
`01CEBC9C = −1.0`. `0x7F / 127.0 == 1.0` exactly.

**BR-4 — CLOSED, and the premise behind it is refuted.** `003A1180` and `003A11F0` resolve against
**the same two globals with byte-identical arithmetic**: the bank-slot handle at `02AEF3FC` and the
24-byte-stride slot table at `02AEEDC8`. Both compute

```
globalSoundId = bankSlot * 512 + localIndex
```

and the equality check inside them forces the stored `entry[+0]` to equal the slot index, so the
`512` block size is exact. `0021B5B0` downstream matches `bank[+0x3C] == id / 512` — the precise
inverse — and `00224570` recovers `id & 0x1FF`.

**The only difference is a precondition.** `003A1180` calls `00267330(0)` first and returns `-1` if
it is non-zero; `003A11F0` does not. `00267330(i)` reads the ActorManager slot flag byte at
`02098E20 + i*0x288` and blocks unless `(flags & 0x81) == 0x01`. So the 99-caller entry point will
not even *look a sound up* while the world runtime is down or held.

**So the wrapper family is not explained by two different lookups.** What actually creates it is id
routing: bit 31 selects the backend (`002DEF40` computes `~(id>>31)&1`; `002DF220` hardcodes `0`),
and bit 30 diverts to a two-byte encoding entirely (`003A0E20` → `002DF4D0((id>>8)&0xFF, id&0xFF, …)`).

**BR-5 — extended from 8 bodies to ~45.** Read in full this block: the complete play chain
(`00249C60`, `00249CA0`, `0024A1A0`, `002DF220`, `002DEF40`, `002DF010`, `001DBDB0`, `00210B30`,
`00210AF0`, `00210C00`, `0021B5B0`, `00219EA0`, `00212950`, `00224540`, `00223160`, `00224570`,
`002256F0`, `002257E0`, `002256B0`), both gates and their writers (`003603C0`, `00360110`,
`00360370`, `00249FC0`, `00512080`, `002D6F90`), both resolvers plus `003A0E20`, `003A1390`,
`00267330`/`002671F0`/`00267360`, the six class constructors, and the inbound cluster
`002DEB40`/`002DEC00`/`002DECE0`/`002DEDE0`/`002DEE30`/`002DEE50`/`002DEE80`/`002DF050`/`002DF070`/
`002DF0F0`/`002DF370`/`002DF530`/`002DF660`, `00360C20`/`00360D70`/`00361200`/`00361630`,
`003D7F30`, `00221870`, `00212760`, `00221F40`, `00222700`/`00222CF0`/`00223730`/`00224C30`/`002251A0`.

**BR-5's population is 168, not 174 — the overcount was six, not two.** Re-derived from a call graph
I regenerated in this block (`DumpFullCoverageGraph.java` against my own fresh import; it came out
byte-identical to `work/graph_gn`), the census reproduces `174` exactly. **Six** of the seven BR-1
retracted functions are inside it; `002256A0` has no non-Audio caller and was never in the set. All
seven were excluded from every figure I report. Positive control: the instrument returns `00249C60`
at 99 non-Audio / 0 Audio callers and each of `00249CA0`, `002DF220`, `003A1180`, `002DEC00`,
`002DEE50` in the set.

**BR-6 — partially closed.** `0215EF44` is the **current music track handle** (`-1` = none; written
by the `002DEC30`/`002DEC80`/`002DECE0`/`002DED30`/`002DED70`/`002DEDB0`/`002DEDE0`/`002DE360`
family, read by `002DEC00` with 12 non-Audio callers). `0215EF4D` is a **0–127 level** for that
track — three writers set it to the constant `0x7F`, and `002DE350` is its only reader. Also mapped:
`0215EF50` is a 16-entry × 8-byte ref-counted registration table (`+4` key, `0xFFFF` = free; `+6`
refcount; `+1` sticky flag), `0215EFD8` a group bitmask (`002DF370`), `0215EFDC` a sequence counter
(`002DF660`).

**BR-3 — not closed, but sharpened.** `02091098` has, image-wide, **exactly one writer**
(`00249FC0`, 7 B) and three readers (`00249C60`, `00249CA0`, `0024A1A0`). One of `00249FC0`'s three
callers is `00512080`, a `Script_VM_Native_Bridge` that pops an int off the VM value stack straight
into it — **authored event script can open and close the audio gate**. `002D6F90` writes `0`.
Named killer observation for whoever takes it next: decompile `0027F5D0` (1,280 B), the third
caller, and find which game state it derives the value from.

### Proposed new questions

| Proposed id | Question | Owner document |
|---|---|---|
| `PROPOSED-repos78-1` | What does the second audio gate `022CB726` represent? It is read only by `003603C0` (making `002DF220` return `0`) and written by `00360110`→`0`, `003601D0`→`1`, and `00360370` (a block reset that also writes `0x5A` at `022CB724`). Effect proven, cause not. **Killer:** read `003601D0` (389 B) and `00360120`. | `18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md` |
| `PROPOSED-repos78-2` | What does **bit 7** of the ActorManager slot flag byte at `02098E20` mean? It is set and cleared inside `ActorManager_RunFieldRuntimePass` and it blocks audio id resolution. "Held" describes its effect, not a recovered name. Cross-category: this is an ActorEntity fact that Audio depends on. | `18-Audio/…` + an `08-Actor-Entity` document |
| ~~`PROPOSED-repos78-3`~~ | **WITHDRAWN** — this is already **BA-1**. repos-55 supplied the measurement I could not: ~273 `ret`-bodied functions folded onto `0016D6A0`. **Caller-count discrepancy, unreconciled:** they report 2,480; my regenerated graph gives **2,479** distinct caller functions and exactly 2,479 edge rows. Off by one — worth someone finding out which, before the figure gets quoted. My §8 now cites BA-1 and repos-f1's BQ-27 rather than claiming an identity for the address. | — |
| `PROPOSED-repos78-4` | Which audible sounds the small bank-local indices name. 66 of 211 call sites pass immediates (`0x25` ×11, `0x0A` ×7, `0x51` ×7, 28 further values from `0x15` to `0x6C`); 145 compute it. Needs bank data, not code. | `18-Audio/Sound-Selection/…` |
| `PROPOSED-repos78-5` | What geometry `007A7E90` applies to the three floats the pan setter passes. The values and the ±1.0 axis are exact; direction-vector vs stereo-balance vs 2-D position is a claim about a body not yet read. | `18-Audio/sqex-sd-sound-driver-architecture.md` |
| `PROPOSED-repos78-6` | `00223190` (356 B), the stream-side voice start, was not read. Its `00219EA0` path matches the **whole** id against `bank[+0x38]` and requires load-state `2`, so it is a different id space from the `slot*512` one. | `18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md` |

---

## AUDIT-LOG

### Corrections applied to `what-the-engine-calls-to-make-a-sound.md` (reopened_count 0 → 1)

| Was | Is | What proved it |
|---|---|---|
| `00249C60` and `003A1180` shown as nullary — `int id = ResolveSoundId();` | Both take the caller's **bank-local sound index** | `00249C60` never writes `ECX` before `call 0x3A1180`; `003A1180` does `mov ebx,ecx` and adds it to its result. 66 of 211 call sites load an immediate into `ECX` |
| "a volume-and-pan pair in a **0–127** range" (filed as a hypothesis) | pan **0–255**, volume 0–127 | `002DF220` masks the volume `& 0x7F` and only truncates the pan (`movzx r8d,sil`); `00210C00` repeats both; `002256F0` branches at `0x80` |
| "the other **172** functions of the inbound surface" / "**174** (upper bound)" | **168** | six of the seven BR-1 retractions are inside the 174 |
| Two resolvers offered as the reason for the wrapper family | Same globals, same arithmetic; the family comes from the world-live precondition and from id bits 30/31 | complete bodies of `003A1180`, `003A11F0`, `002DEF40`, `003A0E20` |
| "Whether `002DF220` is the only play path" (open) | It is not | `002DEF40`, `002DF010`, `003A0E20`, plus two named battle callers that bypass the wrappers |

Nothing in the prior document was found wrong about the boundary census itself, about
`Boundary.Audio.NativeSupport` being a rejection bucket, or about the three-identical-returns
diagnostic point. Those survived the pass.

### What I tried that failed to break my own findings

- **Attacked the pan/volume identification by looking for a third consumer of either literal.**
  Traced every path out of `002DF220`. `00210C00`'s two branches are the only sinks, both reached by
  tail `jmp`, and both carry the same four values. No third consumer exists on this path.
- **Attacked it by checking whether `002256B0` operates on a different object** than the two setters
  (which would make the "same two fields" corroboration worthless). It does not: within `00224570`
  all three take the same local `lVar9`, and the offsets `+0x1C`/`+0x20` match exactly.
- **Attacked the `512` by looking for a different divisor downstream.** `0021B5B0` uses
  `cdq; and edx,0x1ff; lea edi,[rdx+rax]; sar edi,9` (signed `/512`) and `00224570` uses
  `id & 0x1FF`. Both agree with the resolver's `shl edx,9`.
- **Attacked the "same globals" claim for BR-4** by resolving the RIP displacements in each resolver
  independently rather than trusting Ghidra's shared `DAT_` label: `003A119C+0x274E259` and
  `003A11F7+0x274E205` both land on `02AEF3FC`; `003A11BF+0x274DC01` and `003A1218+0x274DBA8` both
  land on `02AEEDC0`. Same targets, computed separately.
- **Positive control on the census instrument** before believing any population number — it returns
  `00249C60` with 99/0 and every other known member of the set. A regenerated graph from my own
  import came out byte-identical to `work/graph_gn`, so the two derivations are independent in
  provenance and identical in content.
- **Did not manage to break** the claim that a handle is issued when nothing plays. `00212950` is
  called at `0021B5E2`, before the list walk, and `EAX` survives the loop unmodified to both
  no-match exits.

### Self-corrections after repos-55's consistency challenge

repos-55 cross-checked my document against theirs within minutes of it landing and caught a name of
mine that asserted a distinction not present in the body. Both fixes are recorded as superseded
readings in the document's §8.

| Was | Is | Why the first was wrong |
|---|---|---|
| `00249C60` `Audio_RequestSound_Gated` / `00249CA0` `Audio_RequestSound_Ungated` | `Audio_RequestSound_WorldLiveResolve` / `Audio_RequestSound_PlainResolve` | **Both are gated.** `00249C64` and `00249CA4` are both `CMP dword [0x02091098], 0`, and my own whole-image `DumpDataXrefs` run lists exactly three readers of that global with both wrappers among them — I had the refuting evidence in hand and named against it. The real difference is one call deeper, in the resolver |
| `0024A1A0` `Audio_StopRequest_Gated`, "routes to the stop/fade path" | `Audio_GatedRequest_AltDispatch`, route stated, role not claimed | Found by re-auditing my own names after the above. I traced `002DF0F0` → `001DBE90` → `00210C50` but never read `00210C50`; "stop" came from the cleanup context of two of `002DF0F0`'s *other* callers. That is caller inference, which is banned as proof. `00210C50` now sits in §7 as unread |

### Two checker findings — one false positive, one structural

**`check_consistency.py` NAME_PATTERNS[0] reads across a blank line.** The pattern is
`` `ADDR` \s*\|\s*`?NAME`? `` and `\s*` matches newlines, so a markdown table whose last row ends
`| `00224BF0` |` followed by a paragraph beginning with a code span pairs that address with the
paragraph's first identifier. That is where the reported `00224BF0` = `SepAudioBank`
"self-contradiction" in my document came from — my §2 class table and §3 address table agree with
each other on all six constructors. I defused it by rewording the paragraph, but the fix is to stop
`\s*` crossing a blank line; it will fire on any document with that shape.

**A mandatory correction trail always looks like a self-contradiction to a name-per-address
checker.** `00249C60`, `00249CA0` and `0024A1A0` still report two names each — the second is the
superseded name recorded in §8, which `EVIDENCE-STANDARD.md` requires ("never silently rewrite; the
path to a wrong answer is evidence"). As written, the checker penalises exactly the discipline the
standard demands. Suggest excluding text under a `Superseded readings` heading, otherwise the
cheapest way to make it green is to delete the correction record.

### Two instrument findings worth carrying to other blocks

**1. The decompiler silently dropped arguments the machine code passes — twice, on this path.**
`00210C00` decompiles as `FUN_0021b5b0(*(undefined8 *)(param_1 + 8))`: a one-argument call in which
the sound id, pan and volume vanish. The disassembly shows `EDX`, `R8D` and `R9D` all loaded
*before* the branch, so both tail calls carry four arguments. `002DF010` shows three where the
register setup has four. Reading only the C would have produced a confident, wrong statement that
the primary play path discards the sound id. **Every argument claim in my document was taken from
disassembly.** This is your "an argument list is a claim, not a signature" rule firing for real.

**2. `0016D6A0` is a bare `ret` and Ghidra's name for it is actively misleading.** Body is
`C2 00 00`. The PE load config's `GuardCFCheckFunctionPointer` slot (`008C31C0`) does hold this
address — hence `_guard_check_icall` — and `GuardCFFunctionCount` is `0`. But the call sites are not
CFG checks: `00210B30` does `cmp [01FD36A0],rcx; setne cl; call 0016D6A0` and `00219EA0` does
`cmp edx,2; sete r15b; mov ecx,r15d; call 0016D6A0` — the argument is a **comparison result** and no
indirect call follows. That is a retail-stripped `Assert(condition)`. It has **2,479 callers**, so
any document that renders one as `_guard_check_icall(x == 2)` and reads it as a protection is wrong
twice: the call is a no-op and the comparison is never acted on. Likely ICF folding of two functions
that both compiled to `ret` — filed as `PROPOSED-repos78-3` rather than claimed.

### Tooling note — `verify_doc_addresses.py` false positive on float literals

The regex `\b(0[0-9A-Fa-f]{7})\b` matches inside `0.0078125f`, yielding the substring `0078125f`,
which the checker then resolves as an interior `.text` address inside `00781240`. Harmless here (it
lands in the `interior` bucket, not a `GHOST ADDRESS`), and I worked around it by dropping the `f`
suffix — but a document that legitimately needs a float ending in an `f`-suffixed 8-hex-digit run
would report a spurious citation. Worth a word-boundary tweak that rejects a preceding `.`.

---

## CALL-CHAINS / ADDRESS-INDEX

### Owner transitions

```
UI / event script / battle logic
  -> 00249C60(localIndex)                        [OWNER TRANSITION -> Audio]  99 non-Audio callers
     -> gate 02091098                            (non-zero -> 0xFFFFFFFF)
     -> 003A1180(localIndex)                     [resolve]
        -> 00267330(0)   [Audio -> ActorEntity state read, no owner transfer]
        -> 02AEF3FC / 02AEEDC8  ->  slot*512 + localIndex
     -> 002DF220(id, 0x40, 0x7F)                 [tail call]
        -> 003603C0 -> gate 022CB726
        -> 001DBDB0 -> 00210B30 (AudioController 01FD36A0) -> 00210C00   [the fork]
           -> 0021B5B0  sel 0 : bank[+0x3C] == id/512
              -> 00212950                        the receipt, issued unconditionally
              -> 00224540 -> 00224570
                 -> 002256F0(voice, 0x40, 0)     pan    -> 007A7E00 / 007A7E90   [-> SQEX Sd]
                 -> 002257E0(voice, 0x7F, 0)     volume -> 007A81F0              [-> SQEX Sd]
           -> 00219EA0  sel 1 : bank[+0x38] == id, state 2
              -> 00223160 -> 00223190
```

Non-wrapper entrants to the same chain — these bypass `00249C60` entirely and are the reason the
document does not call it a chokepoint:

```
003112F0  BattleFormula_ApplyTargetResult              (CombatFormula)              -> 003A1180 + 002DF220
0030C650  BattleStats_AdvanceLevelToTargetAndRecompute (Rewards_Progression_Economy) -> 003A1180 + 002DF220
00357040  (Script_VM_Native_Bridge)                                                  -> 003A1180 + 002DF220
00271500, 00366870, 003E8690, 0046CC70                                               -> 003A1180 and/or 002DF220
00512080  ScriptVM -> 00249FC0 -> writes the global gate 02091098
```

### Cross-subsystem edges the Audio documents now surface

- **Audio → ActorEntity.** `003A1180` → `00267330` reads the ActorManager slot flag array
  `02098E20` (stride `0x288`), whose writers are `ActorSystem_InitializeManagerRuntime`,
  `ActorManager_RunFieldRuntimePass` and `ActorManager_BindLoadedDefinitionPayload`. **Audio id
  resolution is gated on actor/field runtime state.** Any `08-Actor-Entity` document describing that
  flag byte should reopen to mention it, and vice versa.
- **Audio → Party (shared gate, not an Audio edge).** `00267330` is also called by
  `PartyControl_ApplyAnalogLocomotionToActor` and `PartyFocus_TryGetCurrentActorWorldPosition`. It is
  a hub with 8 callers across 4 owners; its census belongs in an ActorEntity document, and the Audio
  documents disposition it by reference rather than duplicating it.
- **ScriptVM → Audio.** `00512080` → `00249FC0` → `02091098`, and `00357040` → the play chain.
  55 of the 401 inbound edges to the corrected 168-function surface come from
  `Script_VM_Native_Bridge`.
- **CombatFormula / Rewards → Audio.** `003112F0` and `0030C650` call `003A1180` and `002DF220`
  directly.

### Address-index additions

Functions (all verified as function entries by `verify_doc_addresses.py`):
`00249C60` `00249CA0` `0024A1A0` `00249FC0` `00512080` `003A1180` `003A11F0` `003A0E20` `003A1390`
`003A13F0` `00267330` `002671F0` `00267360` `002DF220` `002DEF40` `002DF010` `003603C0` `00360110`
`00360370` `001DBDB0` `00210B30` `00210AF0` `00210C00` `0021B5B0` `00219EA0` `00212950` `00224540`
`00223160` `00224570` `00223190` `002256F0` `002257E0` `002256B0` `00221780` `002226A0` `00222CB0`
`002235F0` `00224BF0` `00225160` `002DEC00` `002DE350` `002DECE0` `002DEDE0` `002DEE30` `002DEE50`
`002DEE80` `002DEB40` `002DF070` `002DF370` `002DF530` `002DF660` `00360C20` `00360D70` `00361200`
`00361630` `003D7F30` `00221F40` `00225580` `00225680` `00225690` `0016D6A0`

Data:
`02091098` (global gate, 1 writer) · `022CB726` / `022CB724` (second gate block) ·
`02AEF3FC` (active bank-slot handle) · `02AEEDC8` (bank-slot table, 24 B/entry) ·
`02098E20` (ActorManager slot flags, stride `0x288`) · `01FD36A0` (AudioController singleton) ·
`01FD36B4` (play-handle counter) · `0215EF44` (music track handle) · `0215EF4D` (music level 0–127) ·
`0215EF50` (16 × 8 B registrations) · `0215EFD8` (group mask) · `0215EFDC` (sequence counter) ·
`022CB9F0` (4 × 24 B track slots) · `02EBBA00` (32 × 132 B ref-counted registrations) ·
`00917290` (`SeSep` magic) · `008F6D54` = 60.0 · `008C5B34` = 1/128 · `00906A44` = 127.0 ·
`01CEBBA8` = +1.0 · `01CEBC9C` = −1.0

### RTTI recovered independently of the GFZ (for B-3)

Recovered straight from the authorized EXE — `.?AV<name>@@` type descriptor → complete-object
locator (signature 1) → vftable — not from GFZ annotations. The kind enum comes from each
subclass constructor's literal argument to the base constructor `00221780(this, kind)`:

| kind | class | type descriptor | COL | vftable | ctor |
|---:|---|---|---|---|---|
| 1 | `MusicAudioBank` | `01F49270` | `01CF0768` | `00907910` | `002226A0` |
| 2 | `SebAudioBank` | `01F49350` | `01CF09E8` | `00907D80` | `002235F0` |
| 4 | `SepAudioBank` | `01F492F8` | `01CF08E8` | `00907B48` | `00222CB0` |
| 6 | `StreamAudioBank` | `01F493D0` | `01CF0B68` | `009081A0` | `00225160` |
| 8 | `ShoutAudioBank` | `01F49378` | `01CF0A68` | `00907F90` | `00224BF0` |
| — | `AudioBank` (base) | `01F49250` | `01CF06F0` | `009078B0` | `00221780` |
| — | `AudioController` | `01F48FF0` | `01CF0108` | `00906CD0` | `00212710` |

The load-bearing consequence: **`MusicAudioBank` is the only subclass that does not write `-1` into
the qword at `+0x38`** — it constructs an `SQEX::Sd::Driver::MusicCallback` sub-object there
instead. Since `+0x38` and `+0x3C` are exactly the two match keys the two lookup paths read, **a
music bank cannot be found by either**, which is why music runs on the separate `0215EFxx` command
block rather than through the play call.

---
---

# Second block — BR-3, BR-6, and a self-caught error in my own document

## OPEN-QUESTIONS

### BR-6 — CLOSED. The `0215EFxx` block is the music command block, and it is now body-proven.

`002DE360` is the initialiser and gives the whole layout with its starting values:

```c
DAT_0215EFD8 = 0;                            /* group mask                                     */
DAT_0215EF4C = 0;  DAT_0215EF48 = 0;
for (i = 0; i < 0x10; i++) {                 /* 16 slots at 0215EF50, 8 bytes each              */
    *(u16 *)(0x0215EF50 + i*8) = 0;          /* flags; byte at +1 is the sticky flag            */
    *(u8  *)(0x0215EF52 + i*8) = i;          /* the slot's own index                           */
    *(u16 *)(0x0215EF54 + i*8) = 0xFFFF;     /* key: 0xFFFF = free                             */
    *(u16 *)(0x0215EF56 + i*8) = 0;          /* refcount                                       */
}
DAT_0215EF4D = 0;                            /* level 0..127                                   */
DAT_0215EF44 = 0xFFFFFFFF;                   /* current track: none                            */
DAT_0215EF4E = 1;
```

This independently confirms the `002DEB40` reading I filed last block (key at `+4` with `0xFFFF`
free, refcount at `+6`) and adds the `+2 = slot index` field I had missed.

**You should upgrade the two conservative names — the `Music_` prefix is no longer an inference.**
`001DBC70` / `001DBCA0`, the forward targets of the whole switch family, go to `00210A40` /
`00210A50`, which dereference singleton slot **`+0x00`**, and slot `+0x00` holds a
`MusicAudioController` by its own RTTI. `0215EF44` is the music current-track handle and `0215EF4D`
is the music level. `Audio_GetCurrentTrackHandle` / `Audio_SetTrackLevelAndForward` are not wrong,
but `Music_` is now carried by a body, not a guess. Your call — the conservative names cost nothing.

### BR-3 — NOT closed. Mechanism proven, player-vocabulary answer not.

I said I would rather hand you this than a plausible label, so: the gate's **cause** is still not
proven, and I am not going to name it.

What is proven. `0027F5D0` is a large UI window message handler (its own message-0 branch tears down
child elements named `s_font_c`, `s_targetline_p`, `s_shape`, `s_mini_face_c`, and it owns window
slots in the `0209AC30` state block). Inside it:

```
sub-state 8   : if (003CA0C0()) sub-state = 0xC       /* 003CA0C0: DAT_02B47748 == 2 && 0032F6C0(3) == 0 */
sub-state 0xC : 003CA1B0(3); sub-state = 9            /* writes DAT_02B47748 = 3                          */
sub-state 10  : 00249FC0(1);  002D66A0(DAT_01E0C2A4)  /* CLOSES the audio gate                            */
message 0xF, window type 0x42 : 002D6F90()            /* teardown; 00249FC0(0) OPENS it, then 003CA0A0()  */
```

So the gate is closed at one specific sub-state of one specific window's state machine and reopened
by that window's teardown, with a separate `DAT_02B47748` state machine (values 2 → 3 → 4) running
alongside. That is a modal screen suppressing the game's own sound requests while it is up.

**Which screen, I cannot say.** Naming it needs whoever creates a window with `+0xD4 == 0x42`, and
`0027F5D0`'s child-element names point at a HUD-like window rather than a menu, which does not
obviously match "suppress all sound". I would rather leave BR-3 open with the mechanism nailed down
than attach a screen name I cannot defend. Next person's killer observation: find the caller that
builds the creation block whose second dword is `0x42`.

### `0016D6A0` caller count — RECONCILED. It is 2,479, and 2,480 is not reproducible.

Two independent instruments now agree exactly:

```
DumpFullCoverageGraph (getCalledFunctions)         : 2479 distinct calling functions
DumpDataXrefs, kind=CALL, distinct func_entry      : 2479   (set-identical to the above)
DumpDataXrefs, kind=CALL, reference rows           : 2867 call sites
DumpDataXrefs, all kinds, distinct func_entry      : 2511 functions referencing it at all
                          of which DATA (pointer slots) : 1515
```

**2,480 corresponds to none of those definitions.** Most likely an off-by-one. Please correct it
wherever repos-f1's figure was merged; the three defensible numbers are 2,479 callers / 2,867 call
sites / 2,511 referencing functions, and which one a document wants depends on its sentence.

### Proposed questions

| Proposed id | Question |
|---|---|
| `PROPOSED-repos78-7` | What do the per-class controller pool constants mean — Music **2**, Seb **96**, Sep **256**, Stream **4**, Shout **6**, each passed to a class-specific initialiser on `this+0x20`? "Simultaneous voice capacity" is the natural reading and would be a directly player-facing number (Music 2 = a crossfade pair), but the five initialisers were not read and I have **not** claimed it. |
| `PROPOSED-repos78-8` | Which screen owns window type `0x42` in `0027F5D0` — the BR-3 blocker above. |

## AUDIT-LOG

### I found a real error in my own DOCUMENTED document, and it was banned reasoning

**Was:** "`001DBDB0` fetches the **`AudioController` singleton**", with `00210C00`'s two branches
described as "controller list A at `+8`" and "list B at `+0x10`". That claim ran through §2, §3, §4,
§5 and the data table.

**Is:** the singleton at `01FD36A0` is **not an `AudioController`.** `002105E0` heap-allocates and
constructs **five** objects into slots `+0x00`..`+0x20`, each deriving from `AudioController` (each
ctor calls the base `00212710`, then stamps its own vftable), each named by real RTTI:

| slot | ctor | class | pool constant |
|---|---|---|---:|
| `+0x00` | `00217FD0` | `MusicAudioController` | 2 |
| `+0x08` | `0021A9F0` | `SebAudioController` | 0x60 |
| `+0x10` | `00219400` | `SepAudioController` | 0x100 |
| `+0x18` | `0021CC10` | `StreamAudioController` | 4 |
| `+0x20` | `0021BDB0` | `ShoutAudioController` | 6 |

So `00210C00`'s fork is **Seb vs Sep**, `002DF220` hardcodes the **Seb** side, and the `0215EFxx`
family drives **Music** — which is what closes BR-6.

**How I got it wrong, which is the part worth keeping.** `00212760`, an `AudioController`
destructor, sits beside `00212950` and near `00210B30`, and it was the only class name in the
neighbourhood. I attached it to the singleton. That is **address-adjacency reasoning wearing a class
name** — the inference this database bans outright — and it survived my own falsification pass
because I attacked the pan/volume claim, the 512 split and the census, and never attacked the one
claim I had not derived from a body. *The falsification pass covered what I had worked hardest on,
not what I had assumed cheapest.*

**What caught it:** reading `00212710`, the actual `AudioController` constructor, which builds one
EASTL list with head at `+0x08` and tail at `+0x10` — a layout that cannot produce the accesses
`00210A40` (`[obj+0x00]`) and `00210C00` (`[obj+0x08]` *and* `[obj+0x10]` as two separate objects)
actually make. The contradiction was visible in bodies I already had.

Document corrected in 15 places with the trail in §8. `check_consistency.py` now reports
**consistent: no address is described two different ways** across 90 documents, and your
`Superseded readings` exclusion is working — the correction trail no longer trips it.

---
---

# Third block — falsification pass on `phyre-script-object-accessors.md` (a document I did not write)

Program state: GZF `2ed8affb…`, snapshot `46f02e26…`, EXE `73461d08…`. Claims attacked in
**provenance order — inherited and assumed first, body-derived last.** Full record in the
document's new §10.

## OPEN-QUESTIONS

**AZ-4 — ANSWERED.** What the 156 mis-tagged accessors have in common is a single feature of the
bound type: **140 of the 156 bind a type that is itself a template instantiation** (`PArray<…>`,
`PSharray<…>`), and **zero of the 588 correctly-tagged do** — a perfect separation. Of the other 16:
ten bind a non-Phyre `struct` (D3D11 descriptors), two bind `Phyre::PTimer`, four are cv-qualified.
So the GFZ classifier awarded `Phyre.ScriptVM.Object*Accessor` only for a **plain, non-template,
Phyre-namespaced class** and fell back to `NativeQualified` whenever the bound type carried a nested
`<`, sat outside `Phyre::`, or was a `struct`. The 3 `ReflectionBridge` are plain Phyre classes
(`PClassDescriptorDynamic`, `PAssetReferenceImport` ×2) — a deliberate assignment, not a fallback.

AZ-1, AZ-2 and AZ-3 remain open and were not attacked.

## AUDIT-LOG

### One claim overturned

**§9: "588 of these 747 are among them, 159 are not."** The real intersection of the 747 accessors
with the 1,219 `Phyre.ScriptVM.*`-tagged functions is **591**, complement **156**.

`588` is `323 + 265`, the two accessor sub-tag counts from §8's own table, carried into a sentence
about a **different population** — membership in the 1,219, which is every function with *any*
`Phyre.ScriptVM.*` CodeDomain and therefore includes `ReflectionBridge`. §8 of the same document
records that 3 of the 747 carry `Phyre.ScriptVM.ReflectionBridge`. Those three are inside the 1,219
and were counted as outside it, so the document contradicted itself between §8 and §9 — and the
arithmetic `747 − 588 = 159` happened to match §8's `156 + 3`, which made the wrong figure look
corroborated by a second measurement when it was the same measurement twice.

**This is the exact hazard in the standing rules** — a count correct for the set it was measured on
and wrong for the sentence it was written into — and provenance-ordered attack found it first,
because it was the cheapest claim in the document: a number lifted from a table two sections up.

### Everything else attacked survived, and one claim is now stronger than stated

Re-derived independently from the authorized EXE rather than from `phyre_xrefs.tsv`:

| Claim | Result |
|---|---|
| 747 accessors, all `::Get`, no `Set` | **747 / 747 / 0** — exact |
| 402 pointer / 345 reference by type-name suffix | **402 / 345** — exact |
| 412 distinct bound types | **412** — exact |
| assert lines 106/118 vs 141/143 | **1,494 sites, exactly 2 per function, 747/747.** Pointer writes only 106 and 118 (402 each); reference only 141 and 143 (345 each). **Zero exceptions** |
| the message split | pointer references `00D24BE0` + `00D24C40` (402 each); reference references `00D24050` + `00D240B0` (345 each). **Zero cross-contamination** |
| the 24-byte assert record at `02E41000` | **1,494 writes to each** of `__FILE__`, `__LINE__`, `__FUNCTION__` |
| the §2 disassembly listing | matches **byte-for-byte at every quoted address** (two `test` instructions elided; the listing is explicitly abridged) |
| the `+0x78` base-chain walk | confirmed — walks the **provided** object's chain for the **required** descriptor, so derived-where-base-required is correct as §6 says |

So §4's "three independent features agree" understates it: the type-name suffix, the `__LINE__`
constant and the diagnostic string partition the 747 into the **same** 402 / 345 split with **no
element out of place on any of the three**. That is now written into the document.

### What I tried that failed to break it

- Hunted a `Set` counterpart — **with a positive control first**, because this document records an
  instrument that returned a clean zero on these very strings through its own printable-byte filter.
  My first message scan reproduced that class of failure: filtering on `"obtained from script"`
  silently missed `"Unable to **obtain** object pointer from script…"`. The re-run asserts a
  known-present string before reporting any absence, and only then were all four messages found.
- Tried to make the `__LINE__` and type-name features disagree per-function rather than in
  aggregate. No function writes a line constant belonging to the other variant.
- Tried to break the appendix as an attribution artifact by re-deriving the address→type mapping
  from the EXE instead of the tool output. Counts match exactly.

### Two defects that are not claims

- **`audit: passes: 1` in the frontmatter, while `AUDIT-LOG.md` listed the document as owing "a first
  named falsification pass".** One was wrong and neither was checkable from the other.
  `last_pass_state`, `crossref_clean` and `reopened_count` were absent entirely — so the claimed pass
  had no recorded program state. Filled in, `reopened_count: 1`.
- **§2's bijection sentence did not name its population.** The bijection is over the wider `Phyre::`
  string set (751); the accessor population is 747. Both numbers right, sentence didn't say which.

## NOT MINE — five consistency disagreements from a document that landed after your "all green"

`check_consistency.py` at 91 documents now reports 5, all traceable to
`05-Spawn-Encounter-Lifecycle/spawn-placement-height-and-authored-tunables.md`:

```
SIZE  00267DB0   78 B (spawn-placement-height…)  vs  84 B (scriptvm-verb-dispatch…)
NAME  0016D6A0   _guard_check_icall (spawn-placement-height…)  vs  ICF_FoldedRetStub (x2)
NAME  0050F410   Spawn_SetNativeLifecycleRanges       vs VM_SpawnSetNativeLifecycleRanges
NAME  0050F520   Spawn_SelectAndPrepareAutomaticEntry vs VM_Spawn_SelectAutomaticEntry
NAME  00510390   Spawn_CountActiveCapTrackedActors    vs VM_Spawn_GetActiveCapTrackedCount
```

The last three are **inside that single document** — the same "correction written where it was
discovered while the original statement stayed" shape. The `0016D6A0` row is the fleet-settled name
not having reached it yet. The size disagreement is the interesting one: a body extent should not be
a matter of opinion, so one of the two documents read the wrong function. I have **not** edited
another session's live document; it is yours to merge.

---
---

# Fourth block — falsification pass 8 on `gi-render-command-family.md`

Program state: GZF `2ed8affb…`, snapshot `46f02e26…`, EXE `73461d08…`. Provenance-ordered.
Seven prior passes had worked the device identity hard, so this one went at what no pass had
touched: the headline class count (which §8 itself flags as not independently derived), the
**modding advice**, and the numbers offered as corroboration. Full record in the document's §16.

## OPEN-QUESTIONS

No BG question closed. **BG-1's evidence is weaker than published** — see overturn 3.

## AUDIT-LOG

### Three claims overturned

**1. §6: "Every shape-A command reserves through `[dev+0x000]`."** Only **5 of 14** do —
`GiColorRect`, `GiPolyGT4T`, `GiPrim`, `GiScreenImage`, `GiSprite`. **The document's own §2 census
has always said `[dev+0x000] 5`**; §6 generalised it to the whole shape. This is a *modding* claim
under "best intervention point": a hook there sees five commands and silently misses `GiTrans`,
`GiTransNz`, `GiNormal` and `GiZNormalOnOff`, which never touch that slot. Corrected in place.

**2. §3's "reservation count" column and §4's "independent support" for the reset commands.**
**Neither shape-C reset command makes any device-vtable call at all.** Their `3` is the second
argument to a direct `call FUN_00600A60`:

```asm
001F3260  call 0x609710 ; test al,al ; je ...
          mov  edx, 3            ; <-- the "3"
          call 0x600a60          ; DIRECT, not [dev+n]
```

So it is not a vertex reservation and it is not support for the reservation-count discriminator,
which is a claim about what commands pass to `[dev+0x000]`. **Two mechanisms produced two `3`s and
the agreement was read as corroboration** — the false-corroboration entry you just wrote up, in its
other form: not a figure derived from the one it agrees with, but a figure from an unrelated
mechanism that happens to match. The document's own device-slot census already implied it, since
neither reset command contributes a single slot to it.

**3. §10's "the reserve idiom occurs at exactly 4 sites image-wide, all `Gi*`."** I reproduced the 4
— **and the reproduction shows why it is 4.** Run with a positive control against the five known
`Gi*` reserve sites, the scan returns **4 of 5**: it misses `GiPrim` at `00863DD1`, *a call site this
same document describes in §4* as using the reserve call with a variable count.

The true count of `Gi*` sites through `[dev+0x000]` is **5**. The "exactly 4 image-wide" figure is
the output of a filter with a demonstrated **1-in-5 false-negative rate on its own known-positive
set**, and it is a leg under **BG-1**'s negative ("nothing outside this family touches the
interface"). Not refuted — **not established at the strength stated**, because the standard requires
an absence claim's positive control to come back and this one comes back short.

### Two claims confirmed, one promoted from dependent to independent

**The 18-class headline no longer rests on a shared source.** §8 states plainly that "18 classes"
comes from `methods.tsv` — the same source as the vtable index — and is "that source read again, not
independent corroboration". Re-derived **straight from the EXE's RTTI** (`.?AV<name>@@` → COL → vtable),
with a positive control on a class proven by that route in another category:

```
Gi* type descriptors   : 18
(class, vtable) pairs  : 18    one vtable each, no multiple inheritance
two-slot   classes     : 16
three-slot classes     :  2    GiResetRenderTargetObj, GiResetDefaultRenderTargetObj
```

Every count matches. **§8's shared-source caveat can be retired.**

**The 20-slot device census reproduces exactly** — all twenty slots, every per-slot count, zero
disagreements, including the four recovered by the earlier `jmp` fix. The `+0x78 → +0x98 → +0x80`
triple holds 8 of 8, same order, once each. The reservation-count discriminator reproduces exactly.

### An instrument failure of my own

My first census regex accepted a vtable displacement only in `0x`-prefixed form; capstone prints
small ones bare, so `[rax + 8]` was invisible and I got **19 of 20 slots**, with `+0x008` at zero
against the document's 5. **The document was right and my instrument was wrong.** Worth keeping for
the shape: *a scan that agrees with its target in 19 places and disagrees in 1 is far more likely to
be broken in that 1 place than to have found something.* I chased the disagreement instead of
reporting it, which is the only reason it did not become a false finding.

### Naming, and a fact that follows from it

`0016D6A0` was "the `_guard_check_icall` stub" / "the CFG stub" in §2 and §6 → **`ICF_FoldedRetStub`**
(BA-1). Following from that and not previously stated anywhere: **11 of the 18 `Gi*` classes have
slot 0 folded onto it**, so the `(prepare, execute)` contract §12b confirms from the consumer side
has a **no-op prepare for most of the family**.

### I did the neighbour check first this time, and it was cheap

Before attacking, I indexed every other document citing these 53 addresses:
`vtable-method-index.md` (13 shared), `sqex-sd-sound-driver-architecture.md` (6 shared vtables),
`EVIDENCE-STANDARD.md` (2), `OPEN-QUESTIONS.md` (2). All agree with the target; the six
`SQEX::Sd::Driver::*Sound` vtable addresses are cited identically in the Gi and the Audio documents.
**No contradiction found — but it took about a minute, and last block the same check would have
caught my `AudioController` error before I published it.**

## For your metric work — the checker now detects the defect I reported

`check_consistency.py` reports **0 size, 0 name, 0 caller-count** disagreements at 91 documents, and
**5 `FRONTMATTER audit gaps`** — documents claiming `passes > 0` with no `last_pass_state`:

```
00-Engine-Core-Runtime\Object-Model\vtable-method-index.md
00-Engine-Core-Runtime\Startup-Data-Construction\generated-float-table-builders.md
16-UI\Dynamic-Geometry-Instances\dyngeo-instance-family.md
18-Audio\Audio-Bank-And-Controller-Family\audio-bank-and-controller-family.md
99-Unresolved-Residual\Largest-Unclassified-Code\the-largest-unclassified-functions.md
```

These are exactly the "claimed pass with no recorded program state" case — each one is a pass
`audit_coverage` counts and nobody can verify. `vtable-method-index.md` is the awkward one: your
owed table records it as **DISCHARGED, survived four attacks**, so the pass is real and only the
stamp is missing. The other four need checking before their `passes` is believed.

---
---

# Fifth block — first falsification pass on `dyngeo-instance-family.md`

Program state: GZF `2ed8affb…`, snapshot `46f02e26…`, EXE `73461d08…`. Full record in the
document's new §10.

## THE CLAIMED PASS DID NOT HAPPEN — `passes: 1` was counting the authoring pass

`AUDIT-LOG.md` **pass 103 is the pass that created this document** — its own scope line reads
*"new document `16-UI/Dynamic-Geometry-Instances/dyngeo-instance-family.md`"*. There was no §10 and
no recorded attack, so by `EVIDENCE-STANDARD.md`'s own definition (`AUDITED` = survived a pass
**recorded in §10**) the count had nothing behind it. Pass 103 is a careful piece of authoring — it
declines address adjacency explicitly and carries a "Not claimed" paragraph — but authoring is not
falsification. **This is the first pass.** One data point for your metric work: at least one of the
five gaps was not a missing stamp on a real pass, it was a pass that never occurred.

## AUDIT-LOG

### Overturned: the variants differ at four slots, not two

*"The four `FontTextSpecial` classes differ at **exactly two slots, 10 and 11**, and nowhere else."*
A slot-by-slot diff of the four 12-slot vtables:

| slot | plain | `Final` | `Shadow` | `ShadowFinal` |
|---:|---|---|---|---|
| **2** | `00213AD0` | `00213AA0` | `00213B00` | `00213B00` |
| **6** | `00213D10` | `00213B40` | `00213D10` | `00213D10` |
| 10 | `002142A0` | `00214210` | `00214540` | `002143E0` |
| **11** | `00214890` | `00214860` | `002148B0` | `00214860` |

Slots 0,1,3,4,5,7,8,9 identical across all four. **Slots 2 and 6 were missed**, and both carry real
information.

### Slot 2 is a sized deleting destructor, and it breaks the 2x2 at the layout level

```
00213AD0  plain                    mov edx, 0x160   -> 352 B
00213AA0  Final                    mov edx, 0x170   -> 368 B
00213B00  Shadow AND ShadowFinal   mov edx, 0x168   -> 360 B
```

**`Shadow` and `ShadowFinal` share one destructor and one size.** A clean 2x2 product — plain
`0x160`, `Final` +0x10, `Shadow` +0x08 — would make `ShadowFinal` `0x178`. It is `0x168`, identical
to `Shadow`. So **"Shadow x Final" is a product in behaviour at slot 10 and is not a product in
object layout.** Three free-object sizes for the census as a by-product.

### Overturned: slot 11 has three implementations, not two, and forwards a mode not a boolean

*"**Both** slot-11 overrides… The shadow variant forwards a boolean that the plain variant pins to
false. **That is the entire difference at this slot.**"* There is a third, `00214860`, used by
**both `Final` and `ShadowFinal`**, unmentioned. All three tail-jump into slot 35 (`+0x118`) and
differ only in the third argument:

```asm
00214890  plain    xor r8d, r8d                       -> 0
002148B0  Shadow   test r8b,r8b ; setne al ; movzx    -> 0 or 1
00214860  Final    neg al ; sbb r8w,r8w ; and r8w,2   -> 0 or 2   (also ShadowFinal)
```

The argument is a **three-valued mode `{0 plain, 1 shadow, 2 final}`**, not a boolean. And at this
slot **`ShadowFinal` takes the `Final` value, not the `Shadow` one** — the same asymmetry the
destructor sizes show, from an independent direction.

### Confirmed, and promoted off a shared source

The eight classes and three vtable shapes came from the vtable index. Re-derived **straight from the
EXE's RTTI** with a positive control: 8 type descriptors, one vtable each, 21-slot ×3 / 12-slot ×4 /
3-slot ×1 — exact match. **The shape census no longer depends on the vtable index.** The slot-10
tail-call structure also reproduces (`00214210` and `00214540` both end `jmp 0x2142A0`).

### The constant pool: this document was right, and a NEIGHBOUR IS WRONG

§2 argued from uneven spacing that `008C5F80…` is *"four rows selected from a pool of common
vectors, not a contiguous matrix literal"*. Dumping `0x60` bytes instead of the four cited rows shows
**why** the spacing is uneven — the gaps hold the negations:

```
+0x00  1  0  0  0   <- loaded      +0x30  0  0  1  0   <- loaded
+0x10  0  1  0  0   <- loaded      +0x40  0  0 -1  0
+0x20  0 -1  0  0                  +0x50  0  0  0  1   <- loaded
```

Six +/- axis vectors, interleaved. The four loaded do assemble to the identity, so that claim stands.
But **`99-Unresolved-Residual/Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md` lists
`008C5F80` as "`.rdata` float[4]x4 — the 4x4 identity"**. Its four offsets are right; its type is
not. The first `0x40` bytes there are `1000 / 0100 / 0-100 / 0010`, which is not an identity matrix,
and naming a 64-byte object at that address is exactly the framing the DynGeo author declined to
use. **Routed to that document's owner — I did not edit it.** That makes **five** times the
neighbour check has caught something.

### What I tried that failed to break it

- Attacked the eight-class / three-shape census expecting the vtable-index dependency to hide an
  error. RTTI agrees exactly.
- Attacked the slot-10 tail-call claim by re-reading all four terminating instructions rather than
  trusting the table. All four as described.
- Attacked the identity decode by dumping the whole region rather than the four cited rows — which
  is what surfaced both the +/- pool and the neighbour's error.
- Neighbour check run **first**: 15 addresses shared with the vtable index (agrees throughout), one
  each with two residual documents.

## Gates

0 size, 0 name, 0 caller-count disagreements at 91 documents. **`FRONTMATTER audit gaps` down 5 → 3.**
Links resolve.

---
---

# Sixth block — first falsification pass on `audio-bank-and-controller-family.md`

Program state: GZF `2ed8affb…`, snapshot `46f02e26…`, EXE `73461d08…`. Record in the document's §10.

## Did a pass happen? No — but this one is a harder case than DynGeo, and the distinction matters

`AUDIT-LOG.md` pass 104 is the authoring pass ("**new document** `18-Audio/Audio-Bank-And-Controller-Family/…`").
Unlike pass 103 it **did** include independent re-verification of four load-bearing claims before
publication — a peer read the family, this session re-derived it. That is real work and it is why
the document is as accurate as it turned out to be.

**But verification is support, and support is not proof.** Re-deriving a claim and finding it holds
is the thing `EVIDENCE-STANDARD.md` warns is not enough: *"anyone can assemble evidence agreeing with
a reading they already hold."* Nobody had tried to destroy anything. So the honest classification is
the same as DynGeo's — unattacked — but the *reason* differs, and I would not want the two logged
identically. **Pass 103 mistook careful authoring for a pass; pass 104 mistook verification for
falsification.** The second is the more seductive error, because verification genuinely reduces risk.

**Declared conflict of interest:** I wrote the audio boundary document, which shares five addresses
with this one (the five controller constructors). I attacked those *harder* and re-derived every one
from the image rather than from either document.

## AUDIT-LOG

### Overturned: `StreamAudioController` has no slot 7 and no secondary base

§2's heading is *"Controllers carry a second base at `+0x20`"* and its text reads *"**Every**
controller's slot 7 is an adjustor thunk, and **all four** are the same two instructions"* — a claim
about the family, evidenced by a table of four, while the family has **five**.

| class | vtable | slots | slot 7 |
|---|---|---:|---|
| `AudioController` (base) | `00906CD0` | **7** | — |
| `MusicAudioController` | `00907970` | 8 | `00218980` |
| `SebAudioController` | `00907DE0` | 8 | `0021B150` |
| `SepAudioController` | `00907BA8` | 8 | `00219B10` |
| `ShoutAudioController` | `00907FF0` | 8 | `0021C440` |
| **`StreamAudioController`** | `00908200` | **7** | **absent** |

Its vtable is the same length as the base's. **It does not carry the secondary base**, so the
heading is false for one class in five.

**Stream is the odd member on four independent counts** — and that is the substantive result:
(1) no slot 7 / no secondary base, this pass; (2) `0xB8` with **one** bank method against Seb/Sep at
`0xE0` with 10 and 9; (3) constructed fifth but stored at `+0x18`, before Shout at `+0x20`;
(4) never selected by the play call's fork, which reaches only `+0x08` and `+0x10`. **None of the
four is derived from any other.**

### Everything else attacked — and all of it survived

- **The seven object sizes: 7 of 7 exact**, re-decoded from each deleting destructor's `mov edx`.
  `0x20 / 0x38 / 0x48 / 0x58 / 0x68 / 0x68 / 0xA0`.
- **"All six banks' slot 7 is a 52-byte body": 6 of 6**, identical prologues, each with the
  deallocator call.
- **"Four separate 161-byte bodies with identical prologues, not one folded body"** — attacked
  specifically because `/OPT:ICF` folding has produced false distinctions elsewhere in this project.
  Four distinct addresses, all 161 B, one prologue. **Genuinely not folded.**
- **The hierarchy cross-check** — `MusicAudioBank` slot 0 is 101 B, calls `007A7010` / `007A7A20`
  (SQEX Sd driver), **no deallocation**. Not a destructor, exactly as claimed.
- **The taxonomy chain, end to end, with a positive control on the string scan:**
  `00210980` loads `[rcx+0]` → `00222740` → `.win.mab` / `%s%03d%s`;
  `00210B60` loads `[rcx+8]` → `00223AD0` → `.win.sab` / `%s/se%03d/se%03d%s`;
  `00210C40` loads `[rcx+0x10]` → `00222DC0` → `.win.sab` / `%s/se%03d/se%06d%s`. **Exact.**
- **Manager layout and construction order `0, 8, 0x10, 0x20, 0x18`** — confirmed from `002105E0`.

So the document's strongest claim — **one sound-effect bank format addressed by two id widths, plus
music** — reproduces in full. Three digits against six is the entire `Seb`/`Sep` difference at the
path level.

### What I tried that failed to break it

Expected at least one transcription error across seven sizes: none. Expected ICF to have collapsed
the four adjustor targets: it has not. Ran the string census with a positive control first, because
a missed or absent string has produced a wrong result twice in this project already. Neighbour check
run before attacking — 11 addresses shared with the vtable index, 5 with my own document, no
contradiction in either direction.

## Gates

0 size, 0 name, 0 caller-count disagreements. **`FRONTMATTER audit gaps` 3 → 1.** Links resolve.

---
---

# Seventh block — the `.data` slot population: the premise was wrong

Assigned as a reading job on the grounds that the `.data` vtable-slot population is ~15x larger
than published and **nothing has been read from it**. I measured it, and then found that most of it
*has* been read. Reporting that rather than a document, because a document here would have
duplicated three that already exist.

## The load-bearing correction — the reason the 15x matters is backwards

`why-the-unowned-code-has-no-owner.md` justified the correction with:

> *"`.data` was understated about 15-fold, which matters because `.data` slots are **runtime-built
> dispatch tables** rather than static vtables."*

**The opposite is true.** `.data` runs `01DF0000`..`02F97530`, raw size `0x18E400`, so it is
file-backed only up to **`01F7E400`** — **91.2 % of `.data` has no file image** and is zero at load.
**All 3,015 counted slots lie below that boundary**, so every one is *statically initialised in the
file*. A slot that is genuinely built at runtime is zero in the file and **invisible to this scan by
construction**: the audio registry singleton `01FD36A0`, the audio gate `02091098` and the transform
workbench `022D8F00` are all above the boundary and contribute **nothing** to the 3,015.

So the 3,015 are **writable tables with a static initialiser** — patchable, not runtime-built — and
the runtime-built population is **not measured by this scan at all**.

**The fact that settles it was already in the database when the claim was written**:
`the-shared-transform-workbench.md` §8 derives the same `01F7E400` boundary from the same PE fields.
Corrected in place with that citation.

**My own positive control is what exposed it.** I seeded the scan with `02EAD0B8`, an audio function
pointer I had proven earlier, and it came back absent. The control failing was the finding — had I
picked a control from inside the file-backed range, the scan would have looked sound and I would
have inherited the framing.

## Population, re-derived (definition stated)

8-byte-aligned non-zero qword in the section whose value is a **known function entry**:

```
.rdata  59,306 pointer slots into .text, 29,000 land on an entry (48.9%)
.data    3,423 pointer slots into .text,  3,015 land on an entry (88.1%)
_RDATA     110 pointer slots into .text,      8 land on an entry ( 7.3%)
```

**29,000 / 3,015 / 8 reproduces exactly.** The counts are right; only the interpretation was wrong.

## What I found, and where the database already had it

| I measured | Already documented |
|---|---|
| a 380-entry table at `01EEC460`, 249 entries sharing `002FDDA0` | **`07-Combat-Action/Action-Dispatch/battle-action-handler-table.md`** — base `01EEC460`, span to `01EECF90`, **341** live entries, 249 sharing that handler, both consumers read, already survived a pass |
| 202 slots at `01EFA5C0`, 42 holding `ICF_FoldedRetStub` | **`08-Combat-Formula/Step-Table/combat-formula-step-table.md`** — same base, same 202, **the same 42 no-ops**, with the `ret 0` body quoted and an open question on authored-vs-folded |
| the `01F7E400` BSS boundary | `the-shared-transform-workbench.md` §8 |

**My 380-entry span was wrong in exactly the way that document records correcting** — its §5 reads
*"An earlier attempt over-extended the table to 380 slots by walking outward"*. My span ran past the
end into non-pointer data (`3E80000000000000`, `3F000000` — floats). The correct bound is 341 live
entries in `01EEC460`..`01EECF90`. **I reproduced a previous session's error, and the document that
already fixed it is the one the neighbour check pointed at.**

## Two instrument errors of my own, both from the same assumption

1. **Skipping zero slots fragments a table that has null entries.** My contiguous-run clustering
   split one 341-entry table into runs of 37 / 16 / 226 / 62 because 22 entries are NULL. A run
   boundary is not a table boundary.
2. **A contiguous run is not necessarily a table.** I read the `01EFA5C0` run as "a bank of
   individually-called slots" from 24 `call [rip+d]` sites — but those 24 instructions reach only
   **11 distinct slots** of 202, so the run is overwhelmingly indexed and the direct calls are the
   exception. I nearly published "42 of these calls do nothing"; checking showed **none of the 11
   called slots holds the stub**. The claim would have been false.

## Genuinely unread, handed over rather than claimed

**1,678 of the 2,382 runs are singletons, and 1,535 of those are `Phyre`-free
`Script_VM_Native_Bridge` targets** — individually-initialised, writable, one-per-native function
pointers. `scriptvm-native-dispatch-table.md` discusses record counts (1,496 / 1,960) but I did not
establish whether that is the same population, and I am not asserting it is. That is the one part of
the `.data` slot space I could not find already covered.

## Process note

The neighbour check has now caught a **sixth** thing, and this is the first time it stopped me
**writing a whole document that already existed**. Worth saying plainly: the check is cheap enough
that it should run before *accepting* an assignment, not only before attacking a document — the
premise "nothing has been read from it" was checkable in about two minutes and was wrong.

## Gates

0 size, 0 name, 0 caller-count disagreements. **`FRONTMATTER audit gaps` 1 → 0.** Links resolve.

---
---

# Eighth block — relocation-certified slot census: a residual lead, and the ScriptVM extent

## The predicate, stated (it is what decides what the numbers mean)

A slot `S` is a **certified function pointer** iff **all** of:

```
P1  S is 8-byte aligned AND inside the section's RAW extent   (it has file bytes at all)
P2  the qword V at S is non-zero
P3  V - imagebase + 0x120000 is the ENTRY of a known function
P4  S carries an IMAGE_REL_BASED_DIR64 (type 10) base relocation
```

**P1 is the clause that limits the result.** `.data` is file-backed only to `01F7E400`, so this
census is blind to the 91.2 % of `.data` that is BSS — anything genuinely built at runtime is
invisible to it by construction. Every count below is "statically initialised slots", never "slots".

Reproduced exactly, 114,962 DIR64 entries: **`.rdata` 29,000 → 27,202** certified (1,798
coincidental, 6.2 %) · **`.data` 3,015 → 3,015** (0 %) · **`_RDATA` 8 → 0** (100 %).

**Control 1 (blind, against work predating the census):** recovered 7 of 7 structures I had derived
in earlier blocks — the `GiPolyGT4T` / `GiSprite` / `AudioBank` / `SepAudioBank` / `AudioController`
/ `DynGeoFontTextSpecialInstance` / `MusicAudioController` vtables. **Control 2:** `_RDATA` returns
0, reproducing the cautionary case.

## Finding 1 — the residual category's flagship, bounded

**Of the 158 residual functions, exactly one has a relocation-certified `.rdata` pointer**: `002AAE40`
at `00916518`. That confirms the flag and adds the bound — the other **157 have none**, so this is a
single admissible lead rather than a class of them.

It is **index 11 of a 12-entry sparse table based at `009164C0`**:

```
[ 0] 009164C0 -> 002A9980      [ 6..10]  NULL x5
[ 1] 009164C8 -> 002A8C50      [11] 00916518 -> 002AAE40   <== the residual function
[ 2] 009164D0 -> 002A9F00      [12+] a power-of-ten table: 1,10,100,1000,10000,...
[ 3] 009164D8 -> 002A9980
[ 4] 009164E0 -> 002A8C50
[ 5] 009164E8 -> 002AA800
```

Seven populated entries, **five distinct targets**. Three `.text` sites take the table's address:
`002ABEFD` in `FUN_002abec0` and `002ABF4D` in `FUN_002abf20` (both → `009164C8`), and `002B393C`
in `FUN_002b3930` (→ `009164C0`).

**Admissible as tier 8** — a real data reference in `.rdata`, relocation-certified. It gives
`002AAE40` a structural identity (entry 11 of a dispatch table shared with five named functions)
without naming what it does. The adjacent power-of-ten table is recorded as a **layout fact only**;
adjacency is a banned evidence class and it is not offered as evidence of purpose.

## Finding 2 — the ScriptVM question: it is *both*, and the extent is wrong

**Same population?** Yes, mostly: **1,685** certified ScriptVM-targeting `.data` slots fall inside
the documented table (`base 01EED720`, stride `0x20`). My earlier "1,535 singletons" was my own
run-clustering fragmenting 32-byte records — the third face of the same instrument error.

**A second surface?** Also yes: **502 certified ScriptVM slots fall outside**, in **8 clusters**,
the largest `01F28D30..01F2A140` (187 slots), then `01F277E0..01F28180` (89), `01F281D0..01F28C30`
(83), `01F26F20..01F27790` (77), `01F26728..01F26A40` (28). These target `0050Dxxx` functions and are
not described anywhere I could find. **Handed over as a real lead, not claimed as a table** — I have
not established their record structure.

**And the extent is over-long, in the same way the document already corrected once.**

| extent | certified slots | offsets used in the 32-byte record | owners |
|---|---:|---|---|
| **1,496 records** | 1,739 | `+0` 1,234 · `+8` 276 · `+16` 229 · **`+24` = 0** | ScriptVM 1,685, Movement 19, Party 8 |
| 1,960 records | 1,941 | `+0` 1,285 · `+8` 327 · `+16` 279 · **`+24` = 50** | …plus **CombatFormula 160** |

At 1,496 records **nothing occupies `+24`** — which is precisely the document's own
"no record carries four handlers" correction, reproduced by an instrument that never read it. At
1,960 records `+24` fills up and 160 `CombatFormula` pointers appear, because **`01EFA5C0`, the base
of the combat formula step table, is exactly record 1653 of this frame**:
`(0x01EFA5C0 - 0x01EED720) / 0x20 = 1653.00`.

**The out-of-bounds read was corrected and then re-entered at larger scale by the extent adopted to
fix it.** The `+24`-is-null result stands; the frame it was verified in does not. Corrected in place
in `scriptvm-native-dispatch-table.md` with both censuses shown.

## Gates

0 size, 0 name, 0 caller-count disagreements; 0 frontmatter audit gaps; links resolve.

---
---

# Ninth block — my residue figure regrouped, and the dead-code candidates refuted

## 1. My `.rdata` residue figure was wrong and is corrected

`why-the-unowned-code-has-no-owner.md` said the 266 uncharacterised slots form **192 runs, 166 of
them single**. That was step-8 contiguity — the right rule for the rest of `.rdata`, where slots
really are arrays of pointers, and **the wrong rule for this residue**, which is largely 16-byte
records with one pointer field.

| rule | groups | singletons |
|---|---:|---:|
| contiguity, step 8 | 192 | **166 (86 %)** |
| progression, stride `0x8`–`0x100`, ≥3 members | **52** | **22 (42 %)** |

Strides: `0x10` ×14, `0x8` ×6, `0x18` ×4, `0x30` ×3, `0x20` ×2, `0x60` ×1.

**The residue is not fragmented — it is mostly record tables**, and the largest structures in it are
**not** the Audio pointer arrays I read first:

| group | members | stride |
|---|---:|---|
| `01CCB168`–`01CCB308` | **27** | `0x10` |
| `01CCA3F8`–`01CCA548` | **22** | `0x10` |
| `01CEB070`–`01CEB108` | 20 | `0x8` — the Audio vtable, correctly grouped by contiguity |
| `01CCC6C8`–`01CCC7B8` | 16 | `0x10` |
| `01CCAD58`–`01CCAE28` | 14 | `0x10` |

Contiguity had hidden the two largest. **A family of 16-byte-record tables in `01CCAxxx`–`01CCExxx`,
all unowned, none characterised, consumers not traced** — that is the real shape of the residue and
it is a better target than the singletons ever were.

**86 % singletons against this section's own base rate of ~16 % was the tell**, and it came from a
session measuring grouping behaviour per section — not from anything in my own work. Corrected in
place with both numbers and the rule stated.

## 2. `0034CF90` and `0034D790` are not dead — they are script verb handlers

Both were flagged as dead-code candidates on the strength of **0 incoming / 6 outgoing** and absence
from the residual 158, with the proposed consequence that *dead code is not confined to the
unclassified tail*. **That consequence does not follow, because they are live.**

Searching every ScriptVM command table by its own declared record count:

```
0034CF90  <- family 0, record 0     field begin/+0x08   slot 01EED708
0034D790  <- family 0, record 1493  field begin/+0x08   slot 01EF91A8
0034DCC0  <- family 0, records 0 and 1493, field poll/+0x10
```

They are the **begin callbacks for script call IDs `0x0000` and `0x05D5`**, reached through the
dispatch table the three `VMNativeCommandDispatch_Get*Callback` accessors index. Their zero incoming
edges are a call-graph artifact — **precisely the class this census exists to describe**: two thirds
of uncalled unowned code is reached through a pointer in a table, and an `E8`-based edge list is
blind to all of it by construction.

**The signature "0 incoming, N outgoing, not in the residual" is not evidence of death.** It is the
signature of *reached through data*, which is the majority case here. Distinguishing the two needs a
data-pointer search, and the relocation-certified census answers it in one step. Records 0 and 1493
also share one poll callback while having different begin callbacks — worth noting for whoever holds
the verb-dispatch document.

**This took one step because the family-table structure from an earlier block was still in context**
— the same reason it was worth reporting the extents rather than only the conclusion.

---

# Block: developer tuning console, arm catalogue slices A and B (2026-09-03)

## COVERAGE

Two documents under `00-Engine-Core-Runtime/Developer-Tuning-Console/`:

| Document | Ids | Real arms | Unimplemented |
|---|---:|---:|---:|
| `arm-catalogue-slice-A-ids-12-43.md` | 12–43 | 27 | 5 (13, 16, 17, 18, 23) |
| `arm-catalogue-slice-B-ids-44-75.md` | 44–75 | 29 | 3 (56, 58, 59) |

**64 of the console's 282 ids are now catalogued; 218 are not.** Slices C–I are unclaimed. Both
documents state their own bound in the first line so neither can be read as a statement about the
table as a whole.

Slice A is counters, toggles and mode cycles over 26 fields of the object at `rdi`. Slice B is
**continuous tuning**: 13 of its 32 ids step floats. **The two adjacent slices have different shapes,
which is the single most useful thing to hand the next slice-taker** — an extractor tuned on A would
have reported 13 empty rows in B.

## OPEN-QUESTIONS

**Closure — the direction-flag item raised with the slice division.** It was recorded as "the
register differs between arms — `bl`, `sil` — so it is an argument rather than a global, and the
caller has not been traced." The prologue at `001D1660` settles the first half from the code:

```
001D1673  movzx esi, r8b     ; arg 3 -> sil
001D1677  movzx ebx, dl      ; arg 2 -> bl    <- the direction flag
001D167A  mov   rdi, rcx     ; arg 1 -> rdi   <- the settings object
001D167D  cmp   r9d, 0x119   ; ids 12..293 = 282, the code's own bound
```

Both registers are **arguments**, so an arm consulting `sil` rather than `bl` is reading the console's
second byte parameter, not a different mechanism. **Who calls the console remains open** and is the
half of the item that is not closed.

- **PROPOSED-repos78-1** — What are the thirteen floats at `02CB80B0`–`02CB80F4`? Known: their step
  magnitudes and that ids 63–75 own them one-to-one. **None was traced to a reader.**
- **PROPOSED-repos78-2** — What occupies `02CB80D4`–`02CB80E4`, the six slots the id run skips? The
  gap is a layout fact; it is **not** evidence the slots are unused, since slices C–I are unread.
- **PROPOSED-repos78-3** — Why do ids 67 and 69 step by `0.001` where the other eleven step by `0.01`?
  Their targets (`02CB80C0`, `02CB80C8`) are **not adjacent**, so it is not a contiguous sub-range.
- **PROPOSED-repos78-4** — What is the settings object at `rdi`? Unidentified, which is why every
  slice-A target is an offset rather than a name.
- **PROPOSED-repos78-5** — Who calls the console, supplying the direction flag and the object?

## AUDIT-LOG

**My own slice A had the one-path extraction defect, and I found it in my own output.** The first
version bounded each arm at its first `jmp 001D4BFA`. That address is **both the unimplemented-id
target and the common tail most real arms jump to**, so the walk read one branch of every two-branch
arm and recorded `inc` where the arm has `inc`/`dec`.

- **Fix:** bound each arm at **the next arm's start address**. Recorded in slice B's method note so
  the next slice does not repeat it.
- **Effect:** every stepping row in slice A gained its second direction. **No target, no bound and no
  unimplemented id changed** — the defect cost half of one column, not the catalogue.
- **Why it matters beyond me:** the same fact about `001D4BFA` produces two different failures. A
  *reader* told only that it is the no-op target misreads 212 jumps as 212 commands doing nothing; an
  *extractor* told only that truncates 212 arms. Slice A had the second.

Slice A was **re-run rather than grandfathered** under the corrected row shape
(`field · width · step magnitude · direction mechanism · bound`), and says so in §3.

**Both slices carry the `verify_doc_addresses` disposition rather than a red gate:** `001D4C1C` is a
jump table in `.text` after the console function — the case the checker asks to have confirmed — and
every arm address is an interior address of that same function, because switch arms are not functions.

**Not mine, flagged for merge — confirmed on three consecutive runs, not a mid-write artifact:**
`001D1660` is named `DebugConsole_CommandArms` in `what-the-console-tunes.md` and
`DevConsole_DispatchCommand` in `the-282-command-parameter-console.md`. Neither slice document names
it. The prologue reads as a dispatcher rather than as the arms, but the two documents' authors own
the choice.

## CALL-CHAINS / ADDRESS-INDEX

```
console dispatch  001D1660   (arg1 rcx = settings object, arg2 dl = direction, arg3 r8b)
  id - 12 -> bounds check cmp 0x119
  -> table 001D4C1C + (id-12)*4     a dword RVA
  -> + 0x00120000                   explicit in the code (add r9, rcx)
  -> the arm, interior to 001D1660  read/modify/write an rdi field, or a global, or a helper
  -> jmp 001D4BFA                   shared tail AND the unimplemented-id target
```

- `001D4C1C` — the dispatch table (jump table in `.text`, 282 entries).
- `001D4BFA` — shared tail; also the target of every unimplemented id.
- `02CB80B0`–`02CB80D0` — nine consecutive floats, ids 63–71.
- `02CB80E8`–`02CB80F4` — four consecutive floats, ids 72–75.
- `01DF6E48`, `02CB8148`, `02CB8150` — globals written by slice-A ids 12, 30, 31.
- `02CB8130`, `02CB8138` — globals written by slice-A id 28.

---

# Block: developer tuning console, arm catalogue slice C (2026-09-03)

## COVERAGE

`arm-catalogue-slice-C-ids-76-107.md` — ids 76–107, **29 real arms, 3 unimplemented (100, 101, 102)**.
Stamped against **GN159**. **96 of 282 ids catalogued across A+B+C; 186 remain. Slices D–I are open.**

Slice C is the densest tuning range so far: **27 of 32 ids adjust a float.** The shape question asked
of every remaining slice — *does the arm shape hold here* — answers **mostly, and the exceptions are
the findings**: 26 arms have the standard one-constant/both-directions shape, one is multiplicative,
two are clamped, and one is not a tuning command at all.

## OPEN-QUESTIONS

**Closes PROPOSED-repos78-2** (what occupies the gap in the `02CB80xx` float run). **Ids 90–94 own
exactly those slots.** Re-deriving all of ids 63–98 from the dispatch table:

```
36 ids -> 36 distinct targets -> 36 slots, 02CB80A0 .. 02CB812C, no gap larger than 4 bytes
```

**One unbroken 36-float array with one command per slot.** The array was never sparse — **the id order
does not follow the address order**, which is why slice B saw a hole. Ids 95–98 also sit *below* the
run slice B thought was the start.

**PROPOSED-repos78-1 narrows rather than closes:** the 36 slots now have magnitudes, bounds where they
have them, and a one-to-one id mapping — **but none was traced to a reader.**

- **PROPOSED-repos78-6** — What is the engine object behind id 103's accessor, and what are its
  `+0xCC4` / `+0xCC8` / `+0xCCC` fields? **This is the closest thing yet to a *name* for a tuned
  value**, because id 103 copies those three fields into the three the console tunes.
- **PROPOSED-repos78-7** — Is id 106's non-reciprocal `×0.99` / `×1.01` pair deliberate?
- **PROPOSED-repos78-8** — What does id 99's byte global `01DFE191` enable?

## AUDIT-LOG

**Correction to slice B, found by slice C.** Slice B called the gap "six slots" and its open question
named `02CB80D4`–`02CB80E4` as six. `(0x02CB80E8 − 0x02CB80D0) / 4 − 1 = **5**` — an off-by-one
between the 0x18-byte *distance* and the count of slots strictly inside it. **Corrected in place, with
the arithmetic shown**, and the open question closed rather than deleted.

> **The substantive caution in slice B held up.** It recorded the gap as a layout fact and explicitly
> **not** as evidence the slots were unused, "because no id in this slice reaches them and C–I have
> not been read." **Slice C reached them and they are all in use.** Had that been written the
> confident way, the database would now carry a false absence claim over five live tuning parameters.

**Three structural findings that no single-arm reading would produce:**

1. **Id 103 is not a tuning command — it re-seeds ids 104, 105 and 106.** It toggles `b+0xC0C`, and
   **only on the off edge** calls an engine accessor three times, copying `[rax+0xCC4/0xCC8/0xCCC]`
   into `+0xC10`, `+0xC14`, `+0xC18` — *exactly* the three fields ids 104–106 tune. So 103–106 are one
   group: **an override flag plus its three parameters, where clearing the flag snaps them back to
   live engine state.** The accessor is a **117-caller hub**, so it is named by role and deliberately
   **not** made an address citation.
2. **Id 106 steps by ratio, not addition** — `mulss 0.99` / `mulss 1.01`, the only arm in the slice
   whose two directions use *different* constants. **They are not reciprocals:** `0.99 × 1.01 =
   0.9999`, so **up-then-down does not restore the value** (0.01 % loss per round trip). A
   multiplicative arm is invisible to an `addss`/`subss` classifier, which is why the per-arm
   magnitude census sees it as an outlier rather than a step.
3. **Ids 92 and 93 are the only bounded float arms here** — clamped to `[0.0, 1.0]` by
   `xorps`/`maxss` on the down branch and `minss` against `1.0` on the up branch. **The clamp is
   one-sided per branch**, which is correct and is why it reads as one bound and not two guards.

**A constant that is not what it looks like:** id 104's step is the **typed literal `0.00555556`**,
not a computed `1/180`. `float32(0.00555556)` reproduces the stored bits and `float32(1/180)` does
not. It *is* `1/180` to six figures — recorded as an observation and explicitly **not** as a finding,
since nothing traces the field to an angle.

**Re-derived, not copied:** 282 table entries, 227 distinct targets, 56 ids at `001D4BFA` — reproduced
from the image before any row was written, and they agree with the frame document. **`step` was
re-derived per arm rather than taken from `Tools/work/repos-d2/console_arms.tsv`**, whose author
correctly labelled that column unverified.

**Gates:** links resolve (183 files, 1080 links); consistency 0/0/0/0 — **the `001D1660` name conflict
I reported is now gone, resolved elsewhere**; `verify_doc_addresses` returns only the expected
`001D4C1C` REVIEW, dispositioned in both B and C.

## CALL-CHAINS / ADDRESS-INDEX

```
001D1660 console dispatch
  -> 001D4C1C + (id-12)*4  -> + 0x00120000 -> arm
     ids 76..98, 107 : float global in 02CBxxxx
     ids 104..106    : float field of the object at rdi (+0xC10, +0xC14, +0xC18)
     id  103         : toggle b+0xC0C; on the OFF edge only, seed those three from
                       [rax+0xCC4/0xCC8/0xCCC] via a 117-caller engine accessor
  -> 001D4BFA  shared tail, and the target of ids 100, 101, 102
```

- `02CB80A0`–`02CB812C` — **36-slot float array, ids 63–98, one command per slot, unbroken.**
- `02CB8140` — id 107, step `0.05`, outside that array.
- `01DFE191` — byte global toggled by id 99.
- `rdi+0xC0C` (flag) / `+0xC10` / `+0xC14` / `+0xC18` — the id 103–106 override group.

---

# Block: developer tuning console, arm catalogue slice D (2026-09-03)

## COVERAGE

`arm-catalogue-slice-D-ids-108-139.md` — ids 108–139, **32 real arms, zero unimplemented**. Stamped
against **GN159**. **128 of 282 ids catalogued across A+B+C+D; 154 remain. Slices E–I are open.**

**The shape question gets its sharpest answer yet: the dominant encoding here is not the one slices B
and C are made of.**

| shape | slice D |
|---|---:|
| one constant, `subss K` / `addss K` | 6 |
| **signed pair, `addss (−K)` / `addss (+K)`** | **25** |
| integer step | 1 |
| unimplemented | **0** |

Both are symmetric — every pair is an exact negative pair — so the magnitude is well defined either
way. **But a classifier keyed on `subss` sees 25 of these 32 arms as one-directional.** Slice D runs
56 `addss` against 6 `subss`; that ratio *is* the shape.

**Four slices, four distinct shape profiles**, and the first slice in which every id does something.

## OPEN-QUESTIONS

- **PROPOSED-repos78-9** — What is the engine object reached by the accessor in ids 114–118 and
  127–133, and what are its float fields `+0x2D0` … `+0x304`? **Twelve fields with step magnitudes
  and two known bounds, none traced to a reader.** This is the same class of thread as
  PROPOSED-repos78-6 and is now the largest single cluster of tuned values with a provenance outside
  the console's own settings blob.
- **PROPOSED-repos78-10** — What is the object behind the pointer at `01F82D20`, and what does the
  two-state dword at its `+0x40` select? **Eighteen arms across the whole table dereference that
  pointer** — the widest-shared structure the console touches.
- **PROPOSED-repos78-11** — Are the `02CB7FE8`–`02CB806C` and `02CB8130`–`02CB8144` clusters two
  arrays or one? This slice reaches both and spans neither.
- `+0x2E4` and `+0x2F8` in the engine object are **unreached by this slice and recorded as such** —
  deliberately *not* filed as an open question about unused slots, which is the shape of claim slice C
  just showed to be wrong.

## AUDIT-LOG

**Two corrections to the frame document, both re-derived over all 227 arms.**

**1. `01F82D20` is a pointer slot and is never nudged.** The frame records it as *the hottest single
address, nudged by 18 different commands*.

```
24 references inside the 227 arms — ALL of them `mov <reg>, qword ptr [01F82D20]`, in 18 distinct arms
0 references that read or write it as a 4-byte float
```

**The count of 18 is right; the operation is not.** It is an 8-byte pointer that 18 arms dereference
to reach fields of the object behind it — id 134 steps the dword at its `+0x40`. **A `data_touched`
column cannot separate an 8-byte pointer load from a 4-byte float nudge**, which is how a pointer
became the most-nudged address in the binary. *Control:* the same scan does report float-shaped
references elsewhere — id 112's `01F82ED0`, sixteen bytes further into the same region, is read and
written as a float by this very slice.

**2. The shared-singleton figures 45 and 33 are call sites, not arms.**

| accessor | ids | distinct arms | call sites |
|---|---:|---:|---:|
| `001A9930` | 14 | **14** | **45** |
| `00193D50` | 16 | **16** | **33** |

**Both numbers reproduce exactly — as call sites.** The arms call these accessors two to four times
each because **each arm re-fetches the object instead of keeping the pointer.** This does not weaken
the "name it, do not cite it" rule; it **tightens** it — the neighbourhood a citation commits a row to
is 14 arms, not 45.

**Thirteen arms tune a live engine object rather than the console's blob** — `call` the accessor,
step `[rax + 0x2D0 … 0x304]`, `call` it again to store. Ids 114 and 115 are the only bounded arms and
their ceilings differ: `[0.0, 1.0]` and `[0.0, 10.0]`, both floored at zero.

**The slice C lesson was applied rather than restated:** the field map has holes at `+0x2E4` and
`+0x2F8`, and they are written as **unreached by this slice, not unused** — ids 140–293 are unread and
nothing here licenses a claim about those two slots.

**Gates:** links resolve (184 files, 1087 links); consistency 0/0/0/0; `verify_doc_addresses` returns
only the expected `001D4C1C`, dispositioned for all slices in slice A §8.

## CALL-CHAINS / ADDRESS-INDEX

```
001D1660 console dispatch
  -> 001D4C1C + (id-12)*4 -> + 0x00120000 -> arm
     ids 108..113, 119..126, 135..139 : float global (02CBxxxx / 01DFE194 / 01F82ED0)
     ids 114..118, 127..133           : engine accessor -> [rax + 0x2D0..0x304] -> accessor again
     id  134                          : *[01F82D20] -> cycle dword +0x40 -> two further calls
  -> 001D4BFA  shared tail
```

- `rax+0x2D0 … +0x304` — twelve tuned float fields of an engine object; `+0x2E4`, `+0x2F8` unreached.
- `01F82D20` — **pointer slot**, dereferenced by 18 arms; `+0x40` is a two-state dword (id 134).
- `01F82ED0` — float, id 112, step `0.02` (the positive control for the claim above).
- `02CB7FE8`–`02CB7FF4` — ids 136–139, step `0.01`.
- `02CB8044`–`02CB806C` — ids 119–126, 135.
- `02CB8130`–`02CB8144` — ids 108–110, 113.
- `01DFE194` — id 111, step `0.02` (neighbour of `01DFE191`, id 99's byte toggle in slice C).

---

# Block: developer tuning console, arm catalogue slice F (2026-09-03)

## COVERAGE

`arm-catalogue-slice-F-ids-172-203.md` — ids 172–203, **27 real arms, 5 unimplemented** (184, 194,
195, 198, 203). Stamped against **GN159**. **160 of 282 ids catalogued across A+B+C+D+F; 122 remain**
(E is another session's). **Slices G, H, I are open.**

**Slice F is the least uniform range read so far** — 27 arms in **18 distinct body sizes**, 20 bytes
to 149, and it is mostly *not* a bank of sliders:

| kind | count |
|---|---:|
| boolean toggle | 11 |
| integer cycle / step | 9 |
| float step | 7 |

## OPEN-QUESTIONS

**Closes the "no observed consumer" note on argument 3.** Slice B decoded `arg 3 -> r8b -> sil` from
the prologue and recorded that nothing had been seen to read it. **Slice F has eight arms that do**,
in two different ways — as the up button of a two-button pair, and as a gate on one branch.

- **PROPOSED-repos78-12** — What does the selector at `rdi+0xC58` select, and why is 20 its
  threshold? **Four commands scale their own step by it**; highest-leverage unknown in the slice.
- **PROPOSED-repos78-13** — What quantity do ids 189–193 reach through a getter/setter pair, and what
  is bounded to `[15.9, 48.0]`?
- **PROPOSED-repos78-14** — What do ids 199–201 call before toggling the three adjacent bytes
  `+0xCEC`, `+0xCED`, `+0xCEE`?
- **PROPOSED-repos78-15** — What does id 183 toggle? It has **no field at all** — both the read and
  the write are calls.

## AUDIT-LOG

**`bl` is not "the direction flag". It is argument 2, and what an arm makes of it is per-arm.**

| direction inputs read | arms |
|---|---:|
| `bl` only | 11 |
| **`bl` and `sil` as two separate buttons** | **8** |
| **neither — the command is unconditional** | **8** |

**Eight of 27 arms ignore the direction argument entirely.** In slices A–D it was universal among
stepping arms; here a third of the range never consults it. The name "direction flag" is a slice-A
generalisation that holds for A–D and **fails here** — recorded in the document rather than quietly
kept.

**Four mechanisms this slice adds to the catalogue:**

1. **A step constant that never appears as a memory operand.** Ids 173/174 load `±0.005` **into a
   register** and then `addss xmm6, xmm7`. **An extractor reading the memory operand of `addss` finds
   nothing.** Third distinct encoding of a step, after one-constant `subss`/`addss` (B, C) and the
   two-memory-constant signed pair (D).
2. **A bound that is data, not a literal.** Ids 177/178/180/181 compare against **another field** —
   `d+0xAD0` and `d+0xADC` — and wrapping down loads that field as the new value. So the pair is
   *cursor and count*. **Every bound in A–D was a literal somebody chose; these four mean "as many as
   there are", and a catalogue recording only literals would show them as unbounded.**
3. **A step that scales with a selector.** Ids 190–193 read the same `rdi+0xC58`, and above a
   selector of 20 compute `step = (selector / 5) * base` via the standard `0x66666667`/`sar 1` signed
   divide. **A per-arm magnitude census records one number for these arms; the arm has two
   behaviours.**
4. **A bound that refuses instead of clamping.** Id 193 tests the *result* and skips the write
   entirely if it would cross `15.9` or `48.0`. **Third bound mechanism**, after wrap and
   clamp/saturate — and it behaves differently at the limit: a clamped value rests on the boundary, a
   refused value stops up to one step short of it.

**Gates:** links resolve (185 files, 8159 links); `verify_doc_addresses` returns only the expected
`001D4C1C`; consistency 0 size / 0 caller-count / 0 frontmatter gaps, and **one NAME disagreement that
is not mine** — below.

## NAME DISAGREEMENT ON `001FF740` — decoded, and neither name is right

Confirmed on two consecutive runs, so not a mid-write artifact:

```
Map_FindByName                       00-Engine-Core-Runtime\...\what-the-console-tunes.md
eastl_string_construct_from_cstring  23-Third-Party-Libraries\EASTL\eastl-strings-...md
```

Decoded from the image (20 callers). The function:

1. inline-`strlen`s its **second** argument (a C string);
2. allocates through a virtual call, or uses a static empty sentinel when the length is ≤ 1;
3. copies the bytes in through an imported `memcpy`-shaped call and null-terminates;
4. **calls `001FF6B0` with argument 1 and the string it just built, and returns that call's result**;
5. frees the buffer before returning.

> **It is not a constructor — it returns another function's result and destroys the string on the way
> out. And it is not the find — the lookup is `001FF6B0`.** It is a **by-name lookup wrapper that
> converts a C string into the container's string type, delegates, and cleans up.**

**Each author saw one half.** This is worth more than picking a winner: the EASTL document may have
reasoned from "this is a string constructor" elsewhere, and that premise is wrong here. Both authors
own their names; the decode above is offered so the choice is made on the whole body.

## CALL-CHAINS / ADDRESS-INDEX

```
001D1660 console dispatch   (arg1 rcx -> rdi, arg2 dl -> bl, arg3 r8b -> sil)
  -> 001D4C1C + (id-12)*4 -> + 0x00120000 -> arm
     ids 172..174, 179 : the 16-arm accessor -> +0x19C, +0x1A0, +0x1A4, +0x4A0
     ids 189..193      : a getter/setter pair (one call to read, one to write)
     the rest          : fields of the object at rdi, +0xAC6 .. +0xD90
  -> 001D4BFA  shared tail
```

- `rdi+0xC58` — **selector** read by ids 190–193 to scale their step; threshold 20.
- `rdi+0xAD0`, `rdi+0xADC` — **runtime bounds** for ids 177/178 and 180/181.
- `rdi+0xCEC`, `+0xCED`, `+0xCEE` — three adjacent bools, ids 199–201, each preceded by a call.
- `rdi+0xC70`, `rdi+0xC3E` — toggles gated by argument 3 (ids 197, 202).
- `001FF740` — see the name disagreement above; a by-name lookup wrapper, delegating to `001FF6B0`.

---

# Block: developer tuning console, arm catalogue slice G (2026-09-03)

## COVERAGE

`arm-catalogue-slice-G-ids-204-235.md` — ids 204–235, **15 real arms, 17 unimplemented**. Stamped
against **GN159**. **192 of 282 ids catalogued across A+B+C+D+F+G; 90 remain** (E is another
session's). **Slices H and I are open.**

| kind | count |
|---|---:|
| **unimplemented** | **17** |
| boolean toggle | 7 |
| **numeric entry editor** | **3** |
| float step | 3 |
| integer step / cycle | 2 |

**Seventeen unimplemented ids — 204, 209–216, 221–224, 232–235, including a run of eight
consecutive.** No earlier slice exceeded five; slice D had none. **Slice G is over half retired.**

## OPEN-QUESTIONS

- **PROPOSED-repos78-16** — What do the three numeric entry fields edit? Two eight-digit decimals
  (`d+0xDB4`, `d+0xDE0`) and one sexagesimal value (`d+0xE0C`), cursors and wrap rules fully read,
  **none traced to a consumer.**
- **PROPOSED-repos78-17** — What sets `b+0xE30`, id 231's coarse/fine modifier, and why is its cycle
  **311** long?
- **PROPOSED-repos78-18** — What do ids 205–207 pass to their call, and what does the byte trio
  `+0xCF9`/`+0xCFA`/`+0xCFB` select?
- `d+0xDDC`, between the two digit widgets, is **unreached by this slice and recorded as such** — not
  filed as a question about an unused slot, for the reason slice C established.

## AUDIT-LOG

**The console has numeric entry fields — a command kind no earlier slice contains.**

Ids 225 and 226 are the same widget twice: a cursor selects one element of an **eight-dword digit
array**, the two buttons roll that digit, `+10 then mod 10` wraps it (which is how a decrement below
zero reaches nine and why both buttons share one wrap step), and the whole number is **recomposed by
Horner's method** into a separate field. Each widget is a contiguous ten-dword block:

```
0xDB4 value | 0xDB8 .. 0xDD4  eight digits | 0xDD8 cursor      (id 225)
0xDDC  -- not reached by this slice --
0xDE0 value | 0xDE4 .. 0xE00  eight digits | 0xE04 cursor      (id 226)
```

**Id 227 is the same idea in base 60** — a selector at `d+0xE14` picks one of three sub-fields, each
wrapped `add 0x3B` then modulo 60, four times in the body. A three-part field counting in sixties is
the shape of a time or duration entry; **that reading is an inference and the modulus is the
finding.**

**Id 231's step magnitude is data, not an instruction constant** — `1` or `10`, chosen by a flag at
`b+0xE30`, then wrapped **mod 311**. Every magnitude recorded anywhere else in this catalogue is a
constant in the instruction stream; **a census of step constants cannot see this one.**

**Two divisor claims, each with its own control** — because the first pass at both was wrong:

- **My first check of id 231 truncated to 64 bits before a 64-bit shift** and reported "not 311". Redone
  correctly: `((v × 0x34AE820ED114942B) >> 64) >> 6 == v // 311` across sampled values, **and the same
  test against 312 fails.**
- **My first check of id 227 asked which divisor the magic `0x88888889` implies, and got "all of
  them"** — 15, 30, 60 and 120 all passed, because that multiplier is shared across `15 × 2^k` and
  **only the shift distinguishes them.** The shift is in the code and I had not read it: `sar edx, 5`
  with `imul eax, edx, 0x3c`. **Modulo 60.**

> A magic constant identifies a *family* of divisors. **The shift is the divisor**, and a check that
> does not read it will confirm whichever member the writer already had in mind.

**Also checked, prompted by the NUL-byte report:** all nine of my documents scanned for NUL bytes —
**zero**, with a positive control on a planted NUL. My first attempt at that scan was itself degenerate
— `grep -c $'\x00'` in bash becomes an **empty pattern** that matches every line, and it "found" 1506
hits in a 1506-line file. `file` still reporting `UTF-8 text` was what showed the count was nonsense.
All my documents are written with an editor rather than a shell heredoc, which is why they are clean.

**Gates:** links resolve (186 files, 8175 links); `verify_doc_addresses` returns only the expected
`001D4C1C`; consistency 0/0/0/0.

## CALL-CHAINS / ADDRESS-INDEX

```
001D1660 console dispatch   (arg1 rcx -> rdi, arg2 dl -> bl, arg3 r8b -> sil)
  -> 001D4C1C + (id-12)*4 -> + 0x00120000 -> arm
     ids 205..207     : toggle a byte, then one call carrying the value and an index
     ids 218, 219     : an accessor -> +0x4664, +0x4668
     id  217          : a getter/setter pair;  id 220 : passes -1/+1 to a call, no field
     ids 225..227,231 : widget state at rdi +0xDB4 .. +0xE30
  -> 001D4BFA  shared tail, and the target of 17 of this slice's ids
```

- `rdi+0xDB4` / `+0xDB8..+0xDD4` / `+0xDD8` — value, eight digits, cursor (id 225).
- `rdi+0xDE0` / `+0xDE4..+0xE00` / `+0xE04` — value, eight digits, cursor (id 226).
- `rdi+0xE0C` / `+0xE14` — sexagesimal value and its sub-field selector (id 227).
- `rdi+0xE2C` / `b+0xE30` — id 231's value (mod 311) and its coarse/fine modifier.
- `rdi+0xCF9`, `+0xCFA`, `+0xCFB`, `+0xD07`, `+0xE1C`, `+0xE1D`, `+0xE1E` — this slice's toggles.

---

# Block: developer tuning console, arm catalogue slice I (2026-09-03)

## COVERAGE

`arm-catalogue-slice-I-ids-268-293.md` — ids 268–293, **22 real arms, 4 unimplemented** (282, 286,
289, 290). Stamped against **GN159**. **218 of 282 ids catalogued across A+B+C+D+F+G+I. Only slice H
(ids 236–267) is outstanding**, plus E with another session.

| kind | count |
|---|---:|
| **property write through a setter** | **13** |
| boolean toggle on a local field | 4 |
| integer step / cycle on a local field | 4 |
| step through a getter/setter pair | 3 |

**Almost none of these arms stores to the object it edits.** They compute a value and call.

## OPEN-QUESTIONS

- **PROPOSED-repos78-19** — What is the object behind `01F82D20`? **Thirteen of its properties now
  have a number, a field offset, a bound and a step**; none traced to a reader. Largest identified
  structure the console touches and the best remaining thread.
- **PROPOSED-repos78-20** — What does id 277's second gateway do differently from the shared setter?
- **PROPOSED-repos78-21** — Are the fourteen cross-arm jumps shared tails by design, or the compiler
  folding identical epilogues?
- Properties **11, 14, 16, 19, 20, 21** are **unreached, not absent** — and **slice H is exactly the
  unread range that would hold them.** Recorded as unreached rather than filed as a gap question.

## AUDIT-LOG

**The property id is the field's dword index.** These arms load `01F82D20`, read a field, and call a
three-argument setter — `rcx` object, `edx` property number, `r8d` value:

```asm
001D4B52  cmp   dword ptr [rcx + 0x34], 1
001D4B56  lea   edx, [rsi + 0xd]        ; rsi = 0 -> property 13
001D4B60  call  <setter>                ; 0x34 / 4 == 13
```

| field | property | id | | field | property | id |
|---|---:|---|---|---|---:|---|
| `+0x0C` | 3 | 281 | | `+0x30` | 12 | 280 |
| `+0x10` | 4 | 272 | | `+0x34` | 13 | 281 |
| `+0x14` | 5 | 273 | | `+0x3C` | 15 | 276 |
| `+0x18` | 6 | 274 | | `+0x44` | 17 | 284 |
| `+0x1C` | 7 | 275 | | `+0x48` | 18 | 285 |
| `+0x24` | 9 | 278 | | `+0x58` | 22 | 271 |
| `+0x28` | 10 | 279 | | | | |

**Thirteen pairs, thirteen agreements, no disagreement.** Arms whose field read used an addressing
form my extraction did not capture were **resolved by hand rather than left in the denominator** — a
first pass reported "6 of 11", and five of those five "failures" were unmeasured, not contradicting.
**A ratio that mixes "contradicts" with "not measured" is not a measurement.** The rule was also
tested by pairing each setter call with the field read *live at that call*, not by matching the two
lists in aggregate, which would have agreed for the wrong reason.

**This is what slice D's pointer finding was for:** D established `01F82D20` is dereferenced by 18
arms and never nudged; **slice I holds fifteen of them and says what they do with it.**

**Fourteen arms in the table jump into another arm's interior.** Ids 276 and 280 are 21 and 18 bytes —
too short to contain a setter call. They set up the comparison and the property number, then
`jmp 0x1d4b59`, **into the middle of id 281's arm**, sharing its `setne` / call tail. Measured over all
227 arms with a jump that is not the common tail, not inside the arm's own extent, and not to another
arm's start:

```
14 of 227 arms end by jumping into another arm's INTERIOR
```

> **This is a limit of the model every slice in this catalogue has used.** Bounding an arm at the next
> arm's start extracts the right instructions, but for these fourteen the *behaviour* continues inside
> a neighbour. It is the `001D4BFA` lesson one level further in: the first rule was **"do not stop at
> the shared tail"**; this one is **"the arm's extent is not always the arm's behaviour."**

Both were caught because their byte counts were implausible for the work they had to do. **A body too
small for its job is a jump you have not followed.**

**Gates:** links resolve (188 files, 8194 links); `verify_doc_addresses` only the expected `001D4C1C`;
consistency 0/0/0/0; NUL scan clean with a planted-NUL control.

## CALL-CHAINS / ADDRESS-INDEX

```
001D1660 console dispatch   (arg1 rcx -> rdi, arg2 dl -> bl, arg3 r8b -> sil)
  -> 001D4C1C + (id-12)*4 -> + 0x00120000 -> arm
     ids 271..285 : *[01F82D20] -> read field N -> SetProperty(obj, N/4, value)
     ids 268..270 : their own getter/setter pairs, mirrored into d+0x10C4/0x10CC/0x10D0
     ids 287..293 : local fields and one global byte
  -> 001D4BFA  shared tail (ids 282, 286, 289, 290)
  -> 001D4B59  a SECOND shared tail, inside id 281's arm, reached by ids 276 and 280
```

- `01F82D20` — pointer to the property-bag object; **properties 3–22 map to fields `+0x0C`–`+0x58`.**
- `rdi+0x10C4`, `+0x10CC`, `+0x10D0` — mirrors written by ids 268–270.
- `rdi+0x10D4` — id 288, an **unbounded** counter.
- `rdi+0x10DC` — id 291, wraps 4 states; `b+0x10E0` — id 292; `b+0xC3D` — id 293.
- `01E02801` — global byte toggled by id 287.

---

# Block: gambits — Z-2 answered, Z-19 advanced (2026-09-03)

## COVERAGE

`09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md` **§8l appended**. No new document — the
existing one is the authority and its "Reopened" convention was followed.

**`check_already_answered.py` was run first and changed the target.** On the term `gambit` it returned
29 documents and 9 register rows; on my four candidate addresses it returned **exit 0**, and the useful
part was the *miss*: **`GambitRuntime_RebuildOrderSetForStatsRecord` (`00327DE0`) and
`GambitRuntime_RebuildOrderSetFromConfig` (`00328140`) are cited by no document at all.** The config →
runtime rebuild is what defines the record layout, and it was the one part of the chain nobody had
read. **The checker earned its place by telling me where the hole was, not by vetoing anything.**

## OPEN-QUESTIONS

**Z-2 — ANSWERED.** §8g identified the fields by use and said plainly *"byte offsets are still not
established."* They are now, from two directions that meet — the writer and the reader:

| offset | size | field | anchor |
|---|---|---|---|
| `+0x00` | `u16` | `wActionSelector` | the record pointer itself goes to `BattleData_ResolveWeightedId` (`00308EC0`) at `003014F6` |
| `+0x02` | `s16` | `wActionParameter02` | `movsx ecx, word [r14+2]` at `0030162F` — **signed**, unlike every other field |
| `+0x04` | `u16` | `wFlags` | `test word [r14+4], ax` at `003015A6`; walk's resume bits `test byte [rbx+4], 0x40`/`0x80` |
| `+0x06` | 3 × 6 B | `targetSelector0[]` | `lea rbp, [r14+6]` at `00301681`; bound `cmp ebx, 2` — **exactly three entries** |

**24 bytes exactly: 2 + 2 + 2 + 18.** The three-entry count is fixed twice independently — the
reader's loop bound, and the writer emitting exactly three triples.

**Z-19 — ADVANCED, and it removes a bit from the list.** `0x20`, `0x10` and `0x08` are **not three
independent flags**; they are **one three-bit field, one bit per target-selector entry**:

```asm
003016C3  mov  eax, 0x20
003016C8  mov  ecx, ebx        ; selector index 0..2
003016CA  sar  eax, cl         ; 0x20 >> i
003016CC  test edx, eax        ; edx = wFlags
```

§8g listed `0x20` among the five unknowns; it is the entry-0 bit. When bit `i` **and** bit `i+1` are
both set, **512 bytes** of candidate buffer are copied before the next entry runs — so the three
selectors execute **in index order, each narrowing the candidate set**, with the pair of bits deciding
whether the intermediate set is preserved. Remaining unknowns: `0x400`, `0x1000`, `0x4000`.

- **PROPOSED-repos78-22** — Which member of a 6-byte selector entry is `bSelectorOpcode`? One of the
  three is byte-sourced and two are word-sourced; the names from §8g are still unbound to offsets.
- **PROPOSED-repos78-23** — What writes `record +0x02`? The rebuild never does.
- **PROPOSED-repos78-24** — Each `0x170` order set holds **fourteen** 24-byte slots and the config
  supplies at most **twelve**. What, if anything, fills the other two?

## AUDIT-LOG

**What makes a gambit line dormant is not in the evaluator — a disabled line never becomes a record.**

```asm
0032817B  lea   rax, [rdx + 0x30]     ; rdx = the 12-slot config array
00328187  lea   r15d, [r12 + 0xc]     ; twelve iterations
003281A0  movzx eax, word ptr [rax]   ; the enable mask
003281A3  test  ebx, eax              ; ebx = 1 << slot
003281A5  je    0x32827c              ; disabled -> emit nothing
00328285  rol   ebx, 1
```

**12 config slots of 4 bytes** (two `u16`), and a **16-bit enable mask immediately after them** at
config `+0x30` — `12 × 4 = 0x30` — one bit per slot, walked with a rotating register.

> **A gambit line has three ways to be dormant and they are not the same thing:** its mask bit is
> clear (the player's on/off switch), its slot word is `0xFFFF` (nothing authored), or it is emitted
> and its condition never matches. **Only the third is visible to the evaluator.** The first two are
> gone before any condition runs, which is why a disabled line costs nothing per frame.

`r12d` counts emissions and `mov byte [r13], r12b` writes it as the **first header byte** — which is
the per-subgroup count §2's walk sums to find a subgroup's base. Two sections of the document, written
months apart, meeting on the same byte.

**Order sets:** `0x170` stride, table at `02089378`, indexed by the stats index at `[rcx+4]`.
`0x170 = 0x20 header + 14 × 0x18`. **Authored definitions** are reached through a descriptor at
`02EBF0D8`: `entry = resolve(desc+0x0C) + (id − 0x6000) × desc[+0x08]` — **slot word 0 is an id with a
`0x6000` base**, and the stride is data rather than a constant in the code.

**Bounded negatives kept as such:** `record +0x02` is *not written by this writer* (not "never
written"); the two spare record slots are *not filled from this path* (not "unused"); and which
selector member is the opcode is **not proven**, only that one is byte-sourced.

## CALL-CHAINS / ADDRESS-INDEX

```
GambitConfig_CommitBankAndRebuildRuntimeOrders
  -> GambitRuntime_RebuildAllOrderSets
     -> GambitRuntime_RebuildOrderSetForStatsRecord  00327DE0   (previously uncited)
        -> GambitRuntime_RebuildOrderSetFromConfig   00328140   (previously uncited)
           config slot i (4 B) + enable-mask bit i  ->  runtime record at set+0x20+n*0x18
BattleUnit_TrySelectAndCommitAiOrderFromSet 00305CC0
  -> AiOrder_EvaluateAndResolveActionTarget 003014C0
     -> BattleData_ResolveWeightedId  00308EC0   (record +0x00)
     -> AiOrder_EvaluateTargetSelector 00301AD0  (record, entry index 0..2)
```

- `02089378` — runtime order-set table, `0x170` per stats index.
- `02EBF0D8` — authored gambit-definition table descriptor (`+0x08` stride, `+0x0C` packed pointer).
- config `+0x00…+0x2F` — twelve 4-byte slots; config `+0x30` — the 16-bit enable mask.
- record `+0x00` `wActionSelector`, `+0x02` `wActionParameter02` (signed), `+0x04` `wFlags`,
  `+0x06` three 6-byte selector entries.
- `wFlags & (0x20 >> i)` — the per-selector-entry bit field (`0x20`, `0x10`, `0x08`).

---

# Block: the periodic combat tick, + a slice A correction (2026-09-03)

## COVERAGE

**New:** `10-Status-Periodic-Terminal/Periodic-Tick/what-the-periodic-tick-does.md`, GN159.
`verify_doc_addresses` verdict **ok** — 63 cited addresses, 14 entries / 48 interior / 1 data, zero
review flags.

**`check_already_answered.py` again found the gap rather than a duplicate.** `00310DB0`
(`BattleUnit_RunPeriodicCombatMaintenance`, 1,338 B — *the tick itself*), `00385570`, `00385CA0`,
`0030EA40` and `00300140` were cited by **no document**. The register's only hit, **AH-9**, is an
audit-pass row on the two-layer document, not an answer to any question in the brief.

## AUDIT-LOG — correction to slice A, and the join finding resolved

**`02CB8130` is a float in both slices. There was no contradiction in the data — my slice A row was
misleading, and the join was right to flag it.**

Re-read from the image: id 28's toggle is **`b+0xC72`**, a byte field of the settings object.
`02CB8130` is read and written with `movss` on both edges — id 28 **saves three floats into a save
area, zeroes them, and restores them** on the opposite edge. The row is corrected: not "nine fields",
but one toggle plus a **twelve-field save/restore area**.

**And the three floats it parks are `02CB8130`/`8134`/`8138` — exactly slice D's ids 108/109/110.**
The group is coherent: three tunable floats and one switch that stows them.

> **One trap recorded, because the width-from-the-store rule walks straight into it.** `001D194F` is
> `mov qword ptr [02CB8130], 0` — an **8-byte** store. Read as field width it says `02CB8130` is 8
> bytes wide. It is not: it is one instruction zeroing **two adjacent 4-byte floats**. **A store's
> width bounds the bytes touched, not the width of the field at its base address**, and a compiler
> merging adjacent zero-stores is the ordinary way that gap opens.

## OPEN-QUESTIONS

- **PROPOSED-repos78-25** — What is the field at `+0x28` that the periodic drain divides by −50?
  Without it the drain is "one fiftieth of an unnamed quantity".
- **PROPOSED-repos78-26** — Are stage 2's timers (`BattleFormula_AdvanceStatusTimersAndBuildResult`,
  935 B) the same timers stage 3 decrements, or a second set? **Not established** — both unread names
  say "timers".
- **PROPOSED-repos78-27** — Which global is at `01A78330`? It sets the drain interval for every
  periodic effect at once.
- **PROPOSED-repos78-28** — What is unit flag `0x40000000`, and what sets the tick deadline at
  `unit + 0xDD0`?

## AUDIT-LOG — the tick

**Poison damage is not a special path.** The tick zeroes a `0x148`-byte result record, fills it, and
hands it to **`BattleFormula_ApplyTargetResult` — the same function that applies a sword swing.**
Statuses ride the ordinary damage path; only the builder differs.

**`BattleFormula_BuildPeriodicStatusResult` is 83 bytes and a pure sequencer** — five calls, same two
arguments, fixed order, last one a tail call. **Every tick runs all five stages for every eligible
unit**; there is no per-status dispatch at that level.

**What ends a status — a countdown, one step per tick** (`00385570`, read in full):

```
test byte [.. + 0x68], dl    layer 0        both layers are consulted
test byte [.. + 0x78], dl    layer 1
movzx edx, byte [rec + 6]    timer slot;  0xFF = never expires
movzx ecx, word [unit + rdx*2 + 0x17c]     the live u16 timer
dec ecx                      ONE step per tick, no rate field
-> zero: append the status id to a list at result +0x3E
```

**Duration is entirely the starting value** — every timed status counts down at the same speed. And
**expiry does not remove the status here**: the id is collected and removal happens in the apply
stage, **which is why a status wearing off and a status being cured are the same code path.**

**The beat is a remainder test.** `interval = global(01A78330) × 30 / 3 = global × 10` ticks; the drain
lands only when the raw tick counter divides evenly.

**The drain divisors are negative.** `0xAE147AE1` with `sar 4` is `v / −50` and with `sar 5` is
`v / −100` — verified against integer division across ±20,000 values **with a failing control on 101**.
**The stored delta is a loss, not a magnitude signed later.**

**Refusal on application** (`0030E360`): two independent suppression gates stand in front of every
status, and the second refuses only when the status being applied is itself in the `0x80000003` set —
**an eighth sighting of that mask, and the first where it selects *which status* is blocked rather
than whether a unit may act.** A seventh sighting is in the tick itself.

## CALL-CHAINS / ADDRESS-INDEX

```
BattleUnit_RunPeriodicCombatMaintenance 00310DB0
  gates: [unit+0x698]; mode != 5|6; FieldRecordBit15; global + unit eligibility masks; qwFlags 0x1000000000
  expiry: GameClock tick >= [unit+0xDD0] -> clear flag 0x40000000
  -> BuildPeriodicStatusResult 00385DF0
       003848E0 InitializeResultRecord
       00386C70 AdvanceStatusTimersAndBuildResult      (unread, 935 B)
       00385570 AdvanceStatusLinkedAuxTimers           (the countdown)
       00385CA0 ApplyGlobalPeriodicDrainModes          (interval + drain)
       00386860 BuildRuntimeCounterPeriodicHpCredit    (tail call, unread)
  -> BattleFormula_ApplyTargetResult 003112F0          the ordinary action apply path
BattleStats_ChangeStatusAndProcessSideEffects 0030E360
  -> BattleTarget_HasLow16EligibilitySuppression  0030B9B0   refuse
  -> BattleTarget_HasHigh16EligibilitySuppression 0030B8E0   refuse if status is in 0x80000003
```

- `unit + 0x17C + slot*2` — the live `u16` status timers; slot index is record byte `+6`, `0xFF` = none.
- `unit + 0xDD0` — a tick deadline; passing it clears unit flag `0x40000000`.
- `01A78330` — the global that sets the drain interval (`× 10` ticks).
- result record: `0x148` bytes; `+0x24` and `+0x2A` deltas, `+0x2C` flags (`0x4000` = interval hit),
  `+0x3E` expired-id list, `+0x42 + slot*2` new timer values.

---

# Block: periodic tick stages 2 and 5, and the two suppression gates (2026-09-03)

## COVERAGE

`10-Status-Periodic-Terminal/Periodic-Tick/what-the-periodic-tick-does.md` **§13 appended**; two of
section 10's unknowns closed in place. 87 cited addresses, **zero review flags**.

## OPEN-QUESTIONS

**PROPOSED-repos78-26 — ANSWERED, and it corrects a working name.** *"Are stage 2's timers the same
timers stage 3 decrements?"* **No — stage 2 advances no duration timer at all.** Scanned all three
stages for the timer array, **with stage 3 as its own positive control**:

| stage | touches `0x17C` | word-array writes | accumulates result `+0x24` |
|---|---|---|---|
| 2 `AdvanceStatusTimersAndBuildResult` | **no** | none | **yes** |
| 3 `AdvanceStatusLinkedAuxTimers` | **yes** | `0x17C`, `0x42` | no |
| 5 `BuildRuntimeCounterPeriodicHpCredit` | **no** | none | **yes** |

**Stage 3 is the only decrementer of status durations in the pipeline.** The control is what makes the
two "no"s measurements: the same scan reports `0x17C` and `0x42` for stage 3.

> **`AdvanceStatusTimers…` is a misleading working name for that body.** It builds the HP delta. The
> name is GFZ type work and is left as-is, with a warning attached — **filing the question instead of
> assuming from the shared name was what kept this from becoming a wrong claim.**

**Gate question — ANSWERED.** `HasLow16EligibilitySuppression` and `HasHigh16EligibilitySuppression`
are **one shape on two halves of a packed 32-bit mask**:

```c
variant = (BattleTarget_ClassifyRelationshipClass(unit, other, 0) > 1);
g = ComputeGlobalEligibilityMask();  u = ComputeUnitEligibilityMask(unit, variant);
Low16 :  (g & 0xFFFF) || (u & 0xFFFF)
High16:  (g >> 16)    || (u >> 16)
```

**The tick tests `bx`/`ax` directly — the low half**, the same question `HasLow16` asks.

- **Constraint on Z-13, not an answer to it:** the variant argument is
  `BattleTarget_ClassifyRelationshipClass(...) > 1`, so **whatever values above 1 exist, this caller
  distinguishes only "1 or less" from "more than 1."** A second subsystem bounding Z-13 from outside
  the gambit document.
- **PROPOSED-repos78-29** — What are status bits `0x10`, `0x10000`, bit 16 and bit 28 named?
- **PROPOSED-repos78-30** — What do stage 5's two tables of **64-byte** records hold, and why is the
  default index `0x14`?
- **PROPOSED-repos78-31** — What is the `[rbp+0xBC8]` list stage 5 walks (count `+0xBC4`, stride
  `0x10`), and what does state value `8` from `002F8E90` mean?

## AUDIT-LOG

**Result `+0x24` is the HP delta accumulator** — section 5 recorded the drain writing it and could not
say what it was. **Stages 2, 4 and 5 all add into it; stage 3 never does.** Flag words are `+0x2C`
(2, 4, 5) and `+0x140` (2).

> **A caution recorded for anyone reading these bodies: `+0x24` appears on two different bases.**
> `[rbx+0x24]` / `[r13+0x24]` are the result accumulator; `[rsi+0x24]` / `[rdi+0x24]` are a field of
> the unit's stats block. **The same displacement on two structures inside one function is exactly the
> shape that produces a confident wrong reading**, and only the live register tells them apart. This
> is the same species as the `02CB8130` width trap earlier today — **a number that is right about one
> structure and wrong about the one you think you are reading.**

**Stage 5 refuses far more often than it fires:** a type byte selects a 64-byte record; a state must
equal exactly **8**; status bits `0x10` and `0x10000` block it outright; bit 16 and bit 28 each select
a different source quantity, **bit 28 doubling it**; and if the computed value already equals
`[unit+0x48]` it exits.

**Status bit 28 appears in stage 2 and stage 5 doing the same job in both** — selecting and doubling a
unit-stat-derived amount. **Two independently-read stages agreeing on one bit's role** is the strongest
result in this pass; the bit's name is still unknown.

**Gates:** 196 files, 8519 links resolve; consistency 0/0/0/0; zero address-review flags; NUL clean.

## CALL-CHAINS / ADDRESS-INDEX

```
stage 2  00386C70  reads [unit+0x3C] | [unit+0x64]; accumulates result +0x24; flags +0x2C, +0x140
stage 3  00385570  ONLY decrementer of unit+0x17C durations; expired ids -> result +0x3E
stage 4  00385CA0  interval global*10; delta result +0x24 (/-100) and +0x2A (/-50)
stage 5  00386860  64-byte record by type byte; state must be 8; blocked by status 0x10 | 0x10000
HasLow16EligibilitySuppression  0030B9B0 -> ClassifyRelationshipClass 0030AB40, masks 0030B770/0030B7F0
HasHigh16EligibilitySuppression 0030B8E0 -> same, high half
```

- result `+0x24` — HP delta accumulator (stages 2, 4, 5); `+0x2C`, `+0x140` — flag words.
- unit `+0x24`, `+0x48` — stats fields compared by stages 2 and 5 (**not** the result's `+0x24`).
- `0030AB40` `BattleTarget_ClassifyRelationshipClass` — reduced to `> 1` by both gates.

---

# Block: located-not-read, top three (2026-09-03)

## COVERAGE

**`0020AC30` is opened and off the list** — `18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md`
§11. It was cited by **nine documents, every one at its entry only**. `check_located_not_read.py` now
returns the other two and not this one.

**`002F7380` and `002AAE40` are opened but NOT written up, because they are not in my category.**
Findings are below for the owners to place — rule 3 says documents go under the category I was
assigned, and the coordinator's assignment was of *functions*, not of those folders. **Say the word if
you want me to write them where they belong and I will.**

**Extent checked first on all three, per the tail-call warning.** Disassembled from the image:
`002F7380` ends `ret` at `002F7652`, `002AAE40` ends `ret` at `002AB7C7`, `0020AC30` ends `ret` at
`0020AE6B` — **no `jmp` leaves any of their extents**, so the rendering hazard does not apply to these
three. Measured, not assumed.

## AUDIT-LOG — `0020AC30`: the engine reads meaning out of a bank's filename

**`AudioBank_SetSlotNameAndClassify(slot, name)`** — a setter for one of **five** named audio bank
slots that derives two booleans **by matching substrings in the name**:

```
"sum_"  found -> resolve a ".json" sidecar, then look for "0001" -> set flag A (01F832E8)
"sum_"  absent -> look for "spc_"                               -> set flag B (01F832E9), STICKY
```

> **The engine decides audio behaviour from the name of the bank, not from a field inside it.**
> Renaming a bank file changes what the engine does with it.

Three details that only a read produces:

- **An unchanged name is a no-op** — lengths compared, then `memcmp`, then a jump straight to cleanup.
  Re-setting the same name re-classifies nothing and clears no flag.
- **Flag A and flag B have different update rules in the same function.** Both are zeroed on entry, but
  B is written with `cmovne` **against its own current value** (sticky) and A only on the positive path.
- **`01DFE40C` is `-1` at rest.** It holds the slot index only during the call and is reset on *every*
  exit path. **Anything reading it from outside sees `-1`** — it is a "currently being set" indicator,
  not a record of the last slot.

**Not guessed:** what `sum_`, `spc_` and `0001` abbreviate. The evidence is that the strings are
matched, not what they stand for. Flags A and B are set here and **no reader was traced**.

## For the owner of `field-init-weather-to-legacyps2gs-rebuild.md` — `002F7380` (723 B, 10 docs)

Opened, mechanism only:

```asm
002F738E  mov  ecx, dword ptr [0209A6E8]
002F7394  add  ecx, 0x17
002F7397  shl  eax, cl                  ; mask = 1 << (global + 23)
...
002F74C9  test dword ptr [r9 - 0x11], esi   ; that mask, tested per record
```

**A global selects a bit position, and the resulting single-bit mask is tested against a per-record
flags dword** — a variant/permission selector driven by one global. Then two passes: the first walks
`[rdi+0x150]` records (`[rdi+0x224]` of them, **stride 0x60**) tracking a **maximum** via `cmovl` and a
**sum** via a `cmovne`-selected `4`-or-`n` increment, then hands both to `00467B10(max)` /
`00467B00(sum)` / `00467AA0()`. The second walks `[rdi+0x178]` (`[rdi+0x174]` of them) applying the
mask. **All seven callees are unnamed `FUN_`**, so what the max and sum are *for* is not established.

## For the owner of `numeric-formatting-and-character-mapping.md` — `002AAE40` (2440 B, 9 docs)

Opened, shape only: **505 instructions, sixteen distinct callees, each called exactly once** — a linear
builder or registrar rather than a formatting loop. Fifteen of the sixteen are unnamed; the named one
is `ImageAddress_ResolveRuntimePointer`. Almost no comparisons (`0x808080` twice, then `0xF`, `4`, `3`).
**A function of this size with no loop and no branching arithmetic is a sequence of one-time setup
calls**, and naming it needs the callees, not more of this body.

## CALL-CHAINS / ADDRESS-INDEX

- `0020AC30` — `AudioBank_SetSlotNameAndClassify(slot 0..4, name)`.
- `01F832F0` — five slot name strings, **32 bytes per slot**; `01F832B0` — per-slot dword, nonzero
  triggers a release before reassignment.
- `01F832E8` flag A (`sum_` + `0001`); `01F832E9` flag B (`spc_`, sticky); `01DFE40C` in-progress slot,
  `-1` at rest.
- `00905988` `"sum_"`, `00905990` `"0001"`, `00905998` `"spc_"`, `008FB2B4` `".json"`.
- `0209A6E8` — the global whose value + 23 is the bit position `002F7380` tests per record.

---

# Block: located-not-read, top three — WRITTEN UP (2026-09-03, addendum)

Rule 3 amended by the coordinator: **the person who read the function writes the document; the
category decides where the file goes.** All three are now written in place and **all three are off
`check_located_not_read.py`**:

| function | document | result |
|---|---|---|
| `0020AC30` | `18-Audio/.../how-a-sound-request-becomes-a-voice.md` §11 | the engine classifies audio banks **by filename substring** |
| `002F7380` | `03-World-Area-Field/Weather/call-chains/field-init-...md` | a **count → select → allocate** pass over field records |
| `002AAE40` | `16-UI/Text-And-Number-Rendering/numeric-formatting-...md` §11 | a **per-item SSE quad emitter**, not a registrar |

## AUDIT-LOG — a first-pass reading of `002AAE40` was wrong and was corrected before publication

I reported to the coordinator that `002AAE40` was *"505 instructions, sixteen distinct callees each
called exactly once, almost no comparisons — a linear builder or registrar."* **That was wrong, and
the document says so in its own words rather than quietly publishing the right answer.**

```
002AB67A  jmp -> 002AAFD2      a backward jump spanning almost the whole body
```

**Nearly the entire function is one loop, and all sixteen call sites are inside it.**

> **A count of call sites is not a count of calls.** "Sixteen callees, each called once" was a static
> fact stated as a behavioural one — **the same error shape as *45 call sites read as 45 arms***,
> arrived at independently and caught only by looking for backward jumps instead of trusting an
> instruction histogram.

The instruction mix is what the histogram reading missed: **`movups` 78, `movss` 50, `movaps` 34 —
162 of 505 instructions are SSE moves**, against 10 `cmp`. The low comparison count is not "no
branching logic"; it is float work. Per iteration it writes `1.0f` into two pairs of slots and computed
pairs into four consecutive floats — **the shape of a textured quad's corners** — and it saves `xmm9`,
`xmm13`, `xmm14`, `xmm15`, a register budget no integer formatter needs.

**And the chain does not bottom out:** `002AAE40` calls **`002AC5F0` (7,489 B)**, which is itself on the
located-not-read cut, cited by eight documents.

## AUDIT-LOG — `002F7380`

A **count → select → allocate** pass. `mask = 1 << (global(0209A6E8) + 23)` filters entries; three
passes over records (**stride 0x60**) and entries (**stride 0x30**) count references, select records
**referenced more than once while a budget lasts**, number them, and allocate `[rdi+0x218]` as
`count × 40` bytes zeroed, with `[rdi+0x228]` the count.

> **`word +0x0E` on a record is used for two different things in one function** — a reference counter
> in pass 2, then overwritten with a slot index in pass 3. **A reader arriving at pass 3 and calling it
> "the count" would be wrong**, and only which pass is running separates the two meanings. `word +0x0C`
> marks a continuation, so a reference counts against a whole run of records rather than one.

**All seven callees are unnamed**, so what the max and the sum *measure*, and what the 40-byte entries
hold, are filed as unknown rather than guessed.

**Gates:** 199 files, 8525 links resolve; consistency 0/0/0/0; zero address-review flags on either
document; NUL clean on both.

---

# Block: the `0x1B..0x27` band census, and `002AC5F0` opened (2026-09-03)

## COVERAGE

- `04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md` **§11** — the companion census to
  that document's `+5` census.
- `16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md` **§12** — `002AC5F0`
  opened; **off `check_located_not_read.py`**.

## AUDIT-LOG — the band is not a local convention: 26 sites, 22 functions

The coordinator reported the `0x1B … 0x27` test in `002F8060` and `002F8BB0` and asked for a third
sighting if my reads touched that byte. **They already had two of mine** — the periodic tick and the
status-application path. Scanning `.text` for the exact encoding `2C 1B 3C 0C`
(`sub al,0x1B ; cmp al,0x0C`):

| | |
|---|---:|
| occurrences | **26** |
| distinct functions | **22** |
| testing `byte ptr [<reg> + 4]` | **23 of 26**, on nine different base registers |
| preceded by a `[+5]` test within six instructions | **21 of 26** |

**The idiom is a two-byte discriminator, not a lone range check:**
`if (rec[5] == 0 && (uint8_t)(rec[4] - 0x1B) <= 0x0C)`.

Spread across spawn, rewards, stats, AI, action availability, the periodic tick and the formula layer.

> **Eight subsystems test the same thirteen-value band on the same byte under the same guard, and none
> of them says what it is.** Same shape as `0x80000003` — a set membership several questions consult.
> **Strengthens AL-2 and N-4 without answering either.**

**Recorded as not established:** any value's meaning, **and the polarity** — the sense differs by call
site (in the periodic tick the `ja` skips the guarded block), so a reader must check the branch at each
site rather than assume one direction. The existing document's `+5` census (104 sites, 82 functions)
is of a different quantity and is untouched.

## AUDIT-LOG — `002AC5F0` is the shared consumer at the bottom of the text path

**Extent first:** the function's **last instruction is a `jmp`** at `002AE32C` — but its target
`002ACFE7` is *inside* the body, a loop back edge. **That is exactly the distinction the tail-call
warning is about**, and it is why the target must be checked rather than the mnemonic.

Signature, established from writes rather than types:

```c
void FUN_002AC5F0(void *ctx, char **cursor, void *arg3, int *out)
{ *out = 0; if (**cursor == 0) return; ... }
```

- **`cursor` is a `char**` the function advances** — written back at **six** sites.
- **`out` is an `int*` status** — zeroed at entry, written at **ten** sites, `1` at five of them.

> **That is why seven functions call it.** Each hands over a cursor and a status slot and lets this
> function consume as much of the string as it handles. Every caller's loop is built around the cursor
> it returns.

1,658 instructions, **44 distinct callees over 108 call sites, 61 backward jumps, 212 `movups` + 99
`movss`, zero string literals** — the same profile as `002AAE40` one order of magnitude larger. Its
float constants (`0.25 0.5 0.65 1 3 -3 10 15 16.6 24 90 100 128`) are **layout quantities, not
formatting ones**.

**Scoped explicitly in the document:** 1,658 instructions were **surveyed, not decoded**. The status
values' meanings, the per-character dispatch across the 61 loops, `arg3`, and whether the
`002Axxxx`/`002Bxxxx` mutual recursion terminates on cursor progress or on `002AAE40`'s `0x14` counter
are all filed. **The section says in its own words that the text path is not now understood** — only
that its shared consumer has a signature and a caller set where it had an address.

## CALL-CHAINS / ADDRESS-INDEX

```
002A8C50 · 002A9F00 · 002AAE40 · 002AF340 · 002B1FB0 · 002B2150 · 002B5730
    -> 002AC5F0(ctx, char **cursor, arg3, int *out)      advances the cursor, sets a status
       -> the 0017Fxxx render API (8 small functions), 002B2150, 002B41F0, 002B43C0, 002A9F00
```

**The cluster is mutually recursive, not layered** — `002A9F00` and `002B2150` are both callers of
`002AC5F0` and callees of `002AAE40`.

---

# Block: cut entries `0022A0B0` and `007E5160` — two false positives of different kinds (2026-09-03)

## COVERAGE

Cut **15 → 13**. Both cleared, neither by the route expected.

- `00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md` — independent re-derivation + interior
  anchors for `0022A0B0`.
- `18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md` **§12** — `007E5160` opened.

## AUDIT-LOG — the cut has two distinct false-positive modes, and one of each fired

**`0022A0B0` — read thoroughly, cited only at its entry.** The memory-budget section of the boot
document already had **the nine ids, the nine sizes, the alignment tail, the two unregistered
allocations and the absent id 10.** I re-derived every one of them from the image before reading that
section, and they agree exactly.

> **The cure for this false positive is not to relax the cut; it is to cite the evidence the document
> already rests on.** Eleven allocation sites and nine registration sites are now cited, so each row is
> checkable rather than stated.

One method note: **two of the nine ids are computed, not literal** — `lea ecx, [r9 - 0xE]` and
`lea ecx, [r9 - 0xC]` with `r9 = 0x10` live — so **a scan for `mov ecx, <literal>` finds seven of
nine.** My first pass reported exactly that and was corrected against the disassembly.

**A cross-document link found in passing:** boot computes `2 / [01DFE0B4]` into `02064ACC`, and
`01DFE0B4` is the combat **time-base mode word** documented as Z-11. **The combat time base is read at
boot by a function outside combat.**

**`007E5160` — six citing documents, five of them table rows.** The vtable index lists it as
`Sd::Driver::RandomSound` **slot 43** — a row that *locates* the function and claims nothing about it.

> **The cut's "cited by N documents" is satisfied by an index, and an index does not lean on anything.**
> Different mode from `0022A0B0`'s. **Both of the cut's failure modes are now instances rather than
> predictions**, which is worth more to the instrument than either clearance.

**But the index row is what made it worth reading** — a class and a slot number beat an address.

**Slot 43 is a validation pass.** It walks the list at `this+0x30`, whose count is a **byte at `+5`**,
resolves a `u16` from each element, and on failure emits, from `01CB4D58`:

```
[sead][!!error!!]sequence NULL!! listaddr:0x%p
```

**The `sead` diagnostic layer is present and reachable in the shipped executable** — a retail build
emitting a formatted engine-error string on a data fault, message and `%p` argument both in the image.

**Explicitly not claimed:** the count byte at `+5` here is **unrelated** to the battle-record kind byte
at `+5`. Same offset, different structure, no connection asserted.

## CALL-CHAINS / ADDRESS-INDEX

```
0022A0B0  boot: 11 x 0036D240(size) -> globals 01FD49F0..01FD4A40
              9 x 00369D30(id, size, align)  ids 2,3,4,5,6,7,8,9,11   255.6 MiB
              2 / [01DFE0B4] -> 02064ACC     (the Z-11 time-base mode word)
007E5160  Sd::Driver::RandomSound slot 43
              list at this+0x30, count = byte [+5]
              element -> u16 [+4] -> 007CF9E0 resolve -> 007CF9C0 test -> 007BD240 report
              error descriptor 01CB4D58 = "[sead][!!error!!]sequence NULL!! listaddr:0x%p"
```

- `007CF9A0 / 9C0 / 9E0 / A30 / AC0` — a five-function container accessor family, 27–135 B, **all
  unnamed**, called 29 times from this one method.

---

# Block: cut entries `002ABF70` and `002350C0` (2026-09-03)

## COVERAGE

- `16-UI/Request-Router/ui-request-router.md` — `002ABF70` opened (genuinely unread).
- `05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md` — `002350C0` **re-derived and
  confirmed; a third false positive**, anchors supplied.

**Running tally of the eight cut entries I have examined: five genuinely unread, two already read
(`0022A0B0`, `002350C0`), one inflated by index citations but genuinely unread (`007E5160`).**
**Two in eight were already read to tier 1** — worth knowing when planning the remaining seventeen.

## AUDIT-LOG — `002ABF70` is a per-frame state step with an eight-mode jump table

122 instructions, **no loops**, five `ret` sites. Dispatches on the **low byte of a dword at
`this+0xB0`** through a jump table at **`002AC1B4` — four bytes past its own `ret`**, the same
construction as the developer console's dispatcher.

**Eight modes, six distinct bodies; modes 0/1/4 share one, and mode 6 is a no-op** that jumps straight
to the epilogue.

It steps a counter-animation block: `+0x90` current, `+0x92` previous, `+0x8C` target **clamped to
`0x7D00` = 32,000**, `+0xA0` signed step, `+0x9B` accumulator against **`0x1E` = 30**, `+0x9C` its
per-step increment, `+0x9D`/`+0x9E` a phase and its limit, `+0x88` a delay, `+0x5A` a countdown.

> **`+0xB0` is one dword carrying both the mode and flags.** The dispatcher reads it whole and then
> takes `cl`, so **a reader who treats `+0xB0` as a byte gets the right mode and silently loses bit
> 22** — which mode 2 is the only body to read. Same species as the `+0x24`-on-two-bases trap.

**Not claimed:** what the block belongs to. No caller traced, no allocation site found, so *what* is
animating toward a 32,000 ceiling is unknown. Also not claimed: that `0x1E` is frames — it bounds an
accumulator that grows by an authored per-step amount, so **it counts steps, not necessarily frames.**

## AUDIT-LOG — `002350C0` was already read, and my read adds nothing

Read from the image with no reference to the document. **The "Retirement — two opposite senses"
section is confirmed in full** — gate chain in order, both `bLifecycleMode` branches, the four-slot
focus loop, the squared comparison in each mode, and the three-step retire action. **Nothing was found
that the document does not already say**, including `g_flNativeLifecycleRange` and the per-unit
`flLifecyclePointThreshold`.

Ten interior addresses are now cited against the claims they carry, so each row is checkable.

**One detail added, consistent with the document's own note that the range is script-installed:**
`02089368` **is in the zero-filled tail of `.data` and has no value in the file.** A reader dumping the
shipped image sees `0`, not `43.0`. **That matters to anyone patching it statically**, and it is the
kind of thing only a from-the-image read surfaces.

**Two more `0x80000003` sightings** in this one function (`0023513E`, `00235239`), and **another
`bkbi[5] == 0` guard** at `0023511A`.

## FOR THE COORDINATOR — the encoding-hazard family

The `lea ecx, [r9 - 0xE]` finding belongs beside the `movss`-in-a-register and `mov edx, imm` cases,
and `_index/EVIDENCE-STANDARD.md` is yours to edit, not mine (rule 4). The three as a set:

| hazard | a scan keyed on | misses |
|---|---|---|
| constant held in a register | the memory operand of `addss` | slice F ids 173/174 |
| property id via `lea` | `mov edx, <imm>` | the `xor esi,esi` + `lea edx,[rsi+imm]` form |
| **heap id via `lea`** | **`mov ecx, <literal>`** | **two of nine ids in the boot table** |

**All three are the same shape: the operand is computed rather than encoded, and the scan reads the
encoding.**

---

# Block: `0025D9E0`, the field runtime pass (2026-09-03)

## COVERAGE

**New:** `04-Actor-Entity/the-field-runtime-pass.md`, GN159. 44 cited addresses (6 entry, 35 interior,
3 data), **zero review flags**.

**Pre-screened before opening, per the new advice, and it was worth it.** All four citing documents
cite `0025D9E0` from a **call chain or an ownership table** — *"runs the transaction, does not own
weather"*, *"a per-frame field pass"*. **Its role was known from the call graph and its body had never
been read**: a genuine unread, and a third shape distinct from the two false-positive modes — *edges
known, body unopened*.

**Placed in `04-Actor-Entity` because that is the owner the weather documents themselves assign it**,
not in the Weather folder where it was cited.

## AUDIT-LOG — an actor's script is driven repeatedly within one frame

```asm
0025DB43  call  WorldActor_UpdateRuntimeAndScriptExecutionState
0025DB4C  test  cl, 0x40      ; settled?      -> stop
0025DB51  test  cl, 0xf       ; work pending? -> no: stop
0025DB68  call  WorldActor_UpdateRuntimeAndScriptExecutionState   ; again, same frame
0025DB74  test  cl, 0x40 ; je 0x25db51                            ; loop
```

> **One actor is driven repeatedly inside one frame until it settles**, on bit `0x40` of the record's
> `+0x14`, or until its low nibble is clear. **There is no iteration cap in this function.**

That is why a scripted event can start, run several statements and reach a wait in the frame that
triggered it — **and it means a hook on the actor updater is called several times per actor per frame,
not once.** Anything counting frames from that callee is wrong.

**`byte +0x14` of an actor record has two independent halves** — bit `0x40` settled, bits `0x0F`
pending — both tested in the same instruction stream.

**Four loops, three shapes:** the uncapped drive loop; a **four-iteration pass with a rotating
single-bit mask** (`rol ebp, 1`); and **two full-actor passes bounded by `[rbx+0x20]`, each folding
every actor's `+0x14` into a running AND** — the second shifting right by 6 first, so it asks *"is bit
`0x40` set on every actor"*. **A whole-field settled test by conjunction, not by a counter.**

**Other facts a call-graph citation cannot carry:**

- **A save in flight stops the entire pass — and it still returns `1`.** A caller cannot tell "ran"
  from "declined because saving" by the return value.
- **`+0x11` bit 0 is republished from `+0x10` bit 7 every frame**, so a reader sampling one sees a
  stale copy of the other.
- **`02099D78` (the focus actor's registry entry) is legitimately null** on frames with no party
  focus — the null path is explicit at `0025DAA7`.
- Per-slot state is a **`0x288` = 648-byte block** based at `02098E10`.

**Control on the one absence claim:** *"no iteration cap on the drive loop"* — the same reading
positively identifies the caps on the other three loops (`cmp r15d, 4`, and two `cmp edi, [rbx+0x20]`),
so the drive loop's lack of one is a measurement.

**Not claimed:** any connection between the four-iteration rotating-mask loop and the gambit config's
enable mask. Same idiom, different structure, said so explicitly.

## FOR THE COORDINATOR — `check_source_hygiene.py` usage note

Run on my new document it printed **`no stray control bytes in 0 file(s)`** — a *file* path matched
nothing; it wants a directory. **The false clean was visible only because the tool prints its
population**, which is the project's own rule doing its job inside a checker. Re-run on the directory:
5 files, and 174 across the database, all clean. **Worth a line in its usage text**, because "clean"
and "scanned nothing" read identically to anyone not looking at the count.

---

# Block: `0030E130`'s side-effect half, and a consolidation (2026-09-03)

## COVERAGE

`10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md` **§11**. Cut 23 → 21.

**A fourth shape of cut entry: read for one purpose, rest of the body unexamined.** The document cites
*"complete body … tier 1"* and reads the bit arithmetic exactly right — but the function is named
`…AndProcessSideEffects`, and **553 bytes for `byteIndex = n >> 3` is a great deal of code.** The side
effects were nowhere in the document.

## AUDIT-LOG — status ids `0x68`–`0x71` change how many gambit lines a unit can use

```asm
0030E303  sub   r14b, 0x68
0030E307  cmp   r14b, 9
0030E30B  ja    skip                    ; outside 0x68..0x71
0030E30D  lea   edx, [rbx*2 - 1]        ; set -> +1, clear -> -1
0030E317  call  GambitConfig_AdjustAvailableEntryCountByStatsRecord
```

> **Ten consecutive status ids — 104 to 113 — each move the unit's available gambit-slot count by
> one**, up on set and down on clear. **Nothing else in the id space touches that counter.**

That is the mechanical join between the status system and the gambit config's **twelve slots and
16-bit enable mask**: these ten statuses move the *count of usable entries*.

**Two more behavioural facts the bit arithmetic alone does not give:**

- **Re-applying a status a unit already has is a complete no-op.** Each of the four modes aborts if the
  bit is already in the requested state — before the auxiliary update, before the transition result,
  before every side effect.
- **The layers gate side effects by their union.** After the write the function recomputes presence in
  *either* layer and stops if that did not change — so setting an id in layer 0 while layer 1 already
  carries it stores the bit and fires nothing. **A behavioural consequence of this document's own
  open question E-1.**

**And the same `0x148` record and the same applier again**: `memset(result, 0, 0x148)` → a builder
chosen **by function pointer with `cmovne`** (`00386AE0` on set, `00386A50` on clear) →
`BattleFormula_ApplyTargetResult`. **Status application, status expiry and the periodic drain all
converge on one applier.** The pointer pair also means **a scan for `call <literal>` finds neither
builder at that site** — the computed-operand hazard again, seventh instance, this time on a *call
target* rather than an argument.

## AUDIT-LOG — the three "0x10-stride" sightings are one structure

Raised as `+0x68`/`+0x78`, `+0x6B`/`+0x7B` and `+0x6E`/`+0x7E` across three subsystems. **They are the
same two layers.** Each layer is 16 bytes, so **every byte inside them is `0x10` apart by
construction:**

| offsets | byte of each layer | status ids |
|---|---:|---|
| `+0x68` / `+0x78` | 0 | 0–7 |
| `+0x6B` / `+0x7B` | 3 | 24–31 |
| `+0x6E` / `+0x7E` | 6 | 48–55 |

**One structure, three windows into it — not three structures sharing a stride.** And the arithmetic
pays out: a test of **bit `0x10` at `+0x6E`/`+0x7E`** is byte 6, bit 4, which by this document's own
`n >> 3` / `1 << (n & 7)` rule is **status id 52**. The affinity function's nested condition is
therefore *"does the target have status 52 in either layer"*.

## NOTE — `argscan.py` re-run does not apply to this session

I have never used `argscan.py`; all my extraction is my own capstone tooling. **And the specific idiom
it missed is one I handled explicitly**: slice I resolves `xor esi,esi ; lea edx,[rsi+imm]` by reading
the `xor` at each site, and the document says so. **No DYNAMIC verdicts of mine need re-checking** —
but that was luck of method, not foresight, and the hazard is now filed as its own family.

---

# Block: `0025DF00`, the wait resolver (2026-09-03)

## COVERAGE

`04-Actor-Entity/the-field-runtime-pass.md` **§11**. **The chain is now legible end to end:**

```
ActorManager_RunFieldRuntimePass 0025D9E0   drives one actor repeatedly until it settles
  -> WorldActor_UpdateRuntimeAndScriptExecutionState 0025DF00   decides whether it MAY run
       -> WorldActorScriptVM_InterpretBytecode 0025E4C0         runs it
```

**I put this entry on the cut myself** by citing it at its entry in §6 last block. Pre-screen: four
documents, four narrow purposes — the interpreter document records it as *"the interpreter's **exactly
one** ledger caller"*, a movement call chain lists it, and a cutscene document read it far enough to
see it *"gates the script stop marker"*. **Body never read.**

## AUDIT-LOG — it is a wait resolver, and that is why the drive loop terminates

Four wait kinds, all the same shape: evaluate; **if unsatisfied set `[rsi+0x14] = 1` and stop**; if
satisfied fall through. When nothing blocks, it publishes the record to a global and calls the
interpreter.

| condition | satisfied when |
|---|---|
| `ActorResource_FindActiveEntryByIdOrClass` | an entry exists (`!= 0xFF`) |
| `ActorResource_IsChannelBitActive` | the channel bit is set |
| `ScriptVM_WaitList_HasAnyActorChannelActive` | any channel is active |
| `ActorResource_FindScriptRequestEntry` | an entry exists — **and it is then removed** |

> **Each drive either resolves one wait or runs one bytecode step.** That is the mechanism behind §4's
> repeated driving, and it is why an actor can be driven several times in a frame and still stop.

## AUDIT-LOG — a same-displacement trap I nearly walked into myself

**`[rsi + 0x14]` in this function is NOT the actor record's `+0x14`.**

```asm
0025DFC6  lea  rsi, [rax + rcx*8]     ; an array element — not the record
```

`rdi` is the actor record; `rsi` is a **wait slot**. Both are read at `+0x14` in the same body:

| base | `+0x14` used as |
|---|---|
| `rsi` — wait slot | written `= 1` at **four** sites, one per blocking wait kind |
| `rdi` — actor record | tested `& 0x40` twice and `& 0x10` once |

**The four `= 1` writes are the obvious candidate for "what sets the pending bit §4 tests", and they
are a different structure.** Third instance of the `+0x24`-on-two-bases species — **and the first I
hit inside a function I reached by following my own citation.** Checking the base register before
believing the displacement is now something I do by reflex, and it paid here.

**A refinement to §4, not a retraction:** §4 reads the record's `+0x14` as bit `0x40` settled and bits
`0x0F` pending, which is what the *caller* tests. This function tests **`0x40` and `0x10`**, and
`0x10` is bit 4 — **outside the low nibble**. So the byte has at least three separately-tested
regions. **§4's reading stands; it was simply not the whole byte.**

**And one open item moved down a level rather than closing:** "can the drive loop spin?" — no cap in
the caller, **and none in the callee either**. The question is now whether a *bytecode step* can leave
work pending with the settled bit clear indefinitely. **The interpreter was not read**, and the
document says so.

---

# Block: `002A8C50`, the text markup parser (2026-09-03)

## COVERAGE

`16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md` **§13**. Cut 22 → 21.

**The bytes-per-line ranking worked on its first use for me.** `002A8C50` topped it at **1,121 B per
line of prose** — 3,363 bytes carrying about three lines across three documents — and the gap was
real: **it is the game's text markup parser and nothing said so.**

## AUDIT-LOG — text is variable-width, and `0x20` is the whole rule

```asm
002A8D8C  lea    rax, [rdi + 1]
002A8D90  add    rdi, 2
002A8D94  cmp    cl, 0x20
002A8D97  cmovae rdi, rax        ; >= 0x20 -> 1 byte;  < 0x20 -> 2 bytes
```

**A byte below `0x20` consumes two bytes of the string; `0x20` and above consumes one.** One `cmovae`
is the entire width rule. **Any tool measuring FFXII text length by counting bytes over-counts every
tag.**

## AUDIT-LOG — `0x0F` introduces a tag, and the tag character picks the field

| tag | char | writes |
|---|---|---|
| `0x2D` | `-` | `word [state+0x8E]` |
| `0x2F` | `/` | a magic-divide result; sets `byte [state+0xA0] = 1` |
| `0x23` | `#` | `word [state+0x88]` |
| `0x22` | `"` | `word [state+0x90]`, reading `[state+0x9E]` |
| `0x3B` | `;` | a 16-byte `movups` into the stack copy at `+0x40` |
| `0x70` | `p` | `dword [state+0xB0]` |
| `0x3D` | `=` | `[state+0xAE]` |

**Seven handled tags, seven distinct destinations.** `0x0E` is a second introducer with its own branch,
not followed.

**And a lookahead over a 64-bit character set:** `movabs r8, 0x4100400000000000` then `bt r8, rax`.
**Decoded by evaluating the mask, not by eye** — set bits **46, 56, 62** = **`.` `8` `>`**. The same
constant is loaded at two sites, so one set is consulted twice.

> **Three tag characters appear only in the lookahead and have no handler in this body** — recognised
> here, handled elsewhere. **Full vocabulary this function knows: `"` `#` `-` `.` `/` `8` `;` `=` `>`
> `p`.**

**The shape was the clue and is worth recording as a heuristic:** **208 `movups` against exactly one
backward jump.** That is not a processing pass — it is a large structure snapshotted to the stack,
modified, and written back. **A hook editing that structure mid-call is overwritten by the copy-back.**

**Bounded explicitly:** every written field is named by offset, **no consumer traced**; `0x0E` not
followed; and the `/` tag's magic divide is **not** claimed to be the `0x88888889` family — **the shift
was not read, and the multiplier alone does not fix the divisor.** That rule has cost this project once
already.

---

# Block: the Phyre class-registrar level, and a whole-image SSE census (2026-09-03)

## COVERAGE

`22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md`
**§11**. `005E5400` and `005AD8F0` cleared **as a pair**, with the framing that their rank was one
under-described document counted twice.

**Deliverables in my scratch, free to consume:**
- `Tools/work/h78/sse_loop_census.tsv` — all **38,161** functions: `entry, body_bytes, instrs,
  sse_moves, backward_jumps, name`. 2.8 s, zero unreadable.
- `Tools/work/h78/phyre_class_registrars.json` — **315** registrars → their schema strings.

## AUDIT-LOG — there is a class-registrar level above the field level

**`00639450` is the shared finaliser of class registration: 315 functions have `jmp 0x639450` as their
final instruction.** It is not a helper called from many places — it is a **common epilogue**, marking
the descriptor with `0x40000000` at `+0xFC` and conditionally self-linking an empty list at `+8`.

**This is the first time in my run the tail-call hazard actually applied**: both functions' last
instruction leaves the extent, and the target is its own 88-byte function. Every earlier case was a
loop back edge.

**Two populations, related and not merged:**

| | |
|---|---:|
| functions tail-calling `00639450` | **315** |
| of those, containing a `00632960` field call | **173** |
| `00632960` sites inside them | **593** |
| `00632960` sites outside them | **89** |
| `00632960` sites image-wide | **682** — **independently reproduces this document's figure** |

> **142 of the 315 registrars register no named field**, and **89 of the 682 registrations happen
> outside any registrar.** *"315 classes"* and this document's *"246 named classes"* answer different
> questions and must not be reported as one number.

**935 distinct name strings across the 315, 715 beginning `m_`; 112 registrars yield none.**

**The animation registrar's schema is an API, not a field table** — `playOnce`, `playLooping`, `stop`,
`setSpeed`, plus per-slot variants with explicit weight control. **That is the animation surface a mod
can drive, recovered by name.**

**And a counting trap inside the pair itself:** `005E5400` makes **18** field registrations across 20
`m_*` strings; `005AD8F0` makes **4** across 5, because most of its 29 strings are **method** names.
**Counting `m_*` strings and counting registrations measure different things** — both are in the
document's anchor table rather than one standing for the other.

## AUDIT-LOG — I created the read-but-uncited mode myself, and fixed it

After writing §11 the pair was **still on the cut**: the section cites their entries and the
finaliser's interior, but no interior address of either function. **I had produced the exact
false-positive shape I characterised two blocks ago.** Fixed by adding an anchor table — tail-jmp
sites, first/last `_Init_thread_header`, first/last field call, and named `lea` sites. Both cleared.

> **Citing an interior anchor is what clears a function from either list** — and the way to notice you
> have not is to re-run the check after writing, not before.

## NOTE — the census's population caveat

`movups`-only, `movups`+`movss`, and the full seven-mnemonic set are **different populations, not
different measurements**. My earlier hand counts of 208 and 311 are the narrow sets; the census's 225
and 336 are the full set; 162 vs 162 agreed because that count was already full-set. **None of these
pairs is a disagreement.**

---

# Block: `0035BC50`, and a correction to the alloca diagnosis (2026-09-03)

## COVERAGE

`00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md` — `0035BC50` opened,
cleared from the cut (interior anchors cited, per the new step).

## AUDIT-LOG — the frame is fixed; the "fifth instrument limit" is real but its cause was wrong

The handover reported the listing negating a helper's result into every stack reference, read as a
**dynamically sized frame**. From the image:

```asm
0035BC54  mov  eax, 0x1128     ; a COMPILE-TIME CONSTANT
0035BC59  call 0x808f10        ; _alloca_probe
0035BC5E  sub  rsp, rax
0035C03B  add  rsp, 0x1128     ; the epilogue — a LITERAL
```

**`_alloca_probe` with a constant size is MSVC's large-frame stack probe**, required for any frame over
one page. **Not `alloca`.** The literal epilogue and the fixed-offset stack cookie at `+0x1100` settle
it.

**Censused image-wide: 34 functions use the constant-size probe, 0 use a non-constant size.**
**This executable contains no dynamically sized stack frame at all.**

> **The consequence runs opposite to the warning.** The locals are not unreadable — they are at fixed
> offsets and the listing cannot prove it. The distortion is **cosmetic over an enumerable set of 34
> functions**, not semantic. **A reader who distrusts the frame size loses the function; a reader who
> trusts the listing loses only confidence.**

## AUDIT-LOG — and a stride correction the distorted listing would produce

The handover reported **four slots at stride `0x60`**. Measured:

```asm
0035BDB0  lea  rsi, [rdi - 0x60]    ; two cursors into the SAME slot
0035BE53  add  rdi, 0xc0            ; the stride
0035BE69  cmp  ebp, 4
```

**The stride is `0xC0`.** `rsi` and `rdi` are two views of one slot sixty bytes apart — **a listing
showing both invites reading their difference as the stride.** Slots are at `022C8080`, `022C8140`,
`022C8200`, `022C82C0`, with a parallel array of four resolved registry pointers at `022C8388` stride 8.

## AUDIT-LOG — the three questions answered

- **Which slot is selected:** the one whose **packed actor handle at `slot+0x04` equals the current
  party focus handle**. Pointer → `022C8078`, index → `022C8074` (both initialised to `-1`/0).
- **What the counters count:** `022C8068` counts slots **without** flags bit `0x40`; a second,
  register-only counter counts slots without `0x40` **and** without bits 1–2.
- **Which flag suppresses the pass:** **none singly.** Four independent gates refuse it — a predicate
  call, a flag byte bit at `022C83EC`, a mode word at `02092730` being `0x0B` or `0x18`, and bit
  `0x100` at `022C83E8`. **Two are per-mode, not per-flag**, so "which flag" had no answer as posed.

Full selection-state map (`022C8060`–`022C8078`) is in the document.

---

# Block: `BattleEncodedId_IsValidForClass` read (2026-09-03)

## COVERAGE

`02-Resource-And-Asset-Pipeline/authored-data-table-registry.md` — `00322C50` opened, cleared from the
cut. Placed in the **registry** document rather than the availability document that cites it most,
because the subject is the registry's slots.

## AUDIT-LOG — the class argument is a 32-way index into the registry

```asm
00322C5A  lea eax, [rcx - 1]      ; class - 1
00322C5F  cmp eax, 0x1f           ; classes 1..32
00322C72  mov ecx, [image + rax*4 + 0x203054]    ; jump table at 00323054
```

**Validity rule, from the shared tail:** `valid ⇔ 0 ≤ id < count`, where `count` is the dword at
**slot pointer + 4** — the same header field this document's §2 describes. **A null slot pointer
yields 0**, so an unloaded table makes every id invalid rather than faulting.

**Complete class → slot map for all 32 classes is in the document.** Sharing is real and asymmetric:
`02EBF110` serves classes 22–24, `02EBF068` serves 15/30/31, `02EBF138` serves 19/20, `02EBF038`
serves 25/32. **Class 13 is composite** — three slots and a `0x8000` constant. **Class 1 re-dispatches
via `00309440`**, the function's only loop.

## AUDIT-LOG — the registry's caution is sharpened, not overturned

That document says a slot listing this function as its only consumer is *"an id-indexed table and
nothing more"*, and deliberately leaves those slots unlabelled. **That was right on the evidence and
I have not overridden it.** What changes is that each slot now carries **a stable class number**, and
where a *second, independent* document records what its caller passes as the id, the pair identifies
the table:

| chain | conclusion |
|---|---|
| availability doc reads `IsValidForClass(0x14, actionId)`; class 20 → `02EBF138` | **indexed by action id** |
| spawn doc reads `IsValidForClass(0x17, i)` + selector lookup; class 23 → `02EBF110` | **indexed by definition selector** |
| two-layer doc §11 reads `IsValidForClass(0x1D, …)` gating status side effects; class 29 → `02EBF040` | **indexed by status id** |

> **Two sources per row — a class number from this function and an argument name from a document that
> read the caller.** That is a different and stronger thing than labelling a slot by a consumer that
> touches everything, which is what the caution warns against.

`02EBF138` is also one of that document's two named heavyweights at **128 referencing functions**, and
"the action-id table" is a plausible fit for that fan-in — **stated as a fit, not a proof.**

**Explicitly not claimed:** the contents of the other 26 slots. **A class number is an identity, not a
description.** And classes 22, 23 and 24 are treated *identically* here, so whatever distinguishes them
lives in their callers, not in this function.

---

# Block: `0030C650`, what a level-up actually does (2026-09-03)

## COVERAGE

**New:** `13-Rewards-Progression-Economy/what-happens-when-a-character-levels-up.md`, GN159. 45 cited
addresses, zero review flags. Cleared from the cut on the post-write re-run.

## AUDIT-LOG — all four questions answered

**1. Level IS stored, and this function is its writer.** The concern was that if it re-derived like its
caller, level would be an authority nowhere. It does not:

```asm
0030C7A7  movzx eax, byte ptr [rdi + 0x1c2]
0030C7B3  inc   eax
0030C7B8  cmova eax, ecx            ; cap 0x63
0030C7BB  mov   byte ptr [rdi + 0x1c2], al
```

**`stats + 0x1C2` is the level, one byte** — **and it is the same `+0x1C2` the foe-stat formula reads**
as the left half of `growth × (level − base) + base`. The byte this writes is the byte that decides how
strong a foe is.

**2. It cannot go down.** `cmp ecx, r14d ; jge return` at entry, and the loop only `inc`s. **A target
below the current level is a no-op, not an error and not a decrease.** Cap 99 is applied **twice** —
to the target on entry and to every increment.

**3. Stats are grown per level, not recomputed.** Six fields per iteration through three growth
functions; **four of the six are floats sharing one function**, differing only by which byte of the
character's growth record they read (`+0x1F`, `+0x22`, `+0x25`, `+0x28` — a packed array, stride 3).
**`BattleStats_RecomputeDerivedStateAndAutoStatuses` runs once, on the final level only** — a
four-level gain rebuilds derived state once.

**And the growth record comes from `02EBF130` indexed by the character id at `stats+4`** — which the
class map I read an hour ago assigns to classes 1 and 2. **That slot is the per-character growth
table**, identified by a second consumer rather than by the validator alone.

**4. The third argument is a silence flag.** `r13 = NOT(bit 1 of arg3)`, and the notification block is
gated on it *and* on being the final iteration. **Both known callers pass `0`, so both notify — they do
mean the same thing.** But the applier's value comes from a byte that can be `-1`, and **`-1` has bit 1
set, so that path is silent.** The flag suppresses the fanfare; stats are unaffected.

## AUDIT-LOG — a join with the audio boundary, neither read informing the other

```asm
0030C831  mov  ecx, 7           ; sound bank 7
0030C836  call 003A1180
0030C840  mov  edx, 0x40        ; pan
0030C847  lea  r8d, [rdx+0x3f]  ; = 0x7F, volume
0030C84B  call 002DF220
```

**`003A1180` and `002DF220` are the two audio-boundary functions I read for the BR-2/BR-4 block**, and
`0x40`/`0x7F` are the exact literals that document decodes — **centre pan** (`pan − 0x40` = 0) and
**full volume** (`127/127 = 1.0`).

> **Two documents, opposite ends of the engine, meeting on one call site.** The audio document derived
> what those constants mean from the mixer; this function is a caller passing exactly them for a
> level-up. **Neither read informed the other, and I did not go looking.**

**Control on the one absence claim** (*"nothing lowers a level"*): the same reading positively finds
the entry guard and the increment, and finds **no `dec` or subtracting store to `+0x1C2`** anywhere in
the fully decoded body.

---

# Block: `002A9F00`, where character advance comes from (2026-09-03)

## COVERAGE

`16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md` **§14**. Cleared from the
cut on the post-write re-run.

**Best-case pre-screen:** the document names it unread *and files the exact question* — *"advance
widths are not in this function; they come from `002A9F00`, which is unread."* **A named question
waiting on a named function.**

## AUDIT-LOG — the answer is a negative, and the useful kind

**There is no per-glyph width table.** The pen advances from **four spacing globals**
(`0209CC60/64/68/6C`) plus one scaled term, selected by a mode byte at `context + 0x10FC`.

**Every one of those globals is in the zero-filled tail of `.data`** — **no value in the shipped
image**, installed at run time. **A reader dumping the executable to find character spacing finds
zeros.** Same pattern as the spawn range and the console sliders.

> **Character advance in this game is not metric data attached to glyphs.** It is a handful of runtime
> constants and a scale, and which applies is a mode byte.

**Control for the negative:** the same reading **does** find a table read — `movsx rax, byte [rbp+7]`
indexing `00916560` — and follows it. The byte is **split into nibbles and OR-ed into a 64-bit GPU
command word**. **It selects a render mode, never reaches the pen.** So "no width table" is a
conclusion about where values *go*, not a failure to find a table.

**A running width budget:** `context + 0x10E4` is a float **decremented per character**, not an
accumulated total — a remaining-width budget. The body's only normalised comparison
(`divss` then `comiss 1.0`) is the natural wrap candidate; **what it gates was not followed** and is
filed.

## AUDIT-LOG — the tag set is shared, not local

`movabs rsi, 0x4100400000000000` appears here too — **the same character-set constant decoded in §13**
(bits 46/56/62 = `.` `8` `>`). **Three load sites across two functions**, so the tag class belongs to
the text subsystem rather than to the parser.

And this function opens by copying **`0x100` bytes of render state** to its frame in unrolled `movups`
pairs — the same snapshot-modify-write-back shape as `002A8C50` and `002AAE40`. **That is why all
three surface together on an SSE-density ranking: it is one idiom, not three coincidences.**

## NOTE — a provenance slip corrected in my own document

`what-happens-when-a-character-levels-up.md` §6 said the audio join was between documents *"read months
apart"*. **Both reads were this session, hours apart.** Corrected in place. It was a claim about
provenance, which is exactly the kind that gets quoted back.

---

# Block: `00261F90`, how the music changes when you change area (2026-09-03)

## COVERAGE

**New:** `18-Audio/how-the-music-changes-when-you-change-area.md`, GN159. 26 cited addresses, zero
review flags. Cleared on the post-write re-run. **Announced before starting**, per the new convention.

Four documents cited it as *"the Audio callee"* of the per-frame field pass and nothing more — the
**edges-known-body-unopened** shape.

## AUDIT-LOG — a per-frame call made into a transition handler by one bit

```asm
00261FA3  test byte ptr [rcx + 0x10], 0x40
00261FA7  jne  return                        ; already done
002620D5  or   byte ptr [rcx + 0x10], 0x40   ; latch, on the only completing path
```

**`context + 0x10` bit `0x40` is a done-latch, and nothing in this function clears it.** The field pass
calls this every frame; **the latch is the entire difference between a transition handler and a
per-frame one.**

## AUDIT-LOG — the save file can pin the music

```asm
0026201B  test  byte ptr [rax + 0x1063], 0x40
00262029  movzx edi, byte ptr [rax + 0x1534]
```

**When bit `0x40` of `payload + 0x1063` is set, the track id comes from `payload + 0x1534` and the
field-to-track mapping is skipped entirely.** That is **saved audio state, not a setting**, and it is
one byte.

Track selection has four sources in priority order: the saved override, the field-id mapping, and two
**hardcoded ids `0x5A` and `0x5B`** chosen by state predicates when the mapping is rejected. A
**per-track flag table at `022CBA50`, stride 2, bit 0** decides whether a mapped track is usable at all.

## AUDIT-LOG — the crossfade, and `0x7F` again

Three tiny helpers read in full: `002DEC00` (7 B) returns `dword [0215EF44]` — **the current track**;
`002DEE50` (27 B) writes a volume byte to `0215EF4D` and tail-calls the fader; `003614C0` (28 B) is a
**"start at full volume" wrapper with `r9d = 0x7F` hardcoded.**

**`0x7F` is the same full-scale constant the mixer boundary divides by 127** — third time this session
that constant has turned up from an unrelated direction. **`0x78` = 120 is the fade length**, and
**I did not claim it is frames**: 120 units of whatever the fader counts, with "two seconds at 60 Hz"
recorded as an inference rather than a reading.

**Failure is explicit rather than silent:** if no track is chosen and nothing is playing, the function
**clears bit 7 of `context + 0x17`** — it gives up on music for that transition rather than retrying.

**Control on the one absence claim** (*"no other literal track id"*): the same reading enumerates every
immediate in the 93-instruction body — `0x5A`, `0x5B`, `0x78`, `0x7F`, `0x40`, `0x80`, `1`, `4` — so
the zero is a measurement over a fully decoded function.

---

# Block: `0023B040`, party-control suppression (2026-09-03)

## COVERAGE

`15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md` **§10**. Announced before
starting; cleared on the post-write re-run.

**Placed in the capability document, not the battle-mode ladder that cites it** — that document already
knew `02089340 & 0x40` as *"a shared runtime/gameplay flag"* from a **different** consumer, so this is
the second consumer of a bit it was already tracking.

## AUDIT-LOG — the `0x40` bit is not one input among many; it is the mask's initial value

```asm
0023B056  and  al, 0x40
0023B058  neg  al          ; CF = bit set
0023B05A  sbb  esi, esi    ; -1 if set, 0 if clear
0023B063  mov  ebx, esi
```

> **Set means "start from fully suppressed", clear means "start from nothing suppressed."** The rest of
> the function refines that seed.

**And two more bits of the same word are read further in** — `test dword [02089340], 0x600`. **So
`02089340` carries at least three control-policy bits (`0x40`, `0x200`, `0x400`) where that document
knew one.**

## AUDIT-LOG — a three-bit mask with one bit inverted

| bit | consumer |
|---:|---|
| 0 | `PartyControl_SetMovementSuppressionBit` |
| 1 | `0026BD40`, **inverted** |
| 2 | `PartyControl_SetSuppressionMask1Bit` |

**Bit 1 is passed negated**, so a set bit means *permit* on that path and *suppress* on the other two.
**A reader assuming one polarity across the mask gets one of three backwards.** Same species as the
`+0xB0` mode/flags dword and the `+0x24`-on-two-bases trap: **the field is uniform, its interpretation
is not.**

**The tail-call hazard applies again** — the function's last instruction is `jmp 0x26bd40`, and
`0026BD40` is its own 10-byte function. Second genuine instance tonight.

## AUDIT-LOG — control suppression uses a wider status set than action eligibility

```asm
0023B166  and eax, 0x8800403b
0023B173  and edx, 0x8800003b
```

Both are **strict supersets** of the `0x80000003` predicate tracked across eight sightings:

| mask | extra bits over `0x80000003` |
|---|---|
| `0x8800403B` | 3, 4, 5, **14**, 27 |
| `0x8800003B` | 3, 4, 5, 27 |

**They differ from each other by exactly bit 14.**

> **The statuses that stop you *controlling* a character are a superset of those that stop it
> *acting*.** A unit can be eligible to act on its own and still refuse player input — the mechanical
> shape of *"I can't move but my gambits still run"*.

**That also reframes `0x80000003`**: it is not the status-suppression mask, it is **the smallest of at
least three nested ones**. Worth carrying into `PROPOSED-repos46-5`, which now asks *what set* rather
than *what state* — the answer is that there is a family of sets, ordered by inclusion.

---

# Block: the sound-trigger pair — four policies, one format (2026-09-03)

## COVERAGE

`18-Audio/Sound-Selection/sound-trigger.md` **§10**. `007E67C0` and `007E6360` opened **as a pair**,
both cleared on the post-write re-run. **Leaned-on cut now at 6.**

## AUDIT-LOG — the family has four selection policies over one descriptor format

| function | rule |
|---|---|
| `007BD370` | emit every entry |
| `007E58D0` | unconditional entries, plus **one** from a rotating pool |
| **`007E67C0`** | **emit entries whose `[low, high)` range brackets a queried float** |
| **`007E6360`** | **group consecutive entries by a key byte; report per group** |

> **The descriptor format is one thing and the selection policy is four.** Nothing in the list says
> which rule applies — **the policy is the function you call, not a field you read** — so a tool that
> dumps these lists cannot predict any of their behaviour without the caller.

**`007E67C0` — half-open interval, and the boundary rule is explicit.** `comiss low, v ; ja skip` then
`comiss v, high ; jae skip` means **`low <= v < high`**, so adjacent ranges tile without overlap and a
value exactly on a boundary belongs to the **upper** range. The query is fetched **once before the
loop**, so every entry is tested against the same number. Two accessors return the bounds and are
**used nowhere else in the family**.

**`007E6360` — run grouping, with a subtle index fixup.** Consecutive entries sharing a byte key form
a run; a resolve failure on the run's **leader** is reported for **every member**. The
`dec ebx` before breaking is what makes the outer loop resume *at* the run boundary —
**without it the first entry of every subsequent run would be skipped.** That is the kind of off-by-one
that would be invisible in a summary and produces a silent under-report in play.

**Not established:** what the query value is or its unit; what the key byte means; whether the four
policies ever apply to the same list. **The key byte in particular is named only by behaviour** —
`007CF9A0` returns one byte per entry and equality of that byte defines the run.

---

# Block: `0030CA80`, the commit-to-screen gate (2026-09-03)

## COVERAGE

`07-Combat-Action/Command-And-Action-Seam/native-command-seam.md` — `0030CA80` opened. **Leaned-on cut
now at 4** (from 23 when this block started).

It was the last unread link in the combat chain: commit writes the state, apply applies the result,
and nothing between them had been read.

## AUDIT-LOG — thirty-two 48-byte presentation slots, and a tolerant boundary

`022C17B0 + index * 0x30`, indices **0–31**. **An out-of-range index yields a null base rather than a
fault** (`xor ebx, ebx`), so the function proceeds on null — **a caller cannot distinguish that from a
legitimately empty slot.**

**The slot names an action:** `word [slot+0x1C]` indexes **`02EBF138`** — **third independent
confirmation** that this registry slot is action-id-indexed, from a consumer neither of the first two
touched.

## AUDIT-LOG — two questions, two channels

**The return value is "is the slot ready":** three separate dwords at `+0x10`, `+0x14`, `+0x18` must
**each equal 3**. Not a bitmask, not a counter — **three parallel sub-states that must all reach the
same value.**

**The out-parameter is "should it play":** the caller's flags can veto it (`& 0x3000`), and then a
chain of tests on the action record can restore it.

> **A slot can be *ready* and still not play, and the two answers travel on different channels.** A
> caller that checks only the return value gets a `true` that does not mean what it looks like.

## AUDIT-LOG — it splits a bit-pair another document reads as one

```asm
0030CB06  test dword ptr [02089340], 0x400   ; + a slot flag -> suppress entirely
0030CBAD  test dword ptr [02089340], 0x200   ; -> clear the out-parameter
```

**Tested separately, with different effects.** `PartyControl_RecomputeSuppressionFromLeaderBattleState`
tests them **together as `0x600`**.

> **Two consumers, one global, and the pairing is the caller's choice rather than the field's
> structure.** `02089340` now has four separately-observed policy bits, and **whether `0x200` and
> `0x400` are one policy or two depends on which function you read.**

That is the same species as the incomplete-population-of-sites entry — **a field whose shape looks
settled from one site and is not** — but from the other direction: there the two sites *disagreed* and
were both right; here they *agree* and one of them is coarser.

**Not established:** what the three dwords are or why `3` is ready; what `0x1000`/`0x2000` veto; what
distinguishes `0x200` from `0x400` — **only that this function treats them as different and one other
treats them as one.**

---

# Block: `00316A50`, the achievement counter updater (2026-09-03)

## COVERAGE

`20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md` **§10**. **Cut at 3.**

**Four documents cited `00316A50` — none of them the achievements document it belongs to.** Placed by
subject, not by citation.

## AUDIT-LOG — two authored tables, both shipped in `.rdata`

`00316A50(index 0..29, amount)`. Descriptors at **`00D10460`** (stride 8: `+0x00` type, `+0x02` mode,
`+0x04` threshold) and ids at **`00D10550`** (stride 4). **Thirty distinct ids spanning `0x01`–`0x1E`.**
Full 30-row table is in the document.

**Two paths, and only one reads the threshold:**

- **type `0`** — trigger path: test against the threshold (or an override from `003165C0`), then
  **`bts` a bit into a 30-bit bitmap at `+0x3844`** of the block `002536A0` returns, and notify with
  the id. **That is dedicated "already fired" storage, indexed by the same 0–29 index — bears on AB-4.**
- **type `2` / `4`** — accumulate path: saturating add clamped to **`0x7FFF`** / **`0x7FFFFFFF`**,
  and **it never reads `+0x04` at all.**

## AUDIT-LOG — AB-1 answered, as a negative

> **The eleven counter achievements have no threshold in this table.** The accumulate path never reads
> the threshold field, and every numeric-type entry's is `0` except one whose `16` is a **bit index**
> for a bitfield mode, not a target.

**Whatever decides a counter has reached its goal is not in this function.** AB-1 closes as posed and
reopens as *"who compares a counter against a target"*.

## AUDIT-LOG — two count-and-shape correspondences, deliberately not called mappings

**Eleven entries carry a numeric type**; §2 lists **eleven `ACH_COUNT_*`** counters.
**Ten entries share mode 7 with thresholds 0–9**; §2 lists **`ACH_SPECIAL_MONSTER01..10`**, *"a flat,
zero-padded run of ten"*.

> **No string in this table ties an index to a name.** Both are **count-and-shape matches, not
> identifications**, and the document says so. It makes **AB-7** much narrower — the ten differ only by
> a `0`–`9` parameter into one shared mode — without claiming which name is which index.

## AUDIT-LOG — a type caution I nearly got wrong

Three mode-2 thresholds are `810627072`, `1075331072`, `-1071661038`. **As floats, two are plausible
(`2.379`, `-2.496`) and one is not (`7.6e-10`).** I was about to call the field a float on the strength
of the first two.

**The code compares it with a signed-integer `cmp`** — order-preserving over float bit patterns only
while both operands are non-negative, **and one of the three has its sign bit set.** Type **not
established**, no reading asserted.

**That is the `0.00555556`/`1/180` lesson again:** the inviting interpretation fit two of three, and
the third is what stopped it becoming a claim.

---

# Block: `00198A00`, the rebinding conflict policy (2026-09-03)

## COVERAGE

`15-Input/Binding-Profiles/binding-profiles-remapping-and-control-state.md`. **Cut at 2.**

## AUDIT-LOG — the geometry is self-consistent to the byte

Three device classes with **16, 8 and 4** slots, at base offsets **0, `0x10`, `0x18`** — end to end,
no gap, no overlap. **16 + 8 + 4 = 28 = `0x1C`**, and the profile stride is **`0x70` = 112 = 28
dwords**. **Every number agrees with every other**, which is the strongest confirmation a layout gets.

## AUDIT-LOG — conflict detection crosses profiles

The scan bound is **`0x54` = 84 = 3 × 28**, walking from the class-0 base.

> **A key already bound in a different profile is a conflict.** The binding array is one flat 84-entry
> space and the search does not stop at a profile boundary — **the three profiles are not independent
> keymaps, they are three regions of one.**

## AUDIT-LOG — both remapping policies are implemented; the caller picks

| return | meaning |
|---:|---|
| `0` | assigned |
| `1` | **conflict, refused** |
| `2` | slot out of range for the class, **or the code is reserved** |
| `3` | device class `>= 3` |

**The sixth argument is a swap flag.** Clear → refuse. Set → **the two bindings trade places**
(target's old code into the conflicting slot, new code into the target). **Assigning code `0` clears
the slot** with no conflict scan at all.

## AUDIT-LOG — thirty-five unbindable codes, listed

Table at `01DF13E0`, **35 entries**, checked first; a match returns `2`:

```
02  51 52 54 55 58 59 5A  77 7A 7B 7D 82
83 84 85 86 87 88 89 8A 8B 8C 8D 8E 8F 90 91 92 93 94 95 96 97 98
```

**Twenty-two are the contiguous run `0x83`–`0x98`**; thirteen are scattered singles. **The dword after
the table is `0`**, so the bound of 35 is confirmed by the data as well as by the loop counter — two
independent confirmations of the same count.

**What the codes mean is not established** — this function only refuses them. Recorded as a list
because *"which inputs the game will not let you rebind"* becomes answerable the moment the code space
is named.

---

# Block: the last three cut entries (2026-09-03)

## COVERAGE

- `00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md` — `00313DB0`
- `99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-…md` — `00392A10` **and** `00392CE0`

**The original 23-entry cut is empty.** What remains is `002DC290`, which **my own citation put there**
— the third entry I have generated by opening something. **The cut is a frontier, not a backlog**, and I
have now demonstrated that from the inside three times.

## AUDIT-LOG — `00313DB0`: a 64-entry candidate ring, and one predicate used to revoke

**Circular queue**: head `022BEDA0`, tail `022BEDA1`, entries at `022BEDA4` stride 8, wrap
`and cl, 0x3f` — **64 slots**. Third genuine tail call of the night (`jmp 0x313a00`, a 289-byte
function).

**Every candidate popped is marked whether or not it is chosen** — `and ~0x1000` then `or 0x2000`.
**The mark records "considered", not "selected"**, and a unit rejected on the next test keeps it.

**And the `0x80000003` predicate appears in a new role.** On the select path a failure **`continue`s**
the loop — the cursor skips incapacitated units and keeps popping, and **the queue draining is what
ends it**. On the cancel path the same test **drops a selection already made**. **First sighting where
it revokes something already granted** rather than gating an attempt.

## AUDIT-LOG — `00392A10` / `00392CE0`: a byte one function discards and the other keeps

Both read the **same** rect-and-four-insets geometry, and both index three ways per axis. The
difference is colour:

- `00392A10` — **four `and …, 0xFFFFFF`**; the top byte of each colour dword is masked away.
- `00392CE0` — **no masks at all**, and it reads `byte [r8+3]` and `byte [r8+0xb]` **explicitly, into
  their own slots.**

> **The fourth byte of each colour dword is a real field, not padding.** One renderer extracts it and
> keeps it apart; the other discards it. **Neither function alone shows this** — the first could only
> say a byte was dropped; the second is what shows it was worth keeping.

That is the same shape as the `+0x10E4` resolution — **a field whose nature only appears once you have
two sites** — but arrived at deliberately this time rather than through a collision.

**And a capability call selects between the two renderers at run time**, which makes this the fourth
subsystem tonight where **the policy is the entry point, not the data**.

## NOTE — the cut as an instrument

Cleared 23 of 23 originals. Three further entries were **created by my own reads**, each time because
opening a function adds its callees at their entries. **A list that regenerates from being worked is
behaving correctly**; it should never be reported as a shrinking backlog.

---

# Block: `002DC290` — the shared emitter, and the cut reaches zero (2026-09-03)

## COVERAGE

`99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-…md`. **`check_located_not_read.py`
now reports 0 functions in the leaned-on cut** — including the three entries my own reads created.

## AUDIT-LOG — the quad emitter, and the colour question answered from the bottom

**Eleven callers across seven address neighbourhoods**, including both renderers above. It emits **one
four-vertex quad** into a ring of command buffers:

| vertex | colour dwords | position dwords |
|---:|---|---|
| 0 | `+0x50 +0x54 +0x58 +0x5C` | `+0x60 +0x64 +0x68` |
| 1 | `+0x70 +0x74 +0x78 +0x7C` | `+0x80 +0x84 +0x88` |
| 2 | `+0x90 +0x94 +0x98 +0x9C` | `+0xA0 +0xA4 +0xA8` |
| 3 | `+0xB0 +0xB4 +0xB8 +0xBC` | `+0xC0 +0xC4 +0xC8` |

**Sixteen bytes read from argument 3 — offsets `0`–`15` — each widened to its own dword.** Four bytes
per vertex, four vertices.

> **So the fourth colour byte has a destination: `+0x5C`, `+0x7C`, `+0x9C`, `+0xBC`.** The question the
> two renderers posed is answered from the bottom — **the slot exists in the command either way, and
> one renderer deliberately zeroes it while the other fills it. Masking is a choice about what to send,
> not a discard of something the format cannot hold.**

**Three functions now agree the byte has a slot, and none of them says what fills it with meaning.**
That is a sharper open question than the one this family started with.

**Also:** `dword [0215E6D0] == 0` makes this function emit **nothing at all** — a global draw
kill-switch, with no writer identified here. And the submit advances the ring cursor by the bytes
written, **16-byte aligned**, over a **24-byte buffer descriptor** whose cursor lives at `+8`.

## NOTE — the cut, closed

**23 originals cleared, plus 3 entries generated by my own reads, plus this one. Zero remain.**

**A frontier that empties is a different event from a backlog that empties**, and the distinction is
worth keeping in the record: **every one of the last four entries existed because opening a function
cites its callees.** The list stopped producing new entries only when the chain reached a function
whose callees were already cited elsewhere — **which is what "closed" means for an instrument like
this**, not that nothing is left unread in the binary.

---

# Block: three read-but-uncited entries cleared with anchors (2026-09-03)

## COVERAGE

`00-Engine-Core-Runtime/Developer-Tuning-Console/what-the-console-tunes.md` — two sections adding
interior anchors for **`001F0AD0`, `001EF6D0` and `0018A120`**. All three now clear both lists.

**Not fresh reads — re-derivations against claims that document already makes**, which is the correct
treatment for the read-but-uncited mode. **Every figure agreed.**

## AUDIT-LOG — `001F0AD0`, four true numbers over four populations

| claim | re-derived | |
|---|---|---|
| **144** `movss` stores | **144** `movss` with a memory destination | ✔ |
| writes `+0x190…+0x44F` of the `02CB7FD0` block | span `02CB8160`…`02CB8404`, and `02CB7FD0 + 0x190 = 02CB8160` | ✔ |
| **8 × 64 B** matrices | **128 stores** in `02CB8160`–`02CB835F`, **exactly 16 per block** | ✔ |
| writes the block wholesale | **150 of 155 gaps between targets are exactly 4 bytes** | ✔ |

**A population note, since two counts differ and neither is wrong.** The document says *144 of 154
accesses*; the SSE census says **260**. The census counts **all seven SSE mnemonics in both
directions** — this body also has 96 `shufps`, 59 `movaps`, 44 `movups` — while 144 is specifically
**`movss` with a memory destination**. Plus **13 `movss` loads** and **156 distinct rip-relative write
targets**. **Four different true numbers over four different populations**, now stated together so the
next reader cannot pick one and call the others wrong.

## AUDIT-LOG — `001EF6D0`, four claims and one refinement

Stride `0xD8` at `001F04A8`/`001F04CE`; loop bound `[rbx+0x13C]` at `001F04DF`; the argument
`i*0xD8 + 0x150 + object` built across `001F04A8`–`001F04B9`. **All confirmed.**

**Refinement:** the document says *"virtual slot `+8` called after each parameter write"* — there are
**three such call sites** (`001F0470`, `001F0482`, `001F04A2`), not one. **The claim is right; the count
was never stated.**

## AUDIT-LOG — `0018A120`, and a default that is not a skipped write

```asm
0018A13C  movaps xmm0..xmm3, four constant rows      ; loaded FIRST
0018A158  test   rax, rax                            ; the source pointer at +0xB0
0018A15B  je     keep_the_constants
```

> **The four constant rows are loaded before the null test, not after it.** A source object with a null
> `+0xB0` yields them unchanged — **a missing matrix is a defined result, not a skipped write.**

The populated path gathers `+0x00 +0x04 +0x08 +0x0C +0x10 +0x1C +0x20 +0x2C` into non-adjacent stack
slots — **a transpose, not a copy.**

## NOTE

**Three read-but-uncited entries in one document** is the strongest evidence yet that the mode is a
property of a *writing habit* rather than of any instrument: the same author, the same document, three
functions read in detail and none cited internally. **The fix is per-claim anchors, and it is cheap
enough that it should be a step rather than a cleanup.**

---

# Block: `001FB120`, CharacterRenderObject slot 13 (2026-09-03)

## COVERAGE

`17-Presentation-Rendering/Character-Rendering/character-render-object.md` — slot 13 read. The slot
table listed it with an **empty description column**; it now has one, with anchors.

## AUDIT-LOG — character transforms are double-buffered

```asm
001FB1AC  call  0x189120
001FB1B1  cmp   byte ptr [rax + 0x1c], 0
001FB1BA  je    bank_A
```

| | scalars | three 4×4 matrices |
|---|---|---|
| bank A | `entry + 0x08`, `+0x10` | `this + 0x4C4` … `+0x583` |
| bank B | `entry + 0x0C`, `+0x14` | `this + 0x584` … `+0x643` |

**`0x584 − 0x4C4 = 0xC0` = exactly three 64-byte matrices**, so the banks are contiguous, equal and
adjacent — and the scalar slots are **four bytes apart** in the same pattern. **The geometry proves the
double-buffering; no flag or name says it.**

> **Everything this slot publishes exists in two copies, and which is "current" is one byte reached
> through a shared accessor — not this object's decision.**

## AUDIT-LOG — two smaller things worth carrying

**An enable gate that preserves rather than clears:** `byte [this + 0x4B4]` clear means the function
writes **nothing at all** — **both banks keep their previous contents.** A reader expecting "disabled →
zeroed" would be wrong.

**A NaN takes the non-zero branch.** Two float arguments are tested against zero and a flag is set only
when **both** are zero, but the `jp` guards mean **an unordered comparison falls to the non-zero path**.
So the flag reads "definitely both zero", not "not non-zero" — **the distinction only exists because
the parity flag is checked.**

The two flags are stored through a **double indirection** — `[entry+0xE0]` and `[entry+0xE8]` each
yield a pointer whose `word +0x10` indexes off a base in `r9` — **so they land in a third structure,
not in the entry.**

**Entry array:** `[this + 0x58] + index * 0x318`.

## NOTE — this is what the SSE column is for

48 `movups` in 105 instructions with **zero loops** is the snapshot-and-publish shape the column ranks
on, and it was right: **a fully unrolled triple-matrix copy into one of two banks.** The column found a
function whose own document had an empty description cell for it — **neither the citation graph nor the
bytes-per-line ranking would have surfaced an empty cell**, because the row existed.

---

# Block: the pair frontier's first result — `002AF960` (2026-09-03)

## COVERAGE

Two censuses delivered to the coordinator, both in `Tools/work/h78/`:

| file | rows | what it finds |
|---|---:|---|
| `rip_data_refs.tsv` | **164,489 sites**, 35,879 addresses | **shared globals** — 11,694 touched by ≥2 functions |
| `struct_offset_refs.tsv` | **24,100 sites**, 3,911 displacements | **shared structures** — 1,135 touched by 2–6 functions |

**Control on the first:** `01F82D20` → **157 sites, 156 read, 1 write**, agreeing with my earlier
displacement scan **and** the settings document's independent figure. **Three-way.**

**And a correction the coordinator needed before building:** the case that motivated the frontier,
`+0x10E4`, is **not rip-relative** — both sites are `[reg + disp]`. **The ranking as specified would not
have caught its own motivating example.** Hence the second census.

## AUDIT-LOG — the pair census paid on its first query

`0x10E4` has **three** touchers: `002A9F00`, `002AC5F0` — the two that were compared after a
collision — **and `002AF960`, which nobody had opened.** Read here.

**`+0x10E4` now has three roles in three functions and the lifecycle is closed:**

| function | role |
|---|---|
| **`002AF960`** | **initialises it: `(float)byte[src+0x9D] × float[src+0x50]`** |
| `002A9F00` | **decrements it** once per character |
| `002AC5F0` | **multiplies by it** and compares |

> **A count times a per-unit scale, spent one character at a time, read as a multiplier while it
> lasts.** The initialisation settles the interpretation: **it is a budget**, and the multiply is a use
> of *how much is left* rather than an independent scale.

**Previously answered as "one field, two roles, two functions" after two readers compared notes.** The
third site was found **by census rather than by collision**, and it supplies the origin neither of the
other two could. **That is the pair frontier doing exactly what it was proposed to do, on its first
query.**

**It also closes the third leg of that document's open question** *"what `002AC5F0`, `002AAE40` and
`002AF960` draw"* — **this one does not draw.** It zeroes the batch counter, sets the budget, copies two
words, and brackets the run with two `RenderCommand_SubmitCurrentBufferAndSwap` calls. It is the open
and close of a text run.

## NOTE — a caveat that travels with the second census

**A displacement is only meaningful within one structure type**, and the census cannot know whether
`[rdx+0x10E4]` and `[r8+0x10E4]` are the same field. **The `≥0x400` filter plus a 2–6 toucher band is
what makes it a candidate generator rather than a claim** — the same status as bytes-per-line, not as
the vendor tag. **It earned its first candidate; it has not earned trust in a row.**

---

# Block: `+0x06B5` answered, and a defect in my own census (2026-09-03)

## COVERAGE

New document: **`09-Combat-AI-And-Gambits/which-gambit-set-fires-and-how-a-command-switches-it.md`**
Three functions read: `00305AB0` (517 B), `002FDDA0` (1937 B), `00236A60` (452 B). Gates clean.

## AUDIT-LOG

**`+0x06B5` is the gambit walk's `subgroup_index`.** The gambit document names that parameter in
`BattleUnit_TrySelectAndCommitAiOrderFromSet`'s signature and never traces it to a source, because
the source is in the tail of `00305AB0` — a function that document listed as **"not read"**.

**First, the check your caveat demands.** The three touchers do hold the same pointer: each takes it
as arg 1 (`00236A72`, `002FDDAD`, `00305ABE`), and `+0x698` q, `+0x6B5` b, `+0x6E0` q agree in
width across all three. Corroborated twice more: the callee that receives SelectCommit's pointer
reads `+0x698`/`+0x708`/`+0x714` at the same widths ExecDirect uses, and Reset calls `003105D0`
with arg 1 unchanged, which writes `+0x6B4`/`+0x6B6`/`+0x6B7`.

**Findings:**

- **A unit tries four order sets in a fixed order**, not one. Only attempt C uses the selected
  subgroup; A, B and D force 0.
- **A failed attempt B skips C entirely** (`00305C32 jmp 0x305c61`). A unit whose third set exists
  and fails **never consults its selected subgroup that decision.**
- **`subgroup = (id & 0xFF) - 0x16`** for the twelve command ids `0x4116`-`0x4121`, mapping onto
  subgroups **0-11**, no gap, no overlap.
- **Order sets are 32-bit RVAs in an authored directory** at registry slot `02EBF168`, resolved by a
  three-instruction function against a base at `01F83530`.
- **Two order sets are compiled into the image** (`01EEC320`, `01EEC370`) and **decode exactly under
  the header/record layout the gambit document derived from code alone** — `0x50` is `0x20 + 2*0x18`.
  Independent confirmation from data the code never describes.
- **Nothing leaves a unit without a decision**: all four failing commits a static record, action
  `0x4021`.
- **`002FDDA0`'s full dispatch map**: 249 ids, 25 arms, three jump tables.

**Two things for the registers, which I did not edit:**

- **Z-9 "What distinguishes subgroups within one order set" is ANSWERED at the mechanism level** —
  a per-unit byte set by twelve commands. What each subgroup *means* in authored data stays open.
- **Z-14: `0x414D` is not handled by this dispatcher.** It falls in the `4149-4157` gap and reaches
  the arm that returns `-1` without writing `+0x6B4`.

## NOTE — a defect in `struct_offset_refs.tsv`, and what it is worth

**2,102 of its 24,100 rows are not struct offsets.** They are `[reg + reg*scale + huge_disp]` where
the base register **holds the image base** — the same idiom as the console dispatch table. The
displacement is an **RVA**, not a field offset.

**This was live in the ranking:** the row printed as `01E632B0` is really the global `01F832B0`.
Not junk — but wrong by `0x120000`, and in the wrong list.

**Verified, not assumed:** of the 617 functions carrying such a row, **607 contain a proven
`lea reg, [rip] -> 00120000` in the same body.** 10 do not; their base value is unestablished and
they are flagged `no` in the new file.

**Two replacement files in `Tools/work/h78/`:**

| file | rows | what it is |
|---|---:|---|
| `struct_offset_refs_clean.tsv` | 21,998 | the struct census with the RVA class removed |
| `imagebase_rva_refs.tsv` | 2,102 | that class, **resolved to absolute**, with a `base_proven` column |

**And the class is worth having on its own.** Its 1,209 distinct addresses versus the rip census:
**186 already known, 1,023 new — 84.6%.** The rip-relative census was blind to them because the
base is in a register rather than `rip`. Distinct globals: **35,879 → 36,902.**

> These are exactly the addresses reached by dispatch tables and big authored data, so the class the
> first census missed is the class most likely to be a table worth naming.

**One correction inside this block.** My first reading of the class was **"rip-relative leaked in"**,
and it was wrong — I disassembled a site before sending and found `[r10 + r14 + 0x1b9a340]`, a base
*register*. **And the first overlap number I computed was `0` new out of `0` known**, because the two
files write addresses differently (`0x`-prefixed here, bare hex there) and my filter silently matched
nothing. Both numbers above are from a re-run carrying **two positive controls**: the rip census
reports its expected 35,879 distinct addresses, and `01F82D20` is present in it.

---

# Block: `+0x06B7` — the combo progress counter, and a correction (2026-09-03)

## COVERAGE

New document: **`07-Combat-Action/how-a-combo-continues-and-what-it-blocks.md`**
Two functions read complete (`0030FA00` 146 B, `0031B860` 83 B, `003272A0` 55 B); sites read in
context in `003105D0`, `00325D90`, `0023B040`, `00385680`, `00388660`. Gates clean; 72 addresses
cited, 0 needing confirmation.

**`0030FA00 BattleAction_TryContinueComboSequence` and `00325D90 BattleUnit_CanAdvanceCombatNavigation`
were both undocumented.**

## AUDIT-LOG

**`+0x6B7` is the combo progress counter — how many hits of the current combo have been committed.**

**Pointer identity first.** Four of the six take the unit as arg 1 and touch `+0x698`, `+0x708`,
`+0x714`, `+0x6B4` alongside it. The other two get it from a getter, and that getter proves the type
**by construction**: `BattleStats_FindOwningBattleUnit` walks the slot pool and returns the unit
whose **`+0x698` equals the argument** (`0031B888`-`0031B899`). The value is a BattleUnit because it
came out of `BattleUnit_GetBySlotIndex` — not because of its name. **It also identifies `+0x698` as
the unit's stats pointer**, from the opposite direction to the gambit cascade.

**The mechanism:**

- **A combo re-commits the same action.** `0030FA00` reads `+0x708`, `+0x714`, `+0x710` and calls
  `BattleUnit_CommitAction` with all three unchanged; **only on success** does it `inc` the counter
  and set `+0x6B4 = 5`.
- **The length is rolled once, on hit 1**, and stored in the high nibble of `record + 0x12`.
- **Hits 2..N do not roll.** They compare the counter against that nibble: `>=` ends the combo,
  `<` sets the continue bit.
- **A non-zero counter blocks combat navigation** (`00325DE6`, unconditional `return 0`) and
  **overrides party-control suppression on the leader** (`0023B12D cmova`, discarding flags
  accumulated above it).
- **`+0x6B7` and `+0x6B8` are cleared by a single `word` store** at `003106EB` — the width trap: it
  bounds bytes touched, not field width. Every other access is byte-wide.

## NOTE — a correction to `08-Combat-Formula/combos-and-the-guard-parry-flag.md`

That document reads the branch correctly and **attributes the byte to the wrong object**:

> *"If the source's **record byte** `+0x6B7` is non-zero, no roll happens at all... A forced combo
> count is a field, not a special case."*

In `00388660` the record is `rdi` (`0208D480 + kind*0x40`, built at `003886A7`-`003886B6`) and the
unit is `rax` (`00388679`-`0038868A`). **The gate reads the unit; the stored nibble reads the
record.** `+0x6B7` is a **runtime field** written only by the combo continue path and the action
reset. **There is no forced-value path and no authored field** — the roll is skipped on later hits
because the count was already decided on hit 1. **The suppression is memoisation, not an override.**

That distinction is not cosmetic: an authored record byte would be a per-action designer knob; a
runtime counter cleared by the action reset is not patchable the same way.

> **Their own falsification entry is why this was correctable rather than load-bearing.** They
> wrote *"nothing here says who writes `+0x6B7`"* and left it open. **The uncertainty was marked in
> exactly the right place.**

## NOTE — `+0x6B4`, now constrained by three documents

`0` from the action reset, `2` from all 25 arms of the direct-command dispatcher, `5` from the combo
continue path, and compared against `9` in party control. **At least four reachable values, no
document has read what any of them mean.** Recorded as an observation because three separate reads
now bound it.

---

# Block: anchoring my three documents — and what anchoring found (2026-09-03)

## COVERAGE

| document | before | after |
|---|---:|---:|
| `04-Actor-Entity/the-field-runtime-pass.md` | 10 | **0** |
| `02-Resource-And-Asset-Pipeline/authored-data-table-registry.md` | 19 | **6** |
| `09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md` | 28 | **22** |

Corpus **389 → 347**. **33 names anchored, 0 of them ambiguous** (checked against the 57 duplicated
names image-wide before writing any of them).

## AUDIT-LOG — anchoring was not bookkeeping; it found three errors, two of them mine

**1. A wait-table row was inverted, in my own document.** Three of the four wait kinds branch `jne`
to the proceed path on *found / active*. The fourth branches **`je`** (`0025E0A9`): **finding a
script request BLOCKS**, and finding none proceeds. The table said "satisfied when an entry exists".

**And the removal is in the caller, not the callee.** `ActorResource_FindScriptRequestEntry`'s
**complete 121-byte body contains no store instruction at all** — it is a pure reader. The removal
is `0025E0B0 call ActorResource_RemoveActiveEntry`, on the blocked path. The old wording put the
store in the wrong function *and* inverted which outcome continues.

**2. A claim was resting on a ledger name.** `SaveWrite_GetBusyFlag` is **seven bytes**:
`mov eax, dword ptr [rip+…]` → `02CA99E8`, `ret`. That is the whole function. **What is read is "a
global is non-zero", not "a save is in progress."** The pass's behaviour was established; the
trigger's identity was borrowed. Now says so.

**3. Null arrives two ways.** `ActorHandle_ResolveRegistryEntryByPackedId` has **two null returns of
its own** (`003588B8`, `00358933`) besides the caller's zeroed `rdi`. **A reader of `02099D78` cannot
tell "no party focus" from "the handle did not resolve."**

## NOTE — the registry's consumer table, verified mechanically

All 16 rows name a "principal consumer". **15 of 15 nameable rows genuinely reference the slot they
are named against**, each with a real site now in the table. **No row was taken on the name.**

**Three ref counts disagree with the census and are marked ⚠ rather than overwritten**: `02EBF190`
170→176, `02EBF138` 128→129, `02EBF1A0` 10→13; the other twelve match exactly. **Left in place**,
because the two counts came from different instruments and the census is known to *under*-count
(rip-relative only, and this executable also reaches globals through a register holding the image
base). **A disagreement in the direction of "the census found more" is the one that needs explaining,
and nothing here explains it.**

## NOTE — a role column that was partly restating its own function names

The gambit config table gave seven functions a "Role". **Two I read completely and both roles were
looser than the code:**

- `CopySelectedBankForStatsIndex` does not *switch* anything — it **copies a 52-byte record** to a
  caller buffer (`00327C81`-`00327C9D`), bounded at index ≤ 39.
- `AdjustAvailableEntryCountByStatsIndex` loops **three** banks and clamps each count to **twelve**
  (`0032795B lea r11d, [rdx+0xc]`, `00327985 cmovg`).

**Three rows are still name-derived and are now marked as such in the table.** A role column that
paraphrases the function name asserts nothing; leaving that visible is the point.

**Two joins fell out:**

- **The gambit config layer lives inside `02EBF190`** — the registry's heaviest slot at ~170
  referencing functions. Neither the registry document nor the gambit document said so.
- **A third, independent sighting of twelve** — and this one is a hard `0xC` **clamp** on the entry
  count, not a count of things. §8l counts twelve slots and the command map yields subgroups 0-11;
  **a bound on the quantity itself is worth more than two tallies agreeing.**

## NOTE — I nearly reported a phantom defect in the checker

My replication found 762 mentions against their 389, and **46% of mine were single-lowercase-word
names** (`entry` ×139, `free` ×49, `exit` ×26, `floor` ×24). I was about to report prose-collision
noise as a defect. **Subtracting that class reproduces their counts exactly** — 31−3=28, 20−1=19,
12−2=10. **Their filter was already correct and mine was the noisy one.** The arithmetic check is the
only reason that did not go out as a finding.

---

# Block: `+0x61B0` was not a shared field — it is a construction handoff (2026-09-03)

## COVERAGE

New document: **`16-UI/Widget-Object-Model/the-widget-constructor-and-object-sizes.md`**
Complete bodies read: `002465F0` (395 B), `00245000` (31 B), `00276650` (282 B), `00273A20` (9 B),
`00244F00` (68 B). Gates clean, 63 addresses cited, 0 needing confirmation.
New instrument: `Tools/work/h78/widget_constructor_sites.tsv`.

## AUDIT-LOG

**The row is a constructor and its handler, not two touchers of a field.**

```asm
002766D1  lea  r8, [rip + 0x3748]   ; = 00279E20, the handler
002766D8  mov  edx, 0x61f0          ; the object's SIZE
002766E0  call 0x245000
002766F7  mov  qword ptr [rsi + 0x61b0], rdi   ; arg 2, left for the handler
```

`00279E20` then reads `+0x61B0` back and copies it into each child at `+0x2FE8`. **The census saw one
write and one read and inferred a shared field; the relation is a handoff across construction.** The
link is a `lea rip` plus an immediate — **neither is a struct-field reference, so no field census
could ever have seen it.**

**`002465F0` is the constructor for every widget in the game**: `memset(object, 0, size)`, install the
handler at `object + 0` (defaulting to `005C5230` when null), write a fixed header — **`1.0f` at
`+0xB8` and `100` at `+0x44` on every widget** — then **call the handler once, during construction**.

**49 call sites, 26 distinct object sizes**, each with its handler recovered. 4 cells blank and
reported, not dropped.

**Children are constructed in place inside the parent**: `parent + 0xC0 + index * 0x3010`, and
`0xC0 + 2 * 0x3010 = 0x60E0` — exactly the sub-object base `00279E20` takes the address of at seven
`lea` sites. **At most two children; the geometry leaves room for exactly two.** Stated as an
arithmetic bound, **not** a loop bound — there is no loop, and the index mask `and ecx, r15d` has
`r15d = esi` on one of its paths.

## NOTE — a third invisibility mode, and it hides objects rather than fields

| mode | why a displacement census misses it |
|---|---|
| base materialised by `lea` | later accesses carry a small or zero displacement |
| offset folded into a scaled index | no displacement in the instruction at all |
| **size or offset passed as a value** | **the constant is an immediate to `mov`, never an address** |

**The third hides whole objects**, because the constant that gives the object's extent never appears
in a memory operand anywhere in the image.

**And it is the one that pays.** Any function appearing as a `handler` receives an object of the size
on its row, so its `[rcx + disp]` accesses are fields of a **known-size** object — **two functions
sharing a displacement but not an object size are not touching the same field.** That is a mechanical
type check for the pair frontier.

**Mode 1 measured, not assumed, for this record:** only **4 functions** take a `lea` into
`[0x6000, 0x6400]`, 11 sites, **two of them 32-bit `lea ecx`** — arithmetic on an id, not an address.
Of the 10 transitive callees that receive `parent + 0x60E0`, **none accesses `+0xD0`**. Still not a
finding — "no writer found" never is.

## NOTE — three corrections inside this read, all before writing

- **`edx` is a size, not an offset.** My scan's column was labelled `offset` and my reading was built
  on it. `00246612 movsxd r8, edx` into a `memset` count settles it. **A column name is a claim.**
- **`00861EC0` is not a body.** It is the first of a block of `jmp qword ptr [rip …]` import thunks,
  IAT slot `008C2A60`. The zeroing rests on **the import name plus the argument pattern**, not on a
  body anyone read — it is in a system DLL. **This is the thunk ambiguity the named-not-cited checker
  warns about, met in the wild.**
- **"Two children" was nearly asserted from a mask** that turned out not to be a constant.

---

# Block: `001E9D20` read, and a fifth invisibility mode (2026-09-03)

## COVERAGE

New document: **`99-Unresolved-Residual/Glyph-Run-Rendering/choosing-the-render-target-for-a-text-run.md`**
`001E9D20` (472 B) and `001E9C30` (7 B) read complete. Gates clean, 68 addresses, 0 to confirm.
New instrument: **`Tools/work/h78/struct_offset_refs_w.tsv`** — the struct census rebuilt with
**`width`, `index_reg` and `scale`** columns, 25,234 rows.

## AUDIT-LOG

**`001E9D20` is render-target selection**, the function the sibling document says neither of its two
functions touches.

- **Four-condition memo**: same two parameters, same offscreen flag, target already resolved →
  **returns without writing anything.** The memo keys are exactly what a successful call last wrote,
  and the failure path clears them, **so the memo cannot go stale.**
- The descriptor comes from an ordered tree keyed on **`(b << 32) | a`** — both int arguments packed
  into one 64-bit key.
- **First-free-or-already-mine over exactly two slots**; claiming writes the caller's key into the
  slot's first dword. **A slot holding `0` is free** — which is what the initialiser writes.
- **When both slots are taken the request is not refused: the overflow path reuses slot 1.**

**And the arithmetic closes a structure neither of us was aiming at.** The buffer is
`state + 0x30 + (slot*32 + n) * 0x38`, `1 <= n <= 31`. Two slots of 32 entries of `0x38` is `0xE00`,
and **`0x30 + 0xE00 = 0xE30`** — where your 4×4 float matrix begins. The overflow path's literal
`+0x730` is the same number reached a third way. **Two independent derivations meet on one boundary.**

## NOTE — a correction to the sibling document's record-relative column

The base correction from `+0x2324` to `+0x2320` was applied to the **first two rows and the last**,
and not to the ten between them. **The absolute column and every semantic reading are right.**

| that document says | absolute | correct |
|---|---|---|
| `+0x04` | `+0x2328` | **`+0x08`** — currently duplicates the row above |
| `+0x08`…`+0x20` | `+0x232C`…`+0x2344` | each **+4** |
| `+0x24`, `+0x25` | `+0x2348`, `+0x2349` | **`+0x28`, `+0x29`** |

The initialiser settles it independently of any base: `001E73A0`-`001E73CA` writes at `rax+0`, `+4`,
`+8`, `+0xC`, `+0x14`, `+0x1C`, `+0x20`, `+0x24`, `+0x28`. **The visible symptom is the duplicated
`+0x04`.**

## NOTE — mode 5, and it differs in kind

**The two descriptors do not occupy two sets of displacements.** Both are reached as
`base + index*0x2C + fieldoffset`, so **every access to descriptor 1 is recorded at descriptor 0's
displacement.** Measured: 11 named offsets in `[0x2320, 0x234C)`, **none** in `[0x234C, 0x2378)`.

| mode | what is lost |
|---|---|
| base materialised by `lea` | the displacement |
| offset folded into a scaled index | the displacement |
| size or offset passed as a value | the object's extent |
| one store covering two fields | the second field |
| **entry number carried in the index** | **every element after the first** |

> **A displacement census over an array reports the element layout, not the array.** "This field has
> 11 touchers" is right; "this record is 11 fields" is not.

## NOTE — mode 4 measured, and the number is an upper bound

Rebuilt census: **1,256 of 2,874 named displacements (43.7%) have an interior byte that some other
access names independently.** That is the *candidate* population, **not a count of mode-4 hits** — a
wide access may legitimately be one wide field, and this instrument cannot tell an 8-byte field from
two 4-byte fields read together. **Stated as an upper bound.**

Width distribution over 25,234 rows: 1B ×3,728 · 2B ×1,724 · 4B ×9,408 · 8B ×9,153 · 16B ×1,221.

**Controls:** `+0x6B5` still 4 rows, all width 1. `+0x6B4` is **85, not 84** — the rebuild now
includes indexed forms, which the previous census dropped.

## NOTE — `+0x2349` was not writer-less

The rebuilt census shows **`001E8070` writing it directly at `001E84D0`**
(`mov byte ptr [rcx + rbx + 0x2349], 0`) — an **indexed** form, which is why a census without index
support misses it. **The sibling document is right** ("read and cleared by the emitter"); it is the
summary that overstated. **The restraint was still correct for the right reason** — but the gap was
in the instrument, not the image.

---

# Block: my own over-reach corrected, and nothing frees a slot (2026-09-03)

## AUDIT-LOG — the correction is mine to take

`repos-55` weighed **four** readers of `+0x2379` against the one I had. **It is a mode selector, not
an offscreen or suspend flag**, and my document had called it "the offscreen flag" and the zero path
"the screen". **Neither was read here** — both were imported from a name I chose myself. Removed
throughout; the reading below the interpretation was unaffected.

**And a fifth site agreeing with them, inside my function rather than around it.** The memo guard's
fourth condition is `+0x2379 == 0`, so **the memo only fires in the shared mode** — a claiming run
can never take the early return and does the tree lookup, the allocator and the buffer rebuild every
time. **The non-zero mode does more work, and this is a fifth independent way of seeing it.**

## NOTE — nothing releases a claimed slot

Their mode reading crossed with mine raises a falsifiable question: if the frame-level flush stands
aside in the claiming mode, **what frees a slot?** Searched in the two ways that could hide it:

| search | result |
|---|---:|
| functions taking a `lea` to the array base `+0x2320` | **2** — the initialiser and the selector |
| writes at displacement `+0x2320`, indexed forms included | **1** — the claim itself |

Those two functions are the only code that can reach the array, and **the materialised pointer
escapes neither** — no call sits between `001E7396` and `001E73DA`, or between `001E9DF4` and
`001E9E46`.

> **Two writers image-wide: the initialiser sets the owner field to `0`, the selector sets it to a
> key. Nothing sets it back.** So the first two distinct owners take a slot each and **every owner
> after that shares slot 1** until the record is rebuilt. Their caution that a reused record
> accumulates work from two owners is **not an edge case — it is the steady state from the third
> owner onward.**

**Measured, not assumed**: stated only because both searches positively return the initialiser, the
claim and both `lea` sites. **Had either returned nothing, the section would say nothing.**

---

# Block: `002AC5F0` — the largest unclassified function draws nothing (2026-09-03)

## COVERAGE

New document: **`16-UI/Text-And-Number-Rendering/the-text-control-code-language.md`**
`002AC5F0`: 7,489 B, 1,658 instructions, 61 loops, both jump tables decoded. Gates clean.

## AUDIT-LOG

**It is the interpreter for the control codes embedded in game text, and it draws nothing.** That
answers the glyph-run document's open question *"what `002AC5F0`, `002AAE40` and `002AF960` draw"* —
for this one, the answer is that the premise is wrong.

- **`002AC5F0(ctx, char **cursor, float *out, int *out2)`** — the cursor is **by reference** because
  the function advances it past what it consumes.
- **The return value is "call me again".** All seven call sites are the identical
  `call / test eax,eax / je`. Return 1 = consumed a code; 0 = ordinary character or NUL, caller
  takes over.
- **Bytes `0x01`-`0x0F` are tokens; `0x10` and up are text.** 15 arms at `002AE334`.
  **`0x0B`, `0x0C`, `0x0D` route to the ordinary-character arm — they are not codes.**
- **`0x0F` is an escape prefix**: the next byte, printable ASCII `0x20`-`0x70`, selects among
  **32 distinct arms** (35 targets at `002AE370`, `0x51` case bytes at `002AE3FC`).
- **The three tables tile with no gap** — `002AE334` +0x3C +0x8C +0x51 = `002AE44D`, and `002AE450`
  is the next function. **Three lengths from three separate `cmp` bounds meeting end to end is the
  check that the decode is right.**

**Every arm has the same three lines**, and they explain the whole design:

```asm
lea  rdx, [rsp + 0x40]      ; a payload buffer
call 0x3ffab0               ; parse; returns a BYTE COUNT
add  qword ptr [rdi], rax   ; advance the cursor by that many bytes
```

**The parser decides how long a code is, so the interpreter never needs to know.** `003FFAB0` is the
most-called callee at 19 sites, one of **11 parsers in the band `003FFAB0`-`003FFF10`, 32 sites**.

**Why it is the largest function**: it is the *only* implementation of the language, and
**`002B2150` and `002A9F00` are both callers and callees** — the interpreter and the measure/emit
passes are mutually recursive, which is how a code that inserts text gets that text measured and
drawn by the machinery currently interpreting it.

## NOTE — the catalogue is a map, not a meaning

32 arm addresses are read and tabulated; **four were sampled and 28 were not.** The document says so
in its own "what is not known" rather than letting a complete-looking table imply otherwise.
**A selector-to-arm table is a map of where the code goes, not of what it does.**

---

# Block: the false-premise question withdrawn, and Z-9 closed (2026-09-03)

## AUDIT-LOG — the question was wrong twice, not once

`how-a-line-of-text-becomes-glyph-quads.md` asked *"what `002AC5F0`, `002AAE40` and `002AF960`
draw"*. **Withdrawn rather than answered.**

- **None of the three draws.** The glyph emitter is `002A9F00`, which is not among them.
- **They were never peers.** `002AAE40` calls `002AC5F0` at `002AB5B0`, so the question set a
  function against one of its own callers.

The premise came from a profiler scope: all three close `"display : draw Font"`. **A profiler scope
groups a call tree, not a set of equals.**

| | |
|---|---|
| `002AF960` | opens and closes a run — batch counter, the `+0x10E4` budget, two submit calls |
| `002AAE40` | a drawing pass — sets the per-glyph gradient via `0017FC90`, then walks the string |
| `002AC5F0` | the control-code interpreter |

**Replaced with a question about functions that really are peers**: what divides `002AAE40` from
`002A8C50`, `002AF340`, `002B1FB0` and `002B5730` — the other four callers of the interpreter.

> **The tell was available three readings earlier.** Each of the three came back *not quite fitting*
> the question, and each time the answer was adjusted rather than the question examined. **A run of
> near-misses on one question is evidence about the question.**

## NOTE — the same error as the `+0x1398` withdrawal, one level up

`repos-55` inferred **pointer** from **qword** and reported the mismatch with a literal as a
contradiction in the engine. I inferred **peers** from **shared profiler scope** and asked a question
no answer could fit.

> **Both took a property of the observation — an access width, a scope membership — and read it as a
> property of the thing observed.** The width is real and the scope is real; neither carries the
> meaning that was drawn from it.

## NOTE — Z-9 was stale in the ledger, and it was mine

`check_questions.py --drift` reported **4 unticked boxes the table calls ANSWERED**. One was **Z-9**,
answered by my own reading and never ticked in the document. Fixed: **4 → 3**, questions_closed
315 → 317.

**Ticked for the mechanism only.** The subgroup selector, its range and its two uses are read; *what
each of the twelve subgroups means in authored data is not*. **That is carried as its own successor
question rather than left buried inside a ticked box** — a ticked box with an unread half is how a
question stops being asked.

**Still outstanding and not mine to fix:** 3 stale, 2 early, and **5 ids cited by documents with no
row in the table (BQ-29…BQ-33)**. The last five need rows in `_index/OPEN-QUESTIONS.md`, which I do
not edit.

---

# Block: verifying the classifier fix, and the bug's larger class (2026-09-03)

## AUDIT-LOG — the four named rows confirm, my totals did not

**Independent parser, written without reading theirs: L-7 ANSWERED, Z-9 PARTLY, AO-4 PARTLY, BQ-5
PARTLY.** All four agree with the fix. The one-character bold-span bug is real and is documented in
`check_questions.py` with the measurement attached.

**My totals disagreed and I was wrong.** I read 120 / 11 / 463 against their 148 / 31 / 420 and
briefly had it as a finding. **The cause is vocabulary, not logic**: their classifier knows about 25
status keywords (`RECOVERED`, `ADVANCED`, `SHARPENED`, `BOUNDED`, `CHARACTERISED`…), mine knew 8.

> **Two instruments that do not share a definition of the categories are not cross-checking each
> other.** Agreement on four named rows was worth something; agreement on totals was never available,
> and I nearly reported the gap as a defect in theirs.

## NOTE — the same bug has a larger, still-open class, and it is silent

The fixed classifier reads the **first bold span** and matches a leading keyword. **36 id-rows begin
with a word that is in neither vocabulary**, across **24 distinct lead words**, and every one falls
through to **OPEN** with no warning.

| lead word | rows | example |
|---|---:|---|
| `NARROWED` | 6 | K-2 |
| `LARGELY ANSWERED` | 3 | AP-5 |
| `DONE` | 3 | AW-5 |
| `DISSOLVED` | 2 | G-6 — *"the premise is wrong; none of them does"* |
| `MEASURED PROPERLY` | 2 | AW-3 — *"21, not 53"* |
| `HALF ANSWERED` | 2 | BE-6 |
| `FIELDS IDENTIFIED, offsets OPEN` | 1 | **Z-2** |
| `SUPERSEDED`, `DOCUMENTED`, `TRIAGED`, `NOT A DEFECT`, `NEGATIVE NOW EXHAUSTIVE`, … | 1 each | |

**At least two dozen of the 36 are demonstrably not open** — `DONE`, `DOCUMENTED`,
`MEASURED PROPERLY`, `NEGATIVE NOW EXHAUSTIVE` and `DISSOLVED` are closures; `LARGELY`, `HALF`,
`NARROWED` and `FIELDS IDENTIFIED` are partials. **So `questions_closed` is still under-counting, and
the totals still look stable** — which is the lesson from the row-typography bug, arriving a second
time in the same file.

**The fix is theirs to choose, and their own rule points at it**: *tuning a reader to guess ambiguous
input teaches it to guess; fixing the row stays fixed.* So **normalise the 36 rows**, not add 24
keywords.

> **But there is one reader change that is not guessing: warn on an unrecognised lead word instead of
> defaulting to OPEN.** Today an unknown status word is indistinguishable from a genuinely unanswered
> question. **The failure is silent, and that is the property worth removing** — it turns 36 invisible
> misreads into 36 visible ones and stops the 25th word from ever being written unnoticed.

**`_index/OPEN-QUESTIONS.md` not edited** — reported only.
