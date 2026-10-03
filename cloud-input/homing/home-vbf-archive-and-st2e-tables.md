# Homing pack: `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md`

Generated 2026-10-03 07:51 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-vbf-archive-and-st2e-tables.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 003C9840 (86 B, extent 003C9840-003C9896)

Entered from (direct sites whose caller this page cites): `003C9A30` + 0x13D (call; `003C9A30` is cited on this page); `003C9A30` + 0x288 (call; `003C9A30` is cited on this page)
Other direct sites: none

Host context: "B'; Interior anchor '0028FFD0' | | '003C98E0' | 31 B | '0035C630' + 0x13 | returns when qword '02B47740' is non-zero; otherwise tail-jumps at '003C98E0' + 0x19 with 'ecx' = 0xD8, 'rdx' = the address '003C9A30' and 'r8d' = 0 | Interior anchor '003C98E8'; Interior anchor '003C98ED'; Interior anchor '003C98F4'; Interior anchor '003C98F9' | | '003CA280' | 48 B | '0035C630' + 0xE | when qword '02B47758' is null, stores there the result of th" / "B'; Interior anchor '0028FFD0' | | '003C98E0' | 31 B | '0035C630' + 0x13 | returns when qword '02B47740' is non-zero; otherwise tail-jumps at '003C98E0' + 0x19 with 'ecx' = 0xD8, 'rdx' = the address '003C9A30' and 'r8d' = 0 | Interior anchor '003C98E8'; Interior anchor '003C98ED'; Interior anchor '003C98F4'; Interior anchor '003C98F9' | | '003CA280' | 48 B | '0035C630' + 0xE | when qword '02B47758' is null, stores there the result of th"

```
003C9840  push     rbx
003C9842  sub      rsp, 0x20
003C9846  cmp      qword ptr [rcx + 0xc8], 0
003C984E  mov      rbx, rcx
003C9851  je       0x3c9890  ; -> 003C9890
003C9853  call     0x3c5fb0  ; -> 003C5FB0 fn
003C9858  mov      rcx, rbx
003C985B  mov      edx, 2
003C9860  test     eax, eax
003C9862  jne      0x3c9869  ; -> 003C9869
003C9864  mov      edx, 1
003C9869  call     0x394690  ; -> 00394690 fn
003C986E  mov      rcx, qword ptr [rbx + 0xc8]
003C9875  movsx    edx, word ptr [rax + 0xe]
003C9879  test     rcx, rcx
003C987C  je       0x3c9890  ; -> 003C9890
003C987E  movzx    eax, word ptr [rax + 0xc]
003C9882  mov      word ptr [rcx + 0x98], ax
003C9889  mov      word ptr [rcx + 0x9a], dx
003C9890  add      rsp, 0x20
003C9894  pop      rbx
003C9895  ret      
```

## 003C98A0 (62 B, extent 003C98A0-003C98DE)

Entered from (direct sites whose caller this page cites): `003C9A30` + 0x178 (call; `003C9A30` is cited on this page); `003C9A30` + 0x307 (call; `003C9A30` is cited on this page)
Other direct sites: none

Host context: "B'; Interior anchor '0028FFD0' | | '003C98E0' | 31 B | '0035C630' + 0x13 | returns when qword '02B47740' is non-zero; otherwise tail-jumps at '003C98E0' + 0x19 with 'ecx' = 0xD8, 'rdx' = the address '003C9A30' and 'r8d' = 0 | Interior anchor '003C98E8'; Interior anchor '003C98ED'; Interior anchor '003C98F4'; Interior anchor '003C98F9' | | '003CA280' | 48 B | '0035C630' + 0xE | when qword '02B47758' is null, stores there the result of th" / "B'; Interior anchor '0028FFD0' | | '003C98E0' | 31 B | '0035C630' + 0x13 | returns when qword '02B47740' is non-zero; otherwise tail-jumps at '003C98E0' + 0x19 with 'ecx' = 0xD8, 'rdx' = the address '003C9A30' and 'r8d' = 0 | Interior anchor '003C98E8'; Interior anchor '003C98ED'; Interior anchor '003C98F4'; Interior anchor '003C98F9' | | '003CA280' | 48 B | '0035C630' + 0xE | when qword '02B47758' is null, stores there the result of th"

```
003C98A0  push     rbx
003C98A2  sub      rsp, 0x20
003C98A6  mov      rbx, rcx
003C98A9  mov      rcx, qword ptr [rcx + 0xc8]
003C98B0  test     rcx, rcx
003C98B3  je       0x3c98d8  ; -> 003C98D8
003C98B5  mov      eax, dword ptr [rcx + 0x7c]
003C98B8  and      eax, 0x3ff7ff
003C98BD  or       eax, 0x4b000800
003C98C2  mov      dword ptr [rcx + 0x7c], eax
003C98C5  mov      rcx, qword ptr [rbx + 0xc8]
003C98CC  call     0x244dd0  ; -> 00244DD0 fn
003C98D1  and      dword ptr [rbx + 0xc4], 0xfffffffd
003C98D8  add      rsp, 0x20
003C98DC  pop      rbx
003C98DD  ret      
```
