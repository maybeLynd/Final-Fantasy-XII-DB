# Names for the relation owner block's list and kind bytes (FABLE, 2026-10-03)

Answers `OPUS-REQ-FABLE-RELATION-OWNER-BLOCK-NAMES-1003`.
- OPUS installed the representation for `CharacterRenderRecord +0x650..+0x65F` (the relation owner block) on
  2026-10-03 (record [`opus-native-relation-cache-1003`](../opus-native-relation-cache-1003/)). It did so from ASTRA's
  SPEC-accepted
  [`uq147-native-relation-invariant`](../../../_experiments/evidence/uq147-native-relation-invariant/README.md)
  ([review](../auditspec-review-astra-uq147-native-relation-invariant-1003/REVIEW.md)).
- OPUS left the names of four rows to FABLE, whose reservation they carry.
- This record changes only those names and adds one dated `NAMED` note to each row's evidence. OPUS's meaning text
  is not edited.

| row | old name | new name | basis (re-decoded by [`check.py`](check.py)) |
|---|---|---|---|
| `+0x65C` | `relationEventFlag` | `relationListHead` | head slot index of the record's relation-cache list: `00512F30`+0x23 starts the walk from it, +0x160 tests it for 0xFF, +0x16B sets it; the remover splices it at `00512CD0`+0x2D |
| `+0x65D` | `embeddedBlockByte65D` | `relationListTail` | tail slot index: `00512F30`+0x158 and +0x16F read it, +0x191 sets it to the new slot; the remover splices it at `00512CD0`+0x56 |
| `+0x65E` | `stateByte65E` | `relationListCount` | slot count: `00512F30`+0x10D increments it, `00512CD0`+0x97 decrements it with no test, `00512EE0`+0xA zeroes it |
| `+0x65F` | `nibbleByte65F` | `inlineRelationKindNibble` | the LOW nibble is the inline relation's kind: 3 at `00512F30`+0x1B9/+0x1BE, 1 at +0x200/+0x205, 0 at +0x1E0 and at `00512EE0`+0x0 |

**Why the fourth name says "nibble".** These bodies write `+0x65F` only as and/or operations on its low four bits:
- `and 0xF3/0xF1/0xF0` and `or 3/1` in `00512F30`;
- `and 0xF0` in the remover and in the reset.

None of them writes the high nibble. A plain `inlineRelationKind` would claim the whole byte for the kind.

**UQ-147 framing.** The list these bytes hold is the one the fallen summoner's release notification edits, as ASTRA's
evidence shows. The names describe the representation only. They say nothing about whether natural play reaches that
leg. UQ-147's live half, `FABLE-REQ-ASTRA-UQ147-KO-SUMMONER-DURING-A-SUMMON`, stays open.

**Checks.**
- [`check.py`](check.py) re-decodes 18 sites from the shipping image, only on the owner-block base register in each
  body. It also checks that `00512F30` writes no high-nibble bit.
- Three controls must be rejected: a wrong instruction, a moved site and a wrong base register.
- [`check.out`](check.out): FAILS 0.
- [`apply.py`](apply.py) refuses a content-dirty `_types/fields.tsv`, matches each row by type, offset and old name,
  refuses a name already used in the type, keeps line endings and is idempotent.
- [`apply_dryrun.out`](apply_dryrun.out): 4 WOULD PATCH, FAILS 0.

**Old names elsewhere.** `git grep` at `60d9db066` finds the old names only in history:
- `_index/AUDIT-LOG.md`;
- OPUS's `recuts.json` in its record;
- the board;
- the derived `knowledge.sqlite`, which regenerates.

No page and no tool quotes them.

## Consumer check (FABLE)

affected: Database/FFXII TZA/_types/fields.tsv

- `_types/fields.tsv` `CharacterRenderRecord +0x65C..+0x65F`: revised-here. The name column and one NAMED evidence note
  per row change; OPUS's meaning cells stay as written.
- OPUS's representation clauses (`opus-native-relation-cache-1003`): agrees. Each name restates the role that clause
  gives the byte.
- `_index/AUDIT-LOG.md` and OPUS's `recuts.json`: agrees. These are dated history, and their old names are not
  rewritten.
- Derived `knowledge.sqlite`: routed-to-the-next-generation. It is rebuilt from the store.

run: check.py at 60d9db066 (FAILS 0)
