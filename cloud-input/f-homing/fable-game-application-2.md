# F homing pack (FABLE): `00-Engine-Core-Runtime/Application-Root/game-application.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 20. No bearing page cites them and no documented function calls them directly.

## 00169580 (78 B, extent 00169580-001695CE)

Documented callee on this page: `00184E60`

```
00169580  sub      rsp, 0x28
00169584  lea      rcx, [rip + 0x2d3c1dd]  ; -> 02EA5768
0016958B  call     0x184e60  ; -> 00184E60 fn
00169590  lea      rax, [rip + 0x799941]  ; -> 00902ED8
00169597  mov      dword ptr [rip + 0x2d3c287], 0x3f800000  ; -> 02EA5828
001695A1  lea      rcx, [rip + 0x2d3c1b8]  ; -> 02EA5760
001695A8  mov      qword ptr [rip + 0x2d3c1b1], rax  ; -> 02EA5760
001695AF  mov      dword ptr [rip + 0x2d3c277], 0x3f800000  ; -> 02EA5830
001695B9  call     0x1f0a00  ; -> 001F0A00 fn
001695BE  lea      rcx, [rip + 0x74e6cb]  ; -> 008B7C90
001695C5  add      rsp, 0x28
001695C9  jmp      0x808b90  ; -> 00808B90 fn
```

## 00169600 (32 B, extent 00169600-00169620)

Documented callee on this page: `00808B90`

```
00169600  xorps    xmm1, xmm1
00169603  lea      rcx, [rip + 0x74e736]  ; -> 008B7D40
0016960A  movaps   xmm0, xmm1
0016960D  unpcklps xmm0, xmm1
00169610  unpcklpd xmm0, xmm0
00169614  movaps   xmmword ptr [rip + 0x2d3bef5], xmm0  ; -> 02EA5510
0016961B  jmp      0x808b90  ; -> 00808B90 fn
```

## 00169640 (20 B, extent 00169640-00169654)

Documented callee on this page: `00808B90`

```
00169640  xor      eax, eax
00169642  lea      rcx, [rip + 0x74efe7]  ; -> 008B8630
00169649  xchg     dword ptr [rip + 0x2d43939], eax  ; -> 02EACF88
0016964F  jmp      0x808b90  ; -> 00808B90 fn
```

## 00169830 (56 B, extent 00169830-00169868)

Documented callee on this page: `00808B90`

```
00169830  xor      eax, eax
00169832  lea      rcx, [rip + 0x74ef77]  ; -> 008B87B0
00169839  mov      qword ptr [rip + 0x2d43ac8], rax  ; -> 02EAD308
00169840  xorps    xmm0, xmm0
00169843  lea      rax, [rip + 0x1b4b19e]  ; -> 01CB49E8
0016984A  mov      dword ptr [rip + 0x2d43ab4], 0  ; -> 02EAD308
00169854  mov      qword ptr [rip + 0x2d43aa5], rax  ; -> 02EAD300
0016985B  movdqu   xmmword ptr [rip + 0x2d43aad], xmm0  ; -> 02EAD310
00169863  jmp      0x808b90  ; -> 00808B90 fn
```

## 00169E90 (135 B, extent 00169E90-00169F17)

Documented callee on this page: `00808B90`

```
00169E90  sub      rsp, 0x28
00169E94  xor      eax, eax
00169E96  lea      rcx, [rip + 0x2d439b3]  ; -> 02EAD850
00169E9D  mov      qword ptr [rip + 0x2d439ac], rax  ; -> 02EAD850
00169EA4  mov      qword ptr [rip + 0x2d439ad], rax  ; -> 02EAD858
00169EAB  mov      qword ptr [rip + 0x2d439ae], rax  ; -> 02EAD860
00169EB2  mov      qword ptr [rip + 0x2d439af], rax  ; -> 02EAD868
00169EB9  mov      qword ptr [rip + 0x2d439b0], rax  ; -> 02EAD870
00169EC0  mov      qword ptr [rip + 0x2d439b1], rax  ; -> 02EAD878
00169EC7  mov      qword ptr [rip + 0x2d439b2], rax  ; -> 02EAD880
00169ECE  mov      qword ptr [rip + 0x2d439b3], rax  ; -> 02EAD888
00169ED5  call     qword ptr [rip + 0x7581d5]  ; -> 008C20B0 [u64 0x0000000001CCC0A6]
00169EDB  xor      eax, eax
00169EDD  xor      r9d, r9d
00169EE0  mov      dword ptr [rip + 0x2d4399a], eax  ; -> 02EAD880
00169EE6  xor      r8d, r8d
00169EE9  mov      dword ptr [rip + 0x2d43995], eax  ; -> 02EAD884
00169EEF  xor      ecx, ecx
00169EF1  mov      dword ptr [rip + 0x2d43991], eax  ; -> 02EAD888
00169EF7  lea      edx, [rax + 1]
00169EFA  call     qword ptr [rip + 0x7583e8]  ; -> 008C22E8 [u64 0x0000000001CCC5FA]
00169F00  lea      rcx, [rip + 0x74ee39]  ; -> 008B8D40
00169F07  mov      qword ptr [rip + 0x2d4396a], rax  ; -> 02EAD878
00169F0E  add      rsp, 0x28
00169F12  jmp      0x808b90  ; -> 00808B90 fn
```

## 0016D6C0 (8 B, extent 0016D6C0-0016D6C8)

Documented callee on this page: `00210EB0`

```
0016D6C0  mov      rcx, rdx
0016D6C3  jmp      0x210eb0  ; -> 00210EB0 fn
```

## 0017F610 (60 B, extent 0017F610-0017F64C)

Documented callee on this page: `001AD440`

```
0017F610  push     rbx
0017F612  sub      rsp, 0x20
0017F616  mov      ebx, ecx
0017F618  call     0x1ad440  ; -> 001AD440 fn
0017F61D  test     rax, rax
0017F620  je       0x17f631  ; -> 0017F631
0017F622  call     0x1ad440  ; -> 001AD440 fn
0017F627  mov      rcx, rax
0017F62A  mov      edx, ebx
0017F62C  call     0x1ad850  ; -> 001AD850 fn
0017F631  call     0x1d50d0  ; -> 001D50D0 fn
0017F636  test     rax, rax
0017F639  je       0x17f646  ; -> 0017F646
0017F63B  call     0x1d50d0  ; -> 001D50D0 fn
0017F640  mov      dword ptr [rax + 0xd08], ebx
0017F646  add      rsp, 0x20
0017F64A  pop      rbx
0017F64B  ret      
```

## 00195620 (67 B, extent 00195620-00195663)

Documented callee on this page: `00809950`

```
00195620  mov      qword ptr [rsp + 8], rbx
00195625  push     rdi
00195626  sub      rsp, 0x20
0019562A  lea      rax, [rip + 0x75dfb7]  ; -> 008F35E8
00195631  mov      rdi, rcx
00195634  mov      qword ptr [rcx], rax
00195637  mov      ebx, edx
00195639  add      rcx, 8
0019563D  call     qword ptr [rip + 0x72d3e5]  ; -> 008C2A28 [u64 0x0000000001CCEB8E]
00195643  test     bl, 1
00195646  je       0x195655  ; -> 00195655
00195648  mov      edx, 0x18
0019564D  mov      rcx, rdi
00195650  call     0x809950  ; -> 00809950 fn
00195655  mov      rax, rdi
00195658  mov      rbx, qword ptr [rsp + 0x30]
0019565D  add      rsp, 0x20
00195661  pop      rdi
00195662  ret      
```

## 00199A80 (96 B, extent 00199A80-00199AE0)

Documented callee on this page: `005CD6D0`

```
00199A80  push     rbx
00199A82  sub      rsp, 0x30
00199A86  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
00199A8F  mov      rbx, rcx
00199A92  cmp      byte ptr [rcx + 0xb8], 0
00199A99  je       0x199aa8  ; -> 00199AA8
00199A9B  add      rcx, 0x90
00199AA2  call     0x5cd6d0  ; -> 005CD6D0 fn
00199AA7  nop      
00199AA8  lea      rcx, [rbx + 0x58]
00199AAC  call     0x199b60  ; -> 00199B60 fn
00199AB1  nop      
00199AB2  lea      rcx, [rbx + 0x20]
00199AB6  call     0x199b60  ; -> 00199B60 fn
00199ABB  nop      
00199ABC  mov      rdx, qword ptr [rbx]
00199ABF  test     rdx, rdx
00199AC2  je       0x199ada  ; -> 00199ADA
00199AC4  lea      rcx, [rbx + 0x18]
00199AC8  mov      rax, qword ptr [rcx]
00199ACB  mov      r8, qword ptr [rbx + 0x10]
00199ACF  sub      r8, rdx
00199AD2  and      r8, 0xfffffffffffffff0
00199AD6  call     qword ptr [rax + 0x18]
00199AD9  nop      
00199ADA  add      rsp, 0x30
00199ADE  pop      rbx
00199ADF  ret      
```

## 0019A1A0 (249 B, extent 0019A1A0-0019A299)

Documented callee on this page: `002124C0`

```
0019A1A0  push     rsi
0019A1A2  push     rdi
0019A1A3  push     r14
0019A1A5  sub      rsp, 0x30
0019A1A9  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0019A1B2  mov      qword ptr [rsp + 0x58], rbx
0019A1B7  mov      qword ptr [rsp + 0x60], rbp
0019A1BC  mov      rbp, rcx
0019A1BF  cmp      byte ptr [rcx + 0x154], 0
0019A1C6  je       0x19a284  ; -> 0019A284
0019A1CC  lea      rdi, [rcx + 0x50]
0019A1D0  mov      ecx, 5
0019A1D5  call     0x5ccb80  ; -> 005CCB80 fn
0019A1DA  xor      esi, esi
0019A1DC  lea      rcx, [rbp + 0x28]
0019A1E0  call     0x5cd4f0  ; -> 005CD4F0 fn
0019A1E5  mov      rax, qword ptr [rdi]
0019A1E8  xor      ecx, ecx
0019A1EA  cmp      rax, rdi
0019A1ED  je       0x19a230  ; -> 0019A230
0019A1EF  nop      
0019A1F0  mov      rax, qword ptr [rax]
0019A1F3  inc      rcx
0019A1F6  cmp      rax, rdi
0019A1F9  jne      0x19a1f0  ; -> 0019A1F0
0019A1FB  test     ecx, ecx
0019A1FD  je       0x19a230  ; -> 0019A230
0019A1FF  mov      rax, qword ptr [rbp + 0x58]
0019A203  mov      rsi, qword ptr [rax + 0x10]
0019A207  mov      rdx, qword ptr [rdi + 8]
0019A20B  mov      rcx, qword ptr [rdx + 8]
0019A20F  mov      rax, qword ptr [rdx]
0019A212  mov      qword ptr [rcx], rax
0019A215  mov      rcx, qword ptr [rdx]
0019A218  mov      rax, qword ptr [rdx + 8]
0019A21C  mov      qword ptr [rcx + 8], rax
0019A220  lea      rcx, [rdi + 0x10]
0019A224  mov      rax, qword ptr [rcx]
0019A227  mov      r8d, 0x18
0019A22D  call     qword ptr [rax + 0x18]
0019A230  lea      rcx, [rbp + 0x28]
0019A234  call     0x5cd820  ; -> 005CD820 fn
0019A239  test     rsi, rsi
0019A23C  je       0x19a277  ; -> 0019A277
0019A23E  mov      rax, qword ptr [rsi]
0019A241  test     rax, rax
0019A244  je       0x19a24c  ; -> 0019A24C
0019A246  mov      rcx, qword ptr [rsi + 8]
0019A24A  call     rax
0019A24C  lea      rbx, [rbp + 0x68]
0019A250  mov      qword ptr [rsp + 0x50], rbx
0019A255  mov      rcx, rbx
0019A258  call     0x5cd4f0  ; -> 005CD4F0 fn
0019A25D  nop      
0019A25E  lea      rcx, [rbp + 0x90]
0019A265  mov      rdx, rsi
0019A268  call     0x2124c0  ; -> 002124C0 fn
0019A26D  nop      
0019A26E  mov      rcx, rbx
0019A271  call     0x5cd820  ; -> 005CD820 fn
0019A276  nop      
0019A277  cmp      byte ptr [rbp + 0x154], 0
0019A27E  jne      0x19a1d0  ; -> 0019A1D0
0019A284  xor      eax, eax
0019A286  mov      rbx, qword ptr [rsp + 0x58]
0019A28B  mov      rbp, qword ptr [rsp + 0x60]
0019A290  add      rsp, 0x30
0019A294  pop      r14
0019A296  pop      rdi
0019A297  pop      rsi
0019A298  ret      
```

## 0019A3E0 (105 B, extent 0019A3E0-0019A449)

Documented callee on this page: `00809054`

```
0019A3E0  push     rdi
0019A3E2  sub      rsp, 0x30
0019A3E6  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0019A3EF  mov      qword ptr [rsp + 0x40], rbx
0019A3F4  mov      rdi, rcx
0019A3F7  mov      rcx, qword ptr [rcx + 0x10]
0019A3FB  test     rcx, rcx
0019A3FE  je       0x19a435  ; -> 0019A435
0019A400  lea      rbx, [rcx - 8]
0019A404  lea      r9, [rip + 0xf5]  ; -> 0019A500
0019A40B  mov      r8, qword ptr [rbx]
0019A40E  mov      edx, 0x98
0019A413  call     0x809054  ; -> 00809054 fn
0019A418  nop      
0019A419  imul     rdx, qword ptr [rbx], 0x98
0019A420  add      rdx, 8
0019A424  mov      rcx, rbx
0019A427  call     0x809950  ; -> 00809950 fn
0019A42C  nop      
0019A42D  mov      qword ptr [rdi + 0x10], 0
0019A435  mov      rcx, qword ptr [rdi]
0019A438  mov      rbx, qword ptr [rsp + 0x40]
0019A43D  add      rsp, 0x30
0019A441  pop      rdi
0019A442  jmp      qword ptr [rip + 0x727f97]  ; -> 008C23E0 [u64 0x0000000001CCC076]
```

## 0019A450 (156 B, extent 0019A450-0019A4EC)

Documented callee on this page: `00210EB0`

```
0019A450  mov      qword ptr [rsp + 8], rbx
0019A455  push     rdi
0019A456  sub      rsp, 0x20
0019A45A  mov      rbx, qword ptr [rcx + 8]
0019A45E  mov      rdi, rcx
0019A461  test     rbx, rbx
0019A464  je       0x19a489  ; -> 0019A489
0019A466  mov      rcx, qword ptr [rbx + 8]
0019A46A  test     rcx, rcx
0019A46D  je       0x19a47c  ; -> 0019A47C
0019A46F  call     0x210eb0  ; -> 00210EB0 fn
0019A474  mov      qword ptr [rbx + 8], 0
0019A47C  mov      edx, 0x18
0019A481  mov      rcx, rbx
0019A484  call     0x809950  ; -> 00809950 fn
0019A489  mov      rbx, qword ptr [rdi + 0x10]
0019A48D  test     rbx, rbx
0019A490  je       0x19a4b5  ; -> 0019A4B5
0019A492  mov      rcx, qword ptr [rbx + 8]
0019A496  test     rcx, rcx
0019A499  je       0x19a4a8  ; -> 0019A4A8
0019A49B  call     0x210eb0  ; -> 00210EB0 fn
0019A4A0  mov      qword ptr [rbx + 8], 0
0019A4A8  mov      edx, 0x18
0019A4AD  mov      rcx, rbx
0019A4B0  call     0x809950  ; -> 00809950 fn
0019A4B5  mov      rbx, qword ptr [rdi + 0x18]
0019A4B9  test     rbx, rbx
0019A4BC  je       0x19a4e1  ; -> 0019A4E1
0019A4BE  mov      rcx, qword ptr [rbx + 8]
0019A4C2  test     rcx, rcx
0019A4C5  je       0x19a4d4  ; -> 0019A4D4
0019A4C7  call     0x210eb0  ; -> 00210EB0 fn
0019A4CC  mov      qword ptr [rbx + 8], 0
0019A4D4  mov      edx, 0x18
0019A4D9  mov      rcx, rbx
0019A4DC  call     0x809950  ; -> 00809950 fn
0019A4E1  mov      rbx, qword ptr [rsp + 0x30]
0019A4E6  add      rsp, 0x20
0019A4EA  pop      rdi
0019A4EB  ret      
```

## 0019B130 (87 B, extent 0019B130-0019B187)

Documented callee on this page: `00809950`

```
0019B130  mov      qword ptr [rsp + 8], rbx
0019B135  push     rdi
0019B136  sub      rsp, 0x20
0019B13A  mov      rax, qword ptr [rcx + 8]
0019B13E  xor      edi, edi
0019B140  mov      byte ptr [rcx], 0
0019B143  mov      rbx, rcx
0019B146  mov      byte ptr [rax], 0
0019B149  mov      rax, qword ptr [rcx + 0x10]
0019B14D  mov      byte ptr [rax], 0
0019B150  mov      rax, qword ptr [rcx + 0x18]
0019B154  mov      byte ptr [rax], 0
0019B157  mov      qword ptr [rcx + 0x20], rdi
0019B15B  mov      qword ptr [rcx + 0x28], rdi
0019B15F  cmp      dword ptr [rcx + 0x30], edi
0019B162  je       0x19b170  ; -> 0019B170
0019B164  mov      rcx, qword ptr [rcx + 0x38]
0019B168  lea      edx, [rdi + 8]
0019B16B  call     0x809950  ; -> 00809950 fn
0019B170  mov      dword ptr [rbx + 0x30], edi
0019B173  mov      dword ptr [rbx + 0x88], edi
0019B179  mov      dword ptr [rbx + 0x40], edi
0019B17C  mov      rbx, qword ptr [rsp + 0x30]
0019B181  add      rsp, 0x20
0019B185  pop      rdi
0019B186  ret      
```

## 0019C7C0 (163 B, extent 0019C7C0-0019C863)

Documented callee on this page: `00220760`

```
0019C7C0  mov      qword ptr [rsp + 8], rcx
0019C7C5  push     rbx
0019C7C6  push     rsi
0019C7C7  push     rdi
0019C7C8  sub      rsp, 0x30
0019C7CC  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0019C7D5  mov      rsi, rcx
0019C7D8  call     0x5cc8a0  ; -> 005CC8A0 fn
0019C7DD  lea      rdx, [rip + 0x75793c]  ; -> 008F4120 [str "EASTL map"]
0019C7E4  lea      rcx, [rsp + 0x58]
0019C7E9  call     0x1edf00  ; -> 001EDF00 fn
0019C7EE  lea      rdi, [rsi + 0x28]
0019C7F2  mov      qword ptr [rsp + 0x60], rdi
0019C7F7  lea      rbx, [rdi + 8]
0019C7FB  xor      ecx, ecx
0019C7FD  mov      qword ptr [rbx], rcx
0019C800  mov      qword ptr [rbx + 8], rcx
0019C804  mov      qword ptr [rbx + 0x10], rcx
0019C808  mov      qword ptr [rbx + 0x18], rcx
0019C80C  mov      dword ptr [rdi + 0x28], ecx
0019C80F  lea      rcx, [rdi + 0x30]
0019C813  mov      rdx, rax
0019C816  call     0x1edf00  ; -> 001EDF00 fn
0019C81B  mov      qword ptr [rbx], rbx
0019C81E  mov      qword ptr [rdi + 0x10], rbx
0019C822  mov      qword ptr [rdi + 0x18], 0
0019C82A  mov      byte ptr [rdi + 0x20], 0
0019C82E  mov      dword ptr [rdi + 0x28], 0
0019C835  lea      rcx, [rsi + 0x60]
0019C839  mov      r8b, 1
0019C83C  mov      edx, 0x1800
0019C841  call     0x19c630  ; -> 0019C630 fn
0019C846  nop      
0019C847  mov      rcx, rsi
0019C84A  call     0x5cd0a0  ; -> 005CD0A0 fn
0019C84F  mov      rcx, rdi
0019C852  call     0x220760  ; -> 00220760 fn
0019C857  nop      
0019C858  mov      rax, rsi
0019C85B  add      rsp, 0x30
0019C85F  pop      rdi
0019C860  pop      rsi
0019C861  pop      rbx
0019C862  ret      
```

## 0019C870 (131 B, extent 0019C870-0019C8F3)

Documented callee on this page: `005CD6D0`

```
0019C870  push     rbx
0019C872  sub      rsp, 0x30
0019C876  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0019C87F  mov      rbx, rcx
0019C882  cmp      byte ptr [rcx + 0xb8], 0
0019C889  je       0x19c898  ; -> 0019C898
0019C88B  add      rcx, 0x90
0019C892  call     0x5cd6d0  ; -> 005CD6D0 fn
0019C897  nop      
0019C898  lea      rcx, [rbx + 0x58]
0019C89C  call     0x19c990  ; -> 0019C990 fn
0019C8A1  nop      
0019C8A2  lea      rcx, [rbx + 0x20]
0019C8A6  call     0x19c990  ; -> 0019C990 fn
0019C8AB  nop      
0019C8AC  mov      r10, qword ptr [rbx]
0019C8AF  test     r10, r10
0019C8B2  je       0x19c8ed  ; -> 0019C8ED
0019C8B4  lea      rcx, [rbx + 0x18]
0019C8B8  mov      r9, qword ptr [rcx]
0019C8BB  mov      r8, qword ptr [rbx + 0x10]
0019C8BF  sub      r8, r10
0019C8C2  movabs   rax, 0x2aaaaaaaaaaaaaab
0019C8CC  imul     r8
0019C8CF  sar      rdx, 2
0019C8D3  mov      rax, rdx
0019C8D6  shr      rax, 0x3f
0019C8DA  add      rdx, rax
0019C8DD  lea      r8, [rdx + rdx*2]
0019C8E1  shl      r8, 3
0019C8E5  mov      rdx, r10
0019C8E8  call     qword ptr [r9 + 0x18]
0019C8EC  nop      
0019C8ED  add      rsp, 0x30
0019C8F1  pop      rbx
0019C8F2  ret      
```

## 0019D1D0 (379 B, extent 0019D1D0-0019D34B)

Documented callee on this page: `001EDF00`

```
0019D1D0  mov      rax, rsp
0019D1D3  mov      qword ptr [rax + 0x18], r8
0019D1D7  mov      qword ptr [rax + 0x10], rdx
0019D1DB  push     rbp
0019D1DC  push     rsi
0019D1DD  push     rdi
0019D1DE  push     r14
0019D1E0  push     r15
0019D1E2  sub      rsp, 0x40
0019D1E6  mov      qword ptr [rax - 0x48], 0xfffffffffffffffe
0019D1EE  mov      qword ptr [rax + 0x20], rbx
0019D1F2  mov      rbx, rdx
0019D1F5  mov      r14, rcx
0019D1F8  mov      qword ptr [rcx], r9
0019D1FB  cmp      rdx, r8
0019D1FE  je       0x19d334  ; -> 0019D334
0019D204  xor      ebp, ebp
0019D206  nop      word ptr [rax + rax]
0019D210  mov      rsi, qword ptr [r14]
0019D213  mov      qword ptr [rsp + 0x70], rsi
0019D218  mov      qword ptr [rsp + 0x28], rsi
0019D21D  test     rsi, rsi
0019D220  je       0x19d318  ; -> 0019D318
0019D226  mov      rcx, rsi
0019D229  mov      rax, rbx
0019D22C  mov      edx, 2
0019D231  movups   xmm0, xmmword ptr [rax]
0019D234  movups   xmmword ptr [rcx], xmm0
0019D237  movups   xmm1, xmmword ptr [rax + 0x10]
0019D23B  movups   xmmword ptr [rcx + 0x10], xmm1
0019D23F  movups   xmm0, xmmword ptr [rax + 0x20]
0019D243  movups   xmmword ptr [rcx + 0x20], xmm0
0019D247  movups   xmm1, xmmword ptr [rax + 0x30]
0019D24B  movups   xmmword ptr [rcx + 0x30], xmm1
0019D24F  movups   xmm0, xmmword ptr [rax + 0x40]
0019D253  movups   xmmword ptr [rcx + 0x40], xmm0
0019D257  movups   xmm1, xmmword ptr [rax + 0x50]
0019D25B  movups   xmmword ptr [rcx + 0x50], xmm1
0019D25F  movups   xmm0, xmmword ptr [rax + 0x60]
0019D263  movups   xmmword ptr [rcx + 0x60], xmm0
0019D267  lea      rcx, [rcx + 0x80]
0019D26E  movups   xmm1, xmmword ptr [rax + 0x70]
0019D272  movups   xmmword ptr [rcx - 0x10], xmm1
0019D276  lea      rax, [rax + 0x80]
0019D27D  sub      rdx, 1
0019D281  jne      0x19d231  ; -> 0019D231
0019D283  lea      r15, [rbx + 0x100]
0019D28A  lea      rdi, [rsi + 0x100]
0019D291  mov      qword ptr [rsp + 0x30], rdi
0019D296  mov      qword ptr [rdi], rbp
0019D299  mov      qword ptr [rdi + 8], rbp
0019D29D  mov      qword ptr [rdi + 0x10], rbp
0019D2A1  lea      rcx, [rdi + 0x18]
0019D2A5  lea      rdx, [rip + 0x728cac]  ; -> 008C5F58 [str "EASTL vector"]
0019D2AC  call     0x1edf00  ; -> 001EDF00 fn
0019D2B1  nop      
0019D2B2  cmp      r15, rdi
0019D2B5  je       0x19d2f0  ; -> 0019D2F0
0019D2B7  mov      rcx, qword ptr [rdi]
0019D2BA  mov      rax, qword ptr [r15]
0019D2BD  mov      qword ptr [rdi], rax
0019D2C0  mov      qword ptr [r15], rcx
0019D2C3  mov      rcx, qword ptr [rdi + 8]
0019D2C7  mov      rax, qword ptr [r15 + 8]
0019D2CB  mov      qword ptr [rdi + 8], rax
0019D2CF  mov      qword ptr [r15 + 8], rcx
0019D2D3  mov      rcx, qword ptr [rdi + 0x10]
0019D2D7  mov      rax, qword ptr [r15 + 0x10]
0019D2DB  mov      qword ptr [rdi + 0x10], rax
0019D2DF  mov      qword ptr [r15 + 0x10], rcx
0019D2E3  nop      dword ptr [rax]
0019D2E7  nop      word ptr [rax + rax]
0019D2F0  mov      rax, qword ptr [rbx + 0x120]
0019D2F7  mov      qword ptr [rsi + 0x120], rax
0019D2FE  movzx    eax, byte ptr [rbx + 0x128]
0019D305  mov      byte ptr [rsi + 0x128], al
0019D30B  mov      r8, qword ptr [rsp + 0x80]
0019D313  mov      rbx, qword ptr [rsp + 0x78]
0019D318  add      rbx, 0x130
0019D31F  mov      qword ptr [rsp + 0x78], rbx
0019D324  add      qword ptr [r14], 0x130
0019D32B  cmp      rbx, r8
0019D32E  jne      0x19d210  ; -> 0019D210
0019D334  mov      rax, r14
0019D337  mov      rbx, qword ptr [rsp + 0x88]
0019D33F  add      rsp, 0x40
0019D343  pop      r15
0019D345  pop      r14
0019D347  pop      rdi
0019D348  pop      rsi
0019D349  pop      rbp
0019D34A  ret      
```

## 0019D5B0 (390 B, extent 0019D5B0-0019D736)

Documented callee on this page: `005CD0A0`

```
0019D5B0  mov      qword ptr [rsp + 8], rcx
0019D5B5  push     rbp
0019D5B6  push     rsi
0019D5B7  push     rdi
0019D5B8  push     r12
0019D5BA  push     r13
0019D5BC  push     r14
0019D5BE  push     r15
0019D5C0  sub      rsp, 0x40
0019D5C4  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0019D5CD  mov      qword ptr [rsp + 0x88], rbx
0019D5D5  movzx    ebp, r8b
0019D5D9  mov      r12d, edx
0019D5DC  mov      r14, rcx
0019D5DF  xor      edi, edi
0019D5E1  mov      qword ptr [rcx], rdi
0019D5E4  mov      qword ptr [rcx + 8], rdi
0019D5E8  mov      qword ptr [rcx + 0x10], rdi
0019D5EC  add      rcx, 0x18
0019D5F0  lea      rdx, [rip + 0x728961]  ; -> 008C5F58 [str "EASTL vector"]
0019D5F7  call     0x1edf00  ; -> 001EDF00 fn
0019D5FC  nop      
0019D5FD  lea      rdx, [rip + 0x7566ac]  ; -> 008F3CB0 [str "EASTL set"]
0019D604  lea      rcx, [rsp + 0x98]
0019D60C  call     0x1edf00  ; -> 001EDF00 fn
0019D611  lea      r15, [r14 + 0x20]
0019D615  mov      qword ptr [rsp + 0x28], r15
0019D61A  lea      rbx, [r15 + 8]
0019D61E  xor      ecx, ecx
0019D620  mov      qword ptr [rbx], rcx
0019D623  mov      qword ptr [rbx + 8], rcx
0019D627  mov      qword ptr [rbx + 0x10], rcx
0019D62B  mov      qword ptr [rbx + 0x18], rcx
0019D62F  mov      dword ptr [r15 + 0x28], edi
0019D633  lea      rcx, [r15 + 0x30]
0019D637  mov      rdx, rax
0019D63A  call     0x1edf00  ; -> 001EDF00 fn
0019D63F  mov      qword ptr [rbx], rbx
0019D642  mov      qword ptr [r15 + 0x10], rbx
0019D646  mov      qword ptr [r15 + 0x18], rdi
0019D64A  mov      byte ptr [r15 + 0x20], dil
0019D64E  mov      dword ptr [r15 + 0x28], edi
0019D652  lea      rdx, [rip + 0x756657]  ; -> 008F3CB0 [str "EASTL set"]
0019D659  lea      rcx, [rsp + 0x28]
0019D65E  call     0x1edf00  ; -> 001EDF00 fn
0019D663  lea      rsi, [r14 + 0x58]
0019D667  mov      qword ptr [rsp + 0x30], rsi
0019D66C  lea      rbx, [rsi + 8]
0019D670  xor      ecx, ecx
0019D672  mov      qword ptr [rbx], rcx
0019D675  mov      qword ptr [rbx + 8], rcx
0019D679  mov      qword ptr [rbx + 0x10], rcx
0019D67D  mov      qword ptr [rbx + 0x18], rcx
0019D681  mov      dword ptr [rsi + 0x28], edi
0019D684  lea      rcx, [rsi + 0x30]
0019D688  mov      rdx, rax
0019D68B  call     0x1edf00  ; -> 001EDF00 fn
0019D690  mov      qword ptr [rbx], rbx
0019D693  mov      qword ptr [rsi + 0x10], rbx
0019D697  mov      qword ptr [rsi + 0x18], rdi
0019D69B  mov      byte ptr [rsi + 0x20], dil
0019D69F  mov      dword ptr [rsi + 0x28], edi
0019D6A2  lea      rcx, [r14 + 0x90]
0019D6A9  call     0x5cc8a0  ; -> 005CC8A0 fn
0019D6AE  mov      byte ptr [r14 + 0xb8], bpl
0019D6B5  mov      edx, r12d
0019D6B8  mov      rcx, r14
0019D6BB  call     0x19ec40  ; -> 0019EC40 fn
0019D6C0  test     r12d, r12d
0019D6C3  je       0x19d704  ; -> 0019D704
0019D6C5  mov      esi, r12d
0019D6C8  movzx    ebx, byte ptr [rsp + 0x90]
0019D6D0  mov      rcx, qword ptr [r14]
0019D6D3  add      rcx, rdi
0019D6D6  mov      qword ptr [rsp + 0x98], rcx
0019D6DE  movzx    r9d, bl
0019D6E2  lea      r8, [rsp + 0x98]
0019D6EA  lea      rdx, [rsp + 0x30]
0019D6EF  mov      rcx, r15
0019D6F2  call     0x199db0  ; -> 00199DB0 fn
0019D6F7  add      rdi, 0x130
0019D6FE  sub      rsi, 1
0019D702  jne      0x19d6d0  ; -> 0019D6D0
0019D704  cmp      byte ptr [r14 + 0xb8], 0
0019D70C  je       0x19d71b  ; -> 0019D71B
0019D70E  lea      rcx, [r14 + 0x90]
0019D715  call     0x5cd0a0  ; -> 005CD0A0 fn
0019D71A  nop      
0019D71B  mov      rax, r14
0019D71E  mov      rbx, qword ptr [rsp + 0x88]
0019D726  add      rsp, 0x40
0019D72A  pop      r15
0019D72C  pop      r14
0019D72E  pop      r13
0019D730  pop      r12
0019D732  pop      rdi
0019D733  pop      rsi
0019D734  pop      rbp
0019D735  ret      
```

## 0019D740 (390 B, extent 0019D740-0019D8C6)

Documented callee on this page: `005CD0A0`

```
0019D740  mov      qword ptr [rsp + 8], rcx
0019D745  push     rbp
0019D746  push     rsi
0019D747  push     rdi
0019D748  push     r12
0019D74A  push     r13
0019D74C  push     r14
0019D74E  push     r15
0019D750  sub      rsp, 0x40
0019D754  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0019D75D  mov      qword ptr [rsp + 0x88], rbx
0019D765  movzx    ebp, r8b
0019D769  mov      r12d, edx
0019D76C  mov      r14, rcx
0019D76F  xor      edi, edi
0019D771  mov      qword ptr [rcx], rdi
0019D774  mov      qword ptr [rcx + 8], rdi
0019D778  mov      qword ptr [rcx + 0x10], rdi
0019D77C  add      rcx, 0x18
0019D780  lea      rdx, [rip + 0x7287d1]  ; -> 008C5F58 [str "EASTL vector"]
0019D787  call     0x1edf00  ; -> 001EDF00 fn
0019D78C  nop      
0019D78D  lea      rdx, [rip + 0x75651c]  ; -> 008F3CB0 [str "EASTL set"]
0019D794  lea      rcx, [rsp + 0x98]
0019D79C  call     0x1edf00  ; -> 001EDF00 fn
0019D7A1  lea      r15, [r14 + 0x20]
0019D7A5  mov      qword ptr [rsp + 0x28], r15
0019D7AA  lea      rbx, [r15 + 8]
0019D7AE  xor      ecx, ecx
0019D7B0  mov      qword ptr [rbx], rcx
0019D7B3  mov      qword ptr [rbx + 8], rcx
0019D7B7  mov      qword ptr [rbx + 0x10], rcx
0019D7BB  mov      qword ptr [rbx + 0x18], rcx
0019D7BF  mov      dword ptr [r15 + 0x28], edi
0019D7C3  lea      rcx, [r15 + 0x30]
0019D7C7  mov      rdx, rax
0019D7CA  call     0x1edf00  ; -> 001EDF00 fn
0019D7CF  mov      qword ptr [rbx], rbx
0019D7D2  mov      qword ptr [r15 + 0x10], rbx
0019D7D6  mov      qword ptr [r15 + 0x18], rdi
0019D7DA  mov      byte ptr [r15 + 0x20], dil
0019D7DE  mov      dword ptr [r15 + 0x28], edi
0019D7E2  lea      rdx, [rip + 0x7564c7]  ; -> 008F3CB0 [str "EASTL set"]
0019D7E9  lea      rcx, [rsp + 0x28]
0019D7EE  call     0x1edf00  ; -> 001EDF00 fn
0019D7F3  lea      rsi, [r14 + 0x58]
0019D7F7  mov      qword ptr [rsp + 0x30], rsi
0019D7FC  lea      rbx, [rsi + 8]
0019D800  xor      ecx, ecx
0019D802  mov      qword ptr [rbx], rcx
0019D805  mov      qword ptr [rbx + 8], rcx
0019D809  mov      qword ptr [rbx + 0x10], rcx
0019D80D  mov      qword ptr [rbx + 0x18], rcx
0019D811  mov      dword ptr [rsi + 0x28], edi
0019D814  lea      rcx, [rsi + 0x30]
0019D818  mov      rdx, rax
0019D81B  call     0x1edf00  ; -> 001EDF00 fn
0019D820  mov      qword ptr [rbx], rbx
0019D823  mov      qword ptr [rsi + 0x10], rbx
0019D827  mov      qword ptr [rsi + 0x18], rdi
0019D82B  mov      byte ptr [rsi + 0x20], dil
0019D82F  mov      dword ptr [rsi + 0x28], edi
0019D832  lea      rcx, [r14 + 0x90]
0019D839  call     0x5cc8a0  ; -> 005CC8A0 fn
0019D83E  mov      byte ptr [r14 + 0xb8], bpl
0019D845  mov      edx, r12d
0019D848  mov      rcx, r14
0019D84B  call     0x19ed80  ; -> 0019ED80 fn
0019D850  test     r12d, r12d
0019D853  je       0x19d894  ; -> 0019D894
0019D855  mov      esi, r12d
0019D858  movzx    ebx, byte ptr [rsp + 0x90]
0019D860  mov      rcx, qword ptr [r14]
0019D863  add      rcx, rdi
0019D866  mov      qword ptr [rsp + 0x98], rcx
0019D86E  movzx    r9d, bl
0019D872  lea      r8, [rsp + 0x98]
0019D87A  lea      rdx, [rsp + 0x30]
0019D87F  mov      rcx, r15
0019D882  call     0x199db0  ; -> 00199DB0 fn
0019D887  add      rdi, 0x118
0019D88E  sub      rsi, 1
0019D892  jne      0x19d860  ; -> 0019D860
0019D894  cmp      byte ptr [r14 + 0xb8], 0
0019D89C  je       0x19d8ab  ; -> 0019D8AB
0019D89E  lea      rcx, [r14 + 0x90]
0019D8A5  call     0x5cd0a0  ; -> 005CD0A0 fn
0019D8AA  nop      
0019D8AB  mov      rax, r14
0019D8AE  mov      rbx, qword ptr [rsp + 0x88]
0019D8B6  add      rsp, 0x40
0019D8BA  pop      r15
0019D8BC  pop      r14
0019D8BE  pop      r13
0019D8C0  pop      r12
0019D8C2  pop      rdi
0019D8C3  pop      rsi
0019D8C4  pop      rbp
0019D8C5  ret      
```

## 0019E010 (685 B, extent 0019E010-0019E2BD)

Documented callee on this page: `00808C40`

```
0019E010  push     rbx
0019E012  push     rbp
0019E013  push     rsi
0019E014  push     rdi
0019E015  push     r12
0019E017  push     r14
0019E019  push     r15
0019E01B  sub      rsp, 0x190
0019E022  mov      qword ptr [rsp + 0x40], 0xfffffffffffffffe
0019E02B  mov      rax, qword ptr [rip + 0x1da67fe]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0019E032  xor      rax, rsp
0019E035  mov      qword ptr [rsp + 0x180], rax
0019E03D  mov      rbx, r9
0019E040  mov      r15d, r8d
0019E043  mov      rbp, rdx
0019E046  mov      r14, rcx
0019E049  mov      rcx, qword ptr [rcx + 8]
0019E04D  mov      r9, qword ptr [r14 + 0x10]
0019E051  sub      r9, rcx
0019E054  movabs   r12, 0x6bca1af286bca1b
0019E05E  mov      rax, r12
0019E061  imul     r9
0019E064  sar      rdx, 3
0019E068  mov      rax, rdx
0019E06B  shr      rax, 0x3f
0019E06F  add      rdx, rax
0019E072  cmp      r8d, edx
0019E075  ja       0x19e190  ; -> 0019E190
0019E07B  test     r8d, r8d
0019E07E  je       0x19e29b  ; -> 0019E29B
0019E084  mov      rdx, rbx
0019E087  lea      rcx, [rsp + 0x50]
0019E08C  call     0x19d970  ; -> 0019D970 fn
0019E091  nop      
0019E092  mov      rbx, qword ptr [r14 + 8]
0019E096  mov      rcx, rbx
0019E099  sub      rcx, rbp
0019E09C  mov      rax, r12
0019E09F  imul     rcx
0019E0A2  mov      rsi, rdx
0019E0A5  sar      rsi, 3
0019E0A9  mov      rax, rsi
0019E0AC  shr      rax, 0x3f
0019E0B0  add      rsi, rax
0019E0B3  cmp      r15d, esi
0019E0B6  jae      0x19e0f9  ; -> 0019E0F9
0019E0B8  imul     rsi, r15, 0x130
0019E0BF  mov      rdi, rbx
0019E0C2  sub      rdi, rsi
0019E0C5  movzx    eax, byte ptr [rsp + 0x30]
0019E0CA  mov      byte ptr [rsp + 0x20], al
0019E0CE  mov      r9, rbx
0019E0D1  mov      r8, rbx
0019E0D4  mov      rdx, rdi
0019E0D7  lea      rcx, [rsp + 0x38]
0019E0DC  call     0x19d1d0  ; -> 0019D1D0 fn
0019E0E1  add      qword ptr [r14 + 8], rsi
0019E0E5  mov      r8, rbx
0019E0E8  mov      rdx, rdi
0019E0EB  mov      rcx, rbp
0019E0EE  call     0x19ce30  ; -> 0019CE30 fn
0019E0F3  lea      rdx, [rsi + rbp]
0019E0F7  jmp      0x19e14d  ; -> 0019E14D
0019E0F9  sub      r15d, esi
0019E0FC  mov      edi, r15d
0019E0FF  movzx    r9d, byte ptr [rsp + 0x30]
0019E105  lea      r8, [rsp + 0x50]
0019E10A  mov      edx, r15d
0019E10D  mov      rcx, rbx
0019E110  call     0x19d420  ; -> 0019D420 fn
0019E115  imul     r9, rdi, 0x130
0019E11C  add      r9, qword ptr [r14 + 8]
0019E120  mov      qword ptr [r14 + 8], r9
0019E124  movzx    eax, byte ptr [rsp + 0x30]
0019E129  mov      byte ptr [rsp + 0x20], al
0019E12D  mov      r8, rbx
0019E130  mov      rdx, rbp
0019E133  lea      rcx, [rsp + 0x38]
0019E138  call     0x19d1d0  ; -> 0019D1D0 fn
0019E13D  mov      eax, esi
0019E13F  imul     rcx, rax, 0x130
0019E146  add      qword ptr [r14 + 8], rcx
0019E14A  mov      rdx, rbx
0019E14D  lea      r8, [rsp + 0x50]
0019E152  mov      rcx, rbp
0019E155  call     0x19d100  ; -> 0019D100 fn
0019E15A  nop      
0019E15B  mov      rdx, qword ptr [rsp + 0x150]
0019E163  test     rdx, rdx
0019E166  je       0x19e18b  ; -> 0019E18B
0019E168  mov      r8, qword ptr [rsp + 0x160]
0019E170  sub      r8, rdx
0019E173  and      r8, 0xfffffffffffffff8
0019E177  lea      rcx, [rsp + 0x168]
0019E17F  mov      rax, qword ptr [rsp + 0x168]
0019E187  call     qword ptr [rax + 0x18]
0019E18A  nop      
0019E18B  jmp      0x19e29b  ; -> 0019E29B
0019E190  sub      rcx, qword ptr [r14]
0019E193  mov      rax, r12
0019E196  imul     rcx
0019E199  sar      rdx, 3
0019E19D  mov      rax, rdx
0019E1A0  shr      rax, 0x3f
0019E1A4  add      rdx, rax
0019E1A7  test     edx, edx
0019E1A9  lea      eax, [rdx + rdx]
0019E1AC  jne      0x19e1b3  ; -> 0019E1B3
0019E1AE  mov      eax, 1
0019E1B3  lea      edi, [r15 + rdx]
0019E1B7  cmp      eax, edi
0019E1B9  cmova    edi, eax
0019E1BC  test     edi, edi
0019E1BE  je       0x19e1dc  ; -> 0019E1DC
0019E1C0  lea      rcx, [r14 + 0x18]
0019E1C4  mov      r9, qword ptr [rcx]
0019E1C7  mov      eax, edi
0019E1C9  imul     rdx, rax, 0x130
0019E1D0  xor      r8d, r8d
0019E1D3  call     qword ptr [r9 + 0x10]
0019E1D7  mov      rsi, rax
0019E1DA  jmp      0x19e1de  ; -> 0019E1DE
0019E1DC  xor      esi, esi
0019E1DE  movzx    eax, byte ptr [rsp + 0x30]
0019E1E3  mov      byte ptr [rsp + 0x20], al
0019E1E7  mov      r9, rsi
0019E1EA  mov      r8, rbp
0019E1ED  mov      rdx, qword ptr [r14]
0019E1F0  lea      rcx, [rsp + 0x38]
0019E1F5  call     0x19d1d0  ; -> 0019D1D0 fn
0019E1FA  movzx    r9d, byte ptr [rsp + 0x30]
0019E200  mov      r8, rbx
0019E203  mov      edx, r15d
0019E206  mov      rcx, qword ptr [rsp + 0x38]
0019E20B  call     0x19d420  ; -> 0019D420 fn
0019E210  imul     r9, r15, 0x130
0019E217  add      r9, qword ptr [rsp + 0x38]
0019E21C  movzx    eax, byte ptr [rsp + 0x30]
0019E221  mov      byte ptr [rsp + 0x20], al
0019E225  mov      r8, qword ptr [r14 + 8]
0019E229  mov      rdx, rbp
0019E22C  lea      rcx, [rsp + 0x38]
0019E231  call     0x19d1d0  ; -> 0019D1D0 fn
0019E236  mov      r8, qword ptr [r14 + 8]
0019E23A  mov      rdx, qword ptr [r14]
0019E23D  mov      rcx, r14
0019E240  call     0x19df90  ; -> 0019DF90 fn
0019E245  mov      r10, qword ptr [r14]
0019E248  test     r10, r10
0019E24B  je       0x19e27f  ; -> 0019E27F
0019E24D  lea      rcx, [r14 + 0x18]
0019E251  mov      r9, qword ptr [rcx]
0019E254  mov      r8, qword ptr [r14 + 0x10]
0019E258  sub      r8, r10
0019E25B  mov      rax, r12
0019E25E  imul     r8
0019E261  sar      rdx, 3
0019E265  mov      rax, rdx
0019E268  shr      rax, 0x3f
0019E26C  add      rax, rdx
0019E26F  mov      eax, eax
0019E271  imul     r8, rax, 0x130
0019E278  mov      rdx, r10
0019E27B  call     qword ptr [r9 + 0x18]
0019E27F  mov      qword ptr [r14], rsi
0019E282  mov      rax, qword ptr [rsp + 0x38]
0019E287  mov      qword ptr [r14 + 8], rax
0019E28B  mov      eax, edi
0019E28D  imul     rcx, rax, 0x130
0019E294  add      rcx, rsi
0019E297  mov      qword ptr [r14 + 0x10], rcx
0019E29B  mov      rcx, qword ptr [rsp + 0x180]
0019E2A3  xor      rcx, rsp
0019E2A6  call     0x808c40  ; -> 00808C40 fn
0019E2AB  add      rsp, 0x190
0019E2B2  pop      r15
0019E2B4  pop      r14
0019E2B6  pop      r12
0019E2B8  pop      rdi
0019E2B9  pop      rsi
0019E2BA  pop      rbp
0019E2BB  pop      rbx
0019E2BC  ret      
```

## 0019E740 (107 B, extent 0019E740-0019E7AB)

Documented callee on this page: `00199F10`

```
0019E740  push     rdi
0019E742  sub      rsp, 0x20
0019E746  mov      rdi, qword ptr [rdx + 0x110]
0019E74D  test     rdi, rdi
0019E750  je       0x19e7a5  ; -> 0019E7A5
0019E752  mov      rcx, qword ptr [rdi + 0x108]
0019E759  sub      rcx, qword ptr [rdi + 0x100]
0019E760  movsx    eax, word ptr [rdx]
0019E763  sar      rcx, 3
0019E767  dec      ecx
0019E769  cmp      eax, ecx
0019E76B  jne      0x19e7a5  ; -> 0019E7A5
0019E76D  mov      qword ptr [rsp + 0x30], rbx
0019E772  call     0x19a180  ; -> 0019A180 fn
0019E777  mov      rcx, rax
0019E77A  call     0x199f10  ; -> 00199F10 fn
0019E77F  mov      rbx, rax
0019E782  lea      rax, [rip + 0x6c7]  ; -> 0019EE50
0019E789  mov      qword ptr [rbx], rax
0019E78C  mov      qword ptr [rbx + 8], rdi
0019E790  call     0x19a180  ; -> 0019A180 fn
0019E795  mov      rcx, rax
0019E798  mov      rdx, rbx
0019E79B  call     0x19a000  ; -> 0019A000 fn
0019E7A0  mov      rbx, qword ptr [rsp + 0x30]
0019E7A5  add      rsp, 0x20
0019E7A9  pop      rdi
0019E7AA  ret      
```
