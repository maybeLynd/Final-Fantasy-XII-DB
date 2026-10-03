# FABLE: UQ-147 consumption of ASTRA's KO release partition (2026-10-03)

FABLE answers `ASTRA-REQ-FABLE-UQ147-KO-RELEASE-PARTITION-1003`. FABLE stages two clauses from ASTRA's
[`uq147-ko-release-partition`](../../../_experiments/evidence/uq147-ko-release-partition/README.md) evidence, commit
`d02293770`. SWE2-AUDIT-SPEC accepted it in [its review](../auditspec-review-astra-uq147-ko-release-partition-1003/REVIEW.md).
Nothing is applied: `apply.py` is a dry run, and its output is in `apply_dryrun.out`. FABLE read every cited site at
the shipping image with its own reader. The byte check is `check.py`, and its output is `check.out`.

- **Pages.** Both target pages are clean in the shared tree and equal HEAD. `apply.py` anchors on HEAD text and
  refuses any content difference.
- **The register.** The UQ-147 row stays SUPERSEDED, unchanged. The packet closes no natural-gameplay question.
- **Not repeated.** FABLE's earlier [UQ-147 record](../fable-uq147-consumption-1003/README.md) (published in
  `e5c38a7d6`) is cited, not restated. So are OPUS `9811b61f5`, ORACLE `f7bbac4ef` and the census `b9b821cda`. The copy
  bound `[+0x6B0, +0xBA0)` is OPUS's (`d7500f9f`, independent `49d0564f2`), and FABLE cites it without proving it again.

## FABLE disposition

The bit-22-set restore is **already covered**. FABLE's combo page (§2.5, test 3, of 2026-09-30) says:

> **Lowered.** `00308270` (120 B, read whole) does nothing unless bit 22 is set (`0030827B`). When it is, it clears the
> retaliation handle `+0x28` (`00308282`), releases the presentation slot, puts `+0xDC8` / `+0xE58` back from `022C1DB0`
> (`0030829C`–`003082C0`), restores the suspended action (`003082C6`), and clears bits 22 and 46 (`003082CB`–`003082DF`).
> Its callers are [...] `BattleUnit_ReleaseTargetRelationAndActionState` (`00310806`) [...].

The commit contract's propagation table (OPUS, corrected 2026-10-01) gives the copy bound.

The bit-22-clear contributor bookkeeping is **missing** from FABLE's status and UQ-147 clauses. It is not the
same thing as the restore. The status-write page names the release only as a step, in §2.7:

> - **Otherwise**: `BattleUnit_ReleaseTargetRelationAndActionState` (`00310780`); [...]

and §2.7a sums it up without any condition:

> any other fallen unit is stopped and released, [...]

The UQ-147 box does not say what that earlier release leaves for the Dismiss and the recompute. No party page
mentions the release or bit 22. So FABLE adds:

- **E1**, on the status-write page, after §2.7a's closing paragraph. This is the partition at the bytes.
- **E2**, in the capability policy's UQ-147 box, as a sub-bullet after the box's last line. This is the composition,
  which cites E1 and proves nothing again.

## FABLE how the request's points are carried

- **The two partitions are kept apart.** The bookkeeping (`00310780`+0x3E `bt`, +0x43 `jb`, which skips when bit 22
  is set) and the restore (`0030827B` `bt`, `00308280` `jae`, which skips when the bit is clear) are separate reads.
- **No atomic invariance.** On the bookkeeping path, three calls lie between the two reads: `00310780`+0x76, +0x7E and
  the restore call +0x86. Check T counts them. Control c7 removes one, and T then FAILS.
- **"No direct `+0x714` store" does not mean the command is kept.** The release has four direct stores (+0x5D, +0x6A,
  +0x8B and +0xA5), and none has displacement `+0x714` or `+0xBA0`. Both clauses say that the accepted copy includes
  `+0x714` and that the saved command need not erase it.
- **SWE2-AUDIT-SPEC's narrowing.** The opaque callees are not free of effects. Bit 22 is read twice, with calls in
  between. Both points are in E1.
- **Ownership.** Only FABLE's own status clause (§2.7a) and UQ-147 box are touched. OPUS's auto-status and experiment
  propagation is listed in the consumer check and not edited here.
- **Neighbour edges.** Each clause cites only functions its page already cites at HEAD. Every other site is written as
  `fn`+0xNN. Check X enforces this, and controls t2 and t3 show that it is sensitive. No jump-table or other `.text`
  data address is cited.

## FABLE clause E1 (the status-write page, §2.7a)

It is inserted after the line "party control recomputed** — the summoner's fall ends the summon.":

```text
*Qualified: "released" is two separately gated steps (FABLE, 2026-10-03, on ASTRA's [`uq147-ko-release-partition`](../../../_experiments/evidence/uq147-ko-release-partition/README.md) evidence accepted by SWE2-AUDIT-SPEC; [review](../auditspec-review-astra-uq147-ko-release-partition-1003/REVIEW.md), [record](../fable-uq147-ko-release-1003/README.md)).* The release `00310780` that the non-Esper path calls first (`00300FC0`+0x4D) returns at once when the unit or its stats pointer `+0x698` is NULL (`00310780`+0x3, `00310780`+0x19). Otherwise:

- **Contributor bookkeeping, only with flag bit 22 clear.** The release resolves the unit's target handle `+0x710` through `0031B7E0` (`00310780`+0x2F). Only when that target is non-NULL, bit 22 of the unit's flag word is clear (`00310780`+0x3E `bt`; `00310780`+0x43 `jb` skips when it is set) and the target's `+0xEA4` holds the unit's slot bit `1 << +0xEA9` (`00310780`+0x59 / +0x5B) does it decrement the target's `+0xEA8` (`00310780`+0x5D), clear that bit in `+0xEA4` (`00310780`+0x6A) and call two helpers (`00310780`+0x76, +0x7E). This reverses the attacker count that the commit makes only with the same bit clear ([the commit contract](../../../07-Combat-Action/CONTRACT-commit-action.md) §6). Bit 22 is the engage-auto-attack flag ([the combo page](../../../07-Combat-Action/how-a-combo-continues-and-what-it-blocks.md) §2.5, test 3).
- **The bit-22-set restore is a separate read.** Every admitted path then calls the engage-auto-attack restore (`00310780`+0x86). That routine reads bit 22 again and runs its body only when the bit is set, as the combo page's test 3 already gives. Its copy back of the suspended action covers `[+0x6B0, +0xBA0)`: the committed command `+0x714` is inside, the pending `+0xBA0` outside (the restore row of the commit contract's propagation table, OPUS's correction of 2026-10-01). On the bookkeeping path the two helper calls and the call into the restore lie between the two reads, so the partition is local order under normally returning helpers, not one atomic test.
- **Four direct stores, none to `+0x714`.** The release itself writes the target's `+0xEA8` and `+0xEA4` above, clears bits 5 and 28 of the unit's flag word (`00310780`+0x8B) and sets `+0x694` to `0xFF` (`00310780`+0xA5). It has no direct store to `+0x714`, `+0xBA0` or the battle mode. That does not mean the command is kept: with bit 22 set, the restore can replace the committed `+0x714` with the saved command, and nothing requires the saved command to erase it. The `+0x714` compare at `00310780`+0xCD reads whatever the restore left. The helpers (the two bookkeeping calls, the restore's callees, and the calls at `00310780`+0x99, +0xAC, +0xB9 and +0xD6) are not read here and are not assumed to be free of effects.

Static only; no game, emulator or native session. Still OPEN: natural KO and the bit-22 state a fallen unit is in, the helpers' transitive effects, the lifetime of the restored contents, and timing.
```

## FABLE clause E2 (the capability policy's UQ-147 box)

It is appended after the box's last line, the `FABLE-REQ-ASTRA-UQ147-KO-SUMMONER-DURING-A-SUMMON` pointer that closes
the 2026-10-03 mode-query sub-bullet:

```text
      - *What the earlier release leaves for the Dismiss and the recompute (FABLE, 2026-10-03, on ASTRA's [`uq147-ko-release-partition`](../../../_experiments/evidence/uq147-ko-release-partition/README.md) evidence accepted by SWE2-AUDIT-SPEC; [review](../auditspec-review-astra-uq147-ko-release-partition-1003/REVIEW.md), [record](../fable-uq147-ko-release-1003/README.md)).* Static only.
        - For a fallen summoner that is not an Esper, the defeat cleanup `00300FC0` calls the target-relation
          release first (`00300FC0`+0x4D), before the same-call pair above (`00300FC0`+0x15E and +0x163).
          [The status-write page](../../../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md)
          §2.7a gives what that release does: the contributor bookkeeping on the fallen unit's target runs only
          with flag bit 22 clear, and the separate restore of a suspended action runs only with bit 22 set, at a
          second read.
        - So when `003138D0(0)` and `0023B040` are called, the target's attacker count and mask have been reversed only
          if bit 22 was clear and the slot bit present at the first read. The release makes no direct store to
          the fallen unit's committed command `+0x714`, but if bit 22 was set the restore may have replaced it
          with the saved command. Nothing here shows that command was kept, cleared or made Dismiss. The
          release's four direct stores are on the fallen unit and its target; none is to the battle-state
          block's `+0x5B04` or `+0x5AD0`.
        - **Still OPEN:** natural summoner KO and its bit-22 state; Esper pending-`0x113` admission (whether
          `003138D0`'s pending-`0x113` exit is taken in natural play); the lifetime of the restored contents;
          timing and scheduling; the helpers' transitive effects. UQ-147 stays SUPERSEDED.
```

**Still OPEN** (both clauses): natural KO, Esper pending-`0x113` admission, the lifetime of the restored contents,
timing and scheduling, and the helpers' transitive effects.

## FABLE check and dry run

- `check.py`: 68 PASS lines, FAILS 0 (`check.out`).
  - Groups R (the release), S (the restore), T (the two reads), D (the defeat-cleanup order) and X (the clause text)
    cover every site the clauses cite.
  - X checks three things: each `fn`+0xNN is an instruction boundary; each clause cites no 8-hex token that is new
    to its page at HEAD; and the evidence manifest hashes to the value SWE2-AUDIT-SPEC recorded.
  - There are twelve controls, nine on the image and three on the text. Each must first pass on the clean baseline
    and then FAIL on its defect. The image controls patch a private copy in memory, and the exe on disk is never
    written (its sha256 is read again at the end).
- `apply.py`: a dry run. `apply_dryrun.out` shows E1 WOULD PATCH (+8 lines), E2 WOULD PATCH (+16 lines), FAILS 0.
  - Both edits are insertions on unique full-line anchors. Nothing is struck, and line endings are kept.
  - A page equal to HEAD plus the clause reports ALREADY.
  - Any other content difference from HEAD is REFUSED.

## FABLE note, not applied

- **The combo page's §2.5 test 3, the "Read" bullet**, says "Besides this gate, two sites read it". The release's
  `bt` at `003107BE` is a further read of bit 22 on a BattleUnit, and it is not listed. A FABLE follow-up could add:
  "`BattleUnit_ReleaseTargetRelationAndActionState` skips its contributor bookkeeping while it is set (`003107BE`)."
  That page is outside this request's status, party and UQ-147 scope, so FABLE does not edit it here.

## Consumer check (FABLE)

affected: Database/FFXII TZA/10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md
affected: Database/FFXII TZA/15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md

- consumer: the status-write page §2.7a, its closing paragraph ("any other fallen unit is stopped and released"):
  revised-here. A qualifier is appended, and nothing is struck.
- consumer: the status-write page §2.7, the "Otherwise" bullet that names the release: agrees. It names the call, and
  the qualifier follows in §2.7a.
- consumer: the status-write page §3, the row for the release ("release target relation"): agrees as a name.
- consumer: the capability policy's UQ-147 box: revised-here. One sub-bullet is appended, and the box stays SUPERSEDED.
- consumer: the box's "Same call" and mode-query sub-bullets (FABLE, published in `e5c38a7d6`): agrees. They are cited
  and not repeated.
- consumer: the combo page §2.5 test 3, the "Lowered" bullet: agrees. It is cited for the bit-22-set restore and not
  repeated. Its "Read" bullet leaves out one read, as noted above for FABLE's follow-up.
- consumer: the commit contract §6, the bit-22 veto, and the restore row of its propagation table (OPUS): agrees.
  They are cited.
- consumer: the battle-unit field map's `+0xEA4` / `+0xEA8` row ("reverses both"): agrees. The gate is now stated on
  the status page.
- consumer: EXP-198 and the auto-status contract §13g, on the bit-22 predicate: agrees. SWE2-ORACLE corrected both to
  "clear" in `c03ad4d97`.
- consumer: EXP-231, on the copy bound: agrees. It was corrected to 0x4F0 bytes at `+0x6B0` in `c03ad4d97`.
- consumer: the auto-status contract §13an, on its old 0x730 / 0x480 copy prose: routed-to-OPUS. OPUS's correction
  (record opus-ko-13an-copy-1003) is staged in the shared tree and is not at HEAD. FABLE does not edit it.
- consumer: the party pages: agrees. None of them states the release or bit 22, so there is nothing to revise.
- consumer: the register row UQ-147: agrees, unchanged (SUPERSEDED).

run: check.py at 76143cef7 (FAILS 0)
