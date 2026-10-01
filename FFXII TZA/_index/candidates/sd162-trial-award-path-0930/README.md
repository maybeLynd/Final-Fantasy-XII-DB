# SD-162: where the Trial Mode award calls sit in their stage scripts (SWE2-ORACLE, 2026-09-30)

Register row SD-162 (SWE2-DATA) asks whether each Trial Mode stage script's award call lies on the stage-clear path
of its script. The award call is `unkCall_5ad` with index 39 or 40, with 900 sites each in `tri_*`. The row comes from
[steam-integration-and-achievement-catalogue.md](../../../20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md),
in the section on which achievements the scripts award directly.

**Evidence class: script corpus.** This is the shipped `.ebp` bytecode, decoded and analysed statically. There is one
static read of the certified image: the kind-5 path table, used to pair each file with its field number. Nothing here
is native execution or a run-time observation.

- Checker: `sd162_award_path.py`. Its output is `sd162_award_path.out`, which ends `FAILS 0`.
- Per-site table: `sd162-award-sites.tsv`, 1,800 rows.
- The checker reuses FABLE's decoder (`25-EBP-Script-Container/Bytecode-And-Opcodes/members/gen_req_channel_census.py`),
  exactly as `script_award_verb_census.py` does.

## The answer (SWE2-ORACLE)

**Yes. Every one of the 1,800 sites lies after the stage-clear wait, but each site is live in only one stage file.**
The figure of 900 is 100 stage files × 9 language copies. Every file carries one index-39 call and one index-40 call,
both in the same shared director code. Each call sits under a `nowmap()` test, and only one stage's field passes it.

| index | achievement | sites | on the post-clear path | branch guard (every path to the call takes it) | live in |
|---:|---|---:|---:|---|---|
| 39 | `ACH_TRIAL_MODE_50` | 900 | 900 | `nowmap() != 0x51F`, then the tenth-stage set `{0x48F, 0x49F, …, 0x50F}`, then `nowmap() == 0x4CF` | `tri_j05` only (stage 50), 9 copies |
| 40 | `ACH_TRIAL_MODE_100` | 900 | 900 | `nowmap() == 0x51F` (the else arm of `nowmap() != 0x51F`) | `tri_t05` only (stage 100), 9 copies |

**Per stage file:** 2 award sites. In 98 of the 100 stage files both sites are on branches whose guard is false for
that file's own field. In `tri_j05` the index-39 site is live and the index-40 site is not. In `tri_t05` the reverse
holds. Of the 1,800 sites, 18 are live and 1,782 are statically excluded by their file's field number. The 18 are
the 9 language copies of each of the two files.

### How the sites were classified

- **The code that holds them (C1–C6).** All 1,800 calls are in actor `トライアル監督` (trial director), function
  `main`.
  - The totals equal the published census: 900 + 900 in `tri_*`, plus 9 × index 33 in `slm_a01`.
  - `main` is cut into basic blocks through the script's own jump table. Every jump immediate lands inside the function
    (C6).
  - The 900 `main` bodies come in 118 distinct byte strings. The guards are therefore rebuilt from each file's own bytes,
    not copied from one file.
- **The clear wait (W39, W40).** In every file, one `waitv` call dominates both award sites: every path from `main`'s
  entry to an award passes through it first.
  - The call's argument is a `PUSHP` reference. The file's descriptor table (header `+0x28`) resolves it to class 4
    (`scratch1`), offset `0x06`.
  - Neither site is inside a loop.
- **What wakes that wait.** `scratch1 @0x06` is the engine's group-completion post (EE-9 in
  [CONTRACT-group-completion-and-respawn.md](../../../05-Spawn-Encounter-Lifecycle/CONTRACT-group-completion-and-respawn.md)
  and the group-wipe page). When every member of an event group has died, the dispatcher writes the group's number into
  that word, subject to the party-down and time-stop hold. `waitv`'s poll `00354230` keeps the script waiting while the
  word is zero.
  - No `POPV` in any `tri_*` file writes that variable (K4). The only waker in these scripts is the engine's post.
  - The only event group Trial Mode places units in is **group 1** (K5, K6). Every stage file puts at least one unit in
    group 1, for example `tri_j05` 1 and `tri_t05` 5 in the `us` copy. Group 0 is "no event group".
  - **So "stage clear" in these scripts is precisely: every group-1 unit of the stage is dead.** The director then runs
    the aftermath in this order:
    1. `ucoff`, battle suspension, closing the boss gauge;
    2. on every tenth stage a sound (`sebsoundplay(0, 39)`) and an item (`additemmes(0x9123…0x912B)`), with the award as well on
       stage 50;
    3. then the fade and the `mapjump` to the next stage.
  - On stage 100 the director instead sets `scratch1 @0x0C = 1`, awards 40, and after the fade reads event `0x1AB` (`eventread_e8(0, 0x1AB)`); what that event is was not read.
- **Which file is which field (M1–M3).** `nowmap()` is compared against constants, so each file has to be paired with
  its field number.
  - The engine's kind-5 path table (`01E50B70`) is indexed `3 × N` for the map-script slot (`0032FD3F`–`0032FD44`,
    `lea ebp, [r15 + r15*2]`).
  - Its `.ebp` entries place `tri_<g><s>` at field `0x483 + 8·g + (s − 1)` for groups `a`–`t` and stages `01`–`05`,
    100 of 100.
  - So `tri_a01` = `0x483`, which is the field the Trial Mode load route parks on (FV-1). `tri_j05` = `0x4CF` (stage 50)
    and `tri_t05` = `0x51F` (stage 100).
  - The director's own advance, `mapjump(nowmap() + 1)` with `+3` more after each group's fifth field, walks exactly this
    layout.
  - Controls: slot 0 is `tst_a01.ebp`, and `slm_a01`, the only other award file, sits at field 701, inside the Lowtown
    701–708 run.

### Controls

- **K1 (positive).** The nine tenth-stage item rewards `additemmes(0x9123…0x912B)` sit on the same post-wait branch,
  each under its own `nowmap()` test. They resolve to stages 10, 20, …, 90, one each. That is the ladder the ten-stage
  layout predicts.
- **K2.** In `tri_j05` (`us`) the index-39 award has exactly the guard list of `additemmes(0x9127)`, which is the
  instruction just before it.
- **K3 (negative).** The 100 `us` `bossgaugeopen()` calls in the same `main` come before the `waitv`. The dominance test
  does not credit them with the wait (0 of 100 credited).
- **E0.** Every guard on the award sites is decided by `nowmap()` alone. No other variable, verb result or register is
  tested on the way from the wait to the call.

## Consequences for the page (SWE2-ORACLE; routed, not edited)

The page's table reads "Trial Mode stage scripts `tri_*` · 900". That is a count of code copies, not of award points.

- The award points are **one stage each**: index 39 on stage 50 (`tri_j05`, field `0x4CF`) and index 40 on stage 100
  (`tri_t05`, field `0x51F`).
- Each fires on the stage's group-1 completion. It is not tied to anything counted across stages.
- Restating the row and the page line is SWE2-DATA's (request filed).

## Limits (SWE2-ORACLE)

- **Whether a given run reaches the clear is a run-time fact.** The script reading establishes only that the award
  follows the group-1 completion post. It does not establish that a player's run completes group 1 on that stage.
  - A party wipe does not pass through this code. The director is parked on the wait and simply never wakes. Game over
    is native and was not read here.
  - The completion post also carries the dispatcher's hold rules (party-down states, time-stop request 10), which are
    native and live.
- **The field pairing rests on the path table's `3 × N` indexing.** The chain from `nowmap()` to the loader's index was
  not traced as one value in the image:
  - `nowmap()` reads `[002EF2B0() + 0x1044]` through `003148F0`;
  - `0032FCA0` takes the index in `edx`.
  - The table, the control files and the director's own `mapjump` arithmetic agree on the pairing. Proving the two
    values identical would take a static read of `0032FCA0`'s callers, or one live read of `nowmap()` on a Trial stage.
- **`unkCall_5ad`'s native effect is not re-derived here.** Handler `00352250` → `008632B0`, the by-index award, is
  taken from the Steam catalogue page and its contract. Whether the award is already held, or whether Steam stats are
  received when it fires, is `008632B0`'s concern and is live.
- **Only `main` of the director is analysed for the guards.** A second director function, or another actor that
  requests `main` a second time, would not change the guards: the dominance is intra-function. It could change how
  often `main` runs, which this record does not bound. No `tri_*` actor writes `scratch1 @0x06` (K4), and whether any
  other container loaded on a Trial field does was not surveyed.
