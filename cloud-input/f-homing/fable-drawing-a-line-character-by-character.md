# F homing pack (FABLE): `99-Unresolved-Residual/Glyph-Run-Rendering/drawing-a-line-character-by-character.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 4. No bearing page cites them and no documented function calls them directly.

## 002CB4B0 (733 B, extent 002CB4B0-002CB78D)

Documented callee on this page: `002DD7E0`

```
002CB4B0  mov      qword ptr [rsp + 0x10], rbx
002CB4B5  push     rdi
002CB4B6  sub      rsp, 0x20
002CB4BA  mov      rdi, rcx
002CB4BD  mov      rbx, rdx
002CB4C0  mov      ecx, dword ptr [rdx]
002CB4C2  sub      ecx, 1
002CB4C5  je       0x2cb60b  ; -> 002CB60B
002CB4CB  sub      ecx, 1
002CB4CE  je       0x2cb4eb  ; -> 002CB4EB
002CB4D0  cmp      ecx, 2
002CB4D3  je       0x2cb780  ; -> 002CB780
002CB4D9  mov      rcx, rdi
002CB4DC  mov      rbx, qword ptr [rsp + 0x38]
002CB4E1  add      rsp, 0x20
002CB4E5  pop      rdi
002CB4E6  jmp      0x5c5230  ; -> 005C5230 fn
002CB4EB  mov      rcx, rdi
002CB4EE  call     0x2ca2e0  ; -> 002CA2E0 fn
002CB4F3  mov      rax, qword ptr [rdi + 0xd8]
002CB4FA  test     dword ptr [rax + 0x168], 0xf0000
002CB504  jne      0x2cb517  ; -> 002CB517
002CB506  and      dword ptr [rdi + 0x50], 0xfffffffe
002CB50A  xor      eax, eax
002CB50C  mov      rbx, qword ptr [rsp + 0x38]
002CB511  add      rsp, 0x20
002CB515  pop      rdi
002CB516  ret      
002CB517  or       dword ptr [rdi + 0x50], 1
002CB51B  mov      rax, qword ptr [rdi + 0x60]
002CB51F  mov      rcx, qword ptr [rax + 0x58]
002CB523  or       dword ptr [rcx + 8], 1
002CB527  mov      rax, qword ptr [rdi + 0x60]
002CB52B  mov      edx, dword ptr [rdi + 0xe4]
002CB531  and      edx, 1
002CB534  mov      rcx, qword ptr [rax]
002CB537  and      dword ptr [rcx + 8], 0xfffffffe
002CB53B  or       dword ptr [rcx + 8], edx
002CB53E  mov      rax, qword ptr [rdi + 0x60]
002CB542  mov      edx, dword ptr [rdi + 0xe4]
002CB548  and      edx, 1
002CB54B  mov      rcx, qword ptr [rax + 8]
002CB54F  and      dword ptr [rcx + 8], 0xfffffffe
002CB553  or       dword ptr [rcx + 8], edx
002CB556  mov      rax, qword ptr [rdi + 0x60]
002CB55A  mov      edx, dword ptr [rdi + 0xe4]
002CB560  and      edx, 1
002CB563  mov      rcx, qword ptr [rax + 0x10]
002CB567  and      dword ptr [rcx + 8], 0xfffffffe
002CB56B  or       dword ptr [rcx + 8], edx
002CB56E  mov      rax, qword ptr [rdi + 0x60]
002CB572  mov      edx, dword ptr [rdi + 0xe4]
002CB578  and      edx, 1
002CB57B  mov      rcx, qword ptr [rax + 0x18]
002CB57F  and      dword ptr [rcx + 8], 0xfffffffe
002CB583  or       dword ptr [rcx + 8], edx
002CB586  mov      rax, qword ptr [rdi + 0x60]
002CB58A  mov      edx, dword ptr [rdi + 0xe4]
002CB590  and      edx, 1
002CB593  mov      rcx, qword ptr [rax + 0x20]
002CB597  and      dword ptr [rcx + 8], 0xfffffffe
002CB59B  or       dword ptr [rcx + 8], edx
002CB59E  mov      rax, qword ptr [rdi + 0x60]
002CB5A2  mov      edx, dword ptr [rdi + 0xe4]
002CB5A8  and      edx, 1
002CB5AB  mov      rcx, qword ptr [rax + 0x28]
002CB5AF  and      dword ptr [rcx + 8], 0xfffffffe
002CB5B3  or       dword ptr [rcx + 8], edx
002CB5B6  mov      rax, qword ptr [rdi + 0x60]
002CB5BA  mov      edx, dword ptr [rdi + 0xe4]
002CB5C0  and      edx, 1
002CB5C3  mov      rcx, qword ptr [rax + 0x30]
002CB5C7  and      dword ptr [rcx + 8], 0xfffffffe
002CB5CB  or       dword ptr [rcx + 8], edx
002CB5CE  mov      rax, qword ptr [rdi + 0x60]
002CB5D2  mov      edx, dword ptr [rdi + 0xe4]
002CB5D8  and      edx, 1
002CB5DB  mov      rcx, qword ptr [rax + 0x38]
002CB5DF  and      dword ptr [rcx + 8], 0xfffffffe
002CB5E3  or       dword ptr [rcx + 8], edx
002CB5E6  mov      rax, qword ptr [rdi + 0x60]
002CB5EA  mov      edx, dword ptr [rdi + 0xe4]
002CB5F0  and      edx, 1
002CB5F3  mov      rcx, qword ptr [rax + 0x40]
002CB5F7  and      dword ptr [rcx + 8], 0xfffffffe
002CB5FB  or       dword ptr [rcx + 8], edx
002CB5FE  xor      eax, eax
002CB600  mov      rbx, qword ptr [rsp + 0x38]
002CB605  add      rsp, 0x20
002CB609  pop      rdi
002CB60A  ret      
002CB60B  mov      rax, qword ptr [rip + 0x1dcf61e]  ; -> 0209AC30
002CB612  lea      rcx, [rdi + 0x50]
002CB616  mov      r9, rdi
002CB619  mov      qword ptr [rsp + 0x30], rsi
002CB61E  mov      r8d, 9
002CB624  mov      rdx, qword ptr [rax + 0x38]
002CB628  call     0x2432b0  ; -> 002432B0 fn
002CB62D  movzx    ecx, word ptr [rax + 0xa]
002CB631  movzx    edx, word ptr [rax + 8]
002CB635  movsx    r8d, word ptr [rax + 6]
002CB63A  test     rdi, rdi
002CB63D  je       0x2cb660  ; -> 002CB660
002CB63F  movzx    eax, word ptr [rax + 4]
002CB643  mov      word ptr [rdi + 0x98], ax
002CB64A  mov      word ptr [rdi + 0x9a], r8w
002CB652  mov      word ptr [rdi + 0x9c], dx
002CB659  mov      word ptr [rdi + 0x9e], cx
002CB660  mov      eax, dword ptr [rbx + 8]
002CB663  mov      dword ptr [rdi + 0xd4], eax
002CB669  mov      rax, qword ptr [rbx + 0x10]
002CB66D  mov      qword ptr [rdi + 0xd8], rax
002CB674  test     dword ptr [rax + 0x168], 0xf0000
002CB67E  jne      0x2cb689  ; -> 002CB689
002CB680  and      dword ptr [rdi + 0x50], 0xfffffffe
002CB684  jmp      0x2cb72b  ; -> 002CB72B
002CB689  or       dword ptr [rdi + 0x50], 1
002CB68D  mov      rax, qword ptr [rdi + 0x60]
002CB691  mov      rcx, qword ptr [rax + 0x58]
002CB695  or       dword ptr [rcx + 8], 1
002CB699  mov      rax, qword ptr [rdi + 0x60]
002CB69D  mov      rcx, qword ptr [rax]
002CB6A0  or       dword ptr [rcx + 8], 1
002CB6A4  mov      rax, qword ptr [rdi + 0x60]
002CB6A8  mov      rcx, qword ptr [rax + 8]
002CB6AC  or       dword ptr [rcx + 8], 1
002CB6B0  mov      rax, qword ptr [rdi + 0x60]
002CB6B4  mov      rcx, qword ptr [rax + 0x10]
002CB6B8  or       dword ptr [rcx + 8], 1
002CB6BC  mov      rax, qword ptr [rdi + 0x60]
002CB6C0  mov      rcx, qword ptr [rax + 0x18]
002CB6C4  or       dword ptr [rcx + 8], 1
002CB6C8  mov      rax, qword ptr [rdi + 0x60]
002CB6CC  mov      rcx, qword ptr [rax + 0x20]
002CB6D0  or       dword ptr [rcx + 8], 1
002CB6D4  mov      rax, qword ptr [rdi + 0x60]
002CB6D8  mov      rcx, qword ptr [rax + 0x28]
002CB6DC  or       dword ptr [rcx + 8], 1
002CB6E0  mov      rax, qword ptr [rdi + 0x60]
002CB6E4  mov      rcx, qword ptr [rax + 0x30]
002CB6E8  or       dword ptr [rcx + 8], 1
002CB6EC  mov      rax, qword ptr [rdi + 0x60]
002CB6F0  mov      rcx, qword ptr [rax + 0x38]
002CB6F4  or       dword ptr [rcx + 8], 1
002CB6F8  mov      rax, qword ptr [rdi + 0x60]
002CB6FC  mov      rcx, qword ptr [rax + 0x40]
002CB700  or       dword ptr [rcx + 8], 1
002CB704  mov      rax, qword ptr [rdi + 0x60]
002CB708  mov      rcx, qword ptr [rax + 0x80]
002CB70F  and      dword ptr [rcx + 8], 0xfffffffe
002CB713  mov      rax, qword ptr [rdi + 0x60]
002CB717  mov      rcx, qword ptr [rax + 0x50]
002CB71B  and      dword ptr [rcx + 8], 0xfffffffe
002CB71F  mov      rax, qword ptr [rdi + 0x60]
002CB723  mov      rcx, qword ptr [rax + 0x48]
002CB727  and      dword ptr [rcx + 8], 0xfffffffe
002CB72B  mov      rax, qword ptr [rdi + 0x60]
002CB72F  mov      ecx, 0xf5
002CB734  mov      rbx, qword ptr [rax + 0x50]
002CB738  call     0x2dd7e0  ; -> 002DD7E0 fn
002CB73D  mov      dword ptr [rbx + 0x34], eax
002CB740  mov      ecx, 0xf4
002CB745  mov      dword ptr [rbx + 0x30], eax
002CB748  mov      dword ptr [rbx + 0x2c], eax
002CB74B  mov      dword ptr [rbx + 0x28], eax
002CB74E  mov      rax, qword ptr [rdi + 0x60]
002CB752  mov      rbx, qword ptr [rax + 0x48]
002CB756  call     0x2dd7e0  ; -> 002DD7E0 fn
002CB75B  mov      dword ptr [rbx + 0x34], eax
002CB75E  mov      edx, 0x65
002CB763  mov      dword ptr [rbx + 0x30], eax
002CB766  mov      rcx, rdi
002CB769  mov      dword ptr [rbx + 0x2c], eax
002CB76C  mov      dword ptr [rbx + 0x28], eax
002CB76F  and      dword ptr [rdi + 0x40], 0xfffff7ff
002CB776  call     0x247930  ; -> 00247930 fn
002CB77B  mov      rsi, qword ptr [rsp + 0x30]
002CB780  xor      eax, eax
002CB782  mov      rbx, qword ptr [rsp + 0x38]
002CB787  add      rsp, 0x20
002CB78B  pop      rdi
002CB78C  ret      
```

## 00559910 (192 B, extent 00559910-005599D0)

Documented callee on this page: `002DD7E0`

```
00559910  mov      qword ptr [rsp + 8], rbx
00559915  mov      qword ptr [rsp + 0x10], rbp
0055991A  mov      qword ptr [rsp + 0x18], rsi
0055991F  push     rdi
00559920  sub      rsp, 0x20
00559924  mov      rax, qword ptr [rdx + 0x10]
00559928  mov      rbp, rdx
0055992B  movsxd   rdi, r9d
0055992E  xor      ebx, ebx
00559930  shl      rdi, 5
00559934  add      rdi, rcx
00559937  xor      ecx, ecx
00559939  mov      rsi, qword ptr [rax + 8]
0055993D  mov      rax, qword ptr [rdi + 0xe8]
00559944  mov      qword ptr [rsi + 0x18], rax
00559948  call     0x20e620  ; -> 0020E620 fn
0055994D  mov      dword ptr [rsi + 0x20], eax
00559950  cmp      word ptr [rdi + 0xf4], bx
00559957  je       0x55995d  ; -> 0055995D
00559959  xor      ecx, ecx
0055995B  jmp      0x559962  ; -> 00559962
0055995D  mov      ecx, 2
00559962  call     0x2dd7e0  ; -> 002DD7E0 fn
00559967  mov      dword ptr [rsi + 0x24], eax
0055996A  mov      r10d, 1
00559970  mov      eax, 0xffff
00559975  cmp      word ptr [rdi + 0xf0], ax
0055997C  je       0x559989  ; -> 00559989
0055997E  cmp      byte ptr [rdi + 0xf2], 0xff
00559985  cmovne   ebx, r10d
00559989  mov      rcx, qword ptr [rbp + 0x10]
0055998D  mov      eax, r10d
00559990  mov      r9, qword ptr [rcx]
00559993  and      dword ptr [r9 + 8], 0xfffffffe
00559998  or       dword ptr [r9 + 8], ebx
0055999C  test     ebx, ebx
0055999E  je       0x5599bb  ; -> 005599BB
005599A0  movzx    r8d, byte ptr [rdi + 0xf2]
005599A8  mov      rcx, qword ptr [r9 + 0x20]
005599AC  movzx    edx, byte ptr [rcx + r8*8 + 7]
005599B2  mov      byte ptr [r9 + 0x39], dl
005599B6  mov      word ptr [r9 + 0xa], r8w
005599BB  mov      rbx, qword ptr [rsp + 0x30]
005599C0  mov      rbp, qword ptr [rsp + 0x38]
005599C5  mov      rsi, qword ptr [rsp + 0x40]
005599CA  add      rsp, 0x20
005599CE  pop      rdi
005599CF  ret      
```

## 005639D0 (316 B, extent 005639D0-00563B0C)

Documented callee on this page: `002DD7E0`

```
005639D0  mov      qword ptr [rsp + 0x10], rbx
005639D5  mov      qword ptr [rsp + 0x18], rbp
005639DA  mov      qword ptr [rsp + 0x20], rsi
005639DF  push     r14
005639E1  sub      rsp, 0x20
005639E5  mov      rax, qword ptr [rcx + 0xe0]
005639EC  mov      rsi, rdx
005639EF  movsxd   r14, r9d
005639F2  mov      rbp, rcx
005639F5  test     rax, rax
005639F8  jne      0x563a44  ; -> 00563A44
005639FA  xor      edx, edx
005639FC  mov      rcx, rsi
005639FF  call     0x243580  ; -> 00243580 fn
00563A04  mov      rax, qword ptr [rsi + 0x10]
00563A08  mov      ecx, 0x7d8
00563A0D  mov      rbx, qword ptr [rax + 8]
00563A11  or       dword ptr [rbx + 8], 1
00563A15  call     0x2f9860  ; -> 002F9860 fn
00563A1A  xor      ecx, ecx
00563A1C  mov      qword ptr [rbx + 0x18], rax
00563A20  call     0x20e620  ; -> 0020E620 fn
00563A25  mov      rcx, qword ptr [rbx]
00563A28  mov      dword ptr [rbx + 0x20], eax
00563A2B  movzx    eax, word ptr [rcx + 4]
00563A2F  sub      ax, 0x14
00563A33  mov      word ptr [rbx + 0xc], ax
00563A37  movzx    eax, word ptr [rcx + 6]
00563A3B  mov      word ptr [rbx + 0xe], ax
00563A3F  jmp      0x563af1  ; -> 00563AF1
00563A44  mov      rbx, r14
00563A47  mov      qword ptr [rsp + 0x30], rdi
00563A4C  shl      rbx, 5
00563A50  add      rbx, rax
00563A53  mov      rax, qword ptr [rdx + 0x10]
00563A57  cmp      byte ptr [rbx + 0xa], 0xff
00563A5B  mov      r8, qword ptr [rax]
00563A5E  jne      0x563a67  ; -> 00563A67
00563A60  and      dword ptr [r8 + 8], 0xfffffffe
00563A65  jmp      0x563a82  ; -> 00563A82
00563A67  or       dword ptr [r8 + 8], 1
00563A6C  movzx    edx, byte ptr [rbx + 0xa]
00563A70  mov      rax, qword ptr [r8 + 0x20]
00563A74  movzx    ecx, byte ptr [rax + rdx*8 + 7]
00563A79  mov      byte ptr [r8 + 0x39], cl
00563A7D  mov      word ptr [r8 + 0xa], dx
00563A82  mov      rax, qword ptr [rsi + 0x10]
00563A86  xor      ecx, ecx
00563A88  mov      rdi, qword ptr [rax + 8]
00563A8C  mov      rax, qword ptr [rbx]
00563A8F  mov      qword ptr [rdi + 0x18], rax
00563A93  call     0x20e620  ; -> 0020E620 fn
00563A98  mov      rcx, qword ptr [rdi]
00563A9B  mov      dword ptr [rdi + 0x20], eax
00563A9E  movzx    eax, word ptr [rcx + 4]
00563AA2  mov      word ptr [rdi + 0xc], ax
00563AA6  movzx    eax, word ptr [rcx + 6]
00563AAA  mov      word ptr [rdi + 0xe], ax
00563AAE  test     dword ptr [rbp + 0x180], 0x100
00563AB8  je       0x563acd  ; -> 00563ACD
00563ABA  movsx    eax, word ptr [rbp + 0x17c]
00563AC1  cmp      eax, r14d
00563AC4  jne      0x563acd  ; -> 00563ACD
00563AC6  mov      ecx, 6
00563ACB  jmp      0x563acf  ; -> 00563ACF
00563ACD  xor      ecx, ecx
00563ACF  call     0x2dd7e0  ; -> 002DD7E0 fn
00563AD4  mov      r9d, 7
00563ADA  mov      dword ptr [rdi + 0x24], eax
00563ADD  mov      rdx, rbx
00563AE0  mov      rcx, rsi
00563AE3  lea      r8d, [r9 - 5]
00563AE7  call     0x3fcad0  ; -> 003FCAD0 fn
00563AEC  mov      rdi, qword ptr [rsp + 0x30]
00563AF1  mov      rbx, qword ptr [rsp + 0x38]
00563AF6  mov      eax, 1
00563AFB  mov      rbp, qword ptr [rsp + 0x40]
00563B00  mov      rsi, qword ptr [rsp + 0x48]
00563B05  add      rsp, 0x20
00563B09  pop      r14
00563B0B  ret      
```

## 00563C00 (274 B, extent 00563C00-00563D12)

Documented callee on this page: `002DD7E0`

```
00563C00  mov      qword ptr [rsp + 8], rbx
00563C05  mov      qword ptr [rsp + 0x10], rsi
00563C0A  push     rdi
00563C0B  sub      rsp, 0x20
00563C0F  mov      rax, qword ptr [rcx + 0xe0]
00563C16  mov      rbx, rdx
00563C19  movsxd   rsi, r9d
00563C1C  mov      rdi, rcx
00563C1F  test     rax, rax
00563C22  jne      0x563c6e  ; -> 00563C6E
00563C24  xor      edx, edx
00563C26  mov      rcx, rbx
00563C29  call     0x243580  ; -> 00243580 fn
00563C2E  mov      rax, qword ptr [rbx + 0x10]
00563C32  mov      ecx, 0x7d8
00563C37  mov      rbx, qword ptr [rax + 8]
00563C3B  or       dword ptr [rbx + 8], 1
00563C3F  call     0x2f9860  ; -> 002F9860 fn
00563C44  xor      ecx, ecx
00563C46  mov      qword ptr [rbx + 0x18], rax
00563C4A  call     0x20e620  ; -> 0020E620 fn
00563C4F  mov      rcx, qword ptr [rbx]
00563C52  mov      dword ptr [rbx + 0x20], eax
00563C55  movzx    eax, word ptr [rcx + 4]
00563C59  sub      ax, 0x14
00563C5D  mov      word ptr [rbx + 0xc], ax
00563C61  movzx    eax, word ptr [rcx + 6]
00563C65  mov      word ptr [rbx + 0xe], ax
00563C69  jmp      0x563cfd  ; -> 00563CFD
00563C6E  mov      r9, rsi
00563C71  shl      r9, 5
00563C75  add      r9, rax
00563C78  mov      rax, qword ptr [rdx + 0x10]
00563C7C  cmp      byte ptr [r9 + 0xa], 0xff
00563C81  mov      r8, qword ptr [rax]
00563C84  jne      0x563c8d  ; -> 00563C8D
00563C86  and      dword ptr [r8 + 8], 0xfffffffe
00563C8B  jmp      0x563ca9  ; -> 00563CA9
00563C8D  or       dword ptr [r8 + 8], 1
00563C92  movzx    edx, byte ptr [r9 + 0xa]
00563C97  mov      rax, qword ptr [r8 + 0x20]
00563C9B  movzx    ecx, byte ptr [rax + rdx*8 + 7]
00563CA0  mov      byte ptr [r8 + 0x39], cl
00563CA4  mov      word ptr [r8 + 0xa], dx
00563CA9  mov      rax, qword ptr [rbx + 0x10]
00563CAD  xor      ecx, ecx
00563CAF  mov      rbx, qword ptr [rax + 8]
00563CB3  mov      rax, qword ptr [r9]
00563CB6  mov      qword ptr [rbx + 0x18], rax
00563CBA  call     0x20e620  ; -> 0020E620 fn
00563CBF  mov      rcx, qword ptr [rbx]
00563CC2  mov      dword ptr [rbx + 0x20], eax
00563CC5  movzx    eax, word ptr [rcx + 4]
00563CC9  mov      word ptr [rbx + 0xc], ax
00563CCD  movzx    eax, word ptr [rcx + 6]
00563CD1  mov      word ptr [rbx + 0xe], ax
00563CD5  test     dword ptr [rdi + 0x180], 0x100
00563CDF  je       0x563cf3  ; -> 00563CF3
00563CE1  movsx    eax, word ptr [rdi + 0x17c]
00563CE8  cmp      eax, esi
00563CEA  jne      0x563cf3  ; -> 00563CF3
00563CEC  mov      ecx, 6
00563CF1  jmp      0x563cf5  ; -> 00563CF5
00563CF3  xor      ecx, ecx
00563CF5  call     0x2dd7e0  ; -> 002DD7E0 fn
00563CFA  mov      dword ptr [rbx + 0x24], eax
00563CFD  mov      rbx, qword ptr [rsp + 0x30]
00563D02  mov      eax, 1
00563D07  mov      rsi, qword ptr [rsp + 0x38]
00563D0C  add      rsp, 0x20
00563D10  pop      rdi
00563D11  ret      
```
