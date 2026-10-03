# Homing pack: `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md`

Generated 2026-10-03 06:31 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-battle-text-banks.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002D4FB0 (118 B, extent 002D4FB0-002D5026)

Entered from (direct sites whose caller this page cites): `002902D0` + 0x1E (call; `002902D0` is cited on this page)
Other direct sites: none

Host context: " ('00305F90'–'00305FD8') | ~~'action_data.bin'~~ action-table row '+0x34' ('battle_pack.bin' '+0x3C'; corrected 2026-09-12, AY-6) | 0 | the action — the HUD post of the current action's name through '002902D0' | | 'BattleUnit_ApplyUnitDefinition' ('0023A88A'–'0023A8E1') | enemy row '+0x08' | by the word | the unit's name text, stored at unit '+0x18' | | 'BattleUnit_ApplyUnitDefinition' ('0023AB03'–'0023AB57') | party row '+0x30' | by th"

```
002D4FB0  mov      r11, rsp
002D4FB3  sub      rsp, 0x68
002D4FB7  mov      rax, qword ptr [rip + 0x1c6f872]  ; -> 01F44830 [u64 0x00002B992DDFA232]
002D4FBE  xor      rax, rsp
002D4FC1  mov      qword ptr [rsp + 0x58], rax
002D4FC6  mov      qword ptr [r11 - 0x48], rcx
002D4FCA  lea      rax, [r11 - 0x48]
002D4FCE  mov      dword ptr [rsp + 0x28], edx
002D4FD2  xor      r10d, r10d
002D4FD5  mov      dword ptr [r11 - 0x3c], r8d
002D4FD9  lea      rdx, [rip + 0xa00]  ; -> 002D59E0
002D4FE0  mov      qword ptr [r11 - 0x20], rax
002D4FE4  lea      r8, [r11 - 0x28]
002D4FE8  mov      eax, dword ptr [rsp + 0x90]
002D4FEF  mov      ecx, 0xf8
002D4FF4  mov      dword ptr [r11 - 0x38], r9d
002D4FF8  mov      dword ptr [rsp + 0x34], eax
002D4FFC  mov      eax, dword ptr [rsp + 0x98]
002D5003  mov      dword ptr [rsp + 0x38], eax
002D5007  mov      dword ptr [r11 - 0x28], r10d
002D500B  mov      qword ptr [r11 - 0x18], r10
002D500F  call     0x244f50  ; -> 00244F50 fn
002D5014  mov      rcx, qword ptr [rsp + 0x58]
002D5019  xor      rcx, rsp
002D501C  call     0x808c40  ; -> 00808C40 fn
002D5021  add      rsp, 0x68
002D5025  ret      
```

## 0056DA80 (423 B, extent 0056DA80-0056DC27)

Entered from (direct sites whose caller this page cites): `0056CF10` + 0x1F3 (call; `0056CF10` is cited on this page)
Other direct sites: none

Host context: "ores the four words sign-extended as dwords through the pointers in reverse order (word 0 to the fourth pointer, word 3 to the first) | '00510E4E', '00510E88', '00510EEA', '00510EF4', '00510F18' | | '0056CF10' | 660 B | when qword '+0xC8' of 'rcx' is null it clears bit '0x1' of dword '+8' in the nine objects at qwords '+0' to '+0x40' of the array at qword '[rdx+0x10]' and returns 1; otherwise, for the 32-byte entry 'r9d' of that table, "

```
0056DA80  mov      qword ptr [rsp + 8], rbx
0056DA85  mov      qword ptr [rsp + 0x10], rbp
0056DA8A  mov      qword ptr [rsp + 0x18], rsi
0056DA8F  mov      qword ptr [rsp + 0x20], rdi
0056DA94  push     r12
0056DA96  push     r14
0056DA98  push     r15
0056DA9A  sub      rsp, 0x30
0056DA9E  mov      rdi, rdx
0056DAA1  mov      r10d, 1
0056DAA7  mov      edx, dword ptr [r8]
0056DAAA  or       esi, 0xffffffff
0056DAAD  mov      eax, edx
0056DAAF  mov      rbx, r9
0056DAB2  mov      r14, r8
0056DAB5  mov      rbp, rcx
0056DAB8  and      eax, r10d
0056DABB  je       0x56dac2  ; -> 0056DAC2
0056DABD  mov      r9d, dword ptr [r9]
0056DAC0  jmp      0x56dac6  ; -> 0056DAC6
0056DAC2  mov      r9d, dword ptr [r9 + 4]
0056DAC6  xor      r12d, r12d
0056DAC9  test     dl, 2
0056DACC  je       0x56daf4  ; -> 0056DAF4
0056DACE  test     eax, eax
0056DAD0  lea      rax, [rbx + 4]
0056DAD4  jne      0x56dad9  ; -> 0056DAD9
0056DAD6  mov      rax, rbx
0056DAD9  mov      ecx, dword ptr [rax]
0056DADB  test     dl, 4
0056DADE  je       0x56daeb  ; -> 0056DAEB
0056DAE0  movzx    esi, word ptr [r8 + 4]
0056DAE5  mov      r8d, dword ptr [rbx + 8]
0056DAE9  jmp      0x56db09  ; -> 0056DB09
0056DAEB  mov      r8d, dword ptr [rbx + 8]
0056DAEF  mov      r10d, r12d
0056DAF2  jmp      0x56db09  ; -> 0056DB09
0056DAF4  mov      ecx, dword ptr [rbx + 8]
0056DAF7  test     eax, eax
0056DAF9  movzx    esi, word ptr [rbp + 0xe]
0056DAFD  lea      rax, [rbx + 4]
0056DB01  jne      0x56db06  ; -> 0056DB06
0056DB03  mov      rax, rbx
0056DB06  mov      r8d, dword ptr [rax]
0056DB09  movsxd   rax, ecx
0056DB0C  lea      r15, [rax*8]
0056DB14  mov      rax, qword ptr [rdi + 0x10]
0056DB18  mov      rcx, qword ptr [r15 + rax]
0056DB1C  and      dword ptr [rcx + 8], 0xfffffffe
0056DB20  or       dword ptr [rcx + 8], r10d
0056DB24  mov      rax, qword ptr [rdi + 0x10]
0056DB28  movsxd   rcx, dword ptr [rbx + 0xc]
0056DB2C  mov      rdx, qword ptr [rax + rcx*8]
0056DB30  mov      eax, dword ptr [r14]
0056DB33  shr      eax, 2
0056DB36  xor      eax, dword ptr [rdx + 8]
0056DB39  and      eax, 1
0056DB3C  xor      dword ptr [rdx + 8], eax
0056DB3F  mov      rax, qword ptr [rdi + 0x10]
0056DB43  movsxd   rcx, dword ptr [rbx + 0x10]
0056DB47  mov      rdx, qword ptr [rax + rcx*8]
0056DB4B  mov      eax, dword ptr [r14]
0056DB4E  shr      eax, 2
0056DB51  xor      eax, dword ptr [rdx + 8]
0056DB54  and      eax, 1
0056DB57  xor      dword ptr [rdx + 8], eax
0056DB5A  mov      rax, qword ptr [rdi + 0x10]
0056DB5E  movsxd   rcx, dword ptr [rbx + 0x14]
0056DB62  mov      rdx, qword ptr [rax + rcx*8]
0056DB66  mov      eax, dword ptr [r14]
0056DB69  shr      eax, 2
0056DB6C  movsxd   rcx, r9d
0056DB6F  xor      eax, dword ptr [rdx + 8]
0056DB72  and      eax, 1
0056DB75  xor      dword ptr [rdx + 8], eax
0056DB78  mov      rax, qword ptr [rdi + 0x10]
0056DB7C  mov      rdx, qword ptr [rax + rcx*8]
0056DB80  movsxd   rcx, r8d
0056DB83  and      dword ptr [rdx + 8], 0xfffffffe
0056DB87  mov      rax, qword ptr [rdi + 0x10]
0056DB8B  mov      rdx, qword ptr [rax + rcx*8]
0056DB8F  and      dword ptr [rdx + 8], 0xfffffffe
0056DB93  test     r10d, r10d
0056DB96  je       0x56dbc4  ; -> 0056DBC4
0056DB98  mov      rcx, qword ptr [rdi + 0x10]
0056DB9C  mov      r9d, esi
0056DB9F  mov      qword ptr [rsp + 0x28], r12
0056DBA4  xor      r8d, r8d
0056DBA7  xor      edx, edx
0056DBA9  mov      dword ptr [rsp + 0x20], r12d
0056DBAE  mov      rcx, qword ptr [rcx + r15]
0056DBB2  call     0x29ff60  ; -> 0029FF60 fn
0056DBB7  mov      rcx, qword ptr [rdi + 0x10]
0056DBBB  mov      rcx, qword ptr [rcx + r15]
0056DBBF  call     0x29fb50  ; -> 0029FB50 fn
0056DBC4  test     byte ptr [r14], 4
0056DBC8  je       0x56dc08  ; -> 0056DC08
0056DBCA  mov      r9d, dword ptr [rbp + 0x10]
0056DBCE  xor      r8d, r8d
0056DBD1  movsxd   rax, dword ptr [rbx + 0xc]
0056DBD5  btr      r9d, 0x1f
0056DBDA  mov      rcx, qword ptr [rdi + 0x10]
0056DBDE  xor      edx, edx
0056DBE0  imul     r9d, esi
0056DBE4  mov      qword ptr [rsp + 0x28], r12
0056DBE9  mov      dword ptr [rsp + 0x20], r12d
0056DBEE  mov      rcx, qword ptr [rcx + rax*8]
0056DBF2  call     0x29ff60  ; -> 0029FF60 fn
0056DBF7  movsxd   rax, dword ptr [rbx + 0xc]
0056DBFB  mov      rcx, qword ptr [rdi + 0x10]
0056DBFF  mov      rcx, qword ptr [rcx + rax*8]
0056DC03  call     0x29fb50  ; -> 0029FB50 fn
0056DC08  mov      rbx, qword ptr [rsp + 0x50]
0056DC0D  mov      rbp, qword ptr [rsp + 0x58]
0056DC12  mov      rsi, qword ptr [rsp + 0x60]
0056DC17  mov      rdi, qword ptr [rsp + 0x68]
0056DC1C  add      rsp, 0x30
0056DC20  pop      r15
0056DC22  pop      r14
0056DC24  pop      r12
0056DC26  ret      
```
