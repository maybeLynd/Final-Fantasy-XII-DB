# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-gil-storage-clamp-and-every-path-that-mo-ee-1003-2)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-GIL-STORAGE-CLAMP-AND-EVERY-PATH-THAT-C08B5` · Package: `_index/candidates/opus-gil-storage-clamp-and-every-path-that-mo-ee-1003-2/` (package last changed at `793e20e74`; reviewed at HEAD `85ecbde72`) · Page: `13-Rewards-Progression-Economy/gil-storage-clamp-and-every-path-that-moves-it.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 1 row. It was read clause by clause against a raw capstone decode of the certified image. This session hashed the image itself: SHA256 `73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`. The row holds as written. No narrowing is needed.

## SWE2-AUDIT-SPEC checks

- **Applier dry check.** `interior_applier.py` was invoked from the package directory with the venv python and without `--apply`. It printed `VERIFY 1 functions, 5 anchors` / `ALREADY` / `FAILS 0` and exited 0.
- **Counts.** 1 row with 5 anchors. The README's `Missing: 0` matches `rows.json`.

**`0030AEA0`**: exact.

- s = `rsp+0x20`. `cx` is stored at s+6 (`0030AEB2`) and dword 0xE at s+0 (`0030AEBF`).
- `0030AECD` calls `0031C5D0(&s)`. `test eax,eax` / `jns`, and a negative result returns -1 (`0030AED6`).
- Stores:
  - dword [s+0x38] → [rdx] (saved in `rsi`, `0030AEE4`);
  - `movzx` word [s+0x3C] → [r8] (saved in `rdi`, `0030AEEB`);
  - `movsx` word [s+0x40] → [r9] (saved in `rbx`, `0030AEF2`);
  - `movzx` word [s+0x3E] → [[rsp+0xF0]] (`0030AEFC`);
  - `movsx` word [s+0x42] → [[rsp+0xF8]] (`0030AF0B`).
- Frame: 0xC0 + one push puts the return address at `rsp+0xC8`. So `rsp+0xF0` and `rsp+0xF8` are the fifth and sixth stack arguments.
- The function returns 0. After `0030AED4` the body has no conditional jump, so "no null tests" holds.

The row claims nothing about `0031C5D0` beyond the sign test on its result, so that body was not needed.

## SWE2-AUDIT-SPEC limits

- Body statements only. This review does not interpret the record type 0xE or the five output fields.
- The applier reported `ALREADY`, so the page text was taken to be the `rows.json` text.
