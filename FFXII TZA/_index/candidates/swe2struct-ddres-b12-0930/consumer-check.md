# Consumer check: DD batch 12 corrections on the registry page (SWE2-STRUCT for OPUS, 2026-09-30)

SWE2-STRUCT's batch 12 (this folder's README, checks R2 and R3) struck four superseded statements on the registry page and
added a dated note beside each struck span. Nothing was struck on the FCP page or the render-record page; both carry notes only.

- **Corrects:** in authored-data-table-registry.md:
  - in AG-4's residual, "together with a **data-driven index** (`movsxd rdx, [rax + 0x118]`, from `0208E680`). So any slot, slot 50 included, can be bound through that path without a RIP-relative operand naming it.";
  - in the tail read, "and `00238260` passes `3` in that word (`00238364`)";
  - also in the tail read, "So the eleven are **completion markers**, not pointers: the loaded bytes live in the resource block `0036A190` allocated, tagged at its header by `0036C660`, and nothing reads the twelve but the six-resident count `00233E00`.";
  - "marks the completion of the request for";
  - in the upper-sixteen table, the cell text "the slots hold scalar values, not table pointers".
- **Affected:** 02-Resource-And-Asset-Pipeline/authored-data-table-registry.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the registry page's own sections (the 2026-09-16 indexed-reader item and the `0x02EBF198` disposition) | revised-here (notes added; the "live tension" is resolved in place) |
  | the-resource-request-queue.md §2.4, lines 305-308 ("hand `3` in that word … the slots are completion markers") | disagrees; routed to OPUS for its owner (not edited) |
  | license-board-grid-format.md lines 154-156 ("a generated setter marks each completion") | disagrees in its 2026-09-11 sentence, agrees with its own 2026-09-13 correction on line 174 (readers follow the slot pointer); routed (not edited) |
  | EVIDENCE-STANDARD.md line 4429 (the `02EBF198` row: "a **data-driven index**, so any slot is reachable unnamed") | disagrees; routed (not edited) |
  | _inbox/FABLE.md line 4791 ("twelve loaded-resource pointers") | agrees |
  | AUDIT-LOG.md line 29908 | historical record; left as written |

- **Regression:** Database/FFXII TZA/_index/candidates/swe2struct-ddres-b12-0930/b12_struct.py (149 checks, FAILS 0, including R2's 48-of-48 `licd` control and R3's 42 binder call sites).
- run: b12_struct.py at e54b8e670 (149 PASS, FAILS 0, re-run by OPUS on the worktree)
