---
system: The shipped files in public formats — eight extensions dispositioned as standards from their bytes
category: 02-Resource-And-Asset-Pipeline
status: AUDITED
owner_layer: PrimaryOwner:Resource
evidence_tier: 1
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: one file of each extension extracted from FFXII_TZA.vbf (vbfextract.py) and its header or text read
    against the public specification; populations and paths from the archive-extension census and the
    magic census (Tools/work/formats/), never from the extension alone
corpus_validated: "one sample per extension, 2026-09-11; the .webm magic from the magic census (12 of 40 sampled)"
last_reviewed: 2026-09-11
archive_formats:
  - "tga | standard | Truevision TGA (18-byte v1 header): type 2 uncompressed true-colour, 1920 x 1080, 24 bpp, descriptor 0x20 (top-left); header + pixels = the file, no footer"
  - "csv | standard | comma-separated text (RFC 4180 shape); header rows on opt.csv and softparticle_*.csv, a numeric first field on the nine eventlist.csv"
  - "json | standard | RFC 8259 JSON under jsondata/ (maps 459, cutscenes 337, fontcluts 28, init.json and five more at the root)"
  - "h | standard | C preprocessor header text (#define tables generated from ff12worldmapdata.xls, UTF-8 comments; the kr / cn menuquest.h carry a UTF-8 BOM) - data as code"
  - "cnf | standard | Sony PS2 SYSTEM.CNF boot descriptor (BOOT2 = cdrom0:\\SLPM_667.50;1 / VER = 0.01 / VMODE = NTSC, CRLF, 57 bytes)"
  - "sys | standard | Sony PS2 memory-card icon.sys (magic PS2D) cut at 0xC0: the colour and light block without the title and the three icon filenames"
  - "ico | standard | Sony PS2 memory-card icon model (magic 0x00010000, one shape, 36 vertices, one animation frame, 128 x 128 16-bit texture = 33,688 bytes exactly) - NOT a Windows ICO; the ledger's 2026-09-03 identification is overturned here"
  - "webm | standard | WebM / Matroska (EBML magic 1A 45 DF A3 on the 12 files the magic census sampled); the codecs the loader accepts are not read"
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-standard-formats-pass-1
  last_pass_kind: falsification
  crossref_clean: true
  reopened_count: 0
---

# The shipped files in public formats

> Eight of the archive's 48 extensions are formats the game did not author. This sheet names
> each standard from one extracted file's bytes, says what the archive actually holds in it, and
> corrects one earlier identification: the two `.ico` files are PS2 memory-card icon models, not
> Windows icons — the first four bytes are the same, the next sixteen are not.

## 1. What the player sees

The title screens (`.tga`), the movies (`.webm`), the remaster's render options (`.json`, `.csv`),
and four files that only ever mattered on a PlayStation 2 — the boot descriptor and the
memory-card icon pair, in two language folders — carried into the PC archive unchanged.

## 2. Native mechanism

Each row: the population from the census, the sample, its bytes, the standard, and what is *not*
claimed.

### 2.1 `tga` — Truevision TGA (2 files, `gamedata/titleimage/in/`)

`warning.tga`, 6,220,818 B: header `00 00 02 00 00 00 00 00 00 00 00 00 80 07 38 04 18 20` — no id
field, no colour map, image type 2 (uncompressed true-colour), origin 0 / 0, **1920 × 1080**,
**24 bpp**, descriptor `0x20` (top-left origin, no alpha bits). `18 + 1920 × 1080 × 3 = 6,220,818`:
the file is exactly the header and the pixels, no footer. The other file, `sqex logo size_ffx.tga`,
has the same length in the archive index. **The loader (read 2026-09-11, FR-3):** `00473E80`
(372 B), reached only from the script verb `0x5A2` (`0034E340`, no catalog name — the verb that
puts a title card on screen), takes an index 0–3 into the name table at `01F26568` —
`warning.tga`, `SQEX Logo size_FFX.tga`, `rating_01.tga`, `thankyou.tga` — maps the language from
`00229E40()` to a directory code (`in`, `us`, `es`, `fr`, `de`, `it`, `kr`, … `00473EE5`–`00473F61`),
formats `"%s%s/%s"` over `/GameData/titleimage/`, the code and the name (`00473F74`–`00473F93`),
probes the path with `002DF8E0` and, when that returns nothing, reformats with the fallback
directory `in` (`00473FA6`–`00473FC8`), then hands the path to the texture loader `00183180` →
`001D8D60` (`00473FD2`). So only two of the four names ship, and every language falls back to
`in/`. ~~The TGA decode — and whether the descriptor's origin bit is honoured — is inside
`001D8D60`'s image path (`00597970` / `0059D920`), not read here.~~ *Corrected 2026-09-26 (FABLE, Claude Opus 5.5),
FR-3:* `00597970` and `0059D920` are not an image path. They are the file stream's constructor and its `IsOpen` test
([how a path is resolved to bytes](../VBF-Archive-And-Authored-Tables/how-a-path-is-resolved-to-bytes.md)). The decode
is `001D8D60` itself, and **it never reads the descriptor byte**:
- It reads the 18-byte header into a stack buffer (`001D8DE8`–`001D8DFB`) and uses only the width and height words at
  `+0x0C` / `+0x0E`. Nothing in the body reads the id length, the image type, the pixel depth or the descriptor.
- It reads `width × height × 3` bytes straight after the header (`001D8E43`), so it assumes an uncompressed 24-bit
  image with no id field.
- It hands those bytes to the row copier `001EE820`, which swaps bytes 0 and 2 and adds alpha `0xFF` (BGR to RGBA).
  The copier can write rows bottom-up, but its flip argument here is the literal `0` (`001D8E9E`), and this is its only
  direct caller.

So file row 0 becomes texture row 0 whatever the descriptor says. The shipped `warning.tga` is top-left (`0x20`), which
is what that copy assumes; a bottom-left TGA would load upside down. Control:
`_index/candidates/fr3-tga-origin/tga_origin.py` (7 checks).

### 2.2 `csv` — comma-separated text (17 files)

The census: `ps2data/opt.csv`, five `ps2data/soft_particle/softparticle_*.csv`,
`jsondata/parametersmanageruisizestruct.csv`, `prefetchdata/ff12mapjump_custom_nocrystal.csv`
and nine `prefetchdata/<lang>/eventlist.csv` (4,912 B each). Two were read:

- `opt.csv` (10,182 B, 460 lines, LF, no quoting): a header row `MapName,ForceMSAAOff,
  FlipMapOpaqueOrder,SMAA,ForceNoOpaqueChrFirst` and one row per map (`alc0101,No,No,Yes,No`, …)
  — the remaster's per-map render options.
- `softparticle_chara.csv` (2,187 B): `Name,UseSoftParticle,SoftParticleFactor` per effect file
  (`h0000.efx,No,10`).

The magic census shows `eventlist.csv` opening with `274,` — a numeric first field, so no header
row there — and `ff12mapjump_custom_nocrystal.csv` opening with `name`. Neither was read.

### 2.3 `json` — JSON (830 files, `jsondata/`)

The census: `jsondata/maps` 459, `jsondata/cutscenes` 337, `jsondata/fontcluts` 28, and six more
under `jsondata/` — `init.json` (5,746 B) among them: an object of render toggles (`"EnableAO": 1`,
`"EnableDof": 1`, `"EnableYebis": 1`, …) and a `"ModelsToPreload"` array of asset paths. The
cutscene documents ([the depth-of-field sidecar](../../99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md))
read `jsondata/CutScenes/<name>.json` through the engine's JSON reader; the other trees are not
read here. The magic census's second signature, `7B 7D` (`{}`), is `jsondata/0.json`: an empty
object.

### 2.4 `h` — C header text (6 files, `ps2data/image/ff12/myoshiok/<lang>/`)

`us/worldmap/menumap_sub.h` (742 B), `menumap_world.h`, `menumap_world_debug.h`, and
`{us,kr,cn}/quest/menuquest.h`. The sample: `#ifndef _menumap_sub_h_included_`,
`#define menumap_sub_image_MAX 18`, … — a generated header ("This file was made by CnvSubLocation
… Converted from ff12worldmapdata.xls"), comments in ~~Shift-JIS~~ **UTF-8** *(corrected 2026-09-13, FABLE: all six
headers decode as UTF-8 and none decodes as Shift-JIS)*. The `kr` and `cn` `menuquest.h`
open with `EF BB BF` (a UTF-8 BOM) per the magic census. Data as code from the PS2 build; nothing
in the executable is known to parse it. `menumap_world.h` numbers the 48 sub-locations in `menumap_location.bin`'s record order and
sets its zone / marker / zone-route limits ([lmap §10.6](../PS2-Image-Data-Formats/lmap-menumap-location-graph.md)).

### 2.5 `cnf` — PS2 `SYSTEM.CNF` (1 file, `ps2data/cdi/in/`)

57 bytes of CRLF text: `BOOT2 = cdrom0:\SLPM_667.50;1`, `VER = 0.01`, `VMODE = NTSC` — the
PlayStation 2 boot descriptor for the original disc (`SLPM_667.50`), carried verbatim.

### 2.6 `sys` and `ico` — the PS2 memory-card icon pair (2 + 2 files, `…/{in,ch}/bin_menu/`)

`icon.sys` (192 B): magic `PS2D`, `u16 +6 = 26` (the title line break), `u32 +0x0C = 109`
(background transparency), four background colours from `+0x10` alternating `39, 24, 6, 0` and
`186, 164, 125, 0`, and light vectors of `0.5f` from `+0x50` — the Sony memory-card descriptor,
**cut at `0xC0`**: the 964-byte format's title and three 64-byte icon filenames are absent.

`icon1.ico` (33,688 B): `00 00 01 00 | 01 00 00 00 | 06 00 00 00 | 00 00 80 3F | 24 00 00 00` —
magic `0x00010000`, **one animation shape**, texture type 6, the constant `1.0f`, **36 vertices**:
the PS2 memory-card icon model that `icon.sys` describes. The length agrees with that reading:
`20` (header) `+ 36 × 24` (vertex, normal, uv, colour per vertex, one shape) `+ 20` (animation
header) `+ 16` (one frame with one key) `+ 32,768` (a 128 × 128 16-bit texture) `= 33,688` exactly
— the frame and the texture were not decoded field by field, only summed. Read as a Windows ICO
the same bytes are one image entry of width 1, height 0, six colour planes, 0 bpp, **1,065,353,216
bytes at offset 36** — in a 33,688-byte file. That is how the 2026-09-03 identification in
[the format ledger](../../_index/ASSET-FORMATS.md) ("it is a real Windows ICO") is overturned; the
ledger carries the correction.

### 2.7 `webm` — WebM / Matroska (40 files, `gamedata/d3d11/artdata/video/`, 10,377 MiB)

The EBML magic `1A 45 DF A3` on the 12 sampled files is the magic census's finding, not
re-derived here. **The player, located 2026-09-11:** `001B7F30` formats the path as `%s%s.webm`
(`008F8D75`, `001B8009`–`001B8015`) from a 0x1C-stride movie table (`002DF980`) and opens it through
the player object at its record's `+0x678` (`0067A480`), which sets a 1920 × 1080 frame
(`0067A551`–`0067A558`) before `0016F070`. The container is read by the executable's own Matroska
parser — `00801210` (Segment `0x18538067` at `00801391`), `00801550` (interior read 2026-09-17, SWE2-FRONTIER: `008019A0` first at [`00801569`](../../_index/ADDRESS-INDEX.md) — the element-walk core) / `008025B0` / `00802A10` /
`00802DA0` / `00803E70` (Cluster `0x1F43B675`) and `00806F20` (Tracks `0x1654AE6B` at `008071FA`)
— and the video by the linked **WebM Project VP8 Decoder v1.6.0** (libvpx; its name at `01CEB698`,
referenced by `0016ECE0` and `0016F450`); the audio path is the sound layer's Ogg Vorbis streaming
(`01CB8654`, `01CB85E9`). **No codec-id string (`V_VP8`, `A_VORBIS`) exists anywhere in the image**,
so the parser does not choose a decoder by codec id; what a file with another codec does is
therefore still unread (`FR-1`, narrowed).

## 3. Key addresses

None — this sheet is about files. The readers of `.json` (the engine's JSON parser), `.tga` and
`.webm` are the questions below.

## 4. Data structures and formats

```
tga  : TGA v1 header (18 B) + 1920*1080*3 pixels, top-left origin
ico  : PS2 icon: u32 magic 0x00010000, u32 shapes, u32 textureType, f32 1.0, u32 vertices, ...
sys  : PS2 icon.sys: "PS2D", u16 rsv, u16 lineBreak, u32 rsv, u32 bgAlpha, u32 bg[4][4], f32 light[3][4], f32 lightColor[3][4], f32 ambient[4]  (0xC0 B, then nothing)
cnf  : text  BOOT2 = ... / VER = ... / VMODE = ...   (CRLF)
```

## 5. Call chain

Not applicable; see §7.

## 6. Modding notes

- **The title images are plain 24-bit TGAs** at 1920 × 1080; any TGA writer that emits type 2 with
  descriptor `0x20` produces a drop-in file of the same size.
- **`opt.csv` is the per-map render switch table** the remaster added; a row is a map name and four
  Yes / No columns.
- **The PS2 icon pair is not dead weight — ~~it is the save's sidecar~~.** *(Corrected 2026-09-26 (FABLE, Claude Opus 5.5), `FR-2`: no slot sidecar is written. The names are used only to delete those files and
to fill the fields of an in-memory PS2 `icon.sys` image built from the pool's `icon.sys` bytes, which nothing
submits to storage. Nothing copies the pool pair into a slot.)* The save-slot asset name
  builders (`SavePath_FormatSlotAssetName` `00584610`, `SavePath_BuildSlotAssetName` `005837F0`)
  emit **`icon.sys`** for kind 0 and **`static.ico`** for kinds 2–4 beside the numbered slot file
  (`"%s%03d"` for kind 1), from the literals at `00D23EC8` / `00D23ED8` (`005846CB`–`005846DE`,
  `00584674`–`0058468F`); the shipped `in/icon.sys` and `in/icon1.ico` are resource-pool entries
  494 and 495. Which routine copies the pool files into the slot is not read (`FR-2`). `system.cnf`
  and the `.h` headers have no reader: their strings are referenced by nothing (sweep, 2026-09-11).

## 7. What is not known

- [x] **FR-1.** *(status restated in the register 2026-09-26, FABLE, Claude Opus 5.5: see the row)* **What the `.webm` player does with a codec other than VP8 / Vorbis** — the parser
  (`00801210`–`00806F20`) has no codec-id strings to select by, the VP8 decoder is libvpx 1.6.0
  and the audio path is Ogg Vorbis (§2.7); the rejection path is unread. **FR-1** — narrowed
  2026-09-11 from "which codecs and which library".
- [x] **FR-2.** ~~**Whether anything on PC reads `icon.sys` / `icon1.ico`, `system.cnf` or the `.h` headers**~~
  — narrowed 2026-09-11: `icon.sys` and `static.ico` are save-slot sidecar names the path builders
  emit (§6); `system.cnf` and the `.h` headers have no reader. Left: the routine that copies the
  pool's `icon.sys` / `icon1.ico` into a slot. **FR-2.**
  **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): there is no such routine.** Control: [`fr2_icon_pair.py`](../../_index/candidates/fr2-icon-pair/fr2_icon_pair.py) (5 checks, FAILS 0). Read by a
  delegated read-only pass; re-checked here.
  - **The load.** The save controller loads the pool pair (kind 7, ids `0x2C` and `0x2D`) at start-up and keeps
    their pointers.
  - **The template.** The submission-descriptor builder takes the `icon.sys` bytes from the controller. It clears a
    `0x3C4`-byte image, stamps `PS2D` and writes the three icon names into it, which is the PS2 `icon.sys` layout.
  - **Where the image goes: nowhere.** It is built at the save transaction's state 7 into the transaction record,
    and state 7 submits only the data file.
  - **The names.** `icon.sys` and `static.ico` are otherwise used only to **delete** those files.
- [x] **FR-3.** ~~**Which loader reads `gamedata/titleimage/*.tga`**~~ — `00473E80` from verb `0x5A2` (§2.1,
  2026-09-11). Left: whether the decoder beneath `001D8D60` honours the descriptor's origin bit.
  **FR-3.** **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): no.** `001D8D60` never reads the descriptor byte, and it
  copies rows top-down with the copier's flip argument fixed at `0` (§2.1).

## 8. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| TGA type 2, 1920 × 1080 × 24 | `warning.tga` header bytes; `18 + 1920 × 1080 × 3` = the file size | 1 (archive bytes) | PROVEN |
| The title-image loader, its four names, the language directory and the `in` fallback | `00473E80` read whole; the name table at `01F26568` and the strings at `00D22610`–`00D22680` decoded; verb table row `05A2` | 1 | PROVEN |
| `icon.sys` / `static.ico` are save-slot asset names | `00584610` and `005837F0` read whole; the literals at `00D23EC8` / `00D23ED8` | 1 | PROVEN |
| `system.cnf` and the `.h` headers have no reader | rip-relative sweep of each path string (zero hits) with the `titleimage` string as the positive control (two hits in `00473E80`) | 1 (controlled negative) | PROVEN for rip-relative access |
| `csv` / `json` / `h` / `cnf` are the named text formats | the extracted samples, quoted; populations from the census | 1 (archive bytes) | PROVEN |
| `.ico` is the PS2 icon model, not a Windows ICO | the header decoded both ways; the Windows reading's image size exceeds the file; the PS2 reading's parts sum to the file | 1 (archive bytes) | PROVEN |
| `icon.sys` is the PS2 descriptor cut at `0xC0` | `PS2D` magic, the field values, the 192-byte length | 1 (archive bytes) | PROVEN |
| `.webm` is EBML | the magic census (12 of 40 sampled, one signature) | 1 (archive bytes) | PROVEN |

## 9. Related

- [`../../_index/ASSET-FORMATS.md`](../../_index/ASSET-FORMATS.md) — the census and the dispositions.
- [`../PS2-Image-Data-Formats/tim2-images-and-the-seven-slot-registry.md`](../PS2-Image-Data-Formats/tim2-images-and-the-seven-slot-registry.md) — the other `standard` rows (TIM2).
- [`../Prefetch-And-Json-Data/how-the-prefetch-manifests-are-read.md`](../Prefetch-And-Json-Data/how-the-prefetch-manifests-are-read.md) — the `.txt` manifests beside these.

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run first, per
[`EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md)'s 2026-09-13 amendment.)*

The three PS2 dispositions were re-extracted from `FFXII_TZA.vbf` and **read as bytes**, not taken
from the sheet. All three reproduce, to the character.

### The archive index alone settles three sizes

| file | page | index |
|---|--:|--:|
| `ps2data/cdi/in/system.cnf` | 57 B | **57** |
| `…/bin_menu/icon.sys` | "cut at `0xC0`" | **192** = `0xC0` |
| `…/bin_menu/icon1.ico` | 33,688 B | **33,688** |

### And the bytes settle the contents

`system.cnf` is **exactly** what §2 quotes, all three lines and the line endings:

```
BOOT2 = cdrom0:\SLPM_667.50;1\r\n
VER = 0.01\r\n
VMODE = NTSC\r\n
```

— 57 bytes, **three** CRLFs, no trailing content. `icon.sys` opens **`PS2D`** and stops at `0xC0`,
so it really is the colour-and-light block without the title or the three icon filenames.

`icon1.ico` confirms the sheet's **correction** field by field:

```
+0x00  00 00 01 00   fileId 0x00010000   <- byte-identical to a Windows .ICO signature
+0x04  01 00 00 00   animShapes = 1      <- "one shape"
+0x08  06 00 00 00   texType    = 6      <- the 16-bit texture kind
+0x0C  00 00 80 3F   1.0f
+0x10  24 00 00 00   nbVertices = 0x24   <- 36
```

> **The correction is right, and the bytes show exactly why it was needed.** The first four bytes
> `00 00 01 00` are what a Windows `.ICO` starts with too — an extension plus four bytes agrees with
> the wrong answer. **The next sixteen are what separate them**, and they read as a PS2 icon model:
> one animation shape, texture kind 6, a `1.0f`, and **36 vertices**. §1's *"the first four bytes are
> the same, the next sixteen are not"* is literally true of these bytes.

The frontmatter's eight `archive_formats` entries are **eight**, matching "eight of the archive's 48
extensions".

**Not claimed:** `.tga`, `.csv`, `.json`, `.h` and `.webm` were **not** re-extracted — five of the
eight dispositions stand on the original samples. The populations and paths come from the
archive-extension and magic censuses under `Tools/work/formats/` and were not re-run; the `.webm`
row's own caveat (12 of 40 sampled, codecs unread) stands. This is physical access and meaning —
**no file was executed and nothing was observed live.**

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver / encoder fan-out is MECHANICAL.*

- **Input — LABEL-UNSUPPORTED.** The ~~image-path helpers~~ file-stream helpers *(corrected 2026-09-26, FR-3: the
  stream's constructor and `IsOpen`)* `00597970` / `0059D920` are called by a 1,396-byte body that the
  ledger files under Input. That body is the Phyre framework's option parser (`"Error opening : %s"`, `"%d:%d:%d"`;
  [the Yebis source map](../../23-Third-Party-Libraries/PostEffects-Yebis-PPFX/yebis-ppfx-source-map.md) crossings).
  The body belongs to the framework, not to input.
- **Presentation and Rewards_Progression_Economy — CLIENT.** The locale getter `00229E40`, which picks the directory
  code here, is also read by three Presentation bodies and by `EnemyChain_UpdateOnDefeat`
  ([the chain page](../../13-Rewards-Progression-Economy/the-chain-and-its-sticky-coin.md): the 999 / 998 clamp is
  locale-dependent). The movie table `002DF980` is read by a 1,636-byte Presentation body.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**ActorEntity — CLIENT.** `ActorResource_BeginManagerResourceSetLoad`, owned by that layer, calls `002DF980` on this page. That caller is the manager resource-set load: a mode query decides between two paths before any of the set is touched; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Application — CLIENT.** `00584740` — the default allocator the measured `006CC5A0` pool-init names — is also called by `001A98B0`, an Application-domain body. The allocator is shared CRT/runtime plumbing: the crossing is that Application uses it, not that this page owns anything in that layer.

**Platform — SERVICE.** `00584740` is likewise called by `00650D40` (Platform), and `005CD0E0` — the slot arm the pool-init pair uses — is called by `005CD0A0` (Platform). Both are shared CRT/runtime plumbing: the crossing is that Platform uses them, not a shared responsibility.
- **Audio — CLIENT and SERVICE (10 edges).** 5 inbound (Audio bodies `002125A0`, `006794D0`, `00225C40` call page-cited `00584740`, `005CD330`, `005CD700`); 5 outbound (page-cited `00679A50`, `006794D0`, `0067A480` call Audio bodies `007A4930`, `00881830`, `00882200`). Substantive edges include `0067A480` calls `006794D0`; the remaining edges run through shared helpers the page cites.
- **Script_VM_Native_Bridge — CLIENT and SERVICE (4 edges).** 3 inbound (Script_VM_Native_Bridge bodies `0034BA00`, `0033FED0`, `0034E340` call page-cited `00229E40`, `00473E80`); 1 outbound (page-cited `0034E340` call Script_VM_Native_Bridge bodies `VMValueStack_PopInt32CoerceFloat32` (00267E10)). Substantive edges include `00473E80` is called by `0034E340`; the remaining edges run through shared helpers the page cites.
- **UI — MECHANICAL (2 edges).** 2 UI-side calls into shared helper(s) the page cites (`00229E40`) - the helpers' general call surface, not a UI relationship of this page's subjects.
- **WorldAreaField — CLIENT (1 edge).** 1 inbound (WorldAreaField bodies `00379A10` call page-cited `002DF980`). Substantive edges include `002DF980` is called by `00379A10`.
## The `0067A480` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

`0067A480` (702 B) — a Phyre-side worker/init: `0067A9B0`/`0067A350`
gates (`0067A4BE`/`0067A4CE`), four IAT calls through `008C2228`,
`008C21B8`, `008C2230`, `008C2220` (`0067A4E8`/`0067A501`/`0067A514`/
`0067A545`) with the first result stored to `dword[02E3F800]`
(`0067A4EE`), `0016F070`, `0016DEC0`, member `006CCB00` (`0067A597`),
then the `00801210`/`00803190`/`008028E0` cluster (`0067A5D0`–
`0067A5E8`).

| member | role | interior |
| --- | --- | --- |
| `006794D0` (151 B) | arg-shuffle entry — `(rcx, edx)`; stack `-1`/`0` writes (`006794DD`/`006794E7`), `r8d = edx` (`006794F0`) | [`006794DD`](../../_index/ADDRESS-INDEX.md) |
| `00679A50` (408 B) | destroy/cleanup pair — `00880AF0`/`00880BF0` (`00679A6F`/`00679A7B`), `[rsi+0x480]` field load (`00679A80`) | [`00679A80`](../../_index/ADDRESS-INDEX.md) |
| `006CCB00` (143 B) | scope-guard helper — `qword[rsp+0x20] = -2` mask init (`006CCB06`), `(rcx, rdx)` null-gate (`006CCB1F`) | [`006CCB1F`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0067A9B0`, `0067A350`, `0016F070`,
`0016DEC0`, `00801210`, `00803190`, `008028E0`, `00880AF0`,
`00880BF0`, plus the IAT imports at `008C21B8`/`008C2220`/`008C2228`/
`008C2230`.


## Interior citation — frontier hub `002DF980` (2026-09-18, SWE2-EC7)

`002DF980` — 22 B, 34 callers; the two-level index the 0x1C-stride movie table's readers
share. Interior verified: `0215F000` is an array of row-pointer tables — `[0215F000][ecx*8]`
gives the row head ([`002DF98D`](../../_index/ADDRESS-INDEX.md)), `[row][edx*8]` the element
([`002DF991`](../../_index/ADDRESS-INDEX.md)). Both indices sign-extend from 32-bit.

## SWE2-EC7-78 update (2026-09-20) - `006CC730` + `006CC5A0` object-pool pair measured

`006CC5A0` (200 B) is the pool init: `005CD0E0(+0x28,1)` and
`005CD0E0(+0x38,1)` arm both slots, `+0x30`/`+0x40` set, `+0x4C =
edx+0x20`, `+0x58` takes `r9` or defaults to `00584730` (the
deleter); `(esi+0xF) + +0x4C` bytes are allocated via `r14` or
`00584740`; `+8` takes the buffer, `+0x10 = +0x4C - 0x10`, the
buffer's `+0x10` dword is zeroed, `+0x48`/`+0x20` set, and the
return is `buffer != 0`.
Interior anchor `006CC5CE` (the `005CD0E0` arm call).

`006CC730` (139 B) is the matching drain/commit: `byte[+0x20]`
gates everything and is cleared up front. `edx == 0` calls the
`+0x58` deleter slot on `[rcx+8]`; `edx != 0` pushes 8 bytes into
the `[rdi + (0x60|0x80 by +0xA0!=0)]` cursor vector (`+8` cursor vs
`+0x10` cap, `001AB570` grows), then `005CD700(+0x28)` and
`005CD700(+0x38)` signal and `+0x30`/`+0x40` are cleared.
Interior anchor `006CC79A` (the `005CD700` signal call).

## SWE2-EC7-79 update (2026-09-20) - `005CD700` + `005CD330` IAT wrappers measured

`005CD700` (20 B) is the signal wrapper the `006CC730` drain calls:
`[rcx]` is passed to the `008C23E0` IAT slot and 0 returns - the
SetEvent-shaped call.
Interior anchor `005CD707` (the `008C23E0` call).

`005CD330` (61 B) is the wait-and-read pair: `[rcx]` goes to
`008C20E0` with `edx = -1` (infinite wait), then `[rcx]` again to
`008C21E8` writing `[rsp+0x30]`; that dword is stored to `*rdx` and
0 returns - the exit-code fetch after the wait.
Interior anchor `005CD346` (the `008C20E0` wait call).
