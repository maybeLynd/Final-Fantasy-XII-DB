---
experiment: EXP-101
title: Find-owning-battle-unit under isolated original execution
contract: ../10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md
method: B
live_game: false
tool: evidence/find-owning-unit-exec/check.py
---
# EXP-101 — find-owning-unit-exec

**Status:** complete · **19/19 cases, 12/12 mutants, stable across two processes**
**Evidence:** `evidence/find-owning-unit-exec/` (`check.py`, `result.json`,
`bodies.json`, `run.log`, `run2.log`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

`0031B860` — `BattleStats_FindOwningBattleUnit` — is the reverse lookup
from a stats record to its owning battle unit, a shared primitive with a
**35-caller fan-in** from CombatFormula (see the contract's CombatFormula
section). Both `CONTRACT-auto-status-rebuild.md` and the status-write work
consumed it only as a stubbed oracle (EXP-100 scripted it to return a
planted unit). This experiment executes the shipped body and its whole
call closure — **no scripted boundary exists anywhere in this package**.

| VA | role | execution |
|---|---|---|
| `0031B860` | FIND subject: linear scan | **real** (83 B) |
| `00236850` | pool count getter | **real** (7 B) |
| `00236820` | bounds-checked element getter | **real** (37 B) |

## Measured semantics (native execution, not static reading)

```
0031B860(rec):
  if (!rec) return 0                        ; early out, no pool reads
  for (i = 0; i < COUNT(); i++)             ; COUNT re-read EVERY iteration
    u = GET(i)
    if (u && u[0x698] == rec) return u      ; full 64-bit compare, first hit
  return 0

00236850:  return dword [0x208E6A0]         ; count global, 7 B leaf
00236820:  i < 0 || i > count-1 -> 0        ; signed bound both sides
           else qword [0x208E688] + i*0xF50 ; base global, stride 0xF50
```

Findings measured by the suite:

- **Match field** `unit+0x698`, compared as a full qword: a row whose
  back-pointer matches only the low 32 bits of `rec` does not hit
  (`miss-low32`), nor do `rec±8`/`rec±0xF50` (`miss-adjacent`).
- **Scan order** is ascending index; two matching units return the first
  (`hit-dup-first`).
- **Count is re-read per iteration** — the trace of a 3-unit miss is
  `n g0 n g1 n g2 n`, not `n g0 g1 g2`. Both count and base are global
  reads, not cached in the subject's registers.
- **The element-null skip is reachable only through a null pool base.**
  `GET(i)` can return 0 for `0 <= i < count` only when
  `base + i*0xF50 == 0`, i.e. `base == 0 && i == 0`. `base-null-c1`
  (count=1, base=0) confirms: element 0 lands at address 0, is skipped,
  and the scan returns 0. `base-null-fault` (count=2, base=0) then
  dereferences `0xF50+0x698` and faults — **the pool base has no null
  guard**, unlike the index, which is guarded on both sides.
- **The getter's refusal arm is unreachable from this caller.** The loop
  invariant `0 <= i < count` already implies the getter's bound
  `i <= count-1`; the arm is exercised by direct-call cases
  (`getter-neg`, `getter-at-count`, `getter-over`, `getter0-empty`),
  which is what kills the `js`/`jge`/`dec` mutants. From `0031B860`
  alone those three mutations would be unobservable.
- Negative count (`0xFFFFFFFE`) is refused by the `jle` after the first
  count read — trace `n`, return 0.
- `null_rec` returns before touching the pool globals — no `n` fires.

## Mutants

12/12 killed. The set covers the match offset (0x698 → 0x690/0x699), the
compare polarity, the null-record early-out, the miss-path return value,
the loop bound (`jl` → `jle`), the getter's signed bound on both sides
(`js`, `jge`, removed `dec`), the unit stride (0xF50 → 0xF40), and both
global source addresses (decoy pool base / decoy count planted at the
neighbouring `.data` slots so a mis-sourced read diverges).

## Not claimed

- Callers of `0031B860` (the 35 CombatFormula edges) are not executed.
- What `unit+0x698` points *to* beyond the back-pointer comparison, and
  the pool's allocation lifecycle, are not exercised.
- `00236820`'s bound being unreachable from this caller is established
  for **this call site only** — other callers may reach it.
- No live-process behavior; fixture pools are authored data.

## Files

- `check.py` — Unicorn harness; whole image mapped, pool/count globals
  planted in `.data`, heap arena `0x40000000`.
- `result.json` — per-case traces/observables + mutant outcomes.
- `bodies.json` — span + sha256 of the three real bodies.
