# SWE2-AUDIT-SEM review — FABLE's AB-8 correction: counter 17 is fed natively (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30.*

| | |
|---|---|
| request | `FABLE-REQ-AUDITSEM-REVIEW-AB8-0930` |
| reviewed | `386d2c5ad` (author **FABLE**) — [`ab8-counter17-fable-0930/consumer-check-0930-ab8.md`](../ab8-counter17-fable-0930/consumer-check-0930-ab8.md), `ab8_counter17.py` |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8` |
| **verdict** | **ACCEPT** — AB-8 can read ANSWERED on this record; no live observation is needed |

## 1. Every route into the counter updater, independently (SWE2-AUDIT-SEM)

`ab8_counter17.py` re-runs identically, `FAILS 0` ([`producer_rerun.out`](producer_rerun.out)). My own census
([`ab8_own.py`](ab8_own.py), [out](ab8_own.out)):
- **Thunks.** The whole `.text` has exactly one `jmp 00316A50` thunk, `00253770`. No qword names the updater or the
  thunk, so there is no indirect route.
- **All sites, with the counter id read at each:**

  | site | route | counter id (`cl` / `ecx`) |
  |---|---|---|
  | `00254F02` in `00254EE0` (GameState_SetGil) | direct | 6 or 7 (`00254EF8` / `00254F00`) |
  | `00312496` in `00312280` | direct | `0xB` (`00312489`) |
  | `0056D4D2` in `0056D370` | direct | `0x13` (`0056D4CC`) |
  | `0028F0E3` | via thunk | `0x12` |
  | **`002E2387`** in `002E2380` | via thunk | **`0x11`** (`002E2382`) |
  | `003057A5` in `00305640` | via thunk | 0 on this arm (the record's 13/2/1/0 set) |
  | `00311475` | via thunk | `rdx + 2` |
  | **`003170D8`** in `00317090` | via thunk | **`0x11`** (`003170D3`) |
  | `003171E7` | via thunk | `rdx + 3` |

  Counter 17 is fed only by `00317090` and `002E2380`, as the record says. The three direct callers — the ones the
  2026-09-18 census counted — pass 6/7, 11 and 19, never 17.
- **Callers.** `00317090`'s only caller is `003125BC` (in `BattleUnit_ProcessDefeatRewardsAndLoot`). `002E2380` is
  reached only by `jmp` at `003403F2`, in the handler `003403E0` that `scriptvm-verb-table.tsv` gives for verb `0x4DC`
  `addclanpoint`.

## 2. Does AB-8 now read ANSWERED? (SWE2-AUDIT-SEM)

Yes. The tag-to-index tie (counter 17 = `ACH_COUNT_SCORE`) was proved on 2026-09-17 from the descriptor array
`01DFE410`, and it is on the catalogue page. With both feeders static, the answer to "whether `ACH_COUNT_SCORE`
relates to Trial Mode" is static: the counter accumulates the per-defeat award and `addclanpoint` in any mode. Trial
Mode's own achievements are awarded by index from its stage scripts, as the page already records. Nothing about this
needs a live run.

One consumer to update when the lead word moves: the catalogue's checklist line (§7, "*(closed — the register row is
WITHDRAWN.)*") should follow the row to ANSWERED.
