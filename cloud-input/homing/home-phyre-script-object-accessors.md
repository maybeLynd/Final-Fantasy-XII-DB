# Homing pack: `22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-phyre-script-object-accessors.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 005AA3C0 (138 B, extent 005AA3C0-005AA44A)

Entered from (direct sites whose caller this page cites): `005A2770` + 0x33 (call; `005A2770` is cited on this page); `005A4390` + 0x35 (jmp; `005A4390` is cited on this page); `005A5050` + 0x35 (jmp; `005A5050` is cited on this page); `005A50B0` + 0x22 (jmp; `005A50B0` is cited on this page)
Other direct sites: `005AA710` + 0x68 (call); `005C55C0` + 0x1C (jmp); `006D72F0` + 0x1C (jmp)

Host context: " copies from the result P to 'r8' at the same offsets the dword '+0x8', the qword '+0x10' and the dwords '+0x18', '+0x1C' and '+0x20' | '005A243C', '005A2444', '005A244B', '005A2452', '005A245E' | | '005A2770' | 73 B | calls '005B94D0(rdx)', then with the result P calls '005AA840(r8, P)', copies the qword '+0x48' from P to 'r8', calls '005AA3C0(r8+0x50, P+0x50)' and copies the dword '+0x60' | '005A2780', '005A278E', '005A279B', '005A27A" / "n the result P equals 'r8'; otherwise calls '005AA840(r8, P)' and copies the qword '+0x38' and the 16 bytes at '+0x48' from P to 'r8' | '005A3270', '005A3278', '005A3283', '005A328C', '005A3294' | | '005A4390' | 58 B | calls '005BAB90(rdx)', then with the result P calls '005AA7D0(r8, P)' and tail-jumps to '005AA3C0(r8+0x28, P+0x28)' | '005A43A0', '005A43AE', '005A43C5' | | '005A5050' | 58 B | calls '005B93B0(rdx)', then with the result "

```
005AA3C0  mov      qword ptr [rsp + 8], rbx
005AA3C5  mov      qword ptr [rsp + 0x10], rbp
005AA3CA  mov      qword ptr [rsp + 0x18], rsi
005AA3CF  push     rdi
005AA3D0  sub      rsp, 0x20
005AA3D4  mov      esi, dword ptr [rdx]
005AA3D6  mov      rbx, rcx
005AA3D9  mov      rbp, qword ptr [rdx + 8]
005AA3DD  mov      edi, 0
005AA3E2  and      esi, 0x7fffffff
005AA3E8  jbe      0x5aa40e  ; -> 005AA40E
005AA3EA  mov      ecx, esi
005AA3EC  lea      edx, [rdi + 4]
005AA3EF  shl      rcx, 2
005AA3F3  call     0x17d260  ; -> 0017D260 fn
005AA3F8  mov      rdi, rax
005AA3FB  test     rax, rax
005AA3FE  je       0x5aa40e  ; -> 005AA40E
005AA400  mov      r8d, esi
005AA403  mov      rdx, rbp
005AA406  mov      rcx, rax
005AA409  call     0x5a5b40  ; -> 005A5B40 fn
005AA40E  mov      rcx, qword ptr [rbx + 8]
005AA412  cmp      rcx, rdi
005AA415  je       0x5aa42c  ; -> 005AA42C
005AA417  mov      eax, dword ptr [rbx]
005AA419  shr      eax, 0x1f
005AA41C  not      al
005AA41E  test     al, 1
005AA420  je       0x5aa42c  ; -> 005AA42C
005AA422  test     rcx, rcx
005AA425  je       0x5aa42c  ; -> 005AA42C
005AA427  call     0x584730  ; -> 00584730 fn
005AA42C  mov      rbp, qword ptr [rsp + 0x38]
005AA431  mov      rax, rbx
005AA434  mov      dword ptr [rbx], esi
005AA436  mov      rsi, qword ptr [rsp + 0x40]
005AA43B  mov      qword ptr [rbx + 8], rdi
005AA43F  mov      rbx, qword ptr [rsp + 0x30]
005AA444  add      rsp, 0x20
005AA448  pop      rdi
005AA449  ret      
```
