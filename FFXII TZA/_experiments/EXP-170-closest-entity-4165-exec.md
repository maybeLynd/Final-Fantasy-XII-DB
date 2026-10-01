---
id: EXP-170
title: "312730 opcode 0x4165 — 319850 closest-entity scan with real 2FB310/3A1960, accept and reject"
status: executed
evidence: NATIVE-REPLAY
exe_sha256: 73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8
harness: exp166_check.py
result: 155/155 (stable x3)
---

# EXP-170 — opcode 0x4165 closest-entity scan, executed

The last unexercised `312730` dispatch arm. `0x4165` calls
`319850(rec, out1)` — a closest-entity search — then copies
the result quad and writes `xmm6 + C − 0.1` to `outf`.

## `319850(rec, out)` — decoded + executed

- `rbx = q[0x2EC1360]` — entity list head (`.data`, runtime).
  Null list → `edi = -1` → arm rejects (`js 0x312ad4`).
- `xmm6 = f[0x2F973B8]` — best-distance seed, a
  runtime-initialized global (0 in the image; fixture plants
  FLT_MAX — two more RIP-relative off-by-ones corrected:
  cell `0x2EC1360` was earlier computed `0x3C92E60`, and the
  `2FB310` table is `0x22BE7F0` not `0x4BE47F0`).
- Loop per node `{d+0 id, q+0x18 next}`:
  - **`2FB310(id, &quad)`** — static position table
    `0x22BE7F0 + id*0x20`: `b[+0]` occupied flag →
    quad at `+0x10`; ret 1/0.
  - **`3A1960(rec+0xE0, quad)`** — squared XZ distance
    `(dx² + dz²)`.
  - `comiss best, dist` — strictly-closer wins
    (`jbe` skips); winner copies the quad to `out1`
    and sets `edi = id`.
- ret `edi` = winning id or −1.
- Security cookie (`q[0x1D40830]`) checked via
  `808c40` — passes (unchanged global).

## Epilogue

`xmm6` (the dispatcher's `265090` scale seed)
`+ f[0x1CEBBA7]` (denormal-looking bytes, ~0)
`− f[0x8C5F6C]` = **0.1f** → `d[outf]`. Observed
`0x3F666666` = 0.9 with `xmm6 ≈ 1.0`.

## Executed findings

- `t2730-4165` (reject): shipped-image null list →
  `319850` ret −1 → `eax=0`. `t2fb310` correctly absent.
- `t2730-4165a` (accept): 2-node list, both `b[+0]=1`,
  positions `(1,2,3)` and `(30,2,30)`; `rec+0xE0` planted
  `(1.5, 2, 2.5)` → entry 0 closest → `out1`/`out2` =
  `{1.0, 2.0, 3.0, w}` — **`w` lane is 0xCDCDCDCD**:
  `319850` repacks only x/y/z into its stack quad
  (`+0x20/+0x24/+0x28`); `+0x2C` stays uninitialized
  stack and flows to the outputs. Authentic shipped
  behavior — the opcode output quad's w lane is garbage.
- `outf = 0.9` — proves `xmm6` path: `265090` kind-1
  seed (~1.0) + ~0 − 0.1.

## Disclosures

- `poslist` fixture: planted list nodes + table flags —
  NATIVE-REPLAY, not initialized-gameplay reachability.
- `f[0x2F973B8]` is a runtime global planted as FLT_MAX;
  shipped init value inferred, not read.
- `f[0x1CEBBA7]` reads what may be tail bytes of another
  datum — executed as-is from the shipped image.
