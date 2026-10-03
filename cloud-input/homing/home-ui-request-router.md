# Homing pack: `16-UI/Request-Router/ui-request-router.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-ui-request-router.json`.

Bodies: 11. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00241940 (112 B, extent 00241940-002419B0)

Entered from (direct sites whose caller this page cites): `00241D40` + 0x776 (call; `00241D40` is cited on this page); `00241D40` + 0x7F6 (call; `00241D40` is cited on this page)
Other direct sites: none

Host context: "rame/MessageLine/NobuMessage widget procedure, passes its widget '+0xC0' ('00227F9C'; the widget is '0x190' bytes from [the factory](../Widget-Object-Model/CONTRACT-widget-object.md) at '00227EB8'); '00241D40' and '0057C480', the ConfirmCaption procedures, pass widget '+0xE0' ('002421A5', '0057C8E7', '0057C9B7'; '0057C480''s widget is '0x640' bytes, '0057C39F'); '002A3730' and '002A5CC0' pass their object's '+0xD0' ('002A37BB', '002A37D" / "rame/MessageLine/NobuMessage widget procedure, passes its widget '+0xC0' ('00227F9C'; the widget is '0x190' bytes from [the factory](../Widget-Object-Model/CONTRACT-widget-object.md) at '00227EB8'); '00241D40' and '0057C480', the ConfirmCaption procedures, pass widget '+0xE0' ('002421A5', '0057C8E7', '0057C9B7'; '0057C480''s widget is '0x640' bytes, '0057C39F'); '002A3730' and '002A5CC0' pass their object's '+0xD0' ('002A37BB', '002A37D"

```
00241940  push     rbx
00241942  sub      rsp, 0x20
00241946  mov      rbx, rcx
00241949  test     rcx, rcx
0024194C  je       0x241952  ; -> 00241952
0024194E  and      dword ptr [rcx + 0x40], 0xfffffff7
00241952  test     byte ptr [rcx + 0x3c4], 2
00241959  je       0x241989  ; -> 00241989
0024195B  or       dword ptr [rcx + 0x40], 0x40
0024195F  mov      eax, dword ptr [rcx + 0x40]
00241962  and      eax, 0x21
00241965  cmp      al, 0x21
00241967  jne      0x241970  ; -> 00241970
00241969  call     0x244dd0  ; -> 00244DD0 fn
0024196E  jmp      0x241989  ; -> 00241989
00241970  mov      rax, qword ptr [rcx]
00241973  test     rax, rax
00241976  je       0x241981  ; -> 00241981
00241978  lea      rdx, [rip + 0x6d36d9]  ; -> 00915058
0024197F  call     rax
00241981  mov      rcx, rbx
00241984  call     0x245020  ; -> 00245020 fn
00241989  test     dword ptr [rbx + 0x3c4], 0x400
00241993  je       0x24199a  ; -> 0024199A
00241995  call     0x2ccb10  ; -> 002CCB10 fn
0024199A  test     byte ptr [rbx + 0x3c4], 0x80
002419A1  je       0x2419aa  ; -> 002419AA
002419A3  mov      byte ptr [rbx + 0x3bc], 0
002419AA  add      rsp, 0x20
002419AE  pop      rbx
002419AF  ret      
```

## 0028D1C0 (154 B, extent 0028D1C0-0028D25A)

Entered from (direct sites whose caller this page cites): `0028C4B0` + 0x0 (jmp; `0028C4B0` is cited on this page)
Other direct sites: none

Host context: ", '002CC9F0' (14 B) | '002909F0' tears down '*(0209BE80)''s '+0x10F00' child — '0028C4F0', clears '+0x10F68' bit 3, '+0x10EF0 = 0', '0028C940(+0x7EA0)', marks the '+0xD70' chain via '0028C560', then '0028C4B0' and stores the result back; '002CC9F0' writes the duration to '*(0209AC30)+0xDF0' | '00290A57' ('call 0028C560' — the chain mark) / '002CC9F7' ('mov [rax+0xDF0], ecx') | | tick gate pair | '0024AC00' (7 B), '0024AC10' (21 B) | '00"

```
0028D1C0  push     rdi
0028D1C2  sub      rsp, 0x20
0028D1C6  mov      rdi, rcx
0028D1C9  test     rcx, rcx
0028D1CC  je       0x28d251  ; -> 0028D251
0028D1D2  mov      qword ptr [rsp + 0x30], rbx
0028D1D7  mov      qword ptr [rsp + 0x38], rsi
0028D1DC  xor      esi, esi
0028D1DE  nop      
0028D1E0  cmp      word ptr [rcx + 0xd54], 5
0028D1E8  mov      rbx, qword ptr [rcx + 0xd70]
0028D1EF  jne      0x28d23f  ; -> 0028D23F
0028D1F1  cmp      rdi, rcx
0028D1F4  cmove    rdi, rbx
0028D1F8  test     rbx, rbx
0028D1FB  je       0x28d20b  ; -> 0028D20B
0028D1FD  mov      rax, qword ptr [rcx + 0xd68]
0028D204  mov      qword ptr [rbx + 0xd68], rax
0028D20B  mov      rdx, qword ptr [rcx + 0xd68]
0028D212  test     rdx, rdx
0028D215  je       0x28d225  ; -> 0028D225
0028D217  mov      rax, qword ptr [rcx + 0xd70]
0028D21E  mov      qword ptr [rdx + 0xd70], rax
0028D225  mov      word ptr [rcx + 0xd54], si
0028D22C  mov      qword ptr [rcx + 0xd70], rsi
0028D233  mov      qword ptr [rcx + 0xd68], rsi
0028D23A  call     0x28fa50  ; -> 0028FA50 fn
0028D23F  mov      rcx, rbx
0028D242  test     rbx, rbx
0028D245  jne      0x28d1e0  ; -> 0028D1E0
0028D247  mov      rsi, qword ptr [rsp + 0x38]
0028D24C  mov      rbx, qword ptr [rsp + 0x30]
0028D251  mov      rax, rdi
0028D254  add      rsp, 0x20
0028D258  pop      rdi
0028D259  ret      
```

## 0028F5F0 (74 B, extent 0028F5F0-0028F63A)

Entered from (direct sites whose caller this page cites): `002E0E30` + 0x4 (call; `002E0E30` is cited on this page)
Other direct sites: `002E2320` + 0x4 (call)

Host context: "ng else '0' ('002E1A81'–'002E1AA1') — so they belong to request 22's sub-modes, of which the shipped scripts author '0x42' (once) and '0x40' (once); '0x21''s producer is not among the script calls.  '002E0E30' is the inverse for *current* fullscreen mode: it accepts modes '0..19' and maps them back to request IDs. **Mode 14 maps back to request 14** - which is why request 14 is structurally real even though no ordinary producer emits it"

```
0028F5F0  sub      rsp, 0x28
0028F5F4  mov      rcx, qword ptr [rip + 0x1e0c885]  ; -> 0209BE80
0028F5FB  test     rcx, rcx
0028F5FE  jne      0x28f607  ; -> 0028F607
0028F600  xor      eax, eax
0028F602  add      rsp, 0x28
0028F606  ret      
0028F607  test     dword ptr [rcx + 0x10f68], 0x2000
0028F611  jne      0x28f600  ; -> 0028F600
0028F613  add      rcx, 0xab30
0028F61A  call     0x273a20  ; -> 00273A20 fn
0028F61F  test     eax, eax
0028F621  je       0x28f600  ; -> 0028F600
0028F623  mov      rcx, qword ptr [rip + 0x1e0c856]  ; -> 0209BE80
0028F62A  add      rcx, 0xab30
0028F631  add      rsp, 0x28
0028F635  jmp      0x2767c0  ; -> 002767C0 fn
```

## 002904B0 (20 B, extent 002904B0-002904C4)

Entered from (direct sites whose caller this page cites): `0035D8D0` + 0x4 (call; `0035D8D0` is cited on this page); `0035DA80` + 0x4 (call; `0035DA80` is cited on this page)
Other direct sites: none

Host context: "5', '00252DCB'). It is called from sixteen sites: the generic route's area controller '00280140' (message   18, '00280286'), request 12's arm '0028E970', request 24's widget, '0035C960', '0035CF50', '0035D8D0', '0035DA80', the   '003C8990'–'003C8B70' bodies (seven sites), '00279E20' and '00290780'. The area   unload '002628B0' runs the reset '00252DE0', which zeroes both words too. Image-wide, '02092734' has exactly these   two writers " / "B'). It is called from sixteen sites: the generic route's area controller '00280140' (message   18, '00280286'), request 12's arm '0028E970', request 24's widget, '0035C960', '0035CF50', '0035D8D0', '0035DA80', the   '003C8990'–'003C8B70' bodies (seven sites), '00279E20' and '00290780'. The area   unload '002628B0' runs the reset '00252DE0', which zeroes both words too. Image-wide, '02092734' has exactly these   two writers and the sett"

```
002904B0  mov      rcx, qword ptr [rip + 0x1e0b9c9]  ; -> 0209BE80
002904B7  xor      eax, eax
002904B9  cmp      qword ptr [rcx + 0x10f78], rax
002904C0  setne    al
002904C3  ret      
```

## 00290740 (50 B, extent 00290740-00290772)

Entered from (direct sites whose caller this page cites): `002D5EB0` + 0x6A0 (call; `002D5EB0` is cited on this page)
Other direct sites: `0035DAE0` + 0x0 (jmp)

Host context: "DD batch 15, §7c)*. - **R11. The text stepper.** '002ABF70' has one call site, '002A9945' in the parser slot '002A8C50', which has no   direct caller. - **R12. The 'spattack' window.** Its procedure '002D5EB0' looks up text only through '002D5170', and the four ids   there ('0x4669', '0x466A', '0x466C', '0x46B4') are control-code templates in 'menu_command_template.bin', not a   title. - **R13. No native producer of 15, 18 or 19.** The "

```
00290740  sub      rsp, 0x28
00290744  mov      rax, qword ptr [rip + 0x1e0b735]  ; -> 0209BE80
0029074B  test     rax, rax
0029074E  je       0x29076d  ; -> 0029076D
00290750  cmp      qword ptr [rax + 0x10fb8], 0
00290758  jne      0x29076d  ; -> 0029076D
0029075A  call     0x2d5060  ; -> 002D5060 fn
0029075F  mov      rcx, qword ptr [rip + 0x1e0b71a]  ; -> 0209BE80
00290766  mov      qword ptr [rcx + 0x10fb8], rax
0029076D  add      rsp, 0x28
00290771  ret      
```

## 0029E6D0 (85 B, extent 0029E6D0-0029E725)

Entered from (direct sites whose caller this page cites): `002D5EB0` + 0x284 (call; `002D5EB0` is cited on this page); `002D5EB0` + 0x3AF (call; `002D5EB0` is cited on this page); `002D5EB0` + 0x50C (call; `002D5EB0` is cited on this page); `002D5EB0` + 0x544 (call; `002D5EB0` is cited on this page)
Other direct sites: `00295D50` + 0x0 (jmp); `002BD680` + 0x5D (call); `002BD680` + 0x1A2 (call)

Host context: "DD batch 15, §7c)*. - **R11. The text stepper.** '002ABF70' has one call site, '002A9945' in the parser slot '002A8C50', which has no   direct caller. - **R12. The 'spattack' window.** Its procedure '002D5EB0' looks up text only through '002D5170', and the four ids   there ('0x4669', '0x466A', '0x466C', '0x46B4') are control-code templates in 'menu_command_template.bin', not a   title. - **R13. No native producer of 15, 18 or 19.** The " / "DD batch 15, §7c)*. - **R11. The text stepper.** '002ABF70' has one call site, '002A9945' in the parser slot '002A8C50', which has no   direct caller. - **R12. The 'spattack' window.** Its procedure '002D5EB0' looks up text only through '002D5170', and the four ids   there ('0x4669', '0x466A', '0x466C', '0x46B4') are control-code templates in 'menu_command_template.bin', not a   title. - **R13. No native producer of 15, 18 or 19.** The "

```
0029E6D0  mov      rax, qword ptr [rip + 0x1dfddc1]  ; -> 0209C498
0029E6D7  mov      r9d, ecx
0029E6DA  test     rax, rax
0029E6DD  je       0x29e724  ; -> 0029E724
0029E6DF  mov      r8, qword ptr [rax + 0x158]
0029E6E6  test     r8, r8
0029E6E9  je       0x29e724  ; -> 0029E724
0029E6EB  add      r8, 0xd0
0029E6F2  je       0x29e724  ; -> 0029E724
0029E6F4  xor      edx, edx
0029E6F6  cmp      byte ptr [r8 + 2], dl
0029E6FA  jbe      0x29e724  ; -> 0029E724
0029E6FC  lea      rax, [r8 + 0x18]
0029E700  mov      r10d, 0xfff7
0029E706  test     r9d, r9d
0029E709  je       0x29e711  ; -> 0029E711
0029E70B  and      word ptr [rax], r10w
0029E70F  jmp      0x29e715  ; -> 0029E715
0029E711  or       word ptr [rax], 8
0029E715  movzx    ecx, byte ptr [r8 + 2]
0029E71A  inc      edx
0029E71C  add      rax, 0x18
0029E720  cmp      edx, ecx
0029E722  jl       0x29e706  ; -> 0029E706
0029E724  ret      
```

## 002C98F0 (170 B, extent 002C98F0-002C999A)

Entered from (direct sites whose caller this page cites): `002C98C0` + 0x8 (call; `002C98C0` is cited on this page)
Other direct sites: none

Host context: "with bit 6, '0027F5D0' calls '002D6F90' when the parameter is '0x42', then '00295CE0' and **'0027F2E0'** ('0027F61F'–'0027F63C') — which '002814E0(−1)' also reaches directly. '0027F2E0' runs a fade ('002C98C0', '00250F30', '002CC960'; duration 1 when context '+0x400' bit 11, else 200), re-reads '+0x400' and writes its **low byte**: 2 when bit 9 is clear; 1 when bit 9 is set and bit 10 clear; 2 when both are set ('0027F324'–'0027F33B'); "

```
002C98F0  push     rbx
002C98F2  sub      rsp, 0x20
002C98F6  mov      ebx, ecx
002C98F8  mov      rcx, qword ptr [rip + 0x1dd1331]  ; -> 0209AC30
002C98FF  mov      r8, qword ptr [rcx + rbx*8 + 0x2c8]
002C9907  test     r8, r8
002C990A  je       0x2c9994  ; -> 002C9994
002C9910  test     edx, edx
002C9912  jle      0x2c995d  ; -> 002C995D
002C9914  mov      eax, dword ptr [r8 + 0x7c]
002C9918  and      eax, 0x3ff7ff
002C991D  movzx    r9d, dx
002C9921  shl      r9d, 0x16
002C9925  or       eax, r9d
002C9928  bts      eax, 0xb
002C992C  mov      dword ptr [r8 + 0x7c], eax
002C9930  mov      rcx, qword ptr [rip + 0x1dd12f9]  ; -> 0209AC30
002C9937  mov      rdx, qword ptr [rcx + rbx*8 + 0x2b8]
002C993F  test     rdx, rdx
002C9942  je       0x2c995d  ; -> 002C995D
002C9944  mov      eax, dword ptr [rdx + 0x7c]
002C9947  and      eax, 0x3ff7ff
002C994C  or       eax, r9d
002C994F  bts      eax, 0xb
002C9953  mov      dword ptr [rdx + 0x7c], eax
002C9956  mov      rcx, qword ptr [rip + 0x1dd12d3]  ; -> 0209AC30
002C995D  mov      rcx, qword ptr [rcx + rbx*8 + 0x2c8]
002C9965  call     0x244f00  ; -> 00244F00 fn
002C996A  mov      rcx, qword ptr [rip + 0x1dd12bf]  ; -> 0209AC30
002C9971  mov      rcx, qword ptr [rcx + rbx*8 + 0x2b8]
002C9979  call     0x244f00  ; -> 00244F00 fn
002C997E  mov      rcx, qword ptr [rip + 0x1dd2993]  ; -> 0209C318
002C9985  test     rcx, rcx
002C9988  je       0x2c9994  ; -> 002C9994
002C998A  add      rsp, 0x20
002C998E  pop      rbx
002C998F  jmp      0x244f00  ; -> 00244F00 fn
002C9994  add      rsp, 0x20
002C9998  pop      rbx
002C9999  ret      
```

## 002D54B0 (69 B, extent 002D54B0-002D54F5)

Entered from (direct sites whose caller this page cites): `002D5EB0` + 0x57F (call; `002D5EB0` is cited on this page); `002D5EB0` + 0x607 (call; `002D5EB0` is cited on this page)
Other direct sites: none

Host context: "DD batch 15, §7c)*. - **R11. The text stepper.** '002ABF70' has one call site, '002A9945' in the parser slot '002A8C50', which has no   direct caller. - **R12. The 'spattack' window.** Its procedure '002D5EB0' looks up text only through '002D5170', and the four ids   there ('0x4669', '0x466A', '0x466C', '0x46B4') are control-code templates in 'menu_command_template.bin', not a   title. - **R13. No native producer of 15, 18 or 19.** The " / "DD batch 15, §7c)*. - **R11. The text stepper.** '002ABF70' has one call site, '002A9945' in the parser slot '002A8C50', which has no   direct caller. - **R12. The 'spattack' window.** Its procedure '002D5EB0' looks up text only through '002D5170', and the four ids   there ('0x4669', '0x466A', '0x466C', '0x46B4') are control-code templates in 'menu_command_template.bin', not a   title. - **R13. No native producer of 15, 18 or 19.** The "

```
002D54B0  push     rbx
002D54B2  sub      rsp, 0x20
002D54B6  mov      rbx, rcx
002D54B9  movzx    edx, dx
002D54BC  mov      ecx, 0x14
002D54C1  call     0x35d330  ; -> 0035D330 fn
002D54C6  mov      rcx, rax
002D54C9  test     rbx, rbx
002D54CC  je       0x2d54d6  ; -> 002D54D6
002D54CE  mov      rax, qword ptr [rbx + 0x60]
002D54D2  mov      rbx, qword ptr [rax + 8]
002D54D6  mov      rcx, qword ptr [rcx + 0x18]
002D54DA  xor      edx, edx
002D54DC  call     0x2b58b0  ; -> 002B58B0 fn
002D54E1  xor      ecx, ecx
002D54E3  mov      qword ptr [rbx + 0x18], rax
002D54E7  call     0x20e620  ; -> 0020E620 fn
002D54EC  mov      dword ptr [rbx + 0x20], eax
002D54EF  add      rsp, 0x20
002D54F3  pop      rbx
002D54F4  ret      
```

## 00309E40 (42 B, extent 00309E40-00309E6A)

Entered from (direct sites whose caller this page cites): `002D5EB0` + 0x80 (call; `002D5EB0` is cited on this page)
Other direct sites: none

Host context: "DD batch 15, §7c)*. - **R11. The text stepper.** '002ABF70' has one call site, '002A9945' in the parser slot '002A8C50', which has no   direct caller. - **R12. The 'spattack' window.** Its procedure '002D5EB0' looks up text only through '002D5170', and the four ids   there ('0x4669', '0x466A', '0x466C', '0x46B4') are control-code templates in 'menu_command_template.bin', not a   title. - **R13. No native producer of 15, 18 or 19.** The "

```
00309E40  sub      rsp, 0x28
00309E44  movss    xmm1, dword ptr [rip + 0x1fb833c]  ; -> 022C2188
00309E4C  movss    xmm0, dword ptr [rip + 0x1fb8330]  ; -> 022C2184
00309E54  subss    xmm1, xmm0
00309E58  call     0x2f8b90  ; -> 002F8B90 fn
00309E5D  movss    dword ptr [rip + 0x1fb8323], xmm0  ; -> 022C2188
00309E65  add      rsp, 0x28
00309E69  ret      
```

## 0035C660 (129 B, extent 0035C660-0035C6E1)

Entered from (direct sites whose caller this page cites): `0035D6B0` + 0x153 (call; `0035D6B0` is cited on this page)
Other direct sites: none

Host context: "it-15 exemption, cleared otherwise; arms capability-policy row 8 bits 6, 8, 9, 11 ('002548F0') | mechanism proven 2026-09-12 (FABLE) | | 24 | **party incapacitated** — a '0xC8'-byte widget with proc '0035D6B0' behind the singleton '022CA428'; raised (stage 3 / stage 18) when every non-guest member of the active party is down while playables remain in the reserves; ~~the widget builds the battle-menu selection state ('0035BC50') — the re"

```
0035C660  push     rbx
0035C662  sub      rsp, 0x50
0035C666  xor      eax, eax
0035C668  mov      rbx, rcx
0035C66B  cmp      dword ptr [rip + 0x1d360be], 3  ; -> 02092730
0035C672  mov      ecx, 0x86e
0035C677  mov      qword ptr [rsp + 0x20], rax
0035C67C  mov      qword ptr [rsp + 0x28], rax
0035C681  mov      qword ptr [rsp + 0x30], rax
0035C686  mov      qword ptr [rsp + 0x38], rax
0035C68B  mov      qword ptr [rsp + 0x40], rax
0035C690  mov      qword ptr [rsp + 0x48], rax
0035C695  je       0x35c69c  ; -> 0035C69C
0035C697  mov      ecx, 0x86f
0035C69C  call     0x2f9860  ; -> 002F9860 fn
0035C6A1  xor      ecx, ecx
0035C6A3  mov      qword ptr [rsp + 0x20], rax
0035C6A8  mov      rax, qword ptr [rip + 0x1d32379]  ; -> 0208EA28
0035C6AF  lea      rdx, [rsp + 0x20]
0035C6B4  mov      qword ptr [rsp + 0x30], rax
0035C6B9  mov      qword ptr [rsp + 0x28], rcx
0035C6BE  mov      qword ptr [rsp + 0x38], rbx
0035C6C3  mov      dword ptr [rsp + 0x40], ecx
0035C6C7  mov      dword ptr [rsp + 0x4c], 0x4fb
0035C6CF  mov      word ptr [rsp + 0x48], 0x102
0035C6D6  call     0x241c90  ; -> 00241C90 fn
0035C6DB  add      rsp, 0x50
0035C6DF  pop      rbx
0035C6E0  ret      
```

## 003C8950 (49 B, extent 003C8950-003C8981)

Entered from (direct sites whose caller this page cites): `00253C70` + 0x339 (call; `00253C70` is cited on this page); `0035BAA0` + 0x10 (call; `0035BAA0` is cited on this page)
Other direct sites: none

Host context: "                                            +0x08  void* payload                                                                +0x10  s64   request (movsxd) '''  ## 5. Call chain  ''' pad input   -> 00253C70  InputGameplay_ArbitrateDigitalInputAndModalState      -> eligibility gates      -> requestId prepared      -> 002E1B10 mailbox   OR   00254B50 router directly  authored script   -> 0x048D openfullscreenmenu_48d -> 003462D0 -> 002E" / "ly | strong - triggered by raw pad mask '0x1000' (Triangle) with parameter 0 | | 3 | Field party-leader selection | proven - D-pad Up/Down '0x10 \| 0x40', needs >= 2 eligible candidates, commits via '0035BAA0' | | 4 | Battle Menu open by the same route as request 1 ('0035D660') | proven 2026-09-18 (FABLE); UQ-162 | | 5 | Field free-target actor cycle | proven - D-pad Left/Right '0x20 \| 0x80', spatial actor ordering, commits a real targ"

```
003C8950  sub      rsp, 0x28
003C8954  mov      rax, qword ptr [rip + 0x277edd5]  ; -> 02B47730
003C895B  test     rax, rax
003C895E  je       0x3c897c  ; -> 003C897C
003C8960  test     byte ptr [rax + 0xc0], 2
003C8967  je       0x3c897c  ; -> 003C897C
003C8969  call     0x268620  ; -> 00268620 fn
003C896E  mov      rax, qword ptr [rip + 0x277edbb]  ; -> 02B47730
003C8975  and      dword ptr [rax + 0xc0], 0xfffffffd
003C897C  add      rsp, 0x28
003C8980  ret      
```
