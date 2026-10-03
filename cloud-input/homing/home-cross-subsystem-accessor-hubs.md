# Homing pack: `00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md`

Generated 2026-10-03 08:08 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-cross-subsystem-accessor-hubs.json`.

Bodies: 10. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 003597B0 (31 B, extent 003597B0-003597CF)

Entered from (direct sites whose caller this page cites): `0034C500` + 0x31 (call; `0034C500` is cited on this page)
Other direct sites: `0034C0C0` + 0x14 (call)

Host context: "th the incoming 'rcx' and that call's result as 'edx' | Interior anchor '0034C1DC'; Interior anchor '0034C1E3'; Interior anchor '0034C1EB'; Interior anchor '0034C1F3'; Interior anchor '0034C202' | | '0034C500' | 74 B | calls '00267E10(r9)', then the call at '0034C500'+0x17, passes its result and the '00267E10' value to '00358940', passes that through '00263F10' to the call at '0034C500'+0x31, and tail-jumps to '0026B4E0' with the incomi"

```
003597B0  sub      rsp, 0x28
003597B4  call     0x234d40  ; -> 00234D40 fn
003597B9  sub      eax, 1
003597BC  je       0x3597c8  ; -> 003597C8
003597BE  cmp      eax, 1
003597C1  jne      0x3597c8  ; -> 003597C8
003597C3  add      rsp, 0x28
003597C7  ret      
003597C8  xor      eax, eax
003597CA  add      rsp, 0x28
003597CE  ret      
```

## 003597D0 (46 B, extent 003597D0-003597FE)

Entered from (direct sites whose caller this page cites): `0034CC60` + 0x31 (call; `0034CC60` is cited on this page)
Other direct sites: `0034C8D0` + 0x14 (call)

Host context: "th the incoming 'rcx' and that call's result as 'edx' | Interior anchor '0034C6C9'; Interior anchor '0034C6D1'; Interior anchor '0034C6DA'; Interior anchor '0034C6E2'; Interior anchor '0034C6FB' | | '0034CC60' | 74 B | calls '00267E10(r9)', then the call at '0034CC60'+0x17, passes its result and the '00267E10' value to '00358940', passes that through '00263F10' to the call at '0034CC60'+0x31, and tail-jumps to '0026B4E0' with the incomi"

```
003597D0  sub      rsp, 0x28
003597D4  call     0x234d40  ; -> 00234D40 fn
003597D9  sub      eax, 1
003597DC  je       0x3597f4  ; -> 003597F4
003597DE  cmp      eax, 1
003597E1  je       0x3597ea  ; -> 003597EA
003597E3  xor      eax, eax
003597E5  add      rsp, 0x28
003597E9  ret      
003597EA  mov      eax, 2
003597EF  add      rsp, 0x28
003597F3  ret      
003597F4  mov      eax, 1
003597F9  add      rsp, 0x28
003597FD  ret      
```

## 0035A0C0 (94 B, extent 0035A0C0-0035A11E)

Entered from (direct sites whose caller this page cites): `0034AAD0` + 0x2C (call; `0034AAD0` is cited on this page)
Other direct sites: `0034AF80` + 0x33 (call)

Host context: " 'rcx' and that call's float result moved into 'xmm1' | Interior anchor '0034949C'; Interior anchor '003494A3'; Interior anchor '003494AB'; Interior anchor '003494B0'; Interior anchor '003494BB' | | '0034AAD0' | 74 B | calls '00267E10(r9)' and '00263F10(rdx)', passes that result and the '00267E10' value as 'edx' to the call at '0034AAD0'+0x2C, and tail-jumps to '0026B4E0' with the incoming 'rcx' and that call's result as 'edx' | Interio"

```
0035A0C0  sub      rsp, 0x28
0035A0C4  test     rcx, rcx
0035A0C7  je       0x35a116  ; -> 0035A116
0035A0C9  cmp      edx, 5
0035A0CC  ja       0x35a108  ; -> 0035A108
0035A0CE  movsxd   rax, edx
0035A0D1  lea      r8, [rip - 0x23a0d8]  ; -> 00120000 (image base)
0035A0D8  mov      edx, dword ptr [r8 + rax*4 + 0x23a120]  ; image base + 0x23a120 = 0035A120
0035A0E0  add      rdx, r8
0035A0E3  jmp      rdx
0035A0E5  mov      edx, 1
0035A0EA  jmp      0x35a10a  ; -> 0035A10A
0035A0EC  mov      edx, 2
0035A0F1  jmp      0x35a10a  ; -> 0035A10A
0035A0F3  mov      edx, 3
0035A0F8  jmp      0x35a10a  ; -> 0035A10A
0035A0FA  mov      edx, 4
0035A0FF  jmp      0x35a10a  ; -> 0035A10A
0035A101  mov      edx, 5
0035A106  jmp      0x35a10a  ; -> 0035A10A
0035A108  xor      edx, edx
0035A10A  call     0x31bd80  ; -> 0031BD80 fn
0035A10F  cmp      eax, 0xffff
0035A114  jne      0x35a119  ; -> 0035A119
0035A116  or       eax, 0xffffffff
0035A119  add      rsp, 0x28
0035A11D  ret      
```

## 0036E7B0 (44 B, extent 0036E7B0-0036E7DC)

Entered from (direct sites whose caller this page cites): `00352940` + 0x35 (jmp; `00352940` is cited on this page)
Other direct sites: none

Host context: "3B when byte 'rdx+0x15' is 3, else at '00352270'+0x4A | Interior anchor '00352280'; Interior anchor '0035228A'; Interior anchor '00352292'; Interior anchor '00352297'; Interior anchor '0035229F' | | '00352940' | 58 B | calls '00267E10(r9)' and '003589B0(00263F10(rdx))', then tail-jumps (at '00352940'+0x35) with the '00267E10' value as 'ecx' and the '003589B0' result as 'edx' | Interior anchor '00352950'; Interior anchor '0035295A'; Inte"

```
0036E7B0  test     ecx, ecx
0036E7B2  jns      0x36e7c4  ; -> 0036E7C4
0036E7B4  xor      ecx, ecx
0036E7B6  movsxd   rax, ecx
0036E7B9  lea      rcx, [rip + 0x1f6b0f0]  ; -> 022D98B0
0036E7C0  mov      dword ptr [rcx + rax*4], edx
0036E7C3  ret      
0036E7C4  mov      eax, 0x3f
0036E7C9  cmp      ecx, eax
0036E7CB  cmovg    ecx, eax
0036E7CE  movsxd   rax, ecx
0036E7D1  lea      rcx, [rip + 0x1f6b0d8]  ; -> 022D98B0
0036E7D8  mov      dword ptr [rcx + rax*4], edx
0036E7DB  ret      
```

## 0036E7E0 (44 B, extent 0036E7E0-0036E80C)

Entered from (direct sites whose caller this page cites): `00352270` + 0x4A (jmp; `00352270` is cited on this page)
Other direct sites: none

Host context: "s '00264010(00267E10(r9))' as a qword at '[r8]' and tail-jumps at '00351EE0'+0x20 | Interior anchor '00351EEC'; Interior anchor '00351EF3'; Interior anchor '00351EF8'; Interior anchor '00351F00' | | '00352270' | 79 B | calls '00267E10(r9)' and '003589B0(00263F10(rdx))', then tail-jumps with the '00267E10' value as 'ecx' and the '003589B0' result as 'edx': at '00352270'+0x3B when byte 'rdx+0x15' is 3, else at '00352270'+0x4A | Interior a"

```
0036E7E0  test     ecx, ecx
0036E7E2  jns      0x36e7f4  ; -> 0036E7F4
0036E7E4  xor      ecx, ecx
0036E7E6  movsxd   rax, ecx
0036E7E9  lea      rcx, [rip + 0x1f6afc0]  ; -> 022D97B0
0036E7F0  mov      dword ptr [rcx + rax*4], edx
0036E7F3  ret      
0036E7F4  mov      eax, 0x3f
0036E7F9  cmp      ecx, eax
0036E7FB  cmovg    ecx, eax
0036E7FE  movsxd   rax, ecx
0036E801  lea      rcx, [rip + 0x1f6afa8]  ; -> 022D97B0
0036E808  mov      dword ptr [rcx + rax*4], edx
0036E80B  ret      
```

## 0036E880 (44 B, extent 0036E880-0036E8AC)

Entered from (direct sites whose caller this page cites): `00352270` + 0x3B (jmp; `00352270` is cited on this page)
Other direct sites: none

Host context: "s '00264010(00267E10(r9))' as a qword at '[r8]' and tail-jumps at '00351EE0'+0x20 | Interior anchor '00351EEC'; Interior anchor '00351EF3'; Interior anchor '00351EF8'; Interior anchor '00351F00' | | '00352270' | 79 B | calls '00267E10(r9)' and '003589B0(00263F10(rdx))', then tail-jumps with the '00267E10' value as 'ecx' and the '003589B0' result as 'edx': at '00352270'+0x3B when byte 'rdx+0x15' is 3, else at '00352270'+0x4A | Interior a"

```
0036E880  test     ecx, ecx
0036E882  jns      0x36e894  ; -> 0036E894
0036E884  xor      ecx, ecx
0036E886  movsxd   rax, ecx
0036E889  lea      rcx, [rip + 0x1f6b120]  ; -> 022D99B0
0036E890  mov      dword ptr [rcx + rax*4], edx
0036E893  ret      
0036E894  mov      eax, 0x3f
0036E899  cmp      ecx, eax
0036E89B  cmovg    ecx, eax
0036E89E  movsxd   rax, ecx
0036E8A1  lea      rcx, [rip + 0x1f6b108]  ; -> 022D99B0
0036E8A8  mov      dword ptr [rcx + rax*4], edx
0036E8AB  ret      
```

## 004736E0 (37 B, extent 004736E0-00473705)

Entered from (direct sites whose caller this page cites): `00348800` + 0x23 (call; `00348800` is cited on this page)
Other direct sites: `00340230` + 0x14 (call)

Host context: "and the float written through the 'r9' slot in 'xmm1' | Interior anchor '00347FFC'; Interior anchor '00348003'; Interior anchor '0034801A'; Interior anchor '0034801F'; Interior anchor '00348028' | | '00348800' | 55 B | passes '00263F10(00264010(00267E10(r9)))' to the call at '00348800'+0x23 and tail-jumps to '0026B4E0' with the incoming 'rcx' and that call's result as 'edx' | Interior anchor '0034880C'; Interior anchor '00348813'; Inter"

```
004736E0  sub      rsp, 0x28
004736E4  test     rcx, rcx
004736E7  je       0x4736fe  ; -> 004736FE
004736E9  call     0x3589b0  ; -> 003589B0 fn
004736EE  xor      r8d, r8d
004736F1  xor      edx, edx
004736F3  mov      ecx, eax
004736F5  add      rsp, 0x28
004736F9  jmp      0x3206e0  ; -> 003206E0 fn
004736FE  xor      eax, eax
00473700  add      rsp, 0x28
00473704  ret      
```

## 00473710 (38 B, extent 00473710-00473736)

Entered from (direct sites whose caller this page cites): `0034B060` + 0x23 (call; `0034B060` is cited on this page)
Other direct sites: `003429F0` + 0x14 (call)

Host context: " tail-jumps to '0026B4E0' with the incoming 'rcx' and that call's result as 'edx' | Interior anchor '0034AAE8'; Interior anchor '0034AAF2'; Interior anchor '0034AAFC'; Interior anchor '0034AB15' | | '0034B060' | 55 B | passes '00263F10(00264010(00267E10(r9)))' to the call at '0034B060'+0x23 and tail-jumps to '0026B4E0' with the incoming 'rcx' and that call's result as 'edx' | Interior anchor '0034B06C'; Interior anchor '0034B073'; Inter"

```
00473710  sub      rsp, 0x28
00473714  test     rcx, rcx
00473717  je       0x47372f  ; -> 0047372F
00473719  call     0x3589b0  ; -> 003589B0 fn
0047371E  xor      edx, edx
00473720  mov      ecx, eax
00473722  lea      r8d, [rdx + 0x64]
00473726  add      rsp, 0x28
0047372A  jmp      0x3206e0  ; -> 003206E0 fn
0047372F  xor      eax, eax
00473731  add      rsp, 0x28
00473735  ret      
```

## 00473770 (41 B, extent 00473770-00473799)

Entered from (direct sites whose caller this page cites): `0034C1D0` + 0x23 (call; `0034C1D0` is cited on this page)
Other direct sites: `003434F0` + 0x14 (call)

Host context: "th the incoming 'rcx' and that call's result as 'edx' | Interior anchor '0034B06C'; Interior anchor '0034B073'; Interior anchor '0034B07B'; Interior anchor '0034B083'; Interior anchor '0034B092' | | '0034C1D0' | 55 B | passes '00263F10(00264010(00267E10(r9)))' to the call at '0034C1D0'+0x23 and tail-jumps to '0026B4E0' with the incoming 'rcx' and that call's result as 'edx' | Interior anchor '0034C1DC'; Interior anchor '0034C1E3'; Inter"

```
00473770  sub      rsp, 0x28
00473774  test     rcx, rcx
00473777  je       0x473792  ; -> 00473792
00473779  call     0x3589b0  ; -> 003589B0 fn
0047377E  mov      edx, 1
00473783  mov      ecx, eax
00473785  lea      r8d, [rdx + 0x63]
00473789  add      rsp, 0x28
0047378D  jmp      0x3206e0  ; -> 003206E0 fn
00473792  xor      eax, eax
00473794  add      rsp, 0x28
00473798  ret      
```

## 004737A0 (46 B, extent 004737A0-004737CE)

Entered from (direct sites whose caller this page cites): `0034C6A0` + 0x42 (call; `0034C6A0` is cited on this page)
Other direct sites: none

Host context: "th the incoming 'rcx' and that call's result as 'edx' | Interior anchor '0034C510'; Interior anchor '0034C521'; Interior anchor '0034C529'; Interior anchor '0034C531'; Interior anchor '0034C545' | | '0034C6A0' | 96 B | calls '00267E10(r9)' twice, passes the second value through '00264010' and '00263F10', calls '0034C6A0'+0x42 with that result and the first value clamped to 0 when negative, and tail-jumps to '0026B4E0' with the incoming "

```
004737A0  push     rbx
004737A2  sub      rsp, 0x20
004737A6  mov      ebx, edx
004737A8  test     rcx, rcx
004737AB  je       0x4737c6  ; -> 004737C6
004737AD  call     0x3589b0  ; -> 003589B0 fn
004737B2  mov      r8d, ebx
004737B5  mov      edx, 1
004737BA  mov      ecx, eax
004737BC  add      rsp, 0x20
004737C0  pop      rbx
004737C1  jmp      0x3206e0  ; -> 003206E0 fn
004737C6  xor      eax, eax
004737C8  add      rsp, 0x20
004737CC  pop      rbx
004737CD  ret      
```
