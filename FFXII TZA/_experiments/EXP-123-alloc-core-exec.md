---
experiment: EXP-123
title: allocator core — the 887 B intrusive free-list allocator
  0036BC60 and its full callee tree, executed real
contract: none — the executed subject is the general allocator core
  0036BC60 and its full callee tree; the allocator family
  00369860–0036C900 has no contract — its documentation home is the page
  24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md.
  The previous key named the render-record-pool contract, whose own §13
  declines this record (the intersection is the two shared helpers
  0020E600/0020E620, three instructions each)
method: B
live_game: false
tool: evidence/alloc-core-exec/check.py
---
# EXP-123 — alloc-core-exec

**Status:** complete · **28/28 functional cases, 30/30 mutants, stable
across three processes**
**Evidence:** `evidence/alloc-core-exec/` (`check.py`, `bodies.json`,
`gen_bodies.py`, `result.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

EXP-122 scripted `0036BC60` — the 887 B / 246-insn allocator core at
the centre of the `0036A100` family — on a stale first-return census.
This package executes the core **and its entire callee tree** as real
shipped code:

| VA | role | execution |
|---|---|---|
| `0036BC60` | BC60 — allocator core | **real** (887 B, 246 insns) |
| `0036A490` | A490 — block-header initialiser | **real** (215 B, 60 insns) |
| `0036B210` | B210 — back+fwd coalesce, root fix | **real** (161 B, 47 insns) |
| `0036B2C0` | B2C0 — forward coalesce | **real** (319 B, 94 insns) |
| `0036B5F0` | B5F0 — page-head min-addr insert | **real** (124 B, 37 insns) |
| `0036B670` | B670 — list-1 splice-after | **real** (179 B, 50 insns) |
| `0036B730` | B730 — list-1 splice-before | **real** (179 B, 50 insns) |
| `0036B7F0` | B7F0 — phys-list splice-after | **real** (179 B, 50 insns) |
| `0036B8B0` | B8B0 — phys-list splice-before | **real** (179 B, 50 insns) |
| `0036C900` | C900 — page-head remove + bitmap | **real** (198 B, 60 insns) |
| `0036C9D0` | C9D0 — intrusive-list unlink | **real** (253 B, 71 insns) |
| `0020E600` | BASE — pointer decoder | **real** (10 B, 3 insns) |
| `0020E620` | C620 — BASE-inverse encoder | **real** (9 B, 3 insns) |
| `0036A570` | A570 — corruption diagnostic dump | scripted (entry token) |

Two disclosed boundaries: **A570** is entry-intercepted (the
mask-gated diagnostic body is not executed; the token records its
`ecx`/`edx` args), and the shared hook cell `q[0x8C2D80]` ships as
`0x1CCF02C`, an rdata pointer — a dormant cell, not code (erratum:
this record originally said `0`; corrected by EXP-126's cell dump).
The fixture plants it to FLAG `0046DFE0` (a real shipped leaf),
so the corrupt-path indirect call runs real code before the `int3`
trap. All BSS globals (kind mask, queue count, tag epoch, staged
bytes, codec cell, descriptor table, page table, bitmap) are planted
fixture, disclosed; every executed instruction and every global
address is real.

## Measured semantics (native execution, not static reading)

**The allocator is an intrusive doubly-linked-list allocator**, not
the BST the first census suggested. Each free block is a 0x40-byte
header:

| off | field |
|---|---|
| `+0x00` | magic `0xFF12` live / `0xFF99` unlinked (C9D0 stamp) |
| `+0x03` | owner kind byte |
| `+0x04/+0x08` | list-1 prev/next — **address-ordered** free list |
| `+0x0C/+0x10` | list-2 prev/next — **physical-adjacency** list |
| `+0x14` | flag byte (bit0 = allocated) |
| `+0x15` | secondary flags (`arg4` bit, `8` when `d[0x22D8E28]`) |
| `+0x16` | tag byte |
| `+0x18` | block size key (payload capacity; extent = key + 0x40) |
| `+0x3E` | sequence/mark word — nonzero → corruption path |

All links are **BASE-encoded** (`d[link] = ptr − arena`); the fixture
plants `q[0x1F83530] = 0` so encoded links are raw u32 pointers.
`q[desc+0x90]` and `q[desc+0x98]` are the **head and tail of the
same `+4/+8` free list** — the two search arms walk one list from
opposite ends under an identical `key >= size` predicate, and B210's
root repair writes both cells from one survivor's list-1 links
(`prev == 0 → +0x90`, `next == 0 → +0x98`). No descriptor root for
the `+0xC/+0x10` physical-adjacency pair was observed; how that
chain is anchored remains **open**.

**BC60 `0036BC60(ecx=kind, edx=size, r8=ctx, r9d=arg4) -> rax`:**

1. `ctx == 0 && d[0x22D89C0] == 0` → `jmp $` at `0x36BC87` — a hard
   spin on an empty queue (`bc60-spin`).
2. `r14 = align64(max(edx,0))` — `cdq`-corrected `+0x3F`, `& 0xFFFFFFC0`
   (`bc60-neg-size` proves the `cmovns` clamp; `bc60-align` proves the
   addend carries `0x41` over the boundary).
3. `desc = 0x22D7FD0 + kind*0xA8` for `kind <= 0xE`, else `0` →
   `b[desc+2] = 1` faults at `0x2` for out-of-range kind
   (`bc60-kind-hi` records the fault; `bc60-kind-e` proves 0xE lives).
4. `ctx == 0` → mask gate `bt(d[0x22D89B8], kind&0x1F)` (clear → return
   0, `bc60-maskclr`), then **first-fit-by-address** walk: `arg4 == 0`
   walks `+8` links from `q[desc+0x90]` head forward; `arg4 != 0`
   walks `+4` links from `q[desc+0x98]` tail backward — first node
   with `key >= r14` wins. Tag = `d[0x22D8E1C]`. `ctx != 0` carves the
   caller node directly with tag `b[ctx+0x16]` (`bc60-direct`).
5. **Carve** — `rem = key − r14 − 0x40`:
   - `arg4 == 0` (front): `rsi = node` alloc header, `rbp = node +
     0x40 + r14` remainder header.
   - `arg4 != 0` (tail): `rsi = node + key − r14` alloc header,
     `rbp = node` remainder.
   - `rem < 0` → `rbp = 0`; roots `head = next(+8)`, `tail = prev(+4)`
     when they pointed at the carved node. `rem >= 0` →
     `head = tail = rbp` under the same guard.
6. `C900(desc, node)` page-remove, `C9D0(node, 1)` unlink both lists
   (stamps `0xFF99`), `A490(kind, rsi, r14, seq)` then
   `A490(kind, rbp, rem, seq)` — the remainder header is **rewritten
   in place** over the `0xFF99` stamp.
7. `b[rsi+0x15] |= arg4 & 0xFF`, `b[rsi+0x14] |= 1`, `b[rsi+0x16] =
   tag`, `w[rsi+0x3E] = 0`; `rbp` gets `b[+0x14] &= ~1`, `w[+0x3E]=0`,
   `B5F0(desc, rbp)` page-insert.
8. **Re-splice** (shared tail at `0x36BF1C` for both carve modes):
   - phys pair: `arg4 == 0` inserts `rsi` after `+0xC`-prev /
     before `+0x10`-next (no neighbour → **zero both roots**), then
     `B7F0(rsi, rbp)`. `arg4 != 0` splices `rbp` after `+0xC`-prev
     then `rsi` after `rbp` — mirrored `B8B0` order for `+0x10`-next;
     `rbp == 0` splices `rsi` only.
   - list-1 pair: `prev1 ? B670(prev1, rbp) : next1 ? B730(next1, rbp)`.
   - **`B210(desc, rbp)` always runs when `rbp != 0`** — the remainder
     immediately back+forward-coalesces; the merged survivor fixes
     `head`/`tail` and gets `b[+0x14] &= ~1`, `w[+0x3E] = 0`.
9. `d[desc+0x68 + sx32(tag)*4] += r14` — per-tag usage counters;
   `w[desc+0x60]++` — descriptor sequence; return `rsi + 0x40`.
   Not-found path still bumps the sequence (`bc60-empty` → `5 → 6`).

**The zero-roots arm is a list-emptying**, not an error: after the
carve node is unlinked, `B210` re-establishes `head`/`tail` from the
merged remainder — `bc60-head-split` final state `head = tail = rbp`
arrives *through* the zero+coalesce sequence, not around it.

**A490 `0036A490(ecx=kind, rdx=blk, r8d=size, r9d=seq)`:** stamps
`0xFF12`, kind at `+3`, `0xFF` at `+2`, clears all four encoded links,
`size` at `+0x18`, `seq` at `+0x1C`, `b[+0x15] = 8` iff
`d[0x22D8E28] != 0`, clears `+0x14`/`+0x1E`/`+0x20…+0x30`/`+0x34`/`+0x3C`.

**C9D0 `0036C9D0(rcx=node, edx=flag)`:** unlinks `+4/+8` pair
(prev.next/next.prev swap with `w[+0x3E]` clears), nulls node's
pair-1; `flag != 0` also unlinks `+0xC/+0x10`, stamps `0xFF99`,
nulls pair-2. `w[node+0x3E] = 0` last.

**B210/B2C0 — coalescing:** B2C0 walks `+8` (list-1 next) while
`+0x10` (phys next) points at the same node — that *is* the
adjacency test: the list-1 successor being also the physical
successor means the blocks are contiguous. Each merge: `C900` page
evict, `C9D0` unlink, `survivor.key += victim.key + 0x40`. B210 first
back-walks `+4`/`+0xC` pairs the same way, coalesces from the
earliest contiguous predecessor, then repairs roots:
`prev == 0 → head`, `next == 0 → tail`, `b[+0x15] = 0`.

**B5F0/C900 — the page table:** `slot = (blk − q[desc+0x10]) >> 16`
with signed-16 `cqo`/`movzx` floor semantics (negative deltas
round toward `-∞`, `pslot` discriminates). `q[desc+0x28]` is a qword
array of per-64KiB-slot **lowest-addressed** block heads; `q[desc+0x20]`
is a dword bitmap (`slot&0x1F` bit, `slot>>5` word). Insert keeps the
lower head (`b5f0-min`/`b5f0-keep`); remove promotes the `+8` next
only if it lives in the same slot, else clears the bit
(`c900-swap`/`c900-clear`).

**The four splice twins** are exactly 179 B / 50 insns each —
`B670/B730` operate on `+4/+8` (list-1), `B7F0/B8B0` on `+0xC/+0x10`
(phys), `after`/`before` variants. Each clears `w[+0x3E]` on every
touched node. Residual `rax`: `c620(old next)` for after-splices,
`c620(anchor)` for before-splices.

**Corruption path:** `w[blk+0x3E] != 0` on any twin entry →
`A570(ecx = d[0x22D89BC], edx = 0xB)` (scripted) → `ecx = 1;
call q[0x8C2D80]` (planted FLAG leaf, real) → `int3` at
`0x36B6AE/0x36B76E/0x36B82E/0x36B8EE` — recorded as a trap whose
residual rip lands one past the `int3` (`b670-corrupt` ends at
`0x36B6AF`).

## Execution findings (beyond the static reading)

1. **`arg4` selects the carve end, not the splice shape** — the
   list-1 splice and `B210` coalesce run for *both* modes through the
   shared `0x36BF1C` tail; the first harness revision coalesced only
   for `arg4 != 0` and diverged on every front-carve split.
2. **`head`/`tail` roots are raw pointers, links are BASE-encoded** —
   `q[desc+0x90/0x98]` hold decoded node addresses while `+4/+8`
   fields hold offsets. The mixed codec is real, verified by trace.
3. **The rem<0 root writes are QWORD, the arg4≠0 no-neighbour zero
   is DWORD+qword** — `mov q[rbx+0x90],rax` vs `mov d[rbx+0x90],ebp`
   at `0x36BFA0`; the asymmetric width is a real byte distinction.
4. **Coalescing runs eagerly on every split** — a tail-carve
   remainder contiguous with its predecessor is absorbed in the same
   call (`bc60-coalesce`: NP `key 0x40 → 0xC0`, victim stamped
   `0xFF99`, alloc lands at `N1+0xC0`).
5. **List-1 is address-ordered** — the page-head table stores the
   lowest-addressed block per 64 KiB slot; `C900` promotes the `+8`
   next only within the same slot. First-fit-by-address is the
   allocation policy.
6. **`bc60-two-second` proved the splice writes the remainder, not
   the node** — `N1+8 = N2+0x140` (node + 0x40 + size) showed the
   remainder's address entering list-1 where the carved node had been.
7. **The sequence word `w[desc+0x60]` ticks on every call** — success,
   not-found, and both header inits read it for `+0x1C` stamps; the
   per-tag usage cell `+0x68+tag*4` takes `r14` bytes.
8. **The hook cell `q[0x8C2D80]` ships as `0x1CCF02C`** — an rdata
   pointer, dormant in the shipped image (erratum: originally recorded
   as `0`; the planted-FLAG decision is unaffected — calling into
   rdata faults either way). All four twins call through the same cell
   on the corruption path; the fixture plants the real FLAG leaf so
   the indirect executes shipped code.

## Mutation campaign

30 byte-precise mutations, every site verified against shipped bytes
before patching:

- **BC60 (21):** gate cell `QCOUNT`→`ST_W` (spins on live queue);
  gate `jne`→`je`; align addend `0x3F`→`0x3E` (size `0x41` under-allocates);
  align mask `0xC0`→`0xE0`; kind bound `0xE`→`0xD` (kind 0xE faults);
  desc stride `0xA8`→`0xA0`; live-mark `+2`→`+3`; mask cell disp `−1`;
  mask `jb`→`jae`; key disp `+0x18`→`+0x1C`; found `jge`→`jl` (walks
  past the fit); walk link `+8`→`+4` (walks the wrong pair); remainder
  `+0x40`→`+0x30`; remainder `−0x40`→`−0x30`; exact-fit root write
  `+0x90`→`+0x98`; `arg4` OR `+0x15`→`+0x14`; alloc bit `+0x14`→`+0x15`;
  tag `+0x16`→`+0x15`; usage `+0x68`→`+0x6C`; seq `+0x60`→`+0x62`;
  return `+0x40`→`+0x38`.
- **A490 (4):** magic `0xFF12`→`0xFF13`; seq `+0x1C`→`+0x1E`; size
  `+0x18`→`+0x1C`; `0xFF99` stamp `0x99`→`0x98`.
- **C9D0 (1):** flag `je`→`jne` (pair-2 unlink on the wrong arm).
- **B5F0 (2):** slot `sar 0x10`→`0x11` (64 KiB → 128 KiB slots);
  replace-arm bitmap `or`→`and` (clears instead of sets).
- **B670 (1):** corruption check `+0x3E`→`+0x3C` (marker invisible —
  the corrupt node splices normally; trace/end divergence).
- **B2C0 (1):** merge size `+0x18`→`+0x1C`.

**30/30 killed.** Three mutants needed discriminating fixtures:
`m-root-off` is masked by the no-neighbour zero-roots arm (needed a
phys predecessor in `bc60-exact-phys`); `m-bitmap-op` targets the
*replace* arm's `or` at `0x36B668`, not the insert arm's; `m-align-add`
needs a size `≡1 (mod 64)` to carry over the boundary.

## Limitations

- `0036A570` (729 B, the mask-gated corruption diagnostic) is
  entry-intercepted — its `ecx`/`edx` args are recorded, its body is
  **not** native-proven here.
- `q[0x8C2D80]` is runtime-planted in shipped reality too (ships as
  `0x1CCF02C`, an rdata pointer — dormant, not code); planting it to
  the real FLAG leaf proves the dispatch executes in-image code, not
  which hook the game installs.
- All block headers, the pool base, page table, bitmap, and BSS
  globals are fixture-planted; CODEC `= 0` makes encoded links raw
  u32 pointers — the codec itself is real code, its *base value* is
  planted (the EXP-083-proven valid configuration).
- `bc60-kind-hi`'s fault is recorded as a fault observation
  (access `0x2`, insn `0x36BCC5`, residual `rax = size + 0x3F`) — the
  model predicts the faulting access, not a return.
- The corrupt-path trap is recorded with residual rip = int3 site + 1;
  A570's own diagnostic effects are disclosed as scripted.
- `bodies.json` holds body span + sha256 over shipped bytes for the
  thirteen real bodies plus the indirect-call metadata for the four
  `call q[0x8C2D80]` sites; instruction-start coverage convention
  matches EXP-107–122.
