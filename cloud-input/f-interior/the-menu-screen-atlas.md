# F-interior pack: `16-UI/Menu-Screen-Atlas/the-menu-screen-atlas.md`

Generated 2026-10-02 09:51 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/the-menu-screen-atlas.json`.

Functions: 13. Each is cited on the page only at its entry and is still in the F frontier.

## 00556DB0 (272 B, extent 00556DB0-00556EC0)

Page context: "y | message ids | layout-key families | constant files | effect registry | |---|---:|---|---|---|---|---|---| | '005565E0' | 16 / 15 | evidence | '005572B0' | 1,4,18,25 | 'LicenseBoard…' | — | — | | '00556DB0' | 1 / 1 | child of a license board procedure | '00556D20' | 1,18 | — | — | — | | '00557760' | 9 / 8 | child of a license board procedure | '00557370' | 1,4,18 | — | — | — | | '00557DB0' | 55 / 50 | evidence | '00557AE0' | 10 | 'Li"

```
00556DB0  push     rdi
00556DB2  sub      rsp, 0x20
00556DB6  mov      r8d, dword ptr [rdx]
00556DB9  mov      rdi, rcx
00556DBC  sub      r8d, 1
00556DC0  je       0x556dd6  ; -> 00556DD6
00556DC2  cmp      r8d, 0x11
00556DC6  je       0x556eb8  ; -> 00556EB8
00556DCC  add      rsp, 0x20
00556DD0  pop      rdi
00556DD1  jmp      0x5c5230  ; -> 005C5230 fn
00556DD6  mov      rax, qword ptr [rip + 0x1b43e53]  ; -> 0209AC30
00556DDD  add      rcx, 0x50
00556DE1  mov      qword ptr [rsp + 0x30], rbx
00556DE6  mov      r9, rdi
00556DE9  mov      rbx, qword ptr [rdx + 8]
00556DED  xor      r8d, r8d
00556DF0  mov      rdx, qword ptr [rax + 0x98]
00556DF7  call     0x2432b0  ; -> 002432B0 fn
00556DFC  mov      rcx, qword ptr [rbx]
00556DFF  mov      qword ptr [rdi + 0xc8], rcx
00556E06  movzx    edx, word ptr [rax + 8]
00556E0A  movsx    ecx, word ptr [rax + 6]
00556E0E  movzx    r8d, word ptr [rax + 0xa]
00556E13  movzx    eax, word ptr [rax + 4]
00556E17  mov      word ptr [rdi + 0x9a], cx
00556E1E  mov      rcx, rdi
00556E21  mov      word ptr [rdi + 0x9c], dx
00556E28  lea      rdx, [rip + 0x7cc1b1]  ; -> 00D22FE0
00556E2F  mov      word ptr [rdi + 0x98], ax
00556E36  mov      word ptr [rdi + 0x9e], r8w
00556E3E  call     0x247570  ; -> 00247570 fn
00556E43  mov      rax, qword ptr [rdi + 0x60]
00556E47  xor      edx, edx
00556E49  mov      rcx, qword ptr [rax]
00556E4C  mov      rax, qword ptr [rcx + 0x18]
00556E50  lea      rcx, [rip - 0x19147]  ; -> 0053DD10
00556E57  mov      qword ptr [rdi + 0xc0], rax
00556E5E  mov      qword ptr [rax + 0x120], rcx
00556E65  mov      rax, qword ptr [rdi + 0xc0]
00556E6C  mov      qword ptr [rax + 0xd8], rdi
00556E73  mov      rax, qword ptr [rdi + 0xc0]
00556E7A  and      dword ptr [rax + 0xe0], 0xffdfffff
00556E84  mov      rcx, qword ptr [rdi + 0xc0]
00556E8B  call     0x2d45c0  ; -> 002D45C0 fn
00556E90  mov      rax, qword ptr [rdi + 0xc0]
00556E97  and      dword ptr [rax + 0xe0], 0xf7ffffff
00556EA1  call     0x2445c0  ; -> 002445C0 fn
00556EA6  mov      edx, 0x73
00556EAB  mov      rcx, rdi
00556EAE  call     0x247930  ; -> 00247930 fn
00556EB3  mov      rbx, qword ptr [rsp + 0x30]
00556EB8  xor      eax, eax
00556EBA  add      rsp, 0x20
00556EBE  pop      rdi
00556EBF  ret      
```

## 00558CE0 (386 B, extent 00558CE0-00558E62)

Page context: "| — | | '00557760' | 9 / 8 | child of a license board procedure | '00557370' | 1,4,18 | — | — | — | | '00557DB0' | 55 / 50 | evidence | '00557AE0' | 10 | 'LicenseBoard…' | — | fx-remove,fx-spawn | | '00558CE0' | 7 / 6 | child of a license board procedure | '00558C40' | 1,2,18 | — | — | — | | '00558FB0' | 37 / 37 | evidence | '00558F20' | 1,2,15,16,18,20 | — | 'Maru_c.tm2', 'Maru_c_2.tm2', 'lic_B_4_c.tm2', 'lic_B_8_c.tm2' | fx-reset | | "

```
00558CE0  mov      qword ptr [rsp + 0x10], rbx
00558CE5  push     rsi
00558CE6  sub      rsp, 0x20
00558CEA  mov      rsi, rcx
00558CED  mov      ecx, dword ptr [rdx]
00558CEF  sub      ecx, 1
00558CF2  je       0x558d50  ; -> 00558D50
00558CF4  sub      ecx, 1
00558CF7  je       0x558e55  ; -> 00558E55
00558CFD  cmp      ecx, 0x10
00558D00  je       0x558d14  ; -> 00558D14
00558D02  mov      rcx, rsi
00558D05  mov      rbx, qword ptr [rsp + 0x38]
00558D0A  add      rsp, 0x20
00558D0E  pop      rsi
00558D0F  jmp      0x5c5230  ; -> 005C5230 fn
00558D14  cmp      dword ptr [rip + 0x275095d], 0  ; -> 02CA9678
00558D1B  je       0x558e55  ; -> 00558E55
00558D21  mov      rcx, qword ptr [rip + 0x1b41ef0]  ; -> 0209AC18
00558D28  xor      ebx, ebx
00558D2A  mov      qword ptr [rip + 0x27502af], rbx  ; -> 02CA8FE0
00558D31  test     rcx, rcx
00558D34  je       0x558d3d  ; -> 00558D3D
00558D36  xor      edx, edx
00558D38  call     0x247730  ; -> 00247730 fn
00558D3D  mov      dword ptr [rip + 0x2750935], ebx  ; -> 02CA9678
00558D43  xor      eax, eax
00558D45  mov      rbx, qword ptr [rsp + 0x38]
00558D4A  add      rsp, 0x20
00558D4E  pop      rsi
00558D4F  ret      
00558D50  mov      rax, qword ptr [rip + 0x1b41ed9]  ; -> 0209AC30
00558D57  lea      rcx, [rsi + 0x50]
00558D5B  mov      rbx, qword ptr [rdx + 8]
00558D5F  mov      r9, rsi
00558D62  mov      r8d, 1
00558D68  mov      qword ptr [rsp + 0x30], rdi
00558D6D  mov      rdx, qword ptr [rax + 0x98]
00558D74  call     0x2432b0  ; -> 002432B0 fn
00558D79  movzx    ecx, word ptr [rax + 0xa]
00558D7D  movzx    edx, word ptr [rax + 8]
00558D81  movsx    r8d, word ptr [rax + 6]
00558D86  test     rsi, rsi
00558D89  je       0x558dac  ; -> 00558DAC
00558D8B  movzx    eax, word ptr [rax + 4]
00558D8F  mov      word ptr [rsi + 0x98], ax
00558D96  mov      word ptr [rsi + 0x9a], r8w
00558D9E  mov      word ptr [rsi + 0x9c], dx
00558DA5  mov      word ptr [rsi + 0x9e], cx
00558DAC  lea      rdx, [rip + 0x7ca27d]  ; -> 00D23030
00558DB3  mov      rcx, rsi
00558DB6  call     0x247570  ; -> 00247570 fn
00558DBB  mov      rax, qword ptr [rbx]
00558DBE  mov      qword ptr [rsi + 0xc0], rax
00558DC5  mov      ecx, dword ptr [rax + 0x354]
00558DCB  mov      dword ptr [rsi + 0xc8], ecx
00558DD1  call     0x282df0  ; -> 00282DF0 fn
00558DD6  mov      rcx, qword ptr [rsi + 0x60]
00558DDA  mov      rdi, rax
00558DDD  movsx    edx, word ptr [rax + 0x60]
00558DE1  mov      rbx, qword ptr [rcx + 0x10]
00558DE5  mov      ecx, 2
00558DEA  call     0x35d330  ; -> 0035D330 fn
00558DEF  xor      edx, edx
00558DF1  mov      rcx, qword ptr [rax + 0x18]
00558DF5  call     0x2b58b0  ; -> 002B58B0 fn
00558DFA  xor      ecx, ecx
00558DFC  mov      qword ptr [rbx + 0x18], rax
00558E00  call     0x20e620  ; -> 0020E620 fn
00558E05  mov      dword ptr [rbx + 0x20], eax
00558E08  mov      rax, qword ptr [rsi + 0x60]
00558E0C  movsx    ecx, word ptr [rdi + 0x60]
00558E10  mov      rbx, qword ptr [rax + 8]
00558E14  call     0x2c9bd0  ; -> 002C9BD0 fn
00558E19  mov      rcx, qword ptr [rbx + 0x20]
00558E1D  movsxd   r8, eax
00558E20  movzx    r8d, byte ptr [rcx + r8*8 + 7]
00558E26  mov      rcx, rsi
00558E29  mov      byte ptr [rbx + 0x39], r8b
00558E2D  mov      word ptr [rbx + 0xa], ax
00558E31  call     0x558e70  ; -> 00558E70 fn
00558E36  mov      edx, 0x5f
00558E3B  mov      rcx, rsi
00558E3E  call     0x247930  ; -> 00247930 fn
00558E43  mov      edx, 1
00558E48  mov      rcx, rsi
00558E4B  call     0x247730  ; -> 00247730 fn
00558E50  mov      rdi, qword ptr [rsp + 0x30]
00558E55  xor      eax, eax
00558E57  mov      rbx, qword ptr [rsp + 0x38]
00558E5C  add      rsp, 0x20
00558E60  pop      rsi
00558E61  ret      
```

## 00560210 (1021 B, extent 00560210-0056060D)

Page context: "00560910' (312 instructions): looks up the images '01E0C248' and '01E0C268' ('0024A5A0'), string '0x4B5' ('002814E0'), the name '00D22FE0', builds the '0xC8' child '00558BB0' ('00560A9E'), registers '00560210' and '00560610' as callbacks, assembles the board through '0055F780', '00560EE0', '002D7580' twice, '00291D70'/'00291D80' (string '0xCDF'), '002D45C0', '00561DC0', '00561100', '00558F20' and '00561300', and under '02F9736A' bit 15 "

```
00560210  mov      qword ptr [rsp + 0x18], rbx
00560215  push     rbp
00560216  push     rsi
00560217  push     rdi
00560218  push     r12
0056021A  push     r13
0056021C  push     r14
0056021E  push     r15
00560220  sub      rsp, 0x30
00560224  movsxd   rax, r9d
00560227  mov      rdi, rdx
0056022A  add      rax, 0x48
0056022E  lea      rax, [rcx + rax*4]
00560232  mov      ecx, dword ptr [rax]
00560234  mov      qword ptr [rsp + 0x78], rax
00560239  call     0x282df0  ; -> 00282DF0 fn
0056023E  mov      rcx, qword ptr [rdi + 0x10]
00560242  mov      rsi, rax
00560245  mov      qword ptr [rsp + 0x70], rax
0056024A  movsx    edx, word ptr [rax + 0x60]
0056024E  mov      rbx, qword ptr [rcx + 0x40]
00560252  mov      ecx, 2
00560257  call     0x35d330  ; -> 0035D330 fn
0056025C  xor      edx, edx
0056025E  mov      rcx, qword ptr [rax + 0x18]
00560262  call     0x2b58b0  ; -> 002B58B0 fn
00560267  xor      ecx, ecx
00560269  mov      qword ptr [rbx + 0x18], rax
0056026D  call     0x20e620  ; -> 0020E620 fn
00560272  mov      dword ptr [rbx + 0x20], eax
00560275  movzx    ecx, byte ptr [rsi + 0x60]
00560279  call     0x3236b0  ; -> 003236B0 fn
0056027E  movzx    ecx, byte ptr [rsi + 0x60]
00560282  xor      r12d, r12d
00560285  cmp      al, 0xff
00560287  movzx    r14d, al
0056028B  setne    r12b
0056028F  call     0x323670  ; -> 00323670 fn
00560294  movzx    ecx, byte ptr [rsi + 0x60]
00560298  movzx    ebp, al
0056029B  call     0x323630  ; -> 00323630 fn
005602A0  xor      r13d, r13d
005602A3  movzx    esi, al
005602A6  cmp      bpl, 0xff
005602AA  setne    r13b
005602AE  xor      r15d, r15d
005602B1  cmp      al, 0xff
005602B3  setne    r15b
005602B7  test     r15d, r15d
005602BA  je       0x5602c9  ; -> 005602C9
005602BC  cmp      r14b, al
005602BF  jne      0x5602c9  ; -> 005602C9
005602C1  movzx    esi, bpl
005602C5  movzx    ebp, r14b
005602C9  mov      rax, qword ptr [rdi + 0x10]
005602CD  mov      rbx, qword ptr [rax + 0x70]
005602D1  and      dword ptr [rbx + 8], 0xfffffffe
005602D5  or       dword ptr [rbx + 8], r13d
005602D9  test     r15d, r15d
005602DC  je       0x5602ee  ; -> 005602EE
005602DE  cmp      bpl, sil
005602E1  jle      0x5602ee  ; -> 005602EE
005602E3  movsx    eax, bpl
005602E7  movzx    ebp, sil
005602EB  movzx    esi, al
005602EE  movsx    ecx, bpl
005602F2  add      ecx, 0x3ed
005602F8  call     0x2f9860  ; -> 002F9860 fn
005602FD  movsx    ecx, sil
00560301  mov      rbp, rax
00560304  add      ecx, 0x3ed
0056030A  call     0x2f9860  ; -> 002F9860 fn
0056030F  mov      rsi, rax
00560312  test     r13d, r13d
00560315  je       0x560337  ; -> 00560337
00560317  xor      ecx, ecx
00560319  mov      qword ptr [rbx + 0x18], rbp
0056031D  call     0x20e620  ; -> 0020E620 fn
00560322  mov      rcx, rbx
00560325  mov      dword ptr [rbx + 0x20], eax
00560328  call     0x29fb50  ; -> 0029FB50 fn
0056032D  xor      ecx, ecx
0056032F  call     0x2dd7e0  ; -> 002DD7E0 fn
00560334  mov      dword ptr [rbx + 0x24], eax
00560337  mov      rax, qword ptr [rdi + 0x10]
0056033B  mov      rbx, qword ptr [rax + 0x80]
00560342  test     r15d, r15d
00560345  je       0x560367  ; -> 00560367
00560347  xor      ecx, ecx
00560349  mov      qword ptr [rbx + 0x18], rsi
0056034D  call     0x20e620  ; -> 0020E620 fn
00560352  mov      rcx, rbx
00560355  mov      dword ptr [rbx + 0x20], eax
00560358  call     0x29fb50  ; -> 0029FB50 fn
0056035D  xor      ecx, ecx
0056035F  call     0x2dd7e0  ; -> 002DD7E0 fn
00560364  mov      dword ptr [rbx + 0x24], eax
00560367  and      dword ptr [rbx + 8], 0xfffffffe
0056036B  or       dword ptr [rbx + 8], r15d
0056036F  mov      rax, qword ptr [rdi + 0x10]
00560373  mov      r8, qword ptr [rax + 0x78]
00560377  and      dword ptr [r8 + 8], 0xfffffffe
0056037C  or       dword ptr [r8 + 8], r12d
00560380  test     r12d, r12d
00560383  je       0x56039b  ; -> 0056039B
00560385  mov      rax, qword ptr [r8 + 0x20]
00560389  movsx    rdx, r14b
0056038D  movzx    ecx, byte ptr [rax + rdx*8 + 7]
00560392  mov      byte ptr [r8 + 0x39], cl
00560396  mov      word ptr [r8 + 0xa], dx
0056039B  mov      rsi, qword ptr [rsp + 0x70]
005603A0  mov      edx, 3
005603A5  movsx    ecx, word ptr [rsi + 0x60]
005603A9  call     0x2c9b30  ; -> 002C9B30 fn
005603AE  mov      rcx, qword ptr [rdi + 0x10]
005603B2  mov      r10d, 0xfff
005603B8  movsxd   rdx, eax
005603BB  mov      r9, qword ptr [rcx + 0x60]
005603BF  mov      rcx, qword ptr [r9 + 0x20]
005603C3  lea      r8, [rcx + rdx*8]
005603C7  mov      rdx, qword ptr [r9]
005603CA  movzx    ecx, byte ptr [r8 + 7]
005603CF  mov      word ptr [r9 + 0xa], ax
005603D4  mov      byte ptr [r9 + 0x39], cl
005603D8  movzx    eax, word ptr [rdx + 8]
005603DC  movzx    ecx, word ptr [r8 + 4]
005603E1  and      cx, r10w
005603E5  sub      ax, cx
005603E8  add      ax, word ptr [rdx + 4]
005603EC  mov      word ptr [r9 + 0xc], ax
005603F1  movzx    eax, word ptr [rdx + 0xa]
005603F5  mov      ecx, dword ptr [r8 + 4]
005603F9  shr      ecx, 0xc
005603FC  and      cx, r10w
00560400  sub      ax, cx
00560403  add      ax, word ptr [rdx + 6]
00560407  mov      word ptr [r9 + 0xe], ax
0056040C  movzx    eax, word ptr [r8 + 4]
00560411  and      ax, r10w
00560415  mov      word ptr [r9 + 0x10], ax
0056041A  mov      eax, dword ptr [r8 + 4]
0056041E  shr      eax, 0xc
00560421  and      ax, r10w
00560425  mov      word ptr [r9 + 0x12], ax
0056042A  mov      rax, qword ptr [rip + 0x1b3a7ff]  ; -> 0209AC30
00560431  movsx    ecx, word ptr [rax + 0xde0]
00560438  mov      rax, qword ptr [rsp + 0x78]
0056043D  cmp      ecx, dword ptr [rax]
0056043F  mov      rax, qword ptr [rdi + 0x10]
00560443  mov      rbx, qword ptr [rax]
00560446  jne      0x5604fc  ; -> 005604FC
0056044C  mov      ecx, 0xfc
00560451  call     0x2dd7e0  ; -> 002DD7E0 fn
00560456  and      dword ptr [rbx + 0x28], 0xff000000
0056045D  and      eax, 0xffffff
00560462  or       dword ptr [rbx + 0x28], eax
00560465  mov      ecx, 0xfc
0056046A  and      dword ptr [rbx + 0x2c], 0xff000000
00560471  or       dword ptr [rbx + 0x2c], eax
00560474  and      dword ptr [rbx + 0x30], 0xff000000
0056047B  or       dword ptr [rbx + 0x30], eax
0056047E  and      dword ptr [rbx + 0x34], 0xff000000
00560485  or       dword ptr [rbx + 0x34], eax
00560488  mov      rax, qword ptr [rdi + 0x10]
0056048C  mov      rbx, qword ptr [rax + 8]
00560490  call     0x2dd7e0  ; -> 002DD7E0 fn
00560495  and      dword ptr [rbx + 0x28], 0xff000000
0056049C  and      eax, 0xffffff
005604A1  or       dword ptr [rbx + 0x28], eax
005604A4  mov      ecx, 0xfa
005604A9  and      dword ptr [rbx + 0x2c], 0xff000000
005604B0  or       dword ptr [rbx + 0x2c], eax
005604B3  and      dword ptr [rbx + 0x30], 0xff000000
005604BA  or       dword ptr [rbx + 0x30], eax
005604BD  and      dword ptr [rbx + 0x34], 0xff000000
005604C4  or       dword ptr [rbx + 0x34], eax
005604C7  mov      rax, qword ptr [rdi + 0x10]
005604CB  mov      rbx, qword ptr [rax + 0x28]
005604CF  call     0x2dd7e0  ; -> 002DD7E0 fn
005604D4  mov      dword ptr [rbx + 0x34], eax
005604D7  mov      ecx, 0xfa
005604DC  mov      dword ptr [rbx + 0x30], eax
005604DF  mov      dword ptr [rbx + 0x2c], eax
005604E2  mov      dword ptr [rbx + 0x28], eax
005604E5  mov      rax, qword ptr [rdi + 0x10]
005604E9  mov      rbx, qword ptr [rax + 0x30]
005604ED  call     0x2dd7e0  ; -> 002DD7E0 fn
005604F2  mov      ecx, 0xfa
005604F7  jmp      0x5605a7  ; -> 005605A7
005604FC  mov      ecx, 0xfd
00560501  call     0x2dd7e0  ; -> 002DD7E0 fn
00560506  and      dword ptr [rbx + 0x28], 0xff000000
0056050D  and      eax, 0xffffff
00560512  or       dword ptr [rbx + 0x28], eax
00560515  mov      ecx, 0xfd
0056051A  and      dword ptr [rbx + 0x2c], 0xff000000
00560521  or       dword ptr [rbx + 0x2c], eax
00560524  and      dword ptr [rbx + 0x30], 0xff000000
0056052B  or       dword ptr [rbx + 0x30], eax
0056052E  and      dword ptr [rbx + 0x34], 0xff000000
00560535  or       dword ptr [rbx + 0x34], eax
00560538  mov      rax, qword ptr [rdi + 0x10]
0056053C  mov      rbx, qword ptr [rax + 8]
00560540  call     0x2dd7e0  ; -> 002DD7E0 fn
00560545  and      dword ptr [rbx + 0x28], 0xff000000
0056054C  and      eax, 0xffffff
00560551  or       dword ptr [rbx + 0x28], eax
00560554  mov      ecx, 0xfb
00560559  and      dword ptr [rbx + 0x2c], 0xff000000
00560560  or       dword ptr [rbx + 0x2c], eax
00560563  and      dword ptr [rbx + 0x30], 0xff000000
0056056A  or       dword ptr [rbx + 0x30], eax
0056056D  and      dword ptr [rbx + 0x34], 0xff000000
00560574  or       dword ptr [rbx + 0x34], eax
00560577  mov      rax, qword ptr [rdi + 0x10]
0056057B  mov      rbx, qword ptr [rax + 0x28]
0056057F  call     0x2dd7e0  ; -> 002DD7E0 fn
00560584  mov      dword ptr [rbx + 0x34], eax
00560587  mov      ecx, 0xfb
0056058C  mov      dword ptr [rbx + 0x30], eax
0056058F  mov      dword ptr [rbx + 0x2c], eax
00560592  mov      dword ptr [rbx + 0x28], eax
00560595  mov      rax, qword ptr [rdi + 0x10]
00560599  mov      rbx, qword ptr [rax + 0x30]
0056059D  call     0x2dd7e0  ; -> 002DD7E0 fn
005605A2  mov      ecx, 0xfb
005605A7  mov      dword ptr [rbx + 0x34], eax
005605AA  mov      dword ptr [rbx + 0x30], eax
005605AD  mov      dword ptr [rbx + 0x2c], eax
005605B0  mov      dword ptr [rbx + 0x28], eax
005605B3  mov      rax, qword ptr [rdi + 0x10]
005605B7  mov      rbx, qword ptr [rax + 0x38]
005605BB  call     0x2dd7e0  ; -> 002DD7E0 fn
005605C0  mov      dword ptr [rbx + 0x28], eax
005605C3  xor      r8d, r8d
005605C6  mov      dword ptr [rbx + 0x2c], eax
005605C9  xor      edx, edx
005605CB  mov      dword ptr [rbx + 0x30], eax
005605CE  mov      dword ptr [rbx + 0x34], eax
005605D1  xor      eax, eax
005605D3  mov      rcx, qword ptr [rdi + 0x10]
005605D7  mov      r9d, dword ptr [rsi + 0xb0]
005605DE  mov      qword ptr [rsp + 0x28], rax
005605E3  mov      dword ptr [rsp + 0x20], eax
005605E7  mov      rcx, qword ptr [rcx + 0x50]
005605EB  call     0x29ff60  ; -> 0029FF60 fn
005605F0  mov      rbx, qword ptr [rsp + 0x80]
005605F8  mov      eax, 1
005605FD  add      rsp, 0x30
00560601  pop      r15
00560603  pop      r14
00560605  pop      r13
00560607  pop      r12
00560609  pop      rdi
0056060A  pop      rsi
0056060B  pop      rbp
0056060C  ret      
```

## 00560610 (760 B, extent 00560610-00560908)

Page context: "instructions): looks up the images '01E0C248' and '01E0C268' ('0024A5A0'), string '0x4B5' ('002814E0'), the name '00D22FE0', builds the '0xC8' child '00558BB0' ('00560A9E'), registers '00560210' and '00560610' as callbacks, assembles the board through '0055F780', '00560EE0', '002D7580' twice, '00291D70'/'00291D80' (string '0xCDF'), '002D45C0', '00561DC0', '00561100', '00558F20' and '00561300', and under '02F9736A' bit 15 starts the back"

```
00560610  push     rbx
00560612  push     rbp
00560613  push     rsi
00560614  push     r12
00560616  push     r14
00560618  sub      rsp, 0xd0
0056061F  mov      rax, qword ptr [rip + 0x19e420a]  ; -> 01F44830 [u64 0x00002B992DDFA232]
00560626  xor      rax, rsp
00560629  mov      qword ptr [rsp + 0xa8], rax
00560631  movsxd   rsi, r9d
00560634  mov      rbx, rcx
00560637  mov      r14, r8
0056063A  mov      r12, rdx
0056063D  mov      ecx, dword ptr [rcx + rsi*4 + 0x120]
00560644  call     0x282df0  ; -> 00282DF0 fn
00560649  movzx    ecx, byte ptr [rax + 0x60]
0056064D  call     0x323670  ; -> 00323670 fn
00560652  movzx    ebp, al
00560655  cmp      al, 0xff
00560657  je       0x5608e4  ; -> 005608E4
0056065D  mov      r8, qword ptr [rbx + 0xe0]
00560664  mov      r9d, 0xfff
0056066A  mov      qword ptr [rsp + 0xc8], rdi
00560672  mov      edi, 0xc
00560677  mov      qword ptr [rsp + 0xc0], r13
0056067F  mov      qword ptr [rsp + 0x78], r8
00560684  mov      rcx, qword ptr [r8 + 0x20]
00560688  add      rcx, 0x30
0056068C  mov      qword ptr [rsp + 0xb8], r15
00560694  movzx    eax, word ptr [rcx + 0x14]
00560698  movzx    edx, word ptr [rcx + rax*2 + 0x1c]
0056069D  movzx    eax, word ptr [rcx + 0x10]
005606A1  add      rcx, rax
005606A4  movzx    eax, word ptr [rcx + rdx*8]
005606A8  mov      word ptr [rsp + 0x58], ax
005606AD  movzx    eax, word ptr [rcx + rdx*8 + 2]
005606B2  mov      word ptr [rsp + 0x5a], ax
005606B7  movzx    eax, word ptr [rcx + rdx*8 + 4]
005606BC  and      ax, r9w
005606C0  mov      word ptr [rsp + 0x5c], ax
005606C5  mov      eax, dword ptr [rcx + rdx*8 + 4]
005606C9  shr      eax, 0xc
005606CC  and      ax, r9w
005606D0  mov      word ptr [rsp + 0x5e], ax
005606D5  mov      r13d, dword ptr [rcx + rdx*8 + 4]
005606DA  mov      r15d, r13d
005606DD  mov      eax, dword ptr [r14 + 0x90]
005606E4  and      r15d, r9d
005606E7  mov      r8, qword ptr [r8 + 0x20]
005606EB  mov      dword ptr [rsp + 0x68], eax
005606EF  add      r8, 0x30
005606F3  movzx    eax, byte ptr [r14 + 0x5c]
005606F8  mov      dword ptr [rsp + 0x64], eax
005606FC  shr      r13d, 0xc
00560700  and      r13d, r9d
00560703  movzx    r9d, byte ptr [rcx + rdx*8 + 7]
00560709  movzx    edx, word ptr [r8 + 0x12]
0056070E  mov      eax, r9d
00560711  shr      eax, 4
00560714  and      r9b, 0xf
00560718  movzx    eax, al
0056071B  xor      ecx, ecx
0056071D  add      rax, r8
00560720  movzx    eax, byte ptr [rdx + rax]
00560724  add      al, r9b
00560727  mov      byte ptr [r14 + 0x5c], al
0056072B  call     0x2dd7e0  ; -> 002DD7E0 fn
00560730  mov      dword ptr [r14 + 0x90], eax
00560737  lea      r8d, [rdi - 0xb]
0056073B  mov      rax, qword ptr [r12 + 0x10]
00560740  mov      rdx, r14
00560743  mov      rbx, qword ptr [rbx + rsi*8 + 0x150]
0056074B  mov      rcx, qword ptr [rax + 0x58]
0056074F  movsx    eax, word ptr [rcx + 0xc]
00560753  movsx    r12d, word ptr [rcx + 0xe]
00560758  lea      rcx, [rsp + 0x80]
00560760  mov      dword ptr [rsp + 0x60], eax
00560764  call     0x2d9c40  ; -> 002D9C40 fn
00560769  lea      rcx, [rip + 0x295ea30]  ; -> 02EBF1A0
00560770  movsx    rax, bpl
00560774  xor      r8d, r8d
00560777  mov      edx, r8d
0056077A  mov      dword ptr [rsp + 0x50], edx
0056077E  lea      rax, [rcx + rax*8]
00560782  mov      rcx, qword ptr [rax]
00560785  mov      qword ptr [rsp + 0x70], rax
0056078A  cmp      r8w, word ptr [rcx + 6]
0056078F  jae      0x5608a9  ; -> 005608A9
00560795  nop      word ptr [rax + rax]
005607A0  mov      esi, r8d
005607A3  cmp      r8w, word ptr [rcx + 4]
005607A8  jae      0x56088f  ; -> 0056088F
005607AE  mov      ebp, dword ptr [rsp + 0x60]
005607B2  cmp      word ptr [rbx], -1
005607B6  jle      0x56086e  ; -> 0056086E
005607BC  test     edi, edi
005607BE  jne      0x5607ec  ; -> 005607EC
005607C0  mov      rdx, r14
005607C3  lea      rcx, [rsp + 0x80]
005607CB  call     0x2d9b00  ; -> 002D9B00 fn
005607D0  lea      r8d, [rdi + 1]
005607D4  mov      rdx, r14
005607D7  lea      rcx, [rsp + 0x80]
005607DF  call     0x2d9c40  ; -> 002D9C40 fn
005607E4  xor      r8d, r8d
005607E7  mov      edi, 0xc
005607EC  cmp      word ptr [rbx], 1
005607F0  jne      0x5607f8  ; -> 005607F8
005607F2  movsx    ecx, word ptr [rbx + 2]
005607F6  jmp      0x5607fb  ; -> 005607FB
005607F8  mov      ecx, r8d
005607FB  add      ecx, 0xdb
00560801  call     0x2dd7e0  ; -> 002DD7E0 fn
00560806  mov      r8, qword ptr [rsp + 0x78]
0056080B  lea      r9, [rsp + 0x98]
00560813  mov      dword ptr [rsp + 0x48], 0
0056081B  lea      rcx, [rsp + 0x80]
00560823  mov      dword ptr [rsp + 0x40], r13d
00560828  mov      rdx, r14
0056082B  mov      dword ptr [rsp + 0x38], r15d
00560830  mov      dword ptr [rsp + 0xa4], eax
00560837  mov      dword ptr [rsp + 0xa0], eax
0056083E  mov      dword ptr [rsp + 0x9c], eax
00560845  mov      dword ptr [rsp + 0x98], eax
0056084C  lea      rax, [rsp + 0x58]
00560851  mov      dword ptr [rsp + 0x30], r12d
00560856  mov      dword ptr [rsp + 0x28], ebp
0056085A  mov      qword ptr [rsp + 0x20], rax
0056085F  call     0x2d9380  ; -> 002D9380 fn
00560864  mov      rax, qword ptr [rsp + 0x70]
00560869  dec      edi
0056086B  xor      r8d, r8d
0056086E  mov      rcx, qword ptr [rax]
00560871  add      rbx, 4
00560875  inc      esi
00560877  add      ebp, r15d
0056087A  movzx    eax, word ptr [rcx + 4]
0056087E  cmp      esi, eax
00560880  mov      rax, qword ptr [rsp + 0x70]
00560885  jl       0x5607b2  ; -> 005607B2
0056088B  mov      edx, dword ptr [rsp + 0x50]
0056088F  movzx    eax, word ptr [rcx + 6]
00560893  inc      edx
00560895  add      r12d, r13d
00560898  mov      dword ptr [rsp + 0x50], edx
0056089C  cmp      edx, eax
0056089E  mov      rax, qword ptr [rsp + 0x70]
005608A3  jl       0x5607a0  ; -> 005607A0
005608A9  mov      rdx, r14
005608AC  lea      rcx, [rsp + 0x80]
005608B4  call     0x2d9b00  ; -> 002D9B00 fn
005608B9  mov      eax, dword ptr [rsp + 0x64]
005608BD  mov      r15, qword ptr [rsp + 0xb8]
005608C5  mov      r13, qword ptr [rsp + 0xc0]
005608CD  mov      rdi, qword ptr [rsp + 0xc8]
005608D5  mov      byte ptr [r14 + 0x5c], al
005608D9  mov      eax, dword ptr [rsp + 0x68]
005608DD  mov      dword ptr [r14 + 0x90], eax
005608E4  mov      eax, 1
005608E9  mov      rcx, qword ptr [rsp + 0xa8]
005608F1  xor      rcx, rsp
005608F4  call     0x808c40  ; -> 00808C40 fn
005608F9  add      rsp, 0xd0
00560900  pop      r14
00560902  pop      r12
00560904  pop      rsi
00560905  pop      rbp
00560906  pop      rbx
00560907  ret      
```

## 0056FEF0 (388 B, extent 0056FEF0-00570074)

Page context: "677A0' | 2 / 2 | — | '00567770' | 1,2,14,18 | — | — | — | | '0056C060' | 2 / 2 | — | '0056C170' | 1,2 | — | — | — | | '0056FCB0' | 2 / 2 | — | '005742D0' | — | — | — | — | | '0056FD30' | 1 / 1 | — | '0056FEF0' | 1,3 | — | — | — | | '005701B0' | 47 / 41 | — | '0056EC10' | 1,10,12,14,15,16,18,19 | — | — | — | | '00570460' | 1 / 1 | — | '0056FEF0' | — | — | — | — | | '00570530' | 3 / 3 | — | '0056EF60' | — | — | — | — | | '00570630' | 9 / "

```
0056FEF0  mov      qword ptr [rsp + 0x18], rsi
0056FEF5  push     rdi
0056FEF6  sub      rsp, 0x60
0056FEFA  mov      rax, qword ptr [rip + 0x19d492f]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0056FF01  xor      rax, rsp
0056FF04  mov      qword ptr [rsp + 0x58], rax
0056FF09  mov      rdx, qword ptr [rcx + 0xd0]
0056FF10  mov      r8d, 0x14
0056FF16  mov      rdi, rcx
0056FF19  call     0x3946b0  ; -> 003946B0 fn
0056FF1E  xor      edx, edx
0056FF20  mov      rcx, rdi
0056FF23  call     0x394700  ; -> 00394700 fn
0056FF28  mov      edx, 0x5f
0056FF2D  mov      rcx, rdi
0056FF30  call     0x247930  ; -> 00247930 fn
0056FF35  movzx    edx, word ptr [rdi + 0xe2]
0056FF3C  lea      rcx, [rsp + 0x20]
0056FF41  call     0x5760a0  ; -> 005760A0 fn
0056FF46  movzx    eax, byte ptr [rdi + 0xe1]
0056FF4D  xor      esi, esi
0056FF4F  cmp      al, 2
0056FF51  je       0x56ff7c  ; -> 0056FF7C
0056FF53  cmp      al, 5
0056FF55  jae      0x56ff7c  ; -> 0056FF7C
0056FF57  mov      rcx, qword ptr [rsp + 0x20]
0056FF5C  xor      edx, edx
0056FF5E  call     0x574ba0  ; -> 00574BA0 fn
0056FF63  xor      edx, edx
0056FF65  mov      rcx, rdi
0056FF68  call     0x394660  ; -> 00394660 fn
0056FF6D  mov      rcx, rax
0056FF70  xor      edx, edx
0056FF72  call     0x247870  ; -> 00247870 fn
0056FF77  jmp      0x57000f  ; -> 0057000F
0056FF7C  xor      edx, edx
0056FF7E  mov      qword ptr [rsp + 0x78], rbx
0056FF83  mov      rcx, rdi
0056FF86  lea      r8d, [rdx + 3]
0056FF8A  call     0x3931e0  ; -> 003931E0 fn
0056FF8F  mov      rcx, qword ptr [rsp + 0x20]
0056FF94  mov      rbx, rax
0056FF97  mov      qword ptr [rax + 0x18], rcx
0056FF9B  xor      ecx, ecx
0056FF9D  call     0x20e620  ; -> 0020E620 fn
0056FFA2  xor      r8d, r8d
0056FFA5  mov      dword ptr [rbx + 0x20], eax
0056FFA8  xor      edx, edx
0056FFAA  mov      rcx, rdi
0056FFAD  call     0x3931e0  ; -> 003931E0 fn
0056FFB2  movzx    r9d, word ptr [rdi + 0xe2]
0056FFBA  mov      edx, 3
0056FFBF  inc      r9d
0056FFC2  mov      r8d, edx
0056FFC5  mov      rcx, rax
0056FFC8  call     0x392fa0  ; -> 00392FA0 fn
0056FFCD  movsxd   rax, dword ptr [rdi + 0xd0]
0056FFD4  lea      r8, [rsp + 0x40]
0056FFD9  lea      rdx, [rip + 0x480]  ; -> 00570460
0056FFE0  mov      qword ptr [rsp + 0x48], rax
0056FFE5  mov      ecx, 0xc0
0056FFEA  mov      dword ptr [rsp + 0x40], esi
0056FFEE  mov      qword ptr [rsp + 0x50], rsi
0056FFF3  call     0x244f50  ; -> 00244F50 fn
0056FFF8  mov      rdx, rax
0056FFFB  mov      qword ptr [rdi + 0x148], rax
00570002  mov      rcx, rdi
00570005  call     0x246ad0  ; -> 00246AD0 fn
0057000A  mov      rbx, qword ptr [rsp + 0x78]
0057000F  cmp      qword ptr [rdi + 0xd8], rsi
00570016  je       0x570059  ; -> 00570059
00570018  movsxd   rax, dword ptr [rdi + 0xd8]
0057001F  lea      r8, [rsp + 0x40]
00570024  lea      rdx, [rip - 0x2fb]  ; -> 0056FD30
0057002B  mov      qword ptr [rsp + 0x48], rax
00570030  mov      ecx, 0xc8
00570035  mov      dword ptr [rsp + 0x40], esi
00570039  mov      qword ptr [rsp + 0x50], rsi
0057003E  call     0x244f50  ; -> 00244F50 fn
00570043  mov      rcx, qword ptr [rdi + 0xc0]
0057004A  mov      rdx, rax
0057004D  mov      qword ptr [rdi + 0x150], rax
00570054  call     0x246ad0  ; -> 00246AD0 fn
00570059  mov      rcx, qword ptr [rsp + 0x58]
0057005E  xor      rcx, rsp
00570061  call     0x808c40  ; -> 00808C40 fn
00570066  mov      rsi, qword ptr [rsp + 0x80]
0057006E  add      rsp, 0x60
00570072  pop      rdi
00570073  ret      
```

## 00574BA0 (260 B, extent 00574BA0-00574CA4)

Page context: " | — | '0056EF60' | — | — | — | — | | '00570630' | 9 / 8 | — | '00570080' | 1,3 | — | — | — | | '00571A50' | 47 / 41 | — | '00570BF0' | 1,2,10,12,14,15,18,20 | — | — | — | | '00573B40' | 1 / 1 | — | '00574BA0' | — | — | — | — | | '005742D0' | 35 / 30 | — | '00570080' | 1,3,10,12,14,15,18 | — | — | — | | '00574AD0' | 1 / 1 | — | '00574A00' | — | — | — | — | | '00577F90' | 2 / 2 | — | '00577F00' | 1,18,19 | — | — | — | | '00578450' | 5 / "

```
00574BA0  mov      qword ptr [rsp + 8], rbx
00574BA5  mov      qword ptr [rsp + 0x10], rsi
00574BAA  push     rdi
00574BAB  sub      rsp, 0x80
00574BB2  mov      rax, qword ptr [rip + 0x19cfc77]  ; -> 01F44830 [u64 0x00002B992DDFA232]
00574BB9  xor      rax, rsp
00574BBC  mov      qword ptr [rsp + 0x70], rax
00574BC1  mov      rax, qword ptr [rip + 0x2734b50]  ; -> 02CA9718
00574BC8  mov      rdi, rdx
00574BCB  mov      rsi, rcx
00574BCE  mov      rbx, qword ptr [rax + 0x100]
00574BD5  test     rbx, rbx
00574BD8  je       0x574c82  ; -> 00574C82
00574BDE  mov      rcx, qword ptr [rbx + 0xd0]
00574BE5  test     rcx, rcx
00574BE8  je       0x574bef  ; -> 00574BEF
00574BEA  call     0x244f00  ; -> 00244F00 fn
00574BEF  mov      rax, qword ptr [rbx + 0x60]
00574BF3  lea      r9, [rsp + 0x30]
00574BF8  mov      rcx, qword ptr [rbx + 0xc0]
00574BFF  mov      rdx, qword ptr [rax]
00574C02  lea      rax, [rsp + 0x34]
00574C07  mov      qword ptr [rsp + 0x20], rax
00574C0C  movss    xmm2, dword ptr [rdx + 0x28]
00574C11  mov      rdx, qword ptr [rbx + 0xc8]
00574C18  call     0x29cd00  ; -> 0029CD00 fn
00574C1D  xor      ecx, ecx
00574C1F  mov      qword ptr [rsp + 0x38], rsi
00574C24  mov      dword ptr [rsp + 0x58], ecx
00574C28  lea      rax, [rsp + 0x38]
00574C2D  mov      qword ptr [rsp + 0x60], rax
00574C32  lea      r8, [rsp + 0x58]
00574C37  mov      rax, qword ptr [rip + 0x2734ada]  ; -> 02CA9718
00574C3E  lea      rdx, [rip - 0x1105]  ; -> 00573B40
00574C45  mov      qword ptr [rsp + 0x68], rcx
00574C4A  mov      qword ptr [rsp + 0x40], rdi
00574C4F  mov      rcx, qword ptr [rax + 0x128]
00574C56  mov      eax, dword ptr [rsp + 0x30]
00574C5A  mov      qword ptr [rsp + 0x48], rcx
00574C5F  mov      ecx, 0xc0
00574C64  mov      dword ptr [rsp + 0x50], eax
00574C68  call     0x244f50  ; -> 00244F50 fn
00574C6D  mov      rcx, qword ptr [rip + 0x2734aa4]  ; -> 02CA9718
00574C74  mov      rdx, qword ptr [rcx + 0x100]
00574C7B  mov      qword ptr [rdx + 0xd0], rax
00574C82  mov      rcx, qword ptr [rsp + 0x70]
00574C87  xor      rcx, rsp
00574C8A  call     0x808c40  ; -> 00808C40 fn
00574C8F  lea      r11, [rsp + 0x80]
00574C97  mov      rbx, qword ptr [r11 + 0x10]
00574C9B  mov      rsi, qword ptr [r11 + 0x18]
00574C9F  mov      rsp, r11
00574CA2  pop      rdi
00574CA3  ret      
```

## 00576C70 (44 B, extent 00576C70-00576C9C)

Page context: "D', '0029F4B0', '00225580', '0029F480', post '0x5F'; '0056FD30' (1, 2) a sixteen-byte layout of words '0xFFF', '002D8C80', geometry from '01E0C1D8'/'01E0C1DC', post '0x64'; '00570630' (1, 2; subtree '00576C70') two sprite strips through '002DAF30', '002D9DB0', '002DA2D0' and '002DAC70' with colour words '0x80808080', results at '+0xC0'..'+0xD0': a picture pane; '00573B40' text kind '0x2B' from record '+0x10', '+0x98' widened by record '"

```
00576C70  mov      rax, qword ptr [rip + 0x2732ac1]  ; -> 02CA9738
00576C77  test     rax, rax
00576C7A  je       0x576c88  ; -> 00576C88
00576C7C  mov      rax, qword ptr [rax + 0x118]
00576C83  test     rax, rax
00576C86  jne      0x576c8b  ; -> 00576C8B
00576C88  xor      eax, eax
00576C8A  ret      
00576C8B  cmp      byte ptr [rax + 0xc9], 1
00576C92  jne      0x576c88  ; -> 00576C88
00576C94  mov      rax, qword ptr [rax + 0xf8]
00576C9B  ret      
```

## 00577F00 (141 B, extent 00577F00-00577F8D)

Page context: "1 / 1 | — | '00574BA0' | — | — | — | — | | '005742D0' | 35 / 30 | — | '00570080' | 1,3,10,12,14,15,18 | — | — | — | | '00574AD0' | 1 / 1 | — | '00574A00' | — | — | — | — | | '00577F90' | 2 / 2 | — | '00577F00' | 1,18,19 | — | — | — | | '00578450' | 5 / 5 | — | '005781A0' | 1,10,12,14 | — | — | — | | '005789D0' | 42 / 40 | — | '00578920' | 1,10,12,14,15,16,18 | 'Na…' | — | — | | '00579420' | 27 / 25 | — | '00579130' | 1,2,10,12,14,15,18,"

```
00577F00  mov      r11, rsp
00577F03  sub      rsp, 0x68
00577F07  mov      rax, qword ptr [rip + 0x19cc922]  ; -> 01F44830 [u64 0x00002B992DDFA232]
00577F0E  xor      rax, rsp
00577F11  mov      qword ptr [rsp + 0x50], rax
00577F16  mov      rax, qword ptr [rip + 0x273182b]  ; -> 02CA9748
00577F1D  cmp      qword ptr [rax + 0x128], 0
00577F25  jne      0x577f7b  ; -> 00577F7B
00577F27  mov      byte ptr [rsp + 0x20], cl
00577F2B  lea      rax, [r11 - 0x48]
00577F2F  mov      ecx, dword ptr [rsp + 0x24]
00577F33  xor      r10d, r10d
00577F36  mov      qword ptr [r11 - 0x28], rax
00577F3A  mov      eax, ecx
00577F3C  xor      eax, r9d
00577F3F  mov      dword ptr [r11 - 0x30], r10d
00577F43  and      eax, 1
00577F46  mov      qword ptr [r11 - 0x20], r10
00577F4A  xor      ecx, eax
00577F4C  mov      dword ptr [rsp + 0x24], ecx
00577F50  mov      ecx, 0xd8
00577F55  mov      qword ptr [r11 - 0x40], rdx
00577F59  lea      rdx, [rip + 0x30]  ; -> 00577F90
00577F60  mov      qword ptr [r11 - 0x38], r8
00577F64  lea      r8, [r11 - 0x30]
00577F68  call     0x244f50  ; -> 00244F50 fn
00577F6D  mov      rcx, qword ptr [rip + 0x27317d4]  ; -> 02CA9748
00577F74  mov      qword ptr [rcx + 0x128], rax
00577F7B  mov      rcx, qword ptr [rsp + 0x50]
00577F80  xor      rcx, rsp
00577F83  call     0x808c40  ; -> 00808C40 fn
00577F88  add      rsp, 0x68
00577F8C  ret      
```

## 00579130 (123 B, extent 00579130-005791AB)

Page context: " | 1,18,19 | — | — | — | | '00578450' | 5 / 5 | — | '005781A0' | 1,10,12,14 | — | — | — | | '005789D0' | 42 / 40 | — | '00578920' | 1,10,12,14,15,16,18 | 'Na…' | — | — | | '00579420' | 27 / 25 | — | '00579130' | 1,2,10,12,14,15,18,19,20 | — | — | — | | '00579AF0' | 33 / 33 | — | '00579990', '00579A40' | 1,2,16,18 | — | — | — | | '0057F7D0' | 5 / 5 | — | '00583990' | 1,2,18 | — | — | — |  ## 4. Beyond the menu range — all 267 handler-cen"

```
00579130  mov      r11, rsp
00579133  sub      rsp, 0x68
00579137  mov      rax, qword ptr [rip + 0x19cb6f2]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0057913E  xor      rax, rsp
00579141  mov      qword ptr [rsp + 0x50], rax
00579146  mov      rax, qword ptr [rip + 0x27305fb]  ; -> 02CA9748
0057914D  cmp      qword ptr [rax + 0x118], 0
00579155  jne      0x579199  ; -> 00579199
00579157  mov      byte ptr [rsp + 0x20], cl
0057915B  lea      rax, [r11 - 0x48]
0057915F  xor      r9d, r9d
00579162  mov      qword ptr [r11 - 0x40], rdx
00579166  mov      qword ptr [r11 - 0x38], r8
0057916A  lea      rdx, [rip + 0x2af]  ; -> 00579420
00579171  lea      r8, [r11 - 0x30]
00579175  mov      dword ptr [r11 - 0x30], r9d
00579179  mov      ecx, 0xe0
0057917E  mov      qword ptr [r11 - 0x28], rax
00579182  mov      qword ptr [r11 - 0x20], r9
00579186  call     0x244f50  ; -> 00244F50 fn
0057918B  mov      rcx, qword ptr [rip + 0x27305b6]  ; -> 02CA9748
00579192  mov      qword ptr [rcx + 0x118], rax
00579199  mov      rcx, qword ptr [rsp + 0x50]
0057919E  xor      rcx, rsp
005791A1  call     0x808c40  ; -> 00808C40 fn
005791A6  add      rsp, 0x68
005791AA  ret      
```

## 0057E610 (184 B, extent 0057E610-0057E6C8)

Page context: "age ids | layout-key families | constant files | effect registry | |---|---:|---|---|---|---|---|---| | '0057E4D0' | 19 / 15 | evidence | SaveWrite_OpenOperationController | 1,2,4,12 | — | — | — | | '0057E610' | 1 / 1 | child of a save / load UI (installer name) procedure | '0057EDB0' | — | — | — | — | | '0057E8D0' | 1 / 1 | evidence | SaveLoad_ControllerLifecycleHandler | 1,18 | — | — | — | | '0057EB30' | 1 / 1 | evidence | SaveLoad_Co"

```
0057E610  push     rbx
0057E612  sub      rsp, 0x20
0057E616  cmp      dword ptr [rdx], 1
0057E619  mov      rbx, rcx
0057E61C  je       0x57e628  ; -> 0057E628
0057E61E  add      rsp, 0x20
0057E622  pop      rbx
0057E623  jmp      0x5c5230  ; -> 005C5230 fn
0057E628  mov      rdx, qword ptr [rdx + 8]
0057E62C  mov      r9, rbx
0057E62F  mov      r8d, 7
0057E635  mov      rax, qword ptr [rdx]
0057E638  mov      qword ptr [rcx + 0xc0], rax
0057E63F  movzx    eax, byte ptr [rdx + 8]
0057E643  mov      byte ptr [rcx + 0xc8], al
0057E649  mov      qword ptr [rcx + 0xd0], 0
0057E654  add      rcx, 0x50
0057E658  mov      rdx, qword ptr [rdx + 0x10]
0057E65C  call     0x2432b0  ; -> 002432B0 fn
0057E661  movzx    edx, word ptr [rax + 8]
0057E665  movsx    ecx, word ptr [rax + 6]
0057E669  movzx    r9d, word ptr [rax + 0xa]
0057E66E  movzx    r8d, word ptr [rax + 4]
0057E673  mov      word ptr [rbx + 0x9a], cx
0057E67A  mov      rcx, rbx
0057E67D  mov      word ptr [rbx + 0x9c], dx
0057E684  mov      edx, 0x64
0057E689  mov      word ptr [rbx + 0x98], r8w
0057E691  mov      word ptr [rbx + 0x9e], r9w
0057E699  mov      word ptr [rbx + 0xca], r8w
0057E6A1  call     0x247930  ; -> 00247930 fn
0057E6A6  mov      rcx, qword ptr [rbx + 0xc0]
0057E6AD  mov      rdx, rbx
0057E6B0  call     0x244960  ; -> 00244960 fn
0057E6B5  xor      eax, eax
0057E6B7  mov      qword ptr [rbx + 0xd0], 0
0057E6C2  add      rsp, 0x20
0057E6C6  pop      rbx
0057E6C7  ret      
```

## 0057EDB0 (552 B, extent 0057EDB0-0057EFD8)

Page context: "|---|---|---|---|---|---| | '0057E4D0' | 19 / 15 | evidence | SaveWrite_OpenOperationController | 1,2,4,12 | — | — | — | | '0057E610' | 1 / 1 | child of a save / load UI (installer name) procedure | '0057EDB0' | — | — | — | — | | '0057E8D0' | 1 / 1 | evidence | SaveLoad_ControllerLifecycleHandler | 1,18 | — | — | — | | '0057EB30' | 1 / 1 | evidence | SaveLoad_ControllerLifecycleHandler | 1,18 | — | — | — | | '0057EDB0' | 2 / 2 | evidenc"

```
0057EDB0  push     rdi
0057EDB2  sub      rsp, 0x70
0057EDB6  mov      rax, qword ptr [rip + 0x19c5a73]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0057EDBD  xor      rax, rsp
0057EDC0  mov      qword ptr [rsp + 0x50], rax
0057EDC5  mov      rdi, rcx
0057EDC8  mov      ecx, dword ptr [rdx]
0057EDCA  sub      ecx, 1
0057EDCD  je       0x57ee17  ; -> 0057EE17
0057EDCF  sub      ecx, 0xe
0057EDD2  je       0x57edfb  ; -> 0057EDFB
0057EDD4  cmp      ecx, 3
0057EDD7  je       0x57edf4  ; -> 0057EDF4
0057EDD9  mov      rcx, rdi
0057EDDC  call     0x5c5230  ; -> 005C5230 fn
0057EDE1  mov      rcx, qword ptr [rsp + 0x50]
0057EDE6  xor      rcx, rsp
0057EDE9  call     0x808c40  ; -> 00808C40 fn
0057EDEE  add      rsp, 0x70
0057EDF2  pop      rdi
0057EDF3  ret      
0057EDF4  mov      edx, 0x12
0057EDF9  jmp      0x57ee00  ; -> 0057EE00
0057EDFB  mov      edx, 0xf
0057EE00  mov      rcx, qword ptr [rdi + 0xc0]
0057EE07  mov      r8d, 5
0057EE0D  call     0x247510  ; -> 00247510 fn
0057EE12  jmp      0x57efc3  ; -> 0057EFC3
0057EE17  mov      qword ptr [rsp + 0x90], rbx
0057EE1F  lea      rcx, [rdi + 0x50]
0057EE23  mov      qword ptr [rsp + 0x98], rbp
0057EE2B  mov      r9, rdi
0057EE2E  xor      ebp, ebp
0057EE30  mov      qword ptr [rsp + 0x68], rsi
0057EE35  mov      qword ptr [rsp + 0x60], r14
0057EE3A  mov      r14, qword ptr [rdx + 8]
0057EE3E  lea      r8d, [rbp + 2]
0057EE42  mov      rax, qword ptr [r14]
0057EE45  mov      qword ptr [rdi + 0xc0], rax
0057EE4C  mov      qword ptr [rdi + 0x100], rbp
0057EE53  mov      rdx, qword ptr [r14 + 8]
0057EE57  call     0x2432b0  ; -> 002432B0 fn
0057EE5C  movzx    edx, word ptr [rax + 8]
0057EE60  movsx    ecx, word ptr [rax + 6]
0057EE64  movzx    r8d, word ptr [rax + 0xa]
0057EE69  movzx    eax, word ptr [rax + 4]
0057EE6D  mov      word ptr [rdi + 0x9a], cx
0057EE74  mov      rcx, rdi
0057EE77  mov      word ptr [rdi + 0x9c], dx
0057EE7E  xor      edx, edx
0057EE80  mov      word ptr [rdi + 0x98], ax
0057EE87  mov      word ptr [rdi + 0x9e], r8w
0057EE8F  call     0x394700  ; -> 00394700 fn
0057EE94  lea      edx, [rbp + 0x63]
0057EE97  mov      rcx, rdi
0057EE9A  call     0x247930  ; -> 00247930 fn
0057EE9F  mov      rcx, qword ptr [rdi + 0xc0]
0057EEA6  mov      rdx, rdi
0057EEA9  call     0x246ad0  ; -> 00246AD0 fn
0057EEAE  lea      edx, [rbp + 1]
0057EEB1  mov      rcx, rdi
0057EEB4  call     0x394660  ; -> 00394660 fn
0057EEB9  test     rax, rax
0057EEBC  jne      0x57eec2  ; -> 0057EEC2
0057EEBE  mov      ebx, ebp
0057EEC0  jmp      0x57eec9  ; -> 0057EEC9
0057EEC2  mov      rax, qword ptr [rax + 0x60]
0057EEC6  mov      rbx, qword ptr [rax]
0057EEC9  mov      ecx, 0x875
0057EECE  call     0x2f9860  ; -> 002F9860 fn
0057EED3  xor      ecx, ecx
0057EED5  mov      qword ptr [rbx + 0x18], rax
0057EED9  call     0x20e620  ; -> 0020E620 fn
0057EEDE  mov      edx, 2
0057EEE3  mov      dword ptr [rbx + 0x20], eax
0057EEE6  mov      rcx, rdi
0057EEE9  call     0x394660  ; -> 00394660 fn
0057EEEE  mov      rbx, rax
0057EEF1  test     rax, rax
0057EEF4  jne      0x57eefb  ; -> 0057EEFB
0057EEF6  mov      rsi, rbp
0057EEF9  jmp      0x57ef03  ; -> 0057EF03
0057EEFB  mov      rax, qword ptr [rax + 0x60]
0057EEFF  mov      rsi, qword ptr [rax + 8]
0057EF03  mov      ecx, 0x876
0057EF08  call     0x2f9860  ; -> 002F9860 fn
0057EF0D  xor      ecx, ecx
0057EF0F  mov      qword ptr [rsi + 0x18], rax
0057EF13  call     0x20e620  ; -> 0020E620 fn
0057EF18  mov      dword ptr [rsi + 0x20], eax
0057EF1B  test     rbx, rbx
0057EF1E  jne      0x57ef25  ; -> 0057EF25
0057EF20  mov      rbx, rbp
0057EF23  jmp      0x57ef2d  ; -> 0057EF2D
0057EF25  mov      rax, qword ptr [rbx + 0x60]
0057EF29  mov      rbx, qword ptr [rax + 0x18]
0057EF2D  mov      ecx, 0x877
0057EF32  call     0x2f9860  ; -> 002F9860 fn
0057EF37  xor      ecx, ecx
0057EF39  mov      qword ptr [rbx + 0x18], rax
0057EF3D  call     0x20e620  ; -> 0020E620 fn
0057EF42  mov      dword ptr [rbx + 0x20], eax
0057EF45  xor      edx, edx
0057EF47  mov      rcx, rdi
0057EF4A  mov      qword ptr [rdi + 0x100], rbp
0057EF51  call     0x247870  ; -> 00247870 fn
0057EF56  mov      ebx, ebp
0057EF58  lea      rsi, [rdi + 0xc8]
0057EF5F  nop      
0057EF60  lea      rax, [rsp + 0x20]
0057EF65  mov      dword ptr [rsp + 0x38], ebp
0057EF69  mov      qword ptr [rsp + 0x40], rax
0057EF6E  lea      r8, [rsp + 0x38]
0057EF73  mov      rax, qword ptr [r14 + 8]
0057EF77  lea      rdx, [rip - 0x96e]  ; -> 0057E610
0057EF7E  mov      ecx, 0xd8
0057EF83  mov      qword ptr [rsp + 0x30], rax
0057EF88  mov      qword ptr [rsp + 0x48], rbp
0057EF8D  mov      qword ptr [rsp + 0x20], rdi
0057EF92  mov      byte ptr [rsp + 0x28], bl
0057EF96  call     0x244f50  ; -> 00244F50 fn
0057EF9B  inc      ebx
0057EF9D  mov      qword ptr [rsi], rax
0057EFA0  lea      rsi, [rsi + 8]
0057EFA4  cmp      ebx, 7
0057EFA7  jl       0x57ef60  ; -> 0057EF60
0057EFA9  mov      r14, qword ptr [rsp + 0x60]
0057EFAE  mov      rsi, qword ptr [rsp + 0x68]
0057EFB3  mov      rbp, qword ptr [rsp + 0x98]
0057EFBB  mov      rbx, qword ptr [rsp + 0x90]
0057EFC3  xor      eax, eax
0057EFC5  mov      rcx, qword ptr [rsp + 0x50]
0057EFCA  xor      rcx, rsp
0057EFCD  call     0x808c40  ; -> 00808C40 fn
0057EFD2  add      rsp, 0x70
0057EFD6  pop      rdi
0057EFD7  ret      
```

## 0057F6B0 (276 B, extent 0057F6B0-0057F7C4)

Page context: " sales, and test and equip items through that layer's own bodies.  **Save_Load_Settings — CLIENT and SERVICE (19 edges).** The save/load procedures call into that layer: '0057F360' calls '0057EA40', '0057F6B0', '005812B0', '005813E0', '005817D0' and '00581860'; the slot screen '0057FE80' calls 'SaveImage_GetActiveRuntimeBuffer' ('002EF640'), '00580A80', '00580B40', '00580CD0' and 'SaveLoad_ControllerTransitionStateMachine' ('00580EB0');"

```
0057F6B0  push     rbx
0057F6B2  sub      rsp, 0xd0
0057F6B9  mov      rax, qword ptr [rip + 0x19c5170]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0057F6C0  xor      rax, rsp
0057F6C3  mov      qword ptr [rsp + 0xc0], rax
0057F6CB  cmp      dword ptr [rdx + 8], 1
0057F6CF  mov      rbx, rcx
0057F6D2  ja       0x57f774  ; -> 0057F774
0057F6D8  mov      rcx, qword ptr [rip + 0x272a2e1]  ; -> 02CA99C0
0057F6DF  test     rcx, rcx
0057F6E2  je       0x57f706  ; -> 0057F706
0057F6E4  lea      rax, [rip - 0xbb]  ; -> 0057F630
0057F6EB  mov      dword ptr [rsp + 0x20], 1
0057F6F3  lea      rdx, [rsp + 0x20]
0057F6F8  mov      qword ptr [rsp + 0x28], rax
0057F6FD  mov      dword ptr [rsp + 0x30], ebx
0057F701  call     0x582540  ; -> 00582540 fn
0057F706  mov      edx, 0x40
0057F70B  lea      rcx, [rsp + 0x80]
0057F713  call     0x393630  ; -> 00393630 fn
0057F718  mov      rcx, qword ptr [rip + 0x272a2a1]  ; -> 02CA99C0
0057F71F  mov      r8, qword ptr [rbx + 0xd8]
0057F726  test     rcx, rcx
0057F729  je       0x57f76b  ; -> 0057F76B
0057F72B  mov      dword ptr [rsp + 0x20], 0xa
0057F733  xor      edx, edx
0057F735  nop      word ptr [rax + rax]
0057F740  movzx    eax, byte ptr [rsp + rdx + 0x80]
0057F748  mov      byte ptr [rsp + rdx + 0x28], al
0057F74C  lea      rdx, [rdx + 1]
0057F750  test     al, al
0057F752  jne      0x57f740  ; -> 0057F740
0057F754  lea      rdx, [rsp + 0x20]
0057F759  mov      qword ptr [rsp + 0x68], r8
0057F75E  mov      dword ptr [rsp + 0x70], 0xa0
0057F766  call     0x582540  ; -> 00582540 fn
0057F76B  mov      byte ptr [rbx + 0xcc], 2
0057F772  jmp      0x57f7ab  ; -> 0057F7AB
0057F774  mov      rax, qword ptr [rip + 0x272a245]  ; -> 02CA99C0
0057F77B  mov      dword ptr [rcx + 0xe0], 0xa
0057F785  test     rax, rax
0057F788  jne      0x57f78e  ; -> 0057F78E
0057F78A  mov      al, 0xff
0057F78C  jmp      0x57f795  ; -> 0057F795
0057F78E  movzx    eax, byte ptr [rax + 0x39a]
0057F795  mov      byte ptr [rcx + 0xe4], al
0057F79B  mov      eax, dword ptr [rdx + 8]
0057F79E  mov      dword ptr [rcx + 0xe8], eax
0057F7A4  mov      byte ptr [rcx + 0xcc], 4
0057F7AB  mov      rcx, qword ptr [rsp + 0xc0]
0057F7B3  xor      rcx, rsp
0057F7B6  call     0x808c40  ; -> 00808C40 fn
0057F7BB  add      rsp, 0xd0
0057F7C2  pop      rbx
0057F7C3  ret      
```

## 005812B0 (85 B, extent 005812B0-00581305)

Page context: "test and equip items through that layer's own bodies.  **Save_Load_Settings — CLIENT and SERVICE (19 edges).** The save/load procedures call into that layer: '0057F360' calls '0057EA40', '0057F6B0', '005812B0', '005813E0', '005817D0' and '00581860'; the slot screen '0057FE80' calls 'SaveImage_GetActiveRuntimeBuffer' ('002EF640'), '00580A80', '00580B40', '00580CD0' and 'SaveLoad_ControllerTransitionStateMachine' ('00580EB0'); and 'SaveWr"

```
005812B0  push     rbx
005812B2  sub      rsp, 0x20
005812B6  mov      rbx, qword ptr [rip + 0x272870b]  ; -> 02CA99C8
005812BD  test     rbx, rbx
005812C0  je       0x5812ff  ; -> 005812FF
005812C2  mov      rcx, qword ptr [rbx + 0xf0]
005812C9  mov      qword ptr [rsp + 0x30], rdi
005812CE  xor      edi, edi
005812D0  mov      qword ptr [rbx + 0xd4], 0xffff
005812DB  mov      qword ptr [rbx + 0xdc], rdi
005812E2  mov      dword ptr [rbx + 0xc8], edi
005812E8  test     rcx, rcx
005812EB  je       0x5812f4  ; -> 005812F4
005812ED  xor      edx, edx
005812EF  call     0x225580  ; -> 00225580 fn
005812F4  mov      dword ptr [rbx + 0xfc], edi
005812FA  mov      rdi, qword ptr [rsp + 0x30]
005812FF  add      rsp, 0x20
00581303  pop      rbx
00581304  ret      
```
