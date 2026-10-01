# Facing wrap: exact antipode defeats universal idempotence

The current facing contract says the second wrap is “idempotent, so harmless” (§6) and repeats that justification later. Question: does the exact signed-pi endpoint stay fixed, or alternate sign on repeated wrapping? Consumers are FABLE's facing/steering semantic contract and ED-3 answer, with OPUS's heading domains/representation and SPEC independent review.

**Method A suffices.** Verified shipping source at `0026C090` (129 bytes) chooses a bias with `COMISS` at `0026C096` and `JB` at `0026C09C`. The negative path loads `00915620`, the other path `01CEBC50`; both use `01CEBC78` for division and multiplication. Actual reference constants are `C0490FDB` (negative pi), `40490FDB` (positive pi), `40C90FDB` (two pi). The original `ADDSS`, truncating `CVTTSS2SI`, conversion, multiplication and two subtractions are bound by exact bytes and operand/branch targets. The kind-3 store is `0026C0F9`, record `+0x34`.

Executable SHA-256: `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`. The source, constants, reader identity, instruction listing, current contract/ledger/differential-producer preimages and tool identity are retained. **No FF12, original-code, native or emulator execution was performed for this package.** Existing DY-1 sweep counts remain historical, not new tests.

| Source-calculated input | First wrap | Second wrap | Fixed after first? |
|---|---|---|---|
| `40490FDB` (+pi) | `C0490FDB` (-pi) | `40490FDB` (+pi) | No |
| `C0490FDB` (-pi) | `40490FDB` (+pi) | `C0490FDB` (-pi) | No |
| `00000000` (+zero) | `00000000` | `00000000` | Yes |

For positive pi the biased sum is exactly positive two-pi, the quotient exactly 1, the remainder exactly zero and the result negative pi. The negative path is its exact sign mirror. Every selected noninteger step is exactly representable; the checker verifies rational values against the stored binary32 values at each step under the stated nearest/masked arithmetic boundary. This is source reasoning with a host calculation, not a reconstructed fixture promoted to original execution.

A **labelled private source/calculation intervention** changes the negative bias load's RIP target to positive pi. Its negative-pi result is then a fixed negative-pi value. The original source-binding check rejects those bytes. That control demonstrates why the real negative bias matters; no changed FF12 code was executed. Positive zero provides an ordinary fixed-point control.

Established: the universal idempotence claim is false for the selected exact antipodes. Removing a wrap on the basis of that claim can change the stored float sign at the boundary. The two values represent the same geometric direction; this package does **not** claim a visible difference or a downstream turn consequence. Those require the relevant branch/state/caller evidence. General rounding domains, native CPU exception/status parity, unmasked comparisons, actual game MXCSR and reachable scene input are unproved here.

Required consumer change: remove/qualify the universal idempotence justification in the facing contract and any ED-3 summary; preserve the actual number/order of source wraps and the signed endpoint behavior. The source dispatch identity remains answered. Independent review should accept/narrow/reject this bounded counterexample. Existing differential tests cover individual wrappers; this package does not allege their implementation is wrong or demand another broad sweep. Any assertion of repeated-wrap equivalence must exclude the demonstrated endpoints or preserve the explicit original calls.

Cleanup: read-only reference and peer inputs, disposable host arithmetic only, PC control off, no game/process/save/configuration changes. Published inputs stay immutable and canonical owner files are untouched. S19 extra menu recovery remains unapproved. Full L1+L2 and independent/final acceptance remain NOT_MET.

Learned rule: stop testing universal idempotence once a bound counterexample exists. Do not repeat the DY-1 broad sweep or these endpoint calculations to increase counts. A later proposal must name a different unresolved boundary, actual caller or observable consequence.
