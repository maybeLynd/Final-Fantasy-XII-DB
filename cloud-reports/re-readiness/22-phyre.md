# Reconstruction readiness — `FFXII TZA/22-Middleware-PhyreEngine/`

| | |
|---|---|
| Stream | R (reconstruction readiness), per [`docs/cloud-briefs/re-readiness.md`](../../docs/cloud-briefs/re-readiness.md) |
| Board task | `OPUS-CLOUD-R-READINESS-22-1002` |
| Date | 2026-10-02 |
| Snapshot | this repo's text snapshot only (`86b70c69`); no executable, Ghidra or live game was used |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every item is a quotation or a paraphrase of a page, with its location. Several pages in this folder are being edited by other lanes; every quotation is of the snapshot text. |

**Counts:** _filled in when the report is complete (see the end of the commit history)._

Citation form: `path:line`, where `path` is relative to `FFXII TZA/22-Middleware-PhyreEngine/`. To keep the tables
readable, the long page paths are abbreviated as follows (the abbreviation is always followed by `:line`):

| abbrev. | page | lines |
|---|---|---:|
| `README` | `README.md` | 82 |
| `CAM` | `the-camera-state-snapshot.md` | 228 |
| `MAP` | `Subsystem-Map/phyre-subsystem-map.md` | 425 |
| `MOD` | `Subsystem-Map/the-fifteen-modules-registered-before-main.md` | 598 |
| `APP` | `Application-Framework-Boundary/the-game-is-a-phyre-application.md` | 1,070 |
| `PAC` | `Phyre-Asset-Container/README.md` | 48 |
| `HDR` | `Phyre-Asset-Container/the-cluster-header-and-what-the-loader-rejects.md` | 749 |
| `C-HDR` | `Phyre-Asset-Container/CONTRACT-phyre-cluster-header.md` | 955 |
| `NS` | `Phyre-Asset-Container/the-packed-namespace-and-the-file-side-schema.md` | 644 |
| `C-NS` | `Phyre-Asset-Container/CONTRACT-phyre-packed-namespace.md` | 506 |
| `CDMS` | `Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md` | 1,978 |
| `C-CD` | `Reflection-And-Class-Metadata/CONTRACT-phyre-class-descriptor.md` | 917 |
| `MR` | `Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md` | 2,402 |
| `AR` | `Reflection-And-Class-Metadata/how-a-class-registers-its-array-members-and-annotations.md` | 445 |
| `IS` | `Reflection-And-Class-Metadata/phyre-class-instance-sizes-and-alignments.md` | 220 |
| `FS` | `Reflection-And-Class-Metadata/the-file-schema-against-the-runtime-schema.md` | 495 |
| `LUA` | `Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md` | 1,259 |
| `ACC` | `Script-Object-Accessors/phyre-script-object-accessors.md` | 953 |
| `PPF` | `Post-Process-Chain/the-post-process-passes-and-their-shader-constants.md` | 1,715 |
| `PFX` | `Post-Process-Chain/the-phyre-post-effect-class-family.md` | 884 |
| `CTX` | `Shader-Variant-Selection/the-context-switch-axes-and-the-variant-key.md` | 985 |
| `FRM` | `The-Frame/what-happens-between-two-frames.md` | 1,547 |
| `ANI` | `Animation-Channel-Binding/animation-channel-binding-and-transform-composition.md` | 1,122 |

"Not stated" means none of the 23 pages says it. Where another category's page is the only place a point is made,
the pointer is given as a path from `FFXII TZA/`, but that page was not audited for this report.

## Pages read

All 23 `.md` files were read in full (20,227 lines). Member `.tsv` files were opened only to confirm layouts and row
counts; no item below rests on a `.tsv` alone, and where a `.tsv` disagrees with its page that is reported as a
contradiction, not resolved.

| page | front matter as the page states it | in-body / index banner that differs |
|---|---|---|
| `README` | none; "Functions \| 6,768" (`README:8`) | indexes 8 of the 22 pages only (`README:13-63`) |
| `CAM` | `status: DOCUMENTED — its one register row, SD-60, is ANSWERED …` (`CAM:4`); `evidence_tier: 1` (`:6`); `last_reviewed: 2026-09-03` (`:19`) | body dated to 2026-09-30 (`CAM:104`, `:186`) |
| `MAP` | `status: DOCUMENTED — how the 6,769 Phyre functions map onto the classes (AQ-2) is SUPERSEDED 2026-09-26 …` (`MAP:4`); `evidence_tier: 4` (`:6`); `last_reviewed: 2026-09-02` (`:19`) | "**PARTIAL, and tier 4 by construction.**" (`MAP:41`) |
| `MOD` | `status: AUDITED` (`MOD:4`); `evidence_tier: 1` (`:6`); `last_reviewed: 2026-09-08` (`:19`) | not indexed in `README` |
| `APP` | `status: AUDITED` (`APP:4`); `evidence_tier: 1` (`:6`); `last_reviewed: 2026-09-02` (`:18`) | `README:25` "**DOCUMENTED, tier 1, one falsification pass.**" |
| `PAC` | none | "corrected 2026-09-03" heading (`PAC:27`) |
| `HDR` | `status: AUDITED` (`HDR:4`); `evidence_tier: 1` (`:6`); `last_reviewed: 2026-09-07` (`:20`); `corpus_validated: "169 / 169 extracted .phyre files — 0.47 % of the 35,984 shipped"` (`:19`) | body covers all 35,984 files from 2026-09-12 (`HDR:227-234`) |
| `C-HDR` | `readiness: CONTRACT READY` (`C-HDR:6`); `confidence: PROVEN` (`:7`); `last_reviewed: 2026-09-12` (`:18`) | "This is the first contract in `22-Middleware-PhyreEngine`" (`C-HDR:32`) |
| `NS` | `status: AUDITED` (`NS:4`); `evidence_tier: 1` (`:6`); `last_reviewed: 2026-09-07` (`:20`) | body dated to 2026-09-30 (`NS:275`) |
| `C-NS` | `readiness: CONTRACT READY` (`C-NS:6`); `confidence: PROVEN` (`:7`); `last_reviewed: 2026-09-12` (`:17`) | — |
| `CDMS` | `status: AUDITED` (`CDMS:4`); `evidence_tier: 1` (`:6`); `last_reviewed: 2026-09-13` (`:18`) | `README:21` "**DOCUMENTED, tier 1.**" |
| `C-CD` | `readiness: CONTRACT READY` (`C-CD:6`); `confidence: PROVEN` (`:7`); `last_reviewed: 2026-09-12` (`:17`) | "Status `FAIL_INCOMPLETE`" mutation campaign (`C-CD:329-330`) |
| `MR` | `status: AUDITED` (`MR:4`); `evidence_tier: 1` (`:6`); `last_reviewed: 2026-09-02` (`:18`) | `README:33` "**DOCUMENTED, tier 1, one falsification pass.**"; body dated to 2026-09-28 |
| `AR` | `status: AUDITED — SD-61, SD-62, SD-63 and UQ-281 are ANSWERED and every box on the page is closed …` (`AR:4`); `readiness: SIGNATURE RESOLVED` (`:8`); `confidence: PROVEN` (`:9`); `last_reviewed: 2026-09-08` (`:17`) | an un-boxed open bullet remains (`AR:181`) |
| `IS` | `status: DOCUMENTED` (`IS:4`); `evidence_tier: 1` (`:6`); `last_reviewed: 2026-09-19` (`:18`) | — |
| `FS` | `status: AUDITED - was REOPENED; …` (`FS:4`); `evidence_tier: 3` (`:6`); `last_reviewed: 2026-09-05` (`:20`) | "**Evidence tier 9, deliberately.**" (`FS:39`); "**REOPENED 2026-09-07.**" (`FS:122`) |
| `LUA` | `status: DOCUMENTED` (`LUA:4`); `evidence_tier: 1` (`:6`); `last_reviewed: 2026-09-02` (`:18`) | body dated to 2026-09-25 (`LUA:937`) |
| `ACC` | `status: AUDITED` (`ACC:4`); `evidence_tier: 2` (`:6`); `last_reviewed: 2026-09-13` (`:18`) | `README:46` "**DOCUMENTED, tier 2.**" |
| `PPF` | `status: AUDITED` (`PPF:4`); `evidence_tier: 1` (`:6`); `last_reviewed: 2026-09-13` (`:12`) | not indexed in `README` |
| `PFX` | `status: DOCUMENTED` (`PFX:4`); `evidence_tier: 2` (`:6`); `last_reviewed: 2026-09-29` (`:15`) | `README:59` "tier 2 for the names and tier 1 for everything else" |
| `CTX` | `status: DOCUMENTED` (`CTX:4`); `evidence_tier: 1` (`:6`); `last_reviewed: 2026-09-30` (`:15`) | — |
| `FRM` | `status: AUDITED` (`FRM:4`); `evidence_tier: 1` (`:6`); `last_reviewed: 2026-09-07` (`:18`) | `README:14` "**DOCUMENTED, tier 1, crossref-clean.**" |
| `ANI` | `status: DOCUMENTED — every register row is closed (owner re-status 2026-09-30, OPUS) …` (`ANI:4`); `evidence_tier: 2` (`:6`); `last_reviewed: 2026-09-30` (`:18`) | not indexed in `README` |

Member `.tsv` files checked for layout and count only (results are used in §3 where they disagree with a page):
`Subsystem-Map/members/phyre-function-class-map.tsv` (6,769 rows), `members/phyre-*.tsv` (17 module files),
`Phyre-Asset-Container/members/user-fixup-census.tsv` (239 rows, files sum 35,984),
`Reflection-And-Class-Metadata/phyre-field-schema.tsv` (686 data rows, 246 `class`, 182 `class_leaf`),
`Reflection-And-Class-Metadata/members/phyre-class-instance-sizes.tsv` (177 rows), the 23 family `.tsv` files in
`Reflection-And-Class-Metadata/members/`, the 24 in `Script-Object-Accessors/members/`, and the four in
`Post-Process-Chain/members/`.

---
## 1. Interface

The category is not one system but eight that share a reflection core. A re-implementer meets them in this order:
**application boundary and frame** (who calls whom each frame), **module registry** (what runs before `main`),
**asset container** (how a `.phyre` file is accepted and decoded), **reflection** (class descriptors and member
records that the loader, the animation binder and the script bridge all consume), **script bridge** (Lua 5.2.1 and
the object accessors), **animation channel binding**, **post-process and shader-variant selection**, and the
**camera snapshot** render command. Each subsection gives entry points, inputs and outputs, state, order and
dependencies as the pages state them.

### 1.1 Application boundary and the frame

The framing claim: "FFXII does not *use* PhyreEngine, it **is** a PhyreEngine application" (`README:25-26`).
`GameApplication` derives from `Phyre::PFramework::PApplication`; "the control flow runs the other way" (`README:29-30`).

#### Entry points

| entry | callers | what it does | cite |
|---|---|---|---|
| `GameApplication` vtable `008C5760` (31 slots); `PApplication` vtable `01CB2508` (31 slots) | the framework | 18 slots overridden, 13 inherited; full slot map | `APP:62-74`, `APP:239-270` |
| `WinMain` `007A3770` → start-up `007980A0` (2,153 B) | PE entry → CRT main → 45-byte wrapper | 11 start-up steps: slot 1 at step 8, module-init walker at step 10, message loop at step 11 | `APP:488-511`; `MOD:443-446` |
| run loop `00796490` → inherited slot 28 `0079C140` | framework | per-frame update: resize-refresh, quit check, slot 9 (first frame), slot 30, device poll, slot 7 (input), slot 4 (animate/tick), slot 9 again, each viewport's render, slot 8 (render) | `APP:431-437` |
| slot 4 `0017CCD0` (237 B) | `PApplication` (slot 28 path) | "the Phyre frame tick the game overrides" | `FRM:78-85`, `FRM:463` |
| `0017D6E0` (404 B) | slot 4 only | tick → frame adapter; "sole caller of the frame entry"; tick returns only 0 or 9 | `FRM:464`; `APP:136-137`, `APP:406` |
| `0022A490` (30 B) | `0017D6E0` | stores its 2nd argument to `02064AA0`, calls the dispatcher, bumps `02064AD0` on non-zero | `FRM:87-90` |
| `0022A580` (465 B) | `0022A490` only | `switch` on mode byte `02064AD3` into seven mode bodies | `FRM:466`, `FRM:120-128` |
| mode bodies `0022B6E0`, `0022B7E0`, `0022A770` (field/battle, 2,001 B), `0022B8C0` (full menu), `0022AF50` (screen capture), `0022BC20`, `0022B000` | `0022A580` | per-mode work, with the engine's own section labels (`PAD CONTROL`, `DRAW`, `FAST MODE`, …) | `FRM:120-128` |
| `MainLoop_Draw` `0022B0B0` (1,583 B) | `0022A82D`, `0022AF8A` (arg 0), `0022A8B8` (arg 1) | the draw; post-processing at most once per draw | `FRM:474`, `FRM:690`, `FRM:380-406` |
| `0036D400` (979 B) | the draw | GS register batch (seven register writes with formulas) | `FRM:486`, `FRM:619-636` |
| graphics handshake `0036F2F0` wait, `0036F2C0` settle-read-clear, `0036F360` publish | every mode / end of frame | | `FRM:475-477`, `FRM:734-751` |
| command buffer `003A1DB0` flip, `003A1D50` init, `003A1E10` reconfigure, `003A2090` begin subpacket, `003A2020` finalise subpacket | the draw path | | `FRM:478-484` |
| pass-gate accessors bits 0-8 (`00358380` … `003583D0`), whole mask `00358330`, aux `00358340` | the draw | nine-bit render-pass enable mask | `FRM:495-505` |
| `EffectSystem_ProcessQueuedGraphicsEffectsForPass` `00375500` (374 B) | the draw | 13-kind queued-effect dispatch | `FRM:408-433` |
| mode setter `00229F00` / getter `00229EA0` | `002E09A0` (sets 4), `002E2240(flag)` (sets 6 or 2) | | `FRM:141-146` |
| nine draw-mask setters (`00358510`, `0024C7C0`, `0024CBE0`, `002F1A90`, `002F1950`, `003AB500`, `003AAA50`, `0035B7D0`, `0035B8D0`) | 105 sites in 17 functions | write the pass-enable table | `FRM:690`, `FRM:692` |

Overridden slot behaviours (PA-1 table, `APP:389-398`): 8 render; 9 resize (copies `+0xD24`/`+0xD28` to renderer
`+0xAD8`/`+0xADC`, then base `007A05D0`); 10 renderer byte `+0` = 1; 15 `InputManager+0x39`; 16 `00227D40`; 22 pause
flag; 23/24 scale factor; 25 `InputManager+0x38`. Inherited slot behaviours (PA-5, `APP:431-478`, `APP:655`). "nothing
in this build dispatches slots 10, 15, 16, 22, 23 or 24" (`APP:372`).

#### Inputs, outputs and record layouts

- `GameApplication` object fields: request flags `+0x1E/+0x20/+0x21/+0x22/+0x23/+0x29`, frame time `+0x48` (double),
  frame counter `+0x64`, quit byte `+0x69`, mode `+0xD20`, resolution `+0xD24/+0xD28`, record stream `+0xD98`,
  framework handle `+0x1130/+0x1138`, readiness `+0x113C`, startup latch `+0x113D` (`APP:230-233`, `APP:392-398`,
  `APP:411`, `APP:432-475`, `APP:655`).
- `GraphicsCommandRecord` 0x10 B `{u64 data, u64 regId}` (`FRM:594-597`); `GifTagHeaderRecord` 0x10 B (NLOOP bits
  0-14, EOP bit 15, NREG bits 28-31, register list) (`FRM:599-603`); `RenderCommandBuffer` 0x18 B
  `{pBegin, pWrite, u32 capacity (0x200 by default), u32 initialised}` (`FRM:605-610`); `SubpacketScope` 0x10 B
  (`FRM:612-615`).
- GIFtag constant `0x1000000000008000`, REGS `0xE` (`FRM:541`, `FRM:559-565`); NLOOP finalisation formula
  (`FRM:571-577`); terminator test `(*(u32*)(end-0x10) & 0x70000000)==0x30000000`, record `0x10000000`/0, placed when
  `count<0x200` (`FRM:342-346`); publish value `0x100` (`FRM:349`).
- Queued-effect entry, stride 0x70 at `02EBF9E0`: kind `+0x00` (kind−1 ≤ `0xC`), pass nibble `+1`, class byte `+2`
  (indexes `02EC07E0`), flag `+0x10`, per-kind pass bytes `+0x1D..+0x1F`, live flag `+0x68` (`FRM:410-419`,
  `FRM:435-437`).
- Pass-enable table `022C7F90`: two entries `{u16 pass bits, u16 upper bits}` then bytes `+8`, `+9` (capture),
  `+0xA` (`FRM:690`); `passEnabled(bit, drawMode) = (*(u16*)(0x022C7F90 + drawMode * 4) >> bit) & 1` (`FRM:661`);
  the bit → pass table (`FRM:664-674`).
- Viewport: reference 512×448 (`01E0C1D8`/`01E0C1DC` = 0x200/0x1C0) or 1920×1080, aspect `1.77778` at `008C5B38`
  (`FRM:699-714`, `FRM:529-530`).

#### State (globals, with lifetime)

| global | meaning | lifetime / initialiser | cite |
|---|---|---|---|
| `02064AD3` | frame-mode byte, 0-6 | boot initialiser `0022A0B0` sets 0 at `0022A1A0` | `FRM:141`, `FRM:509-532` |
| `02064AA0` | frame argument | written each frame by `0022A490`; "cleared by mode 3" | `FRM:512` |
| `02064AD0` / `02064AD8` | u8 counter / u32 parity | per frame | `FRM:113` |
| `022C7F90` | pass-enable table | "uninitialised at load", reset by `00358510` whose single caller is `0022A0B0` | `FRM:690`, `FRM:692` |
| `02EBEFC0`, `02EBEFD8`, `02EBEFF0`, `01FD4A78` | two buffer descriptors, buffer index, arena pointer | 512 records × 16 B per buffer | `FRM:286`, `FRM:291`, `FRM:519` |
| `02EAF6D8` | fence word, zero-filled; "All 17 references … are loads" | static | `FRM:191`, `FRM:1094` |
| `02EA5368` | global application pointer (getter `00796E20`) | process | `APP:401`, `APP:404` |
| `[01F7F598]` | renderer singleton | process | `APP:391` |

#### Order

PE entry → CRT initialisers (module registration, §1.2) → `WinMain` → `007980A0` → module init walk → message loop →
run loop → slot 28 per frame → (slot 7, slot 4 → `0017D6E0` → `0022A490` → `0022A580` → mode body) … → slot 8
render (`APP:431-437`, `APP:491-511`, `FRM:78-85`). Mode transitions: 4→3, 6→5, 0→1, 1→2, 3→2 under the stated
predicates (`FRM:133-137`); external writes set 4 and 6 (`FRM:143-146`). Mode 2's section order (`FRM:124`,
`FRM:172-179`). Within a frame: `0036F2F0` in every mode, the mode body, `0036F2C0`, then publish through
`003A1DB0` → `0036F360` (`FRM:734-751`). The `MainLoop_Draw` pass order is `FRM:380-401`.

#### Dependencies

`17-Presentation-Rendering` ordered render command list (`FRM:373`), the shared command-state word page
(`FRM:248`), the PS2 GS texture page (`FRM:652`), script screen effects (`FRM:692`), the CG-6 record
`_index/candidates/cg6-no-consumer/README.md` (`FRM:874`), `game-application.md` (`APP:391`, `APP:396`), the input
stack (`APP:618`), and Movement, Actor, Party, Audio, RNG, Achievements as callees (`FRM:1015-1023`).

### 1.2 Module registry (before `main`)

| entry | callers | what it does | cite |
|---|---|---|---|
| 15 module registrars (e.g. `00166210` for `PScripting`) | CRT `.CRT$XI` initialisers (table `0x008C31D8`, 1,172 entries) | write the derived vtable into a static module object, splice at the head of list `0x02CACC90`, tail-jump `atexit` `00808B90` | `MOD:74-108`, `MOD:239`, `MOD:475` |
| module table (static object / class / derived installer / base installer) | — | 15 rows, `01F2CD80` `PSerialization` … `02E5BE88` `PText` | `MOD:127-143` |
| init walker `005A08E0` (507 B) | start-up `007980A0` | calls slot `+0x08` on each node; non-zero aborts start-up; registers the shutdown walker with `atexit` | `MOD:163`, `MOD:207-215` |
| shutdown walker `005A0840` (145 B) | `atexit`, and directly at teardown | calls slot `+0x10` on each node, return ignored; then the shutdown sequence | `MOD:164`, `MOD:543-549`; `APP:512-513` |
| slot 0 `005A0CB0` (100 B) | — | scalar deleting destructor that unlinks the module | `MOD:393-403` |

Module object: `+0x00` vtable, `+0x08` next, `+0x10` name, `+0x18` ordering key = `0xFF` (`MOD:74-75`, `MOD:104-105`).
Vtable contract: `+0x00` destroy-and-unlink, `+0x08` init (0 = success), `+0x10` shutdown (`MOD:219-223`, `MOD:402`).
State: list head `0x02CACC90`, guard flag `0x02CACCA0` (`MOD:74`, `MOD:212`); init allocates a `0xE0`-byte object
(address disputed, §3 C-V13); sync object `02D3E880`; timer globals `02CB60E8`, `02CB6120` (`MOD:171-174`). Order:
the chain is the reverse of registration order, because each registrar splices at the head (`MOD:104-108`,
`MOD:409-410`). Name hash shared with reflection: seed `0x7B5`, `×0x21 + (c & 0x1F)` (`MOD:261`; `APP:665`;
`MR:506-508`).

### 1.3 Asset container (`.phyre`)

`.phyre` is 35,984 files, 25,896 MB, "40 % of the archive by count and 72 % by size" (`PAC:5`, `PAC:11`).

| entry | callers | what it does | cite |
|---|---|---|---|
| `0059A3B0` header read and validation ladder (589 B) | exactly one, `0059E070` at `0059E153` | `int Read(Stream *rcx, ClusterHeader *rdx, NsBuffer *r8, Buffer *r9, bool *outWasByteSwapped [rsp+0x28], uint32 *outSize [rsp+0x30], bool checkPlatform [rsp+0x38])` | `C-HDR:54-59`; `HDR:249-250` |
| `0059E070` (656 B) | `0059E300` | sets `checkPlatform = 1`; after the header, checks the namespace BOM and size identity (`0059E167`, `0059E173`-`0059E191`) | `HDR:250`, `HDR:174`; `NS:416-417` |
| `0059E300` cluster orchestrator (1,141 B) | — | runs the member builders in body order | `HDR:409` |
| `0059A6F0` packed-namespace reader (116 B) | `0059A3B0`, from its size paths | `int Read(Stream *rcx, bool wasByteSwapped dl, void *buffer r8, uint32 len r9d)`; returns 0/9 only | `C-NS:53-56` |
| `0059C180` namespace byte-swap (202 B); `0059A780` class records (294 B); `0059A8B0` type table (246 B) | `0059A6F0` | swap order header → classes → members → type table | `C-NS:57`, `C-NS:173-174`, `C-NS:254-268` |
| `0059E880` user-fixup loader (959 B) | `0059E300` | 12-byte `{typeIndex, size, offset}` records; type resolution; `PAssetReferenceImport` kept raw | `HDR:706-726` |
| `GetPlatformID` `00686D00`, `GetPhysicsEngineID` `0069E780` (6 B each) | `0059A3B0` | constants `0x44583131`, `0x424C4C54` | `HDR:252-253`, `HDR:164-165` |
| field registrars `005983E0` (18 fields), `00598C50` (3), `00598DF0` (instance-list header) | `PSerialization` module init | | `HDR:254-256`; `C-HDR:533-539` |

**Header** (84 bytes, 21 `u32`, `HDR:68-90`): `+0x00` `m_phyreMarker` = `0x50485952`; `+0x04` `m_size` = 84; `+0x08`
`m_packedNamespaceSize`; `+0x0C` `m_platformID` = `0x44583131`; `+0x10` `m_instanceListCount`; `+0x14`..`+0x2C` array,
pointer and pointer-array fixup sizes and counts and `m_pointersInArraysCount`; `+0x30` `m_userFixupCount`; `+0x34`
`m_userFixupDataSize`; `+0x38` `m_totalDataSize`; `+0x3C` `m_headerClassInstanceCount`; `+0x40`
`m_headerClassChildCount`; `+0x44` `m_physicsEngineID` (`0x424C4C54` or 0); `+0x48/+0x4C/+0x50` index, vertex and max
texture buffer sizes (D3D11 subclass). **Instance-list header** 36 B, nine u32 (`HDR:102-115`). **Return codes** 0
success, 6 refuse, 9 truncated, 0xD out of memory (`HDR:146-147`), and the nine-row return table (`C-HDR:274-284`).
**Fixup tables**: stage order pointer-array, pointer, array; entries 16 B (array, pointer-array) and 0x1C (pointer);
mode byte 0-6 then varint key rotated right by one (`HDR:357-364`). **Packed namespace** (`NS:400-413`): BOM
`0x01020304`, namespaceSize, nTypes, nClasses, nMembers, stringPoolSize, `+0x18` unread, `+0x1C` optional-block size,
then type-name offsets, 9-word class records, 6-word member records, string pool. Size identity `+0x04 == 0x20 +
[+0x1C] + 4 × (nTypes + 9 × nClasses + 6 × nMembers) + stringPoolSize` (`NS:417`). Class words `w0` parent (1-based),
`w1` kind and size, `w2` name, `w3` member count, `w7` flags; member words `w0` name, `w1` type reference, `w2` packed
offset, `w3` width, `w4` attribute word, `w5` fixed-array bound (`NS:480-488`; `C-NS:93-111`). `w7` bits `0x01`
dynamic, `0x02` abstract, `0x04` header, `0x08` no-default-ctor (`C-NS:428`).

State: `PTypeDefault<unsigned int>` singleton `01F2E5A0`; byte-swap descriptor `02CAA0A0`, built by CRT constructor
`00160210` (`HDR:93`, `HDR:258-259`; `C-HDR:552-558`). The namespace buffer's bit 31 marks a borrowed buffer
(`C-HDR:98-102`). Order: read 84 bytes → marker test, swap, retest → platform test → physics test → namespace
allocation and read (`HDR:126-143`; `C-HDR:297-351`). Dependencies: reflection (§1.4) for the swap descriptor and the
member lists; `_aligned_malloc` `0017D260` / `_aligned_free` `00584730` (`C-HDR:136-138`); Bullet (`HDR:451-452`).

### 1.4 Reflection: class descriptors and member records

"4,557 functions — roughly one in every eight in the whole game" (`CDMS:54`). Descriptors are built eagerly by CRT
initialisers; "680 of the 682 `PClassDataMember` registrations execute behind a one-time-initialisation guard"
(`CDMS:110-112`; `MR:113-116`).

| entry | callers | what it does | cite |
|---|---|---|---|
| descriptor ctor `00632D80` (241 B, 173 registrars) and `00632C90` (226 B, 4 registrars) | per-class static initialisers | arg2 → `+0x70`, name → `+0x30`, size → `+0x38`, alignment → `+0x3C`, parent → `+0x78`; last store `+0xFC` | `IS:64-71`, `IS:84-87`, `IS:133-134`; `MR:162-185` |
| `PClassDataMember_Register` `00632960` (165 B, 682 sites) | lazy per-class registrars | the one data-member registration entry | `MR:69-80`, `MR:575` |
| member constructors `00632A10` (array, 165 sites), `00632A70` (fixed-size), `00632BE0` (enum), `00632B30` (dynamic) | registrars | | `MR:2288-2294`; `AR:65-71` |
| base ctor `00632FB0` (141 B) | member ctors | list, owner, name, attrs | `MR:576`, `MR:133-147` |
| `PType_FindOrRegisterByName` `006388C0` (254 B) | registrars | name hash `0x7B5`, `×0x21`, `+ (c & 0x1F)` | `MR:577`, `MR:506-508` |
| `AttachMember` `0062EFD0` (descriptor vslot `+0x40`) | `00632960` | attaches a member; return codes 0/5/0x12/0x15 | `MR:354-378`, `MR:437-438` |
| `FieldStorageWidth` `0063C0C0` (210 B) | `AttachMember` | pointer width from `ctx->vslot08()` when attribute bit 1 is set (corrected 2026-09-19) | `MR:394-410` |
| registration insert `00639160`, finaliser `00639450`, id/pre-order pass `00638AE0` | `005A08E0` | | `CDMS:368-414`, `CDMS:1730` |
| base descriptor destructor `00633390` (500 B), sub-object dtor `0063D640` (109 B), reset `0063D550` (233 B), deleting dtors `005847E0` ×1,148 (92 B) | `atexit` chain | | `C-CD:50-57`, `C-CD:120-125`, `C-CD:375-402` |
| `ObjectTraversal` `0063E2E0` (byte-swap walk) → `0063CE80` per field, `0059FDB0` per element | cluster loader | | `CDMS:429-447` |
| default-object getter `0063BC00` (112 B), default buffer `00639A60`, mask builder `00639C80` (1,160 B), buffer without ctor `0063CB80`, instance copy `0063C910`, `PCluster::create` `0063A990` | object creation | | `CDMS:631-727`, `CDMS:793-796`, `CDMS:847-926`; `MR:1538-1558` |
| `0063E410` | registration | running sum of `+0xF0` into `+0xF4`/`+0xF8` | `MR:1686-1694`, `MR:1750` |
| `PAnnotation` ctor `006B66C0` (37 B, 70 callers) | registrars | `WriteMask = 0x7FFFFFFF` annotations, linked at member `+0x38` | `AR:107-115`, `AR:180` |

**PClassDescriptor** (bytes, after the 2026-09-02 unit correction): `+0x00` vftable, `+0x08..+0x28` membership init
unit (hash `+0x20`, name pointer `+0x28`), `+0x30` name `char *`, `+0x38` instance size, `+0x3C` alignment, `+0x50`
registry node, `+0x60` annotation list, `+0x70` registry/sub-object, `+0x78` parent, `+0x80` fields, `+0x90` methods,
`+0xA0` script bridge, `+0xB0` unnamed (BL-8), `+0xC0` default instance, `+0xC8`/`+0xD0` byte masks, `+0xE8` id,
`+0xEC` pre-order index, `+0xF0` ctor arg 7, `+0xF4`/`+0xF8` offset adjustments (running sums), `+0xFC` flags (bit 1
abstract, 2 header, 3 no default ctor, 30 members registered, 31 buffer built); base size 0x100,
`PClassDescriptorDynamic` 0x140 (`C-CD:66-99`, `C-CD:488-494`, `C-CD:689-691`; `CDMS:160-178`, `CDMS:361-374`,
`CDMS:409-417`, `CDMS:751-778`; `MR:166-185`, `MR:1669-1716`). **PClassDataMember**: `+0x00` vftable, `+0x08/+0x10`
list node, `+0x18` owner, `+0x20` name, `+0x28` u32 attrs, `+0x30` `PType*`, `+0x38/+0x40` annotation list, `+0x48`
u32 field offset, `+0x50` 0 (`MR:638-651`). Array members add `+0x58` element size and `+0x5C` kind (1 fixed, 2
dynamic pointer, 3 `PArray`, 4 `PSharray`) (`AR:65-71`, `AR:90`). Array header `{u32 count (bit 31 adopted), u32,
pointer or inline element}`; `PSharray` size `8 + max(8, sizeof T)` (`MR:2310-2321`, `MR:2347`). **Field address**:
`instance + (member.offset − classdesc[0xF4])` (`MR:1727`, `MR:2319`; `CDMS:433`). The recovered schema is
`phyre-field-schema.tsv` (count disputed, §3 C-V20).

State: id counter `02CF8260`, pre-order total `02CF8264`, root `PBase` descriptor `02CF8270`, registry table
`02CF82E0` (`CDMS:359`, `CDMS:373`, `CDMS:1926-1941`); registration guard `02CB0A98` (`MR:596-598`); default
instances in `.bss`, 173 of them (`MR:1574-1584`; `IS:193-199`). Lifetime: descriptors from CRT start to `atexit`;
member lists "for the process lifetime" once built; static records unlinked, not freed (`MR:302-316`, `MR:727`).
Order: CRT static init → `005A08E0` registry init → lazy member registration on first use → `PCluster::create` →
`0063E2E0` byte swap → `atexit` teardown (`CDMS:293-310`, `CDMS:793-796`, `CDMS:960-965`).

### 1.5 Script bridge: embedded Lua 5.2.1 and the object accessors

"The retail EXE embeds **Lua 5.2.1**, with 1,219 generated binding functions" (`README:41-42`; `LUA:55-60`).

| entry | callers | what it does | cite |
|---|---|---|---|
| `00682980` `luaL_testudata` for `"PhyreObject"` | the 747 accessors | type-checked userdata fetch | `ACC:215`; `LUA:117-133` |
| `00682D20` shared push (112 B), `00682D20(L, obj, descriptor)` | 7 direct, 834 through thunk `00684080`; 841 in total | push an engine object as 16-byte userdata `{descriptor, obj}` | `LUA:162-163`, `LUA:342-361` |
| 747 `PObjectAccessor<T>::Get` (402 pointer, 345 reference) | the bindings | testudata → settop → walk the `+0x78` base chain → match or report into the 24-byte assert record `0x02E41000` | `ACC:54`, `ACC:88-107`, `ACC:133-137`, `ACC:162-192` |
| push / nullable push / optional-pointer adapter families | descriptor vtable `+0x20`/`+0x30` | | `ACC:26-49`; `ACC:908-913` |
| `PCallerScript` slots 1 (`00684D10`, compile and register via `luaL_loadbufferx`) and 2 (`00686280`, execute via `lua_pcall`) | virtual dispatch only | | `LUA:1037-1062` |
| scripting module slot 1 `00685AC0` (five reflection registrations, then four `luaopen_*` appends) / slot 2 `00685F60` (free) | module init walker | | `LUA:883-891`, `LUA:955-958` |

Lua C API addresses: `lua_type` `008119F0`, `lua_settop` `00811130`, `lua_getfield` `0080FA50`, `lua_getmetatable`
`0080FBA0`, `lua_rawequal` `00810810`, `lua_touserdata` `00811950`, `lua_checkstack` `0080F420`, `lua_pushnil`
`00810620`, `lua_newuserdata` `00810240`, `lua_setmetatable` `00810F60` (`LUA:215-231`, `LUA:344-348`). Layouts:
`lua_State` 5.2 64-bit `+0x10` top, `+0x18` G(L), `+0x20` ci; `TValue` 16 B; userdata `ud[0] = descriptor, ud[8] =
obj`, header 0x30, tag 0x47 (`LUA:236-249`, `LUA:344-351`). Constants: `LUA_REGISTRYINDEX` `-1001000` (`0xFFF0B9D8`);
registry key `"PhyreObject"` at `00D6FDE0` (`LUA:135`, `LUA:634-637`). State: `luaO_nilobject` `01CCB510`;
`PScripting` descriptors at a 0x100 stride `02E41070`…`02E41470`; registration list count `02E41570`, buffer
`02E41578` (`LUA:98`, `LUA:929`, `LUA:939-940`). Order and lifetime: **no `PScheduler` ever exists** (`LUA:403-404`,
R-5 answered 2026-09-22 at `LUA:384`); "no standard library is ever opened" (`LUA:366-367`); whether any `lua_State`
is created is open (DA-1, `LUA:924-925`). What runs per frame: not stated.

### 1.6 Animation channel binding and transform composition

| entry | callers | what it does | cite |
|---|---|---|---|
| `AnimationTargetBlender_ApplyChannelsToTargets` `005C72A0` (1,674 B) | vtable slot 12 of `PAnimationTargetBlenderController` `00D31768` | per-frame apply: group channels by target, fold and set bits, compose a 4×4 at group end when `kind==1`, write translation; kinds 2/3 dispatch to setters | `ANI:109-115`, `ANI:139-145`, `ANI:329-399`, `ANI:552` |
| `…BindDataMember` resolve `005C0820` (827 B) | slot 1 of vtable `00D317F0` | bind once: resolve the member path, compute offset and size | `ANI:256-313`, `ANI:566-573` |
| binders `005C1160` (shader parameter, kind 1), `005C0C90` (method, kind 2), `005C0B60` (function, kind 3) | binder family | | `ANI:571-576` |
| `005C6020` additive (323 B), `005C61A0` weighted (288 B) | per frame | mark contributed slots | `ANI:428-439` |
| `005A7E90` variadic setter forwarder (61 B) | kind 2/3 arms | `(*(code**)(*handler+0x10))(handler, context, 0, 0, &ap)` | `ANI:402-415` |
| `005BF290` ChannelValue writer; `005BFE70` whole-slot copier; static init `005C5C80`, teardown `005CB150` | | | `ANI:517-526`, `ANI:1013-1037` |

Layouts: `ChannelSemantic` 24 B, 19-entry table at `01F2CE40` (`ANI:172-204`); `ChannelValue` 40 B, four floats at
`+0x00`, semantic pointer `+0x10`, `+0x18` u16, `+0x1C` dword, `+0x20..+0x27` uninterpreted tail (`ANI:209-216`,
`ANI:521-526`); `AnimationTarget` 48 B (kind, dest, size ≤ 0x10, context, objects) (`ANI:222-230`);
`AnimationBindDescriptor` 56 B (`ANI:256-264`); accumulator bits 0x1 Rotation, 0x2 Scale, 0x4 Translation
(`ANI:323-327`). Formulas: path offset `offset += (int)member[9] - *(int*)(member[3]+0xF4)` (`ANI:271`); normalise
`s = 1/sqrtf(Σ)` with `01CEBBA8` = 1.0f (`ANI:346-347`); rotation, scale and translation (`ANI:357-388`, verified
`ANI:883-905`). State: semantic list head `02CAFCD8`, count `02CACF18`, registry `02CACF20[]`; destination matrix
caller-owned with its fourth column pre-set (`ANI:353-354`, `ANI:517`). Order: bind once, then each frame evaluate →
mark → apply (`ANI:65-66`, `ANI:455-462`). In the shipped data: "**2 clusters and 4 channel targets**"
(`ANI:529-531`, `ANI:643-653`).

### 1.7 Post-process passes, the post-effect class family and shader-variant selection

**Game-side post-process passes** (twelve bodies, `PPF:56-69`):

| address | size | pass |
|---|---:|---|
| `0018E4A0` | 2,418 B | AO blur/composite |
| `0018F6B0` | 567 B | bloom/bright-pass |
| `0018F8F0` | 1,147 B | colour grading |
| `0018FE00` | 1,105 B | single-step edge pass (identity "not claimed", `PPF:553`) |
| `00190260` | 1,273 B | font border |
| `00190760` | 2,507 B | HBAO |
| `00191130` | 1,066 B | depth mask |
| `00191560` | 2,101 B | depth of field |
| `00191E90` | 1,847 B | scalable AO |
| `001925D0` | 2,839 B | SMAA |
| `001930F0` | 2,099 B | SSS blur |
| `001EE8E0` | 840 B | colour-buffer copy |

| entry | callers | what it does | cite |
|---|---|---|---|
| `FindShaderParameter` `0018D240` (209 B) | 37 callers | walks shader `+0x48` (count `+0x40`) and `+0x58` (count `+0x50`), 0x18-byte elements, name at `+0x08` | `PPF:80`, `PPF:267`, `PPF:407`, `PPF:422-423` |
| `001945B0` | the passes | parameter-descriptor write into the constant buffer; type byte must be in `{0x12, 0x16, 0x42, 0x43, 0x44, 0xD9 … 0xDC}` else 5; null 5; bounds 3; success 0 | `PPF:512-520` |
| AO dispatcher `0018F510` | the frame | reads HDAO; when AO is on and `+0x198` is set, runs `+0x344 == 1 ? 00190760 : 00191E90` | `PPF:365-377` |
| `00191DA0` | the frame | SMAA or the PFXAA worker (`0065A630` → `0065A640`), then `001EE8E0` | `PPF:554-561`, `PPF:880-930` |
| render-pass registry `005DC6F0` (shim), `005FDCB0` REGISTER, `005DDD60` UNREGISTER | CRT static init; 60 `atexit` wrappers | node `{name, next, u8 flag, u32 0xFFFFFFFF}`; REGISTER returns 0x11 null name, 0x12 duplicate, 0 success | `PPF:291-313` |
| `001E2AF0` map render pass + 34 constants (4,745 B) | `MapOrderedObject` `00212C60` | | `PPF:1473-1474`, `PPF:1528`, `PPF:1666-1671` |
| post-effect slot-6 overrides and workers (nine classes) | the post-effect class vtables | `PAtmospherics` `0065B270`→`00658470` … `PScreenSpaceReflection` `0065B920`→`0065BA00` | `PFX:58-68` |
| base slots 0-8 of `PPostEffectBase` | — | configure `00655DC0`, refresh `006575E0`, resize `00657680`, ready `006571C0`, which-pass `00657150`, render `0065B8F0` | `PFX:80-90` |
| render-item submit `0060B980` | workers (count disputed, §3) | builds a `PMaterialSelectorMaterialSet`, calls the key builder `00606A20` | `PFX:405-412`; `CTX:400-413` |
| context-switch evaluators (vtable slot 2) `006B9120` NUM_LIGHTS … `006B9450` SKINNING | `00606A20` | each evaluates one draw property into key words | `CTX:52-62`, `CTX:978` |
| registrar `006B8D20`; runtime ctor `006B8590` via `006B89C0` FindOrCreateDynamic | CRT installers `00167050`-`00167280`; asset load | | `CTX:82-94`, `CTX:566-579` |

Layouts and constants:
- **Constant block** `{u32 declaredSize; u8 data[]}`, size word masked `& 0x1FFF` (`PPF:83-96`);
  `PShaderParameterDefinition` 0x18 B (`m_arrayElementCount` u16 `+0x00`, `m_parameterType` `+0x02`, `m_dataType`
  `+0x03`, `m_name` `+0x08`, `m_offset` `+0x10`, `m_size` u16 `+0x12`, `m_constantBufferLocation` `+0x14`)
  (`PPF:425-430`); the shipped packed record is 13 bytes (`PPF:436`).
- **SMAA ladder** on context `+0x184` (threshold, steps, diagonal, corner) (`PPF:107-114`); `SMAA_RT_METRICS =
  (1/w, 1/h, w, h)` (`PPF:136-140`); scalable-AO block `+0x1A8..+0x1C0` with ÷600 and the literal 500.0f
  (`PPF:150-158`); HBAO block `+0x1C4..+0x1E4` with `g_AngleBias = deg × 3.14159250f / 180.0f` (`PPF:186-202`).
- **Post-process context singleton** 0x4A8 B at `01F7F5F0`, built lazily by `00193D50` via `0018CD90`; no vtable;
  defaults `+0x184 = 3`, `+0x198 = 1`, `+0x344 = 1`, HBAO bias 0.523, radius 1.0, intensity 1.25, NumSteps 3,
  NumDir 8 (`PPF:178-181`, `PPF:389-402`, `PPF:1567-1568`). PFXAA member at `+0x378` (`PPF:555`).
- **Post-effect base object**: `+0x10` holder, `+0x18/+0x20/+0x28` cached triple (PMaterial, `PParameterBuffer`,
  runtime field), `+0x40` configured, `+0x41` enabled, `+0x44` width, `+0x48` height (`PFX:110-117`,
  `PFX:668-678`). "**thirty-seven classes … only nine of them have any implementation**" (`PFX:27-28`).
- **Context-switch object** 0x28 B `{vtable, name, next, pool-owned, u32 word count, base value byte}`
  (`CTX:71-78`); evaluator takes seven arguments (`CTX:255-263`); output record `PLight*[4]` + u32 count at `+0x20`
  (`CTX:329-341`); trailing record built by `0060B980` (`CTX:349-357`).
- **Variant key**: light code `(shadowTypeIndex << 5) | lightTypeIndex`; key size `((10·n + 35) >> 5) << 2` bytes;
  count `min(kept, m_maxLightCount)`; LOD_BLEND emits 1 iff 0 < w < 1; SKINNING requires masked count ≤ 0x78; 16BIT
  is byte `+0x4C == 0x0C`; ORTHO is float `+0x6C ≥ 0.01` (`CTX:128-153`, `CTX:979-980`). Key lookup:
  `alloca(budget×4)`, evaluate each switch, binary-search the effect's variant table (`+0x58` count, `+0x60`
  16-byte `{count, words*}`), `index << 6` into a 64-byte table (`CTX:404-413`).
- **State**: switch registry head `02E522D0`, word budget `02E522E0` = 10 after static init (`CTX:88`, `CTX:94`);
  render-pass registry head `02CBF998`, 60 nodes (`PPF:291`, `PPF:296-297`); runtime pass registry in three bands
  (10 game, 43 Phyre, 7 text) (`PFX:594-596`).
- **Order**: passes register at static init (`PPF:291`); per frame the AO dispatcher, then `00191DA0` (`PPF:367-374`,
  `PPF:561`); per draw `0060B980` → `00606A20` (`CTX:400-413`); per load the scene-config loaders `001C3D50`,
  `001C7940` fill the AO blocks (`PPF:169-170`).
- **In the shipped game**: "In the shipped game there is no instance to invoke" for the post-effect family except
  `PFXAA`, which code constructs (`PFX:138`, `PFX:439-445`).

### 1.8 The camera state snapshot (`GiBeginEff` prepare)

`00864F30` (512 B) is slot 0 (prepare) of the `GiBeginEff` render-command vtable `01CCFB78`; no direct callers, reached
by `jmp qword ptr [rax]` in the command list's prepare step (`CAM:31`, `CAM:115-121`, `CAM:151-152`, `CAM:171`).
Record (0x90 B): `+0x00` vtable; `+0x08` mat4, the inverse head matrix from `02AEEB20`; `+0x48` mat4, the camera
projection with m22/m32 rebuilt from near/far; `+0x88`/`+0x8C` depth window from `02AEEBA0`/`02AEEBA4`
(`CAM:157-166`). Execute (slot 1) stores the first matrix to `01FD3620..01FD365F`, passes the second to
`PrimitiveRendererD3D11` `006CAF40`, and stores the depth window at `01FD3660`/`01FD3664` (`CAM:121-125`). Depth
helper `00678B50`: "`m33 == 0` → `f/(n−f)`, `n·f/(n−f)`; else `1/(n−f)`, `n/(n−f)`" (`CAM:136-138`).

### 1.9 Dependencies on other categories (summary)

| depends on | for | cite |
|---|---|---|
| `24-Compiler-And-CRT-Runtime` static init and `atexit` | every registrar, descriptor and module | `MOD:376`, `MOD:474-475`; `CDMS:36` |
| `23-Third-Party-Libraries` inventory | Lua 5.2.1 and Bullet | `LUA:435`, `LUA:1086`; `HDR:451-452` |
| `17-Presentation-Rendering` ordered render command list and Gi command family | render commands, the camera command, pass records | `FRM:373`; `CAM:118`; `PFX:478`, `PFX:549-551` |
| `19-Save-Load-Settings` game-settings ini | HDAO, PostAA and the AO tuning | `PPF:221`, `PPF:369`, `PPF:595` |
| `01-Script-VM-Native-Bridge` | a *different* VM (the EBP VM); not this Lua | `LUA:314-316` |
| game-side callers (Movement, Actor, Party, Audio, RNG, Achievements, Input) | frame-body callees and slot overrides | `FRM:1015-1023`; `APP:618` |

---

## 2. Gaps

### 2.1 Gaps the pages state themselves (still open, or live-only)

| # | gap, as the page states it | cite | note |
|---|---|---|---|
| G-1 | **Where the frame's GS command buffers are consumed**: "nothing in this executable reads a finished batch" | `FRM:870-874` | answered *negatively*: the port cannot copy a consumer, it must supply one (a PS2-GS-stream → D3D11 translation is not described anywhere) |
| G-2 | `UQ-299` residue: "Which of its states the PC build reaches in play, and whether the entry gate's pad bit is Start, are not established; both are live questions." | `FRM:942-944` | live-only |
| G-3 | `UQ-300` "OUT OF EVIDENCE BOUNDARY" | `FRM:945` | |
| G-4 | `UQ-301` residue: whether anything is emitted inside the halved 256-record window | `FRM:956-957` | |
| G-5 | `BA-1` (linker-folded bodies) open on both frame and animation pages | `FRM:168`, `FRM:1112`; `ANI:627`; `README:70` | |
| G-6 | Lua: whether any `lua_State` is ever created (`DA-1`) | `LUA:924-925`, `LUA:1156-1157` | the script bridge may be dead code in this build; a port cannot tell what to keep |
| G-7 | Lua: "*which* scripts these execute, from where and when, is still unknown and stays open" | `LUA:515-516` | |
| G-8 | Lua: "Not established: whether a game-side binder registers the Phyre object functions into `_G` without the base library." | `LUA:381-382` | |
| G-9 | Accessors: "what field any accessor reaches is untouched" | `ACC:880` | a port that re-generates accessors needs the per-type member set |
| G-10 | Reflection: descriptor `+0xB0` unnamed (`BL-8`); "The live read of real heads that `BL-8` names is still the closing step." | `C-CD:472-474`; `CDMS:355-357` | |
| G-11 | Reflection: `+0xFC` bits 4 and 5, "meaning is NOT CLAIMED" | `CDMS:769`, `CDMS:777` | |
| G-12 | Reflection: attribute bits 3-4 (`BL-1`) "remain unexplained" | `MR:817`, `MR:1460` | |
| G-13 | Reflection: "Not established: which of the two list orders serves which direction (load or save)" | `CDMS:449` | changes byte-swap/serialise order |
| G-14 | Reflection: default-instance bytes (`OPUS-REQ-ASTRA-PHYRE-DEFAULT-INSTANCE-BYTES`); load-copy "has **not** been traced instruction by instruction" | `MR:1597`, `MR:1661-1665` | initial values of every reflected object are not in the database |
| G-15 | Reflection: 211 member registrations never harvested (165 array, 25 fixed-size, 21 enum) | `MR:1883`, `MR:797` | the field schema is incomplete for array/enum members |
| G-16 | Asset container: CU-3 "**Not decoded:** what each entry's fields mean (which offset is patched with what), and the texture clusters' trailing bytes." | `HDR:370-371` | fixup semantics are needed to load any `.phyre` |
| G-17 | Asset container: UQ-287 residue — "What each type's `+0x48` resolver does internally. / When the `PAssetReferenceImport` bytes are consumed … / The fixup types in the corpus beyond the 42-file sample" | `HDR:746-749` | |
| G-18 | Asset container: "What the `+0x1C` block holds, and where in the layout it sits, is still open." | `NS:419-420`, `NS:463-466` | zero in every shipped file, so low impact |
| G-19 | Asset container: what `00599500` does with the oversized-header bytes is not claimed | `C-HDR:593-595` | |
| G-20 | Asset container: "The 36-byte instance-list header is NOT covered." by the contract | `C-HDR:701` | |
| G-21 | Post-process: what `0018FE00` is ("Not claimed") | `PPF:553` | |
| G-22 | Post-process: "What the `0xA0`-byte object at `01F81170` is has not been read." | `PPF:574` | |
| G-23 | Post-process: "the node carries **no function pointer** … where each named pass's body enters the frame is a separate question" | `PPF:337-340` | the 60-name registry does not give a dispatch table |
| G-24 | Post-effects: `GF-3` "*Not claimed:* what the 43 slots hold … what writes them" | `PFX:822-825` | |
| G-25 | Post-effects: `GF-4` live question "routed to `ASTRA`" | `PFX:448`, `PFX:648-649` | |
| G-26 | Shader variants: "**which file member feeds `00606A20`'s `[rdi+0x48]`/`[rdi+0x50]` pair is not established here.**" | `CTX:514-518`, `CTX:755-756` | file → runtime effect mapping missing |
| G-27 | Shader variants: slot-1 domain bodies `006B9CF0` (NUM_LIGHTS) and `006BA3A0` (SHADER_LOD) "**neither body was read here**" | `CTX:534-537` | |
| G-28 | Shader variants: `GD-2` rests on an assumption, "that the object at `*(arg7)` is a `PCamera`. … This is not proven here" | `CTX:447-451` | |
| G-29 | Animation: `ChannelValue` `+0x20..0x27` "padding or an unread field; which of the two is intent, and it is not claimed" | `ANI:526` | |
| G-30 | Animation: "A binding constructed natively at run time … would not appear here." | `ANI:134-135`, `ANI:676-680` | |
| G-31 | Application: "Not claimed: a call through a copy of the application pointer held by another object."; "Which condition takes that tail is not read." | `APP:404`, `APP:515` | |
| G-32 | Module registry: "**What the key would mean if something set it lower is still unknown.**" | `MOD:406-407` | ordering key `0xFF` is never varied in this build |
| G-33 | Camera: "`GiBeginEff` suggests the command opens an effect pass; this page does not verify that" | `CAM:110-111` | |
| G-34 | Subsystem map: `AQ-2` residue — "which class each of the 1,063 folded bodies serves …, what the 2,254 are beyond their sub-tags" | `MAP:188` | |

### 2.2 Structural gaps found while mapping (a port needs these and no page states them)

| # | missing piece | where the page shows the gap | why a port needs it |
|---|---|---|---|
| S-1 | **The per-module init (`+0x08`) and shutdown (`+0x10`) bodies of all fifteen modules** | `MOD:219-223` gives the contract only; no body for any module | start-up order and what each module allocates |
| S-2 | **End-to-end `.phyre` file layout after the namespace** (instance-list headers, header-class tables, fixup tables, user-fixup blob, object data, in one sequence with offsets) | `HDR:263` vs `HDR:323-325`, `HDR:357`; `CTX:690-691` gives only "header \| namespace \| N × 36-byte PInstanceListHeader \| data" | the loader cannot be written without it |
| S-3 | **Fixup-table entry field meanings** (which offset is patched with what) | `HDR:370-371` (G-16) | pointer relocation of every loaded object |
| S-4 | **The `+0x48` per-type user-fixup resolvers** | `HDR:746` | asset references across clusters |
| S-5 | **PEffect file → runtime mapping** (runtime `+0x48/+0x50/+0x58/+0x60` feeders) | `CTX:514-518`, `CTX:756` | shader-variant selection cannot run on loaded effects |
| S-6 | **The 64-byte compiled-variant table entry** reached by `index << 6` | `CTX:413` (named, not described) | what the key selects |
| S-7 | **Bit order inside the NUM_LIGHTS key words** (LSB/MSB first, where the 4-bit count sits) and the binary-search comparison signedness | `CTX:133-134`, `CTX:410` | keys must match the shipped variant tables bit for bit |
| S-8 | **The PS2 GS command stream's meaning on PC** — what the D3D11 side does with each GIF register write | `FRM:870-874`, `FRM:885` ("What each command meant to that backend is not decidable from this executable") | the frame draws by writing GS registers that nothing reads (G-1) |
| S-9 | **Mode 3 and mode 5 body order** (only label lists) | `FRM:125`, `FRM:127` | the menu and capture frames |
| S-10 | **Boot predicates `0032E520`, `0037C2E0`, `0209273C==5`** named, not described | `FRM:135-136` | mode 0→1→2 transitions |
| S-11 | **Arguments of `0036D400`** (bits 5/7 pass "first/second argument") while the formulas use none | `FRM:619-636`, `FRM:671`, `FRM:673` | the GS register batch |
| S-12 | **Meanings of `022D8EA8`, `022D8EB4`, `022D8EB8`** in the GS register formulas | `FRM:619-627` | |
| S-13 | **Post-process pass constants other than SMAA and AO**: `g_brightPara`, `colorR/G/B`, `percent`, `gamma`, `dofShift`, `materialColor`, `sssBlur`, `blendAmount`, `FontBorderSetting/Color`, `MaskDepth`, `g_HBAOResolution`, `g_FocalLen`, `widthAO/heightAO` (names only, no source or value) | `PPF:59-66`, `PPF:228-259` | |
| S-14 | **Post-effect worker bodies** (draw content and constants) — only `00652940` and `00659A90` read | `PFX:354-401`, `PFX:387` | PFXAA is the one constructed (`PFX:138`); its constants are not named |
| S-15 | **`ctx` / `flag2` arguments of `00632960` and the context object behind `ctx->vslot08()`** | `MR:397-398`, `MR:614-615` | pointer width in the corrected width formula comes from it (`MR:406-410`) |
| S-16 | **`006372A0` / `006373D0`**, which compute descriptor ctor arguments 2 and 6 | `IS:136` | registry and parent pointers |
| S-17 | **`00639C80` (1,160 B)**: "What it validates is not claimed here." | `CDMS:897` | default-buffer masks |
| S-18 | **`lua_pcall`, `luaL_loadbufferx`, `lua_newstate` addresses** — named only | `LUA:289`, `LUA:380`, `LUA:1061` | |
| S-19 | **`00812960` (accessor "report") and `0063BC00` reference-variant path** | `ACC:104`, `ACC:854` | how a type-check failure is reported |
| S-20 | **Per-accessor field offsets and type-descriptor addresses** ("the constant **is** the payload") | `ACC:871`; appendix `ACC:412-787` gives address and type only | |
| S-21 | **Animation group-boundary detection and `ChannelValue` component → x/y/z/w mapping** | `ANI:109`, `ANI:209-216`, `ANI:343` | composition order inside a group |
| S-22 | **`005A7E90`'s callee protocol** (handler slot `+0x10`, va_list layout) and the kind-2/3 binders' semantics | `ANI:402-421`, `ANI:575-581` | |
| S-23 | **`GameApplication` slot bodies not given**: `FUN_0017d670`, `0079BF70`, `FirstFrameInit` `0017D650`, slot 21 `0017CFD0` | `APP:88`, `APP:219`, `APP:278`, `APP:217` | |
| S-24 | **`GiBeginEff` execute slot address and factory address** | `CAM:116`, `CAM:121-125` | |
| S-25 | **Instance-list (36-byte) records → object construction**: no page joins `m_classID` / `m_objectsSize` / `m_arraysSize` to the descriptor factory call sequence | `HDR:102-115`; `C-HDR:701` | |

### 2.3 Fields written by documented functions whose meaning is not given

- Descriptor `+0xD8`, `+0xE0`: "No setter found" (`C-CD:94`, `C-CD:720`); `+0xE8`/`+0xEC` counters touched in
  passing (`MR:1074`).
- `PAnnotation` `+0x28` written as 0, meaning not given (`AR:180`).
- Post-effect base: the third cached pointer `+0x28` (`PFX:684-685`).
- Frame pass-enable table bytes `+8` and `+0xA` (`FRM:690`, `FRM:692`); upper `u16` bits stated only for bit 2
  (`FRM:505`).
- `00686D10` writes header `+0x48/+0x4C/+0x50` into `rcx`'s `+0x20/+0x1C/+0x24`; destination record not identified
  (`C-HDR:940-943`).
- Camera: the asm at `CAM:47-50` reads source `[rdx+0x50]`, `[rdx+0x60]`, `[rdx+0x80]`, `[rdx+0xb0]`, not reconciled
  with the stated source range `+0x30..+0x6F` (`CAM:134`).

---

## 3. Contradictions (statements a re-implementer would have to choose between)

Every quotation below was re-read against the snapshot (`86b70c69`) line by line. `…` marks an elision inside one
line; nothing is paraphrased inside quotation marks. Two kinds:

- **§3.1 Value-changing**: a count, offset, address, size, constant, formula, order or layout differs. Every one is
  **page-text only - needs local check**. A favoured side is named **only** where a dated correction on the pages
  settles it; otherwise "no favoured side".
- **§3.2 Stale / banner**: a "not read / open / unknown" claim that another line, a later dated section or another
  page answers; a status banner that disagrees with the front matter. These do not change a value a port uses, but a
  reader who stops at the stale line will believe the wrong thing is still open.

### 3.1 Value-changing — page-text only - needs local check

#### Category-wide counts

**C-V1. Phyre function count: 6,768 vs 6,769.**
- "| Functions | 6,768 |" (`README:8`); the composition line sums to 6,768 with "Rendering 287" (`README:66`).
- "**`Reflection` + `ScriptVM` = 5,776 of 6,769 functions — 85.3 % by count.**  *(6,769 at GN161 — the R109 batch classified `00180A70` as `Phyre.Rendering.TextureBufferSetup`; corrected 2026-09-14.)*" (`MAP:274`); `README:70` itself says "4,515 of the 6,769".
- **Favoured: 6,769**, by the dated correction 2026-09-14 (`MAP:274`). `members/phyre-function-class-map.tsv` has 6,769 rows.

**C-V2. Rendering function count: 287 vs 288.**
- "| `Rendering` | 288 | 74,634 | 259 B |" (`MAP:268`)
- "| `Rendering` | 54 | 287 | 18.8 % |" (`MAP:346`); "Rendering 287" (`README:66`)
- **Favoured: 288**, by the same 2026-09-14 correction (`MAP:274`); the seam table and the README were not updated.

**C-V3. RTTI class counts: 2,133 / 2,134 / 2,248, and Phyre classes 1,604 / 1,739.**
- "`rtti_recover.py` recovered **2,133 classes** image-wide, of which **1,604 are `Phyre::`**, carrying" (`MAP:58`)
- "| 2,134 RTTI classes | independent MSVC RTTI walk (`rtti_recover.py`) | 4 |" (`CDMS:489`, evidence row, unstruck)
- "~~**2,134 RTTI classes** are present in the binary~~ — **superseded 2026-09-08, see §14: the count is" / "2,248, and the run that produced 2,134 failed to demangle about three quarters of the names.**" (`CDMS:203-204`); "**Use 2,248.**" (`CDMS:1328`)
- `MAP:188` (NARROWED 2026-09-18): "`classes.tsv` carries **1,739** `Phyre::` names today (the 1,604 above predates the AS-9a recount)".
- **Favoured: 2,248 total** (dated 2026-09-08, `CDMS:203-204`) and **1,739 Phyre** (dated 2026-09-18, `MAP:188`). `MAP:58`, the namespace table `MAP:63-87` and `CDMS:489` are stale.

**C-V4. Classes directly in `Phyre::`: 50 vs 62.**
- "| *(directly in `Phyre::`)* | 50 | 50 |" (`MAP:87`)
- "`@Phyre@@` with no sub-namespace**, which is 62 names. The map's 50 used a different counting rule, not reproduced here." (`MAP:202`)
- No favoured side (the page names the conflict and does not reconcile it).

#### Application boundary, module registry and frame

**C-V5. Frame-tick return codes: 0 / 1 / 9 vs 0 / 9.**
- "                       -> FUN_0017D6E0(frameTime, mode) -> 0 / 1 / 9" (`APP:305`, call-chain block, unstruck)
- "*(Corrected 2026-09-14, FABLE: the comment here read "returns 0, 1 or 9". The tick returns only **0** or **9**" (`APP:136`); "**the premise was wrong: there is no 1**" (`APP:406`)
- **Favoured: 0 / 9**, dated 2026-09-14.

**C-V6. Per-frame slot order: slot 4 before slot 7, vs slot 7 before slot 4.**
- `APP:302-307`: "-> per frame:" / "slot 4  GameApplication : FRAME TICK" … "slot 7  GameApplication : input pump" / "slot 6  GameApplication : pre-step"; slot 8 "at a rate THIS DOCUMENT DOES NOT ESTABLISH" (`APP:308-309`).
- "slot 7 (input, `0079C26B`), slot 4 (animate, `0079C2D6`), slot 9 again after a screen-mode change (`0079C526`), each" / "viewport's render (`0079C5FE`) and slot 8 (render, `0079C655`)." (`APP:434-435`, the PA-5 reading of slot 28)
- **Favoured: 7 → 4 → 9 → viewports → 8**, by the PA-5 answer (2026-09-14/26, `APP:431-452`). Whether slot 6 runs per frame is not settled by either side.

**C-V7. Slots 22 and 25: inherited vs overridden.**
- "**The 145 CFG guard adapters.** Slot 22 and 25 inherit `0016D6A0`, which is the CFG check" (`APP:331`)
- "slot 22  OVERRIDDEN  0017D170                              (Phyre: 0016D6A0 empty)" (`APP:262`); "slot 25  OVERRIDDEN  0017D1E0" (`APP:265`)
- No favoured side by date (the slot table and the "18 overridden" count support "overridden").

**C-V8. The shutdown walker: run only from `atexit`, vs also called directly at teardown.**
- "**registers `005A0840` with `atexit`** (`lea rcx, [rip-0x287]` at `005A0AC0`, then" / "`call 00808B90`) — so the shutdown walk runs at process exit, not from game code." (`MOD:214-215`)
- "(`SteamAPI_UnregisterCallback`), then calls `CoUninitialize` and the module shutdown walker `005A0840`." (`APP:513`)
- No favoured side. (The guard flag `0x02CACCA0`, `MOD:212`, may make the second call a no-op; neither page says which call does the work.)

**C-V9. `006388C0` return value.**
- "(`0067F700`), returning `0x12` on a duplicate insert." (`MOD:262`)
- "Returns `sete` — true when the interned lookup/call succeeded." (`APP:667`)
- No favoured side.

**C-V10. The base-vtable installer column: constructors vs destructors.**
- "Which is ctor-versus-base-ctor and which is ctor-versus-dtor is" / "**not** established, and the column is headed accordingly." (`MOD:124-125`); evidence row "| **Those fifteen are constructors, not destructors** | **not established** —" (`MOD:460`)
- "**A side result settles the ⚠ above.**" … "So the `008Axxxx`–`008Cxxxx` column is the destructor column, registered for process exit." (`MOD:419-424`)
- **Favoured: destructors**, by the 2026-09-14 answer block (`MOD:393-424`). Order matters: these run at exit, not start-up.

**C-V11. `PUtilityDynamicGeometry` registrar address: `00617810` vs `00167810`.**
- "21 no-arg inits (including `00617810`, the `PUtilityDynamicGeometry` registrar of the §2 table)" (`MOD:253`)
- "| `01F2EE60` | `PDynamicGeometry::PUtilityDynamicGeometry` | `00167810` | `008B6A40` |" (`MOD:137`)
- No dated correction; `MOD:137` and `Subsystem-Map/members/phyre-module-utility-registrars.tsv` both give `00167810`, so `00617810` looks like a digit transposition.

**C-V12. Module family member counts: body table vs front matter.**
- Body: "claims the **203 frontier" / "entries" (`MOD:272-273`) for PAnimation; "**477 members**" (`MOD:312`) for PhyreCore; "| `PPhysics` | 95 |" and "| `PRendering` | 306 |" (`MOD:344-345`), with the rest of the table at `MOD:346-358`.
- Front matter: "../members/phyre-pphysics.tsv | 134 |" (`MOD:30`), "../members/phyre-prendering.tsv | 310 |" (`MOD:31`), PAnimation 238, PhyreCore 426 (`MOD:28-29`); the member `.tsv` files carry the front-matter counts.
- **Favoured: the front matter**, by its dated per-row deltas (2026-09-17 … 2026-09-30, `MOD:28-45`). Two front-matter chains do not close on their own (PPostProcessing and PScripting), so the exact deltas are also open.

**C-V13. Address of the `0xE0`-byte object the init walk allocates: `01F3F5B8` vs `01F7F5B8`.**
- "**Init allocates a `0xE0`-byte object at `01F3F5B8`**" (`MOD:213`)
- "ctor for the `0xE0` object the root stores at `01F7F5B8`" (`MOD:250`); "drain the `[01F7F5B8]` list" (`MOD:548`)
- No dated correction; two of three lines say `01F7F5B8`.

**C-V14. Thread procedures in the image: nine vs thirteen.**
- "none of the" / "image's **nine** thread procedures is a plausible consumer of a graphics command stream (the" / "largest is 555 B, and the enumeration is complete — five `CreateThread` and four `_beginthreadex`" (`FRM:218-220`); also `FRM:829-830`, `FRM:1041`.
- "**Premise corrected 2026-09-12 (FABLE)" … the engine's own thread API `008636E0` creates four more threads … "the claim stands on thirteen procedures, not nine (CG-3)" (`FRM:971`)
- **Favoured: thirteen**, dated 2026-09-12.

**C-V15. `003A2090`: GIFtag "begin subpacket" (AND) vs freelist push (OR).**
- "| `003A2090` | begin subpacket | 39 B | writes the GIFtag, masks `NLOOP` to zero |" (`FRM:482`); "hdr->dword0        &= 0x8000;                     // keep bit 15, clear bits 0-14" (`FRM:554`)
- "`003A2090` (39 B) is the intrusive 16-byte-element freelist push" … "or [head], 0x8000` flag — the queue push" (`FRM:1249-1251`)
- No favoured side. An AND-mask and an OR-set of bit 15 produce different headers.

**C-V16. Command-buffer index global: `02EBEFF0` vs `02F8EFF0`.**
- "*(u32*)0x02EBEFF0 = 0;                        // current index" (`FRM:286`); also `FRM:327`, `FRM:519`
- "the flip is `eax = 1 - dword [02F8EFF0]` stored back" (`FRM:1186`)
- No dated correction; every other mention uses `02EBEFF0`.

**C-V17. Callers of `003A1DB0`: 38 vs 17.**
- "+-> (via 003A1DB0, from 38 call sites across the engine)" (`FRM:750`); "it has 38 callers" (`FRM:778`)
- "`003A1DB0` — 84 B, 17 A-measured callers at census" (`FRM:1185`)
- No favoured side (call sites vs callers is not stated).

**C-V18. Sites where the settle spin is inlined: 10, 9 or 11.**
- "inlined at the" / "top of every mode body — `0022A850`, `0022AE50`, `0022AFA0`, `0022B040`, `0022B2C0`, `0022B720`, `0022B820`," / "`0022BAD0`, `0022BD20` — and once more at `00262AE0`." (`FRM:268-270`), ten in all
- "inlined spin at `0022BAD0` and its eight siblings" (`FRM:810`), nine
- "raw disassembly at `0022BAD0` (inside `0022B8C0`) and `0022B2C0` (inside `0022B0B0`); displacement census locates nine more" (`FRM:974`), eleven; and `0022B2C0` is inside `MainLoop_Draw`, not a mode body.
- No favoured side.

**C-V19. Mode 3 and the world tick.**
- "mode 3 does not advance the world." (`FRM:816`)
- "`World_UpdateSimulationTick` (`00314020`), reached from mode 3 as well as mode 2, so \"the menu" / "is open\" is not by itself a reason to expect the simulation to be stopped" (`FRM:817-818`)
- No favoured side (same bullet).

**C-V20. Which passes each mask bit gates: pass list vs bit table.**
- Pass list `FRM:380-401` (e.g. bit 3 "`00252A70`  (or 00251010 on the alternate path)", `FRM:398`; bit 6 "`00332420(1)`", `FRM:386`).
- Bit table `FRM:664-674` (bit 3 "`00252A70` / `0017FD70` / `002450B0`", `FRM:669`; bit 6 "`00332420(3)`, `00332420(0)`, `00332420(1)`", `FRM:672`; bit 0 adds `0036F410` … `00475390`, `FRM:666`).
- No favoured side.

**C-V21. "AO render" and "Water effect": gates and order.**
- "\"AO render\"             <- only if 0017FE10() != 0" / "bit 4   VFXSystem_RenderLayerPass(3), EffectSystem_...ForPass(3)" / "\"Water effect\"          <- only if 0017FE20() != 0" (`FRM:389-391`)
- "`00229F20` | 110 B | when dword `01FD49E8` is non-zero: marks `\"AO render\"` … when it is still non-zero and the argument is non-zero, marks `\"Water effect\"`" (`FRM:1519`), with no VFX pass between them and different gate globals.
- No favoured side.

**C-V22. Who passes the 512×448 viewport.**
- "The field frame calls it as `00184460(0, 0, *(u32*)0x01E0C1D8, *(u32*)0x01E0C1DC, 1)`" (`FRM:717`)
- "the call site in `0022B8C0` passes the globals `01E0C1D8`/`01E0C1DC`" (`FRM:983`); `0022B8C0` is mode 3, "**the full-menu frame**" (`FRM:470`/`FRM:124`)
- No favoured side.

**C-V23. Camera command record size and second block: 140 vs 144 bytes, 60 vs 64 bytes.**
- "**It fills a 140-byte record from two sources and nothing else.**" (`CAM:37`); "**`+0x48 … +0x84`** — 60 bytes" (`CAM:41`)
- "The highest field written is `+0x8C`, a dword — **`0x90` total from the base.**" (`CAM:98`); "allocates `0x90` bytes" (`CAM:116`); "`+0x48`..`+0x87` is handed to one call" (`CAM:125`)
- **Favoured: 0x90 = 144 bytes, second block 64 bytes (a mat4)**, by the layout read 2026-09-30 (`CAM:115-166`).

#### Asset container

**C-V24. `PInstanceListHeader` field count: 10 vs 9.**
- "| `00598DF0` | registers the 10 `PInstanceListHeader` fields — interior verified 2026-09-17 … ×9 each — a nine-element registration battery" (`HDR:256`)
- "**nine** `unsigned int` fields — so the instance-list" / "header is **36 bytes**" (`HDR:102-103`); "**Corrected 2026-09-07 (same day, audit pass).** This table first listed a tenth field," (`HDR:117`)
- **Favoured: nine fields, 36 bytes**, dated 2026-09-07; the key-address row still says 10.

**C-V25. Where the oversized header is copied: `r9` (second buffer) vs `nsBuf`.**
- "| `r9` | **a SECOND buffer of the same shape as `r8`, and a stack local in that one caller** — … Its `+0x08` is where the oversized path copies the 84 bytes (`0059A52E mov rdx, [r12+8]`)." (`C-HDR:57`)
- "if (!grow(nsBuf, size)) return 0xD;" / "memcpy(nsBuf->p, h, 84);                  /* 5 x movups + 1 dword */" (`C-HDR:346-347`), in a formula whose signature has no `r9` (`C-HDR:298-299`)
- **Favoured: `r9`**, by PH-5 (2026-09-15, `C-HDR:575-592`) and §13a (2026-09-18, `C-HDR:458`).

**C-V26. `0059A3B0` argument order: §2 vs the §12 formula.**
- "`int Read(Stream *rcx, ClusterHeader *rdx, NsBuffer *r8, Buffer *r9, bool *outWasByteSwapped [rsp+0x28], uint32 *outSize [rsp+0x30], bool checkPlatform [rsp+0x38])`" (`C-HDR:55`)
- "int PhyreClusterHeader_Read(Stream *s, ClusterHeader *h, Buf *nsBuf," / "bool checkPlatform, uint32 *outSize, bool *outSwapped)" (`C-HDR:298-299`)
- **Favoured: §2**, by §13a (2026-09-18, `C-HDR:436-438`).

**C-V27. Packed-namespace reader argument order.**
- "`int Read(Stream *rcx, bool wasByteSwapped dl, void *buffer r8, uint32 len r9d)`" (`C-NS:53`)
- "return ReadPackedNamespace(s, nsBuf->p + take," / "h->m_packedNamespaceSize - take, *outSwapped);" (`C-HDR:342-343`), i.e. buffer, length, flag
- No favoured side by date (the register-level form is the more specific).

**C-V28. Is a zero-length namespace accepted when the capacity already reads zero?**
- "a *zero-length* namespace is refused, while a zero-length namespace whose capacity already reads zero is accepted, because the second never replaces the buffer." (`C-HDR:286`)
- "if (!nsBuf->data) return 6;                   /* 0059A4D3 -> 0059A598 */" (`C-HDR:329`); "and for a **null `nsRec.buf` regardless of namespace length**: the" / "`test r13, r13` at `0059A4D3` precedes the length paths" (`C-HDR:470-471`, §13a, 2026-09-18). The only caller zeroes the buffer before the call (`C-HDR:579-581`).
- No explicit correction; §13a is the later dated text.

**C-V29. Rejection causes and codes: "Four rejections, three distinct codes" vs "Five distinct causes share the code `6`".**
- "**Four rejections, three distinct codes: `6` refuse, `9` truncated, `0xD` allocation failed.**" (`HDR:146`)
- "**Five distinct causes share the code `6`,**" (`C-HDR:286`), within a nine-row return table (`C-HDR:274-284`); plus the BOM refusal `6` at `0059E295` (`C-NS:387`) and `0x13` from the user-fixup loader (`HDR:716`).
- No dated correction on `HDR`; the contract (2026-09-12, pilot-driven) is the fuller list.

**C-V30. Are the platform and physics id leaves called when the check is off?**
- "if (checkPlatform && hdr->m_platformID != GetPlatformID())        return 6;   /* 0x44583131 */" (`HDR:138`), a short-circuit form
- "**Both leaves are called even when `checkPlatform` is false.** Only the comparisons are guarded, so" (`C-HDR:222`)
- **Favoured: called either way**, by the contract's re-read (2026-09-12, `C-HDR:226`).

**C-V31. Oversized-header copy: "21 dwords" vs SSE, five vs ten `movups`.**
- "copied in as 21 dwords" (`HDR:199`)
- "five `movups` of 16" / "bytes plus one 4-byte `mov`" (`C-HDR:260-261`); formula comment "5 x movups + 1 dword" (`C-HDR:347`)
- "**Ten `movups`, forming five 16-byte transfers**" (`C-HDR:682`, §15a)
- **Favoured: ten `movups` (five 16-byte load/store pairs) plus one dword, inline**, by §15a (2026-09-12).

**C-V32. The second header swap.**
- "**If the file was byte-swapped, the header is swapped *back*** before either path runs." (`HDR:200`)
- "**The size the loader uses is the swapped one.** For a big-endian file, `m_size` is published" / "and compared from the *swapped* header; swapping the header back afterwards does not revise it." (`C-HDR:242-243`)
- **Favoured: the contract**, by its "CORRECTED 2026-09-12" block (`C-HDR:226`).

**C-V33. `bswap`s in the namespace header swap: fourteen vs eight.**
- "**fourteen `bswap`s over eight fixed dwords," (`C-HDR:168`); "fourteen" / "`bswap`s over eight fixed dwords at `+0x00`…`+0x1C`" (`C-HDR:571-572`, 2026-09-18)
- "**eight `bswap`s, one per fixed dword** (*\"fourteen\" corrected 2026-09-25, OPUS - counted at `0059C18B`...`0059C1C2`*)" (`C-NS:172`)
- **Favoured: eight**, dated 2026-09-25; the cluster-header contract was not updated.

**C-V34. Class-record swap: "nine words … the rest `bswap`" vs "only five … use `bswap`".**
- "swapping **nine** words per record; the first is an inlined byte-reversal, the rest `bswap`" (`C-NS:174`)
- "But only **five** of the nine use the `bswap`" / "instruction. The other four — `-0x2c`, `-0x1c`, `-0x18`, `-0x14` — are **open-coded**:" (`C-NS:457-458`)
- No dated correction (§15a is the later read). The bytes produced are the same; the description differs.

**C-V35. Which `w7` bit marks a header class.**
- "class\" is a class whose namespace record carries **bit 4 of class word `w7`** — in this title" / "exactly three: `PParameterBuffer` (`w7` = 12), `PAnimationClipBinding` and" / "`PModifierNetworkInfoPacket` (`w7` = 20)" (`HDR:299-301`); 12 has no bit 4 (0x10).
- "abstract, `0x04` header, `0x08` no default constructor.** Bit `0x10` is set exactly on the two `Header`" / "classes in the corpus" (`C-NS:354-355`, NS-1 answered 2026-09-26)
- "bits 1–5 stay" / "unexplained." (`NS:276-277`, a 2026-09-30 note)
- **Favoured: `0x04` = header**, by NS-1 (2026-09-26, `C-NS:349`). The later-dated `NS:276-277` is stale despite its date.

**C-V36. Member attribute bit 31 as "the pointer bit".**
- "PString               1   m_buffer +0        (attribute 0x80000010 - the pointer bit)" (`NS:586`); "**`m_buffer` is the only field in the file with attribute bit 31 set, and it is the one field that is" / "a pointer**" (`NS:593-594`)
- "**An object pointer carries bit 1, not bit 31.**" … "A walker that tested bit 31 would treat `m_effectVariant`, `m_mesh` and `m_asset` as inline values." (`NS:515-518`)
- **Favoured: bit 1**, by the 2026-09-26 correction block (`NS:497-518`).

**C-V37. The two teardown helpers' count/pointer pairs overlap.**
- "walks the `+0x38/+0x40`, `+0x28/+0x30`, `+0x18/+0x20`, `+0x08/+0x10` count/pointer pairs" (`NS:638`)
- "`+0x50/+0x58`, `+0x40/+0x48` …, `+0x30/+0x38`, `+0x20/+0x28`" (`NS:642`): `+0x38` and `+0x40` are a count in one helper and a pointer in the other.
- No favoured side.

**C-V38. Mesh clusters in the archive: 2,097 vs 2,091.**
- "6 meshes against 2,097 in the archive" (`HDR:239`)
- "**2,091** meshes (index + vertex, no texture)" (`HDR:233`, CU-4 2026-09-12); `members/user-fixup-census.tsv` sums to 2,091.
- **Favoured: 2,091**, dated 2026-09-12.

**C-V39. Field names the registration misses: 85 vs 87.**
- "the schema misses 85 of the 349 field names the files declare." (`NS:203`, 2026-09-26)
- "**138 of 177 classes and 262 of 349 field names are in the recovered" / "registration**" (`NS:321-322`, 2026-09-12): 349 − 262 = 87.
- No favoured side.

**C-V40. Call sites of `0059A6F0` inside `0059A3B0`: 2 vs 3.**
- "| `0059A6F0` is called from the header validator | **stands** — 2 sites, matching the fast path and the version-shim path. |" (`NS:626`)
- "| the three size paths converge on `0059A6F0` | **re-read**: `0059A5BF`, `0059A5D7` and the equal path all call it |" (`C-HDR:630`)
- No favoured side (whether "the equal path" is its own site is not stated).

**C-V41. The three D3D11 header sizes: GPU reservation vs error-field propagation.**
- "**The three D3D11 sizes tell the loader how much GPU memory to reserve.**" (`HDR:277`)
- "`00686D10` (43 B) is the three-field status copy `0059E300` runs: when `r8`'s `+0x48`/`+0x4C`/ `+0x50` are not all zero it writes them to `rcx`'s `+0x20`/`+0x1C` and conditionally `+0x24` - the loader's error-field propagation." (`C-HDR:936-943`)
- No favoured side.

#### Reflection

**C-V42. Descriptor offsets as qword indices, left unstruck after the unit correction.**
- "| `+0x0C` | `FUN_006b6700` | embedded string (the class name) |" (`CDMS:150`) … "| `+0x1D` | compared to `DAT_02CF8260` | a generation / registration counter |" (`CDMS:156`); "+0x0C   str    embedded string (class name)" (`CDMS:255`, §4 block `CDMS:253-261`); "| `02CF8260` | global compared against descriptor `+0x1D` | — |" (`CDMS:246`)
- "**Unit correction 2026-09-02 — the offsets in this block and in §4 are qword indices, not byte" / "offsets.**" (`CDMS:160-161`): bytes `+0x80/+0x90/+0xA0/+0xB0`, sub-object `+0x70`, counter `+0xE8`, name `char *` at `+0x30` (`CDMS:162-172`; `C-CD:81`).
- **Favoured: byte offsets**, dated 2026-09-02. A reader of the §2 table or the §4 block alone gets every descriptor offset wrong by a factor of 8.

**C-V43. "Embedded string" (the name) vs list-unlink.**
- "FUN_006b6700(self + 7);                       // destroy an embedded string (the name)" (`CDMS:131`); "+0x38   str    embedded string (member name)" (`CDMS:267`); evidence row `CDMS:485`.
- "**clear the intrusive list at `+0x38` through `006B6700`**" (`CDMS:1284`); "**⚠ Corrected 2026-09-14 (OPUS), pass 13 — independent re-derivation.** `006B6700` is a list-unlink" (`CDMS:1286`)
- **Favoured: list-unlink, no string**, dated 2026-09-14; the name is a pointer at member `+0x20` (`CDMS:423`; `MR:638-651`).

**C-V44. `PClassDataMember` teardown: which offset is freed and which bit is tested.**
- "+0x28   flags  bit 0 tested during teardown" (`CDMS:266`)
- "and conditionally free `[+0x18]` when `[+0x20] & 1`." (`CDMS:1284`), while `MR:638-651` puts the owner at `+0x18` and the name at `+0x20`.
- No favoured side on the page. `C-CD:456-457` implies the `CDMS:1284` offsets are relative to the node at member `+8` (so member `+0x20`/`+0x28`), but neither line says so.

**C-V45. `FieldStorageWidth`: a literal 8 vs `ctx->vslot08()`.**
- "returns 8 when attribute bit 1 is set, else the type's inline size from `type+0x38`" (`MR:582`); "storage size of literally 8 when this bit is set" (`MR:669`); "returns literally `8` when bit 1 is set" (`MR:916`); `MR:1383` (same wording).
- "**Corrected 2026-09-19 (OPUS).** The earlier transcription of this body said `return /* pointer" / "width */ 8`" (`MR:406-407`): the width is `ctx->vslot08()` (`MR:408-410`).
- **Favoured: `ctx->vslot08()`**, dated 2026-09-19; four unstruck restatements remain.

**C-V46. `classdesc+0xF4`: zero vs not zero.**
- "`descriptor+0xF4`/`+0xF8` are the offset adjustments, both zero (§12)." (`MR:1674`); §12's "The recorded offsets are true in-instance offsets" (`MR:1429-1443`)
- "## 16. CORRECTION — `classdesc+0xF4` is **not** zero (2026-09-19, OPUS, same day)" (`MR:1676`): 0 for 126 classes, 8 for 27, unresolved for 26 (`MR:1714-1716`).
- **Favoured: not zero**, by §16/§17 (2026-09-19). A port that ignores `+0xF4` mis-addresses every field of 27 classes by 8 bytes (`MR:1781`).

**C-V47. Meaning of `+0xF8`.**
- "int used       = *(int *)(cls + 0xF8);" (`MR:361`, `AttachMember` reading)
- "and `+0xF8` as the same sum with each term clamped at zero." (`MR:1751`, §17)
- No favoured side (the `AttachMember` reading was not revisited).

**C-V48. Descriptor size: ~0x110 vs 0x100 (vs "at least 0x140").**
- "Descriptors are about" / "0x110 bytes and packed in `.data`" (`MR:296-297`)
- "The descriptor is 0x100 bytes." (`IS:87`); base 0x100 and `PClassDescriptorDynamic` 0x140 (`C-CD:66-73`, `C-CD:488-494`)
- "| size | **at least `0x140`** — `0063D550` writes `+0x138` and `+0x104`; the exact end is not established (§14) |" (`C-CD:52`)
- **Favoured: 0x100 (base) / 0x140 (Dynamic)**, by PCD-3 answered 2026-09-25 (`C-CD:488-494`); `MR:296` and `C-CD:52` are stale.

**C-V49. `PClassDataMember` layout in the interior citation vs §4.**
- "`00D580B0` installs at `006329B6`, `+0x48`/`+0x50` take the name and context args, `+0x28` bit 1" (`MR:1366`)
- "record[0x30] = memberType;" (`MR:623`); "*(uint32_t *)&record[0x48] = offset;" (`MR:626`); "record[0x50] = 0;" (`MR:627`)
- No dated ruling (§4 is the full body reading).

**C-V50. Field-record count: 682 vs 684 vs 686, over 246 / 182 / 180 / 179 classes.**
- "There are **682 such call sites** in the binary. **680 of them resolve completely**" (`MR:78`); "**680 fully-resolved field records over 246 classes**," (`MR:30`)
- "registered members                                  684 across 182 classes" (`MR:1876`, §18a, 2026-09-22)
- "The schema recovered here is 682 members over 180 classes," (`MR:1799`)
- "| **runtime schema** | … | **682 records, 246 class names, 179 distinct leaves** |" (`FS:61`); "the 179 leaf names in" (`IS:162`)
- `phyre-field-schema.tsv` has **686** data rows, 246 distinct `class`, **182** distinct `class_leaf` (checked for this report).
- No favoured side. §20 (2026-09-27) says four `00632A70` sites were added (`MR:2291`), which would explain 686 = 682 + 4, but no page states the new total.

**C-V51. Attribute-word census: `0x00` 196 vs 200.**
- "0x00 196     0x02  36     0x08 123     0x0A  39     0x10 207     0x12  79" (`MR:658`)
- `phyre-field-schema.tsv` now has `0x00` 200 (the other values match). No favoured side.

**C-V52. Classes whose fields carry constant bits 3-4: 146 of 146 vs 243 of 246; coherence over 164 classes.**
- "constant across every field of a class in **146 of 146** classes" (`MR:910`); "struct-layout coherence across 164 classes" (`MR:905`)
- "-> constant across every field of the class in 243 of 246 classes;" (`MR:672`)
- **Favoured: 243 of 246** (the second-pass figures, explained in §10, `MR:1049-1052`); the §8 evidence rows are stale.

**C-V53. Classes that fit their size exactly: 33 vs 15.**
- "* Sharpness: **33 classes fit exactly**" (`IS:101`); the `.tsv` has 33 rows with slack 0.
- "the 177 independently derived Phyre reflection member rows all fit inside their" / "stated sizes, and 15 sum exactly" (`IS:218-219`)
- No favoured side.

**C-V54. When array members are built: static initialisation vs lazily on first use.**
- "class-descriptor initialisers (static init)" (`AR:351`); "the member descriptors are built by code at static initialisation." (`AR:366`)
- "**680 of the 682 member registrations execute lazily**, behind a one-time-init guard," / "the first time the class is touched." (`MR:968-969`), in MR's "Correction to a sibling document" (`MR:963-971`)
- **Favoured: lazy** for the `00632960` members (`MR:963-971`). Whether the 165 array registrations (`00632A10`) are also behind the guard is not stated on `AR`.

**C-V55. The eleven `006349B0` teardown thunks: 103 vs 96 bytes.**
- "**What each member does.** All eleven are 103 bytes with the same shape." (`AR:414`)
- "same 96-byte `PClassDataMember` teardown shape" (`MR:1333`)
- No favoured side.

**C-V56. The lazy-static accessors: one `0x50`-stride array, and zero-initialised.**
- "each returns a distinct element of **one `0x50`-stride" / "array** at `01F2E330`…`01F2E780`." (`AR:183-184`); "The objects are zero-initialised and only" / "their teardown is generated" (`AR:186-187`)
- "*Answered 2026-09-14 (FABLE): thirteen of the fifteen elements are Phyre type objects, and they are **not**" (`AR:189`, not zero-initialised); "from `01F2E780` up the objects do not follow that stride - `01F2E780` is 0x30 bytes" (`AR:296`, 2026-09-30)
- **Favoured: not zero-initialised (2026-09-14) and no uniform stride above `01F2E780` (2026-09-30).**

**C-V57. `PClassDescriptorConcrete` static initialisers: 254, 255 or 227.**
- front-matter family row "| 254 |" (`CDMS:29`); "| `PClassDescriptorConcrete.StaticInitializer` | **255** | ~~227~~ | — |" (`CDMS:192`)
- "-> PClassDescriptorConcrete<T> static initializer      (227 of these)" (`CDMS:296`, unstruck)
- No favoured side between 254 and 255 (the `.tsv` has 254 rows); 227 is struck at `CDMS:192` but not at `CDMS:296`.

**C-V58. §5 call chain repeats superseded teardown counts.**
- "-> ClassDescriptorStaticTeardown       (372)" / "-> DataMemberMetadataStaticTeardown    (830)" (`CDMS:308-309`)
- "| `DataMemberMetadataStaticTeardown` | **853** | ~~830~~ |" / "| `ClassDescriptorStaticTeardown` | **404** | ~~372~~ |" (`CDMS:188-189`)
- **Favoured: 853 / 404**, dated 2026-09-02 (`CDMS:182`); the `.tsv` files agree.

**C-V59. Traversal adapter: descriptor vtable slot 0 vs the push adapter at `+0x20`.**
- "Of the 331 `Concrete<T>` vtables, 243 have one of the 298" / "traversal adapters as slot 0" (`CDMS:443-444`)
- "| `+0x20` | **315** | the class's **script-VM object push adapter** — … (21 B ×194, 31 B ×115) is that family's own documented split of 188 and 116 |" (`CDMS:1013`)
- No favoured side (slot, sizes 46/75 B vs 21/31 B, and the 194/115 vs 188/116 split all differ).

**C-V60. The vftable written at destructor entry.**
- "| `+0x00` | 8 | vftable. The destructor overwrites it with `PType`'s before releasing anything |" (`C-CD:80`)
- "it assigns `Phyre::PClassDescriptor::vftable` on entry" / "and `Phyre::PType::vftable` on exit" (`CDMS:87-88`); "(`00D581C0` at `006333BC`, `00D31168` at `00633568`), so the object passes through two vtable" / "identities" (`C-CD:197-198`)
- No dated ruling; the instruction addresses on `C-CD:197` favour entry = `PClassDescriptor`, exit = `PType`.

**C-V61. `+0xC8` / `+0xD0`: full-size instances vs byte masks.**
- "| `+0xC8` | 8 | **a second full-size instance**," / "| `+0xD0` | 8 | **a third full-size instance**," (`C-CD:92-93`); "| `+0xD0` | a third buffer registered by the same family; **no reader identified** |" (`CDMS:1146`)
- "**Purpose read 2026-09-25 (FABLE, Claude Opus 5.5): `+0xC8` and `+0xD0` are byte masks over the instance, not" (`C-CD:689`)
- **Favoured: byte masks**, dated 2026-09-25 (`CDMS:715-722` still uses `+0xC8` as a construction target inside `00639A60`; that dual use is not reconciled).

**C-V62. Does `+0x50` return false everywhere, so `0063CB80` always builds?**
- "`+0x50` returns **false on every class measured**, so `00639A60` always hands off to `0063CB80`" (`CDMS:901`); also `CDMS:844-845`, `CDMS:1071-1072`.
- "**WITHDRAWN 2026-09-25 (OPUS): all three arms below are ARMED.**" (`CDMS:861`); "`0063CB80` builds only where `+0x50` returns false or flags bit 0" / "is set.**" (`CDMS:1038-1039`)
- **Favoured: conditional**, dated 2026-09-25.

**C-V63. Registry insert when the parent is in another registry: head vs append.**
- "otherwise it is linked at the **head** of the" / "registry's list (`0063922E`–`00639244`)." (`CDMS:392-393`)
- "else appending `rdi+0x50` into `[rbx+0x10]`'s list (`006391FF`..`00639244`" (`CDMS:1730`); "and appends it otherwise" (`C-CD:444`)
- No favoured side by date (`CDMS:1730` is dated "2026-05-15", earlier than the rest); two of three statements say "append".

**C-V64. Identity of `00632C90`: a scalar-deleting destructor vs a descriptor constructor.**
- "**00632C90** (66 B; heads the ICF-folded cluster of identical scalar-deleting destructors" … "— `??_G` scalar-deleting destructor for the class whose vtable is **00D30168**" (`CDMS:1726`)
- "`00632C90` takes no parent argument and writes `mov qword ptr [rcx + 0x78], r10`" (`C-CD:868-869`); "`00632C90` 226 B, 4 registrars" (`IS:133-134`)
- No favoured side by date; the sizes (66 B vs 226 B) disagree as well.

**C-V65. PSharray / PArray instantiation counts.**
- "`PArray` (66 instantiations) and `PSharray`" / "(9)." (`FS:70-71`)
- "~~All nine `PSharray<T>` descriptors fit that: …~~ **All TEN" (`MR:2348`, 2026-09-28)
- **Favoured for `PSharray`: ten descriptors**, dated 2026-09-28 (`FS` may count schema names, not descriptors; the page does not say).

**C-V66. Class-descriptor globals the schema names: 246 vs 249.**
- "The 246 descriptors span `02CA9DA0`–`02EBA030`" … "All 249 class-descriptor globals the current field schema names are there," (`FS:171`, the second half anchored 2026-09-30)
- **Favoured: 249**, dated 2026-09-30; `class_obj` in the `.tsv` has 249 distinct values.

#### Script bridge

**C-V67. Lua standard-library address range.**
- "**It bounds the standard library**: the named functions span `00814xxx`–`0081Cxxx`, which is where" (`LUA:838`)
- "*exact link range 2026-09-13 (FABLE):* every census entry from `0080F2E0` up to `00830760`" (`LUA:435`)
- **Favoured: `0080F2E0`–`00830760`**, dated 2026-09-13.

**C-V68. Lua function counts: 111 / 90 / 108 / 143.**
- "Lua 5.2.1, **111 functions**, per" (`LUA:1085`); "Across the whole 90-function `ThirdParty.Scripting.Lua` domain" (`LUA:479`); "0x80F000 - 0x812FFF :  108 functions,  6 tagged Lua,  102 generic  (94%)" (`LUA:476`); "**148 records matched; 145 of them fall in 12 arrays; 143 distinct functions are named.**" (`LUA:669`)
- No favoured side (different measures, never reconciled).

**C-V69. `luaopen_*` references: "only" the table entry vs also a `lea` in `00685AC0`.**
- "Each open function's **only** reference in" / "the image is its table entry (one 8-byte hit each; `luaopen_string` two)" (`LUA:375-376`, R-4 2026-09-12)
- "Its only" / "references are its `lea` in `00685AC0` (`00685ADD`, `00685AF0`, `00685B03`, `00685B16`) and its" (`LUA:958-959`, UQ-284 2026-09-25)
- **Favoured: table entry plus the `lea`**, dated 2026-09-25.

**C-V70. `PScheduler` / `PAsyncProcessBuffer` constructor columns.**
- "| `PScripting::PAsyncProcessBuffer` | `00D6FD50` | `00681560`, `00681720` |" / "| `PScripting::PScheduler` | `00D6FD68` | `00681560`, `00681880` |" (`LUA:1094-1095`)
- "`00681560`, which stamps it into `this` … — the constructor —" / "and `00681880`, which stamps it and frees — the destructor." (`LUA:389-390`, 2026-09-22); "`00681720` (166 B) is a call-free intrusive-list unlink" (`LUA:1165`)
- **Favoured: `00681560` = `PScheduler` ctor, `00681880` = its destructor, `00681720` = a list unlink**, by the later dated sections.

**C-V71. What `02E41570` is.**
- "The sixth `0x100` slot `02E41570` belongs to a class none of the five registers and is outside this question" (`LUA:929`, 2026-09-18)
- "a `u32` count" / "with bit 31 as a flag at **`02E41570`**, and the 16-byte-entry buffer pointer at **`02E41578`**." (`LUA:939-940`, 2026-09-25)
- **Favoured: the list count**, dated 2026-09-25.

**C-V72. "Nearly every binding" funnels through one routine.**
- "**Nearly every one of the 1,219 bindings funnels through this one routine.**" (`LUA:166`)
- "reach it through jump thunks**, for **841 in total**." (`LUA:163`); the 588 accessors call `00682980` and do not push (`LUA:293-298`).
- No favoured side.

**C-V73. Argument order of the shared push.**
- "void FUN_005a0e80(L, obj, ctx) { thunk_FUN_00682d20(obj, ctx, &DAT_02cad640); return; }" (`LUA:148`)
- "`00682D20(L, obj, descriptor)`, read in full (112 B)" (`LUA:342`, R-2 2026-09-14)
- **Favoured: `(L, obj, descriptor)`**, dated 2026-09-14.

**C-V74. The push adapters' `+8`: base-class adjustment vs member offset.**
- "The `+ 8` in the middle variant is a **base-class this-pointer adjustment**, which is what a" (`LUA:167`)
- "add a member offset with a null guard (cmove to 0) and differ ONLY in that offset immediate - 8, 1, 0x30, 0x10" (`ACC:26`)
- No favoured side.

**C-V75. Reference accessors: 265 vs 264.**
- "| reference accessors | 265 | **345** | **0** | 80 |" (`ACC:307`); `LUA:173`, `LUA:615` also 265.
- "object-reference-accessors.tsv | 264" (`ACC:30`); "| `ObjectReferenceAccessor` | 264 | **2** | **264** |" (`ACC:820`)
- No favoured side. (The `.tsv` header's frontier-only selector, and the absence of `00599770` from it, would explain the difference; no page says so.)

**C-V76. Null path of the optional-pointer adapters.**
- "**Null:** `lua_checkstack(L, 1)` (`0080F420`), then a tail call of `00810620`. That body is Lua's `lua_pushnil`:" (`LUA:359`), "**Non-null:** a tail call of `thunk_FUN_00682d20` (`00684080`)" (`LUA:361`)
- "non-null tail-jumps shared 00810620, else calls 0080F420 with edx=0x19" (`ACC:34`, also `ACC:35-36`)
- No favoured side (either the `00810620` role or the branch sense is wrong for these families).

**C-V77. Role of `0080F420`.**
- "push arg1 onto the optptr stack via shared 0080F420" (`ACC:43`)
- `0080F420` = `lua_checkstack` (`LUA:225`, `LUA:343`, `LUA:359`)
- **Favoured: `lua_checkstack`** (R-3, 2026-09-14).

**C-V78. `00811130` used as a value-returning call.**
- "`00682A10(rcx, -1)` first, then `00811130(rcx, -2)`; a" / "non-null result is returned verbatim" (`ACC:936-937`)
- "**`00811130` is `lua_settop`**" (`ACC:215`), which returns nothing.
- No favoured side.

**C-V79. Is `"PhyreObject"` the only metatable gate?**
- "**`\"PhyreObject\"` in the Lua registry is the gate.** A userdata without that exact metatable" / "is rejected by every accessor." (`LUA:324-325`)
- "`0080FA50(rcx, 0xFFF0B9D8, \"Vector\")` decorates" (`ACC:945`, 2026-09-20), in a helper the accessor vtable rows share (`ACC:935-936`)
- No favoured side.

#### Animation

**C-V80. Kind-2 target: object at `+0x20` vs `+0x28`.**
- "+0x20  ptr  object    kind 2: object whose setter is invoked     [consumer-only]" (`ANI:228`); "case 2: InvokeReflectedSetter(target->obj_0x20, target->ctx_0x18, &value); break;" (`ANI:397`)
- "kind 2 -> 005A7E90(obj @ +0x28 ... ctx @ +0x18)             005C7531" (`ANI:933`)
- **Favoured: `+0x20`**, by BM-6's producer evidence (2026-09-14, `ANI:565-575`).

**C-V81. Shader parameters reached through kinds 2/3 vs kind 1.**
- "and, through kinds 2/3, arbitrary reflected properties including shader parameters." (`ANI:472`)
- "| `PAnimationChannelTargetBindShaderParameter` | `00D31808` | `005C1160` | **1**, dest at `+0x08` (`005C1274`–`005C127A`) |" (`ANI:574`)
- **Favoured: kind 1**, by BM-6 (2026-09-14).

**C-V82. Array element size: type `+0x38` vs member `+0x58`.**
- "elementSize = *(u32 *)(arrayType + 0x38);" (`ANI:277`)
- "beside the element size at `+0x58`" (`ANI:606`); `AR:65-71` (`+0x58` = element size)
- No favoured side (possibly two different objects; neither line says so).

**C-V83. Member `+0x18`: owning class vs name pointer.**
- "offset += (int)member[9] - *(int *)(member[3] + 0xF4);   // member offset - owning class base" (`ANI:271`)
- "copy `00861EBA`, pointer to `+0x18`)" (`ANI:588`, the name copy in the member base initialiser)
- No favoured side (`ANI:588` may be relative to the node at member `+8`, as `C-CD:456-457` implies, but it does not say so).

**C-V84. `005BF290`: bind-time writer vs the per-frame value floats.**
- "Both are written by the bind-time writer `005BF290` (OPUS, 2026-09-14) and never read by the composer." (`ANI:524`)
- "| `+0x00`..`+0x0F` | the four floats | a 16-byte load, source stride `0x58` |" (`ANI:1032`, the same writer); the per-frame evaluation into `ChannelValue` slots (`ANI:455-456`)
- No favoured side.

**C-V85. Functions that reference a `ChannelSemantic` entry: 23 vs the 22 listed.**
- "**Twenty-three functions reference a `ChannelSemantic` entry directly.** They fall into four groups" / "and none of them was on this page." (`ANI:1065-1066`); the four groups at `ANI:1068-1103` list 22, and `ANI:517` reaches 23 only by including `005C72A0`, which is on the page.
- No favoured side.

#### Post-process, post-effects and shader variants

**C-V86. The constant-block bound: `offset ≥ 4` vs `size ≥ 4`.**
- "if (offset >= 4)                             /* must not overwrite the header */" (`PPF:86`)
- "a second test requires `size >= 4`," (`PPF:1536`); "copies `r9w` bytes from" (`PPF:732`, `r9w` the length)
- No favoured side.

**C-V87. Call sites of `001945B0`.**
- "Eleven call sites in `0018D850`–`00190260`." (`PPF:520`)
- `001930F0` (`PPF:252-253`), `00191E90` (`PPF:386`) and `001E2AF0` (`PPF:1533`) also call it, all outside that range.
- No favoured side.

**C-V88. SMAA pass body size: 2,839 B vs ~220 B.**
- "| `001925D0` | 2,839 B | **SMAA** |" (`PPF:67`)
- "`001925D0` (~220 B) — an EH-protected pass body" (`PPF:665`)
- **Favoured: 2,839 B**, re-measured by the 2026-09-13 falsification pass (`PPF:620-621`).

**C-V89. Role of `001EE8E0`.**
- "| `001EE8E0` | 840 B | **colour-buffer copy** |" (`PPF:69`)
- "`001EE8E0` — 840 B, 7 callers; the submit composer that drives the whole ring battery." (`PPF:714`)
- No favoured side.

**C-V90. `00606A20`: teardown vs the variant-key builder.**
- "`00606A20`/" / "`00606C60`/`00600B30` teardown)." (`PPF:243-244`)
- "`00606A20(effect, …)` is the whole key path." (`CTX:400`)
- No dated ruling; `CTX` is tier 1 and reads the body.

**C-V91. `005DC2F0`: array constructor vs `PRenderer` constructor.**
- "`005DC2F0` (267 B) is an array constructor over `eh_vector_constructor_iterator`;" (`PPF:497`)
- "`PRenderer`'s constructor `005DC2F0` is the only installer of its vtable." (`CTX:385`, GD-1 2026-09-26)
- **Favoured: `PRenderer` constructor**, by GD-1 (2026-09-26).

**C-V92. Is the post-process context object a reflected type?**
- "**Declared 2026-09-17 (SWE2-STRUCT):** the object is in the type store as `PostProcessParamContext`" / "(size `0x4A8`, …) with a 145-row field map" (`PPF:399-400`)
- "at any of this object's known offsets — `+0x184` (SMAA quality), `+0x198`, `+0x344`, `+0x2E0` —" / "returns **no rows at all**." (`PPF:1559-1560`)
- No favoured side (two different stores may be meant; the page does not say).

**C-V93. Factory-slot routes: 24 + 11 + 0 = 35 of 36.**
- "Checked for every one" / "of the 36: slot 10 reaches the class's vtable in **24** cases directly and in **11** through a single" / "call to a wrapper that does it, and in **zero** cases not at all." (`PFX:153-155`)
- No favoured side (one class is unaccounted for).

**C-V94. Bodies that install each post-effect vtable: one vs 66.**
- "Each class's vtable is installed by exactly one body, in the `0064xxxx` band," (`PFX:148`)
- "66 bodies stamp the 36 family vtables" (`PFX:856`, falsification pass 2026-09-29)
- **Favoured: 66**, dated 2026-09-29.

**C-V95. D3D11 post-effect classes that add fields: six of seven carry none vs `PMotionBlurD3D11` adds 3.**
- "Six of" / "the seven are that." (`PFX:804-805`)
- "| `00646A30` | `PMotionBlurD3D11` (second body) | 3 |" (`PFX:796`)
- No favoured side.

**C-V96. Does any code construct a post-effect?**
- "**no code constructs one and no shipped asset names one**. The family ships" / "as middleware the game does not use." (`PFX:755-756`)
- "**CORRECTED 2026-09-29 (OPUS, `CON-198`): one class IS constructed by code.**" (`PFX:138`), PFXAA at context `+0x378`.
- **Favoured: PFXAA is constructed**, dated 2026-09-29.

**C-V97. Callers of `0060B980`: 27 vs 58.**
- "the key builder `00606A20` has exactly one caller, the submission body `0060B980`, and *that*" / "has **27**," (`CTX:161-162`)
- "| `0060B980`, the firing control | **58** |" (`PFX:633`)
- No favoured side (functions vs call sites is not stated).

**C-V98. `0018D0E0`: reached only through a data qword vs 52 direct calls.**
- "| vtable-slot members (reached only through a data qword) | 7 | 458 | `0018D0E0`, …" (`CTX:830`)
- "But `0018D0E0`, the 11-byte body that stamps `008C6C80`, has **52** direct call sites, not none." (`PFX:861`, `CON-200`, 2026-09-29)
- **Favoured: 52 direct calls**, dated 2026-09-29.

**C-V99. The eleven `0065xxxx` bodies: material selectors called from slot 1 vs post-effect workers called from slot 6.**
- "| the `0065xxxx` material-selector bodies | 11 | 13,651 | … the class map names three of them `PRendering::PMaterialSelectorMater…" (`CTX:826`)
- the slot-6 override → worker table (`PFX:58-68`); "reached from slot 6 of each class's vtable" (`PPF:459-460`)
- No dated ruling on `CTX:826`; the post-effect page's tier-1 reading of the slot-6 overrides is the more specific.

**C-V100. Light cap: nine (key format) vs four (output record).**
- "With the registered budget of three words that tops out at" / "nine lights." (`CTX:134-135`)
- "and the structure is not a bug but a four-light bound the caller and the callee agree on." (`CTX:337`); "the record is `PLight*[4]` followed by a `u32` count." (`CTX:341`)
- No favoured side (both 2026-09-22; the page does not say which one caps a draw).

**C-V101. Trailing record `+0x38`: the geometry descriptor vs zero.**
- "| 7 | stack | **the trailing record** — `+0x00` the camera (§5a), `+0x30` instance data, `+0x38` the geometry descriptor |" (`CTX:263`); INDICES_16BIT reads "a byte at `+0x4C` of the last argument's `+0x38`" (`CTX:148`)
- "| `+0x38`, `+0x40`, `+0x48` | `0` | `0060BAF3`, `0060BAFE`, `0060BB08` |" (`CTX:357`, zeroed by the only caller)
- No favoured side. If `CTX:357` holds, `INDICES_16BIT` always evaluates on a null `+0x38`; the page does not say so.

### 3.2 Stale "not read / open" claims and banner disagreements

| # | stale side (quoted) | answering side (quoted) | settled by |
|---|---|---|---|
| C-S1 | `README:14` "**DOCUMENTED, tier 1, crossref-clean.**" (The Frame) | `FRM:4` "status: AUDITED" | no favoured side (banner) |
| C-S2 | `README:21-22` "**DOCUMENTED, tier 1.**" (class descriptors); `README:33` "**DOCUMENTED, tier 1, one falsification pass.**" (member registration); `README:25` same (application); `README:46` "**DOCUMENTED, tier 2.**" (accessors) | `CDMS:4`, `MR:4`, `APP:4`, `ACC:4` "status: AUDITED" | no favoured side (banner) |
| C-S3 | `README:13-63` indexes 8 pages | 23 pages exist; `MOD`, `CAM`, `MAP`, the four asset-container pages, `C-CD`, `AR`, `IS`, `FS`, `PPF` and `ANI` are not indexed | — |
| C-S4 | `README:70` "**AQ-2** (PARTIAL: 4,515 of the 6,769 …)" | `MAP:187` "~~stays PARTIAL on the 2,254 unplaced functions~~ is SUPERSEDED (the line below; 2026-09-29, OPUS" | 2026-09-29 |
| C-S5 | `MAP:186` "**not been applied to the GZF** (open question **B-3**)" | `MAP:187` "**B-3** is now ANSWERED (the class set was applied 2026-09-02 as the vtable method index), so the clause above is history." | 2026-09-26 |
| C-S6 | `MAP:41` "**PARTIAL, and tier 4 by construction.**"; `MAP:42` "No Phyre function body is read here." | `MAP:4` "status: DOCUMENTED"; `MAP:188`/`MAP:198` decode bodies (2026-09-18) | front matter re-statused 2026-09-29 |
| C-S7 | `MAP:180` "whether the ~992 non-glue functions are driven" | `MAP:198` "973 of the 993 are reachable" | 2026-09-18 |
| C-S8 | `MOD:165` "| `005A0CB0` | 100 B | slot `+0x00` of every module vtable — **body unread** |" (also `MOD:221`, `MOD:238`, `MOD:468`) | `MOD:393` "**Answered 2026-09-14 (FABLE): the modules' shared scalar deleting destructor," | 2026-09-14 |
| C-S9 | `APP:381-382` "All nine are" / "overridden and input-tagged; none has been read."; `APP:216` "the input-facing overrides" | `APP:372` "**PA-1 — ANSWERED 2026-09-27 …: nothing in this build dispatches slots 10, 15, 16, 22, 23 or 24.**"; per-slot table `APP:389-398` | 2026-09-14 / 2026-09-27 |
| C-S10 | `APP:400` "**Still open for slots 10, 15 and 16:**" | `APP:372` (as above) | 2026-09-27 |
| C-S11 | `APP:437-438` "Slots 1, 12, 13, 17–20, 29 and" / "30 are not read." | `APP:452` "**ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): every inherited slot now has a behaviour.**" | 2026-09-26 |
| C-S12 | `APP:639-640` "**the caller is inside PhyreEngine and" / "was not read**." | `APP:433-437` (slot 28 `0079C140` read; "The run loop `00796490` calls it") | PA-5, 2026-09-14 |
| C-S13 | `CAM:104` "What is still not claimed is what the two matrices and the two floats mean, `SD-60`." | `CAM:4` "SD-60, is ANSWERED"; answer block `CAM:186-193` | 2026-09-30 |
| C-S14 | `FRM:66-67` "Where the commands are actually consumed is the largest thing this" / "document does not know."; `FRM:753` "the consumer of these buffers is NOT in this executable's" | `FRM:870` "**ANSWERED 2026-09-27 (FABLE, Claude Opus 5.5), static: nothing in this executable reads a finished batch.**" | 2026-09-27 |
| C-S15 | `FRM:876` "uninitialised in the image; only its shape is proven." | `FRM:875` "*(answered 2026-09-18 in section 4.3)*"; `FRM:690` (all values written by nine routines) | 2026-09-18 |
| C-S16 | `FRM:415-416` "spin-waits on `02EAF6D8 bit 0x100` … **and again per entry at `0037559F`–`003755B2`**" | `FRM:208` "**It cannot wait**, no matter who writes the word."; `FRM:212` "**all 17 sites are hoisted**" | falsification 2026-09-12 (`FRM:1093`) |
| C-S17 | `ANI:23` "the binder writes only kind 1, so both halves are measured and still do not meet"; `ANI:845-846` "**no code in this document produces a kind-2 or" / "kind-3 record**" | `ANI:565` "*Answered on the page 2026-09-14 (FABLE), … yes. The binder is a virtual family, and" | 2026-09-14 |
| C-S18 | `ANI:215` "+0x18  ...  (remaining 16 B not read by 005C72A0)"; `ANI:865` "The `ChannelValue` bytes `+0x18`..`+0x27` stay unread." | `ANI:521` "**ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5)**" | 2026-09-26 |
| C-S19 | `ANI:303` "nothing in these bodies says whether it is." (slot-1 purity) | `ANI:591` "**Answered 2026-09-14 (FABLE): it is pure, and the second disjunct is dead.**" | 2026-09-14 |
| C-S20 | `LUA:209-211` "is **not** established from strings alone — see **R-4**, which is the single" / "highest-value open question in this document." | `LUA:366-367` "**R-4 ANSWERED 2026-09-12 (FABLE): neither" / "runs — no standard library is ever opened.**" | 2026-09-12 |
| C-S21 | `LUA:683` "| `01CCB3E0` | 8 | **loadedlibs — opened at startup** |" | `LUA:366-367` (as above) | 2026-09-12 |
| C-S22 | `LUA:307` "**Upstream:** whatever schedules script execution — not yet identified (**R-5**)." | `LUA:384` "**R-5 ANSWERED 2026-09-22 (FABLE): neither — the question has a third answer," | 2026-09-22 |
| C-S23 | `LUA:229` "| `00684D10` / `00686280` | Lua execution sites (`lua_pcall`) | not read |" | `LUA:512` "## 12. The two callers executed — [`EXP-110`]…, folded in 2026-09-19 (OPUS)" | 2026-09-19 |
| C-S24 | `LUA:338` "- [x] What `00684D10` and `00686280` actually execute — which scripts, from where, and when. *(closed — the register row is WITHDRAWN.)*" | `LUA:515-516` "**It does not answer §7's open item** — *which* scripts these execute, from where" / "and when, is still unknown and stays open." | no favoured side (box closed, text open) |
| C-S25 | `ACC:175-176` "the script side reads engine objects through" / "this path and does not write them through it."; `ACC:208` "these are read-side accessors" | `ACC:221` "**But `Get` hands out writable access.**"; `ACC:249` "`AZ-2`'s \"script cannot write\" reading is refuted." | 2026-09-14 |
| C-S26 | `ACC:894` "four shared implementations named above remain not dispositioned." | `ACC:880` "*not in these rows — updated 2026-09-13: `00811130`, `00812960` and `008119F0` are Lua API bodies declared on the Lua library row," | 2026-09-13 (but `ACC:894` is dated later, 2026-09-16; no favoured side) |
| C-S27 | `HDR:251` "| `0059A6F0` | reads the packed namespace — **not read here** | 116 B |" | `C-HDR:147` "### The namespace reader imposes no bound of its own — `0059A6F0`, 116 bytes, read in full" | contract 2026-09-12 |
| C-S28 | `NS:225` "| `0059C180` | the namespace byte-swap fixup — **not read** | — |" | `NS:249` "~~`FUN_0059C180`, the byte-swap fixup — not read.~~ **READ — section 8," | 2026-09-07 |
| C-S29 | `C-HDR:636` "| any execution of this ladder, isolated or live | **none**; §13 | none | UNKNOWN |" | `C-HDR:359` "**Executed 2026-09-12** by [`diff_phyre_header.py`]" | 2026-09-12 |
| C-S30 | `C-HDR:382` "**The byte-swap block is the one that matters and the one that cannot be run.**" | `C-HDR:422` "### 13a. The block that \"cannot be run\" was run — 2026-09-18" | 2026-09-18 |
| C-S31 | `C-NS:478` "`NS-1`'s bit names and `NS-4` stay open," | `C-NS:349` "**ANSWERED 2026-09-26 …: `w7` is the file copy of the runtime class descriptor's `+0xFC` flag byte.**"; `C-NS:382` "**`NS-4` — answered 2026-09-26 …: the loader does read it.**" | 2026-09-26 |
| C-S32 | `NS:360` "| **Why they cluster there** | **not established — a reading, no constructor read** | 8 |" | `NS:195` "**Answered 2026-09-26 (FABLE, Claude Opus 5.5) (`CW-3`): the obvious reading is wrong," | 2026-09-26 |
| C-S33 | `CDMS:244` "| `0063D640` | descriptor sub-object destructor | not read |" | `C-CD:375` "#### `0063D640` takes `(rcx = the sub-object, rdx = the descriptor)` — and this contract had it the other way" | 2026-09-18 |
| C-S34 | `CDMS:158` "**Four separate intrusive linked lists.** Their individual roles are not established — see §7." | `C-CD:115` "### ⚠ CORRECTED 2026-09-12 by the destructor pilot — the destructor does not \"walk four lists\"" | 2026-09-12 |
| C-S35 | `C-CD:551` "| any execution of any of this | **none**; §13 | none | UNKNOWN |"; `C-CD:598` "**Not claimed:** none of this was executed — §13 is unchanged — and `PCD-1`…`PCD-4` stay open" | `C-CD:488` (PCD-3 struck and answered); `C-CD:368` (EXP-097 execution) | 2026-09-18 / 2026-09-25 |
| C-S36 | `C-CD:528` "**Not established:** what `+0x38` measures, and so what the two totals mean." | `C-CD:748` "`+0x38` is this contract's own size field — the one `0063C910` passes to `memcpy`" | 2026-09-20 |
| C-S37 | `MR:498` "Only `+0x80` is identified." | `MR:867` "**Four of six are now identified**"; `+0x60` identified 2026-09-25 (`MR:878-880`) | 2026-09-25 |
| C-S38 | `MR:491` "**(c) is the whole remaining search space, and it is not searched here.** The row" (stays open) | `MR:481` "**ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5): `+0x38`" | 2026-09-25 |
| C-S39 | `MR:2341` "the other 186 unharvested registrations (`RM-1`)." | `MR:797` "**ANSWERED 2026-09-27 (OPUS):** all 215 registrations of the three constructors are accounted for in the store." | 2026-09-27 |
| C-S40 | `MR:1859-1860` "680 of the schema's 682 rows are already carried in `_types/fields.tsv` at" / "the exact type and offset, so the schema side of the propagation is complete" | `MR:1883` "~~**There is no unfinished harvest anywhere in this category.**~~ **Corrected 2026-09-27 (OPUS), §20:" | 2026-09-27 |
| C-S41 | `MR:2019-2020` "**the registered Phyre hierarchy here is" / "shallow.**" | `MR:2050` "**And §19b's reading of control 5 was wrong.**" | §19c, same session |
| C-S42 | `AR:52` "**seven lazy-static accessors**"; `AR:181` "**Which singleton each of the seven accessors returns.** Only that all seven are that shape." (unboxed, while `AR:4` says every box is closed) | `AR:146` "**There are fifteen of them, not seven (2026-09-13, §9).**"; `AR:189` (answered 2026-09-14) | 2026-09-13 / 2026-09-14 |
| C-S43 | `IS:141-142` "so the parent of each class is" / "*not* recovered by this sweep and no class hierarchy is asserted." | `MR` §19 parent chain (`MR:1913-1933`; `members/phyre-class-parent-chain.tsv`) | 2026-09-19 |
| C-S44 | `FS:250` "**`CL-1`** — why the 682-call-site census misses 21 classes that carry both descriptor RTTI and" | `FS:230` "They are ~~**recovery gaps**~~"; CL-1 answered and corrected (`FS:260`, `FS:293`) | 2026-09-14 / 2026-09-26 |
| C-S45 | `FS:39` "**Evidence tier 9, deliberately.**" | `FS:6` "evidence_tier: 3" (explained at `FS:42`) | banner |
| C-S46 | `PPF:223-224` "**but the link is not" / "read, and this document does not claim it.**"; `PPF:589` "| Which setting selects which AO | **not established** | — |" | `PPF:365` "*Answered on the page 2026-09-14 (FABLE), …* **the `HDAO` setting turns AO off or" | 2026-09-14 |
| C-S47 | `PPF:398` "**The class name is still open.** The reflection-schema route this row proposes remains the way to get it."; `PPF:590` "| The context object's class | **not recovered** | — |" | `PPF:1570` "**So the class name is not recoverable from this image by any route this database uses.**" | 2026-09-22 / signed 2026-09-26 (`PPF:387`) |
| C-S48 | `PPF:433` "**Still open:** what the asset puts in bits 13–15." | `PPF:436` "**ANSWERED 2026-09-27 (OPUS):** the shipped assets store **0** there." | 2026-09-27 |
| C-S49 | `PPF:269` "| `001945B0` | 296 B, called before the parameter runs in several passes; **not read** |" | `PPF:512` (`EA-6` answered 2026-09-12) | 2026-09-12 |
| C-S50 | `PPF:54` "**The remaining 48 reference no string and were not read** (`EA-5`)."; `PPF:458` "`UQ-289` stays open on those 30." (also `CTX:832`) | `PPF:504` "***So every one of the 48 now has an identity, and the question changes shape.***" | 2026-09-21 / UQ-289 superseded 2026-09-26 (`PPF:441`) |
| C-S51 | `PFX:434` "*(closed — the register row is WITHDRAWN.)*" (`GF-4`) | `PFX:448` "The question stays open only for content outside"; routed to ASTRA (`PFX:648-649`) | no favoured side (box closed, live question open) |
| C-S52 | `CTX:887` "structural question is not answered and does not need to be" (`GD-5`) | `CTX:332` "**Exactly four pointer slots and then the count**" (§4c settles the structural half) | 2026-09-22 (same day; §4c is the measurement) |
| C-S53 | `CTX:849-850` "The evaluators read four distinct objects" | `CTX:267` "There are five"; `CTX:864` GD-1 answered 2026-09-26 | 2026-09-22 / 2026-09-26 |
| C-S54 | front-matter `last_reviewed` older than the page's own latest dated body section: `APP:18` 2026-09-02, `MR:18` 2026-09-02, `LUA:18` 2026-09-02, `MAP:19` 2026-09-02, `CAM:19` 2026-09-03, `FS:20` 2026-09-05, `HDR:20` 2026-09-07, `NS:20` 2026-09-07, `FRM:18` 2026-09-07, `MOD:19` 2026-09-08, `AR:17` 2026-09-08, `C-HDR:18`, `C-NS:17`, `C-CD:17` 2026-09-12, `CDMS:18`, `ACC:18`, `PPF:12` 2026-09-13 | bodies carry dated sections to 2026-09-25 … 2026-09-30 (e.g. `MR:2348`, `NS:275`, `CAM:186`, `PFX:144`) | banner |

**Not a contradiction between pages, but a probable factual error a port would copy:** `APP:1068` says
"`SetPriorityClass` with `0x8000` (HIGH_PRIORITY_CLASS)". In the Windows SDK, `0x8000` is
`ABOVE_NORMAL_PRIORITY_CLASS` and `HIGH_PRIORITY_CLASS` is `0x80`. This is outside knowledge, not page text. The
immediate (`0x8000`) is what a port should reproduce, but the label should be checked locally.

---

