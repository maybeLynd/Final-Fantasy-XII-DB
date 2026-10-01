---
experiment: EXP-121
title: EXP-109 queue/runtime helper tails — the staged lane queue, table
  resolver, clear pass, flag leaf and poll driver, executed real
contract: ../02-Resource-And-Asset-Pipeline/CONTRACT-resource-request-queue.md
method: B
live_game: false
tool: evidence/exp109-queue-tails-exec/check.py
---
# EXP-121 — exp109-queue-tails-exec

**Status:** complete · **27/27 functional cases, 22/22 mutants, stable
across three processes**
**Evidence:** `evidence/exp109-queue-tails-exec/` (`check.py`,
`bodies.json`, `gen_bodies.py`, `result.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

EXP-109 left a set of scripted thin-boundary helpers around the queue
and runtime-poll paths. This package executes the bounded nine:

| VA | role | execution |
|---|---|---|
| `0036C140` | C140 — LIFO pop into staging globals | **real** (84 B, 19 insns) |
| `0036C1D0` | C1D0 — caller-stack r9 thunk → C1F0 | **real** (20 B, 5 insns) |
| `0036C1F0` | C1F0 — lane-queue push from staging | **real** (150 B, 28 insns) |
| `0032E400` | E400 — pointer-table / 2D fallback resolver | **real** (80 B, 25 insns) |
| `0046DE70` | DE70 — jump thunk → T2D | **real** (5 B, 1 insn) |
| `002DF960` | T2D — `0x1388`-row 2D dword leaf | **real** (28 B, 7 insns) |
| `00512EF0` | CLR — flag clear + 32-entry and-lane/tag pass | **real** (50 B, 13 insns) |
| `0032E520` | E520 — poll driver (boolean path + zero-arg loop) | **real** (107 B, 32 insns) |
| `0046DFE0` | FLAG — state-flag leaf | **real** (18 B, 5 insns) |

Two disclosed scripted boundaries remain — `0032E070` and `0035EA30`,
the deep poll-loop callees inside E520's zero-arg path. They are
entry-intercepted (`e070:`/`ea30:` tokens) with planted returns driving
loop settlement; neither body executed, and they are **not** claimed
native-proven.

All queue/table/flag memory beyond the shipped globals themselves is
planted fixture (disclosed); the executed code and every global address
are the real shipped bodies and real RIP-relative targets.

## Measured semantics (native execution, not static reading)

**C140 `0036C140() -> eax`:**

1. `cnt = d[0x22D89C0]` — signed. `cnt <= 0` → `jmp $` at `0x36C150`,
   a **hard self-loop** (never re-reads the count; `pop-empty` and
   `pop-neg` end there permanently).
2. `cnt--` stored back; `el = 0x22D89D0 + (cnt)*16` — LIFO pop of the
   top 16-byte entry.
3. Copies `{w[el]→d[0x22D89BC], b[el+2]→d[0x22D8E18],
   q[el+8]→q[0x22D8E20], b[el+3]→d[0x22D8E28]}` into staging globals —
   the word/byte fields are stored as **dwords**.
4. Returns `zx8(b[el+3])` — the staged byte3 field.

**C1D0 `0036C1D0`:** `r9 = q[rsp+4] - 5` — a caller-stack read that
captures the qword overlapping the return address and the caller's
first spill slot — then `r8d = 0` and `jmp C1F0`. The fixture plants
the stack bytes; `r9` lands in `q[0x22D8E20]` staging.

**C1F0 `0036C1F0(ecx, edx, r8d=lane, r9) -> eax`:**

1. `cnt = sx32(d[0x22D89C0 + lane*4])`; `cnt >= 0x1F` → `jmp $` at
   `0x36C211` — another hard self-loop (`push-full` ends there).
2. `el = 0x22D89D0 + (lane*32 + cnt)*16` — lane `l` owns the
   `entries[l*32 .. l*32+31]` region of the same queue array C140 pops
   (lane 0). Writes `{staged w→w[el], staged b2→b[el+2],
   staged q→q[el+8], staged b3→b[el+3]}` and `cnt+1`.
3. Then **writes back staging**: `d[0x22D8E18] = edx` (arg2),
   `q[0x22D8E20] = r9` (arg4 — C1D0's caller-stack value),
   `d[0x22D89BC] = tag` where `tag = b[0x22D89A8 + sx32(ecx)]`.
   Returns `tag` (zero-extended).
4. `pop` + `push` compose a **stage-and-requeue pipeline**: `pop-push`
   pops entry 1 into staging then pushes it back at the tail slot —
   the same count, with staged fields rotated.

**E400 `0032E400(ecx, rdx) -> eax`:**

1. `ecx == 0xFF` → `or eax,-1` → returns `0xFFFFFFFF` — before any
   table access (`r400-ff`).
2. `ptr = q[0x22C51F0 + sx32(ecx)*8]`; if `ptr != 0 && rdx < 0x400`
   → returns **`d[ptr + rdx*4]` raw at `0x32E430` — the primary path
   never reaches the rounding code** (the first harness rev wrongly
   rounded it; native `r400-basic` returns `33`, not `64`).
3. Otherwise `call DE70` → `jmp T2D`:
   `eax = d[0x2EC3EE0 + (sx32(ecx)*0x1388 + sx32(edx))*4]` — a
   2D dword table with `0x1388` (5000) row stride. The static-read
   base `0x2EB3EE0` was off by `0x100000`; execution traces showed
   reads at `0x2EC8xxx` and RIP-relative decoding pins the true base
   at `0x2EC3EE0`.
4. Fallback only: `eax > 0` → round to 64 via
   `add 0x3F; cdq; and edx,0x3F; add; and ~0x3F` — a **signed-aware**
   rounding: sums that carry into bit31 get an extra `+0x3F` adjust
   before masking (`eax = 0x7FFFFFF0` → `0x80000040`, not
   `0x80000000`). `eax <= 0` → returned verbatim.
5. All arms return through `eax` → `rax` is **zero-extended**.

**CLR `00512EF0() -> rax`:** clears `b[0x2CA83F0]`, `b[0x2EBA481]`,
`b[0x2EBA480]`; then 32 iterations over `0x2CA81FF` (stride `0x10`):
`b[el] &= 0xF0` and `b[el-3] = loop_index` — a tag-byte clear plus
lane-index restamp. Returns `0x2CA83FF` (`CLRT + 0x200`) — the final
`lea` result, an address-looking value, not a status.

**E520 `0032E520(ecx) -> eax`:**

- `ecx != 0`: `ebx = (q[0x22C51C0] != 0)`; `call FLAG`; result
  `= (pollq != 0) | (flag() != 0)` — the `sete dil` + `xor edi,1`
  pair computes `flag() != 0` (`e520-nz-*` cases split all four
  combinations).
- `ecx == 0`: the poll driver — calls scripted `0032E070`, then loops
  on `pollq`/`flag()` invoking scripted `0035EA30` per pass, exiting
  when `pollq == 0 && flag() == 0` (`e520-zero-exit` settles in one
  pass; `e520-zero-spin*` verify the `jmp`-style re-test order).
  The loop re-test is `lea eax,[rcx+1]; cmp eax,1; jbe` on the
  **reloaded** `ecx` — inside the loop, not the entry.

**FLAG `0046DFE0() -> eax`:** `d[0x215EFF4] == -1` → `2`, else `0`
(`cmove`) — a tri-state leaf, not a boolean.

## Execution findings (beyond the static reading)

1. **The queue is one shared region, lanes are count-sliced** — a
   dword count array at `0x22D89C0` (4 B per lane) and 32-entry lane
   blocks at `0x22D89D0` (16 B per entry). C140 pops lane 0's top;
   C1F0 pushes to any lane — `push-lane2` uses lane 2's own count.
2. **Both queue ops hard-spin, not poll** — `jmp $` self-loops at
   `0x36C150`/`0x36C211`. A full lane or empty pop never re-reads the
   count; the caller must guarantee space.
3. **Push stages its own arguments** — `edx` and `r9` land in the
   same staging dwords pop fills, so `C1D0`'s caller-stack `r9`
   becomes the *next* staged qword — a pipeline register.
4. **E400's rounding is fallback-only** — the primary pointer-table
   path returns the raw dword. This is the finding the first model
   rev got wrong; five functional cases diverged until execution
   showed the `ret` at `0x32E430` precedes the rounding block.
5. **The 2D table base is `0x2EC3EE0`, not `0x2EB3EE0`** — off by
   exactly `0x100000` in the first static read; RIP-relative decode
   (`lea rax,[rip+0x2be456c]` at `0x2DF968`) is unambiguous.
6. **CLR returns an address** — `CLRT+0x200`, the residue of the
   pointer-walk `lea`, not a status code.

## Mutation campaign

22 byte-precise mutations, every site verified against shipped bytes
before patching:

- **C140 (4):** count disp; `jg`→`jge` (cnt=1 spins); `dec`→`inc`
  (pops the wrong end); entry `*8`-scale byte.
- **C1D0/C1F0 (6):** `sub 5`→`add 5` (r9 low bits); `shl r10,5`→`shl 4`
  (lane-2 entry lands at index 33 not 65); count bound `0x1F`→`0x1E`;
  entry strides `*16`→`*8` and `*2`; count-store `lea eax,[r8+1]`→`+2`.
- **E400/T2D (6):** `0xFF`→`0xFE` sentinel; ptab `*8`→`*4`; bound
  `0x400`→`0x200` (`rdx=0x300` falls to the 2D path); table `*4`→`*8`;
  `jle`→`jmp` (rounding skipped); `~0x3F`→`~0x7F`; T2D row `0x1388`→
  `0x1390`.
- **CLR (3):** `&0xF0`→`&0xF8`; index store→`index+1`; iter bound.
- **FLAG (1):** `cmove`→`cmovne` (`flag-set` returns 0).
- **E520 (2):** `setne`→`sete` (needs `ebx=1, dil=0` — `e520-nz-both`);
  `xor edi,1`→`xor edi,0` (dil stays raw — `e520-nz-q0f2`).

**22/22 killed.** Two mutants needed case surgery to discriminate:
`m-e520-sne` is invisible when `flag()` returns nonzero (the `or`
masks it), and `m-push-lane` needed a per-lane count plant — a lane-0
count leaves lane 2's count at shipped `0`, moving the write outside
the watched entry.

## Limitations

- `0032E070` and `0035EA30` are entry-intercepted scripted boundaries
  with planted returns driving E520's loop settlement — **not**
  native-proven here.
- All queue entries, pointer tables, 2D-table cells and flag words
  are planted fixture; the executed bodies, all RIP-relative global
  addresses, and the untouched shipped bytes at those addresses are
  real. Model image reads fall back to shipped bytes where a case
  does not plant.
- Spin cases (`pop-empty`, `push-full`, `e520-zero-spin`) are
  recorded as final-RIP/ends observations at the `jmp $` sites —
  termination is by the harness's instruction bound, matching the
  bodies' non-terminating semantics.
- `bodies.json` holds body span + sha256 over shipped bytes for all
  nine real bodies; instruction-start coverage convention matches
  EXP-107–120.
