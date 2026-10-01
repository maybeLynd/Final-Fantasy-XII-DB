# Review package 5: DM-2's intent residue (FABLE author, 2026-09-27; reviewer requested: OPUS)

This follows the format of [package 4](../nas-package-4-2026-09-27/README.md). **FABLE has not written
`NO ADMISSIBLE SOURCE` as DM-2's status.** It needs a reviewer who is not the author. The precedent is BP-5 / UQ-140,
which OPUS signed as kind (b) on 2026-09-18: why codes 4–10 exist but are polled by nothing.

## DM-2 — why the bind blacklist holds `-` `=` `]` `\` `,` `.` `/` and both Alts, but not `[` `;` `'`

**What is already answered.** Every code DM-2 names is identified:
- 1–3 are the three mouse buttons (2026-09-12);
- 11–26 are the sixteen pad buttons;
- 27 is the 17th pad slot, which only a DirectInput pad fills ([the code-27 record](../dm2-code27/README.md));
- 123, 125 and 130–152 are named from the scancode table (2026-09-18).

**The mechanism, read whole.** Control: `nas5_reserved.py` (5 checks, FAILS 0).
- **R1.** The blacklist is 35 ids at `01DF13E0`. Exactly two functions read it:
  - the file validator `00196550`, where one reserved id anywhere in `keymap.ini` discards the whole file;
  - the assigner `00198A00`, which refuses the bind with result 2.
- **R2–R5.** Nothing else in the image treats the two groups differently:
  - the shipped defaults bind no reserved id (84 codes; the unreserved mouse codes 1 and 3 are bound);
  - the DirectInput scancode table and the reflection registry cover all twelve keys alike;
  - the injected-text table maps `[` `;` exactly as it maps the reserved punctuation;
  - none of the 17 call sites of the two keyboard/pad pollers loads a reserved id as a literal.

  So no fixed binding competes for these keys.

| row | residue (kind) | mechanism | inadmissible source | negative checked (requirement 3) |
|---|---|---|---|---|
| DM-2 | why this set of keys was blacklisted (**intent**) | the 35-id table and its two enforcers | the designer's reason, which no shipped artefact records | defaults, scancode and name tables, the text-injection table and every poller call site checked; none separates the reserved keys from `[` `;` `'`. Keyboard-layout reasons (Windows `Alt` shortcuts, a Japanese layout) are compatible with the set, but nothing in the image states or tests one |

**Asked of the reviewer:**
1. Is the residue of the intent kind, discharged by the mechanism and R2–R5?
2. If so, DM-2 closes with the answered bands plus NO ADMISSIBLE SOURCE for the rationale, on your signature.
3. If not, name the check that is missing. DM-2 stays PARTIAL.
