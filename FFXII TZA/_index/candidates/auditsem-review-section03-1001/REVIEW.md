# SECTION-03 reward bindings: independent review (SWE2-AUDIT-SEM for OPUS)

| Field | Value |
|---|---|
| **request** | OPUS-REQ-AUDITSEM-SECTION03-REVIEW-1001 (stands in for FABLE-REQ-AUDITSPEC-SECTION03-REVIEW-0930 while FABLE is inactive; user-authorized 2026-10-01) |
| **package** | `_experiments/evidence/continuation-section03-reward-bindings/` (overlay merged at 21f25545b; owner review 2ff93a3ff) |
| **reviewer** | SWE2-AUDIT-SEM, Claude session for OPUS; independent of the FABLE session that applied the owner dispositions (880134086, 1d7f46253) |
| **register row** | GR-16 |
| **verdict** | ACCEPT-WITH-NARROWING: every sampled claim holds against the shipping bytes, and run_review.py reproduces bit-identically; the narrowing is N1 (the reproduction runs only against the pinned pre-image of one historical checker) |
| **checker** | `sec03_sem.py` with `sec03_sem.out`: 68 PASS, FAILS 0 |
| **evidence class** | NATIVE/STATIC (own PE, .pdata and Capstone decode of the pinned EXE) plus the package's own native synthetic fixture rerun; no live game |

## What was inspected (SWE2-AUDIT-SEM for OPUS)

- The shipping EXE `Tools/work/exe/FFXII_TZA.exe`, SHA-256 `73461d08...d89721f8`, equal to the pin.
- Ten of the 24 pinned bodies, spread over the manifest (indices 0, 1, 15, 16, 18, 19, 20, 21, 22, 23):
  `002F8BB0` EXP computer, `002F90C0` LP computer, `00264150` LP global gate, `002367A0` stats selector,
  `0031B810` roster selector, `0023A570` kind-one installer, `0020E600` address decoder, `00312280` defeat
  caller, `00254EE0` gil setter, `00469E80` gil notifier.
- The producer's file offsets and disassembly were not used as inputs. The checker parses the PE section
  table and `.pdata` itself, decodes with Capstone 5.0.7 and only afterwards compares its offsets and
  hashes with `original_body_manifest.json`.
- The three pages that carry the pending marker (`what-happens-when-an-enemy-dies.md`,
  `experience-and-license-point-award.md`, `how-experience-is-computed-and-divided.md`) and the notifier
  paragraph of `CONTRACT-defeat-rewards-sequence.md`, read against the decode. They agree with it.

## Re-derived claims (SWE2-AUDIT-SEM for OPUS)

| Claim | Sites read | Result |
|---|---|---|
| R03-1 NULL does not bypass the EXP divisor | `002F8BCF`/`002F8BD2` NULL jumps to subject validation; `002F8C45` and `002F8D24` skip designation and modifiers; shared path walks four slots (`cmp ebx, 4`) through `0031B810`; `cdq; idiv ebp` at `002F8D1C` | holds |
| R03-1 caller passes NULL to both computers | `xor ecx, ecx` at `003124BC` before `call 002F8BB0` (`003124BE`) and at `003124C6` before `call 002F90C0` (`003124CA`) | holds |
| R03-2 LP has its own gate and no owner search or divisor | `002F90D0` calls `00264150` (movsx of a global byte) and rejects nonzero before any dereference (first at `002F90E2`); the gate is the only call; no divide | holds |
| R03-2 LP recipient ids | `002F90EB`-`002F90F5`: 0..6, 0x1A, or 0x28 and above | holds |
| R03-3 id 0x1A is a recipient but not a divisor member | `002F8CD8` excludes 0x1A from `inc ebp` | holds |
| R03-3 0xFF sentinel matches 0xFFFF | `002367E3`-`002367EE` (`cmp edi, 0xff`; `mov ecx, 0xffff`; `cmovne ecx, edi`); `0031B82B` feeds 0xFF when its descriptor test fails | holds; shipped reachability stays open as the package says |
| R03-4 EXP DWORD rows at +0x34, LP unsigned BYTE rows at +0x2F | four `dword ptr [..+0x34]` reads in the EXP body; two `movzx ecx, byte ptr [rax+0x2f]` in the LP body | holds |
| R03-4 zero roster returns 0 before row reads; doubling before zeroing | `002F8CEC`/`002F8CEE`; `add esi, esi` (`002F8D34`) precedes `xor esi, esi` (`002F8D40`) | holds |
| R03-5/R03-6 installer row pointers | `0023A994`-`0023A9A5` and `0023A9DB`-`0023A9F4`: u16 stride at descriptor+8, u16 selector at row+0x22/+0x24, 32-bit `imul`/`add`, QWORD store to +0xE70/+0xE78; absent descriptor and decoded zero both store 0 | holds |
| R03-6 decoder | `0020E600`: `mov eax, ecx` (zero-extend), `add rax, [rip+...]`, `ret` | holds |
| R03-7 gil floor, setter meter and cap | `00312553`-`00312566`: `cmovns ebp, edx` floors old+award at 0 (ebp zeroed at `003122A9`), setter, then `sub ebp, ebx` to the notifier; `00254EF1` meters requested minus current; clamp 0..0x5F5E0FF; store at `00254F1F` | holds; the worked examples (stored gain 4; notifier -5) follow under the package's stated no-intervening-change assumption (INFERRED arithmetic, not executed) |
| R03-8 notifier payload | `sub rsp, 0x58` then six QWORD clears at rsp+0x20..+0x48; `[rsp+0x30]` = payload+0x10 with `r8 = r11-0x38` = rsp+0x20; `jle` skips non-positive; event 0x26 | holds |

## Controls (SWE2-AUDIT-SEM for OPUS)

Each pattern check has a negative control in the same checker, so a pass is not a property of the filter:
a one-byte shifted range fails the body hash; no `.pdata` root exists mid-body; the LP body has no divide;
a private copy of the LP body with one `movzx` turned into `movsx` loses the unsigned match; the EXP body
has no 0xFFFF literal; a non-site store in the installer is not a row store; a private notifier copy with
one store removed counts five. The EXP body itself serves as the positive control for helper calls that
the LP body lacks.

## Rerun of run_review.py (SWE2-AUDIT-SEM for OPUS)

- Host: WSL Ubuntu-22.04, Python 3.10.12, GCC 11.4.0 (the producer used Debian GCC 14.2.0). Script:
  `Tools/work/SWE2-AUDIT-SEM/sec03/rerun.sh`, output `Tools/work/SWE2-AUDIT-SEM/sec03/rerun/`.
- Against the live tree the run stops at input pinning: `input changed:
  _experiments/evidence/retained-reward-bindings/check.py` (11,532 bytes; pinned 11,332).
- Against a pinned-input tree (`sec03/pindb/`: the fifteen inputs copied from the live tree, with that one
  file taken from `13a61b94b~1`, whose SHA-256 equals the pin) the run exits 0: 24 bodies, 88 spans,
  10 corrupted-record controls, historical replay matches, 71/71 native controls, identical repeat,
  6 of 6 mutants fail their intended assertion. Fourteen of fifteen result files are equal to the shipped
  results; only `execution_environment.json` differs (host and compiler), with the same fixture and driver
  hashes.
- The current, sealed `check.py --mutations` still reproduces `observation.json` exactly.

## Findings (SWE2-AUDIT-SEM for OPUS)

- **N1 (narrowing; producer repair).** ASTRA's seal 13a61b94b (2026-09-26, after the 21f25545b merge) added
  three assertions to `retained-reward-bindings/check.py`. The package's README and section 7 still read as
  if run_review.py reproduces against the current database; it does not. The accepted statement is: the
  reproduction holds against the pinned pre-image, and the sealed checker independently agrees with the
  preserved observation. Repair by repinning the input (both outputs agree) or by a reproduction note.
- **N2 (note).** Two sampled bodies (`002F8BB0`, `00312280`) span chained `.pdata` fragments; their root
  entries end at `002F8C8D` and `00312330`. The manifest extents run contiguously to the final `ret`, and the
  decode reaches each end exactly, so the hashes cover whole bodies. `00264150` and `0020E600` are leaf
  functions with no `.pdata` entry.
- **N3 (note).** "Signed-byte global gate" is accurate about the load (`movsx`), but the test is
  `test eax, eax; jne`: any nonzero byte rejects, so the sign is immaterial to the decision.
- Not covered by this review: the other 14 bodies were taken on the rerun's hash check only; no live
  session, row contents or subscriber census; the inherited limits listed in the package stay open
  (GR-17, GR-18).

## Verdict (SWE2-AUDIT-SEM for OPUS)

ACCEPT-WITH-NARROWING. The award contract, the defeat contract corrections and the three pages' SECTION-03
statements hold on the sampled bytes, and the package's native evidence reproduces bit-identically on an
independent host and compiler. GR-16 can be restated by its owner on this verdict, carrying N1 as the
reproduction qualifier.
