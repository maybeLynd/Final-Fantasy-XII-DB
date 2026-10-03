---
system: Sound variant selection (SQEX::Sd::Driver::*Sound)
category: 18-Audio
status: DOCUMENTED — SD-23, SD-24, SD-25, G-1 and G-13 are ANSWERED and G-2 is SUPERSEDED (owner re-status 2026-09-30, OPUS, on SWE2-STRUCT's DD batch 11) — G-2 is SUPERSEDED 2026-09-27 (OPUS, class-1 ruling) with the consumer of the sequence record's +0x28 flag and +0x2C float not found; the range bytes placed 2026-09-18 (that day's placement of +2/+4/+5 and an entry key at +0x24 in the Sequence corrected 2026-09-30 under SD-24, §7); G-1 and G-13 answered 2026-09-17 (§12); shipped data builds only the base Sound (§12, 2026-09-18); SD-24 answered 2026-09-30 (a sound's +0x30 is its SabFile::Sound record); SD-23 (what capability slots 38/39 mean to their callers) and SD-25 (whether the selects share rand() state with gameplay) are since answered in the register (status line current 2026-09-30, SWE2-DATA)
owner_layer: PrimaryOwner:Audio / CodeDomain:Audio.SQEXSd
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
  last_pass: 2026-09-02
  last_pass_state: falsification-pass
  crossref_clean: false
  reopened_count: 0
---

# Sound variant selection

> How FFXII decides *which* sound actually plays when one sound event fires — and why a
> footstep on stone differs from one on sand without the game asking for a different sound.

~~**PARTIAL.**~~ *(Superseded: DOCUMENTED, owner re-status 2026-09-30; struck 2026-10-01, OPUS.)* `SwitchSound` is read and proven at tier 1, as is the record-format versioning.
The base `Sound` shape is read. What distinguishes `RandomSound`, `OrderSound` and
`CycleSound` is **read whole in §12 (2026-09-17)**; the two explanations §2 eliminated were the wrong place to
look, and §12 also names the class selector. Nothing here is asserted from class names.

## 1. What the player sees

One "sound" in FFXII is often not one clip. It is a small set of candidates plus a rule for
picking among them, which is why:

- ~~repeated hits on the same enemy do not sound mechanically identical;~~
- ~~footsteps change with the surface you are walking on, smoothly, without the game switching
  to a different sound effect;~~
- ~~an engine or ambience shifts in character as a value changes rather than snapping.~~

The rule differs per sound. Some pick at random, some step through in order, some cycle, and
some **choose by a measured value** — that last one is proven below.

*(Corrected 2026-09-30, SWE2-DATA: the three bullets were player-level readings of the class names, and the shipped data does not support them. Every one of the 13,150 shipped `snd ` records builds the base `Sound` (class byte `+4` is 0 or 1, §12), so `RandomSound`, `OrderSound`, `CycleSound` and `SwitchSound` are never constructed, and the base select `007BD370` plays every candidate on every trigger. Variety between repeated weapon swings and voices comes from the character's sound emitter choosing which trigger to request, with the presentation PRNG ([how an animation makes a sound](../how-an-animation-makes-a-sound.md) §2); a surface-dependent footstep is chosen by the game before the driver, by the game's footstep chooser indexing the `FOOT` table with the actor's contact-surface word (UQ-66, [the five small bin tables](../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/five-small-bin-tables.md)). The rules below are what the engine would do with records that carried those class bytes.)*

## 2. Native mechanism

All five implementations sit at **vtable slot 43** of their class (except `VariationSound`,
which keeps the base — see the
[architecture document](../sqex-sd-sound-driver-architecture.md)).

### The shared shape

Every variant does the same four things:

1. obtain the candidate container — base uses `FUN_007b2470`, all variants use `FUN_007bd8d0`;
2. begin iteration with `FUN_007cfa30(&list, &iter)`;
3. walk entries with `FUN_007cfac0(&container, &out, index)`, resolving each through
   `FUN_007cf9e0(&iter, &out, key)` where `key` is a `u16` at entry `+4`;
4. **trigger the chosen entry** with `FUN_007bd240(this, &entry)`;
5. clean up with `FUN_007cf580(&list)`.

The candidates are `SQEX::Sd::SABSOUNDSEQUENCEINFO` records, reached through
`SQEX::Sd::AudioBinaryFile::BaseClass<SQEX::Sd::SABSOUNDSEQUENCEINFO>` — so the candidate set
is **authored data in the SAB container**, not code.

`FUN_007bd240` is the common trigger. Everything above it is candidate selection.

### `SwitchSound` — proven

The clearest and the only one fully read. It fetches a single runtime value and plays whichever
candidate's range contains it:

```c
float value = FUN_007bd9d0(this);              // runtime parameter for this sound

for (each entry E in candidates) {
    float lo = FUN_007cfbf0(&E);               // entry range minimum
    float hi = FUN_007cfbc0(&E);               // entry range maximum
    if (lo <= value && value < hi)
        FUN_007bd240(this, &E);                // play E
}
```

The selection formula, exactly as evaluated:

```
play entry E   iff   E.rangeMin <= parameter < E.rangeMax
```

Note the asymmetry — **inclusive lower bound, exclusive upper bound**. Adjacent authored
ranges therefore tile without overlap, and a value exactly on a boundary belongs to the
*upper* range. A modder authoring ranges must respect that or a boundary value plays twice
or not at all.

This is the mechanism behind sound that tracks a continuous quantity: author the candidates
with adjacent ranges, and the driver picks by measurement rather than by event.

### The base `Sound`

Gated on a byte at `*(char *)(*(longlong *)(this + 0x30) + 5)`; when set, it walks entries and
triggers each qualifying one. No selection predicate — it is the straightforward case.

### `RandomSound`, `OrderSound`, `CycleSound` — shape read, rule not yet proven

> **Superseded by §12 (2026-09-17):** the three rules are read in full there.

All three follow the shared shape and differ in a per-entry predicate plus loop structure:

| Class | Slot-43 body | Accessor called | Distinguishing structure |
|---|---|---|---|
| `RandomSound` | `007E5160` | `FUN_007cf9c0` | second pass from `index + 1` |
| `OrderSound` | `007E58D0` | `FUN_007cf830` | maintains a separate counter |
| `CycleSound` | `007E6360` | `FUN_007cf9c0` | second pass from `index + 1`; also overrides slots 39, 40, 42 |

**Corrected 2026-09-02: those are not two different predicates.** Both were read, and they
are the same accessor differing only in return type:

```c
// 007CF9C0                          // 007CF830
byte v = rec->version;               byte v = rec->version;
if (1 < v && v != 2)                 if (1 < v && v != 2)
    return rec[0x10];                    return rec[0x10] != 0;   // as bool
return rec[4];                       return rec[4] != 0;          // as bool
```

Identical field, identical version logic. `007CF830` merely coerces to boolean. **So the
accessor distinguishes nothing** between `Random`, `Order` and `Cycle` — the entire difference
between those three lies in loop structure, plus `CycleSound`'s three extra overridden slots.

No claim is made about randomness or ordering. Both candidate explanations have now been
eliminated (shared predicate, then identical predicate)~~, and the mechanism is *still* unproven~~. *(Corrected 2026-09-30, SWE2-DATA: the mechanism is read whole in §12 — G-1 answered 2026-09-17.)*

### The slots the variants override — read 2026-09-12 (FABLE; G-8, G-9, G-10)

The recovered vtables ([the architecture page](../sqex-sd-sound-driver-architecture.md) §2) give slots 36–43 for the base and the five variants;
reading the override bodies names the slots:

| slot | base `Sound` | what it is | `VariationSound` | `CycleSound` |
|---|---|---|---|---|
| 36 | `007BD990` — the record's word `+8`, the **candidate count** | how many entries the walk sees | `007E57C0` — returns the object's own `+0x538` | = |
| 37 | `007BD0A0` — asks the container (its vtable `+0x18`) **whether there are candidates** | gates the walk | `007E57B0` — **always false** | = |
| 38 | `007E57B0` — false | a capability flag | `007E5800` — **true** | = |
| 39 | `007E5800` — true | a capability flag | = | `007E57B0` — **false** |
| 40 | `007BDDA0` — **bind**: copies the record's fields into the object (`+0x18`, `+0x20`, `+0x38`, `+0x40`, `+0x48` …) | called when a record is attached | `007E57D0` — base, then `+0x538 ← record +0x34` | `007E65B0` — rolls **an interval** `rand() % (rec[+0x14] − rec[+0x10] + 1) + rec[+0x10]`, scales it by a constant into the float `+0x538`, then base |
| 42 | `007BF0A0` — the per-update (2,317 B) | runs every update | = | `007E6620` — when the state (vcall `+0xA8`) is 2 and the walk's index is below the record's byte `+0x18`: **`+0x538 −= dt`, and at or below 0 re-selects** through the cycle helper `007E5E80` |
| 43 | `007BD370` — select | the candidate walk and trigger | = (base) | `007E6360` |

So the three questions answer themselves from the bodies. **G-8:** `VariationSound` keeps the
base select because it **has nothing to select** — slot 37 says there are no candidates, so the
base walk never runs; what it "varies" is the parameter it stores at bind (`+0x538 ← record
+0x34`) and reports through slot 36 in place of a count. **G-9:** `CycleSound` is the **timed
re-trigger**: slot 40 rolls the next interval from the record's `[+0x10, +0x14]` range, slot 42
counts it down and re-selects when it expires, slot 39 turns its capability flag off. **G-10:**
`RandomSound` and `CycleSound` share the selection accessor, and the difference is exactly that
timer — `RandomSound` selects once per trigger, `CycleSound` keeps selecting on its own clock
while in state 2. What the two capability flags (38, 39) mean to their callers is not read here — `SD-23`: an audio-range scan finds 16 virtual calls through `+0x130` (slot 38) and 2 through `+0x138` (slot 39), and none is read for what it does with the answer. *(Answered 2026-09-30 (OPUS `acb04148d` + `9af526c00`); register row SD-23, records [`sd23-sound-slots-38-39-0930`](../../_index/candidates/sd23-sound-slots-38-39-0930/README.md) and [`sd23-state7-dynamicsound-0930`](../../_index/candidates/sd23-state7-dynamicsound-0930/README.md): slot 38 answers "does this sound delegate to a chosen child instead of playing a record of its own" (true only for `VariationSound`); slot 39 answers "does this sound finish, entering the terminal state 7, when its last child ends" (true for every class but `CycleSound`). The four float-using `+0x130` calls are `SQEX::Sd::Lay::DynamicSound`'s own slot 38, not this family's.)*

### The record format is versioned — proven

The accessor's real content is a **format-compatibility shim**:

```
field = (version >= 3) ? record[0x10] : record[0x04]
```

where `version` is the byte at record offset `+0`. Versions 0, 1 and 2 keep the field at
`+0x04`; version 3 and above relocate it to `+0x10`.

The same pattern appears in `FUN_007bd9d0`, `SwitchSound`'s parameter source, which requires
`version > 9` **and** a type byte `record[4] == 5` before walking a variable-length structure
using a length at `+2` and an alignment term `(record[0x23] + 0x10) & 0xf0`.

**The SAB sound format evolved across at least three layout generations and the shipping
engine still reads all of them.** Any tool that parses these records must handle every
version, not just the newest.

## 3. Key addresses

| Address | Working name | Role |
|---|---|---|
| `007BD370` | `Sound::Select` (slot 43 base) | walk and trigger qualifying entries |
| `007E5160` | `RandomSound::Select` | accessor `FUN_007cf9c0` + second pass |
| `007E58D0` | `OrderSound::Select` | accessor `FUN_007cf830` + counter |
| `007E6360` | `CycleSound::Select` | accessor `FUN_007cf9c0` + second pass |
| `007E67C0` | `SwitchSound::Select` | **range match on a runtime float** |
| `007BD240` | *(sound trigger)* | the common play entry point |
| `007BD9D0` | *(runtime parameter getter)* | supplies `SwitchSound`'s value |
| `007CFBF0` / `007CFBC0` | *(entry range min / max)* | |
| `007CFAC0` | *(entry at index)* | |
| `007CF9E0` | *(resolve entry by u16 key)* | key at entry `+4` |
| `007CFA30` / `007CF580` | *(iteration begin / cleanup)* | |
| `007CF9C0` | versioned field accessor | returns `byte`; `(v>=3) ? rec[0x10] : rec[4]` |
| `007CF830` | same accessor, boolean form | returns `!= 0` of the same field |

## 4. Data structures and formulas

```
SABSOUNDSEQUENCEINFO           authored, in the SAB container
  +0x00  u8    version         selects the layout below
  +0x02  u16   length          (used by FUN_007bd9d0's walk)
  +0x04  u16   key             passed to the resolver FUN_007cf9e0
  +0x04  u8    <field>         versions 0-2   } same field,
  +0x10  u8    <field>         versions 3+    } relocated by version
  +0x23  u8    <align term>    (used by FUN_007bd9d0: (v + 0x10) & 0xf0)
  ...          rangeMin        float, via FUN_007cfbf0   (SwitchSound)
  ...          rangeMax        float, via FUN_007cfbc0   (SwitchSound)

Sound object
  +0x20        candidate container      (base path, FUN_007b2470)
  +0x30  ptr   -> byte at +5 gates the base walk
```

~~Exact offsets for `rangeMin` / `rangeMax` are **not** established — they are reached through
accessors, not by direct field access. Do not assume a layout.~~

*(Corrected 2026-09-30, SWE2-DATA: the offsets are established (G-13, §12): the range accessors `007CFBF0` / `007CFBC0` read the `SabFile::Sequence` record's `+0x10` / `+0x14` from version 3 (`+4` / `+8` at version 2, none below), and every shipped record is version 4 with those bytes zero. The block above also merges three records that §12 separates: the 16-byte `SoundSequenceInfo` entry (its `u16 +4` is the key, UQ-250), the `Sequence` (weight `+0x10`, group `+0x11`, byte `+8`, ranges `+0x10` / `+0x14`) and the sound's own `Sound` record (class byte `+4`, candidate count `+5`, cursor `+1`, allow-repeat `+0x19` bit 5). §12's version table is the current field map. ~~Which of the two records a sound's `this + 0x30` holds is stated differently in §7 (G-2, 2026-09-18) and §12 — `SD-24`.~~ `SD-24` is answered 2026-09-30: it is the `Sound` record. The block's `+0x02` length and `+0x23` align term, which `FUN_007bd9d0` uses, belong to that record too (§7, the G-2 and G-11 corrections).)*

**SwitchSound selection:**

```
play entry E   iff   E.rangeMin <= parameter < E.rangeMax
```

**Versioned field access** (both selection accessors, `007CF9C0` and `007CF830`):

```
field = (version >= 3) ? record[0x10] : record[0x04]
```

`007CF830` returns `field != 0`; `007CF9C0` returns the raw byte. Otherwise identical.

**SwitchSound parameter gate** (`FUN_007bd9d0`, partially read):

```
require version > 9  &&  record[4] == 5
then walk:  p = record + record[2] + ((record[0x23] + 0x10) & 0xf0)
            result = (p[0] == 0) ? p + 0x10 : p + p[2]
```

## 5. Call chain

```
a sound event fires
  -> Sound object, vtable slot 43            <- variant-specific selection
     -> FUN_007bd8d0 / FUN_007b2470          obtain candidate container
     -> FUN_007cfa30                          begin iteration
     -> per entry:
          FUN_007cfac0                        entry at index
          FUN_007cf9e0(key = entry+4)         resolve
          [variant rule]                      predicate, or range test
          -> FUN_007bd240(this, entry)        TRIGGER
     -> FUN_007cf580                          cleanup
```

~~**Upstream:** not yet mapped — which engine paths raise a sound event is open (**G-6**).~~
~~**Downstream:** `FUN_007bd240` and below, unread.~~

*(Corrected 2026-09-30, SWE2-DATA: both ends are read. G-6 was WITHDRAWN 2026-09-02 as a wrong premise, and the chain is anchored in the raw call index.)*

```
007BDFA0 (call 007BE080) | 007BF0A0 slot 42, the per-update (call 007BF8CB)
  -> 007BD120  the sound-instance stepper; call [vtable + 0x158] = slot 43 (007BD205; virtual, UQ-251)
    -> 007BD370 | 007E5160 | 007E58D0 | 007E6360 | 007E67C0   the selects (no direct callers)
      -> 007BD240  the trigger: 14 direct call sites, all in the five selects and 007E5E80
        -> 007E7300  the sequence arm (007BD333) -> the per-sequence update and the voice (G-18, G-19)
```

**Upstream** of the stepper is [how a sound request becomes a voice](../Audio-Boundary/how-a-sound-request-becomes-a-voice.md) (UQ-251). **Downstream:** `007BD240` is read whole on [the sound-trigger page](sound-trigger.md) (UQ-262).

**Do not confuse with:** the `SQEX::Sd::Lay` spatial classes. Those decide *where* a sound is
in the world; this decides *which* candidate plays.

## 6. Modding notes

- **The candidate set is authored data**, in the SAB container as `SABSOUNDSEQUENCEINFO`
  records. Adding or changing candidates is a data edit, not a code edit.
- **`SwitchSound` ranges are half-open `[min, max)`.** Author adjacent ranges to tile cleanly;
  a value exactly on a shared boundary goes to the upper range.
- **`FUN_007bd240` is the single trigger.** Anything that needs to observe or intercept sound
  playback should attach there, not at the five selection methods.
- **XIIOnline:** ~~untested territory. Selection is local and driven by local parameters, so it
  most likely needs no synchronisation — but if a `SwitchSound` parameter is derived from
  shared world state, two clients with different state will legitimately pick different
  candidates. Not yet investigated.~~ *(Corrected 2026-09-30, SWE2-DATA: settled by the shipped data: every shipped sound builds the base `Sound`, whose select plays every candidate on every trigger with no parameter and no draw (§12), so the selection layer cannot diverge between clients on shipped banks. Divergence can still come from above it — which trigger the emitter requests ([how an animation makes a sound](../how-an-animation-makes-a-sound.md) §2).)*

## 7. What is not known

- [x] ~~What actually distinguishes `Random`, `Order` and `Cycle`. Both accessors are now read~~
      and are the *same* version-aware field read, so the difference is purely loop structure.
      ~~**G-1** remains open with two explanations eliminated.~~ *(Struck 2026-09-30, SWE2-DATA: G-1 is answered; see the next line and §12.)*
      ***ANSWERED 2026-09-17 (FABLE): the three rules, read whole (§12).** A *set* is a run of consecutive candidates sharing the group byte `007CF9A0` returns (sequence record `+0x11` at version 3 and above); its first entry's weight (`007CF9C0`, `+0x10`) decides for the set. **Random** (`007E5160`): every set whose weight is 0 plays; then one roll `rand() % 101` walks the weighted sets by cumulative weight and takes the first that reaches it; if that index equals the last pick (record `+1`) and record `+0x19` bit 5 is clear, the first other weighted set is substituted, then any later one whose weight exceeds the picked set's; no substitute means nothing plays and `+1` becomes `0xFF`; otherwise `+1` remembers the index. **Order** (`007E58D0`): every set whose weight is not 0 plays; the zero-weight sets are counted, and the one at cursor `+1` (0 when the cursor is at or past the count) plays, with `+1 = (cursor + 1) mod count` (`007E5BB9`..`007E5BD2`). **Cycle** (`007E6360` with `007E5E80`): Random's two passes, but the substitution also refuses any set whose group byte is still sounding among the object's active players (`007E5DA0` collects them from `+0x400`, count `+0x4C`), and slot 42's timer re-runs it. The class is chosen by the factory `007B2F70` from the sound record's byte `+4`: 0 or 1 the base `Sound`, 2 Random, 3 Order, 4 Cycle, 5 Switch. Static, bodies read; the shipped consequence, with every sequence record zero from `+0x10`, is in §12.*
- [x] ~~What the versioned field at `+0x04`/`+0x10` *means*.~~ **G-12** — **ANSWERED 2026-09-15 (OPUS), §11:
      a per-candidate WEIGHT.** The consumer sums it (`add r14d, eax`), compares two candidates' values
      (`cmp dil, al`), and walks candidates until the running total reaches `rand() % 101`; a weight of 0
      skips the candidate, which is why all-zero shipped data never exercises the weighted pass. *Narrowed by data 2026-09-12
      (FABLE):* in the shipped banks the accessor never takes the `+0x04` path and its return is
      **always 0** — every sequence record is version 4, so it reads `+0x10`, and `+0x10` is `0` in all
      **11,165** sequence records of the 4,609 `.sab` (walked through the chunk directory of
      [the container page](../Sound-Bank-And-Voice-Formats/sab-sound-bank-container.md) §2 and each chunk's `{u16 0; u16 0x10; u32 count; 8 zero; u32 offset[count]}` table).
      Whatever the field means, the shipped game exercises only its zero value; the meaning has to
      come from the accessor's consumer, not from the data.
- [x] ~~Full SAB record version history and per-version layouts. **G-13**. *Narrowed by data~~
      2026-09-12 (FABLE): one generation ships.* All 11,165 `seq ` records carry version byte **4**
      and are **64 bytes** (every offset delta), all 13,150 `snd ` records carry version **16**; the
      chunk sub-header word is `0x10` in all 9,218 chunks. So the accessor's versions 0–2 branch
      (`+0x04`) and the `version > 9 && record[4] == 5` walk are **legacy paths no shipped bank
      reaches**; a reconstruction must parse sequence version 4 and sound version 16, and may
      treat the others as unreachable until a bank that carries them is found. Of the 64 bytes of a
      version-4 sequence record, **46 are constant across the corpus** (`+0` = 4, `+2` = `0x20`, `+6` =
      `0x20`, `+0x20`–`+0x23` = `02 04 02 0C`, `+0x31` = 4, the rest 0); the varying bytes are `+4`–`+5`
      (the record's index within its bank, 0–11 in the tallies), `+0x24`, `+0x28`–`+0x2B`, `+0x2C`–
      `+0x2F` (a float, `0x3E92F1AA` in the sample), `+0x30`, `+0x32`–`+0x35`, `+0x39`–`+0x3A` and
      `+0x3D`–`+0x3E`. Tally in `Tools/work/FABLE/bf3-scratch/sab_versions-2026-09-12.json`; naming
      those fields is the residue. *(2026-09-30, SWE2-STRUCT for OPUS: registered - the naming went to G-2 (the next item but one), SUPERSEDED 2026-09-27 with a finite residue: the `Sequence` bytes `+0x24`, `+0x28`, `+0x2C` and `+0x30`, which no reader reaches; the others are placed there and in §12.)*
      ***ANSWERED 2026-09-17 (FABLE): the version vocabulary the image reads, per class (§12).** Every version test in the reader range `007CF000`..`007D0000` and in the four consumers outside it is listed: the sound record (`SabFile::Sound`, ships 16) at version 2 gains four parameter ids `+0x30`..`+0x33` and floats `+0x34`..`+0x43` with the count at `+0x44`, at 12 a ZeroOne-parameter table (`+0x4C` offset, `+0x4E` count, 32-byte rows); its candidate list keeps the entry table at `+2` through version 5 and at `+0x1A` after; the sequence record (`SabFile::Sequence`, ships 4) has no ranges below 2, weight, group and ranges at `+4`/`+5`/`+4`/`+8` at 2, at `+0x10`/`+0x11`/`+0x10`/`+0x14` from 3, a byte at `+8` from 3 (constant 2 below)~~, and the named-parameter block only at 10 and above with type 5~~ *(corrected 2026-09-30, SWE2-DATA, `SD-24`: that block is the `Sound` record's, see G-11 below and the §12 table)*; the `SoundEffect` container moves its table from `+2` (below 9) to the aligned header (9 and 10) to `+0x46` (11 and above); the ZeroOne curve reads `+0xA`/`+0xC` at 1, `+0x12`/`+0x14` at 2, a counted table at `+2` from 3; the music (`MabFile`) records align by byte `+4` from 8, by `+0x48` from 9, `ModeParam` by `+6` from 3. Beyond those thresholds the image holds no history; the shipped banks sit on one branch of each. Static.*
- [x] ~~What actually differentiates `RandomSound` from `CycleSound`, given they call the
      *same* predicate. **G-10**.~~ **Answered 2026-09-12** — the timer (§2, "The slots the variants override").
- [x] Field offsets and full layout of `SABSOUNDSEQUENCEINFO`. **G-2**. *Narrowed 2026-09-12 *(closed — the register row is ~~WITHDRAWN~~ **SUPERSEDED** 2026-09-27 (OPUS, class-1 ruling); the register word corrected 2026-09-30, SWE2-DATA.)*
      (FABLE), two halves.* **The candidate container the accessors read** (`[ctx+8]`, read whole
      from `007CFAC0` / `007CF9E0` / `007CFBF0` / `007CFBC0`): `+0` version byte, `+2` `u16` offset of
      the entry table for versions **≤ 5**, `+0x1A` for higher versions (`007CFACB`–`007CFAD8`),
      `+4` `u16` entry count (`007CF9E9`); entries are **16 bytes** (`shl rcx, 4`, `007CFAC7`), the
      by-key resolver indexes a `u32` offset table at the same `+2` base (`007CF9F3`–`007CFA09`), and
      the range floats sit at `+0x10` / `+0x14` for versions above 2, `+4` / `+8` at version 2, and
      are 0 below (`007CFBF0`, `007CFBC0`). **The sequence record itself**, profiled over all 11,165
      shipped version-4 records: the varying bytes are `+4`–`+5` (the in-bank index 0–255 and a
      flag, 428 set), `+0x24` (0–122, one 0 per bank — a per-bank ordinal), `+0x28` (a flag, 660
      set), `+0x2A`–`+0x2B` (a copy of `+4`–`+5`), `+0x2C`–`+0x2F` (a float, exponent bytes 61–67, i.e.
      values near 0.1–2.0), and `+0x32`–`+0x3E` set in only **12** records (`+0x32` = 3, `+0x33` /
      `+0x39` / `+0x3A` / `+0x3D` = 4, `+0x3E` = 1, `+0x34`–`+0x35` a word) — the twelve are the only
      records with a second block, consistent with the version-10 walk's variable structure being
      absent from shipped banks. Which reader consumes `+0x24`, the float and the flags is the
      residue (the bind copies a descriptor, not the raw record).
      ***NARROWED 2026-09-17 (FABLE): the readers are named by class, and the payload has none found.** The descriptors the accessors return are RTTI classes: the 16-byte entry is `SabFile::SoundSequenceInfo`, the resolved record `SabFile::Sequence`, the sound's own record `SabFile::Sound`; the range, weight and group accessors all take the `Sequence`. Its consumed fields are therefore `+0` version, `+4` key/type, `+8` byte, `+0x10` weight and range minimum, `+0x11` group, `+0x14` range maximum, and the version-10 name block; the varying bytes `+0x24`, `+0x28`, `+0x2C` (the float) and `+0x30`.. have **no reader** in the reader range nor in any audio-range function that loads them through a descriptor pair. The two larger accessors there (`007CFD00`, `007CFE60`) serve the ZeroOne curve, not the sequence. What consumes the payload is not found statically.*
      ***NARROWED 2026-09-18 (FABLE): ~~the record and the container are the same thing, and~~ the key, the count and the range are placed; the flag and the float still have no reader.** The five policy walkers wrap the record at `this+0x30` as the accessor context (`007E681D`..`007E682F`), so ~~the container the accessors read *is* the 64-byte `SabFile::Sequence`: its `u16 +2` = `0x20` is the entry-table offset (version 4 ≤ 5, `007CFAD1`), its `+4` the in-bank index, and~~ its `+5` the entry count every walker loops on (`i < byte [record+5]`, `007E51F5`, `007E5961`, `007E5F38`, `007E63CB`, `007E6841`), which the archive census under G-17 found to be 0 or 1 ~~in all 11,165 records. The one entry therefore sits at `+0x20`..`+0x2F` (`02 04 02 0C ...` in the sample): its word `+4` is the record's `+0x24`, the *per-bank ordinal*, and it~~ *[2026-09-30: the entry's word `+4`]* is the key the walker passes to the by-key resolver `007CF9E0` (`movzx r8d, word ptr [rax+4]`, `007E68B0`) over the context `007CFA30` builds by finding the bank's `seq ` chunk by tag (`01CB6EE0`, the 16-byte directory walk `007CFA80`..`007CFA97` off the `SabHeader` fields `+4`, `+6`, `+8`, `+9`); that resolver indexes the chunk's `u32` offset table (`+0x10`, count at `+4`), so the key names ~~another~~ a sequence record of the same bank: the candidate. The range accessors `007CFBF0` / `007CFBC0` then read the candidate record's `+0x10` / `+0x14` (version-4 path), bytes the corpus profile above finds constant zero. *Not found:* no function in the accessor family `007CF500`..`007CFC80` reads an entry's `+8` or `+0xC` ~~(the record's `+0x28` flag, 660 set, and `+0x2C` float near 0.1..2.0)~~, and the five walkers use only `+4`; their consumer, if any, lies outside the family. Static, the walkers and accessors read in full, joined to the archive census.* *(Corrected 2026-09-30, SWE2-DATA — `SD-24`: the record at `this+0x30` is the sound's own `SabFile::Sound` record from the bank's `snd ` chunk, not a `Sequence`, so the container and the candidate are two different records. The walkers pair it with vtable `01CB43E0`, whose RTTI class is `SabFile::Sound` (`007E593D`, `007E6828`). Every shipped `snd ` record is version 16, so the entry accessor `007CFAC0` takes the entry table at `u16 +0x1A` (`007CFAD8`), not `+2`. And the bind `007BDDA0` reads that record's byte `+0x4E` (`007BDE4E`), past the end of a 64-byte record. Read that way over all 4,609 shipped banks, every one of the 11,165 entries has a `u16 +4` key that indexes the bank's `seq ` table; read with the table at `+2`, none does. So `+4` is the class byte (§12), `+5` the entry count (0 or 1 in all 13,150 `snd ` records), and the entries are `SoundSequenceInfo` rows inside the `Sound` record. The `Sequence` record's `+0x20`..`+0x2F` is not an entry the walkers read. Its `+0x24`, `+0x28` and `+0x2C` return to the unplaced bytes that the SUPERSEDED residue lists. Control `_index/candidates/dd-leftovers-0930/sd24_record.py` (R1–R4, D1–D3, X; FAILS 0).)*
  **NARROWED FURTHER 2026-09-27 (OPUS), G-2 WALK ROUTES CLOSED 2026-09-27:** the indexed walk that the accessor-caller narrowing left open is closed, and so is a stepped-pointer walk. No operand anywhere in the image reads [base + idx*16 + 0x28 / 0x2C], and none reads those displacements with an index shifted by 4 or multiplied by 0x10 just before; the same scanner finds 17 such accesses scaled by 8, the positive control. In the audio range, no pointer stepped by 0x10 reads a byte at +8. The nine functions where a 0x10-stepped register reads a dword at +0xC are dispositioned, and none walks the entry table: 007DA2E0 vector products, 007B0390 a float lerp, 007AC4F0 a record whose +4 is a signed byte index, and five integer reads of +0xC on 007D0400 / 007D06B0 / 007D0600 descriptors plus 007FF1C0's image arithmetic. The raw candidate 007CA560, with 58 callers, is a float ramp (+8 current, +0xC target, +0x10 / +0x14 time and duration, +0x28 rate), not a Sequence. None of the record's 99 known consumers (the accessor family, every function that calls it, and the walkers 007E5000..007E7000) block-copies it or its entry: their only 16-byte moves over those offsets are stack spills, and none calls memcpy (W3 no block copy). What remains is a copy by code outside those consumers. Control _index/candidates/g2-walk-routes/g2_walk_routes.py (W1-W3, FAILS 0).
  **NARROWED FURTHER 2026-09-27 (OPUS): every caller of the accessor family is followed, and none reads the flag or the float. All 40 functions that call into 007CF500..007CFC80 (rel32 scan, all outside the family) are traced after each call: the returned pointer and the out-descriptor passed in rdx, through one dereference. The engine is live: it finds the seven +4 word reads, the walker's 007E68B0 among them. No byte read at an entry's +8 and no dword or float read at its +0xC follows any call. So the flag and the float are not read through the accessors by anyone. What remains is an indexed walk of the entry table (record + 0x20 + i*16), or a copy of the record into the sound middleware. A raw displacement census of the audio range finds 77 reads at +0x28 (byte) or +0x2C (dword) with no receiver typed; 007CA560 alone has 58 callers. Those candidates are the next step. Control _index/candidates/g2-entry-readers/g2_entry_readers.py (E1-E3, FAILS 0).** *(2026-09-30, SWE2-STRUCT for OPUS: answered - the walk-routes narrowing above closes the indexed and stepped walks, disposes of `007CA560` as a float ramp and finds no block copy among the 99 known consumers (`g2_walk_routes.py` W1-W3); what is left is G-2's SUPERSEDED residue, read with the `SD-24` note below.)*
  *(Note 2026-09-30, SWE2-DATA — `SD-24`: both 2026-09-27 narrowings build on the 2026-09-18 premise corrected above, which put the entry table at the `Sequence` record's `+0x20` ("record + 0x20 + i*16"). The entries the accessors return are the `Sound` record's rows at `u16 +0x1A`, so the traced reads of an entry's `+8` / `+0xC` measure those rows, not the `Sequence` record's `+0x28` / `+0x2C`. The no-reader result for the `Sequence` bytes rests on the 2026-09-17 narrowing: no reader in the reader range and none through a descriptor pair. This correction does not change that.)*
- [x] ~~What `FUN_007bd9d0` measures — the runtime parameter `SwitchSound` switches on. **G-11**.~~
      **Read whole 2026-09-12 (FABLE).** The getter resolves a **named runtime parameter**: when the
      object's virtual `+0x130` says no (`007BD9EF`) and the ~~sequence~~ record is version ≥ 10 of type
      5, it walks to the record's name block (`(rec[+0x23] + 0x10) & 0xF0`, then `+ rec.w02`,
      `007BDA0C`–`007BDA36`) and compares the name — **`"default"`** (`01CB39B8`) → the object's float
      **`+0x514`**; **`"distance"`** (`00D4ACF0`) → the object's float **`+0x508`**, the listener
      distance the spatial update `007D6270` writes; any other name → the by-name lookup `007B0E90`
      (0 when it fails). With no name — the virtual says yes, or the record is older than version
      10 — it returns `+0x514`. ~~**Every shipped sequence record is version 4** (G-13 above), so in~~ In
      the shipped banks `SwitchSound` always switches on the **`default` parameter `+0x514`**, the
      value the parameter setters write (`007BEAE0`, `007BFFA0`, `007D2150`, `007DAFF0` — the
      trigger's parameter push on [the trigger page](sound-trigger.md)); the `distance` and
      by-name switches ~~are reachable only through record generations that do not ship~~ are never reached.
      *(Corrected 2026-09-30, SWE2-DATA — `SD-24`: the record the getter tests is the sound's own `SabFile::Sound` at `this+0x30` (`007BD9FB`). Every shipped one is version 16, so the version test passes. The name path is gated only by byte `+4` = 5, the class byte that builds `SwitchSound`, so a `SwitchSound` whose record carries a name block would switch on it. The shipped banks build none: the class byte is 0 or 1 in all 13,150 records (§12). The conclusion holds for that reason, not because of the version. Control `_index/candidates/dd-leftovers-0930/sd24_record.py` R4, D3.)*
- [x] ~~Why `VariationSound` keeps the base slot 43. **G-8**.~~ **Answered 2026-09-12** — no candidates (slot 37 false); it stores a parameter instead (§2).
- [x] ~~**UQ-262.** Mechanism of `FUN_007bd240`, the trigger itself.~~ **Answered by propagation 2026-09-14 (FABLE):**
  [the sound trigger page](sound-trigger.md) reads it whole. It has a state gate at `+0x54` (6 and 7 refuse and 0 is
  excluded), post-increments `slotCount` `+0x4C` into the 8-byte slot array at `+0x400`, binds the `SabFile::Sequence`,
  takes a handle, applies seven parameter ops in fixed order, and dispatches to playback. `slotCount` is compacted by the
  per-update pass (G-17).

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| All five sit at vtable slot 43 | recovered RTTI vtables | 4 |
| Shared iterate-resolve-trigger shape | decompiled bodies of all five | 1 |
| Candidates are authored `SABSOUNDSEQUENCEINFO` | the vtable symbol `SQEX::Sd::AudioBinaryFile::BaseClass<SQEX::Sd::SABSOUNDSEQUENCEINFO>` appears in four of the five bodies | 1 + 3 |
| `SwitchSound` selects by half-open range | decompiled body of `007E67C0`: `lo <= value && value < hi` guarding the trigger | 1 |
| `FUN_007bd240` is the common trigger | called on the success path of all five | 1 |
| `Random` and `Cycle` call the same accessor; `Order`'s is equivalent | decompiled bodies of `007CF9C0` and `007CF830` — same field, same version test, differing only in returning `byte` vs `bool` | 1 |
| The record format is versioned with a relocating field | `if (1 < version && version != 2) -> +0x10 else -> +0x04` in both accessors | 1 |
| A second, higher version gate exists | `FUN_007bd9d0` requires `version > 9` and `record[4] == 5` | 1 |
| Only the base `Sound` is built from shipped banks | the class-byte census over all 13,150 `snd ` records (§12, `members/sndclass-census.tsv`) | 1 + data |
| The selects are reached only through slot 43, from the stepper `007BD120` | raw `E8`/`E9` index: no direct caller of the five selects; the one `+0x158` call at `007BD205` (UQ-251) | 1 |

**Correction record, 2026-09-02.** The first version of this document described
`FUN_007cf9c0` and `FUN_007cf830` as the differing "per-entry predicate" between variants.
Reading both disproved that: they are one accessor in two return flavours. The earlier wording
was not false about the *call sites* — those genuinely differ — but it implied a semantic
difference that does not exist, and would have sent the next reader looking for meaning in the
wrong place.

**Naming discipline held twice.** The obvious write-up remains "RandomSound picks a random
candidate." Two separate attempts to ground that have now failed — first the shared-predicate
observation, then the predicates turning out identical. The code still has not said it, so the
document still does not. ~~Open as **G-10**.~~ *(Corrected 2026-09-30, SWE2-DATA: G-10 was answered 2026-09-12 (the timer, §2) and the rules are read in §12; `RandomSound` does roll `rand() % 101` (§10, §11).)*

## 9. Related

- [`../sqex-sd-sound-driver-architecture.md`](../sqex-sd-sound-driver-architecture.md) — the class hierarchy
- [`../README.md`](../README.md) — category overview

## 9. Falsification pass 2026-09-02 — the withheld claim, tested

**Attack chosen.** This document does something unusual: it reads the shape of `RandomSound`,
`OrderSound` and `CycleSound` and then **explicitly refuses to say what they do** — *"No claim is
made about randomness or ordering."* That restraint is either well-judged or excessive caution, and
the way to find out is to try to settle the question it declined.

The sharpest form: **does `RandomSound::Select` draw from a random number generator at all?**

> **SUPERSEDED WITHIN THE HOUR — see §10.** The finding below is *literally* true and correctly
> bounded: `RandomSound::Select` uses neither the shared LCG nor MT19937. But the search was scoped
> to those two streams' constants and **did not look for the CRT `rand()`**, which
> `RandomSound::Select` does call. The bounded claim stands; the framing around it did not, and §10
> replaces it.

### The answer is no — and the caution was right

Two independent tests, both negative:

| Test | `RandomSound::Select` (`007E5160`, 1,400 B) |
|---|---|
| RNG among its **callees** | **none** — no `RNG_*`, no MT19937 thunk |
| RNG constants **inlined** in its body | **none** — no `0x41C64E6D`/`0x3039` (shared LCG), no `0x6C078965`/`0x9908B0DF` (MT19937) |

The second test matters more than the first, because this database has already been caught out by
exactly that gap: [`../../21-RNG-And-Determinism/rng-streams.md`](../../21-RNG-And-Determinism/rng-streams.md)
§8b records a consumer census built from **call edges** that missed seven functions inlining the LCG
directly. A call-graph negative alone would prove nothing here.

**The zero was positive-controlled.** The same extraction and search, run over two functions known
to use each stream, finds them immediately:

```
00318510  Loot_RollAdditionalItemChance   ->  g_uSharedGameplayLcgState * 0x41c64e6d + 0x3039   (x3)
0025ABA0  (weather draw)                  ->  RNG_MT19937_NextU32_Thunk()
007E5160  RandomSound::Select             ->  nothing
```

**So `RandomSound::Select` consumes neither of the two documented gameplay RNG streams.** Whatever
selects its entry, it is not the generator that decides loot, weather or enemy chain.

**What this does not establish:** that the selection is deterministic. A driver-local generator
inside `SQEX::Sd`, a counter, or a hash would all be invisible to these two tests. The finding is
bounded exactly as stated — **not the shared LCG, not MT19937** — and the class name `RandomSound`
remains a name from the sound driver's own vocabulary rather than evidence about the shipped rule.

**The document's restraint is vindicated.** Had it written the obvious sentence — *"RandomSound picks
a random entry"* — it would have implied a link to the gameplay RNG that does not exist, and a modder
chasing determinism would have looked in the wrong place.

### SURVIVED exactly: the versioned accessor

§2 gives the accessor rule as `(v >= 3) ? rec[0x10] : rec[4]`. Both accessors read in full:

```c
byte FUN_007CF9C0(ctx) {                    /* used by RandomSound and CycleSound */
    rec = *(byte **)(ctx + 8);
    if ((1 < *rec) && (*rec != 2)) return rec[0x10];
    return rec[4];
}

FUN_007CF830(ctx)  /* used by OrderSound */ — identical, returning (… != 0)
```

`(1 < v) && (v != 2)` is `v >= 3`. **The formula is exact**, and the boolean form is the same test.

### A small distinguishing detail

`CycleSound::Select` calls `007E5E80`, which neither `RandomSound::Select` nor `OrderSound::Select`
does. Since §2 notes Random and Cycle otherwise share the same accessor and second-pass shape, that
callee is the most promising place to look for what actually separates them.

*(Ghidra also lists `00000215` among `007E5160`'s callees. That is not an address in this image — an
artefact of an unresolved indirect call, recorded here so it is not mistaken for a finding.)*

## 10. Correction and completion, 2026-09-02 — there is a third random source

§9 tested `RandomSound::Select` for the two RNG streams this database documents, found neither, and
stopped there. **That was the wrong place to stop.** The function draws from the **CRT `rand()`**,
which neither stream covers and which §9 never searched for.

The bounded sentence §9 actually published — *"consumes neither of the two documented gameplay RNG
streams"* — remains true. What was wrong was treating that as the end of the question when the
obvious next one, *"then what does it use?"*, was one grep away.

### `RandomSound::Select` is a weighted random pick

```c
iVar12 = rand();                                  /* ONE draw, before the loop */
do {
    weight = FUN_007CF9C0(&entry);                /* the versioned per-entry byte */
    if (weight != 0 && (iVar12 % 0x65 <= accumulated + weight))
        select this entry;
    accumulated += weight;
    ...
} while (more entries);
```

`0x65` is **101**. So the rule is: **draw once, take `rand() % 101`, and walk the entries
accumulating their weight bytes until the running total reaches the draw.**

### That settles what the accessor is

§2 describes `FUN_007CF9C0` / `FUN_007CF830` as *"the differing per-entry predicate"*. They are not
predicates. **`FUN_007CF9C0` returns a selection weight** on a 0–100 scale — it is the addend in the
cumulative sum above — and `FUN_007CF830` returns the same byte reduced to a boolean. That is why
`RandomSound` and `CycleSound` use the first and `OrderSound` uses the second.

### The three variants, now separated

| Variant | Draw | Accessor | Rule |
|---|---|---|---|
| `RandomSound::Select` (`007E5160`) | `rand()` once | `007CF9C0` → **weight** | weighted random over the entries |
| `CycleSound::Select` (`007E6360`) | via `007E5E80`, `rand()` once | `007CF9C0` → **weight** | same weighted draw, **plus** cycle position stored at record `+0x01` (set to the chosen index, or `0xFF` when nothing qualifies) |
| `OrderSound::Select` (`007E58D0`) | **none** | `007CF830` → **boolean** | no random draw at all — consistent with stepping in order |

**`OrderSound` having no draw is the cleanest evidence that the other two really are random**, since
all three share the same container walk and differ mainly here.

### A third RNG source — used well beyond audio

The engine has **three** distinct random sources, not two:

| Source | Used by |
|---|---|
| shared gameplay LCG (`0x41C64E6D`/`0x3039`) | loot, enemy chain, rewards |
| MT19937 | weather |
| **CRT `rand()`** (import `0x008C3098`) | **48 sites across 30 functions** — Movement, Combat Action, Combat Formula, Presentation, UI, Audio, and Lua `math.random` |

> **Corrected on the day of writing.** This section first said `rand()` was the sound driver's own
> generator. A full census of the import slot shows it is used across gameplay — including
> `BattleAction_ComputeChargeLimitTicks` and `PartyFollow_SolveFormation` — and that Lua's
> `math.random` is backed by it. See
> [`../../21-RNG-And-Determinism/rng-streams.md`](../../21-RNG-And-Determinism/rng-streams.md) §8g.

`rand()` carries no seed in the save image, so unlike the counter-seeded LCG it is not reproducible
from saved state ([rng-streams](../../21-RNG-And-Determinism/rng-streams.md) §8g, which owns that finding; not re-verified here). **The earlier claim that a sound draw "costs no gameplay draw" is withdrawn**: the
same generator serves both, and whether they share state depends on threading, which is not
established here — `SD-25`. *(2026-09-30, SWE2-STRUCT for OPUS: answered - SD-25, ANSWERED 2026-09-30 (OPUS `d7d7e52c9`, [`sd25-sound-thread-rand-0930`](../../_index/candidates/sd25-sound-thread-rand-0930/README.md)): the selects run on the audio driver's own thread (thread body `007A5400`, which seeds its own stream at `007A540B`), and no gameplay `rand()` caller is in that thread's direct-call closure, so they do not share state.)* On shipped banks the question has no consequence: no `RandomSound` or `CycleSound` object is ever built (§12).

### Verified in the bytes, not from the decompiler's label

The decompiler prints `rand()` in these bodies, but **neither function contains a direct call to
it**. Both reach it through `FF 15` on IAT slot `0x008C3098`, which the import table resolves to
`rand` in `api-ms-win-crt-utility-l1-1-0.dll`. A census of direct `E8` calls to the *statically
linked* `rand` at `0x00861F38` finds one caller and **misses all 48 import-slot sites**. The claim
rests on the import table, not on a printed name.

**A note on the modulus.** `% 101` over `0..100` with a `<=` comparison covers 101 outcomes for
weights that sum to 100 — one more than the loot system's `% 100` with `<`. Whether that is an
off-by-one or deliberate headroom is **not established**; it is recorded as read. *(Corrected 2026-09-30, SWE2-DATA: the behaviour is fully read — a roll of 0 to 100 inclusive against a `<=` running total — and whether it was intended is authorial intent, not a code fact; the path never runs on shipped data (§12). Not a register question.)*

### The methodology point

§9 positive-controlled its zero and still reached a misleading conclusion, because the control only
proved the instrument could find **the constants it was given**. It could not reveal a source nobody
had thought to search for. **A positive control validates an instrument, not the completeness of the
question** — which is the lesson worth carrying, and is why §9 is struck through rather than deleted.

## 11. `G-12` answered — the versioned field is a per-candidate WEIGHT, and the roll is `rand() % 101` (OPUS, 2026-09-15)

`G-12` asked what the versioned field at `+0x04` / `+0x10` *means*. FABLE's 2026-09-12 narrowing
established that the shipped data cannot say: every one of the 11,165 `seq ` records is version 4
and every `+0x10` is `0`, so **"the meaning has to come from the accessor's consumer"**. It does.

**The consumer does not treat the return as a flag.** Across the twelve call sites of `007CF9C0`
and the two of `007CF830` — every call site in the image, by a byte-level `rel32` scan — the value
is used three different ways, and two of them are arithmetic:

| use | site | instructions |
|---|---|---|
| **summed** across candidates | `007E5398`, `007E5F88` | `movzx eax, al` then `add r14d, eax` / `add esi, eax` |
| **compared between two candidates** | `007E54E0` + `007E54EC` | `movzx edi, al`, second call, `cmp dil, al` / `jbe` |
| tested as a gate | `007E523B`, `007E54C8`, `007E611F`, `007E645B`, `007E59BB`, `007E5B08` | `test al, al` with `je` / `jne` |

**A byte that is summed and compared is a number, not a boolean.** `007CF830`'s `!= 0` coercion is
the odd one out, and only `OrderSound` uses it.

### The roll it is compared against

Immediately before the weighted walk in `RandomSound` (`007E5160`):

```asm
007E5325  call  qword ptr [rip + 0xddd6d]   ; -> 008C3098, the process-global CRT rand
007E532B  mov   r14d, esi                   ; running total = 0
007E5330  mov   r12d, eax
007E5333  mov   eax, 0x288df0cb             ; the magic divisor for 101
007E5338  imul  r12d
007E533B  sar   edx, 4
007E5345  imul  ecx, edx, 0x65              ; 101
007E5348  sub   r12d, ecx                   ; r12d = rand() % 101   -> 0 … 100
```

`008C3098` is the IAT slot [the battle-locomotion page](../../06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md)
already resolves to the **process-global CRT `rand`**. Then the walk:

```asm
007E5398  call  007CF9C0                    ; this candidate's field
007E539D  movzx eax, al
007E53A4  add   r14d, eax                   ; running total += weight
007E53A7  call  007CF9C0
007E53AC  test  al, al
007E53AE  je    007E53B9                    ; weight 0 -> skip this candidate entirely
007E53B0  cmp   r12d, r14d
007E53B3  jle   007E5459                    ; roll <= running total -> TAKE IT
```

**That is a cumulative-weight selection.** The field is each candidate's weight; the walk adds
weights until the running total reaches a roll of `0 … 100`, and takes that candidate. Nothing in
the code normalises the weights or checks that they sum to 100, but the `% 101` roll is what makes
"percentage" the natural reading of the unit.

### Why the shipped data shows only zero — and what that costs

A candidate whose weight is `0` is **skipped by the weighted pass** (`test al, al` / `je`). Every
shipped record's field is `0`, so **the weighted pass never selects anything in this build**, ~~and
selection always falls through to the uniform second pass §3 describes~~ *(corrected 2026-10-01, OPUS, per §12: so pass 1 plays every set and the weighted roll finds nothing; there is no uniform second pass)*. The field is live code
serving authored data that does not exist here.

**What this does NOT establish.** The unit is inferred from the modulus, not from an authored table:
no shipped record carries a non-zero weight, so nothing in this build demonstrates a weight of 40
behaving as "40 %". And `G-1` — what actually distinguishes `Random`, `Order` and `Cycle` — is
untouched by this: the weight is read the same way by all of them, and the difference remains loop
structure.

## 12. The three rules, the class selector and the version vocabulary — 2026-09-17 (FABLE)

**What was missing was a definition of the unit the loops step over.** Every walk resolves entry `i`
through `007CFAC0` (a 16-byte `SabFile::SoundSequenceInfo`) and its `u16 +4` key through `007CF9E0`
into a `SabFile::Sequence` record — the RTTI classes behind the descriptor pointers the accessors
return (`01CB6E40`, `01CB4D58`; the sound's own record at `this+0x30` is a `SabFile::Sound`, `01CB43E0`).
Then it compares the **group byte** `007CF9A0` gives (`Sequence +0x11` at version 3 and above, `+5`
below) of the following entries with the current one, and treats a run of equal bytes as **one set**:
the set's first entry decides, its mates follow it. Only the head's weight (`007CF9C0`, `+0x10`) is
consulted.

### `RandomSound::Select` (`007E5160`)

1. **Pass 1** (`007E51F5`..`007E531F`): every set whose head weight is 0 plays, mates included.
2. **Pass 2** (`007E5325`..`007E5454`): one `rand() % 101` roll; the weighted sets are walked adding
   their weights, and the first set whose running total reaches the roll is picked. Nothing picked:
   record `+1` := `0xFF`.
3. **Anti-repeat** (`007E5459`..`007E55B5`): unless record `+0x19` bit 5 is set, a pick equal to the
   last index in `+1` is replaced — by the first other weighted set, then by any later one whose weight
   is greater than the picked set's (`007E54F1`); with no replacement nothing plays and `+1` := `0xFF`.
4. The pick plays with its mates and `+1` remembers its index (`007E55B9`).

### `OrderSound::Select` (`007E58D0`)

1. **Pass 1** (`007E5961`..`007E5AA0`): every set whose head weight is **not** 0 plays; the zero-weight
   sets are counted (`r12d`).
2. **Cursor** (`007E5AA8`..`007E5C7D`): `c = record[+1]`, reset to 0 when `c` is at or past that count;
   the `c`-th zero-weight set plays with its mates and `+1 := (c + 1) mod count` (`007E5BB9`..`007E5BD2`).

So *Order* steps one unweighted set per trigger in authored order and wraps, while its weighted sets
play every time. No random draw.

### `CycleSound::Select` (`007E6360`, helper `007E5E80`)

Pass 1 as Random; then the helper rolls and picks as Random does, but its substitution refuses two
things: the last index in `+1`, and **any set whose group byte is still sounding** — `007E5DA0` walks
the object's active players (`+0x400`, count `+0x4C`, each checked through `007B5070`) and lists the
group bytes of their sequences (`007E5E1A`). Slot 42 re-runs the helper on the interval slot 40 rolled
(§2), so a cycling sound keeps choosing among the sets that are not already playing.

### The class selector

`007B2F70` builds the object from the sound record's **byte `+4`** (`007B30C7`): `0` or `1` the base
`Sound` (`007BC8D0`), `2` `RandomSound` (`007E50A0`), `3` `OrderSound` (`007E5810`), `4` `CycleSound`
(`007E5CD0`), `5` `SwitchSound` (`007E6700`); any other value builds nothing. `VariationSound`
(`007E56E0`) is built on a separate branch of the same factory (`007B3145`). The selects also read the
record's byte `+5` as the candidate count, `+1` as the cursor and `+0x19` bit 5 as the allow-repeat
flag; none of those reads is versioned.

### What the shipped banks make of it

Every shipped `Sequence` record is version 4 with `+0x10`..`+0x17` zero (§7, G-13). So in this build
every head weight is 0 and every group byte is 0: **a sound's whole candidate list is one set**, and
Random and Cycle play all of it on every trigger while Order plays it from the cursor on. `SwitchSound`
hands the same `Sequence` pair to `007CFBF0`/`007CFBC0` (`007E68BA`..`007E68CC`), so its ranges are
`0 <= v < 0` and it can never play. Whether any shipped sound record carries selector 2..5 — whether
these classes are ever built — is an authored question, routed to DATA
(`FABLE-REQ-SWE2-DATA-SOUND-CLASS-BYTE-CENSUS`).

***ANSWERED 2026-09-18 (SWE2-DATA): no. Over all 13,150 shipped `snd ` records (all 4,609 `.sab`
banks, walked through each `snd ` chunk's `{u16 0, u16 0x10, u32 count, u32 offsets[]}` directory),
byte `+4` is `0` in 1,985 records and `1` in 11,165 — every record builds the base `Sound`, and
`RandomSound`, `OrderSound`, `CycleSound` and `SwitchSound` are never constructed from shipped data.
The class-1 count equals the `seq ` record count exactly (9,836 `win` + 1,329 `orb`): a class-1
sound is the one that carries a candidate list, its `+5` always 1, while class-0 records (all in
`win` banks) carry `+5` = 0. Byte `+0x19` bit 5 is 0 in every record — the allow-repeat flag is never
set, which is vacuous anyway once Random and Cycle are gone. So the three rules above are dead
machinery over this corpus: the only selection the game performs is the base class's own path.
Census: `members/sndclass-census.tsv` (13,150 rows), regenerated by
`members/gen_sndclass_census.py`.*

### The version vocabulary, by class (G-13)

| record (RTTI class) | ships | version tests and what each gates |
|---|---|---|
| `SabFile::Sound` | 16 | `>= 2`: four parameter ids `+0x30`..`+0x33` (signed, `-2` absent) and floats `+0x34`..`+0x43`, count `+0x44` (`007BDF06`..`007BDF57`); `>= 12`: ZeroOne-parameter table, offset `+0x4C`, count `+0x4E`, 32-byte rows (`007CFF40`, up to two copied at bind); `>= 10` with class byte `+4 == 5` (`SwitchSound`): the named-parameter block (`007BD9D0`; added 2026-09-30, SWE2-DATA, `SD-24`) |
| its candidate list (`SoundSequenceInfo` rows) | — | `<= 5`: table offset at `+2`; `>= 6`: at `+0x1A` (`007CFACB`) |
| `SabFile::Sequence` | 4 | `<= 1`: no ranges; `2`: weight `+4`, group `+5`, ranges `+4`/`+8`; `>= 3`: weight `+0x10`, group `+0x11`, byte `+8` (`007CF980`, constant 2 below), ranges `+0x10`/`+0x14`~~; `>= 10` with type `+4 == 5`: the named-parameter block (`007BD9D0`)~~ *(moved to the `Sound` row 2026-09-30, SWE2-DATA, `SD-24`)* |
| `SabFile::SoundEffect` container | — | `< 9`: table at `+2`; `9`..`10`: after the aligned header `(+0x23 + 0x10) & 0xF0`; `>= 11`: table at `+0x46` (`007CF780`) |
| ZeroOne curve (`AudioBinaryFile::ZeroOne`) | — | `1`: `+0xA`/`+0xC`; `2`: `+0x12`/`+0x14`; `>= 3`: counted table at `+2`, count `+8` (`007CFE60`); the evaluator normalises by `+8`/`+0xC` from 1 and finds its key table at `+2` (`<= 3`) or aligned by byte `+1` (`007CFD00`) |
| `MabFile` `CustomPointList`, `Layer`, `Meter`, `StartMethod`, `VolumeAutomation` | — | `>= 8`: aligned by byte `+4` |
| `MabFile` `EndMethod`, `Mode`, `Section`, and `007D0710` | — | `>= 9`: aligned by byte `+0x48` |
| `MabFile` `ModeParam` | — | `>= 3`: aligned by byte `+6` (`007D04C0`) |

Those are every version comparison in `007CF000`..`007D0000` plus the four consumers outside it; the
image carries no other history, and the shipped banks sit on one branch of each row.

### G-2, narrowed to its residue

The `Sequence` fields the code consumes are the ones in the table above. The bytes that vary across the
shipped records (`+0x24`, `+0x28`, `+0x2C` float, `+0x30`..) are read by **no accessor in the reader
range and by no audio-range function that loads them through a descriptor pair** (scan of `007A0000`..
`007E9000` for `+0x2C`/`+0x24` reads with pair provenance: none). The sequence player the trigger
`007BD240` builds (`007E6960`) keeps the pair at `+0x20` and reads nothing from it at construction.
Whoever consumes the payload does so through a path this reading did not recognise; that is the residue. *(Dispositioned: G-2 SUPERSEDED 2026-09-27 (OPUS) under FRONTIER's class-1 ruling — every field placed or profiled, the indexed and stepped walk routes closed (§7); noted 2026-09-30, SWE2-DATA.)*

## Cross-subsystem neighbours - SWE2-DATA (pass-22 dispositions, 2026-10-02)

- **CombatAction - CLIENT (3 edges).** `00000215` is also called by bodies filed to combat action: `002F8410`, `002F88B0`, `002FA1A0` - shared machinery across the layer boundary, no shared ownership.
- **CombatFormula - CLIENT (1 edge).** `00000215` is also called by bodies filed to combat formula: `00384B10` - shared machinery across the layer boundary, no shared ownership.
- **Gameplay - SERVICE (1 edge).** `00318510` reaches bodies filed to gameplay: `0030B0E0` - shared machinery across the layer boundary, no shared ownership.
- **Movement - CLIENT (7 edges).** `00000215` is also called by bodies filed to movement: `003343D0`, `00334E00`, `00336E40` (+4 more) - shared machinery across the layer boundary, no shared ownership.
- **Presentation - CLIENT (3 edges).** `00000215` is also called by bodies filed to presentation/rendering: `0029F130`, `003BBD00`, `00530E40` - shared machinery across the layer boundary, no shared ownership.
- **Rewards_Progression_Economy - CLIENT (1 edge).** `00318510` is also called by bodies filed to rewards/progression: `003180F0` - shared machinery across the layer boundary, no shared ownership.
- **SaveLoad - CLIENT (1 edge).** `00000215` is also called by bodies filed to save/load: `00866200` - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT (1 edge).** `00000215` is also called by bodies filed to UI: `0055B3F0` - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT and SERVICE (2 edges).** `0025ABA0` is also called by bodies filed to world area: `0025ACA0`; `0025ABA0` reaches bodies filed to world area: `002658B0` - shared machinery across the layer boundary, no shared ownership.

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-sound-variant-selection-ee-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `007B0E90` | 249 B | returns -1 when `rdx` is null or the signed dword count `02EAD3EC` is not positive; otherwise it scans the 0x40-byte entries starting at qword `02EAD3F8`, comparing the zero-terminated string at `q` + word `[q+2]` (with `q` = each entry's qword `+8`) byte by byte with `rdx`, and returns -1 when none matches; for the first match it stores to float `[rcx]` the entry's float `+0x1c` when its float `+0x24` equals 0.0, and otherwise `007A9E50(+0x20 / +0x24, edx = dword +0x2c)` times (`+0x1c` - `+0x18`) plus `+0x18`, and returns 0 | `007B0EC5`, `007B0EEB`, `007B0F29`, `007B0F58`, `007B0F7F` |
| `007CA560` | 236 B | computes a start value that is float `[rcx+0xc]` when the fifth (stack) argument byte is non-zero or float `[rcx+0x14]` equals 0.0, and otherwise `007A9E50([rcx+0x10] / [rcx+0x14], edx = dword [rcx+0x1c])` times (`[rcx+0xc]` - `[rcx+8]`) plus `[rcx+8]`; it stores that value to `[rcx+8]`, `xmm1` to `[rcx+0xc]`, `xmm2` to `[rcx+0x14]`, 0 to dword `[rcx+0x10]`, `r9d` to dword `[rcx+0x1c]` and 1 to byte `[rcx+0x20]`, and when dword `[rcx+0x24]` is 1 it divides the distance between `xmm1` and the start value by the absolute float `[rcx+0x28]` (when `xmm1` is above the start) or `[rcx+0x2c]` (otherwise) and stores that quotient to `[rcx+0x14]` when `xmm2` is not at least it; it returns 0 | `007CA56A`, `007CA5B0`, `007CA5D2`, `007CA606`, `007CA631` |
| `007CF780` | 142 B | reads `h` = qword `[rcx+8]` and the sign-extended index `r8d`, and writes to the output pair at `rdx` the address `01CB6E80` followed by `h` plus a dword offset: for byte `[h]` below 9 the offset is the dword at `h` + word `[h+2]` + index*4; for 9 or 10 it uses `pad` = (byte `[h+0x23]` + 0x10) masked with 0xf0 and the offset is `pad` plus the dword at `h` + word `[h+2]` + `pad` + index*4; for 11 or more the offset is the dword at `h` + word `[h+0x46]` + index*4; it returns `rdx` | `007CF78E`, `007CF79A`, `007CF7C5`, `007CF7D2`, `007CF7F6` |
| `007CFE60` | 209 B | reads `h` = qword `[rcx+8]` and writes the address `01CB6E10` to `[rdx]` and a pointer to `[rdx+8]`: for byte `[h]` = 0 the pointer is 0; for 1 it is `h` + word `[h+0xa]` when `r8d` is zero (then setting byte `+6` of it to 1) and `h` + word `[h+0xc]` otherwise (setting byte `+6` to 2); for 2 the same with words `[h+0x12]` and `[h+0x14]`; for any other type the pointer is `h` plus the dword at `h` + word `[h+2]` + `r8d`*4 when `r8d` is not negative and below byte `[h+8]`, and 0 otherwise; it returns `rdx` | `007CFE6D`, `007CFE92`, `007CFEA6`, `007CFEF6`, `007CFF22` |
| `007D0710` | 142 B | writes the address `01CB6E10` to `[rdx]` and to `[rdx+8]` either 0, when `r8d` is negative or not below byte `[h+0x43]` of `h` = qword `[rcx+8]`, or `h` plus the dword at `h` + word `[h+2]` + (bytes `[h+4]` + `[h+5]` + `[h+0x41]` + `[h+0x42]` + `r8d`)*4 + `pad`, where `pad` is (byte `[h+0x48]` + 0x10) masked with 0xf0 when byte `[h]` is 9 or more and 0 otherwise; it returns `rdx` | `007D0719`, `007D0727`, `007D0738`, `007D0770`, `007D0799` |
| `007E6620` | 222 B | calls the vtable slot `+0xa8` of `rcx` and, when it returns 2, calls `007E5DA0(rcx, rsp+0x20)` and, when that is below byte `+0x18` of `t` = qword `[rcx+0x30]`, subtracts `xmm1` from float `[rcx+0x538]` and, when the result is not above 0.0, calls `007E5E80(rcx)` and stores (dword `[t+0x10]` + the signed remainder of the value returned by a call through the qword at `008C3098` by (dword `[t+0x14]` - `[t+0x10]` + 1)) times 0.001 to `[rcx+0x538]`; on every path it then returns `007BF0A0(rcx)` with the incoming `xmm1`; the stack cookie is checked through `00808C40` | `007E6643`, `007E666F`, `007E6685`, `007E66B0`, `007E66E1` |
| `007E6960` | 227 B | stores `01CB8FA0` to qword `[rcx]` and `01CB4D58` to `[rcx+0x20]`, zeroes qwords `+0x8`, `+0x10`, `+0x18`, `+0x28`, `+0x30`, `+0x60`, `+0x90`, `+0x9c` and `+0xb0`, words `+0x98`, `+0xa4` and `+0xbc`, bytes `+0x5c` and `+0xa9` and dwords `+0xac`, `+0xb8` and `+0xc0`, stores the float 1.0 bit pattern to dwords `+0x38`, `+0x3c`, `+0x40`, `+0x54`, `+0x58` and `+0x68` and as a zero-extended qword to `+0x44` and `+0x4c`, then for four iterations stores byte 0xfe at `+0x6c` onward and the float 1.0 to dword pairs at `+0x70` onward (stride 8), and returns `rcx` | `007E6967`, `007E697F`, `007E69D1`, `007E6A20`, `007E6A3F` |
