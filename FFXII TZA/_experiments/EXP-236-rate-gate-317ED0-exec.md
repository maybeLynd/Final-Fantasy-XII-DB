# EXP-236 — broadcast-rate gate `317ED0` real, `28EFxx` flag sinks boundary

**Status:** complete — **542/542 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 `ff72b856` prefix; 542
cases), fault census unchanged at 20** (the same pre-existing
intentional-null fixtures).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..235; no new cases — the `s7ed0` scripted sink now
executes the shipped body; `28EF70`/`28EF00` declared as `v`-
boundaries; asserts retargeted to real tags + boundary pins).
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Body promoted real this round

`00317ED0` (`l317ed0`, ×1) — the broadcast-rate throttle `312280`
calls at `0x3122CD` on each share-tick when both the source row
(`q[rdx+0x698]` rec, `b[rec+5]==1`) and the peer (`rcx` non-null,
`b[rcx+5]==0`) qualify. Only `d228-gaterc` carries a peer row —
all other d228 cases gate off in the caller before `0x3122CD`:

```text
if rcx == 0:                    ret
rec = q[rcx+0x698];  if !rec or b[rec+5] != 1:      -> tail 0x3180D6
e68 = q[rcx+0xE68];  if b[e68+0x28] & 2:            -> tail
if d[0x22C3168] < 0:                                -> shared tail
if b[rcx+0x56] == d[0x22C3168]:          ; epoch A in sync
    if 229E40() != 0:                   ; lang dword d[0x1E02814]
        d[0x22C315C] = clamp(d[0x22C315C]+1, 0, 0x3E6)
    else:
        d[0x22C315C] = clamp(d[0x22C315C]+1, 0, 0x3E7)
    d[0x22C3164] = 0
else:                                                ; 0x31806C arm
    229E40(); 28EF00(d[0x22C3160]+ret?, d[0x22C3164])  ; v-boundary
    d[0x22C3160] = 0;  d[0x22C3164] = clamp(+1, 0x3E7) ; resync
if w[e68+0x40] == d[0x22C316C]:          ; epoch B in sync
    d[0x22C3160] = clamp(d[0x22C3160]+1, 0, 0x3E7)
else:
    d[0x22C3160] = 0;  d[0x22C316C] = w[e68+0x40]      ; resync
3183D0()                                   ; LCG tick (2-step MSVC rand)
r8 = LCG%100;  bl = r8>=0x28 if b[0x22C3178]&1 else r8<5
28EF70(d[0x22C315C]+(229E40()?1:0), bl, d[0x22C3158])  ; v-boundary
shared tail:  d[0x22C3178] = (d[0x22C3178]&~1)|bl;
              d[0x22C3168] = b[rcx+0x56]
```

## The disclosed `28EFxx` boundaries

`0028EF70` (`v28ef70`, ×1) is called **unconditionally** on the
in-sync arm — the flag write into `q[0x209BE80]`-based structures is
what actually pushes the rate state out. `0028EF00` (`v28ef00`, ×0)
is the epoch-mismatch-arm counterpart. Both deref `q[0x209BE80]`
(BSS-null shipped, `fbdev`-keyed) without a guard — the first attempt
to run the body real faulted at `0x28EF13` on `d[rax+0x7C7C]`. Both
stay scripted until an fbdev-class fixture exists; each has exactly
one direct caller (inside `317ED0`), so the interception is
exactly scoped.

`00229E40` — the `d[0x1E02814]` lang-dword getter — was already real
since EXP-209; the harness plants `e2814v`=0 (the shipped `.data`
bytes `0xD3F521D0` are stale pre-init garbage). It now fires **twice**
per pass (`0x317F2D` epoch-arm poll + `0x31804B` post-LCG poll).

## Case and pins

`d228-gaterc` (`c228(rcx="row2")`) is the only case reaching the
body — `objlink` plants `q[obj+0x698]` rec (`b[rec+5]`=1 via the
`c228` default) and `q[obj+0xE68]` e68; `b[obj+0x56]`=0 ==
`d[0x22C3168]`=0 and `w[e68+0x40]`=0 == `d[0x22C316C]`=0 keep both
epoch arms on the in-sync path:

- `byr("l317ed0")` ×1, `rcx == obj` (the `rdx` member row).
- `byr("l229e40")` ×2 on the case (57 pre-existing elsewhere → ×59
  census).
- `d[0x22C315C]` == 1, `d[0x22C3160]` == 1 — the real clamped
  counter increments.
- `by("v28ef70")` ×1 with `(rcx=1, rdx=0, r8=0)` — `ecx` =
  `d[0x22C315C]` post-write (`e2814v`=0 → no `inc`), `edx` = `bl` =
  0 (LCG%100 ≥ 5 under shipped-zero RNG state), `r8d` =
  `d[0x22C3158]` = 0.
- `v28ef00` ×0 — epoch-mismatch arm disclosed, unreached.
- Tail writes: `d[0x22C3178]` &= ~1 (bl=0), `d[0x22C3168]` = 0 —
  no observable change under zeroed cells.

## Regression arc

First real attempt faulted inside `28EF00` at `0x28EF13`
(`d[rax+0x7C7C]`, rax = BSS-null `q[0x209BE80]`) — the earlier note
that "deep 28EFxx arms stay gated" was wrong: `28EF70` is
**unconditional** on the in-sync path, reached after the LCG tick.
Declared `v28ef00`/`v28ef70` boundaries instead of growing an
fbdev fixture this round; one arg-pin correction (`ecx` 2 → 1:
`e2814v`=0 suppresses the `inc`). Final: **542/542**, zero
remaining regressions, no assertion weakened.

## Boundaries (unchanged disclosures)

`30E130` (`e130` ×0), `290B90` (`s290b90` ×34), `317E50` (`b7e50`
×0), `20CE60` (`v20ce60` ×0), `427320` (`v427320` ×1), `422C20`
(`v422c20` ×1), `3377C0` (`v3377c0` ×19), `28EF70`/`28EF00`
(new — ×1/×0), `3180F0`, `319CA0` (pos tail chain), `46AB10`,
`426130` remain scripted. `live_game: false`.
