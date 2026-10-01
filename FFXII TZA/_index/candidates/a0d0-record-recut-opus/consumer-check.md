# Consumer check: ManagerSubA0D0Record re-cut (OPUS, 2026-09-28)

**What is corrected (OPUS's rows of 2026-09-22):**
- Seven "no access at these displacements by either body installed on this element" spans.
- The element's handler `003F8250` itself writes `+0xE8..+0x108` and reads `+0x38`.
- Its callees reach `+0xC0` (`003F8790`) and interpolate the rects (`003F8140`).
- The spans were censused before the census walked the control flow (FRONTIER 57f9d58ab), so the handler's message
  branches were not followed.

**Replacements:**
- The header rows below `+0xC0` become `widgetBase0000 Widget`. The element is built whole by `00245000` at `003F7F0D`,
  like the 71 other widget types.
- The tail is carved into `children`, `boundObject`, `rectCurrent` / `rectTarget` / `rectFrom`, `t`, `selectedIndex` and
  `flag108`.
- Every replaced row's name and ctype stays in the new rows' evidence (`was ...`).

**Consumers searched:**
- `grep` for `ManagerSubA0D0Record` over the database finds only `_index/TYPE-COVERAGE.md`, which is generated.
- The parent `ManagerSub0209BE80_A0D0` embeds the element by type name. Its route is unchanged.
- `widget-header-embedding/widget_header.py` H1a now verifies this site (71 / 80). The `verified-sites.json` receipt is
  regenerated.

**Regression:** `a0d0_record.py` W fails on the old rows: an absence row over any of the 20 displacements the handler
path accesses.

**Audit context:** 12 other types carry the same "bodies installed" absence wording. A handler-seeded census, excluding
loop-enumerated sites, finds hits in `WidgetSingleton02B47758` / `_05F0` / `_0460`, `HelpMessageSlotRecord0100` and
`PaneListWidget0B68`. Those are read one by one in their own packages, and are not corrected here.
