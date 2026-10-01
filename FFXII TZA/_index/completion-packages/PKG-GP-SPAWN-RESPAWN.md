# PKG-GP-SPAWN-RESPAWN: enemies die, a group is wiped, and the enemies come back (FABLE, Claude Opus 5.5, 2026-09-29)

**behavior.** An enemy's death is counted in its spawn keep entry. The group ledger decides when every member of a group is
dead, locks the party and posts the group's completion. The dead body is torn down and its unit record is reused. The entry
comes back through the automatic spawn selector once its death limit allows and its cooldown has elapsed, or when the party
leaves and returns within the keep window. Every field of the game runs on this loop, and a reimplementation that respawns
too early or too late, or restores the wrong state on return, is visibly wrong.

**reproduction target.** From the accepted package alone, a developer can predict, for a spawn entry and a sequence of kills,
area exits and returns:
- when its group completes, and what that locks and posts;
- when the entry becomes eligible again, from the native gate (elapsed ≥ cooldown, not died out) and from the scripts'
  own checks (elapsed > cooldown);
- what state a return within the keep window restores.

**scope: included.**
- the death count and stamp;
- the death limit and cooldown (authored base plus a random range);
- the group ledger and the completion test, with its posting modes;
- the body teardown after the death reaction;
- unit-record reuse;
- the three re-entry gates: the native selector, the script check and the keep-window bank rotation;
- re-placement (point and area; the continuous-entry copy);
- the two distance-retirement modes, and the fact that retirement does not complete a group.

**scope: adjacent obligations.**

| obligation | owner / locator |
|---|---|
| a live capture of a completion, a despawn, a respawn, and a bank rotation with a non-zero bank | ASTRA (runtime); none queued |
| the death animation and corpse fade | presentation, 17-Presentation-Rendering |
| rare monsters (the console's "100% Spawn Rare Monster") | UQ-18, OPEN |
| story-flag spawn suppression, and weather-dependent spawning (asserted on the weather page with no mechanism) | 14-Story, 03-World-Area-Field |
| `btlAtelGetRespawnCause`'s native meaning | 05; not found |
| which per-action authored tracks carry the body-release entries (opcode 26 with `+4` = 1, opcode 37) | data census; FABLE, not queued (P7 residue) |
| whether anything other than the timeline handler's posts sets bit 34 (no image-wide writer census; the package claims these posts set it, not that nothing else does) | static census; FABLE, not queued (P7 residue) |

**dependencies.**
- S-16 (placement) and S-17 (group completion) are MET at scoped L2 (`_index/L2-VERDICTS.md` l.245, l.250). The S-17 replay
  ran the completion's callees for real.
- `PKG-GP-HP-LETHAL` supplies the death (lethal step 4, spawn statistics).

**owner.** FABLE (Claude Opus 5.5). **contributors:**
- OPUS: the S-16 and S-17 replays;
- SWE2-DATA: the keep-entry field map.

**reviewers.** SWE2-AUDIT-SEM.

**requirement ids.**
- S-16, S-17;
- EE-1..EE-12, L-1..L-11 and EI-1: ANSWERED;
- L-12 and L-13: SUPERSEDED;
- UQ-18: OPEN (adjacent).

**evidence** (static unless marked; the stage map is from an explorer pass, and each correction below was re-checked from the
image):

| stage | canonical locator | class |
|---|---|---|
| death counted | the group page §3; the keep-entry field map l.88–91 | static; S-23 replay |
| group ledger and completion | the group contract §3–§7, §10–§12; the group page §4–§5b | EXP-011/014, the s17 replay, EXP-019 live pre-kill |
| teardown | `the-world-tick-and-the-field-frame.md` l.294–308 (bit 33 → `BattleUnit_TeardownAndDespawn`) | static; EXP-161 |
| reuse | the unit-definition page (`00236A60`) | static |
| re-entry | `spawn-placement-and-retirement.md` l.283–329 (the native gate); the contract §8 (the script check); `why-the-enemies-you-killed-come-back.md` l.36–81 (the 300 s bank rotation) | static |
| re-placement | the placement page §2; the field map §2.4–2.5 | the s16 replay |

**canonical destination.** The pages above. This file keeps the reading order and the item table.

**work items.**

| # | item | kind | locator | owner | reviewer | stage |
|---|---|---|---|---|---|---|
| P1 | "no native code reads the death count, the death stamp or the cooldown": false. The selector `00235720` reads all four fields directly | stale-text | the contract l.95–103 | FABLE | AUDIT-SEM | accepted-and-incorporated: ACCEPT (FABLE-REQ-AUDITSEM-REVIEW-SPAWN-RESPAWN-1, 2026-09-29; `Database/Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-29-eleven-request-wave.md`): `00235720`'s four reads and the `>=` re-admit byte-verified |
| P2 | "the callee bodies are stubbed … unproved": superseded by the s17 replay | stale-text | the contract §13 | FABLE | AUDIT-SEM | accepted-and-incorporated: ACCEPT (FABLE-REQ-AUDITSEM-REVIEW-SPAWN-RESPAWN-1, 2026-09-29; `Database/Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-29-eleven-request-wave.md`): the reviewer checked the contract's struck text is the old text, with dated corrections |
| P3 | "any runtime observation: none exists": EXP-019 exists (pre-kill) | stale-text | the contract §14 table | FABLE | AUDIT-SEM | accepted-and-incorporated: ACCEPT (FABLE-REQ-AUDITSEM-REVIEW-SPAWN-RESPAWN-1, 2026-09-29; `Database/Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-29-eleven-request-wave.md`): the reviewer checked the contract's struck text is the old text, with dated corrections |
| P4 | "`+0x10` is still not seen written … `EE-1` stands": the initialiser `002395A0` writes it | stale-text | the group page §3 | FABLE | AUDIT-SEM | accepted-and-incorporated: ACCEPT (FABLE-REQ-AUDITSEM-REVIEW-SPAWN-RESPAWN-1, 2026-09-29; `Database/Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-29-eleven-request-wave.md`): `002395A0`'s writes byte-verified |
| P5 | "`EE-12`, a live question": answered | stale-text | the group page §5b | FABLE | AUDIT-SEM | accepted-and-incorporated: ACCEPT (FABLE-REQ-AUDITSEM-SPAWN-P5-P6-P7B, 2026-09-29; `Database/Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-29-spawn-p5-p6-p7b.md`) - earlier stage text kept: review: not named in the SPAWN-1 verdict; asked as FABLE-REQ-AUDITSEM-SPAWN-P5-P6-P7B |
| P6 | the slot-pool page's `00236A60` "not read" gets a pointer to the page that read it | stale-text | `battleunit-slot-pool-and-actor-class.md` | FABLE | — | accepted-and-incorporated: ACCEPT (FABLE-REQ-AUDITSEM-SPAWN-P5-P6-P7B, 2026-09-29; `Database/Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-29-spawn-p5-p6-p7b.md`) - earlier stage text kept: review: not named in the SPAWN-1 verdict; asked as FABLE-REQ-AUDITSEM-SPAWN-P5-P6-P7B |
| P7 | the teardown `00300E40` and the step "death reaction ends → bit 33 → teardown" are never stated end to end | gap | the world-tick page / 05 | FABLE | AUDIT-SEM | accepted-and-incorporated: the gate and setters ACCEPTED (SPAWN-1); the poster census ACCEPTED (FABLE-REQ-AUDITSEM-SPAWN-P5-P6-P7B, `REVIEW-2026-09-29-spawn-p5-p6-p7b.md`). The data residue named at the end of this cell (which authored tracks carry the posts; other bit-34 writers) stays an explicit adjacent obligation, listed under scope - earlier stage text kept: evidence-ready: the group page §5c; teardown.py G K. Death sets bit 33, a timeline event (kind 6, or 4) sets bit 34, and the idle frame tears down when the presentation handle's state is below 3. Narrowed 2026-09-29: kind 6 is posted by the authored-event coordinator `003B8670` (so named on the ownerless-functions page) at `003B89D7` when a walked record's `+4` equals 1. The same switch posts kind 3 for 0, 7 for 2 and 8 for 3. `002FC010` posts kinds 0 and 1. Closed 2026-09-29 (teardown.py P T U): the walked records are the per-action authored tracks (BQ-12, the ownerless page §12); kind 4 is opcode 37; every post into the handler is listed (six sites, two functions); the bit goes to the acting unit. Still open, as data: which tracks carry opcode 26 with `+4` = 1 or opcode 37; and no image-wide census of other bit-34 writers **Review:** the gate and the kind-6/4 setters were ACCEPTED (SPAWN-1). The 2026-09-29 poster census (6fdf6d290, teardown.py P T U) was published after the request, and is asked as FABLE-REQ-AUDITSEM-SPAWN-P5-P6-P7B |
| P8 | who calls `00234200` (the slot release that sets keep bit 2) | gap | the field map l.118 | FABLE | AUDIT-SEM | accepted-and-incorporated (see the end of this cell). Finding: one caller, inside `ActorSystem_ReleaseManagerRecords` (teardown.py R); the slot is freed when the actor records are released, not at death **accepted-and-incorporated: ACCEPT (FABLE-REQ-AUDITSEM-REVIEW-SPAWN-RESPAWN-1, 2026-09-29; `Database/Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-29-eleven-request-wave.md`):** the reviewer's own rel32 census agrees |
| P9 | fresh-reader sufficiency: a kill sequence, a cooldown boundary (t+9 / t+10 with a 10 s cooldown) and an A→B→A return | review | this file | FABLE | AUDIT-SEM | accepted-and-incorporated: ACCEPT, pages sufficient (FABLE-REQ-AUDITSEM-P9-SPAWN-FRESH-READER; `FRESH-READER-2026-09-29-hp-lethal-spawn.md`): all three cases predicted from the pages and verified |

**stage.** `accepted-and-incorporated` (2026-09-29). Every item P1–P9 is accepted by AUDIT-SEM and its page change is committed; acceptance checks 1–3 hold. The adjacent obligations (including P7's data residue) stay open where they live; this says nothing about the whole database. ~~`evidence-ready` (2026-09-29; the earliest item stage, P7's addendum). P1–P4, P8 and P9 are accepted-and-incorporated; P5 and P6 are in review. P5, P6 and P7's poster addendum wait on FABLE-REQ-AUDITSEM-SPAWN-P5-P6-P7B.~~

**blocker / next action.** None. The package reopens only at claim level, when a dependency it rests on changes. ~~AUDIT-SEM's short follow-up on P5, P6 and P7B.~~

**reading notes (from the P9 fresh reader's recorded gaps, 2026-09-29).**
- **The re-entry boundary.** The native selector re-admits at elapsed `>=` cooldown. The scripts' own check is a strict
  `>`, so at exactly `t + cooldown` the native gate admits while the script reports false: a one-tick lag. The two halves
  are on the placement page and the contract §8.
- The keep window's length is the authored per-area value at `0208936C`. The 300 s in this file is one area's value, not a
  constant.
- "Kind-1 enemies" are the spawn-backed records, identified by the record kind byte `+5 == 1`.

**acceptance checks.**
1. P1–P6 corrected with the old text kept and struck.
2. A non-author predicts the three P9 cases from the pages.
3. No adjacent obligation is marked closed.
