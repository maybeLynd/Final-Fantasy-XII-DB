---
system: Movement mode selection — 3-D or flat
category: 06-Movement-And-Navigation
status: AUDITED — SD-191 and SD-192 are ANSWERED and every box on the page is closed (owner re-status 2026-09-30, OPUS) — residue registered as SD-191 (which scripted sequences use which party-swap verb pairs) and SD-192 (whether the six +0x14F bit-0 readers each refuse movement), both since answered (§7); BV-1 to BV-5 answered (§7, evidence rows added 2026-09-30); what 00262F50 does with the table entry read 2026-09-18 (it links the summon stand-in to the party member and flags the stand-in's record); K-6 answered 2026-09-07 (+0xA8 is the facing angle) and closed on this page 2026-09-12 (status line current 2026-09-30, SWE2-DATA)
owner_layer: PrimaryOwner:Movement
evidence_tier: 1
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
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: GN158 checkpoint 2ed8affb… / snapshot 46f02e26…, project GFZ_HD2
  falsification_passes: 1
  last_falsification: 2026-09-03
  last_falsification_by: repos-d2
  falsification_result: 1 claim overturned, 8 survived — see section 10
  crossref_clean: true
  reopened_count: 0
  promoted: 2026-10-01 DOCUMENTED -> AUDITED by SWE2-AUDIT-SPEC (FRONTIER eligibility census sweep): falsification record GN158 checkpoint 2ed8affb… / snapshot 46f02e26…, project GFZ_HD2; audit_crossrefs at HEAD reports 0 unresolved findings; cross-subsystem neighbours dispositioned in their section; killer observations recorded in the pass; promoter is not the last substantive author (last substantive commit: OPUS)
---

# Movement mode selection — 3-D or flat

> Two small predicates decide whether a creature's movement is computed in full three dimensions or
> flattened onto the ground plane. Between them they are 115 bytes, and they change what every walk
> in the game costs.

## 1. What the player sees

Some things in FFXII move on the ground and some move through the air, and the engine does not treat
them the same way. A creature restricted to the ground has its motion computed flat — direction and
speed, nothing vertical. A creature that flies or swims has the same motion computed as a direction
in three dimensions, with a climb angle.

The player-visible consequence of the second case is the one documented next door: **when movement is
computed in 3-D, a slope costs you ground.** The forward speed you asked for is shared between
horizontal and vertical motion, so the same requested speed carries you less far across the map when
you are climbing. In the flat case that does not happen — the whole speed goes into horizontal
motion, always.

So the two paths do not just differ in precision. They produce visibly different travel times over
the same sloped ground, and which one a creature gets is decided by two flags on its controller.

## 2. Native mechanism

Three separate things combine, and it is worth keeping them apart because the database has previously
conflated the last two.

### The actor class — three bits at the top of a byte

Every actor carries a class in the top three bits of the byte at `actor + 0x03`:

```c
class = *(u8 *)(actor + 3) >> 5;
```

`FUN_00265200` is the engine's **canonical heading accessor** — 55 bytes, and with **33 distinct
callers it is the most-called single function in this neighbourhood.** It reads a different field
depending on the class:

```c
if (class == 1) return *(f32 *)(*(void **)(actor + 0xB8) + 0x38);
if (class == 3) return *(f32 *)(*(void **)(actor + 0xB8) + 0xA8);
return 0;
```

Two facts follow. **Classes 1 and 3 have differently-shaped movement states** — the same conceptual
value lives at `+0x38` for one and `+0xA8` for the other. And **every other class returns zero**: a
class-0 or class-2 actor has no heading as far as the rest of the engine is concerned.

### The 3-D selector — two adjacent bits on the controller

`FUN_00264460` is 37 bytes and answers "does this actor move in three dimensions?":

```c
if (actor == 0 || *(void **)(actor + 0xC0) == 0) return 0;
b = *(u8 *)(*(void **)(actor + 0xC0) + 0x151);
return (b >> 1 | b) & 1;              /* true if bit 0 OR bit 1 is set */
```

It is called from exactly **three** functions at four sites — the delta computation, the steering
update (twice) and the position integrator — which is to say, every place the answer could matter.

The `(b >> 1 | b) & 1` idiom is worth reading carefully: it is **not** a two-bit field, it is an
**either** — two independent flags that both enable 3-D movement. The engine does not distinguish
which one is set.

### The flat selector — and it needs the actor system to be up

`FUN_00267260` is 78 bytes and is the other half. The flat path is taken when it is true **and** the
3-D selector is false:

```c
if (ActorSystemReady() == 0) return 0;                       /* 003B7730 */
o = *(void **)(actor + 0xC0);
if (!(o == 0 || ((*(u8 *)(o + 0x14F) & 1) == 0 && *(void **)(o + 0x138) != 0))) return 0;
if ((*(u8 *)(actor + 9) & 1) == 0) return 0;
return (*(u8 *)(actor + 8) >> 1) & 1;
```

Both selectors read the **same controller object** at `actor + 0xC0`, at neighbouring bytes `+0x14F`
and `+0x151` — so there is a flags region there that governs how this actor moves.

### The gate is "the actor system is initialised", not a feature switch

> **OVERTURNED in section 10.** Both globals are written during **normal runtime**, not only at
> bootstrap and teardown. `02B40530` has a dedicated 7-byte setter (`003B7E10`) called from
> **six sites** passing an explicit `0` or `1`, and `02B40534` has **eight** writers including
> three that clear it. The reading below is right that it is not a tuning switch, and the
> bootstrap/teardown framing is too narrow.

`FUN_003B7730` is 27 bytes:

```c
return (DAT_02B40530 != 0 && DAT_02B40534 != 0) ? 1 : 0;
```

**Both globals are zero in the shipped image** — they lie past the end of `.data`'s raw contents, so
they are zero-filled at load. The obvious reading, that the flat path is dead code, is wrong: they
have real writers, and the one that sets **both** is `FUN_003B6ED0`, an **actor-module initialisation
and reset** that zeroes a block of actor list/handle state at `02EBCAxx`–`02EBCCxx` and sets both
flags to `1` on the way through.

So this is not a tuning switch. ~~It is *"the actor system has been brought up"*, and it reads as a~~
~~guard against running the flat path during bootstrap or after a teardown, when the controller state~~
~~it depends on is not valid.~~ *(corrected 2026-10-02, OPUS: overturned in §10 — `02B40530` is set by `003B7E10` from six sites and `02B40534` by eight stores, the party-swap verbs among them, during normal runtime)*

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `00265200` | `Movement_GetHeadingForActorClass` | 55 B | the canonical heading accessor — **33 distinct callers**; class 1 → `+0x38`, class 3 → `+0xA8`, else 0 |
| `00264460` | `Movement_ActorUsesThreeDimensionalMotion` | 37 B | `(bit0 \| bit1)` of controller `+0x151` |
| `00267260` | `Movement_ActorUsesFlatMotion` | 78 B | actor-system gate + controller validity + two actor flags |
| `003B7730` | `ActorSystem_IsInitialised` | 27 B | `DAT_02B40530 != 0 && DAT_02B40534 != 0` |
| `003B6ED0` | `ActorModule_InitialiseAndReset` | — | sets **both** gate globals to 1 while zeroing actor list/handle state |
| `002E4380` | `Movement_ComputeDeltaFromHeadingSpeed` | 601 B | consumer; calls the 3-D selector |
| `002E5610` | `Movement_IntegratePositionAndMeasureDisplacement` | 314 B | consumer; calls the 3-D selector at `002E56B7` |
| `002E45E0` | `Movement_UpdateSteeringTowardTarget` | — | consumer; calls the 3-D selector at two sites |

Addresses are Ghidra image base `0x00120000`. Every row above is a function.

### Data addresses cited by this document

| Address | Name | Kind | Contents |
|---|---|---|---|
| `02B40530` | actor-system ready flag A | `u32` | **zero in the image** (BSS); set to 1 by `003B6ED0` |
| `02B40534` | actor-system ready flag B | `u32` | **zero in the image** (BSS); set to 1 by `003B6ED0`, and ~~by eight other writers in the same subsystem~~ written by seven other functions in the same subsystem *(corrected 2026-09-30, SWE2-DATA: eight store sites in eight functions in all, `003B6ED0` included — §7, BV-5; `_index/candidates/dd-data-5-0930/mm_checks.py` W1)* |

## 4. Data structures and formulas

### Actor fields read by the selectors

```
WorldActor
  +0x03  u8   classBits      class = value >> 5
  +0x08  u8   flags          bit 1 is the flat-motion enable
  +0x09  u8   flags          bit 0 must be set for flat motion
  +0xB8  ptr  movementState
  +0xC0  ptr  controller
```

```
controller (at actor +0xC0)
  +0x138  ptr  required non-null for the flat path
  +0x14F  u8   bit 0 must be CLEAR for the flat path
  +0x151  u8   bit 0 OR bit 1 selects THREE-DIMENSIONAL motion
```

### Class → heading field

```c
class = actor[3] >> 5;
class 1 -> movementState + 0x38
class 3 -> movementState + 0xA8
else    -> 0
```

### The 3-D test, exactly

```c
b = controller[0x151];
threeD = (b >> 1 | b) & 1;      /* bit 0 OR bit 1 -- an EITHER, not a 2-bit field */
```

### The flat test, exactly

```c
flat = ActorSystemReady()
    && ( controller == NULL
         || ((controller[0x14F] & 1) == 0 && *(void **)(controller + 0x138) != NULL) )
    && (actor[9] & 1) != 0
    && ((actor[8] >> 1) & 1) != 0;
```

### Mode selection, as the consumers evaluate it

```c
if (Movement_ActorUsesFlatMotion(actor) && !Movement_ActorUsesThreeDimensionalMotion(actor))
        -> planar path: pitch terms dropped
else    -> spherical path: X and Z foreshortened by cos(pitch)
```

Note the asymmetry: **3-D is the default.** Flat motion requires four conditions to hold; 3-D requires
one bit of one byte. An actor whose controller is missing, or whose system is not up, gets the
spherical path.

### The gate

```c
ActorSystemReady() = (DAT_02B40530 != 0) && (DAT_02B40534 != 0);
```

Both are zero at image load. `003B6ED0` sets both to `1`.

## 5. Call chain

```
actor system bootstrap   <- corrected 2026-10-02, OPUS - not only at bootstrap: both flags are also written at runtime (section 10; 003B7E10, the party-swap verbs)
  -> ActorModule_InitialiseAndReset  003B6ED0
     -> DAT_02B40530 = 1, DAT_02B40534 = 1     [the gate opens]

per movement update
  -> Movement_ComputeDeltaFromHeadingSpeed         002E4380
     -> Movement_ActorUsesThreeDimensionalMotion   00264460
     -> Movement_ActorUsesFlatMotion               00267260
        -> ActorSystem_IsInitialised               003B7730
     -> spherical or planar delta

  -> Movement_UpdateSteeringTowardTarget           (2 call sites)
  -> Movement_IntegratePositionAndMeasureDisplacement 002E5610
```

**Upstream:** the movement update. **Downstream:** the delta formula documented in
[`../heading-speed-to-position-delta.md`](../heading-speed-to-position-delta.md) — these two
predicates are what select between its two branches.

**Do not confuse with:**

- **The class byte and the controller flags are independent.** Class (`actor+0x03 >> 5`) decides
  *where the heading lives*; the controller bits decide *how the motion is computed*. A class-3 actor
  is not automatically a 3-D mover.
- **`FUN_003B7730` is not a feature toggle.** Its globals are zero in the image, which invites reading
  the flat path as dead. It is an initialisation gate.

## 6. Modding notes

- **Best intervention point:** controller `+0x151` bit 0. One bit, per actor, and it switches that
  creature between flat and 3-D motion with no other side effects in these two functions.
- **Regenerates itself:** nothing here. These are pure predicates over stored flags.
- **Breaks if:**
  - You clear `+0x151` expecting flat motion. Flat needs **four** further conditions; clearing the
    3-D bit without them gives you neither branch's intent.
  - You set the gate globals directly. They are actor-module state, and `003B6ED0` zeroes a large
    block alongside them — the flags are a *consequence* of initialisation, not its switch.
  - You assume classes 1 and 3 share a movement-state layout. They do not; the same value is at
    `+0x38` and `+0xA8` respectively.
- **Multiplayer / XIIOnline:** the mode is derived from **authored** actor and controller flags, so
  it is identical on every client without replication. The *result* — position — is local derived
  state. If two clients ever disagree about an actor's motion mode, the cause is divergent authored
  data or a failed actor-module init, not desync.
- **Mod compatibility:** the class bits and the controller flags are authored per actor and are a
  legitimate surface for a mod to change.

## 7. What is not known

- [x] ~~**What the two 3-D bits at controller `+0x151` distinguish.** The engine treats them as an
      either; something must set them differently. Flying versus swimming is the obvious guess and is
      **not** asserted here.~~ **`BV-1` ANSWERED 2026-09-12 (FABLE): bit 0 is *fly*, bit 1 is
      *float* — the engine's own verb names.** Each bit has exactly one Boolean setter and each
      setter is the body of a script verb:
      - **bit 0 — fly status.** `0026A7F0(actor, on)` (`0026A809`–`0026A815`) is verb `01E0`
        **`setflystatus(on)`** (`00342E50`). Turning it on also moves the controller's `+0x152` from 1
        to 2, turning it off from 2 back to 1 (`0026A82B`–`0026A850`, with `002681E0` after either
        change), so `+0x152` is the locomotion kind (1 ground, 2 airborne) that `00265B60` initialises
        to 1 (`00265E30`).
      - **bit 1 — float status.** `0026A7C0(actor, on)` (`0026A7D1`–`0026A7E0`) is verb `01E1`
        **`setfloatstatus(on)`** (`00343200`); it changes nothing else.
      - Both setters end in `002682D0`, which copies the two bits into the movement body's flag word
        (`body + 0x30 + 0x60`, bits 0 and 1, `002682F6`–`0026831A`) — the copy
        [the context census](../../04-Actor-Entity/Actor-Contexts/the-movement-and-secondary-context-censuses.md)
        already noted. The getters are `002644C0` (bit 0), `00264490` (bit 1) and
        `Movement_ActorUsesThreeDimensionalMotion` (`00264460`, the *either*).
      - **Where the shipped game sets them.** Neither verb appears in the 1,114 decompiled scripts.
        Both bits come from the unit definition: `BattleUnit_RefreshActorRuntimeFromDefinition`
        clears both (`00238EE4`, `00238EEF`), then sets float when the locomotion class from
        `002361B0` has bit 1 (`00238F01`–`00238F10`, with the float height from `00236210`, the
        slot-5 read [the FCP page](../../17-Presentation-Rendering/Model-And-Motion-Formats/fcp-character-parameter-block.md)
        describes) and fly when it has bit 3 (`00238F29`–`00238F38`). `002361B0` returns 1 (ground)
        for a unit whose `+0x698` record byte `+5` is 0, otherwise from the enemy definition page
        (`unit + 0xE68`) byte `+0x18`: bit `0x10` → 8 (fly), else bit `0x20` → 2 (float), else 1
        (ground), with bit `0x40` adding 4 (`002361CF`–`00236208`). So flying and floating are
        **authored per enemy definition**, and the *either* in `00264460` exists because both are
        "off the ground" for the movement selector while the y-offset and the airborne kind byte
        differ. Swimming is not one of the states.
      - The other bits of `+0x151` are not the 3-D pair: bit 2 is "moved this frame" (`002E5180`,
        `002E51BD` / `002E5278`), bit 3 is set at initialisation (`00265E06`), bit 4 is the ambient
        fetch flag (`0026AD40` ← verbs `setambient` / `fetchambient` / `resetambient`), bit 5 is
        written by `0026ACE0` (← `003B7B00`, `003B7F40`), bit 7 by `0026AF40` (← `002E28E0`, read by
        `00264EA0`).
- [x] ~~What controller `+0x14F` bit 0 and `+0x138` are. They gate the flat path; their own meaning is
      unread.~~ **`BV-2` ANSWERED 2026-09-12 (FABLE): bit 0 is "this actor is attached to another
      actor's bone", `+0x138` is the movement body.** `+0x138` was named 2026-09-11 on
      [the context census](../../04-Actor-Entity/Actor-Contexts/the-movement-and-secondary-context-censuses.md)
      (the `0x130`-byte movement-body pool entry). `+0x14F` is a flag byte with four fields, every
      writer reached through the script verb table:
      - **bit 0 — attached.** Set only by `002E26F0(parent, child, bone)` (`002E2777`), the body of
        script verb `00D9` **`attach`** (`0034A640`: `attach(parentOrdinal, bone)` attaches the
        script's own actor to the parent) and of the chocobo mount handler `00304060` (through the
        thunk `002E28C0`). It is cleared by the detach `002E6B10` (`002E6B98`) — verb `00DA`
        **`attachoff`** (`0034AD60`), the dismount `00304400` (thunk `002E28D0`) and a re-attach — and
        by the teardown `002E3AF0` (`002E3B80`). Attaching stores the parent's render-record index at
        the child's record `+0x3CE` and the bone at `+0x3CC` and sets record `+0x290` bit 19
        (`0042F310`); detaching sets bit 20 instead (`0042F250`) and re-commits the child's own
        position and facing from its movement state (`002E6B4B`–`002E6B82`). The render side resolves
        the pair in `RenderRecords_ProcessDirtyState` (`0042F880` / `0042F6C0`, the only readers of
        `+0x3CC` / `+0x3CE`). So the flat path is refused while attached because an attached actor's
        transform comes from its parent's bone, not from its own movement body: ~~every reader of bit 0~~
        ~~is a movement veto~~ ~~**six of its eight readers are movement vetoes**~~ **eight of its eleven readers refuse** — `00267260` (`00267286`) and the seven named next, while the attach guard `002E26F0` (`002E274A`, which detaches through `002E6B10`) and the two presentation readers below do not *(corrected 2026-10-02, OPUS: every `+0x14F` bit-0 test in the image — `0025B637`, `0025B76F`, `00267286`, `002E506A`, `002E5776`, `002E602C`, `002E634B`, `002EA816` jump past their work; `002E274A`, `003B7812`, `003B7934` do not)* — the two field-pass
        selectors, `Movement_UpdateActorFrame` (`002E506A`), `002E5750` (`002E5776`), `002E6000`
        (`002E602C`), `002E6330` (`002E634B`) and `002EA7F0` (`002EA816`). ~~and `003B7770` /
        `003B7880`, which fold it with actor `+0x09` bit 2 into one "not free-standing" flag
        (`003B7812`, `003B7934`).~~

        > **NARROWED 2026-09-16 (OPUS) on `FABLE-CONTRA-OPUS-NOT-EVERY-READER-OF-SECONDARY-0X14F-BIT-0-IS-A-MOVEMENT-VETO`.
        > `003B7770` / `003B7880` ARE PRESENTATION-VISIBILITY WRITERS, NOT MOVEMENT VETOES**, and the
        > fold has exactly one destination. Read from the image at `003B77FC`–`003B7839`:
        >
        > ```
        > 003B77FC  movzx ebx, byte [rax+9] / shr ebx,2 / and ebx,r12d   actor +0x09 bit 2
        > 003B7812  test byte [rax+0x14F], r12b / cmovne ebx, r12d       OR in +0x14F bit 0
        > 003B782A  and  byte [rax+0x10], 0xFD                          clear +0x10 bit 1
        > 003B7831  add  bl, bl
        > 003B7833  or   byte [rax+0x10], bl                            write +0x10 bit 1
        > 003B7839  call 002E8FD0                                       Actor_RefreshPresentationVisibility
        > ```
        >
        > **The only destination of the fold is `secondaryContext +0x10` bit 1**, and the very next
        > instruction hands the actor to the presentation-visibility refresh, which requires that bit
        > to show the actor at all. So these two read `+0x14F` bit 0 to decide whether an actor is
        > *drawn*, not whether it may *move*. **Calling that a "not free-standing flag" folded the
        > destination out of the sentence** — the fold is real and the conclusion drawn from it was
        > not.
        >
        > **The universal is narrowed rather than replaced, and deliberately not extended:** FABLE
        > states plainly that they did not read the other six, and OPUS has not re-read them here
        > either. Six readers are described correctly and two were wrong; whether the six are
        > *exhaustively* vetoes is a claim neither agent has now made. *(2026-09-30, OPUS owner read: since made - SD-192 ANSWERED, ~~every reader refuses~~ every movement-side reader refuses (the attach guard and two presentation readers excepted) (narrowed 2026-10-01, OPUS, on SWE2-AUDIT-SPEC's review [`auditspec-review-sd192-0930`](../../_index/candidates/auditspec-review-sd192-0930/REVIEW.md)); §7.)*
      - **bit 1 — fight stance.** `002E8540(actor, on)` (`002E854C`–`002E855B`), reached from verbs
        `01A7` `setfightmode` (`0034CB60`), `0483` / `02E0` `setforcefight` / `setforcerelax` through
        their tick `00357F00`, and `02E1` / `0484` `clearforcerelax` / `clearforcefight` (`00343290`);
        read back by `002E9B40` and, ORed with "controller `+0x12` ≥ 0x10", by `002EA2A0` /
        `002EABF0`. The shipped scripts call `setforcefight(-1)` 2,106 times and `setforcerelax(0|1)`
        2,174 times; `setfightmode` never.
      - **bit 2 — attach offsets present.** `0026A140(actor, slot, ptr)` (`0026A163`) is verb `01C8`
        **`attachinfo(slot, &vec3)`** (`00355D20`): it stores a pointer to a script-owned float triple
        in slot 0 / 1 / 2 = controller `+0x120` / `+0x128` / `+0x130` (position / rotation / scale
        offset). When set, `attach` uses `0042F3B0` to write the three offsets into the child's record
        (`00420CF0` / `00420F20` / `00420D50`, record `+0x120` / `+0x140` / `+0x160`) instead of the
        zero-offset `002EDAA0`; `0025D480` then clears the three pointers and the bit (`0025D4BD`),
        also at teardown. 197 `attachinfo` and 266 `attachoff` calls in the corpus; the `attach`
        verb itself does not appear in the 1,114 decompiled scripts, so shipped attachments come from
        the native mount and from scripts not in the corpus.
      - **bits 3–7 — standard-motion variation.** `002E8220(actor, v)` (`002E822C`–`002E8236`) is verb
        `01AA` **`stdmotionvariation`** (`0034D8D0`; also `BattleUnit_RefreshActorRuntimeFromDefinition`
        `00238E98`), mirrored to the render record's `+0x413` (`002E827D`, and again by `002E28E0` at
        `002E2A8C`); the corpus uses values 0, 1 and 2.
      The context census's "2 writers / 7 readers" for `+0x14F` counted only the actor-record-relative
      sites; the displacement sweep over `[controller + 0x14F]` finds 9 writers and 14 readers, all
      listed above.
- [x] ~~What actor `+0x08` bit 1 and `+0x09` bit 0 denote.~~ **`BV-3` ANSWERED 2026-09-12 (FABLE):
      `+0x08` bit 1 is "uses the map" (verb `usemapid`), `+0x09` bit 0 is "field movement enabled",
      set at record initialisation and cleared only when the party is captured for a summon.**
      - **`+0x08` bits 1–2** are one two-bit field with a single writer, `0026AD60(actor, on)`
        (`0026AD69`–`0026AD7E`): `on` → bit 1 set and bit 2 clear, `off` → bit 1 clear and bit 2 set.
        Its callers are verb `007B` **`usemapid(n)`** (`0034CC00`, then a re-read of the world position),
        verb `040D` **`partyusemapid(n)`** (`0033FD60`, per party member, then `002E5DF0`) and the battle
        console verb `301D` `btlAtelSetCtrlCharPosToOrigin` (`0050F560`). The corpus calls `usemapid`
        8,210 times (6,016 × `0`, 2,194 × `1`) and `partyusemapid` 459 times (448 × `1`). Bit 2 is also
        set by the teardown `002E3AF0` (`002E3BE4`) and cleared by the presentation builder `002E28E0`
        (`002E3009`), and `002E5180` measures the frame's displacement with `003A1920` instead of
        `Vector3_ComputeXZDistance` while it is set (`002E5290`). So the flat integrator runs only for
        actors a script (or the party verb) has put *on the map*; an actor with `usemapid(0)` is
        ~~neither flat nor 3-D by these selectors.~~ not flat, and every consumer takes its 3-D side: `002E4380` the spherical delta, and `002E45E0` / `002E5610` the 3-D distance, because `usemapid(0)` sets `+0x08` bit 2 *(corrected 2026-10-02, OPUS: `002E4528`–`002E452F` jump to the spherical path when `00267260` is 0; `002E475E`–`002E4773`, `002E4802`–`002E4817`, `002E56BC`–`002E56CC` OR `+0x08` bit 2 into the 3-D test; `0026AD60` sets bit 2 for `off`)*.
      - **`+0x09` bit 0** is set unconditionally by `00265FF0` (`00266010`–`00266018`, `(old & 0xE9) | 1`),
        the per-class initialiser that only `ActorStorage_InitializeRecord` calls (`0026681B`). It is
        cleared in two places: per party member by `003B72F0` (`003B736E`), the body of verb `0232`
        **`capturepartyforsummon`** (`00348130`; 13 corpus calls), which walks the party table at
        `02EBCA80` and hands each member to `00262F50`; and across the presentation rebuild in
        `002E28E0`, which clears it (`002E2C3C`), re-commits position and facing, then XOR-restores
        the saved bit (`002E2C71`–`002E2C7C`). `002E28E0`'s full 11-member exclusive subtree is bound on
        [the script-naming page](../../01-Script-VM-Native-Bridge/how-a-script-names-a-thing-in-the-world.md)
        §4c. Its only readers are the two field-pass selectors and
        `00267260` (`00267299`); the other three `test byte [+9], 1` sites in the image (`00224428`,
        `0022450D`, `00224ADA`) are audio vtable methods on a different structure. So bit 0 means
        "this actor's field movement is enabled", true from creation until a summon sequence
        captures the party. ~~What `00262F50` does with the table entry is not read.~~ **Read 2026-09-18 (FABLE):** `00262F50(actor, entry)` is `00262F90(actor, entry)` and, when that returns 1, `002ECCF0(actor, 1)`. `00262F90` links the two records: it requires the entry's manager slot live (`byte +0x15` indexes `02098E20 + i × 0x288`, bit 0), both records unlinked (`+0x18 == 0`) and distinct, then marks the entry `+0x18 = 1` with the actor's manager index at `+0x19` and id (`word +0`) at `+0x1A`, marks the actor `+0x18 = 2` with the entry's index and id, calls `002E4A40(actor)`, copies the entry's `+0xC0` and `+0xB8` handles into the actor, and runs `002681E0` on both (`00262FB2`..`00263038`). `002ECCF0(actor, 1)` then sets bit 7 of byte `+0x11` on the actor's `+0xC0` record when its dword is not -1. So the summon capture pairs each party member with its stand-in, hands the member's record handles to the stand-in and flags the stand-in's record; the entry itself only gains the link bytes `+0x18`..`+0x1B`.
- [x] ~~**What classes 0 and 2 are**, given that the canonical heading accessor returns 0 for them.
      An actor with no heading is a strong statement and it is unexplained.~~ **`BV-4` ANSWERED
      2026-09-12 (FABLE): class 0 is a script-only controller actor with no world presence, class 2
      is a trigger line; neither has a heading because neither has a movement context.** The class
      is the layout class of the record carver (M-1); the decompiled scripts declare every actor
      with its sequence — `actor NAME(seq)` — so the corpus says what each class is used for
      (24,820 declarations in 1,114 scripts):
      - **Class 0 = sequence 0 (8,797 declarations):** `__MJ_CTRL` (1,525), `Map_Director` (626),
        `setup` (621), `btl_trap_ctrl` (390), the vibration, director, event-effect and camera
        controllers. The region map gives it **no `+0xB8` and no `+0xC0`** (`00266AFB`–`00266B05`) —
        only the resource-slot arrays at `+0x120` / `+0x1E8` — and the per-class initialiser
        `00265FF0` does nothing class-specific for it. No heading, no position: the position
        accessor's `class == 1 || class == 3` excludes it too.
      - **Class 1 = sequences 1–2 (1,550):** `magic_switch`, `扉` (doors), `gil_magicwall`, `warp_up`,
        `切り替え` — placed objects that never move; its `+0xB8` is a `0x80`-byte block at `+0x120`
        (`00266B15`–`00266B2D`) whose `+0x38` is the heading the accessor returns.
      - **Class 2 = sequences 3–4 (18):** `制御ライン`, `進行管理ライン`, `NPC配置ライン`, `出口のライン`,
        `イベントドア` — **lines**. Its `+0xB8` is a `0x20`-byte block at `+0x120` (`00266B36`–`00266B4B`)
        that `00265FF0` initialises as two homogeneous points (`0026636A`–`00266384`) and verb `001C`
        **`setline(x1, y1, z1, x2, y2, z2)`** fills (`0035168F`–`003516AA`; the one class-2 test in the
        image). `lineenable` / `linedisable` (`00353D00` / `00354910`) are the generic actor enable
        `00269F00` (actor `+0x08` bit 0). **The consumer is the line pass `0025B250`**, called once per
        manager by `ActorManager_RunFieldRuntimePass` (`0025DEBE`): it walks the class-2 ordinal
        range (`+0x1DC` start, `+0x1D4` count) and, for each enabled line (`+0x14` bit 5, `+0x08`
        bit 0, `+0x1C` bit 6), `0025B2E0` tests each of the four party members (`0209A1F0`–`0209A210`)
        whose frame displacement is non-zero (`Vector3_ComputeSquaredXZDistance` of movement
        context `+0x00` / `+0x10`) for a **segment crossing** with the line (`003A17D0`, two side
        products), and on a crossing posts request kind 5 to the line actor with its `+0xD4`
        function id, or the bound payload's function-table entry 6 when `+0xD4` is `0xFFFF`
        (`ActorResource_SubmitRequestDescriptor`, `0025B3C3`), unless the record's `+0x18` is 1. A
        line has two endpoints and no heading.
      - **Class 3 = sequences 5–7 (14,455):** `PC`, `VAN`, `summon` (5); `treasure_`, `WARP_PC`, `NPC`,
        `hitactor` (6); `monster_`, `unique_monster_`, `trial_` (7) — the steerable actors, heading
        at `+0xA8`.
      So the accessor's `0` is not a strong statement: classes 0 and 2 have nothing to point it at.
- [x] ~~The identity of `movementState + 0xA8` relative to `+0xA0` and `+0xA4`.~~ **ANSWERED
      2026-09-07 in [`../heading-speed-to-position-delta.md`](../heading-speed-to-position-delta.md)**
      — `+0xA8` is the **facing angle**, wrapped towards `[-pi, pi]` by its single writer
      `FUN_002E5E10` (a single sign-biased pass, not a range guarantee — corrected 2026-09-11 on the
      facing page after EXP-072); `+0xA0`/`+0xA4` drive motion. **K-6** closed; the relationship between facing
      and motion continues as **K-11**.
- [x] Why `DAT_02B40534` has **nine** writers across the `003B6xxx`–`003B7xxx` subsystem while
      `DAT_02B40530` has **two**. They are read as a pair.
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (BV-5):* **the two flags have different
      masters.** Flag A is the engine's, and flag B belongs to the script verbs that take the party apart and put it back.
      - `02B40530` (A): the initialiser `003B6ED0` and the 7-byte setter `003B7E10`, whose callers are all engine code (§10:
        `0024B6F0`, `0024C6B0`, `0024C870`, `00262870`, `003B8670`).
      - `02B40534` (B), from a full RIP-relative census with eight store sites in eight functions (the register's "nine"
        was not reproduced): the initialiser (1), the setter `003B7E00` (argument; one caller, `00262870`), and six writers
        that are each the body of a script verb, named from [the verb table](../../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv):

        | writer | stores | verb |
        |---|---|---|
        | `003B6F30` (`003B6F37`) | 0 | `0x202` `disposepartywithoutcontrol` |
        | `003B7080` (`003B7089`) | 0 | `0x2A3` `duplicatepartyinfo_spattack` |
        | `003B72F0` (`003B7308`) | 0 (`xor ebx, ebx` just before) | `0x232` `capturepartyforsummon` |
        | `003B7E20` (`003B7E4C`) | 0 (same) | `0x191` `setpossummonspace` |
        | `003B7BB0` (`003B7BCB`) | 1 | `0x195` `resumeposbattletarget` |
        | `003B7C60` (`003B7CBE`) | 1 | `0x205` `changetosummonparty` (begin) and `0x2A4` `resumepartyinfo_spattack` |

        §10's "two store a register" are these two zero stores.
      **So B is dropped by the verbs that capture, dispose or duplicate the party for a summon or a special attack, and
      raised by the verbs that restore it.** The flat-movement gate is closed for the length of a scripted party swap.
      A, the engine's flag, is opened and closed on its own lifecycle. Which on-screen sequences use which verb pairs
      is the verbs' business and is not read here (registered below, 2026-09-30).
- [x] **Which scripted sequences use which party-swap verb pairs** — the dispose / duplicate / capture /
      summon-space verbs that drop flag B and the resume / change-to-summon-party verbs that raise it, and so
      when the flat-movement gate is closed in play. **SD-191** (SWE2-DATA, 2026-09-30). *(Answered 2026-09-30 (OPUS `f06af26c0`); register row SD-191, record [`sd191-party-swap-verbs-0930`](../../_index/candidates/sd191-party-swap-verbs-0930/README.md): the verbs occur only in the 26 summon scripts (the 13 Espers' entry and exit files) and the special-attack script `spc_z0000`, the nine language copies agreeing, so flag B is down only while a summon enters or leaves and during that sequence.)*
- [x] **Whether each of the six remaining `+0x14F` bit-0 readers refuses movement on it.** The two field-pass
      selectors and the four integrator-side readers are listed above as vetoes; the 2026-09-16 narrowing
      showed two other readers are presentation-visibility writers, and no one has since read the six for
      what they do with the bit. **SD-192** (SWE2-DATA, 2026-09-30). *(Answered 2026-09-30; register row SD-192, record [`sd192-attached-bit-readers-0930`](../../_index/candidates/sd192-attached-bit-readers-0930/README.md).)*

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Class is `actor[3] >> 5`; class 1 → `+0x38`, class 3 → `+0xA8`, else 0 | complete exact-current body of `00265200` (55 B) | 1 |
| It has 33 distinct callers at ~~33~~ 37 sites *(corrected 2026-10-02, OPUS: `retool.py callers 00265200`, 37 call sites in 33 functions; §10's re-count)* | edge census over a freshly regenerated graph at the GN checkpoint | 1 |
| The 3-D test is `(bit0 \| bit1)` of controller `+0x151` | complete exact-current body of `00264460` (37 B) | 1 |
| Called from exactly three functions at four sites | xref census against the current program | 1 |
| The flat test's four conditions | complete exact-current body of `00267260` (78 B) | 1 |
| The gate is `DAT_02B40530 != 0 && DAT_02B40534 != 0` | complete exact-current body of `003B7730` (27 B) | 1 |
| Both globals are zero in the shipped image | raw read of `02B40530`, 8 bytes, all zero | 1 |
| `003B6ED0` sets both to 1 while resetting actor-module state | complete body; xref census gives 2 writers for `0530` and ~~9 for `0534`~~ 8 store sites in 8 functions for `0534` *(corrected 2026-09-30, SWE2-DATA: a full rip-relative sweep, `_index/candidates/dd-data-5-0930/mm_checks.py` W1)* | 1 |
| BV-1: controller `+0x151` bit 0 is fly and bit 1 is float, each with one Boolean setter behind a script verb, and the unit definition sets them | §7 box 1: `0026A7F0` / `0026A7C0`, the refresh `00238EE4`–`00238F38`, locomotion class `002361B0` | 1 |
| BV-2: `+0x14F` bit 0 is "attached to another actor's bone", set by `002E26F0`, cleared by `002E6B10` and `002E3AF0`; `+0x138` is the movement body | §7 box 2, with the 2026-09-16 narrowing of the reader list | 1 |
| BV-3: actor `+0x08` bits 1–2 are the "uses the map" field (one writer `0026AD60`); `+0x09` bit 0 is "field movement enabled" (set by `00265FF0`, cleared by `003B72F0` and across `002E28E0`) | §7 box 3 | 1 |
| BV-4: class 0 is a script-only controller actor and class 2 a trigger line; neither has a movement context, so the heading accessor returns 0 | §7 box 4: the region map `00266AFB`–`00266B4B`, the line pass `0025B250`, 24,820 script declarations | 1 |
| BV-5: flag A (`02B40530`) is the engine's; flag B (`02B40534`) is dropped and raised by the party-swap script verbs | §7 box 5 and `_index/candidates/dd-data-5-0930/mm_checks.py` W1 (8 store sites; control C2 sees the gate `003B7730` read both) | 1 |

### K-6 narrowed, not closed — and a naming problem stated precisely *(superseded: the box above closes K-6 on 2026-09-12 and the register answers it 2026-09-07; this heading records the earlier state, reconciled 2026-09-18 by FABLE)*

**K-6** asks which of the GFZ's names for `movementState + 0xA0` (`flCurrent_heading`) and `+0xA4`
(`flDesired_heading`) is wrong, given that the delta computation consumes `+0xA0` as an **elevation**
and `+0xA4` as the **yaw**.

This document adds a third field to the problem. **The canonical heading accessor — the one 33 call
sites use to ask "which way is this actor facing?" — returns neither of them.** For class 3 it
returns `movementState + 0xA8`.

So there are **three angle fields and two names**, and the most-consulted one is unnamed:

```
+0xA0   consumed as pitch/elevation by the delta computation   GFZ: "flCurrent_heading"
+0xA4   consumed as yaw by the delta computation               GFZ: "flDesired_heading"
+0xA8   returned by the canonical accessor, 33 callers         GFZ: unnamed
```

**No renaming is proposed here.** What is established is that the existing pair of names cannot be
correct as a complete account of the field group, because the field the rest of the engine actually
reads is not among them. Settling it needs the writers of `+0xA8` read, which this block did not do.

**Superseded readings — a transposition in this document's first version, corrected within the hour.**

§3 originally read:

> `| 002E5380 | Movement_IntegratePositionAndMeasureDisplacement | 273 B | consumer; calls the 3-D selector |`

and §5's chain repeated the pairing. **The name and the behavioural claim were right and both point at
`002E5610`; the address and the body size were both `002E5380`'s.** The binary:

```
002E5380  Movement_PrepareCandidatePosition                 273 B   calls 00264460 : NO
002E5610  Movement_IntegratePositionAndMeasureDisplacement  314 B   calls 00264460 : YES  (site 002E56B7)
```

**How it happened:** `002E5380` was carried over from the K-4 open question, which names it alongside
`002E54A0`, while the caller list came from an xref census that gives call *sites* — `002E56B7`, which
falls inside `002E5610`. Two rows of source data were combined, so this is a transposition rather
than a mistyped label, and the fix is the address and the size, **not** the name.

**Why nothing else would have caught it.** The size travelled with the wrong address, so it was
internally consistent: a body-size check compares `002E5380` against 273 B and passes. Only the
**name/address pairing** was wrong, and `check_consistency.py` is the one instrument that compares
exactly that. This was its **first true positive**, found one merge after its false-positive rule was
fixed — reported by a peer session, and it is not this document's owner who found it.

## 10. Falsification pass 1 — 2026-09-03, session `repos-d2`

**Previously unattacked** (`passes: 0`). Program state: parent `2ed8affb…`, snapshot `46f02e26…`,
EXE `73461d08…`, project `proj_hd2` / `GFZ_HD2`, `CHECKPOINT VERIFIED` before any reading. Every
figure below is from a capstone census over all 38,161 ledger bodies.

### Overturned — the gate is manipulated at runtime, not only at bring-up

§2 offers a dichotomy — *"this is not a tuning switch. It is 'the actor system has been brought
up', and it reads as a guard against running the flat path during bootstrap or after a teardown."*
**Neither branch fits.** A writer census over every ledger body:

| global | writers | detail |
|---|---:|---|
| `02B40530` | **2** | `003B6ED0` stores `1`; **`003B7E10` is a 7-byte setter** — `mov [02B40530], ecx; ret` |
| `02B40534` | **8** | ~~`003B6ED0` and three others store `1`; **three store `0`**; two store a register~~ `003B6ED0`, `003B7BB0` and `003B7C60` store `1`; four store `0`, two of them through a zeroed register (`003B72F0`, `003B7E20`); `003B7E00` stores its argument *(corrected 2026-10-02, OPUS: stores at `003B6ED7`, `003B6F37`, `003B7089`, `003B7308`, `003B7BCB`, `003B7CBE`, `003B7E00`, `003B7E4C`; BV-5)* |

**`003B7E10` is a public setter and its callers pass constants both ways**, at six sites in five
functions:

```
0024C6B0  arg = 1        0024B6F0  arg = 0
0024C870  arg = 1        003B8670  arg = 0   (twice, 003B8F57 and 003B904C)
00262870  arg = 1
```

**Three sites set it and three clear it.** A value written `0` and `1` from five functions through a
dedicated setter is not a bring-up latch.

**And the clearing has a visible purpose.** `FUN_003B7E20` (284 B, reached through
`thunk_FUN_003b7e20` at `003482E0`) clears `02B40534` **at its head** and then walks the actor list:

```asm
003B7E4C  mov  dword ptr [rip -> 02B40534], ebx     ; ebx = 0, clear the gate
003B7E52  lea  ecx, [rbx + 1]      call 0025A5F0
          call 0036D840
          cmp  dword ptr [02EBCC60], ebx            ; actor count
          mov  ecx, dword ptr [02EBCBE0]
          call 003588B0                             ; ActorHandle_ResolveRegistryEntryByPackedId
          call 00265020                             ; Actor_GetWorldPosition
          ... per-actor loop over the list at 02EBCAC0, calling 003B7F40
```

**So the gate is dropped while the engine is mutating actor state in bulk**, and it is restored by a
*different* function — `003B7E20` never writes it back. That is a **consistency interlock over the
actor list**, held false for the duration of a bulk update, rather than a one-way "the system is up"
latch. The document's instinct that it guards against reading invalid controller state is right; the
lifetime is wrong.

**The practical consequence for §6:** the flat path can be disabled *mid-session*, not only before
bring-up and after teardown. A mod that assumes the gate is a startup latch will mis-predict
behaviour during whatever `003B7E20` serves.

### Survived

Every count and body figure in the document reproduces exactly.

| Claim | Result |
|---|---|
| `00265200` is 55 B with **33 distinct callers** | **SURVIVED, exact** — 33 callers over 37 sites |
| `00264460` is 37 B, called from **exactly three functions at four sites** | **SURVIVED, exact** — `002E4380`, `002E45E0`, `002E5610` |
| `00267260` is 78 B | **SURVIVED** — 3 callers, 3 sites |
| `003B7730` is 27 B and ANDs the two globals | **SURVIVED** |
| both globals are zero in the shipped image, past `.data`'s raw contents | **SURVIVED** — VA→offset returns `None` for both; raw `.data` ends at `01F7E400` |
| **`003B6ED0` is the one function that sets both** | **SURVIVED** — it is the only writer appearing in both censuses |
| the class discriminator and the two selectors' bit arithmetic | **SURVIVED** — bodies re-read |

**The uniqueness claim is the one worth flagging as survived**, because it is the kind that usually
breaks: `003B6ED0` really is the only function that writes both. The document was precise — it
claimed *"the one that sets **both**"*, not "the only writer", and that distinction is exactly what
saves it from the finding above.

### What was tried and failed to break it

- **Tried to break "33 distinct callers"** by counting sites as well: 37 sites, 33 functions. The
  document said *distinct callers* and meant it.
- **Tried to break the "exactly three functions" claim** on `00264460` — three, at four sites, and
  they are the three the document names by role.
- **Tried to make `003B6ED0` not unique.** Ten writes across the two globals, and it is still the
  only function in both sets.
- **No banned evidence.** No `.pdata`/`.xdata`/unwind/EH; no adjacency — `02B40530` and `02B40534`
  are treated as related because **one function writes both and one function reads both**, not
  because they are four bytes apart.

## 9. Related

- [`../heading-speed-to-position-delta.md`](../heading-speed-to-position-delta.md) — the two branches these predicates select between; its spherical formula is why the choice is visible in play
- [`../../04-Actor-Entity/battleunit-slot-pool-and-actor-class.md`](../../04-Actor-Entity/battleunit-slot-pool-and-actor-class.md) — the actor class byte in its own right
- [`../../17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md`](../../17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md) — Presentation can override the heading and speed these predicates route

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

- **CoreRuntimeScheduling — MECHANICAL and CLIENT.**
  - `0025B2E0`, `003B72F0`, `0042F6C0` and `0042F880` reach tables through `ImageAddress_ResolveRuntimePointer`.
  - `003B8670` asks the half-rate-mode test.
- **Gameplay — CLIENT.**
  - `Actor_GetWorldPosition` (`00265020`) is read by `BattleAction_FindApproachGeometryAroundTarget` and a 1,790-byte
    unnamed body.
  - The `clearforcerelax` / `clearforcefight` verb body `00343290` queries `WorldActor_QueryCombatStanceState`.
- **Rewards_Progression_Economy — CLIENT.** `BattleUnit_ProcessDefeatRewardsAndLoot` and
  `Loot_FindOverlappingPickupIndex` read unit positions through `Actor_GetWorldPosition`.

No other layer takes part in the 3-D / flat choice.
- **Audio - CLIENT and SERVICE (4 edges).** `00265020` is also called by bodies filed to audio: `00362850`; `003B8670` reaches bodies filed to audio: `002DF660`, `003B3EA0`, `003B99D0` - shared machinery across the layer boundary, no shared ownership.
- **Party - CLIENT (15 edges).** `00263F40`, `00265020` are also called by bodies filed to party: `00304180`, `00303CC0`, `00359150` - shared machinery across the layer boundary, no shared ownership.
- **Presentation - CLIENT (72 edges).** `0024C6B0`, `0024C870`, `00263F40` are also called by bodies filed to presentation: `003A7360`, `003B70B0`, `003A4290` - shared machinery across the layer boundary, no shared ownership.
- **Resource - SERVICE (4 edges).** `0042F6C0`, `0042F880` reach bodies filed to resource: `002ED570`, `004780B0` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (97 edges).** `0025A5F0`, `00262F50` are also called by bodies filed to script VM / native bridge: `003B7BB0`, `003B7C60`, `003410C0` - shared machinery across the layer boundary, no shared ownership.
- **Spawn_Encounter_Lifecycle - CLIENT (4 edges).** `00265020`, `00265200` are also called by bodies filed to spawn/encounter lifecycle: `00234AF0`, `00234DA0`, `002350C0` - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT (2 edges).** `00265020`, `00265200` are also called by bodies filed to UI: `003C5130` - shared machinery across the layer boundary, no shared ownership.
- **World - CLIENT (3 edges).** `002E5180`, `003B6ED0` are also called by bodies filed to World: `0025E400` (ActorManager), `002623A0` (ActorManager), `00266D10` (NativeSupport) - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - SERVICE (2 edges).** `002E28E0`, `002E4A40` reach bodies filed to WorldAreaField (world area): `00377C20`, `00377DB0` - shared machinery across the layer boundary, no shared ownership.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatFormula — CLIENT.** `FUN_00384f40`, owned by that layer, calls `00265020` on this page. That caller is a 681-byte per-unit scan: it resolves the owning battle unit for a stats pointer, caches it at `[02EBF188]`, takes the actor at `[unit + 0x10]` for its position, and then walks every unit the battle-unit count reports; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

## The `003482E0` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

`003482E0` is a five-byte thunk tail-jumping to `003B7E20` (`003482E0`),
the movement-mode scene-setup body: `ebx → 02B40534` (`003B7E4C`),
`0025A5F0` + `0036D840` (`003B7E55`/`003B7E5C`), `003588B0` on
`[02EBCBE0]` (`003B7E6F`), `00265020` (`003B7E8B`), then `003B7F40` on
`02EBCAC0` and on `[02EBCC68]` (`003B7EB8`/`003B7EDC`), `0017F5B0`
(`003B7EF3`), `002EB030` on `02EBCBC0` (`003B7F0F`).

| member | role | interior |
| --- | --- | --- |
| `003B7E20` | the setup body itself — the thunk's target; see the call list above | [`003B7E4C`](../../_index/ADDRESS-INDEX.md) |
| `002644C0` (31 B) | flag predicate — null-gated `byte[[rcx+0xC0] + 0x151] & 1` (`002644C5`–`002644D8`) | [`002644D1`](../../_index/ADDRESS-INDEX.md) |
| `003B7F40` (236 B) | per-object param set — `00263F40` → `00265020` → `00264670` chain with `float[rsp+0x20]`/`+0x24` params (`003B7F65`–`003B7F97`) | [`003B7F7F`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0025A5F0`, `0036D840`, `003588B0`,
`00265020`, `0017F5B0`, `002EB030`, `00263F40`, `00264670`.

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-how-the-engine-chooses-3d-or-flat-moveme-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00262870` | 57 B | calls, in order, a 5-byte thunk with `ecx = 0`, a 17-byte dword setter with `ecx = -1` (it stores `0xB4` for a non-positive argument), a 13-byte two-global setter with `ecx = 0` and `edx = 0`, a 38-byte routine, a 7-byte dword setter with `ecx = 1`, and tail-jumps a second 7-byte dword setter with `ecx = 1` | `00262876`, `0026287E`, `00262887`, `00262896`, `002628A4` |
| `0026ACE0` | 32 B | when qword `[rcx + 0xC0]` is non-null, replaces bit 5 of its byte `+0x151` with bit 0 of `dl`; otherwise returns without a store | `0026ACEA`, `0026ACEC`, `0026ACF6`, `0026ACF9` |
| `0026AD40` | 32 B | when qword `[rcx + 0xC0]` is non-null, replaces bit 4 of its byte `+0x151` with bit 0 of `dl`; otherwise returns without a store | `0026AD4A`, `0026AD4C`, `0026AD56`, `0026AD59` |
| `0026AF40` | 36 B | when qword `[rcx + 0xC0]` is non-null, sets bit 7 of its byte `+0x151` to 1 when `edx` is nonzero and to 0 otherwise; with a null pointer it returns without a store | `0026AF4A`, `0026AF4C`, `0026AF56`, `0026AF5C` |
| `002E9B40` | 26 B | returns bit 1 of byte `+0x14F` of qword `[rcx + 0xC0]`, or 0 when that pointer is null | `002E9B4A`, `002E9B4C`, `002E9B53`, `002E9B55` |
| `002EA2A0` | 120 B | returns at once for a null `rcx`, a null `[rcx + 0xC0]` (the sub) or a sub whose dword `+0` is -1; otherwise it takes bit 1 of the sub's byte `+0x14F` as a flag, forced to 1 when the sub's signed byte `+0x12` is at least `0x10`, and when the sub's word `+0` is not -1 and the `0x740`-byte record at that index under qword `022C6F28` has a nonzero dword `+0x284` it passes the record and the flag to a 392-byte routine; then it calls a 109-byte routine with byte `[rcx + 0x15]` and word `[rcx]` | `002EA2B9`, `002EA2CF`, `002EA2D3`, `002EA301`, `002EA30D` |
| `002EABF0` | 145 B | returns at once for a null `rcx`, a null `[rcx + 0xC0]` (the sub) or a sub whose dword `+0` is -1; otherwise it takes bit 1 of the sub's byte `+0x14F` as a flag, forced to 1 when the sub's signed byte `+0x12` is at least `0x10`, and when the sub's word `+0` is not -1 and the `0x740`-byte record at that index under qword `022C6F28` has a nonzero dword `+0x284` it sets that record's byte `+0x40B` to `(byte AND 0xFD) OR 1` for a nonzero flag or clears its bits 0 and 1 for a zero flag; every non-returning path tail-jumps a 109-byte routine with byte `[rcx + 0x15]` and word `[rcx]` | `002EAC22`, `002EAC42`, `002EAC56`, `002EAC6B`, `002EAC7B` |
| `003410C0` | 120 B | pops an index through `VMValueStack_PopInt32CoerceFloat32(r9)`, fills a four-entry stack array through an 11-byte collector called with `edx = 4` and, when the index is below (signed) the returned count, the array entry is non-null and a 50-byte check on `(rdx, entry)` returns nonzero, calls a 27-byte routine with the entry and `edx = 1`; any failed test returns without that call | `003410DF`, `003410F1`, `003410F6`, `0034110A`, `0034111B` |
| `00343290` | 141 B | resolves `rdx` through two 44-byte resolvers (the mode-2 one into `rsi`, the mode-1 one into `rbx`), calls the 26-byte bit-1-of-`+0x14F` getter on `rbx` (result unused), sets a flag to `WorldActor_QueryCombatStanceState(rsi) != 0`, calls a 65-byte flag setter on `(rbx, 0, 0)`, a 65-byte routine on `rbx` with `xmm1 = 0.0` and a 65-byte routine on `(rbx, flag, 1)`, then tail-jumps the 39-byte setter of bit 1 of byte `+0x14F` with `(rsi, flag)` | `003432C3`, `003432CF`, `003432D8`, `003432FF`, `00343318` |
| `0034CC00` | 82 B | pops a value through `VMValueStack_PopInt32CoerceFloat32(r9)`, passes `(rdx, value)` to a 34-byte setter of bits 1 and 2 of byte `[rdx + 8]`, reads the three position floats of `rdx` through `Actor_GetWorldPosition` into stack slots and calls `002E5DF0(rdx)` with them in `xmm1`, `xmm2` and `xmm3` | `0034CC0C`, `0034CC16`, `0034CC2D`, `0034CC41`, `0034CC47` |
| `00355D20` | 103 B | reads a global qword through an 8-byte getter, pops a value through `VMValueStack_PopInt32CoerceFloat32(r9)` and passes `(that qword, rcx, value)` to a 206-byte routine; then pops a second value and tail-jumps the 43-byte setter that stores its third argument (the routine's result) to qword `+0x120 + 8 * index` of `[rdx + 0xC0]` and ORs 4 into its byte `+0x14F`, with `rdx` and the second value as the actor and index | `00355D3D`, `00355D48`, `00355D56`, `00355D61`, `00355D82` |
| `00357F00` | 414 B | resolves `rdx` through two 44-byte resolvers (mode 2 then mode 1) and returns 0 when a 56-byte check on the first is zero; otherwise it steps the word state `[r8]`: 0 and 1 store 2 and run state 2, which stores 3 when a 208-byte test on the mode-1 actor is zero; 3 stores the actor's bit 1 of `+0x14F` to dword `+8` and stores 4, calling 65-byte routines and the 39-byte `+0x14F` bit-1 setter with flag 0 when byte `+2` is nonzero, else with flag 1; 4 stores 5 and runs state 5 when the 208-byte test is zero (with byte `+2` nonzero also when a 78-byte float getter is at least 16.0, storing 1 to byte `+3`); 5 calls a 108-byte routine with dword `+0xC` and 4.0 (0.0 when byte `+3` is zero) only when dword `+4` is nonzero, and stores 7; any other state changes nothing; it returns 1 unless the state is 7 | `00357F2E`, `00357F65`, `00357F9D`, `00358036`, `0035808C` |
| `0036D840` | 79 B | reads dwords `02EC0B24` and `02EC0B28`, sets bits 2 and 3 in both when `ecx` is nonzero or clears them when it is zero, passes the low word of the first to a 12-byte word setter and of the second to an 8-byte word setter, and stores both values back to `02EC0B24` and `02EC0B28` | `0036D85A`, `0036D862`, `0036D86B`, `0036D873`, `0036D878` |
| `003B70B0` | 122 B | walks the dword `02EBCBC0` (signed count, none when not positive) qword entries of `02EBCAC0`: each entry is resolved through a 44-byte resolver, and when the 16-byte getter of the resolved actor's `+0xC0` pointer returns non-null it replaces bit 1 of that block's byte `+0x10` with bit 0 of `ecx` and calls `Actor_RefreshPresentationVisibility` on the resolved actor | `003B70BE`, `003B70DA`, `003B70EF`, `003B70FC`, `003B7102` |
| `003B7B00` | 171 B | returns for a null `rcx`; otherwise resolves it through a 44-byte resolver into the actor and gets a record through a 38-byte lookup (returning when null), then calls on the actor `Actor_SetDesiredMovementHeading` with float `+0x34`, `Actor_SetFacingHeading_Variant1` with float `+0x24`, `Actor_SetDesiredMovementHeading` again with `+0x34`, `0026B0C0` with floats `+0`, `+4`, `+8`, `0026B720` with floats `+0x10`, `+0x14`, `+0x18`, `0026ACE0` with 0, a 26-byte setter with the signed byte `+0x64`, and `002E4A40` | `003B7B21`, `003B7B36`, `003B7B66`, `003B7B93`, `003B7B9B` |
| `0050F560` | 59 B | when a 117-byte lookup returns non-null, passes qword `+0x10` of the result with `edx = 0` to a 34-byte setter of bits 1 and 2 of its byte `+8`, then tail-jumps `0026B0C0` with that qword and 0.0 in `xmm1`, `xmm2` and `xmm3`; a null result returns without either call | `0050F566`, `0050F571`, `0050F579`, `0050F588`, `0050F590` |

## Homed bodies: functions reached only indirectly whose callees this page cites (OPUS, 2026-10-02, F homing)

*No page cited these functions and none of their callers is documented: they are reached by table or pointer dispatch or through undocumented callers. Each one calls something this page documents, which the sentence names. Each sentence states what the body does (access and representation, not purpose); the anchors are instructions inside it that do it. Drafted locally and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-how-the-engine-chooses-3d-or-flat-moveme-homing-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `003B79D0` | 94 B | calls `0017F5B0(1)` when dword `022BE970` is non-zero, then for each of the first dword `02EBCBC0` qwords of the array at `02EBCAC0` (the count re-read after each call) calls `002EB030(entry, 0x1049)` on the non-null ones | `003B79D6`, `003B79E4`, `003B7A0E`, `003B7A13`, `003B7A1F` |
| `003B7D80` | 128 B | for each of the first dword `02EBCC60` qwords of the array at `02EBCAC0` that is non-null, calls the entry's record lookup (the direct call at + 0x3C) and, when that returns a record, `0026B720(00263F40(entry), float +0x10, float +0x14, float +0x18 of the record)` | `003B7D88`, `003B7DB1`, `003B7DBC`, `003B7DD8`, `003B7DE3` |

## Homed frontier bodies called from this page's functions (FABLE, 2026-10-03, cloud-drafted)

*Functions no page cited until now. Each is entered directly from a function this page already cites (the site is given as caller + offset). Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's homing pack and re-read by FABLE against the certified image; verified by [`homing_applier.py`](../../_index/candidates/fable-home-how-the-engine-chooses-3d-or-flat-movem-1003/homing_applier.py): every site transfers to its function, the page cites the caller, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors |
|---|---|---|---|---|
| `001AD670` | 101 B | `0017F5B0` + 0x23 | stores `dl` to byte `+0x244` of `rcx`; then, for index `ebx` from 0 while `ebx` is below (signed) dword `+0x20` of the object returned by `001AD670` + 0xE (re-fetched each pass at + 0x50), computes a flag that is 1 when byte `+0x1C` of the result of `001AD670` + 0x20 is non-zero, calls `001AD670` + 0x3C with the object from `001AD670` + 0x2F, that flag and the index, and when this returns non-null passes the result to `001AD670` + 0x49; a count of 0 or less skips the loop | Interior anchor `001AD676`; Interior anchor `001AD686`; Interior anchor `001AD69B`; Interior anchor `001AD6AC`; Interior anchor `001AD6B9` |
| `00358420` | 38 B | `00262870` + 0x1C | calls `00358420` + 0xB with (`ecx` 0, `edx` 1), then the same callee at `00358420` + 0x15 with (`ecx` 1, `edx` 0), then stores byte 0 to `022C7F99` | Interior anchor `0035842B`; Interior anchor `00358435`; Interior anchor `0035843A` |
| `003631A0` | 13 B | `00262870` + 0x17 | stores `cl` to byte `022CBA91` and `edx` to dword `022CBA84` | Interior anchor `003631A6` |
| `00363B20` | 17 B | `00262870` + 0xE | stores `ecx` to dword `022CBB30` when `ecx` is greater than 0 (signed), else stores `0xB4` (180) | Interior anchor `00363B22`; Interior anchor `00363B27`; Interior anchor `00363B2A` |
| `003B7510` | 196 B | `003B6F30` + 0x23 | for each index below dword `02EBCAA0` (signed, re-read every pass; nothing when 0 or less) takes qword `02EBCA80` + 8*i and, when it and the record returned for it by `003B7510` + 0x3B are both non-null, calls `003B7510` + 0x56 with (object, record, record+4, record+8) and `003B7510` + 0x6A with (object, record+0x10, record+0x14, record+0x18), stores the byte from `003B7510` + 0x72 to record byte `+0x64`, and stores the floats from `003B7510` + 0x7D to `+0x34`, from `003B7510` + 0x8A to `+0x24` and from `003B7510` + 0x97 (the same callee as + 0x7D) to `+0x34` again | Interior anchor `003B751E`; Interior anchor `003B7556`; Interior anchor `003B758A`; Interior anchor `003B75A2`; Interior anchor `003B75AC` |
| `003DB150` | 94 B | `002E54A0` + 0xD7 | adds the three floats at `rcx`, `rcx+4`, `rcx+8` into the floats at `r8`, `r8+4`, `r8+8` in place; when `rdx` is non-null it then copies the three sums to dwords `+0x30`, `+0x34`, `+0x38` of `rdx`, copies the second sum also to dword `+0xAC`, and stores word `0xFFFF` to `+0x82` | Interior anchor `003DB159`; Interior anchor `003DB17A`; Interior anchor `003DB183`; Interior anchor `003DB19D`; Interior anchor `003DB1A6` |

## Homed bodies: functions reached only indirectly whose callees this page cites (FABLE, 2026-10-03, F homing)

*No page cited these functions and none of their callers is documented: they are reached by table or pointer dispatch or through undocumented callers. Each one calls something this page documents, which the sentence names. Each sentence states what the body does (access and representation, not purpose); the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's F homing pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-how-the-engine-chooses-3d-or-flat-moveme-homing-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `003DD8D0` | 162 B | returns without other work unless dword `02B581A4` + ((sign-extended `edx` << 4) + sign-extended `r8d`)*0x1c equals 4; when it does, passes the float result of the call at `003DD8D0+0x3e(rcx)` in `xmm1` to the call at `003DD8D0+0x49(rcx)`, sets bit `0x1` of byte `rcx+0xd`, stores the low byte of `r8d` at byte `rcx+0xf5`, calls `003DD8D0+0x6b(rcx, bit 7 of byte +0xd of 00263F40(rcx))`, and calls `003DD8D0+0x88` with (`rcx`, ((`edx` << 4) OR `r8d`) << 0x10 OR `r9d`, 0) and the fifth (stack) argument float in `xmm3` | Interior anchor `003DD905`; Interior anchor `003DD91E`; Interior anchor `003DD92C`; Interior anchor `003DD954`; Interior anchor `003DD958` |
