# F homing pack: `18-Audio/Audio-Bank-And-Controller-Family/audio-bank-and-controller-family.md`

Generated 2026-10-02 21:45 by OPUS (homing_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 5. No bearing page cites them and no documented function calls them directly.

## 0021B2F0 (91 B, extent 0021B2F0-0021B34B)

Documented callee on this page: `00222170`

```
0021B2F0  mov      qword ptr [rsp + 8], rbx
0021B2F5  mov      qword ptr [rsp + 0x10], rsi
0021B2FA  push     rdi
0021B2FB  sub      rsp, 0x20
0021B2FF  mov      rbx, qword ptr [rcx + 8]
0021B303  lea      rdi, [rcx + 8]
0021B307  mov      esi, edx
0021B309  cmp      rbx, rdi
0021B30C  je       0x21b327  ; -> 0021B327
0021B30E  nop      
0021B310  mov      rcx, qword ptr [rbx + 0x10]
0021B314  mov      edx, esi
0021B316  call     0x222170  ; -> 00222170 fn
0021B31B  test     al, al
0021B31D  jne      0x21b339  ; -> 0021B339
0021B31F  mov      rbx, qword ptr [rbx]
0021B322  cmp      rbx, rdi
0021B325  jne      0x21b310  ; -> 0021B310
0021B327  xor      al, al
0021B329  mov      rbx, qword ptr [rsp + 0x30]
0021B32E  mov      rsi, qword ptr [rsp + 0x38]
0021B333  add      rsp, 0x20
0021B337  pop      rdi
0021B338  ret      
0021B339  mov      rbx, qword ptr [rsp + 0x30]
0021B33E  mov      al, 1
0021B340  mov      rsi, qword ptr [rsp + 0x38]
0021B345  add      rsp, 0x20
0021B349  pop      rdi
0021B34A  ret      
```

## 00222B20 (70 B, extent 00222B20-00222B66)

Documented callee on this page: `007A81F0`

```
00222B20  mov      qword ptr [rsp + 8], rbx
00222B25  push     rdi
00222B26  sub      rsp, 0x20
00222B2A  lea      rbx, [rcx + 0x38]
00222B2E  mov      edi, r8d
00222B31  mov      rcx, rbx
00222B34  call     0x7a7010  ; -> 007A7010 fn
00222B39  test     eax, eax
00222B3B  je       0x222b5b  ; -> 00222B5B
00222B3D  movd     xmm1, edi
00222B41  or       r9d, 0xffffffff
00222B45  cvtdq2ps xmm1, xmm1
00222B48  mov      rcx, rbx
00222B4B  xorps    xmm2, xmm2
00222B4E  divss    xmm1, dword ptr [rip + 0x6e3eee]  ; -> 00906A44 [f32 127]
00222B56  call     0x7a81f0  ; -> 007A81F0 fn
00222B5B  mov      rbx, qword ptr [rsp + 0x30]
00222B60  add      rsp, 0x20
00222B64  pop      rdi
00222B65  ret      
```

## 00223320 (110 B, extent 00223320-0022338E)

Documented callee on this page: `002224F0`

```
00223320  mov      qword ptr [rsp + 8], rbx
00223325  push     rdi
00223326  sub      rsp, 0x20
0022332A  mov      edi, r9d
0022332D  test     edx, edx
0022332F  je       0x223364  ; -> 00223364
00223331  call     0x221ed0  ; -> 00221ED0 fn
00223336  mov      rbx, rax
00223339  test     rax, rax
0022333C  je       0x223381  ; -> 00223381
0022333E  mov      rcx, rax
00223341  call     0x225680  ; -> 00225680 fn
00223346  test     eax, eax
00223348  je       0x223381  ; -> 00223381
0022334A  xor      r8d, r8d
0022334D  mov      edx, edi
0022334F  mov      rcx, rbx
00223352  call     0x2257e0  ; -> 002257E0 fn
00223357  mov      al, 1
00223359  mov      rbx, qword ptr [rsp + 0x30]
0022335E  add      rsp, 0x20
00223362  pop      rdi
00223363  ret      
00223364  cmp      dword ptr [rcx + 0x38], r8d
00223368  jne      0x223381  ; -> 00223381
0022336A  xor      r8d, r8d
0022336D  mov      edx, edi
0022336F  call     0x2224f0  ; -> 002224F0 fn
00223374  mov      al, 1
00223376  mov      rbx, qword ptr [rsp + 0x30]
0022337B  add      rsp, 0x20
0022337F  pop      rdi
00223380  ret      
00223381  xor      al, al
00223383  mov      rbx, qword ptr [rsp + 0x30]
00223388  add      rsp, 0x20
0022338C  pop      rdi
0022338D  ret      
```

## 00223390 (122 B, extent 00223390-0022340A)

Documented callee on this page: `002225B0`

```
00223390  mov      qword ptr [rsp + 8], rbx
00223395  push     rdi
00223396  sub      rsp, 0x20
0022339A  mov      edi, r9d
0022339D  test     edx, edx
0022339F  je       0x2233e3  ; -> 002233E3
002233A1  call     0x221ed0  ; -> 00221ED0 fn
002233A6  mov      rbx, rax
002233A9  test     rax, rax
002233AC  je       0x2233fd  ; -> 002233FD
002233AE  mov      rcx, rax
002233B1  call     0x225680  ; -> 00225680 fn
002233B6  test     eax, eax
002233B8  je       0x2233fd  ; -> 002233FD
002233BA  movd     xmm1, edi
002233BE  lea      rcx, [rbx + 8]
002233C2  cvtdq2ps xmm1, xmm1
002233C5  or       r8d, 0xffffffff
002233C9  divss    xmm1, dword ptr [rip + 0x6d3983]  ; -> 008F6D54 [f32 60]
002233D1  call     0x7a84a0  ; -> 007A84A0 fn
002233D6  mov      al, 1
002233D8  mov      rbx, qword ptr [rsp + 0x30]
002233DD  add      rsp, 0x20
002233E1  pop      rdi
002233E2  ret      
002233E3  cmp      dword ptr [rcx + 0x38], r8d
002233E7  jne      0x2233fd  ; -> 002233FD
002233E9  mov      edx, edi
002233EB  call     0x2225b0  ; -> 002225B0 fn
002233F0  mov      al, 1
002233F2  mov      rbx, qword ptr [rsp + 0x30]
002233F7  add      rsp, 0x20
002233FB  pop      rdi
002233FC  ret      
002233FD  xor      al, al
002233FF  mov      rbx, qword ptr [rsp + 0x30]
00223404  add      rsp, 0x20
00223408  pop      rdi
00223409  ret      
```

## 00223410 (114 B, extent 00223410-00223482)

Documented callee on this page: `002224F0`

```
00223410  mov      qword ptr [rsp + 8], rbx
00223415  push     rdi
00223416  sub      rsp, 0x20
0022341A  mov      edi, r9d
0022341D  test     edx, edx
0022341F  je       0x223456  ; -> 00223456
00223421  call     0x221ed0  ; -> 00221ED0 fn
00223426  mov      rbx, rax
00223429  test     rax, rax
0022342C  je       0x223475  ; -> 00223475
0022342E  mov      rcx, rax
00223431  call     0x225680  ; -> 00225680 fn
00223436  test     eax, eax
00223438  je       0x223475  ; -> 00223475
0022343A  mov      edx, dword ptr [rsp + 0x50]
0022343E  mov      r8d, edi
00223441  mov      rcx, rbx
00223444  call     0x2257e0  ; -> 002257E0 fn
00223449  mov      al, 1
0022344B  mov      rbx, qword ptr [rsp + 0x30]
00223450  add      rsp, 0x20
00223454  pop      rdi
00223455  ret      
00223456  cmp      dword ptr [rcx + 0x38], r8d
0022345A  jne      0x223475  ; -> 00223475
0022345C  mov      edx, dword ptr [rsp + 0x50]
00223460  mov      r8d, edi
00223463  call     0x2224f0  ; -> 002224F0 fn
00223468  mov      al, 1
0022346A  mov      rbx, qword ptr [rsp + 0x30]
0022346F  add      rsp, 0x20
00223473  pop      rdi
00223474  ret      
00223475  xor      al, al
00223477  mov      rbx, qword ptr [rsp + 0x30]
0022347C  add      rsp, 0x20
00223480  pop      rdi
00223481  ret      
```
