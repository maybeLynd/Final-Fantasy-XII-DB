# F homing pack: `19-Save-Load-Settings/CONTRACT-save-image-buffers.md`

Generated 2026-10-02 22:03 by OPUS (homing_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 2. No bearing page cites them and no documented function calls them directly.

## 001AA120 (280 B, extent 001AA120-001AA238)

Documented callee on this page: `00183320`

```
001AA120  mov      rax, rsp
001AA123  push     rdi
001AA124  push     r14
001AA126  sub      rsp, 0x88
001AA12D  mov      r14, qword ptr [rcx + 0x2a8]
001AA134  mov      rdi, qword ptr [rcx + 0x2a0]
001AA13B  cmp      rdi, r14
001AA13E  je       0x1aa22d  ; -> 001AA22D
001AA144  mov      qword ptr [rax + 0x18], rbx
001AA148  movzx    ebx, byte ptr [rax + 8]
001AA14C  mov      qword ptr [rax + 0x20], rbp
001AA150  lea      rbp, [rcx + 0x268]
001AA157  mov      qword ptr [rax - 0x18], rsi
001AA15B  lea      rsi, [rbp + 8]
001AA15F  nop      
001AA160  movups   xmm0, xmmword ptr [rdi]
001AA163  mov      rax, qword ptr [rbp + 0x18]
001AA167  mov      rcx, rsi
001AA16A  movups   xmm1, xmmword ptr [rdi + 0x10]
001AA16E  movups   xmmword ptr [rsp + 0x58], xmm0
001AA173  mov      edx, dword ptr [rsp + 0x58]
001AA177  movups   xmmword ptr [rsp + 0x68], xmm1
001AA17C  test     rax, rax
001AA17F  je       0x1aa197  ; -> 001AA197
001AA181  cmp      dword ptr [rax + 0x20], edx
001AA184  jl       0x1aa18f  ; -> 001AA18F
001AA186  mov      rcx, rax
001AA189  mov      rax, qword ptr [rax + 8]
001AA18D  jmp      0x1aa192  ; -> 001AA192
001AA18F  mov      rax, qword ptr [rax]
001AA192  test     rax, rax
001AA195  jne      0x1aa181  ; -> 001AA181
001AA197  cmp      rcx, rsi
001AA19A  je       0x1aa1a1  ; -> 001AA1A1
001AA19C  cmp      edx, dword ptr [rcx + 0x20]
001AA19F  jge      0x1aa1de  ; -> 001AA1DE
001AA1A1  xorps    xmm0, xmm0
001AA1A4  mov      dword ptr [rsp + 0x40], edx
001AA1A8  mov      qword ptr [rsp + 0xa0], rcx
001AA1B0  lea      rdx, [rsp + 0xa8]
001AA1B8  mov      rcx, rbp
001AA1BB  mov      byte ptr [rsp + 0x20], bl
001AA1BF  lea      r9, [rsp + 0x40]
001AA1C4  lea      r8, [rsp + 0xa0]
001AA1CC  movups   xmmword ptr [rsp + 0x48], xmm0
001AA1D1  call     0x1a37c0  ; -> 001A37C0 fn
001AA1D6  mov      rcx, qword ptr [rsp + 0xa8]
001AA1DE  mov      eax, dword ptr [rsp + 0x70]
001AA1E2  movzx    r9d, word ptr [rsp + 0x6a]
001AA1E8  movzx    r8d, word ptr [rsp + 0x68]
001AA1EE  mov      rdx, qword ptr [rsp + 0x60]
001AA1F3  mov      rcx, qword ptr [rcx + 0x28]
001AA1F7  mov      dword ptr [rsp + 0x28], eax
001AA1FB  mov      eax, dword ptr [rsp + 0x6c]
001AA1FF  mov      dword ptr [rsp + 0x20], eax
001AA203  call     0x183320  ; -> 00183320 fn
001AA208  add      rdi, 0x20
001AA20C  cmp      rdi, r14
001AA20F  jne      0x1aa160  ; -> 001AA160
001AA215  mov      rsi, qword ptr [rsp + 0x80]
001AA21D  mov      rbp, qword ptr [rsp + 0xb8]
001AA225  mov      rbx, qword ptr [rsp + 0xb0]
001AA22D  add      rsp, 0x88
001AA234  pop      r14
001AA236  pop      rdi
001AA237  ret      
```

## 005DDBB0 (164 B, extent 005DDBB0-005DDC54)

Documented callee on this page: `00616C60`

```
005DDBB0  push     rdi
005DDBB2  sub      rsp, 0x30
005DDBB6  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
005DDBBF  mov      qword ptr [rsp + 0x40], rbx
005DDBC4  mov      rbx, rcx
005DDBC7  add      rcx, 0x568
005DDBCE  call     0x6167c0  ; -> 006167C0 fn
005DDBD3  nop      
005DDBD4  lea      rcx, [rbx + 0x218]
005DDBDB  call     0x625f20  ; -> 00625F20 fn
005DDBE0  nop      
005DDBE1  test     al, al
005DDBE3  je       0x5ddbf2  ; -> 005DDBF2
005DDBE5  lea      rcx, [rbx + 0x218]
005DDBEC  call     0x62c100  ; -> 0062C100 fn
005DDBF1  nop      
005DDBF2  lea      rcx, [rbx + 0x218]
005DDBF9  call     0x616d20  ; -> 00616D20 fn
005DDBFE  nop      
005DDBFF  lea      rcx, [rbx + 0x188]
005DDC06  call     0x625f10  ; -> 00625F10 fn
005DDC0B  nop      
005DDC0C  test     al, al
005DDC0E  je       0x5ddc1d  ; -> 005DDC1D
005DDC10  lea      rcx, [rbx + 0x188]
005DDC17  call     0x62bf40  ; -> 0062BF40 fn
005DDC1C  nop      
005DDC1D  lea      rcx, [rbx + 0x188]
005DDC24  call     0x616cc0  ; -> 00616CC0 fn
005DDC29  nop      
005DDC2A  mov      rcx, rbx
005DDC2D  call     0x625f00  ; -> 00625F00 fn
005DDC32  nop      
005DDC33  test     al, al
005DDC35  je       0x5ddc40  ; -> 005DDC40
005DDC37  mov      rcx, rbx
005DDC3A  call     0x62bcb0  ; -> 0062BCB0 fn
005DDC3F  nop      
005DDC40  mov      rcx, rbx
005DDC43  call     0x616c60  ; -> 00616C60 fn
005DDC48  nop      
005DDC49  mov      rbx, qword ptr [rsp + 0x40]
005DDC4E  add      rsp, 0x30
005DDC52  pop      rdi
005DDC53  ret      
```
