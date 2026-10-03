# F homing pack (FABLE): `18-Audio/how-the-music-changes-when-you-change-area.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 00347310 (128 B, extent 00347310-00347390)

Documented callee on this page: `003614C0`

```
00347310  mov      qword ptr [rsp + 8], rbx
00347315  push     rdi
00347316  sub      rsp, 0x20
0034731A  movzx    eax, byte ptr [r8 + 3]
0034731F  mov      rdi, r8
00347322  test     al, al
00347324  js       0x347332  ; -> 00347332
00347326  mov      ecx, 1
0034732B  call     0x2f1a30  ; -> 002F1A30 fn
00347330  jmp      0x34737c  ; -> 0034737C
00347332  shl      al, 2
00347335  movsx    ecx, al
00347338  sar      ecx, 2
0034733B  test     ecx, ecx
0034733D  je       0x347353  ; -> 00347353
0034733F  cmp      ecx, 1
00347342  je       0x347377  ; -> 00347377
00347344  xor      ebx, ebx
00347346  mov      eax, ebx
00347348  mov      rbx, qword ptr [rsp + 0x30]
0034734D  add      rsp, 0x20
00347351  pop      rdi
00347352  ret      
00347353  movsx    r8d, byte ptr [r8 + 2]
00347358  mov      ebx, 1
0034735D  movsx    ecx, word ptr [rdi]
00347360  mov      edx, dword ptr [rdi + 8]
00347363  sar      r8d, 4
00347367  call     0x3614c0  ; -> 003614C0 fn
0034736C  test     eax, eax
0034736E  je       0x347383  ; -> 00347383
00347370  and      byte ptr [rdi + 3], 0xc1
00347374  or       byte ptr [rdi + 3], bl
00347377  call     0x360d60  ; -> 00360D60 fn
0034737C  xor      ebx, ebx
0034737E  test     eax, eax
00347380  setne    bl
00347383  mov      eax, ebx
00347385  mov      rbx, qword ptr [rsp + 0x30]
0034738A  add      rsp, 0x20
0034738E  pop      rdi
0034738F  ret      
```
