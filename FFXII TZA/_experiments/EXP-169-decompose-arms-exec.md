---
id: EXP-169
title: "265390 kind-dispatch arms + 0x4125 accept — remaining decompose arms and a real 0x4125 spawn accept"
status: executed
evidence: NATIVE-REPLAY
exe_sha256: 73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8
harness: exp166_check.py
result: 153/153 (stable x3)
---

# EXP-169 — 265390 arms + 0x4125 accept, executed

Continues EXP-168: exercises the three `265390`
kind-dispatch arms behind opcode `0x414E`, and drives
`0x4125` to a real accepted spawn using the EXP-166
commit fixture extended to all 64 cells (`erowall`).

## `265390(row, &x, &y, &z)` — full dispatch decoded + executed

`r10d = b[row+3] >> 5`, then `r10d - 1`:

- **kind 1** (`b3&0xE0==0x20`, `t2730-414e-k1`) —
  `0x26542D`: node `q[row+0xB8]` → outs =
  `{d[node+0x10], d[node+0x14], d[node+0x18]}`.
  Observed `{21.0, 22.0, 23.0}` → out quad.
- **kind 3** (`b3&0xE0==0x60`, `t2730-414e`) —
  `0x2653B7`: node `q[row+0xB8]` → outs =
  `{d[node+0], f[node+4]+adds, d[node+8]}`.
  - Optional `q[row+0xC0]` object: non-null adds
    `f[c0+0x140] + f[c0+0x144]` into the **y** out.
  - `b[node+0x107] & 1` adds `{f[node+0x40],
    f[node+0x44], f[node+0x48]}` to all three outs.
  - `t2730-414e-k3o` proves both adds:
    `{11,12,13} + {0.5,1.5,2.5} + (y)1.0` =
    `{11.5, 14.5, 15.5}` — `0x41380000`/`0x41680000`/
    `0x41780000` observed.
- **default** (`t2730-414e-k0`, `b3==0`) — zeroes all
  three outs, ret. Observed all-zero quad.

The `0x414E` arm then copies out1 → out2 and writes
`d[outf] = 0` itself.

## `0x4125` accept — `t2730-4125a` (eax=1)

- `312DF0(rec+0xD0, edx=-1, r8d=0x14)` — seed planted
  `(16, 5, 16)` via `rec_d`.
- 7 real iterations of `328370` RNG jitter
  `±(rand % 0x29) - 0x14`; iteration 7's candidate
  passed the full chain: `3377C0` → `337700` →
  `391410` → `383F10` → **`382D10` winding accept ×1**
  → `336390` 5-point footprint (`z32a6a0`×5, `z231400`×5,
  `z233050`/`z233110`/`z230a40`/`z2324f0`/`z22f830`×5,
  `z22f8b0`×10) → ret 0 = found.
- `out1` = accepted candidate `(7, 5, 15)` —
  jitter `(-9, 0, -1)` off the seed, deterministic rand.
- `outf = 0x40800000` = 4.0 — the dispatcher's `xmm6`
  scale seed flows through `265090` kind-3
  (`f[node+0x50]`) → `maxss` → outf write.
- `t31abe0` ×7 — the validator consults the member
  resolver each iteration.
- Reject path (`t2730-4125`, empty links) retains
  eax=0 with all 9 iterations real — accept/reject
  distinction proven on the same arm.

## Fixture additions

- `erowall` — `ridx` spans `{0,1}` for all 64 cells
  (jittered candidates land anywhere in the grid).
- `onodeoff` — `b[node+0x107]=1` + `f[node+0x40..0x48]`.
- `orowc0` — `q[row+0xC0]` object `{f+0x140, f+0x144}`.
- `nodey` (pre-existing) drives `f[node+0x50]` → xmm6.

## Disclosures

- All planted rows/nodes/objects are disclosed fixtures —
  NATIVE-REPLAY, not initialized-gameplay reachability.
- `rand` remains the deterministic host stub; candidate
  positions are fixture-dependent, mechanics are real.
- `zverts`/`erowall` are permissive (whole-grid triangle,
  every cell mapped to row 0) to make accept reachable —
  they exercise, not replace, the native predicates.
