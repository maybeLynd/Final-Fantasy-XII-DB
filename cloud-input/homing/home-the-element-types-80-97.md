# Homing pack: `17-Presentation-Rendering/Effect-File-Formats/the-element-types-80-97.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-element-types-80-97.json`.

Bodies: 6. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0047BFB0 (944 B, extent 0047BFB0-0047C360)

Entered from (direct sites whose caller this page cites): `0047C360` + 0x589 (call; `0047C360` is cited on this page); `00482860` + 0x9F4 (call; `00482860` is cited on this page); `00482860` + 0xD10 (call; `00482860` is cited on this page); `00482860` + 0xDC8 (call; `00482860` is cited on this page); `00482860` + 0x112B (call; `00482860` is cited on this page); `00482860` + 0x11AD (call; `00482860` is cited on this page); `00482860` + 0x12F2 (call; `00482860` is cited on this page); `00485790` + 0x919 (call; `00485790` is cited on this page); `00485790` + 0xD74 (call; `00485790` is cited on this page); `00485790` + 0xEED (call; `00485790` is cited on this page); `00485790` + 0xF9C (call; `00485790` is cited on this page); `00485790` + 0x1152 (call; `00485790` is cited on this page); `0048AF70` + 0xB68 (call; `0048AF70` is cited on this page); `0048D4B0` + 0xBC7 (call; `0048D4B0` is cited on this page); `0048F8C0` + 0x236 (call; `0048F8C0` is cited on this page); `0048F8C0` + 0x7EA (call; `0048F8C0` is cited on this page); `0048F8C0` + 0xA3C (call; `0048F8C0` is cited on this page); `0048F8C0` + 0xB8C (call; `0048F8C0` is cited on this page); `0048F8C0` + 0xE02 (call; `0048F8C0` is cited on this page); `0048F8C0` + 0xF7F (call; `0048F8C0` is cited on this page); `0048F8C0` + 0x12B5 (call; `0048F8C0` is cited on this page); `0048F8C0` + 0x15A1 (call; `0048F8C0` is cited on this page); `0048F8C0` + 0x16F1 (call; `0048F8C0` is cited on this page); `0048F8C0` + 0x195D (call; `0048F8C0` is cited on this page); `0048F8C0` + 0x1BE2 (call; `0048F8C0` is cited on this page); `004930A0` + 0x605 (call; `004930A0` is cited on this page); `004930A0` + 0xA4C (call; `004930A0` is cited on this page); `004930A0` + 0xB19 (call; `004930A0` is cited on this page); `004930A0` + 0xC4F (call; `004930A0` is cited on this page); `004930A0` + 0xDCA (call; `004930A0` is cited on this page); `004930A0` + 0x1117 (call; `004930A0` is cited on this page)
Other direct sites: `004B1190` + 0x37F4 (call); `004B1190` + 0x4E32 (call)

Host context: "| Gouraud LINE '0x049' + POINT '0x040' | line bundles with points | 875 / 334; 617 / 156; 80 / 47; 115 / 87; 175 / 51 | | '0x84', '0x88', '0x89', '0x8B', '0x96' | '0048AF70', '0048F8C0', '00482860', '0047C360', '0048D4B0' | flat textured quad strip '0x054' | textured quads placed by the world matrix | 1,972 / 443; 41 / 31; 36 / 8; 1 / 1; 268 / 65 | | '0x85' | '00488340' | textured strip '0x05C' | a ribbon along the 32-sample path | 78 /" / " '004C2160' | Gouraud LINE '0x049' + POINT '0x040' | line bundles with points | 875 / 334; 617 / 156; 80 / 47; 115 / 87; 175 / 51 | | '0x84', '0x88', '0x89', '0x8B', '0x96' | '0048AF70', '0048F8C0', '00482860', '0047C360', '0048D4B0' | flat textured quad strip '0x054' | textured quads placed by the world matrix | 1,972 / 443; 41 / 31; 36 / 8; 1 / 1; 268 / 65 | | '0x85' | '00488340' | textured strip '0x05C' | a ribbon along the 32-sample"

```
0047BFB0  push     rbx
0047BFB2  sub      rsp, 0x50
0047BFB6  movss    xmm0, dword ptr [rip + 0x198687a]  ; -> 01E02838 [u32 0x00000000]
0047BFBE  mov      eax, 0x80
0047BFC3  movss    xmm2, dword ptr [rip + 0x1986871]  ; -> 01E0283C [f32 1]
0047BFCB  xor      ebx, ebx
0047BFCD  movzx    ecx, word ptr [rip + 0x1be8b38]  ; -> 02064B0C
0047BFD4  movaps   xmm3, xmm2
0047BFD7  add      cx, ax
0047BFDA  mov      dword ptr [rip + 0x1be8b20], 0x4096cbe4  ; -> 02064B04
0047BFE4  movss    xmm1, dword ptr [rip + 0x1be8b18]  ; -> 02064B04
0047BFEC  mov      eax, ebx
0047BFEE  comiss   xmm1, dword ptr [rip + 0x1be8cbb]  ; -> 02064CB0
0047BFF5  mov      dword ptr [rsp + 0x60], 0x40c90fdb
0047BFFD  mov      word ptr [rip + 0x1be8dd0], cx  ; -> 02064DD4
0047C004  mov      dword ptr [rip + 0x1be8af6], 0x40c90fdb  ; -> 02064B04
0047C00E  addss    xmm0, xmm1
0047C012  movaps   xmmword ptr [rsp + 0x40], xmm6
0047C017  addss    xmm3, dword ptr [rsp + 0x60]
0047C01D  movss    xmm1, dword ptr [rip + 0x198680f]  ; -> 01E02834 [u32 0x00000000]
0047C025  seta     al
0047C028  mov      dword ptr [rsp + 0x60], 0x3fc90fdb
0047C030  shl      ax, 7
0047C034  movss    dword ptr [rip + 0x1be8c8c], xmm0  ; -> 02064CC8
0047C03C  and      ax, cx
0047C03F  movaps   xmmword ptr [rsp + 0x30], xmm7
0047C044  movaps   xmmword ptr [rsp + 0x20], xmm8
0047C04A  subss    xmm3, xmm2
0047C04E  movss    xmm0, dword ptr [rip + 0x19867da]  ; -> 01E02830 [u32 0x00000000]
0047C056  addss    xmm0, dword ptr [rsp + 0x60]
0047C05C  mov      dword ptr [rsp + 0x60], 0x40490fdb
0047C064  addss    xmm1, dword ptr [rsp + 0x60]
0047C06A  mov      word ptr [rip + 0x1be8d57], ax  ; -> 02064DC8
0047C071  movss    dword ptr [rip + 0x1be8c53], xmm3  ; -> 02064CCC
0047C079  movss    dword ptr [rip + 0x1be8c3f], xmm0  ; -> 02064CC0
0047C081  movss    dword ptr [rip + 0x1be8c3b], xmm1  ; -> 02064CC4
0047C089  call     0x22cc20  ; -> 0022CC20 fn
0047C08E  movzx    eax, word ptr [rip + 0x1be8a77]  ; -> 02064B0C
0047C095  cmp      word ptr [rip + 0x1be8d2c], ax  ; -> 02064DC8
0047C09C  movss    xmm5, dword ptr [rip + 0x1be8c0c]  ; -> 02064CB0
0047C0A4  jne      0x47c0b6  ; -> 0047C0B6
0047C0A6  subss    xmm5, dword ptr [rip + 0x1be8a56]  ; -> 02064B04
0047C0AE  movss    dword ptr [rip + 0x1be8bfa], xmm5  ; -> 02064CB0
0047C0B6  movss    xmm3, dword ptr [rip + 0x1be8c02]  ; -> 02064CC0
0047C0BE  mov      eax, ebx
0047C0C0  movss    xmm4, dword ptr [rip + 0x1986768]  ; -> 01E02830 [u32 0x00000000]
0047C0C8  movzx    ecx, word ptr [rip + 0x1be8d05]  ; -> 02064DD4
0047C0CF  movss    xmm0, dword ptr [rip + 0x1be8bf1]  ; -> 02064CC8
0047C0D7  movss    xmm2, dword ptr [rip + 0x1986755]  ; -> 01E02834 [u32 0x00000000]
0047C0DF  comiss   xmm4, xmm5
0047C0E2  movaps   xmm1, xmm2
0047C0E5  addss    xmm2, xmm3
0047C0E9  addss    xmm1, xmm5
0047C0ED  seta     al
0047C0F0  shl      ax, 7
0047C0F4  and      ax, cx
0047C0F7  mov      word ptr [rip + 0x1be8cca], ax  ; -> 02064DC8
0047C0FE  mov      eax, ebx
0047C100  comiss   xmm3, xmm5
0047C103  movss    dword ptr [rip + 0x1be8bc9], xmm1  ; -> 02064CD4
0047C10B  movss    dword ptr [rip + 0x1be8bd1], xmm2  ; -> 02064CE4
0047C113  seta     al
0047C116  shl      ax, 7
0047C11A  and      ax, cx
0047C11D  comiss   xmm0, xmm5
0047C120  mov      word ptr [rip + 0x1be8ca5], ax  ; -> 02064DCC
0047C127  movaps   xmm0, xmm4
0047C12A  addss    xmm0, xmm5
0047C12E  seta     bl
0047C131  subss    xmm5, xmm3
0047C135  shl      bx, 7
0047C139  and      bx, cx
0047C13C  mov      word ptr [rip + 0x1be8c8d], bx  ; -> 02064DD0
0047C143  movss    dword ptr [rip + 0x1be8b85], xmm0  ; -> 02064CD0
0047C14B  movaps   xmm0, xmm3
0047C14E  addss    xmm0, xmm4
0047C152  movss    dword ptr [rip + 0x1be8b96], xmm5  ; -> 02064CF0
0047C15A  movss    dword ptr [rip + 0x1be8b7e], xmm0  ; -> 02064CE0
0047C162  call     0x22cc20  ; -> 0022CC20 fn
0047C167  movzx    eax, word ptr [rip + 0x1be899e]  ; -> 02064B0C
0047C16E  cmp      word ptr [rip + 0x1be8c53], ax  ; -> 02064DC8
0047C175  je       0x47c18c  ; -> 0047C18C
0047C177  movss    xmm3, dword ptr [rip + 0x1be8b55]  ; -> 02064CD4
0047C17F  addss    xmm3, dword ptr [rip + 0x1be8b39]  ; -> 02064CC0
0047C187  jmp      0x47c222  ; -> 0047C222
0047C18C  cmp      word ptr [rip + 0x1be8c39], ax  ; -> 02064DCC
0047C193  movss    xmm1, dword ptr [rip + 0x1be8b39]  ; -> 02064CD4
0047C19B  movaps   xmm0, xmm1
0047C19E  subss    xmm0, dword ptr [rip + 0x1be8b22]  ; -> 02064CC8
0047C1A6  movss    dword ptr [rip + 0x1be8b46], xmm0  ; -> 02064CF4
0047C1AE  je       0x47c1d3  ; -> 0047C1D3
0047C1B0  movss    xmm0, dword ptr [rip + 0x1be8b2c]  ; -> 02064CE4
0047C1B8  subss    xmm0, xmm1
0047C1BC  movss    dword ptr [rip + 0x1be8b10], xmm0  ; -> 02064CD4
0047C1C4  call     0x22cc20  ; -> 0022CC20 fn
0047C1C9  movss    xmm3, dword ptr [rip + 0x1be8b03]  ; -> 02064CD4
0047C1D1  jmp      0x47c22a  ; -> 0047C22A
0047C1D3  movss    xmm0, dword ptr [rip + 0x1be8ae5]  ; -> 02064CC0
0047C1DB  subss    xmm0, dword ptr [rip + 0x1be8b0d]  ; -> 02064CF0
0047C1E3  movss    dword ptr [rip + 0x1be8ae5], xmm0  ; -> 02064CD0
0047C1EB  call     0x22cc20  ; -> 0022CC20 fn
0047C1F0  movzx    eax, word ptr [rip + 0x1be8915]  ; -> 02064B0C
0047C1F7  cmp      word ptr [rip + 0x1be8bd2], ax  ; -> 02064DD0
0047C1FE  je       0x47c212  ; -> 0047C212
0047C200  movss    xmm3, dword ptr [rip + 0x1be8adc]  ; -> 02064CE4
0047C208  subss    xmm3, dword ptr [rip + 0x1be8aa0]  ; -> 02064CB0
0047C210  jmp      0x47c222  ; -> 0047C222
0047C212  movss    xmm3, dword ptr [rip + 0x1be8ada]  ; -> 02064CF4
0047C21A  addss    xmm3, dword ptr [rip + 0x1986612]  ; -> 01E02834 [u32 0x00000000]
0047C222  movss    dword ptr [rip + 0x1be8aaa], xmm3  ; -> 02064CD4
0047C22A  movss    xmm2, dword ptr [rip + 0x1be8a9e]  ; -> 02064CD0
0047C232  movaps   xmm8, xmm3
0047C236  movaps   xmm7, xmm2
0047C239  mulss    xmm8, xmm3
0047C23E  mov      dword ptr [rsp + 0x60], 0xbe2aaaa4
0047C246  mulss    xmm7, xmm2
0047C24A  movaps   xmm5, xmm2
0047C24D  mov      dword ptr [rip + 0x1be88ad], 0x362e9c14  ; -> 02064B04
0047C257  mulss    xmm5, dword ptr [rip + 0x19865dd]  ; -> 01E0283C [f32 1]
0047C25F  movaps   xmm6, xmm3
0047C262  mulss    xmm6, dword ptr [rip + 0x19865d2]  ; -> 01E0283C [f32 1]
0047C26A  movaps   xmm4, xmm8
0047C26E  movaps   xmm1, xmm7
0047C271  movss    dword ptr [rip + 0x1be8a77], xmm7  ; -> 02064CF0
0047C279  mulss    xmm1, xmm2
0047C27D  movaps   xmm2, xmm8
0047C281  mulss    xmm2, xmm3
0047C285  movaps   xmm3, xmm7
0047C288  mulss    xmm3, xmm1
0047C28C  mulss    xmm1, dword ptr [rsp + 0x60]
0047C292  mulss    xmm4, xmm2
0047C296  mulss    xmm2, dword ptr [rsp + 0x60]
0047C29C  addss    xmm5, xmm1
0047C2A0  mov      dword ptr [rsp + 0x60], 0x3c08873e
0047C2A8  movaps   xmm1, xmm7
0047C2AB  movss    dword ptr [rip + 0x1be8a40], xmm8  ; -> 02064CF4
0047C2B4  mulss    xmm1, xmm3
0047C2B8  mulss    xmm3, dword ptr [rsp + 0x60]
0047C2BE  addss    xmm6, xmm2
0047C2C2  mulss    xmm7, xmm1
0047C2C6  movaps   xmm2, xmm8
0047C2CA  mulss    xmm2, xmm4
0047C2CE  addss    xmm5, xmm3
0047C2D2  mulss    xmm4, dword ptr [rsp + 0x60]
0047C2D8  mov      dword ptr [rsp + 0x60], 0xb94fb21f
0047C2E0  mulss    xmm1, dword ptr [rsp + 0x60]
0047C2E6  mulss    xmm8, xmm2
0047C2EB  addss    xmm6, xmm4
0047C2EF  mulss    xmm2, dword ptr [rsp + 0x60]
0047C2F5  addss    xmm5, xmm1
0047C2F9  movss    xmm1, dword ptr [rip + 0x1be8803]  ; -> 02064B04
0047C301  movaps   xmm0, xmm1
0047C304  movss    dword ptr [rip + 0x1be89d4], xmm7  ; -> 02064CE0
0047C30C  addss    xmm6, xmm2
0047C310  mulss    xmm0, xmm7
0047C314  movaps   xmm7, xmmword ptr [rsp + 0x30]
0047C319  mulss    xmm1, xmm8
0047C31E  addss    xmm0, xmm5
0047C322  movss    dword ptr [rip + 0x1be89b9], xmm8  ; -> 02064CE4
0047C32B  movaps   xmm8, xmmword ptr [rsp + 0x20]
0047C331  addss    xmm1, xmm6
0047C335  movss    dword ptr [rip + 0x1be87e7], xmm6  ; -> 02064B24
0047C33D  movaps   xmm6, xmmword ptr [rsp + 0x40]
0047C342  movss    dword ptr [rip + 0x1be87d6], xmm5  ; -> 02064B20
0047C34A  movss    dword ptr [rip + 0x1be895e], xmm0  ; -> 02064CB0
0047C352  movss    dword ptr [rip + 0x1be895a], xmm1  ; -> 02064CB4
0047C35A  add      rsp, 0x50
0047C35E  pop      rbx
0047C35F  ret      
```

## 00487D60 (551 B, extent 00487D60-00487F87)

Entered from (direct sites whose caller this page cites): `00488340` + 0x96D (call; `00488340` is cited on this page)
Other direct sites: none

Host context: "'0048AF70', '0048F8C0', '00482860', '0047C360', '0048D4B0' | flat textured quad strip '0x054' | textured quads placed by the world matrix | 1,972 / 443; 41 / 31; 36 / 8; 1 / 1; 268 / 65 | | '0x85' | '00488340' | textured strip '0x05C' | a ribbon along the 32-sample path | 78 / 41 | | '0x8C'–'0x92', '0x95' | '00497AC0' / '00499A20', '004BF500', '0049B9E0', '0049D540' / '004A0090', '004A4410' / '004A33B0' / '004A1E30', '004A6C20', '004A8B"

```
00487D60  sub      rsp, 0x48
00487D64  movss    xmm2, dword ptr [rip + 0x1bdcf44]  ; -> 02064CB0
00487D6C  xor      eax, eax
00487D6E  movss    xmm3, dword ptr [rip + 0x1bdcf3e]  ; -> 02064CB4
00487D76  ucomiss  xmm2, xmm3
00487D79  movaps   xmmword ptr [rsp + 0x30], xmm6
00487D7E  movaps   xmmword ptr [rsp + 0x20], xmm7
00487D83  jp       0x487d8a  ; -> 00487D8A
00487D85  lea      ecx, [rax + 1]
00487D88  je       0x487d8c  ; -> 00487D8C
00487D8A  mov      ecx, eax
00487D8C  movss    xmm0, dword ptr [rip + 0x1863ddc]  ; -> 01CEBB70 [f32 0.5]
00487D94  xorps    xmm7, xmm7
00487D97  movss    xmm6, dword ptr [rip + 0x4785c1]  ; -> 00900360 [u32 0x7F7FFFFF]
00487D9F  comiss   xmm3, xmm2
00487DA2  movss    dword ptr [rip + 0x1bdcd5a], xmm0  ; -> 02064B04
00487DAA  seta     al
00487DAD  shl      ax, 4
00487DB1  add      ax, cx
00487DB4  movzx    ecx, word ptr [rip + 0x1bdcd51]  ; -> 02064B0C
00487DBB  shl      ax, 3
00487DBF  mov      word ptr [rip + 0x1bdcd4a], ax  ; -> 02064B10
00487DC6  and      ax, word ptr [rip + 0x1bdd013]  ; -> 02064DE0
00487DCD  mov      word ptr [rip + 0x1bdd004], ax  ; -> 02064DD8
00487DD4  cmp      ax, cx
00487DD7  jne      0x487e4c  ; -> 00487E4C
00487DD9  cmp      word ptr [rip + 0x1bdcff4], cx  ; -> 02064DD4
00487DE0  jne      0x487ec8  ; -> 00487EC8
00487DE6  ucomiss  xmm3, xmm7
00487DE9  jp       0x487dfa  ; -> 00487DFA
00487DEB  jne      0x487dfa  ; -> 00487DFA
00487DED  movss    dword ptr [rip + 0x1bdcd0b], xmm6  ; -> 02064B00
00487DF5  movaps   xmm1, xmm6
00487DF8  jmp      0x487e09  ; -> 00487E09
00487DFA  movaps   xmm1, xmm2
00487DFD  divss    xmm1, xmm3
00487E01  movss    dword ptr [rip + 0x1bdccf7], xmm1  ; -> 02064B00
00487E09  movss    xmm0, dword ptr [rip + 0x197aa1f]  ; -> 01E02830 [u32 0x00000000]
00487E11  addss    xmm0, xmm1
00487E15  cvttss2si eax, xmm0
00487E19  movd     xmm1, eax
00487E1D  cvtdq2ps xmm1, xmm1
00487E20  mulss    xmm1, xmm3
00487E24  subss    xmm2, xmm1
00487E28  movss    dword ptr [rip + 0x1bdce90], xmm1  ; -> 02064CC0
00487E30  movss    dword ptr [rip + 0x1bdce78], xmm2  ; -> 02064CB0
00487E38  call     0x22cc20  ; -> 0022CC20 fn
00487E3D  movss    xmm2, dword ptr [rip + 0x1bdce6b]  ; -> 02064CB0
00487E45  movzx    ecx, word ptr [rip + 0x1bdccc0]  ; -> 02064B0C
00487E4C  cmp      word ptr [rip + 0x1bdcf79], cx  ; -> 02064DCC
00487E53  je       0x487f0f  ; -> 00487F0F
00487E59  movzx    edx, word ptr [rip + 0x1bdcf68]  ; -> 02064DC8
00487E60  lea      r9, [rip + 0x1bdcfc9]  ; -> 02064E30
00487E67  cvttss2si eax, xmm2
00487E6B  mov      dword ptr [rip + 0x1bdce3f], eax  ; -> 02064CB0
00487E71  movzx    r8d, ax
00487E75  nop      word ptr [rax + rax]
00487E80  movsx    eax, dx
00487E83  inc      dx
00487E86  shl      eax, 4
00487E89  movsxd   rcx, eax
00487E8C  movzx    eax, word ptr [rcx + r9 + 4]
00487E92  sub      r8w, ax
00487E96  mov      word ptr [rip + 0x1bdcf33], ax  ; -> 02064DD0
00487E9D  test     r8w, r8w
00487EA1  jg       0x487e80  ; -> 00487E80
00487EA3  dec      dx
00487EA6  mov      word ptr [rip + 0x1bdcf26], r8w  ; -> 02064DD4
00487EAE  movsx    eax, dx
00487EB1  shl      eax, 4
00487EB4  movsxd   rcx, eax
00487EB7  mov      word ptr [rip + 0x1bdcf0a], dx  ; -> 02064DC8
00487EBE  movzx    eax, word ptr [rcx + r9]
00487EC3  jmp      0x487f71  ; -> 00487F71
00487EC8  movzx    eax, word ptr [rip + 0x1bdcefd]  ; -> 02064DCC
00487ECF  cmp      ax, cx
00487ED2  jne      0x487ee3  ; -> 00487EE3
00487ED4  movzx    eax, word ptr [rip + 0x1bdcef5]  ; -> 02064DD0
00487EDB  dec      ax
00487EDE  jmp      0x487f71  ; -> 00487F71
00487EE3  movsx    ecx, ax
00487EE6  lea      r9, [rip + 0x1bdcf43]  ; -> 02064E30
00487EED  movzx    eax, word ptr [rip + 0x1bdced4]  ; -> 02064DC8
00487EF4  dec      cx
00487EF7  add      ax, cx
00487EFA  mov      word ptr [rip + 0x1bdcec7], ax  ; -> 02064DC8
00487F01  cwde     
00487F02  shl      eax, 4
00487F05  movsxd   rcx, eax
00487F08  movzx    eax, word ptr [rcx + r9]
00487F0D  jmp      0x487f71  ; -> 00487F71
00487F0F  movss    xmm0, dword ptr [rip + 0x1bdcda1]  ; -> 02064CB8
00487F17  ucomiss  xmm0, xmm7
00487F1A  jp       0x487f1e  ; -> 00487F1E
00487F1C  je       0x487f25  ; -> 00487F25
00487F1E  movaps   xmm6, xmm2
00487F21  divss    xmm6, xmm0
00487F25  movss    xmm0, dword ptr [rip + 0x197a907]  ; -> 01E02834 [u32 0x00000000]
00487F2D  addss    xmm0, xmm6
00487F31  movss    dword ptr [rip + 0x1bdcbc7], xmm6  ; -> 02064B00
00487F39  ucomiss  xmm0, xmm7
00487F3C  movss    dword ptr [rip + 0x1bdcd70], xmm0  ; -> 02064CB4
00487F44  jp       0x487f55  ; -> 00487F55
00487F46  jne      0x487f55  ; -> 00487F55
00487F48  call     0x22cc40  ; -> 0022CC40 fn
00487F4D  movss    xmm0, dword ptr [rip + 0x1bdcd5f]  ; -> 02064CB4
00487F55  comiss   xmm7, xmm0
00487F58  jbe      0x487f67  ; -> 00487F67
00487F5A  call     0x22cc30  ; -> 0022CC30 fn
00487F5F  movss    xmm0, dword ptr [rip + 0x1bdcd4d]  ; -> 02064CB4
00487F67  cvttss2si eax, xmm0
00487F6B  mov      dword ptr [rip + 0x1bdcd43], eax  ; -> 02064CB4
00487F71  movaps   xmm6, xmmword ptr [rsp + 0x30]
00487F76  movaps   xmm7, xmmword ptr [rsp + 0x20]
00487F7B  mov      word ptr [rip + 0x1bdce4a], ax  ; -> 02064DCC
00487F82  add      rsp, 0x48
00487F86  ret      
```

## 00487F90 (937 B, extent 00487F90-00488339)

Entered from (direct sites whose caller this page cites): `00488340` + 0x1112 (call; `00488340` is cited on this page)
Other direct sites: none

Host context: "'0048AF70', '0048F8C0', '00482860', '0047C360', '0048D4B0' | flat textured quad strip '0x054' | textured quads placed by the world matrix | 1,972 / 443; 41 / 31; 36 / 8; 1 / 1; 268 / 65 | | '0x85' | '00488340' | textured strip '0x05C' | a ribbon along the 32-sample path | 78 / 41 | | '0x8C'–'0x92', '0x95' | '00497AC0' / '00499A20', '004BF500', '0049B9E0', '0049D540' / '004A0090', '004A4410' / '004A33B0' / '004A1E30', '004A6C20', '004A8B"

```
00487F90  sub      rsp, 0x68
00487F94  movss    xmm0, dword ptr [rip + 0x1bdcd14]  ; -> 02064CB0
00487F9C  subss    xmm0, dword ptr [rip + 0x1bdcd1c]  ; -> 02064CC0
00487FA4  movaps   xmmword ptr [rsp + 0x50], xmm6
00487FA9  movaps   xmmword ptr [rsp + 0x40], xmm7
00487FAE  movaps   xmmword ptr [rsp + 0x30], xmm8
00487FB4  movaps   xmmword ptr [rsp + 0x20], xmm9
00487FBA  movss    dword ptr [rip + 0x1bdccee], xmm0  ; -> 02064CB0
00487FC2  call     0x22cc20  ; -> 0022CC20 fn
00487FC7  movzx    r10d, word ptr [rip + 0x1bdcb3d]  ; -> 02064B0C
00487FCF  mov      eax, 0x80
00487FD4  movss    xmm3, dword ptr [rip + 0x1bdccd4]  ; -> 02064CB0
00487FDC  add      r10w, ax
00487FE0  movss    xmm4, dword ptr [rip + 0x197a848]  ; -> 01E02830 [u32 0x00000000]
00487FE8  xor      ecx, ecx
00487FEA  ucomiss  xmm3, xmm4
00487FED  lea      r9d, [rax - 0x7f]
00487FF1  mov      word ptr [rip + 0x1bdcddb], r10w  ; -> 02064DD4
00487FF9  jp       0x488000  ; -> 00488000
00487FFB  mov      eax, r9d
00487FFE  je       0x488002  ; -> 00488002
00488000  mov      eax, ecx
00488002  movss    xmm5, dword ptr [rip + 0x1bdccb6]  ; -> 02064CC0
0048800A  mov      edx, ecx
0048800C  comiss   xmm4, xmm3
0048800F  seta     dl
00488012  shl      dx, 4
00488016  add      dx, ax
00488019  shl      dx, 3
0048801D  ucomiss  xmm3, xmm5
00488020  mov      word ptr [rip + 0x1bdcae9], dx  ; -> 02064B10
00488027  jp       0x48802e  ; -> 0048802E
00488029  mov      eax, r9d
0048802C  je       0x488030  ; -> 00488030
0048802E  mov      eax, ecx
00488030  movss    xmm0, dword ptr [rip + 0x1bdcc8c]  ; -> 02064CC4
00488038  mov      r8d, ecx
0048803B  comiss   xmm5, xmm3
0048803E  seta     r8b
00488042  shl      r8w, 4
00488047  add      r8w, ax
0048804B  shl      r8w, 3
00488050  ucomiss  xmm3, xmm0
00488053  mov      word ptr [rip + 0x1bdcab7], r8w  ; -> 02064B12
0048805B  jp       0x488062  ; -> 00488062
0048805D  mov      r11d, r9d
00488060  je       0x488065  ; -> 00488065
00488062  mov      r11d, ecx
00488065  comiss   xmm0, xmm3
00488068  mov      eax, ecx
0048806A  movss    xmm0, dword ptr [rip + 0x1bdcc56]  ; -> 02064CC8
00488072  seta     al
00488075  shl      ax, 4
00488079  add      ax, r11w
0048807D  shl      ax, 3
00488081  ucomiss  xmm3, xmm0
00488084  mov      word ptr [rip + 0x1bdca89], ax  ; -> 02064B14
0048808B  jp       0x48808f  ; -> 0048808F
0048808D  je       0x488092  ; -> 00488092
0048808F  mov      r9d, ecx
00488092  movss    xmm2, dword ptr [rip + 0x197a79a]  ; -> 01E02834 [u32 0x00000000]
0048809A  comiss   xmm0, xmm3
0048809D  movaps   xmm0, xmm4
004880A0  movaps   xmm1, xmm2
004880A3  addss    xmm0, xmm3
004880A7  seta     cl
004880AA  addss    xmm1, xmm3
004880AE  shl      cx, 4
004880B2  addss    xmm4, xmm5
004880B6  addss    xmm2, xmm5
004880BA  add      cx, r9w
004880BE  subss    xmm3, xmm5
004880C2  shl      cx, 3
004880C6  and      dx, r10w
004880CA  mov      word ptr [rip + 0x1bdca45], cx  ; -> 02064B16
004880D1  and      r8w, r10w
004880D5  movss    dword ptr [rip + 0x1bdcbf3], xmm0  ; -> 02064CD0
004880DD  movss    dword ptr [rip + 0x1bdcbef], xmm1  ; -> 02064CD4
004880E5  movss    dword ptr [rip + 0x1bdcbf3], xmm4  ; -> 02064CE0
004880ED  movss    dword ptr [rip + 0x1bdcbef], xmm2  ; -> 02064CE4
004880F5  movss    dword ptr [rip + 0x1bdcbf3], xmm3  ; -> 02064CF0
004880FD  mov      word ptr [rip + 0x1bdccc4], dx  ; -> 02064DC8
00488104  mov      word ptr [rip + 0x1bdccc0], r8w  ; -> 02064DCC
0048810C  call     0x22cc20  ; -> 0022CC20 fn
00488111  movzx    eax, word ptr [rip + 0x1bdc9fe]  ; -> 02064B16
00488118  and      ax, word ptr [rip + 0x1bdccb5]  ; -> 02064DD4
0048811F  mov      word ptr [rip + 0x1bdccaa], ax  ; -> 02064DD0
00488126  movzx    eax, word ptr [rip + 0x1bdc9df]  ; -> 02064B0C
0048812D  cmp      word ptr [rip + 0x1bdcc94], ax  ; -> 02064DC8
00488134  je       0x48814b  ; -> 0048814B
00488136  movss    xmm1, dword ptr [rip + 0x1bdcb96]  ; -> 02064CD4
0048813E  addss    xmm1, dword ptr [rip + 0x1bdcb7a]  ; -> 02064CC0
00488146  jmp      0x4881e1  ; -> 004881E1
0048814B  cmp      word ptr [rip + 0x1bdcc7a], ax  ; -> 02064DCC
00488152  movss    xmm2, dword ptr [rip + 0x1bdcb7a]  ; -> 02064CD4
0048815A  movaps   xmm0, xmm2
0048815D  subss    xmm0, dword ptr [rip + 0x1bdcb63]  ; -> 02064CC8
00488165  movss    dword ptr [rip + 0x1bdcb87], xmm0  ; -> 02064CF4
0048816D  je       0x488192  ; -> 00488192
0048816F  movss    xmm0, dword ptr [rip + 0x1bdcb6d]  ; -> 02064CE4
00488177  subss    xmm0, xmm2
0048817B  movss    dword ptr [rip + 0x1bdcb51], xmm0  ; -> 02064CD4
00488183  call     0x22cc20  ; -> 0022CC20 fn
00488188  movss    xmm1, dword ptr [rip + 0x1bdcb44]  ; -> 02064CD4
00488190  jmp      0x4881e9  ; -> 004881E9
00488192  movss    xmm0, dword ptr [rip + 0x1bdcb26]  ; -> 02064CC0
0048819A  subss    xmm0, dword ptr [rip + 0x1bdcb4e]  ; -> 02064CF0
004881A2  movss    dword ptr [rip + 0x1bdcb26], xmm0  ; -> 02064CD0
004881AA  call     0x22cc20  ; -> 0022CC20 fn
004881AF  movzx    eax, word ptr [rip + 0x1bdc956]  ; -> 02064B0C
004881B6  cmp      word ptr [rip + 0x1bdcc13], ax  ; -> 02064DD0
004881BD  je       0x4881d1  ; -> 004881D1
004881BF  movss    xmm1, dword ptr [rip + 0x1bdcb1d]  ; -> 02064CE4
004881C7  subss    xmm1, dword ptr [rip + 0x1bdcae1]  ; -> 02064CB0
004881CF  jmp      0x4881e1  ; -> 004881E1
004881D1  movss    xmm1, dword ptr [rip + 0x1bdcb1b]  ; -> 02064CF4
004881D9  addss    xmm1, dword ptr [rip + 0x197a653]  ; -> 01E02834 [u32 0x00000000]
004881E1  movss    dword ptr [rip + 0x1bdcaeb], xmm1  ; -> 02064CD4
004881E9  movss    xmm0, dword ptr [rip + 0x1bdcadf]  ; -> 02064CD0
004881F1  movaps   xmm9, xmm1
004881F5  movss    xmm7, dword ptr [rip + 0x197a63f]  ; -> 01E0283C [f32 1]
004881FD  movaps   xmm8, xmm0
00488201  mulss    xmm9, xmm1
00488206  movaps   xmm6, xmm7
00488209  mov      dword ptr [rsp + 0x70], 0xbe2aaaa4
00488211  mulss    xmm8, xmm0
00488216  mov      dword ptr [rip + 0x1bdc8e4], 0x362e9c14  ; -> 02064B04
00488220  mulss    xmm7, xmm1
00488224  movaps   xmm3, xmm9
00488228  mulss    xmm6, xmm0
0048822C  movaps   xmm5, xmm9
00488230  mulss    xmm3, xmm1
00488234  movaps   xmm2, xmm8
00488238  movss    xmm1, dword ptr [rsp + 0x70]
0048823E  movaps   xmm4, xmm8
00488242  mulss    xmm2, xmm0
00488246  movaps   xmm0, xmm1
00488249  mov      dword ptr [rsp + 0x70], 0x3c08873e
00488251  mulss    xmm1, xmm3
00488255  mulss    xmm5, xmm3
00488259  movaps   xmm3, xmm9
0048825D  mulss    xmm0, xmm2
00488261  addss    xmm7, xmm1
00488265  movss    xmm1, dword ptr [rsp + 0x70]
0048826B  mulss    xmm4, xmm2
0048826F  movaps   xmm2, xmm8
00488273  mov      dword ptr [rsp + 0x70], 0xb94fb21f
0048827B  addss    xmm6, xmm0
0048827F  mulss    xmm3, xmm5
00488283  movaps   xmm0, xmm1
00488286  movss    dword ptr [rip + 0x1bdca61], xmm8  ; -> 02064CF0
0048828F  mulss    xmm1, xmm5
00488293  mulss    xmm0, xmm4
00488297  addss    xmm7, xmm1
0048829B  mulss    xmm2, xmm4
0048829F  movss    xmm1, dword ptr [rsp + 0x70]
004882A5  addss    xmm6, xmm0
004882A9  movaps   xmm0, xmm1
004882AC  movss    dword ptr [rip + 0x1bdca3f], xmm9  ; -> 02064CF4
004882B5  mulss    xmm1, xmm3
004882B9  mulss    xmm0, xmm2
004882BD  addss    xmm7, xmm1
004882C1  mulss    xmm8, xmm2
004882C6  movss    xmm1, dword ptr [rip + 0x1bdc836]  ; -> 02064B04
004882CE  addss    xmm6, xmm0
004882D2  mulss    xmm9, xmm3
004882D7  movaps   xmm0, xmm1
004882DA  mulss    xmm0, xmm8
004882DF  mulss    xmm1, xmm9
004882E4  addss    xmm0, xmm6
004882E8  movss    dword ptr [rip + 0x1bdc9ef], xmm8  ; -> 02064CE0
004882F1  movaps   xmm8, xmmword ptr [rsp + 0x30]
004882F7  addss    xmm1, xmm7
004882FB  movss    dword ptr [rip + 0x1bdc9e0], xmm9  ; -> 02064CE4
00488304  movaps   xmm9, xmmword ptr [rsp + 0x20]
0048830A  movss    dword ptr [rip + 0x1bdc80e], xmm6  ; -> 02064B20
00488312  movaps   xmm6, xmmword ptr [rsp + 0x50]
00488317  movss    dword ptr [rip + 0x1bdc805], xmm7  ; -> 02064B24
0048831F  movaps   xmm7, xmmword ptr [rsp + 0x40]
00488324  movss    dword ptr [rip + 0x1bdc984], xmm0  ; -> 02064CB0
0048832C  movss    dword ptr [rip + 0x1bdc980], xmm1  ; -> 02064CB4
00488334  add      rsp, 0x68
00488338  ret      
```

## 0048D240 (619 B, extent 0048D240-0048D4AB)

Entered from (direct sites whose caller this page cites): `0048D4B0` + 0xD97 (call; `0048D4B0` is cited on this page)
Other direct sites: none

Host context: "NE '0x049' + POINT '0x040' | line bundles with points | 875 / 334; 617 / 156; 80 / 47; 115 / 87; 175 / 51 | | '0x84', '0x88', '0x89', '0x8B', '0x96' | '0048AF70', '0048F8C0', '00482860', '0047C360', '0048D4B0' | flat textured quad strip '0x054' | textured quads placed by the world matrix | 1,972 / 443; 41 / 31; 36 / 8; 1 / 1; 268 / 65 | | '0x85' | '00488340' | textured strip '0x05C' | a ribbon along the 32-sample path | 78 / 41 | | '0x8"

```
0048D240  sub      rsp, 0x48
0048D244  movzx    ecx, word ptr [rip + 0x1bd78c1]  ; -> 02064B0C
0048D24B  xor      r9d, r9d
0048D24E  movss    xmm3, dword ptr [rip + 0x1bd7a5e]  ; -> 02064CB4
0048D256  mov      edx, 0xe0
0048D25B  movss    xmm2, dword ptr [rip + 0x1bd7a4d]  ; -> 02064CB0
0048D263  movzx    r8d, word ptr [rip + 0x1bd7b65]  ; -> 02064DD0
0048D26B  comiss   xmm3, xmm2
0048D26E  lea      eax, [rdx + rcx]
0048D271  mov      dword ptr [rip + 0x1bd7889], 0x3f000000  ; -> 02064B04
0048D27B  seta     r9b
0048D27F  shl      r9w, 7
0048D284  and      r9w, ax
0048D288  lea      eax, [rcx + 1]
0048D28B  mov      word ptr [rip + 0x1bd7b45], r9w  ; -> 02064DD8
0048D293  mov      word ptr [rip + 0x1bd7b2e], ax  ; -> 02064DC8
0048D29A  cmp      r8w, ax
0048D29E  jne      0x48d2ac  ; -> 0048D2AC
0048D2A0  mov      word ptr [rip + 0x1bd7b25], cx  ; -> 02064DCC
0048D2A7  add      rsp, 0x48
0048D2AB  ret      
0048D2AC  movaps   xmmword ptr [rsp + 0x30], xmm6
0048D2B1  mov      eax, 0x1c2
0048D2B6  movss    xmm6, dword ptr [rip + 0x4730a2]  ; -> 00900360 [u32 0x7F7FFFFF]
0048D2BE  movaps   xmmword ptr [rsp + 0x20], xmm7
0048D2C3  xorps    xmm7, xmm7
0048D2C6  lea      edx, [rax + rcx]
0048D2C9  mov      word ptr [rip + 0x1bd7af8], dx  ; -> 02064DC8
0048D2D0  cmp      r9w, cx
0048D2D4  jne      0x48d35e  ; -> 0048D35E
0048D2DA  cmp      word ptr [rip + 0x1bd7af3], cx  ; -> 02064DD4
0048D2E1  mov      dword ptr [rip + 0x1bd7819], 0x3f000000  ; -> 02064B04
0048D2EB  jne      0x48d3d4  ; -> 0048D3D4
0048D2F1  ucomiss  xmm3, xmm7
0048D2F4  jp       0x48d305  ; -> 0048D305
0048D2F6  jne      0x48d305  ; -> 0048D305
0048D2F8  movss    dword ptr [rip + 0x1bd7800], xmm6  ; -> 02064B00
0048D300  movaps   xmm1, xmm6
0048D303  jmp      0x48d314  ; -> 0048D314
0048D305  movaps   xmm1, xmm2
0048D308  divss    xmm1, xmm3
0048D30C  movss    dword ptr [rip + 0x1bd77ec], xmm1  ; -> 02064B00
0048D314  movss    xmm0, dword ptr [rip + 0x1975514]  ; -> 01E02830 [u32 0x00000000]
0048D31C  addss    xmm0, xmm1
0048D320  cvttss2si eax, xmm0
0048D324  movd     xmm1, eax
0048D328  cvtdq2ps xmm1, xmm1
0048D32B  mulss    xmm1, xmm3
0048D32F  subss    xmm2, xmm1
0048D333  movss    dword ptr [rip + 0x1bd7985], xmm1  ; -> 02064CC0
0048D33B  movss    dword ptr [rip + 0x1bd796d], xmm2  ; -> 02064CB0
0048D343  call     0x22cc20  ; -> 0022CC20 fn
0048D348  movzx    ecx, word ptr [rip + 0x1bd77bd]  ; -> 02064B0C
0048D34F  movss    xmm2, dword ptr [rip + 0x1bd7959]  ; -> 02064CB0
0048D357  movzx    edx, word ptr [rip + 0x1bd7a6a]  ; -> 02064DC8
0048D35E  cmp      word ptr [rip + 0x1bd7a67], cx  ; -> 02064DCC
0048D365  je       0x48d420  ; -> 0048D420
0048D36B  cvttss2si eax, xmm2
0048D36F  lea      r9, [rip + 0x1bd7aba]  ; -> 02064E30
0048D376  mov      dword ptr [rip + 0x1bd7934], eax  ; -> 02064CB0
0048D37C  movss    xmm0, dword ptr [rip + 0x1bd792c]  ; -> 02064CB0
0048D384  movss    dword ptr [rsp + 0x50], xmm0
0048D38A  movzx    r8d, word ptr [rsp + 0x50]
0048D390  movsx    eax, dx
0048D393  inc      dx
0048D396  shl      eax, 4
0048D399  movsxd   rcx, eax
0048D39C  movzx    eax, word ptr [rcx + r9 + 4]
0048D3A2  sub      r8w, ax
0048D3A6  mov      word ptr [rip + 0x1bd7a23], ax  ; -> 02064DD0
0048D3AD  jns      0x48d390  ; -> 0048D390
0048D3AF  dec      dx
0048D3B2  mov      word ptr [rip + 0x1bd7a1a], r8w  ; -> 02064DD4
0048D3BA  movsx    eax, dx
0048D3BD  shl      eax, 4
0048D3C0  movsxd   rcx, eax
0048D3C3  mov      word ptr [rip + 0x1bd79fe], dx  ; -> 02064DC8
0048D3CA  movzx    eax, word ptr [rcx + r9]
0048D3CF  jmp      0x48d495  ; -> 0048D495
0048D3D4  movzx    eax, word ptr [rip + 0x1bd79f1]  ; -> 02064DCC
0048D3DB  cmp      ax, cx
0048D3DE  jne      0x48d3fb  ; -> 0048D3FB
0048D3E0  movaps   xmm6, xmmword ptr [rsp + 0x30]
0048D3E5  dec      r8w
0048D3E9  movaps   xmm7, xmmword ptr [rsp + 0x20]
0048D3EE  mov      word ptr [rip + 0x1bd79d6], r8w  ; -> 02064DCC
0048D3F6  add      rsp, 0x48
0048D3FA  ret      
0048D3FB  cwde     
0048D3FC  lea      r9, [rip + 0x1bd7a2d]  ; -> 02064E30
0048D403  dec      ax
0048D406  add      dx, ax
0048D409  movsx    eax, dx
0048D40C  shl      eax, 4
0048D40F  movsxd   rcx, eax
0048D412  mov      word ptr [rip + 0x1bd79af], dx  ; -> 02064DC8
0048D419  movzx    eax, word ptr [rcx + r9]
0048D41E  jmp      0x48d495  ; -> 0048D495
0048D420  movss    xmm0, dword ptr [rip + 0x1bd7890]  ; -> 02064CB8
0048D428  ucomiss  xmm0, xmm7
0048D42B  jp       0x48d42f  ; -> 0048D42F
0048D42D  je       0x48d436  ; -> 0048D436
0048D42F  movaps   xmm6, xmm2
0048D432  divss    xmm6, xmm0
0048D436  movss    xmm0, dword ptr [rip + 0x19753f6]  ; -> 01E02834 [u32 0x00000000]
0048D43E  addss    xmm0, xmm6
0048D442  movss    dword ptr [rip + 0x1bd76b6], xmm6  ; -> 02064B00
0048D44A  ucomiss  xmm0, xmm7
0048D44D  movss    dword ptr [rip + 0x1bd785f], xmm0  ; -> 02064CB4
0048D455  jp       0x48d466  ; -> 0048D466
0048D457  jne      0x48d466  ; -> 0048D466
0048D459  call     0x22cc40  ; -> 0022CC40 fn
0048D45E  movss    xmm0, dword ptr [rip + 0x1bd784e]  ; -> 02064CB4
0048D466  comiss   xmm7, xmm0
0048D469  jbe      0x48d478  ; -> 0048D478
0048D46B  call     0x22cc30  ; -> 0022CC30 fn
0048D470  movss    xmm0, dword ptr [rip + 0x1bd783c]  ; -> 02064CB4
0048D478  cvttss2si eax, xmm0
0048D47C  mov      dword ptr [rip + 0x1bd7832], eax  ; -> 02064CB4
0048D482  movss    xmm0, dword ptr [rip + 0x1bd782a]  ; -> 02064CB4
0048D48A  movss    dword ptr [rsp + 0x50], xmm0
0048D490  movzx    eax, word ptr [rsp + 0x50]
0048D495  movaps   xmm6, xmmword ptr [rsp + 0x30]
0048D49A  movaps   xmm7, xmmword ptr [rsp + 0x20]
0048D49F  mov      word ptr [rip + 0x1bd7926], ax  ; -> 02064DCC
0048D4A6  add      rsp, 0x48
0048D4AA  ret      
```

## 0048F790 (291 B, extent 0048F790-0048F8B3)

Entered from (direct sites whose caller this page cites): `0047C360` + 0x55C (call; `0047C360` is cited on this page); `00482860` + 0xDC3 (call; `00482860` is cited on this page); `00482860` + 0x1126 (call; `00482860` is cited on this page); `00482860` + 0x11A8 (call; `00482860` is cited on this page); `00485790` + 0xD6F (call; `00485790` is cited on this page); `00485790` + 0xEE8 (call; `00485790` is cited on this page); `00488340` + 0x75 (call; `00488340` is cited on this page); `00488340` + 0xB9 (call; `00488340` is cited on this page); `0048AF70` + 0xB63 (call; `0048AF70` is cited on this page); `0048F8C0` + 0xA37 (call; `0048F8C0` is cited on this page); `0048F8C0` + 0xB87 (call; `0048F8C0` is cited on this page); `0048F8C0` + 0x159C (call; `0048F8C0` is cited on this page); `004930A0` + 0xA47 (call; `004930A0` is cited on this page); `004930A0` + 0xB14 (call; `004930A0` is cited on this page)
Other direct sites: `004B1190` + 0x37EF (call); `004B1190` + 0x4E2D (call)

Host context: "| Gouraud LINE '0x049' + POINT '0x040' | line bundles with points | 875 / 334; 617 / 156; 80 / 47; 115 / 87; 175 / 51 | | '0x84', '0x88', '0x89', '0x8B', '0x96' | '0048AF70', '0048F8C0', '00482860', '0047C360', '0048D4B0' | flat textured quad strip '0x054' | textured quads placed by the world matrix | 1,972 / 443; 41 / 31; 36 / 8; 1 / 1; 268 / 65 | | '0x85' | '00488340' | textured strip '0x05C' | a ribbon along the 32-sample path | 78 /" / " '004C2160' | Gouraud LINE '0x049' + POINT '0x040' | line bundles with points | 875 / 334; 617 / 156; 80 / 47; 115 / 87; 175 / 51 | | '0x84', '0x88', '0x89', '0x8B', '0x96' | '0048AF70', '0048F8C0', '00482860', '0047C360', '0048D4B0' | flat textured quad strip '0x054' | textured quads placed by the world matrix | 1,972 / 443; 41 / 31; 36 / 8; 1 / 1; 268 / 65 | | '0x85' | '00488340' | textured strip '0x05C' | a ribbon along the 32-sample"

```
0048F790  movss    xmm2, dword ptr [rip + 0x1bd5518]  ; -> 02064CB0
0048F798  xor      ecx, ecx
0048F79A  movzx    r10d, word ptr [rip + 0x1bd536a]  ; -> 02064B0C
0048F7A2  mov      eax, ecx
0048F7A4  mov      dword ptr [rip + 0x1bd5356], 0x40c90fdb  ; -> 02064B04
0048F7AE  mov      edx, ecx
0048F7B0  movss    xmm0, dword ptr [rip + 0x1bd534c]  ; -> 02064B04
0048F7B8  mov      r11d, 0x80
0048F7BE  comiss   xmm0, xmm2
0048F7C1  mov      dword ptr [rip + 0x1bd5339], 0x40c90fdb  ; -> 02064B04
0048F7CB  lea      r8d, [r11 + r10]
0048F7CF  mov      word ptr [rip + 0x1bd55f9], r8w  ; -> 02064DD0
0048F7D7  movaps   xmm0, xmm2
0048F7DA  mulss    xmm0, dword ptr [rip + 0x892dae]  ; -> 00D22590 [f32 0.1591549]
0048F7E2  seta     al
0048F7E5  shl      ax, 7
0048F7E9  and      ax, r8w
0048F7ED  comiss   xmm2, dword ptr [rip + 0x197303c]  ; -> 01E02830 [u32 0x00000000]
0048F7F4  mov      word ptr [rip + 0x1bd55cd], ax  ; -> 02064DC8
0048F7FB  cvttss2si r9d, xmm0
0048F800  seta     dl
0048F803  shl      dx, 7
0048F807  and      dx, r8w
0048F80B  mov      word ptr [rip + 0x1bd55ba], dx  ; -> 02064DCC
0048F812  mov      dword ptr [rip + 0x1bd54a7], r9d  ; -> 02064CC0
0048F819  cmp      ax, r10w
0048F81D  jne      0x48f852  ; -> 0048F852
0048F81F  movd     xmm0, r9d
0048F824  cvtdq2ps xmm0, xmm0
0048F827  mov      dword ptr [rip + 0x1bd52d3], 0x40c90fdb  ; -> 02064B04
0048F831  mulss    xmm0, dword ptr [rip + 0x1bd52cb]  ; -> 02064B04
0048F839  subss    xmm2, xmm0
0048F83D  movss    dword ptr [rip + 0x1bd547b], xmm0  ; -> 02064CC0
0048F845  movss    dword ptr [rip + 0x1bd5463], xmm2  ; -> 02064CB0
0048F84D  jmp      0x22cc20  ; -> 0022CC20 fn
0048F852  cmp      dx, r10w
0048F856  jne      0x48f8b2  ; -> 0048F8B2
0048F858  movss    xmm1, dword ptr [rip + 0x1bd52a4]  ; -> 02064B04
0048F860  xorps    xmm0, xmm0
0048F863  addss    xmm1, xmm2
0048F867  mov      dword ptr [rip + 0x1bd5293], 0x40c90fdb  ; -> 02064B04
0048F871  comiss   xmm0, xmm1
0048F874  movd     xmm0, r9d
0048F879  cvtdq2ps xmm0, xmm0
0048F87C  cmova    cx, r11w
0048F881  and      cx, r8w
0048F885  mov      word ptr [rip + 0x1bd553c], cx  ; -> 02064DC8
0048F88C  subss    xmm0, dword ptr [rip + 0x1972fa8]  ; -> 01E0283C [f32 1]
0048F894  movss    dword ptr [rip + 0x1bd5424], xmm0  ; -> 02064CC0
0048F89C  cmp      cx, r8w
0048F8A0  je       0x48f831  ; -> 0048F831
0048F8A2  addss    xmm2, dword ptr [rip + 0x1bd525a]  ; -> 02064B04
0048F8AA  movss    dword ptr [rip + 0x1bd53fe], xmm2  ; -> 02064CB0
0048F8B2  ret      
```

## 004AD9E0 (813 B, extent 004AD9E0-004ADD0D)

Entered from (direct sites whose caller this page cites): `004ADD10` + 0xA02 (call; `004ADD10` is cited on this page); `004ADD10` + 0xAF6 (call; `004ADD10` is cited on this page); `004ADD10` + 0x1317 (call; `004ADD10` is cited on this page); `004ADD10` + 0x141F (call; `004ADD10` is cited on this page); `004ADD10` + 0x17F6 (call; `004ADD10` is cited on this page); `004ADD10` + 0x18E2 (call; `004ADD10` is cited on this page); `004ADD10` + 0x1CB9 (call; `004ADD10` is cited on this page); `004ADD10` + 0x1DC8 (call; `004ADD10` is cited on this page)
Other direct sites: none

Host context: "ebuilt strip resource, randomly mirrored | '0x8C' 7,509 / 889; '0x8D' 1,170 / 503; '0x8E' 136 / 74; '0x8F' 1,663 / 376; '0x90' 765 / 307; '0x91' 12 / 7; '0x92' 84 / 45; '0x95' 456 / 216 | | '0x94' | '004ADD10' | triangle fan '0x05D' | a textured fan | 2,344 / 357 | | '0x81', '0x8A', '0x97' | raw GS packets | - | **nothing on PC** (UQ-204), and **no shipped effect authors them** | 0 |  ## Cross-subsystem neighbours — FINAL-AUDIT pass 22 " / "ebuilt strip resource, randomly mirrored | '0x8C' 7,509 / 889; '0x8D' 1,170 / 503; '0x8E' 136 / 74; '0x8F' 1,663 / 376; '0x90' 765 / 307; '0x91' 12 / 7; '0x92' 84 / 45; '0x95' 456 / 216 | | '0x94' | '004ADD10' | triangle fan '0x05D' | a textured fan | 2,344 / 357 | | '0x81', '0x8A', '0x97' | raw GS packets | - | **nothing on PC** (UQ-204), and **no shipped effect authors them** | 0 |  ## Cross-subsystem neighbours — FINAL-AUDIT pass 22 "

```
004AD9E0  mov      rax, rsp
004AD9E3  mov      qword ptr [rax + 8], rbx
004AD9E7  mov      qword ptr [rax + 0x10], rbp
004AD9EB  mov      qword ptr [rax + 0x18], rsi
004AD9EF  push     rdi
004AD9F0  push     r12
004AD9F2  push     r13
004AD9F4  push     r14
004AD9F6  push     r15
004AD9F8  sub      rsp, 0x60
004AD9FC  lea      rdi, [r8 + 0x140]
004ADA03  movaps   xmmword ptr [rax - 0x38], xmm6
004ADA07  movaps   xmmword ptr [rax - 0x48], xmm7
004ADA0B  lea      rsi, [r8 + 0x180]
004ADA12  movaps   xmmword ptr [rax - 0x58], xmm8
004ADA17  mov      rbx, r8
004ADA1A  movaps   xmmword ptr [rax - 0x68], xmm9
004ADA1F  mov      r8, rdi
004ADA22  movsx    eax, word ptr [r9]
004ADA26  mov      rdx, rsi
004ADA29  add      eax, 0x13
004ADA2C  mov      r15, r9
004ADA2F  shl      eax, 4
004ADA32  xorps    xmm6, xmm6
004ADA35  movsxd   rcx, eax
004ADA38  lea      rax, [rip + 0x1bb73f1]  ; -> 02064E30
004ADA3F  movups   xmm0, xmmword ptr [rcx + rax]
004ADA43  movups   xmmword ptr [rdi], xmm0
004ADA46  movups   xmm1, xmmword ptr [rcx + rax + 0x10]
004ADA4B  movups   xmmword ptr [rdi + 0x10], xmm1
004ADA4F  movups   xmm0, xmmword ptr [rcx + rax + 0x20]
004ADA54  movups   xmmword ptr [rdi + 0x20], xmm0
004ADA58  movups   xmm1, xmmword ptr [rcx + rax + 0x30]
004ADA5D  movups   xmmword ptr [rdi + 0x30], xmm1
004ADA61  movups   xmm0, xmmword ptr [rcx + rax + 0x40]
004ADA66  movups   xmmword ptr [rdi + 0x40], xmm0
004ADA6A  movups   xmm1, xmmword ptr [rcx + rax + 0x50]
004ADA6F  movups   xmmword ptr [rdi + 0x50], xmm1
004ADA73  movups   xmm0, xmmword ptr [rcx + rax + 0x60]
004ADA78  movups   xmmword ptr [rdi + 0x60], xmm0
004ADA7C  movups   xmm1, xmmword ptr [rcx + rax + 0x70]
004ADA81  mov      rcx, rsi
004ADA84  movups   xmmword ptr [rdi + 0x70], xmm1
004ADA88  call     0x203080  ; -> 00203080 fn
004ADA8D  lea      rbp, [rbx + 0x190]
004ADA94  mov      rdx, rbp
004ADA97  lea      r8, [rbx + 0x150]
004ADA9E  mov      rcx, rbp
004ADAA1  call     0x203080  ; -> 00203080 fn
004ADAA6  lea      r14, [rbx + 0x1a0]
004ADAAD  mov      rdx, r14
004ADAB0  lea      r8, [rbx + 0x160]
004ADAB7  mov      rcx, r14
004ADABA  call     0x203080  ; -> 00203080 fn
004ADABF  mov      eax, dword ptr [rsp + 0xb0]
004ADAC6  cmp      eax, 2
004ADAC9  ja       0x4adaf9  ; -> 004ADAF9
004ADACB  movss    xmm0, dword ptr [rbx + 0x17c]
004ADAD3  xorps    xmm0, xmmword ptr [rip + 0x183e2c6]  ; -> 01CEBDA0 [f32x4 -0, -0, -0, -0]
004ADADA  movss    dword ptr [rbx + 0x17c], xmm0
004ADAE2  movss    xmm0, dword ptr [rbx + 0x1bc]
004ADAEA  xorps    xmm0, xmmword ptr [rip + 0x183e2af]  ; -> 01CEBDA0 [f32x4 -0, -0, -0, -0]
004ADAF1  movss    dword ptr [rbx + 0x1bc], xmm0
004ADAF9  movsd    xmm9, qword ptr [rip + 0x183e27e]  ; -> 01CEBD80 [u64 0x7FFFFFFFFFFFFFFF]
004ADB02  movss    xmm2, dword ptr [rbx + 0x17c]
004ADB0A  movss    xmm3, dword ptr [rbx + 0x1bc]
004ADB12  movss    xmm0, dword ptr [rbx + 0x170]
004ADB1A  subss    xmm0, xmm2
004ADB1E  cvtps2pd xmm1, xmm0
004ADB21  movss    xmm0, dword ptr [rbx + 0x174]
004ADB29  subss    xmm0, xmm2
004ADB2D  andps    xmm1, xmm9
004ADB31  cvtpd2ps xmm5, xmm1
004ADB35  cvtps2pd xmm1, xmm0
004ADB38  movss    xmm0, dword ptr [rbx + 0x178]
004ADB40  movss    dword ptr [rbx + 0x170], xmm5
004ADB48  subss    xmm0, xmm2
004ADB4C  andps    xmm1, xmm9
004ADB50  cvtpd2ps xmm7, xmm1
004ADB54  cvtps2pd xmm1, xmm0
004ADB57  movss    dword ptr [rbx + 0x174], xmm7
004ADB5F  andps    xmm1, xmm9
004ADB63  cvtpd2ps xmm8, xmm1
004ADB68  cvtps2pd xmm0, xmm2
004ADB6B  movss    xmm2, dword ptr [rbx + 0x1b0]
004ADB73  movss    dword ptr [rbx + 0x178], xmm8
004ADB7C  andps    xmm0, xmm9
004ADB80  subss    xmm2, xmm3
004ADB84  cvtpd2ps xmm0, xmm0
004ADB88  cvtps2pd xmm1, xmm3
004ADB8B  movss    dword ptr [rbx + 0x17c], xmm0
004ADB93  andps    xmm1, xmm9
004ADB97  cvtpd2ps xmm0, xmm1
004ADB9B  movss    dword ptr [rbx + 0x1bc], xmm0
004ADBA3  cvtps2pd xmm0, xmm2
004ADBA6  andps    xmm0, xmm9
004ADBAA  cvtpd2ps xmm4, xmm0
004ADBAE  movss    xmm0, dword ptr [rbx + 0x1b4]
004ADBB6  subss    xmm0, xmm3
004ADBBA  addss    xmm4, xmm5
004ADBBE  cvtps2pd xmm1, xmm0
004ADBC1  movss    xmm0, dword ptr [rbx + 0x1b8]
004ADBC9  movss    dword ptr [rbx + 0x1b0], xmm4
004ADBD1  subss    xmm0, xmm3
004ADBD5  andps    xmm1, xmm9
004ADBD9  cvtpd2ps xmm2, xmm1
004ADBDD  cvtps2pd xmm1, xmm0
004ADBE0  addss    xmm2, xmm7
004ADBE4  andps    xmm1, xmm9
004ADBE8  cvtpd2ps xmm3, xmm1
004ADBEC  movss    dword ptr [rbx + 0x1b4], xmm2
004ADBF4  addss    xmm3, xmm8
004ADBF9  movss    dword ptr [rbx + 0x1b8], xmm3
004ADC01  test     eax, eax
004ADC03  je       0x4adc31  ; -> 004ADC31
004ADC05  cmp      eax, 3
004ADC08  je       0x4adc31  ; -> 004ADC31
004ADC0A  cmp      eax, 1
004ADC0D  je       0x4adc28  ; -> 004ADC28
004ADC0F  cmp      eax, 4
004ADC12  je       0x4adc28  ; -> 004ADC28
004ADC14  cmp      eax, 2
004ADC17  je       0x4adc1e  ; -> 004ADC1E
004ADC19  cmp      eax, 5
004ADC1C  jne      0x4adc38  ; -> 004ADC38
004ADC1E  movaps   xmm6, xmm8
004ADC22  divss    xmm6, xmm3
004ADC26  jmp      0x4adc38  ; -> 004ADC38
004ADC28  movaps   xmm6, xmm7
004ADC2B  divss    xmm6, xmm2
004ADC2F  jmp      0x4adc38  ; -> 004ADC38
004ADC31  movaps   xmm6, xmm5
004ADC34  divss    xmm6, xmm4
004ADC38  cvtps2pd xmm0, xmm6
004ADC3B  mov      rdx, rsi
004ADC3E  mov      rcx, rsi
004ADC41  andps    xmm0, xmm9
004ADC45  cvtpd2ps xmm2, xmm0
004ADC49  movss    dword ptr [rbx + 0x1bc], xmm2
004ADC51  call     0x202fe0  ; -> 00202FE0 fn
004ADC56  movss    xmm2, dword ptr [rbx + 0x1bc]
004ADC5E  mov      rdx, rbp
004ADC61  mov      rcx, rbp
004ADC64  call     0x202fe0  ; -> 00202FE0 fn
004ADC69  movss    xmm2, dword ptr [rbx + 0x1bc]
004ADC71  mov      rdx, r14
004ADC74  mov      rcx, r14
004ADC77  call     0x202fe0  ; -> 00202FE0 fn
004ADC7C  mov      r8, rdi
004ADC7F  mov      rdx, rsi
004ADC82  mov      rcx, rsi
004ADC85  call     0x202b10  ; -> 00202B10 fn
004ADC8A  lea      r8, [rbx + 0x150]
004ADC91  mov      rdx, rbp
004ADC94  mov      rcx, rbp
004ADC97  call     0x202b10  ; -> 00202B10 fn
004ADC9C  lea      r8, [rbx + 0x160]
004ADCA3  mov      rdx, r14
004ADCA6  mov      rcx, r14
004ADCA9  call     0x202b10  ; -> 00202B10 fn
004ADCAE  movsx    eax, word ptr [r15]
004ADCB2  lea      r11, [rsp + 0x60]
004ADCB7  movups   xmm0, xmmword ptr [rsi]
004ADCBA  mov      rbx, qword ptr [r11 + 0x30]
004ADCBE  add      eax, 0x13
004ADCC1  mov      rbp, qword ptr [r11 + 0x38]
004ADCC5  movaps   xmm6, xmmword ptr [rsp + 0x50]
004ADCCA  movaps   xmm7, xmmword ptr [rsp + 0x40]
004ADCCF  movaps   xmm8, xmmword ptr [r11 - 0x30]
004ADCD4  movaps   xmm9, xmmword ptr [r11 - 0x40]
004ADCD9  shl      eax, 4
004ADCDC  movsxd   rcx, eax
004ADCDF  lea      rax, [rip + 0x1bb714a]  ; -> 02064E30
004ADCE6  movups   xmmword ptr [rcx + rax], xmm0
004ADCEA  movups   xmm1, xmmword ptr [rsi + 0x10]
004ADCEE  movups   xmmword ptr [rcx + rax + 0x10], xmm1
004ADCF3  movups   xmm0, xmmword ptr [rsi + 0x20]
004ADCF7  mov      rsi, qword ptr [r11 + 0x40]
004ADCFB  movups   xmmword ptr [rcx + rax + 0x20], xmm0
004ADD00  mov      rsp, r11
004ADD03  pop      r15
004ADD05  pop      r14
004ADD07  pop      r13
004ADD09  pop      r12
004ADD0B  pop      rdi
004ADD0C  ret      
```
