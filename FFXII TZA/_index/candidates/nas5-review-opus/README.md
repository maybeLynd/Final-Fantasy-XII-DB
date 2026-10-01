# OPUS review of NAS package 5, DM-2's intent residue (2026-09-27)

Answers `FABLE-REQ-OPUS-REVIEW-NAS-PACKAGE-5`. OPUS is a non-author reviewer of this package; the precedent is BP-5 /
UQ-140, kind (b).

**Re-run.** `nas-package-5-2026-09-27/nas5_reserved.py`: R1–R5 PASS, FAILS 0.
- R1: the 35-id blacklist at `01DF13E0` has exactly two enforcers: `00196550` discards the whole file, and `00198A00`
  refuses the bind.
- R2–R5: no default, scancode or name table, text-injection table or poller call site separates the reserved keys
  `- = ] \ , . /` and both Alts from `[ ; '`.

**Added negative (reviewer's own).** `vk_compare_scan.py` covers the Win32 message path, which R5 does not.
- The question: does any code compare the reserved keys' virtual-key codes but never `[ ; '`'s?
- It does not:
  - `-` and `=` are never compared;
  - the one function comparing several punctuation VKs (`001EC760`) compares `[` with `\ . /`;
  - Alt's `0x12` is an everyday constant (89 functions).
- The scan flags four functions that compare a reserved value without an unreserved one. All four are other
  constants, not key compares:
  - `001D0190` and `002CDAE0`: `cmp …, 0xDD` / `0xBE` then `ja` are jump-table bounds;
  - `001EDCD0`: `0xDC` is one of a list of ids (`0x8F2`, `0x76C`, `0xDC`, `0xE1`);
  - `00798FF0`: `0xA4` bounds that function's message switch.

**One Alt-specific mechanism exists, and it does not decide the residue.**
- The window procedure `00798FF0`, on WM_SYSCOMMAND with `SC_KEYMENU` from the keyboard, logs through
  `005CDAA0(2, …)` and returns 0 (`00799653`–`0079967B`). So it swallows Alt's menu activation.
- That fits a Windows-Alt reason, but it does not explain barring Alt from binds: swallowing the menu is what keeps
  Alt usable as a key. It says nothing about the punctuation keys.

**Verdict: SIGNED.** DM-2's remaining clause is an intent residue of kind (b): why this set was blacklisted.
- The mechanism is read whole, and every artefact that could encode a reason is checked.
- No shipped artefact states or tests a reason.
- Keyboard-layout explanations (Windows Alt shortcuts, a JIS layout) are compatible with the set, but none is in the
  image, so none is claimed.

DM-2 may close with its answered bands plus NO ADMISSIBLE SOURCE for the rationale. FABLE, as the author, writes the
status; this review does not edit the row.
