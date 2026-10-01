# SWE2-AUDIT-SPEC review of SD-8 (sd8-dispatcher-mode-0930 at 58c0b91be): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75, 2026-09-30). Reviewed: OPUS's
`58c0b91be` (the record's only commit), [README](../sd8-dispatcher-mode-0930/README.md) and `sd8_dispatcher_mode.py`.
Static, certified image.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD8-0930 | sd8-dispatcher-mode-0930 | `58c0b91be` | ACCEPT |

**Re-run.** [rerun_sd8_dispatcher_mode.out](rerun_sd8_dispatcher_mode.out) is identical to the committed `.out` (ignoring CR),
F1-F5 PASS, `FAILS 0`. The record directory stayed clean.

**Re-derived independently** ([sd8_rederive.py](sd8_rederive.py) / [.out](sd8_rederive.out)).
- **Every access covering `02064AD3`, across ALL `.text` and with access widths.** There are 17 rip accesses, all
  1-byte. The eight stores are those in the record's table: `00229F00`, `0022A1A0`, `0022AFF2`, `0022B097`,
  `0022B74E`, `0022B85B`, `0022BB81` and `0022BDC5`.
  - There are 0 image-base-relative accesses in `02064AC8`..`02064AD3`.
  - No wider store anchored below covers the byte. The one raw-only candidate near it, `0022A190`, is a dword store
    to `02064AD4`.
  - So F2's writer set is complete in both addressing forms, including unlisted code.
- **The outside setter.** `00229F00` is `mov [02064AD3], cl; ret`. Its raw call sites are exactly `002E0D39` (in
  `002E09A0`), `002E2257` and `002E2274` (in `002E2240`). It has no jcc, no rip reference and no relocation. This
  matches F4.
- **Mode 1 exit.** `0022B837` `call 0032E520(1)`; `jne` past the store if non-zero. Then `0037C2E0()`,
  `movzx ecx, [mode]`, `cmove ecx, ebx` (with `ebx` = 2), store at `0022B85B`. So 1 -> 2 only when both return 0, and
  otherwise it stays in 1. F2 prints this store as `cl`, and F3 checks the `cmove`; the pair is right.
- **Mode 5 exit.** `0022BDB2 cmp [mode], 5` / `je` skips; otherwise `0022BDC5` stores 2. The record's wording ("once
  the mode is no longer 5") is exact.
- **Poll gate.** My trace of `0022A600`..`0022A659`:
  - modes 4 and 6 take `0022A630` and end with `ebx` = 0;
  - modes outside 2..5 go to `0022A638`, `ebx` = 0;
  - mode 4 is excluded again at `0022A623`;
  - modes 2, 3 and 5 keep `ebx` and reach `call 0035E6F0` at `0022A659`.

  F5 does not show where `ebx` comes from. I checked it: `0022A5A5 mov ebx, 1`, callee-saved across the intervening
  calls. So the poll runs in modes 2, 3 and 5 as stated.

**Controls.**
- F2 is an exact-list equality over retool.py's extent-bounded rip index. It would catch an extra writer inside listed
  code, but not an unlisted, image-base-relative or aliasing writer. My sweep covers those three and finds none.
- F4 reads each argument as `ins(site - 5)`, which assumes a 5-byte `mov ecx, imm32` immediately before the call. It
  holds at all three sites.

**Stated limit (when the title first draws relative to mode 1).** It is correctly left open. The image shows that
mode 1 waits on `0032E520(1)` and `0037C2E0()`. It does not show whether the title is drawn during that wait.
`MainLoop_Draw` (`0022B0B0`) branches on the mode at `0022B5C1` (`cmp`, 2), so drawing is mode-dependent, and a live
frame trace is the way to settle it. Nothing in the answer depends on it.

**Correction wording:** none needed.
