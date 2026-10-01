# Consumer check: the help-slot and pane-list rows (OPUS, 2026-09-28)

**Corrected (OPUS's rows):**
- `HelpMessageSlotRecord0100`'s header rows, including six "no access by either body installed" spans, become
  `widgetBase0000 Widget`, because the element is built whole at `002BFCCA`. The `+0x08` span was contradicted by
  `00247930`'s read of the header's `+0x10`.
- `PaneListWidget0B68 +0xC0..+0x17F` (four rows) is the nested 0xC0 widget that `0029C850` builds, now
  `nestedWidget0C0 Widget`.
- `+0xB4C` (28 B) is split around `selectedSlot` at `+0xB58`.
- Old rows are named in the new rows' evidence.

**Not changed:**
- The census hit at `HelpMessageSlotRecord0100 +0x60` (`002BFBFC`). That code's `rdi` is the parent
  `HelpMessageWidget0500`, so it was a seeding artefact of the audit, not an access.

**Consumers searched:**
- `grep` for both type names in candidate scripts finds only `store-byte-array-widths/byte_array_widths.py`. It asserts
  `PaneListWidget0B68 +0xB44`, which is unchanged, and still gives FAILS 0.
- `widget-header-embedding/widget_header.py` H1a now verifies `002BFCCA`: 73 / 82, with the receipt regenerated.
- No page names these rows.

**Audit closed:** all 13 types carrying the "bodies installed" absence wording have been re-censused from their
installed handlers.
- Seven were corrected: BattleMenuChildWidget1620 (dc2bcc912); ManagerSubA0D0Record (4250ca069); WidgetSingleton02B47758
  and its _0460 / _05F0 children (6a597a1a0); HelpMessageSlotRecord0100 and PaneListWidget0B68 (this record).
- The other six had no hit outside loop enumeration: BattleMenuWidget2DC0, BattleMenuPanelWidget3010,
  ManagerSub0209BE80_AB30, ManagerSub7FB0Record, PaneSlotWidget0160, ManagerSub0209AC60_02F8_00C0.
