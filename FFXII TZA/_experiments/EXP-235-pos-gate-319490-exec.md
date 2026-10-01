# EXP-235 — position gate `319490` real, `3377C0` broadcast boundary

**Status:** complete — **542/542 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 `6a1b9b14` prefix; 542
cases), fault census unchanged at 20** (the same pre-existing
intentional-null fixtures).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..234; no new cases — the `s9490` scripted sink now
executes the shipped body; `ctx4` fixture gained `n30` node wiring;
asserts retargeted to real tags + `v3377c0` boundary pins).
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Body promoted real this round

`00319490` (`l319490`, ×19) — the position broadcast gate every
`312280` run calls once at `0x31258D` (its only image caller) with
the `265020`-built position triple:

```text
rbx = rcx                         ; &vec3
eax = 3590D0()                    ; d[0x22C7FE0] — ctx id cell
if b[0x2089340] & 0x10:           ; ctx-resolution enable flag
    ctx = 3588B0(eax)             ; cls=(id>>16)&0xF -> 263FF0 table
    if ctx:                       ; idx=cx bounded, gen=w[+0x16]==(id>>20)&0x7FF
        node = 263E30(ctx)        ; q[ctx+0x30]
        if node and b[node]&8:    ; keep node
        else:                     ; ctx = 0
    else:                         ; ctx = 0
else:                             ; ctx = 0
vec4 = {f[rbx], f[rbx+4], f[rbx+8], 1.0f}   ; w = literal 0x1CEBBA8
eax = 3377C0(ctx, &vec4)          ; scripted boundary
return eax
```

All four ctx-resolution callees (`3590D0`, `3588B0`, `263E30`, and
the `263FF0` class-table helper) were already real — this round
promotes the gate body itself and wires the fixtures that exercise
its non-null arm.

## `3377C0` — the disclosed scripted boundary (`v3377c0`, ×19)

`003377C0` is the spatial/entity broadcast: `q[ctx+0x10]` resolve →
`265090`/`236820`/`31ABE0`/`2EA7F0` gating → `391D10` (normal) or
`3920F0` (NaN/alternate bounds) spatial query → per-entity `263E30`
classification (`+0xE68`/`+0x18` flag chains, `314EB0`, `313F80`
return-class switch). Five image callers (`0x31950C`, `0x334E65`,
`0x335093`, `0x339935`, `0x33BE55`) — promotion needs its entity-list
fixture classified. The bespoke `v3377c0` handler records args AND
snapshots the marshalled `vec4` (`x,y,z` + `w`), then returns the
case's `s9490_ret` — reproducing the old stub's `test eax` contract
at `0x312588` exactly.

## Execution split across the 19 calls

| arm | count | path |
|-----|-------|------|
| `b[0x2089340]&0x10` unset | 17 | `v3377c0(0, &vec)` — null-ctx broadcast stub, ret 0 |
| ctx resolves + `b[node]&8` | 2 | `d228-pos`/`d228-pos2` — real `3590D0`→`3588B0`→`263E30` chain resolves `mctxid=0x12340000` (cls 4, gen 0x123, idx 0) through `clstab` to `ctx0`, `263E30` reads `q[ctx+0x30]` = the new `n30` node → `v3377c0(node, &vec)`, ret `s9490_ret`=1 → `s80f0`/`s9ca0` chain continues as before |

## New fixture

`ctx4` cspec key **`n30`**: allocates a node buffer, wires
`q[ctx+0x30]` (the field `263E30` returns — not previously
plantable), plants `d`/`b` fields. `d228-pos`/`d228-pos2` use
`n30={"b":{0:8}}` so the `b[node]&8` gate passes — `v3377c0`'s rcx
is a real resolved node, pinned against `w.ctxn30`.

## Shipped-value pins

`v3377c0v` snapshots: `vec4.w == 0x3F800000` (**1.0f** — the literal
at `0x1CEBBA8` the body loads via `movss xmm1`) on both pos cases.
`byr("l319490")` ×1 each; `v3377c0` rcx == `w.ctxn30` each.

## Corrections of record

Assert retargets only: two `by("s9490")` sites → `byr("l319490")`;
`s80f0`/`s9ca0` scripted-chain pins unchanged. Zero regression
failures — **542/542 first run**. Census: `l319490` ×19,
`v3377c0` ×19, `l263e30` ×2 (pos cases only — null-ctx arm exits
before it), `l3588b0` ×21 (19 via `319490` + 2 pre-existing callers),
`l3590d0` ×124 (105 pre-existing + 19 new).

## Boundaries (unchanged disclosures)

`30E130` (`e130` ×0), `290B90` (`s290b90` ×34), `317E50` (`b7e50`
×0), `20CE60` (`v20ce60` ×0), `427320` (`v427320` ×1), `422C20`
(`v422c20` ×1), `3377C0` (`v3377c0` ×19 — new), `317ED0`, `3180F0`,
`319CA0` (pos tail chain), `46AB10`, `426130` remain scripted.
`live_game: false`.
