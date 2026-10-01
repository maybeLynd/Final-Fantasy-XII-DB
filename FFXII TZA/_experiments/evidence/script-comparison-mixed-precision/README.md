# Typed ScriptVM comparison precision — 78

QUESTION: does changing one operand from integer to float preserve the comparison
of 16,777,217 against 16,777,216, and does supplied rounding mode matter?
Major system ScriptVM; consumers FABLE semantic, OPUS contracts, DATA canonical.

METHOD A: full original comparator `0025D740`, 413 bytes, and prior72 isolated
original conversion observations at `c4cbbfb8abe0bd5e73daf47d92c9378923292c29`.
No new guest/native/live run. Competing all-float, always-nearest and reversed
operand interpretations are rejected by focused source/retained-bit controls.

REFERENCE: shipping EXE SHA256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`, imagebase
`00120000`. Raw source rows, exact bytes, certified reader, shared access-role
adapter and Python/Capstone providers are pinned in `raw.json` and `retained/`.
Actual capture invokes reviewed op_kind/written; reducer checks store/read/LEA
and a labelled private memory RMW instruction. No raw access-flag bypass.

SOURCE: with supplied depth2, top tag and preceding tag are read before dispatch.
Only both tag1 select signed integer CMP ESI,EBP. Top payload becomes EBP or XMM7;
preceding payload ESI or XMM6. Mixed tag1 uses MOVD/CVTDQ2PS, tag2 MOVSS. The
float comparisons are UCOMISS XMM6,XMM7 and COMISS XMM7,XMM6, so the three-way
return describes preceding/lower versus top/popped operand. Depth transitions
are source facts here, not newly observed effects.

CONDITIONAL RESULTS for valid depth2/tag1-or2, finite values, supplied masked RC:

| lower versus top | nearest `1F80` | toward +infinity `5F80` |
|---|---:|---:|
| int 16777217 versus int 16777216 | +1 | +1 |
| int 16777217 versus float 16777216 | 0 | +1 |
| float 16777216 versus int 16777217 | 0 | -1 |
| int 123 versus float 124 | -1 | -1 |

The boundary prediction uses prior72's actual original CVTDQ2PS values
`4B800000` and `4B800001` (16777216 and16777218). Prior72's initial raw labels
remain wrong; its additive correction is source/invocation-derived and supported
by post-stage RC, not a fresh initial-state measurement. All original files
remain immutable, retained identity/correction travels with the composed result.
The exact-small-value control is a source calculation, not an additional run.

IMPLICATION: a faithful specification needs the signed integer fast path and
mixed promotion under supplied MXCSR. An all-float or always-nearest replacement
changes this conditional behavior. `result.json` separates source facts from
predictions; raw-default and three rejected alternatives are reproducible.

LIMITS: no actual mixed comparator execution, native status/unmasked exceptions,
game RC, authored values, normal caller reachability, invalid tags/underflow/
fault callbacks, interpreter boolean push, initialization or live behavior.
Prior77's masked NaN guests do not prove mixed/int paths. Consumer incorporation
and independent acceptance remain pending. PC control OFF, no FF12 process,
instrumentation or save/config/reference changes; disposable guest cleanup
belongs to retained72's receipt, not a new cleanup claim. S19 spent/unapproved
extension persists. Full L1+L2 database goal remains ACTIVE / NOT_MET.
