# Homing pack: `00-Engine-Core-Runtime/CONTRACT-boot-fixups.md`

Generated 2026-10-02 22:54 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-contract-boot-fixups.json`.

Bodies: 16. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0035D070 (12 B, extent 0035D070-0035D07C)

Entered from (direct sites whose caller this page cites): `003C6000` + 0x13 (call; `003C6000` is cited on this page)
Other direct sites: none

Host context: ".** 18 inbound (UI bodies '0024B9B0', '003FA790', '0035D6B0' call page-cited '001EDEC0', '00229EA0', '001EDDA0'); 4 outbound (page-cited '002507C0', '00250540' call UI bodies '00367200', '0035BC40', '003C6000'). Substantive edges include '001EDE80' is called by '003FA790'; '00250540' calls '00367200'; '002507C0' calls '00367200'; '002507C0' calls '0035BC40'; the remaining edges run through shared helpers the page cites. - **Party — SERV"

```
0035D070  lea      rcx, [rip + 0x1f6afe9]  ; -> 022C8060
0035D077  jmp      0x35e5f0  ; -> 0035E5F0 fn
```

## 0044D460 (54 B, extent 0044D460-0044D496)

Entered from (direct sites whose caller this page cites): `002F3BC0` + 0xCA (call; `002F3BC0` is cited on this page)
Other direct sites: none

Host context: "VIF-program state-block initializers — '0037DF90' calls '0047E140'/'0048AB40'/'0048CE70'/ '0048F410'/'004B8F20' — and this page's '001EBA40'/'001EDDA0' are called by '00187950'/'001F9B20'/'002F2530'/'002F3BC0' on that layer. The fixups construct Presentation statics; the page's subject is the construction, not the render layer.  '004B8F20' (2250 B) is the state-block initializer for '02AE4F20': '008631E0'/'008631D0' open the descriptor "

```
0044D460  push     rbx
0044D462  sub      rsp, 0x20
0044D466  mov      rbx, rcx
0044D469  call     0x2f2d60  ; -> 002F2D60 fn
0044D46E  test     eax, eax
0044D470  jne      0x44d478  ; -> 0044D478
0044D472  add      rsp, 0x20
0044D476  pop      rbx
0044D477  ret      
0044D478  mov      rcx, rbx
0044D47B  call     0x44d840  ; -> 0044D840 fn
0044D480  call     0x44b960  ; -> 0044B960 fn
0044D485  mov      dword ptr [rbx + 0x258], eax
0044D48B  mov      eax, 1
0044D490  add      rsp, 0x20
0044D494  pop      rbx
0044D495  ret      
```

## 0044ED90 (54 B, extent 0044ED90-0044EDC6)

Entered from (direct sites whose caller this page cites): `002F3BC0` + 0xF1 (call; `002F3BC0` is cited on this page)
Other direct sites: none

Host context: "VIF-program state-block initializers — '0037DF90' calls '0047E140'/'0048AB40'/'0048CE70'/ '0048F410'/'004B8F20' — and this page's '001EBA40'/'001EDDA0' are called by '00187950'/'001F9B20'/'002F2530'/'002F3BC0' on that layer. The fixups construct Presentation statics; the page's subject is the construction, not the render layer.  '004B8F20' (2250 B) is the state-block initializer for '02AE4F20': '008631E0'/'008631D0' open the descriptor "

```
0044ED90  push     rbx
0044ED92  sub      rsp, 0x20
0044ED96  mov      rbx, rcx
0044ED99  call     0x2f2d60  ; -> 002F2D60 fn
0044ED9E  test     eax, eax
0044EDA0  jne      0x44eda8  ; -> 0044EDA8
0044EDA2  add      rsp, 0x20
0044EDA6  pop      rbx
0044EDA7  ret      
0044EDA8  mov      rcx, rbx
0044EDAB  call     0x44f4c0  ; -> 0044F4C0 fn
0044EDB0  call     0x44b960  ; -> 0044B960 fn
0044EDB5  mov      dword ptr [rbx + 0x244], eax
0044EDBB  mov      eax, 1
0044EDC0  add      rsp, 0x20
0044EDC4  pop      rbx
0044EDC5  ret      
```

## 0044F930 (54 B, extent 0044F930-0044F966)

Entered from (direct sites whose caller this page cites): `002F3BC0` + 0xFE (call; `002F3BC0` is cited on this page)
Other direct sites: none

Host context: "VIF-program state-block initializers — '0037DF90' calls '0047E140'/'0048AB40'/'0048CE70'/ '0048F410'/'004B8F20' — and this page's '001EBA40'/'001EDDA0' are called by '00187950'/'001F9B20'/'002F2530'/'002F3BC0' on that layer. The fixups construct Presentation statics; the page's subject is the construction, not the render layer.  '004B8F20' (2250 B) is the state-block initializer for '02AE4F20': '008631E0'/'008631D0' open the descriptor "

```
0044F930  push     rbx
0044F932  sub      rsp, 0x20
0044F936  mov      rbx, rcx
0044F939  call     0x2f2d60  ; -> 002F2D60 fn
0044F93E  test     eax, eax
0044F940  jne      0x44f948  ; -> 0044F948
0044F942  add      rsp, 0x20
0044F946  pop      rbx
0044F947  ret      
0044F948  mov      rcx, rbx
0044F94B  call     0x4500c0  ; -> 004500C0 fn
0044F950  call     0x44b960  ; -> 0044B960 fn
0044F955  mov      dword ptr [rbx + 0x454], eax
0044F95B  mov      eax, 1
0044F960  add      rsp, 0x20
0044F964  pop      rbx
0044F965  ret      
```

## 00451140 (54 B, extent 00451140-00451176)

Entered from (direct sites whose caller this page cites): `002F3BC0` + 0x118 (call; `002F3BC0` is cited on this page)
Other direct sites: none

Host context: "VIF-program state-block initializers — '0037DF90' calls '0047E140'/'0048AB40'/'0048CE70'/ '0048F410'/'004B8F20' — and this page's '001EBA40'/'001EDDA0' are called by '00187950'/'001F9B20'/'002F2530'/'002F3BC0' on that layer. The fixups construct Presentation statics; the page's subject is the construction, not the render layer.  '004B8F20' (2250 B) is the state-block initializer for '02AE4F20': '008631E0'/'008631D0' open the descriptor "

```
00451140  push     rbx
00451142  sub      rsp, 0x20
00451146  mov      rbx, rcx
00451149  call     0x2f2d60  ; -> 002F2D60 fn
0045114E  test     eax, eax
00451150  jne      0x451158  ; -> 00451158
00451152  add      rsp, 0x20
00451156  pop      rbx
00451157  ret      
00451158  mov      rcx, rbx
0045115B  call     0x450ce0  ; -> 00450CE0 fn
00451160  call     0x44b960  ; -> 0044B960 fn
00451165  mov      dword ptr [rbx + 0x290], eax
0045116B  mov      eax, 1
00451170  add      rsp, 0x20
00451174  pop      rbx
00451175  ret      
```

## 00451890 (54 B, extent 00451890-004518C6)

Entered from (direct sites whose caller this page cites): `002F3BC0` + 0x125 (call; `002F3BC0` is cited on this page)
Other direct sites: none

Host context: "VIF-program state-block initializers — '0037DF90' calls '0047E140'/'0048AB40'/'0048CE70'/ '0048F410'/'004B8F20' — and this page's '001EBA40'/'001EDDA0' are called by '00187950'/'001F9B20'/'002F2530'/'002F3BC0' on that layer. The fixups construct Presentation statics; the page's subject is the construction, not the render layer.  '004B8F20' (2250 B) is the state-block initializer for '02AE4F20': '008631E0'/'008631D0' open the descriptor "

```
00451890  push     rbx
00451892  sub      rsp, 0x20
00451896  mov      rbx, rcx
00451899  call     0x2f2d60  ; -> 002F2D60 fn
0045189E  test     eax, eax
004518A0  jne      0x4518a8  ; -> 004518A8
004518A2  add      rsp, 0x20
004518A6  pop      rbx
004518A7  ret      
004518A8  mov      rcx, rbx
004518AB  call     0x452020  ; -> 00452020 fn
004518B0  call     0x44b960  ; -> 0044B960 fn
004518B5  mov      dword ptr [rbx + 0x290], eax
004518BB  mov      eax, 1
004518C0  add      rsp, 0x20
004518C4  pop      rbx
004518C5  ret      
```

## 00453CB0 (54 B, extent 00453CB0-00453CE6)

Entered from (direct sites whose caller this page cites): `002F3BC0` + 0x14C (call; `002F3BC0` is cited on this page)
Other direct sites: none

Host context: "VIF-program state-block initializers — '0037DF90' calls '0047E140'/'0048AB40'/'0048CE70'/ '0048F410'/'004B8F20' — and this page's '001EBA40'/'001EDDA0' are called by '00187950'/'001F9B20'/'002F2530'/'002F3BC0' on that layer. The fixups construct Presentation statics; the page's subject is the construction, not the render layer.  '004B8F20' (2250 B) is the state-block initializer for '02AE4F20': '008631E0'/'008631D0' open the descriptor "

```
00453CB0  push     rbx
00453CB2  sub      rsp, 0x20
00453CB6  mov      rbx, rcx
00453CB9  call     0x2f2d60  ; -> 002F2D60 fn
00453CBE  test     eax, eax
00453CC0  jne      0x453cc8  ; -> 00453CC8
00453CC2  add      rsp, 0x20
00453CC6  pop      rbx
00453CC7  ret      
00453CC8  mov      rcx, rbx
00453CCB  call     0x454480  ; -> 00454480 fn
00453CD0  call     0x44b960  ; -> 0044B960 fn
00453CD5  mov      dword ptr [rbx + 0x244], eax
00453CDB  mov      eax, 1
00453CE0  add      rsp, 0x20
00453CE4  pop      rbx
00453CE5  ret      
```

## 004548F0 (54 B, extent 004548F0-00454926)

Entered from (direct sites whose caller this page cites): `002F3BC0` + 0x159 (call; `002F3BC0` is cited on this page)
Other direct sites: none

Host context: "VIF-program state-block initializers — '0037DF90' calls '0047E140'/'0048AB40'/'0048CE70'/ '0048F410'/'004B8F20' — and this page's '001EBA40'/'001EDDA0' are called by '00187950'/'001F9B20'/'002F2530'/'002F3BC0' on that layer. The fixups construct Presentation statics; the page's subject is the construction, not the render layer.  '004B8F20' (2250 B) is the state-block initializer for '02AE4F20': '008631E0'/'008631D0' open the descriptor "

```
004548F0  push     rbx
004548F2  sub      rsp, 0x20
004548F6  mov      rbx, rcx
004548F9  call     0x2f2d60  ; -> 002F2D60 fn
004548FE  test     eax, eax
00454900  jne      0x454908  ; -> 00454908
00454902  add      rsp, 0x20
00454906  pop      rbx
00454907  ret      
00454908  mov      rcx, rbx
0045490B  call     0x454f90  ; -> 00454F90 fn
00454910  call     0x44b960  ; -> 0044B960 fn
00454915  mov      dword ptr [rbx + 0x290], eax
0045491B  mov      eax, 1
00454920  add      rsp, 0x20
00454924  pop      rbx
00454925  ret      
```

## 0045BF50 (87 B, extent 0045BF50-0045BFA7)

Entered from (direct sites whose caller this page cites): `002F3BC0` + 0x1E8 (call; `002F3BC0` is cited on this page)
Other direct sites: none

Host context: "VIF-program state-block initializers — '0037DF90' calls '0047E140'/'0048AB40'/'0048CE70'/ '0048F410'/'004B8F20' — and this page's '001EBA40'/'001EDDA0' are called by '00187950'/'001F9B20'/'002F2530'/'002F3BC0' on that layer. The fixups construct Presentation statics; the page's subject is the construction, not the render layer.  '004B8F20' (2250 B) is the state-block initializer for '02AE4F20': '008631E0'/'008631D0' open the descriptor "

```
0045BF50  push     rbx
0045BF52  sub      rsp, 0x20
0045BF56  mov      rbx, rcx
0045BF59  call     0x2f2d60  ; -> 002F2D60 fn
0045BF5E  test     eax, eax
0045BF60  jne      0x45bf68  ; -> 0045BF68
0045BF62  add      rsp, 0x20
0045BF66  pop      rbx
0045BF67  ret      
0045BF68  mov      qword ptr [rsp + 0x30], rdi
0045BF6D  mov      edi, 1
0045BF72  mov      dword ptr [rbx + 0x24c], 0x10001
0045BF7C  call     0x44b960  ; -> 0044B960 fn
0045BF81  mov      dword ptr [rbx + 0x244], eax
0045BF87  call     0x44b960  ; -> 0044B960 fn
0045BF8C  mov      rcx, rbx
0045BF8F  mov      dword ptr [rbx + 0x248], eax
0045BF95  call     0x45c450  ; -> 0045C450 fn
0045BF9A  mov      eax, edi
0045BF9C  mov      rdi, qword ptr [rsp + 0x30]
0045BFA1  add      rsp, 0x20
0045BFA5  pop      rbx
0045BFA6  ret      
```

## 0045C920 (87 B, extent 0045C920-0045C977)

Entered from (direct sites whose caller this page cites): `002F3BC0` + 0x1F5 (call; `002F3BC0` is cited on this page)
Other direct sites: none

Host context: "VIF-program state-block initializers — '0037DF90' calls '0047E140'/'0048AB40'/'0048CE70'/ '0048F410'/'004B8F20' — and this page's '001EBA40'/'001EDDA0' are called by '00187950'/'001F9B20'/'002F2530'/'002F3BC0' on that layer. The fixups construct Presentation statics; the page's subject is the construction, not the render layer.  '004B8F20' (2250 B) is the state-block initializer for '02AE4F20': '008631E0'/'008631D0' open the descriptor "

```
0045C920  push     rbx
0045C922  sub      rsp, 0x20
0045C926  mov      rbx, rcx
0045C929  call     0x2f2d60  ; -> 002F2D60 fn
0045C92E  test     eax, eax
0045C930  jne      0x45c938  ; -> 0045C938
0045C932  add      rsp, 0x20
0045C936  pop      rbx
0045C937  ret      
0045C938  mov      qword ptr [rsp + 0x30], rdi
0045C93D  mov      edi, 1
0045C942  mov      dword ptr [rbx + 0x24c], 0x10001
0045C94C  call     0x44b960  ; -> 0044B960 fn
0045C951  mov      dword ptr [rbx + 0x244], eax
0045C957  call     0x44b960  ; -> 0044B960 fn
0045C95C  mov      rcx, rbx
0045C95F  mov      dword ptr [rbx + 0x248], eax
0045C965  call     0x45cdc0  ; -> 0045CDC0 fn
0045C96A  mov      eax, edi
0045C96C  mov      rdi, qword ptr [rsp + 0x30]
0045C971  add      rsp, 0x20
0045C975  pop      rbx
0045C976  ret      
```

## 0045D290 (87 B, extent 0045D290-0045D2E7)

Entered from (direct sites whose caller this page cites): `002F3BC0` + 0x202 (call; `002F3BC0` is cited on this page)
Other direct sites: none

Host context: "VIF-program state-block initializers — '0037DF90' calls '0047E140'/'0048AB40'/'0048CE70'/ '0048F410'/'004B8F20' — and this page's '001EBA40'/'001EDDA0' are called by '00187950'/'001F9B20'/'002F2530'/'002F3BC0' on that layer. The fixups construct Presentation statics; the page's subject is the construction, not the render layer.  '004B8F20' (2250 B) is the state-block initializer for '02AE4F20': '008631E0'/'008631D0' open the descriptor "

```
0045D290  push     rbx
0045D292  sub      rsp, 0x20
0045D296  mov      rbx, rcx
0045D299  call     0x2f2d60  ; -> 002F2D60 fn
0045D29E  test     eax, eax
0045D2A0  jne      0x45d2a8  ; -> 0045D2A8
0045D2A2  add      rsp, 0x20
0045D2A6  pop      rbx
0045D2A7  ret      
0045D2A8  mov      qword ptr [rsp + 0x30], rdi
0045D2AD  mov      edi, 1
0045D2B2  mov      dword ptr [rbx + 0x24c], 0x10001
0045D2BC  call     0x44b960  ; -> 0044B960 fn
0045D2C1  mov      dword ptr [rbx + 0x244], eax
0045D2C7  call     0x44b960  ; -> 0044B960 fn
0045D2CC  mov      rcx, rbx
0045D2CF  mov      dword ptr [rbx + 0x248], eax
0045D2D5  call     0x45d7d0  ; -> 0045D7D0 fn
0045D2DA  mov      eax, edi
0045D2DC  mov      rdi, qword ptr [rsp + 0x30]
0045D2E1  add      rsp, 0x20
0045D2E5  pop      rbx
0045D2E6  ret      
```

## 0045DCA0 (112 B, extent 0045DCA0-0045DD10)

Entered from (direct sites whose caller this page cites): `002F3BC0` + 0x20C (call; `002F3BC0` is cited on this page)
Other direct sites: none

Host context: "VIF-program state-block initializers — '0037DF90' calls '0047E140'/'0048AB40'/'0048CE70'/ '0048F410'/'004B8F20' — and this page's '001EBA40'/'001EDDA0' are called by '00187950'/'001F9B20'/'002F2530'/'002F3BC0' on that layer. The fixups construct Presentation statics; the page's subject is the construction, not the render layer.  '004B8F20' (2250 B) is the state-block initializer for '02AE4F20': '008631E0'/'008631D0' open the descriptor "

```
0045DCA0  push     rbx
0045DCA2  sub      rsp, 0x20
0045DCA6  mov      rbx, rcx
0045DCA9  call     0x2f2d60  ; -> 002F2D60 fn
0045DCAE  test     eax, eax
0045DCB0  jne      0x45dcb8  ; -> 0045DCB8
0045DCB2  add      rsp, 0x20
0045DCB6  pop      rbx
0045DCB7  ret      
0045DCB8  lea      rcx, [rbx + 0x2a0]
0045DCBF  mov      qword ptr [rsp + 0x30], rdi
0045DCC4  xor      edx, edx
0045DCC6  call     0x3a3e20  ; -> 003A3E20 fn
0045DCCB  mov      edi, 1
0045DCD0  mov      dword ptr [rbx + 0x2f0], 0x10001
0045DCDA  call     0x44b960  ; -> 0044B960 fn
0045DCDF  mov      dword ptr [rbx + 0x254], eax
0045DCE5  call     0x44b960  ; -> 0044B960 fn
0045DCEA  mov      dword ptr [rbx + 0x258], eax
0045DCF0  call     0x44b960  ; -> 0044B960 fn
0045DCF5  mov      rcx, rbx
0045DCF8  mov      dword ptr [rbx + 0x25c], eax
0045DCFE  call     0x45e3c0  ; -> 0045E3C0 fn
0045DD03  mov      eax, edi
0045DD05  mov      rdi, qword ptr [rsp + 0x30]
0045DD0A  add      rsp, 0x20
0045DD0E  pop      rbx
0045DD0F  ret      
```

## 0045E8C0 (112 B, extent 0045E8C0-0045E930)

Entered from (direct sites whose caller this page cites): `002F3BC0` + 0x216 (call; `002F3BC0` is cited on this page)
Other direct sites: none

Host context: "VIF-program state-block initializers — '0037DF90' calls '0047E140'/'0048AB40'/'0048CE70'/ '0048F410'/'004B8F20' — and this page's '001EBA40'/'001EDDA0' are called by '00187950'/'001F9B20'/'002F2530'/'002F3BC0' on that layer. The fixups construct Presentation statics; the page's subject is the construction, not the render layer.  '004B8F20' (2250 B) is the state-block initializer for '02AE4F20': '008631E0'/'008631D0' open the descriptor "

```
0045E8C0  push     rbx
0045E8C2  sub      rsp, 0x20
0045E8C6  mov      rbx, rcx
0045E8C9  call     0x2f2d60  ; -> 002F2D60 fn
0045E8CE  test     eax, eax
0045E8D0  jne      0x45e8d8  ; -> 0045E8D8
0045E8D2  add      rsp, 0x20
0045E8D6  pop      rbx
0045E8D7  ret      
0045E8D8  lea      rcx, [rbx + 0x2a0]
0045E8DF  mov      qword ptr [rsp + 0x30], rdi
0045E8E4  xor      edx, edx
0045E8E6  call     0x3a3e20  ; -> 003A3E20 fn
0045E8EB  mov      edi, 1
0045E8F0  mov      dword ptr [rbx + 0x2f0], 0x10001
0045E8FA  call     0x44b960  ; -> 0044B960 fn
0045E8FF  mov      dword ptr [rbx + 0x254], eax
0045E905  call     0x44b960  ; -> 0044B960 fn
0045E90A  mov      dword ptr [rbx + 0x258], eax
0045E910  call     0x44b960  ; -> 0044B960 fn
0045E915  mov      rcx, rbx
0045E918  mov      dword ptr [rbx + 0x25c], eax
0045E91E  call     0x45f140  ; -> 0045F140 fn
0045E923  mov      eax, edi
0045E925  mov      rdi, qword ptr [rsp + 0x30]
0045E92A  add      rsp, 0x20
0045E92E  pop      rbx
0045E92F  ret      
```

## 004CF230 (78 B, extent 004CF230-004CF27E)

Entered from (direct sites whose caller this page cites): `004C8320` + 0x396A (call; `004C8320` is cited on this page); `004C8320` + 0x3D0E (call; `004C8320` is cited on this page); `004C8320` + 0x3EF5 (call; `004C8320` is cited on this page); `004C8320` + 0x3F08 (call; `004C8320` is cited on this page); `004C8320` + 0x4BCF (call; `004C8320` is cited on this page); `004C8320` + 0x4BE2 (call; `004C8320` is cited on this page); `004C8320` + 0x5706 (call; `004C8320` is cited on this page); `004C8320` + 0x5719 (call; `004C8320` is cited on this page); `004C8320` + 0x6220 (call; `004C8320` is cited on this page); `004C8320` + 0x623D (call; `004C8320` is cited on this page)
Other direct sites: none

Host context: "onstant fill - a module record's init.  Interior anchor '004EC973' (function '004EC960').  '004C8080' (509 B) is a battery constructor '0037E0F0' calls: '00861EC0' zeroes first, '008631E0' registers '004C8320', '008631D0(0x27)' fills '+0x10', then '+0xC' = 0x02000000, '+0x18' = 0x1000404, '+0x1C' = 0x6C260000 - the largest field count of the family.  Interior anchor '004C8097' (function '004C8080').  '004DCA00' (507 B) is a battery cons" / "onstant fill - a module record's init.  Interior anchor '004EC973' (function '004EC960').  '004C8080' (509 B) is a battery constructor '0037E0F0' calls: '00861EC0' zeroes first, '008631E0' registers '004C8320', '008631D0(0x27)' fills '+0x10', then '+0xC' = 0x02000000, '+0x18' = 0x1000404, '+0x1C' = 0x6C260000 - the largest field count of the family.  Interior anchor '004C8097' (function '004C8080').  '004DCA00' (507 B) is a battery cons"

```
004CF230  movss    xmm0, dword ptr [rdx]
004CF234  minss    xmm0, xmm2
004CF238  movss    dword ptr [rcx], xmm0
004CF23C  movss    xmm1, dword ptr [rdx + 4]
004CF241  comiss   xmm2, xmm1
004CF244  jbe      0x4cf24d  ; -> 004CF24D
004CF246  movss    dword ptr [rcx + 4], xmm1
004CF24B  jmp      0x4cf252  ; -> 004CF252
004CF24D  movss    dword ptr [rcx + 4], xmm2
004CF252  movss    xmm0, dword ptr [rdx + 8]
004CF257  comiss   xmm2, xmm0
004CF25A  jbe      0x4cf263  ; -> 004CF263
004CF25C  movss    dword ptr [rcx + 8], xmm0
004CF261  jmp      0x4cf268  ; -> 004CF268
004CF263  movss    dword ptr [rcx + 8], xmm2
004CF268  movss    xmm0, dword ptr [rdx + 0xc]
004CF26D  comiss   xmm2, xmm0
004CF270  jbe      0x4cf278  ; -> 004CF278
004CF272  movss    dword ptr [rcx + 0xc], xmm0
004CF277  ret      
004CF278  movss    dword ptr [rcx + 0xc], xmm2
004CF27D  ret      
```

## 004E7980 (52 B, extent 004E7980-004E79B4)

Entered from (direct sites whose caller this page cites): `0037E0F0` + 0x9B (call; `0037E0F0` is cited on this page)
Other direct sites: none

Host context: " save data passes both and fails the third. Test I3 at both frame limits and assert the triple is written **only** at 60. Compare all nine registrations and both unregistered allocation sizes (I4).  '0037E0F0' (596 B) is the register battery '0022A0B0' runs inside the boot subtree: ~~46 straight 'lea rcx, 02AE9xxx'/'02AEAxxx'/'02AEBxxx'/'02AECxxx' globals each handed to a '004C2040'/'004Dxxxx'/'004Exxxx'/'004Fxxxx' initializer~~ 49 'lea"

```
004E7980  push     rbx
004E7982  sub      rsp, 0x20
004E7986  xor      r8d, r8d
004E7989  lea      rdx, [rip + 0x400]  ; -> 004E7D90
004E7990  mov      rbx, rcx
004E7993  call     0x8631e0  ; -> 008631E0 fn
004E7998  lea      rcx, [rbx + 0x10]
004E799C  mov      dword ptr [rbx + 8], 0x3000000
004E79A3  mov      dword ptr [rbx + 0xc], 0x2000000
004E79AA  add      rsp, 0x20
004E79AE  pop      rbx
004E79AF  jmp      0x4e7a90  ; -> 004E7A90 fn
```

## 004EB910 (1387 B, extent 004EB910-004EBE7B)

Entered from (direct sites whose caller this page cites): `004EBE80` + 0x74A (call; `004EBE80` is cited on this page); `004EBE80` + 0x804 (call; `004EBE80` is cited on this page); `004EBE80` + 0x8BE (call; `004EBE80` is cited on this page); `004EBE80` + 0x978 (call; `004EBE80` is cited on this page); `004EBE80` + 0xA25 (call; `004EBE80` is cited on this page)
Other direct sites: none

Host context: "00') at '+0x1C'/'+0x20'/'+0x24' - a module record's field init.  Interior anchor '004DB06E' (function '004DB060').  '004EC960' (515 B) is a battery constructor '0037E0F0' calls: '008631E0' registers '004EBE80', '008631D0(0x11)' fills '+0x10', then '+0xC' = 0x02000000, '+0x18' = 0x1000404, '+0x1C' = 0x6C0E0000 head the constant fill - a module record's init.  Interior anchor '004EC973' (function '004EC960').  '004C8080' (509 B) is a batt" / "00') at '+0x1C'/'+0x20'/'+0x24' - a module record's field init.  Interior anchor '004DB06E' (function '004DB060').  '004EC960' (515 B) is a battery constructor '0037E0F0' calls: '008631E0' registers '004EBE80', '008631D0(0x11)' fills '+0x10', then '+0xC' = 0x02000000, '+0x18' = 0x1000404, '+0x1C' = 0x6C0E0000 head the constant fill - a module record's init.  Interior anchor '004EC973' (function '004EC960').  '004C8080' (509 B) is a batt"

```
004EB910  push     rbx
004EB912  sub      rsp, 0x60
004EB916  movss    xmm5, dword ptr [rip + 0x1b793e6]  ; -> 02064D04
004EB91E  lea      rbx, [rip + 0x1b7950b]  ; -> 02064E30
004EB925  movss    xmm3, dword ptr [rip + 0x1b793d3]  ; -> 02064D00
004EB92D  movaps   xmm2, xmm5
004EB930  mulss    xmm5, dword ptr [rip + 0x1b792c8]  ; -> 02064C00
004EB938  movaps   xmm1, xmm3
004EB93B  movsx    edx, word ptr [rip + 0x1b791ca]  ; -> 02064B0C
004EB942  mulss    xmm1, dword ptr [rip + 0x1b792a6]  ; -> 02064BF0
004EB94A  inc      word ptr [rip + 0x1b79467]  ; -> 02064DB8
004EB951  mulss    xmm3, dword ptr [rip + 0x1b792a7]  ; -> 02064C00
004EB959  lea      eax, [rdx + 2]
004EB95C  mulss    xmm2, dword ptr [rip + 0x1b7928c]  ; -> 02064BF0
004EB964  shl      eax, 4
004EB967  cmp      word ptr [rip + 0x1b7944e], dx  ; -> 02064DBC
004EB96E  movaps   xmmword ptr [rsp + 0x50], xmm6
004EB973  movss    xmm6, dword ptr [rip + 0x1b79399]  ; -> 02064D14
004EB97B  movaps   xmmword ptr [rsp + 0x40], xmm7
004EB980  movss    xmm7, dword ptr [rip + 0x1b79388]  ; -> 02064D10
004EB988  movaps   xmm4, xmm7
004EB98B  movaps   xmmword ptr [rsp + 0x30], xmm8
004EB991  mulss    xmm7, dword ptr [rip + 0x1b7926b]  ; -> 02064C04
004EB999  movsxd   rcx, eax
004EB99C  mulss    xmm4, dword ptr [rip + 0x1b79250]  ; -> 02064BF4
004EB9A4  addss    xmm7, xmm3
004EB9A8  movaps   xmmword ptr [rsp + 0x20], xmm9
004EB9AE  movss    dword ptr [rip + 0x1b7916e], xmm5  ; -> 02064B24
004EB9B6  movups   xmm8, xmmword ptr [rcx + rbx]
004EB9BB  addss    xmm4, xmm1
004EB9BF  movss    dword ptr [rip + 0x1b79159], xmm3  ; -> 02064B20
004EB9C7  movups   xmmword ptr [rip + 0x1b79291], xmm8  ; -> 02064C60
004EB9CF  movss    xmm0, dword ptr [rip + 0x1b79291]  ; -> 02064C68
004EB9D7  movaps   xmm1, xmm6
004EB9DA  mulss    xmm1, dword ptr [rip + 0x1b79212]  ; -> 02064BF4
004EB9E2  movups   xmm9, xmm8
004EB9E6  mulss    xmm6, dword ptr [rip + 0x1b79216]  ; -> 02064C04
004EB9EE  addss    xmm9, xmm7
004EB9F3  movups   xmmword ptr [rip + 0x1b79275], xmm8  ; -> 02064C70
004EB9FB  addss    xmm1, xmm2
004EB9FF  movss    dword ptr [rip + 0x1b79211], xmm0  ; -> 02064C18
004EBA07  movss    xmm0, dword ptr [rip + 0x1b79269]  ; -> 02064C78
004EBA0F  addss    xmm6, xmm5
004EBA13  movss    xmm5, dword ptr [rip + 0x1b79249]  ; -> 02064C64
004EBA1B  addss    xmm8, xmm4
004EBA20  movss    dword ptr [rip + 0x1b79200], xmm0  ; -> 02064C28
004EBA28  movss    dword ptr [rip + 0x1b791d0], xmm7  ; -> 02064C00
004EBA30  movss    xmm7, dword ptr [rip + 0x1b7923c]  ; -> 02064C74
004EBA38  addss    xmm5, xmm1
004EBA3C  movss    dword ptr [rip + 0x1b791b0], xmm1  ; -> 02064BF4
004EBA44  addss    xmm7, xmm6
004EBA48  movss    xmm1, dword ptr [rip + 0x1b7921c]  ; -> 02064C6C
004EBA50  movss    dword ptr [rip + 0x1b791c4], xmm1  ; -> 02064C1C
004EBA58  movss    xmm1, dword ptr [rip + 0x1b7921c]  ; -> 02064C7C
004EBA60  movss    dword ptr [rip + 0x1b791fc], xmm5  ; -> 02064C64
004EBA68  movss    dword ptr [rip + 0x1b791ef], xmm8  ; -> 02064C60
004EBA71  movups   xmm0, xmmword ptr [rip + 0x1b791e8]  ; -> 02064C60
004EBA78  movss    dword ptr [rip + 0x1b791ef], xmm9  ; -> 02064C70
004EBA81  mulps    xmm0, xmmword ptr [rip + 0x429968]  ; -> 009153F0 [f32x4 16, 16, 16, 16]
004EBA88  movss    dword ptr [rip + 0x1b791e4], xmm7  ; -> 02064C74
004EBA90  movss    dword ptr [rip + 0x1b79194], xmm1  ; -> 02064C2C
004EBA98  movups   xmm1, xmmword ptr [rip + 0x1b791d1]  ; -> 02064C70
004EBA9F  cvttps2dq xmm0, xmm0
004EBAA3  mulps    xmm1, xmmword ptr [rip + 0x429946]  ; -> 009153F0 [f32x4 16, 16, 16, 16]
004EBAAA  movdqu   xmmword ptr [rip + 0x1b791ae], xmm0  ; -> 02064C60
004EBAB2  movss    dword ptr [rip + 0x1b7914a], xmm6  ; -> 02064C04
004EBABA  xorps    xmm6, xmm6
004EBABD  cvttps2dq xmm0, xmm1
004EBAC1  movss    dword ptr [rip + 0x1b79127], xmm4  ; -> 02064BF0
004EBAC9  movdqu   xmmword ptr [rip + 0x1b7919f], xmm0  ; -> 02064C70
004EBAD1  movss    dword ptr [rip + 0x1b79146], xmm9  ; -> 02064C20
004EBADA  movss    dword ptr [rip + 0x1b79142], xmm7  ; -> 02064C24
004EBAE2  je       0x4ebbf5  ; -> 004EBBF5
004EBAE8  movss    xmm2, dword ptr [rip + 0x1b79200]  ; -> 02064CF0
004EBAF0  mulss    xmm2, dword ptr [rip + 0x1b79188]  ; -> 02064C80
004EBAF8  movss    xmm1, dword ptr [rip + 0x1b791f4]  ; -> 02064CF4
004EBB00  mulss    xmm1, dword ptr [rip + 0x1b79178]  ; -> 02064C80
004EBB08  subss    xmm8, xmm2
004EBB0D  movss    dword ptr [rip + 0x1b7911b], xmm2  ; -> 02064C30
004EBB15  subss    xmm5, xmm1
004EBB19  movss    dword ptr [rip + 0x1b79113], xmm1  ; -> 02064C34
004EBB21  ucomiss  xmm8, xmm6
004EBB25  movss    dword ptr [rip + 0x1b790e2], xmm8  ; -> 02064C10
004EBB2E  movss    dword ptr [rip + 0x1b790de], xmm5  ; -> 02064C14
004EBB36  jp       0x4ebb3a  ; -> 004EBB3A
004EBB38  je       0x4ebb41  ; -> 004EBB41
004EBB3A  ucomiss  xmm5, xmm6
004EBB3D  jp       0x4ebb57  ; -> 004EBB57
004EBB3F  jne      0x4ebb57  ; -> 004EBB57
004EBB41  call     0x22cc40  ; -> 0022CC40 fn
004EBB46  movss    xmm5, dword ptr [rip + 0x1b790c6]  ; -> 02064C14
004EBB4E  movss    xmm8, dword ptr [rip + 0x1b790b9]  ; -> 02064C10
004EBB57  comiss   xmm6, xmm8
004EBB5B  ja       0x4ebb62  ; -> 004EBB62
004EBB5D  comiss   xmm6, xmm5
004EBB60  jbe      0x4ebb67  ; -> 004EBB67
004EBB62  call     0x22cc30  ; -> 0022CC30 fn
004EBB67  call     0x22cc20  ; -> 0022CC20 fn
004EBB6C  movss    xmm1, dword ptr [rip + 0x1b790ac]  ; -> 02064C20
004EBB74  movss    xmm0, dword ptr [rip + 0x1b790a8]  ; -> 02064C24
004EBB7C  subss    xmm1, dword ptr [rip + 0x1b790ac]  ; -> 02064C30
004EBB84  subss    xmm0, dword ptr [rip + 0x1b790a8]  ; -> 02064C34
004EBB8C  ucomiss  xmm1, xmm6
004EBB8F  movss    dword ptr [rip + 0x1b79089], xmm1  ; -> 02064C20
004EBB97  movss    dword ptr [rip + 0x1b79085], xmm0  ; -> 02064C24
004EBB9F  jp       0x4ebba3  ; -> 004EBBA3
004EBBA1  je       0x4ebbaa  ; -> 004EBBAA
004EBBA3  ucomiss  xmm0, xmm6
004EBBA6  jp       0x4ebbbf  ; -> 004EBBBF
004EBBA8  jne      0x4ebbbf  ; -> 004EBBBF
004EBBAA  call     0x22cc40  ; -> 0022CC40 fn
004EBBAF  movss    xmm0, dword ptr [rip + 0x1b7906d]  ; -> 02064C24
004EBBB7  movss    xmm1, dword ptr [rip + 0x1b79061]  ; -> 02064C20
004EBBBF  comiss   xmm6, xmm1
004EBBC2  ja       0x4ebbc9  ; -> 004EBBC9
004EBBC4  comiss   xmm6, xmm0
004EBBC7  jbe      0x4ebbce  ; -> 004EBBCE
004EBBC9  call     0x22cc30  ; -> 0022CC30 fn
004EBBCE  call     0x22cc20  ; -> 0022CC20 fn
004EBBD3  movss    xmm5, dword ptr [rip + 0x1b79039]  ; -> 02064C14
004EBBDB  movss    xmm8, dword ptr [rip + 0x1b7902c]  ; -> 02064C10
004EBBE4  movss    xmm7, dword ptr [rip + 0x1b79038]  ; -> 02064C24
004EBBEC  movss    xmm9, dword ptr [rip + 0x1b7902b]  ; -> 02064C20
004EBBF5  movss    xmm4, dword ptr [rip + 0x1b790f3]  ; -> 02064CF0
004EBBFD  movss    xmm2, dword ptr [rip + 0x1b790ef]  ; -> 02064CF4
004EBC05  movaps   xmm3, xmm4
004EBC08  mulss    xmm3, dword ptr [rip + 0x1b78f50]  ; -> 02064B60
004EBC10  movaps   xmm1, xmm2
004EBC13  mulss    xmm1, dword ptr [rip + 0x1b78f45]  ; -> 02064B60
004EBC1B  mulss    xmm2, dword ptr [rip + 0x1b78f41]  ; -> 02064B64
004EBC23  addss    xmm8, xmm3
004EBC28  mulss    xmm4, dword ptr [rip + 0x1b78f34]  ; -> 02064B64
004EBC30  addss    xmm5, xmm1
004EBC34  addss    xmm7, xmm2
004EBC38  movss    dword ptr [rip + 0x1b78ff0], xmm3  ; -> 02064C30
004EBC40  subss    xmm8, dword ptr [rip + 0x1b78ee7]  ; -> 02064B30
004EBC49  addss    xmm9, xmm4
004EBC4E  movss    dword ptr [rip + 0x1b78fde], xmm1  ; -> 02064C34
004EBC56  subss    xmm5, dword ptr [rip + 0x1b78ed6]  ; -> 02064B34
004EBC5E  movss    dword ptr [rip + 0x1b78fde], xmm2  ; -> 02064C44
004EBC66  movss    dword ptr [rip + 0x1b78fd2], xmm4  ; -> 02064C40
004EBC6E  ucomiss  xmm8, xmm6
004EBC72  movss    dword ptr [rip + 0x1b78fa5], xmm9  ; -> 02064C20
004EBC7B  movss    dword ptr [rip + 0x1b78fa1], xmm7  ; -> 02064C24
004EBC83  movss    dword ptr [rip + 0x1b78f84], xmm8  ; -> 02064C10
004EBC8C  movss    dword ptr [rip + 0x1b78f80], xmm5  ; -> 02064C14
004EBC94  jp       0x4ebc98  ; -> 004EBC98
004EBC96  je       0x4ebc9f  ; -> 004EBC9F
004EBC98  ucomiss  xmm5, xmm6
004EBC9B  jp       0x4ebcb5  ; -> 004EBCB5
004EBC9D  jne      0x4ebcb5  ; -> 004EBCB5
004EBC9F  call     0x22cc40  ; -> 0022CC40 fn
004EBCA4  movss    xmm5, dword ptr [rip + 0x1b78f68]  ; -> 02064C14
004EBCAC  movss    xmm8, dword ptr [rip + 0x1b78f5b]  ; -> 02064C10
004EBCB5  comiss   xmm6, xmm8
004EBCB9  ja       0x4ebcc0  ; -> 004EBCC0
004EBCBB  comiss   xmm6, xmm5
004EBCBE  jbe      0x4ebcc5  ; -> 004EBCC5
004EBCC0  call     0x22cc30  ; -> 0022CC30 fn
004EBCC5  call     0x22cc20  ; -> 0022CC20 fn
004EBCCA  movss    xmm1, dword ptr [rip + 0x1b78f4e]  ; -> 02064C20
004EBCD2  movss    xmm0, dword ptr [rip + 0x1b78f4a]  ; -> 02064C24
004EBCDA  subss    xmm1, dword ptr [rip + 0x1b78e4e]  ; -> 02064B30
004EBCE2  subss    xmm0, dword ptr [rip + 0x1b78e4a]  ; -> 02064B34
004EBCEA  ucomiss  xmm1, xmm6
004EBCED  movss    dword ptr [rip + 0x1b78f2b], xmm1  ; -> 02064C20
004EBCF5  movss    dword ptr [rip + 0x1b78f27], xmm0  ; -> 02064C24
004EBCFD  jp       0x4ebd01  ; -> 004EBD01
004EBCFF  je       0x4ebd08  ; -> 004EBD08
004EBD01  ucomiss  xmm0, xmm6
004EBD04  jp       0x4ebd1d  ; -> 004EBD1D
004EBD06  jne      0x4ebd1d  ; -> 004EBD1D
004EBD08  call     0x22cc40  ; -> 0022CC40 fn
004EBD0D  movss    xmm0, dword ptr [rip + 0x1b78f0f]  ; -> 02064C24
004EBD15  movss    xmm1, dword ptr [rip + 0x1b78f03]  ; -> 02064C20
004EBD1D  comiss   xmm6, xmm1
004EBD20  ja       0x4ebd27  ; -> 004EBD27
004EBD22  comiss   xmm6, xmm0
004EBD25  jbe      0x4ebd2c  ; -> 004EBD2C
004EBD27  call     0x22cc30  ; -> 0022CC30 fn
004EBD2C  call     0x22cc20  ; -> 0022CC20 fn
004EBD31  movsx    r9d, word ptr [rip + 0x1b7907b]  ; -> 02064DB4
004EBD39  movss    xmm0, dword ptr [rip + 0x1916af7]  ; -> 01E02838 [u32 0x00000000]
004EBD41  mov      edx, r9d
004EBD44  addss    xmm0, dword ptr [rip + 0x1916af0]  ; -> 01E0283C [f32 1]
004EBD4C  movss    xmm4, dword ptr [rip + 0x1b78ebc]  ; -> 02064C10
004EBD54  movss    xmm5, dword ptr [rip + 0x1b78eb8]  ; -> 02064C14
004EBD5C  lea      eax, [r9 + 2]
004EBD60  movss    xmm2, dword ptr [rip + 0x1b78eb8]  ; -> 02064C20
004EBD68  movss    xmm3, dword ptr [rip + 0x1b78eb4]  ; -> 02064C24
004EBD70  mulss    xmm4, dword ptr [rip + 0x1b78e28]  ; -> 02064BA0
004EBD78  shl      eax, 4
004EBD7B  mulss    xmm5, dword ptr [rip + 0x1b78e21]  ; -> 02064BA4
004EBD83  movsxd   rcx, eax
004EBD86  lea      eax, [r9 + 5]
004EBD8A  addss    xmm4, dword ptr [rip + 0x1b78dfe]  ; -> 02064B90
004EBD92  mulss    xmm2, dword ptr [rip + 0x1b78e06]  ; -> 02064BA0
004EBD9A  shl      eax, 4
004EBD9D  addss    xmm5, dword ptr [rip + 0x1b78def]  ; -> 02064B94
004EBDA5  mulss    xmm3, dword ptr [rip + 0x1b78df7]  ; -> 02064BA4
004EBDAD  shl      edx, 4
004EBDB0  addss    xmm2, dword ptr [rip + 0x1b78dd8]  ; -> 02064B90
004EBDB8  movaps   xmm6, xmmword ptr [rsp + 0x50]
004EBDBD  addss    xmm3, dword ptr [rip + 0x1b78dcf]  ; -> 02064B94
004EBDC5  movaps   xmm7, xmmword ptr [rsp + 0x40]
004EBDCA  movaps   xmm8, xmmword ptr [rsp + 0x30]
004EBDD0  movaps   xmm9, xmmword ptr [rsp + 0x20]
004EBDD6  movss    dword ptr [rip + 0x1b78e3a], xmm0  ; -> 02064C18
004EBDDE  movss    dword ptr [rip + 0x1b78e42], xmm0  ; -> 02064C28
004EBDE6  movups   xmm0, xmmword ptr [rip + 0x1b78e73]  ; -> 02064C60
004EBDED  movss    dword ptr [rip + 0x1b78e1b], xmm4  ; -> 02064C10
004EBDF5  movups   xmmword ptr [rcx + rbx], xmm0
004EBDF9  movsxd   rcx, eax
004EBDFC  lea      eax, [rdx + 0x10]
004EBDFF  movups   xmm0, xmmword ptr [rip + 0x1b78e6a]  ; -> 02064C70
004EBE06  movss    dword ptr [rip + 0x1b78e06], xmm5  ; -> 02064C14
004EBE0E  movups   xmmword ptr [rcx + rbx], xmm0
004EBE12  movsxd   rcx, eax
004EBE15  lea      eax, [r9 + 4]
004EBE19  movups   xmm0, xmmword ptr [rip + 0x1b78d50]  ; -> 02064B70
004EBE20  shl      eax, 4
004EBE23  movss    dword ptr [rip + 0x1b78df5], xmm2  ; -> 02064C20
004EBE2B  movups   xmmword ptr [rcx + rbx], xmm0
004EBE2F  movsxd   rcx, eax
004EBE32  movups   xmm0, xmmword ptr [rip + 0x1b78d47]  ; -> 02064B80
004EBE39  movsxd   rax, edx
004EBE3C  movss    dword ptr [rip + 0x1b78de0], xmm3  ; -> 02064C24
004EBE44  movups   xmmword ptr [rcx + rbx], xmm0
004EBE48  movups   xmm0, xmmword ptr [rip + 0x1b78dc1]  ; -> 02064C10
004EBE4F  movups   xmmword ptr [rax + rbx], xmm0
004EBE53  lea      eax, [r9 + 3]
004EBE57  movups   xmm0, xmmword ptr [rip + 0x1b78dc2]  ; -> 02064C20
004EBE5E  shl      eax, 4
004EBE61  movsxd   rcx, eax
004EBE64  add      r9w, 6
004EBE69  mov      word ptr [rip + 0x1b78f43], r9w  ; -> 02064DB4
004EBE71  movups   xmmword ptr [rcx + rbx], xmm0
004EBE75  add      rsp, 0x60
004EBE79  pop      rbx
004EBE7A  ret      
```
