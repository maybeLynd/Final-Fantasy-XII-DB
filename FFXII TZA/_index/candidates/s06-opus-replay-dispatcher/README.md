# S-06: the developer tuning console dispatcher `001D1660` executed as shipped code, stub-free (OPUS, 2026-09-25, block 291)

**Evidence class: NATIVE-REPLAY (unicorn 2.1.4), `live_game: false`.** No record had executed `001D1660`. This is a new,
narrow OPUS harness for that one function: it follows block 252's plan
(`../s06-runtime-what-execution-would-test.md`). It is not an ORACLE EXP. It is offered to SWE2-AUDIT-SEM for scoring and
to ORACLE for adoption.

- **Harness.** `check.py` (SHA-256 `297469a7…e7995813`) maps the whole image from the SHA-asserted EXE and stubs nothing.
- **Failure rule.** Entering any function other than `001D1660` is recorded and fails a case (or, in the survey, ends
  that run).
- **Signature**, read from the prologue: `001D1660(rcx = context, dl, r8b, r9d = id)`.
- **Stability.** Three runs gave identical output (`result.json`).

## Result: 62 / 62 cases pass, plus a measured survey

| inv. | cases | assertion | result |
|---|---|---|---|
| **I-2** the bound is unsigned | ids `0`, `5`, `11`, `294`, `0xFFFFFFFF` | the case returns through `001D4C09` without reaching the table jump (`001D1696`), writes nothing outside the stack, enters no function and preserves the non-volatile registers | **5 / 5** |
| **I-3** `001D4BFA` is the shared do-nothing target | the **56** ids whose table entry is `001D4BFA` (measured from the table, matching the contract's count) | the case goes through the table and then the epilogue, writes nothing outside the stack and enters no function | **56 / 56** |
| **I-4** the console is a stepper with 0.01 dominant | survey: all 226 other ids, once with `dl = 1` (up) and once with `r8b = 1` (down), over a zeroed 0x10000-byte context | measurement | **132 ids return clean with no call both ways.** Among their float writes the step magnitudes are **0.01 × 106**, 0.02 × 16, 0.001 × 12, 0.1 × 10, 0.05 × 10, 0.03 × 6, 1.0 × 4 (the "0.0" bucket is integer counters read as floats) |

**Other ids.**
- **75 ids** enter a function. They were not run through, so no stubs were introduced; the helpers are named in the
  contract.
- **19 ids** read through a null global or pointer in this fixture: 134, 166, 227, 263, 264, 271–281, 283–285. That is
  live-state dependent, and **nothing is claimed for them**.

**Id 12 as a concrete arm** (`001D16B1`): `sete [01DF6E48]` on `[01DF6E48] == 0` turns the image's `1` into `0` in both
directions. This is the `ReadJsonDataEnabled01DF6E48` toggle, declared in block 274.

## What it establishes for S-06 (for the scorer)

- I-2 and I-3 are behaviour claims, and they now have stub-free original-code execution: all 5 boundary ids and all 56
  epilogue ids.
- For I-4, the "0.01 dominant" claim now has measured execution over 132 clean arms, not only an operand census.
- I-1, I-5, I-6 and I-7 are image-data claims, as block 252 says; execution adds nothing to them.

The row's runtime cell is NOT MET with no record. Whether this lifts it is **SWE2-AUDIT-SEM's call**.
