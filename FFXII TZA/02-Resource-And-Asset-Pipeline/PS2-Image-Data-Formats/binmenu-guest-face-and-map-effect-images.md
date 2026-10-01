---
system: The eighteen headerless `bin_menu` image units — `face_guestNN`, `map_efeNN`, `mini_guest_face`
category: 02-Resource-And-Asset-Pipeline
status: AUDITED
owner_layer: CodeDomain:Presentation.Menu
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-21 (FABLE) - 16 addresses cited - 4 data, 9 entry, 2 interior, 1 literal, every one resolving into a known section of the authority image.
    **This records a check performed on that date, NOT the method of the
    original derivation**, which this block never carried; see this
    document's own evidence section for that.
corpus_validated: "all 162 shipped files (18 logical units x 9 locales) extracted from FFXII_TZA.vbf, 2026-09-16; 0 structural failures; kind-7 registry ids 0x0D-0x20 verified against the exe path array"
archive_formats:
  - "binmenuimage | explained | the eighteen headerless raw 8-bit bin_menu images face_guest07-16 (2x2-upscaled, byte-doubled), map_efe00-06 and mini_guest_face (undoubled) (.bin member; its seven leading patterns are pixel bytes, not magics; wording narrowed 2026-09-30 per SWE2-AUDIT-SEM N1): the file is the pixel buffer, section 2; request and binding, section 4 (mini_guest_face is kind-7 id 0x0D)"
  - "itemclut | explained | Item_Clut.bin (.bin member): 7 palettes x 256 x 32-bit RGBA (7,168 B) - (kind 7, 0x99) in the 00291C80 request loop, bound at object +0xE0 by 00291D90, indexed (id >> 6) << 10 by 00292390, section 5b"
last_reviewed: 2026-09-16
audit:
  passes: 1
  last_pass: 2026-09-17
  last_pass_state: falsification-pass
  crossref_clean: false        # 2026-09-30 (SWE2-DATA): false until the pass-22 UNACCOUNTED NEIGHBOUR findings are accounted (FRONTIER-REQ-SWE2-DATA-PASS22-DEBT; OPUS-REQ-DATA-PASS30-CROSSREF-CLEAN-0930)
  reopened_count: 0
function_families:
  - "MMSG value receiver adapters | B | members/mmsg-value-receiver-adapters.tsv | 28 | PROVED BY FORM with the full per-member semantics in the table: the 28 lea targets of the per-kind dispatcher 002FA560, each exactly movsxd rdx,ecx ; mov ecx,K (xor ecx,ecx for K=0) ; mov [rip+02EC3D80+8K],rdx ; jmp 00238640 - sign-extend the incoming value, store it in slot K of the group table this page's chain documents, and forward (K, value) to the record fixup. K runs 0..0x1B contiguous and the 28 globals are the consecutive table slots, 28 of 28 form match, all tails 00238640. NEAR-MISS CONTROL: the 7 other census bodies in 002F7000-002F8000 all fail the form check. NOT dispositioned: 002FA560, 002385D0, 00384420, 00238640, 003845F0, the record table 02F973C0, and what each slot K's value means. Selector: members/select_mmsg_receivers.py"
---

# The eighteen `bin_menu` image units — `face_guestNN`, `map_efeNN`, `mini_guest_face`

> **Raw single-channel 8-bit image buffers — no magic, no header, no CLUT.** These are the
> eighteen "byte-doubled" `.bin` units of the signature census. The doubling is real only in
> `face_guestNN`, and it is a **2x2 nearest-neighbour upscale** — each source pixel is written
> into a uniform 2x2 block — not a channel duplication. `map_efeNN` and `mini_guest_face` are
> ordinary resolution images whose byte-pair correlation is content, not structure.

**Corpus validation, before anything else.**

||| |
|---|---|
| files examined | **162 of 162** shipped copies in `FFXII_TZA.vbf` — 18 logical units × 9 locales |
| directory | `ps2data/image/ff12/myoshiok/<lang>/bin_menu/` |
| structural failures | **0 of 162** — every `face_guest` in every locale is 2x2-uniform to the byte |
| kind-7 ids | `0x0D` mini_guest_face · `0x0E`–`0x14` map_efe00–06 · `0x17`–`0x20` face_guest07–16 |

Decoder/validator: `Tools/work/DATA/binimg/decode_binimg.py` → `decode_binimg.out.txt`,
renders in `Tools/work/DATA/binimg/renders/`.

## 1. What the player sees

- **`face_guest07`–`face_guest16`** — the guest-character portraits shown in the party/status
  menu pages (the "Guest" frame). Ten files ship, but only six portraits are distinct: the
  corpus is pairwise-duplicate — `08≡09`, `10≡13`, `11≡12`, `14≡16` — presumably front-end
  slots that share art. Byte-identical across all 9 locales.
- **`map_efe00`–`map_efe06`** — the field-effect indicator icons on the map/field screens:
  `efe00` "HP↓" arrow, `efe01` "MP↓" arrow, `efe02`–`efe05` item/action-class icons
  (sword, staff, armour, potion) in normal + crossed-out states, `efe06` a magnet icon.
  `efe00`/`efe01` carry text and are the only `map_efe` files with locale variants
  (`de`/`es`/`fr` — the "HP"/"MP" lettering is localized; `efe01` additionally splits `es`/`fr`).
- **`mini_guest_face`** — the mini portrait strip used in compact party displays; six pages
  of four mini faces each (24 cells). Three locale variants (`us` distinct, `es`/`fr` shared).

## 2. The layout — the file IS the pixel buffer

There is no envelope at all. Each file is a raw row-major byte image; size = stride × rows
exactly:

| family | file bytes | stored w×h | structure |
|---|---:|---|---|
| `face_guestNN` | 12,288 | 128×96 | every 2×2 block uniform → logical **64×48**, 2× upscale both axes |
| `map_efeNN` | 16,384 | 128×128 | two stacked 128×64 cells (normal / disabled-or-variant icon state) |
| `mini_guest_face` | 73,728 | six 128×96 pages | each page a 2×2 grid of 64×48 cells → 24 mini portraits |

Byte meaning: **one byte per stored pixel, a single 8-bit channel**. Histograms are
continuous-tone (`face_guest07` uses 238/256 values; `map_efe00` and `mini_guest_face` use
all 256) — photographic intensity data, not a sparse index set.

## 3. The doubling question — horizontal upscale vs channel duplication

The census recorded *"every byte doubled over the first 32"*, which is byte-pattern-ambiguous
between a horizontal pixel upscale and two-channel interleave. The data settles it in three
independent measurements (all `us` copies; identical in every locale):

| measurement | `face_guest07` | `map_efe00` | `mini_guest_face` |
|---|---:|---:|---:|
| horizontal pair equality `d[2i]==d[2i+1]` | **1.0000** | 0.7645 | 0.629 |
| even-row pair equality `row[2i]==row[2i+1]` | **1.0000** | 0.0938 | 0.319 |
| every 2×2 block uniform | **all 3,072** | no | no |

- `face_guest` is doubled **on both axes**: if the pairs were two channels of a 64×96 image,
  successive rows would be independent — instead every even row equals the odd row under it.
  De-duplicated to 64×48 the buffer is a coherent guest portrait (`renders/
  face_guest07_logical_64x48.png`); read raw at 128×96 it is the same portrait doubled.
  **Verdict: a 64×48 image stored at 128×96 by 2× nearest-neighbour upscale.**
- `map_efe` is **not** doubled. The ~0.76 pair-equality is smooth-content coincidence —
  anti-aliased icon art where neighbours correlate. Its two 128×64 cells differ (1,274–3,959
  differing bytes) and render as distinct icon states (`renders/map_efe0N_128x128.png`).
- `mini_guest_face` is **not** doubled either: six pages of four real 64×48 portraits each;
  left/right cells of a row differ throughout the face region — 24 distinct mini portraits,
  not 12 duplicated pairs.

## 4. Native plumbing

All eighteen are kind-7 resources. The `us` path array at **`0x01EC73A0`** resolves:

| id | path |
|---|---|
| `0x0D` | `…\us\Bin_Menu\mini_guest_face.bin` |
| `0x0E`–`0x14` | `…\us\Bin_Menu\map_efe00`–`06.bin` |
| `0x17`–`0x20` | `…\us\Bin_Menu\face_guest07`–`16.bin` |

Shared resource API (verified in the exe):

| function | role |
|---|---|
| `0032E620` | resource request `(kind=7, id, element, outRect)` |
| `0032E400` | per-kind descriptor/size lookup `(kind, id)` |
| `002F8040` | loaded-state check — `g_slotTable[0x02EC3D80 + id*8] != 0` |
| `002F83E0` | release by id |
| `002FA560` | per-kind dispatcher (kind 0–0x1B) → `002385D0` |
| `00238640` | indexes the per-kind record table `0x050E53C0 + kind*8` → `003845F0` |
| `003845F0` | record pointer fixup: `dword` offset fields at `rec+0xC/0x10/0x14/0x18/0x1C` relocated to absolute (plus a sub-offset table via `+0x14`) |

The record-fixup shape (`+0xC…+0x1C` self-relative offsets) shows kind-7 loads produce a
**record whose fields point into the blob**; for these headerless units the blob is the
pixel buffer itself. The per-kind descriptor table `0x050E53C0` is **runtime-populated**
(null in the offline image), so the texture-format descriptor for these ids is not
recoverable statically — §5 states the consequence.

**Signature census note (2026-09-16):** `face_guest15.bin` leads with the bytes `2F 2F 32 32`
(`//22`), which the `.bin` signature census counted as a nine-entry family. **It is not a magic**
— it is the first four doubled bytes of the 2×2-upscaled pixel payload (`0x2F2F 3232` =
texels `0x2F,0x32` replicated horizontally). Every copy across the nine locales carries the same
first texels, which is why the pseudo-signature is stable. The `//22` rows in
`bin-signature-census.tsv` already read `NOT_A_MAGIC`; this package's decode is the explanation.

`0032E400`, `0032E620` and `003845F0` are shared APIs, not internals of this family:
`0032E400`/`0032E620` are the generic kind-7 descriptor and request entries (their other
callers live in ActorEntity, Input, Presentation and Save/Load), and `003845F0` is the
generic record-relocation pass (its other callers live in CombatAI and CombatAction).
Those callers are fellow API consumers, not readers of these images.

## 5. Evidence status and falsification

- **Established (native):** the eighteen ids↔paths in the kind-7 registry; the request /
  loaded-state / release plumbing; the record-offset fixup proving the loaded object is a
  record-with-pointers, i.e. these blobs arrive as payload, not self-describing images.
- **Established (corpus):** 162/162 files validated, zero failures; `face_guest` 2×2-uniform
  in all locales; locale-split pattern (face_guest invariant; only text-bearing `efe00`/`01`
  localize) matching the field-effect-icon reading.
- **Established (measurement):** the doubling is a **2×2 nearest-neighbour upscale** in
  `face_guest` — not channel duplication; `map_efe`/`mini_guest_face` are undoubled images.
- **Open (static limit):** **palette ownership.** No CLUT ships in these files, and no
  sibling resource is bound to ids `0x0D`–`0x20` in the registry. The byte channel could be
  direct intensity (A8/L8-class) or a CLUT index against a palette delivered by the
  consumer's material; the descriptor table that would decide it (`0x050E53C0`) is filled at
  runtime. Adjacent `bin_menu` palette resources (`item_clut.bin` = seven 256-entry
  ~~RGBA5551 banks~~ 32-bit RGBA banks (7 × 256 × 4 = 7,168 bytes; corrected 2026-09-29, SWE2-DATA, §5b), `monotone_chr.bin` = `CLT2`, `fontcolor.bin`) ship only in the `in`/`ch`
  trees and belong to item icons and fonts — none is evidence of a palette for this family.
  Their loaders are bound in [the loader-bound `.bin` families](loader-bound-bin-families.md) —
  `monotone_chr`'s loader grafts the `clutpack_ys` palette slot at `*(0209AC30)+0x390`, so its
  palette is proven delivered by an adjacent pack, not by this file.
  Resolving it needs an engine-in-loop read of the descriptor or the draw-time texture
  format.
- **Open:** the exact guest-slot → `face_guestNN` selection table (the guest-face requester
  computes its id; the `0xD10C98` slot table near the guest widget maps slots to `0xDA`–`0xDF`
  ExFont `.btm` resources, i.e. the guest status *fonts*, a separate mechanism).
- **Falsifier:** if any `face_guest` in any locale fails the 2×2-uniform check, or the
  registry ids move off these paths, the decoder reports it.

## 5b. The adjacent item palette — `bin_menu/Item_Clut.bin` (2026-09-29, SWE2-DATA)

*`OPUS-REQ-DATA-BUCKET-MEMBER-FORMATS` (the `.bin` bucket's member `itemclut`); check
[`b5_item_clut.py`](../../_index/candidates/bucket-members-0929/checks/b5_item_clut.py), 43 checks, FAILS 0.*
Not part of the eighteen-image family above; recorded here because §5 named it. Two copies (`ch`,
`in`), byte-identical, **7,168 bytes = 7 palettes × 256 entries × 4 bytes RGBA**; alpha is `0x80`
(the PS2 full-opacity value) in 1,791 of 1,792 entries and `0x00` once (palette 3, entry 0). §5's
"RGBA5551" reading was wrong: the size admits only 4-byte entries.

**Request.** A loop in `00291C80` (ledger label Input; the body is a kind-7 resource loader, the
LABEL-UNSUPPORTED case pass 22 section 4.2 already lists) requests kind 7 ids `0x98`–`0xA1` — `itemgra_c.tm2`,
`Item_Clut.bin` (`0x99`), `Item_Gra00`–`07.as7` — through `0024AB90` (a jump to `0032E400`) with
`lea edx, [rbx+0x98]` (`00291CB8`, `00291CF3`) and `0032E620` (`00291D04`), filling 16-byte slots
of the table at `0209BEA0` (a raw sweep finds only `00291C60`, `00291C80` and `00291D90` touching
it). The handler `00291D90` copies the slots into its object, which puts the `Item_Clut` data at
object `+0xE0`.

**Reader.** `00292390` loads `+0xE0` (`00292506`, `002926D0`) and indexes it by the item graphic id:
`(id >> 6) << 10` bytes (`sar` at `00292748`, `shl 0xa` at `0029278A`, `add` at `00292790`) — the
graphic's group picks one 1,024-byte palette.

**Not claimed.** Eight `Item_Gra0N.as7` groups ship against seven palettes; a group-7 graphic id
would index palette 7, past the end of the file. Whether any shipped id reaches group 7 was not
checked.

## 6. Out of scope

The remaining magic-less `.bin` shapes — 14 count-prefixed, 4 EBP section bodies, 9
leading-zero — and the six unnamed token families (`QST1`, `//22`, `hcom`, `hodr`, `EVME`,
`dP<d`) are separate packages (`OPUS-REQ-SWE2-DATA-SIX-UNNAMED-BIN-FAMILIES` and follow-ons);
this page covers the eighteen byte-doubled units only.

## Crossings into other layers — pass 22 (SWE2-DATA, 2026-09-29)

- **Input — LABEL-UNSUPPORTED, body read.** The `Item_Clut.bin` requester `00291C80` is labelled
  Input in the ledger, but its body is a kind-7 resource loader: a ten-pass loop over the request
  API (§5b); the page's claim is the palette file it fetches.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-FRONTIER for SWE2-DATA, 2026-09-30)

*Added 2026-09-30 (SWE2-FRONTIER, executing SWE2-DATA's pass-22 debt). These are the layers pass 22 still reported for this page at HEAD `4dfe4a006`. Every edge was listed in full, and each cited helper was read at its instructions or is named as the page reads it.*

**WorldAreaField, World, ActorEntity, Presentation, Save_Load_Settings, Script_VM_Native_Bridge — CLIENT (24 edges).** Most of these edges are other layers' loaders using the per-kind size lookup `0032E400` (`[022C51F0][kind][id]` for `id < 0x400`, else a fallback call) and the request queue `0032E620`. The callers are `MapRef_BeginLoadResources` (`00268750`), `003319D0`, `00378030`, `00379A10`, `AreaArd_LoadOrUnloadFieldResource` (`003EA820`), `00378540`, `ActorResource_BeginManagerResourceSetLoad` (`0032FCA0`), `ActorResource_BeginPrimaryPayloadLoad` (`00330310`), `003306E0`, `003B2310`, `003B53C0`, the save-slot loader `002EF300` and the script adapters `0050DF70` / `0050DFE0`. The rest go through `AreaData_BindAndRebaseSectionDescriptor` (`003845F0`). It rebases the descriptor's offsets (`+0xC`, `+0x10`, `+0x18`, `+0x1C` by adding the base) and re-encodes only its `+0x14` pointer through the image-address codec (`0020E620`), then walks the entries through `003846F0`; `00236C30`, `BattleData_SetAreaArdSectionCategory` (`0023A160`), `00238640` and `003847B0` call it. These are shared loaders and a shared rebase; the image formats stay this page's.

**CombatAI and CombatAction — CLIENT (2 edges).** `GambitTargetDefinition_BindAndBuildMenuLookup` (`00238880`) and `00237FC0` call the same section rebase `003845F0`, and that is their only tie here.
