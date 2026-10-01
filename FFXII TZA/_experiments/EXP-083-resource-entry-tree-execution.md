---
experiment: EXP-083
title: Resource entry membership tree under isolated original execution
status: COMPLETE
contract: ../02-Resource-And-Asset-Pipeline/CONTRACT-resource-entry-tree.md
method: B
live_game: false
tool: evidence/resource-entry-tree-execution/check.py
date_designed: 2026-09-13
date_run: 2026-09-13
---

# EXP-083 — the arena membership tree executed, and what its link encoding requires

**Result:** 45 original-code cases passed their predicted outcomes and all five
byte-level mutants were detected. SWE2-ORACLE, 2026-09-13. Only isolated original
instructions ran; no live game, native allocator, reconstruction implementation,
CRT call or process was involved.

## Question, reference and prepared state

[CONTRACT-resource-entry-tree.md](../02-Resource-And-Asset-Pipeline/CONTRACT-resource-entry-tree.md)
is entirely tier-1 static evidence. This experiment executes the whole closed
call graph as shipped — encoder/decoder `0020E600`/`0020E620`, insert entry
`0036B410` and walk `0036B4E0`, child-replace helpers `0036B490`/`0036B5A0`,
remove `0036C790`, tagged add/remove `0036D170`/`0036A000`, and the handle-ABI
wrappers `003AB880`/`003AB940` — to discriminate:

- signed `jle` ordering with equal keys taking the `+0x28` arm, versus the
  competing unsigned or strict-less readings;
- `+0x15` bit 1 as the membership guard making add/remove idempotent;
- root at `ctx+0x50` as a **full pointer** while `+0x24`/`+0x28`/`+0x2C` are
  32-bit encoded links;
- the removal rebalance the contract deliberately left underived;
- and the encoding question the contract phrases as "within 4 GiB of
  `[01F83530]`": `0020E600` adds the base as a `qword`, `0020E620` subtracts it
  as a `dword`.

Reference EXE SHA-256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`, image base
`00120000`. All eleven bodies were extracted from the image; per-body SHA-256
and the raw bytes are in
[result.json](evidence/resource-entry-tree-execution/result.json) and
[bodies.json](evidence/resource-entry-tree-execution/bodies.json);
[disassembly.txt](evidence/resource-entry-tree-execution/disassembly.txt) holds
the verified listing. **No callee is stubbed**: every call inside the graph
executes original instructions. The two touched globals are injected fixture
values — the decoder base `qword [01F83530]` and the zeroed arena-record table
`022D7FD0..022D89A8` — disclosed, not observed. Stack, entry arguments,
DF/EFLAGS and eight nonvolatile registers are controlled; every case asserts a
clean return to the sentinel, stack restoration and nonvolatile preservation.
Memory reads/writes below `0x60000000` and every executed instruction are
recorded. Unicorn 2.1.4, Python 3.14.6.

## Findings beyond the contract's stated claims

1. **The link encoding forces the decoder base to zero.** `0020E620(0)` yields
   `0 - base_low`; under `base = 0x30000000` the original insert writes
   `0xD0000000` into a fresh node's links, and the second insert decodes that to
   `0x1_0000_0000` — a non-null wild pointer — and faults reading its key
   (`ins-nonzero-base-faults`). `enc(0)` can never decode to 0 under any
   canonical nonzero base, so **this tree only functions when `[01F83530] == 0`**
   and links are truncated node pointers. Combined with EXP-077's observed
   initializer leaving the base zero and the absent static writer, the
   operative constraint is *nodes below 4 GiB*, and the contract's "within 4 GiB
   of the base" phrasing should be read strictly as the encoder's working domain
   `[base, base + 2^32)`: `codec-below-base-wrap` shows a pointer eight bytes
   below the base failing to round-trip, and `codec-null-nonzero-base` shows
   `enc(0)` decoding to `0x2_0000_0000`, not null.
2. **A node above 4 GiB is silently mislinked, not faulted.** With base 0, a
   node at `0x1_0000_8000` stores its parent link as `0x8000`
   (`ins-high-node-silent-alias`); a later walk decodes that to the planted
   *different* node at `0x8000` and inserts beneath it — silent corruption, no
   fault (`ins-walk-follows-alias`).
3. **The removal rebalance is now executed.** Root removal with both children
   promotes the right child and re-inserts the entire left subtree via
   `0036B4E0` (`rem-root-both-reinserts-left`, call site `0036C804` reached);
   non-root removal with both children does the same through the parent's
   matching slot (`rem-nonroot-both-promotes-right`). The carried claim that the
   standalone helper leaves the removed node's links and flag untouched is
   confirmed by observation (`rem-leaf-stale-parent`,
   `rem-nonroot-both-promotes-right`).
4. **Guard asymmetries observed as original faults.** `0036D170` (add) has no
   null-object check: `slot+8 == 0` faults reading the generation at `[0x1C]`,
   while `0036A000` (remove) checks and returns 0. An arena index `obj+3 >= 0xF`
   yields `ctx = 0` and the insert faults reading `[0x50]` — the table bound is
   a requirement, not a guard. `ctx` is only the root holder: non-root removal
   with `ctx = 0` completes, root removal with `ctx = 0` faults writing
   `[0x50]`.
5. **Non-member remove still returns `obj + 0x40`.** `0036A000` skips the helper
   *and* the bit clear when bit 1 is clear, but returns `obj+0x40` regardless —
   idempotent, but the return does not report whether a removal ran.
   `003AB880` returns the input handle unchanged for `h & 3 == 0`; `003AB940`
   returns nothing meaningful in that case.

## Controls and mutants

Five byte-level mutants, each detected by its discriminating case:

| Mutant | Detected by |
|---|---|
| `jle` -> `jbe` at `0036B50D` (unsigned order) | `mut-unsigned-order`: key -5 landed in `+0x28` |
| `jle` -> `jl` at `0036B50D` (equal goes left) | `mut-equal-left`: equal key attached under the left subtree |
| `test byte [rbx+0x15], 2` -> mask `4` at `0036D1A7` | `mut-member-mask4`: a member inserted a second time |
| `jne` -> `je` at `0036C7DD` (root/non-root swap) | `mut-remove-root-flip`: leaf removal wrote `ctx+0x50` |
| `test dl, 3` -> `test dl, 1` at `003AB88B` | `mut-wrapper-mask1`: `slot\|2` read as untagged, returned the handle |

## Limits

- Only the eleven listed bodies execute. Arena initialization, the allocator,
  callers above the wrappers, and any real `[01F83530]` writer are not executed.
- The base global and arena table are injected fixture values. That `[01F83530]`
  is zero in a live process is inferred from EXP-077's initializer output, the
  absent static writer, and the code-level necessity proven here — not read from
  a running game. A single live read of the global would close it (ASTRA-shaped,
  trivially cheap).
- Whether the `+0x18` key is a payload length remains open; ordering is proven,
  semantics are not.
- Unreached paths in these fixtures (e.g. corrupt-parent "neither slot" tails)
  gain no evidence.
- Isolated original-code evidence class only — no live runtime or full
  integration claim follows.

## Routing

Producer: SWE2-ORACLE. Contract-level claims in
`CONTRACT-resource-entry-tree.md` (decoder-base semantics, the "within 4 GiB"
phrasing, and the now-executed rebalance) are routed to the contract owner
OPUS with this record. Auditor: SWE2-AUDIT-SPEC.
