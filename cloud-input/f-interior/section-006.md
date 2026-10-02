# F-interior pack: `25-EBP-Script-Container/Sections/section-006.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/section-006.json`.

Functions: 4. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 01c2429f6	SWE2-CONTRACT: pass-22 debt batch B - 47 Script-VM, Resource, EBP and PKFL pages' cross-subsystem ne; inbox mentions: SWE2-CONTRACT.md, SWE2-DATA.md, SWE2-FRONTIER.md, repos-c9.md). OPUS read these before packing.

## 001B1C10 (852 B, extent 001B1C10-001B1F64)

Page context: "e-cited '00674A00', '00249210'); 5 outbound (page-cited '00249210', '003BC2D0', '003C2210' call Resource bodies '0032E620', '0032E400', '00249210'). Substantive edges include '00674A00' is called by '001B1C10'; '00674A00' is called by '001B1440'; '00674A00' is called by '0020BE50'; '00674A00' is called by '0020C1B0'; the remaining edges run through shared helpers the page cites. - **Story_Event_Quest_Hunt — SERVICE (1 edge).** 1 outboun"

```
001B1C10  mov      rax, rsp
001B1C13  push     rbp
001B1C14  push     r14
001B1C16  push     r15
001B1C18  lea      rbp, [rax - 0x1b8]
001B1C1F  sub      rsp, 0x2a0
001B1C26  mov      qword ptr [rsp + 0x78], 0xfffffffffffffffe
001B1C2F  mov      qword ptr [rax + 8], rbx
001B1C33  mov      qword ptr [rax + 0x10], rsi
001B1C37  mov      qword ptr [rax + 0x18], rdi
001B1C3B  mov      rax, qword ptr [rip + 0x1d92bee]  ; -> 01F44830 [u64 0x00002B992DDFA232]
001B1C42  xor      rax, rsp
001B1C45  mov      qword ptr [rbp + 0x190], rax
001B1C4C  mov      rbx, rcx
001B1C4F  mov      rax, qword ptr [rip + 0x1dcf592]  ; -> 01F811E8
001B1C56  test     rax, rax
001B1C59  je       0x1b1f38  ; -> 001B1F38
001B1C5F  lea      r14, [rax + 0x20]
001B1C63  xor      edx, edx
001B1C65  mov      r8d, 0x100
001B1C6B  lea      rcx, [rbp - 0x70]
001B1C6F  call     0x861ec0  ; -> 00861EC0 fn
001B1C74  xor      edx, edx
001B1C76  mov      r8d, 0x100
001B1C7C  lea      rcx, [rbp + 0x90]
001B1C83  call     0x861ec0  ; -> 00861EC0 fn
001B1C88  mov      r8, qword ptr [rbx]
001B1C8B  xor      r15d, r15d
001B1C8E  mov      eax, r15d
001B1C91  movzx    ecx, byte ptr [r8]
001B1C95  inc      eax
001B1C97  test     cl, cl
001B1C99  je       0x1b1ca2  ; -> 001B1CA2
001B1C9B  cmp      eax, 0x100
001B1CA0  jl       0x1b1c95  ; -> 001B1C95
001B1CA2  movsxd   rdx, eax
001B1CA5  lea      rcx, [rbp - 0x70]
001B1CA9  call     0x19c5d0  ; -> 0019C5D0 fn
001B1CAE  lea      rdx, [rip + 0x74494b]  ; -> 008F6600 [str "EASTL basic_string"]
001B1CB5  lea      rcx, [rbp - 0x80]
001B1CB9  call     0x1edf00  ; -> 001EDF00 fn
001B1CBE  xorps    xmm0, xmm0
001B1CC1  movdqu   xmmword ptr [rsp + 0x38], xmm0
001B1CC7  mov      qword ptr [rsp + 0x48], r15
001B1CCC  mov      rdx, rax
001B1CCF  lea      rcx, [rsp + 0x50]
001B1CD4  call     0x1edf00  ; -> 001EDF00 fn
001B1CD9  lea      rcx, [rbp - 0x70]
001B1CDD  or       rax, 0xffffffffffffffff
001B1CE1  inc      rax
001B1CE4  cmp      byte ptr [rcx + rax], r15b
001B1CE8  jne      0x1b1ce1  ; -> 001B1CE1
001B1CEA  lea      rsi, [rbp - 0x70]
001B1CEE  add      rsi, rax
001B1CF1  lea      rcx, [rbp - 0x70]
001B1CF5  mov      eax, esi
001B1CF7  sub      eax, ecx
001B1CF9  inc      eax
001B1CFB  cmp      eax, 1
001B1CFE  jbe      0x1b1d2c  ; -> 001B1D2C
001B1D00  mov      ebx, eax
001B1D02  xor      r8d, r8d
001B1D05  mov      edx, eax
001B1D07  lea      rcx, [rsp + 0x50]
001B1D0C  mov      rax, qword ptr [rsp + 0x50]
001B1D11  call     qword ptr [rax + 0x10]
001B1D14  mov      rdi, rax
001B1D17  mov      qword ptr [rsp + 0x38], rax
001B1D1C  mov      qword ptr [rsp + 0x40], rax
001B1D21  lea      rcx, [rbx + rax]
001B1D25  mov      qword ptr [rsp + 0x48], rcx
001B1D2A  jmp      0x1b1d49  ; -> 001B1D49
001B1D2C  lea      rdi, [rip + 0x2d085ad]  ; -> 02EBA2E0
001B1D33  mov      qword ptr [rsp + 0x38], rdi
001B1D38  mov      qword ptr [rsp + 0x40], rdi
001B1D3D  lea      rax, [rip + 0x2d0859d]  ; -> 02EBA2E1
001B1D44  mov      qword ptr [rsp + 0x48], rax
001B1D49  lea      rax, [rbp - 0x70]
001B1D4D  mov      r8, rsi
001B1D50  sub      r8, rax
001B1D53  lea      rdx, [rbp - 0x70]
001B1D57  mov      rcx, rdi
001B1D5A  call     qword ptr [rip + 0x710ce0]  ; -> 008C2A40 [u64 0x0000000001CCEB62]
001B1D60  lea      rax, [rbp - 0x70]
001B1D64  sub      rdi, rax
001B1D67  add      rdi, rsi
001B1D6A  mov      qword ptr [rsp + 0x40], rdi
001B1D6F  mov      byte ptr [rdi], r15b
001B1D72  mov      rbx, qword ptr [rsp + 0x38]
001B1D77  cmp      rbx, qword ptr [rsp + 0x40]
001B1D7C  jae      0x1b1d9a  ; -> 001B1D9A
001B1D7E  nop      
001B1D80  movzx    ecx, byte ptr [rbx]
001B1D83  call     qword ptr [rip + 0x711297]  ; -> 008C3020 [u64 0x0000000001CCEF32]
001B1D89  mov      byte ptr [rbx], al
001B1D8B  inc      rbx
001B1D8E  cmp      rbx, qword ptr [rsp + 0x40]
001B1D93  jb       0x1b1d80  ; -> 001B1D80
001B1D95  mov      rbx, qword ptr [rsp + 0x38]
001B1D9A  mov      rdx, rbx
001B1D9D  lea      rcx, [rbp + 0x90]
001B1DA4  call     0x1a1e40  ; -> 001A1E40 fn
001B1DA9  cmp      byte ptr [rbp - 0x70], 0
001B1DAD  je       0x1b1f0a  ; -> 001B1F0A
001B1DB3  lea      rcx, [rbp + 0x90]
001B1DBA  call     0x674a00  ; -> 00674A00 fn
001B1DBF  mov      ebx, eax
001B1DC1  mov      rdx, qword ptr [r14 + 0x18]
001B1DC5  lea      rsi, [r14 + 8]
001B1DC9  mov      rcx, rsi
001B1DCC  test     rdx, rdx
001B1DCF  je       0x1b1de7  ; -> 001B1DE7
001B1DD1  cmp      dword ptr [rdx + 0x20], ebx
001B1DD4  jb       0x1b1ddf  ; -> 001B1DDF
001B1DD6  mov      rcx, rdx
001B1DD9  mov      rdx, qword ptr [rdx + 8]
001B1DDD  jmp      0x1b1de2  ; -> 001B1DE2
001B1DDF  mov      rdx, qword ptr [rdx]
001B1DE2  test     rdx, rdx
001B1DE5  jne      0x1b1dd1  ; -> 001B1DD1
001B1DE7  cmp      rcx, rsi
001B1DEA  je       0x1b1df1  ; -> 001B1DF1
001B1DEC  cmp      ebx, dword ptr [rcx + 0x20]
001B1DEF  jae      0x1b1df4  ; -> 001B1DF4
001B1DF1  mov      rcx, rsi
001B1DF4  cmp      rcx, rsi
001B1DF7  jne      0x1b1f0a  ; -> 001B1F0A
001B1DFD  call     0x19ce20  ; -> 0019CE20 fn
001B1E02  mov      rcx, rax
001B1E05  lea      rdx, [rbp - 0x70]
001B1E09  call     0x19ca80  ; -> 0019CA80 fn
001B1E0E  test     rax, rax
001B1E11  je       0x1b1f0a  ; -> 001B1F0A
001B1E17  lea      rdx, [rax + 0x38]
001B1E1B  mov      rcx, qword ptr [rdx]
001B1E1E  cmp      rcx, rdx
001B1E21  lea      r8, [rip + 0x2b09ad8]  ; -> 02CBB900
001B1E28  cmove    rcx, r15
001B1E2C  test     rcx, rcx
001B1E2F  je       0x1b1f0a  ; -> 001B1F0A
001B1E35  mov      rax, qword ptr [rcx + 0x50]
001B1E39  test     rax, rax
001B1E3C  je       0x1b1e56  ; -> 001B1E56
001B1E3E  nop      
001B1E40  cmp      rax, r8
001B1E43  je       0x1b1e50  ; -> 001B1E50
001B1E45  mov      rax, qword ptr [rax + 0x78]
001B1E49  test     rax, rax
001B1E4C  jne      0x1b1e40  ; -> 001B1E40
001B1E4E  jmp      0x1b1e56  ; -> 001B1E56
001B1E50  cmp      dword ptr [rcx + 0x74], 0
001B1E54  ja       0x1b1e61  ; -> 001B1E61
001B1E56  mov      rax, qword ptr [rcx]
001B1E59  mov      rcx, rax
001B1E5C  cmp      rax, rdx
001B1E5F  jmp      0x1b1e28  ; -> 001B1E28
001B1E61  test     rcx, rcx
001B1E64  je       0x1b1f0a  ; -> 001B1F0A
001B1E6A  mov      rax, qword ptr [rcx + 0x50]
001B1E6E  mov      r9d, dword ptr [rax + 0x38]
001B1E72  mov      rdx, qword ptr [rcx + 0x60]
001B1E76  mov      r8d, dword ptr [rcx + 0x74]
001B1E7A  mov      r10d, dword ptr [rax + 0xf8]
001B1E81  mov      rax, qword ptr [rcx + 0x10]
001B1E85  test     r8d, r8d
001B1E88  je       0x1b1f0a  ; -> 001B1F0A
001B1E8E  cmp      rdx, rax
001B1E91  jne      0x1b1e9e  ; -> 001B1E9E
001B1E93  add      rdx, r9
001B1E96  mov      rax, qword ptr [rax]
001B1E99  cmp      rdx, rax
001B1E9C  je       0x1b1e93  ; -> 001B1E93
001B1E9E  test     r8d, r8d
001B1EA1  je       0x1b1f0a  ; -> 001B1F0A
001B1EA3  lea      rdi, [rdx + r10]
001B1EA7  mov      rcx, qword ptr [r14 + 0x18]
001B1EAB  mov      rax, rsi
001B1EAE  test     rcx, rcx
001B1EB1  je       0x1b1ec9  ; -> 001B1EC9
001B1EB3  cmp      dword ptr [rcx + 0x20], ebx
001B1EB6  jb       0x1b1ec1  ; -> 001B1EC1
001B1EB8  mov      rax, rcx
001B1EBB  mov      rcx, qword ptr [rcx + 8]
001B1EBF  jmp      0x1b1ec4  ; -> 001B1EC4
001B1EC1  mov      rcx, qword ptr [rcx]
001B1EC4  test     rcx, rcx
001B1EC7  jne      0x1b1eb3  ; -> 001B1EB3
001B1EC9  cmp      rax, rsi
001B1ECC  je       0x1b1ed3  ; -> 001B1ED3
001B1ECE  cmp      ebx, dword ptr [rax + 0x20]
001B1ED1  jae      0x1b1f06  ; -> 001B1F06
001B1ED3  mov      dword ptr [rsp + 0x68], ebx
001B1ED7  mov      qword ptr [rsp + 0x70], r15
001B1EDC  mov      qword ptr [rsp + 0x58], rax
001B1EE1  movzx    eax, byte ptr [rsp + 0x30]
001B1EE6  mov      byte ptr [rsp + 0x20], al
001B1EEA  lea      r9, [rsp + 0x68]
001B1EEF  lea      r8, [rsp + 0x58]
001B1EF4  lea      rdx, [rsp + 0x60]
001B1EF9  mov      rcx, r14
001B1EFC  call     0x1ae9b0  ; -> 001AE9B0 fn
001B1F01  mov      rax, qword ptr [rsp + 0x60]
001B1F06  mov      qword ptr [rax + 0x28], rdi
001B1F0A  mov      rcx, qword ptr [rsp + 0x48]
001B1F0F  mov      rax, rcx
001B1F12  mov      rdx, qword ptr [rsp + 0x38]
001B1F17  sub      rax, rdx
001B1F1A  cmp      rax, 1
001B1F1E  jle      0x1b1f38  ; -> 001B1F38
001B1F20  sub      ecx, edx
001B1F22  test     rdx, rdx
001B1F25  je       0x1b1f38  ; -> 001B1F38
001B1F27  mov      r8d, ecx
001B1F2A  lea      rcx, [rsp + 0x50]
001B1F2F  mov      rax, qword ptr [rsp + 0x50]
001B1F34  call     qword ptr [rax + 0x18]
001B1F37  nop      
001B1F38  mov      rcx, qword ptr [rbp + 0x190]
001B1F3F  xor      rcx, rsp
001B1F42  call     0x808c40  ; -> 00808C40 fn
001B1F47  lea      r11, [rsp + 0x2a0]
001B1F4F  mov      rbx, qword ptr [r11 + 0x20]
001B1F53  mov      rsi, qword ptr [r11 + 0x28]
001B1F57  mov      rdi, qword ptr [r11 + 0x30]
001B1F5B  mov      rsp, r11
001B1F5E  pop      r15
001B1F60  pop      r14
001B1F62  pop      rbp
001B1F63  ret      
```

## 00249350 (37 B, extent 00249350-00249375)

Page context: "'002B0280'; '0039C4A0' is called by '002AAE40'; the remaining edges run through shared helpers the page cites. - **Resource — CLIENT and SERVICE (16 edges).** 11 inbound (Resource bodies '002493D0', '00249350', '00249380' call page-cited '00674A00', '00249210'); 5 outbound (page-cited '00249210', '003BC2D0', '003C2210' call Resource bodies '0032E620', '0032E400', '00249210'). Substantive edges include '00674A00' is called by '001B1C10';"

```
00249350  sub      rsp, 0x38
00249354  mov      dword ptr [rsp + 0x20], 0
0024935C  call     0x249210  ; -> 00249210 fn
00249361  lea      rcx, [rip + 0x2f8]  ; -> 00249660
00249368  mov      qword ptr [rax + 0x10], rcx
0024936C  mov      rax, qword ptr [rax + 8]
00249370  add      rsp, 0x38
00249374  ret      
```

## 00249380 (73 B, extent 00249380-002493C9)

Page context: "'0039C4A0' is called by '002AAE40'; the remaining edges run through shared helpers the page cites. - **Resource — CLIENT and SERVICE (16 edges).** 11 inbound (Resource bodies '002493D0', '00249350', '00249380' call page-cited '00674A00', '00249210'); 5 outbound (page-cited '00249210', '003BC2D0', '003C2210' call Resource bodies '0032E620', '0032E400', '00249210'). Substantive edges include '00674A00' is called by '001B1C10'; '00674A00' "

```
00249380  mov      qword ptr [rsp + 8], rbx
00249385  push     rdi
00249386  sub      rsp, 0x30
0024938A  mov      rdi, r9
0024938D  mov      dword ptr [rsp + 0x20], 1
00249395  mov      r9d, 3
0024939B  call     0x249210  ; -> 00249210 fn
002493A0  mov      edx, dword ptr [rsp + 0x60]
002493A4  mov      rcx, rdi
002493A7  mov      rbx, rax
002493AA  call     0x24a4e0  ; -> 0024A4E0 fn
002493AF  lea      rcx, [rip + 0x2ba]  ; -> 00249670
002493B6  mov      qword ptr [rbx + 0x18], rax
002493BA  mov      qword ptr [rbx + 0x10], rcx
002493BE  mov      rbx, qword ptr [rsp + 0x40]
002493C3  add      rsp, 0x30
002493C7  pop      rdi
002493C8  ret      
```

## 0035C160 (651 B, extent 0035C160-0035C3EB)

Page context: "IENT (1 edge).** '0024A680' is also called by world-filed '003C63A0' — the same shared free. - **Presentation — CLIENT and SERVICE (8 edges).** 7 inbound (Presentation bodies '002B7B80', '002BAF80', '0035C160' call page-cited '00249410', '00249580', '0039C4A0'); 1 outbound (page-cited '0017F790' call Presentation bodies '001B47A0'). Substantive edges include '0017F790' calls '001B47A0'; '002B3400' is called by '0035C160'; '0039C4A0' is "

```
0035C160  push     rbx
0035C162  push     rbp
0035C163  push     rsi
0035C164  push     r14
0035C166  push     r15
0035C168  sub      rsp, 0x130
0035C16F  mov      rax, qword ptr [rip + 0x1be86ba]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0035C176  xor      rax, rsp
0035C179  mov      qword ptr [rsp + 0x110], rax
0035C181  mov      rsi, rcx
0035C184  mov      ecx, dword ptr [rdx]
0035C186  sub      ecx, 1
0035C189  je       0x35c370  ; -> 0035C370
0035C18F  sub      ecx, 3
0035C192  je       0x35c1bd  ; -> 0035C1BD
0035C194  sub      ecx, 8
0035C197  je       0x35c1af  ; -> 0035C1AF
0035C199  cmp      ecx, 6
0035C19C  je       0x35c3ca  ; -> 0035C3CA
0035C1A2  mov      rcx, rsi
0035C1A5  call     0x5c5230  ; -> 005C5230 fn
0035C1AA  jmp      0x35c3cc  ; -> 0035C3CC
0035C1AF  xor      eax, eax
0035C1B1  mov      qword ptr [rsi + 0xf0], rax
0035C1B8  jmp      0x35c3ca  ; -> 0035C3CA
0035C1BD  movsx    ebx, word ptr [rsi + 0xc0]
0035C1C4  lea      eax, [rbx - 2]
0035C1C7  cmp      eax, 3
0035C1CA  ja       0x35c3ca  ; -> 0035C3CA
0035C1D0  mov      eax, dword ptr [rip + 0x1d3339a]  ; -> 0208F570
0035C1D6  xorps    xmm0, xmm0
0035C1D9  mov      rbp, qword ptr [rsi + 0x38]
0035C1DD  cvtsi2ss xmm0, rax
0035C1E2  mulss    xmm0, dword ptr [rip + 0x198fa66]  ; -> 01CEBC50 [f32 3.141593]
0035C1EA  divss    xmm0, dword ptr [rip + 0x59cb8e]  ; -> 008F8D80 [f32 30]
0035C1F2  call     0x861f0e  ; -> 00861F0E fn
0035C1F7  mulss    xmm0, dword ptr [rip + 0x5b97f9]  ; -> 009159F8 [f32 32]
0035C1FF  addss    xmm0, dword ptr [rip + 0x5b9999]  ; -> 00915BA0 [f32 96]
0035C207  cvttss2si ecx, xmm0
0035C20B  cmp      ebx, 2
0035C20E  je       0x35c221  ; -> 0035C221
0035C210  cmp      ebx, 3
0035C213  je       0x35c364  ; -> 0035C364
0035C219  lea      eax, [rbx - 4]
0035C21C  cmp      eax, 1
0035C21F  ja       0x35c233  ; -> 0035C233
0035C221  mov      byte ptr [rbp + 0x90], cl
0035C227  mov      byte ptr [rbp + 0x92], cl
0035C22D  mov      byte ptr [rbp + 0x91], cl
0035C233  mov      ecx, dword ptr [rsi + 0xec]
0035C239  call     0x2ea230  ; -> 002EA230 fn
0035C23E  test     eax, eax
0035C240  jne      0x35c3ca  ; -> 0035C3CA
0035C246  mov      ecx, dword ptr [rsi + 0xec]
0035C24C  lea      rdx, [rsp + 0x20]
0035C251  call     0x2e9a90  ; -> 002E9A90 fn
0035C256  mov      r9d, 1
0035C25C  lea      r8, [rsp + 0x20]
0035C261  lea      rdx, [rip + 0x2791b48]  ; -> 02AEDDB0
0035C268  lea      rcx, [rsp + 0x100]
0035C270  call     0x249110  ; -> 00249110 fn
0035C275  mov      ecx, dword ptr [rsp + 0x108]
0035C27C  mov      r14d, dword ptr [rsp + 0x100]
0035C284  mov      r15d, dword ptr [rsp + 0x104]
0035C28C  cmp      ecx, 0x1000000
0035C292  jge      0x35c3ca  ; -> 0035C3CA
0035C298  mov      eax, 0x100000
0035C29D  mov      qword ptr [rsp + 0x170], rdi
0035C2A5  movaps   xmmword ptr [rsp + 0x120], xmm6
0035C2AD  cmp      ecx, eax
0035C2AF  jl       0x35c2bd  ; -> 0035C2BD
0035C2B1  mov      edx, 0x400000
0035C2B6  mov      eax, ecx
0035C2B8  cmp      ecx, edx
0035C2BA  cmovg    eax, edx
0035C2BD  mov      dword ptr [rsp + 0x108], eax
0035C2C4  lea      rdx, [rsi + 0xc8]
0035C2CB  add      eax, 0xfff00000
0035C2D0  lea      rcx, [rsp + 0x30]
0035C2D5  xor      r8d, r8d
0035C2D8  movd     xmm6, eax
0035C2DC  movsx    eax, word ptr [rsi + 0xe8]
0035C2E3  cvtdq2ps xmm6, xmm6
0035C2E6  movd     xmm0, eax
0035C2EA  mulss    xmm6, dword ptr [rip + 0x198f87e]  ; -> 01CEBB70 [f32 0.5]
0035C2F2  movsx    eax, word ptr [rsi + 0xea]
0035C2F9  cvtdq2ps xmm0, xmm0
0035C2FC  divss    xmm6, dword ptr [rip + 0x9b496c]  ; -> 00D10C70 [f32 3145728]
0035C304  addss    xmm6, dword ptr [rip + 0x198f864]  ; -> 01CEBB70 [f32 0.5]
0035C30C  mulss    xmm0, xmm6
0035C310  cvttss2si edi, xmm0
0035C314  movd     xmm0, eax
0035C318  cvtdq2ps xmm0, xmm0
0035C31B  mulss    xmm0, xmm6
0035C31F  cvttss2si ebx, xmm0
0035C323  call     0x2b3400  ; -> 002B3400 fn
0035C328  movsx    eax, bx
0035C32B  lea      r9, [rsp + 0x30]
0035C330  sub      r15d, eax
0035C333  movsx    eax, di
0035C336  cdq      
0035C337  mov      r8d, r15d
0035C33A  sub      eax, edx
0035C33C  mov      rcx, rbp
0035C33F  sar      eax, 1
0035C341  sub      r14d, eax
0035C344  movss    dword ptr [rsp + 0x64], xmm6
0035C34A  mov      edx, r14d
0035C34D  call     0x2d8650  ; -> 002D8650 fn
0035C352  movaps   xmm6, xmmword ptr [rsp + 0x120]
0035C35A  mov      rdi, qword ptr [rsp + 0x170]
0035C362  jmp      0x35c3ca  ; -> 0035C3CA
0035C364  mov      byte ptr [rbp + 0x90], 0x80
0035C36B  jmp      0x35c227  ; -> 0035C227
0035C370  mov      ecx, dword ptr [rip + 0x1aafe66]  ; -> 01E0C1DC [u32 0x000001C0]
0035C376  xor      eax, eax
0035C378  mov      edx, dword ptr [rip + 0x1aafe5a]  ; -> 01E0C1D8 [u32 0x00000200]
0035C37E  test     rsi, rsi
0035C381  je       0x35c397  ; -> 0035C397
0035C383  mov      dword ptr [rsi + 0x98], eax
0035C389  mov      word ptr [rsi + 0x9c], dx
0035C390  mov      word ptr [rsi + 0x9e], cx
0035C397  mov      byte ptr [rsi + 0xc8], al
0035C39D  mov      edx, 0xdc
0035C3A2  mov      rcx, rsi
0035C3A5  mov      dword ptr [rsi + 0xec], eax
0035C3AB  mov      word ptr [rsi + 0xc0], ax
0035C3B2  mov      dword ptr [rsi + 0xc4], eax
0035C3B8  call     0x247930  ; -> 00247930 fn
0035C3BD  mov      edx, 1
0035C3C2  mov      rcx, rsi
0035C3C5  call     0x247950  ; -> 00247950 fn
0035C3CA  xor      eax, eax
0035C3CC  mov      rcx, qword ptr [rsp + 0x110]
0035C3D4  xor      rcx, rsp
0035C3D7  call     0x808c40  ; -> 00808C40 fn
0035C3DC  add      rsp, 0x130
0035C3E3  pop      r15
0035C3E5  pop      r14
0035C3E7  pop      rsi
0035C3E8  pop      rbp
0035C3E9  pop      rbx
0035C3EA  ret      
```
