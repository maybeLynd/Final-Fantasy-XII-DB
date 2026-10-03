# F homing pack (FABLE): `19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md`

Generated 2026-10-03 04:02 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 18. No bearing page cites them and no documented function calls them directly.

## 001F3A00 (73 B, extent 001F3A00-001F3A49)

Documented callee on this page: `001B31D0`

```
001F3A00  push     rbx
001F3A02  sub      rsp, 0x20
001F3A06  mov      rbx, rdx
001F3A09  call     0x189120  ; -> 00189120 fn
001F3A0E  mov      rcx, rax
001F3A11  call     0x188730  ; -> 00188730 fn
001F3A16  xor      edx, edx
001F3A18  mov      rcx, rbx
001F3A1B  call     0x5fefd0  ; -> 005FEFD0 fn
001F3A20  call     0x1b31d0  ; -> 001B31D0 fn
001F3A25  test     rax, rax
001F3A28  je       0x1f3a37  ; -> 001F3A37
001F3A2A  call     0x1b31d0  ; -> 001B31D0 fn
001F3A2F  mov      rcx, rax
001F3A32  call     0x1b26f0  ; -> 001B26F0 fn
001F3A37  mov      edx, 3
001F3A3C  mov      rcx, rbx
001F3A3F  add      rsp, 0x20
001F3A43  pop      rbx
001F3A44  jmp      0x600a60  ; -> 00600A60 fn
```

## 0023CAF0 (412 B, extent 0023CAF0-0023CC8C)

Documented callee on this page: `0029FAD0`

```
0023CAF0  mov      qword ptr [rsp + 8], rbx
0023CAF5  mov      qword ptr [rsp + 0x10], rbp
0023CAFA  mov      qword ptr [rsp + 0x18], rsi
0023CAFF  mov      qword ptr [rsp + 0x20], rdi
0023CB04  push     r14
0023CB06  sub      rsp, 0x20
0023CB0A  cmp      dword ptr [rcx + 0xc8], 0
0023CB11  mov      rbx, rdx
0023CB14  mov      rax, qword ptr [rdx + 0x10]
0023CB18  mov      rdi, rcx
0023CB1B  movsxd   rbp, r9d
0023CB1E  je       0x23cc0c  ; -> 0023CC0C
0023CB24  mov      ecx, dword ptr [rcx + rbp*4 + 0xd0]
0023CB2B  mov      rsi, qword ptr [rax + 0x18]
0023CB2F  call     0x1e0b00  ; -> 001E0B00 fn
0023CB34  mov      ecx, eax
0023CB36  call     0x2f9860  ; -> 002F9860 fn
0023CB3B  xor      ecx, ecx
0023CB3D  mov      qword ptr [rsi + 0x18], rax
0023CB41  call     0x20e620  ; -> 0020E620 fn
0023CB46  mov      dword ptr [rsi + 0x20], eax
0023CB49  mov      rax, qword ptr [rbx + 0x10]
0023CB4D  mov      rcx, qword ptr [rax + 0x18]
0023CB51  or       dword ptr [rcx + 8], 1
0023CB55  mov      rax, qword ptr [rbx + 0x10]
0023CB59  mov      rcx, qword ptr [rax + 0x20]
0023CB5D  and      dword ptr [rcx + 8], 0xfffffffe
0023CB61  cmp      dword ptr [rdi + 0xe8], ebp
0023CB67  jne      0x23cbb6  ; -> 0023CBB6
0023CB69  mov      rax, qword ptr [rbx + 0x10]
0023CB6D  mov      rcx, qword ptr [rax]
0023CB70  or       dword ptr [rcx + 8], 1
0023CB74  mov      rax, qword ptr [rbx + 0x10]
0023CB78  mov      rcx, qword ptr [rax + 8]
0023CB7C  and      dword ptr [rcx + 8], 0xfffffffe
0023CB80  mov      rax, qword ptr [rbx + 0x10]
0023CB84  mov      rcx, qword ptr [rax + 0x10]
0023CB88  and      dword ptr [rcx + 8], 0xfffffffe
0023CB8C  cmp      dword ptr [rdi + 0xec], 0
0023CB93  je       0x23cc64  ; -> 0023CC64
0023CB99  mov      ecx, 0x46dd
0023CB9E  call     0x2f9860  ; -> 002F9860 fn
0023CBA3  xor      ecx, ecx
0023CBA5  mov      qword ptr [rsi + 0x18], rax
0023CBA9  call     0x20e620  ; -> 0020E620 fn
0023CBAE  mov      dword ptr [rsi + 0x20], eax
0023CBB1  jmp      0x23cc64  ; -> 0023CC64
0023CBB6  mov      eax, dword ptr [rdi + rbp*4 + 0xd0]
0023CBBD  cmp      dword ptr [rdi + rbp*4 + 0xdc], eax
0023CBC4  mov      rax, qword ptr [rbx + 0x10]
0023CBC8  je       0x23cbeb  ; -> 0023CBEB
0023CBCA  mov      rcx, qword ptr [rax + 0x10]
0023CBCE  or       dword ptr [rcx + 8], 1
0023CBD2  mov      rax, qword ptr [rbx + 0x10]
0023CBD6  mov      rcx, qword ptr [rax + 8]
0023CBDA  and      dword ptr [rcx + 8], 0xfffffffe
0023CBDE  mov      rax, qword ptr [rbx + 0x10]
0023CBE2  mov      rcx, qword ptr [rax]
0023CBE5  and      dword ptr [rcx + 8], 0xfffffffe
0023CBE9  jmp      0x23cc64  ; -> 0023CC64
0023CBEB  mov      rcx, qword ptr [rax]
0023CBEE  and      dword ptr [rcx + 8], 0xfffffffe
0023CBF2  mov      rax, qword ptr [rbx + 0x10]
0023CBF6  mov      rcx, qword ptr [rax + 8]
0023CBFA  or       dword ptr [rcx + 8], 1
0023CBFE  mov      rax, qword ptr [rbx + 0x10]
0023CC02  mov      rcx, qword ptr [rax + 0x10]
0023CC06  and      dword ptr [rcx + 8], 0xfffffffe
0023CC0A  jmp      0x23cc64  ; -> 0023CC64
0023CC0C  mov      rsi, qword ptr [rax + 0x20]
0023CC10  lea      ecx, [rbp + 0x53f]
0023CC16  call     0x2f9860  ; -> 002F9860 fn
0023CC1B  xor      ecx, ecx
0023CC1D  mov      qword ptr [rsi + 0x18], rax
0023CC21  call     0x20e620  ; -> 0020E620 fn
0023CC26  mov      dword ptr [rsi + 0x20], eax
0023CC29  mov      rax, qword ptr [rbx + 0x10]
0023CC2D  mov      rcx, qword ptr [rax]
0023CC30  and      dword ptr [rcx + 8], 0xfffffffe
0023CC34  mov      rax, qword ptr [rbx + 0x10]
0023CC38  mov      rcx, qword ptr [rax + 8]
0023CC3C  and      dword ptr [rcx + 8], 0xfffffffe
0023CC40  mov      rax, qword ptr [rbx + 0x10]
0023CC44  mov      rdx, qword ptr [rax + 0x18]
0023CC48  and      dword ptr [rdx + 8], 0xfffffffe
0023CC4C  mov      rax, qword ptr [rbx + 0x10]
0023CC50  mov      rdx, qword ptr [rax + 0x20]
0023CC54  or       dword ptr [rdx + 8], 1
0023CC58  mov      rax, qword ptr [rbx + 0x10]
0023CC5C  mov      rdx, qword ptr [rax + 0x10]
0023CC60  and      dword ptr [rdx + 8], 0xfffffffe
0023CC64  mov      rcx, rsi
0023CC67  call     0x29fad0  ; -> 0029FAD0 fn
0023CC6C  mov      rbx, qword ptr [rsp + 0x30]
0023CC71  mov      eax, 1
0023CC76  mov      rbp, qword ptr [rsp + 0x38]
0023CC7B  mov      rsi, qword ptr [rsp + 0x40]
0023CC80  mov      rdi, qword ptr [rsp + 0x48]
0023CC85  add      rsp, 0x20
0023CC89  pop      r14
0023CC8B  ret      
```

## 0026A660 (184 B, extent 0026A660-0026A718)

Documented callee on this page: `0020E600`

```
0026A660  mov      qword ptr [rsp + 0x18], rsi
0026A665  push     rdi
0026A666  sub      rsp, 0x20
0026A66A  mov      esi, edx
0026A66C  mov      rdi, rcx
0026A66F  test     edx, edx
0026A671  je       0x26a6fe  ; -> 0026A6FE
0026A677  movzx    eax, byte ptr [rcx + 0x15]
0026A67B  mov      qword ptr [rsp + 0x30], rbx
0026A680  imul     rbx, rax, 0x288
0026A687  lea      rax, [rip + 0x1e2e782]  ; -> 02098E10
0026A68E  mov      qword ptr [rsp + 0x38], rbp
0026A693  add      rbx, rax
0026A696  mov      ebp, 0xffff
0026A69B  cmp      byte ptr [rcx + 0x18], 1
0026A69F  je       0x26a6d9  ; -> 0026A6D9
0026A6A1  movzx    eax, word ptr [rcx + 0xd2]
0026A6A8  cmp      ax, bp
0026A6AB  jne      0x26a6d0  ; -> 0026A6D0
0026A6AD  mov      rax, qword ptr [rcx + 0x40]
0026A6B1  mov      rbx, qword ptr [rbx]
0026A6B4  mov      ecx, dword ptr [rax + 0x18]
0026A6B7  call     0x20e600  ; -> 0020E600 fn
0026A6BC  mov      ecx, eax
0026A6BE  mov      eax, 5
0026A6C3  cmp      ax, word ptr [rcx + rbx]
0026A6C7  jge      0x26a6d7  ; -> 0026A6D7
0026A6C9  movsx    eax, word ptr [rcx + rbx + 0xc]
0026A6CE  jmp      0x26a6d3  ; -> 0026A6D3
0026A6D0  movzx    eax, ax
0026A6D3  test     eax, eax
0026A6D5  jns      0x26a6d9  ; -> 0026A6D9
0026A6D7  jmp      0x26a6d7  ; -> 0026A6D7
0026A6D9  cmp      byte ptr [rdi + 0x18], 1
0026A6DD  mov      rbx, qword ptr [rsp + 0x30]
0026A6E2  je       0x26a6f9  ; -> 0026A6F9
0026A6E4  cmp      word ptr [rdi + 0xd0], bp
0026A6EB  jne      0x26a6f9  ; -> 0026A6F9
0026A6ED  mov      rax, qword ptr [rdi + 0x40]
0026A6F1  mov      ecx, dword ptr [rax + 0x18]
0026A6F4  call     0x20e600  ; -> 0020E600 fn
0026A6F9  mov      rbp, qword ptr [rsp + 0x38]
0026A6FE  and      byte ptr [rdi + 0xc], 0xdf
0026A702  test     esi, esi
0026A704  mov      rsi, qword ptr [rsp + 0x40]
0026A709  setne    al
0026A70C  shl      al, 5
0026A70F  or       byte ptr [rdi + 0xc], al
0026A712  add      rsp, 0x20
0026A716  pop      rdi
0026A717  ret      
```

## 002A7C70 (183 B, extent 002A7C70-002A7D27)

Documented callee on this page: `001EDDA0`

```
002A7C70  mov      qword ptr [rsp + 0x10], rbx
002A7C75  mov      qword ptr [rsp + 0x18], rbp
002A7C7A  mov      qword ptr [rsp + 0x20], rsi
002A7C7F  push     rdi
002A7C80  sub      rsp, 0x20
002A7C84  mov      esi, r9d
002A7C87  mov      ebp, r8d
002A7C8A  mov      rdi, rdx
002A7C8D  mov      rbx, rcx
002A7C90  test     r9d, r9d
002A7C93  jne      0x2a7ca0  ; -> 002A7CA0
002A7C95  and      dword ptr [rcx + 8], 0xfffffff7
002A7C99  mov      eax, dword ptr [rdx]
002A7C9B  mov      dword ptr [rcx + 0x20], eax
002A7C9E  jmp      0x2a7d12  ; -> 002A7D12
002A7CA0  mov      qword ptr [rsp + 0x30], r14
002A7CA5  xor      r14d, r14d
002A7CA8  cmp      word ptr [rcx + 0x40], r14w
002A7CAD  jne      0x2a7cbc  ; -> 002A7CBC
002A7CAF  call     0x1edda0  ; -> 001EDDA0 fn
002A7CB4  test     eax, eax
002A7CB6  jne      0x2a7cbc  ; -> 002A7CBC
002A7CB8  mov      dword ptr [rbx + 0x20], r14d
002A7CBC  or       dword ptr [rbx + 8], 8
002A7CC0  mov      eax, dword ptr [rbx + 0x20]
002A7CC3  mov      dword ptr [rbx + 0x34], eax
002A7CC6  mov      word ptr [rbx + 0x44], bp
002A7CCA  movzx    ecx, byte ptr [rdi]
002A7CCD  movzx    eax, al
002A7CD0  sub      cx, ax
002A7CD3  movzx    eax, byte ptr [rbx + 0x21]
002A7CD7  mov      word ptr [rbx + 0x38], cx
002A7CDB  movzx    ecx, byte ptr [rdi + 1]
002A7CDF  sub      cx, ax
002A7CE2  movzx    eax, byte ptr [rbx + 0x22]
002A7CE6  mov      word ptr [rbx + 0x3a], cx
002A7CEA  movzx    ecx, byte ptr [rdi + 2]
002A7CEE  sub      cx, ax
002A7CF1  movzx    eax, byte ptr [rbx + 0x23]
002A7CF5  mov      word ptr [rbx + 0x3c], cx
002A7CF9  movzx    ecx, byte ptr [rdi + 3]
002A7CFD  sub      cx, ax
002A7D00  mov      word ptr [rbx + 0x40], r14w
002A7D05  mov      r14, qword ptr [rsp + 0x30]
002A7D0A  mov      word ptr [rbx + 0x3e], cx
002A7D0E  mov      word ptr [rbx + 0x42], si
002A7D12  mov      rbx, qword ptr [rsp + 0x38]
002A7D17  mov      rbp, qword ptr [rsp + 0x40]
002A7D1C  mov      rsi, qword ptr [rsp + 0x48]
002A7D21  add      rsp, 0x20
002A7D25  pop      rdi
002A7D26  ret      
```

## 002D5590 (255 B, extent 002D5590-002D568F)

Documented callee on this page: `001EDEC0`

```
002D5590  push     rbx
002D5592  sub      rsp, 0x20
002D5596  mov      rbx, rcx
002D5599  mov      ecx, dword ptr [rdx]
002D559B  sub      ecx, 1
002D559E  je       0x2d55f3  ; -> 002D55F3
002D55A0  cmp      ecx, 1
002D55A3  je       0x2d55b2  ; -> 002D55B2
002D55A5  mov      rcx, rbx
002D55A8  add      rsp, 0x20
002D55AC  pop      rbx
002D55AD  jmp      0x5c5230  ; -> 005C5230 fn
002D55B2  mov      ecx, dword ptr [rbx + 0xb4]
002D55B8  call     0x1edec0  ; -> 001EDEC0 fn
002D55BD  test     eax, eax
002D55BF  je       0x2d5687  ; -> 002D5687
002D55C5  mov      eax, dword ptr [rbx + 0xc4]
002D55CB  test     eax, eax
002D55CD  jle      0x2d5687  ; -> 002D5687
002D55D3  dec      eax
002D55D5  mov      dword ptr [rbx + 0xc4], eax
002D55DB  test     eax, eax
002D55DD  jg       0x2d5687  ; -> 002D5687
002D55E3  mov      rcx, rbx
002D55E6  call     0x244f00  ; -> 00244F00 fn
002D55EB  xor      eax, eax
002D55ED  add      rsp, 0x20
002D55F1  pop      rbx
002D55F2  ret      
002D55F3  mov      dword ptr [rbx + 0xc4], 0x28
002D55FD  mov      rcx, rbx
002D5600  mov      eax, dword ptr [rdx + 8]
002D5603  lea      rdx, [rip + 0x641b76]  ; -> 00917180
002D560A  mov      dword ptr [rbx + 0xc0], eax
002D5610  call     0x247570  ; -> 00247570 fn
002D5615  mov      ecx, dword ptr [rbx + 0xc0]
002D561B  sub      ecx, 1
002D561E  je       0x2d5635  ; -> 002D5635
002D5620  cmp      ecx, 1
002D5623  je       0x2d562d  ; -> 002D562D
002D5625  mov      r8d, 3
002D562B  jmp      0x2d563b  ; -> 002D563B
002D562D  mov      r8d, 5
002D5633  jmp      0x2d563b  ; -> 002D563B
002D5635  mov      r8d, 4
002D563B  mov      rax, qword ptr [rip + 0x1dc55ee]  ; -> 0209AC30
002D5642  lea      rcx, [rbx + 0x50]
002D5646  mov      r9, rbx
002D5649  mov      rdx, qword ptr [rax + 0x18]
002D564D  call     0x2432b0  ; -> 002432B0 fn
002D5652  movzx    r8d, word ptr [rax + 0xa]
002D5657  movzx    edx, word ptr [rax + 8]
002D565B  movsx    ecx, word ptr [rax + 6]
002D565F  movzx    eax, word ptr [rax + 4]
002D5663  and      dword ptr [rbx + 0x40], 0xffffff7f
002D566A  mov      word ptr [rbx + 0x98], ax
002D5671  mov      word ptr [rbx + 0x9a], cx
002D5678  mov      word ptr [rbx + 0x9c], dx
002D567F  mov      word ptr [rbx + 0x9e], r8w
002D5687  xor      eax, eax
002D5689  add      rsp, 0x20
002D568D  pop      rbx
002D568E  ret      
```

## 003484A0 (26 B, extent 003484A0-003484BA)

Documented callee on this page: `00263FF0`

```
003484A0  sub      rsp, 0x28
003484A4  mov      ecx, 3
003484A9  call     0x263ff0  ; -> 00263FF0 fn
003484AE  mov      rcx, rax
003484B1  add      rsp, 0x28
003484B5  jmp      0x3b7ab0  ; -> 003B7AB0 fn
```

## 00348A70 (26 B, extent 00348A70-00348A8A)

Documented callee on this page: `00263FF0`

```
00348A70  sub      rsp, 0x28
00348A74  mov      ecx, 3
00348A79  call     0x263ff0  ; -> 00263FF0 fn
00348A7E  mov      rcx, rax
00348A81  add      rsp, 0x28
00348A85  jmp      0x3b7210  ; -> 003B7210 fn
```

## 00348DA0 (26 B, extent 00348DA0-00348DBA)

Documented callee on this page: `00263FF0`

```
00348DA0  sub      rsp, 0x28
00348DA4  mov      ecx, 3
00348DA9  call     0x263ff0  ; -> 00263FF0 fn
00348DAE  mov      rcx, rax
00348DB1  add      rsp, 0x28
00348DB5  jmp      0x3b7a30  ; -> 003B7A30 fn
```

## 00357170 (36 B, extent 00357170-00357194)

Documented callee on this page: `00263FF0`

```
00357170  push     rbx
00357172  sub      rsp, 0x20
00357176  xor      ecx, ecx
00357178  call     0x263ff0  ; -> 00263FF0 fn
0035717D  mov      rbx, rax
00357180  call     0x264160  ; -> 00264160 fn
00357185  cmp      eax, 2
00357188  je       0x35718e  ; -> 0035718E
0035718A  or       byte ptr [rbx + 0x17], 4
0035718E  add      rsp, 0x20
00357192  pop      rbx
00357193  ret      
```

## 003E0860 (168 B, extent 003E0860-003E0908)

Documented callee on this page: `0020E600`

```
003E0860  test     rcx, rcx
003E0863  je       0x3e0907  ; -> 003E0907
003E0869  push     rbx
003E086A  sub      rsp, 0x20
003E086E  mov      rbx, rcx
003E0871  mov      ecx, dword ptr [rcx + 8]
003E0874  call     0x20e600  ; -> 0020E600 fn
003E0879  test     rax, rax
003E087C  je       0x3e088e  ; -> 003E088E
003E087E  mov      ecx, dword ptr [rbx + 8]
003E0881  call     0x20e600  ; -> 0020E600 fn
003E0886  mov      rcx, rax
003E0889  call     0x5154b0  ; -> 005154B0 fn
003E088E  mov      ecx, dword ptr [rbx + 0x28]
003E0891  call     0x20e600  ; -> 0020E600 fn
003E0896  test     rax, rax
003E0899  je       0x3e08ab  ; -> 003E08AB
003E089B  mov      ecx, dword ptr [rbx + 0x28]
003E089E  call     0x20e600  ; -> 0020E600 fn
003E08A3  mov      rcx, rax
003E08A6  call     0x518e60  ; -> 00518E60 fn
003E08AB  mov      ecx, dword ptr [rbx + 0x34]
003E08AE  call     0x20e600  ; -> 0020E600 fn
003E08B3  test     rax, rax
003E08B6  je       0x3e08c8  ; -> 003E08C8
003E08B8  mov      ecx, dword ptr [rbx + 0x34]
003E08BB  call     0x20e600  ; -> 0020E600 fn
003E08C0  mov      rcx, rax
003E08C3  call     0x4719f0  ; -> 004719F0 fn
003E08C8  mov      ecx, dword ptr [rbx + 0x3c]
003E08CB  call     0x20e600  ; -> 0020E600 fn
003E08D0  test     rax, rax
003E08D3  je       0x3e08e5  ; -> 003E08E5
003E08D5  mov      ecx, dword ptr [rbx + 0x3c]
003E08D8  call     0x20e600  ; -> 0020E600 fn
003E08DD  mov      rcx, rax
003E08E0  call     0x472820  ; -> 00472820 fn
003E08E5  mov      ecx, dword ptr [rbx + 0x24]
003E08E8  call     0x20e600  ; -> 0020E600 fn
003E08ED  test     rax, rax
003E08F0  je       0x3e0902  ; -> 003E0902
003E08F2  mov      ecx, dword ptr [rbx + 0x24]
003E08F5  call     0x20e600  ; -> 0020E600 fn
003E08FA  mov      rcx, rax
003E08FD  call     0x5175f0  ; -> 005175F0 fn
003E0902  add      rsp, 0x20
003E0906  pop      rbx
003E0907  ret      
```

## 003EF050 (488 B, extent 003EF050-003EF238)

Documented callee on this page: `001EDEC0`

```
003EF050  mov      qword ptr [rsp + 8], rbx
003EF055  push     rdi
003EF056  sub      rsp, 0x20
003EF05A  mov      eax, dword ptr [rdx]
003EF05C  mov      rdi, rdx
003EF05F  dec      eax
003EF061  mov      rbx, rcx
003EF064  cmp      eax, 0x12
003EF067  ja       0x3ef226  ; -> 003EF226
003EF06D  lea      rcx, [rip - 0x2cf074]  ; -> 00120000 (image base)
003EF074  cdqe     
003EF076  mov      r8d, dword ptr [rcx + rax*4 + 0x2cf238]  ; image base + 0x2cf238 = 003EF238
003EF07E  add      r8, rcx
003EF081  jmp      r8
003EF084  mov      rdx, qword ptr [rdx + 0x10]
003EF088  lea      rcx, [rbx + 0x50]
003EF08C  mov      r9, rbx
003EF08F  mov      r8d, 1
003EF095  call     0x2432b0  ; -> 002432B0 fn
003EF09A  movzx    ecx, word ptr [rax + 0xa]
003EF09E  movzx    edx, word ptr [rax + 8]
003EF0A2  movsx    r8d, word ptr [rax + 6]
003EF0A7  test     rbx, rbx
003EF0AA  je       0x3ef0cd  ; -> 003EF0CD
003EF0AC  movzx    eax, word ptr [rax + 4]
003EF0B0  mov      word ptr [rbx + 0x98], ax
003EF0B7  mov      word ptr [rbx + 0x9a], r8w
003EF0BF  mov      word ptr [rbx + 0x9c], dx
003EF0C6  mov      word ptr [rbx + 0x9e], cx
003EF0CD  mov      rax, qword ptr [rdi + 8]
003EF0D1  mov      rcx, rbx
003EF0D4  mov      qword ptr [rbx + 0xc0], rax
003EF0DB  xor      eax, eax
003EF0DD  mov      qword ptr [rbx + 0xc8], rax
003EF0E4  lea      edx, [rax + 0x63]
003EF0E7  call     0x247930  ; -> 00247930 fn
003EF0EC  mov      rcx, qword ptr [rip + 0x27700d5]  ; -> 02B5F1C8
003EF0F3  mov      rdx, rbx
003EF0F6  mov      dword ptr [rbx + 0xc8], 0x12
003EF100  call     0x244960  ; -> 00244960 fn
003EF105  xor      edx, edx
003EF107  mov      rcx, rbx
003EF10A  call     0x247870  ; -> 00247870 fn
003EF10F  xor      eax, eax
003EF111  mov      rbx, qword ptr [rsp + 0x30]
003EF116  add      rsp, 0x20
003EF11A  pop      rdi
003EF11B  ret      
003EF11C  mov      ecx, dword ptr [rbx + 0xb4]
003EF122  call     0x1edec0  ; -> 001EDEC0 fn
003EF127  test     eax, eax
003EF129  je       0x3ef219  ; -> 003EF219
003EF12F  test     byte ptr [rbx + 0xcc], 1
003EF136  jne      0x3ef219  ; -> 003EF219
003EF13C  mov      eax, dword ptr [rbx + 0xc8]
003EF142  test     eax, eax
003EF144  je       0x3ef155  ; -> 003EF155
003EF146  sub      eax, 1
003EF149  mov      dword ptr [rbx + 0xc8], eax
003EF14F  jne      0x3ef219  ; -> 003EF219
003EF155  mov      rcx, qword ptr [rip + 0x277006c]  ; -> 02B5F1C8
003EF15C  mov      rdx, rbx
003EF15F  call     0x246ad0  ; -> 00246AD0 fn
003EF164  xor      eax, eax
003EF166  mov      rbx, qword ptr [rsp + 0x30]
003EF16B  add      rsp, 0x20
003EF16F  pop      rdi
003EF170  ret      
003EF171  or       dword ptr [rbx + 0xcc], 1
003EF178  mov      rcx, rbx
003EF17B  call     0x2470d0  ; -> 002470D0 fn
003EF180  xor      eax, eax
003EF182  mov      rbx, qword ptr [rsp + 0x30]
003EF187  add      rsp, 0x20
003EF18B  pop      rdi
003EF18C  ret      
003EF18D  mov      edx, 0x13
003EF192  jmp      0x3ef207  ; -> 003EF207
003EF194  mov      rax, qword ptr [rip + 0x277002d]  ; -> 02B5F1C8
003EF19B  mov      rcx, qword ptr [rax + 0xd0]
003EF1A2  test     byte ptr [rcx + 0xc4], 1
003EF1A9  jne      0x3ef1b9  ; -> 003EF1B9
003EF1AB  mov      eax, 0xff09
003EF1B0  test     word ptr [rip + 0x2ba81b3], ax  ; -> 02F9736A
003EF1B7  je       0x3ef219  ; -> 003EF219
003EF1B9  mov      rcx, qword ptr [rbx + 0xc0]
003EF1C0  xor      r8d, r8d
003EF1C3  mov      edx, 0x8001
003EF1C8  call     0x247510  ; -> 00247510 fn
003EF1CD  xor      eax, eax
003EF1CF  mov      rbx, qword ptr [rsp + 0x30]
003EF1D4  add      rsp, 0x20
003EF1D8  pop      rdi
003EF1D9  ret      
003EF1DA  mov      r8, qword ptr [rdx + 0x10]
003EF1DE  mov      rdx, qword ptr [rdx + 8]
003EF1E2  mov      rcx, qword ptr [rbx + 0xc0]
003EF1E9  call     0x247510  ; -> 00247510 fn
003EF1EE  xor      eax, eax
003EF1F0  mov      rbx, qword ptr [rsp + 0x30]
003EF1F5  add      rsp, 0x20
003EF1F9  pop      rdi
003EF1FA  ret      
003EF1FB  mov      edx, 0xf
003EF200  jmp      0x3ef207  ; -> 003EF207
003EF202  mov      edx, 0x12
003EF207  mov      rcx, qword ptr [rbx + 0xc0]
003EF20E  mov      r8d, 3
003EF214  call     0x247510  ; -> 00247510 fn
003EF219  xor      eax, eax
003EF21B  mov      rbx, qword ptr [rsp + 0x30]
003EF220  add      rsp, 0x20
003EF224  pop      rdi
003EF225  ret      
003EF226  mov      rcx, rbx
003EF229  mov      rbx, qword ptr [rsp + 0x30]
003EF22E  add      rsp, 0x20
003EF232  pop      rdi
003EF233  jmp      0x5c5230  ; -> 005C5230 fn
```

## 00551610 (144 B, extent 00551610-005516A0)

Documented callee on this page: `0020E620`

```
00551610  push     rbx
00551612  sub      rsp, 0x20
00551616  cmp      qword ptr [rcx + 8], 0
0055161B  mov      rbx, r8
0055161E  mov      r10, rcx
00551621  jne      0x551632  ; -> 00551632
00551623  and      dword ptr [rdx + 8], 0xfffffffe
00551627  and      dword ptr [r8 + 8], 0xfffffffe
0055162C  add      rsp, 0x20
00551630  pop      rbx
00551631  ret      
00551632  cmp      byte ptr [rcx + 2], 0
00551636  jbe      0x55164f  ; -> 0055164F
00551638  mov      rax, qword ptr [rdx + 0x20]
0055163C  movzx    ecx, byte ptr [rax + 7]
00551640  xor      eax, eax
00551642  mov      word ptr [rdx + 0xa], ax
00551646  or       dword ptr [rdx + 8], 1
0055164A  mov      byte ptr [rdx + 0x39], cl
0055164D  jmp      0x551672  ; -> 00551672
0055164F  test     byte ptr [rcx + 0x10], 1
00551653  je       0x55166e  ; -> 0055166E
00551655  mov      rax, qword ptr [rdx + 0x20]
00551659  movzx    ecx, byte ptr [rax + 0xf]
0055165D  mov      eax, 1
00551662  mov      word ptr [rdx + 0xa], ax
00551666  or       dword ptr [rdx + 8], eax
00551669  mov      byte ptr [rdx + 0x39], cl
0055166C  jmp      0x551672  ; -> 00551672
0055166E  and      dword ptr [rdx + 8], 0xfffffffe
00551672  mov      eax, dword ptr [r10 + 0x10]
00551676  xor      ecx, ecx
00551678  shr      eax, 1
0055167A  xor      eax, dword ptr [r9 + 8]
0055167E  and      eax, 1
00551681  xor      dword ptr [r9 + 8], eax
00551685  or       dword ptr [r8 + 8], 1
0055168A  mov      rax, qword ptr [r10 + 8]
0055168E  mov      qword ptr [r8 + 0x18], rax
00551692  call     0x20e620  ; -> 0020E620 fn
00551697  mov      dword ptr [rbx + 0x20], eax
0055169A  add      rsp, 0x20
0055169E  pop      rbx
0055169F  ret      
```

## 005516A0 (346 B, extent 005516A0-005517FA)

Documented callee on this page: `0020E620`

```
005516A0  mov      qword ptr [rsp + 0x10], rbx
005516A5  mov      qword ptr [rsp + 0x18], rsi
005516AA  push     rdi
005516AB  sub      rsp, 0x20
005516AF  mov      r10, qword ptr [rdx + 0x10]
005516B3  mov      rbx, rcx
005516B6  movsx    rax, byte ptr [rcx + 0x17]
005516BB  movsx    edx, word ptr [rcx + 0x14]
005516BF  sar      edx, 7
005516C2  mov      dword ptr [rsp + 0x30], 0x80808080
005516CA  mov      r11, qword ptr [r10 + rax*8]
005516CE  movsx    rax, byte ptr [rcx + 0x16]
005516D3  movsxd   rsi, r9d
005516D6  mov      rdi, qword ptr [r10 + rax*8]
005516DA  movsx    rax, word ptr [rcx + 0x18]
005516DF  mov      r9, qword ptr [r10 + rax*8]
005516E3  movsx    eax, word ptr [r8 + 0x58]
005516E8  imul     edx, eax
005516EB  sar      edx, 7
005516EE  mov      byte ptr [rdi + 0x27], dl
005516F1  mov      byte ptr [rsp + 0x33], dl
005516F5  mov      eax, dword ptr [rsp + 0x30]
005516F9  mov      dword ptr [r11 + 0x34], eax
005516FD  mov      dword ptr [r11 + 0x30], eax
00551701  mov      dword ptr [r11 + 0x2c], eax
00551705  mov      dword ptr [r11 + 0x28], eax
00551709  mov      dword ptr [r9 + 0x34], eax
0055170D  mov      dword ptr [r9 + 0x30], eax
00551711  mov      dword ptr [r9 + 0x2c], eax
00551715  mov      dword ptr [r9 + 0x28], eax
00551719  test     edx, edx
0055171B  jne      0x551730  ; -> 00551730
0055171D  and      dword ptr [r11 + 8], 0xfffffffe
00551722  and      dword ptr [rdi + 8], 0xfffffffe
00551726  and      dword ptr [r9 + 8], 0xfffffffe
0055172B  jmp      0x5517e5  ; -> 005517E5
00551730  movsx    ecx, word ptr [rcx + 0x10]
00551734  test     ecx, ecx
00551736  je       0x5517cb  ; -> 005517CB
0055173C  sub      ecx, 1
0055173F  je       0x55175e  ; -> 0055175E
00551741  cmp      ecx, 2
00551744  jne      0x5517e5  ; -> 005517E5
0055174A  lea      rcx, [rbx + 0x28]
0055174E  mov      r8, rdi
00551751  mov      rdx, r11
00551754  call     0x552050  ; -> 00552050 fn
00551759  jmp      0x5517e5  ; -> 005517E5
0055175E  lea      rcx, [rsi + rsi*2]
00551762  cmp      qword ptr [rbx + rcx*8 + 0x30], 0
00551768  lea      rdx, [rbx + rcx*8]
0055176C  jne      0x551779  ; -> 00551779
0055176E  and      dword ptr [r11 + 8], 0xfffffffe
00551773  and      dword ptr [rdi + 8], 0xfffffffe
00551777  jmp      0x5517e5  ; -> 005517E5
00551779  mov      ebx, 1
0055177E  test     byte ptr [rdx + 0x38], bl
00551781  je       0x55179a  ; -> 0055179A
00551783  mov      rax, qword ptr [r11 + 0x20]
00551787  movzx    ecx, byte ptr [rax + 0xf]
0055178B  mov      word ptr [r11 + 0xa], bx
00551790  or       dword ptr [r11 + 8], ebx
00551794  mov      byte ptr [r11 + 0x39], cl
00551798  jmp      0x55179f  ; -> 0055179F
0055179A  and      dword ptr [r11 + 8], 0xfffffffe
0055179F  and      dword ptr [r9 + 8], 0xfffffffe
005517A4  xor      ecx, ecx
005517A6  or       dword ptr [rdi + 8], ebx
005517A9  mov      rax, qword ptr [rdx + 0x30]
005517AD  mov      qword ptr [rdi + 0x18], rax
005517B1  call     0x20e620  ; -> 0020E620 fn
005517B6  mov      dword ptr [rdi + 0x20], eax
005517B9  mov      eax, ebx
005517BB  mov      rbx, qword ptr [rsp + 0x38]
005517C0  mov      rsi, qword ptr [rsp + 0x40]
005517C5  add      rsp, 0x20
005517C9  pop      rdi
005517CA  ret      
005517CB  lea      rcx, [rsi*2 + 5]
005517D3  mov      r8, rdi
005517D6  add      rcx, rsi
005517D9  mov      rdx, r11
005517DC  lea      rcx, [rbx + rcx*8]
005517E0  call     0x551610  ; -> 00551610 fn
005517E5  mov      rbx, qword ptr [rsp + 0x38]
005517EA  mov      eax, 1
005517EF  mov      rsi, qword ptr [rsp + 0x40]
005517F4  add      rsp, 0x20
005517F8  pop      rdi
005517F9  ret      
```

## 00552050 (149 B, extent 00552050-005520E5)

Documented callee on this page: `0020E620`

```
00552050  push     rbx
00552052  sub      rsp, 0x20
00552056  cmp      qword ptr [rcx + 8], 0
0055205B  mov      rbx, r8
0055205E  mov      r10, rcx
00552061  jne      0x552077  ; -> 00552077
00552063  and      dword ptr [rdx + 8], 0xfffffffe
00552067  and      dword ptr [r8 + 8], 0xfffffffe
0055206C  and      dword ptr [r9 + 8], 0xfffffffe
00552071  add      rsp, 0x20
00552075  pop      rbx
00552076  ret      
00552077  test     byte ptr [rcx + 0x14], 1
0055207B  je       0x552094  ; -> 00552094
0055207D  mov      rax, qword ptr [rdx + 0x20]
00552081  movzx    ecx, byte ptr [rax + 7]
00552085  xor      eax, eax
00552087  mov      word ptr [rdx + 0xa], ax
0055208B  or       dword ptr [rdx + 8], 1
0055208F  mov      byte ptr [rdx + 0x39], cl
00552092  jmp      0x5520b7  ; -> 005520B7
00552094  test     byte ptr [rcx + 0x10], 1
00552098  je       0x5520b3  ; -> 005520B3
0055209A  mov      rax, qword ptr [rdx + 0x20]
0055209E  movzx    ecx, byte ptr [rax + 0xf]
005520A2  mov      eax, 1
005520A7  mov      word ptr [rdx + 0xa], ax
005520AB  or       dword ptr [rdx + 8], eax
005520AE  mov      byte ptr [rdx + 0x39], cl
005520B1  jmp      0x5520b7  ; -> 005520B7
005520B3  and      dword ptr [rdx + 8], 0xfffffffe
005520B7  mov      eax, dword ptr [r10 + 0x10]
005520BB  xor      ecx, ecx
005520BD  shr      eax, 1
005520BF  xor      eax, dword ptr [r9 + 8]
005520C3  and      eax, 1
005520C6  xor      dword ptr [r9 + 8], eax
005520CA  or       dword ptr [r8 + 8], 1
005520CF  mov      rax, qword ptr [r10 + 8]
005520D3  mov      qword ptr [r8 + 0x18], rax
005520D7  call     0x20e620  ; -> 0020E620 fn
005520DC  mov      dword ptr [rbx + 0x20], eax
005520DF  add      rsp, 0x20
005520E3  pop      rbx
005520E4  ret      
```

## 00556F50 (55 B, extent 00556F50-00556F87)

Documented callee on this page: `0020E620`

```
00556F50  push     rbx
00556F52  sub      rsp, 0x20
00556F56  mov      rax, qword ptr [rdx + 0x10]
00556F5A  add      rcx, 0xd0
00556F61  mov      rbx, qword ptr [rax]
00556F64  movsxd   rax, r9d
00556F67  shl      rax, 8
00556F6B  add      rax, rcx
00556F6E  xor      ecx, ecx
00556F70  mov      qword ptr [rbx + 0x18], rax
00556F74  call     0x20e620  ; -> 0020E620 fn
00556F79  mov      dword ptr [rbx + 0x20], eax
00556F7C  mov      eax, 1
00556F81  add      rsp, 0x20
00556F85  pop      rbx
00556F86  ret      
```

## 00616560 (411 B, extent 00616560-006166FB)

Documented callee on this page: `00618FD0`

```
00616560  push     rdi
00616562  sub      rsp, 0x30
00616566  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0061656F  mov      qword ptr [rsp + 0x40], rbx
00616574  mov      rdi, rcx
00616577  add      rcx, 0x18c0
0061657E  call     0x6c8870  ; -> 006C8870 fn
00616583  nop      
00616584  mov      rcx, qword ptr [rdi + 0x1840]
0061658B  test     rcx, rcx
0061658E  je       0x6165a2  ; -> 006165A2
00616590  mov      rax, qword ptr [rcx]
00616593  call     qword ptr [rax + 0x10]
00616596  nop      
00616597  mov      qword ptr [rdi + 0x1840], 0
006165A2  and      dword ptr [rdi + 0x183c], 0xffffff7f
006165AC  lea      rcx, [rdi + 0x1820]
006165B3  call     0x16d6a0  ; -> 0016D6A0 fn
006165B8  nop      
006165B9  lea      rcx, [rdi + 0xba0]
006165C0  lea      r9, [rip - 0x4a8f27]  ; -> 0016D6A0
006165C7  mov      edx, 0x190
006165CC  mov      r8d, 8
006165D2  call     0x809054  ; -> 00809054 fn
006165D7  nop      
006165D8  mov      edx, dword ptr [rdi + 0x6f8]
006165DE  mov      eax, edx
006165E0  shr      eax, 0x1f
006165E3  not      al
006165E5  test     al, 1
006165E7  je       0x6165fa  ; -> 006165FA
006165E9  btr      edx, 0x1f
006165ED  mov      rcx, qword ptr [rdi + 0x700]
006165F4  call     0x618fd0  ; -> 00618FD0 fn
006165F9  nop      
006165FA  mov      qword ptr [rdi + 0x700], 0
00616605  mov      dword ptr [rdi + 0x6f8], 0
0061660F  lea      rcx, [rdi + 0x630]
00616616  call     0x16d6a0  ; -> 0016D6A0 fn
0061661B  nop      
0061661C  lea      r9, [rip - 0x4a8f83]  ; -> 0016D6A0
00616623  mov      edx, 0x18
00616628  lea      r8d, [rdx - 0x10]
0061662C  lea      rcx, [rdi + 0x570]
00616633  call     0x809054  ; -> 00809054 fn
00616638  nop      
00616639  lea      rcx, [rdi + 0x548]
00616640  call     0x16d6a0  ; -> 0016D6A0 fn
00616645  nop      
00616646  lea      rcx, [rdi + 0x520]
0061664D  call     0x16d6a0  ; -> 0016D6A0 fn
00616652  nop      
00616653  cmp      qword ptr [rdi + 0x4f8], 0
0061665B  jne      0x616667  ; -> 00616667
0061665D  cmp      qword ptr [rdi + 0x4e8], 0
00616665  je       0x616674  ; -> 00616674
00616667  lea      rcx, [rdi + 0x4d0]
0061666E  call     0x62b890  ; -> 0062B890 fn
00616673  nop      
00616674  lea      rcx, [rdi + 0x4d0]
0061667B  call     0x5ddb00  ; -> 005DDB00 fn
00616680  nop      
00616681  cmp      qword ptr [rdi + 0x4a8], 0
00616689  jne      0x616695  ; -> 00616695
0061668B  cmp      qword ptr [rdi + 0x498], 0
00616693  je       0x6166a2  ; -> 006166A2
00616695  lea      rcx, [rdi + 0x480]
0061669C  call     0x62b890  ; -> 0062B890 fn
006166A1  nop      
006166A2  lea      rcx, [rdi + 0x480]
006166A9  call     0x5ddb00  ; -> 005DDB00 fn
006166AE  nop      
006166AF  lea      rcx, [rdi + 0x2f8]
006166B6  call     0x5de250  ; -> 005DE250 fn
006166BB  nop      
006166BC  lea      rcx, [rdi + 0x170]
006166C3  call     0x5de250  ; -> 005DE250 fn
006166C8  nop      
006166C9  lea      rcx, [rdi + 0xc8]
006166D0  call     0x16d6a0  ; -> 0016D6A0 fn
006166D5  nop      
006166D6  lea      r9, [rip - 0x4a903d]  ; -> 0016D6A0
006166DD  mov      edx, 0x18
006166E2  lea      r8d, [rdx - 0x10]
006166E6  lea      rcx, [rdi + 8]
006166EA  call     0x809054  ; -> 00809054 fn
006166EF  nop      
006166F0  mov      rbx, qword ptr [rsp + 0x40]
006166F5  add      rsp, 0x30
006166F9  pop      rdi
006166FA  ret      
```

## 0067ACF0 (100 B, extent 0067ACF0-0067AD54)

Documented callee on this page: `0067B100`

```
0067ACF0  mov      qword ptr [rsp + 8], rcx
0067ACF5  push     rdi
0067ACF6  sub      rsp, 0x30
0067ACFA  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0067AD03  mov      qword ptr [rsp + 0x48], rbx
0067AD08  mov      rbx, rcx
0067AD0B  xor      edi, edi
0067AD0D  mov      dword ptr [rcx], edi
0067AD0F  mov      qword ptr [rcx + 8], rdi
0067AD13  mov      eax, dword ptr [rdx + 0x10]
0067AD16  mov      dword ptr [rcx + 0x10], eax
0067AD19  test     eax, eax
0067AD1B  je       0x67ad46  ; -> 0067AD46
0067AD1D  cmp      dword ptr [rdx + 0x10], edi
0067AD20  cmovne   rdi, qword ptr [rdx + 8]
0067AD25  mov      edx, dword ptr [rdx]
0067AD27  btr      edx, 0x1f
0067AD2B  call     0x67b100  ; -> 0067B100 fn
0067AD30  mov      rcx, qword ptr [rbx + 8]
0067AD34  test     rcx, rcx
0067AD37  je       0x67ad46  ; -> 0067AD46
0067AD39  mov      r8d, dword ptr [rbx + 0x10]
0067AD3D  mov      rdx, rdi
0067AD40  call     0x861eba  ; -> 00861EBA fn
0067AD45  nop      
0067AD46  mov      rax, rbx
0067AD49  mov      rbx, qword ptr [rsp + 0x48]
0067AD4E  add      rsp, 0x30
0067AD52  pop      rdi
0067AD53  ret      
```

## 00798AC0 (677 B, extent 00798AC0-00798D65)

Documented callee on this page: `00597A70`

```
00798AC0  push     rbp
00798AC2  push     r14
00798AC4  push     r15
00798AC6  sub      rsp, 0xa0
00798ACD  lea      rbp, [rsp + 0x20]
00798AD2  mov      qword ptr [rbp + 0x10], 0xfffffffffffffffe
00798ADA  mov      qword ptr [rbp + 0xa0], rbx
00798AE1  mov      qword ptr [rbp + 0xa8], rsi
00798AE8  mov      qword ptr [rbp + 0xb0], rdi
00798AEF  mov      qword ptr [rbp + 0xb8], r12
00798AF6  mov      rax, qword ptr [rip + 0x17abd33]  ; -> 01F44830 [u64 0x00002B992DDFA232]
00798AFD  xor      rax, rbp
00798B00  mov      qword ptr [rbp + 0x70], rax
00798B04  mov      rbx, rcx
00798B07  or       r8, 0xffffffffffffffff
00798B0B  nop      dword ptr [rax + rax]
00798B10  inc      r8
00798B13  cmp      byte ptr [rdx + r8], 0
00798B18  jne      0x798b10  ; -> 00798B10
00798B1A  inc      r8
00798B1D  lea      rax, [r8 + 0xf]
00798B21  cmp      rax, r8
00798B24  ja       0x798b30  ; -> 00798B30
00798B26  movabs   rax, 0xffffffffffffff0
00798B30  and      rax, 0xfffffffffffffff0
00798B34  call     0x808f10  ; -> 00808F10 fn
00798B39  sub      rsp, rax
00798B3C  lea      r14, [rsp + 0x20]
00798B41  mov      rcx, r14
00798B44  call     0x861eba  ; -> 00861EBA fn
00798B49  mov      rax, r14
00798B4C  cmp      byte ptr [r14], 0
00798B50  je       0x798b67  ; -> 00798B67
00798B52  lea      rax, [rax + 1]
00798B56  movzx    ecx, byte ptr [rax]
00798B59  cmp      cl, 0x2c
00798B5C  je       0x798b64  ; -> 00798B64
00798B5E  test     cl, cl
00798B60  jne      0x798b52  ; -> 00798B52
00798B62  jmp      0x798b67  ; -> 00798B67
00798B64  mov      byte ptr [rax], 0
00798B67  test     rbx, rbx
00798B6A  je       0x798d2e  ; -> 00798D2E
00798B70  mov      r8, r14
00798B73  lea      rdx, [rip + 0x151a046]  ; -> 01CB2BC0
00798B7A  mov      ecx, 2
00798B7F  call     0x5cdaa0  ; -> 005CDAA0 fn
00798B84  mov      rax, qword ptr [rbx + 0xe8]
00798B8B  lea      rcx, [rbx + 0xe8]
00798B92  call     qword ptr [rax + 0x10]
00798B95  lea      rcx, [rbx + 0xe8]
00798B9C  call     0x610330  ; -> 00610330 fn
00798BA1  xor      r12d, r12d
00798BA4  mov      dword ptr [rbp + 8], r12d
00798BA8  mov      dword ptr [rbp + 4], r12d
00798BAC  mov      dword ptr [rbp + 0xc], r12d
00798BB0  lea      rcx, [rbp]
00798BB4  call     0x615bc0  ; -> 00615BC0 fn
00798BB9  nop      
00798BBA  lea      rcx, [rbp]
00798BBE  call     0x624670  ; -> 00624670 fn
00798BC3  lea      r9, [rbp + 0xc]
00798BC7  lea      r8, [rbp + 4]
00798BCB  lea      rdx, [rbp + 8]
00798BCF  mov      rcx, rax
00798BD2  call     0x624960  ; -> 00624960 fn
00798BD7  mov      ebx, eax
00798BD9  lea      rcx, [rbp]
00798BDD  call     0x616700  ; -> 00616700 fn
00798BE2  test     ebx, ebx
00798BE4  jne      0x798d2a  ; -> 00798D2A
00798BEA  mov      esi, dword ptr [rbp + 0xc]
00798BED  imul     esi, dword ptr [rbp + 4]
00798BF1  add      esi, 0x38
00798BF4  movsxd   rcx, esi
00798BF7  lea      edx, [rbx + 4]
00798BFA  call     0x17d260  ; -> 0017D260 fn
00798BFF  mov      rdi, rax
00798C02  mov      r15, rax
00798C05  test     rax, rax
00798C08  je       0x798d25  ; -> 00798D25
00798C0E  add      rdi, 2
00798C12  lea      rcx, [rbp]
00798C16  call     0x615bc0  ; -> 00615BC0 fn
00798C1B  nop      
00798C1C  lea      rcx, [rbp]
00798C20  call     0x624670  ; -> 00624670 fn
00798C25  lea      rdx, [rdi + 0x36]
00798C29  mov      rcx, rax
00798C2C  call     0x61ee30  ; -> 0061EE30 fn
00798C31  mov      ebx, eax
00798C33  lea      rcx, [rbp]
00798C37  call     0x616700  ; -> 00616700 fn
00798C3C  test     ebx, ebx
00798C3E  jne      0x798d17  ; -> 00798D17
00798C44  mov      r9d, r12d
00798C47  mov      edx, dword ptr [rbp + 4]
00798C4A  test     edx, edx
00798C4C  je       0x798c96  ; -> 00798C96
00798C4E  mov      ecx, dword ptr [rbp + 8]
00798C51  mov      eax, r9d
00798C54  imul     eax, dword ptr [rbp + 0xc]
00798C58  add      rax, 0x36
00798C5C  add      rax, rdi
00798C5F  mov      r8d, r12d
00798C62  test     ecx, ecx
00798C64  je       0x798c8e  ; -> 00798C8E
00798C66  nop      word ptr [rax + rax]
00798C70  movzx    edx, byte ptr [rax]
00798C73  movzx    ecx, byte ptr [rax + 2]
00798C77  mov      byte ptr [rax], cl
00798C79  mov      byte ptr [rax + 2], dl
00798C7C  lea      rax, [rax + 3]
00798C80  inc      r8d
00798C83  mov      ecx, dword ptr [rbp + 8]
00798C86  cmp      r8d, ecx
00798C89  jb       0x798c70  ; -> 00798C70
00798C8B  mov      edx, dword ptr [rbp + 4]
00798C8E  inc      r9d
00798C91  cmp      r9d, edx
00798C94  jb       0x798c51  ; -> 00798C51
00798C96  mov      word ptr [rdi], 0x4d42
00798C9B  mov      qword ptr [rdi + 2], r12
00798C9F  mov      dword ptr [rdi + 0xa], 0x36
00798CA6  mov      dword ptr [rdi + 0xe], 0x28
00798CAD  mov      eax, dword ptr [rbp + 8]
00798CB0  mov      dword ptr [rdi + 0x12], eax
00798CB3  mov      eax, dword ptr [rbp + 4]
00798CB6  mov      dword ptr [rdi + 0x16], eax
00798CB9  mov      qword ptr [rdi + 0x1a], 0x180001
00798CC1  mov      qword ptr [rdi + 0x22], r12
00798CC5  mov      qword ptr [rdi + 0x2a], r12
00798CC9  mov      dword ptr [rdi + 0x32], r12d
00798CCD  mov      rdx, r14
00798CD0  lea      rcx, [rbp + 0x20]
00798CD4  call     0x597a70  ; -> 00597A70 fn
00798CD9  nop      
00798CDA  lea      rcx, [rbp + 0x20]
00798CDE  call     0x59d920  ; -> 0059D920 fn
00798CE3  test     al, al
00798CE5  je       0x798d01  ; -> 00798D01
00798CE7  mov      r8d, esi
00798CEA  mov      rdx, rdi
00798CED  lea      rcx, [rbp + 0x20]
00798CF1  call     0x59f450  ; -> 0059F450 fn
00798CF6  test     eax, eax
00798CF8  je       0x798d04  ; -> 00798D04
00798CFA  mov      ebx, 9
00798CFF  jmp      0x798d04  ; -> 00798D04
00798D01  mov      ebx, dword ptr [rbp + 0x28]
00798D04  lea      rcx, [rbp + 0x20]
00798D08  call     0x59bd40  ; -> 0059BD40 fn
00798D0D  nop      
00798D0E  lea      rcx, [rbp + 0x20]
00798D12  call     0x598140  ; -> 00598140 fn
00798D17  mov      rcx, r15
00798D1A  call     0x584730  ; -> 00584730 fn
00798D1F  test     ebx, ebx
00798D21  jne      0x798d2a  ; -> 00798D2A
00798D23  jmp      0x798d2e  ; -> 00798D2E
00798D25  mov      ebx, 0xd
00798D2A  mov      eax, ebx
00798D2C  jmp      0x798d30  ; -> 00798D30
00798D2E  xor      eax, eax
00798D30  mov      rcx, qword ptr [rbp + 0x70]
00798D34  xor      rcx, rbp
00798D37  call     0x808c40  ; -> 00808C40 fn
00798D3C  mov      rbx, qword ptr [rbp + 0xa0]
00798D43  mov      rsi, qword ptr [rbp + 0xa8]
00798D4A  mov      rdi, qword ptr [rbp + 0xb0]
00798D51  mov      r12, qword ptr [rbp + 0xb8]
00798D58  lea      rsp, [rbp + 0x80]
00798D5F  pop      r15
00798D61  pop      r14
00798D63  pop      rbp
00798D64  ret      
```
