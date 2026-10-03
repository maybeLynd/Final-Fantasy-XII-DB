# Homing pack: `03-World-Area-Field/Weather/weather-apply-and-environment-materialization.md`

Generated 2026-10-03 11:24 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h9-weather-apply-and-environment-materialization.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00321EA0 (110 B, extent 00321EA0-00321F0E)

Entered from (direct sites whose caller this page cites): `003EBE70` + 0xA1 (jmp; `003EBE70` is cited on this page)
Other direct sites: `003EBD30` + 0x31 (jmp)

Host context: "erior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*  | function | size | what the body does | interior anchors | |---|---|---|---| | '003EBE70' | 171 B | stores qword '02B5EC60' = 'rcx' and returns when it is null; otherwise passes a non-null qword '02B5EC68' to the call at '003EBE70+0x20' and zeroes it, calls '0036C1D0(5, 5)', stores qword '02B5EC68' = '0036A190(0x100)' "

```
00321EA0  mov      qword ptr [rsp + 0x10], rsi
00321EA5  push     rdi
00321EA6  sub      rsp, 0x30
00321EAA  mov      rdi, rdx
00321EAD  mov      dword ptr [rsp + 0x20], 1
00321EB5  mov      r8, rdx
00321EB8  mov      rsi, rcx
00321EBB  mov      rdx, rcx
00321EBE  xor      r9d, r9d
00321EC1  xor      ecx, ecx
00321EC3  call     0x321f10  ; -> 00321F10 fn
00321EC8  test     eax, eax
00321ECA  je       0x321edc  ; -> 00321EDC
00321ECC  mov      eax, 1
00321ED1  mov      rsi, qword ptr [rsp + 0x48]
00321ED6  add      rsp, 0x30
00321EDA  pop      rdi
00321EDB  ret      
00321EDC  mov      qword ptr [rsp + 0x40], rbx
00321EE1  xor      r9d, r9d
00321EE4  xor      ebx, ebx
00321EE6  mov      r8, rdi
00321EE9  mov      rdx, rsi
00321EEC  mov      dword ptr [rsp + 0x20], ebx
00321EF0  xor      ecx, ecx
00321EF2  call     0x321f10  ; -> 00321F10 fn
00321EF7  mov      rsi, qword ptr [rsp + 0x48]
00321EFC  test     eax, eax
00321EFE  setne    bl
00321F01  mov      eax, ebx
00321F03  mov      rbx, qword ptr [rsp + 0x40]
00321F08  add      rsp, 0x30
00321F0C  pop      rdi
00321F0D  ret      
```
