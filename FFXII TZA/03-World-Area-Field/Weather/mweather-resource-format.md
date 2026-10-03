---
system: MWeather authored resource format
category: 03-World-Area-Field
status: DOCUMENTED
owner_layer: PrimaryOwner:WorldAreaField (resource) / Presentation (consumption)
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
  previous_parent: 381d2aea82b96d7af781844e191d9b92a37e93bd2d4ff276a33ba56e7307461b
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-02
archive_formats:
  - "GRMI | explained | gramap_weatherinfo.bin (.bin member): {GRMI01, u16 count at +6 = 776, 9-bit packed (selector, slot) records from +8} - read by 003777C0 (bit base 9*(3*selector+slot)); corpus decode D-7"   # <- corrected 2026-10-02, OPUS - with a zero-based slot; the callers pass 1..3 and 003777C0 subtracts 9 (003777F9 lea r10d,[r9-9]), so the entry is 3*selector + slot - 1
audit:
  passes: 1
  last_pass: 2026-09-02
  last_pass_state: reverification-against-current-parent
  crossref_clean: true
  reopened_count: 1
---

# MWeather authored resource format

> A packed 9-bit-per-entry authored table that decides both what the weather *looks* like and
> what it *does* to combat.

## 1. What the player sees

Which visual weather preset a zone shows in each of its three Weather Slots, which direction
the environment is oriented, and - through the gameplay class - whether strong-wind combat
effects are active.

## 2. Native mechanism

The executable contains the literal authored resource name **`MWeather`**. Its loader binds
the resource and `00378F70` publishes the loaded pointer into WorldAreaField weather-resource
state.

All three field extractors share one packed-bit reader, `003777C0`, with effective bit base:

```
9 * (3 * selector + weatherSlotIndex)   <- corrected 2026-10-02, OPUS: for the 1..3 slot the callers pass it is 9 * (3 * selector + slot - 1) - 003777E9 lea eax,[rcx+rcx*8], 003777F9 lea r10d,[r9-9] (CONTRACT-weather.md I-4)
```

where `selector` is a MapRef-derived value. **9 bits per (selector, Weather Slot) pair.**

| Wrapper | Bits | Width | Meaning |
|---|---|---:|---|
| `00377850` | 0..2 | 3 | Presentation backend preset / mode, `0..7` |
| `003777A0` | 3..6 | 4 | azimuth / orientation sector, 16 sectors |
| `003777B0` | 7..8 | 2 | elevation / orientation class |

### Presentation consumption

`0040AAD0`:
- **bits 0..2** select backend preset `0..7` via `0040B3B0`;
- **bits 3..6** select one of 16 azimuth sectors, each `pi/8` = **22.5 deg** apart;
- **bits 7..8** select an elevation base: `0` -> 0 deg, `1` -> +30 deg, other -> -30 deg;
- both angles receive a receiver-local procedural perturbation of about `+/-0.15 rad`
  (**+/-8.59 deg**) from the shared render PRNG;
- `0040B430` normalises and publishes the resulting basis.

The only identified high-level consumer of that basis is `0040FF30`, a large embedded
Presentation visual evaluator.

#### What `0040B430` actually publishes — EXP-129, adopted 2026-09-20 (OPUS)

**It publishes two vectors, and the second is built from the first.** The page has called this
"normalises and publishes the resulting basis" since it was written; the executed record
([`EXP-129-vec3-normalize-exec.md`](../../_experiments/EXP-129-vec3-normalize-exec.md),
SWE2-ORACLE) reads the body, and the shape is a **frame**, not a pair of independent directions:

| | published to | what it is |
|---|---|---|
| **stage 1** | `02CA43A0`..`+0xC` | `dir = v / \|v\|` — the caller's vector, normalised |
| **stage 2** | `02CA43B0`..`+0xC` | `normalize({0, 1.0f, ~1e-5f} × dir)` — the cross of an
almost-exactly-up reference with that direction |

That is the standard construction of an orthonormal frame from **a direction plus a world-up
reference**, and the odd third component of the up vector is the **degeneracy guard**: a cross
product with a purely vertical `dir` would vanish, and the tilt keeps it finite.

**The guard is sized, not arbitrary, and the two constants live in different cells.** Measured
here rather than taken from the record: the gate epsilon is `d[0x908E10]` = `0x358637BD` = **1e-6f**
and the tilt is `d[0xD108A0]` = `0x3727C5AC` = **1e-5f** — **exactly ten times the epsilon**. For
the worst case `dir = {0, 1, 0}` the cross is `{−1e-5, 0, 0}`, whose length is ten times the gate,
so stage 2 divides rather than zeroing and publishes `{−1, 0, 0}`. The vertical case survives with
a full decade of margin.

**Both stages gate on the same predicate, and equality divides.** `0040B4A6`
`comiss xmm11, xmm1` / `jbe` and `0040B561` `comiss xmm11, xmm0` / `ja` are the *same* test in
opposite branch polarity: scale is `1/len` whenever `len >= eps`, and `0` only when `len < eps`
strictly. A NaN length makes `comiss` unordered, which sets `CF` and `ZF`, so **both** stages take
the divide arm and a NaN component produces all-`0x7FC00000` published vectors — it never reaches
the zero arm. `len² = inf` gives `len = inf`, `s = 0`, and both published vectors are **zero, not
NaN**.

> **A contradiction inside the record, resolved against the image.** EXP-129's *Measured semantics*
> says the two gates are asymmetric, *"so `len' == eps` takes the divide path in stage 2 but not
> stage 1"* — while its own *Execution findings* item 3 says the `b430-eps-edge` case **proves the
> `jbe` boundary includes equality (s = 1/eps)**. The second is right and the first is a slip:
> `comiss eps, len` sets `ZF` on equality, `jbe` is `CF|ZF`, so stage 1 divides at equality exactly
> as stage 2 does. Only the branch polarity differs. Raised with the record's author; the finding
> is adopted here in the form its own execution evidence supports.

**`0040DB70` is the reset entry**: it clears `b[0x2CA4390]`, builds the seed vector
`{1.0f, 0, 0}` on its own stack and calls `0040B430` with it — so the published frame after a
reset is the world X axis and its tangent. **The `w` lane is dead end to end**: the caller's
`v[+0xC]` is copied into the local, `00202E10` overwrites it with `0`, and `0040DB70` never writes
it at all.

**`00202E10` is alias-safe.** It computes the cross into stack temporaries and copies all sixteen
bytes with one `movups`, so `dst == src` is legal — which is what lets `0040B430` cross the local
with the published `dir` straight back into the same local.

### Gameplay consumption

`0026D910` extracts the same 3-bit preset **before** the Presentation refresh and collapses it:

| Preset | Gameplay class |
|---:|---:|
| 0 | 0 |
| 1..3 | 1 |
| >= 4 | 2 (**strong wind**) |

Stored at `02099DAC`, read by CombatFormula. **MWeather is therefore not purely visual.**

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `00378F70` | MWeather resource publisher | 10 B | binds loaded resource |
| `003777C0` | packed bitfield reader | 144 B | shared by all three extractors |
| `00377850` | preset extractor | 14 B | bits 0..2 |
| `003777A0` | azimuth extractor | 15 B | bits 3..6 |
| `003777B0` | elevation extractor | 15 B | bits 7..8 |
| `0040AAD0` | Presentation backend init | 286 B | consumes all three |
| `0040B3B0` | preset selector | 118 B | 0..7 |
| `0040B430` | basis normalise/publish | 416 B | |
| `0040FF30` | embedded visual evaluator | 5,919 B | sole identified basis consumer; interior verified 2026-09-17 (SWE2-FRONTIER): `0020E600` row-lookups ×60 (first at [`0040FF4F`](../../_index/ADDRESS-INDEX.md)), `0036DD80` ×4, `003D8E50` ×2, `sqrtf` ×4 — a per-row evaluate loop |
| `00263E20` | gameplay class getter | 7 B | reads `02099DAC` |

## 4. Data structures

```
MWeather packed record
  9 bits per (MapRef-derived selector, Weather Slot) combination
  bitBase = 9 * (3 * selector + weatherSlotIndex)   <- corrected 2026-10-02, OPUS: 9 * (3 * selector + slot - 1) for the 1..3 slot the callers pass (003777F9 lea r10d,[r9-9]; CONTRACT-weather.md I-4)

    bits 0..2   u3   presentation preset / mode      0..7
    bits 3..6   u4   azimuth sector                  16 x 22.5 deg
    bits 7..8   u2   elevation class                 0 -> 0 deg, 1 -> +30 deg, else -30 deg
```

## 5. Call chain

```
MWeather resource load
  -> 00378F70 publish into WorldAreaField weather-resource state

apply path
  -> 0026D910
     -> extract preset -> collapse -> 02099DAC   [GAMEPLAY]
     -> 002E3D40 (zero mode)
        -> 00377850 / 003777A0 / 003777B0
           -> 0040AAD0                            [PRESENTATION]
              -> 0040B3B0 preset
              -> 003D8E50 x2 perturbation
              -> 0046D160 / 0046D200 rotation
              -> 0040B430 normalise/publish
                 -> 0040FF30 visual evaluator
```

## 6. Modding notes

- **MWeather edits change gameplay, not just looks.** Any preset change crossing the
  `>= 4` boundary flips strong-wind combat effects on or off.
- The *selector* is MapRef-derived, so the same Weather Slot can look and behave differently
  per area - that is intended.
- **XIIOnline:** the resource itself is not network authority, but its gameplay projection
  means every client must agree on the authoritative Weather Slot and area before local
  combat prediction is trustworthy. Clients running different MWeather data can disagree on
  damage even with the same slot - version-fence it if previews must match.

## 7. What is not known

- [x] ~~Authored/designer name of the MapRef-derived selector (open question **D-1**).~~ **Closed
      2026-09-12 (FABLE): not in the image.** The selector is the word `+0` of the field's 8-byte row
      in the map-reference table `[02099D88]` (`MapRef_GetPrimaryFieldValue`, `00264F29`–`00264F39`),
      a header-offset file image that `MapRef_BeginLoadResources` (`00268750`) requests at bootstrap
      as loader id 9, ~~kinds 4 and 2~~ kind 4 (`00268803`–`00268809`; the kind-2 request at `0026880E`–`0026883E` is a second file, `test_area_ref.bin`, kept at `02099D98`) *(corrected 2026-10-02, OPUS: `002687CF` stores the kind-4 buffer at `02099D88` and `00268829` the kind-2 buffer at `02099D98`; choosing-the-field-environment-variant.md, the two test_ siblings)*, and that carries no column names; the
      authoring tool's grammar names only `weatherProbability` on the script side. The mechanism —
      selector × Weather Slot → the 9-bit packed record — is fully read (§2, §4); the designer's
      label for the selector is not recoverable from the shipped data and the row is retired as a
      naming residue, not a blocker.
- [x] ~~Whether authored elevation value **3** is ever emitted (open question **D-7**).~~ **Never,
      by either source — measured 2026-09-12 (FABLE).** *Mode 0 (the table):* the shipped
      `gramap_weatherinfo.bin` (`GRMI01`, count word `+6` = **776** selectors, bits from `+8`,
      2,620 bytes for the 2,619 the 776 × 27 bits need; the `ch` and `in` copies are byte-identical
      and no `us` copy ships) decoded with `003777C0`'s own rule — bit base `9 × (3 × selector +
      slot)` with the slot zero-based *(corrected 2026-10-02, OPUS: the callers pass `1..3` and `003777C0` takes the 9 bits back off, `003777F9 lea r10d, [r9-9]`; CONTRACT-weather.md I-4)*, `width` bits read most-significant first — gives, over all 2,328 (selector, slot)
      entries: elevation **0 × 1,865, 1 × 214, 2 × 249, 3 × 0**; presets 0 × 1,180, 1 × 550, 2 × 420,
      4 × 153, 5 × 24, 6 × 1 (3 and 7 never); 391 selectors carry any non-zero field. *Mode 1 (the
      verb):* all **174** `setmapwind` calls in the 1,114 shipped scripts push immediates, and the
      elevation argument — the last pushed, first popped — is **0 in every one** (presets 0 / 2 /
      3 / 5, azimuths 0–15). So the `+30°` arm is reached only from the table's 214 entries, the
      `−30°` arm from its 249 value-2 entries, and value 3 — which would also select `−30°` — is
      unauthored everywhere. Tally file: `Tools/work/FABLE/bf3-scratch/gramap_weatherinfo-in-2026-09-12.bin`.
- [x] Physical meaning of the published basis - do **not** call it sun/sky/fog/light
      direction without stronger proof (open question **D-9**). *Rebound 2026-09-26 (FABLE, Claude Opus 5.5): this
      box cited D-4 until then. D-4 is a different vector, the direction at `02CB8420` that the render-frame descriptor carries, and
      it was answered that day as the scene light (the map and cutscene JSON's `lightOrientation`/`lightHeight`). This
      basis is built from the MWeather selector's azimuth and elevation (§3). Only `0040FF30` reads it
      (`00410083`/`0041008A`), and neither of the scene loaders writes it, so the D-4 answer does not carry over.*
      **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): it is the map's wind direction, the frame the model-sway
      oscillator swings along.** Two facts, each read:
      - **It is authored as wind.** The script sets the three fields it is built from with `setmapwind(elevation,
        azimuth, preset)` and restores the table's values with `defaultmapwind` (§ "The script interface").
      - **Its only reader is the sway.** `0040FF30` is the heavy stage 1 of
        [the per-model oscillator](../../17-Presentation-Rendering/Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md),
        the controller that keeps cloth, hair and hanging gear moving. It loads the direction and the tangent into
        VU0 registers vf3 and vf4 (`022D91D0`/`022D91E0`) and scales them by samples from its oscillation table.
      - *Not claimed:* that anything besides the oscillator reads the basis through another route, or what the
        preset field selects.
      ***NARROWED, NOT ANSWERED, 2026-09-20 (OPUS) from EXP-129.** What the pair IS is now read:
      `02CA43A0` is the normalised direction and `02CA43B0` is `normalize({0,1,~1e-5} × dir)`, so
      the two are **a direction and the tangent axis of an orthonormal frame built from it against
      a world-up reference** - see the subsection in §3. That is a statement about the
      CONSTRUCTION and it still does not name the thing: a frame built from a direction plus up is
      what you build for a sun, for a fog gradient, for a wind field or for a billboard basis
      alike, and the azimuth/elevation inputs that feed it are equally neutral. The one thing it
      does rule out is reading the second vector as an independent second direction. Naming it
      still needs `0040FF30`, the sole identified consumer, read - which is where this question (D-9 since
      2026-09-26) has always pointed.* *(answered: see the ANSWERED 2026-09-26 note above — the map's wind direction, read through `0040FF30`; 2026-10-02, OPUS)*

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Resource is named `MWeather` | literal authored resource name in the executable + exact loader/publisher topology | 2 |
| 9-bit packed layout and bit base | complete body of `003777C0` (144 B, `a3688ce2...cd2e`) and the three wrappers | 1 |
| Presentation preset/azimuth/elevation semantics | complete body of `0040AAD0` (286 B, `ace98b94...dd9b`), literal `pi/8`, +/-30 deg branches | 1 |
| Elevation 3 is never authored; the table's field populations | `gramap_weatherinfo.bin` (776 selectors) decoded with `003777C0`'s bit rule; the 174 `setmapwind` calls over 1,114 scripts | data (2026-09-12) |
| Preset -> gameplay class collapse | complete body of `0026D910`; store to `02099DAC`; getter `00263E20` | 1 |
| Class 2 = strong wind effects | `0038B220` applies Fire x1.2, Water x0.5, Wind x1.2 when `02099DAC == 2` | 1 |

## 9. Related

- [`weather-apply-and-environment-materialization.md`](weather-apply-and-environment-materialization.md)
- [`../../08-Combat-Formula/Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md`](../../08-Combat-Formula/Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md)

## Re-verification 2026-09-02 (AH-1)

Stamped against parent `381d2aea...`; re-checked against the current `2ed8affb...`.

**Addresses:** 16 cited, **16 resolve as function entries**, 0 unresolved
(`verify_doc_addresses.py`).

**Central claim re-derived.** The headline is *"a packed 9-bit-per-entry authored table"*. The three
extractors were decompiled fresh:

```c
FUN_00377850(a, b) -> FUN_003777C0(a, b, 0, 3);   // bit offset 0, width 3  -> bits 0..2
FUN_003777A0(a, b) -> FUN_003777C0(a, b, 3);      // bit offset 3           -> bits 3..6
FUN_003777B0(a, b) -> FUN_003777C0(a, b, 7);      // bit offset 7           -> bits 7..8
```

They are thin wrappers over one shared packed reader, passing **bit offsets 0, 3 and 7** - exactly
the ranges section 2 documents, and summing to **9 bits**. The claim holds.

The shared reader bounds-checks `param_1 < *(ushort *)(DAT_02ADD0B0 + 6)`, so the MWeather resource
carries its entry count at `+6`.

**Width caveat:** only the first wrapper's width argument (`3`) survives decompilation; the other two
pass offset only. ~~The widths 4 and 2 are inferred from the offsets being 3 and 7 with a 9-bit total,~~
~~not read directly.~~ *(answered: the widths are read, not inferred — "The field widths are read" below closes this caveat; 2026-10-02, OPUS)*

**Stamp advanced because the bodies were re-read**, per the evidence standard.

## Cross-subsystem neighbours — disposition (audit pass, repos-2d, 2026-09-03)

`audit_crossrefs.py` reported two **core runtime scheduling** edges for this document: a Combat
Formula function and a Presentation function each calling the engine's image-address resolver.

That 10-byte routine converts a stored 32-bit image address into a runtime pointer — the convention
**every authored table in this engine is addressed through**, including the MWeather resource this
document describes. It has **815 callers across 18 owner subsystems**, and it is runtime
infrastructure, in the same class as the CFG guard stub and `memset`: uninformative as a neighbour
and as a subject. Its census is enumerated in
[weather-apply-and-environment-materialization.md](weather-apply-and-environment-materialization.md)
§ *Cross-subsystem neighbours*.

*Disposition: runtime infrastructure, not an MWeather relationship.*

**Method note, twice learned in one pass.** The first version of this section was shared boilerplate
that also named the field-id accessor; this document had never cited it, and naming it immediately
drew three **Movement** and five **UI** findings that had not existed. The second version fixed that
but cited the image-address resolver **by address** — and that one has 815 callers, so it pulled in
**Actor/Entity, Audio, Combat AI, Combat Action** and more, taking the category from 5 findings to
10. Both times the fix was the same: **name the function, do not cite the hex.** A citation is a
commitment to account for everything it drags in, and a reference to a census someone else holds is
not a citation.
- **CombatFormula - SERVICE (1 edge).** `0038B220` reaches bodies filed to combat formula: `0031B860` - shared machinery across the layer boundary, no shared ownership.
- **Gameplay - CLIENT (1 edge).** `00202E10` is also called by bodies filed to Gameplay: `00339630` (Combat) - shared machinery across the layer boundary, no shared ownership.
- **Save_Load_Settings - SERVICE (1 edge).** `0026D910` reaches bodies filed to save/load/settings: `002EF2B0` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (5 edges).** `0026D910`, `002E3D40`, `0032E400` are also called by bodies filed to script VM / native bridge: `003565C0`, `0034B6C0`, `0034BD10` - shared machinery across the layer boundary, no shared ownership.

## The script interface: `setmapwind` and `defaultmapwind` (repos-2d, 2026-09-03)

**A script can set these three fields directly, bypassing the table.** Two authored verbs reach
`002E3D40`, and between them they answer what the three MWeather fields are *for*:

| Call id | Verb | Args | Handler | Arity check |
|---|---|---:|---|---|
| `0x0481` | **`setmapwind`** | 3 | `0034B6C0` | **3** pops, then `002E3D40` with `mode = 1` |
| `0x0482` | **`defaultmapwind`** | 0 | `0034BD10` | **0** pops; zeroes all four arguments, `mode = 0` |

`002E3D40(mode, A, B, C)` is a two-source multiplexer in front of the Presentation backend init:

```c
ebp = A;  esi = B;  eax = C;
if (mode == 0) {                                  /* defaultmapwind */
    field    = <active-or-pending field id>;
    selector = MapRef_GetPrimaryFieldValue(field);
    slot     = <current Weather Slot, 1..3>;       /* the getter in the slot-state document */
    ebp = FUN_00377850(selector, slot);            /* offset 0, width 3  - preset   */
    esi = FUN_003777A0(selector, slot);            /* offset 3, width 4  - azimuth  */
    eax = FUN_003777B0(selector, slot);            /* offset 7, width 2  - elevation */
}
jmp FUN_0040AAD0(ecx = ebp, edx = esi, r8d = eax);
```

**Mode 0 fills the three registers from the three MWeather extractors; mode 1 fills the same three
registers from the script's arguments.** Same consumer, same slots, two sources — so the script
arguments *are* the three packed fields.

### The argument order, derived rather than assumed

The order is **not** the one the field layout suggests. Following the registers:

| Handler pop | `002E3D40` param | Register | Reaches `0040AAD0` as | Which mode 0 fills from | So the argument is |
|---|---|---|---|---|---|
| pop 1 = `paramType[0]` | `C` (`r9d`) | `eax` | 3rd (`r8d`) | `003777B0`, offset 7 width 2 | **elevation class** |
| pop 2 = `paramType[1]` | `B` (`r8d`) | `esi` | 2nd (`edx`) | `003777A0`, offset 3 width 4 | **azimuth sector** |
| pop 3 = `paramType[2]` | `A` (`edx`) | `ebp` | 1st (`ecx`) | `00377850`, offset 0 width 3 | **backend preset** |

```
setmapwind(elevation, azimuth, preset)
```

The pop-to-parameter direction is the convention proved in
[`../../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md`](../../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md)
§4.4 — *"the catalog's `paramType[0]` is the first value the handler pops"* — established there
against a five-argument verb whose shape makes a wrong convention obvious.

**This is why the question was worth settling rather than assuming.** §4 lists the packed fields as
preset, azimuth, elevation, in that order; a reader carrying that order into the verb would write
`setmapwind(preset, azimuth, elevation)` and be exactly reversed. The handler passes its pops in
the opposite order to the one the record lists them in.

### The field widths are read, not inferred — §9's caveat is closed

The re-verification in §9 records that only the first wrapper's width survived decompilation and
that *"the widths 4 and 2 are inferred from the offsets being 3 and 7 with a 9-bit total, not read
directly."* The encodings state both, because each wrapper computes its **offset from its width**:

```asm
00377850   mov r9d, 3    xor r8d, r8d         ; width 3, offset 0        preset
003777A0   mov r9d, 4    lea r8d, [r9 - 1]    ; width 4, offset 4-1 = 3  azimuth
003777B0   mov r9d, 2    lea r8d, [r9 + 5]    ; width 2, offset 2+5 = 7  elevation
```

Widths **3, 4, 2** and offsets **0, 3, 7** are now both read directly, summing to the documented
9 bits. The inference was correct; it is no longer an inference.

### Modding consequence

`setmapwind` overrides all three fields at once for as long as the script leaves them set, and
`defaultmapwind` restores them from the record for the **current** field and Weather Slot — so a
zone script that sets wind and never resets it leaves the override in place across a slot change
that would otherwise have re-read the table.


## The `00268750` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00268750` (`MapRef_BeginLoadResources`) — `0032E400(9, 4)` allocates,
then clears the `02099D88`/`02099D98` slots (`0026875A`/`0026876B`).

| member | role | interior |
| --- | --- | --- |
| `00267930` | assert-tagged load body — `0036C1D0(5)` then `0036C750("..\..\katano\ateldecode.c")` diagnostic path (`00267943`/`0026794F`) | [`00267948`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0032E400`, `0036C1D0`, `0036C750`.

## SWE2-EC7-39 update (2026-09-19) - `0040B430`

`0040B430` (416 B) is the basis normalise/publish the page names - `01CEBBA8`/`01F44830`, the `02CA43A0`..`02CA43B8` field block, `00861F14` pair plus `00202E10`/`00808C40`. Interior anchor `0040B495` (an `00861F14` call).

## SWE2-EC7-43 update (2026-09-19) - `0040AAD0`

`0040AAD0` (286 B) is the MWeather presentation-backend init - `008F30F4`/`0091523C`/`009155F0`/`00915610`/`00D10AE0`/`00D12300`/`01F44830`/`02CA4391`, `00202B90`/`003D8E50`/`0040B3B0`/`0040B430`/`0046D160`/`0046D200`/`00808C40`. Interior anchor `0040AB07` (a `00202B90` call).


## SWE2-EC7-63 update (2026-09-19) - `003777C0`

`003777C0` (144 B) is ~~the 3-bit weather preset body~~ the packed-bit reader the three extractors share, and the preset is `00377850`'s *(corrected 2026-10-02, OPUS: `retool.py callers 003777C0` — `00377850`, `003777A0` and `003777B0` all enter it)* - call-free index arithmetic (`rdx+rcx*2`, `rcx*9`, `r9-9` bounds), `02ADD0B0`. Interior anchor `003777E9` (the `rcx*9` index form).

`00377850` (14 B) is the preset extractor — the third of the field readers sharing `003777C0`: tail-enters `003777C0(ecx, edx, 0, 3)`, i.e. `(selector, slot, bitOffset 0, width 3)`, which is exactly the 3-bit weather preset `choosing-the-field-environment-variant.md` describes.

Interior anchor `00377859` (function `00377850`).
