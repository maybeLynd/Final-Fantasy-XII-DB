# F-interior pack: `17-Presentation-Rendering/Scripted-Camera/the-scripted-camera-player.md`

Generated 2026-10-02 09:51 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/the-scripted-camera-player.json`.

Functions: 15. Each is cited on the page only at its entry and is still in the F frontier.

## 00255C20 (40 B, extent 00255C20-00255C48)

Page context: "s     ('02096270'–'02096290'). Verb '0x34F' 'behindtoeventcamera' ('00349FA0') reaches the starter '00255C50' through     '003DA300'. The sync verb '0x350' ('0034A530') polls it through '00255CB0' / '00255C20', and it uses the same     easing function.   - **The easing function '00256650'** maps progress 't':     - mode 0: '(sin(πt − π/2) + 1) / 2', ease in and out;     - mode 1: 'sin(πt/2 − π/2) + 1', ease in;     - mode 2: 'sin(πt/2)'"

```
00255C20  movss    xmm1, dword ptr [rip + 0x1e40648]  ; -> 02096270
00255C28  movss    xmm0, dword ptr [rip + 0x1e40644]  ; -> 02096274
00255C30  comiss   xmm0, xmm1
00255C33  jae      0x255c42  ; -> 00255C42
00255C35  xorps    xmm0, xmm0
00255C38  ucomiss  xmm1, xmm0
00255C3B  jp       0x255c3f  ; -> 00255C3F
00255C3D  je       0x255c42  ; -> 00255C42
00255C3F  xor      eax, eax
00255C41  ret      
00255C42  mov      eax, 1
00255C47  ret      
```

## 00255C50 (92 B, extent 00255C50-00255CAC)

Page context: "578B0'.   - **'00255850' is the "behind to event camera" blend,** the same machine on its own globals     ('02096270'–'02096290'). Verb '0x34F' 'behindtoeventcamera' ('00349FA0') reaches the starter '00255C50' through     '003DA300'. The sync verb '0x350' ('0034A530') polls it through '00255CB0' / '00255C20', and it uses the same     easing function.   - **The easing function '00256650'** maps progress 't':     - mode 0: '(sin(πt − π/2)"

```
00255C50  sub      rsp, 0x28
00255C54  mov      eax, dword ptr [rsp + 0x50]
00255C58  xorps    xmm0, xmm0
00255C5B  mov      dword ptr [rip + 0x1e4061b], eax  ; -> 0209627C
00255C61  xor      eax, eax
00255C63  mov      dword ptr [rip + 0x1e4061b], ecx  ; -> 02096284
00255C69  lea      rcx, [rip + 0x1e40620]  ; -> 02096290
00255C70  mov      word ptr [rip + 0x1e406e9], ax  ; -> 02096360
00255C77  movss    dword ptr [rip + 0x1e405f1], xmm2  ; -> 02096270
00255C7F  movss    dword ptr [rip + 0x1e405ed], xmm0  ; -> 02096274
00255C87  mov      dword ptr [rip + 0x1e405ea], r9d  ; -> 02096278
00255C8E  mov      dword ptr [rip + 0x1e405ec], edx  ; -> 02096280
00255C94  call     0x3cbff0  ; -> 003CBFF0 fn
00255C99  lea      rax, [rip + 0x1e406d0]  ; -> 02096370
00255CA0  mov      qword ptr [rip + 0x1e40749], rax  ; -> 020963F0
00255CA7  add      rsp, 0x28
00255CAB  ret      
```

## 00255CB0 (53 B, extent 00255CB0-00255CE5)

Page context: "ts own globals     ('02096270'–'02096290'). Verb '0x34F' 'behindtoeventcamera' ('00349FA0') reaches the starter '00255C50' through     '003DA300'. The sync verb '0x350' ('0034A530') polls it through '00255CB0' / '00255C20', and it uses the same     easing function.   - **The easing function '00256650'** maps progress 't':     - mode 0: '(sin(πt − π/2) + 1) / 2', ease in and out;     - mode 1: 'sin(πt/2 − π/2) + 1', ease in;     - mode 2"

```
00255CB0  movss    xmm1, dword ptr [rip + 0x1e405b8]  ; -> 02096270
00255CB8  movss    xmm0, dword ptr [rip + 0x1e405b4]  ; -> 02096274
00255CC0  comiss   xmm0, xmm1
00255CC3  jae      0x255ce4  ; -> 00255CE4
00255CC5  xorps    xmm0, xmm0
00255CC8  ucomiss  xmm1, xmm0
00255CCB  jp       0x255ccf  ; -> 00255CCF
00255CCD  je       0x255ce4  ; -> 00255CE4
00255CCF  subss    xmm1, dword ptr [rip + 0x1a95ed1]  ; -> 01CEBBA8 [f32 1]
00255CD7  movss    dword ptr [rip + 0x1e40595], xmm1  ; -> 02096274
00255CDF  jmp      0x255850  ; -> 00255850 fn
00255CE4  ret      
```

## 00257800 (40 B, extent 00257800-00257828)

Page context: "cord ('002593A0')       ('00257583'–'00257618'). It wraps the yaw difference into '[−π, π]' ('00257654'–'00257691').     - Verb '0x1E5' 'resumebehindcamerasync' ('003445E0') polls completion through '00257800', or advances the blend       through '002578B0'.   - **'00255850' is the "behind to event camera" blend,** the same machine on its own globals     ('02096270'–'02096290'). Verb '0x34F' 'behindtoeventcamera' ('00349FA0') reaches th"

```
00257800  movss    xmm1, dword ptr [rip + 0x1e3ebf0]  ; -> 020963F8
00257808  movss    xmm0, dword ptr [rip + 0x1e3ebec]  ; -> 020963FC
00257810  comiss   xmm0, xmm1
00257813  jae      0x257822  ; -> 00257822
00257815  xorps    xmm0, xmm0
00257818  ucomiss  xmm1, xmm0
0025781B  jp       0x25781f  ; -> 0025781F
0025781D  je       0x257822  ; -> 00257822
0025781F  xor      eax, eax
00257821  ret      
00257822  mov      eax, 1
00257827  ret      
```

## 002578B0 (53 B, extent 002578B0-002578E5)

Page context: " It wraps the yaw difference into '[−π, π]' ('00257654'–'00257691').     - Verb '0x1E5' 'resumebehindcamerasync' ('003445E0') polls completion through '00257800', or advances the blend       through '002578B0'.   - **'00255850' is the "behind to event camera" blend,** the same machine on its own globals     ('02096270'–'02096290'). Verb '0x34F' 'behindtoeventcamera' ('00349FA0') reaches the starter '00255C50' through     '003DA300'. The"

```
002578B0  movss    xmm1, dword ptr [rip + 0x1e3eb40]  ; -> 020963F8
002578B8  movss    xmm0, dword ptr [rip + 0x1e3eb3c]  ; -> 020963FC
002578C0  comiss   xmm0, xmm1
002578C3  jae      0x2578e4  ; -> 002578E4
002578C5  xorps    xmm0, xmm0
002578C8  ucomiss  xmm1, xmm0
002578CB  jp       0x2578cf  ; -> 002578CF
002578CD  je       0x2578e4  ; -> 002578E4
002578CF  subss    xmm1, dword ptr [rip + 0x1a942d1]  ; -> 01CEBBA8 [f32 1]
002578D7  movss    dword ptr [rip + 0x1e3eb1d], xmm1  ; -> 020963FC
002578DF  jmp      0x257520  ; -> 00257520 fn
002578E4  ret      
```

## 00257AA0 (35 B, extent 00257AA0-00257AC3)

Page context: "ld the view** into '+0x210' — '003CC000' in path-follow (up vector '+0x110'), else    '003CC080' ('003CC970' only when '+0x188' is set, which only the 'debug_cameraescape' verb    does, '0050CD30' → '00257AA0'; no shipped script uses it) — and store 'fov', '1 / tan(fov / 2)'.  In **mode 1** (the hit check) step 4 is replaced by a probe '00230B60(actor, eye, target)'; '*out = 1' when it returns non-negative. '002567E0' runs the shot on t"

```
00257AA0  movsxd   rax, ecx
00257AA3  imul     r9, rax, 0xbb0
00257AAA  movsxd   rax, edx
00257AAD  imul     rcx, rax, 0x2e0
00257AB4  lea      rax, [rip + 0x1e3aefd]  ; -> 020929B8
00257ABB  add      r9, rcx
00257ABE  mov      byte ptr [r9 + rax], r8b
00257AC2  ret      
```

## 0025A3B0 (24 B, extent 0025A3B0-0025A3C8)

Page context: "are '0, 0, 1' in 7,609 of 7,614 keys.  ### 2.8 Handing the view to the camera stack  '002555D0', per frame, walks every player (5 slots × 4 channels). For each with a frame ('+0x184 != -1') it calls '0025A3B0(frame, 5, &player.view)': frame 0 copies the view into **camera record 5** ('CameraRecord_CopyViewState', '0025A2C0'; records at '02097300', stride '0x110') and sets its mode to 3 ('0025A500'); frame 1 copies into a separate view a"

```
0025A3B0  mov      eax, edx
0025A3B2  test     ecx, ecx
0025A3B4  jne      0x25a3c0  ; -> 0025A3C0
0025A3B6  mov      rdx, r8
0025A3B9  mov      ecx, eax
0025A3BB  jmp      0x25a2c0  ; -> 0025A2C0 fn
0025A3C0  mov      rcx, r8
0025A3C3  jmp      0x25a3d0  ; -> 0025A3D0 fn
```

## 0025A4A0 (42 B, extent 0025A4A0-0025A4CA)

Page context: "1D0 byte[64]  targetAttach  matrix +0x210 byte[208] view          copied to camera record 5 '''  **Two debug verbs write camera record 1 directly (added 2026-09-19, FABLE; four bodies read whole).** '0025A4A0' (42 B) stores three floats and 'w' = 1.0 at a camera record's '+0x00' - the **source eye** - and '0025A4D0' (43 B) does the same at '+0x10', the **source target**; both index 'g_cameraRecords' by their first argument. Each has exa"

```
0025A4A0  movsxd   rax, ecx
0025A4A3  imul     rcx, rax, 0x110
0025A4AA  lea      rax, [rip + 0x1e3ce4f]  ; -> 02097300
0025A4B1  add      rcx, rax
0025A4B4  movss    dword ptr [rcx], xmm1
0025A4B8  movss    dword ptr [rcx + 4], xmm2
0025A4BD  movss    dword ptr [rcx + 8], xmm3
0025A4C2  mov      dword ptr [rcx + 0xc], 0x3f800000
0025A4C9  ret      
```

## 0025A4D0 (43 B, extent 0025A4D0-0025A4FB)

Page context: " verbs write camera record 1 directly (added 2026-09-19, FABLE; four bodies read whole).** '0025A4A0' (42 B) stores three floats and 'w' = 1.0 at a camera record's '+0x00' - the **source eye** - and '0025A4D0' (43 B) does the same at '+0x10', the **source target**; both index 'g_cameraRecords' by their first argument. Each has exactly one caller, a script verb handler that pops three numbers and tail-jumps with **the record index fixed "

```
0025A4D0  movsxd   rax, ecx
0025A4D3  imul     rcx, rax, 0x110
0025A4DA  lea      rax, [rip + 0x1e3ce1f]  ; -> 02097300
0025A4E1  add      rcx, rax
0025A4E4  movss    dword ptr [rcx + 0x10], xmm1
0025A4E9  movss    dword ptr [rcx + 0x14], xmm2
0025A4EE  movss    dword ptr [rcx + 0x18], xmm3
0025A4F3  mov      dword ptr [rcx + 0x1c], 0x3f800000
0025A4FA  ret      
```

## 00341AB0 (99 B, extent 00341AB0-00341B13)

Page context: "**Script_VM_Native_Bridge - CLIENT and SERVICE (112 edges).** '00203170', '00255C20', '00255CB0', '00257800' (+20 more) are called by bodies filed to Script_VM_Native_Bridge: '0033F7F0', '0033FD60', '00341AB0', '00342490' (+71 more); '003442D0', '00349FA0', '0034E9B0', '0034EDB0' (+13 more) reach bodies filed to Script_VM_Native_Bridge: VMValueStack_PopNumericDiscard ('00267DB0'), VMValueStack_PopInt32CoerceFloat32 ('00267E10'), VMValue"

```
00341AB0  mov      qword ptr [rsp + 8], rbx
00341AB5  push     rdi
00341AB6  sub      rsp, 0x30
00341ABA  mov      rcx, r9
00341ABD  movaps   xmmword ptr [rsp + 0x20], xmm6
00341AC2  mov      rbx, r8
00341AC5  mov      rdi, rdx
00341AC8  call     0x267db0  ; -> 00267DB0 fn
00341ACD  call     0x3a1c50  ; -> 003A1C50 fn
00341AD2  movaps   xmm1, xmm0
00341AD5  mov      rcx, rdi
00341AD8  movaps   xmm6, xmm0
00341ADB  call     0x26c090  ; -> 0026C090 fn
00341AE0  mov      rcx, rdi
00341AE3  call     0x265200  ; -> 00265200 fn
00341AE8  movaps   xmm1, xmm0
00341AEB  mov      rcx, rdi
00341AEE  call     0x26c290  ; -> 0026C290 fn
00341AF3  mov      edx, 3
00341AF8  movss    dword ptr [rbx], xmm6
00341AFC  mov      rcx, rdi
00341AFF  mov      rbx, qword ptr [rsp + 0x40]
00341B04  movaps   xmm6, xmmword ptr [rsp + 0x20]
00341B09  add      rsp, 0x30
00341B0D  pop      rdi
00341B0E  jmp      0x26c120  ; -> 0026C120 fn
```

## 003445E0 (48 B, extent 003445E0-00344610)

Page context: "tion fields toward the live camera record ('002593A0')       ('00257583'–'00257618'). It wraps the yaw difference into '[−π, π]' ('00257654'–'00257691').     - Verb '0x1E5' 'resumebehindcamerasync' ('003445E0') polls completion through '00257800', or advances the blend       through '002578B0'.   - **'00255850' is the "behind to event camera" blend,** the same machine on its own globals     ('02096270'–'02096290'). Verb '0x34F' 'behindt"

```
003445E0  sub      rsp, 0x28
003445E4  movzx    ecx, byte ptr [rdx + 0x15]
003445E8  call     0x267310  ; -> 00267310 fn
003445ED  test     eax, eax
003445EF  je       0x3445fd  ; -> 003445FD
003445F1  call     0x2578b0  ; -> 002578B0 fn
003445F6  xor      eax, eax
003445F8  add      rsp, 0x28
003445FC  ret      
003445FD  call     0x257800  ; -> 00257800 fn
00344602  xor      ecx, ecx
00344604  test     eax, eax
00344606  sete     cl
00344609  mov      eax, ecx
0034460B  add      rsp, 0x28
0034460F  ret      
```

## 0034A530 (48 B, extent 0034A530-0034A560)

Page context: "lend,** the same machine on its own globals     ('02096270'–'02096290'). Verb '0x34F' 'behindtoeventcamera' ('00349FA0') reaches the starter '00255C50' through     '003DA300'. The sync verb '0x350' ('0034A530') polls it through '00255CB0' / '00255C20', and it uses the same     easing function.   - **The easing function '00256650'** maps progress 't':     - mode 0: '(sin(πt − π/2) + 1) / 2', ease in and out;     - mode 1: 'sin(πt/2 − π/2"

```
0034A530  sub      rsp, 0x28
0034A534  movzx    ecx, byte ptr [rdx + 0x15]
0034A538  call     0x267310  ; -> 00267310 fn
0034A53D  test     eax, eax
0034A53F  je       0x34a54d  ; -> 0034A54D
0034A541  call     0x255cb0  ; -> 00255CB0 fn
0034A546  xor      eax, eax
0034A548  add      rsp, 0x28
0034A54C  ret      
0034A54D  call     0x255c20  ; -> 00255C20 fn
0034A552  xor      ecx, ecx
0034A554  test     eax, eax
0034A556  sete     cl
0034A559  mov      eax, ecx
0034A55B  add      rsp, 0x28
0034A55F  ret      
```

## 00350660 (59 B, extent 00350660-0035069B)

Page context: ", frame 0 | | 'camerastart_7d(ch, entry, frame)' | '0034F2F0' | '003DA400' | play on 'ch', the given frame (scripts pass 'getcamerasubframe()') | | 'camerastop()' (channel 0) / 'camerastop_54(ch)' | '00350660' / '003502E0' | '003DA4D0' | channel state ← 0 | | 'camerachange(ch)' | '00351C00' | '003DA570' | the channel's frame is driven by 'ch' | | 'cameraclear()' | '00351540' | '003DA000' | both frames unowned, all four channels idle | |"

```
00350660  mov      qword ptr [rsp + 8], rbx
00350665  push     rdi
00350666  sub      rsp, 0x20
0035066A  xor      edx, edx
0035066C  mov      rcx, r9
0035066F  mov      rdi, r9
00350672  call     0x267f90  ; -> 00267F90 fn
00350677  call     0x2640c0  ; -> 002640C0 fn
0035067C  mov      rcx, rdi
0035067F  mov      rbx, rax
00350682  call     0x267e10  ; -> 00267E10 fn
00350687  mov      edx, eax
00350689  mov      rcx, rbx
0035068C  mov      rbx, qword ptr [rsp + 0x30]
00350691  add      rsp, 0x20
00350695  pop      rdi
00350696  jmp      0x3da4d0  ; -> 003DA4D0 fn
```

## 00350B00 (73 B, extent 00350B00-00350B49)

Page context: "the channel's frame is driven by 'ch' | | 'cameraclear()' | '00351540' | '003DA000' | both frames unowned, all four channels idle | | 'cameraratio(rate)' / 'cameraratio_115(ch, rate)' | '00351190' / '00350B00' | '003DA2D0' | channel '+0x10' rate | | 'camerahitcheck(entry)' / 'camerahitcheck_33c' | '0034EDB0' / '0034E9B0' | '003DA330' → '002567E0' | dry-run the shot; 1 if a probe hits |  The entry number is the low 24 bits of the script "

```
00350B00  mov      qword ptr [rsp + 8], rbx
00350B05  push     rdi
00350B06  sub      rsp, 0x30
00350B0A  movaps   xmmword ptr [rsp + 0x20], xmm6
00350B0F  mov      rdi, r9
00350B12  call     0x2640c0  ; -> 002640C0 fn
00350B17  mov      rcx, rdi
00350B1A  mov      rbx, rax
00350B1D  call     0x267db0  ; -> 00267DB0 fn
00350B22  mov      rcx, rdi
00350B25  movaps   xmm6, xmm0
00350B28  call     0x267e10  ; -> 00267E10 fn
00350B2D  movaps   xmm2, xmm6
00350B30  mov      edx, eax
00350B32  mov      rcx, rbx
00350B35  mov      rbx, qword ptr [rsp + 0x40]
00350B3A  movaps   xmm6, xmmword ptr [rsp + 0x20]
00350B3F  add      rsp, 0x30
00350B43  pop      rdi
00350B44  jmp      0x3da2d0  ; -> 003DA2D0 fn
```

## 00351190 (109 B, extent 00351190-003511FD)

Page context: "'003DA570' | the channel's frame is driven by 'ch' | | 'cameraclear()' | '00351540' | '003DA000' | both frames unowned, all four channels idle | | 'cameraratio(rate)' / 'cameraratio_115(ch, rate)' | '00351190' / '00350B00' | '003DA2D0' | channel '+0x10' rate | | 'camerahitcheck(entry)' / 'camerahitcheck_33c' | '0034EDB0' / '0034E9B0' | '003DA330' → '002567E0' | dry-run the shot; 1 if a probe hits |  The entry number is the low 24 bits o"

```
00351190  mov      qword ptr [rsp + 8], rbx
00351195  push     rdi
00351196  sub      rsp, 0x30
0035119A  mov      rcx, r9
0035119D  movaps   xmmword ptr [rsp + 0x20], xmm6
003511A2  mov      rdi, r9
003511A5  call     0x267e10  ; -> 00267E10 fn
003511AA  xor      edx, edx
003511AC  mov      rcx, rdi
003511AF  movd     xmm6, eax
003511B3  cvtdq2ps xmm6, xmm6
003511B6  call     0x267f90  ; -> 00267F90 fn
003511BB  mov      rcx, rdi
003511BE  movaps   xmm1, xmm6
003511C1  call     0x267f60  ; -> 00267F60 fn
003511C6  call     0x2640c0  ; -> 002640C0 fn
003511CB  mov      rcx, rdi
003511CE  mov      rbx, rax
003511D1  call     0x267db0  ; -> 00267DB0 fn
003511D6  mov      rcx, rdi
003511D9  movaps   xmm6, xmm0
003511DC  call     0x267e10  ; -> 00267E10 fn
003511E1  movaps   xmm2, xmm6
003511E4  mov      edx, eax
003511E6  mov      rcx, rbx
003511E9  mov      rbx, qword ptr [rsp + 0x40]
003511EE  movaps   xmm6, xmmword ptr [rsp + 0x20]
003511F3  add      rsp, 0x30
003511F7  pop      rdi
003511F8  jmp      0x3da2d0  ; -> 003DA2D0 fn
```
