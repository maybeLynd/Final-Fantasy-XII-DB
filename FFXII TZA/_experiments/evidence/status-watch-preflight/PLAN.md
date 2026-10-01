# Status sparse-slot observation preflight

Claim/request: does the authored StatusDefinitionRecord sparse-byte span have a
reader missed by static analysis? Consumer: OPUS types/contracts and FABLE
Status_Periodic_Terminal. The request identifies row3 as Doom and proposes a
watch at row+0x14 during apply/expire, with absence interpreted as authored-dead.

Hypotheses: (1) requested row/coverage does not match the intended status or all
authored slots; (2) a valid read detector observes a selected transition; (3) no
read occurs within a qualified selected observation, leaving other paths open.
Existing hwbp.py only programs execute breakpoints; it cannot yet serve as a
read-watch positive/detection control. No unchanged failing live setup.

Method A is sufficient for row identity, exact populated positions, proposed
coverage and observer capability. Extract one US shipping battle_pack entry,
validate directory+0x40, st2e header/count/stride/data bounds, embedded self IDs
and published timer/mask controls. Preserve exact slice and source hashes. Do
not repeat the static reader census or infer semantic meaning from value range.

Budget: one bounded source entry (under1MiB) and one 32x40B table decode. Controls:
wrong directory, row identity, count/stride, truncation, empty coverage and wrong
status selection must reject. Acceptance: source-bound populated-byte coverage
and explicit instrument limits. Failure: malformed/ambiguous entry/table stops
this method; no automatic C escalation. No game/input/writes/attach or save
changes. Fresh live state identity, real registered->accepted->executed status
trigger, a qualified read detector and normal health/detach controls remain C
prerequisites. A zero hit is never universal dead/unread proof.

## FRONTIER qualification predicate — 2026-09-27 (ASTRA-RETURN-FRONTIER-STATUS-WATCH-PREREQUISITES)

The preflight stands (Stop3/Float26/Doom6 repairs accepted). ASTRA's return narrowed what a
future read-watch must prove; the qualified detector predicate is recorded here so owner,
reviewer and any live preparation agree on it before a C spend.

**Trap semantics (Intel SDM 17.3.1.2):** a data breakpoint is a *trap* — it fires AFTER the
access completes and reports the NEXT instruction's context, not the accessing one. The
proposed watch site `31E241` is a 4-byte `MOVZX [rbp+0x13]`; the next instruction is
`31E245`. Any detector must therefore distinguish the raw trap-context RIP from the
normalized access-PC (the address of the instruction that touched the window). A correct
normalized `31E241` label is not a rejection cause — but a native positive must prove the
trap↔access association; the label alone is not evidence.

**Window discipline:** RW watchpoints fire on writes as well as reads — a hit is not a reader
until access-kind is recorded. The four hardware windows include the extra `+0x13` span; an
access from a *different* RIP that touches `+0x13` only is not a sparse-slot reader and must
not be counted as one. A qualified observation records, per hit: source RIP (raw + normalized),
opcode/decode at that RIP, effective address, access kind (R/W), which hardware window fired,
and the actual width.

**Owner:** OPUS (structural types/contracts). **Reviewer:** FABLE (Status_Periodic_Terminal
consumer) + AUDIT lane acceptance of the predicate. **Remaining requirements before C:**
owner/reviewer agreement on this predicate, a named ordinary save/area/trigger producing a
real registered→accepted→executed status transition, and a native detector that meets every
clause above. No reader, meaning, or absence conclusion is derivable from synthetic criteria;
a zero-hit under a qualified detector still cannot prove universal unread.
