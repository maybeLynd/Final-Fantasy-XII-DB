# SWE2-AUDIT-SEM types re-score 2: the twelve PARTIAL types cells after OPUS's declarations, 2026-10-03

run: types_census2.py at add0de2aa (scratch-output wrapper rescore2scratch/run_census.py)
affected: `_index/L2-VERDICTS.md` (types, L2 and binding-gap cells of S-09, S-10, S-14, S-17, S-39; types cells of S-16, S-22, S-25, S-28, S-31, S-36, S-45)

**Applied 2026-10-03 by the SWE2-AUDIT-SEM stand-in** (`Tools/work/SWE2-AUDIT-SEM/standin1003/apply_rescore2.py`): the 17 edits below plus 5 binding-gap closures for the MET rows (`edits_binding_gap.json`); after it the table reads types MET 45 / PARTIAL 7, L2 MET 32 / NOT MET 20, and `goal_gate.py` 20/52 NOT MET.


*Measured at HEAD `add0de2aa` (started at `15ec1ea71`; between the two, nothing changed in `L2-VERDICTS.md`, `_types/` or `important-subsystems.tsv`). EXE `73461d08…`. Proposal only: no page, type-store row or tool is edited here. The edits are in [`edits.json`](edits.json).*

## SWE2-AUDIT-SEM result

**Five types cells go MET: S-09, S-10, S-14, S-17 and S-39.** For each of them, the item that made the cell PARTIAL is now declared at the granularity the contract names, and a hand check of the rest of the contract's Types/State items finds nothing undeclared. Each of the five rows then has all five requirement cells MET, or LIVE with its ruling cited (S-09's runtime), so **their L2 cells go MET too**. Simulated on a scratch copy of the page, `goal_gate.check_verdicts` moves from `(False, '25/52 systems NOT MET (first: S-01)')` to `(False, '20/52 systems NOT MET (first: S-01)')`, and the L2 MET count from 27 to 32.

**Seven stay PARTIAL: S-16, S-22, S-25, S-28, S-31, S-36 and S-45.** In six of them the item the cell named is now declared or covered. In the seventh, S-31, the cell named the wrong item. Every one of the seven still has another contract-named item with no declaration at the named granularity. In all but S-36, census2 cannot see that item's form: a lower-case record name, a fenced layout with no type name, a symbol-named global, or a sub-section outside its grammar. In S-36 the item sits in a contract that census2 does not read. Each of the seven cells is re-worded so that it states its current reason. The old text is struck in place.

| system | cause the cell stated | now declared? | census2 class of that item | verdict | L2 effect |
|---|---|---|---|---|---|
| S-09 | `ResourceSectionHeader` (`+0x00` tag, `+0x10..+0x2F` name key) | yes: 0x30, PROVEN, `+0x000 tag`, `+0x010 nameKey` u8[32] (`5f91e98be`) | FIELD (both REC rows) | **MET** | **NOT MET → MET** (runtime LIVE, ruling cited) |
| S-10 | vf00.w `01EF93FC` | yes: `Vf00ConstantVector` 0x10 STATIC, `+0xC w` (`5f91e98be`) | FIELD | **MET** | **NOT MET → MET** |
| S-14 | spawn-counter table `02089340+0x4014` = `0208D354` | yes: `SpawnCounterRow` 0x80, ARRAY count 2, `counters` uint16[64] (`5f91e98be`) | FIELD | **MET** | **NOT MET → MET** |
| S-17 | capability row 12 `0215F1F0`; byte `0209A2C6` | yes: `CapabilityRow12Cell` 0x8; `GroupCompletionBytes0209A2C4 +0x002` int8 (`5f91e98be`, both HIGH) | FIELD (`0209A2C6` resolved here: census2's token is the base) | **MET** | **NOT MET → MET** |
| S-39 | handshake word `02EBA3F8` | yes: `BootHandshakeWord` 0x4 (`5f91e98be`) | FIELD | **MET** | **NOT MET → MET** |
| S-16 | `arcDeg` `02089358` | yes: `SpawnArcDegrees` | FIELD | PARTIAL, new reason: `g_nSpawnKeepReturnWindow` = `0208936C` UNDECLARED; format-class-0 candidate record has no type | none (contract SCOPE-SHORT too) |
| S-22 | `ActionDefinition +0x13` | yes: `+0x013 elementMask` | FIELD | PARTIAL, new reason: the recipe blob (`i32[...]` lists) has no declaration; `01EF9530..01EFA5B0` UNDECLARED | none (runtime MIXED too) |
| S-25 | `AiOrderSet` route had no `count=` | yes: `count=40`, HIGH (`50b624658`) | FIELD | PARTIAL, new reason: enmity threat vector `SpawnRecord +0x1A..` is not declared (GAP-SPAN, extent not established); `AiOrderRecord[14]` vs store `[12]`+tail | none (contract SCOPE-SHORT too) |
| S-28 | camera context 0 `02097D20` | covered: `CameraContext` 0x860, ARRAY count 2 | OBJECT (bare-base ruling `f8b2904c0`) | PARTIAL, new reason: §5's `+0x850` float and two `0xB0` blocks have no field rows | none (runtime MIXED) |
| S-31 | "`licenceOwnedBits` at `0208E680`" (misidentified) | `0208E680` is `BattlePackBlobPointer` (`5f91e98be`); `licenceOwnedBits` is `BattleStatsRecord +0x194`, already PROVEN | FIELD | PARTIAL, identification corrected; new reason: §8a.2 node-table fields `+4..+8` covered only by a 24-byte unobserved span | none (stays NOT MET) |
| S-36 | global tick `0208F570`; router `0215F1A0..0215F1AB`, `020927D8` | tick yes (`GlobalFrameTick`); router state **no** | tick FIELD; router contract not read by census2 | PARTIAL, reason narrowed to the router's §5a state | none (runtime MIXED) |
| S-45 | manager pointer cell `01F83450` | yes: `AchievementManager` 0x80, PTR | PTR-CELL | PARTIAL, new reason: manager `+0x18` flag has no field row; Steam context `+0x28` undeclared | none (stays NOT MET) |

## SWE2-AUDIT-SEM method

**census2 re-run without touching AUDIT-SPEC's package.** Scratch wrappers exec `types_census2.py` with only its output directory repointed (`rescore2scratch/run_census.py`). A second wrapper, `run_census_head.py`, also points both type-store reads at **HEAD copies** of `types.tsv`/`fields.tsv`. That was needed because the shared worktree carries a peer's uncommitted type-store edits (`git status`: ` M _types/fields.tsv`, ` M _types/types.tsv`). The verdicts here are scored on the committed store.
- HEAD-store run: selftest 11/11 PASS; `rows 501 {'FIELD': 337, 'PTR-CELL': 24, 'UNATTRIBUTED': 134, 'RANGE-START': 1, 'RANGE-END': 3, 'OBJECT': 1, 'AMBIGUOUS-DEREF': 1}`; `systems with UNDECLARED/UNTYPED/OUT-OF-EXTENT: []`.
- Worktree-store run: 500 rows. The twelve systems' rows are identical in the two runs.
- `git status --short` on `auditspec-l2-expansion-1003/` is empty after both runs.

**census2 per-system rows for the twelve** (HEAD store; FIELD / OBJECT / PTR-CELL / UNATTRIBUTED; every other class 0):

| system | FIELD | OBJECT | PTR-CELL | UNATTRIBUTED | what the UNATTRIBUTED rows are |
|---|---|---|---|---|---|
| S-09 | 24 | 0 | 0 | 9 | `AuthoredTableHeader`'s offset table `+0x00..+0x1C`. All 9 are contract-named, and all are declared: 8 FIELD, plus `+0x02` (reserved, no name in the contract), an exact-extent `unobservedSpan002` |
| S-10 | 7 | 0 | 0 | 0 | |
| S-14 | 8 | 0 | 0 | 0 | |
| S-16 | 2 | 0 | 0 | 0 | |
| S-17 | 12 | 0 | 2 | 0 | |
| S-22 | 19 | 0 | 0 | 0 | |
| S-25 | 1 | 0 | 0 | 0 | |
| S-28 | 8 | 1 | 0 | 1 | `ActorStorageRecord +0x0F` (presence code), FIELD `partyPresenceCode` |
| S-31 | 4 | 0 | 0 | 0 | |
| S-36 | 11 | 0 | 3 | 10 | the Widget header table `+0x00/+0x40/+0x44/+0x48/+0x98/+0x9C/+0xA0/+0xA1/+0xB4/+0xB8`, all FIELD on `Widget` |
| S-39 | 4 | 0 | 2 | 0 | |
| S-45 | 2 | 0 | 1 | 0 | |

**Why a census2 zero was not enough, and the hand sweep that replaced it.** census2 attributes record-relative state only when the record carries a CamelCase type name inline or heads a fenced layout. A sweep of the same ruled sections (`offs.py`) found **175 lines that carry a `+0xNN` offset; census2's record extractor consumes 10 of them and leaves 165** (a few of the 165 also hold an absolute address that census2 reads as ABS). The forms it leaves are:
- lower-case names: `unit +0x698`, `set + 0x20`, `statsRecord + 0x194`, `header+0x08`;
- fenced layouts headed by prose or by an all-caps name: `records:`, `ledger:`, `BKEI (unit + 0x6A0)`, `[02EBF190] -> the battle-state block`;
- offset tables with no type on the line.

census2 also never sees:
- globals named by symbol (`g_nSpawnKeepReturnWindow`);
- slash lists (`02EBF150/168/148/140`);
- indexed bytes: it reads `0209A2C4[2]` as `0209A2C4`;
- contracts credited by a row's contract cell but missing from `important-subsystems.tsv`'s contract column (S-36's router contract).

**How each such item was checked.** It was resolved by hand against the store with the old census's own `field_at` / `resolve`:
- `chk.py` takes item lists `items_a..e.txt`; their outputs `wt_*.out` (worktree store) and `head_*.out` (HEAD store) are identical except one field *name* (`01F7F594`: `aoRanLatch` vs `byte0114`, FIELD in both);
- `resolve_all.py` resolves bare addresses;
- `ruled.py` prints each contract's ruled sections, and these were read in full.

**A rule applied consistently, stated so it can be argued with.** A contract-named item covered by an unobserved/gap row of **exactly the extent the contract names** counts as declared. Its missing meaning is debt, which is a quality measure under the accepted criterion. A gap row **coarser** than the named item, or no field row at all, does not count (precision 1 of the ruling). The exact-extent cases accepted here are:
- S-09 `+0x02`;
- S-17 ledger padding `+0x11..+0x17`;
- S-39 `OrderedCommandList +0x2A`/`+0x2B` and `OrderedObject +0x11`;
- S-45 `AchievementState +0x04`, whose parent row `ImageBackedStateBlock +0x3848 flagBitmap3848` is a FIELD.

## SWE2-AUDIT-SEM evidence per row

**S-09 — MET.**
- `CONTRACT-resource-section-addressing.md` §3: `ResourceSectionHeader +0x000 tag` u32 and `+0x010 nameKey` u8[32] are FIELD. `ResourceEntry` (alias `RenderResourceEntry`) `+0x04/+0x10/+0x30/+0x38` are FIELD; `02B62E10` and `02B62E20` are FIELD.
- `CONTRACT-authored-table-row-lookup.md`: the 9 `AuthoredTableHeader` offsets are FIELD or exact-extent (above). `header+0x08`/`+0x0C` (State) are FIELD. Registry slots `02EBF008..02EBF200` are `AuthoredTableRegistrySlot` FIELD, and the Interface state row `01F83530` is FIELD.
- `CONTRACT-ard-area-binder.md`: `Ff12Ar03Header +0x00` char[8], `+0x0C`, `+0x10` u32[8], and `0215F000`/`0215F0A8` are FIELD.
- Everything the address sweep finds UNDECLARED in these files lies outside the ruled sections: invariants, the image-address-base essay, pass-22 neighbours, interior citations.

**S-10 — MET.** §3's record bytes `+0x00/+0x04/+0x0C/+0x0D/+0x0E` are `AuthoredExpressionRecord` FIELD at the named widths. §5's `01EF93E8`, `022D9138`, `022D91A0`, `022D92E0` and `022D92F0` are FIELD; `01EF93FC` is `Vf00ConstantVector +0xC w` FIELD.

**S-14 — MET.**
- §3: `BattleUnit +0x698 statsRecord`, `+0x6A0 spawnRecord`, `+0xE60 unitDefinitionRow`, `+0xE68 ardClassRow` and `SpawnRecord +0x80 battleStats` are FIELD.
- §5: `02EBF120`, `02EBF130` and `02EBF150/168/148/140` (the slash list resolved one by one) are FIELD. So are `02EBF190`, `02EBF170`, `02089300` (`RngReseedGate`), `0208D354` (`SpawnCounterRow`, span `0208D354..0208D454`, 2 rows) and `02EC1380`.

**S-17 — MET.**
- §3's head-less layouts are all FIELD: `SpawnRecord +0x08/+0x0C/+0x10`; `SpawnGroupLedger +0x00/+0x08/+0x10` (padding exact-extent); `BattleUnit +0x00 unitFlags`, `+0x698`, `+0x6A0`, `+0xE98`, `+0xE99`.
- §5 State: unit `+0x10`/`+0x40` are FIELD. `0208E690`/`0208E688` are PTR-CELL; `0208E6A0`, `0208D45C`, `01DFE0B8`, `02089340`, `01FD46D4`, `02098E20` and `02098E68` are FIELD. "u16 slot 3 of the table at `*(02098E68)`" is `02099DF6` in `FieldScratchBank`, FIELD. "the party suppression state behind `00359200`" is `PartyMovementLocks022C8000`, FIELD. `0215F1F0` and `0209A2C6` are FIELD. `008F8D80` is `.rdata` (30.0f), a constant as before.

**S-39 — MET.**
- §3: `OrderedCommandList +0x00..+0x18` is FIELD through the embedded `EastlPointerVector`; `+0x20/+0x24/+0x28/+0x29/+0x2C` are FIELD; `+0x2A`/`+0x2B` are exact-extent. `RenderCommandOwnerList +0x00..+0x18` is FIELD. `OrderedObject +0x00/+0x08/+0x10` are FIELD and `+0x11` u8[7] is exact-extent.
- §5: `01F7F5E0`/`01F7F5E8` are PTR-CELL; `01DF08FC`, `01F7F594`, `01FD4A88` and `02EBA3F8` are FIELD; render params `+0x199`/`+0x49C` are `PostProcessParamContext` FIELD.
- Quality notes, not coverage: the store calls `OrderedObject +0x08` `orderValue` where the contract says `executeTarget`, and it holds `+0x2A` unobserved where the contract gives it a meaning.

**S-16 — PARTIAL.** `02089358` is FIELD and `01F004E0` is FIELD.
- §5 names `g_nSpawnKeepReturnWindow`. That global is `0208936C` (i32, default 300: `spawn-placement-and-retirement.md` lines 85 and 511), and it resolves UNDECLARED.
- §3 and §5 name "the format-class-0 candidate record" (`+0x00` mode byte, `+0x10` authored position). No type in the store carries it: none of the `05-Spawn-Encounter-Lifecycle` types, and no type whose instance or evidence text mentions it.

**S-22 — PARTIAL.** Every census2 row is FIELD. By hand:
- `BattleStatsRecord +0x1C2/+0x2A..+0x30/+0x50` uint16[5] are FIELD;
- `01EFA5C0` is FIELD (`PreparationStepCalculatorTable`, 1616 = 202 × 8);
- `02AEDFB8`, `02AEDFE0`, `02AEE054/58/5C`, `02099DA8` and `02099DAC` are FIELD.

But `CONTRACT-weapon-recipes.md` §3 lays out `recipe blob i32[...]`, two lists each terminated by -1. `WeaponRecipeRef` (count 109) types each entry as `void*`, and its own evidence puts the blobs in `01EF9530..01EFA5B0`; `01EF9530` resolves UNDECLARED. Not used for the verdict: §5 of `CONTRACT-environmental-element-scaling.md` also names cross-system state in words only (the target's effect layers, the caster's merged bitmap, the target's field record).

**S-25 — PARTIAL.**
- **HIGH is enough for the extent.** The count does not need PROVEN. The accepted criterion asks for "a declared type with a measured extent", and its own text puts confidence and debt on the readiness side. 40 is measured, not assumed:
  - `00328105 add rax, 0x1c8` / `00328114 cmp rax, 0x4740`, re-decoded here from fn `00327F80`: 0x4740 / 0x1C8 = 40;
  - the next referenced object starts at `0208CCF8` = `02089378` + 40 × 0x170. The span resolves as `0x2089378..0x208ccf8`, stride 368.
  - What PROVEN still needs, by the route's own words, is the writer census of the `+4` index byte. That is a bound on access, not on the storage. This re-score applies the same reading to S-17, whose two declarations are HIGH (`CapabilityRow12Cell`, `GroupCompletionBytes0209A2C4`).
- **Residual 1, the threat vector.** `CONTRACT-enmity.md` §3 lays out `BKEI (unit + 0x6A0)`, which is `SpawnRecord` (`BattleUnit +0x6A0 spawnRecord`): `+0x19` the decay timer is FIELD (`bEnmityDecayTimer`), and `+0x1A..` is "one threat byte per combatant id". §5 says the vector is owned state. The store has `+0x01A unobservedSpan001A` u8[6], whose meaning text says it is *"NOT part of the enmity vector… the vector's extent is not established"*, and then `+0x020 copiedBlock0020`. So the vector has no declaration with a measured extent.
- **Residual 2, the record array.** `CONTRACT-gambit-walk.md` §3, corrected 2026-10-02, names `set + 0x20` as `AiOrderRecord[14]`. The store has `+0x020 orders AiOrderRecord[12]` and `+0x140 unobservedTail0140` u8[48], so records 12 and 13 fall in a 48-byte gap row, coarser than a 24-byte record.
- Every other §3 item is FIELD: `set + 0x00` u8[32]; `record + 0x04` flags; `unit + 0x708` (`actionContextPtr AiOrderRecord*`), `+0x714`, `+0x698`; `stats[+0x05]`.

**S-28 — PARTIAL.** `02097D20` is OBJECT, as the request expected. But §5 of `CONTRACT-party-focus-and-control-suppression.md` names "camera context 0's two `0xB0` blocks and its `+0x850` float", and `CameraContext` has no field rows at all, so `CameraContext +0x850` resolves `GAP-SPAN (no field row)`. Everything else is FIELD:
- `PartyRosterSlots`;
- `ActorStorageRecord +0x0F/+0x12/+0xC0`;
- the focus block `022C7FE0/E4/E8/F8`;
- `BattleUnit +0x698/+0x6B4/+0x6B7/+0x714`;
- `BattleSystemState +0x0000/+0x0004/+0x0008` (`BattleStatsRecord[40]`), the five maps `+0x5A48..+0x5A90` (uint16[9] each), `+0x5AA4`, `+0x5AC8` and `+0x5ACC`.

**S-31 — PARTIAL, identification corrected.**
- `0208E680` is the `battle_pack.bin` blob pointer: §3 says *"bound … from the `battle_pack.bin` blob (`0208E680`) directory `+0x34`"*, and §8a.2 says *"`0208E680` holds the encoded handle of the `battle_pack.bin` blob"*. It is declared `BattlePackBlobPointer` (FIELD `blob`).
- `licenceOwnedBits` is `BattleStatsRecord +0x194` uint8[46]. It is reached as `statsRecord + 0x194`, which census2 cannot read, and it was declared PROVEN before 2026-10-03.
- Every §3/§5 item is FIELD: `+0x004`, `+0x005`, `+0x194`, `02EBF038`, `02EBF130` and `02EBF138`.
- **Residual.** §8a.2 (FABLE, 2026-10-03, the section that answers this row's narrow SCOPE-SHORT) names the node-table row fields `+4` LP cost, `+5` category, `+6` square kind, `+7` start mask and `+8` ids. `LicenseNodeRecord` declares only `+0x000 unobservedSpan000` u8[24]. Its instance column also still reads "360 records in license_data.bin", where the contract says the game reads the 361-record `st2e` table at `02EBF038`.
- The rest of §8a.2 is FIELD: `+0x190 licencePoints`, `+0x20`, `+0x1C3/+0x1C4/+0x1C5`, the boards `02EBF1A0..02EBF1F8`, and `01EF91E0`.

**S-36 — PARTIAL, narrowed.** In `CONTRACT-widget-object.md`, every named item is FIELD or PTR-CELL:
- the WidgetMessage `+0x00/+0x08/+0x10`;
- the Widget header and draw-time fields `+0x00/+0x10/+0x18/+0x20/+0x38/+0x40/+0x44/+0x48/+0x9C/+0xA0/+0xA1/+0xA2/+0xAC/+0xAD/+0xB4/+0xB8`;
- the EC7-26 state-commit fields `+0x70/+0x80/+0x84/+0x86/+0x8C/+0x8E/+0x90/+0x94/+0x98/+0x9A`;
- `WidgetDrawRecord +0x58/+0x5A`;
- the asset widget's `+0xC0/+0xC8/+0xD0` (`WidgetSingleton02AEE4C0`);
- the globals and `0208F570`.

The contract cell also credits `16-UI/CONTRACT-ui-request-router.md`, whose §5a State table names six cells. All six resolve UNDECLARED: `0215F1A0`, `0215F1A1`, `0215F1A4`, `0215F1A8`, `020927D8` and `01E0C2C0` (u32[22]). §5a itself says *"The fields proposal declares them"*, and that proposal has not landed. `important-subsystems.tsv` lists only `CONTRACT-widget-object.md` for S-36, which is why census2 cannot see this.

**S-45 — PARTIAL.** `01F83450` is PTR-CELL. `AchievementDescriptor +0x00/+0x01/+0x02/+0x04` (table `00D10460`, 30 × 8) is FIELD. `AchievementState +0x00`/`+0x08` are FIELD and `+0x04` is exact-extent. `SteamAchievementRecord +0x08/+0x10/+0x90/+0x190/+0x194` and `01DFE410` are FIELD. Two items in `CONTRACT-steam-integration-subsystem.md` §2 are not declared:
- **the manager's `+0x18` "stats received" flag.** `AchievementManager`'s field rows end at `+0x014 achievedCount`, so `+0x18` reads `GAP-SPAN (no field row)`;
- **the Steam API context's `+0x28` user-stats interface.** `SteamApiContextInitHeader` is 0x10, and its own row says the returned context sits at this block + 0x10 *"per the Steamworks ABI … INFERENCE"*. `01DFE0E0` and `01DFE108` resolve UNDECLARED.

## SWE2-AUDIT-SEM decisions a reviewer may contest

1. **S-25: HIGH counts as a measured extent** (above). If the ruling is that the extent must be PROVEN, S-25's verdict does not change, because it is PARTIAL on two other items.
2. **S-31: §8a is in the denominator.** census2's grammar reads only `##` headings that name types, state or objects, so it skips `## 8a`. The accepted ruling's denominator is "Types and State sections and any interface-table state column". §8a.2, *"What it reads and writes"*, is the state enumeration of the scope that §8a adds to answer the row's SCOPE-SHORT. Leaving it out would let a contract widen its scope without widening its types denominator. **If AUDIT-SPEC rules §8a out, S-31 types is MET** (every §3/§5 item FIELD, as above), and so is its L2 cell, because its other four cells are MET.
3. **The exact-extent rule for gap rows** (method section). If AUDIT-SPEC rules that such a row does not satisfy the cell, S-09, S-17 and S-39 return to PARTIAL on those items. S-45 is PARTIAL either way.

## SWE2-AUDIT-SEM follow-ups not in edits.json

- **Binding-gap cells.** The gap cells of S-09, S-10, S-14, S-17 and S-39 still lead with "types PARTIAL … closes with OPUS's declaration". Once the types cells change, those leads are stale and should be struck by the cell's next writer. The seven PARTIAL rows' gap cells name the old item and should name the new one. `edits.json` carries only types and L2 cells, as requested.
- **Declaration work list for the seven PARTIAL rows**, the type store's owner:
  - S-16: `0208936C` i32; a format-class-0 candidate-record type.
  - S-22: the recipe blob layout.
  - S-25: the threat vector from `SpawnRecord +0x1A`, and `AiOrderRecord[14]`.
  - S-28: `CameraContext +0x850` and the two `0xB0` blocks.
  - S-31: `LicenseNodeRecord +4..+8`, and its instance column.
  - S-36: the router's `0215F1A0/A1/A4/A8`, `020927D8` and `01E0C2C0`.
  - S-45: `AchievementManager +0x18` and the Steam context.
- **The blind spots apply to all 40 types cells now MET.** None of them was checked here: they are outside this request. Every one rests on census2 or the older census, and both miss the forms listed in the method section. In these twelve rows the hand sweep turned up seven residuals that census2 did not report. A census pass that reads lower-case and head-less layouts, symbol names, slash lists, `ADDR[n]`, and contracts credited only in the contract cell is the instrument fix. Until it exists, a "census2 zero" is not a types MET.

## SWE2-AUDIT-SEM reproduction

The scripts are in `Database/Tools/work/SWE2-AUDIT-SEM/rescore2scratch/`, run with the analysis venv:
- `run_census.py` and `run_census_head.py`: census2, written to scratch; the second against the HEAD store.
- `list_cells.py`: verdict words via `progress_report.parse_verdicts`.
- `per_system.py`: census2 rows per system.
- `offs.py`, `ruled.py`, `ctx.py`: ruled-section text.
- `resolve_all.py` and `chk.py` (`HEADSTORE=` for the committed store): item resolution.
- `make_edits.py`: builds `edits.json` from the current cells. It checks every edit:
  - `old` equals the current cell;
  - no `|` or newline in `new`;
  - each struck span quotes `old`, and no `~~` is nested;
  - `_cell_verdict(new)` gives the intended word.

  It then simulates the page and `goal_gate` (17 edits, FAILS 0).


## SWE2-AUDIT-SEM consumers

- consumer: the L2 verdict table's 12 types cells, 5 L2 cells and 5 binding-gap cells - revised-here (old verdicts struck in place).
- consumer: PROGRESS.md and the progress snapshot (L2 27 -> 32) - routed-to- the derived-surface gate, which regenerates or labels them STALE in the publishing commit.
- consumer: `auditsem-types-rescore-1003` (the PARTIAL re-score this follows up) - agrees; its causes are closed or re-worded here.
- consumer: SWE2-AUDIT-SPEC's census2 (`types_census2.py`) - agrees on every item it can see; its extractor blind spot is recorded above for SWE2-AUDIT-SPEC.
