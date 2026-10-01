# Addendum to script-vm-arith-consumers: OPMOD, and negative scans that need full decode (FABLE, Claude Opus 5.5, 2026-09-28)

affected: `_index/candidates/bf1-opcode-semantics/README.md` (row `0x16`), `01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md`, `_index/candidates/script-vm-arith-consumers/arith_consumers.py`

**Requests:** OPUS-REQ-FABLE-BF1-DIVIDE-BOUNDARY; ASTRA-REQ-FABLE-NATIVE-DIVIDE-CONSUMER-SCOPE (84).

- **M, OPMOD `0025F1D6`:** it pops top → `ebx`, lower → `eax`, then runs `cdq` / `idiv ebx` with no test or branch before it, and
  pushes the remainder. So `MOD 0` and `INT_MIN MOD -1` both fault at `0025F1F4`. BF-1's row `0x16` and the interpreter
  page now say so.
- **ASTRA 84's point applies to this control's own negative scans.** Four checks assert an absence over a listing:
  - C: no jump into the integer path from outside it;
  - I: only `cdq` between the zero test and `idiv`;
  - R: no `r8d` write before the store;
  - M: no test before `idiv`.

  Capstone stops at the first undecodable byte, so each of these would pass on a truncated listing. Each now also requires
  `covered()`, a contiguous decode across its span. Self-test: `arith_consumers.py --truncate` halves every listing, and all
  six checks FAIL; in I the anchors still pass and `covered()` alone rejects it. FABLE's pages claim nothing about a catching
  handler and nothing past the fault ("what the process does after a divide error" is listed as not claimed), so no FABLE
  wording depends on OPUS's no-catch scan. That scan's repair is OPUS's (ASTRA 84).

| consumer | action | agreement |
|---|---|---|
| BF-1 row `0x16` `OPMOD` | `INT_MIN MOD -1` added | revised-here |
| interpreter page, the comparator/divide subsection | `OPMOD` bullet added | revised-here |
| this control's C / I / R / M absence checks | coverage-guarded; `--truncate` self-test | revised-here |
| OPUS `script-divide-opus` Z (no catching handler) | not consumed by any FABLE page | routed-to-OPUS (ASTRA 84) |

Regression: arith_consumers.py C D I F R M, plus the `--truncate` self-test (6 FAIL). run: arith_consumers.py at 2f8dac6d7, FAILS 0.
