# F homing pack (FABLE): `12-Items-Equipment-Shops-License/license-board-grid-format.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 003FCAD0 (495 B, extent 003FCAD0-003FCCBF)

Documented callee on this page: `003FC900`

```
003FCAD0  mov      qword ptr [rsp + 8], rcx
003FCAD5  push     rbx
003FCAD6  push     r12
003FCAD8  push     r13
003FCADA  push     r15
003FCADC  sub      rsp, 0x28
003FCAE0  movsxd   r15, r8d
003FCAE3  mov      r13, rdx
003FCAE6  movsxd   r12, r9d
003FCAE9  mov      rbx, rcx
003FCAEC  mov      r8, r15
003FCAEF  cmp      r15, r12
003FCAF2  jg       0x3fcb24  ; -> 003FCB24
003FCAF4  mov      r9d, 7
003FCAFA  nop      word ptr [rax + rax]
003FCB00  mov      rax, qword ptr [rbx + 0x10]
003FCB04  mov      rdx, qword ptr [rax + r8*8]
003FCB08  inc      r8
003FCB0B  mov      rax, qword ptr [rdx + 0x20]
003FCB0F  movzx    ecx, byte ptr [rax + 0x3f]
003FCB13  mov      word ptr [rdx + 0xa], r9w
003FCB18  and      dword ptr [rdx + 8], 0xfffffffe
003FCB1C  mov      byte ptr [rdx + 0x39], cl
003FCB1F  cmp      r8, r12
003FCB22  jle      0x3fcb00  ; -> 003FCB00
003FCB24  mov      eax, 0xffff
003FCB29  cmp      word ptr [r13 + 8], ax
003FCB2E  je       0x3fcc0f  ; -> 003FCC0F
003FCB34  mov      qword ptr [rsp + 0x58], rbp
003FCB39  xor      ebp, ebp
003FCB3B  mov      qword ptr [rsp + 0x60], rsi
003FCB40  mov      qword ptr [rsp + 0x20], r14
003FCB45  mov      qword ptr [rsp + 0x68], rdi
003FCB4A  lea      r14d, [rbp + 8]
003FCB4E  nop      
003FCB50  mov      ecx, ebp
003FCB52  call     0x282df0  ; -> 00282DF0 fn
003FCB57  mov      rcx, rax
003FCB5A  mov      rsi, rax
003FCB5D  call     0x282fa0  ; -> 00282FA0 fn
003FCB62  test     eax, eax
003FCB64  je       0x3fcbed  ; -> 003FCBED
003FCB6A  mov      rcx, qword ptr [rbx + 0x10]
003FCB6E  cmp      r15, r12
003FCB71  mov      rdx, r12
003FCB74  cmovle   rdx, r15
003FCB78  mov      rdi, qword ptr [rcx + rdx*8]
003FCB7C  mov      ecx, 1
003FCB81  or       dword ptr [rdi + 8], 1
003FCB85  movzx    edx, word ptr [r13 + 8]
003FCB8A  shl      edx, 0x10
003FCB8D  call     0x35d330  ; -> 0035D330 fn
003FCB92  movzx    ecx, word ptr [r13 + 8]
003FCB97  mov      rdx, rsi
003FCB9A  mov      rbx, rax
003FCB9D  call     0x282f10  ; -> 00282F10 fn
003FCBA2  mov      ecx, dword ptr [rbx]
003FCBA4  cmp      ecx, 6
003FCBA7  je       0x3fcc1b  ; -> 003FCC1B
003FCBA9  add      ecx, -8
003FCBAC  cmp      ecx, 1
003FCBAF  ja       0x3fcbe8  ; -> 003FCBE8
003FCBB1  mov      rcx, qword ptr [rdi + 0x20]
003FCBB5  movzx    edx, byte ptr [rcx + 0x47]
003FCBB9  mov      byte ptr [rdi + 0x39], dl
003FCBBC  mov      word ptr [rdi + 0xa], r14w
003FCBC1  test     al, al
003FCBC3  je       0x3fcbe8  ; -> 003FCBE8
003FCBC5  movsx    ecx, word ptr [rsi + 0x60]
003FCBC9  mov      edx, 5
003FCBCE  call     0x2c9b30  ; -> 002C9B30 fn
003FCBD3  mov      rcx, qword ptr [rdi + 0x20]
003FCBD7  inc      eax
003FCBD9  movsxd   rdx, eax
003FCBDC  movzx    edx, byte ptr [rcx + rdx*8 + 7]
003FCBE1  mov      byte ptr [rdi + 0x39], dl
003FCBE4  mov      word ptr [rdi + 0xa], ax
003FCBE8  mov      rbx, qword ptr [rsp + 0x50]
003FCBED  inc      ebp
003FCBEF  inc      r15
003FCBF2  cmp      ebp, 9
003FCBF5  jl       0x3fcb50  ; -> 003FCB50
003FCBFB  mov      r14, qword ptr [rsp + 0x20]
003FCC00  mov      rdi, qword ptr [rsp + 0x68]
003FCC05  mov      rsi, qword ptr [rsp + 0x60]
003FCC0A  mov      rbp, qword ptr [rsp + 0x58]
003FCC0F  add      rsp, 0x28
003FCC13  pop      r15
003FCC15  pop      r13
003FCC17  pop      r12
003FCC19  pop      rbx
003FCC1A  ret      
003FCC1B  test     al, al
003FCC1D  je       0x3fcc88  ; -> 003FCC88
003FCC1F  movzx    ecx, byte ptr [rsi + 0x60]
003FCC23  call     0x323670  ; -> 00323670 fn
003FCC28  movzx    ecx, byte ptr [rsi + 0x60]
003FCC2C  movzx    ebx, al
003FCC2F  call     0x323630  ; -> 00323630 fn
003FCC34  movzx    edx, word ptr [r13 + 8]
003FCC39  movzx    ecx, bl
003FCC3C  movzx    r14d, al
003FCC40  call     0x3fc900  ; -> 003FC900 fn
003FCC45  test     eax, eax
003FCC47  jne      0x3fcc70  ; -> 003FCC70
003FCC49  movzx    edx, word ptr [r13 + 8]
003FCC4E  movzx    ecx, r14b
003FCC52  call     0x3fc900  ; -> 003FC900 fn
003FCC57  test     eax, eax
003FCC59  jne      0x3fcc70  ; -> 003FCC70
003FCC5B  mov      rax, qword ptr [rdi + 0x20]
003FCC5F  mov      r14d, 8
003FCC65  movzx    ecx, byte ptr [rax + 0x47]
003FCC69  mov      word ptr [rdi + 0xa], r14w
003FCC6E  jmp      0x3fcc85  ; -> 003FCC85
003FCC70  mov      rax, qword ptr [rdi + 0x20]
003FCC74  movzx    ecx, byte ptr [rax + 0x4f]
003FCC78  mov      eax, 9
003FCC7D  mov      word ptr [rdi + 0xa], ax
003FCC81  lea      r14d, [rax - 1]
003FCC85  mov      byte ptr [rdi + 0x39], cl
003FCC88  movzx    r8d, word ptr [r13 + 8]
003FCC8D  lea      rax, [rsi + 0x98]
003FCC94  xor      edx, edx
003FCC96  nop      word ptr [rax + rax]
003FCCA0  movzx    ecx, word ptr [rax + 2]
003FCCA4  cmp      r8d, ecx
003FCCA7  je       0x3fcbc5  ; -> 003FCBC5
003FCCAD  inc      rdx
003FCCB0  add      rax, 4
003FCCB4  cmp      rdx, 5
003FCCB8  jl       0x3fcca0  ; -> 003FCCA0
003FCCBA  jmp      0x3fcbe8  ; -> 003FCBE8
```
