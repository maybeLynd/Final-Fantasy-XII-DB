# Consumer check: 09-Combat-AI contradictions from a cloud reconstruction-readiness map, settled at the bytes, OPUS's share applied (OPUS, 2026-10-02)

Board task OPUS-RE-READINESS-09-VALUES-1002. Cloud wave 2 mapped `09-Combat-AI-And-Gambits/` from a text snapshot
(session `session_01FNGRVb6xYymAE7HhAttG93`, report `cloud-reports/re-readiness/09-ai.md` in maybeLynd/Final-Fantasy-XII-DB,
899678f8; rated NOT YET). That session could not see the executable, so all 12 of its value-changing contradictions
were page-text only. A local read-only pass decided 11 of them at the shipping image; C-V11 needs no edit because both
sides are right. OPUS re-read the deciding instructions (`ai_check.py`). Several verdicts go against the side the map
leaned to:

- the gambit pseudocode's highest / lowest seed ternary is reversed (`00301B44`-`00301BF9`);
- the opcode is the high byte of the second word (`00301B14`);
- the AI-suspend bit returns before the `0x414D` exception (`00301511`);
- enmity floors at 1 (`00321923`, `r12d = 1` from `003218DF`);
- an order set has room for 14 records, of which at most 12 are filled (`00328160`, `00328187`);
- the handler table `01EEC460` has exactly 18 zero entries out of 359.

The draft holds 43 strike edits (`apply_09ai.py`). OPUS applies the 13 on its own lines (`apply_by_owner.py OPUS`). The
30 on FABLE-led pages, plus FABLE's one sentence on the gambit-walk contract, are routed to FABLE as a request.

- **Affected:** 09-Combat-AI-And-Gambits/CONTRACT-gambit-walk.md, 09-Combat-AI-And-Gambits/README.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the gambit-walk contract (OPUS-led) and the README | revised-here |
  | `gambit-evaluation-and-enmity.md`, `which-gambit-set-fires-and-how-a-command-switches-it.md`, `CONTRACT-enmity.md`, and FABLE's "Whether the unit arm" sentence on the walk contract | routed-to-FABLE (request with `apply_by_owner.py FABLE`, 30 edits) |
  | C-V11 (`+0xBC0` is the candidate buffer's base, `+0xBC4` its count, `+0xBC8` its entries) | agrees (both sides right, no edit) |
  | RE repo `docs/readiness/09-ai.md` | routed-to-OPUS (filed from this commit, with the byte verdicts) |
  | the map's structural gaps (the two unstated cascade branches, the final target pick, the enemy's initial set C) | routed-to-OPUS (later reads) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-ai-readiness-fixes-1002/ai_check.py, verified at ad7eadd20: 21 instructions decode as cited and `01EEC460`'s zero entries are exactly the 18 ids, FAILS 0 ([`ai_check.out`](ai_check.out)). `apply_by_owner.py OPUS` re-runs as ALREADY (13), FAILS 0.
