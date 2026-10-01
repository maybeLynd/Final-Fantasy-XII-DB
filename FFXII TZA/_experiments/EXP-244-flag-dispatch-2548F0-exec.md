# EXP-244 — flag-dispatch `2548F0` real

**Status:** complete — **542/542 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 `16c6d974` prefix; 542
cases), fault census unchanged at 20** (the same pre-existing
intentional-null fixtures).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn; no new fixture — the target cell is shipped
BSS; none claim initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..243; asserts retargeted and extended, none
weakened).
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Bodies promoted real this round

- **`002548F0`** (`l2548f0`, ×4 — `b48f0` stub removed) — a
  flag→bit-op dispatcher on the `u0fc0` teardown path:

```text
rbx = ecx ? 2E1C20 : 2E1CA0        ; set vs clear leaf
rbx(ecx=8, edx=8)                  ; slot 8, bit 8
rbx(ecx=8, edx=9)                  ; slot 8, bit 9
rbx(ecx=8, edx=0xB)                ; slot 8, bit 0xB
jmp rbx(ecx=8, edx=6)              ; slot 8, bit 6 (tail)
```

- **`002E1C20`** (`l2e1c20`, ×16) — `if ecx<0x10:
  d[0x215F1C0+ecx*4] |= (1<<edx)`.
- **`002E1CA0`** (`l2e1ca0`, ×0) — the clear twin
  (`&= ~(1<<edx)`); every harness caller passes `ecx=1`, so only
  the set arm runs — disclosed.

## Shipped-value pin

The slot-8 cell `d[0x215F1E0]` is **BSS** (`.data` raw ends at
canonical `0x1F7E400` — every caller starts from 0). All four
`u0fc0` callers (`def`, `m1`, `mtail`, `caps`) pass `ecx=1`, so the
real set arm leaves `d[0x215F1E0] == 0xB40` (bits 6|8|9|0xB) —
pinned on `u0fc0-def`. A fixture path calling with `ecx=0` would
now exercise the real `2E1CA0` clear arm.

## Sibling stubs triaged and deferred this round

- `bc140`/`36C140` (×3) — deferred-call-stack pop: **`jmp $`
  infinite loop when `d[0x22D89C0] ≤ 0`** — the stub is load-
  bearing on empty-state callers; promotion needs a count>0 record
  fixture and is deferred.
- `bc1d0`/`36C1D0` (×3) — reads its caller's return-address bytes
  (`q[rsp]` family) to dispatch; stack-layout-sensitive, deferred.
- `b040`/`23B040` (×3) — 0x1C0-byte body over `303EC0`/`313F60`/
  `3272A0` + `b[0x2089340]&0x40` epoch gate; medium, deferred.
- `d8bf0`/`238BF0` (×7) — 0x400-byte unlink carrier; deferred.

## Retargets

`by("b48f0")` → `byr("l2548f0")` on `u0fc0-def` and the `u0fc0-s800`
negative pin (`0x100` arm not fired there — flag differs). No
`_ret` plants existed. Fault census unchanged at 20.

## Boundaries (unchanged disclosures)

`30E130` (`e130` ×0), `317E50` (`b7e50` ×0), `20CE60`, `427320`/
`422C20` (×1 each), `3377C0` (`v3377c0` ×19), `2E8FD0` (`v2e8fd0`
×1), `3B02A0`, `46AB10`, `210EC0`, `1CCB20`, `3180F0`, `319CA0`,
`426130`, `238BF0`, `23B040`, `36C140`, `36C1D0` remain scripted.
`live_game: false`.
