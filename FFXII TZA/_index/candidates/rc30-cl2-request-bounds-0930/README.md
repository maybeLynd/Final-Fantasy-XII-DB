# RC-30: the loca_*.cl2 request exists, its authored selector, and the reader (ORACLE, 2026-09-30)

## The question

RC-30 asks which function reads a loaded `loca_*.cl2`: its header (`+0x10` endOff, `+0x14` dataSize, `+0x1C`
fieldLo, `+0x1E` count, `+0x22`/`+0x23` variant) and its palette. The answer should give the colour component order
and say whether the variant selects a decode path.

SWE2-DATA's narrowing (`../rc22-34-resource-readers-0930/` section 3, commit `1261e2044`) found no route to kind 7
ids `0xE2`-`0xE4`. It left open three computed-id sites and "18 path-API sites whose kind is computed".
ORACLE's `../rc29-console-cl2-lst-mg-0930/` bounded one of the three and left two residues. The coordinator asked for
the rest to be bounded.

## Method

- **[`rc30_census.py`](rc30_census.py), output [`rc30_census.out`](rc30_census.out) and [`rc30_census.tsv`](rc30_census.tsv).**
  An independent census of **every** call site of the request and path APIs:
  - kind in `ecx`: `ResourcePath_Get` `002DF980`, `ResourcePath_Copy` `002DF880`, `0032E400`, `0032E620`, `0024AB90`;
  - kind in `edx`: the pool front ends `00249180`/`210`/`3D0`/`350`/`320`/`380`.
  The `(kind, id)` arguments are resolved with OPUS's value-set dataflow (`../rc9-log-channels-0930/rc9_channels.py`,
  resolved through callers to depth 4). Controls K1-K3 pass. The census gives 191 sites:
  - 94 exclude kind 7;
  - 49 are kind 7 with an id the dataflow resolves (none is `0xE2`-`0xE4`);
  - 46 are OPEN;
  - 2 were not reached from their function's entry.
- **[`verb_census.py`](verb_census.py), output [`verb_census.out`](verb_census.out).** Verb-call counts over all 7,562
  distinct shipped `.ebp` (198,302 actor scripts), using FABLE's decode rules. Control: `debug_mapjump` is found 1,545
  times.
- **[`rc30_bounds.py`](rc30_bounds.py), output [`rc30_bounds.out`](rc30_bounds.out).** The hand bound of every OPEN
  site, each asserted against the image bytes (B1-B8). All pass.

## Result

**RC-30: ANSWERED.** There is a `loca_*.cl2` request, the authored data selects two of the three files, and the
reader is `003C26C0`. It reads the file as a TIM2 picture header plus palette. The `+0x22`/`+0x23` variant is not
read.

### 1. Every kind the API sites can pass is bounded

A raw rip scan finds that only `ResourcePath_Get` and `ResourcePath_Copy` read the path table `0215F000` (B1). Copy's
only caller passes kind 4 (B1b). Every OPEN site whose kind was unresolved is bounded away from 7:

| sites | kind source | kinds |
|---|---|---|
| `001BB397`, `001F5E64`, `002EEF70`, `00863144` (via `002E98F0`), `002E6776`, `002EADEA`, `002EAE08`, `002E9988`, `002E99A8`, `002E700C` | the packed-code decoder `002ED6F0`, every arm read | 0x1, 0xD-0x10, 0x12-0x14, 0x16-0x19, 0x22 |
| `001DA31B`, `003DDAB9`, `003DF593`, `003E9F59`, `00332280` | the manager formula `0032F170`, and `0032FCA0`'s copy of it | 1, 5, 8 |
| `0032F617` | `rdi + 8` after the loop that counts `rdi` down to 0 | 8 |
| the six `003A13F0` sites | `002ED8C0` | 0x20 |
| `003DC977`, `003DC683` | `003DCA30`, whose only store through the kind pointer is 0x1E | 0x1E |
| `003EAE29` and the other `003EADE0` request | the BGM stream descriptor `02B5E0FC`, written only at `003EB10C` | 0x24 |
| `002E61A8`, `002E6277` (in `002E60F0`, not reached by the dataflow) | constants | 0x20 |
| `0050DF9D`, `0050E039` | the script stack of `debug_filesize` `0x2006` / `debug_fileread` `0x2007` | shipped bytecode calls them 0 times |

These are this record's 27 unresolved-kind sites. SWE2-DATA's count of 18 used a narrower definition, and all of its
sites are within these 27.

### 2. Every kind-7 site with a computed id is bounded

- `002CEAE0`: `0x10 + d`, with `d` a guest's party row, so `0x10`-`0x37` (`../rc25-party-definition-rows-0930/`).
- `003C9950`: `0x0E`-`0x14` (the rc29 record).
- `00575C30`: its category byte comes fresh only from `0056F2A0`, which posts it only when it is at most 5
  (`0056F2BD`). The other senders replay an accepted value: `+0xD2` is written only at `00575CD2`, and the history
  sits at `+0xD4`. So the id is at least `00D23740[0..5]` = 552-852, and the question about bytes 6 and 7 does not
  arise (B6).
- The rest are SWE2-DATA's bounded sites: the list helpers, `0xE8 + byte`, `0x496 + byte`, `0x142 + dil`,
  `0x129`/`0x12A + byte`, table + 1, `0xAA + i`, `0x98 + i`, and the font table.

**One site is new, and it is the answer.** `003C1F00`'s second request, `003C208D`, is not in SWE2-DATA's list:
- it requests kind 7 id `0xE1 + b`, where `b` is byte `+1` of entry `rdi` of `[[02B457E0] + 0xE8]`;
- it requests only when `b` is non-zero, and stores the buffer at `[02B457E0] + 0x118` (B7a);
- `+0xE8` is kind 7 id `0xA4`, `menumap_common.bin` (`003BC35D`);
- the byte is the `CmapEntry.page` field of the `cmap` sheet.

Across all 9 shipped copies, exactly two entries are non-zero (B7d):

| entry | name | byte | request |
|---|---|---|---|
| 40 | gil01_s02 (name id 60181) | 1 | `0xE2` `Loca_gil.cl2` |
| 46 | bhm01_s01 (name id 60187) | 2 | `0xE3` `Loca_bhm.cl2` |

**No entry selects 3, so `Loca_rbl.cl2` (`0xE4`) is requested by nothing in shipped data.**

### 3. The reader, `003C26C0`

It takes the buffer at `+0x118`, or the buffer at `+0x110` when `+0x118` is empty, and calls the section
walker `0024A9E0(buf, 0)`. That walker returns `buf + 0x10`, so the file's `+0x10` block is read as a **TIM2 picture
header**:

| file offset | the page's name | TIM2 picture field | read? |
|---|---|---|---|
| `+0x10` | endOff | TotalSize | only for section index 1 and up; index 0 is used, so **not read** |
| `+0x14` | dataSize | ClutSize | **not read** |
| `+0x18` | (0) | ImageSize | **read** (`003C27B4`), 0, added to the palette offset |
| `+0x1C` | fieldLo = 0x30 | HeaderSize | **read** (`003C27B0`): palette = `+0x10 + 0 + 0x30` = file `+0x40` |
| `+0x1E` | count | ClutColors | **read** (`003C27B7`): 512 or 32 colours |
| `+0x22` | variant, 3 | ClutType | **not read** |
| `+0x23` | variant, 5 / 4 | ImageType | **not read** |

- **Binding.** `0024A480` stores the palette and count as a palette override in the page image's entry (`+0x28`,
  `+0x38` count << 18). The image upload `0024A1D0` decodes it with `00180E70`, passing **the image's own** ClutType
  and ImageType bytes (`[picture header]+0x12`/`+0x13`, at `0024A36E`/`0024A372`).
- **The variant selects no decode path.** The `.cl2`'s own `+0x22`/`+0x23` are never read. Its values (3 with 5 or
  4) are the TIM2 ClutType / ImageType pair for 32-bit colours with 8-bit or 4-bit images.
- **Component order.**
  - `00180E70` copies the colours in 16-entry rows, one 32-bit colour per entry.
  - For the type pairs `0x105`/`0x205`/`0x305` and `0x4104`/`0x4204`/`0x4304` it only un-swizzles the PS2 8-entry
    block order.
  - It never reorders the bytes inside a colour, and it passes the rows to `0017F3B0` ~~as texture format 1~~ *(narrowed 2026-09-30, SWE2-ORACLE, per `SWE2CONTRACT-CONTRA-ORACLE-RC30-RC25-0930`: `1` is the count argument `r9d = 1` (`00180F81` / `00180F87`), which `0017F3B0` keeps in `r15d` (`0017F3E9`) and uses as a count (`0017F440` / `0017F447`). The format is the fixed object `02CF7480` (`0017F419`), named `RGBA8`; `0017F3B0` rescales byte 3 as a PS2 alpha)*.
  - So the order is the file's byte order, the same as every TIM2 CLUT the engine binds. By TIM2 convention that is
    R, G, B, A, with the 4th byte an alpha of 0 to 255 (the page's measurement). ~~This record does not trace
    `0017F3B0`'s format 1 to a DXGI format.~~ *(Superseded 2026-09-30, SWE2-ORACLE: there is no "format 1". The
    format object is `RGBA8`, per SWE2-CONTRACT's `rc_round3_check.py` B1-B5. The conclusion, no byte reordering and
    order R, G, B, A, stands.)*
- **No magic check:** `CLT2` is not tested.

## Corrections to route (not edited here)

- SWE2-DATA's `cl2_requests.py` S2 list omits `003C208D`, the request that exists.
- The `.cl2` page's field names should be the TIM2 picture-header names: `+0x10` TotalSize, `+0x14` ClutSize,
  `+0x18` ImageSize, `+0x1C` HeaderSize, `+0x1E` ClutColors, `+0x22` ClutType, `+0x23` ImageType. The file is a
  one-picture TIM2-style container with no image.
- The `cmap` sheet's `CmapEntry.page` field (`+1`) is the `.cl2` selector: `0xE1 + page`.

## Not claimed

- When the map screen enters entries 40 and 46 in play. The entry index is the menu's selection.
- What the `+0x110` fallback buffer holds.
- ~~`0017F3B0`'s format 1 as a DXGI format.~~ *(withdrawn 2026-09-30, SWE2-ORACLE: `1` is a count; the format object is `RGBA8`, as above)*
- The 46 OPEN sites whose kind is 7 are bounded through SWE2-DATA's per-site bounds, or here where named. The
  dataflow's 49 resolved kind-7 sites were not re-listed by hand.
