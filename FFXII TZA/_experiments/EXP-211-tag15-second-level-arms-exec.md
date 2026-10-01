# EXP-211 — `002AC5F0` tag-15 second-level sub-arms, executed

**Status:** complete — **503/503 cases, stable across 3 independent runs,
byte-identical `result.json` (SHA256
`d3378248ac68fa4b361ffae823e5ecc150cbaf4dddc3553d2fe8b1e146d9fa16`), zero
unexpected faults.**
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes executed
under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py` (extends
EXP-192..210; 466 inherited + 37 new/changed `c5f0-*` cases)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Scope

The tag-15 arm at `0x2AD01A` re-dispatches on the byte after `\x0f`:
`idx = sub − 0x20`, `kind = b[base + 0x18E3FC + idx]`, target =
`base + d[0x2AE370 + 4·kind]` — **the jump table is kind-indexed**;
many sub bytes share arms. This package promotes the two pure decoders
and exercises 35 representative sub-arm cases.

## Bodies promoted real this round

- **`003FFAB0`** — the param decoder every arm calls: `rcx` = string
  cursor, `rdx` = byte out. `b[+1]&7 != 0` → direct
  `(b[+1]&0xC0)·2 | (b[+2]&0x7F)`; `b[+1]&7 == 0` → escape path through
  `39BA00`. Returns `eax = 3` (bytes consumed).
- **`0039BA00`** — compact escape-table lookup: reads
  `q[0x2AEE870]` (a **runtime-built BSS table** — planted by the new
  `ba00t` fixture) and returns `b[table + 1 + 5·(cx & 0x1FF)]`.

New boundary stubs (deep/runtime-dependent callees, disclosed):
`3FFEE0`, `3FFBC0`, `3FFD70`, `3FFC60`, `3FFCE0`, `3FFDA0`, `3FFB00`,
`3FFB90`, `3FFF10`, `39BA30`, `17FD30`, `2B1ED0`, `2B4730`, `3A1DB0`,
`2AE610`, `2AEB20`, `2639E0`.

## Sub-arm semantics now executed

| sub | kind → arm | executed behavior |
|-----|-----------|-------------------|
| `0x30`/`0x5F` | 0x0D/0x22 → ret-1 tail | cursor already +1 from the head; ret 1 (`f30`/`f5f`) |
| `0x22` `"` | 0x02 → `0x2AD1ED` | `3FFEE0(&sub, 0, &state+0x9E)` quoted skip; cursor += 1+ret (`f22`, fee0n=5 → cursor+6) |
| `0x2C` `,` (+`0x2F`,`0x3B`,`0x70`) | 0x0A → `0x2AE308` | pure `3FFAB0` param skip, ret 1 (`f2c`) |
| `0x56` `V` | 0x1D → `0x2AE2F0` | `3FFAB0` + `d[aux]=0` (`f56`) |
| `0x24` `$` | 0x04 → `0x2AD252` | param → `f[state+0x4C]` = `float(movsx(p))`, gated by `d[state+0xB0]&0x2000000` (`f24`/`f24s`) |
| `0x23` `#` | 0x03 → `0x2AD205` | `p != 0` → `w[state+0x88] = p·0x1E`, `b9B=1`; `p == 0` (via escape) → `w88=0x2710`, `bB0=5`, `dB0 \|= 0x4080000` (`f23`/`f23z`/`f23e` — `f23e` decodes `ba00t[1]=0x37` through real `39BA00` → `w88=0x642`) |
| `0x21` `!` | 0x01 → `0x2AD151` | `39BA30(b[state+0xA6],1)` → `q60/q68` font rec; `254A10()==0` → `d44 \|= 0x800`, `17FD30(7,0)`, `d[0209CC30]=7`, `d[0209CC34]=0`; `!=0` → `17FD30(bA6,1)`, `cc30=bA6`, `cc34=1`; tail clears `q[0209CC70]`/`[0209CC78]`, calls `2B1ED0(state)`, cursor **+2** total (`f21`/`f21a`) |
| `0x25`/`0x26`/`0x27` | 0x05 → `0x2AD289` | align family: `b99=param`, `b9A=sub`, `b[ctxo+0x1104]=sub`; `ctxo b1102 != 0` → nested `2B2150` then real `2B1F20` dispatches on `b9A`: `0x25` → `float(b99)`, `0x26` → `int(w94)−nested_h+b99`, `0x27` → `int(w94)/2+b99` (`f25`/`f25n`=7.0, `f26n`=55.0, `f27n`=31.0) |
| `0x28` `(` | 0x06 → `0x2AD2F4` | `f34 = param/24.0` h-scale; `254A10()==0 && q68 && param≥24` → `b44 = int((p−24)·0.25)` (`f28`: 48→2.0,b44=6; `f28l`: 16→0.667,b44=0) |
| `0x37` `7` | 0x14 → `0x2AD38A` | `f34 = param/100.0` v-scale; `param≥100` → `b44 = int((p−100)/16.6)` (`f37`: 120→1.2, b44=1) |
| `0x20` ` ` | 0x00 → `0x2AD041` | `f40` override; `p==0 && old==0` → ret-1 early; old≠0 → `17F920(1)` kern → `cc68 = f920·f34·f38·old`; `d44&0x800` adds `f34·f38` (`f20`/`f20r`=60.0/`f20k`=66.0) |
| `0x29` `)` | 0x07 → `0x2AD3F7` | colour via `3FFBC0(&sub, &d30)`; **`b[e312+0x33]` is saved pre-parse and restored over d30's top byte** → `d30 = colour & 0xFFFFFF`; `d30==0` → `0x80808080`+alpha-select; `b[A8]==0xFF` absorbs `b[9F]`; mirrored to `d[ctxo+0x10D0]`; shared alpha tail merges `b9F` hi-nib (`f29`: `00223344`/`f29z`: `00808080`) |
| `0x2B` `+` | 0x09 → `0x2AD76B` | `3FFAB0` alpha (param `0xFF`→0) → shared `0x2AD78B` tail: `b9F = alpha \| (old_b9F & 0xF0)` when hi-nibs differ (`f2b`: 0x50\|0xA0=0xF0) |
| `0x2D` `-` | 0x0B → `0x2AD8AB` | `3FFC60(&sub, &tmp, &state+0xA1, 0)` → cursor += ret; then `2AE610(state, &sub, &f16copy, aux)`; `d[aux]=0` (`f2d`) |
| `0x31` `1` | 0x0E → `0x2ADBF5` | `3FFF10(&sub,0,0,0)` → cursor += ret (`f31`, ff10n=6 → cursor+7) |
| `0x34` `4` | 0x11 → `0x2ADD03` | `3FFAB0` → `b[state+0xA9] = param` (`f34`: 0x12) |
| `0x35` `5` | 0x12 → `0x2ADD19` | `b[state+0xAA] = param`; `ctxo b1102 != 0` → `f[params] = float(movsx(param))`; `b[ctxo+0x10FD] = param` (`f35`/`f35n`=18.0) |
| `0x36` `6` | 0x13 → `0x2ADD62` | `b[state+0xAA] = −param`; `b[ctxo+0x10FD] = −param` (`f36`: 0xEE) |
| `0x33` `3` | 0x10 → `0x2ADC5A` | `3FFDA0(&sub, &state+0x38, &state+0x3C)` writes `f38`/`f3C` (`f33`) |
| `0x6F` `o` | 0x21 → `0x2ADCDD` | `3FFB00(&sub, &w)` → `f[params] = float(movsx(w))`; tail clears `q[0209E598]` + `17FAE0(0)` (`f6f`: 40.0) |
| `0x32` `2` | 0x0F → `0x2ADC71` | `param==0` → `d[ctxo+0x10E0] = d[params]`; `param!=0` → `f[0209CC68] = max(0, 2·p − (f[params] − f[ctxo+0x10E0]))` (`f32`/`f32a`=no write/`f32b`=34.0) |
| `0x40`–`0x6B` | 0x1C → `0x2AE1F1` | catch-all: `0xD0` state copy, alpha from `d[ctxo+0x10DC]·f[ctxo+0x10E4]`, `b[ctxo+0x10FC]=1`, nested `2AEB20(copy, ccp, params)`, cursor += ret, `bA9=0`, `d[aux]=1` (`f42`) |

## Corrections of record

**The big one — dead assertions since EXP-206.** Every `elif` assert for
`b3120-*`, `b3050-*`, `b24b0-*`, `b2150-*`, `af340-*` and `c5f0-*` was
nested inside the `elif name.startswith(("fa3b0-", ..., "c5d0-"))` block
— those six prefixes were absent from the tuple, so the semantic checks
never ran; EXP-206..210 "pass" results only proved the generic
no-fault check. The guard now admits all sixteen prefixes and every
assert executes. EXP-208..210's promoted bodies still pass under live
asserts, but several stub-era expectations were wrong and have been
corrected against executed behavior:

- **`229E40` reads `d[01E02814]`, not `01E02E14`** — fixture renamed
  `e2814v`; the tag-7 `==7 → 0x1A` gate is now genuinely exercised
  (`tag7a` → `cc68 = 156.0`).
- **`002AC5F0` prologue zeroes `d[r9]` (the aux out) at entry** — params
  presets must use a distinct aux buffer (`auxout`) to survive.
- **`2B3050` armed path:** `39C4A0` calls are `(0)` (2AC1E0 init) then
  `(1)` (`(d44>>0xB)&1` after `bts`); the result lands `q[state+0x60]`,
  not `+0x80`.
- **`2B24B0` byte outs:** the `b1100 → out+0x51` copy is **gated on
  `ctxo b10FE`** — a tag-5 string leaves `+0x51 = 0` despite
  `b[ctxo+0x1100]=1`.
- **Tag-14's `b10FE` = `(d[rsp+0x48] == 0)`** — a `3FFDF0` stack-passed
  out cell; new `df0v` fixture writes it. `b1101` is set
  unconditionally.
- **Nested self-calls are invisible**: `addr == self.entry` skips the
  rargs record, so `2B2150`'s own nested call couldn't be counted — new
  `l2b2150n` call-site tag at `0x2ACDF9` proves the `ctx48==0` gate
  fires (`b2150-lite`).
- **`2B2150` restores `ctxo b10FC`/`b10FF`** at exit — post-run values
  are the presets, not the mid-walk clears (`b2150-lite` now asserts
  `0xAB`).
- **`af340-tag2` recount:** tag-2's nested measure does not consume the
  `\x05` — the outer walk re-interprets it → 3 nested `2B2150`, 2
  `2AC5F0`.
- **Colour arm d30** carries `old_b33` in its top byte (saved pre-parse,
  restored after) — `0x11223344` stores as `0x00223344`.
- **`!` arm cursor advance is +2** (head +1, arm +1).

## New fixtures

- `ba00t {idx: byte}` — planted escape table; `q[0x2AEE870]` points at
  it (`39BA00` reads `table[1 + 5·(b2 & 0x1FF)]`).
- `paramd`/`paramf` — presets on the params block (must pair with
  `r9="auxout"` — the prologue clears `d[r9]`).
- `auxout` — a separate aux-out alloc so `d[r9]` clears don't clobber
  `params`.
- `df0v` — `3FFDF0`'s stack-passed out cell (drives tag-14's `b10FE`).
- `s254a10_ret`, `fee0n`, `ba30v`, `fbc0n`/`fbc0v`, `fc60n`, `ff10n`,
  `fda0n`/`fda0a`/`fda0b`, `fb00w`/`fb00n`, `eb20n`, `e312b`/`e312d` —
  stub return/out keys for the new boundaries.

## Not claimed

`live_game: false`. The deep parsers (`3FFEE0`/`3FFBC0`/`3FFDA0`/`3FFB00`/
`3FFDA0`-family), font-resource lookups (`39BA30`/`2639E0`), and the
`2B4730`/`3A1DB0`/`2AE610`/`2AEB20`/`2B1ED0`/`17FD30` helpers stay
disclosed scripted boundaries. The `0x1C` catch-all's nested `2AEB20`
and the unexercised kind arms (`0x1E`/`0x1F`/`0x20` tiny field writes,
`0x08` icon-block via `3FFD70`, `0x0C` via `3FFCE0`, `0x15`/`0x19`/`0x1A`/
`0x1B` variants) run native but are fixture-dark or stub-bounded.
