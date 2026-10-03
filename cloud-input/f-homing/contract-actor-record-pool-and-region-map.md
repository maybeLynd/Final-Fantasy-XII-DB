# F homing pack: `04-Actor-Entity/CONTRACT-actor-record-pool-and-region-map.md`

Generated 2026-10-02 22:03 by OPUS (homing_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 2. No bearing page cites them and no documented function calls them directly.

## 00269060 (33 B, extent 00269060-00269081)

Documented callee on this page: `00268690`

```
00269060  sub      rsp, 0x28
00269064  mov      ecx, 9
00269069  call     0x268690  ; -> 00268690 fn
0026906E  call     0x3148d0  ; -> 003148D0 fn
00269073  and      eax, 0xffffffe7
00269076  mov      ecx, eax
00269078  add      rsp, 0x28
0026907C  jmp      0x314da0  ; -> 00314DA0 fn
```

## 003446D0 (61 B, extent 003446D0-0034470D)

Documented callee on this page: `00268530`

```
003446D0  push     rbx
003446D2  sub      rsp, 0x20
003446D6  mov      rcx, r9
003446D9  call     0x267e10  ; -> 00267E10 fn
003446DE  mov      ecx, eax
003446E0  call     0x268530  ; -> 00268530 fn
003446E5  xor      ebx, ebx
003446E7  mov      ecx, ebx
003446E9  call     0x263750  ; -> 00263750 fn
003446EE  test     rax, rax
003446F1  je       0x344700  ; -> 00344700
003446F3  mov      edx, 1
003446F8  mov      rcx, rax
003446FB  call     0x35ae10  ; -> 0035AE10 fn
00344700  inc      ebx
00344702  cmp      ebx, 4
00344705  jl       0x3446e7  ; -> 003446E7
00344707  add      rsp, 0x20
0034470B  pop      rbx
0034470C  ret      
```
