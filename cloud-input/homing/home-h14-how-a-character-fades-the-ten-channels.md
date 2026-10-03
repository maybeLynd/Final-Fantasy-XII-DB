# Homing pack: `17-Presentation-Rendering/Character-Render-Records/how-a-character-fades-the-ten-channels.md`

Generated 2026-10-03 15:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h14-how-a-character-fades-the-ten-channels.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

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
