---
experiment: EXP-120
title: EXP-108 tail resolvers — the two remaining scripted boundaries of the ramp-channel consumer tree, executed real
contract: ../17-Presentation-Rendering/CONTRACT-render-record-pool-lifecycle.md
method: B
live_game: false
tool: evidence/exp108-tail-resolvers-exec/check.py
---
# EXP-120 — exp108-tail-resolvers-exec

**Status:** complete · **14/14 functional cases, 14/14 mutants, stable
across three processes**
**Evidence:** `evidence/exp108-tail-resolvers-exec/` (`check.py`,
`bodies.json`, `gen_bodies.py`, `result.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

EXP-108's evidence pack scripted three boundaries on a "deep subtree"
estimate. `002ED570` was closed by EXP-117; this package executes the
remaining two — and the estimate was wrong again:

- `003E56A0` is **24 B / 9 insns**, not the "358 B deep object
  resolver" the EXP-108 note recorded.
- `00370F60` is **61 B / 19 insns** calling only `0020E600`.

| VA | role | execution |
|---|---|---|
| `003E56A0` | F56 — `+0x400` table tail resolver | **real** (24 B, 9 insns) |
| `00370F60` | F60 — `0x290`-stride record lookup | **real** (61 B, 19 insns) |
| `0020E600` | BASE — arena codec base | **real** (10 B, 3 insns; rerun in-tree) |

**Zero scripted boundaries** — every call target executes real. All
object memory is planted fixture (disclosed): the F56 record arg, the
inline-offset table, and F60's pointer arg; `q[0x01F83530]` codec base
is planted at its real shipped address.

## Measured semantics (native execution, not static reading)

**F56 `003E56A0(rcx=rec, edx=arg) -> rax`:**

1. `rdx = q[rec+0x400]` — **this clobbers the argument register**.
   The second parameter is dead: `f56-deadarg` runs the entry twice
   with `rdx = 0` and `rdx = 0xDEADBEEF` and gets identical results.
2. `rdx == 0` → return `0`.
3. `ret = sx32( zx16(w[rdx+2]) + edx )` — and `edx` is now the table
   pointer's own low dword, so the body computes
   **`sx32( low32(tab) + w[tab+2] )`** — effectively `tab +
   inline_offset`, a pointer-shaped result sign-extended through
   `cdqe` (`f56-sign`: tab `0x7FFF9000` + `0x8000` → sum `0x80008000`
   → `rax = 0xFFFFFFFF80008000`).
4. The word is `movzx` — `w[tab+2]` is **unsigned** (`f56-negword`:
   `0xFFFF` adds `65535`, not `-1`).

This is the same `+0x400` table the FLDR resolver (`003E5AD0`,
EXP-117) and GETV arm-3 (`003E5B30`, EXP-118) read — F56 resolves a
cursor into it.

**F60 `00370F60(rcx=p, edx=idx) -> rax`:**

1. `rbx = sx32(edx)` first — the index sign-extends **before** the
   sentinel test.
2. `bx == 0xFFFF` → return `0`. The test is on **low16**, not
   `idx == -1`: `f60-low16` (`idx = 0x0001FFFF`) returns `0`, but
   `f60-hineg` (`idx = 0xFFFF0000`) **proceeds** with `sx32 = -65536`
   → `base - 0x1060000 + 0x80`.
3. `ret = BASE(d[p+0x84]) + sx32(idx)*0x290 + 0x80` — a `0x290`
   (656 B)-stride record lookup biased `+0x80` past the resolved
   base. Negative indices address backward (`f60-neg2`:
   `base - 0x520 + 0x80`).

**BASE `0020E600`:** unchanged — `q[0x01F83530] + u32(arg)`.

## Execution findings (beyond the static reading)

1. **F56's second parameter is dead code at the ABI level.** Callers
   pass a value in `edx` (EXP-108/109 traces captured args), but the
   body's first instruction overwrites `rdx` with the table pointer
   and `add eax,edx` then adds the pointer's own low dword. The
   function is `resolve_table_cursor(rec)`, arity one.
2. **The result is a sign-extended 32-bit pointer sum.** `cdqe`
   makes the high half all-ones whenever `low32(tab) + offset ≥
   0x80000000` — a caller treating the return as a pointer relies on
   the table living in the low 2 GB.
3. **F60's sentinel is `low16(idx) == 0xFFFF`, not `idx == -1`.**
   `0x0001FFFF` is rejected; `0xFFFF0000` indexes `-65536` records
   backward. The guard is a 16-bit sentinel on a 32-bit field.
4. **Every scripted boundary in EXP-108 is now closed** — the three
   "deep subtree" notes were all stale (`002ED570` EXP-117;
   `003E56A0`/`00370F60` here). The same pattern held for EXP-109's
   `0051B9E0`/`00370E20` (EXP-119) — the "deep" annotations
   overestimated thin resolvers.

## Mutation campaign

14 byte-precise mutations, every site verified against shipped bytes
before patching:

- **F56 (7):** table disp `+0x400`→`+0x408`; `test rdx`→`test rcx`
  (null case dereferences `w[0+2]` → fault at `0x2`); `jne`→`je`;
  `movzx word`→`byte` (killed by `w=0x180`); word disp `+2`→`+4`;
  `add`→`sub` (returns `w - low32(tab)`); `cdqe 48 98`→`REX nop`
  (killed by `f56-sign` — rax upper stays 0).
- **F60 (7):** `movsxd rbx,edx`→`rbx,eax` (product collapses to 0);
  cmp const `0xffff`→`0xfffe` (`idx=-1` proceeds); `je`→`jne`;
  offset disp `+0x84`→`+0x88`; stride `0x290`→`0x280`;
  `sub rax,-0x80`→`add` (`-0x80` vs `+0x80`); `add rax,r8`→`sub`.

**14/14 killed.** The dead-arg finding made `f56-deadarg` a
functional case rather than a mutant — no byte change can make the
parameter live.

## Limitations

- All object memory is planted fixture; the executed code and
  `q[0x01F83530]` are the real shipped bodies and real global
  address.
- `f56-badptr`'s fault is recorded as a fault observation — the
  model predicts the faulting address (`tab+2`), not a return.
- `bodies.json` holds body span + sha256 over shipped bytes for all
  three real bodies; instruction-start coverage convention matches
  EXP-107–119.
