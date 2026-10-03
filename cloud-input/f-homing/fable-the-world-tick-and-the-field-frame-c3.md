# F homing pack (FABLE): `00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md`

Generated 2026-10-03 06:31 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 5. No bearing page cites them and no documented function calls them directly.

## 002DF1E0 (54 B, extent 002DF1E0-002DF216)

Documented callee on this page: `001DBF00`

```
002DF1E0  sub      rsp, 0x38
002DF1E4  test     edx, edx
002DF1E6  jg       0x2df1fc  ; -> 002DF1FC
002DF1E8  xor      edx, edx
002DF1EA  mov      r9d, r8d
002DF1ED  mov      r8d, ecx
002DF1F0  lea      ecx, [rdx + 1]
002DF1F3  add      rsp, 0x38
002DF1F7  jmp      0x1dbf00  ; -> 001DBF00 fn
002DF1FC  mov      r9d, edx
002DF1FF  mov      dword ptr [rsp + 0x20], r8d
002DF204  xor      edx, edx
002DF206  mov      r8d, ecx
002DF209  lea      ecx, [rdx + 1]
002DF20C  call     0x1dbfa0  ; -> 001DBFA0 fn
002DF211  add      rsp, 0x38
002DF215  ret      
```

## 002EC630 (74 B, extent 002EC630-002EC67A)

Documented callee on this page: `00426E20`

```
002EC630  sub      rsp, 0x28
002EC634  test     rcx, rcx
002EC637  je       0x2ec673  ; -> 002EC673
002EC639  cmp      dword ptr [rcx], -1
002EC63C  je       0x2ec673  ; -> 002EC673
002EC63E  movzx    eax, word ptr [rcx]
002EC641  cmp      ax, -1
002EC645  je       0x2ec669  ; -> 002EC669
002EC647  movsx    rax, ax
002EC64B  imul     rcx, rax, 0x740
002EC652  add      rcx, qword ptr [rip + 0x1fda8cf]  ; -> 022C6F28
002EC659  je       0x2ec669  ; -> 002EC669
002EC65B  cmp      dword ptr [rcx + 0x284], 0
002EC662  je       0x2ec669  ; -> 002EC669
002EC664  call     0x426e20  ; -> 00426E20 fn
002EC669  mov      eax, 1
002EC66E  add      rsp, 0x28
002EC672  ret      
002EC673  xor      eax, eax
002EC675  add      rsp, 0x28
002EC679  ret      
```

## 003EB190 (111 B, extent 003EB190-003EB1FF)

Documented callee on this page: `003EB470`

```
003EB190  cmp      ecx, 0x1f
003EB193  ja       0x3eb1fe  ; -> 003EB1FE
003EB195  mov      qword ptr [rsp + 0x10], rbp
003EB19A  mov      qword ptr [rsp + 0x18], rsi
003EB19F  push     rdi
003EB1A0  sub      rsp, 0x20
003EB1A4  movsxd   rax, ecx
003EB1A7  mov      edi, r9d
003EB1AA  lea      rcx, [rip + 0x277386f]  ; -> 02B5EA20
003EB1B1  mov      qword ptr [rsp + 0x30], rbx
003EB1B6  mov      esi, r8d
003EB1B9  mov      rbp, rdx
003EB1BC  lea      rbx, [rcx + rax*8]
003EB1C0  mov      rcx, qword ptr [rcx + rax*8]
003EB1C4  test     rcx, rcx
003EB1C7  je       0x3eb1d5  ; -> 003EB1D5
003EB1C9  call     0x3eb470  ; -> 003EB470 fn
003EB1CE  mov      qword ptr [rbx], 0
003EB1D5  mov      r9d, dword ptr [rsp + 0x50]
003EB1DA  mov      r8d, edi
003EB1DD  mov      edx, esi
003EB1DF  mov      rcx, rbp
003EB1E2  call     0x3eb250  ; -> 003EB250 fn
003EB1E7  mov      rbp, qword ptr [rsp + 0x38]
003EB1EC  mov      rsi, qword ptr [rsp + 0x40]
003EB1F1  mov      qword ptr [rbx], rax
003EB1F4  mov      rbx, qword ptr [rsp + 0x30]
003EB1F9  add      rsp, 0x20
003EB1FD  pop      rdi
003EB1FE  ret      
```

## 00473490 (43 B, extent 00473490-004734BB)

Documented callee on this page: `00466C40`

```
00473490  push     rbx
00473492  sub      rsp, 0x30
00473496  movaps   xmmword ptr [rsp + 0x20], xmm6
0047349B  mov      ebx, ecx
0047349D  call     0x466c40  ; -> 00466C40 fn
004734A2  mov      ecx, ebx
004734A4  movaps   xmm6, xmm0
004734A7  call     0x466c80  ; -> 00466C80 fn
004734AC  subss    xmm0, xmm6
004734B0  movaps   xmm6, xmmword ptr [rsp + 0x20]
004734B5  add      rsp, 0x30
004734B9  pop      rbx
004734BA  ret      
```

## 004734C0 (46 B, extent 004734C0-004734EE)

Documented callee on this page: `00466BB0`

```
004734C0  push     rbx
004734C2  sub      rsp, 0x30
004734C6  movaps   xmmword ptr [rsp + 0x20], xmm6
004734CB  mov      ebx, ecx
004734CD  call     0x466bb0  ; -> 00466BB0 fn
004734D2  mov      ecx, ebx
004734D4  movaps   xmm6, xmm0
004734D7  call     0x466c40  ; -> 00466C40 fn
004734DC  subss    xmm6, xmm0
004734E0  movaps   xmm0, xmm6
004734E3  movaps   xmm6, xmmword ptr [rsp + 0x20]
004734E8  add      rsp, 0x30
004734EC  pop      rbx
004734ED  ret      
```
