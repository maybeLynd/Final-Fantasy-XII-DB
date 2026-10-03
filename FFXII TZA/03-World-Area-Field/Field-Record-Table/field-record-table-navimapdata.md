---
system: Field record table — the shipped `navimapdata.bin`, all three bytes, and the statuses bit 15 overrides
category: 03-World-Area-Field
status: AUDITED
owner_layer: PrimaryOwner:WorldAreaField (the table and its seven accessors) — consumed engine-wide
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
  authored_data:
    navimapdata_bin_md5: 74bf21a8ec128bdfcfb441137b04d0a8
    vbf_path: ps2data/image/ff12/{in,ch,cn}/bin/navimapdata.bin
last_reviewed: 2026-09-08
archive_formats:
  - "PLMN | explained | planmapname.bin (.bin member): (kind 1, 32) requested by 00378540, published to 02ADD0F8 by 00378BB0; field and area names read by 00377B60 / 00377870 through the u16 offset table"
  - "NAV | explained | navimapdata.bin (.bin member; NAV\x02): the three-byte-per-area field record table - (kind 9, 8) published to 02ADD100 by 00378B80, its accessors on this page"
audit:
  passes: 1
  last_pass: 2026-09-02
  last_pass_state: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  crossref_clean: true
  reopened_count: 1
---

# Field record table — the shipped data, all three bytes, and the statuses bit 15 overrides

> The per-area table that tells the engine *"this is a town"*. Its most-consulted bit waives the
> rule that a knocked-out, petrified or vanished character is out of play — and this document
> names those three states, names the file the table is shipped in, and lists every area that
> sets the bit.

This document closes the three questions the
[bit 15 action-permission document](field-record-bit15-action-permission.md) left open:
**C-9** (what statuses `0x80000003` actually is), **C-10** (which fields set bit 15) and
**C-11** (the other fifteen bits of the record and the third byte).

## 1. What the player sees

Three things can take a character out of a fight for good: being **KO'd**, being turned to
**Stone**, and — for enemies — simply **vanishing without a trace**. A character in any of those
three states is, as far as the battle system is concerned, *not there*: they cannot act, they
cannot be given commands, they earn no EXP or LP from the fight, monsters will not spawn near
them or hate them, and the game will not even bother running damage on them.

**Inside a town, that rule is switched off.** Migelo's Sundries, The Sandsea, the Clan Hall,
Muthru Bazaar, Bhujerba's Travica Way, Balfonheim's Sea Breeze Lane, Archades' Molberry, every
Aerodrome, the airship's Sky Saloon and Air Deck, Jahara, Eruyt Village, Mt Bur-Omisace, the
Nalbina cells you begin the game in — in **193 of the game's 1,154 areas** the engine stops
treating a KO'd or petrified party member as absent. That is why a fallen character still behaves
like a party member while you shop, talk and walk around, instead of being frozen out of
everything the moment you cross the gate.

It is not the battle system that decides this. It is **one bit in the map's own data file**, one
three-byte record per area, shipped in a file called `navimapdata.bin`. The same three bytes also
hold which page of the in-game **Map** the area appears on, and a per-area choice of *which party
member the game focuses on by default* that the shipped game never actually uses.

Walk into a different zone and the same character in the same condition can be treated
differently. Nothing on screen tells you this is happening.

## 2. Native mechanism

### 2a. Where the table comes from

`00378540` is the World/Area/Field boot-time registration routine. It asks the resource system
for authored tables and installs a ten-byte publisher for each. ~~**Three were read here; two more~~
~~were found on 2026-09-08 and are marked below.**~~ The routine is 943 bytes ~~and has been read only~~
~~at the registration sites an operand scan pointed to, so five is a floor, not a total~~ and installs seven *(answered: the 2026-09-14 note below; `00378540` makes seven `0032E620` submissions; 2026-10-02, OPUS)*:

| Requested as | resource `(kind, index)` | Publisher | Global | Shipped file |
|---|---|---|---|---|
| `"MapNo"` + `"MapName"` | (1, 32) | `00378BB0` | `02ADD0F8` | `planmapname.bin` (magic `PLMN`) |
| **`"MapInfo"`** | **(9, 8)** | **`00378B80`** | **`02ADD100`** | **`navimapdata.bin`** (magic `NAV\x02`) |
| `"MapNo"` + `"MWeather"` | (9, 39) | `00378F70` | `02ADD0B0` | `gramap_weatherinfo.bin` (magic `GRMI`) |
| *(not read)* | (9, 40) | `00378B90` | `02ADD0D0` | **`mapjumpgroupinit.bin`**, 116 B — added 2026-09-08 |
| *(not read)* | (9, 41) | `00378A50` | `02ADD0A8` | **`eventmemorylist.bin`**, 26 B — added 2026-09-08 |

*(2026-09-14 — NOCALLER-INSTALLERS: the full member list is now bound. `00378540` installs **seven**
publishers, not five — `00378BA0` and `00378F80` were missed by the earlier operand scan. All seven
are the same ten-byte shape `mov eax, ecx; mov [rip+…], rax; ret`, and the string keys for the two
previously unread rows are now decoded:*

| Requested as | resource `(kind, index)` | Publisher | Global | interior |
|---|---|---|---|---|
| `"FOTTBL"` | (9, 9) | `00378F80` | `02ADD0C0` | `00378F82` |
| `"MJGP_ROM"` | (9, 10) | `00378BA0` | `02ADD0C8` | `00378BA2` |
| `"MJGPINIT"` | (9, 40) | `00378B90` | `02ADD0D0` | `00378B92` |
| `"EVTMEM"` | (9, 41) | `00378A50` | `02ADD0A8` | `00378A52` |

*All seven are no-caller frontier functions — a raw E8/E9 scan finds zero call sites for
`00378B90` too; like the other six it is reached only through its lea-installed registration.
`FOTTBL` (9,9) and `MJGP_ROM` (9,10) slot immediately after `MapInfo` (9,8) in the same kind — a
run of four adjacent map-table indices — and `EVTMEM` (9,41) is `eventmemorylist.bin`, the last
request the installer issues.)*

> **The two added rows come from the flag-bank side, by this document's own method.** Their
> registration sites are `003787B5` and `0037881A`; their publishers are address-taken by `lea`
> and have **zero `E8` and zero `E9` callers**, which is why a call-graph pass did not surface
> them. Their consumers are `PersistentFlag_ApplyAuthoredInitialPrimarySet` and
> `EventMemory_QueryDefinitionIdAbsent`; the derivation, the path-array controls and the
> `.fst` sizes are in
> [`persistent-flag-banks.md` §8f](../../14-Story-Event-Quest-Hunt/persistent-flag-banks.md).
> The “Requested as” column is blank for both because ~~**the string keys were not read**~~ *(answered: decoded 2026-09-14, the note above; 2026-10-02, OPUS)* — only
> the `(kind, index)` pair and the publisher.

The `(kind, index)` pair indexes the executable's own file table — a `.data` array of path
pointers, the same space the shipped `FileSizeTables\FileSizeTable_*.fst` sizes. The MapInfo and
MWeather requests are **31 slots apart in the same kind**, and `navimapdata.bin` and
`gramap_weatherinfo.bin` sit exactly 31 slots apart in that array. Both files then parse *exactly*
under their own readers — see §8, where this identification is attacked rather than asserted.

The publisher is a curiosity worth recording: it stores the delivered value **zero-extended from
32 bits** (`mov eax, ecx` / `mov [rip+…], rax`), yet every reader dereferences the global as a
pointer. The engine has a matching `ImageAddress_ResolveRuntimePointer` convention elsewhere, so
the resource arena evidently lives below 4 GB. Recorded, not explained — open question **PROPOSED-repos2d-4**.

### 2b. The record and its seven accessors

Every accessor bounds-checks the same way and **fails to a fixed default record** rather than
reading out of range — `0x0FFF` for the `u16`, `0` for the third byte. That default matters: it is
the *permissive* value for the navigation-map id (`0xFFF` = "none") and the *restrictive* value for
~~every flag.~~ every flag but the third byte's bit 0, which `00377700` reads inverted, so its default is the permissive 1 *(corrected 2026-10-02, OPUS: `00377713 je` / `00377718 jae` → `00377728 xor dl, dl`, then `0037772D not` / `0037772F test al, 1` and `0037773C mov eax, 1` unless the save veto `00314A60` fires)*.

| Accessor | Reads | Takes | Reached by |
|---|---|---|---|
| `00377C20` | bit 15 | *(active-or-pending field)* | 65 direct callers + 47 through thunk `00313F60` |
| `00377480` | bit 15 | explicit field id | `ActorManager_BindLoadedDefinitionPayload` |
| `00377A40` | bit 14 | explicit field id | 5 UI functions |
| `00377BA0` | bits 12-13 | *(active field)*, save-overridable | 4 functions, **only through tail-call thunk `00320160`** |
| `003779F0` | bits 0-11 | explicit field id | 9 functions — UI, achievements |
| `00377700` | third byte, bit 0 | *(active field)*, save-gated | 6 ActorEntity / Movement functions |
| `00377C70` | third byte, bits 4-6 | *(active field)* | `PartyFocus_SelectAndRequestDefaultActor`, `BattleGroup_RefreshFourActorDefinitions`, `0031C000` |

Nothing reads bits 1-3 of the third byte, although the shipped data sets them. Nothing sets bits
4-6 of the third byte, although the engine reads them. Both halves of that statement are
falsifiable and were tested — §8.

### 2c. What bit 15 does, and what it overrides

`00377C20` is consulted by more distinct subsystems than any other gameplay function in the
executable. In **117 of the 173 instructions** in the image that test the constant `0x80000003`,
a call to `00377C20` or its thunk stands within a few instructions of the test. The pairing is the
mechanism: *the mask asks "is this unit out of play?", the field record asks "does that matter
here?"*

The three masked bits are **status ids 0, 1 and 31**, because the status engine converts an id to
a bit with `1 << (id & 0x1f)`. Their identities are established in §2d.

### 2d. C-9 — the three statuses are KO, Stone and Vanished

`BattleStats_ChangeStatusAndProcessSideEffects` (`0030E360`) owns every status transition. It
keeps **three** 32-bit status masks per combatant and a six-way operation mode, and the terminal
behaviour lives in a `switch` on the status id at the end of the function:

- **status 0** — no presentation event; runs the unit's defeat cleanup (`00300FC0`) and then
  `BattleUnit_ProcessDefeatRewardsAndLoot`. `BattleStats_ModifyHPAndProcessLethalState` applies it,
  in add-mode 3, when HP reaches zero — two call sites, both `xor r8d, r8d`.
  **Corrected 2026-09-03:** this document first said status 0 was the *only* id passed as a
  constant anywhere. It is not — see the corrected census in §8 and the correction trail. What
  survives, and is what the argument needs, is that **no native call site adds status 1 or 31 by
  constant**: they arrive from authored data.
- **status 1** — emits presentation event `0x200C`, then the same defeat cleanup and rewards.
- **status 31** — emits presentation event `0x200E`, then the same defeat cleanup and rewards.
- removing any of the three enters `BattleUnit_RecoverFromTerminalStatusSetIfClear`, which recovers
  the unit **only once all three are clear**.

That is why one mask covers exactly these three ids: they are the three ways a unit permanently
leaves play, and they share one recovery path.

The shipped authored data names them. `listhelp_status.bin` is a 32-entry help-text list in status
id order, and `status_data.bin` is the status definition table the engine itself indexes
(`stride = *(u16*)(base+8)` = 40, records at `+0x20`, 32 of them, file size exact):

| id | Player-facing text, verbatim from `listhelp_status.bin` |
|---:|---|
| **0** | *"The character has lost consciousness and cannot move or act. Remove with a tuft of Phoenix Down."* — **KO** |
| **1** | *"The character has been turned to stone and cannot move or act. Remove with a Gold Needle."* — **Stone** |
| **31** | *"The character has vanished without a trace. The effect cannot be reversed."* — ~~**Vanished**~~ **X-Zone** *(corrected 2026-10-02, OPUS: status 31's name in bank 5, this page's 2026-09-26 note)* |

The alignment of that list to the id space is not taken on trust; it is cross-checked against the
engine's own table in §8, and the checks are what make this claim tier 1 rather than tier 9.

Two consequences worth stating plainly:

- **Stone is a terminal state, Petrify is not.** Status 2 is *"turning to stone… once the count
  reaches 0"*, carries a 45-unit default timer in `status_data.bin`, and is **not** in the mask.
  Status 1 is the finished state, has no timer, and *its* definition record clears status 2.
- **Vanished is the engine's own "remove from the world" state.** Its definition record clears
  every status from 2 to 30 — everything except the other two members of `0x80000003`.

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `00377C20` | `FieldData_GetActiveFieldRecordBit15` | 78 B | bit 15 for the active-or-pending field |
| `00313F60` | thunk → `00377C20` | 5 B | 47 further callers reach the predicate here |
| `00377480` | `FieldRecord_GetBit15ByFieldId` | 61 B | bit 15 by explicit field id |
| `00377A40` | `FieldRecord_GetBit14ByFieldId` | 67 B | bit 14 by explicit field id |
| `00377BA0` | `FieldRecord_GetBits12To13OrSaveOverride` | 102 B | bits 12-13, save-flag override |
| `00320160` | `thunk_FUN_00377ba0` | 5 B | the **only** route to `00377BA0` |
| `003779F0` | `FieldRecord_GetNavigationMapIdByFieldId` | 72 B | bits 0-11, `0xFFF` → `-1` |
| `00377700` | `FieldRecord_GetThirdByteBit0Inverted` | 77 B | third byte bit 0, gated by a save flag |
| `00377C70` | `FieldRecord_GetDefaultFocusCombatantId` | 68 B | third byte bits 4-6 |
| `003148F0` | `WorldTransition_GetActiveOrPendingFieldId` | 27 B | supplies the field id |
| `00378540` | `WorldAreaField_RequestAuthoredMapTables` | 943 B | requests ~~all three map tables~~ seven authored tables *(corrected 2026-10-02, OPUS: seven `0032E620` submissions in `00378540`; §2a's 2026-09-14 note)* |
| `00378B80` | `FieldRecord_PublishLoadedTable` | 10 B | publishes into `02ADD100` |
| `00378BB0` | `MapName_PublishLoadedTable` | 10 B | publishes into `02ADD0F8` |
| `00378F70` | `MWeather_PublishLoadedTable` | 10 B | publishes into `02ADD0B0` |
| `00377CC0` | `WorldAreaField_BootMapTables` | 233 B | the sole caller of `00378540` |
| `00377B60` | `MapName_GetFieldNameById` | 45 B | `PLMN` field-name reader, bound at `+4` |
| `00377870` | `MapName_GetAreaNameById` | 49 B | `PLMN` area-name reader, base `+4`, bound `+8` |
| `003778B0` | `MapName_GetActiveAreaName` | 68 B | same, for the current area |
| `0032E400` | `Resource_GetFileSizeByKindAndIndex` | 80 B | `(kind, index)` → size |
| `0032E620` | `Resource_SubmitRequest` | 340 B | async request + completion callback |
| `00314A60` | `SaveFlags_GetPayload1062Bit0` | 24 B | gates `00377700` |
| `00314AA0` | `SaveFlags_GetPayload1062Bit7` | 24 B | selects the `00377BA0` override |
| `00314AC0` | `SaveFlags_GetPayload1063Bits4To5` | 27 B | the override value |
| `0030D9A0` | `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` | 105 B | bit 15 → mode 3 |
| `0030E360` | `BattleStats_ChangeStatusAndProcessSideEffects` | 1,323 B | owns all 32 status transitions |
| `0030E990` | `BattleStats_RemoveStatusMode0` | 35 B | wrapper, status id stays in `r8` |
| `0030EAE0` | `BattleStats_AddStatusMode3` | 38 B | wrapper, status id stays in `r8` |
| `00300530` | `BattleStats_ModifyHPAndProcessLethalState` | 880 B | applies **status 0** when HP hits 0 |
| `00301140` | `BattleUnit_RecoverFromTerminalStatusSetIfClear` | 452 B | recovery only when all three clear |
| `003876D0` | `BattleStatus_ComputeDefaultShortTimer` | 88 B | reads the definition record's `+9` |
| `003299B0` | `BattleUnit_DispatchActorPresentationEvent` | 83 B | carries `0x200C` / `0x200E` |
| `00312280` | `BattleUnit_ProcessDefeatRewardsAndLoot` | 857 B | the reward path all three enter |
| `00326500` | `PartyFocus_SelectAndRequestDefaultActor` | 274 B | consumes third-byte bits 4-6 in mode 3 |
| `003266C0` | `BattleGroup_RefreshFourActorDefinitions` | 1,253 B | same accessor, three call sites |
| `0026C8C0` | `ActorManager_BindLoadedDefinitionPayload` | 1,330 B | sole caller of `00377480` |
| `003F92B0` | `FUN_003f92b0` | 216 B | bit 14 → area-name display |
| `003160C0` | `FUN_003160c0` | 212 B | navigation-map id vs a seen-map bitmap |
| `0026A1D0` | `FUN_0026a1d0` | 178 B | Movement consumer of third-byte bit 0 |
| `00338490` | `PartyFollow_SolveFormation` | 4,101 B | tests the mask **without** the waiver |
| `002F8BB0` | `Reward_ComputeExperienceForRecipient` | 430 B | mask gate, no waiver |
| `002F90C0` | `Reward_ComputeLicensePointsForRecipient` | 179 B | mask gate, no waiver |
| `00321D30` | `BattleEnmity_WriteAllCombatantIds` | 141 B | mask gate |
| `002350C0` | `SpawnLifecycle_CheckAndRetireByNativeRange` | 529 B | mask gate |
| `00234DA0` | `Spawn_ValidateCandidateDistanceToPlayers` | 290 B | mask gate |
| `00264F90` | `MapRef_GetPersistenceGroupId` | 49 B | supplies the area id to `003778B0` |

**Which names are recovered and which are authored here.** Rows whose name the ledger already
carries — `FieldData_GetActiveFieldRecordBit15`, `WorldTransition_GetActiveOrPendingFieldId`,
`thunk_FUN_00377ba0`, `MapRef_GetPersistenceGroupId`, `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15`,
`BattleStats_*`, `BattleStatus_ComputeDefaultShortTimer`, `BattleUnit_*`, `PartyFocus_*`,
`PartyFollow_SolveFormation`, `BattleGroup_RefreshFourActorDefinitions`,
`ActorManager_BindLoadedDefinitionPayload`, `Reward_*`, `BattleEnmity_WriteAllCombatantIds`,
`SpawnLifecycle_CheckAndRetireByNativeRange`, `Spawn_ValidateCandidateDistanceToPlayers`,
`BattleMenu_BuildCommandEntryList` — are quoted **verbatim from the ledger**. The rest
(`FieldRecord_*`, `MapName_*`, `Resource_*`, `SaveFlags_*`, `WorldAreaField_*`) are **working
names authored by this document** for functions the ledger leaves as `FUN_*`; nothing rests on
them.

### Data addresses cited by this document

| Address | Name | Kind | Contents |
|---|---|---|---|
| `02ADD100` | field record table pointer | `.data` qword | `navimapdata.bin` once loaded |
| `02ADD0F8` | map/area name table pointer | `.data` qword | `planmapname.bin` once loaded |
| `02ADD0B0` | MWeather table pointer | `.data` qword | `gramap_weatherinfo.bin` once loaded |
| `02EBF118` | status definition table pointer | `.data` qword | `status_data.bin` once loaded |
| `022C51F0` | per-kind file-size table pointers | `.data` array | indexed by resource kind |
| `01DFE0B4` | status timer scale | `.data` u32 | multiplies the definition's `+9` byte |
| `0030E88C` | status operation-mode jump table | **`.text` data**, 6 × u32 image-relative | the six mode targets of `0030E360`; sits immediately after that function's body, which ends at `0030E88B` |

## 4. Data structures and formulas

### The field record table (`navimapdata.bin`)

```
FieldRecordTable          base = DAT_02ADD100
  +0x00  u32   magic          'N''A''V' 0x02        (0x0256414E little-endian)
  +0x04  u32   fieldCount     1154 in the shipped file  <- the bound every accessor tests
  +0x08  ...   records, stride 3 bytes

FieldRecord               at base + 8 + 3*fieldId
  +0x00  u16   flags         little-endian, assembled from two byte loads
  +0x02  u8    thirdByte     packedOptions in the type store (OPUS 2026-09-16)

  flags bits 0-11   navigationMapId    0xFFF = none  (003779F0 returns -1)
  flags bits 12-13  2-bit field, save-overridable    (00377BA0)
  flags bit  14     area-name display flag           (00377A40)
  flags bit  15     ACTION-PERMISSION OVERRIDE       (00377C20 / 00377480)

  thirdByte bit  0  the same "safe area" flag, for a different consumer  (00377700)
  thirdByte bits 1-3  set in the shipped data, READ BY NOTHING
  thirdByte bits 4-6  default focus combatant id     (00377C70) - never set in shipped data
  thirdByte bit  7    never set in shipped data, read by nothing
```

The exact reader, transcribed from `00377C20`:

```c
uint FieldData_GetActiveFieldRecordBit15(void)
{
    uint id   = WorldTransition_GetActiveOrPendingFieldId();
    u16  rec  = (base != 0 && id < *(u32*)(base+4))
                  ? *(u8*)(base + 8 + 3*id) | (*(u8*)(base + 9 + 3*id) << 8)
                  : 0x0FFF;                    /* the fail-closed default record */
    return rec >> 15;
}
```

`0x0FFF` is literal in the fail path (`mov edx, 0xfff` / `shr edx, 0xf`) and is not an artefact of
returning zero — the compiler folds a real default record, which is how we know the *authored*
default is "no navigation map, no flags".

The five sibling extractions, same record:

```c
navigationMapId = (rec & 0x0FFF) == 0x0FFF ? -1 : (rec & 0x0FFF);   /* 003779F0 */
areaNameFlag    = (rec >> 14) & 1;                                  /* 00377A40 */
twoBitField     = SaveFlags_GetPayload1062Bit7()                    /* 00377BA0 */
                    ? SaveFlags_GetPayload1063Bits4To5()
                    : (rec >> 12) & 3;
safeAreaFlagInv = ((~thirdByte & 1) && SaveFlags_GetPayload1062Bit0() == 0) ? 1 : 0;  /* 00377700 */
defaultFocusId  = (thirdByte >> 4) & 7;                             /* 00377C70 */
```

### Under layout validation — 2026-09-10

The two shapes above were established in this document in a plain code block, so
`check_layouts.py` never saw them. They are declared as fences here, which puts them under the
same validator every other recovered format answers to. **No new evidence** — this is the same
layout, restated in a form an instrument can check.

```struct NavimapdataHeader base=file
+0x00  u32  magic       'N' 'A' 'V' 0x02, little-endian 0x0256414E; 10,314 of 10,314 files
+0x04  u32  fieldCount  1154 in the shipped file - the bound every accessor tests
```

```struct FieldRecord base=header+8+3*fieldId
+0x00  u16  flags      assembled from two byte loads, so alignment is never assumed
+0x02  u8   thirdByte  a separate byte, not padding
```

**Three bytes, and the stride is what proves the record is not padded to four.** Every accessor
indexes `base + 8 + 3*id` and reads `flags` as two **separate byte loads** OR-ed together
(`*(u8*)(base+8+3*id) | (*(u8*)(base+9+3*id) << 8)`) rather than as a `u16` — which is exactly what
a compiler must emit for a 2-byte field at an odd address. A reimplementation that declares
`struct { uint16_t flags; uint8_t third; }` gets a 4-byte record from the C alignment rules and
every field past the first indexes wrong.

The bit assignments within `flags` and `thirdByte` are in §4 above and are deliberately **not**
repeated as fence fields: the fence records the physical layout, and a bitfield's placement is a
reading of the consumers, not a byte offset.

### The gate this table exists to answer

The engine-wide predicate, exactly as it is compiled (`mov eax,[rsi+0x64]` / `or eax,[rsi+0x3c]` /
`test eax, 0x80000003`):

```c
outOfPlay(unit) = ((*(u32*)(bkbi + 0x64) | *(u32*)(bkbi + 0x3C)) & 0x80000003) != 0
                  /* status ids 0 (KO), 1 (Stone), 31 (Vanished) */

refuse          = outOfPlay(unit) && FieldData_GetActiveFieldRecordBit15() == 0
```

Two of the three status masks are OR'd; the third (`+0x38`) is not consulted by this gate.

### The three status masks and the six operation modes

`0030E360` selects one mask and one direction from a six-entry jump table
(`00120000 + [00120000 + 0x1EE88C + mode*4]`), verified by reading the table itself:

| mode | operation | BKBI field | GFZ's typed name |
|---:|---|---|---|
| 0 | clear bit | `+0x64` | `dwStatusMaskMode0_3` |
| 1 | clear bit | `+0x3C` | `dwStatusMaskMode1_4` |
| 2 | clear bit | `+0x38` | `dwStatusMaskMode2_5` |
| 3 | set bit | `+0x64` — refuses if the bit is already set in `+0x64` **or** `+0x38` | |
| 4 | set bit | `+0x3C` | |
| 5 | set bit | `+0x38` | |

```c
bit = 1 << (statusId & 0x1F);          /* status id -> mask bit, 32 statuses per mask */
```

**How the name-to-offset pairing is established**, since it is the one claim here that could be
published backwards. The jump table at `0030E88C` is six image-relative dwords:

```
0030E88C  e7 e4 1e 00  fd e4 1e 00  13 e5 1e 00  26 e5 1e 00  43 e5 1e 00  57 e5 1e 00
          mode 0       mode 1       mode 2       mode 3       mode 4       mode 5
          0030E4E7     0030E4FD     0030E513     0030E526     0030E543     0030E557

0030E4E7  8b 4e 64 …  89 46 64      mode 0: read/write [rsi+0x64]
0030E4FD  8b 4e 3c …  89 46 3c      mode 1: read/write [rsi+0x3c]
0030E513  8b 4e 38 …  eb 3e         mode 2: read [rsi+0x38], jump to the shared store
0030E526  8b 4e 64  85 7e 38 …  89 46 64   mode 3: read [rsi+0x64], TEST [rsi+0x38], write [rsi+0x64]
0030E543  8b 4e 3c …  89 46 3c      mode 4: read/write [rsi+0x3c]
0030E557  8b 46 38 …                mode 5: read [rsi+0x38], falls through
0030E564  89 46 38                  the store modes 2 and 5 share
```

Three routes agree, and the first needs no decompiler at all:

1. **The names encode the mode pairs, and the bytes prove the partition.** The table pairs the
   modes as `{0,3} -> +0x64`, `{1,4} -> +0x3C`, `{2,5} -> +0x38`. That partition is not the
   obvious one — a reader guessing would pair `{0,1}`, `{2,3}`, `{4,5}` — so a name of the form
   `…Mode0_3` matching the `{0,3}` field is a real agreement, not a restatement.
2. **Mode 3's block is the only one with two different reads** (`8b 4e 64` then `85 7e 38`), and
   the decompiled `case 3:` is the only case with two reads, naming `dwStatusMaskMode0_3` for the
   one it writes and `dwStatusMaskMode2_5` for the one it only tests. That pins `+0x64` and
   `+0x38` by structural fingerprint, with no reliance on case ordering.
3. **Modes 2 and 5 share one store instruction** at `0030E564`; the decompiled cases 2 and 5 are
   the two that converge on it, and both name `dwStatusMaskMode2_5`.

`+0x3C = dwStatusMaskMode1_4` then follows by elimination. What this settles is *which offset each
GFZ name denotes*, not whether the names are good ones.

### The status definition table (`status_data.bin`, bound at `02EBF118`)

```
StatusDefTable
  +0x00  u32   magic 'st2e'
  +0x04  u32   count            32
  +0x08  u16   stride           40      <- read by every native consumer
  +0x0C  u32   recordsOffset    0x20    <- resolved to a runtime pointer

StatusDef                at records + id*40
  +0x00  u16   nameWord                 0x2800 + id: bank word>>11 = 5, entry word&0x7FF = id
  +0x02  u8    (separate byte)          copied alone to the status query's +0x24; meaning open
  +0x09  u8    defaultDurationUnits     0 = no timer
  +0x0C  u32   clearOnApplyMask         each set bit b -> ChangeStatus(b, mode 0)

defaultTimerFrames = record[+9] * DAT_01DFE0B4 * 30      /* 003876D0 */
```

> **Corrected 2026-09-26 (FABLE, Claude Opus 5.5).** This block first gave `+0x00` as `u8 id (0..31, self-indexing)`.
> That byte is the **low byte of a sixteen-bit name key**, which is why it looked like the id.
> - **The key.** The battle status query arm reads `word[record + 0]` twice. First it shifts right by 11 to pick
>   the text bank through `02EBF170`, then it masks with `0x7FF` to pick the entry. The resolved string pointer goes
>   to the query's `+0x18`.
> - **The separate byte.** The same arm reads **`byte[record + 2]`** on its own and stores it to the query's
>   `+0x24`. It uses the same row base, `resolve([02EBF118] + 0xC) + stride × row`.
> - The instruction addresses are in the package README below. This page names only the data addresses, because
>   the arm belongs to the battle status system, not to this table.
> - **Not a four-byte field.** The third byte varies: row 0 is `FF`, row 3 `1B`, row 6 `1A`, row 31 `FF`.
> - **The key values.** All 32 shipped keys are `0x2800 + row`, and bank 5's entries decode to the status names:
>   0 KO, 3 Stop, 6 Doom, 31 X-Zone.
>
> The evidence is ASTRA's [status-row-key-qualification](../../_experiments/evidence/status-row-key-qualification/README.md): offline, the original bytes plus the retained table, with 7 rejecting controls.
> I re-read the arm independently, and this correction rests on those instructions. The package's own
> review (`ASTRA-REVIEW-STATUS-ROW-KEY`, SWE2-AUDIT-SPEC) is still pending. The [thirty-two statuses page](../../10-Status-Periodic-Terminal/the-thirty-two-statuses.md) already gives the
> `u16` key.
>
> **Open:** what the `+2` byte indexes, and the sparse bytes' meaning and readers. The row
> alignment argued in §10 Attack 2 is unaffected, because the key's entry field *is* the row.

Shipped values that carry the C-9 argument:

| id | name | `+9` timer | `clearOnApplyMask` |
|---:|---|---:|---|
| 0 | KO | 0 | `0x7FFEF57C` — clears 2-6, 8, 10, 12-15, 17-30 |
| 1 | Stone | 0 | `0x1FFC0004` — clears **2 (Petrify)** and 18-28 (every buff) |
| 2 | Petrify | 45 | `0x00000000` |
| 6 | Doom | 100 | `0x00000000` |
| 8 | Poison | 120 | `0x00000000` |
| 10 | Sap | 1 | `0x02000000` — clears 25 (Regen) |
| 15 | Slow | 0 | `0x00100000` — clears 20 (Haste) |
| 20 | Haste | 0 | `0x00008000` — clears 15 (Slow) |
| 25 | Regen | 15 | `0x00000400` — clears 10 (Sap) |
| 31 | ~~Vanished~~ X-Zone *(corrected 2026-10-02, OPUS: status 31's name in bank 5)* | 0 | `0x7FFFFFFC` — clears **2 through 30**, i.e. everything except ids 0, 1 and itself |

### C-10 — every field that sets bit 15

**193 of 1,154 fields (16.72 %).** Names are from `planmapname.bin` read through the engine's own
`00377B60` indexing; a blank means that field has no name entry.

| Field ids | Count | Named fields in the run |
|---|---:|---|
| `0-22` | 23 | *(no name entries — the low system/boot slots)* |
| `48` | 1 | Stockade |
| `50-51` | 2 | rbn_z01, Oubliette |
| `124-130` | 7 | Observation Parlour, Sky Saloon, Air Deck, South Bank Village, North Bank Village |
| `233` | 1 | Outpost |
| `243` | 1 | Nomad Village |
| `289-310` | 22 | North End, Muthru Bazaar, East End, Southern Plaza, Amal's Weaponry, Panamis's Protectives, Migelo's Sundries, Yugri's Magicks, Batahn's Technicks, Yamoora's Gambits, Samalzalam Manor, The Clan Hall, The Sandsea, Eastgate, Southgate, Westgate |
| `312` | 1 | East Waterway Control |
| `488` | 1 | Hunters' Camp |
| `567-575` | 9 | Cellar Stores, Cellars, Lower Halls, Secret Passage, Treasure Room No. 8, The Garden Stairs |
| `631-643` | 13 | Jajim Bazaar, West Ward, Grand Arcade, Highgarden Terrace, Molberry, Trant, Charlotte's Magickery, Bulward's Technicks |
| `666` | 1 | Womb of the Sun-cryst |
| `701-708` | 8 | North Sprawl, South Sprawl, Dalan's House, Residence |
| `736`, `738-770` | 34 | Hall of the Light, Temple Grounds, Temple Approach, Sand-strewn Pass, Nilbasse, Rienna, Vint's Armaments, Granch's Requisites, Lebleu's Gambits, Banks of the Sogoht, Lull of the Land, The Elderknoll, Tsenoble, Alley of Muted Sighs, Alley of Low Whispers, Fane of the Path, The Spiritwood, Road of Verdant Praise, vic_a04 |
| `788-837` | 50 | Aerodrome ×5, Travica Way, Cloudborne Row, Miners' End, Lhusu Square, Khus Skygrounds, Kaff Terrace, Targe's Arms, Rithil's Protectives, Mait's Magicks, Clio's Technicks, Bashketi's Gambits, The Staras Residence, The Cloudborne, Sea Breeze Lane, Gallerina Marketplace, Quayside Court, Saccio Lane, Chivany Breakwater, Canal Lane, Beruny's Armaments, Odo's Technicks, Port Villa ×2, The Whitecap |
| `854`, `856`, `858`, `860`, `862`, `864`, `866-869`, `871` | 12 | dor_z01, Dalan's Marker, glf_z01, rbn_x01, byu_z01, byu_y01, alc_z01..alc_z04, Bridge |
| `910`, `912`, `914`, `916`, `918`, `922`, `924` | 7 | rbn_y01, byu_w01, byu_x01, Siti Bhrusuna, var_z01, bhm_y01, bhm_z01 |
| `1151` | 1 | Babbling Vale |

Every named entry is a town, a village, a shop interior, a plaza, an aerodrome, an airship
interior, or a story room the game does not fight in. The code-shaped names (`alc_z01`,
`byu_w01`, `rbn_x01`, `var_z01`, `bhm_z01`, `dor_z01`, `glf_z01`) are the engine's own map codes
for event/cutscene variants of those areas.

Two internal cross-checks on that set, both from the same file:

- **`thirdByte & 1` is set on exactly 170 fields, and every one of them also sets bit 15.** The 23
  fields that set bit 15 without it are precisely the unnamed system slots `0..22`. Two flags, one
  meaning, two different consumers.
- **bit 14 is set on 155 fields, 154 of them inside the bit-15 set.**

### C-11 — the rest of the record, as shipped

| Field | Distinct shipped values | Consumers | What is proven |
|---|---|---|---|
| bits 0-11 | 370 values; `0xFFF` on 556 fields, `0` on 200, otherwise 0..368 | UI (`003C5E50`, `003C17E0`, `003C60F0`, `003C8670`, `00576A50`), achievements (`003160C0`), `002550E0`/`002551B0`/`00255200` | a navigation-map entry id. `003160C0` uses it to index a per-bit "seen" bitmap at `DAT_022C2550 + 4 + (n>>3)`; shop interiors carry `0`, wilderness carries `0xFFF` |
| bits 12-13 | `0`:945 `1`:36 `2`:69 `3`:104 | `BattleAction_ComputeTargetPrimaryResourceGainFromHpDamage`, `…CasterPrimaryResourceGain…`, `BattleUnit_ResolvePeriodicPrimaryResourceRecoveryStep`, `AiOrder_EvaluateTargetSelector` — all through thunk `00320160` | a 2-bit per-field selector feeding primary-resource gain and AI target selection, **overridable by a persistent save flag**. **The MP meaning is settled 2026-09-07: values 2 and 3 — and only those — triple MP gain from damage in both formula functions (`lea ebx,[rbx+rbx*2]`) and divide the walk-recovery interval by `3.0` (`divss xmm6,[008F311C]`). For MP it is the one-bit test `>= 2`, true in 173 of these 1,154 fields.** ~~The `AiOrder_EvaluateTargetSelector` use is **not** examined, so **PROPOSED-repos2d-2 stays open**.~~ *(answered: examined 2026-09-12 — one selector predicate compares the raw value with its operand, `00303043`–`0030304D`; 2026-10-02, OPUS)* See [`../../10-Status-Periodic-Terminal/where-mp-comes-from.md`](../../10-Status-Periodic-Terminal/where-mp-comes-from.md) |
| bit 14 | 155 fields | 5 UI functions; `003F92B0` reads it and then calls the **area-name** reader `00377870` | gates area-name display for the field |
| bit 15 | 193 fields | 110 functions, 15 subsystems | the action-permission override |
| third byte bit 0 | 170 fields | 6 ActorEntity/Movement functions | the same safe-area flag, ANDed with save flag `payload[0x1062] & 1` |
| third byte bits 1-3 | values `0x02`,`0x04`,`0x08` combinations across 638 fields | **none** | authored and never read — **PROPOSED-repos2d-3** |
| third byte bits 4-6 | **`0` on all 1,154 fields** | `PartyFocus_SelectAndRequestDefaultActor`, `BattleGroup_RefreshFourActorDefinitions`, `0031C000` | a per-field **default focus combatant id**, consulted only when the runtime mode is 3 — the mode bit 15 itself produces. Shipped inert |

**The third byte now carries a store name: `packedOptions`** (OPUS 2026-09-16, completing
`FieldRecord` at 2 / 2). The name is for the *container*; the bit meanings and the shipped-value
census in the table above are FABLE's and are not restated. What justified naming it rather than
leaving it UNRESOLVED is that **every bit region is accounted for** — bit 0 the safe-area flag,
bits 1–3 authored and read by nothing (`PROPOSED-repos2d-3`), bits 4–6 the default focus
combatant id, bit 7 never set and never read. A byte with no unexplained region is a field with a
meaning, not a gap. Both accessors were re-read from the shipping bytes before the name was
installed: `00377700` defaults the byte to **0** on the table-missing path (`xor dl, dl`), so its
failure default is bit 0 *clear* — the permissive value, and the opposite of what `+0x00`'s
bit-15 accessor defaults to. Both index `base + id*3 + 0xA`, the same arithmetic as `+0x00`'s byte
loads at `+8` and `+9`, which remains the proof that this is a **separate field and not the u16's
high byte**.

The bits 4-6 finding is the sharpest modding hook in the record. `PartyFocus_SelectAndRequestDefaultActor`:

```c
mode = BattleRuntime_GetMode0To5FromFlagsAndFieldBit15();
if      (mode == 0 || mode == 1) id = *(u8*)(DAT_02EBF190 + 0x5AA4);   /* the saved leader */
else if (mode == 2)              id = 0x1A;
else if (mode == 3)              id = (fieldRecord.thirdByte >> 4) & 7;  /* 00377C70 */
unit = BattleUnit_FindByCombatantId(id);
if (unit == 0 || unit->pBkbi == 0) { /* fall back: scan four slots, then party slot 0 */ }
```

Mode 3 *is* the bit-15 mode (see the [mode ladder](../../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md)).
So the engine supports "in this town, focus on party member N by default", every shipped field
says `0`, and the fallback scan runs instead.

### C-11 — what the consumers make of bits 12–13 and the third byte's bit 0 (2026-09-12, FABLE-C11)

The encoding half of C-11 closed on the accessor contract; this is the meaning half, read from the
functions that consume the two values the earlier table left unnamed. Nothing here re-derives the
shapes; the shipped distribution above was re-counted from `navimapdata.bin` (1,154 records) and
matches the table exactly.

**Bits 12–13 are the field's primary-resource (MP) regime, and values 2 and 3 are the same regime.**
Through the thunk `00320160` → `00377BA0` (save-overridable: `+0x1063` bits 4–5 replace it when
`+0x1062` bit 7 is set), four consumers read it:

| consumer | what the value does |
|---|---|
| `BattleUnit_ResolvePeriodicPrimaryResourceRecoveryStep` (`002F9400`) | value 2 or 3 → the periodic recovery amount is **divided by 3.0** (`002F957E divss`, constant at `008F311C`) |
| `BattleAction_ComputeTargetPrimaryResourceGainFromHpDamage` (`002F91A0`) | value 2 or 3 → the resource gained from HP damage is **tripled** (`002F9234 lea ebx, [rbx+rbx*2]`) |
| `BattleAction_ComputeCasterPrimaryResourceGainFromHpDamage` (`002F9240`) | the same tripling for the caster (`002F93D6`) |
| `AiOrder_EvaluateTargetSelector` (`00301AD0`) | one selector predicate compares the raw value with its operand (`00303043`–`0030304D`, `setge`; the sibling arm `sete`) — a gambit condition can test the field's regime directly |

So the shipped values partition into two regimes the combat code can tell apart — 0/1 (945 + 36
fields, normal) and 2/3 (69 + 104 fields: walking restores a third as much, damage restores three
times as much) — and the 1-vs-0 and 3-vs-2 distinctions reach only the selector. Which named fields
carry 2 and 3 is a join this page already knows how to make (`planmapname.bin` through `00377B60`);
the regime's authored name is not in the binary.

**The third byte's bit 0 is a per-field flag that two functions fold into the global byte
`02099DE7`.** `00377700` returns 1 when the field's bit is *clear* and save flag `+0x1062` bit 0 is
clear (the inversion is the compiler's `not`/`test` on a "1 = special" bit); its six consumers are
actor-system functions, and two of them write the byte: `0026A1D0` (`0026A20B`, when its second
argument is negative) and `00268D10` (`00268E29`) both store `(00377700() == 0)` — i.e. *"the field
has the bit, or the save flag says so"* — into `02099DE7`, beside `02099DE5` / `02099DE6` which the
same family writes (`002628B0`, `00263050`, `00266D10`, `0026A1D0`) and reads (`00263480`,
`00263560`). ~~The triple is field-entry state the actor system consults; what it selects is not read
here (FZ-28).~~ **Read 2026-09-12 (FABLE), FZ-28:** the triple is the tail of **five party-hold
bytes `02099DE3`–`02099DE7`**, and it selects two things.

*The hold.* `00263560` ORs `DE3 | DE4 | DE5 | DE6` (`00263566`–`00263586`; `DE7` is not in the OR)
and, when the actor system is up (`02098E20` bit 0), visits the four-entry party roster `0209A1F0`
([the binding page](../../01-Script-VM-Native-Bridge/Interpreter-Core/how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md) §2.2) and for every registered record: sets the unit's flags-word **bit 36** when
any reason is set and clears it otherwise (`00312130`, `0x1000000000`), sets unit `+0x004` bit 5 to
the same (`00238B40`), writes the roster byte `+9` bit 7 to it, and zeroes the requested speed
(`Movement_SetRequestedSpeed(rec, 0.0, 2)`, `002635C0`–`0026360E`). So **any of the four bytes holds
the party**. Their writers name the reasons: `002628B0` (the area unload path under
`ActorResource_BeginManagerResourceSetLoad`) writes `DE3`, `DE4`, `DE5` with its argument and
`DE7 = 0xFF`; `00263050` (under `ActorResource_RemoveActiveEntry`) writes `DE5`; `0026A1D0` writes
`DE6` from its first argument; `00268D10` writes `DE5 = 1`; the bootstrap `00266D10` writes all of
`DE3`–`DE6` from one value with `DE7 = 0xFF` between the steps. `0xFF` in `DE7` is "not decided yet".

*The request.* `00263480(ctx, mode)` — called by `002628B0`, `00263050` and `00268D10`, the latter
two with `mode = (storage record byte +0xC >> 7) + 1` — then, when `DE5 | DE6` is non-zero, raises
one **system-mode request** through the 28-id registry `00226BE0` (a bit of `01FD46D4` per id, two
`0x18`-byte records per id at `01FD4160`, `00227680` filling them — interior verified
2026-09-17, SWE2-FRONTIER: sparse body, calls only `00182CD0` ([`002277E5`](../../_index/ADDRESS-INDEX.md))
and `002DDC30` (`002277FD`)): **id 5** for mode 0, **id 4** for
mode 1, **id 7** for mode 2 with the actor's handle (`ActorHandle_EncodeRegistryEntry(ctx)`) as the
request's parameter, and in every case `(DE7 == 0)` as the request's flag byte (`00263480`'s
`[rsp+0x28]`, stored at the id record's `+0x14` by `00227680`); when `DE5 | DE6` is zero it cancels
ids 5, 4 and 7 (`00225CD0(id, −1)`, `00263524`–`00263540`). `0026A1D0` does the same with id 5 only
and its own `DE7`. So **`DE7` — the field's third-byte bit 0 folded with the save flag — is the
parameter of the hold request, not a hold reason**; it reaches the mode registry as a 0/1 byte and
what the registry does with it is **read**: `00226BE0` is the start and `00226280` the apply
step of the system-stop registry, both bodies read whole on
[the time-stop registry](../../00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md) §3–§4
(*"unread" corrected 2026-09-12 (OPUS) — the residue note below had already been updated for the same page, and this sentence was left behind*). [The request router](../../16-UI/Request-Router/ui-request-router.md) §2 meets the
same pair for UI ids. **Residue (narrower):** the names of system-mode ids 4, 5 and 7 ~~and the
registry's own contract — no page documents `00226BE0`'s 28 ids — and the row for unit flag bit 36
on the unit field map~~ — *the registry's contract and bit 36 are documented 2026-09-12 on
[the time-stop registry](../../00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md):
ids 4 / 5 / 7 are this hold's stop requests, and bit 36 is a battle-side stop mark.* The "safe area" reading in the table above rests on the bit-15 name join, not on
these consumers, and is left as it was.

**Bits 1–3 stay authored-only**: 638 fields carry a combination of `0x02` / `0x04` / `0x08`, no
accessor reads them, and no function reads the third byte other than through `00377700` and
`00377C70` (the bit-15/bit-0 pages' sweep). `PROPOSED-repos2d-3` stands.

## 5. Call chain

```
area load / transition   <- corrected 2026-10-02, OPUS: boot, once - 00377CC0's one caller is 00266D10 (00267146), whose one caller is the boot routine
  -> 00377CC0  WorldAreaField_BootMapTables
     -> 00378540  request (1,32) planmapname.bin  -> 00378BB0 -> 02ADD0F8
                  request (9, 8) navimapdata.bin  -> 00378B80 -> 02ADD100     [OWNER]
                  request (9,39) gramap_weatherinfo.bin -> 00378F70 -> 02ADD0B0   <- corrected 2026-10-02, OPUS: four more requests follow - seven 0032E620 submissions in 00378540 (section 2a)

any gameplay decision about a unit
  -> (bkbi[+0x64] | bkbi[+0x3C]) & 0x80000003          "is this unit KO / Stone / Vanished?"
     -> 00377C20 (or thunk 00313F60)                    "does that matter in this field?"
        -> 003148F0 active-or-pending field id
        -> record -> bit 15
           -> 0 : refuse the action / skip the unit / withhold the reward
           -> 1 : proceed as though the unit were functional

  -> 0030D9A0 BattleRuntime_GetMode0To5FromFlagsAndFieldBit15
     -> bit 15 set -> mode 3, pre-empting mode 2
        -> 00326500 PartyFocus_SelectAndRequestDefaultActor
           -> 00377C70 third byte bits 4-6 -> default focused combatant
```

**Upstream:** `WorldTransition_GetActiveOrPendingFieldId`; the resource system
(`0032E620` → completion → `00378B80`); the shipped `navimapdata.bin`.

**Downstream (owner transitions in bold):** **Status/Periodic/Terminal** (`0030E360` refuses to
apply a terminal status to an already-terminal unit unless bit 15), **CombatFormula**
(`00300530` skips HP work on a terminal unit unless bit 15), CombatAction eligibility, CombatAI
targeting and enmity, Spawn eligibility and range retirement, Party control suppression,
Movement, Presentation, UI command lists, Items, Rewards.

**Do not confuse with:**

- **The mask without the waiver.** 55 of the 173 mask sites have no escape call at all.
  `PartyFollow_SolveFormation` is one: a KO'd character is dropped from the follow formation
  *everywhere*, town or not. `Reward_ComputeExperienceForRecipient` and
  `Reward_ComputeLicensePointsForRecipient` are two more — a KO'd character earns nothing anywhere.
  Bit 15 is not a blanket "ignore statuses" switch.
- **`00377480` vs `00377C20`.** Same bit, but `00377480` takes an explicit field id and
  `00377C20` uses the active-or-pending one. Substituting either for the other changes behaviour
  during a transition.
- **The two "safe area" flags.** `flags` bit 15 and `thirdByte` bit 0 agree on every named field
  but are read by different subsystems and one of them is additionally gated by a save flag.
  They are not interchangeable.
- **Petrify and Stone.** Status 2 is the countdown; status 1 is the terminal state. Only status 1
  is in the mask.
- **`navimapdata.bin` and `gramap_weatherinfo.bin`.** Sibling tables, adjacent resource indices,
  different headers — the weather table's count is a `u16` at `+6`, this one's is a `u32` at `+4`.

## 6. Modding notes

- **Best intervention point for "which areas are safe":** the third byte of the record in
  `navimapdata.bin`, plus `flags` bit 15. Set both — the engine reads them through different
  paths, and the shipped data never disagrees between them except on the 23 system slots.
- **The record is authored map data, not code.** Nothing recomputes it; the file is published
  once per boot into `02ADD100` and read directly thereafter.
- **It fails closed except at `00377700`.** An absent table or an out-of-range field id yields record `0x0FFF` /
  third byte `0`: no navigation map, and every flag clear ~~— the restrictive answer~~, which `00377700` reads inverted as the permissive 1 *(corrected 2026-10-02, OPUS: `00377728 xor dl, dl` / `0037772D not` / `0037773C mov eax, 1`; CONTRACT-field-record-accessors.md §10)*. Preserve that
  if you rebuild the file; the fail path is a literal constant, not a zero return.
- **Free real estate:** `thirdByte` bits 4-6 are read by the engine and set by nothing. Writing
  `n` there makes combatant `n` the default focus in that field whenever the runtime is in mode 3
  — which, in a bit-15 field, is exactly when the game is not in combat. This is untested in play:
  it is derived from the complete bodies of `00326500` and `00377C70`, not from a running game.
- **Do not repurpose `thirdByte` bits 1-3.** They are set across 638 fields and read by nothing in
  this executable; something outside the engine — a tool, an earlier build, or code reached by a
  route this document did not enumerate — may still care.
- **Growing the table:** every accessor bounds-checks against the `u32` at `+4`, so the count and
  the record array must grow together. `0032E400` supplies the request size from the shipped
  `FileSizeTable_*.fst`, so a resized file needs its size table entry updated too.
- **XIIOnline:** bit 15 is derived from area identity — **never network the bit**. Network the
  authoritative field id and let every client read its own table, exactly as the existing bit-15
  document says. Note the consequence for terminal statuses: two clients that disagree about the
  active field will disagree about whether a KO'd unit may act, which is a divergence in the
  *status transition* path (`0030E360`), not just in presentation.
- **Mod compatibility:** `navimapdata.bin`, `planmapname.bin`, `status_data.bin` and
  `listhelp_status.bin` are all replaceable authored data. Status ids 0, 1 and 31 are baked into
  the executable's constant `0x80000003`, so a mod may rename or re-describe those statuses but
  cannot move them to different ids without patching code.

## 7. What is not known

- [x] ~~The meaning of `flags` bits 12-13, the 2-bit field feeding primary-resource gain and AI
      target selection, and of the save override at `payload[0x1062] bit 7` / `payload[0x1063]
      bits 4-5`.~~ **C-11 ANSWERED to the image's limit (2026-09-12, FABLE):** the MP regime —
      values 2 / 3 third the periodic recovery and triple the gain from HP damage, 0 / 1 are normal,
      and the selector consumer is now read (one predicate compares the raw value, so a gambit
      condition can tell 1 from 0 and 3 from 2); the save override substitutes `+0x1063` bits 4–5
      when `+0x1062` bit 7 is set. The authored *name* of the regime is not in the binary — §"C-11 —
      what the consumers make of bits 12–13". **PROPOSED-repos2d-2.**
      **Half answered 2026-09-07:** for the MP economy the field is the test `>= 2` — values 2 and 3
      triple gain from damage and third the walk-recovery interval, values 0 and 1 do nothing.
      ~~**The `AiOrder_EvaluateTargetSelector` consumer is still unread, so this box stays unticked.**~~ *(answered: read 2026-09-12, `00303043`–`0030304D`, as C-11's box records; 2026-10-02, OPUS)*
      [`../../10-Status-Periodic-Terminal/where-mp-comes-from.md`](../../10-Status-Periodic-Terminal/where-mp-comes-from.md)
- [x] ~~Why `thirdByte` bits 1-3 are authored across 638 fields and read by nothing.~~ **Closed
      2026-09-12 (FABLE, C-11): not in the image** — no reader by any accessor or hop, so the *why* is
      authoring history; a reconstruction preserves the bits as data. **PROPOSED-repos2d-3.**
- [x] **UQ-83.** Why the resource publishers store a 32-bit-truncated pointer that every reader then
      dereferences as a 64-bit pointer. **PROPOSED-repos2d-4.**
      ***ANSWERED 2026-09-18 (FABLE): the truncation is the engine's own image-address convention, whose base is zero, so a 32-bit image address *is* the low half of an absolute pointer and zero-extending it *is* the resolve.** *The convention.* `RuntimePointer_EncodeImageAddress` `0020E620` is `sub ecx, [01F83530]; mov eax, ecx` and `ImageAddress_ResolveRuntimePointer` `0020E600` is `mov eax, ecx; add rax, [01F83530]`; the base `01F83530` is zero-initialised `.data` ~~that no instruction in the image writes~~ that no instruction NAMES (every rip-relative site targeting `01F83500`..`01F83538` is those two reads and two unrelated loads in `008A7360`; no base-plus-displacement form exists) *(Scope corrected 2026-09-25, FABLE, Claude Opus 5.5: `01F83530` is **zero at image load**, because it lies past `.data`'s file-backed extent. That is separate from whether later code can write it, and one in-image store route can. The texture-id table writer `00210570`, reached through GiSetTexture's execute, bounds its id only from above with a signed compare, so id `0xFFFB` stores a pointer into `01F83530`. That was replayed on the unmodified bytes. The id producers read keep ids below `0x4000` at the shipped frame width, so the route is **undriven, not absent**. "Zero for the process's life" is supported, not proven. See [the row-lookup contract](../../02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md) §7, the reconciliation.)*, so encode is truncation to 32 bits and resolve is zero-extension, engine-wide. *Where the truncation happens here.* The registration `00378540` allocates the destination block (`0036A190` → `0036A1A0`, heap id `[022D89BC]`, tagged by `0036C660`), stores its low half into the request record's user word (`mov dword ptr [rbp-0x28], ebx`, `003787D3`) and passes the same pointer whole as `r8` (`003787DE`) to `0032E620`; the resource system copies the user word into its slot (`mov [r10+0x60], r11d`, `0032E961`) and delivers it to every completion in `ecx` (`mov ecx, [rcx+0x60]; call rax`, `0032E30C`, `0032E34F`, `0032E392`, `0032E189`); the ten-byte publisher `mov eax, ecx; mov [rip+g], rax` is then the resolve with base zero. The allocator itself stamps each block's header with an encoded address (`0036A209`..`0036A20E`, `[block-0x10]`), so the arena is addressed in this 32-bit space by design. *Why it works.* It requires every such pointer below 4 GiB, and nothing in the image checks that: the arena is CRT heap (imports `malloc` ×37, `_aligned_malloc` ×3, `calloc` ×1; no `VirtualAlloc`, `HeapAlloc` or `MapViewOfFile` import), and the image opts out of ASLR (DllCharacteristics `0x8120`: `HIGH_ENTROPY_VA` and `NX_COMPAT` set, `DYNAMIC_BASE` clear; base `0x120000`, image end `0x3096000`), so the process runs without address randomisation and its heap grows bottom-up from the low address space, which is what the PS2-era 32-bit convention relies on (a reading of the documented loader behaviour, tier 6). Static; the encode, resolve, allocator, registration, slot copy and completion calls read in full.*
- [x] **UQ-84.** Which authored action, script or item applies status **31 (Vanished)** — no native call site
      passes it as a constant. **PROPOSED-repos2d-5.**
      **ANSWERED 2026-09-15 (FABLE): one enemy technick, *Telega*, and nothing else.** This is an authored-data census
      of every carrier the status paths read, with the readers cited (`work/FABLE/drift4/uq84_census.py`); nothing
      was executed. Status 31 is *X-Zone* in the name bank ([the thirty-two statuses](../../10-Status-Periodic-Terminal/the-thirty-two-statuses.md)).
      - **Actions.** Of the 543 action rows, exactly one has bit 31 in its status mask `+0x18`: **row 462, Telega**
        (mask `0x80000000`, hit threshold 85, [the action definition row](../../07-Combat-Action/Action-Definition-Row/the-action-definition-row.md)).
        - Its recipe 72 commits slots `[21, 40, 181]`. Slot 181 is `BattleFormula_CalcApplyCandidateStatusesRequired`.
        - Stone Gaze, Doom and Bad Breath share the recipe. The trap rows 250–258 are the control: their masks match
          the statuses that page lists.
      - **Who uses it.** Exactly 2 of the 50,050 authored order records select action `0x1CE`: set 0 record 17 and
        set 2 record 18 of `rwg_b.ard`. No weighted table lists it.
        - Those are the default order sets (`+0x50`) of that area's two unit rows, and both rows are named *Demon Wall*.
        - No decompiled `us` script uses `0x1CE` (or 462) as an action id; the literal occurs only as a shape
          coordinate and a motion frame.
      - **Weapons and ammunition** do not carry it. The `u32` at equipment row `+0x20`, beside the on-hit chance byte
        `+0x1F`, holds each chance-bearing weapon's single status (Mage Masher `0x200` Silence at 15, Blood Sword
        `0x400` Sap at 100). Bit 31 is set on none of the 557 rows. The word's reader is not traced here.
      - **Permanent-status words** never carry it. The stat rebuild `002FEF30` ORs these into `+0x3C`:
        - the party rows' `+0x48`: bit 31 on 0 of 40;
        - the equipment attribute blocks' `+0x08`: 0 of 176. The blocks are the 24-byte heap after the record array.
          The header's `+0x14` is 0 in this copy; its `+0x18` holds `0x7144`, the base `00238160` adds to every
          handle (corrected 2026-09-15, AY-11). The alignment was also checked independently: of the candidate 4-byte
          alignments, exactly one leaves the three bytes the rebuild never reads (`+0x15`–`+0x17`) zero in every
          block, and it gives Ribbon the immunity word `0x0001EFFC`.
      - **Scripts** never apply it. `btlAtelSetStatus` codes 1 and 2 (applied once at spawn) occur for status 31 in
        none of the 6,746 calls in the `us` corpus.
      - **What the other carriers do with status 31 is make a unit immune to it:**
        - the thirteen Esper party rows 27–39 set it in their immunity word `+0x4C` (`0x8801FFFE`);
        - 6,205 of the 6,746 `btlAtelSetStatus` tables give it code 3, the other 541 tables are empty. Code 3 reaches
          the immunity word `+0x38`, not the status words ([the auto-status rebuild](../../08-Combat-Formula/the-auto-status-rebuild.md),
          corrected the same day).
      **Bound:** `us` data only; a unit made to act through a path other than its order records was not censused.
- [x] ~~The `DAT_01E0C2B4` / `DAT_020927E0` consumer noted in the bit-15 document — still open
      (**C-12**), untouched by this work.~~ **Answered on [the R2 force-fight toggle page](../../15-Input/Modal-Toggles/r2-force-fight-toggle.md) (ledger reconciled
      2026-09-12, FABLE):** the consumer is `InputGameplay_ArbitrateDigitalInputAndModalState`
      (`00253C70`), sole owner of the three globals; `020927E0` is the **R2 force-fight toggle**, its
      latch `01E0C2B4`, and bit 15 of the field record pins the toggle off on release when snapshot
      bit 9 is clear (`00254232`–`0025423B`), the value then applied by
      `ForceFightToggle_ApplyWithCapabilityGates` (`00252B60`). That page keeps the toggle's own
      residue (the sound index, the two refusal predicates, `020927CC`).
- [x] ~~**UQ-85.** Designer name for bit 15 itself. The behaviour is proven; the label is not recovered.~~
  **NO ADMISSIBLE SOURCE** (2026-09-14, FABLE; EVIDENCE-STANDARD addendum 2026-09-15bk): ~~no admitted artefact carries the label.~~
  *no artefact in the searched population carries it (below).*
  *Signed 2026-09-17 by OPUS (reviewer; FABLE, author), recorded 2026-09-27 (FABLE, Claude Opus 5.5), and relabelled OUT OF EVIDENCE BOUNDARY under FRONTIER's carrier test (27f): the bit is tested in code, so its name is an identifier the unshipped source / `FF12X64.pdb` would carry. The negative covers a named population: the three shipped `navimapdata.bin` copies (no printable run at all), the bit-15 predicate's 112-body direct-caller closure (no string operand), an image-wide vocabulary scan and SWE2-DATA's label tables. The unknown name itself is not searchable by construction. [Record](../../_index/candidates/uq82-uq85-signature/README.md).*

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The record layout and all seven extractions | complete exact-current bodies of `00377C20` (78 B), `00377480`, `003779F0`, `00377A40`, `00377BA0`, `00377700`, `00377C70`, disassembled from the authorized EXE | 1 |
| The fail-closed default record is `0x0FFF` | literal `mov edx, 0xfff` / `shr edx, 0xf` on the guard path of `00377C20` and `00377480` | 1 |
| Three status masks, six operation modes, and their offsets | six-entry jump table read at `00120000 + 0x1EE88C` = `0030E88C`; each target block disassembled from the authorized EXE | 1 |
| `dwStatusMaskMode0_3` = `+0x64`, `Mode1_4` = `+0x3C`, `Mode2_5` = `+0x38` | three independent routes: the `{0,3}/{1,4}/{2,5}` mode partition the names encode and the jump table proves; mode 3's unique two-read block; the store modes 2 and 5 share at `0030E564` | 1 |
| `statusId -> bit` is `1 << (id & 0x1F)` | complete body of `0030E360` | 1 |
| Status 0 is applied when HP reaches zero | `BattleStats_ModifyHPAndProcessLethalState` passes the constant `0` in `r8` at two call sites (`xor r8d, r8d`, both hand-verified in the disassembly) | 1 |
| The constant-status-id census, corrected | backward register-liveness over **all 17 call sites** of `0030E360` and its two wrappers: **6 CONST, 9 DYNAMIC, 2 UNKNOWN**. Every CONST hand-verified against the encoding. Ids: `0` ×2, `4`, `5`, `24`, `31` — table below | 1 |
| No native site **adds** status 1 or 31 by constant | the single native constant use of `31` is a **removal** (`BattleStats_RemoveStatusMode0` from `BattleSystem_InitializeAreaState`); status 1 has no native constant site at all | 1 |
| The authored direct-command family maps to status ids arithmetically | `BattleUnit_ExecuteDirectStateCommandOrder` computes the id as `lea r8d, [rdx - 0x51]` for the add path and `lea r8d, [rdx - 0x71]` for the remove path | 1 |
| Statuses 0, 1, 31 share the defeat/reward path and one recovery gate | the terminal `switch` in `0030E360`; `00312280`; `00301140` | 1 |
| Status 1 emits `0x200C`, status 31 emits `0x200E` | same switch, via `003299B0` | 1 |
| The three are named KO, Stone and Vanished | `listhelp_status.bin`, 32 entries in id order, decoded with a charset derived in-file (see below) | 9 |
| …and the naming is right | four independent cross-checks against the binary and against `status_data.bin` — see the falsification pass in §10 | 1 |
| The table is `navimapdata.bin` | registration `(kind 9, index 8)` in `00378540`; the executable's own path array places `navimapdata.bin` and `gramap_weatherinfo.bin` exactly 31 slots apart, matching indices 8 and 39; the file's magic is `NAV\x02`; `8 + 3 * 1154 == 3470` is the exact file size | 1 + 2 |
| 193 fields set bit 15, and they are towns/safe areas | the shipped file parsed with the reader's own arithmetic, joined to `planmapname.bin` through `00377B60`'s own `+0x10` indexing | 1 + 9 |
| `thirdByte` bit 0 ⊂ bit 15, exactly | cross-tabulation over all 1,154 records: 170 / 170 / 0 | 1 |
| 117 of 173 mask sites pair with the field-record escape | full linear disassembly of all 38,161 function bodies; stable at ±8 and ±25 instruction windows | 1 |
| `00377BA0` is reached only through thunk `00320160` | direct-call census (`edges.tsv`), thunk census, rip-relative `lea` sweep, 8-byte data-pointer scan, and a `call`/`jmp rel32` instruction census with a positive control (80 sites to `00377C20`) | 1 |
| Bits 4-6 of the third byte are the mode-3 default focus id | complete bodies of `00377C70` and `00326500` | 1 |
| The FFXII text charset used to read the authored strings | derived in-file: `'A'=0x20`, `'a'=0x3A`, space `0x04`, digits `0x85`-`0x8E`. Proven by the Doom help string reading *"will be KO'd when the count reaches 0"* and by map codes decoding as `rbn_z01`, `alc_z01` | 2 |

**Superseded readings.**

**Corrected 2026-09-03 — my own instrument was wrong, and it produced confident wrong values.**
This document originally reported the constant-status-id census as *"4 CONST (all 0) and 13
UNKNOWN — no other constant status id is passed anywhere in the executable."* Two of those four
CONST verdicts were false. The census tool determined which registers an instruction writes from
capstone's `regs_access()`, and capstone reports

```
lea edx, [rdi + 0x15]      ->  written = ['rdi'],  read = ['edx']
```

with **destination and base inverted**. A backward walk therefore stepped straight *past* every
`lea` write and reported whatever earlier instruction it found. At the two
`BattleUnit_ExecuteDirectStateCommandOrder` sites the real arguments are
`lea r8d, [rdx - 0x51]` and `lea r8d, [rdx - 0x71]`; the walk skipped them and found an earlier
`xor r8d, r8d`, reporting **CONST 0**.

The tool now derives `lea` destinations from the operands and never from `regs_access()`, and every
constant below was re-verified by reading the encoding by hand:

| Site | Encoding | Id | Caller |
|---|---|---:|---|
| `0030077A` | `xor r8d, r8d` | 0 | `BattleStats_ModifyHPAndProcessLethalState` |
| `003007CF` | `xor r8d, r8d` | 0 | same |
| `0030EB8D` | `mov r8b, 4` | 4 | `BattleSpecialSequence_CommitAccumulatedTargetHp` |
| `0030EBB7` | `mov r8b, 5` | 5 | same |
| `00304A76` | `mov r8b, 0x18` | 24 | `BattleUnit_AdvanceStandardActionState` |
| `0023437E` | `mov r8b, 0x1F` | 31 | `BattleSystem_InitializeAreaState`, through the **remove** wrapper |

**The correction strengthens §2d rather than weakening it.** Four of the six ids now have a native
behavioural check against the help text used to name them, and all four agree:

- **4 = Sleep** and **5 = Confuse**, both cleared where a special sequence commits accumulated
  damage — damage waking a sleeping or confused unit.
- **24 = Invisible**, touched as a standard action advances — acting breaking invisibility.
- **31 = Vanished**, *removed* when an area initialises — clearing an irreversible removal state
  at area load, which is the only sane time to clear it.

None of those four was sought; each fell out of a corrected census. The naming in §2d was derived
before any of them was known.

**What did not survive:** the sentence "status 0 is the only status id any native call site passes
as a constant." **What did:** no native site *adds* 1 or 31 by constant, which is the claim §2d
actually rests on.

Two further refinements are recorded:

- *Old:* the terminal test is over "two status layers". *New:* there are **three** 32-bit status
  masks (`+0x38`, `+0x3C`, `+0x64`); the gate ORs two of them and ignores `+0x38`. The GFZ's typed
  names map as `dwStatusMaskMode0_3` = `+0x64`, `dwStatusMaskMode1_4` = `+0x3C`,
  `dwStatusMaskMode2_5` = `+0x38` — several documents in other categories print the first two the
  other way round. Flagged to the coordinator; not edited here.
- *Old:* the record's third byte is "not read here, something else reads it". *New:* two accessors
  read it, they read only bit 0 and bits 4-6, and the shipped data and the code disagree about
  which of those bits are live.

## 9. Related

- [`field-record-bit15-action-permission.md`](field-record-bit15-action-permission.md) — the bit 15 gate itself; this document closes its C-9, C-10 and C-11
- [`../Weather/mweather-resource-format.md`](../Weather/mweather-resource-format.md) — the sibling table, adjacent resource index, same registration routine
- [`../../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md`](../../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md) — bit 15 → mode 3, which is what gates the default-focus field
- [`../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md`](../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md) — the 128-bit effect layers, a **different** structure from the three 32-bit status masks
- [`../../11-Party/party-roster-and-control-suppression.md`](../../11-Party/party-roster-and-control-suppression.md) — a consumer of the same predicate
- [`../../13-Rewards-Progression-Economy/experience-and-license-point-award.md`](../../13-Rewards-Progression-Economy/experience-and-license-point-award.md) — the mask **without** the waiver
- [`../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md`](../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md) — spawn eligibility and range retirement
- [`../../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md`](../../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md) — enmity refuses to write threat through the same predicate

## 10. Falsification pass 2026-09-02

Run against snapshot `46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2`,
parent `2ed8affb…`, embedded EXE `73461d08…`, all reproduced by `Verify-GfzCheckpoint.ps1`
before any reading was done.

### Attack 1 — "the file is not the table"

*Killer observation:* a file that merely looks plausible would not satisfy the reader's own
arithmetic, and the registration index would not line up.

Four checks, three of which could have failed independently:

1. `8 + 3 * (u32 at +4) == 3470` — the exact byte length of `navimapdata.bin`. A wrong file passes
   this with probability ~2⁻³².
2. The file's first four bytes are `NAV\x02`.
3. The registration requests `(9, 8)` for `"MapInfo"` and `(9, 39)` for `"MWeather"` — **31 apart**
   — and the executable's path array holds `navimapdata.bin` and `gramap_weatherinfo.bin` exactly
   31 slots apart. This is the check that could have refuted the identification and did not.
4. **The sibling parses too.** `gramap_weatherinfo.bin` satisfies the *MWeather* reader documented
   elsewhere in this database (`count = u16 at +6` = 776; 776 × 3 slots × 9 bits = 2,619 bytes,
   + 8 header = 2,627 ≤ 2,628 actual). A wrong (kind, index) → path model would have to be wrong
   for both files in the same direction.

*Not broken.*

### Attack 2 — "the status help list is off by one"

This one **did** find an error, in my own first reading, and is the reason the naming is not
carried on the text file alone.

`listhelp_status.bin`'s block is `[count = 32][32 string offsets]`, not 33 offsets; reading it as
33 shifts every name by one id. The shift was caught by four checks that must all agree:

| check | expects | shipped data |
|---|---|---|
| `status_data.bin` timer `+9` non-zero exactly where the help text mentions a count | ids 2 and 6 | 2 → 45, 6 → 100 ✓ |
| Sap's text says *"Remove by casting Regen"* | id(Sap).clearMask has bit id(Regen), and vice versa | 10 ↔ 25, both ways ✓ |
| Slow's text says *"Remove by casting Haste"* | 15 ↔ 20, both ways | ✓ |
| Stone's text describes the finished state of Petrify's countdown | id(Stone).clearMask has bit id(Petrify) | `0x1FFC0004` bit 2 ✓ |

Under the off-by-one reading **every one of those four fails**. Under the corrected reading all
four hold, *and* the alignment agrees with the external status enum this database already cites at
tier 6 for three independent ids (Petrify = bit 2, Disease = bit 16, Lure = bit 17). The native
behaviour agrees too: HP → 0 applies status 0, whose text is *"has lost consciousness"*.

*Broken, corrected, and the corrected reading survives.*

### Attack 3 — "the field-name table indexes a different id space"

*Killer observation:* if `planmapname.bin` were indexed differently from `navimapdata.bin`, joining
them would produce plausible-looking but wrong area names — the worst possible failure for §4's
table.

Test: cross-tabulate "has a name entry" against "has a navigation-map id" over the 1,154 ids both
files cover, with the null stated in advance (independence → agreement ≈ 0.502).

- Indexing the name table from the offset where its data *appears to start*: agreement **0.510**
  vs null 0.503 — indistinguishable from chance, i.e. **the join was wrong**.
- Indexing it as the engine's own reader `00377B60` does — `u16` at `table + 0x10 + 2*id` —
  agreement **0.951**.

The first reading was mine and it was wrong by 48 ids. It is recorded here because it is exactly
the failure the joined table would have hidden: names that read beautifully and belong to other
areas.

*Broken, corrected, and the corrected join is what §4 publishes.*

### Attack 4 — "the pairing statistic is a window artefact"

The claim "117 of 173 mask sites pair with the escape call" depends on a proximity window. Re-run
at ±8 instructions: 116 PAIRED, 55 NO-ESCAPE. At ±25: 117 / 55. *(corrected 2026-10-02, OPUS: the two figures are not a partition of 173. The 55 are the sites in the 42 functions that never call `00377C20` or its thunk `00313F60`; the other 118 lie in functions that do, and the third class — the call present but outside the window — holds 2 at ±8 and 1 at ±25, both in `0030E360` (`0030E454`, 28 instructions from the nearest call, and `0030E48A`, 12). So 116 + 2 + 55 = 117 + 1 + 55 = 173, re-derived over `retool.py grep 0x80000003`: 173 sites in 131 functions.)* The statistic does not move with
the window, and the 55 no-escape sites are a real population — `PartyFollow_SolveFormation` and
both reward functions are among them, which is why §5 warns against reading bit 15 as a blanket
waiver.

*Not broken.*

### Attack 5 — "the zero-caller accessor is dead code"

`00377BA0` has **zero** direct callers in the call graph. Before publishing "dead", every route
this database knows was enumerated: direct call edges, jump thunks, rip-relative `lea`,
8-byte data pointers in `.rdata`/`.data`, and a `call`/`jmp rel32` instruction census with a
positive control (80 instructions target `00377C20`). The last route found it: a **tail-call
thunk** at `00320160`, itself called by four functions in three subsystems.

*Broken. "Dead code" was withdrawn before it was written down.*

### What was not attacked

- No runtime observation was taken. Every claim here is static plus authored data; the
  bits 4-6 modding advice in §6 is explicitly marked untested in play.
- The area-id space behind `00377870` / `MapRef_GetPersistenceGroupId` was not derived, so the
  59 area names in `planmapname.bin` are not joined to fields in this document.
- ~~`audit_crossrefs.py` has not yet been run against this document — `crossref_clean: false`.~~ *(answered: run since — the front matter says `crossref_clean: true`; 2026-10-02, OPUS)*

## 11. Cross-subsystem neighbours — disposition

`audit_crossrefs.py`, run against the current graph (`Tools/work/graph_gn`, 38,161 functions /
90,525 edges), reported **6 UNACCOUNTED NEIGHBOUR** findings for this document. Each is
dispositioned below. One of them turned out to be a finding rather than a neighbour.

### Explained — real relationships this document had not named

**`Input` — `InputGameplay_ArbitrateDigitalInputAndModalState` (`00253C70`, 1,599 B) reaches the
predicate twice, by both routes**: directly at `00254067` and through thunk `00313F60` at
`00254232`. It is one of only two functions in the image that call it both ways. This is not a
stray edge — it is **open question C-12 from the
[bit 15 document](field-record-bit15-action-permission.md)**, which described "one structurally
different consumer around `DAT_01E0C2B4` / `DAT_020927E0`, paired with a `DAT_02F97360 & 0x200`
test — a separate subsystem, not the combat gate. Not yet explained." It is explained below.

**`InputGameplay` — `00313A00` (289 B)** calls the predicate at `00313A34`, immediately after
`00253B90`, and keeps the answer in a register alongside an unrelated flag. A second Input-side
consumer, same subsystem family as the above.

**`PlatformOnlineAchievements`** — this document already discusses `003160C0` as the consumer that
tests the navigation-map id against a per-bit "seen" bitmap; the finding is that the *owner name*
was never written. Its own caller is `00315E90`, same owner. Separately,
`BattleUnit_ProcessDefeatRewardsAndLoot` (`00312280`) calls `00316A50`, also
`PlatformOnlineAchievements` — so the defeat path the three terminal statuses share reaches
achievement bookkeeping. **What `00316A50` counts is not established here**; the claim is the edge
only (tier 11), and it is recorded rather than characterised.

### C-12, substantially closed

The three globals are **private to one function.** A full-body sweep of all 38,161 functions for
rip-relative references finds `DAT_01E0C2B4` at 4 sites, `DAT_020927E0` at 5 and `DAT_020927E4` at
2 — **every one of them inside `00253C70`**. Positive control: the same sweep found all 6 sites of
`DAT_02F97360`, which really is shared (two other Input functions touch it). So C-12's "separate
subsystem" is not a subsystem at all: it is one input-arbitration function's own modal state.

```c
/* tail of InputGameplay_ArbitrateDigitalInputAndModalState */
if (FUN_0017DE10() == 0) {
    if ((DAT_02F97360 & 0x200) == 0) {                 /* input-snapshot bit 9 not set */
        if (DAT_01E0C2B4 == 1 || FieldData_GetActiveFieldRecordBit15() != 0)
            DAT_020927E0 = 0;                          /* <- the field record forces it OFF */
    } else if (FUN_00862CF0() != 1) {
        DAT_020927E0 = 1;  DAT_01E0C2B4 = 1;  goto emit;
    }
    if (DAT_01E0C2B4 != 0) goto emit;
} else {
    DAT_01E0C2B4 = 0;
    if ((~DAT_020927E4 & 1) != 0)
        DAT_020927E0 = (DAT_020927E0 == 0);            /* toggle, once per edge */
    DAT_020927E4 = 1;
}
emit:
FUN_00252B60(DAT_020927E0, 0);
```

So `DAT_020927E0` is a **two-state gameplay toggle**, flipped once per input edge with
`DAT_020927E4` as the edge latch and `DAT_01E0C2B4` as a sticky override; `DAT_02F97360` is the
input frame snapshot. **A bit-15 field forces the toggle off.** The value is handed to
`FUN_00252B60`, which routes it through the gameplay capability mask (`FUN_002E0FA0`) and
`FUN_0035C880(0xC, …)`.

~~**What the toggle is remains unnamed** — that is 15-Input's to close~~ *(answered: `020927E0` is the R2 force-fight toggle, this page's 2026-09-12 note; 2026-10-02, OPUS)*, and this session does not
write in that category. But C-12's question — *what is this structurally different consumer?* — is
answered: **a per-press input toggle that towns force off**, held in one function's private state,
not a parallel status gate.

### Dispositioned as hub neighbourhood, not relationships of this system

Citing a hub imports its whole caller census. Three of the addresses in §3 are hubs:

- **`003148F0` `WorldTransition_GetActiveOrPendingFieldId` — 49 callers across 11 subsystems**,
  enumerated in
  [`../../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md`](../../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md)
  §2 (hub 2), where all 11 subsystem rows are verified row by row. The `Audio`
  (`00261F90`) and script VM / native bridge (`00357450`, `0033F310`) edges flagged against this
  document are that hub's neighbours, asking the engine for the current field id. They are not
  field-record relationships. *Disposition by reference — valid because that document contains the
  census.*
- **`0032E620` `Resource_SubmitRequest` — 38 callers over 7 owners**: `(none)` 21, `Resource` 9,
  `WorldAreaField` 3, `ActorEntity` 2, `Save_Load_Settings` 1, `Presentation` 1,
  script VM / native bridge 1. No hub document enumerates it, so the census is stated here rather
  than deferred. This document cites it only for the three `WorldAreaField` requests in §2a; the
  `Input` edge (`00291C80`) and the script-VM edge are other subsystems loading their own
  resources.
- **`00264F90` `MapRef_GetPersistenceGroupId` — 19 callers over 5 owners**: `(none)` 13,
  `WorldAreaField` 2, script VM / native bridge 2, `UI` 1, `Save_Load_Settings` 1. The nineteen include
  `WorldTransition_StageFieldTransition` (`003145E0`, call at `003146BC`) and `SaveImage_FinalizeHeaderAndChecksum` (`00583D60`, call at `00583F3F`) — the
  `Save_Load_Settings` caller, which carries the id into the save header (named 2026-09-14 for the citation on
  [script variables](../../01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md)). Cited here only
  as the area-id source for `003778B0`. The script VM / native bridge callers (`0050CDE0`,
  `00357450`) are ScriptVM verbs asking the engine for the current area id — authored-intent
  consumers of the id, not of the field record.

One further edge, `0026A1D0 callee 00226BE0`: this document cites `0026A1D0` only as one of the six
Movement/ActorEntity consumers of the third-byte bit-0 accessor. Its own callees belong to
Movement's frame work, not to the field record. *Irrelevant to this system, with the reason
stated.*

**Audit state.** `audit_crossrefs.py` run against `Tools/work/graph_gn` (38,161 functions,
90,525 edges, regenerated for the certified GN158 parent) reported **6** findings for this
document's folder on the first pass and **0** after the dispositions above. Both documents in the
folder are now `crossref_clean: true` **against that graph state** — a claim about one program
state, not a permanent property. `check_links.py` and `verify_doc_addresses.py` both pass; the
latter reports `0030E88B`/`0030E88C` as `.text` non-function citations to confirm, which is
correct: they are the last byte of `0030E360`'s body and the jump table immediately after it, both
declared as data above.

## The `00315E90` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`00315E90` (520 B) — the navimapdata command interpreter: `002536A0`
(`00315EB5`), `003165C0`/`00316760` (`00315F1D`/`00315F34`),
`00309EC0` (`00315F66`), a second `003165C0` + `003166F0` arm
(`00315F90`/`00315FA5`), and the two member arms `003160C0`
(`00315FDC`) and `003161A0` (`00315FEB`) — every arm converges on the
`00316045` tail.

| member | role | interior |
| --- | --- | --- |
| `003160C0` (212 B) | command arm on the `[022C2550]` object — null-gate (`003160CD`), `00264790` (`003160EA`), `003148F0` (`003160F3`) | [`003160F3`](../../_index/ADDRESS-INDEX.md) |
| `003161A0` (308 B) | command arm on the same `[022C2550]` object — null-gates on `rcx`/`rdx` (`003161AD`/`003161BA`), `esi = eax` result (`003161C8`) | [`003161C8`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `002536A0`, `003165C0`, `00316760`,
`00309EC0`, `003166F0`, `00264790`, `003148F0`. The `022C2550` cell is
the shared navimapdata context object.

## The `00261F90` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00261F90` (~330 B) — gated field-record op: `dword[+0x28]` nonzero or
`byte[+0x10] & 0x40` set → early out (`00261F96`/`00261FA3`).

| member | role | interior |
| --- | --- | --- |
| `00360D30` (25 B) | `022CBA60` one-shot — nonzero → clear + tail `002DE050`; zero → ret (`00360D30`/`00360D43`) | [`00360D30`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `002DE050`.

## The `00326500` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00326500` (`PartyFocus_SelectAndRequestDefaultActor`~~, ~119 B~~, 274 B *(corrected 2026-10-02, OPUS: its last instruction is the short `jmp` at `00326610`, so `0x112` bytes)*) —
`bl = 0xFF` then `00311E20()` + `00326620()` (`0032650A`/`00326511`).

| member | role | interior |
| --- | --- | --- |
| `00317400` | `003137E0(rcx)` then `movzx ecx, al` — bool forward (`0031740D`/`00317412`) | [`0031740D`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00311E20`, `00326620`, `003137E0`.

## The `00378540` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00378540` ~~(~85 B)~~ (943 B *(corrected 2026-10-02, OPUS: its last instruction is the `ret` at `003788EE`, so `0x3AF` bytes, as §2a says)*) — `rbp = rsp` frame (`00378550`/`00378553`).

| member | role | interior |
| --- | --- | --- |
| `00267990` | `0036C1D0(5)` assert-path twin of `00267930` (`0026799A`/`002679A1`) | [`0026799A`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0036C1D0`.

## Interior citation — frontier hub `002E0FA0` (2026-09-18, SWE2-EC7)

`002E0FA0` — 126 B, 6 A-measured callers; the flag-fold that reads the `0215F1C0` dword
array `002E1CD0` bits into. Interior verified: a 0x20-stride SSE sweep `por`-accumulates the
whole table into two lanes (`002E0FC0`–`002E0FDD`), `psrldq` folds them to a single dword at
[`002E0FC5`](../../_index/ADDRESS-INDEX.md)/`002E0FEF`–`002E1005`, and when `00360360()` reports its flag set, bit
`0x13` of the aggregate is cleared before returning — an "any flags raised" query with one
mode-dependent mask-out.

## SWE2-EC7-29 update (2026-09-18) — `002E1CD0` `0215F1C0` flag-mask writer

`002E1CD0` (50 B) is the complementary flag-mask writer for the
`0215F1C0` 16-slot array the `por` sweep above accumulates: `edx >= 0x10`
bounds both arms; `ecx != 0` clears (`and [0215F1C0 + edx*4],
0xFFEC6DFC` — the `0x139203` channel bits off) while `ecx == 0` sets
(`or [0215F1C0 + edx*4], 0x139203`). Interior anchor `002E1CFA` (the
`or` set arm).
## SWE2-EC7-31 update (2026-09-18) — `00264F90` persistence-group getter

`00264F90` (49 B) is `MapRef_GetPersistenceGroupId` as the census row
names it: both `02099D88` (the map-record table) and `02099D90` (the
table's live flag) must be non-null, then the row base is the
self-relative pointer `r8 + dword[r8+4]` and `ecx` indexes 8-byte
slots — `word[slot+6]` is the answer, 0 when any of the three guards
fails. Interior anchor `00264FB9` (the `+6` word read).

## SWE2-EC7-37 update (2026-09-19) - `00576A50`

`00576A50` (529 B) is a navimap entry-id reader - `02CA9738`, `00309EC0`/`003148F0`/`003779F0`/`003C4AD0`/`00255060`/`00255120`/`002F9860`. Interior anchor `00576B65` (a `00309EC0` call).

## SWE2-EC7-47 update (2026-09-19) - `003F92B0`

`003F92B0` (216 B) is a body - `00254380`/`002543D0`/`00254F30`/`002AC2C0`/`002F9860`/`003148F0`/`00377870`. Interior anchor `003F92D3` (a `00254380` call).

## SWE2-EC7-47 update (2026-09-19) - `0031C000`

`0031C000` (212 B) is a body - `00313F60`/`0031BDC0`/`00377C70`. Interior anchor `0031C083` (a `00313F60` call).

## SWE2-EC7-77 update (2026-09-20) - `002543D0` + `00254380` counted-table indexers measured

`002543D0` (31 B) and `00254380` (31 B) are the `020927D0` counted
byte-table siblings: `edx = word[blob+8]` (or `+0xA`) + the blob base,
`byte[edx]` is the element count, and `ecx < count` returns
`byte[edx+1+ecx]` - else 0. Same counted-index shape the
`0209AC30` tables use.
Interior anchors `002543E9` / `00254399` (the `+1+ecx` byte loads).

## SWE2-EC7-102 update (2026-09-20) - `0028FF20` measured

`0028FF20` (81 B) is the conditional word-publish
`00251F40`, `00254AC0`, `00255330` and `003C5E50`
call on the `[0209BE80 + 0x10F80]` object: when the
slot is nonnull `002544B0()` runs; a return of 1
zeroes `word[+0x1D78]`, and `word[+0x1D7A]` always
gains bit 3 - the clear-and-arm sequence the
navimap paths post.
Interior anchor `0028FF4F` (the `+0x1D78` word
clear).

## SWE2-EC7-105 update (2026-09-20) - `00255120` + `00255060` measured

`00255120` (47 B) is the bounded row
select `003160C0` and `00576A50` run ahead
of the scanner: `ecx <= 0x180` computes
`020927C0 + 0x224 + ecx * 0x20`, sets
`edx = 0x20` and tails `00255060`; larger
indices answer `-1`.
Interior anchor `00255132` (the `0x224`
base add).

`00255060` (128 B) is the bitfield
cardinality scan `002550E0`, `00255120`,
`003160C0`, `003C17E0` and `00576A50`
call: over `edx` bytes at `rcx` it counts
set bits - a `0x00` byte contributes 0, a
`0xFF` byte contributes 8, anything else
is unfolded bit-by-bit - the popcount the
row selectors feed their answers through.
Interior anchor `00255075` (the loop-head
byte fetch).

## Cross-subsystem neighbours — SWE2-EC7 (pass-22 dispositions)

- **ActorEntity - CLIENT and SERVICE (122 edges).** `00225CD0` is also called by bodies filed to ActorEntity: `00263050`; `00225CD0` reaches bodies filed to ActorEntity: `00263FF0`, `00358940`, `00359B80` - shared machinery across the layer boundary, no shared ownership.
- **Audio - SERVICE (14 edges).** `00226280`, `00261F90` reach bodies filed to audio: `002DF370`, `002DEC00`, `002DEE50` - shared machinery across the layer boundary, no shared ownership.
- **CombatAI - CLIENT and SERVICE (22 edges).** `00253B90` is also called by bodies filed to combat AI: `00308610`; `00300FC0`, `00301AD0` reach bodies filed to combat AI: `003219D0`, `00308C20`, `0030BD00` - shared machinery across the layer boundary, no shared ownership.
- **CombatAction - CLIENT (64 edges).** `00225CD0`, `00226280`, `00226BE0` are also called by bodies filed to combat action: `00313DB0`, `002FFCF0` - shared machinery across the layer boundary, no shared ownership.
- **CombatFormula - SERVICE (21 edges).** `002F8BB0`, `002F9400`, `002FEF30` reach bodies filed to combat formula: `0031B860`, `00320AB0`, `002F8E50` - shared machinery across the layer boundary, no shared ownership.
- **CoreRuntimeScheduling - CLIENT and SERVICE (9 edges).** `00226280` is also called by bodies filed to core runtime: `0022B8C0`, `0022BC20`; `00253C70`, `002628B0` reach bodies filed to core runtime: `001EDE70`, `00229EE0` - shared machinery across the layer boundary, no shared ownership.
- **Gameplay - CLIENT and SERVICE (32 edges).** `00234DA0`, `00253B90` are also called by bodies filed to Gameplay: `00308040` (Combat), `00307D10` (Combat), `00309A90` (Combat); `002FEF30` reaches bodies filed to Gameplay: `00307D10` (Combat) - shared machinery across the layer boundary, no shared ownership.
- **Input - CLIENT and SERVICE (34 edges).** `0017DE10` is also called by bodies filed to input: `00253C70`; `0017DE10` reaches bodies filed to input: `00197710`, `00198790`, `0079E6A0` - shared machinery across the layer boundary, no shared ownership.
- **InputGameplay - CLIENT (2 edges).** `00253B90`, `00377C20` are also called by bodies filed to InputGameplay: `00313A00` (FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation) - shared machinery across the layer boundary, no shared ownership.
- **Items_Equipment_Shops_License - CLIENT (4 edges).** `002FEF30`, `00309EC0`, `00377C20` are also called by bodies filed to items/equipment: `0030A4E0`, `00317930`, `00309FB0` - shared machinery across the layer boundary, no shared ownership.
- **Movement - CLIENT (64 edges).** `00225CD0`, `00226280`, `00226BE0` are also called by bodies filed to movement: `0026A1D0`, `0026C3E0` - shared machinery across the layer boundary, no shared ownership.
- **Party - SERVICE (38 edges).** `00226BE0`, `00234DA0`, `002350C0` reach bodies filed to party: `00263750`, `003590D0`, `003273B0` - shared machinery across the layer boundary, no shared ownership.
- **PlatformOnlineAchievements - CLIENT (51 edges).** `002536A0` is also called by bodies filed to PlatformOnlineAchievements: `00315390`, `00315420`, `003154B0` - shared machinery across the layer boundary, no shared ownership.
- **Presentation - CLIENT and SERVICE (56 edges).** `00253B90`, `002543D0` are also called by bodies filed to presentation: `00308130`, `002B7B80` (UI), `002BAF80` (UI); `00226280` reaches bodies filed to presentation: `002EBBF0` - shared machinery across the layer boundary, no shared ownership.
- **Resource - CLIENT and SERVICE (31 edges).** `0032E400` is also called by bodies filed to resource: `00249210`; `002628B0`, `00291C80`, `003145E0` reach bodies filed to resource: `0032E520`, `0032E620` - shared machinery across the layer boundary, no shared ownership.
- **Rewards_Progression_Economy - CLIENT and SERVICE (15 edges).** `002F8BB0`, `002F90C0` are also called by bodies filed to rewards/progression: `00312280`; `0030E360`, `00312280` reach bodies filed to rewards/progression: `00312280`, `00253690` - shared machinery across the layer boundary, no shared ownership.
- **SaveLoad - SERVICE (1 edge).** `003145E0` reaches bodies filed to SaveLoad (save/load settings): `0020E500` (WorldTransition) - shared machinery across the layer boundary, no shared ownership.
- **Save_Load_Settings - CLIENT and SERVICE (22 edges).** `00254380`, `00264F90` are also called by bodies filed to save/load/settings: `00583D60`; `00261F90`, `002628B0` reach bodies filed to save/load/settings: `002EF2B0` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT and SERVICE (22 edges).** `00264F90`, `002E1CD0` are also called by bodies filed to script VM / native bridge: `00357450`, `0050CDE0`, `00344C60`; `00266D10` reaches bodies filed to script VM / native bridge: `003DC2D0` - shared machinery across the layer boundary, no shared ownership.
- **Spawn_Encounter_Lifecycle - CLIENT and SERVICE (7 edges).** `00234DA0`, `00313F60` are also called by bodies filed to spawn/encounter lifecycle: `00234AF0`, `00234DA0`; `002350C0`, `00300530` reach bodies filed to spawn/encounter lifecycle: `00306E60`, `00306F00` - shared machinery across the layer boundary, no shared ownership.
- **Status_Periodic_Terminal - CLIENT and SERVICE (31 edges).** `002F9400`, `002FEF30` are also called by bodies filed to status/periodic terminal: `00310DB0`, `0030FED0`; `002F9400` reaches bodies filed to status/periodic terminal: `00320450`, `00329A20` - shared machinery across the layer boundary, no shared ownership.
- **Story_Event_Quest_Hunt - SERVICE (3 edges).** `00253C70`, `0026C8C0`, `00583D60` reach bodies filed to story/event: `0032A8A0`, `00377440` - shared machinery across the layer boundary, no shared ownership.
- **UI - SERVICE (103 edges).** `00251F40` reaches bodies filed to UI: `0028FF20`, `00290030`, `00290060` - shared machinery across the layer boundary, no shared ownership.

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-field-record-table-navimapdata-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00255330` | 132 B | when `ecx` is not 1, calls `00251F40(dword 020927E8)`, ORs word `01E0C2AC` with 0xC and returns; when `ecx` is 1, unless both bits 0xC0 of dword `01E0C320` are set it calls `003C8990()`, `0035DAC0()`, `0028FF20()`, `003C58B0()`, `002B6140()`, `0035D5A0()`, `0035D0E0(dword 020927EC)`, `003C9900()` and `003BBFA0(0)` and clears bit 7 of dword `020927EC`, then in either case ANDs word `01E0C2AC` with 0xFFF3 and tail-jumps to `0017E7D0()` | `00255344`, `0025537D`, `0025538C`, `00255397`, `002553A7` |
| `002AC2C0` | 17 B | stores `cl` OR 0x80 to byte `01E0CDFF` and returns the address `01E0CDFC` | `002AC2C3`, `002AC2CA` |
| `003778B0` | 68 B | takes `i` = `00264F90()` and `p` = qword `02ADD0F8`; when `p` is non-null, `i` is below dword `p+8` (unsigned) and the word `w` at `p+0x10+2*(dword p+4 + i)` is non-zero, returns `p + w`, and otherwise returns the address `01CEB638` | `003778B4`, `003778C7`, `003778D3`, `003778E0`, `003778E8` |

## Homed bodies: functions reached only indirectly whose callees this page cites (FABLE, 2026-10-03, F homing)

*No page cited these functions and none of their callers is documented: they are reached by table or pointer dispatch or through undocumented callers. Each one calls something this page documents, which the sentence names. Each sentence states what the body does (access and representation, not purpose); the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's F homing pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-field-record-table-navimapdata-homing-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0031BD80` | 62 B | returns `0xffff` when `rcx` is null, when the call at `0031BD80+0xd` (with `rcx`) returns null, or when qword `+0x698` of that result is null; otherwise tail-jumps to `0031BDC0(that qword + 0x50, edx)` with the incoming `edx` | Interior anchor `0031BD8D`; Interior anchor `0031BD97`; Interior anchor `0031BDA3`; Interior anchor `0031BDAE`; Interior anchor `0031BDB3` |
