---
experiment: EXP-072
title: original facing writer boundary and callback controls
status: COMPLETE - bounded isolated original-code evidence
contract: none - Facing-and-steering lists different entry points; writer 002E5E10 is not an executed substitute for its 0026B5A0/0026C090 or unread 002E5FB0 paths.
evidence_class: isolated original-code
method: B - isolated original-code execution
live_game: false
execution_scope: Complete original facing writer with three recording callback stubs and controlled MXCSR; no native transforms or live movement.
contract_coverage: No matching existing contract at recovery; this disposition does not close a database knowledge or contract gap.
tool: evidence/EXP-072-facing-writer-controls/check.py
date_designed: 2026-09-11
date_run: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-072: original facing writer boundary and callback controls

**Result:** 25 original-code controls pass; a private signed-handle mutation is
detected. ASTRA, 2026-09-11. One first-run EAX oracle error is preserved and
corrected. This is isolated execution with three recording callback stubs, not
live movement or native transform execution.

## Question and evidence

The [K-6 facing-writer section](../06-Movement-And-Navigation/heading-speed-to-position-delta.md)
describes `002E5E10` as a three-argument writer whose output cannot escape
`[-pi, pi]`, with three or four transform calls on every change. Test those
boundaries, field writes, argument sources and conditional callback sequence.

The [checker](evidence/EXP-072-facing-writer-controls/check.py) verifies the full
reference EXE SHA-256, extracts all 374 bytes of `002E5E10` and its three original
constants, then executes that original body in Unicorn. Actor, movement state,
controller and node occupy separate synthetic pages with sentinel fill. MXCSR
starts at `1F80` (round to nearest, masked exceptions, no FTZ/DAZ).

`003DA850`, `003DAF20` and `003EC260` are RET stubs recording argument values and
both field values at entry. They overwrite all volatile integer and XMM0–5
registers. They perform no native transform, animation or invalidation work.
Every control compares the exact interleaved field-write/callback sequence,
whole fixture and constant pages, STOP return, RSP+8, all eight nonvolatile
integer registers and full XMM6–15 values. Reads, visited instruction addresses,
EAX, MXCSR and arithmetic intermediates are retained in
[raw results](evidence/EXP-072-facing-writer-controls/result.json).

Full [disassembly](evidence/EXP-072-facing-writer-controls/disassembly.txt),
binary extracts and exact source identities are sealed by the
[manifest](evidence/EXP-072-facing-writer-controls/manifest.json).

To reproduce from the shared repository root, use the existing analysis Python
and installed offline libraries (Unicorn 2.1.4, Capstone 5.0.7):

```powershell
& '.\Collaboration\Tools\analysis\venv\Scripts\python.exe' 'Database/FFXII TZA/_experiments/evidence/EXP-072-facing-writer-controls/check.py'
```

This regenerates current results and extracts in the evidence directory; the
preserved first-run files remain separate historical evidence.

## Argument and state contract

The observed Windows x64 input positions are RCX = actor, XMM1 low dword = angle,
XMM2 low dword = auxiliary float bits, and R9D = a fourth integer argument.
The fixture deliberately puts unrelated `DEADBEEF` in R8D. The body saves
XMM2 into XMM8 and R9D into R14D. Treating the third argument as an integer
register argument loses its actual source; the fourth argument is used below.

The body loads actor+B8 as the movement-state pointer and actor+C0 as the
controller. **A null controller skips both stores and all callbacks.** This
control preserves the sentinel field bits and returns normally. A null actor
is not tested or declared safe; the body still dereferences RCX+B8 at `002E5E55`.

For a present controller, native stores occur in this order:

| Instruction | Destination | Data |
|---|---|---|
| `002E5E88` | state+AC | XMM2 input's low 32 bits |
| `002E5EBE` | state+A8 | computed facing bits |

Both stores precede every callback. All untouched fixture bytes remain equal
to their initial values under these stubs.

## Exact arithmetic and counterexamples

Constants are positive pi `40490FDB` at `01CEBC50`, negative pi `C0490FDB` at
`00915620`, and two pi `40C90FDB` at `01CEBC78`. COMISS/JB chooses negative bias
for negative and unordered input, positive bias otherwise. Each addition,
division, integer-to-float conversion, multiplication and subtraction uses the
native binary32 operation; CVTTSS2SI truncates to signed 32-bit integer and
produces integer indefinite `80000000` for the tested invalid conversions.

The oracle rounds each operation separately. These are observed output bits:

| Input | Stored facing | Meaning |
|---|---|---|
| `3F800000` (+1) | `3F800002` | already-small finite input can change |
| `BF800000` (-1) | `BF800002` | corresponding negative rounding |
| `00000000`, `80000000` | `00000000` | both zero signs become positive zero |
| `40490FDA` | `40490FD9` | immediately below positive pi |
| `40490FDB` | `C0490FDB` | positive pi becomes negative pi |
| `40490FDC` | `C0490FD9` | immediately above positive pi |
| `C0490FDA` | `C0490FD9` | immediately inside negative pi |
| `C0490FDB` | `40490FDB` | negative pi becomes positive pi |
| `C0490FDC` | `40490FD9` | immediately outside negative pi |
| `40C90FDB` | `B4800000` | positive two pi leaves a small negative residual |
| `C0C90FDB` | `34800000` | negative two pi leaves a small positive residual |
| `60AD78EC`, `E0AD78EC` (approximately +/-1e20) | unchanged | finite outputs outside the claimed range |
| `7F800000`, `FF800000` | unchanged | infinities are stored |
| `7FC12345` | unchanged | this quiet NaN payload is stored |

Thus the universal range guarantee is false even for finite input. The tested
small finite cases remain in the pi interval, but this experiment does not
derive the largest safe interval or establish all floating-point inputs. It
does not execute `0033CB70`, so equivalence to that helper remains outside the
evidence. Reapplying the arithmetic to either exact pi endpoint would change
its sign again; the `002E5F90` wrapper itself is not executed here.

## Callback order and arguments

For a present controller, the `003DA850` calls receive RCX target and XMM1 low
dword equal to the computed angle. The order is:

1. state+50, always within this non-null-controller path.
2. state+70, then state+60, unless actor+0D has bit 20 set.
3. node+F0, only when the reread actor+C0 and its +138 node are non-null.

The tested paths therefore have **one to four** calls to this target; the
null-controller path has none. An unrelated flag 40 does not suppress calls.
When a node exists, `003DAF20` follows its transform call, receiving RCX = node,
EDX = zero-extended byte state+104, R8D = byte state+105, R9D = byte state+106.
The distinguishing bytes 12, 80 and FF arrive as 18, 128 and 255.

Finally, the initially saved controller's first dword is compared with
`FFFFFFFF`. That sentinel skips `003EC260`. Otherwise its arguments are:

| Position | Value |
|---|---|
| ECX | **zero-extended** low word of controller's first dword |
| XMM1 low dword | original auxiliary float bits |
| XMM2 low dword | computed angle bits |
| XMM3 low dword | positive zero |
| fifth argument, callee RSP+28 | fourth input integer != 0, as a dword |

Handle `0000FFFF` therefore passes 65535, not -1. `12348000` passes 32768.
Fourth-input controls 0, 2 and FFFFFFFF distinguish false from nonzero; the
17.25 auxiliary input is forwarded separately from the angle. No controller
pointer mutation occurs in these controls; the difference between saved and
reread pointers is a static observation, not a tested lifetime guarantee.

EAX is recorded as machine state, not a declared semantic return. It follows
the last stub in most controls; the no-node/sentinel path retains the controller
pointer's low dword after the reload at `002E5EE9`. This caused the initial
oracle error, preserved in [failed setup](evidence/EXP-072-facing-writer-controls/failed-setup.txt),
[first source](evidence/EXP-072-facing-writer-controls/failed-first-check.py) and
[first results](evidence/EXP-072-facing-writer-controls/failed-first-result.json).
All first-run event/page/return-boundary/preservation checks passed; only that
EAX expectation failed. Correcting the oracle changed no native bytes.

## Falsification and limits

The private mutant changes `0F B7 0F` at `002E5F3F` (MOVZX word) to `0F BF 0F`
(MOVSX word). It still returns normally with matching pages, EAX, stack and
nonvolatile registers, but the callback argument becomes FFFFFFFF instead of
0000FFFF. The exact event oracle detects the discrepancy.

This evidence requires correction of K-6's unconditional store/call wording,
universal range claim, integer auxiliary signature and signed short callback
argument. The broader writer census, ownership, relation between facing and
travel direction, native callback effects, live input distribution, scheduling
and movement parity are not validated here. No game process was launched or
attached, and the existing runtime pause remains in force.
