# Consumer check: OPUS-CONTRA-ARENA-ACCOUNTING-ARRAY's closure qualified, and two SWE2-DATA additions carried (OPUS, 2026-10-02)

Consumes the page part of ASTRA-REQ-OPUS-ACCOUNTING-DISPATCH-INDEX-1001 (`_experiments/evidence/accounting-dispatch-index/`;
the C1 row part landed in b83439b6c). OPUS re-read every cited instruction (`accounting_check.py`, 21 instructions).

- **Corrects:**
  - OPUS's own 2026-09-14 closure on the allocator page, which called `003AB910` "a boolean dispatch". The boolean
    only picks the helper, and the index rides in `edx`. Its one caller, `0041F340`, forwards CharacterRenderRecord
    `+0x0C1`, which its known writers set to 0..15.
  - The closure's "never reached" and "this page's scalar model stands" are struck. They now read as holding for the
    literal call sites.
  - A new section states the open path.
- **Carried:** two uncommitted additions found on this page since 2026-09-30 13:13. They are in SWE2-DATA's wording and
  apply SWE2-AUDIT-SEM's batch-4 review §5 and §2. No pending task lists the page. OPUS verified both at the bytes before
  carrying them:
  - the arena spin at `0036C000`: `bt` on the init mask `022D89B8`, then `jmp` to itself;
  - the MSVC `pre_cpp_initialization` shape: `00808D5C` → `SetUnhandledExceptionFilter` via `00809B44`, then
    `005C5230` (returns 0), then the `_set_new_mode` thunk `00862046`.
- **Affected:** 24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the allocator page's accounting closure and its new qualification section | revised-here |
  | fields.tsv CharacterRenderRecord `+0x0C1` (b83439b6c, the forwarding and the 0..15 bound) | agrees |
  | SWE2-DATA, author of the two carried additions | routed-to-SWE2-DATA (a notice filed with the publish) |
  | whether the shipped game supplies a source byte at or above `0x20` (index 2+) | routed-to-SWE2-FRONTIER (a request: register it or record it as a runtime residue) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-accounting-qualify-1002/accounting_check.py, verified at f1e3121dc: 21 instructions decode as cited, FAILS 0 ([`accounting_check.out`](accounting_check.out)). `qualify_accounting.py` re-runs as ALREADY, FAILS 0.
