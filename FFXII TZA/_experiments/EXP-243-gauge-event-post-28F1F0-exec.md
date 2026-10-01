# EXP-243 — gauge-event post `28F1F0` real

**Status:** complete — **542/542 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 `0e1b4ed7` prefix; 542
cases), fault census unchanged at 20** (the same pre-existing
intentional-null fixtures).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn; no new fixture was needed — the path runs on
shipped-BSS-zero state; none claim initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..242; asserts retargeted, none weakened).
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Bodies promoted real this round

- **`0028F1F0`** (`l28f1f0`, ×7 — `q28f1f0` stub removed) — the
  gauge/event post called by the `30F340`/`2ACE00`-family stat paths:

```text
edi=r9d esi=r8d ebp=edx ebx=ecx        ; (channel id, a, b, flags)
rax = 296280(ecx)                      ; channel-table id scan
if !rax:
    rax = 2962C0()                     ; static default slot 0x209C240
    if d[rax+0xB0] == 0 || != ebx: ret ; default-slot id gate
rsp pair = {edx, r8d}                  ; event payload
rcx = rax (+0x58 if edi != 0)
call 3F8980(rcx, &pair)                ; post sink
```

- **`00296280`** (`l296280`, ×24) — scans the four-entry channel
  table `0x209BF66..0x209C2BE` (0xC0 stride): an entry participates
  only when `b[e-0x58]&2` or `b[e]&2`, then `d[e+0x32]==ecx` returns
  `e-0x7E`. **The whole region is BSS** — `.data` raw ends at RVA
  `0x1E5E400` (canonical `0x1F7E400`); `0x209BF66` is virtual-only,
  shipped-zero — so no entry's flag bits are set, the compare never
  runs, and the scan always returns 0. 17 of the 24 calls are
  pre-existing silent-real callers surfaced by REAL-listing (arg
  recording only — no behavior change); 7 come via `28F1F0`.

- **`002962C0`** (`l2962c0`, ×7) — `ret 0x209C240`, the static
  default channel slot (also BSS-zero shipped).

- **`003F8980`** (`l3f8980`, ×0 — REAL-listed so a future fixture
  surfaces it with args) — the post sink: `q[obj+0x38]` handler,
  `call rax(obj, 1, pair)` when set, else `w[obj+0x26] &= ~1`.

## Path taken under shipped-zero state

All 7 callers pass `ecx=0`. Real execution: `296280(0)` → 0 (flag
bits all clear — the `d[+0x32]` compare is gated behind them, so
even `ecx==0` never matches) → `2962C0` → `d[0x209C2F0]`==0 →
early-out at `0x28F24B`; `3F8980` is not called. Observably
identical to the old stub, but the scan, fallback and gate now run
shipped bytes — a fixture that plants `b[e]&2` + `d[e+0x32]` in the
table, or `d[0x209C2F0]` in the default slot, exercises the real
post arm instead of unmapped code.

## Retargets

`ce0-basic`'s `by("q28f1f0")` → `byr("l28f1f0")` (the lone scripted-
call assert for this tag; the other six callers record through
`rargs`/`calls` already). No `_ret` plants existed. Fault census
unchanged at 20.

## Boundaries (unchanged disclosures)

`30E130` (`e130` ×0), `317E50` (`b7e50` ×0), `20CE60` (`v20ce60`
×0), `427320`/`422C20` (×1 each), `3377C0` (`v3377c0` ×19),
`2E8FD0` (`v2e8fd0` ×1), `28F0C0`'s `ecx==0` `273A20`/`244F00` tail,
`3B02A0`, `46AB10`, `210EC0`, `1CCB20`, `3180F0`, `319CA0`,
`426130`, `238BF0` (×7 — 0x400-byte unlink carrier, scoped and
deferred) remain scripted or unexplored. `live_game: false`.
