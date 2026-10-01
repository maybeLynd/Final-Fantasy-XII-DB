---
experiment: EXP-034
title: Committed target handle to BattleUnit resolution
status: VALIDATED — original resolver chain with synthetic memory; read helper prepared
date_designed: 2026-09-11
method: B - isolated original-code execution
live_game: false
contract: ../07-Combat-Action/CONTRACT-commit-action.md
---

# EXP-034 — bind the committed target without guessing a pool slot

EXP-027 could only associate its visible Cactite target with a nearby actor by
position. FABLE identified the committed focus handle at BattleUnit+0x710; EXP-032
preserves it but did not decode it. This package follows its actual resolver and
tests the complete four-function chain offline. No live target binding is claimed.

## Original chain and local contract

`0031B7E0` first requires02089340 bit0x10, calls`003588B0`, null-checks the actor
and tailcalls`00263E30`, which returns the actor's qword+0x30 without extra checks.
`003588B0` rejects handle0 and decodes:

| Bits | Meaning in this resolver |
|---|---|
| 0–15 | Index into the manager's pointer vector |
| 16–19 | Manager selector; values5–15 return null |
| 20–30 | Discriminator compared to the actor's full u16+0x16 |
| 31 | Omitted by these extraction masks; a tested nonzero handle aliases when toggled |

`00263FF0` computes manager base02098E10+selector*0x288. Resolution requires
non-null qword+8 (vector) and qword+0 (storage), index less than signed dword+0x20,
manager byte+0x10 bit0 set, and index less than the vector's signed dword+0 count.
The actor pointer is vector+8+index*8. Null entries or mismatched discriminators
return null. The actor's word is not masked down to11 bits at comparison. A resolved
actor can still have null BattleUnit+0x30. No active-unit or actor-class guard occurs
in this chain; an observer must separately validate the returned unit's identity.

These are discriminator fields, not a newly proven generation counter. The
[existing encoder description](../04-Actor-Entity/battleunit-slot-pool-and-actor-class.md)
already describes their packing and explicitly leaves lifetime meaning unresolved.

## Original-code controls

[check.py](evidence/EXP-034-focus-resolver/check.py) verifies the reference executable
SHA256 and extracts exact bodies of42,143,21 and5 bytes. Each case maps those original
instructions and explicit synthetic managers/vector/actor/stack into a fresh Unicorn
instance. No calls are stubbed: all four native-code bodies execute. Each case must
reach the declared return sentinel with restored stack position before200 instructions.
The actor/vector fixture memory must remain unchanged; stack writes are expected.
This is isolated execution of original code, not execution inside FFXII.

Seventeen cases cover valid selectors2/4, field gate off, zero handle, selector5,
null vector/storage, disabled manager, equal and negative capacity/count, null entry,
different/full-word discriminator, bit31 alias and null BattleUnit. Every case reaches
the return boundary and produces its declared result. This is a selected control set,
not exhaustive handle enumeration. [Raw results](evidence/EXP-034-focus-resolver/result.json)
include inputs, visited instructions and the actor passed into the final getter.

The [read-only counterpart](evidence/EXP-034-focus-resolver/reader_resolver.py) matches
all17 original return values and actor-getter arguments. Additional tests reject
short/unreadable discriminator bytes and values outside u32. It performs no OS calls,
input or writes; the caller supplies an already qualified Reader. Sequential reads
are not atomic, so live use needs fresh command/unit identity and frame brackets.
An unreadable address raises an error rather than masquerading as a legitimate null.

## Use and limits

The next combat observer can resolve the sampled+0x710 handle, then match the returned
BattleUnit pointer against the fresh field census before comparing target HP. It must
retain null and unreadable cases distinctly and avoid treating pointer identity as
lifetime proof. This does not establish the UI's pre-commit selection, command range,
enemy death, generation updates or loaded debugger safety.

Return these resolver details to FABLE/OPUS for their owned semantic/type pages.
Exact bodies, disassembly, source identities and test receipt are listed in the
[manifest](evidence/EXP-034-focus-resolver/manifest.json). The game and its saves were
not opened or modified for this package.
