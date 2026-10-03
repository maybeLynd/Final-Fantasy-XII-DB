# Homing pack: `16-UI/Shared-Dialogs/the-shared-dialog-widgets.md`

Generated 2026-10-03 15:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h14-the-shared-dialog-widgets.json`.

Bodies: 4. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00240680 (112 B, extent 00240680-002406F0)

Entered from (direct sites whose caller this page cites): `00281ED0` + 0x2AD (call; `00281ED0` is cited on this page)
Other direct sites: none

Host context: "281AE0' (→'00280DE0', the menu-list proc) | 'mCommandMenuOffsetY', 'mCommandMenuStrHeight' | 'OffsetY' → 'r8d' position arg ('00281D23'); 'StrHeight' → 'eax' + 'movss 1.0' row pitch ('00281CCD') | | '00281ED0' (→'00280DE0') | 'ConfigBlackBandH', 'PartyBlackBandGradH', 'BlackBandAnimTime' | the menu list's band: 'ecx'/'edx'/'r8d' → '002C9490' ('002821CA'/'002821C4'/'002821BD') | | '0028D460' (→'0028C970') | 'm2DSideCursorCenterX', 'm2DSi"

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

Host context: "281AE0' (→'00280DE0', the menu-list proc) | 'mCommandMenuOffsetY', 'mCommandMenuStrHeight' | 'OffsetY' → 'r8d' position arg ('00281D23'); 'StrHeight' → 'eax' + 'movss 1.0' row pitch ('00281CCD') | | '00281ED0' (→'00280DE0') | 'ConfigBlackBandH', 'PartyBlackBandGradH', 'BlackBandAnimTime' | the menu list's band: 'ecx'/'edx'/'r8d' → '002C9490' ('002821CA'/'002821C4'/'002821BD') | | '0028D460' (→'0028C970') | 'm2DSideCursorCenterX', 'm2DSi"

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

Host context: "281AE0' (→'00280DE0', the menu-list proc) | 'mCommandMenuOffsetY', 'mCommandMenuStrHeight' | 'OffsetY' → 'r8d' position arg ('00281D23'); 'StrHeight' → 'eax' + 'movss 1.0' row pitch ('00281CCD') | | '00281ED0' (→'00280DE0') | 'ConfigBlackBandH', 'PartyBlackBandGradH', 'BlackBandAnimTime' | the menu list's band: 'ecx'/'edx'/'r8d' → '002C9490' ('002821CA'/'002821C4'/'002821BD') | | '0028D460' (→'0028C970') | 'm2DSideCursorCenterX', 'm2DSi"

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

## 00292090 (33 B, extent 00292090-002920B1)

Entered from (direct sites whose caller this page cites): `00281ED0` + 0x496 (call; `00281ED0` is cited on this page)
Other direct sites: none

Host context: "281AE0' (→'00280DE0', the menu-list proc) | 'mCommandMenuOffsetY', 'mCommandMenuStrHeight' | 'OffsetY' → 'r8d' position arg ('00281D23'); 'StrHeight' → 'eax' + 'movss 1.0' row pitch ('00281CCD') | | '00281ED0' (→'00280DE0') | 'ConfigBlackBandH', 'PartyBlackBandGradH', 'BlackBandAnimTime' | the menu list's band: 'ecx'/'edx'/'r8d' → '002C9490' ('002821CA'/'002821C4'/'002821BD') | | '0028D460' (→'0028C970') | 'm2DSideCursorCenterX', 'm2DSi"

```
00292090  mov      rax, qword ptr [rip + 0x1e08b99]  ; -> 0209AC30
00292097  mov      rcx, qword ptr [rax + 0x300]
0029209E  test     rcx, rcx
002920A1  je       0x2920ae  ; -> 002920AE
002920A3  movzx    eax, word ptr [rcx + 0x16a]
002920AA  and      eax, 0xf
002920AD  ret      
002920AE  xor      eax, eax
002920B0  ret      
```
