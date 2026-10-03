# F homing pack (FABLE): `17-Presentation-Rendering/Scripted-Camera/the-scripted-camera-player.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 5. No bearing page cites them and no documented function calls them directly.

## 002565C0 (144 B, extent 002565C0-00256650)

Documented callee on this page: `002593A0`

```
002565C0  sub      rsp, 0x28
002565C4  call     0x2593a0  ; -> 002593A0 fn
002565C9  movss    xmm2, dword ptr [rax + 0x90]
002565D1  movss    xmm1, dword ptr [rax + 0xa0]
002565D9  ucomiss  xmm2, xmm1
002565DC  jp       0x2565fa  ; -> 002565FA
002565DE  jne      0x2565fa  ; -> 002565FA
002565E0  movss    xmm0, dword ptr [rax + 0x98]
002565E8  ucomiss  xmm0, dword ptr [rax + 0xa8]
002565EF  jp       0x2565fa  ; -> 002565FA
002565F1  jne      0x2565fa  ; -> 002565FA
002565F3  xor      eax, eax
002565F5  add      rsp, 0x28
002565F9  ret      
002565FA  subss    xmm2, xmm1
002565FE  movss    xmm1, dword ptr [rax + 0x98]
00256606  subss    xmm1, dword ptr [rax + 0xa8]
0025660E  movaps   xmm0, xmm2
00256611  call     0x861f02  ; -> 00861F02 fn
00256616  addss    xmm0, dword ptr [rip + 0x6beff2]  ; -> 00915610 [f32 0.3926991]
0025661E  movss    xmm2, dword ptr [rip + 0x1a95652]  ; -> 01CEBC78 [f32 6.283185]
00256626  xorps    xmm1, xmm1
00256629  comiss   xmm1, xmm0
0025662C  jbe      0x256632  ; -> 00256632
0025662E  addss    xmm0, xmm2
00256632  comiss   xmm0, xmm2
00256635  jbe      0x25663f  ; -> 0025663F
00256637  addss    xmm0, dword ptr [rip + 0x6befe5]  ; -> 00915624 [f32 -6.283185]
0025663F  divss    xmm0, dword ptr [rip + 0x6befcd]  ; -> 00915614 [f32 0.7853982]
00256647  cvttss2si eax, xmm0
0025664B  add      rsp, 0x28
0025664F  ret      
```

## 0027B3B0 (121 B, extent 0027B3B0-0027B429)

Documented callee on this page: `002E9D10`

```
0027B3B0  mov      r11, rsp
0027B3B3  push     rbx
0027B3B4  sub      rsp, 0x60
0027B3B8  mov      rax, qword ptr [rip + 0x1cc9471]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0027B3BF  xor      rax, rsp
0027B3C2  mov      qword ptr [rsp + 0x50], rax
0027B3C7  xor      eax, eax
0027B3C9  mov      ebx, edx
0027B3CB  lea      rdx, [r11 - 0x38]
0027B3CF  mov      qword ptr [r11 - 0x38], rax
0027B3D3  mov      qword ptr [r11 - 0x30], rax
0027B3D7  mov      qword ptr [r11 - 0x48], rax
0027B3DB  mov      qword ptr [r11 - 0x40], rax
0027B3DF  mov      qword ptr [r11 - 0x28], rax
0027B3E3  mov      qword ptr [r11 - 0x20], rax
0027B3E7  call     0x2e9d10  ; -> 002E9D10 fn
0027B3EC  lea      rdx, [rsp + 0x20]
0027B3F1  mov      ecx, ebx
0027B3F3  call     0x2e9d10  ; -> 002E9D10 fn
0027B3F8  lea      r8, [rsp + 0x20]
0027B3FD  lea      rdx, [rsp + 0x30]
0027B402  lea      rcx, [rsp + 0x40]
0027B407  call     0x203080  ; -> 00203080 fn
0027B40C  lea      rcx, [rsp + 0x40]
0027B411  call     0x2703f0  ; -> 002703F0 fn
0027B416  mov      rcx, qword ptr [rsp + 0x50]
0027B41B  xor      rcx, rsp
0027B41E  call     0x808c40  ; -> 00808C40 fn
0027B423  add      rsp, 0x60
0027B427  pop      rbx
0027B428  ret      
```

## 00373380 (444 B, extent 00373380-0037353C)

Documented callee on this page: `00409270`

```
00373380  mov      qword ptr [rsp + 0x10], rbx
00373385  mov      qword ptr [rsp + 0x18], rbp
0037338A  push     rsi
0037338B  push     rdi
0037338C  push     r13
0037338E  push     r14
00373390  push     r15
00373392  sub      rsp, 0x20
00373396  or       r13d, 0xffffffff
0037339A  xor      ebp, ebp
0037339C  mov      r14, rdx
0037339F  mov      r15, rcx
003733A2  test     rdx, rdx
003733A5  je       0x37344c  ; -> 0037344C
003733AB  mov      eax, dword ptr [rcx + 4]
003733AE  cmp      dword ptr [rdx + 0x10], eax
003733B1  jne      0x37344c  ; -> 0037344C
003733B7  mov      ecx, dword ptr [rdx + 0x84]
003733BD  mov      qword ptr [rsp + 0x50], r12
003733C2  mov      dword ptr [rdx + 0x10], r13d
003733C6  call     0x20e600  ; -> 0020E600 fn
003733CB  mov      ecx, dword ptr [r14 + 0x84]
003733D2  mov      r12, rax
003733D5  call     0x20e600  ; -> 0020E600 fn
003733DA  movsx    rcx, word ptr [r14 + 0x88]
003733E2  mov      edi, ebp
003733E4  imul     rsi, rcx, 0x290
003733EB  add      rsi, rax
003733EE  cmp      bp, word ptr [r14 + 0x8a]
003733F6  jge      0x373447  ; -> 00373447
003733F8  nop      dword ptr [rax + rax]
00373400  movsx    rcx, word ptr [rsi]
00373404  imul     rbx, rcx, 0x290
0037340B  mov      ecx, dword ptr [rbx + r12 + 0x278]
00373413  call     0x20e600  ; -> 0020E600 fn
00373418  test     rax, rax
0037341B  je       0x373435  ; -> 00373435
0037341D  xor      ecx, ecx
0037341F  call     0x20e620  ; -> 0020E620 fn
00373424  mov      dword ptr [rbx + r12 + 0x278], eax
0037342C  mov      word ptr [rbx + r12 + 0x27c], r13w
00373435  movsx    eax, word ptr [r14 + 0x8a]
0037343D  inc      edi
0037343F  add      rsi, 2
00373443  cmp      edi, eax
00373445  jl       0x373400  ; -> 00373400
00373447  mov      r12, qword ptr [rsp + 0x50]
0037344C  mov      ecx, dword ptr [r15 + 0x84]
00373453  mov      dword ptr [r15 + 8], r13d
00373457  mov      word ptr [r15 + 0x14], r13w
0037345C  call     0x20e600  ; -> 0020E600 fn
00373461  mov      ecx, dword ptr [r15 + 0x84]
00373468  mov      rsi, rax
0037346B  call     0x20e600  ; -> 0020E600 fn
00373470  movsx    rcx, word ptr [r15 + 0x88]
00373478  imul     rdi, rcx, 0x290
0037347F  lea      rcx, [rsi + 0x1f0]
00373486  add      rdi, rax
00373489  call     0x46d110  ; -> 0046D110 fn
0037348E  mov      ecx, dword ptr [r15 + 0xa0]
00373495  call     0x20e600  ; -> 0020E600 fn
0037349A  mov      r14, rax
0037349D  test     rax, rax
003734A0  je       0x373525  ; -> 00373525
003734A6  cmp      bp, word ptr [r15 + 0x8a]
003734AE  jge      0x373525  ; -> 00373525
003734B0  movsx    rax, word ptr [rdi]
003734B4  imul     rbx, rax, 0x290
003734BB  add      rbx, rsi
003734BE  and      word ptr [rbx + 0x280], 0xfffd
003734C6  mov      ecx, dword ptr [r15 + 0xa0]
003734CD  call     0x20e600  ; -> 0020E600 fn
003734D2  test     rax, rax
003734D5  je       0x373513  ; -> 00373513
003734D7  movsx    edx, word ptr [rbx + 0x27e]
003734DE  mov      rcx, r14
003734E1  call     0x409270  ; -> 00409270 fn
003734E6  mov      ecx, dword ptr [rax]
003734E8  mov      eax, ecx
003734EA  and      eax, 0xfff000
003734EF  cmp      eax, 0xfff000
003734F4  jne      0x3734fb  ; -> 003734FB
003734F6  or       ecx, 0xffffffff
003734F9  jmp      0x373504  ; -> 00373504
003734FB  shr      ecx, 0xc
003734FE  and      ecx, 0xfff
00373504  mov      word ptr [rbx + 0x270], cx
0037350B  mov      word ptr [rbx + 0x276], r13w
00373513  movsx    eax, word ptr [r15 + 0x8a]
0037351B  inc      ebp
0037351D  add      rdi, 2
00373521  cmp      ebp, eax
00373523  jl       0x3734b0  ; -> 003734B0
00373525  mov      rbx, qword ptr [rsp + 0x58]
0037352A  mov      rbp, qword ptr [rsp + 0x60]
0037352F  add      rsp, 0x20
00373533  pop      r15
00373535  pop      r14
00373537  pop      r13
00373539  pop      rdi
0037353A  pop      rsi
0037353B  ret      
```

## 0042D9C0 (61 B, extent 0042D9C0-0042D9FD)

Documented callee on this page: `00421D70`

```
0042D9C0  mov      qword ptr [rsp + 8], rbx
0042D9C5  push     rdi
0042D9C6  sub      rsp, 0x20
0042D9CA  mov      rbx, rdx
0042D9CD  mov      rdi, rcx
0042D9D0  movzx    edx, word ptr [rdx + 0x1c]
0042D9D4  call     0x421d70  ; -> 00421D70 fn
0042D9D9  mov      ecx, 0xffff
0042D9DE  cmp      cx, ax
0042D9E1  je       0x42d9f2  ; -> 0042D9F2
0042D9E3  mov      qword ptr [rbx + 0x20], rdi
0042D9E7  mov      word ptr [rbx + 0x28], ax
0042D9EB  mov      dword ptr [rbx + 0x18], 1
0042D9F2  mov      rbx, qword ptr [rsp + 0x30]
0042D9F7  add      rsp, 0x20
0042D9FB  pop      rdi
0042D9FC  ret      
```

## 0050D540 (38 B, extent 0050D540-0050D566)

Documented callee on this page: `00377DB0`

```
0050D540  sub      rsp, 0x28
0050D544  call     0x377db0  ; -> 00377DB0 fn
0050D549  test     eax, eax
0050D54B  jne      0x50d55f  ; -> 0050D55F
0050D54D  lea      ecx, [rax + 1]
0050D550  call     0x314d40  ; -> 00314D40 fn
0050D555  mov      eax, 1
0050D55A  add      rsp, 0x28
0050D55E  ret      
0050D55F  xor      eax, eax
0050D561  add      rsp, 0x28
0050D565  ret      
```
