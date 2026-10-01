# Original modular row-address equality: special row113hex only

QUESTION: can another action row alias row`0x113` (275) through the original
32-bit address arithmetic, and does the intermediate normalization change the
producer's row pointer? Method A source/invariant proof. OPUS consumes the exact
selector/address/ABI preconditions; FABLE consumes the remaining OV42/OV21
natural type-admission question. No game/native run is needed for this claim.

Inputs: retained class20 caller prefix`0030CBFC..0030CD9E`, retained full
selector`00309230` and`00306BD0` prefix frome4e9fc11, plus new full normalization
body`0030CE10..0030CF3F`. Parent manifests/member bytes and the actual parent
proof01 exit/exception/driver/output are checked. Every original new/retained
instruction matches EXE
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
Reviewed shared access-role adapter is actually used/re-decoded; no raw access
flags, new nine-table census or claimed parent independent acceptance.

## Exact invariant

Let `B` be the stable low32 resolver return, `i` the original u16 row and
`s` the stable u16 stride, with **1 <= s <= 65535**. `0030CC76/7A` load WORDs,
`0030CC7E/81` form `P = (B + i*s) mod2^32`. The selector forms
`C = (B + 275*s) mod2^32` and compares against the full64-bit zero-extendedP.

The original widths give:

```
0 <= i*s <= 65535^2 = 4294836225 < 2^32
-18022125 <= (i-275)*s <= 4276814100 < 2^32
```

The signed difference is also strictly greater than`-2^32`. Thus equality
modulo`2^32` forces `(i-275)*s = 0`, and nonzero s forces **i = 275**. The same
product bound proves injectivity between any two u16 rows at a fixed s.
ArbitraryB cancels, even whenB+product wraps; no no-addition-wrap premise.

`0030CE59..7F` subtractsB modulo32, clearsEDX and unsigned-divides bys. Because
i*s itself does not wrap, subtraction recoversi*s, DIV recoversi/remainder0,
and multiply/add recomposesP exactly. Original`0030CF07..0D` forwards the
**entry** pointerRBP to`00306BD0`, whose retained prefix passes it to`00309230`.
Normalization neither clamps the row nor turns another validu16 row into275.

These deductions require stable resolver/context/stride across the distinct
calls/reads, ordinaryABI/nonvolatile preservation and accessible memory/no
interference. Their natural truth is **not** proved. The caller prefix is not
a full caller/interpreter/lifetime closure. MathematicalB=0/i=0 boundary
witnesses are algebra, not calls passing the caller's nonzero-pointer gate.

Five mathematical countermodels demonstrate why scope matters: zero stride;
row wider thanu16; stride wider thanu16; changed base; changed stride. Zero
stride also violates original DIV's divisor precondition. None was executed,
injected into FF12 or observed as a shipped bad state. Twenty-four algebraic
boundary witnesses cover wrapping additions/extreme widths; the interval proof,
not their count, establishes the invariant.

## Controls and reproduction

`result-01.json`, full source, parent inputs and terminal capture01/proof01
receipts preserve exact identity and raw output. Three actual proof CLI controls
require exact refusal/empty stdout/absent result and the valid positive: failed
capture, missing required parent proof status, same-size/count coherent
`XOR EDX,EDX -> OR EDX,EDX` change rejected against shipping bytes. No unrelated
exception/partial/zero-case run can pass. Old parent controls/runs are reused
as provenance, not counted as new runs.

Run project Python from repository root with
`prove.py FRESH_JSON --src PUBLISHED_PACKET_DIRECTORY`.
Shared source_pins are emitted by the actual producer; the **actual** publication
annotation function is checked before freezing/claiming publication. This
precondition avoids the previous interface omission without weakening its
guard. Published inputs/results are immutable; reviewers use fresh outputs.

## Effect on the frontier

The proposed “another WORD row may alias the special table branch solely due to
32-bit wrap” explanation is refuted under the explicit stable-state premises.
One more implementation proposition is answered without live gameplay. The
remaining equal-branch actor-type question narrows to row275. Natural context
stability, initializedactor type27..39 for that row, external helper effects,
other producers/branches and actual rejection/consequence remain open. This
does not close wholeOV42/21 or independently accept the previous packet.

No game/PC/native/instrument/save/config/reference/peer-process changes. All
our finite helpers terminate. Runtime restoration is vacuous; no state touched.
Producer validity, independent acceptance and canonical consumption remain
separate; required SPEC/OPUS/FABLE review/incorporation follows publication.
