## Falsification pass 1 — 2026-09-30 (OPUS): every section tested survives

**Attack.** The contract's static clauses were turned into checks at their instructions: the interface, invariants I2,
I3, I4 and I6, the slot layout's consumed and cleared fields, and the error helper. SECTION-02/-09's executions and
EXP-146 are carried, not re-run. Script: `Tools/analysis-kit/gfz-scripts/falsify_request_queue.py`, output
`falsify_request_queue.out`, image `73461d08…`, 0 BROKEN, exit 0.

| # | Clause attacked | Result |
|---|---|---|
| Q1 | §2 and §10: the requester and the gated builder | **survives**. The kind and index telemetry is stored before a negative index is refused with `0xFFFFFFFF`. The gate is `003EB0D0`. The gated branch copies `0x28` bytes and sets local `+4 = 0x80000` and `+0x20 = 0`. For a nonzero id only, it clears `+0x50` and sets the cap `0x80000`, chunk word 1, the remaining count, and the signed-minimum first part |
| Q2 | I3, I4, I6 | **survives**. While the free head `022C51D0` is null, it loops pump → in-flight getter → pacer. The id is `(counter << 6) + (slot & 0x3F)`, and the counter at `01EED498` resets to 1 above `0xFFFFFF` by a signed `cmovg`. The offset is `cdq; and 0x7ff; add; and 0xfffff800`, toward zero |
| Q3 | §3: what the requester consumes | **survives**. Descriptor `+0`, `+8`, `+0x10` and `+0x18` are consumed; `+0x20` is never read and slot `+0x50` is cleared. The remaining fields are written as tabulated, and the fifth and sixth arguments arrive at entry `rsp+0x28/+0x30` |
| Q4 | I2 and §2: the free list | **survives**. `0032E990` takes its flag in ECX and the slot from the free head, advancing the head; a null head faults at `[+0x10]`. `0032EC40` pushes the slot on the free head and sets its id to −1, clearing nothing else |
| Q5 | §10: the error helper | **survives**. The done callback runs with success 0 only for a nonnull callback with byte count −1. Kind `0xFF` frees the sign-extended path, and otherwise `rax` still holds the callback pointer, which is not a boolean |
