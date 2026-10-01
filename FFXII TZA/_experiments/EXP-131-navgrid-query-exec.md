---
experiment: EXP-131
title: nav-grid query tree — QWALK 0033D3E0 adjacency-walk segment
  probe over WWRAP/GGRID/ROOTL/TTEST/ETHUNK/ECLASS/SEGT/BASE with
  real VSUB/XPROD/__security_check_cookie, executed real
contract: none — consumer anchor is the corridor-width probe PRED
  00335E50 (EXP-130, which scripted this tree as its deep boundary);
  no reciprocal contract names this experiment, so findings adoption
  is routed via REQ-OPUS
method: B
live_game: false
tool: evidence/navgrid-query-exec/check.py
---
# EXP-131 — navgrid-query-exec

**Status:** complete · **54/54 functional cases, 61/61 mutants, stable
across three processes**
**Evidence:** `evidence/navgrid-query-exec/` (`check.py`,
`bodies.json`, `gen_bodies.py`, `result.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

The claimed slice was the nav-grid query tree that EXP-130 scripted
as `0033D3E0`'s deep boundary: the full point→triangle and
segment→adjacency query stack. All bodies execute real under Unicorn
against a planted synthetic nav mesh:

| VA | role | execution |
|---|---|---|
| `0033D3E0` | QWALK — tri-adjacency segment walk | **real** (631 B, 145 insns) |
| `00384130` | WWRAP — `{x,z}` pair wrapper → GGRID | **real** (40 B, 9 insns) |
| `00383F10` | GGRID — grid point query → tri id / `0xFF` | **real** (542 B, 141 insns) |
| `00383840` | ROOTL — `rax = q[0x2AEDFB0]` | **real** (8 B, 2 insns) |
| `00382D10` | TTEST — point-in-triangle test | **real** (391 B, 93 insns) |
| `0032A780` | ETHUNK — `jmp 0026E300` | **real** (5 B, 1 insn) |
| `0026E300` | ECLASS — edge-class bit-pair query | **real** (73 B, 22 insns) |
| `00468880` | SEGT — seg-vs-seg orientation test | **real** (496 B, 108 insns) |
| `0020E600` | BASE — `rax = ecx + q[0x1F83530]` | **real** (10 B, 3 insns) |
| `00203080` | VSUB — inside SEGT (re-executed) | **real** (81 B, 17 insns) |
| `00202E10` | XPROD — inside SEGT (re-executed) | **real** (115 B, 26 insns) |
| `00808C40` | `__security_check_cookie` | **real** (33 B, 8 insns) |

Scripted boundary (traced, NOT executed):

- `api-ms-win-crt-math-l1-1-0.dll!_fdclass` — real IAT cell
  `q[0x8C2C10]` (ships an unbound hint record; identity proven by the
  PE import directory), planted to `0x63070000`; host computes the
  exact CRT float-class result on the `movss`-presented float:
  NaN → `2`, ±inf → `1`, normal finite → `-1`, denormal → `-2`,
  zero → `0`.

Planted fixture globals (disclosed; all BSS — ship zero):

- `q[0x2AEDFB0]` — nav-grid root pointer.
- `q[0x1F83530]` — BASE pool base; `BASE(i) = pool + i`.
- `d[0x209A3E0]` — ECLASS bit-pair table (BSS, runtime-populated).

Shipped rdata read from the image: `d[0x915760]` class→bit table
(6 dwords → bit indices `23/25/26/27/−1/24`), `d[0xD112B0]` triangle
edge index array `{0,1,2,0}`.

## Measured semantics (native execution, not static reading)

**QWALK** (`0033D3E0`, `rcx=p1, rdx=p2, r9d=walk flag`): walks the
triangle adjacency graph, advancing across edges the segment crosses.

- `grid(p1) == 0xFF` → return `0`; `grid(p2) == 0xFF` → return `1`
  (both go through WWRAP→GGRID for real).
- `cur == dst` → return `0`. Candidate slots `0..deg-1`
  (`deg = w[root+0xA]` tri count); slot `== cur` or `== prev` skipped.
- `m[cur*deg + slot]` — 2-byte adjacency entries — is a **1-based
  edge-record index**; `0` means no edge.
- Edge record at `BASE(edgeId*8)` (record stride 8, `{w va, w vb,
  b +4, b class@+5, b flag@+6}`), vertex pool at `root+0xC` pool.
- `ECLASS(edge.class, flag)`: `1` → proceed; `0` → flag gate
  `b[ep+6] & (1<<flag)`; else skip.
- `SEGT(p1,p2,va,vb)` returns `1` → advance `prev=cur, cur=slot`
  (slot's tri = matrix slot index, not the edge's far vertex).
- Exhaust all slots → return `1`; budget `r13d == 0x80` → return `0`.
- Exit `rax` on early-outs is the cookie residual path through CHKCK.

**GGRID** (`00383F10`, `rcx=&{x,z}`): grid point query → tri id or
`0xFF`.

- `_fdclass(x)`/`_fdclass(z)` — `ax==2` (NaN) → return `0xFF`.
- `comiss` bounds vs grid header: unordered/below → `0xFF`.
- `cvttss2si` then **signed `idiv`** by cell width/height — truncates
  toward zero (`cvttss2si` invalid/overflow → `0x80000000`).
- Cell map byte → list offset → 0xFF-terminated byte list of record
  indices; record stride `0x22`, tri selector at `+0x14`; `TTEST`
  per candidate; first hit returns its id, exhaustion → `0xFF`.

**TTEST** (`00382D10`, `rcx=pt pair, rdx=idx array, r8d=count`):
reads the **second** shipped index first (`0x382D7A`), then vertex
fields in a fixed order — the model reproduces exact read order and
fault sites (`tri-badptr` proves `0x382DFA` on a wild pointer).
Same-sign `ucomiss` accumulation over the three edges.

**ECLASS** (`0026E300`, `ecx=class, dx=flag`): **asymmetric sign
extension** — `dx` sign-extends for the class table index, `ecx`
sign-extends for the bit-pair table. A negative **table entry**
(`classtab[4] == −1`) returns `0xFFFFFFFF`; a negative *argument*
does not (`classtab[-1]` ships `0x3F800000` — positive). Bit-pair
result: both words set → `2`, low only → `1`, else `0`.

**SEGT** (`00468880`): two stacked orientation evaluations built from
VSUB ×6 + XPROD ×4, `comiss`-style compares on the z components;
cookie-checked (`__security_check_cookie` real).

## Scope corrections found by execution

1. **BSS cell addresses were wrong (rip+disp class, third
   occurrence):** root `0x5ADFB0` → **`0x2AEDFB0`**, BASE pool
   `0x1FED530` → **`0x1F83530`**. Native standalone tests read zero
   until the true RIP-relative targets were computed.
2. **The bit-pair table is BSS** — `0x209A3E0` lies beyond raw
   section data; ships zero, planted per case.
3. **Edge ids are 1-based record indices** — record 0 is unused
   padding; the first real edge is index 1.
4. **Native `idiv` truncates toward zero** — Python `//` floors;
   `-7 // 2` differs from the shipped body on negative numerators.
   `cvttss2si` overflow/NaN yields `0x80000000`, not an exception.
5. **`_fdclass` sees the float, not a double** — the caller passes
   via `movss` with no `cvtss2sd`; the host model reproduces the
   observed class map rather than calling the double API.
6. **`m-walk-slotsk` mutant insight** — the slot register `ebx` in
   the loop is not fixed: it cycles through dst, edge id, and vertex
   index as the loop reloads it, so a naive reg-swap mutation is
   dead. The landed mutant flips the prev-skip to a cur-skip and
   diverges through watched memory (last-tested edge).

## Validation

- **54/54 functional cases** — leaf (BASE/ROOTL/ECLASS), TTEST,
  SEGT, WWRAP, GGRID, and QWALK levels; includes invalid-pointer
  fault ordering, NaN/inf/denormal/zero `_fdclass` classes, signed
  division edges, empty/off-grid/FFFF lists, flag gates, negative
  class entries, 1/2/3-hop walks, dead ends, and budget cycles.
- **61/61 byte-precise mutants** — each patches one verified shipped
  byte; all sites byte-asserted against the EXE image.
- Stable across three independent processes; exit 0.

Evidence class: **NATIVE-REPLAY** over a disclosed synthetic fixture
— proves the shipped bodies' semantics, not production integration.
