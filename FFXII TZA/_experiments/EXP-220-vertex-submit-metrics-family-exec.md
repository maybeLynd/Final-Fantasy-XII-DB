# EXP-220 — `1E8070` vertex-batch submitter + `17Fxxx` metric/getter family + `1E7A20` vector insert

**Status:** complete — **536/536 cases, stable across 3 independent runs,
byte-identical `result.json` (SHA256
`ba21a95191a6` prefix; 536 cases), zero unexpected faults** (the 10
faulted cases are all pre-existing intentional-null fixtures that
assert the fault).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..219; +11 cases this round)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Bodies promoted real this round

| body | semantics |
|------|-----------|
| `001E8070` | vertex-batch submitter (278 insns) — EXP-219's disclosed scripted boundary, now real. `rbx`=dev (`q[0x1F811F8]`), `r13`=source state. `d[state+0x9C]` mod `0x1C` → `1E94E0` ext-metric record; negative index → default record `dev+0x1358`. If `q[dev]` null → straight to epilogue. 2×3 vertex loop expands the source into `0x3C`-byte records: `x = f[st+(v>>1)*4] / d[devsub+0x24]`, `y = (d[devsub+0x28] − f[st+8+(v&1)*4]) / d[devsub+0x28]`; `r14` walks `st+0x2C+k*4` (`k=o+i∈0..3`) feeding `rec+0x0C/+0x10/+0x14/+0x18` raw floats and `rec+0x1C..+0x34` as `d[rec_metric+X] × cvtdq(d[st+…]) × (1/128) / 255`; `rec+0x28` takes `d[r15+0x20]×(1/128)` when slot flag `b[+0x2348]` set else `d[st+0x8C+k*4]×(1/128)×f[dev+0x137C+k*4]×d[r15+0x20]×(1/128)`; `rec+0x38 = d[r15+0x10]×(1/128)`. Appends via `q[dev+0x10]` vector (grow → `1E7A20`). Per-vertex bounds accumulate in slot `d[dev+0x20]` (stride `0x2C`): flag `+0x2324`=1, A min/max `+0x2328/2C/30/34`, B-mirror mins `+0x2338` (x) and `(slot+0xCD)*0x2C` = `+0x233C` (y) — compared against the **raw stream floats** `f[st+0x1C+k*4]`/`f[st+0x2C+k*4]`, not the computed pos. Post-loop: `b[+0x2349]` set → writes `+0x2340` and `+0x2344` = `d[st+0x8C]×(1/128)×f[dev+0x137C]` then clears the flag; clear → writes `+0x2344` only. Epilogue resets `f[dev+0x137C..0x138B]` to `1.0` quad. |
| `001E7A20` | `vector<0x3C-rec>::insert` with `_Emplace_reallocate` (61+ insns): non-grow shifts tail `0x3C`, copies record, `end+=0x3C`; grow computes 2× capacity (count 1→2→4→8), virtual `alloc` at `q[obj+0x30]` vtable `+0x10`, three-copy splice, virtual dealloc at `+0x18`, updates `+0x00/+0x08/+0x10`. Verified: `e8070-grow` forces 3 reallocs — `salloc`/`sdealloc` scripted VAs ×3 each, final `begin=e7buf, end=e7buf+7*0x3C, cap=e7buf+8*0x3C`. |
| `001E94E0` | lazy metric-record getter: `record = dev + idx*36 + 0xF68`; flag `+0` unset → calls `19C5D0`/`1C5F20` (kept scripted — deep init boundary) then sets flag; returns record. Fixture plants flag=1 per record, exercising the hit path. |
| `0017F880`→`001E93C0` | font metric: `1B5FB0`→`q[0x1F81200]` map, `1B51C0(map,1)` exact-key find → `q[node+0x28]` value; `1B1620` flag `b[0x1F811E0]`; flag=0 → `ceilf(d[val+0x30] / f[val+0x34])` via real IAT `861F4A`→`0x1CCEF90` `ceilf` stub; miss → shipped const `f[0x901990]` = **23.0**. |
| `0017F8A0`→`001E9450` | same chain, `d[val+0x2C]` field (key 1). |
| `0017F960`→`001E9580` | same chain, `d[val+0x30]` (key 3). |
| `0017F980`→`001E9610` | same chain, `d[val+0x2C]` (key 3), via `225670`/`79CFA0` leaves. |
| `0017F920`→`001E9840` | `cl` selects: `0` → `1F49E0` → `d[q[dev1]+0x20]`; `!=0` → `1FDDC0` → `d[q[dev1]+0x1C]`. |
| `0017F9C0`→`001E9BD0` | `1B1620` flag=0 → `ceilf(edx / f[q[dev1]+0x34])` (`1FDDB0` scale leaf). |
| `0017F8C0`→`001E9860` | codepoint remap: `d[q[q[dev1+8]]+idx*4]` (vector begin) → `1FDEC0(devsub, remapped)` → inline map walk rooted `devsub+0x50`, returns `node+0x24`. |
| `0017F940`→`005C52D0` | getter leaf: `return q[dev1+0x28]` (saved-ctx slot). |
| `0017FAE0`→`00848C20` | setter leaf: `q[dev1+0x28] = rcx`. |

Support leaves promoted (2–23 insns each): `1B5FB0` (singleton
`q[0x1F81200]` behind `16D6A0` once-guard — `16D6A0` itself is
`ret`-equivalent), `1B51C0` (`std::map` lower_bound→exact-key),
`1B1620` (`b[0x1F811E0]` flag byte — shares the cell with real
`180150`), `1FDDB0`, `225670`, `79CFA0`, `225690` (`d[+0x24]` divisor),
`79E3C0` (`d[+0x28]` divisor), `1FDDC0`/`1F49E0`/`848C20`/`5C52D0`/
`1FDEC0` field leaves.

## Corrections of record — the stub values were wrong

- **`17F880` returns 7.0, not the stub's 6.5.** The real body computes
  `ceilf(d[val+0x30] / f[val+0x34])` — fixture `13/2.0 → 7.0`. Every
  raw `6.5` assert updated (`f(ctxe8)`, publish global `cc64`, tag-5/6
  heights); integer-ceil asserts (`w16==7`, `f58==7.0`) unchanged
  because `ceilf(7.0)==7`.
- **`17F920` arm values are `d[+0x20]=6` / `d[+0x1C]=5`**, so the
  tag-1/tag-4 advance under the fixture is `6.0`/`5.0` — the stub's
  symmetric `f920v` default collapsed them.
- **`ceilf` trace count doubled** in `bd00-t2`/`b24b0-run` (2→4): the
  real `1E93C0` ceils inside each `17F880` call on top of the
  evaluator's own ceils. Assert updated, not weakened — the count is
  now two sourced halves.
- **`1E8070`'s bounds compare raw stream floats** (`f[st+0x1C+k*4]`,
  `f[st+0x2C+k*4]`), not the computed x/y positions — min writes
  require `old>new`, so fixture slots start at ±1e30 sentinels.
- **`(slot+0xCD)*0x2C` is the B-array min_y** (`+0x233C` at slot 0) —
  earlier draft misread it as `+0x241C`.
- **`d[st+0x8C]` is the post-loop scale source** — an over-wide stream
  plant clobbered it mid-fixture; the streams only need `k≤3` reads
  (they stop at `+0x88`), so `+0x8C` is planted last.
- **Map miss returns `f[0x901990]` = 23.0f** (verified `0x41B80000` in
  xmm0), not the earlier guessed constant.
- **`17F7C0` is only reached via `2A9F00`'s gated glyph loop**, which
  no case drives — `1E8070` gets direct-entry cases
  (`e8070-append/grow/flag/neg`) through `17F7C0`'s real 0xA0 copy.

## New fixtures (all disclosed synthetic)

- `dev1` (`q[0x1F811F8]`, 0x2800): `q[dev1]`→`devsub` (divisors
  `+0x24/+0x28`, arm dwords `+0x1C/+0x20`, scale `f[+0x34]=1.0`, inline
  glyph map root `+0x50`); `q[dev1+8]`→`devrmp` codepoint vector;
  `q[dev1+0x10]`→`devec` emit vector (begin/end/cap at `+0x18/20/28`,
  allocator obj `+0x30` with fn ptrs `+0x10` alloc/`+0x18` dealloc →
  scripted `0x7000A100`/`0x7000A108` returning `e7buf`);
  `q[dev1+0x28]`=saved-ctx slot (default `0x1234`); ext-metric records
  `dev1+0xF68+i*36` (flag 1, ints `4+j`); scale quad `f[dev1+0x137C]`
  = 1.0×4; bounds slot seeded ±1e30.
- `devmap` (`q[0x1F81200]`): two-node metric map, key1→`mv1`
  (`+0x2C=12,+0x30=13,+0x34=2.0` → 6.0/7.0), key3→`mv3`
  (`+0x2C=9,+0x30=8,+0x34=1.0` → 9.0/8.0); `nomap` plants null root.
- `dwtab`/`devrmp`: identity codepoint→index vector (dev1+8).
- `gnode`: inline glyph-map node key 3 → value at `+0x24`.
- `st7c0`: `17F7C0` source state — `d[+0x9C]` metric idx (`vidx`),
  float stream `+0x00..`, vertex stream `+0x2C+k*4`, dword streams
  `+0x5C/6C/7C`, `d[+0x8C]=64` scale source; `dslot`/`b2349`/`vcap`/
  `vfill` case keys.
- Scripted VAs `0x7000A100`/`0x7000A108` (`salloc`/`sdealloc`) and
  `s19c5d0`/`s1c5f20` — the allocator and lazy-init boundaries.

## New cases (11)

`e8070-append` (vector append ×6, bounds, post-loop `+0x2344=0.5`,
scale-quad reset), `e8070-grow` (3× realloc through scripted
alloc/dealloc), `e8070-flag` (`b2349` arm writes `+0x2340/44`, clears),
`e8070-neg` (`vidx=−1` → default record `dev+0x1358`, `e94e0` skipped),
`f880-miss` (map miss → 23.0 const, flag arm skipped), `f920-arm0/1`
(`d[+0x20]=6` / `d[+0x1C]=5` select via `f49e0`/`fddc0`),
`f9c0-scale` (`ceilf(4/1.0)=4.0`), `f8c0-hit` (codepoint 3 → inline-map
hit → `gnode+0x24`), `f940-get` (`eax=0x1234`), `fae0-set`
(`q[dev1+0x28]=0x77`).

## Remaining scripted boundaries (unchanged class)

`181560` + six `181xxx` device wrappers (`q[0x1F811E8]` render-device
object still unplanted), `19C5D0`/`1C5F20` (`1E94E0`'s flag-0 init
path — planted flag avoids it), allocator vtable fns, `2AC2F0`
decoder, sibling `17Fxxx` thunks `17F850`/`17FA10`/`17FB00`/`17FD30`,
`3FFDF0`, `254A10`, `861EC0` memset hook.

## Next candidates (EXP-221+)

- The `181xxx`/`1Bxxxx` render-device subtree — needs a planted
  `q[0x1F811E8]` device object (`+0x3930` write region, method vtable).
- `1E94E0`'s flag-0 arm — plant a record with flag 0 to force the real
  `19C5D0`/`1C5F20` lazy-init chain.
- Sibling thunks `17F850`/`17FA10`/`17FB00`/`17FD30` — same
  `1B5FB0`→method pattern, bounded leaves.
- `2AC2F0` decoder — the remaining scripted interpreter boundary.
- `2A9F00`'s glyph-loop gate — the only path that reaches `17F7C0`
  naturally; currently only direct-entry covers `1E8070`.
