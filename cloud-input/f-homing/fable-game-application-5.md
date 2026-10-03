# F homing pack (FABLE): `00-Engine-Core-Runtime/Application-Root/game-application.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 20. No bearing page cites them and no documented function calls them directly.

## 002D79D0 (178 B, extent 002D79D0-002D7A82)

Documented callee on this page: `00808C40`

```
002D79D0  push     rbx
002D79D2  sub      rsp, 0x40
002D79D6  mov      rax, qword ptr [rip + 0x1c6ce53]  ; -> 01F44830 [u64 0x00002B992DDFA232]
002D79DD  xor      rax, rsp
002D79E0  mov      qword ptr [rsp + 0x38], rax
002D79E5  mov      ebx, ecx
002D79E7  mov      rcx, qword ptr [rip + 0x1dc3242]  ; -> 0209AC30
002D79EE  mov      rax, qword ptr [rcx + 0xd8]
002D79F5  test     rax, rax
002D79F8  jne      0x2d7a06  ; -> 002D7A06
002D79FA  mov      rax, qword ptr [rcx + 0x100]
002D7A01  test     rax, rax
002D7A04  je       0x2d7a20  ; -> 002D7A20
002D7A06  mov      dword ptr [rax + 0xcc], 2
002D7A10  mov      dword ptr [rax + 0xc4], 4
002D7A1A  mov      dword ptr [rax + 0xc8], ebx
002D7A20  xor      ecx, ecx
002D7A22  call     0x561260  ; -> 00561260 fn
002D7A27  test     ebx, ebx
002D7A29  je       0x2d7a6f  ; -> 002D7A6F
002D7A2B  mov      rax, qword ptr [rip + 0x1dc31fe]  ; -> 0209AC30
002D7A32  mov      rcx, qword ptr [rax + 0xd8]
002D7A39  test     rcx, rcx
002D7A3C  jne      0x2d7a4a  ; -> 002D7A4A
002D7A3E  mov      rcx, qword ptr [rax + 0x100]
002D7A45  test     rcx, rcx
002D7A48  je       0x2d7a6f  ; -> 002D7A6F
002D7A4A  mov      rax, qword ptr [rcx]
002D7A4D  movdqa   xmm0, xmmword ptr [rip + 0x63f7bb]  ; -> 00917210 [u32x4 0x00000001, 0x00000000, 0x00000002, 0x00000000]
002D7A55  mov      dword ptr [rsp + 0x20], 0x120
002D7A5D  movdqu   xmmword ptr [rsp + 0x28], xmm0
002D7A63  test     rax, rax
002D7A66  je       0x2d7a6f  ; -> 002D7A6F
002D7A68  lea      rdx, [rsp + 0x20]
002D7A6D  call     rax
002D7A6F  mov      rcx, qword ptr [rsp + 0x38]
002D7A74  xor      rcx, rsp
002D7A77  call     0x808c40  ; -> 00808C40 fn
002D7A7C  add      rsp, 0x40
002D7A80  pop      rbx
002D7A81  ret      
```

## 002D7BF0 (183 B, extent 002D7BF0-002D7CA7)

Documented callee on this page: `00808C40`

```
002D7BF0  push     rbx
002D7BF2  sub      rsp, 0x40
002D7BF6  mov      rax, qword ptr [rip + 0x1c6cc33]  ; -> 01F44830 [u64 0x00002B992DDFA232]
002D7BFD  xor      rax, rsp
002D7C00  mov      qword ptr [rsp + 0x38], rax
002D7C05  mov      ebx, r8d
002D7C08  mov      r8d, ecx
002D7C0B  mov      rcx, qword ptr [rip + 0x1dc301e]  ; -> 0209AC30
002D7C12  mov      rax, qword ptr [rcx + 0xd8]
002D7C19  test     rax, rax
002D7C1C  jne      0x2d7c2a  ; -> 002D7C2A
002D7C1E  mov      rax, qword ptr [rcx + 0x100]
002D7C25  test     rax, rax
002D7C28  je       0x2d7c44  ; -> 002D7C44
002D7C2A  mov      dword ptr [rax + 0xcc], 3
002D7C34  mov      dword ptr [rax + 0xc4], 8
002D7C3E  mov      dword ptr [rax + 0xc8], ebx
002D7C44  mov      ecx, r8d
002D7C47  call     0x561280  ; -> 00561280 fn
002D7C4C  test     ebx, ebx
002D7C4E  je       0x2d7c94  ; -> 002D7C94
002D7C50  mov      rax, qword ptr [rip + 0x1dc2fd9]  ; -> 0209AC30
002D7C57  mov      rcx, qword ptr [rax + 0xd8]
002D7C5E  test     rcx, rcx
002D7C61  jne      0x2d7c6f  ; -> 002D7C6F
002D7C63  mov      rcx, qword ptr [rax + 0x100]
002D7C6A  test     rcx, rcx
002D7C6D  je       0x2d7c94  ; -> 002D7C94
002D7C6F  mov      rax, qword ptr [rcx]
002D7C72  movdqa   xmm0, xmmword ptr [rip + 0x63f5a6]  ; -> 00917220 [u32x4 0x00000001, 0x00000000, 0x00000003, 0x00000000]
002D7C7A  mov      dword ptr [rsp + 0x20], 0x120
002D7C82  movdqu   xmmword ptr [rsp + 0x28], xmm0
002D7C88  test     rax, rax
002D7C8B  je       0x2d7c94  ; -> 002D7C94
002D7C8D  lea      rdx, [rsp + 0x20]
002D7C92  call     rax
002D7C94  mov      rcx, qword ptr [rsp + 0x38]
002D7C99  xor      rcx, rsp
002D7C9C  call     0x808c40  ; -> 00808C40 fn
002D7CA1  add      rsp, 0x40
002D7CA5  pop      rbx
002D7CA6  ret      
```

## 002E2310 (12 B, extent 002E2310-002E231C)

Documented callee on this page: `0016D6A0`

```
002E2310  mov      edx, ecx
002E2312  mov      ecx, 1
002E2317  jmp      0x16d6a0  ; -> 0016D6A0 fn
```

## 00342D80 (70 B, extent 00342D80-00342DC6)

Documented callee on this page: `005C5230`

```
00342D80  mov      qword ptr [rsp + 8], rbx
00342D85  push     rdi
00342D86  sub      rsp, 0x20
00342D8A  mov      rcx, r9
00342D8D  mov      rbx, rdx
00342D90  call     0x267e10  ; -> 00267E10 fn
00342D95  movzx    ecx, byte ptr [rbx + 0x15]
00342D99  mov      edx, eax
00342D9B  mov      edi, eax
00342D9D  call     0x5c5230  ; -> 005C5230 fn
00342DA2  test     eax, eax
00342DA4  je       0x342dab  ; -> 00342DAB
00342DA6  call     0x16d6a0  ; -> 0016D6A0 fn
00342DAB  movzx    ecx, byte ptr [rbx + 0x15]
00342DAF  mov      r8d, 1
00342DB5  mov      edx, edi
00342DB7  mov      rbx, qword ptr [rsp + 0x30]
00342DBC  add      rsp, 0x20
00342DC0  pop      rdi
00342DC1  jmp      0x26b790  ; -> 0026B790 fn
```

## 00379D60 (198 B, extent 00379D60-00379E26)

Documented callee on this page: `00861EC0`

```
00379D60  mov      qword ptr [rsp + 8], rbx
00379D65  mov      qword ptr [rsp + 0x10], rbp
00379D6A  mov      qword ptr [rsp + 0x18], rsi
00379D6F  push     rdi
00379D70  sub      rsp, 0x20
00379D74  xor      esi, esi
00379D76  lea      rbp, [rip + 0x27633f3]  ; -> 02ADD170
00379D7D  mov      qword ptr [rip + 0x2763af4], rsi  ; -> 02ADD878
00379D84  mov      rbx, rbp
00379D87  mov      qword ptr [rip + 0x2763ae2], rsi  ; -> 02ADD870
00379D8E  mov      edi, esi
00379D90  xor      edx, edx
00379D92  mov      rcx, rbx
00379D95  lea      r8d, [rdx + 0x70]
00379D99  call     0x861ec0  ; -> 00861EC0 fn
00379D9E  lea      eax, [rdi + 0x10]
00379DA1  inc      edi
00379DA3  mov      dword ptr [rbx + 0x28], eax
00379DA6  add      rbx, 0x70
00379DAA  cmp      edi, 0x10
00379DAD  jl       0x379d90  ; -> 00379D90
00379DAF  lea      rax, [rbp - 0x70]
00379DB3  mov      r8d, 0xe
00379DB9  nop      dword ptr [rax]
00379DC0  lea      rcx, [rax + 0xe0]
00379DC7  mov      qword ptr [rax + 0x78], rax
00379DCB  mov      qword ptr [rax + 0x70], rcx
00379DCF  add      rax, 0x70
00379DD3  sub      r8, 1
00379DD7  jne      0x379dc0  ; -> 00379DC0
00379DD9  mov      rbx, qword ptr [rsp + 0x30]
00379DDE  lea      rax, [rip + 0x27633fb]  ; -> 02ADD1E0
00379DE5  mov      qword ptr [rip + 0x2763384], rax  ; -> 02ADD170
00379DEC  lea      rax, [rip + 0x276399d]  ; -> 02ADD790
00379DF3  mov      qword ptr [rip + 0x276337e], rsi  ; -> 02ADD178
00379DFA  mov      qword ptr [rip + 0x27639ff], rsi  ; -> 02ADD800
00379E01  mov      qword ptr [rip + 0x2763a78], rbp  ; -> 02ADD880
00379E08  mov      rbp, qword ptr [rsp + 0x38]
00379E0D  mov      qword ptr [rip + 0x2763a74], rsi  ; -> 02ADD888
00379E14  mov      rsi, qword ptr [rsp + 0x40]
00379E19  mov      qword ptr [rip + 0x27639e8], rax  ; -> 02ADD808
00379E20  add      rsp, 0x20
00379E24  pop      rdi
00379E25  ret      
```

## 003B6C70 (78 B, extent 003B6C70-003B6CBE)

Documented callee on this page: `00808C40`

```
003B6C70  sub      rsp, 0x48
003B6C74  mov      rax, qword ptr [rip + 0x1b8dbb5]  ; -> 01F44830 [u64 0x00002B992DDFA232]
003B6C7B  xor      rax, rsp
003B6C7E  mov      qword ptr [rsp + 0x30], rax
003B6C83  call     0x259b00  ; -> 00259B00 fn
003B6C88  test     eax, eax
003B6C8A  je       0x3b6cac  ; -> 003B6CAC
003B6C8C  lea      rcx, [rsp + 0x20]
003B6C91  mov      qword ptr [rsp + 0x20], 0x80
003B6C9A  mov      dword ptr [rsp + 0x28], 0xff
003B6CA2  mov      byte ptr [rsp + 0x2f], 0
003B6CA7  call     0x3ed170  ; -> 003ED170 fn
003B6CAC  mov      rcx, qword ptr [rsp + 0x30]
003B6CB1  xor      rcx, rsp
003B6CB4  call     0x808c40  ; -> 00808C40 fn
003B6CB9  add      rsp, 0x48
003B6CBD  ret      
```

## 003BBB30 (40 B, extent 003BBB30-003BBB58)

Documented callee on this page: `00861EC0`

```
003BBB30  sub      rsp, 0x28
003BBB34  call     0x28fb60  ; -> 0028FB60 fn
003BBB39  lea      rcx, [rip + 0x2788890]  ; -> 02B443D0
003BBB40  xor      edx, edx
003BBB42  mov      r8d, 0x1400
003BBB48  mov      qword ptr [rip + 0x2789c81], rcx  ; -> 02B457D0
003BBB4F  add      rsp, 0x28
003BBB53  jmp      0x861ec0  ; -> 00861EC0 fn
```

## 003C5030 (48 B, extent 003C5030-003C5060)

Documented callee on this page: `00861EC0`

```
003C5030  sub      rsp, 0x28
003C5034  xor      edx, edx
003C5036  lea      rcx, [rip + 0x2780813]  ; -> 02B45850
003C503D  mov      r8d, 0x120
003C5043  call     0x861ec0  ; -> 00861EC0 fn
003C5048  xor      edx, edx
003C504A  lea      rcx, [rip + 0x278122f]  ; -> 02B46280
003C5051  mov      r8d, 0x1430
003C5057  add      rsp, 0x28
003C505B  jmp      0x861ec0  ; -> 00861EC0 fn
```

## 003CB320 (162 B, extent 003CB320-003CB3C2)

Documented callee on this page: `00808C40`

```
003CB320  push     rbx
003CB322  sub      rsp, 0x60
003CB326  mov      rax, qword ptr [rip + 0x1b79503]  ; -> 01F44830 [u64 0x00002B992DDFA232]
003CB32D  xor      rax, rsp
003CB330  mov      qword ptr [rsp + 0x58], rax
003CB335  mov      rbx, rcx
003CB338  lea      rdx, [rsp + 0x20]
003CB33D  xor      ecx, ecx
003CB33F  call     0x3200a0  ; -> 003200A0 fn
003CB344  xor      r8d, r8d
003CB347  lea      r9, [rip + 0x94640a]  ; -> 00D11758
003CB34E  lea      rdx, [rbx + 0x108]
003CB355  test     rbx, rbx
003CB358  jne      0x3cb35e  ; -> 003CB35E
003CB35A  xor      ecx, ecx
003CB35C  jmp      0x3cb369  ; -> 003CB369
003CB35E  movsxd   rcx, dword ptr [r9]
003CB361  mov      rax, qword ptr [rbx + 0x60]
003CB365  mov      rcx, qword ptr [rax + rcx*8]
003CB369  mov      eax, dword ptr [rdx]
003CB36B  inc      r8d
003CB36E  mov      qword ptr [rdx - 8], rcx
003CB372  cmp      dword ptr [rsp + 0x34], r8d
003CB377  jge      0x3cb37e  ; -> 003CB37E
003CB379  and      eax, 0xfffffffe
003CB37C  jmp      0x3cb381  ; -> 003CB381
003CB37E  or       eax, 1
003CB381  mov      dword ptr [rdx], eax
003CB383  add      r9, 4
003CB387  and      dword ptr [rcx + 8], 0xfffffffe
003CB38B  and      eax, 1
003CB38E  or       dword ptr [rcx + 8], eax
003CB391  add      rdx, 0x58
003CB395  cmp      r8d, 3
003CB399  jb       0x3cb355  ; -> 003CB355
003CB39B  mov      eax, dword ptr [rsp + 0x34]
003CB39F  mov      ecx, 3
003CB3A4  cmp      eax, ecx
003CB3A6  cmovae   eax, ecx
003CB3A9  mov      dword ptr [rbx + 0x1d0], eax
003CB3AF  mov      rcx, qword ptr [rsp + 0x58]
003CB3B4  xor      rcx, rsp
003CB3B7  call     0x808c40  ; -> 00808C40 fn
003CB3BC  add      rsp, 0x60
003CB3C0  pop      rbx
003CB3C1  ret      
```

## 003DE480 (57 B, extent 003DE480-003DE4B9)

Documented callee on this page: `0016D6A0`

```
003DE480  sub      rsp, 0x28
003DE484  mov      byte ptr [rip + 0x277a796], cl  ; -> 02B58C20
003DE48A  lea      rcx, [rip + 0x277a78f]  ; -> 02B58C20
003DE491  call     0x16d6a0  ; -> 0016D6A0 fn
003DE496  xor      eax, eax
003DE498  mov      qword ptr [rip + 0x277a781], rax  ; -> 02B58C20
003DE49F  mov      byte ptr [rip + 0x277a781], 0x80  ; -> 02B58C27
003DE4A6  mov      qword ptr [rip + 0x277a77b], rax  ; -> 02B58C28
003DE4AD  mov      qword ptr [rip + 0x277a77c], rax  ; -> 02B58C30
003DE4B4  add      rsp, 0x28
003DE4B8  ret      
```

## 003DE7E0 (187 B, extent 003DE7E0-003DE89B)

Documented callee on this page: `00861F08`

```
003DE7E0  mov      qword ptr [rsp + 8], rbx
003DE7E5  push     rdi
003DE7E6  sub      rsp, 0x20
003DE7EA  movsxd   rax, ecx
003DE7ED  mov      ebx, edx
003DE7EF  imul     rdi, rax, 0x70
003DE7F3  lea      rax, [rip + 0x277a456]  ; -> 02B58C50
003DE7FA  xor      edx, edx
003DE7FC  add      rdi, rax
003DE7FF  lea      r8d, [rdx + 0x50]
003DE803  lea      rcx, [rdi + 0x20]
003DE807  call     0x861ec0  ; -> 00861EC0 fn
003DE80C  or       byte ptr [rdi + 0x25], 1
003DE810  xor      eax, eax
003DE812  mov      byte ptr [rdi + 0x20], bl
003DE815  mov      dword ptr [rdi + 0x21], 0x10100c0
003DE81C  mov      dword ptr [rdi + 0x2c], 0x41200000
003DE823  mov      byte ptr [rdi + 0x26], 0
003DE827  mov      dword ptr [rdi + 0x30], 0x3f800000
003DE82E  mov      dword ptr [rdi + 0x34], 0x3f800000
003DE835  mov      qword ptr [rdi + 0x38], 0x3f800000
003DE83D  mov      qword ptr [rdi + 0x40], rax
003DE841  mov      dword ptr [rdi + 0x48], eax
003DE844  mov      dword ptr [rdi + 0x4c], 0x3f800000
003DE84B  mov      dword ptr [rdi + 0x50], 0x3f800000
003DE852  mov      dword ptr [rdi + 0x54], 0x3f800000
003DE859  mov      dword ptr [rdi + 0x58], 0x3f800000
003DE860  mov      dword ptr [rdi + 0x5c], 0x3f800000
003DE867  cmp      ebx, 4
003DE86A  jne      0x3de890  ; -> 003DE890
003DE86C  movss    xmm0, dword ptr [rip + 0x536d9c]  ; -> 00915610 [f32 0.3926991]
003DE874  call     0x861f08  ; -> 00861F08 fn
003DE879  movss    dword ptr [rdi + 0x60], xmm0
003DE87E  movss    xmm0, dword ptr [rip + 0x536d8e]  ; -> 00915614 [f32 0.7853982]
003DE886  call     0x861f08  ; -> 00861F08 fn
003DE88B  movss    dword ptr [rdi + 0x64], xmm0
003DE890  mov      rbx, qword ptr [rsp + 0x30]
003DE895  add      rsp, 0x20
003DE899  pop      rdi
003DE89A  ret      
```

## 00407300 (167 B, extent 00407300-004073A7)

Documented callee on this page: `0016D6A0`

```
00407300  mov      r10d, r8d
00407303  test     rcx, rcx
00407306  je       0x4073a6  ; -> 004073A6
0040730C  cmp      byte ptr [rcx + 0xc0], 1
00407313  jne      0x407320  ; -> 00407320
00407315  imul     edx, edx, 0x3c
00407318  imul     r10d, r10d, 0x3c
0040731C  imul     r9d, r9d, 0x3c
00407320  movzx    r8d, byte ptr [rcx + 0xdc]
00407328  sub      r8d, 1
0040732C  je       0x40736a  ; -> 0040736A
0040732E  sub      r8d, 1
00407332  je       0x407340  ; -> 00407340
00407334  sub      r8d, 1
00407338  je       0x40736a  ; -> 0040736A
0040733A  cmp      r8d, 1
0040733E  jne      0x407392  ; -> 00407392
00407340  cmp      r9d, -1
00407344  je       0x40734e  ; -> 0040734E
00407346  mov      word ptr [rcx + 0xea], r9w
0040734E  cmp      r10d, -1
00407352  je       0x40735c  ; -> 0040735C
00407354  mov      word ptr [rcx + 0xec], r10w
0040735C  cmp      edx, -1
0040735F  je       0x407392  ; -> 00407392
00407361  mov      word ptr [rcx + 0xee], dx
00407368  jmp      0x407392  ; -> 00407392
0040736A  cmp      edx, -1
0040736D  je       0x407376  ; -> 00407376
0040736F  mov      word ptr [rcx + 0xea], dx
00407376  cmp      r10d, -1
0040737A  je       0x407384  ; -> 00407384
0040737C  mov      word ptr [rcx + 0xec], r10w
00407384  cmp      r9d, -1
00407388  je       0x407392  ; -> 00407392
0040738A  mov      word ptr [rcx + 0xee], r9w
00407392  mov      rcx, qword ptr [rcx + 0xd0]
00407399  test     rcx, rcx
0040739C  je       0x4073a6  ; -> 004073A6
0040739E  mov      r8d, r10d
004073A1  jmp      0x16d6a0  ; -> 0016D6A0 fn
004073A6  ret      
```

## 0046E050 (129 B, extent 0046E050-0046E0D1)

Documented callee on this page: `00861EC0`

```
0046E050  cmp      ecx, 2
0046E053  jge      0x46e0d0  ; -> 0046E0D0
0046E055  push     rbp
0046E056  push     rsi
0046E057  push     r14
0046E059  sub      rsp, 0x20
0046E05D  movsxd   rax, ecx
0046E060  mov      r14d, r8d
0046E063  mov      qword ptr [rsp + 0x40], rbx
0046E068  mov      esi, edx
0046E06A  mov      qword ptr [rsp + 0x48], rdi
0046E06F  xor      edx, edx
0046E071  mov      qword ptr [rsp + 0x50], r15
0046E076  mov      r8d, 0xa0
0046E07C  lea      rdi, [rax + rax*4]
0046E080  mov      rbp, r9
0046E083  shl      rdi, 5
0046E087  lea      r15, [rip + 0x2837fe2]  ; -> 02CA6070
0046E08E  lea      rbx, [rdi + r15]
0046E092  mov      rcx, rbx
0046E095  call     0x861ec0  ; -> 00861EC0 fn
0046E09A  mov      edx, r14d
0046E09D  mov      ecx, esi
0046E09F  call     0x46de80  ; -> 0046DE80 fn
0046E0A4  mov      dword ptr [rdi + r15 + 4], eax
0046E0A9  mov      qword ptr [rdi + r15 + 0x10], rbp
0046E0AE  mov      byte ptr [rdi + r15 + 0x98], 0
0046E0B7  mov      r15, qword ptr [rsp + 0x50]
0046E0BC  mov      rdi, qword ptr [rsp + 0x48]
0046E0C1  mov      dword ptr [rbx], esi
0046E0C3  mov      rbx, qword ptr [rsp + 0x40]
0046E0C8  add      rsp, 0x20
0046E0CC  pop      r14
0046E0CE  pop      rsi
0046E0CF  pop      rbp
0046E0D0  ret      
```

## 0050CC50 (64 B, extent 0050CC50-0050CC90)

Documented callee on this page: `0017D280`

```
0050CC50  push     rbx
0050CC52  sub      rsp, 0x20
0050CC56  mov      rcx, r9
0050CC59  call     0x267e10  ; -> 00267E10 fn
0050CC5E  mov      ebx, eax
0050CC60  cmp      eax, 0x1b
0050CC63  jge      0x50cc6c  ; -> 0050CC6C
0050CC65  mov      ebx, 0x1b
0050CC6A  jmp      0x50cc76  ; -> 0050CC76
0050CC6C  mov      eax, 0x27
0050CC71  cmp      ebx, eax
0050CC73  cmovg    ebx, eax
0050CC76  mov      ecx, ebx
0050CC78  call     0x16d6a0  ; -> 0016D6A0 fn
0050CC7D  mov      edx, ebx
0050CC7F  lea      rcx, [rip + 0x815c92]  ; -> 00D22918
0050CC86  add      rsp, 0x20
0050CC8A  pop      rbx
0050CC8B  jmp      0x17d280  ; -> 0017D280 fn
```

## 0050D570 (84 B, extent 0050D570-0050D5C4)

Documented callee on this page: `0017D280`

```
0050D570  mov      qword ptr [rsp + 8], rbx
0050D575  mov      qword ptr [rsp + 0x10], rsi
0050D57A  push     rdi
0050D57B  sub      rsp, 0x20
0050D57F  mov      rbx, r9
0050D582  mov      rdi, rdx
0050D585  call     0x2640c0  ; -> 002640C0 fn
0050D58A  mov      rcx, rbx
0050D58D  mov      rsi, rax
0050D590  call     0x267e10  ; -> 00267E10 fn
0050D595  test     eax, eax
0050D597  jns      0x50d59c  ; -> 0050D59C
0050D599  movzx    eax, word ptr [rdi]
0050D59C  mov      ecx, dword ptr [rsi + 0x28]
0050D59F  mov      edx, eax
0050D5A1  call     0x263a30  ; -> 00263A30 fn
0050D5A6  mov      rdx, rax
0050D5A9  lea      rcx, [rip + 0x3e6e88]  ; -> 008F4438
0050D5B0  mov      rbx, qword ptr [rsp + 0x30]
0050D5B5  mov      rsi, qword ptr [rsp + 0x38]
0050D5BA  add      rsp, 0x20
0050D5BE  pop      rdi
0050D5BF  jmp      0x17d280  ; -> 0017D280 fn
```

## 0050F070 (43 B, extent 0050F070-0050F09B)

Documented callee on this page: `0016D6A0`

```
0050F070  sub      rsp, 0x28
0050F074  mov      ecx, 7
0050F079  call     0x16d6a0  ; -> 0016D6A0 fn
0050F07E  mov      ecx, 0xc
0050F083  call     0x16d6a0  ; -> 0016D6A0 fn
0050F088  mov      ecx, 0xb
0050F08D  call     0x16d6a0  ; -> 0016D6A0 fn
0050F092  add      rsp, 0x28
0050F096  jmp      0x36ddb0  ; -> 0036DDB0 fn
```

## 0053EDB0 (233 B, extent 0053EDB0-0053EE99)

Documented callee on this page: `00249810`

```
0053EDB0  push     rbx
0053EDB2  sub      rsp, 0x20
0053EDB6  mov      rbx, qword ptr [rip + 0x2769cc3]  ; -> 02CA8A80
0053EDBD  test     rbx, rbx
0053EDC0  je       0x53ee93  ; -> 0053EE93
0053EDC6  mov      rcx, qword ptr [rbx + 0xc0]
0053EDCD  mov      qword ptr [rsp + 0x30], rdi
0053EDD2  test     rcx, rcx
0053EDD5  je       0x53ede7  ; -> 0053EDE7
0053EDD7  call     0x3697f0  ; -> 003697F0 fn
0053EDDC  mov      qword ptr [rbx + 0xc0], 0
0053EDE7  xor      edx, edx
0053EDE9  lea      rcx, [rbx + 0xc0]
0053EDF0  mov      r8d, 0x13d8
0053EDF6  call     0x861ec0  ; -> 00861EC0 fn
0053EDFB  mov      edx, 0x10000
0053EE00  mov      ecx, 2
0053EE05  call     0x249810  ; -> 00249810 fn
0053EE0A  xor      edx, edx
0053EE0C  mov      qword ptr [rbx + 0xc0], rax
0053EE13  mov      r8d, 0x10000
0053EE19  mov      rcx, rax
0053EE1C  call     0x861ec0  ; -> 00861EC0 fn
0053EE21  mov      rdi, qword ptr [rsp + 0x30]
0053EE26  mov      byte ptr [rbx + 0xfc], 0
0053EE2D  mov      byte ptr [rbx + 0x100], 0
0053EE34  mov      byte ptr [rbx + 0x102], 1
0053EE3B  mov      eax, dword ptr [rip + 0x18cd39b]  ; -> 01E0C1DC [u32 0x000001C0]
0053EE41  mov      dword ptr [rbx + 0xf0], eax
0053EE47  mov      eax, 0x80
0053EE4C  mov      word ptr [rbx + 0x1494], ax
0053EE53  mov      byte ptr [rbx + 0xff], 1
0053EE5A  mov      word ptr [rbx + 0xce], 0x202
0053EE63  mov      dword ptr [rbx + 0xd0], 0x3f800000
0053EE6D  mov      word ptr [rbx + 0xd6], 0x202
0053EE76  mov      dword ptr [rbx + 0xd8], 0x3f800000
0053EE80  mov      word ptr [rbx + 0xde], 0x202
0053EE89  mov      dword ptr [rbx + 0xe0], 0x3f800000
0053EE93  add      rsp, 0x20
0053EE97  pop      rbx
0053EE98  ret      
```

## 00598140 (54 B, extent 00598140-00598176)

Documented callee on this page: `00584730`

```
00598140  sub      rsp, 0x38
00598144  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0059814D  lea      rax, [rip + 0x78eb0c]  ; -> 00D26C60
00598154  mov      qword ptr [rcx], rax
00598157  mov      rdx, qword ptr [rcx + 0x10]
0059815B  test     rdx, rdx
0059815E  je       0x598171  ; -> 00598171
00598160  mov      eax, edx
00598162  not      al
00598164  test     al, 1
00598166  je       0x598171  ; -> 00598171
00598168  mov      rcx, rdx
0059816B  call     0x584730  ; -> 00584730 fn
00598170  nop      
00598171  add      rsp, 0x38
00598175  ret      
```

## 005994A0 (87 B, extent 005994A0-005994F7)

Documented callee on this page: `0017D260`

```
005994A0  push     rdi
005994A2  sub      rsp, 0x20
005994A6  mov      rdi, rcx
005994A9  test     rcx, rcx
005994AC  je       0x5994ef  ; -> 005994EF
005994AE  mov      qword ptr [rsp + 0x30], rbx
005994B3  mov      qword ptr [rsp + 0x38], rsi
005994B8  mov      esi, edx
005994BA  mov      edx, 2
005994BF  mov      ecx, esi
005994C1  call     0x17d260  ; -> 0017D260 fn
005994C6  mov      rbx, rax
005994C9  test     rax, rax
005994CC  je       0x5994df  ; -> 005994DF
005994CE  mov      r8d, esi
005994D1  mov      rdx, rdi
005994D4  mov      rcx, rax
005994D7  call     0x861eba  ; -> 00861EBA fn
005994DC  mov      rax, rbx
005994DF  mov      rbx, qword ptr [rsp + 0x30]
005994E4  mov      rsi, qword ptr [rsp + 0x38]
005994E9  add      rsp, 0x20
005994ED  pop      rdi
005994EE  ret      
005994EF  xor      eax, eax
005994F1  add      rsp, 0x20
005994F5  pop      rdi
005994F6  ret      
```

## 005A1C20 (51 B, extent 005A1C20-005A1C53)

Documented callee on this page: `00584730`

```
005A1C20  sub      rsp, 0x38
005A1C24  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
005A1C2D  mov      qword ptr [rdx + 0x38], 0
005A1C35  mov      rcx, qword ptr [rdx + 0x28]
005A1C39  test     rcx, rcx
005A1C3C  je       0x5a1c4c  ; -> 005A1C4C
005A1C3E  mov      eax, ecx
005A1C40  not      al
005A1C42  test     al, 1
005A1C44  je       0x5a1c4c  ; -> 005A1C4C
005A1C46  call     0x584730  ; -> 00584730 fn
005A1C4B  nop      
005A1C4C  mov      al, 1
005A1C4E  add      rsp, 0x38
005A1C52  ret      
```
