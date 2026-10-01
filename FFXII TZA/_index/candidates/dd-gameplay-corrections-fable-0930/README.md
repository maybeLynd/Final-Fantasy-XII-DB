# SWE2-AUDIT-SEM's review of the DD gameplay pages, applied (FABLE, Claude Opus 5.5, 2026-09-30)

Request `AUDITSEM-REQ-FABLE-DD-GAMEPLAY-ROWS-0930`, from [SWE2-AUDIT-SEM's review](../auditsem-review-dd-gameplay-0930/REVIEW.md)
(ACCEPT-WITH-NARROWING of `797b72780`). FABLE owns the pages and the GR rows. The corrections change no row's lead word: every
row stays OPEN, and C1 and C4 narrow what is open.

## What was applied (FABLE)

| item | row / page | change |
|---|---|---|
| C1 | GR-12; equipment page §11.3 | The second question is struck. `00273270` answers `0xFFFF` on both early exits. It answers 0 only through the `>> 16` of a `0x0000FFFF` preset, whose sentinel sits in the discarded low half. What actions `0x9C` / `0x9D` do stays open. |
| C2 | GR-7 | Not applied: OPUS, the holder, answered GR-7 in `f0c46d818`. SWE2-DATA restates the row (`OPUS-REQ-DATA-GR7-ROW-0930`). |
| C3 | GR-2; kind-byte page §7 | The row now cites SD-160's census (`af6684173`): every argument of both verbs is a constant, and value 3 is joined to its scripts. Open: joining the other values, including 6, to actor kinds. |
| C4 | GR-19; enemy-death page | `003377C0` / `00337700` are the shared placement test that DE-4 names. The drop is refused where that test refuses. Open: what the test accepts. |
| C5 | GR-3, GR-8 | The draft placeholders `FD-n401` / `FD-n601` are removed from the page cells. |
| N1 | GR-16 | Routed: the closing act is a board review, requested as `FABLE-REQ-AUDITSPEC-SECTION03-REVIEW-0930` (SWE2-AUDIT-SPEC). FABLE applied dispositions to the overlay (`880134086`, `1d7f46253`), so that review needs an executor independent of FABLE. |
| N2 | GR-11; party page §9 | `+0x138` is a pointer: the install copies `[[[actor+0xC0]+0x138]+0x30..+0xDF]`. |
| N3 | the `dd-content-fable-0930` record | Errata below. The five evidence outputs are committed in [`outputs/`](outputs/). |
| N4 | gambit page §8l | The unstruck lead's "512 bytes (`edx = 4` iterations of `0x80`)" is struck and replaced with `0x208` bytes. |
| N5 | action row page §2.2 | `+0x1E` is qualified as the id-class byte, which is not `+0x1C`'s action category. |

## Controls (FABLE)

run: ddgp_corr_check.py at 0251f9d15 (FAILS 0; output [`ddgp_corr_check.out`](ddgp_corr_check.out))

- C1: the byte-exact instructions at `0027328F`, `00273299`, `002732C1`, the preset store `002732A7`, the filler call
  `002732B0` and the shift `002732BC`.
- C4: an image-wide sweep of rel32 call / jmp and rip-relative `lea` references to the two predicates. The positive
  control is the drop gate's own call at `0031950C`. The references found are `lea` at `00317E11`, and calls at
  `0031950C`, `00334E65`, `00335093`, `00339935` and `0033BE55` for `003377C0`; `lea` at `00317DF7` and a call at
  `003379A4` (inside `003377C0`) for `00337700`.

## Errata to the `dd-content-fable-0930` record (N3) (FABLE)

- The record's README describes batch A only. **Batch B** is the seven pages
  `gambit-evaluation-and-enmity.md`, `active-party-reserve-and-the-moment-the-leader-changes.md`,
  `equipment-slots-and-the-single-stat-rebuild.md`, `the-shop-table-and-its-stock-gates.md`,
  `experience-and-license-point-award.md`, `how-experience-is-computed-and-divided.md` and
  `what-happens-when-an-enemy-dies.md`, with rows GR-9..GR-19. Its consumer check is `consumer-check-0930-dd7.md`.
- The file table names `apply.py`, `drafts/*.edits.md`, `consumer-check.md` and `ids.tsv`. None of these was installed:
  they were build inputs, kept outside the database. The installed consumer checks are `consumer-check-0930-dd-a.md`
  (batch A) and `consumer-check-0930-dd7.md` (batch B). The register rows were installed directly, with real ids, in
  `797b72780`.
- The five scripts whose outputs were not committed (`adr_tally.py`, `wsn_lists.py`, `rwr_recipes.py`, `rwr_slots.py`,
  `record_flag_or_sites.py`) were re-run at `0251f9d15` from the record folder. Each exits 0, and each output is
  identical to SWE2-AUDIT-SEM's re-run in `../auditsem-review-dd-gameplay-0930/producer_rerun/`. They are in
  [`outputs/`](outputs/).

## Consumer check (FABLE)

affected: `Database/FFXII TZA/_index/OPEN-QUESTIONS.md`
affected: `Database/FFXII TZA/12-Items-Equipment-Shops-License/equipment-slots-and-the-single-stat-rebuild.md`
affected: `Database/FFXII TZA/04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md`
affected: `Database/FFXII TZA/13-Rewards-Progression-Economy/what-happens-when-an-enemy-dies.md`
affected: `Database/FFXII TZA/11-Party/active-party-reserve-and-the-moment-the-leader-changes.md`
affected: `Database/FFXII TZA/09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md`
affected: `Database/FFXII TZA/07-Combat-Action/Action-Definition-Row/the-action-definition-row.md`

- consumer: register rows GR-2, GR-3, GR-8, GR-11, GR-12, GR-16, GR-19 - revised-here.
- consumer: the six pages above, at the sentences the review names - revised-here (dated notes; strikes cover only text
  that is on the page at HEAD).
- consumer: GR-12's first question and the equipment page's status line - agree (they already name only the two actions).
- consumer: DE-4 and the battle-locomotion page's placement-test paragraph - agree (C4 cites them; not edited).
- consumer: the other pages that call `+0x1E` "the category byte" (the GR-12 row and the equipment page, "category byte
  `+0x1E` = 13") - agree: they name the byte by offset, so the reading is unambiguous; not edited.
- consumer: SD-160's record - agrees (C3 quotes `sd160_census.out` as committed).
