# F homing pack (FABLE): `17-Presentation-Rendering/Model-And-Motion-Formats/adm-add-motion-tables.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 3. No bearing page cites them and no documented function calls them directly.

## 0034DEA0 (61 B, extent 0034DEA0-0034DEDD)

Documented callee on this page: `0025B470`

```
0034DEA0  push     rbx
0034DEA2  sub      rsp, 0x30
0034DEA6  mov      rcx, r9
0034DEA9  movaps   xmmword ptr [rsp + 0x20], xmm6
0034DEAE  mov      rbx, rdx
0034DEB1  call     0x267e10  ; -> 00267E10 fn
0034DEB6  mov      rcx, rbx
0034DEB9  movd     xmm6, eax
0034DEBD  cvtdq2ps xmm6, xmm6
0034DEC0  movaps   xmm1, xmm6
0034DEC3  call     0x26dac0  ; -> 0026DAC0 fn
0034DEC8  movaps   xmm1, xmm6
0034DECB  mov      rcx, rbx
0034DECE  movaps   xmm6, xmmword ptr [rsp + 0x20]
0034DED3  add      rsp, 0x30
0034DED7  pop      rbx
0034DED8  jmp      0x25b470  ; -> 0025B470 fn
```

## 00357570 (163 B, extent 00357570-00357613)

Documented callee on this page: `00262F50`

```
00357570  mov      qword ptr [rsp + 8], rbx
00357575  mov      qword ptr [rsp + 0x10], rbp
0035757A  mov      qword ptr [rsp + 0x18], rsi
0035757F  mov      qword ptr [rsp + 0x20], rdi
00357584  push     r14
00357586  sub      rsp, 0x20
0035758A  mov      rbp, rcx
0035758D  mov      rsi, r9
00357590  mov      rcx, r9
00357593  mov      r14, rdx
00357596  call     0x267e10  ; -> 00267E10 fn
0035759B  mov      rcx, rsi
0035759E  mov      edi, eax
003575A0  call     0x267e10  ; -> 00267E10 fn
003575A5  mov      rcx, rsi
003575A8  mov      ebx, eax
003575AA  call     0x267e10  ; -> 00267E10 fn
003575AF  mov      r8d, edi
003575B2  mov      edx, ebx
003575B4  mov      ecx, eax
003575B6  call     0x359ca0  ; -> 00359CA0 fn
003575BB  mov      rbx, rax
003575BE  test     rax, rax
003575C1  je       0x3575ee  ; -> 003575EE
003575C3  mov      rdx, rax
003575C6  mov      rcx, r14
003575C9  call     0x262f50  ; -> 00262F50 fn
003575CE  mov      rcx, rbp
003575D1  test     eax, eax
003575D3  je       0x3575f1  ; -> 003575F1
003575D5  mov      edx, 1
003575DA  call     0x26b4e0  ; -> 0026B4E0 fn
003575DF  mov      edx, 1
003575E4  mov      rcx, rbx
003575E7  call     0x35ae10  ; -> 0035AE10 fn
003575EC  jmp      0x3575f8  ; -> 003575F8
003575EE  mov      rcx, rbp
003575F1  xor      edx, edx
003575F3  call     0x26b4e0  ; -> 0026B4E0 fn
003575F8  mov      rbx, qword ptr [rsp + 0x30]
003575FD  mov      rbp, qword ptr [rsp + 0x38]
00357602  mov      rsi, qword ptr [rsp + 0x40]
00357607  mov      rdi, qword ptr [rsp + 0x48]
0035760C  add      rsp, 0x20
00357610  pop      r14
00357612  ret      
```

## 003B7210 (221 B, extent 003B7210-003B72ED)

Documented callee on this page: `00262F50`

```
003B7210  mov      qword ptr [rsp + 0x18], rbx
003B7215  mov      qword ptr [rsp + 0x20], rdi
003B721A  push     r14
003B721C  sub      rsp, 0x20
003B7220  mov      rbx, qword ptr [rcx]
003B7223  mov      r14, rcx
003B7226  mov      ecx, dword ptr [rbx + 0x68]
003B7229  call     0x20e600  ; -> 0020E600 fn
003B722E  mov      rdi, rax
003B7231  call     0x2e6420  ; -> 002E6420 fn
003B7236  test     rdi, rdi
003B7239  je       0x3b72dc  ; -> 003B72DC
003B723F  movsxd   rax, edi
003B7242  cmp      dword ptr [rax + rbx], 0
003B7246  jle      0x3b72dc  ; -> 003B72DC
003B724C  mov      ecx, dword ptr [rax + rbx + 4]
003B7250  mov      qword ptr [rsp + 0x38], rsi
003B7255  call     0x20e600  ; -> 0020E600 fn
003B725A  movsxd   rsi, eax
003B725D  xor      edi, edi
003B725F  add      rsi, rbx
003B7262  cmp      di, word ptr [rsi]
003B7265  jae      0x3b72d7  ; -> 003B72D7
003B7267  mov      qword ptr [rsp + 0x30], rbp
003B726C  mov      ebx, edi
003B726E  lea      rbp, [rip + 0x2b0584b]  ; -> 02EBCAC0
003B7275  movzx    ecx, word ptr [rsi + rbx*2 + 2]
003B727A  test     cx, cx
003B727D  js       0x3b72c6  ; -> 003B72C6
003B727F  test     rbx, rbx
003B7282  je       0x3b72a1  ; -> 003B72A1
003B7284  lea      eax, [rdi - 1]
003B7287  cmp      eax, dword ptr [rip + 0x2b05933]  ; -> 02EBCBC0
003B728D  jge      0x3b72c6  ; -> 003B72C6
003B728F  movsx    edx, cx
003B7292  mov      rcx, r14
003B7295  call     0x358940  ; -> 00358940 fn
003B729A  mov      rdx, qword ptr [rbp + rbx*8 - 8]
003B729F  jmp      0x3b72be  ; -> 003B72BE
003B72A1  cmp      qword ptr [rip + 0x2b059bf], 0  ; -> 02EBCC68
003B72A9  je       0x3b72c6  ; -> 003B72C6
003B72AB  movsx    edx, word ptr [rsi + 2]
003B72AF  mov      rcx, r14
003B72B2  call     0x358940  ; -> 00358940 fn
003B72B7  mov      rdx, qword ptr [rip + 0x2b059aa]  ; -> 02EBCC68
003B72BE  mov      rcx, rax
003B72C1  call     0x262f50  ; -> 00262F50 fn
003B72C6  movzx    eax, word ptr [rsi]
003B72C9  inc      edi
003B72CB  inc      rbx
003B72CE  cmp      edi, eax
003B72D0  jl       0x3b7275  ; -> 003B7275
003B72D2  mov      rbp, qword ptr [rsp + 0x30]
003B72D7  mov      rsi, qword ptr [rsp + 0x38]
003B72DC  mov      rbx, qword ptr [rsp + 0x40]
003B72E1  mov      rdi, qword ptr [rsp + 0x48]
003B72E6  add      rsp, 0x20
003B72EA  pop      r14
003B72EC  ret      
```
