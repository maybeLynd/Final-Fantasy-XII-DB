# F homing pack (FABLE): `12-Items-Equipment-Shops-License/the-bazaar-recipe-unlock-and-purchase.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 003FEE40 (469 B, extent 003FEE40-003FF015)

Documented callee on this page: `0029FB50`

```
003FEE40  push     rbx
003FEE42  sub      rsp, 0x40
003FEE46  mov      rbx, rcx
003FEE49  mov      ecx, dword ptr [rdx]
003FEE4B  sub      ecx, 1
003FEE4E  je       0x3fee66  ; -> 003FEE66
003FEE50  cmp      ecx, 0x11
003FEE53  je       0x3ff00d  ; -> 003FF00D
003FEE59  mov      rcx, rbx
003FEE5C  add      rsp, 0x40
003FEE60  pop      rbx
003FEE61  jmp      0x5c5230  ; -> 005C5230 fn
003FEE66  mov      rax, qword ptr [rip + 0x1c9bdc3]  ; -> 0209AC30
003FEE6D  lea      rcx, [rbx + 0x50]
003FEE71  mov      qword ptr [rsp + 0x50], rbp
003FEE76  mov      r9, rbx
003FEE79  mov      qword ptr [rsp + 0x58], rsi
003FEE7E  mov      r8d, 2
003FEE84  movsxd   rsi, dword ptr [rdx + 8]
003FEE88  mov      rdx, qword ptr [rax + 0x40]
003FEE8C  mov      qword ptr [rsp + 0x60], rdi
003FEE91  call     0x2432b0  ; -> 002432B0 fn
003FEE96  movzx    ecx, word ptr [rax + 0xa]
003FEE9A  movzx    edx, word ptr [rax + 8]
003FEE9E  movsx    r8d, word ptr [rax + 6]
003FEEA3  test     rbx, rbx
003FEEA6  je       0x3feec9  ; -> 003FEEC9
003FEEA8  movzx    eax, word ptr [rax + 4]
003FEEAC  mov      word ptr [rbx + 0x98], ax
003FEEB3  mov      word ptr [rbx + 0x9a], r8w
003FEEBB  mov      word ptr [rbx + 0x9c], dx
003FEEC2  mov      word ptr [rbx + 0x9e], cx
003FEEC9  lea      rdx, [rip + 0x913180]  ; -> 00D12050
003FEED0  mov      rcx, rbx
003FEED3  call     0x247570  ; -> 00247570 fn
003FEED8  xor      edi, edi
003FEEDA  test     rbx, rbx
003FEEDD  jne      0x3feee3  ; -> 003FEEE3
003FEEDF  mov      ecx, edi
003FEEE1  jmp      0x3feeeb  ; -> 003FEEEB
003FEEE3  mov      rax, qword ptr [rbx + 0x60]
003FEEE7  mov      rcx, qword ptr [rax + 0x10]
003FEEEB  call     0x29fb50  ; -> 0029FB50 fn
003FEEF0  mov      rax, qword ptr [rip + 0x1c9bd39]  ; -> 0209AC30
003FEEF7  mov      rcx, rsi
003FEEFA  shl      rcx, 5
003FEEFE  mov      r8d, esi
003FEF01  movzx    edx, word ptr [rcx + rax + 0xd48]
003FEF09  lea      rcx, [rsp + 0x20]
003FEF0E  call     0x27f1a0  ; -> 0027F1A0 fn
003FEF13  test     rbx, rbx
003FEF16  jne      0x3fef1d  ; -> 003FEF1D
003FEF18  mov      rbp, rdi
003FEF1B  jmp      0x3fef25  ; -> 003FEF25
003FEF1D  mov      rax, qword ptr [rbx + 0x60]
003FEF21  mov      rbp, qword ptr [rax + 0x30]
003FEF25  sub      esi, 1
003FEF28  je       0x3fef55  ; -> 003FEF55
003FEF2A  sub      esi, 1
003FEF2D  je       0x3fef4e  ; -> 003FEF4E
003FEF2F  sub      esi, 1
003FEF32  je       0x3fef47  ; -> 003FEF47
003FEF34  cmp      esi, 1
003FEF37  je       0x3fef40  ; -> 003FEF40
003FEF39  mov      ecx, 0x4a99
003FEF3E  jmp      0x3fef5a  ; -> 003FEF5A
003FEF40  mov      ecx, 0x4a9e
003FEF45  jmp      0x3fef5a  ; -> 003FEF5A
003FEF47  mov      ecx, 0x4a9d
003FEF4C  jmp      0x3fef5a  ; -> 003FEF5A
003FEF4E  mov      ecx, 0x4a9c
003FEF53  jmp      0x3fef5a  ; -> 003FEF5A
003FEF55  mov      ecx, 0x4a9a
003FEF5A  call     0x2f9860  ; -> 002F9860 fn
003FEF5F  xor      ecx, ecx
003FEF61  mov      qword ptr [rbp + 0x18], rax
003FEF65  call     0x20e620  ; -> 0020E620 fn
003FEF6A  mov      rcx, rbp
003FEF6D  mov      dword ptr [rbp + 0x20], eax
003FEF70  call     0x29fb50  ; -> 0029FB50 fn
003FEF75  mov      rsi, qword ptr [rsp + 0x58]
003FEF7A  mov      eax, 0xffff
003FEF7F  mov      rbp, qword ptr [rsp + 0x50]
003FEF84  cmp      word ptr [rsp + 0x28], ax
003FEF89  je       0x3fefe1  ; -> 003FEFE1
003FEF8B  test     rbx, rbx
003FEF8E  jne      0x3fef95  ; -> 003FEF95
003FEF90  mov      r8, rdi
003FEF93  jmp      0x3fef9d  ; -> 003FEF9D
003FEF95  mov      rax, qword ptr [rbx + 0x60]
003FEF99  mov      r8, qword ptr [rax + 0x20]
003FEF9D  movzx    edx, byte ptr [rsp + 0x2a]
003FEFA2  mov      rax, qword ptr [r8 + 0x20]
003FEFA6  movzx    ecx, byte ptr [rax + rdx*8 + 7]
003FEFAB  mov      byte ptr [r8 + 0x39], cl
003FEFAF  mov      word ptr [r8 + 0xa], dx
003FEFB4  test     rbx, rbx
003FEFB7  je       0x3fefc1  ; -> 003FEFC1
003FEFB9  mov      rax, qword ptr [rbx + 0x60]
003FEFBD  mov      rdi, qword ptr [rax + 0x28]
003FEFC1  mov      rax, qword ptr [rsp + 0x20]
003FEFC6  xor      ecx, ecx
003FEFC8  mov      qword ptr [rdi + 0x18], rax
003FEFCC  call     0x20e620  ; -> 0020E620 fn
003FEFD1  mov      dword ptr [rdi + 0x20], eax
003FEFD4  xor      eax, eax
003FEFD6  mov      rdi, qword ptr [rsp + 0x60]
003FEFDB  add      rsp, 0x40
003FEFDF  pop      rbx
003FEFE0  ret      
003FEFE1  test     rbx, rbx
003FEFE4  jne      0x3fefeb  ; -> 003FEFEB
003FEFE6  mov      rax, rdi
003FEFE9  jmp      0x3feff3  ; -> 003FEFF3
003FEFEB  mov      rax, qword ptr [rbx + 0x60]
003FEFEF  mov      rax, qword ptr [rax + 0x20]
003FEFF3  and      dword ptr [rax + 8], 0xfffffffe
003FEFF7  test     rbx, rbx
003FEFFA  je       0x3ff004  ; -> 003FF004
003FEFFC  mov      rax, qword ptr [rbx + 0x60]
003FF000  mov      rdi, qword ptr [rax + 0x28]
003FF004  and      dword ptr [rdi + 8], 0xfffffffe
003FF008  mov      rdi, qword ptr [rsp + 0x60]
003FF00D  xor      eax, eax
003FF00F  add      rsp, 0x40
003FF013  pop      rbx
003FF014  ret      
```
