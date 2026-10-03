---
system: .ta — the map texture animation lists
category: 02-Resource-And-Asset-Pipeline
status: AUDITED
owner_layer: PrimaryOwner:Resource
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 98 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
corpus_validated: "45 / 45 .ta in the archive index, all opened, 2026-09-12"
last_reviewed: 2026-09-12
archive_formats:
  - "ta"
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-ta-lists-pass-1 - all eleven corpus figures reproduced from the archive (45 files, 42 maps, 594 entries, 98/489/7); the seven unresolved entries name a tex/ directory that ships no files while the seven frames DO ship in the shared pool, so the missing thing is the phyremaps redirect, not the art
  crossref_clean: true
  reopened_count: 0
---

# `.ta` — the map texture animation lists

> A plain-text list, one per animated texture on a map, naming the texture and its numbered frames;
> the map loader reads every list the map has in order, binds each name to the texture already
> loaded for the map, and the map renderer later swaps a material's `TextureSampler` between those
> frames.

**Corpus validation.**

| | |
|---|---|
| files examined | **45 of 45** `.ta` entries in the archive index, all opened |
| where | `gamedata/d3d11/artdata/map/<area>/<map>/<map>_anime_<k>_d3d11.ta`, **42 maps**; three maps (`glf0103`, `glf0104`, `rwg0202`) have two lists, `k` = 0 and 1 |
| size | 158 B – 2,672 B |
| entries per file | 2 (4 files) · 3 (2) · 7 (9) · 15 (11) · 16 (16) · 32 (3) — 594 in all |
| line ending | **CRLF after every entry, 45 / 45**, and no other whitespace |
| shape | **one un-numbered entry plus `_pic_1` … `_pic_n`, contiguous, 45 / 45** |
| list numbers | **contiguous from 0 in every map** |
| entries resolving to a shipped texture | 98 as written, 489 through `shared/phyremaps.txt`, **7 unresolved — all seven of `frs0109`'s list**; **the seven textures do ship, in the shared pool — what is missing is the redirect (§9)** |

Census: [`census.py`](../../_experiments/evidence/ta-texture-animation-lists/census.py) →
[`census.out.txt`](../../_experiments/evidence/ta-texture-animation-lists/census.out.txt).

---

## 1. What the player sees

**Flickering fire, moving tree shade, tent cloth, shimmering reflections.** Some surfaces on a map
are animated by flipping through a short sequence of pictures rather than by moving geometry. The
texture names say what they are: `dst0100_fire`, `frs0100_kokage_mime` ("tree-shade"),
`glf0100_ya_tento04` ("tent"), `var0100_m_hansya01_` ("reflection"). Each `.ta` file names one such
texture and its frames. Without a map's `.ta`, the renderer finds no frame set for that texture
(`001A7460` returns null) and nothing swaps it; the base picture still draws.

## 2. The layout

The file is text: **entries separated by CRLF**, each a logical asset path.

```
/GameData/D3D11/ArtData/map/glf01/glf0102/tex/glf0100_ya_tento04.dds.phyre<CR><LF>
/GameData/D3D11/ArtData/map/glf01/glf0102/tex/glf0100_ya_tento04_pic_1.dds.phyre<CR><LF>
```

- The entry **without** `_pic_` is **frame 0** — the texture the map's materials already use.
- An entry containing `_pic_N` is **frame N**, `N` read as decimal digits straight after `_pic_`.
  The order of lines does not matter: shipped files list `_pic_10` before `_pic_2`.
- The paths are **logical**. The archive stores most map textures once under
  `artdata/shared/map/<name>_<hash>….dds.phyre`, and `artdata/shared/phyremaps.txt` (47,341
  logical → physical pairs) maps one to the other.

There is no header, count or version.

## 3. The loader contract

**Discovery — `001A7D50`, chained by `001A9770`.** The map-art routine `001A5B30` zeroes the counter at map-art context `+0x264` (`001A6956`) and calls `001A7D50`, which
formats `"%s%d_%s.ta"` (`008F6768`) from the prefix `.\GameData\D3D11\ArtData\map\<area>\<map>\<map>_anime_`
(built by `001A7A50` at `001A7C6E` into `+0x141`), the counter, and `D3D11` (`001A7D98`), post-
increments the counter (`001A7D9D`), and submits a kind-4 load request whose completion callback is
`001A9770` (`001A7DBF`–`001A7DD0`). The callback, if a buffer arrived, parses it (`001A9787`), frees it
and **requests the next number** (`001A97AE`); if none arrived, it sets `+0x140` — "all lists read"
(`001A97B8`). **So the lists must be numbered 0, 1, 2 … with no gap: a missing `_anime_1` hides
`_anime_2` and every later one.**

**Parsing — `001A8BA0`.** Each list becomes a new element (a vector of texture pointers) of the
context's list at `+0x120`, seeded with one null frame (`001A8BE1`–`001A8C2A`). Then, per entry:

```c
while (sscanf(p, "%s", tok) == 1) {                    // 001A8C6F
    p += strlen(tok) + 2;                              // 001A8C8F: assumes a two-byte separator
    tok = phyremaps_lookup(tok) ?: tok;                // 001A9940 map built from shared/phyremaps.txt
    path = (tok[0] == '.') ? tok : "." + tok;          // 001A8E4B
    asset = LoadedAssets_FindByPathHash(path);         // 0019CE20 -> 0019CA80: hash 00674A00, only if loaded
    tex = asset ? Asset_FindTextureObject(asset) : 0;  // 001A7630
    if ((q = strstr(tok, "_pic_")))                    // 001A8EA3
        frames[atoi_digits(q + 5)] = tex;              // 001A8EB1..001A8F03, growing the vector
    else
        frames[0] = tex;                               // 001A8F11
}
```

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| file name `<map>_anime_<k>_d3d11.ta` | `001A7D50` | **`k` not contiguous from 0 → never requested** | — | — |
| separator | `001A8C8F` | — | — | **not tolerant: a one-byte separator (LF only) cuts the first character off the next entry**, which then fails to resolve |
| an entry's path | `001A9940`, `0019CA80` | **a texture the map has not loaded → a null frame**, silently | — | — |
| the digits after `_pic_` | `001A8EB1` | — | none — a large `N` grows the frame vector to `N + 1` | — |
| the suffix after the digits (`.dds.phyre`) | — | — | — | the frame number stops at the first non-digit |

**The list does not load textures.** `0019CA80` only returns an asset already in the loaded-asset
table (the entry's `+4` count must be at least 1, `0019CAF0`); the `.ah` manifest is what loads them. A frame named in
a `.ta` but absent from the map's `.ah` is stored as null.

**`frs0109` ships exactly that case.** Its one list names `frs0100_kokage_mime` and six frames, and none
of the seven paths is in the archive or in `phyremaps.txt` (the map has no `tex` entries at all), so
all seven frames bind to null at run time ~~unless the textures are loaded under those paths by some~~
~~other route~~ (`TA-2`) *(answered: see UQ-71 - the frames stay null; 2026-10-02, OPUS)*.

**The write path.** None; authored offline.

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `001A5B30` | map-art routine (3,808 B); resets the counter and starts discovery (`001A6956`, `001A6965`) | ◐ that block |
| `001A7A50` | builds the `_anime_` prefix at context `+0x141` (`001A7C6E`) | ◐ |
| `001A7D50` | formats and submits request `<prefix><k>_D3D11.ta` | ✅ full body |
| `001A9770` | completion: parse and chain, or mark done at `+0x140` | ✅ full body |
| `001A8BA0` | the parser | ✅ full body |
| `001A96B0` | grows the list of frame sets | ◐ |
| `001A9940` | returns the `phyremaps.txt` remap table (lazily built from `008F6530`) | ◐ |
| `0019CA80` | loaded-asset lookup by path hash | ✅ full body |
| `001A7630` | finds the texture object inside a loaded asset | ◐ |
| `001A7460` | `FindFrameSet(context, texture)`: the set whose frame 0 is that texture, once `+0x140` is set | ✅ full body |
| `001E62E0` | binds a render object's `TextureSampler` texture to its frame set (cached at `+0x210`) and selects a frame (`+0x204`, dirty flag `+0x208`) when `0 <= frame < count` | ✅ full body |
| `001807F0` | the entry to `001E62E0`, gated on `+0x140` | ✅ full body |
| `002F4520` | the rendering pass that supplies the frame number (call at `002F4A5D`) | ~~✗ `TA-1`~~ *(answered: `TA-1` answered 2026-09-25 below; 2026-10-02, OPUS)* |

### Data addresses

| Address | Name | Kind | Contents |
|---|---|---|---|
| `008F6768` | `"%s%d_%s.ta"` | `.rdata` string | the request format |
| `008F65D8` | `".\GameData\%s\ArtData\map\%s\%s_anime_"` | `.rdata` string | the prefix format |
| `008F6774` | `"_pic_"` | `.rdata` string | the frame marker |
| `008F6530` | `"/GameData/D3D11/ArtData/shared/phyremaps.txt"` | `.rdata` string | the remap table source |
| `008F66D8` | `"TextureSampler"` | `.rdata` string | the material parameter `001E62E0` rebinds |
| `01F81168` | map-art context pointer | `.data` | `+0x120` frame sets, `+0x140` done, `+0x141` prefix, `+0x264` counter |
| `01F81178` | pending `.ta` buffer | `.data` | the load result the callback consumes and frees |

### The `001A7A50` exclusive subtree — all 10 members bound (SWE2-FRONTIER, followup queue)

The exclusive-callee census assigns the prefix builder **10 frontier functions** — the map-art
context's private machinery around the `_anime_` prefix. Interior cites are one instruction
inside each declared extent (`interior_cite.py scan`; no boundary crossings).

| cluster | members | role | interior |
|---|---|---|---|
| sibling list reader | `001A7CB0` (157 B) | formats `.\GameData\%s\ArtData\map\NoModelGroupMaps.txt` and submits the request — the same path pattern as the `.ta` lists, one directory level up | `001A7CC1` |
| context init | `001A92C0` (485 B), `001ABE30` (274 B) | `001A92C0` — the context block's init (`01F81170`/`01F81180` touched): `001EEEF0`, `00220390`, a `[rax+0x18]` virtual, `001BDAB0`, `001BD7E0`, and the `00189120`/`00185A90` pair; `001ABE30` runs the same global-getter + `00185A90` emplace pair twice | `001A92C7` / `001ABE3B` |
| slot emplace | `001A92C0`'s callee `001BD7E0` (86 B, sole call site `001A93C9`), `001F8860` (325 B) | `001BD7E0` forwards to `001F8860` — a `(end − begin)` walk by magic-reciprocal division over a record range, `memcpy` + `001945B0` — the frame-set list's copy/notify step; `00185A90`'s only callee is `001858A0` | `001BD7EA` / `001F8866` |
| teardown | `001BF230` (167 B), `001A5890` (237 B) | `001BF230` — `free` + `001BF190` + a message-stub site; `001A5890` — a `[rax]`-virtual predicate guarding `free` + `001A4920` — the context's release path | `001BF23B` / `001A589A` |
| string + dispatch | `001AD780` (35 B), `001A1EA0` (89 B) | `001AD780` — the byte-copy loop writing the name into `+0x16C` of the context; `001A1EA0` — formats a `0x20`-byte stack message through `0016D670` and forwards it through an indirect call | `001AD790` / `001A1EAF` |
| resource-side helper | `0019EAA0` (84 B) | four `00597xxx`/`0059Bxxx`/`00598xxx` Resource calls — the load queue's private arm | `0019EAB2` |

The subtree is the machinery the page's pipeline assumed: where the prefix string is copied
(`+0x16C`), how the frame-set list is copied and notified, the context teardown, and the sibling
`NoModelGroupMaps.txt` list read — the map-art context's own seams, all private to the prefix
builder's tree.

## 5. Corpus survey

Everything in the validation table was measured over all 45 files. The frame counts cluster on 7,
15, 16 and 32 — sequences of 8, 16 or 32 pictures, counting frame 0. Every listed path points into
its own map's `tex/` folder, even when the texture is shared with neighbouring maps
(`dst0100_fire` is listed by `dst0101`, `dst0104`, `dst0105` and `dst0108`, each under its own folder,
and `phyremaps.txt` sends them to one physical file).

## 6. Falsification pass

~~Not yet run.~~ *(answered: see §9, Falsification pass 1 - 2026-09-13; 2026-10-02, OPUS)*

## 7. What this document does not claim

- [x] **TA-1.** How `002F4520` chooses the frame number it passes to `001807F0`, and so the playback rate and
      looping of a texture animation. `TA-1`.
      *Narrowed 2026-09-14 (FABLE, TA-1): the selection is read; the clock is not.* In `002F4520` (`002F4943`–`002F4A5D`):
      `frame = trunc(*[[ctx + 0x50] + 0x90]) − 1` (a float read through a pointer; 0 when that pointer is null). The draw
      record's signed word `+4` (the pass skips values above `0x3FFF`) is added to `frame`, and the sum is clamped into
      `0 … count − 1` of the animation table at `[r14 + 0x150]` (a count at `+0`, then `0x60`-byte entries at `[+8]`). The
      frame goes to `001807F0` only when that entry's `u16 +0x0C` equals `frame` itself. `001807F0` then forwards
      `(ctx, frame)` to `001E62E0` when byte `+0x140` of the object `001A9930()` returns is set (`001807FF`–`00180814`).
      **The pass clamps and never wraps,** so looping, and the playback rate, belong to whatever advances the float behind
      `[ctx + 0x50] + 0x90`. That writer is not read here.
      **`TA-1` ANSWERED 2026-09-25 (OPUS): the float is a track value of the map's tag-23 animation-slot family, on channel 9, and
      its clock is that slot's time.**
      - **What `+0x50` is.** The per-frame pass `002F5550` stores into the entry's `+0x50` the 0x130-byte slot record
        that `00466CB0` matches (`002F57A3`-`002F57CE`).
      - **What `+0x90` is.** `004677A0` binds every track through `00466420(record, channel, &track+0xC)`. Channel 9's
        arm `00466488` stores `[record+0x90] = &track+0xC`.
      - **The clock.** `004678E0(dt)` adds `dt * rate(+0x38)` to the delta `+0x48`. `004668C0` adds the delta to the
        time `+0x44`:
        - with loop bit 1 of `+0x4C` set, it wraps once by the span `+0x40 - +0x3C`;
        - otherwise it clamps and sets bit 2 (finished);
        - then the tracks are sampled.
      - **dt.** `0036F460`, called by the field frame at `0022AB43`, is the field step accumulator's advance
        `[02064AC0]` (speed-up x1/x2/x4) divided by the time-base scale `[01DFE0B8]`.
      - **So:** the rate is slot `+0x38` (setter `00467700`), and looping is slot `+0x4C` bit 1 (setter
        `004676C0`) over `[+0x3C, +0x40]` (setter `00467660`).
      - **Executed on the shipped `dst0101.mpk` tag-23 chunk** ([replay](../../_index/candidates/ta1-opus-replay-texture-anim-clock/)):
        - the one channel-9 binding points at its track;
        - with loop on, the time wraps at 39 and the frame value cycles 1-16;
        - with loop off, the time clamps and the value holds at 16;
        - rate 2.0 doubles the step.
      - ~~**Not read:** the track sampler `00466240`'s formula~~ **read the same day:** each track keeps its own time,
        which wraps or clamps inside [max(slot start, first key), min(slot end, last key)]. It keeps a key cursor, and
        its value is a cubic between the bracketing keys. The layouts are in the type store as `MapAnimSlot` (0x50) and
        `MapAnimTrackState` (0x18), from an executed census.
      - **Not read:** the script verbs that change rate and loop, and the 0x130 binding record beyond `+0x40`/`+0x44`/
        `+0x46` and its channel pointers.
- [x] **UQ-71.** What `frs0109` shows where its unresolved animated texture would be — whether those paths are
      loaded by another route or the seven frames stay null. `TA-2`.
      *Answered 2026-09-26 (FABLE, Claude Opus 5.5), restating section 9 ("Why the seven do not resolve"): the frames stay
      null, and the unanimated base picture keeps drawing. `frs0109/tex/` does not exist in the archive, and
      `phyremaps.txt` has no row redirecting it. `0019CA80` returns only an asset already loaded under the listed path,
      and no route can load a path the archive lacks. The frames themselves ship in the shared pool under their
      `frs0100` names. Still not traced through the loader: whether `001A7460` is reached for `frs0109`. `TA-2` carries
      the answer; this box is its duplicate.*
- The PS2 source of these animations (the original `mime` texture animation data) is not traced.

## 8. Related

- [`.ah` — the D3D11 asset-header manifests](ah-asset-header-manifests.md) — what loads the textures a `.ta` binds; the same `/GameData/…` text shape.
- [Reflected render parameters and shader assets](../../17-Presentation-Rendering/Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md) — lists `shared/phyremaps.txt` among the plain-text index files.

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run first, one query at a time and read in full.)*

### Every corpus figure reproduces, re-derived from the archive

| claim | measured |
|---|---|
| **45** `.ta` entries, all opened | **45** |
| **42** maps; `glf0103`, `glf0104`, `rwg0202` have two lists at `k` = 0 and 1 | **42**, and exactly those three, with `[0, 1]` each |
| list numbers contiguous from 0 in every map | **no map breaks it** |
| sizes 158 B – 2,672 B | **158 – 2,672** |
| entries per file — 2×4, 3×2, 7×9, 15×11, 16×16, 32×3 | **exactly that histogram** |
| **594** entries in all | **594** |
| CRLF after every entry and no other whitespace, 45 / 45 | **45 / 45** |
| one un-numbered entry plus `_pic_1` … `_pic_n`, contiguous, 45 / 45 | **45 / 45** |
| **98** as written, **489** through `shared/phyremaps.txt`, **7** unresolved | **98 / 489 / 7** |
| the seven are all of `frs0109`'s list | **all seven**, and they are the only unresolved entries |

`phyremaps.txt` is **47,341 pairs** of lines — a logical path followed by the shared file it resolves
to — and the 489 come through it exactly.

> **Two of my own checks failed first and neither was reported.** The shape test read `0 / 45` because
> my `_pic_(\d+)$` anchored at end-of-string and every entry ends `.dds.phyre`; the resolution test
> read `0 / 0 / 594` because I parsed `phyremaps.txt` as whitespace-separated columns when it is
> **pairs of whole lines**. Both are fixed above and both were my instrument. A census that returns a
> clean `0` is the shape this database has been bitten by before.

### ✔ Why the seven do not resolve — and the art is not missing

The page records the seven as unresolved and stops. Measured:

* **`frs0109/tex/` does not exist in the archive at all** — **0** files ship under it, so every entry
  in that list points into a directory the archive does not have. (The other 44 lists name `tex/`
  directories that do.)
* **The textures themselves ship**, in the shared pool: `frs0100_kokage_mime` and its `_pic_1` …
  `_pic_6` are present under `gamedata/d3d11/artdata/shared/map/` as hashed `.dds.phyre` — **21
  entries**, which is the seven logical frames × three variants (plain, `_n`, `_spec`).
* So the list is not naming art that was cut. **What is missing is the `phyremaps.txt` row** that
  would redirect `…/frs0109/tex/frs0100_kokage_mime*.dds.phyre` to the shared files, the way the other
  489 entries are redirected.

> **And the list names another map's textures.** Every one of the seven is a `frs0100_*` name sitting
> in `frs0109`'s `tex/` path — the stem says `frs0100`, the directory says `frs0109`. Whether that is
> an authoring copy from `frs0100`'s list or a deliberate share is **not** established here; what is
> established is that the frames exist, the directory does not, and the redirect does not.

The player-facing consequence is the one §1 already states, reached a different way: `001A7460`
returns null and the base picture keeps drawing. **The difference is that the frames are on the disc**
— a modder restoring that animation needs a `phyremaps` row, not the textures.

**Not claimed.** Whether `001A7460` is actually reached for `frs0109` — the resolution is measured on
the archive index, **not traced through the loader**. Why `frs0109`'s list names `frs0100` stems.
Whether any of the other 44 lists would fail the same way at run time for a reason the index cannot
show. What the `_n` and `_spec` companions are for — they are counted, not read. The archive was
**read, never written**, and nothing was executed.

## 10. The `001A5B30` exclusive subtree — the map-art routine's 33 helpers (SWE2-FRONTIER, exclusive-subtrees package)

The exclusive-callee census assigns 33 frontier functions to `001A5B30` (the map-art routine of §4).
All signature-swept 2026-09-15 (`bshape.py`); the tree is mostly container machinery under the
discovery/registration path:

| cluster | members | role |
|---|---|---|
| registration monster | `001E4000` (2,779 B — `0018D240` ×67 + `0016D6A0` ×61 + `001E5290`, 67 unique RIP refs spanning `008F66D8`/`00900288`–`00901750`+; interior confirmed 2026-09-17, SWE2-FRONTIER: `001E5290` prologue call at [`001E405F`](../../_index/ADDRESS-INDEX.md), then the register/free alternation begins `001E41AE`/`001E41BE`) | a 67-entry table-driven register-and-free pass — the largest body in the subtree |
| twin dispatchers | `001AD130` / `001C0A90` (687/683 B, identical shape: `001EDF00` ×3, `001A1220` ×2, `00210EC0`, `001A4BF0`, `001A0A90`, `0019C5D0`, `0016D6A0`, `001A0BB0`, tables `001AD450`/`001C0DB0`); their `404 B` siblings `001AB3D0`/`001BED50` and `137 B` pair `001AB2C0`/`001BEB20` | two parallel list walks — same machinery instantiated for two record types |
| container iterators | `001A3220`, `001A3380`, `001A34F0`, `001A4390` (161–358 B, `0016D840`/`0016D720` + `[rax+0x10]` indirect), `001A1920`, `001A20A0` (`02CBBD00`), `001A4D20`, `001A5150`, `001A6F10`, `001A7850` | string/refcount helpers (`0016Dxxx`) wrapped around container-vtable calls |
| master populate | `001A7F10` (3,194 B — `001A2F70` ×12, 26 rip-indirect calls via `008C2A08`/`008C2A40` slots, `00210EB0` ×5, `008F66F0`/`008F6730` consts; interior verified 2026-09-17, SWE2-FRONTIER — `001A9940`/`001A7630`/`001A5630`/`0017D2E0` direct calls head the body at [`001A7F5D`](../../_index/ADDRESS-INDEX.md); `001A5630` is a shared leaf — Platform's `0020DE30`/`00781EC0` and PlatformOnlineAchievements' `007A0C60` call the same helper, mechanical) | the fan-out the discovery chain runs — likely the `.ta` list instantiate |
| `001Exxxx` processors | `001E1210`, `001E12C0`, `001E1370`, `001E1490`, `001E1670` (987 B — `01F82D88`/`90`/`A8` triples), `001E1DD0` (1,139 B — `001E1370` ×4 + `[r9+0x10]`/`[r9+0x18]` callback pair; interior verified 2026-09-17, SWE2-FRONTIER — `001E1370` first at [`001E1EF1`](../../_index/ADDRESS-INDEX.md)), `001E3F70`, `001E5290`, `001E55C0`/`001E6110` (462 B twins → `001E6040`), `001AC480`/`001ABC80`/`001ABCE0`/`001AD6E0`/`001AD7B0` | element ops behind the iterators — `001E1DD0`'s `[r9]` pair is the same callback idiom as the SEAD container family (`00210760` subtree) |

Not established: which of the two dispatcher twins serves `.ta` versus its companion list type,
and what the 67 `0018D240` registrations install (`008F66D8`/`009012xx` consts suggest a
vtable/descriptor bank).

## 11. The `002F4520` exclusive subtree — the frame-number pass's 27 helpers (SWE2-FRONTIER, exclusive-subtrees package)

The exclusive-callee census assigns 27 frontier functions to `002F4520`, the rendering pass
that supplies the frame number (§4, `TA-1`). All signature-swept 2026-09-15 (`bshape.py`):

| cluster | members | role |
|---|---|---|
| resource-handle helpers | `00180650` (108 B — `001A9930` ×2 + `001A94C0`/`001E3E80`/`001E3FF0`/`001A4FE0`, `[rax+8]` virtual), `00180730` (`001A9930` + `001A9B70`), `001807F0` (`001A9930` + `001E62E0` — the entry `TA-1` names), `00180830`, `00180900` (`001AA240`), `001809A0` (`0018CA40` ×2), `001806C0` (`00189120`), `001803F0` (`001E4B00`), `001A4FE0` (`001AB570`), `001A94C0` (`001A2E50`), `001A9B70` (`001E5790`), `001AA240` (`001E69A0`) | the `001A9930` resolve + `001Exxxx` fetch chain the pass walks per `.ta` entry |
| frame/source bodies | `001E5790` (530 B on `01CEBDA0` — ~~the frame-clock read behind `001A9B70`~~ a call-free record writer that negates two floats with the `.rdata` sign mask *(corrected 2026-10-02, OPUS: `01CEBDA0` is four `0x80000000` and `001E5790+0xF7` `xorps`es with it)*), `001E62E0` (284 B — `0016D6A0` ×2 + `0018D240`/`001A9930`/`001A7460`, `008F66D8`), `001E69A0` (263 B), `001A7460` (the null-returning resolver of §6/§9) | `TA-1`'s actual machinery — the clock read and the resolver the open question covers |
| emit/scratch | `0018C3C0` (144 B — `0085E730` + `001F1D30` + `001AB570` + `0018B4E0`, the same shape as the `0022B0B0` four-sibling pass arms), `003ABD20` (`02B3F508`), `00467A70`/`00467A90` (`02CA5FF4`/`F8`), `00467B60` (71 B — rip-indirect + `008C2BD8`/`00901988`/`00D12518`/`01CEBD80`/`02AED570`), `00468070` | the draw-side emit the pass feeds |
| leaves | `00180870`, `001A9DD0`, `001E3E80`, `001E3FF0`, `001E4B00` | five 7–17 B thunks |

`TA-1`'s answer lives here in embryo: ~~`001E5790` is the clock source (`01CEBDA0` — the same~~ *(corrected 2026-10-02, OPUS: `001E5790` makes no call and `01CEBDA0` is the float sign mask its `+0xF7` `xorps` uses; the clock is the animation slot's time, `TA-1` answered 2026-09-25 above)* (the same
global the fps exceptions read) and `001E62E0` owns `001A7460`. What selects the *index* into
that clock — the question's open half — sits in `002F4520` itself, not the subtree.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver / encoder fan-out is MECHANICAL.*

- **CoreRuntimeScheduling — CLIENT.**
  - `MainLoop_Draw` (`0022B0B0`) is called by the field frame (2,001 B) and the capture mode (174 B).
  - The console-block accessor `001A9930` and `001A1220` are read by a 404-byte core body.
  - `0018B4E0` / `0018CA40` are read by two core bodies (79 B and 237 B).
- **Movement — SERVICE.** `MainLoop_Draw` calls a 7-byte movement getter. The frame-number supplier `002F4520`
  (`"display map"`) calls a 73-byte movement helper.
- **Audio — SERVICE and CLIENT.** The `.win.config` loader `00210760` is reached through a 31-byte Audio-filed body. It
  calls four Audio-filed helpers (41–1,373 B).

- **Platform — MECHANICAL (SWE2-EC7-170, 7 edges).** `0020D1E0` — the second
  `001A5030` caller this page names — is itself called by `0020DE30` on the
  Platform layer; the loader's own reach, not a ta-list relationship. Edge list
  from `edges.tsv` 2026-09-22.
- **Presentation — MECHANICAL (SWE2-EC7-170, 99 edges).** `00195670` (the grow
  helper `001A5030` runs) is called by `0020DC70`, and `0020D1E0` calls
  `0020DC70`, on the Presentation layer — shared string-helper fan-in over the
  pair's wider edge set, no presentation relationship to the lists. Edge list
  from `edges.tsv` 2026-09-22.
- **Save_Load_Settings — CLIENT (6 edges).** 6 inbound (Save_Load_Settings bodies `SaveloadManager_RequestDisableAutosaveList` (001C1810), `GameSettingConfig_ParseText` (001DE5D0), `SaveloadManager_ParseDisableAutosaveList` (001C0F20) call page-cited `001858A0`, `001A0A90`, `001A0BB0`). Substantive edges include `001858A0` is called by `SaveloadManager_ParseDisableAutosaveList` (001C0F20); `001A0A90` is called by `SaveloadManager_RequestDisableAutosaveList` (001C1810); `001A0BB0` is called by `SaveloadManager_RequestDisableAutosaveList` (001C1810); `001A1220` is called by `SaveloadManager_RequestDisableAutosaveList` (001C1810); the remaining edges run through shared helpers the page cites.
## Interior citation — frontier hub `001A5630` (2026-09-18, SWE2-EC7)

`001A5630` — 301 B, 9 A-measured callers; the "shared leaf" the master-populate row names
above. Interior verified: it is `basic_string::assign(ptr, n)` with the MS-STL self-reference
guard — when `rdx` lies inside the string's own buffer (`[rcx]`/`[rcx+0x10]` bounds computed
through the `+0x18 >= 0x10` SSO test at `001A564D`–`001A5674`) it tail-branches to the
offset-based sibling `001A5500` (`001A56A2`). `n > -2` raises `length_error` via the literal
at `008F39F8` and the throw helper `008C2618` (`001A56AD`–`001A56BA`). Otherwise
`00195670` grows capacity when `[+0x18] < n`, `memcpy` (`00861EBA`) copies `n` bytes at
[`001A572E`](../../_index/ADDRESS-INDEX.md), `[+0x10]` becomes `n`, and the terminator is written at
`001A5746` — empty input short-circuits to `n=0` + terminator only.

## SWE2-EC7-27 update (2026-09-18) — `00674A00` the path hash

`00674A00` (40 B) is the hash this page names for `LoadedAssets_`
`FindByPathHash`: `eax = 0x1505`, then per byte `eax = eax*0x21 +
movsx(dl)` over the null-terminated string, finished by `btr 0x1F` —
the 33-multiplicative hash with the sign bit stripped. Interior anchor
`00674A10` (the multiply-accumulate).
## SWE2-EC7-32 update (2026-09-18) — `001A4250` `vector<int>` insert (via `001A5B30`/`001A7850`/`001E1670`)

`001A4250` (315 B) — reached through `001A5B30`, `001A7850`,
`001E1670`, `00201EB0`, `0020AE70` and `0020AF10` — is the CRT
`vector<int>` insert the ta list builders share: room at
`[rcx+8] != [rcx+0x10]` shifts the tail one element and writes
in place; a full vector doubles capacity through the allocator's
`+0x10` vfunc, `008C2A40`-memmoves both halves around the insert
point, writes the new element, frees the old block through the
`+0x18` vfunc, and republishes begin/end/cap. The `r8` inside-
range check bumps the source pointer when it aliases the move
window. Interior anchor `001A42F2` (the `call [rax+0x10]` grow
allocation).

## SWE2-EC7-36 update (2026-09-19) - `001AD130`

`001AD130` (687 B) is a TA-list record builder - `008F6600` allocator, `001EDF00`/`001A1220`/`001AB3D0`/`00210EC0`/`00808C40`. Interior anchor `001AD178` (an `001EDF00` call).

## SWE2-EC7-36 update (2026-09-19) - `001C0A90`

`001C0A90` (683 B) is the sibling TA-list builder - same `008F6600`/`001EDF00`/`001A1220`/`00210EC0` shape plus `00861EC0`. Interior anchor `001C0AD8` (an `001EDF00` call).

## SWE2-EC7-37 update (2026-09-19) - `001E5790`

`001E5790` (530 B) is a call-free mode-switch record writer - `edx` switch on `{1,2,3,>3}` copying 16-byte records into `+0x16c`/`+0x1d8`-family offsets of the `+0xd8`-selected channel. Interior anchor `001E5887` (inside the copy arms).

## SWE2-EC7-38 update (2026-09-19) - `001E55C0`

`001E55C0` (462 B) is a TA-list body - `00861EBA`/`001E6040`. Interior anchor `001E56F9` (the `00861EBA` call).

## SWE2-EC7-38 update (2026-09-19) - `001E6110`

`001E6110` (462 B) is the sibling TA-list body - same `00861EBA`/`001E6040` pair. Interior anchor `001E6249` (the `00861EBA` call).

## SWE2-EC7-39 update (2026-09-19) - `001A2F70`

`001A2F70` (397 B) is a TA-list body - `01CEBBA8`/`02EBA2E0`/`02EBA2E1`, `"EASTL basic_string"`, `00861EC0`/`001EDF00`/`001A2750`/`001A3D70` plus two vcalls. Interior anchor `001A2FE4` (an `00861EC0` call).

## SWE2-EC7-40 update (2026-09-19) - `001858A0`

`001858A0` (367 B) is a TA-list body - two vcalls only, no direct calls. Interior anchor `00185956` (the first vcall).

## SWE2-EC7-40 update (2026-09-19) - `001A3380`

`001A3380` (358 B) is a TA-list sibling - `0016D840`/`0016D720` plus two vcalls. Interior anchor `001A33F3` (a `0016D720` call).

## SWE2-EC7-40 update (2026-09-19) - `001EEEF0`

`001EEEF0` (358 B) is a TA-list body - `0063ABF0` pair plus `00584730`. Interior anchor `001EEF6E` (a `0063ABF0` call).

## SWE2-EC7-41 update (2026-09-19) - `001A34F0`

`001A34F0` (350 B) is a ta-list body - `0016D6D0`/`0016D840` pair/`001A4390`/`001A3380`. Interior anchor `001A3529` (an `0016D6D0` call).

## SWE2-EC7-41 update (2026-09-19) - `001A3220`

`001A3220` (337 B) is a ta-list body - `0016D720`/`0016D840` pair sibling. Interior anchor `001A3293` (an `0016D720` call).

## SWE2-EC7-42 update (2026-09-19) - `001A5150`

`001A5150` (322 B) is a ta-list body - `"string too long"`, `008C2618`/`008F39F8`, `00195670`/`00861EBA`. Interior anchor `001A51DD` (an `00195670` call).

## SWE2-EC7-44 update (2026-09-19) - `001E69A0`

`001E69A0` (263 B) is a call-free record initializer - `dl`/`r8b` flags to `[+0xC1]`/`[+0xC2]`, a `(vec_end-vec_begin)>>3` walk writing `r9d`-or-0 into `[+0x78]` keyed on `byte[+0x58]`, a `comiss`>0 float select into `[+0xC8]`, `+0xC3`/`+0xC4` stack-byte copies, then a flag-gated `+0x98` zero pass. Interior anchor `001E69D0` (the first array walk).

## SWE2-EC7-46 update (2026-09-19) - `001A7850`

`001A7850` (233 B) is a body - `001A4250`/`001AB570`/`00865720`. Interior anchor `001A788A` (an `001A4250` call).

## SWE2-EC7-46 update (2026-09-19) - `001A6F10`

`001A6F10` (224 B) is a body - `001A1990`/`00861ED2`. Interior anchor `001A6F82` (an `001A1990` call).

## SWE2-EC7-47 update (2026-09-19) - `001E5290`

`001E5290` (218 B) is a body - `001E12C0`/`001E1DD0`/`00861EC0`. Interior anchor `001E52E9` (an `001E12C0` call).

## SWE2-EC7-48 update (2026-09-19) - `001E6040`

`001E6040` (201 B) is the shared TA-list callee - `0018AA00`/`001945B0`/`001E3EB0`. Interior anchor `001E60A7` (an `0018AA00` call).

## SWE2-EC7-49 update (2026-09-19) - `001E1370`

`001E1370` (195 B) is a call-free record-copy sibling - `[r10]` dst chain, `movups` x8 per `0x80`, `rdx != r8` loop with a null-skip. Interior anchor `001E13A5` (the first `movups` block).

## SWE2-EC7-50 update (2026-09-19) - `001A96B0`

`001A96B0` (182 B) is a body - `001A4650`/`001A6D80`/`001EDF00` plus a `call [rax+0x18]` vcall. Interior anchor `001A96FC` (an `001A4650` call).

## SWE2-EC7-52 update (2026-09-19) - `001A4650`

`001A4650` (620 B) is a texture-animation body - `0019D8D0`/`001A1F00`/`001A1A00`/`001A1FC0`/`001A1CE0` calls. Interior anchor `001A46A2` (a `0019D8D0` call).

## SWE2-EC7-53 update (2026-09-19) - `001A3D70`

`001A3D70` (412 B) is a TA-list body - `0016D6D0`/`0016D840`/`001A2750`/`001A3BE0`/`001A4590` plus two vcalls. Interior anchor `001A3DB7` (a `0016D6D0` call).

## SWE2-EC7-54 update (2026-09-19) - `001A3BE0`

`001A3BE0` (387 B) is a TA-list body - `0016D720`/`0016D840`/`001A2750` plus two vcalls. Interior anchor `001A3C52` (a `0016D720` call).


## SWE2-EC7-54 update (2026-09-19) - `001A1A00`

`001A1A00` (354 B) is a `0x20`-stride backward element-move sibling of `001AB6B0` - `[r14+8]`/`[r14]` pairs, `call [rax+0x10]`/`call [r9+0x18]` vcalls plus `008C2A40` import sites. Interior anchor `001A1A55` (the `[r14+8]` pair load).


## SWE2-EC7-54 update (2026-09-19) - `001A1CE0`

`001A1CE0` (339 B) is a `0x20`-stride forward element-move sibling of `001A1A00` - `[r12+8]`/`[r12]` pairs, `call [rax+0x10]`/`call [r9+0x18]` vcalls plus `008C2A40` import sites. Interior anchor `001A1D1D` (the `[r12+8]` pair load).


## SWE2-EC7-54 update (2026-09-19) - `0063ABF0`

`0063ABF0` (299 B) is a shared helper called by the TA-list, post-process and vtable pages' bodies - `0063B3E0`/`0063B4D0`/`0063D8B0`/`00680030`/`00680200`. Interior anchor `0063AC5A` (a `0063B4D0` call).

## SWE2-EC7-55 update (2026-09-19) - `00865720`

`00865720` (275 B) is an indirect-only element-move sibling of `001A1A00` - `call [rax+0x10]`/`call [r9+0x18]` vcalls plus `008C2A40` import sites. Interior anchor `008657B1` (the `call [rax+0x10]` vcall).


## SWE2-EC7-55 update (2026-09-19) - `0063B4D0`

`0063B4D0` (250 B) is a shared helper the TA-list page names - `006800F0` single call plus one vcall. Interior anchor `0063B594` (a `006800F0` call).

## SWE2-EC7-56 update (2026-09-19) - `0063B3E0`

`0063B3E0` (230 B) is a shared helper the TA-list page names - `00584730` single call plus one vcall. Interior anchor `0063B4AD` (a `00584730` call).


## SWE2-EC7-56 update (2026-09-19) - `001A1FC0`

`001A1FC0` (219 B) is a texture-animation body - `001EDF00` single call plus two vcalls. Interior anchor `001A2025` (a `001EDF00` call).

## SWE2-EC7-57 update (2026-09-19) - `001A1F00`

`001A1F00` (188 B) is a texture-animation body - `001EDF00` single call, `008C5F58` and the `"EASTL vector"` literal. Interior anchor `001A1F58` (a `001EDF00` call).


## SWE2-EC7-57 update (2026-09-19) - `001E3EB0`

`001E3EB0` (183 B) is a call-free tail-call dispatcher - `r8d` arms selecting `edx` 0-3 then `jmp 0018A9E0`/`jmp 0018AA00` on the `01F7E340` singleton. Interior anchor `001E3EE7` (the `jmp 0018A9E0` tail).


## SWE2-EC7-57 update (2026-09-19) - `001A4590`

`001A4590` (179 B) is a TA-list body - `0016D840`/`001A2750` plus one vcall. Interior anchor `001A4611` (a `001A2750` call).

## SWE2-EC7-58 update (2026-09-19) - `001E1210`

`001E1210` (168 B) is a call-free `0x80`-stride record copier - 4-iteration `movups` pairs (`ecx`=4, `sub r9,0x220`). Interior anchor `001E1251` (the first `movups` store).


## SWE2-EC7-58 update (2026-09-19) - `001E12C0`

`001E12C0` (166 B) is a call-free `0x80`-stride record copier - 4-iteration `movups` pairs (`r8d`=4), `001E1210` sibling. Interior anchor `001E12F1` (the first `movups` store).

## SWE2-EC7-59 update (2026-09-19) - `001A4390`

`001A4390` (161 B) is a TA-list container iterator - `0016D840` single call plus one vcall. Interior anchor `001A440A` (a `0016D840` call).

## SWE2-EC7-60 update (2026-09-19) - `001A6D80`

`001A6D80` (158 B) is a TA-list body - `001A1B70` single call plus one vcall. Interior anchor `001A6DB6` (a `001A1B70` call).


## SWE2-EC7-60 update (2026-09-19) - `001A2750`

`001A2750` (156 B) is a TA-list body - `001A4BF0`/`001EDF00`. Interior anchor `001A27C3` (a `001EDF00` call).


## SWE2-EC7-60 update (2026-09-19) - `0019D8D0`

`0019D8D0` (155 B) is a TA-list body - `001EDF00` single call plus two vcalls, `008C2A40`. Interior anchor `0019D8FE` (a `001EDF00` call).


## SWE2-EC7-60 update (2026-09-19) - `001A4920`

`001A4920` (155 B) is a TA-list teardown body - `001A4920` self-recursive call plus two vcalls. Interior anchor `001A4956` (a `001A4920` call).

## SWE2-EC7-61 update (2026-09-19) - `001A1B70`

`001A1B70` (354 B) is an indirect-only node-tree walk - `[r14]`/`[r14+8]` child pointers, `call [rax+0x10]`/`call [r9+0x18]` plus three `008C2A40` import calls (`001A1A00` sibling). Interior anchor `001A1BEF` (the `call [rax+0x10]` vcall).


## SWE2-EC7-61 update (2026-09-19) - `001AD6E0`

`001AD6E0` (153 B) is a TA-list processor - `001ABB30` single call. Interior anchor `001AD736` (a `001ABB30` call).


## SWE2-EC7-61 update (2026-09-19) - `001AD7B0`

`001AD7B0` (153 B) is a TA-list processor - `001ABB30` single call. Interior anchor `001AD806` (a `001ABB30` call).


## SWE2-EC7-61 update (2026-09-19) - `0020AE70`

`0020AE70` (151 B) is a TA-list CRT body - `001A4250` single call plus `01DFE40C`/`01F832B0`/`01F83390`. Interior anchor `0020AEDE` (a `001A4250` call).

## SWE2-EC7-62 update (2026-09-19) - `001ABB30`

`001ABB30` (324 B) is a TA-list body - `0019D8D0`/`001AB570`/`001AB8A0`/`001EDF00`/`00808C40` plus one vcall, `008C5F58`/`01F44830` and the `"EASTL vector"` literal. Interior anchor `001ABB87` (a `001EDF00` call).


## SWE2-EC7-62 update (2026-09-19) - `001A7630`

`001A7630` (148 B) is the `Asset_FindTextureObject` the TA page names - call-free `[rcx+0x50]` then `[rax+0x78]` chain walk for `rax==r8`, outer `[rcx]` advance to `rdx` bound. Interior anchor `001A7665` (the `[rax+0x78]` chain advance).



## SWE2-EC7-63 update (2026-09-19) - `001AB8A0`

`001AB8A0` (488 B) is a TA-list body - `0019D8D0`/`001AA4F0`/`001AA630`/`001AAF80`/`001AB350` plus two vcalls. Interior anchor `001AB906` (a `0019D8D0` call).



## SWE2-EC7-63 update (2026-09-19) - `001E1490`

`001E1490` (144 B) is a call-free `0x80`-stride `movups` record copier - 4-iteration unroll. Interior anchor `001E14B8` (the first `movups` load).



## SWE2-EC7-63 update (2026-09-19) - `001A4D20`

`001A4D20` (142 B) is a container-iterator body - `001A5A80`/`005FEC70` plus `008C2A40` and one vcall. Interior anchor `001A4D46` (a `005FEC70` call).



## SWE2-EC7-64 update (2026-09-19) - `001AAF80`

`001AAF80` (362 B) is an indirect-only record copier - byte-by-byte `[rdx+N]` -> `[rcx+N]` head, five vcall sites, `008C2A40`. Interior anchor `001AAF95` (the `[rcx]=al` copy head).



## SWE2-EC7-65 update (2026-09-19) - `001AA630`

`001AA630` (137 B) is a TA-list body - `0019D8D0` single call. Interior anchor `001AA686` (a `0019D8D0` call).



## SWE2-EC7-65 update (2026-09-19) - `001AB2C0`

`001AB2C0` (137 B) is a `001EDF00`-apply body - `001A4BF0`/`001EDF00`. Interior anchor `001AB318` (a `001EDF00` call).



## SWE2-EC7-65 update (2026-09-19) - `001BEB20`

`001BEB20` (137 B) is a `001EDF00`-apply body - `001A4BF0`/`001EDF00`. Interior anchor `001BEB78` (a `001EDF00` call).



## SWE2-EC7-66 update (2026-09-19) - `001A2E50`

`001A2E50` (133 B) is a resource-handle helper - `001FB470` single call. Interior anchor `001A2EC2` (a `001FB470` call).


## SWE2-EC7-67 update - `005FEC70`

`005FEC70` (128 B) is a ta-texture-animation body - `00210EC0` x2 plus `008C2608`/`008C2DA8` import pairs. Interior anchor `005FECBA` (an indirect call).

## SWE2-EC7-77 update (2026-09-20) - `00185A90` cursor-slot vector push measured

`00185A90` (86 B) is the slotted push_back: the record is
`rcx + 0xC38 + movsx dword[rcx+0xCB8]*0x20`; when its `[+8]` write
cursor is below `[+0x10]` the `{rdx, r8}` pair is stored there and
the cursor bumps `0x10`; otherwise `001858A0` grows the vector.
Interior anchor `00185AB3` (the `+8` cursor load).

## SWE2-EC7-118 update (2026-09-21) - `006800F0` measured

`006800F0` (10 B) is the
three-instruction list push
`0063B4D0` runs: `*rdx =
*r8; *r8 = rdx` - node
`rdx` takes the head's
target and becomes the new
head.
Interior anchor `006800F6`
(the head store).

`001A5030` (283 B) is the `basic_string::append(str, pos, count)` `001A5150` and `0020D1E0` lean on: `pos > [rdx+0x10]` throws `invalid string position`, `count` clamps to `srclen - pos`, `~destlen < count` or `destlen + count > ~1` throws `string too long`; `[rcx+0x18] < newlen` grows through `00195670`, the `+0x18 >= 0x10` SSO test swaps both strings to their heap pointers, and the tail copies `rsi` bytes into the destination - the MSVC append behind the ta-list path build.

Interior anchor `001A50BE` (function `001A5030`).

`001A5030` (283 B) is the `basic_string::append(str, pos, count)` `001A5150` and `0020D1E0` lean on: `pos > [rdx+0x10]` throws `invalid string position`, `count` clamps to `srclen - pos`, `~destlen < count` or `destlen + count > ~1` throws `string too long`; `[rcx+0x18] < newlen` grows through `00195670`, the `+0x18 >= 0x10` SSO test swaps both strings to their heap pointers, and the tail copies `rsi` bytes into the destination - the MSVC append behind the ta-list path build.

Interior anchor `001A50BE` (function `001A5030`).

`001A9940` (227 B) is the lazily-built `phyremaps.txt` holder this page names: TLS slot `gs:[0x58] + [02EAED3C]*8` version-checks against `01F811C0`'s init counter; first entry builds the `std::map` sentinel at `01F81188` (vtable `008F6500`, self-linked head `01F81190`) inside `008092FC`/`0080929C` init-once guards, `00677340` parses `/GameData/D3D11/ArtData/shared/phyremaps.txt` into it, and every later call just returns `01F81188` - the shared texture-name redirect the TA resolution uses.

Interior anchor `001A998D` (function `001A9940`).

`001E1670` (987 B) is the TA-list object constructor `001A5B30` allocates: it installs vtable `009012C0` (RTTI locator `01CED7F0`), constructs the EASTL vectors at `+0x18` and `+0x38` (allocator tag `008C5F58`), carves the `+0x58` byte-run and the `+0x78` slot through the embedded `008F6500` allocator's `+0x10` vcall, seeds the scale fields `+0x15C..+0x168`, `+0x1D8..+0x1E4`, `+0x1F8` and `+0xC8` with 1.0f, packs counts `0x01010100`/`0x100`/`4` into `+0xC0`/`+0x250`/`+0x230`, and when the `01F82DA8` freelist count is nonzero pops a node off `01F82D88` through `0016D6D0`/`0016DA60`/vtable `+0x18`/`00199DB0` before registering the new object with `0016D6A0` and storing the back-link `+0x10`/`[node+8]`.

Interior anchor `001E19EC` (function `001E1670`).

`0016D6B0` (10 B) is the argument-shift thunk the TA-list constructor's freelist path and the save-container contract share: it moves `rdx` into `rcx` and tail-jumps through the `008C2B40` indirect pointer (holding `01CCEE88` in the verified image).

Interior anchor `0016D6B3` (function `0016D6B0`).

`001A7770` (213 B) is the per-node refresh `001A5B30` runs over the `[+0x498..+0x4A0]` list: each node gets `[+0x30]` cleared, `[+0x484] -> [+0x28]` and `[+0x480] -> [+0x24]` copied, and when `[+0x488]` is nonzero the IAT call at `01CCEF20` supplies a scalar so `[+0x24] += (2 * [+0x488] * f) / 22020000.0 - [+0x488]` - the randomized jitter - before `0016D6D0` walks to the next node

Interior anchor `001A7819` (function `001A7770`).

`0020D1E0` (139 B) is the string-assign `0020DE30` uses on the `{+0x10 length, +0x18 capacity}` records: a range-overlap test between the two buffers picks `0020DC70` (overlap-safe copy) or `001A5030` (plain move), then the destination is reset to its inline form (`+0x18 = 0xF`, `+0x10 = 0`, NUL) and `001A4C90` commits the text - the aliasing-aware assign the TA list parser's string records go through.

Interior anchor `0020D226` (function `0020D1E0`).

`0020DC70` (442 B) is the MSVC `std::string` assign/insert primitive `0020D1E0`'s path joins call: both positions bounds-check against `+0x10` with `invalid string position` throws, the `~r8`/`rdi` overflow pair raises `string too long`, `00195670` grows the buffer when `+0x18` capacity (SSO threshold 0x10) cannot hold the result, and the source span copies in before the new length and terminator land - the STL string core the list-builder links against.

Interior anchor `0020DCBB` (function `0020DC70`).

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-ta-texture-animation-lists-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00180830` | 60 B | keeps `rcx`, `edx` and `r8d`, calls `001A9930` with the incoming registers still in place, then tail-jumps to `001A9DD0(that result, rcx, edx, r8d)` | `00180847`, `0018084F`, `00180855`, `00180867` |
| `00180900` | 115 B | calls `001A9930` with the incoming registers still in place, then calls `001AA240(that result, rcx, dl, r8b, r9d, the fifth (stack) argument as f32, the low bytes of the sixth and seventh (stack) arguments)` and returns its `rax` | `00180921`, `00180926`, `0018094B`, `00180955`, `00180959` |
| `001809A0` | 52 B | when byte `01F7F50D` is 0 and `0018CA40()` returns non-null, stores 1 in byte `01F7F50D` and tail-jumps to `0018C3C0(0018CA40())`; otherwise returns without work | `001809A4`, `001809AD`, `001809B7`, `001809BE`, `001809CA` |
| `001A1920` | 98 B | measures the zero-terminated string at `r8` (length 0 when its first byte is 0) and calls `001A5150(rdx, r8, length)` with `r9` also holding `rdx` and a zero fifth (stack) argument; then sets `rcx`'s qword `+0x18` to 0xF, qword `+0x10` to 0 and byte `+0` to 0, calls `001A4C90(rcx, that result)` and returns `rcx` | `001A1949`, `001A1956`, `001A195B`, `001A1974`, `001A1979` |
| `001A4FE0` | 70 B | returns without work when `rdx` is null; otherwise, on the qword triple at `rcx+0x90`, when qword `+0x98` is below qword `+0xA0` (unsigned) advances `+0x98` by 8 and stores `rdx` at its old value (the store skipped when that old value is null), else calls `001AB570(rcx+0x90, qword +0x98, the address of the saved rdx)` | `001A4FEE`, `001A4FFC`, `001A5006`, `001A500F`, `001A501C` |
| `001A7460` | 52 B | when byte `+0x140` of `rcx` is non-zero, walks 0x20-byte entries from qword `+0x120` up to qword `+0x128` and returns the address of the first entry whose first qword points at a qword equal to `rdx`; returns 0 when the byte is 0, the range is empty or no entry matches | `001A7467`, `001A7479`, `001A7483`, `001A7488`, `001A7491` |
| `001A9DD0` | 64 B | stores a qword at `rdx+0xD0` chosen by `r9d`: 1 stores 3, 2 stores 2, 3 stores 1, any other value stores 0 | `001A9DD4`, `001A9DDA`, `001A9DE0`, `001A9DE4`, `001A9E04` |
| `001AA240` | 120 B | maps the fifth (stack) argument 0 to 0, 2 to 2, 3 to 3 and any other value to 1, then calls `001E69A0(rdx, r8b, r9b, the mapped value, the sixth (stack) argument as f32, the low bytes of the seventh and eighth (stack) arguments)` and returns its `rax`; `rcx` is not used | `001AA255`, `001AA25C`, `001AA263`, `001AA28A`, `001AA2AD` |
| `001AA4F0` | 125 B | copies 0x30-byte records backwards, from the range `rcx` to `rdx` into the range ending at `r8`: per record bytes `+0` to `+5` and `+0x28` are copied directly and `+8` through `0019DDD0(destination+8, source+8)`; returns the destination start (`r8` when `rdx` equals `rcx`) | `001AA508`, `001AA514`, `001AA520`, `001AA549`, `001AA552` |
| `001AB350` | 115 B | when `rdx` is below `r8` (unsigned), visits each 0x30-byte record from `rdx` to `r8` (count (`r8`-`rdx`-1)/0x30+1); for each record whose qword `+8` is non-null calls slot `+0x18` of the vtable held in its qword `+0x20`, with `rcx` = the address `record+0x20` (not the qword there), `rdx` = qword `+8` and `r8` = (qword `+0x18` minus qword `+8`) AND ~7 | `001AB353`, `001AB37C`, `001AB393`, `001AB3A6`, `001AB3AA` |
| `001ABC80` | 89 B | returns without work when `r8d` is negative (signed); otherwise calls `001AC810(rcx, r8d)`, then `001AD7B0(that result, rdx, r9d, the fifth (stack) argument)`, and stores byte 1 at offset `2*r9d - 2` (sign-extended) of the buffer the result's first qword points at | `001ABC83`, `001ABC9D`, `001ABCB3`, `001ABCBB`, `001ABCCF` |
| `001ABCE0` | 89 B | returns without work when `r8d` is negative (signed); otherwise calls `001AC810(rcx, r8d)`, then `001AD6E0(that result, rdx, r9d, the fifth (stack) argument)`, and stores byte 1 at offset `2*r9d - 1` (sign-extended) of the buffer the result's first qword points at | `001ABCE3`, `001ABCFD`, `001ABD13`, `001ABD1B`, `001ABD2F` |
| `001AC480` | 34 B | calls `001AD130(rcx, rcx+0x16C)`, then stores byte 1 at `rcx+0x250` | `001AC486`, `001AC490`, `001AC495` |
| `003ABD20` | 39 B | walks the list headed by qword `02B3F508` through each node's qword `+0x10` and returns the address `+0x20` of the first node whose byte `+0x23` equals 5; returns 0 when the head is null or no node matches | `003ABD27`, `003ABD30`, `003ABD36`, `003ABD3F`, `003ABD42` |
| `00467A70` | 27 B | copies dword `02CA5FF4` to dword `02CA5FF8`, stores 0 in dwords `02CA5FFC` and `02CA6000`, and returns 0 | `00467A76`, `00467A7C`, `00467A7E`, `00467A84` |
| `00467B60` | 71 B | subtracts f32 `02AED570` from 20.0 (`00901988`), takes the absolute value in double precision (sign mask `01CEBD80`) and passes it as f32 to the function pointer at `008C2BD8`; multiplies the returned f32 by -16.0 (`00D12518`), truncates it to an int and stores that int, sign-extended and shifted left 32, in qword `02EBB6C8` | `00467B6C`, `00467B77`, `00467B82`, `00467B88`, `00467B9B` |
| `00468070` | 84 B | takes the 0x30-byte record at qword `+8` of `rcx` and advances that qword by 0x30 (no bound check); writes qword `+0` = 0x10000002, qword `+8` = 0, dword `+0x10` = 0, dword `+0x14` = 0x10000000, dword `+0x18` = 0x1000404, dword `+0x1C` = `r8d` OR 0x6C010000, and copies the four dwords at `rdx` to `+0x20` through `+0x2C` | `00468074`, `0046807F`, `00468089`, `004680A4`, `004680BF` |

## No-reference bodies homed by the table that reaches them (FABLE, 2026-10-03)

*No page cited these functions and no census-listed instruction calls or jumps to them: each is reached through data or through code this page documents. Each sentence states what the body does (access and representation, not purpose) and ends with the reference that reaches it; the anchors are instructions inside the body that do it. Handed over by SWE2-EC7 and read whole by FABLE against the certified image; verified by [`apply.py`](../../_index/candidates/fable-noref-ta-texture-animation-lists-data-1003/apply.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic, and every named reference holds or forms the body's address at the bytes.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `008A69A0` | 38 B | calls `001A49C0` with `rcx` = `01F81188` and `rdx` = qword `01F811A0`; its address is formed into `rcx` by `001A9940` + 0x87 for the `00808B90` exit registration at +0xCD | Interior anchor `008A69AD`; Interior anchor `008A69B4`; Interior anchor `008A69BB` |

## Homed bodies: functions reached only indirectly whose callees this page cites (FABLE, 2026-10-03, F homing)

*No page cited these functions and none of their callers is documented: they are reached by table or pointer dispatch or through undocumented callers. Each one calls something this page documents, which the sentence names. Each sentence states what the body does (access and representation, not purpose); the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's F homing pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-ta-texture-animation-lists-homing-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0019D420` | 240 B | returns at once when `edx` is 0; otherwise, for `edx` destination records of stride 0x130 starting at `rcx`, skips a null destination and else copies 0x100 bytes from `r8` to it, calls `0019D8D0(dest+0x100, r8+0x100)` and copies qword `+0x120` and byte `+0x128` from `r8`; the same source `r8` is used for every record | Interior anchor `0019D422`; Interior anchor `0019D473`; Interior anchor `0019D4D0`; Interior anchor `0019D4DC`; Interior anchor `0019D4FA` |
| `0019D970` | 183 B | copies 0x100 bytes from `rdx` to `rcx` in two 0x80-byte passes, calls `0019D8D0(rcx+0x100, rdx+0x100)`, copies qword `+0x120` and byte `+0x128` from `rdx` to `rcx` and returns `rcx` | Interior anchor `0019D9A1`; Interior anchor `0019D9E9`; Interior anchor `0019D9F9`; Interior anchor `0019DA05`; Interior anchor `0019DA19` |
| `001AAE70` | 102 B | calls `001AB350(rcx, qword [rcx], qword [rcx+8])`, then when qword `[rcx]` is non-null releases it through virtual slot `+0x18` of the object at `rcx+0x18` with size ((qword `+0x10` minus qword `+0`) / 0x30, signed) * 0x30 | Interior anchor `001AAE89`; Interior anchor `001AAE92`; Interior anchor `001AAEA5`; Interior anchor `001AAECB` |
| `001AD0C0` | 112 B | when qword `rcx+8` is below qword `rcx+0x10` (unsigned), advances qword `rcx+8` by 0x30 and, if the old value is non-null, copies dword `[rdx]` and word `rdx+4` into it, calls `0019D8D0(old+8, rdx+8)` and copies byte `rdx+0x28` to `old+0x28`; otherwise calls `001AB8A0(rcx, qword rcx+8, rdx)` | Interior anchor `001AD0DB`; Interior anchor `001AD0EA`; Interior anchor `001AD10C`; Interior anchor `001AD115`; Interior anchor `001AD120` |
| `001B6A70` | 213 B | walks the list from qword `rcx+0x80` until it reaches `rcx+0x78`, calling for each node `00185A90(00189120(), the address loaded at 001B6AA0, node qword +0x20)` and stepping with `0016D6D0(node)`; then walks the chain from qword `rcx+0x88` (next at `+8`) calling `00220390(rcx+0x70, link qword +0)` and releasing each link through virtual slot `+0x18` of the object at `rcx+0xa0` with size 0x28; finally points qwords `rcx+0x80` and `rcx+0x78` at `rcx+0x78`, zeroes qword `+0x88`, byte `+0x90` and dword `+0x98`, and returns 1 when dword `+0x60` is 0, else 0 | Interior anchor `001B6AAA`; Interior anchor `001B6AB2`; Interior anchor `001B6AD7`; Interior anchor `001B6B15`; Interior anchor `001B6B3C` |
