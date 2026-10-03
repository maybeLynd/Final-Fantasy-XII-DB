# F homing pack (FABLE): `03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 0031BD80 (62 B, extent 0031BD80-0031BDBE)

Documented callee on this page: `0031BDC0`

```
0031BD80  push     rbx
0031BD82  sub      rsp, 0x20
0031BD86  mov      ebx, edx
0031BD88  test     rcx, rcx
0031BD8B  je       0x31bdb3  ; -> 0031BDB3
0031BD8D  call     0x263e30  ; -> 00263E30 fn
0031BD92  test     rax, rax
0031BD95  je       0x31bdb3  ; -> 0031BDB3
0031BD97  mov      rcx, qword ptr [rax + 0x698]
0031BD9E  test     rcx, rcx
0031BDA1  je       0x31bdb3  ; -> 0031BDB3
0031BDA3  add      rcx, 0x50
0031BDA7  mov      edx, ebx
0031BDA9  add      rsp, 0x20
0031BDAD  pop      rbx
0031BDAE  jmp      0x31bdc0  ; -> 0031BDC0 fn
0031BDB3  mov      eax, 0xffff
0031BDB8  add      rsp, 0x20
0031BDBC  pop      rbx
0031BDBD  ret      
```
