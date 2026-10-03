# F homing pack (FABLE): `04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md`

Generated 2026-10-03 06:31 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 0035D5C0 (43 B, extent 0035D5C0-0035D5EB)

Documented callee on this page: `00273BA0`

```
0035D5C0  sub      rsp, 0x28
0035D5C4  test     dword ptr [rip + 0x1f6ae1a], 0x200  ; -> 022C83E8
0035D5CE  jne      0x35d5e6  ; -> 0035D5E6
0035D5D0  lea      rcx, [rip + 0x1f6b531]  ; -> 022C8B08
0035D5D7  call     0x273ba0  ; -> 00273BA0 fn
0035D5DC  or       dword ptr [rip + 0x1f6ae02], 0x200  ; -> 022C83E8
0035D5E6  add      rsp, 0x28
0035D5EA  ret      
```
