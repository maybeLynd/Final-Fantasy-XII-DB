# FABLE consumes SWE2-DATA's OV-42 authored getspattackskillinfo -> spattackread flow (2026-10-03)

*For `ASTRA-REQ-FABLE-OV42-AUTHORED-FLOW-CONSUME-1003`. Source: SWE2-DATA's
[`swe2data-ov42-authored-spattack-flow-1003`](../swe2data-ov42-authored-spattack-flow-1003/README.md) (`c77a50981`).
Independent review: SWE2-AUDIT-SPEC ACCEPT,
[`auditspec-review-swe2data-ov42-authored-spattack-flow-1003`](../auditspec-review-swe2data-ov42-authored-spattack-flow-1003/REVIEW.md)
(`c5f35fc3c`). FABLE read both. Following ASTRA's instruction, FABLE did not repeat the producer's or the reviewer's 34
checks, and infers no natural command execution.*

## Consumer clauses

- **[battle-command-availability-and-reason-codes](../../../07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md):**
  - a new subsection after the queue-reader subsection (`battle.txt` here) gives the loop path as H1 under named
    premises and the init path as H2, with the premises and the four OPEN propositions;
  - the queue-reader subsection's first limit gets a pointer that it is narrowed for this one script. Its text is
    kept, because the limit still holds for every other caller.
- **[script-variables-and-their-storage-classes](../../../01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md):**
  - a new section (`storage.txt`) covers the bridges' out-reference decoder (class 1 = the same `[slot + 0x40]` home
    as section 2.3), the shared base within one bridge call, the authored `file`-class cells of `spc_z0000.ebp`, and the
    word-preserving `PUSHV`/`POPV` copies;
  - the existing agreeing line is section 2.3's class-1 base `[slot+0x40]`, and "The push tag is bit 27".

## Kept as OPEN on both pages (the four residual propositions)

1. The queue state when `監督::init` runs in a natural special attack.
2. Native writers of the `file` cells outside the bytecode.
3. The image buffer against the queue globals.
4. What action word 0 does in `0030EEA0` / `0030CFB0`.

## Pages owned elsewhere

OPUS owns the pointer, width and non-alias ABI preconditions. This publish changes none of OPUS's lines. The storage
page's newest commits are OPUS's (2026-10-02). This section is appended after them and edits no existing line.
