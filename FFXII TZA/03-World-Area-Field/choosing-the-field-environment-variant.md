---
system: Choosing the field environment variant
category: 03-World-Area-Field
status: DOCUMENTED — every register row is closed (owner re-status 2026-09-30, OPUS) — ~~what the selector's three states mean to a player is not established~~ the selector is the field's weather slot, one of three authored weather configurations (CONTRACT-weather section 1, reconciled 2026-09-30); GB-1 (defect or design of the two-slot divergence) is NO ADMISSIBLE SOURCE; 00377850 (the 3-bit weather preset extractor) and 002E3D40 (the weather-to-presentation refresh) read 2026-09-18 (status line current 2026-09-30, SWE2-DATA)
owner_layer: PrimaryOwner:WorldAreaField
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 5 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-30
falsification_passes: 1
archive_formats:
  - "MRF | explained | map_ref.bin (.bin member; MRF\x02): header offsets to an 8-byte-per-field records array (+4), a 16-byte block array (+8) and two lookup arrays (+0x10, +0x18) - (kind 9, 4) by 00268750 into 02099D88, read by WorldField_InitializeCurrentFieldRuntimeParameters 0026D910"
  - "testarearef | explained | test_area_ref.bin (.bin member): u16[321] ascending, entry k = first map_ref row with area word k - (kind 9, 2) by MapRef_BeginLoadResources 00268750 into 02099D98, which nothing reads (raw sweep: two stores); section 'The two test_ siblings'"
  - "testmapref | explained | test_map_ref.bin (.bin member; kind-9 index 1): 274 headerless 8-byte rows in the map_ref row shape {u16, i16, u16 area, u16 group}, an older/partial table - no requester found; section 'The two test_ siblings'"
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: first-read-repos-55
  crossref_clean: false
  reopened_count: 0
---

# Choosing the field environment variant

`WorldField_InitializeCurrentFieldRuntimeParameters` at **`0026D910`**, 418 bytes.

~~**Eleven documents cited this function — the most-cited unopened function in the database — and none~~
~~had opened it.**~~ *(Corrected 2026-09-30, SWE2-DATA: that count was the 2026-09-03 census and has no anchor here. Today 22 pages outside `_index/` cite `0026D910` (`pf_env_checks.py` E7), and it is read in full on this page and in [the weather contract](CONTRACT-weather.md).)* It is the step that decides, on entering an area, **which authored variant of that
area's environment you get**, and publishes the answer as ~~five globals~~ four globals the rest of the engine reads *(corrected 2026-09-30, SWE2-DATA: its rip-relative stores hit exactly `02099DA8`, `02099DAC`, `02099DB0` and `02099DBC`, `pf_env_checks.py` E4; the committed slot itself is the payload byte `+0x1060`)*.

## The finding that has to come first, because it changes what the pseudocode means

**`0026D910` ends in a tail call, and the decompiler presents the callee's body as part of it.**

```asm
0026DA88  xor  r9d, r9d
0026DA8B  xor  r8d, r8d
0026DA8E  xor  edx, edx
0026DA90  xor  ecx, ecx
0026DA92  mov  byte ptr [rax + 0x1061], 0
0026DAAD  jmp  0x002E3D40          ; <- a tail call, not a continuation
```

`002E3D40` is **its own 116-byte function in the ledger**. Everything the pseudocode shows after that
point — the π/6 and π/8 rotations, the `0.15` bias, the two matrix composes — **belongs to
`002E3D40`, not to this function**, and a reader working from pseudocode alone would attribute up to
116 bytes of behaviour to the wrong name.

> **A tail call is a call. The decompiler renders it as a body, and a body is what a reader will
> believe.**

**And the four argument registers are zeroed immediately before the jump**, so at *this* call site
`002E3D40` receives `(0, 0, 0, 0)`. **The values in that trig block are constants here, not
quantities flowing out of the field setup** — which is precisely the false connection an inlined
rendering invites.

~~This is the **fourth** distinct way this executable's decompiled output has misdescribed a function~~
~~boundary — after an unmodelled `xmm0` return, a return through a tail call, and a `void` on a~~
~~function that returns its source object. **Three were about the return; this one is about the body.**~~
*(Struck 2026-09-30, SWE2-DATA: the three earlier cases are not cited, so the count has no anchor. The tail-call finding above stands on its own, `pf_env_checks.py` E1.)*

## What it actually does

**Pick a variant index, look up the field's authored row, publish ~~five~~ four globals.** *(Corrected 2026-09-30, SWE2-DATA, per SWE2-AUDIT-SEM's batch-4 review C2 (`_index/candidates/auditsem-review-dd-owner-read-4-0930/REVIEW.md`): the stores hit exactly `02099DA8`, `02099DAC`, `02099DB0` and `02099DBC`, as the corrected line above says.)*

```
selector  = clamp(count - 1, 0, 2)                 ; 0, 1 or 2
if [ctx + 0x1061] == 0:  [ctx + 0x1060] = selector ; a latch: first writer wins
fieldId   = WorldTransition_GetActiveOrPendingFieldId()   ; 003148F0
```

*(Corrected 2026-09-30, SWE2-DATA: `count` is the weather slot the caller requests in `ecx`, authored `1..3`. When the debug override `0017D490` (dword `+0xAAC` of the debug singleton) is positive, it replaces the request (`0026D91F`–`0026D92F`, `pf_env_checks.py` E2). Between the latch and the field lookup, the committed slot is published through `00180620` (`0026D96F`–`0026D976`, E5), which the block above omits.)*

The table is a loaded file image at global **`02099D88`** *(the file is `map_ref.bin`, kind 9 id 4, loaded by `00268750`;
named 2026-09-13 in [the resource path directory](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md) §13)*, addressed entirely by header offsets — a
records array at `header[+4]`, a 16-byte-stride block at `header[+8]`, and two lookup arrays at
`header[+0x10]` and `header[+0x18]`. The field's row is `records + fieldId*8`; its first `u16` is
carried forward, and its `+2` `s16` selects the 16-byte block entry, **offset by
`([ctx+0x1060] + 1) * 4`** — so **the variant selector is an index into the row, not a separate
table.**

| global | written |
|---|---|
| `02099DA8` | `header[+0x10]` array looked up by the selected byte, when in range |
| `02099DAC` | `0` if `00377850(rowU16, selector+1)` returns 0, else **`1` or `2`** — `(result > 3) + 1` |
| `02099DB0` | the selected entry's byte `+2` |
| `02099DBC` | `header[+0x18]` array looked up by the same byte; **pre-zeroed at entry** |

**`02099DAC` is a three-state result compressed from an arbitrary one** — `0`, `1`, `2` — where the
boundary between `1` and `2` is *"greater than 3"*. **A function returning a count is being read as a
band**, and the bands are not equal in width.

**Then the latch is released** (`[ctx+0x1061] = 0`), so the selector written earlier is consumed
exactly once.

## The two `test_` siblings of `map_ref.bin` (2026-09-29, SWE2-DATA)

*`OPUS-REQ-DATA-BUCKET-MEMBER-FORMATS`; check [`b3_test_refs.py`](../_index/candidates/bucket-members-0929/checks/b3_test_refs.py), 30 checks, FAILS 0.*
Kind-9 indices 1 and 2 of the path array that holds `map_ref.bin` at index 4 name two more files.
They are two different layouts, and neither is read.

- **`test_area_ref.bin` (index 2, `ch` and `in`, 642 bytes) is loaded and never read.**
  `MapRef_BeginLoadResources` `00268750` requests `(9, 2)` (`lea ecx, [rdi+9]` / `lea edx, [rdi+2]`
  at `00268811` / `0026880E`, call `00268814`), takes a buffer from `00267930` and stores it in
  **`02099D98`** (`00268829`); the completion is registered at `0026883E`. A raw sweep of that slot
  finds exactly two references, both stores (`00268772` zeroes it first, `00268829` publishes it),
  and no `lea` of a base in `02099D80`–`02099D98` reaches it through a displacement. The bytes are
  `u16[321]`, strictly ascending: **entry k is the index of the first `map_ref.bin` row whose word
  `+4` equals k** — the area index `MapRef_GetAreaArdFieldResourceIndex` returns (`00264EF9`) — so
  it is an area → first-field index derived from `map_ref`, 321/321 on both copies, and not a copied
  section of it.
- **`test_map_ref.bin` (index 1, `common`, 2,192 bytes) has no requester found.** It is 274
  headerless 8-byte rows in the `map_ref` row shape `{u16, i16, u16 area, u16 group}` with the same
  non-decreasing word `+4`, but only 14 of its 274 rows equal `map_ref`'s row at the same index and
  its area word stops at 124 (`map_ref`: 320) — an older or partial table, not a prefix. The two
  `(9, 1)` constant pairs in the image reach `00252B40` and `003E12A0`, neither a request API; the
  sweeps cannot see a kind/id computed at run time at a register-held request site.

## What this document does NOT claim

- ~~**What the five globals feed.** They are published here; their consumers are not in this function.~~
  *(Answered by reconciliation 2026-09-30, SWE2-DATA: [the weather contract](CONTRACT-weather.md) §5 censuses the readers. `02099DA8` and `02099DAC` are read through getter thunks by the combat stage, `02099DBC` through a third getter, and `02099DB0` by nothing (GB-3, answered; `pf_env_checks.py` E8).)*
- **What `00377850` computes** from `(rowU16, selector+1)`. Only how its result is banded.
  *Read 2026-09-18 (FABLE), by cross-reference:* it is the **3-bit weather preset**. `00377850` tail-calls the packed-bit reader `003777C0` with `(bit 0, width 3)`, whose bit base is `9 × (3 × selector + slot)` ([the MWeather page](Weather/mweather-resource-format.md)), so the band above is preset 0 / presets 1–3 / presets 4–7, the last the strong-wind class that page names.
- ~~**What the variant selector means to a player** — three states exist and are chosen from a count,~~
  ~~but nothing here names them.~~ *(Answered by reconciliation 2026-09-30, SWE2-DATA: the selector is the field's weather slot. Each area has three authored weather configurations, a retention roll picks one on entry, the choice survives save and load, and `setweatherslot` can force it ([the weather contract](CONTRACT-weather.md) §1). The page's "What the player sees" section states it.)*
- **Whether the two-slot divergence is a defect or a design.** This function takes the combat class from the requested slot and the presentation from the committed one. GB-1 records that the question is **NO ADMISSIBLE SOURCE**: the code is read end to end, and no evidence in the image or data can say which was intended.
- **What `002E3D40` does.** It is a separate function, reached by tail call, and it deserves its own
  read rather than a paragraph borrowed from a rendering error.
  *Read 2026-09-18 (FABLE):* it is the **weather-to-presentation refresh**. With a non-zero first argument it passes its three arguments straight to the Presentation backend init `0040AAD0`; with zero — this page's call — it computes them itself: the current field (`003148F0`), its MapRef primary value (`00264F10`), the weather slot (`00265920`), then the three extractors `00377850`, `003777A0`, `003777B0` (`002E3D60`–`002E3D8F`), and tail-calls `0040AAD0` with preset, azimuth sector and elevation class (`002E3DAF`). The trig block the pseudocode showed belongs to that backend init, on the MWeather page.

## What the player sees (SWE2-DATA, 2026-09-30)

Every field area has three authored weather configurations. When you enter an area, one of them is put in force, and
this function is the step that applies it. The sky and lighting follow the slot through the presentation refresh it
tail-calls. The combat side follows it through `02099DAC`, the weather class the damage formula reads, so the same
choice decides whether the weather is strong enough to change a spell's power ([the weather contract](CONTRACT-weather.md) §1). A story script can force a
slot, and the choice survives save and load. The decision itself (the retention roll) is made before this function
runs; this function commits and publishes it.

## Key addresses (SWE2-DATA, 2026-09-30)

| address | role |
|---|---|
| `0026D910` | this function: commit the weather slot and publish the environment values (418 B) |
| `0017D490` | the debug slot override: returns dword `+0xAAC` of the debug singleton; a positive value replaces the requested slot |
| payload `+0x1060` / `+0x1061` | the committed slot (`0..2`) and the restore latch, in the object the payload getter returns |
| `00180620` | publishes the committed slot's environment parameter bank (`0026D976`) |
| `003148F0` | `WorldTransition_GetActiveOrPendingFieldId`: the field whose `map_ref` row is read |
| `02099D88` / `02099D90` | the loaded `map_ref.bin` image and its loaded guard |
| `02099DA8`, `02099DAC`, `02099DB0`, `02099DBC` | the four published globals (table above) |
| `00377850` | the 3-bit weather preset extractor, banded into `02099DAC` |
| `002E3D40` | the weather-to-presentation refresh, reached by the tail jump at `0026DAAD` |

## Call chain (SWE2-DATA, 2026-09-30)

```
field entry: the field-runtime init -> the retention roll -- tail --> 0026D910(slot)
script:      the setweatherslot verb handler (clamps to 1..3)     --> 0026D910(slot)
boot:        the bootstrap environment apply                      --> 0026D910(1), twice (D-2)

0026D910
  -> 0017D490              debug override (twice)
  -> the payload getter    five times
  -> 00180620              environment bank publication (committed slot)
  -> 003148F0              current field id
  -> 00377850              weather preset -> 02099DAC band (requested slot)
  -- tail --> 002E3D40(0, 0, 0, 0) -> the presentation backend init (committed slot)
```

The three callers are named by role; [the weather contract](CONTRACT-weather.md) §6 gives their addresses and the order they run in.

## Modding notes (SWE2-DATA, 2026-09-30)

- The variant data is `map_ref.bin` (`MRF` `02`), not code: a field's row `+2` picks a 16-byte block, and the block's
  lanes 1–3 (bytes `+4`, `+8`, `+0xC`) are weather slots 1–3. Lane 0 is never read, because the slot index is biased
  by one.
- A slot request outside `1..3` saturates silently, so passing 0 gives slot 1 and 9 gives slot 3.
- The combat class comes from the requested slot and the sky from the committed one. When the restore latch fires,
  they can differ ([the weather contract](CONTRACT-weather.md) §4, I-7). An edit that changes only one lane can therefore show one slot's sky with another's
  combat weather.
- `02099DB0` (lane byte `+2`) ~~is written and never read, so editing that byte has no effect in the shipped build.~~ is written, and no reader is found (GB-3). *(Corrected 2026-09-30, SWE2-DATA, per SWE2-AUDIT-SEM's batch-4 review C11: GB-3 bounds the negative to rip-relative readers, so the page no longer claims editing it has no effect.)*

## Evidence (SWE2-DATA, 2026-09-30)

| claim | evidence | tier |
|---|---|---|
| tail call into `002E3D40` with zeroed arguments | `0026DA88`–`0026DAAD`; [`pf_env_checks.py`](../_index/candidates/dd-data-4-0930/pf_env_checks.py) E1 | 1 |
| slot = requested `ecx` or the positive debug override, clamped to `0..2` | `0026D91F`–`0026D943`; E2, E3 | 1 |
| exactly four globals stored; `map_ref` root and guard loaded | rip-relative census of the body; E4 | 1 |
| the environment bank is published for the committed slot | `0026D96F`–`0026D976`; E5 | 1 |
| the table image is `map_ref.bin` | shipped file magic and header; E6 | 1 |
| what the globals feed | [the weather contract](CONTRACT-weather.md) §5 reader census; GB-3; [`pf_env_checks.py`](../_index/candidates/dd-data-4-0930/pf_env_checks.py) E8 | 1 |
| what the slot means to a player | [the weather contract](CONTRACT-weather.md) §1 | 1 |

## Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Is the trig block part of this function? | **No.** `0026DAAD` is `jmp 002E3D40`, and `002E3D40` is a distinct 116-byte function in the ledger. Caught by disassembling the tail rather than trusting the pseudocode. |
| Does the function's 418-byte extent cover everything the decompiler showed? | **No, and that is the same finding.** The extent is right; the *rendering* crosses it. |
| Is `[ctx+0x1061]` a flag or a byte of something larger? | Read **and written as a byte** at two sites (`0026DA92` writes `0`), adjacent to `+0x1060` which holds the selector. Treated as a latch, not asserted as a boolean type. |
| Are the header offsets a struct or coincidence? | Four distinct offsets (`+4`, `+8`, `+0x10`, `+0x18`) each used as a base for a different array, all relative to one global. ~~**Consistent with a loaded file image; not proven to be one.**~~ *(Corrected 2026-09-30, SWE2-DATA: it is one: `map_ref.bin`, magic `MRF` `02`, header `+4` = `0x30`, `pf_env_checks.py` E6.)* |

## Why it was never opened

It headed this database's **"leaned on and never opened"** cut: **418 bytes, cited by eleven
documents, no interior anchor anywhere.** The most-cited function nobody had read.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

`WorldTransition_GetActiveOrPendingFieldId` (`003148F0`, 27 B) is one of the most widely read world accessors. Every
crossing below is a **CLIENT** of it: something in another layer asks *which field am I in*. The page's variant rule
depends on none of them.

- **UI.** Five UI-filed bodies of 170–1,827 bytes ask for it.
- **Script_VM_Native_Bridge.** Two script-verb bodies (29 B and 36 B) ask for it.
  - A 99-byte verb body calls `WorldField_InitializeCurrentFieldRuntimeParameters` (`0026D910`).
  - Two verb bodies (79 B and 15 B) reach `002E3D40`.
- **Movement.** A 4,006-byte movement body and two helpers in the `003EDxxx` range ask for it.
- **ActorEntity.** `BattleSlotMap_InitializeMappingClasses` and `ActorManager_RunFieldRuntimePass` ask for it.
- **CombatAction.**
  - `BattleUnit_TryTriggerNearbyAuthoredFieldAction`, the trigger test of
    [walking into an authored trigger point](walking-into-an-authored-trigger-point.md), asks for it.
  - A 477-byte sibling also asks for it; that sibling also queries `PersistentFlag_QueryBank512Low` and draws the
    gameplay MT.
- **Spawn_Encounter_Lifecycle.** `SpawnKeep_RotatePersistenceBanksForAreaTransition` asks for it.
- **Audio.** The 335-byte Audio-filed body that also reads the persistent payload base asks for it
  ([field record accessors](CONTRACT-field-record-accessors.md), crossings).
- **PlatformOnlineAchievements.** The 212-byte achievement-side caller asks for it
  ([the world tick](../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md) names that edge).
- **Presentation - CLIENT and SERVICE (5 edges).** `003148F0` is also called by bodies filed to presentation: `002B7B80` (UI), `002BAF80` (UI); `002E3D40`, `0040AAD0` reach bodies filed to presentation: `0040AAD0`, `0040B3B0` - shared machinery across the layer boundary, no shared ownership.
- **Resource - SERVICE (2 edges).** `00268750` reaches bodies filed to resource: `0032E400`, `0032E620` - shared machinery across the layer boundary, no shared ownership.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Save_Load_Settings — CLIENT.** `SaveImage_FinalizeHeaderAndChecksum`, owned by that layer, calls `003148F0` on this page. That caller is the header finalisation, in a `0x70`-byte frame with a stack cookie, taking a byte and a dword from its caller before it touches the image; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).
