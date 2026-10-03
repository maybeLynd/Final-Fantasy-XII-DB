# OPUS audit: the 29 L1 production contracts against the 52 L2-MET systems

*Draft for `FABLE-REQ-OPUS-AUDIT-L1-CONTRACTS-1003` (independent corpus audit 2026-10-03, section 7).
OPUS, 2026-10-03. Not published and not applied: every page change below is a **proposed edit** for the
page's owner to take or refuse.*

## OPUS headline

| measure | count |
|---|---:|
| production contracts (front-matter `contract:` key, outside `_` folders) | **107** |
| `level: L2` / `level: L1` | **78 / 29** (the audit's figures, reproduced exactly) |
| readiness CONTRACT READY / BEHAVIORALLY UNDERSTOOD / DIFFERENTIAL TESTED / RUNTIME VALIDATED | 59 / 37 / 9 / 2 (also exact) |
| registered systems / verdict rows / MET (read the way `goal_gate.py check_verdicts` reads them) | 52 / 52 / 52 |
| L1 contracts registered on, or credited by, at least one MET system | **29 of 29** |
| **supplemental** (no MET verdict rests on it) | **0** |
| **justified** (load-bearing, L1 sufficient for the system's declared scope) | **23** |
| **promote** (load-bearing, named work missing) | **6** — rows 5, 6, 8, 17, 21, 24 |

**No difference from the audit's 29 needed explaining.** The census reaches 107/78/29 when a contract is
defined as a file whose YAML front matter carries `contract:`. One page body has a `contract:` key further
down (`17-Presentation-Rendering/Gi-Render-Commands/gi-render-command-family.md`, line 655), and it is
correctly not counted.

## OPUS finding: what the `level:` key on a contract actually records

The census prints three cross-tabs, and together they change how the 29 should be read:

- **All 29 L1 contracts have executed evidence**: §13 class ISOLATED for 27 and LIVE for 2, read by
  `check_gate26.runtime_class`. **43 of the 78 L2 contracts have nothing executed.** So `L1` does not
  mean "less evidence".
- **28 of 29 L1 contracts are narrower than `scope: subsystem`** (23 family, 3 operation, 2 transition).
  **73 of 78 L2 contracts are `scope: subsystem`.** In practice the key tracks scope.
- **All 29 L1 files were first added 2026-09-11 to 09-13**, and none has had its level changed since. 49 of
  the 78 L2 contracts were added on or after 2026-09-21. The subsystem contracts that turned these
  systems MET were written **as composition layers over the L1 contracts**, and say so:
  - `CONTRACT-shared-transform-workbench.md`: *"the two [L1 contracts] cover how to borrow the area and
    what the primitives compute. Neither says what the area IS"*.
  - `CONTRACT-character-render-object.md` names `CONTRACT-character-transform-publish.md` as *"the
    operation R-5 and R-6 describe"*.
  - `CONTRACT-the-moment-an-action-is-committed.md` §13 states that its own runtime evidence is
    `CONTRACT-commit-action.md` §13 and §13a.

The reading this supports is FRONTIER's adequacy ruling at the head of `L2-VERDICTS.md`: *a narrower
contract is adequate exactly when the system's operations have no cross-operation invariant or ordering
it leaves unstated.* So an L1 contract is **load-bearing** whenever a MET system relies on it, and it is
**sufficient** when something else on that system states the cross-operation layer.

## OPUS classification rule

A contract is **load-bearing** to a MET system if that system's verdict rests on it in any of these ways:

- the verdict contract cell credits it, by file name or by subject (for example "update gate (pre-existing)");
- it is the only contract implementing one of the system's `primary_pages` (census link `SOLE`);
- a `scope: subsystem` L2 contract on the same system names it as the per-operation layer (census link `COMP`).

**justified** means all three of these hold:

- **J1:** a composing `scope: subsystem` L2 contract states the system's cross-operation layer, or
  `L2-VERDICTS.md` has ruled that the narrow scope spans the system's whole extent.
- **J2:** the contract has executed §13 evidence and at least one falsification pass. All 29 meet J2:
  each has `audit.passes: 1`, OPUS, and confidence PROVEN.
- **J3:** what is still open in its §14 is naming, intent, live frequency or placement residue. None of
  it changes what a reimplementation must do inside the system's declared scope.

**promote** means J1 or J3 fails. The row then names exactly what is missing.

## OPUS table — all 29

Census links: `REG` registry `contracts` column · `CELL` named in the verdict contract cell · `SOLE` the
only contract implementing a primary page · `COMP` named by a composing `scope: subsystem` L2 on that
system · `IMPL` implements a primary page that other contracts also implement.

| # | contract | cited by (MET) | class | reason |
|---:|---|---|---|---|
| 1 | `00/CONTRACT-per-frame-update-gate.md` | S-02 (REG SOLE COMP; cell: "update gate (pre-existing)") | justified | Composed by two subsystem L2s, `world-simulation-tick` and `system-stop-registry`. Isolated execution. All §14 items closed; the `0x0010` group is UQ-26, signed NO ADMISSIBLE SOURCE. |
| 2 | `00/CONTRACT-transform-primitives.md` | S-05 (REG COMP) | justified | `shared-transform-workbench` (L2 subsystem) is explicitly layered on it. DIFFERENTIAL TESTED: 123 point + 123 compose cases, 0 mismatches. All six §14 items answered. |
| 3 | `00/CONTRACT-transform-workbench-save-restore.md` | S-05 (REG COMP) | justified | Same composing L2. All nine shipped call sites decoded (eight pass `ecx = 1`, one passes `ecx = 2`). Residue: whether an indirect call inside a save window could reach Save, which no edge list can answer; the shipped convention is fully specified. |
| 4 | `02/CONTRACT-authored-table-row-lookup.md` | S-09 (REG SOLE COMP; cell: "row lookup") | justified | Composed by `ard-area-binder` and `resource-section-addressing`. LIVE (EXP-079). Residue: whether the two null guards are reachable in play; both arms are specified, and the static half is settled. |
| 5 | `02/CONTRACT-efx-source-rebase.md` | S-47 (REG IMPL COMP; cell: "EFX source rebase (pre-existing family contract)") | **promote** | J3 fails inside S-47's titled subject, "arena reference lifetime". §14.2: the **global safety schedule** is open. Nothing yet shows that every consumer of a rebased pointer is refreshed before use, or that callbacks or threads cannot observe the intermediate state. §14.4: external-owner replacement, all pin/unpin callers and specialised payloads remain obligations. `resource-input-ownership` (the L2) does not discharge either item; it reads pin/unpin order for its own path only. |
| 6 | `02/CONTRACT-resource-entry-tree.md` | S-47 (REG IMPL COMP; cell: "ordered-tree membership") | **promote** | The contract says of itself, at §14.3, *"this is not a whole-tree or L2 acceptance"*. Missing: execution of `409CA0` (only checked statically), all tag forms, and the complex child callbacks of the release chain above the pair. |
| 7 | `03/CONTRACT-field-record-accessors.md` | S-11 (REG SOLE COMP; cell: "accessors (pre-existing)") | justified | Composed by `authored-trigger-points` and `field-environment-variant`. DIFFERENTIAL TESTED over a planted table. Residue: whether the null-table window is entered in play. §14 calls this "the one that matters for a reconstruction", but §10 now specifies both arms (permissive for `00377700`), so it is a reachability question, not missing behaviour. *Judgement call; see the closing notes.* |
| 8 | `04/CONTRACT-actor-record-pool-and-region-map.md` | S-13 (REG SOLE COMP; cell: "slot-pool via ...") | **promote** | J3 fails on two static items. (a) The pool header is `2 × roundUp16(8 × definitionValueTotal + 8)`: one pointer table plus a **second table of the same size, whose content and readers are open**. (b) **No census of shipped descriptor group counts exists.** EXP-107 shows that more than eight groups are accepted, read past `01E0C328`, and never carved. Sequences 5/6 and the class-0 NULLs are meaning-only residue. |
| 9 | `04/CONTRACT-manager-slot-entry-tables.md` | S-52 (REG CELL SOLE), S-13 (SOLE COMP) | justified | The S-52 cell rules that it "covers the row's whole subject", the same whole-extent principle as S-23. §14 is closed: side A is the camera-shot table and side B the camera-shake table; `lookupIndex > 1` is verified. |
| 10 | `06/CONTRACT-movement-body-pool.md` | S-19 (REG IMPL COMP) | justified | `separation-pass` (L2 subsystem) names it "S-19's other half" and owns the pass geometry and list-order consequences. Exhaustion (NULL from the allocator, silently) is specified. Residue: whether play ever approaches 128 bodies, which is live frequency. |
| 11 | `07/CONTRACT-battle-target-buffer.md` | S-20 (REG COMP), S-14 (IMPL) | justified | `the-moment-an-action-is-committed` cites it for the `+0x778` structure that CM-3/CM-4 touch. DIFFERENTIAL TESTED. All three §14 items struck or corrected (flags bit `0x1` is a live perception-cache gate). |
| 12 | `07/CONTRACT-commit-action.md` | S-20 (REG COMP), S-14 (IMPL) | justified | The composing L2's own runtime evidence is this contract's §13/§13a: 1,309 commands, 704 lines, 0 mismatches, plus EXP-091. Its §14 band question is answered by the handler-table page. |
| 13 | `08/CONTRACT-hp-write-and-lethal-transition.md` | S-23 (REG SOLE) | justified | No composing L2, but `L2-VERDICTS.md` ("S-43, S-09, S-23, S-05 — judged by contract SUBJECT") rules that the transition scope **spans the system's own extent**. §14 closed (the `+0x48` floor writers; status row 28 = Bubble). |
| 14 | `08/CONTRACT-preparation-step-family.md` | S-22 (REG SOLE COMP; cell: "pre-existing, audited") | justified | Composed by `formula-step-table`, `weapon-recipes` and `environmental-element-scaling`. Residue: semantic names for nine members (E-3, the semantic lead's). Also open: whether a shipped recipe list carries an out-of-range slot, which the `weapon-recipes` census (109 pointers) can settle statically; proposed below. |
| 15 | `09/CONTRACT-gambit-walk.md` | S-25 (REG IMPL COMP) | justified | `enmity` (L2 subsystem) carries the enmity half. DIFFERENTIAL TESTED. §14.1 proves the subgroup bound (at most `0x0B`, via the `+0x6B5` direct-command arm). That also states "how a command switches it", the subject of S-25's second page. |
| 16 | `10/CONTRACT-auto-status-rebuild.md` | S-24 (REG SOLE COMP) | justified | Composed by `stat-derivation`. Every call in the apply tail now runs from shipped bytes (§13d). Residue: what gate values `3` and `2` distinguish, which is naming (FABLE's); the values themselves are specified. |
| 17 | `11/CONTRACT-party-slot-assignment.md` | S-28 (REG SOLE COMP; cell: "slot assignment ... (pre-existing, audited)") | **promote** | J3 fails on one of its own `entries:`. For `0025BFB0` (the pending-request consumer), **what its five request bits select and what `0026CE60`/`002628B0` do natively** is open (§14). The party-focus L2 describes only `002628B0`'s slot write. Smaller items: the `+0x0F` values (two writers, no reader) and whether `00263770` writes the roster in a callee. *Judgement call.* |
| 18 | `12/CONTRACT-bazaar-unlock-and-purchase.md` | S-30 (REG SOLE COMP; cell: "both named pages") | justified | Composed by `shop-stock-ladders`. The last §14 item (FZ-3 against the `0030B6A0` mask) was answered statically on 2026-09-26: a valid restored header skips the rebase. The save round trip is not executed, and the row's runtime cell already accounts for that. |
| 19 | `12/CONTRACT-inventory-class-storage.md` | S-29 (REG IMPL COMP) | justified | Composed by `equipment-compatibility`. Residue: "the remaining bytes of the `0x58` descriptor". That is type-store residue, routed to the type audit (`../opus-audit-type-residue-1003/`); the class operations do not read them. |
| 20 | `13/CONTRACT-experience-and-licence-award.md` | S-32 (REG SOLE COMP; cell: "EXP/LP award (pre-existing)") | justified | Composed by four L2s, led by `defeat-rewards-sequence`. Residue: unretained live samples. Also open: placement of a relocation base at or above 4 GB, which is OS policy (the UQ-137 class). The contract says orchestration belongs elsewhere. |
| 21 | `17/CONTRACT-authored-command-ramp-channels.md` | S-48 (REG SOLE; cell credits it by subject) | **promote** | **Relabel only.** It is the system's only contract and declares `scope: subsystem` (repaired at `3981ee43d`). It is DIFFERENTIAL TESTED (483 commands, 0 mismatches) and the verdict credits it. `level: L1` contradicts its own scope and the MET verdict. Nothing substantive is missing: the only open item, how often repeat-dispatch fires, is live frequency. |
| 22 | `17/CONTRACT-character-transform-publish.md` | S-38 (REG IMPL COMP) | justified | `character-render-object` (L2 subsystem) is the object, and it names this contract as the operation R-5/R-6 describe. The §14 premise was corrected: `+0x1C` is a camera-source flag, not a per-frame parity bit. |
| 23 | `17/CONTRACT-coast-down-latch.md` | S-38 (REG IMPL) | justified | As a transition, J3 holds: DIFFERENTIAL TESTED, and §14.1–3 are answered (the `+0x457` fixed point at −76, the `+0x006` owner link, the `+0xCC` event word). The missing composition of S-38's second page is recorded once, on row 24. |
| 24 | `17/CONTRACT-render-record-pool-lifecycle.md` | S-38 (REG IMPL) | **promote** | J1 fails. S-38's second primary page, `the-character-render-record-array.md`, is implemented **only by this contract and row 23 (both L1)**. No subsystem contract composes the record array: the S-38 L2 composes the render **object**, page 1. Missing: (a) a statement of the array's cross-operation layer, covering pool lifecycle, the coast-down latch and the `+0x006` attach link; (b) the outside-family writers of flag word `+0x18` bits `0x1`/`0x4`/`0x10`. Smaller items: `+0x40`/`+0x4C..+0x70`/`+0x64` (type residue) and the caller that supplies allocation names. |
| 25 | `19/CONTRACT-save-container-transform.md` | S-43 (REG IMPL COMP) | justified | Composed by `save-image-pipeline`. EXP-088 ran 46/46 cases and 9/9 mutants, round trip both directions. All three §14 items struck. |
| 26 | `19/CONTRACT-save-image-buffers.md` | S-43 (REG IMPL COMP) | justified | Same composing L2. §14 closed. The backup buffer's purpose (`V-6`) is bounded: the mechanism is closed and only intent is open. |
| 27 | `19/CONTRACT-storage-read-completion.md` | S-43 (REG IMPL COMP) | justified | Same composing L2. DIFFERENTIAL TESTED (100/100 lines, 4 mutants killed). Residue: whether a shipped **caller** mishandles a `0` partial-read result. That is consumer-side and live, and the contract declines to claim it. No OPEN-QUESTIONS row was found for it; proposed below. |
| 28 | `20/CONTRACT-achievement-counters.md` | S-45 (REG IMPL) | justified | The census misses `COMP` here only because the registry row lists this contract alone, and the cell names the L2 by commit (`699c743c8`), not by file. By reading: `steam-integration-subsystem` (L2 subsystem) names it. §14 closed (all eight mode arms decoded; the kind-7 bitmap was found). |
| 29 | `21/CONTRACT-gameplay-generators.md` | S-46 (REG SOLE COMP) | justified | Composed by `which-generator-serves-which-roll`, which owns routing. DIFFERENTIAL TESTED over the algorithm. §14 closed (reseed paths censused; `MTRand_int32`/`MTRand_closed` identified). |

*Category prefixes are shortened: `00/` = `00-Engine-Core-Runtime/` and so on; the census output carries
full paths.*

## OPUS proposed edits (for the owners; none applied)

1. **`_index/important-subsystems.tsv`, S-45:** add `20-Platform-Online-Achievements/CONTRACT-steam-integration-subsystem.md`
   to `contracts`. The verdict cell credits it, and the registry still lists only `CONTRACT-achievement-counters.md`.
2. **`17/CONTRACT-authored-command-ramp-channels.md`:** change `level: L1` to `level: L2` (row 21), after
   review by someone other than the author. OPUS ran its only falsification pass.
3. **`10/CONTRACT-auto-status-rebuild.md`:** consider adding `08-Combat-Formula/the-auto-status-rebuild.md`
   to `implements:`. That S-24 primary page has no implementing contract, and this contract is its subject.
   The owner decides.
4. **S-25 and S-29 primary pages with no implementer:** `which-gambit-set-fires-and-how-a-command-switches-it.md`
   (by subject, row 15 covers it) and `using-an-item-is-an-action-that-costs-an-item.md`. Route to the
   verdict owner (SWE2-AUDIT-SEM) to confirm which contract covers each page.
5. **`19/CONTRACT-storage-read-completion.md` §14.1:** add or point to an OPEN-QUESTIONS row. The template
   requires every §14 item there, and `grep` found none for the caller-side `0` result.
6. **`08/CONTRACT-preparation-step-family.md` §14:** the out-of-range-slot question can be settled statically
   against `CONTRACT-weapon-recipes.md`'s 109-pointer census.
7. **`_templates/CONTRACT.md`, `level:` line:** document what the key means on a contract. On the evidence
   above it records scope (narrower than subsystem gives L1), not a measured maturity. Without that note,
   "29 L1" reads as 29 weak contracts.

## OPUS: how to re-run

```
python -B "Database/FFXII TZA/_index/candidates/opus-audit-l1-contracts-1003/l1_contract_census.py" > l1_contract_census.out
```

The script is read-only and needs `git` on PATH for the first-added dates; it takes about 50 s. It reads:

- every `*.md` front matter outside the `_` folders;
- `_index/important-subsystems.tsv`;
- `_index/L2-VERDICTS.md`, with the same width rule as `goal_gate.check_verdicts`;
- `Tools/analysis-kit/gfz-scripts/check_gate26.py`, imported for `sections`/`runtime_class` and not copied.

`l1_contract_census.out` is the run behind this README, made against `HEAD c7319b1b8` plus the shared
worktree as it stood on 2026-10-03.

## OPUS: what this does not do, and the judgement calls

- The **classification column is a reading**, not script output. The script prints the mechanical links;
  each row's class comes from the verdict cell, the composing L2's text and the contract's own §14. The
  closest calls are rows **7, 8, 17 and 24**.
  - Row 7 could be promote, if reachability of the permissive null-table window counts as in-scope.
  - Rows 8 and 17 could be justified, if the second header table and `0025BFB0`'s request bits count as
    meaning-only.
  - Row 24 rests on reading S-38's MET cell as covering page 1 only.
- **`COMP` is name-based.** It shows that a subsystem L2 names the L1 file, not that it composes it. I
  read the composing sentence for rows 2, 3, 11, 12, 15, 22, 25–28. For the rest, the L2's sibling table
  or prose was spot-read, not read whole.
- **No verdict is changed.** Row 24's finding, that S-38's second page has no subsystem statement, belongs
  to the verdict owner. It is not a re-score.
