# Homing pack: `16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-numeric-formatting-and-character-mapping.json`.

Bodies: 8. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002476E0 (58 B, extent 002476E0-0024771A)

Entered from (direct sites whose caller this page cites): `002A70B0` + 0x103 (call; `002A70B0` is cited on this page)
Other direct sites: none

Host context: "     ; the slot-1 dispatcher '''  '002A4830' shows the same relation from the other side: its state is copied out of '[window + 0xD0]'. So the values the parametric setters carry — '4' and '11' from '002A70B0', '6' from '002D66D0', '10' from '00572600', and '0xFF' remapped to '1' inside '002475D0' for '00227EE0', '00241D40' and '003F4330' — are the **widget's** byte and never index the four-group table. That distinction is load-bearing:"

```
002476E0  test     rcx, rcx
002476E3  je       0x247719  ; -> 00247719
002476E5  mov      eax, dword ptr [rcx + 0x40]
002476E8  test     al, al
002476EA  jns      0x247719  ; -> 00247719
002476EC  bt       eax, 8
002476F0  jb       0x247719  ; -> 00247719
002476F2  movzx    eax, byte ptr [rdx]
002476F5  add      byte ptr [rcx + 0xa4], al
002476FB  movzx    eax, byte ptr [rdx + 2]
002476FF  add      byte ptr [rcx + 0xa5], al
00247705  movzx    eax, byte ptr [rdx + 4]
00247709  add      byte ptr [rcx + 0xa6], al
0024770F  movzx    eax, byte ptr [rdx + 6]
00247713  add      byte ptr [rcx + 0xa7], al
00247719  ret      
```

## 0028F750 (88 B, extent 0028F750-0028F7A8)

Entered from (direct sites whose caller this page cites): `002A70B0` + 0x129 (call; `002A70B0` is cited on this page)
Other direct sites: none

Host context: "     ; the slot-1 dispatcher '''  '002A4830' shows the same relation from the other side: its state is copied out of '[window + 0xD0]'. So the values the parametric setters carry — '4' and '11' from '002A70B0', '6' from '002D66D0', '10' from '00572600', and '0xFF' remapped to '1' inside '002475D0' for '00227EE0', '00241D40' and '003F4330' — are the **widget's** byte and never index the four-group table. That distinction is load-bearing:"

```
0028F750  push     rbx
0028F752  sub      rsp, 0x20
0028F756  mov      rax, qword ptr [rip + 0x1e0c723]  ; -> 0209BE80
0028F75D  mov      rbx, rcx
0028F760  mov      rcx, qword ptr [rax + 0x10f80]
0028F767  test     rcx, rcx
0028F76A  jne      0x28f774  ; -> 0028F774
0028F76C  xor      eax, eax
0028F76E  add      rsp, 0x20
0028F772  pop      rbx
0028F773  ret      
0028F774  test     byte ptr [rcx + 0x1d39], 1
0028F77B  je       0x28f76c  ; -> 0028F76C
0028F77D  mov      ecx, dword ptr [rcx + 0x1d40]
0028F783  call     0x3588b0  ; -> 003588B0 fn
0028F788  cmp      rax, rbx
0028F78B  jne      0x28f76c  ; -> 0028F76C
0028F78D  mov      rax, qword ptr [rip + 0x1e0c6ec]  ; -> 0209BE80
0028F794  mov      rcx, qword ptr [rax + 0x10f80]
0028F79B  movzx    eax, byte ptr [rcx + 0x1d38]
0028F7A2  add      rsp, 0x20
0028F7A6  pop      rbx
0028F7A7  ret      
```

## 002A4030 (126 B, extent 002A4030-002A40AE)

Entered from (direct sites whose caller this page cites): `002A70B0` + 0x4A4 (call; `002A70B0` is cited on this page); `002A70B0` + 0x618 (call; `002A70B0` is cited on this page)
Other direct sites: none

Host context: "     ; the slot-1 dispatcher '''  '002A4830' shows the same relation from the other side: its state is copied out of '[window + 0xD0]'. So the values the parametric setters carry — '4' and '11' from '002A70B0', '6' from '002D66D0', '10' from '00572600', and '0xFF' remapped to '1' inside '002475D0' for '00227EE0', '00241D40' and '003F4330' — are the **widget's** byte and never index the four-group table. That distinction is load-bearing:" / "     ; the slot-1 dispatcher '''  '002A4830' shows the same relation from the other side: its state is copied out of '[window + 0xD0]'. So the values the parametric setters carry — '4' and '11' from '002A70B0', '6' from '002D66D0', '10' from '00572600', and '0xFF' remapped to '1' inside '002475D0' for '00227EE0', '00241D40' and '003F4330' — are the **widget's** byte and never index the four-group table. That distinction is load-bearing:"

```
002A4030  test     edx, edx
002A4032  je       0x2a40ad  ; -> 002A40AD
002A4034  xor      r8d, r8d
002A4037  test     rcx, rcx
002A403A  jne      0x2a4041  ; -> 002A4041
002A403C  mov      r9d, r8d
002A403F  jmp      0x2a4049  ; -> 002A4049
002A4041  mov      rax, qword ptr [rcx + 0x60]
002A4045  mov      r9, qword ptr [rax + 8]
002A4049  mov      r9, qword ptr [r9 + 0x18]
002A404D  test     r9, r9
002A4050  jne      0x2a4057  ; -> 002A4057
002A4052  mov      rax, r8
002A4055  jmp      0x2a405e  ; -> 002A405E
002A4057  mov      rax, qword ptr [r9 + 0x60]
002A405B  mov      rax, qword ptr [rax]
002A405E  add      word ptr [rax + 0x10], dx
002A4062  add      word ptr [r9 + 0x9c], dx
002A406A  test     rcx, rcx
002A406D  jne      0x2a4074  ; -> 002A4074
002A406F  mov      rcx, r8
002A4072  jmp      0x2a407b  ; -> 002A407B
002A4074  mov      rax, qword ptr [rcx + 0x60]
002A4078  mov      rcx, qword ptr [rax]
002A407B  mov      rcx, qword ptr [rcx + 0x18]
002A407F  test     rcx, rcx
002A4082  jne      0x2a4089  ; -> 002A4089
002A4084  mov      rax, r8
002A4087  jmp      0x2a4090  ; -> 002A4090
002A4089  mov      rax, qword ptr [rcx + 0x60]
002A408D  mov      rax, qword ptr [rax]
002A4090  add      word ptr [rax + 0x10], dx
002A4094  test     rcx, rcx
002A4097  je       0x2a40a1  ; -> 002A40A1
002A4099  mov      rax, qword ptr [rcx + 0x60]
002A409D  mov      r8, qword ptr [rax + 8]
002A40A1  add      word ptr [r8 + 0xc], dx
002A40A6  add      word ptr [rcx + 0x9c], dx
002A40AD  ret      
```

## 002A5520 (109 B, extent 002A5520-002A558D)

Entered from (direct sites whose caller this page cites): `002A70B0` + 0x40D (call; `002A70B0` is cited on this page); `002A70B0` + 0x547 (call; `002A70B0` is cited on this page)
Other direct sites: none

Host context: "     ; the slot-1 dispatcher '''  '002A4830' shows the same relation from the other side: its state is copied out of '[window + 0xD0]'. So the values the parametric setters carry — '4' and '11' from '002A70B0', '6' from '002D66D0', '10' from '00572600', and '0xFF' remapped to '1' inside '002475D0' for '00227EE0', '00241D40' and '003F4330' — are the **widget's** byte and never index the four-group table. That distinction is load-bearing:" / "     ; the slot-1 dispatcher '''  '002A4830' shows the same relation from the other side: its state is copied out of '[window + 0xD0]'. So the values the parametric setters carry — '4' and '11' from '002A70B0', '6' from '002D66D0', '10' from '00572600', and '0xFF' remapped to '1' inside '002475D0' for '00227EE0', '00241D40' and '003F4330' — are the **widget's** byte and never index the four-group table. That distinction is load-bearing:"

```
002A5520  mov      qword ptr [rsp + 8], rbx
002A5525  push     rdi
002A5526  sub      rsp, 0x30
002A552A  movaps   xmmword ptr [rsp + 0x20], xmm6
002A552F  mov      rbx, rcx
002A5532  call     0x28f810  ; -> 0028F810 fn
002A5537  mov      ecx, dword ptr [rbx + 0x114]
002A553D  mov      edi, eax
002A553F  shr      ecx, 0xb
002A5542  and      ecx, 1
002A5545  call     0x39c4a0  ; -> 0039C4A0 fn
002A554A  test     edi, edi
002A554C  cmovs    edi, dword ptr [rip + 0x1b66c89]  ; -> 01E0C1DC [u32 0x000001C0]
002A5553  call     0x17f880  ; -> 0017F880 fn
002A5558  cvttss2si ecx, xmm0
002A555C  lea      eax, [rcx + rcx*4]
002A555F  sub      edi, eax
002A5561  movd     xmm6, edi
002A5565  cvtdq2ps xmm6, xmm6
002A5568  call     0x24aba0  ; -> 0024ABA0 fn
002A556D  mov      rbx, qword ptr [rsp + 0x40]
002A5572  mulss    xmm0, dword ptr [rip + 0x65d18e]  ; -> 00902708 [f32 38]
002A557A  subss    xmm6, xmm0
002A557E  cvttss2si eax, xmm6
002A5582  movaps   xmm6, xmmword ptr [rsp + 0x20]
002A5587  add      rsp, 0x30
002A558B  pop      rdi
002A558C  ret      
```

## 004052A0 (14 B, extent 004052A0-004052AE)

Entered from (direct sites whose caller this page cites): `003EC810` + 0xD (jmp; `003EC810` is cited on this page)
Other direct sites: none

Host context: "d — and for each live slot either       calls '002A3730' to arm or writes '0' to disarm, on one 'int' argument. It also caches that       argument to '0209C62C' and calls '003EC830' when non-zero or '003EC810' when zero (18 bytes       each). **Every live message window is switched together.**        **And what decides it comes from the world tick.** '002A38C0''s only caller is '002E09A0', whose       only caller is '00314020'; '002E09A"

```
004052A0  mov      rcx, qword ptr [rip + 0x275dae1]  ; -> 02B62D88
004052A7  xor      edx, edx
004052A9  jmp      0x406dd0  ; -> 00406DD0 fn
```

## 004052B0 (17 B, extent 004052B0-004052C1)

Entered from (direct sites whose caller this page cites): `003EC830` + 0xD (jmp; `003EC830` is cited on this page)
Other direct sites: none

Host context: "a rsi, 0209C510' as the bound — and for each live slot either       calls '002A3730' to arm or writes '0' to disarm, on one 'int' argument. It also caches that       argument to '0209C62C' and calls '003EC830' when non-zero or '003EC810' when zero (18 bytes       each). **Every live message window is switched together.**        **And what decides it comes from the world tick.** '002A38C0''s only caller is '002E09A0', whose       only ca"

```
004052B0  mov      rcx, qword ptr [rip + 0x275dad1]  ; -> 02B62D88
004052B7  mov      edx, 1
004052BC  jmp      0x406dd0  ; -> 00406DD0 fn
```

## 00574770 (390 B, extent 00574770-005748F6)

Entered from (direct sites whose caller this page cites): `005742D0` + 0x10D (call; `005742D0` is cited on this page)
Other direct sites: none

Host context: "x14]      = measuredExtent '''  ## 5. Call chain  ''' Presentation.Rendering.ShaderMaterial (002B0280)  -. Runtime.RealFunctionPointerOrVtableMember          | Boundary.Audio.NativeSupport (002A6190, 005742D0) -+-> cluster doors                                                    |    002AC5F0  (7,489 B)  <====>  002B2150  (hub)  <-'       |  \       |   '-> 002B2DF0       v    002AE610 --> 003FFC60   three-byte record field decoder (NOT"

```
00574770  mov      qword ptr [rsp + 0x10], rbx
00574775  mov      qword ptr [rsp + 0x18], rbp
0057477A  mov      qword ptr [rsp + 0x20], rsi
0057477F  push     rdi
00574780  sub      rsp, 0x20
00574784  lea      rdx, [rsp + 0x30]
00574789  mov      rbx, rcx
0057478C  call     0x574080  ; -> 00574080 fn
00574791  mov      rdx, qword ptr [rbx + 0xd0]
00574798  mov      ebp, 0xffff8000
0057479D  movsx    edi, word ptr [rsp + 0x30]
005747A2  mov      r8, rax
005747A5  movsx    r11d, word ptr [rsp + 0x32]
005747AB  mov      r9d, edi
005747AE  mov      r10d, r11d
005747B1  movzx    ecx, word ptr [rdx + 0x48]
005747B5  cmp      cx, bp
005747B8  je       0x5747be  ; -> 005747BE
005747BA  movsx    r9d, cx
005747BE  movzx    eax, word ptr [rdx + 0x4a]
005747C2  cmp      ax, bp
005747C5  je       0x5747cb  ; -> 005747CB
005747C7  movsx    r10d, ax
005747CB  movzx    ecx, word ptr [rsp + 0x34]
005747D0  mov      esi, 0xffff
005747D5  movzx    eax, byte ptr [rsp + 0x36]
005747DA  mov      word ptr [rbx + 0x114], cx
005747E1  cmp      word ptr [rdx + 0x4c], si
005747E5  cmovne   cx, word ptr [rdx + 0x4c]
005747EA  mov      word ptr [rbx + 0x114], cx
005747F1  movzx    ecx, byte ptr [rdx + 0x4e]
005747F5  cmp      cl, 0xff
005747F8  je       0x5747fd  ; -> 005747FD
005747FA  movzx    eax, cl
005747FD  movzx    r8d, word ptr [r8 + 0xa]
00574802  movsx    edx, word ptr [rbx + 0x114]
00574809  mov      rcx, qword ptr [rbx + 0xe0]
00574810  imul     r8d, eax
00574814  movzx    eax, byte ptr [rsp + 0x37]
00574819  add      edx, eax
0057481B  test     rcx, rcx
0057481E  je       0x57483f  ; -> 0057483F
00574820  mov      word ptr [rcx + 0x98], r9w
00574828  mov      word ptr [rcx + 0x9a], r10w
00574830  mov      word ptr [rcx + 0x9c], dx
00574837  mov      word ptr [rcx + 0x9e], r8w
0057483F  mov      rax, qword ptr [rbx + 0xe0]
00574846  mov      rcx, qword ptr [rax + 0xc0]
0057484D  test     rcx, rcx
00574850  je       0x574859  ; -> 00574859
00574852  mov      word ptr [rcx + 0x9c], dx
00574859  cmp      byte ptr [rbx + 0x8060], 5
00574860  jne      0x5748e1  ; -> 005748E1
00574862  mov      rcx, qword ptr [rbx + 0xd0]
00574869  xor      r8d, r8d
0057486C  mov      r9d, r8d
0057486F  movzx    eax, word ptr [rcx + 0x48]
00574873  cmp      ax, bp
00574876  je       0x57487f  ; -> 0057487F
00574878  movsx    r8d, ax
0057487C  sub      r8d, edi
0057487F  movzx    eax, word ptr [rcx + 0x4a]
00574883  cmp      ax, bp
00574886  je       0x57488f  ; -> 0057488F
00574888  movsx    r9d, ax
0057488C  sub      r9d, r11d
0057488F  mov      rax, qword ptr [rbx + 0x60]
00574893  mov      rdx, qword ptr [rax + 8]
00574897  mov      rcx, qword ptr [rdx]
0057489A  movzx    eax, word ptr [rcx + 4]
0057489E  add      ax, r8w
005748A2  mov      word ptr [rdx + 0xc], ax
005748A6  movzx    eax, word ptr [rcx + 6]
005748AA  add      ax, r9w
005748AE  mov      word ptr [rdx + 0xe], ax
005748B2  mov      rax, qword ptr [rbx + 0x60]
005748B6  mov      rdx, qword ptr [rax + 0x10]
005748BA  mov      rcx, qword ptr [rdx]
005748BD  movzx    eax, word ptr [rcx + 4]
005748C1  add      ax, r8w
005748C5  mov      word ptr [rdx + 0xc], ax
005748C9  movzx    eax, word ptr [rcx + 6]
005748CD  add      ax, r9w
005748D1  mov      word ptr [rdx + 0xe], ax
005748D5  movzx    eax, word ptr [rcx + 8]
005748D9  sub      ax, r8w
005748DD  mov      word ptr [rdx + 0x10], ax
005748E1  mov      rbx, qword ptr [rsp + 0x38]
005748E6  mov      rbp, qword ptr [rsp + 0x40]
005748EB  mov      rsi, qword ptr [rsp + 0x48]
005748F0  add      rsp, 0x20
005748F4  pop      rdi
005748F5  ret      
```

## 005766B0 (44 B, extent 005766B0-005766DC)

Entered from (direct sites whose caller this page cites): `00573BE0` + 0x110 (call; `00573BE0` is cited on this page); `00573BE0` + 0x15D (call; `00573BE0` is cited on this page); `005742D0` + 0x140 (call; `005742D0` is cited on this page)
Other direct sites: `00574160` + 0x13B (call)

Host context: "ok content page** — [the menu screen atlas](../Menu-Screen-Atlas/the-menu-screen-atlas.md) lists it beside '00571A50' and '00579AF0' as handbook content, with dispatch ids 1, 3, 10, 12, 14, 15, 18 | '00573BE0' → '002B5390' → the hub '002B2150', from **cases 1 and 10** ('005745A6', '00574672') |       | '002B0280' | the ShaderMaterial body, 6,441 B | calls the hub directly; its six callers are '002A86A0' (a message-window helper), '002D8" / "ok content page** — [the menu screen atlas](../Menu-Screen-Atlas/the-menu-screen-atlas.md) lists it beside '00571A50' and '00579AF0' as handbook content, with dispatch ids 1, 3, 10, 12, 14, 15, 18 | '00573BE0' → '002B5390' → the hub '002B2150', from **cases 1 and 10** ('005745A6', '00574672') |       | '002B0280' | the ShaderMaterial body, 6,441 B | calls the hub directly; its six callers are '002A86A0' (a message-window helper), '002D8"

```
005766B0  mov      rax, qword ptr [rip + 0x2733081]  ; -> 02CA9738
005766B7  test     rax, rax
005766BA  je       0x5766c8  ; -> 005766C8
005766BC  mov      rax, qword ptr [rax + 0x110]
005766C3  test     rax, rax
005766C6  jne      0x5766cb  ; -> 005766CB
005766C8  xor      eax, eax
005766CA  ret      
005766CB  cmp      byte ptr [rax + 0xc9], 1
005766D2  jne      0x5766c8  ; -> 005766C8
005766D4  mov      rax, qword ptr [rax + 0xf8]
005766DB  ret      
```
