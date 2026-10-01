---
experiment: EXP-049
title: renewing a handle and requesting party-focus refresh
status: COMPLETE - bounded isolated original-code evidence
contract: ../04-Actor-Entity/CONTRACT-field-runtime-pass.md
evidence_class: isolated original-code
method: B - isolated original-code execution
live_game: false
execution_scope: Ten original bodies with synthetic registry and pool; stop before native refresh, with expected null-input fault separate.
contract_coverage: Resolver dependency 003588B0 inside renewal and focus selection; stops before native refresh and never executes the field pass.
tool: evidence/EXP-049-handle-renewal-focus/check.py
date_designed: 2026-09-11
date_run: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-049: renewing a handle and requesting party-focus refresh

**Result:** original `003220E0` encodes the old handle, advances the discriminator,
encodes the new handle, and compares the old value with the currently selected
unit's cached handle. A match writes a preferred selector as a **dword** and reaches
the native focus-refresh call. Seven controlled boundaries passed. ASTRA, 2026-09-11.

## Question and authority

[EXP-047](EXP-047-attacker-mask-reset.md) stopped at this delegate;
[EXP-048](EXP-048-handle-discriminator-advance.md) established the original
advance/encode/resolve chain. This experiment asks how renewal uses that chain
and when it requests party-focus refresh.

[check.py](evidence/EXP-049-handle-renewal-focus/check.py) checks the certified
executable hash and extracts ten original bodies: the six from EXP-048, the complete
176-byte renewal function, the 117-byte focus lookup at `00327150`, and its original
unit-pool count/index helpers `00236850` and `00236820`. Exact bytes and
[disassembly](evidence/EXP-049-handle-renewal-focus/disassembly.txt) are retained.
No call is stubbed. The final native refresh at `00326500` is an explicit stop
boundary and is never executed.

## Original sequence

1. Encode the input actor's old handle at `003220FD`.
2. Call the discriminator incrementer at `00322107`.
3. Encode the new handle at `00322118`.
4. Call the original focus lookup at `0032211F`; compare old handle against returned
   unit+8 (or zero when lookup is null).
5. If unequal, return the new handle. If equal, resolve the **new** handle with the
   battle gate and read its unit's stats+4 byte when available; otherwise use FFh.
6. At `00322173`, write that zero-extended selector to **four bytes** at
   `*(02EBF190)+5AA4h`, then call `00326500` at `00322179`.

The original focus lookup reads the preferred selector's low byte, rejects values
above 27h, computes `state+8+selector*1C8h`, and searches the unit pool for a unit
whose stats pointer equals that record. This lookup remains original code in the
fixture, including its count and index helpers.

## Controls and observed boundaries

Each case starts with a fresh emulator, stable synthetic actor registry, one-unit
pool and a patterned battle-state block. Initial actor discriminator is 7; renewal
sets it to 8. The selector bytes start `03 A5 A5 A5`, so a byte-only store cannot
masquerade as the original dword write. The stats record's definition selector is 3.

| Case | Outcome | Selector bytes after |
|---|---|---|
| Focus cached handle equals old encoding | stop before refresh | `03 00 00 00` |
| Focus cached handle differs | normal return of new handle | `03 A5 A5 A5` |
| No focus (selector FFh) | normal return of new handle | `FF A5 A5 A5` |
| Match, battle gate off | stop before refresh | `FF 00 00 00` |
| Match, registry manager disabled | stop before refresh | `FF 00 00 00` |
| Match, resolved actor has no unit | stop before refresh | `FF 00 00 00` |
| Null input actor | unmapped read at incrementer `002659D0` | no non-stack writes |

The null input reaches an unconditional incrementer call despite null checks
surrounding encoding. It is not a successful no-op. This is an isolated unmapped
null-read result, not a live-game crash or a claim that valid callers pass null.

For nonnull cases the test asserts exact call order: encode, advance, encode,
focus lookup, then refresh boundary only on match. It checks the complete actor,
unit and battle-state memory images and exact non-stack write addresses/widths.
The unit's cached handle remains unchanged at these boundaries: the outer wrapper
in EXP-047 stores the new return value afterward. Mismatch cases reach RET with
RSP+8 and the new handle in RAX. Match cases stop before the refresh, so their
full-operation return and downstream memory effects are not credited.

A private mutant changes only the selector store from ECX to CL. The low byte is
still right, but three stale bytes remain and the footprint becomes one byte;
both checks detect it. Original bytes remain unchanged.
[Results](evidence/EXP-049-handle-renewal-focus/result.json) retain instruction
traces, call order, writes and selector bytes. The
[manifest](evidence/EXP-049-handle-renewal-focus/manifest.json) seals this package.

## Integration and limits

Return this evidence to FABLE for renewal/focus semantics and OPUS for the observed
four-byte preferred-selector writer. A byte reader alone does not establish that
the field has only byte-width stores. The full native refresh, caller lifecycle,
live focus changes, concurrency and object lifetime remain untested. Fixtures
are synthetic and no game process was opened. Run `check.py` with the existing
Windows Python and Unicorn environment.
