# Homing pack: `99-Unresolved-Residual/the-blinking-icon-and-its-atlas.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-blinking-icon-and-its-atlas.json`.

Bodies: 4. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00247980 (47 B, extent 00247980-002479AF)

Entered from (direct sites whose caller this page cites): `00228130` + 0x1A6 (call; `00228130` is cited on this page)
Other direct sites: none

Host context: "mber of 60 Hz vblanks each presented frame spans — and only while the frame argument '02064AA0' is zero ([the frame page](../22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md)); '00228130' re-bases it from '[01FD46F4]' on message 18. So 'sin(counter × π / 30)' completes a cycle every 60 ticks: **one second at 60 Hz whatever the present interval**, which is what a blink cadence needs. *(Previously: not established he"

```
00247980  mov      rax, rdx
00247983  test     rdx, rdx
00247986  je       0x2479ae  ; -> 002479AE
00247988  cmp      qword ptr [rdx + 0x10], 0
0024798D  jne      0x2479a3  ; -> 002479A3
0024798F  and      dword ptr [rdx + 0x40], 0xfffffffd
00247993  and      r8d, 1
00247997  add      r8d, r8d
0024799A  or       dword ptr [rdx + 0x40], r8d
0024799E  jmp      0x248220  ; -> 00248220 fn
002479A3  mov      edx, r8d
002479A6  mov      rcx, rax
002479A9  jmp      0x247870  ; -> 00247870 fn
002479AE  ret      
```

## 00264420 (58 B, extent 00264420-0026445A)

Entered from (direct sites whose caller this page cites): `00345430` + 0x3C (call; `00345430` is cited on this page)
Other direct sites: `00345CD0` + 0x89 (call)

Host context: "180' calls '00265200', 'Actor_SetDesiredMovementHeading' ('0026A0D0'), '0026B0C0', 'Actor_SetFacingHeading_Variant1' ('0026B620') and 1 more; 'VMValueStack_PushFloat32Bits' ('00267F60') is called by '00345430', '003488B0', '00349680', '003548B0'; '0026A870' is called by '002EBFA0', '002EC140', '002EC1C0', '002EC2C0'; '003A1D30' is called by 'Movement_ComputeDeltaFromHeadingSpeed' ('002E4380'), 'Movement_UpdateSteeringTowardTarget' ('002"

```
00264420  sub      rsp, 0x28
00264424  mov      rax, qword ptr [rcx + 0xc0]
0026442B  test     rax, rax
0026442E  je       0x264447  ; -> 00264447
00264430  movzx    edx, byte ptr [rax + 0x154]
00264437  test     dl, 2
0026443A  je       0x264447  ; -> 00264447
0026443C  movzx    eax, dl
0026443F  and      eax, 1
00264442  add      rsp, 0x28
00264446  ret      
00264447  call     0x30bfb0  ; -> 0030BFB0 fn
0026444C  xor      ecx, ecx
0026444E  test     eax, eax
00264450  setne    cl
00264453  mov      eax, ecx
00264455  add      rsp, 0x28
00264459  ret      
```

## 002644E0 (43 B, extent 002644E0-0026450B)

Entered from (direct sites whose caller this page cites): `00340480` + 0x23 (call; `00340480` is cited on this page); `00340BE0` + 0x23 (call; `00340BE0` is cited on this page); `00342040` + 0x23 (call; `00342040` is cited on this page)
Other direct sites: `00349F10` + 0x23 (call); `0034FFF0` + 0x23 (call); `00356740` + 0x23 (call); `00356AF0` + 0x30 (call); `00356F20` + 0x30 (call)

Host context: "ore; '00264010' is called by '00341410', '00343D10', '00344390', '003448F0' and 30 more; 'VMValueStack_PushFloat32Bits' ('00267F60') is called by 'WorldActorScriptVM_InterpretBytecode' ('0025E4C0'), '00340480', '00340BE0', '00342040' and 30 more; '0026A1A0' is called by '0033F270', '0033F770', '0033FBA0', '00340480' and 25 more; 'Actor_GetWorldPosition' ('00265020') is called by '0033FD60', '00344AF0', '00345180', '00345830' and 19 more" / "10' is called by '00341410', '00343D10', '00344390', '003448F0' and 30 more; 'VMValueStack_PushFloat32Bits' ('00267F60') is called by 'WorldActorScriptVM_InterpretBytecode' ('0025E4C0'), '00340480', '00340BE0', '00342040' and 30 more; '0026A1A0' is called by '0033F270', '0033F770', '0033FBA0', '00340480' and 25 more; 'Actor_GetWorldPosition' ('00265020') is called by '0033FD60', '00344AF0', '00345180', '00345830' and 19 more; '003A19A0'"

```
002644E0  movzx    eax, byte ptr [rcx + 3]
002644E4  and      al, 0xe0
002644E6  cmp      al, 0x60
002644E8  je       0x2644fb  ; -> 002644FB
002644EA  movss    xmm0, dword ptr [rip + 0x1b99bca]  ; -> 01DFE0BC [f32 1]
002644F2  mulss    xmm0, dword ptr [rip + 0x6b122e]  ; -> 00915728 [f32 0.2094395]
002644FA  ret      
002644FB  mov      rax, qword ptr [rcx + 0xb8]
00264502  movss    xmm0, dword ptr [rax + 0xb0]
0026450A  ret      
```

## 0037FA00 (116 B, extent 0037FA00-0037FA74)

Entered from (direct sites whose caller this page cites): `0037F4D0` + 0x47 (call; `0037F4D0` is cited on this page)
Other direct sites: none

Host context: "; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).  **Resource — SERVICE (SWE2-EC7-158, 4 edges).** Batch-123's '0037FBA0' matcher is called by '0037F4D0', which — with '0029CED0'/'002B7B80' — calls the resource layer's '00249210'/'00249580'; the atlas's callers consult shared helpers, fan-in only.  - **Presentation — CLIENT (SWE2-EC7-164, 90 edges, one fan-in).** The '00184950'/'00"

```
0037FA00  mov      qword ptr [rsp + 0x10], rsi
0037FA05  push     rdi
0037FA06  sub      rsp, 0x20
0037FA0A  mov      rsi, rcx
0037FA0D  xor      edi, edi
0037FA0F  mov      rcx, qword ptr [rcx + 0xc8]
0037FA16  test     rcx, rcx
0037FA19  je       0x37fa27  ; -> 0037FA27
0037FA1B  call     0x3697f0  ; -> 003697F0 fn
0037FA20  mov      qword ptr [rsi + 0xc8], rdi
0037FA27  movzx    eax, byte ptr [rsi + 0xee]
0037FA2E  test     al, al
0037FA30  je       0x37fa69  ; -> 0037FA69
0037FA32  mov      qword ptr [rsp + 0x30], rbx
0037FA37  lea      rbx, [rsi + 0xf0]
0037FA3E  nop      
0037FA40  mov      rcx, qword ptr [rbx + 0x10]
0037FA44  call     0x3697f0  ; -> 003697F0 fn
0037FA49  mov      byte ptr [rbx], 0
0037FA4C  lea      rbx, [rbx + 0x18]
0037FA50  movzx    eax, byte ptr [rsi + 0xee]
0037FA57  inc      edi
0037FA59  cmp      edi, eax
0037FA5B  jl       0x37fa40  ; -> 0037FA40
0037FA5D  mov      rbx, qword ptr [rsp + 0x30]
0037FA62  mov      byte ptr [rsi + 0xee], 0
0037FA69  mov      rsi, qword ptr [rsp + 0x38]
0037FA6E  add      rsp, 0x20
0037FA72  pop      rdi
0037FA73  ret      
```
