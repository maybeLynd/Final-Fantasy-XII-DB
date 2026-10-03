# Homing pack: `02-Resource-And-Asset-Pipeline/Prefetch-And-Json-Data/ta-texture-animation-lists.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-ta-texture-animation-lists.json`.

Bodies: 16. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001802E0 (47 B, extent 001802E0-0018030F)

Entered from (direct sites whose caller this page cites): `002F5550` + 0xA94 (call; `002F5550` is cited on this page)
Other direct sites: none

Host context: "ERED 2026-09-25 (OPUS): the float is a track value of the map's tag-23 animation-slot family, on channel 9, and       its clock is that slot's time.**       - **What '+0x50' is.** The per-frame pass '002F5550' stores into the entry's '+0x50' the 0x130-byte slot record         that '00466CB0' matches ('002F57A3'-'002F57CE').       - **What '+0x90' is.** '004677A0' binds every track through '00466420(record, channel, &track+0xC)'. Channel"

```
001802E0  push     rbx
001802E2  sub      rsp, 0x20
001802E6  mov      ebx, ecx
001802E8  call     0x1a9930  ; -> 001A9930 fn
001802ED  test     rax, rax
001802F0  je       0x180306  ; -> 00180306
001802F2  call     0x1a9930  ; -> 001A9930 fn
001802F7  mov      rcx, rax
001802FA  mov      edx, ebx
001802FC  add      rsp, 0x20
00180300  pop      rbx
00180301  jmp      0x1a7410  ; -> 001A7410 fn
00180306  xorps    xmm0, xmm0
00180309  add      rsp, 0x20
0018030D  pop      rbx
0018030E  ret      
```

## 001803A0 (42 B, extent 001803A0-001803CA)

Entered from (direct sites whose caller this page cites): `002F5550` + 0x7FD (call; `002F5550` is cited on this page)
Other direct sites: none

Host context: "ERED 2026-09-25 (OPUS): the float is a track value of the map's tag-23 animation-slot family, on channel 9, and       its clock is that slot's time.**       - **What '+0x50' is.** The per-frame pass '002F5550' stores into the entry's '+0x50' the 0x130-byte slot record         that '00466CB0' matches ('002F57A3'-'002F57CE').       - **What '+0x90' is.** '004677A0' binds every track through '00466420(record, channel, &track+0xC)'. Channel"

```
001803A0  sub      rsp, 0x28
001803A4  call     0x1a9930  ; -> 001A9930 fn
001803A9  test     rax, rax
001803AC  je       0x1803c5  ; -> 001803C5
001803AE  call     0x1a9930  ; -> 001A9930 fn
001803B3  xor      ecx, ecx
001803B5  cmp      byte ptr [rax + 0x3d8], cl
001803BB  setne    cl
001803BE  mov      eax, ecx
001803C0  add      rsp, 0x28
001803C4  ret      
001803C5  add      rsp, 0x28
001803C9  ret      
```

## 00180430 (43 B, extent 00180430-0018045B)

Entered from (direct sites whose caller this page cites): `002F5550` + 0x806 (call; `002F5550` is cited on this page)
Other direct sites: none

Host context: "ERED 2026-09-25 (OPUS): the float is a track value of the map's tag-23 animation-slot family, on channel 9, and       its clock is that slot's time.**       - **What '+0x50' is.** The per-frame pass '002F5550' stores into the entry's '+0x50' the 0x130-byte slot record         that '00466CB0' matches ('002F57A3'-'002F57CE').       - **What '+0x90' is.** '004677A0' binds every track through '00466420(record, channel, &track+0xC)'. Channel"

```
00180430  sub      rsp, 0x28
00180434  call     0x1a9930  ; -> 001A9930 fn
00180439  test     rax, rax
0018043C  je       0x180456  ; -> 00180456
0018043E  call     0x1a9930  ; -> 001A9930 fn
00180443  movzx    ecx, byte ptr [rax + 0x80]
0018044A  xor      eax, eax
0018044C  test     cl, cl
0018044E  setne    al
00180451  add      rsp, 0x28
00180455  ret      
00180456  add      rsp, 0x28
0018045A  ret      
```

## 001804A0 (72 B, extent 001804A0-001804E8)

Entered from (direct sites whose caller this page cites): `002F5550` + 0xA1C (call; `002F5550` is cited on this page)
Other direct sites: none

Host context: "ERED 2026-09-25 (OPUS): the float is a track value of the map's tag-23 animation-slot family, on channel 9, and       its clock is that slot's time.**       - **What '+0x50' is.** The per-frame pass '002F5550' stores into the entry's '+0x50' the 0x130-byte slot record         that '00466CB0' matches ('002F57A3'-'002F57CE').       - **What '+0x90' is.** '004677A0' binds every track through '00466420(record, channel, &track+0xC)'. Channel"

```
001804A0  push     rbx
001804A2  sub      rsp, 0x20
001804A6  mov      ebx, ecx
001804A8  call     0x1a9930  ; -> 001A9930 fn
001804AD  test     rax, rax
001804B0  je       0x1804e0  ; -> 001804E0
001804B2  call     0x1a9930  ; -> 001A9930 fn
001804B7  movzx    eax, byte ptr [rax + 0x80]
001804BE  test     al, al
001804C0  je       0x1804e0  ; -> 001804E0
001804C2  call     0x1a9930  ; -> 001A9930 fn
001804C7  mov      rcx, rax
001804CA  mov      edx, ebx
001804CC  call     0x1a7940  ; -> 001A7940 fn
001804D1  test     al, al
001804D3  je       0x1804e0  ; -> 001804E0
001804D5  mov      eax, 1
001804DA  add      rsp, 0x20
001804DE  pop      rbx
001804DF  ret      
001804E0  xor      eax, eax
001804E2  add      rsp, 0x20
001804E6  pop      rbx
001804E7  ret      
```

## 001804F0 (111 B, extent 001804F0-0018055F)

Entered from (direct sites whose caller this page cites): `002F5550` + 0x845 (call; `002F5550` is cited on this page)
Other direct sites: none

Host context: "ERED 2026-09-25 (OPUS): the float is a track value of the map's tag-23 animation-slot family, on channel 9, and       its clock is that slot's time.**       - **What '+0x50' is.** The per-frame pass '002F5550' stores into the entry's '+0x50' the 0x130-byte slot record         that '00466CB0' matches ('002F57A3'-'002F57CE').       - **What '+0x90' is.** '004677A0' binds every track through '00466420(record, channel, &track+0xC)'. Channel"

```
001804F0  push     rbx
001804F2  sub      rsp, 0x20
001804F6  mov      ebx, ecx
001804F8  call     0x1a9930  ; -> 001A9930 fn
001804FD  test     rax, rax
00180500  je       0x180557  ; -> 00180557
00180502  call     0x1a9930  ; -> 001A9930 fn
00180507  mov      rdx, qword ptr [rax + 0x100]
0018050E  lea      rcx, [rax + 0xf0]
00180515  lea      r8, [rax + 0xf0]
0018051C  mov      rax, rcx
0018051F  test     rdx, rdx
00180522  je       0x18053a  ; -> 0018053A
00180524  cmp      dword ptr [rdx + 0x20], ebx
00180527  jl       0x180532  ; -> 00180532
00180529  mov      rax, rdx
0018052C  mov      rdx, qword ptr [rdx + 8]
00180530  jmp      0x180535  ; -> 00180535
00180532  mov      rdx, qword ptr [rdx]
00180535  test     rdx, rdx
00180538  jne      0x180524  ; -> 00180524
0018053A  cmp      rax, rcx
0018053D  je       0x180544  ; -> 00180544
0018053F  cmp      ebx, dword ptr [rax + 0x20]
00180542  jge      0x180547  ; -> 00180547
00180544  mov      rax, rcx
00180547  cmp      rax, r8
0018054A  je       0x180557  ; -> 00180557
0018054C  mov      eax, 1
00180551  add      rsp, 0x20
00180555  pop      rbx
00180556  ret      
00180557  xor      eax, eax
00180559  add      rsp, 0x20
0018055D  pop      rbx
0018055E  ret      
```

## 00180560 (111 B, extent 00180560-001805CF)

Entered from (direct sites whose caller this page cites): `002F5550` + 0x1133 (call; `002F5550` is cited on this page)
Other direct sites: none

Host context: "ERED 2026-09-25 (OPUS): the float is a track value of the map's tag-23 animation-slot family, on channel 9, and       its clock is that slot's time.**       - **What '+0x50' is.** The per-frame pass '002F5550' stores into the entry's '+0x50' the 0x130-byte slot record         that '00466CB0' matches ('002F57A3'-'002F57CE').       - **What '+0x90' is.** '004677A0' binds every track through '00466420(record, channel, &track+0xC)'. Channel"

```
00180560  mov      qword ptr [rsp + 0x18], rbp
00180565  push     rsi
00180566  sub      rsp, 0x20
0018056A  mov      rsi, rdx
0018056D  mov      ebp, ecx
0018056F  call     0x1a9930  ; -> 001A9930 fn
00180574  test     rax, rax
00180577  je       0x1805c4  ; -> 001805C4
00180579  mov      qword ptr [rsp + 0x30], rbx
0018057E  mov      qword ptr [rsp + 0x38], rdi
00180583  call     0x189120  ; -> 00189120 fn
00180588  xor      edi, edi
0018058A  mov      ebx, edi
0018058C  cmp      byte ptr [rax + 0x1c], bl
0018058F  setne    bl
00180592  call     0x1a9930  ; -> 001A9930 fn
00180597  mov      rcx, rax
0018059A  mov      r9, rsi
0018059D  mov      r8d, ebp
001805A0  mov      edx, ebx
001805A2  call     0x1a7a10  ; -> 001A7A10 fn
001805A7  mov      rbx, qword ptr [rsp + 0x30]
001805AC  test     al, al
001805AE  setne    dil
001805B2  mov      eax, edi
001805B4  mov      rdi, qword ptr [rsp + 0x38]
001805B9  mov      rbp, qword ptr [rsp + 0x40]
001805BE  add      rsp, 0x20
001805C2  pop      rsi
001805C3  ret      
001805C4  mov      rbp, qword ptr [rsp + 0x40]
001805C9  add      rsp, 0x20
001805CD  pop      rsi
001805CE  ret      
```

## 0019DDD0 (296 B, extent 0019DDD0-0019DEF8)

Entered from (direct sites whose caller this page cites): `001AA4F0` + 0x59 (call; `001AA4F0` is cited on this page)
Other direct sites: `0019CE30` + 0x85 (call); `0019CEF0` + 0x5C (call); `0019D100` + 0x7F (call)

Host context: "ter '[rcx]' advance to 'rdx' bound. Interior anchor '001A7665' (the '[rax+0x78]' chain advance).    ## SWE2-EC7-63 update (2026-09-19) - '001AB8A0'  '001AB8A0' (488 B) is a TA-list body - '0019D8D0'/'001AA4F0'/'001AA630'/'001AAF80'/'001AB350' plus two vcalls. Interior anchor '001AB906' (a '0019D8D0' call).    ## SWE2-EC7-63 update (2026-09-19) - '001E1490'  '001E1490' (144 B) is a call-free '0x80'-stride 'movups' record copier - 4-itera"

```
0019DDD0  mov      qword ptr [rsp + 0x20], rbx
0019DDD5  push     r14
0019DDD7  sub      rsp, 0x20
0019DDDB  mov      r14, rdx
0019DDDE  mov      rbx, rcx
0019DDE1  cmp      rdx, rcx
0019DDE4  je       0x19dee9  ; -> 0019DEE9
0019DDEA  mov      rcx, qword ptr [rcx]
0019DDED  mov      rax, qword ptr [rbx + 0x10]
0019DDF1  mov      qword ptr [rsp + 0x30], rbp
0019DDF6  sub      rax, rcx
0019DDF9  mov      rbp, qword ptr [rdx]
0019DDFC  mov      qword ptr [rsp + 0x38], rsi
0019DE01  mov      rsi, qword ptr [rdx + 8]
0019DE05  mov      qword ptr [rsp + 0x40], rdi
0019DE0A  mov      rdi, rsi
0019DE0D  sub      rdi, rbp
0019DE10  sar      rax, 3
0019DE14  sar      rdi, 3
0019DE18  cmp      edi, eax
0019DE1A  jbe      0x19de82  ; -> 0019DE82
0019DE1C  test     edi, edi
0019DE1E  je       0x19de39  ; -> 0019DE39
0019DE20  mov      rax, qword ptr [rbx + 0x18]
0019DE24  lea      rcx, [rbx + 0x18]
0019DE28  mov      edx, edi
0019DE2A  xor      r8d, r8d
0019DE2D  shl      rdx, 3
0019DE31  call     qword ptr [rax + 0x10]
0019DE34  mov      r14, rax
0019DE37  jmp      0x19de3c  ; -> 0019DE3C
0019DE39  xor      r14d, r14d
0019DE3C  sub      rsi, rbp
0019DE3F  mov      rdx, rbp
0019DE42  mov      r8, rsi
0019DE45  mov      rcx, r14
0019DE48  call     qword ptr [rip + 0x724bf2]  ; -> 008C2A40 [u64 0x0000000001CCEB62]
0019DE4E  mov      rdx, qword ptr [rbx]
0019DE51  test     rdx, rdx
0019DE54  je       0x19de73  ; -> 0019DE73
0019DE56  mov      r8, qword ptr [rbx + 0x10]
0019DE5A  lea      rcx, [rbx + 0x18]
0019DE5E  mov      r9, qword ptr [rcx]
0019DE61  sub      r8, rdx
0019DE64  sar      r8, 3
0019DE68  mov      r8d, r8d
0019DE6B  shl      r8, 3
0019DE6F  call     qword ptr [r9 + 0x18]
0019DE73  mov      eax, edi
0019DE75  mov      qword ptr [rbx], r14
0019DE78  lea      rcx, [r14 + rax*8]
0019DE7C  mov      qword ptr [rbx + 0x10], rcx
0019DE80  jmp      0x19decd  ; -> 0019DECD
0019DE82  mov      r8, qword ptr [rbx + 8]
0019DE86  mov      rdx, rbp
0019DE89  sub      r8, rcx
0019DE8C  sar      r8, 3
0019DE90  cmp      edi, r8d
0019DE93  jbe      0x19dec1  ; -> 0019DEC1
0019DE95  lea      r8, [r8*8]
0019DE9D  call     qword ptr [rip + 0x724b9d]  ; -> 008C2A40 [u64 0x0000000001CCEB62]
0019DEA3  mov      rcx, qword ptr [rbx + 8]
0019DEA7  mov      rax, qword ptr [r14]
0019DEAA  mov      rdx, rcx
0019DEAD  sub      rdx, qword ptr [rbx]
0019DEB0  mov      r8, qword ptr [r14 + 8]
0019DEB4  sar      rdx, 3
0019DEB8  lea      rdx, [rax + rdx*8]
0019DEBC  sub      r8, rdx
0019DEBF  jmp      0x19dec7  ; -> 0019DEC7
0019DEC1  sub      rsi, rbp
0019DEC4  mov      r8, rsi
0019DEC7  call     qword ptr [rip + 0x724b73]  ; -> 008C2A40 [u64 0x0000000001CCEB62]
0019DECD  mov      rax, qword ptr [rbx]
0019DED0  mov      rsi, qword ptr [rsp + 0x38]
0019DED5  mov      rbp, qword ptr [rsp + 0x30]
0019DEDA  mov      ecx, edi
0019DEDC  mov      rdi, qword ptr [rsp + 0x40]
0019DEE1  lea      rcx, [rax + rcx*8]
0019DEE5  mov      qword ptr [rbx + 8], rcx
0019DEE9  mov      rax, rbx
0019DEEC  mov      rbx, qword ptr [rsp + 0x48]
0019DEF1  add      rsp, 0x20
0019DEF5  pop      r14
0019DEF7  ret      
```

## 001AC810 (316 B, extent 001AC810-001AC94C)

Entered from (direct sites whose caller this page cites): `001ABC80` + 0x1D (call; `001ABC80` is cited on this page); `001ABCE0` + 0x1D (call; `001ABCE0` is cited on this page)
Other direct sites: none

Host context: "; interior verified 2026-09-17, SWE2-FRONTIER — '001E1370' first at ['001E1EF1'](../../_index/ADDRESS-INDEX.md)), '001E3F70', '001E5290', '001E55C0'/'001E6110' (462 B twins → '001E6040'), '001AC480'/'001ABC80'/'001ABCE0'/'001AD6E0'/'001AD7B0' | element ops behind the iterators — '001E1DD0''s '[r9]' pair is the same callback idiom as the SEAD container family ('00210760' subtree) |  Not established: which of the two dispatcher twins serv" / "verified 2026-09-17, SWE2-FRONTIER — '001E1370' first at ['001E1EF1'](../../_index/ADDRESS-INDEX.md)), '001E3F70', '001E5290', '001E55C0'/'001E6110' (462 B twins → '001E6040'), '001AC480'/'001ABC80'/'001ABCE0'/'001AD6E0'/'001AD7B0' | element ops behind the iterators — '001E1DD0''s '[r9]' pair is the same callback idiom as the SEAD container family ('00210760' subtree) |  Not established: which of the two dispatcher twins serves '.ta' ve"

```
001AC810  mov      rax, rsp
001AC813  push     rdi
001AC814  sub      rsp, 0x90
001AC81B  mov      qword ptr [rax - 0x58], 0xfffffffffffffffe
001AC823  mov      qword ptr [rax + 0x10], rbx
001AC827  mov      qword ptr [rax + 0x20], rsi
001AC82B  movaps   xmmword ptr [rax - 0x18], xmm6
001AC82F  movaps   xmmword ptr [rax - 0x28], xmm7
001AC833  movaps   xmmword ptr [rax - 0x38], xmm8
001AC838  movaps   xmmword ptr [rax - 0x48], xmm9
001AC83D  mov      esi, edx
001AC83F  lea      rbx, [rcx + 0xf0]
001AC846  mov      rax, qword ptr [rbx + 8]
001AC84A  sub      rax, qword ptr [rbx]
001AC84D  sar      rax, 3
001AC851  mov      edi, edx
001AC853  sub      edi, eax
001AC855  js       0x1ac912  ; -> 001AC912
001AC85B  xorps    xmm6, xmm6
001AC85E  movss    xmm7, dword ptr [rip + 0x74a4ee]  ; -> 008F6D54 [f32 60]
001AC866  movss    xmm8, dword ptr [rip + 0x1b3f399]  ; -> 01CEBC08 [f32 2]
001AC86F  movss    xmm9, dword ptr [rip + 0x74a4e0]  ; -> 008F6D58 [f32 80]
001AC878  nop      dword ptr [rax + rax]
001AC880  mov      ecx, 0x48
001AC885  call     0x210ec0  ; -> 00210EC0 fn
001AC88A  mov      qword ptr [rsp + 0xb0], rax
001AC892  test     rax, rax
001AC895  je       0x1ac8d3  ; -> 001AC8D3
001AC897  mov      rdx, qword ptr [rbx + 8]
001AC89B  sub      rdx, qword ptr [rbx]
001AC89E  sar      rdx, 3
001AC8A2  mov      dword ptr [rsp + 0x38], 6
001AC8AA  movss    dword ptr [rsp + 0x30], xmm6
001AC8B0  mov      dword ptr [rsp + 0x28], 1
001AC8B8  movss    dword ptr [rsp + 0x20], xmm7
001AC8BE  movaps   xmm3, xmm8
001AC8C2  movaps   xmm2, xmm9
001AC8C6  mov      rcx, rax
001AC8C9  call     0x1aa840  ; -> 001AA840 fn
001AC8CE  mov      rcx, rax
001AC8D1  jmp      0x1ac8d5  ; -> 001AC8D5
001AC8D3  xor      ecx, ecx
001AC8D5  mov      qword ptr [rsp + 0xa0], rcx
001AC8DD  mov      rdx, qword ptr [rbx + 8]
001AC8E1  cmp      rdx, qword ptr [rbx + 0x10]
001AC8E5  jae      0x1ac8f9  ; -> 001AC8F9
001AC8E7  lea      rax, [rdx + 8]
001AC8EB  mov      qword ptr [rbx + 8], rax
001AC8EF  test     rdx, rdx
001AC8F2  je       0x1ac909  ; -> 001AC909
001AC8F4  mov      qword ptr [rdx], rcx
001AC8F7  jmp      0x1ac909  ; -> 001AC909
001AC8F9  lea      r8, [rsp + 0xa0]
001AC901  mov      rcx, rbx
001AC904  call     0x1ab570  ; -> 001AB570 fn
001AC909  sub      edi, 1
001AC90C  jns      0x1ac880  ; -> 001AC880
001AC912  mov      rax, qword ptr [rbx]
001AC915  mov      rcx, qword ptr [rax + rsi*8]
001AC919  mov      dword ptr [rcx + 0x38], esi
001AC91C  mov      rax, qword ptr [rbx]
001AC91F  mov      rax, qword ptr [rax + rsi*8]
001AC923  lea      r11, [rsp + 0x90]
001AC92B  mov      rbx, qword ptr [r11 + 0x18]
001AC92F  mov      rsi, qword ptr [r11 + 0x28]
001AC933  movaps   xmm6, xmmword ptr [r11 - 0x10]
001AC938  movaps   xmm7, xmmword ptr [rsp + 0x70]
001AC93D  movaps   xmm8, xmmword ptr [r11 - 0x30]
001AC942  movaps   xmm9, xmmword ptr [r11 - 0x40]
001AC947  mov      rsp, r11
001AC94A  pop      rdi
001AC94B  ret      
```

## 001DE280 (116 B, extent 001DE280-001DE2F4)

Entered from (direct sites whose caller this page cites): `00201EB0` + 0x725 (call; `00201EB0` is cited on this page); `00201EB0` + 0x76A (call; `00201EB0` is cited on this page)
Other direct sites: `001DE360` + 0x10 (call); `001DE4A0` + 0x14 (call); `002008F0` + 0x207 (call); `00200BF0` + 0x21B (call); `00201890` + 0x370 (call)

Host context: "ply-accumulate). ## SWE2-EC7-32 update (2026-09-18) — '001A4250' 'vector<int>' insert (via '001A5B30'/'001A7850'/'001E1670')  '001A4250' (315 B) — reached through '001A5B30', '001A7850', '001E1670', '00201EB0', '0020AE70' and '0020AF10' — is the CRT 'vector<int>' insert the ta list builders share: room at '[rcx+8] != [rcx+0x10]' shifts the tail one element and writes in place; a full vector doubles capacity through the allocator's '+0x1" / "ply-accumulate). ## SWE2-EC7-32 update (2026-09-18) — '001A4250' 'vector<int>' insert (via '001A5B30'/'001A7850'/'001E1670')  '001A4250' (315 B) — reached through '001A5B30', '001A7850', '001E1670', '00201EB0', '0020AE70' and '0020AF10' — is the CRT 'vector<int>' insert the ta list builders share: room at '[rcx+8] != [rcx+0x10]' shifts the tail one element and writes in place; a full vector doubles capacity through the allocator's '+0x1"

```
001DE280  mov      qword ptr [rsp + 8], rbx
001DE285  push     rdi
001DE286  sub      rsp, 0x20
001DE28A  mov      rax, qword ptr [rcx - 0x98]
001DE291  mov      rdi, rcx
001DE294  movsxd   rdx, dword ptr [rax + 4]
001DE298  lea      rax, [rip + 0x722d01]  ; -> 00900FA0
001DE29F  mov      qword ptr [rdx + rcx - 0x98], rax
001DE2A7  mov      rax, qword ptr [rcx - 0x98]
001DE2AE  movsxd   rdx, dword ptr [rax + 4]
001DE2B2  lea      rax, [rip + 0x722c67]  ; -> 00900F20
001DE2B9  lea      r8d, [rdx - 0x98]
001DE2C0  mov      dword ptr [rdx + rcx - 0x9c], r8d
001DE2C8  mov      qword ptr [rcx - 0x80], rax
001DE2CC  add      rcx, -0x80
001DE2D0  call     0x1df8c0  ; -> 001DF8C0 fn
001DE2D5  lea      rcx, [rdi - 0x80]
001DE2D9  call     qword ptr [rip + 0x6e44c1]  ; -> 008C27A0 [u64 0x0000000001CCDA9C]
001DE2DF  lea      rcx, [rdi - 0x78]
001DE2E3  mov      rbx, qword ptr [rsp + 0x30]
001DE2E8  add      rsp, 0x20
001DE2EC  pop      rdi
001DE2ED  jmp      qword ptr [rip + 0x6e4224]  ; -> 008C2518 [u64 0x0000000001CCE090]
```

## 001E0360 (35 B, extent 001E0360-001E0383)

Entered from (direct sites whose caller this page cites): `00201EB0` + 0x665 (call; `00201EB0` is cited on this page)
Other direct sites: `002002E0` + 0x4B9 (call); `002008F0` + 0x142 (call); `00201890` + 0x16B (call); `002161C0` + 0x1B8 (call)

Host context: "ply-accumulate). ## SWE2-EC7-32 update (2026-09-18) — '001A4250' 'vector<int>' insert (via '001A5B30'/'001A7850'/'001E1670')  '001A4250' (315 B) — reached through '001A5B30', '001A7850', '001E1670', '00201EB0', '0020AE70' and '0020AF10' — is the CRT 'vector<int>' insert the ta list builders share: room at '[rcx+8] != [rcx+0x10]' shifts the tail one element and writes in place; a full vector doubles capacity through the allocator's '+0x1"

```
001E0360  push     rbx
001E0362  sub      rsp, 0x30
001E0366  add      rcx, 0x18
001E036A  mov      dword ptr [rsp + 0x20], 0
001E0372  mov      rbx, rdx
001E0375  call     0x1e0100  ; -> 001E0100 fn
001E037A  mov      rax, rbx
001E037D  add      rsp, 0x30
001E0381  pop      rbx
001E0382  ret      
```

## 00465FF0 (120 B, extent 00465FF0-00466068)

Entered from (direct sites whose caller this page cites): `002F5550` + 0x1D9 (call; `002F5550` is cited on this page)
Other direct sites: none

Host context: "ERED 2026-09-25 (OPUS): the float is a track value of the map's tag-23 animation-slot family, on channel 9, and       its clock is that slot's time.**       - **What '+0x50' is.** The per-frame pass '002F5550' stores into the entry's '+0x50' the 0x130-byte slot record         that '00466CB0' matches ('002F57A3'-'002F57CE').       - **What '+0x90' is.** '004677A0' binds every track through '00466420(record, channel, &track+0xC)'. Channel"

```
00465FF0  xor      r8d, r8d
00465FF3  mov      eax, 1
00465FF8  sub      eax, dword ptr [rip + 0x2a55732]  ; -> 02EBB730
00465FFE  lea      rcx, [rax + rax*2]
00466002  lea      rax, [rip + 0x2a556f7]  ; -> 02EBB700
00466009  lea      rdx, [rax + rcx*8]
0046600D  mov      rax, qword ptr [rax + rcx*8 + 8]
00466012  lea      rcx, [rax + 0x10]
00466016  mov      qword ptr [rdx + 8], rcx
0046601A  mov      qword ptr [rax], 0x10000000
00466021  mov      qword ptr [rax + 8], r8
00466025  mov      dword ptr [rcx - 8], r8d
00466029  mov      dword ptr [rcx - 4], 0x10000000
00466030  mov      rcx, qword ptr [rdx + 8]
00466034  lea      rax, [rcx + 0x10]
00466038  mov      qword ptr [rdx + 8], rax
0046603C  mov      qword ptr [rcx], 0x70000000
00466043  mov      qword ptr [rcx + 8], r8
00466047  mov      ecx, 0x80000000
0046604C  mov      eax, dword ptr [rdx]
0046604E  and      eax, 0xfffffff
00466053  cmp      dword ptr [rdx + 0x14], r8d
00466057  je       0x46605c  ; -> 0046605C
00466059  or       rax, rcx
0046605C  test     ecx, eax
0046605E  jne      0x466067  ; -> 00466067
00466060  xor      ecx, ecx
00466062  jmp      0x16d6a0  ; -> 0016D6A0 fn
00466067  ret      
```

## 00466070 (126 B, extent 00466070-004660EE)

Entered from (direct sites whose caller this page cites): `002F5550` + 0x1CF (call; `002F5550` is cited on this page)
Other direct sites: none

Host context: "ERED 2026-09-25 (OPUS): the float is a track value of the map's tag-23 animation-slot family, on channel 9, and       its clock is that slot's time.**       - **What '+0x50' is.** The per-frame pass '002F5550' stores into the entry's '+0x50' the 0x130-byte slot record         that '00466CB0' matches ('002F57A3'-'002F57CE').       - **What '+0x90' is.** '004677A0' binds every track through '00466420(record, channel, &track+0xC)'. Channel"

```
00466070  mov      qword ptr [rsp + 8], rbx
00466075  push     rdi
00466076  sub      rsp, 0x20
0046607A  mov      rbx, rcx
0046607D  mov      edi, edx
0046607F  xor      ecx, ecx
00466081  call     0x5c5230  ; -> 005C5230 fn
00466086  mov      rcx, rax
00466089  xor      r8d, r8d
0046608C  xor      edx, edx
0046608E  call     0x5c5230  ; -> 005C5230 fn
00466093  mov      dword ptr [rip + 0x2a55693], 0  ; -> 02EBB730
0046609D  mov      rdx, rbx
004660A0  lea      rcx, [rip + 0x2a55659]  ; -> 02EBB700
004660A7  test     edi, edi
004660A9  js       0x4660d0  ; -> 004660D0
004660AB  mov      r8d, edi
004660AE  call     0x4fe420  ; -> 004FE420 fn
004660B3  lea      r8d, [rbx + rdi]
004660B7  mov      rdx, rbx
004660BA  lea      rcx, [rip + 0x2a55657]  ; -> 02EBB718
004660C1  mov      rbx, qword ptr [rsp + 0x30]
004660C6  add      rsp, 0x20
004660CA  pop      rdi
004660CB  jmp      0x4fe420  ; -> 004FE420 fn
004660D0  call     0x4fe3d0  ; -> 004FE3D0 fn
004660D5  mov      rdx, rbx
004660D8  lea      rcx, [rip + 0x2a55639]  ; -> 02EBB718
004660DF  mov      rbx, qword ptr [rsp + 0x30]
004660E4  add      rsp, 0x20
004660E8  pop      rdi
004660E9  jmp      0x4fe3d0  ; -> 004FE3D0 fn
```

## 004660F0 (38 B, extent 004660F0-00466116)

Entered from (direct sites whose caller this page cites): `002F5550` + 0x1D4 (call; `002F5550` is cited on this page)
Other direct sites: none

Host context: "ERED 2026-09-25 (OPUS): the float is a track value of the map's tag-23 animation-slot family, on channel 9, and       its clock is that slot's time.**       - **What '+0x50' is.** The per-frame pass '002F5550' stores into the entry's '+0x50' the 0x130-byte slot record         that '00466CB0' matches ('002F57A3'-'002F57CE').       - **What '+0x90' is.** '004677A0' binds every track through '00466420(record, channel, &track+0xC)'. Channel"

```
004660F0  mov      eax, 1
004660F5  lea      rdx, [rip + 0x2a55604]  ; -> 02EBB700
004660FC  sub      eax, dword ptr [rip + 0x2a5562e]  ; -> 02EBB730
00466102  mov      dword ptr [rip + 0x2a55628], eax  ; -> 02EBB730
00466108  lea      rcx, [rax + rax*2]
0046610C  mov      rax, qword ptr [rdx + rcx*8]
00466110  mov      qword ptr [rdx + rcx*8 + 8], rax
00466115  ret      
```

## 00466120 (28 B, extent 00466120-0046613C)

Entered from (direct sites whose caller this page cites): `002F5550` + 0x372 (call; `002F5550` is cited on this page)
Other direct sites: none

Host context: "ERED 2026-09-25 (OPUS): the float is a track value of the map's tag-23 animation-slot family, on channel 9, and       its clock is that slot's time.**       - **What '+0x50' is.** The per-frame pass '002F5550' stores into the entry's '+0x50' the 0x130-byte slot record         that '00466CB0' matches ('002F57A3'-'002F57CE').       - **What '+0x90' is.** '004677A0' binds every track through '00466420(record, channel, &track+0xC)'. Channel"

```
00466120  sub      rsp, 0x28
00466124  xor      ecx, ecx
00466126  call     0x5c5230  ; -> 005C5230 fn
0046612B  mov      rcx, rax
0046612E  xor      r8d, r8d
00466131  xor      edx, edx
00466133  add      rsp, 0x28
00466137  jmp      0x5c5230  ; -> 005C5230 fn
```

## 00466B80 (47 B, extent 00466B80-00466BAF)

Entered from (direct sites whose caller this page cites): `002F5550` + 0x22A (call; `002F5550` is cited on this page)
Other direct sites: none

Host context: "ERED 2026-09-25 (OPUS): the float is a track value of the map's tag-23 animation-slot family, on channel 9, and       its clock is that slot's time.**       - **What '+0x50' is.** The per-frame pass '002F5550' stores into the entry's '+0x50' the 0x130-byte slot record         that '00466CB0' matches ('002F57A3'-'002F57CE').       - **What '+0x90' is.** '004677A0' binds every track through '00466420(record, channel, &track+0xC)'. Channel"

```
00466B80  test     ecx, ecx
00466B82  js       0x466bac  ; -> 00466BAC
00466B84  cmp      ecx, dword ptr [rip + 0x2a54b56]  ; -> 02EBB6E0
00466B8A  jge      0x466bac  ; -> 00466BAC
00466B8C  movsxd   rax, ecx
00466B8F  lea      rcx, [rax + rax*4]
00466B93  shl      rcx, 4
00466B97  add      rcx, qword ptr [rip + 0x2a54b52]  ; -> 02EBB6F0
00466B9E  cmp      qword ptr [rcx + 8], 0
00466BA3  je       0x466bac  ; -> 00466BAC
00466BA5  mov      eax, dword ptr [rcx + 0x4c]
00466BA8  and      eax, 1
00466BAB  ret      
00466BAC  xor      eax, eax
00466BAE  ret      
```

## 00467940 (128 B, extent 00467940-004679C0)

Entered from (direct sites whose caller this page cites): `002F5550` + 0x560 (call; `002F5550` is cited on this page)
Other direct sites: none

Host context: "ERED 2026-09-25 (OPUS): the float is a track value of the map's tag-23 animation-slot family, on channel 9, and       its clock is that slot's time.**       - **What '+0x50' is.** The per-frame pass '002F5550' stores into the entry's '+0x50' the 0x130-byte slot record         that '00466CB0' matches ('002F57A3'-'002F57CE').       - **What '+0x90' is.** '004677A0' binds every track through '00466420(record, channel, &track+0xC)'. Channel"

```
00467940  movss    xmm5, dword ptr [rcx + 0x50]
00467945  xor      eax, eax
00467947  movd     xmm0, dword ptr [rcx + 0x44]
0046794C  movd     xmm2, dword ptr [rcx + 0x48]
00467951  cvtdq2ps xmm0, xmm0
00467954  mov      qword ptr [rcx + 4], rax
00467958  mov      qword ptr [rcx + 0xc], rax
0046795C  mov      qword ptr [rcx + 0x18], rax
00467960  mov      qword ptr [rcx + 0x20], rax
00467964  cvtdq2ps xmm2, xmm2
00467967  mulss    xmm0, dword ptr [rip + 0x1884201]  ; -> 01CEBB70 [f32 0.5]
0046796F  mulss    xmm2, dword ptr [rip + 0x498995]  ; -> 0090030C [f32 -0.5]
00467977  movss    dword ptr [rcx], xmm0
0046797B  movaps   xmm0, xmm5
0046797E  movss    dword ptr [rcx + 0x14], xmm2
00467983  subss    xmm0, dword ptr [rcx + 0x4c]
00467988  mov      dword ptr [rcx + 0x2c], eax
0046798B  mov      dword ptr [rcx + 0x30], 0x45000000
00467992  mov      dword ptr [rcx + 0x34], 0x45000000
00467999  mulss    xmm0, dword ptr [rip + 0x49896b]  ; -> 0090030C [f32 -0.5]
004679A1  movss    dword ptr [rcx + 0x28], xmm0
004679A6  addss    xmm5, dword ptr [rcx + 0x4c]
004679AB  mov      dword ptr [rcx + 0x3c], 0x3f800000
004679B2  mulss    xmm5, dword ptr [rip + 0x18841b6]  ; -> 01CEBB70 [f32 0.5]
004679BA  movss    dword ptr [rcx + 0x38], xmm5
004679BF  ret      
```
