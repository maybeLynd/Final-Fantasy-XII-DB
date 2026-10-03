# Homing pack: `18-Audio/the-spatial-audio-object-model.md`

Generated 2026-10-03 12:43 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h12-the-spatial-audio-object-model.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001DBFA0 (84 B, extent 001DBFA0-001DBFF4)

Entered from (direct sites whose caller this page cites): `002DF1A0` + 0x2E (call; `002DF1A0` is cited on this page)
Other direct sites: `002DF1E0` + 0x2C (call)

Host context: " | Interior anchor '002DEF23'; Interior anchor '002DEF28'; Interior anchor '002DEF2C' | [CONTRACT-world-simulation-tick](../00-Engine-Core-Runtime/Battle-Frame/CONTRACT-world-simulation-tick.md) | | '002DF1A0' | 56 B | '003B99D0' + 0x2EE | when 'edx' is zero, tail-jumps ('002DF1A0' + 0x18) with 1 in 'ecx', the incoming 'ecx' in 'edx', 0 in 'r8d' and the incoming 'r8d' in 'r9d'; otherwise calls '002DF1A0' + 0x2E with 1 in 'ecx', the inco"

```
001DBFA0  mov      qword ptr [rsp + 8], rbx
001DBFA5  mov      qword ptr [rsp + 0x10], rbp
001DBFAA  mov      qword ptr [rsp + 0x18], rsi
001DBFAF  push     rdi
001DBFB0  sub      rsp, 0x30
001DBFB4  mov      ebx, r9d
001DBFB7  mov      edi, r8d
001DBFBA  mov      esi, edx
001DBFBC  mov      ebp, ecx
001DBFBE  call     0x210b30  ; -> 00210B30 fn
001DBFC3  mov      rcx, rax
001DBFC6  mov      r9d, edi
001DBFC9  mov      eax, dword ptr [rsp + 0x60]
001DBFCD  mov      r8d, esi
001DBFD0  mov      dword ptr [rsp + 0x28], eax
001DBFD4  mov      edx, ebp
001DBFD6  mov      dword ptr [rsp + 0x20], ebx
001DBFDA  call     0x210e10  ; -> 00210E10 fn
001DBFDF  mov      rbx, qword ptr [rsp + 0x40]
001DBFE4  mov      rbp, qword ptr [rsp + 0x48]
001DBFE9  mov      rsi, qword ptr [rsp + 0x50]
001DBFEE  add      rsp, 0x30
001DBFF2  pop      rdi
001DBFF3  ret      
```
