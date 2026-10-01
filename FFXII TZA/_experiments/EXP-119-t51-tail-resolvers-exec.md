---
experiment: EXP-119
title: T51/E20 tail resolvers — the two boundaries that stayed scripted through EXP-109/117/118 on a stale "deep" estimate, executed real
contract: ../17-Presentation-Rendering/CONTRACT-render-record-pool-lifecycle.md
method: B
live_game: false
tool: evidence/t51-tail-resolvers-exec/check.py
---
# EXP-119 — t51-tail-resolvers-exec

**Status:** complete · **16/16 functional cases, 15/15 mutants, stable
across three processes**
**Evidence:** `evidence/t51-tail-resolvers-exec/` (`check.py`,
`bodies.json`, `gen_bodies.py`, `result.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

EXP-118's record named the residual honestly: `0051B9E0` (the T51
tail of G42) and `00370E20` (the D6A tail) stayed scripted through
EXP-109/117/118 on a "deep ~85 insns / 6 calls" estimate. Reading the
bodies shows the estimate was wrong — **neither is deep**:

- `0051B9E0` is a 5-byte `jmp 0051F240` thunk; `0051F240` is 138 B /
  43 insns calling only `003AB7F0` (RES, already real).
- `00370E20` is 11 B / 2 insns: `mov ecx,[rcx+0x94]; jmp 0020E600`.

This package executes both real — closing **every** scripted boundary
in the `003E5B30` get_vec tree except `0036B130` (already proven real
in EXP-084).

| VA | role | execution |
|---|---|---|
| `0051B9E0` | T51T — jmp thunk | **real** (5 B, 1 insn) |
| `0051F240` | T51 — `resolve_element(ctx, idx)` | **real** (138 B, 43 insns) |
| `00370E20` | E20 — `BASE(d[p+0x94])` | **real** (11 B, 2 insns) |
| `003AB7F0` | RES — handle-mode dispatcher + bound | **real** (99 B, 32 insns; rerun in-tree) |
| `0020E600` | BASE — arena codec base | **real** (10 B, 3 insns; rerun in-tree) |
| `0036B130` | RES's nonzero-mode resolver | scripted boundary — **executed real in EXP-084**; args traced as `hres:` |

All object/table memory is planted fixture (disclosed): the ctx
object, the 48-byte-stride element table, and E20's pointer arg.
`q[0x01F83530]` codec base is planted at its real shipped address.

## Measured semantics (native execution, not static reading)

**T51 `0051F240(rcx=ctx, edx=idx) -> rax`:**

1. `mode = sx2(d[ctx+4])` — `shl r8d,0x1e; sar r8d,0x1e` keeps the
   low two bits sign-extended: `{0→0, 1→1, 2→-2, 3→-1}`.
2. `mode == 0` → `base = RES(q[ctx+8])`;
   `mode == 1` → `base = q[ctx+8]` directly (no RES call);
   `mode == 2/3` → return `0` **before any table read**.
3. `elem = base + (idx & 0xFFFF) * 48` — the index is masked to a
   word (`movzx ecx,di`), element stride is 48.
4. `elem == 0` → return `0`. **The null check is on the element
   pointer, not the table** — a null-resolved table with `idx != 0`
   produces `elem = idx*48` and dereferences it (`t51-nulltab-i1`
   faults reading `b[0x30]` — a real crash path).
5. `b[elem] & 2` → lazy resolve + write-back:
   `q[elem+0x18] = sx32(RES(q[elem+0x10]) + d[elem+0x20])` —
   `movsxd` sign-extends the 32-bit sum into the qword slot.
6. `return q[elem+0x18]` — the cached slot whether freshly written
   or not.

**E20 `00370E20(rcx=p) -> rax`:** `ecx = d[p+0x94]` (zero-extended —
the offset is **unsigned**), tail `BASE` → `rax = q[0x01F83530] +
ecx`. `e20-big` (`0xFFFFFFF0`) returns `ARENA + 0xFFFFFFF0`.

**RES `003AB7F0`:** unchanged from EXP-117 — `rcx==0 → 0`;
`low2==0 → passthrough`; else `0036B130` with the `sx32 ≤ 0x40`
result bound (observed again in-tree: `t51-hres-low`'s `0x30`
resolves to `0`, and the addend still applies → `q[+0x18] = 0x20`).

## Execution findings (beyond the static reading)

1. **The "deep tails" were thin.** Both bodies that carried a
   ~85-insn estimate since EXP-109 turn out to be a 5-byte thunk and
   an 11-byte trampoline — the residual was an overestimate, not a
   subsystem. The `003E5B30` tree is now proven-real end to end.
2. **T51's null guard is on the element, not the table.** A table
   that resolves to `0` only short-circuits when `idx == 0`; any
   nonzero index dereferences `idx*48` — `t51-nulltab-i1` faults at
   `0x30`. The resolver does not validate its inputs.
3. **The mode field is a signed 2-bit value.** `shl/sar 0x1e` makes
   `d[ctx+4]&3 == 2` produce `-2`, `3` produce `-1` — both return 0.
   `m-t51-shl` (`0x1e`→`0x1f`) is killed on `t51-mode2`: shifting by
   31 truncates to `0` and the body proceeds.
4. **The lazy write-back writes a sign-extended dword.** `RES(hdl)
   + addend` is computed in `eax`, `movsxd` to `rcx`, stored to
   `q[elem+0x18]` — `t51-neg-add` (`addend 0xFFFFFFF0`) stores
   `hres − 0x10` as a signed qword.
5. **The RES bound does not suppress the addend.** `t51-hres-low`:
   the element handle resolves `0x30 → 0` via the bound, but
   `0 + 0x20` still writes `0x20` — the bound zeroes the handle, not
   the sum.
6. **`idx` is masked to 16 bits.** `movzx ecx,di` —
   `t51-idx-wrap` (`idx = 0x10001`) reads element 1.
7. **E20's offset is unsigned.** `mov ecx` zero-extends — E20 is
   `BASE + u32(d[+0x94])`, not a signed add.

## Mutation campaign

15 byte-precise mutations, every site verified against shipped bytes
before patching:

- **T51 mode decode (2):** `shl 0x1e`→`0x1f` (killed on `t51-mode2` —
  the truncated shift yields `0` and the body proceeds), `cmp 1`→`2`
  (mode-1 arm unreachable).
- **T51 index arithmetic (4):** mode-0 and mode-1 `lea [rcx+rcx*2]`
  SIB scale `2`→`4` (stride 80), both `shl 4`→`3` (stride 24) — the
  arms are separate instruction pairs and each needs its own site.
- **T51 table disp (2):** `+8`→`+0x10` in both arms — the mode-0
  site turns the RES arg into `0` (fault at `0x30`), the mode-1
  site adds the element offset to `0`.
- **T51 lazy path (5):** flag `test 2`→`4`, handle disp
  `+0x10`→`+0x18` (resolves the old cache slot), addend disp
  `+0x20`→`+0x24`, write-back disp `+0x18`→`+0x20` (clobbers the
  addend — observed in the `elems` diff), return disp
  `+0x18`→`+0x20` (returns the addend dword).
- **T51T (1):** `jmp E9`→`call E8` — the "return" lands on int3 →
  fault.
- **E20 (1):** offset disp `+0x94`→`+0x98`.

**15/15 killed.** `t51-nulltab-i0`/`i1` needed the `elem == 0` vs
`elem = idx*48` split to pin the guard's position; the stride
mutants needed per-arm sites because the two index blocks are
separate instruction pairs.

## Limitations

- `0036B130` remains the only scripted boundary — executed real in
  EXP-084 (`efx-source-rebase`), so the full RES call tree is proven;
  only the planted per-case return is synthetic. `hres:` tokens
  record each call's argument.
- RES/BASE are re-executions already proven in EXP-084/117/118 —
  included because T51/E20 call them and re-verification is free
  corroboration.
- All object/table memory is planted fixture; the executed code and
  `q[0x01F83530]` are the real shipped bodies and real global
  address.
- `bodies.json` holds body span + sha256 over shipped bytes for all
  five real bodies; instruction-start coverage convention matches
  EXP-107–118.
