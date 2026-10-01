---
id: EXP-162
title: "Object detach chain 238BF0 — 301140's scripted 235i callee promoted to real"
status: executed
evidence: NATIVE-REPLAY
exe_sha256: 73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8
harness: exp162_check.py
result: 126/126 (stable x3)
---

# EXP-162 — `238BF0` object detach/param-normalize, executed

`00238BF0` (235 insns, 27 call sites) is the cleanup chain `301140`
invokes between the `311F70` helper and the `3105D0` unlink. It was
the last scripted callee on the despawn path's mainline; it now runs
real end-to-end, taking the whole EXP-150..161 corpus underneath it.

## `238BF0(rec)` — executed semantics

- Guards: `rcx==0` → ret; `q[rec+0x10]==0` → bail at `0x238F76`
  (no work); `q[rec+0x698]==0` → skip to tail.
- Mode byte `b[objrow+5]`:
  - `==0` (foe/other): `q[rec+0xE60]` equip/steal-table ptr →
    `w[e60+0x7A]` → `cvtdq2ps`/`divss` normalize vs rodata const.
    Class byte `b[objrow+4]`: `(al-0x1B) <= 0xC` →
    `269F30(obj, 3, 8)`, else `269F30(obj, 2, 1)` — the object
    mode setter.
  - `==1` (member): `q[rec+0xE68]` member sheet → `w[e68+0x10]`
    float; `q[rec+0xE60]`; `q[rec+0x6A0]` flag byte — bit `0x20`
    → `267CC0`+`26B4A0(obj,0xA)`; else `b[rec+0x58]` dispatch
    (`4`→write `1`; `1`→`2659A0`+`25D5E0(obj,0xA)`).
- Shared detach sequence on `q[rec+0x10]` (all real):
  `269FE0`, `2E5FD0`, `26DAC0`, `2EC5B0`, `26A430`, `26A3A0`,
  `2E8220`, `269F20`, `2E8A10`, `26AD00`, `2361B0`, `26A7F0`,
  `26A7C0`, `269E20`, `236210` (member-gated: `b[objrow+5]==1` +
  `b[e68+0x18]` bits `0x10/0x20/0x40` select → `cl&0xA` →
  `3204D0(rec,6,&out)`), `26A330(obj, float)`, tail
  `312700(rec)` — 246i conditional dispatcher, scripted boundary.
- Also real inside the chain: `2E9780`, `26D6F0` (under `26A330`),
  `3204D0` subtree, `30A130`/`265090`, `312DF0`, `26B6A0`,
  `3587C0`, `2EB930`, `2E5C70`/`2E5C90`, `2E4A10`, `2646C0`,
  the `3DBxxx`/`26xxxx` leaf families.

## Proven

- `v8bf0-foe` (b5=0, b4=0): full chain — 18 real callee tags +
  `m312700` scripted call, ret 0, 0 faults.
- `v8bf0-memb` (b5=1): member path — `e68`/`6A0` reads, `236210`
  member arm, same shared tail.
- `v8bf0-cls1b` (b4=0x1B): class-byte arm → `269F30(obj,3,8)`.
- `v8bf0-noobj` (`q[rec+0x10]`=0): bail, zero trace.
- `u1140-base`/`noflg`/`eng` re-proven with `238BF0` real inside
  `301140` — the despawn path now executes its cleanup natively.

## Fixture disclosures (planted)

- `q[rec+0xE60]` / `q[rec+0xE68]` — equip-table / member-sheet
  blocks (0x400 each).
- `q[rec+0x6A0]` — flag byte (`0x20` arm selectable).
- `b[objrow+4]` class byte, `b[objrow+5]` mode byte.
- Prior EXP-161 fixture: `+0x698` bidirectional link, `q[rec+0x10]`
  object, `q[0x209BE80]` object registry, `q[0x2EBF190]` state cell.
- Scripted boundary: `312700` (246i dispatcher) — the only scripted
  callee left on `301140`'s mainline besides `311F70`, `3299B0`,
  `0x3B02A0` (async wait), `290DF0` (safety).

NATIVE-REPLAY only — no initialized-gameplay reachability claimed.
