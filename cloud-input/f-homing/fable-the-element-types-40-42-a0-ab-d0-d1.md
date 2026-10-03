# F homing pack (FABLE): `17-Presentation-Rendering/Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 2. No bearing page cites them and no documented function calls them directly.

## 003DE8A0 (127 B, extent 003DE8A0-003DE91F)

Documented callee on this page: `003AC920`

```
003DE8A0  push     rbx
003DE8A2  sub      rsp, 0x40
003DE8A6  movsxd   rax, ecx
003DE8A9  imul     rbx, rax, 0x70
003DE8AD  movaps   xmmword ptr [rsp + 0x30], xmm6
003DE8B2  xorps    xmm6, xmm6
003DE8B5  movaps   xmmword ptr [rsp + 0x20], xmm7
003DE8BA  maxss    xmm6, xmm1
003DE8BE  movaps   xmm7, xmm2
003DE8C1  lea      rax, [rip + 0x277a388]  ; -> 02B58C50
003DE8C8  add      rbx, rax
003DE8CB  movaps   xmm0, xmm6
003DE8CE  call     0x861f08  ; -> 00861F08 fn
003DE8D3  movss    dword ptr [rbx + 0x60], xmm0
003DE8D8  maxss    xmm6, xmm7
003DE8DC  movaps   xmm0, xmm6
003DE8DF  call     0x861f08  ; -> 00861F08 fn
003DE8E4  movss    dword ptr [rbx + 0x64], xmm0
003DE8E9  cmp      qword ptr [rbx + 8], 0
003DE8EE  je       0x3de90f  ; -> 003DE90F
003DE8F0  mov      ecx, dword ptr [rbx]
003DE8F2  test     ecx, ecx
003DE8F4  je       0x3de90f  ; -> 003DE90F
003DE8F6  call     0x3abd00  ; -> 003ABD00 fn
003DE8FB  mov      ecx, dword ptr [rbx + 0x60]
003DE8FE  mov      dword ptr [rax + 0x40], ecx
003DE901  mov      ecx, dword ptr [rbx + 0x64]
003DE904  mov      dword ptr [rax + 0x44], ecx
003DE907  mov      rcx, rax
003DE90A  call     0x3ac920  ; -> 003AC920 fn
003DE90F  movaps   xmm6, xmmword ptr [rsp + 0x30]
003DE914  movaps   xmm7, xmmword ptr [rsp + 0x20]
003DE919  add      rsp, 0x40
003DE91D  pop      rbx
003DE91E  ret      
```

## 003DEAC0 (103 B, extent 003DEAC0-003DEB27)

Documented callee on this page: `003AC920`

```
003DEAC0  push     rbx
003DEAC2  sub      rsp, 0x20
003DEAC6  movsxd   rax, ecx
003DEAC9  imul     rbx, rax, 0x70
003DEACD  lea      rax, [rip + 0x277a17c]  ; -> 02B58C50
003DEAD4  add      rbx, rax
003DEAD7  cmp      byte ptr [rbx + 0x20], 0
003DEADB  je       0x3deb21  ; -> 003DEB21
003DEADD  xorps    xmm0, xmm0
003DEAE0  comiss   xmm0, xmm1
003DEAE3  jbe      0x3deaf3  ; -> 003DEAF3
003DEAE5  or       byte ptr [rbx + 0x25], 1
003DEAE9  movss    xmm1, dword ptr [rip + 0x190d0b7]  ; -> 01CEBBA8 [f32 1]
003DEAF1  jmp      0x3deaf7  ; -> 003DEAF7
003DEAF3  and      byte ptr [rbx + 0x25], 0xfe
003DEAF7  movss    dword ptr [rbx + 0x2c], xmm1
003DEAFC  cmp      qword ptr [rbx + 8], 0
003DEB01  je       0x3deb21  ; -> 003DEB21
003DEB03  mov      ecx, dword ptr [rbx]
003DEB05  test     ecx, ecx
003DEB07  je       0x3deb21  ; -> 003DEB21
003DEB09  call     0x3abd00  ; -> 003ABD00 fn
003DEB0E  mov      ecx, dword ptr [rbx + 0x2c]
003DEB11  mov      dword ptr [rax + 0xc], ecx
003DEB14  mov      rcx, rax
003DEB17  add      rsp, 0x20
003DEB1B  pop      rbx
003DEB1C  jmp      0x3ac920  ; -> 003AC920 fn
003DEB21  add      rsp, 0x20
003DEB25  pop      rbx
003DEB26  ret      
```
