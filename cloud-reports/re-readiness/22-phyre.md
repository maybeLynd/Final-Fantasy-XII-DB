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

