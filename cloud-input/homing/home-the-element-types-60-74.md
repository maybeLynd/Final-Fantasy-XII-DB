# Homing pack: `17-Presentation-Rendering/Effect-File-Formats/the-element-types-60-74.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-element-types-60-74.json`.

Bodies: 23. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 004B0F60 (553 B, extent 004B0F60-004B1189)

Entered from (direct sites whose caller this page cites): `004B1190` + 0x5057 (call; `004B1190` is cited on this page)
Other direct sites: none

Host context: "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320"

```
004B0F60  sub      rsp, 0x48
004B0F64  movzx    ecx, word ptr [rip + 0x1bb3ba1]  ; -> 02064B0C
004B0F6B  mov      edx, 0xe0
004B0F70  movss    xmm2, dword ptr [rip + 0x1bb3d38]  ; -> 02064CB0
004B0F78  movss    xmm3, dword ptr [rip + 0x1bb3d34]  ; -> 02064CB4
004B0F80  movaps   xmm0, xmm2
004B0F83  subss    xmm0, xmm3
004B0F87  mov      dword ptr [rip + 0x1bb3b73], 0x3f000000  ; -> 02064B04
004B0F91  lea      eax, [rcx + 1]
004B0F94  cmp      word ptr [rip + 0x1bb3e35], ax  ; -> 02064DD0
004B0F9B  lea      r8d, [rdx + rcx]
004B0F9F  mov      word ptr [rip + 0x1bb3e22], ax  ; -> 02064DC8
004B0FA6  mov      word ptr [rip + 0x1bb3e2a], r8w  ; -> 02064DD8
004B0FAE  movss    dword ptr [rip + 0x1bb3b5a], xmm0  ; -> 02064B10
004B0FB6  je       0x4b1184  ; -> 004B1184
004B0FBC  movaps   xmmword ptr [rsp + 0x30], xmm6
004B0FC1  movaps   xmmword ptr [rsp + 0x20], xmm7
004B0FC6  and      r8w, word ptr [rip + 0x1bb3b42]  ; -> 02064B10
004B0FCE  mov      eax, 0x118
004B0FD3  movss    xmm6, dword ptr [rip + 0x44f385]  ; -> 00900360 [u32 0x7F7FFFFF]
004B0FDB  xorps    xmm7, xmm7
004B0FDE  mov      word ptr [rip + 0x1bb3df2], r8w  ; -> 02064DD8
004B0FE6  lea      edx, [rax + rcx]
004B0FE9  mov      word ptr [rip + 0x1bb3dd8], dx  ; -> 02064DC8
004B0FF0  cmp      r8w, cx
004B0FF4  jne      0x4b107e  ; -> 004B107E
004B0FFA  cmp      word ptr [rip + 0x1bb3dd3], cx  ; -> 02064DD4
004B1001  mov      dword ptr [rip + 0x1bb3af9], 0x3f000000  ; -> 02064B04
004B100B  jne      0x4b10ef  ; -> 004B10EF
004B1011  ucomiss  xmm3, xmm7
004B1014  jp       0x4b1025  ; -> 004B1025
004B1016  jne      0x4b1025  ; -> 004B1025
004B1018  movss    dword ptr [rip + 0x1bb3ae0], xmm6  ; -> 02064B00
004B1020  movaps   xmm1, xmm6
004B1023  jmp      0x4b1034  ; -> 004B1034
004B1025  movaps   xmm1, xmm2
004B1028  divss    xmm1, xmm3
004B102C  movss    dword ptr [rip + 0x1bb3acc], xmm1  ; -> 02064B00
004B1034  movss    xmm0, dword ptr [rip + 0x19517f4]  ; -> 01E02830 [u32 0x00000000]
004B103C  addss    xmm0, xmm1
004B1040  cvttss2si eax, xmm0
004B1044  movd     xmm1, eax
004B1048  cvtdq2ps xmm1, xmm1
004B104B  mulss    xmm1, xmm3
004B104F  subss    xmm2, xmm1
004B1053  movss    dword ptr [rip + 0x1bb3c65], xmm1  ; -> 02064CC0
004B105B  movss    dword ptr [rip + 0x1bb3c4d], xmm2  ; -> 02064CB0
004B1063  call     0x22cc20  ; -> 0022CC20 fn
004B1068  movss    xmm2, dword ptr [rip + 0x1bb3c40]  ; -> 02064CB0
004B1070  movzx    ecx, word ptr [rip + 0x1bb3a95]  ; -> 02064B0C
004B1077  movzx    edx, word ptr [rip + 0x1bb3d4a]  ; -> 02064DC8
004B107E  cmp      word ptr [rip + 0x1bb3d47], cx  ; -> 02064DCC
004B1085  je       0x4b1118  ; -> 004B1118
004B108B  cvttss2si eax, xmm2
004B108F  lea      r9, [rip + 0x1bb3d9e]  ; -> 02064E34
004B1096  mov      dword ptr [rip + 0x1bb3c14], eax  ; -> 02064CB0
004B109C  movss    xmm0, dword ptr [rip + 0x1bb3c0c]  ; -> 02064CB0
004B10A4  movss    dword ptr [rsp + 0x50], xmm0
004B10AA  movzx    r8d, word ptr [rsp + 0x50]
004B10B0  movsx    eax, dx
004B10B3  inc      dx
004B10B6  shl      eax, 4
004B10B9  movsxd   rcx, eax
004B10BC  movzx    eax, word ptr [rcx + r9]
004B10C1  sub      r8w, ax
004B10C5  mov      word ptr [rip + 0x1bb3d04], ax  ; -> 02064DD0
004B10CC  jns      0x4b10b0  ; -> 004B10B0
004B10CE  movaps   xmm6, xmmword ptr [rsp + 0x30]
004B10D3  dec      dx
004B10D6  movaps   xmm7, xmmword ptr [rsp + 0x20]
004B10DB  mov      word ptr [rip + 0x1bb3ce6], dx  ; -> 02064DC8
004B10E2  mov      word ptr [rip + 0x1bb3cea], r8w  ; -> 02064DD4
004B10EA  add      rsp, 0x48
004B10EE  ret      
004B10EF  movzx    eax, word ptr [rip + 0x1bb3cd6]  ; -> 02064DCC
004B10F6  cmp      ax, cx
004B10F9  je       0x4b117a  ; -> 004B117A
004B10FB  movaps   xmm6, xmmword ptr [rsp + 0x30]
004B1100  movaps   xmm7, xmmword ptr [rsp + 0x20]
004B1105  cwde     
004B1106  dec      ax
004B1109  add      dx, ax
004B110C  mov      word ptr [rip + 0x1bb3cb5], dx  ; -> 02064DC8
004B1113  add      rsp, 0x48
004B1117  ret      
004B1118  movss    xmm0, dword ptr [rip + 0x1bb3b98]  ; -> 02064CB8
004B1120  ucomiss  xmm0, xmm7
004B1123  jp       0x4b1127  ; -> 004B1127
004B1125  je       0x4b112e  ; -> 004B112E
004B1127  movaps   xmm6, xmm2
004B112A  divss    xmm6, xmm0
004B112E  movss    xmm0, dword ptr [rip + 0x19516fe]  ; -> 01E02834 [u32 0x00000000]
004B1136  addss    xmm0, xmm6
004B113A  movss    dword ptr [rip + 0x1bb39be], xmm6  ; -> 02064B00
004B1142  ucomiss  xmm0, xmm7
004B1145  movss    dword ptr [rip + 0x1bb3b67], xmm0  ; -> 02064CB4
004B114D  jp       0x4b115e  ; -> 004B115E
004B114F  jne      0x4b115e  ; -> 004B115E
004B1151  call     0x22cc40  ; -> 0022CC40 fn
004B1156  movss    xmm0, dword ptr [rip + 0x1bb3b56]  ; -> 02064CB4
004B115E  comiss   xmm7, xmm0
004B1161  jbe      0x4b1170  ; -> 004B1170
004B1163  call     0x22cc30  ; -> 0022CC30 fn
004B1168  movss    xmm0, dword ptr [rip + 0x1bb3b44]  ; -> 02064CB4
004B1170  cvttss2si eax, xmm0
004B1174  mov      dword ptr [rip + 0x1bb3b3a], eax  ; -> 02064CB4
004B117A  movaps   xmm6, xmmword ptr [rsp + 0x30]
004B117F  movaps   xmm7, xmmword ptr [rsp + 0x20]
004B1184  add      rsp, 0x48
004B1188  ret      
```

## 004B97F0 (66 B, extent 004B97F0-004B9832)

Entered from (direct sites whose caller this page cites): `004B1190` + 0x566F (call; `004B1190` is cited on this page); `004B1190` + 0x5674 (call; `004B1190` is cited on this page); `004B1190` + 0x5679 (call; `004B1190` is cited on this page); `004B1190` + 0x567E (call; `004B1190` is cited on this page); `004B1190` + 0x5683 (call; `004B1190` is cited on this page); `004B1190` + 0x6189 (call; `004B1190` is cited on this page)
Other direct sites: none

Host context: "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320" / "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320"

```
004B97F0  cmp      dword ptr [rip + 0x1bab305], 0  ; -> 02064AFC
004B97F7  jne      0x4b9802  ; -> 004B9802
004B97F9  movss    xmm0, dword ptr [rip + 0x18323a7]  ; -> 01CEBBA8 [f32 1]
004B9801  ret      
004B9802  mov      eax, dword ptr [rip + 0x1949020]  ; -> 01E02828 [f32 1]
004B9808  mov      ecx, eax
004B980A  shr      ecx, 0x12
004B980D  xor      ecx, eax
004B980F  and      eax, 0x3fffff
004B9814  shr      ecx, 4
004B9817  or       eax, 0x1fc00000
004B981C  add      eax, eax
004B981E  and      ecx, 1
004B9821  or       ecx, eax
004B9823  mov      dword ptr [rip + 0x1948fff], ecx  ; -> 01E02828 [f32 1]
004B9829  movss    xmm0, dword ptr [rip + 0x1948ff7]  ; -> 01E02828 [f32 1]
004B9831  ret      
```

## 004B9840 (46 B, extent 004B9840-004B986E)

Entered from (direct sites whose caller this page cites): `004B1190` + 0x67D1 (call; `004B1190` is cited on this page); `004B1190` + 0x6918 (call; `004B1190` is cited on this page); `004B1190` + 0x694D (call; `004B1190` is cited on this page); `004B1190` + 0x696B (call; `004B1190` is cited on this page); `004B1190` + 0x74FF (call; `004B1190` is cited on this page); `004B1190` + 0x7646 (call; `004B1190` is cited on this page); `004B1190` + 0x767B (call; `004B1190` is cited on this page); `004B1190` + 0x7699 (call; `004B1190` is cited on this page)
Other direct sites: none

Host context: "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320" / "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320"

```
004B9840  movss    xmm0, dword ptr [rdx]
004B9844  addss    xmm0, dword ptr [r8]
004B9849  movss    dword ptr [rcx], xmm0
004B984D  movss    xmm1, dword ptr [rdx + 4]
004B9852  addss    xmm1, dword ptr [r8 + 4]
004B9858  movss    dword ptr [rcx + 4], xmm1
004B985D  movss    xmm0, dword ptr [rdx + 8]
004B9862  addss    xmm0, dword ptr [r8 + 8]
004B9868  movss    dword ptr [rcx + 8], xmm0
004B986D  ret      
```

## 004B9870 (32 B, extent 004B9870-004B9890)

Entered from (direct sites whose caller this page cites): `004B1190` + 0x6AA1 (call; `004B1190` is cited on this page); `004B1190` + 0x6B54 (call; `004B1190` is cited on this page); `004B1190` + 0x77CF (call; `004B1190` is cited on this page); `004B1190` + 0x7882 (call; `004B1190` is cited on this page)
Other direct sites: none

Host context: "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320" / "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320"

```
004B9870  xorps    xmm0, xmm0
004B9873  ucomiss  xmm2, xmm0
004B9876  jp       0x4b9887  ; -> 004B9887
004B9878  jne      0x4b9887  ; -> 004B9887
004B987A  movss    xmm0, dword ptr [rip + 0x446ade]  ; -> 00900360 [u32 0x7F7FFFFF]
004B9882  movss    dword ptr [rcx], xmm0
004B9886  ret      
004B9887  divss    xmm1, xmm2
004B988B  movss    dword ptr [rcx], xmm1
004B988F  ret      
```

## 004B9890 (55 B, extent 004B9890-004B98C7)

Entered from (direct sites whose caller this page cites): `004B1190` + 0x6C46 (call; `004B1190` is cited on this page); `004B1190` + 0x6C59 (call; `004B1190` is cited on this page); `004B1190` + 0x7978 (call; `004B1190` is cited on this page); `004B1190` + 0x798B (call; `004B1190` is cited on this page)
Other direct sites: none

Host context: "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320" / "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320"

```
004B9890  movss    xmm0, dword ptr [rdx]
004B9894  movss    xmm2, dword ptr [rip + 0x18323e8]  ; -> 01CEBC84 [f32 16]
004B989C  mulss    xmm0, xmm2
004B98A0  cvttss2si eax, xmm0
004B98A4  mov      dword ptr [rcx], eax
004B98A6  movss    xmm0, dword ptr [rdx + 4]
004B98AB  mulss    xmm0, xmm2
004B98AF  cvttss2si eax, xmm0
004B98B3  mov      dword ptr [rcx + 4], eax
004B98B6  movss    xmm1, dword ptr [rdx + 8]
004B98BB  mulss    xmm1, xmm2
004B98BF  cvttss2si eax, xmm1
004B98C3  mov      dword ptr [rcx + 8], eax
004B98C6  ret      
```

## 004B98F0 (21 B, extent 004B98F0-004B9905)

Entered from (direct sites whose caller this page cites): `004B1190` + 0x6FF8 (call; `004B1190` is cited on this page); `004B1190` + 0x7105 (call; `004B1190` is cited on this page)
Other direct sites: none

Host context: "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320" / "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320"

```
004B98F0  shl      edx, 4
004B98F3  movsxd   rax, edx
004B98F6  lea      rdx, [rip + 0x1bab537]  ; -> 02064E34
004B98FD  movzx    eax, word ptr [rax + rdx]
004B9901  mov      word ptr [rcx], ax
004B9904  ret      
```

## 004B99D0 (20 B, extent 004B99D0-004B99E4)

Entered from (direct sites whose caller this page cites): `004B1190` + 0x6786 (call; `004B1190` is cited on this page); `004B1190` + 0x688A (call; `004B1190` is cited on this page); `004B1190` + 0x68C5 (call; `004B1190` is cited on this page); `004B1190` + 0x697A (call; `004B1190` is cited on this page); `004B1190` + 0x707F (call; `004B1190` is cited on this page); `004B1190` + 0x74B4 (call; `004B1190` is cited on this page); `004B1190` + 0x75B8 (call; `004B1190` is cited on this page); `004B1190` + 0x75F3 (call; `004B1190` is cited on this page); `004B1190` + 0x76A8 (call; `004B1190` is cited on this page)
Other direct sites: none

Host context: "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320" / "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320"

```
004B99D0  shl      edx, 4
004B99D3  movsxd   rax, edx
004B99D6  lea      rdx, [rip + 0x1bab457]  ; -> 02064E34
004B99DD  mov      eax, dword ptr [rax + rdx]
004B99E0  mov      dword ptr [rcx + 4], eax
004B99E3  ret      
```

## 004B99F0 (22 B, extent 004B99F0-004B9A06)

Entered from (direct sites whose caller this page cites): `004B1190` + 0x6600 (call; `004B1190` is cited on this page); `004B1190` + 0x66C3 (call; `004B1190` is cited on this page); `004B1190` + 0x732E (call; `004B1190` is cited on this page); `004B1190` + 0x73F1 (call; `004B1190` is cited on this page)
Other direct sites: none

Host context: "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320" / "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320"

```
004B99F0  shl      edx, 4
004B99F3  movsxd   rax, edx
004B99F6  lea      rdx, [rip + 0x1bab43b]  ; -> 02064E38
004B99FD  mov      rax, qword ptr [rax + rdx]
004B9A01  mov      qword ptr [rcx + 8], rax
004B9A05  ret      
```

## 004B9A10 (22 B, extent 004B9A10-004B9A26)

Entered from (direct sites whose caller this page cites): `004B1190` + 0x659C (call; `004B1190` is cited on this page); `004B1190` + 0x72CA (call; `004B1190` is cited on this page)
Other direct sites: none

Host context: "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320" / "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320"

```
004B9A10  movss    xmm0, dword ptr [rdx + 0xc]
004B9A15  mulss    xmm0, dword ptr [r8 + 4]
004B9A1B  addss    xmm0, dword ptr [rcx + 0xc]
004B9A20  movss    dword ptr [rcx + 0xc], xmm0
004B9A25  ret      
```

## 004B9A30 (82 B, extent 004B9A30-004B9A82)

Entered from (direct sites whose caller this page cites): `004B1190` + 0x6A3D (call; `004B1190` is cited on this page); `004B1190` + 0x6B00 (call; `004B1190` is cited on this page); `004B1190` + 0x776B (call; `004B1190` is cited on this page); `004B1190` + 0x782E (call; `004B1190` is cited on this page)
Other direct sites: none

Host context: "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320" / "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320"

```
004B9A30  movss    xmm0, dword ptr [r8 + 4]
004B9A36  mulss    xmm0, dword ptr [rdx]
004B9A3A  addss    xmm0, dword ptr [rcx]
004B9A3E  movss    dword ptr [rcx], xmm0
004B9A42  movss    xmm1, dword ptr [rdx + 4]
004B9A47  mulss    xmm1, dword ptr [r8 + 4]
004B9A4D  addss    xmm1, dword ptr [rcx + 4]
004B9A52  movss    dword ptr [rcx + 4], xmm1
004B9A57  movss    xmm0, dword ptr [rdx + 8]
004B9A5C  mulss    xmm0, dword ptr [r8 + 4]
004B9A62  addss    xmm0, dword ptr [rcx + 8]
004B9A67  movss    dword ptr [rcx + 8], xmm0
004B9A6C  movss    xmm1, dword ptr [rdx + 0xc]
004B9A71  mulss    xmm1, dword ptr [r8 + 4]
004B9A77  addss    xmm1, dword ptr [rcx + 0xc]
004B9A7C  movss    dword ptr [rcx + 0xc], xmm1
004B9A81  ret      
```

## 004B9A90 (82 B, extent 004B9A90-004B9AE2)

Entered from (direct sites whose caller this page cites): `004B1190` + 0x6A5B (call; `004B1190` is cited on this page); `004B1190` + 0x6B1E (call; `004B1190` is cited on this page); `004B1190` + 0x7789 (call; `004B1190` is cited on this page); `004B1190` + 0x784C (call; `004B1190` is cited on this page)
Other direct sites: none

Host context: "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320" / "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320"

```
004B9A90  movss    xmm0, dword ptr [r8 + 8]
004B9A96  mulss    xmm0, dword ptr [rdx]
004B9A9A  addss    xmm0, dword ptr [rcx]
004B9A9E  movss    dword ptr [rcx], xmm0
004B9AA2  movss    xmm1, dword ptr [rdx + 4]
004B9AA7  mulss    xmm1, dword ptr [r8 + 8]
004B9AAD  addss    xmm1, dword ptr [rcx + 4]
004B9AB2  movss    dword ptr [rcx + 4], xmm1
004B9AB7  movss    xmm0, dword ptr [rdx + 8]
004B9ABC  mulss    xmm0, dword ptr [r8 + 8]
004B9AC2  addss    xmm0, dword ptr [rcx + 8]
004B9AC7  movss    dword ptr [rcx + 8], xmm0
004B9ACC  movss    xmm1, dword ptr [rdx + 0xc]
004B9AD1  mulss    xmm1, dword ptr [r8 + 8]
004B9AD7  addss    xmm1, dword ptr [rcx + 0xc]
004B9ADC  movss    dword ptr [rcx + 0xc], xmm1
004B9AE1  ret      
```

## 004B9AF0 (95 B, extent 004B9AF0-004B9B4F)

Entered from (direct sites whose caller this page cites): `004B1190` + 0x6A80 (call; `004B1190` is cited on this page); `004B1190` + 0x6B3C (call; `004B1190` is cited on this page); `004B1190` + 0x77AE (call; `004B1190` is cited on this page); `004B1190` + 0x786A (call; `004B1190` is cited on this page)
Other direct sites: none

Host context: "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320" / "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320"

```
004B9AF0  movss    xmm0, dword ptr [r8 + 0xc]
004B9AF6  mulss    xmm0, dword ptr [rdx]
004B9AFA  addss    xmm0, dword ptr [rip + 0x1bab01e]  ; -> 02064B20
004B9B02  movss    dword ptr [rcx], xmm0
004B9B06  movss    xmm1, dword ptr [rdx + 4]
004B9B0B  mulss    xmm1, dword ptr [r8 + 0xc]
004B9B11  addss    xmm1, dword ptr [rip + 0x1bab00b]  ; -> 02064B24
004B9B19  movss    dword ptr [rcx + 4], xmm1
004B9B1E  movss    xmm0, dword ptr [rdx + 8]
004B9B23  mulss    xmm0, dword ptr [r8 + 0xc]
004B9B29  addss    xmm0, dword ptr [rip + 0x1baaff7]  ; -> 02064B28
004B9B31  movss    dword ptr [rcx + 8], xmm0
004B9B36  movss    xmm1, dword ptr [rdx + 0xc]
004B9B3B  mulss    xmm1, dword ptr [r8 + 0xc]
004B9B41  addss    xmm1, dword ptr [rip + 0x1baafe3]  ; -> 02064B2C
004B9B49  movss    dword ptr [rcx + 0xc], xmm1
004B9B4E  ret      
```

## 004B9B50 (46 B, extent 004B9B50-004B9B7E)

Entered from (direct sites whose caller this page cites): `004B1190` + 0x655E (call; `004B1190` is cited on this page); `004B1190` + 0x728C (call; `004B1190` is cited on this page)
Other direct sites: none

Host context: "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320" / "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320"

```
004B9B50  movss    xmm0, dword ptr [rdx]
004B9B54  mulss    xmm0, dword ptr [r8]
004B9B59  movss    dword ptr [rcx], xmm0
004B9B5D  movss    xmm1, dword ptr [rdx + 4]
004B9B62  mulss    xmm1, dword ptr [r8 + 4]
004B9B68  movss    dword ptr [rcx + 4], xmm1
004B9B6D  movss    xmm0, dword ptr [rdx + 8]
004B9B72  mulss    xmm0, dword ptr [r8 + 8]
004B9B78  movss    dword ptr [rcx + 8], xmm0
004B9B7D  ret      
```

## 004B9B80 (59 B, extent 004B9B80-004B9BBB)

Entered from (direct sites whose caller this page cites): `004B1190` + 0x6A1F (call; `004B1190` is cited on this page); `004B1190` + 0x6AE2 (call; `004B1190` is cited on this page); `004B1190` + 0x774D (call; `004B1190` is cited on this page); `004B1190` + 0x7810 (call; `004B1190` is cited on this page)
Other direct sites: none

Host context: "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320" / "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320"

```
004B9B80  movss    xmm0, dword ptr [rdx]
004B9B84  mulss    xmm0, dword ptr [r8]
004B9B89  movss    dword ptr [rcx], xmm0
004B9B8D  movss    xmm1, dword ptr [rdx + 4]
004B9B92  mulss    xmm1, dword ptr [r8]
004B9B97  movss    dword ptr [rcx + 4], xmm1
004B9B9C  movss    xmm0, dword ptr [rdx + 8]
004B9BA1  mulss    xmm0, dword ptr [r8]
004B9BA6  movss    dword ptr [rcx + 8], xmm0
004B9BAB  movss    xmm1, dword ptr [rdx + 0xc]
004B9BB0  mulss    xmm1, dword ptr [r8]
004B9BB5  movss    dword ptr [rcx + 0xc], xmm1
004B9BBA  ret      
```

## 004B9BC0 (35 B, extent 004B9BC0-004B9BE3)

Entered from (direct sites whose caller this page cites): `004B1190` + 0x65F1 (call; `004B1190` is cited on this page); `004B1190` + 0x6ABC (call; `004B1190` is cited on this page); `004B1190` + 0x6B6F (call; `004B1190` is cited on this page); `004B1190` + 0x731F (call; `004B1190` is cited on this page); `004B1190` + 0x77EA (call; `004B1190` is cited on this page); `004B1190` + 0x789D (call; `004B1190` is cited on this page)
Other direct sites: none

Host context: "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320" / "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320"

```
004B9BC0  movaps   xmm0, xmm2
004B9BC3  movaps   xmm1, xmm2
004B9BC6  mulss    xmm0, dword ptr [rdx]
004B9BCA  movss    dword ptr [rcx], xmm0
004B9BCE  mulss    xmm1, dword ptr [rdx + 4]
004B9BD3  movss    dword ptr [rcx + 4], xmm1
004B9BD8  mulss    xmm2, dword ptr [rdx + 8]
004B9BDD  movss    dword ptr [rcx + 8], xmm2
004B9BE2  ret      
```

## 004B9BF0 (47 B, extent 004B9BF0-004B9C1F)

Entered from (direct sites whose caller this page cites): `004B1190` + 0x66B4 (call; `004B1190` is cited on this page); `004B1190` + 0x6777 (call; `004B1190` is cited on this page); `004B1190` + 0x73E2 (call; `004B1190` is cited on this page); `004B1190` + 0x74A5 (call; `004B1190` is cited on this page)
Other direct sites: none

Host context: "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320" / "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320"

```
004B9BF0  movss    xmm0, dword ptr [rdx]
004B9BF4  mulss    xmm0, dword ptr [r8 + 0xc]
004B9BFA  movss    dword ptr [rcx], xmm0
004B9BFE  movss    xmm1, dword ptr [rdx + 4]
004B9C03  mulss    xmm1, dword ptr [r8 + 0xc]
004B9C09  movss    dword ptr [rcx + 4], xmm1
004B9C0E  movss    xmm0, dword ptr [rdx + 8]
004B9C13  mulss    xmm0, dword ptr [r8 + 0xc]
004B9C19  movss    dword ptr [rcx + 8], xmm0
004B9C1E  ret      
```

## 004B9C20 (47 B, extent 004B9C20-004B9C4F)

Entered from (direct sites whose caller this page cites): `004B1190` + 0x67AB (call; `004B1190` is cited on this page); `004B1190` + 0x68FA (call; `004B1190` is cited on this page); `004B1190` + 0x74D9 (call; `004B1190` is cited on this page); `004B1190` + 0x7628 (call; `004B1190` is cited on this page)
Other direct sites: none

Host context: "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320" / "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320"

```
004B9C20  movss    xmm0, dword ptr [rdx]
004B9C24  mulss    xmm0, dword ptr [r8 + 4]
004B9C2A  movss    dword ptr [rcx], xmm0
004B9C2E  movss    xmm1, dword ptr [rdx + 4]
004B9C33  mulss    xmm1, dword ptr [r8 + 4]
004B9C39  movss    dword ptr [rcx + 4], xmm1
004B9C3E  movss    xmm0, dword ptr [rdx + 8]
004B9C43  mulss    xmm0, dword ptr [r8 + 4]
004B9C49  movss    dword ptr [rcx + 8], xmm0
004B9C4E  ret      
```

## 004B9C50 (77 B, extent 004B9C50-004B9C9D)

Entered from (direct sites whose caller this page cites): `004B1190` + 0x6613 (call; `004B1190` is cited on this page); `004B1190` + 0x6626 (call; `004B1190` is cited on this page); `004B1190` + 0x6639 (call; `004B1190` is cited on this page); `004B1190` + 0x664C (call; `004B1190` is cited on this page); `004B1190` + 0x665F (call; `004B1190` is cited on this page); `004B1190` + 0x66D6 (call; `004B1190` is cited on this page); `004B1190` + 0x66E9 (call; `004B1190` is cited on this page); `004B1190` + 0x66FC (call; `004B1190` is cited on this page); `004B1190` + 0x670F (call; `004B1190` is cited on this page); `004B1190` + 0x6722 (call; `004B1190` is cited on this page); `004B1190` + 0x6FD5 (call; `004B1190` is cited on this page); `004B1190` + 0x7138 (call; `004B1190` is cited on this page); `004B1190` + 0x714B (call; `004B1190` is cited on this page); `004B1190` + 0x715E (call; `004B1190` is cited on this page); `004B1190` + 0x7171 (call; `004B1190` is cited on this page); `004B1190` + 0x7184 (call; `004B1190` is cited on this page); `004B1190` + 0x7341 (call; `004B1190` is cited on this page); `004B1190` + 0x7354 (call; `004B1190` is cited on this page); `004B1190` + 0x7367 (call; `004B1190` is cited on this page); `004B1190` + 0x737A (call; `004B1190` is cited on this page); `004B1190` + 0x738D (call; `004B1190` is cited on this page); `004B1190` + 0x7404 (call; `004B1190` is cited on this page); `004B1190` + 0x7417 (call; `004B1190` is cited on this page); `004B1190` + 0x742A (call; `004B1190` is cited on this page); `004B1190` + 0x743D (call; `004B1190` is cited on this page); `004B1190` + 0x7450 (call; `004B1190` is cited on this page); `004B1190` + 0x7CFE (call; `004B1190` is cited on this page)
Other direct sites: none

Host context: "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320" / "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320"

```
004B9C50  cmp      dword ptr [rip + 0x1baaea5], 0  ; -> 02064AFC
004B9C57  mov      rdx, rcx
004B9C5A  jne      0x4b9c69  ; -> 004B9C69
004B9C5C  movss    xmm0, dword ptr [rip + 0x1831f44]  ; -> 01CEBBA8 [f32 1]
004B9C64  movss    dword ptr [rcx], xmm0
004B9C68  ret      
004B9C69  mov      eax, dword ptr [rip + 0x1948bb9]  ; -> 01E02828 [f32 1]
004B9C6F  mov      ecx, eax
004B9C71  shr      ecx, 0x12
004B9C74  xor      ecx, eax
004B9C76  and      eax, 0x3fffff
004B9C7B  shr      ecx, 4
004B9C7E  or       eax, 0x1fc00000
004B9C83  add      eax, eax
004B9C85  and      ecx, 1
004B9C88  or       ecx, eax
004B9C8A  mov      dword ptr [rip + 0x1948b98], ecx  ; -> 01E02828 [f32 1]
004B9C90  movss    xmm0, dword ptr [rip + 0x1948b90]  ; -> 01E02828 [f32 1]
004B9C98  movss    dword ptr [rdx], xmm0
004B9C9C  ret      
```

## 004B9CA0 (79 B, extent 004B9CA0-004B9CEF)

Entered from (direct sites whose caller this page cites): `004B1190` + 0x7197 (call; `004B1190` is cited on this page); `004B1190` + 0x71AA (call; `004B1190` is cited on this page); `004B1190` + 0x71BD (call; `004B1190` is cited on this page); `004B1190` + 0x71D0 (call; `004B1190` is cited on this page); `004B1190` + 0x71E3 (call; `004B1190` is cited on this page)
Other direct sites: none

Host context: "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320" / "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320"

```
004B9CA0  cmp      dword ptr [rip + 0x1baae55], 0  ; -> 02064AFC
004B9CA7  mov      rdx, rcx
004B9CAA  jne      0x4b9cba  ; -> 004B9CBA
004B9CAC  movss    xmm0, dword ptr [rip + 0x1831ef4]  ; -> 01CEBBA8 [f32 1]
004B9CB4  movss    dword ptr [rcx + 4], xmm0
004B9CB9  ret      
004B9CBA  mov      eax, dword ptr [rip + 0x1948b68]  ; -> 01E02828 [f32 1]
004B9CC0  mov      ecx, eax
004B9CC2  shr      ecx, 0x12
004B9CC5  xor      ecx, eax
004B9CC7  and      eax, 0x3fffff
004B9CCC  shr      ecx, 4
004B9CCF  or       eax, 0x1fc00000
004B9CD4  add      eax, eax
004B9CD6  and      ecx, 1
004B9CD9  or       ecx, eax
004B9CDB  mov      dword ptr [rip + 0x1948b47], ecx  ; -> 01E02828 [f32 1]
004B9CE1  movss    xmm0, dword ptr [rip + 0x1948b3f]  ; -> 01E02828 [f32 1]
004B9CE9  movss    dword ptr [rdx + 4], xmm0
004B9CEE  ret      
```

## 004B9CF0 (79 B, extent 004B9CF0-004B9D3F)

Entered from (direct sites whose caller this page cites): `004B1190` + 0x67F3 (call; `004B1190` is cited on this page); `004B1190` + 0x6806 (call; `004B1190` is cited on this page); `004B1190` + 0x6819 (call; `004B1190` is cited on this page); `004B1190` + 0x682C (call; `004B1190` is cited on this page); `004B1190` + 0x683F (call; `004B1190` is cited on this page); `004B1190` + 0x71F6 (call; `004B1190` is cited on this page); `004B1190` + 0x7209 (call; `004B1190` is cited on this page); `004B1190` + 0x721C (call; `004B1190` is cited on this page); `004B1190` + 0x722F (call; `004B1190` is cited on this page); `004B1190` + 0x7242 (call; `004B1190` is cited on this page); `004B1190` + 0x7521 (call; `004B1190` is cited on this page); `004B1190` + 0x7534 (call; `004B1190` is cited on this page); `004B1190` + 0x7547 (call; `004B1190` is cited on this page); `004B1190` + 0x755A (call; `004B1190` is cited on this page); `004B1190` + 0x756D (call; `004B1190` is cited on this page)
Other direct sites: none

Host context: "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320" / "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320"

```
004B9CF0  cmp      dword ptr [rip + 0x1baae05], 0  ; -> 02064AFC
004B9CF7  mov      rdx, rcx
004B9CFA  jne      0x4b9d0a  ; -> 004B9D0A
004B9CFC  movss    xmm0, dword ptr [rip + 0x1831ea4]  ; -> 01CEBBA8 [f32 1]
004B9D04  movss    dword ptr [rcx + 8], xmm0
004B9D09  ret      
004B9D0A  mov      eax, dword ptr [rip + 0x1948b18]  ; -> 01E02828 [f32 1]
004B9D10  mov      ecx, eax
004B9D12  shr      ecx, 0x12
004B9D15  xor      ecx, eax
004B9D17  and      eax, 0x3fffff
004B9D1C  shr      ecx, 4
004B9D1F  or       eax, 0x1fc00000
004B9D24  add      eax, eax
004B9D26  and      ecx, 1
004B9D29  or       ecx, eax
004B9D2B  mov      dword ptr [rip + 0x1948af7], ecx  ; -> 01E02828 [f32 1]
004B9D31  movss    xmm0, dword ptr [rip + 0x1948aef]  ; -> 01E02828 [f32 1]
004B9D39  movss    dword ptr [rdx + 8], xmm0
004B9D3E  ret      
```

## 004B9D80 (171 B, extent 004B9D80-004B9E2B)

Entered from (direct sites whose caller this page cites): `004B1190` + 0x2D29 (call; `004B1190` is cited on this page); `004B1190` + 0x2D4E (call; `004B1190` is cited on this page); `004B1190` + 0x3379 (call; `004B1190` is cited on this page); `004B1190` + 0x339E (call; `004B1190` is cited on this page); `004B1190` + 0x4783 (call; `004B1190` is cited on this page); `004B1190` + 0x47A9 (call; `004B1190` is cited on this page); `004B1190` + 0x47C7 (call; `004B1190` is cited on this page); `004B1190` + 0x47EF (call; `004B1190` is cited on this page); `004B1190` + 0x480D (call; `004B1190` is cited on this page); `004B1190` + 0x483C (call; `004B1190` is cited on this page); `004B1190` + 0x486F (call; `004B1190` is cited on this page); `004B1190` + 0x489C (call; `004B1190` is cited on this page); `004B1190` + 0x5D43 (call; `004B1190` is cited on this page); `004B1190` + 0x5D69 (call; `004B1190` is cited on this page); `004B1190` + 0x5D87 (call; `004B1190` is cited on this page); `004B1190` + 0x5DAF (call; `004B1190` is cited on this page); `004B1190` + 0x5DCD (call; `004B1190` is cited on this page); `004B1190` + 0x5DFC (call; `004B1190` is cited on this page); `004B1190` + 0x5E2C (call; `004B1190` is cited on this page); `004B1190` + 0x5E59 (call; `004B1190` is cited on this page); `004B1190` + 0x6BBC (call; `004B1190` is cited on this page); `004B1190` + 0x6BF0 (call; `004B1190` is cited on this page); `004B1190` + 0x6C0E (call; `004B1190` is cited on this page); `004B1190` + 0x6C33 (call; `004B1190` is cited on this page); `004B1190` + 0x78EC (call; `004B1190` is cited on this page); `004B1190` + 0x7922 (call; `004B1190` is cited on this page); `004B1190` + 0x7940 (call; `004B1190` is cited on this page); `004B1190` + 0x7965 (call; `004B1190` is cited on this page)
Other direct sites: none

Host context: "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320" / "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320"

```
004B9D80  mov      qword ptr [rsp + 8], rbx
004B9D85  mov      qword ptr [rsp + 0x10], rdi
004B9D8A  movss    xmm4, dword ptr [rdx]
004B9D8E  xor      r9d, r9d
004B9D91  movss    xmm5, dword ptr [r8]
004B9D96  mov      rdi, rcx
004B9D99  ucomiss  xmm4, xmm5
004B9D9C  lea      r10d, [r9 + 1]
004B9DA0  jp       0x4b9da7  ; -> 004B9DA7
004B9DA2  mov      r11d, r10d
004B9DA5  je       0x4b9daa  ; -> 004B9DAA
004B9DA7  mov      r11d, r9d
004B9DAA  movss    xmm0, dword ptr [rdx + 4]
004B9DAF  movss    xmm1, dword ptr [r8 + 4]
004B9DB5  ucomiss  xmm0, xmm1
004B9DB8  jp       0x4b9dbf  ; -> 004B9DBF
004B9DBA  mov      ebx, r10d
004B9DBD  je       0x4b9dc2  ; -> 004B9DC2
004B9DBF  mov      ebx, r9d
004B9DC2  movss    xmm2, dword ptr [rdx + 8]
004B9DC7  movss    xmm3, dword ptr [r8 + 8]
004B9DCD  ucomiss  xmm2, xmm3
004B9DD0  jp       0x4b9dd4  ; -> 004B9DD4
004B9DD2  je       0x4b9dd7  ; -> 004B9DD7
004B9DD4  mov      r10d, r9d
004B9DD7  comiss   xmm3, xmm2
004B9DDA  mov      ecx, r9d
004B9DDD  mov      eax, 4
004B9DE2  mov      edx, 8
004B9DE7  cmova    cx, ax
004B9DEB  mov      eax, r9d
004B9DEE  comiss   xmm1, xmm0
004B9DF1  cmova    ax, dx
004B9DF5  add      cx, ax
004B9DF8  mov      eax, 0x10
004B9DFD  comiss   xmm5, xmm4
004B9E00  cmova    r9w, ax
004B9E05  add      cx, r9w
004B9E09  add      cx, r11w
004B9E0D  add      cx, cx
004B9E10  add      cx, bx
004B9E13  mov      rbx, qword ptr [rsp + 8]
004B9E18  add      cx, cx
004B9E1B  add      cx, r10w
004B9E1F  add      cx, cx
004B9E22  mov      word ptr [rdi], cx
004B9E25  mov      rdi, qword ptr [rsp + 0x10]
004B9E2A  ret      
```

## 004B9E30 (41 B, extent 004B9E30-004B9E59)

Entered from (direct sites whose caller this page cites): `004B1190` + 0x6539 (call; `004B1190` is cited on this page); `004B1190` + 0x7267 (call; `004B1190` is cited on this page)
Other direct sites: none

Host context: "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320" / "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320"

```
004B9E30  movss    xmm0, dword ptr [rdx]
004B9E34  subss    xmm0, xmm2
004B9E38  movss    dword ptr [rcx], xmm0
004B9E3C  movss    xmm1, dword ptr [rdx + 4]
004B9E41  subss    xmm1, xmm2
004B9E45  movss    dword ptr [rcx + 4], xmm1
004B9E4A  movss    xmm0, dword ptr [rdx + 8]
004B9E4F  subss    xmm0, xmm2
004B9E53  movss    dword ptr [rcx + 8], xmm0
004B9E58  ret      
```

## 004B9E60 (50 B, extent 004B9E60-004B9E92)

Entered from (direct sites whose caller this page cites): `004B1190` + 0x7051 (call; `004B1190` is cited on this page); `004B1190` + 0x709D (call; `004B1190` is cited on this page)
Other direct sites: none

Host context: "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320" / "rvals** (timer words '+0x24C' / '+0x24E', reload definition words '+0x2BC' / '+0x2BE', the second gated by '+0x2C0' bit 0), which the walk hands to its program ('0045C00E'–'0045C024') | '0045C882' | '004B1190': line strip + textured strip | 84 / 22 | | '0x61', '0x62' | '0045CDC0', '0045D7D0' | the same code; four operands differ (colour '+0x140' for '0x61'; timer words '+0x280'–'+0x284' / '+0x2C8'–'+0x2CC') | yes | '004B9EA0', '004BC320"

```
004B9E60  movss    xmm0, dword ptr [rdx + 4]
004B9E65  xor      eax, eax
004B9E67  movss    xmm1, dword ptr [r8 + 0xc]
004B9E6D  ucomiss  xmm0, xmm1
004B9E70  jp       0x4b9e77  ; -> 004B9E77
004B9E72  lea      edx, [rax + 1]
004B9E75  je       0x4b9e79  ; -> 004B9E79
004B9E77  mov      edx, eax
004B9E79  comiss   xmm1, xmm0
004B9E7C  mov      r8d, 0x10
004B9E82  cmova    ax, r8w
004B9E87  add      ax, dx
004B9E8A  shl      ax, 2
004B9E8E  mov      word ptr [rcx], ax
004B9E91  ret      
```
