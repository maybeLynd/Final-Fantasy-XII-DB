# Reconstruction readiness, pass 2: `FFXII TZA/11-Party/`

| | |
|---|---|
| Stream | R2 (reconstruction readiness, pass 2), per [`docs/cloud-briefs/re-readiness-r2.md`](../../docs/cloud-briefs/re-readiness-r2.md), part A |
| Session | FABLE r2-12 |
| Date | 2026-10-03 |
| Snapshot | this repo at `b23bdddd` (synced from XIIOnline `f9d9053b9`); pass 1 read `df2c9f47` |
| Pass 1 | [`cloud-reports/re-readiness/11-party.md`](../re-readiness/11-party.md) (2026-10-02) |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every verdict quotes a page with its `page:line` in this snapshot. No executable, Ghidra or live game was used. |

Citation form: `page:line`. A bare file name is a page in `FFXII TZA/11-Party/`; `BSB/` stands for
`FFXII TZA/11-Party/Battle-State-Block/`. Any other page is given as a path from `FFXII TZA/`. The register is
`_index/OPEN-QUESTIONS.md` (`OQ:line`).

**How the verdicts were reached.** I diffed every 11-Party page and the register between `df2c9f47` and `b23bdddd`
(253 lines added, 169 removed). I re-read each passage that a pass-1 item cites, and searched the whole snapshot for
each address a gap names. Where the answer is on a page outside 11-Party, I checked whether that text was already in
`df2c9f47` (`git show df2c9f47:<page> | grep`). If it was, the verdict is **WRONG-IN-PASS-1**: pass 1 scoped itself to
11-Party pages and missed it. If it was added since, the verdict is **CLOSED** or **NARROWED**.

## 1. Summary

**Pass-1 gaps (41: G-1 to G-22 and S-1 to S-19)**

| verdict | count | items |
|---|---:|---|
| CLOSED | 4 | G-2, S-3, S-12, S-13 |
| NARROWED | 8 | G-4, G-6, G-10, G-11, G-14, G-22, S-5, S-10 |
| OPEN | 21 | G-1, G-3, G-5, G-7, G-8, G-9, G-12, G-15, G-16, G-17, G-18, G-19, G-20, G-21, S-6, S-7, S-8, S-9, S-14, S-15, S-16 |
| WRONG-IN-PASS-1 | 8 | G-13, S-1, S-2, S-4, S-11, S-17, S-18, S-19 |

Classes of the 29 OPEN or NARROWED items: **STATIC 21**, **RUNTIME 6** (G-4, G-8, G-15, G-20, G-22, and
S-5's live half is not counted separately), **DATA 2** (G-11, G-21). Six of the eight WRONG-IN-PASS-1 items leave a
**DOC** residue: the answer is on another page and the 11-Party page has no pointer to it.

**Pass-1 contradictions (54: C-V1 to C-V27 and C-B1 to C-B27).** These are not gaps in pass 1's numbering, but each
one is a choice a re-implementer would have had to make, so each gets a verdict too (§2.3, §2.4).

| | CLOSED | NARROWED | OPEN |
|---|---:|---:|---:|
| value-changing (C-V) | 25 | 2 (C-V5, C-V21) | 0 |
| stale / banner (C-B) | 23 | 2 (C-B19, C-B27) | 2 (C-B15, C-B24) |

Almost all were closed by OPUS's dated 2026-10-02 corrections, which struck or annotated the losing side in place.
**C-V19 was settled the other way from pass 1's reading:** the licence board is granted when the preset's LP word is
**not** `0xFFFF` (`the-setsavedata-presets-test-battle-scenarios.md:49`, `:122`).

**New gaps (8):** STATIC 4 (N-1, N-2, N-3, N-8), DOC 4 (N-4, N-5, N-6, N-7). None is RUNTIME or DATA. No register
row tracks any of them.

**Rating: NOT YET (unchanged), but now for one reason instead of two.** Pass 1 had two subsystems at NOT YET.
Control suppression moves to **MOSTLY**: the mask formula, the mode-1 replacement, the publication and the frame
position are all stated, on the capability-policy and world-tick pages that 11-Party points to or should point to.
The **follow formation stays NOT YET**: no page states where a follower is placed. The other five subsystems stay
MOSTLY, with fewer open items than in pass 1 (§4).
