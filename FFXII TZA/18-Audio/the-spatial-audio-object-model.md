---
system: The spatial audio object model — a listener and five shapes of sound source
category: 18-Audio
status: AUDITED
owner_layer: PrimaryOwner:Audio
evidence_tier: 4
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN160 -> GN161 - the records this document rests on are unchanged except for `002F0280`, `002F67C0`, which gained a plate comment and CodeDomain tags in batch R109 and lost nothing; voided by any delta that removes or rewrites a comment, tag, name, prototype or body range; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-13
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-spatial-audio-pass-1 - WITHDRAWN: the abstract's 'every SIMD vector instruction in the entire executable belongs to this system' fails under every reading - packed arithmetic is 2,585 instructions in 235 functions image-wide, of which only 29 lie in the Sd::Lay range, and the counter-examples include the transform workbench's own point transform; the section 2 warning's denominator of 12 matches none of the four censuses and does not state its instrument; BUT sqrtps occurs 14 times in exactly six functions and ALL SIX are inside the audio cluster 007F0320-007F25E0, so PACKED square root does belong to this system even though packed arithmetic does not - NARROWED 2026-09-13: that is a claim about the sqrtps INSTRUCTION and not about square roots as an operation, because the animation composer 005C72A0 takes one per quaternion normalize through a call to the sqrtf thunk 00861F14, which no instruction census can see; the class family and the 39 methods were NOT re-derived
  crossref_clean: false        # 2026-09-30 (SWE2-DATA): false until the pass-22 UNACCOUNTED NEIGHBOUR findings are accounted (FRONTIER-REQ-SWE2-DATA-PASS22-DEBT; OPUS-REQ-DATA-PASS30-CROSSREF-CLEAN-0930)
  reopened_count: 0
---

# The spatial audio object model

> FFXII does not have one kind of sound source. It has **five shapes** — a point, an area, a
> direction, a polygon and a dynamic one — ~~and **every SIMD vector instruction in the entire
> executable belongs to this system**, not to graphics or movement.~~ **The SIMD claim is
> wrong and is withdrawn (§8): packed-SSE arithmetic appears in 235 functions image-wide, of
> which 29 are in this system's address range.**

## 1. What the player sees

Stand near a chest and its glimmer chimes from that spot: turn around and the sound moves to the
other ear, walk away and it fades. That is a **point** source, and it is the one everybody expects.

Walk along the river in the Estersand and the water does not behave that way. It does not come from
a spot; it comes from **the whole length of the bank**, and its volume barely changes as you walk
parallel to it — it changes when you walk *toward or away from* the water. The engine models that
edge as a **polygon** source, and the difference is why a river sounds like a river rather than like
a very loud chest sitting in the middle of it.

A cave rumble that is simply *everywhere in this room* has no position to move around at all. Wind
with a prevailing direction, a source that follows a moving object — the engine has a distinct class
for each.

**The listener is the player.** Everything above is computed relative to one listener object holding
a position and an orientation, and every one of these classes answers the same question in its own
way: *given where the player is standing and facing, how loud and from which direction am I?*

## 2. Native mechanism

### The class family, recovered from vtables

Nine `SQEX::Sd::Lay::*` classes hold **39 recovered virtual methods** in the RTTI map, and each
class's overrides occupy **one contiguous address range** — compile order, which is declaration
order in one translation unit:

> ⚠ **This table accounts for 4 of the 12 SIMD-bearing functions and reads as though it were a
> complete partition.** The other eight carry SIMD with **no class attribution** — two of them two
> `sqrtps` each. The missing attributions are `CO-10`.
>
> **Attributed 2026-09-14 (FABLE, `CO-10`): all twelve.** The attribution maps every function containing `sqrtps` or
> `rsqrtps` against the slots of every RTTI-named `Sd::Lay` vtable, `SoundSourceObject` included, then follows callers for
> the rest.
>
> **Seven are virtual methods:**
>
> | function | where it sits |
> |---|---|
> | `007F0820` (1,966 B) | `SoundSourceObject` slot 10, inherited by Ambient, Point, Direction and Polygon |
> | `007F1670` | `DynamicSound` slot 10 |
> | `007F1340`, `007F1A50`, `007F25E0` | slot 34 of Dynamic, Point and Polygon |
> | `007F1EC0` | `DirectionSound` slot 7 |
>
> **Five are non-virtual helpers of those classes:**
>
> | function | what calls it |
> |---|---|
> | `007F0320` (600 B, 2 × `sqrtps`) | slot 35 of Dynamic, Point, Direction and Polygon, never Ambient |
> | `007F74E0` (1 × `rsqrtps`) | `PolygonSound` slot 34, three times |
> | `007EF630` and `007EF790` (2 × `rsqrtps` each) | the `Lay` action consumer `007BAEC0` |
> | `007EF1E0` and `007EF3B0` | `007EF630` and `007EF790` |
>
> - **The last four are the listener's setters.** In `007BAEC0` each call receives the `Listener` from `007BB610` in
>   `rcx` and floats from the action record. Both store a position with `w` = 1 at `Listener + 0x30` (`007EF68D`,
>   `007EF7ED`) and normalise direction vectors into `+0x40` / `+0x50`.
> - **The two differ in one store.** `007EF790` also writes the position to `+0x20` (`007EF7F2`).
>
> This also answers who moves the listener: `Lay` actions, consumed by `007BAEC0`, not a per-frame poll inside Sead.
> Interior anchor (2026-09-17, SWE2-FRONTIER): the consumer's own body interleaves the
> `007BB610` listener getter (×4) with the two setters exactly as described —
> [`007BB00A`](../_index/ADDRESS-INDEX.md) → `007EF790`, `007BB076` → `007EF630` —
> around a `007BC2B0` ×12 per-element loop.

| class | address range | methods |
|---|---|---:|
| `Sd::Lay::Page` | `007BB950` | 1 |
| `Sd::Lay::Listener` | `007EF1A0` | 1 |
| `Sd::Lay::SoundSourceObject` | `007EFA70` | 1 |
| **`Sd::Lay::DynamicSound`** | `007F1030` – `007F1670` | **10** |
| **`Sd::Lay::PointSound`** | `007F17B0` – `007F1A50` | **6** |
| **`Sd::Lay::AmbientSound`** | `007F1C80` – `007F1D10` | **3** |
| **`Sd::Lay::DirectionSound`** | `007F1D70` – `007F1F80` | **4** |
| **`Sd::Lay::PolygonSound`** | `007F2020` – `007F25E0` | **6** |
| `Sd::Lay::SoundObject` | `007F7390` – `007F7420` | 4 |
| `Sd::Lay::ACTION` | — | 2 |

### Slot 34 is the spatial computation, and which classes override it is the finding

| class | overrides slot 34 | SIMD in it |
|---|---|---|
| `PointSound` | **yes** — `007F1A50` | `sqrtps` ×1 |
| `PolygonSound` | **yes** — `007F25E0` | `sqrtps` ×7 |
| `DynamicSound` | **yes** — `007F1340` | `sqrtps` ×1 |
| `DirectionSound` | ~~**no** — its heavy method is slot 7, `007F1EC0`~~ **yes** - superseded by the 2026-09-14 correction below | `rsqrtps` ×1 |
| `AmbientSound` | ~~**no override at all**~~ **yes** - a constant position (`007F1D10`); superseded by the correction below | none |

> **Corrected 2026-09-14 (FABLE, `CO-4` / `CO-6`), from the vtables themselves: every source class overrides slot 34.
> What differs is how much each one computes there.** Read straight from the five RTTI-named 40-slot vtables:
> `AmbientSound` `01CB9C88`, `PointSound` `01CB9B40`, `DirectionSound` `01CB9DD0`, `DynamicSound` `01CB99F0`,
> `PolygonSound` `01CB9F18`. The base `SoundObject` (`01CBAB68`) has 34 slots, so slots 34–39 are the source-object
> interface. The table above came from the method index, which recovered only part of each class.
>
> | slot | `AmbientSound` | `PointSound` | `DirectionSound` | `DynamicSound` | `PolygonSound` |
> |---:|---|---|---|---|---|
> | 7 | `007F0210` (262 B), inherited from `SoundSourceObject` (corrected 2026-10-01, OPUS) | `007F1960` (212 B) | `007F1EC0` (188 B) | `007F1220` (210 B) | `007F24F0` (219 B) |
> | 34 | **`007F1D10` (33 B)** | `007F1A50` (497 B) | **`007F1F80` (35 B)** | `007F1340` (742 B) | `007F25E0` (2,115 B) |
> | 35 | `007F1CE0` (42 B) | `007F1850` (265 B) | `007F1DD0` (232 B) | `007F10F0` (265 B) | `007F20E0` (1,032 B) |
> | 36 | `007E57B0` → `false` | `007F1A40` → byte `+0x128` | `007E57B0` → `false` | `007F1300` (8 B) | `007F25D0` (8 B) |
> | 39 | `007E57B0` → `false` | `007E5800` → `true` | `007E57B0` → `false` | `007E5800` → `true` | `007E5800` → `true` |
>
> - **Slot 34 writes the source's effective position** to `+0xD0 … +0xDC` (with `w` = 1.0) and writes the byte
>   `+0xE0`.
>   **CORRECTED 2026-09-22 (FABLE), against this box's own author.** This read *"and sets the ready byte
>   `+0xE0` = 1"*. **That is true of two classes of the five**, and it contradicted §"The early-out, in
>   `PointSound::slot34`" **on this page**, which already had `+0xE0` as *"listener-to-source distance
>   `< +0xE4`"*. Read from the bytes in all five bodies: `AmbientSound` (`007F1D29`) and `DirectionSound`
>   (`007F1F9B`) store the immediate `1`; **`PointSound` (`007F1A7A`, `007F1C23`), `DynamicSound`
>   (`007F15EE`) and `PolygonSound` (`007F2DEE` `setb al`, and `0` on the early-out at `007F2DF9`) derive
>   it from a `comiss` against the radius `+0xE4`.** *`+0xE0` is an audibility boolean, not a readiness
>   flag, and the two classes that always set it are exactly the two that have no geometry to test.*
>   See [the spatial-source contract](CONTRACT-spatial-source-objects.md) SA-3.
>   **A second thing this box did not say:** among the five slot-34 bodies, `+0xE4` is **written by
>   `DynamicSound` alone** (`007F13EC`) — for the other four the radius is supplied to slot 34, for
>   that one slot 34 produces it (SA-4). *(Worded without the obvious noun deliberately: the crossings
>   gate credits a layer whenever its alias appears as a whole word ANYWHERE in the prose, and that
>   noun is also a layer name, so using it here silently cleared one of this page's unaccounted
>   crossings. Filed as a gate defect.)*
>   - `AmbientSound`'s version writes `(0, 0, 0, 1)` and nothing else (`007F1D10`).
>   - `DirectionSound`'s copies a stored vector from `+0x100` (`007F1F80`).
>   - Point, Dynamic and Polygon compute it against the listener, which is where the square roots are.
> - **Slot 35 for `AmbientSound`** fills its out-parameters with constants: `1.0`, then zeros, then `(0, 0, 0, 1)`,
>   and returns 0 (`007F1CE0`). The other four compute theirs.
> - **Slot 39** returns `false` for Ambient and Direction and `true` for Point, Dynamic and Polygon: a
>   geometric-source flag.
> - ~~**Slot 7 is per-class in all five.**~~ *(Corrected 2026-10-01, OPUS: in four of five - `AmbientSound`'s slot 7 is `SoundSourceObject`'s own `007F0210`.)* It is not `DirectionSound`'s substitute for slot 34.

> **A sound that is everywhere needs no geometry, and the class that models it has none.**
> `AmbientSound` contributes **three** methods and not one SIMD instruction. `PolygonSound` needs
> seven square roots because measuring distance to an *edge* is not measuring distance to a *point*.

**That is the shape of the whole system in one table**: the amount of vector maths per class tracks
exactly the geometric complexity of the shape it represents.

### Every SIMD square root in the executable is here

Twelve functions in the image contain `sqrtps` or `rsqrtps`. **All twelve are Audio-owned**, and
**all twelve are in this cluster** (`007EF1E0`–`007F74E0`).

**The callers were censused rather than assumed** — and the first census was over-counted, corrected
2026-09-07 by an independent audit:

> ⚠ **This originally read "12 direct callers".** **Twelve is the number of call *edges*; there are
> nine distinct callers** — and the coincidence that the edge count equals the function count is
> exactly what hid it. Worse, **four of the nine are themselves members of the twelve**
> (`007EF630`, `007EF790`, `007F1670`, `007F25E0`): the cluster vouching for itself.

**The honest figure is five callers from outside the cluster** — `007F10F0`, `007F1850`, `007F1DD0`,
`007F20E0`, `007BAEC0` — **and all five are Audio-owned.** The conclusion stands (zero non-Audio
callers, internal or external, nothing from Movement or Presentation), **but on five independent
supports rather than twelve.**

> **This is why the geometry path in FFXII contains no SIMD at all.** The engine takes every
> gameplay distance through a scalar `sqrtf` call into the system CRT (566 call sites), and reserves
> its only hand-vectorised maths for positional audio. The vector normalise, the cross product and
> the masked 3-component dot product documented in
> [`../24-Compiler-And-CRT-Runtime/Maths-Library/the-maths-the-game-runs-on.md`](../24-Compiler-And-CRT-Runtime/Maths-Library/the-maths-the-game-runs-on.md)
> §4 are **audio DSP**, not scene geometry.

### The listener, and the shared accessor

`FUN_007BB610` is called by the whole cluster and returns the listener/context object. Read from
`PointSound::slot34`:

| offset | read as |
|---|---|
| `+0x30 … +0x3C` | four floats — the listener position (with a `w`) |
| `+0x60 … +0x9C` | sixteen floats — the listener orientation, read as four rows of four |

> **The object, identified 2026-09-14 (FABLE, `CO-5`): the single `SQEX::Sd::Lay::Listener`.**
>
> - **The accessor.** `007BB610` is `mov rax, [02EADE08] ; ret`. Its only writer is `007BB620`, which allocates
>   `0xA0` bytes through Sead's allocator (`007AD460`, memory category 3, the `Lay` layer), constructs them with
>   `007EF100`, and stores the pointer (or 0 on failure).
> - **When it is created.** `007BB620` is called once, from the `Lay` initialiser `007A5B50` (`007A5C87`), immediately
>   after the `LayAction` pool is built.
> - **The class.** The constructor installs vtable `01CB9898`, whose RTTI is `SQEX::Sd::Lay::Listener`, deriving from
>   `SeadObject<3,16>`. Slot 0 is `007EF1A0`, the one method this page already lists.
> - **The initial state, which is exactly what `PointSound::slot34` reads.** `+0x10` and `+0x40`/`+0x50` are
>   zeroed. `+0x20` and `+0x30` are `(0, 0, 0, 1)`, a position at the origin with `w` = 1. `+0x60 … +0x9C` is the
>   identity matrix, loaded from rows `(1,0,0,0)`, `(0,1,0,0)`, `(0,0,1,0)` and `(0,0,0,1)` at `008C5F80`, `008C5F90`,
>   `008C5FB0` and `008C5FD0`.
> - **Scope.** There is one listener per process, and it lives in the `Lay` static block beside the containers named
>   on [static initialization, T-8](../24-Compiler-And-CRT-Runtime/Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md).
>   Its position and orientation are written by the `Lay` action consumer `007BAEC0` through `007EF630` / `007EF790` (see
>   `CO-10` above).

**A position and a full transform**, which is what a source needs to answer *"from which direction,
relative to the way the player is facing?"* rather than merely *"how far?"*.

### The early-out, in `PointSound::slot34`

```c
if (*(float *)(this + 0xE4) <= 0.0f) {
    *(u8 *)(this + 0xE0) = 0;      /* param_1[0x1C] as a byte */
    return 0xFFFFFFFF;             /* "nothing to do" */
}
```

**A float at `+0xE4` gates the entire spatial computation**, and a non-positive value both clears a
flag byte and returns the failure sentinel. Its identity is not established — a radius, a gain or a
range would all fit — see `CO-1`. *(Superseded 2026-09-14, FABLE, `CO-1`: it is **the audible range**.
The same method ends by setting `+0xE0` = listener-to-source distance < `+0xE4` (`007F1BF8`–`007F1C23`),
and slot 7 `007F1960` initialises it from descriptor `+0x18`; see the answered `CO-1` item in the checklist below.)*

Past the gate the method fetches the listener twice, copies the full transform to the stack, and
optionally calls **`this->vtable[0x20]`** (a virtual on itself) whose result is passed through
`FUN_007A46E0` and `FUN_007A7010`, gated on a byte at `this + 0x129`.

## 3. Key addresses

| address | class · slot |
|---|---|
| `007EF1A0` | `Sd::Lay::Listener` slot 0 |
| `007EF1E0` | vector normalise — `rsqrtps` + one Newton–Raphson step |
| `007F1340` | `Sd::Lay::DynamicSound` slot 34 |
| `007F1670` | `Sd::Lay::DynamicSound` slot 10 |
| `007F1A50` | `Sd::Lay::PointSound` slot 34 |
| `007F1EC0` | `Sd::Lay::DirectionSound` slot 7 |
| `007F25E0` | `Sd::Lay::PolygonSound` slot 34 — 2,115 B, 7 × `sqrtps` |
| `007BB610` | listener/context accessor, called across the cluster |
| `007EFA70` | `Sd::Lay::SoundSourceObject` slot 0 |

## 4. Modding notes

- **Sound source *shape* is a class, not a parameter.** Making a point source behave like a river is
  not a tuning change; it is a different object with a different slot-34 implementation.
- ~~**`AmbientSound` has no spatial method**, so nothing about listener position can affect it.~~ *(Superseded 2026-09-14, CO-4: its slot 34 writes a constant position, so listener position still does not move it. Struck 2026-10-01, OPUS.)* A mod
  that expects an ambient bed to attenuate is fighting the class hierarchy.
- **The five heavy methods have no direct callers** — they are reached through vtables only, so a
  call-graph search for them returns nothing. That is what made this family invisible until the RTTI
  map was applied.
- **`+0xE4` is the master gate on a point source's spatial update.** Zero or negative disables it
  entirely and clears the flag at `+0xE0`.

## 5. What is not known

- [x] **What `+0xE4` is** — radius, gain or range all fit the single comparison. `CO-1`.
  *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (CO-1):* **the audible range — the distance
  beyond which the source is dropped from the frame.** `PointSound::slot34` (`007F1A50`) uses `+0xE4` twice:
  - **Entry gate.** A range `<= 0.0` clears `+0xE0` and returns `0xFFFFFFFF` (`007F1A6E`–`007F1A81`).
  - **Exit test.** It computes the Euclidean distance from the listener position (`Listener + 0x30`) to the effective
    position `+0xD0`, masked by `(1, 1, 1, 0)` at `00D11570`, followed by `sqrtps`. It then sets **`+0xE0` =
    (distance < `+0xE4`)** (`007F1BF8`–`007F1C23`).

  `+0xE0` is exactly the byte `007BC4F0` requires before copying a source into the per-frame batch (`CO-2`), so a
  source outside its range is computed but not submitted.
  - **Where the range comes from.** Slot 7 initialises it from its descriptor argument: `PointSound` slot 7 `007F1960`
    stores descriptor `+0x18` at `+0xE4` (`007F19B0`), beside `+0x1C` → `+0xE8`, the base position `+0x24…+0x2C` →
    `+0x100`, and the byte `+0x30` → `+0xE1`. `DynamicSound` slot 34 recomputes it (`007F13EC`).
  - **In between** (read, not named): when `+0x124` is non-zero, the source's `y` follows the listener's `y` by at most
    `|+0x124|`, and only in the direction its sign allows (`007F1B94`–`007F1BF0`). When `+0x129` is 1 and a check
    through slot 4 succeeds, the position is instead `+0x110` transformed through the listener's matrix
    (`007F1AA8`–`007F1B8A`).
- [x] **What slot 34 returns and what its callers do with it.** The signature is
  `undefined8 (Sound *this)` and the failure path returns `0xFFFFFFFF`. `CO-2`.
  *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (CO-2):* **a signed status, and the one caller
  that dispatches it uses it to decide whether the source joins this frame's batch of positioned sources.** The call is
  `007BC5B6`, in `007BC4F0`, which is called from `007A5E50`. `007BC4F0` walks the `Lay` sound-object list under the
  critical section `02EADEB0`, and for each object:
  1. It calls slot 6 (`[vtable + 0x30]`). Every source class returns `true` there (`007E5800`); the base returns `false`.
  2. It calls **slot 34**.
     - **A negative result** (the `0xFFFFFFFF` path) makes it call **slot 11** with `0.0` in `xmm1` (`007BC647`–`007BC650`).
     - **Otherwise**, it requires the byte `+0xE1` = 0 and slot 34's ready byte `+0xE0` ≠ 0, then calls slot 1 twice and
       skips the object if that returns 2 or 3.
  3. A source that passes is copied into the next 32-byte entry of the array at `[02EADEE0]`: its effective position
     `+0xD0`/`+0xD4`/`+0xD8` (the values slot 34 wrote), the dword `+0xF0` and the qword `+0x08`. The object pointer goes to
     `[02EADED8][n]`, and the count is incremented (`007BC5F6`–`007BC641`).

  So slot 34's output is consumed as data (the position) and its return only as success or failure. **Not established:**
  what slot 11 does with the `0.0`, what slot 1's states 2 and 3 are, and who reads the batch arrays. The other `+0x110`
  dispatch in Sead, `007A7760` in `007A76A0`, is on a different object (from `007B77E0`) and returns a float, so it is
  not this interface.
- [x] ~~The `PolygonSound` edge algorithm.~~ **EXTRACTED 2026-09-07** — two modes (nearest-vertex and
  plane-and-edges), a plane projection with an inside test, and three edge distances under a
  `(1,1,1,0)` mask. See the extension below. Residue: `CO-7` (which mode the shipped data uses),
  `CO-8` (`+0x218`), `CO-9` (one triangle or a fan). `CO-3`.
- [x] **What `DirectionSound` uses slot 7 for** when its siblings use 34. `CO-4`.
  *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (CO-4): the premise was wrong.*
  `DirectionSound` does override slot 34, with a 35-byte body (`007F1F80`) that copies its stored vector `+0x100` into
  the effective position and needs no computation. **Every** source class has its own slot 7 (188–262 B each), so slot 7
  is not a substitute for 34. What slot 7 does in any class was not read. See the corrected table under the slot-34
  section.
- [x] **Whether nothing else gives `AmbientSound` a spatial path.** `CO-6`.
  *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (CO-6): confirmed at every
  source-interface slot — it has none.*
  - Its slot 34 writes the constant position `(0, 0, 0, 1)` (`007F1D10`).
  - Its slot 35 returns constant outputs (`007F1CE0`).
  - Slots 36 and 39 return `false`; the geometric classes return `true` at 39.
  - ~~It contributes five slots of its own (0, 1, 7, 34, 35), not three.~~ *(Corrected 2026-10-01, OPUS, from the vtable bytes: it differs from `SoundSourceObject` (`01CB98A8`) at slots 0, 1, 34, 35 and 39, but slot 1 (`007E3260`) and slot 39 (`007E57B0`) are shared stubs and slot 7 (`007F0210`) is the parent's own entry, so its own bodies are 0, 34 and 35 - three, as `UQ-267` says.)* No function in its vtable calls the listener
    accessor `007BB610`; all 15 call sites are in the Point, Direction, Dynamic and Polygon bodies and the driver.
- [x] ~~**UQ-266.** **The full slot map of `Sd::Lay::SoundObject`** — the base class whose 4 methods every source
  inherits.~~
  ***ANSWERED 2026-09-22 (FABLE): all 34 slots read. `SoundObject` is an ABSTRACT base that is mostly inert —
  four slots are pure virtual, twenty-six are constant stubs, and only four carry a body.***
  **First, the vtable is confirmed by RTTI rather than assumed.** `01CBAB68 − 8` holds a complete-object
  locator whose type descriptor reads **`.?AVSoundObject@Lay@Sd@SQEX@@`, offset 0**; the five source vtables
  resolve the same way to `AmbientSound`, `PointSound`, `DirectionSound`, `DynamicSound` and `PolygonSound`,
  all at offset 0. *(This also re-confirms the §2 statement that the base has 34 slots, on which
  [the contract's](CONTRACT-spatial-source-objects.md) `SA-5` rests.)*

  | slots | target | size | what it is |
  |---|---|---:|---|
  | **0** | `007F7390` | 62 B | own body — installs the vtable `01CB9888` and runs a member teardown |
  | **1–4** | `00861EC6` | 6 B | **`_purecall`** — four PURE VIRTUAL slots |
  | 5, 18, 20, 22, 24, 26–32 | `007AC3D0` | **4 B** | `or eax, -1; ret` — **returns −1**, twelve slots |
  | 6 | `007E57B0` | 3 B | `xor al, al; ret` — returns false |
  | **7** | `007F7420` | 23 B | own body — stores `r9` at `+0x18` and copies two qwords in: a setter |
  | **8** | `007F7400` | 24 B | own body — reads `+0x18`, null-guarded, and dispatches through it |
  | **9** | `007F73D0` | 33 B | own body — the same `+0x18` indirection with a frame |
  | 10–17, 19, 21, 23, 25 | `007AD440` | **3 B** | `xor eax, eax; ret` — **returns 0**, twelve slots |
  | 33 | `007EFF80` | 14 B | zeroes the three out-parameters `[rdx]`, `[r8]`, `[r9]` and returns −1 |

  **So the base's four real methods are exactly the `007F7390`–`007F7420` range §2 records**, and every other
  slot is either pure virtual or a shared constant. *The two constant stubs are engine-wide, not this
  interface's:* `007AD440` and `007AC3D0` each fill **twelve** base slots, and `007E57B0` is the same
  false-returning stub the source classes use at slots 36 and 39 — which is why
  [the contract's](CONTRACT-spatial-source-objects.md) `SA-6` says neither stub belongs to this interface
  alone.
  **What the derived classes do with it.** All five override nearly every slot; the base is a shape to fill,
  not behaviour to inherit. The only slots any source class leaves at the base value are the inert ones —
  `DynamicSound` alone overrides 14, 15 and 33, and 16 is overridden only by Point, Dynamic and Polygon.
  ***Not claimed:*** what the four real methods are FOR — `+0x18` is plainly an owner or parent pointer and
  slots 7–9 set and follow it, but no caller was traced, and the pure-virtual four are named by nothing.*
- [x] ~~**UQ-267.** No `AmbientSound`, `DynamicSound` or `PolygonSound` body has been read; only the address,
  class, slot and instruction census.~~
  ***NARROWED 2026-09-22 (FABLE): `AmbientSound` is now read in FULL, and what remains is named in bytes
  rather than as "no body".*** Each class's own bodies are the ones inside its declared address range; every
  other slot in its vtable points at the shared `Sd::Lay` object machinery. Counted from the vtables:

  | class | own bodies | own code | state |
  |---|---:|---:|---|
  | **`AmbientSound`** | **3** | **163 B** | **fully read** |
  | `DynamicSound` | 10 | 1,761 B | 4 read (`s33`, `s36`, and `s34`/`s35` in part) |
  | `PolygonSound` | 6 | 3,548 B | 2 read (`s36`, and `s34` in part) |

  **`AmbientSound`, all three:** `s0` `007F1C80` (88 B) is the **scalar-deleting destructor** — it installs
  its own vtable at `[rcx]`, calls the base teardown `007EFA30`, and on flag bit 0 either frees through
  `007AD450` or takes a guarded path on bit 2, returning `this`; `s34` `007F1D10` (33 B) and `s35` `007F1CE0`
  (42 B) are the two §2 already describes. *So the destructor was the only unread one, and this class is done.*

  **Two slot families completed across all five while reading them.**
  - **Slot 36 is a per-class stored boolean, at a DIFFERENT offset in each class**: `PointSound`
    `byte [this + 0x128]` (`007F1A40`), `DynamicSound` `byte [this + 0x148]` (`007F1300`), `PolygonSound`
    `byte [this + 0x214]` (`007F25D0`) — each an 8-byte `movzx`-and-return — while `AmbientSound` and
    `DirectionSound` both use the constant-false stub `007E57B0`. *That is the same partition as slot 39
    ([the contract's](CONTRACT-spatial-source-objects.md) `SA-6`): the three geometric classes carry real
    state and the two without geometry answer with a constant.*
  - **Slot 33 asks for three floats, and the base's answer is "I have none".** `DynamicSound`'s override
    `007F1200` (29 B) copies `[this + 0x110]`, `+0x114` and `+0x118` into the three out-parameters and
    returns **0**; the base `SoundObject`'s `007EFF80` zeroes the same three and returns **−1** (`UQ-266`).
    *Dynamic is the only source class that overrides it.*

  ***`DynamicSound`: all ten own bodies now identified, and its state model falls out of them — 2026-09-22
  (FABLE).*** The class keeps **two position copies, a time accumulator and a dirty flag**, and every one of
  its small methods is about them:

  ```
  +0x100 .. +0x108   f32[3]  a SECOND copy of the position, synced only on demand
  +0x110 .. +0x118   f32[3]  the current position
  +0x138             f32     a time accumulator, advanced by slot 10
  +0x13C             u8      DIRTY — set by every position mutator, tested by slot 10
  +0x148             u8      the slot-36 boolean
  ```

  | slot | body | what it does |
  |---|---|---|
  | `s14` | `007F1630` (58 B) | **set position, syncing both copies** — writes the triple to `+0x110` *and* `+0x100`, sets dirty |
  | `s15` | `007F1310` (34 B) | **set position, current copy only** — writes `+0x110` alone, sets dirty |
  | `s16` | `007F1090` (88 B) | **add to position** — `addss` into `+0x110`, sets dirty, and syncs `+0x100` **only when the byte argument is zero** |
  | `s33` | `007F1200` (29 B) | **get position** — copies `+0x110`/`+0x114`/`+0x118` out, returns 0 |
  | `s10` | `007F1670` (239 B) | **the tick** — accumulates its float argument into `+0x138` and branches on the dirty byte |
  | `s0` | `007F1030` (88 B) | the scalar-deleting destructor, the same shape as `AmbientSound`'s |
  | `s7` | `007F1220` (210 B) | a wrapper that marshals two arguments and calls the shared `007F0210` |
  | `s36` | `007F1300` (8 B) | returns `byte [this + 0x148]` |
  | `s34`, `s35` | 742 / 265 B | the spatial computation and its parameters — read in part, in §2 and §4 |

  > **That is what "Dynamic" means against "Point".** A `PointSound` has a position; a `DynamicSound` is
  > *moved* — three distinct mutators, a dirty flag so the spatial pass knows, and a per-tick accumulator.
  > **The s14/s15 pair is the distinction worth keeping:** two setters that differ only in whether the second
  > copy follows, which a reimplementation with one setter cannot express.

  *A link recorded as a candidate, not a finding:* `DirectionSound`'s slot 34 reads its stored vector from
  **`+0x100`** (`007F1F80`), the same offset `DynamicSound` syncs here. Both classes derive from
  `SoundObject`, so a shared base field is the natural reading — **but no base-layout evidence was taken and
  this is not asserted.**

  ***`PolygonSound`: all six own bodies identified — 2026-09-22 (FABLE), and with it every body of all three
  classes.*** `s0` `007F2020` (88 B) is the same scalar-deleting destructor shape as the other two. `s7`
  `007F24F0` (219 B) marshals two arguments to the shared `007F0210` exactly as `DynamicSound`'s does, and on
  success **stores the descriptor's `+0x18` into `+0xE4` — the radius**. `s16` `007F2080` (86 B) **translates
  the whole polygon**: it walks `[this + 0x108]` entries of a `0x10`-strided array starting at `+0x110`,
  adding `(xmm1, xmm2, xmm3)` to each — so **`+0x108` is the vertex count and `+0x110` the vertex array**.
  `s35` `007F20E0` (1,032 B) reads the effective position `+0xD0`, the radius `+0xE4`, `+0xE8`, `+0x100`, a
  float at `+0x210`, and **three stored dword indices at `+0x218` / `+0x21C` / `+0x220`**, each used to
  address a 16-byte vector inside the object — *three points, which is why measuring to an edge costs the
  seven square roots §2 counts.* *(The exact index convention is not established: `s35` addresses with
  `[rbx + rax*8]` while `s16` walks a `0x10` stride, and nothing here reconciles the two.)*

  ***A structural law that held four times.*** The partition §2 found at slot 34 — Point, Dynamic and Polygon
  against Ambient and Direction — is **the same at slots 7, 16, 36 and 39**. The three geometric classes set
  a radius in slot 7, implement a translate in slot 16, return a stored boolean in slot 36 and `true` in slot
  39; the two without geometry write no radius at all, leave slot 16 alone, and answer both booleans with a
  constant stub. *One partition, four independent slot families.* **It also refines
  [the contract's](CONTRACT-spatial-source-objects.md) `SA-4`**, which was scoped to the slot-34 bodies and
  said four classes are *given* the radius: the giving happens in **slot 7**, in exactly the three classes
  that have one, and `DynamicSound` alone additionally rewrites it in slot 34.

  ***Depth, stated plainly so the tick is not read as more than it is.*** **All nineteen own bodies are
  identified. Fifteen are read in full**; the four left partial are the two large spatial computations of
  `DynamicSound` and `PolygonSound` (`s34` 742 / 2,115 B and `s35` 265 / 1,032 B), whose substance §2 and §4
  already carry and whose line-by-line arithmetic is not transcribed here.*

## 6. Evidence

| claim | evidence | tier |
|---|---|---|
| Nine classes, 39 virtual methods, contiguous per class | the recovered RTTI vtable map (`vtable-method-index.md`) | 4 |
| All 12 SIMD-bearing functions are in this cluster | full-image instruction decode over every function body | 1 |
| ~~All 12 callers are Audio-owned~~ **Nine distinct callers; five from outside the cluster; all Audio-owned** | caller census over the current call graph, **corrected 2026-09-07** — the original counted edges, and four of the nine callers are cluster members | 1 + 11 |
| ~~Slot 34 overridden by Point / Polygon / Dynamic and not by Ambient~~ *(Superseded 2026-09-14, CO-4: all five override slot 34; Ambient's writes a constant position. Struck 2026-10-01, OPUS.)* | vtable map slot numbers | 4 |
| `PolygonSound::slot34` holds 7 × `sqrtps` | instruction decode of its exact body | 1 |
| The `+0xE4` gate and the listener reads | complete decompilation of `PointSound::slot34` | 1 |
| **The player-facing shape descriptions in §1** | ~~inference from class names plus the SIMD distribution~~ — **UPGRADED 2026-09-07 to tier 1 for `PolygonSound`**: the plane projection, point-in-triangle test and three edge distances are read in full (see the `CO-3` extension). `AmbientSound`, `DynamicSound` and `DirectionSound` remain **tier 8** — class name plus instruction census, no body read. | 1 / 8 |

> **§1 is the weakest section in this document and is marked as such.** *"A river is a polygon
> source"* is a reading of a class name and an instruction count, not of an algorithm. It is written
> in the confident register the writing standard asks for; the evidence table is where its real tier
> is recorded.

## 7. Related

- [`sqex-sd-sound-driver-architecture.md`](sqex-sd-sound-driver-architecture.md) — the driver these
  classes sit on.
- [`../24-Compiler-And-CRT-Runtime/Maths-Library/the-maths-the-game-runs-on.md`](../24-Compiler-And-CRT-Runtime/Maths-Library/the-maths-the-game-runs-on.md)
  — the vector maths, now attributed here.
- [`../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md`](../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md)
  — the map that made this family findable.

## Extension 2026-09-07 — `CO-3`: the `PolygonSound` distance algorithm, extracted

`xiionline-61`, GN160. Complete decompilation of `PolygonSound::slot34` (`007F25E0`, 2,115 B).

### What a player hears, now with the mechanism behind it

The river is not measured from a point. **The engine measures the shortest distance from the player
to a *surface*** — and if the player is standing "over" that surface, the distance is the
perpendicular drop to it, not the distance to any corner. That is precisely why walking *along* a
riverbank barely changes the water's volume while walking *away from it* changes it immediately.

**And there are two modes.** One measures to the nearest **corner** of the shape; the other measures
to the **face and its edges**. A designer picks per source.

> **Corrected 2026-09-14 (FABLE, `CO-8` / `CO-9`): there are five modes, not two.** `PolygonSound::slot34` (`007F25E0`)
> branches on the mode byte `+0x104` = 0, 1, 2, 3 and 4 (`007F2688`, `007F26E4`, `007F279F`, `007F2978`, `007F2B21`). The
> vertices are the 16-byte entries from `+0x110`, and `+0x108` is their count.
>
> | mode | shape | what is measured |
> |---:|---|---|
> | 0 | point set | the nearest vertex (`007F268C`–`007F26CD`) |
> | 1 | **polyline** | the nearest point on each segment `(i, i+1)`, `i < count − 1`, through `007F7440` (`007F26EC`–`007F2770`) |
> | 2 | **triangle strip** | triangle `(i, i+1, i+2)` for `i < count − 2`, with the winding flipped on odd `i` (`007F27D0`–`007F2807`) |
> | 3 | **triangle fan** | triangle `(0, i−1, i)` for `i` = 2 … `count − 1` (`007F299B`–`007F29E4`) |
> | 4 | **triangle list** | `count / 3` triangles `(k, k+1, k+2)`, `k` stepping by 3 (`007F2B29`–`007F2CE5`) |
>
> For every triangle mode the procedure is the same:
> 1. Build the unit normal (`007F74E0`) and project the listener onto the plane.
> 2. If `007F7570` says the projection lies inside the triangle, take the absolute plane distance, and if it wins,
>    **store the triangle's three vertex indices in `+0x218` / `+0x21C` / `+0x220`**.
> 3. Test the three edges through `007F7440`; an edge that wins sets **`+0x218` = `0xFFFFFFFF`**.

### The object

| offset | meaning |
|---|---|
| `+0x0E4` | float gate — `<= 0.0` disables the source entirely |
| `+0x0E0` | flag byte, cleared on the disabled path |
| `+0x104` | **mode byte** — ~~`0` selects nearest-vertex, non-zero selects plane-and-edges~~ 0-4: point set, polyline, triangle strip, triangle fan, triangle list *(superseded by the CO-8 box above; struck 2026-10-01, OPUS)* |
| `+0x108` | **vertex count** — `< 1` disables the source |
| `+0x110 …` | the vertex array, **16-byte stride** (four floats each) |
| `+0x218` | written `0xFFFFFFFF` whenever an edge improves the best distance |

### The distance metric, with its real constant

Every distance in this function is the same 4-wide expression, and **the fourth lane is discarded by
a mask, not weighted**:

```
mask = (1.0f, 1.0f, 1.0f, 0.0f)         at 00D11570
d²   = Σ (P − Q)² · mask                 /* i.e. dx² + dy² + dz², computed 4-wide */
d    = sqrtps(d²)
```

`00D11570` is **the same W-lane kill mask** the maths library document already records for the masked
3-component dot product. **It is an ordinary Euclidean distance in three dimensions** — the fourth
component of every vector here is padding.

> **A note on how nearly this went wrong.** The decompiler renders the mask as four separate
> multiplies by four separate symbols (`_DAT_00D11570`, `_UNK_00D11574`, `_UNK_00D11578`,
> `_UNK_00D1157C`), which reads exactly like **per-axis weighting** — and a per-axis weighted
> distance would be a real and interesting finding: it would let a designer make a sound fall off
> faster vertically than horizontally. **It is not what the constant says.** Reading the sixteen
> bytes settled it in one step. *Four adjacent `_UNK_` symbols are one constant the decompiler
> could not name.*

### The algorithm

```c
if (this[0xE4] <= 0.0f || this[0x108] < 1) { this[0xE0] = 0; return 0xFFFFFFFF; }

listener = FUN_007BB610();
P        = listener[0x30 .. 0x3C];          /* listener position */
V        = (vec4 *)(this + 0x110);
best     = |P − V[0]|;                      /* seed on the first vertex */

if (this[0x104] == 0) {
    /* --- nearest-vertex mode --- */
    for (i = 0; i < this[0x108]; i++)
        best = min(best, |P − V[i]|);
}
else {
    /* --- plane-and-edge mode, per triangle --- */
    n    = FUN_007F74E0(v0, v1, v2);        /* plane normal, normalised (rsqrtps) */
    t    = dot3(n, v0 − P);                 /* signed distance to the plane */
    proj = P + t·n;                         /* project the listener onto the plane */

    if (FUN_007F7570(v0, v1, v2, proj))     /* is the projection inside the triangle? */
        best = |t|;                         /* yes: the perpendicular drop */
    else
        for (e = 0; e < 3; e++) {           /* no: the three edges, indexed modulo 3 */
            c = FUN_007F7440(vA, vB, P);    /* closest point on that segment */
            if (|P − c| < best) { best = |P − c|; this[0x218] = 0xFFFFFFFF; }
        }
}
```

**That is the textbook point-to-triangle distance**, and it accounts for the seven `sqrtps`: the
seed, the vertex scan, and the edge candidates.

The edge loop's index arithmetic is a **modulo 3** written out by the compiler as
`i + (i/3 + (i>>31) + …)·−3`, which is the standard signed-division-by-constant expansion — it is
`(i % 3)`, not a magic table.

| helper | size | role |
|---|---:|---|
| `FUN_007F74E0` | 135 B | plane normal from three points, normalised — the `rsqrtps` site |
| `FUN_007F7570` | — | point-in-triangle test on the projected point |
| `FUN_007F7440` | — | closest point on a segment |

### What this does to section 1

**It confirms it.** *"A polygon source is measured to a surface, not to a point"* was written from a
class name and an instruction count and marked **tier 8**. The algorithm is now read: a plane
projection, an inside test, and three edge distances. **§1's claim survives on tier 1 evidence**, and
its evidence-table row is corrected accordingly.

**What §1 did not know and now does:** there are **two** modes, and a `PolygonSound` in
nearest-vertex mode behaves much more like a point source than the section implies.

### Still open

- **Which mode the shipped data uses**, and for what. `+0x104` is read, never written here. `CO-7`.
  ***Chain traced to four originators 2026-09-15 (FABLE); the descriptor's writer is NOT identified,
  and the reason is stated rather than papered over.*** The previous narrowing ended at "the
  descriptor's writer is the next read". The reader `00221940` takes the descriptor in **`r8`**
  (`0022196F`) and pulls the kind from `+0x18` (`002219BF`), the mode byte from `+0x1C`
  (`00221A5F`), the count from `+0x20` (`00221A47`) and the vertex array from `+0x28` (`00221A7B`).
  Its three callers — `00223190`, `00224570`, `00224E40` — all **forward** a descriptor rather than
  build one, and each forwards it again from its own caller. The `rel32` chain, every edge read from
  the bytes and each function having exactly one caller until the last step:

  ```
  00221940  <- 00224E40 <- 0021C760 <- 00211200 <- 001DC190 <- 002DF460 <- 003A0E50
                                                                             |
      <- 00332C40 / 003B99D0 / 0046C8F0 / 0046CC70      (four callers, the first bodies that
                                                         pass the address of their OWN storage)
  ```

  `0046C8F0` is the worked example: it passes `lea rdx, [rsp + 0xa0]` and `lea r8, [rsp + 0x30]`
  into `003A0E50` at `0046CAA6`–`0046CAAE`.
  - **Why the trace stops there and no writer is named.** `003A0E50` (42 B) **swaps its arguments**:
    `mov rax, rdx` at entry, then `mov r9, r8` and `mov r8, rax` (`003A0E64`–`003A0E6A`), so which of
    the caller's two stack blocks becomes `00221940`'s `r8` depends on the swap **and** on the
    argument shuffles in the five wrappers between. Reading those five is the work, and it was not
    done. **Guessing which block is the descriptor would decide `CO-7` on a coin flip**, and the one
    field this document can already see in `0046C8F0` — a volume byte clamped to `0x7F` and stored at
    `[rsp + 0x49]` (`0046CA9B`) — does not disambiguate it.
  - **What this does settle:** the descriptor is **built on a caller's stack**, not loaded from a
    file. So `CO-7`'s answer is not going to be found by censusing authored data; it is in whichever
    of those four bodies fills the block, and the next read is the argument threading through the
    five wrappers.

  > ### `CO-7` ANSWERED 2026-09-22 (FABLE) — the modes are **1 and 3**, and two sentences above are wrong
  >
  > **The five wrappers have now been read, and the swap did not have to be resolved, because
  > NEITHER stack block is the descriptor.** `00221940`'s `r8` is the global **`0215E710`**.
  >
  > **`002DF460` does not forward a descriptor — it introduces one.** It consumes both incoming
  > blocks by calling `002DE800(rcx = arg3, rdx = arg4)` at `002DF497`, and then loads
  > `lea r8, [rip …]` → **`0215E710`** at `002DF49F` before tail-jumping to `001DC190`. *Every link
  > after that carries the global, and the argument position was read at each one:*
  >
  > | link | what carries it |
  > |---|---|
  > | `002DF460` → `001DC190` | `002DF49F lea r8, 0215E710` — **arg3** |
  > | `001DC190` → `00211200` | `001DC1A7 mov rdi, r8` then `001DC1BA mov r9, rdi` — **arg4** |
  > | `00211200` → `0021C760` | a 9-byte thunk; only `rcx` is rewritten, `r9` passes through |
  > | `0021C760` → `00224E40` | `0021C782 mov r14, r9` then `0021C7B1 mov r9, r14` — **arg4** |
  > | `00224E40` → `00221940` | `00224E5C mov rsi, r9` then `00224EB2 mov r8, rsi` — **arg3** |
  >
  > **An independent control that this document already contained.** The byte `0046C8F0` writes at
  > `[rsp + 0x49]` (`0046CA9B`) — noted above as *"does not disambiguate it"* — disambiguates it
  > exactly. `0046CA9F lea r8, [rsp + 0x30]` and `0046CAA6 lea rdx, [rsp + 0xa0]`, so the source
  > block is `[rsp + 0x30]`, and `002DE84A` reads **`[rdi + 0x19]`** — which is `[rsp + 0x49]`, the
  > same byte. *A wrong threading would not have landed on the one byte this page had already
  > singled out.* The other block, `[rsp + 0xa0]`, becomes `002DE800`'s `rcx`, whose first three
  > dwords are read as floats at `002DE816`–`002DE82B`: **a position, not a descriptor.**
  >
  > #### What `002DE800` writes, and the ladder that chooses it (FABLE, 2026-09-22)
  >
  > It fills the global from the source object and dispatches on **`[rdx + 9] & 0x7F`**
  > (`002DE89E`–`002DE8C1`), a **shape selector**:
  >
  > | selector | kind `+0x18` | mode `+0x1C` | count `+0x20` |
  > |--:|---|---|---|
  > | **0** | **5** `PolygonSound` | **3** — triangle fan | 15 (`002DEB00`) |
  > | **1** | **5** | **3** — triangle fan | 6 (`002DEA9F`) |
  > | **2** | **5** | **1** — polyline | computed, `002DEA4A lea eax, [rdi + 1]` |
  > | **3** | **2** (`002DE8D2`) | — | — |
  > | **4** | **1** (`002DE8C7`, `ecx` is 1 there) | — | — |
  > | ≥ 5 | the selector itself (`002DE85B`) | — | — |
  >
  > **So `CO-7`'s answer is: modes 1 and 3. Never 0, 2 or 4.** The three `PolygonSound` arms run
  > `… mode … kind = 5` as a common tail at `002DEB0A`/`002DEB14`; selectors 3, 4 and above
  > **`jmp 0x2deb1e`, straight into the epilogue**, so they never reach the kind-5 store.
  >
  > > **A trap worth naming, because I fell into it for a minute.** `002DE800` has exactly **one
  > > `ret`**, which makes it look as though every path ends at the kind-5 tail. It does not: five
  > > arms jump *into the epilogue* and bypass the tail. **Counting `ret`s is not counting exits.**
  >
  > #### The question was partly mis-posed, and the better one is answered (FABLE, 2026-09-22)
  >
  > `CO-7` asks *which mode the shipped **data** uses*. **No data selects a mode.** The mode is a
  > constant in whichever arm the builder takes; what the authored object supplies is the **shape
  > selector** at `+9`. *So the right question is "which shapes does the data declare, and what does
  > the builder map them onto", and the mapping is the table above.*
  >
  > **Three statements above are superseded.** *(1)* “no immediate store of kind 5 exists” —
  > `002DEB14 mov dword ptr [rip …], 5` into `0215E728` is one. *(2)* “the descriptor is built on a
  > caller's stack, not loaded from a file” — the descriptor is a **global**; the stack blocks are
  > its *inputs*. *(3)* “guessing which block is the descriptor would decide `CO-7` on a coin flip”
  > — no guess was needed, because neither block is it.
  >
  > **Bounded, and the bound is measured.** `00221940` has **exactly three call sites**
  > (`00223267`, `002247D4`, `00224EBB`), from a sweep with a planted known positive that reported
  > PRESENT. This answer is the `00224E40` route — **the one this chain already traced**. The other
  > two pass their own `[rsp + 0x60]` (`00223259`) and `r13` (`002247CB`), and **what those carry is
  > not established here.** `002DE800` itself has two callers, `002DEFA0` and `002DF460`, and both
  > `lea` the same global.
  *Narrowed 2026-09-12 (FABLE):* the byte is written once, by `PolygonSound`'s vtable slot 7
  (`007F24F0`, vtable `01CB9F18`), from **byte `+0x24` of a record** whose gate float is `+0x18`,
  vertex count `+0x28` and vertices `+0x30` at 12 bytes each; that record is built on the stack by
  the game-side source builder `00221940` (`0x2e0`-byte factory `007BBFB0` constructs the class for
  kind 5) from a **game-side descriptor** whose shape kind is `+0x18` (1 / 2 / 4 / 5, `002219BF`–
  `002219E0`), polygon mode byte `+0x1C` (`00221A5F`/`00221A70`), vertex count `+0x20` and vertices
  `+0x28` at 16 bytes each (`00221A7B`–`00221AA4`). The descriptor reaches the builder as
  `AudioBank_StartVoice`'s sixth argument (null through the wrapper `00224540`; supplied by
  `00223EB0` ← `0021B200`) or `00224E40`'s fourth (← `0021C760` ← `00211200`); the stream side
  passes null. **No instruction in the image stores the kind 5 as an immediate**, so polygon
  descriptors are copied from data or assembled through registers — the writer of descriptor
  `+0x18` = 5 is the discriminating next read, and the shipped mode value follows from it.
- **What `+0x218` means.** It is set to `0xFFFFFFFF` only when an *edge* wins, never when the
  perpendicular or a vertex wins — so it distinguishes *which feature* was closest, and something
  downstream reads that. `CO-8`.
  *Answered 2026-09-14 (FABLE):* **`+0x218…+0x220` are the vertex indices of the triangle whose face was closest.** The
  face path writes all three (`007F28AE`–`007F28BC`, `007F2A4F`–`007F2A5D`, `007F2C1B`–`007F2C31`). An edge win overwrites
  `+0x218` with `0xFFFFFFFF`, so `-1` marks "the nearest feature was an edge, not a face". Its reader was not traced.
- **Whether the vertex array is one triangle or a fan.** `+0x108` is a general count and the
  plane path uses three vertices at a time; the loop that would iterate triangles is not extracted.
  `CO-9`.
  *Answered 2026-09-14 (FABLE): neither alone — the mode byte chooses.* Mode 2 is a triangle strip, mode 3 a fan and mode
  4 a triangle list, beside a polyline mode (1) and the nearest-vertex mode (0). See the corrected mode table above.

## 8. Falsification pass 1 — 2026-09-13 (OPUS)

*(Static only — an image-wide instruction census over every function body. Nothing executed and no
audio played.)*

### ✖ Withdrawn: "every SIMD vector instruction in the entire executable belongs to this system"

The abstract states a universal over the whole image. It fails under **every** reading of "SIMD
vector instruction", measured over all **38,161** function bodies:

| reading | instructions | functions | in `Sd::Lay`'s range `007BB950`–`007F1F80` |
|---|---:|---:|---:|
| packed **arithmetic** (`mulps`, `addps`, `subps`, `divps`, `sqrtps`, `haddps`, `rsqrtps`, `min/maxps`, and the `pd` forms) | **2,585** | **235** | **29** |
| packed shuffle / unpack | 5,069 | 530 | — |
| packed logical (`andps`, `xorps`, `orps`, `andnps`) | 6,199 | 2,479 | — |
| packed 16-byte moves | 83,763 | 4,294 | — |

**Even on the strictest reading the claim is out by a factor of twenty**, and the counter-examples
are not obscure: `00398F90` and `0039ABF0` — the **transform workbench's** point transform and its
`w`-returning twin — both carry `mulps`, as do `003970F0` (×7 — interior read 2026-09-17,
SWE2-FRONTIER: a pure SIMD body, no calls, staging vectors into the `022D932C`–`022D9370`
global block from `01EF93F0` at [`003970FA`](../_index/ADDRESS-INDEX.md), stores at
`00397126`–`00397186`), `0039AFA0` (×4 — interior read 2026-09-17, SWE2-FRONTIER:
1,444 B of scalar `mulss`/`addss` (×49 each) over `movaps`/`movups`, no calls, reads the
`02AEE7F0` table at [`0039AFAF`](../_index/ADDRESS-INDEX.md) and accumulates into the
`022D91A0` block), `00397B50`,
`00398030` and the rest of the `0039xxxx` transform run. `002F0280` carries **eleven** (interior read
2026-09-17, SWE2-FRONTIER: `0022CC20` ×3 + `002EFE70` ×2 + `sqrtf` + one UI-shared leaf, first call at
[`002F041E`](../_index/ADDRESS-INDEX.md) — a transform/processor hybrid). Those are
Presentation, and they are exactly the functions a reader would reach for after
[the position-to-scalar node](../17-Presentation-Rendering/Position-To-Scalar/how-a-position-becomes-a-single-number.md).

**The true statement in the neighbourhood is much smaller**: the `Sd::Lay` range holds **29** of the
235 packed-arithmetic functions. Spatial audio certainly does vector maths; it does not own it.

### ⚠ The "12 SIMD-bearing functions" denominator is not reproducible either

§2's own warning — *"this table accounts for 4 of the 12 SIMD-bearing functions"* — is the right
kind of caution, but **12 matches none of the four censuses above**, and the page does not say
which instruction set or which address range produced it. It should state its instrument.

### ✔ But one narrow claim in this neighbourhood is true, and it is the interesting one

**`sqrtps` — packed square root, the operation a distance-per-lane calculation needs — occurs
14 times in the whole image, in exactly six functions, and all six are inside the audio
cluster**: `007F0320`, `007F0820`, `007F1340`, `007F1670`, `007F1A50`, `007F25E0`. Three of
them fall inside §2's own class ranges (`007F1340` and `007F1670` in `DynamicSound`, `007F1A50`
at the end of `PointSound`), and **not one lies outside `007F0320`–`007F25E0`**.

So the abstract was reaching for something real and overshot it. **Packed square root belongs
to this system; packed arithmetic does not** — the workbench multiplies vectors all day without
ever taking a packed root, because a transform needs `mulps` and a distance needs `sqrtps`.

### ⚠ Narrowed 2026-09-13 (OPUS, `OPUS-COMPOSER-QUATERNION`): a census of one instruction

The `sqrtps` figures above are unchanged and still correct: **14 instructions in exactly six
functions, all inside `007F0320`-`007F25E0`.** What is narrowed is the reading they invited.

I wrote that *"packed square root belongs to this system even though packed arithmetic does not"*.
That is a claim about **`sqrtps`**. It does not extend to square roots as an operation - and the
counter-example was found the same week, in
[animation channel binding](../22-Middleware-PhyreEngine/Animation-Channel-Binding/animation-channel-binding-and-transform-composition.md)
section 12: `005C72A0` takes a square root **every time it normalizes a quaternion**, at
`005C7481 call 0x861F14`, and `00861F14` is a six-byte import thunk named **`sqrtf`**. That is
animation middleware, not audio, and **no instruction census would ever see it**, because the
operation is a call.

**So the honest form of the claim is narrower and still worth having:** among functions that do
square roots *four lanes at a time*, all six are this system's. Scalar square roots are taken all
over the image through the CRT, and this page's instrument cannot count them. The same caution
section 2's warning already needed - *state which instruction set and which range produced the
number* - applies to the number I added.

**What this does not touch.** The class family, the nine `SQEX::Sd::Lay::*` names, the 39 recovered
virtual methods and the per-class contiguous ranges were **not re-derived here** — this pass tested
one sentence, the one that quantifies over the whole executable. `CO-10` stands. Everything from
§3 on is **unread by this pass**. Nothing was executed.

## Residual placements — 2026-09-14 (SWE2-FRONTIER, residual-placement package)

| function | size | role (call-signature read) |
|---|---:|---|
| `002F67C0` | 739 | spatial-audio body (caller `002F5550`): `002330D0` then `00861F14` — two-call shape over its own argument setup |

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

Both crossings enter this document with the `CO-7` call chain in §What is not known, and both are
calls **out** of bodies this page names; nothing in the spatial-audio object model is reached from
either layer.

**Platform — SERVICE (2 edges).** `00223190` and `00224570`, two of `00221940`'s three callers, each
call `FUN_005CC930`, owned by that layer. It is a **high-resolution counter read**: it calls the
import at `008C2188`, converts the unsigned 64-bit result to `double` and applies the `2^64` fixup
from `00D27A68` when the value is negative (`005CC947`–`005CC959`). The crossing is that one call,
not a shared responsibility, and the render-command-list page accounts for the same callee the same
way. Read from the shipping bytes 2026-09-15 (FABLE).

**Party — READ-ONLY GETTER (1 edge).** `0046CC70`, one of the four bodies that originate a descriptor (interior read 2026-09-17, SWE2-FRONTIER: 1,069 B — `00237420` first at [`0046CCAE`](../_index/ADDRESS-INDEX.md), `004FE270`/`00421E20`/`002EDBD0` ×2),
calls `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`), owned by Party. It is **7 bytes** — a
packed actor handle read, nothing more — so a sound source asks who the party's focus actor currently
is. No write, and no Party state is owned here. Read from the shipping bytes 2026-09-15 (FABLE).

**Save_Load_Settings — MECHANICAL (3 edges).** `00225580`, one callee named inside the
`00224E40`/`002251B0` descriptor-forwarding sections (batch 16, SWE2-EC7), is itself called by
three bodies filed under Save_Load_Settings — `005812B0`, `005817D0`, `00581930`. The crossing
is a shared callee at one remove: this page uses `00225580` only as an audio descriptor
forwarding target and owns nothing of what the settings layer calls it for.

**CombatFormula — CLIENT (1 edge).** `002DF220`, the bit-30-clear decode path this page's
`003A0E20` section names, is also called by `003112F0`, a CombatFormula-layer body - one
shared decode routine; the formula call is that layer's business.

**Rewards_Progression_Economy — CLIENT (1 edge).** The same `002DF220` is called by
`0030C650`, a Rewards-layer body - the same shared decode at one remove; nothing of the
rewards call is owned here.
- **CoreRuntimeScheduling - CLIENT and SERVICE (3 edges).** `001A9930`, `003603C0` are also called by bodies filed to core runtime scheduling: `0017D6E0`, `0022A770`; `003B99D0` reaches bodies filed to core runtime scheduling: `001EDDA0` - shared machinery across the layer boundary, no shared ownership.
- **Gameplay - CLIENT (1 edge).** `00203170` is also called by bodies filed to gameplay: `00339630` - shared machinery across the layer boundary, no shared ownership.
- **Movement - CLIENT and SERVICE (28 edges).** `00203170`, `00202C70`, `00230790` are also called by bodies filed to movement: `00230790`, `00338490`, `0022EF20` (+18 more); `002F5550`, `002330D0`, `002F4520` reach bodies filed to movement: `0026E5F0`, `00233050`, `0026E5D0` (+1 more) - shared machinery across the layer boundary, no shared ownership.
- **Presentation - CLIENT and SERVICE (376 edges).** `00398F90`, `002ED570`, `00398030` are also called by bodies filed to presentation/rendering: `0046CC70`, `003E4CB0`, `00417F40` (+268 more); `002F4520`, `002F5550`, `003E5B30` reach bodies filed to presentation/rendering: `002EDBD0`, `003E55F0`, `00180650` (+20 more) - shared machinery across the layer boundary, no shared ownership.
- **Resource - CLIENT and SERVICE (36 edges).** `002ED570`, `00409F50` are also called by bodies filed to resource: `00409CA0`, `00409D60`, `00409F50` (+6 more); `00409FE0`, `00409CA0`, `00409D60` reach bodies filed to resource: `002ED570`, `0051FE30`, `003B37E0` (+12 more) - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (6 edges).** `003A0E20`, `00203170`, `002DEF40` are also called by bodies filed to script VM / native bridge: `00356160`, `00346990`, `00357040` (+3 more) - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT (16 edges).** `00203170`, `00202C70`, `00225580` are also called by bodies filed to UI: `002D2600`, `002D28E0`, `003F26F0` (+8 more) - shared machinery across the layer boundary, no shared ownership.
## Interior citation — frontier hub `00421E20` (2026-09-18, SWE2-EC7)

`00421E20` — 458 B, 21 callers (5 A-measured; `0046CC70` already interior-read above); the
handle→sub-record→opcode-resolve property getter. Interior verified: `[rcx+0x18]` is the
persistent index (`-1` = absent, checked four times), `0020E600([rcx+0x10])` resolves the owner
([`00421E55`/`00421EEF`](../_index/ADDRESS-INDEX.md)), `[rax+0xD98]` is the paged table and
`002ED570` — the two-level paged accessor measured in batch 1 — indexes it by `ebp`
(`00421E6C`). The `bx` selector `0x107`/`0x108` is remapped to the record's `[+0x2F4]`/`[+0x2F6]`
words (`00421E7D`–`00421E9A`); `bx - 0x300` inside `[0, 0xFF]` takes the `003E5B30` lookup
(`00421ECA`); a second resolve then runs `003710E0` with the out-block
([`00421F2A`](../_index/ADDRESS-INDEX.md)) — the descriptor's named-parameter read.

### Crossing — Resource (batch-8 hub exposure)

Naming `002ED570` (the paged-table accessor `00421E20` uses) exposes its Resource-domain
caller set on this page: `00409CA0`, `00409D60`, `00409F50`, `00409FE0`, `0046E1B0`,
`004780B0` all index through it, and `00409660` sits on the same accessor's callee side via
`002EDBD0`. These are Resource-table consumers sharing the two-level index idiom — the
audio descriptors borrow the accessor; they do not own the table.

## SWE2-EC7-23 update (2026-09-18) — `004FE270` packed-field float lookup

`004FE270` (122 B) is the packed-field decoder the descriptor builders call:
`edx >> 0x10` byte compared against `byte[r8+0x32]` (a bound check), `edx >> 8`
byte indexing the `[01F265B0]` float table; `edx >= 0x20000000` selects the
`-1.0f` constant at `01CEBC9C`, and the continuation decodes `edx >> 0x18 &
0x1F` — a bit-packed parameter field expanded to its table float. Interior
anchor `004FE27A` (the high-byte extract). The Party crossing already names it
inside `0046CC70`'s descriptor build.

## SWE2-EC7-34 update (2026-09-19) - `00397B50`

`00397B50` (887 B) is the call-free spatial transform - two vec4 blocks `[rcx]`/`[rdx]` staged into `022D9300`-`022D9350`, `shufps`/`mulps`/`addss` rows writing `022D91A0`-`022D935C`. Interior anchor `00397DB4` (a `022D91A0` `movups` store).

## SWE2-EC7-35 update (2026-09-19) - `002F67C0`

`002F67C0` (739 B) is a spatial-audio object body - `00902EEC`/`01CEBBA8`/`008F3110`/`008F30E4`/`008F30F4` rdata run, `00861F14`/`002330D0`. Interior anchor `002F67F0` (an `00861F14` call).

## SWE2-EC7-35 update (2026-09-19) - `00230790`

`00230790` (688 B) is a spatial-audio sibling - `00908E30`/`022D91B0`/`01CEBBA8`/`01CEBB70`, three `00861F14` plus `00203170`/`00202D70`/`00202D50`/`00202C70`. Interior anchor `00230836` (an `00861F14` call).

## SWE2-EC7-38 update (2026-09-19) - `0039ABF0`

`0039ABF0` (489 B) is a call-free spatial-audio matrix compute - `shufps`/`mulps`/`addss`, writing `022D91A0`/`022D9300`; the `00397B50` family's sibling. Interior anchor `0039AC1E` (the `022D9300` store).

## SWE2-EC7-41 update (2026-09-19) - `003E5B30`

`003E5B30` (338 B) is a spatial-audio body - `00422D50`/`0041C970`/`003E6DA0`. Interior anchor `003E5B4D` (a `00422D50` call).

## SWE2-EC7-48 update (2026-09-19) - `00224E40`

`00224E40` (203 B) is the descriptor-forwarding audio body - `00221940`/`00221D60`/`00222050`/`00224C40`/`00225580`/`00225590`/`002256E0`. Interior anchor `00224E69` (a `00221940` call).


## SWE2-EC7-64 update (2026-09-19) - `005817D0`

`005817D0` (142 B) is a Save_Load_Settings-filed audio body - `00225580`/`0029F4B0` plus `02CA99C8`. Interior anchor `0058181C` (a `00225580` call).



## SWE2-EC7-65 update (2026-09-19) - `0021B200`

`0021B200` (134 B) is a spatial-audio stream body - `00212950`/`00223EB0`. Interior anchor `0021B231` (a `00212950` call).


## SWE2-EC7-67 update - `0021C760`

`0021C760` (128 B) is a spatial-audio body - `00212950`/`00224E40`. Interior anchor `0021C7A1` (a `00212950` call).

## SWE2-EC7-73 update (2026-09-19) - `003A0E20` encoded-index dispatch measured

`003A0E20` (41 B) is the two-way index dispatch the audio bodies call:
`ecx == -1` returns 0; `bt ecx, 0x1E` set splits `cl`/`ecx>>8` and
tails ~~`002DF4D0(cl, cl>>8, edx, r8d)`~~ `002DF4D0((ecx >> 8) & 0xFF, ecx & 0xFF, edx, r8d)` *(corrected 2026-10-01, OPUS: `003A0E3C movzx ecx, cl` after `shr ecx, 8` is the first argument, `003A0E30 movzx edx, cl` the second)*, clear tails `002DF220` - the
bit-30 selected decode path.
Interior anchor `003A0E2A` (the `bt ecx, 0x1e` test).

## SWE2-EC7-74 update (2026-09-19) - `003617B0` constant record copy measured

`003617B0` (83 B) is the descriptor copy the audio bodies share: four
`movaps` rows `022CBAB0`..`022CBAE0` land at `r9 + 0`..`+0x30`, byte
`022CBA94` at `+0x19`, and two stack floats at `+0x1C`/`+0x10` - the
canned audio record with two caller overrides.
Interior anchor `003617BE` (the first `movups` store).

## SWE2-EC7-75 update (2026-09-19) - `002DEFA0` + `002DEF40` gated audio tails measured

`002DEFA0` (104 B) is the `003603C0`-gated two-call chain: the gate
failing returns 0; otherwise `002DE800(rsi, rdi)` runs, then
`001DBE00` tails with `ecx = !(ecx >> 31)`, `edx = ecx & 0x7FFFFFFF`,
`r8 = 0215E710` - the sign-bit split the audio bodies share.
Interior anchor `002DEFD8` (the `002DE800` call).

`002DEF40` (95 B) is the sibling repack: same `003603C0` gate to 0,
then `001DBDB0` tails with `ecx = !(ecx >> 31)`, `edx = ecx &
0x7FFFFFFF`, `r8d = sil & 0xFF`, `r9d = edi & 0x7F` - the masked-arg
variant.
Interior anchor `002DEF9A` (the `jmp 001DBDB0` tail).

## SWE2-EC7-81 update (2026-09-20) - `00361CF0` ramp-frame setup measured

`00361CF0` (239 B, stack-cookie) is the constant-block frame builder
`00337410`'s callers drive: `022CBAB0`/`022CBAC0`/`022CBAD0`/
`022CBAE0` copy 64 B of constants into the frame, `xmm3` and the
`+0x6C` argument join `01CEBC9C`/`00D10C90`/`022CBA8C` floats, and
`00361810(&frame, rdx = 022CBB00, r9)` executes; then `dword[rbx]`
is rescaled through the `0x81020409` reciprocal multiply with a
`>> 6` signed fixup - the fixed-point divide.
Interior anchor `00361DA3` (the `00361810` call).

## SWE2-EC7-83 update (2026-09-20) - `0046C8D0` volume clamp measured

`0046C8D0` (18 B) is the 7-bit clamp the audio callers share:
`ecx` capped at `0x7F`, then floored at 0 - `min(max(ecx,0),0x7F)`,
call-free.
Interior anchor `0046C8D7` (the `cmovg` cap).

## SWE2-EC7-112 update (2026-09-20) - `00180320` measured

`00180320` (70 B) is the
flag-forwarding poke
`002F4520` and `002F5550`
run: a live `001A9930()`
object is required, then
`byte[00189120() + 0x1C]` is
read as a boolean and passed
to `001A7600(obj, flag, ecx)`
as the middle argument - the
second singleton's flag byte
gates the first's call.
Interior anchor `0018035B`
(the `001A7600` tail).

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../_index/candidates/fable-the-spatial-audio-object-model-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `001A7600` | 41 B | loads qword `+0x88` of `rcx` and returns 0 when it is null, when `r8d` is negative (`js`) or when `r8d` is not below dword `+0x20` (signed `jge`); otherwise returns the qword at index `edx + r8d*2` (both sign-extended, stride 8) of that array | `001A760A`, `001A760F`, `001A7611`, `001A7621`, `001A7626` |
| `001DBE00` | 58 B | calls the callee at `001DBE00` + 0x16 with the incoming `rcx`, `rdx` and `r8` unchanged, then tail-jumps the callee at `001DBE00` + 0x35 with `rcx` = that call's result, `edx` = the incoming `ecx`, `r8d` = the incoming `edx` and `r9` = the incoming `r8` | `001DBE16`, `001DBE1B`, `001DBE21`, `001DBE35` |
| `00223EB0` | 35 B | calls the callee at `00223EB0` + 0x19 with `rcx`, `rdx` and `r8` passed through, `r9d` = 0, the fifth (stack) argument the dword 0, the sixth the byte 1 and the seventh the incoming `r9`, and returns its result | `00223EB4`, `00223EB9`, `00223EBC`, `00223EC1`, `00223EC9` |
| `0026E5D0` | 31 B | returns 0 when qword `0209A670` is zero; otherwise returns the bitwise NOT of qword `0209A6C0` AND qword `0209A6C8` | `0026E5D8`, `0026E5E1`, `0026E5E4`, `0026E5EC` |
| `0041C970` | 42 B | walks the sign-extended word `+0x28` of `rcx` records of 0xA0 bytes starting at `rcx + 0x30` and returns the address of the first whose dword `+0x80` equals `edx`; returns 0 when the count is not positive or no record matches | `0041C97F`, `0041C981`, `0041C98C`, `0041C995`, `0041C997` |

## Homed frontier bodies called from this page's functions (FABLE, 2026-10-02, cloud-drafted)

*Functions no page cited until now. Each is entered directly from a function this page already cites (the site is given as caller + offset). Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's homing pack and re-read by FABLE against the certified image; verified by [`homing_applier.py`](../_index/candidates/fable-home-the-spatial-audio-object-model-1002/homing_applier.py): every site transfers to its function, the page cites the caller, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors |
|---|---|---|---|---|
| `00210BE0` | 30 B | `001DBE00` + 0x35 | moves the arguments down one place (`edx` = `r8d`, `r8` = `r9`) and, when the incoming `edx` is zero, tail-jumps (`00210BE0` + 0x10) with `rcx` = qword `rcx+8`, otherwise tail-jumps (`00210BE0` + 0x19) with `rcx` = qword `rcx+0x10` | Interior anchor `00210BE3`; Interior anchor `00210BE7`; Interior anchor `00210BF0`; Interior anchor `00210BF9` |
| `002DF280` | 17 B | `003A0E50` + 0x25 | returns 0 when `ecx` is -1; otherwise sets bit 31 of `ecx` (`bts`) and tail-jumps (`002DF280` + 0xC) with the other arguments unchanged | Interior anchor `002DF283`; Interior anchor `002DF285`; Interior anchor `002DF288`; Interior anchor `002DF28C` |

## Homed bodies re-homed here for host fit (FABLE, 2026-10-03; move drafted by OPUS)

*Each body below was homed on another page by FABLE's homing stream (cloud-drafted, FABLE-verified). SWE2-AUDIT-SPEC reviewed its sentence, site and anchors exact, and rejected only the host: that page cites the caller as a foreign or boundary mention (commit `4522aeff6`). The row is moved here because this page cites the caller in its own text. The sentence is unchanged except where `moves.json` records a bits-as-values edit. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Verified by [`move_rows.py`](../_index/candidates/opus-fable-home-host-moves-1003/move_rows.py): every site transfers to its function, this page cites the caller outside this section, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors | moved from |
|---|---|---|---|---|---|
| `002DEF20` | 17 B | `00332C40` + 0x320 | tail-jumps (`002DEF20` + 0xC) with 1 in `ecx`, the incoming `ecx` in `edx`, 0 in `r8d` and the incoming `edx` in `r9d` | Interior anchor `002DEF23`; Interior anchor `002DEF28`; Interior anchor `002DEF2C` | [CONTRACT-world-simulation-tick](../00-Engine-Core-Runtime/Battle-Frame/CONTRACT-world-simulation-tick.md) |
| `002DF1A0` | 56 B | `003B99D0` + 0x2EE | when `edx` is zero, tail-jumps (`002DF1A0` + 0x18) with 1 in `ecx`, the incoming `ecx` in `edx`, 0 in `r8d` and the incoming `r8d` in `r9d`; otherwise calls `002DF1A0` + 0x2E with 1 in `ecx`, the incoming `ecx` in `edx`, 0 in `r8d`, the incoming `edx` in `r9d` and the incoming `r8d` as the fifth (stack) argument, and returns its result | Interior anchor `002DF1A6`; Interior anchor `002DF1B8`; Interior anchor `002DF1BD`; Interior anchor `002DF1CE` | [CONTRACT-world-simulation-tick](../00-Engine-Core-Runtime/Battle-Frame/CONTRACT-world-simulation-tick.md) |
