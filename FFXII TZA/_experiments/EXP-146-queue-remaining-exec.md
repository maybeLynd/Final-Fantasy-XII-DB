---
experiment: EXP-146
title: Resource request queue remaining entries executed — 0032E450
  constructor, 0032E990 slot-taker, 0032E620 request builder,
  0032E870 requester/stall, and 0032E040 once-per-frame caller on
  shipped bytes, including the full
  construct→request→pump→retire→free lifecycle in one process
contract: 02-Resource-And-Asset-Pipeline/CONTRACT-resource-request-queue.md
method: B
live_game: false
tool: evidence/queue-remaining-exec/check.py
---
# EXP-146 — queue-remaining-exec

> **SECTION-02 current interpretation (2026-09-22):** [original-code review](evidence/continuation-section02-resource-queue/REVIEW.md) corrects ABI/list names, selective initialization/recycling and the common-footer description below. The original `check.py` and `result.json` are unchanged historical artifacts. Their 22 assertion branches replay, but the two positive loader-gate cases had no positive assertion; new native checks cover them. This is production propagation, not new T2 acceptance or a rerun of the full producer campaign.

**Status:** complete · **22 cases, zero failures, stable ×3**
**Evidence:** `evidence/queue-remaining-exec/` (`check.py`,
`result.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base
`0x120000`

## Objective

`CONTRACT-resource-request-queue.md` §13 listed five `entries`
with **NO executed evidence**: `0032E450` (pool constructor),
`0032E620` (request builder), `0032E870` (requester/stall),
`0032E990` (slot-taker/linker), `0032E040` (once-per-frame pump
caller). EXP-128 had already executed the pump `0032E070`, the
splice `0032EC40` and retire helper `0032E370`. This experiment
executes the remaining five on shipped bytes and closes the gap
with a single-process lifecycle: construct → request → pump →
retire → free.

## Executed signature map

- `0032E450()` — constructor; no arguments. Initialises selected fields and linkage in 64
  `0x80`-byte slots at `0x022C31C0` and links all 64 into the
  free list (`0x022C51D0` head, each slot's `+0x10` next /
  `+0x18` prev). Reruns linkage initialization over dirty state. It does not clear the entire records; the original dirty-rerun assertions check global heads/counter, and SECTION-02 adds all-byte sentinel checks.
- `0032E990(ecx=atTail)` — free-head pop/pending-list insertion, no calls. RCX is not an input slot pointer; the body loads that slot from `022C51D0`.
  `flag!=0` unlinks the slot from the free list and appends it
  to the pending list (`0x022C51C0` pending head / `0x022C51C8` pending tail; `0x022C51D0` free head). Either flag
  on an empty free list dereferences the null head's `+0x10`
  unconditionally → **fault at `0x10`** (no guard; observed).
- `0032E870(ecx=a, rdx=b, r8=c, r9=d, [rsp+0x28]=aux-or-0,
  [rsp+0x30]=atTail)` — requester. Stall loop while no free
  slot: `0032E070` pump → `0046DFE0` flag leaf → `0035EA30`
  pacer thunk; then `0032E990` to take a slot, stamps
  `+0x20=1`, `+0x21=a`, `+0x24=b`, `+0x28=d`, `+0x60` from aux
  or 0, `+0x64` = request id.
- `0032E620(ecx, edx, r8, r9, [rsp+0x28]=aux)` — builder.
  Reads telemetry cells, calls `003EB0D0` gate, then `0032E870`
  and returns its id. `003EB0D0` walks the `BgmStream` records at
  stride `0x38` (count 1) and returns 1 iff any record's `b[+0x31]` —
  `02B5E111`, streamActive — is nonzero (owner re-read, I2 verdict).
  **Gate polarity: `b[02B5E111]==0` → raw
  path** — caller's aux pointer passed through unmodified, no
  post-fixups; **gate set → aux copied to a stack local**
  (observed: `q[rsp+0x28]` at `0032E870` entry is a stack
  address, not the caller's `0x40001000`), and on success the
  slot gets `+0x30=0x80000`, `+0x22=1`, `+0x34=d[+0x28]` pre-
  clamp, `+0x28` clamped to `≤0x80000`, `+0x2C` re-rounded
  (`aux.d0` `0x8FF → 0x800`), `q[slot]=0`. Failure is a 32-bit
  `or eax,-1` → returns `0xFFFFFFFF`, not a sign-extended
  qword.
- `0032E040()` — checks the two loader predicates (`001EDE80`,
  `0017D930`, scripted) and tail-jumps into `0032E070` only if
  either is active. Both idle → returns without touching the
  pump (verified: no `e070` trace marker).

## Findings

1. **Request id is a generation counter, not an index.** The
   id is `(idctr++ << 6) | slot_index` (`0x01EED498`). Two
   requests in one process produced `0x40` then `0x81` — the
   counter increments once per request and the low six bits are
   the slot index, so `id>>6` is a generation and `id&0x3F`
   recovers the slot. A planted zero counter with slot zero yields `id=0` **after consuming the slot**. The gated builder skips post-fixups; it does not undo acquisition. Normal constructor initialization sets the counter to1. The actual wrap comparison is signed; the usual wrap statement is scoped to the constructor-derived domain.
2. **The pump reaches a common service footer, including when empty.**
   After the pending list empties, `0032E070` still calls the scripted
   `003EADD0` service gate and `0046DD50`/`003E9780`/`0036FD50` boundaries.
   `00862090` is the separate scripted tick source, not the `xadd0` gate.
   The old "teardown" label did not establish shutdown or destruction;
   the same footer also runs for busy, nonempty work.
3. **The stall loop is pump+flag+pacer, in that order.** With
   the free list empty, `0032E870` ran three full passes of
   `0032E070 → 0046DFE0 → 0035EA30` before `0032E990` consumed
   the slot the pacer stub injected on pass 3 — the
   `take-slot → stall → pump → retry` shape the contract
   describes, now executed.
4. **`0032E990` has no empty-free-list guard.** Either flag
   against `free_head==0` faults on `[0x10]` — callers (the
   requester) always test the head first.
5. **Retirement recycles selectively, not by clearing the whole record.**
   The retained lifecycle itself ends with `b21=3` and `d24=256`,
   contradicting the original zero-kind/zero-index prose. `0032EC40`
   updates linkage and id; its callers clear state. SECTION-02 seeds
   nonzero payloads and verifies that kind, index, callbacks, destinations
   and unused bytes can survive recycling. Old raw observations are retained.
6. **`0032E040` is a pure gate.** It performs no work itself;
   either loader predicate active → tail `jmp` into `0032E070`.

## Evidence classes and boundaries

**NATIVE-REPLAY** on shipped bytes (hash-verified image,
Unicorn): the five named entries plus the pump/retire/splice
machinery from EXP-128, `003EB0D0` (reads the flag byte at
`0x02B5E111`) and `0046DFE0` (18-byte flag getter, compares `0215EFF4` with -1 and returns 2 or 0, with **no calls**) executed as shipped.

**Scripted boundaries, disclosed:** loader predicates
`001EDE80`/`0017D930` (return values planted), pacer chain
`0035EA30 → 0035EB70` (return plants; in the stall case the
`0035EA30` stub injects the free-list slot on pass 3), the
`003EADD0` service gate (`xadd0` trace tag), submit boundaries, and separate `00862090` tick source, and the teardown
externals `0046DD50`/`003E9780`/`0036FD50`/`003BB790`
(traced, not executed). No live-game reachability is claimed —
fixture globals are MODEL-PROVEN; the executed control flow,
list manipulation, id arithmetic, clamp/fixup semantics and
the fault behaviour are NATIVE-REPLAY.
