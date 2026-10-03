# FABLE: UQ-147 consumption of ASTRA's native relation-cache invariant (2026-10-03)

FABLE answers `ASTRA-REQ-FABLE-UQ147-NATIVE-RELATION-SEMANTICS-1003`. FABLE stages two clauses from ASTRA's
[`uq147-native-relation-invariant`](../../../_experiments/evidence/uq147-native-relation-invariant/README.md) evidence,
commit `86cdcde10`. SWE2-AUDIT-SPEC accepted it in
[its review](../auditspec-review-astra-uq147-native-relation-invariant-1003/REVIEW.md), with no narrowing beyond the
README's own limits. FABLE carries those limits in full. Nothing is applied: `apply.py` is a dry run, and its output is
in `apply_dryrun.out`. FABLE read every cited site at the shipping image with its own reader. The byte check is
`check.py`, and its output is `check.out`.

- **Pages.** Both target pages are clean in the shared tree and equal HEAD. `apply.py` anchors on HEAD text and
  refuses any content difference.
- **The register.** The UQ-147 row stays SUPERSEDED, unchanged. Its live half,
  `FABLE-REQ-ASTRA-UQ147-KO-SUMMONER-DURING-A-SUMMON`, stays OPEN. The packet closes no natural-gameplay question.
- **Not repeated.** FABLE's earlier records are cited, not restated:
  - [UQ-147 consumption](../fable-uq147-consumption-1003/README.md) (`e5c38a7d6`);
  - [KO release partition](../fable-uq147-ko-release-1003/README.md) (`d107fd273`).

  The five earlier positives are not used again. Neither are the accepted copy-bound and bit-22 proofs.
- **Already canonical, so not a new closure.** The notify's target-mask gate and what a zero third argument does are
  in OPUS's [commit contract](../../../07-Combat-Action/CONTRACT-commit-action.md) §13a:

  > **`00313B30` is notify** (§14.3). Target stats null → `r8` decides directly. Stats mask
  > `([+0x64] | [+0x3C]) & 0x80000003` **clear** → collect unconditionally, `r8` ignored; mask set →
  > `00377C20` flag77, pass → collect, fail → `r8 != 0` suppresses and `r8 == 0` collects. [...] The dispatch record
  > is `{+0 kind (self 1 / other 2), +1 flag (`r8 == 0`), +4 uid, +8 aid, +0xC tid}`, handed to `002ED2A0(uid, &rec)`
  > per unit.

  E1 cites that section and proves none of it again. Check group P reads the packet stores only as context.

## FABLE disposition

The native effect is **missing** from every FABLE clause. FABLE's status-write clause of 2026-10-03 (§2.7a, the
release) stops at the boundary:

> The helpers (the two bookkeeping calls, the restore's callees, and the calls at `00310780`+0x99, +0xAC, +0xB9 and
> +0xD6) are not read here and are not assumed to be free of effects.

The capability policy's UQ-147 box does not mention the notification. Neither do the party pages or the combo page.
FABLE's group-completion page (EE-7) reads only the kind-3 arm of the same handler, and a kind-3 record is not this
leg. [The all-ones page](../../../00-Engine-Core-Runtime/the-all-ones-empty-convention.md) §9 gives the pool, its size
and its one-byte links. It does not give the effects, the invariant or the unguarded decrements. So FABLE adds:

- **E1**, on the status-write page, after the closing "Static only; ... and timing." line of the §2.7a release clause.
  This is what the first bookkeeping call's notification does in the native cache, with its premises, its
  counterexample and its limits.
- **E2**, in the capability policy's UQ-147 box, as a sub-bullet after the box's last line. This is the UQ-147
  framing. It cites E1 and proves nothing again.

## FABLE how the request's points are carried

- **A fixed pool and a local remover, not an opaque callback.** The handler and the remover transfer only to each
  other: one call and one tail jump. Check H finds exactly these two transfers out, and control c4 (an indirect call)
  FAILS H. The 26 + 11 write sites are each matched to a named envelope: the receiver's inline block, the pool rows,
  the cursor `02CA83F0` and the counters `02EBA480` / `02EBA481`. Control c6 (a store outside the envelope) FAILS H.
- **The conditional invariant.** Check Q reads the branch polarities from the decoded `jcc`s:
  - creation: `00512F98`, `00512FA0`;
  - the first removal: `00512FF5`, `00512FFD`;
  - the tail removal: `00513010`.

  Q then enumerates the 203 set partitions itself. It finds 20 coherent cases, 0 double removals and 0 invariant
  breaks without a removal, and creation never yields target = recipient. Control c1 reverses the matching-target
  branch and FAILS Q. Control c2 inverts the creation inequality and FAILS Q.
- **Value preservation is read, not assumed.** The remover writes no `rbx`, `rdi` or `r11`. Its stores are all
  one byte wide, at `+0xC`..`+0xF` or at `02EBA481`, so it never writes the identity words. Control c3 moves one store
  onto `+0x8` and FAILS L.
- **The counterexample and the limits.** Q keeps the all-equal flag-1 witness. L checks that the remover's tail is
  straight-line: `and [node+0xF],0xF0`, `dec [owner+0xE]`, `dec [02EBA481]`, `ret`, with no test before the
  decrements. Control c5 inserts a guard and FAILS L. Both clauses say that this is a malformed-state fact, not a
  natural bug.
- **The zero argument reaches this leg.** N checks `00310780`+0x67 `xor r8d,r8d` and that `r8` is not rewritten
  before the call at +0x76. Control c7 FAILS N. W checks that the dispatch reaches the handler on the recipient's
  render record `+0x650`. Control c8 FAILS W. That route is static: whether a live cache is bound there is a premise.
- **The scope of "no import or heap free".** Both clauses limit it to the two bodies. E1 names the other KO helpers
  and the caller flow as not covered. It also says the result proves nothing about initialisation, binding, reuse,
  scheduling or presentation.
- **Ownership.** Only FABLE's own §2.7a release clause and the UQ-147 box are touched. The representation and contract
  wording is OPUS's: the pool record's fields, the cache type, and the EXP-091 stub limit. Those items are routed in
  the consumer check and not edited.
- **Neighbour edges.** Each clause cites only functions its page already cites at HEAD. Every other site is written
  as `00310780`+0xNN. Check X enforces this, and controls t2 and t3 show it is sensitive. No jump table or other
  `.text` data address is cited. Control t4 shows the link check is sensitive.

## FABLE clause E1 (the status-write page, §2.7a)

It is inserted after the line "Static only; no game, emulator or native session. Still OPEN: natural KO and the bit-22
state a fallen unit is in, the helpers' transitive effects, the lifetime of the restored contents, and timing.". The
links below are rewritten to resolve from this record folder (on the page each has one `../` fewer):

```text
*Qualified further: what the first bookkeeping call's notification does in the native relation cache (FABLE, 2026-10-03, on ASTRA's [`uq147-native-relation-invariant`](../../../_experiments/evidence/uq147-native-relation-invariant/README.md) evidence accepted by SWE2-AUDIT-SPEC; [review](../../../_index/candidates/auditspec-review-astra-uq147-native-relation-invariant-1003/REVIEW.md), [record](../../../_index/candidates/fable-uq147-native-relation-1003/README.md)).* The first bookkeeping call (`00310780`+0x76) is the notify of [the commit contract](../../../07-Combat-Action/CONTRACT-commit-action.md) §13a, and the release passes it a zero third argument (`00310780`+0x67 `xor r8d,r8d`). §13a already gives what that argument does: the target's terminal-status mask cannot suppress collection, and every collected record carries flag `+1` = 1, with kind 1 for the acting unit itself or 2 for another member. That is canonical and is not proved again here. What is new is where the records go. [EXP-091](../../../_experiments/EXP-091-commit-callees-exec.md) stopped them at a `ret` stub on the native relation-event handler, which the notify's dispatch reaches on the recipient's character render record at `+0x650` when that record is live. The handler keeps a fixed pool of 32 sixteen-byte relation rows with one-byte links ([the all-ones page](../../../00-Engine-Core-Runtime/the-all-ones-empty-convention.md) §9, "What the pooled record is").

- **A closed local operation, not an opaque callback.** The handler (532 bytes) and its entry-reachable remover (162 bytes) transfer only to each other: one call and one tail jump into the remover. There is no indirect call, no import thunk and no heap free. The two bodies have 26 and 11 persistent write sites, all in the receiver's inline block, the pool rows, the pool's allocation cursor and two global count bytes. Removing a row clears its occupancy nibble; it does not free memory.
- **What a flag-1 record does.** A kind-2 record that matches no row creates nothing, because creation needs flag 0 and a recipient different from the target. On a row matched by kind and actor, the handler first removes the row when its target equals the record's target. It then removes the row, by a tail jump, when the record's recipient equals the record's target. Otherwise it overwrites the row's target with the record's, and it does this even after the first removal, so an inactive row can still be changed. A kind-1 record acts only on the receiver's inline entry. With flag 1 it clears that entry's kind nibble when the entry's target equals the record's, and otherwise it writes nothing.
- **At most one removal on a coherent row.** Take a receiver that is the recipient's own cache (the record's recipient equals the row's), a matched actor, and a row whose target still differs from its recipient, which creation enforces. Then the two removal tests cannot both pass, because together they need row target = record target = recipient. ASTRA's reducer covers all 203 equality partitions of the six identities with flags 0 and 1. Twenty cases are coherent, and none of them removes twice. SWE2-AUDIT-SPEC re-derived the count with its own enumeration. When neither test removes, the new target still differs from the recipient. The remover leaves the handler's receiver and record pointers and the record's values unchanged. That is read from its code under the evidence's disjoint-object premise; it is not assumed from the ABI.
- **The malformed counterexample and the limits are kept.** A row whose six identities are all equal, with flag 1, reaches both removals. The remover does not test occupancy. It clears the nibble and then decrements the owner's count byte `+0xE` and a global count byte without a test, so a second removal turns a zero count into `0xFF`. It never clears the removed row's three identity words or its links, so stale bytes stay in inactive rows. This is a conditional fact about malformed state. It is not a claim that natural play produces that state.
- **What it does not close.** "No import or heap free" covers these two bodies only. It does not cover the second bookkeeping call (`00310780`+0x7E), the restore (`00310780`+0x86), the later calls (`00310780`+0x99, +0xAC, +0xB9 and +0xD6) or the caller flow. It proves nothing about the cache's initialisation, binding, reuse, scheduling or presentation.

Static only (Method A); no game, emulator or native session. Still OPEN: natural KO and whether it reaches this leg, the cache's actual binding and initialisation, outside writers to the count bytes, termination on a corrupted list, scheduling and presentation.
```

The kind-1 sentence is FABLE's own reading at the bytes (check H: the kind-1, flag-1 path writes only `00513110`). It
lies inside the write census SWE2-AUDIT-SPEC re-counted, and it is labelled in this record rather than credited to
ASTRA. This caller sends only kinds 1 and 2 (`00313C5E`/`61`/`63`), as SWE2-AUDIT-SPEC noted, so the kind-3 arm is not
on this leg.

## FABLE clause E2 (the capability policy's UQ-147 box)

It is appended after the box's last line, "timing and scheduling; the helpers' transitive effects. UQ-147 stays
SUPERSEDED.", which closes the 2026-10-03 release sub-bullet. As for E1, the links below are rewritten to
resolve from this record folder (on the page each has one `../` fewer):

```text
      - *What the release's notification does in the native relation cache (FABLE, 2026-10-03, on ASTRA's [`uq147-native-relation-invariant`](../../../_experiments/evidence/uq147-native-relation-invariant/README.md) evidence accepted by SWE2-AUDIT-SPEC; [review](../../../_index/candidates/auditspec-review-astra-uq147-native-relation-invariant-1003/REVIEW.md), [record](../../../_index/candidates/fable-uq147-native-relation-1003/README.md)).* Static only.
        - [The status-write page](../../../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md)
          §2.7a now gives it. On the release's contributor-bookkeeping path above (bit 22 clear), the notify
          ends relation rows in a fixed native pool through a local remover. It is not an opaque callback. On a
          coherent row it removes at most once. A malformed row can be removed twice, and the remover's count
          bytes then underflow. That is a conditional fact about malformed state, not a natural bug.
        - For UQ-147 this removes one opaque effect from the fallen summoner's release and nothing else. It does
          not show that natural summoner KO reaches that leg. It says nothing about the other helpers, the
          caller flow, or the cache's initialisation, reuse, scheduling or presentation.
        - **Still OPEN:** natural summoner KO and its live admission; Esper pending-`0x113` admission; the
          cache's binding and lifetime; timing and scheduling; presentation. UQ-147 as a whole stays open: the
          row stays SUPERSEDED, and its live half `FABLE-REQ-ASTRA-UQ147-KO-SUMMONER-DURING-A-SUMMON` is OPEN.
```

## FABLE check and dry run

- `check.py`: 119 PASS lines, FAILS 0 (`check.out`).
  - Groups N (the notify leg), P (the packet, as context), W (the route), H (the handler), L (the remover), Q (the
    reducer, with polarities read from the image) and X (the clause text) cover every site and fact the clauses
    state. K checks this README: its links, its headings and the consumer-check form.
  - The evidence manifest hashes to the value SWE2-AUDIT-SPEC recorded (`e1db8d80…`), and so do its members.
  - There are twelve controls, eight on the image and four on the text. Each must first pass on the clean baseline
    and then FAIL on its defect. The image controls patch a private copy in memory, and the exe on disk is never
    written (its sha256 is read again at the end).
- `apply.py`: a dry run. `apply_dryrun.out` shows E1 WOULD PATCH (+10 lines), E2 WOULD PATCH (+12 lines), FAILS 0.
  - Both edits are insertions on unique full-line anchors. Nothing is struck, and line endings are kept.
  - A page equal to HEAD plus the clause reports ALREADY.
  - Any other content difference from HEAD is REFUSED.

## FABLE notes for owners, not applied

- **OPUS, the commit contract §13a, "What `EXP-091` discloses about itself".** It still calls `0x512F30` "the deep
  render/event sink". The handler and its remover are now a bounded local cache operation. The stub-limit wording is
  OPUS's to revise, and so is EXP-091's own "SINK (deep render/event sink)" line. Two parts are unchanged: EXP-091's
  dispatch hits still prove no native effect, and its 85 cases are not re-run.
- **OPUS, the all-ones page §9, "What the pooled record is".** The page gives `+0x4` as "the key the applier matches
  an event against" and the owner's `+0xE` as "a live count". On ASTRA's accepted reading:
  - row `+0`/`+4`/`+8` are recipient, actor and target;
  - the remover decrements the owner's `+0xE` and the global byte `02EBA481` without a test, so a second removal
    takes a zero count to `0xFF`;
  - a removed row keeps its identity words and links.

  That is cache representation, which ASTRA's README gives to OPUS. Renaming a field is OPUS's call, not FABLE's.
- **The relation-reset packet.** ASTRA's separate `uq147-relation-reset-effects` (`e06561376`, SPEC ACCEPT in
  `220da2129`) bears on the status-write §2.7 row `002ED180` ("the render side's defeat call, unread"). It is a
  separate request and is not consumed here.

## Consumer check (FABLE)

affected: Database/FFXII TZA/10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md
affected: Database/FFXII TZA/15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md

- consumer: the status-write page §2.7a, FABLE's release clause of 2026-10-03 ("The helpers ... are not read here and
  are not assumed to be free of effects."): revised-here. A qualifier for the first helper's native relation effect
  is appended. Nothing is struck, and the sentence still holds for every other helper.
- consumer: the status-write page §2.7, the row `002ED180` ("the render side's defeat call, unread"): agrees. That
  row is the reset path, which is not part of this packet.
- consumer: the capability policy's UQ-147 box: revised-here. One sub-bullet is appended, and the box stays
  SUPERSEDED.
- consumer: the box's same-call, mode-query and release sub-bullets (FABLE, `e5c38a7d6` and `d107fd273`): agrees.
  They are cited and not repeated.
- consumer: the commit contract §13a, the notify bullet (OPUS): agrees. It is cited for the zero argument, the
  target-mask gate and the record layout, and not re-proved.
- consumer: the commit contract §13a, "What `EXP-091` discloses about itself", on `0x512F30` as "the deep
  render/event sink": routed-to-OPUS. The stub-limit wording is OPUS's.
- consumer: EXP-091, the `002ED2A0` bullet and the stubbed-entries line: routed-to-OPUS, with the contract line
  above. The route it gives (`+0x650`, the stub) agrees with check W.
- consumer: the all-ones page §9, the pooled-record table and the owner's count: routed-to-OPUS. This is cache
  representation, and the unguarded decrement and the stale bytes are not stated there.
- consumer: the group-completion page, EE-7 (FABLE), on the handler's kind-3 arm: agrees. Kind 3 is not sent on
  this leg.
- consumer: the battle-unit field map's `003E6B40` thunk row: agrees. Its `00512F30` forwarder is the route that
  check W reads.
- consumer: the type-flow census, `embeddedBlock0650` (SWE2-DATA): agrees. It is prior physical-access credit, and
  nothing is renamed.
- consumer: EXP-198, the `00310780` notes ("`00313B30(obj,row2)` + `002FEAD0(row2)` (scripted boundaries)"):
  agrees. The boundaries stay scripted there.
- consumer: the party pages and the combo page: agrees. None of them states the notification or the cache, so there
  is nothing to revise.
- consumer: the register row UQ-147: agrees, unchanged (SUPERSEDED, with its live half OPEN).

run: check.py at d7a9175bb (FAILS 0)
