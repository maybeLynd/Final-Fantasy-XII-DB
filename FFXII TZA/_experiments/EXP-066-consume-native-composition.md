---
experiment: EXP-066
title: native cost-to-consumption-to-resource-write composition
status: COMPLETE - bounded isolated original-code evidence
contract: none - No existing contract specifies this cost-to-consume-to-MP composition; the HP and inventory storage operations are not executed.
evidence_class: isolated original-code
method: B - isolated original-code execution
live_game: false
execution_scope: Ten complete original bodies from consumer entry through cost and MP writes, no phase bridge; ownership, eligibility and gil controlled.
contract_coverage: No matching existing contract at recovery; this disposition does not close a database knowledge or contract gap.
tool: evidence/EXP-066-consume-native-composition/check.py
date_designed: 2026-09-11
date_run: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-066: native cost-to-consumption-to-resource-write composition

**Result:** 15 controls passed on the first execution; removing cost negation
was detected. ASTRA, 2026-09-11. No game process accessed.

## Question and composition boundary

Do the recovered cost calculation, consume dispatch and resource-writer contracts
agree when original instructions execute together against the same memory?
[EXP-063](EXP-063-mp-cost-controls.md), [EXP-065](EXP-065-resource-consume-controls.md)
and [EXP-061](EXP-061-mp-writer-controls.md) establish their separate boundaries.
Here costs must cause the expected native MP, secondary-word and tier stores.

The [checker](evidence/EXP-066-consume-native-composition/check.py) verifies the
reference executable SHA-256, begins at the consumer entry and runs ten complete
original bodies without a phase bridge or injected intermediate results:

| original body | bytes |
|---|---:|
| consume `00305640` | 393 |
| MP cost `00309110` | 165 |
| tier cost `00308FF0` | 110 |
| modified cost `002F95D0` | 589 |
| alternate-channel predicate `002F9820` | 51 |
| pointer resolver `0020E600` | 10 |
| MP writer `00300CE0` | 351 |
| secondary writer `00300BC0` | 207 |
| tier reconciler `0030E060` | 200 |
| original no-op `0016D6A0` | 3 |

Original float constants 50.0 / 100.0 / 64.0 are read from the executable and
asserted. Synthetic unit/stats, action/effect tables and relocation globals supply
inputs. Ownership resolver `0031B860` returns zero; eligibility helpers `0030B770`
and `0030B7F0` return controlled masks; gil getter/setter `00253690` / `00254EE0`
are stubs. Each clobbers volatile integer registers. No ownership, native
eligibility, gil storage, presentation, inventory, scheduling or whole-action
parity is inferred. Tested categories 3 / 5 / 6 avoid the accounting tail.

Original bytes, [disassembly](evidence/EXP-066-consume-native-composition/disassembly.txt),
[results](evidence/EXP-066-consume-native-composition/result.json) and executed source
are sealed in the [manifest](evidence/EXP-066-consume-native-composition/manifest.json).

## Additional native helper

`00308FF0` consumes the low 16-bit action id and returns zero above `0x21E`.
For admitted ids it resolves the action row and returns byte `+0x0A` only when
category byte `+0x1E` is 5 or 6; other categories return zero. It does not inspect
the unit argument. The complete 110-byte body, including both returns, was read;
this composition exercises categories 3 / 5 / 6. The upper-id and invalid-table
behaviour is static evidence here, not separately exercised helper controls.

## Same-state outcomes

Unless stated otherwise, initial MP is 40, secondary word 150, maximum 100,
multiplier 3 and tier 1. Costs are synthetic table values, not shipped data.

| control | computed MP / tier cost | final MP / secondary / tier |
|---|---|---|
| base byte 31 | 31 / 0 | 9 / 150 / 1 |
| effect 36 halves | 15 / 0 | 25 / 150 / 1 |
| effect 91 with 10 percent | 27 / 0 | 13 / 150 / 1 |
| effect 51 frees | 0 / 0 | 40 / 150 / 1 |
| effect 32, kind zero | 0 / 0 | 40 / 150 / 1 |
| effect 32, kind one | 390 / 0 | 0 / 150 / 1 |
| category 5, byte 2 | 0 / 2 | 40 / 0 / 0 |
| category 6, byte 1 | 0 / 1 | 40 / 50 / 0 |
| id `0xD0` bypasses effect 51 | 31 / 0 | 9 / 150 / 1 |
| 240 percent reduction then half | -21 / 0 | 61 / 171 / 1 |
| effect 39 capacity zero | 31 / 0 | 0 / 0 / 0 |

The negative synthetic cost becomes positive MP delta 21, so the native MP writer
also adds 21 to the secondary word before the consumer's separate zero-delta
secondary call. This interaction is executed, not copied between test stages.
It does not establish that shipped authored percentages produce negative costs.

Four additional controls distinguish gate behaviour: initial low-half refusal
leaves MP at 40; late high-half refusal also leaves MP at 40, including when
input flag 1 bypasses the initial gate. With flag 1 and a low-half-only mask,
the late gate admits the spend, leaving MP 9. All four leave secondary 150 and
tier 1 under their specified mask sequences. These confirm that the consumer's
flag translation composes with the writer's distinct initial and late gates.

Kind-zero reservations clear natively before cost calculation; kind one retains
them. The consumer reaches the gil setter with 93 from controlled balance 100
and extra field 7 in every normal case, even when the MP write is refused.
The setter's actual balance change is outside the experiment.

## Oracle and falsification

Every original helper entry, stub entry and native non-stack store is compared
in one exact ordered event stream, including arguments, multiplicity and values.
Expected state is calculated independently in Python from the recovered rules.
Complete action/effect, unit/stats and registry/relocation fixture pages are
compared in memory; result receipts retain the comparison verdict, exact events
and final resource fields rather than serializing the full pages. The checker
reconstructs the fixture and expected pages from recorded inputs. Normal runs
must reach the consumer return boundary and restore RSP and all eight nonvolatile
integer registers. Visited instructions and exact source identity are retained.
No SIMD-preservation claim is made.

A private mutant replaces `NEG EBX` at `003056EC` with two NOPs. The unchanged
cost 31 becomes an MP gain: final MP 71 and secondary 181, rather than 9 and 150.
The mutant reaches normal return, but fails both the exact event and full-page
oracles. No original file or replacement implementation is mutated.

## Scope and propagation

This validates the local composition from authored row bytes through calculated
costs to actual original MP/secondary/tier writes. It adds evidence for the
[MP page](../10-Status-Periodic-Terminal/where-mp-comes-from.md) and the
[item lifecycle](../12-Items-Equipment-Shops-License/using-an-item-is-an-action-that-costs-an-item.md).
It neither closes native external dependencies nor proves live action timing or
integrated replacement parity. EXP-065's callback interventions remain separate;
this composition has no callback memory interventions.
