---
system: The @FDM and @FOR entries of .cm files - the keyed draw-part table and the LOD/variant config
category: 17-Presentation-Rendering
status: DOCUMENTED — the @FOR tail lists and the @FDM descriptor +0x08 read 2026-09-30 (SWE2-DATA, UQ-218 pass 18)
owner_layer: PrimaryOwner:Presentation
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the entry binder 00504F00, the LOD selector 004201F0, the @FOR keyed-float reader
    00504840, the @FDM key lookup 005048A0 and the spawn bridge 00521050 disassembled from the
    authority image and read whole; the authored layouts they imply then re-parsed out of all
    1,066 .cm files in the archive with every structural check passing
    (members/for_fdm_entry_census.py), 2026-09-26
last_reviewed: 2026-09-30
archive_formats:
  - "cm"
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-fdm-for-falsification-pass-1
  note: written by SWE2-DATA as the UQ-218 @FDM/@FOR slice, following the @FTR slice
    (ftr-node-table.md). Header fields, the 0xE0 record stride, the centimeter LOD thresholds
    and the key table are code-proven and census-verified; the @FOR table-A/B roles
    ({texture slot, palette slot} pair selection) and the @FDM descriptor-pool layout
    are read in the 0053B2xx draw builder (2026-09-29 pass 16). The @FOR record's tail
    lists and the @FDM descriptor +0x08 pair are read by the same builder (2026-09-30 pass 18). The w2/w4/w6 records that feed the
    composite-key bridge are presentation command 0x14 (FABLE 2026-09-26 correction; the group part of the key
    starts at bit 16, so the old 0xBCD3 = group 2 example was wrong).
---

# `@FDM` and `@FOR` — the keyed draw-part table and the LOD/variant config (SWE2-DATA)

**Package:** `SWE2-DATA-UQ218-FDM-FOR` (UQ-218 residue). **Population:** every `.cm`
in the archive — `1,066` files; `@FOR` present `1,066/1,066`, `@FDM`
`1,045/1,066` (the 21 missing are ~~mostly `treasure`/`bg_obj` files~~ all weapons *(corrected 2026-10-02, OPUS: the tag set of every `.cm` in the extracted archive; FCP's 21 `@FCP @FTR @FOR` weapons)*). Census:
`members/for_fdm_entry_census.py`. Native proof: `004201F0`, `00504840`,
`005048A0`, `00521050`, `00504F00` disassembled in full.

## How the entries reach the render record (SWE2-DATA)

`00504F00` (the render-record entry binder) resolves all seven `.cm` entries
by tag through `00409A30` and stores their offsets in the record:

| record offset | tag | entry |
|---|---|---|
| `+0x208` | `@FOR` | LOD/variant config |
| `+0x20C` | `@FDM` | keyed draw-part table |
| `+0x210` | `@FTR` | node table (see `ftr-node-table.md`) |
| `+0x214` | `@FEF` | effect carrier ([decoded](fef-and-motion-entries.md)) |
| `+0x218` | `@FTE` | texture table |
| `+0x21C` | `@FCT` | colour table |
| `+0x220` | `@FCP` | character parameter block |

Consumers resolve the entry pointer as `dword[record+0x1F8] (blob base) +
dword[record+0x208+4k] (stored offset)` — seen at `00420240`–`00420274` for
`@FOR` and `005048E5`–`005048F8` for `@FDM`, both checking for the `-1`
"no entry" sentinel first. `00504E70` binds `@FRP`/`@FEF` into the
`+0x1F0`/`+0x228` sub-records. The mirror unbind lives at `00504CBF`
(`00409CA0` under `test byte[obj+8],4`).

## `@FOR` authored layout (SWE2-DATA)

```
+0x00  '@FOR', u32 kind = 0, u32 entryLen, u32 0
+0x10  char[0x20] name        (== file basename: "m1283", …)
+0x30  u8    recordCount      (1..8 typical)
+0x31  u8[3]                  (1,1,1 in all sampled files)
+0x34  u16   tableA_off       = 0x40 in all 1,066 files
+0x36  u16   tableB_off       = 0x40 + 3·k, k = table-A record count
+0x38  u16   recordBase       (0x40..0x108; records start here)
+0x3A  u8    lodThresholdCount  (0:751, 1:179, 2:136)
+0x3B  u8    lodCap             (max selectable index)
+0x3C  u16   lodDistance[0]     — authored in centimeters
+0x3E  u16   lodDistance[1]     (×0.01f = meters, constant 008F30E4)
+0x40  table A — small records (3 B stride suggested by the B offset arithmetic; content unresolved)   <- corrected 2026-10-02, OPUS - resolved 2026-09-29, Table A/B section below
…      table B — bytes between u16@0x36 and u16@0x38 (unresolved)   <- corrected 2026-10-02, OPUS - resolved 2026-09-29, Table A/B section below
+rb    records[recordCount], stride 0xE0 — proven by 00504840
…      tail — u16 index lists addressed by the record fields
```

### `@FOR` record (`0xE0` bytes)

| off | field | evidence |
|---|---|---|
| `+0x00` | u8 key — `i+1` in `1,062/1,066` files (4 exceptions carry reordered keys) | `00504870` `cmp eax, r10d` |
| `+0x01` | u8 ~~= 0~~ packing kind of the fourth list *(corrected 2026-10-02, OPUS: `0053AB50`+0x16DF `movzx eax, byte ptr [rbx + 1]` on the flag-1 pass)* | sampled |
| `+0x02` | ~~u8[6] enable flags = 1~~ **u8[3] per-part packing kind** of the tail list (0 = empty, 1 / 2 / 3 = 2- / 3- / 4-byte elements; `0053C227`), then **u8[3] per-part selector counts** at `+0x05` (`0053B426`) *(corrected 2026-09-30, pass 18)* | sampled; `0053AB50` |
| `+0x08`/`+0x0A`/`+0x0C` | u16 offsets, from the record base, of the three **per-part draw lists** (`0053C16B`) — ~~u16 index lists~~ packed elements, see below | every list fits its entry under its kind's width, 1,891 lists |
| `+0x0E` | u16 offset of the fourth list, read on the builder's flag-1 pass (`0053C173`) | non-zero only in the 132 high-model records |
| `+0x10`/`+0x12`/`+0x14` | u16 element counts of the three lists (`0053C187`) | same |
| `+0x16` | u16 count of the fourth list (`0053C18F`); its packing kind is `byte[+0x01]` (`0053C22F`) | same |
| `+0x18` | f32 key value (usually `1.0`) | `00504895` `movss [rcx+r11+0x18]` |
| `+0x20`+ | 0xA0-byte parameter block, `0xFF` defaults with a `0x00` at `+0x48`/`+0x68` | sampled; consumers ~~unresolved~~ partly read *(answered: see the 2026-09-29 table A/B section - five `0x20`-stride part sub-records, read by the builder; 2026-10-02, OPUS)* |

### `@FOR` consumer 1 — distance LOD select (`004201F0`, `CharacterRenderRecord_SelectLODForViewDepth`)

1. Resolves the `@FOR` entry (index ~~`rec+0x208` + base `rec+0x1F8`~~ `+0x208` + base `+0x1F8` of the model resource `004780B0(word[record+0x64])`, not of the render record *(corrected 2026-10-02, OPUS: `004201F0`+0x42 `call 004780B0`, +0x50 `mov ecx, dword ptr [rax + 0x208]`, +0x6C; the view depth `f32[+0x208]` of step 4 is read from the record or the second argument at +0x192)*), checks
   the `'@FOR'` magic at `00420274`.
2. Builds the threshold vector `{0, f(u16@3C), f(u16@3E), 1.0e8}` on the
   stack — `u16 × 0.01f`, i.e. authored centimeters → meters (m1283: `600,
   1300` → 6 m / 13 m; m1282: `1000, 2500` → 10 m / 25 m). The sentinel
   `1.0e8f` (`00D10824`, bytes `20 BC BE 4C` — corrected 2026-09-28 from
   `9.99e7`, FABLE control) is the "no farther edge" cap.
3. The comparison table is the stack vector, **or the render record's
   `+0xA0` float array when `byte[record+0xC0] & 1`** — this resolves the
   render-record page's "seven-float ladder `100,200,…700` at `+0xA4`..`+0xBC`
   behind `+0xA0`, no direct reader": it is the cached threshold array, used
   by this exact site when the flag directs it.
4. Loop (`004203C0`–`004203D9`): `lod = count of thresholds the view depth
   meets or exceeds`, i.e. skip while `depth < t[i]` … window check
   `t[i] ≤ depth < t[i+1]`; result clamped by `u8[entry+0x3B]`.
   `depth = f32[object+0x208]` (the camera-space view distance).
5. `lodFrac = (thresholdCount+1 − lod) / (thresholdCount+1)` →
   `f32[object+0x2A4]` (1.0 = nearest); `word[object+0x90]` → `+0x64`;
   `003E57D0` result gets bit `0x2000` set/cleared by `object+0x284 & 0x100`;
   then `00421280(object, 1)` applies.
   With `u8@0x3A = 0` (751 files) the branch is skipped entirely: `lodFrac =
   1.0` — no distance switching.

### `@FOR` consumer 2 — keyed float (`00504840`)

`00504840(entry, key)`: walks `recordCount` records at `entry + u16@0x38`,
stride `0xE0`, matches `u8[rec+0]` against the key byte and returns
`f32[rec+0x18]` (default `f32[01CEBBA8]`). Called once — from the
model-resource constructor `00420480` at `0042061B` with
`u8[modelRec+0x5C]` (a selector byte) — result stored to
`modelRec+0x26C`. This is the authored per-variant scalar the record table
carries (the variant keys `1..n`).

**Table A/B resolved 2026-09-29 (SWE2-DATA, `0053B2xx` draw builder):**
`word[+0x34]`/`word[+0x36]`/`word[+0x38]` are resolved to entry pointers at
`0053B33A`–`0053B35A`. The `0xE0` record is selected by
`byte[rec+0] == s8[object+0xB8]` (the variant key — same axis
`00504840`/`00504740` read). Per part, the builder iterates a selector-byte
array in the record's part sub-record (`byte[subRec + i]`,
`i < byte[rec + 5 + part]` on the `dword[ctx+0x86F8]==0` arm; the `!=0` arm
uses `rec+0x80` with count `byte[rec+0x1C]` — `0053B41D`–`0053B43E`). Each
selector byte resolves through **table A**, a u8 triplet table:

```
bIdx = byte[tableA + 3·sel + part] + byte[@FOR+0x32]·variant
pair = tableB[2·bIdx .. 2·bIdx+1]
```

(`0053B4B6`–`0053B4E7` — note the `byte[+0x32]`·variant term lands on the
**table-B** index, not the table-A index.) **Table B** is a **u8 pair
table**: every selected `{byte0, byte1}` pair is deduped into two scratch
lists (`ctx+0x83B0`/`ctx+0x83D0`, pre-seeded from another entry's
`u8 n @+0x30` / `u8[n] @+0x31` list — `0053B45A`–`0053B48A`). Byte 0 drives
the `@FTE` side (`dword[@FTE + (slot+2)·0x20]` summed = texture byte total,
`0053B5B0`–`0053B5F6`, then per-slot `word[ctx68 + slot·2 + 0x100]` +
`@FTE + (slot+2)·0x20` → `005212E0`), byte 1 the `@FCT` palette side
(~~`word[@FCT + (pal+3)·8]`~~ `word[@FCT + (pal+3)·0x10]` *(corrected 2026-10-02, OPUS: `0053AB50`+0xADC `add rax, rax` then +0xADF `movzx eax, word ptr [rdi + rax*8]`)* summed, `0053B620`–`0053B64D`). The summed byte
total feeds `00537AF0`. So table B's pairs are
**`{texture slot, palette slot}` per (part, selector, variant)**.
The record's `0xA0` parameter block at `+0x20` is **five `0x20`-stride part
sub-records** (`rec + (i+1)·0x20`).

Two more `@FOR` record consumers found while tracing: `00504740` is the
`00504840` twin reading `f32[rec+0x18]` for `s8[obj+0xB8]` (no key arg),
and the `00504F00` `.cm` binder itself walks the table for a requested key
(`00505071`–`005050A0`): it stamps `s8[obj+0xB8]` with the matched record
key (fallback record 0's key, then 0), stamps `u8[obj+0xB9]` = an argument
clamped by `byte[@FOR+0x33]`, and `u8[obj+0xB3]` = `byte[@FOR+0x3A] + 1`
(the LOD level count).

~~The three u16 index lists per record (`+0x08..+0x14`) remain the unresolved
piece — every `0xE0`-stride walker in the image (`00504740`, `00504840`,
`00504F00`, `0053B2xx`) has been enumerated and none reads them; they are
either read through a different base or dead metadata.~~ *(Corrected 2026-09-30, pass 18: the builder reads them.)*

**The tail lists are the per-part draw lists (2026-09-30, SWE2-DATA, UQ-218 pass 18,
[record](../../_index/candidates/uq218-pass18-0930/README.md), `for_tail_census.py` FAILS 0).** For each part the builder reads
`list = recordBase + word[rec + 8 + 2·part]`, `count = word[rec + 0x10 + 2·part]` (`0053C16B`, `0053C187`) and
decodes each element by the part's packing kind `byte[rec + 2 + part]` (`0053C227`–`0053C2E4`):

| kind | element | fields |
|---|---|---|
| 3 | 4 bytes | `d`, `s`, `a`, `b` |
| 2 | 3 bytes | `d`, `s`, `a` = low nibble, `b` = high nibble |
| 1 | 2 bytes | `d` = low 5 bits, `s` = high 3 bits; `a` / `b` = nibbles of the second byte |

`d` selects the part's `@FDM` descriptor (`0053C308`), `s` the descriptor's sub-record (`0053C320`), and `a` / `b`
travel with the sub-record to `0053D140`, which uses `byte[sub+2]` of them as indexes into the builder's per-draw
table of packed texture-register qwords (`rbp+0x2B0`, built from each texture the table-A/B selection resolved,
`0053BF85`–`0053BFEC`; read at `0053D3E0`–`0053D3E8`). A second call with argument 6 = 1 reads a fourth list (`+0x0E` / `+0x16`,
packing `byte[+0x01]`); `0053D780` makes it only for a class-`'h'` object (`byte[obj+0xC] == 0x68`, `0053D8C9`). The
builder takes the records from its `rcx` argument and the `@FDM` from its `rdx` argument (`0053B29D`–`0053B30E`),
so a high model's first pass indexes its partner's `@FDM`. Corpus, 1,045 `.cm`: kinds 0 / 1 / 2 / 3 on 1,871 / 1,565 /
311 / 15 part slots, kind 0 exactly the empty lists; the 1,759 normal-model lists resolve in their own `@FDM`; the
132 high-model first-pass lists resolve in the base model `<name>.cm`'s `@FDM` (59 of them would not in their
own); the 132 fourth lists are all high models' and resolve in their own `@FDM` part 0 — 18,049 elements. Which file
the partner index names is inferred from that fit, not traced.

## `@FDM` authored layout (SWE2-DATA)

```
+0x00  '@FDM', u32 kind = 0, u32 entryLen, u32 0
+0x10  char[0x20] name
+0x30  u16   variantCount      (1:730, 2:179, 3:136 — same distribution shape as @FOR)
+0x32  u16   keyTable_off      = 0x50 in all 1,045 files
+0x34  u32   listA_off         \  each = offset of a {u32 n, u16[n]}
+0x38  u32   listB_off          > block, or 0xFFFFFFFF when absent
+0x3C  u32   listC_off         /  (parse-verified 1,045/1,045)
+0x40  u8[16]  0xFF
+0x50  keyTable: {u32 count, u32 keys[count]}   — consumed by 005048A0
…      listA/B/C: u16 offset lists into the record pool
…      record pool: 0x10-stride descriptors — see below
        followed by the sub-record regions the lists index into
```

**Descriptor pool decoded 2026-09-29 (SWE2-DATA, `0053B2xx` builder).**
`dword[@FDM+0x34+4·sel]` picks one of the three lists (`sel` = the part's
list selector), and each u16 element is an **entry-relative offset** to a
`0x10` descriptor (`0053C305`–`0053C31D`). A kind byte ~~in the pool head
(`byte[rec+1]`/flag-driven, values 1/2/3)~~ *(corrected 2026-09-30, pass 18: it is the `@FOR` record's per-part
packing kind `byte[rec+2+part]`, `byte[rec+1]` on the flag-1 pass — above)* selects among three packed
decoders that unpack the part's element indices — case 3 carries four
bytes, case 2 a `{lo4,hi4}` nibble pair plus two bytes, case 1 a
`{lo5,hi3}`/`{lo4,hi4}` split (`0053C222`–`0053C2E4`). The descriptor
fields consumed:

| off | field | evidence |
|---|---|---|
| `+0x00` | u16 kind/tag = 1 | layout |
| `+0x02`/`+0x03` | s8 default pair A/B — the fallback values when the override slot reads `0x7FFF` or res flag `0x1000` is clear (`0053C386`/`0053C3C0`–`0053C3CF`) | `0053B2xx` |
| `+0x04` | u32 slot ordinals: `A = (bits>>8)&0x3FF`, `B = (bits>>18)&0x3FF`, `0x3FF` = absent — fed to `00371330` (the `@FTR` tailU16 slot reader) at `0053C36F`/`0053C3AD` | `0053C354`–`0053C3AD` |
| `+0x08` | ~~u32 — not consumed in the pass; field meaning open~~ **s8 pair** `+0x08` / `+0x09`, written into the VU1 packet by `0053D4B0` (`0053D585`, `0053D592`) beside `+0x04` bits 0, 1–7, 28, 29; `+0x0A` / `+0x0B` unread there. **Zero in all 12,044 shipped descriptors** — read and constant *(corrected 2026-09-30, pass 18)* | `0053C403` → `0053D4B0` |
| `+0x0C` | u16 offset region — `word[desc+0xC + 2·idx]` resolves (entry-relative, `+fdmBase`) to a **sub-record**; `word[sub+4]` then offsets to the part's u16 **bone-index stream** (`0053C31A`–`0053C331`, `0053C5D0`–`0053C627`) whose elements are scaled `×0x290` — the `@FTR` record stride — and packed into VU1 `V4_32` `UNPACK` rows (`0x6C040000`) at `0053CB50`–`0053CBA2` | `0053B2xx` |

The descriptor-targeted **sub-record** (reached via `+0x0C`) reads
`u32 sub+0` resolved `+fdmBase` into the VU1 row's high dword and
`dword sub+8` into the low (`0053CC02`–`0053CC18`, `|0x30000000` tag) —
so the sub-record is `{u32 link/ptr, u16 boneListOff @+4, u32 @+8}` —
the `{u32 n, u16[n]}` lists, 0x10 descriptors and sub-records together
form a small directed pool: list → descriptor → sub-record → bone
stream.

So a `@FDM` descriptor is a **per-part draw-parameter record**: an authored
s8 pair (overridable at runtime by the command-`0x14` slot write path —
below) plus a bone-index stream into the `@FTR` 0x290 table.

Keys are dense small ints; `774/1,045` tables are strictly sequential
(`k[i+1]−k[i] == 1`), the rest have gaps. For `m1283`: `23` keys `0xBCD3..
0xBCE9`. ~~`0xBCD3` decodes as `(2 << 14) | 0x3CD3` under the composite-key
construction below — i.e. group 2, item `0x3CD3`.~~

> **Corrected (FABLE, Claude Opus 5.5, 2026-09-26).** The construction below puts the group part at **bit 16 and up**, not bit 14.
> - `(w4 & 0xFFFC) << 14` is `(w4 >> 2) << 16`, so the key is `((w4 >> 2) << 16) | w2`. The low sixteen bits are
>   `w2` and the bits above them are `w4`'s upper fourteen.
> - Group 2 with item `0x3CD3` means `w4 >> 2 = 2`, which gives **`0x23CD3`**.
> - `(2 << 14) | 0x3CD3` does equal `0xBCD3`, but that is a different construction (a shift of 12 on
>   `w4 & 0xFFFC`). No `w4` value turns item `0x3CD3` into `0xBCD3`.
> - So `0xBCD3` is a key **with no group part**: `w4 >> 2 = 0`, and the whole key is `w2 = 0xBCD3`.
> - **The same holds for every shipped key.** All 30,023 keys in the 1,045 key tables are below `0x10000`.
>
> The formula and the census above stand. Control: [`fdm_composite_key.py`](../../_index/candidates/fdm-composite-key/fdm_composite_key.py) (FAILS 0), which has three parts:
> - a static decode of `005210A6`–`005210BB`;
> - an **executed original-code window**: those bytes run under Unicorn for all 65,536 `w4` values, with a mutant
>   (`shl 0x0C`) that the checks catch. The mutant produces exactly the old `0xBCD3` reading;
> - the archive key census.
>
> The window proves the arithmetic only. It is **not** a rendering test, and it says nothing on its own about
> which records the game reaches.

### `@FDM` consumers — key → ordinal → spawn record

- `005048A0(object, u32 key)`: resolves `@FDM` via `rec+0x20C`, reads
  `u16[entry+0x32]` → `{u32 count, u32 keys[]}` at `entry + off`, linear-searches
  the key, returns the ordinal or `-1`.
- `00521050` is the bridging consumer: ~~it walks 8-byte authored records
  `{u16 w2, u16 flags w4, u16 w6}` and for each~~ *(corrected (FABLE, Claude Opus 5.5, 2026-09-26): it takes **one** 8-byte record per
  call and does not walk. The record is an authored presentation **command `0x14`**, whose words `+2`/`+4`/`+6`
  are `w2`/`w4`/`w6`. The handler `00520E70` takes the entity index from `word[+0]` of its *first* argument, the
  record the command runs for, not from the command. `00426870` then applies this body to that entity and to each
  node of its sub-tree; see the [command-handler page](../Authored-Commands/the-authored-presentation-command-handlers.md))*: `w4 & 1` must equal
  `u16[object+0x2F2]` ~~(a variant/state word — the same axis `@FOR` keys
  select on)~~ *(corrected: that is the **substitute-record flag** — 0 normally, 1 when the record was built with
  no key — per the [command-handler page](../Authored-Commands/the-authored-presentation-command-handlers.md)'s `word[record + 0x2F2]` section. Nothing ties it to the `@FOR` key: `00504840`
  takes that key from `u8[modelRec+0x5C]`, above)*; if `w4 & 2`, the lookup key is the **composite
  `(w4 & 0xFFFC) << 14 | w2`** resolved through `005048A0`, else `w2` is a
  direct s16 ordinal; the ordinal plus `w6` then feed
  `00373060(resolvedObject, ordinal, w6)`, which writes `w6` into the
  `@FTR` core's **u16 override-slot array** — `core + count*0x292 + 2*ordinal`,
  i.e. the `tailU16` region after the `0x290` bone records (see
  `ftr-node-table.md`). **Sink resolved 2026-09-28 (FABLE evidence record
  `_index/candidates/uq218-cm-entry-residues/`, controls FAILS 0):**
  `00373060` bounds the ordinal by ~~`@FTR u32 +0x38`~~ `@FTR u16 +0x38` *(corrected 2026-10-02, OPUS: `00373060`+0x5A `movzx ecx, word ptr [rax + 0x38]`)* (`003730BA`) — the data
  join holds: **@FDM key count == @FTR `+0x38` in 1,045/1,045 files** (and
  `+0x38` is 0 in all 21 files without `@FDM`; mutant against the node count
  fails 148/1,045). `0x7FFF` is stored without a flag; any other value also
  sets `res dword[+0] |= 0x1000` (`003730C2`..`003730D6`), and `00372820` /
  `00372510` initialise every slot to `0x7FFF` with `0x1000` cleared. The
  slot reader is `00371330` (called only at `0053C36F`/`0053C3AD`): per
  `@FDM` part record it takes `slotA = (dword[+4] >> 8) & 0x3FF` and `slotB =
  (dword[+4] >> 18) & 0x3FF` (`0x3FF` = absent; slotB absent exactly when
  bit0 = 0), and **only while res flag `0x1000` is set** replaces the part's
  authored `s8 +2/+3` defaults, then hands the pair to `0053D4B0`, which
  uploads it to VU1 through a VIF `UNPACK V4-32` row `{bit0, A|B != 0, B, A}`
  (`0053D50F`..`0053D57A`). So an event's `0x14` command sets a per-model,
  key-addressed pair of integers on chosen draw parts — what the VU1 program
  does with the pair is not established (no microcode read).

**What the shipped data reaches** (FABLE, Claude Opus 5.5, 2026-09-26). This is a static census, not an execution result.
- Over the 7,193 authored `0x14` commands (event blocks only), `w4` is **3 on 6,164 and 2 on 1,029**; the census
  is on the [command-handler page](../Authored-Commands/the-authored-presentation-command-handlers.md).
- So the lookup bit is always set, and the direct signed-ordinal path is never authored.
- `w4 >> 2` is 0 in every command, so **the key sent to `005048A0` is exactly `w2`**.
- That matches the key tables, none of which holds a key at or above `0x10000`.
- A command whose `w2` is not in the entity's own key table gets `-1` back, and that node is skipped silently.
- **Not established here:** which of those commands run in play, and whether each `w2` is present in the table
  of the entity it reaches. That needs the event-block-to-entity join or a runtime trace.

So `@FDM` is the .cm's **keyed part table**: authored ~~names
`(group << 14) | part`~~ keys *(corrected (FABLE, Claude Opus 5.5, 2026-09-26): `((w4 >> 2) << 16) | w2`, see above)* → part ordinals; the u16 lists + 0x10-stride
descriptor pool carry the per-part draw data — both resolved 2026-09-29:
the pool is `list -> descriptor -> sub-record -> bone-index stream`
(table above). The `w2/w4/w6` record source **and** the
sink are answered (command `0x14` above; `00373060` → the `@FTR` tailU16
override slots → `00371330` → VU1 `0053D4B0`) — together with `@FTE`,
`@FCT`, `@FEF` (`1,044`, `1,044`, `144` files) and `@FMC`/`@FMN`/`@FMW`
(`209`, `111`, `111` ~~files~~ entries, in 45 files *(corrected 2026-10-02, OPUS: 29 weapons and 16 treasures carry them; recount of the `.cm` tag sets)*).

## Evidence

- `004201F0` — `@FOR` LOD select, fully disassembled (~~144~~ 143 insns *(corrected 2026-10-02, OPUS: 648 bytes to the `ret` at `004201F0`+0x287; the falsification pass's count note)*).
- `00504840` — `@FOR` keyed float reader, fully disassembled.
- `005048A0` — `@FDM` key→ordinal lookup, fully disassembled.
- `00521050` — spawn bridge: composite key `((w4 & 0xFFFC) << 14) | w2` = `((w4 >> 2) << 16) | w2`; one command
  `0x14` record per node. Control [`fdm_composite_key.py`](../../_index/candidates/fdm-composite-key/fdm_composite_key.py) (static decode, executed original-code window with a
  mutant, key census; FAILS 0).
- `00504F00` — seven-tag index binder into render record `+0x208..+0x220`.
- `00504CBF` — `@FDM` unbind (`00409CA0`).
- `00420480` — model-record constructor calling `00504840` at `0042061B`.
- Scale constants: `008F30E4 = 0.01f` (cm→m), `00D10824 = 1.0e8f` sentinel
  (corrected 2026-09-28: bytes `20 BC BE 4C`, not `9.99e7`).
- Census `members/for_fdm_entry_census.py`: all claims over `1,066` files,
  2026-09-26.

## Falsification pass 1 — 2026-09-29 (OPUS): every code claim tested survives

**Attack.** The page's claims about the code were turned into checks at their cited instructions. Script:
`Tools/analysis-kit/gfz-scripts/falsify_fdm_for.py`, output `falsify_fdm_for.out`, image `73461d08…`, 0 BROKEN, exit 0.

The claims tested:
- the binder and the unbind;
- both `@FOR` consumers, the key lookup and the bridge;
- the slot sink, its initialisers and its reader;
- the `0053B2xx` builder's cited windows and the VIF row.

Every "one caller" and "called only at" claim was re-counted with a raw E8/E9 sweep. Two things are carried, not re-run:
the 1,066-file archive census (`members/for_fdm_entry_census.py`) and FABLE's composite-key control. Still open, as the
page says: the `@FOR` record's three u16 tail lists and the `@FDM` descriptor `+0x08`. *(Both answered 2026-09-30,
SWE2-DATA pass 18 — the per-part draw lists section and the descriptor table above.)*

| # | Clause attacked | Result |
|---|---|---|
| M0 | sizes; the evidence list's "144 insns" for `004201F0` | **survives** for all eleven sizes. Count note: `004201F0` decodes to 143 instructions in its 648 bytes. This is an evidence-list count, not a mechanism claim, so no correction row |
| M1 | the binder `00504F00`; the unbind `00504CBF` | **survives**: the seven tags in order into `+0x208`..`+0x220`, `@FRP` into `+0x1F0` and `@FEF` into `+0x228`. The `@FDM` unbind sits behind bit 2 of byte `+8` |
| M2 | `@FOR` consumer 1, `004201F0` | **survives**: the magic at `00420274`; the vector {0, cm × 0.01, cm × 0.01, 1.0e8}; the `+0xA0` alternative on `+0xC0` bit 0; the window loop; the `+0x3B` clamp; `+0x2A4`, `+0x64`, the `0x2000` bit and `00421280(object, 1)` |
| M3 | `@FOR` consumer 2, `00504840` | **survives**: the `0xE0` walk and `f32 +0x18` with default 1.0. Its one caller is `0042061B`, with byte `+0x5C`, and the result goes to `+0x26C` |
| M4 | `005048A0` | **survives**: `+0x20C`, u16 `+0x32`, the linear key search and -1. Its one caller is `005210BB` |
| M5 | `00521050` | **survives**: the `+0x2F2` flag test; `(w4 & 0xFFFC) << 14 \| w2` on `w4 & 2`; otherwise `movsx w2`. It is `00373060`'s one caller |
| M6 | `00373060`, the initialisers, `00371330` | **survives**: the `+0x38` bound at `003730BA`; `0x7FFF` stored bare; anything else is flagged `0x1000`. Both initialisers store `0x7FFF` and clear `0x1000`. The reader is called only at `0053C36F` / `0053C3AD` |
| M7 | the `0053B2xx` builder | **survives**: the table A / B / record resolutions; the `@FTE` `(idx + 2) × 0x20` sum; list → descriptor → sub-record; the `0x1000` gate at `0053C34C`; the slot ordinals `>> 8` / `>> 18` and their s8 fallbacks; `× 0x290`, `0x6C040000` and `\| 0x30000000` |
| M8 | `0053D4B0`'s row | **survives**: {bit 0, A \| B != 0, B, A} |

No correction.

## Crossings into other layers — pass 22 (SWE2-DATA, 2026-09-30)

- **Resource — SERVICE, edges.tsv.** The builder's caller `0053D780` and the slot reader `00371330` (with `00372510`)
  reach the model's entries through the resource table (`004096C0`, `00409F50` and the `ResourceTable_Resolve*`
  helpers); this page claims the entry layouts they read, not the table's lookup.
- **CoreRuntimeScheduling — OUT-OF-SCOPE, edges.tsv.** The builder `0053AB50` calls `001EDE70`; no statement here rests
  on that callee, which is not read on this page.
