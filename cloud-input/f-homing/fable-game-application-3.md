# F homing pack (FABLE): `00-Engine-Core-Runtime/Application-Root/game-application.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 20. No bearing page cites them and no documented function calls them directly.

## 0019EC40 (320 B, extent 0019EC40-0019ED80)

Documented callee on this page: `001EDF00`

```
0019EC40  mov      rax, rsp
0019EC43  push     rdi
0019EC44  sub      rsp, 0x170
0019EC4B  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0019EC54  mov      qword ptr [rax + 0x18], rbx
0019EC58  mov      qword ptr [rax + 0x20], rsi
0019EC5C  mov      rax, qword ptr [rip + 0x1da5bcd]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0019EC63  xor      rax, rsp
0019EC66  mov      qword ptr [rsp + 0x160], rax
0019EC6E  mov      edi, edx
0019EC70  mov      rbx, rcx
0019EC73  mov      r8, qword ptr [rcx + 8]
0019EC77  mov      r9, qword ptr [rcx]
0019EC7A  mov      rcx, r8
0019EC7D  sub      rcx, r9
0019EC80  movabs   rsi, 0x6bca1af286bca1b
0019EC8A  mov      rax, rsi
0019EC8D  imul     rcx
0019EC90  sar      rdx, 3
0019EC94  mov      rax, rdx
0019EC97  shr      rax, 0x3f
0019EC9B  add      rdx, rax
0019EC9E  cmp      edi, edx
0019ECA0  jbe      0x19ed49  ; -> 0019ED49
0019ECA6  xor      edx, edx
0019ECA8  mov      r8d, 0x130
0019ECAE  lea      rcx, [rsp + 0x30]
0019ECB3  call     0x861ec0  ; -> 00861EC0 fn
0019ECB8  xorps    xmm0, xmm0
0019ECBB  movdqa   xmmword ptr [rsp + 0x130], xmm0
0019ECC4  mov      qword ptr [rsp + 0x140], 0
0019ECD0  lea      rdx, [rip + 0x727281]  ; -> 008C5F58 [str "EASTL vector"]
0019ECD7  lea      rcx, [rsp + 0x148]
0019ECDF  call     0x1edf00  ; -> 001EDF00 fn
0019ECE4  nop      
0019ECE5  mov      rcx, qword ptr [rbx + 8]
0019ECE9  sub      rcx, qword ptr [rbx]
0019ECEC  mov      rax, rsi
0019ECEF  imul     rcx
0019ECF2  sar      rdx, 3
0019ECF6  mov      rax, rdx
0019ECF9  shr      rax, 0x3f
0019ECFD  add      rdx, rax
0019ED00  sub      edi, edx
0019ED02  lea      r9, [rsp + 0x30]
0019ED07  mov      r8d, edi
0019ED0A  mov      rdx, qword ptr [rbx + 8]
0019ED0E  mov      rcx, rbx
0019ED11  call     0x19e010  ; -> 0019E010 fn
0019ED16  nop      
0019ED17  mov      rdx, qword ptr [rsp + 0x130]
0019ED1F  test     rdx, rdx
0019ED22  je       0x19ed47  ; -> 0019ED47
0019ED24  mov      r8, qword ptr [rsp + 0x140]
0019ED2C  sub      r8, rdx
0019ED2F  and      r8, 0xfffffffffffffff8
0019ED33  lea      rcx, [rsp + 0x148]
0019ED3B  mov      rax, qword ptr [rsp + 0x148]
0019ED43  call     qword ptr [rax + 0x18]
0019ED46  nop      
0019ED47  jmp      0x19ed5b  ; -> 0019ED5B
0019ED49  imul     rdx, rdi, 0x130
0019ED50  add      rdx, r9
0019ED53  mov      rcx, rbx
0019ED56  call     0x19ea20  ; -> 0019EA20 fn
0019ED5B  mov      rcx, qword ptr [rsp + 0x160]
0019ED63  xor      rcx, rsp
0019ED66  call     0x808c40  ; -> 00808C40 fn
0019ED6B  lea      r11, [rsp + 0x170]
0019ED73  mov      rbx, qword ptr [r11 + 0x20]
0019ED77  mov      rsi, qword ptr [r11 + 0x28]
0019ED7B  mov      rsp, r11
0019ED7E  pop      rdi
0019ED7F  ret      
```

## 0019ED80 (208 B, extent 0019ED80-0019EE50)

Documented callee on this page: `00861EC0`

```
0019ED80  mov      qword ptr [rsp + 8], rbx
0019ED85  mov      qword ptr [rsp + 0x10], rsi
0019ED8A  mov      qword ptr [rsp + 0x18], rdi
0019ED8F  push     r14
0019ED91  sub      rsp, 0x140
0019ED98  mov      rsi, qword ptr [rcx + 8]
0019ED9C  mov      r14, rcx
0019ED9F  mov      rcx, qword ptr [rcx]
0019EDA2  mov      r8, rsi
0019EDA5  sub      r8, rcx
0019EDA8  mov      edi, edx
0019EDAA  movabs   rax, 0xea0ea0ea0ea0ea1
0019EDB4  imul     r8
0019EDB7  mov      rbx, rdx
0019EDBA  sar      rbx, 4
0019EDBE  mov      rax, rbx
0019EDC1  shr      rax, 0x3f
0019EDC5  add      rbx, rax
0019EDC8  cmp      edi, ebx
0019EDCA  jbe      0x19edf5  ; -> 0019EDF5
0019EDCC  xor      edx, edx
0019EDCE  lea      rcx, [rsp + 0x20]
0019EDD3  mov      r8d, 0x118
0019EDD9  call     0x861ec0  ; -> 00861EC0 fn
0019EDDE  sub      edi, ebx
0019EDE0  lea      r9, [rsp + 0x20]
0019EDE5  mov      r8d, edi
0019EDE8  mov      rdx, rsi
0019EDEB  mov      rcx, r14
0019EDEE  call     0x19e2c0  ; -> 0019E2C0 fn
0019EDF3  jmp      0x19ee36  ; -> 0019EE36
0019EDF5  imul     rbx, rdi, 0x118
0019EDFC  mov      rdx, rsi
0019EDFF  add      rbx, rcx
0019EE02  mov      rcx, rsi
0019EE05  mov      r8, rbx
0019EE08  call     0x19d050  ; -> 0019D050 fn
0019EE0D  sub      rsi, rbx
0019EE10  movabs   rax, 0xf15f15f15f15f15f
0019EE1A  imul     rsi
0019EE1D  sar      rdx, 4
0019EE21  mov      rax, rdx
0019EE24  shr      rax, 0x3f
0019EE28  add      rdx, rax
0019EE2B  imul     rax, rdx, 0x118
0019EE32  add      qword ptr [r14 + 8], rax
0019EE36  lea      r11, [rsp + 0x140]
0019EE3E  mov      rbx, qword ptr [r11 + 0x10]
0019EE42  mov      rsi, qword ptr [r11 + 0x18]
0019EE46  mov      rdi, qword ptr [r11 + 0x20]
0019EE4A  mov      rsp, r11
0019EE4D  pop      r14
0019EE4F  ret      
```

## 0019F9F0 (82 B, extent 0019F9F0-0019FA42)

Documented callee on this page: `00584730`

```
0019F9F0  push     rdi
0019F9F2  sub      rsp, 0x30
0019F9F6  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0019F9FF  mov      qword ptr [rsp + 0x40], rbx
0019FA04  mov      edi, edx
0019FA06  mov      rbx, rcx
0019FA09  call     0x19f930  ; -> 0019F930 fn
0019FA0E  nop      
0019FA0F  test     dil, 1
0019FA13  je       0x19fa34  ; -> 0019FA34
0019FA15  test     dil, 4
0019FA19  jne      0x19fa26  ; -> 0019FA26
0019FA1B  mov      rcx, rbx
0019FA1E  call     0x584730  ; -> 00584730 fn
0019FA23  nop      
0019FA24  jmp      0x19fa34  ; -> 0019FA34
0019FA26  mov      edx, 0x140228
0019FA2B  mov      rcx, rbx
0019FA2E  call     0x16d6a0  ; -> 0016D6A0 fn
0019FA33  nop      
0019FA34  mov      rax, rbx
0019FA37  mov      rbx, qword ptr [rsp + 0x40]
0019FA3C  add      rsp, 0x30
0019FA40  pop      rdi
0019FA41  ret      
```

## 001A3190 (130 B, extent 001A3190-001A3212)

Documented callee on this page: `001A4BF0`

```
001A3190  push     rdi
001A3192  sub      rsp, 0x30
001A3196  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001A319F  mov      qword ptr [rsp + 0x48], rbx
001A31A4  mov      qword ptr [rsp + 0x58], rsi
001A31A9  mov      rsi, rdx
001A31AC  add      rcx, 0x30
001A31B0  mov      rax, qword ptr [rcx]
001A31B3  xor      r8d, r8d
001A31B6  lea      edx, [r8 + 0x40]
001A31BA  call     qword ptr [rax + 0x10]
001A31BD  mov      rdi, rax
001A31C0  mov      qword ptr [rsp + 0x40], rax
001A31C5  lea      rbx, [rax + 0x20]
001A31C9  mov      qword ptr [rsp + 0x50], rbx
001A31CE  test     rbx, rbx
001A31D1  je       0x1a3202  ; -> 001A3202
001A31D3  xor      eax, eax
001A31D5  mov      qword ptr [rbx], rax
001A31D8  mov      qword ptr [rbx + 8], rax
001A31DC  mov      qword ptr [rbx + 0x10], rax
001A31E0  lea      rdx, [rsi + 0x18]
001A31E4  lea      rcx, [rbx + 0x18]
001A31E8  call     0x1edf00  ; -> 001EDF00 fn
001A31ED  mov      r8, qword ptr [rsi + 8]
001A31F1  mov      rdx, qword ptr [rsi]
001A31F4  mov      rcx, rbx
001A31F7  call     0x1a4bf0  ; -> 001A4BF0 fn
001A31FC  nop      
001A31FD  mov      rax, rdi
001A3200  jmp      0x1a3202  ; -> 001A3202
001A3202  mov      rbx, qword ptr [rsp + 0x48]
001A3207  mov      rsi, qword ptr [rsp + 0x58]
001A320C  add      rsp, 0x30
001A3210  pop      rdi
001A3211  ret      
```

## 001A6CC0 (184 B, extent 001A6CC0-001A6D78)

Documented callee on this page: `001AF2B0`

```
001A6CC0  mov      qword ptr [rsp + 0x10], rbx
001A6CC5  mov      qword ptr [rsp + 0x18], rsi
001A6CCA  push     rdi
001A6CCB  sub      rsp, 0x20
001A6CCF  mov      rbx, qword ptr [rcx + 0x4f8]
001A6CD6  lea      rdi, [rcx + 0x4f0]
001A6CDD  mov      rsi, rcx
001A6CE0  cmp      rbx, rdi
001A6CE3  je       0x1a6d0c  ; -> 001A6D0C
001A6CE5  nop      word ptr [rax + rax]
001A6CF0  mov      rcx, qword ptr [rbx + 0x28]
001A6CF4  xor      edx, edx
001A6CF6  mov      rax, qword ptr [rcx]
001A6CF9  call     qword ptr [rax + 8]
001A6CFC  mov      rcx, rbx
001A6CFF  call     0x16d6d0  ; -> 0016D6D0 fn
001A6D04  mov      rbx, rax
001A6D07  cmp      rax, rdi
001A6D0A  jne      0x1a6cf0  ; -> 001A6CF0
001A6D0C  lea      rdi, [rsi + 0x4e8]
001A6D13  mov      rsi, qword ptr [rdi + 0x18]
001A6D17  test     rsi, rsi
001A6D1A  je       0x1a6d51  ; -> 001A6D51
001A6D1C  mov      qword ptr [rsp + 0x30], r14
001A6D21  mov      rdx, qword ptr [rsi]
001A6D24  mov      rcx, rdi
001A6D27  call     0x1af2b0  ; -> 001AF2B0 fn
001A6D2C  mov      rax, qword ptr [rdi + 0x30]
001A6D30  lea      rcx, [rdi + 0x30]
001A6D34  mov      rbx, qword ptr [rsi + 8]
001A6D38  mov      r8d, 0x30
001A6D3E  mov      rdx, rsi
001A6D41  call     qword ptr [rax + 0x18]
001A6D44  mov      rsi, rbx
001A6D47  test     rbx, rbx
001A6D4A  jne      0x1a6d21  ; -> 001A6D21
001A6D4C  mov      r14, qword ptr [rsp + 0x30]
001A6D51  mov      rbx, qword ptr [rsp + 0x38]
001A6D56  lea      rax, [rdi + 8]
001A6D5A  mov      rsi, qword ptr [rsp + 0x40]
001A6D5F  mov      qword ptr [rax], rax
001A6D62  mov      qword ptr [rdi + 0x10], rax
001A6D66  xor      eax, eax
001A6D68  mov      qword ptr [rdi + 0x18], rax
001A6D6C  mov      byte ptr [rdi + 0x20], al
001A6D6F  mov      dword ptr [rdi + 0x28], eax
001A6D72  add      rsp, 0x20
001A6D76  pop      rdi
001A6D77  ret      
```

## 001AA840 (411 B, extent 001AA840-001AA9DB)

Documented callee on this page: `001AB570`

```
001AA840  mov      rax, rsp
001AA843  push     rsi
001AA844  push     rdi
001AA845  push     r14
001AA847  sub      rsp, 0x90
001AA84E  mov      qword ptr [rax - 0x80], 0xfffffffffffffffe
001AA856  mov      qword ptr [rax + 0x10], rbx
001AA85A  mov      qword ptr [rax + 0x18], rbp
001AA85E  movaps   xmmword ptr [rax - 0x28], xmm6
001AA862  movaps   xmmword ptr [rax - 0x38], xmm7
001AA866  mov      rax, qword ptr [rip + 0x1d99fc3]  ; -> 01F44830 [u64 0x00002B992DDFA232]
001AA86D  xor      rax, rsp
001AA870  mov      qword ptr [rsp + 0x68], rax
001AA875  movaps   xmm6, xmm3
001AA878  movaps   xmm7, xmm2
001AA87B  mov      ebx, edx
001AA87D  mov      rdi, rcx
001AA880  mov      qword ptr [rsp + 0x30], rcx
001AA885  xor      r14d, r14d
001AA888  mov      qword ptr [rcx], r14
001AA88B  mov      qword ptr [rcx + 8], r14
001AA88F  mov      qword ptr [rcx + 0x10], r14
001AA893  add      rcx, 0x18
001AA897  lea      rdx, [rip + 0x71b6ba]  ; -> 008C5F58 [str "EASTL vector"]
001AA89E  call     0x1edf00  ; -> 001EDF00 fn
001AA8A3  nop      
001AA8A4  mov      qword ptr [rdi + 0x28], r14
001AA8A8  mov      qword ptr [rdi + 0x30], 1
001AA8B0  mov      dword ptr [rdi + 0x38], r14d
001AA8B4  mov      dword ptr [rdi + 0x3c], 1
001AA8BB  mov      byte ptr [rdi + 0x40], 1
001AA8BF  mov      dword ptr [rdi + 0x44], r14d
001AA8C3  xor      eax, eax
001AA8C5  mov      qword ptr [rdi + 0x20], rax
001AA8C9  lea      rcx, [rsp + 0x38]
001AA8CE  call     0x1aac50  ; -> 001AAC50 fn
001AA8D3  nop      
001AA8D4  mov      rdx, rax
001AA8D7  mov      rcx, rdi
001AA8DA  call     0x1ad0c0  ; -> 001AD0C0 fn
001AA8DF  nop      
001AA8E0  mov      rdx, qword ptr [rsp + 0x40]
001AA8E5  test     rdx, rdx
001AA8E8  je       0x1aa904  ; -> 001AA904
001AA8EA  mov      r8, qword ptr [rsp + 0x50]
001AA8EF  sub      r8, rdx
001AA8F2  and      r8, 0xfffffffffffffff8
001AA8F6  lea      rcx, [rsp + 0x58]
001AA8FB  mov      rax, qword ptr [rsp + 0x58]
001AA900  call     qword ptr [rax + 0x18]
001AA903  nop      
001AA904  mov      dword ptr [rdi + 0x38], ebx
001AA907  mov      rcx, qword ptr [rdi + 8]
001AA90B  sub      rcx, qword ptr [rdi]
001AA90E  movabs   rax, 0x2aaaaaaaaaaaaaab
001AA918  imul     rcx
001AA91B  sar      rdx, 3
001AA91F  mov      rax, rdx
001AA922  shr      rax, 0x3f
001AA926  add      rdx, rax
001AA929  dec      edx
001AA92B  lea      rbp, [rdx + rdx*2]
001AA92F  shl      rbp, 4
001AA933  add      rbp, qword ptr [rdi]
001AA936  mov      esi, 6
001AA93B  nop      dword ptr [rax + rax]
001AA940  mov      qword ptr [rsp + 0x20], r14
001AA945  mov      rdx, qword ptr [rbp + 0x10]
001AA949  cmp      rdx, qword ptr [rbp + 0x18]
001AA94D  jae      0x1aa961  ; -> 001AA961
001AA94F  lea      rax, [rdx + 8]
001AA953  mov      qword ptr [rbp + 0x10], rax
001AA957  test     rdx, rdx
001AA95A  je       0x1aa96f  ; -> 001AA96F
001AA95C  mov      qword ptr [rdx], r14
001AA95F  jmp      0x1aa96f  ; -> 001AA96F
001AA961  lea      r8, [rsp + 0x20]
001AA966  lea      rcx, [rbp + 8]
001AA96A  call     0x1ab570  ; -> 001AB570 fn
001AA96F  sub      rsi, 1
001AA973  jne      0x1aa940  ; -> 001AA940
001AA975  mov      byte ptr [rbp + 0x28], 1
001AA979  movss    dword ptr [rdi + 0x20], xmm7
001AA97E  movss    dword ptr [rdi + 0x24], xmm6
001AA983  movss    xmm0, dword ptr [rsp + 0xd0]
001AA98C  movss    dword ptr [rdi + 0x28], xmm0
001AA991  mov      ecx, dword ptr [rsp + 0xd8]
001AA998  mov      dword ptr [rdi + 0x30], ecx
001AA99B  movss    xmm0, dword ptr [rsp + 0xe0]
001AA9A4  movss    dword ptr [rdi + 0x2c], xmm0
001AA9A9  mov      rax, rdi
001AA9AC  mov      rcx, qword ptr [rsp + 0x68]
001AA9B1  xor      rcx, rsp
001AA9B4  call     0x808c40  ; -> 00808C40 fn
001AA9B9  lea      r11, [rsp + 0x90]
001AA9C1  mov      rbx, qword ptr [r11 + 0x28]
001AA9C5  mov      rbp, qword ptr [r11 + 0x30]
001AA9C9  movaps   xmm6, xmmword ptr [r11 - 0x10]
001AA9CE  movaps   xmm7, xmmword ptr [rsp + 0x70]
001AA9D3  mov      rsp, r11
001AA9D6  pop      r14
001AA9D8  pop      rdi
001AA9D9  pop      rsi
001AA9DA  ret      
```

## 001AAC50 (164 B, extent 001AAC50-001AACF4)

Documented callee on this page: `001AB570`

```
001AAC50  mov      qword ptr [rsp + 8], rcx
001AAC55  push     rbp
001AAC56  push     rsi
001AAC57  push     rdi
001AAC58  sub      rsp, 0x30
001AAC5C  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001AAC65  mov      qword ptr [rsp + 0x60], rbx
001AAC6A  mov      rsi, rcx
001AAC6D  lea      rbx, [rcx + 8]
001AAC71  mov      qword ptr [rsp + 0x58], rbx
001AAC76  xor      ebp, ebp
001AAC78  mov      qword ptr [rbx], rbp
001AAC7B  mov      qword ptr [rbx + 8], rbp
001AAC7F  mov      qword ptr [rbx + 0x10], rbp
001AAC83  lea      rcx, [rbx + 0x18]
001AAC87  lea      rdx, [rip + 0x71b2ca]  ; -> 008C5F58 [str "EASTL vector"]
001AAC8E  call     0x1edf00  ; -> 001EDF00 fn
001AAC93  nop      
001AAC94  mov      byte ptr [rsi + 0x28], bpl
001AAC98  xor      eax, eax
001AAC9A  mov      dword ptr [rsi], eax
001AAC9C  mov      word ptr [rsi + 4], ax
001AACA0  lea      edi, [rbp + 6]
001AACA3  nop      dword ptr [rax]
001AACA7  nop      word ptr [rax + rax]
001AACB0  mov      qword ptr [rsp + 0x58], rbp
001AACB5  mov      rdx, qword ptr [rbx + 8]
001AACB9  cmp      rdx, qword ptr [rbx + 0x10]
001AACBD  jae      0x1aacd1  ; -> 001AACD1
001AACBF  lea      rax, [rdx + 8]
001AACC3  mov      qword ptr [rbx + 8], rax
001AACC7  test     rdx, rdx
001AACCA  je       0x1aacde  ; -> 001AACDE
001AACCC  mov      qword ptr [rdx], rbp
001AACCF  jmp      0x1aacde  ; -> 001AACDE
001AACD1  lea      r8, [rsp + 0x58]
001AACD6  mov      rcx, rbx
001AACD9  call     0x1ab570  ; -> 001AB570 fn
001AACDE  sub      rdi, 1
001AACE2  jne      0x1aacb0  ; -> 001AACB0
001AACE4  mov      rax, rsi
001AACE7  mov      rbx, qword ptr [rsp + 0x60]
001AACEC  add      rsp, 0x30
001AACF0  pop      rdi
001AACF1  pop      rsi
001AACF2  pop      rbp
001AACF3  ret      
```

## 001AD490 (55 B, extent 001AD490-001AD4C7)

Documented callee on this page: `00809950`

```
001AD490  test     rcx, rcx
001AD493  je       0x1ad4c6  ; -> 001AD4C6
001AD495  push     rbx
001AD496  sub      rsp, 0x30
001AD49A  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001AD4A3  mov      rbx, rcx
001AD4A6  call     0x1abd40  ; -> 001ABD40 fn
001AD4AB  mov      rcx, rbx
001AD4AE  call     0x1aae70  ; -> 001AAE70 fn
001AD4B3  nop      
001AD4B4  mov      edx, 0x48
001AD4B9  mov      rcx, rbx
001AD4BC  call     0x809950  ; -> 00809950 fn
001AD4C1  add      rsp, 0x30
001AD4C5  pop      rbx
001AD4C6  ret      
```

## 001AE010 (94 B, extent 001AE010-001AE06E)

Documented callee on this page: `001EDF00`

```
001AE010  mov      qword ptr [rsp + 8], rcx
001AE015  push     rdi
001AE016  sub      rsp, 0x30
001AE01A  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001AE023  mov      qword ptr [rsp + 0x50], rbx
001AE028  mov      rdi, rcx
001AE02B  lea      rbx, [rcx + 0x38]
001AE02F  mov      qword ptr [rsp + 0x48], rbx
001AE034  xor      eax, eax
001AE036  mov      qword ptr [rbx], rax
001AE039  mov      qword ptr [rbx + 8], rax
001AE03D  mov      qword ptr [rbx + 0x10], rax
001AE041  lea      rcx, [rbx + 0x18]
001AE045  lea      rdx, [rip + 0x717f0c]  ; -> 008C5F58 [str "EASTL vector"]
001AE04C  call     0x1edf00  ; -> 001EDF00 fn
001AE051  nop      
001AE052  mov      edx, 0x400
001AE057  mov      rcx, rbx
001AE05A  call     0x1b1a20  ; -> 001B1A20 fn
001AE05F  nop      
001AE060  mov      rax, rdi
001AE063  mov      rbx, qword ptr [rsp + 0x50]
001AE068  add      rsp, 0x30
001AE06C  pop      rdi
001AE06D  ret      
```

## 001AE3E0 (104 B, extent 001AE3E0-001AE448)

Documented callee on this page: `001FB460`

```
001AE3E0  push     rdi
001AE3E2  sub      rsp, 0x30
001AE3E6  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001AE3EF  mov      qword ptr [rsp + 0x40], rbx
001AE3F4  mov      qword ptr [rsp + 0x48], rsi
001AE3F9  mov      rsi, rcx
001AE3FC  mov      rdi, qword ptr [rcx + 8]
001AE400  mov      rbx, qword ptr [rcx]
001AE403  cmp      rbx, rdi
001AE406  jae      0x1ae41a  ; -> 001AE41A
001AE408  mov      rcx, rbx
001AE40B  call     0x1fb460  ; -> 001FB460 fn
001AE410  nop      
001AE411  add      rbx, 0x40
001AE415  cmp      rbx, rdi
001AE418  jb       0x1ae408  ; -> 001AE408
001AE41A  mov      rdx, qword ptr [rsi]
001AE41D  test     rdx, rdx
001AE420  je       0x1ae438  ; -> 001AE438
001AE422  lea      rcx, [rsi + 0x18]
001AE426  mov      rax, qword ptr [rcx]
001AE429  mov      r8, qword ptr [rsi + 0x10]
001AE42D  sub      r8, rdx
001AE430  and      r8, 0xffffffffffffffc0
001AE434  call     qword ptr [rax + 0x18]
001AE437  nop      
001AE438  mov      rbx, qword ptr [rsp + 0x40]
001AE43D  mov      rsi, qword ptr [rsp + 0x48]
001AE442  add      rsp, 0x30
001AE446  pop      rdi
001AE447  ret      
```

## 001B2630 (79 B, extent 001B2630-001B267F)

Documented callee on this page: `005CD0A0`

```
001B2630  mov      qword ptr [rsp + 8], rbx
001B2635  push     rdi
001B2636  sub      rsp, 0x20
001B263A  mov      rdi, rcx
001B263D  add      rcx, 0x218
001B2644  call     0x5cc8a0  ; -> 005CC8A0 fn
001B2649  lea      rcx, [rdi + 4]
001B264D  xor      edx, edx
001B264F  mov      r8d, 0x1c0
001B2655  call     0x861ec0  ; -> 00861EC0 fn
001B265A  xor      eax, eax
001B265C  lea      rcx, [rdi + 0x218]
001B2663  mov      qword ptr [rdi + 0x1c8], rax
001B266A  mov      dword ptr [rdi], eax
001B266C  call     0x5cd0a0  ; -> 005CD0A0 fn
001B2671  mov      rbx, qword ptr [rsp + 0x30]
001B2676  mov      rax, rdi
001B2679  add      rsp, 0x20
001B267D  pop      rdi
001B267E  ret      
```

## 001B3AF0 (96 B, extent 001B3AF0-001B3B50)

Documented callee on this page: `005CD6D0`

```
001B3AF0  push     rbx
001B3AF2  sub      rsp, 0x30
001B3AF6  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001B3AFF  mov      rbx, rcx
001B3B02  cmp      byte ptr [rcx + 0xb8], 0
001B3B09  je       0x1b3b18  ; -> 001B3B18
001B3B0B  add      rcx, 0x90
001B3B12  call     0x5cd6d0  ; -> 005CD6D0 fn
001B3B17  nop      
001B3B18  lea      rcx, [rbx + 0x58]
001B3B1C  call     0x1b3c30  ; -> 001B3C30 fn
001B3B21  nop      
001B3B22  lea      rcx, [rbx + 0x20]
001B3B26  call     0x1b3c30  ; -> 001B3C30 fn
001B3B2B  nop      
001B3B2C  mov      rdx, qword ptr [rbx]
001B3B2F  test     rdx, rdx
001B3B32  je       0x1b3b4a  ; -> 001B3B4A
001B3B34  lea      rcx, [rbx + 0x18]
001B3B38  mov      rax, qword ptr [rcx]
001B3B3B  mov      r8, qword ptr [rbx + 0x10]
001B3B3F  sub      r8, rdx
001B3B42  and      r8, 0xffffffffffffffe0
001B3B46  call     qword ptr [rax + 0x18]
001B3B49  nop      
001B3B4A  add      rsp, 0x30
001B3B4E  pop      rbx
001B3B4F  ret      
```

## 001B60D0 (62 B, extent 001B60D0-001B610E)

Documented callee on this page: `0016D6A0`

```
001B60D0  sub      rsp, 0x28
001B60D4  xor      ecx, ecx
001B60D6  cmp      qword ptr [rip + 0x1dcb123], rcx  ; -> 01F81200
001B60DD  setne    cl
001B60E0  call     0x16d6a0  ; -> 0016D6A0 fn
001B60E5  cmp      qword ptr [rip + 0x1dcb113], 0  ; -> 01F81200
001B60ED  je       0x1b6109  ; -> 001B6109
001B60EF  mov      ecx, 1
001B60F4  call     0x16d6a0  ; -> 0016D6A0 fn
001B60F9  mov      rcx, qword ptr [rip + 0x1dcb100]  ; -> 01F81200
001B6100  add      rsp, 0x28
001B6104  jmp      0x1b5140  ; -> 001B5140 fn
001B6109  add      rsp, 0x28
001B610D  ret      
```

## 001B9910 (94 B, extent 001B9910-001B996E)

Documented callee on this page: `001BA910`

```
001B9910  push     rbx
001B9912  sub      rsp, 0x30
001B9916  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001B991F  lea      rax, [rip + 0x73f82a]  ; -> 008F9150
001B9926  mov      qword ptr [rcx], rax
001B9929  xor      eax, eax
001B992B  mov      qword ptr [rcx + 0x58], rax
001B992F  mov      qword ptr [rcx + 0x60], rax
001B9933  mov      qword ptr [rcx + 0x68], rax
001B9937  mov      qword ptr [rcx + 0x70], rax
001B993B  mov      qword ptr [rcx + 0x78], rax
001B993F  mov      qword ptr [rcx + 0x80], rax
001B9946  mov      qword ptr [rcx + 0x88], rax
001B994D  mov      qword ptr [rcx + 0x90], rax
001B9954  lea      rbx, [rcx + 0x10]
001B9958  mov      rcx, rbx
001B995B  call     0x1ba910  ; -> 001BA910 fn
001B9960  nop      
001B9961  mov      rcx, rbx
001B9964  add      rsp, 0x30
001B9968  pop      rbx
001B9969  jmp      0x1b9750  ; -> 001B9750 fn
```

## 001BE520 (114 B, extent 001BE520-001BE592)

Documented callee on this page: `001A5760`

```
001BE520  mov      qword ptr [rsp + 0x10], rbx
001BE525  mov      qword ptr [rsp + 0x18], rbp
001BE52A  push     rdi
001BE52B  sub      rsp, 0x20
001BE52F  mov      rdi, r8
001BE532  mov      rbx, rdx
001BE535  mov      rbp, rcx
001BE538  cmp      rdx, rcx
001BE53B  je       0x1be57f  ; -> 001BE57F
001BE53D  mov      qword ptr [rsp + 0x30], rsi
001BE542  mov      rsi, r8
001BE545  sub      rsi, rdx
001BE548  nop      dword ptr [rax + rax]
001BE550  sub      rbx, 0x28
001BE554  sub      rdi, 0x28
001BE558  cmp      rbx, rdi
001BE55B  je       0x1be56c  ; -> 001BE56C
001BE55D  mov      r8, qword ptr [rbx + 8]
001BE561  mov      rcx, rdi
001BE564  mov      rdx, qword ptr [rbx]
001BE567  call     0x1a5760  ; -> 001A5760 fn
001BE56C  mov      rcx, qword ptr [rbx + 0x20]
001BE570  mov      qword ptr [rsi + rbx + 0x20], rcx
001BE575  cmp      rbx, rbp
001BE578  jne      0x1be550  ; -> 001BE550
001BE57A  mov      rsi, qword ptr [rsp + 0x30]
001BE57F  mov      rbx, qword ptr [rsp + 0x38]
001BE584  mov      rax, rdi
001BE587  mov      rbp, qword ptr [rsp + 0x40]
001BE58C  add      rsp, 0x20
001BE590  pop      rdi
001BE591  ret      
```

## 001BE5A0 (186 B, extent 001BE5A0-001BE65A)

Documented callee on this page: `001EDF00`

```
001BE5A0  mov      qword ptr [rsp + 0x18], r8
001BE5A5  mov      qword ptr [rsp + 0x10], rdx
001BE5AA  push     rbp
001BE5AB  push     rsi
001BE5AC  push     rdi
001BE5AD  sub      rsp, 0x30
001BE5B1  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001BE5BA  mov      qword ptr [rsp + 0x68], rbx
001BE5BF  mov      rbx, rdx
001BE5C2  mov      rsi, rcx
001BE5C5  mov      qword ptr [rcx], r9
001BE5C8  cmp      rdx, r8
001BE5CB  je       0x1be64a  ; -> 001BE64A
001BE5CD  xor      ebp, ebp
001BE5CF  nop      
001BE5D0  mov      rdi, qword ptr [rsi]
001BE5D3  mov      qword ptr [rsp + 0x50], rdi
001BE5D8  mov      qword ptr [rsp + 0x28], rdi
001BE5DD  test     rdi, rdi
001BE5E0  je       0x1be638  ; -> 001BE638
001BE5E2  mov      qword ptr [rdi], rbp
001BE5E5  mov      qword ptr [rdi + 8], rbp
001BE5E9  mov      qword ptr [rdi + 0x10], rbp
001BE5ED  lea      rdx, [rbx + 0x18]
001BE5F1  lea      rcx, [rdi + 0x18]
001BE5F5  call     0x1edf00  ; -> 001EDF00 fn
001BE5FA  mov      rcx, qword ptr [rdi]
001BE5FD  mov      rax, qword ptr [rbx]
001BE600  mov      qword ptr [rdi], rax
001BE603  mov      qword ptr [rbx], rcx
001BE606  mov      rcx, qword ptr [rdi + 8]
001BE60A  mov      rax, qword ptr [rbx + 8]
001BE60E  mov      qword ptr [rdi + 8], rax
001BE612  mov      qword ptr [rbx + 8], rcx
001BE616  mov      rcx, qword ptr [rdi + 0x10]
001BE61A  mov      rax, qword ptr [rbx + 0x10]
001BE61E  mov      qword ptr [rdi + 0x10], rax
001BE622  mov      qword ptr [rbx + 0x10], rcx
001BE626  mov      rax, qword ptr [rbx + 0x20]
001BE62A  mov      qword ptr [rdi + 0x20], rax
001BE62E  mov      r8, qword ptr [rsp + 0x60]
001BE633  mov      rbx, qword ptr [rsp + 0x58]
001BE638  add      rbx, 0x28
001BE63C  mov      qword ptr [rsp + 0x58], rbx
001BE641  add      qword ptr [rsi], 0x28
001BE645  cmp      rbx, r8
001BE648  jne      0x1be5d0  ; -> 001BE5D0
001BE64A  mov      rax, rsi
001BE64D  mov      rbx, qword ptr [rsp + 0x68]
001BE652  add      rsp, 0x30
001BE656  pop      rdi
001BE657  pop      rsi
001BE658  pop      rbp
001BE659  ret      
```

## 001BEA90 (135 B, extent 001BEA90-001BEB17)

Documented callee on this page: `001A4BF0`

```
001BEA90  push     rdi
001BEA92  sub      rsp, 0x30
001BEA96  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001BEA9F  mov      qword ptr [rsp + 0x48], rbx
001BEAA4  mov      qword ptr [rsp + 0x58], rsi
001BEAA9  mov      rsi, rdx
001BEAAC  add      rcx, 0x30
001BEAB0  mov      rax, qword ptr [rcx]
001BEAB3  xor      r8d, r8d
001BEAB6  lea      edx, [r8 + 0x48]
001BEABA  call     qword ptr [rax + 0x10]
001BEABD  mov      rdi, rax
001BEAC0  mov      qword ptr [rsp + 0x40], rax
001BEAC5  lea      rbx, [rax + 0x20]
001BEAC9  mov      qword ptr [rsp + 0x50], rbx
001BEACE  test     rbx, rbx
001BEAD1  je       0x1beb07  ; -> 001BEB07
001BEAD3  xor      eax, eax
001BEAD5  mov      qword ptr [rbx], rax
001BEAD8  mov      qword ptr [rbx + 8], rax
001BEADC  mov      qword ptr [rbx + 0x10], rax
001BEAE0  lea      rdx, [rsi + 0x18]
001BEAE4  lea      rcx, [rbx + 0x18]
001BEAE8  call     0x1edf00  ; -> 001EDF00 fn
001BEAED  mov      r8, qword ptr [rsi + 8]
001BEAF1  mov      rdx, qword ptr [rsi]
001BEAF4  mov      rcx, rbx
001BEAF7  call     0x1a4bf0  ; -> 001A4BF0 fn
001BEAFC  mov      eax, dword ptr [rsi + 0x20]
001BEAFF  mov      dword ptr [rbx + 0x20], eax
001BEB02  mov      rax, rdi
001BEB05  jmp      0x1beb07  ; -> 001BEB07
001BEB07  mov      rbx, qword ptr [rsp + 0x48]
001BEB0C  mov      rsi, qword ptr [rsp + 0x58]
001BEB11  add      rsp, 0x30
001BEB15  pop      rdi
001BEB16  ret      
```

## 001C0EB0 (100 B, extent 001C0EB0-001C0F14)

Documented callee on this page: `00809950`

```
001C0EB0  push     rdi
001C0EB2  sub      rsp, 0x30
001C0EB6  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001C0EBF  mov      qword ptr [rsp + 0x40], rbx
001C0EC4  mov      edi, edx
001C0EC6  mov      rbx, rcx
001C0EC9  lea      rax, [rip + 0x738cb0]  ; -> 008F9B80
001C0ED0  mov      qword ptr [rcx], rax
001C0ED3  mov      rdx, qword ptr [rcx + 0x50]
001C0ED7  test     rdx, rdx
001C0EDA  je       0x1c0ef2  ; -> 001C0EF2
001C0EDC  add      rcx, 0x68
001C0EE0  mov      rax, qword ptr [rcx]
001C0EE3  mov      r8, qword ptr [rbx + 0x60]
001C0EE7  sub      r8, rdx
001C0EEA  and      r8, 0xfffffffffffffff0
001C0EEE  call     qword ptr [rax + 0x18]
001C0EF1  nop      
001C0EF2  test     dil, 1
001C0EF6  je       0x1c0f06  ; -> 001C0F06
001C0EF8  mov      edx, 0xa78
001C0EFD  mov      rcx, rbx
001C0F00  call     0x809950  ; -> 00809950 fn
001C0F05  nop      
001C0F06  mov      rax, rbx
001C0F09  mov      rbx, qword ptr [rsp + 0x40]
001C0F0E  add      rsp, 0x30
001C0F12  pop      rdi
001C0F13  ret      
```

## 001C5530 (61 B, extent 001C5530-001C556D)

Documented callee on this page: `00200BE0`

```
001C5530  mov      qword ptr [rsp + 8], rbx
001C5535  push     rdi
001C5536  sub      rsp, 0x20
001C553A  mov      rbx, rdx
001C553D  mov      rdi, rcx
001C5540  call     0x1ff740  ; -> 001FF740 fn
001C5545  mov      rcx, rax
001C5548  call     0x200be0  ; -> 00200BE0 fn
001C554D  lea      rcx, [rip + 0x1dbbe74]  ; -> 01F813C8
001C5554  mov      rdx, rbx
001C5557  test     al, al
001C5559  jne      0x1c555e  ; -> 001C555E
001C555B  mov      rcx, rdi
001C555E  mov      rbx, qword ptr [rsp + 0x30]
001C5563  add      rsp, 0x20
001C5567  pop      rdi
001C5568  jmp      0x1ff740  ; -> 001FF740 fn
```

## 001D5FD0 (46 B, extent 001D5FD0-001D5FFE)

Documented callee on this page: `0016D6A0`

```
001D5FD0  push     rbx
001D5FD2  sub      rsp, 0x20
001D5FD6  mov      rbx, rcx
001D5FD9  xor      ecx, ecx
001D5FDB  cmp      qword ptr [rip + 0x1dacc9e], rcx  ; -> 01F82C80
001D5FE2  setne    cl
001D5FE5  call     0x16d6a0  ; -> 0016D6A0 fn
001D5FEA  mov      rcx, qword ptr [rip + 0x1dacc8f]  ; -> 01F82C80
001D5FF1  mov      rdx, rbx
001D5FF4  add      rsp, 0x20
001D5FF8  pop      rbx
001D5FF9  jmp      0x1d6250  ; -> 001D6250 fn
```
