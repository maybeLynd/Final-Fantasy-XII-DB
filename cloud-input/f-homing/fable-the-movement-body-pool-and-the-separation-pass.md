# F homing pack (FABLE): `06-Movement-And-Navigation/the-movement-body-pool-and-the-separation-pass.md`

Generated 2026-10-03 04:02 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 8. No bearing page cites them and no documented function calls them directly.

## 0023B2A0 (49 B, extent 0023B2A0-0023B2D1)

Documented callee on this page: `0026BF60`

```
0023B2A0  push     rbx
0023B2A2  sub      rsp, 0x30
0023B2A6  movaps   xmmword ptr [rsp + 0x20], xmm6
0023B2AB  mov      rbx, rcx
0023B2AE  movaps   xmm6, xmm1
0023B2B1  movaps   xmm1, xmm2
0023B2B4  call     0x26bbc0  ; -> 0026BBC0 fn
0023B2B9  movaps   xmm2, xmm6
0023B2BC  movaps   xmm1, xmm6
0023B2BF  mov      rcx, rbx
0023B2C2  movaps   xmm6, xmmword ptr [rsp + 0x20]
0023B2C7  add      rsp, 0x30
0023B2CB  pop      rbx
0023B2CC  jmp      0x26bf60  ; -> 0026BF60 fn
```

## 00347D20 (64 B, extent 00347D20-00347D60)

Documented callee on this page: `002EBC70`

```
00347D20  mov      qword ptr [rsp + 8], rbx
00347D25  push     rdi
00347D26  sub      rsp, 0x20
00347D2A  mov      rcx, r9
00347D2D  mov      rbx, r9
00347D30  call     0x267e10  ; -> 00267E10 fn
00347D35  mov      rcx, rbx
00347D38  mov      edi, eax
00347D3A  call     0x267e10  ; -> 00267E10 fn
00347D3F  mov      ecx, eax
00347D41  call     0x263770  ; -> 00263770 fn
00347D46  test     rax, rax
00347D49  je       0x347d55  ; -> 00347D55
00347D4B  mov      edx, edi
00347D4D  mov      rcx, rax
00347D50  call     0x2ebc70  ; -> 002EBC70 fn
00347D55  mov      rbx, qword ptr [rsp + 0x30]
00347D5A  add      rsp, 0x20
00347D5E  pop      rdi
00347D5F  ret      
```

## 0034A340 (41 B, extent 0034A340-0034A369)

Documented callee on this page: `002E3580`

```
0034A340  push     rbx
0034A342  sub      rsp, 0x20
0034A346  mov      rcx, rdx
0034A349  mov      rbx, rdx
0034A34C  call     0x2e3580  ; -> 002E3580 fn
0034A351  mov      rcx, rbx
0034A354  call     0x265950  ; -> 00265950 fn
0034A359  movaps   xmm1, xmm0
0034A35C  mov      rcx, rbx
0034A35F  add      rsp, 0x20
0034A363  pop      rbx
0034A364  jmp      0x25b470  ; -> 0025B470 fn
```

## 0034F210 (111 B, extent 0034F210-0034F27F)

Documented callee on this page: `0025D540`

```
0034F210  mov      qword ptr [rsp + 8], rbx
0034F215  push     rdi
0034F216  sub      rsp, 0x40
0034F21A  movaps   xmmword ptr [rsp + 0x30], xmm6
0034F21F  mov      rcx, r9
0034F222  movaps   xmmword ptr [rsp + 0x20], xmm7
0034F227  mov      rbx, r9
0034F22A  mov      rdi, rdx
0034F22D  call     0x267db0  ; -> 00267DB0 fn
0034F232  mov      rcx, rbx
0034F235  movaps   xmm7, xmm0
0034F238  call     0x267db0  ; -> 00267DB0 fn
0034F23D  mov      rcx, rbx
0034F240  movaps   xmm6, xmm0
0034F243  call     0x267db0  ; -> 00267DB0 fn
0034F248  movaps   xmm3, xmm7
0034F24B  movaps   xmm2, xmm6
0034F24E  movaps   xmm1, xmm0
0034F251  mov      rcx, rdi
0034F254  call     0x26b0c0  ; -> 0026B0C0 fn
0034F259  mov      rcx, rdi
0034F25C  call     0x25d540  ; -> 0025D540 fn
0034F261  xor      edx, edx
0034F263  mov      rcx, rdi
0034F266  mov      rbx, qword ptr [rsp + 0x50]
0034F26B  movaps   xmm6, xmmword ptr [rsp + 0x30]
0034F270  movaps   xmm7, xmmword ptr [rsp + 0x20]
0034F275  add      rsp, 0x40
0034F279  pop      rdi
0034F27A  jmp      0x26ae90  ; -> 0026AE90 fn
```

## 00350C30 (147 B, extent 00350C30-00350CC3)

Documented callee on this page: `0025D540`

```
00350C30  mov      qword ptr [rsp + 8], rbx
00350C35  push     rdi
00350C36  sub      rsp, 0x50
00350C3A  movaps   xmmword ptr [rsp + 0x40], xmm6
00350C3F  mov      rcx, r9
00350C42  movaps   xmmword ptr [rsp + 0x30], xmm7
00350C47  mov      rbx, r9
00350C4A  movaps   xmmword ptr [rsp + 0x20], xmm8
00350C50  mov      rdi, rdx
00350C53  call     0x267db0  ; -> 00267DB0 fn
00350C58  mov      rcx, rbx
00350C5B  movaps   xmm8, xmm0
00350C5F  call     0x267db0  ; -> 00267DB0 fn
00350C64  mov      rcx, rbx
00350C67  movaps   xmm7, xmm0
00350C6A  call     0x267db0  ; -> 00267DB0 fn
00350C6F  mov      rcx, rbx
00350C72  movaps   xmm6, xmm0
00350C75  call     0x267db0  ; -> 00267DB0 fn
00350C7A  movaps   xmm3, xmm7
00350C7D  movaps   xmm2, xmm6
00350C80  movaps   xmm1, xmm0
00350C83  mov      rcx, rdi
00350C86  call     0x26b0c0  ; -> 0026B0C0 fn
00350C8B  movaps   xmm1, xmm8
00350C8F  mov      rcx, rdi
00350C92  call     0x26b620  ; -> 0026B620 fn
00350C97  mov      rcx, rdi
00350C9A  call     0x25d540  ; -> 0025D540 fn
00350C9F  xor      edx, edx
00350CA1  mov      rcx, rdi
00350CA4  mov      rbx, qword ptr [rsp + 0x60]
00350CA9  movaps   xmm6, xmmword ptr [rsp + 0x40]
00350CAE  movaps   xmm7, xmmword ptr [rsp + 0x30]
00350CB3  movaps   xmm8, xmmword ptr [rsp + 0x20]
00350CB9  add      rsp, 0x50
00350CBD  pop      rdi
00350CBE  jmp      0x26ae90  ; -> 0026AE90 fn
```

## 00379240 (36 B, extent 00379240-00379264)

Documented callee on this page: `0026E850`

```
00379240  add      ecx, 0x40
00379243  test     edx, edx
00379245  js       0x379256  ; -> 00379256
00379247  mov      r9d, 5
0037924D  lea      r8d, [r9 + 0xd]
00379251  jmp      0x26e880  ; -> 0026E880 fn
00379256  mov      edx, 0x12
0037925B  lea      r8d, [rdx - 0xd]
0037925F  jmp      0x26e850  ; -> 0026E850 fn
```

## 00379270 (24 B, extent 00379270-00379288)

Documented callee on this page: `0026E130`

```
00379270  test     ecx, ecx
00379272  jns      0x379280  ; -> 00379280
00379274  mov      edx, 0x20
00379279  mov      ecx, edx
0037927B  jmp      0x26e150  ; -> 0026E150 fn
00379280  add      ecx, 0x20
00379283  jmp      0x26e130  ; -> 0026E130 fn
```

## 003DE4C0 (294 B, extent 003DE4C0-003DE5E6)

Documented callee on this page: `0025AB30`

```
003DE4C0  mov      qword ptr [rsp + 8], rbx
003DE4C5  mov      qword ptr [rsp + 0x10], rbp
003DE4CA  mov      qword ptr [rsp + 0x18], rsi
003DE4CF  push     rdi
003DE4D0  push     r14
003DE4D2  push     r15
003DE4D4  sub      rsp, 0x20
003DE4D8  movsxd   rbp, ecx
003DE4DB  lea      r15, [rip + 0x277a76e]  ; -> 02B58C50
003DE4E2  mov      rcx, rdx
003DE4E5  mov      ebx, r8d
003DE4E8  imul     rdi, rbp, 0x70
003DE4EC  mov      rsi, rdx
003DE4EF  call     0x25ab30  ; -> 0025AB30 fn
003DE4F4  sub      ebx, 1
003DE4F7  je       0x3de50c  ; -> 003DE50C
003DE4F9  cmp      ebx, 1
003DE4FC  je       0x3de505  ; -> 003DE505
003DE4FE  mov      eax, 1
003DE503  jmp      0x3de511  ; -> 003DE511
003DE505  mov      eax, 4
003DE50A  jmp      0x3de511  ; -> 003DE511
003DE50C  mov      eax, 2
003DE511  mov      byte ptr [rdi + r15 + 0x20], al
003DE516  mov      ecx, dword ptr [rdi + r15]
003DE51A  movzx    ebx, byte ptr [rsi + 0x15]
003DE51E  test     ecx, ecx
003DE520  je       0x3de527  ; -> 003DE527
003DE522  call     0x3abca0  ; -> 003ABCA0 fn
003DE527  xor      r14d, r14d
003DE52A  lea      rcx, [r15 + 0x20]
003DE52E  add      rcx, rdi
003DE531  mov      dword ptr [rdi + r15], r14d
003DE535  mov      qword ptr [rdi + r15 + 8], r14
003DE53A  mov      qword ptr [rdi + r15 + 0x10], r14
003DE53F  mov      byte ptr [rdi + r15 + 5], r14b
003DE544  call     0x3ab960  ; -> 003AB960 fn
003DE549  mov      byte ptr [rdi + r15 + 4], bl
003DE54E  lea      r8d, [r14 + 0x50]
003DE552  lea      rbx, [rdi + r15]
003DE556  mov      dword ptr [rdi + r15], eax
003DE55A  lea      rcx, [rbx + 0x20]
003DE55E  xor      edx, edx
003DE560  call     0x861ec0  ; -> 00861EC0 fn
003DE565  or       byte ptr [rbx + 0x25], 1
003DE569  mov      dword ptr [rbx + 0x20], 0x100c002
003DE570  mov      byte ptr [rbx + 0x24], 1
003DE574  mov      dword ptr [rbx + 0x2c], 0x41200000
003DE57B  mov      byte ptr [rbx + 0x26], r14b
003DE57F  mov      dword ptr [rbx + 0x30], 0x3f800000
003DE586  mov      dword ptr [rbx + 0x34], 0x3f800000
003DE58D  mov      qword ptr [rbx + 0x38], 0x3f800000
003DE595  mov      qword ptr [rbx + 0x40], r14
003DE599  mov      dword ptr [rbx + 0x48], r14d
003DE59D  mov      dword ptr [rbx + 0x4c], 0x3f800000
003DE5A4  mov      dword ptr [rbx + 0x50], 0x3f800000
003DE5AB  mov      dword ptr [rbx + 0x54], 0x3f800000
003DE5B2  mov      dword ptr [rbx + 0x58], 0x3f800000
003DE5B9  mov      dword ptr [rbx + 0x5c], 0x3f800000
003DE5C0  mov      rbx, qword ptr [rsp + 0x40]
003DE5C5  mov      qword ptr [rdi + r15 + 8], rsi
003DE5CA  mov      byte ptr [rsi + 5], bpl
003DE5CE  mov      rbp, qword ptr [rsp + 0x48]
003DE5D3  mov      byte ptr [rsi + 4], 2
003DE5D7  mov      rsi, qword ptr [rsp + 0x50]
003DE5DC  add      rsp, 0x20
003DE5E0  pop      r15
003DE5E2  pop      r14
003DE5E4  pop      rdi
003DE5E5  ret      
```
