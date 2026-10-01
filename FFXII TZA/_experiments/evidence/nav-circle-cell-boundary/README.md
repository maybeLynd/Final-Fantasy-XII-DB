# Original circle/cell contact boundaries

Question: does `004690B0` use inclusive contact everywhere, only an expanded bounding rectangle, or inclusive edge bands followed by strict corner tests? Consumers: FABLE navigation §10, OPUS geometry/layout/contracts, FRONTIER's unit-definition carrier. Method **A** established source, input accesses and caller; **B** executed the verified complete 237-byte call-free leaf in disposable Unicorn guests for exact finite tangent and adjacent-binary32 cases. No live setup was needed. This is one package, not ten gameplay experiments.

Certified image SHA256 `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`; source.json and raw.json pin reader, shared role adapter, source, driver, Python, Capstone and Unicorn modules/native DLLs. Retained original237.bin and caller679.bin match the image. All 67 instructions are locally reachable in the existing source-flow check; the final-byte cut fails. Memory roles come from the shared reviewed adapter through the actual preparation/check paths. No raw Capstone access flags are used.

The predicate reads four floats at RCX `+0,+8,+10,+18` and three at RDX `+0,+8,+10`. In the navigation call, `003923CD` calls this predicate; the zero return skips marking at `003923D4`. The cookie call is `00392482 -> 00808C40`. The retained unit-definition carrier wrongly names `003923CD` as that cookie call. Its owner must correct the actual producer/check or generation procedure plus the affected row/history; cause is not established here and the canonical index is not reported regressed.

For finite ordered bounds and nonnegative radius, the source first checks two bands using ordered inclusive comparisons: A in `[minA-r,maxA+r]` with B in `[minB,maxB]`, then A in `[minA,maxA]` with B in `[minB-r,maxB+r]`. Arithmetic follows the shipping ADDSS/SUBSS sequence. If neither succeeds, it computes radius² and four corner distances using the original MULSS/ADDSS order. The first three decisions are **JA**, and the final result is **SETA**: radius² must be strictly greater than the computed corner distance². Replacing this with a generic inclusive nearest-point distance rule would change boundary behavior. These formulas describe the source's branches, not exact real-number equivalence for all floats.

Each fresh guest initialized RCX/RDX, a valid stack/return sentinel, EFLAGS, XMM0–5 and **MXCSR 1F80** (round nearest, exceptions masked, DAZ/FTZ clear). Rectangle bounds were 0..10 on both axes. Unread argument bytes were poisoned. No callback or stub is used; the entire original leaf executes to RET. A 128-instruction budget, positive inside and distant negative controls precede the boundary batch. Read hooks restrict addresses to the arguments and return slot; unexpected execution/access/write or incomplete return invalidates the result. Every raw case was saved before its assertions.

| Injected case | Original EAX |
|---|---:|
| Inside (5,5), radius5 | 1 |
| Outside (-6,5), radius5 | 0 |
| Edge tangent (-5,5), radius5 | 1 |
| Four corner tangencies (-3,-4), (-3,14), (13,-4), (13,14), radius5 | 0 each |
| First corner, radius bits40A00001 (next above5) | 1 |
| First corner, radius bits409FFFFF (next below5) | 0 |
| Private first JA->JAE, first corner/radius5 | 1 |

At edge contact the compared bits are both C0A00000. Each nearest-corner comparison at exact3-4-5 contact has operands41C80000/41C80000 (25/25). The next-above radius produces41C80003 against41C80000; the next-below produces41C7FFFE. The labelled JA->JAE bytes are never deployed and fail the shipping identity binding. check.py rederives source/flow/caller/layout, validates every raw path/read/input/return and performs a bounded host replay for these selected values. That replay validates the instrument; it is not independent proof of native game behavior or a general replacement implementation. Raw COMISS operands use numeric hex for register low-lane bits and byte-order hex for memory operands; the reducer explicitly handles both representations.

All captured paths return to the sentinel with RSP advanced by8; arguments and stack bytes are unchanged, and no memory writes occur. Provider/module hashes match before/after capture. The process ends with no attached instrumentation. PC remains OFF; no FF12, save/config/reference or peer consumer writes. S19's spent allowance and unapproved extension are preserved.

Limits: injected argument/state and emulator execution; actual FF12 bounds/radii/MXCSR, caller occurrence, initialization, scene presentation, ownership, scheduling, atomicity and complete rasterizer effects remain unobserved. The observed MXCSR is emulator state, not validation of native CPU exception/status flags. No negative radius, NaN/unmasked exception, degenerate/inverted rectangle, overflow/underflow or all malformed-input safety conclusion is awarded. Preserve floating-point order and the tested domain. Independent owner/reviewer acceptance is required before canonical incorporation; a manifest or checker pass alone is insufficient.

Reproduce the reduction, without recapturing, from repo root:

```
Collaboration/Tools/analysis/venv/Scripts/python.exe "Database/FFXII TZA/_experiments/evidence/nav-circle-cell-boundary/check.py"
```

Player view: FF12's original overlap helper accepts a circle touching a cell along a side but rejects the tested exact corner touches. This defines a precise navigation rule without claiming a live player-facing collision result. The full L1+L2 database goal is still NOT_MET.
