# F homing pack (FABLE): `17-Presentation-Rendering/Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md`

Generated 2026-10-03 04:02 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 13. No bearing page cites them and no documented function calls them directly.

## 0024E070 (114 B, extent 0024E070-0024E0E2)

Documented callee on this page: `00375470`

```
0024E070  sub      rsp, 0x28
0024E074  mov      rcx, qword ptr [rip + 0x1e4465d]  ; -> 020926D8
0024E07B  mov      eax, 0xfff9
0024E080  and      word ptr [rip + 0x1e4465d], ax  ; -> 020926E4
0024E087  test     rcx, rcx
0024E08A  je       0x24e0c4  ; -> 0024E0C4
0024E08C  movzx    eax, word ptr [rip + 0x1e440d7]  ; -> 0209216A
0024E093  mov      edx, 0x100
0024E098  cmp      ax, dx
0024E09B  jb       0x24e0a4  ; -> 0024E0A4
0024E09D  call     0x182ca0  ; -> 00182CA0 fn
0024E0A2  jmp      0x24e0b9  ; -> 0024E0B9
0024E0A4  movzx    eax, ax
0024E0A7  lea      rdx, [rip + 0x1e438a2]  ; -> 02091950
0024E0AE  mov      qword ptr [rdx + rax*8], rcx
0024E0B2  inc      word ptr [rip + 0x1e440b1]  ; -> 0209216A
0024E0B9  mov      qword ptr [rip + 0x1e44614], 0  ; -> 020926D8
0024E0C4  mov      ecx, dword ptr [rip + 0x1e44616]  ; -> 020926E0
0024E0CA  test     ecx, ecx
0024E0CC  je       0x24e0dd  ; -> 0024E0DD
0024E0CE  call     0x375470  ; -> 00375470 fn
0024E0D3  mov      dword ptr [rip + 0x1e44603], 0  ; -> 020926E0
0024E0DD  add      rsp, 0x28
0024E0E1  ret      
```

## 00345600 (45 B, extent 00345600-0034562D)

Documented callee on this page: `00360E50`

```
00345600  sub      rsp, 0x28
00345604  mov      rcx, r9
00345607  call     0x267e10  ; -> 00267E10 fn
0034560C  test     eax, eax
0034560E  jns      0x345622  ; -> 00345622
00345610  call     0x2dec00  ; -> 002DEC00 fn
00345615  test     eax, eax
00345617  jns      0x345622  ; -> 00345622
00345619  add      rsp, 0x28
0034561D  jmp      0x360d70  ; -> 00360D70 fn
00345622  mov      ecx, eax
00345624  add      rsp, 0x28
00345628  jmp      0x360e50  ; -> 00360E50 fn
```

## 00346A60 (64 B, extent 00346A60-00346AA0)

Documented callee on this page: `00264180`

```
00346A60  mov      qword ptr [rsp + 8], rbx
00346A65  mov      qword ptr [rsp + 0x10], rsi
00346A6A  push     rdi
00346A6B  sub      rsp, 0x20
00346A6F  mov      rdi, r8
00346A72  xor      ebx, ebx
00346A74  call     0x264180  ; -> 00264180 fn
00346A79  test     eax, eax
00346A7B  mov      esi, 1
00346A80  cmovne   ebx, esi
00346A83  call     0x264830  ; -> 00264830 fn
00346A88  test     eax, eax
00346A8A  mov      eax, ebx
00346A8C  je       0x346a90  ; -> 00346A90
00346A8E  mov      dword ptr [rdi], esi
00346A90  mov      rbx, qword ptr [rsp + 0x30]
00346A95  mov      rsi, qword ptr [rsp + 0x38]
00346A9A  add      rsp, 0x20
00346A9E  pop      rdi
00346A9F  ret      
```

## 0034AF80 (81 B, extent 0034AF80-0034AFD1)

Documented callee on this page: `00263750`

```
0034AF80  mov      qword ptr [rsp + 8], rbx
0034AF85  mov      qword ptr [rsp + 0x10], rsi
0034AF8A  push     rdi
0034AF8B  sub      rsp, 0x20
0034AF8F  mov      rsi, rcx
0034AF92  mov      rdi, r9
0034AF95  mov      rcx, r9
0034AF98  call     0x267e10  ; -> 00267E10 fn
0034AF9D  mov      rcx, rdi
0034AFA0  mov      ebx, eax
0034AFA2  call     0x267e10  ; -> 00267E10 fn
0034AFA7  mov      ecx, eax
0034AFA9  call     0x263750  ; -> 00263750 fn
0034AFAE  mov      edx, ebx
0034AFB0  mov      rcx, rax
0034AFB3  call     0x35a0c0  ; -> 0035A0C0 fn
0034AFB8  mov      edx, eax
0034AFBA  mov      rcx, rsi
0034AFBD  mov      rbx, qword ptr [rsp + 0x30]
0034AFC2  mov      rsi, qword ptr [rsp + 0x38]
0034AFC7  add      rsp, 0x20
0034AFCB  pop      rdi
0034AFCC  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 0034D3A0 (42 B, extent 0034D3A0-0034D3CA)

Documented callee on this page: `00183070`

```
0034D3A0  push     rbx
0034D3A2  sub      rsp, 0x20
0034D3A6  mov      rcx, r9
0034D3A9  mov      rbx, rdx
0034D3AC  call     0x267e10  ; -> 00267E10 fn
0034D3B1  movzx    r8d, word ptr [rbx]
0034D3B5  mov      ecx, eax
0034D3B7  movzx    edx, byte ptr [rbx + 0x15]
0034D3BB  call     0x360980  ; -> 00360980 fn
0034D3C0  add      rsp, 0x20
0034D3C4  pop      rbx
0034D3C5  jmp      0x183070  ; -> 00183070 fn
```

## 003527D0 (20 B, extent 003527D0-003527E4)

Documented callee on this page: `003C58B0`

```
003527D0  sub      rsp, 0x28
003527D4  xor      ecx, ecx
003527D6  call     0x3c5de0  ; -> 003C5DE0 fn
003527DB  add      rsp, 0x28
003527DF  jmp      0x3c58b0  ; -> 003C58B0 fn
```

## 0036E640 (54 B, extent 0036E640-0036E676)

Documented callee on this page: `0024DE70`

```
0036E640  mov      qword ptr [rsp + 8], rbx
0036E645  push     rdi
0036E646  sub      rsp, 0x20
0036E64A  mov      edi, ecx
0036E64C  xor      ebx, ebx
0036E64E  call     0x24de70  ; -> 0024DE70 fn
0036E653  add      eax, -2
0036E656  cmp      eax, 1
0036E659  ja       0x36e669  ; -> 0036E669
0036E65B  mov      edx, ebx
0036E65D  mov      ecx, edi
0036E65F  call     0x24e210  ; -> 0024E210 fn
0036E664  test     eax, eax
0036E666  sete     bl
0036E669  mov      eax, ebx
0036E66B  mov      rbx, qword ptr [rsp + 0x30]
0036E670  add      rsp, 0x20
0036E674  pop      rdi
0036E675  ret      
```

## 0036E6B0 (55 B, extent 0036E6B0-0036E6E7)

Documented callee on this page: `0024DE70`

```
0036E6B0  mov      qword ptr [rsp + 8], rbx
0036E6B5  push     rdi
0036E6B6  sub      rsp, 0x20
0036E6BA  mov      edi, ecx
0036E6BC  xor      ebx, ebx
0036E6BE  call     0x24de70  ; -> 0024DE70 fn
0036E6C3  add      eax, -2
0036E6C6  cmp      eax, 1
0036E6C9  ja       0x36e6da  ; -> 0036E6DA
0036E6CB  lea      edx, [rbx + 3]
0036E6CE  mov      ecx, edi
0036E6D0  call     0x24e210  ; -> 0024E210 fn
0036E6D5  test     eax, eax
0036E6D7  sete     bl
0036E6DA  mov      eax, ebx
0036E6DC  mov      rbx, qword ptr [rsp + 0x30]
0036E6E1  add      rsp, 0x20
0036E6E5  pop      rdi
0036E6E6  ret      
```

## 0036E8B0 (225 B, extent 0036E8B0-0036E991)

Documented callee on this page: `0024DE70`

```
0036E8B0  mov      qword ptr [rsp + 0x18], rbp
0036E8B5  mov      qword ptr [rsp + 0x20], rsi
0036E8BA  push     r14
0036E8BC  sub      rsp, 0x30
0036E8C0  xor      esi, esi
0036E8C2  mov      ebp, edx
0036E8C4  test     ecx, ecx
0036E8C6  jns      0x36e8cc  ; -> 0036E8CC
0036E8C8  mov      ecx, esi
0036E8CA  jmp      0x36e8d6  ; -> 0036E8D6
0036E8CC  mov      eax, 0x1f
0036E8D1  cmp      ecx, eax
0036E8D3  cmovg    ecx, eax
0036E8D6  movsxd   rax, ecx
0036E8D9  lea      rcx, [rax + rax*2]
0036E8DD  lea      rax, [rip + 0x1f6abcc]  ; -> 022D94B0
0036E8E4  lea      r14, [rax + rcx*8]
0036E8E8  movsx    eax, word ptr [rax + rcx*8 + 4]
0036E8ED  add      eax, -2
0036E8F0  cmp      eax, 1
0036E8F3  ja       0x36e97e  ; -> 0036E97E
0036E8F9  mov      ecx, dword ptr [r14]
0036E8FC  call     0x24de70  ; -> 0024DE70 fn
0036E901  add      eax, -2
0036E904  cmp      eax, 1
0036E907  ja       0x36e97e  ; -> 0036E97E
0036E909  mov      eax, 3
0036E90E  mov      qword ptr [rsp + 0x40], rbx
0036E913  mov      word ptr [r14 + 4], ax
0036E918  mov      qword ptr [rsp + 0x48], rdi
0036E91D  call     0x3b7760  ; -> 003B7760 fn
0036E922  mov      edi, eax
0036E924  call     0x3b7750  ; -> 003B7750 fn
0036E929  mov      rbx, rax
0036E92C  call     0x3b7720  ; -> 003B7720 fn
0036E931  mov      r9d, dword ptr [r14]
0036E934  mov      ecx, eax
0036E936  mov      r8d, edi
0036E939  mov      dword ptr [rsp + 0x20], ebp
0036E93D  mov      rdx, rbx
0036E940  call     0x3b1ba0  ; -> 003B1BA0 fn
0036E945  mov      ecx, dword ptr [r14]
0036E948  movsx    eax, byte ptr [r14 + 8]
0036E94D  mov      rdi, qword ptr [rsp + 0x48]
0036E952  mov      rbx, qword ptr [rsp + 0x40]
0036E957  test     ecx, ecx
0036E959  je       0x36e968  ; -> 0036E968
0036E95B  cmp      eax, 3
0036E95E  cmove    esi, eax
0036E961  mov      edx, esi
0036E963  call     0x24f8d0  ; -> 0024F8D0 fn
0036E968  mov      eax, 1
0036E96D  mov      rbp, qword ptr [rsp + 0x50]
0036E972  mov      rsi, qword ptr [rsp + 0x58]
0036E977  add      rsp, 0x30
0036E97B  pop      r14
0036E97D  ret      
0036E97E  mov      rbp, qword ptr [rsp + 0x50]
0036E983  xor      eax, eax
0036E985  mov      rsi, qword ptr [rsp + 0x58]
0036E98A  add      rsp, 0x30
0036E98E  pop      r14
0036E990  ret      
```

## 0037C3C0 (46 B, extent 0037C3C0-0037C3EE)

Documented callee on this page: `00263750`

```
0037C3C0  push     rbx
0037C3C2  sub      rsp, 0x20
0037C3C6  xor      ebx, ebx
0037C3C8  mov      ecx, ebx
0037C3CA  call     0x263750  ; -> 00263750 fn
0037C3CF  test     rax, rax
0037C3D2  je       0x37c3e1  ; -> 0037C3E1
0037C3D4  mov      edx, 1
0037C3D9  mov      rcx, rax
0037C3DC  call     0x2e6bb0  ; -> 002E6BB0 fn
0037C3E1  inc      ebx
0037C3E3  cmp      ebx, 4
0037C3E6  jl       0x37c3c8  ; -> 0037C3C8
0037C3E8  add      rsp, 0x20
0037C3EC  pop      rbx
0037C3ED  ret      
```

## 003CAB00 (693 B, extent 003CAB00-003CADB5)

Documented callee on this page: `00303CC0`

```
003CAB00  mov      qword ptr [rsp + 0x18], rbx
003CAB05  push     rbp
003CAB06  push     rsi
003CAB07  push     rdi
003CAB08  push     r14
003CAB0A  push     r15
003CAB0C  sub      rsp, 0xd0
003CAB13  mov      rax, qword ptr [rip + 0x1b79d16]  ; -> 01F44830 [u64 0x00002B992DDFA232]
003CAB1A  xor      rax, rsp
003CAB1D  mov      qword ptr [rsp + 0xc0], rax
003CAB25  mov      eax, dword ptr [rdx]
003CAB27  mov      rbp, rcx
003CAB2A  dec      eax
003CAB2C  cmp      eax, 0x1e
003CAB2F  ja       0x3cad86  ; -> 003CAD86
003CAB35  lea      r8, [rip - 0x2aab3c]  ; -> 00120000 (image base)
003CAB3C  cdqe     
003CAB3E  movzx    eax, byte ptr [r8 + rax + 0x2aadd4]
003CAB47  mov      ecx, dword ptr [r8 + rax*4 + 0x2aadb8]  ; image base + 0x2aadb8 = 003CADB8
003CAB4F  add      rcx, r8
003CAB52  jmp      rcx
003CAB54  mov      rdx, qword ptr [rdx + 8]
003CAB58  lea      rcx, [rbp + 0x50]
003CAB5C  mov      r9, rbp
003CAB5F  mov      r8d, 1
003CAB65  call     0x2432b0  ; -> 002432B0 fn
003CAB6A  movzx    ecx, word ptr [rax + 0xa]
003CAB6E  movzx    edx, word ptr [rax + 8]
003CAB72  movsx    r8d, word ptr [rax + 6]
003CAB77  test     rbp, rbp
003CAB7A  je       0x3cab9d  ; -> 003CAB9D
003CAB7C  movzx    eax, word ptr [rax + 4]
003CAB80  mov      word ptr [rbp + 0x98], ax
003CAB87  mov      word ptr [rbp + 0x9a], r8w
003CAB8F  mov      word ptr [rbp + 0x9c], dx
003CAB96  mov      word ptr [rbp + 0x9e], cx
003CAB9D  mov      ecx, 4
003CABA2  call     0x2735e0  ; -> 002735E0 fn
003CABA7  mov      rdx, rax
003CABAA  mov      rcx, rbp
003CABAD  call     0x247570  ; -> 00247570 fn
003CABB2  xor      esi, esi
003CABB4  test     rbp, rbp
003CABB7  jne      0x3cabc2  ; -> 003CABC2
003CABB9  mov      qword ptr [rsp + 0x30], rsi
003CABBE  mov      eax, esi
003CABC0  jmp      0x3cabd2  ; -> 003CABD2
003CABC2  mov      rcx, qword ptr [rbp + 0x60]
003CABC6  mov      rax, qword ptr [rcx]
003CABC9  mov      qword ptr [rsp + 0x30], rax
003CABCE  mov      rax, qword ptr [rcx + 8]
003CABD2  mov      edx, 0xc
003CABD7  mov      qword ptr [rsp + 0x38], rax
003CABDC  lea      rcx, [rsp + 0x50]
003CABE1  call     0x29da70  ; -> 0029DA70 fn
003CABE6  lea      r15, [rsp + 0x30]
003CABEB  lea      r14, [rsp + 0x58]
003CABF0  movzx    eax, byte ptr [rsp + 0x52]
003CABF5  cmp      esi, eax
003CABF7  jge      0x3cad82  ; -> 003CAD82
003CABFD  movsxd   rax, esi
003CAC00  lea      rdi, [rbp + 0xc0]
003CAC07  shl      rax, 7
003CAC0B  mov      ecx, 0x467c
003CAC10  add      rdi, rax
003CAC13  call     0x2f9860  ; -> 002F9860 fn
003CAC18  mov      r9, qword ptr [r14]
003CAC1B  mov      r8, rax
003CAC1E  mov      rax, qword ptr [r14 + 8]
003CAC22  mov      rdx, rdi
003CAC25  mov      ecx, 0x80
003CAC2A  mov      qword ptr [rsp + 0x20], rax
003CAC2F  call     0x2b4090  ; -> 002B4090 fn
003CAC34  mov      rbx, qword ptr [r15]
003CAC37  xor      ecx, ecx
003CAC39  mov      qword ptr [rbx + 0x18], rdi
003CAC3D  call     0x20e620  ; -> 0020E620 fn
003CAC42  inc      esi
003CAC44  mov      dword ptr [rbx + 0x20], eax
003CAC47  add      r14, 0x18
003CAC4B  add      r15, 8
003CAC4F  cmp      esi, 2
003CAC52  jl       0x3cabf0  ; -> 003CABF0
003CAC54  xor      eax, eax
003CAC56  jmp      0x3cad8e  ; -> 003CAD8E
003CAC5B  mov      rcx, rbp
003CAC5E  call     0x2470d0  ; -> 002470D0 fn
003CAC63  xor      eax, eax
003CAC65  jmp      0x3cad8e  ; -> 003CAD8E
003CAC6A  lea      rdx, [rsp + 0x50]
003CAC6F  xor      ecx, ecx
003CAC71  call     0x3200a0  ; -> 003200A0 fn
003CAC76  mov      ecx, 0x10e
003CAC7B  call     0x29dbe0  ; -> 0029DBE0 fn
003CAC80  movzx    ecx, word ptr [rip + 0x2bcc6e3]  ; -> 02F9736A
003CAC87  test     ecx, eax
003CAC89  je       0x3cacb0  ; -> 003CACB0
003CAC8B  xorps    xmm0, xmm0
003CAC8E  mov      dword ptr [rsp + 0x30], 0x1e
003CAC96  lea      rdx, [rsp + 0x30]
003CAC9B  mov      rcx, rbp
003CAC9E  movdqu   xmmword ptr [rsp + 0x38], xmm0
003CACA4  call     0x275440  ; -> 00275440 fn
003CACA9  xor      eax, eax
003CACAB  jmp      0x3cad8e  ; -> 003CAD8E
003CACB0  mov      ecx, 0x10d
003CACB5  call     0x29dbe0  ; -> 0029DBE0 fn
003CACBA  movzx    ecx, word ptr [rip + 0x2bcc6a9]  ; -> 02F9736A
003CACC1  test     ecx, eax
003CACC3  je       0x3cad82  ; -> 003CAD82
003CACC9  test     byte ptr [rsp + 0x54], 2
003CACCE  jne      0x3cacf2  ; -> 003CACF2
003CACD0  cmp      dword ptr [rsp + 0x64], 0
003CACD5  je       0x3cacf2  ; -> 003CACF2
003CACD7  mov      ecx, 1
003CACDC  call     0x303f00  ; -> 00303F00 fn
003CACE1  mov      ecx, 0x55
003CACE6  call     0x249c60  ; -> 00249C60 fn
003CACEB  xor      eax, eax
003CACED  jmp      0x3cad8e  ; -> 003CAD8E
003CACF2  mov      ecx, 5
003CACF7  call     0x249c60  ; -> 00249C60 fn
003CACFC  xor      eax, eax
003CACFE  jmp      0x3cad8e  ; -> 003CAD8E
003CAD03  lea      rdx, [rsp + 0x50]
003CAD08  xor      ecx, ecx
003CAD0A  call     0x3200a0  ; -> 003200A0 fn
003CAD0F  test     rbp, rbp
003CAD12  jne      0x3cad18  ; -> 003CAD18
003CAD14  xor      esi, esi
003CAD16  jmp      0x3cad1f  ; -> 003CAD1F
003CAD18  mov      rax, qword ptr [rbp + 0x60]
003CAD1C  mov      rsi, qword ptr [rax]
003CAD1F  test     byte ptr [rsp + 0x54], 2
003CAD24  jne      0x3cad35  ; -> 003CAD35
003CAD26  cmp      dword ptr [rsp + 0x64], 0
003CAD2B  je       0x3cad35  ; -> 003CAD35
003CAD2D  or       dword ptr [rsi + 8], 1
003CAD31  xor      eax, eax
003CAD33  jmp      0x3cad8e  ; -> 003CAD8E
003CAD35  and      dword ptr [rsi + 8], 0xfffffffe
003CAD39  xor      eax, eax
003CAD3B  jmp      0x3cad8e  ; -> 003CAD8E
003CAD3D  lea      rdx, [rsp + 0x50]
003CAD42  xor      ecx, ecx
003CAD44  call     0x3200a0  ; -> 003200A0 fn
003CAD49  xorps    xmm0, xmm0
003CAD4C  comiss   xmm0, dword ptr [rsp + 0x5c]
003CAD51  jb       0x3cad82  ; -> 003CAD82
003CAD53  call     0x303cc0  ; -> 00303CC0 fn
003CAD58  test     eax, eax
003CAD5A  je       0x3cad82  ; -> 003CAD82
003CAD5C  mov      rax, qword ptr [rip + 0x277c9f5]  ; -> 02B47758
003CAD63  test     rax, rax
003CAD66  je       0x3cad82  ; -> 003CAD82
003CAD68  and      dword ptr [rax + 0xa90], 0xfffffffe
003CAD6F  or       dword ptr [rax + 0xa90], 2
003CAD76  xor      eax, eax
003CAD78  jmp      0x3cad8e  ; -> 003CAD8E
003CAD7A  mov      rcx, rbp
003CAD7D  call     0x2470c0  ; -> 002470C0 fn
003CAD82  xor      eax, eax
003CAD84  jmp      0x3cad8e  ; -> 003CAD8E
003CAD86  mov      rcx, rbp
003CAD89  call     0x5c5230  ; -> 005C5230 fn
003CAD8E  mov      rcx, qword ptr [rsp + 0xc0]
003CAD96  xor      rcx, rsp
003CAD99  call     0x808c40  ; -> 00808C40 fn
003CAD9E  mov      rbx, qword ptr [rsp + 0x110]
003CADA6  add      rsp, 0xd0
003CADAD  pop      r15
003CADAF  pop      r14
003CADB1  pop      rdi
003CADB2  pop      rsi
003CADB3  pop      rbp
003CADB4  ret      
```

## 003DDC50 (189 B, extent 003DDC50-003DDD0D)

Documented callee on this page: `0024CFF0`

```
003DDC50  mov      qword ptr [rsp + 8], rbx
003DDC55  mov      qword ptr [rsp + 0x10], rbp
003DDC5A  mov      qword ptr [rsp + 0x18], rsi
003DDC5F  push     rdi
003DDC60  sub      rsp, 0x20
003DDC64  xor      esi, esi
003DDC66  mov      ebx, ecx
003DDC68  mov      ebp, 3
003DDC6D  test     ecx, ecx
003DDC6F  jns      0x3ddc75  ; -> 003DDC75
003DDC71  mov      eax, esi
003DDC73  jmp      0x3ddc7c  ; -> 003DDC7C
003DDC75  cmp      ebx, ebp
003DDC77  mov      eax, ebx
003DDC79  cmovg    eax, ebp
003DDC7C  cdqe     
003DDC7E  imul     rdi, rax, 0x68
003DDC82  lea      rax, [rip + 0x277adf7]  ; -> 02B58A80
003DDC89  add      rdi, rax
003DDC8C  mov      ecx, dword ptr [rdi]
003DDC8E  test     ecx, ecx
003DDC90  je       0x3ddc99  ; -> 003DDC99
003DDC92  call     0x24cff0  ; -> 0024CFF0 fn
003DDC97  mov      dword ptr [rdi], esi
003DDC99  test     ebx, ebx
003DDC9B  jns      0x3ddca1  ; -> 003DDCA1
003DDC9D  mov      ebx, esi
003DDC9F  jmp      0x3ddca6  ; -> 003DDCA6
003DDCA1  cmp      ebx, ebp
003DDCA3  cmovg    ebx, ebp
003DDCA6  movsxd   rax, ebx
003DDCA9  xor      edx, edx
003DDCAB  imul     rbx, rax, 0x68
003DDCAF  lea      rax, [rip + 0x277adda]  ; -> 02B58A90
003DDCB6  add      rbx, rax
003DDCB9  lea      r8d, [rdx + 0x58]
003DDCBD  mov      rcx, rbx
003DDCC0  call     0x861ec0  ; -> 00861EC0 fn
003DDCC5  movzx    eax, byte ptr [rbx + 0x1c]
003DDCC9  mov      dword ptr [rbx], 0x13602
003DDCCF  and      al, 0xe3
003DDCD1  or       al, bpl
003DDCD4  mov      rbp, qword ptr [rsp + 0x38]
003DDCD9  mov      byte ptr [rbx + 0x1c], al
003DDCDC  mov      qword ptr [rbx + 0x20], rsi
003DDCE0  mov      rsi, qword ptr [rsp + 0x40]
003DDCE5  mov      dword ptr [rbx + 0x28], 0x3f800000
003DDCEC  mov      qword ptr [rbx + 0x2c], 0x3f800000
003DDCF4  mov      dword ptr [rbx + 0x34], 0x3f000000
003DDCFB  mov      dword ptr [rbx + 0x38], 0x80ffffff
003DDD02  mov      rbx, qword ptr [rsp + 0x30]
003DDD07  add      rsp, 0x20
003DDD0B  pop      rdi
003DDD0C  ret      
```

## 00473E60 (25 B, extent 00473E60-00473E79)

Documented callee on this page: `00183070`

```
00473E60  push     rbx
00473E62  sub      rsp, 0x20
00473E66  mov      ebx, ecx
00473E68  call     0x183070  ; -> 00183070 fn
00473E6D  mov      ecx, ebx
00473E6F  add      rsp, 0x20
00473E73  pop      rbx
00473E74  jmp      0x182f10  ; -> 00182F10 fn
```
