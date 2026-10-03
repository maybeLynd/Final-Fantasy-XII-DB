# F homing pack (FABLE): `01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 20. No bearing page cites them and no documented function calls them directly.

## 00347A50 (87 B, extent 00347A50-00347AA7)

Documented callee on this page: `00267F90`

```
00347A50  mov      qword ptr [rsp + 8], rbx
00347A55  mov      qword ptr [rsp + 0x10], rbp
00347A5A  mov      qword ptr [rsp + 0x18], rsi
00347A5F  push     rdi
00347A60  sub      rsp, 0x20
00347A64  mov      rsi, rdx
00347A67  mov      rbp, rcx
00347A6A  mov      edx, 1
00347A6F  mov      rcx, r9
00347A72  mov      rbx, r9
00347A75  mov      rdi, r8
00347A78  call     0x267f90  ; -> 00267F90 fn
00347A7D  mov      r9, rbx
00347A80  mov      r8, rdi
00347A83  mov      rdx, rsi
00347A86  mov      rcx, rbp
00347A89  call     0x346c00  ; -> 00346C00 fn
00347A8E  mov      rbx, qword ptr [rsp + 0x30]
00347A93  mov      rbp, qword ptr [rsp + 0x38]
00347A98  mov      rsi, qword ptr [rsp + 0x40]
00347A9D  add      rsp, 0x20
00347AA1  pop      rdi
00347AA2  jmp      0x25d5d0  ; -> 0025D5D0 fn
```

## 00348040 (123 B, extent 00348040-003480BB)

Documented callee on this page: `00267DB0`

```
00348040  mov      qword ptr [rsp + 8], rbx
00348045  push     rdi
00348046  sub      rsp, 0x50
0034804A  movaps   xmmword ptr [rsp + 0x40], xmm6
0034804F  mov      rcx, r9
00348052  movaps   xmmword ptr [rsp + 0x30], xmm7
00348057  mov      rbx, r9
0034805A  movaps   xmmword ptr [rsp + 0x20], xmm8
00348060  mov      rdi, rdx
00348063  call     0x267db0  ; -> 00267DB0 fn
00348068  mov      rcx, rbx
0034806B  movaps   xmm8, xmm0
0034806F  call     0x267db0  ; -> 00267DB0 fn
00348074  mov      rcx, rbx
00348077  movaps   xmm7, xmm0
0034807A  call     0x267db0  ; -> 00267DB0 fn
0034807F  mov      edx, 1
00348084  mov      rcx, rdi
00348087  movaps   xmm6, xmm0
0034808A  call     0x2e75a0  ; -> 002E75A0 fn
0034808F  movaps   xmm3, xmm7
00348092  movaps   xmm2, xmm6
00348095  movaps   xmm1, xmm8
00348099  mov      rcx, rdi
0034809C  mov      rbx, qword ptr [rsp + 0x60]
003480A1  movaps   xmm6, xmmword ptr [rsp + 0x40]
003480A6  movaps   xmm7, xmmword ptr [rsp + 0x30]
003480AB  movaps   xmm8, xmmword ptr [rsp + 0x20]
003480B1  add      rsp, 0x50
003480B5  pop      rdi
003480B6  jmp      0x2e7530  ; -> 002E7530 fn
```

## 00348750 (123 B, extent 00348750-003487CB)

Documented callee on this page: `00267DB0`

```
00348750  mov      qword ptr [rsp + 8], rbx
00348755  push     rdi
00348756  sub      rsp, 0x50
0034875A  movaps   xmmword ptr [rsp + 0x40], xmm6
0034875F  mov      rcx, r9
00348762  movaps   xmmword ptr [rsp + 0x30], xmm7
00348767  mov      rbx, r9
0034876A  movaps   xmmword ptr [rsp + 0x20], xmm8
00348770  mov      rdi, rdx
00348773  call     0x267db0  ; -> 00267DB0 fn
00348778  mov      rcx, rbx
0034877B  movaps   xmm8, xmm0
0034877F  call     0x267db0  ; -> 00267DB0 fn
00348784  mov      rcx, rbx
00348787  movaps   xmm7, xmm0
0034878A  call     0x267db0  ; -> 00267DB0 fn
0034878F  mov      edx, 1
00348794  mov      rcx, rdi
00348797  movaps   xmm6, xmm0
0034879A  call     0x2e75a0  ; -> 002E75A0 fn
0034879F  movaps   xmm3, xmm7
003487A2  movaps   xmm2, xmm6
003487A5  movaps   xmm1, xmm8
003487A9  mov      rcx, rdi
003487AC  mov      rbx, qword ptr [rsp + 0x60]
003487B1  movaps   xmm6, xmmword ptr [rsp + 0x40]
003487B6  movaps   xmm7, xmmword ptr [rsp + 0x30]
003487BB  movaps   xmm8, xmmword ptr [rsp + 0x20]
003487C1  add      rsp, 0x50
003487C5  pop      rdi
003487C6  jmp      0x2e74c0  ; -> 002E74C0 fn
```

## 0034A3B0 (54 B, extent 0034A3B0-0034A3E6)

Documented callee on this page: `002640C0`

```
0034A3B0  mov      qword ptr [rsp + 8], rbx
0034A3B5  push     rdi
0034A3B6  sub      rsp, 0x20
0034A3BA  mov      rbx, r9
0034A3BD  call     0x2640c0  ; -> 002640C0 fn
0034A3C2  mov      rcx, rbx
0034A3C5  mov      rdi, rax
0034A3C8  call     0x267e10  ; -> 00267E10 fn
0034A3CD  mov      ecx, dword ptr [rdi + 0x28]
0034A3D0  xor      edx, edx
0034A3D2  test     eax, eax
0034A3D4  sete     dl
0034A3D7  mov      rbx, qword ptr [rsp + 0x30]
0034A3DC  add      rsp, 0x20
0034A3E0  pop      rdi
0034A3E1  jmp      0x26a2a0  ; -> 0026A2A0 fn
```

## 0034A720 (73 B, extent 0034A720-0034A769)

Documented callee on this page: `002640C0`

```
0034A720  mov      qword ptr [rsp + 8], rbx
0034A725  push     rdi
0034A726  sub      rsp, 0x30
0034A72A  movaps   xmmword ptr [rsp + 0x20], xmm6
0034A72F  mov      rdi, r9
0034A732  call     0x2640c0  ; -> 002640C0 fn
0034A737  mov      rcx, rdi
0034A73A  mov      rbx, rax
0034A73D  call     0x267db0  ; -> 00267DB0 fn
0034A742  mov      rcx, rdi
0034A745  movaps   xmm6, xmm0
0034A748  call     0x267e10  ; -> 00267E10 fn
0034A74D  movaps   xmm2, xmm6
0034A750  mov      edx, eax
0034A752  mov      rcx, rbx
0034A755  mov      rbx, qword ptr [rsp + 0x40]
0034A75A  movaps   xmm6, xmmword ptr [rsp + 0x20]
0034A75F  add      rsp, 0x30
0034A763  pop      rdi
0034A764  jmp      0x3dd1f0  ; -> 003DD1F0 fn
```

## 0034A7A0 (191 B, extent 0034A7A0-0034A85F)

Documented callee on this page: `00267F90`

```
0034A7A0  mov      qword ptr [rsp + 8], rbx
0034A7A5  mov      qword ptr [rsp + 0x10], rbp
0034A7AA  mov      qword ptr [rsp + 0x18], rsi
0034A7AF  mov      qword ptr [rsp + 0x20], rdi
0034A7B4  push     r12
0034A7B6  push     r14
0034A7B8  push     r15
0034A7BA  sub      rsp, 0x20
0034A7BE  mov      r12, rcx
0034A7C1  mov      rbp, r9
0034A7C4  mov      rcx, r9
0034A7C7  mov      r14, r8
0034A7CA  mov      r15, rdx
0034A7CD  call     0x267e10  ; -> 00267E10 fn
0034A7D2  mov      rcx, rbp
0034A7D5  mov      esi, eax
0034A7D7  call     0x267e10  ; -> 00267E10 fn
0034A7DC  mov      rcx, rbp
0034A7DF  mov      ebx, eax
0034A7E1  call     0x267e10  ; -> 00267E10 fn
0034A7E6  mov      edx, eax
0034A7E8  mov      rcx, rbp
0034A7EB  mov      edi, eax
0034A7ED  call     0x267f90  ; -> 00267F90 fn
0034A7F2  mov      edx, ebx
0034A7F4  mov      rcx, rbp
0034A7F7  call     0x267f90  ; -> 00267F90 fn
0034A7FC  xor      edx, edx
0034A7FE  mov      rcx, rbp
0034A801  call     0x267f90  ; -> 00267F90 fn
0034A806  xor      edx, edx
0034A808  mov      rcx, rbp
0034A80B  call     0x267f90  ; -> 00267F90 fn
0034A810  xor      edx, edx
0034A812  mov      rcx, rbp
0034A815  call     0x267f90  ; -> 00267F90 fn
0034A81A  mov      edx, 0xfffffffd
0034A81F  mov      rcx, rbp
0034A822  call     0x267f90  ; -> 00267F90 fn
0034A827  mov      edx, esi
0034A829  mov      ecx, edi
0034A82B  call     0x2e2090  ; -> 002E2090 fn
0034A830  mov      r9, rbp
0034A833  mov      r8, r14
0034A836  mov      rdx, r15
0034A839  mov      rcx, r12
0034A83C  mov      rbx, qword ptr [rsp + 0x40]
0034A841  mov      rbp, qword ptr [rsp + 0x48]
0034A846  mov      rsi, qword ptr [rsp + 0x50]
0034A84B  mov      rdi, qword ptr [rsp + 0x58]
0034A850  add      rsp, 0x20
0034A854  pop      r15
0034A856  pop      r14
0034A858  pop      r12
0034A85A  jmp      0x349800  ; -> 00349800 fn
```

## 0034A920 (31 B, extent 0034A920-0034A93F)

Documented callee on this page: `00267F90`

```
0034A920  push     rbx
0034A922  sub      rsp, 0x20
0034A926  mov      rbx, r9
0034A929  nop      dword ptr [rax]
0034A930  mov      edx, 2
0034A935  mov      rcx, rbx
0034A938  call     0x267f90  ; -> 00267F90 fn
0034A93D  jmp      0x34a930  ; -> 0034A930
```

## 0034AC70 (109 B, extent 0034AC70-0034ACDD)

Documented callee on this page: `00267F60`

```
0034AC70  mov      qword ptr [rsp + 8], rbx
0034AC75  push     rdi
0034AC76  sub      rsp, 0x30
0034AC7A  mov      rcx, r9
0034AC7D  movaps   xmmword ptr [rsp + 0x20], xmm6
0034AC82  mov      rdi, r9
0034AC85  call     0x267e10  ; -> 00267E10 fn
0034AC8A  xor      edx, edx
0034AC8C  mov      rcx, rdi
0034AC8F  movd     xmm6, eax
0034AC93  cvtdq2ps xmm6, xmm6
0034AC96  call     0x267f90  ; -> 00267F90 fn
0034AC9B  mov      rcx, rdi
0034AC9E  movaps   xmm1, xmm6
0034ACA1  call     0x267f60  ; -> 00267F60 fn
0034ACA6  call     0x2640c0  ; -> 002640C0 fn
0034ACAB  mov      rcx, rdi
0034ACAE  mov      rbx, rax
0034ACB1  call     0x267db0  ; -> 00267DB0 fn
0034ACB6  mov      rcx, rdi
0034ACB9  movaps   xmm6, xmm0
0034ACBC  call     0x267e10  ; -> 00267E10 fn
0034ACC1  movaps   xmm2, xmm6
0034ACC4  mov      edx, eax
0034ACC6  mov      rcx, rbx
0034ACC9  mov      rbx, qword ptr [rsp + 0x40]
0034ACCE  movaps   xmm6, xmmword ptr [rsp + 0x20]
0034ACD3  add      rsp, 0x30
0034ACD7  pop      rdi
0034ACD8  jmp      0x3dd1f0  ; -> 003DD1F0 fn
```

## 0034B1E0 (149 B, extent 0034B1E0-0034B275)

Documented callee on this page: `00267F90`

```
0034B1E0  mov      qword ptr [rsp + 8], rbx
0034B1E5  mov      qword ptr [rsp + 0x10], rbp
0034B1EA  mov      qword ptr [rsp + 0x18], rsi
0034B1EF  push     rdi
0034B1F0  sub      rsp, 0x20
0034B1F4  mov      edx, dword ptr [r8]
0034B1F7  mov      rbp, rcx
0034B1FA  mov      rcx, r9
0034B1FD  mov      rdi, r9
0034B200  mov      rbx, r8
0034B203  call     0x267f90  ; -> 00267F90 fn
0034B208  mov      edx, dword ptr [rbx + 4]
0034B20B  mov      rcx, rdi
0034B20E  call     0x267f90  ; -> 00267F90 fn
0034B213  xor      edx, edx
0034B215  mov      rcx, rdi
0034B218  call     0x267f90  ; -> 00267F90 fn
0034B21D  mov      rcx, rdi
0034B220  call     0x267e10  ; -> 00267E10 fn
0034B225  mov      rcx, rdi
0034B228  mov      ebx, eax
0034B22A  call     0x267e10  ; -> 00267E10 fn
0034B22F  mov      rcx, rdi
0034B232  mov      esi, eax
0034B234  call     0x267e10  ; -> 00267E10 fn
0034B239  mov      edi, eax
0034B23B  test     ebx, ebx
0034B23D  je       0x34b24e  ; -> 0034B24E
0034B23F  mov      r8d, 1
0034B245  mov      edx, esi
0034B247  mov      ecx, eax
0034B249  call     0x2e2540  ; -> 002E2540 fn
0034B24E  mov      edx, esi
0034B250  mov      ecx, edi
0034B252  call     0x32a810  ; -> 0032A810 fn
0034B257  mov      edx, eax
0034B259  mov      rcx, rbp
0034B25C  mov      rbx, qword ptr [rsp + 0x30]
0034B261  mov      rbp, qword ptr [rsp + 0x38]
0034B266  mov      rsi, qword ptr [rsp + 0x40]
0034B26B  add      rsp, 0x20
0034B26F  pop      rdi
0034B270  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 0034BFE0 (39 B, extent 0034BFE0-0034C007)

Documented callee on this page: `002640C0`

```
0034BFE0  push     rbx
0034BFE2  sub      rsp, 0x20
0034BFE6  mov      rbx, r8
0034BFE9  call     0x2640c0  ; -> 002640C0 fn
0034BFEE  mov      edx, dword ptr [rbx]
0034BFF0  mov      ecx, dword ptr [rax + 0x28]
0034BFF3  call     0x3dd0d0  ; -> 003DD0D0 fn
0034BFF8  xor      ecx, ecx
0034BFFA  test     eax, eax
0034BFFC  setne    cl
0034BFFF  mov      eax, ecx
0034C001  add      rsp, 0x20
0034C005  pop      rbx
0034C006  ret      
```

## 0034C5C0 (110 B, extent 0034C5C0-0034C62E)

Documented callee on this page: `00267DB0`

```
0034C5C0  push     rbx
0034C5C2  sub      rsp, 0x50
0034C5C6  movaps   xmmword ptr [rsp + 0x40], xmm6
0034C5CB  mov      rcx, r9
0034C5CE  movaps   xmmword ptr [rsp + 0x30], xmm7
0034C5D3  mov      rbx, r9
0034C5D6  movaps   xmmword ptr [rsp + 0x20], xmm8
0034C5DC  call     0x267db0  ; -> 00267DB0 fn
0034C5E1  mov      rcx, rbx
0034C5E4  movaps   xmm6, xmm0
0034C5E7  call     0x267db0  ; -> 00267DB0 fn
0034C5EC  mov      rcx, rbx
0034C5EF  movaps   xmm7, xmm0
0034C5F2  call     0x267db0  ; -> 00267DB0 fn
0034C5F7  movaps   xmm8, xmm0
0034C5FB  xor      ebx, ebx
0034C5FD  nop      dword ptr [rax]
0034C600  movaps   xmm3, xmm6
0034C603  movaps   xmm2, xmm7
0034C606  movaps   xmm1, xmm8
0034C60A  mov      ecx, ebx
0034C60C  call     0x2ece40  ; -> 002ECE40 fn
0034C611  inc      ebx
0034C613  cmp      ebx, 5
0034C616  jl       0x34c600  ; -> 0034C600
0034C618  movaps   xmm6, xmmword ptr [rsp + 0x40]
0034C61D  movaps   xmm7, xmmword ptr [rsp + 0x30]
0034C622  movaps   xmm8, xmmword ptr [rsp + 0x20]
0034C628  add      rsp, 0x50
0034C62C  pop      rbx
0034C62D  ret      
```

## 0034C9E0 (53 B, extent 0034C9E0-0034CA15)

Documented callee on this page: `003DBF60`

```
0034C9E0  sub      rsp, 0x28
0034C9E4  mov      rcx, qword ptr [r8]
0034C9E7  test     rcx, rcx
0034C9EA  jne      0x34c9f3  ; -> 0034C9F3
0034C9EC  xor      eax, eax
0034C9EE  add      rsp, 0x28
0034C9F2  ret      
0034C9F3  mov      edx, dword ptr [r8 + 8]
0034C9F7  test     edx, edx
0034C9F9  js       0x34c9ec  ; -> 0034C9EC
0034C9FB  or       r8d, 0xffffffff
0034C9FF  call     0x3dbf60  ; -> 003DBF60 fn
0034CA04  xor      ecx, ecx
0034CA06  cmp      eax, 0xff
0034CA0B  setne    cl
0034CA0E  mov      eax, ecx
0034CA10  add      rsp, 0x28
0034CA14  ret      
```

## 0034CAC0 (65 B, extent 0034CAC0-0034CB01)

Documented callee on this page: `00267DB0`

```
0034CAC0  push     rbx
0034CAC2  sub      rsp, 0x30
0034CAC6  mov      rcx, r9
0034CAC9  movaps   xmmword ptr [rsp + 0x20], xmm6
0034CACE  mov      rbx, rdx
0034CAD1  call     0x267db0  ; -> 00267DB0 fn
0034CAD6  movaps   xmm1, xmm0
0034CAD9  mov      rcx, rbx
0034CADC  movaps   xmm6, xmm0
0034CADF  call     0x26ba00  ; -> 0026BA00 fn
0034CAE4  mulss    xmm6, dword ptr [rip + 0x199f07c]  ; -> 01CEBB68 [f32 0.25]
0034CAEC  mov      rcx, rbx
0034CAEF  movaps   xmm1, xmm6
0034CAF2  movaps   xmm6, xmmword ptr [rsp + 0x20]
0034CAF7  add      rsp, 0x30
0034CAFB  pop      rbx
0034CAFC  jmp      0x26b9d0  ; -> 0026B9D0 fn
```

## 0034D260 (65 B, extent 0034D260-0034D2A1)

Documented callee on this page: `00267DB0`

```
0034D260  push     rbx
0034D262  sub      rsp, 0x30
0034D266  mov      rcx, r9
0034D269  movaps   xmmword ptr [rsp + 0x20], xmm6
0034D26E  mov      rbx, rdx
0034D271  call     0x267db0  ; -> 00267DB0 fn
0034D276  movaps   xmm1, xmm0
0034D279  mov      rcx, rbx
0034D27C  movaps   xmm6, xmm0
0034D27F  call     0x269e60  ; -> 00269E60 fn
0034D284  mulss    xmm6, dword ptr [rip + 0x199e8dc]  ; -> 01CEBB68 [f32 0.25]
0034D28C  mov      rcx, rbx
0034D28F  movaps   xmm1, xmm6
0034D292  movaps   xmm6, xmmword ptr [rsp + 0x20]
0034D297  add      rsp, 0x30
0034D29B  pop      rbx
0034D29C  jmp      0x26abd0  ; -> 0026ABD0 fn
```

## 00351210 (61 B, extent 00351210-0035124D)

Documented callee on this page: `002640C0`

```
00351210  mov      qword ptr [rsp + 8], rbx
00351215  push     rdi
00351216  sub      rsp, 0x20
0035121A  mov      rcx, r9
0035121D  mov      rbx, r9
00351220  call     0x267e10  ; -> 00267E10 fn
00351225  mov      rcx, rbx
00351228  mov      edi, eax
0035122A  call     0x267e10  ; -> 00267E10 fn
0035122F  mov      ebx, eax
00351231  call     0x2640c0  ; -> 002640C0 fn
00351236  mov      r8d, edi
00351239  mov      edx, ebx
0035123B  mov      ecx, dword ptr [rax + 0x28]
0035123E  mov      rbx, qword ptr [rsp + 0x30]
00351243  add      rsp, 0x20
00351247  pop      rdi
00351248  jmp      0x3dea00  ; -> 003DEA00 fn
```

## 00351250 (76 B, extent 00351250-0035129C)

Documented callee on this page: `00267DB0`

```
00351250  push     rbx
00351252  sub      rsp, 0x30
00351256  mov      rcx, r9
00351259  movaps   xmmword ptr [rsp + 0x20], xmm6
0035125E  mov      rbx, r9
00351261  call     0x267db0  ; -> 00267DB0 fn
00351266  mov      rcx, rbx
00351269  movaps   xmm6, xmm0
0035126C  call     0x267e10  ; -> 00267E10 fn
00351271  mov      ecx, eax
00351273  mov      ebx, eax
00351275  call     0x16d6a0  ; -> 0016D6A0 fn
0035127A  mov      ecx, ebx
0035127C  call     0x3eb700  ; -> 003EB700 fn
00351281  movsxd   rcx, eax
00351284  movaps   xmm3, xmm6
00351287  movaps   xmm2, xmm6
0035128A  movaps   xmm1, xmm6
0035128D  movaps   xmm6, xmmword ptr [rsp + 0x20]
00351292  add      rsp, 0x30
00351296  pop      rbx
00351297  jmp      0x3eb940  ; -> 003EB940 fn
```

## 003512A0 (160 B, extent 003512A0-00351340)

Documented callee on this page: `002650B0`

```
003512A0  mov      qword ptr [rsp + 8], rbx
003512A5  mov      qword ptr [rsp + 0x10], rbp
003512AA  mov      qword ptr [rsp + 0x18], rsi
003512AF  push     rdi
003512B0  push     r14
003512B2  push     r15
003512B4  sub      rsp, 0x20
003512B8  mov      rsi, r9
003512BB  mov      r15, rdx
003512BE  mov      rbp, rcx
003512C1  call     0x2640c0  ; -> 002640C0 fn
003512C6  mov      rcx, rsi
003512C9  mov      rdi, rax
003512CC  call     0x267e10  ; -> 00267E10 fn
003512D1  mov      r8d, eax
003512D4  mov      rdx, rbp
003512D7  mov      rcx, rdi
003512DA  call     0x2650b0  ; -> 002650B0 fn
003512DF  mov      rcx, rsi
003512E2  mov      r14, rax
003512E5  call     0x267e10  ; -> 00267E10 fn
003512EA  mov      r8d, eax
003512ED  mov      rdx, rbp
003512F0  mov      rcx, rdi
003512F3  call     0x2650b0  ; -> 002650B0 fn
003512F8  mov      rcx, rsi
003512FB  mov      rbx, rax
003512FE  call     0x267e10  ; -> 00267E10 fn
00351303  mov      r8d, eax
00351306  mov      rdx, rbp
00351309  mov      rcx, rdi
0035130C  call     0x2650b0  ; -> 002650B0 fn
00351311  mov      rdx, qword ptr [r15 + 0xb8]
00351318  mov      rbp, qword ptr [rsp + 0x48]
0035131D  mov      rsi, qword ptr [rsp + 0x50]
00351322  mov      ecx, dword ptr [rdx]
00351324  mov      dword ptr [rax], ecx
00351326  mov      ecx, dword ptr [rdx + 4]
00351329  mov      dword ptr [rbx], ecx
0035132B  mov      eax, dword ptr [rdx + 8]
0035132E  mov      rbx, qword ptr [rsp + 0x40]
00351333  mov      dword ptr [r14], eax
00351336  add      rsp, 0x20
0035133A  pop      r15
0035133C  pop      r14
0035133E  pop      rdi
0035133F  ret      
```

## 00351340 (58 B, extent 00351340-0035137A)

Documented callee on this page: `00267DB0`

```
00351340  push     rbx
00351342  sub      rsp, 0x30
00351346  mov      rcx, r9
00351349  movaps   xmmword ptr [rsp + 0x20], xmm6
0035134E  mov      rbx, rdx
00351351  call     0x267db0  ; -> 00267DB0 fn
00351356  mov      rcx, rbx
00351359  movaps   xmm6, xmm0
0035135C  call     0x2e9560  ; -> 002E9560 fn
00351361  mulss    xmm6, xmm0
00351365  mov      rcx, rbx
00351368  movaps   xmm1, xmm6
0035136B  movaps   xmm6, xmmword ptr [rsp + 0x20]
00351370  add      rsp, 0x30
00351374  pop      rbx
00351375  jmp      0x2e4f40  ; -> 002E4F40 fn
```

## 00351850 (105 B, extent 00351850-003518B9)

Documented callee on this page: `002640C0`

```
00351850  push     rbx
00351852  sub      rsp, 0x20
00351856  mov      rcx, r9
00351859  call     0x267e10  ; -> 00267E10 fn
0035185E  mov      ebx, eax
00351860  call     0x2640c0  ; -> 002640C0 fn
00351865  mov      edx, ebx
00351867  mov      ecx, dword ptr [rax + 0x28]
0035186A  add      rsp, 0x20
0035186E  pop      rbx
0035186F  jmp      0x3dea10  ; -> 003DEA10 fn
00351874  int3     
00351875  int3     
00351876  int3     
00351877  int3     
00351878  int3     
00351879  int3     
0035187A  int3     
0035187B  int3     
0035187C  int3     
0035187D  int3     
0035187E  int3     
0035187F  int3     
00351880  mov      qword ptr [rsp + 8], rbx
00351885  push     rdi
00351886  sub      rsp, 0x20
0035188A  mov      rcx, r9
0035188D  mov      rbx, r9
00351890  mov      rdi, r8
00351893  call     0x267e10  ; -> 00267E10 fn
00351898  mov      rcx, rbx
0035189B  mov      dword ptr [rdi + 4], eax
0035189E  call     0x267e10  ; -> 00267E10 fn
003518A3  mov      ecx, dword ptr [rdi + 4]
003518A6  mov      edx, eax
003518A8  mov      dword ptr [rdi], eax
003518AA  mov      rbx, qword ptr [rsp + 0x30]
003518AF  add      rsp, 0x20
003518B3  pop      rdi
003518B4  jmp      0x1d6a70  ; -> 001D6A70 fn
```

## 00351970 (192 B, extent 00351970-00351A30)

Documented callee on this page: `002650B0`

```
00351970  mov      qword ptr [rsp + 8], rbx
00351975  mov      qword ptr [rsp + 0x10], rsi
0035197A  mov      qword ptr [rsp + 0x18], rdi
0035197F  mov      qword ptr [rsp + 0x20], r14
00351984  push     r15
00351986  sub      rsp, 0x20
0035198A  mov      rsi, r9
0035198D  mov      rdi, rcx
00351990  call     0x2640c0  ; -> 002640C0 fn
00351995  mov      rcx, rsi
00351998  mov      rbx, rax
0035199B  call     0x267e10  ; -> 00267E10 fn
003519A0  mov      r8d, eax
003519A3  mov      rdx, rdi
003519A6  mov      rcx, rbx
003519A9  call     0x2650b0  ; -> 002650B0 fn
003519AE  mov      rcx, rsi
003519B1  mov      r14, rax
003519B4  call     0x267e10  ; -> 00267E10 fn
003519B9  mov      r8d, eax
003519BC  mov      rdx, rdi
003519BF  mov      rcx, rbx
003519C2  call     0x2650b0  ; -> 002650B0 fn
003519C7  mov      rcx, rsi
003519CA  mov      r15, rax
003519CD  call     0x267e10  ; -> 00267E10 fn
003519D2  mov      r8d, eax
003519D5  mov      rdx, rdi
003519D8  mov      rcx, rbx
003519DB  call     0x2650b0  ; -> 002650B0 fn
003519E0  mov      rcx, rsi
003519E3  mov      rbx, rax
003519E6  call     0x267e10  ; -> 00267E10 fn
003519EB  mov      ecx, eax
003519ED  call     0x264010  ; -> 00264010 fn
003519F2  test     rax, rax
003519F5  je       0x351a0d  ; -> 00351A0D
003519F7  mov      rdx, qword ptr [rax + 0xb8]
003519FE  mov      ecx, dword ptr [rdx]
00351A00  mov      dword ptr [rbx], ecx
00351A02  mov      eax, dword ptr [rdx + 4]
00351A05  mov      dword ptr [r15], eax
00351A08  mov      eax, dword ptr [rdx + 8]
00351A0B  jmp      0x351a12  ; -> 00351A12
00351A0D  mov      dword ptr [rbx], eax
00351A0F  mov      dword ptr [r15], eax
00351A12  mov      rbx, qword ptr [rsp + 0x30]
00351A17  mov      rsi, qword ptr [rsp + 0x38]
00351A1C  mov      rdi, qword ptr [rsp + 0x40]
00351A21  mov      dword ptr [r14], eax
00351A24  mov      r14, qword ptr [rsp + 0x48]
00351A29  add      rsp, 0x20
00351A2D  pop      r15
00351A2F  ret      
```
