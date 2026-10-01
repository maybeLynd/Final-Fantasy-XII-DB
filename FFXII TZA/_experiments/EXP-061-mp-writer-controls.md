---
experiment: EXP-061
title: native MP writes and secondary-resource reconciliation
status: COMPLETE - bounded isolated original-code evidence
contract: none - No existing contract specifies MP and secondary-resource writers; the HP writer contract is a different operation.
evidence_class: isolated original-code
method: B - isolated original-code execution
live_game: false
execution_scope: Five original MP and reconciliation bodies; ownership, eligibility, reaction, number and accumulator boundaries controlled.
contract_coverage: No matching existing contract at recovery; this disposition does not close a database knowledge or contract gap.
tool: evidence/EXP-061-mp-writer-controls/check.py
date_designed: 2026-09-11
date_run: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-061: native MP writes and secondary-resource reconciliation

**Result:** 27 isolated original-code controls passed on first execution; an ignored
late-gate mutant was detected. ASTRA, 2026-09-11. No game process was accessed.

## Question, source and dependencies

[Where MP comes from](../10-Status-Periodic-Terminal/where-mp-comes-from.md) leaves
CS-3 open and says the secondary helper reenters the primary modifier and itself.
Its flag table also says bit 0 skips the two eligibility masks. Following
[EXP-060](EXP-060-result-numeric-dispatch.md), this experiment tests the native
local mutations behind those previously stubbed entries and challenges both claims.

The [checker](evidence/EXP-061-mp-writer-controls/check.py) verifies the certified
EXE hash and executes these complete original bodies in synthetic mapped memory:

| Entry | Bytes | Role |
|---|---:|---|
| `00300CE0` | 351 | primary MP delta |
| `00300C90` | 73 | absolute primary request |
| `00300BC0` | 207 | secondary delta |
| `0030E060` | 200 | secondary tier reconciliation, through `0030E127 RET` |
| `0016D6A0` | 3 | original `RET 0` no-op |

The first unwind entry for `0030E060` covers only 57 bytes. The retained complete
body includes the rest of its branches and epilogue; that unwind fragment is not
mistaken for the function extent. Original bytes and the complete
[disassembly](evidence/EXP-061-mp-writer-controls/disassembly.txt) are sealed with
source and [results](evidence/EXP-061-mp-writer-controls/result.json) in the
[manifest](evidence/EXP-061-mp-writer-controls/manifest.json).

Owner lookup `0031B860` returns an injected unit or null. Global eligibility
`0030B770` and unit eligibility `0030B7F0(unit, 0)` return explicit per-call masks.
Reaction `003283D0`, number publication `0028F1F0`, and accumulator clear `002FA540`
are no-effect stubs. Stubs record consumed register arguments and clobber volatile
integer registers. The original folded no-op is executed, not replaced by a stub.
Native ownership lookup, presentation, and accumulator mutation are not established.

## Primary modifier: gates and event order

The modifier reads current MP as signed word `stats+0x4C`, adds the signed dword
delta with 32-bit arithmetic, and writes the low word of its clamped candidate.
A negative sum selects zero. Otherwise the signed word maximum `+0x28` is the cap,
unless bit 7 of either byte `+0x6C` or `+0x7C` sets capacity to zero. Tests cover
ordinary floor/cap, either effect layer, and an explicitly out-of-domain negative
maximum. With a negative maximum the original can store a negative word; do not
silently replace its branch order with a universally nonnegative clamp.

Before that calculation, **unless flag bit 0 is set**, both eligibility helpers
are called and any nonzero low half rejects the operation. Both calls occur even
when the first return already has a blocking low bit.

With an owner, before the store, the original publishes:

1. Reaction `(unit, originalDelta, direction, 1)`, unless flag bit 4.
2. Number `(unitHandle, oldMP, clampedCandidate, 1)`, unless flag bit 7.

Direction is `delta > 0` for nonzero delta and flag bit 5 for zero delta. A null
owner suppresses these calls. The tests cover both zero directions and flags `0x90`.

**Every negative delta then calls both eligibility helpers again, even with flag
bit 0 set.** Nonzero high halves reject the store. `bit0-still-late-refusal` passes
flags 1 and a global mask `00010000`: both publishers run, both later gates run,
and neither the MP store nor accumulator clear occurs. The page's statement that
bit 0 skips both masks requires this late-check exception. Flags 1 bypass only the
initial low-half checks on this function, unlike the HP sibling's gate structure.

After admission, the native order is MP word store, then secondary delta if the
**original delta is positive**, then accumulator-clear call if an owner exists
and the candidate is less than the old MP. The clear stub proves the call, not the
native accumulator effect. A gain at the primary cap still forwards the full
original positive delta to the secondary modifier; forwarding is not limited to
the amount actually gained in `+0x4C`.

## Secondary word and derived tier: CS-3 correction

`00300BC0` reads and writes signed word **`stats+0x06`**. Its low-half eligibility
gates have the same initial bit-0 bypass. Once admitted, it adds the dword delta,
chooses zero for a negative sum, otherwise limits the candidate to:

```
capacity = effect39 ? 0 : signed16(stats+0x28) * (byte(stats+0x37) or 1)
```

It stores the low 16 bits at `+0x06` and calls `0030E060(stats, flags)`. It does not
read `+0x4C` or call `00300CE0` or itself. The complete call graph retained here is
`primary -> secondary -> reconciliation`, with the absolute wrapper also calling
secondary. The old CS-3 recursion claim is contradicted by the complete bodies.

Reconciliation first resolves the owner. When signed maximum `+0x28` is zero or
negative, it returns without updating the tier. Otherwise:

```
oldTier = unsigned8(stats+0x4E)
newTier = byte(stats+0x37) > 0 ? signed16(stats+0x06) / signed16(stats+0x28) : 0
```

Division truncates toward zero. If tier changes and flag bit 1 is clear, it calls
the original no-op with `(stats, newTier-oldTier)`; no hidden MP mutation is supplied
by that retail body. If `(flags & 0x410) == 0x400`, an owner exists, and the tier
changes, it calls reaction `(unit, newTier-oldTier, newTier>oldTier, 1)`. Finally it
stores low8(newTier) at `+0x4E`, even when unchanged. Flags `0x400` versus `0x410`
and bit 1 distinguish the two call controls.

A zero multiplier still gives the secondary word a one-maximum cap, but forces
tier zero. Synthetic oversized secondary values demonstrate word truncation:
with maximum 20000, multiplier 3 and delta 40000, the pre-store capacity permits
the value, then signed-word rereading feeds a negative quotient to tier derivation.
This is a width boundary control, not evidence that shipped game state reaches it.
No player-facing resource name or authored producer of the multiplier is assigned.

## Absolute primary wrapper

`00300C90` first calls primary with `requested - signed16(currentMP)`. After that
call it reads the **current secondary word `+0x06`** and, if the requested signed
dword is greater, calls secondary with their difference. The read occurs after
the primary call's possible secondary increment. The `absolute-second-topup`
control starts MP 40, secondary 0, and requests 80: primary adds 40 to each, then
the wrapper adds a further 40 to secondary. The final MP/secondary pair is 80/80.
The lower request control exercises the branch with no secondary top-up.

## Controls, falsification and propagation

Each case compares a separate arithmetic/event model with the exact ordered
native entry calls, stub calls and nonstack writes. It compares the full 4096-byte
fixture page, reaches the exact injected return boundary, restores RSP, and checks
all eight nonvolatile integer registers. Inputs, full initial/expected/final pages,
ordered events and instruction visits are retained. Return-register meaning,
nonvolatile SIMD state, full native dependency ABI and live action composition
are outside the claim.

The 27 cases cover gain/cap/spend/floor, both zero directions, silent flags, absent
owner, both effect layers, initial/late global and unit gates, bit-0 distinctions,
secondary tier changes and suppression, capacity and multiplier boundaries,
nonpositive reconcile maximum, both absolute branches and signed-width extremes.
A private mutant replaces the late global rejection branch at `00300DF6` with
NOPs. Under flags 1 and a blocking high global bit it reaches the same return but
writes MP and calls accumulator clear; exact event/memory comparison rejects it.

FABLE receives a contradiction for the old CS-3 recursion/field assertion and the
unqualified bit-0 mask bypass. OPUS receives the local `+0x06` / `+0x4E` relationship,
widths, capacity and flags for structured propagation. Existing peer field rows
already name `+0x06` as a secondary resource; this result does not claim to discover
that field first. Canonical correction closure remains pending its integration.
