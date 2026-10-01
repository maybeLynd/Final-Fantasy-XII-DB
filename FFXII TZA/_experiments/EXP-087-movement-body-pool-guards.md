---
experiment: EXP-087
title: Movement body-pool guards under isolated original execution
contract: ../06-Movement-And-Navigation/CONTRACT-movement-body-pool.md
method: B
live_game: false
tool: evidence/movement-body-pool-guards/check.py
# Transcribed from this record's own prose header by OPUS 2026-09-16; status and dates
# are SWE2-ORACLE's to state and are deliberately left absent.
---
# EXP-087 — movement body-pool guard execution

**Date:** 2026-09-13 · **Worker:** SWE2-ORACLE · **Method:** B (isolated original-code execution, Unicorn)
**Subject:** creator `002E3500` + five consumers `00269EC0`, `002681D0`/`002681E0`, `002682D0`, `002685F0`, `00268380`
**Contract:** `Database/FFXII TZA/06-Movement-And-Navigation/CONTRACT-movement-body-pool.md`
**Board task:** `SWE2-ORACLE-BODYPOOL-GUARDS-EXEC`
**Evidence:** `evidence/movement-body-pool-guards/` (`check.py`, `result.json`, `bodies.json`)

## Result

**49/49 cases pass; 9/9 byte-level mutants detected.**

The contract's §13 pilot executed only the allocator (`003DA8A0`) and release (`003DAD00`);
the document noted "no pilot drives any of these eight functions". This package executes the
remaining surface end-to-end: the **creator** `002E3500` (release-old → alloc → **untested**
store at `actor+0x138` → all five consumers), the five consumers, and every bounded real callee:
the two alloc-time initialisers (`00380B80`, `003DA830`), the five consumer-5 leaf callees
(`003DA710`, `006C0520`, `003DB130`, `003DB120`, `003DAF20`), and the whole consumer-2 chain
(`003590D0`, `00263F10`, `00263FF0`, `003587C0`, `003589B0`, `002672B0`). Two deep predicates
(`00265680`, `0037C860`) are `ret`-stubbed at their real entries with argument logging —
disclosed in `bodies.json`. The memset/cosf/sinf import thunks resolve through the real IAT
slots to fixture implementations (rep-stosb / x87 fcos/fsin).

## Executed confirmations

- **The contract's central claim holds**: allocator exhaustion produces `NULL`, the creator
  stores it **untested** at `actor+0x138`, and every consumer still runs — all writes are
  skipped behind their guards and no crash occurs. With the edx==0 predicate path armed,
  the full chain (`003590D0` → resolver → `003589B0` → `002672B0` → `0037C860`) executes
  against the null body — predicates run, only the stores are gated.
- **Release/recycle semantics**: `create-replace` shows the released body is *immediately
  re-popped* — release pushes self-index onto the free head, alloc pops it back; the slot
  is zeroed (`[actor+0x138]=0`) between release and alloc. Exhausted+replace recycles the
  same body; the pool survives.
- **Creator guards**: `actor==NULL` (via `[ctx+0xC0]`) returns early — pool untouched,
  no alloc, no consumer calls. `ctx==NULL` is **not** guarded — faults reading `[rcx+0xC0]`
  at VA `0xC0` (measured).
- **Consumer 1** (`00269EC0`): both hops guarded; `body+6 = dl` only when the chain is live.
- **Consumer 2** (`002681D0`/`002681E0`): the only consumer guarding `rcx` at its own head.
  Kind gate is `(ctx+3 & 0xE0) == 0x60` (kind 3). Dispatch on `actor+0x152`: `0` → predicate
  chain; `2` → 3; `3` → 5; else → 2 — the non-zero arms **jump directly to the writes**
  (no predicate calls; measured by trace absence). On the edx==0 arm: encoded handle
  `((w[rec+0x16]&0x7FF)<<4 | b[rec+0x15]&0xF)<<16 | w[rec]` vs global `022C7FE0`; mismatch →
  `ebx=1` straight to writes; match → `ctx+0xC & 0x10` gates `00265680` (nonzero → 1, else 0),
  then `002672B0`'s `cmove` (returns 0 → `ebx=esi=1`), then `0037C860` nonzero → `ebx=5`.
  **Both writes — `body+0x80` and `actor+0x153` — are behind the single body reload guard**;
  exhaustion leaves even the actor byte unwritten.
- **Record resolver** (`00263F10`/`003587C0`): `[ctx+0x18]==2` selects row `movsx[ctx+0x19]`,
  slot `word[ctx+0x1A]` of the row's slot array (`row = 02098E10 + idx*0x288`, `slots=[row+8]`,
  bounds-checked, returns 0 → `cmovne` keeps the original record). Alternate-record path
  executed: the ALT record's handle is what gets compared.
- **Consumer 3** (`002682D0`): four-hop guard including `body+0x30`; replaces `body+0x90`
  bits 0–1 from `actor+0x151`, preserving upper bits (measured `0xCCCCCCC8 | a151&3`).
- **Consumer 4** (`002685F0`): copies `actor+0x148` → `body+8`. The `xorps` zero-substitution
  on null-actor is **measurably dead**: the second `test` rejects `rax==0` before any store —
  `actor==0` produces no write regardless.
- **Consumer 5** (`00268380`): kind-nibble dispatch — kind1: `xmm6=[pb+0x68]`, `xmm3=[pb+0x38]`,
  rgb defaults `0x25/0x32/0x25`; kind3: `xmm6=[pb+0xC0]*[pb+0x24]`, `xmm3=[pb+0xA8]`, rgb from
  `pb+0x104..106`; other kinds: zeros. The initial `actor+body` guard dominates — the last
  three calls reload `[ctx+0xC0]→[+0x138]` **without re-testing** (kind3 executed end-to-end:
  `body+0xE0 = 11.0*4.0 = 44.0`, `+0xE4 = 2.0+3.0 = 5.0`, quat `[6,7,10,0]` via `006C0520`).
- **`002672B0` row scan** (real): iterates codec rows `02098E10..<02099ACF` stride `0x288`;
  any enabled row (`b[row+0x10]&1`) whose value byte `b[row+0x17]&3 != 3` drives eax to 0.
  The codec table base is `02098E10`, not `02649E10` — verified by `00263FF0`'s lea
  (`0x263FFA + 0x1E34E16`).

## Findings

- **F1 — `002685F0`'s xorps path is dead code.** The `actor==0` arm substitutes `xmm0=0`,
  but the subsequent body/`rax` guard refuses before any store — the substitute value is
  never observable.
- **F2 — `002681E0`'s kind gate is byte-level `(+3 & 0xE0) == 0x60`**, same shape as
  `00268380`'s — the `+3` high nibble IS the kind field for both.
- **F3 — the release→alloc recycle is deterministic**: release pushes the freed index to
  the free head; the very next alloc pops it. Any old body the actor still references is
  therefore the *first* slot reused — no quarantine.
- **F4 — the two `.rdata` predicate-table reads that gate `002672B0` are per-row
  (flag `+0x10`, value `+0x17`)** — the scan is a conjunction over all 5 rows, not a
  single predicate.
- **F5 — `003DAF20` reads its rotation angle from `body+0xF8`** (poison-deterministic in
  the fixture) and writes the full rotation block `+0x40..0x4C` plus scaled extents
  `+0x94..0xA8` — the divisor is the real float at `.rdata 0x8F312F`.
- **F6 — host-emulator defect (not guest)**: the vendored and stock unicorn 2.1.x DLLs on
  this host intermittently return `UC_ERR_*_UNMAPPED` from the `uc_mem_write`/`uc_mem_read`
  API for pages that are mapped and executable, and earlier runs showed rip-relative `lea`
  results skewed by 8 bytes in some cases. Root-caused as the *API lookup path*, not the
  softmmu: emulation over `mem_map_ptr` regions is stable. All fixture I/O therefore
  bypasses the API (ctypes host buffers). 3 consecutive full-suite processes → identical
  49/49, 9/9.

## Mutation campaign (9/9 detected)

| mutant | site | effect measured |
|---|---|---|
| `je` → nops (cons1 actor guard) | 00269ECA | falls through → reads `[0+0x138]` → fault at VA `0x138` |
| `je` → nops (cons2 body guard) | 002682A5 | writes `[0+0x80]` → fault at VA `0x80` |
| `jne` → `je` (cons2 kind gate) | 00268202 | kind1 enters the kind3 pipeline → `body+0x80 = 3` |
| `cmove ebx,esi` → `mov ebx,esi` | 00268277 | flag-clear arm (`ebx=0`, `002672B0`→1) forced to `ebx=1` → `body+0x80 = 1` instead of 0 |
| `je` → nops (cons3 body guard) | 002682EB | `lea r8,[0+0x30]` stays nonnull → write lands at `[0x90]` → fault at VA `0x90` |
| `je` → nops (cons4 body guard) | 00268618 | store to `[0+8]` → fault at VA `0x8` |
| `je` → `jne` (cons5 body guard) | 002683C7 | null body falls through → `006C0520` writes through `r10=0` at `+0xF0..` → fault at VA `0xF0` |
| `jne` → `je` (cons5 kind gate) | 00268391 | kind1 reads `[ctx+0xB8]=0` then `[0+0x50]` → fault at VA `0x50` |
| `mov [rcx+0x138],rax` → `...,rcx` (creator store) | 002E3546 | `actor+0x138` = actor pointer, not the allocated body |

## Deviations and limits (disclosed)

- `00265680` and `0037C860` are `ret`-stubs with controlled eax — their internal logic is
  not evidence; their call/no-call ordering and argument registers **are** measured.
- memset/cosf/sinf resolve through the real IAT thunks to fixture implementations —
  the import bodies are not shipped code.
- `body+0xF8` (rotation angle input) is not in the alloc-init window; fixture value is
  `0xCC`-poison-derived. The cos/sin outputs are deterministic but carry no semantic claim.
- `NATIVE-REPLAY`/live claims are not made — this is isolated original-code evidence
  under synthetic fixtures.

## Kill set

Every mutant diverged on observable state (fault VA, written value, or stored pointer).
The suite is sensitive to: both creator guards, all five consumer guard chains, the kind
nibble gate, the edx dispatch arms, the handle-compare path, the `cmove` override, the
body-store, and the dominated reloads in `00268380`.
