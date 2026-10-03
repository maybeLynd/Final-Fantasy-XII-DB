# F homing pack (FABLE): `00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md`

Generated 2026-10-03 04:02 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 29. No bearing page cites them and no documented function calls them directly.

## 00240A60 (100 B, extent 00240A60-00240AC4)

Documented callee on this page: `002F9860`

```
00240A60  mov      qword ptr [rsp + 8], rbx
00240A65  push     rdi
00240A66  sub      rsp, 0x20
00240A6A  mov      rax, qword ptr [rdx + 0x10]
00240A6E  lea      rcx, [rip + 0x6d41eb]  ; -> 00914C60
00240A75  mov      rdi, rdx
00240A78  mov      rbx, qword ptr [rax]
00240A7B  movsxd   rax, r9d
00240A7E  mov      ecx, dword ptr [rcx + rax*8]
00240A81  call     0x2f9860  ; -> 002F9860 fn
00240A86  xor      ecx, ecx
00240A88  mov      qword ptr [rbx + 0x18], rax
00240A8C  call     0x20e620  ; -> 0020E620 fn
00240A91  mov      dword ptr [rbx + 0x20], eax
00240A94  mov      ecx, 0x53d
00240A99  mov      rax, qword ptr [rdi + 0x10]
00240A9D  mov      rbx, qword ptr [rax + 8]
00240AA1  call     0x2f9860  ; -> 002F9860 fn
00240AA6  xor      ecx, ecx
00240AA8  mov      qword ptr [rbx + 0x18], rax
00240AAC  call     0x20e620  ; -> 0020E620 fn
00240AB1  mov      dword ptr [rbx + 0x20], eax
00240AB4  mov      eax, 1
00240AB9  mov      rbx, qword ptr [rsp + 0x30]
00240ABE  add      rsp, 0x20
00240AC2  pop      rdi
00240AC3  ret      
```

## 002637D0 (54 B, extent 002637D0-00263806)

Documented callee on this page: `002E97B0`

```
002637D0  push     rbx
002637D2  sub      rsp, 0x20
002637D6  mov      ebx, edx
002637D8  call     0x2e97b0  ; -> 002E97B0 fn
002637DD  test     rax, rax
002637E0  je       0x2637fe  ; -> 002637FE
002637E2  cmp      dword ptr [rax], -1
002637E5  je       0x2637fe  ; -> 002637FE
002637E7  movzx    ecx, byte ptr [rax + 0x29]
002637EB  test     cl, 1
002637EE  je       0x2637fe  ; -> 002637FE
002637F0  movzx    eax, cl
002637F3  shr      eax, 1
002637F5  and      eax, 1
002637F8  add      rsp, 0x20
002637FC  pop      rbx
002637FD  ret      
002637FE  mov      eax, ebx
00263800  add      rsp, 0x20
00263804  pop      rbx
00263805  ret      
```

## 00269F60 (44 B, extent 00269F60-00269F8C)

Documented callee on this page: `002E97B0`

```
00269F60  push     rbx
00269F62  sub      rsp, 0x20
00269F66  mov      ebx, edx
00269F68  call     0x2e97b0  ; -> 002E97B0 fn
00269F6D  test     rax, rax
00269F70  je       0x269f86  ; -> 00269F86
00269F72  cmp      dword ptr [rax], -1
00269F75  je       0x269f86  ; -> 00269F86
00269F77  movzx    ecx, word ptr [rax]
00269F7A  mov      edx, ebx
00269F7C  add      rsp, 0x20
00269F80  pop      rbx
00269F81  jmp      0x3ec200  ; -> 003EC200 fn
00269F86  add      rsp, 0x20
00269F8A  pop      rbx
00269F8B  ret      
```

## 002CA6C0 (255 B, extent 002CA6C0-002CA7BF)

Documented callee on this page: `002432B0`

```
002CA6C0  mov      qword ptr [rsp + 0x10], rbx
002CA6C5  push     rdi
002CA6C6  sub      rsp, 0x20
002CA6CA  mov      rbx, rcx
002CA6CD  mov      rdi, rdx
002CA6D0  mov      ecx, dword ptr [rdx]
002CA6D2  sub      ecx, 1
002CA6D5  je       0x2ca734  ; -> 002CA734
002CA6D7  sub      ecx, 1
002CA6DA  je       0x2ca6f7  ; -> 002CA6F7
002CA6DC  cmp      ecx, 2
002CA6DF  je       0x2ca7b2  ; -> 002CA7B2
002CA6E5  mov      rcx, rbx
002CA6E8  mov      rbx, qword ptr [rsp + 0x38]
002CA6ED  add      rsp, 0x20
002CA6F1  pop      rdi
002CA6F2  jmp      0x5c5230  ; -> 005C5230 fn
002CA6F7  mov      rcx, rbx
002CA6FA  call     0x2ca2e0  ; -> 002CA2E0 fn
002CA6FF  mov      rax, qword ptr [rbx + 0x108]
002CA706  test     dword ptr [rax + 0x168], 0x10000
002CA710  je       0x2ca723  ; -> 002CA723
002CA712  and      dword ptr [rbx + 0x50], 0xfffffffe
002CA716  xor      eax, eax
002CA718  mov      rbx, qword ptr [rsp + 0x38]
002CA71D  add      rsp, 0x20
002CA721  pop      rdi
002CA722  ret      
002CA723  or       dword ptr [rbx + 0x50], 1
002CA727  xor      eax, eax
002CA729  mov      rbx, qword ptr [rsp + 0x38]
002CA72E  add      rsp, 0x20
002CA732  pop      rdi
002CA733  ret      
002CA734  mov      rax, qword ptr [rip + 0x1dd04f5]  ; -> 0209AC30
002CA73B  lea      rcx, [rbx + 0x50]
002CA73F  mov      r9, rbx
002CA742  mov      qword ptr [rsp + 0x30], rsi
002CA747  mov      r8d, 6
002CA74D  mov      rdx, qword ptr [rax + 0x38]
002CA751  call     0x2432b0  ; -> 002432B0 fn
002CA756  movzx    ecx, word ptr [rax + 0xa]
002CA75A  movzx    edx, word ptr [rax + 8]
002CA75E  movsx    r8d, word ptr [rax + 6]
002CA763  test     rbx, rbx
002CA766  je       0x2ca789  ; -> 002CA789
002CA768  movzx    eax, word ptr [rax + 4]
002CA76C  mov      word ptr [rbx + 0x98], ax
002CA773  mov      word ptr [rbx + 0x9a], r8w
002CA77B  mov      word ptr [rbx + 0x9c], dx
002CA782  mov      word ptr [rbx + 0x9e], cx
002CA789  mov      eax, dword ptr [rdi + 8]
002CA78C  mov      dword ptr [rbx + 0xd4], eax
002CA792  mov      rax, qword ptr [rdi + 0x10]
002CA796  mov      qword ptr [rbx + 0x108], rax
002CA79D  test     dword ptr [rax + 0x168], 0x10000
002CA7A7  je       0x2ca7ad  ; -> 002CA7AD
002CA7A9  and      dword ptr [rbx + 0x50], 0xfffffffe
002CA7AD  mov      rsi, qword ptr [rsp + 0x30]
002CA7B2  xor      eax, eax
002CA7B4  mov      rbx, qword ptr [rsp + 0x38]
002CA7B9  add      rsp, 0x20
002CA7BD  pop      rdi
002CA7BE  ret      
```

## 002CB150 (156 B, extent 002CB150-002CB1EC)

Documented callee on this page: `002432B0`

```
002CB150  push     rbx
002CB152  sub      rsp, 0x20
002CB156  cmp      dword ptr [rdx], 1
002CB159  mov      rbx, rcx
002CB15C  je       0x2cb168  ; -> 002CB168
002CB15E  add      rsp, 0x20
002CB162  pop      rbx
002CB163  jmp      0x5c5230  ; -> 005C5230 fn
002CB168  mov      rax, qword ptr [rip + 0x1dcfac1]  ; -> 0209AC30
002CB16F  add      rcx, 0x50
002CB173  mov      r9, rbx
002CB176  mov      r8d, 8
002CB17C  mov      rdx, qword ptr [rax + 0x38]
002CB180  call     0x2432b0  ; -> 002432B0 fn
002CB185  xor      ecx, ecx
002CB187  movzx    edx, word ptr [rax + 0xa]
002CB18B  movzx    r8d, word ptr [rax + 8]
002CB190  movsx    r9d, word ptr [rax + 6]
002CB195  test     rbx, rbx
002CB198  je       0x2cb1c5  ; -> 002CB1C5
002CB19A  movzx    eax, word ptr [rax + 4]
002CB19E  mov      word ptr [rbx + 0x98], ax
002CB1A5  mov      rax, qword ptr [rbx + 0x60]
002CB1A9  mov      word ptr [rbx + 0x9a], r9w
002CB1B1  mov      word ptr [rbx + 0x9c], r8w
002CB1B9  mov      word ptr [rbx + 0x9e], dx
002CB1C0  mov      rdx, qword ptr [rax]
002CB1C3  jmp      0x2cb1c8  ; -> 002CB1C8
002CB1C5  mov      rdx, rcx
002CB1C8  and      dword ptr [rdx + 8], 0xfffffffe
002CB1CC  test     rbx, rbx
002CB1CF  je       0x2cb1d9  ; -> 002CB1D9
002CB1D1  mov      rax, qword ptr [rbx + 0x60]
002CB1D5  mov      rcx, qword ptr [rax + 8]
002CB1D9  and      dword ptr [rcx + 8], 0xfffffffe
002CB1DD  and      dword ptr [rbx + 0x40], 0xfffff7ff
002CB1E4  xor      eax, eax
002CB1E6  add      rsp, 0x20
002CB1EA  pop      rbx
002CB1EB  ret      
```

## 002D59E0 (590 B, extent 002D59E0-002D5C2E)

Documented callee on this page: `00264150`

```
002D59E0  push     rsi
002D59E2  push     rdi
002D59E3  sub      rsp, 0x78
002D59E7  mov      rax, qword ptr [rip + 0x1c6ee42]  ; -> 01F44830 [u64 0x00002B992DDFA232]
002D59EE  xor      rax, rsp
002D59F1  mov      qword ptr [rsp + 0x50], rax
002D59F6  mov      rdi, rcx
002D59F9  mov      ecx, dword ptr [rdx]
002D59FB  sub      ecx, 1
002D59FE  je       0x2d5bce  ; -> 002D5BCE
002D5A04  cmp      ecx, 1
002D5A07  je       0x2d5a16  ; -> 002D5A16
002D5A09  mov      rcx, rdi
002D5A0C  call     0x5c5230  ; -> 005C5230 fn
002D5A11  jmp      0x2d5c1a  ; -> 002D5C1A
002D5A16  mov      ecx, dword ptr [rdi + 0xb4]
002D5A1C  call     0x1edec0  ; -> 001EDEC0 fn
002D5A21  test     eax, eax
002D5A23  je       0x2d5c18  ; -> 002D5C18
002D5A29  cmp      dword ptr [rdi + 0xf0], 0
002D5A30  jne      0x2d5c18  ; -> 002D5C18
002D5A36  mov      rcx, qword ptr [rdi + 0xc0]
002D5A3D  mov      qword ptr [rsp + 0xa0], rbx
002D5A45  mov      qword ptr [rsp + 0x70], rbp
002D5A4A  mov      ebp, 1
002D5A4F  mov      qword ptr [rsp + 0x68], r14
002D5A54  mov      esi, ebp
002D5A56  mov      qword ptr [rsp + 0x60], r15
002D5A5B  xor      r15d, r15d
002D5A5E  mov      r14d, r15d
002D5A61  test     rcx, rcx
002D5A64  jne      0x2d5a6b  ; -> 002D5A6B
002D5A66  mov      ebp, r15d
002D5A69  jmp      0x2d5ae5  ; -> 002D5AE5
002D5A6B  mov      eax, dword ptr [rdi + 0xcc]
002D5A71  test     eax, eax
002D5A73  jg       0x2d5a85  ; -> 002D5A85
002D5A75  mov      ebp, r15d
002D5A78  cmp      qword ptr [rdi + 0xe0], rbp
002D5A7F  setne    bpl
002D5A83  jmp      0x2d5ae5  ; -> 002D5AE5
002D5A85  dec      eax
002D5A87  mov      dword ptr [rdi + 0xcc], eax
002D5A8D  test     eax, eax
002D5A8F  jg       0x2d5ae5  ; -> 002D5AE5
002D5A91  mov      eax, dword ptr [rdi + 0xd0]
002D5A97  test     eax, eax
002D5A99  jle      0x2d5ae5  ; -> 002D5AE5
002D5A9B  lea      rdx, [rsp + 0x20]
002D5AA0  mov      qword ptr [rsp + 0x20], rcx
002D5AA5  mov      qword ptr [rsp + 0x40], rdx
002D5AAA  lea      rbx, [rdi + 0xe0]
002D5AB1  lea      rdx, [rip - 0x428]  ; -> 002D5690
002D5AB8  mov      dword ptr [rsp + 0x38], r15d
002D5ABD  lea      r8, [rsp + 0x38]
002D5AC2  mov      qword ptr [rsp + 0x48], r15
002D5AC7  mov      ecx, 0xe0
002D5ACC  mov      dword ptr [rsp + 0x28], eax
002D5AD0  mov      qword ptr [rsp + 0x30], rbx
002D5AD5  call     0x244f50  ; -> 00244F50 fn
002D5ADA  mov      rcx, rax
002D5ADD  mov      qword ptr [rbx], rax
002D5AE0  call     0x246ac0  ; -> 00246AC0 fn
002D5AE5  call     0x254a10  ; -> 00254A10 fn
002D5AEA  test     eax, eax
002D5AEC  je       0x2d5af7  ; -> 002D5AF7
002D5AEE  call     0x264150  ; -> 00264150 fn
002D5AF3  test     eax, eax
002D5AF5  je       0x2d5afa  ; -> 002D5AFA
002D5AF7  mov      r14d, esi
002D5AFA  mov      ecx, dword ptr [rdi + 0xc8]
002D5B00  test     ecx, ecx
002D5B02  jle      0x2d5b98  ; -> 002D5B98
002D5B08  cmp      ecx, 0xc8
002D5B0E  je       0x2d5b98  ; -> 002D5B98
002D5B14  test     r14d, r14d
002D5B17  je       0x2d5b1d  ; -> 002D5B1D
002D5B19  cmp      ecx, esi
002D5B1B  je       0x2d5b98  ; -> 002D5B98
002D5B1D  mov      eax, dword ptr [rdi + 0xd4]
002D5B23  test     eax, eax
002D5B25  jg       0x2d5b37  ; -> 002D5B37
002D5B27  mov      esi, r15d
002D5B2A  cmp      qword ptr [rdi + 0xe8], rsi
002D5B31  setne    sil
002D5B35  jmp      0x2d5b9b  ; -> 002D5B9B
002D5B37  dec      eax
002D5B39  mov      dword ptr [rdi + 0xd4], eax
002D5B3F  test     eax, eax
002D5B41  jg       0x2d5b9b  ; -> 002D5B9B
002D5B43  mov      eax, dword ptr [rdi + 0xd8]
002D5B49  test     eax, eax
002D5B4B  jle      0x2d5b9b  ; -> 002D5B9B
002D5B4D  lea      rdx, [rsp + 0x20]
002D5B52  mov      dword ptr [rsp + 0x20], ecx
002D5B56  mov      qword ptr [rsp + 0x40], rdx
002D5B5B  lea      rbx, [rdi + 0xe8]
002D5B62  lea      rdx, [rip - 0x339]  ; -> 002D5830
002D5B69  mov      dword ptr [rsp + 0x38], r15d
002D5B6E  lea      r8, [rsp + 0x38]
002D5B73  mov      qword ptr [rsp + 0x48], r15
002D5B78  mov      ecx, 0xd8
002D5B7D  mov      dword ptr [rsp + 0x24], eax
002D5B81  mov      qword ptr [rsp + 0x28], rbx
002D5B86  call     0x244f50  ; -> 00244F50 fn
002D5B8B  mov      rcx, rax
002D5B8E  mov      qword ptr [rbx], rax
002D5B91  call     0x246ac0  ; -> 00246AC0 fn
002D5B96  jmp      0x2d5b9b  ; -> 002D5B9B
002D5B98  mov      esi, r15d
002D5B9B  mov      r15, qword ptr [rsp + 0x60]
002D5BA0  test     ebp, ebp
002D5BA2  mov      rbp, qword ptr [rsp + 0x70]
002D5BA7  mov      r14, qword ptr [rsp + 0x68]
002D5BAC  mov      rbx, qword ptr [rsp + 0xa0]
002D5BB4  jne      0x2d5c18  ; -> 002D5C18
002D5BB6  test     esi, esi
002D5BB8  jne      0x2d5c18  ; -> 002D5C18
002D5BBA  mov      rcx, rdi
002D5BBD  mov      dword ptr [rdi + 0xf0], 1
002D5BC7  call     0x244f00  ; -> 00244F00 fn
002D5BCC  jmp      0x2d5c18  ; -> 002D5C18
002D5BCE  mov      rcx, qword ptr [rdx + 8]
002D5BD2  mov      rax, qword ptr [rcx]
002D5BD5  mov      qword ptr [rdi + 0xc0], rax
002D5BDC  mov      eax, dword ptr [rcx + 8]
002D5BDF  mov      dword ptr [rdi + 0xc8], eax
002D5BE5  mov      eax, dword ptr [rcx + 0xc]
002D5BE8  mov      dword ptr [rdi + 0xcc], eax
002D5BEE  mov      eax, dword ptr [rcx + 0x10]
002D5BF1  mov      dword ptr [rdi + 0xd0], eax
002D5BF7  mov      eax, dword ptr [rcx + 0x14]
002D5BFA  mov      dword ptr [rdi + 0xd4], eax
002D5C00  mov      eax, dword ptr [rcx + 0x18]
002D5C03  mov      rcx, rdi
002D5C06  and      dword ptr [rdi + 0x40], 0xffffff7f
002D5C0D  mov      dword ptr [rdi + 0xd8], eax
002D5C13  call     0x246ac0  ; -> 00246AC0 fn
002D5C18  xor      eax, eax
002D5C1A  mov      rcx, qword ptr [rsp + 0x50]
002D5C1F  xor      rcx, rsp
002D5C22  call     0x808c40  ; -> 00808C40 fn
002D5C27  add      rsp, 0x78
002D5C2B  pop      rdi
002D5C2C  pop      rsi
002D5C2D  ret      
```

## 002D5E00 (161 B, extent 002D5E00-002D5EA1)

Documented callee on this page: `002432B0`

```
002D5E00  push     rbx
002D5E02  sub      rsp, 0x20
002D5E06  cmp      dword ptr [rdx], 1
002D5E09  mov      rbx, rcx
002D5E0C  je       0x2d5e18  ; -> 002D5E18
002D5E0E  add      rsp, 0x20
002D5E12  pop      rbx
002D5E13  jmp      0x5c5230  ; -> 005C5230 fn
002D5E18  mov      rax, qword ptr [rip + 0x1dc4e11]  ; -> 0209AC30
002D5E1F  add      rcx, 0x50
002D5E23  mov      r9, rbx
002D5E26  mov      r8d, 1
002D5E2C  mov      rdx, qword ptr [rax + 0x18]
002D5E30  call     0x2432b0  ; -> 002432B0 fn
002D5E35  mov      rdx, rax
002D5E38  test     rbx, rbx
002D5E3B  jne      0x2d5e41  ; -> 002D5E41
002D5E3D  xor      ecx, ecx
002D5E3F  jmp      0x2d5e48  ; -> 002D5E48
002D5E41  mov      rax, qword ptr [rbx + 0x60]
002D5E45  mov      rcx, qword ptr [rax]
002D5E48  or       dword ptr [rcx + 0x20], 0x8000000
002D5E4F  movzx    ecx, word ptr [rdx + 0xa]
002D5E53  movzx    r8d, word ptr [rdx + 8]
002D5E58  movsx    r9d, word ptr [rdx + 6]
002D5E5D  test     rbx, rbx
002D5E60  je       0x2d5e84  ; -> 002D5E84
002D5E62  movzx    eax, word ptr [rdx + 4]
002D5E66  mov      word ptr [rbx + 0x98], ax
002D5E6D  mov      word ptr [rbx + 0x9a], r9w
002D5E75  mov      word ptr [rbx + 0x9c], r8w
002D5E7D  mov      word ptr [rbx + 0x9e], cx
002D5E84  mov      ecx, 5
002D5E89  call     0x2735e0  ; -> 002735E0 fn
002D5E8E  mov      rdx, rax
002D5E91  mov      rcx, rbx
002D5E94  call     0x247570  ; -> 00247570 fn
002D5E99  xor      eax, eax
002D5E9B  add      rsp, 0x20
002D5E9F  pop      rbx
002D5EA0  ret      
```

## 00347580 (67 B, extent 00347580-003475C3)

Documented callee on this page: `00264010`

```
00347580  push     rbx
00347582  sub      rsp, 0x30
00347586  mov      rbx, rcx
00347589  mov      rcx, r9
0034758C  call     0x267e10  ; -> 00267E10 fn
00347591  mov      ecx, eax
00347593  call     0x264010  ; -> 00264010 fn
00347598  lea      r9, [rsp + 0x24]
0034759D  mov      rcx, rax
003475A0  lea      r8, [rsp + 0x28]
003475A5  lea      rdx, [rsp + 0x20]
003475AA  call     0x265020  ; -> 00265020 fn
003475AF  movss    xmm1, dword ptr [rsp + 0x20]
003475B5  mov      rcx, rbx
003475B8  call     0x26b4c0  ; -> 0026B4C0 fn
003475BD  add      rsp, 0x30
003475C1  pop      rbx
003475C2  ret      
```

## 00347600 (81 B, extent 00347600-00347651)

Documented callee on this page: `00264010`

```
00347600  mov      qword ptr [rsp + 8], rbx
00347605  mov      qword ptr [rsp + 0x10], rsi
0034760A  push     rdi
0034760B  sub      rsp, 0x20
0034760F  mov      rcx, r9
00347612  mov      rsi, r9
00347615  call     0x267e10  ; -> 00267E10 fn
0034761A  mov      rcx, rsi
0034761D  mov      edi, eax
0034761F  call     0x267e10  ; -> 00267E10 fn
00347624  mov      rcx, rsi
00347627  mov      ebx, eax
00347629  call     0x267e10  ; -> 00267E10 fn
0034762E  mov      ecx, eax
00347630  call     0x264010  ; -> 00264010 fn
00347635  mov      r8d, edi
00347638  mov      edx, ebx
0034763A  mov      rcx, rax
0034763D  mov      rbx, qword ptr [rsp + 0x30]
00347642  mov      rsi, qword ptr [rsp + 0x38]
00347647  add      rsp, 0x20
0034764B  pop      rdi
0034764C  jmp      0x4737d0  ; -> 004737D0 fn
```

## 00347AB0 (67 B, extent 00347AB0-00347AF3)

Documented callee on this page: `00264010`

```
00347AB0  push     rbx
00347AB2  sub      rsp, 0x30
00347AB6  mov      rbx, rcx
00347AB9  mov      rcx, r9
00347ABC  call     0x267e10  ; -> 00267E10 fn
00347AC1  mov      ecx, eax
00347AC3  call     0x264010  ; -> 00264010 fn
00347AC8  lea      r9, [rsp + 0x24]
00347ACD  mov      rcx, rax
00347AD0  lea      r8, [rsp + 0x20]
00347AD5  lea      rdx, [rsp + 0x28]
00347ADA  call     0x265020  ; -> 00265020 fn
00347ADF  movss    xmm1, dword ptr [rsp + 0x20]
00347AE5  mov      rcx, rbx
00347AE8  call     0x26b4c0  ; -> 0026B4C0 fn
00347AED  add      rsp, 0x30
00347AF1  pop      rbx
00347AF2  ret      
```

## 00347BE0 (81 B, extent 00347BE0-00347C31)

Documented callee on this page: `00264010`

```
00347BE0  mov      qword ptr [rsp + 8], rbx
00347BE5  mov      qword ptr [rsp + 0x10], rsi
00347BEA  push     rdi
00347BEB  sub      rsp, 0x20
00347BEF  mov      rcx, r9
00347BF2  mov      rsi, r9
00347BF5  call     0x267e10  ; -> 00267E10 fn
00347BFA  mov      rcx, rsi
00347BFD  mov      edi, eax
00347BFF  call     0x267e10  ; -> 00267E10 fn
00347C04  mov      rcx, rsi
00347C07  mov      ebx, eax
00347C09  call     0x267e10  ; -> 00267E10 fn
00347C0E  mov      ecx, eax
00347C10  call     0x264010  ; -> 00264010 fn
00347C15  mov      r8d, edi
00347C18  mov      edx, ebx
00347C1A  mov      rcx, rax
00347C1D  mov      rbx, qword ptr [rsp + 0x30]
00347C22  mov      rsi, qword ptr [rsp + 0x38]
00347C27  add      rsp, 0x20
00347C2B  pop      rdi
00347C2C  jmp      0x473690  ; -> 00473690 fn
```

## 00347FF0 (67 B, extent 00347FF0-00348033)

Documented callee on this page: `00264010`

```
00347FF0  push     rbx
00347FF2  sub      rsp, 0x30
00347FF6  mov      rbx, rcx
00347FF9  mov      rcx, r9
00347FFC  call     0x267e10  ; -> 00267E10 fn
00348001  mov      ecx, eax
00348003  call     0x264010  ; -> 00264010 fn
00348008  lea      r9, [rsp + 0x20]
0034800D  mov      rcx, rax
00348010  lea      r8, [rsp + 0x24]
00348015  lea      rdx, [rsp + 0x28]
0034801A  call     0x265020  ; -> 00265020 fn
0034801F  movss    xmm1, dword ptr [rsp + 0x20]
00348025  mov      rcx, rbx
00348028  call     0x26b4c0  ; -> 0026B4C0 fn
0034802D  add      rsp, 0x30
00348031  pop      rbx
00348032  ret      
```

## 00348800 (55 B, extent 00348800-00348837)

Documented callee on this page: `00264010`

```
00348800  push     rbx
00348802  sub      rsp, 0x20
00348806  mov      rbx, rcx
00348809  mov      rcx, r9
0034880C  call     0x267e10  ; -> 00267E10 fn
00348811  mov      ecx, eax
00348813  call     0x264010  ; -> 00264010 fn
00348818  mov      rcx, rax
0034881B  call     0x263f10  ; -> 00263F10 fn
00348820  mov      rcx, rax
00348823  call     0x4736e0  ; -> 004736E0 fn
00348828  mov      edx, eax
0034882A  mov      rcx, rbx
0034882D  add      rsp, 0x20
00348831  pop      rbx
00348832  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 00349490 (48 B, extent 00349490-003494C0)

Documented callee on this page: `00264010`

```
00349490  push     rbx
00349492  sub      rsp, 0x20
00349496  mov      rbx, rcx
00349499  mov      rcx, r9
0034949C  call     0x267e10  ; -> 00267E10 fn
003494A1  mov      ecx, eax
003494A3  call     0x264010  ; -> 00264010 fn
003494A8  mov      rcx, rax
003494AB  call     0x263cc0  ; -> 00263CC0 fn
003494B0  movaps   xmm1, xmm0
003494B3  mov      rcx, rbx
003494B6  add      rsp, 0x20
003494BA  pop      rbx
003494BB  jmp      0x26b4c0  ; -> 0026B4C0 fn
```

## 0034AAD0 (74 B, extent 0034AAD0-0034AB1A)

Documented callee on this page: `00263F10`

```
0034AAD0  mov      qword ptr [rsp + 8], rbx
0034AAD5  mov      qword ptr [rsp + 0x10], rsi
0034AADA  push     rdi
0034AADB  sub      rsp, 0x20
0034AADF  mov      rsi, rcx
0034AAE2  mov      rdi, rdx
0034AAE5  mov      rcx, r9
0034AAE8  call     0x267e10  ; -> 00267E10 fn
0034AAED  mov      rcx, rdi
0034AAF0  mov      ebx, eax
0034AAF2  call     0x263f10  ; -> 00263F10 fn
0034AAF7  mov      edx, ebx
0034AAF9  mov      rcx, rax
0034AAFC  call     0x35a0c0  ; -> 0035A0C0 fn
0034AB01  mov      edx, eax
0034AB03  mov      rcx, rsi
0034AB06  mov      rbx, qword ptr [rsp + 0x30]
0034AB0B  mov      rsi, qword ptr [rsp + 0x38]
0034AB10  add      rsp, 0x20
0034AB14  pop      rdi
0034AB15  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 0034B060 (55 B, extent 0034B060-0034B097)

Documented callee on this page: `00264010`

```
0034B060  push     rbx
0034B062  sub      rsp, 0x20
0034B066  mov      rbx, rcx
0034B069  mov      rcx, r9
0034B06C  call     0x267e10  ; -> 00267E10 fn
0034B071  mov      ecx, eax
0034B073  call     0x264010  ; -> 00264010 fn
0034B078  mov      rcx, rax
0034B07B  call     0x263f10  ; -> 00263F10 fn
0034B080  mov      rcx, rax
0034B083  call     0x473710  ; -> 00473710 fn
0034B088  mov      edx, eax
0034B08A  mov      rcx, rbx
0034B08D  add      rsp, 0x20
0034B091  pop      rbx
0034B092  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 0034C1D0 (55 B, extent 0034C1D0-0034C207)

Documented callee on this page: `00264010`

```
0034C1D0  push     rbx
0034C1D2  sub      rsp, 0x20
0034C1D6  mov      rbx, rcx
0034C1D9  mov      rcx, r9
0034C1DC  call     0x267e10  ; -> 00267E10 fn
0034C1E1  mov      ecx, eax
0034C1E3  call     0x264010  ; -> 00264010 fn
0034C1E8  mov      rcx, rax
0034C1EB  call     0x263f10  ; -> 00263F10 fn
0034C1F0  mov      rcx, rax
0034C1F3  call     0x473770  ; -> 00473770 fn
0034C1F8  mov      edx, eax
0034C1FA  mov      rcx, rbx
0034C1FD  add      rsp, 0x20
0034C201  pop      rbx
0034C202  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 0034C500 (74 B, extent 0034C500-0034C54A)

Documented callee on this page: `00263F10`

```
0034C500  mov      qword ptr [rsp + 8], rbx
0034C505  push     rdi
0034C506  sub      rsp, 0x20
0034C50A  mov      rdi, rcx
0034C50D  mov      rcx, r9
0034C510  call     0x267e10  ; -> 00267E10 fn
0034C515  mov      ebx, eax
0034C517  call     0x2640c0  ; -> 002640C0 fn
0034C51C  mov      edx, ebx
0034C51E  mov      rcx, rax
0034C521  call     0x358940  ; -> 00358940 fn
0034C526  mov      rcx, rax
0034C529  call     0x263f10  ; -> 00263F10 fn
0034C52E  mov      rcx, rax
0034C531  call     0x3597b0  ; -> 003597B0 fn
0034C536  mov      edx, eax
0034C538  mov      rcx, rdi
0034C53B  mov      rbx, qword ptr [rsp + 0x30]
0034C540  add      rsp, 0x20
0034C544  pop      rdi
0034C545  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 0034C6A0 (96 B, extent 0034C6A0-0034C700)

Documented callee on this page: `00264010`

```
0034C6A0  mov      qword ptr [rsp + 8], rbx
0034C6A5  mov      qword ptr [rsp + 0x10], rsi
0034C6AA  push     rdi
0034C6AB  sub      rsp, 0x20
0034C6AF  mov      rsi, rcx
0034C6B2  mov      rbx, r9
0034C6B5  mov      rcx, r9
0034C6B8  call     0x267e10  ; -> 00267E10 fn
0034C6BD  mov      rcx, rbx
0034C6C0  mov      edi, eax
0034C6C2  call     0x267e10  ; -> 00267E10 fn
0034C6C7  mov      ecx, eax
0034C6C9  call     0x264010  ; -> 00264010 fn
0034C6CE  mov      rcx, rax
0034C6D1  call     0x263f10  ; -> 00263F10 fn
0034C6D6  xor      ecx, ecx
0034C6D8  test     edi, edi
0034C6DA  cmovs    edi, ecx
0034C6DD  mov      rcx, rax
0034C6E0  mov      edx, edi
0034C6E2  call     0x4737a0  ; -> 004737A0 fn
0034C6E7  mov      edx, eax
0034C6E9  mov      rcx, rsi
0034C6EC  mov      rbx, qword ptr [rsp + 0x30]
0034C6F1  mov      rsi, qword ptr [rsp + 0x38]
0034C6F6  add      rsp, 0x20
0034C6FA  pop      rdi
0034C6FB  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 0034CC60 (74 B, extent 0034CC60-0034CCAA)

Documented callee on this page: `00263F10`

```
0034CC60  mov      qword ptr [rsp + 8], rbx
0034CC65  push     rdi
0034CC66  sub      rsp, 0x20
0034CC6A  mov      rdi, rcx
0034CC6D  mov      rcx, r9
0034CC70  call     0x267e10  ; -> 00267E10 fn
0034CC75  mov      ebx, eax
0034CC77  call     0x2640c0  ; -> 002640C0 fn
0034CC7C  mov      edx, ebx
0034CC7E  mov      rcx, rax
0034CC81  call     0x358940  ; -> 00358940 fn
0034CC86  mov      rcx, rax
0034CC89  call     0x263f10  ; -> 00263F10 fn
0034CC8E  mov      rcx, rax
0034CC91  call     0x3597d0  ; -> 003597D0 fn
0034CC96  mov      edx, eax
0034CC98  mov      rcx, rdi
0034CC9B  mov      rbx, qword ptr [rsp + 0x30]
0034CCA0  add      rsp, 0x20
0034CCA4  pop      rdi
0034CCA5  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 0034DA30 (75 B, extent 0034DA30-0034DA7B)

Documented callee on this page: `00263F10`

```
0034DA30  mov      qword ptr [rsp + 8], rbx
0034DA35  mov      qword ptr [rsp + 0x10], rsi
0034DA3A  push     rdi
0034DA3B  sub      rsp, 0x20
0034DA3F  mov      rsi, rcx
0034DA42  mov      rdi, r9
0034DA45  mov      rcx, rdx
0034DA48  call     0x263f10  ; -> 00263F10 fn
0034DA4D  mov      rcx, rdi
0034DA50  mov      rbx, rax
0034DA53  call     0x267e10  ; -> 00267E10 fn
0034DA58  mov      edx, eax
0034DA5A  mov      rcx, rbx
0034DA5D  call     0x35a1c0  ; -> 0035A1C0 fn
0034DA62  mov      edx, eax
0034DA64  mov      rcx, rsi
0034DA67  mov      rbx, qword ptr [rsp + 0x30]
0034DA6C  mov      rsi, qword ptr [rsp + 0x38]
0034DA71  add      rsp, 0x20
0034DA75  pop      rdi
0034DA76  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 0034E190 (89 B, extent 0034E190-0034E1E9)

Documented callee on this page: `00264010`

```
0034E190  mov      qword ptr [rsp + 8], rbx
0034E195  mov      qword ptr [rsp + 0x10], rsi
0034E19A  push     rdi
0034E19B  sub      rsp, 0x20
0034E19F  mov      rsi, rcx
0034E1A2  mov      rbx, r9
0034E1A5  mov      rcx, r9
0034E1A8  call     0x267e10  ; -> 00267E10 fn
0034E1AD  mov      rcx, rbx
0034E1B0  mov      edi, eax
0034E1B2  call     0x267e10  ; -> 00267E10 fn
0034E1B7  mov      ecx, eax
0034E1B9  call     0x264010  ; -> 00264010 fn
0034E1BE  mov      rcx, rax
0034E1C1  call     0x263f10  ; -> 00263F10 fn
0034E1C6  mov      edx, edi
0034E1C8  mov      rcx, rax
0034E1CB  call     0x35a1c0  ; -> 0035A1C0 fn
0034E1D0  mov      edx, eax
0034E1D2  mov      rcx, rsi
0034E1D5  mov      rbx, qword ptr [rsp + 0x30]
0034E1DA  mov      rsi, qword ptr [rsp + 0x38]
0034E1DF  add      rsp, 0x20
0034E1E3  pop      rdi
0034E1E4  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 00351EE0 (37 B, extent 00351EE0-00351F05)

Documented callee on this page: `00264010`

```
00351EE0  push     rbx
00351EE2  sub      rsp, 0x20
00351EE6  mov      rcx, r9
00351EE9  mov      rbx, r8
00351EEC  call     0x267e10  ; -> 00267E10 fn
00351EF1  mov      ecx, eax
00351EF3  call     0x264010  ; -> 00264010 fn
00351EF8  mov      qword ptr [rbx], rax
00351EFB  add      rsp, 0x20
00351EFF  pop      rbx
00351F00  jmp      0x473b20  ; -> 00473B20 fn
```

## 00352270 (79 B, extent 00352270-003522BF)

Documented callee on this page: `00263F10`

```
00352270  mov      qword ptr [rsp + 8], rbx
00352275  push     rdi
00352276  sub      rsp, 0x20
0035227A  mov      rcx, r9
0035227D  mov      rbx, rdx
00352280  call     0x267e10  ; -> 00267E10 fn
00352285  mov      rcx, rbx
00352288  mov      edi, eax
0035228A  call     0x263f10  ; -> 00263F10 fn
0035228F  mov      rcx, rax
00352292  call     0x3589b0  ; -> 003589B0 fn
00352297  cmp      byte ptr [rbx + 0x15], 3
0035229B  mov      edx, eax
0035229D  mov      ecx, edi
0035229F  jne      0x3522b0  ; -> 003522B0
003522A1  mov      rbx, qword ptr [rsp + 0x30]
003522A6  add      rsp, 0x20
003522AA  pop      rdi
003522AB  jmp      0x36e880  ; -> 0036E880 fn
003522B0  mov      rbx, qword ptr [rsp + 0x30]
003522B5  add      rsp, 0x20
003522B9  pop      rdi
003522BA  jmp      0x36e7e0  ; -> 0036E7E0 fn
```

## 00352940 (58 B, extent 00352940-0035297A)

Documented callee on this page: `00263F10`

```
00352940  mov      qword ptr [rsp + 8], rbx
00352945  push     rdi
00352946  sub      rsp, 0x20
0035294A  mov      rcx, r9
0035294D  mov      rbx, rdx
00352950  call     0x267e10  ; -> 00267E10 fn
00352955  mov      rcx, rbx
00352958  mov      edi, eax
0035295A  call     0x263f10  ; -> 00263F10 fn
0035295F  mov      rcx, rax
00352962  call     0x3589b0  ; -> 003589B0 fn
00352967  mov      edx, eax
00352969  mov      ecx, edi
0035296B  mov      rbx, qword ptr [rsp + 0x30]
00352970  add      rsp, 0x20
00352974  pop      rdi
00352975  jmp      0x36e7b0  ; -> 0036E7B0 fn
```

## 003C9840 (86 B, extent 003C9840-003C9896)

Documented callee on this page: `003C5FB0`

```
003C9840  push     rbx
003C9842  sub      rsp, 0x20
003C9846  cmp      qword ptr [rcx + 0xc8], 0
003C984E  mov      rbx, rcx
003C9851  je       0x3c9890  ; -> 003C9890
003C9853  call     0x3c5fb0  ; -> 003C5FB0 fn
003C9858  mov      rcx, rbx
003C985B  mov      edx, 2
003C9860  test     eax, eax
003C9862  jne      0x3c9869  ; -> 003C9869
003C9864  mov      edx, 1
003C9869  call     0x394690  ; -> 00394690 fn
003C986E  mov      rcx, qword ptr [rbx + 0xc8]
003C9875  movsx    edx, word ptr [rax + 0xe]
003C9879  test     rcx, rcx
003C987C  je       0x3c9890  ; -> 003C9890
003C987E  movzx    eax, word ptr [rax + 0xc]
003C9882  mov      word ptr [rcx + 0x98], ax
003C9889  mov      word ptr [rcx + 0x9a], dx
003C9890  add      rsp, 0x20
003C9894  pop      rbx
003C9895  ret      
```

## 003FC3F0 (283 B, extent 003FC3F0-003FC50B)

Documented callee on this page: `002432B0`

```
003FC3F0  push     rbx
003FC3F2  sub      rsp, 0x20
003FC3F6  mov      rbx, rcx
003FC3F9  mov      ecx, dword ptr [rdx]
003FC3FB  sub      ecx, 1
003FC3FE  je       0x3fc46d  ; -> 003FC46D
003FC400  sub      ecx, 1
003FC403  je       0x3fc42b  ; -> 003FC42B
003FC405  cmp      ecx, 0xd
003FC408  je       0x3fc417  ; -> 003FC417
003FC40A  mov      rcx, rbx
003FC40D  add      rsp, 0x20
003FC411  pop      rbx
003FC412  jmp      0x5c5230  ; -> 005C5230 fn
003FC417  mov      eax, 1
003FC41C  mov      word ptr [rbx + 0xc2], ax
003FC423  xor      eax, eax
003FC425  add      rsp, 0x20
003FC429  pop      rbx
003FC42A  ret      
003FC42B  cmp      word ptr [rbx + 0xc2], 0
003FC433  jne      0x3fc503  ; -> 003FC503
003FC439  imul     ecx, dword ptr [rip + 0x1a01c74], 0x3c  ; -> 01DFE0B4 [u32 0x00000001]
003FC440  movsx    edx, word ptr [rbx + 0xc0]
003FC447  cmp      edx, ecx
003FC449  jb       0x3fc45b  ; -> 003FC45B
003FC44B  mov      rcx, rbx
003FC44E  call     0x244f00  ; -> 00244F00 fn
003FC453  xor      eax, eax
003FC455  add      rsp, 0x20
003FC459  pop      rbx
003FC45A  ret      
003FC45B  inc      dx
003FC45E  mov      word ptr [rbx + 0xc0], dx
003FC465  xor      eax, eax
003FC467  add      rsp, 0x20
003FC46B  pop      rbx
003FC46C  ret      
003FC46D  mov      qword ptr [rsp + 0x30], rbp
003FC472  mov      qword ptr [rsp + 0x38], rsi
003FC477  mov      qword ptr [rsp + 0x40], rdi
003FC47C  call     0x35d3f0  ; -> 0035D3F0 fn
003FC481  lea      rcx, [rbx + 0x50]
003FC485  mov      r9, rbx
003FC488  mov      r8d, 2
003FC48E  mov      rdx, rax
003FC491  call     0x2432b0  ; -> 002432B0 fn
003FC496  mov      rdi, rax
003FC499  movzx    esi, word ptr [rax + 0xa]
003FC49D  movzx    ebp, word ptr [rax + 8]
003FC4A1  call     0x28f810  ; -> 0028F810 fn
003FC4A6  movzx    ecx, word ptr [rdi + 0xa]
003FC4AA  mov      edx, 0xc
003FC4AF  sub      edx, ecx
003FC4B1  add      eax, edx
003FC4B3  test     rbx, rbx
003FC4B6  je       0x3fc4d8  ; -> 003FC4D8
003FC4B8  movzx    ecx, word ptr [rdi + 4]
003FC4BC  mov      word ptr [rbx + 0x98], cx
003FC4C3  mov      word ptr [rbx + 0x9a], ax
003FC4CA  mov      word ptr [rbx + 0x9c], bp
003FC4D1  mov      word ptr [rbx + 0x9e], si
003FC4D8  lea      rdx, [rip + 0x915b11]  ; -> 00D11FF0
003FC4DF  mov      rcx, rbx
003FC4E2  call     0x247570  ; -> 00247570 fn
003FC4E7  mov      edx, 0x58
003FC4EC  mov      rcx, rbx
003FC4EF  call     0x247930  ; -> 00247930 fn
003FC4F4  mov      rdi, qword ptr [rsp + 0x40]
003FC4F9  mov      rsi, qword ptr [rsp + 0x38]
003FC4FE  mov      rbp, qword ptr [rsp + 0x30]
003FC503  xor      eax, eax
003FC505  add      rsp, 0x20
003FC509  pop      rbx
003FC50A  ret      
```

## 0050E3A0 (101 B, extent 0050E3A0-0050E405)

Documented callee on this page: `002E97B0`

```
0050E3A0  mov      qword ptr [rsp + 8], rbx
0050E3A5  mov      qword ptr [rsp + 0x10], rsi
0050E3AA  push     rdi
0050E3AB  sub      rsp, 0x20
0050E3AF  mov      rcx, rdx
0050E3B2  mov      rdi, r9
0050E3B5  mov      rsi, rdx
0050E3B8  call     0x2e97b0  ; -> 002E97B0 fn
0050E3BD  mov      rcx, rdi
0050E3C0  mov      rbx, rax
0050E3C3  call     0x267e10  ; -> 00267E10 fn
0050E3C8  test     rbx, rbx
0050E3CB  je       0x50e3ea  ; -> 0050E3EA
0050E3CD  bts      eax, 0xc
0050E3D1  mov      rcx, rsi
0050E3D4  mov      edx, eax
0050E3D6  mov      rbx, qword ptr [rsp + 0x30]
0050E3DB  mov      rsi, qword ptr [rsp + 0x38]
0050E3E0  add      rsp, 0x20
0050E3E4  pop      rdi
0050E3E5  jmp      0x2eb330  ; -> 002EB330 fn
0050E3EA  lea      rcx, [rip + 0x814627]  ; -> 00D22A18
0050E3F1  mov      rbx, qword ptr [rsp + 0x30]
0050E3F6  mov      rsi, qword ptr [rsp + 0x38]
0050E3FB  add      rsp, 0x20
0050E3FF  pop      rdi
0050E400  jmp      0x17d280  ; -> 0017D280 fn
```

## 0057FA30 (197 B, extent 0057FA30-0057FAF5)

Documented callee on this page: `002F9860`

```
0057FA30  mov      qword ptr [rsp + 8], rbx
0057FA35  push     rdi
0057FA36  sub      rsp, 0x20
0057FA3A  xor      edx, edx
0057FA3C  mov      rdi, r8
0057FA3F  mov      rbx, rcx
0057FA42  call     0x393190  ; -> 00393190 fn
0057FA47  mov      rax, qword ptr [rbx + 0x10]
0057FA4B  lea      r9, [rip + 0x7a445a]  ; -> 00D23EAC
0057FA52  mov      rdx, qword ptr [rax + 0xd8]
0057FA59  and      dword ptr [rdx + 8], 0xfffffffe
0057FA5D  mov      rax, qword ptr [rbx + 0x10]
0057FA61  mov      rdx, qword ptr [rax + 0xb0]
0057FA68  or       dword ptr [rdx + 8], 1
0057FA6C  xor      r8d, r8d
0057FA6F  nop      
0057FA70  movzx    ecx, byte ptr [r9]
0057FA74  lea      r9, [r9 + 1]
0057FA78  mov      rax, qword ptr [rbx + 0x10]
0057FA7C  inc      r8d
0057FA7F  mov      rdx, qword ptr [rax + rcx*8]
0057FA83  or       dword ptr [rdx + 8], 1
0057FA87  cmp      r8d, 7
0057FA8B  jb       0x57fa70  ; -> 0057FA70
0057FA8D  mov      rax, qword ptr [rbx + 0x10]
0057FA91  mov      rcx, qword ptr [rax + 0xd0]
0057FA98  and      dword ptr [rcx + 8], 0xfffffffe
0057FA9C  mov      ecx, dword ptr [rdi]
0057FA9E  sub      ecx, 3
0057FAA1  je       0x57fac4  ; -> 0057FAC4
0057FAA3  sub      ecx, 1
0057FAA6  je       0x57fabd  ; -> 0057FABD
0057FAA8  cmp      ecx, 1
0057FAAB  je       0x57fab6  ; -> 0057FAB6
0057FAAD  lea      rcx, [rip + 0x176bb84]  ; -> 01CEB638
0057FAB4  jmp      0x57fad1  ; -> 0057FAD1
0057FAB6  mov      ecx, 0x872
0057FABB  jmp      0x57fac9  ; -> 0057FAC9
0057FABD  mov      ecx, 0x873
0057FAC2  jmp      0x57fac9  ; -> 0057FAC9
0057FAC4  mov      ecx, 0x874
0057FAC9  call     0x2f9860  ; -> 002F9860 fn
0057FACE  mov      rcx, rax
0057FAD1  mov      rax, qword ptr [rbx + 0x10]
0057FAD5  mov      rbx, qword ptr [rax + 0xb0]
0057FADC  mov      qword ptr [rbx + 0x18], rcx
0057FAE0  xor      ecx, ecx
0057FAE2  call     0x20e620  ; -> 0020E620 fn
0057FAE7  mov      dword ptr [rbx + 0x20], eax
0057FAEA  mov      rbx, qword ptr [rsp + 0x30]
0057FAEF  add      rsp, 0x20
0057FAF3  pop      rdi
0057FAF4  ret      
```
