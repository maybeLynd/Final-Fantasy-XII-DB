# SWE2-AUDIT-SPEC review of SD-101 (sd101-pass1-widgets-0930 at b545fdb02): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75, 2026-09-30). Author: OPUS.
Reviewed: commit `b545fdb02`, record [`sd101-pass1-widgets-0930`](../sd101-pass1-widgets-0930/README.md). Static.
Request: `OPUS-REQ-AUDITSPEC-SD101-0930`.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD101-0930 | sd101-pass1-widgets-0930 | `b545fdb02` | ACCEPT |

**Re-run.** `sd101_pass1.py` re-run from its own directory ([`rerun_sd101_pass1.out`](rerun_sd101_pass1.out)).
Identical to the committed `.out` (ignoring CR): P1-P6 PASS, `FAILS 0`. No tracked file changed.

**Re-derived independently** ([`sd101_indep.py`](sd101_indep.py) → [`sd101_indep.out`](sd101_indep.out)).
- **P3, the setters, with a wider sweep.** I used my own sweep ([`../auditspec-review-sd4-0930/bitsweep.py`](../auditspec-review-sd4-0930/bitsweep.py)
  with `0x40 24`) over every listed function plus every unlisted `.pdata` range (38,175 ranges). It covers any width
  at `+0x40..+0x43`, `bts` / `btr` / `btc`, and register read-modify-write stores. The record's P3 misses a
  `bts [reg+0x40], 0x18` (it tests `(0x18 >> 24) & 1`) and register-built whole-word stores. The sweep has 30 hits:
  - Its control **PASS** finds `005728E6`, `00573AF5`, `00247754`, `0057390E`, `00573952` and the subtree clear
    `0024773A`.
  - It finds no `bts`-family write.
  - Every other variable-register OR resolves to another bit or another object. The single-bit setters are `002418E0`
    bit 5, `002478D0` bit 18, `00247950` / `00247980` bit 1, `00248030` bit 17, `00559800` / `003C9900` bit 16,
    `003C99D0` / `003C9F80` bit 15 and `0055A1F0` bit 15 (xor). `002E2010` / `002E2570` write bit 0.
  - `002ECA30` ORs `1 << cl` into a 0x120-byte static record array (`r9` = rip table + index × 0x120), not a widget.
    `00226640` merges `+0x54` into `+0x40` of an object returned by `00359B80`, which is not shown to be a widget.
  - The four register-store clears (`and eax, 0x3ff`, then `mov [rcx+0x40], eax`, in `002A9F00` / `002AA800` /
    `002AAE40` / `002B0280`) store a 10-bit value, not a flag word.
  - Two `or reg, -1` stores remain, and neither is shown to be a widget. `00800F90` (`00801126`) initialises a new
    middleware object field by field. `0022F430` (`0022F4A4`) stores word `+0x42` = -1 beside word `+0x44` = 0, a
    16-bit field pair, on an object whose `+0x10` / `+0x18` go to `00233050`. The object is not identified here. If it
    were a widget, this would set bits 16-31 of `+0x40`, so it is the one residual candidate.

  So "set only at those five places" holds for every identified widget writer. The one unidentified candidate is
  `0022F4A4`, above.
- **P5, the call sites, from raw bytes.** A raw rel32 sweep (E8 / E9 / 0F 8x) of all `.text` for `00247730` finds
  **33** references: 31 `call` and 2 `jmp` (`00561E50`, `00573969`). One is the self-recursion `00247765`, leaving
  **32 outside sites**: 19 pass 1, 3 pass 0 and 10 a variable, the same site list as the record. My classification
  uses the same "last write of edx/rdx/dl in the 10 instructions before the site" heuristic, so it confirms the
  *sites* independently but the `:1` / `:0` / `:var` split only by the same method.

**Controls.** P1, P2, P4 and P6 are exact-instruction-text checks, sensitive to a misread body. P3 is a known-answer
check on its own sweep's output. It fails if a listed setter disappears, but it is **not sensitive** to a setter in an
unswept shape (`bts`, byte at `+0x43` with a register source, register-built stores). The sweep above closes that gap
with no new widget setter. P5 reads the catalogue call map, and the raw sweep shows that map is complete for `00247730`,
including both tail-jumps.

**Labels.** The "on top of" reading is correctly labelled as inference from frame order. The record also correctly
limits itself on wholesale `+0x40` copies and on the variable callers.
