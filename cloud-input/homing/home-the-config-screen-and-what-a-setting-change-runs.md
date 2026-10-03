# Homing pack: `16-UI/Config-Screen/the-config-screen-and-what-a-setting-change-runs.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-config-screen-and-what-a-setting-change-runs.json`.

Bodies: 11. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0019B8C0 (127 B, extent 0019B8C0-0019B93F)

Entered from (direct sites whose caller this page cites): `00202930` + 0x150 (call; `00202930` is cited on this page)
Other direct sites: `0019B400` + 0x5E (call)

Host context: "7360' (446 B) is a 'Presentation.Rendering.NativeSupport' sibling - '01F813C8'/'008FA338'/'008FA350', '"TrackingMapScreenRateX"', '001FF740' quadruple plus '00200BE0'/'001FEE10'/'001EDF00' pairs and '00202930'. Interior anchor '001C7394' (a '001FF740' call).  ## SWE2-EC7-38 update (2026-09-19) - '001C7520'  '001C7520' (446 B) is the 'TrackingMapScreenSuperWideMul' sibling - '01F813C8'/'008FA368'/'008FA388', same '001FF740'/'00200BE0'/'0"

```
0019B8C0  mov      qword ptr [rsp + 8], rbx
0019B8C5  mov      qword ptr [rsp + 0x10], rsi
0019B8CA  push     rdi
0019B8CB  sub      rsp, 0x20
0019B8CF  cmp      qword ptr [rcx + 0x80], 0
0019B8D7  mov      rbx, rcx
0019B8DA  jne      0x19b8e2  ; -> 0019B8E2
0019B8DC  xor      edi, edi
0019B8DE  mov      esi, edi
0019B8E0  jmp      0x19b905  ; -> 0019B905
0019B8E2  call     0x19b580  ; -> 0019B580 fn
0019B8E7  mov      rcx, qword ptr [rbx + 0x80]
0019B8EE  xor      edi, edi
0019B8F0  test     al, al
0019B8F2  mov      rsi, rbx
0019B8F5  cmove    rsi, rdi
0019B8F9  call     qword ptr [rip + 0x727601]  ; -> 008C2F00 [u64 0x0000000001CCECE2]
0019B8FF  test     eax, eax
0019B901  cmovne   rsi, rdi
0019B905  mov      rcx, rbx
0019B908  mov      byte ptr [rbx + 0x7c], 0
0019B90C  mov      byte ptr [rbx + 0x71], 0
0019B910  call     qword ptr [rip + 0x726e9a]  ; -> 008C27B0 [u64 0x0000000001CCDB24]
0019B916  mov      qword ptr [rbx + 0x80], rdi
0019B91D  mov      rax, rsi
0019B920  mov      rcx, qword ptr [rip + 0x1de5819]  ; -> 01F81140
0019B927  mov      rsi, qword ptr [rsp + 0x38]
0019B92C  mov      qword ptr [rbx + 0x74], rcx
0019B930  mov      qword ptr [rbx + 0x68], rdi
0019B934  mov      rbx, qword ptr [rsp + 0x30]
0019B939  add      rsp, 0x20
0019B93D  pop      rdi
0019B93E  ret      
```

## 0019B990 (311 B, extent 0019B990-0019BAC7)

Entered from (direct sites whose caller this page cites): `00202930` + 0xFA (call; `00202930` is cited on this page)
Other direct sites: none

Host context: "7360' (446 B) is a 'Presentation.Rendering.NativeSupport' sibling - '01F813C8'/'008FA338'/'008FA350', '"TrackingMapScreenRateX"', '001FF740' quadruple plus '00200BE0'/'001FEE10'/'001EDF00' pairs and '00202930'. Interior anchor '001C7394' (a '001FF740' call).  ## SWE2-EC7-38 update (2026-09-19) - '001C7520'  '001C7520' (446 B) is the 'TrackingMapScreenSuperWideMul' sibling - '01F813C8'/'008FA368'/'008FA388', same '001FF740'/'00200BE0'/'0"

```
0019B990  push     rdi
0019B992  sub      rsp, 0x40
0019B996  mov      qword ptr [rsp + 0x38], 0xfffffffffffffffe
0019B99F  mov      qword ptr [rsp + 0x58], rbx
0019B9A4  mov      qword ptr [rsp + 0x60], rsi
0019B9A9  mov      eax, r8d
0019B9AC  mov      r10, rdx
0019B9AF  mov      rbx, rcx
0019B9B2  cmp      qword ptr [rcx + 0x80], 0
0019B9BA  jne      0x19bab5  ; -> 0019BAB5
0019B9C0  mov      r8d, r9d
0019B9C3  mov      edx, eax
0019B9C5  mov      rcx, r10
0019B9C8  call     qword ptr [rip + 0x726bfa]  ; -> 008C25C8 [u64 0x0000000001CCDC76]
0019B9CE  mov      rdi, rax
0019B9D1  test     rax, rax
0019B9D4  je       0x19bab5  ; -> 0019BAB5
0019B9DA  mov      byte ptr [rbx + 0x7c], 1
0019B9DE  mov      byte ptr [rbx + 0x71], 0
0019B9E2  mov      rcx, rbx
0019B9E5  call     qword ptr [rip + 0x726dc5]  ; -> 008C27B0 [u64 0x0000000001CCDB24]
0019B9EB  xor      esi, esi
0019B9ED  mov      qword ptr [rsp + 0x50], rsi
0019B9F2  mov      qword ptr [rsp + 0x20], rsi
0019B9F7  mov      qword ptr [rsp + 0x28], rsi
0019B9FC  lea      r9, [rsp + 0x28]
0019BA01  lea      r8, [rsp + 0x20]
0019BA06  lea      rdx, [rsp + 0x50]
0019BA0B  mov      rcx, rdi
0019BA0E  call     qword ptr [rip + 0x72740c]  ; -> 008C2E20 [u64 0x0000000001CCEEC8]
0019BA14  mov      rax, qword ptr [rsp + 0x50]
0019BA19  mov      qword ptr [rbx + 0x18], rax
0019BA1D  mov      qword ptr [rbx + 0x20], rax
0019BA21  mov      rax, qword ptr [rsp + 0x20]
0019BA26  mov      qword ptr [rbx + 0x38], rax
0019BA2A  mov      qword ptr [rbx + 0x40], rax
0019BA2E  mov      rax, qword ptr [rsp + 0x28]
0019BA33  mov      qword ptr [rbx + 0x50], rax
0019BA37  mov      qword ptr [rbx + 0x58], rax
0019BA3B  mov      qword ptr [rbx + 0x80], rdi
0019BA42  mov      rax, qword ptr [rip + 0x1de56f7]  ; -> 01F81140
0019BA49  mov      qword ptr [rbx + 0x74], rax
0019BA4D  mov      qword ptr [rbx + 0x68], rsi
0019BA51  lea      rdx, [rsp + 0x28]
0019BA56  mov      rcx, rbx
0019BA59  call     qword ptr [rip + 0x726d49]  ; -> 008C27A8 [u64 0x0000000001CCDAD8]
0019BA5F  nop      
0019BA60  mov      rcx, rax
0019BA63  call     0x19b2f0  ; -> 0019B2F0 fn
0019BA68  mov      rdi, rax
0019BA6B  mov      rcx, rax
0019BA6E  call     qword ptr [rip + 0x726bc4]  ; -> 008C2638 [u64 0x0000000001CCCE5A]
0019BA74  test     al, al
0019BA76  je       0x19ba7e  ; -> 0019BA7E
0019BA78  mov      qword ptr [rbx + 0x68], rsi
0019BA7C  jmp      0x19ba8c  ; -> 0019BA8C
0019BA7E  mov      qword ptr [rbx + 0x68], rdi
0019BA82  mov      rcx, rbx
0019BA85  call     qword ptr [rip + 0x726d25]  ; -> 008C27B0 [u64 0x0000000001CCDB24]
0019BA8B  nop      
0019BA8C  mov      rcx, qword ptr [rsp + 0x30]
0019BA91  test     rcx, rcx
0019BA94  je       0x19bab0  ; -> 0019BAB0
0019BA96  mov      rax, qword ptr [rcx]
0019BA99  call     qword ptr [rax + 0x10]
0019BA9C  test     rax, rax
0019BA9F  je       0x19bab0  ; -> 0019BAB0
0019BAA1  mov      r8, qword ptr [rax]
0019BAA4  mov      edx, 1
0019BAA9  mov      rcx, rax
0019BAAC  call     qword ptr [r8]
0019BAAF  nop      
0019BAB0  mov      rax, rbx
0019BAB3  jmp      0x19bab7  ; -> 0019BAB7
0019BAB5  xor      eax, eax
0019BAB7  mov      rbx, qword ptr [rsp + 0x58]
0019BABC  mov      rsi, qword ptr [rsp + 0x60]
0019BAC1  add      rsp, 0x40
0019BAC5  pop      rdi
0019BAC6  ret      
```

## 001DD050 (14 B, extent 001DD050-001DD05E)

Entered from (direct sites whose caller this page cites): `0017E070` + 0x4D (jmp; `0017E070` is cited on this page)
Other direct sites: none

Host context: "1, bound "> 0x16" -> default    each live arm: r8d = a property id, then 0017DD2E   call 001CD040(manager, direction, propertyId) 0017DD39   call 0016D6A0()                 ; unread 0017DD40   return 0017E070(row)            ; read the value back out of the config '''  ''' 001CD040  test dl,dl / mov r9d,r8d / sete r8b / jmp 001D1660   ; 14 B, direction in both polarities    001D1660   282-id dispatcher, 226 arms       001D5120   graphic"

```
001DD050  cmp      dword ptr [rcx + 0x18], 0
001DD054  jne      0x1dd05a  ; -> 001DD05A
001DD056  mov      eax, dword ptr [rcx + 0x38]
001DD059  ret      
001DD05A  mov      eax, dword ptr [rcx + 0x24]
001DD05D  ret      
```

## 00227DD0 (68 B, extent 00227DD0-00227E14)

Entered from (direct sites whose caller this page cites): `00228C70` + 0x417 (call; `00228C70` is cited on this page); `00228C70` + 0x51A (call; `00228C70` is cited on this page); `00228C70` + 0x551 (call; `00228C70` is cited on this page); `00228C70` + 0x571 (call; `00228C70` is cited on this page)
Other direct sites: none

Host context: "2527B0' tail). ## SWE2-EC7-31 update (2026-09-18) — '00241C90' '0x3D0' record ensure (via '003948B0'/'003949B0')  '00241C90' (101 B) — reached through '003948B0', '003949B0', '00394A90', '003CA310', '00228C70' and '002A1FB0' — is the shared 0x3D0-byte record ensure the settings/dialog builders call: a null 'rcx' allocates one through '002497B0(0x3D0)' (the 'rsp+0x20' flag records borrowed-vs-owned), then '002465F0(rec, 0x3D0, 00241D40, " / "2527B0' tail). ## SWE2-EC7-31 update (2026-09-18) — '00241C90' '0x3D0' record ensure (via '003948B0'/'003949B0')  '00241C90' (101 B) — reached through '003948B0', '003949B0', '00394A90', '003CA310', '00228C70' and '002A1FB0' — is the shared 0x3D0-byte record ensure the settings/dialog builders call: a null 'rcx' allocates one through '002497B0(0x3D0)' (the 'rsp+0x20' flag records borrowed-vs-owned), then '002465F0(rec, 0x3D0, 00241D40, "

```
00227DD0  sub      rsp, 0x28
00227DD4  imul     edx, ecx, 0x3c
00227DD7  mov      eax, 0x10624dd3
00227DDC  imul     edx
00227DDE  sar      edx, 6
00227DE1  mov      ecx, edx
00227DE3  shr      ecx, 0x1f
00227DE6  add      ecx, edx
00227DE8  call     0x251ee0  ; -> 00251EE0 fn
00227DED  call     0x250f30  ; -> 00250F30 fn
00227DF2  mov      rax, qword ptr [rip + 0x1e72e37]  ; -> 0209AC30
00227DF9  mov      rcx, qword ptr [rax + 0xc8]
00227E00  test     rcx, rcx
00227E03  je       0x227e0f  ; -> 00227E0F
00227E05  mov      dword ptr [rcx + 0xcc], 2
00227E0F  add      rsp, 0x28
00227E13  ret      
```

## 002405B0 (50 B, extent 002405B0-002405E2)

Entered from (direct sites whose caller this page cites): `0023FBE0` + 0x37D (call; `0023FBE0` is cited on this page); `0023FBE0` + 0x470 (call; `0023FBE0` is cited on this page)
Other direct sites: none

Host context: "he screen object '''  '0023BCC0' is itself 'lea'-materialised, at '0023C537' inside '0023BD40', and additionally has **three 'E8' call sites** ('002401FD', '0024027D', '00282186') in two functions — '0023FBE0' and '00281ED0'. **'00281ED0' is owned by UI and tagged 'V112-UI-Menu-HUD'**, and its own caller '00280DE0' carries the same ownership and '00280DE0' has **zero callers of its own** — the same 'lea' mechanism, one level further up." / "he screen object '''  '0023BCC0' is itself 'lea'-materialised, at '0023C537' inside '0023BD40', and additionally has **three 'E8' call sites** ('002401FD', '0024027D', '00282186') in two functions — '0023FBE0' and '00281ED0'. **'00281ED0' is owned by UI and tagged 'V112-UI-Menu-HUD'**, and its own caller '00280DE0' carries the same ownership and '00280DE0' has **zero callers of its own** — the same 'lea' mechanism, one level further up."

```
002405B0  cmp      ecx, 0x2d
002405B3  jae      0x2405df  ; -> 002405DF
002405B5  mov      eax, ecx
002405B7  lea      r8, [rip + 0x1bcb9a2]  ; -> 01E0BF60
002405BE  mov      r8, qword ptr [r8 + rax*8]
002405C2  test     r8, r8
002405C5  je       0x2405df  ; -> 002405DF
002405C7  movzx    eax, word ptr [r8 + 2]
002405CC  cmp      edx, eax
002405CE  jae      0x2405df  ; -> 002405DF
002405D0  mov      eax, edx
002405D2  lea      rax, [rax + rax*2]
002405D6  lea      rax, [rax + 2]
002405DA  lea      rax, [r8 + rax*2]
002405DE  ret      
002405DF  xor      eax, eax
002405E1  ret      
```

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

## 00292090 (33 B, extent 00292090-002920B1)

Entered from (direct sites whose caller this page cites): `00281ED0` + 0x496 (call; `00281ED0` is cited on this page)
Other direct sites: none

Host context: "t '''  '0023BCC0' is itself 'lea'-materialised, at '0023C537' inside '0023BD40', and additionally has **three 'E8' call sites** ('002401FD', '0024027D', '00282186') in two functions — '0023FBE0' and '00281ED0'. **'00281ED0' is owned by UI and tagged 'V112-UI-Menu-HUD'**, and its own caller '00280DE0' carries the same ownership and '00280DE0' has **zero callers of its own** — the same 'lea' mechanism, one level further up.  '0023BD40' (2"

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

## 003689E0 (97 B, extent 003689E0-00368A41)

Entered from (direct sites whose caller this page cites): `002D45C0` + 0x76 (call; `002D45C0` is cited on this page)
Other direct sites: none

Host context: "ge)  | function | size | role (call-signature read) | |---|---:|---| | '0023EFC0' | 449 | config-screen widget body (caller '0023FBE0'): '[rcx+0x60]'/'+0xC2', '[rbx+0xE0..0x120]' fields; '002D48C0', '002D45C0', '002445C0', inventory '002526F0', '002D46F0' |  ## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)  *Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only th"

```
003689E0  cmp      word ptr [rip + 0x1f63448], 0  ; -> 022CBE30
003689E8  je       0x368a40  ; -> 00368A40
003689EA  test     ecx, ecx
003689EC  je       0x3689f8  ; -> 003689F8
003689EE  mov      ecx, 8
003689F3  jmp      0x3688e0  ; -> 003688E0 fn
003689F8  movzx    eax, byte ptr [rip + 0x1f63488]  ; -> 022CBE87
003689FF  test     al, al
00368A01  je       0x368a24  ; -> 00368A24
00368A03  cmp      al, 1
00368A05  je       0x368a0e  ; -> 00368A0E
00368A07  sub      al, 2
00368A09  cmp      al, 1
00368A0B  ja       0x368a2d  ; -> 00368A2D
00368A0D  ret      
00368A0E  movsx    eax, word ptr [rip + 0x1f63475]  ; -> 022CBE8A
00368A15  movsx    ecx, word ptr [rip + 0x1f6346c]  ; -> 022CBE88
00368A1C  shl      eax, 3
00368A1F  cdq      
00368A20  idiv     ecx
00368A22  jmp      0x368a26  ; -> 00368A26
00368A24  xor      eax, eax
00368A26  mov      word ptr [rip + 0x1f6345d], ax  ; -> 022CBE8A
00368A2D  mov      eax, 8
00368A32  mov      byte ptr [rip + 0x1f6344e], 2  ; -> 022CBE87
00368A39  mov      word ptr [rip + 0x1f63448], ax  ; -> 022CBE88
00368A40  ret      
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
