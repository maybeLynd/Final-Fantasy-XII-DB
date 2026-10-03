# F homing pack: `00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-D-ids-108-139.md`

Generated 2026-10-02 22:28 by OPUS (homing_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 001C0960 (299 B, extent 001C0960-001C0A8B)

Documented callee on this page: `001BF8B0`

```
001C0960  push     rdi
001C0962  sub      rsp, 0x30
001C0966  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001C096F  mov      qword ptr [rsp + 0x40], rbx
001C0974  mov      qword ptr [rsp + 0x48], rsi
001C0979  mov      rsi, rcx
001C097C  call     0x1a9930  ; -> 001A9930 fn
001C0981  test     rax, rax
001C0984  je       0x1c0a7b  ; -> 001C0A7B
001C098A  mov      rbx, qword ptr [rsi + 0x30]
001C098E  lea      rdi, [rsi + 0x28]
001C0992  cmp      rbx, rdi
001C0995  je       0x1c0a7b  ; -> 001C0A7B
001C099B  mov      rax, qword ptr [rbx + 0x40]
001C099F  cmp      qword ptr [rax + 0x100], 0
001C09A7  je       0x1c09d7  ; -> 001C09D7
001C09A9  call     0x1a9930  ; -> 001A9930 fn
001C09AE  mov      rcx, qword ptr [rbx + 0x20]
001C09B2  lea      r8, [rax + 0x241]
001C09B9  sub      r8, rcx
001C09BC  nop      dword ptr [rax]
001C09C0  movzx    edx, byte ptr [rcx]
001C09C3  movzx    eax, byte ptr [rcx + r8]
001C09C8  sub      edx, eax
001C09CA  jne      0x1c09d3  ; -> 001C09D3
001C09CC  inc      rcx
001C09CF  test     eax, eax
001C09D1  jne      0x1c09c0  ; -> 001C09C0
001C09D3  test     edx, edx
001C09D5  je       0x1c09e7  ; -> 001C09E7
001C09D7  mov      rcx, rbx
001C09DA  call     0x16d6d0  ; -> 0016D6D0 fn
001C09DF  mov      rbx, rax
001C09E2  cmp      rax, rdi
001C09E5  jmp      0x1c0995  ; -> 001C0995
001C09E7  mov      rdi, qword ptr [rbx + 0x40]
001C09EB  test     rdi, rdi
001C09EE  je       0x1c0a7b  ; -> 001C0A7B
001C09F4  dec      dword ptr [rsi + 0x48]
001C09F7  mov      rcx, rbx
001C09FA  call     0x16d6d0  ; -> 0016D6D0 fn
001C09FF  lea      rdx, [rsi + 0x28]
001C0A03  mov      rcx, rbx
001C0A06  call     0x16da60  ; -> 0016DA60 fn
001C0A0B  nop      
001C0A0C  mov      rdx, qword ptr [rbx + 0x20]
001C0A10  mov      rax, qword ptr [rbx + 0x30]
001C0A14  sub      rax, rdx
001C0A17  cmp      rax, 1
001C0A1B  jle      0x1c0a34  ; -> 001C0A34
001C0A1D  mov      r8d, dword ptr [rbx + 0x30]
001C0A21  sub      r8d, edx
001C0A24  test     rdx, rdx
001C0A27  je       0x1c0a34  ; -> 001C0A34
001C0A29  lea      rcx, [rbx + 0x38]
001C0A2D  mov      rax, qword ptr [rcx]
001C0A30  call     qword ptr [rax + 0x18]
001C0A33  nop      
001C0A34  lea      rcx, [rsi + 0x50]
001C0A38  mov      rax, qword ptr [rcx]
001C0A3B  mov      r8d, 0x48
001C0A41  mov      rdx, rbx
001C0A44  call     qword ptr [rax + 0x18]
001C0A47  mov      r8, qword ptr [rdi + 0x108]
001C0A4E  mov      rdx, qword ptr [rdi + 0x100]
001C0A55  mov      rcx, rsi
001C0A58  call     0x1bf8b0  ; -> 001BF8B0 fn
001C0A5D  mov      rcx, qword ptr [rdi + 0x100]
001C0A64  test     rcx, rcx
001C0A67  je       0x1c0a6e  ; -> 001C0A6E
001C0A69  call     0x210eb0  ; -> 00210EB0 fn
001C0A6E  mov      edx, 0x118
001C0A73  mov      rcx, rdi
001C0A76  call     0x809950  ; -> 00809950 fn
001C0A7B  mov      rbx, qword ptr [rsp + 0x40]
001C0A80  mov      rsi, qword ptr [rsp + 0x48]
001C0A85  add      rsp, 0x30
001C0A89  pop      rdi
001C0A8A  ret      
```
