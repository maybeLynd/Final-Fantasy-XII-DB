# SWE2-AUDIT-SPEC review: FABLE correction of the 003EEEC0 row (repair of SPEC's REJECT)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session) · 2026-10-03 ·
Task: `FABLE-REQ-AUDITSPEC-CORR-003EEEC0-1003` · Correction commit `370cd06c9` · Record: `_index/candidates/fable-corr-003eeec0-1003/`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks at the bytes

The dispatch is `movzx ecx, byte [rbx+0C8h]` (`003EEF53`).

| byte `+0C8h` | instructions | effect |
|---|---|---|
| 0 | `je 003EEFC6` | calls `251D20`; when the result is above 2 (signed), sets the byte to 1 and `+0CCh` to 12h |
| 1 | `sub ecx,1 / je 003EEF9A` | calls `2C99A0(3E8h, 8, 0)`, sets the byte to 2 and `+0CCh` to 3Ch, then continues with `edx` = 13h |
| 2 | second `sub ecx,1 / je 003EEF86` | sets the byte to 3 and returns 0 |
| 4 | `cmp ecx,2` (`003EEF68` = `003EEEC0`+0xA8) matches | falls to `mov rcx,rbx / call 00244F00` at `003EEF74` (= `003EEEC0`+0xB4), then `xor eax,eax` |
| 3 or anything else | `jne 003EF037` | `xor eax,eax / ret` |

The repaired clause, "2 sets it to 3, ~~3 calls~~ 4 calls `003EEEC0`+0xB4 with `rcx`, and 3 or any other value returns
0", is exact. The strike is over real old text.

FABLE's `check.py` re-run gives: states reaching `003EEF74` = [4] (expected {4}); the control that ignores the subs
gives [2]; FAILS 0. This review closes SPEC's REJECT of the ui-layout row (parent session, `46d2749cb`).
