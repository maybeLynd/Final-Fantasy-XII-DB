# F homing pack (FABLE): `06-Movement-And-Navigation/Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 003DD8D0 (162 B, extent 003DD8D0-003DD972)

Documented callee on this page: `00263F40`

```
003DD8D0  mov      qword ptr [rsp + 8], rbx
003DD8D5  mov      qword ptr [rsp + 0x10], rbp
003DD8DA  mov      qword ptr [rsp + 0x18], rsi
003DD8DF  push     rdi
003DD8E0  sub      rsp, 0x20
003DD8E4  movsxd   rbx, edx
003DD8E7  mov      rdi, rcx
003DD8EA  mov      r10, rbx
003DD8ED  movsxd   rsi, r8d
003DD8F0  shl      r10, 4
003DD8F4  lea      rcx, [rip + 0x277a8a9]  ; -> 02B581A4
003DD8FB  add      r10, rsi
003DD8FE  mov      ebp, r9d
003DD901  imul     rax, r10, 0x1c
003DD905  cmp      dword ptr [rax + rcx], 4
003DD909  jne      0x3dd95d  ; -> 003DD95D
003DD90B  mov      rcx, rdi
003DD90E  call     0x2e9560  ; -> 002E9560 fn
003DD913  movaps   xmm1, xmm0
003DD916  mov      rcx, rdi
003DD919  call     0x2e4f40  ; -> 002E4F40 fn
003DD91E  or       byte ptr [rdi + 0xd], 1
003DD922  mov      rcx, rdi
003DD925  mov      byte ptr [rdi + 0xf5], sil
003DD92C  call     0x263f40  ; -> 00263F40 fn
003DD931  mov      rcx, rdi
003DD934  movzx    edx, byte ptr [rax + 0xd]
003DD938  shr      edx, 7
003DD93B  call     0x2e8170  ; -> 002E8170 fn
003DD940  movss    xmm3, dword ptr [rsp + 0x50]
003DD946  xor      r8d, r8d
003DD949  shl      ebx, 4
003DD94C  mov      rcx, rdi
003DD94F  or       ebx, esi
003DD951  shl      ebx, 0x10
003DD954  or       ebx, ebp
003DD956  mov      edx, ebx
003DD958  call     0x2eb080  ; -> 002EB080 fn
003DD95D  mov      rbx, qword ptr [rsp + 0x30]
003DD962  mov      rbp, qword ptr [rsp + 0x38]
003DD967  mov      rsi, qword ptr [rsp + 0x40]
003DD96C  add      rsp, 0x20
003DD970  pop      rdi
003DD971  ret      
```
