# F homing pack (FABLE): `16-UI/Request-Router/ui-request-router.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 2. No bearing page cites them and no documented function calls them directly.

## 002E1660 (33 B, extent 002E1660-002E1681)

Documented callee on this page: `0028F7C0`

```
002E1660  push     rbx
002E1662  sub      rsp, 0x20
002E1666  xor      ebx, ebx
002E1668  call     0x28f7c0  ; -> 0028F7C0 fn
002E166D  dec      eax
002E166F  mov      ecx, 1
002E1674  cmp      eax, ecx
002E1676  cmovbe   ebx, ecx
002E1679  mov      eax, ebx
002E167B  add      rsp, 0x20
002E167F  pop      rbx
002E1680  ret      
```

## 002E2320 (20 B, extent 002E2320-002E2334)

Documented callee on this page: `002E0E30`

```
002E2320  sub      rsp, 0x28
002E2324  call     0x28f5f0  ; -> 0028F5F0 fn
002E2329  mov      ecx, eax
002E232B  add      rsp, 0x28
002E232F  jmp      0x2e0e30  ; -> 002E0E30 fn
```
