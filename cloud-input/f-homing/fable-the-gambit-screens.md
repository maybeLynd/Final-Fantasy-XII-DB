# F homing pack (FABLE): `16-UI/Gambit-Screens/the-gambit-screens.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 002CABF0 (999 B, extent 002CABF0-002CAFD7)

Documented callee on this page: `002CC8D0`

```
002CABF0  mov      qword ptr [rsp + 0x20], rbx
002CABF5  push     rdi
002CABF6  sub      rsp, 0x30
002CABFA  mov      rbx, rcx
002CABFD  mov      ecx, dword ptr [rdx]
002CABFF  sub      ecx, 1
002CAC02  je       0x2caebc  ; -> 002CAEBC
002CAC08  sub      ecx, 1
002CAC0B  je       0x2cad79  ; -> 002CAD79
002CAC11  sub      ecx, 1
002CAC14  je       0x2cac95  ; -> 002CAC95
002CAC16  cmp      ecx, 1
002CAC19  je       0x2cac2d  ; -> 002CAC2D
002CAC1B  mov      rcx, rbx
002CAC1E  mov      rbx, qword ptr [rsp + 0x58]
002CAC23  add      rsp, 0x30
002CAC27  pop      rdi
002CAC28  jmp      0x5c5230  ; -> 005C5230 fn
002CAC2D  mov      rax, qword ptr [rbx + 0xd8]
002CAC34  test     rax, rax
002CAC37  je       0x2cafca  ; -> 002CAFCA
002CAC3D  test     dword ptr [rax + 0x168], 0x300
002CAC47  jne      0x2cafca  ; -> 002CAFCA
002CAC4D  mov      rax, qword ptr [rax + 0xd0]
002CAC54  xor      edi, edi
002CAC56  movsx    r8d, word ptr [rbx + 0xe6]
002CAC5E  movsx    edx, word ptr [rbx + 0xe4]
002CAC65  inc      r8d
002CAC68  mov      dword ptr [rsp + 0x28], edi
002CAC6C  movsx    ecx, word ptr [rax + 0x9e]
002CAC73  movsx    r9d, word ptr [rax + 0x9c]
002CAC7B  mov      dword ptr [rsp + 0x20], ecx
002CAC7F  mov      rcx, qword ptr [rbx + 0x38]
002CAC83  call     0x242a80  ; -> 00242A80 fn
002CAC88  xor      eax, eax
002CAC8A  mov      rbx, qword ptr [rsp + 0x58]
002CAC8F  add      rsp, 0x30
002CAC93  pop      rdi
002CAC94  ret      
002CAC95  mov      r8d, dword ptr [rbx + 0xe0]
002CAC9C  mov      r9d, 2
002CACA2  lea      edx, [r9 + 0x2e]
002CACA6  lea      ecx, [rdx + 0x50]
002CACA9  call     0x2cc8d0  ; -> 002CC8D0 fn
002CACAE  mov      ecx, 2
002CACB3  mov      edi, eax
002CACB5  call     0x2dd7e0  ; -> 002DD7E0 fn
002CACBA  mov      rcx, qword ptr [rbx + 0x60]
002CACBE  mov      edx, eax
002CACC0  mov      r8, qword ptr [rcx + 0x10]
002CACC4  test     byte ptr [r8 + 8], 1
002CACC9  je       0x2cace4  ; -> 002CACE4
002CACCB  mov      ecx, dword ptr [r8 + 0x24]
002CACCF  mov      dword ptr [rsp + 0x40], ecx
002CACD3  cmp      ecx, eax
002CACD5  je       0x2cace4  ; -> 002CACE4
002CACD7  mov      byte ptr [rsp + 0x43], dil
002CACDC  mov      eax, dword ptr [rsp + 0x40]
002CACE0  mov      dword ptr [r8 + 0x24], eax
002CACE4  mov      rax, qword ptr [rbx + 0x60]
002CACE8  mov      rcx, qword ptr [rax + 0x18]
002CACEC  test     byte ptr [rcx + 8], 1
002CACF0  je       0x2cad09  ; -> 002CAD09
002CACF2  mov      eax, dword ptr [rcx + 0x24]
002CACF5  mov      dword ptr [rsp + 0x40], eax
002CACF9  cmp      eax, edx
002CACFB  je       0x2cad09  ; -> 002CAD09
002CACFD  mov      byte ptr [rsp + 0x43], dil
002CAD02  mov      eax, dword ptr [rsp + 0x40]
002CAD06  mov      dword ptr [rcx + 0x24], eax
002CAD09  mov      rax, qword ptr [rbx + 0x60]
002CAD0D  mov      rcx, qword ptr [rax + 8]
002CAD11  test     byte ptr [rcx + 8], 1
002CAD15  je       0x2cad37  ; -> 002CAD37
002CAD17  mov      eax, dword ptr [rcx + 0x28]
002CAD1A  mov      dword ptr [rsp + 0x40], eax
002CAD1E  cmp      eax, edx
002CAD20  je       0x2cad37  ; -> 002CAD37
002CAD22  mov      byte ptr [rsp + 0x43], dil
002CAD27  mov      eax, dword ptr [rsp + 0x40]
002CAD2B  mov      dword ptr [rcx + 0x34], eax
002CAD2E  mov      dword ptr [rcx + 0x30], eax
002CAD31  mov      dword ptr [rcx + 0x2c], eax
002CAD34  mov      dword ptr [rcx + 0x28], eax
002CAD37  mov      rax, qword ptr [rbx + 0x60]
002CAD3B  mov      rcx, qword ptr [rax]
002CAD3E  test     byte ptr [rcx + 8], 1
002CAD42  je       0x2cafca  ; -> 002CAFCA
002CAD48  mov      eax, dword ptr [rcx + 0x28]
002CAD4B  mov      dword ptr [rsp + 0x40], eax
002CAD4F  cmp      eax, edx
002CAD51  je       0x2cafca  ; -> 002CAFCA
002CAD57  mov      byte ptr [rsp + 0x43], dil
002CAD5C  mov      eax, dword ptr [rsp + 0x40]
002CAD60  mov      dword ptr [rcx + 0x34], eax
002CAD63  mov      dword ptr [rcx + 0x30], eax
002CAD66  mov      dword ptr [rcx + 0x2c], eax
002CAD69  mov      dword ptr [rcx + 0x28], eax
002CAD6C  xor      eax, eax
002CAD6E  mov      rbx, qword ptr [rsp + 0x58]
002CAD73  add      rsp, 0x30
002CAD77  pop      rdi
002CAD78  ret      
002CAD79  movzx    eax, word ptr [rbx + 0xe8]
002CAD80  test     ax, ax
002CAD83  jle      0x2cad8f  ; -> 002CAD8F
002CAD85  dec      ax
002CAD88  mov      word ptr [rbx + 0xe8], ax
002CAD8F  movzx    eax, word ptr [rbx + 0xea]
002CAD96  test     ax, ax
002CAD99  jle      0x2cada5  ; -> 002CADA5
002CAD9B  dec      ax
002CAD9E  mov      word ptr [rbx + 0xea], ax
002CADA5  mov      rax, qword ptr [rip + 0x1dcfe84]  ; -> 0209AC30
002CADAC  movzx    ecx, byte ptr [rax + 0xde9]
002CADB3  test     cl, 3
002CADB6  je       0x2cadea  ; -> 002CADEA
002CADB8  test     cl, 1
002CADBB  je       0x2cadcb  ; -> 002CADCB
002CADBD  mov      eax, 4
002CADC2  mov      word ptr [rbx + 0xea], ax
002CADC9  jmp      0x2caddc  ; -> 002CADDC
002CADCB  test     cl, 2
002CADCE  je       0x2caddc  ; -> 002CADDC
002CADD0  mov      eax, 4
002CADD5  mov      word ptr [rbx + 0xe8], ax
002CADDC  mov      rax, qword ptr [rip + 0x1dcfe4d]  ; -> 0209AC30
002CADE3  and      byte ptr [rax + 0xde9], 0xfc
002CADEA  mov      ecx, dword ptr [rbx + 0xc0]
002CADF0  test     cl, 3
002CADF3  je       0x2cae65  ; -> 002CAE65
002CADF5  mov      r8d, dword ptr [rip + 0x1dc4774]  ; -> 0208F570
002CADFC  sub      r8d, dword ptr [rbx + 0xd0]
002CAE03  mov      edx, dword ptr [rbx + 0xcc]
002CAE09  shr      ecx, 2
002CAE0C  and      ecx, 0xf
002CAE0F  call     0x248f40  ; -> 00248F40 fn
002CAE14  ucomiss  xmm0, dword ptr [rip + 0x1a20d8d]  ; -> 01CEBBA8 [f32 1]
002CAE1B  jp       0x2cae36  ; -> 002CAE36
002CAE1D  jne      0x2cae36  ; -> 002CAE36
002CAE1F  movzx    eax, word ptr [rbx + 0xc8]
002CAE26  add      ax, word ptr [rbx + 0xc4]
002CAE2D  and      dword ptr [rbx + 0xc0], 0xfffffffc
002CAE34  jmp      0x2cae5e  ; -> 002CAE5E
002CAE36  movsx    eax, word ptr [rbx + 0xc8]
002CAE3D  movd     xmm1, eax
002CAE41  movsx    eax, word ptr [rbx + 0xc4]
002CAE48  cvtdq2ps xmm1, xmm1
002CAE4B  mulss    xmm1, xmm0
002CAE4F  movd     xmm0, eax
002CAE53  cvtdq2ps xmm0, xmm0
002CAE56  addss    xmm1, xmm0
002CAE5A  cvttss2si eax, xmm1
002CAE5E  mov      word ptr [rbx + 0xe4], ax
002CAE65  mov      rax, qword ptr [rbx + 0x60]
002CAE69  mov      rdx, qword ptr [rax + 8]
002CAE6D  mov      rcx, qword ptr [rdx]
002CAE70  movzx    eax, word ptr [rcx + 4]
002CAE74  add      ax, word ptr [rbx + 0xee]
002CAE7B  sub      ax, word ptr [rbx + 0xe8]
002CAE82  mov      word ptr [rdx + 0xc], ax
002CAE86  movzx    eax, word ptr [rcx + 6]
002CAE8A  mov      word ptr [rdx + 0xe], ax
002CAE8E  mov      rax, qword ptr [rbx + 0x60]
002CAE92  mov      rdx, qword ptr [rax]
002CAE95  mov      rcx, qword ptr [rdx]
002CAE98  movzx    eax, word ptr [rcx + 4]
002CAE9C  add      ax, word ptr [rbx + 0xea]
002CAEA3  mov      word ptr [rdx + 0xc], ax
002CAEA7  movzx    eax, word ptr [rcx + 6]
002CAEAB  mov      word ptr [rdx + 0xe], ax
002CAEAF  xor      eax, eax
002CAEB1  mov      rbx, qword ptr [rsp + 0x58]
002CAEB6  add      rsp, 0x30
002CAEBA  pop      rdi
002CAEBB  ret      
002CAEBC  mov      rax, qword ptr [rip + 0x1dcfd6d]  ; -> 0209AC30
002CAEC3  lea      rcx, [rbx + 0x50]
002CAEC7  mov      qword ptr [rsp + 0x48], rbp
002CAECC  mov      r9, rbx
002CAECF  mov      rbp, qword ptr [rdx + 0x10]
002CAED3  mov      r8d, 7
002CAED9  mov      qword ptr [rsp + 0x50], rsi
002CAEDE  mov      rdx, qword ptr [rax + 0x38]
002CAEE2  call     0x2432b0  ; -> 002432B0 fn
002CAEE7  xor      edi, edi
002CAEE9  movzx    ecx, word ptr [rax + 0xa]
002CAEED  movzx    edx, word ptr [rax + 8]
002CAEF1  movsx    r8d, word ptr [rax + 6]
002CAEF6  test     rbx, rbx
002CAEF9  je       0x2caf26  ; -> 002CAF26
002CAEFB  movzx    eax, word ptr [rax + 4]
002CAEFF  mov      word ptr [rbx + 0x98], ax
002CAF06  mov      rax, qword ptr [rbx + 0x60]
002CAF0A  mov      word ptr [rbx + 0x9a], r8w
002CAF12  mov      word ptr [rbx + 0x9c], dx
002CAF19  mov      word ptr [rbx + 0x9e], cx
002CAF20  mov      rsi, qword ptr [rax + 0x10]
002CAF24  jmp      0x2caf29  ; -> 002CAF29
002CAF26  mov      rsi, rdi
002CAF29  mov      ecx, 0x466d
002CAF2E  call     0x2f9860  ; -> 002F9860 fn
002CAF33  xor      ecx, ecx
002CAF35  mov      qword ptr [rsi + 0x18], rax
002CAF39  call     0x20e620  ; -> 0020E620 fn
002CAF3E  and      dword ptr [rsi + 8], 0xfffffffe
002CAF42  mov      dword ptr [rsi + 0x20], eax
002CAF45  mov      rsi, qword ptr [rsp + 0x50]
002CAF4A  test     rbx, rbx
002CAF4D  je       0x2caf57  ; -> 002CAF57
002CAF4F  mov      rax, qword ptr [rbx + 0x60]
002CAF53  mov      rdi, qword ptr [rax + 0x18]
002CAF57  mov      ecx, 0x4670
002CAF5C  call     0x2f9860  ; -> 002F9860 fn
002CAF61  xor      ecx, ecx
002CAF63  mov      qword ptr [rdi + 0x18], rax
002CAF67  call     0x20e620  ; -> 0020E620 fn
002CAF6C  and      dword ptr [rdi + 8], 0xfffffffe
002CAF70  mov      dword ptr [rdi + 0x20], eax
002CAF73  or       eax, 0xffffffff
002CAF76  mov      word ptr [rbx + 0xec], ax
002CAF7D  mov      qword ptr [rbx + 0xd8], rbp
002CAF84  mov      eax, dword ptr [rip + 0x1dc45e6]  ; -> 0208F570
002CAF8A  mov      dword ptr [rbx + 0xe0], eax
002CAF90  test     dword ptr [rbp + 0x168], 0xf0000
002CAF9A  jne      0x2cafa5  ; -> 002CAFA5
002CAF9C  mov      rax, qword ptr [rbp + 0xd0]
002CAFA3  jmp      0x2cafac  ; -> 002CAFAC
002CAFA5  mov      rax, qword ptr [rbp + 0x118]
002CAFAC  mov      rax, qword ptr [rax + 0x98]
002CAFB3  mov      rbp, qword ptr [rsp + 0x48]
002CAFB8  mov      word ptr [rbx + 0xe4], ax
002CAFBF  shr      rax, 0x10
002CAFC3  mov      word ptr [rbx + 0xe6], ax
002CAFCA  xor      eax, eax
002CAFCC  mov      rbx, qword ptr [rsp + 0x58]
002CAFD1  add      rsp, 0x30
002CAFD5  pop      rdi
002CAFD6  ret      
```
