# F homing pack (FABLE): `04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md`

Generated 2026-10-03 06:31 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 2. No bearing page cites them and no documented function calls them directly.

## 00239370 (104 B, extent 00239370-002393D8)

Documented callee on this page: `0026BB50`

```
00239370  push     rbx
00239372  sub      rsp, 0x50
00239376  movaps   xmmword ptr [rsp + 0x40], xmm6
0023937B  mov      rbx, rcx
0023937E  movaps   xmmword ptr [rsp + 0x30], xmm7
00239383  xorps    xmm6, xmm6
00239386  comiss   xmm3, xmm6
00239389  movaps   xmmword ptr [rsp + 0x20], xmm8
0023938F  movaps   xmm7, xmm1
00239392  movaps   xmm8, xmm2
00239396  jb       0x2393a0  ; -> 002393A0
00239398  movaps   xmm1, xmm3
0023939B  call     0x26bb50  ; -> 0026BB50 fn
002393A0  comiss   xmm8, xmm6
002393A4  jb       0x2393b2  ; -> 002393B2
002393A6  movaps   xmm1, xmm8
002393AA  mov      rcx, rbx
002393AD  call     0x26ba00  ; -> 0026BA00 fn
002393B2  comiss   xmm7, xmm6
002393B5  jb       0x2393c2  ; -> 002393C2
002393B7  movaps   xmm1, xmm7
002393BA  mov      rcx, rbx
002393BD  call     0x26b940  ; -> 0026B940 fn
002393C2  movaps   xmm6, xmmword ptr [rsp + 0x40]
002393C7  movaps   xmm7, xmmword ptr [rsp + 0x30]
002393CC  movaps   xmm8, xmmword ptr [rsp + 0x20]
002393D2  add      rsp, 0x50
002393D6  pop      rbx
002393D7  ret      
```

## 0026BE00 (56 B, extent 0026BE00-0026BE38)

Documented callee on this page: `002E86B0`

```
0026BE00  movzx    eax, byte ptr [rcx + 3]
0026BE04  and      al, 0xe0
0026BE06  cmp      al, 0x60
0026BE08  jne      0x26be37  ; -> 0026BE37
0026BE0A  mov      rax, qword ptr [rcx + 0xb8]
0026BE11  movss    dword ptr [rax + 0xe4], xmm1
0026BE19  movzx    eax, byte ptr [rcx + 3]
0026BE1D  and      al, 0xe0
0026BE1F  cmp      al, 0x60
0026BE21  jne      0x26be37  ; -> 0026BE37
0026BE23  mov      rax, qword ptr [rcx + 0xb8]
0026BE2A  movss    xmm1, dword ptr [rax + 0xe4]
0026BE32  jmp      0x2e86b0  ; -> 002E86B0 fn
0026BE37  ret      
```
