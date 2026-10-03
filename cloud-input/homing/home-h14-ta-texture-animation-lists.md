# Homing pack: `02-Resource-And-Asset-Pipeline/Prefetch-And-Json-Data/ta-texture-animation-lists.md`

Generated 2026-10-03 15:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h14-ta-texture-animation-lists.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

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
