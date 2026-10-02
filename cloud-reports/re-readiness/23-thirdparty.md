# Reconstruction readiness — `FFXII TZA/23-Third-Party-Libraries/`

| | |
|---|---|
| Stream | R (reconstruction readiness), per [`docs/cloud-briefs/re-readiness.md`](../../docs/cloud-briefs/re-readiness.md) |
| Board task | `OPUS-CLOUD-R-READINESS-23-1002` |
| Date | 2026-10-02 |
| Snapshot | this repo's text snapshot only (`f26c5667`); no executable, Ghidra or live game was used |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every item is a quotation or a paraphrase of a page, with its location. Several pages in this folder are being edited by other lanes; every quotation is of the snapshot text. |

**Counts:** COUNTS-PLACEHOLDER

Citation form: `ABBREV:line`, where the abbreviation stands for a page path relative to
`FFXII TZA/23-Third-Party-Libraries/`. Line numbers are those of the snapshot file.

| abbrev. | page | lines |
|---|---|---:|
| `README` | `README.md` | 42 |
| `INV` | `third-party-middleware-inventory.md` | 1,292 |
| `BUL` | `Bullet-Physics-Integration/phyre-to-bullet-rigid-body-materialization.md` | 656 |
| `EASTL` | `EASTL/eastl-strings-containers-and-the-logging-allocator.md` | 574 |
| `VPX` | `LibVPX-VP8-Decoder/the-vp8-codec-interface-and-its-control-map.md` | 245 |
| `LUAC` | `Lua-Core/CONTRACT-lua-chunk-loader.md` | 523 |
| `LUA` | `Lua-Core/the-lua-loader-and-what-it-accepts.md` | 597 |
| `PPFX` | `PostEffects-Yebis-PPFX/yebis-ppfx-source-map.md` | 775 |

"Not stated" means none of the 8 pages says it. Where a point is made only on a page outside this folder, it is
named as outside the audited set and not used as evidence.

## Pages read

All 8 `.md` files were read in full (4,704 lines). Member `.tsv` files were opened only to confirm layouts and
row counts:

| members file | data rows | page count it backs |
|---|---:|---|
| `members/bullet.tsv` | 467 | `INV:32` (467) |
| `members/cri-hca-decoder.tsv` | 53 | `INV:29` (53) |
| `members/imgui.tsv` | 9 | `INV:41` (9) |
| `members/jsonbox.tsv` | 54 | `INV:40` (54) |
| `members/libogg-bitwise.tsv` | 4 | `INV:31` (4) |
| `members/libogg-framing.tsv` | 22 | `INV:27` (22) |
| `members/libvorbis.tsv` | 115 | `INV:30` (115) |
| `members/libvpx-vp8-decoder.tsv` | 116 | `INV:35` (116) |
| `members/libvpx-vp8-decoder-uc1.tsv` | 4 (with a column header) | `INV:36` (4) |
| `members/libvpx-vp8-dsp-kernels.tsv` | 63: 30 below `00129800`, 1 at `00133B40`, 30 in `0014xxxx`, 2 at `00158Bxx` | `INV:37` (63; the row's own per-range figures differ, §3 X-17) |
| `members/libwebm-mkvparser.tsv` | 104 | `INV:38` (104) |
| `members/lua.tsv` | 600 | `INV:33` (600) |
| `members/msvc-runtime-tail.tsv` | 52 | `INV:39` (52) |
| `members/tremor-vorbisfile.tsv` | 99 | `INV:28` (99) |
| `members/zlib.tsv` | 54 | `INV:34` (54) |
| `EASTL/members/eastl-string-static-initialisers.tsv` | 51 (all 240 B) | `EASTL:27` (51) |
| `EASTL/members/eastl-basicstring-variant-initialisers.tsv` | 7: five at 228 B, two at 74 B | `EASTL:28` (7) |
| `EASTL/members/eastl-container-static-initialisers.tsv` | 4 (39, 137, 76, 137 B) | `EASTL:29` (4) |
| `PostEffects-Yebis-PPFX/members/ppfx-span.tsv` | 1,598 | `PPFX:28` (1,598) |
| `PostEffects-Yebis-PPFX/members/ppfx-span-uc1.tsv` | 732 (617 with `refs` 0, 115 referenced) | `PPFX:29` (732; 617 / 115) |

Every count column agrees with its file. Where a page's prose arithmetic does not reach that count, the
disagreement is reported in §3 and not resolved. The `select_*.py` scripts were not run (no export is in this repo).

The category `README` indexes **3 of the 7 system pages** (`README:13-30`): `VPX`, `PPFX`, `INV`. `BUL`, `EASTL`,
`LUAC` and `LUA` are not linked from it.

| page | front matter as the page states it | README / in-body banner that differs |
|---|---|---|
| `INV` | `status: DOCUMENTED - was REOPENED; both triggers … are resolved` (`INV:4`); `evidence_tier: 2` (`:6`); `last_reviewed: 2026-09-02` (`:18`); `passes: 3`, `last_pass: 2026-10-01`, `reopened_count: 2` (`:20-25`) | unstruck banner "**REOPENED 2026-09-02 — this document's census had a scope defect.**" (`INV:51`); `README:28` "**DOCUMENTED, tier 2.** Eleven libraries, 690 functions." |
| `BUL` | `status: AUDITED — …` (`BUL:4`); `evidence_tier: 6` (`:6`); `last_reviewed: 2026-09-02` (`:18`); `passes: 1`, `last_pass: 2026-09-03` (`:20-21`); `promoted: 2026-10-01 DOCUMENTED -> AUDITED` (`:29`) | not indexed in `README`; body dated to 2026-09-27 (`BUL:4`); §10 precedes §9 (`BUL:496`, `:575`) |
| `EASTL` | `status: AUDITED — every register row is closed` (`EASTL:4`); `evidence_tier: 3`; `last_reviewed: 2026-09-30` (`:18`); `passes: 1`, `last_pass: 2026-09-03` (`:20-21`); `promoted: 2026-10-01` (`:25`) | not indexed in `README`; "**Superseded readings:** none — this is the document's first version." (`EASTL:427`) beside corrections dated 2026-09-03 and 2026-09-30 |
| `VPX` | `status: DOCUMENTED` (`VPX:4`); `evidence_tier: 1`; `last_reviewed: 2026-09-13` (`:12`); `passes: 1` (`:14`); `crossref_clean: false` (`:20`) | `README:14` "**DOCUMENTED, tier 1.**" (agrees); answers dated to 2026-09-26 (`VPX:128`, `:139`, `:196`) |
| `LUAC` | `readiness: CONTRACT READY`, `confidence: PROVEN` (`LUAC:6-7`); `last_reviewed: 2026-09-08` (`:17`); `passes: 1`, `last_pass: 2026-09-12` (`:20-21`); `crossref_clean: false` (`:23`) | not indexed in `README`; corrections dated 2026-09-25 (`LUAC:54`, `:109`) and a bound dated 2026-09-26 (`LUAC:369`) |
| `LUA` | `status: AUDITED` (`LUA:4`); `evidence_tier: 1`; `last_reviewed: 2026-09-13` (`:13`); `passes: 1`, `last_pass: 2026-09-13` (`:15-16`) | not indexed in `README`; answers dated to 2026-09-26 (`LUA:401`) |
| `PPFX` | `status: AUDITED` (`PPFX:5`); `evidence_tier: 2`; `last_reviewed: 2026-09-02` (`:19`); `passes: 1`, `last_pass: 2026-09-02` (`:21-22`); no `promoted:` line | `README:20` "**DOCUMENTED, tier 2, one falsification pass.**"; body dated to 2026-09-26 (`PPFX:428`); section order §9, §11, BQ-32, §10 (`PPFX:323`, `:331`, `:430`, `:474`) |
| `README` | "Functions \| ~1,000" (`README:8`) | `INV:139` gives 827 tagged; the declared families alone exceed 3,000 (§1.1) |

## 1. Interface

This category is not one engine system. It is the set of upstream libraries linked into the executable, plus the
seams where game or Phyre code enters them. For most libraries the pages establish **identity, version, link
extent and the client edge**, and say outright that they do not describe internals ("**No formula is asserted for
any library's internals.** These are inventory facts." `INV:651`). A port therefore has two different jobs:

- **Upstream-replaceable libraries** (zlib, Lua, Bullet, libvpx, libwebm, libogg, Tremor, libvorbis, JsonBox,
  Dear ImGui, EASTL, the MSVC runtime tail): the port links the named upstream release and reproduces only the
  **seam** (how the game calls in, which build options differ from stock). §1.1 gives the versions; §1.2-§1.6
  give the seams the pages document.
- **Closed libraries** (Yebis/PPFX, the CRI HCA decoder): no upstream text exists to fall back on (`INV:1133-1134`),
  so the port needs a behavioural description. The pages give identity and file structure, not behaviour (§1.7, §2.2).

Sub-systems mapped:

| § | sub-system | pages |
|---|---|---|
| 1.1 | the link map: every declared library, its extent, version and client | `INV`, `README` |
| 1.2 | Phyre → Bullet rigid-body materialisation | `BUL`, `INV` |
| 1.3 | EASTL strings, containers and the allocator | `EASTL`, `INV` |
| 1.4 | the libvpx VP8 codec interface and its control map | `VPX`, `INV` |
| 1.5 | the Lua chunk loader | `LUAC`, `LUA`, `INV` |
| 1.6 | audio and save codecs: libogg, Tremor, libvorbis, CRI HCA, zlib; the movie container | `INV` |
| 1.7 | Yebis / PPFX post-effects and the licence check | `PPFX`, `INV` |
| 1.8 | JsonBox, Dear ImGui, the MSVC runtime tail | `INV`, `EASTL` |
| 1.9 | order, and dependencies on other categories | all |

### 1.1 The link map

Addresses are Ghidra image addresses, base `0x00120000` (`BUL:185`, `EASTL:172`). "Members" is the current
front-matter count; the body figure dated 2026-09-13 is given where it differs.

| library | link extent (census entries) | members now (body figure) | version | inbound client | cite |
|---|---|---:|---|---|---|
| CRI HCA decoder | `00121000` up to `00125740`, less `001243B0` | 53 | decoder banner `Ver.2.05.00` (`INV:810`); see X-32 | SEAD: `Voice::Initialize` `007EBAD0` and voice functions | `INV:29`, `:297-302` |
| libvpx VP8 DSP kernels | `00125740`–`001297DE`, `00133B40`, `001481D0`–`0014C221`, `00158B40` / `00158C09` | 63 (66) | 1.6.0 | the decoder object only; dispatch set-up `0016F080` | `INV:37`, `:455` |
| libvpx VP8 decoder | `0016DDD0` up to `0017C890` | 116 + 4 UC-1 (122) | 1.6.0 (`INV:993`) | video client at `0067xxxx` only | `INV:35-36`, `:436-450` |
| libogg `bitwise.c` | `0017C890` up to `0017CC70` | 4 | 1.3 line (by `framing.c`) | libvorbis, Tremor | `INV:31`, `:339-344` |
| JsonBox | `001FE0E0`–`00202B10`, `002161C0`–`00216540` | 54 (57) | 0.6.2 (`INV:808`, `:810`) | 26 callers in `001Cxxxx` | `INV:40`, `:554-579` |
| Yebis / PPFX | `006DA880` up to `007911E0` | 1,598 + 732 UC-1 (1,638) | not recoverable (`INV:808`) | integration client, 23 functions at `006Cxxxx` | `PPFX:28-29`, `:331-415` |
| Dear ImGui | four runs from `00791D80` to `00798E90` | 9 (10) | v1.35 (`INV:810`) | none live: static initialiser and atexit only | `INV:41`, `:581-600` |
| libogg `framing.c` | `007B9D70`–`007BA970` | 22 | 1.3 (`INV:809`) | SEAD and Tremor | `INV:27`, `:223-253` |
| Tremor + `vorbisfile.c` | `007F41A0` up to `007F6FB0`, `007F7680` up to `007FFBC0` | 99 (106 / 107) | not stated | SEAD voice code: `ov_open_callbacks` `007F5970`, `ov_pcm_seek` `007F59C0`, `ov_read` `007F6750` | `INV:28`, `:277-287` |
| libwebm `mkvparser` | `007FFBC0` up to `00808888`, plus `007AD440`, `007BD590`, `007E3260` | 104 (105) | not stated | movie client at `0067xxxx`, 25 call sites | `INV:38`, `:457-505` |
| MSVC runtime tail | `008087C4` up to `0080C5A0`, plus 14 stdio COMDATs | 52 (54) | `sprintf` "FID-identified VS2019" | the whole image | `INV:39`, `:507-552` |
| zlib | `0080C5A0` up to `0080F2BC`, `0087AF40` up to `0087F180` | 54 (58) | 1.2.11 | `uncompress` from `0019AA20` and the save reader `00865D90`; `compress2` from the save writer `00866200` | `INV:34`, `:409-431` |
| Lua | `0080F2E0` up to `00830760` | 600 (606) | 5.2.1 | 32 API entries, about 1,300 call sites in the Phyre bindings | `INV:33`, `:382-406` |
| Bullet | `00830760` up to `00861E90`, `0087F180` up to `008800C0` | 467 (480) | the 2.77 line (`BUL:387`) | Phyre physics client `0068xxxx`–`006Axxxx`, 62 call sites | `INV:32`, `:351-379` |
| libvorbis (float) | `008800C0` up to `008958B0` | 115 (119) | 1.3.5 (`INV:810`) | `Boundary.Audio` wrappers `00679600` / `00679A50` / `00679F40`; the movie player `0067A480` | `INV:30`, `:316-337`, `:775-780` |
| EASTL | no contiguous span; 97 tagged functions; static-initialiser families 51 + 7 + 4 | — | OUT OF EVIDENCE BOUNDARY (`EASTL:4`) | everything ("a leaf dependency of the whole engine") | `INV:119`, `EASTL:27-29`, `:270` |

libxml2 is **not linked** (`INV:782-805`); the four functions once tagged as libxml2 are game code
(`INV:1049-1060`). The MS ADPCM block decoder `007F6FB0` and its helper `007F7350` sit between the Tremor ranges and
stay undeclared, "because their upstream — SEAD's or a third party's — is not established" (`INV:294-295`).

### 1.2 Phyre → Bullet rigid-body materialisation (`BUL`)

#### Entry point

| function | role | callers | cite |
|---|---|---|---|
| `0069FB10` `PPhysicsRigidBody_MaterializeBulletBody` (1,899 B) | builds a `btCompoundShape` and a `btRigidBody` from one Phyre body | one caller `0069F070` ← `0069EF20` ← `00698C80` ← `006883A0`, which has no listed caller (reached by pointer) | `BUL:174`, `:415` |
| `006A4A60` `PPhysicsRigidBody_ResetBulletTransformScaleAndActivation` (965 B) | `(rcx = self, dl = alsoRescaleShapes)`, always returns 0; removes the body from the world and re-adds it | called at the end of materialisation | `BUL:175`, `:588`, `:640-643` |

#### Inputs and outputs (record layouts)

- **Phyre body, fields read by the seam** (`BUL:202-221`): `+0x28/+0x2C/+0x30` centre of mass z / y / x (but see
  X-1), `+0x58..+0x60` authored inertia ((0,0,0) means compute), `+0x88..+0x90` scale, `+0x98` geometry,
  `+0xB0` child count (bit 31 an ownership flag), `+0xB8` children (inline when count < 2), `+0xC0` damping pair,
  `+0xE4` mass, `+0xE8` `isDynamic` (u8), outputs `+0x118` `btRigidBody*` and `+0x120` `btCompoundShape*`.
- **Further Phyre fields read by `006A4A60`** (`BUL:592-636`): `+0xE9` in-world latch; `+0xC8 → +0x10 → +0x60`
  the world object (vtable slot `+0xA0` to remove, `+0x130` to add); `+0x68..+0x70` and `+0x78..+0x80` two vec3s
  pushed into the body at `+0x150` / `+0x160`; `+0x48` 16 bytes into `006A57C0`; `+0x38..+0x40` translation;
  `+0xE0` collision-group index; mask = `u16` table at `+0x78` of `[self+0xC8]+0x10`, indexed by the same byte.
- **Child record** (`BUL:224-230`): `+0x0C` mass, `+0x18` material (8 bytes read from its `+0x04`),
  `+0x50..+0x58` local scale. Child-array base expression: `BUL:236-242`.
- **`btRigidBodyConstructionInfo`** as filled (`BUL:272-287`): mass, no motion state, identity start transform,
  the compound, inertia, damping from `phyreBody+0xC0`, friction / restitution from `material+0x04`, and seven
  stock trailing constants `0.8, 1.0, false, 0.005, 0.01, 0.01, 0.01`. BN-2 reads the field split directly
  (`BUL:404`).
- **Bullet-side fields named:** collision object `+0xF4` activation state (`BUL:301`); `+0xFC` / `+0x100` friction /
  restitution, body `+0x1E0` / `+0x1E4` damping clamped to `[0, 1]`, `+0x150..+0x158` linear and `+0x160..+0x168`
  angular velocity (`BUL:404`); `rigidBody[0x108]` back-pointer to the Phyre body (`BUL:164`).
- **Compound constants** (`BUL:257-263`): shape type 31, AABB `±0x5D5E0B6B`, scaling `1.0`; `enableDynamicAabbTree`
  is 0 at the only construction site (`BUL:457-464`, `:511-519`).
- **Mass rule** (`BUL:135-144`): dynamic and authored inertia zero → `calculateLocalInertia`; dynamic and mass 0 →
  sum of child masses; non-dynamic → mass 0 and `setActivationState(2)` (`BUL:162-163`).
- **Return codes** (`BUL:312-317`): 0 success (including already built), 9 no geometry, `0xE` allocation failure,
  otherwise a child's failure code.

#### State

- `02EAF6C4` `gNumAlignedAllocs`; `01F44CE0..01F44CF8` Bullet's allocator table (`malloc` `0085E730`, `free`
  `0019C590`, aligned-alloc `0085E630`, aligned-free `0085E6F0`); one writer `0085E6C0` (`BUL:195-196`, `:527-544`).
  Initial values: the four pointers above; the counter's initial value is not stated.
- Lifetime: materialisation is one-time per body, guarded by `+0x118` (`BUL:68-71`, `:358-360`).

#### Order

"**This is materialization, not per-frame update.** Nothing in this document runs per frame." (`BUL:354`). When the
world is stepped, and with what time step, is not stated.

**Reachability.** "the Phyre→ Bullet path has code, registration and reflection, and **no authored input**"
(`BUL:445-446`): no shipped `.phyre` cluster names any physics class (`BUL:422-440`). Physics fed from non-Phyre data
is not excluded (`BUL:448-452`).

### 1.3 EASTL (`EASTL`)

| item | statement | cite |
|---|---|---|
| `basic_string` | 24 bytes, `begin` / `end` / `capacity_end`, no short-string buffer | `EASTL:187-191`, `:451-466` |
| empty string | `end` = `02EBA2E0`, `capacity_end` = `02EBA2E1`, shared process-wide | `EASTL:79-87`, `:178-179`, `:211` |
| destruction guard | `if ((capacity_end - begin) > 1 && begin != NULL) deallocate(begin, …)` | `EASTL:222-223` |
| `vector` | `begin` / `end` / `capacity_end`, inline allocator object at `+0x18`; growth `max(size + n, size ? size*2 : 1)` | `EASTL:194-199`, `:228-235` |
| allocator | `eastl::allocator_memory_log`, ctor `001EDF00` (14 B, writes vtable `00902720`, ignores the name); vtable slots: 1 `001EDF10` `_aligned_malloc(size, alignment)`, 2 `001EDF80` `_aligned_malloc(size, 16)`, 3 `001EDFE0` `_aligned_free`, 4 `0016D690` returns `"EASTL"`; call sites use `+0x10` allocate and `+0x18` deallocate | `EASTL:202-205`, `:387-396` |
| inert log record | slots 1-3 create once a 32-byte record at `01F82E48` holding `0x2000000, 0x200000, 0, 0`; never read | `EASTL:398-401` |
| containers present | `basic_string`, `vector`, `set`, `map`, `list` (allocator-name literals `008F6600`, `008C5F58`, `008F3CB0`, `008F4120`, `008F3CC0`) | `EASTL:327-340`, `:484-490` |
| `001FF740` | C-string → temporary string, delegates to the lookup `001FF6B0`, frees the temporary, returns the lookup's result; 17 callers, 669 sites | `EASTL:521-535` |
| `001FF6B0` | makes a JsonBox value an object (type 3, `0x38`-byte map) when not one, then tail-jumps to the find `001FF4F0` | `EASTL:170` |
| `list` lower bound `001BCE30` | walks `[rcx+0x18]`, key at `node+0x20` | `EASTL:572` |
| static strings | JsonBox's 13 tokens in four copies (52 strings) and 6 empty strings; each with its own globals and atexit destructor via `00808B90` | `EASTL:344-357`, `:153-157` |

State lifetime: the 58 static strings are built before `main` and torn down at exit (`EASTL:153-157`, `:266-267`).
The ordered-tree (rbtree) runtime the inventory now counts as EASTL lives on a category-24 page
(`INV:124-129`) and is outside this map.

### 1.4 libvpx VP8 interface (`VPX`)

| item | statement | cite |
|---|---|---|
| getter | `0016F070` (8 B) returns `01CDB290`; one call site `0067A55F` in the movie decoder set-up | `VPX:26-29`, `:150-151` |
| interface layout | `+0x00` name `01CEB698`; `+0x08` `abi_version` 5; `+0x0C` `caps` `0x140001`; `+0x10` init `0016E110`; `+0x18` destroy `0016E210`; `+0x20` control map `01CDB320`; `+0x28` peek `0016E380`; `+0x30` `0016E3A0`; `+0x38` decode `0016E4A0`; `+0x40` get_frame `0016EA80`; `+0x48..+0x90` zero | `VPX:36-49`, `:205-214` |
| control map | eleven `{u64 id, ptr}` pairs, terminator at `01CDB3D0`; ids 1-7 and `0x100`-`0x103` = libvpx 1.6.0 `vp8_ctf_maps` | `VPX:59-74`, `:128-135` |
| return codes | 0 done, 4 refused (ids 4-7), 8 null argument; `0x101` also returns 1 | `VPX:80-84`, `:71` |
| decoder context | `vpx_codec_alg_priv_t`, 0x330 B: `+0x1A8` `use_frame_threads` (always 0), `+0x1B0` `pbi[0]` (0x4480 B), `pbi+0x2BEC/+0x2BF0/+0x2BF4` refresh flags | `VPX:139-146` |
| mode info | `MODE_INFO` grid at `[pbi+0x1EB0]`, pitch `mode_info_stride` `+0x1E7C` = `mb_cols + 1`, entry 0x4C, `+0x02` `ref_frame` | `VPX:182-204` |
| decoder set-up | `vpx_codec_dec_init_ver` with ABI `0xA`, flags 0, config `{threads, 0x780, 0x438}`; decode via `vpx_codec_decode` | `VPX:152-156` |
| controls issued | none; no dispatcher exists | `VPX:148-175` |

### 1.5 The Lua chunk loader (`LUAC`, `LUA`)

| item | statement | cite |
|---|---|---|
| entry chain | `00683C30` → `00812F70` `luaL_loadbufferx` → `00810180` `lua_load` → `0081DF50` `luaD_protectedparser` → `0081D790` `f_parser` → `0082E910` `luaU_undump` or `0082BE30` `luaY_parser` | `LUAC:51-61`, `:138-153` |
| callers of `00683C30` | `00684D10` and `00686280` (`PClassCallableMethodScript::PCallerScript` slots 1 and 2), `00684F60` (from `PScheduler` slots 0, 1, 4) | `LUA:421-426` |
| buffer record (`PScript`) | `+0x10` u32 length (bit 31 a flag), `+0x18` data, `+0x48` tagged name pointer | `LUAC:106-108`, `LUA:408-410` |
| reproduction formula | `LUAC:220-236` (mode = `NULL`; on error `00811530(L,-1,NULL)`, `00811130(L,-2)`, return false) | `LUAC:220-236` |
| fork | first byte `0x1B` → bytecode, else source; mode checks are `if (mode && …)` | `LUAC:157-169` |
| header | 18 bytes `1B 4C 75 61 52 00 01 04 08 04 04 00 19 93 0D 0A 1A 0A`; byte 0 planted, 17 read, 18 compared; five rejection messages | `LUAC:83-96`, `:459-494` |
| number type | `lua_Number` is 4 bytes (`float`) | `LUAC:99-101` |
| libraries | only `math`, `bit32`, `string`, `coroutine` registered; `load`, `loadfile`, `dofile` and the `package` searchers are dead | `LUAC:178-181`, `LUA:439-454` |
| failure | compile errors are swallowed on all three caller paths | `LUA:455-464` |
| scheduler pool | 40-byte entries; template `+0x18`, size `+0x10 & 0x7FFFFFFF`, destination `+0x08`, `L` at `+0x20`; pool count `+0x58`, capacity `+0x48 & 0x7FFFFFFF`, array `+0x50`; running scheduler `02E41050`, fallback `02E41020` | `LUA:427-434` |
| return extractors | `006810B0` float, `00681130` float widened to double | `LUA:586-587` |

**State and lifetime.** "the image contains **no code that can create a `lua_State`**" (`LUAC:369`); no shipped
asset declares `PScript`, `PClassCallableMethodScript` or `PScheduler` (`LUA:349-359`, `:387-391`). So, as the
pages stand, the loader is reachable only if a state built outside the image is handed in (`LUAC:369`).

**Order.** Not stated: no page says when in a frame any script runs.

### 1.6 Audio, movie and save codecs (`INV`)

- **libogg `framing.c`**: the 22 functions and their identifying bodies are tabulated (`INV:227-248`); allocation goes
  through four hook pointers `01F41CF8` / `01F41D00` / `01F41D08` / `01F41D10`, initialised to the CRT and overwritten
  by SEAD's init `007A4D50` (`INV:250-253`).
- **Tremor** (`INV:277-287`): the SEAD voice code calls `ov_open_callbacks`, `ov_pcm_seek` and `ov_read`; the codec
  registry is `_mapping_P` at `01F41E58` → mapping0 `01F41F40`, residue bundles `01F41EC8` / `01F41EF0` / `01F41F18`,
  floor bundles from `01F41E60` and `01F41E98` (`INV:259-264`).
- **libvorbis**: the movie player's audio path, `0067A480` → `00679A50` → `008800C0` / `00880AF0` / `00880BF0`
  (`INV:775-780`); `_float32_unpack` bias −788 (`INV:329`); its own allocator slots `01CEB618..01CEB630`
  (`INV:330`). The wrapper `00679600` strides two arrays by `0x17700` and `0xBB80` per instance (`INV:1188`).
- **Which decoder runs:** "Tremor runs the sound driver's streams, and libvorbis decodes the movie audio."
  (`INV:779-780`).
- **CRI HCA decoder**: extent and callers only (`INV:297-302`).
- **MS ADPCM** `007F6FB0`: adaptation table 230 … 768, coefficient pairs 256/0, 240/0, 460/−208, 392/−232, samples per
  block `2 × align / channels − 12` (`INV:289-292`).
- **libwebm `mkvparser`**: parse half only; element-walk core `00801550` (`INV:466-468`); the game's `IMkvReader`
  (`VbfMkvReader`) is the client and not covered (`INV:503-505`).
- **zlib** (save path): `0080C750` is stock `inflate()`, so "the save container can be reconstructed against
  upstream zlib 1.2.11 source directly" (`INV:421`); the save body is `compress2` level 9 followed by RC4 (`INV:676-678`).

### 1.7 Yebis / PPFX post-effects (`PPFX`, `INV`)

| item | statement | cite |
|---|---|---|
| identity | PPFX is the core of Silicon Studio's Yebis | `INV:806`, `PPFX:417-425` |
| extent | 1,766 census entries `006DA880` up to `007911E0`; lower edge counter pair `006DA880` / `006DA8A0` on `02EA0B3C`, tested by `006DA8F0` | `PPFX:333-335`, `:348` |
| client | 23 functions at `006Cxxxx` ("the code that reads `FeatureId = YEBIS_D3D11 …`"), static initialisers, teardown thunks | `PPFX:409-412` |
| outbound | 44 targets: CRT and math imports, `sprintf`, MSVC string / container helpers, `0018A320`, `006CBBC0` | `PPFX:404-408` |
| source map | 193 functions attributed to 25 files; the file table | `PPFX:108-133` |
| assertion reporter | `0016D6A0`, a 3-byte `ret 0` | `PPFX:165`, `:242-244` |
| TinyEffect | an effect-source text tokenizer (`00717760`, `0071A230`) and an effect-descriptor deserializer `0078C730` | `PPFX:259-264`, `:358-363` |
| licence check | verifier `006DFF40`; decode `0071C550`; check `0071D9E0`: signed vs plain-text date fields (status 1 on mismatch), all six zero skips the date test, otherwise a `_mktime64` window (status 2, expired) | `INV:707-721` |
| licence record | `FeatureId = YEBIS_D3D11`, six date fields, all zero in the shipped record (`00D86C51`) | `INV:633-649`, `:720` |

### 1.8 JsonBox, Dear ImGui, MSVC runtime tail (`INV`)

- **JsonBox**: parser `00200E60` (1,527 B), client entry `00200BF0`, writer `001FF210`; output-filter vtables
  `00905070` / `009050F0` / `00905170`; error-literal pool `00904FE8`–`00905038` (`INV:556-572`, `EASTL:308-315`). It
  parses an `istream` into EASTL-backed values for `JsonData/*.json` (`EASTL:325-326`).
- **Dear ImGui**: a dormant context, created before `main` by the static initialiser `00169620` → `00791E70` and torn
  down at exit; never pumped (`INV:725-729`, `:747-750`). Context size 0x3AC0 (`INV:810`). A port needs nothing from it.
- **MSVC runtime tail**: `__scrt_common_main_seh` `00808C90`; the `_initterm` range `008C31D0`–`008C5678`; the
  `0xE06D7363` filter `00809B54`; the `__isa_available`-gated math dispatch `008098C0` / `00809900` (`INV:517-526`).
  The start-up and runtime are documented on category-24 pages, outside this map.

### 1.9 Order and dependencies

**Order within a frame.** The only ordering statements are:
- "startup -> EnableYebis -> licence/feature check" (`INV:656-660`);
- "render frame -> Phyre.PostProcessing (72) … -> PPFX (348) … -> YEBIS (3+)" (`INV:662-665`), which X-7 contradicts;
- "the remaster runs the whole image through it every frame" (`PPFX:52`);
- static EASTL strings and the ImGui context are built before `main` (`EASTL:153-157`, `INV:725-729`).

Where post-effects sit relative to UI, and when physics, scripts or audio decoding run in a frame, is not stated.

**Dependencies.**

| on | what | cite |
|---|---|---|
| MSVC CRT / UCRT | every library's outbound calls; `longjmp` for Lua; `_aligned_malloc` for EASTL | `INV:402-403`, `EASTL:393-395` |
| Phyre (cat. 22) | physics client and the materialisation seam; script executors and reflection descriptors; the PPFX integration client; `PImGuiDynamicMesh` | `BUL:338-340`, `LUA:374-381`, `PPFX:409-410`, `INV:599-600` |
| SEAD audio (cat. 18) | Tremor, libogg, CRI HCA; SEAD installs the `_ogg_` hooks | `INV:250-253`, `:300-302` |
| movie player (cat. 17) | libvpx, libwebm, libvorbis | `VPX:150-156`, `INV:501-505`, `:775-780` |
| save pipeline (cat. 19) | zlib `uncompress` / `compress2`, then RC4 | `INV:429-431`, `:671` |
| static initialisation (cat. 24) | EASTL statics, ImGui, the MSVC tail | `EASTL:434`, `INV:727` |
| JSON consumers (Presentation, ItemsEquipment) | JsonBox | `INV:575-576` |

## 2. Gaps

### 2.1 Gaps the pages state themselves (still open, live-only, or out of evidence)

Only gaps the pages still leave open are listed. Rows the pages answer are not listed, even where a stale "open"
sentence remains; those are in §3.2.

| # | gap as the page states it | cite |
|---|---|---|
| G-1 | Whether a Lua chunk is ever supplied: "**Bounded statically 2026-09-26 (OPUS), not closed:**" — no `lua_State` constructor is in the image; "What remains open: whether any module does that, and `EB-1`" | `LUAC:369` |
| G-2 | "**The equivalent enumeration for `PClassCallableMethodScript`'s two descriptors has not been run, and is the next step for this row.**" | `LUA:398-399` |
| G-3 | The `+0x48` tag bit: "What the tag bit at `+0x48` marks (the SSO reading in §3.2 is a guess from its subtraction) is the residue." | `LUAC:281-282` |
| G-4 | Loader parity: "`INTEGRATION` is not covered … and `FULL-SUBSYSTEM` is not, because this is one operation of the loader and the fork, the parser and the undumper are not reconstructed." | `LUAC:510-513` |
| G-5 | Parser identification is by strings and call position: "No body was read line by line."; "`0082F000`'s exact `lcode.c` name was not recovered." | `LUA:470`, `:492` |
| G-6 | "What `0081C6A0`, `00811530` or `00811130` are." (listed under **Not claimed**) | `LUA:567-568` |
| G-7 | Bullet: "The Bullet API names behind vtable slots `+0xA0`, `+0x28`, `+0x78` and `+0x130` are **not read**"; "`006A57C0`, `00853FE0` and `0083A030` are called and **not entered**." | `BUL:648-650` |
| G-8 | Bullet: of the 102 generically tagged bodies, "The other ninety install no vtable … need a structural match against a Bullet release to name." | `BUL:466` |
| G-9 | Bullet: BN-4 excludes only the Phyre route — "**What is excluded is the Phyre component route — the one this page traced — not physics in the game.**" | `BUL:448-452` |
| G-10 | VPX: control `2` "has the same guard and image conversion (not read in full)"; 62 displacement-`0x20` operands "are not triaged" | `VPX:130`, `:168-169` |
| G-11 | PPFX: what the 193 attributed functions do (BQ-29, superseded as a population statement, not answered); "What the 1,657 bodies compute is §7's open work" | `PPFX:252-255`, `:427-428` |
| G-12 | PPFX TinyEffect: "Not established: that retail FFXII feeds it any text (`00717760` has no direct caller)." | `PPFX:263-264` |
| G-13 | PPFX source lines: BQ-31 — the `__LINE__` values "are not determinate" | `PPFX:268-269`, `:287-292` |
| G-14 | PPFX UC-1: "2 UC-1 bodies of the span that RVA-valued data cells outside it match … stay frontier" | `PPFX:29` |
| G-15 | `0071F970` (shared CRT `sscanf_s` reading): "*Narrowed, not closed:* the match is by shape." | `PPFX:378` |
| G-16 | YEBIS licence outcome: "The verifier's outcome for this build is decided by step 1, the signature and field match, which this reading does not re-derive." | `INV:720-721` |
| G-17 | YEBIS product version and EASTL version: OUT OF EVIDENCE BOUNDARY | `INV:808`, `EASTL:4`, `:377-381` |
| G-18 | Game debug menu (not ImGui): "whether mode 1 ever receives a non-zero mask in shipped play is the one thing not settled statically" | `INV:739-740` |
| G-19 | MS ADPCM decoder `007F6FB0` / `007F7350`: upstream "not established" | `INV:294-295` |
| G-20 | libvorbis `00887630` left out "because nothing but its position says what it is"; DSP kernels nothing references (`001274D0`, `00129870`, `0012A290`) "are left undeclared" | `INV:322-323`, `:455` |
| G-21 | Tremor stream vtables: "Which driver object owns which vtable is the residue." | `INV:773` |
| G-22 | "*Reached* means a static caller exists, not that it runs in a given scene." (libvorbis / Tremor) | `INV:781` |
| G-23 | EASTL container set: "The absence of `hash_map`, `deque`, `fixed_*` and the others is therefore not proven." | `EASTL:338-340` |
| G-24 | EASTL statics: "NOT dispositioned: 001EDF00 (documented here), the per-object destructors, the literals, and which game string each object holds" | `EASTL:27` |
| G-25 | Selectors that do not reproduce their own file at HEAD: `select_jsonbox.py` "does not re-run at HEAD"; `select_imgui.py` "does not re-run at HEAD" | `INV:40`, `:41` |
| G-26 | Inventory scope: "Bodies of every third-party function — this is an inventory, not an analysis." (X-1, superseded as a population statement) | `INV:703-704` |
| G-27 | Inventory evidence ceiling: libogg, Tremor and libvorbis carry no upstream text; "YEBIS is a third case: Silicon Studio's middleware is not open source, so there is no upstream text in existence to match against." | `INV:1130-1135` |

### 2.2 Structural gaps (a port needs these and no page states them)

| # | missing | where the gap shows |
|---|---|---|
| SG-1 | **Yebis / PPFX behaviour.** No page gives any post-effect algorithm (depth of field, glare, luminance, the post-effect chain), its parameters, its shaders, or the order of passes. The library is closed (`INV:1133-1134`), so a port has no upstream to link. The pages give file identity only ("This document establishes **where they came from**, not what they compute.") | `PPFX:252-253`, `:192-205` |
| SG-2 | **Where the post-effects sit in a frame**, and their inputs and outputs (which render targets, which formats). §5's chain names only "**Upstream:** the renderer. **Downstream:** the frame buffer." | `PPFX:205`; `INV:662-665` (contradicted, X-7) |
| SG-3 | **The YEBIS licence decode and signature check.** `0071C550` (decode) and step 1 (signature and field match) are named, not described. A port that keeps the check needs both; one that drops it needs to know the success path is the only one taken. | `INV:708-713`, `:720-721` |
| SG-4 | **The PPFX integration client** (`006C9B20` onward, 23 functions) is excluded from every family and documented nowhere in this folder; it is the code that feeds Yebis its parameters. | `PPFX:28`, `:409-410` |
| SG-5 | **CRI HCA decoder behaviour.** Extent, version and callers only; no API, no bitstream, no tables. The decoder is proprietary (no upstream). | `INV:29`, `:297-302`, `:810` |
| SG-6 | **The Bullet world**: who creates the `btDiscreteDynamicsWorld`, the broadphase type (both `btAxisSweep3` and `btDbvtBroadphase` are named), gravity, the fixed time step and sub-steps, solver iterations, and where in the frame the world is stepped. Not stated. | `BUL:342`, `:354`, `:466` |
| SG-7 | **The Phyre physics classes beyond the seam**: sixteen `PPhysics*` classes are registered, and only `PPhysicsRigidBody`'s seam fields are laid out. Shape, material, world and character-controller records are not described. | `BUL:436-440` |
| SG-8 | **The collision-group mask table** read by `006A4A60` (a `u16` table at `+0x78` of the object behind `self+0xC8 → +0x10`): its contents and owner. | `BUL:633-634` |
| SG-9 | **Lua build configuration beyond the header.** The header fixes `lua_Number` = `float`, `int` 4, `size_t` 8. Number formatting (`LUA_NUMBER_FMT`), `lua_str2number`, integer conversion and any other `luaconf.h` change that a `float` build implies are not stated. A port that builds stock 5.2.1 with `float` cannot know whether it matches. | `LUAC:83-101` |
| SG-10 | **The Lua state's construction and the Phyre binding layer.** No page in this folder says how a `lua_State` is made (none is in the image, `LUAC:369`), how the four libraries are opened, or what the `PhyreObject` bindings expose; the bindings page is in category 22. | `LUAC:178-181`; `LUA:513-515` |
| SG-11 | **The PScheduler task and pool records** beyond the fields listed in §1.5 (task list layout, what the `+0x20` dword passed as the third argument means, the scheduler object's other fields). | `LUA:425-434` |
| SG-12 | **EASTL ordered containers and lists.** `map` / `set` node layout, comparator and iteration, and the `list` node layout (only `[rcx+0x18]` chain and key at `node+0x20` are given). The rbtree is on a category-24 page. | `EASTL:572`; `INV:124-129` |
| SG-13 | **EASTL allocator `flags` and alignment.** The call-site signature is `allocate(self, size, flags)`; slot 1 takes an alignment and slot 2 fixes 16. Which slot each container uses, and what `flags` selects, are not stated. Slot 0 is not described. | `EASTL:203-204`, `:391-396` |
| SG-14 | **Third-party build options other than those read.** Stated: libvpx caps (decoder, postproc, input fragments; no frame threading, `VPX:211-217`); Lua header; Bullet's `enableDynamicAabbTree = 0`. Not stated: zlib compile options, Tremor's variant (low-memory or not), libvorbis options, libwebm options, JsonBox's EASTL port details beyond `String32` (`INV:810`). | `VPX:211-217`; `INV:810` |
| SG-15 | **The movie path's data flow**: how `mkvparser` frames reach `vpx_codec_decode`, the output image format handed to the renderer, and how `00679600` feeds libvorbis output to audio (its two strided arrays and channel list are named, not explained). | `VPX:152-156`; `INV:1188-1189` |
| SG-16 | **The MS ADPCM decoder's full algorithm** (only the tables and the samples-per-block formula are given) and whether it is SEAD's or a third party's. | `INV:289-295` |
| SG-17 | **SEAD's use of Tremor**: callback set passed to `ov_open_callbacks`, the read size and the output format. | `INV:282` |
| SG-18 | **Save body encryption**: the save line gives `compress2` level 9 then RC4; the RC4 key and its derivation are not stated in this folder. | `INV:671`, `:676-678` |

### 2.3 Fields written or read by documented functions whose meaning is not given

| # | field | cite |
|---|---|---|
| F-1 | Phyre body `+0x38..+0x40`, `+0x48` (16 B), `+0x68..+0x70`, `+0x78..+0x80`, `+0xC8`, `+0xE0`, `+0xE9`: read by `006A4A60` but absent from the §4 layout; the two vec3s land in Bullet's velocity slots (`+0x150` / `+0x160`) | `BUL:593-607`, `:626-634` vs `:202-221` |
| F-2 | `006A0A50` record `+0x260/+0x264/+0x268` (per-axis scale) and the write into `+0x160..+0x164` | `BUL:654` |
| F-3 | VP8 control 3 context fields `+0xF8` (flag), `+0xFC` (8 B), `+0x104` (4 B), and `+0x108` / `+0x110` (decryptor pointer and state): ids named (`VPX:131-135`), fields not | `VPX:65`, `:73` |
| F-4 | VP8 `+0x30` slot `0016E3A0` "(unnamed, 26 B sibling of `vp8_peek_si`)" | `VPX:44` |
| F-5 | EASTL inert record `01F82E48`: `0x2000000`, `0x200000`, 0, 0 — "nothing ever reads the record" | `EASTL:398-401` |
| F-6 | EASTL map ctor `001E6FD0` "`-2` scope mask"; `00212D60` vtable `00906DA0`, `dword[rbx+0x18] = 0` | `EASTL:562-563` |
| F-7 | ImGui owner record: nine qword fields `+0x34A0`, `+0xFA0`, … freed through `[[01F40380] + 0xC0]` | `INV:1232` |
| F-8 | `00679600`: `dword[rcx+0x324]`, strides `0x17700` / `0xBB80`, `qword[rcx+0x4E8]`; `0067A240`: sub-list heads `+0x10/+0x18/+0x20`, counter `+0x28`, latch `+0x40` | `INV:1188-1189` |
| F-9 | Info-page builder `001D5260`: `byte[rcx+0xA70]` gate; dispatcher `001D0190`'s `[01DFE40C]` mode index and `[rdi+0xA74]` | `INV:1161-1172` |
| F-10 | Debug gates: frame mode byte `02064AD3`, mask `[022C7F94]`, latch `01F81258` `+9` / `+0xA74` | `INV:734-736` |
| F-11 | PPFX nesting counter `02EA0B3C` (incremented / decremented / tested; meaning not given) | `PPFX:348` |
| F-12 | `PScheduler` task `+0x20` dword (third argument) and the running-scheduler refusal code `0x17` | `LUA:427-429` |
