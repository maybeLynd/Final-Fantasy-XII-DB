# F-interior pack: `07-Combat-Action/Command-And-Action-Seam/native-command-seam.md`

Generated 2026-10-02 20:18 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/native-command-seam.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

## 00359250 (103 B, extent 00359250-003592B7)

Page context: "arty — CLIENT (SWE2-EC7-158, 25 edges).** Batch-123's '0026B4A0' names '00351F40'/'00355540'/'00355A00'/'00238BF0', and the seam's own '0026D6D0' is called by the party layer's '00358B40'/'00359200'/'00359250'/'003592C0' — the party side consults the seam's helpers, fan-in only.  - **CombatFormula — SERVICE (3 edges).** 'BattleUnit_AdvanceStandardActionState' ('00304850') reaches the combat formula helpers '00387090'/'00387A50', and '00"

```
00359250  sub      rsp, 0x28
00359254  test     edx, edx
00359256  je       0x35926a  ; -> 0035926A
00359258  movzx    edx, byte ptr [rip + 0x1f6eda5]  ; -> 022C8004
0035925F  bts      edx, ecx
00359262  mov      byte ptr [rip + 0x1f6ed9c], dl  ; -> 022C8004
00359268  jmp      0x35927d  ; -> 0035927D
0035926A  movzx    eax, byte ptr [rip + 0x1f6ed93]  ; -> 022C8004
00359271  btr      eax, ecx
00359274  movzx    edx, al
00359277  mov      byte ptr [rip + 0x1f6ed87], al  ; -> 022C8004
0035927D  movzx    eax, byte ptr [rip + 0x1f6ed81]  ; -> 022C8005
00359284  or       al, byte ptr [rip + 0x1f6ed7c]  ; -> 022C8006
0035928A  or       al, byte ptr [rip + 0x1f6ed77]  ; -> 022C8007
00359290  or       al, dl
00359292  test     al, 1
00359294  je       0x3592b2  ; -> 003592B2
00359296  mov      ecx, dword ptr [rip + 0x1f6ed44]  ; -> 022C7FE0
0035929C  call     0x3588b0  ; -> 003588B0 fn
003592A1  test     rax, rax
003592A4  je       0x3592b2  ; -> 003592B2
003592A6  mov      rcx, rax
003592A9  add      rsp, 0x28
003592AD  jmp      0x26d6d0  ; -> 0026D6D0 fn
003592B2  add      rsp, 0x28
003592B6  ret      
```
