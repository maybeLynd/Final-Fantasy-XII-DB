# Widget-derived types embed the shared Widget header as one row (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

Corrects: `_types/fields.tsv`, the rows below `+0xC0` of 68 widget-derived types (1,412 rows). These are the
WidgetSingleton* and Widget* types, BattleMenu*, PaneListWidget0B68, WidgetConsumer02AEE4C8 and ManagerSub0209BE80_*.
Each of them re-described the shared Widget header from its own per-type census. Three errors resulted:
- **Misleading "no access" gaps** over header fields the Widget type names. These surfaced as index contradictions in
  the unobserved-row audit.
- **+0x98 / +0x9C typed as dwords**, where the base has four int16s written once by a packed initialising store.
- **+0xA1 typed as a word**, where the base has two bytes.

**The store's own convention.** GlyphRunWidget1498, ActiveLogWidget40C8 and MapScreenPage already carry
`+0x0000 192 widgetBase0000 Widget`. That row is the base `002465F0` writes on every constructed widget. This
correction applies the same convention to the other types.

**Receiver proof, per type (H1).** A type is normalised only when the site its own allocation record cites was
confirmed in code. The site must load the type's own size into `ecx` and call the widget allocator `00244F50`, or load
it into `edx` and call the in-place constructor `00245000`. Either way, the object's base is a widget.
- **70 of 78 candidates verified** (`verified-sites.json`).
  - 67 by the site their own record cites. The owning function is disassembled; `mov ecx|edx, <size>` must fall
    within 16 instructions of the call, with no intervening write to that register.
  - 3 interior types by an explicit in-place site, proved from the owning function's instructions:
    - BattleMenuChildWidget1620 at `002779FA`;
    - ManagerSub7FB0Record at `002968DE`, a 0xF0 widget at the record base;
    - PaneSlotWidget0160 at `0029BBDA`.
- **Held back:** the 8 whose records cite no single construction site. They stay as they are.
- **MessageWindowRecord is included, after its one width conflict was settled (H4).** It declared `+0x40` as
  `flags040 uint8`, but `002465F0` writes that field as a dword (`0024666D`), and the registry probe byte-tests bit
  0x10 of it (`002A28F8`). Its dispatcher's uses of base fields (`+0x38`, `+0x7C`, `+0x9A`/`+0x9C`/`+0x9E`, `+0xB4`)
  are kept in its embedded row's text.

**The base's widths (H2).** In the widget code, `+0x98 / +0x9A / +0x9C / +0x9E` are accessed as words (9 / 9 / 15 / 19
sites). Every dword or qword access there is a packed store (`002445F3`, `00246711`) or an 8-byte copy.

**Regression (H3).** H3 fails on the current store: 68 of the verified types still re-describe the header. It passes
after `Tools/work/OPUS/widgethdr/patch_store.py`. That was tested on a copy, where `types_index.py --validate` reports
0 errors and 0 gaps.

**Replaced rows.** All 1,412 are kept verbatim in `replaced-header-rows.tsv`, which the patch writes: 924 TYPE RESOLVED,
449 DISCOVERED, 32 SIGNATURE RESOLVED and 7 SEMANTICALLY IDENTIFIED. The seven semantic rows:
- two are base facts the embedded row restates: ManagerSub7FB0Record `widget0000` and
  ManagerSub0209AC60_02F8_00C0 `handler0000`;
- four are ManagerSub0209AC60_02F8's proc using base fields (flags bit 11, `+0x98`, `+0x9C/+0x9E` from two globals).
  They are copied onto that type's embedded row, as MessageWindowRecord's dispatcher uses are.
- one is ManagerSub8FA0SlotRecord02B8 `occupancyWord`: the container tests the base's `+0x00` proc qword to decide
  whether a slot is in use. It is copied onto that type's embedded row. Each type's specific use
of a base field stays in that file and on its pages.

**Consumers:**

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv`, 68 types' header rows | one embedded `Widget` row each; replaced rows kept in `replaced-header-rows.tsv` | revised-here |
| `_types/types.tsv` evidence cells naming header fields (`firstChild`, `halfRatePhase`, and MessageWindowRecord's `flags040`) | dated evidence text; the fields are the base's, and the old rows are in `replaced-header-rows.tsv` | agrees |
| `_index/AUDIT-LOG.md` | history, not edited | agrees |
| the unobserved-row vs index audit (`Tools/work/OPUS/silent_unobserved.json`) | 74 of its 106 rows sit in these headers and are closed by this; the rest stay open for one-type-at-a-time verification | agrees |

Run receipt: executed at bbd3af82a - `widget_header.py` H1 PASS (70 verified), H2 PASS, H4 PASS, H3 FAIL on the pre-fix store and PASS on the patched copy (FIELDS_PATH); `types_index.py --validate` on the patched mirror: 0 errors, 0 gaps.

## Review follow-up: whole-object versus prefix proofs, and a drift check (OPUS, 2026-09-27, night)

**Counts, corrected.** 26ccf838a's commit message says "64 widget types". The store, this record and the receipt
agree on something else:
- 68 types were normalised;
- 70 carry the embedded row, which includes GlyphRunWidget1498 and ActiveLogWidget40C8, already in the convention;
- MapScreenPage also embeds, but by its earlier convention, not by a verified site.

The number to cite is **68 types, 1,412 rows**.

**H1 overstated one proof.** Its label said every verified site "loads the type's own size". That holds for 69 of the
70. ManagerSub7FB0Record's site (`002968DE`) builds a **0xF0** widget at the base of a **0x110** record. That proves
**base identity**: the record begins with a widget, so the 0xC0 header is inside it. It does **not** prove the
record's extent. The 0x110 rests on the parent's stride arithmetic (`types.tsv`: `EMBED ManagerSub0209BE80_7FB0 +0x0
stride=0x110 count=6`), and the record's own `ctor` cell already says the constructor reaches only the first 0xF0.

The control now separates the two proofs:
- **H1a whole-object:** 69 types, the loaded size equals the declared size;
- **H1b prefix-only:** exactly ManagerSub7FB0Record, `prefix:0xf0`;
- **N:** no `mov edx, 0x110` precedes `002968DE`, so the prefix cannot be promoted.

**The receipt is immutable now.** `widget_header.py` used to rewrite `verified-sites.json` on every run. It now writes
only with `--write`; otherwise **R** checks that the tracked receipt reproduces. Each entry gains its kind (`whole` or
`prefix:0x..`). The 70 site triples are unchanged, which was checked against HEAD before the rewrite.

**Drift check.** The shared header's truth lives on `Widget`, and each derived type references it with one row.
`Tools/analysis-kit/gfz-scripts/check_embed_overlap.py` gains a constructor-proven-base rule: every type in this
receipt must cover `[0, 0xC0)` with ONE row whose ctype is `Widget`. It does not reject:
- a derived type's own fields at or past `+0xC0`;
- a prefix-constructed record.

Its synthetic controls:
- a re-described header is REPORTED;
- an embedded header plus a derived field is SILENT;
- a prefix-constructed record whose tail outgrows the widget is SILENT.

Exceptions would be explicit, each with a reason (`BASE_EXCEPTIONS`); there are none.

Receipt, run verified at d04bfb7ee:
- on today's store: 0 of 70 re-describe the header;
- on the pre-normalisation store (`26ccf838a^`): exactly 68 do, the 68 normalised.

**Derived uses of base fields are preserved.** They were checked on the embedded rows:
- MessageWindowRecord's dispatcher (`+0x38`, `+0x7C`, `+0x9A` / `+0x9C` / `+0x9E`, `+0xB4`, the `+0x40` bit-0x10
  probe);
- ManagerSub0209AC60_02F8's message-1 initialisation (flags bit 11, `+0x98`, `+0x9C` / `+0x9E` from two globals);
- ManagerSub8FA0SlotRecord02B8's occupancy test on the `+0x00` proc qword.

**Review.** SWE2-AUDIT-SPEC's ACCEPT of 26ccf838a (`Tools/work/SWE2-AUDIT-SPEC/REVIEW-OPUS-REQ-0927-AFTERNOON.md`,
item 2) covered the batch as submitted, and that request said "64". This follow-up changes the control's claims (H1a,
H1b, N, R) and adds a gate rule. Both go back to an independent reviewer; tiling is not acceptance.

| consumer | action | agreement |
|---|---|---|
| `widget_header.py`, `verified-sites.json` | H1 split whole / prefix; the receipt carries the kind and is immutable | revised-here |
| `Tools/analysis-kit/gfz-scripts/check_embed_overlap.py` | constructor-proven-base rule plus its controls | revised-here |
| `_types/types.tsv` ManagerSub7FB0Record | already states the 0xF0 prefix and the stride-derived 0x110 | agrees |
| `_types/fields.tsv`, the 70 embedded rows | unchanged; derived uses on the rows confirmed | agrees |
