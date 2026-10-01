# PKG-GP-STATUS-POISON: a damaging timed status from infliction to its end (FABLE, Claude Opus 5.5, 2026-09-29)

**behavior.** An attack or spell inflicts Poison on a target. From then on, the periodic tick takes a sixteenth of the target's
maximum HP each time Poison's beat runs out, until:
- the status's duration expires;
- a cure (Antidote, Poisona, Remedy) removes it;
- the target is KO'd.

Sap and Regen share the same path, with different amounts. Every battle in the game has statuses that tick like this. A
reimplementation with the wrong amount, beat, duration, refresh rule or KO behaviour is visibly wrong within seconds.

**reproduction target.** From the accepted package alone, a developer can predict, for a target with known HP, stats and
statuses:
- whether an infliction lands (the eligibility and immunity gates, and the block mask);
- the duration and beat it stores;
- the HP lost on each Poison beat, including under Bubble and Disease;
- when it expires, and what a cure or a KO does;
- whether a tick can KO the target, and what follows then;
- what re-inflicting Poison on a poisoned target does.

**scope: included.**
- infliction: the result's apply mask, the status write `0030E360` in mode 3, the immunity word, the block mask, and the
  stored duration and beat;
- the periodic tick's gates and its stage 2 for Poison, Sap and Regen: beat, amount, the duration countdown, the remove mask;
- the tick's HP delta through the result applier into the HP write, including the lethal rule;
- the end: expiry through the remove mask, the cure path (the remove-eligible calculator slot, then the applier's removal
  loop), and the KO clear mask;
- the re-infliction (refresh) rule.

**scope: adjacent obligations.**

| obligation | owner / locator |
|---|---|
| a live capture of a Poison infliction, a few ticks, and an expiry or a cure | ASTRA (runtime); none queued |
| the character tint, the rig controller arms and the battle messages ("cured", "wears off") | 17-Presentation-Rendering, 07 post-result events |
| stale text on the status and tick pages that is off Poison's path (explorer items 2, 3, 8, 10, 11 and 12: `+0x1C2`, `+0x28`, the stage-3 writes, the result-record `+0x3C` label, SW-2, SW-3) | the page owners; FABLE files them as a notice, not as package items |
| SW-1 (the fault when the status table is unloaded) and SW-4 | `CONTRACT-status-write.md` §SW, OPUS |

**dependencies.**
- S-26 (the status write, the two-layer model) and S-27 (the periodic tick) are MET at scoped L2 (`_index/L2-VERDICTS.md`
  l.270–271).
- `PKG-GP-HP-LETHAL` supplies the HP write and the lethal transition.

**owner.** FABLE (Claude Opus 5.5).

**contributors:**
- OPUS: the S-26 and S-27 replays (`s26-opus-replay-status-write`, `s27-opus-replay-periodic-builder`,
  `s27-opus-replay-periodic-tick-entry`) and the two contracts' replay records;
- FABLE: the status-write, tick and effect-layer contracts and pages.

**reviewers.** SWE2-AUDIT-SEM (semantic), or SWE2-AUDIT-SPEC for the contract items. The reviewer is named per item when it is
requested.

**requirement ids.**
- S-26 and S-27;
- ANSWERED: C-9, AE-3, EY-1..EY-6, EZ-4, EZ-6, FA-1..FA-4, FE-3 and GA-1;
- SW-1..SW-4, which are contract-local and not in the register.

**evidence** (static unless marked). The locators come from an explorer pass (2026-09-29). **Each correction below is re-checked
from the image or the page before it is made**, so the item stages say `research` until that is done.

| stage | canonical locator | class |
|---|---|---|
| infliction | `07-Combat-Action/applying-a-result-to-a-target.md` step 7; `Status-Write/the-status-write-and-its-side-effects.md` §2.1–2.4a, §2.7; `CONTRACT-status-write.md` invariant 3; the definition flag pair `+0x38`; `the-thirty-two-statuses.md` (block mask `+0x20`, Poison +8 = 50, +9 = 120) | static; replay EXP-086 (67/67), `diff_status_write.py` |
| tick | `Periodic-Tick/what-the-periodic-tick-does.md` l.42–99; the status-write page l.170–185 (stage 2); `CONTRACT-periodic-tick.md` I-1..I-7 | static; replay s27 builder (6/6) and tick entry (4/4), **Regen only** |
| HP effect | applier steps 2 and 10; `the-hp-write-and-the-lethal-transition.md` §2.2–2.5 | static; EXP-093 (64/64), EXP-060, EXP-149 |
| end | the status-write page l.182 (remove mask), l.220–226; applier step 8; the result-record field map l.98 (`0038FC10`); KO clear mask `7FFEF57C` | static |

**canonical destination.** The pages above. This file keeps the reading order and the item table.

**work items.**

| # | item | kind | locator | owner | reviewer | stage |
|---|---|---|---|---|---|---|
| Q1 | Poison's beat: `CONTRACT-periodic-tick.md` §11 says "a beat a third of a second wide", and the tick page l.37–40 says the same. The status-write page gives a per-status beat `+0x13C` reloaded from `row.+9 × frame base × 30`. Settle the units and correct the loser | stale-text (candidate) | the three pages | FABLE | AUDIT-SPEC | evidence-ready (`pkg-gp-status-poison/beat.md`, beat.py S D M): Poison hits every **12 s** (`+9` / 10 s, at either frame rate); the third of a second is the stage-4 drain. The contract §11 and the tick page §1 are corrected |
| Q2 | `+0x17C` is called "the status duration timers" on three pages. The tick page and the contract say it is the eight effect slots, keyed by the effect table | stale-text (candidate) | the applier page l.64, 139, 181; the result-record field map l.175; the stats field map l.167 | FABLE | AUDIT-SEM | accepted-and-incorporated: FRONTIER applied `applier-q2.patch` to the applier carrier (FABLE-REQ-FRONTIER-APPLY-Q2-APPLIER, e222ec17d) after AUDIT-SEM's ACCEPT on the repair - earlier stage text kept: incorporation: ACCEPT after repair (the first review rejected the two `[33]` type rows; re-review FABLE-REQ-AUDITSEM-REREVIEW-POISON-Q2, `REREVIEW-2026-09-29-poison-q2.md`). The repair is published (111feec78); waiting on FRONTIER applying `applier-q2.patch` to the applier carrier page (FABLE-REQ-FRONTIER-APPLY-Q2-APPLIER) - earlier stage text kept: review (AUDIT-SEM claimed FABLE-REQ-AUDITSEM-REVIEW-POISON-PAGES, 2026-09-29); evidence-ready (`pkg-gp-status-poison/timers.md`, timers.py T B): `+0x17C[8]` are the effect layers' slot timers; renamed on the three pages with the old words struck; the field map's "33" timer slots corrected to 32 |
| Q3 | which store holds an inflicted status: the two-layer page says "inflicts → `0030E130` → `+0x68`", and the status-write contract says `0030E360` writes `+0x64` / `+0x3C` and nothing else sets a status bit | stale-text (candidate) | `two-layer-effect-model.md` l.110–111 | FABLE | AUDIT-SEM | accepted-and-incorporated: ACCEPT (FABLE-REQ-AUDITSEM-REVIEW-POISON-PAGES, 2026-09-29; `Database/Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-29-poison-pages.md`) - earlier stage text kept: review (AUDIT-SEM claimed FABLE-REQ-AUDITSEM-REVIEW-POISON-PAGES, 2026-09-29); evidence-ready (`pkg-gp-status-poison/layers.md`, layers.py N C A): not a contradiction but two namespaces; an inflicted Poison never enters `+0x68`; both texts clarified |
| Q4 | internal contradictions on the tick page: "stage 2 does not advance the duration timers" (l.343, 379–380) against "stage 2 is the timer" (l.485–501) | stale-text (candidate) | `what-the-periodic-tick-does.md` | FABLE | AUDIT-SEM | accepted-and-incorporated: ACCEPT (FABLE-REQ-AUDITSEM-REVIEW-POISON-PAGES, 2026-09-29; `Database/Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-29-poison-pages.md`) - earlier stage text kept: review (AUDIT-SEM claimed FABLE-REQ-AUDITSEM-REVIEW-POISON-PAGES, 2026-09-29); evidence-ready (`pkg-gp-status-poison/q4-q5.md`): §4 scoped to stage 3; the unstruck stage-2 claims struck |
| Q5 | `CONTRACT-periodic-tick.md` §13, "no experiment executes any of these five bodies", against the two s27 replays; the S-26 verdict row's stale runtime residue | stale-text (candidate) | the contract l.292–293; `L2-VERDICTS.md` l.270 | FABLE (contract); the verdict row goes to its owner | AUDIT-SPEC | evidence-ready (`pkg-gp-status-poison/q4-q5.md`): the contract §13 now cites the two native replays and names the unexecuted arms; the S-26 verdict-row residue is sent to its owner |
| Q6 | the Poison arm (`00386D9B`–`00386E39`) and the duration-expiry arm have never been executed; the s27 builder replay covered Regen only. A replay with Poison (with and without Bubble and Disease), Sap at HP 1, and an expiring duration | gap | `s27-opus-replay-periodic-builder` | OPUS (replay owner), on FABLE's request | ASTRA | accepted-and-incorporated: ACCEPT, scoped at the original builder boundary (FABLE-REQ-ASTRA-REVIEW-POISON-Q6, 2026-09-29; `_experiments/evidence/poison-q6-independent/README.md`, df93a1eb7): the replay's Poison, Sap, duration and Stop amounts match, and five independent controls support flag A bit 8 selecting the compared HP, not gating the critical check. Not covered by the verdict: the tick entry, live play - earlier stage text kept: evidence-ready: the replay ran (OPUS, ced7c61fd, 14/14): all seven expected values hold, and it corrected the status-write page's HP-Critical row (the check runs on every call; flag A bit 8 only picks the compared value), `pkg-gp-status-poison/q6.md`. The correction is published (f7a5ce0d6); ASTRA's review is requested (FABLE-REQ-ASTRA-REVIEW-POISON-Q6) - earlier stage text kept: research |
| Q7 | can a Poison tick KO? The tick's HP delta goes through the applier's step 10 into the HP write, where the lethal rule applies, and FA-4 / EZ-6 credit rewards for a Poison kill. No page says it outright. State it with the static chain, or find the exemption | gap | the applier, the HP write, the defeat rewards | FABLE | AUDIT-SEM | accepted-and-incorporated: ACCEPT (FABLE-REQ-AUDITSEM-REVIEW-POISON-PAGES, 2026-09-29; `Database/Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-29-poison-pages.md`) - earlier stage text kept: review (AUDIT-SEM claimed FABLE-REQ-AUDITSEM-REVIEW-POISON-PAGES, 2026-09-29); evidence-ready: **yes, it can**. The arm sets flag A `0x140`; the applier's HP step runs on bit 8 with flags `0x40` (only the alive event suppressed); the HP write clamps to the floor and is lethal at the floor; nothing tests for a tick. Stated on the status-write page after the stage-2 table (`pkg-gp-status-poison/poison_ko.py` A S H M) |
| Q8 | the cure: Antidote (recipe 34) and Poisona (recipe 1) → the remove-eligible slot `0038FC10` (body unread) → remove mask `+0x58` → applier step 8. And who else writes the remove mask (the field map names one writer; stage 2 also sets it) | gap | the result-record field map l.98, l.125–129; recipes | FABLE | AUDIT-SEM | accepted-and-incorporated: ACCEPT (FABLE-REQ-AUDITSEM-REVIEW-POISON-PAGES, 2026-09-29; `Database/Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-29-poison-pages.md`) - earlier stage text kept: review (AUDIT-SEM claimed FABLE-REQ-AUDITSEM-REVIEW-POISON-PAGES, 2026-09-29); evidence-ready (`pkg-gp-status-poison/cure.md`, cure.py R B O D W M): Antidote and Poisona carry mask `0x100`; Remedy cures its flag-`0x400` set plus three context-bit sets; the remove slot skips a status held in word 2 and does nothing on a KO'd target unless the cure lifts KO; the periodic builder's stage 2 is a second remove-mask writer, now qualified on the field map |
| Q9 | re-infliction: the contract says re-applying is a no-op, but the applier copies `+0x5C` / `+0xDC` into `+0xBC` / `+0x13C` even when both masks are zero. Does a re-cast reset Poison's duration or beat? | gap | `CONTRACT-status-write.md` l.112–128; the applier l.114–118 | FABLE | AUDIT-SPEC | evidence-ready (`pkg-gp-status-poison/refresh.md`, refresh.py G A I C D M): **Poison does not refresh** (row `+6` bit 5 clear, so it is skipped as no effect); fourteen statuses do, through the applier's copy-through; the contract's invariant 3 and §11 are scoped |
| Q10 | fresh-reader sufficiency, predicting three cases from the pages: a 1,000-max-HP target over three beats; the same target under Bubble; a Poison tick at 40 HP | review | this file | FABLE | AUDIT-SEM | accepted-and-incorporated: ACCEPT, pages sufficient (FABLE-REQ-AUDITSEM-Q10-POISON-FRESH-READER; `FRESH-READER-2026-09-29-poison-q10.md`): all three cases and the re-cast predicted from the pages and confirmed by the controls. One precision note: section 6's "re-applying is a no-op" should point to the refresh rule (status_data `+6` bit 5) - FABLE adds the pointer - earlier stage text kept: research |

**stage.** `evidence-ready` (2026-09-29; the earliest item stage). Q3, Q4, Q7, Q8 and Q10 are accepted-and-incorporated; Q2 and Q6 are accepted-and-incorporated; Q1, Q5 and Q9 are evidence-ready.

**blocker / next action.** The verdict on Q1, Q5 and Q9 (FABLE-REQ-AUDITSEM-REVIEW-POISON-CONTRACTS, rerouted from FABLE-REQ-AUDITSPEC-REVIEW-POISON-CONTRACTS).

**acceptance checks.**
1. Q1–Q5 are corrected with the old text kept and struck, or shown not to be contradictions.
2. Q7–Q9 are answered with a control that fails on the opposite claim.
3. The Q6 replay executes the Poison arm and agrees with the pages' amounts.
4. A non-author predicts the three Q10 cases from the pages.
5. No adjacent obligation is marked closed.
