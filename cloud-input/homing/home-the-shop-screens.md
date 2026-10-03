# Homing pack: `16-UI/Shop-Screens/the-shop-screens.md`

Generated 2026-10-03 06:31 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-shop-screens.json`.

Bodies: 5. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00243580 (49 B, extent 00243580-002435B1)

Entered from (direct sites whose caller this page cites): `003FCFE0` + 0x4D (call; `003FCFE0` is cited on this page); `003FDDE0` + 0x4D (call; `003FDDE0` is cited on this page)
Other direct sites: `00563560` + 0x2F (call); `005637D0` + 0x2F (call); `005639D0` + 0x2F (call); `00563C00` + 0x29 (call); `00568AA0` + 0x1A (call); `00568BB0` + 0x41 (call)

Host context: "xc1'; 0xf stores word '0x507' at '+0xc0' and byte 3 at '+0xc2'; all these return 0, and any other value tail-jumps to '005C5230(rcx)' | '003C974F', '003C9819', '003C96EC', '003C9611', '003C95F4' | | '003FCFE0' | 494 B | takes 'D' = qword '+8' of '[rdx+0x10]' and 's' = '002DD7E0(0)'; when qword 'rcx+0xe0' is null it calls '00243580(rdx, 0, byte rcx+0x180)', sets bit '0x1' of 'D' dword '+8', calls '002B4090(0x80, 02B5F220, 002F9860(0x867)" / "rcx+0x10]', or returns 0 when 'rcx', that qword or the pointer is null; 0x12 returns 0; any other value tail-jumps to '005C5230(rcx)' | '003FD1E8', '003FD216', '003FD28F', '003FD29D', '003FD2A7' | | '003FDDE0' | 508 B | takes 'D' = qword '+8' of '[rdx+0x10]' and 's' = '002DD7E0(0)'; when qword 'rcx+0xe0' is null it calls '00243580(rdx, 0, byte rcx+0x180)', sets bit '0x1' of 'D' dword '+8', calls '002B4090(0x80, 02B5F220, 002F9860(0x867)"

```
00243580  xor      edx, edx
00243582  mov      r9, rcx
00243585  test     dword ptr [rcx], 0x3fffc
0024358B  jbe      0x2435b0  ; -> 002435B0
0024358D  mov      r8d, edx
00243590  mov      rax, qword ptr [r9 + 0x10]
00243594  lea      r8, [r8 + 8]
00243598  inc      edx
0024359A  mov      rcx, qword ptr [r8 + rax - 8]
0024359F  and      dword ptr [rcx + 8], 0xfffffffe
002435A3  mov      eax, dword ptr [r9]
002435A6  shr      eax, 2
002435A9  movzx    eax, ax
002435AC  cmp      edx, eax
002435AE  jb       0x243590  ; -> 00243590
002435B0  ret      
```

## 0027F030 (282 B, extent 0027F030-0027F14A)

Entered from (direct sites whose caller this page cites): `003FCFE0` + 0xF4 (call; `003FCFE0` is cited on this page); `003FDDE0` + 0x102 (call; `003FDDE0` is cited on this page)
Other direct sites: `003FCA70` + 0x48 (call)

Host context: "xc1'; 0xf stores word '0x507' at '+0xc0' and byte 3 at '+0xc2'; all these return 0, and any other value tail-jumps to '005C5230(rcx)' | '003C974F', '003C9819', '003C96EC', '003C9611', '003C95F4' | | '003FCFE0' | 494 B | takes 'D' = qword '+8' of '[rdx+0x10]' and 's' = '002DD7E0(0)'; when qword 'rcx+0xe0' is null it calls '00243580(rdx, 0, byte rcx+0x180)', sets bit '0x1' of 'D' dword '+8', calls '002B4090(0x80, 02B5F220, 002F9860(0x867)" / "rcx+0x10]', or returns 0 when 'rcx', that qword or the pointer is null; 0x12 returns 0; any other value tail-jumps to '005C5230(rcx)' | '003FD1E8', '003FD216', '003FD28F', '003FD29D', '003FD2A7' | | '003FDDE0' | 508 B | takes 'D' = qword '+8' of '[rdx+0x10]' and 's' = '002DD7E0(0)'; when qword 'rcx+0xe0' is null it calls '00243580(rdx, 0, byte rcx+0x180)', sets bit '0x1' of 'D' dword '+8', calls '002B4090(0x80, 02B5F220, 002F9860(0x867)"

```
0027F030  push     rdi
0027F032  sub      rsp, 0x30
0027F036  mov      qword ptr [rsp + 0x40], rbx
0027F03B  xor      edi, edi
0027F03D  mov      qword ptr [rsp + 0x48], rbp
0027F042  mov      ebp, r9d
0027F045  mov      qword ptr [rsp + 0x28], r12
0027F04A  mov      ebx, r8d
0027F04D  mov      qword ptr [rsp + 0x20], r15
0027F052  mov      r15d, edx
0027F055  mov      r12d, ecx
0027F058  test     r9d, r9d
0027F05B  jne      0x27f09d  ; -> 0027F09D
0027F05D  cmp      dword ptr [rsp + 0x60], 1
0027F062  je       0x27f112  ; -> 0027F112
0027F068  mov      ecx, ebx
0027F06A  call     0x2cca10  ; -> 002CCA10 fn
0027F06F  test     eax, eax
0027F071  je       0x27f112  ; -> 0027F112
0027F077  mov      rbx, qword ptr [rip + 0x1e1bbb2]  ; -> 0209AC30
0027F07E  mov      ecx, r15d
0027F081  call     0x2ca430  ; -> 002CA430 fn
0027F086  movzx    edx, word ptr [rbx + 0xd68]
0027F08D  mov      ecx, eax
0027F08F  call     0x2cca40  ; -> 002CCA40 fn
0027F094  test     eax, eax
0027F096  jne      0x27f112  ; -> 0027F112
0027F098  lea      edi, [rbp + 4]
0027F09B  jmp      0x27f112  ; -> 0027F112
0027F09D  cmp      ebp, 1
0027F0A0  jne      0x27f112  ; -> 0027F112
0027F0A2  mov      rax, qword ptr [rip + 0x1e1bb87]  ; -> 0209AC30
0027F0A9  mov      ecx, ebx
0027F0AB  mov      qword ptr [rsp + 0x50], rsi
0027F0B0  movzx    esi, byte ptr [rax + 0xd6b]
0027F0B7  call     0x2cca00  ; -> 002CCA00 fn
0027F0BC  test     eax, eax
0027F0BE  je       0x27f10d  ; -> 0027F10D
0027F0C0  mov      ecx, esi
0027F0C2  call     0x2cca00  ; -> 002CCA00 fn
0027F0C7  test     eax, eax
0027F0C9  je       0x27f0d9  ; -> 0027F0D9
0027F0CB  cmp      ebx, esi
0027F0CD  mov      eax, 4
0027F0D2  cmove    eax, edi
0027F0D5  mov      edi, eax
0027F0D7  jmp      0x27f10d  ; -> 0027F10D
0027F0D9  mov      ecx, esi
0027F0DB  call     0x2cca30  ; -> 002CCA30 fn
0027F0E0  test     eax, eax
0027F0E2  jne      0x27f108  ; -> 0027F108
0027F0E4  mov      rax, qword ptr [rip + 0x1e1bb45]  ; -> 0209AC30
0027F0EB  movzx    ecx, word ptr [rax + 0xd48]
0027F0F2  call     0x2ca430  ; -> 002CA430 fn
0027F0F7  mov      ecx, eax
0027F0F9  mov      esi, eax
0027F0FB  call     0x2cca00  ; -> 002CCA00 fn
0027F100  test     eax, eax
0027F102  je       0x27f108  ; -> 0027F108
0027F104  cmp      ebx, esi
0027F106  je       0x27f10d  ; -> 0027F10D
0027F108  mov      edi, 4
0027F10D  mov      rsi, qword ptr [rsp + 0x50]
0027F112  mov      r9d, dword ptr [rsp + 0x60]
0027F117  mov      r8d, ebp
0027F11A  movzx    edx, r15w
0027F11E  movzx    ecx, r12b
0027F122  call     0x317b70  ; -> 00317B70 fn
0027F127  mov      r15, qword ptr [rsp + 0x20]
0027F12C  mov      r12, qword ptr [rsp + 0x28]
0027F131  mov      rbp, qword ptr [rsp + 0x48]
0027F136  mov      rbx, qword ptr [rsp + 0x40]
0027F13B  test     eax, eax
0027F13D  jne      0x27f142  ; -> 0027F142
0027F13F  or       edi, 1
0027F142  mov      eax, edi
0027F144  add      rsp, 0x30
0027F148  pop      rdi
0027F149  ret      
```

## 003FCAD0 (495 B, extent 003FCAD0-003FCCBF)

Entered from (direct sites whose caller this page cites): `003FCFE0` + 0x1CC (call; `003FCFE0` is cited on this page); `003FDDE0` + 0x1D5 (call; `003FDDE0` is cited on this page)
Other direct sites: `00563560` + 0x169 (call); `005639D0` + 0x117 (call)

Host context: "xc1'; 0xf stores word '0x507' at '+0xc0' and byte 3 at '+0xc2'; all these return 0, and any other value tail-jumps to '005C5230(rcx)' | '003C974F', '003C9819', '003C96EC', '003C9611', '003C95F4' | | '003FCFE0' | 494 B | takes 'D' = qword '+8' of '[rdx+0x10]' and 's' = '002DD7E0(0)'; when qword 'rcx+0xe0' is null it calls '00243580(rdx, 0, byte rcx+0x180)', sets bit '0x1' of 'D' dword '+8', calls '002B4090(0x80, 02B5F220, 002F9860(0x867)" / "rcx+0x10]', or returns 0 when 'rcx', that qword or the pointer is null; 0x12 returns 0; any other value tail-jumps to '005C5230(rcx)' | '003FD1E8', '003FD216', '003FD28F', '003FD29D', '003FD2A7' | | '003FDDE0' | 508 B | takes 'D' = qword '+8' of '[rdx+0x10]' and 's' = '002DD7E0(0)'; when qword 'rcx+0xe0' is null it calls '00243580(rdx, 0, byte rcx+0x180)', sets bit '0x1' of 'D' dword '+8', calls '002B4090(0x80, 02B5F220, 002F9860(0x867)"

```
003FCAD0  mov      qword ptr [rsp + 8], rcx
003FCAD5  push     rbx
003FCAD6  push     r12
003FCAD8  push     r13
003FCADA  push     r15
003FCADC  sub      rsp, 0x28
003FCAE0  movsxd   r15, r8d
003FCAE3  mov      r13, rdx
003FCAE6  movsxd   r12, r9d
003FCAE9  mov      rbx, rcx
003FCAEC  mov      r8, r15
003FCAEF  cmp      r15, r12
003FCAF2  jg       0x3fcb24  ; -> 003FCB24
003FCAF4  mov      r9d, 7
003FCAFA  nop      word ptr [rax + rax]
003FCB00  mov      rax, qword ptr [rbx + 0x10]
003FCB04  mov      rdx, qword ptr [rax + r8*8]
003FCB08  inc      r8
003FCB0B  mov      rax, qword ptr [rdx + 0x20]
003FCB0F  movzx    ecx, byte ptr [rax + 0x3f]
003FCB13  mov      word ptr [rdx + 0xa], r9w
003FCB18  and      dword ptr [rdx + 8], 0xfffffffe
003FCB1C  mov      byte ptr [rdx + 0x39], cl
003FCB1F  cmp      r8, r12
003FCB22  jle      0x3fcb00  ; -> 003FCB00
003FCB24  mov      eax, 0xffff
003FCB29  cmp      word ptr [r13 + 8], ax
003FCB2E  je       0x3fcc0f  ; -> 003FCC0F
003FCB34  mov      qword ptr [rsp + 0x58], rbp
003FCB39  xor      ebp, ebp
003FCB3B  mov      qword ptr [rsp + 0x60], rsi
003FCB40  mov      qword ptr [rsp + 0x20], r14
003FCB45  mov      qword ptr [rsp + 0x68], rdi
003FCB4A  lea      r14d, [rbp + 8]
003FCB4E  nop      
003FCB50  mov      ecx, ebp
003FCB52  call     0x282df0  ; -> 00282DF0 fn
003FCB57  mov      rcx, rax
003FCB5A  mov      rsi, rax
003FCB5D  call     0x282fa0  ; -> 00282FA0 fn
003FCB62  test     eax, eax
003FCB64  je       0x3fcbed  ; -> 003FCBED
003FCB6A  mov      rcx, qword ptr [rbx + 0x10]
003FCB6E  cmp      r15, r12
003FCB71  mov      rdx, r12
003FCB74  cmovle   rdx, r15
003FCB78  mov      rdi, qword ptr [rcx + rdx*8]
003FCB7C  mov      ecx, 1
003FCB81  or       dword ptr [rdi + 8], 1
003FCB85  movzx    edx, word ptr [r13 + 8]
003FCB8A  shl      edx, 0x10
003FCB8D  call     0x35d330  ; -> 0035D330 fn
003FCB92  movzx    ecx, word ptr [r13 + 8]
003FCB97  mov      rdx, rsi
003FCB9A  mov      rbx, rax
003FCB9D  call     0x282f10  ; -> 00282F10 fn
003FCBA2  mov      ecx, dword ptr [rbx]
003FCBA4  cmp      ecx, 6
003FCBA7  je       0x3fcc1b  ; -> 003FCC1B
003FCBA9  add      ecx, -8
003FCBAC  cmp      ecx, 1
003FCBAF  ja       0x3fcbe8  ; -> 003FCBE8
003FCBB1  mov      rcx, qword ptr [rdi + 0x20]
003FCBB5  movzx    edx, byte ptr [rcx + 0x47]
003FCBB9  mov      byte ptr [rdi + 0x39], dl
003FCBBC  mov      word ptr [rdi + 0xa], r14w
003FCBC1  test     al, al
003FCBC3  je       0x3fcbe8  ; -> 003FCBE8
003FCBC5  movsx    ecx, word ptr [rsi + 0x60]
003FCBC9  mov      edx, 5
003FCBCE  call     0x2c9b30  ; -> 002C9B30 fn
003FCBD3  mov      rcx, qword ptr [rdi + 0x20]
003FCBD7  inc      eax
003FCBD9  movsxd   rdx, eax
003FCBDC  movzx    edx, byte ptr [rcx + rdx*8 + 7]
003FCBE1  mov      byte ptr [rdi + 0x39], dl
003FCBE4  mov      word ptr [rdi + 0xa], ax
003FCBE8  mov      rbx, qword ptr [rsp + 0x50]
003FCBED  inc      ebp
003FCBEF  inc      r15
003FCBF2  cmp      ebp, 9
003FCBF5  jl       0x3fcb50  ; -> 003FCB50
003FCBFB  mov      r14, qword ptr [rsp + 0x20]
003FCC00  mov      rdi, qword ptr [rsp + 0x68]
003FCC05  mov      rsi, qword ptr [rsp + 0x60]
003FCC0A  mov      rbp, qword ptr [rsp + 0x58]
003FCC0F  add      rsp, 0x28
003FCC13  pop      r15
003FCC15  pop      r13
003FCC17  pop      r12
003FCC19  pop      rbx
003FCC1A  ret      
003FCC1B  test     al, al
003FCC1D  je       0x3fcc88  ; -> 003FCC88
003FCC1F  movzx    ecx, byte ptr [rsi + 0x60]
003FCC23  call     0x323670  ; -> 00323670 fn
003FCC28  movzx    ecx, byte ptr [rsi + 0x60]
003FCC2C  movzx    ebx, al
003FCC2F  call     0x323630  ; -> 00323630 fn
003FCC34  movzx    edx, word ptr [r13 + 8]
003FCC39  movzx    ecx, bl
003FCC3C  movzx    r14d, al
003FCC40  call     0x3fc900  ; -> 003FC900 fn
003FCC45  test     eax, eax
003FCC47  jne      0x3fcc70  ; -> 003FCC70
003FCC49  movzx    edx, word ptr [r13 + 8]
003FCC4E  movzx    ecx, r14b
003FCC52  call     0x3fc900  ; -> 003FC900 fn
003FCC57  test     eax, eax
003FCC59  jne      0x3fcc70  ; -> 003FCC70
003FCC5B  mov      rax, qword ptr [rdi + 0x20]
003FCC5F  mov      r14d, 8
003FCC65  movzx    ecx, byte ptr [rax + 0x47]
003FCC69  mov      word ptr [rdi + 0xa], r14w
003FCC6E  jmp      0x3fcc85  ; -> 003FCC85
003FCC70  mov      rax, qword ptr [rdi + 0x20]
003FCC74  movzx    ecx, byte ptr [rax + 0x4f]
003FCC78  mov      eax, 9
003FCC7D  mov      word ptr [rdi + 0xa], ax
003FCC81  lea      r14d, [rax - 1]
003FCC85  mov      byte ptr [rdi + 0x39], cl
003FCC88  movzx    r8d, word ptr [r13 + 8]
003FCC8D  lea      rax, [rsi + 0x98]
003FCC94  xor      edx, edx
003FCC96  nop      word ptr [rax + rax]
003FCCA0  movzx    ecx, word ptr [rax + 2]
003FCCA4  cmp      r8d, ecx
003FCCA7  je       0x3fcbc5  ; -> 003FCBC5
003FCCAD  inc      rdx
003FCCB0  add      rax, 4
003FCCB4  cmp      rdx, 5
003FCCB8  jl       0x3fcca0  ; -> 003FCCA0
003FCCBA  jmp      0x3fcbe8  ; -> 003FCBE8
```

## 0057A960 (22 B, extent 0057A960-0057A976)

Entered from (direct sites whose caller this page cites): `0056DD00` + 0x9 (call; `0056DD00` is cited on this page)
Other direct sites: none

Host context: " of one step | | 10 | '0056E259' | '0056DED0' — directional-input helper | | 12 | '0056E269' | '00293110', '00244F00' (mark-delete), '0056E5D0' | | 14 | '0056E212' | '002470D0' | | 15 | '0056E322' | '0056DD00' gate, then '00247510(self+0x188, 0xF, (self+0x194)>>2 & 1)' ('0056E322'–'0056E355') | | 18 | '0056E374' | '00247510', '003697F0' — deferred free | | 19 | '0056E222' | '0056E5D0' | | 20 | '0056E356' | '0056DD00' gate, then '002CFCF"

```
0057A960  xor      eax, eax
0057A962  cmp      qword ptr [rip + 0x272ee27], rax  ; -> 02CA9790
0057A969  je       0x57a975  ; -> 0057A975
0057A96B  cmp      qword ptr [rip + 0x272ee2e], rax  ; -> 02CA97A0
0057A972  setne    al
0057A975  ret      
```

## 0057FA30 (197 B, extent 0057FA30-0057FAF5)

Entered from (direct sites whose caller this page cites): `0057F8C0` + 0xB3 (call; `0057F8C0` is cited on this page)
Other direct sites: none

Host context: "alls '0016D6A0' with 'rcx' unchanged and stores dword 1 at '+0xc0'; these return 0, and any other value tail-jumps to '005C5230(rcx)' | '0053EF1E', '0053EF4C', '0053EF73', '0053EEFC', '0053EED8' | | '0057F8C0' | 357 B | takes 'k' = byte '[rcx + r9d + 0xef]'; when bit '0x1' of byte 'rcx+0xe0' is clear it calls '003BB3E0(k)' and, when that record's dword '+0' is 2, calls '0057FB00(rdx, r8, qword rcx+0x1c0 + k*0xa0)'; otherwise (bit set, u"

```
0057FA30  mov      qword ptr [rsp + 8], rbx
0057FA35  push     rdi
0057FA36  sub      rsp, 0x20
0057FA3A  xor      edx, edx
0057FA3C  mov      rdi, r8
0057FA3F  mov      rbx, rcx
0057FA42  call     0x393190  ; -> 00393190 fn
0057FA47  mov      rax, qword ptr [rbx + 0x10]
0057FA4B  lea      r9, [rip + 0x7a445a]  ; -> 00D23EAC
0057FA52  mov      rdx, qword ptr [rax + 0xd8]
0057FA59  and      dword ptr [rdx + 8], 0xfffffffe
0057FA5D  mov      rax, qword ptr [rbx + 0x10]
0057FA61  mov      rdx, qword ptr [rax + 0xb0]
0057FA68  or       dword ptr [rdx + 8], 1
0057FA6C  xor      r8d, r8d
0057FA6F  nop      
0057FA70  movzx    ecx, byte ptr [r9]
0057FA74  lea      r9, [r9 + 1]
0057FA78  mov      rax, qword ptr [rbx + 0x10]
0057FA7C  inc      r8d
0057FA7F  mov      rdx, qword ptr [rax + rcx*8]
0057FA83  or       dword ptr [rdx + 8], 1
0057FA87  cmp      r8d, 7
0057FA8B  jb       0x57fa70  ; -> 0057FA70
0057FA8D  mov      rax, qword ptr [rbx + 0x10]
0057FA91  mov      rcx, qword ptr [rax + 0xd0]
0057FA98  and      dword ptr [rcx + 8], 0xfffffffe
0057FA9C  mov      ecx, dword ptr [rdi]
0057FA9E  sub      ecx, 3
0057FAA1  je       0x57fac4  ; -> 0057FAC4
0057FAA3  sub      ecx, 1
0057FAA6  je       0x57fabd  ; -> 0057FABD
0057FAA8  cmp      ecx, 1
0057FAAB  je       0x57fab6  ; -> 0057FAB6
0057FAAD  lea      rcx, [rip + 0x176bb84]  ; -> 01CEB638
0057FAB4  jmp      0x57fad1  ; -> 0057FAD1
0057FAB6  mov      ecx, 0x872
0057FABB  jmp      0x57fac9  ; -> 0057FAC9
0057FABD  mov      ecx, 0x873
0057FAC2  jmp      0x57fac9  ; -> 0057FAC9
0057FAC4  mov      ecx, 0x874
0057FAC9  call     0x2f9860  ; -> 002F9860 fn
0057FACE  mov      rcx, rax
0057FAD1  mov      rax, qword ptr [rbx + 0x10]
0057FAD5  mov      rbx, qword ptr [rax + 0xb0]
0057FADC  mov      qword ptr [rbx + 0x18], rcx
0057FAE0  xor      ecx, ecx
0057FAE2  call     0x20e620  ; -> 0020E620 fn
0057FAE7  mov      dword ptr [rbx + 0x20], eax
0057FAEA  mov      rbx, qword ptr [rsp + 0x30]
0057FAEF  add      rsp, 0x20
0057FAF3  pop      rdi
0057FAF4  ret      
```
