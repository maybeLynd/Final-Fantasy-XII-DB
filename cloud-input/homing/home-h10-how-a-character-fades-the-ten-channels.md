# Homing pack: `17-Presentation-Rendering/Character-Render-Records/how-a-character-fades-the-ten-channels.md`

Generated 2026-10-03 12:18 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h10-how-a-character-fades-the-ten-channels.json`.

Bodies: 4. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 003F2580 (65 B, extent 003F2580-003F25C1)

Entered from (direct sites whose caller this page cites): `002915C0` + 0x15A (call; `002915C0` is cited on this page)
Other direct sites: none

Host context: "r the audit still reported for this page.*  **UI - MECHANICAL (24 edges).** Sixteen UI bodies call '00202C90', the 7-byte copy of one 16-byte vector that the '+0x2E0' hand-off tails into (among them '002915C0', '002C7660', '003F26F0', '003F9720' and '005528C0', and 11 more); seven call '00203170', the 44-byte store of a 4x4 identity matrix ('00247AE0', '002D2600', '002D28E0', '00368010', '003C5500', '003F26F0' and '003F2A70'); and '0024"

```
003F2580  mov      r8, rcx
003F2583  test     rcx, rcx
003F2586  jne      0x3f258c  ; -> 003F258C
003F2588  mov      rax, rdx
003F258B  ret      
003F258C  mov      rax, qword ptr [rcx + 0x9b0]
003F2593  test     rax, rax
003F2596  je       0x3f25af  ; -> 003F25AF
003F2598  nop      dword ptr [rax + rax]
003F25A0  mov      rcx, rax
003F25A3  mov      rax, qword ptr [rax + 0x9b0]
003F25AA  test     rax, rax
003F25AD  jne      0x3f25a0  ; -> 003F25A0
003F25AF  mov      qword ptr [rcx + 0x9b0], rdx
003F25B6  mov      rax, r8
003F25B9  mov      qword ptr [rdx + 0x9b8], rcx
003F25C0  ret      
```

## 003F2600 (234 B, extent 003F2600-003F26EA)

Entered from (direct sites whose caller this page cites): `002915C0` + 0x13F (call; `002915C0` is cited on this page)
Other direct sites: none

Host context: "r the audit still reported for this page.*  **UI - MECHANICAL (24 edges).** Sixteen UI bodies call '00202C90', the 7-byte copy of one 16-byte vector that the '+0x2E0' hand-off tails into (among them '002915C0', '002C7660', '003F26F0', '003F9720' and '005528C0', and 11 more); seven call '00203170', the 44-byte store of a 4x4 identity matrix ('00247AE0', '002D2600', '002D28E0', '00368010', '003C5500', '003F26F0' and '003F2A70'); and '0024"

```
003F2600  mov      qword ptr [rsp + 8], rbx
003F2605  push     rdi
003F2606  sub      rsp, 0x20
003F260A  mov      r9d, 0x20
003F2610  mov      rbx, rdx
003F2613  lea      rdx, [rcx + 0x3c0]
003F261A  mov      rdi, rcx
003F261D  lea      r8d, [r9 - 0x1a]
003F2621  call     0x3f2a70  ; -> 003F2A70 fn
003F2626  lea      rcx, [rdi + 0x780]
003F262D  mov      dword ptr [rdi + 0x998], 0x3f800000
003F2637  mov      rdx, rbx
003F263A  call     0x3f2f20  ; -> 003F2F20 fn
003F263F  lea      rcx, [rdi + 0x870]
003F2646  mov      rdx, rbx
003F2649  call     0x3f2f20  ; -> 003F2F20 fn
003F264E  mov      eax, dword ptr [rbx]
003F2650  mov      dword ptr [rdi + 0x970], eax
003F2656  movss    xmm0, dword ptr [rbx + 4]
003F265B  movaps   xmm1, xmm0
003F265E  mulss    xmm1, dword ptr [rip + 0x18f950a]  ; -> 01CEBB70 [f32 0.5]
003F2666  divss    xmm0, dword ptr [rip + 0x505b12]  ; -> 008F8180 [f32 10]
003F266E  subss    xmm1, xmm0
003F2672  movss    dword ptr [rdi + 0x974], xmm1
003F267A  mov      eax, dword ptr [rbx + 8]
003F267D  mov      dword ptr [rdi + 0x978], eax
003F2683  movss    xmm0, dword ptr [rbx + 4]
003F2688  movaps   xmm1, xmm0
003F268B  mulss    xmm1, dword ptr [rip + 0x18f94dd]  ; -> 01CEBB70 [f32 0.5]
003F2693  divss    xmm0, dword ptr [rip + 0x505ae5]  ; -> 008F8180 [f32 10]
003F269B  addss    xmm1, dword ptr [rbx + 0xc]
003F26A0  mov      rbx, qword ptr [rsp + 0x30]
003F26A5  mov      dword ptr [rdi + 0x924], 0x3e570a3d
003F26AF  mov      dword ptr [rdi + 0x92c], 0x3e4ccccd
003F26B9  mov      dword ptr [rdi + 0x930], 0x42fe0000
003F26C3  addss    xmm1, xmm0
003F26C7  mov      dword ptr [rdi + 0x934], 0x42fe0000
003F26D1  mov      qword ptr [rdi + 0x938], 0x42fe0000
003F26DC  movss    dword ptr [rdi + 0x97c], xmm1
003F26E4  add      rsp, 0x20
003F26E8  pop      rdi
003F26E9  ret      
```

## 00422F30 (65 B, extent 00422F30-00422F71)

Entered from (direct sites whose caller this page cites): `0041FBF0` + 0x6B (call; `0041FBF0` is cited on this page)
Other direct sites: none

Host context: "ancestor, ~~and the flag handed over with it says whether the whole chain is also unculled.~~  **Corrected 2026-09-19 (FABLE): bit 5 has no live source, so that second flag is always 0.** The setter '0041FBF0' (135 B, read whole) is called only by the propagation '00429D40' (271 B, read whole) and its descendant callback '0042DE50' (59 B): the value is **bit 2 of the requested-state word '+0x304'**, applied to the record, its child and "

```
00422F30  push     rbx
00422F32  sub      rsp, 0x20
00422F36  cmp      dword ptr [rcx + 0xc4], -1
00422F3D  mov      rbx, rcx
00422F40  je       0x422f6b  ; -> 00422F6B
00422F42  mov      ecx, dword ptr [rcx + 0x10]
00422F45  call     0x20e600  ; -> 0020E600 fn
00422F4A  mov      edx, dword ptr [rbx + 0xc4]
00422F50  mov      rcx, qword ptr [rax + 0xda8]
00422F57  call     0x51b9e0  ; -> 0051B9E0 fn
00422F5C  test     rax, rax
00422F5F  je       0x422f6b  ; -> 00422F6B
00422F61  and      dword ptr [rax + 0xc], 0xfffffffd
00422F65  xor      ecx, ecx
00422F67  mov      word ptr [rax + 0x24], cx
00422F6B  add      rsp, 0x20
00422F6F  pop      rbx
00422F70  ret      
```

## 00422F80 (68 B, extent 00422F80-00422FC4)

Entered from (direct sites whose caller this page cites): `0041FBF0` + 0x52 (call; `0041FBF0` is cited on this page)
Other direct sites: none

Host context: "ancestor, ~~and the flag handed over with it says whether the whole chain is also unculled.~~  **Corrected 2026-09-19 (FABLE): bit 5 has no live source, so that second flag is always 0.** The setter '0041FBF0' (135 B, read whole) is called only by the propagation '00429D40' (271 B, read whole) and its descendant callback '0042DE50' (59 B): the value is **bit 2 of the requested-state word '+0x304'**, applied to the record, its child and "

```
00422F80  push     rbx
00422F82  sub      rsp, 0x20
00422F86  cmp      dword ptr [rcx + 0xc4], -1
00422F8D  mov      rbx, rcx
00422F90  je       0x422fbe  ; -> 00422FBE
00422F92  mov      ecx, dword ptr [rcx + 0x10]
00422F95  call     0x20e600  ; -> 0020E600 fn
00422F9A  mov      edx, dword ptr [rbx + 0xc4]
00422FA0  mov      rcx, qword ptr [rax + 0xda8]
00422FA7  call     0x51b9e0  ; -> 0051B9E0 fn
00422FAC  test     rax, rax
00422FAF  je       0x422fbe  ; -> 00422FBE
00422FB1  or       dword ptr [rax + 0xc], 2
00422FB5  mov      ecx, 1
00422FBA  mov      word ptr [rax + 0x24], cx
00422FBE  add      rsp, 0x20
00422FC2  pop      rbx
00422FC3  ret      
```
