# F homing pack (FABLE): `16-UI/License-Board-View/the-license-board-screen-widgets.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 2. No bearing page cites them and no documented function calls them directly.

## 00511920 (87 B, extent 00511920-00511977)

Documented callee on this page: `002D7B40`

```
00511920  push     rsi
00511922  sub      rsp, 0x20
00511926  mov      rsi, r9
00511929  call     0x280120  ; -> 00280120 fn
0051192E  test     eax, eax
00511930  jne      0x511971  ; -> 00511971
00511932  mov      qword ptr [rsp + 0x30], rbx
00511937  mov      rcx, rsi
0051193A  mov      qword ptr [rsp + 0x38], rdi
0051193F  call     0x267e10  ; -> 00267E10 fn
00511944  mov      rcx, rsi
00511947  mov      edi, eax
00511949  call     0x267e10  ; -> 00267E10 fn
0051194E  mov      rcx, rsi
00511951  mov      ebx, eax
00511953  call     0x267e10  ; -> 00267E10 fn
00511958  xor      r9d, r9d
0051195B  mov      r8d, edi
0051195E  mov      edx, ebx
00511960  mov      ecx, eax
00511962  call     0x2d7b40  ; -> 002D7B40 fn
00511967  mov      rdi, qword ptr [rsp + 0x38]
0051196C  mov      rbx, qword ptr [rsp + 0x30]
00511971  add      rsp, 0x20
00511975  pop      rsi
00511976  ret      
```

## 00561280 (119 B, extent 00561280-005612F7)

Documented callee on this page: `00559800`

```
00561280  push     rbx
00561282  sub      rsp, 0x20
00561286  mov      rax, qword ptr [rip + 0x1b399a3]  ; -> 0209AC30
0056128D  mov      rbx, qword ptr [rax + 0x320]
00561294  test     rbx, rbx
00561297  je       0x5612d9  ; -> 005612D9
00561299  test     ecx, ecx
0056129B  jne      0x5612bb  ; -> 005612BB
0056129D  test     byte ptr [rbx + 0x570], 2
005612A4  jne      0x5612d9  ; -> 005612D9
005612A6  mov      rcx, rbx
005612A9  call     0x55a1f0  ; -> 0055A1F0 fn
005612AE  or       dword ptr [rbx + 0x570], 2
005612B5  add      rsp, 0x20
005612B9  pop      rbx
005612BA  ret      
005612BB  test     byte ptr [rbx + 0x570], 2
005612C2  je       0x5612d9  ; -> 005612D9
005612C4  mov      rcx, rbx
005612C7  call     0x559800  ; -> 00559800 fn
005612CC  and      dword ptr [rbx + 0x570], 0xfffffffd
005612D3  add      rsp, 0x20
005612D7  pop      rbx
005612D8  ret      
005612D9  mov      edx, 3
005612DE  lea      ecx, [rdx - 2]
005612E1  call     0x2d7580  ; -> 002D7580 fn
005612E6  mov      edx, 3
005612EB  xor      ecx, ecx
005612ED  add      rsp, 0x20
005612F1  pop      rbx
005612F2  jmp      0x2d7580  ; -> 002D7580 fn
```
