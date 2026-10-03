# Homing pack: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md`

Generated 2026-10-03 15:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h14-the-fifteen-modules-registered-before-main.json`.

Bodies: 10. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00158F60 (124 B, extent 00158F60-00158FDC)

Entered from (direct sites whose caller this page cites): `00158FE0` + 0x1A (call; `00158FE0` is cited on this page); `001590B0` + 0x1A (call; `001590B0` is cited on this page); `00159180` + 0x2B (call; `00159180` is cited on this page); `00159270` + 0x21 (call; `00159270` is cited on this page)
Other direct sites: `00159340` + 0x66 (call)

Host context: "erior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*  | function | size | what the body does | interior anchors | |---|---|---|---| | '00158FE0' | 193 B | atomically adds 1 to dword '02EAE128' and calls '00158F60(0)'; a non-zero result is returned as is; otherwise 'f' = qword '02EAE1B0', filled when null by calling qword '02EAE0E0' (when non-null) with 0xE5AC921F and cachi" / "E0F8' (when non-null) with (0xE5AC921F, t, r) and gives 'r'; on every path it atomically adds -1 to dword '02EAE128' before returning | '00158FF0', '00158FFA', '00159029', '00159068', '00159085' | | '001590B0' | 193 B | atomically adds 1 to dword '02EAE128' and calls '00158F60(0)'; a non-zero result is returned as is; otherwise 'f' = qword '02EAE260', filled when null by calling qword '02EAE0E0' (when non-null) with 0xCEEE8E9F and cachi"

```
00158F60  mov      qword ptr [rsp + 8], rbx
00158F65  mov      qword ptr [rsp + 0x10], rbp
00158F6A  mov      qword ptr [rsp + 0x18], rsi
00158F6F  push     rdi
00158F70  sub      rsp, 0x20
00158F74  lea      rbp, [rip - 0x38f7b]  ; -> 00120000 (image base)
00158F7B  movsxd   rsi, ecx
00158F7E  xor      ebx, ebx
00158F80  cmp      byte ptr [rsi + rbp + 0x2d8e120], bl
00158F87  je       0x158fac  ; -> 00158FAC
00158F89  nop      dword ptr [rax]
00158F90  mov      ecx, 0x64
00158F95  call     qword ptr [rip + 0x769215]  ; -> 008C21B0 [u64 0x0000000001CCC316]
00158F9B  inc      ebx
00158F9D  cmp      ebx, 0xa
00158FA0  jae      0x158fc0  ; -> 00158FC0
00158FA2  cmp      byte ptr [rsi + rbp + 0x2d8e120], 0
00158FAA  jne      0x158f90  ; -> 00158F90
00158FAC  cmp      qword ptr [rbp + rsi*8 + 0x2d8e100], 0  ; image base + 0x2d8e100 = 02EAE100
00158FB5  jne      0x158fc5  ; -> 00158FC5
00158FB7  mov      ecx, esi
00158FB9  call     0x158ec0  ; -> 00158EC0 fn
00158FBE  jmp      0x158fc7  ; -> 00158FC7
00158FC0  or       eax, 0xffffffff
00158FC3  jmp      0x158fc7  ; -> 00158FC7
00158FC5  xor      eax, eax
00158FC7  mov      rbx, qword ptr [rsp + 0x30]
00158FCC  mov      rbp, qword ptr [rsp + 0x38]
00158FD1  mov      rsi, qword ptr [rsp + 0x40]
00158FD6  add      rsp, 0x20
00158FDA  pop      rdi
00158FDB  ret      
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

## 005A5B40 (144 B, extent 005A5B40-005A5BD0)

Entered from (direct sites whose caller this page cites): `005C8BF0` + 0x57 (call; `005C8BF0` is cited on this page); `005C9DD0` + 0x83 (call; `005C9DD0` is cited on this page)
Other direct sites: `005AA3C0` + 0x49 (call)

Host context: "16-byte elements from 'rdx' into 'p', sets qwords '+0' and '+8' of each of the remaining 'ecx' - 'r8d' elements to 0, and returns 'p' | '005AD85E', '005AD86B', '005AD893', '005AD89D', '005AD8B5' | | '005C8BF0' | 168 B | returns 0 at once when 'edx' equals dword '[rcx]'; otherwise 'p' = 0 for 'edx' = 0, else '0017D260(edx*4, 4)', and a null 'p' with a non-zero 'edx' returns 0xD; a non-null 'p' gets '005A5B40(p, qword [rcx+8], min(edx, dw" / "0x7FFFFFFF elements (stride 0x80) and calls '00584730(old)'; on every path stores 'r8d' to dword '[rcx]' and 'rdx' to qword '[rcx+8]' | '005C993E', '005C994A', '005C9962', '005C997D', '005C9984' | | '005C9DD0' | 346 B | returns 'r' = '005C9F30(rcx, edx)' when it is non-zero; with 'c' = dword '[rcx+0x28]' AND 0x7FFFFFFF, returns 0 when 'c' equals 'edx'; otherwise, when 'edx' differs from dword '[rcx+0x28]', takes 'p' = 0 for 'edx' = 0 or"

```
005A5B40  xor      r11d, r11d
005A5B43  mov      r10d, r8d
005A5B46  cmp      r8d, 4
005A5B4A  jb       0x5a5bad  ; -> 005A5BAD
005A5B4C  lea      eax, [r8 - 4]
005A5B50  shr      eax, 2
005A5B53  inc      eax
005A5B55  mov      r9d, eax
005A5B58  lea      r11d, [rax*4]
005A5B60  test     rcx, rcx
005A5B63  je       0x5a5b6d  ; -> 005A5B6D
005A5B65  mov      eax, dword ptr [rdx]
005A5B67  add      rdx, 4
005A5B6B  mov      dword ptr [rcx], eax
005A5B6D  lea      r8, [rcx + 4]
005A5B71  test     r8, r8
005A5B74  je       0x5a5b7f  ; -> 005A5B7F
005A5B76  mov      eax, dword ptr [rdx]
005A5B78  add      rdx, 4
005A5B7C  mov      dword ptr [r8], eax
005A5B7F  lea      rax, [rcx + 8]
005A5B83  test     rax, rax
005A5B86  je       0x5a5b91  ; -> 005A5B91
005A5B88  mov      eax, dword ptr [rdx]
005A5B8A  add      rdx, 4
005A5B8E  mov      dword ptr [rcx + 8], eax
005A5B91  lea      r8, [rcx + 0xc]
005A5B95  test     r8, r8
005A5B98  je       0x5a5ba3  ; -> 005A5BA3
005A5B9A  mov      eax, dword ptr [rdx]
005A5B9C  add      rdx, 4
005A5BA0  mov      dword ptr [r8], eax
005A5BA3  add      rcx, 0x10
005A5BA7  sub      r9, 1
005A5BAB  jne      0x5a5b60  ; -> 005A5B60
005A5BAD  cmp      r11d, r10d
005A5BB0  jae      0x5a5bcf  ; -> 005A5BCF
005A5BB2  sub      r10d, r11d
005A5BB5  mov      r8d, r10d
005A5BB8  test     rcx, rcx
005A5BBB  je       0x5a5bc5  ; -> 005A5BC5
005A5BBD  mov      eax, dword ptr [rdx]
005A5BBF  add      rdx, 4
005A5BC3  mov      dword ptr [rcx], eax
005A5BC5  add      rcx, 4
005A5BC9  sub      r8, 1
005A5BCD  jne      0x5a5bb8  ; -> 005A5BB8
005A5BCF  ret      
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

## 006560E0 (231 B, extent 006560E0-006561C7)

Entered from (direct sites whose caller this page cites): `00655C10` + 0x60 (call; `00655C10` is cited on this page)
Other direct sites: `00654160` + 0x0 (jmp)

Host context: "' (0x2D0 when 's' is null), returns 'r' = '00653E80(rcx, 02D35600, w, h)' when it is non-zero, else returns '00655DC0(rcx, edx, r8d)' | '00655B97', '00655BAB', '00655BC5', '00655BE0', '00655BF1' | | '00655C10' | 134 B | with 's' = '005FD050()' + 0x520, 'w' = 'edx', or when that is 0 dword '[s+0x18]' (0x500 when 's' is null), and 'h' = 'r8d', or when that is 0 dword '[s+0x1C]' (0x2D0 when 's' is null), returns 'r' = '006560E0(rcx, 02D356"

```
006560E0  mov      qword ptr [rsp + 0x10], rbx
006560E5  mov      qword ptr [rsp + 0x18], rbp
006560EA  push     rdi
006560EB  push     r12
006560ED  push     r13
006560EF  push     r14
006560F1  push     r15
006560F3  sub      rsp, 0x30
006560F7  mov      rbp, rdx
006560FA  mov      r12d, r9d
006560FD  xor      r9d, r9d
00656100  mov      r13d, r8d
00656103  mov      r15, rcx
00656106  lea      r8, [rip + 0x26657f3]  ; -> 02CBB900
0065610D  mov      rcx, rbp
00656110  lea      edx, [r9 + 1]
00656114  call     0x63a990  ; -> 0063A990 fn
00656119  mov      r14, rax
0065611C  test     rax, rax
0065611F  jne      0x656128  ; -> 00656128
00656121  xor      ebx, ebx
00656123  mov      rdi, rbx
00656126  jmp      0x65619e  ; -> 0065619E
00656128  mov      rdx, r14
0065612B  mov      rcx, rbp
0065612E  call     0x5d8e40  ; -> 005D8E40 fn
00656133  xor      ebx, ebx
00656135  mov      rdi, rax
00656138  test     rax, rax
0065613B  je       0x656123  ; -> 00656123
0065613D  mov      qword ptr [rsp + 0x60], rsi
00656142  cmp      byte ptr [rax + 8], bl
00656145  jne      0x656180  ; -> 00656180
00656147  mov      rsi, qword ptr [rax]
0065614A  test     rsi, rsi
0065614D  je       0x656180  ; -> 00656180
0065614F  lea      r9, [rip + 0x26a132a]  ; -> 02CF7480
00656156  mov      dword ptr [rsp + 0x20], ebx
0065615A  mov      r8d, r12d
0065615D  mov      edx, r13d
00656160  mov      rcx, rsi
00656163  call     0x60dd70  ; -> 0060DD70 fn
00656168  test     eax, eax
0065616A  jne      0x656180  ; -> 00656180
0065616C  and      dword ptr [rsi + 0x18], 0xfffffffd
00656170  mov      rcx, rsi
00656173  mov      byte ptr [rsi + 9], bl
00656176  call     0x610990  ; -> 00610990 fn
0065617B  mov      byte ptr [rdi + 9], bl
0065617E  jmp      0x656199  ; -> 00656199
00656180  mov      rdx, rdi
00656183  mov      rcx, rbp
00656186  call     0x63abf0  ; -> 0063ABF0 fn
0065618B  mov      rdx, r14
0065618E  mov      rcx, rbp
00656191  call     0x63abf0  ; -> 0063ABF0 fn
00656196  mov      rdi, rbx
00656199  mov      rsi, qword ptr [rsp + 0x60]
0065619E  mov      rbp, qword ptr [rsp + 0x70]
006561A3  mov      eax, 0xd
006561A8  test     rdi, rdi
006561AB  mov      qword ptr [r15 + 0x50], rdi
006561AF  cmove    ebx, eax
006561B2  mov      eax, ebx
006561B4  mov      rbx, qword ptr [rsp + 0x68]
006561B9  add      rsp, 0x30
006561BD  pop      r15
006561BF  pop      r14
006561C1  pop      r13
006561C3  pop      r12
006561C5  pop      rdi
006561C6  ret      
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

## 006AA600 (190 B, extent 006AA600-006AA6BE)

Entered from (direct sites whose caller this page cites): `006BAED0` + 0xB5 (call; `006BAED0` is cited on this page)
Other direct sites: `006AA200` + 0x17 (call); `006AA230` + 0x23 (call)

Host context: "de its function and decodes to the recorded mnemonic.*  | function | size | what the body does | interior anchors | |---|---|---|---| | '006BAA40' | 135 B | stores '00D81200' to qword '[rcx]', calls '006BAED0(rcx)', '00809054(rcx+0x58, 0x10, 2, 0016D6A0)', '00809054(rcx+0x38, 0x10, 2, 0016D6A0)' and '006AA200(rcx)', then '00809950(rcx, 0xA8)' when bit '0x1' of 'dl' is set; returns 'rcx' | '006BAA60', '006BAA63', '006BAA7D', '006BAA97', "

```
006AA600  push     rdi
006AA602  sub      rsp, 0x30
006AA606  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
006AA60F  mov      qword ptr [rsp + 0x48], rbx
006AA614  mov      qword ptr [rsp + 0x50], rbp
006AA619  mov      qword ptr [rsp + 0x58], rsi
006AA61E  mov      rdi, rcx
006AA621  xor      ebp, ebp
006AA623  cmp      qword ptr [rcx + 8], rbp
006AA627  je       0x6aa660  ; -> 006AA660
006AA629  mov      esi, ebp
006AA62B  cmp      dword ptr [rcx + 0x10], ebp
006AA62E  jbe      0x6aa660  ; -> 006AA660
006AA630  mov      eax, esi
006AA632  imul     rbx, rax, 0x38
006AA636  add      rbx, qword ptr [rdi + 8]
006AA63A  mov      dword ptr [rsp + 0x40], ebp
006AA63E  lea      rdx, [rsp + 0x40]
006AA643  lea      rcx, [rbx + 0x10]
006AA647  call     0x5cd330  ; -> 005CD330 fn
006AA64C  lea      rcx, [rbx + 0x10]
006AA650  call     0x5c5230  ; -> 005C5230 fn
006AA655  mov      byte ptr [rbx + 0x28], bpl
006AA659  inc      esi
006AA65B  cmp      esi, dword ptr [rdi + 0x10]
006AA65E  jb       0x6aa630  ; -> 006AA630
006AA660  mov      rcx, qword ptr [rdi + 8]
006AA664  test     rcx, rcx
006AA667  je       0x6aa68b  ; -> 006AA68B
006AA669  lea      rbx, [rcx - 8]
006AA66D  lea      r9, [rip - 0x53cfd4]  ; -> 0016D6A0
006AA674  mov      r8, qword ptr [rbx]
006AA677  mov      edx, 0x38
006AA67C  call     0x809054  ; -> 00809054 fn
006AA681  nop      
006AA682  mov      rcx, rbx
006AA685  call     0x584730  ; -> 00584730 fn
006AA68A  nop      
006AA68B  mov      rcx, qword ptr [rdi + 0x28]
006AA68F  call     0x584730  ; -> 00584730 fn
006AA694  mov      rcx, qword ptr [rdi + 0x18]
006AA698  call     0x584730  ; -> 00584730 fn
006AA69D  mov      qword ptr [rdi + 8], rbp
006AA6A1  mov      qword ptr [rdi + 0x28], rbp
006AA6A5  mov      qword ptr [rdi + 0x18], rbp
006AA6A9  mov      rbx, qword ptr [rsp + 0x48]
006AA6AE  mov      rbp, qword ptr [rsp + 0x50]
006AA6B3  mov      rsi, qword ptr [rsp + 0x58]
006AA6B8  add      rsp, 0x30
006AA6BC  pop      rdi
006AA6BD  ret      
```

## 006AAA20 (17 B, extent 006AAA20-006AAA31)

Entered from (direct sites whose caller this page cites): `005A9480` + 0x14 (call; `005A9480` is cited on this page); `006A97C0` + 0x10 (call; `006A97C0` is cited on this page)
Other direct sites: `006ADE00` + 0x2A (call); `006AFDC0` + 0x27 (call); `006CDF00` + 0x2A (call)

Host context: "ty) with bit '0x1' to qword '[rdx+0x10]', stores 'rdx' into the child slot taken (qword '[rcx+0x18]' for an empty tree) and returns 0 | '005A7DC0', '005A7DC6', '005A7DFE', '005A7E34', '005A7E5F' | | '005A9480' | 223 B | calls '006AAA20(rcx+8, 02CAD140)'; stores '00D31898' to qword '[rcx]', '00D31620' to qword '+0x38', '00D31768' to qword '+0x70' and '00D31880' to qword '+0x90'; stores 0 to qwords '+0x20', '+0x30', '+0x48', '+0x58', '+0x" / "hen 'rdx' is 'rcx+8', 'r8d' is 1 and 'r' is non-null it calls '00639850(r, rcx+8, 1)', otherwise '006A5950(rcx, rdx, r8d)'; returns 0 | '006A92BF', '006A92C2', '006A92CA', '006A92DA', '006A92EA' | | '006A97C0' | 101 B | calls '006AAA20(rcx, 02E4E1E0)', then leaves dwords '+0x1C', '+0x24' and '+0x30' at 0x3F800000 and dwords '+0x18', '+0x20', '+0x28', '+0x2C', '+0x34', '+0x38', '+0x3C', '+0x40' and '+0x44' and qwords '+0x48', '+0x50', '+"

```
006AAA20  xor      eax, eax
006AAA22  mov      qword ptr [rcx], rax
006AAA25  mov      qword ptr [rcx + 8], rax
006AAA29  mov      rax, rcx
006AAA2C  mov      qword ptr [rcx + 0x10], rdx
006AAA30  ret      
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
