# F homing pack (FABLE): `17-Presentation-Rendering/Model-And-Motion-Formats/fcp-character-parameter-block.md`

Generated 2026-10-03 04:02 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 8. No bearing page cites them and no documented function calls them directly.

## 00263810 (72 B, extent 00263810-00263858)

Documented callee on this page: `002E9630`

```
00263810  movzx    edx, byte ptr [rcx + 3]
00263814  movzx    eax, dl
00263817  and      al, 0xe0
00263819  cmp      al, 0x60
0026381B  je       0x263852  ; -> 00263852
0026381D  movzx    edx, dl
00263820  xorps    xmm0, xmm0
00263823  shr      edx, 5
00263826  sub      edx, 1
00263829  je       0x263845  ; -> 00263845
0026382B  cmp      edx, 2
0026382E  jne      0x263857  ; -> 00263857
00263830  mov      rax, qword ptr [rcx + 0xb8]
00263837  movss    xmm0, dword ptr [rax + 0xc0]
0026383F  mulss    xmm0, dword ptr [rax + 0x24]
00263844  ret      
00263845  mov      rax, qword ptr [rcx + 0xb8]
0026384C  movss    xmm0, dword ptr [rax + 0x68]
00263851  ret      
00263852  jmp      0x2e9630  ; -> 002E9630 fn
00263857  ret      
```

## 00344050 (101 B, extent 00344050-003440B5)

Documented callee on this page: `0026AC70`

```
00344050  mov      qword ptr [rsp + 8], rbx
00344055  mov      qword ptr [rsp + 0x10], rbp
0034405A  mov      qword ptr [rsp + 0x18], rsi
0034405F  push     rdi
00344060  sub      rsp, 0x30
00344064  mov      rsi, rcx
00344067  movaps   xmmword ptr [rsp + 0x20], xmm6
0034406C  mov      rcx, r9
0034406F  mov      rbx, r9
00344072  mov      rdi, r8
00344075  mov      rbp, rdx
00344078  call     0x267db0  ; -> 00267DB0 fn
0034407D  mov      r9, rbx
00344080  mov      r8, rdi
00344083  mov      rdx, rbp
00344086  mov      rcx, rsi
00344089  movaps   xmm6, xmm0
0034408C  call     0x34be50  ; -> 0034BE50 fn
00344091  movaps   xmm1, xmm6
00344094  mov      rcx, rbp
00344097  mov      rbx, qword ptr [rsp + 0x40]
0034409C  mov      rbp, qword ptr [rsp + 0x48]
003440A1  mov      rsi, qword ptr [rsp + 0x50]
003440A6  movaps   xmm6, xmmword ptr [rsp + 0x20]
003440AB  add      rsp, 0x30
003440AF  pop      rdi
003440B0  jmp      0x26ac70  ; -> 0026AC70 fn
```

## 00349F10 (108 B, extent 00349F10-00349F7C)

Documented callee on this page: `0026A1A0`

```
00349F10  mov      qword ptr [rsp + 8], rbx
00349F15  mov      qword ptr [rsp + 0x10], rbp
00349F1A  mov      qword ptr [rsp + 0x18], rsi
00349F1F  push     rdi
00349F20  sub      rsp, 0x20
00349F24  mov      rbp, rcx
00349F27  mov      rbx, r9
00349F2A  mov      rcx, rdx
00349F2D  mov      rdi, r8
00349F30  mov      rsi, rdx
00349F33  call     0x2644e0  ; -> 002644E0 fn
00349F38  movaps   xmm1, xmm0
00349F3B  mov      rcx, rbx
00349F3E  call     0x267f60  ; -> 00267F60 fn
00349F43  xor      edx, edx
00349F45  mov      rcx, rsi
00349F48  call     0x26a1a0  ; -> 0026A1A0 fn
00349F4D  xor      edx, edx
00349F4F  mov      rcx, rsi
00349F52  call     0x26a1a0  ; -> 0026A1A0 fn
00349F57  mov      r9, rbx
00349F5A  mov      r8, rdi
00349F5D  mov      rdx, rsi
00349F60  mov      rcx, rbp
00349F63  mov      rbx, qword ptr [rsp + 0x30]
00349F68  mov      rbp, qword ptr [rsp + 0x38]
00349F6D  mov      rsi, qword ptr [rsp + 0x40]
00349F72  add      rsp, 0x20
00349F76  pop      rdi
00349F77  jmp      0x357ba0  ; -> 00357BA0 fn
```

## 00356740 (114 B, extent 00356740-003567B2)

Documented callee on this page: `0026A1A0`

```
00356740  mov      qword ptr [rsp + 8], rbx
00356745  mov      qword ptr [rsp + 0x10], rbp
0035674A  mov      qword ptr [rsp + 0x18], rsi
0035674F  push     rdi
00356750  sub      rsp, 0x20
00356754  mov      rbp, rcx
00356757  mov      rbx, r9
0035675A  mov      rcx, rdx
0035675D  mov      rdi, r8
00356760  mov      rsi, rdx
00356763  call     0x2644e0  ; -> 002644E0 fn
00356768  movaps   xmm1, xmm0
0035676B  mov      rcx, rbx
0035676E  call     0x267f60  ; -> 00267F60 fn
00356773  mov      edx, 1
00356778  mov      rcx, rsi
0035677B  call     0x26a1a0  ; -> 0026A1A0 fn
00356780  mov      edx, 1
00356785  mov      rcx, rsi
00356788  call     0x26a1a0  ; -> 0026A1A0 fn
0035678D  mov      r9, rbx
00356790  mov      r8, rdi
00356793  mov      rdx, rsi
00356796  mov      rcx, rbp
00356799  mov      rbx, qword ptr [rsp + 0x30]
0035679E  mov      rbp, qword ptr [rsp + 0x38]
003567A3  mov      rsi, qword ptr [rsp + 0x40]
003567A8  add      rsp, 0x20
003567AC  pop      rdi
003567AD  jmp      0x357ba0  ; -> 00357BA0 fn
```

## 00356AF0 (121 B, extent 00356AF0-00356B69)

Documented callee on this page: `0026A1A0`

```
00356AF0  mov      qword ptr [rsp + 8], rbx
00356AF5  mov      qword ptr [rsp + 0x10], rbp
00356AFA  mov      qword ptr [rsp + 0x18], rsi
00356AFF  push     rdi
00356B00  sub      rsp, 0x20
00356B04  mov      rsi, rdx
00356B07  mov      rbp, rcx
00356B0A  mov      edx, 0x30b
00356B0F  mov      rcx, r9
00356B12  mov      rbx, r9
00356B15  mov      rdi, r8
00356B18  call     0x267f90  ; -> 00267F90 fn
00356B1D  mov      rcx, rsi
00356B20  call     0x2644e0  ; -> 002644E0 fn
00356B25  movaps   xmm1, xmm0
00356B28  mov      rcx, rbx
00356B2B  call     0x267f60  ; -> 00267F60 fn
00356B30  xor      edx, edx
00356B32  mov      rcx, rsi
00356B35  call     0x26a1a0  ; -> 0026A1A0 fn
00356B3A  xor      edx, edx
00356B3C  mov      rcx, rsi
00356B3F  call     0x26a1a0  ; -> 0026A1A0 fn
00356B44  mov      r9, rbx
00356B47  mov      r8, rdi
00356B4A  mov      rdx, rsi
00356B4D  mov      rcx, rbp
00356B50  mov      rbx, qword ptr [rsp + 0x30]
00356B55  mov      rbp, qword ptr [rsp + 0x38]
00356B5A  mov      rsi, qword ptr [rsp + 0x40]
00356B5F  add      rsp, 0x20
00356B63  pop      rdi
00356B64  jmp      0x357ba0  ; -> 00357BA0 fn
```

## 00356F20 (127 B, extent 00356F20-00356F9F)

Documented callee on this page: `0026A1A0`

```
00356F20  mov      qword ptr [rsp + 8], rbx
00356F25  mov      qword ptr [rsp + 0x10], rbp
00356F2A  mov      qword ptr [rsp + 0x18], rsi
00356F2F  push     rdi
00356F30  sub      rsp, 0x20
00356F34  mov      rsi, rdx
00356F37  mov      rbp, rcx
00356F3A  mov      edx, 0x30b
00356F3F  mov      rcx, r9
00356F42  mov      rbx, r9
00356F45  mov      rdi, r8
00356F48  call     0x267f90  ; -> 00267F90 fn
00356F4D  mov      rcx, rsi
00356F50  call     0x2644e0  ; -> 002644E0 fn
00356F55  movaps   xmm1, xmm0
00356F58  mov      rcx, rbx
00356F5B  call     0x267f60  ; -> 00267F60 fn
00356F60  mov      edx, 1
00356F65  mov      rcx, rsi
00356F68  call     0x26a1a0  ; -> 0026A1A0 fn
00356F6D  mov      edx, 1
00356F72  mov      rcx, rsi
00356F75  call     0x26a1a0  ; -> 0026A1A0 fn
00356F7A  mov      r9, rbx
00356F7D  mov      r8, rdi
00356F80  mov      rdx, rsi
00356F83  mov      rcx, rbp
00356F86  mov      rbx, qword ptr [rsp + 0x30]
00356F8B  mov      rbp, qword ptr [rsp + 0x38]
00356F90  mov      rsi, qword ptr [rsp + 0x40]
00356F95  add      rsp, 0x20
00356F99  pop      rdi
00356F9A  jmp      0x357ba0  ; -> 00357BA0 fn
```

## 003573C0 (124 B, extent 003573C0-0035743C)

Documented callee on this page: `0026A1A0`

```
003573C0  mov      qword ptr [rsp + 8], rbx
003573C5  mov      qword ptr [rsp + 0x10], rbp
003573CA  mov      qword ptr [rsp + 0x18], rsi
003573CF  mov      qword ptr [rsp + 0x20], rdi
003573D4  push     r14
003573D6  sub      rsp, 0x20
003573DA  mov      r14, rcx
003573DD  mov      rdi, r9
003573E0  mov      rcx, r9
003573E3  mov      rsi, r8
003573E6  mov      rbp, rdx
003573E9  call     0x267e10  ; -> 00267E10 fn
003573EE  mov      edx, 0x30b
003573F3  mov      rcx, rdi
003573F6  mov      ebx, eax
003573F8  call     0x267f90  ; -> 00267F90 fn
003573FD  mov      edx, ebx
003573FF  mov      rcx, rdi
00357402  call     0x267f90  ; -> 00267F90 fn
00357407  xor      edx, edx
00357409  mov      rcx, rbp
0035740C  call     0x26a1a0  ; -> 0026A1A0 fn
00357411  mov      r9, rdi
00357414  mov      r8, rsi
00357417  mov      rdx, rbp
0035741A  mov      rcx, r14
0035741D  mov      rbx, qword ptr [rsp + 0x30]
00357422  mov      rbp, qword ptr [rsp + 0x38]
00357427  mov      rsi, qword ptr [rsp + 0x40]
0035742C  mov      rdi, qword ptr [rsp + 0x48]
00357431  add      rsp, 0x20
00357435  pop      r14
00357437  jmp      0x357b10  ; -> 00357B10 fn
```

## 00505240 (698 B, extent 00505240-005054FA)

Documented callee on this page: `00265240`

```
00505240  mov      r11, rsp
00505243  push     rbp
00505244  push     rsi
00505245  push     r15
00505247  lea      rbp, [r11 - 0x3f8]
0050524E  sub      rsp, 0x4e0
00505255  movaps   xmmword ptr [r11 - 0x38], xmm6
0050525A  movaps   xmmword ptr [r11 - 0x48], xmm7
0050525F  movaps   xmmword ptr [r11 - 0x58], xmm8
00505264  movaps   xmmword ptr [r11 - 0x78], xmm10
00505269  mov      rax, qword ptr [rip + 0x1a3f5c0]  ; -> 01F44830 [u64 0x00002B992DDFA232]
00505270  xor      rax, rsp
00505273  mov      qword ptr [rbp + 0x370], rax
0050527A  movss    xmm10, dword ptr [rip + 0x17e6925]  ; -> 01CEBBA8 [f32 1]
00505283  xorps    xmm7, xmm7
00505286  movsxd   r15, ecx
00505289  movaps   xmm8, xmm7
0050528D  mov      qword ptr [rsp + 0x64], 0
00505296  movaps   xmm6, xmm2
00505299  mov      dword ptr [rsp + 0x60], 0
005052A1  mov      rsi, rdx
005052A4  mov      dword ptr [rsp + 0x6c], 0x3f800000
005052AC  test     ecx, ecx
005052AE  jle      0x5054c7  ; -> 005054C7
005052B4  mov      qword ptr [r11 + 8], rbx
005052B8  lea      rbx, [rbp - 0x80]
005052BC  mov      qword ptr [r11 - 0x20], rdi
005052C0  lea      rdi, [rsp + 0x70]
005052C5  mov      qword ptr [r11 - 0x28], r14
005052C9  movaps   xmmword ptr [r11 - 0x68], xmm9
005052CE  mov      r14d, r15d
005052D1  mov      rcx, qword ptr [rsi]
005052D4  call     0x263f40  ; -> 00263F40 fn
005052D9  lea      r8, [rdi + 4]
005052DD  mov      qword ptr [rbx], rax
005052E0  lea      r9, [r8 + 4]
005052E4  mov      rdx, rdi
005052E7  mov      rcx, rax
005052EA  call     0x265020  ; -> 00265020 fn
005052EF  mov      rcx, qword ptr [rbx]
005052F2  call     0x263940  ; -> 00263940 fn
005052F7  mov      rcx, qword ptr [rbx]
005052FA  lea      r8, [rsp + 0x38]
005052FF  lea      rdx, [rsp + 0x34]
00505304  movaps   xmm9, xmm0
00505308  call     0x265090  ; -> 00265090 fn
0050530D  movss    xmm1, dword ptr [rbx - 0x10]
00505312  ucomiss  xmm1, xmm7
00505315  jp       0x50535c  ; -> 0050535C
00505317  jne      0x50535c  ; -> 0050535C
00505319  movss    xmm1, dword ptr [rbx - 0xc]
0050531E  ucomiss  xmm1, xmm7
00505321  jp       0x50535c  ; -> 0050535C
00505323  jne      0x50535c  ; -> 0050535C
00505325  movss    xmm0, dword ptr [rbx - 8]
0050532A  ucomiss  xmm0, xmm7
0050532D  jp       0x50535c  ; -> 0050535C
0050532F  jne      0x50535c  ; -> 0050535C
00505331  movss    xmm0, dword ptr [rsp + 0x34]
00505337  maxss    xmm0, dword ptr [rsp + 0x38]
0050533D  movss    dword ptr [rsp + 0x54], xmm9
00505344  mov      dword ptr [rsp + 0x58], 0
0050534C  mov      dword ptr [rsp + 0x5c], 0x3f800000
00505354  movss    dword ptr [rsp + 0x50], xmm0
0050535A  jmp      0x5053cd  ; -> 005053CD
0050535C  lea      rax, [rsp + 0x30]
00505361  mov      rdx, rdi
00505364  lea      r9, [rsp + 0x3c]
00505369  mov      qword ptr [rsp + 0x20], rax
0050536E  lea      r8, [rsp + 0x40]
00505373  lea      rcx, [rsp + 0x60]
00505378  call     0x3cc130  ; -> 003CC130 fn
0050537D  movss    xmm3, dword ptr [rsp + 0x30]
00505383  lea      rax, [rsp + 0x50]
00505388  movss    xmm2, dword ptr [rsp + 0x3c]
0050538E  lea      rcx, [rsp + 0x60]
00505393  movaps   xmm1, xmm7
00505396  mov      qword ptr [rsp + 0x20], rax
0050539B  call     0x3cc2f0  ; -> 003CC2F0 fn
005053A0  movss    xmm0, dword ptr [rsp + 0x34]
005053A6  maxss    xmm0, dword ptr [rsp + 0x38]
005053AC  movss    xmm1, dword ptr [rsp + 0x50]
005053B2  addss    xmm1, xmm0
005053B6  movss    xmm0, dword ptr [rsp + 0x54]
005053BC  addss    xmm0, xmm9
005053C1  movss    dword ptr [rsp + 0x50], xmm1
005053C7  movss    dword ptr [rsp + 0x54], xmm0
005053CD  lea      rax, [rsp + 0x30]
005053D2  lea      r9, [rsp + 0x3c]
005053D7  mov      qword ptr [rsp + 0x20], rax
005053DC  lea      r8, [rsp + 0x40]
005053E1  lea      rdx, [rsp + 0x50]
005053E6  lea      rcx, [rsp + 0x60]
005053EB  call     0x3cc130  ; -> 003CC130 fn
005053F0  movss    xmm0, dword ptr [rsp + 0x30]
005053F6  add      rdi, 0x20
005053FA  maxss    xmm0, xmm8
005053FF  add      rsi, 8
00505403  add      rbx, 0x20
00505407  movaps   xmm8, xmm0
0050540B  sub      r14, 1
0050540F  jne      0x5052d1  ; -> 005052D1
00505415  ucomiss  xmm0, xmm7
00505418  mov      r14, qword ptr [rsp + 0x4d0]
00505420  movaps   xmm9, xmmword ptr [rsp + 0x490]
00505429  jp       0x505431  ; -> 00505431
0050542B  je       0x5054b7  ; -> 005054B7
00505431  divss    xmm6, xmm0
00505435  comiss   xmm10, xmm6
00505439  jbe      0x5054b7  ; -> 005054B7
0050543B  mov      rdi, r15
0050543E  test     r15d, r15d
00505441  jle      0x5054b7  ; -> 005054B7
00505443  lea      rbx, [rbp - 0x80]
00505447  nop      word ptr [rax + rax]
00505450  mov      rcx, qword ptr [rbx]
00505453  movaps   xmm3, xmm6
00505456  mulss    xmm3, dword ptr [rbx - 8]
0050545B  movaps   xmm2, xmm6
0050545E  mulss    xmm2, dword ptr [rbx - 0xc]
00505463  movaps   xmm1, xmm6
00505466  mulss    xmm1, dword ptr [rbx - 0x10]
0050546B  call     0x26b0c0  ; -> 0026B0C0 fn
00505470  mov      rcx, qword ptr [rbx]
00505473  lea      r9, [rsp + 0x44]
00505478  lea      r8, [rsp + 0x48]
0050547D  lea      rdx, [rsp + 0x4c]
00505482  call     0x265240  ; -> 00265240 fn
00505487  movss    xmm3, dword ptr [rsp + 0x44]
0050548D  movss    xmm2, dword ptr [rsp + 0x48]
00505493  movss    xmm1, dword ptr [rsp + 0x4c]
00505499  mov      rcx, qword ptr [rbx]
0050549C  mulss    xmm3, xmm6
005054A0  mulss    xmm2, xmm6
005054A4  mulss    xmm1, xmm6
005054A8  call     0x26b720  ; -> 0026B720 fn
005054AD  lea      rbx, [rbx + 0x20]
005054B1  sub      rdi, 1
005054B5  jne      0x505450  ; -> 00505450
005054B7  mov      rbx, qword ptr [rsp + 0x500]
005054BF  mov      rdi, qword ptr [rsp + 0x4d8]
005054C7  mov      rcx, qword ptr [rbp + 0x370]
005054CE  xor      rcx, rsp
005054D1  call     0x808c40  ; -> 00808C40 fn
005054D6  lea      r11, [rsp + 0x4e0]
005054DE  movaps   xmm6, xmmword ptr [r11 - 0x20]
005054E3  movaps   xmm7, xmmword ptr [r11 - 0x30]
005054E8  movaps   xmm8, xmmword ptr [r11 - 0x40]
005054ED  movaps   xmm10, xmmword ptr [r11 - 0x60]
005054F2  mov      rsp, r11
005054F5  pop      r15
005054F7  pop      rsi
005054F8  pop      rbp
005054F9  ret      
```
