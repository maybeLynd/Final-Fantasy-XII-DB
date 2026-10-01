---
experiment: EXP-126
title: allocator free/release path — PREL 00369860, the AE00/ACE0
  find-free pair, the emit wrapper F17D2E0, _chkstk 00808F10, and the
  PINIT/memcpy thunk, executed real
contract: none — the executed subject is the general allocator's
  free/release path 00369860 and its find-free pair; the allocator
  family 00369860–0036C900 has no contract — its documentation home is
  the page
  24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md.
  The previous key named the render-record-pool contract, whose own §13
  declines this record (the intersection is the two shared helpers
  0020E600/0020E620, three instructions each)
method: B
live_game: false
tool: evidence/alloc-free-path-exec/check.py
---
# EXP-126 — alloc-free-path-exec

**Status:** complete · **82/82 functional cases, 71/71 mutants, stable
across three processes**
**Evidence:** `evidence/alloc-free-path-exec/` (`check.py`,
`bodies.json`, `gen_bodies.py`, `result.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

EXP-125 left two scripted cells inside A2A0's adopt-one body:
`00369860` (PREL — the allocator's free/release path) and `004746F0`
(PINIT — a `memcpy` wrapper). This package executes the free path end
to end — including the find-free-below/above lookup pair it calls, the
diagnostic emit wrapper, `_chkstk`, and the real IAT thunk — closing
the last non-native cells in the allocator family:

| VA | role | execution |
|---|---|---|
| `00369860` | PREL — free/release path | **real** (1009 B, 246 insns) |
| `0036AE00` | AE00 — find-free-at-or-below | **real** (287 B, 94 insns) |
| `0036ACE0` | ACE0 — find-free-at-or-above | **real** (286 B, 90 insns) |
| `0017D2E0` | EMIT — diagnostic emit wrapper | **real** (91 B, 27 insns) |
| `0016D670` | GETOBJ — emit object getter leaf | **real** (8 B, 2 insns) |
| `00808F10` | `_chkstk` — stack probe | **real** (81 B, 25 insns) |
| `004746F0` | PINIT — `memcpy` wrapper | **real** (26 B, 9 insns) |
| `00861EBA` | IAT thunk → `VCRUNTIME140!memcpy` | **real** (6 B, 1 insn) |
| `0036AAD0`/`0036ABE0`/`0036A2A0` | adoption layer (re-executed; A2A0 now calls real PREL/PINIT) | **real** |
| `0036C790` + pool-BST helpers | BST unlink/insert/attach | **real** |
| `0036A570`/`0036A850` | diagnostics | **real** |
| `0036BC60` + 10 | BC60 + EXP-123 helper tree | **real** |
| `0020E600`/`0020E620` | BASE/C620 codec leaves | **real** |
| `0046DFE0` | FLAG — planted hook target | **real** |
| `00808C40` | `__security_check_cookie` | **real** |

Scripted boundary (entry-intercepted, traced, NOT executed):
`VCRUNTIME140.dll!memcpy` — reached through the **real** PINIT body and
the **real** `00861EBA` thunk jumping through the real IAT cell
`q[0x8C2A68]`; the cell is planted to a trampoline at `0x63000000` so
the copy is observable (`memcpy:dst:src:n` token). The import body
itself is external code and stays disclosed-scripted.

## Planted cells — all dormant in the shipped image

- `q[0x8C2D80]` — PREL/twin corrupt-path hook. Ships `0x1CCF02C`, an
  rdata pointer (**EXP-123 erratum**: that record said `0`; the
  planted-FLAG decision is unaffected — calling into rdata faults
  either way).
- `q[0x8C2F08]` — EMIT's output-hook cell. Ships `0x1CCECB4` (rdata).
- `q[0x8C2F70]` — A570's output hook. Ships `0x1CCEF16` (rdata).
- `q[0x2E39ED0]` — EMIT's output-object global. BSS, planted.
- `gs:[0x10]` — `_chkstk`'s stack-limit read. Fake TEB at `0x6F000000`
  via `UC_X86_REG_GS_BASE`.

All BSS globals (mask, counters, descriptor table, page table, bitmap,
index table, BST root) are planted fixture, disclosed; every executed
instruction and every global address is real.

## Measured semantics (native execution, not static reading)

**PREL** (`00369860`, `(rcx=payload, rdx=aux)`) is the allocator's
free path:

- `_chkstk` over a `0x1168` frame, then the GS cookie.
- `rcx == 0` → return 0.
- `rcx & 3` → emit `"%p might be MHANDLE from %p"` (buf `rsp+0x40`),
  return.
- `w[rcx-0x40] != 0xFF12` → **bad-magic abort**: dump `0xB0` header
  bytes then `0xD0` aux bytes — one `emit("%02x ", rsp+0x30)` call per
  byte plus a `w[0x8F3F58]` separator word (`0x000A`) appended every
  16th byte and a `"\nSTACK\n\0"` qword tail between the two dumps;
  then `emit("CannotFreeIlligalAdrs %p from %p\n%s", rsp+0x940)`,
  `d[0x22D89BC] = b[rbx+3]`, `A570(kind, 0xB, -1)`, `call q[0x8C2D80]`,
  `int3`.
- `w[rbx+0x3E] != 0` → **mark abort**: emit `"MCB Broken"`, same
  ST_W/A570/hook/`int3` tail.
- `!(b[rbx+0x14] & 1)` → emit `"Allready Free:%p from %p"` and
  **return** — freeing a free block is a diagnostic, not a crash.
- `b[rbx+3] >= 0xF` → real `d[0x2]`-write fault (no descriptor).
- Real free: `b[desc+2] = 1`, clear `b[+0x14] & ~1`, `b[+2] = 0xFF`,
  `d[desc+0x68+tag*4] -= key`, `d[PTAGC + b[+0x17]*4] -= key` when the
  secondary tag is set, clear `b[+0x34]`/`w[+0x1E]`/`b[+0x17]`,
  `d[+0x30] = C620(0)`, `d[+0x3E] = 0`.
- Splice-in is **phys-neighbour first**: free `BASE(d[+0xC])` →
  `B670(pp, rbx)`; else free `BASE(d[+0x10])` → `B730(pn, rbx)`; else
  `rbx < q[desc+0x18]` (bound) → `AE00` first with `ACE0` fallback,
  `rbx >= bound` → `ACE0` first with `AE00` fallback. Each lookup
  result is guarded by a **stale-link check** (`BASE(d[+4])` /
  `BASE(d[+8])`) — if the found block already equals the stale link,
  no splice runs. Then `B210` coalesces and `B5F0` updates the
  page-head table.

**AE00** (`0036AE00`) finds the last free block at-or-below the node:
phys-prev `BASE(d[+0xC])` → signed-16 page slot → bitmap mask keeps
bits up through the slot → walks `q[desc+0x28]` page heads downward,
then the `+8` chain. **ACE0** (`0036ACE0`) is the at-or-above twin via
phys-next `BASE(d[+0x10])` with the descriptor bound check.

**EMIT** (`0017D2E0`) builds `hook(obj|1, buf, -1, fmt)`: GETOBJ
returns the `lea`-loaded output object, `r9 = fmt`, `rdx = buf`,
`r8 = -1`, `rcx = q[rax] | 1`, then `call q[0x8C2F08]`; returns
`eax` clamped `cmovs -1` — always `>= 0`, so the planted FLAG residual
(2 iff `d[0x215EFF4] == -1` else 0) propagates.

**`_chkstk`** (`00808F10`) reads `gs:[0x10]` (fake TEB limit), probes
pages downward `r11 -= 0x1000` until `r10` (new frame top), `bnd ret`.
**PINIT** (`004746F0`) is a pure `memcpy` wrapper: `movsxd r8, r8d`,
`call 00861EBA` (the real thunk `jmp q[0x8C2A68]`), returns `rcx`
(dst).

## Execution findings beyond the static reading

1. **The dump accumulates no formatted text under the planted hook** —
   FLAG is a pure `cmove` leaf and writes nothing into `rsp+0x30`, so
   the dump buffer holds only the `0x0A` separators and the
   `"\nSTACK\n"` tail. The separator cell is `w[0x8F3F58] = 0x000A`
   (not the `0x1F2FF58` cell a first reading suggested).
2. **The append end-find is O(dump length) per emit** — each byte's
   emit re-scans `rsp+0x140` for its first NUL; the bad-magic path
   executes ~50 K insns, so the emu instruction cap had to rise to
   `300000`. A first run silently truncated mid-scan — the `ends` rip
   exposed it.
3. **Nested PREL frames are rsp-derived, not constant** — AAD0's
   nested `A2A0 → PREL` chain emits at `0x6107EDC8`, ABE0's at
   `0x6107EDE8`; the model carries the caller's virtual rsp
   (`vsp − 0x48` / `vsp − 0x28` for the A2A0 calls, `vsp − 0x1230` for
   PREL's frame).
4. **Residual RAX on the aux-dump fault is the `movsd` destination**
   — `rsp+0x140 + 0xB` (`0x6107EFD3`) when `r15 = 0` faults at the
   first aux read; non-sep iterations leave `i & 0xF`, sep iterations
   leave `0x000A`.
5. **Freeing a free block is not a crash** — the `f14 & 1` gate emits
   the diagnostic and returns, byte-verified.
6. **`_chkstk` really runs** — the `prel-chkstk` case raises the fake
   TEB limit so the probe loop touches `0x6107F000`/`0x6107E000`
   pages; a GS-base register write makes `gs:[0x10]` real.
7. **The three hook cells are one dormant family** — `0x8C2D80` /
   `0x8C2F08` / `0x8C2F70` all ship as rdata pointers
   (`0x1CCF02C` / `0x1CCECB4` / `0x1CCEF16`); the planted FLAG leaf
   makes each dispatch execute shipped code.

## Mutation campaign

71 byte-precise mutants, all killed. Coverage: PREL's null gate,
alignment gate, magic compare and both dump loops, the `w[+0x3E]`
mark check (repointed to the `d[+0x3E]` clear site, discriminated by a
12-byte label reaching `+0x3C`), the alloc-bit gate, kind bound, per-tag
and secondary counter subtracts, all four phys-neighbour/stale-link
branches, the bound compare, AE00's slot/shift/mask/head/next logic,
ACE0's bound/mask/head/prev logic, `_chkstk`'s probe branch, EMIT's
`r9`/`rdx` operand selection (`m-emit-r9` first patched `mov r9,rdx` —
a no-op since `rdx` still held fmt; repointed to `mov r9,rdi` = buf),
PINIT's `movsxd` sign extension, and the thunk's IAT displacement.
Six mutant sites needed off-by-one repointing to the opcode byte
during bring-up (all verified against raw shipped bytes).

## Limits / boundaries

- `VCRUNTIME140!memcpy` is the sole scripted boundary — reached via
  the real thunk/IAT, its body entry-intercepted at the trampoline.
- The three hook cells and the emit-object global are planted
  dispatches to a real leaf; their shipped rdata/dormant values are
  disclosed above. The planted FLAG proves the dispatch executes
  in-image code, not which hook the game installs.
- The dump's formatted text is produced by the real emit path only as
  far as the planted hook — under FLAG the buffer receives separators
  and the STACK tail; a real game hook would write the `%02x ` text.
- `CODEC = 0` (raw u32 links) is the EXP-083-proven valid
  configuration; non-zero codecs are not exercised.
- `_chkstk` runs against a fake TEB; the probe writes are modelled as
  zero-page touches — no guard-page commit semantics.

## Board routing

- Audit request → `SWE2-AUDIT-SPEC`
- Findings request → `OPUS`
- Publication queued → `EXP126-PUB`
