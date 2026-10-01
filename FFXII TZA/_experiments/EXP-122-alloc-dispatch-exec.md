---
experiment: EXP-122
title: EXP-109 allocator dispatch — the staged-kind front door and the
  create-with-retry path, executed real
contract: none — the executed subject is the general allocator's dispatch
  layer (0036A100 front door, 0036BFE0 create-with-retry into 0036BC60);
  the allocator family 00369860–0036C900 has no contract — its
  documentation home is the page
  24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md.
  The previous key named the render-record-pool contract, whose own §13
  declines this record (the intersection is the two shared helpers
  0020E600/0020E620, three instructions each)
method: B
live_game: false
tool: evidence/alloc-dispatch-exec/check.py
---
# EXP-122 — alloc-dispatch-exec

**Status:** complete · **16/16 functional cases, 14/14 mutants, stable
across three processes**
**Evidence:** `evidence/alloc-dispatch-exec/` (`check.py`,
`bodies.json`, `gen_bodies.py`, `result.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

EXP-109 scripted the `0036A100` allocator family on stale sizes. The
family's true shape is the whole allocator subsystem — `0036BC60` alone
is 887 B / 246 insns with ten callees, and `0036A2A0` recurses back into
it. This package executes the bounded **dispatch layer** — the two
entry points every allocation request passes through — with the deep
core disclosed as scripted boundaries:

| VA | role | execution |
|---|---|---|
| `0036A100` | A100 — front door: BC60 then BFE0 fallback | **real** (129 B, 36 insns) |
| `0036BFE0` | BFE0 — create-with-retry dispatcher | **real** (261 B, 77 insns) |
| `0020E620` | C620 — BASE-inverse leaf | **real** (9 B, 3 insns) |
| `0036BC60` | BC60 — allocator core | scripted (planted returns) |
| `0036AAD0` | AAD0 — live-pool counter | scripted (planted return) |
| `0036ABE0` | ABE0 — live-pool flag | scripted (planted return) |

The indirect `call rax` at `0x36C03B` is **not stubbed** — the fixture
plants `q[desc+0xA0] = 0046DFE0` (the FLAG leaf executed real in
EXP-121), so the per-kind constructor dispatch runs a real shipped body
through the real indirect call.

All BSS globals (mask, staged word, descriptor table, codec cell,
object pointer) are planted fixture, disclosed; the executed code and
every global address are real.

## Measured semantics (native execution, not static reading)

**A100 `0036A100(ecx=arg) -> rax`:**

1. `edi = ecx` — the request argument (`edx`/`size` downstream).
2. `rax = BC60(ecx = d[0x22D89BC], edx = edi)` — the staged word
   (`ST_W`, the queue push's tag store from EXP-121) **is the
   allocation kind**. Scripted here; the trace shows
   `bc60:stw:arg`.
3. On null: `rax = BFE0(ecx = d[0x22D89BC], edx = edi)` — the **same
   cell**, not a neighbouring one. (The first harness revision read
   `d[0x22D89BD]` — a 6-vs-7-byte decode slip; execution traces
   settled `ecx = ST_W` at the gate.)
4. On success (either arm): `b[rbx-0x3E] = b[0x22D8E18]` (the staged
   byte2 — the object's class tag), `d[rbx-0x10] = C620(0) =
   -low32(arena base)`, `w[rbx-2] = 0`. `rbx` is the returned pointer
   — the header extends *below* it.
5. On double-null: returns `0`, no header writes (`a100-null`).

**BFE0 `0036BFE0(ecx=kind, edx=size) -> rax`:**

1. `bt(d[0x22D89B8], ecx&0x1F)` — the kind's mask bit must be **set**
   or the body falls into `jmp $` at `0x36C000` — a hard spin, never
   re-read (`bfe0-spin`, `bfe0-karg-bit3`).
2. `kind_d = sx32(d[0x22D89BC])` — ST_W re-read **inside** the body.
   `desc = 0x22D7FD0 + kind_d*0xA8` when `kind_d <= 0xE`, else `0`.
   (The descriptor table base is `0x22D7FD0` — the first static read
   had `0x22D8FD0`, off by `0x1000`; rbx at the pool check proved
   `0x22D8120` for kind 2.)
3. `kind_d > 0xE` → `desc = 0` → `mov rax,q[0xA0]` → **real fault**
   (`bfe0-desc-hi` — the out-of-range-kind crash path is recorded as
   a fault observation).
4. `cb = q[desc+0xA0]` — per-kind constructor. Non-null →
   `call rax(ecx = kind_d, edx = size)` → `esi = result`; here it
   executes the real FLAG leaf, so `esi = (d[0x215EFF4]==-1 ? 2 : 0)`.
5. Pool check — only when `bt(mask, kind_d)` set AND `q[desc+0x50]!=0`:
   `edi = AAD0(desc)` + `(ABE0(desc) != 0)`. `edi != 0` →
   `b[desc+2] = 1; b[desc+0x62] = 1` — marks the descriptor live.
6. `rax = BC60(ecx = kind_d, edx = size)` — the alloc call.
7. Result routing — **three outcomes**:
   - `edi != 0 && rax == 0` → `jmp 0x36C013` — **retry**: re-reads
     ST_W and redispatches the whole pass (callback included).
   - `edi == 0 && rax == 0 && esi != 0` → retry — the ctor reported
     work, so try again.
   - otherwise return `rax` (`bfe0-retry` settles `0,OBJ` across two
     passes; `bfe0-fail` returns `0` when `esi == 0`).

   The retry re-reads `d[0x22D89BC]` each pass — the staged kind can
   legally change between passes (the queue push stages it).

**C620 `0020E620(ecx) -> eax`:** `ecx - low32(q[0x1F83530])` — the
**inverse** of BASE `0020E600` (`base + u32`): converts an arena
pointer back to an offset. A100 calls it with `ecx = 0`, producing
`-low32(arena)` for the object's `-0x10` header slot.

## Execution findings (beyond the static reading)

1. **The queue tag is the allocation kind** — EXP-121's push writes
   `d[0x22D89BC]`; this dispatch reads that same dword as `kind` for
   BC60, BFE0's mask gate, the descriptor index, and the constructor
   argument. The staged pipeline feeds object creation directly.
2. **Two mask gates, same dword** — `d[0x22D89B8]` is `bt`-tested at
   entry (kind argument) and again before the pool check (reloaded
   ST_W kind). Both hard-fail paths exist: entry clear → `jmp$`;
   pool-gate clear → `edi = 0` (check skipped, not an error).
3. **`kind_d > 0xE` is a real crash path** — the bound clamps the
   descriptor pointer to `0` and `q[0xA0]` dereferences it. There is
   no error return for an out-of-range kind.
4. **Retry is livelock-shaped, not a poll** — the loop re-reads the
   staged kind each pass and re-invokes the constructor; exit needs
   either a successful BC60 or "no work reported" (`esi == 0`,
   `edi == 0`). With a static kind and a failing allocator it spins
   forever — recorded as a bound, matching the `jmp$` convention.
5. **The descriptor table base is `0x22D7FD0`** — stride `0xA8`, 15
   kinds, fields `+0x50` pool ptr, `+0xA0` ctor, `+2`/`+0x62` live
   marks. Off by `0x1000` in the first static read — same class of
   slip as EXP-121's `0x2EC3EE0` table.
6. **`w[obj-2] = si` is always `0`** — `esi` is `xor`-cleared at
   `0x36A124` before either arm. The header's word field is a
   constant clear, proven by the `hdrfill` discriminating case.

## Mutation campaign

14 byte-precise mutations, every site verified against shipped bytes
before patching:

- **A100 (6):** kind cell disp `ST_W`→`QCOUNT` (BC60 gets the count —
  trace divergence); fallback `je`→`jne` (BFE0 success skips header
  writes); BFE0 arg disp `−1` (reads `d[0x22D89BB]` → mask bit0 fails
  → spin); staged-b2 cell disp `−1`; header dword disp `−0x10`→`−0x14`;
  header word disp `−2`→`−4` (needs `hdrfill` — a zero-write's
  misplacement is otherwise invisible).
- **BFE0 (7):** entry gate `jb`→`jae` (bit-clear proceeds); kind bound
  `0xE`→`0xD` (kind 0xE loses its descriptor → fault); desc stride
  `0xA8`→`0xA0` (callback cell misreads → `esi = 0` → no retry);
  pool disp `+0x50`→`+0x58`; live-flag byte `+2`→`+3`; pool gate
  `jae`→`jb` (set bit skips the pool check); retry `jne`→`je`
  (near-jcc; `esi != 0` no longer retries).
- **C620 (1):** `sub`→`add` (returns `base + ecx`).

**14/14 killed.** Two mutants needed discriminating fixtures:
`m-a100-je` only fires inside the fallback arm (`a100-direct` never
reaches it), and `m-a100-w2` writes a constant zero — observable only
against a nonzero `hdrfill` window.

## Limitations

- `0036BC60` (the 887 B allocator core), `0036AAD0`, `0036ABE0` are
  entry-intercepted scripted boundaries with planted returns —
  **not** native-proven here. BC60's own ten-callee subtree is the
  EXP-123 candidate.
- The `call rax` target is runtime-planted in shipped reality too
  (the descriptor table is BSS); planting it to the real FLAG leaf
  proves the dispatch executes in-image code, not which ctor the
  game installs.
- `bfe0-desc-hi`'s fault is recorded as a fault observation
  (address `0xA0`, insn `0x36C02D`, residual `rax = mask`) — the
  model predicts the faulting access, not a return.
- `bodies.json` holds body span + sha256 over shipped bytes for the
  three real bodies plus the indirect-call metadata for `0x36C03B`;
  instruction-start coverage convention matches EXP-107–121.
