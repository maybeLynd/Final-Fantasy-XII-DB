---
contract: <semantic operation name — what it does, not what it is called>
category: <NN-Category>
scope: operation | family | subsystem | transition
level: L1 | L2 | L3
readiness: DISCOVERED | CLASSIFIED | SEMANTICALLY IDENTIFIED | SIGNATURE RESOLVED | TYPE RESOLVED | DEPENDENCIES RESOLVED | BEHAVIORALLY UNDERSTOOD | RUNTIME VALIDATED | CONTRACT READY | RECONSTRUCTION READY | IMPLEMENTED | DIFFERENTIAL TESTED | PARITY CERTIFIED
confidence: PROVEN | VERY HIGH | HIGH | PROBABLE | HYPOTHESIS | UNKNOWN | CONTRADICTED | SUPERSEDED
implements: <document(s) this contract formalises>
entries: [<VA>, ...]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: <YYYY-MM-DD>
audit:
  passes: 0                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: null              # YYYY-MM-DD
  last_pass_state: null        # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

> **`audit:` is not optional and was missing from this template until 2026-09-12.** A contract
> without it cannot record a falsification pass, and `progress.py` counts a pass only when
> `passes > 0` **and** `last_pass_state` names the program state it ran against — an amendment bump
> produces neither. Thirty-four contracts were in that position: permanently in `audit_coverage`'s
> denominator with their audit debt invisible rather than zero. **Leave it at `passes: 0` until a
> pass actually happens**, and remember that a contract is the document an L2 claim rests on, so it
> is the last one that should go unattacked.

# Contract — <semantic operation name>

> **What a contract is for.** A system document explains a mechanism to a person. A contract states
> it precisely enough that **someone who has never seen the binary can reimplement it**, and
> precisely enough that a **differential test can be written from it**. If a field below cannot be
> filled from evidence, write **UNRESOLVED** — never a plausible guess. An honest gap keeps the
> contract usable; an invented one poisons both the implementation and the test.

## Scope — read this before filling anything in

**Choose the smallest scope that avoids duplication**, and say which in the frontmatter:

| scope | use when | example |
|---|---|---|
| `operation` | one semantic operation, however many functions implement it | "apply the frame-limit setting" |
| `family` | N functions share a body shape and differ in stated ways | the 351 return-value adapters |
| `transition` | one edge of a state machine | "actor: realized → retiring" |
| `subsystem` | the invariants and ordering that hold *across* its operations | "the post-process chain" |

**Do not write one contract per function.** Most functions are a step inside an operation; the
operation is the reimplementable unit. A per-function contract is justified only when the function
*is* the whole operation.

## 1. Purpose

What this operation accomplishes in the game, in the game's vocabulary. One paragraph.

## 2. Interface

| | |
|---|---|
| entry point(s) | `<VA>` — with body size |
| calling convention | |
| parameters | index, register, type, meaning, valid range |
| return type | |
| return semantics | what each returned value *means*, including error encodings |
| callbacks / indirect dispatch | address-taken, vtable slot, registry — and how it is reached |

## 3. Types

Every structure this operation touches. **Preserve the physical offsets beside the semantic names —
`object->generation` never replaces `+0x1A8`, it accompanies it.**

| offset | size | field | type | meaning | evidence |
|---|---|---|---|---|---|

State the **total size**, the **allocation site**, and whether the layout is complete or partial.

## 4. Preconditions · postconditions · invariants

- **Preconditions** — what must be true before the call, and what happens if it is not.
- **Postconditions** — what is guaranteed after a successful call.
- **Invariants** — what is true throughout, including across the failure paths.

## 5. State

| | fields / globals | evidence |
|---|---|---|
| read | | |
| written | | |
| allocated | | |
| deallocated | | |

**Use `globals_index.py --addr <VA>` to enumerate readers and writers**, and record its blind spot
(RIP-relative only) if a negative matters.

## 6. Relationships

Callers · callees · callbacks · indirect dispatch. **Exclude EH funclet edges** — they are banned as
semantic evidence and `edges.tsv` contains them.

## 7. State transitions

`previous state → resulting state`, with the condition on each edge and the exact test that decides it.

## 8. Script · resource · event interactions

Which opcodes, verbs, authored tables, archives or events participate, and in which direction.

## 9. Determinism

- **RNG** — which stream, drawn how many times, scaled how. Write the scaling expression with real
  constants.
- **Timing / update ordering** — which phase of the frame, what must already have run.
- **Threading / synchronization** — which thread, what is shared, what protects it.

## 10. Failure paths and edge conditions

Every branch that does not complete the operation, and every *meaningfully distinct* boundary state.
**Not every arithmetic edge — the ones that change behaviour.**

## 11. Observable behaviour

What can be seen or measured from outside: on screen, in a log, in memory, in a save file. **This
section is what makes a differential test possible; if it is empty the contract cannot be validated.**

## 12. Reproduction formula

The actual expressions, with real constants, in the order the code evaluates them. Reproducible by
hand, or the contract is not finished.

## 13. Runtime validation

| claim | how it was observed live | date | result |
|---|---|---|---|

**Empty is a legitimate and common state — say so explicitly**, because it is the difference between
`BEHAVIORALLY UNDERSTOOD` and `RUNTIME VALIDATED`, and the readiness gate depends on it.

## 14. Unresolved

Numbered, each with what would resolve it. These are the contract's own frontier and must also appear
in `OPEN-QUESTIONS.md`.

## 15. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|

Tiers from `_index/EVIDENCE-STANDARD.md`. **Never sum tiers.**

## 16. Parity plan

How this would be differentially tested, and against which dimensions:
`STRUCTURAL · CONTRACT · STATE-TRANSITION · CALCULATION · RNG · SERIALIZATION · TIMING ·
INTEGRATION · PRESENTATION · EDGE-CASE · FULL SUBSYSTEM`.

**Name the dimensions that will *not* be tested and why** — an untested dimension recorded is a
known limit; an untested dimension unrecorded is a false parity claim.
