# Homing pack: `17-Presentation-Rendering/Render-Command-List/the-ordered-render-command-list.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-ordered-render-command-list.json`.

Bodies: 5. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001EBA90 (60 B, extent 001EBA90-001EBACC)

Entered from (direct sites whose caller this page cites): `001C6320` + 0x22C (call; `001C6320` is cited on this page)
Other direct sites: none

Host context: "ry across the layer boundary, no shared ownership. - **Developer - CLIENT and SERVICE (5 edges).** '001FE8B0', '00200B50', '00200BE0', '00796E20' are called by bodies filed to Developer: '001C2F50', '001C6320'; '0017D6E0' reaches bodies filed to Developer: '001C2F50' - shared machinery across the layer boundary, no shared ownership. - **Input - CLIENT and SERVICE (70 edges).** '00225570', '00265680', InputDevice_QueryAvailabilityState_A"

```
001EBA90  push     rbx
001EBA92  sub      rsp, 0x20
001EBA96  lea      rbx, [rcx + 0x40]
001EBA9A  movss    dword ptr [rcx + 0x250], xmm1
001EBAA2  mov      rax, qword ptr [rbx]
001EBAA5  mov      rcx, rbx
001EBAA8  movss    dword ptr [rbx + 0xd0], xmm1
001EBAB0  call     qword ptr [rax + 8]
001EBAB3  mov      rax, qword ptr [rbx]
001EBAB6  mov      rcx, rbx
001EBAB9  mov      dword ptr [rbx + 0xd4], 0x3f93cd3a
001EBAC3  add      rsp, 0x20
001EBAC7  pop      rbx
001EBAC8  jmp      qword ptr [rax + 8]
```

## 001EBBF0 (36 B, extent 001EBBF0-001EBC14)

Entered from (direct sites whose caller this page cites): `001C6320` + 0xE2 (call; `001C6320` is cited on this page); `001C6320` + 0x124 (call; `001C6320` is cited on this page)
Other direct sites: none

Host context: "ry across the layer boundary, no shared ownership. - **Developer - CLIENT and SERVICE (5 edges).** '001FE8B0', '00200B50', '00200BE0', '00796E20' are called by bodies filed to Developer: '001C2F50', '001C6320'; '0017D6E0' reaches bodies filed to Developer: '001C2F50' - shared machinery across the layer boundary, no shared ownership. - **Input - CLIENT and SERVICE (70 edges).** '00225570', '00265680', InputDevice_QueryAvailabilityState_A" / "ry across the layer boundary, no shared ownership. - **Developer - CLIENT and SERVICE (5 edges).** '001FE8B0', '00200B50', '00200BE0', '00796E20' are called by bodies filed to Developer: '001C2F50', '001C6320'; '0017D6E0' reaches bodies filed to Developer: '001C2F50' - shared machinery across the layer boundary, no shared ownership. - **Input - CLIENT and SERVICE (70 edges).** '00225570', '00265680', InputDevice_QueryAvailabilityState_A"

```
001EBBF0  mov      dword ptr [rcx + 0x12c], 0
001EBBFA  test     r8d, r8d
001EBBFD  je       0x1ebc13  ; -> 001EBC13
001EBBFF  movsxd   rax, edx
001EBC02  mov      dword ptr [rcx + rax*4 + 0x124], r8d
001EBC0A  lea      eax, [rdx + 1]
001EBC0D  mov      dword ptr [rcx + 0x12c], eax
001EBC13  ret      
```

## 00271E50 (155 B, extent 00271E50-00271EEB)

Entered from (direct sites whose caller this page cites): `002986E0` + 0x414 (call; `002986E0` is cited on this page)
Other direct sites: none

Host context: " the layer boundary, no shared ownership. - **UI - CLIENT and SERVICE (14 edges).** '00186660', '001867B0', '001867C0', '0018CD90' (+7 more) are called by bodies filed to UI: '0018EEE0', '00279E20', '002986E0', '00299090' (+2 more); '001F3300' reaches bodies filed to UI: '0018EEE0' - shared machinery across the layer boundary, no shared ownership. - **WorldAreaField - CLIENT and SERVICE (10 edges).** '00263660', '00265920', '002DEBA0', "

```
00271E50  mov      r10d, r8d
00271E53  mov      r11, rcx
00271E56  sar      r10d, 8
00271E5A  dec      edx
00271E5C  cmp      r10d, edx
00271E5F  jl       0x271e68  ; -> 00271E68
00271E61  movsxd   rax, edx
00271E64  mov      eax, dword ptr [rcx + rax*8]
00271E67  ret      
00271E68  test     r8d, r8d
00271E6B  jg       0x271e70  ; -> 00271E70
00271E6D  mov      eax, dword ptr [rcx]
00271E6F  ret      
00271E70  movzx    r9d, r8b
00271E74  movsxd   rax, r10d
00271E77  lea      r8, [rcx + rax*8]
00271E7B  lea      eax, [r10 + 1]
00271E7F  movsxd   rcx, eax
00271E82  movzx    eax, byte ptr [r8]
00271E86  lea      rdx, [r11 + rcx*8]
00271E8A  movzx    ecx, byte ptr [r11 + rcx*8]
00271E8F  sub      ecx, eax
00271E91  imul     ecx, r9d
00271E95  sar      ecx, 8
00271E98  add      cl, al
00271E9A  movzx    eax, byte ptr [r8 + 1]
00271E9F  mov      byte ptr [rsp + 0x10], cl
00271EA3  movzx    ecx, byte ptr [rdx + 1]
00271EA7  sub      ecx, eax
00271EA9  imul     ecx, r9d
00271EAD  sar      ecx, 8
00271EB0  add      cl, al
00271EB2  movzx    eax, byte ptr [r8 + 2]
00271EB7  mov      byte ptr [rsp + 0x11], cl
00271EBB  movzx    ecx, byte ptr [rdx + 2]
00271EBF  sub      ecx, eax
00271EC1  imul     ecx, r9d
00271EC5  sar      ecx, 8
00271EC8  add      cl, al
00271ECA  movzx    eax, byte ptr [r8 + 3]
00271ECF  mov      byte ptr [rsp + 0x12], cl
00271ED3  movzx    ecx, byte ptr [rdx + 3]
00271ED7  sub      ecx, eax
00271ED9  imul     ecx, r9d
00271EDD  sar      ecx, 8
00271EE0  add      cl, al
00271EE2  mov      byte ptr [rsp + 0x13], cl
00271EE6  mov      eax, dword ptr [rsp + 0x10]
00271EEA  ret      
```

## 00274870 (101 B, extent 00274870-002748D5)

Entered from (direct sites whose caller this page cites): `002986E0` + 0x3F2 (call; `002986E0` is cited on this page)
Other direct sites: none

Host context: " the layer boundary, no shared ownership. - **UI - CLIENT and SERVICE (14 edges).** '00186660', '001867B0', '001867C0', '0018CD90' (+7 more) are called by bodies filed to UI: '0018EEE0', '00279E20', '002986E0', '00299090' (+2 more); '001F3300' reaches bodies filed to UI: '0018EEE0' - shared machinery across the layer boundary, no shared ownership. - **WorldAreaField - CLIENT and SERVICE (10 edges).** '00263660', '00265920', '002DEBA0', "

```
00274870  mov      r10d, r8d
00274873  mov      r11, rcx
00274876  sar      r10d, 8
0027487A  test     r9d, r9d
0027487D  je       0x274891  ; -> 00274891
0027487F  lea      eax, [rdx - 1]
00274882  cmp      r10d, eax
00274885  jl       0x274899  ; -> 00274899
00274887  shl      edx, 8
0027488A  lea      eax, [rdx - 0x100]
00274890  ret      
00274891  test     r10d, r10d
00274894  jg       0x274899  ; -> 00274899
00274896  xor      eax, eax
00274898  ret      
00274899  movzx    ecx, r8b
0027489D  movsxd   rax, r10d
002748A0  test     r9d, r9d
002748A3  je       0x2748c0  ; -> 002748C0
002748A5  add      ecx, dword ptr [r11 + rax*8 + 4]
002748AA  cmp      ecx, 0x100
002748B0  jl       0x2748cc  ; -> 002748CC
002748B2  xor      ecx, ecx
002748B4  inc      r10d
002748B7  shl      r10d, 8
002748BB  lea      eax, [rcx + r10]
002748BF  ret      
002748C0  sub      ecx, dword ptr [r11 + rax*8 + 4]
002748C5  jns      0x2748cc  ; -> 002748CC
002748C7  xor      ecx, ecx
002748C9  dec      r10d
002748CC  shl      r10d, 8
002748D0  lea      eax, [rcx + r10]
002748D4  ret      
```

## 00360C00 (27 B, extent 00360C00-00360C1B)

Entered from (direct sites whose caller this page cites): `00341F90` + 0x1D (call; `00341F90` is cited on this page)
Other direct sites: none

Host context: " ownership. - **Script_VM_Native_Bridge - CLIENT and SERVICE (32 edges).** '001EC500', '001EC620', '00265680', '00265920' (+5 more) are called by bodies filed to Script_VM_Native_Bridge: '00341840', '00341F90', '003423E0', '00343690' (+27 more); '0034C7E0' reaches bodies filed to Script_VM_Native_Bridge: VMValueStack_PopInt32CoerceFloat32 ('00267E10') - shared machinery across the layer boundary, no shared ownership. - **UI - CLIENT and"

```
00360C00  test     ecx, ecx
00360C02  js       0x360c17  ; -> 00360C17
00360C04  movsxd   rax, ecx
00360C07  lea      rcx, [rax + rax*2]
00360C0B  lea      rax, [rip + 0x1f6adde]  ; -> 022CB9F0
00360C12  movzx    eax, byte ptr [rax + rcx*8]
00360C16  ret      
00360C17  or       eax, 0xffffffff
00360C1A  ret      
```
