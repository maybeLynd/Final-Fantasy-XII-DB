# EXP-205 — `0031C5D0` kind-dispatched resource resolver, executed (type-0x1A arm)

**Status:** complete — **431/431 cases, stable across 3 independent runs,
byte-identical `result.json` (SHA256
`106eb70187221dffe85d712c23d45aa7a98b7082a4b66f64057374e8a1d9cf4b`), zero
unexpected faults.**
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes executed
under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py` (extends
EXP-192..204; 424 inherited + 7 new `c5d0-*` cases)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Scope

EXP-201..204 left exactly two scripted edges on the display path, both in the
type-2 arm: `0031C5D0` (deep resource resolver called by real `0035D330`) and
`002B3050` (string copy, ~131-body CRT subtree — deferred). This package
promotes `0031C5D0` to executed bodies together with the `002F9860` bucket leaf
its type-`0x1A` arm calls. The other 31 kind arms are disassembled but only
kind `0x1A` (used by the display path), kind 1 (auto-kind rewrite), and the
out-of-range dispatch are fixture-exercised here.

## `0031C5D0(blk)` — kind dispatch over a resource descriptor

- `d[blk]` = kind; `q[blk+0x18]` cleared at entry. `kind-1 > 0x1F` (unsigned)
  → validate path `00322C50(d[blk], d[blk+4], 0)` → 0 → **`-2`**
  (`c5d0-kind0`, `c5d0-kind33`).
- **kind 1 = auto-kind:** `00309440(w[blk+6])` reads the shipped remap
  `d[01EEBCF8 + (w6>>0xC)*0x58]` = **`5 + hi-nibble`** — rewrites `d[blk]`
  and re-dispatches (`c5d0-auto`: `w6=1` → `d[blk]=5` observed, kind-5 arm
  then fails `-2`).
- Each remaining arm validates `00322C50(kind, d[blk+4], 0)` — failure →
  **`-2`** (`c5d0-noval`: id 7 >= count 3).
- Return: `0` success, `-2` validation/lookup-gate failure, `-1` via the
  `0x31E57A` tail (not reached on arm 0x1A).

## Type-`0x1A` arm (`0031E137`) — the display-path resolution

`0035D330(0x1A, id)` fills `d[022CA520]=0x1A`, `d[+4]=id` and calls this arm.
Under fixtures the full chain executes:

- **Validator** `00322C50(0x1A, id)`: `q[02EBF118]` non-null **and**
  `id <= d[T1+4]-1` — the bound is the **same `02EBF118` descriptor cell the
  per-bit cascade table uses** (`CASCD`; the kind-0x1A L1 rows ARE the
  cascade rows).
- `L1row = elemb + d[T1+0xC] + w[T1+8] * id` — the standard authored-table
  idiom (`0020E600` = `elemb + off`, `elemb = q[01F83530]`).
- `w[L1row]` packs two indices: **`hi5 = w>>0xB`** selects
  `d[02EBF170-desc + 4 + hi5*4]` (a T2 index table of elemb offsets → a T3
  inline table), **`lo11 = w & 0x7FF`** selects `d[T3 + 4 + lo11*4]` →
  `elemb + that` → **`q[blk+0x18]`** (the resource data pointer — for
  type-2 display, the name string consumed by `002B58B0` → `q[entry+0x30]`).
- Field copies from the L1 row: `b[blk+0x20]=b[row+0x10]`,
  `b[+0x21]=b[row+0x26]`, `b[+0x22]=b[row+0x27]`, `b[+0x23]=b[row+0x13]`,
  **`b[+0x24]=b[row+2]`** — the `0xFF` byte `003BBD00`'s type-2 pre-gate
  rejects on (`bd00-t2ff` now proves the byte comes from the row).
- `q[blk+0x10]` = `002F9860(w[row+0xA])` — a bucket resolver
  (`x/1000` → `q[02EC3D80 + i*8]` gate → `q[02FF93C0 + i*8]` bucket desc →
  `x%1000`-indexed element). Both bucket tables ship zero → the resolver's
  **early-out default `0x1CEB638`** is what fixtures observe
  (`c5d0-ok`, `bd00-t2`).
- `b[blk+0x25]` = **`((w[row+6]>>0xD)&1) | ((b[row+0x24]<<1) & 0x1E)`** —
  bit-by-bit XOR-mask composition (`c5d0-b25`: `w6=0x2000`, `b24row=0xB` →
  `0x17`). `00506700` then dispatches colour: `b25&2 → 2DD7E0(style)`;
  `&4 → 2DD7E0(0x12)`; `&8 → 2DD7E0(0xB6)`; `&0x10 → 2DD7E0(0xF3)`
  (`bd00-t2b25`: `b24row=2` → `b25=4` → `2DD7E0(0x12)` → `d[entry+0xC]`).
- **T2-null is graceful, not a failure** (`c5d0-not2`): `q[02EBF170]==0`
  → `q18 = 0` but field copies, `q10`, `b25` and return `0` still happen —
  the `-1` tail is not in this arm's shape.

## End-to-end type-2 consequences

- `bd00-t2` now runs the real resolver twice (`003BBD00` gate + `00506700`
  arm) — `q30 = 002B58B0(q18)` skips the empty 2-byte tag → `elemb+0x80002`,
  `w3A=3`, `b3F = b[req+8]`, `d0C = 0x80808080` (b25=0 → no colour lookup),
  `s2b3050` sees `rdx = q30`, `r8/r9 = slot+0x40/+0x42`.
- `bd00-t2neg`: `cascd=None` → null `02EBF118` → validator 0 → `-2` →
  `0035D330` memsets the 0x98 blk → `b24=0` → gate *passes* — the negative
  result does not reject the request.
- `d4d0-near`: `003284D0`'s arg becomes the resolver id (`d[blk+4]=5`); the
  `l1row` fixture follows `c5id`.

## Corrections of record

- **`02EBF118` is `CASCD`** — the kind-0x1A L1 table is the per-bit
  cascade table `0030E360` already consumes (`row = elemb+off+stride*idx`,
  `d[row+0xC]` cascade mask). EXP-193's `cascd` fixture and kind-0x1A's T1
  descriptor are the same object; the kind-0x1A arm reads additional row
  fields (`w0` index pack, `w6`, `wA`, `b2` gate byte, `b10/13/24/26/27`).
- `00309440`'s remap base is `01EEBCF8` (ships `5+hi`), not `01ECBCF8` —
  same class of transcription slip as EXP-204's `022C8064`.
- `002F9860`'s early-out default pointer is `0x1CEB638` (read live, not
  hand-computed).
- `002B3050` remains scripted — its transitive closure is a ~131-body
  CRT/formatter subtree; only `31C5D0`'s 9-body closure was promoted.

## Validation

`python check.py` — 431/431, three independent runs, `result.json` SHA256
`106eb70187221dffe85d712c23d45aa7a98b7082a4b66f64057374e8a1d9cf4b`
(byte-identical), zero unexpected faults.
