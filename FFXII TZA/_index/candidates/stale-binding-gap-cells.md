# Binding-gap cells that contradict their own row (OPUS, 2026-09-25, block 259)

`goal_gate.py` names the next action from each row's **binding gap** cell. **23 of those cells contradict other cells
of the same row** in `_index/L2-VERDICTS.md`. The detector is two literal rules, applied by script to the table:
- **types-short:** the gap says `types PARTIAL`, `types NOT MET` or `type-resolved`, while the row's **types** cell
  reads MET;
- **nothing-executed:** the gap says `nothing executed`, `nothing in it is executed` or `unexecuted`, while the row's
  **runtime** cell reads MIXED or PARTIAL (i.e., not NOT MET).

The cells are AUDIT-SEM's. This note changes nothing in the table and scores nothing.

| row | types cell | runtime cell | stale gap text (start) | rule(s) |
|---|---|---|---|---|
| S-04 | MET | MIXED | validator arms 2–32 unexecuted | nothing-executed |
| S-05 | MET | MIXED | types PARTIAL and nothing executed | both |
| S-07 | MET | MIXED | types PARTIAL and nothing executed | both |
| S-08 | MET | MIXED | the pump, requester and builder are all unexecuted | nothing-executed |
| S-11 | MET | NOT MET | types PARTIAL and nothing executed | types-short |
| S-15 | MET | MIXED | … BattleUnit is 4 of 177 rows type-resolved | types-short |
| S-19 | MET | MIXED | types PARTIAL and nothing executed | both |
| S-22 | MET | NOT MET | types PARTIAL, runtime ASTRA/ORACLE's gap | types-short |
| S-24 | MET | MIXED | types PARTIAL and nothing executed | both |
| S-25 | MET | MIXED | types PARTIAL and nothing executed | both |
| S-26 | MET | MIXED | types PARTIAL and nothing executed | both |
| S-27 | MET | PARTIAL | types PARTIAL and nothing executed | both |
| S-28 | MET | MIXED | types PARTIAL and nothing executed | both |
| S-29 | MET | MIXED | runtime only … nothing executed | nothing-executed |
| S-30 | MET | MIXED | types PARTIAL and nothing executed | both |
| S-32 | MET | MIXED | types PARTIAL and nothing executed | both |
| S-38 | MET | MIXED | types PARTIAL and nothing executed | both |
| S-41 | MET | MIXED | types PARTIAL (Category 11 of 20 DISCOVERED) and nothing executed | both |
| S-42 | MET | MIXED | types PARTIAL, runtime ASTRA/ORACLE's gap | types-short |
| S-43 | MET | MIXED | types PARTIAL and nothing executed | both |
| S-46 | MET | MIXED | the routing is unexecuted; only the algorithms are tested | nothing-executed (*possibly still right: it names a specific unexecuted part*) |
| S-47 | MET | MIXED | types PARTIAL (1 of 5 …) and nothing executed | both |
| S-50 | MET | MIXED | types NOT MET -> PARTIAL … | types-short |

**What the cells would say instead is the scorer's to write.** For rows OPUS has analysed, the per-invariant notes
name the real remaining boundary:

| row | note |
|---|---|
| S-04 | `s04-runtime-per-invariant-exposure.md` |
| S-05 | `s05-runtime-what-has-run.md` |
| S-08 | `s08-runtime-per-invariant-exposure.md` |
| S-14 | `s14-runtime-per-invariant-exposure.md` |
| S-21 | `s21-runtime-per-invariant-exposure.md` |
| S-32 | `s32-runtime-per-invariant-exposure.md` |
| S-47 | `s47-runtime-per-invariant-exposure.md` |
| S-49 | `s49-runtime-per-invariant-exposure.md` |
| S-51 | `s51-runtime-per-invariant-exposure.md` |
| S-02 | `s02-runtime-rejudged-against-exp191.md` |
