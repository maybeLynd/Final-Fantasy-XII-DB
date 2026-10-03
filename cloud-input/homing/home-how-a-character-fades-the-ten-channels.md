# Homing pack: `17-Presentation-Rendering/Character-Render-Records/how-a-character-fades-the-ten-channels.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-how-a-character-fades-the-ten-channels.json`.

Bodies: 5. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 003B3080 (27 B, extent 003B3080-003B309B)

Entered from (direct sites whose caller this page cites): `0042D830` + 0x62 (call; `0042D830` is cited on this page)
Other direct sites: none

Host context: "d was not established.~~ *The setter's two other callers, both record phases, ~~were~~* *~~not read~~.* *(answered: see the setter '003B33A0' has three callers, '0042CBF0'+0x330, '0042D7A0'+0x59 and '0042D830'+0x3A; '0042CBF0' is read whole in section 4a; 2026-10-02, OPUS)*  **The three bits, by their setters (added the same day; a displacement sweep finds one setter each).** **Bit 3 is "not culled this frame"**: '00421010' (29 B, read "

```
003B3080  mov      eax, ecx
003B3082  and      eax, 0x3f
003B3085  imul     rdx, rax, 0x38
003B3089  lea      rax, [rip + 0x2b0a3f0]  ; -> 02EBD480
003B3090  cmp      dword ptr [rdx + rax], ecx
003B3093  jne      0x3b309a  ; -> 003B309A
003B3095  or       byte ptr [rdx + rax + 0x30], 1
003B309A  ret      
```

## 003B3AA0 (109 B, extent 003B3AA0-003B3B0D)

Entered from (direct sites whose caller this page cites): `0042D830` + 0x57 (call; `0042D830` is cited on this page)
Other direct sites: none

Host context: "d was not established.~~ *The setter's two other callers, both record phases, ~~were~~* *~~not read~~.* *(answered: see the setter '003B33A0' has three callers, '0042CBF0'+0x330, '0042D7A0'+0x59 and '0042D830'+0x3A; '0042CBF0' is read whole in section 4a; 2026-10-02, OPUS)*  **The three bits, by their setters (added the same day; a displacement sweep finds one setter each).** **Bit 3 is "not culled this frame"**: '00421010' (29 B, read "

```
003B3AA0  mov      eax, ecx
003B3AA2  lea      r8, [rip + 0x2b099d7]  ; -> 02EBD480
003B3AA9  and      eax, 0x3f
003B3AAC  imul     rax, rax, 0x38
003B3AB0  cmp      dword ptr [rax + r8], ecx
003B3AB4  jne      0x3b3b0c  ; -> 003B3B0C
003B3AB6  mov      rax, qword ptr [rax + r8 + 0x10]
003B3ABB  test     rax, rax
003B3ABE  je       0x3b3b0c  ; -> 003B3B0C
003B3AC0  mov      ecx, 0x4000
003B3AC5  test     word ptr [rax + 0x368], cx
003B3ACC  je       0x3b3af7  ; -> 003B3AF7
003B3ACE  mov      dword ptr [rax + 0x320], 0x3f800000
003B3AD8  mov      dword ptr [rax + 0x324], 0x3f800000
003B3AE2  mov      dword ptr [rax + 0x328], 0x3f800000
003B3AEC  mov      dword ptr [rax + 0x32c], 0x3f800000
003B3AF6  ret      
003B3AF7  movaps   xmm0, xmmword ptr [rdx]
003B3AFA  movdqa   xmmword ptr [rax + 0x320], xmm0
003B3B02  mov      dword ptr [rax + 0x32c], 0x3f800000
003B3B0C  ret      
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

## 005213B0 (53 B, extent 005213B0-005213E5)

Entered from (direct sites whose caller this page cites): `0041EC00` + 0x128 (call; `0041EC00` is cited on this page)
Other direct sites: none

Host context: "iary handles - which is why a weapon never outlasts the hand that holds it.  ## 4b. The projected origin, and why channel 4's point is the camera  'CharacterRenderRecord_UpdateProjectedOriginState' ('0041EC00', 480 B), which a root record and an orphaned piece run (section 4a, step 1), was read whole, and it settles two things this page had left open.  It multiplies the record's world matrix '+0x180' by the matrix at **'02AEDDB0'** and "

```
005213B0  movss    xmm2, dword ptr [rdx]
005213B4  movss    xmm0, dword ptr [rdx + 4]
005213B9  subss    xmm0, dword ptr [rcx + 4]
005213BE  subss    xmm2, dword ptr [rcx]
005213C2  movss    xmm1, dword ptr [rdx + 8]
005213C7  subss    xmm1, dword ptr [rcx + 8]
005213CC  mulss    xmm0, xmm0
005213D0  mulss    xmm2, xmm2
005213D4  mulss    xmm1, xmm1
005213D8  addss    xmm0, xmm2
005213DC  addss    xmm0, xmm1
005213E0  jmp      0x861f14  ; -> 00861F14 fn
```
