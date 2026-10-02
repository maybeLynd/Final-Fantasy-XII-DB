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

---

## 2. Gaps

### 2.1 Open or partly open items the pages themselves list

| # | item | cite |
|---:|---|---|
| O1 | Whether a non-`us`/non-BW-1 tree populates slot 17: "needs the `jp`/`eu` trees, which are not unpacked here". BW-1's census covered nine trees (`us kr it in fr es de cn ch`), none of them `jp` | `CON:583-584`, `CON:91-95` |
| O2 | Where the arena's backing blocks land in a running process, and whether `DYNAMIC_BASE` clear describes it (`CI-1`) | `CON:626-627`, `CON:640-641` |
| O3 | "The game does not write `.ebp`" rests on no header-constructing code on the read path, "not on an exhaustive scan" | `CON:644-646` |
| O4 | `0025B580` after a submit; target `+0x10`, `+0x24`, `+0x26` "beyond per-channel masks"; why lists are empty | `S000:584-587` |
| O5 | What an individual tag entry means beyond the pushed word | `S000:623-624` |
| O6 | The 17 non-printable author fields | `S000:632` |
| O7 | The language decoders `FUN_00267930` / `FUN_00267bb0` / `FUN_00267c20`: "their bodies were not read" | `S000:633-635` |
| O8 | Header `+0x52..+0x54` "contents unknown"; `+0x78`–`+0x8C` "not individually characterised" (oracle names only) | `S000:101`, `S000:111-116`, `S000:260-261` |
| O9 | Whether any reader other than `002658B0` weighs the weather bytes | `S000:294-295` |
| O10 | Meaning of every text escape code (`0x0F` 44 codes, `0x0E` 32, `0x10` 196) | `S002:353-356` |
| O11 | Which of the other `002E16B0` openers open a deferred flagged window | `S002:371-375` |
| O12 | Whether authored scripts ever set message-id bits 24–31 | `S002:379-380` |
| O13 | Where a caption is drawn: `FUN_00269F20` "was not read" | `S003:331-333` |
| O14 | Why 543 caption slots are placeholders | `S003:334-335` |
| O15 | Section 4's live reader: "**not identified**. `PROPOSED-c9-4`" | `S004:277-278` |
| O16 | Section 4 type-to-icon mapping, record bytes `+0x0A`/`+0x0B`/`+0x0D`/`+0x0E`/`+0x0F`, coordinate space | `S004:349-353` |
| O17 | Whether `0039BAD0` / `0039C4A0` resolve the registered TIM2 form: "the register-side link is not" proven | `S006:326-327` |
| O18 | The glyph width source for TIM2 strips, "still open" | `S006:268-270` |
| O19 | Second TIM2 picture header not walked; pixel data not decoded; not compared with the 447 `.tm2` | `S006:333-337` |
| O20 | Whether `CAM7_Load` can be reached with slot ≥ 5 | `S009:320-321` |
| O21 | Shake chunk `+0x08`/`+0x0C` purpose; whether the two pointer copies differ in lifetime ("The second was not traced") | `S010:477-481` |
| O22 | Whether SHK1 `+0x0C` is read outside `FUN_0037da90` | `S011:473-475` |
| O23 | What the rest of `FUN_003306e0` (984 instructions) does | `S011:480-481` |
| O24 | Section 12: "The section's reader is still unlocated"; lowercase ids do not follow the decoder's block order; what `n` ids 0–8 denote | `S012:347-351`, `S012:366-368` |
| O25 | Section 14: the 0x70-byte light record beyond `+0x21`/`+0x27`; type-3 and type-6 payloads; consumers of the bound chunk pointers; which manager index a map gets | `S014:426-437` |
| O26 | `0037B230` (slot reset) and `0037A9B0` (type-2 initialiser) not read | `S014:236-237` |
| O27 | `CD-1` residue: which authored file fills `02ADD090` (answered in-page as the map pack's slot 17) | `S014:454`, `S014:456-463` |
| O28 | POSENT terminator `0x0000000A` has no reader; no writer search beyond the magic and `g_fieldRoots` | `S016:360-364` |
| O29 | Section 19 table B "not decoded at all" | `S019:226-228`, `S019:473` |
| O30 | `CD-2` "stays open" for a write watchpoint on `01F83530` | `S019:315-318` |
| O31 | Byte compatibility of section 19 and a standalone `.ard`: `PROPOSED-c9-5` | `S019:395-398`, `S019:476-478` |

### 2.2 Structural gaps: what a port needs and no page states

These are things a re-implementation has to decide that none of the fourteen pages states. Several may be stated
on pages in other categories; this report did not read those.

| # | gap | why a port needs it | where the gap shows |
|---:|---|---|---|
| G1 | **Which manager index loads which `.ebp`, and how many managers there are.** The pages give five pointer entries per array (`S014:284-287`) and manager 0 as "the primary area manager that runs the field frame" (`CON:400`). What managers 1–4 are, which id each is given, and how `id` is chosen in the three-way branch is not stated | the namespace, index stride and slot-14 skip all key on the manager index | `CON:134-138`, `CON:395-396`, `S009:218-219` (nibble admits 0–15) |
| G2 | **Who sets the pending-resource bits on the `.ebp` route.** Every handler clears one (`btr`), and finalize runs when the mask drains. The only setter quoted is `OR qword ptr [RDI],0x10000` in the `LGTDAT` registration (`S014:234`), inside `003306E0`, which "never runs in this build" (`S010:295`) | without the initial mask a port cannot reproduce the finalize barrier | `S014:289-292`, `S014:297-303` |
| G3 | **What the ns-37 size probe sizes.** The probe index is `lea eax, [rbp + 3]` (`CON:164`); under the stated layout `index mod 4 = 3` is `.vpcjp` (`CON:186`). The page says only "the size is taken from namespace 37" (`CON:174`), not for which asset, nor what the request's own index is | the read size of the `.ebp` | `CON:164`, `CON:174-176`, `CON:186` |
| G4 | **The slot-12 pre-pass** at `003304E4` is listed as a read and not described | dispatch order and any early decision it makes | `CON:268` |
| G5 | **`ActorResource_FinalizeManagerRuntimeAfterLoads` (`0032F1B0`) beyond the slot-14 bind.** S012 lists it "❌"; S014 notes Ghidra "rendered … two calls where the listing has eight" and names only the `0037AA90` call | what else happens at the load barrier | `S012:146`, `S014:359`, `S014:278-281` |
| G6 | **The rest of `ActorManager_BindLoadedDefinitionPayload`.** Only its read set is tabled; it also sets fade parameters and movement speed, calls `PartyControl_SetMovementSuppressionBit` and `EventMemory_QueryDefinitionIdAbsent` (edges only), and its record writes beyond the rebased fields and `+0x12` are not stated. What record `+0x12` means is not stated | header binding is the first step of every script | `S000:175-196`, `S000:666-673`, `S000:686`, `S000:689` |
| G7 | **How header `+0x64` reaches the manager record.** `002658B0` "reads the manager record … resolves its `+0x64` reference" with a "version word `≥ 7`" (`S000:285-287`), but the binder does not read header `+0x64` (`S000:196`). Who copies or points the record at it, and what the version word is, are not stated | the weather chooser | `S000:196`, `S000:285-288` |
| G8 | **The remaining option and table fields**: `+0x60`, `+0x68`, `+0x70` (5 offsets), `+0x74`, `+0x54`/`+0x58`/`+0x5C`, `+0x34`. Shapes and arities only; no reader or meaning | a port must at least know whether any engine path reads them | `S000:88-110`, `S000:136-142` |
| G9 | **Text rendering**: escape semantics, the glyph table for `0x10` two-byte escapes, and the language decoders | every `mes` | `S002:181-185`, `S002:353-356`, `S000:633-635` |
| G10 | **Section 4 has no consumer.** The format is bound and never read on any traced path | either the map-icon feature cannot be ported, or it is dead | `S004:165-166`, `S004:277-278` |
| G11 | **TIM2 palette and draw path.** The palette "is not in this section" (`S006:99-102`); the 2026-09-25 note says "the text renderer supplies colours" (`S006:274-275`) without saying which; `0039BF50` "not read" | drawing a section-6 strip | `S006:223`, `S006:274-275`, `S006:326-327` |
| G12 | **The CAM7 command stream, ease curves and paths** are summarised here and decoded on the scripted-camera page in 17 (stated on another page). The per-field layout of a key (0x40) and segment (0x2C) is not on these pages | playing a camera | `S009:102-107`, `S009:119-130` |
| G13 | **The shake runtime.** `FUN_0037D1F0` as eight sine oscillators is stated with a pointer to 17 (`S011:458-467`); the oscillator formula, units and the role of record `duration` are not stated here. `0037DCF0`, which receives the index from `003DD230`, is not described | playing a shake | `S010:278`, `S011:349-352`, `S011:458-467` |
| G14 | **The light record and chunk payloads** (types 0, 2, 3, 5, 6), the values of the 6-entry remap table at `01EF94E4`, and the meaning of `+0x27` bit `0x20` | lighting | `S014:173-184`, `S014:426-432` |
| G15 | **Section 19 table B**, and `003DCF10` / `003DCA30` beyond the record decode (stated on another page) | area data | `S019:224-228`, `S019:466-472` |
| G16 | **POSENT engine-fixed entries 8 and 32**: which entry roles these are is stated only as "steers against entry 8" and "reads entry 32" | engine behaviour that depends on authored index | `S016:325-326` |
| G17 | **Wait kinds 5 and 7** for `REQWAITALL` / `REQALL`: their scheduling is stated per opcode; the wait record (`+0x15`, `+0x1C`, `+0x22`, `+0x26`) is partial, and the submit paths `003DBB60` / `003DBBE0` are named, not described | actor-list requests | `S000:543-563` |
| G18 | **The weather chooser's order** when only one alternative is open and its weather numbering (weather 1..3 via `clamp(idx − 1, 0, 2) + 1`; weather 0 not stated) | weather transitions | `S000:286-292` |
| G19 | **Message-slot record `0215F200`** (eight × `0x68`): only `+0x10`..`+0x16`, `+0x38`, `+0x3A`, `+0x3E` bits 0–1 are given | modal message state | `S002:364-370`, `S002:430-438` |
| G20 | **Teardown order and content** across all sections: given piecemeal (slots 8, 9, 10, 11, 12, 4, 16, 19); slots 2, 3, 6, 14 teardown not stated | unload / map change | `S008:240-242`, `S009:241`, `S010:181`, `S011:293-294`, `S004:177-180`, `S019:248-250` |
| G21 | **Section 12's purpose at runtime**: nothing walks it (`S012:323-326`), yet the model-id decoder's lowercase mapping (`id × 25` blocks) does not match the §5 `id + 1000` rule (`S012:349-351`) | the cast list, if any port feature uses it | `S012:332-351` |
| G22 | **Where `.ebp` buffers live** so the 32-bit pointer conditions hold: the rule is stated ("keep resource buffers within 4 GiB of the base, or widen every reference and link"), the allocator's placement is not | memory layout of a port | `CON:628-631`, `CON:640-641` |

**Fields a documented function writes but no page explains:** record `+0x12` from header `+0x50` (`S000:195`);
light `+0x21` (remapped) and `+0x27` bit `0x20` (`S014:173-179`); TIM2 cache refcount (`S006:145-147`); `LGT2`
slot `+0x4C` "ready" (`S014:154`, consumer not stated); CAM7 runtime entry `+0x20`/`+0x28` written zero
(`S009:197-198`, use not stated).

### 2.3 CONTRADICTIONS

These are statements a re-implementer would have to choose between. Each item quotes both sides exactly, with
`ABBR:line`.

- **A** is value-changing: an offset, address, constant, field role, formula or control flow that a port would
  hard-code, where believing the wrong side gives different behaviour. Every A item is **page-text only - needs
  local check**: this session cannot see the executable.
- **B** is a count, size or address that disagrees but changes no ported behaviour. These are also page-text only.
- **C** is a stale "open / not read" claim that a later dated section answers, a status banner or front matter that
  disagrees with the body, or a corrected name still in use.

A favoured side is named **only** where a dated correction on the pages settles it. Otherwise the item says "not
settled on the pages".

#### A. Value-changing

**A1. `CML1` binding: authored index, or name lookup (sections 8, 10, 11).**
- Name side, unstruck:
  - S008 lede: "**The index that ships in the file is never used** — the engine recomputes it by name." (`S008:34-35`)
  - S008 box: "**Renaming a camera in `section_009` breaks the link; renumbering the index column in `section_008` does nothing at all.**" (`S008:194-195`)
  - S008 key addresses: "`CML1_ResolveNames` — the only reader of this section (… index write-back `0x003DA28F` …)" (`S008:250`)
  - S010 §1: "**renumbering `index` does nothing, because the engine recomputes it — but renaming a shake in `section_011` breaks the link.**" (`S010:68-69`); again at `S010:261-262`; and "it is an input the engine consumes and then overwrites" (`S010:443-444`)
  - S011 propagated correction: "`SHKCTL_ResolveNames` (`0x003DD120`), which resolves `section_010`'s entries by **name**" (`S011:416-417`)
- Index side:
  - "**CORRECTED 2026-09-12 (FABLE) — the resolver below never resolves anything in the shipped build, so the authored index column is the binding.**" (`S008:131-132`); "**REVERSED 2026-09-12 — the box above has the direction wrong.** … **Renumbering the index column in `section_008` changes which camera a script plays; renaming a camera in `section_009` changes nothing**" (`S008:198-200`)
  - "**CORRECTED 2026-09-12 (FABLE) — the resolving store above never executes in the shipped build.** … **renumbering `index` in `section_010` changes which shake plays, and renaming a shake in `section_011` changes nothing**" (`S010:271-276`)
  - S011: "the only reader of this section's record names that has been found, `Shk1_FindByName`, is unreachable, and `section_010` binds by its authored index." (`S011:411-413`)
- The difference shows in data: "in **all eleven** the authored index points at the **later** of the two same-named records … in **seven** of the eleven the two records differ" (`S008:201-203`).
- **Favoured: the authored index, by the dated corrections of 2026-09-12** (`S008:131`, `S010:271`). *Page-text only - needs local check.*

**A2. Text-bank entry count: low `u16` of the first entry, or the whole first dword.**
- Field tables: "section `+0x00` low u16 (first offset) | `0x00264D74` | — | — | no — **doubles as the entry count** (`>> 2`)" (`S002:240`); "section `+0x00` low u16 | `0x00264DA4` | … **doubles as the entry count**" (`S003:195`).
- Audit: "`00264D74  movsxd rax, dword ptr [r8]      ; the WHOLE first dword, sign-extended`" (`S002:95`); "**In `section_002` this fires in 213 of 828 sections**" (`S003:92`).
- The two give different counts in 213 of 828 sections ("the guard at `0x00264D81` admits indices **0 … 16,390**", `S002:109-110`).
- **Favoured: the whole dword, by the AUDIT of 2026-09-05** (`S002:90`, `S003:89`). *Page-text only - needs local check.*

**A3. `ActorScriptResource_GetBytecodeOffsetById`: which dword of the 8-byte entry.**
- Listing comment: "`00358A0F  mov    eax, dword ptr [r8 + rax*8 + 8]  ; 8-byte stride, dword at entry+0`" (`S000:390`).
- BW-5: the table is "`{u32 count; {u32 nameOffInPool, u32 offsetWithinScript}[count]}`" (`S000:425`) and the function returns "function `id`'s offset within the script** (the 8-byte entry's second dword)" (`S000:434-435`).
- **Favoured: the second dword, by BW-5 of 2026-09-12** (`S000:409`). *Page-text only - needs local check.*

**A4. Header `+0x6C`: a length-prefixed byte array, or `{u32 count; u32 packedRef}`.**
- "`+0x60` through `+0x74` each point at an array whose **first byte is the element count**, followed by that many bytes." (`S000:133-134`); "`+0x6C` | **`1` in 1114/1114** | a 1-element authored option" (`S000:139`); "`+0x6C`/`+0x70` are likewise fixed at `1`/`5`. A data byte that never varies while its neighbours do is a length." (`S000:595`).
- "`+0x6C  u32  trapRefs     -> {u32 count = 1; u32 packedRef} - the trap table's tag-3 reference, read by 002641B0 (corrected 2026-09-12)`" (`S000:108`); "`+0x6C` is `{u32 1; u32 packedRef}`" (`S000:256`).
- **Favoured: `{u32 count; u32 packedRef}`, by the correction of 2026-09-12** (`S000:108`). Whether `+0x70` (also called a byte-count array of "4-byte offsets", `S000:140`) has the same `u32`-count shape is not settled. *Page-text only - needs local check.*

**A5. `weatherProbability`: per-slot survival chances, or availability flags.**
- "**Most maps are `{100, 0, 0}` — slot 0 always survives the roll, i.e. the weather never changes.** … this is three independent per-slot chances, not a distribution." (`S000:327-331`); README quoting the glossary: "*"authored per-slot chance the current slot survives the transition roll, script header `+0x64`."*" (`README:134-135`); S000 §1 "*the per-slot chance the current weather survives the transition roll*" (`S000:70-71`).
- "**BW-4 answered 2026-09-12 (FABLE): … the three bytes are availability flags to their one consumer, not chances against a roll.** … tests candidates' bytes **`> 0`** and picks the first available; when both alternatives are open the order is a `RNG_MT19937_NextU32 % 100 < 50` coin … and the byte's *value* is never compared to the roll." (`S000:283-292`)
- **Favoured: availability flags, by BW-4 of 2026-09-12**, for the one consumer found; "whether another reader weighs the values is not established" (`S000:294-295`). *Page-text only - needs local check.*

**A6. Section-6 handler: where the base and the pending word live.**
- S000 interior note: "`ecx` splits into base `ecx & ~0xF` (stored at `0233A6F0 + lane*8`) … the `0233AE48 + lane*8` word clears bit `0x40`" (`S000:683`).
- S006: "`00330097  MOV [r15 + rax*8 + 0x21A6CF0],RBX        ; 022C6CF0[mgr] = section`" (`S006:136`); CON: "stores to `DAT_022c6cf0[mgr]`" (`CON:345`); the pending mask is "`022C6E48[mgr] = mask`" (`S014:273`) and "`022C6E48` | — | per-manager flags" (`S012:153`).
- Two pages against one for the store; three against one for the mask array. Not settled on the pages. *Page-text only - needs local check.*

**A7. Section 11 pending bit: `0x400`, cleared by `btr rdi, 0xb`.**
- "pairs the tag with the completion callback `FUN_003316b0` and pending-mask bit **`0x400`**" (`S011:290`); CON gives slot 11 "mask bit 10" (`CON:349`).
- "`0x0033166F` | `btr rdi, 0xb` — clears pending-resource bit `0x400`" (`S011:326`). `btr … 0xb` is bit 11, `0x800`, which S010 gives to section 10: "`0x00331662` — `btr rdi, 0xb`: clear pending-resource bit `0x800`." (`S010:173`).
- Either the instruction or the bit in `S011:326` is wrong. Not settled on the pages. *Page-text only - needs local check.*

**A8. `CML1_ResolveNames` reset: what `+0x18` / `+0x1A` are set to.**
- "five `(u16, u16)` pairs in the manager record are reset to `(0, 0xFFFF)` on every resolve — `+0x18`, `+0x118`, `+0x130`, `+0x148`, `+0x160`." (`S008:230-231`); S010's listing: "`reset five (u16,u16) pairs to (0, 0xFFFF)`" (`S010:241`).
- S008's listing: "`manager[+0x18] = 0xFFFF ; manager[+0x1A] = 0xFFFF`" (`S008:149`); BY-4: "`+0x18` / `+0x1A` are the main and sub frames' owning channel, both set to `0xFFFF`" (`S008:234`).
- **Favoured: `+0x18` and `+0x1A` both `0xFFFF`, by BY-4 of 2026-09-12** (`S008:234`). *Page-text only - needs local check.*

**A9. `SHK1` `+0x04`–`+0x07`: two `u16`, or one count whose upper half is unread.**
- "**`+0x04` and `+0x06` are two 16-bit fields, not one 32-bit count.**" (`S011:92`); "**the two-`u16` split is proven, not inferred**" (`S011:440`).
- §7: "**Whether `recordCount`'s upper 16 bits are meaningful.** The loader reads only the low half. No shipped file has a non-zero upper half" (`S011:482-483`). `+0x06` is `curveCount`, "2 .. 127 observed" (`S011:86`), so it is non-zero in every file.
- **Favoured: two `u16`, by the audit pass of 2026-09-05** (`S011:423`, `S011:439-441`). *Page-text only - needs local check.*

**A10. Does the engine write into the shake chunk (`+0x28`, `+0x62`)?**
- "**CA-1 answered 2026-09-12 (FABLE): the `CML1` chunk is read — through the per-record copy, for kind-3 actors.** … **sets bit 7 of chunk `+0x62`** … reads and **clears chunk `+0x28`**" (`S010:457-463`), unstruck.
- "**RETRACTED 2026-09-12 (FABLE) — the CA-1 answer that follows misread its base.** `[actor + 0xB8]` is the actor record's `contextPtr` … So `00263230` and `002693D0` touch a steering record's `+0x62`, `+0x28` and `+0x65`, not this chunk" (`S010:448-452`).
- **Favoured: no writes into the chunk, by the retraction of 2026-09-12** (`S010:448`). The retracted block is still printed in full below it. *Page-text only - needs local check.*

**A11. Section-12 ids: one `id + 1000` rule, a per-letter rule, or the decoder's block index.**
- "**Column 1 is the model number less 1000**" (`S012:175`), unqualified.
- Per-letter (audit 2026-09-05): `c`/`m`/`n` use `id + 1000`, `b`/`g`/`s`/`t` resolve "directly" (`S012:197-212`); "*"column 1 is the model number less 1000"*, stated without qualification … holds for three letters of eleven" (`S012:392-393`).
- Engine decoder (2026-09-26): "`c` → kind 14, index = id × 25 … `n` → kind 19, index = id × 25" (`S012:335-337`), and "the **lowercase** ids do not follow the decoder's block order … So that reader translates lowercase ids somehow" (`S012:349-351`).
- **Favoured for matching ids to model stems: the per-letter rule, by the audit of 2026-09-05.** How the engine would map a lowercase id is not settled on the pages. *Page-text only - needs local check.*

**A12. Section-19 record field roles.**
- §2: "`+0x02` is the striking one: **three values in 2,116 records.** A field with that distribution is a kind or a version, not a quantity. `+0x08` … reads like an identifier." (`S019:220-222`).
- CC-10: "`{u32 modelKey (a letter — the three values of `+0x02` are `m` / `n` / `s` — over a model number); u16 class; u16 groupId; u16 motionIndex}`" (`S019:468-469`).
- **Favoured: CC-10, dated 2026-09-12** (`S019:466`). *Page-text only - needs local check.*

**A13. Section-19 header: how many fields any code reads.**
- "**So four of the eight constant header fields are now proven inert and one is proven live.**" (`S019:327`).
- BZ-2: "**`+0x0C` is read** … so **`+0x2C` (the handler) and `+0x0C` (the trailer reader) are the only header fields any code reads**" (`S019:274-278`); field table "`+0x0C` `offsetB` | `003EA650(1)` … | **NO — read (BZ-2, 2026-09-12)**" (`S019:264`).
- **Favoured: two fields read (`+0x0C`, `+0x2C`), by BZ-2 of 2026-09-12.** *Page-text only - needs local check.*

**A14. Container directory slot width.**
- README plan: "`EBP2` magic at `+0x00`, a version/count `0x14` at `+0x04`, and an offset table in 8-byte slots." (`README:101-102`).
- "`+0x10  u32[20]  sectionOff`" (`CON:80`); "**"An offset table in 8-byte slots"** appeared in an early plan for this category. The directory is **`u32[20]`, 4-byte slots**." (`CON:655-656`); README's own census: "`+0x10  u32[20]   section offsets`" (`README:181`).
- **Favoured: `u32[20]`, by the 2026-09-03 census** (`README:171`, `README:181`; `CON:655-656`). *Page-text only - needs local check.*

**A15. Do `REQALL` / `REQIALL` carry a channel?**
- "`PREQ*`/`REQWAIT`/`REQCHG`/`REQCANCEL`/`REQALL`/`REQIALL` consume built entries and carry no new channel." (`S000:497-498`), unstruck; the member TSV classifies every `REQALL` / `REQIALL` row as `channel_class n/a` (B5).
- "***Corrected 2026-09-24 (FABLE, Claude Opus 5.5) for `REQALL`/`REQIALL`:*** each pops **one channel**" (`S000:498-499`); the opcode table "`0x5F REQALL` | pops the **channel**" (`S000:543`).
- **Favoured: they pop a channel, by the correction of 2026-09-24.** *Page-text only - needs local check.*

**A16. CAM7 record `+0x20`: inert, or read.**
- Falsification row: "Could the `0x8000` at record `+0x20` be read somewhere the census missed? | **Not resolved by search alone, and it is not claimed.** … Listed inert **with that method named**, not asserted unused." (`S009:294`).
- "rec `+0x20`, `+0x22` | **`002572E0`** at manager runtime init … | **no — the attachment word.** *Corrected 2026-09-12*" (`S009:169`); fence "`+0x20  u32  attachWord  eye/target attachment bitfield, decoded by 002572E0`" (`S009:96`).
- **Favoured: read, by the correction of 2026-09-12.** *Page-text only - needs local check.*

#### B. Counts, sizes and addresses that disagree but change no ported behaviour

**B1. How often `0x003304A0` reads `+0x04`.** "`0x003304A0` at 15 sites" (`CON:253`); "all 15 `cmp dword ptr [rdi+4], N` sites" (`CON:321`); "15 sites → 14 distinct slots" (`CON:578`) — against "a field the function reads fourteen times" (`CON:295`) and "compared against **fourteen different constants**" (`CON:576`). Fifteen sites, fourteen distinct constants is consistent; "reads fourteen times" is not. Not settled on the pages.

**B2. Listing order in the ns-37 probe.** "`0032FDD9  mov  r12d, eax`" is printed before "`0032FDD4  mov  ecx, 0x25`" (`CON:167-168`). The addresses are out of order in the listing. Not settled on the pages.

**B3. Weather triples.** "775 of the 1,114 scripts spell it `{100, 0, 0}`" (`S000:72`); the triple table (`S000:316-325`) sums to 1,087 of 1,114. The table does not say it is partial. Not settled on the pages.

**B4. The msp region (class / tag 3): used or not.** "`+0x40` (`image + tableOff40`, class 3, no shipped script uses it)" (`S000:361`) — against "`+0x6C … {u32 count = 1; u32 packedRef} - the trap table's tag-3 reference`" (`S000:108`), whose count is 1 in "1114/1114" (`S000:139`), and "`+0x3C  u32  mspSize … 0 in 352 files`" (`S000:95`). The base chooser is "the same table as the variable classes" (`S000:254-255`). Whether "no shipped script uses it" means variable descriptors only is not settled on the pages.

**B5. Member TSV against the REQALL correction.** `req-channel-census.tsv` classifies all 47,812 `REQALL` and 3,699 `REQIALL` rows as `channel_class n/a` (member file); S000's correction says each "pops **one channel** … an immediate between 0 and 7 at all 51,511 shipped sites" (`S000:499-500`). **Favoured: the correction of 2026-09-24**; the TSV predates it.

**B6. Section-6 dimension table.** Headed "The dimensions, all 67" (`S006:104`), its rows sum to 64 (`S006:108-115`). Not settled on the pages.

**B7. Section-6 24 × 23 count.** "55 of the 67 are the same tiny 24×23" (`S006:35-36`) and "**24 × 23** | **55**" (`S006:108`) — against "57 of 67 are exactly 448 B" (`S006:45`), "the 57 single-picture 448 B files" (`S006:96`), and "55–57 files carry one **24 × 23** picture (448 B)" (`S006:232`). Not settled on the pages.

**B8. Section-6 non-24 × 23 shapes in `us`.** §2: `640 × 23` ×3, `40 × 23`, `80 × 21`, `576 × 21`, `616 × 16`, `200 × 16`, `640 × 46` (`S006:109-115`). Cross-tree note: "In every Latin-script tree the population is the same: … three carry a two-picture **640 × 23**, one a 64 × 23, one an 8 × 22, one a 40 × 14 and one two-picture 640 × 46" (`S006:232-234`). `us` is a Latin-script tree (`S006:230`). Not settled on the pages.

**B9. Section-6 multi-picture count.** "**10 files carry `pictureCount == 2`**" (`S006:296`; also `S006:70`) — against four two-picture files in the Latin-tree list (`S006:233-234`). Not settled on the pages.

**B10. CAM7 record lengths.** "Record length takes 11 distinct values." (`S009:259`) — against "The distribution came back with **twelve** distinct lengths, not eleven" (`S009:358`) and the inline fix "*(The 152 was missing from this list until 2026-09-13 …)*" (`S009:115`). **Favoured: twelve, by the pass of 2026-09-13.**

**B11. Callers of `CAM7_Load`.** "the one caller reads `param & 0xF`" (`S009:218-219`) — against "`002561C0` is called by `0032FAC0`; `002561C0` is called by `003306E0`" (`S009:405`; also `S008:422`). The second is the dead ATEL route (`S009:152-156`). Not settled on the pages.

**B12. Teardown function address.** "`ActorResource_ResetManagerLoadState` (`0x0032ED80`)" (`S008:240`, `S009:241`) — against "Teardown is `FUN_0032ED70`" (`S010:181`, `S011:293`) and "`0x0032ED70` | teardown — unbind, free, null" (`S011:328`). Not settled on the pages.

**B13. One free site for two blobs.** S008: "loads the blob at `0x0032EFD3`, frees it at `0x0032EFBD`, and clears the slot at `0x0032F00C`" (`S008:240-241`); S009: "frees the blob at `0x0032EFBD`, clears the slot at `0x0032EFC4`" (`S009:241`). Two different blobs, one free address, and S008's load is after its free. Not settled on the pages.

**B14. Section-12 frequency.** "in every third map file" (`S012:33`) — against "**842 (75.6 %)**" (`S012:39`). README gives "842 (75.5 %)" (`README:48`; 842 / 1,115 against 842 / 1,114). Not settled on the pages.

**B15. High-detail model pool sizes.** "each id set is larger than its candidate pool (40 ids against 17 `hc` stems)" (`S012:217-218`) — against "48 `hc*.cm`, 87 `hn*.cm` and 5 `hs*.cm`" and "Every `C` id (0–46) is below 48" (`S012:339-342`). **Favoured: 48, by UQ-333 of 2026-09-26** (`S012:331`); the 17 counted `obj_finish` stems, not the decoder's table.

**B16. Pair without section 14.** "every file that has `014` has both, while 423 files have the pair without `014`." (`S014:47-48`) — against 423 files with the pair in total (`S008:42-43`) and 140 with `014` (`S014:43-44`), which leaves 283. Not settled on the pages.

**B17. Standalone `.ard` count.** "the same format also ships as 332 standalone `.ard` files" (`S019:36-37`; `S019:390`) — against "`repos-d6` measured 166 areas" (`S019:155-156`), "`.ard`, **166/166**" (`S019:169`) and "my own parse of the 166 standalone .ard files" (`S019:25`). Not settled on the pages.

**B18. Legacy-path probes.** "the four directories it builds (`entry`, `icon`, `treasure`, and the `.ard` sibling) occur **0, 0, 0** times respectively" (`S004:338-339`) — four names, three figures; the probe table measures `.icn`, `/icon/`, `.eps` and `/entry/` and has no `treasure` row (`S004:259-265`). Not settled on the pages.

#### C. Stale "open / not read" claims, banners and names

**C1. README: the container sheet "not written".** "**§3, the loader contract, is still empty**" and "**The sheet is deliberately not written yet.**" (`README:262-266`) — against `Container/ebp2-container.md`, `status: AUDITED` (`CON:4`) with a full §3 (`CON:105-432`). **Favoured: CON** (falsification pass 2026-09-03, `CON:567`).

**C2. README: whether the magic is checked.** "**Two readings, and this does not choose between them** … **Settling it needs the loader body read in Ghidra.** Until then the sheet may not claim either." (`README:230-239`) — against "**So the first reading is the correct one, and the second should not be carried forward.**" (`CON:299`). **Favoured: CON, 2026-09-03.**

**C3. README: seven units "*unknown*".** `section_004`, `008`, `009`, `010`, `011`, `014`, `019` are "*unknown*" (`README:42-51`), and "**Seven of the fourteen units have no tool-side lead at all.**" (`README:67`) — against the AUDITED sheets: `NAVIICN2` (`S004:2`), `CML1` (`S008:2`, `S010:2`), `CAM7` (`S009:2`), `SHK1` (`S011:2`), `LGT2` (`S014:2`), `FF12AR03` (`S019:2`). **Favoured: the section sheets.**

**C4. README: section 6 is "pre-rendered text lines".** "23-pixel-high strips of varying width — pre-rendered text lines (section-006 §5)" (`README:43`) — against "**Correction/refinement 2026-09-24 (SWE2-DATA) — the `in` strips are per-event expansion-glyph sheets, not captions.**" (`S006:247-248`) and "The earlier "a line of text rendered to a texture" reading is superseded for the `in`/`ch`/`cn`/`kr` populations" (`S006:272-273`). **Favoured: S006, 2026-09-24.**

**C5. README: `+0x04` as a version.** "a version/count `0x14` at `+0x04`" (`README:101`) — against "`+0x04` is therefore **not a version stamp**." (`CON:327`) and the 2026-09-03 falsification row (`CON:576`). **Favoured: CON.**

**C6. CON: slot 17 still an open question.** "Open question `PROPOSED-repos-1e-1`." (`CON:391`); "**Not yet attacked:** whether another language's archive populates slot 17" (`CON:583`) — against "**BW-1 answered 2026-09-12 (FABLE): the always-zero slots are zero in every language tree.**" (`CON:91`). **Partly settled:** BW-1 covers nine trees; `CON:584` asks for `jp`/`eu`, which BW-1 does not list (`CON:93-94`).

**C7. CON: manager 0's slot-14 skip "open".** "**Slot 14's manager-0 exclusion is described, not explained.** What distinguishes manager 0 is open." (`CON:642-643`) — against "*Answered 2026-09-14 (FABLE, `BW-3`): **manager 0's lighting comes from the map-control pack, not from EBP.**" (`CON:397`). **Favoured: BW-3, 2026-09-14.**

**C8. CON: `FUN_0036c660` "not read".** "It does **not** claim the allocator guarantees a low arena — `FUN_0036c660` was not read." (`CON:598-599`); "Open question `PROPOSED-repos-1e-2`." (`CON:421-422`) — against "**CORRECTED 2026-09-12** … `FUN_0036C660(p, name, tag)` is a **header tagger**" (`CON:607-610`). **Favoured: the correction of 2026-09-12.**

**C9. CON: binders "not read".** "`0x003DFE60` | shared binder for slot 16 (selector 0) and slot 17 (selector 1) | not read" (`CON:449`); "**The binders.** `FUN_003dfe60`, … `FUN_0026c8xx`, `FUN_0026ceXX` and `FUN_0026d3xx` … **Their bodies were not read**" (`CON:591-593`) — against "`0x003DFE60` | `FUN_003dfe60` — `g_fieldRoots[class] = ptr`; the store is `0x003DFE6A` | ✅" (`S016:219`), "`0x0026C880` | binder — writes `ctx+0xA0` | ✅ 1 instruction" (`S002:281`), "`0x0026CE00` | binder … | ✅ full body" (`S008:253`), "`0026CE40` | … | ✅ complete 21-byte body *(audit 2026-09-05)*" (`S012:144`), and "`0x0026D3A0` | stores the **second copy** … | ✅ full body, 5 instructions" (`S010:288`). **Favoured: the section sheets** (S012's audit is dated 2026-09-05).

**C10. S000: the weather reader "not found".** "the *reader* was not found — see §7" (`S000:596`); "**Who reads `weatherProbability` was not found.** … `PROPOSED-repos-1e-4`." (`S000:610-614`) — against "**BW-4 answered 2026-09-12 (FABLE): the reading instruction is `002658EB`**" (`S000:283`). **Favoured: BW-4, 2026-09-12.**

**C11. S002: `0xA5` / `0xA3` "unresolved".** "**The full character table.** `0xA5` … and `0xA3` are unresolved. No glyph table was located" (`S002:376-377`) — against "**BX-2 ANSWERED 2026-09-15 (OPUS) — both are the hyphen** … Carried to `section_002`'s 4,262 occurrences by the shared table" (`S003:315-330`). **Favoured: BX-2, 2026-09-15.**

**C12. S002: the renderer "not read".** "Their semantics belong to the text renderer (`FUN_00269F20`, `FUN_002E16B0`), which this document did not read." (`S002:354-355`) — against BX-1's reading of `mes` and the window paths: "**only when the flag is 0 opens the window itself** (`002E16B0`, `00348EFF`)" (`S002:366-367`). **Partly settled by BX-1, 2026-09-12**: the escape semantics remain open.

**C13. Front matter `last_reviewed` older than the body.** `last_reviewed: 2026-09-03` on S002 (`S002:19`), S003 (`S003:19`), S004 (`S004:19`), S006 (`S006:19`), S012 (`S012:19`) and S016 (`S016:19`), while their bodies carry dated changes to 2026-09-12 (`S002:360`), 2026-09-15 (`S003:315`), 2026-09-04 (`S004:134`), 2026-09-28 (`S006:319`), 2026-09-27 (`S012:323`) and 2026-09-12 (`S016:316`). Banner only.

**C14. S004 §7 against its own §3 and front matter.** "**No loader contract.** Section 3 has no `Read by` entry that is a real instruction address. That is the main gap in this sheet and the reason its status is `PARTIAL`, not `DOCUMENTED`." and "**no field below is marked `Inert`**" (`S004:344-348`) — against `status: AUDITED` (`S004:4`), "the section pointer | `003DFDC0`" (`S004:163`), the four "**YES — never read**" rows (`S004:159-162`), and "**Established 2026-09-04.**" (`S004:134`). **Favoured: §3, 2026-09-04.**

**C15. S019 §7 and §3 against its own corrections.**
- "**No loader contract.** No `Read by` cell in section 3 holds a real instruction address, which is why the status is `PARTIAL`. **No field is marked `Inert`**" (`S019:460-462`) — against `status: AUDITED` (`S019:4`), "`003EAA32` `MOV ECX,[RBX+0x2C]`, twice" (`S019:267`) and the "**YES — never read**" rows (`S019:262-269`), "**Established 2026-09-04.**" (`S019:232`).
- "**The eight constant `u32` in the header are not explained**" (`S019:474`) — against "**`BZ-2` closes**: the eight fields are directory slots" (`S019:179`) and BZ-2 of 2026-09-12 (`S019:271-282`).
- "The agreement is structural — same directory, same size, same absent slots" (`S019:183-184`) — against "**CORRECTED 2026-09-05 by the audit — the two absences are not the same**" (`S019:162`).
- "`003320D0` | the `.ard` stream-completion callback … | ❌ not read" (`S019:413`) — against "`FUN_003320D0  (13 bytes)`" read in §3 (`S019:242-244`).
- "the `.ard` files were not extracted from the archive for this block" (`S019:396`) — against "from my own parse of the 166 extracted files" (`S019:177`).
- **Favoured: the dated §2/§3 corrections (2026-09-04, 2026-09-05, 2026-09-12).**

**C16. S006 "not read" and "open" rows against its §3 and §5.**
- "`0037F1F0`, `003BC4E0`, `00575710`, `0029CAC0` | the four callers | ❌ not read" (`S006:224`) — against the `0029CAC0` listing (`S006:144-148`) and "`003BC4E0` (1,163 B) — one of `0039BEC0`'s four callers, previously unread — is an **event dispatcher**" (`S006:367-368`).
- Falsification: "**none of its four callers is in the `atelload.c` unit**. Left open rather than asserted." (`S006:308`) and "The attempt failed to confirm the link" (`S006:313-314`) — against "**Complete as of 2026-09-04. The connection to `section_006` is made**" (`S006:122-123`).
- "**The palette source is unknown.**" (`S006:331`) — against "The external-palette invariant (§2) now has its explanation: the text renderer supplies colours" (`S006:274-275`, 2026-09-25).
- **Favoured: §3 (2026-09-04) and §5 (2026-09-25).**

**C17. S008: section 10 has no sheet, and the subset is unexplained.** "`section_010` — … `repos-c7`'s unit; the sheet does not exist yet, so this is deliberately not a link." (`S008:363-365`); "**`section_010`'s subset relationship is stated, not explained.**" (`S008:357`) — against `Sections/section-010.md` (AUDITED, `S010:4`) and "*That co-occurrence is not engine-enforced (BY-5, answered 2026-09-26 …)*" (`S008:58`). **Favoured: BY-5, 2026-09-26.**

**C18. S009: `subCount` at record `+0x28`.** "**`subCount` at record `+0x28` is 1 in 3,941 of 3,942 records.**" (`S009:275`); "the one `subCount == 2` record" (`S009:310`) — against the fence "`+0x28  u8  firstCommand  type byte of the command stream`" (`S009:99`) and "`+0x28` is the first command's type: `1` = key." (`S009:279`). **Favoured: `firstCommand`, 2026-09-12.**

**C19. `BY-4` names two different questions.** In S008 and S009 it is the four camera channels: "*(Established 2026-09-12, `BY-4`: `+0x110 + 0x18·ch` are the four **camera channels**" (`S008:234`), "**Explained 2026-09-12 (`BY-4` answered): four camera channels**" (`S009:316`). In S009's pass 2 it is census reproducibility: "### `BY-4` is closed … I raised `BY-4` on 2026-09-12: `census.py`'s output was not byte-reproducible" (`S009:377-379`). Not settled on the pages.

**C20. S010: `PROPOSED-repos-c7-1` both open and closed; a missing §3b.** "That residue is open question **PROPOSED-repos-c7-1**." (`S010:213`); "Recorded as PROPOSED-repos-c7-1 rather than written up as an inert section." (`S010:356`) — against "**PROPOSED-repos-c7-1 is CLOSED** by `repos-4b`'s pass." (`S010:474`). The field table cites "the searches in §3b" (`S010:152`); the page has no §3b. **Favoured: closed, 2026-09-05** (`S010:471`).

**C21. S011: `dataOffset` still called 32-bit.** "read 16-bit only — the high half of the u32 is discarded" (`S011:247`); "Declared `u32` at `+0x08` in §2.1" (`S011:272`); "**16-bit read of the 32-bit `+0x08`**" (`S011:320`) — against the fence "`+0x08  u16  dataOffset`" and "`+0x0A  u16  _unread`" (`S011:87-88`), "**Audit note, 2026-09-05 (`repos-4b`): `dataOffset` is read 16-bit, so the fence says `u16`.**" (`S011:101`). **Favoured: `u16`, 2026-09-05.**

**C22. S011: "seven of the nine" key floats unnamed.** "**Seven of the nine are named `_unnamedN` on purpose.**" (`S011:200`) — against the fence, which names six of nine (`startFrame`, `coefA`–`coefD`, `weight`) and leaves three `_unnamed` (`S011:189-197`), and "**Four of the other seven are identified by the evaluator; three are never read (2026-09-26 …)**" (`S011:214`). **Favoured: the fence, 2026-09-26.**

**C23. S011: duplicated heading.** "## 6. Falsification pass — 2026-09-03" twice (`S011:370-371`). Banner only.

**C24. S012: consumer search target, and the id list "not stored".**
- "**Consequence for §7:** the consumer to look for reads **`managerRecord[+0x100]`**" (`S012:116`); "**The consumer is not in this function and this document does not claim to have found it.**" (`S012:124`) — against "**ANSWERED 2026-09-27 (FABLE, Claude Opus 5.5), static: nothing in this executable walks it.**" (`S012:323`).
- "**That needs the id list, and the database does not store one** … no `members/` file on this page carries them." (`S012:299-301`); "**Not closed** — that is sufficiency, not proof, and the id list needed to finish it is not stored anywhere." (`S012:373-374`) — against "`members/section012_model_ids.py` writes it to `members/section012-model-ids.tsv`" (`S012:416-417`) and "**ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5): both, and the split is measured.**" (`S012:364`).
- "mapping the uppercase letter to the `h`-prefixed family gives 13 of 40, 13 of 66 and 1 of 5 — **better than zero and not a finding**" (`S012:216-217`) — against "**ANSWERED (FABLE, Claude Opus 5.5, 2026-09-26), static: they are the high-detail model tables, `hc`, `hn` and `hs`.**" (`S012:331`).
- **Favoured: the answers of 2026-09-25 to 2026-09-27.**

**C25. `0032F1B0` named "teardown".** "`0032F1B0` | teardown path when the flags word goes to zero | ❌" (`S012:146`) — against "`0032F1B0` | `ActorResource_FinalizeManagerRuntimeAfterLoads` — calls the binder" (`S014:224`) and "`ActorResource_FinalizeManagerRuntimeAfterLoads` (`0032F1B0`) binds it through `0037AA90(block, slot)` once the slot's loads finish" (`CON:398-399`). Not settled by a dated correction; two pages against one.

**C26. S014: `003775D0` "not read".** "`003775D0` | `FUN_003775d0` — the second binder caller (site `003776A6`) | ❌ not read" (`S014:235`); "`FUN_003775d0`'s call at `003776A6` — **not read.**" (`S014:465`) — against "**CD-1 answered 2026-09-12 (FABLE): the branch is live, on the lighting-set route.** `003775D0` is read" (`S014:443-444`). The CD-1 block's "entered through a relative dispatch table whose entries at `01D7BC70` / `01D7BCA4` carry its RVA" (`S014:450-451`) is corrected in the next paragraph: "begin/end/unwind triples … exception metadata, not callers" (`S014:460-461`). **Favoured: CD-1 and its residue answer, 2026-09-12.**

**C27. S016: `type == 2` "too rare".** "a third shape, too rare to characterise" (`S016:124`); "**`type == 2`.** Nineteen records in 25,687. Too few to characterise honestly." (`S016:344`) — against CC-3: "**2** draws `u` the same way and bounds `v` by the ellipse `sqrt(B² − u²·B²/A²)`" (`S016:339`). **Favoured: CC-3, 2026-09-12** (`S016:333`).

**C28. Evidence tier 9 on instruction-level sheets.** S002 and S003 carry `evidence_tier: 9` (`S002:6`, `S003:6`) while every loader claim in them cites instructions read "from raw instruction bytes via capstone against the authorized EXE" (`S003:303`) and their siblings carry tier 1. Banner only; not settled on the pages.
