---
system: The two actor contexts — access censuses for the movement context (record +0x120, 0x230) and the secondary context (record +0x350, 0x188)
category: 04-Actor-Entity
status: AUDITED — the secondary context's entryId (FS-2, the render record index the binder 002E3110 assigns) and the movement context's +0x10C..+0x21F (UQ-91, two steering sub-records behind the +0xF0 pointer) answered 2026-09-17
owner_layer: PrimaryOwner:ActorEntity — the censuses; the layouts are the store's to declare
evidence_tier: 1
level: L1
readiness: PARTIALLY UNDERSTOOD
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: hop_scan.py with container seeds — the two record-returning accessors ActorManager_GetRecordByOrdinal
    (00358940) and ActorHandle_ResolveRegistryEntryByPackedId (003588B0) return the CONTAINER (the actor record);
    a qword load at +0xB8 (or +0xC0) out of a tracked container yields the context, containers are followed
    through argument registers and learned at ret (24 further container-returning functions), three hops;
    controls 0026B6A0's float store at movement +0x38 and 0025B600's qword test at secondary +0x138 (both found).
    MERGED 2026-09-16 (OPUS-REQ-SWE2-STRUCT-MOVCTX-CENSUS-MERGE): movement-context-accesses.tsv is now the union
    of that route census and record_field_scan.py --chain 0xB8 (control 00265020 = +0x00/+0x04/+0x08 reproduced);
    merge_census.py found zero displacement disagreements across 230 shared sites. 1,028 rows, 122 distinct
    displacements; chain-only rows carry route `chain:0xB8`
corpus_validated: "the planter 00266AD0 read for both regions (00266B54–00266B6F)"
last_reviewed: 2026-09-12
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-context-censuses-pass-1
  last_pass_kind: authored
  crossref_clean: true
  reopened_count: 0
---

# The two actor contexts — access censuses

> Every actor record carries two regions its own census could not see: the **movement context**
> (0x230 bytes at `+0x120`, pointer at `+0xB8`) and the **secondary context** (0x188 bytes at
> `+0x350`, pointer at `+0xC0`). Code reaches them through the pointers, so a scan seeded on the
> record attributes their accesses nowhere. This page seeds on the pointers instead and publishes
> what it finds: ~~313 accesses at 58 offsets of the movement context, 302 at 40 of the secondary~~ 708 accesses at 101 offsets of the movement context, 309 at 42 of the secondary *(answered: the files on disk, measured; 2026-10-02, OPUS)*. It
> names nothing — the store owns the layouts — it locates them.

## 1. What the player sees

Nothing directly. Where an actor stands, which way it faces and how it steers live in the first
region; the second is read by the presentation-visibility and event code more than by anything
that moves.

## 2. Native mechanism

### 2.1 The regions are interior, and the pointers are planted once

`00266AD0` plants both pointers when a record is set up (`00266B54`–`00266B79`):

```
00266B54  lea  rax, [rdx+0x120]          ; the movement context, inside the record
00266B5B  mov  [rdx+0xB8], rax
00266B62  add  rax, 0x230
00266B68  mov  [rdx+0xC0], rax           ; the secondary context, at +0x350
00266B6F  lea  r8,  [rax+0x188]          ; a third region, at +0x4D8
00266B79  mov  [rdx+0xA0], r8
```

> **CORRECTED 2026-09-11.** The first publication called the arm at `00266B36`–`00266B52` "another
> branch that points the three slots outside the record". It does not: the planter is an
> eight-arm switch on the **sequence** (`rec[3] & 0x1F`, `00266AD3`–`00266AF9`), and every arm
> plants interior pointers — sequence 0 no contexts (`+0xB8` = `+0xC0` = NULL, `00266AFB`–
> `00266B0C`), sequences 1–2 a `0x80`-byte movement context and no secondary (`00266B15`–
> `00266B2D`), sequences 3–4 a `0x20`-byte movement context and no secondary (`00266B36`–
> `00266B4B`), sequences 5–7 the `0x230` movement context and the `0x188` secondary
> (`00266B54`–`00266B6F`). The `0x230` and `0x188` this page censuses are the sequence-5–7 shapes,
> and only kind-3 actors have them (the kind table at `01E0C328` pairs kind 3 with rows 5–7 —
> [the steering contract](../../06-Movement-And-Navigation/CONTRACT-facing-and-steering.md) §4).
> The record page's per-sequence table is the reference. Nothing below depended on the wrong
> sentence: the censuses follow the pointer fields.

> **What a census like this cannot see (2026-09-11, OPUS-NOTICE-CENSUSWRITES).** Seeds: container seeds through the record accessors; the region planter `00266AD0` and the record's index-derived initialisers are outside them.
> A scan seeded on *accessors* reaches *consumers*: a constructor that builds the record before
> any accessor can return it is reached only if it is seeded on its own. So the **reads** below are
> the well-covered side and the **writes** are under-covered wherever a constructor or an
> index-derived writer sits outside the seeds — do not rest an absence-of-writer claim on this
> TSV alone; pair it with a displacement scan of the candidate writers.

### 2.2 How the censuses were made

The scanner's container mode: the two record accessors that seeded the actor census
([the field map](../Actor-Storage-Record/the-actor-storage-record-field-map.md) §2.1) now seed a
*container*; a `mov r, qword [container+0xB8]` (or `+0xC0`) makes `r` the record under scan;
containers are followed into callees through argument registers and learned at `ret` (24 more
functions return one). Three hops. Rows: `movement-context-accesses.tsv`, `secondary-context-accesses.tsv`, beside this page.

**Dropped as branch artifacts:** a linear scan cannot see that `mov rax, [rax+0xB8]` on a sibling
branch re-loads the pointer from the *record* the register held on that path, not from the context
it held on the path just scanned. Every row of that exact shape — the destination register equal to
the base, a qword load at the pointer's own displacement — is removed: 4 from the movement census
(`0025B0D7` (`0025B070`); `0025B16C` (`0025B070`); `00264735` (`002646C0`); `002654A2` (`00265470`)), 1 from the secondary (`002EBCD4` (`002EBC90`)). Float loads and stores at those displacements are real and stay.

### 2.3 The movement context — 313 accesses, 62 functions, 58 offsets

Width is the most common operand size at the offset; "w / r" counts distinct functions.

| offset | width | w / r | writers | readers |
|---|---|---|---|---|
| `+0x000` | 4 | 2 / 20 | `Movement_IntegratePositionAndMeasureDisplacement` `002E5610` (`002E5729`); `0026AFE0` (`0026B04C`) | `00350DD0` (`00350E4C`); `003516E0` (`0035175C`); +18 more |
| `+0x004` | 4 | 2 / 14 | `Movement_IntegratePositionAndMeasureDisplacement` `002E5610` (`002E5730`); `0026AFE0` (`0026B051`) | `00350DD0` (`00350E65`); `00352580` (`003525F6`); +12 more |
| `+0x008` | 4 | 2 / 18 | `Movement_IntegratePositionAndMeasureDisplacement` `002E5610` (`002E573B`); `0026AFE0` (`0026B056`) | `00350DD0` (`00350E7A`); `003516E0` (`00351775`); +16 more |
| `+0x010` | 4 | 2 / 8 | `0026AFE0` (`0026B05B`); `002E4A10` (`002E4A23`) | `0025B250` (`0025B2B9`); `PartyFocus_ProcessActorControlPresentationState` `00358F90` (`00358FFF`); +6 more |
| `+0x014` | 4 | 2 / 2 | `0026AFE0` (`0026B061`); `002E4A10` (`002E4A29`) | `003A1920` (`003A1929`); `003A1C90` (`003A1CAB` +1) |
| `+0x018` | 4 | 2 / 4 | `0026AFE0` (`0026B066`); `002E4A10` (`002E4A2F`) | `003A1920` (`003A1937`); `0025BE50` (`0025BF32`); +2 more |
| `+0x020` | 4 | 1 / 0 | `0026AFE0` (`0026B06B`) |  |
| `+0x024` | 4 | 1 / 4 | `0026AFE0` (`0026B071`) | `0025BAD0` (`0025BC09`); `0025C230` (`0025C30C`); +2 more |
| `+0x028` | 4 | 1 / 0 | `0026AFE0` (`0026B076`) |  |
| `+0x030` | 4 | 1 / 3 | `Movement_SnapshotSteeringStartPosition` `0026AF10` (`0026AF24`) | `0025C830` (`0025CAB3` +1); `003DA730` (`003DA7C1`); +1 more |
| `+0x034` | 4 | 0 / 2 |  | `0025C830` (`0025CAC8`); `003DA730` (`003DA7CD`) |
| `+0x038` | 4 | 1 / 4 | `0026B6A0` (`0026B70D`) | `00265200` (`0026522D`); `0025C830` (`0025C950`); +2 more |
| `+0x03C` | 4 | 0 / 1 |  | `003DA5A0` (`003DA60F`) |
| `+0x040` | 4 | 0 / 6 |  | `0025BAD0` (`0025BBE0`); `0025C830` (`0025CC14` +1); +4 more |
| `+0x044` | 4 | 0 / 5 |  | `0025BAD0` (`0025BBEB`); `0025C830` (`0025CC29`); +3 more |
| `+0x048` | 4 | 1 / 6 | `0026B6A0` (`0026B712`) | `0025BAD0` (`0025BBF6`); `0025C830` (`0025CADD`); +4 more |
| `+0x04C` | 4 | 0 / 1 |  | `003DA5A0` (`003DA60F`) |
| `+0x050` | 0 | 0 / 4 |  | `Movement_UpdateSteeringTowardTarget` `002E45E0` (`002E4681` +3); `0025BE50` (`0025BF3C`); +2 more |
| `+0x054` | 4 | 1 / 3 | `0026B520` (`0026B58D`) | `003DA730` (`003DA7CD`); `FloatPair_CopyToOptionalOutputs` `003DA710` (`003DA71E`); +1 more |
| `+0x058` | 4 | 1 / 1 | `0026B520` (`0026B592`) | `003DA730` (`003DA73E`) |
| `+0x05C` | 1 | 0 / 3 |  | `003DA6A0` (`003DA6ED`); `0025BE50` (`0025BEC7`); +1 more |
| `+0x05D` | 1 | 1 / 2 | `0026AFE0` (`0026B048`) | `0025BE50` (`0025BE92`); `0025C830` (`0025C8DF` +5) |
| `+0x060` | 4 | 1 / 4 | `0025C830` (`0025C8B9` +1) | `0025BE50` (`0025BF09`); `0025C830` (`0025C8B3` +2); +2 more |
| `+0x064` | 4 | 0 / 1 |  | `003DA730` (`003DA7CD`) |
| `+0x068` | 4 | 0 / 5 |  | `0025BE50` (`0025BEEC`); `0025C830` (`0025C8A9`); +3 more |
| `+0x06C` | 4 | 0 / 3 |  | `0025BE50` (`0025BEDD`); `0025C830` (`0025C8A3`); +1 more |
| `+0x070` | 0 | 0 / 4 |  | `0025BAD0` (`0025BC5F`); `0025C230` (`0025C511`); +2 more |
| `+0x074` | 4 | 1 / 1 | `ActorSystem_ReleaseManagerRecords` `0025B070` (`0025B111` +1) | `003DA730` (`003DA7CD`) |
| `+0x078` | 4 | 0 / 1 |  | `003DA730` (`003DA73E`) |
| `+0x07C` | 4 | 0 / 1 |  | `003DA5A0` (`003DA60F`) |
| `+0x0A0` | 4 | 1 / 3 | `Movement_UpdateSteeringTowardTarget` `002E45E0` (`002E479F`) | `Movement_UpdateActorFrame` `002E5030` (`002E50DB`); `Movement_UpdateSteeringTowardTarget` `002E45E0` (`002E4715`); +1 more |
| `+0x0A4` | 4 | 2 / 3 | `Actor_SetDesiredMovementHeading` `0026A0D0` (`0026A128`); `Movement_UpdateSteeringTowardTarget` `002E45E0` (`002E4797`) | `Movement_UpdateActorFrame` `002E5030` (`002E50D0`); `Movement_UpdateSteeringTowardTarget` `002E45E0` (`002E46F2`); +1 more |
| `+0x0A8` | 4 | 0 / 3 |  | `00265200` (`0026521D`); `0026C120` (`0026C181` +1); +1 more |
| `+0x0AC` | 4 | 0 / 2 |  | `002E5FB0` (`002E5FBA`); `002651C0` (`002651DC`) |
| `+0x0B4` | 4 | 1 / 1 | `002EBE50` (`002EBE7F` +2) | `002EBE50` (`002EBEC8`) |
| `+0x0B8` | 4 | 2 / 1 | `002E5180` (`002E5264`); `Movement_UpdateActorFrame` `002E5030` (`002E5109`) | `002E5180` (`002E525C`) |
| `+0x0BC` | 4 | 0 / 1 |  | `0025BAD0` (`0025BD80`) |
| `+0x0C0` | 4 | 0 / 2 |  | `00263940` (`00263958`); `00268380` (`00268410`) |
| `+0x0C8` | 4 | 0 / 2 |  | `0025BAD0` (`0025BC22`); `0025C230` (`0025C332`) |
| `+0x0CC` | 4 | 0 / 2 |  | `0025BAD0` (`0025BC1A`); `0025C230` (`0025C326`) |
| `+0x0D0` | 4 | 4 / 2 | `Movement_SetRequestedSpeed` `0026D6F0` (`0026D750`); `0026D810` (`0026D847`); `Movement_ClearSteeringRequest` `002E55C0` (`002E55FD`); +1 more | `Movement_SetRequestedSpeed` `0026D6F0` (`0026D73D`); `Movement_ComputeDeltaFromHeadingSpeed` `002E4380` (`002E4419`) |
| `+0x0D4` | 4 | 1 / 0 | `002E5180` (`002E521F`) |  |
| `+0x0D8` | 4 | 1 / 1 | `0025D4F0` (`0025D52E`) | `0025D4F0` (`0025D50E`) |
| `+0x0DD` | 1 | 0 / 2 |  | `0025BAD0` (`0025BC01`); `0025C230` (`0025C31C`) |
| `+0x0E0` | 4 | 0 / 1 |  | `002640E0` (`002640F5`) |
| `+0x0EC` | 4 | 1 / 0 | `002E5180` (`002E52E2`) |  |
| `+0x0F0` | 8 | 0 / 21 |  | `002693D0` (`00269448` +3); `WorldActor_UpdateRuntimeAndScriptExecutionState` `0025DF00` (`0025DF50`); +19 more |
| `+0x0F8` | 4 | 2 / 1 | `Movement_UpdateSteeringTowardTarget` `002E45E0` (`002E48C0`); `Movement_ComputeDeltaFromHeadingSpeed` `002E4380` (`002E43E6` +1) | `Movement_ComputeDeltaFromHeadingSpeed` `002E4380` (`002E443E`) |
| `+0x0FC` | 4 | 0 / 1 |  | `002645D0` (`002645F1`) |
| `+0x100` | 4 | 1 / 1 | `0025C230` (`0025C34C` +1) | `0025C230` (`0025C311` +3) |
| `+0x104` | 1 | 0 / 1 |  | `00268380` (`00268488`) |
| `+0x105` | 1 | 0 / 1 |  | `00268380` (`0026848F`) |
| `+0x106` | 1 | 0 / 1 |  | `00268380` (`00268496`) |
| `+0x107` | 1 | 0 / 4 |  | `0025BAD0` (`0025BBD8`); `0025C230` (`0025C2C8`); +2 more |
| `+0x108` | 4 | 1 / 1 | `0025D690` (`0025D714`) | `0025D690` (`0025D6F0`) |
| `+0x220` | 4 | 1 / 1 | `ActorSystem_ReleaseManagerRecords` `0025B070` (`0025B102` +1) | `ActorSystem_ReleaseManagerRecords` `0025B070` (`0025B0CF` +1) |
| `+0x224` | 4 | 1 / 1 | `002EBE50` (`002EBE85` +2) | `002EBE50` (`002EBEEA`) |
| `+0x228` | 4 | 1 / 0 | `0025C230` (`0025C357` +1) |  |

<!-- untouched: +0xC..+0xF (4 B), +0x1C..+0x1F (4 B), +0x2C..+0x2F (4 B), +0x51..+0x53 (3 B), +0x5E..+0x5F (2 B), +0x71..+0x73 (3 B), +0x88..+0x8F (8 B), +0x98..+0x9F (8 B), +0xB0..+0xB3 (4 B), +0xC4..+0xC7 (4 B), +0xDC..+0xDC (1 B), +0xE4..+0xEB (8 B), +0x10C..+0x21F (276 B), +0x22C..+0x22F (4 B) -->

*Named in the store 2026-09-18 (SWE2-STRUCT-MOVCTX-STEERING-BAND): the `+0x50..+0x9F`
steering band decoded from the per-kind arms of `0026B2E0`/`0026BBC0` and the two
helpers they share — `003DA860(out_scaled, out_unscaled, x, y, sx, sy)` stores
`x*sx`,`y*sy` at the first pointer and the raw pair at the second; `003DA890`
copies a `{u64, u32, f32@+0xC}` block. Kind 3 (mask `0x60`): scaled command dir →
`+0x50`/`+0x54` (`steerCmdVecX/Y`, init 2π/0), its unscaled copy → `+0x80`/`+0x84`,
the turn/blend scalar `max(0.05, (x·scaleX + y·scaleZ)·0.5)` → `+0xFC`, plus
secondary dir scaled → `+0x70`/`+0x74` and unscaled → `+0x90`/`+0x94` (`0026BBC0`).
Gate bytes `+0xDE`/`+0xDF` (`dirCopy70Pending`/`dirCopy60Pending`, verb-set,
init `0x0101`) make the next `0026B2E0` pass block-copy `+0x50` into `+0x70` /
`+0x60`. Kind overlays proven by `002677F0`: the party-slot mask lives at
`+0x60` on kind 1 (`kind1SlotMask`) and at `+0x100`/`+0x228` on kind 3
(`kind3SlotMaskA/B`, selected by arg2) — so `+0x60` is also the kind-3 copy
target, and `+0x70` is kind 1's home of the blend scalar (`0026B3A8`).*
*Falsified in part 2026-09-18 (FABLE): the `+0x50` band is a **radius** band, not a steering command direction. Script verbs `0220 setradius` / `0221 setradius_221` (`0033F890` → `0026B2D0`, `0033FCD0`) tail-jump `0026B2E0` with the script's two floats; the bind `002E28E0` feeds it the FCP section-1 default pair (slots 67 / 68, or 79 / 80 by field bit 15 — UQ-221 on [the FCP page](../../17-Presentation-Rendering/Model-And-Motion-Formats/fcp-character-parameter-block.md)) that verbs `02B1` / `02B2 getdefaultradiusw` / `getdefaultradiusd` read back through `002E9660`; and the body shape `00268380` copies `+0x50` / `+0x54` into the movement body's radii `+0xF0` / `+0xF4` (`002683A8`). So `+0x80` / `+0x84` is the authored radius pair (width, depth), `+0x50` / `+0x54` that pair × the x / z scale `+0x20` / `+0x28`, and `+0xFC` the mean scaled radius — whose floor is `0.01` (`008F30E4`, `0026B357`), not 0.05. The store's `steerCmdVecX/Y` should become radius names; the rename is the store owner's (board notice `FABLE-NOTICE-MOVCTX-RADIUS-BAND`). The `2π` initial at `+0x50` is then a sentinel, not an angle.*
*Same pass, tail fields (SWE2-STRUCT-MOVCTX-TAIL-FIELDS): `+0x34` is the per-kind union of the
class-3 start-position snapshot Y (`0026AF10` copies `+0x00..+0x0F` over `+0x30..+0x3F`) and
kind 1's scaled direction Y (`003DA860` store via `0026B2E0` kind-1 arm). `+0x220` is the kind-3
`pendingVerbDword` — verb `003433A0` reads it via `002638C0`, consumes it in `0024CFF0`, then
`00269DD0` stores 0; kind 1 keeps the same slot at `+0x74` (`00269DFA`). `+0x224` is
`wrappedAngleK3` — `0026A950` wraps an angle into (−π, π] by `x ± π`, subtracting
`trunc(x/2π)·2π` and the adjustment, and stores it on the kind-`0x60` arm only.*

The three floats at `+0x00` / `+0x04` / `+0x08` are written by `Movement_IntegratePositionAndMeasureDisplacement`
(`002E5610`) and `0026AFE0` and read by twenty functions — the position. `+0xF0` is the hottest
offset (57 rows). The block `+0x10C`–`+0x21F` (276 bytes) is reached by nothing enumerated. *(2026-09-17, UQ-91: it is reached through `+0xF0`, which points at one of two `0x80`-byte sub-records at `+0x120` / `+0x1A0`; see §7.)*

> **Which context's `+0x138`, and a third writer (OPUS, 2026-09-15).** The paragraph below sits at
> the end of §2.3, but the field it names is the **secondary** context's — §2.4's table row at
> `+0x138`, writers `002E3D00` / `002E3AF0`, and §1's own note that `0025B600` tests *"secondary
> `+0x138`"*. §2.3's summary immediately above says its `+0x10C`–`+0x21F` block is reached by nothing
> enumerated, which would leave the naming with nothing to attach to. The image decides it: an
> image-wide displacement census (`disp_image_census.py 0x138`) shows `002E3500` reading this offset
> at `002E3515`, zeroing it at `002E352D` and **storing the new pointer at `002E3546`**, while
> `002E3BB5` and `002E3D2D` null it — the same two writers §2.4 already lists. One field, so the
> placement is a layout artefact and the name is installed on `SecondaryContext +0x138`.
>
> **That also makes the `2 / 20` count short by one.** The third writer is the creator's own store at
> `002E3546`, which a census keyed on a function list cannot see unless `002E3500` is in the list.
> The table is correct about what it enumerated; it is not a count of the writers that exist.

**`+0x138` named (2026-09-11).** The pointer is the actor's **movement body** — a `0x130`-byte entry
of the 128-entry pool at `02B4E4C0`, created by `002E3500` after the presentation set-up and released
by the two writers above ([the movement body page](../../06-Movement-And-Navigation/the-movement-body-pool-and-the-separation-pass.md)).
The context's `+0x148` is copied into the body as its weight and `+0x151` bits 0–1 into its flags;
`+0x14F` bit 0 is the veto the field pass tests beside it. *Named 2026-09-12 (BV-2):* the byte is
`{bit 0 attached-to-parent (`attach` / `attachoff`), bit 1 fight stance (`setforcefight` / `setforcerelax`),
bit 2 attach offsets present (`attachinfo`), bits 3–7 `stdmotionvariation`}` — see
[the movement-mode page](../../06-Movement-And-Navigation/Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md);
the table's 2 / 7 counts are actor-relative sites only (9 / 14 through the controller pointer).

### 2.4 The secondary context — 302 accesses, 89 functions, 40 offsets

| offset | width | w / r | writers | readers |
|---|---|---|---|---|
| `+0x000` | 2 | 1 / 49 | `002E35B0` (`002E3A0A` +1) — **the reset to `−1`** (a qword of ones covers `+0x00`–`+0x07`) | `002E4150` (`002E420A` +3); `002E6420` (`002E647B` +1); +47 more — **the actor's character-render record index** (`s16`, `−1` = none): every reader tests the dword against `−1`, then the word against `−1`, then indexes the 160 × `0x740`-byte array at `[022C6F28]` and requires the record's `+0x284` to be non-zero (`002E420A`–`002E423B`, `002ED2BF`–`002ED2E8`; [the party-presentation verbs](../../01-Script-VM-Native-Bridge/Party-Presentation-Verbs/how-a-script-changes-how-the-party-looks.md) §3, [heading and speed](../../06-Movement-And-Navigation/heading-speed-to-position-delta.md)). ~~The write that assigns a real index is not in this census (`FS-2`)~~ *(answered: the element binder `002E3110` — FS-2, 2026-09-17, §7; 2026-10-02, OPUS)* |
| `+0x004` | 4 | 0 / 2 |  | `002E6BD0` (`002E6C5E` +2); `002E35B0` (`002E39B5`) |
| `+0x008` | 8 | 1 / 4 | `002E35B0` (`002E3A2A`) — the release epilogue stores the resolved resource-chain entry here | `002EA6A0` (`002EA6BC`); `002E9A00` (`002E9A11`); +2 more — **`boundRecord`: the resolved resource-record pointer** (2026-09-18, SWE2-STRUCT-EL-FIELDS): the release path walks the resource chain (each entry `+0x14` dword == `boundResourceId`, `+0x08` = next link) and stores the found entry; readers prefer it over re-resolving `+0x04` — `002E6C7B` feeds it to `002E9C60` with `002E3F00(boundResourceId)` as the null fallback, and `002EC714` uses its `+0x1E` word as a `0x120`-stride table index and `+0x24` dword as a serial tag |
| `+0x010` | 1 | 2 / 3 | `002ECD50` (`002ECD6A` +1) — **bit 0 writer** (`and 0xFE; or arg&1`); `002E35B0` (`002E3A16`) — the release mask `and 0xF` (bits 4-7 transient, cleared on release) | `002E9FE0` (`002EA009`); `002E7E90` (`002E7EB6`); +1 more — **bit 0 = shown by script target group**: `hidetargetgroup` clears it and `showtargetgroup` sets it through `0026DC70` → `002ECD50`, and the presence predicate requires it (2026-09-12, [the stop registry](../../00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md) §7 `SM-2`) |
| `+0x011` | 1 | 3 / 5 | `002E4150` (`002E4293`); `002EB0D0` (`002EB125` +1); `002ECCF0` (`002ECD06` +1) | `002E4150` (`002E4285`); `002E9FE0` (`002EA005`); +3 more |
| `+0x012` | 1 | 2 / 1 | `002E6BD0` (`002E6CAC`); `002EC6B0` (`002EC6E3`) | `002E6BD0` (`002E6C52`) |
| `+0x013` | 1 | 0 / 1 |  | `002E8CE0` (`002E8CF6`) |
| `+0x014` | 4 | 1 / 1 | `002EB0D0` (`002EB16F` +1) | `002EB0D0` (`002EB160` +2) — **`pendingParamVec` X** (2026-09-18): see `+0x14`/`+0x18`/`+0x1C` note below |
| `+0x018` | 4 | 1 / 1 | `002EB0D0` (`002EB231`) — reset to `−1.0f` | `002EB0D0` (`002EB1B3`) — **pendingParamVec Y** |
| `+0x01C` | 4 | 1 / 1 | `002EB0D0` (`002EB238`) — reset to `−1.0f` | `002EB0D0` (`002EB1AE`) — **pendingParamVec Z** |
| `+0x020` | 4 | 1 / 0 | `002E35B0` (`002E3A33`) — **write-only slot**: the release-path zero is the only observed access; no consumer exists in the census |  |
| `+0x029` | 1 | 1 / 1 | `00269D60` (`00269D60` +1) | `00269D60` (`00269D69`) |
| `+0x02A` | 2 | 1 / 1 | `002EB0D0` (`002EB22A`) | `002EB0D0` (`002EB17D`) |
| `+0x030` | 0 | 0 / 3 |  | `Actor_RefreshPresentationVisibility` `002E8FD0` (`002E8FF9`); `002E4A40` (`002E4B18`); +1 more |
| `+0x060` | 0 | 0 / 2 |  | `Actor_RefreshPresentationVisibility` `002E8FD0` (`002E900A`); `002E35B0` (`002E3600`) |
| `+0x090` | 0 | 0 / 3 |  | `Actor_RefreshPresentationVisibility` `002E8FD0` (`002E901B`); `002E4A40` (`002E4B30` +2); +1 more |
| `+0x0C0` | 8 | 0 / 1 |  | `002E35B0` (`002E3630`) |
| `+0x120` | 8 | 1 / 0 | `0025D480` (`0025D493`) |  |
| `+0x128` | 8 | 1 / 0 | `0025D480` (`0025D4A1`) |  |
| `+0x130` | 8 | 1 / 0 | `0025D480` (`0025D4AF`) |  |
| `+0x138` | 8 | ~~2 / 20~~ 3 / 20 *(answered: see the note above — `002E3546` is the third writer; 2026-10-02, OPUS)* | `002E3D00` (`002E3D2D`); `002E3AF0` (`002E3BB5`) | `0025B600` (`0025B644` +1); `0025B740` (`0025B778` +1); +18 more |
| `+0x140` | 4 | 1 / 4 | `Actor_SetPresentationYOffsetPrimary` `00269E20` (`00269E2C`) | `0025BAD0` (`0025BBA0`); `0025C230` (`0025C29E`); +2 more |
| `+0x144` | 4 | 1 / 4 | `Actor_SetPresentationYOffsetSecondary` `00269E40` (`00269E4C`) | `0025BAD0` (`0025BBAC`); `0025C230` (`0025C2AA`); +2 more |
| `+0x14C` | 1 | 0 / 1 |  | `0050D860` (`0050D8C2`) — *2026-09-26: one writer, the setter (see the corrected note above); readers also include the high-model key getter* |
| `+0x14D` | 1 | 0 / 1 |  | `0050D780` (`0050D7E2`) — *2026-09-26: one writer, the same setter; readers also include the second key getter* |
| `+0x14E` | 1 | 0 / 1 |  | `002E6330` (`002E638C`) — *2026-09-26: one writer, the actor-record initialiser, which sets it to 1* |
| `+0x14F` | 1 | 2 / 7 | `002E3AF0` (`002E3B80`); `0025D480` (`0025D4BD`) | `0025B600` (`0025B637`); `0025B740` (`0025B76F`); +5 more |
| `+0x151` | 1 | 1 / 3 | `002E5180` (`002E51BD` +1) | `Actor_RefreshPresentationVisibility` `002E8FD0` (`002E916A`); `002E4A40` (`002E4ABD`); +1 more |
| `+0x152` | 1 | 0 / 1 |  | `002681E0` (`00268207`) |
| `+0x153` | 1 | 1 / 0 | `002681E0` (`002682B5`) |  |
| `+0x154` | 1 | 1 / 2 | `0026A770` (`0026A77C` +2) | `00264420` (`00264430`); `0026A770` (`0026A79F`) |
| `+0x158` | 4 | 1 / 1 | `002269A0` (`002269E1` +1) | `002269A0` (`002269B9` +1) — **stop set 5 (animation rate) live bitset**; `+0x15C`/`+0x160` are its pending set/clear words, folded by `002269A0` in the `00226640` pass ([the stop registry](../../00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md) §5/§5a) |
| `+0x15C` | 4 | 4 / 1 | `00225CD0` (`00225DDD`); `00225EB0` (`00225FBD`); `00226BE0` (`00226D5C` +6); +1 more | `002269A0` (`002269C3`) |
| `+0x160` | 4 | 4 / 1 | `00225CD0` (`00225DD0`); `00225EB0` (`00225FB0`); `00226BE0` (`00226D6A`); +1 more | `002269A0` (`002269E7`) |
| `+0x164` | 4 | 1 / 3 | `00226640` (`002267E9` +1) | `002E9FE0` (`002E9FFC`); `002E7E90` (`002E7EA9`); +1 more |
| `+0x168` | 4 | 4 / 1 | `00225CD0` (`00225DBE`); `00225EB0` (`00225F9E`); `00226640` (`002267EF`); +1 more | `00226640` (`002267DF`) |
| `+0x16C` | 4 | 4 / 1 | `00225CD0` (`00225DB1`); `00225EB0` (`00225F91`); `00226640` (`00226802`); +1 more | `00226640` (`002267F6`) |
| `+0x170` | 4 | 1 / 2 | `00226640` (`0022678F` +1) | `00226640` (`0022676D` +1); `00264DC0` (`00264DD3`) |
| `+0x174` | 4 | 4 / 1 | `00225CD0` (`00225D9F`); `00225EB0` (`00225F7F`); `00226640` (`00226788`); +1 more | `00226640` (`00226776`) |
| `+0x178` | 4 | 4 / 1 | `00225CD0` (`00225D92`); `00225EB0` (`00225F72`); `00226640` (`002267A1`); +1 more | `00226640` (`00226795`) |

<!-- untouched: +0x2..+0x3 (2 B), +0x24..+0x28 (5 B), +0x2C..+0x2F (4 B), +0x31..+0x5F (47 B), +0x61..+0x8F (47 B), +0x91..+0xBF (47 B), +0xC8..+0x11F (88 B), +0x148..+0x14B (4 B), +0x150..+0x150 (1 B), +0x155..+0x157 (3 B), +0x17C..+0x187 (12 B) -->

*Named in the store 2026-09-18 (SWE2-STRUCT-SECONDARY-STOPSET-FIELDS): the nine dwords
`+0x158`..`+0x178` are the three **(live, pendingSet, pendingClear) triplets** the stop
registry's `00226640`/`002269A0` fold passes operate on — `stopSet3Render*`
(`+0x170`/`+0x174`/`+0x178`), `stopSet4Presentation*` (`+0x164`/`+0x168`/`+0x16C`),
`stopSet5Animation*` (`+0x158`/`+0x15C`/`+0x160`), matching [the stop registry](../../00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md)
§5's live/pending column pairs. Also named: `+0x152` = `moveModeOverride` (0 = auto,
2 → mode 3, 3 → mode 5, else → 2, read by `002681E0` on kind-3 actors) and `+0x153` =
`resolvedMoveMode` (low byte of the mode word `002681E0` pushes to the movement body's
`+0x80`). `+0x14C`/`+0x14D`/`+0x14E` stay UNRESOLVED — debug-printf reads (`%d`,
`0050D860`/`0050D780`) and a single boolean gate (`002E6330` → `003DB0D0`) ~~with no
located writer~~.* *(Corrected 2026-09-26 (FABLE, Claude Opus 5.5): all three have a writer, and two are named.*
- *`+0x14C` is the model **local number** and `+0x14D` its **CLUT number**, going by the two debug verbs that
  print them (`debug_tty_modellocalno`, `debug_tty_modelclutno`). They are also the `b`/`c` keys of the
  high-model replace lookup, read through two getters.*
- *One setter stores both. Its only call, in the secondary-context initialiser, passes (1, 0), which are the
  getters' own defaults.*
- *`+0x14E` is set to 1 by the actor-record initialiser.*
- *An image-wide sweep of stores through a base loaded from `+0xC0` finds exactly these three. Control: [`hm1_model_selectors.py`](../../_index/candidates/hm1-model-selectors/hm1_model_selectors.py)
  (`HM-1`).)*

A word at `+0x00` read by 49 functions and written by one (`002E35B0`) — named 2026-09-11: **the
actor's character-render record index** (`s16`, `−1` = none), the handle every presentation reader
turns into a `0x740`-byte record at `[022C6F28]`; the one enumerated write is the reset to `−1`, so
the assigning writer reaches the word by a route this scan does not follow — byte flags at `+0x10`–`+0x13`,
and a block of qwords and dwords from `+0x138` — the region `Actor_RefreshPresentationVisibility`
(`002E8FD0`) and the `00226xxx` event functions work in. Three 47-byte spans (`+0x31`, `+0x61`,
`+0x91`) are untouched: the shape of three 48-byte sub-records whose first byte alone is read.

## 3. Key addresses

| address | name | role |
|---|---|---|
| `00266AD0` | region planter | writes the three pointers (`+0xB8`, `+0xC0`, `+0xA0`) |
| `00358940` | `ActorManager_GetRecordByOrdinal` | container seed |
| `003588B0` | `ActorHandle_ResolveRegistryEntryByPackedId` | container seed |
| `0026B6A0` | — | the movement control: `movss [ctx+0x38]`, `[ctx+0x48]` at `0026B70D` / `0026B712` |
| `0025B600` | — | the secondary control: `cmp qword [ctx+0x138], 0` at `0025B644` |
| `002ED2A0` | `CharacterRender_DispatchCombatRelationEvent` | research import (`XIIONLINE_NATIVE_CALL_ROADMAP_PLAN.md`, "unit-message post"; body re-read 2026-09-15): `003588B0` → `[rec+0xC0]` → the `+0x000` s16 index (`002ED2BF`–`002ED2E8`, the second example in the `+0x000` row) → `0x740` record at `[022C6F28]`, `+0x284` gate, then tail `003E6B50` with the event argument. The body confirms the guarded dispatch; which relation event is not read here |
| `002EBB80` | `Actor_SetPresentationVisibilityEnabled` | research import (`X55_NATIVE_REPLAY_CONTRACT.md`; body re-read 2026-09-15): record-kind gate `([rcx+3] & 0xE0) == 0x60`, then bit 3 of the secondary context's `+0x10` set from `dl`, then `jmp 002E8FD0` — i.e. writes the enable bit and immediately refreshes visibility |

## 4. Data structures and formulas

```
ActorStorageRecord (0x6E0)
  +0xA0  ptr -> +0x4D8   (third region, 0x208 to the record's end — not censused)
  +0xB8  ptr -> +0x120   MovementContext  (0x230)
  +0xC0  ptr -> +0x350   SecondaryContext (0x188)
```

SecondaryContext's first 192 bytes are a **4 × 0x30 element array** (proven 2026-09-16,
`OPUS-REQ-SWE2-STRUCT-SECONDARYCONTEXT-0X30-ELEMENTS`). `002E35B0`, `002E8FD0` and
`002E4A40` each `lea` the bases `ctx+0x30`/`+0x60`/`+0x90` and drive byte-identical access
sequences through all four: the `entryId` idiom (`cmp dword [el],-1` / `movzx word [el]`,
dword sentinel + low-16 payload), a `dword +4` read, a `qword +8` pointer store, flag-byte
ops at `+0x10`/`+0x11`, a `dword +0x20` zero, and the shared element mutator `00269D60`
(`+0x29`) called once per base. Element-relative fields replicate element 0's shape;
offsets `+0x12`/`+0x13`/`+0x14`/`+0x18`/`+0x1C`/`+0x2A` are shape-carried (no element-relative
access censused yet).

**Element fields resolved 2026-09-18 (SWE2-STRUCT-EL-FIELDS):**

- `+0x08` **`boundRecord`** (`NameBindingEntry*`) — a pointer to the resolved entry of the
  `0215FDA0` name-binding table (declared 2026-09-18 as `NameBindingEntry`), the record whose
  `+0x14` dword equals `boundResourceId` (`+0x04`). `002E35B0`'s release epilogue walks the chain
  (`rax = [rax+8]`, comparing `[rax+0x14]`) and stores the hit (`002E3A2A`). Readers prefer the
  pointer over re-resolving the id (`002E6C7B` → `002E9C60`, fallback `002E3F00(+0x04)`); `002EC714`
  further treats the entry's `+0x1E` word as an index into a `0x120`-stride table and `+0x24` as a
  serial tag. Written on every element by the generic release path; readers observed on element 0.
- `+0x10` **`elementFlags`** — a per-element flag byte. Bit 0 = shown-by-target-group (script verbs
  `hidetargetgroup`/`showtargetgroup` reach it via `0026DC70` → `002ECD50`, `and 0xFE; or dl&1`);
  the release epilogue keeps only the low nibble (`and 0xF`, `002E3A16`), so bits 4-7 are transient.
- `+0x14`/`+0x18`/`+0x1C` **`pendingParamVec`** — a three-float parameter vector with the `−1.0f`
  unset sentinel, **proven on element 0 only**: all nine `002EB0D0` callers pass
  `rdx = [rcx+0xC0]` (the array base). When `motionLoopPreset` (`+0x2A`, `u16`) is negative,
  `002EB0D0` forwards the triple to the bound `CharacterRenderRecord`'s `+0x3C0`/`+0x3C4`/`+0x3C8`
  via `00427880` and sets record `+0x294` bit `0x10000`; a `+0x14` of exactly `0.0` is coerced to
  `−1.0f` first (`002EB1B8`–`002EB210`) and all three are reset to `−1.0f` after apply
  (`002EB223`/`231`/`238`). When the preset is non-negative the vector is ignored and the preset
  word goes to record `+0x3C4` instead (`004278B0` flag `0x400000`, or `004272C0` flag `0x800000`
  which also stores `+0x14` to `+0x3C0`). Either way the pending bundle is consumed:
  `+0x14`/`+0x18`/`+0x1C` go to `−1.0f` and `motionLoopPreset` itself is reset to `0xFFFF`
  (`002EB220`–`002EB238`). Whether elements 1-5 carry the same vector is unproven —
  no caller was observed passing them.
- `+0x20` — a write-only dword: zeroed by the release epilogue (`002E3A33`), no reader found.

MovementContext `+0x048` is a **kind-discriminated overlay** (settled 2026-09-16,
`OPUS-REQ-SWE2-STRUCT-MOVCTX-48-OVERLAY`; discriminator `byte[actor+0x03] >> 5`, fixed at
record planting). On **kind 1** it is `wrappedAngleB`, member +8 of the `+0x40` sixteen-byte
angle block (the kind-1 init builds `+0x30`/`+0x40` through `003DA830`/`003DA860` and seeds
`+0x50` = 2π); `0026B6A0` writes it together with `+0x038` and `0026BC70` writes it alone.
On **kind 3** it is `positionOffsetZ`, third float of the `+0x40..+0x4C` vec4 that the
kind-3 init path zeroes (w = 1.0f) and the kind-3-gated setter `0026B170` RMWs. The offset
reading cannot reach kind 1 — `+0x107`.0 is latched only by kind-3-gated writers
(`0026B230`, `0026BA70`) and the accessors `00265390`/`002646C0` divert kind 1 before it.
Residual: `0026BC70` also stores the wrapped angle to `+0x48` on kind 3 — a genuine
in-kind alias between angle and offset-Z, recorded as such. Corroborating convention:
accessors `00263CC0`/`00265200` kind-dispatch the same logical angle to `+0x38` on kind 1
and `+0xA4`/`+0xA8` on kind 3 — the type's storage is kind-dispatched by design.

## 5. Call chain

Not a chain — two censuses. The routes column of each TSV records how every access was reached.

## 6. Modding notes

- **Read the contexts through the pointers, not the record offsets.** ~~The planter has a second~~
  ~~branch that points them elsewhere; code that assumes `record+0x120` will be wrong there.~~ *(answered: there is no second branch — see "CORRECTED 2026-09-11" in §2; `+0xB8` is `rec + 0x120` or NULL, `+0xC0` `rec + 0x350` or NULL, `00266AFB`–`00266B68`; 2026-10-02, OPUS)*
- **The position is the first three floats of the movement context** and twenty functions read it
  from there — a mover that writes the record's own position fields moves nothing.

## 7. What is not known

- [x] ~~**UQ-91.** **What the movement context's `+0x10C`–`+0x21F` holds** — 276 untouched bytes, a third of the~~
  region; reached by a pointer the scan does not follow, or unused. **FS-1.**
  ***ANSWERED 2026-09-17 (FABLE, under the live id FS-1 of the UQ-91 / FS-1 pair): the block is a header and two `0x80`-byte steering sub-records, and every consumer reaches them through the pointer at `+0xF0`, the census's hottest offset, which is why a displacement census on the context saw nothing there.** The planter `00266AD0` lays the movement context inline at record `+0x120` and the secondary context at `+0x350` (`00266B54`..`00266B68`), so the context is `0x230` bytes and the block is real storage. `00265FF0`, the Movement callee [the record page](../Actor-Storage-Record/the-record-behind-every-actor.md) lists as unread, initialises it with the context in `r14` from `[record + 0xB8]` (`00266042`): a header `+0x100` dword 0, `+0x104` word `0x3225`, `+0x106` byte `0x25`, `+0x107` kept, `+0x108` and `+0x110` qwords 0 (`00266053`..`0026609B`, `00266352`..`00266359`), then two sub-records of one layout at `+0x120` and `+0x1A0` (`0026610C`..`002661F2`, `002664AC`..`002664D9`): within each, `+0x20` qword 0, `+0x28` word 0, `+0x2C` qword 0, `+0x3C` qword 0, `+0x4C` dword 0, `+0x50`, `+0x54` and `+0x5C` the float π (`0x40490FDB`), `+0x58` and `+0x6C` π/20 (`0x3E20D97C`, nine degrees), `+0x62` bit 7 cleared, `+0x64` and `+0x65` bytes 0, `+0x70` and `+0x74` dwords 0, `+0x7C` dword 0. It then stores the first sub-record's address at `+0xF0` (`002660D7`, `002660F4`) and zeroes the index byte `+0xDC` (`002660ED`). `00269F90` re-points `+0xF0` to `+0x120 + (+0xDC) x 0x80` whenever `+0xDC` is 0 or 1 (`00269F90`..`00269FAC`): `+0xDC` selects the active sub-record and `+0xF0` addresses it; `0026C8C0` points both `+0xF0` and `+0xF8` at another block for its kind (`0026CC10`..`0026CC17`). A scan seeded on `[x + 0xF0]` loads finds 45 functions in the movement module reading the pointee at 27 offsets between `+0` and `+0x7C`: `002690D0` ten of them, `002E45E0` nine, `0026C120` seven, `0026C330` three, the rest one or two each (`00263230`, `002636F0`, `00263720`, `00263D00`, `00264E10`, `002652A0`, `002654E0`, `00265510`, `00265530`, `002655D0`, `00265600`, `00265630`, `00265660`, `00265830`, `002693D0`, `00269C30`, `0026A170`, `0026A1A0`, `0026A640`, `0026A870`, `0026A8E0`, `0026AAD0`, `0026ADF0`, `0026AE30`, `0026AE90`, `0026B450`, `0026C070`, `0026C090`, `0026C290`, `0026C300`, `0026D6F0`, `0026D810`, `002E4BC0`, `002E4BF0`, `002E5030`, `002E55C0`, `002E5B60`, `002E5B90`, `002E60C0`, `002E64E0`). What each field of the sub-record means is the STRUCT layer's to name; a request with this reader list is filed (`FABLE-REQ-SWE2-STRUCT-MOVCTX-STEER-SUBRECORD`). *Corrected 2026-09-17: the STRUCT layer had already declared it as `SteeringRecord` (`0x80`, two inline slots, selector `+0xDC`, cursor `+0xF0`, `turn_step +0x58`, `turn_limit +0x5C`); its 2026-09-18 pass verified the constants above against the bytes and swept the 44 readers onto declared fields, closing the request.* π and π/20 as the initial values read as angle limits and a per-frame step, a reading, not a claim. Static, planter, initialiser and selector read; pointer-seeded scan.*
- [x] ~~**FS-2.** **What the secondary context's word `+0x00` is** — 49 readers, one writer (`002E35B0`,~~
  `002E3A0A`). The "three 48-byte sub-records" guess is corrected: `0x000–0x0BF` is **four**
  `0x30`-byte elements of one shape (proven 2026-09-16 — see §4); `+0x00` is each element's
  `entryId`. The entryId's *meaning* remains open. **FS-2.**
  ***ANSWERED 2026-09-17 (FABLE): the writer that assigns a real index is the element binder `002E3110`, and the index is the character-render record the binder allocates for the element's bound resource; the three spans are elements 1..3 of the four-element array, proven 2026-09-16.** `002E3110(actor, k, ..., entry)` takes the secondary context from `[actor + 0xC0]` (`002E312A`), selects element `k` (`002E32D0`..`002E32D6`, `+0x90` for `k = 4`), and after `002E8FD0` calls [the render-record allocator](../../17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md) `0042FB80([entry + 0x10], 1, 0)` (`002E3353`..`002E335B`), which names the record `cn\plan...`, resolves it in the `0x740`-stride array at `[022C6F28]` (`0042FBFC`) and returns its word `+0` sign-extended, or `-1` (`0042FC7A`). The binder stores that return, sign-extended, as the element's dword `+0` (`0042FB80`'s `eax`, `cwde`, `002E336B`..`002E336C`), the entry's `boundId +0x14` as `+4` (`002E336E`..`002E3372`) and the entry pointer as `+8` (`002E3375`). So the word is the index of the render record drawn for that element, `-1` when none, which is exactly what the 49 readers test before touching the record's `+0x284`. The release `002E35B0` and the reset `002E3A60` write the `-1` sentinel (`002E3A0A`..`002E3A20`, `002E3AAA`..`002E3ABF`), and `002E3110` itself resets before binding (`002E330E`..`002E331E`). The equipment page places the binder's callers as the weapon (`k = 0`), off-hand (`k = 1`) and part-8 pair (`k = 3`) appliers. Static, binder and allocator read.*
- [x] ~~**What the third region at `+0xA0` holds** — planted per sequence (`rec+0x120` / `+0x1A0` /
  `+0x140` / `+0x4D8`), with `+0xA8` = `+0xA0` + `0xC8` or `0xA0` by the kind table's `sub` byte
  (`00266B83`–`00266B9B`); its contents are unread.~~ **FS-3 ANSWERED 2026-09-12 (FABLE), by
  reconciliation with [the record page](../Actor-Storage-Record/the-record-behind-every-actor.md)
  §12–§13 (2026-09-10), which read it after this row was filed.** The `+0xA0` pointer is
  `slotsA0`: a pool of **`slotCountA0` (`+0x89`: 10, or 8 when `sub == 1`) `0x14`-byte
  `ActorResourceEntry` records** — next/prev indices at `+0`/`+1`, a dword seeded `0x80000000` at
  `+4`, a word at `+0x10` — that `003DB580` links into a free list and the `ActorResource_*` family
  (`ActorResource_GetEntryByOrdinal` `003DB550`, `ActorResource_InsertEntryFromDescriptor`
  `003DB7A0`, `ActorResource_FindActiveEntryByIdOrClass` `003DBF60`) moves by index between the
  free list (`+0x60`), the detached list (`+0x61`) and the per-channel lists (`+0x94[ch]` /
  `+0x8C[ch]`, active mask `+0x06`); these are the script-request entries `FZ-26` filed (kind, mode,
  wait slot, index, return offset). `+0xA8` is `slotsA8`: **one `0x28`-byte state block per
  channel**, `slotCountA8` (`+0x88`: 8, or 6) of them, exactly the record's tail on all eight
  sequences; `+0x11` is the channel index `WorldActor_UpdateRuntimeAndScriptExecutionState` uses
  at `0025DFB6`. The `0xC8` / `0xA0` step between the two pointers is `10 × 0x14` / `8 × 0x14`. So
  the third region is not a third *context*: it is the actor's resource-request bookkeeping, and
  its consumers are the actor pass, not the movement or secondary families censused here.

## 8. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| the regions sit at `+0x120` / `+0x350`, sizes 0x230 / 0x188 | the planter `00266B54`–`00266B6F` | 1 | PROVEN |
| the accesses listed | `movement-context-accesses.tsv`, `secondary-context-accesses.tsv`; both controls found | 1 | PROVEN |
| the dropped rows are artifacts | `0025B0C8` / `0025B0D7`: two branches, each loading `[rax+0xB8]` from the record | 1 | PROVEN |

## 9. Related

- [`../Actor-Storage-Record/the-record-behind-every-actor.md`](../Actor-Storage-Record/the-record-behind-every-actor.md) — the record; its `+0xB8` / `+0xC0` rows.
- [`../Actor-Storage-Record/the-actor-storage-record-field-map.md`](../Actor-Storage-Record/the-actor-storage-record-field-map.md) — the record's own census and the seeds reused here.

## Falsification pass 1 — 2026-09-13 (OPUS)

| claim | measured |
|---|---|
| the movement census: **313** accesses, **62** functions, **58** offsets | `movement-context-accesses.tsv`: **313 rows, 62 distinct functions, 58 distinct displacements** — SUPERSEDED 2026-09-16 by the merged census (**1,028 rows, 122 displacements**); the pass-1 measurement stands for the route-only census it measured |
| the secondary census: **302**, **89**, **40** | `secondary-context-accesses.tsv`: **302, 89, 40** |
| the planter's four arms at `00266AFB` / `00266B15` / `00266B36` / `00266B54` | every instruction as § renders it |
| the switch is on `rec[3] & 0x1F`, eight arms | `movzx ecx, byte [rcx+3]` / `and eax, 0x1f` / `cmp eax, 7` / `ja` — **bounded to 0–7** |
| the secondary sits at `+0x350` and the third region at `+0x4D8` | `0x120 + 0x230 = 0x350` and `0x350 + 0x188 = 0x4D8` |
| the kind table at `01E0C328` pairs kind 3 with rows 5–7 | exact — and the full mapping is below |

### Every censused access lands inside its region

Neither census overflows the size the planter allocates:

| region | size | furthest access ends at | unused tail |
|---|---:|---:|---:|
| movement | `0x230` | **`0x22A`** (`0x228`, a dword, in `0025C230`) | 6 bytes |
| secondary | `0x188` | **`0x17A`** (`0x178`, a dword, in `00225CD0`) | 14 bytes |

The region sizes and the censuses are independent measurements — one from the planter's `add rax,
0x230`, the other from 615 access sites — and they agree, with a small tail untouched in each. That
is the check that the two really are the regions these accesses belong to.

### The per-sequence grouping is not an inference — it *is* the jump table

§ groups the sequences 0 · 1–2 · 3–4 · 5–7. The eight-entry table at `00266BA4` groups them the same
way because it holds only four distinct targets:

| sequence | arm target | shape |
|---:|---|---|
| 0 | `00266AFB` | no contexts |
| 1, 2 | `00266B15` | `0x80` movement, no secondary |
| 3, 4 | `00266B36` | `0x20` movement, no secondary |
| 5, 6, 7 | `00266B54` | `0x230` movement **and** `0x188` secondary |

### The four shapes are the four actor kinds, one for one

§ says *"only kind-3 actors have them (the kind table at `01E0C328` pairs kind 3 with rows 5–7)"*.
The table's byte `+0`, read across all eight rows, gives the whole correspondence:

| sequence | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| kind (`01E0C328[seq].b0`) | 0 | 1 | 1 | 2 | 2 | **3** | **3** | **3** |

**The kind boundaries and the arm boundaries are the same boundaries.** So the context shape is a
function of the actor *kind*, not of the sequence as such: kind 0 gets nothing, kind 1 a `0x80`
movement context, kind 2 a `0x20` one, kind 3 the `0x230` + `0x188` pair this page censuses. §'s
statement is the last column of that table; the first three columns are the rest of it.

### Sequence 0 has no contexts, but it is not left without a pointer

§ reads sequence 0 as *"no contexts (`+0xB8` = `+0xC0` = NULL)"*, which is exactly right about those
two. **`+0xA0` is still planted.** All four arms converge at `00266B76`, and `00266B79 mov [rdx+0xa0],
r8` runs on every path — for sequence 0 with `r8 = rdx + 0x120` (`00266B0C`), the address where a
movement context would have started.

So a reconstruction that treats `+0xA0` as "present only when there are contexts" would be wrong for
sequence 0: **the third-region pointer is unconditional, and for kind 0 it points at bytes no
movement context occupies.** What lives there is not established here.

**Not claimed:** nothing was executed or observed live. §2.1's own warning stands untouched — these
censuses are seeded on accessors, so the **writes** remain under-covered wherever a constructor sits
outside the seeds, and nothing here turns an absent writer into an absence of writers. §§2.3–2.4's
per-offset readings and §§5–7 were not re-derived.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CoreRuntimeScheduling — CLIENT and SERVICE.** A cited function is called by `MainLoop_UpdateAndRenderFrame`, and cited functions call two small core helpers (27 and 61 bytes).
- **Rewards_Progression_Economy — CLIENT.** `00265020` on this page — the `byte[rcx+3] >> 5` field reader
  that returns `[rcx+0xB8]` when the decoded value is 1 or 2 (`00265025`–`0026507D`) — is called by the
  Rewards bodies `002FB150` and `00312280` (`BattleUnit_ProcessDefeatRewardsAndLoot`): the defeat-rewards
  path consults this census's packed actor field. (edges: `edges.tsv`, two of them)

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatFormula — CLIENT.** `FUN_00384f40`, owned by that layer, calls `003A1920` on this page. That caller is a 681-byte per-unit scan: it resolves the owning battle unit for a stats pointer, caches it at `[02EBF188]`, takes the actor at `[unit + 0x10]` for its position, and then walks every unit the battle-unit count reports; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Gameplay — SERVICE.** `00264420` on this page calls `WorldActor_QueryCombatStanceState`, owned by that layer. What it reaches is a 96-byte query that takes the actor from `0031B760`, needs bit 4 of `byte[actor]`, and tests the `+0x698` block's `+0x3C` OR `+0x64` pair; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Spawn_Encounter_Lifecycle — CLIENT.** `Spawn_TrySelectCandidatePosition`, owned by that layer, calls `00265200` on this page. That caller is the spawn candidate-position search, working in a `0x100`-byte frame with three saved SSE registers; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — CLIENT.** `FUN_0035dcc0`, owned by that layer, calls `00265470` on this page. That caller is a 492-byte routine in a `0x70`-byte frame with a stack cookie, seeded with two 1.0 scales and a `-1` index; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatAction — MECHANICAL (SWE2-CONTRACT 2026-09-15, 8 edges).** All caller fan-in through the page's cited
helpers: `00313DB0` shares `00225CD0`/`00226BE0`, `Battle_ProcessActionTarget` `00307300` shares
`00265200`/`0026A0D0`, and `00306010`/`BattleAction_ResolveSpecialSequenceTargets`/
`BattleAction_EvaluateTargetPreviews` share `0031B760`; `BattleUnit_TryTriggerNearbyAuthoredFieldAction`
shares `003A1920`. The census helpers are consulted by the action layer; no census semantics cross.

**CombatAI — MECHANICAL (SWE2-CONTRACT 2026-09-15, 6 edges).** Same shape — the AI layer's bodies neighbour the
census accessors this page lists; no AI relationship.

**Input — MECHANICAL (SWE2-CONTRACT 2026-09-15, 7 edges).** `00225CD0`/`00225EB0` call the input helpers
`00182D40`/`00182D60`/`00182DA0` (6 edges), and `Input.ActorControlMaskPropagationRuntime`
`00226BE0` shares `00358940`. The context census reads the same control-mask helpers the input
layer writes — cadence-level adjacency.

**Audio — SERVICE (SWE2-CONTRACT 2026-09-15, 1 edge).** `00313DB0` calls the Audio helper `002DEE70`. Small, real.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page. The page cites its functions as the accessors a census found touching the two actor contexts; almost every edge below is another layer calling one of those accessors, or an accessor defaulting to the current focus actor.*

**Party — SERVICE and CLIENT (42 edges).** Twelve census accessors, among them `00226BE0`, `0025B600`, `00263230`, `002677F0`, `Movement_SetRequestedSpeed` `0026D6F0`, `Movement_UpdateSteeringTowardTarget` `002E45E0` and `ActorManager_BindLoadedDefinitionPayload` `0026C8C0`, call `PartyFocus_GetCurrentPackedActorHandle` `003590D0`; `00226BE0` also calls `PartyRoster_GetActorBySlot` `00263750`, `0025C830` calls `PartyFocus_CommitPendingPackedActorHandle_Thunk` `00358BB0`, and the bind calls `PartyControl_SetMovementSuppressionBit` `00359200`; in the other direction `PartyControl_ApplyAnalogLocomotionToActor` `00358CB0` calls `00265200`, `00265830`, `Actor_SetDesiredMovementHeading` `0026A0D0`, `0026D810`, `003A1AD0` and `003A1D30`, `PartyFocus_ProcessActorControlPresentationState` `00358F90` (itself called by `PartyFocus_UpdatePrimarySecondaryActorProcessing` `00358EE0`) calls `002640E0` and `003A1920`, `PartyFocus_TryGetCurrentActorWorldPosition` `00359150` calls `Actor_GetWorldPosition` `00265020`, `002E9FE0` and `002EA6A0`, `PartyRoster_AssignActorToSlot` `00269C70` calls `002681E0`, the party-filed `00303CC0`, `00304180` and `00312EE0` call `00265020`, `00265200` and `0026A0D0`, a 63-byte party-filed body calls `ActorWork_GetBattleUnit` `0031B760`, and `003590D0` is called by `PartyRoster_GetActorBySlotOrCurrentFocus` `00263770`, `00269C70`, `00327270`, `BattleUnit_GetPartyLeader` `003272A0`, `003272F0` and `PartyFocus_IsCurrentPackedActorHandle` `003273B0`. The party layer steers the controlled actor by writing its movement context through these accessors, and the accessors resolve "the current actor" through the party's focus handle; the contexts' layout is this page's, the choice of actor is the party's.

**Presentation — CLIENT and SERVICE (86 edges).** Render bodies read actors through the census accessors: `Actor_GetWorldPosition` `00265020` is called by `BattleUnit_TestActorViewFrustumAtCurrentPosition` `00322360`, `002B7B80`, `0037AD40`, `003A40F0`, `003A56F0`, `003C29A0` and `003C37B0`; `003590D0` by `RenderSystem_UpdateCharacterRecords` `00426090`, `CharacterRenderSystem_UpdateLODAndRenderState` `004264A0` and ten more render bodies; `ActorManager_GetRecordByOrdinal` `00358940` by `003A4290`, `003A56F0`, `00465120` and `00465690`; `0024CFF0` by `CharacterRenderRecord_TeardownAndReset` `004200A0` and `CharacterRenderRecord_UpdateRootAnimationPresentationPhase` `0042C410`; `00263940` by `WorldActor_TestBoundsAgainstViewFrustumAtPosition` `003223C0`; `00267310` by the resource owner sweep `003DD4C0`. In the other direction the census accessors drive render state: the bind `0026C8C0` sets the character fade distances through `CharacterRenderSystem_SetFadeWidth` `002E83A0`, `CharacterRenderSystem_SetFadeStartDistance` `002EBC30` and six `CharacterRenderConfig_*` fade getters and setters; `002E28E0`, `002E3110`, `002E35B0`, `002EBB80` and `002ECD50` reach `Actor_RefreshPresentationVisibility` `002E8FD0`, which sets render-record flags through `RenderRecord_SetPresentationFlag400` `00428DE0`, `RenderRecord_SetPresentationFlag800` `00428E10` and `RenderHierarchy_SetPresentationFlag1000` `00429020`; `002EB0D0` calls eight small render-record bodies from `004270A0` to `004278B0`; `CharacterRender_DispatchCombatRelationEvent` `002ED2A0` and `CharacterRender_ApplyCombatRelationEvent` `003E6B50` pass a relation event on to `RelationLook_ApplyRelationEvent` `00512F30`; `00358F90` calls `CameraSystem_SetCameraActive` `0025A520`; and `WorldActor_UpdateRuntimeAndScriptExecutionState` `0025DF00` calls three small presentation bodies. The contexts carry the actor state the renderer reads each frame, and the census accessors are also where actor-side changes are pushed into render records; the render records themselves are that layer's.

**Resource — SERVICE (1 edge).** `0042FB80` calls `00409090`, a 53-byte walk of the null-terminated tag table at `01EFF940` that returns the entry whose first dword matches. A generic tag lookup under a census accessor; no context semantics cross.

**Save_Load_Settings — SERVICE (1 edge).** The bind `0026C8C0` calls `SaveImage_GetPersistentPayloadBase` `002EF2B0`. Binding a loaded definition payload reads the persistent save payload (as the field-id getter does); what it reads there is not read here.

**Script_VM_Native_Bridge — CLIENT and SERVICE (320 edges).** Script-verb bodies are the largest client of the census accessors: 56 verbs call the per-slot byte reader `00267310` (among them `0033F330`, `00340260`, `00340FA0`), 29 call `0026A1A0` (which, for a kind-3 actor, sets or clears bit 7 of byte `+0x62` behind the context's `+0xF0` pointer), 23 call `Actor_GetWorldPosition` `00265020`, 17 call `ActorManager_GetRecordByOrdinal` `00358940` (including `WorldActorScriptVM_InterpretBytecode` `0025E4C0`), 16 call `0026C120`, 14 call `003590D0`, and 49 more census accessors have one to 13 verb callers each; the census's own verb bodies `00350DD0`, `003516E0`, `00352580`, `0033F890`, `0033FCD0`, `0050D780` and `0050D860` call `VMValueStack_PopNumericDiscard` `00267DB0`, `VMValueStack_PopInt32CoerceFloat32` `00267E10` and `VMResult_WriteInt32` `0026B4E0`; and the actor drive pass `0025DF00` calls the interpreter `0025E4C0` and the wait-list tests `ScriptVM_WaitList_HasAnyActorChannelActive` `00267420` and `ScriptVM_WaitList_HasAnyActorResourceEntryActive` `002674B0`. Authored script reads and writes both contexts through these accessors, one verb per operation, and the drive pass runs the interpreter that dispatches those verbs; the verb dispatch is the VM's, the context layout is this page's.

**Story_Event_Quest_Hunt — SERVICE (1 edge).** The bind `0026C8C0` calls `EventMemory_QueryDefinitionIdAbsent` `00377440`. Binding a definition asks the event memory whether that definition id is absent; the event memory is the story layer's, and the bind is cited here only as a context writer.

## The `002E45E0` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`002E45E0` `Movement_UpdateSteeringTowardTarget` (380 B) — the steering
update: `003587C0` (`002E464A`), unit resolve `003590D0` + `003588B0`
(`002E4651`/`002E465C`), `00265020` (`002E467C`), `003DA6A0`
(`002E468F`), then `003A19C0` delta math (`002E46E1`), `003A1AD0` ×2
(`002E46FF`/`002E4722`), `00267310` (`002E4730`), `0026AFE0`
(`002E4751`).

| member | role | interior |
| --- | --- | --- |
| `003A19C0` (268 B) | vector-delta math — `xmm6 = [r9+4]−[r8+4]`, `xmm7 = [r9+8]−[r8+8]`, `xmm8 = [r9]−[r8]`, `mulss xmm3, xmm7` (`003A19D2`–`003A1A05`) — the Y/Z/X difference and cross product | [`003A19F8`](../../_index/ADDRESS-INDEX.md) |
| `003DA6A0` (112 B) | steering-angle stage — `(rcx, rdx, r8, r9)` shuffled to `rsi/rdi/rbx/rbp`, then `003DA730` + `003A1D30` (`003DA6C8`/`003DA6CD`) | [`003DA6C8`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `003587C0`, `003590D0`, `003588B0`,
`00265020`, `003A1AD0`, `00267310`, `0026AFE0`, `003DA730`,
`003A1D30`.

## The `0025B070` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`0025B070` (`ActorSystem_ReleaseManagerRecords`) — walks the record
range `word[rcx+0x1DA]` through `word[rcx+0x1D2] + count`
(`0025B086`/`0025B095`), releasing each through the member.

| member | role | interior |
| --- | --- | --- |
| `002EB780` (21 B) | record free — `0026AF30(rcx, 0)` then return 1 (`002EB786`/`002EB78B`) | [`002EB786`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0026AF30`.

## The `002E6BD0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`002E6BD0` (~400 B) — null-gated census walk (`002E6BD3`).

| member | role | interior |
| --- | --- | --- |
| `002E9C60` | `movsx word[+0x1E]` < 0 → out; else `×9` index (`002E9C65`/`002E9C6E`) | [`002E9C65`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.
