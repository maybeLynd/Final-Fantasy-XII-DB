---
system: The audio boundary — what the engine calls to make a sound
category: 18-Audio
status: AUDITED — every question this page asks is closed (the 0215EFxx command block, UQ-254, answered 2026-09-17); the remaining ~130 functions of the inbound API surface are tracked as UQ-245 on the request page (UQ-253 superseded); status re-derived 2026-09-18 (FABLE)
owner_layer: PrimaryOwner:Audio + Boundary.Audio.NativeSupport
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN158 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). Of the functions classified since GN158 this document cites `0028DC00`, `002C7660`, `002C7B10`; the 21 classified before GN160 are named in AUDIT-LOG's batch records and not in a tracked machine-readable list, so identity is not claimed. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md, lineage extension (twenty ledger figures across five generations)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-12
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  crossref_clean: false        # 2026-09-30 (SWE2-DATA): false until the pass-22 UNACCOUNTED NEIGHBOUR findings are accounted (FRONTIER-REQ-SWE2-DATA-PASS22-DEBT; OPUS-REQ-DATA-PASS30-CROSSREF-CLEAN-0930)
  reopened_count: 1
---

# The audio boundary — what the engine calls to make a sound

> The first Audio function bodies read in this database, the actual call that plays a sound, and
> the single global that silences all of it.

## 1. What the player sees

Every sound in FFXII — a sword connecting, a menu cursor moving, a spell going off — is some piece
of game code asking the sound system for it. The game and the sound system are separate things: one
decides *that* a sound should happen, the other decides *how* it is produced. The handful of calls
between them is the seam this document describes.

Two things a player can observe come straight out of that seam.

**Sound can be switched off at one point — for the common requests.** There is a single value the
game checks before it will start a sound through its convenience wrappers. When it is set, the request
is abandoned immediately and the caller is told the sound did not start. Not muted at the mixer —
never begun. *(Qualified 2026-09-12: one ungated wrapper, `00271500`, and the script verb
`sebsoundplay_2c1` do not check it —
[the request page](how-a-sound-request-becomes-a-voice.md) §2, scope correction.)*

**The game asks for a sound and gets a receipt.** A successful request hands back a handle the caller
can keep; a failed one hands back a "nothing" value. That is why some sounds can be stopped, moved or
faded later while others are fire-and-forget: it depends on whether the caller kept the receipt.

## 2. Native mechanism

### The play call

The most-called audio entry point in the game is `00249C60` — **99 callers, none of them inside
Audio**, which is the signature of a service the rest of the engine consumes. Its complete body is
five lines:

```c
uint32_t Audio_RequestSoundA(int localIndex) {
    if (globalAudioGate /* DAT_02091098 */ == 0) {
        int id = ResolveSoundId(localIndex);    /* 003A1180 */
        if (id != -1)
            return PlaySound(id, 0x40, 0x7F);   /* 002DF220, tail call */
    }
    return 0xFFFFFFFF;                          /* no handle */
}
```

> **Corrected 2026-09-02.** This block previously showed both the wrapper and the resolver as
> nullary. Both take the caller's **bank-local sound index**: `00249C60` never writes `ECX` before
> `call 0x3A1180`, so its own first argument passes straight through, and `003A1180` consumes `ECX`
> and adds it to its result. 66 of the 211 call sites load that index as an immediate in the range
> `0x0A`–`0x6C`. See [`how-a-sound-request-becomes-a-voice.md`](how-a-sound-request-becomes-a-voice.md) §2.

Three separate refusals, in order: the global gate, an unresolved sound id, and whatever `002DF220`
itself decides. Each returns the same `0xFFFFFFFF`, so **a caller cannot tell from the return value
which of the three happened** — a real diagnostic limitation for a modder chasing a silent sound.
(There are in fact four refusals, and the last two return `0` rather than `0xFFFFFFFF` — see the
companion document.)

`00249CA0` is the same function with a different resolver (`003A11F0`). So these are members of a
family of thin per-sound wrappers over one shared play call, which is why the boundary has many small
entry points rather than one general one. **The family is four wrappers over four resolvers on three
boot-loaded bank handles, and the script verb `sebsoundplay_2c1` reaches the play call with its own
pan and volume** (corrected 2026-09-12, OPUS-CONTRA-FABLE-SOUND-REQUEST-SCOPE; the table is on
[the request page](how-a-sound-request-becomes-a-voice.md) §2).

### The two constants — settled

`002DF220` is invoked as `(soundId, 0x40, 0x7F)` from both wrappers — `0x40` = 64 and `0x7F` = 127.

**Corrected in §10:** only the pan is an immediate. The volume is **computed from it** —
`mov edx, 0x40` then `lea r8d, [rdx + 0x3f]` — and no call site in the image passes `0x7F` as a
literal. Both are compile-time constants in effect; only one is a constant in the encoding, which
matters to anyone patching them. The Script VM caller `00357040` passes a **variable** volume.

**They are a pan and a volume: `0x40` is the pan and `0x7F` is the volume.** Following them through
`00210C00` → `0021B5B0` → `00224570` shows them reaching two distinct voice setters, `002256F0`
(pan, writing `voice+0x20`) and `002257E0` (volume, writing `voice+0x1C`) — and `002256B0`, the
voice reset, writes those same two fields with those same two literals. The full formulas, with
their real constants, are in
[`how-a-sound-request-becomes-a-voice.md`](how-a-sound-request-becomes-a-voice.md) §4.

> **The 0–127 half of the earlier hypothesis was wrong.** This document read the pair as "a
> volume-and-pan pair in a 0–127 range". The volume is 0–127; **the pan is 0–255**. `002DF220`
> masks the volume `& 0x7F` and merely truncates the pan to a byte, and `002256F0` branches at
> `0x80` and handles `0x80..0xFF` on a mirrored axis. 64 is the centre of the pan's range, not its
> mid-scale point in a 0–127 field.

### The global gate

`DAT_02091098` is checked before any work is done. Non-zero means no sound is started and no handle
is issued. This is the cheapest possible intervention point for silencing the game's own sound
requests, and — because the check is *before* id resolution — it also suppresses the lookup, not just
the playback.

### Handle and command state

A small cluster of accessors sits on a dedicated command/handle block in the `0215EFxx` range:

- `002DEC00` returns `DAT_0215EF44` — a plain read of the current command/handle state word.
- `002DEE50` gates on `param_1 < 0 && DAT_0215EF44 < 0`, and otherwise writes a byte to
  `DAT_0215EF4D` before forwarding to `001DBCA0`. The negative test on both the argument and the
  stored word is a "neither the request nor the current state is valid" guard.

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `00249C60` | `Audio_RequestSound_WorldLiveResolve` | 51 B | **the most-called audio entry point** — 99 external callers, 0 internal; takes a bank-local index; gate → resolve → play |
| `00249CA0` | `Audio_RequestSound_PlainResolve` | 51 B | same shape, resolver without the world-live precondition; 6 external callers |
| `002DF220` | `Audio_PlayResolvedSound` | 92 B | the shared play call, `(id, pan=0x40, volume=0x7F)`; 5 external + 4 internal callers |
| `003A1180` | `Audio_ResolveBankLocalId_WorldLive` | 111 B | `bankSlot*512 + localIndex`, refused unless the world runtime is live; returns `-1` on failure |
| `003A11F0` | `Audio_ResolveBankLocalId_Plain` | 79 B | the same arithmetic against the same globals, without the precondition |
| `002DEE50` | `Audio_SetTrackLevelAndForward` | 27 B | guarded write to the `0215EFxx` command block |
| `002DEC00` | `Audio_GetCurrentTrackHandle` | 7 B | reads `DAT_0215EF44`; 12 external callers |
| `001DBCA0` | forward target of `002DEE50` | — | not read |
| `007AD450` | audio-internal free thunk | 11 B | `(*DAT_02EAD0B8)(*(void**)(p - 8))` — 98 callers, **all inside Audio** |

Addresses are Ghidra image base `0x00120000`. Every row above is a function.

### Data addresses cited by this document

| Address | Name | Kind | Contents |
|---|---|---|---|
| `02091098` | global audio gate | `u32` | non-zero suppresses sound requests before id resolution |
| `0215EF44` | command/handle state word | `u32` | read by `002DEC00`, tested by `002DEE50` |
| `0215EF4D` | command state byte | `u8` | written by `002DEE50` |
| `02EAD0B8` | audio free function pointer | pointer | called by the audio-internal free thunk |

## 4. Data structures and formulas

### The request, exactly as the engine evaluates it

```c
uint32_t Audio_RequestSound(int localIndex) {
    if (*(int *)0x02091098 != 0) return 0xFFFFFFFF;   /* gate closed        */
    int id = ResolveSoundId(localIndex);              /* bankSlot*512 + localIndex */
    if (id == -1)                return 0xFFFFFFFF;   /* id not resolved    */
    return PlaySound(id, /*pan*/ 0x40, /*volume*/ 0x7F);   /* may also fail */
}
```

### The command-state guard

```c
if (param_1 < 0 && *(int32_t *)0x0215EF44 < 0) return;   /* both invalid -> no-op */
*(uint8_t *)0x0215EF4D = param_3;
Forward_001DBCA0();
```

Note the guard is a conjunction: a valid argument **or** a valid stored state is enough to proceed.

### Boundary population, measured

Against a freshly regenerated `DumpFullCoverageGraph.java` at the GN checkpoint:

| Set | Count |
|---|---:|
| Functions tagged `Boundary.Audio.NativeSupport` | 177 |
| — with no callers at all | 51 (graph) / **50** (byte decode, §11) |
| — called only by Audio-owned functions | 25 |
| — called only by non-Audio functions | 54 |
| — mixed | 47 |

> **The rule behind the split, added by §11 because it was unstated.** These three rows count a
> caller as *Audio* if it is `PrimaryOwner:Audio` **or is itself tagged
> `Boundary.Audio.NativeSupport`**. Under the stricter rule — owner only — the split is
> **14 / 69 / 43**. Both are defensible; §5 and §8 argue that the tag is a *rejection bucket* rather
> than Audio membership, so the stricter reading is the one consistent with this document's own
> thesis, and it strengthens it: **69 of the 177 are called only from outside Audio, not 54.**
| Functions tagged Audio-owned | 2,064 |
| — with at least one non-Audio caller | 174 (upper bound — see §8) |
| — **corrected**, excluding the seven unhonoured retractions | **168** |

## 5. Call chain

```
gameplay / UI / script decides a sound should happen
  -> Audio_RequestSoundA  00249C60          [AUTHORITY * -> 18]
     -> global gate  DAT_02091098           (closed -> 0xFFFFFFFF, nothing else runs)
     -> Audio_ResolveSoundIdA  003A1180     (-1 -> 0xFFFFFFFF)
     -> Audio_PlayResolvedSound  002DF220 (id, 0x40, 0x7F)
        -> SQEX Sd driver internals (007Axxxx-007Fxxxx), not read here
  -> handle, or 0xFFFFFFFF
```

**Upstream:** 99 distinct non-Audio functions call `00249C60` directly. **Downstream:** the SQEX Sd
driver, whose internals live in the high address range and are documented structurally in
[`../sqex-sd-sound-driver-architecture.md`](../sqex-sd-sound-driver-architecture.md).

**Do not confuse with:**

- **`Boundary.Audio.NativeSupport` is not the audio API.** See §8 — it is a rejection bucket.
- **`007AD450` is not a boundary in the inbound sense.** All 98 of its callers are inside Audio; it
  is an internal free thunk. A high caller count alone does not make something an interface.

## 6. Modding notes

- **Best intervention point:** `DAT_02091098` to suppress everything, or `00249C60`'s return to
  suppress one family of requests. Both are ahead of the driver, so nothing is allocated or queued.
- **Regenerates itself:** nothing here. These are request-time calls; there is no cached state to
  keep consistent beyond the `0215EFxx` block.
- **Breaks if:**
  - You expect the return value to tell you *why* a sound failed. All three failure paths return the
    same `0xFFFFFFFF`.
  - You hook `002DF220` expecting every sound to pass through it. Only this wrapper family is
    proven to use it; the rest of the 174-function surface is unread.
  - You assume a function tagged `Boundary.Audio.*` has anything to do with sound. Most do not.
- **Multiplayer / XIIOnline:** sound is **local presentation**. What may legitimately cross the wire
  is the *authored sound identity and its timing* — the id and when it was requested — never a
  native handle, which is a local allocation with no meaning on another client. The GFZ's own
  annotations reach the same conclusion independently ("synchronize authored Audio intent rather than
  native objects"), which is a useful corroboration of a design rule rather than a claim about code.
- **Mod compatibility:** the sound ids resolved by `003A1180`/`003A11F0` are authored data and are
  the right surface for a mod to change.

## 7. What is not known

- [x] **CLOSED** — the meaning of `0x40` and `0x7F` (**BR-2**). They are a pan and a volume; the killer
      observation named here (read `002DF220`'s body and follow each parameter) is what settled it,
      and it also refuted the "0–127 pan" half of the guess. See
      [`how-a-sound-request-becomes-a-voice.md`](how-a-sound-request-becomes-a-voice.md) §2 and §4.
      *Ledger reconciled and confirmed 2026-09-12 (FABLE):* the row stayed OPEN because this box
      carried no id. Followed independently to the setters: `002DF220` masks the third argument to
      7 bits and passes the second as a byte through `001DBDB0` → `00210C00` → `0021B5B0` →
      `00224540` → `00224570`, where `002256F0(voice, 0x40, ramp)` is the **pan** — `(edx − 0x40) ×
      1/128` with sign +1 for `edx ≤ 0x7F` and `(0xBF − edx)` with sign −1 above it (`00225743`–
      `00225783`; constants `01CEBBA8` = 1, `01CEBC9C` = −1, `008C5B34` = 1/128), so `0x40` is
      **centre** — and `002257E0(voice, 0x7F, ramp)` is the **volume** — clamped to `[0, 127]`
      against `00906A44` = 127, stored at voice `+0x1C`, scaled by 1/127 (`002257E0`–`00225827`), so
      `0x7F` is **full**. The third argument both receive is a ramp in **frames**, divided by
      `008F6D54` = 60 (`0022571B`, `002257F8`); the wrappers pass 0. The refusal gate `003603C0` is
      the byte `022CB726`.
- [x] **CLOSED** — what `003A1180` and `003A11F0` resolve against, and how they differ. The same
      global handle (`02AEF3FC`) and the same 24-byte table (`02AEEDC8`), with identical arithmetic;
      the only difference is `003A1180`'s world-live precondition `00267330(0)`. The wrapper family
      is *not* explained by two different lookups.
- [x] ~~**UQ-253.** The remaining ~130 functions of the corrected 168-function inbound API surface. This document~~
      reads eight; the companion adds roughly forty more.
      *SUPERSEDED (register, 2026-09-14): a duplicate of `UQ-245`, the older and richer row, which lives on [the request page](how-a-sound-request-becomes-a-voice.md) and stays open; the surface question is tracked there, not here.*
- [x] What `DAT_02091098` represents in the player's vocabulary — a settings toggle, a cutscene
      suppression, a loading state. Its **effect** is proven, and it is now known to have exactly one
      writer (`00249FC0`) reachable from authored script via `00512080`; its **cause** is still not
      proven. **Killer observation:** decompile `0027F5D0` and see what state it sets the gate from.
  *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (BR-3): **"sound effects off while a full-screen
  menu needs silence".*** The gate has exactly three writers of its one setter `00249FC0` (`*(02091098) = arg`):
  - the script verb **`fsmenu_sedisable`** (`0x7013`, handler `00512080`), which passes the script's integer straight into the
    gate unless the full-screen menu context `[0209AC30] + 0xC0` is empty (`00280120`). The verb's own name, *se disable*, is
    the authored vocabulary ([the sound request contract](CONTRACT-sound-request.md));
  - the full-screen request widget `0027F5D0`, which closes it (`00249FC0(1)` at `0027F67B`) in the sub-state entered when its
    parameter `+0xD4` is `0x42`;
  - that widget's teardown `002D6F90`, which opens it again (`002D6FD4`).

  `0x42` is the remapped parameter of UI request 22 for the map-jump controller `__MJ_CTRL005`
  ([the UI request router](../../16-UI/Request-Router/ui-request-router.md)), and shipped scripts author it once. So in the
  player's vocabulary the gate is the sound-effect mute that a scripted full-screen menu holds while it is open, one
  map-jump screen in the shipped data. The HUD-like children the earlier note found belong to that widget's own layout.
  **Which in-game moment authors `__MJ_CTRL005` was not traced to a script.**
- [x] ~~**UQ-254.** The `0215EFxx` command block's layout beyond the fields now read. `0215EF44` (music track~~
      handle) and `0215EF4D` (0–127 music level) are established; the 16-entry table at `0215EF50`,
      the group mask `0215EFD8` and the sequence counter `0215EFDC` have structure but no named
      purpose.
      ***ANSWERED 2026-09-17 (FABLE): the table is a sixteen-slot handle table the build never fills, the mask is the mirror of the driver's group-hold mask, and the counter is the request serial.** *The table* at `0215EF50` is 16 entries of 8 bytes, `{u16 +0, u8 +2 index, u8 +3, s16 +4 id, s16 +6 count}`, laid out by the audio initialiser `002DE360` (`002DE3D2`..`002DE3F7`: index `i`, id `-1`, count 0, the rest 0). A rip-relative census over `0215EF50`..`0215EFCF` returns exactly two functions, that initialiser and the release `002DEB40(id)`, which finds the entry whose `+4` equals the id, decrements `+6` and, at zero, frees the entry with `id = -1` unless byte `+1` is set, in which case it pins the count at 1 (`002DEB50`..`002DEB84`). No instruction sets an id or raises a count, and no `lea` derives a pointer into the table, so the four release callers (`00363750`, `003D7F30`, `003DEC90`, `003DEE10`) always walk sixteen empty entries. *The mask* `0215EFD8` is written only by `002DF370(mask, set, immediate)`: with `immediate` it calls the driver's `001DBA90(mask, set)` and ORs or AND-NOTs the mirror (`002DF383`..`002DF39F`); otherwise it sends only the bits that would change, `mask & ~mirror` to set and `mirror & mask` to clear, and updates the mirror (`002DF3B5`..`002DF3F1`). `001DBA90` forwards to `00210FF0` on the driver object `00210B30()`. Its callers are the pause-menu handler `00229590`, which clears `0x3F` on pause (`0022980A`) and sets it back (`002298AD`), the screen-mask verbs' `003601D0` setting `0x1C` at once (`0036028C`), and the event coordinator `00226280` toggling `0x20`, `0x1` and the mask with bit 3 added (`0022651F`, `00226560`, `0022659C`): six group bits, the set of sound groups currently held. *The counter* `0215EFDC` is read and incremented only by `002DF660(a, b, c)`, which passes the old value as the second argument of `001DC2E0` (`00211270` on the driver object) from the voice start `003E9C10` (`003E9CEC`), the script BGM stream machine `003EADE0` (`003EAE9B`) and the bootstrap coordinator `003B8670` (`003B9136`): a serial stamped on every such request, as [the music page](../the-music-control-file-and-the-bgm-stream.md) already says. Static, rip census and bodies read.*
- [x] **CLOSED** — `002DF220` is *not* the only play path. `002DEF40` and `002DF010` reach the same
      dispatcher with a selector derived from bit 31 of the id, `003A0E20` routes bit-30 ids to a
      different encoding entirely, and music never passes through it at all.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| `00249C60` is the most-called audio entry point, 99 external / 0 internal callers | edge census over a freshly regenerated graph at GN, callers partitioned by owner tag | 11 (corroboration) + 1 for the body |
| Its exact gate → resolve → play structure and the three identical failure returns | complete exact-current body | 1 |
| `002DF220` is called as `(id, 0x40, 0x7F)` from both wrappers | complete exact-current bodies of `00249C60` and `00249CA0` | 1 |
| The `0215EFxx` command-state accessors and the conjunction guard | complete exact-current bodies of `002DEC00` and `002DEE50` | 1 |
| `007AD450`'s 98 callers are all Audio-owned | edge census partitioned by owner tag | 11 |
| Boundary population figures (177 / 51 / 25 / 54 / 47) | edge census over the GN graph | 1 |

### G-6 is dissolved, not answered — `Boundary.Audio.NativeSupport` is a rejection bucket

**G-6 asked which of the 177 `Boundary.Audio.NativeSupport` functions the rest of the engine calls to
produce sound. The premise is wrong: none of them does, by construction.** The tag does not mark an
audio interface — it marks functions that were *considered for Audio ownership and refused*. The GFZ
says so in its own annotations on those functions:

> `BOUNDARY_THIN_OR_GENERIC_LIBRARY_HELPER` — *"Thin accessor/thunk/allocator/free-dispatch helper
> **owns no independent Audio state or behavior**; no owner credit… **prevents Audio category
> contamination**."*

> `REJECT_AUDIO_EMPTY_NOOP_LIBRARY_STUB` — *"Body is an empty return-only function… carries no Audio
> state, command, codec, or device behavior… **do not count toward Audio owner denominator**."*

Bodies read from the set, all confirming it: `00584730` is `if (p) _aligned_free(p)` with **2,306
non-Audio callers**; `00203080` is a four-component float subtract; `00202C70` is a 64-byte copy;
`002E9B80` is an actor-handle accessor; `003601B0` is `mask |= 1 << (n & 0x1F)`; `0036DD80` copies a
16-byte constant; `007B8C80` is `return;`. **Seven bodies, no sound semantics between them.**

The correct question — *which Audio-owned functions does the rest of the engine call?* — is answered
by inverting the test: **174 of the 2,064 Audio-owned functions have at least one non-Audio caller.**
That is the real inbound surface, and `00249C60` sits at the top of it.

### The 174 is an upper bound, because GFZ corrections are not machine-readable

**Two of the functions my selector returned are explicitly disowned by the GFZ — in prose the tags do
not carry.** `00225580` is a `+0x18` dword setter and `00225690` a `+0x24` dword getter; both bodies
are single field accesses with no sound semantics, and both carry a correction marker:

> `RECLASSIFY_AUDIO_TO_SHARED_ICF_FIELD_ACCESSOR` — *"Cross-subsystem reuse proves it is not
> Audio-specific… **no Audio owner credit**. **SUPERSEDES** = Earlier rolling Audio owner credit at
> this exact address."*

Yet their tag sets are **identical** to `00249C60`'s, which is genuinely audio: all three carry
`GFZ.V120.PrimaryOwner.Audio`, `GFZ.V120WIP.X0.AudioReconstructionBB.Owner`, and the rest. The V120
reconstruction re-applied ownership from *"persisted affirmative V113 Audio ownership evidence"* and
**did not honour the V113.10R / V113.12R retractions** — so a later batch effectively undid the
correction by reading the earlier evidence and not the later withdrawal.

**Consequence:** a `PrimaryOwner` tag can be present on a function the GFZ has explicitly retracted,
and no tooling that reads tags can tell. The retraction lives only in the comment body, keyed by
`SUPERSEDES` and `RECLASSIFY_`. Filed as **BR-1**.

> **Bounded 2026-09-02, and this document's first version overstated it.** It said the retraction was
> *also* keyed by `REJECT_`, and that *"every tag-based census in this database"* over-counts as a
> result. A whole-image measurement by a peer session settled both halves:
>
> - **`REJECT_` is not a retraction marker.** It is `SOURCE_REJECTION_REASON=REJECT_<CATEGORY>_…`,
>   which declines ownership *for* a category — exactly what it is doing on the `Boundary.Audio.*`
>   functions above, correctly. Machine test: **zero owned functions carry a `REJECT` naming their own
>   owner.** Reading it as a retraction is what made the defect look widespread.
> - **`SUPERSEDES` and `RECLASSIFY` mark the same seven functions** — `00182E80`, `001DC3D0`,
>   `00225570`, `00225580`, `00225680`, `00225690`, `002256A0` — all `PrimaryOwner:Audio`, all still
>   tagged. **Tags and prose contradict each other nowhere else in the image.**
>
> So the correct claim is **"seven functions carry an unhonoured retraction"**, not "every census
> over-counts". The mechanism is real and the `174` above is still an upper bound by two; the scale
> was not. Recorded rather than quietly rewritten because the *reason* the wrong version was
> reachable is the point: a defect found in one place was generalised to the image without measuring
> the image.

### The overcount was six, not two

The paragraph above bounded the `174` as "an upper bound by two", because only two of the seven
retracted functions had been identified when it was written. Re-deriving the census from a call
graph regenerated against a freshly imported and freshly verified parent reproduces `174` exactly,
and six of the seven retracted functions are inside it (`002256A0` has no non-Audio caller and was
never in the set). **The corrected inbound surface is 168.** The mechanism this document identified
was right; the size of its effect was under-measured by exactly the number of retractions not yet
found — which is the same lesson in the other direction from the one recorded above.

**Superseded readings:**

- *Working names `Audio_RequestSoundA/B`, `Audio_GetCommandStateWord`,
  `Audio_CommandStateWriteAndForward`, `Audio_ResolveSoundIdA/B`* (§3) — **positional placeholders,
  replaced with evidence-based names.** The two request wrappers differ by an **ActorManager
  slot-flag gate**, not by "A" and "B": `003A1180` calls `00267330(0)` first and returns `-1` unless
  `(flags & 0x81) == 0x01`. The command-state pair turned out to be a **current-track handle** and a
  **0-127 track level**. The conservative form was kept in those two cases: the peer's proposed
  `Music_` prefix rests on one further inference and this document does not carry it.

- *`00249C60` and `003A1180` shown as nullary* (§2) — both take the bank-local sound index. Reachable
  because Ghidra prints `FUN_003a1180()` with no arguments when it has no signature for the callee,
  and an `ECX` pass-through leaves no trace in the C.
- *"a volume-and-pan pair in a 0–127 range"* (§2) — filed as a hypothesis and half right. The pair
  is confirmed; the pan is 0–255, not 0–127.
- *"174 (upper bound)"* (§4) — the corrected figure is 168.
- *"`003A11F0` … id resolution for `00249CA0`", offered as the reason for a wrapper family* (§2/§3) —
  the two resolvers read the same globals with the same arithmetic.

Corrections applied 2026-09-02 by the block that closed BR-2 and BR-4; the evidence for each is in
[`how-a-sound-request-becomes-a-voice.md`](how-a-sound-request-becomes-a-voice.md) §8.

## 9. Related

- [`how-a-sound-request-becomes-a-voice.md`](how-a-sound-request-becomes-a-voice.md) — the mechanism
  below this seam: the play call's complete body, the pan and volume formulas, the `slot*512+local`
  id space, the five bank classes, and the corrections listed above

- [`../sqex-sd-sound-driver-architecture.md`](../sqex-sd-sound-driver-architecture.md) — the driver this boundary calls into; establishes structure only
- [`../Sound-Selection/sound-trigger.md`](../Sound-Selection/sound-trigger.md) — selection above this seam
- [`../Audio-Bank-And-Controller-Family/audio-bank-and-controller-family.md`](../Audio-Bank-And-Controller-Family/audio-bank-and-controller-family.md) — the bank/controller classes
- [`../../_index/EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md) — the GFZ-can-be-wrong rule this document supplies a mechanism for

## 10. Falsification pass 2026-09-03 (repos-2d)

Run against snapshot `46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2`,
parent `2ed8affb…`, embedded EXE `73461d08…`.

**Disclosure.** This session cited `003A1180`, `002DF220` and this document's wrapper family in
[the R2 toggle document](../../15-Input/Modal-Toggles/r2-force-fight-toggle.md) while tracing a
looping sound. That makes this an audit of a document I have leaned on, and the pass corrected **my**
document as well as this one — see the last section.

### SURVIVED — every caller count, including against the thunk route

Caller counts are the class that has produced wrong answers twice elsewhere in this database, so
each was re-derived from the current graph and checked for jump thunks (there are none on any of
these):

| Claim | Measured |
|---|---|
| `00249C60` — 99 callers, **none inside Audio** | **99**, owners: unowned 67, UI 29, Save/Load 3. **Zero Audio.** |
| `00249CA0` — 6 external callers | **6** |
| `002DF220` — 5 external + 4 internal | **9 total, 4 Audio-owned** → 5 + 4 |
| `002DEC00` — 12 external callers | **16 total, 4 Audio-owned** → 12 |
| `007AD450` — 98 callers, all Audio | **98, all Audio** |

The external/internal split is applied consistently throughout the document, which is what makes
these numbers reproducible rather than merely repeatable.

### SURVIVED — the resolver's arithmetic and its precondition

```asm
003A1186  mov  ebx, ecx        ; the caller's bank-local index, passed straight through
003A118A  call 0x267330        ; the world-live precondition
003A1191  je   0x3a119c        ; zero -> proceed
003A1193  or   eax, -1         ; else -1, the refusal
…
003A11D7  shl  edx, 9          ; bankSlot * 512
003A11DA  add  edx, ebx        ; + localIndex
```

`bankSlot*512 + localIndex`, the `-1` refusal and the world-live gate are all exact. So is §2's
statement that `00249C60` never writes `ECX` before the call, so its own first argument passes
through — visible in the wrapper body below.

### SURVIVED — the gate is ahead of resolution

```asm
00249C64  cmp  dword ptr [rip -> 02091098], 0
00249C6B  jne  0x249c8b        ; gate non-zero -> -1, before any lookup
00249C6D  call 0x3a1180
00249C72  cmp  eax, -1
00249C75  je   0x249c8b        ; unresolved -> the same -1
```

Three refusals, one return value, and the gate genuinely suppresses the *lookup* as §2 claims.

### CORRECTED — `0x7F` is not a literal at any call site

§2 says of the pan/volume pair: *"The values are not derived from anything at the call site; **they
are literals compiled in**."* Half of that is wrong, and it is the half a modder would act on:

```asm
00249C77  mov  edx, 0x40          ; the pan IS an immediate
00249C7E  lea  r8d, [rdx + 0x3f]  ; the volume is COMPUTED: pan + 0x3F = 0x7F
```

`00249CA0` uses the identical idiom, and so does every direct caller of `002DF220` outside the
wrapper pair that this pass could resolve: of those **five** — owned by Rewards/Progression,
Combat Formula, Script VM / native bridge and two unowned — **four** pass
`lea r8d, [rdx + 0x3f]`. **Not one call site in the image passes `0x7F` as an immediate.** Both
values are compile-time constants in effect; only one is a constant in the encoding.

*(Those four are named by owner rather than address deliberately: they are illustrative of a census,
not evidence this document needs to account for, and citing four large gameplay functions would
import their neighbourhoods into an audio document. The fifth is cited below because the claim
rests on it.)*

That matters because §6 offers this call site as an intervention point: **a modder searching for a
`0x7F` immediate near the play call will not find one**, and patching the pan silently changes the
volume with it, because the volume is derived from the pan register.

### REFINED — the constants are the wrappers' convention, not the play call's signature

§2's claim is correctly scoped (*"from both wrappers"*), but the fifth direct caller does something
the document does not mention: `00357040` (183 B, Script VM / native bridge, one caller) passes
`mov r8d, r15d` — a **variable** volume. Script-driven sounds are therefore not fixed at `0x7F`.

§6's warning is *"you hook `002DF220` expecting every sound to pass through it"*; the companion
finding is that **even the sounds that do pass through it do not all carry the same volume**.

### Population note — 206 sites measured against a stated 211

§2 quotes the companion: *"66 of the 211 call sites load that index as an immediate in the range
`0x0A`–`0x6C`."* Measured here over the population **`00249C60` (192 sites) + `00249CA0` (14
sites) = 206**: 157 constant, 47 computed, 2 not determined, of which **63** fall in `0x0A`–`0x6C`.

Differences of 5 sites and 3 immediates. The instrument used here counts direct `call`/`jmp`
immediates inside bodies bounded by the next function entry, so it cannot see an indirect call and
can truncate a body that overruns its successor. **The two numbers are not comparable without the
companion's definition of the 211**, and this is recorded rather than reconciled — the shape of the
finding (most callers pass a small constant bank-local index) is unaffected either way.

### The pass corrected the auditor's own document

`003A1180` has **8 callers**, and one of them is the repeating-sound acquirer that
[the R2 toggle document](../../15-Input/Modal-Toggles/r2-force-fight-toggle.md) describes as
acquiring *"sound id `0x52`"* (named there, not cited here — it sits in a band another session
holds). This document establishes that the argument is a **bank-local
index**, not an id: the resolver returns `bankSlot*512 + localIndex`. That document's phrasing was
wrong and its open question understated the work — identifying the sound needs the **runtime bank
slot** as well as the `sead` bank data. Corrected there, with the reason recorded.

### Status

`audit.passes` 0 → 1. **Status stays `PARTIAL`**: §7 still carries three genuine unknowns — the
remaining ~130 functions of the inbound surface, what `DAT_02091098` represents in the player's
vocabulary, and the `0215EFxx` block's layout beyond the read fields. Those are open questions, not
unattacked claims.

### What was not attacked

The boundary population figures (177 / 51 / 25 / 54 / 47) and the `Boundary.Audio.NativeSupport`
rejection-bucket analysis in §8 were not re-measured; they rest on an edge census over the same
graph and would need an independently built census to attack rather than re-run. The `0215EFxx`
accessors' bodies were read but their consumers were not.

### Crossref state, and what this pass added to it

This document carries `crossref_clean: false` and did so before this pass — `audit_crossrefs`
reports unaccounted neighbours for citations in its own §2, §4 and §7 (`00202C70`, `00203080`,
`00224570`, `00225690`, `0027F5D0`, `003601B0` and others reaching **Movement**, **Platform**,
**Party** and **Resource**). Dispositioning those is a separate job from this falsification pass and
is not done here.

**What this pass added, and its disposition:** one citation, `00267330`, the world-live precondition
`003A1180` calls. It has **8 callers over 4 owners** (Party 2, Audio 2, unowned 3, Script VM 1), so
naming it imports a small Party neighbourhood. It is cited because the *"refused unless the world
runtime is live"* claim rests on it and cannot be checked without it. The Party callers are that
predicate's own consumers asking the same question, not audio relationships.

**Two illustrative citations were removed** during the pass for the opposite reason: naming four
large gameplay callers of `002DF220` to make a census point imported their neighbourhoods into an
audio document, and the census point survives without them. *A citation is a commitment to account
for what it drags in — and an illustration is not worth the commitment.*

## 11. Falsification pass 2 — 2026-09-03, session `repos-9e`

**§10 named what it could not attack**: *"the boundary population figures (177 / 51 / 25 / 54 / 47)
… rest on an edge census over the same graph and would need an independently built census to attack
rather than re-run."* This pass builds that census from the image and attacks exactly those figures.

**Two overturned, three survived, and one correction to the auditing session's own earlier work.**

### The numeric layer is clean

Flagged in advance because the companion document in this category had **seven** body sizes filled in
by estimating from decompiled line count. **That defect did not reach this document.** All eight
sizes re-derived from the certified function list:

```
00249C60  51    00249CA0  51    002DF220  92    003A1180 111
003A11F0  79    002DEE50  27    002DEC00   7    007AD450  11      8 of 8 exact
```

`177` tagged `Boundary.Audio.NativeSupport` and `2,064` Audio-owned are both exact, and the
four-way partition sums to 177. The arithmetic is sound throughout.

### Overturned 1 — the split counts the rejection bucket as Audio, which the document's own argument forbids

Re-deriving the partition with *"Audio caller"* meaning `PrimaryOwner == Audio` does **not**
reproduce §4:

| | document | `owner == 'Audio'` |
|---|---:|---:|
| no callers at all | 51 | 51 |
| only Audio-owned callers | **25** | **14** |
| only non-Audio callers | **54** | **69** |
| mixed | **47** | **43** |

Rather than assert the document is wrong, five candidate definitions were tested to find which one
reproduces it. **Two do, and they are the same rule:**

```
"Audio caller" := PrimaryOwner == Audio  OR  the caller is itself tagged Boundary.Audio.NativeSupport
                                                            -> 51 / 25 / 54 / 47   exact
```

**So the figures count `Boundary.Audio.NativeSupport` functions as Audio.** That is a defensible
rule — but this document argues the opposite twice, in §5 and at length in §8:

> **`Boundary.Audio.NativeSupport` is not the audio API.** See §8 — it is a rejection bucket.

**The same tag is a rejection bucket where §8 needs it to be, and Audio membership where §4 needs it
to be.** The numbers are not wrong; the definition behind them is unstated and contradicts the
document's own central argument. Under the stricter rule the boundary tells a different story —
**69 of the 177 are called *only* from outside Audio, not 54** — which strengthens §8's thesis rather
than weakening it.

**What should change:** §4 should state its rule inline, and say which of the two readings its
numbers use. Both partitions are defensible; publishing one without its definition is not.

### Overturned 2 — "no callers at all: 51" is 50 against the bytes

`0035D030` is counted among the 51 and is reached through a five-byte thunk:

```
002E22F0  thunk_FUN_0035d030  --JMP-->  0035D030
```

A thunk is a sink in the call graph, so the edge out of it is not recorded and the target's caller
list omits it. Same defect class as the one that hid `0020AC30`'s caller.

### Survived

| Claim | How attacked | Result |
|---|---|---|
| all eight §3 body sizes | re-derived from the certified function list | **8 of 8 exact** |
| 177 `Boundary.Audio.NativeSupport` | independent tag census | **exact** |
| 2,064 Audio-owned | independent census | **exact** |
| the partition sums to 177 | arithmetic | **exact under both definitions** |

### A correction to this auditor's own earlier pass, which is the useful part

In [the companion document's §10](how-a-sound-request-becomes-a-voice.md) this session wrote, of the
inbound-surface census:

> *"the graph has **0** edges the byte decode lacks. It never invents an edge, only omits — so every
> figure in this document is a lower bound."*

**The first clause was true of that population and is not true in general, and the second does not
follow.** Measured across the whole image, the call graph holds **384 edges a direct `E8`/`E9`
decode does not** — indirect and computed calls that Ghidra resolved and a byte scan cannot see.
Over the 177 functions here:

```
edges the GRAPH has that the byte decode lacks :  1     (a resolved indirect call)
edges the BYTES have that the graph lacks      :  8     (thunk JMPs)
```

**Neither route bounds the other. They see different things** — the graph sees resolved indirect
calls, the byte decode sees thunk tail-jumps — and a figure derived from either is a floor with
respect to the other's blind spot, not a floor absolutely. The companion's numbers still move
upward, because for *that* population the graph-only count was genuinely zero; but the general
statement was over-drawn from one measurement and is corrected there as well as here.

> **A property measured on one population is not a property of the instrument.** That is the same
> error as reading six entries of a nineteen-entry table — a boundary observed and then assumed to
> be the edge.

### What this pass did not attack

- §2's play-call disassembly and the two constants — already attacked by §10 and not re-run.
- §8's `Boundary.Audio.NativeSupport` rejection-bucket analysis itself, as opposed to its use in §4.
- The `0215EFxx` block's layout, and §7's three standing unknowns.
- The 206-versus-211 site-count discrepancy §10 recorded rather than reconciled; it remains open and
  this pass adds nothing to it.

## Residual placements — 2026-09-14 (SWE2-FRONTIER, residual-placement package)

| function | size | role (call-signature read) |
|---|---:|---|
| `0028DC00` | 965 | transform-heavy body over `[rdi+0x10..0x80]`: `00202C70` x1, `00202C90` x2/`00202FE0` x1, `00202B10` x1, `00202C50` x1, `00203080` x1, `00202DE0` x2/`00202B90`/`00202D20`/`00202D80` — workbench vocabulary throughout |
| `002C7B10` | 1146 | channel-evaluation mid-layer (caller `002C7660`): `0035D470` context getter x3, `003F0040` slot alloc, `00202C90` x3/`00202DE0`/`00203080`/`00202B10`, `002708B0`, `003F12E0`; fields `[rcx+0x15]`/`+0x4A`/`+0x10`, `[rsi+0x15]`/`+0x16` |

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL.*

**CoreRuntimeScheduling — SERVICE.** The global enable byte read by `003603C0` is also read by the 2,001-byte
field / battle frame body (mode 2). The frame and the play entry `002DF220` consult the same audio enable
([the sound request contract](CONTRACT-sound-request.md), crossings).

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Input — CLIENT and SERVICE, not read.** Two cited sound entries are called by small Input-filed stubs (21 and 25 bytes). Two cited bodies call small Input-filed helpers (30 and 24 bytes). What input state they pass or read is not read here.

- **CombatAction — MECHANICAL (SWE2-EC7-40, 1 edge).** `0032E520`, called by this page's `003DEC90` section body, is also called by a CombatAction-filed body; the file-request family is shared, so that caller is a CLIENT, not an audio dependency.

## SWE2-EC7-34 update (2026-09-19) - `0028DC00`

`0028DC00` (965 B) is a sound-request driver - 0x228 cookie frame, `00202C70`/`00202C90`/`00202DE0`/`00202FE0`/`00202D80` UI-object helpers plus `00203080`. Interior anchor `0028DC45` (an `00202C70` call).

## SWE2-EC7-40 update (2026-09-19) - `003DEC90`

`003DEC90` (375 B) is a sound-call body - `02B59360`/`02B59C20`, `0032E520`/`0035EA30`/`003697F0` pairs plus `002DEE90`/`00379E30`/`003DEB30`. Interior anchor `003DECEF` (a `002DEE90` call).

## SWE2-EC7-42 update (2026-09-19) - `003F12E0`

`003F12E0` (324 B) is a sound-call body - `01F44830`, `00271140`/`00808C40`. Interior anchor `003F13DC` (a `00271140` call).

## SWE2-EC7-48 update (2026-09-19) - `00210FF0`

`00210FF0` (204 B) is a body - `00212A90`/`00212AE0`/`00212B30`/`00212BD0`. Interior anchor `00211019` (a `00212A90` call).

## SWE2-EC7-92 update (2026-09-20) - `00379E30` drain loop measured

`00379E30` (46 B) is the bounded drain the `003DEC90`/`003DEE10`
sound callers run: while `00379E60(ecx)` reports pending work it calls
`0032E040` then `0035EA30(0)` and re-tests — a poll-until-empty, not a
fixed-count loop.
Interior anchor `00379E41` (the `0032E040` call).
