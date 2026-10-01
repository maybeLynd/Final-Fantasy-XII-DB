# SWE2-AUDIT-SPEC review of SD-3 (sd3-policy-bit21-0930 at 1113232aa): ACCEPT (as NARROWED)

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75, 2026-09-30). Author: OPUS.
Reviewed: commit `1113232aa`, record [`sd3-policy-bit21-0930`](../sd3-policy-bit21-0930/README.md). Static.
Request: `OPUS-REQ-AUDITSPEC-SD3-0930`. The record proposes NARROWED, and the register carries it as narrowed; this
verdict accepts that status, not an answer.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD3-0930 | sd3-policy-bit21-0930 | `1113232aa` | ACCEPT |

**Re-run.** `sd3_bit21.py` re-run from its own directory ([`rerun_sd3_bit21.out`](rerun_sd3_bit21.out)). Identical to
the committed `.out` (ignoring CR): A1, A2, I1, I2 PASS, `FAILS 0`. No tracked file changed.

**Re-derived independently** ([`sd3_indep.py`](sd3_indep.py) → [`sd3_indep.out`](sd3_indep.out); raw rel32
E8 / E9 / 0F 8x over all `.text`, rip references, DIR64 relocations, full linear bodies read by hand):
- **Reachability.** `00228380` has exactly **1** reference: `00253CC3 call` in `00253C70`
  (`InputGameplay_ArbitrateDigitalInputAndModalState`), with 0 rip and 0 relocations. So "only caller" holds in every
  addressing form. `00229AF0` is reached only by the `jmp` at `0017D4B0`. `0017D4B0` is reached only by `007A3B74 jmp`
  in `007A3B20`. `00229590` has 0 branch references and 1 rip reference, the `lea` at `0022832E` in `002282F0`.
  Control: `00253C70` is found (PASS).
- **`007A3B20` event decode, read by hand.** `[rdx]` minus 1, 2, 1 reaches `007A3B5A` on event 4. There `[rdx+4] == 0`
  gives `mov [rcx+8], 3`, then `call 00228480`; a non-zero `al` skips (`007A3B6E jne`), otherwise `jmp 0017D4B0`.
  Holds.
- **`00229AF0`, the whole body (19 instructions).** It zeroes a global, then `00229B03 bt eax, 0x15` on `002E0FA0()`.
  When set, `mov ecx, 1` / `jmp 002E1020` (returns row 1's word). When clear, `00226BD0(0xF)`; if that is zero,
  `jmp 002DF370` with `ecx = 0x3F`, `edx = r8d = 1`. Holds exactly as A1 states. The name `Audio_SetGroupMask` for
  `002DF370` is not in `functions.tsv`. It comes from the cited sound page, and I did not re-derive it.
- **`00228380`, the whole body.** Bit 21 of the aggregate (`002283DA bt esi, 0x15`) leads to row 1 (`002E1020(1)`).
  If row 1's bit 21 is clear it goes to `0022843A` (return 0); if set, `xor ebx, ebx` (flag 0). Holds (I1).

**One precision the record leaves implicit (non-blocking).** The modal is not opened on every pass. Before the bit test
the function returns 0 when `003603C0()` or `0017D930()` is non-zero, or when a global dword is 0 (`002283D2`). After
it, the function returns 1 without opening when the modal already exists (`[01FD4940]`, `002283EF`) or while a
countdown dword is positive (it is decremented at `00228405`). It returns 0 when a second global pointer is null
(`002283B5` / `00228420`). So "normally carries a flag of 1" means "when it opens the modal at all". Bit 21 changes
only the flag, or suppresses the open when row 1 lacks the bit.

**Controls.** A1-A2 and I1-I2 are exact-instruction-text checks at fixed addresses. They are sensitive to a misread
body (any changed operand fails), but not to reachability. The "only caller" part of I1 uses the catalogue's call
map, and my raw sweep confirms it in every form.

**Status.** NARROWED is right. The player-visible meaning still depends on what `00229590` does with flag 0 against
flag 1, and on the identity of event 4. The record says both are open.
