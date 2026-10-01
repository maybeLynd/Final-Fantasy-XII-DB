# The REOPENED capability policy page: its trigger, one falsification pass, and the null-leader state narrowed (SWE2-STRUCT for OPUS, 2026-10-01)

Request: OPUS asked for one REOPENED page to be returned through DOCUMENTED, as
[`swe2struct-reopened3-0930`](../swe2struct-reopened3-0930/README.md) did for three pages. The page is
[`capability-inhibition-policy.md`](../../../15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md).
FABLE's ruling ([status-currency-ruling-fable](../status-currency-ruling-fable/README.md), *What this ruling does not
cover*) lets a REOPENED page return through DOCUMENTED only with two things: its reopening trigger resolved, and a
falsification pass. This record supplies both.

The work was done by a Claude session in the SWE2-STRUCT lane, started by OPUS. It used no subagents, no board
operations and no commits. No status word and no front-matter audit counter was edited; the proposals are below.

The page was clean in git when the work started (`git status --short` empty, HEAD `b0524530f`), and nobody else changed
it while the work ran. The page is LF only and stays LF only (1,099 LF, 0 CRLF). `git diff --numstat` gives
**125 added, 12 removed**. Every removed line is kept verbatim under a `~~strike~~` on the page, either whole or split
around an inserted correction.

## (a) The trigger, and whether it is resolved (SWE2-STRUCT for OPUS)

The front matter has `reopened_count: 2`.
1. **2026-09-02, `audit_crossrefs.py`.** The page treated `00377C20` as a WorldAreaField detail (it has 65 callers in 13
   subsystems) and cited `01E0C2C0` as a function (it is data). `reopened_resolved` records both corrections, and §10
   re-derived them from the graph. **Resolved.**
2. **2026-09-12, ASTRA's original-code falsification (§11).** It found bit-1 polarity and the Immobilize gate scope
   wrong. Both were corrected in §10 and §11. FABLE agreed on 2026-09-12 and OPUS on 2026-09-13 (§12). FABLE
   re-checked on 2026-09-21 that the party page carries the correction (front matter: "PEER CONSUMER PROPAGATION IS
   DISCHARGED"). **Resolved.**

`last_pass_state` names what still keeps the page REOPENED: "THE INITIALIZATION RESIDUE ALONE", routed as
`FABLE-REQ-ASTRA-LEADER-STATS-NULL`. That residue is register row **UQ-147**.
- **Register state:** `SUPERSEDED 2026-09-26 (FABLE, Claude Opus 5.5) under the runtime rule`.
  - Static half done: the null branch reaches the unguarded read, and the mode-1 counterpart is the Esper summon's
    acting member `+0x5AD5`.
  - Live half: carried by `FABLE-REQ-ASTRA-LEADER-STATS-NULL` (board: BLOCKED, P2) and
    `FABLE-REQ-ASTRA-UQ147-KO-SUMMONER-DURING-A-SUMMON` (board: READY, P3).
- **Under FABLE's ruling:** "SUPERSEDED under a class-1 ruling or the runtime rule takes the question out of the
  required scope. The runtime remainder is admissible, but not required." The live request is admissible, but it no
  longer keeps the page's scope open. **The trigger is resolved.** `documented_rule.py` gives READY both before and
  after this work (no open box, no live register id).

**The static half, narrowed further.** OPUS asked who can store the null leader state, and whether an initialised path
reaches it. Both are now pinned (checks L1 to L11):
- **Who stores it.** The only store of zero into a BattleUnit's `+0x698` is `BattleUnit_ResetStateForReuse`
  (`00236AB4`). On the same straight line, that function first clears unit flag bits 2 and 3 (`00236AA6`).
- **Why the leader can never have it.** `BattleUnit_GetPartyLeader` (`003272A0`) returns 0 unless flag bit 3 is set.
  In the typed BattleUnit census, bit 3 is set only at `00233B4B`, which is reached only when bit 2 is already set.
  Bit 2 is set only at `0023AC56`, which comes after the re-arm `0023ABFA`, and `r15` there is never zero.
- **So no initialised path reaches it from an enumerated writer.** A unit `0023B040` reads as the leader always has a
  non-null `+0x698`. The pool also starts as zeros (`memset`, `00236943`).
- **It also breaks FABLE's 2026-09-20 "condition (2) holds".** During the reset window, the re-applied unit's bit 3 is
  clear, so `0023B040` leaves at `0023B08F`. Corrected on the page under a strike.
- **Blind spots:** register-valued flag writes outside the typed census, bulk copies into a unit, and concurrency.
  The live request stays open as admissible; by ASTRA's accepted rule, a no-hit still proves nothing about every state.

## (b) The falsification pass (SWE2-STRUCT for OPUS)

Recorded on the page as "Falsification pass 2026-10-01 (SWE2-STRUCT for OPUS)".

- **Claim attacked:** §2's mechanism. `00313A00` publishes row-2 bits 0-8, 10, 11, 12 and 20, and through `01E0C2C0`
  they inhibit exactly UI requests 1, 2, 3, 5, 14 and 21. The pass also attacked §7's C-7 writer census and the
  `002E1CD0` polarity. This is the page's headline: the lede, the first and third evidence rows, and the C-7 register
  answer all rest on it. No earlier pass re-decoded `00313A00`'s arguments.
- **Attack:** a constant tracker over every call `00313A00` makes, including the two through registers, and the table
  decoded from its bytes. Both were compared with the page, entry by entry.
- **Positive control:** the same tracker gives row 1 bit 21 at the four Save/Load sites the page read by hand, with the
  page's set / clear split (P1). The table hashes to the page's SHA-256 (P2).
- **Result: CORRECTED.**
  - **Survives:** the table (F1), the 22-bit walk (F2), the row-2 bit set (F3), the request set (F6), and the 29 sites
    in 25 functions (F8).
  - **Corrected:** bit 5 of row 2 is a selection bit like 0, 2-4 and 6-8, written at `00313AA0`–`00313AA8` (F4). The
    tail `002E1C40` writes the words `0215F1AC` / `0215F1B4`, never the policy table (F5). `002E1CD0` clears its mask
    when `ecx != 0` and sets it when `ecx == 0`; the 2026-09-18 read had this reversed (F7).
  - **Struck and re-stated in place:** §2's tail sentence, §7's C-7 writer sentence, and the evidence-only read's
    polarity.

## (c) Residue without an id (SWE2-STRUCT for OPUS)

Found with `grep -n -i` for *not read, not yet, unresolved, still open, stays open, remain open, unknown, not
established, not shown, residue, still owed, not exercised, does not establish, still requires, not queued*. Line
numbers are those at the start of the work.

| line | sentence | disposition |
|---|---|---|
| 643 | "Related party-control prose still requires peer propagation" | STALE: pointer added (discharged 2026-09-12 / 13, the box in §11, front matter) |
| 717 | "The mask-1 aggregate bit-0 callback branch was not exercised" | **RESIDUE, answered statically** (M1). `003592C0` calls `0026D6D0` on actor `[022C7FE0]` when bit 0 of the OR of `022C8004`..`022C8007` is set. `0023B040` writes bit 1, so it never decides that branch. Pointer added |
| 754 | "Whether it reaches a KO counterpart during a summon is not queued." | **corrected under a strike**: queued as `FABLE-REQ-ASTRA-UQ147-KO-SUMMONER-DURING-A-SUMMON` |
| 757 | FABLE note: "the event and flag meanings ... remain open" | STALE: pointer to `UQ-195` (ANSWERED 2026-09-17) |
| 766 | "The two preconditions stay open on their own rows: UQ-193 ... UQ-194" | STALE: pointer (both ANSWERED 2026-09-27) |
| 803, 806 | "the initialization invariant §11 leaves open"; "Not established by this review" | carried by UQ-147; pointer added to the new narrowing |
| 853-857, 919-927 | "What is still NOT established ... exactly two things"; "condition (2) holds" | condition (2) **corrected under a strike** (it fails at `003272CB`); condition (1) is moot for the leader read |
| 951 (heading) | "the static side is closed" | pointer added under the heading (the static side was taken one step further) |
| 457 | "what the achievement code does with the answer is not read" | BOUNDARY: a caller of a cited reader, with the reason stated on the page; it belongs to the achievements page |
| 504, 589, 608 / 614, 700, 723, 735, 891, 971 | SD-3 (established), the ticked §10 boxes, UQ-148 / UQ-147 dispositions, "No claim is made", the no-hit rule | carried: answered or id-bearing |

**Proposed register rows: none.** Every id-less residue sentence was stale, answered here, or a stated boundary.

## (d) crossref_clean (SWE2-STRUCT for OPUS)

`crossref_clean: false` gates AUDITED, not DOCUMENTED. SWE2-DATA set it on 2026-09-30, under
`OPUS-REQ-DATA-PASS30-CROSSREF-CLEAN-0930` (board: DONE). It waits on the pass-22 UNACCOUNTED NEIGHBOUR findings.
**That debt is still open:**
- [`pass22-debt.tsv`](../pass22-debt-0929/pass22-debt.tsv) carries 21 layer pairs for this page (461 edges, created by
  `folder:15-Input`).
- The routing ([`routing.md`](../pass22-debt-0929/routing.md)) gives `folder:15-Input` to SWE2-DATA under
  `FRONTIER-REQ-SWE2-DATA-PASS22-DEBT`, which is READY and not done.
- [`neighbour-dispositions.tsv`](../neighbour-dispositions.tsv) has no row for this page.

This record does not touch the debt; it leaves `crossref_clean` false.

## For OPUS: proposed status line and audit values (SWE2-STRUCT for OPUS)

| field | proposed |
|---|---|
| `status:` | `status: DOCUMENTED` |
| `audit.passes` | `4` |
| `audit.last_pass` | `2026-10-01` |
| `audit.last_pass_kind` | `falsification` (a new key, as on the three sibling pages) |
| `audit.last_pass_state` | `swe2struct-falsification-2026-10-01 - row-2 bit set, 01E0C2C0 projection and request set {1,2,3,5,14,21} SURVIVED; C-7 bit-5 attribution, the 002E1C40 tail wording and the 002E1CD0 polarity CORRECTED; both reopening triggers resolved; the initialization residue is UQ-147, SUPERSEDED under the runtime rule (live remainder admissible: FABLE-REQ-ASTRA-LEADER-STATS-NULL, FABLE-REQ-ASTRA-UQ147-KO-SUMMONER-DURING-A-SUMMON); null leader unreachable under the typed BattleUnit census (GetPartyLeader bit 3, reset clears bits 2 and 3 before nulling +0x698)` |
| `audit.crossref_clean` | unchanged, `false` (pass-22 debt open, `FRONTIER-REQ-SWE2-DATA-PASS22-DEBT`) |
| `audit.reopened_count` | unchanged, `2` |

The pass CORRECTED claims, and the corrections are applied with their regression. As with the sibling record, OPUS
decides whether a corrected pass counts toward DOCUMENTED or is itself a reopening that needs another pass.

**Routed, not edited** (see [`consumer-check.md`](consumer-check.md)):
- Register row **C-7** says "one condition for all but 1 / 5 / 10". It should read "all but 1 / 10": bit 5 is in the
  selection set, and `002E1C40` writes `0215F1AC` / `0215F1B4`.
- Register row **UQ-147** says "whether it reaches a KO counterpart during a summon is not queued". It is queued as
  `FABLE-REQ-ASTRA-UQ147-KO-SUMMONER-DURING-A-SUMMON`.
- The shared-neighbours page ties `002E1C40` to "the policy page's inhibit bits". F5 shows it never writes the policy
  table.
- For FABLE / ASTRA: the `LEADER-STATS-NULL` row in `fable-astra-live-facts-0930` and the board request call the
  question a single path-satisfiability question. Condition (2) fails at `003272CB`, so a live hit would now show a
  flag-word writer outside the typed census.

## Receipts (SWE2-STRUCT for OPUS)

| script | result |
|---|---|
| [`cap_policy.py`](cap_policy.py) ([`cap_policy.out`](cap_policy.out)) | C0, P1-P2, F1-F8, L1-L11, M1: 23 checks, run: cap_policy.py at 48557d9d2 (FAILS 0) |
| `documented_rule.py` ([`documented_rule.out`](documented_rule.out)) | READY, `TALLY READY=1 of 1`, FAILS 0 |
| `check_questions.py --db "FFXII TZA"` | "questions consistent: the table and the document checklists agree" |
| `check_links.py` | no broken link on the page |
| [`consumer-check.md`](consumer-check.md) | the five corrections on the page, and their consumers |

Inputs: the certified image `73461d08…` through `retool.py` / `rc9_channels`, and the typed census
`04-Actor-Entity/Battle-Unit/battle-unit-accesses.tsv`, which is read only.

**Blind spots:**
- **F3-F5:** the tracker is linear and path-insensitive. It works here because `00313A00` sets every argument just
  before its call; P1 shows it on two other functions.
- **L5:** covers the flag-word writes the typed census holds. L10 widens the immediate setters to every function that
  touches `+0x698`, but not the register-valued ones.
- **L11:** a direct-call closure. It found no indirect call in the five closures.
- **Not modelled:** bulk copies into a unit, and another thread.
