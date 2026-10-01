---
system: Which variation of a sound you hear
category: 18-Audio
status: DOCUMENTED — every register row is closed (owner re-status 2026-09-30, OPUS): ~~the group value and the emitter's use of the entry are not established~~ the group value is answered (UQ-259), the emitter's use of the entry is answered on the trigger page (UQ-262), and the descriptor's other bytes are SUPERSEDED under G-2; the 007CF830 predicate read 2026-09-18 (is a range authored); the SD-24 record identity answered 2026-09-30
owner_layer: PrimaryOwner:Audio
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN159 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). Of the functions classified since GN159 this document cites none of batch R109's 109; the 21 classified before GN160 are named in AUDIT-LOG's batch records and not in a tracked machine-readable list, so identity is not claimed. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md, lineage extension (twenty ledger figures across five generations)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-30
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: first-read-repos-55
  crossref_clean: false
  reopened_count: 0
---

# Which variation of a sound you hear

`007E58D0`, 1,021 bytes. Three documents cited it; none had opened it.

## What the player hears

**A sound trigger that carries several variations does not pick one at random. It cycles them in
order, and the position in the cycle is stored in the trigger itself.**

```asm
007E5BC7  idiv  r12d                        ; (index + 1) % pool size
007E5BD2  mov   byte ptr [rax + 0x1], dl    ; <- written back into the descriptor
007E5BE1  call  0x007BD240                  ; and this one is emitted
```

**One byte at `descriptor + 0x01` is the cursor, and one byte at `descriptor + 0x05` is the count.**
The cursor is advanced modulo the pool size **at the moment a variation is chosen**, so the next
invocation resumes where this one stopped.

> **After the RNG work in this database, the notable thing is what is absent: no draw, no seed, no
> generator.** Repeated footsteps or hits vary because a counter moves, **not because anything is
> rolled** — which also means the sequence is identical on every playthrough and unaffected by
> reloading a save.
>
> *Scoped 2026-09-20 (FABLE): true of this routine and of footsteps. Above the driver, the character's sound emitter
> chooses WHICH trigger to ask for, and for weapon swings and voices it does roll - with ~~the gameplay generator~~ the
> presentation PRNG (`01EF93E8`; corrected 2026-09-29, OPUS, CON-190), with silence among the outcomes - [how an animation makes a sound](how-an-animation-makes-a-sound.md) §2.*

**A cursor left out of range is reset to zero rather than clamped**, so a descriptor edited to an
impossible value starts the cycle over instead of misbehaving: the cursor byte `+1` is loaded and compared with the pool count, and `cmovge` replaces it with 0 when it is at or past the count (`007E5AA8`–`007E5AB4`).

## Two classes of entry, and only one of them cycles

Each entry yields a `u16` key at `+0x04` of a sub-object (`007E5B56`), which is looked up, and the
result is tested by a predicate:

- **predicate true → the entry is emitted immediately**, in the first pass, **every time**;
- **predicate false → the entry joins the round-robin pool**, and exactly **one** pool entry is emitted
  per invocation.

> **So a trigger can hold both unconditional layers and a rotating set**, and the two are distinguished
> by a property of the looked-up object rather than by anything in the entry itself.

## Consecutive entries can be grouped

```asm
007E5B68  call 0x007CF9A0        ; a group value for this entry
007E5B74  call 0x007CF9A0        ; and for the next
007E5B7D  cmp  al, dil
007E5B8B  jnz  ...               ; different -> step back one and stop
```

**A run of consecutive entries sharing one group value is walked as a unit**, with the index stepped
back by one when the run ends so the outer loop resumes correctly. **Both passes do this, with the
same pair of calls in the same order.**

## The sibling: the same descriptor, the other policy

`007BD370`, 357 bytes, was also on the cut and is **the same walk with the selection removed.**

```asm
007BD3D1  mov  rax, qword ptr [rbx + 0x30]   ; the same descriptor
007BD3D7  cmp  byte ptr [rax + 0x5], dil     ; the same count byte
007BD3DB  jbe  ...                           ; zero entries -> nothing
```

It fetches each entry, looks up the same `u16` key at `+0x04`, and hands **every one** of them to the
same emitter `007BD240` — **no predicate, no group runs, no cursor, and nothing written back to the
descriptor.**

> **Two functions over one descriptor format, and the descriptor does not say which applies.** The
> policy is the caller's choice: **`007BD370` emits all entries; `007E58D0` emits the unconditional
> ones and exactly one from the rotating pool.**

**AMENDED 2026-09-03 — there are four, not two.** Two further policies over the same format were read
by `repos-78` and are documented with the functions:

| function | rule |
|---|---|
| `007BD370` | emit **every** entry |
| `007E58D0` | unconditional entries, plus **one** from a rotating pool |
| `007E67C0` | emit entries whose **`[low, high)` range brackets a queried float** |
| `007E6360` | **group consecutive entries by a key byte**, and report per group |

> **The descriptor format is one thing and the selection policy is four. Nothing in the list says which
> rule applies — the policy is the function you call, not a field you read.** A tool that dumps these
> lists **cannot predict how any of them behaves without knowing the caller.**

**The range rule is `low <= v < high`** — `comiss low, v ; ja skip` then `comiss v, high ; jae skip` —
so **adjacent ranges tile without overlap and a value on a boundary belongs to the upper range**, and
the query is fetched **once before the loop**, so every entry is tested against the same number.

**That is why the cursor lives in the descriptor rather than in the trigger** — a descriptor played by
the all-entries function is never advanced, and one played by the cycling function keeps its place
across invocations from anywhere.

## The emitter all four policies converge on

`007BD240`, 303 bytes, four documents. **Every one of the four selection policies hands its chosen
entry here**, so this is where a selected entry becomes an audible voice.

**Two states refuse outright:**

```asm
007BD252  test eax, eax             ; state 0 -> refuse
007BD25A  add  eax, -0x6
007BD25D  cmp  eax, 0x1
007BD260  jbe  refuse               ; states 6 and 7 -> refuse
```

**and the refusal returns `-1` without touching anything** — so a trigger in one of those states emits
nothing and reports it.

**The slot index advances whether or not the voice is acquired:**

```asm
007BD266  movsxd r8, dword ptr [rcx + 0x4c]   ; the slot counter
007BD272  lea    eax, [r8 + 1]
007BD276  mov    dword ptr [rcx + 0x4c], eax  ; incremented BEFORE the acquire
007BD279  lea    rbx, [rcx + r8*8]
```

**The acquire is the next call, and when it returns negative everything after is skipped — but the
counter is already advanced.**

> **A failed emission still consumes a slot index.** Nothing in this function decrements it, and
> nothing bounds it here. **A caller that emits into a full or refusing voice pool leaves the counter
> higher than the number of voices it started.**

**On success**, the trigger is configured by **six calls in fixed order** — one of them run twice with
`0` and `1` — and then started, with an extra parameter taken from `+0x500` **only when the state is 1
or 2** and `0` otherwise. **The same start call is used for every policy; the state chooses what it is
given.** The six are `007BFE30`, `007BFDB0`, `007BFD00`, `007BFEB0` (with 0, then 1), `007BFBA0` and `007BFC30` (`007BD2D8`–`007BD30C`), the parameter operations the trigger page names (G-14); the state test is `dec eax ; cmp eax, 1 ; jbe` (`007BD31F`–`007BD324`), the start is `007E7300` (`007BD333`), and it is also handed the start delay `+0x51C` in every state (`007BD317`; G-18).

## Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Is the cursor really persistent, or a local? | It is **written back to `[descriptor + 0x01]`** at `007E5BD2`, on the object reached through `param_1 + 0x30`. |
| Is the count `+0x05` or a local copy? | **Re-read from `[descriptor + 0x05]` at every loop test** — `007E5B8D` and `007E5BEC` — never cached. |
| Could the modulo be a division used for something else? | `idiv` at `007E5BC7` with the **remainder** (`dl`) stored, three instructions later, into the cursor byte. |
| Is any randomness involved? | **No RNG entry point is called anywhere in the body**, and the emitted entry is selected solely by the cursor. |
| Are the two passes duplicates of one loop? | **No** — the first emits on the predicate being **true**, the second on it being **false**, and only the second writes the cursor. |
| Does the emitter's slot counter really advance on failure? | **Yes** — incremented at `007BD276`, three instructions **before** the acquire whose negative return skips the rest. Two separate instructions, not a compiler reordering of one. |
| Is `state - 6 <= 1` two states or a range? | **Two** — states 6 and 7, expressed as an unsigned compare after a subtract, the same idiom as the actor-kind band. |
| Is the sibling a stripped copy, or a different descriptor format? | **Same format** — `[param_1 + 0x30]`, count at `+0x05`, key at `+0x04`, emitter `007BD240`. It is the same walk **with the selection removed**, not a different structure. |

**Read 2026-09-18 (FABLE): the predicate at `007CF830` asks whether a range is authored.** It takes the container at `[ctx + 8]` (the version byte first), and returns whether the first byte of the version-positioned range field is non-zero — `+4` for versions 0–2, `+0x10` for later versions (`007CF834`–`007CF850`) — the same field the range getters on [the sound-variant page](Sound-Selection/sound-variant-selection.md) (G-2) read as a float, so it is a byte test on that float's low byte, true only when a range was authored. The rest stands.

**What this document does not claim:** ~~what the predicate at `007CF830` tests,~~ ~~what the group value at
`007CF9A0` represents, what `007BD240` does with the entry it is handed,~~ ~~what the `u16` key indexes,~~ ~~or
what the other bytes of the descriptor hold.~~ *(Corrected 2026-09-30, SWE2-DATA: all four are answered elsewhere. The group value is the entry's group id (UQ-259, [the sound-trigger page](Sound-Selection/sound-trigger.md)); what `007BD240` does with the entry is read whole there (UQ-262: state gate, slot, bind, the seven parameter operations, the arm); the descriptor's consumed fields are placed and its varying bytes profiled — G-2, SUPERSEDED 2026-09-27 (OPUS, class-1 ruling), on [the sound-variant page](Sound-Selection/sound-variant-selection.md) §7 and §12; which record class it is, `SabFile::Sound` or `SabFile::Sequence`, is `SD-24`.)* What this page does not claim is anything about which of these policies the shipped data exercises: every shipped sound record builds the base `Sound`, so of the four policies only `007BD370` runs ([the sound-variant page](Sound-Selection/sound-variant-selection.md) §12).

**Placed 2026-09-18 (FABLE):** the `u16` key is the ordinal of a `SabFile::Sequence` record in the same bank's `seq ` chunk; `007CF9E0` is that chunk's bounds-checked get-by-index (UQ-250 on [the sound-request page](Audio-Boundary/how-a-sound-request-becomes-a-voice.md) §12). The group value is answered as UQ-259 and the trigger is described on [the sound-trigger page](Sound-Selection/sound-trigger.md).

## Key addresses (SWE2-DATA, 2026-09-30)

| Address | What | Where |
|---|---|---|
| `007E58D0` | `OrderSound` select (slot 43): the unconditional pass and the one-per-call cursor | the top of this page |
| `007BD370` | base `Sound` select (slot 43): emit every entry | "The sibling" |
| `007E67C0` | `SwitchSound` select: `low <= v < high` | "The sibling" table |
| `007E6360` | `CycleSound` select: groups by key byte | "The sibling" table |
| `007BD240` | the emitter all four converge on | "The emitter" |
| `007CF9A0` | the group byte (UQ-259) | "Consecutive entries can be grouped" |
| `007CF830` | is a range authored (a byte test on the range field) | "Read 2026-09-18" |
| `007CF9E0` | a `seq ` chunk's get-by-index (UQ-250) | "Placed 2026-09-18" |
| `007E7300` | the sequence arm the emitter starts | "The emitter" |

## Data structures (SWE2-DATA, 2026-09-30)

The descriptor is the record at the sound's `this + 0x30`. `007E58D0` wraps it with the descriptor `01CB43E0`
(`007E5939`–`007E593D`), `SabFile::Sound` by its RTTI ([the sound-variant page](Sound-Selection/sound-variant-selection.md)
§12); ~~that page's G-2 narrowing of 2026-09-18 calls the same record the `SabFile::Sequence`, and which is right is~~
~~`SD-24`.~~ *(Corrected 2026-09-30, SWE2-DATA: `SD-24` is answered: it is the `Sound` record. The entry table sits at its `u16 +0x1A` (version 16), and that page's G-2 narrowing is corrected (§7). Control `_index/candidates/dd-leftovers-0930/sd24_record.py`.)* The fields this page reads:

```
+0x01  u8   the round-robin cursor, written back at 007E5BD2; reset to 0 when at or past the pool count (007E5AA8-007E5AB4)
+0x05  u8   the entry count, re-read at every loop test (007E5B8D, 007E5BEC)
entry  16 bytes (SabFile::SoundSequenceInfo); its u16 +0x04 is the key, the ordinal of a Sequence in the same bank (UQ-250)
```

The emitter's own fields — the lifecycle state `+0x54`, the slot counter `+0x4C` and slots `+0x400`, the start
offset `+0x500` and the start delay `+0x51C` — are tabled on [the sound-trigger page](Sound-Selection/sound-trigger.md) §4.

## Call chain (SWE2-DATA, 2026-09-30)

```
007BD120  the sound-instance stepper -> call [vtable + 0x158] (slot 43, 007BD205; virtual)
  -> 007E58D0 (Order) | 007BD370 (base) | 007E5160 (Random) | 007E6360 (Cycle) | 007E67C0 (Switch)
    -> 007BD240  the emitter   (from 007E58D0 at 007E59DA, 007E5A6D, 007E5BE1, 007E5C61; from 007BD370 at 007BD46D)
      -> 007E7300  the sequence arm (007BD333)
```

Every `007BD240` call site found by the raw `E8`/`E9` index (14) lies in one of the five selects or the Cycle helper
`007E5E80`; the selects themselves have no direct caller and are reached only through slot 43 of their vtables
([the architecture page](sqex-sd-sound-driver-architecture.md) §9). Upstream of the stepper is
[how a sound request becomes a voice](Audio-Boundary/how-a-sound-request-becomes-a-voice.md) (UQ-251).

## Modding notes (SWE2-DATA, 2026-09-30)

- **The cursor is data.** A sound's position in its rotation is the byte `+1` of the record at `this + 0x30`, so it
  survives across triggers and is shared by every trigger of that record; resetting it to 0 restarts the rotation.
- **None of this runs on shipped banks.** Every shipped sound record builds the base `Sound`, whose select emits every
  entry ([the sound-variant page](Sound-Selection/sound-variant-selection.md) §12): to make a sound rotate, a bank
  edit must also set the record's class byte `+4` to 3 (`OrderSound`).

## Evidence (SWE2-DATA, 2026-09-30)

| Claim | Evidence | Tier |
|---|---|---|
| The cursor is `+1`, advanced modulo the pool size and written back | `007E5BB9`–`007E5BD2` | 1 |
| An out-of-range cursor restarts at 0 | `007E5AA8`–`007E5AB4` | 1 |
| Unconditional entries play every time; one pool entry per call | the two passes of `007E58D0` (falsification table) | 1 |
| `007BD370` emits every entry | `007BD3D1`–`007BD3DB` and its single `007BD240` call | 1 |
| The emitter consumes a slot index before the acquire | `007BD266`–`007BD276` | 1 |
| The emitter's six configuration calls and the state-dependent start | `007BD2D8`–`007BD333` | 1 |
| Only the base `Sound` is built from shipped data | the class-byte census on [the sound-variant page](Sound-Selection/sound-variant-selection.md) §12 | 1 + data |

## Related (SWE2-DATA, 2026-09-30)

- [the sound-variant page](Sound-Selection/sound-variant-selection.md) — the four rules and the class selector
- [the sound-trigger page](Sound-Selection/sound-trigger.md) — the emitter read whole
- [how a sound request becomes a voice](Audio-Boundary/how-a-sound-request-becomes-a-voice.md) — the key, the stepper
- [the architecture page](sqex-sd-sound-driver-architecture.md) — the vtables
