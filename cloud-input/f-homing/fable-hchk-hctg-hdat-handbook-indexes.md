# F homing pack (FABLE): `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/hchk-hctg-hdat-handbook-indexes.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 005792F0 (298 B, extent 005792F0-0057941A)

Documented callee on this page: `00577C30`

```
005792F0  mov      qword ptr [rsp + 8], rbx
005792F5  mov      qword ptr [rsp + 0x10], rbp
005792FA  mov      qword ptr [rsp + 0x18], rsi
005792FF  push     rdi
00579300  sub      rsp, 0x30
00579304  xor      esi, esi
00579306  lea      rbx, [rip + 0x7aa593]  ; -> 00D238A0
0057930D  cmp      byte ptr [rcx + 0xc5], sil
00579314  mov      r10d, r9d
00579317  mov      rbp, r8
0057931A  mov      rdi, rdx
0057931D  seta     sil
00579321  mov      r9, rcx
00579324  xor      r11d, r11d
00579327  nop      word ptr [rax + rax]
00579330  mov      rax, qword ptr [rdi + 0x10]
00579334  inc      r11d
00579337  movzx    ecx, word ptr [rbx]
0057933A  lea      rbx, [rbx + 2]
0057933E  mov      rdx, qword ptr [rax + rcx*8]
00579342  and      dword ptr [rdx + 8], 0xfffffffe
00579346  or       dword ptr [rdx + 8], esi
00579349  cmp      r11d, 9
0057934D  jb       0x579330  ; -> 00579330
0057934F  cmp      byte ptr [r9 + 0xc5], 0
00579357  jbe      0x5793d0  ; -> 005793D0
00579359  movzx    edx, byte ptr [r9 + 0xc4]
00579361  cmp      dl, 1
00579364  je       0x57937b  ; -> 0057937B
00579366  mov      rax, qword ptr [r9 + 0xc8]
0057936D  movzx    ecx, word ptr [rax + 0xe8]
00579374  sub      ecx, r10d
00579377  lea      r10d, [rcx - 1]
0057937B  test     byte ptr [r9 + 0xc0], 3
00579383  je       0x5793ad  ; -> 005793AD
00579385  mov      rax, qword ptr [rip + 0x27303bc]  ; -> 02CA9748
0057938C  mov      rcx, qword ptr [rax + 0x128]
00579393  test     rcx, rcx
00579396  jne      0x57939d  ; -> 0057939D
00579398  or       eax, 0xffffffff
0057939B  jmp      0x5793a4  ; -> 005793A4
0057939D  movzx    eax, byte ptr [rcx + 0xc1]
005793A4  cmp      r10d, eax
005793A7  jne      0x5793ad  ; -> 005793AD
005793A9  xor      eax, eax
005793AB  jmp      0x579405  ; -> 00579405
005793AD  mov      rax, qword ptr [r9 + 0xd0]
005793B4  mov      r8d, r10d
005793B7  movzx    ecx, dl
005793BA  lea      r9, [rip + 0x7aa3ff]  ; -> 00D237C0
005793C1  mov      rdx, rdi
005793C4  mov      qword ptr [rsp + 0x20], rax
005793C9  call     0x577c30  ; -> 00577C30 fn
005793CE  jmp      0x579400  ; -> 00579400
005793D0  xor      ecx, ecx
005793D2  cmp      byte ptr [r9 + 0xc4], cl
005793D9  setne    cl
005793DC  add      ecx, 0x868
005793E2  call     0x2f9860  ; -> 002F9860 fn
005793E7  mov      r9, rax
005793EA  mov      qword ptr [rsp + 0x20], 0
005793F3  xor      r8d, r8d
005793F6  xor      edx, edx
005793F8  mov      rcx, rbp
005793FB  call     0x2d8910  ; -> 002D8910 fn
00579400  mov      eax, 1
00579405  mov      rbx, qword ptr [rsp + 0x40]
0057940A  mov      rbp, qword ptr [rsp + 0x48]
0057940F  mov      rsi, qword ptr [rsp + 0x50]
00579414  add      rsp, 0x30
00579418  pop      rdi
00579419  ret      
```
