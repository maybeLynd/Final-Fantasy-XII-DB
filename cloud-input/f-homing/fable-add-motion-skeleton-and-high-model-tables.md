# F homing pack (FABLE): `17-Presentation-Rendering/Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md`

Generated 2026-10-03 04:02 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 10. No bearing page cites them and no documented function calls them directly.

## 003418B0 (198 B, extent 003418B0-00341976)

Documented callee on this page: `002EB540`

```
003418B0  mov      qword ptr [rsp + 8], rbx
003418B5  push     rdi
003418B6  sub      rsp, 0x20
003418BA  cmp      byte ptr [r8 + 8], 0
003418BF  mov      rdi, r8
003418C2  mov      rbx, rdx
003418C5  je       0x341923  ; -> 00341923
003418C7  movzx    eax, word ptr [r8 + 0xa]
003418CC  test     ax, ax
003418CF  jne      0x341932  ; -> 00341932
003418D1  mov      ecx, dword ptr [r8 + 4]
003418D5  call     0x2e97c0  ; -> 002E97C0 fn
003418DA  test     rax, rax
003418DD  jne      0x34190e  ; -> 0034190E
003418DF  movzx    edx, byte ptr [rbx + 0x15]
003418E3  mov      ecx, dword ptr [rdi]
003418E5  call     0x2eb540  ; -> 002EB540 fn
003418EA  mov      rcx, rax
003418ED  call     0x2e9810  ; -> 002E9810 fn
003418F2  mov      dword ptr [rdi + 4], eax
003418F5  mov      ebx, 1
003418FA  mov      ecx, ebx
003418FC  call     0x314d40  ; -> 00314D40 fn
00341901  mov      eax, ebx
00341903  mov      rbx, qword ptr [rsp + 0x30]
00341908  add      rsp, 0x20
0034190C  pop      rdi
0034190D  ret      
0034190E  mov      rcx, rax
00341911  call     0x2e4c20  ; -> 002E4C20 fn
00341916  mov      ebx, 1
0034191B  test     eax, eax
0034191D  je       0x3418fa  ; -> 003418FA
0034191F  mov      word ptr [rdi + 0xa], bx
00341923  xor      ebx, ebx
00341925  mov      eax, ebx
00341927  mov      rbx, qword ptr [rsp + 0x30]
0034192C  add      rsp, 0x20
00341930  pop      rdi
00341931  ret      
00341932  cmp      ax, 2
00341936  jne      0x341965  ; -> 00341965
00341938  mov      ecx, dword ptr [r8 + 4]
0034193C  call     0x2e97c0  ; -> 002E97C0 fn
00341941  mov      rcx, rax
00341944  call     0x2e4c20  ; -> 002E4C20 fn
00341949  test     eax, eax
0034194B  je       0x3418f5  ; -> 003418F5
0034194D  mov      eax, 3
00341952  xor      ebx, ebx
00341954  mov      word ptr [rdi + 0xa], ax
00341958  mov      eax, ebx
0034195A  mov      rbx, qword ptr [rsp + 0x30]
0034195F  add      rsp, 0x20
00341963  pop      rdi
00341964  ret      
00341965  mov      ebx, dword ptr [rsp + 0x40]
00341969  mov      eax, ebx
0034196B  mov      rbx, qword ptr [rsp + 0x30]
00341970  add      rsp, 0x20
00341974  pop      rdi
00341975  ret      
```

## 00343B00 (177 B, extent 00343B00-00343BB1)

Documented callee on this page: `002EB540`

```
00343B00  mov      qword ptr [rsp + 8], rbx
00343B05  mov      qword ptr [rsp + 0x10], rbp
00343B0A  mov      qword ptr [rsp + 0x18], rsi
00343B0F  push     rdi
00343B10  push     r14
00343B12  push     r15
00343B14  sub      rsp, 0x20
00343B18  mov      rcx, r9
00343B1B  mov      rdi, r9
00343B1E  mov      rsi, r8
00343B21  mov      rbp, rdx
00343B24  call     0x267e10  ; -> 00267E10 fn
00343B29  mov      rcx, rdi
00343B2C  mov      r15d, eax
00343B2F  call     0x267e10  ; -> 00267E10 fn
00343B34  mov      rcx, rdi
00343B37  mov      ebx, eax
00343B39  call     0x267e10  ; -> 00267E10 fn
00343B3E  mov      ecx, ebx
00343B40  mov      edi, eax
00343B42  call     0x2e9a60  ; -> 002E9A60 fn
00343B47  xor      ebx, ebx
00343B49  mov      r14d, eax
00343B4C  mov      word ptr [rsi + 0xa], bx
00343B50  test     edi, edi
00343B52  js       0x343b60  ; -> 00343B60
00343B54  mov      eax, 1
00343B59  mov      ebx, edi
00343B5B  cmp      edi, eax
00343B5D  cmovg    ebx, eax
00343B60  movzx    ecx, byte ptr [rbp + 0x15]
00343B64  call     0x267310  ; -> 00267310 fn
00343B69  test     eax, eax
00343B6B  je       0x343b73  ; -> 00343B73
00343B6D  mov      byte ptr [rsi + 8], 0
00343B71  jmp      0x343b98  ; -> 00343B98
00343B73  mov      dword ptr [rsi], r14d
00343B76  mov      ecx, r14d
00343B79  movzx    edx, byte ptr [rbp + 0x15]
00343B7D  call     0x2eb540  ; -> 002EB540 fn
00343B82  mov      rcx, rax
00343B85  call     0x2e9810  ; -> 002E9810 fn
00343B8A  mov      dword ptr [rsi + 4], eax
00343B8D  mov      dword ptr [rsi + 0xc], r15d
00343B91  mov      byte ptr [rsi + 9], bl
00343B94  mov      byte ptr [rsi + 8], 1
00343B98  mov      rbx, qword ptr [rsp + 0x40]
00343B9D  mov      rbp, qword ptr [rsp + 0x48]
00343BA2  mov      rsi, qword ptr [rsp + 0x50]
00343BA7  add      rsp, 0x20
00343BAB  pop      r15
00343BAD  pop      r14
00343BAF  pop      rdi
00343BB0  ret      
```

## 00344F00 (121 B, extent 00344F00-00344F79)

Documented callee on this page: `002EB540`

```
00344F00  mov      qword ptr [rsp + 8], rbx
00344F05  mov      qword ptr [rsp + 0x10], rsi
00344F0A  push     rdi
00344F0B  sub      rsp, 0x20
00344F0F  mov      rcx, r9
00344F12  mov      rbx, r8
00344F15  mov      rsi, rdx
00344F18  call     0x267e10  ; -> 00267E10 fn
00344F1D  mov      ecx, eax
00344F1F  call     0x2e9a60  ; -> 002E9A60 fn
00344F24  mov      edi, eax
00344F26  xor      eax, eax
00344F28  mov      word ptr [rbx + 0xa], ax
00344F2C  movzx    ecx, byte ptr [rsi + 0x15]
00344F30  call     0x267310  ; -> 00267310 fn
00344F35  test     eax, eax
00344F37  je       0x344f4d  ; -> 00344F4D
00344F39  mov      byte ptr [rbx + 8], 0
00344F3D  mov      rbx, qword ptr [rsp + 0x30]
00344F42  mov      rsi, qword ptr [rsp + 0x38]
00344F47  add      rsp, 0x20
00344F4B  pop      rdi
00344F4C  ret      
00344F4D  mov      dword ptr [rbx], edi
00344F4F  mov      ecx, edi
00344F51  movzx    edx, byte ptr [rsi + 0x15]
00344F55  call     0x2eb540  ; -> 002EB540 fn
00344F5A  mov      rcx, rax
00344F5D  call     0x2e9810  ; -> 002E9810 fn
00344F62  mov      rsi, qword ptr [rsp + 0x38]
00344F67  mov      dword ptr [rbx + 4], eax
00344F6A  mov      byte ptr [rbx + 8], 1
00344F6E  mov      rbx, qword ptr [rsp + 0x30]
00344F73  add      rsp, 0x20
00344F77  pop      rdi
00344F78  ret      
```

## 0034CED0 (66 B, extent 0034CED0-0034CF12)

Documented callee on this page: `00314D40`

```
0034CED0  mov      qword ptr [rsp + 8], rbx
0034CED5  push     rdi
0034CED6  sub      rsp, 0x20
0034CEDA  mov      rcx, r9
0034CEDD  mov      rdi, r9
0034CEE0  call     0x267e10  ; -> 00267E10 fn
0034CEE5  mov      ebx, eax
0034CEE7  test     eax, eax
0034CEE9  jns      0x34cef2  ; -> 0034CEF2
0034CEEB  call     0x314840  ; -> 00314840 fn
0034CEF0  mov      ebx, eax
0034CEF2  mov      rcx, rdi
0034CEF5  call     0x267e10  ; -> 00267E10 fn
0034CEFA  mov      ecx, eax
0034CEFC  call     0x26b750  ; -> 0026B750 fn
0034CF01  mov      ecx, ebx
0034CF03  mov      rbx, qword ptr [rsp + 0x30]
0034CF08  add      rsp, 0x20
0034CF0C  pop      rdi
0034CF0D  jmp      0x314d40  ; -> 00314D40 fn
```

## 00352E40 (60 B, extent 00352E40-00352E7C)

Documented callee on this page: `00314D40`

```
00352E40  mov      qword ptr [rsp + 8], rbx
00352E45  push     rdi
00352E46  sub      rsp, 0x20
00352E4A  mov      rcx, r9
00352E4D  mov      rdi, r9
00352E50  call     0x267e10  ; -> 00267E10 fn
00352E55  mov      rcx, rdi
00352E58  mov      ebx, eax
00352E5A  call     0x267e10  ; -> 00267E10 fn
00352E5F  mov      edx, ebx
00352E61  mov      ecx, eax
00352E63  call     0x2e2560  ; -> 002E2560 fn
00352E68  mov      ecx, 1
00352E6D  mov      rbx, qword ptr [rsp + 0x30]
00352E72  add      rsp, 0x20
00352E76  pop      rdi
00352E77  jmp      0x314d40  ; -> 00314D40 fn
```

## 0036EB70 (160 B, extent 0036EB70-0036EC10)

Documented callee on this page: `002DF440`

```
0036EB70  mov      qword ptr [rsp + 8], rbx
0036EB75  mov      qword ptr [rsp + 0x10], rsi
0036EB7A  push     rdi
0036EB7B  sub      rsp, 0x20
0036EB7F  lea      rbx, [rip + 0x1f6af66]  ; -> 022D9AEC
0036EB86  xor      edi, edi
0036EB88  lea      rsi, [rip + 0x1f6afbd]  ; -> 022D9B4C
0036EB8F  nop      
0036EB90  movsx    eax, byte ptr [rbx - 0xb]
0036EB94  cmp      byte ptr [rbx - 0xa], dil
0036EB98  lea      ecx, [rax + 2]
0036EB9B  cmove    ecx, eax
0036EB9E  call     0x2df440  ; -> 002DF440 fn
0036EBA3  mov      ecx, dword ptr [rbx]
0036EBA5  call     0x369800  ; -> 00369800 fn
0036EBAA  mov      ecx, dword ptr [rbx + 4]
0036EBAD  mov      dword ptr [rbx], edi
0036EBAF  call     0x369800  ; -> 00369800 fn
0036EBB4  mov      dword ptr [rbx + 4], edi
0036EBB7  add      rbx, 0x18
0036EBBB  cmp      rbx, rsi
0036EBBE  jl       0x36eb90  ; -> 0036EB90
0036EBC0  lea      rbx, [rip + 0x1f6aef5]  ; -> 022D9ABC
0036EBC7  lea      rsi, [rip + 0x1f6af1e]  ; -> 022D9AEC
0036EBCE  nop      
0036EBD0  movsx    eax, byte ptr [rbx - 0xb]
0036EBD4  cmp      byte ptr [rbx - 0xa], dil
0036EBD8  lea      ecx, [rax + 2]
0036EBDB  cmove    ecx, eax
0036EBDE  call     0x2df440  ; -> 002DF440 fn
0036EBE3  mov      ecx, dword ptr [rbx]
0036EBE5  call     0x369800  ; -> 00369800 fn
0036EBEA  mov      ecx, dword ptr [rbx + 4]
0036EBED  mov      dword ptr [rbx], edi
0036EBEF  call     0x369800  ; -> 00369800 fn
0036EBF4  mov      dword ptr [rbx + 4], edi
0036EBF7  add      rbx, 0x18
0036EBFB  cmp      rbx, rsi
0036EBFE  jl       0x36ebd0  ; -> 0036EBD0
0036EC00  mov      rbx, qword ptr [rsp + 0x30]
0036EC05  mov      rsi, qword ptr [rsp + 0x38]
0036EC0A  add      rsp, 0x20
0036EC0E  pop      rdi
0036EC0F  ret      
```

## 0050CA40 (67 B, extent 0050CA40-0050CA83)

Documented callee on this page: `002EB540`

```
0050CA40  mov      qword ptr [rsp + 8], rbx
0050CA45  push     rdi
0050CA46  sub      rsp, 0x20
0050CA4A  mov      rcx, r9
0050CA4D  mov      rbx, r8
0050CA50  mov      rdi, rdx
0050CA53  call     0x267e10  ; -> 00267E10 fn
0050CA58  test     eax, eax
0050CA5A  jle      0x50ca63  ; -> 0050CA63
0050CA5C  mov      ecx, eax
0050CA5E  call     0x2e9a60  ; -> 002E9A60 fn
0050CA63  mov      dword ptr [rbx], eax
0050CA65  test     eax, eax
0050CA67  js       0x50ca78  ; -> 0050CA78
0050CA69  movzx    edx, byte ptr [rdi + 0x15]
0050CA6D  mov      ecx, eax
0050CA6F  call     0x2eb540  ; -> 002EB540 fn
0050CA74  mov      qword ptr [rbx + 8], rax
0050CA78  mov      rbx, qword ptr [rsp + 0x30]
0050CA7D  add      rsp, 0x20
0050CA81  pop      rdi
0050CA82  ret      
```

## 0050CBD0 (95 B, extent 0050CBD0-0050CC2F)

Documented callee on this page: `002E3C20`

```
0050CBD0  mov      qword ptr [rsp + 8], rbx
0050CBD5  push     rdi
0050CBD6  sub      rsp, 0x30
0050CBDA  cmp      dword ptr [r8], 0
0050CBDE  mov      rdi, r8
0050CBE1  mov      rbx, rdx
0050CBE4  mov      rcx, rdx
0050CBE7  jl       0x50cc1b  ; -> 0050CC1B
0050CBE9  mov      edx, 2
0050CBEE  lea      r8d, [rdx - 1]
0050CBF2  call     0x2ebc90  ; -> 002EBC90 fn
0050CBF7  mov      r9, qword ptr [rdi + 8]
0050CBFB  xor      r8d, r8d
0050CBFE  xor      edx, edx
0050CC00  mov      dword ptr [rsp + 0x20], 0
0050CC08  mov      rcx, rbx
0050CC0B  call     0x2e3110  ; -> 002E3110 fn
0050CC10  mov      rbx, qword ptr [rsp + 0x40]
0050CC15  add      rsp, 0x30
0050CC19  pop      rdi
0050CC1A  ret      
0050CC1B  xor      r8d, r8d
0050CC1E  xor      edx, edx
0050CC20  mov      rbx, qword ptr [rsp + 0x40]
0050CC25  add      rsp, 0x30
0050CC29  pop      rdi
0050CC2A  jmp      0x2e3c20  ; -> 002E3C20 fn
```

## 0050CD80 (94 B, extent 0050CD80-0050CDDE)

Documented callee on this page: `002E3C20`

```
0050CD80  mov      qword ptr [rsp + 8], rbx
0050CD85  push     rdi
0050CD86  sub      rsp, 0x30
0050CD8A  cmp      dword ptr [r8], 0
0050CD8E  mov      rbx, rdx
0050CD91  mov      rcx, rbx
0050CD94  mov      rdi, r8
0050CD97  mov      edx, 1
0050CD9C  jl       0x50cdcc  ; -> 0050CDCC
0050CD9E  mov      r8d, edx
0050CDA1  call     0x2ebc90  ; -> 002EBC90 fn
0050CDA6  mov      r9, qword ptr [rdi + 8]
0050CDAA  xor      r8d, r8d
0050CDAD  mov      rcx, rbx
0050CDB0  mov      dword ptr [rsp + 0x20], 0
0050CDB8  lea      edx, [r8 + 1]
0050CDBC  call     0x2e3110  ; -> 002E3110 fn
0050CDC1  mov      rbx, qword ptr [rsp + 0x40]
0050CDC6  add      rsp, 0x30
0050CDCA  pop      rdi
0050CDCB  ret      
0050CDCC  xor      r8d, r8d
0050CDCF  mov      rbx, qword ptr [rsp + 0x40]
0050CDD4  add      rsp, 0x30
0050CDD8  pop      rdi
0050CDD9  jmp      0x2e3c20  ; -> 002E3C20 fn
```

## 0050CF20 (99 B, extent 0050CF20-0050CF83)

Documented callee on this page: `002E3C20`

```
0050CF20  mov      qword ptr [rsp + 8], rbx
0050CF25  push     rdi
0050CF26  sub      rsp, 0x30
0050CF2A  cmp      dword ptr [r8], 0
0050CF2E  mov      rdi, r8
0050CF31  mov      rbx, rdx
0050CF34  mov      rcx, rdx
0050CF37  jl       0x50cf6d  ; -> 0050CF6D
0050CF39  mov      edx, 3
0050CF3E  lea      r8d, [rdx - 2]
0050CF42  call     0x2ebc90  ; -> 002EBC90 fn
0050CF47  mov      r9, qword ptr [rdi + 8]
0050CF4B  xor      r8d, r8d
0050CF4E  mov      rcx, rbx
0050CF51  mov      dword ptr [rsp + 0x20], 0
0050CF59  lea      edx, [r8 + 2]
0050CF5D  call     0x2e3110  ; -> 002E3110 fn
0050CF62  mov      rbx, qword ptr [rsp + 0x40]
0050CF67  add      rsp, 0x30
0050CF6B  pop      rdi
0050CF6C  ret      
0050CF6D  xor      r8d, r8d
0050CF70  lea      edx, [r8 + 2]
0050CF74  mov      rbx, qword ptr [rsp + 0x40]
0050CF79  add      rsp, 0x30
0050CF7D  pop      rdi
0050CF7E  jmp      0x2e3c20  ; -> 002E3C20 fn
```
