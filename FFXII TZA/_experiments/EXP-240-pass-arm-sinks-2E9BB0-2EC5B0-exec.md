# EXP-240 — `26D6F0`/`2EBB80` pass arms exercised; sinks `2E9BB0`/`2EC5B0` real

**Status:** complete — **542/542 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 `0fcf1ce5` prefix; 542
cases), fault census unchanged at 20** (the same pre-existing
intentional-null fixtures).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..239; `u0fc0-m1`/`l01140-bbb1` gained disclosed
pass-arm fixtures; asserts extended, none weakened).
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Why this round

EXP-237/239 promoted the `b[+3]&0xE0==0x60` gate family but every call
ran the gate-fail early-out — the pass arms had never executed. This
round plants the gate honestly on one case per caller family and
promotes the two sinks the arms reach.

## Bodies promoted real this round

`002E9BB0` (`l2e9bb0`, ×1) — flag-target getter:

```text
n = q[rcx+0xC0];  if !n:                    ret 0
t = q[n+0x138];   if !t:                    ret 0
ret d[t+0x110]
```

`002EC5B0` (`l2ec5b0`, ×1) — the matching setter:
`d[q[q[rcx+0xC0]+0x138]+0x110] = edx`, same null-guards. Both are
null-guarded leaves; under the new fixture both execute their
read/write arm rather than the null early-out.

## New fixtures (disclosed)

- **`desc8`** — `q[ent+0xB8]` desc buffer (0x100) with
  `q[desc+0xF0]` → fresh float cell (0x40); optional `d:`/`f:` fields.
  `26D6F0`'s pass arm writes `f[q[desc+0xF0]+0x24]` and `f[desc+0xD0]`.
- **`objc0q`** — `{off: size}` wires `q[objc0+off]` to a fresh zeroed
  buffer; `objc0` alloc widened 0x80→0x200 for the `+0x138` slot.
- `u0fc0-m1` plants `ent_b={3:0x60}` + `desc8` + `objc0` +
  `objc0q={0x138:0x140}`; `l01140-bbb1` plants `ent_b={3:0x60}` +
  `objc0` (node only — `2E8FD0` stays scripted).

## What the pass arms actually did (shipped bytes)

`u0fc0-m1` — `26D6F0` pass arm end to end:

- `f[q[desc+0xF0]+0x24] = xmm6` (param 0.0 — caller-supplied, mode
  `esi=r8d`≠1 so the `b[ent+0xC]|=0x10` arm is correctly skipped),
  `f[desc+0xD0] = xmm6`.
- `q[ent+0xC0]` node → `q[node+0x138]` flag target →
  `f[tgt+0x30+0x98] = c1·c2·c3·xmm6` (three `.data` float constants).
- `l2e9bb0(ent)` → `d[tgt+0x110]` = 0 → `ebx = 0 & ~4 = 0`;
  `b[ent+0x12]`=0 ≤3 → `xmm6==0.0` → `ebx |= 4`.
- `l2ec5b0(ent, 4)` → `d[tgt+0x110] = 4` — **pinned**.
- `2E9780`'s pass arm also ran: `b[node+0x11]>>6&1` on the zeroed
  node → ret 0 (unchanged result, new authority).

`l01140-bbb1` — `2EBB80` pass arm: gate passes, `q[ent+0xC0]` node
live → `b[node+0x10] = (0&0xF7)|((1&1)<<3) = 8` — **pinned** —
then `jmp 2E8FD0` → `v2e8fd0(ent, edx=8, r8=0, r9=1)` records the
folded `dl` — **pinned**.

## Boundary status

`2E8FD0` stays scripted (`v2e8fd0` ×1, now with real recorded args
instead of ×0) — its `q[+0xC0]` second-level walk into
`3E6A60`/`2E8CE0`/`2EE190`/`2E8AC0`/`2E8A70` needs a populated node
subtree; the boundary record proves the real fold ran first.

## Shipped-value pins

`u0fc0-m1`: `l2e9bb0` ×1 (rcx==ent); `l2ec5b0` ×1 (rcx==ent, edx==4);
`d[tgt+0x110]==4`; float-write cells read back 0.0 (param-driven —
the write *path* is proven by the d110 pin). `l01140-bbb1`:
`b[node+0x10]==8`; `v2e8fd0` args pinned.

## Corrections of record

Fixture additions only — no assert weakened; `u0fc0-m1`'s four
pre-existing asserts all still hold under the pass arm (the upstream
`300FC0` path is insensitive to `b[ent+3]`). Zero regression
failures — **542/542 on the run carrying the new pins**. Census:
`l2e9bb0` ×1, `l2ec5b0` ×1, `v2e8fd0` ×1, stale `b9bb0`/`bc5b0` ×0.

## Boundaries (unchanged disclosures)

`30E130` (`e130` ×0), `290B90` (`s290b90` ×34), `317E50` (`b7e50`
×0), `20CE60` (`v20ce60` ×0), `427320` (`v427320` ×1), `422C20`
(`v422c20` ×1), `3377C0` (`v3377c0` ×19), `28EF70`/`28EF00`
(×1/×0), `2E8FD0` (`v2e8fd0` ×1), `3B02A0`, `46AB10`, `210EC0`,
`1CCB20`, `3180F0`, `319CA0`, `426130` remain scripted.
`live_game: false`.
