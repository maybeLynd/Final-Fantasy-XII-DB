# Question-marker truth: a partial checkbox counted as closed, and four boxes closed with live residue (FABLE, Claude Opus 5.5, 2026-09-30)

The user's goal, item 4: *fix or report missing and invalid question ids; unknown identifiers must never silently count
as closed.* This record measures the places where a page can count a question as closed while nothing in the register
backs that, beyond what the two green checkers already cover.

## What the green checkers cover, and what they do not (FABLE)

- `check_question_ids.py` finds ids that a document *defines* but the register lacks. It reads 10 definitions, and finds 0
  unregistered and 0 mismatched.
- `check_questions.py` cross-checks the `- [ ]` / `- [x]` boxes and `**ID.**` citations against the table. It is green.
  **Its box pattern is `^\s*-\s*\[[x ]\]`, so a `- [~]` box is invisible to it.**
- The DD rule `status-currency-ruling-fable/documented_rule.py`, which the dashboard runs, counted only `- [ ]` as page
  residue. **A `- [~]` box is a partial answer, and the rule rated all seven pages carrying one READY.**

## Measurements (FABLE)

run: qid_gap.py at 701f1f01a (control: an unregistered GR-999 is flagged)

- [`qid_gap.py`](qid_gap.py) ([out](qid_gap.out)) checks status lines and checkbox lines on live pages for any id-shaped
  token whose prefix the register uses (at least 3 rows) but whose exact id has no row. It finds **0**, so no status or
  box line cites an unregistered id. It also counts **669 ticked boxes in 193 files that name no register id**. These
  are page-local closures; most carry the answer inline.
- [`qid_ticked_open.py`](qid_ticked_open.py) ([out](qid_ticked_open.out)) counts the ticked no-id boxes, continuation
  lines included: 333. Of those, it flags the ones whose unstruck text still says narrowed, partly answered, open or not
  read: 15. FABLE read all 15:
  - **8 are closed:** the flagged word sits inside a real answer (the ladder page ×3, party verbs, loader page ×2,
    input, audio ×2).
  - **4 more are closed on reading:** the console tuning box (SWE2-CONTRACT's narrowing explains the integer accesses),
    the world-tick flag bits (all four answered), the float-table stamp (answered, with its boundary stated), and the
    loader `behindcamera` box (answered: it is a control polygon).
  - **3 are closed with live residue:**
    - VIF1 layer §7, the VU-toucher box: "Still open: which of the 19 caller-less rows are JAL/JR sub-programs"
      (registered here as **UQ-385**);
    - the all-ones convention box: "`+0xB8` / `+0xB9` is narrowed, not closed". The item it defers to, UQ-218, was
      ANSWERED 2026-09-30, so the prose is reconciled here;
    - map screens §7: "Who sends it message 14, and with which index, is not read". That page carries another party's
      uncommitted pass-22 overlay, so it is **routed, not edited** (below).

## The seven `[~]` boxes (FABLE)

Six are normalised here; the numeric-formatting box is routed because that page carries another lane's uncommitted edit.

| page | box | row state | disposition |
|---|---|---|---|
| verbs that only wait | UQ-65, `restartbattle` | SUPERSEDED (duplicate of CR-2, NO ADMISSIBLE SOURCE) | `[x]` with a note |
| VBF archive / st2e | the `action_data` join, AY-9 | ANSWERED (negative, exhaustive) | `[x]` with a note |
| field record bit 15 | the second consumer, C-12 | ANSWERED | `[x]` with a note |
| keymap ini | the code bands, DM-2 | NO ADMISSIBLE SOURCE, every band answered | `[x]` with a note |
| numeric formatting | why Audio enters the cluster | answered by the box's own 2026-09-15 note | **routed, not edited**: SWE2-CONTRACT's DD batch 13 for OPUS is editing the page (uncommitted); the box should become `[x]` |
| the unresolved 158 | common property, AC-2 | ANSWERED 2026-09-26 | `[x]` with a note |
| VIF1 layer | GS-buffer consumer | no row; residue live (device class behind `[01FC35F8]`, the state handlers' stores) | `[ ]` **UQ-384**, registered |

## The rule change (FABLE)

`documented_rule.py` now counts `^\s*[-*]\s*\[[ ~]\]` as open, so `- [~]` and `*` bullets are included. A self-test case
("partial box -> PARTIAL") pins this; the self-test passes 34 cases. Measured before the markers were normalised, the
changed rule rates the VIF1 and keymap pages PARTIAL, where the old rule rated them READY. After this publish:
- the keymap page is READY again, because its marker now matches its closed row;
- the VIF1 page is PARTIAL on real registered residue (UQ-384, UQ-385).

## Routed (FABLE)

- `check_questions.py` (kit gate, owner OPUS): `- [~]` boxes are outside its box pattern, so their ids are never
  cross-checked with the table. Routed as a request; FABLE does not edit a shared gate in place.
- map screens §7 (message 14 to the field-time container `02B47760`): the box should be opened and the residue
  registered once the page's overlay is resolved. Routed to SWE2-FRONTIER, which is disposing of that overlay.

## Consumer check (FABLE)

affected: `Database/FFXII TZA/_index/candidates/status-currency-ruling-fable/documented_rule.py`
affected: `Database/FFXII TZA/_index/OPEN-QUESTIONS.md`
affected: `Database/FFXII TZA/01-Script-VM-Native-Bridge/verbs-that-only-wait-and-verbs-that-do-nothing.md`
affected: `Database/FFXII TZA/02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md`
affected: `Database/FFXII TZA/03-World-Area-Field/Field-Record-Table/field-record-bit15-action-permission.md`
affected: `Database/FFXII TZA/15-Input/Binding-Profiles/keymap-ini-file-format-and-default-controls.md`
affected: `Database/FFXII TZA/99-Unresolved-Residual/the-unresolved-158.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md`
affected: `Database/FFXII TZA/00-Engine-Core-Runtime/the-all-ones-empty-convention.md`

- consumer: the DD rule's self-test and its dashboard run - revised-here.
- consumer: the register - revised-here (UQ-384, UQ-385 added, OPEN).
- consumer: the seven pages above - revised-here (markers normalised with dated notes; strikes none).
- consumer: numeric formatting - routed-to OPUS / SWE2-CONTRACT (their DD batch 13 is editing the page): tick the `[~]` box.
- consumer: `check_questions.py` - routed-to OPUS.
- consumer: map screens §7 - routed-to SWE2-FRONTIER.
