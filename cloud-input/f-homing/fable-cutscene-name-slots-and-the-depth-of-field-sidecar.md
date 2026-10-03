# F homing pack (FABLE): `99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md`

Generated 2026-10-03 04:02 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 16. No bearing page cites them and no documented function calls them directly.

## 001B5610 (308 B, extent 001B5610-001B5744)

Documented callee on this page: `001B31E0`

```
001B5610  mov      rax, rsp
001B5613  mov      qword ptr [rax + 0x10], rdx
001B5617  push     rsi
001B5618  push     rdi
001B5619  push     r14
001B561B  sub      rsp, 0x50
001B561F  mov      qword ptr [rax - 0x48], 0xfffffffffffffffe
001B5627  mov      qword ptr [rax + 8], rbx
001B562B  mov      qword ptr [rax + 0x18], rbp
001B562F  mov      rsi, rdx
001B5632  add      rcx, 0xd0
001B5639  call     0x1ba860  ; -> 001BA860 fn
001B563E  mov      rbp, rax
001B5641  lea      r14, [rax + 0x20]
001B5645  xor      ebx, ebx
001B5647  mov      qword ptr [r14], rbx
001B564A  cmp      rsi, rax
001B564D  je       0x1b565e  ; -> 001B565E
001B564F  mov      r8, qword ptr [rsi + 8]
001B5653  mov      rdx, qword ptr [rsi]
001B5656  mov      rcx, rax
001B5659  call     0x1a5760  ; -> 001A5760 fn
001B565E  lea      rdi, [rbp + 0x28]
001B5662  mov      qword ptr [rdi], rbx
001B5665  call     0x1a1220  ; -> 001A1220 fn
001B566A  mov      rcx, rax
001B566D  call     0x1a0a90  ; -> 001A0A90 fn
001B5672  mov      rbx, rax
001B5675  mov      dword ptr [rax], 4
001B567B  lea      rax, [rip + 0x95e]  ; -> 001B5FE0
001B5682  mov      qword ptr [rbx + 8], rax
001B5686  mov      qword ptr [rbx + 0x10], rbp
001B568A  mov      byte ptr [rbx + 0x18], 0
001B568E  mov      r8, qword ptr [rip + 0x1c41773]  ; -> 01DF6E08 [u64 0x00000000008F81F4]
001B5695  mov      rdx, rsi
001B5698  lea      rcx, [rsp + 0x28]
001B569D  call     0x1b31e0  ; -> 001B31E0 fn
001B56A2  nop      
001B56A3  lea      rcx, [rbx + 0x20]
001B56A7  mov      r8, qword ptr [rsp + 0x28]
001B56AC  mov      edx, 0x100
001B56B1  call     qword ptr [rip + 0x70d981]  ; -> 008C3038 [u64 0x0000000001CCEF0A]
001B56B7  mov      qword ptr [rbx + 0x120], r14
001B56BE  mov      qword ptr [rbx + 0x128], rdi
001B56C5  call     0x1a1220  ; -> 001A1220 fn
001B56CA  mov      rcx, rax
001B56CD  xor      r8d, r8d
001B56D0  mov      rdx, rbx
001B56D3  call     0x1a0bb0  ; -> 001A0BB0 fn
001B56D8  nop      
001B56D9  mov      rcx, qword ptr [rsp + 0x38]
001B56DE  mov      rax, rcx
001B56E1  mov      rdx, qword ptr [rsp + 0x28]
001B56E6  sub      rax, rdx
001B56E9  cmp      rax, 1
001B56ED  jle      0x1b5707  ; -> 001B5707
001B56EF  sub      ecx, edx
001B56F1  test     rdx, rdx
001B56F4  je       0x1b5707  ; -> 001B5707
001B56F6  mov      r8d, ecx
001B56F9  lea      rcx, [rsp + 0x40]
001B56FE  mov      rax, qword ptr [rsp + 0x40]
001B5703  call     qword ptr [rax + 0x18]
001B5706  nop      
001B5707  mov      rdx, qword ptr [rsi]
001B570A  mov      rax, qword ptr [rsi + 0x10]
001B570E  sub      rax, rdx
001B5711  cmp      rax, 1
001B5715  jle      0x1b572e  ; -> 001B572E
001B5717  mov      r8d, dword ptr [rsi + 0x10]
001B571B  sub      r8d, edx
001B571E  test     rdx, rdx
001B5721  je       0x1b572e  ; -> 001B572E
001B5723  lea      rcx, [rsi + 0x18]
001B5727  mov      rax, qword ptr [rcx]
001B572A  call     qword ptr [rax + 0x18]
001B572D  nop      
001B572E  mov      rbx, qword ptr [rsp + 0x70]
001B5733  mov      rbp, qword ptr [rsp + 0x80]
001B573B  add      rsp, 0x50
001B573F  pop      r14
001B5741  pop      rdi
001B5742  pop      rsi
001B5743  ret      
```

## 0033FFC0 (48 B, extent 0033FFC0-0033FFF0)

Documented callee on this page: `002EB430`

```
0033FFC0  push     rbx
0033FFC2  sub      rsp, 0x20
0033FFC6  mov      rbx, rdx
0033FFC9  call     0x357a20  ; -> 00357A20 fn
0033FFCE  mov      rcx, rbx
0033FFD1  call     0x263f40  ; -> 00263F40 fn
0033FFD6  mov      rcx, rax
0033FFD9  call     0x2eb430  ; -> 002EB430 fn
0033FFDE  mov      edx, 2
0033FFE3  mov      rcx, rbx
0033FFE6  add      rsp, 0x20
0033FFEA  pop      rbx
0033FFEB  jmp      0x26c120  ; -> 0026C120 fn
```

## 00348580 (129 B, extent 00348580-00348601)

Documented callee on this page: `003EB720`

```
00348580  push     rbx
00348582  sub      rsp, 0x40
00348586  movaps   xmmword ptr [rsp + 0x30], xmm6
0034858B  mov      rcx, r9
0034858E  movaps   xmmword ptr [rsp + 0x20], xmm7
00348593  mov      rbx, r9
00348596  call     0x267db0  ; -> 00267DB0 fn
0034859B  mov      rcx, rbx
0034859E  movaps   xmm6, xmm0
003485A1  call     0x267db0  ; -> 00267DB0 fn
003485A6  mov      rcx, rbx
003485A9  movaps   xmm7, xmm0
003485AC  call     0x267e10  ; -> 00267E10 fn
003485B1  mov      ecx, eax
003485B3  mov      ebx, eax
003485B5  call     0x16d6a0  ; -> 0016D6A0 fn
003485BA  mov      ecx, ebx
003485BC  call     0x3eb720  ; -> 003EB720 fn
003485C1  mov      rbx, rax
003485C4  test     rax, rax
003485C7  je       0x3485f1  ; -> 003485F1
003485C9  xorps    xmm1, xmm1
003485CC  comiss   xmm6, xmm1
003485CF  jb       0x3485db  ; -> 003485DB
003485D1  movaps   xmm0, xmm7
003485D4  maxss    xmm0, xmm6
003485D8  movaps   xmm6, xmm0
003485DB  movaps   xmm1, xmm7
003485DE  mov      rcx, rbx
003485E1  call     0x2ec9c0  ; -> 002EC9C0 fn
003485E6  movaps   xmm1, xmm6
003485E9  mov      rcx, rbx
003485EC  call     0x2ec900  ; -> 002EC900 fn
003485F1  movaps   xmm6, xmmword ptr [rsp + 0x30]
003485F6  movaps   xmm7, xmmword ptr [rsp + 0x20]
003485FB  add      rsp, 0x40
003485FF  pop      rbx
00348600  ret      
```

## 00348A90 (80 B, extent 00348A90-00348AE0)

Documented callee on this page: `003EB720`

```
00348A90  push     rbx
00348A92  sub      rsp, 0x30
00348A96  mov      rcx, r9
00348A99  movaps   xmmword ptr [rsp + 0x20], xmm6
00348A9E  mov      rbx, r9
00348AA1  call     0x267db0  ; -> 00267DB0 fn
00348AA6  mov      rcx, rbx
00348AA9  movaps   xmm6, xmm0
00348AAC  call     0x267e10  ; -> 00267E10 fn
00348AB1  mov      ecx, eax
00348AB3  mov      ebx, eax
00348AB5  call     0x16d6a0  ; -> 0016D6A0 fn
00348ABA  mov      ecx, ebx
00348ABC  call     0x3eb720  ; -> 003EB720 fn
00348AC1  test     rax, rax
00348AC4  je       0x348ad5  ; -> 00348AD5
00348AC6  xorps    xmm1, xmm1
00348AC9  mov      rcx, rax
00348ACC  maxss    xmm1, xmm6
00348AD0  call     0x2eccb0  ; -> 002ECCB0 fn
00348AD5  movaps   xmm6, xmmword ptr [rsp + 0x20]
00348ADA  add      rsp, 0x30
00348ADE  pop      rbx
00348ADF  ret      
```

## 003490F0 (85 B, extent 003490F0-00349145)

Documented callee on this page: `003EB720`

```
003490F0  push     rbx
003490F2  sub      rsp, 0x30
003490F6  mov      rcx, r9
003490F9  movaps   xmmword ptr [rsp + 0x20], xmm6
003490FE  mov      rbx, r9
00349101  call     0x267db0  ; -> 00267DB0 fn
00349106  mov      rcx, rbx
00349109  movaps   xmm6, xmm0
0034910C  call     0x267e10  ; -> 00267E10 fn
00349111  mov      ecx, eax
00349113  mov      ebx, eax
00349115  call     0x16d6a0  ; -> 0016D6A0 fn
0034911A  mov      ecx, ebx
0034911C  call     0x3eb720  ; -> 003EB720 fn
00349121  mov      rcx, rax
00349124  mov      rbx, rax
00349127  call     0x2e95b0  ; -> 002E95B0 fn
0034912C  mulss    xmm6, xmm0
00349130  mov      rcx, rbx
00349133  movaps   xmm1, xmm6
00349136  movaps   xmm6, xmmword ptr [rsp + 0x20]
0034913B  add      rsp, 0x30
0034913F  pop      rbx
00349140  jmp      0x2e4fe0  ; -> 002E4FE0 fn
```

## 00349460 (43 B, extent 00349460-0034948B)

Documented callee on this page: `003EB720`

```
00349460  push     rbx
00349462  sub      rsp, 0x20
00349466  mov      rcx, r9
00349469  call     0x267e10  ; -> 00267E10 fn
0034946E  mov      ecx, eax
00349470  mov      ebx, eax
00349472  call     0x16d6a0  ; -> 0016D6A0 fn
00349477  mov      ecx, ebx
00349479  call     0x3eb720  ; -> 003EB720 fn
0034947E  mov      rcx, rax
00349481  add      rsp, 0x20
00349485  pop      rbx
00349486  jmp      0x2e4330  ; -> 002E4330 fn
```

## 003498D0 (54 B, extent 003498D0-00349906)

Documented callee on this page: `003EB720`

```
003498D0  push     rbx
003498D2  sub      rsp, 0x20
003498D6  mov      rcx, r9
003498D9  call     0x267e10  ; -> 00267E10 fn
003498DE  mov      ecx, eax
003498E0  mov      ebx, eax
003498E2  call     0x16d6a0  ; -> 0016D6A0 fn
003498E7  mov      ecx, ebx
003498E9  call     0x3eb720  ; -> 003EB720 fn
003498EE  mov      rcx, rax
003498F1  mov      rbx, rax
003498F4  call     0x2e4330  ; -> 002E4330 fn
003498F9  mov      rcx, rbx
003498FC  add      rsp, 0x20
00349900  pop      rbx
00349901  jmp      0x2ec630  ; -> 002EC630 fn
```

## 0034A290 (48 B, extent 0034A290-0034A2C0)

Documented callee on this page: `002EB430`

```
0034A290  push     rbx
0034A292  sub      rsp, 0x20
0034A296  mov      rbx, rdx
0034A299  call     0x357980  ; -> 00357980 fn
0034A29E  mov      rcx, rbx
0034A2A1  call     0x263f40  ; -> 00263F40 fn
0034A2A6  mov      rcx, rax
0034A2A9  call     0x2eb430  ; -> 002EB430 fn
0034A2AE  mov      edx, 2
0034A2B3  mov      rcx, rbx
0034A2B6  add      rsp, 0x20
0034A2BA  pop      rbx
0034A2BB  jmp      0x26c120  ; -> 0026C120 fn
```

## 0034B0A0 (67 B, extent 0034B0A0-0034B0E3)

Documented callee on this page: `003EB720`

```
0034B0A0  mov      qword ptr [rsp + 8], rbx
0034B0A5  push     rdi
0034B0A6  sub      rsp, 0x20
0034B0AA  mov      rcx, r9
0034B0AD  mov      rbx, r9
0034B0B0  call     0x267e10  ; -> 00267E10 fn
0034B0B5  mov      rcx, rbx
0034B0B8  mov      edi, eax
0034B0BA  call     0x267e10  ; -> 00267E10 fn
0034B0BF  mov      ecx, eax
0034B0C1  mov      ebx, eax
0034B0C3  call     0x16d6a0  ; -> 0016D6A0 fn
0034B0C8  mov      ecx, ebx
0034B0CA  call     0x3eb720  ; -> 003EB720 fn
0034B0CF  mov      edx, edi
0034B0D1  mov      rcx, rax
0034B0D4  mov      rbx, qword ptr [rsp + 0x30]
0034B0D9  add      rsp, 0x20
0034B0DD  pop      rdi
0034B0DE  jmp      0x2ed3f0  ; -> 002ED3F0 fn
```

## 0034B710 (80 B, extent 0034B710-0034B760)

Documented callee on this page: `003EB720`

```
0034B710  mov      qword ptr [rsp + 8], rbx
0034B715  push     rdi
0034B716  sub      rsp, 0x20
0034B71A  mov      edx, 1
0034B71F  mov      rcx, r9
0034B722  mov      rbx, r9
0034B725  call     0x267f90  ; -> 00267F90 fn
0034B72A  mov      rcx, rbx
0034B72D  call     0x267e10  ; -> 00267E10 fn
0034B732  mov      rcx, rbx
0034B735  mov      edi, eax
0034B737  call     0x267e10  ; -> 00267E10 fn
0034B73C  mov      ecx, eax
0034B73E  mov      ebx, eax
0034B740  call     0x16d6a0  ; -> 0016D6A0 fn
0034B745  mov      ecx, ebx
0034B747  call     0x3eb720  ; -> 003EB720 fn
0034B74C  mov      edx, edi
0034B74E  mov      rcx, rax
0034B751  mov      rbx, qword ptr [rsp + 0x30]
0034B756  add      rsp, 0x20
0034B75A  pop      rdi
0034B75B  jmp      0x2ed3f0  ; -> 002ED3F0 fn
```

## 0034BAB0 (77 B, extent 0034BAB0-0034BAFD)

Documented callee on this page: `003EB720`

```
0034BAB0  mov      qword ptr [rsp + 8], rbx
0034BAB5  push     rdi
0034BAB6  sub      rsp, 0x20
0034BABA  xor      edx, edx
0034BABC  mov      rcx, r9
0034BABF  mov      rbx, r9
0034BAC2  call     0x267f90  ; -> 00267F90 fn
0034BAC7  mov      rcx, rbx
0034BACA  call     0x267e10  ; -> 00267E10 fn
0034BACF  mov      rcx, rbx
0034BAD2  mov      edi, eax
0034BAD4  call     0x267e10  ; -> 00267E10 fn
0034BAD9  mov      ecx, eax
0034BADB  mov      ebx, eax
0034BADD  call     0x16d6a0  ; -> 0016D6A0 fn
0034BAE2  mov      ecx, ebx
0034BAE4  call     0x3eb720  ; -> 003EB720 fn
0034BAE9  mov      edx, edi
0034BAEB  mov      rcx, rax
0034BAEE  mov      rbx, qword ptr [rsp + 0x30]
0034BAF3  add      rsp, 0x20
0034BAF7  pop      rdi
0034BAF8  jmp      0x2ed3f0  ; -> 002ED3F0 fn
```

## 0034BF40 (73 B, extent 0034BF40-0034BF89)

Documented callee on this page: `003EB720`

```
0034BF40  mov      qword ptr [rsp + 8], rbx
0034BF45  push     rdi
0034BF46  sub      rsp, 0x20
0034BF4A  mov      rcx, r9
0034BF4D  mov      rbx, r9
0034BF50  call     0x267e10  ; -> 00267E10 fn
0034BF55  mov      rcx, rbx
0034BF58  mov      edi, eax
0034BF5A  call     0x267e10  ; -> 00267E10 fn
0034BF5F  mov      ecx, eax
0034BF61  mov      ebx, eax
0034BF63  call     0x16d6a0  ; -> 0016D6A0 fn
0034BF68  mov      ecx, ebx
0034BF6A  call     0x3eb720  ; -> 003EB720 fn
0034BF6F  test     rax, rax
0034BF72  je       0x34bf7e  ; -> 0034BF7E
0034BF74  mov      edx, edi
0034BF76  mov      rcx, rax
0034BF79  call     0x2ec6a0  ; -> 002EC6A0 fn
0034BF7E  mov      rbx, qword ptr [rsp + 0x30]
0034BF83  add      rsp, 0x20
0034BF87  pop      rdi
0034BF88  ret      
```

## 0034C900 (73 B, extent 0034C900-0034C949)

Documented callee on this page: `003EB720`

```
0034C900  mov      qword ptr [rsp + 8], rbx
0034C905  push     rdi
0034C906  sub      rsp, 0x20
0034C90A  mov      rcx, r9
0034C90D  mov      rbx, r9
0034C910  call     0x267e10  ; -> 00267E10 fn
0034C915  mov      rcx, rbx
0034C918  mov      edi, eax
0034C91A  call     0x267e10  ; -> 00267E10 fn
0034C91F  mov      ecx, eax
0034C921  mov      ebx, eax
0034C923  call     0x16d6a0  ; -> 0016D6A0 fn
0034C928  mov      ecx, ebx
0034C92A  call     0x3eb720  ; -> 003EB720 fn
0034C92F  test     rax, rax
0034C932  je       0x34c93e  ; -> 0034C93E
0034C934  mov      edx, edi
0034C936  mov      rcx, rax
0034C939  call     0x2ec890  ; -> 002EC890 fn
0034C93E  mov      rbx, qword ptr [rsp + 0x30]
0034C943  add      rsp, 0x20
0034C947  pop      rdi
0034C948  ret      
```

## 0034CCF0 (67 B, extent 0034CCF0-0034CD33)

Documented callee on this page: `003EB720`

```
0034CCF0  mov      qword ptr [rsp + 8], rbx
0034CCF5  push     rdi
0034CCF6  sub      rsp, 0x20
0034CCFA  mov      rcx, r9
0034CCFD  mov      rbx, r9
0034CD00  call     0x267e10  ; -> 00267E10 fn
0034CD05  mov      rcx, rbx
0034CD08  mov      edi, eax
0034CD0A  call     0x267e10  ; -> 00267E10 fn
0034CD0F  mov      ecx, eax
0034CD11  mov      ebx, eax
0034CD13  call     0x16d6a0  ; -> 0016D6A0 fn
0034CD18  mov      ecx, ebx
0034CD1A  call     0x3eb720  ; -> 003EB720 fn
0034CD1F  mov      edx, edi
0034CD21  mov      rcx, rax
0034CD24  mov      rbx, qword ptr [rsp + 0x30]
0034CD29  add      rsp, 0x20
0034CD2D  pop      rdi
0034CD2E  jmp      0x2ed3a0  ; -> 002ED3A0 fn
```

## 0034D2B0 (80 B, extent 0034D2B0-0034D300)

Documented callee on this page: `003EB720`

```
0034D2B0  mov      qword ptr [rsp + 8], rbx
0034D2B5  push     rdi
0034D2B6  sub      rsp, 0x20
0034D2BA  mov      edx, 1
0034D2BF  mov      rcx, r9
0034D2C2  mov      rbx, r9
0034D2C5  call     0x267f90  ; -> 00267F90 fn
0034D2CA  mov      rcx, rbx
0034D2CD  call     0x267e10  ; -> 00267E10 fn
0034D2D2  mov      rcx, rbx
0034D2D5  mov      edi, eax
0034D2D7  call     0x267e10  ; -> 00267E10 fn
0034D2DC  mov      ecx, eax
0034D2DE  mov      ebx, eax
0034D2E0  call     0x16d6a0  ; -> 0016D6A0 fn
0034D2E5  mov      ecx, ebx
0034D2E7  call     0x3eb720  ; -> 003EB720 fn
0034D2EC  mov      edx, edi
0034D2EE  mov      rcx, rax
0034D2F1  mov      rbx, qword ptr [rsp + 0x30]
0034D2F6  add      rsp, 0x20
0034D2FA  pop      rdi
0034D2FB  jmp      0x2ed3a0  ; -> 002ED3A0 fn
```

## 0034D640 (77 B, extent 0034D640-0034D68D)

Documented callee on this page: `003EB720`

```
0034D640  mov      qword ptr [rsp + 8], rbx
0034D645  push     rdi
0034D646  sub      rsp, 0x20
0034D64A  xor      edx, edx
0034D64C  mov      rcx, r9
0034D64F  mov      rbx, r9
0034D652  call     0x267f90  ; -> 00267F90 fn
0034D657  mov      rcx, rbx
0034D65A  call     0x267e10  ; -> 00267E10 fn
0034D65F  mov      rcx, rbx
0034D662  mov      edi, eax
0034D664  call     0x267e10  ; -> 00267E10 fn
0034D669  mov      ecx, eax
0034D66B  mov      ebx, eax
0034D66D  call     0x16d6a0  ; -> 0016D6A0 fn
0034D672  mov      ecx, ebx
0034D674  call     0x3eb720  ; -> 003EB720 fn
0034D679  mov      edx, edi
0034D67B  mov      rcx, rax
0034D67E  mov      rbx, qword ptr [rsp + 0x30]
0034D683  add      rsp, 0x20
0034D687  pop      rdi
0034D688  jmp      0x2ed3a0  ; -> 002ED3A0 fn
```
