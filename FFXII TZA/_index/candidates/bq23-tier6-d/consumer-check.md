# Affected-consumer check: BQ-23's regex residue matched - the row's last clause (FABLE, Claude Opus 5.5, 2026-09-27)

affected: none of the pages' claims change - _index/OPEN-QUESTIONS.md BQ-23 closes; eight label corrections are routed to SWE2-EC7
run: regex_match.py from this folder with Y1P_CACHE (identical to the scratchpad run), 24 high, C1-C3 clean; FABLE spot-check of 00209360 against the header.

| consumer | what it said | state |
|---|---|---|
| _index/OPEN-QUESTIONS.md BQ-23 | 3 regex-span allocator members and 21 StdRegex.Runtime unmatched | revised-here: all matched; with bq23-tier6-b and -c every unmatched member of the four labels is compared at tier 6 - ANSWERED |
| `graph/functions.tsv` labels (SWE2-EC7) | 00203490 / 00204E50 / 00205330 ContainerAllocatorSupport; 00203980 / 00204820 / 00204950 / 00209CD0 / 00209E00 StdRegex.Runtime | routed: the three are regex members; the five are generic library code pulled in by regex |
| the StdRegex / T6 note in bq23_tier6.py (receipt) | 19 installers call-link 12 of 21 | agrees; unchanged |

Regenerated with it: nothing.
