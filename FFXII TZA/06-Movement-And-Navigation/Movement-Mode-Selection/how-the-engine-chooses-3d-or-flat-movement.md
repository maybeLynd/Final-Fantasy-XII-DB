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
