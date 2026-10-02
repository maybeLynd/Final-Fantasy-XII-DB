# F-interior pack: `08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md`

Generated 2026-10-02 08:46 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/the-battle-stats-record-field-map.json`.

Functions: 3. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 7903502f7	FABLE: pass-22 debt - crossing sections on 94 pages (FABLE's group; 12 overlay-carrier pages routed ; 934f4edf9	FABLE: PKG-GP-EXP-LEVEL-UP E4 - the four f32 base stats a level grows are, in order, Strength, Magic; inbox mentions: FABLE.md, SWE2-AUDIT-SPEC.md). OPUS read these before packing.

## 003478A0 (195 B, extent 003478A0-00347963)

Page context: "rs call and that other gameplay bodies call too; none of them owns a stats field.  **Script_VM_Native_Bridge — CLIENT (34 edges).** 23 verb bodies call '00265020', among them '0033FD60', '00345180', '003478A0', '0050E060' and '0050F6E0'; '00344740' and '003509E0' call '00233D70'; '0050F360' calls '00235A70'; '0050FAF0' calls '002FAFD0'; '00342230' calls '00328BD0'; '00351A40' calls '00328FB0' and pops its argument with 'VMValueStack_Pop"

```
003478A0  mov      qword ptr [rsp + 0x18], rbx
003478A5  push     rdi
003478A6  sub      rsp, 0x60
003478AA  mov      rax, qword ptr [rip + 0x1bfcf7f]  ; -> 01F44830 [u64 0x00002B992DDFA232]
003478B1  xor      rax, rsp
003478B4  mov      qword ptr [rsp + 0x50], rax
003478B9  mov      rax, rdx
003478BC  lea      r8, [rsp + 0x24]
003478C1  mov      rbx, r9
003478C4  lea      rdx, [rsp + 0x20]
003478C9  mov      rdi, rcx
003478CC  lea      r9, [rsp + 0x28]
003478D1  mov      rcx, rax
003478D4  call     0x265020  ; -> 00265020 fn
003478D9  mov      rcx, rbx
003478DC  mov      dword ptr [rsp + 0x24], 0
003478E4  mov      dword ptr [rsp + 0x44], 0
003478EC  mov      dword ptr [rsp + 0x34], 0
003478F4  call     0x267db0  ; -> 00267DB0 fn
003478F9  mov      rcx, rbx
003478FC  movss    dword ptr [rsp + 0x38], xmm0
00347902  call     0x267db0  ; -> 00267DB0 fn
00347907  mov      rcx, rbx
0034790A  movss    dword ptr [rsp + 0x30], xmm0
00347910  call     0x267db0  ; -> 00267DB0 fn
00347915  mov      rcx, rbx
00347918  movss    dword ptr [rsp + 0x48], xmm0
0034791E  call     0x267db0  ; -> 00267DB0 fn
00347923  lea      r8, [rsp + 0x20]
00347928  movss    dword ptr [rsp + 0x40], xmm0
0034792E  lea      rdx, [rsp + 0x30]
00347933  lea      rcx, [rsp + 0x40]
00347938  call     0x3a1c90  ; -> 003A1C90 fn
0034793D  movaps   xmm1, xmm0
00347940  mov      rcx, rdi
00347943  call     0x26b4c0  ; -> 0026B4C0 fn
00347948  mov      rcx, qword ptr [rsp + 0x50]
0034794D  xor      rcx, rsp
00347950  call     0x808c40  ; -> 00808C40 fn
00347955  mov      rbx, qword ptr [rsp + 0x80]
0034795D  add      rsp, 0x60
00347961  pop      rdi
00347962  ret      
```

## 003509E0 (253 B, extent 003509E0-00350ADD)

Page context: "of them owns a stats field.  **Script_VM_Native_Bridge — CLIENT (34 edges).** 23 verb bodies call '00265020', among them '0033FD60', '00345180', '003478A0', '0050E060' and '0050F6E0'; '00344740' and '003509E0' call '00233D70'; '0050F360' calls '00235A70'; '0050FAF0' calls '002FAFD0'; '00342230' calls '00328BD0'; '00351A40' calls '00328FB0' and pops its argument with 'VMValueStack_PopInt32CoerceFloat32' '00267E10'; and '00344740', '00352"

```
003509E0  push     rbx
003509E2  push     rbp
003509E3  push     rdi
003509E4  push     r12
003509E6  push     r13
003509E8  push     r14
003509EA  push     r15
003509EC  sub      rsp, 0x50
003509F0  mov      rax, qword ptr [rip + 0x1bf3e39]  ; -> 01F44830 [u64 0x00002B992DDFA232]
003509F7  xor      rax, rsp
003509FA  mov      qword ptr [rsp + 0x40], rax
003509FF  mov      r15, rcx
00350A02  mov      qword ptr [rsp + 0x20], r8
00350A07  mov      rcx, r9
00350A0A  mov      qword ptr [rsp + 0x28], rdx
00350A0F  mov      rbp, r9
00350A12  xor      r14d, r14d
00350A15  call     0x267e10  ; -> 00267E10 fn
00350A1A  lea      edx, [r14 + 4]
00350A1E  mov      r13d, eax
00350A21  lea      rcx, [rsp + 0x30]
00350A26  call     0x31b510  ; -> 0031B510 fn
00350A2B  xor      edx, edx
00350A2D  movsxd   r12, eax
00350A30  mov      rcx, r15
00350A33  call     0x26b4e0  ; -> 0026B4E0 fn
00350A38  mov      edi, r14d
00350A3B  mov      ebx, r14d
00350A3E  test     r12, r12
00350A41  jle      0x350ab5  ; -> 00350AB5
00350A43  mov      qword ptr [rsp + 0xa0], rsi
00350A4B  nop      dword ptr [rax + rax]
00350A50  cmp      dword ptr [rsp + rbx*4 + 0x30], r13d
00350A55  jne      0x350aa3  ; -> 00350AA3
00350A57  mov      ecx, edi
00350A59  call     0x263750  ; -> 00263750 fn
00350A5E  mov      rsi, rax
00350A61  test     rax, rax
00350A64  je       0x350aa3  ; -> 00350AA3
00350A66  mov      rcx, rax
00350A69  call     0x2373a0  ; -> 002373A0 fn
00350A6E  test     eax, eax
00350A70  je       0x350a7e  ; -> 00350A7E
00350A72  mov      rcx, rsi
00350A75  call     0x233d70  ; -> 00233D70 fn
00350A7A  test     eax, eax
00350A7C  je       0x350aa3  ; -> 00350AA3
00350A7E  mov      edx, edi
00350A80  mov      rcx, rbp
00350A83  call     0x267f90  ; -> 00267F90 fn
00350A88  mov      r8, qword ptr [rsp + 0x20]
00350A8D  mov      r9, rbp
00350A90  mov      rdx, qword ptr [rsp + 0x28]
00350A95  mov      rcx, r15
00350A98  call     0x352fa0  ; -> 00352FA0 fn
00350A9D  mov      r14d, 1
00350AA3  inc      edi
00350AA5  inc      rbx
00350AA8  cmp      rbx, r12
00350AAB  jl       0x350a50  ; -> 00350A50
00350AAD  mov      rsi, qword ptr [rsp + 0xa0]
00350AB5  mov      edx, r14d
00350AB8  mov      rcx, r15
00350ABB  call     0x26b4e0  ; -> 0026B4E0 fn
00350AC0  mov      rcx, qword ptr [rsp + 0x40]
00350AC5  xor      rcx, rsp
00350AC8  call     0x808c40  ; -> 00808C40 fn
00350ACD  add      rsp, 0x50
00350AD1  pop      r15
00350AD3  pop      r14
00350AD5  pop      r13
00350AD7  pop      r12
00350AD9  pop      rdi
00350ADA  pop      rbp
00350ADB  pop      rbx
00350ADC  ret      
```

## 00560210 (1021 B, extent 00560210-0056060D)

Page context: "UnitActionAvailability' '00306480' and '00322360', and '00322A80' also calls '00322360'; 12 licence-board screen bodies from '00557B90' to '005618E0' (19 edges; among them the node check '005587E0', '00560210' and '005618E0') call the board-selector getters 'BattleStats_GetLicenseBoardSelectorB' '00323630', 'BattleStats_GetLicenseBoardSelectorA' '00323670' and 'BattleStats_GetActiveLicenseBoardSelector' '003236B0'; '003C5130' calls '002"

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
