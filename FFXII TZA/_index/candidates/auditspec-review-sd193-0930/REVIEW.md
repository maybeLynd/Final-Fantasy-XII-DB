# REVIEW: sd193-turn-step-0930

- **Package:** `sd193-turn-step-0930` (OPUS, commit `79ba50e5c`)
- **Task:** `OPUS-REQ-AUDITSPEC-SD193-0930`
- **Reviewer:** SWE2-AUDIT-SPEC (independent of OPUS author maybeLynd)
- **Verdict: ACCEPT-WITH-NARROWING**

## Controls re-run

`sd193_turn.py` re-executed: `rerun_sd193_turn.out` text-identical to the committed `.out`
(CRLF only), H1–H3 / E1–E2 / M1 PASS, `FAILS 0`. Package dir clean after re-run.

## Independent verification

Own toolchain: `rvimg.py` (pefile + capstone + unicorn, image sha256 asserted), `sd193_rederive.py`
→ `sd193_rederive.out` — after fixing two defects in *my own* instrument (see below), all checks pass:
`FAILS 0`.

- **D1–D4** branch/operand reads verified instruction-for-instruction.
- **W1/W2** image-wide writer census: `01DFE0BC` has 183 rip references (it is the image's shared
  `1.0f` constant — not a private step cell) and exactly **one** write: `001EDDE0 movss
  [rip+..],xmm1`, gated on `001EDDC0`'s ecx!=0 arm (the 60-fps FrameLimit==1 fixup branch).
- **X1–X3**: executed `003A1AD0` on 4,006 samples = reference bit-for-bit; `003EC510` on 9,003
  points; `003A1980` = `min(|x|,s)` on 2,000 points — all executed, not decoded-only.
- **X4–X9**: full `003EC040` unicorn runs — constant-rate step confirmed (12×0.1 then 0.05 landing
  exactly on target; no easing); mode-2 via `003A1AD0`, modes 0/1 forced direction via `003EC510`
  with one-step snap; modes 3/−1/no-rate-record return the target; hold ids 0x0D/0x35/0x36 hold
  `+0x124` (00422D50 stubbed).

## Narrowings (found by executed re-derivation)

1. **Missing case-table row:** `+0x290 & 0x100000 == 0` with `word +6 != -1` (and `+0x284` bit
   `0x8000000` clear) returns the **target at once in every mode** (`003EC10C..003EC115 →
   003EC124`; executed as X6). Turning happens only when bit `0x100000` is set or `+6 == -1`.
2. **The 0.5 multiplier is conditional:** `01DFE0BC` is `1.0` in the file; `001EDDE0` stores `0.5`
   only on `001EDDC0`'s `ecx != 0` arm (the 60-fps FrameLimit==1 branch). "set to 0.5 by the boot
   fixups" / "half the record's rate" overreach — at the default it stays 1.0.
3. **Modes 0/1 do not wrap:** `cur ± step` is returned unwrapped (X7: 3.1 + 0.1 → 3.200000 > π).
   Not claimed otherwise; recorded for completeness.

## Instrument defects fixed during review (mine, disclosed)

- The rip-candidate filter excluded `next_ip == site+4` (disp as last field) — `0 <` → `0 <=`.
- Decode-back took the *first* validating start, which admitted misaligned ghosts whose own disp
  field also landed on the site (`adc byte [rip+d],dl` at `site-2` shadowing the true `movss` at
  `site-4`). Now: earliest validating start wins, and the dword at `site` must equal the operand's
  disp. Before the fix the sweep returned 183 ghost-aliased hits and missed all three known refs;
  after, W1/W2 pass with the true instructions.
- X1's one mismatch was an unrounded float64 sample (`0.1` → `r32(0.1)`).

## Limits

- Static + emulated-single-function scope; which caller combinations occur in shipping play is
  not exercised.
- `01DFE0BC`'s 183 readers are the shared-constant pool; W1 proves write-exclusivity, not
  "only the step uses this cell".

**Verdict: ACCEPT-WITH-NARROWING** — core claim (constant-rate heading step, mode-2 shortest-way
via `003A1AD0`, forced direction with snap via `003EC510`, not an easing curve) verified by
execution on original bytes; narrowed by the missing case row, the conditional 0.5 multiplier and
the unwrapped modes-0/1 result.
