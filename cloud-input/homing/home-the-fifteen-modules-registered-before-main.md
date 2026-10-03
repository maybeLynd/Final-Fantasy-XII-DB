# Homing pack: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md`

Generated 2026-10-03 07:51 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-fifteen-modules-registered-before-main.json`.

Bodies: 15. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001DE200 (116 B, extent 001DE200-001DE274)

Entered from (direct sites whose caller this page cites): `001DE400` + 0x14 (call; `001DE400` is cited on this page)
Other direct sites: `001DE330` + 0x10 (call)

Host context: "or through IAT slot '008C25E8' with 'rcx'; when bit '0x1' of 'edx' is set it calls '00809950(rcx - 0x90, 0xF0)'; returns 'rcx' - 0x90 | '001DE3C4', '001DE3CC', '001DE3D2', '001DE3E4', '001DE3EE' | | '001DE400' | 80 B | calls '001DE200(rcx)' and the basic_ios<char> destructor through IAT slot '008C25E8' with 'rcx'; when bit '0x1' of 'edx' is set it calls '00809950(rcx - 0x88, 0xE8)'; returns 'rcx' - 0x88 | '001DE414', '001DE41C', '001DE4"

```
001DE200  mov      qword ptr [rsp + 8], rbx
001DE205  push     rdi
001DE206  sub      rsp, 0x20
001DE20A  mov      rax, qword ptr [rcx - 0x88]
001DE211  mov      rdi, rcx
001DE214  movsxd   rdx, dword ptr [rax + 4]
001DE218  lea      rax, [rip + 0x722e71]  ; -> 00901090
001DE21F  mov      qword ptr [rdx + rcx - 0x88], rax
001DE227  mov      rax, qword ptr [rcx - 0x88]
001DE22E  movsxd   rdx, dword ptr [rax + 4]
001DE232  lea      rax, [rip + 0x722ce7]  ; -> 00900F20
001DE239  lea      r8d, [rdx - 0x88]
001DE240  mov      dword ptr [rdx + rcx - 0x8c], r8d
001DE248  mov      qword ptr [rcx - 0x80], rax
001DE24C  add      rcx, -0x80
001DE250  call     0x1df8c0  ; -> 001DF8C0 fn
001DE255  lea      rcx, [rdi - 0x80]
001DE259  call     qword ptr [rip + 0x6e4541]  ; -> 008C27A0 [u64 0x0000000001CCDA9C]
001DE25F  lea      rcx, [rdi - 0x78]
001DE263  mov      rbx, qword ptr [rsp + 0x30]
001DE268  add      rsp, 0x20
001DE26C  pop      rdi
001DE26D  jmp      qword ptr [rip + 0x6e435c]  ; -> 008C25D0 [u64 0x0000000001CCDC3C]
```

## 0021EE00 (151 B, extent 0021EE00-0021EE97)

Entered from (direct sites whose caller this page cites): `0021EEA0` + 0x89 (call; `0021EEA0` is cited on this page)
Other direct sites: `0021E830` + 0x23 (jmp)

Host context: "slot '+0x18' of the object at 'rcx+0x18' with ('rcx+0x18', qword '[rcx]', ((qword '[rcx+0x10]' - qword '[rcx]') / 0xA, signed) * 0xA) | '0021E746', '0021E750', '0021E76C', '0021E787', '0021E791' | | '0021EEA0' | 273 B | stores '00908830' to qword '[rcx]' and calls '00220B80(rcx)', then '005CD6D0' on 'rcx+0x300', '+0x328', '+0x350' and '+0x378', '0021E970(rcx+0x3A0)', '0021EAF0' on '+0x2C0' and '+0x288', '0021EE00(rcx+0x268)', '0021EA70'"

```
0021EE00  push     rdi
0021EE02  sub      rsp, 0x30
0021EE06  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0021EE0F  mov      qword ptr [rsp + 0x40], rbx
0021EE14  mov      qword ptr [rsp + 0x48], rsi
0021EE19  mov      rsi, rcx
0021EE1C  mov      rdi, qword ptr [rcx + 8]
0021EE20  mov      rbx, qword ptr [rcx]
0021EE23  cmp      rbx, rdi
0021EE26  jae      0x21ee47  ; -> 0021EE47
0021EE28  nop      dword ptr [rax + rax]
0021EE30  mov      rax, qword ptr [rbx]
0021EE33  xor      edx, edx
0021EE35  mov      rcx, rbx
0021EE38  call     qword ptr [rax]
0021EE3A  nop      
0021EE3B  add      rbx, 0x218
0021EE42  cmp      rbx, rdi
0021EE45  jb       0x21ee30  ; -> 0021EE30
0021EE47  mov      r10, qword ptr [rsi]
0021EE4A  test     r10, r10
0021EE4D  je       0x21ee87  ; -> 0021EE87
0021EE4F  lea      rcx, [rsi + 0x18]
0021EE53  mov      r9, qword ptr [rcx]
0021EE56  mov      r8, qword ptr [rsi + 0x10]
0021EE5A  sub      r8, r10
0021EE5D  movabs   rax, 0x7a44c6afc2dd9ca9
0021EE67  imul     r8
0021EE6A  sar      rdx, 8
0021EE6E  mov      rax, rdx
0021EE71  shr      rax, 0x3f
0021EE75  add      rdx, rax
0021EE78  imul     r8, rdx, 0x218
0021EE7F  mov      rdx, r10
0021EE82  call     qword ptr [r9 + 0x18]
0021EE86  nop      
0021EE87  mov      rbx, qword ptr [rsp + 0x40]
0021EE8C  mov      rsi, qword ptr [rsp + 0x48]
0021EE91  add      rsp, 0x30
0021EE95  pop      rdi
0021EE96  ret      
```

## 005AD1B0 (124 B, extent 005AD1B0-005AD22C)

Entered from (direct sites whose caller this page cites): `006D03D0` + 0x31 (call; `006D03D0` is cited on this page)
Other direct sites: `005A4E90` + 0x26 (call); `005C5760` + 0x26 (call); `006D50B0` + 0x26 (call)

Host context: "ear it calls '006D2D20(old qword, dword [rcx] AND 0x7FFFFFFF)'; stores 'n' to dword '[rcx]' and 'p' to qword '[rcx+8]'; returns 'rcx' | '006D0362', '006D0373', '006D0389', '006D03A8', '006D03BC' | | '006D03D0' | 115 B | assigns 'rdx' to 'rcx' and returns 'rcx': qword '+0', dwords '+8' and '+0xC'; for the pair (dword '+0x10', qword '+0x18') it takes 'p' = '005AD1B0(source dword AND 0x7FFFFFFF, source qword)', calls '00584730(old qword)' "

```
005AD1B0  mov      qword ptr [rsp + 0x10], rbx
005AD1B5  push     rsi
005AD1B6  sub      rsp, 0x20
005AD1BA  mov      esi, ecx
005AD1BC  mov      rbx, rdx
005AD1BF  test     ecx, ecx
005AD1C1  je       0x5ad21f  ; -> 005AD21F
005AD1C3  mov      qword ptr [rsp + 0x30], rdi
005AD1C8  lea      rcx, [rsi*8]
005AD1D0  mov      edx, 4
005AD1D5  mov      edi, esi
005AD1D7  call     0x17d260  ; -> 0017D260 fn
005AD1DC  mov      r8, rax
005AD1DF  test     rax, rax
005AD1E2  je       0x5ad20f  ; -> 005AD20F
005AD1E4  mov      rcx, rax
005AD1E7  test     esi, esi
005AD1E9  je       0x5ad20f  ; -> 005AD20F
005AD1EB  nop      dword ptr [rax + rax]
005AD1F0  mov      rdx, rcx
005AD1F3  add      rcx, 8
005AD1F7  test     rdx, rdx
005AD1FA  je       0x5ad206  ; -> 005AD206
005AD1FC  mov      rax, qword ptr [rbx]
005AD1FF  add      rbx, 8
005AD203  mov      qword ptr [rdx], rax
005AD206  sub      rdi, 1
005AD20A  jne      0x5ad1f0  ; -> 005AD1F0
005AD20C  mov      rax, r8
005AD20F  mov      rdi, qword ptr [rsp + 0x30]
005AD214  mov      rbx, qword ptr [rsp + 0x38]
005AD219  add      rsp, 0x20
005AD21D  pop      rsi
005AD21E  ret      
005AD21F  xor      eax, eax
005AD221  mov      rbx, qword ptr [rsp + 0x38]
005AD226  add      rsp, 0x20
005AD22A  pop      rsi
005AD22B  ret      
```

## 005D8E40 (103 B, extent 005D8E40-005D8EA7)

Entered from (direct sites whose caller this page cites): `0064A000` + 0x66 (call; `0064A000` is cited on this page)
Other direct sites: `00653E80` + 0x5A (call); `00653E80` + 0xEB (call); `00653E80` + 0x17C (call); `00653E80` + 0x20D (call); `00654470` + 0x70 (call); `00654610` + 0x4E (call); `00654610` + 0xE4 (call); `00654610` + 0x184 (call); `006560E0` + 0x4E (call)

Host context: "' and 'm_marchStepFactor' by '00632960(02D37AE0, 02D364A0, 006301F0(), name, 0x54, 0, 0, 0)'; then tail-jumps to '00639450(02D364A0)' | '006496BB', '006496DF', '0064972E', '0064979D', '006497CC' | | '0064A000' | 219 B | with 'st' = the seventh argument, or a stack dword when it is null, stores 0 to dword '[st]'; returns 0 when 'o' = '0063A990(rcx, 1, 02CBB900, 0)' or 'b' = '005D8E40(rcx, o)' is null; otherwise stores 'r' = '00650490(b, "

```
005D8E40  push     rdi
005D8E42  sub      rsp, 0x30
005D8E46  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
005D8E4F  mov      qword ptr [rsp + 0x40], rbx
005D8E54  mov      rdi, rdx
005D8E57  xor      r9d, r9d
005D8E5A  lea      r8, [rip + 0x26de83f]  ; -> 02CB76A0
005D8E61  lea      edx, [r9 + 1]
005D8E65  call     0x6394e0  ; -> 006394E0 fn
005D8E6A  test     rax, rax
005D8E6D  jne      0x5d8e76  ; -> 005D8E76
005D8E6F  mov      qword ptr [rsp + 0x50], rax
005D8E74  jmp      0x5d8e84  ; -> 005D8E84
005D8E76  mov      rbx, qword ptr [rax + 0x60]
005D8E7A  mov      qword ptr [rsp + 0x50], rbx
005D8E7F  test     rbx, rbx
005D8E82  jne      0x5d8e88  ; -> 005D8E88
005D8E84  xor      eax, eax
005D8E86  jmp      0x5d8e9c  ; -> 005D8E9C
005D8E88  mov      qword ptr [rsp + 0x58], rbx
005D8E8D  mov      rdx, rdi
005D8E90  mov      rcx, rbx
005D8E93  call     0x615c90  ; -> 00615C90 fn
005D8E98  nop      
005D8E99  mov      rax, rbx
005D8E9C  mov      rbx, qword ptr [rsp + 0x40]
005D8EA1  add      rsp, 0x30
005D8EA5  pop      rdi
005D8EA6  ret      
```

## 005E2E00 (148 B, extent 005E2E00-005E2E94)

Entered from (direct sites whose caller this page cites): `00663720` + 0x2C (call; `00663720` is cited on this page); `00663720` + 0xA4 (call; `00663720` is cited on this page)
Other direct sites: `00607000` + 0x26 (call)

Host context: "bytes '+0xC', '+0xD' and '+0xE', dword '+0x10'; '006634B0(rcx+0x18, rdx+0x18)'; dwords '+0x68', '+0x6C' and '+0x70' and qword '+0x78' | '006636BF', '006636D4', '006636F3', '006636FB', '00663713' | | '00663720' | 381 B | assigns 'rdx' to 'rcx' and returns 'rcx': '00663370(rcx, rdx)'; for the pairs (dword '+0x10', qword '+0x18') and (dword '+0x30', qword '+0x38') with 'p' = '005E2E00(source dword AND 0x7FFFFFFF, source qword)', (dword '+0" / "bytes '+0xC', '+0xD' and '+0xE', dword '+0x10'; '006634B0(rcx+0x18, rdx+0x18)'; dwords '+0x68', '+0x6C' and '+0x70' and qword '+0x78' | '006636BF', '006636D4', '006636F3', '006636FB', '00663713' | | '00663720' | 381 B | assigns 'rdx' to 'rcx' and returns 'rcx': '00663370(rcx, rdx)'; for the pairs (dword '+0x10', qword '+0x18') and (dword '+0x30', qword '+0x38') with 'p' = '005E2E00(source dword AND 0x7FFFFFFF, source qword)', (dword '+0"

```
005E2E00  mov      qword ptr [rsp + 0x10], rsi
005E2E05  push     rdi
005E2E06  sub      rsp, 0x20
005E2E0A  mov      edi, ecx
005E2E0C  mov      rsi, rdx
005E2E0F  test     ecx, ecx
005E2E11  je       0x5e2e87  ; -> 005E2E87
005E2E13  mov      ecx, edi
005E2E15  mov      qword ptr [rsp + 0x30], rbx
005E2E1A  shl      rcx, 6
005E2E1E  mov      edx, 4
005E2E23  mov      ebx, edi
005E2E25  call     0x17d260  ; -> 0017D260 fn
005E2E2A  mov      r8, rax
005E2E2D  test     rax, rax
005E2E30  je       0x5e2e77  ; -> 005E2E77
005E2E32  test     edi, edi
005E2E34  je       0x5e2e77  ; -> 005E2E77
005E2E36  lea      rdx, [rsi + 0x20]
005E2E3A  nop      word ptr [rax + rax]
005E2E40  mov      rcx, rax
005E2E43  add      rax, 0x40
005E2E47  test     rcx, rcx
005E2E4A  je       0x5e2e6e  ; -> 005E2E6E
005E2E4C  movups   xmm0, xmmword ptr [rdx - 0x20]
005E2E50  movups   xmmword ptr [rcx], xmm0
005E2E53  movups   xmm0, xmmword ptr [rdx - 0x10]
005E2E57  movups   xmmword ptr [rcx + 0x10], xmm0
005E2E5B  movups   xmm0, xmmword ptr [rdx]
005E2E5E  movups   xmmword ptr [rcx + 0x20], xmm0
005E2E62  movups   xmm0, xmmword ptr [rdx + 0x10]
005E2E66  add      rdx, 0x40
005E2E6A  movups   xmmword ptr [rcx + 0x30], xmm0
005E2E6E  sub      rbx, 1
005E2E72  jne      0x5e2e40  ; -> 005E2E40
005E2E74  mov      rax, r8
005E2E77  mov      rbx, qword ptr [rsp + 0x30]
005E2E7C  mov      rsi, qword ptr [rsp + 0x38]
005E2E81  add      rsp, 0x20
005E2E85  pop      rdi
005E2E86  ret      
005E2E87  xor      eax, eax
005E2E89  mov      rsi, qword ptr [rsp + 0x38]
005E2E8E  add      rsp, 0x20
005E2E92  pop      rdi
005E2E93  ret      
```

## 005F0470 (173 B, extent 005F0470-005F051D)

Entered from (direct sites whose caller this page cites): `005DDC60` + 0x86 (call; `005DDC60` is cited on this page); `005DE7A0` + 0x6A (call; `005DE7A0` is cited on this page); `0060CAB0` + 0x6B (call; `0060CAB0` is cited on this page)
Other direct sites: `005DCFA0` + 0x27 (call); `00600650` + 0x27 (call); `0060F0C0` + 0x4C (call)

Host context: "f 'rcx' and returns 'rcx' | '005DC8B2', '005DC8BD', '005DC8C1', '005DC8C4', '005DC8C8' | | '005DCDA0' | 135 B | when bit '0x80000000' of dword '[rcx]' is clear and qword '[rcx+8]' is non-null, calls '005DDC60' on each of the dword AND 0x7FFFFFFF 0x50-byte elements there and then '00584730' on the buffer; on every path dword '[rcx]' and qword '[rcx+8]' end zeroed | '005DCDCC', '005DCDE7', '005DCDFA', '005DCE02', '005DCE0C' | | '005DCE30'" / "ear it calls '005F0410(old qword, dword [rcx] AND 0x7FFFFFFF)'; stores 'n' to dword '[rcx]' and 'p' to qword '[rcx+8]'; returns 'rcx' | '005DE732', '005DE746', '005DE75C', '005DE77B', '005DE78F' | | '005DE7A0' | 141 B | with 'n' = dword '[rdx]' AND 0x7FFFFFFF takes 'p' = 0 when 'n' is 0, else '0017D260(n*0x30, 8)' filled by '005D8930(p, qword [rdx+8], n)' when non-null; when the old qword '[rcx+8]' differs from 'p' and bit '0x80000000' "

```
005F0470  test     rcx, rcx
005F0473  je       0x5f051c  ; -> 005F051C
005F0479  push     rdi
005F047A  sub      rsp, 0x30
005F047E  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
005F0487  mov      qword ptr [rsp + 0x40], rbx
005F048C  mov      qword ptr [rsp + 0x48], rsi
005F0491  mov      rsi, rcx
005F0494  test     edx, edx
005F0496  je       0x5f0505  ; -> 005F0505
005F0498  lea      rbx, [rcx + 0x10]
005F049C  mov      edi, edx
005F049E  nop      
005F04A0  mov      rcx, qword ptr [rbx + 8]
005F04A4  test     rcx, rcx
005F04A7  je       0x5f04b7  ; -> 005F04B7
005F04A9  mov      eax, ecx
005F04AB  not      al
005F04AD  test     al, 1
005F04AF  je       0x5f04b7  ; -> 005F04B7
005F04B1  call     0x584730  ; -> 00584730 fn
005F04B6  nop      
005F04B7  mov      rcx, qword ptr [rbx]
005F04BA  test     rcx, rcx
005F04BD  je       0x5f04cd  ; -> 005F04CD
005F04BF  mov      eax, ecx
005F04C1  not      al
005F04C3  test     al, 1
005F04C5  je       0x5f04cd  ; -> 005F04CD
005F04C7  call     0x584730  ; -> 00584730 fn
005F04CC  nop      
005F04CD  mov      rcx, qword ptr [rbx - 8]
005F04D1  test     rcx, rcx
005F04D4  je       0x5f04e4  ; -> 005F04E4
005F04D6  mov      eax, ecx
005F04D8  not      al
005F04DA  test     al, 1
005F04DC  je       0x5f04e4  ; -> 005F04E4
005F04DE  call     0x584730  ; -> 00584730 fn
005F04E3  nop      
005F04E4  mov      rcx, qword ptr [rbx - 0x10]
005F04E8  test     rcx, rcx
005F04EB  je       0x5f04fb  ; -> 005F04FB
005F04ED  mov      eax, ecx
005F04EF  not      al
005F04F1  test     al, 1
005F04F3  je       0x5f04fb  ; -> 005F04FB
005F04F5  call     0x584730  ; -> 00584730 fn
005F04FA  nop      
005F04FB  add      rbx, 0x30
005F04FF  sub      rdi, 1
005F0503  jne      0x5f04a0  ; -> 005F04A0
005F0505  mov      rcx, rsi
005F0508  call     0x584730  ; -> 00584730 fn
005F050D  mov      rbx, qword ptr [rsp + 0x40]
005F0512  mov      rsi, qword ptr [rsp + 0x48]
005F0517  add      rsp, 0x30
005F051B  pop      rdi
005F051C  ret      
```

## 0060C340 (162 B, extent 0060C340-0060C3E2)

Entered from (direct sites whose caller this page cites): `005C8850` + 0x1D (call; `005C8850` is cited on this page)
Other direct sites: `0060EDA0` + 0x0 (jmp)

Host context: ", is non-null and bit '0x80000000' of dword '[rcx]' is clear, and stores 'p' to qword '[rcx+8]' and 'edx' to dword '[rcx]'; returns 0 | '005C87E4', '005C87EA', '005C87F9', '005C8827', '005C8830' | | '005C8850' | 164 B | returns 'r' = '0060C340(rcx, dword 02CACF18)' when it is non-zero; otherwise, with 'n' = 'edx'*'r8d', when 'n' differs from dword '[rcx+0x10]' it takes 'p' = 0 for 'n' = 0 or '0017D260(n*2, 2)' (returns 0xD when that is "

```
0060C340  mov      qword ptr [rsp + 0x10], rbx
0060C345  mov      qword ptr [rsp + 0x18], rbp
0060C34A  mov      qword ptr [rsp + 0x20], rsi
0060C34F  push     r14
0060C351  sub      rsp, 0x20
0060C355  mov      rsi, rcx
0060C358  mov      ebx, edx
0060C35A  cmp      edx, dword ptr [rcx]
0060C35C  je       0x60c3bf  ; -> 0060C3BF
0060C35E  xor      ebp, ebp
0060C360  test     edx, edx
0060C362  je       0x60c3d7  ; -> 0060C3D7
0060C364  mov      r14d, ebx
0060C367  lea      edx, [rbp + 8]
0060C36A  shl      r14, 3
0060C36E  mov      rcx, r14
0060C371  call     0x17d260  ; -> 0017D260 fn
0060C376  mov      rbp, rax
0060C379  test     rax, rax
0060C37C  je       0x60c3d7  ; -> 0060C3D7
0060C37E  test     ebx, ebx
0060C380  je       0x60c39b  ; -> 0060C39B
0060C382  mov      qword ptr [rsp + 0x30], rdi
0060C387  mov      rdi, rax
0060C38A  shr      r14, 3
0060C38E  xor      eax, eax
0060C390  mov      rcx, r14
0060C393  rep stosq qword ptr [rdi], rax
0060C396  mov      rdi, qword ptr [rsp + 0x30]
0060C39B  mov      rcx, qword ptr [rsi + 8]
0060C39F  cmp      rcx, rbp
0060C3A2  je       0x60c3b9  ; -> 0060C3B9
0060C3A4  mov      eax, dword ptr [rsi]
0060C3A6  shr      eax, 0x1f
0060C3A9  not      al
0060C3AB  test     al, 1
0060C3AD  je       0x60c3b9  ; -> 0060C3B9
0060C3AF  test     rcx, rcx
0060C3B2  je       0x60c3b9  ; -> 0060C3B9
0060C3B4  call     0x584730  ; -> 00584730 fn
0060C3B9  mov      qword ptr [rsi + 8], rbp
0060C3BD  mov      dword ptr [rsi], ebx
0060C3BF  xor      eax, eax
0060C3C1  mov      rbx, qword ptr [rsp + 0x38]
0060C3C6  mov      rbp, qword ptr [rsp + 0x40]
0060C3CB  mov      rsi, qword ptr [rsp + 0x48]
0060C3D0  add      rsp, 0x20
0060C3D4  pop      r14
0060C3D6  ret      
0060C3D7  test     ebx, ebx
0060C3D9  je       0x60c39b  ; -> 0060C39B
0060C3DB  mov      eax, 0xd
0060C3E0  jmp      0x60c3c1  ; -> 0060C3C1
```

## 00619070 (104 B, extent 00619070-006190D8)

Entered from (direct sites whose caller this page cites): `00616BB0` + 0x31 (call; `00616BB0` is cited on this page); `00616D80` + 0x68 (call; `00616D80` is cited on this page); `00627C60` + 0x6B (call; `00627C60` is cited on this page)
Other direct sites: `006110B0` + 0x34 (call); `00612DA0` + 0x27 (call); `00621F40` + 0x27 (call); `0062A7F0` + 0x4C (call)

Host context: " it calls '00584730(qword)' when bit '0x80000000' of the dword is clear and the qword is non-null, and zeroes both fields of the pair | '00616B61', '00616B6C', '00616B74', '00616B90', '00616B96' | | '00616BB0' | 80 B | calls '0062BAB0(rcx)'; with 'd' = dword '[rcx+0x78]', when bit '0x80000000' of 'd' is clear calls '00619070(qword [rcx+0x80], d AND 0x7FFFFFFF)'; stores 0 to qword '[rcx+0x80]' and dword '[rcx+0x78]' and tail-jumps to '00" / "0(qword [rcx+0x80], d AND 0x7FFFFFFF)'; stores 0 to qword '[rcx+0x80]' and dword '[rcx+0x78]' and tail-jumps to '00616B40' with 'rcx' | '00616BC2', '00616BD4', '00616BE1', '00616BE9', '00616BFB' | | '00616D80' | 139 B | with 'n' = dword '[rdx]' AND 0x7FFFFFFF takes 'p' = 0 when 'n' is 0, else '0017D260(n*0x20, 8)' filled by '00613690(p, qword [rdx+8], n)' when non-null; when the old qword '[rcx+8]' differs from 'p' and bit '0x80000000' "

```
00619070  test     rcx, rcx
00619073  je       0x6190d7  ; -> 006190D7
00619075  push     rdi
00619076  sub      rsp, 0x30
0061907A  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
00619083  mov      qword ptr [rsp + 0x40], rbx
00619088  mov      qword ptr [rsp + 0x48], rsi
0061908D  mov      rsi, rcx
00619090  test     edx, edx
00619092  je       0x6190c0  ; -> 006190C0
00619094  mov      rbx, rcx
00619097  mov      edi, edx
00619099  nop      dword ptr [rax]
006190A0  mov      rcx, qword ptr [rbx]
006190A3  test     rcx, rcx
006190A6  je       0x6190b6  ; -> 006190B6
006190A8  mov      eax, ecx
006190AA  not      al
006190AC  test     al, 1
006190AE  je       0x6190b6  ; -> 006190B6
006190B0  call     0x584730  ; -> 00584730 fn
006190B5  nop      
006190B6  add      rbx, 0x20
006190BA  sub      rdi, 1
006190BE  jne      0x6190a0  ; -> 006190A0
006190C0  mov      rcx, rsi
006190C3  call     0x584730  ; -> 00584730 fn
006190C8  mov      rbx, qword ptr [rsp + 0x40]
006190CD  mov      rsi, qword ptr [rsp + 0x48]
006190D2  add      rsp, 0x30
006190D6  pop      rdi
006190D7  ret      
```

## 0063DCA0 (131 B, extent 0063DCA0-0063DD23)

Entered from (direct sites whose caller this page cites): `00633880` + 0x5E (call; `00633880` is cited on this page); `0063D9C0` + 0x6B (call; `0063D9C0` is cited on this page)
Other direct sites: `0063DE10` + 0xB3 (call)

Host context: "k (qword '+8'), calling '0063CE80(&record, node - 8)' for each node until it reaches the sentinel, a null node or a node at address 8 | '006310EF', '006310F5', '0063110D', '00631148', '00631164' | | '00633880' | 118 B | with 'n' = dword '[rdx]' AND 0x7FFFFFFF and its elements at qword '[rdx+8]' ('n' above 1), 'rdx+8' ('n' = 1) or 0, takes 'x' = '00639650(rcx, n, elements)'; then, with 'c' = dword '[rcx]' AND 0x7FFFFFFF and 'e' = 'rcx''s" / "th non-null it tail-jumps to '00684080(rdx, r8 + that, rcx)'; otherwise it calls '0080F420(rdx, 1)' and tail-jumps to '00810620(rdx)' | '0063D3C9', '0063D3CE', '0063D3E5', '0063D3F2', '0063D3FF' | | '0063D9C0' | 135 B | returns 0 at once when 'edx' equals dword '[rcx]'; with 'b' = qword '[rcx+8]' when the count (dword AND 0x7FFFFFFF) is above 1, 'rcx+8' when it is 1 and 0 when it is 0, 'p' = '006396C0(rcx, edx, b, min(edx, count))'; a n"

```
0063DCA0  push     rdi
0063DCA2  sub      rsp, 0x30
0063DCA6  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0063DCAF  mov      qword ptr [rsp + 0x40], rbx
0063DCB4  mov      qword ptr [rsp + 0x48], rbp
0063DCB9  mov      qword ptr [rsp + 0x50], rsi
0063DCBE  mov      ebp, r8d
0063DCC1  mov      rsi, rdx
0063DCC4  mov      rbx, rcx
0063DCC7  lea      rdi, [rcx + 8]
0063DCCB  cmp      r9, rdx
0063DCCE  je       0x63dd04  ; -> 0063DD04
0063DCD0  cmp      r9, rdi
0063DCD3  jne      0x63dced  ; -> 0063DCED
0063DCD5  mov      rcx, qword ptr [r9]
0063DCD8  test     rcx, rcx
0063DCDB  je       0x63dceb  ; -> 0063DCEB
0063DCDD  mov      eax, ecx
0063DCDF  not      al
0063DCE1  test     al, 1
0063DCE3  je       0x63dceb  ; -> 0063DCEB
0063DCE5  call     0x584730  ; -> 00584730 fn
0063DCEA  nop      
0063DCEB  jmp      0x63dd04  ; -> 0063DD04
0063DCED  mov      eax, dword ptr [rcx]
0063DCEF  shr      eax, 0x1f
0063DCF2  not      al
0063DCF4  test     al, 1
0063DCF6  je       0x63dd04  ; -> 0063DD04
0063DCF8  mov      edx, dword ptr [rsp + 0x60]
0063DCFC  mov      rcx, r9
0063DCFF  call     0x1c2720  ; -> 001C2720 fn
0063DD04  mov      dword ptr [rbx], ebp
0063DD06  cmp      rsi, rdi
0063DD09  je       0x63dd0e  ; -> 0063DD0E
0063DD0B  mov      qword ptr [rdi], rsi
0063DD0E  mov      rbx, qword ptr [rsp + 0x40]
0063DD13  mov      rbp, qword ptr [rsp + 0x48]
0063DD18  mov      rsi, qword ptr [rsp + 0x50]
0063DD1D  add      rsp, 0x30
0063DD21  pop      rdi
0063DD22  ret      
```

## 00664F10 (110 B, extent 00664F10-00664F7E)

Entered from (direct sites whose caller this page cites): `00663940` + 0x2B (call; `00663940` is cited on this page); `00663940` + 0x6D (call; `00663940` is cited on this page)
Other direct sites: `00671270` + 0x26 (call)

Host context: " bit '0x80000000' of the old dword is clear, and stores the count and 'p'; then dwords '+0x18', '+0x1C', '+0x20', '+0x24' and '+0x28' | '006638B9', '006638D1', '006638F4', '00663902', '00663925' | | '00663940' | 194 B | assigns 'rdx' to 'rcx' and returns 'rcx': dword '+0'; for the pairs (dword '+8', qword '+0x10') and (dword '+0x20', qword '+0x28') it takes 'p' = '00664F10(source dword AND 0x7FFFFFFF, source qword)', calls '00584730(old" / " bit '0x80000000' of the old dword is clear, and stores the count and 'p'; then dwords '+0x18', '+0x1C', '+0x20', '+0x24' and '+0x28' | '006638B9', '006638D1', '006638F4', '00663902', '00663925' | | '00663940' | 194 B | assigns 'rdx' to 'rcx' and returns 'rcx': dword '+0'; for the pairs (dword '+8', qword '+0x10') and (dword '+0x20', qword '+0x28') it takes 'p' = '00664F10(source dword AND 0x7FFFFFFF, source qword)', calls '00584730(old"

```
00664F10  mov      qword ptr [rsp + 0x10], rbx
00664F15  push     rsi
00664F16  sub      rsp, 0x20
00664F1A  mov      esi, ecx
00664F1C  mov      rbx, rdx
00664F1F  test     ecx, ecx
00664F21  je       0x664f71  ; -> 00664F71
00664F23  mov      qword ptr [rsp + 0x30], rdi
00664F28  mov      edx, 4
00664F2D  mov      ecx, esi
00664F2F  mov      edi, esi
00664F31  call     0x17d260  ; -> 0017D260 fn
00664F36  mov      r8, rax
00664F39  test     rax, rax
00664F3C  je       0x664f61  ; -> 00664F61
00664F3E  mov      rcx, rax
00664F41  test     esi, esi
00664F43  je       0x664f61  ; -> 00664F61
00664F45  mov      rdx, rcx
00664F48  inc      rcx
00664F4B  test     rdx, rdx
00664F4E  je       0x664f58  ; -> 00664F58
00664F50  movzx    eax, byte ptr [rbx]
00664F53  inc      rbx
00664F56  mov      byte ptr [rdx], al
00664F58  sub      rdi, 1
00664F5C  jne      0x664f45  ; -> 00664F45
00664F5E  mov      rax, r8
00664F61  mov      rdi, qword ptr [rsp + 0x30]
00664F66  mov      rbx, qword ptr [rsp + 0x38]
00664F6B  add      rsp, 0x20
00664F6F  pop      rsi
00664F70  ret      
00664F71  xor      eax, eax
00664F73  mov      rbx, qword ptr [rsp + 0x38]
00664F78  add      rsp, 0x20
00664F7C  pop      rsi
00664F7D  ret      
```

## 00665190 (144 B, extent 00665190-00665220)

Entered from (direct sites whose caller this page cites): `006617A0` + 0x77 (call; `006617A0` is cited on this page); `00663560` + 0x31 (call; `00663560` is cited on this page); `006635F0` + 0x31 (call; `006635F0` is cited on this page); `006BBD30` + 0x2F (call; `006BBD30` is cited on this page)
Other direct sites: `00671500` + 0x26 (call)

Host context: "erior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*  | function | size | what the body does | interior anchors | |---|---|---|---| | '006617A0' | 250 B | copy-constructs 'r8d' 0x88-byte elements from 'rdx' into 'rcx' (nothing when 'r8d' is 0; a null destination element is skipped without advancing the source): dwords '+0'/'+4'; dword '+8' = 0, then 'p' = '00665190(source " / " bit '0x80000000' of that dword is clear; stores 'n' to dword '[rcx]' and 'p' to qword '[rcx+8]' unless 'p' is 'rcx+8'; returns 'rcx' | '006634CE', '006634ED', '00663514', '00663530', '0066353F' | | '00663560' | 140 B | assigns 'rdx' to 'rcx' and returns 'rcx': dwords '+0'/'+4'; for the pair (dword '+8', qword '+0x10') it takes 'p' = '00665190(source dword AND 0x7FFFFFFF, source qword)', calls '00584730(old qword)' when the old qword di"

```
00665190  mov      qword ptr [rsp + 0x10], rsi
00665195  push     rdi
00665196  sub      rsp, 0x20
0066519A  mov      edi, ecx
0066519C  mov      rsi, rdx
0066519F  test     ecx, ecx
006651A1  je       0x665213  ; -> 00665213
006651A3  lea      rcx, [rdi + rdi*2]
006651A7  mov      qword ptr [rsp + 0x30], rbx
006651AC  shl      rcx, 3
006651B0  mov      edx, 8
006651B5  mov      ebx, edi
006651B7  call     0x17d260  ; -> 0017D260 fn
006651BC  mov      r9, rax
006651BF  test     rax, rax
006651C2  je       0x665203  ; -> 00665203
006651C4  mov      r8, rax
006651C7  test     edi, edi
006651C9  je       0x665203  ; -> 00665203
006651CB  lea      rdx, [rsi + 0x10]
006651CF  nop      
006651D0  mov      rcx, r8
006651D3  add      r8, 0x18
006651D7  test     rcx, rcx
006651DA  je       0x6651fa  ; -> 006651FA
006651DC  mov      eax, dword ptr [rdx - 0x10]
006651DF  mov      dword ptr [rcx], eax
006651E1  mov      rax, qword ptr [rdx - 8]
006651E5  mov      qword ptr [rcx + 8], rax
006651E9  movzx    eax, byte ptr [rdx]
006651EC  mov      byte ptr [rcx + 0x10], al
006651EF  movzx    eax, byte ptr [rdx + 1]
006651F3  add      rdx, 0x18
006651F7  mov      byte ptr [rcx + 0x11], al
006651FA  sub      rbx, 1
006651FE  jne      0x6651d0  ; -> 006651D0
00665200  mov      rax, r9
00665203  mov      rbx, qword ptr [rsp + 0x30]
00665208  mov      rsi, qword ptr [rsp + 0x38]
0066520D  add      rsp, 0x20
00665211  pop      rdi
00665212  ret      
00665213  xor      eax, eax
00665215  mov      rsi, qword ptr [rsp + 0x38]
0066521A  add      rsp, 0x20
0066521E  pop      rdi
0066521F  ret      
```

## 00693C40 (140 B, extent 00693C40-00693CCC)

Entered from (direct sites whose caller this page cites): `005AA970` + 0x34 (call; `005AA970` is cited on this page); `00692660` + 0x4F (call; `00692660` is cited on this page)
Other direct sites: `005C57D0` + 0x26 (call)

Host context: "18' and '+0x20' of 'rdx' to 'rcx', calls '005AA690(rcx+0x28, rdx+0x28)', '005AA7D0(rcx+0x38, rdx+0x38)' and '005AA3C0(rcx+0x60, rdx+0x60)', copies dword '+0x78' and qwords '+0x80' and '+0x88', calls '005AA970(rcx+0x90, rdx+0x90)' and returns 'rcx' | '005AA73A', '005AA75E', '005AA76B', '005AA778', '005AA7AD' | | '005AA7D0' | 111 B | copies dword '[rdx+8]' to dword '[rcx+8]' and qword '[rdx+0x10]' to qword '[rcx+0x10]'; with 'n' = dword '" / " | calls '00692290(rcx, rdx)', then copies qwords '+0x130'..'+0x148' and dwords '+0x150'..'+0x18C' from 'rdx' to 'rcx'; returns 'rcx' | '00692550', '0069255C', '00692586', '00692593', '0069264C' | | '00692660' | 218 B | copies the 0x30 bytes '+0'..'+0x2F' from 'rdx' to 'rcx'; with 'n' = dword '[rdx+0x30]' AND 0x7FFFFFFF takes 'p' = '00693C40(n, qword [rdx+0x38])', calls '00584730' on the old qword '[rcx+0x38]' when it is not 'p', is non"

```
00693C40  mov      qword ptr [rsp + 0x10], rsi
00693C45  push     rdi
00693C46  sub      rsp, 0x20
00693C4A  mov      esi, ecx
00693C4C  mov      rdi, rdx
00693C4F  test     ecx, ecx
00693C51  je       0x693cbf  ; -> 00693CBF
00693C53  lea      rcx, [rsi + rsi*2]
00693C57  mov      qword ptr [rsp + 0x30], rbx
00693C5C  shl      rcx, 4
00693C60  mov      edx, 8
00693C65  mov      ebx, esi
00693C67  call     0x17d260  ; -> 0017D260 fn
00693C6C  mov      rdx, rax
00693C6F  test     rax, rax
00693C72  je       0x693caf  ; -> 00693CAF
00693C74  mov      rcx, rax
00693C77  test     esi, esi
00693C79  je       0x693caf  ; -> 00693CAF
00693C7B  nop      dword ptr [rax + rax]
00693C80  mov      rax, rcx
00693C83  add      rcx, 0x30
00693C87  test     rax, rax
00693C8A  je       0x693ca6  ; -> 00693CA6
00693C8C  movups   xmm0, xmmword ptr [rdi]
00693C8F  movups   xmmword ptr [rax], xmm0
00693C92  movups   xmm1, xmmword ptr [rdi + 0x10]
00693C96  movups   xmmword ptr [rax + 0x10], xmm1
00693C9A  movups   xmm0, xmmword ptr [rdi + 0x20]
00693C9E  add      rdi, 0x30
00693CA2  movups   xmmword ptr [rax + 0x20], xmm0
00693CA6  sub      rbx, 1
00693CAA  jne      0x693c80  ; -> 00693C80
00693CAC  mov      rax, rdx
00693CAF  mov      rbx, qword ptr [rsp + 0x30]
00693CB4  mov      rsi, qword ptr [rsp + 0x38]
00693CB9  add      rsp, 0x20
00693CBD  pop      rdi
00693CBE  ret      
00693CBF  xor      eax, eax
00693CC1  mov      rsi, qword ptr [rsp + 0x38]
00693CC6  add      rsp, 0x20
00693CCA  pop      rdi
00693CCB  ret      
```

## 006AAA50 (39 B, extent 006AAA50-006AAA77)

Entered from (direct sites whose caller this page cites): `005AC8C0` + 0x53 (call; `005AC8C0` is cited on this page)
Other direct sites: `006A9450` + 0x10 (call); `006ADC20` + 0x38 (call); `006AF910` + 0x45 (call); `006CDD30` + 0x43 (call)

Host context: "ord '[rcx+0x18]' is clear, and stores 'p' and 'n' there; copies qword '+0x28', calls '005AA600(rcx+0x30, rdx+0x30)' and returns 'rcx' | '005AAB2A', '005AAB45', '005AAB68', '005AAB80', '005AAB84' | | '005AC8C0' | 140 B | stores '00D31898' to qword '[rcx]', calls '005A9F10(rcx+0x90)', stores '00D312F0' to qword '[rcx+0x70]', and calls '005AA1D0(rcx+0x38)', '005A98B0(rcx+0x28)' and '006AAA50(rcx+8)'; when bit '0x1' of 'dl' is set it calls "

```
006AAA50  sub      rsp, 0x38
006AAA54  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
006AAA5D  mov      rax, qword ptr [rcx + 8]
006AAA61  test     rax, rax
006AAA64  je       0x6aaa72  ; -> 006AAA72
006AAA66  mov      rdx, rcx
006AAA69  mov      rcx, rax
006AAA6C  call     0x6aca70  ; -> 006ACA70 fn
006AAA71  nop      
006AAA72  add      rsp, 0x38
006AAA76  ret      
```

## 006AADD0 (48 B, extent 006AADD0-006AAE00)

Entered from (direct sites whose caller this page cites): `005B80E0` + 0x9 (call; `005B80E0` is cited on this page); `006AFF00` + 0x9 (call; `006AFF00` is cited on this page)
Other direct sites: `006ADD70` + 0x3 (jmp)

Host context: "' | 26 B | with 'o' = qword '[rdx]', tail-calls 'o''s vtable slot '+8' with ('o', 'rcx') and floats '[rdx+8]' in 'xmm2' and '[rdx+0xC]' in 'xmm3' | '005B80C5', '005B80CB', '005B80D3', '005B80D6' | | '005B80E0' | 188 B | returns 'r' = '006AADD0(rcx)' when it is non-zero; otherwise, for each of the dword '[rcx+0x70]' records 'e' from qword '[rcx+0x58]' - 8 (0 when that qword is null; stride dword '+0x38' of qword '[rcx+0x50]'), calls '005" / "00000' of dword '[rcx]' is clear, it calls '00584730(old)'; it stores 'p' to qword '[rcx+8]' and 'edx' to dword '[rcx]' and returns 0 | '006AF6C4', '006AF6DD', '006AF6EE', '006AF71A', '006AF723' | | '006AFF00' | 103 B | returns '006AADD0(rcx)' when that is non-zero; otherwise, for each of dword '[rcx+0x70]' records from qword '[rcx+0x58]' (stride dword '+0x38' of qword '[rcx+0x50]'), with 'n' = record + 0x18 (0 for a null record) it lin"

```
006AADD0  mov      r9d, dword ptr [rcx + 0x70]
006AADD4  mov      rax, qword ptr [rcx + 0x58]
006AADD8  mov      rdx, qword ptr [rcx + 0x50]
006AADDC  test     r9d, r9d
006AADDF  je       0x6aadfd  ; -> 006AADFD
006AADE1  mov      r8d, dword ptr [rdx + 0x38]
006AADE5  mov      ecx, r9d
006AADE8  nop      dword ptr [rax + rax]
006AADF0  mov      qword ptr [rax + 0x10], rdx
006AADF4  add      rax, r8
006AADF7  sub      rcx, 1
006AADFB  jne      0x6aadf0  ; -> 006AADF0
006AADFD  xor      eax, eax
006AADFF  ret      
```

## 006CD4F0 (132 B, extent 006CD4F0-006CD574)

Entered from (direct sites whose caller this page cites): `006CD390` + 0x10A (call; `006CD390` is cited on this page)
Other direct sites: `00167C50` + 0xB (call)

Host context: "C' after): '006B6820(02E5C270, 'PTriggerType', 0x18, 8, 006CD4C0, 006CD580)', qword '02E5C270' = '00D89F40', and '00808B90(008B7010)' | '006CD29A', '006CD2A9', '006CD2EA', '006CD2F6', '006CD311' | | '006CD390' | 290 B | returns 0 when 'rcx' is null; returns the first entry of the list from qword '02E5C210' (next at qword '+8') whose qword '+0' string matches 'rcx' by '_stricmp'; otherwise it calls '005CDAA0(1, 00D4E5C0, rcx)' ('PNamedSe"

```
006CD4F0  sub      rsp, 8
006CD4F4  mov      r10, qword ptr [rcx]
006CD4F7  mov      r11, rcx
006CD4FA  test     r10, r10
006CD4FD  jne      0x6cd508  ; -> 006CD508
006CD4FF  lea      eax, [r10 + 0x11]
006CD503  add      rsp, 8
006CD507  ret      
006CD508  mov      qword ptr [rsp], rbx
006CD50C  mov      rbx, qword ptr [rip + 0x278ecfd]  ; -> 02E5C210
006CD513  mov      r9, rbx
006CD516  test     rbx, rbx
006CD519  je       0x6cd550  ; -> 006CD550
006CD51B  nop      dword ptr [rax + rax]
006CD520  mov      rax, qword ptr [r9]
006CD523  mov      r8, r10
006CD526  sub      r8, rax
006CD529  nop      dword ptr [rax]
006CD530  movzx    edx, byte ptr [rax]
006CD533  movzx    ecx, byte ptr [rax + r8]
006CD538  sub      edx, ecx
006CD53A  jne      0x6cd543  ; -> 006CD543
006CD53C  inc      rax
006CD53F  test     ecx, ecx
006CD541  jne      0x6cd530  ; -> 006CD530
006CD543  test     edx, edx
006CD545  je       0x6cd566  ; -> 006CD566
006CD547  mov      r9, qword ptr [r9 + 8]
006CD54B  test     r9, r9
006CD54E  jne      0x6cd520  ; -> 006CD520
006CD550  mov      qword ptr [r11 + 8], rbx
006CD554  xor      eax, eax
006CD556  mov      rbx, qword ptr [rsp]
006CD55A  mov      qword ptr [rip + 0x278ecaf], r11  ; -> 02E5C210
006CD561  add      rsp, 8
006CD565  ret      
006CD566  mov      eax, 0x12
006CD56B  mov      rbx, qword ptr [rsp]
006CD56F  add      rsp, 8
006CD573  ret      
```
