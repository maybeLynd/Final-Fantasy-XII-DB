---
system: The `.btm` exfont glyph bitmap — `ExFont/font_stf_*.btm`
category: 02-Resource-And-Asset-Pipeline
status: DOCUMENTED — every register row is closed (owner re-status 2026-09-30, OPUS, on SWE2-CONTRACT's reconciliation; superseded readings are marked on the page) — the texel bit depth (RC-26: 4 bpp), the glyph-table owner (RC-27: fontpack_fs.bin; ids 130-135 never requested, correcting §3 and §4) and the glyph-coverage census (RC-28, with its round-2 leftovers: language arms, the refused KR/CN load, the staff roll never drawing the accented glyphs) answered; the refused KR/CN .btm answered (RC-37: the request still completes and the ready bit is set, so the staff roll does not wait and draws from a 0-byte sheet; open only as a limit: what the allocator returns for size 0); the record's unknown byte has no reader (UQ-364's residual); the c-family naming answered from fontlist.ah (status line current 2026-09-30, SWE2-CONTRACT)
owner_layer: CodeDomain:Presentation.Font
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-21 (FABLE) - 20 addresses cited - 2 data, 16 entry, 2 interior, every one resolving into a known section of the authority image.
    **This records a check performed on that date, NOT the method of the
    original derivation**, which this block never carried; see this
    document's own evidence section for that.
corpus_validated: "all 12 shipped .btm files extracted from FFXII_TZA.vbf and hashed, 2026-09-14; consumer chain read at 00365810 + glyph-run page"
archive_formats:
  - "btm | explained | Raw exfont glyph texels — no magic/header; indexed externally by the glyph-table pixelOffset into buffer slot 022CBE00+0x110."
last_reviewed: 2026-09-30
audit:
  passes: 1
  last_pass: 2026-09-17
  last_pass_state: falsification-pass
  crossref_clean: false
  reopened_count: 0
---

# The `.btm` exfont glyph bitmap — `ExFont/font_stf_*.btm`

> **A raw glyph pixel sheet — no magic, no header.** The first four zero bytes are *pixel data*,
> not a signature: the file is a flat texel buffer that the font subsystem indexes through the
> **external** glyph table's `pixelOffset` field. Declaring a format off the leading zeros would
> have been a mistake — the body read is what the earlier disposition correctly demanded.

**Corpus validation, before anything else.**

|| |
|---|---|
| files examined | **12 of 12** shipped `.btm` entries — 6 names × `in`/`ch` copies = **6 distinct contents** (hash-identical pairs); ships only in `in` and `ch` |
| names | `font_stf_a_normal`, `font_stf_a_shadow`, `font_stf_b_normal`, `font_stf_b_shadow`, `font_stf_c_shadow`, `font_stfc_normal` |
| size range | 29,184 B (`font_stf_b_*`) – 42,240 B (`font_stf_a_*`) |
| first dword | `00 00 00 00` in 12 of 12 — **pixel data, not a magic** |
| first nonzero byte | `0x34` (`font_stf_a_normal`) — sparse early glyph cells |

## 1. What the player sees

The `font_stf` family is the **staff-roll / extended font set** (the `f1` font family in the
kerning census — `font_stf_a/b/c` each carry 1,237 kerning pairs). `_normal` is the face,
`_shadow` the drop-shadow variant. The `.btm` is the pixel sheet those glyphs rasterize from.

## 2. The layout

**There is no in-file header this pass can defend.** The buffer is a contiguous texel payload;
its interpretation lives entirely in the companion glyph table:

```struct BtmFile base=file
+0x00  u8[]   texels   raw glyph pixel rows, packed back to back
```

- The leading `0x00..0x34` zeros are the first glyph cells (blank / space / padding), not a
  signature block — `font_stf_a_shadow` has nonzero bytes as early as `+0x15`.
- Byte histogram is pixel-like: `0x00` dominant (~74%), `0xFF`/`0x06`/`0x60`/`0x66`/`0x27`… —
  sparse ink on a zero field.
- The glyph table record (12 B, held at `[022CBE00 + 0x10 + fontId*8]`, table `+0x04` count,
  records at `+0x10`) carries `{u16 charCode, u8 cellW, u8 cellH, u8 ?, u32 pixelOffset}` — and
  **`pixelOffset` indexes into the `.btm` buffer** at `[022CBE00 + 0x110 + fontId*8]`
  ([glyph-run page](../../99-Unresolved-Residual/Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md) §The font glyph table record).

So the *format contract is two-sided by construction*: `.btm` is meaningless without the glyph
table that owns its `pixelOffset`s, and the bit-depth is whatever the cache-fill produces — the
consumer rounds cell dims to pow2 (8..128) and copies the cell into its own texture.

## 3. The loader contract — **the buffer-to-slot binding is instruction-verified**

|| |
|---|---|
| loader | `00365810` — iterates the 12-id table at `00D10C98` = `{130..135, 218..223}` |
| request chain | `0032E400` size (`00365882`) + `0032E620` request (`003658C7`), kind `0x7`. The pair is the generic resource-pool API — also called by ActorEntity (`0032FCA0`, `00330310`, `003306E0`), Presentation (`003B2310`, `003B53C0`), Script_VM_Native_Bridge (`0050DF70`, `0050DFE0`), Input (`00291C80`) and Save_Load_Settings (`002EF300`) clients for unrelated resources; fellow API consumers, not `.btm` readers |
| buffer slot | `[022CBE00 + 0x110 + slot*8]` — the `.btm` half of the 12 ids |
| ready bit | `[022CBE00 + 0x240]` bit `slot` — set on completion |
| glyph table slot | `[022CBE00 + 0x10 + fontId*8]` — companion resource (the `fontpack`/`fontheader` half, ids 130–135) *(superseded: ids 130–135 are never requested; the glyph tables come from `fontpack_fs.bin`, RC-27)* |
| consumers | glyph measure/draw at `00364210`/`00364380`/`003649A0` — read `pixelOffset` into the `.btm` buffer *(`00364380` is the `.btm` requests' completion callback, not a glyph measure, RC-27)* |
| magic check | none possible — no magic exists |

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| whole buffer | glyph cache-fill via `pixelOffset` | — | cell dims rounded to pow2 (8..128) by `00364210` | — |
| leading zeros | — | — | — | pixel data, not a signature |

*(narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../../_index/candidates/auditspec-review-dd-02-b2-0930/REVIEW.md) correction 2: the §3 glyph-table-slot and consumers rows above and the §4 `00364380` row carry their answers.)*

## 4. Key addresses

| Address | Role |
|---|---|
| `00365810` | font resource loader — 12-id table `00D10C98` |
| `00365882` / `003658C7` | `0032E400` / `0032E620` call sites inside it |
| `022CBE00 + 0x110` | the `.btm` buffer array (8 per slot) |
| `022CBE00 + 0x240` | font-ready bitmask |
| `00364210` | pow2 cell-dim rounding in the cache fill |
| `00364380` / `003649A0` | glyph measure/quad push *(`00364380` is the `.btm` requests' completion callback, not a glyph measure, RC-27)* |
| `003658F0` | `fontpack_fs.bin` loader (id `0xD2`) — companion |

## 5. Corpus survey — 12 files

|| |
|---|---|
| zero first dword | 12 of 12 — pixel data |
| sizes | a-family 42,240 · c/`stfc` 32,256 · b-family 29,184 |
| `in`/`ch` duplication | same 6 names in both dirs; `ch` copy hash-identical |
| nonzero density | ~26% of bytes nonzero (a_normal) — consistent with glyph ink |

## 6. Falsification pass — 2026-09-14

| attack | result |
|---|---|
| "Null first dword = format signature" | **Rejected — this was the standing trap.** The four zeros are the first glyph cells' padding; nonzero pixels begin at `0x15` in one file. |
| Is there a header table? | None found in body reads — nonzero data is continuous pixel-like content, not a record array. |
| Is `.btm` dead baggage? | **No** — `00365810` binds each buffer to a font slot with a ready bit; the glyph renderer reads it via `pixelOffset`. |
| Could the glyph table live inside `.btm`? | **No** — the table pointer (`+0x10` band) and the pixel base (`+0x110` band) are separate slots filled by separate resources. |

## 7. What this document does not claim

- **Bit depth** (8bpp vs 4bpp nibbles) — the cache-fill copies cells but the per-texel packing is
  not decoded.
- **Which resource file owns the glyph table** for `font_stf` — candidates are the
  `fontheader_*`/`fontpack_*` `.bin`s; the binding is not traced to a specific file.
- **Glyph count / coverage** — no census against the `f1` family's 1,237 kerning pairs.
- **Why `font_stf_c` ships only `_shadow`** — the `c`/`stfc` naming asymmetry is unexplained.
  *Answered as far as the data goes (2026-09-30, SWE2-CONTRACT): it does not ship only `_shadow`.* The authored
  `fontlist.ah` files list six `font_stf` members, `font_stf_{a,as,b,bs,c,cs}` (ids 17–22,
  [font data](../../16-UI/Text-And-Number-Rendering/font-data-kerning-and-expansion.md)), so the `c` family has both a
  face and a shadow; the face ships under the spelling `font_stfc_normal`. Matching `font_stfc_normal` to the `c`
  member is a name inference (tier 3); the spelling itself is authoring.

*The glyph record's unknown `u8` (§2): no reader.* UQ-364 (ANSWERED 2026-09-24) reads the record's `+0x04` as the
advance width from the shipped `fontpack_fs.bin` bytes and finds `+0x05`–`+0x07` read by no function on the glyph
path ([the glyph-run page](../../99-Unresolved-Residual/Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md),
UQ-364). The same answer shows the `022CBE00 + 0x10 + fontId*8` tables are fixed (`00366080`) into a kind-7 blob. Tier 1.

- [x] **RC-26.** The `.btm` texel packing: 8 bits per texel or 4-bit nibbles, as the cache fill `00364210`
  copies a cell. Registered 2026-09-30 (SWE2-CONTRACT); static.
  *Applied 2026-09-30 (records) RC-26:* **ANSWERED 2026-09-30 (static; SWE2-DATA's record `_index/candidates/rc22-34-resource-readers-0930/` §5, commit `1261e2044`, `btm_font_census.py`): 4 bits per texel, low nibble first**, cells at power-of-two pitch.
- [x] **RC-27.** Which resource file supplies the glyph table for the `font_stf` faces: the ids 130–135 half of
  `00365810`'s 12-id table `00D10C98` against the kind-7 path array. Registered 2026-09-30 (SWE2-CONTRACT); static.
  *Applied 2026-09-30 (records) RC-27:* **ANSWERED 2026-09-30 (the same record §5): the glyph tables come from `fontpack_fs.bin` (kind 7 id `0xD2`); ids 130–135 are never requested.** *(This corrects §3's reading of ids 130–135 as the glyph-table half and §4's `00364380` "glyph measure" label — see the note under §7.)*
- [x] **RC-28.** How many glyphs each `font_stf` face carries against the `f1` family's 1,237 kerning pairs.
  Registered 2026-09-30 (SWE2-CONTRACT); authored data.
  *Applied 2026-09-30 (records) RC-28:* **ANSWERED 2026-09-30 (the same record §5), counts:** 78 glyphs per face in the `in`/`ch`/`cn`/`kr` packs; in `us`/`it`, 78, 78 and four faces of 127 (the 78 plus 49 accented Latin). All twelve `stf` `.ker` files carry the same 1,237 pairs; both code points are glyphs of a 78-glyph face for 398 pairs and of a 127-glyph face for 663.
  *Round 2 (records) RC-28:* **Leftovers answered 2026-09-30 (SWE2-DATA's round-2 record `_index/candidates/rc-residue-0930/`, commit `39d08c02f` §3):** (1) the language index → path arm table (`rc28_lang_arms.py`): the `us`-family languages 1–6 load `fontpack_fs.bin` from `us` but the `.btm` from `in`; KR, CH and CN load their own. (2) The KR / CN `.btm` are absent: their file-size tables hold −1 for all six ids, and the read issuer `002DF780` refuses the request before it resolves a path, so no file is opened and no fallback is tried; the completion side is registered as RC-37.
  *Round 3 (records) RC-28:* **the completion side answered 2026-09-30 (SWE2-DATA, `_index/candidates/rc28-callback-0930/`, `rc28c_callback.py` FAILS 0, reviewed ACCEPT by SWE2-AUDIT-SEM `f29e44c6e`; incorporated by SWE2-CONTRACT, `_index/candidates/swe2contract-rc-round3-0930/`):** a refused KR / CN `.btm` request still completes. `0046E030` returns 1 whatever `002DF780` did, and the pump completes the slot from the stale status word `0215EFF4`. A stale value ≥ 0 runs `0032E330`, a value < 0 runs `0032E370`, and both call `00364380`: the second because the request's byte count is −1. `00364380` sets the ready bit regardless, so the staff roll does not wait. It draws from the 0-byte sheet allocation (`0036BC60` clamps −1 to 0), which no read fills. See RC-37. (3) The 49 accented glyphs only the `us` faces carry occur only in the `fr`/`de`/`it`/`es` staff-roll rows 894–944, and no `fsroll_nameA/B/C` call in the shipped staff roll requests those rows (`rc28_staffroll.py`, `rc28_staffroll_faces.py`), so the shipped staff roll never draws one.
- [x] **RC-37.** Whether the KR / CN staff roll waits for, or draws without, the `.btm` sheet whose read is
  refused (the queue `0032E620` → `0032E870` and the callback `00364380`). *(Registered 2026-09-30, SWE2-CONTRACT;
  static.)*
  *Round 3 (records) RC-37:* **ANSWERED 2026-09-30 (static; SWE2-CONTRACT, `_index/candidates/swe2contract-rc-round3-0930/`, on two independent records that agree: OPUS's `_index/candidates/rc37-refused-read-0930/`, `b2320ed29`, and SWE2-DATA's `_index/candidates/rc28-callback-0930/`, `79e70e154`):** the staff roll does not wait. The kind-7 issue wrapper `0046E030` returns 1 whatever the refusing issuer `002DF780` returned, so the pump takes the request as issued; state 3 finds the status slot `0215EFF4` as the previous read left it (not −1) and completes through `0032E330` (success) or `0032E370` (which calls the callback because the byte count is −1). `00364380` sets bit `slot` of `[[022CBE00] + 0x240]` and never reads its success flag, so `003657E0` reports the face ready. The roll then draws from a sheet no read filled. The two records name different layers of one allocation chain, and they agree: `00365810` → `00249810` / `002497E0` → `0036A190` / `0036A100` → `0036BC60`, which clamps the −1 size to 0 before rounding to 64, and the 0 reaches its first-fit tests `cmp [block + 0x18], r14d` (`0036BD03`, `0036BD31`) (`_index/candidates/swe2contract-rc-round3-0930/` A1–A4). **Limit (static, kept in the row, not a new row):** what `0036BC60` (or its retry `0036BFE0`) returns for that 0-byte request, and so whether the glyph reads fault or read unrelated heap bytes; whether a KR / CN build reaches the staff roll at all is not claimed.

*Superseded readings, 2026-09-30 (SWE2-CONTRACT, from SWE2-DATA's record `_index/candidates/rc22-34-resource-readers-0930/` §5, commit `1261e2044`): §3's "glyph table slot … ids 130–135" and §4's `00364380` "glyph measure" are corrected by RC-27 — the glyph tables come from `fontpack_fs.bin`, ids 130–135 are never requested; `00364380` is the `.btm` requests' completion callback (it sets bit `slot` of `[022CBE00 + 0x240]`), not a glyph measure. §2's "bit depth … not decoded" is RC-26 (4 bpp). The tables are kept as written.*

## 8. Related

- [`how-a-line-of-text-becomes-glyph-quads.md`](../../99-Unresolved-Residual/Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md) — the glyph-table record and consumer chain this sheet's contract rests on.
- [`font-data-kerning-and-expansion.md`](../../16-UI/Text-And-Number-Rendering/font-data-kerning-and-expansion.md) — the `f1` font family.
- [`README.md`](README.md) — the `ps2data/image` long tail.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-FRONTIER for SWE2-DATA, 2026-09-30)

*Added 2026-09-30 (SWE2-FRONTIER, executing SWE2-DATA's pass-22 debt). These are the layers pass 22 still reported for this page at HEAD `4dfe4a006`. Every edge was listed in full, and each cited helper was read at its instructions or is named as the page reads it.*

**ActorEntity, WorldAreaField, World, Presentation, Input, Save_Load_Settings, Script_VM_Native_Bridge — CLIENT (request path).** These layers use the generic pool entry points this page names: the per-kind size lookup `0032E400` (`[022C51F0][kind][id]`, `id < 0x400`) and the request queue `0032E620`. The actor loaders `ActorResource_BeginManagerResourceSetLoad` (`0032FCA0`, reached from `0032FC30`), `ActorResource_BeginPrimaryPayloadLoad` (`00330310`) and `003306E0` call them, along with their own calls (`002628B0`, `0032ED80`, `00263FF0`, `003304A0`, and `003306E0`'s calls to `002561C0`, `002566E0` and `0037DC30`). The field loaders `MapRef_BeginLoadResources` (`00268750`), `003319D0`, `00378030`, `00379A10` and `AreaArd_LoadOrUnloadFieldResource` (`003EA820`) call them, as do `00378540` and the render bodies `003B2310` / `003B53C0` (reached from `003B25D0` and `CharacterRenderSystem_Initialize` `004269A0`). So do `00291C80`, the save-slot loader `002EF300` and the script adapters `0050DF70` / `0050DFE0`, which pop their arguments through `00267E10` and write the result through `0026B4E0`. These are fellow API consumers for unrelated resources, not readers of this format.

**Presentation, World, WorldAreaField, Script_VM_Native_Bridge, UI, Save_Load_Settings — CLIENT and SERVICE (allocation and glyph path).** The allocation chain the page reads is shared. `00249810` / `002497E0` select the pool, allocate through `0036A190` / `0036A100` and restore the pool. `0036A100` takes the pool index from a global and falls back from its first allocation to a second one. About forty render bodies (`003A7460` to `0046F380`, `002561C0`, `003325D0` and peers), `00378540`, the field bodies `00268750`, `00267930`, `003319D0`, `00377DC0`, `00378030`, `00378BC0` and `003EA820`, the actor loaders `00330310` / `003306E0` and the script verb `0050D8F0` allocate through `0036A100` / `0036A190`. `002497E0` is called by `0055B560`, `0057CF20` and `00582860`, and `00249810` by `00247AE0` and `00291C80`. The glyph readers `00364210` / `003649A0` are the page's consumers: `003649A0` calls `00364210` and `003A1DB0` / `003A2020` / `003A2090`, and it is called by `0053E0B0`. `002EF300` is reached from `0050D9A0` and reads `002EF640`. These are shared allocation and draw paths; the `.btm` layout stays this page's.
