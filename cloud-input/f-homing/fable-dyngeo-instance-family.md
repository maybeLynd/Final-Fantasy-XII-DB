# F homing pack (FABLE): `16-UI/Dynamic-Geometry-Instances/dyngeo-instance-family.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 3. No bearing page cites them and no documented function calls them directly.

## 001B6110 (274 B, extent 001B6110-001B6222)

Documented callee on this page: `00213540`

```
001B6110  test     rcx, rcx
001B6113  je       0x1b6221  ; -> 001B6221
001B6119  push     rdi
001B611A  sub      rsp, 0x50
001B611E  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001B6127  mov      qword ptr [rsp + 0x60], rbx
001B612C  mov      rdi, rcx
001B612F  lea      rdx, [rsp + 0x28]
001B6134  call     0x1fde60  ; -> 001FDE60 fn
001B6139  nop      
001B613A  mov      rbx, qword ptr [rax]
001B613D  call     0x19ce20  ; -> 0019CE20 fn
001B6142  mov      rcx, rax
001B6145  mov      rdx, rbx
001B6148  call     0x19ca80  ; -> 0019CA80 fn
001B614D  mov      rbx, rax
001B6150  mov      r8, qword ptr [rsp + 0x38]
001B6155  mov      rcx, r8
001B6158  mov      rdx, qword ptr [rsp + 0x28]
001B615D  sub      rcx, rdx
001B6160  cmp      rcx, 1
001B6164  jle      0x1b617c  ; -> 001B617C
001B6166  sub      r8d, edx
001B6169  test     rdx, rdx
001B616C  je       0x1b617c  ; -> 001B617C
001B616E  lea      rcx, [rsp + 0x40]
001B6173  mov      rax, qword ptr [rsp + 0x40]
001B6178  call     qword ptr [rax + 0x18]
001B617B  nop      
001B617C  test     rbx, rbx
001B617F  je       0x1b6217  ; -> 001B6217
001B6185  add      rbx, 0x38
001B6189  mov      rcx, qword ptr [rbx]
001B618C  xor      r8d, r8d
001B618F  cmp      rcx, rbx
001B6192  lea      rdx, [rip + 0x2b05767]  ; -> 02CBB900
001B6199  cmove    rcx, r8
001B619D  test     rcx, rcx
001B61A0  je       0x1b6217  ; -> 001B6217
001B61A2  mov      rax, qword ptr [rcx + 0x50]
001B61A6  test     rax, rax
001B61A9  je       0x1b61c6  ; -> 001B61C6
001B61AB  nop      dword ptr [rax + rax]
001B61B0  cmp      rax, rdx
001B61B3  je       0x1b61c0  ; -> 001B61C0
001B61B5  mov      rax, qword ptr [rax + 0x78]
001B61B9  test     rax, rax
001B61BC  jne      0x1b61b0  ; -> 001B61B0
001B61BE  jmp      0x1b61c6  ; -> 001B61C6
001B61C0  cmp      dword ptr [rcx + 0x74], r8d
001B61C4  ja       0x1b61d1  ; -> 001B61D1
001B61C6  mov      rax, qword ptr [rcx]
001B61C9  mov      rcx, rax
001B61CC  cmp      rax, rbx
001B61CF  jmp      0x1b6199  ; -> 001B6199
001B61D1  test     rcx, rcx
001B61D4  je       0x1b6217  ; -> 001B6217
001B61D6  mov      rax, qword ptr [rcx + 0x50]
001B61DA  mov      edx, dword ptr [rax + 0x38]
001B61DD  mov      r8, qword ptr [rcx + 0x60]
001B61E1  mov      r9d, dword ptr [rax + 0xf8]
001B61E8  mov      rax, qword ptr [rcx + 0x10]
001B61EC  cmp      dword ptr [rcx + 0x74], 0
001B61F0  je       0x1b6217  ; -> 001B6217
001B61F2  cmp      r8, rax
001B61F5  jne      0x1b620b  ; -> 001B620B
001B61F7  nop      word ptr [rax + rax]
001B6200  add      r8, rdx
001B6203  mov      rax, qword ptr [rax]
001B6206  cmp      r8, rax
001B6209  je       0x1b6200  ; -> 001B6200
001B620B  lea      rdx, [r8 + r9]
001B620F  mov      rcx, rdi
001B6212  call     0x213540  ; -> 00213540 fn
001B6217  mov      rbx, qword ptr [rsp + 0x60]
001B621C  add      rsp, 0x50
001B6220  pop      rdi
001B6221  ret      
```

## 001B6230 (274 B, extent 001B6230-001B6342)

Documented callee on this page: `00213560`

```
001B6230  test     rcx, rcx
001B6233  je       0x1b6341  ; -> 001B6341
001B6239  push     rdi
001B623A  sub      rsp, 0x50
001B623E  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001B6247  mov      qword ptr [rsp + 0x60], rbx
001B624C  mov      rdi, rcx
001B624F  lea      rdx, [rsp + 0x28]
001B6254  call     0x1fdf10  ; -> 001FDF10 fn
001B6259  nop      
001B625A  mov      rbx, qword ptr [rax]
001B625D  call     0x19ce20  ; -> 0019CE20 fn
001B6262  mov      rcx, rax
001B6265  mov      rdx, rbx
001B6268  call     0x19ca80  ; -> 0019CA80 fn
001B626D  mov      rbx, rax
001B6270  mov      r8, qword ptr [rsp + 0x38]
001B6275  mov      rcx, r8
001B6278  mov      rdx, qword ptr [rsp + 0x28]
001B627D  sub      rcx, rdx
001B6280  cmp      rcx, 1
001B6284  jle      0x1b629c  ; -> 001B629C
001B6286  sub      r8d, edx
001B6289  test     rdx, rdx
001B628C  je       0x1b629c  ; -> 001B629C
001B628E  lea      rcx, [rsp + 0x40]
001B6293  mov      rax, qword ptr [rsp + 0x40]
001B6298  call     qword ptr [rax + 0x18]
001B629B  nop      
001B629C  test     rbx, rbx
001B629F  je       0x1b6337  ; -> 001B6337
001B62A5  add      rbx, 0x38
001B62A9  mov      rcx, qword ptr [rbx]
001B62AC  xor      r8d, r8d
001B62AF  cmp      rcx, rbx
001B62B2  lea      rdx, [rip + 0x2b05647]  ; -> 02CBB900
001B62B9  cmove    rcx, r8
001B62BD  test     rcx, rcx
001B62C0  je       0x1b6337  ; -> 001B6337
001B62C2  mov      rax, qword ptr [rcx + 0x50]
001B62C6  test     rax, rax
001B62C9  je       0x1b62e6  ; -> 001B62E6
001B62CB  nop      dword ptr [rax + rax]
001B62D0  cmp      rax, rdx
001B62D3  je       0x1b62e0  ; -> 001B62E0
001B62D5  mov      rax, qword ptr [rax + 0x78]
001B62D9  test     rax, rax
001B62DC  jne      0x1b62d0  ; -> 001B62D0
001B62DE  jmp      0x1b62e6  ; -> 001B62E6
001B62E0  cmp      dword ptr [rcx + 0x74], r8d
001B62E4  ja       0x1b62f1  ; -> 001B62F1
001B62E6  mov      rax, qword ptr [rcx]
001B62E9  mov      rcx, rax
001B62EC  cmp      rax, rbx
001B62EF  jmp      0x1b62b9  ; -> 001B62B9
001B62F1  test     rcx, rcx
001B62F4  je       0x1b6337  ; -> 001B6337
001B62F6  mov      rax, qword ptr [rcx + 0x50]
001B62FA  mov      edx, dword ptr [rax + 0x38]
001B62FD  mov      r8, qword ptr [rcx + 0x60]
001B6301  mov      r9d, dword ptr [rax + 0xf8]
001B6308  mov      rax, qword ptr [rcx + 0x10]
001B630C  cmp      dword ptr [rcx + 0x74], 0
001B6310  je       0x1b6337  ; -> 001B6337
001B6312  cmp      r8, rax
001B6315  jne      0x1b632b  ; -> 001B632B
001B6317  nop      word ptr [rax + rax]
001B6320  add      r8, rdx
001B6323  mov      rax, qword ptr [rax]
001B6326  cmp      r8, rax
001B6329  je       0x1b6320  ; -> 001B6320
001B632B  lea      rdx, [r8 + r9]
001B632F  mov      rcx, rdi
001B6332  call     0x213560  ; -> 00213560 fn
001B6337  mov      rbx, qword ptr [rsp + 0x60]
001B633C  add      rsp, 0x50
001B6340  pop      rdi
001B6341  ret      
```

## 006C8BF0 (92 B, extent 006C8BF0-006C8C4C)

Documented callee on this page: `006CB2A0`

```
006C8BF0  mov      qword ptr [rsp + 8], rbx
006C8BF5  mov      qword ptr [rsp + 0x10], rbp
006C8BFA  mov      qword ptr [rsp + 0x18], rsi
006C8BFF  push     rdi
006C8C00  sub      rsp, 0x30
006C8C04  mov      edi, r9d
006C8C07  mov      rsi, r8
006C8C0A  mov      ebp, edx
006C8C0C  mov      rbx, rcx
006C8C0F  call     0x6cb2a0  ; -> 006CB2A0 fn
006C8C14  mov      r9d, dword ptr [rsp + 0x68]
006C8C19  lea      rcx, [rbx + 0x880]
006C8C20  mov      r8, qword ptr [rsp + 0x60]
006C8C25  mov      edx, ebp
006C8C27  mov      dword ptr [rsp + 0x28], edi
006C8C2B  mov      qword ptr [rsp + 0x20], rsi
006C8C30  call     0x6da470  ; -> 006DA470 fn
006C8C35  mov      rbx, qword ptr [rsp + 0x40]
006C8C3A  xor      eax, eax
006C8C3C  mov      rbp, qword ptr [rsp + 0x48]
006C8C41  mov      rsi, qword ptr [rsp + 0x50]
006C8C46  add      rsp, 0x30
006C8C4A  pop      rdi
006C8C4B  ret      
```
