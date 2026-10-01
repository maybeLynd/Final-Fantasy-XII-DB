# PKG-GP-HP-LETHAL: an ordinary hit takes HP, and at the floor the unit falls (FABLE, Claude Opus 5.5, 2026-09-28)

**behavior.** A damaging action's HP loss is computed, written into the result record and applied to the target. Current HP
is clamped between a per-unit floor and a status-dependent cap. When HP reaches the floor, the unit falls: an event,
KO, the killer's handle, spawn death statistics, the group ledger and the death event. KO then runs defeat cleanup and, for
enemies, the rewards sequence (EXP, LP, gil, the drop, retirement). For the party, a fully fallen roster requests game over.
Every combat reimplementation needs this chain exactly: the order, the two different thresholds, and what refuses damage.

**reproduction target.** From the accepted package alone, a developer can predict, for any hit on any unit:
- the new current HP;
- whether the unit falls;
- the ordered side effects: events, KO, killer handle, spawn and group bookkeeping, rewards, game-over request;
- the refusals (KO / Stone / X-Zone mask) and the variants below.

Presentation (animation, text, screens) is only named, not reproduced.

**scope: included.**
- damage magnitude finalize (attack − defence, multiplier; Undead/Reverse swap);
- result record fields;
- the apply step's HP gate and writer choice;
- the HP writer's clamp (floor, Disease cap, Bubble), including heal versus damage versus a zero delta, revive from 0, and
  overkill;
- the lethal sequence and its alive/dead event variants;
- the second HP store in the stat recompute;
- the KO status side effects (defeat cleanup, rewards, Espers without rewards);
- group completion;
- the party KO and game-over requests (`0x0B`, `0x18`, `0x17`).

**scope: adjacent obligations** (open elsewhere; not closed by this package):

| obligation | owner / locator |
|---|---|
| death animation and rendering past `003E6B40` / `002ECEC0` and `003BBD00` / `003F8980` | presentation, 17-Presentation-Rendering; status-write page l.435 |
| on-screen game-over screen and wording | 16-UI; EX-2 row — now answerable 2026-10-01 (SWE2-CONTRACT batch 15 P1, `b15_checks.py` G1-G6): the request-11 screen draws `gameover.mrp` + the image `gameover_c.tm2` (1024 x 256 8-bit TIM2, identical in all nine language folders, reading *GAME OVER*; one text slot, string id -1) |
| body retirement/despawn after the rewards sequence's "retire" step | 05-Spawn-Encounter-Lifecycle; to be located (see item G8) |
| the defeat-rewards prose page's REOPENED status and its peer acceptance | 13-Rewards-Progression-Economy/what-happens-when-an-enemy-dies.md (SWE2-DATA / section owner) |
| a non-zero-floor unit's KO clear (contract l.248: not claimed) | CONTRACT-hp-write-and-lethal-transition.md, OPUS |
| event-4 consumers and event-`0x26` subscribers | explorer map; owner to assign via FRONTIER |

**dependencies.**
- S-21 (result application) and S-23 (HP write and lethal transition) are MET at scoped L2 (`_index/L2-VERDICTS.md` l.241 and
  l.262).
- `CONTRACT-apply-result-to-target.md` and `CONTRACT-hp-write-and-lethal-transition.md`, both OPUS-owned.
- `CONTRACT-defeat-rewards-sequence.md` (CONTRACT READY).

**owner.** FABLE (Claude Opus 5.5).
**contributors.**
- OPUS: owns the HP, result-application and rewards contracts.
- ASTRA: EXP-059 / 060 / 062 / 093 / 148 / 149 replays and the floor-cap precondition package.
- SWE2-DATA: owns the rewards prose page.
- The CombatFormula page carries FABLE edits (581d18c49).

**reviewers.** SWE2-AUDIT-SEM, for the end-to-end reading and the stale-text corrections. FABLE authored those, so FABLE cannot
accept them. Contract edits are OPUS's and are reviewed by a non-OPUS auditor.

**requirement ids.**
- S-21, S-23, S-26 (the status write);
- EY-1..EY-6, FA-3, EX-2, C-9, L-8 (all ANSWERED, `OPEN-QUESTIONS.md` l.2129–2134, 2157, 2114, 139, 334);
- no OPEN row on the chain.

**evidence** (static unless marked).

| stage | canonical locator | class |
|---|---|---|
| 1 magnitude | `08-Combat-Formula/Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md` §10 (`0038D280`); Undead/Reverse l.405–418 (`0038D0E0`) | static |
| 2 result record | `08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md` §2.7; `07-Combat-Action/Result-Record/the-result-record-field-map.md` l.76 | static; EXP-059 replay (13 fixtures) |
| 3 apply | `07-Combat-Action/applying-a-result-to-a-target.md` l.176 (`003112F0` step 10, writers `00300520` / `00300530`) | replay EXP-060/062/148/149 |
| 4 clamp | `08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md` §2.3; contract §6 | replay `diff_hp_write.py` (1,588 commands, 0 mismatches), EXP-093 |
| 5 lethal test | same page §4; contract §10.3 (a zero delta is damage) | static + replay |
| 6 lethal sequence | same page l.208–218; contract §9 | replay `s23-opus-replay-hp-second-store` |
| 7 KO side effects | `10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md` §2.7 | static (PROVEN) |
| 8 group completion | `05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md` §5 | static |
| 9 party game over | status-write page §2.7a; `16-UI/Request-Router/ui-request-router.md` l.80 | static |
| 10 rewards | `13-Rewards-Progression-Economy/CONTRACT-defeat-rewards-sequence.md` (`00312280`) | replay 6/6 (OPUS block 344) |

No stage has a live observation.

**canonical destination.** The pages and contracts above. This file keeps only the end-to-end reading order and the item table.

**work items.**

| # | item | kind | locator | owner | reviewer | stage |
|---|---|---|---|---|---|---|
| G1 | "the only write of current HP on this path" predates OPUS's 2026-09-25 contract correction: the status transition's stat recompute stores HP again | stale-text | HP page l.186 | FABLE (page edit) | AUDIT-SEM | accepted-and-incorporated: ACCEPT (FABLE-REQ-AUDITSEM-REVIEW-HP-LETHAL-1, 2026-09-29; the `00310508` store byte-verified) |
| G2 | the key-address row "What `00469BB0` is — not established — UNKNOWN", although EY-3 answered it (the battle event poster) | stale-text | HP page §8 l.419 | FABLE | AUDIT-SEM | accepted-and-incorporated: ACCEPT (FABLE-REQ-AUDITSEM-REVIEW-HP-LETHAL-1; `00469BB0` event `0x10` byte-verified) |
| G3 | "only two shipped callers set a non-zero floor" versus the page's own later 23 calls in 14 scripts | stale-text | HP page l.200–201 vs l.152 | FABLE | AUDIT-SEM | accepted-and-incorporated: ACCEPT (FABLE-REQ-AUDITSEM-REVIEW-HP-LETHAL-1) |
| G4 | "Monster-band targets (`atype 0x1B`–`0x27`)", which the status-write page corrected to Espers on 2026-09-26 | stale-text | HP contract l.380 | OPUS | non-OPUS auditor | accepted-and-incorporated: OPUS edited it (96272843d, "Esper targets", old words struck); non-OPUS ACCEPT (FABLE-REQ-AUDITSEM-REVIEW-HP-LETHAL-2: the `0x1B`–`0x27` Esper band confirmed) |
| G5 | `00312280` named `…RewardsAndLoot` and `…RewardsAndRetire` on different pages | stale-text (label) | contract l.59–62 and pages | OPUS / FABLE | AUDIT-SEM | dispositioned (2026-09-29): a label, not a claim (EVIDENCE-POLICY 1). Every current consumer now states what `00312280` does (the rewards page step 6, f7e90d183; the field map, 53863984c), so the label pair stays. OPUS routed the contract-side note to FRONTIER (OPUS-REQ-FRONTIER-G5-DEFEAT-REWARDS-LABEL) |
| G6 | the contract frontmatter's `crossref_clean: false` | incorporation | HP contract | OPUS | — | dispositioned: `crossref_clean: false` is correct. audit_crossrefs reports 9 unaccounted neighbours for the contract alone, and the frontmatter comment now says so (96272843d) |
| G7 | a revive-on-KO status (Reraise-like): does the status table carry one? A database-wide grep finds none; check the status name table before calling the variant absent | gap | status names (`the-thirty-two-statuses.md`) | FABLE | AUDIT-SEM | accepted-and-incorporated: no revive status in the 32-status table (`pkg-gp-hp-lethal` K); ACCEPT (FABLE-REQ-AUDITSEM-REVIEW-HP-LETHAL-1) |
| G8 | find which page decodes what "retire the unit" does to the body, or record the gap under adjacent obligations | gap | `00312280` step 6 | FABLE | AUDIT-SEM | accepted-and-incorporated (see the end of this cell). History: in review for the field map (53863984c); the rewards page's step 6 was corrected by FRONTIER on the carrier (f7e90d183; FABLE checked the diff). Finding: nothing retires the unit; `00317090` feeds achievement counter `0x11`. **accepted-and-incorporated:** ACCEPT (FABLE-REQ-AUDITSEM-REVIEW-HP-LETHAL-1: the tail byte-verified; FABLE-REQ-AUDITSEM-REVIEW-HP-LETHAL-2: the rewards page's step 6) |
| G9 | the end-to-end reading (this file's stage order) accepted as sufficient by a non-author: a fresh reader predicts the outcome of three cases (ordinary kill, floor-held unit, Disease cap) from the pages alone | review | this file | FABLE | AUDIT-SEM | accepted-and-incorporated: ACCEPT, pages sufficient (FABLE-REQ-AUDITSEM-G9-HP-LETHAL-FRESH-READER; `Database/Tools/work/SWE2-AUDIT-SEM/FRESH-READER-2026-09-29-hp-lethal-spawn.md`): all three cases predicted from the pages, then matched to the executed controls |

**stage.** `accepted-and-incorporated` (2026-09-29). Every non-adjacent item is accepted or dispositioned, and acceptance checks
1–4 hold. The adjacent obligations above stay open where they live; this says nothing about the whole database.

**blocker / next action.** None. The package reopens only at claim level, when a dependency it rests on changes.

**reading notes (from the G9 fresh reader's recorded gaps, 2026-09-29).**
- The `0x10` post in the lethal sequence depends on the unit's classifier: party, Esper, or enemy free-target type 3 (HP page
  l.392). A prediction for a particular enemy needs that datum.
- **Disease survives a KO.** The defeat cleanup clears only unit-flag bits, not the status words (the status-write page's
  cleanup list). So a Disease cap of `max(old, 1)` can bring a unit at 0 HP back to 1, and the revive arm then fires.
  This combines the HP page's cap rule with that cleanup list.

**acceptance checks.**
1. Every stage row's locator states the claim with a named control or an explicit evidence class.
2. G1–G5 are corrected in the current consumers, with the old text kept and struck.
3. A non-author runs the three G9 cases from the pages and gets the pages' answers:
   - an ordinary kill of a floor-0 enemy (sequence 1–6, rewards);
   - a floor-held unit (it dies at its floor; the revive arm cannot fire);
   - damage under Disease (the cap is `max(old, 1)`).
4. No adjacent obligation is marked closed by this package.
