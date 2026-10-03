# F homing pack (FABLE): `19-Save-Load-Settings/Game-Settings-Config/ff12config-and-debglobal.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 003E9B80 (112 B, extent 003E9B80-003E9BF0)

Documented callee on this page: `002DEBB0`

```
003E9B80  mov      qword ptr [rsp + 8], rbx
003E9B85  push     rdi
003E9B86  sub      rsp, 0x20
003E9B8A  movsxd   rbx, ecx
003E9B8D  lea      rax, [rip + 0x277351c]  ; -> 02B5D0B0
003E9B94  shl      rbx, 6
003E9B98  add      rbx, rax
003E9B9B  movsxd   rdi, edx
003E9B9E  call     0x2debb0  ; -> 002DEBB0 fn
003E9BA3  cmp      byte ptr [rbx + 4], 3
003E9BA7  movsxd   rcx, eax
003E9BAA  mov      r8, qword ptr [rbx + rcx*8 + 0x20]
003E9BAF  mov      qword ptr [rbx + 0x30], r8
003E9BB3  jne      0x3e9be3  ; -> 003E9BE3
003E9BB5  test     r8, r8
003E9BB8  je       0x3e9be3  ; -> 003E9BE3
003E9BBA  cmp      dword ptr [r8 + 4], edi
003E9BBE  jbe      0x3e9be3  ; -> 003E9BE3
003E9BC0  mov      rcx, rdi
003E9BC3  shl      rcx, 4
003E9BC7  add      rcx, 8
003E9BCB  add      rcx, r8
003E9BCE  je       0x3e9be3  ; -> 003E9BE3
003E9BD0  xor      eax, eax
003E9BD2  cmp      dword ptr [rcx + 0xc], eax
003E9BD5  setne    al
003E9BD8  mov      rbx, qword ptr [rsp + 0x30]
003E9BDD  add      rsp, 0x20
003E9BE1  pop      rdi
003E9BE2  ret      
003E9BE3  xor      eax, eax
003E9BE5  mov      rbx, qword ptr [rsp + 0x30]
003E9BEA  add      rsp, 0x20
003E9BEE  pop      rdi
003E9BEF  ret      
```
