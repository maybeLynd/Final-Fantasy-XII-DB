# F homing pack (FABLE): `16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 2. No bearing page cites them and no documented function calls them directly.

## 003CA530 (810 B, extent 003CA530-003CA85A)

Documented callee on this page: `00272CB0`

```
003CA530  push     rsi
003CA532  push     rdi
003CA533  sub      rsp, 0xd8
003CA53A  mov      rax, qword ptr [rip + 0x1b7a2ef]  ; -> 01F44830 [u64 0x00002B992DDFA232]
003CA541  xor      rax, rsp
003CA544  mov      qword ptr [rsp + 0xa0], rax
003CA54C  mov      rdi, rcx
003CA54F  mov      ecx, dword ptr [rdx]
003CA551  sub      ecx, 1
003CA554  je       0x3ca7ba  ; -> 003CA7BA
003CA55A  cmp      ecx, 1
003CA55D  je       0x3ca56c  ; -> 003CA56C
003CA55F  mov      rcx, rdi
003CA562  call     0x5c5230  ; -> 005C5230 fn
003CA567  jmp      0x3ca840  ; -> 003CA840
003CA56C  mov      qword ptr [rsp + 0x100], rbx
003CA574  lea      rdx, [rsp + 0x38]
003CA579  mov      qword ptr [rsp + 0xd0], rbp
003CA581  xor      ecx, ecx
003CA583  mov      qword ptr [rsp + 0xc0], r13
003CA58B  mov      qword ptr [rsp + 0xb0], r15
003CA593  call     0x3200a0  ; -> 003200A0 fn
003CA598  xor      esi, esi
003CA59A  test     rdi, rdi
003CA59D  jne      0x3ca5a3  ; -> 003CA5A3
003CA59F  mov      ebp, esi
003CA5A1  jmp      0x3ca5ab  ; -> 003CA5AB
003CA5A3  mov      rax, qword ptr [rdi + 0x60]
003CA5A7  mov      rbp, qword ptr [rax + 0x18]
003CA5AB  movss    xmm2, dword ptr [rsp + 0x44]
003CA5B1  comiss   xmm2, dword ptr [rip + 0x19215f0]  ; -> 01CEBBA8 [f32 1]
003CA5B8  mov      rbp, qword ptr [rbp + 0x18]
003CA5BC  movaps   xmm1, xmm2
003CA5BF  cvttss2si r15d, xmm2
003CA5C4  movd     xmm0, r15d
003CA5C9  cvtdq2ps xmm0, xmm0
003CA5CC  subss    xmm1, xmm0
003CA5D0  mulss    xmm1, dword ptr [rip + 0x52dba8]  ; -> 008F8180 [f32 10]
003CA5D8  cvttss2si r13d, xmm1
003CA5DD  jb       0x3ca5ed  ; -> 003CA5ED
003CA5DF  xor      ecx, ecx
003CA5E1  call     0x2dd7e0  ; -> 002DD7E0 fn
003CA5E6  mov      ebx, eax
003CA5E8  jmp      0x3ca748  ; -> 003CA748
003CA5ED  xorps    xmm0, xmm0
003CA5F0  mov      qword ptr [rsp + 0xc8], r12
003CA5F8  comiss   xmm0, xmm2
003CA5FB  mov      r12d, 0x80
003CA601  jb       0x3ca662  ; -> 003CA662
003CA603  mov      ebx, dword ptr [rdi + 0xc0]
003CA609  xorps    xmm0, xmm0
003CA60C  mov      qword ptr [rsp + 0xb8], r14
003CA614  mov      r14d, dword ptr [rip + 0x1cc4f55]  ; -> 0208F570
003CA61B  mov      eax, r14d
003CA61E  sub      eax, ebx
003CA620  cvtsi2ss xmm0, rax
003CA625  mulss    xmm0, dword ptr [rip + 0x1921623]  ; -> 01CEBC50 [f32 3.141593]
003CA62D  divss    xmm0, dword ptr [rip + 0x52e74b]  ; -> 008F8D80 [f32 30]
003CA635  call     0x861f0e  ; -> 00861F0E fn
003CA63A  mulss    xmm0, dword ptr [rip + 0x54bcd6]  ; -> 00916318 [f32 64]
003CA642  addss    xmm0, dword ptr [rip + 0x5293e2]  ; -> 008F3A2C [f32 128]
003CA64A  cvttss2si r12d, xmm0
003CA64F  test     ebx, ebx
003CA651  jne      0x3ca65a  ; -> 003CA65A
003CA653  mov      dword ptr [rdi + 0xc0], r14d
003CA65A  mov      r14, qword ptr [rsp + 0xb8]
003CA662  mov      ecx, 6
003CA667  call     0x2dd7e0  ; -> 002DD7E0 fn
003CA66C  xor      ecx, ecx
003CA66E  mov      dword ptr [rsp + 0x30], eax
003CA672  mov      ebx, eax
003CA674  call     0x2dd7e0  ; -> 002DD7E0 fn
003CA679  movss    xmm0, dword ptr [rsp + 0x44]
003CA67F  lea      r8, [rsp + 0x70]
003CA684  mulss    xmm0, dword ptr [rip + 0x54b374]  ; -> 00915A00 [f32 256]
003CA68C  lea      rdx, [rsp + 0x80]
003CA694  movzx    ecx, bl
003CA697  mov      dword ptr [rsp + 0x80], ecx
003CA69E  movzx    ecx, byte ptr [rsp + 0x31]
003CA6A3  mov      dword ptr [rsp + 0x84], ecx
003CA6AA  movzx    ecx, byte ptr [rsp + 0x32]
003CA6AF  mov      dword ptr [rsp + 0x88], ecx
003CA6B6  movzx    ecx, byte ptr [rsp + 0x33]
003CA6BB  mov      dword ptr [rsp + 0x8c], ecx
003CA6C2  movzx    ecx, al
003CA6C5  mov      dword ptr [rsp + 0x70], ecx
003CA6C9  mov      ecx, eax
003CA6CB  shr      ecx, 8
003CA6CE  movzx    ecx, cl
003CA6D1  mov      dword ptr [rsp + 0x74], ecx
003CA6D5  mov      ecx, eax
003CA6D7  shr      ecx, 0x10
003CA6DA  movzx    ecx, cl
003CA6DD  mov      dword ptr [rsp + 0x78], ecx
003CA6E1  lea      rcx, [rsp + 0x90]
003CA6E9  shr      eax, 0x18
003CA6EC  cvttss2si r9d, xmm0
003CA6F1  mov      dword ptr [rsp + 0x7c], eax
003CA6F5  call     0x2752e0  ; -> 002752E0 fn
003CA6FA  mov      eax, dword ptr [rsp + 0x90]
003CA701  imul     eax, r12d
003CA705  sar      eax, 7
003CA708  mov      byte ptr [rsp + 0x30], al
003CA70C  mov      eax, dword ptr [rsp + 0x94]
003CA713  imul     eax, r12d
003CA717  sar      eax, 7
003CA71A  mov      byte ptr [rsp + 0x31], al
003CA71E  mov      eax, dword ptr [rsp + 0x98]
003CA725  imul     eax, r12d
003CA729  mov      r12, qword ptr [rsp + 0xc8]
003CA731  sar      eax, 7
003CA734  mov      byte ptr [rsp + 0x32], al
003CA738  movzx    eax, byte ptr [rsp + 0x9c]
003CA740  mov      byte ptr [rsp + 0x33], al
003CA744  mov      ebx, dword ptr [rsp + 0x30]
003CA748  test     rbp, rbp
003CA74B  jne      0x3ca752  ; -> 003CA752
003CA74D  mov      rcx, rsi
003CA750  jmp      0x3ca759  ; -> 003CA759
003CA752  mov      rax, qword ptr [rbp + 0x60]
003CA756  mov      rcx, qword ptr [rax]
003CA759  mov      edx, 3
003CA75E  mov      dword ptr [rsp + 0x20], r15d
003CA763  mov      r9d, ebx
003CA766  lea      r8d, [rdx + 2]
003CA76A  call     0x29f6e0  ; -> 0029F6E0 fn
003CA76F  mov      r15, qword ptr [rsp + 0xb0]
003CA777  test     rbp, rbp
003CA77A  je       0x3ca784  ; -> 003CA784
003CA77C  mov      rax, qword ptr [rbp + 0x60]
003CA780  mov      rsi, qword ptr [rax + 0x18]
003CA784  mov      edx, 1
003CA789  mov      dword ptr [rsp + 0x20], r13d
003CA78E  mov      r9d, ebx
003CA791  mov      rcx, rsi
003CA794  lea      r8d, [rdx + 4]
003CA798  call     0x29f6e0  ; -> 0029F6E0 fn
003CA79D  mov      r13, qword ptr [rsp + 0xc0]
003CA7A5  mov      rbp, qword ptr [rsp + 0xd0]
003CA7AD  mov      rbx, qword ptr [rsp + 0x100]
003CA7B5  jmp      0x3ca83e  ; -> 003CA83E
003CA7BA  mov      rax, qword ptr [rip + 0x1cd046f]  ; -> 0209AC30
003CA7C1  lea      rcx, [rdi + 0x50]
003CA7C5  mov      r9, rdi
003CA7C8  mov      r8d, 3
003CA7CE  mov      rdx, qword ptr [rax + 0x28]
003CA7D2  call     0x2432b0  ; -> 002432B0 fn
003CA7D7  movzx    ecx, word ptr [rax + 0xa]
003CA7DB  movzx    edx, word ptr [rax + 8]
003CA7DF  movsx    r8d, word ptr [rax + 6]
003CA7E4  test     rdi, rdi
003CA7E7  je       0x3ca80a  ; -> 003CA80A
003CA7E9  movzx    eax, word ptr [rax + 4]
003CA7ED  mov      word ptr [rdi + 0x98], ax
003CA7F4  mov      word ptr [rdi + 0x9a], r8w
003CA7FC  mov      word ptr [rdi + 0x9c], dx
003CA803  mov      word ptr [rdi + 0x9e], cx
003CA80A  lea      rdx, [rsp + 0x38]
003CA80F  xor      ecx, ecx
003CA811  call     0x3200a0  ; -> 003200A0 fn
003CA816  test     rdi, rdi
003CA819  jne      0x3ca81f  ; -> 003CA81F
003CA81B  xor      esi, esi
003CA81D  jmp      0x3ca827  ; -> 003CA827
003CA81F  mov      rax, qword ptr [rdi + 0x60]
003CA823  mov      rsi, qword ptr [rax + 8]
003CA827  mov      ecx, dword ptr [rsp + 0x40]
003CA82B  call     0x272cb0  ; -> 00272CB0 fn
003CA830  xor      ecx, ecx
003CA832  mov      qword ptr [rsi + 0x18], rax
003CA836  call     0x20e620  ; -> 0020E620 fn
003CA83B  mov      dword ptr [rsi + 0x20], eax
003CA83E  xor      eax, eax
003CA840  mov      rcx, qword ptr [rsp + 0xa0]
003CA848  xor      rcx, rsp
003CA84B  call     0x808c40  ; -> 00808C40 fn
003CA850  add      rsp, 0xd8
003CA857  pop      rdi
003CA858  pop      rsi
003CA859  ret      
```

## 00404E10 (264 B, extent 00404E10-00404F18)

Documented callee on this page: `00406DD0`

```
00404E10  sub      rsp, 0x28
00404E14  mov      rcx, qword ptr [rip + 0x275df6d]  ; -> 02B62D88
00404E1B  test     rcx, rcx
00404E1E  je       0x404f13  ; -> 00404F13
00404E24  mov      rax, qword ptr [rcx + 0xc0]
00404E2B  test     rax, rax
00404E2E  je       0x404f13  ; -> 00404F13
00404E34  test     byte ptr [rax + 0xc2], 1
00404E3B  jne      0x404f13  ; -> 00404F13
00404E41  xor      edx, edx
00404E43  mov      qword ptr [rsp + 0x20], rdi
00404E48  call     0x406dd0  ; -> 00406DD0 fn
00404E4D  mov      rdx, qword ptr [rip + 0x275df34]  ; -> 02B62D88
00404E54  xor      edi, edi
00404E56  mov      r8d, edi
00404E59  mov      ecx, edi
00404E5B  mov      rax, qword ptr [rdx + 0xc0]
00404E62  or       byte ptr [rax + 0xc2], 1
00404E69  movzx    r9d, byte ptr [rdx + 0xe3]
00404E71  test     r9, r9
00404E74  je       0x404e94  ; -> 00404E94
00404E76  mov      rax, qword ptr [rdx + 0xe8]
00404E7D  add      rax, 8
00404E81  cmp      dword ptr [rax], edi
00404E83  jg       0x404e94  ; -> 00404E94
00404E85  inc      r8d
00404E88  inc      rcx
00404E8B  add      rax, 0x18
00404E8F  cmp      rcx, r9
00404E92  jl       0x404e81  ; -> 00404E81
00404E94  cmp      r8d, r9d
00404E97  jge      0x404eae  ; -> 00404EAE
00404E99  mov      rcx, qword ptr [rdx + 0xc0]
00404EA0  mov      rdi, qword ptr [rsp + 0x20]
00404EA5  add      rsp, 0x28
00404EA9  jmp      0x244f00  ; -> 00244F00 fn
00404EAE  mov      qword ptr [rsp + 0x30], rbx
00404EB3  mov      ebx, 0xc8
00404EB8  test     rdx, rdx
00404EBB  je       0x404ef9  ; -> 00404EF9
00404EBD  mov      rcx, qword ptr [rdx + 0xc0]
00404EC4  test     rcx, rcx
00404EC7  je       0x404ef9  ; -> 00404EF9
00404EC9  cmp      rdi, 2
00404ECD  jge      0x404ef9  ; -> 00404EF9
00404ECF  mov      rcx, qword ptr [rbx + rcx]
00404ED3  test     rcx, rcx
00404ED6  je       0x404ef9  ; -> 00404EF9
00404ED8  mov      eax, dword ptr [rcx + 0x130]
00404EDE  test     al, 0x10
00404EE0  je       0x404eed  ; -> 00404EED
00404EE2  or       eax, 8
00404EE5  mov      dword ptr [rcx + 0x130], eax
00404EEB  jmp      0x404ef9  ; -> 00404EF9
00404EED  call     0x245020  ; -> 00245020 fn
00404EF2  mov      rdx, qword ptr [rip + 0x275de8f]  ; -> 02B62D88
00404EF9  inc      rdi
00404EFC  add      rbx, 8
00404F00  cmp      rbx, 0xd8
00404F07  jl       0x404eb8  ; -> 00404EB8
00404F09  mov      rbx, qword ptr [rsp + 0x30]
00404F0E  mov      rdi, qword ptr [rsp + 0x20]
00404F13  add      rsp, 0x28
00404F17  ret      
```
