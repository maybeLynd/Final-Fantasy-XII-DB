# Homing pack: `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-vbf-archive-and-st2e-tables.json`.

Bodies: 3. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0028FF80 (88 B, extent 0028FF80-0028FFD8)

Entered from (direct sites whose caller this page cites): `0035C630` + 0x9 (call; `0035C630` is cited on this page)
Other direct sites: none

Host context: "d (UI bodies '00253780', '00562F90', '00561390' call page-cited '00249210', '002493D0', '00249180'); 12 outbound (page-cited '00558FB0', '00561390', '00253780' call UI bodies '00291D70', '00291D80', '0035C630'). Substantive edges include '002467A0' is called by '00253780'; '00249180' is called by '0035C5B0'; '00249180' is called by '00253780'; '00249210' is called by '00561390'; the remaining edges run through shared helpers the page ci"

```
0028FF80  sub      rsp, 0x28
0028FF84  mov      rcx, qword ptr [rip + 0x1e0bef5]  ; -> 0209BE80
0028FF8B  cmp      qword ptr [rcx + 0x10f80], 0
0028FF93  jne      0x28ffc7  ; -> 0028FFC7
0028FF95  mov      ecx, 0x1d90
0028FF9A  call     0x271420  ; -> 00271420 fn
0028FF9F  mov      rcx, qword ptr [rip + 0x1e0beda]  ; -> 0209BE80
0028FFA6  mov      qword ptr [rcx + 0x10f80], rax
0028FFAD  mov      rcx, qword ptr [rip + 0x1e0becc]  ; -> 0209BE80
0028FFB4  mov      rcx, qword ptr [rcx + 0x10f80]
0028FFBB  call     0x2c63d0  ; -> 002C63D0 fn
0028FFC0  mov      rcx, qword ptr [rip + 0x1e0beb9]  ; -> 0209BE80
0028FFC7  xor      eax, eax
0028FFC9  cmp      qword ptr [rcx + 0x10f80], rax
0028FFD0  setne    al
0028FFD3  add      rsp, 0x28
0028FFD7  ret      
```

## 003C98E0 (31 B, extent 003C98E0-003C98FF)

Entered from (direct sites whose caller this page cites): `0035C630` + 0x13 (call; `0035C630` is cited on this page)
Other direct sites: none

Host context: "d (UI bodies '00253780', '00562F90', '00561390' call page-cited '00249210', '002493D0', '00249180'); 12 outbound (page-cited '00558FB0', '00561390', '00253780' call UI bodies '00291D70', '00291D80', '0035C630'). Substantive edges include '002467A0' is called by '00253780'; '00249180' is called by '0035C5B0'; '00249180' is called by '00253780'; '00249210' is called by '00561390'; the remaining edges run through shared helpers the page ci"

```
003C98E0  cmp      qword ptr [rip + 0x277de58], 0  ; -> 02B47740
003C98E8  jne      0x3c98fe  ; -> 003C98FE
003C98EA  xor      r8d, r8d
003C98ED  lea      rdx, [rip + 0x13c]  ; -> 003C9A30
003C98F4  mov      ecx, 0xd8
003C98F9  jmp      0x244f50  ; -> 00244F50 fn
003C98FE  ret      
```

## 003CA280 (48 B, extent 003CA280-003CA2B0)

Entered from (direct sites whose caller this page cites): `0035C630` + 0xE (call; `0035C630` is cited on this page)
Other direct sites: none

Host context: "d (UI bodies '00253780', '00562F90', '00561390' call page-cited '00249210', '002493D0', '00249180'); 12 outbound (page-cited '00558FB0', '00561390', '00253780' call UI bodies '00291D70', '00291D80', '0035C630'). Substantive edges include '002467A0' is called by '00253780'; '00249180' is called by '0035C5B0'; '00249180' is called by '00253780'; '00249210' is called by '00561390'; the remaining edges run through shared helpers the page ci"

```
003CA280  sub      rsp, 0x28
003CA284  mov      rax, qword ptr [rip + 0x277d4cd]  ; -> 02B47758
003CA28B  test     rax, rax
003CA28E  jne      0x3ca2ab  ; -> 003CA2AB
003CA290  xor      r8d, r8d
003CA293  lea      rdx, [rip + 0x5c6]  ; -> 003CA860
003CA29A  mov      ecx, 0xaa0
003CA29F  call     0x244f50  ; -> 00244F50 fn
003CA2A4  mov      qword ptr [rip + 0x277d4ad], rax  ; -> 02B47758
003CA2AB  add      rsp, 0x28
003CA2AF  ret      
```
