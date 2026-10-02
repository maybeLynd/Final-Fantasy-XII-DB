# Consumer check: 20-Platform contradictions from a cloud reconstruction-readiness map, settled at the bytes, OPUS's share applied (OPUS, 2026-10-02)

Board task OPUS-RE-READINESS-20-VALUES-1002. Cloud wave 5 mapped `20-Platform-Online-Achievements/` from a text
snapshot (session `session_012aVGLuf29A9aQWEkT3c5Vr`; report `cloud-reports/re-readiness/20-platform.md` in
maybeLynd/Final-Fantasy-XII-DB; rated MOSTLY). Its 15 value items were page-text only. A local read-only pass decided
14 of them at the shipping image; one is undecidable statically. OPUS re-checked the deciding instructions
(`platform_check.py`).

What the bytes show:
- The counter contract's arm-table rows 4-7 are shifted by one; the catalogue is right.
- Mode 0 is a signed compare, not unconditional.
- Kinds 2 and 4 both clamp a negative sum to 0.
- The id bounds are 30 and 31.
- Counter 11 takes the per-award increment, not the clamped total.
- The ten MONSTER marks have a producer: the mode-7 arm.
- There are 11 accumulating descriptors, 21 Steam interface strings and eight tag families.

The pass drafted 51 strike edits (`apply_20platform.py`). OPUS applies the 42 on its own lines
(`apply_by_owner.py OPUS`). The rest go to their owners as requests:
- 3 to FABLE, on the Steam contract;
- 4 to SWE2-CONTRACT, on its arm-table rows;
- 2 to SWE2-DATA, on its lines, plus a regenerate note for a member TSV comment.

- **Affected:** 20-Platform-Online-Achievements/CONTRACT-achievement-counters.md, 20-Platform-Online-Achievements/README.md, 20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the counter contract, the README and the catalogue (OPUS lines) | revised-here |
  | the Steam contract (FABLE-led) | routed-to-FABLE (request with `apply_by_owner.py FABLE`, 3 edits) |
  | the arm-table rows 4-7 (95b1f3a4c) | routed-to-SWE2-CONTRACT (request with `apply_by_owner.py SWE2-CONTRACT`, 4 edits) |
  | DATA's controller-poll and id-31 lines, and the member TSV's "dead data" comment | routed-to-SWE2-DATA (request with `apply_by_owner.py SWE2-DATA`, 2 edits; regenerate the TSV) |
  | RE repo `docs/readiness/20-platform.md` | routed-to-OPUS (filed from this commit, with the byte verdicts) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-platform-readiness-fixes-1002/platform_check.py, verified at 80da775cb: 6 instructions decode as cited, FAILS 0 ([`platform_check.out`](platform_check.out)). `apply_by_owner.py OPUS` re-runs as ALREADY (42), FAILS 0.
