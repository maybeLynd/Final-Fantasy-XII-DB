# DD residue closure, batch 5: the second `02` batch — `chse` and `lmap` (SWE2-CONTRACT, 2026-09-30)

Request: `OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929`. The batch was run by OPUS's Claude subagent in the SWE2-CONTRACT
lane. Scope: the two remaining pages of `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/` on the worksheet:
- `chse-character-se-tables.md`
- `lmap-menumap-location-graph.md`

Both were clean before editing and LF-only. No status word was moved; OPUS re-statuses after its owner read.

## What changed, per page (SWE2-CONTRACT)

| page | answered from the database | answered by this record (static) | registered |
|---|---|---|---|
| `chse` | SB-2 (FABLE, the reader section); the Audio helper `003A1650` = SE block registration (`seb-se-block-index.md` §3.2); the letter = the model-id letter (`character-render-object.md`) | slot 3 = the actor's fallback pack key (`chse_slot3.py` T1–T10); header `+0x04` / `+0x06` / `+0x0C` unread (T1, T11); §3 contract rebuilt | none |
| `lmap` | the 60,000-range ids (§10.7); `003BDDE0` / `003BDFF0` / `003C1A20` (map-screens §4, SWE2-FRONTIER); the zone routes drawn as lines (map-screens UQ-156, FABLE) | array C read by `003BCDE0`: endpoints, gate, viability pairs (`lmap_readers.py` C1–C3); A's `x`/`y` → the draw row (P1, P2); the marker arm (P3–P5); §3 contract rebuilt | RC-35 (the 8-byte block), RC-36 (who reads B `+0xC`) |

Stale text (§3 / §4 / §7 / §9 "no reader" on `chse`; §2.3 "not established" and §6 "Was a reader found? No" on
`lmap`) is marked superseded in place and kept.

## chse slot 3, in player terms (SWE2-CONTRACT)

When a party member is read in (the party read-in state machine, state 4), the game swaps the character's
refcounted voice/resource pack (UQ-50). It takes the pack key from the character's battle record first. Only when
there is none does it fall back to slot 3 of the character's `charseinfo_<letter>` row. `0xFFFF` there means no
pack, and the swap is skipped.

The 39 authored values sit in `_c`, `_m`, `_n` and `_s`. Which shipped actors reach that step with no battle-record
key is not bounded here.

## Receipts (static, shipping image `73461d08…`, run at HEAD `7f2e5b34b`) (SWE2-CONTRACT)

| script | result |
|---|---|
| `chse_slot3.py` (`chse_slot3.out`) | T1–T11 PASS. T1: the table pointers are read only by `002EA530` and `002ED950` (control: the loader's `lea`). T3/T9/T10: callers of `002ED950` = `002E60F0`, `002EA6E0`, `002ED910`; of `002ED910` = `0037B4D0`. The whole-image E8/E9 and data-pointer negative has controls at `002E6152` / `0037B85B`; its one `.pdata` entry is unwind metadata. D1/D2: the shipped values. |
| `lmap_readers.py` (`lmap_readers.out`) | C1–C3, P1–P5 PASS, each an instruction pin. C3 and P4 carry positive controls (`+0x10` at `003BCDEB`, `+0x12` at `003C24F7`). **P4 narrowed 2026-09-30 on FABLE's `rc36-lmap-label-fable-0930` (`9a4cd5784`):** it holds only through the `003BDDE0` call at `003C253F`; the marker arm continues to `003C25BD`, which does read `+0x0C` (the drawn destination label). The check's range was always `≤ 0x003C253F`; the row's earlier "arm does not read `+0x0C`" prose overstated the bound. |
| `check_questions.py` | `questions consistent: the table and the document checklists agree` (INCONSISTENT grep: none) |
| `documented_rule.py` (`documented_rule.out`) | `TALLY PARTIAL=1 READY=1 of 2`, FAILS 0 — `chse` READY; `lmap` PARTIAL on RC-35 and RC-36 (the pre-commit run flags RC-36's record path as untracked under condition T until this publish lands) |

A first draft of `chse_slot3.py` T8 read `002EB7A0`'s pass-through arm as "no letter", and so claimed only 1 of the
39 slot-3 values reachable. The party read-in page (the `002EB7A0` remap line) and the `cmp ecx, 0xd; ja` pin show
that model ids pass through with their letter. The claim was withdrawn before publication, and T8 now pins the
pass-through.

## Consumer check for the corrections in this publish (EVIDENCE-POLICY 4a/4b) (SWE2-CONTRACT)

corrects: `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/chse-character-se-tables.md` §7 — "Anything about the
loader. None was found" and "Whether `version = 1` gates anything … no reader found" (struck, superseded in place);
§3 / §9 "no reader" (superseded in place).
corrects: `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/lmap-menumap-location-graph.md` §6 "Was a reader
found? No" and §2.3's "not established here" (superseded in place, not struck).

Current consumers and their state:
- consumer `18-Audio/Sound-Bank-And-Voice-Formats/seb-se-block-index.md` (links the chse reader section): agrees.
- consumer `01-Script-VM-Native-Bridge/Party-Presentation-Verbs/the-party-read-in-state-machine.md` row 4
  (`002ED910` resolves the key): agrees.
- consumers `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/README.md`, `_index/ASSET-FORMATS.md`,
  `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/the-dat-and-bin-extension-buckets.md` (count
  CHSE as a magic): agree. None claims the reader absent.
- consumer `16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md` §4, row `003C1680` ("none of its
  `countA+countB` points is a B-entry whose `word[+0xC]` fails `003C17E0`"): disagrees. The read at `003C17A2` runs
  only for kind 0, the zones (P5). Routed to SWE2-FRONTIER, the rows' author, as a board request; not edited here.
- the two pages themselves: revised-here.

Regression: `chse_slot3.py` rejects "no reader" for the loader and "version gates something" (T1, T11: the only
table-pointer users, and no read of `+0x04`). `lmap_readers.py` P5 rejects the "B-entry" reading of `003C1680`.
verified at 7f2e5b34b (run: 7f2e5b34b), exit 0.

## Not done in this batch (SWE2-CONTRACT)

- The owner read and any status move: OPUS's.
- RC-35 and RC-36: static, named next steps; not routed to ASTRA.
- The ch/in-only distribution (`PROPOSED-repos-c7-21`) and why three CHSE tables ship empty: left as the page's
  limits. The second is authoring intent, and its static effect is stated on the page.
