# Homing pack: `16-UI/Shared-Dialogs/the-shared-dialog-widgets.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-shared-dialog-widgets.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00270230 (45 B, extent 00270230-0027025D)

Entered from (direct sites whose caller this page cites): `0028D460` + 0x307 (call; `0028D460` is cited on this page)
Other direct sites: none

Host context: "00281CCD') | | '00281ED0' (→'00280DE0') | 'ConfigBlackBandH', 'PartyBlackBandGradH', 'BlackBandAnimTime' | the menu list's band: 'ecx'/'edx'/'r8d' → '002C9490' ('002821CA'/'002821C4'/'002821BD') | | '0028D460' (→'0028C970') | 'm2DSideCursorCenterX', 'm2DSideCursorCenterY' | 'neg ecx' then 'movd' — the side cursor's centre subtracted from the anchor point ('0028D6F5', '0028D718') | | '00292390' P (menu list, 'ListItem' keys) | 'ListItemI"

```
00270230  movaps   xmm0, xmm2
00270233  movaps   xmm1, xmm3
00270236  addss    xmm0, dword ptr [rdx]
0027023A  movss    dword ptr [rcx], xmm0
0027023E  addss    xmm1, dword ptr [rdx + 4]
00270243  movss    dword ptr [rcx + 4], xmm1
00270248  addss    xmm2, dword ptr [rdx + 8]
0027024D  movss    dword ptr [rcx + 8], xmm2
00270252  addss    xmm3, dword ptr [rdx + 0xc]
00270257  movss    dword ptr [rcx + 0xc], xmm3
0027025C  ret      
```

## 003FF9A0 (71 B, extent 003FF9A0-003FF9E7)

Entered from (direct sites whose caller this page cites): `002C2320` + 0x561 (call; `002C2320` is cited on this page)
Other direct sites: none

Host context: "ear and copy loops that write a W×H block into the icon texture — plus the atlas steps '01E0C478'/'01E0C47C' — not an icon-width argument and a height guard ('002925AA', '002925D0') | | '002C9BF0' (→'002C2320' geometry pass) | 'MenuListWindowHeightModifer' | 'add ecx, edx' — the height modifier added to the list window's base height ('002C9C6A') | | '002CD170' P (menu-list marks pane) | 'MenuListMarkOffsetX/Y', 'MenuListNewOffsetX/Y', '"

```
003FF9A0  sub      rsp, 0x28
003FF9A4  mov      rax, qword ptr [rip + 0x1c9b285]  ; -> 0209AC30
003FF9AB  mov      rcx, qword ptr [rax + 0x108]
003FF9B2  test     rcx, rcx
003FF9B5  je       0x3ff9e2  ; -> 003FF9E2
003FF9B7  mov      rcx, qword ptr [rcx + 0x170]
003FF9BE  xor      r9d, r9d
003FF9C1  xor      r8d, r8d
003FF9C4  xor      edx, edx
003FF9C6  call     0x2d4840  ; -> 002D4840 fn
003FF9CB  mov      rcx, qword ptr [rip + 0x1c9b25e]  ; -> 0209AC30
003FF9D2  mov      rcx, qword ptr [rcx + 0x108]
003FF9D9  add      rsp, 0x28
003FF9DD  jmp      0x2470d0  ; -> 002470D0 fn
003FF9E2  add      rsp, 0x28
003FF9E6  ret      
```
