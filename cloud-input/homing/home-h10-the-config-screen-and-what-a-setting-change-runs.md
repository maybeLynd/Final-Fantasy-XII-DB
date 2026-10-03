# Homing pack: `16-UI/Config-Screen/the-config-screen-and-what-a-setting-change-runs.md`

Generated 2026-10-03 12:18 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h10-the-config-screen-and-what-a-setting-change-runs.json`.

Bodies: 4. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00292010 (64 B, extent 00292010-00292050)

Entered from (direct sites whose caller this page cites): `00281ED0` + 0x1FC (call; `00281ED0` is cited on this page); `00281ED0` + 0x216 (call; `00281ED0` is cited on this page); `00281ED0` + 0x27B (call; `00281ED0` is cited on this page)
Other direct sites: none

Host context: "t '''  '0023BCC0' is itself 'lea'-materialised, at '0023C537' inside '0023BD40', and additionally has **three 'E8' call sites** ('002401FD', '0024027D', '00282186') in two functions — '0023FBE0' and '00281ED0'. **'00281ED0' is owned by UI and tagged 'V112-UI-Menu-HUD'**, and its own caller '00280DE0' carries the same ownership and '00280DE0' has **zero callers of its own** — the same 'lea' mechanism, one level further up.  '0023BD40' (2" / "t '''  '0023BCC0' is itself 'lea'-materialised, at '0023C537' inside '0023BD40', and additionally has **three 'E8' call sites** ('002401FD', '0024027D', '00282186') in two functions — '0023FBE0' and '00281ED0'. **'00281ED0' is owned by UI and tagged 'V112-UI-Menu-HUD'**, and its own caller '00280DE0' carries the same ownership and '00280DE0' has **zero callers of its own** — the same 'lea' mechanism, one level further up.  '0023BD40' (2"

```
00292010  mov      rax, qword ptr [rip + 0x1e08c19]  ; -> 0209AC30
00292017  mov      rcx, qword ptr [rax + 0x300]
0029201E  test     rcx, rcx
00292021  je       0x29204f  ; -> 0029204F
00292023  and      dword ptr [rcx + 0x168], 0xfff5ffff
0029202D  or       dword ptr [rcx + 0x168], 0x50000
00292037  mov      rax, qword ptr [rip + 0x1e08bf2]  ; -> 0209AC30
0029203E  mov      rcx, qword ptr [rax + 0x300]
00292045  and      dword ptr [rcx + 0x168], 0xff0fffff
0029204F  ret      
```

## 003B0190 (133 B, extent 003B0190-003B0215)

Entered from (direct sites whose caller this page cites): `0024C600` + 0x1F (call; `0024C600` is cited on this page)
Other direct sites: none

Host context: "89340 & 0x10' flag-gate the arms, 'byte[rax+4]' seeds the step, '0030A880', '003590D0', '003588B0', '00263E30', '0031B770' x2, '00313F60' x4, '003003F0' x2, '00311F70', '00236850' x2, '00236820' and '0024C600' drive the rebuild - the setting-change path's flagged worker; its '00263E30', '00236820'/'00236850', '00313F60' and '00311F70' helpers are shared with Combat-, Spawn_Encounter_Lifecycle- and Status_Periodic_Terminal-side callers. "

```
003B0190  mov      qword ptr [rsp + 8], rbx
003B0195  mov      r9d, edx
003B0198  lea      r11, [rip + 0x2b0ea69]  ; -> 02EBEC08
003B019F  mov      r10d, ecx
003B01A2  lea      rbx, [rip + 0x2b0edbf]  ; -> 02EBEF68
003B01A9  nop      dword ptr [rax]
003B01B0  cmp      dword ptr [r11 - 8], 0
003B01B5  je       0x3b0206  ; -> 003B0206
003B01B7  cmp      byte ptr [r11 + 9], 1
003B01BC  je       0x3b0206  ; -> 003B0206
003B01BE  mov      r8, qword ptr [r11]
003B01C1  test     r8, r8
003B01C4  je       0x3b0206  ; -> 003B0206
003B01C6  cmp      dword ptr [r8 + 8], r10d
003B01CA  jne      0x3b01d0  ; -> 003B01D0
003B01CC  mov      dword ptr [r8 + 8], r9d
003B01D0  xor      edx, edx
003B01D2  cmp      byte ptr [r8 + 0x372], dl
003B01D9  jbe      0x3b0206  ; -> 003B0206
003B01DB  lea      rax, [r8 + 0x90]
003B01E2  cmp      dword ptr [rax - 0x80], r10d
003B01E6  jne      0x3b01ec  ; -> 003B01EC
003B01E8  mov      dword ptr [rax - 0x80], r9d
003B01EC  cmp      dword ptr [rax], r10d
003B01EF  jne      0x3b01f4  ; -> 003B01F4
003B01F1  mov      dword ptr [rax], r9d
003B01F4  movzx    ecx, byte ptr [r8 + 0x372]
003B01FC  inc      edx
003B01FE  add      rax, 4
003B0202  cmp      edx, ecx
003B0204  jl       0x3b01e2  ; -> 003B01E2
003B0206  add      r11, 0x18
003B020A  cmp      r11, rbx
003B020D  jl       0x3b01b0  ; -> 003B01B0
003B020F  mov      rbx, qword ptr [rsp + 8]
003B0214  ret      
```

## 003B14F0 (97 B, extent 003B14F0-003B1551)

Entered from (direct sites whose caller this page cites): `0024C600` + 0x28 (call; `0024C600` is cited on this page)
Other direct sites: none

Host context: "89340 & 0x10' flag-gate the arms, 'byte[rax+4]' seeds the step, '0030A880', '003590D0', '003588B0', '00263E30', '0031B770' x2, '00313F60' x4, '003003F0' x2, '00311F70', '00236850' x2, '00236820' and '0024C600' drive the rebuild - the setting-change path's flagged worker; its '00263E30', '00236820'/'00236850', '00313F60' and '00311F70' helpers are shared with Combat-, Spawn_Encounter_Lifecycle- and Status_Periodic_Terminal-side callers. "

```
003B14F0  mov      r8, qword ptr [rip + 0x1cdfc31]  ; -> 02091128
003B14F7  mov      r9d, edx
003B14FA  mov      r10d, ecx
003B14FD  test     r8, r8
003B1500  je       0x3b1550  ; -> 003B1550
003B1502  cmp      dword ptr [r8 + 8], r10d
003B1506  jne      0x3b150c  ; -> 003B150C
003B1508  mov      dword ptr [r8 + 8], r9d
003B150C  xor      edx, edx
003B150E  cmp      byte ptr [r8 + 0x372], dl
003B1515  jbe      0x3b1544  ; -> 003B1544
003B1517  lea      rax, [r8 + 0x90]
003B151E  nop      
003B1520  cmp      dword ptr [rax - 0x80], r10d
003B1524  jne      0x3b152a  ; -> 003B152A
003B1526  mov      dword ptr [rax - 0x80], r9d
003B152A  cmp      dword ptr [rax], r10d
003B152D  jne      0x3b1532  ; -> 003B1532
003B152F  mov      dword ptr [rax], r9d
003B1532  movzx    ecx, byte ptr [r8 + 0x372]
003B153A  inc      edx
003B153C  add      rax, 4
003B1540  cmp      edx, ecx
003B1542  jl       0x3b1520  ; -> 003B1520
003B1544  mov      r8, qword ptr [r8 + 0x348]
003B154B  test     r8, r8
003B154E  jne      0x3b1502  ; -> 003B1502
003B1550  ret      
```

## 003F5260 (46 B, extent 003F5260-003F528E)

Entered from (direct sites whose caller this page cites): `003FBA80` + 0x342 (call; `003FBA80` is cited on this page)
Other direct sites: none

Host context: "8C0'; '002DD7E0' is reached by the nine-patch backgrounds '002455A0'/'00245170', icon draws '002BCB00'/'002B8EE0', post-process binding '0029A930', ScreenCapture '002D0650' and '00506700'/'003FB3E0'/'003FBA80'/'004048E0'. '001D1660' both calls and is called by the 'Presentation.Rendering.NativeSupport' family ('001C7520'/'001C7360'/'001CD040'/'001DC650'/ '001DC7A0'/'001DDAB0', 7 edges) — the settings-change path runs through native-supp"

```
003F5260  push     rbx
003F5262  sub      rsp, 0x20
003F5266  mov      rbx, rcx
003F5269  lea      rdx, [rip + 0x26f8b40]  ; -> 02AEDDB0
003F5270  add      rcx, 0x10
003F5274  call     0x202c70  ; -> 00202C70 fn
003F5279  lea      rcx, [rbx + 0x50]
003F527D  lea      rdx, [rip + 0x26f836c]  ; -> 02AED5F0
003F5284  add      rsp, 0x20
003F5288  pop      rbx
003F5289  jmp      0x202c90  ; -> 00202C90 fn
```
