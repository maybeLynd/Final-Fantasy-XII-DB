---
system: The character render record array
category: 17-Presentation-Rendering
status: DOCUMENTED — every register row is closed or dispositioned and the page's residue is answered (owner re-status 2026-09-30, OPUS, on SWE2-STRUCT's DD batch 12) — the rest of the 0x740 record (UQ-196) is SUPERSEDED as a duplicate of BT-2, itself SUPERSEDED 2026-09-27 under FRONTIER's class-1 ruling (fields.tsv tiles all 1,856 bytes; the DISCOVERED spans are the static-FIELDS work); the rest of the 0x130 tail (UQ-197) is SUPERSEDED as a duplicate of BT-3, answered 2026-09-26; pool exhaustion (UQ-198) is SUPERSEDED as a duplicate of BT-5, answered 2026-09-18 (160 records, 160 slots, one per promotion; an exhausted allocation would store handle 0 and every consumer guards on it); the subtype meanings (BT-4) answered 2026-09-27 (each is the motion slot it plays: revive, c_turbo, active, deact); BT-6 answered 2026-09-17 with its premise corrected; the three special bones' roles and +0x414 (write-only on PC) answered 2026-09-30 (swe2struct-ddres-b12-0930)
owner_layer: PrimaryOwner:Presentation
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN158 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). Of the functions classified since GN158 this document cites `001D76A0`, `001D7DD0`; the 21 classified before GN160 are named in AUDIT-LOG's batch records and not in a tracked machine-readable list, so identity is not claimed. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md, lineage extension (twenty ledger figures across five generations)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-02
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: GN158 checkpoint 2ed8affb… / snapshot 46f02e26…, project GFZ_HD2
  falsification_passes: 1
  last_falsification: 2026-09-03
  last_falsification_by: repos-d2
  falsification_result: 1 claim overturned, 6 survived — see section 10
  crossref_clean: false
  reopened_count: 0
---

# The character render record array

> The fixed pool of 160 slots that every visible character occupies, the linked list that says which
> are alive, and the one function where Presentation reaches back into Movement and changes how fast
> a character is walking.

## 1. What the player sees

FFXII can only draw so many characters at once. There is a **fixed pool of 160 slots**, allocated
once at startup and never grown, and every visible character — party, enemies, NPCs, summons — must
occupy one. Nothing appears on screen without one.

The player-visible consequence is one you have felt without knowing its cause: when a zone is very
busy, the game does not slow down indefinitely. It runs out of slots and stops adding characters. The
budget is decided at startup, not per zone.

The other thing this system does is stranger and easier to notice once you know. **Presentation can
override how fast a character appears to be moving.** When a character stops, this code keeps feeding
the *previous* heading and a decaying speed back into the movement system for a short while, so the
character glides to a halt rather than stopping dead on the frame the input ended. And one class of
object has its speed forced to exactly zero regardless of what movement asked for.

## 2. Native mechanism

### One allocation, at startup, never grown

`CharacterRenderSystem_AllocateAndInitialize` (`003325D0`) does the whole thing in eight calls:

```c
g_pCharacterRenderRecordArray = allocate(0x48930);
...
RenderResourceRoot_InitializeSubcontainers(ctx, 10, 10, 5, 5, 0x13, 0x2A00, 0x16000);
CharacterRenderSystem_Initialize();
FUN_00426480(0xA0, ctx);
```

The size decomposes exactly, and this is arithmetic rather than a claim:

```
0x48930  total allocation
0x48800  = 160 * 0x740   the records
0x00130  the system-state tail that follows them
```

**160 is not stored anywhere as a capacity** — but it **is enforced**, as an immediate, see §10. It is a consequence of the allocation size divided by
the record stride. `FUN_00426480` is passed `0xA0` (160) and **never uses the argument** — its entire
body encodes the *other* parameter and stores it at the tail:

```c
*(dword *)(g_pCharacterRenderRecordArray + 0x48830) = EncodeImageAddress(param_2);
```

So a reader looking for where the capacity is registered will not find it. The pool size lives in the
allocation constant and nowhere else — which matters if you want to change it.

### Which slots are alive: an intrusive list, not a scan

Records are not swept. The tail holds the head of a **linked list threaded through the records
themselves**, and `FUN_00426420` walks it:

```c
if (tail[0x42] == 1 && tail[0x43] == 0)                  /* the system gate */
    for (i = *(int *)(base + 0x48800); i != -1;
         i = *(short *)(base + i * 0x740 + 4))            /* next index, in the record */
        Reconcile(base + i * 0x740);
```

The list head is a 32-bit index at the very start of the tail; each record's **`+0x04` is a 16-bit
index of the next live record**; `-1` terminates. A record's `+0x00` is a 16-bit id which is `-1`
when the slot is not in use~~, and every consumer tests that first~~; the id is not a validity test every consumer makes first - the list walks select by link, and the allocator publishes a new slot into the pending list before it writes the id *(corrected 2026-10-02, FABLE, Claude Opus 5.5: see section 11a)*.

That is why the whole system costs nothing when the world is empty: an empty list is one comparison,
not 160.

### Presentation reaching back into Movement

`Movement_ModifyHeadingSpeedForObjectState` (`00424080`) is the seam, and it is the reason this array
matters outside rendering. Movement hands it a heading and a speed **by pointer**, and it may
substitute both:

```c
rec = g_pCharacterRenderRecordArray + object_index * 0x740;
if (rec->id16 == -1) return;                  /* slot not in use */
subtype = rec->u16_at_0xCC & 0xFFF;
```

**When the coast-down latch is set** (`+0x62C` bit 0), the record drives movement outright:

```c
rec->cachedSpeed  *= 0.83f;                   /* +0x624 */
*heading = rec->cachedHeading;                /* +0x620 */
*speed   = rec->cachedSpeed;
if (rec->cachedSpeed <= 0.05f)
    rec->flags_0x62C &= ~1;                   /* latch releases */
```

So a stopped character coasts: the speed is multiplied by `0.83` every call until it drops below
`0.05`, then the latch clears and movement resumes control. That is the glide-to-a-halt in §1, and
the two constants are the whole of its feel.

**When the latch is clear**, the record instead *caches* the current heading and speed for next time,
and the latch is armed only under a narrow condition — object flag `0x08000000` set, `+0x06` equal to
`-1`, subtype exactly `0x10`, the incoming speed exactly `0.0`, and a per-record counter at `+0x457`
having reached `_DAT_01DFE0B4 * 30`. That last term is the frame-count member of the time-base triple.

### Subtype-specific speed rules

A second, independent branch runs when the record has a resolved presentation entry
(`+0xC4 != -1`) whose derived resource reports `1` at its second byte:

```c
if (subtype == 0x35 || subtype == 0x36) {     /* (subtype - 0x35) < 2 */
    rec->scale_0x618 *= 0.9f;
    *speed = rec->scale_0x618 * *speed;       /* the NEW value, post-multiply */
} else if (subtype == 0x0D) {
    *speed = 0.0f;                            /* forced stop */
} else {
    rec->scale_0x618 = 1.0f;                  /* reset */
}
```

Subtype `0x0D` is the forced-stop class from §1. Note the `0x35`/`0x36` case reads the *already
multiplied* value, so the decay compounds with itself within the frame.

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `003325D0` | `CharacterRenderSystem_AllocateAndInitialize` | 139 B | the single allocation of `0x48930`; publishes the array pointer |
| `00426480` | `CharacterRenderSystem_PublishRootPointer` | — | writes the encoded root at tail `+0x30`; **ignores its `0xA0` argument** |
| `00426420` | `CharacterRenderSystem_ReconcileActiveRecords` | — | walks the intrusive active list under the system gate |
| `00426340` | `CharacterRenderRecord_SyncShadowObjects` | 211 B | **read 2026-09-12 (BT-1, §13)** — per active record, gates the record's two shadow objects on its state and pushes the scripted or computed shadow LOD |
| `00424080` | `Movement_ModifyHeadingSpeedForObjectState` | 427 B | the Presentation→Movement seam: coast-down latch and subtype speed rules |
| `0036A100` | pool allocator | — | `Boundary.CrossSubsystem.NativeSupport`; writes a header at `-0x3E`/`-0x10`/`-0x02` |

Addresses are Ghidra image base `0x00120000`. Every row above is a function.

### Data addresses cited by this document

| Address | Name | Kind | Contents |
|---|---|---|---|
| `022C6F28` | `g_pCharacterRenderRecordArray` | pointer | the pool base — **639 references image-wide** |
| `022C6F20` | render context | pointer | the context passed to the allocator, published first |
| `01DFE0B4` | frame-count time base | `u32` | `× 30` gives the latch-arming threshold |

## 4. Data structures and formulas

### The allocation

```
base + 0x00000 .. 0x487FF   160 records, stride 0x740 (1,856 bytes)
base + 0x48800 .. 0x4892F   system-state tail, 0x130 bytes
  tail +0x00   i32   headActiveIndex     -1 = no live records
  tail +0x04   i32   tailActiveIndex     -1 when empty (section 11, 2026-09-11)
  tail +0x08   i32   nextFreeIndex       the allocator's scan cursor
  tail +0x0C   i32   liveCount           the allocator refuses at 160
  tail +0x10   i32   headPendingIndex    records allocated but not yet promoted
  tail +0x14   i32   tailPendingIndex
  tail +0x30   u32   encodedRootPointer  written by 00426480
  tail +0x42   u8    gateEnabled         reconcile requires == 1
  tail +0x43   u8    gateInhibit         reconcile requires == 0
```

### The record — fields proven by the functions read here

**These are BYTE offsets.** The decompiler renders the record through a `short *`, so its subscripts
are 2-byte indices; every offset below is the subscript doubled. Transcribing the subscripts directly
would be the index-as-offset defect that `check_layout_units.py` exists to catch.

```
CharacterRenderRecord -- 0x740 bytes
  +0x000  i16   id                 -1 when the slot is free (was 'every consumer tests this first' - corrected 2026-10-02, section 11a)
  +0x002  i16   prevActiveIndex    intrusive list link back, -1 at the head (section 11)
  +0x004  i16   nextActiveIndex    intrusive list link, -1 terminates
  +0x006  i16   (tested == -1 as a latch precondition)   <- corrected 2026-10-02, OPUS - the piece's owner-record link, -1 = unattached (CONTRACT-coast-down-latch.md section 15 row, answered 2026-09-22)
  +0x010  ptr   encodedContextPtr   8-byte pointer, stored whole (was listed u32 - corrected 2026-09-27, see below)
  +0x0C4  i32   presentationEntryId -1 when absent
  +0x0CC  u16   subtype             used as (subtype & 0xFFF)
  +0x284  u32   objectFlags         bit 0x08000000 gates the latch
  +0x457  i8    stopFrameCounter    compared against DAT_01DFE0B4 * 30
  +0x610  f32   liveHeading         the cache source
  +0x614  f32   liveSpeed
  +0x618  f32   speedScale          the 0.9 decay / 1.0 reset target
  +0x620  f32   cachedHeading       what the latch replays
  +0x624  f32   cachedSpeed         multiplied by 0.83 per call
  +0x628  f32   (copied alongside cachedSpeed)
  +0x62C  u16   flags               bit 0 = coast-down latch active
```

*Corrected 2026-09-27 (FABLE, Claude Opus 5.5), on OPUS-NOTICE-FABLE-CRR-PLUS10-IS-8-BYTES: `+0x010` was listed `u32`. It is an 8-byte pointer stored whole - the only writer, `0042055B` in `00420480`, stores `0020E600`'s 64-bit return (sole caller `004279B0`), and `0042DA5C` dereferences the qword directly; the 145 dword readers pass the low half back through `0020E600`. [Record](../../_index/candidates/crr-context-ptr-width/README.md) (OPUS, `b4b5f347b`).*


> *Added 2026-09-12 (FABLE, K-13; static, from `003EC260` and `00420A40`):* **`+0x120..+0x12C`** are
> four floats `{pitch, yaw, roll = 0, 1.0}` — the actor's `+0xAC` and `+0xA8` angles as
> `FUN_003EC260` stores them (`003EC348`–`003EC358`), with the previous values kept at
> **`+0x250..+0x258`**; `CharacterRenderRecord_ComposeModelTransformFromParent` turns the three
> angles into the **model rotation matrix at `+0x180`** through `Matrix4x4f_BuildEulerRotation`
> (`0046D380`, X-Y-Z order, Y up) before scale and parent composition — see
> [the heading page](../../06-Movement-And-Navigation/heading-speed-to-position-delta.md).

### Record count

```
recordCount = 0x48800 / 0x740 = 296960 / 1856 = 160
```

Not read from a field. The `0xA0` passed to `00426480` is an unused argument.

### The active-record walk

```c
if (tail.gateEnabled != 1 || tail.gateInhibit != 0) return;
for (i = tail.headActiveIndex; i != -1; i = record[i].nextActiveIndex)
    Reconcile(&record[i]);
```

### The coast-down latch, exactly

```c
/* latch set */
cachedSpeed *= 0.83f;
*heading = cachedHeading;
*speed   = cachedSpeed;
if (cachedSpeed <= 0.05f) flags &= ~1;

/* latch clear, and armed only when ALL of: */
(objectFlags & 0x08000000) != 0
&& field_0x006 == -1
&& subtype == 0x10
&& *speed == 0.0f
&& (u32)stopFrameCounter >= (u32)(DAT_01DFE0B4 * 30)
   -> cachedHeading = liveHeading; cachedSpeed = liveSpeed; flags |= 1;   // <- corrected 2026-10-02, OPUS - arming replays the CACHED pair (+0x620 heading, +0x624 speed times 0.83) to the caller and sets +0x62C bit 0 (00424080+0xD8..+0xFB); the live-to-cache copy runs only when the test fails (00424080+0x105)
```

From `0.83` per call and a `0.05` floor: a speed of `1.0` takes `ceil(log(0.05)/log(0.83)) = 17`
calls to release the latch.

### Subtype speed rules

```c
if ((u32)(subtype - 0x35) < 2) { speedScale *= 0.9f; *speed = speedScale * *speed; }
else if (subtype == 0x0D)      { *speed = 0.0f; }
else                           { speedScale = 1.0f; }
```

## 5. Call chain

```
startup
  -> CharacterRenderSystem_AllocateAndInitialize  003325D0   [creates the pool]
     -> allocate(0x48930)                          0036A100
     -> CharacterRenderSystem_Initialize
     -> CharacterRenderSystem_PublishRootPointer   00426480

per frame, Presentation
  -> CharacterRenderSystem_ReconcileActiveRecords  00426420
     -> gate: tail+0x42 == 1 && tail+0x43 == 0
     -> walk the intrusive active list
        -> per-record shadow sync 00426340   [read - section 13]
           -> 003B6900 / 003AFD00   mode bits on the two shadow objects
           -> 003B5980 -> 003B6B80  computed shadow LOD, or the record's +0x27C

per frame, Movement
  -> Movement_ModifyHeadingSpeedForObjectState     00424080   [NOT AN OWNER TRANSITION: the only
     |                                                         caller 002E4380 is Movement as well]
     -> add rbx, [022C6F28] at 00424098            [DATA REACH, not an owner transition: no call]
     -> PresentationEntryReferenceContainer_ResolveEntryById
        0051B9E0 (thunk) -> 0051F240               [TRIGGER 06 -> 17]
     -> substitutes *heading and *speed by pointer
```

### 5a. The seam is real, but it is not where the marker put it

Until 2026-09-18 the row above read `[OWNER TRANSITION, Presentation -> Movement]`, and that marker
was wrong in both of its parts. It survived because *"the `Presentation→Movement` seam"* is a true
sentence about this function and the marker looks like a restatement of it. It is not: **the sentence
is about data and the marker is about a call.**

*It is not a transition.* `00424080` has **exactly one caller in the image, `002E4380`**
(`Movement_ComputeDeltaFromHeadingSpeed`), and the classification store gives `owner=Movement` for
both. Same owner on both sides of the hop, which rule 6's own checker rejects as malformed when it
is written out (`[TRIGGER 22 -> 22]`).

*And the direction was reversed.* Whatever else crosses here, the **call** goes from Movement into
this body, never the other way; `002E4380`'s own only caller is `002E5030`, also Movement.

What is genuinely Presentation's reaches this function two ways, and only one of them is a hop:

| what | where | kind |
|---|---|---|
| the `0x740`-stride array base `022C6F28` | one load, `00424098`, `add rbx, qword ptr [rip+0x1EA2E89]` | a read of another owner's global **with no call at all** |
| `PresentationEntryReferenceContainer_ResolveEntryById` | `0051B9E0`, a 5-byte `jmp` thunk (`final_no_owner`, `thunk`) onto `0051F240`, 138 B, `owner=Presentation` | the transition, one hop **below** where the marker sat |

**`TRIGGER`, not `AUTHORITY`, and the body is the reason.** `0051F240` sign-extends a two-bit mode
from `[container+4]` (`shl r8d,0x1e` / `sar r8d,0x1e`), takes the entry array either directly
(`mode 1`) or through `003AB7F0` (`mode 0`), indexes it by `id * 0x30`
(`lea rbx,[rcx+rcx*2]; shl rbx,4`), returns `0` for any other mode, and — when `byte[entry] & 2` —
lazily rebinds `[entry+0x18] = 003AB7F0([entry+0x10]) + [entry+0x20]` before returning
`[entry+0x18]`. **Every decision in it is about where the entry lives, none about what the heading
or the speed becomes.** The coast-down latch, the `0.83` decay, the `0.05` floor and the subtype
rules including `0x0D -> speed 0` are all in `00424080`, on the Movement side. Presentation is asked
where something is; it does not decide the outcome. Under rule 6 that is control crossing, and the
lazy rebind is Presentation writing its **own** record, which does not change the label.

**Upstream:** the movement update supplies the index and the two pointers. **Downstream:** whatever
consumes the modified heading and speed — this function writes through the caller's pointers, so its
effect is felt in
[`../../06-Movement-And-Navigation/heading-speed-to-position-delta.md`](../../06-Movement-And-Navigation/heading-speed-to-position-delta.md),
whose spherical decomposition consumes exactly these two values.

**Do not confuse with:**

- **`CharacterRenderObject` is a different thing.** That class is `0x668` bytes with a vtable pointer
  first and is allocated per object; this array is `0x740`-stride records with an `i16` id first, in
  one block. **No function in the image references both** the class vtable and this array base. See
  [`../Character-Rendering/character-render-object.md`](../Character-Rendering/character-render-object.md).
- **The `0xA0` argument to `00426480` is not a capacity registration.** It is unused.

## 6. Modding notes

- **Best intervention point:** the allocation constant `0x48930` in `003325D0`, if you want a larger
  pool — but it must stay `count * 0x740 + 0x130`, because the tail is addressed at fixed absolute
  offsets from the base (`+0x48800`, `+0x48830`, `+0x48842`) **compiled into every consumer**.
  Changing the count without rebuilding those offsets moves the tail out from under 639 references.
- **Regenerates itself:** `cachedHeading`/`cachedSpeed` are re-cached from live values whenever the
  latch is clear. Writing them while the latch is clear achieves nothing.
- **Breaks if:**
  - You raise the record count and expect `0xA0` to matter. It is ignored; the pool size is the
    allocation size.
  - You treat the decompiler's `short *` subscripts as byte offsets. Every offset in §4 is doubled
    from what the decompilation prints.
  - You clear the tail gate at `+0x48842`. Reconciliation stops for every character at once.
- **Multiplayer / XIIOnline:** slot indices are **local allocations** — the same character will hold
  different indices on different clients, so an index must never cross the wire. The coast-down latch
  is local presentation smoothing and should be allowed to run independently per client; replicating
  it would fight each client's own interpolation.
- **Mod compatibility:** the subtype values (`0x0D`, `0x10`, `0x35`, `0x36`) ~~are authored per object;
  changing an object's subtype changes which speed rule it gets, with no code change~~ *(corrected 2026-09-27, FABLE, Claude Opus 5.5: they are event indices the engine posts - revival, the mount's turbo, the combat-stance change - and script verbs can post them too. What is authored is the motion each character's container holds at that slot, so replacing its `revive`, `c_turbo`, `active` or `deact` block changes what plays under the rule, not the rule; [record](../../_index/candidates/bt4-event-motion-slots/README.md))*.

## 7. What is not known

- [x] ~~What `00426340`, the per-record reconcile callee, actually does. It is the body of the per-frame
      pass and is unread.~~ **BT-1 ANSWERED 2026-09-12 (FABLE): it is the per-record shadow sync** —
      see §13.
- [x] **UQ-196.** **BT-2.** The other ~1,700 bytes of the `0x740` record. This document proves 14 fields. *(One question, two ids: `BT-2` is the elder and carries the residue - labelled 2026-09-27, FABLE, Claude Opus 5.5.)*
      **Narrowed 2026-09-18 (FABLE): the record's occupancy, its default map and its bind.* The bullet's *fourteen fields* predates the tiers above; what was still missing was a measure of the whole record and the initializer's own reading of it. **Occupancy.** Over this page's `character-render-record-accesses.tsv` (3,381 sites, 545 functions) the record has **368 distinct accessed offsets covering 1,523 of its 1,856 bytes**; the untouched bytes total 333, and the only runs of sixteen or more are `+0x70`..`+0x8F` (32), `+0x398`..`+0x3B3` (28), `+0x3D5`..`+0x3F3` (31), `+0x458`..`+0x47F` (40) and `+0x4F6`..`+0x52F` (58) — so about a fifth of the record is padding or reached only through pointers the census does not route. **The default map**, from `CharacterRenderRecord_ResetDefaults` (`0041F730`: `memset(record, 0, 0x740)` at `0041F754`, then the seeds): the `−1` sentinels at `+0x00`..`+0x0A` (six words), `+0x18`, `+0x64`, `+0xC4`, `+0xC8`, `+0xCC`, `+0xCE`, `+0x24C`, `+0x288`, `+0x2AC`, `+0x2C4`, `+0x2F0`, `+0x2F8`, `+0x408`, `+0x40F`, `+0x434`, `+0x450`, `+0x718`, the `0xFFFF` at `+0x60` and the word pairs `{−1, 0}` at `+0x438` and `+0x440`; the dword `0xF` at `+0x2A0`; eight **`{0, 0, 0, 1}` vec4s** at `+0x120`, `+0x130`, `+0x140`, `+0x150`, `+0x200`, `+0x310`, `+0x320` and `+0x630`; three **`{1, 1, 1, 1}` vec4s** at `+0x160`, `+0x170` and `+0x330`; `1.0` triples at `+0x210` and `+0x220` through the four-float setter `006C0520` (the fourth from the stack slot, also `1.0`); **identity matrices at `+0x180` and `+0x1C0`** (`0046D110` copies the constant matrix `01F204E0` through `00202C70`); a **seven-float ladder `100, 200, … 700` at `+0xA4`..`+0xBC`** behind `+0xA0 = 0` (no direct reader in the census — indexed, or dead); the five small constants `+0x414 = 1/6`, `+0x41C = 1/90`, `+0x420 = 1/75`, `+0x424 = 1/15`, `+0x428 = 0.2`; `+0x4A8 = 1.0`, `+0x4B0 = 0.03`; the four bytes `03 03 05 03` at `+0x2F4`; `+0x738 = 1`; and Q12 channel 0 set to `1.0` through `003E5D00(record, 0, 1.0)`. **The bind.** `0041FCF0` (939 B, unnamed) seeds the eight `+0x90` words to `−1`, `+0x41A = 0x10`, clears `+0xC0` bits 3–4 and `+0x304` bits 0 and 14, ors `0x20100004` into `+0x284`, resolves the record's context (`+0x10` → `ImageAddress_ResolveRuntimePointer` → holder `+0xD90`, the resource entry) and finds the model's sections **by tag and the name at `+0x3C`**: **`@FRP`** → the word `+0x408` (`0041FDB2`), **`@FCP`** → the payload pointer `+0x400` (`0041FDF0`..`0041FE1A`), **`@FMC`** → `+0x2FA` (`0041FE7E`), **`@FLD`** → `+0x2C0` and, when found, a loop over its `0x30`-byte entries calling `0041F340` per entry to fill the `+0x90` words with the count in `+0xC2` (`0041FFC0`..`0041FFE8`; one synthetic entry when absent), after which `+0x64` takes word 0; then `+0x26C` from `00504740`, bit 26 of `+0x284` set and bit 27 cleared, `0046C1E0(+0x5F0, id)` and the heading cache `+0x610`..`+0x628` reset. `00420480` adds **`@FOR`** → the byte `+0x6A0` from the section's `+0x38`. **Two per-model constants by name.** `00420480` compares the name against a literal table at `00D12314`: `+0x73C = 1` for `m1181`, `m1201`, `m1002`, `m1194` (else 0); and **`+0x734`** — the tier's `kindTunedFloat` — is chosen by directory letter and name: `s0011` 2.0, `s0012` 1.7, `s0004` 2.0, `s0013` 1.3, `s0005` 1.3, other `s` 1.5; `m1015` 1.5, `m1198` 2.0, `m1231` 2.0, other `m` 1.2; `n1196` 1.6, other `n` 1.1; everything else 1.0 (`00420646`..`0042082C`). What remains: the meaning of the constant blocks (the ladder, the five reciprocals, `03 03 05 03`) and of the 333 untouched bytes. Static: the TSV census, the two bodies.*
      *SUPERSEDED 2026-09-27 (FABLE, Claude Opus 5.5) in the register (OPUS, cd73ae1d5) under FRONTIER's class-1 ruling (batch-K Extension 2026-09-27c): `fields.tsv` tiles all 1,856 bytes of CharacterRenderRecord across 343 rows; the residue is the DISCOVERED spans, carried by OPUS's static-FIELDS work. Ticked on OPUS-NOTICE-FABLE-TICK-FIVE-SUPERSEDED-BOXES.*
- [x] **UQ-197.** The remaining `0x130` tail beyond the four fields read. *(closed — the register row is ~~WITHDRAWN~~ SUPERSEDED as a duplicate of `BT-3` *(corrected 2026-10-02, OPUS: the register's UQ-197 row and the front matter say SUPERSEDED)*.)*
- [x] **BT-4.** **What the subtypes mean.** `0x0D` forces a stop, `0x10` arms the latch, `0x35`/`0x36` decay —
      four values out of a 12-bit field, with no authored names.
      *Narrowed 2026-09-15 (FABLE, static): the "subtype" is the index half of the record's current render event.*
      - **What `+0xCC` is.** It is the signed word that [the render-event selection evidence](render-event-selection-evidence.md)
        reads as the *current event*: bits 12–15 are a kind and the low 12 bits an index. The priority bytes at `01F00410`
        are indexed by the same 12 bits.
      - **The store read here** is `00424D80` at `00424FAB`, which writes its fourth argument, the candidate event.
        - The per-frame path reaches it: `RenderRecords_ProcessDirtyState` (`00427DE0`) → `0042AC30` → `00423B10` →
          `00424D80`. `00423B10` tests its candidate against `0x2009` and `0x2031` by value before the call.
        - The same function swaps `0x2005` into `+0xCC` around a selector-2 check (`00424E61` / `00424E8B`).
        - `00427320` compares the word's low 12 bits against `0x35` / `0x36` (`00427705`–`00427719`).
      - **So the four speed rules key on event indices, not on a separate object type:** `0x0D` stops the object, index
        `0x10` is the only one that can arm the coast-down latch, and `0x35` / `0x36` are the indices the selection policy
        normalizes kind-4 events to (`0x2035` / `0x2036`).
      - **A lead, not traced:** the battle-mode mount's turbo posts actor event `0x2010`, index `0x10`, when it starts
        ([the mode ladder](../../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md)). Whether that
        post is the event stored here was not followed.
      - ~~**Still open:** what each index is on screen. No name table for the event indices has been found.~~
      ***ANSWERED 2026-09-27, FABLE, Claude Opus 5.5, static plus the shipped data: each index is the slot of the motion it plays, and the name table is the character's own motion container.** `00424D80` stores the event into the presentation entry's word `+0x31C` beside `+0xCC` (`00424FA4` / `00424FAB`). The entry resolves `+0x31C & 0xFFF` as a child slot of its `.ca` `@FRP` container, 80 event slots per bank, and keeps that child as its `@FMC` motion block. Across all 1,195 version-1 `.ca` files every slot carries one name: **`0x0D` `revive`**, **`0x10` `c_turbo`**, **`0x35` `active`**, **`0x36` `deact`**. The posters agree. `0x200D` is posted when a unit's terminal statuses have all cleared, and to the target the ability Spawn moves to its caster. `0x2010` replaces the ordinary `0x2001` (`ready`) for the mount while turbo is on - the lead above, now traced. `0x4035` / `0x4036` come from entering and leaving the party combat stance. So a reviving or appearing unit stands still, a mount stopped out of a turbo run glides to a halt, and a character drawing or sheathing its weapon slows by 0.9 per call. The other 47 slots (`damage`, `dead`, `stn`, `poach`, `steal`, `attack` ...) are in the record's `event-slot-names.tsv`. [Record and control](../../_index/candidates/bt4-event-motion-slots/README.md) (8 checks, FAILS 0).*
- [x] **UQ-198.** Whether the pool ever actually exhausts in normal play, and what happens when it does. The
      160-slot budget is proven; its behaviour at the limit is not.
      ***ANSWERED 2026-09-18 (FABLE) — it cannot exhaust under the lifecycle, and if it did the character would simply draw without its shadow objects.** *Why it cannot:* the record array holds exactly 160 records (`0x48800 / 0x740`, the count this page derives) and the pool has exactly 160 slots (`0xA0`, the allocator's loop bound at `003B56FF`); the only allocation site is the promotion `00428710`, which takes one slot per record (`003B56D0(record.id)` at `00428785`) and only when `003E68E0` says the record carries an FCP payload whose first byte is non-zero (`003E68E4`..`003E68F7`); retirement frees the slot through `003B6000`. One slot per promoted record and as many slots as records means the scan can never find all 160 taken unless a record were promoted twice without retiring, which the lifecycle contract's step order excludes. *What would happen:* `003B56D0` walks the `0xE0`-byte entries testing bit 0 of `+0x40` (`003B56F0`..`003B5705`) and, finding none free, returns 0 (`003B5707`); the promotion stores that 0 into `+0x114` without a test (`0042878A`); and every consumer of `+0x114` guards on a non-zero handle before touching the entry (the shadow verbs above, `003B6900(handle, 6)` / `(handle, 4)`), so nothing dereferences a missing entry and the character renders without the shadow objects the entry would carry. A valid handle is never 0 by construction: it is the generation shifted left by 8 with the slot in the low byte, and the generation counter `02B40520` wrapping from `0xFFFFFF` to 1 (`003B5724`..`003B574D`). Static: the allocator, the promotion, the predicate, the record count. *(BT-5 is the register's id for this box.)**
- [x] ~~**BT-6.** **Whether five authored profiler labels name this system's stages.** A peer session reported~~
      *"display character : preprocessing / shadow / draw clip / draw objects / after emission"* as
      tier-2 evidence for this array. **A string search of the image for `display character`,
      `after emission`, `draw clip` and `preprocessing` returns nothing**, so those labels are not
      confirmed and no claim here rests on them. Either they are differently phrased or they came
      from elsewhere; it needs settling before anyone cites them.
      ***ANSWERED 2026-09-17 (FABLE), and the premise corrected: the five labels exist, and they name this system's stages.** The strings are plain ASCII in `.rdata` at `00D10A18` (`display character : draw clip`), `00D10A38` (`: preprocessing`), `00D10A60` (`: shadow`), `00D10A80` (`: draw objects`) and `00D10AA8` (`: after emission`), beside the `CAMDAT`/`CHRMDL`/`LGTDAT` block; the earlier search that found nothing was wrong. Their only readers are `00332440` and `00332510`, two functions beside the allocator `CharacterRenderSystem_AllocateAndInitialize` (`003325D0`), and both begin by publishing this page's own globals: `00332440(ctx, array, stage)` stores `rcx` into the render context `022C6F20` and `rdx` into `g_pCharacterRenderRecordArray` `022C6F28` (`00332446`..`00332450`), then wraps one stage in [the engine's named-scope push](../../00-Engine-Core-Runtime/Application-Root/game-application.md) and pop (`001EB150`/`001EB110`): stage 0 *preprocessing* runs `004264A0`, 1 *shadow* `00428E40`, 2 *draw objects* `0041E4D0(ctx)` followed by *after emission* `00425DC0(array)`, 3 *draw clip* `00426500`; `00332510` runs preprocessing, draw objects and after emission back to back with the context `022C6F30`. Their callers are the thunk `00332420` and the frame driver `001EC060`. So the peer's labels are authored, present, and attached to the functions that own the array; the five stage bodies themselves are not read here. Static, bytes and bodies read.*

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| One `0x48930` allocation; `160 * 0x740 = 0x48800` records plus a `0x130` tail | complete exact-current body of `003325D0`; the decomposition is arithmetic, not a claim | 1 |
| 160 is not stored as a capacity; `00426480` ignores its `0xA0` argument | complete body of `00426480` — it references only `param_2` | 1 |
| Intrusive active list: head `i32` at tail `+0x00`, `i16` next at record `+0x04`, `-1` terminates | complete body of `00426420` | 1 |
| The system gate is `tail+0x42 == 1 && tail+0x43 == 0` | same body | 1 |
| Record `+0x00` is an `i16` id tested against `-1` | complete bodies of `00424080` and `00426420` agreeing | 1 |
| The coast-down latch, `0.83` decay and `0.05` floor | complete exact-current body of `00424080` | 1 |
| Subtype rules `0x0D` / `0x10` / `0x35` / `0x36` | same body | 1 |
| 639 references to the array base | xref census against the current program | 11 |

**Corrections made to a peer's report while writing this.** A peer session supplied the starting
addresses, and three figures in that report did not survive checking:

1. *"160 × 0x740 = 0x48830"* — the product is **0x48800**. The address `0x48830` is real and is where
   `00426480` writes, but it is **inside the tail**, not the end of the record area. Two correct
   numbers joined by a wrong equation.
2. *"one 0x48930 block"* and *"0x48830"* appeared in the same message as the same quantity. They are
   different quantities: total allocation and a tail field address.
3. *"registers capacity 0xA0"* — the argument is **unused**.

The **mechanism** the peer described was confirmed byte-exactly: the `0x740` stride, the `i16` id
compared against `-1`, the by-reference rewrite of heading and speed, the `0.83`-per-call decay to a
`0.05` floor, and subtype `0x0D` forcing speed to zero. Only the arithmetic joining the sizes was
wrong. Recorded because the pattern is now familiar: **individually correct figures, joined by an
equation nobody evaluated.**

**Superseded readings:** none — this is the document's first version.

**Census regeneration 2026-09-16** (OPUS-REQ-STRUCT-WIDEN-FOUR-CENSUS-SEED-LISTS):
`character-render-record-accesses.tsv` is now `hop_scan.py --array 0x022C6F28:0x740 --argseed
003E4730:0,003E4780:0,003E51F0:0,003E69E0:0,003E70F0:0,0041E960:0,0041F270:0,004201F0:0,004209C0:0,00421D20:0,0042D050:0,0042D7A0:0,0042E7F0:1
--size 0x740 --depth 3 --control 0041F730:0xA` — the same array-only recipe under the current
scanner gives 3,097 accesses in 525 functions, so the committed file predates scanner fixes
(pop-kill exemption, TWOREG refusal); the thirteen argseeds are the `CharacterRenderRecord_*`
functions the named-gap audit found outside the census, each proven to carry the record in the
seeded argument by reading its entry block (`0042E7F0` holds it in `arg1` — `mov rdi, rdx` —
not `arg0`). Result **3,381 accesses in 545 functions over 368 displacements** *(not in the committed file: `character-render-record-accesses.tsv` holds 2,872 rows in 499 functions over 351 displacements - recount 2026-10-02, OPUS; regeneration routed to SWE2-STRUCT)* (was
2,874/499/351; the delta is the widened seeds plus scanner-generation drift, not field movement —
two stale `nop`-operand rows were dropped by the TWOREG fix and four hand-corrected
mis-attribution rows were carried forward). One named function
stays out with cause: `003E69E0` `RemoveModelSubresourceVariantBindings` forwards `rcx` to the
resolver `003E55B0` and the result to `00504610` without touching a field — argseeding it is
correct for propagation but emits no own-body rows.

## 10. Falsification pass 1 — 2026-09-03, session `repos-d2`

**Previously unattacked** (`passes: 0`). Program state: parent `2ed8affb…`, snapshot `46f02e26…`,
EXE `73461d08…`, project `proj_hd2` / `GFZ_HD2`, `CHECKPOINT VERIFIED` before any reading.

### Overturned — 160 is not stored, but it is enforced

§2 says *"160 is not stored anywhere as a capacity. It is a consequence of the allocation size
divided by the record stride."* The first clause is true of *storage* and **false of enforcement**.
`FUN_004279B0` (Presentation) is a slot allocator over this array and compares against `0xA0`
**three times**:

```asm
004279E9  cmp  dword ptr [rbx + 0x4880c], 0xa0   ; live count >= 160 -> refuse
004279F3  jge  <fail>
004279FA  movsxd rsi, dword ptr [rbx + 0x48808]  ; the cursor
00427A06  imul rdi, rsi, 0x740                   ; index by the record stride
...
00427A7F  inc  dword ptr [rbx + 0x4880c]         ; live count++
00427A85  cmp  dword ptr [rbx + 0x4880c], 0xa0
00427A94  jl   <keep>                            ; else reset the cursor
...
00427AB0  inc  ecx
00427AB2  mov  dword ptr [rbx + 0x48808], ecx    ; cursor++
00427AB8  cmp  ecx, 0xa0
00427AC0  mov  ecx, eax                          ; wrap the cursor to 0 at 160
00427ACB  imul r8, rdx, 0x740
```

**And this decodes the `0x130` tail that §4 identified but left unread.** Two of its dwords are
the allocator's bookkeeping, at fixed offsets from the pool base:

```
base + 0x48808   i32   allocation cursor   round-robin, wrapped at 160
base + 0x4880C   i32   live record count   compared against 160 to refuse allocation
```

**What this changes for a modder**, and it is the practical half: §6 can now say *why* the pool
cannot simply be grown. There is no capacity field to edit — **160 is compiled into three
immediates in one function**, and the allocation size is a fourth literal in `003325D0`. Raising the
pool means patching ~~all four~~ more than four - the three in `004279B0` (`004279B0`+0x39, +0xD5, +0x108), the size `0x48930` at `003325D0`+0x17, and also the constructor's loop count (`004269A0`+0x16) and the refusal in `0042FB80` (`0042FB80`+0x88) *(corrected 2026-10-02, OPUS: `mov edi, 0xa0` and `cmp dword ptr [rax + 0x4880c], 0xa0`)* - and nothing in the data will tell you that.

### The 160 derivation is sound, and the tautology risk was checked

`160` is a **quotient**, not a stated bound and not a counted one: the only literal in `003325D0` is
the allocation size `0x48930`, and `160 = (0x48930 - 0x130) / 0x740`. That would be circular if the
stride `0x740` had itself been derived by assuming 160 records.

**It was not.** `0x740` is independently established at **652 sites in 376 functions** that stride or
step by it. Two independent inputs, one quotient. **The document's arithmetic holds and now rests on
a second source.**

### Survived

| Claim | Result |
|---|---|
| one `0x48930` allocation, stored to `022C6F28`, context `022C6F20` published first | **SURVIVED** — complete body of `003325D0` |
| `RenderResourceRoot_InitializeSubcontainers(ctx, 10, 10, 5, 5, 0x13, 0x2A00, 0x16000)` | **SURVIVED, all eight arguments exact** |
| `0x48800 = 160 × 0x740`, with a `0x130` tail | **SURVIVED** — and the tail is now partly decoded, above |
| `00426480` is passed `0xA0` and never uses it | **SURVIVED** — it is the tail call at `00332656` |
| the record stride is `0x740` | **SURVIVED, strongly** — 652 sites in 376 functions |
| `022C6F28` is the pool base with heavy image-wide use | **SURVIVED** — see the count note below |

### A count restated with its predicate

§3 gives `022C6F28` **639 references image-wide**. Counting RIP-relative operands over all
38,161 ledger bodies gives **636 sites in 372 functions**, and **zero** data slots hold the address.
Three sites apart. **This is a predicate difference, not an error in either figure** — and it is
recorded rather than corrected because the document does not state how it counted. The figure that
can be re-derived is: *636 code sites, 372 functions, RIP-relative operands, ledger bodies only.*

### The adjacency test, and a clean negative

This document was attacked immediately after four functions at `001D72F0`–`001D7DD0`, unresolved
at the time of that read, were examined, which drive a **global draw context** (`01F811E8`) through
a reset-then-set sequence and compute rect arithmetic. The obvious question was whether they draw
*these* records. *(Since then, GN161 has classified `001D7DD0` as
`Presentation.CharacterRender.FieldFill`; `001D72F0`, `001D76A0` and `001D7A20` remain
unclassified.)*

**They do not.** Over all 38,161 bodies:

- functions referencing **both** `022C6F28` and `01F811E8`: **0**
- functions referencing **both** `022C6F28` and the authored-command table at `01EFFAF0`: **0**

`01F811E8` has only **3** referencing functions image-wide against `022C6F28`'s 372. **Two separate
drawing paths that share no code**, and the character render records are not what the `001D7xxx`
family emits.

### What was tried and failed to break anything

- **Tried to make 160 circular** by asking where `0x740` came from. It is established 652 times.
- **Tried to find a stored capacity** so the "not stored" claim would fail on its own terms. There is
  none — the claim fails on *enforcement*, which is a different and sharper failure.
- **Tried to connect this array to the `001Bxxxx` draw context.** Empty intersection, twice.
- **No banned evidence.** No `.pdata`/`.xdata`/unwind/EH; no adjacency argument — the tail offsets
  `+0x48808` and `+0x4880C` are read from the instructions that index them, not inferred from lying
  after the records.

## 11. Extension 2026-09-11 — the tail keeps two lists (OPUS-REQ-FABLE-CRRHEAD)

OPUS's store read the allocator and found the list head at tail `+0x10`; this page's walk starts
at `+0x00`. **Both are right: they are two lists.**

| tail | field | written by | read by |
|---|---|---|---|
| `+0x00` | `headActiveIndex` | `CharacterRenderSystem_Initialize` (−1, `004269E1`); the promoter `00428710` when the active list is empty (`0042882A`–`00428833`); the remover `00427C90` when the head is removed (`00427D21`–`00427D2D`) | the reconcile walk (`0042643D`), the name lookup `004278E0` (`004278EF`), `RenderRecords_ProcessDirtyState` and some thirty more — every walk of the live records |
| `+0x04` | `tailActiveIndex` | initialise (−1); the promoter appends here (`00428840`–`0042886A`); the remover when the tail is removed (`00427D36`–`00427D42`) | the promoter, to link the new last record |
| `+0x08` | `nextFreeIndex` | initialise (0, `004269ED`); the allocator advances it (`00427A96`–`00427AC2`); the remover resets it to 0 when the count reaches 0 (`00427D48`–`00427D50`) | the allocator (`004279FA`), read signed with no range check before the clear it addresses, so that clear is in range only under the precondition 0..159 *(qualified 2026-10-02, OPUS: render-slot-identity-publication, accepted)* |
| `+0x0C` | `liveCount` | the allocator increments (`00427A7F`), the remover decrements (`00427D18`) | the allocator refuses at 160 (`004279E9`, `00427A85`) - a bound on the count only, not on the cursor, and neither remover tests the count before decrementing it *(qualified 2026-10-02, OPUS: render-slot-identity-publication and render-removal-phase-contracts, accepted)* |
| `+0x10` | `headPendingIndex` | initialise (−1); the allocator links a fresh record here (`00427A18`–`00427A21`); the promoter unlinks (`00428803`–`0042880F`) and finally resets it to −1 (`00428893`) | the name lookup's second pass (`00427945`), the promoter (`00428724`) |
| `+0x14` | `tailPendingIndex` | initialise (−1); the allocator (`00427A29`–`00427A47`); the promoter (`00428818`–`00428824`, `0042888C`) | the allocator, to link the new last record |

The record's links are `+0x00` its own index (`00427A4D`), **`+0x02` the previous index** and
`+0x04` the next index (`00427A37`–`00427A43`, `004287C4`–`004287FB`). The promoter `00428710` is
the seam between the lists: for each pending record it binds the model resources
(`0041FCF0`, which also finds the `@FCP` block), stamps `+0x414` from tail `+0x28` and `+0x114`
from `003B56D0`, clears `+0x290` bit 0, unlinks it from the pending pair and appends it to the
active pair (`00428750`–`0042886A`). So a record allocated this frame is not walked until the
promoter runs; a reimplementation must keep both pairs, and the reconcile walk starts from `+0x00`.

**There are TWO removers, one per list (OPUS, 2026-09-15).** The table above credits `00427C90` with
every removal. It removes from the **active** list — it is the only writer of `+0x00`/`+0x04` outside
the constructor and the promoter. **`FUN_00429140` (358 B) removes from the PENDING list**, and the
census never saw it:

| it does | site | the active-list counterpart |
|---|---|---|
| repoints `+0x10` when the removed record was the pending head | `00429256` compare, `00429262` store | `00427D21`–`00427D2D` on `+0x00` |
| repoints `+0x14` when it was the pending tail | `0042926B`, `00429277` | — |
| decrements `+0x0C` | `0042924D`, retested at `0042927D` | `00427D18` |
| resets `+0x08` to 0 once the count reaches zero | `00429288` | `00427D50` |
| hands the record to `CharacterRenderRecord_ResetDefaults` | `00429291` → `0041F730` | ~~same~~ only through the per-record teardown called at `00427DAE`, which tail-jumps there *(corrected 2026-10-02, FABLE, Claude Opus 5.5: see section 11a)* |

It touches **neither** `+0x00` nor `+0x04`, which is what makes the split a fact rather than a
reading: a record destroyed before the promoter runs is unlinked here, and nothing on this page
previously described that path *(qualified 2026-10-02, OPUS: only one of its three non-null arms removes anything - `+0x284` mask 04 clear with `+0x290` mask 01 set; with mask 04 set it marks the row for the retire sweep (`+0x290` mask 02, `+0x2AE` mask 01) and writes through three helper-returned objects, with no count change and no clear, and with both masks clear it makes no call and no non-stack write; all three return 1, so a 1 is not a free-slot certificate. Both removers decrement the one shared count `+0x0C` and reset the one shared cursor `+0x08`; render-removal-phase-contracts with FABLE's narrowing, accepted)*. Measured with `disp_image_census.py`, an image-wide sweep of `.text`
(2,110,203 instructions, 3,869 resyncs, positive control on `0x48824`/`0x4881C`), and attributed
through the function list.

**The census is nine sites short in total**, across `+0x08`, `+0x0C`, `+0x10`, `+0x14` and `+0x18`,
and nothing it contains is absent from the image — so its addresses are right and its *counts* are
counts of what one function list reached. The `+0x18` flag word is the other correction: **25 sites
in 12 distinct functions**, not the 23 in 10 the census has. The two extra are reads, in
`CharacterRenderRecord_UpdateChildInheritedState` (`0042D004`) and
`CharacterRenderRecord_UpdateRootLODAndPresentationState` (`0042D3A2`).

### 11a. The slot lifecycle in order - allocation, clear, removal request, active sweep (FABLE, 2026-10-02)

*FABLE (Claude Opus 5.5), consuming three ASTRA packets that FABLE reviewed independently and accepted with narrowing:
slot identity and publication (`aac0489ac`, review [`f1a265c5b`](../../_index/candidates/fable-review-astra-render-slot-identity-publication-1002/REVIEW.md)),
the clear's callee footprints (`621dbd2cc`, review [`b3fb2d6cf`](../../_index/candidates/fable-review-astra-render-clear-callee-footprints-1002/REVIEW.md))
and the removal phases (`31f29775a`, review [`b3fb2d6cf`](../../_index/candidates/fable-review-astra-render-removal-phase-contracts-1002/REVIEW.md));
SWE2-AUDIT-SPEC accepted at `fd96f1634`. Every order below is a dominance fact in one body, re-derived at the bytes;
the record is [`render-lifecycle-consumption-fable-1002`](../../_index/candidates/render-lifecycle-consumption-fable-1002/README.md).*

**Allocation publishes the slot before it names it.** In `004279B0` the only tests before the clear are the name
lookup and the signed live-count gate (`jge` against 160, `004279E9`-`004279F3`); the next-free cursor is read signed
(`004279FA`) and nothing bounds it. Then, in this order:

1. the clear, `0041F730` (call at `00427A13`);
2. the pending-list writes: the head `+0x10` (`00427A21`) when the list is empty, otherwise the old tail record's
   `+0x04` (`00427A37`) and the new record's `+0x02` (`00427A43`); then the tail `+0x14` (`00427A47`);
3. the record's own index into WORD `+0x00` (`00427A4D`), which the clear had left at `-1`;
4. the initialiser `00420480` (`00427A71`), whose first non-stack access ORs `0x2010F9` into `+0x284` (`0042049A`);
5. `+0x290` bit 0 (`00427A76`), the bit the promoter later clears;
6. the live-count increment (`00427A7F`), then the cursor scan to the next row whose dword `+0x284` is 0.

So a record is reachable from the pending list while its id is still `-1`, and the id is written before `+0x290`
bit 0 and the count. A reimplementation must not read "listed" as "id valid", nor "id valid" as "counted".

**The clear's postcondition.** `0041F730` fills the whole `0x740` bytes with 0 (`memset`, call at `0041F754`), and
after that exactly one write reaches WORD `+0x00`: `-1` at `0041F795`. No later write overlaps dword `+0x284` at full
width. So on return the id is `0xFFFF` and `+0x284` is 0. This holds under two premises the review states: `memset`
behaves as the C library's and preserves the ABI's non-volatile registers, and the constant inputs it copies are
readable. The two `006C0520` calls each make four 4-byte scalar (`movss`) stores, 16 bytes per call, over
`+0x210`..`+0x220` and `+0x220`..`+0x230`.

**The removal request, `00429140`, has four arms, and only one of them removes.**

| input | what it does | returns |
|---|---|---|
| null record | nothing: no call, no write, no record read (`0042915C`) | 0 |
| `+0x284` bit 2 set (mark) | `+0x290` bit 1 (`0042916F`), `+0x2AE` bit 0 (`00429178`), qword `+0x108` and dword `+0x110` cleared, `+0x284` = (old without bit 2) with bit 30 (`00429199`), all before its first call; then helper calls, and it writes three helper-returned objects (`004291A9`, `004291E4`, `004291F3`); no count, cursor or list write, no clear | 1 (`00429203`) |
| bit 2 clear, `+0x290` bit 0 clear | nothing (`00429204` to the `ret`) | 1 |
| bit 2 clear, `+0x290` bit 0 set (pending unlink) | the neighbours' `+0x04`/`+0x02`, the pending head `+0x10` and tail `+0x14`; the single count decrement (`0042924D`) dominates both the cursor reset (`00429288`, when the new count is 0) and the clear (`00429291` → `0041F730`) | 1 (`004292A5`) |

The mark arm is therefore not record-only, and a return of 1 does not mean the record was released.

**The active sweep, `00427C90`, decrements before it cleans up.** It walks the active list from tail `+0x00`; for a
row whose `+0x290` bit 1 is set it caches the signed next index (WORD `+0x04`) before branching and reads no id. The
single count decrement (`00427D18`) dominates every call of that iteration: `0042F4C0` (`00427D59`), the child loop
(`00427D7E`), `003B6000` (`00427D97`), `003AFBE0` (`00427DA6`) and the per-record teardown (`00427DAE`), which ends by
tail-jumping to the clear `0041F730`. The cursor is reset to 0 when the new count is 0 (`00427D50`). After the teardown
returns, the sweep ORs `0x20` into the pool flag word `+0x48818` (`00427DB3`, the "active list dirty" bit of section
12) and continues on the cached next index.

**What the two lists share.** The active and pending removals keep separate list ends (tail `+0x00`/`+0x04` and
`+0x10`/`+0x14`) but one live count (`+0x0C`) and one next-free cursor (`+0x08`), so a pending removal and an active
removal decrement the same count. A count of 0 decrements to -1, and the zero test then skips the cursor reset; that is
arithmetic, never executed.

**Not established here.** These are static orders inside single bodies. The reviews accept nothing about:
- what the native helpers do beyond the footprints listed;
- ABI preservation by anything but the modelled `memset`;
- that rows and indices are valid (the cursor is unbounded, and an out-of-range cursor addresses outside the 160-row
  pool);
- frame placement, aliasing, interference between callers, or that list chains are finite;
- lifetimes and scheduling;
- a census of every writer of these fields.

ASTRA's later 76-check additive packet is producer-valid but unpublished and has not been independently reviewed, so
nothing here rests on it.

## 12. Extension 2026-09-11 — the tail's other fields, and what the record's two strings are (OPUS-REQ-FABLE-TAILNAMES, -RECORDNAMES)

**The tail past the list heads.** `+0x1C` is the **fade start distance** (34.0 at construction) and
`+0x24` the **fade width** (4.0): `CharacterRenderRecord_UpdateDistanceFadeAndCull` adds them and
compares the sum with the record's distance (`0042EA9C`, `0042EB36`). **Corrected 2026-09-15
(OPUS): which of the two is the start and which the width is not nomenclature — it is the ramp.**
At the second site the pass computes `xmm1 = [+0x24]`, `xmm0 = xmm1 + [+0x1C]`, `xmm0 -= d`, and
where `xmm1 > xmm0` takes `divss xmm0, xmm1` then `mulss` by `1.5707964` (π/2, `008C5F70`) and
`sinf` (`00861F0E` → `api-ms-win-crt-math-l1-1-0.dll!sinf`), `0042EB2B`–`0042EB54`. So the fade
value is `sin(((start + width − d) / width) · π/2)` — flat `1.0` inside the start distance
(`01CEBBA8`), falling to `0` at `start + width`, where `0042EAA4` has already set `+0xD3` bit 1 and
`0042EB05` jumps past the ramp entirely. **The divisor is `+0x24`, so `+0x24` is the width.**
`+0x28` holds the float `1/6`; the promoter copies it into every promoted record's `+0x414`
(`0042876A`, `00428773`). **What that value MEANS was withdrawn 2026-09-15 (OPUS): this page called
it the "default fade step, six frames from invisible to drawn", and nothing reads it.** An
image-wide displacement census (`disp_image_census.py 0x414`, 2,110,203 instructions decoded across
`.text`, 3,869 resyncs; positive control on `0x48824` returns its five known sites) finds 22
operands at that displacement, of which exactly two — `0041FA68` and `00428773` — are this record,
and **both are writes**. A step implies an accumulator; no accumulator exists, so the reading is
retracted and `CharacterRenderRecord +0x414` stays `UNRESOLVED` on meaning while its *source* is now
established. The census cannot see a reader that folds an array offset into the displacement or
works from a biased base pointer, and that is the only door left open. *(Closed 2026-09-30, SWE2-STRUCT for OPUS,
DD batch 12, [`swe2struct-ddres-b12-0930`](../../_index/candidates/swe2struct-ddres-b12-0930/README.md) F1-F5. A
structflow census follows the record pointer to call depth 3 over 1,238 functions, biased bases and element pointers
included. It starts from all 639 references to the array global, and from the pointer's 12 escapes: the published
copies, the model instance's `+0xF8`, the `+0x2E0` holders, the status-push blocks and five out-parameters. It finds
only the two writes. The control finds the known `+0x408` read `002EDC14`, and the `+0x5EC` read `003ABDF3`, which is
reachable only through `+0xF8`. The source is a constant too: tail `+0x28` is written `1/6` by `004269A0` and
`0042ED30` and read only by the promoter. So `+0x414` is a write-only `1/6` on PC.)* The write side carries the
same limit in another shape (AL-8): a block store marks one displacement while covering sixteen
offsets, so *no store row at `+0xNN`* never proves *never written* — **14 of this census's no-write
displacements sit inside a wider store's range** (`work/STRUCT/blockwrite_overlap.tsv`), the
`004204CE` initialiser block alone accounting for `+0x3D..+0x41`. `+0x2C` is the **focus record
index**:
`RenderSystem_UpdateCharacterRecords` stores the record index resolved from
`PartyFocus_GetCurrentPackedActorHandle` through `002E9B80`, or −1 (`00426099`–`004260C3`), and the
fade pass scales it by `0x740` to reach the reference record (`0042E954`–`0042E97A`). `+0x54`
(`0x80404040`) has no reader.

**`+0x18`, the flag word.** Bit 0 = **distance cull enabled** — the three `…DistanceCullEnable`
functions write it, and the fade pass tests it three times before touching a record (`0042EA43`,
`0042EA6C`, `0042EAB1`). Bit 2 is set with bit 0 by the constructor (`00426C59`) and the reset
helper (`0042ED37`) and is neither cleared nor tested. Bit 4 = **external fade enable** — written
only by `002E8700(bool)` (`002E8707`, `002E871C`) from platform-layer callers (`0015CC90`, `0017CDF0`,
`0017CE20`, `0017D6E0`, `0017DE60`), read only by the fade subtraction at `0042EB79`. Bit 5 =
**active list dirty** — set by the promoter (`00428863`) and the remover (`00427DB3`), cleared and
consumed by `0042ED60` (← `00332660`): it clears the bit, runs the remover and the promoter, and if
the bit is set again re-resolves the lookup (`0041E500` on `+0x30`), walks the active list through
`CharacterRenderRecord_RefreshLoadedResourceBindings` and posts `003697C0(6)`.

**The record's two strings.** `+0x1C` is a **generated instance key, not a name**: the allocator's
sole caller `0042FB80` writes the seven bytes `cn\plan` (the literal at `00CB2474`) and appends one
raw byte, the tail's next free index (`0042FB9F`–`0042FC5E`), refusing when the live count is 160
or more (`0042FC08`); the lookup's refusal to allocate a matching key is a refusal by ordinal.
`+0x3C` is the **model container's name** — the 32 bytes of the current plan object
(`00409090(003AB7F0())`, `0042FBF0`–`0042FC03`), the `.cm` basename under `obj_finish/in/`. Its
first letter is the archive directory: `c` `chara/` (17 files), `m` `monster/` (254), `n` `npc/`
(174), `s` `summon/` (26), `h` `high/` (the high-detail companions `hs####_##`, 132); outside the
selector's set, `w` `weapon/` (326), `g` `gadget/` (103), `t` `treasure/` (17), `b` `bg_obj/` (17) —
a census of every `.cm` in the `us` archive index. The initialiser `00420480` accepts exactly the
four character-model directories `c / m / n / s` and marks the record with `+0x284` bit 14
(`004204DB`–`004204EF`); `h` is the high-detail variant tested on its own (`00421684`, `00426283`).
## 13. Extension 2026-09-12 — the per-record reconcile is the shadow sync (BT-1)

`00426340` (211 B), the callee `CharacterRenderSystem_ReconcileActiveRecords` (`00426420`) runs on
every record of the active list (head at tail `+0x48800`, `+4` links, under the gate tail `+0x48842`
== 1 and `+0x48843` == 0), reads exactly seven record fields and touches nothing on the record. What
it does is **keep the record's two shadow objects in step with the record's state**:

1. If the handle at **`+0x114`** is non-zero, `003B6900(handle, 6)` — set bit 1 of the object's mode
   byte (`+0x41`), keeping bit 0. If the handle at **`+0x118`** is non-zero, `003AFD00(handle, 0)` — set
   the object's low nibble (`+0x20`) to 0. This is the *off* state, applied unconditionally first.
2. The record qualifies only if **all** of: flags `+0x284` bit 2 (live), bit 7, bit 6 and bit 12
   set; `+0x006 == -1`; `+0x2AE` bit 1 clear. Otherwise it returns with both objects off.
3. Kind 0 — `(+0xC0 >> 3) & 3 == 0` — and the `+0x114` handle present: `003B6900(handle, 4)` (bit 1
   back off, so the object runs), then the LOD: if `+0xC0` bit 1 is set, the record's own float at
   **`+0x27C`**, otherwise **`003B5980(handle)`** computes it; either way `003B6B80(handle, lod)` stores
   it at the object's `+0x14`.
4. Kind 1 — `(+0xC0 >> 3) & 3 == 1` — and the `+0x118` handle present: `003AFD00(handle, 1)`.

**The two objects are the character's shadows, and the fields are the shadow verbs' fields.** The
handle at `+0x114` names an entry of a **160-slot, `0xE0`-byte pool at the pointer `02B40528`**
(allocated by `003B6890` from `CharacterRenderSystem_Initialize`, handle = generation `02B40520` << 8
| slot, validated at entry `+0x10`; allocator `003B56D0(record.id)`, taken at promotion — the
lifecycle contract's step 3 — and freed by `003B6000` at retirement). Its entry holds the owning
record index (`+4`), the LOD float (`+0x14`, default 1.0), a mode byte (`+0x41`), a bone index at
`+0x3C` = `003E5AD0(record, 0x104)` — the model header's word `+0x3A`, one of the three model-declared
special bones (`0x104`/`0x105`/`0x106` → header `+0x3A`/`+0x3C`/`+0x3E`) — and five tweened float
pairs that `003B5890` (from `RenderSystem_UpdateCharacterRecords`, `00426112`) steps ~~once per frame~~ once per
character-update pass for every allocated entry whose mode bit 0 and the global mask `02B40524` allow. *(Corrected
2026-09-14, FABLE: a presented frame can hold two passes, and `003B5C00` also steps a single entry from the
presentation fast-forward. See [the ramp contract](../CONTRACT-authored-command-ramp-channels.md) §5, UG-5.)* The handle at
`+0x118` names an entry of a **32-slot, `0x70`-byte inline table at `02B3F570`** (allocator
`003AF340(record.id)`, needs `003E6E40(record)` non-null; freed by `003AFBE0`), the same tween pattern
(`003AFB30`, stepped from `0041C850` and `PresentationEntry_RebuildAndFastForwardToTime`), and its
handle is also copied into the render object's `+0x360`. **Which kind a record uses** is bits 3–4 of
`+0xC0`, set by `003E73B0(record, kind)` from `RenderRecords_ProcessDirtyState` (`00428097`) when
dirty bit 22 of `+0x290` is set, with `kind = (+0x304 >> 12) & 3`; kind 0 keeps only the pool-A
object, kind 1 allocates a pool-B object, kinds 2 and 3 leave both off.

The script verbs own the rest: **`setshadowlod`** (`0x0286`, `00342CF0`) calls `002E8950(actor, 1)`
— bit 1 of `+0xC0`, "LOD is scripted" — and `002E89B0(actor, v)`, which clamps `v` to `[0, max]` and
stores it at **`+0x27C`**; **`clearshadowlod`** (`0x0287`) is `002E8950(actor, 0)`. **`setshadowalpha`**
(`0x0284`, `00342410`) calls `002E88A0(actor, 1)` — bit 2 of `+0xC0` — and `002E8900(actor, a)` →
**`+0x274`**; **`clearshadowalpha`** (`0x0285`) clears the bit. Both floats reset to 1.0 in
`CharacterRenderRecord_ResetDefaults` (`0041F814`, `0041F81E`). The computed LOD, `003B5980`, resolves
the entry's bone through `00421FF0(record, bone)` (skeleton at context `+0xD98`, `002ED570`, then the
bone matrix `00370F60`), takes the distance from that bone's translation to the render object's
position (`003E6F70(record)` → `+0x20/+0x24/+0x2C`; the difference is squared, summed and rooted at
`00861F14`), and maps it through a clamp into `[low, 1.0]` — the shadow fades with the tracked bone's
height above the character's position. **What is not read:** the consumers of the pool-A entry's
tweened floats (the shadow draw itself), and the semantic names of the three special bones. *(Roles read 2026-09-30, SWE2-STRUCT for OPUS, DD batch 12, [`swe2struct-ddres-b12-0930`](../../_index/candidates/swe2struct-ddres-b12-0930/README.md) SB1-SB9: the image gives the ids no name, so they are named by consumer. `0x104` is the body bone: this shadow entry measures and anchors on it, lights flagged for it are evaluated at it (`004221F0` → model instance `+0xF0` → `003ABD50`), and the hit-flinch, Immobilize and Float-bob applies (`00471230`, `004717E0`) move it. `0x105` is read only as the second link of the first-non-`0xFFFF` chain (`00421CD0`, `003E4CB0`, `003E5FA0`), and 284 of the 326 weapons declare it. `0x106` is this entry's second anchor `+0x3E`, which authored command class `0x09` can switch to, and it is bone 0, the root, in all 1,066 blocks. The chain's result goes to the model object's `+0xB6`, whose one reader hands that bone to the draw setup `004FD4B0`.)* *(2026-09-30, OPUS: the first half is answered - UQ-191, [`uq191-shadow-channels-pc`](../../_index/candidates/uq191-shadow-channels-pc/README.md): the one consumer is the shadow draw `003B62D0`, whose output goes to the PS2 command ring that no PC code reads back.)*

## 14. Extension 2026-09-13 — the dirty bits and the handler each one runs (FABLE; completed 2026-09-14, FRONTIER)

`RenderRecords_ProcessDirtyState` (`00427DE0`) walks the live records once per frame and runs **five consecutive
sweeps** of each record's two dirty words — `+0x290` and `+0x294` — in fixed bit order, then runs a tail commit. The
walk: `ebx = [+0x48800]@022C6F28` head index, `rbx = base + index*0x740`, `next = [rbx+4]` (`00427DF2`, `00427E0A`,
`00428A2A`). Per record, `esi = arg1` (a caller-supplied flag — only `0042ED60` passes 1 (`0042EDF3`, reached by
tail-jmp from `00332660`); `00426090` `RenderSystem_UpdateCharacterRecords` passes 0 (`004260E9`, called by
`003323D0`) — those are the only two call sites of `00427DE0`) and `edi = "any work ran"`; a record whose `+0x284`
bit 30 is set is skipped entirely (`00427E23`).

Each block tests one bit, runs its handler when set, and clears the bit — by one of four mechanisms: the **processor**
clears after the call (40 rows), the **handler self-clears** (11 rows, the large resource/children refresh functions
`00429830`, `00429xxx`, `0042BAxx`, `0042BCB0`-family plus `0042F4C0`/`0042F6C0`/`0042F880`), the work is **inline**
in the processor (2 rows), or the bit is **consumed** by a bare `bt`+`btr` with no handler at all (2 rows — `+0x294`
bits 18 and 19). Pass 5 is not a test at all: it checks `+0x290` bit 1, and **when the bit is clear** ungates the
record (`+0x284`:30 off, `004286AB`) and — only when `esi` — snapshots `+0x120/124/128` into `+0x250/254/258`
(`004286B9`); when bit 1 is **set** the record stays gated and `+0x290` bit 20 is re-dispatched into `0042F4C0`. The
tail commit runs only when `esi && edi` (record had work *and* the caller opted in): pass-1 bits 2 and 3 promote to
`0042C410` `CharacterRenderRecord_UpdateRootAnimationPresentationPhase` (`00427F09`; interior read 2026-09-17, SWE2-FRONTIER: 1,234 B — `003E7D10` first at [`0042C46A`](../../_index/ADDRESS-INDEX.md), `0020E600` ×6 + `003E58B0` ×3 + `00423050`/`00422D50` ×2), and after several passes every
record with work done gets `+0x294` bit 25 set on its `+6`-chain tail records (`00427F3A`, `00427F88`, `00428068`,
`004284DA`) — `00427BD0` walks that chain, clears bit 25 and calls `00420A40`
`CharacterRenderRecord_ComposeModelTransformFromParent` on the tail.

The full 56-block census — mechanically enumerated from the disassembly, merged with the measured setters and each
handler's distinctive callee — is [`members/dirty-bits.tsv`](members/dirty-bits.tsv). Reading it column-wise:

- **Pass 1** (`00427E33`–`004280BA`, 13 blocks): `+0x290` bits ~~{2,3,12,19,20,22,23,24,25,29,30}~~ {2,3,12,18,19,20,22,23,24,25,29,30} and `+0x294` bit 26 *(corrected 2026-10-02, OPUS: bit 18 is tested at `00427DE0`+0x1B4 `bt eax, 0x12`; twelve bits plus one make the 13 blocks)*.
- **Pass 2** (`0042810D`–`00428173`, 4 blocks): `+0x290` bits {9,10,11,17}.
- **Pass 3** (`004281C3`–`004284A4`, 26 blocks): `+0x290` bits ~~{26,27,28,31,9-again}~~ {26,28,31,9-again} *(corrected 2026-10-02, OPUS: bit 27 is tested only in pass 4, at `00427DE0`+0x7F7; four bits plus 22 make the 26 blocks)* and `+0x294` bits
  {0,1,2,3,4,5,6,7,8,10,11,12,13,14,15,16,17,18,19,20,22,23} — the bulk of the protocol lives here.
- **Pass 4** (`00428531`–`00428660`, 11 blocks): `+0x290` bits {4,5,6,13,14,15,16,21,27}, `+0x294` bits {24,27}.
- **Pass 5** (`004286A7`–`0042870A`, 2 blocks): the `+0x290` bit-1 gate described above.

**Who sets the bits.** A whole-process census of `or [x+0x290/0x294], imm` / `bts`+`mov` writes finds exactly one
writer per request bit in most cases, all named in the TSV's `set_by` column — including **one writer with no
direct caller** that is nevertheless live, and one genuinely dead one. `00520430` (`bts`/`or +0x290, 0x200`,
bit 9, plus clears of bits 9 and 10) is the registered handler for **presentation command id `0x13`**:
`CharacterRenderSystem_Initialize` installs it at `02CA4410 + 0x13*8` (`00426A4E`–`00426A58`), and the
command-stream drains reach it through invoker table `01EFFAF0[0x13]` = `00417530`, which tail-jumps the slot
(see [the render-event page's dispatch section](render-event-selection-evidence.md), §"handler arrays").
`0042EE10` (`or +0x290, 0x400000`, bit 22, `0042EE4C`) is the one truly dead writer: its only reference is the
uncalled tail-jump thunk `002E8390` (`jmp 0x42ee10`, and nothing calls `002E8390`). Three mechanics: plain `or`-immediate
setters (the `002Exxxx` request family — `002E8FD0` `Actor_RefreshPresentationVisibility` sets `+0x290`:4 and its
visibility pair `00428DE0`/`00428E10` sets `+0x290`:29/30; `002E8730`/`002E87F0`/`002E8A10` set `+0x290`:22;
`00428AF0` sets `+0x294`:26 from the `RenderRecord_ApplyPresentation*` family); `bts`+store setters inside the
`0042F2xx`/`0042F3xx` cascade (`0042F250` sets `+0x290`:20; `0042F310`/`0042F3B0` set `+0x290`:19); and **group-write
setters** for `+0x294` bits {2,5,7,8}: `00427280`, `00426130`, `00426560`, `00426C90`, `004270A0`, `004272E0`,
`00427860` each do `and [+0x294], ~cluster` clearing a cluster of sibling bits before setting their own —
the cluster union is {0,1,5,7,8,10,17} and bit 17 is cleared by every one of them. `00427320` is the composite:
`and +0x290,~0x80000000; and +0x294,0xFFFDFFFC` (clears `+0x294`:{0,1,17}) then `or +0x294,8` — it is the only setter
of `+0x294`:3.

**Which bits have no setter.** The census found no direct write anywhere in the image for `+0x290` bits
{2,5,18,24,31} or `+0x294` bits {0,1,4,6,10,11,13,14,17,18,19,20} — and no byte- or word-granular `or`/`bts` lands
inside either dword at any other offset, so these are not sub-word aliasing artifacts. Some are structurally explained:
`+0x290`:19/20 are re-armed *inside* the handler cascade itself (`0042F250` family — the cascade keeps the record
dirty until the refresh completes); `+0x294`:0,1,17 are cleared-then-re-set by the group writers so they are always
transient; `+0x294`:18,19 are pure consume bits with no handler. The rest (`+0x290`:2,5,24; `+0x294`:4,6,10,11,13,14,
20) have no located setter and no handler-side re-arm — they can only arrive via a whole-record write (clone/init or
the `+0x340` pending-record swap the array docs describe). This is a measured gap, not inferred: every setter and
clearer above is an interior-cited instruction.

**What the handlers do.** 36 of the 52 distinct handler addresses are child-iteration loops of one shape: `rbx` =
record at `[rcx+0]` … `[rbx+8]`/`[rbx+0xA]` chain, each child filtered through gate `00426220` or the
`[+6]==-1 || [+0x2F2]==1` chain-tail test, then a single leaf call per child. The leaves resolve the child's
active-presentation entry (`00422D50` `ResolveActivePresentationEntry`, `00422D10`) or write into it — e.g.
`00424010` writes entry `+0x4B6`/`+0x4B7` + vec3 `+0x2B0`, `00423570`→`0041CEA0` sets/clears entry `+0xC` bit 3,
`00423AB0`→`0041C7C0` writes entry `+0x340`/`+0x3C`. Three handlers (`0042AE00`, `0042AF10`, `0042A580`) instead
~~perform a **CFG-guarded virtual call** into each chain-tail child~~
(`0016D6A0` `_guard_check_icall`). ***Corrected 2026-09-19 (FABLE), for the two read: it is not a virtual call.** A
control-flow-guard check is an indirect call followed by a call through `rax`; `0042AE00` makes a **direct** call to
`0016D6A0` (`0042AEB2`) and the callbacks of `0042AE00` and `0042AF10` end in a direct `jmp` to it, with no indirect
call after. `0016D6A0` is `ret 0`: an **empty function** that identical-code folding merged with the guard stub,
which is where its label comes from. Whatever these handlers called on another platform is compiled out here - see
the callbacks section at the end of this page. `0042A580` was not read.* *(Read 2026-09-30, OPUS, [`opus-render-record-residue-0930`](../../_index/candidates/opus-render-record-residue-0930/README.md) A1-A4: the bit-20 handler walks the record's node, its first child and their subtrees (`0042EF90` with callback `0042E4B0`), and every per-node call is the empty `0016D6A0` too; its one lasting store clears `+0x294` bit 20. It returns a flag that is 0 when a visited node's `+6` is -1 and otherwise an **uninitialised stack dword** (`0042A5EA`, `0042A68D`), and `00427DE0` uses that return as its rebuild flag (`00429E50`'s argument, the `00427100` gate) unless a later handler sets it to 1.)* The heavyweight passes: `0042F880`/`0042F6C0`/`0042F4C0` are the self-clearing
resource refresh (runtime-pointer + signed-index resolves, `003E55B0` ResolveModelInstance, `004780B0`
ResourceTable_ResolveEntryBySignedIndex16) that re-arms `+0x290`:10 and re-dirties `+0x290`:20 until complete.
The object `003E55B0` returns is declared in the store as **`RenderModelInstance`** (size `0x260`,
element of the `+0xDA0` chunked table — stride proven by `mov edx,0x260` at `00477EF3`);
`0042AC30` (shared by `+0x290`:31 and `+0x294`:3) is the +`0x124`/`+0x254`/`+0x304` field refresh; `003B3C00`
(`+0x294`:27) is the `[+0x288]`-gated Phyre-side call family with `edx = +0x304>>27`. `003E74B0` (`+0x290`:21) is
nine bytes — it copies `[+0x3FC]` to `+0x278`. Per-block interior citations are in the TSV.

**52 distinct handler addresses across 56 test blocks.** The named ones are the
ensure/remove subresource-variant pair `003E7210`/`003E69E0` (`+0x290`:24) and — on the tail-commit path —
`0042C410` `UpdateRootAnimationPresentationPhase`. Every row's test site, handler, clear site and mechanism,
setter instruction(s), and distinctive leaf call is mechanically derived — no bit semantics were inferred from
names.

### The staged / flush parameter surface — 2026-09-18 (SWE2-STRUCT-CRR-PENDING-PARAM-SURFACE)

Four `+0x294` bits gate a **two-stage parameter pipeline** that begins in `SecondaryContext`
element 0 ([the context censuses](../../04-Actor-Entity/Actor-Contexts/the-movement-and-secondary-context-censuses.md)
§4, `pendingParamVec`) and ends on the resolved presentation entry:

- **Stage 1 — staged fields** `+0x3BC` (`stagedRateScalar`) and `+0x3C0`/`+0x3C4`/`+0x3C8`
  (`stagedParamVec`). Writers are one-instruction setters that OR a single dirty bit and store the
  payload: `00427880` stores the vec3 + bit `0x10000`; `00427300` stores the scalar + bit `0x8000`;
  `004278B0` stores an integer to `+0x3C4` + bit `0x400000`; `004272C0` stores float `+0x3C0` + int
  `+0x3C4` + bit `0x800000`.
- **`+0x3C4` is a union**: float Y of the vec under bit `0x10000`, but a motion **preset index
  `0..4`** under `0x400000`/`0x800000` — consumers `0042B270`/`0042A390` bounds-check `0 <= x <= 4`,
  index a stride-6 word table at `+0xC0` of the resolved entry, and run a `@FMN`-family tag lookup
  (`mov edx, 0x4e4d4640`).
- **Stage 2 — flush fields** `+0x2BC` (`flushRateScalar`, ResetDefaults seeds `30.0f`) and
  `+0x2B0`/`+0x2B4`/`+0x2B8` (`flushParamVec`, seeded `−1.0f`). The pass-3 handlers copy staged →
  flush **on each child record** of the `[+8]`/`[+0xA]` chain: `0042B130` → `00424010` for the vec,
  `0042AB20` → `00423AB0` for the scalar.
- **Terminal apply.** The four `00424870`-family forwarders read the child's `+0x2B0` vec as
  `xmm1/2/3` and reset it to `−1.0f` after use (the same consume-and-reset idiom as the element
  side). `0041D7E0` stores the triple to the resolved entry's `+0x344`/`+0x348`/`+0x34C`, swapping
  the X/Z pair when begin > end — an **ordered range**. `0041C7C0` scales the rate scalar by a
  constant onto entry `+0x340`/`+0x50`; the same family computes `1.0f/rate` (divss at `004249DC`),
  i.e. a per-frame step against the 30 fps default.

Deliberately not claimed: what the range endpoints count (frames vs seconds), and whether the
mid component `+0x348` is a cursor, a blend weight, or something else — no reader discriminates
it yet.

### The high-traffic fields — 2026-09-18 (SWE2-STRUCT-CRR-HOT-FIELDS)

The offsets with the densest access counts in `character-render-record-accesses.tsv`, named from
the named accessors that touch them:

- **`+0x304` `presentationFlags`** (75 sites) — the record's persistent flag **dword**, distinct
  from the `+0x294` pending-apply mask: dozens of `and`/`or` bit-ops from the verb setters and
  `Actor_RefreshPresentationVisibility`. Bits observed live: `0x02`, `0x08`, `0x40`, `0x100`,
  `0x200`, `0x1000`, and the two-bit field `0x3000` — bits 12–13, already cited above as the
  tween `kind` selector (`(+0x304 >> 12) & 3`).
- **`+0x400` `fcpPayloadPtr`** (39 sites) — the FCP presentation payload pointer, written by
  `CharacterRenderRecord_RefreshFCPPayloadByRecordId` and read by
  `GetFCPPresentationConfigurationPayload` plus the `003Exxxx` payload getters, which index it
  by `word[+0x12]` and select `payload+0x30`/`+0x34` on `objectFlags` bit `0x40000` (`003E58B0`).
- **`+0x408` `fcpPayloadSelector`** — the word id refreshed beside the payload pointer
  (`movzx`, `002EDC14`) and consulted by `RefreshLoadedResourceBindings` (`0042DA46`).
- **`+0x42C` `boundResourceHandle`** — written by the bind/redispatch functions
  (`002E6BD0`/`002EC6B0`/`002EDD20`/`002EE1D0`) and maintained by
  `MaintainPresentationResourceReferences` (`00422B0A`/`00422B2F`).
- **`+0x260`/`+0x264`/`+0x268` `scaleVec`** and **`+0x26C` `uniformScale`** — the payload getters
  compose three record scalars multiplicatively: `scaleVecX × lodFactorVecX × uniformScale ×
  payload scalar` (`003E58D9`–`003E58F3`); `UpdateRootLODAndPresentationState` uses `scaleVec`
  as a vec3 (`mulss` per component, `0042D229`–`0042D23F`). All four reset to `1.0f`.
- **`+0x160`..`+0x16C` `lodFactorVec`** — a vec4 loaded whole (`movaps`, `0042D211`); only X is
  used scalar in the factor chains so far.
- **`+0x288` `rootDistanceFadeIndex`** — dword index gated `!= -1` by
  `UpdateRootDistanceFade` (`0042D7DB`); −1 = no fade entry.
- **`+0x2F2` `resolveStateWord`** — value 1 makes the chain walker `0042A580` run the
  ~~re-resolve helper~~ empty function `0016D6A0` (`ret 0`, so nothing is re-resolved) *(corrected 2026-10-02, OPUS: `0016D6A0`+0x0 is `ret 0`; the call is `0042A580`+0x5E; as corrected 2026-09-19 above)* on the record (`0042A5D1`); written by setters
  `004218A0`/`004219C0`.
- **`+0x40B` `flagByte40B`** and **`+0x4B7` `flagByte4B7`** — per-record flag bytes; `+0x40B`
  keeps only its top three bits across ResetDefaults (`and 0xE0`), `+0x4B7` bit 2 is tested and
  set by `00545FB0`.
- **`+0x4C0`.. `q12Channel` array** — stride-8 entries of four `int16` indexed
  `[record + 0x4C0 + i*8]`, word 0 initialised to `0x1000` (Q12 = 1.0) and accumulated by
  `003E5D60`; read by `EvaluateQ12PresentationChannel`,
  `BuildPresentationChannelVector4` and `UpdateCompositePresentationFactorQ12`. The per-word
  rows are named `q12Channel{0..6}W{0..3}` in the store.
  *Completed 2026-09-18 (FABLE):* there are **ten** channels, not seven (`+0x4C0`..`+0x50F`; the per-frame stepper
  `003E4370` and `ResetDefaults` both loop to `0xA`), the four words are `{base, delta, progress, step}`, `003E5D60`
  does not accumulate but **starts a ramp** toward a target over a frame count, and each channel has an owner -
  distance fade, viewer-inside fade, attached-piece visibility, the script colour of `rgbatrans`. All of it is on
  [how a character fades](how-a-character-fades-the-ten-channels.md).

Second tier (same pass): **`+0x118` `tweenEntryIndex`** — the record's slot in the 32-entry
`0x70`-stride tween table at `02B3F570` already described above; **`+0x114` ~~`animPhaseHandle`~~** the slot handle `003B56D0` returns - the ramp-channel (shadow) slot of the pool at `02B40528` *(corrected 2026-10-02, OPUS: stored at `00428710`+0x7A after the call at `00428710`+0x75; not an animation-phase handle)*
read beside it; **`+0x2F8` `optionalLinkId`** — word id with `-1` sentinel; **`+0x2FC`
`authoredDataOffset` + `+0x300` `authoredDataCount`** — the payload getters resolve `+0x2FC`
through the base-relative resolver `0020E600` only when `+0x300` is nonzero and then advance by
it (`003E6694`–`003E66B0`); **`+0x430` `boundResourceHandle2`** — a second handle in the same
bind/maintain family as `+0x42C`; **`+0x550` `embeddedTweenObj`** — an embedded sub-object whose
`+0x18` member (record `+0x568`) is read through `arg0+0x550`-routed calls to the `003AExxx`
tween methods; **`+0x66C` `animPhaseByte`** — the byte `UpdateRootAnimationPresentationPhase`
reads and rewrites; **`+0x734` `kindTunedFloat`** — a ~~per-kind constant (`2.0`/`1.7`/`1.3`)~~ per-model constant chosen by directory letter and name, 1.0 to 2.0 (the full table is in section 7) *(corrected 2026-10-02, OPUS: `00420480`+0x1F4 through `00420480`+0x394 store 2.0, 1.7, 1.3, 1.5, 1.2 and 1.6)*
written by setter `00420480`.

Third tier (same pass): **`+0x4B4` `compositeScalarQ12`** — the word
`ComputeCompositePresentationScalar{,WithMultiplier}` returns; **`+0x4A0` `blendStateFlags`** —
bit 1 gated by `PublishBlendStateToModelInstance`; **`+0x678` `auxTransformBlend`** *(corrected 2026-09-19, FABLE: not a blend factor - `+0x670`/`+0x674`/`+0x678` are the three components of the character's focus point, and the blend is the eased countdown in `+0x66C`; see [the focus point of a character](the-focus-point-of-a-character.md))* — the
interpolation factor inside `UpdateAuxTransformInterpolation`; **`+0x450` `phaseEntryIndex`**,
**`+0x23C` `animPhaseFloat`**, **`+0x64C` `phaseStateDword`**, **`+0x6A4` `phaseParamDword`** —
the four phase-lifecycle fields `UpdateRootAnimationPresentationPhase` consults;
**`+0x108` `sourceBindingPtr`** — the record's back-pointer, stored by the element bind/release
paths and cleared on release; **`+0x640` ~~`bindingResultDword`~~** — a float countdown, the lip-flap timer of the rig page *(corrected 2026-10-02, OPUS: `0042EE90`+0x27 reads it as a float and `0042EE90`+0x36 subtracts `[01DFE0BC]` each tick, clearing `+0x304` bit 6 at zero)*; written by the binding update
`002E3110`; **`+0x69C` `boundResourceKey`** — written by both resource-binding maintainers;
**`+0x220` `lodScalarVec2`**, **`+0x3FA` `cachedSelectorWord`**, **`+0x413` `pendingStateByte`**;
**`+0x570`** is `embeddedTweenObj`'s member `+0x20`, a list link (`arg0+0x550`-routed).

Fourth tier (array-index fields): ~~**`+0x6` `ownArrayIndex`** — sign-extended, multiplied by `0x740` (CRR stride), added to pool `022C6F28` at `00425E97` to compute the record's own base address;~~ **`+0x6`** — the parent (owner) record's index, `-1` at a root: `00420FB0`+0x1B walks it up the chain and `00424080`+0xAB tests it for `-1`; the record's own index is word `+0x0` *(corrected 2026-10-02, OPUS: `00425E70`+0x19 `movzx eax, word ptr [rcx]`; the cited site lies inside the `je` at `00425E70`+0x24)*; **`+0x8` `nextLinkedIndex`** — checked against `-1`; if valid, used as an index to fetch the linked record via the same `×0x740 + pool` pattern (`00425EBC`); **`+0xA` `altLinkedIndex`** — ~~same pattern for an alternate/parent linked record (`00425EE4`)~~ the next-sibling link: the depth-first walk recurses on `+0x8`, the first child, and iterates `+0xA` *(corrected 2026-10-02, OPUS: `0042EF90`+0x3A and `0042EF90`+0x4F; the parent is `+0x6`)*; **`+0x18` `traversalIndex`** — dword index read in 57 skeleton/pose traversal functions, compared/written as `-1` (reset). These implement the CRR array's internal linked-list navigation.

Fifth tier (LOD and view-dependent fields): **`+0x64` `lodLevelSelector`** — 16-bit LOD selector read by `SelectLODForViewDepth`, compared against `-1`; written by `ResetDefaults` and setters. **`+0xC0` `lodVariantFlags`** — byte flag bitfield: bits `0x40`/`0x20`/`0x18`/`0x02`/`0x04` tested/cleared by `EnableLocalLodThresholds`, `EnsureModelSubresourceVariantBindings`, `UpdateRootLODAndPresentationState`. **`+0x2E0` `viewDependentFactorVec4`** — four floats written by `UpdateViewDependentPresentationFactors` at `+0x2E0`/`+0x2E4`/`+0x2E8`/`+0x2EC`; the last is initialized to `0x437f0000` (`255.0f`?) at `0041EBC2`. `+0x22C` is the W component of the existing `+0x220` `lodScalarVec2` vec4, read as a scalar by `ComputeCompositePresentationScalar` rather than as the array. **`+0x2AE` `presentationStateFlags`** — byte flag bitfield: bits 1 and 2 tested by `UpdateRootLODAndPresentationState`, `UpdateRootDistanceFade`, `UpdateRootAnimationPresentationPhase`. **`+0x1B0`/`+0x1B4` `projectedOriginX/Y`** — float components read by `UpdateProjectedOriginState` and `UpdateDistanceFadeAndCull`. **`+0x2C4` `auxTransformResultDword`** — dword written by `ResetDefaults` and presentation update functions. **`+0x2C8` `presentationStateWord`** — word read/written by `ResetDefaults` and presentation dirty-state functions.

Sixth tier (presentation state and resource slots): **`+0x49C` `lodViewScale`** — float initialized to `1.0f` and used as a view-dependent multiplier in `UpdateRootLODAndPresentationState`. **`+0x4A4` `presentationBlendFlags`** — dword with bit `0x2` and related flags reset/queried. **`+0x66D` `auxTransformState`** — byte bitfield with bit 1 ~~gating the three-channel auxiliary transform interpolation~~ asking the focus-point update to snap the smoothed vector `+0x680` once and clear the bit *(corrected 2026-10-02, OPUS: `003E43D0`+0x25F `test al, 2` through `003E43D0`+0x270 `movdqa xmmword ptr [rbx + 0x680], xmm0`)*; bit 2 reset by `ResetDefaults`. ~~**`+0x674`/`+0x678` are the previous X/Y scalars** for that interpolation.~~ **`+0x670`/`+0x674`/`+0x678` are the focus point's three components** *(corrected 2026-10-02, OPUS: `003E43D0` blends all three in one pass, reading `+0x674` at `003E43D0`+0xD2 and storing `+0x678` at `003E43D0`+0x12D; the focus-point page)*. **`+0x3D1` `presentationModeFlags`** — byte bitfield: bit `0x40` and low bits used by presentation and fade logic. **`+0xD3` `distanceFadeFlags`** — byte bitfield manipulated by `UpdateDistanceFadeAndCull`. **`+0x68`/`+0xD8`/`+0xF0` `maintainedResourceRef1/2/3`** — qword resource-reference slots written by `MaintainPresentationResourceReferences` and `RefreshLoadedResourceBindings`. **`+0x644`/`+0x648` `timedStateScalarA/B`** — floats read/written by `UpdateTimedPresentationStates` and initialized to `0`.

## 9. Related

- [`../Character-Rendering/character-render-object.md`](../Character-Rendering/character-render-object.md) — a **different** structure, deliberately contrasted in §5
- [`../../06-Movement-And-Navigation/heading-speed-to-position-delta.md`](../../06-Movement-And-Navigation/heading-speed-to-position-delta.md) — consumes the heading and speed this system may overwrite
- [`../../04-Actor-Entity/battleunit-slot-pool-and-actor-class.md`](../../04-Actor-Entity/battleunit-slot-pool-and-actor-class.md) — the other fixed slot pool in the engine; same idea, different budget

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Audio — CLIENT.** `FUN_00332c40`, owned by that layer, calls `002E9B80` on this page. That caller is an 857-byte step that demands bit 2 of `byte[+9]`, takes `word[+4]` as an index and skips the `0xFFFF` sentinel - and it indexes **the same `0x740`-byte records at `[022C6F28]`** the heading-speed step walks, testing their `dword[+0x284]`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Developer — SERVICE.** `0017D6E0` on this page calls `FUN_001c2f50`, owned by that layer. What it reaches is a string-assembling routine over the EASTL allocator at `008F6600`, the globals at `01F8127C` / `01DF6E38` / `01DF6E40` and the static empty buffer `02EBA2E0`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Save_Load_Settings — SERVICE.** `0017D6E0` on this page calls `FUN_001c1910`, owned by that layer. What it reaches is a 43-byte guard over the same `byte[+0x10]` flag: only when that is clear AND `byte[+0xA70]` differs from it does the release run, after which `+0xA70` is zeroed; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**CoreRuntimeScheduling — MECHANICAL (SWE2-CONTRACT 2026-09-15, 39 edges).** 23 edges are the
image-pointer fixup pair `0020E600`/`0020E620` inside this page's record-walk bodies; `0017D6E0`
calls seven CoreRT helpers (`001E0550`/`001E0590`/`001E05E0`/`001E05F0`/`001DB600`/`0022A490`/
`001A1460`); the remaining nine are the frame bodies `0022A770`/`0022B8C0`/`0022BC20` and `0017CCD0`
reaching `0017DE60`/`003323D0`/`00332660`. Shared infrastructure fan-in, not a scheduling
relationship the record array owns.

**RNG — CLIENT (SWE2-FRONTIER 2026-09-15, 1 edge).** `0022A0B0`, cited in §15 as the subtree's
single boot caller, also calls `00379CF0` in that layer — the startup hub's rng seeding on the
way through init. The edge is init-out from the boot hub, not a render-record responsibility;
the record array owns nothing in RNG.

**Script_VM_Native_Bridge — CLIENT (SWE2-EC7 2026-10-03, 38 edges).** Script-VM verb handlers
call this layer's record machinery: the element binder and the add-motion/event-channel body
each sit behind a block of handlers, and seven handlers tail-jump into
the EC7-222 flag/sync backends (`002E7150`, `002EBAD0`, `002E82E0`, `002E8BB0`, `002E8C70`,
`002ECF60`, `002ECFD0`); the remainder are the handler layer's shared arg-pop and
return-path helpers touching page-cited bodies. The crossing is verbs asking for record
writes, not bridge ownership of the records.

## 15. The `003325C0` exclusive subtree — all 33 members bound (SWE2-FRONTIER, followup queue)

`0022A0B0` calls `003325C0` exactly once at boot: a twelve-byte thunk that loads the
render-context block `022C6F30` into `rcx` and tail-jumps into
`CharacterRenderSystem_AllocateAndInitialize` (`003325D0`). Everything the exclusive
census counts hangs under that one call — the pool allocation §2 describes, the
subcontainer battery `0041E3A0`, the record/handler-table init `004269A0`, and the
`00426480` publish — and every member below was disassembled from the shipping image.
Interior citations are instruction addresses inside each member's declared extent.

| cluster | members | role | interior |
| --- | --- | --- | --- |
| root | `003325C0` | 12 B thunk — `lea rcx,[022C6F30]`, tail-jumps to `003325D0` | [`003325C0`](../../_index/ADDRESS-INDEX.md) |
| root battery | `003325D0` | 139 B — stores `rcx`→`022C6F20`, allocates `0x48930`→`022C6F28` (§2), then `0041E550`→`0041E3A0`→`004269A0`→`00426480` | [`003325EC`](../../_index/ADDRESS-INDEX.md) |
| | `0041E550` | 35 B — zeroes pool `+0xD90`/`+0xD98`/`+0xDA0`/`+0xDA8`, tails `0051C270` | [`0041E552`](../../_index/ADDRESS-INDEX.md) |
| | `0041E3A0` | 233 B — the eleven-arm subcontainer battery (all eleven callees are members) | [`0041E40B`](../../_index/ADDRESS-INDEX.md) |
| | `004269A0` | 741 B — `0041F730`×160 record clear, tail-field seeds, ~25 `0041D6xx` handler registrations, member-init battery, `+0x48818 |= 5` + config floats | [`004269C3`](../../_index/ADDRESS-INDEX.md) |
| | `00426480` | 30 B — `0020E620` image-pointer store of ~~the `0xA0` handle~~ the caller's pointer (`rdx`, `[022C6F20]`; the `0xA0` in `ecx` is unused) into pool `+0x48830` *(corrected 2026-10-02, OPUS: `00426480`+0x4 `mov rcx, rdx` before `call 0020E620`)* | [`00426493`](../../_index/ADDRESS-INDEX.md) |
| `0041E3A0` arms | `00409F80` | 18 B — `0040A230` table-seed, tails `0051FB70` | [`00409F84`](../../_index/ADDRESS-INDEX.md) |
| | `0040A230` | 2017 B — flat installer: exactly 144 `lea`(~~.text fn~~ **`.rdata` `obj_finish` path string**, CON-196)/`mov`(global) pairs seeding `02C65BF0`–`02C83C78`; no other logic | [`0040A237`](../../_index/ADDRESS-INDEX.md) |
| | `0046E4B0` | 28 B — `0051FB70(rcx)` then `005371A0(rcx+0x60)` | [`0046E4B9`](../../_index/ADDRESS-INDEX.md) |
| | `0046E250` | 96 B — `0051F9F0` container (tables `02CA61B0`/`02CA6250`) + `00537270(+0x60,1,2,edx<<5)` | [`0046E285`](../../_index/ADDRESS-INDEX.md) |
| | `00477EE0` | 52 B — `RenderModelInstanceContainer_InitializeStorage`: `0051F9F0` over `02CA74A0`/`02CA7540` (`0x260`/`5`) | [`00477F0A`](../../_index/ADDRESS-INDEX.md) |
| | `00478040` | 35 B — `RenderModelInstanceContainer_Reset`: `0051FB70` + `+0x60`=`0xFFFF`, `+0x62`/`+0x66`=0 | [`00478055`](../../_index/ADDRESS-INDEX.md) |
| | `0051B9D0` | 14 B — `PresentationEntryReferenceContainer_InitializeStorage`: tails `0051F170(rcx,0x40,rcx+0x30)` | [`0051B9D9`](../../_index/ADDRESS-INDEX.md) |
| | `0051BA20` | 27 B — `PresentationEntryReferenceContainer_ResetAndInitializeGlobals`: `0041CCA0` + `0051F2D0` | [`0051BA29`](../../_index/ADDRESS-INDEX.md) |
| | `00521300` | 17 B — clears `02CA8450`/`02CA8458` (the `005211F0` table pointer + sibling) | [`00521302`](../../_index/ADDRESS-INDEX.md) |
| | `00409F10` | 50 B — `0051F9F0` container (tables `02B62E40`/`02B62F80`, `0x50`/`5`) | [`00409F38`](../../_index/ADDRESS-INDEX.md) |
| | `005211F0` | 87 B — create-once `0x3000` alloc→`02CA8450`; fills 256×`0x30` records with `{0xFFFF,0xFFFFFFFF}` sentinels | [`00521201`](../../_index/ADDRESS-INDEX.md) |
| `004269A0` arms | `0041D6D0` | 15 B — `02CA4670[ecx*8] = rdx` handler-slot store | [`0041D6DA`](../../_index/ADDRESS-INDEX.md) |
| | `0041D6E0` | 8 B — `02CA4668 = rcx` handler-head store | [`0041D6E0`](../../_index/ADDRESS-INDEX.md) |
| | `003B6890` | 110 B — create-once `0x8C00`→`02B40528`; flag clears over ~~80×`0x1C0` records~~ the 160 `0xE0`-byte records, two per `0x1C0` step of an 80-pass loop *(corrected 2026-10-02, OPUS: `003B6890`+0x52 clears `+0x40` bit 0 at `-0xE0` and at `+0`, looping at `003B6890`+0x67; `0x8C00` / `0xE0` = 160)*; `02B40520`/`02B40524` counters | [`003B68AC`](../../_index/ADDRESS-INDEX.md) |
| | `003AFCD0` | 45 B — `02B3F554`=1, `02B3F550`=0, first-dword clear of 32×`0x70` table at `02B3F574` | [`003AFCD2`](../../_index/ADDRESS-INDEX.md) |
| | `004778A0` | 46 B — `02CA6C94`/`02CA6C90`=0, first-word clear of 32×`0x40` table at `02CA6CA0` | [`004778C0`](../../_index/ADDRESS-INDEX.md) |
| | `003AF2B0` | 102 B — create-once `0x3000`→`02B3F530`; byte-clear of 128×`0x60` records; `02B3F538`/`02B3F540`/`02B3F53C` counters | [`003AF2CA`](../../_index/ADDRESS-INDEX.md) |
| | `0042F000` | 33 B — `02CA4ED0`=0, first-dword clear of 32×`0x30` table at `02CA48D4` | [`0042F014`](../../_index/ADDRESS-INDEX.md) |
| | `003E0720` | 18 B — `00512EF0` then tail `0040DB70` | [`003E0724`](../../_index/ADDRESS-INDEX.md) |
| | `0040DB70` | 49 B — `02CA4390`=0, pushes `{float [01CEBBA8], 0}` to `0040B430` | [`0040DB97`](../../_index/ADDRESS-INDEX.md) |
| | `003B53C0` | 119 B — clears `02B40518` low bits, sentinel-fills descriptors `02B40508`/`02B40514`, then issues a kind-9 resource request (`0032E400`/`0032E620`/`0032E520`) for index `0x2A` and drains it | [`003B5407`](../../_index/ADDRESS-INDEX.md) |
| PresentationEntryReferenceContainer | `0051F170` | 27 B — generic-list init: `+4` flag fix, `+0x10`=count, `+8`=arena, tails `0051F2F0` | [`0051F182`](../../_index/ADDRESS-INDEX.md) |
| | `0051F2D0` | 24 B — node-state reset: `+0x1C`=`-1`, `+0`/`+0x10`/`+0x18`/`+8`=0 | [`0051F2D2`](../../_index/ADDRESS-INDEX.md) |
| | `0051F2F0` | 132 B — `InitializeNodes`: picks the arena by `+4` mode bits (0→`003AB7F0` alloc, 1→`[+8]` static), fills `[+0x10]`×`0x30` nodes `{idx,-1,-1,0,0,0}` | [`0051F340`](../../_index/ADDRESS-INDEX.md) |
| `0051EExx` arena helpers | `005371A0` | 26 B — `0051EE10(rcx)` then `+0x20`=0 | [`005371A9`](../../_index/ADDRESS-INDEX.md) |
| | `00537270` | 89 B — `0051F020` arena alloc of `edx*edi` bytes, stores dims at `+0x20`/`+0x24`, optional `005371C0` fill pass | [`00537296`](../../_index/ADDRESS-INDEX.md) |
| | `005371C0` | 148 B — `0051EE30`+`006B5C70` resolve, then `edi`× per-element `rsi(base)` stepping `+0x20`; tails `0051EF80` | [`00537220`](../../_index/ADDRESS-INDEX.md) |

Shared callees with other callers are excluded from the census — the allocation trio
`0036C1D0`/`0036A100`/`0036C140`, image-pointer fixup `0020E620`, generic-container
`0051F9F0`/`0051FB70`/`0051C270`, arena family `0051EE10`/`0051EE30`/`0051EF80`/`0051F020`,
`003AB7F0`/`006B5C70`/`0040B430`/`00512EF0`, the per-record clear `0041F730`, the third
handler writer `0041D6C0`, and the resource-queue trio `0032E400`/`0032E620`/`0032E520`.

## The system tail's whole access census — `BT-3` answered (OPUS, 2026-09-15)

`BT-3` asks what the rest of the `0x130`-byte system tail is, "beyond the four fields read (list
head `+0x00`, encoded root `+0x30`, gate `+0x42`/`+0x43`)". **The four-field premise was already
stale** — the type store carries **24** fields for `CharacterRenderSystemTail` — and the question
behind it is answerable exactly, because the tail is addressed as `pool + 0x48800 + offset`, so a
displacement census over `.text` is a complete census of it.

**Measured** (`work/OPUS/tail_census.py`, `tail_compare.py`; every listed body in `functions.tsv`
decoded, displacements in `[0x48800, 0x48930)` collected):

| | |
|---|---:|
| pool-relative offsets touched | **24** |
| accesses over them | **152** |
| offsets in the type store | **24** |
| touched but not declared | **0** |
| declared but never touched | **0** |
| of the 24, carrying a name | 9 |
| of the 24, `UNRESOLVED` | 15 |

**The store and the image agree exactly**: every offset any listed body touches is recorded, and
every recorded offset is touched. So the discovery half of `BT-3` is closed — there is no
undiscovered field in this object.

**And the last 192 bytes are dead.** The highest offset touched is `+0x06C` (4 bytes), so
**`[+0x070, +0x130)` — 192 of the 304 bytes — carries no access at all.** The object is declared
`0x130` because that is the tail of a single `0x48930` allocation, not because anything uses the
space.

**Ten offsets have exactly one access site**, all in `CharacterRenderSystem_Initialize` except
`+0x020`: `+0x020`, `+0x040`, `+0x04C`, `+0x050`, `+0x054`, `+0x058`, `+0x05C`, `+0x060`, `+0x064`,
`+0x06C`. Those are the constructor-written, never-read fields the store already flags.

### Two blind spots, stated

- **The instrument is displacement-based.** An access through a pointer already computed into the
  span — `lea rbx, [pool + 0x48870]` then `mov [rbx], eax` — carries no displacement in range and is
  invisible here. The 192-byte statement is "no listed body addresses it by displacement", not "no
  byte of it is ever written".
- **It covers listed bodies only.** The 244,619 bytes of unlisted `.text`
  ([the unlisted-code census](../../99-Unresolved-Residual/Unlisted-Code/the-code-the-function-list-does-not-contain.md))
  are not scanned.

**A control, because a clean agreement is worth nothing from an instrument that cannot be wrong.**
The raw scan returned **27** offsets, not 24. The extra three — `+0x05B`, `+0x07C`, `+0x0B2`, all
8-byte and two of them unaligned — are `lea rN, [rip + 0x488xx]` inside `FUN_0044CC50`, which is
RIP-relative addressing of unrelated data that merely lands at the same numeric displacement. They
are excluded by base register, and they are why the raw count is reported here rather than the tidy
one: the same false-positive class that the descriptor-list census hit at `+0x50`/`+0x60`/`+0xB0`.

**What remains open is meaning, not discovery**: the 15 `UNRESOLVED` rows in the store. That is the
type store's worklist, and it is not this row.

## Four per-descendant callbacks, read whole (2026-09-19, FABLE)

Several dirty-state handlers finish by walking the record's two child chains (words `+8` and `+0xA`) with
`CharacterRenderHierarchy_TraverseIndexDepthFirst` `0042EF90`, handing it a callback `(descendant, context)`. Four of
those callbacks, none of which any page cited:

| callback | handed over by | what it does to each descendant |
|---|---|---|
| `0042D810` (22 B) | `00428B30` | copies **bit 0 of context byte `+0x60` into bit 3 of `+0x4B7`** - the same bit `00428B30` has just set on the parent (`00428BD2`..`00428BE1`), so the setting reaches the whole subtree |
| `0042E300` (22 B) | `0042AC30` | when the descendant's resolve-state word `+0x2F2` is non-zero, copies **context word `+0x20` into `+0x3FA`** (the cached selector word) |
| `0042E320` (36 B) | `0042AE00` | for a descendant with no parent or with `+0x2F2 == 1`: loads `rdx` from context `+0x18`, `r8` = 0, `r9` = 1 and **jumps to `0016D6A0`** |
| `0042E350` (37 B) | `0042AF10` | the same with `r8` = context dword `+0x20` |

**The last two do nothing in this build.** `0016D6A0` is `ret 0` - an empty function (see the correction above). The
arguments they prepare show what the missing callee took - an object from the context, an optional value, and the
constant 1 - but there is nothing left to receive them, and the hierarchy walks of `0042AE00` and `0042AF10` that exist to
run these callbacks have no effect. *A reimplementation can drop both walks; it cannot learn from this image what they
were for.*

**A fifth, and the cascade that runs it (added 2026-09-19, FABLE; three bodies read whole).** `0042E550` (192 B)
**re-poses one record against its parent**: it resolves the record's model entry and, through the parent index `+6`,
the parent record's; a record with a model has the skeleton's parent-transform propagation run with (its model, the
parent's model or null) and then its final pose updated. `00428E70` (152 B) runs it on a record, on its child `+8`,
and depth-first down the child's chains `+8` and `+0xA`. The dirty-state pass runs that cascade under **dirty bit 12
of `+0x290`** - or, when a flag the pass holds is set, **defers it**: it walks `+6` to the chain's root and raises bit 25
of the root's `+0x294` instead (`00428033`..`00428068`). `00427BD0` runs it too, right after installing the record's
`+0x180` block into the model. Separately, `004209C0` (38 B) copies the record's sixteen bytes at `+0x2E0` into its
model instance's `+0xD0`, from the root and the child LOD updates; *what that vector is was not established.*
Interior: `0042E55F`, `0042E582`, `0042E591`, `0042E5BD`, `0042E5DB`, `0042E5F3`, `0042E5FB`; `00428E9F`, `00428EA4`,
`00428EC6`, `00428EDF`, `00428EF8`.

## SWE2-EC7-61 update (2026-09-19) - `0042F310`

`0042F310` (151 B) is the `+0x290`:19 attach-flag setter the record-array page names - call-free `movsx` index x`0x740` into `022C6F28`, `cmove` fallback, `bts +0x284`:30 under `+0x284`:2 gate then `bts +0x290`:19 (verifies the page). Interior anchor `0042F39C` (the `bts +0x290`:19 the page names).


## SWE2-EC7-68 update (2026-09-19) - `003E55B0` `CharacterRenderRecord_ResolveModelInstance` measured

`003E55B0` (53 B) is the resolver the page names, now read from the
image: `word[rcx+0x64]` is the model-instance selector - `-1`
returns NULL with no work; otherwise `0020E600(dword[rcx+0x10])`
resolves the record's context object and `qword[rax+0xDA0]` is its
instance table, handed with the selector word to `004780B0` by tail
jump. Interior anchor `003E55CB` (the `0020E600` context resolve).

## Interior citations for the entry-cited functions (OPUS, 2026-10-01)

*Functions this page named only at their entry. Each was read from the certified image; the sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Verified by [`renderrec_interior.py`](../../_index/candidates/opus-renderrec-interior-1001/renderrec_interior.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0015CC90` | 37 B | calls `001E1520(01F82D60, 20000)`, then tail-jumps to `00808B90(008A6C70)` | `0015CC94`, `0015CCA0`, `0015CCB0` |
| `002E87F0` | 164 B | for a non-null `rcx` whose dword `+0` and word `+0` are not -1, takes the 0x740-byte record (signed word `+0`) of `[022C6F28]`; when its dword `+0x284` is non-zero: with `edx` non-zero clears bit 13 and sets bit 12 of dword `+0x304`, with `edx` 0 clears bits 12-13; either way sets bit 22 of dword `+0x290` | `002E8817`, `002E8827`, `002E8830`, `002E883A`, `002E887F` |
| `00332510` | 124 B | stores `022C6F30` in qword `022C6F20` and calls `001EB150("display character : preprocessing" at 00D10A38)`, `004264A0` and `001EB110`; stores it again and calls `001EB150("display character : draw objects" at 00D10A80)`, `0041E4D0([022C6F20])` and `001EB110`; calls `001EB150("display character : after emission" at 00D10AA8)` and `00425DC0` with qword `022C6F28` as read before the second string, then tail-jumps to `001EB110` | `00332528`, `0033252F`, `0033255F`, `00332578`, `00332587` |
| `00342410` | 59 B | calls `002E88A0(rdx, 1)`, then tail-calls `002E8900(rdx)` with `xmm1` = `00267DB0(r9)` | `00342421`, `00342431`, `00342446` |
| `00342CF0` | 59 B | calls `002E8950(rdx, 1)`, then tail-calls `002E89B0(rdx)` with `xmm1` = `00267DB0(r9)` | `00342D01`, `00342D11`, `00342D26` |
| `003B6000` | 27 B | clears bit 0 of byte `+0x40` of record `cl` of the 0xE0-byte records at `[02B40528]` when its dword `+0x10` equals `ecx` | `003B6003`, `003B600A`, `003B6011`, `003B6016` |
| `0041CEA0` | 22 B | when qword `+0x18` is non-null, sets bit 3 of dword `+0xC` when `edx` is 1, else clears it | `0041CEA7`, `0041CEAC`, `0041CEB1` |
| `00423050` | 70 B | when dword `+0xC4` is not -1, looks up `0051B9E0(qword +0xDA8 of 0020E600(dword +0x10), dword +0xC4)` and tail-calls `0041C6B0` on it; returns 0 when there is none | `00423056`, `00423065`, `00423077`, `00423089`, `0042308E` |
| `00423570` | 76 B | when dword `+0xC4` is not -1, looks up `0051B9E0(qword +0xDA8 of 0020E600(dword +0x10), dword +0xC4)` and, when found, calls `0041CEA0(it, edx)` | `0042357A`, `0042359D`, `004235AC` |
| `00423AB0` | 87 B | stores `xmm1` in float `+0x2BC`; when dword `+0xC4` is not -1, looks up `0051B9E0(qword +0xDA8 of 0020E600(dword +0x10), dword +0xC4)` and, when found, calls `0041C7C0(it)` with `xmm1` | `00423AC8`, `00423AE7`, `00423AF7` |
| `004270A0` | 85 B | when `xmm1` is 0.0, calls a 249-byte record helper and sets dword `+0x294` to (itself AND `0xFFFDFA7F`) OR 0x20; otherwise stores `xmm1` in float `+0x308` and sets `+0x294` to (itself AND `0xFFFDFB5F`) with bit 8 set | `004270AC`, `004270B3`, `004270BE`, `004270D2`, `004270E5` |
| `004272C0` | 26 B | sets bit 23 of dword `+0x294`, stores `xmm1` in float `+0x3C0` and `r8d` in dword `+0x3C4` | `004272CA`, `004272D2` |
| `004272E0` | 21 B | sets dword `+0x294` to (itself AND `0xFFFDFA7F`) OR 0x20 | `004272E6`, `004272EB`, `004272EE` |
| `00427300` | 19 B | sets bit 15 of dword `+0x294` and stores `xmm1` in float `+0x3BC` | `0042730A` |
| `00427880` | 35 B | sets bit 16 of dword `+0x294` and stores `xmm1`, `xmm2` and `xmm3` in floats `+0x3C0`, `+0x3C4` and `+0x3C8` | `0042788A`, `00427892`, `0042789A` |
| `004278B0` | 17 B | sets bit 22 of dword `+0x294` and stores `edx` in dword `+0x3C4` | `004278BA` |
| `00428DE0` | 36 B | sets bit 10 of dword `+0x304` when `edx` is non-zero, else clears it, and sets bit 29 of dword `+0x290` | `00428DEA`, `00428DEE`, `00428DF3`, `00428DF9` |
| `00428E10` | 36 B | sets bit 11 of dword `+0x304` when `edx` is non-zero, else clears it, and sets bit 30 of dword `+0x290` | `00428E1A`, `00428E1E`, `00428E23`, `00428E29` |
| `0042D810` | 22 B | copies bit 0 of byte `+0x60` of `rdx` into bit 3 of byte `+0x4B7` | `0042D814`, `0042D81D`, `0042D81F` |
| `0042E300` | 22 B | when word `+0x2F2` is non-zero, copies word `+0x20` of `rdx` to word `+0x3FA` | `0042E308`, `0042E30A`, `0042E30E` |
| `0042E320` | 36 B | when word `+6` is -1 or word `+0x2F2` is 1, tail-calls `0016D6A0(rcx, qword +0x18 of rdx, 0, 1)` | `0042E327`, `0042E331`, `0042E33B`, `0042E33E` |
| `0042E350` | 37 B | when word `+6` is -1 or word `+0x2F2` is 1, tail-calls `0016D6A0(rcx, qword +0x18 of rdx, dword +0x20 of rdx, 1)` | `0042E357`, `0042E361`, `0042E36B`, `0042E36F` |
| `0042E4B0` | 63 B | when word `+6` is -1 or word `+0x2F2` is 1, calls `0016D6A0` with its own incoming arguments; then, when word `+6` is -1, zeroes dword `+0x58` of `rdx` | `0042E4C7`, `0042E4D1`, `0042E4D6`, `0042E4DD` |
| `00504740` | 117 B | returns 1.0 (`01CEBBA8`) unless a match is found: for a non-null `rcx` with dword `+0x208` not -1, takes A = dword `+0x1F8` + dword `+0x208` (a 32-bit sum used as an address), scans the byte `A+0x30` count of 0xE0-byte records from `A` + word `A+0x38` for one whose byte `+0` equals signed byte `+0xB8` of `rcx`, and returns that record's float `+0x18` | `0050475E`, `00504764`, `0050478B`, `00504796`, `005047AD` |
| `0051EE10` | 20 B | zeroes dwords `+0` and `+0x10` and qword `+8`, and stores 0x800 in qword `+0x14` | `0051EE12`, `0051EE1A`, `0051EE1C`, `0051EE20` |
| `0051EE30` | 69 B | copies from `rdx` its qword `+8` passed through the 42-byte external-source handle check (null stays null) and its dwords `+0x10`, `+0x14` and `+0x18` | `0051EE4F`, `0051EE54`, `0051EE5B`, `0051EE67` |
| `0051F020` | 91 B | stores `003AB8B0(edx, dword [rcx])` in qword `+8` and `edx` in dword `+0x10`, calls the 42-byte external-source handle check on the new qword, and when `r8d` is 1 zeroes `edx` bytes at `003AB7F0(qword +8)` with `00861EC0` | `0051F03C`, `0051F044`, `0051F04B`, `0051F059`, `0051F066` |

## Homed bodies re-homed here for host fit (FABLE, 2026-10-03; AUDIT-SPEC batch 6)

*FABLE's homing stream (cloud-drafted, FABLE-verified) homed these bodies on other pages. SWE2-AUDIT-SPEC reviewed each sentence, site and anchor set and rejected the host, because that page named the caller only in passing. The sentences are unchanged except where the review gave replacement wording, which the row's line below says. Each states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Why each row is here:*

- `00420860`: this page documents its caller `00427DE0` as a subject (a list item, a paragraph). The sentence carries the review's replacement wording (the source-block-mover review, Repair 3: the callee `006C0520` reads `xmm1`-`xmm3`, never `rdx`, `r8` or `r9`).
- `004209F0`: this page documents its caller `00427DE0` as a subject (a list item, a paragraph).

*Verified by [`move_rows.py`](../../_index/candidates/fable-home-host-moves-b6-1003/move_rows.py): every site transfers to its function; the caller named above (for a thunk, the thunk's callers) is a subject of this page outside this section - an address in a heading, the first address of a table row, or the first address of a paragraph or list item; and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors | moved from |
|---|---|---|---|---|---|
| `00420860` | 35 B | `00427DE0` + 0xD7 | calls the site `00420860` + 0x19 with `rcx+0x210`, the floats `xmm1`, `xmm2` and `xmm3` passed through, and 1.0 (`01CEBBA8`) as the fifth (stack) argument, then returns | Interior anchor `00420864`; Interior anchor `0042086C`; Interior anchor `00420873`; Interior anchor `00420879` | [the-source-block-mover-and-separate-consumer-refresh](../../02-Resource-And-Asset-Pipeline/the-source-block-mover-and-separate-consumer-refresh.md) |
| `004209F0` | 22 B | `00427DE0` + 0xA2 | ORs 0x200 into dword `rcx+0x284`, then tail-jumps at the site `004209F0` + 0x11 with `rcx+0x180` and the other registers unchanged | Interior anchor `004209FA`; Interior anchor `00420A01` | [the-source-block-mover-and-separate-consumer-refresh](../../02-Resource-And-Asset-Pipeline/the-source-block-mover-and-separate-consumer-refresh.md) |

## SWE2-EC7-222 update (2026-10-03) - the render-record flag verbs' seven backends

Five presentation verbs and the two halves of `stdmotioneventsync` all reach the same render record the actor's secondary context points at. Their handlers take the actor in `rcx`, and each body resolves `[actor + 0xC0]`, reads the bound element's render-record index (word `+0` of the context's `+0` element, or its dword `+0` for `stdmotioneventsync`), rejects `-1`, and lands on `022C6F28 + 0x740*index` - the same bound-record chain the element binder builds, with the same `+0x284` liveness test this page documents. `bonephysical` additionally walks the `+0x90` element (the `k = 4` slot). None touches the record when the chain is broken.

| function | size | verb / caller | what the body does | interior anchors |
|---|---|---|---|---|
| `002E7150` | 108 B | `denybonephysical` `0x03D6` (handler `0034CCB0` tail-jumps with the popped int in `edx`) | resolves `[rcx+0xC0]`, its word `+0` (the element's render-record index, `-1` = unbound) and `022C6F28 + 0x740*index`; when the record's `+0x284` is non-zero it calls `003E68A0(record, edx != 0)` and ORs `0x800` into `+0x290` - the deny flag through the controller, plus the dirty bit | Interior anchor `002E715C`; Interior anchor `002E717F`; Interior anchor `002E718F`; Interior anchor `002E71A3`; Interior anchor `002E71A8` |
| `002EBAD0` | 165 B | `bonephysical` `0x0169` (handler `00350350` tail-jumps with the popped int in `edx`) | resolves two elements of `[rcx+0xC0]` - the `+0` element and the `+0x90` element (the `k = 4` slot) - through the same word-index/`0x740`-record chain and calls `00428960(record, edx)` on each live record; | Interior anchor `002EBAE3`; Interior anchor `002EBB06`; Interior anchor `002EBB1F`; Interior anchor `002EBB30`; Interior anchor `002EBB65` |
| `002E82E0` | 96 B | `setcharfogstatus` `0x0346` (handler `00347BC0` tail-jumps with the popped int in `edx`) | same resolution to the bound record; clears bit `0x200` of dword `+0x304`, sets it when `edx != 0` (`neg`/`sbb`/`and 0x200`/`or`), then ORs `0x2000000` into `+0x290` - the fog-disable write and its dirty bit | Interior anchor `002E82E5`; Interior anchor `002E8303`; Interior anchor `002E831C`; Interior anchor `002E8326`; Interior anchor `002E8335` |
| `002E8BB0` | 87 B | `setzclipoverdraw` `0x0283` (handler `00342120` tail-jumps with the popped int in `edx`) | same resolution; when `+0x284` is non-zero it `bts`/`btr`s bit `0x17` of that dword itself by `edx != 0` - no separate dirty bit, the flag lives inside `+0x284` | Interior anchor `002E8BB5`; Interior anchor `002E8BF1`; Interior anchor `002E8BFC` |
| `002E8C70` | 79 B | `setshadowratio` `0x028A` (handler `00343870` tail-jumps with the popped float in `xmm1`) | same resolution; stores `xmm1` at float `+0x3FC` of the live record and ORs `0x200000` into `+0x290` | Interior anchor `002E8C75`; Interior anchor `002E8CAC`; Interior anchor `002E8CB4` |
| `002ECFD0` | 80 B | `stdmotioneventsync` `0x0473` begin half (handler `003479E0` tail-jumps) | resolves `[rcx+0xC0]`'s dword `+0` - the element's `entryId` - and calls `0042F210(entryId, 0)` and `0042F210(entryId, 1)`, which clear bits 0 and 1 of the bound record's byte `+0x419` - the motion-event pending bits, reset before the sync | Interior anchor `002ECFD9`; Interior anchor `002ED000`; Interior anchor `002ED005` |
| `002ECF60` | 98 B | `stdmotioneventsync` `0x0473` poll half (handler `00347DD0` tail-jumps) | same `entryId` resolution; calls `0042F1C0(entryId, 0)` and `0042F1C0(entryId, 1)` - the `+0x419` bit tests - returning that callee's non-zero answer at the first set bit, or `2` when neither bit is set | Interior anchor `002ECF6D`; Interior anchor `002ECF97`; Interior anchor `002ECF9A`; Interior anchor `002ECFA5` |
