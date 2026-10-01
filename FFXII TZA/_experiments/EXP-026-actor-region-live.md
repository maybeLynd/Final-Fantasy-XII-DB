---
experiment: EXP-026
title: Live kind-3 actor region map across a zone transition
status: VALIDATED — two zone-specific region maps; byte transitions unobserved
date_designed: 2026-09-10
method: C - ordinary UI input and read-only process observation
live_game: true
contract: ../04-Actor-Entity/CONTRACT-actor-record-pool-and-region-map.md
---

# EXP-026 — actor storage in a loaded field and after zoning

OPUS-REQ-ASTRA-ACTORLIVE requests the first live control of the static actor-storage
map. Read one kind-3 actor, anchored independently by active BattleUnit slot 0 and
membership in one of the five manager pointer tables. Preserve the complete manager
header/table and the selected actor header plus embedded arrays. Decode the sequence
from actor byte3 before selecting the extent: sequence5/6 is 0x6E0, sequence7 is
0x668. The predicted pointer deltas at A0/A8/B8/C0 are 4D8/5A0/120/350 for5/6 and
4D8/578/120/350 for7. Record mismatches as findings, not invalid reads.

Capture two seconds at 20Hz before transition and after a visually confirmed zone
change. Record signed cursor +11, wait/resource counts +88/+89 and four separate
bytes +60..63. Snapshot all wait/resource slots so current ordinals can be checked
against their pool, including FF sentinels. Do not infer byte independence merely
from a matching value: a before/after transition may leave these bytes unchanged.

Use the known Stepping save, full executable/module/code qualification, read-only
process handles and fresh foreground/input controls. Reach the nearby Rabanastre
exit using the validated horizontal-camera and one-second movement pulses. Stop
at HP below70, a lost identity/focus/input control, or 12 movement pulses without
the transition. Take a screenshot before adapting direction. No attack, debugger
or process-memory intervention is needed. Preserve unsuccessful route evidence.

After transition, resolve the actor afresh through the active unit and manager
tables. A reused address does not establish continuity of object lifetime; a new
address does not establish that old storage was freed. Label before/after identities
and any missing membership explicitly. Concurrent reads are not an atomic snapshot,
even within the same frame counter value. Repeated matching samples support only
the observed states, not a universal cursor or allocator invariant.

Close only the owned reference process, restore the complete save/config census,
and release runtime. Return the bounded result to OPUS for canonical integration;
this capture alone cannot certify free-list behavior, half-rate timing or lifetime.

## Result and limits

Fresh reference PID11300 loaded the named Stepping save. Before movement, 40 samples
identified active BattleUnit slot0's actor at decimal1734153104, independently present
in manager0's pointer table at ordinal9. One Right camera pulse (1second), followed by
one W movement pulse (1second), crossed the visible Rabanastre boundary. The next
screenshot explicitly names Rabanastre Eastgate. HP remained103 at the captured checks.
No attack, R2 toggle, debugger or process-memory write was used.

After the transition, 40 samples resolved slot0's actor afresh at decimal1734369776,
manager0 ordinal74. The two captures exercise different kind-3 sequences:

| Observation | Stepping | Eastgate |
|---|---:|---:|
| Sequence (`byte3 & 31`) | 5 | 7 |
| Captured record extent | 0x6E0 | 0x668 |
| A0 pointer minus actor base | 0x4D8 | 0x4D8 |
| A8 pointer minus actor base | 0x5A0 | 0x578 |
| B8 pointer minus actor base | 0x120 | 0x120 |
| C0 pointer minus actor base | 0x350 | 0x350 |
| Wait/resource counts (+88/+89) | 8 / 10 | 6 / 8 |
| Sampled signed wait cursor (+11) | 7 | 5 |
| Four bytes (+60..63) | 00 FF 00 00 | 00 FF 00 00 |

All40 samples in each capture match that column. Thus the static per-sequence region
map and array counts have a live positive control in two zone states. The cursor is
within its array in the samples; no drive-loop trace establishes its intermediate
values or half-rate scheduling. The unchanged four bytes do not demonstrate byte
independence, free-list mutations, allocation/recycling, or exclude a competing
interpretation by themselves. Static writer evidence remains needed for those claims.

The changed actor address and table ordinal identify different storage selections;
they do not establish freeing of the old record or lifetime continuity. The capture
does not read the old address after zoning. No allocator/destructor claim is promoted.
The selected actor is Vaan in both visible states, but that is not proof of one
continuously allocated object. These are80 samples across two states, not80 states.

Raw manager tables, actor bytes, typed decodes, frame brackets and instrument hashes
are retained separately from this interpretation in `evidence/EXP-026-actor-region/`.
Full selected .text comparison and watched-module checks passed before and after;
executable SHA256 is73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8.
Reads are non-atomic; matching frame counters do not remove that limitation.

## Cleanup

The original conservative cleanup closed PID11300, then correctly refused to restore
anything because zoning changed FFXII_000 as well as GameSetting.ini. The changed
autosave/config were preserved in ignored local scratch. `restore_after_zone.py`
verified the exact two-file change set, the config's sole LUIDLow difference and the
original backup census, then restored all26 original hashes with no extra files.
The initial guard rejection is retained in the restoration receipt; no runtime claim
remains. OPUS-REQ-ASTRA-ACTORLIVE receives this bounded result for integration.
