---
experiment: EXP-074
title: angle conversion boundary, not blanket pass-through
status: COMPLETE - bounded isolated original-code evidence
contract: none - Conversion-boundary controls run 002E5F90/002E5E10/0033CB70, not the facing-and-steering contract entry set; a category match is insufficient.
evidence_class: isolated original-code
method: B - isolated original-code execution
live_game: false
execution_scope: Ten new paired conversion-boundary inputs through original reapply/writer and separate helper; writer callbacks controlled, older runs not replayed.
contract_coverage: No matching existing contract at recovery; this disposition does not close a database knowledge or contract gap.
tool: evidence/EXP-074-angle-conversion-boundary/check.py
date_designed: 2026-09-12
date_run: 2026-09-12
metadata_recovered: 2026-09-12
---

# EXP-074: angle conversion boundary, not blanket pass-through

**Result:** ten paired original-code controls passed on first execution; a
private pass-through mutation was detected. ASTRA, 2026-09-12. Offline evidence
with explicit writer callback stubs; no live game access.

## Question and method

After [EXP-072](EXP-072-facing-writer-controls.md) and
[EXP-073](EXP-073-facing-reapply-comparison.md), corrections `2f419ae` and `e307fa1`
say large angles beyond the signed-conversion threshold pass through unchanged.
The [facing page](../06-Movement-And-Navigation/heading-speed-to-position-delta.md)
states this for magnitude at least `2^31 * two pi`; the
[maths page](../24-Compiler-And-CRT-Runtime/Maths-Library/the-maths-the-game-runs-on.md)
attributes it to rounding absorbing the product once the quotient is too large.
EXP-073 only observed unchanged results at +/-1e20, infinity and one quiet NaN.
Those inputs cannot establish absorption immediately beyond the conversion limit.

The [checker](evidence/EXP-074-angle-conversion-boundary/check.py) reuses the
verified original 26-byte wrapper, 374-byte writer and 128-byte helper, with all
six constants byte-identical to EXP-073. Ten **new** inputs test adjacent floats
at both signed-conversion limits, +/-1.4e10 and +/-1e11. Sealed earlier controls
were not replayed. Each wrapper fixture runs once; each paired helper fixture is
fresh. Full reference EXE identity is checked before extraction.

The wrapper reads the supplied initial field A8 and tail-jumps into the writer;
all three native downstream targets remain recording RET stubs. Exact native
field writes, callback sequence/arguments, whole fixture/constant pages, return
boundary, stack, nonvolatile integer and XMM6–15 values are checked as in EXP-073.
The separate helper has no stubs and checks result bits, branch, no writes,
constant pages, stack and preserved registers. MXCSR starts at `1F80`; exception
flag fidelity is not claimed. Unicorn 2.1.4 and Capstone 5.0.7 were used.

[Raw results](evidence/EXP-074-angle-conversion-boundary/result.json),
[disassembly](evidence/EXP-074-angle-conversion-boundary/disassembly.txt), binary
extracts and source identities are sealed by the
[manifest](evidence/EXP-074-angle-conversion-boundary/manifest.json).

## Observed boundary behavior

Let `T` be binary32 `2^31 * two pi`, bits `50490FDB`, value 13,493,038,080.
Each adjacent float here is 1024 away. W is the wrapper/writer's stored facing;
H is the independent helper result. All values below are hexadecimal float bits.

| Input | W | H | Conversion interpretation |
|---|---|---|---|
| `50490FDA` (T-1024) | `C0490FDB` | `00000000` | quotient converts to 2147483520 |
| `50490FDB` (T) | `50C90FDB` | `50C90FDB` | positive 2147483648 is invalid; integer indefinite is -2147483648 |
| `50490FDC` (T+1024) | `50C90FDC` | `50C90FDC` | positive overflow |
| `D0490FDA` (-T+1024) | `40490FDB` | `00000000` | quotient converts to -2147483520 |
| `D0490FDB` (-T) | `40490FDB` | `00000000` | **-2147483648 is valid**, although its bits equal integer indefinite |
| `D0490FDC` (-T-1024) | `C47F36F0` | `C4800000` | negative overflow; H is -1024 |
| `50509DC3` (about +1.4e10) | `50CCD6CF` | `50CCD6CF` | positive overflow |
| `D0509DC3` (about -1.4e10) | `CDF1BD00` | `CDF1BD00` | negative overflow |
| `51BA43B7` (about +1e11) | `51D365B2` | `51D365B2` | positive overflow |
| `D1BA43B7` (about -1e11) | `D1A121BC` | `D1A121BC` | negative overflow |

None of these ten inputs passes through unchanged in either routine. In
particular, positive T produces **2T**, whereas negative T produces zero in the
helper and positive pi in the writer. A sign-symmetric magnitude test does not
describe the signed conversion boundary correctly.

For the helper's far path, the supported expression is:

```text
q = binary32(a / two_pi)
k = trunc_to_s32(q), or -2147483648 for invalid conversion
p = binary32(binary32(k) * two_pi)
result = binary32(a - p)
```

When conversion is invalid, `p` is -T. Subtracting -T adds T; it is only absorbed
when the input's binary32 precision makes that addition round away. EXP-073's
+/-1e20 are examples of absorption, not the whole overflow domain. The writer
has the additional sign-biased add/subtract steps documented in EXP-072, which
account for its pi and negative-boundary residuals. No maximal absorption domain
or universal finite-input range is derived here.

## Falsification, implications and reproduction

The private helper mutant replaces its four-byte `SUBSS XMM2,XMM0` at `0033CBE8`
with NOPs. At input T it returns T instead of 2T. It still returns normally,
preserves stack/registers, takes the expected far branch and performs no writes;
the result oracle detects the false pass-through.

The current facing and maths pages must replace their blanket unchanged-input
claims with the actual arithmetic and signed boundary behavior, retaining the
valid +/-1e20 observations. This corrects a reconstruction-relevant formula; it
does not establish the game's live angle distribution, native callback effects
or visual consequences. Peer-owned consumers remain pending until integrated.

Reproduce from the shared repository root using the installed analysis runtime:

```powershell
& '.\Collaboration\Tools\analysis\venv\Scripts\python.exe' 'Database/FFXII TZA/_experiments/evidence/EXP-074-angle-conversion-boundary/check.py'
```
