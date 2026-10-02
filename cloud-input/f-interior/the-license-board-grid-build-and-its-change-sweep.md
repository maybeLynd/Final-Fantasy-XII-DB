# F-interior pack: `16-UI/License-Board-View/the-license-board-grid-build-and-its-change-sweep.md`

Generated 2026-10-02 09:51 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/the-license-board-grid-build-and-its-change-sweep.json`.

Functions: 10. Each is cited on the page only at its entry and is still in the F frontier.

## 001E0A40 (40 B, extent 001E0A40-001E0A68)

Page context: "r sets '+0x524' bit 0, re-reads the cell, runs '0055B8C0' + '0055A180', posts '00247510(0x8000)' and SE 1; the stick pan reads '02F97398'/'02F97399' (or '02F9739A'/'02F9739B' fallback) sar-5 through '001E0A40'/'001E0A70'/'00228480' into '+0x51C'/'+0x51E', clamped to the '+0x514'..'+0x51B' rectangle, and '+0x570' bit 0x100 clears once the pan returns to its resting point.  Interior anchor '0055CBDE' (function '0055C740').  '0055B6D0' (36"

```
001E0A40  sub      rsp, 0x28
001E0A44  call     0x198790  ; -> 00198790 fn
001E0A49  test     rax, rax
001E0A4C  je       0x1e0a63  ; -> 001E0A63
001E0A4E  call     0x198790  ; -> 00198790 fn
001E0A53  mov      rcx, rax
001E0A56  call     0x1976e0  ; -> 001976E0 fn
001E0A5B  movzx    eax, al
001E0A5E  add      rsp, 0x28
001E0A62  ret      
001E0A63  add      rsp, 0x28
001E0A67  ret      
```

## 001E0A70 (40 B, extent 001E0A70-001E0A98)

Page context: "524' bit 0, re-reads the cell, runs '0055B8C0' + '0055A180', posts '00247510(0x8000)' and SE 1; the stick pan reads '02F97398'/'02F97399' (or '02F9739A'/'02F9739B' fallback) sar-5 through '001E0A40'/'001E0A70'/'00228480' into '+0x51C'/'+0x51E', clamped to the '+0x514'..'+0x51B' rectangle, and '+0x570' bit 0x100 clears once the pan returns to its resting point.  Interior anchor '0055CBDE' (function '0055C740').  '0055B6D0' (360 B) is the"

```
001E0A70  sub      rsp, 0x28
001E0A74  call     0x198790  ; -> 00198790 fn
001E0A79  test     rax, rax
001E0A7C  je       0x1e0a93  ; -> 001E0A93
001E0A7E  call     0x198790  ; -> 00198790 fn
001E0A83  mov      rcx, rax
001E0A86  call     0x1976f0  ; -> 001976F0 fn
001E0A8B  movzx    eax, al
001E0A8E  add      rsp, 0x28
001E0A92  ret      
001E0A93  add      rsp, 0x28
001E0A97  ret      
```

## 002C1000 (687 B, extent 002C1000-002C12AF)

Page context: "ct '00559800''s bit16 propagate touches. Interior anchor '00247693' (the 'bts' on '+0x40').  ## SWE2-EC7-102 update (2026-09-20) - '00283730' measured  '00283730' (220 B) is the command-id predicate '002C1000', '0055BFF0' and '0055F830' call: 'ecx - 0x4B3' bounds a 12-arm '0028380C' jump table whose arms mostly answer 'setne' on '0032A8A0(0x4004..0x4010)' capability ids, two arms first gate on '00254A50() == 0', one arm returns 1 outrig"

```
002C1000  push     rbx
002C1002  sub      rsp, 0x40
002C1006  mov      rbx, rcx
002C1009  mov      ecx, dword ptr [rdx]
002C100B  sub      ecx, 1
002C100E  je       0x2c103b  ; -> 002C103B
002C1010  sub      ecx, 1
002C1013  je       0x2c102b  ; -> 002C102B
002C1015  cmp      ecx, 0x10
002C1018  je       0x2c12a7  ; -> 002C12A7
002C101E  mov      rcx, rbx
002C1021  add      rsp, 0x40
002C1025  pop      rbx
002C1026  jmp      0x5c5230  ; -> 005C5230 fn
002C102B  mov      rcx, rbx
002C102E  call     0x2d0410  ; -> 002D0410 fn
002C1033  xor      eax, eax
002C1035  add      rsp, 0x40
002C1039  pop      rbx
002C103A  ret      
002C103B  mov      rax, qword ptr [rip + 0x1dd9bee]  ; -> 0209AC30
002C1042  mov      qword ptr [rsp + 0x50], rbp
002C1047  mov      qword ptr [rsp + 0x58], rsi
002C104C  mov      qword ptr [rsp + 0x60], rdi
002C1051  movsx    ecx, word ptr [rax + 0xde0]
002C1058  mov      qword ptr [rsp + 0x38], r14
002C105D  mov      qword ptr [rsp + 0x30], r15
002C1062  call     0x282df0  ; -> 00282DF0 fn
002C1067  mov      rcx, qword ptr [rip + 0x1dd9bc2]  ; -> 0209AC30
002C106E  mov      r9, rbx
002C1071  mov      r8d, 0xf
002C1077  mov      rsi, rax
002C107A  mov      r14d, dword ptr [rax + 0x90]
002C1081  mov      rdx, qword ptr [rcx + 0x30]
002C1085  lea      rcx, [rbx + 0x50]
002C1089  mov      r15d, dword ptr [rax + 0xb0]
002C1090  mov      ebp, dword ptr [rax + 0x94]
002C1096  call     0x2432b0  ; -> 002432B0 fn
002C109B  movzx    ecx, word ptr [rax + 0xa]
002C109F  movzx    edx, word ptr [rax + 8]
002C10A3  movsx    r8d, word ptr [rax + 6]
002C10A8  test     rbx, rbx
002C10AB  je       0x2c10ce  ; -> 002C10CE
002C10AD  movzx    eax, word ptr [rax + 4]
002C10B1  mov      word ptr [rbx + 0x98], ax
002C10B8  mov      word ptr [rbx + 0x9a], r8w
002C10C0  mov      word ptr [rbx + 0x9c], dx
002C10C7  mov      word ptr [rbx + 0x9e], cx
002C10CE  xor      edi, edi
002C10D0  mov      eax, 0x5f5e0ff
002C10D5  cmp      r14d, -1
002C10D9  cmove    r14d, edi
002C10DD  cmp      r15d, -1
002C10E1  cmove    r15d, edi
002C10E5  cmp      ebp, -1
002C10E8  cmove    ebp, edi
002C10EB  cmp      r14d, eax
002C10EE  cmova    r14d, eax
002C10F2  mov      eax, 0x1869f
002C10F7  cmp      r15d, eax
002C10FA  cmova    r15d, eax
002C10FE  mov      eax, 0xf423f
002C1103  cmp      ebp, eax
002C1105  cmova    ebp, eax
002C1108  test     rbx, rbx
002C110B  jne      0x2c1111  ; -> 002C1111
002C110D  mov      ecx, edi
002C110F  jmp      0x2c1119  ; -> 002C1119
002C1111  mov      rax, qword ptr [rbx + 0x60]
002C1115  mov      rcx, qword ptr [rax + 0x30]
002C1119  lea      rdx, [rbx + 0xd4]
002C1120  mov      qword ptr [rsp + 0x28], rdi
002C1125  mov      r9d, r14d
002C1128  mov      dword ptr [rsp + 0x20], edi
002C112C  mov      r8d, 0x20
002C1132  call     0x29ff60  ; -> 0029FF60 fn
002C1137  mov      r14, qword ptr [rsp + 0x38]
002C113C  cmp      word ptr [rsi + 0x60], di
002C1140  jl       0x2c11c8  ; -> 002C11C8
002C1146  test     byte ptr [rsi], 2
002C1149  je       0x2c11c8  ; -> 002C11C8
002C114B  test     rbx, rbx
002C114E  jne      0x2c1155  ; -> 002C1155
002C1150  mov      rax, rdi
002C1153  jmp      0x2c115d  ; -> 002C115D
002C1155  mov      rax, qword ptr [rbx + 0x60]
002C1159  mov      rax, qword ptr [rax + 0x10]
002C115D  and      dword ptr [rax + 8], 0xfffffffe
002C1161  test     rbx, rbx
002C1164  jne      0x2c116b  ; -> 002C116B
002C1166  mov      rcx, rdi
002C1169  jmp      0x2c1173  ; -> 002C1173
002C116B  mov      rax, qword ptr [rbx + 0x60]
002C116F  mov      rcx, qword ptr [rax + 0x38]
002C1173  lea      rdx, [rbx + 0xf4]
002C117A  mov      qword ptr [rsp + 0x28], rdi
002C117F  mov      r9d, ebp
002C1182  mov      dword ptr [rsp + 0x20], edi
002C1186  mov      r8d, 0x20
002C118C  call     0x29ff60  ; -> 0029FF60 fn
002C1191  test     rbx, rbx
002C1194  je       0x2c119e  ; -> 002C119E
002C1196  mov      rax, qword ptr [rbx + 0x60]
002C119A  mov      rdi, qword ptr [rax + 0x20]
002C119E  mov      ecx, 0x3eb
002C11A3  call     0x2f9860  ; -> 002F9860 fn
002C11A8  xor      ecx, ecx
002C11AA  mov      qword ptr [rdi + 0x18], rax
002C11AE  call     0x20e620  ; -> 0020E620 fn
002C11B3  mov      ecx, 2
002C11B8  mov      dword ptr [rdi + 0x20], eax
002C11BB  call     0x2dd7e0  ; -> 002DD7E0 fn
002C11C0  mov      dword ptr [rdi + 0x24], eax
002C11C3  jmp      0x2c128c  ; -> 002C128C
002C11C8  test     rbx, rbx
002C11CB  jne      0x2c11d2  ; -> 002C11D2
002C11CD  mov      rax, rdi
002C11D0  jmp      0x2c11da  ; -> 002C11DA
002C11D2  mov      rax, qword ptr [rbx + 0x60]
002C11D6  mov      rax, qword ptr [rax + 0x10]
002C11DA  and      dword ptr [rax + 8], 0xfffffffe
002C11DE  test     rbx, rbx
002C11E1  jne      0x2c11e8  ; -> 002C11E8
002C11E3  mov      rax, rdi
002C11E6  jmp      0x2c11f0  ; -> 002C11F0
002C11E8  mov      rax, qword ptr [rbx + 0x60]
002C11EC  mov      rax, qword ptr [rax + 0x20]
002C11F0  and      dword ptr [rax + 8], 0xfffffffe
002C11F4  test     rbx, rbx
002C11F7  jne      0x2c11fe  ; -> 002C11FE
002C11F9  mov      rcx, rdi
002C11FC  jmp      0x2c1206  ; -> 002C1206
002C11FE  mov      rax, qword ptr [rbx + 0x60]
002C1202  mov      rcx, qword ptr [rax + 0x38]
002C1206  lea      rdx, [rbx + 0xf4]
002C120D  mov      qword ptr [rsp + 0x28], rdi
002C1212  mov      r9d, ebp
002C1215  mov      dword ptr [rsp + 0x20], edi
002C1219  mov      r8d, 0x20
002C121F  call     0x29ff60  ; -> 0029FF60 fn
002C1224  test     rbx, rbx
002C1227  jne      0x2c122e  ; -> 002C122E
002C1229  mov      rsi, rdi
002C122C  jmp      0x2c1236  ; -> 002C1236
002C122E  mov      rax, qword ptr [rbx + 0x60]
002C1232  mov      rsi, qword ptr [rax + 0x28]
002C1236  mov      ecx, 0x4b5
002C123B  call     0x283730  ; -> 00283730 fn
002C1240  and      dword ptr [rsi + 8], 0xfffffffe
002C1244  lea      rdx, [rbx + 0x114]
002C124B  and      eax, 1
002C124E  mov      qword ptr [rsp + 0x28], rdi
002C1253  or       dword ptr [rsi + 8], eax
002C1256  mov      r9d, r15d
002C1259  mov      r8d, 0x20
002C125F  mov      dword ptr [rsp + 0x20], edi
002C1263  mov      rcx, rsi
002C1266  call     0x29ff60  ; -> 0029FF60 fn
002C126B  test     rbx, rbx
002C126E  je       0x2c1278  ; -> 002C1278
002C1270  mov      rax, qword ptr [rbx + 0x60]
002C1274  mov      rdi, qword ptr [rax + 0x18]
002C1278  mov      ecx, 0x4b5
002C127D  call     0x283730  ; -> 00283730 fn
002C1282  and      dword ptr [rdi + 8], 0xfffffffe
002C1286  and      eax, 1
002C1289  or       dword ptr [rdi + 8], eax
002C128C  and      dword ptr [rbx + 0x40], 0xfffff7ff
002C1293  mov      r15, qword ptr [rsp + 0x30]
002C1298  mov      rdi, qword ptr [rsp + 0x60]
002C129D  mov      rsi, qword ptr [rsp + 0x58]
002C12A2  mov      rbp, qword ptr [rsp + 0x50]
002C12A7  xor      eax, eax
002C12A9  add      rsp, 0x40
002C12AD  pop      rbx
002C12AE  ret      
```

## 002C12B0 (75 B, extent 002C12B0-002C12FB)

Page context: "ve or the start index closes the loop. The page-up armed-slot search.  Interior anchor '0027F471' (function '0027F430').  '0027EDA0' (216 B) is the '0027F430' mirror '00557A40' and '0055AE00' share ('002C12B0' also calls): 'word[rcx]-1' wraps to 8 under 'cmovs', the same '+0xAC8' ring, the same '+0xD3C'-bit-0x10 gate, the same 'word[+0x60]'/'byte[+0]' eligibility tests and 'r8' predicate — the page-down armed-slot search.  Interior anch"

```
002C12B0  sub      rsp, 0x28
002C12B4  mov      rax, qword ptr [rip + 0x1dd9975]  ; -> 0209AC30
002C12BB  mov      rcx, qword ptr [rax + 0x118]
002C12C2  test     rcx, rcx
002C12C5  je       0x2c12f4  ; -> 002C12F4
002C12C7  add      rcx, 0xc8
002C12CE  xor      r8d, r8d
002C12D1  xor      edx, edx
002C12D3  call     0x27eda0  ; -> 0027EDA0 fn
002C12D8  cmp      eax, 1
002C12DB  jne      0x2c12f4  ; -> 002C12F4
002C12DD  lea      ecx, [rax + 0x50]
002C12E0  call     0x249c60  ; -> 00249C60 fn
002C12E5  call     0x2c1800  ; -> 002C1800 fn
002C12EA  call     0x2c38b0  ; -> 002C38B0 fn
002C12EF  call     0x2c4720  ; -> 002C4720 fn
002C12F4  xor      eax, eax
002C12F6  add      rsp, 0x28
002C12FA  ret      
```

## 002C1320 (75 B, extent 002C1320-002C136B)

Page context: "re-lays the pane — the detail pane's whole rebuild on a page commit.  Interior anchor '005587AE' (function '00558760').  '0027F430' (270 B) is the forward ring-query '00557A90' and '0055B840' share ('002C1320' also calls): 'word[rcx]+1' folds mod 9 by the '0x38E38E39' multiply, then the '[0209AC30+0xAC8]' 8-byte-entry ring walks — when 'byte[+0xD3C]' bit 0x10 is set, records with 'word[+0x60]' negative, 'byte[+0]' bit 1 set, or 'word[+0"

```
002C1320  sub      rsp, 0x28
002C1324  mov      rax, qword ptr [rip + 0x1dd9905]  ; -> 0209AC30
002C132B  mov      rcx, qword ptr [rax + 0x118]
002C1332  test     rcx, rcx
002C1335  je       0x2c1364  ; -> 002C1364
002C1337  add      rcx, 0xc8
002C133E  xor      r8d, r8d
002C1341  xor      edx, edx
002C1343  call     0x27f430  ; -> 0027F430 fn
002C1348  cmp      eax, 1
002C134B  jne      0x2c1364  ; -> 002C1364
002C134D  lea      ecx, [rax + 0x50]
002C1350  call     0x249c60  ; -> 00249C60 fn
002C1355  call     0x2c1800  ; -> 002C1800 fn
002C135A  call     0x2c38b0  ; -> 002C38B0 fn
002C135F  call     0x2c4720  ; -> 002C4720 fn
002C1364  xor      eax, eax
002C1366  add      rsp, 0x28
002C136A  ret      
```

## 002D0270 (13 B, extent 002D0270-002D027D)

Page context: "erer consumes.  Interior anchor '002D0300' (function '002D02C0').  '002D03B0' (83 B) is the enumeration shim paired with '002D02C0': under a stack cookie it invokes '00249CE0' on 'rcx' with callback '002D0270', a local 4-byte state slot and bound 'r8d = 4' - the fixed four-item iteration the license-grid callers run per pull.  Interior anchor '002D03E6' (function '002D03B0').  '002845E0' (472 B) is the license-board link fixup '00283E40"

```
002D0270  movsx    r8d, byte ptr [rcx + 1]
002D0275  movsx    eax, byte ptr [rdx + 1]
002D0279  sub      eax, r8d
002D027C  ret      
```

## 002D6680 (20 B, extent 002D6680-002D6694)

Page context: "ble**; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).  **Input — consumed by this page (2 edges).** '0055F3E0' and '00560070' call '002D6620'/'002D6680' — the input-read leaves the directional arms share.  **Presentation — consumed by this page (1 edge).** '0055CD40' calls '003B2D80', the menu-effect registry entry the grid uses for its effect teardown — the same registry family t"

```
002D6680  mov      rax, qword ptr [rip + 0x2cc0d1a]  ; -> 02F973A1
002D6687  test     al, al
002D6689  movzx    eax, al
002D668C  jne      0x2d6693  ; -> 002D6693
002D668E  mov      eax, 8
002D6693  ret      
```

## 00556570 (15 B, extent 00556570-0055657F)

Page context: "uare the predicate accepts to 'n' when it is lower ('0055E499'..'0055E4B6'), skipping '0xFFFF' squares; it runs with 'n = 4' over squares with bit 13 ('00556580') and 'n = 1' over every real square ('00556570').  **So the nibble alphabet is '{0, 1, 4, 5}'**, exactly the values the driver distinguishes (UQ-153's narrowing): **0** blank or hidden, **1** a licence out of reach, **4** a licence next to one the character owns — the state tha"

```
00556570  xor      eax, eax
00556572  mov      edx, 0xffff
00556577  cmp      word ptr [rcx + 8], dx
0055657B  setne    al
0055657E  ret      
```

## 00556580 (10 B, extent 00556580-0055658A)

Page context: "urrent nibble of the four neighbours of every square the predicate accepts to 'n' when it is lower ('0055E499'..'0055E4B6'), skipping '0xFFFF' squares; it runs with 'n = 4' over squares with bit 13 ('00556580') and 'n = 1' over every real square ('00556570').  **So the nibble alphabet is '{0, 1, 4, 5}'**, exactly the values the driver distinguishes (UQ-153's narrowing): **0** blank or hidden, **1** a licence out of reach, **4** a licenc"

```
00556580  mov      eax, dword ptr [rcx + 0x18]
00556583  shr      eax, 0xd
00556586  and      eax, 1
00556589  ret      
```

## 00558CE0 (386 B, extent 00558CE0-00558E62)

Page context: " 'id-0x9E <= 0x17' Quickening arm — before '002D48C0([+0xC0], r15d or 1)' posts the count.  Interior anchor '00559FEB' (function '00559E30').  '00558E70' (174 B) is the text-record setter '00557DB0'/'00558CE0' run: '00282DF0([+0xC8])' resolves the record, '003236B0'/'00323670'/'00323630' map its '+0x60' byte; a non-0xFF result sets bit 0 of '[+0x60]''s '+0x18' record's '+8', replaces it with '00556380(base+0x60, bpl, al, -2)''s return, "

```
00558CE0  mov      qword ptr [rsp + 0x10], rbx
00558CE5  push     rsi
00558CE6  sub      rsp, 0x20
00558CEA  mov      rsi, rcx
00558CED  mov      ecx, dword ptr [rdx]
00558CEF  sub      ecx, 1
00558CF2  je       0x558d50  ; -> 00558D50
00558CF4  sub      ecx, 1
00558CF7  je       0x558e55  ; -> 00558E55
00558CFD  cmp      ecx, 0x10
00558D00  je       0x558d14  ; -> 00558D14
00558D02  mov      rcx, rsi
00558D05  mov      rbx, qword ptr [rsp + 0x38]
00558D0A  add      rsp, 0x20
00558D0E  pop      rsi
00558D0F  jmp      0x5c5230  ; -> 005C5230 fn
00558D14  cmp      dword ptr [rip + 0x275095d], 0  ; -> 02CA9678
00558D1B  je       0x558e55  ; -> 00558E55
00558D21  mov      rcx, qword ptr [rip + 0x1b41ef0]  ; -> 0209AC18
00558D28  xor      ebx, ebx
00558D2A  mov      qword ptr [rip + 0x27502af], rbx  ; -> 02CA8FE0
00558D31  test     rcx, rcx
00558D34  je       0x558d3d  ; -> 00558D3D
00558D36  xor      edx, edx
00558D38  call     0x247730  ; -> 00247730 fn
00558D3D  mov      dword ptr [rip + 0x2750935], ebx  ; -> 02CA9678
00558D43  xor      eax, eax
00558D45  mov      rbx, qword ptr [rsp + 0x38]
00558D4A  add      rsp, 0x20
00558D4E  pop      rsi
00558D4F  ret      
00558D50  mov      rax, qword ptr [rip + 0x1b41ed9]  ; -> 0209AC30
00558D57  lea      rcx, [rsi + 0x50]
00558D5B  mov      rbx, qword ptr [rdx + 8]
00558D5F  mov      r9, rsi
00558D62  mov      r8d, 1
00558D68  mov      qword ptr [rsp + 0x30], rdi
00558D6D  mov      rdx, qword ptr [rax + 0x98]
00558D74  call     0x2432b0  ; -> 002432B0 fn
00558D79  movzx    ecx, word ptr [rax + 0xa]
00558D7D  movzx    edx, word ptr [rax + 8]
00558D81  movsx    r8d, word ptr [rax + 6]
00558D86  test     rsi, rsi
00558D89  je       0x558dac  ; -> 00558DAC
00558D8B  movzx    eax, word ptr [rax + 4]
00558D8F  mov      word ptr [rsi + 0x98], ax
00558D96  mov      word ptr [rsi + 0x9a], r8w
00558D9E  mov      word ptr [rsi + 0x9c], dx
00558DA5  mov      word ptr [rsi + 0x9e], cx
00558DAC  lea      rdx, [rip + 0x7ca27d]  ; -> 00D23030
00558DB3  mov      rcx, rsi
00558DB6  call     0x247570  ; -> 00247570 fn
00558DBB  mov      rax, qword ptr [rbx]
00558DBE  mov      qword ptr [rsi + 0xc0], rax
00558DC5  mov      ecx, dword ptr [rax + 0x354]
00558DCB  mov      dword ptr [rsi + 0xc8], ecx
00558DD1  call     0x282df0  ; -> 00282DF0 fn
00558DD6  mov      rcx, qword ptr [rsi + 0x60]
00558DDA  mov      rdi, rax
00558DDD  movsx    edx, word ptr [rax + 0x60]
00558DE1  mov      rbx, qword ptr [rcx + 0x10]
00558DE5  mov      ecx, 2
00558DEA  call     0x35d330  ; -> 0035D330 fn
00558DEF  xor      edx, edx
00558DF1  mov      rcx, qword ptr [rax + 0x18]
00558DF5  call     0x2b58b0  ; -> 002B58B0 fn
00558DFA  xor      ecx, ecx
00558DFC  mov      qword ptr [rbx + 0x18], rax
00558E00  call     0x20e620  ; -> 0020E620 fn
00558E05  mov      dword ptr [rbx + 0x20], eax
00558E08  mov      rax, qword ptr [rsi + 0x60]
00558E0C  movsx    ecx, word ptr [rdi + 0x60]
00558E10  mov      rbx, qword ptr [rax + 8]
00558E14  call     0x2c9bd0  ; -> 002C9BD0 fn
00558E19  mov      rcx, qword ptr [rbx + 0x20]
00558E1D  movsxd   r8, eax
00558E20  movzx    r8d, byte ptr [rcx + r8*8 + 7]
00558E26  mov      rcx, rsi
00558E29  mov      byte ptr [rbx + 0x39], r8b
00558E2D  mov      word ptr [rbx + 0xa], ax
00558E31  call     0x558e70  ; -> 00558E70 fn
00558E36  mov      edx, 0x5f
00558E3B  mov      rcx, rsi
00558E3E  call     0x247930  ; -> 00247930 fn
00558E43  mov      edx, 1
00558E48  mov      rcx, rsi
00558E4B  call     0x247730  ; -> 00247730 fn
00558E50  mov      rdi, qword ptr [rsp + 0x30]
00558E55  xor      eax, eax
00558E57  mov      rbx, qword ptr [rsp + 0x38]
00558E5C  add      rsp, 0x20
00558E60  pop      rsi
00558E61  ret      
```
