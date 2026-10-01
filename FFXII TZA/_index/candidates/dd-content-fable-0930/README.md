# DD content pass on eight PARTIAL pages (FABLE, Claude Opus 5.5, 2026-09-30)

This is the content work that OPUS's owner read (`../dd-owner-read-0929/worksheet.tsv`) asked for on eight pages. It
follows the user's rule: "Do not change status merely to reduce DD. Answer/register actual residue, reconcile stale
prose, then re-run the rule."

**No page is re-statused by this pass.** The two REOPENED pages stay REOPENED, and the other six stay PARTIAL. Each
status line now says what really remains. The work, per page:
- the missing sections, written from what the page already establishes and from bodies read in the binary;
- the uncited claims, anchored (or marked not verified);
- the residue, answered where the binary or another page answers it, and otherwise registered;
- the stale prose, reconciled with dated notes. A strike covers only text that was on the HEAD page.

Drafted by FABLE with four helper forks (one page each; one fork took the combo pair). FABLE reviewed every draft and
re-measured it on a patched export.

## Files

| file | what it is |
|---|---|
| `apply.py` | Applies the drafts all-or-nothing. `--check` validates without writing. Every page must equal its HEAD blob (`--allow-eol-only` for CRLF-only checkouts), and every OLD anchor must match exactly once, with no overlaps. `--ids ids.tsv` maps placeholders to register ids that must already exist. |
| `drafts/*.edits.md` | one draft per page: `page:` line + REPLACE blocks (166 in all) |
| `new_rows.tsv` | 8 register-row drafts (placeholder, question, owning page, OPEN status, suggested section). Placeholders are `FD-n<k>`, which the rule's id regex does not match; `FD-1`..`FD-5` are real rows. |
| `consumer-check.md` | the correction record: 21 corrections, each consumer marked agrees / revised-here / routed-to |
| `adr_tally.py`, `wsn_lists.py`, `rwr_recipes.py`, `rwr_slots.py`, `record_flag_or_sites.py` | the evidence scripts the pages cite; each prints or asserts a control first |
| `dd_verdicts.py` | documented_rule's `judge()` on an exported tree, with the live register and tracked set |
| `audit_side.py` | one side of the neighbour differential (audit_crossrefs findings and check_links `--raw` for the eight pages) |

**To publish:**
1. Register the 8 rows of `new_rows.tsv` in `OPEN-QUESTIONS.md`. The owner assigns real ids; the suggested sections are
   hints. This pass does not edit the register.
2. Write `ids.tsv` (`GR-1<TAB><real id>`, …).
3. `python apply.py --root <repo> --check --allow-eol-only --ids ids.tsv`.
4. `python apply.py --root <repo> --allow-eol-only --ids ids.tsv`.

The record folder is `_index/candidates/dd-content-fable-0930/`: the consumer check, `new_rows.tsv`, this README and
the scripts. It is installed with placeholders mapped.

## Verdicts (documented_rule, judge() per page)

- **Before:** the live tree, `documented_rule.py <page>`. The S self-test passes (32 cases).
- **After:** a `git archive` export of HEAD `4407f8484` with the drafts applied (`--keep-placeholders`), through
  `dd_verdicts.py`. The wrapper exists because a plain run inside an export reads an empty git-tracked set.
- **After + registered:** each placeholder is mapped to a synthetic id registered OPEN, as after step 1.

| page | before | after | after + registered | stays open, and why |
|---|---|---|---|---|
| `04-Actor-Entity/the-field-runtime-pass.md` | READY | PARTIAL (1 box) | PARTIAL (live GR-1) | GR-1: is the wait slot's `+0x27` settled byte read anywhere? Status stays REOPENED until a new falsification pass. |
| `04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md` | READY | PARTIAL (1 box) | PARTIAL (live GR-2) | GR-2: what each free-target type value denotes as authored. |
| `05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md` | READY | READY-WITH-POINTER (L-12, L-13 SUPERSEDED, pointers present) | same | No register residue. Status stays REOPENED. `crossref_clean` is false, and L-13's live-only residue is routed for a runtime carrier (below). |
| `07-Combat-Action/how-a-combo-continues-and-what-it-blocks.md` | READY | PARTIAL (1 box) | PARTIAL (live GR-3) | GR-3: what the HUD's per-entry routine draws for a combo-count entry. |
| `07-Combat-Action/Action-Definition-Row/the-action-definition-row.md` | NEEDS-POINTER (UQ-106) | PARTIAL (4 boxes; UQ-106 pointer present) | PARTIAL (4 live) | GR-4 `+0x28`'s reader; GR-5 `+0x0B`'s reader; GR-6 the 436 bit-15-clear `+0x24` words; GR-7 the reader of the kind-10 mask that `+0x3A` feeds. |
| `08-Combat-Formula/combos-and-the-guard-parry-flag.md` | READY | READY (NOTE check N passes) | PARTIAL (live GR-8) | GR-8: the unmapped fields of the per-unit 64-byte record. Converted to NOTE (`note_kind: function`, parent = the combo page), per FABLE's note-class table. |
| `08-Combat-Formula/where-a-stat-number-comes-from.md` | READY | READY | READY | Nothing open. It stays PARTIAL only until the owner read (see below). |
| `08-Combat-Formula/Recipe-System/ranged-weapon-recipes.md` | READY | READY | READY | Nothing open beyond the declared boundary (designer intent, E-4). It stays PARTIAL until the owner read. |

A READY before this pass was the defect OPUS's read found: prose residue with no register id passes the rule. After
the pass, six pages read PARTIAL because their residue is now visible to the rule, and two read READY because their
residue is answered on the page.

## Per page

**the-field-runtime-pass** (22 blocks):
- **§1 and §11.** The "driven repeatedly in one frame" prose is reconciled with §4's correction.
- **§4.** The first-drive line is corrected (slot and payload, not actor). Bit 5 cites FRP-1, already ANSWERED.
- **§6.** It gains upstream / downstream / do-not-confuse text. The "49 callees / 59 sites" figure is recounted with
  capstone and agrees.
- **New §6a.** Key addresses: 30 functions and 9 data addresses.
- **§12 Limits.** The open items are answered: the `table256` writers and `table32` reader, slot 3, and who fills
  `recordPool`.
- **Falsification pass.** Its two "not claimed" items are closed.
- **One row:** GR-1.

**battle-record-kind-byte** (22 blocks):
- **Status line.** Rewritten: AL-1, AL-8, AL-9 and AL-10 are ANSWERED.
- **Stale prose.** The six "meaning open / unanswerable" passages are struck with dated notes; "unanswerable from the
  binary" was wrong.
- **New §5a call chain.** It names two owner transitions: the `0023AD8E` store, and the party-record initialisation in
  the battle-runtime reset. It gives accessor counts from the raw call index.
- **Anchors.** The "eight sites" claim is anchored (15 `or` sites, control 8 of 8). The unnamed 110-byte RNG function
  is `002398F0`.
- **`+0x019`.** Its writer `00321810` is found; it forms the address with `lea` and stores at displacement 0.
- **New crossing paragraph.** It covers the reset's three scheduling and save-rebind edges.
- **One row:** GR-2.
- **Section numbers.** The duplicate §11–§13 numbering is left alone, because `_index/_inbox/repos-78.md` refers to the
  band census as §11.

**spawn-placement-and-retirement** (55 blocks):
- **L-12 / L-13.** The "open" and "review pending" prose in §§11–29 is reconciled with the register: both are
  SUPERSEDED, not WITHDRAWN as §7 said.
- **Two stale statements corrected:**
  - the L32 DOCUMENTED banner is dated history;
  - `00235360` and `00308D90` were read whole.
- **The cap.** The active cap counts units with flag bit 21 (`00308DB3`).
- **§5 upstream.** Anchored from the raw call index; the unanchored "encounter/spawn controllers" line is struck.
- **`004058E0`.** It is not a spawn body.
- **FRONTIER-subtree fixes:**
  - six sizes;
  - one call list;
  - three copy descriptions;
  - three "no shared callees" claims.
- **No row.**

**how-a-combo-continues-and-what-it-blocks** (15 blocks):
- **Bit 22.** Unit flag bit 22 is answered: an engage auto-attack is in progress (set `003130D2`, cleared by
  `00308270`).
- **§5 upstream.** Both functions now have callers: `0030FA00` from `BattleUnit_UpdateCombatFrame`, and `00388660` as
  step-table slot 10.
- **Anchors.** The HUD cap is anchored (`00289DE7`–`00289E08`). The "25 arms" figure is counted.
- **Reconciled.** The `+0x6B4` "unread" sentence is reconciled with UQ-118. `0023B146` is read.
- **The HUD residue.** Narrowed: the routine records a popup and draws nothing itself.
- **One row:** GR-3.

**the-action-definition-row** (20 blocks):
- **Status line.** It carries UQ-106's SUPERSEDED pointer.
- **§2.2, answered from the binary:**
  - `+0x04` is the knockback-chance base (`00388B50`);
  - `+0x05`'s `00384F40` is the Reflect retarget (the result-record page);
  - `+0x0A` is the MP cost, read as a byte (`where-mp-comes-from` CS-5);
  - `+0x1C` is the category (BT-4);
  - `+0x1D` / `+0x1F` / `+0x20` are the enmity parameters (Z-5, `003216E0` read whole);
  - `+0x21` is unread (AY-2);
  - `+0x24` is narrowed: the selector's three cases, and 39 / 68 / 436 rows;
  - `+0x38` is the list position, reader `00237FC0`;
  - `+0x3A` is a bit number into the kind-10 mask (`00312170`).
- **Stale prose.** The `+0x28` "Esper attack" wording, the fence names, the "unread" list and the UQ-107 "still not
  read" line are reconciled.
- **§8.** Seven evidence rows.
- **Four rows:** GR-4..GR-7.

**combos-and-the-guard-parry-flag** (11 blocks):
- **NOTE conversion.** Scope / Findings / Evidence (12-row tier table) / Method (with a positive control) / Limits.
- **Anchors.** "Rolled eleven more times" and the navigation early return are anchored.
- **`02AEDFE4`.** Its writer is cited (ComputeComboChance, `00388648`).
- **"Status bit 23".** Corrected to unit flag bit 23, the engaged flag.
- **The combo cap.** Corrected: it reads the attacker, not the target.
- **One row:** GR-8.

**where-a-stat-number-comes-from** (10 blocks; R3 older layout):
- **New sections:** Key addresses (and data addresses), Call chain (two direct callers, from the raw call index),
  Modding notes, Evidence (tier table), What is not known, Related.
- **Corrected:**
  - the party helpers take base HP and base MP, not a level (`002F8E50`, `002F9180` read whole);
  - the two "affinity flag" dwords are status masks;
  - the main value floors at 1.
- **Anchored.** The cancel-on-change tail is anchored instruction by instruction. The pair is Confuse and Berserk (bits
  5 and 27).
- **The three status lists.** Decoded (`wsn_lists.py`): Strength, Magick Power, max HP.
- **The page's "does not claim" list.** Every item is answered.
- **No row.**

**ranged-weapon-recipes** (11 blocks):
- **The lists.** Recipes 25 and 26 are decoded from the image (`rwr_recipes.py`, which checks both pointers) and match
  §2.
- **§5 corrected:**
  - the threshold loader, the weather scales and the outcome resolvers are in the **first** list;
  - slots 25 / 94 / 95 (`00389040`, `0038B220`, `0038B6A0`) are in neither list;
  - the committed element stages are slots 96–99, on weapon rows.
- **The first list.** Corrected: it runs at execution (stage 9), not as a UI preview.
- **§4.** ActionDefinition `+0x12` / `+0x13` are corrected as not read by these recipes; the hit chance starts at 100.
- **Anchors.** MWeather class 2 is anchored (`003895D0` read whole; the MWeather page).
- **Stale prose.** The E-3 lines are reconciled.
- **No row.**

## Checks on the patched export (HEAD `4407f8484`)

- **`verify_doc_addresses.py`:** all 8 pages `ok`. 1,101 entry and 1,093 interior citations, and 0 `.text`
  non-function citations to confirm.
- **Neighbour differential.** `audit_side.py` (in the record) runs `check_publish_neighbours.py`'s own `findings()` (audit_crossrefs
  over the whole tree) and `broken_links()` (check_links `--raw`) on the export, before and after. I did not run the
  guard itself, because it copies the published paths from the shared working tree, which this draft must not touch.
  - **Before:** 0 findings and 0 broken links on the eight pages.
  - **First draft:** 21 UNACCOUNTED NEIGHBOUR findings on four pages, from new entry-address citations of callers and
    callees outside a crossing section. Those far ends are now named by role. The one central new subject, the kind-0
    owner transition `00237DF0`, got a crossing paragraph instead.
  - **Final:** 0 findings and 0 broken links on the eight pages.
  - The guard itself must still run at publish time.

## Routed, not edited (other owners' pages)

- `08-Combat-Formula/CONTRACT-stat-derivation.md` L61, "plus the level at `+0x08`": it is base HP.
- `Battle-Stats-Record/the-battle-stats-record-field-map.md`: the foe cap is `0x3B9ACA00` = 1,000,000,000, not
  999,999,999.
- `08-Combat-Formula/CONTRACT-weapon-recipes.md` §14: `0x3858E7` is not orphaned code. It is inside
  `BattleFormula_EvaluateTargetPreview`, which has two direct callers.
- The UQ-80 manifest still lists `action_data` `+0x0A` / `+0x04` / `+0x1D` / `+0x1F` / `+0x20` / `+0x3A` as shape. They
  are placed by this pass.
- `Actor-Storage-Record/the-record-behind-every-actor.md` L1819: kind 7 also sets `+0x27`.
- `Battle-Unit/the-battle-unit-field-map.md` L1022: `00321810` stores 0 at `+0x19`, not `edx ? 1 : 0`.
- `_index/ADDRESS-INDEX.md` maps `004058E0` to the spawn page (SWE2-FRONTIER).
- `09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md` L1632: the restore copies back one bank, not both.
- **L-13's live-only residue** (a slot-0 autosave load with non-zero banks). FRONTIER's ruling names the carrier
  `FABLE-REQ-ASTRA-L13-BANKS`, which is DONE on EXP-080 with both banks zero. Under the same ruling, uncarried residue
  goes to `FRONTIER-RT-RUNTIME-SURROGATE`, and that board operation is still to do. An OPEN register row instead would
  conflict with the runtime SUPERSEDED rule, so none is drafted.

## Uncertain, or for the owner

- **Two pages are READY with no open residue:** `where-a-stat-number-comes-from` and `ranged-weapon-recipes`. I left
  them PARTIAL ("awaiting the owner read") rather than self-promote them. FABLE drafted their new content, so the
  DOCUMENTED call belongs to the completion owner.
- **The spawn fork proposed REOPENED → PARTIAL.** I kept REOPENED, as the field-runtime page does, until a fresh graph
  audit and falsification pass.
- **Interpretations worded as matches, not proofs:**
  - the HUD's `0x12` cap is read as "12", matching the twelve-hit ceiling;
  - the bit-22 sweep covers `[reg]` operands only (tier 2 on the page).
- **Readers that come from call direction:** `00312170`'s mask is ORed into "the second unit it is handed", and the
  `+0x04` knockback formula names its terms by argument order (first / second). In both, which unit is the actor was
  not traced.
- **`ids.tsv`.** The placeholder numbering (`n1xx` … `n6xx` by page) is only for drafting.
