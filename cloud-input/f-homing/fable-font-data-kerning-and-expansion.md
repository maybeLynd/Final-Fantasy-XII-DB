# F homing pack (FABLE): `16-UI/Text-And-Number-Rendering/font-data-kerning-and-expansion.md`

Generated 2026-10-03 04:02 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 2. No bearing page cites them and no documented function calls them directly.

## 001B5140 (119 B, extent 001B5140-001B51B7)

Documented callee on this page: `001B4930`

```
001B5140  mov      qword ptr [rsp + 0x18], rbx
001B5145  push     rdi
001B5146  sub      rsp, 0x40
001B514A  mov      rdi, rcx
001B514D  call     0x1b4930  ; -> 001B4930 fn
001B5152  mov      rbx, qword ptr [rdi + 8]
001B5156  cmp      rbx, qword ptr [rdi + 0x10]
001B515A  je       0x1b51ac  ; -> 001B51AC
001B515C  mov      qword ptr [rsp + 0x58], rsi
001B5161  xor      esi, esi
001B5163  xorps    xmm0, xmm0
001B5166  mov      qword ptr [rsp + 0x30], rsi
001B516B  lea      rdx, [rbx + 0x18]
001B516F  lea      rcx, [rsp + 0x38]
001B5174  movdqu   xmmword ptr [rsp + 0x20], xmm0
001B517A  call     0x1edf00  ; -> 001EDF00 fn
001B517F  mov      r8, qword ptr [rbx + 8]
001B5183  lea      rcx, [rsp + 0x20]
001B5188  mov      rdx, qword ptr [rbx]
001B518B  call     0x1a4bf0  ; -> 001A4BF0 fn
001B5190  lea      rdx, [rsp + 0x20]
001B5195  mov      rcx, rdi
001B5198  call     0x1b5610  ; -> 001B5610 fn
001B519D  add      rbx, 0x20
001B51A1  cmp      rbx, qword ptr [rdi + 0x10]
001B51A5  jne      0x1b5163  ; -> 001B5163
001B51A7  mov      rsi, qword ptr [rsp + 0x58]
001B51AC  mov      rbx, qword ptr [rsp + 0x60]
001B51B1  add      rsp, 0x40
001B51B5  pop      rdi
001B51B6  ret      
```

## 00679ED0 (107 B, extent 00679ED0-00679F3B)

Documented callee on this page: `00679BF0`

```
00679ED0  push     rbx
00679ED2  sub      rsp, 0x20
00679ED6  mov      rbx, rcx
00679ED9  mov      eax, dword ptr [rcx + 0x258]
00679EDF  cmp      eax, 1
00679EE2  je       0x679f33  ; -> 00679F33
00679EE4  mov      qword ptr [rsp + 0x30], rdi
00679EE9  nop      dword ptr [rax]
00679EF0  lea      rcx, [rbx + 0x4f8]
00679EF7  call     0x5cd840  ; -> 005CD840 fn
00679EFC  mov      eax, dword ptr [rbx + 0x268]
00679F02  cmp      eax, 1
00679F05  je       0x679f12  ; -> 00679F12
00679F07  mov      eax, dword ptr [rbx + 0x268]
00679F0D  cmp      eax, 2
00679F10  jne      0x679f23  ; -> 00679F23
00679F12  cmp      dword ptr [rbx + 0x25c], 2
00679F19  je       0x679f23  ; -> 00679F23
00679F1B  mov      rcx, rbx
00679F1E  call     0x679bf0  ; -> 00679BF0 fn
00679F23  mov      eax, dword ptr [rbx + 0x258]
00679F29  cmp      eax, 1
00679F2C  jne      0x679ef0  ; -> 00679EF0
00679F2E  mov      rdi, qword ptr [rsp + 0x30]
00679F33  xor      eax, eax
00679F35  add      rsp, 0x20
00679F39  pop      rbx
00679F3A  ret      
```
