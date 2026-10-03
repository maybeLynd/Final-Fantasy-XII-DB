# F homing pack (FABLE): `17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md`

Generated 2026-10-03 04:02 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 8. No bearing page cites them and no documented function calls them directly.

## 003340C0 (87 B, extent 003340C0-00334117)

Documented callee on this page: `0046F370`

```
003340C0  sub      rsp, 0x28
003340C4  cmp      edx, 0x1d
003340C7  jge      0x334112  ; -> 00334112
003340C9  movsxd   rax, edx
003340CC  mov      qword ptr [rsp + 0x20], rbx
003340D1  lea      rbx, [rcx + rax*4]
003340D5  mov      ecx, dword ptr [rcx + rax*4 + 0x2c]
003340D9  call     0x20e600  ; -> 0020E600 fn
003340DE  test     rax, rax
003340E1  je       0x33410d  ; -> 0033410D
003340E3  mov      ecx, dword ptr [rbx + 0x2c]
003340E6  call     0x20e600  ; -> 0020E600 fn
003340EB  mov      rcx, rax
003340EE  call     0x46f370  ; -> 0046F370 fn
003340F3  mov      ecx, dword ptr [rbx + 0x2c]
003340F6  call     0x20e600  ; -> 0020E600 fn
003340FB  mov      rcx, rax
003340FE  call     0x3697f0  ; -> 003697F0 fn
00334103  xor      ecx, ecx
00334105  call     0x20e620  ; -> 0020E620 fn
0033410A  mov      dword ptr [rbx + 0x2c], eax
0033410D  mov      rbx, qword ptr [rsp + 0x20]
00334112  add      rsp, 0x28
00334116  ret      
```

## 00343E20 (40 B, extent 00343E20-00343E48)

Documented callee on this page: `003590D0`

```
00343E20  sub      rsp, 0x28
00343E24  call     0x3590d0  ; -> 003590D0 fn
00343E29  mov      ecx, eax
00343E2B  call     0x3588b0  ; -> 003588B0 fn
00343E30  test     rax, rax
00343E33  je       0x343e43  ; -> 00343E43
00343E35  xor      edx, edx
00343E37  mov      rcx, rax
00343E3A  add      rsp, 0x28
00343E3E  jmp      0x26ae90  ; -> 0026AE90 fn
00343E43  add      rsp, 0x28
00343E47  ret      
```

## 0034C630 (111 B, extent 0034C630-0034C69F)

Documented callee on this page: `00358940`

```
0034C630  mov      qword ptr [rsp + 8], rbx
0034C635  mov      qword ptr [rsp + 0x10], rbp
0034C63A  mov      qword ptr [rsp + 0x18], rsi
0034C63F  push     rdi
0034C640  sub      rsp, 0x20
0034C644  mov      rbx, r9
0034C647  mov      rdi, r8
0034C64A  call     0x2640c0  ; -> 002640C0 fn
0034C64F  mov      rcx, rbx
0034C652  mov      rsi, rax
0034C655  call     0x267e10  ; -> 00267E10 fn
0034C65A  mov      rcx, rbx
0034C65D  mov      ebp, eax
0034C65F  call     0x267e10  ; -> 00267E10 fn
0034C664  mov      edx, eax
0034C666  mov      rcx, rsi
0034C669  call     0x358940  ; -> 00358940 fn
0034C66E  mov      rbx, rax
0034C671  test     rax, rax
0034C674  je       0x34c687  ; -> 0034C687
0034C676  mov      r8d, ebp
0034C679  mov      rdx, rax
0034C67C  mov      rcx, rsi
0034C67F  call     0x265380  ; -> 00265380 fn
0034C684  mov      dword ptr [rdi + 8], eax
0034C687  mov      rbp, qword ptr [rsp + 0x38]
0034C68C  mov      rsi, qword ptr [rsp + 0x40]
0034C691  mov      qword ptr [rdi], rbx
0034C694  mov      rbx, qword ptr [rsp + 0x30]
0034C699  add      rsp, 0x20
0034C69D  pop      rdi
0034C69E  ret      
```

## 0035A1C0 (57 B, extent 0035A1C0-0035A1F9)

Documented callee on this page: `003589B0`

```
0035A1C0  push     rbx
0035A1C2  sub      rsp, 0x20
0035A1C6  mov      ebx, edx
0035A1C8  call     0x3589b0  ; -> 003589B0 fn
0035A1CD  lea      rdx, [rsp + 0x40]
0035A1D2  mov      ecx, eax
0035A1D4  call     0x320ca0  ; -> 00320CA0 fn
0035A1D9  test     eax, eax
0035A1DB  je       0x35a1f1  ; -> 0035A1F1
0035A1DD  mov      eax, dword ptr [rsp + 0x40]
0035A1E1  bt       eax, ebx
0035A1E4  jae      0x35a1f1  ; -> 0035A1F1
0035A1E6  mov      eax, 1
0035A1EB  add      rsp, 0x20
0035A1EF  pop      rbx
0035A1F0  ret      
0035A1F1  xor      eax, eax
0035A1F3  add      rsp, 0x20
0035A1F7  pop      rbx
0035A1F8  ret      
```

## 003A87B0 (332 B, extent 003A87B0-003A88FC)

Documented callee on this page: `003A92D0`

```
003A87B0  mov      qword ptr [rsp + 0x10], rbx
003A87B5  push     rsi
003A87B6  sub      rsp, 0x20
003A87BA  mov      rdx, qword ptr [rip + 0x2b167c7]  ; -> 02EBEF88
003A87C1  movzx    esi, cl
003A87C4  mov      rbx, qword ptr [rdx + 8]
003A87C8  test     rbx, rbx
003A87CB  je       0x3a88f1  ; -> 003A88F1
003A87D1  mov      qword ptr [rsp + 0x30], rdi
003A87D6  nop      word ptr [rax + rax]
003A87E0  mov      rdi, qword ptr [rbx + 8]
003A87E4  cmp      byte ptr [rbx + 0x13a], sil
003A87EB  jne      0x3a88e0  ; -> 003A88E0
003A87F1  mov      rax, qword ptr [rbx]
003A87F4  test     rax, rax
003A87F7  je       0x3a87ff  ; -> 003A87FF
003A87F9  mov      qword ptr [rax + 8], rdi
003A87FD  jmp      0x3a8803  ; -> 003A8803
003A87FF  mov      qword ptr [rdx + 8], rdi
003A8803  mov      rcx, qword ptr [rbx + 8]
003A8807  mov      rax, qword ptr [rbx]
003A880A  test     rcx, rcx
003A880D  je       0x3a8814  ; -> 003A8814
003A880F  mov      qword ptr [rcx], rax
003A8812  jmp      0x3a8818  ; -> 003A8818
003A8814  mov      qword ptr [rdx + 0x10], rax
003A8818  cmp      qword ptr [rbx + 0x110], 0
003A8820  je       0x3a8836  ; -> 003A8836
003A8822  mov      rcx, rbx
003A8825  call     0x3a92d0  ; -> 003A92D0 fn
003A882A  mov      rcx, qword ptr [rbx + 0x110]
003A8831  call     0x3697f0  ; -> 003697F0 fn
003A8836  mov      rax, qword ptr [rip + 0x2b1674b]  ; -> 02EBEF88
003A883D  movsx    edx, byte ptr [rbx + 0x13b]
003A8844  add      rax, 0x18
003A8848  mov      r9d, dword ptr [rbx + 0x1c]
003A884C  xor      r8d, r8d
003A884F  nop      
003A8850  mov      ecx, dword ptr [rax]
003A8852  cmp      ecx, -1
003A8855  je       0x3a88d1  ; -> 003A88D1
003A8857  cmp      ecx, r9d
003A885A  jne      0x3a8864  ; -> 003A8864
003A885C  movzx    ecx, byte ptr [rax + 4]
003A8860  cmp      ecx, edx
003A8862  je       0x3a8873  ; -> 003A8873
003A8864  inc      r8d
003A8867  add      rax, 8
003A886B  cmp      r8d, 0x20
003A886F  jl       0x3a8850  ; -> 003A8850
003A8871  jmp      0x3a88d1  ; -> 003A88D1
003A8873  sub      word ptr [rax + 6], 1
003A8878  jne      0x3a88d1  ; -> 003A88D1
003A887A  test     byte ptr [rax + 5], 1
003A887E  je       0x3a88d1  ; -> 003A88D1
003A8880  lea      r9, [rax + 8]
003A8884  cmp      r8d, 0x1f
003A8888  jge      0x3a88bc  ; -> 003A88BC
003A888A  nop      word ptr [rax + rax]
003A8890  mov      edx, dword ptr [r9]
003A8893  mov      dword ptr [rax], edx
003A8895  movzx    ecx, byte ptr [r9 + 4]
003A889A  mov      byte ptr [rax + 4], cl
003A889D  movzx    ecx, word ptr [r9 + 6]
003A88A2  mov      word ptr [rax + 6], cx
003A88A6  cmp      edx, -1
003A88A9  je       0x3a88bc  ; -> 003A88BC
003A88AB  inc      r8d
003A88AE  add      rax, 8
003A88B2  add      r9, 8
003A88B6  cmp      r8d, 0x1f
003A88BA  jl       0x3a8890  ; -> 003A8890
003A88BC  mov      dword ptr [rax], 0xffffffff
003A88C2  movsx    edx, byte ptr [rbx + 0x13b]
003A88C9  mov      ecx, dword ptr [rbx + 0x1c]
003A88CC  call     0x3a8130  ; -> 003A8130 fn
003A88D1  mov      rcx, rbx
003A88D4  call     0x3697f0  ; -> 003697F0 fn
003A88D9  mov      rdx, qword ptr [rip + 0x2b166a8]  ; -> 02EBEF88
003A88E0  mov      rbx, rdi
003A88E3  test     rdi, rdi
003A88E6  jne      0x3a87e0  ; -> 003A87E0
003A88EC  mov      rdi, qword ptr [rsp + 0x30]
003A88F1  mov      rbx, qword ptr [rsp + 0x38]
003A88F6  add      rsp, 0x20
003A88FA  pop      rsi
003A88FB  ret      
```

## 0042DA00 (48 B, extent 0042DA00-0042DA30)

Documented callee on this page: `00421E20`

```
0042DA00  push     rbx
0042DA02  sub      rsp, 0x20
0042DA06  mov      r9, qword ptr [rdx + 0x10]
0042DA0A  mov      rbx, rdx
0042DA0D  mov      r8d, dword ptr [rdx + 0xc]
0042DA11  movzx    edx, word ptr [rdx + 8]
0042DA15  call     0x421e20  ; -> 00421E20 fn
0042DA1A  test     rax, rax
0042DA1D  je       0x42da2a  ; -> 0042DA2A
0042DA1F  mov      qword ptr [rbx + 0x10], rax
0042DA23  mov      dword ptr [rbx + 0x18], 1
0042DA2A  add      rsp, 0x20
0042DA2E  pop      rbx
0042DA2F  ret      
```

## 0046E950 (61 B, extent 0046E950-0046E98D)

Documented callee on this page: `002ED570`

```
0046E950  push     rbx
0046E952  sub      rsp, 0x20
0046E956  mov      rax, rdx
0046E959  mov      rbx, rcx
0046E95C  mov      edx, dword ptr [rcx + 8]
0046E95F  cmp      edx, -1
0046E962  je       0x46e984  ; -> 0046E984
0046E964  mov      rcx, rax
0046E967  call     0x2ed570  ; -> 002ED570 fn
0046E96C  test     rax, rax
0046E96F  jne      0x46e97b  ; -> 0046E97B
0046E971  or       eax, 0xffffffff
0046E974  mov      dword ptr [rbx + 8], eax
0046E977  mov      word ptr [rbx + 0x14], ax
0046E97B  and      dword ptr [rbx], 0xfffffffd
0046E97E  add      rsp, 0x20
0046E982  pop      rbx
0046E983  ret      
0046E984  and      dword ptr [rcx], 0xfffffffd
0046E987  add      rsp, 0x20
0046E98B  pop      rbx
0046E98C  ret      
```

## 00473B30 (20 B, extent 00473B30-00473B44)

Documented callee on this page: `003589B0`

```
00473B30  sub      rsp, 0x28
00473B34  call     0x3589b0  ; -> 003589B0 fn
00473B39  mov      ecx, eax
00473B3B  add      rsp, 0x28
00473B3F  jmp      0x290840  ; -> 00290840 fn
```
