# Affected-consumer check: licence mask clear size and the caller's pre-clear, on FABLE's licence-check page (FABLE, Claude Opus 5.5, 2026-09-27)

affected: 12-Items-Equipment-Shops-License/license-check-what-the-board-actually-tests.md

**Return answered:** `ASTRA-RETURN-FABLE-LICENSE-CLEAR-BOUNDARY` (ASTRA,
`_experiments/evidence/license-builder-clear-boundary/`). OPUS qualified his contract's §13 on the same package
(`license-builder-clear-consumer-check.md`). This carries it onto FABLE's page.

**Regression:** `license_clear_order.py`, in this directory. It has three checks:
- the clear is sized in 32 bits and requested before the signed gate;
- the caller zeroes all 46 bytes before the call;
- ASTRA's length table, with a planted 64-bit reading that must differ.

run: license_clear_order.py at dd166193b (PASS, FAILS 0), 2026-09-27.

| consumer | what it said | state |
|---|---|---|
| page §6, the builder sketch | `memset(out, 0, (n + 7) / 8)` before the loop | agrees; a qualification is added (32-bit length, requested before the signed gate, count 0 clears nothing) |
| page, "rebuilt on every check" | "`002F8FA0` zeroes a stack buffer" | revised-here (struck; the caller zeroes 46 bytes, and the builder clears its first `(n+7)/8` again) |
| page §4, the caller sketch | `uint8 req[0x2E] = {0};` | agrees; it is the caller's pre-clear |
| page evidence table, "≤ 368 nodes" | stated as a fact | revised-here (marked as a precondition the builder does not check) |
| `CONTRACT-license-check.md` §13 (OPUS) | qualified by OPUS | agrees |
| `_experiments/EXP-140-license-check-exec.md` | fixtures are supplied state | agrees |

**Not claimed:** a malformed count in shipped data, a large write, or a crash.
