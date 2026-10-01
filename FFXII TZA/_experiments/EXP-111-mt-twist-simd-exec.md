---
experiment: EXP-111
title: MT19937 twist SIMD arm — shipped twist 00866B90 under both feature-gate values vs an independent reference
contract: ../08-Combat-Formula/CONTRACT-preparation-step-family.md
method: B
live_game: false
tool: evidence/mt-twist-simd-exec/check.py
---
# EXP-111 — mt-twist-simd-exec

**Status:** complete · **8/8 state cases, 20/20 mutants, stable across
three processes**
**Evidence:** `evidence/mt-twist-simd-exec/` (`check.py`, `bodies.json`,
`gen_bodies.py`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

`CONTRACT-prep-step-simd` carried one bounded unexecuted residual: the
SIMD arm of the shipped MT19937 twist at `00866B90`, gated on feature
dword `d[0x01F44858] >= 2` (the shipped value is `1`, so the shipped
path is scalar). This experiment executes the real shipped body under
Unicorn with the flag planted at `1` (scalar arm) and `2` (SIMD arm)
and diffs the complete 624-word output state and the MT index against
an independent Python MT19937 twist reference.

| VA | role | execution |
|---|---|---|
| `00866B90` | TWIST — MT19937 twist, SIMD prefix + scalar tail | **real** (463 B, 98 insns) |

Self-contained leaf — no calls, no scripted boundaries.

## Measured semantics (native execution, not static reading)

```
if d[0x01F44858] >= 2:                       ; feature gate (shipped = 1)
    ecx = 0xE0 ; SIMD arm: elements 0..223 in 28 passes of 4 lanes,
               ; advancing rax +0x20 per pass (two 4-lane groups)
    xmm3 = [0x01CCFE00] = 0x80000001 x4      ; hi mask + don't-care bit0
    xmm4 = [0x01CCFDF0] = 0x7FFFFFFE x4      ; lo mask (bit0 already 0)
    xmm5 = [0x01CCFE10] = 0x9908B0DF x4      ; twist multiplier
    xmm7 = [0x01CEBCD0] = 0x00000001 x4      ; odd-bit pick
    per lane: y = (s[i]&xmm3) | (s[i+1]&xmm4)
              s[i] = s[i+397] ^ (y>>1) ^ (magic * (s[i+1]&1))
scalar loop (always runs; SIMD leaves ecx = 0xE0):
    elements ecx..623: s[i] = s[i+397 wrap] ^ (((s[i]&0x80000000)|
                            (s[i+1]&0x7FFFFFFF)) >> 1) ^
                            (0x9908B0DF * (s[i+1]&1))
    wraparound for i+397 >= 624 reads back over the state base
d[0x02EB4230] = 0                            ; MT index reset (mti)
```

State base `0x02EB3870`; the `+0x634` byte offset = `+397` words —
standard MT19937 twist distance. The scalar arm is entered at whatever
`ecx` the SIMD arm leaves (`0xE0` when SIMD ran, `0` otherwise), so
scalar always covers elements `ecx..623` plus the final wraparound
tail — the SIMD arm is a **prefix accelerator**, not a replacement.

## Execution findings (beyond the contract's static reading)

1. **SIMD and scalar arms produce byte-identical state** — all eight
   planted 624-word states (zeros, ones, incremental, PRNG-random,
   lsb-alternating, high-bit-only, mixed edge, standard seed 5489)
   come out bit-exact under both flag values, and both match the
   independent reference. The SIMD arm is a pure optimization with no
   observable semantic difference — correct vectorization confirmed
   by execution, not assumed.
2. **The two SIMD masks encode differently than the scalar form but
   are equivalent** — SIMD uses `0x80000001`/`0x7FFFFFFE` where scalar
   uses `0x80000000`/`0x7FFFFFFF` (via `(x^y)&0x7FFFFFFE` + `^s[i]`).
   The differing bit0 lanes are shifted out by `psrld 1`/`shr 1` —
   dead by construction. Proven: patching the scalar mask bit0
   (`m-sc1-mask`) produces identical output.
3. **The feature gate is a prefix switch, not an arm switch** — with
   the gate flipped (`jl`→`jge` at `0x866B9E`, `m-gate`), flag=1 runs
   the SIMD prefix AND the scalar tail and still lands byte-identical.
   The gate is only observable through the SIMD arm's xmm6/xmm7
   callee-saves (`movaps [rsp]`, `[rsp+0x10]`) — planted as a canary.
4. **`mti` reset is unconditional** — `d[0x02EB4230] = 0` on both
   arms, verified against a `0xDEADBEEF` sentinel.

## Mutation campaign

20 byte-precise mutations across the gate, SIMD arm, scalar arm, and
tail — gate direction, SIMD element count and mask consts
(`0x80000001` sign lane), src/dst disp32 (`-0x634`/`-0x630`),
`rax +0x20` advance, scalar `0x7FFFFFFE` mask, `0x9908B0DF`
multiplier (two sites), `+0x634` M-word disp (two sites), `&1` odd
pick, `shr` target register, loop bound JCCs, tail s[0] read, tail
multiplier, `mti` store immediate. **20/20 killed.**

Three initial findings were equivalent-encoding or harness gaps:

- `m-simd-hi` patched mask byte0 (`0x80000001`→`0x80000000`) — bit0
  is shifted out; equivalent. Repointed to the sign lane
  (`0x80`→`0x00` at `0x1CCFE03`), which is live.
- `m-sc1-mask` bit0 — same don't-care-by-shift equivalence. Repointed
  to bit1 (`0xFE`→`0xFC`), live.
- `m-gate` on flag=1 — output-equivalent by construction (both arms
  produce identical state). Killed via the SIMD arm's xmm6/xmm7
  `movaps` callee-saves on the stack, observed with planted register
  values.
- Scalar baseline needed `count >= ~7900` insns (initial `count=8000`
  truncated the tail; raised to 20000). The earlier "scalar!=simd at
  elements 570–623" and the surviving tail mutants were all this
  truncation artifact.

## Limitations

- The fixture plants `d[0x01F44858]` directly; what sets it in the
  live game (CPU feature detection) is outside this package — the
  contract's question was only whether the two arms agree.
- Eight state shapes cover zeros/ones/ramp/random/bit-structured
  cases; exhaustive state-space coverage is not claimed — the
  differential (native vs reference) is per-twist, not per-sequence.
- `bodies.json` holds the body span + sha256 over shipped bytes;
  coverage is instruction-start ratio, same convention as
  EXP-107–110.
