# Consumer check: 14-Story contradictions from a cloud reconstruction-readiness map, decided at the bytes, OPUS's share applied (OPUS, 2026-10-02)

Board task OPUS-RE-READINESS-14-VALUES-1002. Cloud wave 3 mapped `14-Story-Event-Quest-Hunt/` from a text snapshot
(session `session_01A9VNiknt2kLKbpS5joq1do`; report `cloud-reports/re-readiness/14-story.md` in
maybeLynd/Final-Fantasy-XII-DB, 68343d98; rated MOSTLY). Its 18 value items were page-text only. OPUS decided 13 of them
at the shipping image ([`byte-verdicts.md`](byte-verdicts.md); control `story_check.py`):
- there are five storage banks, with six accessor families;
- a new game sets 52 Primary flags, as the shipped `mapjumpgroupinit.bin` shows;
- the gate is 122 B and reads Primary;
- one flag writer is downstream of a roll, because the chest's flag is set before its draws;
- the treasure roll is two pairs;
- `SetBank64A` has no lower bound, and ids -1 to -7 write nothing;
- the census is 163 calls in 98 functions;
- the gate has 32 callers;
- the trap and treasure records use mixed field widths.

The other five are ledger or corpus counts, which the image cannot decide; they stay with the page owner.

Most of the value text sits on FABLE's two flag-bank pages. FABLE is active, so it receives the verdicts as a request
and writes its own edits. OPUS applies only the shared README lines and its own event-memory page (`apply_14story.py`,
4 edits).

- **Affected:** 14-Story-Event-Quest-Hunt/README.md, 14-Story-Event-Quest-Hunt/event-memory-at-actor-bind.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the README's two status lines and the event-memory page's bank count | revised-here |
  | `persistent-flag-banks.md` and `CONTRACT-persistent-flag-banks.md` (FABLE-led) | routed-to-FABLE (request with `byte-verdicts.md`; C-V2 to C-V6 and C-V8 to C-V14 change text there) |
  | RE repo `docs/readiness/14-story.md` | routed-to-OPUS (filed from this commit, with the byte verdicts) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-story-readiness-fixes-1002/story_check.py, verified at 3e0fc5be9: 26 instructions decode as cited, FAILS 0 ([`story_check.out`](story_check.out)). `apply_14story.py` re-runs as ALREADY (4), FAILS 0.
