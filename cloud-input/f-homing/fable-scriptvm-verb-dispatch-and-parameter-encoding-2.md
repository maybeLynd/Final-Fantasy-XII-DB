# F homing pack (FABLE): `01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md`

Generated 2026-10-03 04:02 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 23. No bearing page cites them and no documented function calls them directly.

## 00510100 (84 B, extent 00510100-00510154)

Documented callee on this page: `0026B4E0`

```
00510100  push     rbx
00510102  sub      rsp, 0x20
00510106  mov      rbx, rcx
00510109  mov      rcx, r9
0051010C  call     0x267e10  ; -> 00267E10 fn
00510111  test     eax, eax
00510113  je       0x510140  ; -> 00510140
00510115  cmp      eax, 1
00510118  je       0x51012c  ; -> 0051012C
0051011A  or       eax, 0xffffffff
0051011D  mov      rcx, rbx
00510120  mov      edx, eax
00510122  add      rsp, 0x20
00510126  pop      rbx
00510127  jmp      0x26b4e0  ; -> 0026B4E0 fn
0051012C  call     0x318390  ; -> 00318390 fn
00510131  mov      edx, eax
00510133  mov      rcx, rbx
00510136  add      rsp, 0x20
0051013A  pop      rbx
0051013B  jmp      0x26b4e0  ; -> 0026B4E0 fn
00510140  call     0x318380  ; -> 00318380 fn
00510145  mov      edx, eax
00510147  mov      rcx, rbx
0051014A  add      rsp, 0x20
0051014E  pop      rbx
0051014F  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 00510AA0 (53 B, extent 00510AA0-00510AD5)

Documented callee on this page: `00280120`

```
00510AA0  push     rbx
00510AA2  sub      rsp, 0x20
00510AA6  mov      rbx, r8
00510AA9  call     0x280120  ; -> 00280120 fn
00510AAE  test     eax, eax
00510AB0  je       0x510aba  ; -> 00510ABA
00510AB2  xor      eax, eax
00510AB4  add      rsp, 0x20
00510AB8  pop      rbx
00510AB9  ret      
00510ABA  mov      ecx, dword ptr [rbx]
00510ABC  mov      edx, 1
00510AC1  call     0x2d7800  ; -> 002D7800 fn
00510AC6  xor      ecx, ecx
00510AC8  test     eax, eax
00510ACA  sete     cl
00510ACD  mov      eax, ecx
00510ACF  add      rsp, 0x20
00510AD3  pop      rbx
00510AD4  ret      
```

## 00510B40 (50 B, extent 00510B40-00510B72)

Documented callee on this page: `00280120`

```
00510B40  push     rbx
00510B42  sub      rsp, 0x20
00510B46  mov      rbx, r8
00510B49  call     0x280120  ; -> 00280120 fn
00510B4E  test     eax, eax
00510B50  je       0x510b5a  ; -> 00510B5A
00510B52  xor      eax, eax
00510B54  add      rsp, 0x20
00510B58  pop      rbx
00510B59  ret      
00510B5A  mov      ecx, dword ptr [rbx]
00510B5C  xor      edx, edx
00510B5E  call     0x2d7800  ; -> 002D7800 fn
00510B63  xor      ecx, ecx
00510B65  test     eax, eax
00510B67  sete     cl
00510B6A  mov      eax, ecx
00510B6C  add      rsp, 0x20
00510B70  pop      rbx
00510B71  ret      
```

## 00510F30 (216 B, extent 00510F30-00511008)

Documented callee on this page: `002650B0`

```
00510F30  push     rbp
00510F32  push     r15
00510F34  sub      rsp, 0x28
00510F38  mov      rbp, r9
00510F3B  mov      r15, rcx
00510F3E  call     0x280120  ; -> 00280120 fn
00510F43  test     eax, eax
00510F45  jne      0x511000  ; -> 00511000
00510F4B  mov      qword ptr [rsp + 0x40], rbx
00510F50  mov      qword ptr [rsp + 0x48], rsi
00510F55  mov      qword ptr [rsp + 0x50], rdi
00510F5A  mov      qword ptr [rsp + 0x20], r14
00510F5F  call     0x2640c0  ; -> 002640C0 fn
00510F64  mov      rcx, rbp
00510F67  mov      rbx, rax
00510F6A  call     0x267e10  ; -> 00267E10 fn
00510F6F  mov      r8d, eax
00510F72  mov      rdx, r15
00510F75  mov      rcx, rbx
00510F78  call     0x2650b0  ; -> 002650B0 fn
00510F7D  mov      rcx, rbp
00510F80  mov      r14, rax
00510F83  call     0x267e10  ; -> 00267E10 fn
00510F88  mov      r8d, eax
00510F8B  mov      rdx, r15
00510F8E  mov      rcx, rbx
00510F91  call     0x2650b0  ; -> 002650B0 fn
00510F96  mov      rcx, rbp
00510F99  mov      rsi, rax
00510F9C  call     0x267e10  ; -> 00267E10 fn
00510FA1  mov      r8d, eax
00510FA4  mov      rdx, r15
00510FA7  mov      rcx, rbx
00510FAA  call     0x2650b0  ; -> 002650B0 fn
00510FAF  mov      rcx, rbp
00510FB2  mov      rdi, rax
00510FB5  call     0x267e10  ; -> 00267E10 fn
00510FBA  mov      r8d, eax
00510FBD  mov      rdx, r15
00510FC0  mov      rcx, rbx
00510FC3  call     0x2650b0  ; -> 002650B0 fn
00510FC8  mov      rcx, rbp
00510FCB  mov      rbx, rax
00510FCE  call     0x267e10  ; -> 00267E10 fn
00510FD3  mov      dword ptr [rbx], 0x20
00510FD9  mov      rbx, qword ptr [rsp + 0x40]
00510FDE  mov      dword ptr [rdi], 0x20
00510FE4  mov      rdi, qword ptr [rsp + 0x50]
00510FE9  mov      dword ptr [rsi], 0x20
00510FEF  mov      rsi, qword ptr [rsp + 0x48]
00510FF4  mov      dword ptr [r14], 0x20
00510FFB  mov      r14, qword ptr [rsp + 0x20]
00511000  add      rsp, 0x28
00511004  pop      r15
00511006  pop      rbp
00511007  ret      
```

## 00511010 (232 B, extent 00511010-005110F8)

Documented callee on this page: `002650B0`

```
00511010  push     rbp
00511012  push     r15
00511014  sub      rsp, 0x38
00511018  mov      rbp, r9
0051101B  mov      r15, rcx
0051101E  call     0x280120  ; -> 00280120 fn
00511023  test     eax, eax
00511025  jne      0x5110f0  ; -> 005110F0
0051102B  mov      qword ptr [rsp + 0x50], rbx
00511030  mov      qword ptr [rsp + 0x58], rsi
00511035  mov      qword ptr [rsp + 0x60], rdi
0051103A  mov      qword ptr [rsp + 0x30], r14
0051103F  call     0x2640c0  ; -> 002640C0 fn
00511044  mov      rcx, rbp
00511047  mov      rbx, rax
0051104A  call     0x267e10  ; -> 00267E10 fn
0051104F  mov      r8d, eax
00511052  mov      rdx, r15
00511055  mov      rcx, rbx
00511058  call     0x2650b0  ; -> 002650B0 fn
0051105D  mov      rcx, rbp
00511060  mov      r14, rax
00511063  call     0x267e10  ; -> 00267E10 fn
00511068  mov      r8d, eax
0051106B  mov      rdx, r15
0051106E  mov      rcx, rbx
00511071  call     0x2650b0  ; -> 002650B0 fn
00511076  mov      rcx, rbp
00511079  mov      rsi, rax
0051107C  call     0x267e10  ; -> 00267E10 fn
00511081  mov      r8d, eax
00511084  mov      rdx, r15
00511087  mov      rcx, rbx
0051108A  call     0x2650b0  ; -> 002650B0 fn
0051108F  mov      rcx, rbp
00511092  mov      rdi, rax
00511095  call     0x267e10  ; -> 00267E10 fn
0051109A  mov      r8d, eax
0051109D  mov      rdx, r15
005110A0  mov      rcx, rbx
005110A3  call     0x2650b0  ; -> 002650B0 fn
005110A8  mov      rcx, rbp
005110AB  mov      rbx, rax
005110AE  call     0x267e10  ; -> 00267E10 fn
005110B3  lea      rdx, [rsp + 0x20]
005110B8  mov      ecx, eax
005110BA  call     0x55fed0  ; -> 0055FED0 fn
005110BF  movsx    ecx, word ptr [rsp + 0x20]
005110C4  mov      dword ptr [rbx], ecx
005110C6  movsx    eax, word ptr [rsp + 0x22]
005110CB  mov      rbx, qword ptr [rsp + 0x50]
005110D0  mov      dword ptr [rdi], eax
005110D2  movsx    eax, word ptr [rsp + 0x24]
005110D7  mov      rdi, qword ptr [rsp + 0x60]
005110DC  mov      dword ptr [rsi], eax
005110DE  movsx    eax, word ptr [rsp + 0x26]
005110E3  mov      rsi, qword ptr [rsp + 0x58]
005110E8  mov      dword ptr [r14], eax
005110EB  mov      r14, qword ptr [rsp + 0x30]
005110F0  add      rsp, 0x38
005110F4  pop      r15
005110F6  pop      rbp
005110F7  ret      
```

## 00511200 (84 B, extent 00511200-00511254)

Documented callee on this page: `00280120`

```
00511200  push     rsi
00511202  sub      rsp, 0x20
00511206  mov      rsi, r9
00511209  call     0x280120  ; -> 00280120 fn
0051120E  test     eax, eax
00511210  jne      0x51124e  ; -> 0051124E
00511212  mov      qword ptr [rsp + 0x30], rbx
00511217  mov      rcx, rsi
0051121A  mov      qword ptr [rsp + 0x38], rdi
0051121F  call     0x267e10  ; -> 00267E10 fn
00511224  mov      rcx, rsi
00511227  mov      edi, eax
00511229  call     0x267e10  ; -> 00267E10 fn
0051122E  mov      rcx, rsi
00511231  mov      ebx, eax
00511233  call     0x267e10  ; -> 00267E10 fn
00511238  mov      r8d, edi
0051123B  mov      edx, ebx
0051123D  mov      ecx, eax
0051123F  call     0x2d7710  ; -> 002D7710 fn
00511244  mov      rdi, qword ptr [rsp + 0x38]
00511249  mov      rbx, qword ptr [rsp + 0x30]
0051124E  add      rsp, 0x20
00511252  pop      rsi
00511253  ret      
```

## 00511360 (61 B, extent 00511360-0051139D)

Documented callee on this page: `00280120`

```
00511360  push     rdi
00511362  sub      rsp, 0x20
00511366  mov      rdi, r9
00511369  call     0x280120  ; -> 00280120 fn
0051136E  test     eax, eax
00511370  jne      0x511397  ; -> 00511397
00511372  mov      rcx, rdi
00511375  mov      qword ptr [rsp + 0x30], rbx
0051137A  call     0x267e10  ; -> 00267E10 fn
0051137F  mov      rcx, rdi
00511382  mov      ebx, eax
00511384  call     0x267e10  ; -> 00267E10 fn
00511389  mov      edx, ebx
0051138B  mov      ecx, eax
0051138D  call     0x56a140  ; -> 0056A140 fn
00511392  mov      rbx, qword ptr [rsp + 0x30]
00511397  add      rsp, 0x20
0051139B  pop      rdi
0051139C  ret      
```

## 00511400 (46 B, extent 00511400-0051142E)

Documented callee on this page: `00280120`

```
00511400  push     rbx
00511402  sub      rsp, 0x20
00511406  mov      rbx, rcx
00511409  call     0x280120  ; -> 00280120 fn
0051140E  test     eax, eax
00511410  jne      0x511428  ; -> 00511428
00511412  xor      ecx, ecx
00511414  call     0x2cde80  ; -> 002CDE80 fn
00511419  mov      edx, eax
0051141B  mov      rcx, rbx
0051141E  add      rsp, 0x20
00511422  pop      rbx
00511423  jmp      0x26b4e0  ; -> 0026B4E0 fn
00511428  add      rsp, 0x20
0051142C  pop      rbx
0051142D  ret      
```

## 00511460 (48 B, extent 00511460-00511490)

Documented callee on this page: `00280120`

```
00511460  push     rbx
00511462  sub      rsp, 0x20
00511466  mov      rbx, r8
00511469  call     0x280120  ; -> 00280120 fn
0051146E  test     eax, eax
00511470  je       0x51147a  ; -> 0051147A
00511472  xor      eax, eax
00511474  add      rsp, 0x20
00511478  pop      rbx
00511479  ret      
0051147A  xor      ecx, ecx
0051147C  call     0x2cde80  ; -> 002CDE80 fn
00511481  xor      ecx, ecx
00511483  cmp      dword ptr [rbx], eax
00511485  setne    cl
00511488  mov      eax, ecx
0051148A  add      rsp, 0x20
0051148E  pop      rbx
0051148F  ret      
```

## 00511490 (44 B, extent 00511490-005114BC)

Documented callee on this page: `00280120`

```
00511490  push     rbx
00511492  sub      rsp, 0x20
00511496  mov      rbx, rcx
00511499  call     0x280120  ; -> 00280120 fn
0051149E  test     eax, eax
005114A0  jne      0x5114b6  ; -> 005114B6
005114A2  call     0x2c1370  ; -> 002C1370 fn
005114A7  mov      edx, eax
005114A9  mov      rcx, rbx
005114AC  add      rsp, 0x20
005114B0  pop      rbx
005114B1  jmp      0x26b4e0  ; -> 0026B4E0 fn
005114B6  add      rsp, 0x20
005114BA  pop      rbx
005114BB  ret      
```

## 005114C0 (46 B, extent 005114C0-005114EE)

Documented callee on this page: `00280120`

```
005114C0  push     rbx
005114C2  sub      rsp, 0x20
005114C6  mov      rbx, r8
005114C9  call     0x280120  ; -> 00280120 fn
005114CE  test     eax, eax
005114D0  je       0x5114da  ; -> 005114DA
005114D2  xor      eax, eax
005114D4  add      rsp, 0x20
005114D8  pop      rbx
005114D9  ret      
005114DA  call     0x2c1370  ; -> 002C1370 fn
005114DF  xor      ecx, ecx
005114E1  cmp      dword ptr [rbx], eax
005114E3  setne    cl
005114E6  mov      eax, ecx
005114E8  add      rsp, 0x20
005114EC  pop      rbx
005114ED  ret      
```

## 005115B0 (30 B, extent 005115B0-005115CE)

Documented callee on this page: `00280120`

```
005115B0  sub      rsp, 0x28
005115B4  call     0x280120  ; -> 00280120 fn
005115B9  test     eax, eax
005115BB  jne      0x5115c9  ; -> 005115C9
005115BD  or       ecx, 0xffffffff
005115C0  add      rsp, 0x28
005115C4  jmp      0x2d75f0  ; -> 002D75F0 fn
005115C9  add      rsp, 0x28
005115CD  ret      
```

## 005118D0 (41 B, extent 005118D0-005118F9)

Documented callee on this page: `00280120`

```
005118D0  sub      rsp, 0x28
005118D4  call     0x280120  ; -> 00280120 fn
005118D9  test     eax, eax
005118DB  je       0x5118e4  ; -> 005118E4
005118DD  xor      eax, eax
005118DF  add      rsp, 0x28
005118E3  ret      
005118E4  xor      ecx, ecx
005118E6  call     0x2d77c0  ; -> 002D77C0 fn
005118EB  xor      ecx, ecx
005118ED  test     eax, eax
005118EF  sete     cl
005118F2  mov      eax, ecx
005118F4  add      rsp, 0x28
005118F8  ret      
```

## 005119C0 (44 B, extent 005119C0-005119EC)

Documented callee on this page: `00280120`

```
005119C0  sub      rsp, 0x28
005119C4  call     0x280120  ; -> 00280120 fn
005119C9  test     eax, eax
005119CB  je       0x5119d4  ; -> 005119D4
005119CD  xor      eax, eax
005119CF  add      rsp, 0x28
005119D3  ret      
005119D4  mov      ecx, 1
005119D9  call     0x2d77c0  ; -> 002D77C0 fn
005119DE  xor      ecx, ecx
005119E0  test     eax, eax
005119E2  sete     cl
005119E5  mov      eax, ecx
005119E7  add      rsp, 0x28
005119EB  ret      
```

## 00511AA0 (30 B, extent 00511AA0-00511ABE)

Documented callee on this page: `00280120`

```
00511AA0  sub      rsp, 0x28
00511AA4  call     0x280120  ; -> 00280120 fn
00511AA9  test     eax, eax
00511AAB  jne      0x511ab9  ; -> 00511AB9
00511AAD  lea      ecx, [rax + 1]
00511AB0  add      rsp, 0x28
00511AB4  jmp      0x2d7d40  ; -> 002D7D40 fn
00511AB9  add      rsp, 0x28
00511ABD  ret      
```

## 00511B00 (47 B, extent 00511B00-00511B2F)

Documented callee on this page: `00280120`

```
00511B00  push     rbx
00511B02  sub      rsp, 0x20
00511B06  mov      rbx, r9
00511B09  call     0x280120  ; -> 00280120 fn
00511B0E  test     eax, eax
00511B10  jne      0x511b29  ; -> 00511B29
00511B12  mov      rcx, rbx
00511B15  call     0x267e10  ; -> 00267E10 fn
00511B1A  xor      eax, 1
00511B1D  mov      ecx, eax
00511B1F  add      rsp, 0x20
00511B23  pop      rbx
00511B24  jmp      0x2d7d30  ; -> 002D7D30 fn
00511B29  add      rsp, 0x20
00511B2D  pop      rbx
00511B2E  ret      
```

## 00511B70 (84 B, extent 00511B70-00511BC4)

Documented callee on this page: `00280120`

```
00511B70  push     rsi
00511B72  sub      rsp, 0x20
00511B76  mov      rsi, r9
00511B79  call     0x280120  ; -> 00280120 fn
00511B7E  test     eax, eax
00511B80  jne      0x511bbe  ; -> 00511BBE
00511B82  mov      qword ptr [rsp + 0x30], rbx
00511B87  mov      rcx, rsi
00511B8A  mov      qword ptr [rsp + 0x38], rdi
00511B8F  call     0x267e10  ; -> 00267E10 fn
00511B94  mov      rcx, rsi
00511B97  mov      edi, eax
00511B99  call     0x267e10  ; -> 00267E10 fn
00511B9E  mov      rcx, rsi
00511BA1  mov      ebx, eax
00511BA3  call     0x267e10  ; -> 00267E10 fn
00511BA8  mov      r8d, edi
00511BAB  mov      edx, ebx
00511BAD  mov      ecx, eax
00511BAF  call     0x567ae0  ; -> 00567AE0 fn
00511BB4  mov      rdi, qword ptr [rsp + 0x38]
00511BB9  mov      rbx, qword ptr [rsp + 0x30]
00511BBE  add      rsp, 0x20
00511BC2  pop      rsi
00511BC3  ret      
```

## 00511D60 (49 B, extent 00511D60-00511D91)

Documented callee on this page: `00280120`

```
00511D60  push     rbx
00511D62  sub      rsp, 0x20
00511D66  mov      rbx, r9
00511D69  call     0x280120  ; -> 00280120 fn
00511D6E  test     eax, eax
00511D70  jne      0x511d8b  ; -> 00511D8B
00511D72  mov      rcx, rbx
00511D75  call     0x267e10  ; -> 00267E10 fn
00511D7A  mov      r8d, eax
00511D7D  xor      edx, edx
00511D7F  xor      ecx, ecx
00511D81  add      rsp, 0x20
00511D85  pop      rbx
00511D86  jmp      0x2d7bf0  ; -> 002D7BF0 fn
00511D8B  add      rsp, 0x20
00511D8F  pop      rbx
00511D90  ret      
```

## 00511DA0 (50 B, extent 00511DA0-00511DD2)

Documented callee on this page: `00280120`

```
00511DA0  push     rbx
00511DA2  sub      rsp, 0x20
00511DA6  mov      rbx, r9
00511DA9  call     0x280120  ; -> 00280120 fn
00511DAE  test     eax, eax
00511DB0  jne      0x511dcc  ; -> 00511DCC
00511DB2  mov      rcx, rbx
00511DB5  call     0x267e10  ; -> 00267E10 fn
00511DBA  xor      edx, edx
00511DBC  mov      r8d, eax
00511DBF  lea      ecx, [rdx + 1]
00511DC2  add      rsp, 0x20
00511DC6  pop      rbx
00511DC7  jmp      0x2d7bf0  ; -> 002D7BF0 fn
00511DCC  add      rsp, 0x20
00511DD0  pop      rbx
00511DD1  ret      
```

## 00511E60 (52 B, extent 00511E60-00511E94)

Documented callee on this page: `00280120`

```
00511E60  push     rbx
00511E62  sub      rsp, 0x20
00511E66  mov      rbx, r9
00511E69  call     0x280120  ; -> 00280120 fn
00511E6E  test     eax, eax
00511E70  jne      0x511e8e  ; -> 00511E8E
00511E72  mov      rcx, rbx
00511E75  call     0x267e10  ; -> 00267E10 fn
00511E7A  mov      r8d, eax
00511E7D  mov      edx, 1
00511E82  xor      ecx, ecx
00511E84  add      rsp, 0x20
00511E88  pop      rbx
00511E89  jmp      0x2d7bf0  ; -> 002D7BF0 fn
00511E8E  add      rsp, 0x20
00511E92  pop      rbx
00511E93  ret      
```

## 00511EE0 (52 B, extent 00511EE0-00511F14)

Documented callee on this page: `00280120`

```
00511EE0  push     rbx
00511EE2  sub      rsp, 0x20
00511EE6  mov      rbx, r9
00511EE9  call     0x280120  ; -> 00280120 fn
00511EEE  test     eax, eax
00511EF0  jne      0x511f0e  ; -> 00511F0E
00511EF2  mov      rcx, rbx
00511EF5  call     0x267e10  ; -> 00267E10 fn
00511EFA  mov      edx, 1
00511EFF  mov      r8d, eax
00511F02  mov      ecx, edx
00511F04  add      rsp, 0x20
00511F08  pop      rbx
00511F09  jmp      0x2d7bf0  ; -> 002D7BF0 fn
00511F0E  add      rsp, 0x20
00511F12  pop      rbx
00511F13  ret      
```

## 005120C0 (27 B, extent 005120C0-005120DB)

Documented callee on this page: `00280120`

```
005120C0  sub      rsp, 0x28
005120C4  call     0x280120  ; -> 00280120 fn
005120C9  test     eax, eax
005120CB  jne      0x5120d6  ; -> 005120D6
005120CD  add      rsp, 0x28
005120D1  jmp      0x2d7840  ; -> 002D7840 fn
005120D6  add      rsp, 0x28
005120DA  ret      
```

## 00512180 (27 B, extent 00512180-0051219B)

Documented callee on this page: `00280120`

```
00512180  sub      rsp, 0x28
00512184  call     0x280120  ; -> 00280120 fn
00512189  test     eax, eax
0051218B  jne      0x512196  ; -> 00512196
0051218D  add      rsp, 0x28
00512191  jmp      0x295d00  ; -> 00295D00 fn
00512196  add      rsp, 0x28
0051219A  ret      
```
