# RC-30 closed: the `loca_*.cl2` files are requested by `003C1F00` from `menumap_common.bin` and read by `003C26C0` as TIM2-shaped CLUTs (SWE2-DATA, 2026-09-30)

affected: _index/candidates/rc22-34-resource-readers-0930/README.md, _index/candidates/rc-residue-0930/README.md

**Question.** RC-30 asks which function reads a loaded `loca_*.cl2`: its header fields and palette, the component order,
and whether the variant selects a decode path. The second record ([`../rc-residue-0930/`](../rc-residue-0930/README.md))
bounded three index-computed request sites. It left one fact open: whether any data-driven `(kind, id)` source reaching
the path API can hold kind 7 with id `0xE2`–`0xE4`. This record runs that census.

**The census found the route the earlier records missed.**

| item | verdict |
|---|---|
| the data-driven `(kind, id)` structures (`003A13F0`, `003DDA70`, `003DF550`, `003E9EF0`, `003EADE0`, `003DC5B0` / `003DC8D0`) | **none can carry kind 7** — every kind field has a constant writer |
| the script-verb route (`debug_filesize` / `debug_fileread`) | **not used** by any shipped script |
| who requests the `.cl2` | **`003C1F00`**: kind 7, id `0xE1 + byte [menumap_common entry + 1]` |
| which files ship a request | `menumap_common` entry 40 → `Loca_gil.cl2` (`0xE2`), entry 46 → `Loca_bhm.cl2` (`0xE3`); `Loca_rbl.cl2` (`0xE4`) is never selected |
| who reads the loaded file | **`003C26C0`**, as a TIM2-shaped CLUT for a location-map image |

**RC-30: ANSWERED.** One fact is left, and it is static: the byte order the texture upload gives the palette entries (§4).

All scripts are in this directory. Each prints its checks with a positive control and ends `FAILS 0`.

run: rc30c_kind_slice.py, rc30c_data_fields.py and rc30c_cl2_reader.py at 63f4b8f89, plus the supporting
rc30c_ard_list.py, each FAILS 0 (the .out files beside them).

| script | what it establishes |
|---|---|
| [`rc30c_kind_slice.py`](rc30c_kind_slice.py) ([out](rc30c_kind_slice.out)) | the kind value set at all 124 path-API call sites, then the id set at the 11 kind-7 sites |
| [`rc30c_data_fields.py`](rc30c_data_fields.py) ([out](rc30c_data_fields.out)) | the four structure fields' writers, the script-verb census, the `003C1F00` request and the `menumap_common` census |
| [`rc30c_cl2_reader.py`](rc30c_cl2_reader.py) ([out](rc30c_cl2_reader.out)) | the reader `003C26C0` and the TIM2-shaped header, over all 20 shipped `.cl2` |
| [`rc30c_ard_list.py`](rc30c_ard_list.py) ([out](rc30c_ard_list.out)) | supporting: the `.ard` `+0x2C` list behind the `003DC5B0` / `003DC8D0` leaf — it remaps the **id**, never the kind (§2a) |

## 1. The kind of every path-API call (`rc30c_kind_slice.py`)

The script slices `ecx` backwards from each of the 124 rel32 call/jmp/jcc sites of `0032E400` / `0032E620` / `0032E3F0`.
- **What it follows:** constants, register moves, `lea` offsets and `cmov` (both sources); stack slots, including
  out-parameters written by a callee; argument registers into every raw caller (3 levels).
- **Idioms it knows:**
  - a counted loop's fall-through (the counter is 0);
  - the `_alloca_probe` and folded `return 0` (`005C5230`) stubs;
  - `r11`-relative frames.
- **Result:** kind 7 is reachable at 11 sites. Every other site resolves to a set without 7. Six leaves remain, all
  handled in §2:
  - `003A13F0` → `{0x20}`, through `002ED8C0`, which writes `[rdx] = 0x20` unconditionally;
  - `003DC5B0` / `003DC8D0` → `{0x1E}`, through `003DCA30`, which writes `[r9] = 0x1E` first;
  - `0032EB40` → `{5, 0x15}`, from `00330310`'s kind and `003EA820`'s `0x15 + 005C5230()`;
  - the `002ED6F0` out-parameter group (`002E6700`, `002E9920`, `002EAD50`, `002E6EB0`) → its per-arm constants.
- **The 11 kind-7 sites' ids.**
  - None of the constant ids is `0xE2`–`0xE4` (K1).
  - The pool core `00249210` inherits ids from its callers. The 46 constants among them exclude `0xE2`–`0xE4`.
  - Among the pool core's computed leaves is **`003C207A add r8d, 0xE1`**. The first record's census list carried
    `003C1F00`'s other site (`003C200D`, `0x142 + dil`) but not this one. §3 follows it.
- **Controls:**
  - C1: the font request `00365882` resolves to `{7}`;
  - C2: `003A13F0`'s out-parameter resolves to `{0x20}`;
  - C3: the MapRef site `00268814` resolves to `{9}`.

## 2. The data-driven leaves (`rc30c_data_fields.py` S1, S2)

Every field is written by one filler, and the census lists it (control C1 for each):

| structure (field) | read by | only filler | kind values |
|---|---|---|---|
| `02B581A0` 0x1C-byte slots (`+0x10`) | `003DDA70` | `003DD609`, from `0032F170` | `1`, `5`, `8` |
| `02B59360` 0x38-byte slots (`+0x2C`) | `003DF550` | `003DF4EA`, from `0032F170` | `1`, `5`, `8` |
| `02B5D0B0` 0x40-byte slots (`+0xC + 2n`) | `003E9EF0` | `003EA06B`, from `003E9FED`–`003E9FFF` | `8`, `0x25` |
| `02B5E0E0` (`+0x1C`) | `003EADE0` | `003EB10C` (`0x24`), plus the qword clear at `003EB088` | `0`, `0x24` |

**Scope of the filler census.** For each structure it covers every function that holds a raw rip reference into the
array, plus their direct callees. `0032F170` writes only the constants 1, 8 and 5 through its kind out-pointer.

The two script verbs pop their `(kind, id)` from the VM stack: `debug_filesize` (verb `2006`, `0050DF70`) and
`debug_fileread` (verb `2007`, `0050DFE0`). **No shipped script calls either.** The count is 0 across the 1,114-file
decompile; the control verb `setposparty` is found 788 times.

### 2a. The `003DC5B0` / `003DC8D0` leaf's authored list (`rc30c_ard_list.py`) (SWE2-DATA)

The slicer bounds this pair to `{0x1E}`: `003DCA30` writes its first out-parameter `0x1E` (`003DCA49`) before it
consults a list, and `003DC5B0` / `003DC8D0` pass that word as the kind to `0032E620` / `0032E400`. The list
therefore cannot change the kind. What it *can* change is the id — its matched entry's `word +8` replaces the
request id (miss → −1). This supporting census pins that authored table:

- `02B57F70` is a 16-slot request registry keyed `(002E96B0(obj), arg id, arg sub)`, filled by `003DCD00` →
  `003DC380` (writes at `003DC3CF`/`003DC3D6`/`003DC3DB`); `003DCD00` also admits an entry only while its
  `003DC8D0` size fits a 4×32 KB budget.
- `003DCA30` walks three list heads. Head A (`02B58188`) has no code installer; head C (`02B58180`) is only ever
  reset to null. Head B (`02B58178`) is installed by the AREA bind callback `003EA710` (registered at `003EA947`)
  as `ard_blob + dword[ard + 0x2C]` — the one authored list on the path.
- The list is `{u32 count; entries {u32 keyA, u16 keyC, u16 keyB, u16 mappedId, u16 pad[3]} stride 0x10}`: `keyA`
  matches the caller's object key (shipped values `0x6Dxxxx` / `0x6Exxxx` / `0x73xxxx`), `keyB` the original id,
  `keyC` the sub selector. **All 166 distinct `.ard` resources parse** — the archive holds 332 paths because each
  ships byte-identically under `plan_master/in/` and `plan_master/ch/` (census counts 3,546 entries over the
  copies). Mapped ids run 56–2306; two entries map to `0xE4` — still requested under kind `0x1E`, so harmless to
  RC-30.

## 3. The route that requests the files (`rc30c_data_fields.py` S3)

**Request.** `003C1F00` is the location-map pane loader:
- it reads `menumap_common` (`[widget 02B457E0] + 0xE8`) entry `edi`'s byte `+1` (`003C2068`);
- if that byte is non-zero, it requests **kind 7, id `0xE1 + byte`** through the pool core (`003C2071`–`003C208D`);
- it keeps the buffer at **widget `+0x118`** (`003C209D`).

**What ships.** The byte is non-zero in exactly two of the 48 entries, identically in all nine language copies:

| entry | byte `+1` | request |
|---|---|---|
| 40 | 1 | `0xE2` `Loca_gil.cl2` |
| 46 | 2 | `0xE3` `Loca_bhm.cl2` |

- No entry selects 3, so **`Loca_rbl.cl2` (`0xE4`) is never requested.** It is also sized −1 in `FileSizeTable_US`
  (the second record, §3).
- Control C3: the file reads as 48 entries over 47 persistence groups, the join the lmap page makes.

## 4. The reader (`rc30c_cl2_reader.py`)

**Who reads it.** In the widget module, `+0x118` has one reader besides the release: `003C26C0`
(`tools/dispscan.py 118 118` over `003B0000`–`003D0000`). It takes `[widget + 0x118]`, or the fallback
`[widget + 0x110]`, as the CLUT for a location-map image:
- `0024A9E0(buf, 0)` returns the picture header `buf + 0x10`. Further pictures step by `u32 [pic]` while
  `k < u16 [buf + 6]`.
- palette = `pic + u16 [pic + 0xC] + u32 [pic + 8]`; count = `u16 [pic + 0xE]` (`003C27B0`–`003C27C1`).
- `0024A480(image, name, kind, palette, count)` registers the image with that external palette (`003C281D`–`003C2824`).
- `0024A1D0` later copies the palette in 64-byte groups for the upload (from `0024A2E0`).

**The layout.** The CLT2 file is a **TIM2-shaped container**. The first record's field names map onto it:

| offset | first record's name | TIM2 reading |
|---|---|---|
| `+6` | — | u16 picture count |
| `+0x10` | `endOff` | u32 picture total size |
| `+0x14` | `dataSize` | u32 CLUT size |
| `+0x18` | — | u32 image size (0) |
| `+0x1C` | `fieldLo` = `0x30` | u16 header size |
| `+0x1E` | `count` | u16 colour count |
| `+0x40` | — | the palette |

**Checks.**
- D1: all 20 shipped files fit this reading.
- Control C1: the same picture-header arithmetic fits a shipped TIM2, `loca_00.tm2` (header `0x70` + image
  `0x100000` + CLUT `0x400` = total).
- D2: **`+0x22` / `+0x23` (`kindLo` / `kindHi`) are not read** by `003C26C0` or `0024A9E0`. So the "variant" selects
  nothing on this path.

**Remaining fact (static):** the component order. `0024A1D0` copies the entries whole, so the byte order is whatever
format its upload declares for the palette texture. That upload was not read here.

## Consumer check

| consumer | finding | state |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` row RC-30 | §3 / §4 | routed-to-SWE2-CONTRACT (row text below) |
| `cl2-menu-colour-tables.md` §3 / §7 ("no constant-request site", "no reader found" for every header field, "component order / variant not established") | §3, §4 | routed-to-SWE2-CONTRACT |
| `../rc-residue-0930/README.md` §2 D ("no reader of a `loca_*.cl2` is reachable through any route traced") | superseded by §3 | revised-here: the sentence is struck in that record with a pointer to this one |
| `../rc22-34-resource-readers-0930/README.md` §3 RC-30 ("no static request route … outside three index-computed sites") | superseded: the route is `003C208D`, a register-held site the list missed | revised-here: the row and the paragraph are struck in that record with a pointer here |
| `../rc22-34-resource-readers-0930/cl2_requests.py` S2 (its list of computed-id kind-7 sites) | lacks `003C208D`; it prints the list and asserts only the decode, so it is not wrong, only incomplete | agrees (this record's `rc30c_kind_slice.py` is the complete census) |

## Crossings into other layers

The request and the reader belong to the location-map pane (UI). They cross into:
- **Resource**: the pool request core, the kind-7 path array, the TIM2 container helper, and the image registry that
  takes the palette;
- **Party / battle, actor resources, effects, script VM**: the sites of §1–§2, read here only to bound their kind
  argument.

No neighbour body's semantics is claimed beyond the instructions pinned in the scripts.

## For SWE2-CONTRACT (RC-30 row)

> **ANSWERED 2026-09-30 (SWE2-DATA, `_index/candidates/rc30-census-0930/`, three scripts FAILS 0):** the location-map pane loader `003C1F00` requests kind 7 id `0xE1 + byte [menumap_common entry + 1]` (`003C207A`–`003C208D`) and keeps the buffer at world-map widget `+0x118`. Only entries 40 (→ `0xE2` `Loca_gil.cl2`) and 46 (→ `0xE3` `Loca_bhm.cl2`) select one, in all nine copies; `Loca_rbl.cl2` is never requested. `003C26C0` reads it as a TIM2-shaped CLUT through `0024A9E0`: picture header at `+0x10`, palette at `pic + u16[pic+0xC] + u32[pic+8]` (= `+0x40`), colour count `u16 [+0x1E]`. So `+0x10` is the picture total size, `+0x14` the CLUT size and `+0x1C` the header size. The palette is handed to `0024A480` as an external CLUT for a location-map image. `+0x22` / `+0x23` are not read. Every other data-driven `(kind, id)` source carries a constant non-7 kind, and the two script verbs that take a kind are unused. Open (static): the byte order the palette upload in `0024A1D0` declares.
