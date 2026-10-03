# F homing pack (FABLE): `17-Presentation-Rendering/Character-Rendering/character-render-object.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 3. No bearing page cites them and no documented function calls them directly.

## 001E5370 (182 B, extent 001E5370-001E5426)

Documented callee on this page: `001E3D80`

```
001E5370  push     rdi
001E5372  sub      rsp, 0x40
001E5376  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001E537F  mov      qword ptr [rsp + 0x50], rbx
001E5384  mov      qword ptr [rsp + 0x58], rsi
001E5389  mov      edi, edx
001E538B  mov      rbx, rcx
001E538E  mov      r9, qword ptr [rcx + 8]
001E5392  mov      r10, qword ptr [rcx]
001E5395  mov      rdx, r9
001E5398  sub      rdx, r10
001E539B  movabs   rsi, 0x2aaaaaaaaaaaaaab
001E53A5  mov      rax, rsi
001E53A8  imul     rdx
001E53AB  sar      rdx, 2
001E53AF  mov      r8, rdx
001E53B2  shr      r8, 0x3f
001E53B6  add      rdx, r8
001E53B9  cmp      edi, edx
001E53BB  jbe      0x1e5403  ; -> 001E5403
001E53BD  lea      rcx, [rsp + 0x28]
001E53C2  call     0x212c20  ; -> 00212C20 fn
001E53C7  mov      r9, rax
001E53CA  mov      rcx, qword ptr [rbx + 8]
001E53CE  sub      rcx, qword ptr [rbx]
001E53D1  mov      rax, rsi
001E53D4  imul     rcx
001E53D7  sar      rdx, 2
001E53DB  mov      rcx, rdx
001E53DE  shr      rcx, 0x3f
001E53E2  add      rdx, rcx
001E53E5  sub      edi, edx
001E53E7  mov      r8d, edi
001E53EA  mov      rdx, qword ptr [rbx + 8]
001E53EE  mov      rcx, rbx
001E53F1  call     0x1e2250  ; -> 001E2250 fn
001E53F6  nop      
001E53F7  lea      rcx, [rsp + 0x28]
001E53FC  call     0x212c50  ; -> 00212C50 fn
001E5401  jmp      0x1e5416  ; -> 001E5416
001E5403  lea      rcx, [rdi + rdi*2]
001E5407  lea      rdx, [r10 + rcx*8]
001E540B  mov      r8, r9
001E540E  mov      rcx, rbx
001E5411  call     0x1e3d80  ; -> 001E3D80 fn
001E5416  mov      rbx, qword ptr [rsp + 0x50]
001E541B  mov      rsi, qword ptr [rsp + 0x58]
001E5420  add      rsp, 0x40
001E5424  pop      rdi
001E5425  ret      
```

## 001F4C50 (323 B, extent 001F4C50-001F4D93)

Documented callee on this page: `001F8A70`

```
001F4C50  mov      qword ptr [rsp + 8], rcx
001F4C55  push     rbx
001F4C56  push     rbp
001F4C57  push     rsi
001F4C58  push     rdi
001F4C59  push     r14
001F4C5B  push     r15
001F4C5D  sub      rsp, 0x48
001F4C61  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001F4C6A  mov      r15d, edx
001F4C6D  mov      r14, rcx
001F4C70  xor      edi, edi
001F4C72  mov      qword ptr [rcx], rdi
001F4C75  mov      qword ptr [rcx + 8], rdi
001F4C79  mov      qword ptr [rcx + 0x10], rdi
001F4C7D  add      rcx, 0x18
001F4C81  lea      rdx, [rip + 0x6d12d0]  ; -> 008C5F58 [str "EASTL vector"]
001F4C88  call     0x1edf00  ; -> 001EDF00 fn
001F4C8D  nop      
001F4C8E  lea      rdx, [rip + 0x6ff01b]  ; -> 008F3CB0 [str "EASTL set"]
001F4C95  lea      rcx, [rsp + 0x90]
001F4C9D  call     0x1edf00  ; -> 001EDF00 fn
001F4CA2  lea      rbp, [r14 + 0x20]
001F4CA6  mov      qword ptr [rsp + 0x98], rbp
001F4CAE  lea      rbx, [rbp + 8]
001F4CB2  xor      ecx, ecx
001F4CB4  mov      qword ptr [rbx], rcx
001F4CB7  mov      qword ptr [rbx + 8], rcx
001F4CBB  mov      qword ptr [rbx + 0x10], rcx
001F4CBF  mov      qword ptr [rbx + 0x18], rcx
001F4CC3  mov      dword ptr [rbp + 0x28], edi
001F4CC6  lea      rcx, [rbp + 0x30]
001F4CCA  mov      rdx, rax
001F4CCD  call     0x1edf00  ; -> 001EDF00 fn
001F4CD2  mov      qword ptr [rbx], rbx
001F4CD5  mov      qword ptr [rbp + 0x10], rbx
001F4CD9  mov      qword ptr [rbp + 0x18], rdi
001F4CDD  mov      byte ptr [rbp + 0x20], dil
001F4CE1  mov      dword ptr [rbp + 0x28], edi
001F4CE4  lea      rdx, [rip + 0x6fefc5]  ; -> 008F3CB0 [str "EASTL set"]
001F4CEB  lea      rcx, [rsp + 0x98]
001F4CF3  call     0x1edf00  ; -> 001EDF00 fn
001F4CF8  lea      rsi, [r14 + 0x58]
001F4CFC  mov      qword ptr [rsp + 0x28], rsi
001F4D01  lea      rbx, [rsi + 8]
001F4D05  xor      ecx, ecx
001F4D07  mov      qword ptr [rbx], rcx
001F4D0A  mov      qword ptr [rbx + 8], rcx
001F4D0E  mov      qword ptr [rbx + 0x10], rcx
001F4D12  mov      qword ptr [rbx + 0x18], rcx
001F4D16  mov      dword ptr [rsi + 0x28], edi
001F4D19  lea      rcx, [rsi + 0x30]
001F4D1D  mov      rdx, rax
001F4D20  call     0x1edf00  ; -> 001EDF00 fn
001F4D25  mov      qword ptr [rbx], rbx
001F4D28  mov      qword ptr [rsi + 0x10], rbx
001F4D2C  mov      qword ptr [rsi + 0x18], rdi
001F4D30  mov      byte ptr [rsi + 0x20], dil
001F4D34  mov      dword ptr [rsi + 0x28], edi
001F4D37  mov      edx, r15d
001F4D3A  mov      rcx, r14
001F4D3D  call     0x1f8a70  ; -> 001F8A70 fn
001F4D42  test     r15d, r15d
001F4D45  je       0x1f4d83  ; -> 001F4D83
001F4D47  mov      esi, r15d
001F4D4A  movzx    ebx, byte ptr [rsp + 0x88]
001F4D52  mov      rcx, qword ptr [r14]
001F4D55  add      rcx, rdi
001F4D58  mov      qword ptr [rsp + 0x90], rcx
001F4D60  movzx    r9d, bl
001F4D64  lea      r8, [rsp + 0x90]
001F4D6C  lea      rdx, [rsp + 0x28]
001F4D71  mov      rcx, rbp
001F4D74  call     0x199db0  ; -> 00199DB0 fn
001F4D79  add      rdi, 0x18
001F4D7D  sub      rsi, 1
001F4D81  jne      0x1f4d52  ; -> 001F4D52
001F4D83  mov      rax, r14
001F4D86  add      rsp, 0x48
001F4D8A  pop      r15
001F4D8C  pop      r14
001F4D8E  pop      rdi
001F4D8F  pop      rsi
001F4D90  pop      rbp
001F4D91  pop      rbx
001F4D92  ret      
```

## 0042E130 (63 B, extent 0042E130-0042E16F)

Documented callee on this page: `00426220`

```
0042E130  push     rbx
0042E132  sub      rsp, 0x20
0042E136  mov      rdx, qword ptr [rdx + 8]
0042E13A  mov      rbx, rcx
0042E13D  call     0x426220  ; -> 00426220 fn
0042E142  test     eax, eax
0042E144  jne      0x42e169  ; -> 0042E169
0042E146  mov      eax, 0x1000
0042E14B  cmp      word ptr [rbx + 0x3fa], ax
0042E152  jae      0x42e15c  ; -> 0042E15C
0042E154  mov      rcx, rbx
0042E157  call     0x41fc80  ; -> 0041FC80 fn
0042E15C  mov      rcx, rbx
0042E15F  add      rsp, 0x20
0042E163  pop      rbx
0042E164  jmp      0x423a10  ; -> 00423A10 fn
0042E169  add      rsp, 0x20
0042E16D  pop      rbx
0042E16E  ret      
```
