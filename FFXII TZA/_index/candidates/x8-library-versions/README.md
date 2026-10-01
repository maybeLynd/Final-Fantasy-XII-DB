# X-8: the linked library versions (FABLE, Claude Opus 5.5, 2026-09-27)

**Question (X-8):** the exact versions of Bullet, libvorbis, libxml2, JsonBox, Dear ImGui and YEBIS.

**Answer:**

| library | version | status |
|---|---|---|
| Bullet | **2.77** | already answered as `BN-1` (2026-09-26); corroborated here by three more discriminators |
| libvorbis | **1.3.5** | answered |
| Dear ImGui | **v1.35** | answered |
| JsonBox | **the 0.6 line**, locally ported | answered to what the linked code can show |
| libxml2 | not in the image | premise withdrawn |
| YEBIS | not recoverable | class 3 |

The two residues are out of the image's reach:
- ~~**JsonBox**: which of 0.6, 0.6.1, 0.6.2 or later master the port was forked from. The port erased the one code difference.~~ *Corrected 2026-09-27 (FABLE, Claude Opus 5.5): answered, **0.6.2** - see [`x8-jsonbox-062/`](../x8-jsonbox-062/README.md).*
- **YEBIS**: its product version. The image states none, and the vendor publishes no history.

**Evidence classes, kept apart:**
- **STATIC:** every image-side fact, read from the authorised exe.
- **Upstream source:** every "which release added X" fact. It was read in the public repository history, or in the release tarballs for Bullet, and none of it is inferred.
- **Compiled-layout probe:** the Dear ImGui layout numbers. Upstream headers were compiled with g++ x86-64 under WSL. They are corroboration of the store pattern, not authority for it; see the limits under Dear ImGui.

**Control:** `x8_versions.py`. It has 8 image checks, plus 3 upstream-ancestry checks when given a directory of clones (FAILS 0 both ways).

**Method.** A reader first drafted the per-library evidence. FABLE then re-measured every image-side discriminator in the control, re-ran the ancestry checks, and reproduced the ImGui probe on v1.34, v1.35 and v1.36 (`imgui-layout-v1.34-v1.36.txt`).

## Bullet: 2.77 (`BN-1`, corroborated)

`BN-1` pinned 2.77 from the serializer chunk names. Three further discriminators agree, each checked against the 2.76, 2.77 and 2.78 release tarballs:
- **The ray-test adder** `LocalInfoAdder2::addSingleResult` `0083AFB0` copies the user callback's closest-hit fraction back after `call [rax+0x10]` (`0083AFE6`/`0083AFE9`). Upstream `9086c15e` (2010-08-25) added that, so the build is 2.77 or later.
- **The cylinder's inertia.** `btCylinderShape`'s `calculateLocalInertia` slot (vtable `01CCDC60` slot 7) is `00835970`, the box formula, folded with `btBoxShape`'s. Upstream `c49927b4` (2010-11-17) gave the cylinder its own tensor, so the build is 2.77 or earlier.
- **The mesh-part record.** `btStridingMeshInterface::serialize` `008365C0` allocates 0x30-byte mesh parts and has no `PHY_UCHAR` branch. Upstream `f10846ed` (2011-01-07) added that branch, so the build is older than 2.78.

## libvorbis: 1.3.5

- **Lower bound.** `vorbis_book_init_decode` `00882C20` has the single-entry codebook branch at `00882F50`:
  - the test is `n == 1 && dec_maxlength == 1`;
  - it sets `dec_firsttablen = 1` and allocates `calloc(2, 4)`;
  - it stores 1 into both entries.

  Upstream `65417f3a` added exactly this block (`if(n==1 && c->dec_maxlength==1)`). It is in v1.3.5 and not in v1.3.4, so the build is 1.3.5 or later.
- **Upper bound.** `_book_maptype1_quantvals` `00882850` contains no `div`/`idiv`. The 1.3.6 fix `e5b13789` adds `b->entries/vals` and `LONG_MAX/(vals+1)`, and both are variable divisors that need one. The fix is in v1.3.6 and not in v1.3.5, so the build is older than 1.3.6.

**Sensitivity.** The same counter finds 13 divides in the neighbouring libvorbis code `00880000`–`00890000`.

**Limit.** The one decode-side commit between 1.3.5 and 1.3.6 that might be visible (`c75b3b12`, comment-query temporaries) touches code no member is known to contain. So a master snapshot from 2015-03 to 2016-10 reads the same as the tag.

## Dear ImGui: v1.35

**Image.** The `ImGuiIO` ctor `00791D80` memsets 0xB88 bytes and stores `MousePos` at +0xD0 and `MousePosPrev` at +0x310. The static context ctor `00791E70`:
- memsets +0xFA8 for 0x24E0, +0x34B0 for 0x400 and +0x38D8 for 0x1E0;
- stores `LogAutoExpandMaxDepth = 2` at +0x38D4;
- ends with a qword store at +0x3AB8, so the object is 0x3AC0 bytes.

**Upstream, compiled.** v1.35 gives exactly these offsets: InputTextState 0xFA8, Tooltip 0x34B0, PrivateClipboard 0x38B0, LogAutoExpandMaxDepth 0x38D4, FramerateSecPerFrame 0x38D8, the frame-index word 0x3AB8, size 0x3AC0. The neighbouring tags miss:

| tag | Tooltip | size |
|---|---|---|
| v1.34 | 0x308C | 0x36A0 |
| v1.36 | 0x30B0 | 0x42C8 |

Over all 91 commits that touch the two files between v1.34 and v1.36 (`imgui-commit-window.txt`), 0x3AC0 occurs in 12 commits, dated 2015-03-08 to 2015-03-13. v1.35 (`d440a13b`, 2015-03-09) is the only tag in that window.

**Limits.**
- **The probe compiler.** It is g++, not MSVC. These structs have no `long` and no bitfields, and the image's own store offsets agree field by field. So the layout is corroborated by the image, not assumed.
- **A master snapshot.** One from 2015-03-08 to 03-13 would read the same as the tag.
- **The object is dormant in retail** (`UQ-314`).

## JsonBox: the 0.6 line, locally ported

- **The three `OutputFilter` vtables.** `00905070`, `009050F0` and `00905170` are 0x80 apart. Each has 15 `.text` slots followed by a non-code qword.
  - In 0.5, `OutputFilter` declared `virtual setbuf(char*, int)`. On x64 that does not override `basic_streambuf::setbuf(char*, streamsize)`, so it would add a 16th slot.
  - Upstream `37de9008` removed it, together with the `sync()` forwarder. That commit is in 0.6 and not in 0.5, so the build is 0.6 or later.
  - Slot 13 being the `sync` import thunk is **not** used as evidence. A forwarder that only calls the base could fold into a byte-identical `jmp [iat]` stub.
- **Double output.** `001FF3AE` sets precision 17 for double output, which arrived in 0.5 and corroborates the bound.

**Why nothing tighter can be read.** 0.6.1 differs from 0.6 only in documentation. 0.6.2 differs in container typedefs and in `String32` switching from `basic_string` to `vector`. ~~The game replaced those containers with EASTL, so that difference is gone from the image.~~ Later master changes only build files, apart from `getToString`, which is not linked. ~~Which tag the port was forked from is therefore a fact about the game's source tree, not about the shipped code.~~ *Corrected 2026-09-27 (FABLE, Claude Opus 5.5): the port replaced the `Array` / `Object` wrappers, but `String32` survives as a vector - the backslash-u append in `00201EB0` writes no terminator (`002023FB`-`00202414`) - so the build is 0.6.2. [Record](../x8-jsonbox-062/README.md).*

## libxml2: premise withdrawn

- It is not linked: CF-1 withdrew it on 2026-09-12, and `X-6` retired its half as premise-withdrawn on 2026-09-15.
- There is no version to name.

## YEBIS: class 3

The image carries:
- a `__DATE__` of **Feb 18 2016** in the PPFX error format strings (e.g. `00D8E200`);
- the build path `d:\bamboo\build\yeblic-ppfxlic-bl2015\` (`00D94ED0`);
- the licence descriptor `FeatureId = YEBIS_D3D11 …` (`00D86C00`) and its expiry message (`00D8F690`).

It carries no product version. YEBIS is closed source with no public version history. A 2026-09-27 web search for a vendor statement tying a YEBIS version to this title found none. So the version is answerable only from the vendor or the game's build records. That is class 3 under FRONTIER's batch-K ruling, like `MH-1` and `UQ-212`.

## Corrections made with this record

- **Six addresses in FABLE's 2026-09-18 narrowing were file offsets.** The narrowing is on the inventory page's X-8 box. Control check A0 shows each old number holds its string only when read as a file offset.

  | old | correct | string |
  |---|---|---|
  | `01BAC180` | `01CCD380` | `btCollisionShapeData` |
  | `01BAD1D8` | `01CCE3D8` | `btCollisionObjectFloatData` |
  | `01E26F40` | `01F48940` | the `OutputFilter<SolidusEscaper>` RTTI |
  | `01B973D0` | `01CB85D0` | the SEAD vorbis error text |
  | `00C65A00` | `00D86C00` | the YEBIS licence string |
  | `00C6E490` | `00D8F690` | the YEBIS expiry message |

- **A fifth version banner.** Pass 26 recorded the CRI HCA *mixer* banner, 2.00.00. The *decoder* has its own: `HCA Decoder (Float) Ver.2.05.00` at `01CBA5D1` (check H1).

## Files

- `x8_versions.py`: the control.
- `imgui_layout_probe.py`: the layout probe, which needs WSL g++ and an imgui clone.
- `imgui-layout-v1.34-v1.36.txt`: FABLE's reproduction.
- `imgui-commit-window.txt`: the reader's 91-commit census. Columns: sha, date, `sizeof` of IO, Style and context, then `MousePos` and `FramerateSecPerFrame`.
- `consumer-check.md`.
