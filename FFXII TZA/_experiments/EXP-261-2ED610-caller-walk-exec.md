# EXP-261 — `002ED610` caller-side walk over `002ED570` (direct entry)

**Status:** complete — **571/571 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 prefix `0040634e`; 571
cases), fault census 24** (the 20 pre-existing intentional-null
fixtures plus the two new pinned `0x2ED648` derefs — each records
a `mem` and a `uc` stop tuple).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn on the `ecarr` + `dcntr`/`c2` fixtures;
nothing claims initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..260).
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Mechanism exercised (all shipped bytes, `d2ed610-*`)

`002ED610(cx = ecarr word index, dx = 0x290-stride multiplier)`:

```
edi = zx(dx)
row = cx == -1 ? 0 : q[022C6F28] + sx(cx) * 0x740
if d[row + 0x284] == 0: row = 0            (cmove)
ebx = d[row + 0x18]                        <- UNGUARDED when row==0
if ebx == -1: ret 0                        (checked twice — the
                                            second cmp at 0x2ED658
                                            is dead; rbx is callee-
                                            saved across 20E600)
elem = 20E600(d[row + 0x10])
rax = 2ED570(q[elem + 0xD98], ebx)         ; ==0 -> ret 0
ret = 20E600(d[rax + 0x84]) + edi * 0x290
```

Resolve-only — `002ED610` performs no writes of its own (the `&=~8`
is `00422C20`'s, not `002ED570`'s); the only stores are
`002ED570`'s resolved-base caches `q[C2+0x38]`/`q[C2+0x10]`.

## Cases and pins

- **`d2ed610-live`** — row 2 live (`d[+0x284]`≠0), `d[+0x10]`=elemb
  offset `0x70000`, `d[+0x18]`=slot 1 → `002ED570` resolves e2 →
  `d[e2+0x84]`=`0x72000` → `ret = elemb+0x72000 + 3*0x290`
  = `elemb+0x727B0`, exact-pointer pinned. `d[e2]` stays `0xF`
  (no `&=~8` on this path).
- **`d2ed610-slotm1`** — `d[row+0x18]`==-1 → ret 0 before `20E600`.
- **`d2ed610-c2nul`** — `002ED570` returns 0 (row gate `-1`) → ret 0;
  bases still resolved and stored into `C2` before the gate.
- **`d2ed610-dead`** / **`d2ed610-neg1`** — dead row
  (`d[+0x284]`==0) and `cx==-1` both funnel to `rax=0` then read
  `d[0x18]` — an **unguarded null deref**, pinned by
  `expect_fault=0x2ED648`. No page-0 fixture is fabricated; the
  fault PC is the honest record that real callers must guarantee a
  live row.

## Not claimed

- Which callers feed `002ED610` and whether the crash arms are ever
  reachable in initialized gameplay (a negative xref is not proof of
  absence — but both arms were read in the shipped body and are
  unguarded in the code itself),
- the `0x290`-stride destination structure's semantics beyond the
  pointer arithmetic,
- `0036B130` rejection arms, `0051BA40` mode-0/`&2`, `0041CF00`
  row-loop/`0x1000` arms, `005369C0`/`003B02A0` real —
  `NATIVE-REPLAY`, `live_game: false`.
