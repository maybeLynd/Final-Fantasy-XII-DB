---
experiment: EXP-125
title: pool-adoption layer — the compacting-allocator move scan
  0036AAD0/0036ABE0, adopt-one 0036A2A0, the keyed pool BST helpers,
  and the A570/A850 diagnostics, executed real
contract: none — the executed subject is the allocator's pool-adoption
  (compaction) layer 0036AAD0/0036ABE0/0036A2A0 plus diagnostics; the
  allocator family 00369860–0036C900 has no contract — its documentation
  home is the page
  24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md.
  The keyed BST helpers 0036B410/0036B4E0/0036C790 executed here are
  shared callees — they are CONTRACT-resource-entry-tree.md's own
  entries, already executed in that scope by EXP-083, so filing this
  record there would double-count. The previous key named the
  render-record-pool contract, whose own §13 declines this record
  (shared helpers 0020E600/0020E620 only)
method: B
live_game: false
tool: evidence/alloc-pool-adoption-exec/check.py
---
# EXP-125 — pool-adoption-exec

**Status:** complete · **43/43 functional cases, 34/34 mutants, stable
across three processes**
**Evidence:** `evidence/alloc-pool-adoption-exec/` (`check.py`,
`bodies.json`, `gen_bodies.py`, `result.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

EXP-122/123 left four scripted boundaries in the allocator family:
the AAD0/ABE0 callers of `0036A2A0`, the `004746F0`/`00369860` payload
helpers inside A2A0, and the A570 corruption diagnostic. This package
executes the **pool-adoption (compaction) layer** end to end — the two
adoption scans, the adopt-one body (which drives the real EXP-123 BC60
carve), the keyed pool-BST helpers, and both diagnostic bodies:

| VA | role | execution |
|---|---|---|
| `0036AAD0` | AAD0 — BST-scan adoption vs free-list head | **real** (261 B, 83 insns) |
| `0036ABE0` | ABE0 — per-free-node adoption walk | **real** (243 B, 73 insns) |
| `0036A2A0` | A2A0 — adopt-one (move + ctx carve) | **real** (495 B, 138 insns) |
| `0036C790` | C790 — BST unlink + subtree re-attach | **real** (359 B, 100 insns) |
| `0036B410` | B410 — BST insert entry | **real** (124 B, 37 insns) |
| `0036B4E0` | B4E0 — keyed BST descend-and-insert | **real** (177 B, 52 insns) |
| `0036B490` | B490 — force left-child attach | **real** (71 B, 21 insns) |
| `0036B5A0` | B5A0 — force right-child attach | **real** (71 B, 21 insns) |
| `0036A570` | A570 — mask-gated allocator diagnostic | **real** (729 B, 189 insns) |
| `0036A850` | A850 — BST label-format walk | **real** (382 B, 92 insns) |
| `0036BC60` + 10 | BC60 + EXP-123 helper tree (ctx carve inside A2A0) | **real** (EXP-123 bodies) |
| `0020E600`/`0020E620` | BASE decoder / C620 encoder | **real** |
| `0046DFE0` | FLAG — planted output-hook target | **real** (18 B, 5 insns) |
| `00808C40` | CHKCK — `__security_check_cookie` | **real** (60 B, 18 insns) |

Scripted boundaries (entry-intercepted, args traced, NOT executed):
`00369860` (PREL — deep payload-release diagnostic; contains a nested
deep call chain) and `004746F0` (PINIT — deep float/payload copy).
Both return values are dead at their call sites, so the boundary does
not mask observable state.

Indirect-call disclosure: the diagnostic output hook `q[0x8C2F70]`
ships pointing at `0x1CCEF16`, which decodes as rdata, not code — a
dormant cell. The fixture plants it to FLAG `0046DFE0` (a real shipped
leaf) so A570's `call qword [rip+disp]` at `0x36A6FA` dispatches real
code; the leaf is pure (`cmove` residual only, no writes). The EXP-123
hook cell `q[0x8C2D80]` (ships rdata ptr `0x1CCF02C` — dormant,
non-code; EXP-123's "ships 0" corrected by EXP-126) is likewise
planted to FLAG for the
twin corrupt paths, though no EXP-125 case reaches them.

All BSS globals (kind mask, queue count, tag epoch, descriptor table,
page table, bitmap, index-table base, pool-BST root, per-tag counters)
are planted fixture, disclosed; every executed instruction and every
global address is real.

## Measured semantics (native execution, not static reading)

**The allocator is a compacting allocator.** The adoption layer moves
live pool blocks *down* into lower-addressed free blocks:

- **AAD0** (`0036AAD0`) takes `(rcx=desc, edx=repeat)`. It reads the
  free-list head `q[desc+0x90]`, then descends the keyed pool BST at
  `q[desc+0x50]` (children `+0x24` smaller / `+0x28` larger-or-equal,
  parent `+0x2C`, all BASE-encoded). On a node with `key ==
  d[head+0x18]`, `addr > head` (unsigned), and `!(f15 & 4)`, it calls
  A2A0 and counts it. `edx != 0` re-reads the head and rescans;
  `edx == 0` returns after one adoption. The `<`-arm's best-candidate
  tracking register is **dead** — computed but never consumed.
- **ABE0** (`0036ABE0`) walks the free list via `+8`. For each node it
  reads the physical next `BASE(d[rdi+0x10])`: if `(b[+0x15] & 6) == 2`
  *and* `b[+0x14] & 1`, it adopts **the phys-next block itself** —
  the `jne` at `0x36ACBF` skips the `mov r8,rbx` reload so `r8`
  survives as the phys-next pointer. If the flag is set but the block
  is free, the whole scan returns 0 immediately (it does not fall
  through to the BST scan). Otherwise it BST-scans for `key ==
  d[rdi+0x18]`, `addr > rdi`, `!(f15 & 4)`, adopts on hit, else
  advances.
- **A2A0** (`0036A2A0`, `(rcx=desc, rdx=free-node, r8=pool-src)`)
  performs the move: snapshots the source trailer (`+0x14/+0x15/+2/
  +3/+0x16/+0x17/+0x1E/+0x30`) and label string (`+0x34`); if `f15 & 2`
  unlinks the source from the pool BST via C790; splices `rbx` into
  the threaded chain after `BASE(d[src+0x20])` (`q[rsi+8]=rbx`,
  `d[rbx+0x20]=C620(rsi)`, `w[rsi+6]=w[rbx+0x1C]`); bumps
  `d[0x22D8E10 + b[src+0x17]*4] += d[src+0x18]`; calls the scripted
  PREL/PINIT payload pair; then runs **the real BC60 ctx-carve**
  `BC60(b[desc+1], src-key, rbx, 0)` — the free node is carved in
  place with kind from the descriptor and tag from `b[rbx+0x16]`.
  Finally it copies the snapshot + label over the fresh header,
  re-inserts `rbx` into the BST when `f15 & 2` (cleared → B410 →
  re-set), re-splices the chain, clears `w[rbx+0x3E]`, and returns.
- **C790** (`0036C790`) is a BST unlink with subtree re-attach:
  root-node arms promote right (then re-attach left under it via
  B4E0) or left, or clear the root; child-node arms re-attach the
  left subtree under the right child via B4E0 and fix the parent's
  slot, or force-attach the left subtree via B490 (`+0x24` arm) or
  B5A0 (`+0x28` arm). The `r8d` tag constants (`0x4AA`, `0x4BF`,
  `0x4DF`, `0x4E3`, `0x14B6`, `0x14E5`, `0x50E`) are dead diagnostic
  line-IDs — confirmed unused.
- **B4E0** (`0036B4E0`) descends `+0x24` while `anchor.key > node.key`
  (signed compare), else `+0x28`; inserts as a leaf and back-links
  `+0x2C`. **B410** (`0036B410`) nulls a node's three links + clears
  `w[+0x3E]` then inserts under `q[desc+0x50]` (empty root → node
  becomes root). **B490/B5A0** force-attach a child into the named
  slot with parent back-link and `w[+0x3E]` clears.
- **A570** (`0036A570`, `(ecx=kind, edx=flags, r8d=sel)`) is the
  corruption-diagnostic dumper the EXP-123 twins call before `int3`:
  `bt(d[0x22D89B8], kind)` mask gate (silent return on clear), kind
  bound `<= 0xE` (else `q[0x10]` deref fault), then flag-selected
  walks — `&1` the pool chain via `+0x10` with a `+8` self-loop check
  and the `M2/U`-`FREE` label grid + `sel` match + output hook on
  `w[+0x1E] != 0 || b[+0x34] != 0`; `&2` the free list via `+8`;
  `&8`/`&0x10` the two 16-byte index tables at `q[desc+0x48]` /
  `q[desc+0x40]` over `q[desc+0x30]`; `&0x20` calls A850 on the BST.
- **A850** (`0036A850`) builds the same label strings (plus `/I`/`/C`
  suffix) on the stack for every BST node in pre-order — and
  **discards them**; no output call, so its only observable behaviour
  is traversal order and the faults a corrupt tree would produce.

## Execution findings beyond the static reading

1. **ABE0's flag arm adopts the phys-next node, not a scanned
   candidate** — the `jne 0x36AC8F` at `0x36ACBF` jumps *past* the
   `mov r8,rbx` at `0x36AC8C`, so `r8` keeps the phys-next pointer.
   The first reading predicted a stale-register quirk; execution
   proved the physical-adjacency fast path.
2. **The `+0x28` arm of C790 is a separate body, not B490** — the
   second force-attach calls `0036B5A0`, a 71 B twin that writes
   `d[parent+0x28]` instead of `+0x24`. Static reading of the tag
   constants (`0x4DF`/`0x4E3`) suggested two B490 call sites; the
   second is B5A0.
3. **A2A0's carve is the real BC60 ctx path** — `r9d=0` (front carve),
   `r8=rbx`, `edx=d[src+0x18]` (the *source* key is the carve size,
   not the free node's key), `ecx=b[desc+1]`. The free node's own key
   only matters to the scan eligibility tests.
4. **Residual returns are live register values, not status codes** —
   A2A0 returns `w[rbx+0x1C]` (the fresh sequence stamp) when the
   re-splice arm runs, the label-copy `NUL` residual (`0`) otherwise;
   C790 returns `0` on the child+right arm (`xor eax,eax` tail) but
   the B490/B5A0 `C620` residual on the left-only arm; A570 returns
   the last walk's decode/`cur_idx`/`DTAB`/`MASKG` value depending on
   which flag arms ran.
5. **`w[rsi+6]` is a real overlapping word field** — the chain seq
   write at `+6` overlaps the `+4` dword link's high half; free nodes
   and pool-chain nodes use the bytes differently (the harness's
   first fixture clobbered `prev`'s high word and produced a real
   `0x36CA32` write fault — the trace pinned it).
6. **AAD0's repeat arm can fault on a legal re-read** — after an
   adoption empties the free list (exact-fit carve, no phys
   neighbours → roots zeroed), the `edx != 0` rescan reads
   `d[0x18]` and faults at `0x36AB16`.
7. **The output-hook cell is dormant in the shipped image** —
   `q[0x8C2F70] = 0x1CCEF16` decodes as rdata. The planted FLAG leaf
   makes the dispatch real; its only effect is the `cmove` residual.
8. **GS cookie residuals are modelled, not guessed** — fault paths
   inside A2A0/A850 return `cookie ^ rsp` measured per-frame
   (`0x2B994CD85D6A` / `0x2B994CD85FAA`).

## Mutation campaign

34 byte-precise mutants, all killed. Coverage: the BST descend
directions (`+0x24`/`+0x28`), the head-key compare and `jle`/`jbe`
eligibility, the `f15&4`/`f15&6`/`f14&1` flag gates, the repeat flag,
the `+0x10`/`+8`/`+0xC` link offsets, the `+0x20` chain and `+0x50`
root, the counter index (`+0x17`) and seq copy (`+0x1C` post-carve
site), the BC60 arg `b[desc+1]`, the parent/left/right/root writes in
C790, the force-attach slots in B490/B5A0, the mask gate, kind bound,
print gate (`w[+0x1E]`), self-check, advance, `0xFFFF` sentinel and
`&0x20` arm in A570, and A850's left-recurse offset. Two survivors
needed repointing during bring-up: `m-a2a0-seqcp` first hit the
pre-carve seq read (masked by the post-carve overwrite — moved to
`0x36A460`), and the ABE0 mask/`cmp` pair needed `f15=6`/`f15=4`
fixtures to discriminate.

## Limits / boundaries

- `00369860` and `004746F0` are scripted boundaries — payload release
  and deep float copy. Their returns are dead at both call sites.
- The output hook `q[0x8C2F70]` is a fixture-planted dispatch to a
  real leaf; its shipped rdata target is disclosed above.
- A850's stack-built label strings are unobservable — only traversal,
  faults and residuals are modelled.
- No EXP-125 case reaches the twin corrupt path (`w[+0x3E] != 0` →
  A570 → hook → `int3`); A570 is proven as an entry point instead.
- `CODEC` is planted 0 (links raw), the EXP-083-proven valid
  configuration; non-zero codecs are not exercised.
- `r8d` tag arguments are confirmed dead but not exhaustively varied.

## Board routing

- Audit request → `SWE2-AUDIT-SPEC`
- Findings request → `OPUS`
- Publication queued → `EXP124-PUB`
