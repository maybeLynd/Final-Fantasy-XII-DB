---
experiment: EXP-048
title: discriminator advancement, invalidation and finite wrap
status: COMPLETE - bounded isolated original-code evidence
contract: ../04-Actor-Entity/CONTRACT-field-runtime-pass.md
evidence_class: isolated original-code
method: B - isolated original-code execution
live_game: false
execution_scope: Six original bodies composed with a stable synthetic registry, including finite wrap; no stubs.
contract_coverage: Resolver dependency 003588B0 under discriminator advance and finite wrap; no field pass, native registry construction or scheduling.
tool: evidence/EXP-048-handle-discriminator-advance/check.py
date_designed: 2026-09-11
date_run: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-048: discriminator advancement, invalidation and finite wrap

**Result:** `002659D0` is an original incrementer for actor+16h. Composed original
advance/encode/resolve controls reject a stale handle after one advance and accept
the new handle. A full 2047-step period restores the original handle under an
unchanged synthetic registry. ASTRA, 2026-09-11. No live game or stubs.

## Question and source

The current handle page and handleTag11 type row say no incrementer was found.
Following the delegate in [EXP-047](EXP-047-attacker-mask-reset.md) exposed its
call at `00322107` to `002659D0`. The complete 24-byte incrementer is:

```text
002659D0 movzx eax, word ptr [rcx+16h]
002659D4 mov edx, 1
002659D9 inc eax
002659DB and eax, 7FFh
002659E0 cmove eax, edx
002659E3 mov word ptr [rcx+16h], ax
002659E7 ret
```

It computes `next = ((old + 1) & 0x7FF); if (!next) next = 1`, writes a word,
and returns the new value in EAX. This is a concrete counter advancement, not
an inference from the shape of an encoded handle. Its null input is not guarded.

[check.py](evidence/EXP-048-handle-discriminator-advance/check.py) verifies the
certified executable hash and extracts six complete original bodies: advance,
the 38-byte encoder at `003589B0`, and the four resolver bodies from
[EXP-034](EXP-034-focus-resolver.md). The resolver bytes must match that retained
experiment exactly. [Disassembly](evidence/EXP-048-handle-discriminator-advance/disassembly.txt)
and all six binary bodies are preserved.

## Method and controls

Every boundary case uses a fresh Unicorn instance with a synthetic enabled manager
2, index 1, vector/count/capacity controls and one actor with a unit back-pointer.
The actor page has patterned surrounding bytes. The original encoder makes the
old handle, the original resolver checks it, the incrementer executes, and then
the original encoder/resolver test the new and old handles. No callee is stubbed.
Every call must return to its sentinel with RSP+8 within 200 instructions.

The advance's only non-stack write must be a two-byte store at actor+16h; the
rest of the actor page must match. Encoder/resolver calls must make no non-stack
writes and preserve the whole actor page.

| Initial word | Old handle resolves before advance | Next word | Old/new handle after advance |
|---|---|---|---|
| 0 | yes | 1 | null / unit |
| 1 | yes | 2 | null / unit |
| 2046 | yes | 2047 | null / unit |
| 2047 | yes | 1 | null / unit |
| 0800h (malformed fixture) | no | 1 | null / unit |
| FFFFh (malformed fixture) | no | 1 | null / unit |

The malformed high-word cases distinguish the encoder's 11-bit mask from the
resolver's full-word comparison. They are synthetic boundary inputs, not evidence
that the game constructs them. Zero is accepted by this resolver when the packed
handle itself is nonzero; the incrementer does not produce zero.

A separate original-code cycle starts at 1 and executes all 2047 advances. The
asserted sequence is 2 through 2047, then 1. The original encoded handle then
resolves to the same unit in the unchanged registry. Its sequence hash and final
resolver trace are retained. This establishes the finite period without claiming
that a real actor persists through that many updates.

A private fault removes only the conditional zero-to-one move. At old=2047 it
stores zero and fails the required boundary result. Original bytes are unchanged.
[result.json](evidence/EXP-048-handle-discriminator-advance/result.json) records
all boundary traces, writes, handles, resolutions and the cycle/fault controls.
The [manifest](evidence/EXP-048-handle-discriminator-advance/manifest.json) seals
the evidence. Run `check.py` with the existing Windows Python/Unicorn environment.

## Correction and limits

The prior "no incrementer found" statement is superseded by this writer. Its
earlier negative search remains a historical result of a limited search, not
proof that no writer exists. Evidence is routed to FABLE for the handle page/M-5
and OPUS for the type row; those owners retain their file claims.

This proves a generation-like discriminator advance and rejection of the prior
value under a stable registry. It does not establish every call site, when the
game renews identities, allocation/deallocation semantics, per-frame timing,
thread safety, or lifetime validity of a returned unit. Finite wrap permits an
old encoded value to match again; handles must not be treated as globally unique
for all time. The full `003220E0` operation remains outside this execution.
