# Reconstruction readiness — `FFXII TZA/25-EBP-Script-Container/`

| | |
|---|---|
| Stream | R (reconstruction readiness), per [`docs/cloud-briefs/re-readiness.md`](../../docs/cloud-briefs/re-readiness.md) |
| Board task | `OPUS-CLOUD-R-READINESS-25-1002` |
| Date | 2026-10-02 |
| Snapshot | this repo's text snapshot at `86b70c69` only; no executable, Ghidra, extracted data or live game was used. Several pages in this folder are being edited by other lanes; every quote is the snapshot's text |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every item quotes or paraphrases a page and gives its location. |

## Counts

| | |
|---|---:|
| `.md` pages read (every one in the folder and its subfolders) | 14 |
| member `.tsv` files checked for layout and row counts | 4 |
| entry-point rows listed (§1.1) | _pending_ |
| open items the pages list themselves (§2.1) | _pending_ |
| structural gaps: a function, formula or format a port needs that no page states (§2.2) | _pending_ |
| **contradictions, total (§2.3)** | _pending_ |
| **Rating (§3)** | _pending_ |

## Citation form

`ABBR:line` means a line of the page below, as the snapshot has it. Every path is relative to
`FFXII TZA/25-EBP-Script-Container/`. "Not stated" means none of these fourteen pages says it. A claim the
pages make by linking to another category (for example the scripted-camera player in 17) is cited as the link
line here and marked "stated on another page"; those other pages were not read for this report.

| abbr | page | status as the page states it |
|---|---|---|
| README | `README.md` | category index; no front matter. Its unit table still calls seven units "*unknown*" (`README:42-51`); see C3 |
| CON | `Container/ebp2-container.md` | `status: AUDITED`, `evidence_tier: 1`, `audit.passes: 1`, `last_reviewed: 2026-09-12` (`CON:4-6`, `:19`, `:25`); `ebp_units: container` (`CON:22-23`) |
| S000 | `Bytecode-And-Opcodes/section-000-bytecode.md` | `status: AUDITED`, tier 1, `last_reviewed: 2026-09-11` (`S000:4-6`, `:19`); dated sections run to 2026-09-27 (`S000:557`) |
| S002 | `Sections/section-002-text.md` | `status: AUDITED`, **`evidence_tier: 9`**, `audit.passes: 2` (`S002:4-6`, `:23`), `last_reviewed: 2026-09-03` (`S002:19`) |
| S003 | `Sections/section-003-text.md` | `status: AUDITED`, **`evidence_tier: 9`**, `audit.passes: 2` (`S003:4-6`, `:23`), `last_reviewed: 2026-09-03` (`S003:19`) |
| S004 | `Sections/section-004.md` | `status: AUDITED`, tier 1, `reopened_count: 1` (`S004:4-6`, `:29`); the body calls its status `PARTIAL` (`S004:344-345`), see C14 |
| S006 | `Sections/section-006.md` | `status: AUDITED`, tier 1 (`S006:4-6`), `last_reviewed: 2026-09-03` (`S006:19`); dated text to 2026-09-28 (`S006:319`) |
| S008 | `Sections/section-008.md` | `status: AUDITED`, tier 1, `audit.passes: 2`, last pass 2026-09-13 (`S008:4-6`, `:23-24`) |
| S009 | `Sections/section-009.md` | `status: AUDITED`, tier 1, `audit.passes: 2`, last pass 2026-09-13 (`S009:4-6`, `:23-24`) |
| S010 | `Sections/section-010.md` | `status: AUDITED`, tier 1, `audit.passes: 1`, `reopened_count: 1` (`S010:4-6`, `:23`, `:28`) |
| S011 | `Sections/section-011.md` | `status: AUDITED`, tier 1, `audit.passes: 1`, `reopened_count: 1` (`S011:4-6`, `:23`, `:28`) |
| S012 | `Sections/section-012.md` | `status: AUDITED`, tier 1, `audit.passes: 1` (`S012:4-6`, `:23`), `last_reviewed: 2026-09-03` (`S012:19`) |
| S014 | `Sections/section-014.md` | `status: AUDITED`, tier 1, `audit.passes: 2`, `reopened_count: 1` (`S014:4-6`, `:23`, `:29`) |
| S016 | `Sections/section-016.md` | `status: AUDITED`, tier 1, `audit.passes: 2`, `corrections: 1` (`S016:4-6`, `:23`, `:30`), `last_reviewed: 2026-09-03` (`S016:19`) |
| S019 | `Sections/section-019.md` | `status: AUDITED`, tier 1, `audit.passes: 3`, `reopened_count: 1` (`S019:4-6`, `:23`, `:30`); the body calls its status `PARTIAL` (`S019:460-461`), see C15 |

**Member files checked** (layout and row counts only):

- `Bytecode-And-Opcodes/members/req-channel-census.tsv`: 530,028 data rows, columns
  `file script pc opcode opname args_push_order channel_class channel_byte ge80`, over 7,735 distinct files.
  Opcode counts: `REQ` 197,102, `REQEW` 101,398, `REQSW` 27,704, `REQWAIT` 126,506, `REQCHG` 16,956, `REQALL`
  47,812, `REQIALL` 3,699, `REQWAITALL` 8,851. `channel_class const-int` rows: 326,204, channel distribution
  `{0:18, 1:242611, 2:43738, 3:16446, 4:13347, 5:7929, 6:198, 7:1917}`, `ge80` 0. This matches S000's
  "All 326,204 channel operands … maximum `0x07`, zero ≥ `0x80`" (`S000:503-504`). `REQALL` / `REQIALL` rows carry
  `channel_class n/a`; see B5.
- `Bytecode-And-Opcodes/members/list-wait-census.tsv`: 60,362 data rows, columns
  `file script pc opname list_index lists_in_script in_range list_len pairs(…)`. Per opcode: `REQALL` 47,812 sites,
  0 out of range, 2,286 empty, longest 41; `REQIALL` 3,699 / 0 / 1,485 / 34; `REQWAITALL` 8,851 / 0 / 1,674 / 41.
  All exactly as S000's table (`S000:571-577`).
- `Bytecode-And-Opcodes/members/actdef-header-census.tsv`: 76 data rows (`+0x00` … `+0x4B`), columns
  `offset class distinct values`. **No page in the folder cites this file**; its generator says it covers "the first
  0x4C bytes of the section-0 header" for `OPUS-REQ-DATA-ACTORDEFINITIONPAYLOAD-HEADER-GAPS`. It agrees with
  S000 where they overlap (`+0x1C`–`+0x1F` ZERO, as `S000:87`; `+0x08` constant `0x9C`, as the one-file example at
  `S000:129`; `+0x10` constant `0x90`, the timestamp S000 says is "the first thing at `0x90`", `S000:125-126`).
  It does not reach `+0x50` or beyond.
- `Sections/members/section012-model-ids.tsv`: 482 data rows, columns `letter id model_stem resolves containers`.
  Distinct ids per letter `C 40, N 66, S 5, b 12, c 16, g 97, m 57, n 112, s 13, t 10, w 54`; resolving
  `b 10, c 5, g 77, m 50, n 77, s 10, t 8, w 14`, 251 of 482 overall (52.1 %); maxima `C 46, N 86, S 4`;
  35 unresolved `n` ids = ids 0–8 plus 26 others. All as S012 states (`S012:197-212`, `:342-343`, `:425-428`).

---

## 1. Interface

The folder documents **the `.ebp` file**, not the VM that runs it (`README:7-8`). A `.ebp` is a 0x60-byte header
and directory of 20 section offsets, dispatched by one function to fourteen per-slot handlers; each handler binds
its section's pointer into per-manager state, and a few parse or rewrite the section in place. The bytecode's
*semantics* are category 01's (`S000:605-609`).

### 1.1 Entry points (functions, with their callers)

#### Load path (container level)

| function | role | caller(s) as stated | cite |
|---|---|---|---|
| `WorldSimulation_ProcessDeferredModeRequest` `0x0032FC30` | head of the load path | `BattleAction_InitializeGlobalSpecialSequenceMode` (edges only, tier 2) | `CON:114`, `CON:697` |
| `ActorResource_BeginManagerResourceSetLoad` `0x0032FCA0` | picks `(namespace, index)` per manager index; ns-37 size override for managers 1–3 | `0x0032FC30`, "the *only* caller" | `CON:110-116`, `CON:131-176` |
| `ActorResource_BeginPrimaryPayloadLoad` `0x00330310` | size `FUN_0032e400`, allocate `FUN_0036a100`, tag `FUN_0036c660(buf, name, 0x95C)`, async read `FUN_0032e620` | `0x0032FCA0` | `CON:116-121`, `CON:607-613` |
| `ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources` `0x003304A0` (570 B) | **the directory walk**; the read completion callback | the async read | `CON:107-121`, `CON:285-293` |
| `ResourcePath_Get` `0x002DF980` | `pathTables[namespace][index]` | `0x0032FCA0` | `CON:129-131` |
| `FUN_002DF9A0` | populates the path-table selector array at runtime | boot initialiser `0x0022A0B0` (edges) | `CON:180-181`, `CON:219-220`, `CON:710` |
| `FUN_00332250` | whitelist `{5, 8, 37}` of namespaces | not stated (`00575710` also runs `0017FA90`, `CON:718-719`) | `CON:238-243` |

#### Per-slot handlers (from the dispatcher, in the dispatch table at `CON:339-354`)

| slot | handler | stores / binds | mask bit | parser or reader | cite |
|---:|---|---|---:|---|---|
| 0 | `ActorResource_OnDefinitionPayloadLoaded` `0x0032F850` | `DAT_022c6c28[manager]`; first-byte test `0032F87E` | not stated | `ActorManager_BindLoadedDefinitionPayload` `0x0026C8C0` (1,330 B) | `S000:151-167`, `S000:175-196` |
| 2 | `FUN_00330190` | `DAT_022C6CA0[mgr]`; binder `FUN_0026C880` → `ctx+0xA0` | 4 | `FUN_00264D60` (string), `FUN_002673A0` (bit 16); `mes` `0x00348DF0`, `fieldsignmes` `0x00356B70`; ten call sites | `S002:207-233`, `S002:284-285`, `S003:218` |
| 3 | `FUN_00330220` | `DAT_022C6CC8[mgr]`; binder `FUN_0026C8A0` → `ctx+0xA8` | 5 | `FUN_00264D90`; `fieldsign` (`0x0176`, `FUN_00355A00`), `fieldsignmesbyid` (`0x0179`, `FUN_00357120`) | `S003:168-171`, `S003:178-187`, `S003:211-216` |
| 4 | `FUN_00332100` (13 B) → `FUN_003DFDC0` (8 B) | `02B59D58` = `g_fieldRoots[2]`; manager index discarded | none ("no mask accounting") | **none identified** | `S004:137-155`, `S004:182-191`, `S004:277-278`, `CON:344` |
| 6 | `FUN_00330060` (170 B) | `022C6CF0[mgr]`; binder `FUN_0026C860` → `slot+0xB0`; then `FUN_0017F790`, tail `FUN_0029CAC0` (6-entry refcounted cache) → `FUN_0039BEC0` (TIM2 validate-and-register) | 6 | consumed as a resref by `002E16B0` (window `+0x1A8`) and `002B3400` (text element) | `S006:125-151`, `S006:319-327`, `CON:345` |
| 8 | `CAMCTL_OnLoaded` `0x0032FA10` | `g_cmlBlob = 0x022C6D80[slot]`; `0x0026CE00` → manager `+0xD8`; calls `CML1_ResolveNames` `0x003DA1F0` if `+0xE0` is present | 8 | readers of entry `+0x04`: `0x003DA400` (from `camerastart_7d` `0x0034F2F0`, `camerastart_7e` `0x0034F930`) and `0x003DA330` (from `camerahitcheck` `0x0034EDB0`, `camerahitcheck_33c` `0x0034E9B0`) | `S008:115-125`, `S008:136-139` |
| 9 | `CAMDAT_OnLoaded` `0x0032FAC0` | `DAT_022c6d58[mgr]`; loops `FUN_002566E0(slot, 0..3)`; `0x0026CE20` → manager `+0xE0` | 7 | `CAM7_Load` `0x002561C0` (498 B); runtime `002572E0` (attachment word), `00258350` (command stream) | `CON:347`, `S009:138-144`, `S009:169-171`, `S009:236-238`, `S009:316-318` |
| 10 | `SHKCTL_OnLoaded` `0x00331610` | `0x022C6DF8[mgr]`; `FUN_0026D3A0` → `0x02098F00` (manager `+0xF0`); calls `SHKCTL_ResolveNames` `0x003DD120` | 11 (`0x800`) | reader of entry `+0x04`: `0x003DD230` at `0x003DD29F` (from `camerashakestart_1a2` `0x003492F0`, `camerashakestart_1a3` `0x00349730`), which hands it to `0x0037DCF0` | `S010:164-173`, `S010:154`, `S010:271-279`, `S010:419-423` |
| 11 | `FUN_003316B0` | `DAT_022c6dd0[mgr]`, binder `FUN_0026d3c0` (per CON); loader `FUN_0037DA90` (42 instructions) builds bank `0x02ADD980` (stride `0x3D0`) | 10 (`0x400`) — but see A7 | runtime `FUN_0037D1F0` (8 oscillators); evaluator `003CC5F0` | `CON:349`, `S011:239-265`, `S011:288-304`, `S011:216-221`, `S011:460-467` |
| 12 | `FUN_0032FB70` (186 B) | `0x022C6DA8[mgr]`; `FUN_0026CE40` → manager `+0x100` | 9 | **none**: "nothing in this executable walks it" (2026-09-27) | `S012:85-118`, `S012:323-326` |
| 14 | `FUN_00330110` (122 B), **skipped for manager 0** (`0033066B`) | `022C6E20[mgr]`; when the pending mask drains, `ActorResource_FinalizeManagerRuntimeAfterLoads` `0x0032F1B0` → `FUN_0037AA90(ptr, mgr)` | 16 | `FUN_0037AA90` binds into `02EBF420 + slot*0x50`; manager 0's light set comes from the map pack via `003775D0` → `0037AA90([02ADD090], 0)` | `S014:258-282`, `S014:443-463`, `CON:395-406` |
| 16 | `FUN_003320E0` | tail `FUN_003DFE60(0, ptr)` → `g_fieldRoots[0]` `0x02B59D48` | none stated | `FieldData_CopyIndexedRecordByFormatClass` `0x003DFD00`; its four callers `FieldData_GetFormat0RecordVectorByIndex` `00320940`, `003209C0`, `setentrypos` (`0x0405`, `00354FB0`), `debug_positioninfo` (`0x2059`, `0050EBA0`) | `S016:142-160`, `S016:166`, `S016:316-320` |
| 17 | `FUN_00332110` | `FUN_003DFE60(1, ptr)` → `g_fieldRoots[1]`; **0 shipped files** | none stated | none | `CON:353`, `CON:388-391`, `S004:190` |
| 19 | `FUN_003320D0` (13 B) → `FUN_003EAA00` (105 B) | latches `02B5E0C8`; unbinds and releases the previous section first | none stated | `FUN_003DCF10(section + [+0x2C])`; record consumer `003DCA30`; `+0x0C` read by `003EA650` for `0035A3A0` / `0035AC60` | `S019:234-257`, `S019:264`, `S019:271-282`, `S019:466-469` |

Slots 1, 5, 7, 13, 15 and 18 have no handler (`CON:257-274`, `CON:392-394`).

#### Script-image entry points (section 0)

| function | role | caller(s) | cite |
|---|---|---|---|
| `ActorStorage_InitializeRecord` `0x00266530` | plants the record's `+0x48` function table, `+0x50` jump table, `+0x58` bytecode base from the script directory | not stated | `S000:409-416`, `S000:423-428` |
| `ActorResource_StartEntryScriptExecution` `0x003DBDC0` | pc = function offset + `[record+0x58]` | the interpreter `0x0025E4C0`; `ActorResource_SelectPendingEntryForExecution` `0x003DB6E0` | `S000:370-380`, `S000:397-402` |
| `ActorScriptResource_GetBytecodeOffsetById` `0x00358A00` | function id → offset; out of range returns 0 | `0x003DBDC0` | `S000:382-393`, `S000:434-435` |
| `FUN_003589E0` | jump index → offset | the `JMP` family at `002618AE`, `00261967`, `00261A63` | `S000:394-395`, `S000:436-440` |
| `ScriptVariable_Resolve` `0x00262440`; `PUSHI` `0x4E`; `PUSHF` `0x50`; `PUSHTAG` `0x4C` | readers of the four rebased tables | the interpreter | `S000:352-357` |
| `REQALL` `0x5F`, `REQIALL` `0x63`, `REQWAITALL` `0x61`; submitter `00268B10` | actor-list requests | the interpreter | `S000:528-545` |
| `002658B0(idx)` | reads the weather option through the manager record | only `0025ABA0` (transition chooser), from `0025ACA0`, from `002620E0` | `S000:283-293` |
| `002641B0(slot, index)` | resolves the trap table's packed reference | trap reader; also `BattleUnit_TryTriggerNearbyAuthoredFieldAction`'s sibling | `S000:256-257`, `S000:675-677` |
| `00264E30` | resolves the `local` variable class | not stated | `S000:362-365` |

#### Teardown and dead routes

| function | role | cite |
|---|---|---|
| `ActorResource_ResetManagerLoadState` `0x0032ED80` | frees and clears the slot-8, slot-9 and slot-12 stores | `S008:240-242`, `S009:241`, `S012:321` |
| `FUN_0032ED70` | the teardown the shake pages name (see B12) | `S010:181-182`, `S011:293-294` |
| `FUN_003DFA50` | tears down `g_fieldRoots[0..1]` in a loop, `02B59D58` separately; called at the top of `FUN_003319D0` | `S004:199-206`, `S016:161-162` |
| `FUN_002561A0` | invalidate CAM7 slot | `S009:235` |
| `FUN_003319D0` (`atelload.c`) | legacy per-map loader of `NV_ICON` / `POSENT` / `MAPARD` / `TREENT`; the directories it builds do not ship | `S004:245-270`, `S019:358-386` |
| `FUN_003306E0` | ATEL loose-file registration; "**never runs in this build**" | `S010:295`, `S011:327`, `S009:146-157` |
| `FUN_0032F3D0` | name-resolution gate; returns 0 for every call kind in the image | `S008:131-134` |
| `FUN_003DFAC0` | older `FF12POS` reader, unreachable | `S016:350-359` |

### 1.2 Inputs and outputs (data read and written, with record layouts)

#### The container

- **Header** (`CON:75-81`): `+0x00 u32 magic 'EBP2'` (never read), `+0x04 u32 slotCount` (= `0x14`, enforced),
  `+0x08`/`+0x0C` `u32` reserved (never read), `+0x10 u32[20] sectionOff`, indexed by section number, 0 = absent,
  file-relative.
- **Rules**: slot `n` is dispatched only if `slotCount > n`, unsigned (`CON:321-325`); a zero offset is absent
  (`CON:331`); length is "the **next present offset**", the last section runs to EOF (`CON:99-101`); bytes
  `0x60..0x80` are padding nothing reads (`CON:487-516`).
- **Pointer packing**: resolved pointer `OR` manager index in the low nibble, carried through 32 bits; every handler
  masks with `0xFFFFFFF0` (`CON:410-422`). So offsets must be 16-aligned (`CON:410-415`) and the buffer must lie
  below 4 GiB absolute (`CON:631`).
- **Non-container**: `us/event/evt_t/evt_t0020/evt_t0020.ebp` is a bare section body (`CON:555-565`).

#### Section 0 — the script image

- **Header** `0x90` bytes (`S000:79-117`). Read at load: `+0x14` (summed into record `+0x20`, `S000:219-224`),
  `+0x20`/`+0x24`/`+0x28`/`+0x2C` (sign-extended, rebased into record `+0x68`/`+0x70`/`+0x78`/`+0x80`), `+0x48`
  (zero-extended, rebased into `+0x50`), `+0x50` (`i16 >= 0` → record byte `+0x12`) (`S000:182-206`, `S000:230-234`).
  Read later: `+0x18` script directory (`S000:411-412`), `+0x30` list table (`S000:520-525`), `+0x38` `file`-class
  base into slot `+0x40` (`S000:360-361`), `+0x3C`/`+0x40` msp region (`S000:253-255`), `+0x4C` name pool, `+0x64`
  weather option (`S000:283-288`), `+0x6C` trap reference (`S000:108`, `S000:256-257`).
- **Script directory entry**, `0x30` bytes: `scriptNameOff`, `scriptType`, `pcId`, `scriptStartOff`,
  `numOfInstructions`, `nameOff` (→ record `+0x48`), `listOff` (→ `+0x50`), `sepaOff`, `stackBegin`,
  `duplicateId`, `pos` (`S000:417-432`). Stride `0x20` when the image's first word is below 8 (`S000:412-414`).
- **Packed reference**: tag bits 24–26, offset bits 0–23, resolved by `00265770`; tag 3 = `image + mspOffset + x`
  (`S000:253-255`).
- **Actor lists**: `table = payload + [payload + 0x30]` `{u32 count; u32 listOffset[count]}`;
  `list = {u32 count; {u16 actorOrdinal; u16 functionId}[count]}` (`S000:523-525`).
- **Weather option**: `byte[table + clamp(idx − 1, 0, 2) + 1]`, tested `> 0` (`S000:286-291`).

#### Sections 2 and 3 — text banks

`u32[count]` offset table then NUL-terminated strings; entry `= (flag << 16) | offset16`; engine count
`= firstDword >> 2` on the whole sign-extended dword; index masked to 24 bits; out of range or absent → the
eight-zero-byte string `&DAT_01CEB638` (`S002:77-132`, `S002:217-233`, `S002:252-255`; `S003:77-107`,
`S003:178-188`). Bit 16 (section 2 only) makes `mes` modal: written to message-slot byte `+0x38` at
`0215F200 + slot × 0x68` (`S002:360-370`). Character table: `S002:155-165`, `S003:125-133`.

#### Section 4 — `NAVIICN2`

`char[8] magic`, `u16 slotCount = 10`, ten `{u16 offset, u16 count}` slots, 16-byte records
`{s16 x1, y1, x2, y2, type; u8 ×6}` (`S004:70-117`). The handler reads none of it (`S004:157-166`).

#### Section 6 — `TIM2`

Sony `TIM2` with a 0x30-byte picture header and extended header (`S006:66-94`). Validated: non-null,
`strncmp(block, "TIM2", 4)`, `(*(u32*)(block + 0x40) & 0xF) == 1`; registered in the first free entry 1..7 of
`02AEE810`, returning 0 on failure or full (`S006:159-174`).

#### Sections 8 and 10 — `CML1`

16-byte header `{magic, u32 count, 0, 0}`; 16-byte entries `{u32 nameOffset (section-relative, signed), i32 index,
u32 _reserved0, u32 _reserved1}`; name blob after the entries (`S008:80-98`, `S010:78-97`, `S010:104-107`). At load
`+0x08` is zeroed and `+0x0C` has its low byte zeroed (`S008:159-160`, `S010:249-250`); the index is **not**
rewritten in the shipped build (`S008:131-134`, `S010:271-279`).

#### Section 9 — `CAM7`

0x20-byte header `{magic, cameraCount, countB, countC, 0, 0, 0, firstRecord}` (`S009:75-84`); variable-length
camera records `{0, recordLength, char[24] name, attachWord, eyeJoint, targetJoint, command stream from +0x28}`
(`S009:92-100`, `S009:102-107`); array B `u32`-prefixed ease curves, array C `u16`-prefixed paths (`S009:119-130`).
Output: per slot, `cameraCount × 0x40` runtime entries `{name[24], ptr → record+0x28, 0, 0, u16 eyeJoint,
u16 targetJoint}` and arrays of pointers into the blob (`S009:179-201`).

#### Section 11 — `SHK1`

Header `{magic, u16 recordCount, u16 curveCount, u16 dataOffset, u16 _unread, u32 _reserved0}`; `0x60`-byte
records `{char[24] name, u32 duration, u32 0, u16 curveId[32]}`; chained curves `{i32 byteLength, u32 keyCount,
f32 startTime, valueBefore, duration, valueAfter}` + 36-byte keys `{3 unread f32, startFrame, coefA..D,
weight}` (`S011:83-90`, `S011:120-125`, `S011:163-170`, `S011:188-198`). Evaluator: `S011:216-221`. Channel slot `k`
= parameter `k mod 4` of oscillator `k div 4` (`S011:462-465`).

#### Section 12 — actor manifest

`u32 count` then `count × {u16 id, u16 categoryLetter}` (`S012:52-68`); stored, never walked (`S012:323-326`).

#### Section 14 — `LGT2`

Header `{magic, u16 listOffset, u16 0, u16 1, u16 lightCount, u32 0}`, `lightCount × 0x70` light records, then a
chunk list `{u16 size, u16 type, payload}` ended by size 0 (`S014:69-96`). Bind record per slot
(`02EBF420 + slot*0x50`): `+0x00` base, `+0x08..+0x30` first chunk of types 0, 1, 2, 3, 6, 7, `+0x38` type-5
payload, `+0x4C` ready byte (`S014:139-154`). **Writes into the file buffer**: light `+0x21` remapped through
`01EF94E4` when `< 6`; for slot 0 light `+0x27 |= 0x20`; type-5 sub-entries encoded as runtime addresses
(`S014:169-184`); type 2 initialised only when `DAT_01ef94e0 != 0` (`S014:189-195`).

#### Section 16 — `FF12POS3`

Header `{char[8] magic, u32 size = 0x10 + 0x30*count, u32 count}`; 0x30-byte records `{u32 type, f32 extentA,
extentB, extentC, posX, posY, posZ, dir (radians), 4 × f32 0}`; terminator `0x0000000A` at `+size`
(`S016:79-103`). Accessor: byte 7 `>= '3'` → 0x30 records at `base + 0x10 + index*0x30`, else 0x10 legacy records;
`index >= count` → all-zero output (`S016:166-206`). Region sampling for types 0/1/2: `S016:333-343`.

#### Section 19 — `FF12AR03`

0x30-byte header with an eight-slot directory (`+0x10..+0x2C`), `+0x0C` trailer offset; table-A header at `0x30`
(`countA`), 16-byte records, table B after (`S019:102-125`, `S019:201-228`). Record per CC-10:
`{u32 modelKey; u16 class; u16 groupId; u16 motionIndex}` (`S019:466-469`). Handler follows only slot 7 (`+0x2C`)
(`S019:284-292`).

#### Outputs into the actor-manager record (`0x02098E10 + idx*0x288`, `CON:448`)

`+0x12` (bool from header `+0x50`), `+0x18`/`+0x1A` (main/sub frame owning camera channel), `+0x20` (sum),
`+0x40` (`file` class), `+0x50` (local storage), `+0x68`/`+0x70`/`+0x78`/`+0x80` (constant pools, descriptors,
tags), `+0xA0`/`+0xA8`/`+0xB0`/`+0xD8`/`+0xE0`/`+0xF0`/`+0xF8`/`+0x100` (section pointers, written only by binder
stubs), `+0x110 + 0x18·ch` (four camera channels), `+0x201` (`subStepOptIn`) (`S000:189-195`, `S008:149-151`,
`S008:234`, `CON:369-384`, `S000:548-550`).

### 1.3 State (globals and objects, with lifetime)

| state | what | lifetime and initial value | cite |
|---|---|---|---|
| per-manager arrays `022C6C28`, `022C6CA0`, `022C6CC8`, `022C6CF0`, `022C6D58`, `022C6D80`, `022C6DA8`, `022C6DD0`, `022C6DF8`, `022C6E20` | section pointer per manager, `base + mgr*8`, five entries | written by the slot handler; teardown frees and nulls (`0032ED80` / `0032ED70`); `022C6DF8` is nulled at init `0x0032F4C2` | `S000:160`, `S002:207`, `S003:168`, `S006:136`, `S008:120`, `CON:347-349`, `S012:91`, `S010:169`, `S014:271`, `S014:284-287`, `S010:181-182` |
| pending-resource mask `022C6E48[mgr]` | one bit per section (4, 5, 6, 7, 8, 9, 10, 11, 16) | cleared by each handler; finalize runs when it drains. **Who sets the bits on the `.ebp` route is not stated** (G2) | `S014:272-273`, `S014:289-292`, `S012:93`, `S012:153` |
| actor-manager record `02098E10 + idx*0x288` | see §1.2 | `ctx+0xA0` / `+0xA8` zeroed on field entry (`0026CC49`, `0026CC50`); `+0x100` cleared at `0026CC31` | `CON:448`, `S002:212-213`, `S003:170-171`, `S012:317` |
| current-manager cache `02099D70` | the installed slot pointer | installed at `0026CE60`, gated on `+0x10` / `+0x13` | `CON:382-383` |
| `g_fieldRoots[3]` at `02B59D48` | sections 16, 17, 4 | `003DFE60` writes 0/1, `003DFDC0` writes 2; `003DFA50` tears down | `S016:155-162`, `S004:182-203` |
| `02B5E0C8` (second entry of the `.ard` base table `02B5E0C0`) | section 19 | released and replaced on rebind | `S019:248-251`, `S019:271-276` |
| CAM7 tables `02092808` / `02092810` / `02092818` / `02092820` | blob, entries, array B, array C | per slot; stride `0xBB0` per S008; blob must stay resident | `S009:181-190`, `S008:210`, `S008:422` |
| SHK bank `02ADD980` (+ `02ADD988` curve pointers) | five slots × `0x3D0`; four `0xF0` sub-slots each | unbind `0037DA70` ignores slot ≥ 5 | `S011:258-262`, `S011:296-302` |
| `LGT2` bind table `02EBF420` | five × `0x50` | reset by `0037B230` before a bind; `+0x4C` set even on magic reject | `S014:139-167` |
| TIM2 cache `0209C320` and registry `02AEE810` | 6 × 16 refcounted; 8 pointers, slots 1–7 | not stated beyond claim / register | `S006:144-148`, `S006:170-174` |
| message slots `0215F200` | eight × `0x68` | `+0x38` / `+0x3E` bit 0 cleared by close and advance paths | `S002:364-370`, `S002:430-438` |
| image-address base `[01F83530]` | added by `0020E600` | zero at image load; "unwritten by every form searched", not proven (`CD-2` open) | `S019:286-288`, `S019:304-325`, `CON:631` |
| remap config `01EF94E0` / `01EF94E4` | type-2 enable and 6-entry remap | values not stated | `S014:191-202` |

### 1.4 Order (what runs when, and what triggers it)

1. A deferred mode request starts a manager's resource-set load; the `.ebp` is read whole, in one async read
   (`CON:113-125`).
2. On completion `0x003304A0` walks the directory. It is "a flat open-coded sequence" (`CON:336-337`); by the read
   addresses in `CON:256-275` the order is: slot-12 pre-pass (`003304E4`), 0, 2, 3, 6, 9, 8, 11, 10, 12, 16, 17, 4,
   19, 14 (14 only for manager ≠ 0). What the slot-12 pre-pass does is not stated (G4).
3. Each handler stores its pointer and clears its pending bit; slot 6 also registers the texture; slot 8/9 resolve
   whichever arrives second (`S008:236-238`); slot 10 calls `003DD120`; slot 11 builds the curve table.
4. When a manager's pending mask reaches zero, `0x0032F1B0` runs (from `00330175` and from the dispatcher tail at
   `003306BF`), and binds section 14 (`S014:289-292`). The rest of the finalizer is not stated (G5).
5. At script start, `ActorStorage_InitializeRecord` and `0x003DBDC0` turn the directory into a pc (`S000:397-416`).
6. Per frame: not stated on these pages, except that a modal message holds the field frame through the gate
   `00265680` (`S002:367-370`), and that `0025ABA0` chooses the next weather when called from the native-command
   family (`S000:288-293`).

### 1.5 Dependencies (on other systems)

- **01 Script VM**: interpreter, verb table and opcode semantics (`README:17-21`, `S000:605-609`).
- **02 Resource**: `ResourcePath_Get`, path tables, `0032E400` / `0032E620` (`CON:129-131`, `CON:180-236`);
  authored-table contract §7 for the zero image base (`S000:530-534`).
- **04 Actor**: actor-manager record and actor storage record (`CON:400-401`, `S000:449`).
- **03 World / map pack**: manager 0's light set (`CON:397-406`, `S014:456-463`).
- **17 Presentation**: scripted camera player (CAM7 command stream, ease curves, paths, channels) and shake sampler
  (`S009:102-107`, `S009:121-130`, `S011:458-467`); text and window rendering (`S006:319-327`).
- **16 UI**: `.fex` expansion-glyph tables (`S006:247-251`).
- **05 / 06 / 09**: POSENT consumers (`S016:321-330`).
- **21 RNG**: MT19937 coin for weather (`S000:291`), shared gameplay LCG for region sampling (`S016:337-338`).
- **14 / 19**: persistent flag bank (`README:137-140`, `S000:257`).
- **24 CRT memory**: the arena and its 32-bit link conditions (`CON:614-641`).
