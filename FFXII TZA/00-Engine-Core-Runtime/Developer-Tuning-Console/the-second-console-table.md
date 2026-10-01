---
system: The second console table
category: 00-Engine-Core-Runtime
status: DOCUMENTED — what the codes name answered 2026-09-30 (map-pack codes indexed by field id, 599 of 601 agree with map_ref.bin); the two entries that name a different pack are explained (RC-6, answered); the +0x4A2 byte corrected 2026-09-30 to the scene key mUseLinearTonemap, written by the scene-config loader; the bypassed accessor is not dead (four callers, 2026-09-18); owner read 2026-09-30 (OPUS, `_index/candidates/dd-owner-read-b1-0930/` round 3)
owner_layer: CodeDomain:DeveloperConsole; no PrimaryOwner
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
last_reviewed: 2026-09-03
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: pair-frontier-repos-55
  crossref_clean: false
  reopened_count: 0
---

# The second console table

**The console's row renderer has two per-id tables, not one.** The label table — `ctx + id*8 + 0x130`,
293 names — was recovered earlier. **This is a second, static one, and it holds authored asset codes.**

## The read, and the correction that had to come first

```asm
001CDBE6  mov  rdx, r8          ; the id
001CDBE9  add  rdx, rdx         ; id * 2
001CDBF7  mov  rax, qword ptr [rsi + rdx*8 + 0x1CD6E68]
```

**`rsi` holds the image base.** The displacement is an **RVA**, so the table is at **`01DF6E68`**, not
at the address in the instruction.

> **This document's author read `01CD6E68` as an address and dumped it — one tick after being warned
> that this exact class of row exists.** The dump returned plausible-looking 16-byte records and
> **nothing in it announced that it was the wrong memory.**
>
> **A wrong address does not fail; it returns something.** The only reason the error surfaced is that
> the "pointers" in it did not look like pointers.

## What the table holds

**Sixteen bytes per id**, the load taking the **qword at the entry base**:

```
01DF6E68   008F7508   1        -> "ous0101"
01DF6E78   0          2
01DF6E88   0          3
```

**and the strings the first entry points into are a packed run of eight-byte records** — seven
characters and a NUL, **three letters then four digits**:

```
ous0101  nal0101  nal0201  rwr0101  nal0301
```

> **A sparse per-id table of short authored codes**, most entries null, each paired with a small
> integer that counts up with the index.

**What the codes name is not established here.** They are the shape of an authored asset or area
identifier — **three letters and a four-digit number** — and **nothing in this function says which.**

**Answered 2026-09-30 (SWE2-CONTRACT): they are map-pack names, and the table is indexed by field id.** The table is
1,314 entries long, not 294 (the contract's I-7 and its 2026-09-25 correction; the console reads one entry by the id
it holds at `+0xAB4`). Joining entry *i* with row *i* of `map_ref.bin`'s per-field census
([`map-ref-field-packs.tsv`](../../03-World-Area-Field/Map-Pack/members/map-ref-field-packs.tsv), FABLE 2026-09-17: the
pack each field loads in its own mode) gives **599 of the 601 populated entries equal to the field's own pack name**
(`ous0101` at 0 → `ous0101.mpk`, `rui0108` at 200, `dst0104` at both 230 and 232, `rbn1001` at 295, `mrm0204` at 600;
4 of the 599 match one candidate of a size-ambiguous census name). The same join shifted by one field agrees for only
198 of 601, so the agreement is bound to the index, not to neighbouring fields sharing packs. This also answers the
contract's "why `dst0104` appears at two ids": fields 230 and 232 both load `dst0104.mpk`. Control:
[`console_codes_vs_mapref.py`](../../_index/candidates/swe2contract-ddres-b1-0930/console_codes_vs_mapref.py)
(output `console_codes_vs_mapref.out`; control: entry 0 decodes to `ous0101` and the sequence word equals index + 1 for
all 1,314). Tier 1 + authored data (static). *Not claimed:* that the engine reads this table to load a map — the join
shows what the codes name, and the console is its only known reader.

- [x] **RC-6.** Why two populated entries name a different pack than `map_ref.bin` gives their field: entry 670
  `rbl0102` against `rbl0121.mpk`, entry 1003 `gil0301` against `gil0303.mpk`. Registered 2026-09-30 (SWE2-CONTRACT).
  **ANSWERED 2026-09-30 (authored data; SWE2-CONTRACT on FABLE's record `rc789-fable-0930` (commit `8bdf31fcb`)): the table records map codes, and both fields
  load a pack other than the map the code names.** Field 1003 is the only field that owns `gil0303.mpk`, a variant pack
  of `gil0301` with no art of its own (its bytes carry `gil0301`'s codes); field 670, like 671, loads `rbl0121.mpk`,
  and `rbl0102` ships only an effect bank, no map pack, map JSON or art. *Not claimed:* why the entries were left so.

## The accessor that this reader bypasses

The same field the renderer reads at `+0xAAC` **has a dedicated nineteen-byte accessor:**

```asm
0017D490  sub  rsp, 0x28
0017D494  call 0x001D50D0        ; fetch the owning object
0017D499  mov  eax, dword ptr [rax + 0xaac]
0017D4A3  ret
```

**The renderer does not call it.** It reads `[r15 + 0xAAC]` directly from an object it already holds.

*(2026-09-18, FABLE: the accessor is not dead — `0017D490` has four callers in the edge list, `0025ACA0`, `002620E0`, `00265920` and `WorldField_InitializeCurrentFieldRuntimeParameters` `0026D910`, so the field is read through it by the world-field initialisation and around it by the console renderer.)*

*What `+0xAAC` holds (2026-09-30 pointer, SWE2-CONTRACT):* the weather-slot debug override, `debugWeatherSlotOverride`
(`s32`, a positive value forces the slot), read through `0017D490` `WorldField_GetDebugWeatherSlotOverride` at
`0026D921` / `0026D92A` / `00265924` ([the weather contract](../../03-World-Area-Field/CONTRACT-weather.md);
[the weather slot state model](../../03-World-Area-Field/Weather/weather-slot-state-model.md), tier 2: the authored
format string `Weather Slot:%d (Triangle/Cross to toggle)` prints `[singleton+0xAAC]`). Both readers use the same
object: the accessor fetches the `0x10E8`-byte console settings singleton from `001D50D0` (cached at `01F81428`), and
the renderer's context is that singleton too, since it reads the labels at `+0x130 + 8 × id` that `001CCB20`, the
singleton's constructor, clears and `001D0390` fills ([slice B](arm-catalogue-slice-B-ids-44-75.md)'s caller box).

> **Two consumers of one field, one through a named accessor and one around it** — so **anything
> hooking the accessor sees the weather reader and not the console.** That is invisible from either
> function and is exactly what the pair census surfaces.

## A second console channel: one byte the glyph path reads

> **Corrected 2026-09-30 (SWE2-CONTRACT), read from the bytes; regression
> [`second_table_4a2_key.py`](../../_index/candidates/swe2contract-ddres-b1-0930/second_table_4a2_key.py).**
> Three identifications in this section were wrong, and the instructions it quotes are right:
> 1. `001C977B` is not a console arm. It lies inside `001C7940`, the scene-config loader (11,445 B), not inside the
>    console dispatcher `001D1660`. The section's own RESOLVED paragraph below already places `001C978E` in `001C7940`.
> 2. The byte is not `ShadowValueB`. In the loader's idiom the key is the `lea rdx` before the lookup `001FF740` that
>    precedes the read. For `+0x4A2` that key is **`mUseLinearTonemap`** (`001C9725` / `001C9744`), read as an
>    integer by `00200B80` and stored as `== 1` (`cmp eax, 1 / sete bl`). The `lea` after the store is the **next**
>    setting's key. The control applies the same rule to the float store before it (`001C972F`) and gets
>    `mMapObjectShadowFadeRange`.
> 3. `0018F316` is not a glyph-record builder. It lies inside `0018EEE0`, the post-process frame build, which copies
>    the byte into the frame parameters `+0x9A`. Step 6 of the post-processing chain reads it: with `+0x98` clear the
>    mode is `+1` if `+0x9A` is set and `−1` otherwise ([the post-processing contract](../../17-Presentation-Rendering/Post-Processing/CONTRACT-post-processing-subsystem.md)
>    step 6; `_types/fields.tsv`, `PostProcessFrameParams +0x09A`).
>
> The object written is `00193D50`'s render-parameter block `PostProcessParamContext` (`+0x4A2`, write `001C977B` in
> `_types/fields.tsv`). So the channel is: the scene's `mUseLinearTonemap` → block `+0x4A2` → frame `+0x9A` → the
> tonemap mode's sign. The text below is kept as written.

**A different pair row, same shape.** `+0x4A2` is ~~**written by a console arm**~~ written by the scene-config loader (`001C977B`) and
~~**read by the glyph-record builder**~~ read by the post-process frame build (`0018F316`) — two functions in two documents, neither citing the
other.

```asm
; the console arm writes it, then looks up a NAMED render parameter
001C977B  mov  byte ptr [rax + 0x4a2], bl
001C9781  call 0x001FF740            ; EASTL_LookupByCString
001C978E  lea  rdx, [0x8FA928]       ; -> "ShadowValueB", "EnableIBL", "lightShaftColorR", ...

; the glyph-record builder copies it into the record it is filling
0018F30C  movzx eax, byte ptr [rsi + 0x164]
0018F313  mov   byte ptr [rdi + 0x21], al
0018F316  movzx eax, byte ptr [rsi + 0x4a2]
0018F31D  mov   byte ptr [rdi + 0x9a], al
```

> **The console writes a byte on one object; a render-record builder copies it to `+0x9A` of another.**
> **Neither function names the channel and no document connected them.**

**CORRECTED 2026-09-03 — the `lea` is not a table base.** A census of the parameter-name region
`008FA700`–`008FAB00` found **93 references, all 93 landing exactly on a string start, none mid-string,
and no pointer array into the region anywhere in the image.** The strings are **variable-length and
packed**, so the region **cannot be indexed by stride** and nothing indexes it by pointer.

> **An address that looks like a base is a specific datum** — the inverse of the image-base trap two
> sections above. ~~**`lea rdx, [0x8FA928]` selects one parameter, and the string at exactly that address
> is the answer: `ShadowValueB`.**~~ *The first half stands: the `lea` selects one parameter. The second is superseded
> (2026-09-30, see the correction at the head of this section): that `lea` selects the next setting; `+0x4A2`'s key is
> `mUseLinearTonemap`.*

**And it is not a second naming scheme.** The C-strings are **the scene-config keys** — names like
`mMapAmbientColorR` and `mMapFarPlane` already appear in the console frame's own name-to-offset table.
**The console is a consumer of the same authored data the scene-config loader reads**, not the owner of
a parallel scheme.

**RESOLVED 2026-09-03: there was never a disagreement between censuses, only a bad summary in one.**
The true split is **84 references in `001C7940` and 9 in `001C3D50`** — **the two scene-config
loaders** the console frame document already names. `001C3D50` ends at `001C4F4F`, nowhere near
`001C978E`.

> **A summary line counted an *owner* column and was read as counting *functions*, because the eight
> rows printed happened all to agree with that reading.** *93 rows existed; 8 were looked at.*

**And the corrected split is more informative than the claim it replaced**, because it exposes
something the wrong version hid: **`ShadowValueB` has three references** — one in one loader, two in
the other, the instruction here being one of them.

> ***A census of a name counts lookups, not settings.***

## Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Is the table really at `01DF6E68`? | The instruction's base register is the image base (`+0x120000`), and **the corrected address contains pointers into the string region while the raw one did not.** |
| Is the stride 16? | `id` is doubled, then scaled by 8 in the addressing mode — **`id × 16`.** |
| Are the strings eight bytes each? | Five consecutive seven-character runs, each NUL-terminated, **no padding between them.** |
| Is `+0xAAC` the same field in both readers? | **Same displacement, same width, both `read`** — and the accessor's own body does nothing else. **Whether the two hold the same object type is not established**; the accessor fetches its object, the renderer already has one. *Answered 2026-09-30 (pointer, SWE2-CONTRACT): the same object, the console settings singleton from `001D50D0` — see "The accessor that this reader bypasses".* |
| Could the accessor be dead? | **Not established.** It has a document of its own from the weather work; this document says only that **the renderer does not go through it.** *Answered 2026-09-18 (FABLE): not dead — four callers (same section).* |

**What this document does not claim:** what the codes identify, what the small integers beside them
count, how many entries the table has, what `+0xAAC` holds, **which named render parameter the `+0x4A2`
arm selects**, or what `+0x9A` of a glyph record does with the byte it receives.
*All six are answered since (2026-09-30, SWE2-CONTRACT): the codes are map-pack names by field id (above; residue
RC-6); the integer is index + 1 and the table has 1,314 entries (the contract I-7); `+0xAAC` is the weather-slot
debug override; `+0x4A2` is `mUseLinearTonemap == 1`, and `+0x9A` of the post-process frame parameters sets the
tonemap mode's sign (the correction above).*

*(Pass 22 adjacency, 2026-09-14: `001C3D50` calls **presentation** `001CC9A0` and `001C7940` is
called by `001C7290`/`001C61F0` (3 edges) — the second table's accessors sit inside the same
render-path neighbourhood as the first table's.)*

## What the player sees (SWE2-CONTRACT, 2026-09-30)

Nothing in a retail game. This table belongs to the developer menu, which the retail build never opens: the menu
prints the name of a map's data pack beside the current field's number, the kind of readout a developer uses to see
which map is loaded. One of the two values this page follows does reach players, indirectly: whether a map's lighting
file asks for linear tonemapping decides the sign of one setting of the post-processing pass that colours every frame.

## Key addresses (SWE2-CONTRACT, 2026-09-30)

| Address | Working name | Body | Role |
|---|---|---:|---|
| `001CD0E0` | console row renderer | 11,276 B | reads the code table at `001CDBF7` and `+0xAAC` directly |
| `001D50D0` | console settings singleton getter | 66 B | the `0x10E8`-byte object cached at `01F81428` |
| `0017D490` | `WorldField_GetDebugWeatherSlotOverride` | 20 B | returns `[singleton + 0xAAC]` |
| `0026D910` | `WorldField_InitializeCurrentFieldRuntimeParameters` | 418 B | one of the accessor's four callers |
| `001C7940` | map scene-config loader | 11,445 B | writes `+0x4A2` from `mUseLinearTonemap` at `001C977B` |
| `001C3D50` | cutscene scene-config loader | 4,607 B | the other loader of the same key family |
| `001FF740` | keyed lookup wrapper | 300 B | the lookup each key goes through |
| `0018EEE0` | post-process frame build | 1,581 B | copies `+0x4A2` to the frame parameters `+0x9A` at `0018F31D` |

### Data addresses cited by this document (SWE2-CONTRACT, 2026-09-30)

| Address | Name | Kind | Contents |
|---|---|---|---|
| `01DF6E68` | authored-code table | `.data`, 1,314 × 16 B | `{char* code, u32 index + 1, u32 0}`; 601 codes |
| `008FA700`–`008FAB00` | scene-config key strings | `.rdata` | packed C strings, 93 references, no pointer array |

## Call chain (SWE2-CONTRACT, 2026-09-30)

```
developer menu (not opened in retail)
  -> 001CD0E0 row renderer
       code = qword[01DF6E68 + fieldId * 16]          (fieldId from the singleton's +0xAB4)
       reads [singleton + 0xAAC]
field init 0026D910, 0025ACA0, 002620E0, 00265920
  -> 0017D490 -> 001D50D0 -> [singleton + 0xAAC]       (the weather-slot override)
map load: 001C7940 -> 001FF740("mUseLinearTonemap") -> 00193D50 block +0x4A2 = (value == 1)
frame:    0018EEE0 -> frame parameters +0x9A -> post-process step 6: mode +1 / -1
```

**Upstream (who causes this):** the developer menu for the table; map loading for the `+0x4A2` byte.

**Downstream (what this causes):** a printed pack name; the weather slot forced when the override is positive; the
sign of the post-process mode in step 6.

**Do not confuse with:** the console's label table (`ctx + id*8 + 0x130`, 293 names) and the `map_ref.bin` field
table the codes agree with.

## Modding notes (SWE2-CONTRACT, 2026-09-30)

- **Best intervention point:** for the tonemap sign, the map's scene JSON key `mUseLinearTonemap`; the loader stores
  only whether it equals 1.
- **Inert for gameplay:** the code table has no known reader outside the developer menu, so editing it changes only
  that readout.
- **Regenerates itself:** `+0x4A2` is re-written on every map load that reaches the key.
- **Multiplayer / XIIOnline:** all three are local presentation state.

## Evidence — claims, evidence and tier (SWE2-CONTRACT, 2026-09-30)

| Claim | Evidence | Tier |
|---|---|---|
| The table is at `01DF6E68`, 16-byte entries, `+0x08` = index + 1, 1,314 long | `001CDBF7` read as an RVA; the contract I-7 / D6 / D7; `console_codes_vs_mapref.py` control | 1 |
| The codes are the field's own map-pack name for 599 of 601 entries | `console_codes_vs_mapref.py` against `map-ref-field-packs.tsv`, with the shifted-join control | 1 + authored data |
| `+0xAAC` is the weather-slot debug override and both readers read one object | the weather contract; the weather slot state model; slice B's singleton trace | 1 (access) + 2 (format string) |
| `+0x4A2` = `mUseLinearTonemap == 1`, written by `001C7940` | `second_table_4a2_key.py` K1, K2 | 1 |
| `+0x9A` sets the step-6 mode sign | `second_table_4a2_key.py` K3; the post-processing contract step 6 | 1 |
| The key-name region has 93 references, none mid-string, no pointer array | the 2026-09-03 census in this page | 1 |

## Crossings into other layers — FINAL-AUDIT pass 22 (OPUS, 2026-09-18)

**Ten edges over four layers, through four of this page's subjects — and a console table is the one
kind of page where that is expected**, because a tuning console's entries exist to reach into
whatever they tune.

**Audio — four edges, and it is the busiest.** `00265920` is called by three audio bodies
(`002DE800`, `00361810`, `00363B40`, 830 to 982 bytes), and `002620E0` calls the last of those.
**Four edges, one console entry and one audio pathway**, in both directions.

**Script/VM native bridge — three edges, all inbound.** `00265920` is reached from a 29-byte
adapter (`00356250`) and a 59-byte one (`0050D360`); `0026D910` is reached from a 99-byte one
(`003565C0`). **All three are small adapters** — the shape of a verb calling a console entry rather
than of the console reaching into the VM.

**ActorEntity — two edges through one subject.** `002620E0` calls a 66-byte actor routine and is
called by the actor field-runtime pass. *Both are named by role: each would import a Movement edge
this page does not mention, and the field-runtime pass would import Party as well.*

**RNG — one edge, and the carrier is five bytes with sixty-six neighbours.** `0025ACA0` calls the
Mersenne-Twister next-u32 **thunk**. *Named by role for the same reason — that five-byte forward is
reached from combat action, combat formula and rewards, none of which this page mentions. A thunk
being tiny is not the same as a thunk being cheap to cite.*

**Nothing in any of the four layers is owned here.** The page documents a console table's entries;
what an entry tunes belongs to the layer it tunes.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings become reportable once citations written 0x... or FUN_... count (R5); tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Input — CLIENT.** A 66-byte function this page cites is called by `InputManager_TranslateBindingProfileToControlState` and by two Input bodies (100 and 105 bytes).
- **Save_Load_Settings — MECHANICAL (4 edges).** 4 calls from page-cited bodies into shared Save_Load_Settings plumbing (`SaveImage_GetPersistentPayloadBase` (002EF2B0)) - the helpers' general call surface, not a Save_Load_Settings relationship of this page's subjects.
- **Platform — SERVICE (1 edge).** 1 outbound (page-cited `001CCB20` call Platform bodies `005CC930`).
- **Resource — CLIENT and SERVICE (3 edges).** 1 inbound (Resource bodies `001A7A50` call page-cited `00193D50`, `001CD0E0`, `001D1660`); 2 outbound (page-cited `001CD0E0`, `001D1660` call Resource bodies `0020C700`, `002EEEE0`).
