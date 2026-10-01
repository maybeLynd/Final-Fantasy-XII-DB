# Consumer check: the absence re-cut on 16 widget types (OPUS, 2026-09-28)

**What is corrected.** OPUS wrote "no access at these displacements ..." rows between 2026-09-20 and 09-22. On these 16
types, the rows were contradicted by a handler-seeded census that walks the control flow:

- HelpMessageWidget0500, PaneListWidget0B68
- Widget02CA6C80, Widget02CA9790, Widget02CA99B0, Widget02CA99B4, Widget02CA99E8
- WidgetSingleton01EFAC10, WidgetSingleton01FD4940, WidgetSingleton0208E6C8, WidgetSingleton0208E6D8,
  WidgetSingleton0209C300, WidgetSingleton022C83A8, WidgetSingleton02AEE4D0, WidgetSingleton02CA8FE0,
  WidgetSingleton02CA9678

The census is `census_receiver_fixpoint.py SEED=ctor`, seeded on each type's handler at its function start, with
loop-enumerated sites excluded.

**How the rows were replaced:**
- Each contradicted row is re-cut by one rule (`absence_recut.py` R). Accessed offsets become fields as wide as their
  widest access, runs of 16-byte SSE copies become blocks, and untouched bytes stay spans.
- `PaneListWidget0B68 +0x180` is a nested Widget header (N).
- Every old row's name, ctype and meaning is kept in its replacements' evidence.
- The 245 census sites are frozen in `census-hits.json`, each with its instruction text. `absence_recut.py` C
  re-decodes every one against the certified image, and `--census` re-runs the census.

**Seeding discipline, found while building this.** The type rows' text also names interior addresses. These include
the initialiser's handler-call site `00246748` and mid-handler sites such as `00581A26`. An interior seed assumes
`rcx = this` mid-function, so only function starts are seeded. The hit set is identical either way.

**Consumers searched:**
- `grep` over the database for these 16 type names outside `_inbox` / `_experiments` finds the generated
  `TYPE-COVERAGE.md` and these candidate scripts, which still give FAILS 0 after the patch:
  - `help-pane-audit-opus/help_pane_audit.py`
  - `widget-header-embedding/widget_header.py`
  - `small-unobserved-rows/small_rows.py`
  - `store-byte-array-widths/byte_array_widths.py`
- No page cites the replaced rows.

**Not changed:**
- `ManagerSub0209BE80_8FA0 +0x1038`: its hit lands on an already-named row (`int1038`).
- 32 other types with the same wording (49 carry it; 17 had hits): the handler-seeded census finds no hit in their rows, or no function-start
  handler is named for them. For the latter, their absence stays as scoped as its wording.

**Regression:** `absence_recut.py` W fails on the old rows, because an unobserved row covers a frozen hit.
