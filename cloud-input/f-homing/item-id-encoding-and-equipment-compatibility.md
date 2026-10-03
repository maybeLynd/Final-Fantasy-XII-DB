# F homing pack: `12-Items-Equipment-Shops-License/item-id-encoding-and-equipment-compatibility.md`

Generated 2026-10-02 22:28 by OPUS (homing_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 00352430 (208 B, extent 00352430-00352500)

Documented callee on this page: `003DFBE0`

```
00352430  mov      qword ptr [rsp + 8], rbx
00352435  mov      qword ptr [rsp + 0x10], rbp
0035243A  mov      qword ptr [rsp + 0x18], rsi
0035243F  mov      qword ptr [rsp + 0x20], rdi
00352444  push     r14
00352446  sub      rsp, 0x40
0035244A  mov      r14, rcx
0035244D  mov      rsi, r9
00352450  mov      rcx, r9
00352453  mov      rbp, r8
00352456  mov      rdi, rdx
00352459  call     0x267e10  ; -> 00267E10 fn
0035245E  mov      rcx, rsi
00352461  mov      ebx, eax
00352463  call     0x267e10  ; -> 00267E10 fn
00352468  lea      r8, [rsp + 0x20]
0035246D  mov      edx, ebx
0035246F  mov      ecx, eax
00352471  call     0x3dfbe0  ; -> 003DFBE0 fn
00352476  mov      rax, qword ptr [rsp + 0x30]
0035247B  test     rax, rax
0035247E  je       0x352497  ; -> 00352497
00352480  movsx    edx, word ptr [rax + 8]
00352484  movsx    ecx, word ptr [rax + 2]
00352488  or       dl, 0x40
0035248B  movzx    eax, byte ptr [rax]
0035248E  mov      byte ptr [rdi + 0xf], dl
00352491  mov      byte ptr [rdi + 0x21], al
00352494  mov      byte ptr [rdi + 0x22], cl
00352497  mov      rbx, qword ptr [rsp + 0x20]
0035249C  test     rbx, rbx
0035249F  je       0x3524e5  ; -> 003524E5
003524A1  movss    xmm1, dword ptr [rbx]
003524A5  mov      rcx, rsi
003524A8  call     0x267f60  ; -> 00267F60 fn
003524AD  movss    xmm1, dword ptr [rbx + 4]
003524B2  mov      rcx, rsi
003524B5  call     0x267f60  ; -> 00267F60 fn
003524BA  movss    xmm1, dword ptr [rbx + 8]
003524BF  mov      rcx, rsi
003524C2  call     0x267f60  ; -> 00267F60 fn
003524C7  movss    xmm1, dword ptr [rbx + 0xc]
003524CC  mov      rcx, rsi
003524CF  call     0x267f60  ; -> 00267F60 fn
003524D4  mov      r9, rsi
003524D7  mov      r8, rbp
003524DA  mov      rdx, rdi
003524DD  mov      rcx, r14
003524E0  call     0x350c30  ; -> 00350C30 fn
003524E5  mov      rbx, qword ptr [rsp + 0x50]
003524EA  mov      rbp, qword ptr [rsp + 0x58]
003524EF  mov      rsi, qword ptr [rsp + 0x60]
003524F4  mov      rdi, qword ptr [rsp + 0x68]
003524F9  add      rsp, 0x40
003524FD  pop      r14
003524FF  ret      
```
