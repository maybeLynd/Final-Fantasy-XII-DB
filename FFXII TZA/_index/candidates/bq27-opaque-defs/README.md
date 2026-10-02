# bq27-opaque-defs — BQ-27 pass O (opaque-definition follow-up)

SWE2-ORACLE, 2026-10-02. Third narrowing pass on BQ-27 ("can any
indirect slot-0/slot-7 call reach `0016D6A0` with edx carrying both bit0
and bit2, i.e. flag value 5?"). Input: the 39 still-open rows of
`../bq27-callee-saved/bq27-cs-sites.tsv` (607-site population, 567
settled).

This pass classifies the **reaching rdx-family definition** at each open
site (last rdx write before the call, scanned inside the enclosing
function's listing, stopping at earlier `call`/`ret`), plus a
path-conditioned-zero rule (`test edx,edx; jne` to a target *past* the
call means every reaching path has edx ≡ 0) and an image-wide writer
census for `edx = d[reg+off]` loads.

## Result — 570/607 settled, 37 open, no flag-5 provable

Three new literal settles (`bq27-opaque.tsv`):

| site | edx | mechanism |
|---|---|---|
| `00624367` | **0** | `edx=[r9]; test edx,edx; jne` *past* the call → reaching value is 0 |
| `00691B06` | **1** | `xor edi,edi` … `lea edx,[rdi+1]` — no jump lands in the window |
| `007DDA3A` | **1** | `xor r14d,r14d` … `lea edx,[r14+1]` — same |

The 37 open rows classify as (see `bq27-opaque.tsv`):

- **25 × `forwards:arg2-edx`** — rdx is never written in the body; the
  function forwards its own arg2 to the vtable call. The flag is the
  *caller's* choice; the residue is the caller population of each
  function, which is the `no-direct-caller`/`callers:*` question the
  callee-saved pass already named.
- **3 × `computed:cmov-cond`** (`00213421`, `00214351`, `002156E2`) —
  edx = `min(x, bound)` via `cmp/mov/cmovg`; a clamped count argument.
- **2 × `field:0x1894`** (`00624317`, `006296FF`) + **`006243EC`**
  (`dec edx` storing the same field) — `d[obj+0x1894]` has exactly one
  image-wide writer: `006243DC mov [rcx+0x1894], edx` where edx =
  `d[arg4]-1` on the `d[arg4]!=0` path. A caller-seeded decrement
  counter — unbounded; bit-0&2 not excludable, destructor semantics not
  provable.
- **1 × `field:glob:02EA1924`** (`00720ADF`) — a .data global with one
  writer, `0075C1B3 mov [02EA1924], ecx` = `r11d` or a conditional field
  dword (`d[rbx+0x38] & 0x10000` → `cmovne ecx, edx`). A saved state
  word, unbounded.
- **1 × `field:0x60` writers=1006** (`00863DD1`) — generic field.
- **4 × open-shaped** — `00212BF9` (`edx=esi`, own argument forwarded
  under a different name), `0022F894` (`sub dx,r8w` — table-derived
  word delta), `006243EC` (above), `0072192E` (`edx=ebx`,
  table-selected object's argument).

No site and no writer provably produces flag value 5; equally, no open
site can be excluded by static dataflow — they pass data, and whether
that data is ever `5` at a *deleting destructor* target is the live
question.

## Boundary

- Flat-listing reaching-def, not full SSA: a backward jump landing
  between a `xor`/`mov` and the call could invalidate a `lit` verdict.
  For the three settles, the listing was grepped for jumps into the
  xor→call windows: none exist (only `je 0x691b08`, a target *after*
  `00691B06`'s call).
- `forwards:arg2-edx` does not claim the callers' flags — it names where
  the next level of analysis lives.
- Field-load verdicts settle nothing about the vtable target's
  semantics: an edx of 5 reaching a non-dtor slot method is not a
  deleting-destructor flag, and a edx of 1 reaching a deleting dtor is
  still "delete, don't free". The row's actual question needs the call
  target's identity, which is the surviving live probe:
  **breakpoint `0016D6A0` with rcx≠0**, now over 37 sites (was 345 at
  pass W entry, 40 at pass CS entry).

## Checks — `bq27_opaque.py` (`FAILS 0`)

1. Input population = the 39 open rows of `bq27-cs-sites.tsv`.
2. Exactly 3 literal settles, all listed above.
3. No site/classification yields `edx=5` (or any `edx&5==5`) provably.
4. `d[+0x1894]` image-wide writer census = exactly 1 store (`006243DC`).

Requires `Y1P_CACHE` (or the default path) to point at the capstone
listing `y1p_all.txt` (`insn_addr func_addr disasm` columns) built from
the canonical exe `73461D08…21F8`.
