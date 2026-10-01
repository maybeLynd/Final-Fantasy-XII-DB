# Consumer check: nested widgets in WidgetSingleton02B47758 and two of its children (OPUS, 2026-09-28)

**Corrected (OPUS's rows):**
- `WidgetSingleton02B47758_0460 +0xC0` (208 B), `WidgetSingleton02B47758_05F0 +0xC8` (968 B) and
  `WidgetSingleton02B47758 +0xC8` (448 B) said "no access by either body installed".
- In each, `+0xC0` holds a nested widget.
  - `_0460`'s handler builds a 0xD0 widget there on message 14 (new type `WidgetChild00D0At3CA530`).
  - The other two handlers drive a widget header there through `00273A20` / `00244F00` / `00244DD0`.
- The `qword00C0 void*` rows are that header's handler slot, and are absorbed into `nestedWidget0C0 Widget`.
- Old names, ctypes and meanings stay in the new rows' evidence.

**Consumers searched:**
- `grep` for the three type names outside `_inbox` / `_experiments` finds only the generated `TYPE-COVERAGE.md` and this
  package.
- `widget-header-embedding/widget_header.py` H1a now also verifies the new 0xD0 type's site: 72 / 81, with the receipt
  regenerated. H3 still holds, because the nested rows start at `+0xC0`, not below it.

**Open:**
- The nested widgets of `_05F0` and of the singleton are not constructed in their handlers, so their extent past the
  0xC0 header is not claimed.
- `HelpMessageSlotRecord0100` (2 hits) and `PaneListWidget0B68` (1 hit) remain in the audit.

**Regression:** `widget_singleton_nested.py` P fails on the old rows.
