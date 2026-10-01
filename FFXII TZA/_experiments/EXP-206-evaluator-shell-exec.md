# EXP-206 — `002B3050` evaluator wrapper + `002B3120` float→word shell, executed

**Status:** complete — **438/438 cases, stable across 3 independent runs,
byte-identical `result.json` (SHA256
`1527aab08722b6cab5ea6174411718339985561577f4880c3e1eb5f69c90e560`), zero
unexpected faults.**
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes executed
under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py` (extends
EXP-192..205; 431 inherited + 7 new `b3120-*`/`b3050-*` cases)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Scope

EXP-205 left `002B3050` as the last scripted edge on the display path — its
transitive closure is ~131 bodies of CRT/format machinery. Fresh decode showed
the body itself is a 0xC0-byte wrapper whose depth lives entirely inside its
callees, so this package promotes `002B3050` plus its worker `002B3120`
(~0x160 bytes, single callee `002B24B0`) to executed bytes while the
evaluator/formatter core stays a bounded stub. **With this, every body on the
display path executes as shipped bytes** — the only remaining stubs are the
CRT evaluator `002B24B0` and five leaf helpers.

## `002B3050(ctx, str, outW1, outW2)` — evaluator wrapper (0xC0 bytes)

`00506700`'s type-2 arm calls `2B3050(0, q30-string, slot+0x40, slot+0x42)`
(recorded args `0, str, +0x40, +0x42` on both `bd00-t2` and `d4d0-near`).

- `rbx=ctx`, `rdi=str`, `rsi=outW1`, `rbp=outW2`.
- `002AC1E0(&state[rsp+0x20])` — initializes a 0xD0-byte evaluator state
  struct (scripted leaf `s2ac1e0`).
- `q[state+0x90] = 0` — becomes `002B3120`'s stack arg (r8 = 0 to
  `002B24B0`).
- `0039BAD0(ctx) -> bl` — byte query on the ctx object (`s39bad0`).
- **Flag arm:** if `00254A10() == 0` **and** `bl == 7`:
  `d[state+0x64]` gets `bts 0xB`, then `0039C4A0((d64 >> 0xB) & 1)` is
  called and its result stored to `q[state+0x80]` — proven live by
  `b3050-arm`: `s39bad0_ret=7` + `s254a10_ret=0` → `s39c4a0` called with
  rcx `= (0xCDCDCDCD >> 0xB) & 1 = 1`, and `q[evaluator-struct+0x80]` in
  the copied frame reads back `0x1234` (the stub's return).
- `b[state+0xC3] = 0`; `002B3120(&state, rdx=outW1, r8=outW2,
  stack-cell=str)` — the str pointer goes to `q[rsp+0x48]` = the callee's
  `[rsp+0x50]` input cell (see below).
- Returns whatever `002B3120` leaves in `eax`.

## `002B3120(state, outW1, outW2)` — float→word output shell (0x15C bytes)

- **Null gate:** `q[state+0x28] == 0` → writes `w[outW1]=0`, `w[outW2]=0`
  (each guarded), returns `0` — no evaluator call (`b3120-nil`).
- Otherwise copies the whole **0xD0-byte state struct** to its frame
  (`rsp+0x70`, 13 `movups`), builds a 5-slot pointer array on the stack
  (`rsp+0x20..0x40` → cells `+0x58,+0x60,+0x5C,+0x50,+0x51`), and calls
  `002B24B0(&copy, &double-const@009166EC, r8=[rsp+0x98], r9=&cell+0x54,
  stack ptrs)` — the real evaluator, stubbed.
- Output plumbing (all proven): `w[outW1] = cvttss2si d[rsp+0x54]` and
  `w[outW2] = cvttss2si d[rsp+0x58]` — **the evaluator returns two
  floats, truncated to words** (`b3120-ok`: `30.7→30`, `-2.9→0xFFFE`;
  `b3120-negf`: `200.9→200`, `0.4→0`). Each write is guarded — null out
  pointers are skipped (`b3120-noout` returns the byte anyway).
- Return value `movsx eax, b[rsp+0x50]` — a **byte** (`b3120-negf`:
  `0xFF → 0xFFFFFFFF`).
- ABI note: `002B3050`'s `q[rsp+0x48]=str` lands on the callee's
  `[rsp+0x50]` cell — `002B24B0` reads the string pointer through that
  arg-pointer slot and the same cell is overwritten by the result byte
  (`b[r9-4]` in the stub, `r9 = &+0x54`).

## End-to-end consequence

`bd00-t2` / `d4d0-near` now show `l2b3050`→`l2b3120`→`s2b24b0` in place of
the old `s2b3050` record, and `w[slot+0x40]`/`w[slot+0x42]` receive the
stub-evaluator's truncated floats (`17.9→17`, `4.2→4`). These two words —
the string's measured dimensions — are what `00506700` packs into the
display slot for the type-2 path.

## Still scripted (disclosed)

`002B24B0` (the real evaluator — ~131-body CRT subtree, fixture-stubbed
via the `b24b0` tuple), `002AC1E0`, `0039BAD0`, `00254A10`, `0039C4A0`,
`00808C40` (cookie). The `bl==7` gate's meaning (a `0039BAD0` byte-query
kind) and `00254A10`'s global predicate are internal to the stubbed
helpers and are not claimed.

## Corrections of record

- `002B3050` is not itself a formatter — a state wrapper over the
  `002B3120` worker. EXP-201/202's "string copy" label is narrowed:
  it measures/evaluates and writes two truncated-float words plus a
  byte return.
- `b3120-noout` initially faulted writing `w[2]` — the case lacked an
  explicit `edx`, and `main()` defaults `edx` to `w.sel` (=2), so `rdi`
  was nonzero. Explicit `edx=0`/`r8=0` asserts the null-out guard.

## Validation

`python check.py` — 438/438, three independent runs, `result.json` SHA256
`1527aab08722b6cab5ea6174411718339985561577f4880c3e1eb5f69c90e560`
(byte-identical), zero unexpected faults.
