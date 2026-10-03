# F-interior pack: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md`

Generated 2026-10-03 03:15 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/the-fifteen-modules-registered-before-main.json`.

Functions: 11. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 4760745aa	SWE2-EC7: Phyre module selectors under the uniform closure-source rule - 227 bodies admitted to 8 mo; 89d1a685a	SWE2-EC7: accounting state no longer feeds five family selectors (JsonBox, ImGui, mkvparser, MSVC ru; inbox mentions: FABLE.md, SWE2-AUDIT-SPEC.md, SWE2-EC7.md, SWE2-FRONTIER.md). OPUS read these before packing.

## 005AD230 (125 B, extent 005AD230-005AD2AD)

Page context: "'rdx' to 'rcx' and returns 'rcx': qword '+0'; for the pairs (dword '+8', qword '+0x10') with 'p' = '006BC4C0(source dword AND 0x7FFFFFFF, source qword)' and (dword '+0x18', qword '+0x20') with 'p' = '005AD230' of the same it calls '00584730(old qword)' when the old qword differs from 'p', is non-null and bit '0x80000000' of the old dword is clear, and stores the count and 'p' | '006C310A', '006C311D', '006C3140', '006C3159', '006C317C' "

```
005AD230  mov      qword ptr [rsp + 0x10], rbx
005AD235  push     rsi
005AD236  sub      rsp, 0x20
005AD23A  mov      esi, ecx
005AD23C  mov      rbx, rdx
005AD23F  test     ecx, ecx
005AD241  je       0x5ad2a0  ; -> 005AD2A0
005AD243  mov      ecx, esi
005AD245  mov      qword ptr [rsp + 0x30], rdi
005AD24A  shl      rcx, 4
005AD24E  mov      edx, 0x10
005AD253  mov      edi, esi
005AD255  call     0x17d260  ; -> 0017D260 fn
005AD25A  mov      rdx, rax
005AD25D  test     rax, rax
005AD260  je       0x5ad290  ; -> 005AD290
005AD262  test     esi, esi
005AD264  je       0x5ad290  ; -> 005AD290
005AD266  nop      word ptr [rax + rax]
005AD270  mov      rcx, rax
005AD273  add      rax, 0x10
005AD277  test     rcx, rcx
005AD27A  je       0x5ad287  ; -> 005AD287
005AD27C  movaps   xmm0, xmmword ptr [rbx]
005AD27F  add      rbx, 0x10
005AD283  movdqa   xmmword ptr [rcx], xmm0
005AD287  sub      rdi, 1
005AD28B  jne      0x5ad270  ; -> 005AD270
005AD28D  mov      rax, rdx
005AD290  mov      rdi, qword ptr [rsp + 0x30]
005AD295  mov      rbx, qword ptr [rsp + 0x38]
005AD29A  add      rsp, 0x20
005AD29E  pop      rsi
005AD29F  ret      
005AD2A0  xor      eax, eax
005AD2A2  mov      rbx, qword ptr [rsp + 0x38]
005AD2A7  add      rsp, 0x20
005AD2AB  pop      rsi
005AD2AC  ret      
```

## 005C39B0 (49 B, extent 005C39B0-005C39E1)

Page context: " at qword 'M+0x10' + 0x90 when qword 'M+0x18' is non-null and '005A7A40(qword M+0x10, qword M+0x18)' returns null; after each, unguarded, qwords 'M+0x30'/'M+0x38' = '00D6AD90'/'001B80C0', '00D6ADC0'/'005C39B0' and '00D6ADF0'/'005C4CC0' and qword 'M+0x28' = 'M+0x30'; then tail-jumps to '00639450(02D3A440)' | '00666581', '006665F9', '0066666A', '006666E1', '006667FE' | | '006668B0' | 1503 B | calls '006388C0(02D3A640)'; each once under it"

```
005C39B0  mov      eax, dword ptr [rcx]
005C39B2  btr      eax, 0x1f
005C39B6  mov      r8d, edx
005C39B9  cmp      edx, eax
005C39BB  jae      0x5c39dc  ; -> 005C39DC
005C39BD  cmp      eax, 1
005C39C0  jbe      0x5c39cb  ; -> 005C39CB
005C39C2  mov      rcx, qword ptr [rcx + 8]
005C39C6  mov      rax, qword ptr [rcx + r8*8]
005C39CA  ret      
005C39CB  add      rcx, 8
005C39CF  xor      edx, edx
005C39D1  test     eax, eax
005C39D3  cmove    rcx, rdx
005C39D7  mov      rax, qword ptr [rcx + r8*8]
005C39DB  ret      
005C39DC  xor      edx, edx
005C39DE  mov      eax, edx
005C39E0  ret      
```

## 005C4CC0 (7 B, extent 005C4CC0-005C4CC7)

Page context: "nd dword '02EB7A00' = 0x7FFFFFFF, and registers 'm_els' by '00632A10(02EB7A10, 02EB7860, 02EB6CF0, name, 8, 2, 2, 8)' with qword '02EB7A10' = '01CD6B70' and qwords '02EB7A70'/'02EB7A78'/'02EB7A80' = '005C4CC0'/0/'00673130'; between the last two it calls '006B67D0(02EB79A8, 02EB79D0)' when qword '02EB79D8' holds its own address; it then sets dword '02EB7A68' = 8 and calls '006388C0(02EB7860)' and '00639450(02EB7860)' | '0086E513', '0086E"

```
005C4CC0  mov      eax, dword ptr [rcx]
005C4CC2  btr      eax, 0x1f
005C4CC6  ret      
```

## 0062EB20 (103 B, extent 0062EB20-0062EB87)

Page context: "ossings).  | member | size | role | interior | |---|---:|---|---| | '0062EA20' | 51 B | ctor for the '0xE0' object the root stores at '01F7F5B8' — eh-vector build of 4 × '0x38' records (element ctor '0062EB20', dtor '0062EAE0') through '' 'eh_vector_constructor_iterator' '' '00808FE4' | '0062EA26' | | '00677450' | 27 B | create-once gate for the sync object at '02D3E880': returns '0x16' when the flag byte is already set, else tail-jumps"

```
0062EB20  mov      qword ptr [rsp + 0x10], rbx
0062EB25  push     rdi
0062EB26  sub      rsp, 0x20
0062EB2A  mov      rdi, rcx
0062EB2D  lea      rdx, [rip + 0x2c517c]  ; -> 008F3CB0 [str "EASTL set"]
0062EB34  lea      rcx, [rsp + 0x30]
0062EB39  call     0x1edf00  ; -> 001EDF00 fn
0062EB3E  xor      ecx, ecx
0062EB40  lea      rbx, [rdi + 8]
0062EB44  mov      qword ptr [rbx], rcx
0062EB47  mov      rdx, rax
0062EB4A  mov      qword ptr [rbx + 8], rcx
0062EB4E  mov      qword ptr [rbx + 0x10], rcx
0062EB52  mov      qword ptr [rbx + 0x18], rcx
0062EB56  mov      dword ptr [rdi + 0x28], ecx
0062EB59  lea      rcx, [rdi + 0x30]
0062EB5D  call     0x1edf00  ; -> 001EDF00 fn
0062EB62  mov      qword ptr [rbx], rbx
0062EB65  mov      qword ptr [rdi + 0x10], rbx
0062EB69  mov      rbx, qword ptr [rsp + 0x38]
0062EB6E  mov      qword ptr [rdi + 0x18], 0
0062EB76  mov      byte ptr [rdi + 0x20], 0
0062EB7A  mov      dword ptr [rdi + 0x28], 0
0062EB81  add      rsp, 0x20
0062EB85  pop      rdi
0062EB86  ret      
```

## 00664F80 (122 B, extent 00664F80-00664FFA)

Page context: " '+0x38') with 'p' = '005E2E00(source dword AND 0x7FFFFFFF, source qword)', (dword '+0x20', qword '+0x28') with '00665080', and (dword '+0x50', qword '+0x58') and (dword '+0x70', qword '+0x78') with '00664F80', it calls '00584730(old qword)' when the old qword differs from 'p', is non-null and bit '0x80000000' of the old dword is clear, and stores the count and 'p'; between them '005DE8C0(rcx+0x40, rdx+0x40)' and '00646C00(rcx+0x60, rdx"

```
00664F80  mov      qword ptr [rsp + 0x10], rbx
00664F85  push     rsi
00664F86  sub      rsp, 0x20
00664F8A  mov      esi, ecx
00664F8C  mov      rbx, rdx
00664F8F  test     ecx, ecx
00664F91  je       0x664fed  ; -> 00664FED
00664F93  mov      qword ptr [rsp + 0x30], rdi
00664F98  lea      rcx, [rsi*4]
00664FA0  mov      edx, 4
00664FA5  mov      edi, esi
00664FA7  call     0x17d260  ; -> 0017D260 fn
00664FAC  mov      r8, rax
00664FAF  test     rax, rax
00664FB2  je       0x664fdd  ; -> 00664FDD
00664FB4  mov      rcx, rax
00664FB7  test     esi, esi
00664FB9  je       0x664fdd  ; -> 00664FDD
00664FBB  nop      dword ptr [rax + rax]
00664FC0  mov      rdx, rcx
00664FC3  add      rcx, 4
00664FC7  test     rdx, rdx
00664FCA  je       0x664fd4  ; -> 00664FD4
00664FCC  mov      eax, dword ptr [rbx]
00664FCE  add      rbx, 4
00664FD2  mov      dword ptr [rdx], eax
00664FD4  sub      rdi, 1
00664FD8  jne      0x664fc0  ; -> 00664FC0
00664FDA  mov      rax, r8
00664FDD  mov      rdi, qword ptr [rsp + 0x30]
00664FE2  mov      rbx, qword ptr [rsp + 0x38]
00664FE7  add      rsp, 0x20
00664FEB  pop      rsi
00664FEC  ret      
00664FED  xor      eax, eax
00664FEF  mov      rbx, qword ptr [rsp + 0x38]
00664FF4  add      rsp, 0x20
00664FF8  pop      rsi
00664FF9  ret      
```

## 00665000 (124 B, extent 00665000-0066507C)

Page context: "x' to 'rcx' and returns 'rcx': qword '+8'; for the pairs (dword '+0x10', qword '+0x18') with 'p' = '00665190(source dword AND 0x7FFFFFFF, source qword)' and (dword '+0x20', qword '+0x28') with 'p' = '00665000' of the same it calls '00584730(old qword)' when the old qword differs from 'p', is non-null and bit '0x80000000' of the old dword is clear, and stores the count and 'p'; then dword '+0x30' | '006BBD4B', '006BBD5F', '006BBD82', '00"

```
00665000  mov      qword ptr [rsp + 0x10], rsi
00665005  push     rdi
00665006  sub      rsp, 0x20
0066500A  mov      esi, ecx
0066500C  mov      rdi, rdx
0066500F  test     ecx, ecx
00665011  je       0x66506f  ; -> 0066506F
00665013  mov      ecx, esi
00665015  mov      qword ptr [rsp + 0x30], rbx
0066501A  shl      rcx, 4
0066501E  mov      edx, 4
00665023  mov      ebx, esi
00665025  call     0x17d260  ; -> 0017D260 fn
0066502A  mov      rdx, rax
0066502D  test     rax, rax
00665030  je       0x66505f  ; -> 0066505F
00665032  test     esi, esi
00665034  je       0x66505f  ; -> 0066505F
00665036  nop      word ptr [rax + rax]
00665040  mov      rcx, rax
00665043  add      rax, 0x10
00665047  test     rcx, rcx
0066504A  je       0x665056  ; -> 00665056
0066504C  movups   xmm0, xmmword ptr [rdi]
0066504F  add      rdi, 0x10
00665053  movups   xmmword ptr [rcx], xmm0
00665056  sub      rbx, 1
0066505A  jne      0x665040  ; -> 00665040
0066505C  mov      rax, rdx
0066505F  mov      rbx, qword ptr [rsp + 0x30]
00665064  mov      rsi, qword ptr [rsp + 0x38]
00665069  add      rsp, 0x20
0066506D  pop      rdi
0066506E  ret      
0066506F  xor      eax, eax
00665071  mov      rsi, qword ptr [rsp + 0x38]
00665076  add      rsp, 0x20
0066507A  pop      rdi
0066507B  ret      
```

## 00671250 (29 B, extent 00671250-0067126D)

Page context: "B0, 02E5C710, 00D337A0, 8, 2, 2, 8)' with qword '02E4DEC0' = '00D7BED0' and qwords '02E4DF20'/'02E4DF28'/'02E4DF30' = '005C4CC0'/0/'006A9290'; sets bit '0x40' of dword '02E4DEE8', qword '02E4DF28' = '00671250', dword '02E4DF18' = 8; once each registers 'm_count' ('00632960(02E4DF40, 02E4DDB0, 00630180(), name, 0, 0, 0, 0)') and builds '006B66C0(02E4DFA0, 02CF8570, 00630180(), 0)' with '00D32D50' and dword '02E4DFD0' = 0x7FFFFFFF; calls "

```
00671250  mov      edx, dword ptr [rcx]
00671252  btr      edx, 0x1f
00671256  cmp      edx, 1
00671259  jbe      0x671260  ; -> 00671260
0067125B  mov      rax, qword ptr [rcx + 8]
0067125F  ret      
00671260  lea      rax, [rcx + 8]
00671264  xor      ecx, ecx
00671266  test     edx, edx
00671268  cmove    rax, rcx
0067126C  ret      
```

## 00673130 (87 B, extent 00673130-00673187)

Page context: "B7A00' = 0x7FFFFFFF, and registers 'm_els' by '00632A10(02EB7A10, 02EB7860, 02EB6CF0, name, 8, 2, 2, 8)' with qword '02EB7A10' = '01CD6B70' and qwords '02EB7A70'/'02EB7A78'/'02EB7A80' = '005C4CC0'/0/'00673130'; between the last two it calls '006B67D0(02EB79A8, 02EB79D0)' when qword '02EB79D8' holds its own address; it then sets dword '02EB7A68' = 8 and calls '006388C0(02EB7860)' and '00639450(02EB7860)' | '0086E513', '0086E527', '0086E5"

```
00673130  mov      qword ptr [rsp + 8], rbx
00673135  mov      qword ptr [rsp + 0x10], rsi
0067313A  push     rdi
0067313B  sub      rsp, 0x20
0067313F  mov      ebx, r8d
00673142  mov      rsi, rdx
00673145  mov      rdi, rcx
00673148  test     r8d, r8d
0067314B  js       0x673175  ; -> 00673175
0067314D  mov      rcx, qword ptr [rcx + 8]
00673151  cmp      rcx, rdx
00673154  je       0x67316b  ; -> 0067316B
00673156  mov      eax, dword ptr [rdi]
00673158  shr      eax, 0x1f
0067315B  not      al
0067315D  test     al, 1
0067315F  je       0x67316b  ; -> 0067316B
00673161  test     rcx, rcx
00673164  je       0x67316b  ; -> 0067316B
00673166  call     0x584730  ; -> 00584730 fn
0067316B  bts      ebx, 0x1f
0067316F  mov      qword ptr [rdi + 8], rsi
00673173  mov      dword ptr [rdi], ebx
00673175  mov      rbx, qword ptr [rsp + 0x30]
0067317A  xor      eax, eax
0067317C  mov      rsi, qword ptr [rsp + 0x38]
00673181  add      rsp, 0x20
00673185  pop      rdi
00673186  ret      
```

## 006AE1F0 (124 B, extent 006AE1F0-006AE26C)

Page context: "BBDD7' | | '006BBDF0' | 295 B | assigns 'rdx' to 'rcx' and returns 'rcx': '006BBD30(rcx, rdx)'; then for the pairs (dword '+0x38', qword '+0x40') with '006BC4C0', (dword '+0x48', qword '+0x50') with '006AE1F0', (dword '+0x58', qword '+0x60') with '00664F80' and (dword '+0x68', qword '+0x70') with '006BC540', taking 'p' = that call of (source dword AND 0x7FFFFFFF, source qword), it calls '00584730(old qword)' when the old qword differs f"

```
006AE1F0  mov      qword ptr [rsp + 0x10], rsi
006AE1F5  push     rdi
006AE1F6  sub      rsp, 0x20
006AE1FA  mov      esi, ecx
006AE1FC  mov      rdi, rdx
006AE1FF  test     ecx, ecx
006AE201  je       0x6ae25f  ; -> 006AE25F
006AE203  mov      ecx, esi
006AE205  mov      qword ptr [rsp + 0x30], rbx
006AE20A  shl      rcx, 4
006AE20E  mov      edx, 8
006AE213  mov      ebx, esi
006AE215  call     0x17d260  ; -> 0017D260 fn
006AE21A  mov      rdx, rax
006AE21D  test     rax, rax
006AE220  je       0x6ae24f  ; -> 006AE24F
006AE222  test     esi, esi
006AE224  je       0x6ae24f  ; -> 006AE24F
006AE226  nop      word ptr [rax + rax]
006AE230  mov      rcx, rax
006AE233  add      rax, 0x10
006AE237  test     rcx, rcx
006AE23A  je       0x6ae246  ; -> 006AE246
006AE23C  movups   xmm0, xmmword ptr [rdi]
006AE23F  add      rdi, 0x10
006AE243  movups   xmmword ptr [rcx], xmm0
006AE246  sub      rbx, 1
006AE24A  jne      0x6ae230  ; -> 006AE230
006AE24C  mov      rax, rdx
006AE24F  mov      rbx, qword ptr [rsp + 0x30]
006AE254  mov      rsi, qword ptr [rsp + 0x38]
006AE259  add      rsp, 0x20
006AE25D  pop      rdi
006AE25E  ret      
006AE25F  xor      eax, eax
006AE261  mov      rsi, qword ptr [rsp + 0x38]
006AE266  add      rsp, 0x20
006AE26A  pop      rdi
006AE26B  ret      
```

## 006BC4C0 (124 B, extent 006BC4C0-006BC53C)

Page context: "C961', '0086C967' | | '0086C990' | 148 B | copies 'rdx' into 'rcx' and returns 'rcx': unless 'rcx' and 'rdx' are the same object it calls '001EAD40(rcx+8, qword [rdx+8] with bit 0x1 cleared)'; 'p' = '006BC4C0(n, qword [rdx+0x18])' with 'n' = dword '[rdx+0x10]' AND 0x7FFFFFFF; when the old qword '[rcx+0x18]' differs from 'p', is non-null and bit '0x80000000' of dword '[rcx+0x10]' is clear it calls '00584730(old)'; then stores 'p' to qwor"

```
006BC4C0  mov      qword ptr [rsp + 0x10], rbx
006BC4C5  push     rsi
006BC4C6  sub      rsp, 0x20
006BC4CA  mov      esi, ecx
006BC4CC  mov      rbx, rdx
006BC4CF  test     ecx, ecx
006BC4D1  je       0x6bc52f  ; -> 006BC52F
006BC4D3  mov      qword ptr [rsp + 0x30], rdi
006BC4D8  lea      rcx, [rsi*8]
006BC4E0  mov      edx, 8
006BC4E5  mov      edi, esi
006BC4E7  call     0x17d260  ; -> 0017D260 fn
006BC4EC  mov      r8, rax
006BC4EF  test     rax, rax
006BC4F2  je       0x6bc51f  ; -> 006BC51F
006BC4F4  mov      rcx, rax
006BC4F7  test     esi, esi
006BC4F9  je       0x6bc51f  ; -> 006BC51F
006BC4FB  nop      dword ptr [rax + rax]
006BC500  mov      rdx, rcx
006BC503  add      rcx, 8
006BC507  test     rdx, rdx
006BC50A  je       0x6bc516  ; -> 006BC516
006BC50C  mov      rax, qword ptr [rbx]
006BC50F  add      rbx, 8
006BC513  mov      qword ptr [rdx], rax
006BC516  sub      rdi, 1
006BC51A  jne      0x6bc500  ; -> 006BC500
006BC51C  mov      rax, r8
006BC51F  mov      rdi, qword ptr [rsp + 0x30]
006BC524  mov      rbx, qword ptr [rsp + 0x38]
006BC529  add      rsp, 0x20
006BC52D  pop      rsi
006BC52E  ret      
006BC52F  xor      eax, eax
006BC531  mov      rbx, qword ptr [rsp + 0x38]
006BC536  add      rsp, 0x20
006BC53A  pop      rsi
006BC53B  ret      
```

## 006BC540 (134 B, extent 006BC540-006BC5C6)

Page context: "n for the pairs (dword '+0x38', qword '+0x40') with '006BC4C0', (dword '+0x48', qword '+0x50') with '006AE1F0', (dword '+0x58', qword '+0x60') with '00664F80' and (dword '+0x68', qword '+0x70') with '006BC540', taking 'p' = that call of (source dword AND 0x7FFFFFFF, source qword), it calls '00584730(old qword)' when the old qword differs from 'p', is non-null and bit '0x80000000' of the old dword is clear, and stores the count and 'p' |"

```
006BC540  mov      qword ptr [rsp + 0x10], rsi
006BC545  push     rdi
006BC546  sub      rsp, 0x20
006BC54A  mov      esi, ecx
006BC54C  mov      rdi, rdx
006BC54F  test     ecx, ecx
006BC551  je       0x6bc5b9  ; -> 006BC5B9
006BC553  lea      rcx, [rsi + rsi*2]
006BC557  mov      qword ptr [rsp + 0x30], rbx
006BC55C  shl      rcx, 3
006BC560  mov      edx, 8
006BC565  mov      ebx, esi
006BC567  call     0x17d260  ; -> 0017D260 fn
006BC56C  mov      rdx, rax
006BC56F  test     rax, rax
006BC572  je       0x6bc5a9  ; -> 006BC5A9
006BC574  mov      rcx, rax
006BC577  test     esi, esi
006BC579  je       0x6bc5a9  ; -> 006BC5A9
006BC57B  nop      dword ptr [rax + rax]
006BC580  mov      rax, rcx
006BC583  add      rcx, 0x18
006BC587  test     rax, rax
006BC58A  je       0x6bc5a0  ; -> 006BC5A0
006BC58C  movups   xmm0, xmmword ptr [rdi]
006BC58F  movups   xmmword ptr [rax], xmm0
006BC592  movsd    xmm1, qword ptr [rdi + 0x10]
006BC597  add      rdi, 0x18
006BC59B  movsd    qword ptr [rax + 0x10], xmm1
006BC5A0  sub      rbx, 1
006BC5A4  jne      0x6bc580  ; -> 006BC580
006BC5A6  mov      rax, rdx
006BC5A9  mov      rbx, qword ptr [rsp + 0x30]
006BC5AE  mov      rsi, qword ptr [rsp + 0x38]
006BC5B3  add      rsp, 0x20
006BC5B7  pop      rdi
006BC5B8  ret      
006BC5B9  xor      eax, eax
006BC5BB  mov      rsi, qword ptr [rsp + 0x38]
006BC5C0  add      rsp, 0x20
006BC5C4  pop      rdi
006BC5C5  ret      
```
