# F homing pack (FABLE): `03-World-Area-Field/Weather/weather-probability-and-transition-roll.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 2. No bearing page cites them and no documented function calls them directly.

## 003597B0 (31 B, extent 003597B0-003597CF)

Documented callee on this page: `00234D40`

```
003597B0  sub      rsp, 0x28
003597B4  call     0x234d40  ; -> 00234D40 fn
003597B9  sub      eax, 1
003597BC  je       0x3597c8  ; -> 003597C8
003597BE  cmp      eax, 1
003597C1  jne      0x3597c8  ; -> 003597C8
003597C3  add      rsp, 0x28
003597C7  ret      
003597C8  xor      eax, eax
003597CA  add      rsp, 0x28
003597CE  ret      
```

## 003597D0 (46 B, extent 003597D0-003597FE)

Documented callee on this page: `00234D40`

```
003597D0  sub      rsp, 0x28
003597D4  call     0x234d40  ; -> 00234D40 fn
003597D9  sub      eax, 1
003597DC  je       0x3597f4  ; -> 003597F4
003597DE  cmp      eax, 1
003597E1  je       0x3597ea  ; -> 003597EA
003597E3  xor      eax, eax
003597E5  add      rsp, 0x28
003597E9  ret      
003597EA  mov      eax, 2
003597EF  add      rsp, 0x28
003597F3  ret      
003597F4  mov      eax, 1
003597F9  add      rsp, 0x28
003597FD  ret      
```
