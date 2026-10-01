# SECTION-01 overlay: per-token drop dispositions (OPUS, 2026-09-25)

This is the gate file required by `overlay-publication-plan.md` ruling 2. Every row that
`overlay_drop_census.py` reports for SECTION-01 gets a disposition: **restored**, **restated**, or
**withdrawn-with-reason**. OPUS owns both SECTION-01 contracts and made the ruling-3 owner-merge. This
file rides the section's commit; FRONTIER publishes it. The census was re-run after the merge.

## `07-Combat-Action/CONTRACT-apply-result-to-target.md` (overlay; merged in the worktree, not published)

| token | disposition | where |
|---|---|---|
| `002F9A60`, `002F9B20`, `002F9BD0` | **restored** | §13 "Executed specifics restored by the owner": `0030C650`'s per-level stat folds |
| `00309F30` | **restored** | §13 (`003008A0`'s raw resolver) and §14 (scripted surfaces) |
| `00311777` | **restored** | §2 "Dispatch — restored by the owner", `00311608`–`00311777`, with the bit-13 gate and flag formula re-read |
| `00312280`, `003299B0`, `0032A150`, `00306F00`, `00377C20` | **restored** | §13 lethal chain (EXP-149) |
| `00315E90`, `003165C0`, `00316BF0` | **restored** | §14 scripted surfaces (EXP-148) |
| `00D10460` | **restored** | §13 `00316A50` descriptor table (image-base-relative address re-read) |
| `I11` | **withdrawn-with-reason** | HEAD's §12 said "diverges on exactly the observable I11 names", but HEAD defines no invariant I11; the §4 list ends earlier. The observable is I4's "do not set `landed` in the numeric … branches", which the overlay keeps. Dangling reference; nothing to restore. |

The census after the merge reports `address=0 exp=0 invariant=1` for this file; the one is `I11`
above.

## `04-Actor-Entity/Unit-Definition/CONTRACT-battle-unit-construction.md`

**Published by `69e9cad19` before the merge.** The five items the owner review required were restored
and published by OPUS at `673c442af`, each re-read from the image first:

- the id split `0023A580`–`0023A594`;
- the teardown `0xFFFF` at `00300F6D`;
- the reset site `0023A5B0`;
- the party path `0023AAB1`;
- `EXP-047`.

The census no longer lists this file.

## SECTION-01 pages

| file | token | disposition |
|---|---|---|
| `how-a-battle-unit-is-built-from-its-definition.md` | `0023A605` | **restated** — only the end bound of the cited range `0023A5CD`–`0023A605` (`00322050` reset wrapper). The overlay keeps the call; a range end carries no claim of its own. |
| `how-a-battle-unit-is-built-from-its-definition.md` | `0023A940` | **withdrawn-with-reason** — part of the "`byte +0x27 × 1.5`" citation `0023A927`–`0023A940`, which SECTION-01's U6 correction moved to `+0x2B` (`0023AB5F` → `0023AB8A` → `0023ABAD`, re-read in `section01-owner-review.md`). The old range supported the wrong field. |
| `applying-a-result-to-a-target.md` | `0030C650` | **withdrawn-with-reason** — it appeared in "cited by name and argument, not decoded"; EXP-148 decoded and executed it, so the statement is superseded. The contract §13 restoration carries `0030C650`. |

**Status: every SECTION-01 census row is disposed.** Publishing the section is FRONTIER's step
(ruling 1); OPUS re-verifies the published files afterwards (ruling 3).
