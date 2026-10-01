# A NaN bound need not reject all four corners

The actual OPUSd87bb8501 `NavGridParams.cellBitsetArray` consumer says “a NaN fails every test.” The original predicate uses different operands for its four alternative corners. **A source plus B bounded original-code execution** supplies a counterexample to a universal reading of that clause.

Original237-byte `004690B0` (certified image SHA256 `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`) is the immutable55 parent from commit `9998e98b8ae823f8fc703bccfe23118f1de8b5e9`. We reuse that actual runner, retaining its original source and explicit small adaptation: supply rectangle bits, and observe flags at branch/SETA boundaries. Code is unchanged in every case. Five fresh isolated guests, injected Win64 argument/stack/register state, masked round-nearest MXCSR1F80,128-step limit, no callbacks/stubs/memory writes.

| Rectangle / circle | Return |
|---|---|
| Rectangle0..10; center13,14; radius6 | 1 |
| Same; radius5, exact opposite-corner contact | 0 |
| Same radius6; **minA=quiet NaN7FC00000** | **1** |
| Finite rectangle/radius6; centerA=quiet NaN | 0 |
| Finite rectangle/center; radius=quiet NaN | 0 |

For the malformed minA case, both band tests and the two minA-based corners fail. Their completed unordered COMISS outcomes carry CF/PF/ZF=1. The maxA/minB corner is too far away. The final maxA/maxB corner uses only finite bounds: radius²=36 (`42100000`), distance²=25 (`41C80000`). Original `00469196 COMISS` followed by `00469199 SETA` returns1. Thus one NaN bound does not contaminate every alternative. Source paths, operand values, branch flags, actual return and unchanged argument/stack bytes are retained and independently reduced. The center/radius negative controls show this is operand-specific, not an observer that accepts everything.

The host source/value/path replay is an instrument check; original guest execution is the B evidence. The checker does not rerun guests. A private `--fault-universal-nan-reject` reducer mutation forces the broad rule and must fail this actual counterexample. This is not an additional FF12 execution. Required independent acceptance remains separate.

Correction goes to OPUS's actual consumer/model/domain guard and FABLE's actual affected prose if any. Add this precise bound-NaN control and distinguish center/radius from individual malformed rectangle operands. Preserve valid finite contact/corner rules and their source instruction order. Correct a broader canonical statement additively; published55 and57 remain immutable. OPUS's existing model may already compute this path correctly—the coverage and semantic postcondition must prevent the broader prose from passing again, not merely change a count label.

Limits: quiet NaN in minA, one specific finite opposite-corner case and injected guest state. No all-NaN payloads, all malformed rectangles, negative-radius safety, native COMISS status/exception effects, unmasked continuation, actual FF12 MXCSR or normal malformed gameplay reachability. Semantic native interpretation is conditional on comparisons completing with suitable masked state. EXP57 already demonstrates an emulator precision-status omission; unchanged guest MXCSR is not proof of native absence of exceptions. Screenshots/presentation/live scene/init/scheduling are not tested here.

Exact parent/code/runner/reader/tool/provider identities and actual OPUS source/field preimage are preserved. Raw case records precede acceptance checks. Fresh guest cleanup completes RET/stack+8 with no writes and argument bytes unchanged; original reference is read-only and matched. PC control remains off, no FF12 process/save/config/peer writes. S19's spent allowance/unapproved extension persists; L1+L2 database NOT_MET, L3 later.

First reduction was **INVALID_REDUCTION_ROW_HASH** before path checks/result creation: the producer recorded the UTF8/LF normalized field-row checksum, while Windows `write_text` retained CRLF bytes and the first checker hashed those physical bytes. The old checker and exact hashes/failure phase are preserved under `retained/invalid-row-hash-normalization`. The actual default checker now hashes normalized row text for that declared field; the manifest separately protects physical bytes. Raw capture/driver and five guest observations remain unchanged; no recapture. Learn the distinction before retrying a retained-text checksum, rather than treating the mismatch as original-code behavior.

Reproduce the read-only retained reduction from repo root:

```
Collaboration/Tools/analysis/venv/Scripts/python.exe "Database/FFXII TZA/_experiments/evidence/nav-nan-operand-domain/check.py"
```

Player view: a broken boundary number can disable some tests while another valid corner still accepts the object. “Any bad number makes the test fail” is too broad. This does not show that normal gameplay supplies broken boundaries.
