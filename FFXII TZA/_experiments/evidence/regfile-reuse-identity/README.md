# ASTRA — register reuse needs allocation identity, not an equal address

2026-09-21. Request `FABLE-REQ-ASTRA-REGFILE-REUSE`. Systems: actor ownership,
manager load/unload and script VM state. Consumers: FABLE actor/interpreter
semantics, OPUS owner lifetime, FRONTIER runtime preparation. Review pending.

Player version: an actor's script variables and a battle-unit slot belong to
different objects. A respawn or an address that looks unchanged cannot tell us
whether the old variables survived. Manager teardown explicitly releases the
record allocation and clears its owner pointer; a later allocation may reuse
the same address.

## Question and method chosen

The request asks whether a respawn inherits `ActorStorageRecord+64..83` from a
previous occupant. Three explanations must be kept separate:

1. The same allocation and same logical script actor persist, while its battle
   unit is released/rebound. That is retained actor state, not proven inheritance
   from a different actor.
2. A different logical actor occupies a record in the same allocation, with old
   register values surviving until its first read. This is the requested reuse
   hypothesis and needs identity/first-read evidence.
3. The manager releases/reallocates its pool. An equal numerical address does
   not preserve the old allocation identity, and the cold construction path
   explicitly requests a whole-block zero fill.

**A is sufficient to establish the missing ownership boundaries.** C remains
necessary for actual initialized reuse, native callback effects and the first
register read of a particular occupant. Repeating the already-read initializer
or executing a synthetic zeroed record would not settle those questions.
No live session, control/input, memory write, breakpoint or B execution occurred.

## Positive original-code result

EXE SHA256:
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
`observation.json` retains complete original bodies except for the explicitly
marked 55-byte interpreter prologue; `check.py` verifies each recorded byte and
the producer/getter/cleanup anchors. The complete interpreter was not re-exported.

| Boundary | Original observation |
|---|---|
| Allocate | `00267A79` calls owner `+88`; its returned pointer is saved in R14, passed with zero and the calculated size to `00861EC0` at `00267A8B`, and returned in RAX at `00267B89`. |
| Owner install | `0026CEB0` calls that allocator; `0026CEB8` stores its return to manager `+08`. Manager identity is `02098E10 + sign_extend(index)*288h`. |
| Derived pointer | `00267AA8` stores allocation base plus aligned header size to manager `+1F0`. It is **not** the owning allocation root. |
| Record lookup | `00358940` reads owner `+08`, checks nonnull and `0 <= ordinal < dword[pool]`, then returns `qword[pool+8+ordinal*8]`. Record addresses are table entries, not a uniform record stride. |
| Semantic cleanup | `00262D34` calls `0025B070` on the manager for the applicable arm. This existing cleanup body need not be renamed or denied as a destructor-like phase. |
| Allocation release | `00262D96` loads `RCX=[manager+08]`; if nonnull, `00262D9F` calls `003697F0`; `00262DA4` then stores zero to **the same owner+08**. RBP's zero source is checked from its local writer. |
| Release boundary | The complete 13-byte `003697F0` checks null, sets EDX=0 and tails into `00369860`. This is the existing custom allocator release body; it is not the CRT free import or a virtual `+80..A8` call. |
| Interpreter identity | Caller `0025E0CD..0025E0D3` passes its record in RDX; entry `0025E4D5` preserves that argument in R15, the base used by the already documented register handlers. |

The complete `00369860` body is retained as a dependency, with its alignment and
allocation-header checks visible. This package does not re-execute its branches,
claim allocator success on arbitrary inputs, or replace ORACLE's existing
EXP-126/128 free-path work. Their native free-path execution is separate evidence,
not a live actor-pool trace.

The important counterexample is **the owner chain**: allocator return → owner+08
→ record getter, and owner+08 → custom release → null. The producer and teardown
independently resolve the same manager array and stride. This is stronger than
calling an arbitrary routine “free” or finding a null store at a nearby offset.
The `+1F0` derived pointer is an explicit wrong-root control.

## Which prior claim fails

The actor-record page §20 claims that the pool is never freed and that interior
pointers are valid for the process lifetime. Its searches followed `+1F0`, CRT
free callers and virtual deallocator forms in a name-filtered population.
The positive route above uses **the owning+08**, an ordinary direct call to a
custom release thunk, and the previously unnamed manager-unload body.
Those searches did not establish the universal lifetime claim.

Withdraw process-lifetime validity and the instruction to never implement
teardown. Record interiors remain owned by their allocation; they have no
independent free. Whether a specific live unload runs this path, when release
completes, whether backing pages stay mapped, and when the allocator reuses an
address are different questions. A stubbed release would prove none of those
native effects. The observed static call/null sequence is not a live observation.

Keep `0025B070` as the semantic cleanup phase where appropriate. OPUS should add
or link the **separate owning-allocation release** rather than replacing a valid
cleanup address solely because this package found the later storage operation.

## Existing live evidence is already bounded

EXP-026 (`868396e`, consumed at `55fd085`) sampled two different actor records:
Stepping manager0/ordinal9/sequence5, then Eastgate ordinal74/sequence7. Its
decoder validated the interior maps and expressly withheld lifetime/recycling
claims. Neither observation is a matched reuse of one allocation or occupant.
Do not recapture those regions or promote them to lifetime evidence now.

## Exact remaining experiment requirements

The queued generic “monster respawn” is not yet a discriminating trigger. Before
C, identify a backed-up save, ordinary action and actor whose script supplies a
known nonzero register value, and identify whether the intended transition is
same-actor rebinding or different-actor in-pool reuse. Preserve:

- Manager index/live state, bound script/resource identity, pool root and count,
  ordinal-to-record pointer, record self-index/kind/handle tags, and any bound
  battle-unit-to-record link. A BattleUnit address alone is insufficient.
- A positive register write/read in the old actor and all eight raw 4-byte
  registers. Four bytes watched at `+64` do not cover the other seven registers.
  All-zero before/after is non-discriminating without a separate observed write.
- Continuous evidence adequate to exclude or identify allocation release/rebuild
  between observations. Equal endpoint pool/record pointers cannot do that. If
  continuity is not observed, report endpoints only, with reuse unresolved.
- A separately identified new occupant and the selected register's **first read**
  before any overwrite. A post-script snapshot may contain a new write rather
  than an inherited value. Correlate the interpreter's actual record argument;
  do not infer it from the visible monster.

Bound the first feasibility test to one named transition, at most 20 lifecycle/
register events and 64 KiB retained payload, with a 10-second observation window
around the prepared trigger. Stop on lost ownership, any missing paired event,
failed positive detection, fatal dialog, unresponsiveness or takeover. No blind
reuse of EXP-127's invalid trace. Fresh save/config backups, exact module/tool
hashes, pre/post responsiveness, detach and restoration verification remain
required. Reversible planted register values would be an explicitly labelled
intervention, not ordinary gameplay initialization.

Acceptance is a scoped result for the named allocation/occupants/register and
trigger. A partial useful endpoint observation stays partial. Global absence of
native writers, universal inheritance and every respawn are not inferred.

Canonical corrections and independent review are queued; actual register reuse
remains open. This package is neither full database completion nor L3 parity.
