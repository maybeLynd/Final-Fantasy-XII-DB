# Homing pack: `16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-map-screens-and-their-shared-map-data.json`.

Bodies: 10. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00240680 (112 B, extent 00240680-002406F0)

Entered from (direct sites whose caller this page cites): `00281ED0` + 0x2AD (call; `00281ED0` is cited on this page)
Other direct sites: none

Host context: "E0' ('00281579', '002817CA', '00281844') | | '0028E790' | world map from the saved '0209BE80 +0x10FA2' / '+0x10FA6' / '+0x10FA8', after destroying the field-time container | '0027F5D0' ('0027FA2C'), '00281ED0' ('002823B8'), '002804E0' ('00280566') | | '002BA040' | location map setup. With '+0x179D2' bit 10 set, it copies 32 bytes at '+0x190' from the field-time container ('002BA095'–'002BA0B1'). Otherwise it destroys that container ('00"

```
00240680  sub      rsp, 0x48
00240684  mov      rax, qword ptr [rip + 0x1d041a5]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0024068B  xor      rax, rsp
0024068E  mov      qword ptr [rsp + 0x38], rax
00240693  call     0x265270  ; -> 00265270 fn
00240698  mov      dword ptr [rsp + 0x20], 0
002406A0  cmp      ax, 0x19
002406A4  jg       0x2406b0  ; -> 002406B0
002406A6  movdqa   xmm0, xmmword ptr [rip + 0x6d46c2]  ; -> 00914D70 [u32x4 0x00000002, 0x00000000, 0x000000FF, 0x00000000]
002406AE  jmp      0x2406b8  ; -> 002406B8
002406B0  movdqa   xmm0, xmmword ptr [rip + 0x6d46a8]  ; -> 00914D60 [u32x4 0x00000000, 0x00000000, 0x000000FF, 0x00000000]
002406B8  cmp      qword ptr [rip + 0x1e4e018], 0  ; -> 0208E6D8
002406C0  movdqu   xmmword ptr [rsp + 0x28], xmm0
002406C6  jne      0x2406de  ; -> 002406DE
002406C8  lea      r8, [rsp + 0x20]
002406CD  mov      ecx, 0x4d8
002406D2  lea      rdx, [rip - 0xaf9]  ; -> 0023FBE0
002406D9  call     0x244f50  ; -> 00244F50 fn
002406DE  mov      rcx, qword ptr [rsp + 0x38]
002406E3  xor      rcx, rsp
002406E6  call     0x808c40  ; -> 00808C40 fn
002406EB  add      rsp, 0x48
002406EF  ret      
```

## 00240D60 (127 B, extent 00240D60-00240DDF)

Entered from (direct sites whose caller this page cites): `00281ED0` + 0x2E8 (call; `00281ED0` is cited on this page)
Other direct sites: none

Host context: "E0' ('00281579', '002817CA', '00281844') | | '0028E790' | world map from the saved '0209BE80 +0x10FA2' / '+0x10FA6' / '+0x10FA8', after destroying the field-time container | '0027F5D0' ('0027FA2C'), '00281ED0' ('002823B8'), '002804E0' ('00280566') | | '002BA040' | location map setup. With '+0x179D2' bit 10 set, it copies 32 bytes at '+0x190' from the field-time container ('002BA095'–'002BA0B1'). Otherwise it destroys that container ('00"

```
00240D60  sub      rsp, 0x48
00240D64  mov      rax, qword ptr [rip + 0x1d03ac5]  ; -> 01F44830 [u64 0x00002B992DDFA232]
00240D6B  xor      rax, rsp
00240D6E  mov      qword ptr [rsp + 0x38], rax
00240D73  cmp      qword ptr [rip + 0x1e4d94d], 0  ; -> 0208E6C8
00240D7B  xorps    xmm0, xmm0
00240D7E  movdqu   xmmword ptr [rsp + 0x28], xmm0
00240D84  mov      dword ptr [rsp + 0x20], 0
00240D8C  jne      0x240dcd  ; -> 00240DCD
00240D8E  lea      r8, [rsp + 0x20]
00240D93  mov      ecx, 0xc8
00240D98  lea      rdx, [rip - 0x2cf]  ; -> 00240AD0
00240D9F  call     0x244f50  ; -> 00244F50 fn
00240DA4  lea      rdx, [rip + 0x6d3ec5]  ; -> 00914C70
00240DAB  mov      qword ptr [rip + 0x1e4d916], rax  ; -> 0208E6C8
00240DB2  mov      rcx, rax
00240DB5  call     0x247570  ; -> 00247570 fn
00240DBA  mov      rdx, qword ptr [rip + 0x1e4d907]  ; -> 0208E6C8
00240DC1  mov      rcx, qword ptr [rip + 0x1e4dc60]  ; -> 0208EA28
00240DC8  call     0x246ad0  ; -> 00246AD0 fn
00240DCD  mov      rcx, qword ptr [rsp + 0x38]
00240DD2  xor      rcx, rsp
00240DD5  call     0x808c40  ; -> 00808C40 fn
00240DDA  add      rsp, 0x48
00240DDE  ret      
```

## 0027EBC0 (120 B, extent 0027EBC0-0027EC38)

Entered from (direct sites whose caller this page cites): `00281ED0` + 0x2C6 (call; `00281ED0` is cited on this page)
Other direct sites: none

Host context: "E0' ('00281579', '002817CA', '00281844') | | '0028E790' | world map from the saved '0209BE80 +0x10FA2' / '+0x10FA6' / '+0x10FA8', after destroying the field-time container | '0027F5D0' ('0027FA2C'), '00281ED0' ('002823B8'), '002804E0' ('00280566') | | '002BA040' | location map setup. With '+0x179D2' bit 10 set, it copies 32 bytes at '+0x190' from the field-time container ('002BA095'–'002BA0B1'). Otherwise it destroys that container ('00"

```
0027EBC0  sub      rsp, 0x48
0027EBC4  mov      rax, qword ptr [rip + 0x1cc5c65]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0027EBCB  xor      rax, rsp
0027EBCE  mov      qword ptr [rsp + 0x38], rax
0027EBD3  cmp      qword ptr [rip + 0x1e1c045], 0  ; -> 0209AC20
0027EBDB  xorps    xmm0, xmm0
0027EBDE  movdqu   xmmword ptr [rsp + 0x28], xmm0
0027EBE4  mov      dword ptr [rsp + 0x20], 0
0027EBEC  jne      0x27ec26  ; -> 0027EC26
0027EBEE  lea      r8, [rsp + 0x20]
0027EBF3  mov      ecx, 0xc0
0027EBF8  lea      rdx, [rip - 0x18f]  ; -> 0027EA70
0027EBFF  call     0x244f50  ; -> 00244F50 fn
0027EC04  lea      rdx, [rip + 0x69707d]  ; -> 00915C88
0027EC0B  mov      qword ptr [rip + 0x1e1c00e], rax  ; -> 0209AC20
0027EC12  mov      rcx, rax
0027EC15  call     0x247570  ; -> 00247570 fn
0027EC1A  mov      rcx, qword ptr [rip + 0x1e1bfff]  ; -> 0209AC20
0027EC21  call     0x246ac0  ; -> 00246AC0 fn
0027EC26  mov      rcx, qword ptr [rsp + 0x38]
0027EC2B  xor      rcx, rsp
0027EC2E  call     0x808c40  ; -> 00808C40 fn
0027EC33  add      rsp, 0x48
0027EC37  ret      
```

## 00281A10 (63 B, extent 00281A10-00281A4F)

Entered from (direct sites whose caller this page cites): `002814E0` + 0x13C (call; `002814E0` is cited on this page); `002814E0` + 0x1F3 (jmp; `002814E0` is cited on this page); `002814E0` + 0x237 (call; `002814E0` is cited on this page); `002814E0` + 0x28D (jmp; `002814E0` is cited on this page); `002814E0` + 0x2B6 (jmp; `002814E0` is cited on this page); `002814E0` + 0x3FA (call; `002814E0` is cited on this page)
Other direct sites: none

Host context: "0550400(1, +0x10FA6)', '00550510(+0x10F68 bit 12)', '00550540' with a record '{req.u16[2] & 0x7FFF, 1 \| (req.u16[2] bit 15 → 2), req.s16[4]}', '00550610' ('0028E6EA'–'0028E770') | the close request '002814E0' ('00281579', '002817CA', '00281844') | | '0028E790' | world map from the saved '0209BE80 +0x10FA2' / '+0x10FA6' / '+0x10FA8', after destroying the field-time container | '0027F5D0' ('0027FA2C'), '00281ED0' ('002823B8'), '002804E0'" / "0550400(1, +0x10FA6)', '00550510(+0x10F68 bit 12)', '00550540' with a record '{req.u16[2] & 0x7FFF, 1 \| (req.u16[2] bit 15 → 2), req.s16[4]}', '00550610' ('0028E6EA'–'0028E770') | the close request '002814E0' ('00281579', '002817CA', '00281844') | | '0028E790' | world map from the saved '0209BE80 +0x10FA2' / '+0x10FA6' / '+0x10FA8', after destroying the field-time container | '0027F5D0' ('0027FA2C'), '00281ED0' ('002823B8'), '002804E0'"

```
00281A10  sub      rsp, 0x28
00281A14  xor      ecx, ecx
00281A16  call     0x2cf8b0  ; -> 002CF8B0 fn
00281A1B  xor      ecx, ecx
00281A1D  call     0x2ce7a0  ; -> 002CE7A0 fn
00281A22  call     0x2cf710  ; -> 002CF710 fn
00281A27  mov      rax, qword ptr [rip + 0x1e19202]  ; -> 0209AC30
00281A2E  mov      rdx, qword ptr [rax + 0xd8]
00281A35  test     rdx, rdx
00281A38  je       0x281a4a  ; -> 00281A4A
00281A3A  mov      rcx, qword ptr [rip + 0x1e0cfe7]  ; -> 0208EA28
00281A41  add      rsp, 0x28
00281A45  jmp      0x246ad0  ; -> 00246AD0 fn
00281A4A  add      rsp, 0x28
00281A4E  ret      
```

## 0028F710 (38 B, extent 0028F710-0028F736)

Entered from (direct sites whose caller this page cites): `002814E0` + 0x7D (call; `002814E0` is cited on this page); `002814E0` + 0x34C (call; `002814E0` is cited on this page)
Other direct sites: none

Host context: "0550400(1, +0x10FA6)', '00550510(+0x10F68 bit 12)', '00550540' with a record '{req.u16[2] & 0x7FFF, 1 \| (req.u16[2] bit 15 → 2), req.s16[4]}', '00550610' ('0028E6EA'–'0028E770') | the close request '002814E0' ('00281579', '002817CA', '00281844') | | '0028E790' | world map from the saved '0209BE80 +0x10FA2' / '+0x10FA6' / '+0x10FA8', after destroying the field-time container | '0027F5D0' ('0027FA2C'), '00281ED0' ('002823B8'), '002804E0'" / "0550400(1, +0x10FA6)', '00550510(+0x10F68 bit 12)', '00550540' with a record '{req.u16[2] & 0x7FFF, 1 \| (req.u16[2] bit 15 → 2), req.s16[4]}', '00550610' ('0028E6EA'–'0028E770') | the close request '002814E0' ('00281579', '002817CA', '00281844') | | '0028E790' | world map from the saved '0209BE80 +0x10FA2' / '+0x10FA6' / '+0x10FA8', after destroying the field-time container | '0027F5D0' ('0027FA2C'), '00281ED0' ('002823B8'), '002804E0'"

```
0028F710  mov      rax, qword ptr [rip + 0x1e0c769]  ; -> 0209BE80
0028F717  test     rax, rax
0028F71A  jne      0x28f722  ; -> 0028F722
0028F71C  mov      eax, 1
0028F721  ret      
0028F722  movzx    ecx, byte ptr [rax + 0x10fa3]
0028F729  mov      eax, 1
0028F72E  test     cl, cl
0028F730  je       0x28f735  ; -> 0028F735
0028F732  movzx    eax, cl
0028F735  ret      
```

## 0028F850 (38 B, extent 0028F850-0028F876)

Entered from (direct sites whose caller this page cites): `002814E0` + 0x2BB (call; `002814E0` is cited on this page)
Other direct sites: none

Host context: "0550400(1, +0x10FA6)', '00550510(+0x10F68 bit 12)', '00550540' with a record '{req.u16[2] & 0x7FFF, 1 \| (req.u16[2] bit 15 → 2), req.s16[4]}', '00550610' ('0028E6EA'–'0028E770') | the close request '002814E0' ('00281579', '002817CA', '00281844') | | '0028E790' | world map from the saved '0209BE80 +0x10FA2' / '+0x10FA6' / '+0x10FA8', after destroying the field-time container | '0027F5D0' ('0027FA2C'), '00281ED0' ('002823B8'), '002804E0'"

```
0028F850  mov      rax, qword ptr [rip + 0x1e0c629]  ; -> 0209BE80
0028F857  test     rax, rax
0028F85A  jne      0x28f862  ; -> 0028F862
0028F85C  mov      eax, 1
0028F861  ret      
0028F862  movzx    ecx, byte ptr [rax + 0x10fa2]
0028F869  mov      eax, 1
0028F86E  test     cl, cl
0028F870  je       0x28f875  ; -> 0028F875
0028F872  movzx    eax, cl
0028F875  ret      
```

## 002920F0 (75 B, extent 002920F0-0029213B)

Entered from (direct sites whose caller this page cites): `002814E0` + 0x118 (call; `002814E0` is cited on this page); `002814E0` + 0x283 (call; `002814E0` is cited on this page); `002814E0` + 0x3D1 (call; `002814E0` is cited on this page)
Other direct sites: none

Host context: "0550400(1, +0x10FA6)', '00550510(+0x10F68 bit 12)', '00550540' with a record '{req.u16[2] & 0x7FFF, 1 \| (req.u16[2] bit 15 → 2), req.s16[4]}', '00550610' ('0028E6EA'–'0028E770') | the close request '002814E0' ('00281579', '002817CA', '00281844') | | '0028E790' | world map from the saved '0209BE80 +0x10FA2' / '+0x10FA6' / '+0x10FA8', after destroying the field-time container | '0027F5D0' ('0027FA2C'), '00281ED0' ('002823B8'), '002804E0'" / "0550400(1, +0x10FA6)', '00550510(+0x10F68 bit 12)', '00550540' with a record '{req.u16[2] & 0x7FFF, 1 \| (req.u16[2] bit 15 → 2), req.s16[4]}', '00550610' ('0028E6EA'–'0028E770') | the close request '002814E0' ('00281579', '002817CA', '00281844') | | '0028E790' | world map from the saved '0209BE80 +0x10FA2' / '+0x10FA6' / '+0x10FA8', after destroying the field-time container | '0027F5D0' ('0027FA2C'), '00281ED0' ('002823B8'), '002804E0'"

```
002920F0  mov      rax, qword ptr [rip + 0x1e08b39]  ; -> 0209AC30
002920F7  mov      rcx, qword ptr [rax + 0x300]
002920FE  test     rcx, rcx
00292101  je       0x29213a  ; -> 0029213A
00292103  and      dword ptr [rcx + 0x168], 0xfff5ffff
0029210D  or       dword ptr [rcx + 0x168], 0x50000
00292117  mov      rax, qword ptr [rip + 0x1e08b12]  ; -> 0209AC30
0029211E  mov      rcx, qword ptr [rax + 0x300]
00292125  mov      eax, dword ptr [rcx + 0x168]
0029212B  and      eax, 0xff1fffff
00292130  bts      eax, 0x14
00292134  mov      dword ptr [rcx + 0x168], eax
0029213A  ret      
```

## 00314AE0 (24 B, extent 00314AE0-00314AF8)

Entered from (direct sites whose caller this page cites): `00377750` + 0x4 (call; `00377750` is cited on this page)
Other direct sites: none

Host context: "3148F0' is called by the field bodies 'WorldField_InitializeCurrentFieldRuntimeParameters' '0026D910', 'WorldPersistence_ResetBanksForFieldTransition' '0026DB30', '0026DE00', '002FA520', '00377700', '00377750', '00377780', '00377BA0', '00377C20', '00377C70', '003C0450' and '00576A50'; '00264F90' and '00265270' by 'WorldTransition_StageFieldTransition' '003145E0', '003778B0', '003C0450', '0057FB00', '001EDCD0' and '003EAA70'; '002EFD20' "

```
00314AE0  sub      rsp, 0x28
00314AE4  call     0x2ef2b0  ; -> 002EF2B0 fn
00314AE9  movzx    eax, byte ptr [rax + 0x1063]
00314AF0  and      eax, 3
00314AF3  add      rsp, 0x28
00314AF7  ret      
```

## 003688A0 (59 B, extent 003688A0-003688DB)

Entered from (direct sites whose caller this page cites): `002D3BA0` + 0x6AB (call; `002D3BA0` is cited on this page)
Other direct sites: none

Host context: "0223DA0' and '00224C40' call the same '00225570'; the close request '002814E0' calls '002DEE50', which stores one audio-side state byte and tail-jumps into the audio layer; the list-input dispatcher '002D3BA0' and '002D2D40' call '00249CA0', which resolves a sound through the audio layer and plays it unless the resolve returns -1; and '00261F90' calls '003148F0'. The map pages play their cursor sounds through the audio layer, the close "

```
003688A0  test     byte ptr [rip + 0x1f6358b], 0x10  ; -> 022CBE32
003688A7  je       0x3688da  ; -> 003688DA
003688A9  cmp      ecx, -1
003688AC  mov      word ptr [rip + 0x1f6358c], 0x406  ; -> 022CBE41
003688B5  mov      eax, 2
003688BA  mov      byte ptr [rip + 0x1f63582], 0x1e  ; -> 022CBE43
003688C1  cmove    ecx, eax
003688C4  mov      byte ptr [rip + 0x1f63572], 1  ; -> 022CBE3D
003688CB  xor      eax, eax
003688CD  mov      byte ptr [rip + 0x1f6356d], cl  ; -> 022CBE40
003688D3  mov      word ptr [rip + 0x1f63564], ax  ; -> 022CBE3E
003688DA  ret      
```

## 00393190 (65 B, extent 00393190-003931D1)

Entered from (direct sites whose caller this page cites): `0057FB00` + 0x9C (call; `0057FB00` is cited on this page)
Other direct sites: `0057FA30` + 0x12 (call)

Host context: "77700', '00377750', '00377780', '00377BA0', '00377C20', '00377C70', '003C0450' and '00576A50'; '00264F90' and '00265270' by 'WorldTransition_StageFieldTransition' '003145E0', '003778B0', '003C0450', '0057FB00', '001EDCD0' and '003EAA70'; '002EFD20' by 'WorldTransition_RequestFieldTransition' '00314440'; the string lookup '0036A100' by '00267930', '003319D0' and 'AreaArd_LoadOrUnloadFieldResource' '003EA820'; and the members '001EC560', "

```
00393190  xor      r8d, r8d
00393193  mov      r10d, edx
00393196  test     dword ptr [rcx], 0x3fffc
0039319C  jbe      0x3931d0  ; -> 003931D0
0039319E  and      r10d, 1
003931A2  nop      dword ptr [rax]
003931A6  nop      word ptr [rax + rax]
003931B0  mov      rax, qword ptr [rcx + 0x10]
003931B4  mov      rdx, qword ptr [rax + r8*8]
003931B8  inc      r8d
003931BB  and      dword ptr [rdx + 8], 0xfffffffe
003931BF  or       dword ptr [rdx + 8], r10d
003931C3  mov      eax, dword ptr [rcx]
003931C5  shr      eax, 2
003931C8  movzx    eax, ax
003931CB  cmp      r8d, eax
003931CE  jb       0x3931b0  ; -> 003931B0
003931D0  ret      
```
