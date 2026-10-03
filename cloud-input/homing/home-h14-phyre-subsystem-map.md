# Homing pack: `22-Middleware-PhyreEngine/Subsystem-Map/phyre-subsystem-map.md`

Generated 2026-10-03 15:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h14-phyre-subsystem-map.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00793410 (118 B, extent 00793410-00793486)

Entered from (direct sites whose caller this page cites): `007933C0` + 0x40 (jmp; `007933C0` is cited on this page)
Other direct sites: `00793F10` + 0x42 (call); `00793F80` + 0xF (call); `00793FC0` + 0x42 (call)

Host context: "F0' (4,745 B, Rendering), '005CCD00' (926 B, DebugUtils), '006A8A20' (320 B) and '006A8810' (270 B, Middleware), '006A0B60' (139 B) and '00691DB0' (64 B, Physics), '00646AB0' (81 B, PostProcessing), '007933C0', '00793570', '00793750', '007934E0' (Framework, 11–73 B), '005AA2C0', '005AA260', '005A9F00', '005A9E60' (Animation, 11–43 B), '006A91C0', '006A9280', '006A9150' (GameplayTrigger, 4–62 B), '0018D0E0' and '005DD660' (Rendering, 11 "

```
00793410  push     rdi
00793412  sub      rsp, 0x30
00793416  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0079341F  mov      qword ptr [rsp + 0x40], rbx
00793424  mov      rbx, rcx
00793427  lea      rax, [rip + 0x151f06a]  ; -> 01CB2498
0079342E  mov      qword ptr [rcx], rax
00793431  mov      eax, dword ptr [rcx + 8]
00793434  xor      edi, edi
00793436  test     eax, eax
00793438  je       0x793459  ; -> 00793459
0079343A  mov      rcx, qword ptr [rcx + 0x10]
0079343E  test     rcx, rcx
00793441  je       0x793452  ; -> 00793452
00793443  shr      eax, 0x1f
00793446  not      al
00793448  test     al, 1
0079344A  je       0x793452  ; -> 00793452
0079344C  call     0x584730  ; -> 00584730 fn
00793451  nop      
00793452  mov      qword ptr [rbx + 0x10], rdi
00793456  mov      dword ptr [rbx + 8], edi
00793459  mov      eax, dword ptr [rbx + 8]
0079345C  shr      eax, 0x1f
0079345F  not      al
00793461  test     al, 1
00793463  je       0x793474  ; -> 00793474
00793465  mov      rcx, qword ptr [rbx + 0x10]
00793469  test     rcx, rcx
0079346C  je       0x793474  ; -> 00793474
0079346E  call     0x584730  ; -> 00584730 fn
00793473  nop      
00793474  mov      qword ptr [rbx + 0x10], rdi
00793478  mov      dword ptr [rbx + 8], edi
0079347B  mov      rbx, qword ptr [rsp + 0x40]
00793480  add      rsp, 0x30
00793484  pop      rdi
00793485  ret      
```
