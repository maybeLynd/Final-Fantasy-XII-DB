# F homing pack (FABLE): `17-Presentation-Rendering/Character-Render-Records/render-event-selection-evidence.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 5. No bearing page cites them and no documented function calls them directly.

## 003B4DA0 (170 B, extent 003B4DA0-003B4E4A)

Documented callee on this page: `003E6AA0`

```
003B4DA0  push     rbx
003B4DA2  sub      rsp, 0x20
003B4DA6  movzx    eax, word ptr [rip + 0x278b75f]  ; -> 02B4050C
003B4DAD  xor      ebx, ebx
003B4DAF  cmp      ax, -1
003B4DB3  je       0x3b4dde  ; -> 003B4DDE
003B4DB5  movsx    rax, ax
003B4DB9  imul     rcx, rax, 0x740
003B4DC0  add      rcx, qword ptr [rip + 0x1f12161]  ; -> 022C6F28
003B4DC7  cmp      dword ptr [rcx + 0x284], ebx
003B4DCD  cmove    rcx, rbx
003B4DD1  test     rcx, rcx
003B4DD4  je       0x3b4dde  ; -> 003B4DDE
003B4DD6  lea      edx, [rbx + 2]
003B4DD9  call     0x3e6aa0  ; -> 003E6AA0 fn
003B4DDE  movzx    eax, word ptr [rip + 0x278b72f]  ; -> 02B40514
003B4DE5  mov      dword ptr [rip + 0x278b71d], 0xffffffff  ; -> 02B4050C
003B4DEF  mov      word ptr [rip + 0x278b712], bx  ; -> 02B40508
003B4DF6  mov      byte ptr [rip + 0x278b70e], bl  ; -> 02B4050A
003B4DFC  cmp      ax, -1
003B4E00  je       0x3b4e2d  ; -> 003B4E2D
003B4E02  movsx    rax, ax
003B4E06  imul     rcx, rax, 0x740
003B4E0D  add      rcx, qword ptr [rip + 0x1f12114]  ; -> 022C6F28
003B4E14  cmp      dword ptr [rcx + 0x284], ebx
003B4E1A  cmove    rcx, rbx
003B4E1E  test     rcx, rcx
003B4E21  je       0x3b4e2d  ; -> 003B4E2D
003B4E23  mov      edx, 2
003B4E28  call     0x3e6aa0  ; -> 003E6AA0 fn
003B4E2D  mov      dword ptr [rip + 0x278b6dd], 0xffffffff  ; -> 02B40514
003B4E37  mov      word ptr [rip + 0x278b6d2], bx  ; -> 02B40510
003B4E3E  mov      byte ptr [rip + 0x278b6ce], bl  ; -> 02B40512
003B4E44  add      rsp, 0x20
003B4E48  pop      rbx
003B4E49  ret      
```

## 003B5180 (386 B, extent 003B5180-003B5302)

Documented callee on this page: `003E6AA0`

```
003B5180  mov      qword ptr [rsp + 8], rbx
003B5185  push     rdi
003B5186  sub      rsp, 0x40
003B518A  cmp      byte ptr [rip + 0x278b379], 1  ; -> 02B4050A
003B5191  mov      ebx, ecx
003B5193  mov      dword ptr [rsp + 0x24], 0xffffffff
003B519B  mov      word ptr [rsp + 0x20], 0
003B51A2  mov      rdx, qword ptr [rsp + 0x20]
003B51A7  cmove    rdx, qword ptr [rip + 0x278b359]  ; -> 02B40508
003B51AF  cmp      byte ptr [rip + 0x278b35c], 1  ; -> 02B40512
003B51B6  mov      qword ptr [rsp + 0x20], rdx
003B51BB  jne      0x3b51d5  ; -> 003B51D5
003B51BD  movzx    eax, byte ptr [rip + 0x278b34d]  ; -> 02B40511
003B51C4  cmp      byte ptr [rsp + 0x21], al
003B51C8  cmovb    rdx, qword ptr [rip + 0x278b340]  ; -> 02B40510
003B51D0  mov      qword ptr [rsp + 0x20], rdx
003B51D5  xor      ecx, ecx
003B51D7  call     0x2ea030  ; -> 002EA030 fn
003B51DC  xor      edi, edi
003B51DE  cmp      eax, ebx
003B51E0  jne      0x3b5230  ; -> 003B5230
003B51E2  movzx    eax, word ptr [rip + 0x278b323]  ; -> 02B4050C
003B51E9  cmp      ax, -1
003B51ED  je       0x3b5218  ; -> 003B5218
003B51EF  movsx    rax, ax
003B51F3  imul     rcx, rax, 0x740
003B51FA  add      rcx, qword ptr [rip + 0x1f11d27]  ; -> 022C6F28
003B5201  cmp      dword ptr [rcx + 0x284], edi
003B5207  cmove    rcx, rdi
003B520B  test     rcx, rcx
003B520E  je       0x3b5218  ; -> 003B5218
003B5210  lea      edx, [rdi + 2]
003B5213  call     0x3e6aa0  ; -> 003E6AA0 fn
003B5218  mov      dword ptr [rip + 0x278b2ea], 0xffffffff  ; -> 02B4050C
003B5222  mov      word ptr [rip + 0x278b2df], di  ; -> 02B40508
003B5229  mov      byte ptr [rip + 0x278b2da], dil  ; -> 02B4050A
003B5230  mov      ecx, 1
003B5235  call     0x2ea030  ; -> 002EA030 fn
003B523A  cmp      eax, ebx
003B523C  jne      0x3b5293  ; -> 003B5293
003B523E  movzx    eax, word ptr [rip + 0x278b2cf]  ; -> 02B40514
003B5245  cmp      ax, -1
003B5249  je       0x3b5276  ; -> 003B5276
003B524B  movsx    rax, ax
003B524F  imul     rcx, rax, 0x740
003B5256  add      rcx, qword ptr [rip + 0x1f11ccb]  ; -> 022C6F28
003B525D  cmp      dword ptr [rcx + 0x284], edi
003B5263  cmove    rcx, rdi
003B5267  test     rcx, rcx
003B526A  je       0x3b5276  ; -> 003B5276
003B526C  mov      edx, 2
003B5271  call     0x3e6aa0  ; -> 003E6AA0 fn
003B5276  xor      cl, cl
003B5278  mov      dword ptr [rip + 0x278b292], 0xffffffff  ; -> 02B40514
003B5282  xor      dl, dl
003B5284  mov      word ptr [rip + 0x278b285], di  ; -> 02B40510
003B528B  mov      byte ptr [rip + 0x278b281], dl  ; -> 02B40512
003B5291  jmp      0x3b52a1  ; -> 003B52A1
003B5293  movzx    edx, byte ptr [rip + 0x278b278]  ; -> 02B40512
003B529A  movzx    ecx, byte ptr [rip + 0x278b270]  ; -> 02B40511
003B52A1  cmp      byte ptr [rip + 0x278b262], 1  ; -> 02B4050A
003B52A8  mov      dword ptr [rsp + 0x2c], 0xffffffff
003B52B0  mov      word ptr [rsp + 0x28], di
003B52B5  mov      rax, qword ptr [rsp + 0x28]
003B52BA  cmove    rax, qword ptr [rip + 0x278b246]  ; -> 02B40508
003B52C2  mov      qword ptr [rsp + 0x28], rax
003B52C7  cmp      dl, 1
003B52CA  jne      0x3b52dd  ; -> 003B52DD
003B52CC  cmp      byte ptr [rsp + 0x29], cl
003B52D0  cmovb    rax, qword ptr [rip + 0x278b238]  ; -> 02B40510
003B52D8  mov      qword ptr [rsp + 0x28], rax
003B52DD  mov      eax, dword ptr [rsp + 0x2c]
003B52E1  cmp      dword ptr [rsp + 0x24], eax
003B52E5  jne      0x3b52f2  ; -> 003B52F2
003B52E7  movzx    eax, byte ptr [rsp + 0x28]
003B52EC  cmp      byte ptr [rsp + 0x20], al
003B52F0  je       0x3b52f7  ; -> 003B52F7
003B52F2  call     0x3b4fd0  ; -> 003B4FD0 fn
003B52F7  mov      rbx, qword ptr [rsp + 0x50]
003B52FC  add      rsp, 0x40
003B5300  pop      rdi
003B5301  ret      
```

## 003E0740 (279 B, extent 003E0740-003E0857)

Documented callee on this page: `003E6DA0`

```
003E0740  push     rdi
003E0742  sub      rsp, 0x20
003E0746  mov      rdx, qword ptr [rip + 0x1ee67db]  ; -> 022C6F28
003E074D  mov      edi, dword ptr [rdx + 0x48800]
003E0753  cmp      edi, -1
003E0756  je       0x3e0851  ; -> 003E0851
003E075C  mov      qword ptr [rsp + 0x30], rbx
003E0761  cmp      di, -1
003E0765  je       0x3e0835  ; -> 003E0835
003E076B  movsx    rax, di
003E076F  imul     rcx, rax, 0x740
003E0776  add      rcx, rdx
003E0779  je       0x3e0835  ; -> 003E0835
003E077F  cmp      dword ptr [rcx + 0x284], 0
003E0786  je       0x3e0835  ; -> 003E0835
003E078C  call     0x3e6da0  ; -> 003E6DA0 fn
003E0791  mov      rbx, rax
003E0794  test     rax, rax
003E0797  je       0x3e082e  ; -> 003E082E
003E079D  mov      ecx, dword ptr [rax + 8]
003E07A0  call     0x20e600  ; -> 0020E600 fn
003E07A5  test     rax, rax
003E07A8  je       0x3e07ba  ; -> 003E07BA
003E07AA  mov      ecx, dword ptr [rbx + 8]
003E07AD  call     0x20e600  ; -> 0020E600 fn
003E07B2  mov      rcx, rax
003E07B5  call     0x5154b0  ; -> 005154B0 fn
003E07BA  mov      ecx, dword ptr [rbx + 0x28]
003E07BD  call     0x20e600  ; -> 0020E600 fn
003E07C2  test     rax, rax
003E07C5  je       0x3e07d7  ; -> 003E07D7
003E07C7  mov      ecx, dword ptr [rbx + 0x28]
003E07CA  call     0x20e600  ; -> 0020E600 fn
003E07CF  mov      rcx, rax
003E07D2  call     0x518e60  ; -> 00518E60 fn
003E07D7  mov      ecx, dword ptr [rbx + 0x34]
003E07DA  call     0x20e600  ; -> 0020E600 fn
003E07DF  test     rax, rax
003E07E2  je       0x3e07f4  ; -> 003E07F4
003E07E4  mov      ecx, dword ptr [rbx + 0x34]
003E07E7  call     0x20e600  ; -> 0020E600 fn
003E07EC  mov      rcx, rax
003E07EF  call     0x4719f0  ; -> 004719F0 fn
003E07F4  mov      ecx, dword ptr [rbx + 0x3c]
003E07F7  call     0x20e600  ; -> 0020E600 fn
003E07FC  test     rax, rax
003E07FF  je       0x3e0811  ; -> 003E0811
003E0801  mov      ecx, dword ptr [rbx + 0x3c]
003E0804  call     0x20e600  ; -> 0020E600 fn
003E0809  mov      rcx, rax
003E080C  call     0x472820  ; -> 00472820 fn
003E0811  mov      ecx, dword ptr [rbx + 0x24]
003E0814  call     0x20e600  ; -> 0020E600 fn
003E0819  test     rax, rax
003E081C  je       0x3e082e  ; -> 003E082E
003E081E  mov      ecx, dword ptr [rbx + 0x24]
003E0821  call     0x20e600  ; -> 0020E600 fn
003E0826  mov      rcx, rax
003E0829  call     0x5175f0  ; -> 005175F0 fn
003E082E  mov      rdx, qword ptr [rip + 0x1ee66f3]  ; -> 022C6F28
003E0835  mov      eax, edi
003E0837  imul     rcx, rax, 0x740
003E083E  movsx    edi, word ptr [rcx + rdx + 4]
003E0843  cmp      edi, -1
003E0846  jne      0x3e0761  ; -> 003E0761
003E084C  mov      rbx, qword ptr [rsp + 0x30]
003E0851  add      rsp, 0x20
003E0855  pop      rdi
003E0856  ret      
```

## 00423980 (137 B, extent 00423980-00423A09)

Documented callee on this page: `0051BA40`

```
00423980  mov      qword ptr [rsp + 8], rbx
00423985  push     rdi
00423986  sub      rsp, 0x20
0042398A  mov      edi, dword ptr [rcx + 0xc4]
00423990  mov      rbx, rcx
00423993  cmp      edi, -1
00423996  je       0x4239ae  ; -> 004239AE
00423998  mov      ecx, dword ptr [rcx + 0x10]
0042399B  call     0x20e600  ; -> 0020E600 fn
004239A0  mov      edx, edi
004239A2  mov      rcx, qword ptr [rax + 0xda8]
004239A9  call     0x51ba40  ; -> 0051BA40 fn
004239AE  mov      edi, dword ptr [rbx + 0x18]
004239B1  mov      dword ptr [rbx + 0xc4], 0xffffffff
004239BB  cmp      edi, -1
004239BE  je       0x4239fe  ; -> 004239FE
004239C0  mov      ecx, dword ptr [rbx + 0x10]
004239C3  call     0x20e600  ; -> 0020E600 fn
004239C8  cmp      edi, -1
004239CB  je       0x4239fe  ; -> 004239FE
004239CD  mov      rcx, qword ptr [rax + 0xd98]
004239D4  mov      edx, edi
004239D6  call     0x2ed570  ; -> 002ED570 fn
004239DB  test     rax, rax
004239DE  je       0x4239fe  ; -> 004239FE
004239E0  movss    xmm0, dword ptr [rax + 0x98]
004239E8  comiss   xmm0, dword ptr [rip + 0x18c81b9]  ; -> 01CEBBA8 [f32 1]
004239EF  jb       0x4239fe  ; -> 004239FE
004239F1  and      dword ptr [rax], 0xfffffff7
004239F4  mov      dword ptr [rax + 0x98], 0
004239FE  mov      rbx, qword ptr [rsp + 0x30]
00423A03  add      rsp, 0x20
00423A07  pop      rdi
00423A08  ret      
```

## 0046E8D0 (50 B, extent 0046E8D0-0046E902)

Documented callee on this page: `00372F60`

```
0046E8D0  push     rbx
0046E8D2  sub      rsp, 0x20
0046E8D6  mov      rax, rdx
0046E8D9  mov      rbx, rcx
0046E8DC  mov      edx, dword ptr [rcx + 0x10]
0046E8DF  cmp      edx, -1
0046E8E2  je       0x46e8fc  ; -> 0046E8FC
0046E8E4  mov      rcx, rax
0046E8E7  call     0x2ed570  ; -> 002ED570 fn
0046E8EC  mov      rdx, rax
0046E8EF  mov      rcx, rbx
0046E8F2  add      rsp, 0x20
0046E8F6  pop      rbx
0046E8F7  jmp      0x372f60  ; -> 00372F60 fn
0046E8FC  add      rsp, 0x20
0046E900  pop      rbx
0046E901  ret      
```
