# F homing pack (FABLE): `17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 4. No bearing page cites them and no documented function calls them directly.

## 002E4FE0 (74 B, extent 002E4FE0-002E502A)

Documented callee on this page: `00427300`

```
002E4FE0  sub      rsp, 0x28
002E4FE4  test     rcx, rcx
002E4FE7  je       0x2e5023  ; -> 002E5023
002E4FE9  cmp      dword ptr [rcx], -1
002E4FEC  je       0x2e5023  ; -> 002E5023
002E4FEE  movzx    eax, word ptr [rcx]
002E4FF1  cmp      ax, -1
002E4FF5  je       0x2e5019  ; -> 002E5019
002E4FF7  movsx    rax, ax
002E4FFB  imul     rcx, rax, 0x740
002E5002  add      rcx, qword ptr [rip + 0x1fe1f1f]  ; -> 022C6F28
002E5009  je       0x2e5019  ; -> 002E5019
002E500B  cmp      dword ptr [rcx + 0x284], 0
002E5012  je       0x2e5019  ; -> 002E5019
002E5014  call     0x427300  ; -> 00427300 fn
002E5019  mov      eax, 1
002E501E  add      rsp, 0x28
002E5022  ret      
002E5023  xor      eax, eax
002E5025  add      rsp, 0x28
002E5029  ret      
```

## 0034C4B0 (73 B, extent 0034C4B0-0034C4F9)

Documented callee on this page: `002E87F0`

```
0034C4B0  mov      qword ptr [rsp + 8], rbx
0034C4B5  push     rdi
0034C4B6  sub      rsp, 0x20
0034C4BA  mov      rcx, r9
0034C4BD  mov      rbx, r9
0034C4C0  call     0x267e10  ; -> 00267E10 fn
0034C4C5  mov      rcx, rbx
0034C4C8  mov      edi, eax
0034C4CA  call     0x267e10  ; -> 00267E10 fn
0034C4CF  mov      ecx, eax
0034C4D1  mov      ebx, eax
0034C4D3  call     0x16d6a0  ; -> 0016D6A0 fn
0034C4D8  mov      ecx, ebx
0034C4DA  call     0x3eb720  ; -> 003EB720 fn
0034C4DF  test     rax, rax
0034C4E2  je       0x34c4ee  ; -> 0034C4EE
0034C4E4  mov      edx, edi
0034C4E6  mov      rcx, rax
0034C4E9  call     0x2e87f0  ; -> 002E87F0 fn
0034C4EE  mov      rbx, qword ptr [rsp + 0x30]
0034C4F3  add      rsp, 0x20
0034C4F7  pop      rdi
0034C4F8  ret      
```

## 003EB250 (533 B, extent 003EB250-003EB465)

Documented callee on this page: `00427300`

```
003EB250  push     rbx
003EB252  sub      rsp, 0x30
003EB256  mov      rbx, qword ptr [rip + 0x2773913]  ; -> 02B5EB70
003EB25D  mov      r11d, r8d
003EB260  test     rcx, rcx
003EB263  je       0x3eb45c  ; -> 003EB45C
003EB269  test     rbx, rbx
003EB26C  je       0x3eb45c  ; -> 003EB45C
003EB272  mov      r10, qword ptr [rbx]
003EB275  mov      rax, qword ptr [rbx + 8]
003EB279  mov      qword ptr [rsp + 0x40], rsi
003EB27E  mov      qword ptr [rsp + 0x48], rdi
003EB283  test     r10, r10
003EB286  je       0x3eb28c  ; -> 003EB28C
003EB288  mov      qword ptr [r10 + 8], rax
003EB28C  test     rax, rax
003EB28F  je       0x3eb294  ; -> 003EB294
003EB291  mov      qword ptr [rax], r10
003EB294  xor      esi, esi
003EB296  mov      qword ptr [rbx], rsi
003EB299  mov      qword ptr [rbx + 8], rsi
003EB29D  mov      rax, qword ptr [rip + 0x277387c]  ; -> 02B5EB20
003EB2A4  mov      qword ptr [rip + 0x2773875], rbx  ; -> 02B5EB20
003EB2AB  test     rax, rax
003EB2AE  je       0x3eb2b4  ; -> 003EB2B4
003EB2B0  mov      qword ptr [rax + 8], rbx
003EB2B4  mov      byte ptr [rbx + 0x41], dl
003EB2B7  lea      r8, [rip + 0x2773862]  ; -> 02B5EB20
003EB2BE  mov      qword ptr [rbx + 8], r8
003EB2C2  mov      edx, r11d
003EB2C5  mov      qword ptr [rbx], rax
003EB2C8  mov      r8d, r9d
003EB2CB  mov      byte ptr [rbx + 0x40], 1
003EB2CF  mov      qword ptr [rbx + 0x18], rcx
003EB2D3  inc      word ptr [rcx + 0x1c]
003EB2D7  and      byte ptr [rcx + 0x18], 0xfb
003EB2DB  mov      eax, dword ptr [rcx + 0x14]
003EB2DE  mov      dword ptr [rip + 0x1b94224], eax  ; -> 01F7F508
003EB2E4  mov      ecx, dword ptr [rcx + 0x10]
003EB2E7  call     0x2ed4e0  ; -> 002ED4E0 fn
003EB2EC  mov      dword ptr [rbx + 0x10], eax
003EB2EF  mov      dword ptr [rip + 0x1b94213], esi  ; -> 01F7F508
003EB2F5  movzx    eax, word ptr [rbx + 0x10]
003EB2F9  cmp      ax, -1
003EB2FD  je       0x3eb322  ; -> 003EB322
003EB2FF  movsx    rax, ax
003EB303  imul     rcx, rax, 0x740
003EB30A  add      rcx, qword ptr [rip + 0x1edbc17]  ; -> 022C6F28
003EB311  je       0x3eb322  ; -> 003EB322
003EB313  cmp      dword ptr [rcx + 0x284], esi
003EB319  je       0x3eb322  ; -> 003EB322
003EB31B  mov      qword ptr [rcx + 0x108], rsi
003EB322  movzx    eax, word ptr [rbx + 0x10]
003EB326  mov      rsi, qword ptr [rsp + 0x40]
003EB32B  cmp      ax, -1
003EB32F  je       0x3eb355  ; -> 003EB355
003EB331  movsx    rax, ax
003EB335  imul     rcx, rax, 0x740
003EB33C  add      rcx, qword ptr [rip + 0x1edbbe5]  ; -> 022C6F28
003EB343  je       0x3eb355  ; -> 003EB355
003EB345  cmp      dword ptr [rcx + 0x284], 0
003EB34C  je       0x3eb355  ; -> 003EB355
003EB34E  xor      edx, edx
003EB350  call     0x3e5e20  ; -> 003E5E20 fn
003EB355  movzx    eax, word ptr [rbx + 0x10]
003EB359  cmp      ax, -1
003EB35D  je       0x3eb383  ; -> 003EB383
003EB35F  movsx    rax, ax
003EB363  imul     rcx, rax, 0x740
003EB36A  add      rcx, qword ptr [rip + 0x1edbbb7]  ; -> 022C6F28
003EB371  je       0x3eb383  ; -> 003EB383
003EB373  cmp      dword ptr [rcx + 0x284], 0
003EB37A  je       0x3eb383  ; -> 003EB383
003EB37C  mov      byte ptr [rcx + 0x413], 0
003EB383  movzx    eax, word ptr [rbx + 0x10]
003EB387  movaps   xmmword ptr [rsp + 0x20], xmm6
003EB38C  cmp      ax, -1
003EB390  jne      0x3eb39c  ; -> 003EB39C
003EB392  movss    xmm6, dword ptr [rip + 0x50d9e6]  ; -> 008F8D80 [f32 30]
003EB39A  jmp      0x3eb3d5  ; -> 003EB3D5
003EB39C  movsx    rax, ax
003EB3A0  imul     rcx, rax, 0x740
003EB3A7  add      rcx, qword ptr [rip + 0x1edbb7a]  ; -> 022C6F28
003EB3AE  jne      0x3eb3ba  ; -> 003EB3BA
003EB3B0  movss    xmm6, dword ptr [rip + 0x50d9c8]  ; -> 008F8D80 [f32 30]
003EB3B8  jmp      0x3eb3d5  ; -> 003EB3D5
003EB3BA  cmp      dword ptr [rcx + 0x284], 0
003EB3C1  jne      0x3eb3cd  ; -> 003EB3CD
003EB3C3  movss    xmm6, dword ptr [rip + 0x50d9b5]  ; -> 008F8D80 [f32 30]
003EB3CB  jmp      0x3eb3d5  ; -> 003EB3D5
003EB3CD  call     0x423280  ; -> 00423280 fn
003EB3D2  movaps   xmm6, xmm0
003EB3D5  xor      edx, edx
003EB3D7  lea      rcx, [rbx + 0x10]
003EB3DB  call     0x2e8340  ; -> 002E8340 fn
003EB3E0  movss    xmm1, dword ptr [rip + 0x19007c0]  ; -> 01CEBBA8 [f32 1]
003EB3E8  movzx    ecx, word ptr [rbx + 0x10]
003EB3EC  movaps   xmm3, xmm1
003EB3EF  movaps   xmm2, xmm1
003EB3F2  call     0x2ee050  ; -> 002EE050 fn
003EB3F7  movzx    eax, word ptr [rbx + 0x10]
003EB3FB  cmp      ax, -1
003EB3FF  je       0x3eb426  ; -> 003EB426
003EB401  movsx    rax, ax
003EB405  imul     rcx, rax, 0x740
003EB40C  add      rcx, qword ptr [rip + 0x1edbb15]  ; -> 022C6F28
003EB413  je       0x3eb426  ; -> 003EB426
003EB415  cmp      dword ptr [rcx + 0x284], 0
003EB41C  je       0x3eb426  ; -> 003EB426
003EB41E  movaps   xmm1, xmm6
003EB421  call     0x427300  ; -> 00427300 fn
003EB426  movzx    eax, word ptr [rbx + 0x10]
003EB42A  movaps   xmm6, xmmword ptr [rsp + 0x20]
003EB42F  mov      rdi, qword ptr [rsp + 0x48]
003EB434  cmp      ax, -1
003EB438  je       0x3eb45c  ; -> 003EB45C
003EB43A  movsx    rcx, ax
003EB43E  imul     rcx, rcx, 0x740
003EB445  add      rcx, qword ptr [rip + 0x1edbadc]  ; -> 022C6F28
003EB44C  je       0x3eb45c  ; -> 003EB45C
003EB44E  cmp      dword ptr [rcx + 0x284], 0
003EB455  je       0x3eb45c  ; -> 003EB45C
003EB457  call     0x426e20  ; -> 00426E20 fn
003EB45C  mov      rax, rbx
003EB45F  add      rsp, 0x30
003EB463  pop      rbx
003EB464  ret      
```

## 003EB910 (37 B, extent 003EB910-003EB935)

Documented callee on this page: `003EC260`

```
003EB910  sub      rsp, 0x38
003EB914  test     rcx, rcx
003EB917  je       0x3eb930  ; -> 003EB930
003EB919  cmp      dword ptr [rcx + 0x10], 0
003EB91D  jl       0x3eb930  ; -> 003EB930
003EB91F  movzx    ecx, word ptr [rcx + 0x10]
003EB923  mov      dword ptr [rsp + 0x20], 1
003EB92B  call     0x3ec260  ; -> 003EC260 fn
003EB930  add      rsp, 0x38
003EB934  ret      
```
