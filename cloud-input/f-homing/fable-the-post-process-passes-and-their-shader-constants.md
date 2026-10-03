# F homing pack (FABLE): `22-Middleware-PhyreEngine/Post-Process-Chain/the-post-process-passes-and-their-shader-constants.md`

Generated 2026-10-03 04:02 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 7. No bearing page cites them and no documented function calls them directly.

## 001653B0 (42 B, extent 001653B0-001653DA)

Documented callee on this page: `00662A80`

```
001653B0  sub      rsp, 0x38
001653B4  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001653BD  lea      rcx, [rip + 0x1dc949c]  ; -> 01F2E860
001653C4  call     0x662a80  ; -> 00662A80 fn
001653C9  nop      
001653CA  lea      rcx, [rip + 0x74b2bf]  ; -> 008B0690
001653D1  add      rsp, 0x38
001653D5  jmp      0x808b90  ; -> 00808B90 fn
```

## 001694E0 (39 B, extent 001694E0-00169507)

Documented callee on this page: `005DBF60`

```
001694E0  sub      rsp, 0x28
001694E4  lea      rdx, [rip + 0x2d3c365]  ; -> 02EA5850
001694EB  lea      rcx, [rip + 0x2d3c346]  ; -> 02EA5838
001694F2  call     0x5dbf60  ; -> 005DBF60 fn
001694F7  lea      rcx, [rip + 0x74e682]  ; -> 008B7B80
001694FE  add      rsp, 0x28
00169502  jmp      0x808b90  ; -> 00808B90 fn
```

## 001EEC50 (41 B, extent 001EEC50-001EEC79)

Documented callee on this page: `0063ABF0`

```
001EEC50  test     rcx, rcx
001EEC53  je       0x1eec78  ; -> 001EEC78
001EEC55  cmp      byte ptr [rcx + 8], 0
001EEC59  jne      0x1eec6a  ; -> 001EEC6A
001EEC5B  mov      rdx, qword ptr [rcx]
001EEC5E  mov      rcx, qword ptr [rip + 0x1d941eb]  ; -> 01F82E50
001EEC65  jmp      0x63abf0  ; -> 0063ABF0 fn
001EEC6A  mov      rcx, qword ptr [rip + 0x1d941df]  ; -> 01F82E50
001EEC71  xor      edx, edx
001EEC73  jmp      0x63abf0  ; -> 0063ABF0 fn
001EEC78  ret      
```

## 004C0EA0 (4501 B, extent 004C0EA0-004C2035)

Documented callee on this page: `00182EE0`

```
004C0EA0  mov      rax, rsp
004C0EA3  mov      qword ptr [rax + 8], rbx
004C0EA7  push     rbp
004C0EA8  push     rsi
004C0EA9  push     rdi
004C0EAA  push     r12
004C0EAC  push     r13
004C0EAE  push     r14
004C0EB0  push     r15
004C0EB2  lea      rbp, [rax - 0x268]
004C0EB9  sub      rsp, 0x330
004C0EC0  movaps   xmmword ptr [rax - 0x48], xmm6
004C0EC4  mov      r15, rdx
004C0EC7  movaps   xmmword ptr [rax - 0x58], xmm7
004C0ECB  mov      r12, rcx
004C0ECE  movaps   xmmword ptr [rax - 0x68], xmm8
004C0ED3  movaps   xmmword ptr [rax - 0x78], xmm9
004C0ED8  movaps   xmmword ptr [rax - 0x88], xmm10
004C0EE0  movaps   xmmword ptr [rax - 0x98], xmm11
004C0EE8  movaps   xmmword ptr [rax - 0xa8], xmm12
004C0EF0  movaps   xmmword ptr [rax - 0xb8], xmm13
004C0EF8  movaps   xmmword ptr [rax - 0xc8], xmm14
004C0F00  movaps   xmmword ptr [rax - 0xd8], xmm15
004C0F08  call     0x182ee0  ; -> 00182EE0 fn
004C0F0D  mulss    xmm0, dword ptr [rip + 0x182ac53]  ; -> 01CEBB68 [f32 0.25]
004C0F15  mulss    xmm0, dword ptr [rip + 0x4321ff]  ; -> 008F311C [f32 3]
004C0F1D  call     0x861f14  ; -> 00861F14 fn
004C0F22  xor      edx, edx
004C0F24  movss    dword ptr [rsp + 0x40], xmm0
004C0F2A  mov      r8d, 0x200
004C0F30  lea      rcx, [rbp - 0x80]
004C0F34  call     0x861ec0  ; -> 00861EC0 fn
004C0F39  movss    xmm6, dword ptr [rip + 0x182ad0f]  ; -> 01CEBC50 [f32 3.141593]
004C0F41  lea      r13, [rip + 0x1ba3ee8]  ; -> 02064E30
004C0F48  movss    xmm5, dword ptr [rip + 0x182ad28]  ; -> 01CEBC78 [f32 6.283185]
004C0F50  xor      eax, eax
004C0F52  movss    xmm10, dword ptr [rip + 0x404be5]  ; -> 008C5B40 [f32 255]
004C0F5B  mov      r8d, 0x3ff
004C0F61  movsx    r9d, ax
004C0F65  xorps    xmm7, xmm7
004C0F68  mov      qword ptr [rip + 0x27e6fd9], rax  ; -> 02CA7F48
004C0F6F  cmp      r9d, 0x400
004C0F76  mov      qword ptr [rip + 0x27e6fd3], rax  ; -> 02CA7F50
004C0F7D  mov      ecx, r9d
004C0F80  cmovge   ecx, r8d
004C0F84  mov      qword ptr [rip + 0x27e6fb5], rax  ; -> 02CA7F40
004C0F8B  mov      qword ptr [rip + 0x27e6fc6], rax  ; -> 02CA7F58
004C0F92  xor      edi, edi
004C0F94  mov      qword ptr [rip + 0x27e6fc5], rax  ; -> 02CA7F60
004C0F9B  test     ecx, ecx
004C0F9D  mov      qword ptr [rip + 0x27e6fc4], rax  ; -> 02CA7F68
004C0FA4  movzx    r14d, di
004C0FA8  mov      qword ptr [rip + 0x27e6fc1], rax  ; -> 02CA7F70
004C0FAF  mov      qword ptr [rip + 0x27e6fc2], rax  ; -> 02CA7F78
004C0FB6  cmovns   eax, ecx
004C0FB9  shl      eax, 4
004C0FBC  movsxd   rcx, eax
004C0FBF  mov      eax, edi
004C0FC1  mov      word ptr [rip + 0x27e6f84], di  ; -> 02CA7F4C
004C0FC8  mov      word ptr [rip + 0x27e6f89], di  ; -> 02CA7F58
004C0FCF  movups   xmm0, xmmword ptr [rcx + r13]
004C0FD4  movups   xmm1, xmmword ptr [rcx + r13 + 0x10]
004C0FDA  lea      ecx, [r9 + 2]
004C0FDE  cmp      ecx, 0x400
004C0FE4  movaps   xmmword ptr [rbp - 0x70], xmm0
004C0FE8  movaps   xmmword ptr [rbp - 0x60], xmm1
004C0FEC  movss    xmm8, dword ptr [rbp - 0x5c]
004C0FF2  cmovge   ecx, r8d
004C0FF6  movss    xmm9, dword ptr [rbp - 0x60]
004C0FFC  test     ecx, ecx
004C0FFE  cmovns   eax, ecx
004C1001  shl      eax, 4
004C1004  cdqe     
004C1006  movzx    ecx, word ptr [rax + r13 + 4]
004C100C  mov      eax, 0xbb
004C1011  mov      word ptr [rip + 0x27e6f2c], ax  ; -> 02CA7F44
004C1018  mov      eax, 0xbc
004C101D  mov      word ptr [rip + 0x27e6f24], ax  ; -> 02CA7F48
004C1024  mov      eax, 0xb9
004C1029  mov      word ptr [rip + 0x27e6f24], ax  ; -> 02CA7F54
004C1030  mov      word ptr [rip + 0x27e6f19], cx  ; -> 02CA7F50
004C1037  test     cx, cx
004C103A  jle      0x4c1768  ; -> 004C1768
004C1040  movsx    edx, r14w
004C1044  mov      eax, edi
004C1046  lea      ecx, [rdx + 0x34]
004C1049  cmp      ecx, 0x400
004C104F  cmovge   ecx, r8d
004C1053  test     ecx, ecx
004C1055  cmovns   eax, ecx
004C1058  add      edx, 0x33
004C105B  shl      eax, 4
004C105E  movsxd   rcx, eax
004C1061  cmp      edx, 0x400
004C1067  mov      eax, edi
004C1069  movups   xmm2, xmmword ptr [rcx + r13]
004C106E  movups   xmm0, xmmword ptr [rcx + r13 + 0x10]
004C1074  mov      ecx, edx
004C1076  cmovge   ecx, r8d
004C107A  movaps   xmmword ptr [rbp - 0x40], xmm2
004C107E  movaps   xmmword ptr [rbp - 0x30], xmm0
004C1082  test     ecx, ecx
004C1084  movd     xmm11, dword ptr [rbp - 0x24]
004C108A  movd     xmm12, dword ptr [rbp - 0x2c]
004C1090  cmovns   eax, ecx
004C1093  movd     xmm13, dword ptr [rbp - 0x28]
004C1099  shl      eax, 4
004C109C  cdqe     
004C109E  cmp      edx, 0x400
004C10A4  cvtdq2ps xmm11, xmm11
004C10A8  cmovge   edx, r8d
004C10AC  test     edx, edx
004C10AE  movzx    esi, word ptr [rax + r13]
004C10B3  mov      eax, edi
004C10B5  cmovns   eax, edx
004C10B8  shl      eax, 4
004C10BB  cdqe     
004C10BD  cvtdq2ps xmm12, xmm12
004C10C1  movzx    ebx, word ptr [rax + r13 + 4]
004C10C7  movd     eax, xmm0
004C10CB  movaps   xmm0, xmm2
004C10CE  addss    xmm0, xmm6
004C10D2  movaps   xmm6, xmm2
004C10D5  shufps   xmm2, xmm2, 0xff
004C10D9  cvtdq2ps xmm13, xmm13
004C10DD  divss    xmm0, xmm5
004C10E1  movd     xmm14, eax
004C10E6  cvttss2si eax, xmm0
004C10EA  cvtdq2ps xmm14, xmm14
004C10EE  movd     xmm1, eax
004C10F2  cvtdq2ps xmm1, xmm1
004C10F5  mulss    xmm11, xmm2
004C10FA  mulss    xmm1, xmm5
004C10FE  subss    xmm6, xmm1
004C1102  movaps   xmm0, xmm6
004C1105  call     0x861f0e  ; -> 00861F0E fn
004C110A  movss    dword ptr [rbp + 0x280], xmm0
004C1112  movaps   xmm0, xmm6
004C1115  call     0x861f08  ; -> 00861F08 fn
004C111A  comiss   xmm7, xmm14
004C111E  movaps   xmm15, xmm0
004C1122  jbe      0x4c1128  ; -> 004C1128
004C1124  movaps   xmm14, xmm7
004C1128  comiss   xmm7, xmm12
004C112C  jbe      0x4c1132  ; -> 004C1132
004C112E  movaps   xmm12, xmm7
004C1132  comiss   xmm7, xmm13
004C1136  jbe      0x4c113c  ; -> 004C113C
004C1138  movaps   xmm13, xmm7
004C113C  comiss   xmm7, xmm11
004C1140  jbe      0x4c1146  ; -> 004C1146
004C1142  movaps   xmm11, xmm7
004C1146  comiss   xmm14, xmm10
004C114A  jbe      0x4c1150  ; -> 004C1150
004C114C  movaps   xmm14, xmm10
004C1150  comiss   xmm12, xmm10
004C1154  jbe      0x4c115a  ; -> 004C115A
004C1156  movaps   xmm12, xmm10
004C115A  comiss   xmm13, xmm10
004C115E  jbe      0x4c1164  ; -> 004C1164
004C1160  movaps   xmm13, xmm10
004C1164  comiss   xmm11, xmm10
004C1168  jbe      0x4c116e  ; -> 004C116E
004C116A  movaps   xmm11, xmm10
004C116E  movss    xmm0, dword ptr [rbp - 0x3c]
004C1173  add      r14w, 3
004C1178  cvttss2si eax, xmm14
004C117D  mov      word ptr [rip + 0x27e6dd3], r14w  ; -> 02CA7F58
004C1185  mov      r14d, 0x3ff
004C118B  movaps   xmm1, xmm0
004C118E  mulss    xmm15, xmm0
004C1193  mov      dword ptr [rbp - 0x30], eax
004C1196  xorps    xmm1, xmmword ptr [rip + 0x182ac03]  ; -> 01CEBDA0 [f32x4 -0, -0, -0, -0]
004C119D  cvttss2si eax, xmm12
004C11A2  movss    xmm12, dword ptr [rbp + 0x280]
004C11AB  mov      dword ptr [rbp - 0x2c], eax
004C11AE  cvttss2si eax, xmm13
004C11B3  movss    dword ptr [rbp + 0x288], xmm15
004C11BC  mov      dword ptr [rbp - 0x28], eax
004C11BF  cvttss2si eax, xmm11
004C11C4  movaps   xmm11, xmm12
004C11C8  mulss    xmm12, xmm1
004C11CD  mov      dword ptr [rbp - 0x24], eax
004C11D0  mulss    xmm11, xmm0
004C11D5  movss    dword ptr [rbp + 0x280], xmm12
004C11DE  movss    dword ptr [rsp + 0x30], xmm11
004C11E5  nop      word ptr [rax + rax]
004C11F0  movsx    ecx, si
004C11F3  mov      eax, edi
004C11F5  add      ecx, 0x39
004C11F8  cmp      ecx, 0x400
004C11FE  cmovge   ecx, r14d
004C1202  test     ecx, ecx
004C1204  cmovns   eax, ecx
004C1207  dec      bx
004C120A  shl      eax, 4
004C120D  movsxd   rcx, eax
004C1210  add      si, 4
004C1214  mov      word ptr [rip + 0x27e6d51], bx  ; -> 02CA7F6C
004C121B  mov      word ptr [rip + 0x27e6d46], si  ; -> 02CA7F68
004C1222  movups   xmm1, xmmword ptr [rcx + r13]
004C1227  movups   xmm2, xmmword ptr [rcx + r13 + 0x10]
004C122D  movups   xmm3, xmmword ptr [rcx + r13 + 0x20]
004C1233  movups   xmm4, xmmword ptr [rcx + r13 + 0x30]
004C1239  movaps   xmm0, xmm1
004C123C  movaps   xmmword ptr [rbp + 0xc0], xmm1
004C1243  mulss    xmm0, xmm15
004C1248  movaps   xmm6, xmm1
004C124B  shufps   xmm6, xmm1, 0x55
004C124F  movaps   xmm10, xmm2
004C1253  mulss    xmm1, xmm11
004C1258  movaps   xmm5, xmm6
004C125B  mulss    xmm5, xmm12
004C1260  mulss    xmm6, xmm15
004C1265  addss    xmm5, xmm0
004C1269  shufps   xmm10, xmm2, 0x55
004C126E  movaps   xmm13, xmm10
004C1272  movaps   xmmword ptr [rbp + 0xd0], xmm2
004C1279  mulss    xmm13, xmm12
004C127E  addss    xmm6, xmm1
004C1282  movss    xmm1, dword ptr [rbp - 0x70]
004C1287  movaps   xmm0, xmm2
004C128A  mulss    xmm0, xmm15
004C128F  mulss    xmm10, xmm15
004C1294  addss    xmm13, xmm0
004C1299  mulss    xmm2, xmm11
004C129E  movaps   xmm11, xmm3
004C12A2  movaps   xmmword ptr [rbp + 0xe0], xmm3
004C12A9  shufps   xmm11, xmm3, 0x55
004C12AE  movaps   xmm0, xmm3
004C12B1  mulss    xmm3, dword ptr [rsp + 0x30]
004C12B7  addss    xmm10, xmm2
004C12BC  mulss    xmm0, xmm15
004C12C1  movaps   xmm14, xmm11
004C12C5  mulss    xmm14, xmm12
004C12CA  movaps   xmm12, xmm4
004C12CE  mulss    xmm11, xmm15
004C12D3  shufps   xmm12, xmm4, 0x55
004C12D8  addss    xmm14, xmm0
004C12DD  movaps   xmm15, xmm12
004C12E1  movaps   xmmword ptr [rbp + 0xf0], xmm4
004C12E8  mulss    xmm15, dword ptr [rbp + 0x280]
004C12F1  addss    xmm11, xmm3
004C12F6  mulss    xmm12, dword ptr [rbp + 0x288]
004C12FF  movaps   xmm0, xmm4
004C1302  mulss    xmm0, dword ptr [rbp + 0x288]
004C130A  mulss    xmm4, dword ptr [rsp + 0x30]
004C1310  addss    xmm15, xmm0
004C1315  movss    xmm0, dword ptr [rsp + 0x40]
004C131B  divss    xmm5, xmm0
004C131F  divss    xmm13, xmm0
004C1324  mulss    xmm6, xmm0
004C1328  addss    xmm5, xmm1
004C132C  mulss    xmm10, xmm0
004C1331  addss    xmm12, xmm4
004C1336  divss    xmm14, xmm0
004C133B  mulss    xmm11, xmm0
004C1340  addss    xmm13, xmm1
004C1345  divss    xmm15, xmm0
004C134A  mulss    xmm12, xmm0
004C134F  movss    xmm0, dword ptr [rbp - 0x6c]
004C1354  addss    xmm6, xmm0
004C1358  movss    dword ptr [rsp + 0x20], xmm5
004C135E  addss    xmm10, xmm0
004C1363  movss    dword ptr [rbp + 0x100], xmm5
004C136B  movss    dword ptr [rbp + 0x110], xmm13
004C1374  movss    dword ptr [rbp + 0x104], xmm6
004C137C  movss    dword ptr [rbp + 0x114], xmm10
004C1385  addss    xmm14, xmm1
004C138A  addss    xmm11, xmm0
004C138F  addss    xmm15, xmm1
004C1394  addss    xmm12, xmm0
004C1399  movss    dword ptr [rbp + 0x120], xmm14
004C13A2  movss    dword ptr [rbp + 0x124], xmm11
004C13AB  movss    dword ptr [rbp + 0x130], xmm15
004C13B4  movss    dword ptr [rbp + 0x134], xmm12
004C13BD  call     0x39d1f0  ; -> 0039D1F0 fn
004C13C2  movsx    r9d, word ptr [rip + 0x27e6b76]  ; -> 02CA7F40
004C13CA  mov      eax, edi
004C13CC  movss    dword ptr [rbp + 0x108], xmm0
004C13D4  movss    dword ptr [rbp + 0x118], xmm0
004C13DC  movss    dword ptr [rbp + 0x128], xmm0
004C13E4  lea      edx, [r9 + 2]
004C13E8  movss    dword ptr [rbp + 0x138], xmm0
004C13F0  movss    xmm0, dword ptr [rsp + 0x20]
004C13F6  cmp      edx, 0x400
004C13FC  mov      ecx, edx
004C13FE  mov      dword ptr [rbp + 0x12c], 0x3f800000
004C1408  cmovge   ecx, r14d
004C140C  mov      dword ptr [rbp + 0x13c], 0x3f800000
004C1416  test     ecx, ecx
004C1418  cmovns   eax, ecx
004C141B  shl      eax, 4
004C141E  cdqe     
004C1420  cmp      edx, 0x400
004C1426  cmovge   edx, r14d
004C142A  test     edx, edx
004C142C  mov      eax, dword ptr [rax + r13 + 0xc]
004C1431  mov      dword ptr [rbp + 0x10c], eax
004C1437  mov      eax, edi
004C1439  cmovns   eax, edx
004C143C  shl      eax, 4
004C143F  comiss   xmm7, xmm0
004C1442  cdqe     
004C1444  mov      eax, dword ptr [rax + r13 + 0xc]
004C1449  mov      dword ptr [rbp + 0x11c], eax
004C144F  ja       0x4c1701  ; -> 004C1701
004C1455  comiss   xmm0, xmm9
004C1459  ja       0x4c1701  ; -> 004C1701
004C145F  comiss   xmm7, xmm6
004C1462  ja       0x4c1701  ; -> 004C1701
004C1468  comiss   xmm6, xmm8
004C146C  ja       0x4c1701  ; -> 004C1701
004C1472  comiss   xmm7, xmm13
004C1476  ja       0x4c1701  ; -> 004C1701
004C147C  comiss   xmm13, xmm9
004C1480  ja       0x4c1701  ; -> 004C1701
004C1486  comiss   xmm7, xmm10
004C148A  ja       0x4c1701  ; -> 004C1701
004C1490  comiss   xmm10, xmm8
004C1494  ja       0x4c1701  ; -> 004C1701
004C149A  comiss   xmm7, xmm14
004C149E  ja       0x4c1701  ; -> 004C1701
004C14A4  comiss   xmm14, xmm9
004C14A8  ja       0x4c1701  ; -> 004C1701
004C14AE  comiss   xmm7, xmm11
004C14B2  ja       0x4c1701  ; -> 004C1701
004C14B8  comiss   xmm11, xmm8
004C14BC  ja       0x4c1701  ; -> 004C1701
004C14C2  comiss   xmm7, xmm15
004C14C6  ja       0x4c1701  ; -> 004C1701
004C14CC  comiss   xmm15, xmm9
004C14D0  ja       0x4c1701  ; -> 004C1701
004C14D6  comiss   xmm7, xmm12
004C14DA  ja       0x4c1701  ; -> 004C1701
004C14E0  comiss   xmm12, xmm8
004C14E4  ja       0x4c1701  ; -> 004C1701
004C14EA  movsx    r8d, word ptr [rip + 0x27e6a56]  ; -> 02CA7F48
004C14F2  mov      eax, edi
004C14F4  movaps   xmm0, xmmword ptr [rbp + 0x130]
004C14FB  movss    xmm1, dword ptr [rbp + 0xc8]
004C1503  movss    dword ptr [rbp + 0x130], xmm1
004C150B  movss    xmm1, dword ptr [rbp + 0xd8]
004C1513  lea      ecx, [r8 + 8]
004C1517  cmp      ecx, 0x400
004C151D  mov      dword ptr [rbp + 0x138], 0x3f800000
004C1527  cmovge   ecx, r14d
004C152B  test     ecx, ecx
004C152D  cmovns   eax, ecx
004C1530  lea      ecx, [r8 + 6]
004C1534  shl      eax, 4
004C1537  cdqe     
004C1539  cmp      ecx, 0x400
004C153F  cmovge   ecx, r14d
004C1543  test     ecx, ecx
004C1545  movups   xmmword ptr [rax + r13], xmm0
004C154A  mov      eax, edi
004C154C  movaps   xmm0, xmmword ptr [rbp + 0x120]
004C1553  cmovns   eax, ecx
004C1556  shl      eax, 4
004C1559  lea      ecx, [r8 + 2]
004C155D  cdqe     
004C155F  cmp      ecx, 0x400
004C1565  movss    dword ptr [rbp + 0x120], xmm1
004C156D  movss    xmm1, dword ptr [rbp + 0xe8]
004C1575  cmovge   ecx, r14d
004C1579  test     ecx, ecx
004C157B  mov      dword ptr [rbp + 0x128], 0x3f800000
004C1585  movups   xmmword ptr [rax + r13], xmm0
004C158A  mov      eax, edi
004C158C  movaps   xmm0, xmmword ptr [rbp + 0x100]
004C1593  cmovns   eax, ecx
004C1596  shl      eax, 4
004C1599  lea      ecx, [r8 + 4]
004C159D  cdqe     
004C159F  cmp      ecx, 0x400
004C15A5  movss    dword ptr [rbp + 0x100], xmm1
004C15AD  movss    xmm1, dword ptr [rbp + 0xf8]
004C15B5  cmovge   ecx, r14d
004C15B9  test     ecx, ecx
004C15BB  mov      dword ptr [rbp + 0x108], 0x3f800000
004C15C5  movups   xmmword ptr [rax + r13], xmm0
004C15CA  mov      eax, edi
004C15CC  movaps   xmm0, xmmword ptr [rbp + 0x110]
004C15D3  cmovns   eax, ecx
004C15D6  shl      eax, 4
004C15D9  lea      ecx, [r8 + 1]
004C15DD  cdqe     
004C15DF  cmp      ecx, 0x400
004C15E5  movss    dword ptr [rbp + 0x110], xmm1
004C15ED  movss    xmm1, dword ptr [rbp + 0xdc]
004C15F5  cmovge   ecx, r14d
004C15F9  test     ecx, ecx
004C15FB  movss    dword ptr [rbp + 0x124], xmm1
004C1603  movss    xmm1, dword ptr [rbp + 0xfc]
004C160B  movups   xmmword ptr [rax + r13], xmm0
004C1610  mov      eax, edi
004C1612  mov      dword ptr [rbp + 0x118], 0x3f800000
004C161C  movaps   xmm0, xmmword ptr [rbp - 0x30]
004C1620  cmovns   eax, ecx
004C1623  inc      word ptr [rip + 0x27e6922]  ; -> 02CA7F4C
004C162A  add      r8w, 9
004C162F  shl      eax, 4
004C1632  cdqe     
004C1634  movsx    edx, r8w
004C1638  movss    dword ptr [rbp + 0x114], xmm1
004C1640  mov      word ptr [rip + 0x27e6900], r8w  ; -> 02CA7F48
004C1648  movups   xmmword ptr [rax + r13], xmm0
004C164D  lea      ecx, [rdx - 9]
004C1650  mov      eax, edi
004C1652  movss    xmm0, dword ptr [rbp + 0xcc]
004C165A  cmp      ecx, 0x400
004C1660  movss    dword ptr [rbp + 0x134], xmm0
004C1668  movss    xmm0, dword ptr [rbp + 0xec]
004C1670  cmovge   ecx, r14d
004C1674  test     ecx, ecx
004C1676  movss    dword ptr [rbp + 0x104], xmm0
004C167E  cmovns   eax, ecx
004C1681  movaps   xmm0, xmmword ptr [rbp + 0x130]
004C1688  lea      ecx, [rdx - 6]
004C168B  shl      eax, 4
004C168E  cdqe     
004C1690  cmp      ecx, 0x400
004C1696  cmovge   ecx, r14d
004C169A  test     ecx, ecx
004C169C  movups   xmmword ptr [rax + r13], xmm0
004C16A1  mov      eax, edi
004C16A3  movaps   xmm0, xmmword ptr [rbp + 0x120]
004C16AA  cmovns   eax, ecx
004C16AD  shl      eax, 4
004C16B0  lea      ecx, [rdx - 4]
004C16B3  cdqe     
004C16B5  cmp      ecx, 0x400
004C16BB  cmovge   ecx, r14d
004C16BF  test     ecx, ecx
004C16C1  movups   xmmword ptr [rax + r13], xmm0
004C16C6  mov      eax, edi
004C16C8  movaps   xmm0, xmmword ptr [rbp + 0x100]
004C16CF  cmovns   eax, ecx
004C16D2  shl      eax, 4
004C16D5  lea      ecx, [rdx - 2]
004C16D8  cdqe     
004C16DA  cmp      ecx, 0x400
004C16E0  cmovge   ecx, r14d
004C16E4  test     ecx, ecx
004C16E6  movups   xmmword ptr [rax + r13], xmm0
004C16EB  mov      eax, edi
004C16ED  movaps   xmm0, xmmword ptr [rbp + 0x110]
004C16F4  cmovns   eax, ecx
004C16F7  shl      eax, 4
004C16FA  cdqe     
004C16FC  movups   xmmword ptr [rax + r13], xmm0
004C1701  movzx    ebx, word ptr [rip + 0x27e6864]  ; -> 02CA7F6C
004C1708  test     bx, bx
004C170B  je       0x4c1732  ; -> 004C1732
004C170D  movzx    esi, word ptr [rip + 0x27e6854]  ; -> 02CA7F68
004C1714  movss    xmm15, dword ptr [rbp + 0x288]
004C171D  movss    xmm12, dword ptr [rbp + 0x280]
004C1726  movss    xmm11, dword ptr [rsp + 0x30]
004C172D  jmp      0x4c11f0  ; -> 004C11F0
004C1732  sub      word ptr [rip + 0x27e6816], 1  ; -> 02CA7F50
004C173A  movss    xmm10, dword ptr [rip + 0x4043fd]  ; -> 008C5B40 [f32 255]
004C1743  movss    xmm5, dword ptr [rip + 0x182a52d]  ; -> 01CEBC78 [f32 6.283185]
004C174B  movss    xmm6, dword ptr [rip + 0x182a4fd]  ; -> 01CEBC50 [f32 3.141593]
004C1753  je       0x4c176e  ; -> 004C176E
004C1755  movzx    r14d, word ptr [rip + 0x27e67fb]  ; -> 02CA7F58
004C175D  mov      r8d, 0x3ff
004C1763  jmp      0x4c1040  ; -> 004C1040
004C1768  mov      r14d, 0x3ff
004C176E  movss    xmm3, dword ptr [rbp - 0x70]
004C1773  mov      eax, edi
004C1775  movss    xmm4, dword ptr [rbp - 0x6c]
004C177A  subss    xmm3, dword ptr [rbp - 0x68]
004C177F  subss    xmm4, dword ptr [rbp - 0x64]
004C1784  movsx    r10d, r9w
004C1788  lea      ecx, [r10 + 2]
004C178C  cmp      ecx, 0x400
004C1792  cmovge   ecx, r14d
004C1796  test     ecx, ecx
004C1798  cmovns   eax, ecx
004C179B  shl      eax, 4
004C179E  cdqe     
004C17A0  movzx    ecx, word ptr [rax + r13]
004C17A5  mov      word ptr [rip + 0x27e67a4], cx  ; -> 02CA7F50
004C17AC  test     cx, cx
004C17AF  jle      0x4c1f82  ; -> 004C1F82
004C17B5  mulss    xmm3, dword ptr [rip + 0x43198b]  ; -> 008F3148 [f32 -2]
004C17BD  movzx    r14d, di
004C17C1  mulss    xmm4, dword ptr [rip + 0x43197f]  ; -> 008F3148 [f32 -2]
004C17C9  movss    dword ptr [rsp + 0x60], xmm3
004C17CF  movss    dword ptr [rsp + 0x70], xmm4
004C17D5  nop      word ptr [rax + rax]
004C17E0  mov      r8d, 0x3ff
004C17E6  movsx    edx, r14w
004C17EA  mov      eax, edi
004C17EC  lea      ecx, [rdx + 4]
004C17EF  cmp      ecx, 0x400
004C17F5  cmovge   ecx, r8d
004C17F9  test     ecx, ecx
004C17FB  cmovns   eax, ecx
004C17FE  add      edx, 3
004C1801  shl      eax, 4
004C1804  movsxd   rcx, eax
004C1807  cmp      edx, 0x400
004C180D  mov      eax, edi
004C180F  movups   xmm2, xmmword ptr [rcx + r13]
004C1814  movups   xmm0, xmmword ptr [rcx + r13 + 0x10]
004C181A  mov      ecx, edx
004C181C  cmovge   ecx, r8d
004C1820  movaps   xmmword ptr [rbp - 0x40], xmm2
004C1824  test     ecx, ecx
004C1826  movaps   xmmword ptr [rbp - 0x30], xmm0
004C182A  movd     xmm11, dword ptr [rbp - 0x24]
004C1830  movaps   xmm15, xmm2
004C1834  movd     xmm12, dword ptr [rbp - 0x2c]
004C183A  cmovns   eax, ecx
004C183D  movd     xmm13, dword ptr [rbp - 0x28]
004C1843  lea      ecx, [r10 + 1]
004C1847  shl      eax, 4
004C184A  cdqe     
004C184C  cmp      edx, 0x400
004C1852  shufps   xmm15, xmm2, 0xaa
004C1857  cmovge   edx, r8d
004C185B  movaps   xmm1, xmm15
004C185F  test     edx, edx
004C1861  mulss    xmm1, xmm3
004C1865  movzx    esi, word ptr [rax + r13]
004C186A  mov      eax, edi
004C186C  cmovns   eax, edx
004C186F  mulss    xmm15, xmm4
004C1874  shl      eax, 4
004C1877  cdqe     
004C1879  cmp      ecx, 0x400
004C187F  movss    dword ptr [rsp + 0x30], xmm1
004C1885  cmovge   ecx, r8d
004C1889  test     ecx, ecx
004C188B  movzx    ebx, word ptr [rax + r13 + 4]
004C1891  mov      eax, edi
004C1893  cmovns   eax, ecx
004C1896  shl      eax, 4
004C1899  cdqe     
004C189B  cvtdq2ps xmm11, xmm11
004C189F  mov      eax, dword ptr [rax + r13 + 8]
004C18A4  mov      dword ptr [rbp + 0x98], eax
004C18AA  movd     eax, xmm0
004C18AE  movaps   xmm0, xmm2
004C18B1  addss    xmm0, xmm6
004C18B5  movaps   xmm6, xmm2
004C18B8  shufps   xmm2, xmm2, 0xff
004C18BC  mulss    xmm11, xmm2
004C18C1  cvtdq2ps xmm12, xmm12
004C18C5  mulss    xmm11, dword ptr [rbp + 0x98]
004C18CE  divss    xmm0, xmm5
004C18D2  movd     xmm14, eax
004C18D7  cvttss2si eax, xmm0
004C18DB  cvtdq2ps xmm14, xmm14
004C18DF  movd     xmm1, eax
004C18E3  cvtdq2ps xmm1, xmm1
004C18E6  cvtdq2ps xmm13, xmm13
004C18EA  mulss    xmm1, xmm5
004C18EE  subss    xmm6, xmm1
004C18F2  movaps   xmm0, xmm6
004C18F5  call     0x861f0e  ; -> 00861F0E fn
004C18FA  movss    dword ptr [rsp + 0x20], xmm0
004C1900  movaps   xmm0, xmm6
004C1903  call     0x861f08  ; -> 00861F08 fn
004C1908  comiss   xmm7, xmm14
004C190C  movss    dword ptr [rbp + 0x280], xmm0
004C1914  jbe      0x4c191a  ; -> 004C191A
004C1916  movaps   xmm14, xmm7
004C191A  comiss   xmm7, xmm12
004C191E  jbe      0x4c1924  ; -> 004C1924
004C1920  movaps   xmm12, xmm7
004C1924  comiss   xmm7, xmm13
004C1928  jbe      0x4c192e  ; -> 004C192E
004C192A  movaps   xmm13, xmm7
004C192E  comiss   xmm7, xmm11
004C1932  jbe      0x4c1938  ; -> 004C1938
004C1934  movaps   xmm11, xmm7
004C1938  comiss   xmm14, xmm10
004C193C  jbe      0x4c1942  ; -> 004C1942
004C193E  movaps   xmm14, xmm10
004C1942  comiss   xmm12, xmm10
004C1946  jbe      0x4c194c  ; -> 004C194C
004C1948  movaps   xmm12, xmm10
004C194C  comiss   xmm13, xmm10
004C1950  jbe      0x4c1956  ; -> 004C1956
004C1952  movaps   xmm13, xmm10
004C1956  comiss   xmm11, xmm10
004C195A  jbe      0x4c1960  ; -> 004C1960
004C195C  movaps   xmm11, xmm10
004C1960  movss    xmm0, dword ptr [rsp + 0x30]
004C1966  add      r14w, 3
004C196B  addss    xmm15, dword ptr [rbp - 0x6c]
004C1971  addss    xmm0, dword ptr [rbp - 0x70]
004C1976  cvttss2si eax, xmm14
004C197B  mov      word ptr [rip + 0x27e65d5], r14w  ; -> 02CA7F58
004C1983  mov      r14d, 0x3ff
004C1989  movaps   xmmword ptr [rbp + 0x180], xmm15
004C1991  mov      dword ptr [rbp - 0x30], eax
004C1994  cvttss2si eax, xmm12
004C1999  movss    xmm12, dword ptr [rbp + 0x280]
004C19A2  mov      dword ptr [rbp - 0x2c], eax
004C19A5  cvttss2si eax, xmm13
004C19AA  movss    dword ptr [rsp + 0x30], xmm0
004C19B0  movss    xmm0, dword ptr [rbp - 0x3c]
004C19B5  mov      dword ptr [rbp - 0x28], eax
004C19B8  movaps   xmm1, xmm0
004C19BB  xorps    xmm1, xmmword ptr [rip + 0x182a3de]  ; -> 01CEBDA0 [f32x4 -0, -0, -0, -0]
004C19C2  cvttss2si eax, xmm11
004C19C7  movss    xmm11, dword ptr [rsp + 0x20]
004C19CE  movaps   xmm15, xmm11
004C19D2  mulss    xmm12, xmm0
004C19D7  mov      dword ptr [rbp - 0x24], eax
004C19DA  mulss    xmm15, xmm0
004C19DF  mulss    xmm11, xmm1
004C19E4  movss    dword ptr [rbp + 0x288], xmm15
004C19ED  movss    dword ptr [rbp + 0x280], xmm12
004C19F6  movss    dword ptr [rsp + 0x20], xmm11
004C19FD  nop      dword ptr [rax]
004C1A00  movsx    ecx, si
004C1A03  mov      eax, edi
004C1A05  add      ecx, 0x39
004C1A08  cmp      ecx, 0x400
004C1A0E  cmovge   ecx, r14d
004C1A12  test     ecx, ecx
004C1A14  cmovns   eax, ecx
004C1A17  dec      bx
004C1A1A  shl      eax, 4
004C1A1D  movsxd   rcx, eax
004C1A20  add      si, 4
004C1A24  mov      word ptr [rip + 0x27e6541], bx  ; -> 02CA7F6C
004C1A2B  mov      word ptr [rip + 0x27e6536], si  ; -> 02CA7F68
004C1A32  movups   xmm1, xmmword ptr [rcx + r13]
004C1A37  movups   xmm2, xmmword ptr [rcx + r13 + 0x10]
004C1A3D  movups   xmm3, xmmword ptr [rcx + r13 + 0x20]
004C1A43  movups   xmm4, xmmword ptr [rcx + r13 + 0x30]
004C1A49  movaps   xmm0, xmm1
004C1A4C  movaps   xmmword ptr [rbp + 0xc0], xmm1
004C1A53  mulss    xmm0, xmm12
004C1A58  movaps   xmm6, xmm1
004C1A5B  shufps   xmm6, xmm1, 0x55
004C1A5F  movaps   xmm10, xmm2
004C1A63  shufps   xmm10, xmm2, 0x55
004C1A68  movaps   xmm5, xmm6
004C1A6B  mulss    xmm5, xmm11
004C1A70  movaps   xmm13, xmm10
004C1A74  mulss    xmm13, xmm11
004C1A79  movaps   xmm11, xmm3
004C1A7D  addss    xmm5, xmm0
004C1A81  mulss    xmm6, xmm12
004C1A86  mulss    xmm10, xmm12
004C1A8B  movaps   xmm0, xmm2
004C1A8E  mulss    xmm0, xmm12
004C1A93  mulss    xmm1, xmm15
004C1A98  addss    xmm13, xmm0
004C1A9D  shufps   xmm11, xmm3, 0x55
004C1AA2  movaps   xmm14, xmm11
004C1AA6  movaps   xmmword ptr [rbp + 0xd0], xmm2
004C1AAD  mulss    xmm14, dword ptr [rsp + 0x20]
004C1AB4  addss    xmm6, xmm1
004C1AB8  movss    xmm1, dword ptr [rsp + 0x30]
004C1ABE  movaps   xmm0, xmm3
004C1AC1  mulss    xmm0, xmm12
004C1AC6  mulss    xmm11, xmm12
004C1ACB  movaps   xmm12, xmm4
004C1ACF  shufps   xmm12, xmm4, 0x55
004C1AD4  addss    xmm14, xmm0
004C1AD9  mulss    xmm2, xmm15
004C1ADE  movaps   xmm0, xmm4
004C1AE1  mulss    xmm0, dword ptr [rbp + 0x280]
004C1AE9  movaps   xmmword ptr [rbp + 0xe0], xmm3
004C1AF0  addss    xmm10, xmm2
004C1AF5  mulss    xmm3, xmm15
004C1AFA  movaps   xmm15, xmm12
004C1AFE  mulss    xmm15, dword ptr [rsp + 0x20]
004C1B05  mulss    xmm12, dword ptr [rbp + 0x280]
004C1B0E  addss    xmm11, xmm3
004C1B13  addss    xmm15, xmm0
004C1B18  movaps   xmmword ptr [rbp + 0xf0], xmm4
004C1B1F  movss    xmm0, dword ptr [rsp + 0x40]
004C1B25  mulss    xmm4, dword ptr [rbp + 0x288]
004C1B2D  divss    xmm5, xmm0
004C1B31  divss    xmm13, xmm0
004C1B36  mulss    xmm6, xmm0
004C1B3A  addss    xmm5, xmm1
004C1B3E  mulss    xmm10, xmm0
004C1B43  addss    xmm12, xmm4
004C1B48  divss    xmm14, xmm0
004C1B4D  mulss    xmm11, xmm0
004C1B52  addss    xmm13, xmm1
004C1B57  divss    xmm15, xmm0
004C1B5C  mulss    xmm12, xmm0
004C1B61  movaps   xmm0, xmmword ptr [rbp + 0x180]
004C1B68  addss    xmm6, xmm0
004C1B6C  movss    dword ptr [rsp + 0x50], xmm5
004C1B72  addss    xmm10, xmm0
004C1B77  movss    dword ptr [rbp + 0x100], xmm5
004C1B7F  movss    dword ptr [rbp + 0x110], xmm13
004C1B88  movss    dword ptr [rbp + 0x104], xmm6
004C1B90  movss    dword ptr [rbp + 0x114], xmm10
004C1B99  addss    xmm14, xmm1
004C1B9E  addss    xmm11, xmm0
004C1BA3  addss    xmm15, xmm1
004C1BA8  addss    xmm12, xmm0
004C1BAD  movss    dword ptr [rbp + 0x120], xmm14
004C1BB6  movss    dword ptr [rbp + 0x124], xmm11
004C1BBF  movss    dword ptr [rbp + 0x130], xmm15
004C1BC8  movss    dword ptr [rbp + 0x134], xmm12
004C1BD1  call     0x39d1e0  ; -> 0039D1E0 fn
004C1BD6  movsx    r10d, word ptr [rip + 0x27e6362]  ; -> 02CA7F40
004C1BDE  mov      eax, edi
004C1BE0  movss    dword ptr [rbp + 0x108], xmm0
004C1BE8  movss    dword ptr [rbp + 0x118], xmm0
004C1BF0  movss    dword ptr [rbp + 0x128], xmm0
004C1BF8  lea      edx, [r10 + 2]
004C1BFC  movss    dword ptr [rbp + 0x138], xmm0
004C1C04  movss    xmm0, dword ptr [rsp + 0x50]
004C1C0A  cmp      edx, 0x400
004C1C10  mov      ecx, edx
004C1C12  mov      dword ptr [rbp + 0x12c], 0x3f800000
004C1C1C  cmovge   ecx, r14d
004C1C20  mov      dword ptr [rbp + 0x13c], 0x3f800000
004C1C2A  test     ecx, ecx
004C1C2C  cmovns   eax, ecx
004C1C2F  shl      eax, 4
004C1C32  cdqe     
004C1C34  cmp      edx, 0x400
004C1C3A  cmovge   edx, r14d
004C1C3E  test     edx, edx
004C1C40  mov      eax, dword ptr [rax + r13 + 0xc]
004C1C45  mov      dword ptr [rbp + 0x10c], eax
004C1C4B  mov      eax, edi
004C1C4D  cmovns   eax, edx
004C1C50  shl      eax, 4
004C1C53  comiss   xmm7, xmm0
004C1C56  cdqe     
004C1C58  mov      eax, dword ptr [rax + r13 + 0xc]
004C1C5D  mov      dword ptr [rbp + 0x11c], eax
004C1C63  ja       0x4c1f15  ; -> 004C1F15
004C1C69  comiss   xmm0, xmm9
004C1C6D  ja       0x4c1f15  ; -> 004C1F15
004C1C73  comiss   xmm7, xmm6
004C1C76  ja       0x4c1f15  ; -> 004C1F15
004C1C7C  comiss   xmm6, xmm8
004C1C80  ja       0x4c1f15  ; -> 004C1F15
004C1C86  comiss   xmm7, xmm13
004C1C8A  ja       0x4c1f15  ; -> 004C1F15
004C1C90  comiss   xmm13, xmm9
004C1C94  ja       0x4c1f15  ; -> 004C1F15
004C1C9A  comiss   xmm7, xmm10
004C1C9E  ja       0x4c1f15  ; -> 004C1F15
004C1CA4  comiss   xmm10, xmm8
004C1CA8  ja       0x4c1f15  ; -> 004C1F15
004C1CAE  comiss   xmm7, xmm14
004C1CB2  ja       0x4c1f15  ; -> 004C1F15
004C1CB8  comiss   xmm14, xmm9
004C1CBC  ja       0x4c1f15  ; -> 004C1F15
004C1CC2  comiss   xmm7, xmm11
004C1CC6  ja       0x4c1f15  ; -> 004C1F15
004C1CCC  comiss   xmm11, xmm8
004C1CD0  ja       0x4c1f15  ; -> 004C1F15
004C1CD6  comiss   xmm7, xmm15
004C1CDA  ja       0x4c1f15  ; -> 004C1F15
004C1CE0  comiss   xmm15, xmm9
004C1CE4  ja       0x4c1f15  ; -> 004C1F15
004C1CEA  comiss   xmm7, xmm12
004C1CEE  ja       0x4c1f15  ; -> 004C1F15
004C1CF4  comiss   xmm12, xmm8
004C1CF8  ja       0x4c1f15  ; -> 004C1F15
004C1CFE  movsx    r8d, word ptr [rip + 0x27e6242]  ; -> 02CA7F48
004C1D06  mov      eax, edi
004C1D08  movaps   xmm0, xmmword ptr [rbp + 0x130]
004C1D0F  movss    xmm1, dword ptr [rbp + 0xc8]
004C1D17  movss    dword ptr [rbp + 0x130], xmm1
004C1D1F  movss    xmm1, dword ptr [rbp + 0xe8]
004C1D27  lea      ecx, [r8 + 8]
004C1D2B  cmp      ecx, 0x400
004C1D31  mov      dword ptr [rbp + 0x138], 0x3f800000
004C1D3B  cmovge   ecx, r14d
004C1D3F  test     ecx, ecx
004C1D41  cmovns   eax, ecx
004C1D44  lea      ecx, [r8 + 6]
004C1D48  shl      eax, 4
004C1D4B  cdqe     
004C1D4D  cmp      ecx, 0x400
004C1D53  cmovge   ecx, r14d
004C1D57  test     ecx, ecx
004C1D59  movups   xmmword ptr [rax + r13], xmm0
004C1D5E  mov      eax, edi
004C1D60  movaps   xmm0, xmmword ptr [rbp + 0x120]
004C1D67  cmovns   eax, ecx
004C1D6A  shl      eax, 4
004C1D6D  lea      ecx, [r8 + 2]
004C1D71  cdqe     
004C1D73  cmp      ecx, 0x400
004C1D79  mov      dword ptr [rbp + 0x128], 0x3f800000
004C1D83  cmovge   ecx, r14d
004C1D87  test     ecx, ecx
004C1D89  movups   xmmword ptr [rax + r13], xmm0
004C1D8E  mov      eax, edi
004C1D90  movaps   xmm0, xmmword ptr [rbp + 0x100]
004C1D97  cmovns   eax, ecx
004C1D9A  shl      eax, 4
004C1D9D  lea      ecx, [r8 + 4]
004C1DA1  cdqe     
004C1DA3  cmp      ecx, 0x400
004C1DA9  movss    dword ptr [rbp + 0x100], xmm1
004C1DB1  movss    xmm1, dword ptr [rbp + 0xdc]
004C1DB9  cmovge   ecx, r14d
004C1DBD  test     ecx, ecx
004C1DBF  movss    dword ptr [rbp + 0x124], xmm1
004C1DC7  movss    xmm1, dword ptr [rbp + 0xfc]
004C1DCF  movups   xmmword ptr [rax + r13], xmm0
004C1DD4  mov      eax, edi
004C1DD6  mov      dword ptr [rbp + 0x108], 0x3f800000
004C1DE0  movaps   xmm0, xmmword ptr [rbp + 0x110]
004C1DE7  cmovns   eax, ecx
004C1DEA  shl      eax, 4
004C1DED  lea      ecx, [r8 + 1]
004C1DF1  cdqe     
004C1DF3  cmp      ecx, 0x400
004C1DF9  movss    dword ptr [rbp + 0x114], xmm1
004C1E01  cmovge   ecx, r14d
004C1E05  mov      dword ptr [rbp + 0x118], 0x3f800000
004C1E0F  test     ecx, ecx
004C1E11  movups   xmmword ptr [rax + r13], xmm0
004C1E16  mov      eax, edi
004C1E18  movss    xmm0, dword ptr [rbp + 0xd8]
004C1E20  cmovns   eax, ecx
004C1E23  inc      word ptr [rip + 0x27e6122]  ; -> 02CA7F4C
004C1E2A  add      r8w, 9
004C1E2F  shl      eax, 4
004C1E32  movss    dword ptr [rbp + 0x120], xmm0
004C1E3A  movss    xmm0, dword ptr [rbp + 0xf8]
004C1E42  cdqe     
004C1E44  movss    dword ptr [rbp + 0x110], xmm0
004C1E4C  movaps   xmm0, xmmword ptr [rbp - 0x30]
004C1E50  movsx    edx, r8w
004C1E54  movups   xmmword ptr [rax + r13], xmm0
004C1E59  mov      eax, edi
004C1E5B  mov      word ptr [rip + 0x27e60e5], r8w  ; -> 02CA7F48
004C1E63  movss    xmm0, dword ptr [rbp + 0xcc]
004C1E6B  lea      ecx, [rdx - 9]
004C1E6E  movss    dword ptr [rbp + 0x134], xmm0
004C1E76  movss    xmm0, dword ptr [rbp + 0xec]
004C1E7E  cmp      ecx, 0x400
004C1E84  movss    dword ptr [rbp + 0x104], xmm0
004C1E8C  cmovge   ecx, r14d
004C1E90  test     ecx, ecx
004C1E92  cmovns   eax, ecx
004C1E95  movaps   xmm0, xmmword ptr [rbp + 0x130]
004C1E9C  lea      ecx, [rdx - 6]
004C1E9F  shl      eax, 4
004C1EA2  cdqe     
004C1EA4  cmp      ecx, 0x400
004C1EAA  cmovge   ecx, r14d
004C1EAE  test     ecx, ecx
004C1EB0  movups   xmmword ptr [rax + r13], xmm0
004C1EB5  mov      eax, edi
004C1EB7  movaps   xmm0, xmmword ptr [rbp + 0x120]
004C1EBE  cmovns   eax, ecx
004C1EC1  shl      eax, 4
004C1EC4  lea      ecx, [rdx - 4]
004C1EC7  cdqe     
004C1EC9  cmp      ecx, 0x400
004C1ECF  cmovge   ecx, r14d
004C1ED3  test     ecx, ecx
004C1ED5  movups   xmmword ptr [rax + r13], xmm0
004C1EDA  mov      eax, edi
004C1EDC  movaps   xmm0, xmmword ptr [rbp + 0x100]
004C1EE3  cmovns   eax, ecx
004C1EE6  shl      eax, 4
004C1EE9  lea      ecx, [rdx - 2]
004C1EEC  cdqe     
004C1EEE  cmp      ecx, 0x400
004C1EF4  cmovge   ecx, r14d
004C1EF8  test     ecx, ecx
004C1EFA  movups   xmmword ptr [rax + r13], xmm0
004C1EFF  mov      eax, edi
004C1F01  movaps   xmm0, xmmword ptr [rbp + 0x110]
004C1F08  cmovns   eax, ecx
004C1F0B  shl      eax, 4
004C1F0E  cdqe     
004C1F10  movups   xmmword ptr [rax + r13], xmm0
004C1F15  movzx    ebx, word ptr [rip + 0x27e6050]  ; -> 02CA7F6C
004C1F1C  test     bx, bx
004C1F1F  je       0x4c1f46  ; -> 004C1F46
004C1F21  movzx    esi, word ptr [rip + 0x27e6040]  ; -> 02CA7F68
004C1F28  movss    xmm12, dword ptr [rbp + 0x280]
004C1F31  movss    xmm15, dword ptr [rbp + 0x288]
004C1F3A  movss    xmm11, dword ptr [rsp + 0x20]
004C1F41  jmp      0x4c1a00  ; -> 004C1A00
004C1F46  sub      word ptr [rip + 0x27e6002], 1  ; -> 02CA7F50
004C1F4E  je       0x4c1f82  ; -> 004C1F82
004C1F50  movzx    r14d, word ptr [rip + 0x27e6000]  ; -> 02CA7F58
004C1F58  movss    xmm10, dword ptr [rip + 0x403bdf]  ; -> 008C5B40 [f32 255]
004C1F61  movss    xmm3, dword ptr [rsp + 0x60]
004C1F67  movss    xmm4, dword ptr [rsp + 0x70]
004C1F6D  movss    xmm5, dword ptr [rip + 0x1829d03]  ; -> 01CEBC78 [f32 6.283185]
004C1F75  movss    xmm6, dword ptr [rip + 0x1829cd3]  ; -> 01CEBC50 [f32 3.141593]
004C1F7D  jmp      0x4c17e0  ; -> 004C17E0
004C1F82  movsx    ecx, word ptr [rip + 0x27e5fbb]  ; -> 02CA7F44
004C1F89  mov      eax, 0xffff8000
004C1F8E  or       word ptr [rip + 0x27e5fb7], ax  ; -> 02CA7F4C
004C1F95  mov      r8d, 1
004C1F9B  cmp      ecx, 0x400
004C1FA1  mov      eax, edi
004C1FA3  mov      rdx, r15
004C1FA6  cmovge   ecx, r14d
004C1FAA  test     ecx, ecx
004C1FAC  cmovns   eax, ecx
004C1FAF  shl      eax, 4
004C1FB2  movsxd   rcx, eax
004C1FB5  mov      eax, dword ptr [rip + 0x27e5f91]  ; -> 02CA7F4C
004C1FBB  mov      dword ptr [rcx + r13], eax
004C1FBF  movsx    eax, word ptr [rip + 0x27e5f8e]  ; -> 02CA7F54
004C1FC6  cmp      eax, 0x400
004C1FCB  cmovge   eax, r14d
004C1FCF  test     eax, eax
004C1FD1  cmovns   edi, eax
004C1FD4  shl      edi, 4
004C1FD7  movsxd   rcx, edi
004C1FDA  add      rcx, r13
004C1FDD  mov      rax, r12
004C1FE0  lea      r11, [rsp + 0x330]
004C1FE8  mov      rbx, qword ptr [r11 + 0x40]
004C1FEC  movaps   xmm6, xmmword ptr [r11 - 0x10]
004C1FF1  movaps   xmm7, xmmword ptr [r11 - 0x20]
004C1FF6  movaps   xmm8, xmmword ptr [r11 - 0x30]
004C1FFB  movaps   xmm9, xmmword ptr [r11 - 0x40]
004C2000  movaps   xmm10, xmmword ptr [r11 - 0x50]
004C2005  movaps   xmm11, xmmword ptr [r11 - 0x60]
004C200A  movaps   xmm12, xmmword ptr [r11 - 0x70]
004C200F  movaps   xmm13, xmmword ptr [r11 - 0x80]
004C2014  movaps   xmm14, xmmword ptr [r11 - 0x90]
004C201C  movaps   xmm15, xmmword ptr [r11 - 0xa0]
004C2024  mov      rsp, r11
004C2027  pop      r15
004C2029  pop      r14
004C202B  pop      r13
004C202D  pop      r12
004C202F  pop      rdi
004C2030  pop      rsi
004C2031  pop      rbp
004C2032  jmp      rax
```

## 0063AAD0 (288 B, extent 0063AAD0-0063ABF0)

Documented callee on this page: `0063B3E0`

```
0063AAD0  push     rdi
0063AAD2  push     r14
0063AAD4  push     r15
0063AAD6  sub      rsp, 0x30
0063AADA  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0063AAE3  mov      qword ptr [rsp + 0x50], rbx
0063AAE8  mov      qword ptr [rsp + 0x58], rbp
0063AAED  mov      qword ptr [rsp + 0x60], rsi
0063AAF2  mov      rbp, rdx
0063AAF5  mov      rsi, rcx
0063AAF8  lea      r14, [rcx + 0x38]
0063AAFC  mov      rdi, qword ptr [r14]
0063AAFF  xor      r15d, r15d
0063AB02  cmp      rdi, r14
0063AB05  cmove    rdi, r15
0063AB09  test     rdi, rdi
0063AB0C  je       0x63abd7  ; -> 0063ABD7
0063AB12  mov      rbx, rdi
0063AB15  test     rdi, rdi
0063AB18  je       0x63ab27  ; -> 0063AB27
0063AB1A  mov      rax, qword ptr [rdi]
0063AB1D  mov      rdi, rax
0063AB20  cmp      rax, r14
0063AB23  cmove    rdi, r15
0063AB27  cmp      qword ptr [rbx + 0x50], rbp
0063AB2B  jne      0x63abce  ; -> 0063ABCE
0063AB31  mov      rcx, qword ptr [rbx]
0063AB34  mov      rax, qword ptr [rbx + 8]
0063AB38  mov      qword ptr [rcx + 8], rax
0063AB3C  mov      qword ptr [rax], rcx
0063AB3F  mov      qword ptr [rbx], rbx
0063AB42  mov      qword ptr [rbx + 8], rbx
0063AB46  mov      r10, qword ptr [rsi + 0x78]
0063AB4A  test     r10, r10
0063AB4D  je       0x63abb0  ; -> 0063ABB0
0063AB4F  xor      dl, dl
0063AB51  mov      r9, qword ptr [rbx + 0x50]
0063AB55  test     r9, r9
0063AB58  je       0x63abb0  ; -> 0063ABB0
0063AB5A  nop      word ptr [rax + rax]
0063AB60  mov      ecx, dword ptr [r9 + 0xec]
0063AB67  mov      eax, dword ptr [r10 + 0x10]
0063AB6B  btr      eax, 0x1f
0063AB6F  cmp      ecx, eax
0063AB71  jae      0x63aba7  ; -> 0063ABA7
0063AB73  mov      eax, ecx
0063AB75  shl      rax, 5
0063AB79  add      rax, qword ptr [r10 + 0x18]
0063AB7D  je       0x63aba7  ; -> 0063ABA7
0063AB7F  test     dl, dl
0063AB81  jne      0x63ab9e  ; -> 0063AB9E
0063AB83  lea      r8, [rbx + 0x38]
0063AB87  mov      rdx, qword ptr [r8]
0063AB8A  mov      rcx, qword ptr [r8 + 8]
0063AB8E  mov      qword ptr [rdx + 8], rcx
0063AB92  mov      qword ptr [rcx], rdx
0063AB95  mov      qword ptr [r8], r8
0063AB98  mov      qword ptr [r8 + 8], r8
0063AB9C  mov      dl, 1
0063AB9E  mov      ecx, dword ptr [rbx + 0x70]
0063ABA1  sub      dword ptr [rax + 0x10], ecx
0063ABA4  dec      dword ptr [rax + 0x14]
0063ABA7  mov      r9, qword ptr [r9 + 0x78]
0063ABAB  test     r9, r9
0063ABAE  jne      0x63ab60  ; -> 0063AB60
0063ABB0  mov      rcx, rbx
0063ABB3  call     0x63b3e0  ; -> 0063B3E0 fn
0063ABB8  lea      rcx, [rbx + 0x10]
0063ABBC  call     0x680030  ; -> 00680030 fn
0063ABC1  nop      
0063ABC2  lea      rcx, [rsi + 0x50]
0063ABC6  mov      rdx, rbx
0063ABC9  call     0x680200  ; -> 00680200 fn
0063ABCE  test     rdi, rdi
0063ABD1  jne      0x63ab12  ; -> 0063AB12
0063ABD7  mov      rbx, qword ptr [rsp + 0x50]
0063ABDC  mov      rbp, qword ptr [rsp + 0x58]
0063ABE1  mov      rsi, qword ptr [rsp + 0x60]
0063ABE6  add      rsp, 0x30
0063ABEA  pop      r15
0063ABEC  pop      r14
0063ABEE  pop      rdi
0063ABEF  ret      
```

## 00793640 (83 B, extent 00793640-00793693)

Documented callee on this page: `005DDBA0`

```
00793640  push     rdi
00793642  sub      rsp, 0x30
00793646  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0079364F  mov      qword ptr [rsp + 0x40], rbx
00793654  mov      rdi, rcx
00793657  add      rcx, 0x200
0079365E  call     0x16d6a0  ; -> 0016D6A0 fn
00793663  nop      
00793664  lea      r9, [rip - 0x625fcb]  ; -> 0016D6A0
0079366B  mov      edx, 0x18
00793670  lea      r8d, [rdx - 0x10]
00793674  lea      rcx, [rdi + 0x140]
0079367B  call     0x809054  ; -> 00809054 fn
00793680  nop      
00793681  mov      rcx, rdi
00793684  mov      rbx, qword ptr [rsp + 0x40]
00793689  add      rsp, 0x30
0079368D  pop      rdi
0079368E  jmp      0x5ddba0  ; -> 005DDBA0 fn
```

## 00877790 (74 B, extent 00877790-008777DA)

Documented callee on this page: `0063BC00`

```
00877790  push     rbx
00877792  sub      rsp, 0x20
00877796  lea      rcx, [rip + 0x243f8e3]  ; -> 02CB7080
0087779D  mov      rbx, rdx
008777A0  call     0x63bc00  ; -> 0063BC00 fn
008777A5  test     rax, rax
008777A8  jne      0x8777b0  ; -> 008777B0
008777AA  add      rsp, 0x20
008777AE  pop      rbx
008777AF  ret      
008777B0  test     rbx, rbx
008777B3  je       0x8777d2  ; -> 008777D2
008777B5  xor      ecx, ecx
008777B7  mov      qword ptr [rbx], rcx
008777BA  mov      qword ptr [rbx + 0x18], rax
008777BE  mov      qword ptr [rbx + 0x30], rcx
008777C2  mov      rcx, rbx
008777C5  mov      qword ptr [rbx + 0x20], rbx
008777C9  mov      qword ptr [rbx + 0x28], rbx
008777CD  call     0x8792d0  ; -> 008792D0 fn
008777D2  mov      al, 1
008777D4  add      rsp, 0x20
008777D8  pop      rbx
008777D9  ret      
```
