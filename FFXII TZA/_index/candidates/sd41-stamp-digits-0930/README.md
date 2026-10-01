# SD-41: the image gives the two save stamps no meaning beyond equality (OPUS, 2026-09-30)

Register row SD-41 was registered by SWE2-DATA (`f7a3292bd`, version-stamps-and-what-loading-normalises.md §6). It asks
what the packed-decimal digits of `0x20050223` and `0x05071901` mean. The row itself notes the owner may close it OUT
OF EVIDENCE BOUNDARY if no labelled source exists. This record is the search for that source in the certified image.
The checker is `sd41_stamp_digits.py` (output `sd41_stamp_digits.out`, `FAILS 0`).

## Finding (OPUS)

**No labelled source exists in the image.**

- **F1: where the bytes occur.** Each constant's four bytes occur in the whole file only as instruction immediates at
  the known uses. `0x20050223` occurs once, in its getter `002EF2A0`. `0x05071901` occurs three times: its getter
  `00235E90`, the stamp store `002370DF`, and the one equality test `00233C4D`.
- **F2: how instructions use them.** No catalogued function uses either value in any other instruction. Nothing masks
  it, shifts it, splits it into digits or compares it by order.
- **F3: strings.** No string spells either value as a date or a digit run, in ANSI or UTF-16. Nothing formats either
  value for display or a log.

So the image uses both only as magic values: stored, returned, and tested for equality (V-2). The date reading
(2005-02-23; 05-07-19-01) is an interpretation of the digits. Nothing in the program confirms or refutes it.
**Proposed disposition for the owner: OUT OF EVIDENCE BOUNDARY**, with this record as the negative search.

## Limits (OPUS)

- **Scope of the search.** It covers the executable only. The shipped data archives are not searched, though a stamp
  written by the game would come from this code, not from data. Developer documentation outside the shipped files is
  out of scope by definition.

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register row belongs to SWE2-DATA's page.
