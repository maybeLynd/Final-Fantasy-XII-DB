# Consumer check: BattleMenuChildWidget1620's base-handler layout and the re-homed +0x340 dword (OPUS, 2026-09-28)

## What is corrected (all OPUS's own rows)

1. `BattleMenuChildWidget1620 +0xC0` (640 B) and `+0x344` (380 B) said *no access at these displacements by either body
   installed on this object*. The installed handler `0027AD70` tail-jumps to `003EE420` with `rcx = this`, and that body
   walks two 0x1E0-byte records from `+0xC0` and reads the fields at `+0x480..+0x4B8`. The tail jump was not followed on
   2026-09-20 / 09-22, so both absence rows were wrong. The replacement rows are the records (`BattleMenuChildRecord1E0[2]`)
   and the fields. Every old row text is kept in the `evidence` cells.
2. `BattleMenuChildWidget1620 +0x340 dword0340` was migrated on 2026-09-20 under FABLE's rule 0, through
   singleton `+0xB240` -> AB30 `+0x710` -> panel `+0x650` -> widget `+0x430`. That chain is right about bytes but wrong
   about the object. `00290707` builds a 0x720-byte widget at `singleton + 0xAB30` when `+0x10F68` bit `0x2000` is clear,
   and every `+0x710` access runs behind that bit. So the dword is re-homed to `Widget0720At0209BE80_AB30 +0x710` with
   its evidence carried verbatim. Inside the 0x61F0 variant, `+0x340` of the child is the second record's `textDraw`.

## Consumers searched

- `grep` over the database for `dword0340`, `BattleMenuChildWidget1620 +0x340`, `+0xB240`, `+0x710` and the absence
  wording.
- **`00-Engine-Core-Runtime/CONTRACT-per-frame-update-gate.md`** (OPUS's page) treats `singleton + 0xAB30` as one object
  and names `+0x710` its field. It gains an additive REFINED block after that paragraph. Nothing is struck: the extent
  argument stands for the 0x61F0 variant, and the `+0x710` observation stands for the 0x720 variant.
- **`16-UI/Widget-Object-Model/CONTRACT-widget-object.md`** names the type only in a descriptor table, `+0x48`; it is
  unaffected.
- **Evidence scripts:** `_index/candidates/widget-header-embedding/widget_header.py` reads the type's `+0x00` base row,
  which is unchanged. The AB30 type row gains a SHARED STORAGE note in its evidence.
- **FABLE (rule-0 arbiter)** is notified, because the rule's "innermost declared type" assumed one occupant per byte, and
  this storage has two.

## Regressions

- `battle_menu_child_base.py` P fails on the old rows: a `+0x340` dword on the widget, or no records at `+0xC0`.
- J / R prove the tail jump and the loop bounds. That rejects the "no access" reading.
- R's `cmp ... , 2` loop bounds also reject the census over-reach, which invented records out to `+0x14F0` by
  re-propagating `lea rbx, [rbx+0x1E0]` past the bound.

## child_base_4c0.py (OPUS, 2026-09-28): the 0x4C0 base as its own type

**Finding.** `00298250`, the 0x650 child's handler, builds a standalone 0x4C0 widget at its +0xC0. The call is `00245000` at
`0029849E`, with the handler `002985C0` = `jmp 003EE420`. BattleMenuChildWidget1620's first 0x4C0 bytes are the same object,
because 003EE420 is that widget's base handler. The changes:

- The layout moved into `BattleMenuChildBase4C0`, with each re-homed row's evidence noting the move.
- BattleMenuChildWidget1620 now embeds the base at +0 as `base0000`.
- WidgetChild0650At298250's `unobservedSpan0C0` (1424 B) became the base at +0xC0, four int16 at +0x580..+0x586, a 0xC0
  Widget at +0x588 and an int16[4] at +0x648.
- BattleMenuChildRecord1E0 is routed through the base.

Checks B, E, N and W: FAILS 0. W failed before the patch.

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` BattleMenuChildWidget1620 rows below +0x4C0 | moved to BattleMenuChildBase4C0 (same offsets); one embed row left | revised-here |
| `_types/fields.tsv` WidgetChild0650At298250 `unobservedSpan0C0` | carved into 7 rows | revised-here |
| `_types/types.tsv` BattleMenuChildBase4C0 (new); BattleMenuChildRecord1E0 instance and route | added / re-routed | revised-here |
| `battle_menu_child_base.py` P | reads the base type's rows once the widget embeds it (successor clause); FAILS 0 | revised-here |
| `widget_header.py` H1a / H3 / R | 77 / 84 (the new base type); H3 accepts a header inside an embedded widget base; receipt regenerated with `--write`; FAILS 0 | revised-here |
| `CONTRACT-per-frame-update-gate.md` line 564, `CONTRACT-widget-object.md` | name BattleMenuChildWidget1620 for bytes it still owns, through the base | agrees |

**Run receipt:**
- `child_base_4c0.py` FAILS 0. `battle_menu_child_base.py`, `rule0_apply.py` and `widget0720_child.py` FAILS 0.
- `widget_header.py` and `widget_header_more.py` FAILS 0. `absence_recut.py`, `widget_singleton_nested.py`,
  `help_pane_audit.py`, `a0d0_record.py` and `glyph_run_arrays.py` FAILS 0.
- `types_index.py --validate`: 0 errors. The width, reference, embed, route and census-width checks: 0.
