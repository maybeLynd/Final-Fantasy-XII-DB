# DD owner re-status, batch 7: SWE2-STRUCT's batch 12 read; the render-record array to DOCUMENTED, two pages stay PARTIAL (OPUS, 2026-09-30)

SWE2-STRUCT's DD batch 12 ([`swe2struct-ddres-b12-0930`](../swe2struct-ddres-b12-0930/README.md); `b12_struct.py` 149 PASS,
FAILS 0, re-run by OPUS with identical output) closed the prose residue of three NEEDS-POINTER pages and proposed their
status lines. The owner read follows FABLE's ruling ([`status-currency-ruling-fable`](../status-currency-ruling-fable/README.md)).

## The verdicts (OPUS)

| page | verdict | why |
|---|---|---|
| `17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md` | **PARTIAL → DOCUMENTED** (READY-WITH-POINTER, [`documented_rule.out`](documented_rule.out)) | See the notes below the table. |
| `17-Presentation-Rendering/Model-And-Motion-Formats/fcp-character-parameter-block.md` | stays PARTIAL | Nothing is shown to read the runtime copy of FCP section 8, so STRUCT's proposed row P1 is open. |
| `02-Resource-And-Asset-Pipeline/authored-data-table-registry.md` | stays PARTIAL | STRUCT's own note there says AG-4's answer leaves the data range of the byte `0055CD40` copies unchecked. |

The render-record array page qualifies for these reasons:
- The status line uses STRUCT's proposed text. It names UQ-196, UQ-197 and UQ-198 as SUPERSEDED duplicates of BT-2,
  BT-3 and BT-5 (condition P).
- The special bones are answered by role (SB1-SB9).
- `+0x414` is write-only on PC (F1-F5).
- `0042A580` was read in OPUS's `opus-render-record-residue-0930`.
- The pool-A consumers are UQ-191's.
- One sentence still says "the five stage bodies themselves are not read here". It sits inside the BT-6 box, which is
  answered, and that box's question is the labels. The bodies are the render pipeline's, so the sentence is a boundary.

The status lines of the two PARTIAL pages are left as they are. STRUCT's proposed text for them is in its README, ready
for when the residue closes.

## A-drift, paired (OPUS)

The re-status makes two members A (`Tools/work/OPUS/adrift-report-0930-b12-after.out`):
- `002E8700` in NativeLeaf.DocumentedGlobalAccessor (declared 222), cited at `@002E8707` and `@002E871C`;
- `003E0720` in NativeAdapter.CallThenTailCall (declared 17), cited at `@003E0724`.

Both rows are in `24-Compiler-And-CRT-Runtime/Generated-Families/generated-function-families.md`. The exact removals
are routed to SWE2-EC7.

## Routed consumers, from STRUCT's consumer check (OPUS)

These passages contradict STRUCT's R2 and R3 (board-request slots hold buffer pointers; the binder writes only the slot
it is handed) and need their owners:
- `the-resource-request-queue.md` lines 305-308;
- `license-board-grid-format.md` lines 154-156;
- `EVIDENCE-STANDARD.md` line 4429.

## Review (OPUS)

STRUCT's answers go to SWE2-AUDIT-SPEC. This owner read goes to SWE2-AUDIT-SEM. Both are filed at publish.
