# Homing pack: `01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md`

Generated 2026-10-03 13:52 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h13-scriptvm-verb-dispatch-and-parameter-encoding.json`.

Bodies: 18. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002637B0 (32 B, extent 002637B0-002637D0)

Entered from (direct sites whose caller this page cites): `00377560` + 0x8 (call; `00377560` is cited on this page)
Other direct sites: none

Host context: ")', when it is zero it tail-jumps to '002E1C40(a, 0)' | Interior anchor '0035699D'; Interior anchor '003569A7'; Interior anchor '003569B2'; Interior anchor '003569C1'; Interior anchor '003569D4' | | '00377560' | 101 B | returns at once when 'ecx' is negative, when the call at '00377560' + 0x8 (with 'ecx' unchanged) returns a negative value 'i', or when '003587C0(0, i)' returns null; otherwise tail-jumps to '0026AF80' with 'rcx' = that p"

```
002637B0  cmp      ecx, 3
002637B3  ja       0x2637cc  ; -> 002637CC
002637B5  movsxd   rax, ecx
002637B8  lea      rcx, [rip + 0x1e36a31]  ; -> 0209A1F0
002637BF  mov      rcx, qword ptr [rcx + rax*8]
002637C3  test     rcx, rcx
002637C6  je       0x2637cc  ; -> 002637CC
002637C8  movzx    eax, word ptr [rcx]
002637CB  ret      
002637CC  or       eax, 0xffffffff
002637CF  ret      
```

## 0026A2A0 (107 B, extent 0026A2A0-0026A30B)

Entered from (direct sites whose caller this page cites): `0034A3B0` + 0x31 (jmp; `0034A3B0` is cited on this page)
Other direct sites: none

Host context: "rst float, 'xmm2' = the third and 'xmm3' = the second | Interior anchor '00348773'; Interior anchor '0034879A'; Interior anchor '003487A2'; Interior anchor '003487A5'; Interior anchor '003487C6' | | '0034A3B0' | 54 B | calls '002640C0' with the incoming registers and '00267E10(r9)', then tail-jumps to the function at site '0034A3B0' + 0x31 with 'ecx' = dword '+0x28' of the '002640C0' result and 'edx' = 1 when the '00267E10' result is 0,"

```
0026A2A0  movsxd   rax, ecx
0026A2A3  imul     rcx, rax, 0x288
0026A2AA  lea      rax, [rip + 0x1e2eb5f]  ; -> 02098E10
0026A2B1  add      rcx, rax
0026A2B4  test     edx, edx
0026A2B6  je       0x26a2be  ; -> 0026A2BE
0026A2B8  or       byte ptr [rcx + 0x17], 8
0026A2BC  jmp      0x26a2c2  ; -> 0026A2C2
0026A2BE  and      byte ptr [rcx + 0x17], 0xf7
0026A2C2  xor      al, al
0026A2C4  mov      edx, 1
0026A2C9  test     byte ptr [rip + 0x1e2eb57], 8  ; -> 02098E27
0026A2D0  cmovne   eax, edx
0026A2D3  test     byte ptr [rip + 0x1e2edd5], 8  ; -> 020990AF
0026A2DA  cmovne   eax, edx
0026A2DD  test     byte ptr [rip + 0x1e2f053], 8  ; -> 02099337
0026A2E4  movzx    ecx, al
0026A2E7  cmovne   ecx, edx
0026A2EA  test     byte ptr [rip + 0x1e2f2ce], 8  ; -> 020995BF
0026A2F1  movzx    eax, cl
0026A2F4  cmovne   eax, edx
0026A2F7  test     byte ptr [rip + 0x1e2f549], 8  ; -> 02099847
0026A2FE  movzx    eax, al
0026A301  cmovne   eax, edx
0026A304  mov      byte ptr [rip + 0x1e2fa97], al  ; -> 02099DA1
0026A30A  ret      
```

## 0026ABD0 (34 B, extent 0026ABD0-0026ABF2)

Entered from (direct sites whose caller this page cites): `0034D260` + 0x3C (jmp; `0034D260` is cited on this page)
Other direct sites: `0034D6D0` + 0x1C (jmp)

Host context: "nction at site '0034CAC0' + 0x3C with ('rdx', 'xmm1' = f times 0.25 ('01CEBB68')) | Interior anchor '0034CAD1'; Interior anchor '0034CADF'; Interior anchor '0034CAE4'; Interior anchor '0034CAFC' | | '0034D260' | 65 B | reads a float f by calling '00267DB0(r9)', calls the function at site '0034D260' + 0x1F with ('rdx', 'xmm1' = f), then tail-jumps to the function at site '0034D260' + 0x3C with ('rdx', 'xmm1' = f times 0.25 ('01CEBB68')) "

```
0026ABD0  movzx    eax, byte ptr [rcx + 3]
0026ABD4  and      al, 0xe0
0026ABD6  cmp      al, 0x60
0026ABD8  jne      0x26abf1  ; -> 0026ABF1
0026ABDA  mov      rax, qword ptr [rcx + 0xb8]
0026ABE1  movss    dword ptr [rax + 0xc4], xmm1
0026ABE9  movss    dword ptr [rax + 0xcc], xmm1
0026ABF1  ret      
```

## 0026B9D0 (46 B, extent 0026B9D0-0026B9FE)

Entered from (direct sites whose caller this page cites): `0034CAC0` + 0x3C (jmp; `0034CAC0` is cited on this page)
Other direct sites: `0034CE60` + 0x1C (jmp)

Host context: "d [r8], dword [r8+8], -1)' and returns 1 when that does not return '0xFF', else 0 | Interior anchor '0034C9E7'; Interior anchor '0034C9F9'; Interior anchor '0034C9FF'; Interior anchor '0034CA0B' | | '0034CAC0' | 65 B | reads a float f by calling '00267DB0(r9)', calls the function at site '0034CAC0' + 0x1F with ('rdx', 'xmm1' = f), then tail-jumps to the function at site '0034CAC0' + 0x3C with ('rdx', 'xmm1' = f times 0.25 ('01CEBB68')) "

```
0026B9D0  movzx    edx, byte ptr [rcx + 3]
0026B9D4  shr      edx, 5
0026B9D7  sub      edx, 1
0026B9DA  je       0x26b9f1  ; -> 0026B9F1
0026B9DC  cmp      edx, 2
0026B9DF  jne      0x26b9fd  ; -> 0026B9FD
0026B9E1  mov      rax, qword ptr [rcx + 0xb8]
0026B9E8  movss    dword ptr [rax + 0xcc], xmm1
0026B9F0  ret      
0026B9F1  mov      rax, qword ptr [rcx + 0xb8]
0026B9F8  movss    dword ptr [rax + 0x6c], xmm1
0026B9FD  ret      
```

## 0026BFF0 (113 B, extent 0026BFF0-0026C061)

Entered from (direct sites whose caller this page cites): `00352810` + 0x53 (call; `00352810` is cited on this page); `00352C00` + 0x36 (call; `00352C00` is cited on this page)
Other direct sites: `00351E00` + 0x40 (jmp); `00355A00` + 0x11B (call)

Host context: " + 0x38 with (dword '+0x28' of that result, 'b', 'a') | Interior anchor '00352140'; Interior anchor '0035214A'; Interior anchor '00352151'; Interior anchor '0035215B'; Interior anchor '00352168' | | '00352810' | 129 B | pops four floats 'a', 'b', 'c', 'd' in that order through '00267DB0(r9)', calls the function at '00352810' + 0x53 with 'rcx' = the incoming 'rdx', 'xmm1' = 'd', 'xmm2' = 'c', then tail-jumps to the function at '00352810'" / "', calls '003DB420(rdx, n, 4)' and tail-jumps to '003DB6E0(rdx)' (incoming 'rdx') | Interior anchor '0035298C'; Interior anchor '00352991'; Interior anchor '0035299C'; Interior anchor '003529A9' | | '00352C00' | 126 B | pops floats 'a', 'b' through '00267DB0(r9)' and calls the function at '00352C00' + 0x36 with 'rcx' = the incoming 'rdx', 'xmm1' = 'b', 'xmm2' = 'a'; then pops 'c', 'd', 'e' the same way and tail-jumps to '0026B0C0(rdx)' "

```
0026BFF0  movzx    edx, byte ptr [rcx + 3]
0026BFF4  xorps    xmm0, xmm0
0026BFF7  cvtss2sd xmm0, xmm1
0026BFFB  shr      edx, 5
0026BFFE  andps    xmm0, xmmword ptr [rip + 0x1a7fd7b]  ; -> 01CEBD80 [u32x4 0xFFFFFFFF, 0x7FFFFFFF, 0xFFFFFFFF, 0x7FFFFFFF]
0026C005  cvtpd2ps xmm1, xmm0
0026C009  xorps    xmm0, xmm0
0026C00C  cvtss2sd xmm0, xmm2
0026C010  andps    xmm0, xmmword ptr [rip + 0x1a7fd69]  ; -> 01CEBD80 [u32x4 0xFFFFFFFF, 0x7FFFFFFF, 0xFFFFFFFF, 0x7FFFFFFF]
0026C017  cvtpd2ps xmm4, xmm0
0026C01B  sub      edx, 1
0026C01E  je       0x26c02d  ; -> 0026C02D
0026C020  cmp      edx, 2
0026C023  jne      0x26c060  ; -> 0026C060
0026C025  movaps   xmm2, xmm4
0026C028  jmp      0x26bf60  ; -> 0026BF60 fn
0026C02D  mov      rax, qword ptr [rcx + 0xb8]
0026C034  or       byte ptr [rax + 0x5d], 2
0026C038  movss    xmm0, dword ptr [rax + 0x40]
0026C03D  comiss   xmm0, xmm1
0026C040  movss    dword ptr [rax + 0x30], xmm1
0026C045  movss    dword ptr [rax + 0x34], xmm4
0026C04A  jbe      0x26c051  ; -> 0026C051
0026C04C  movss    dword ptr [rax + 0x40], xmm1
0026C051  movss    xmm0, dword ptr [rax + 0x44]
0026C056  comiss   xmm0, xmm4
0026C059  jbe      0x26c060  ; -> 0026C060
0026C05B  movss    dword ptr [rax + 0x44], xmm4
0026C060  ret      
```

## 002D75F0 (117 B, extent 002D75F0-002D7665)

Entered from (direct sites whose caller this page cites): `005115B0` + 0x14 (jmp; `005115B0` is cited on this page)
Other direct sites: `00511550` + 0x21 (jmp)

Host context: "and returns 1 when dword '[r8]' differs from its result and 0 when they are equal | Interior anchor '005114D0'; Interior anchor '005114DA'; Interior anchor '005114E1'; Interior anchor '005114E3' | | '005115B0' | 30 B | returns at once, with 'eax' still holding that value, when '00280120()' returns non-zero; otherwise tail-jumps through '005115B0+0x14' with 'ecx' = -1 | Interior anchor '005115BB'; Interior anchor '005115BD'; Interior anc"

```
002D75F0  mov      r8, qword ptr [rip + 0x1dc3639]  ; -> 0209AC30
002D75F7  mov      rax, qword ptr [r8 + 0xd8]
002D75FE  mov      rdx, rax
002D7601  test     rax, rax
002D7604  jne      0x2d760d  ; -> 002D760D
002D7606  mov      rdx, qword ptr [r8 + 0x100]
002D760D  test     rdx, rdx
002D7610  je       0x2d7664  ; -> 002D7664
002D7612  test     rax, rax
002D7615  jne      0x2d7623  ; -> 002D7623
002D7617  mov      rax, qword ptr [r8 + 0x100]
002D761E  test     rax, rax
002D7621  je       0x2d7638  ; -> 002D7638
002D7623  mov      dword ptr [rax + 0xcc], 1
002D762D  mov      qword ptr [rax + 0xc4], 2
002D7638  cmp      ecx, -1
002D763B  jne      0x2d7651  ; -> 002D7651
002D763D  cmp      dword ptr [rdx + 0xc0], 0
002D7644  jne      0x2d7664  ; -> 002D7664
002D7646  mov      dword ptr [rdx + 0xc0], 0xa
002D7650  ret      
002D7651  cmp      dword ptr [rdx + 0xc0], 9
002D7658  jne      0x2d7664  ; -> 002D7664
002D765A  mov      dword ptr [rdx + 0xc0], 1
002D7664  ret      
```

## 002D7710 (65 B, extent 002D7710-002D7751)

Entered from (direct sites whose caller this page cites): `00511200` + 0x3F (call; `00511200` is cited on this page)
Other direct sites: none

Host context: "r (word 0 to the fourth pointer, word 3 to the first) | Interior anchor '00511025'; Interior anchor '00511058'; Interior anchor '005110BA'; Interior anchor '005110BF'; Interior anchor '005110E8' | | '00511200' | 84 B | returns at once, with 'eax' still holding that value, when '00280120()' returns non-zero; otherwise pops a, b, c in that order through '00267E10(r9)' and makes the call at '00511200+0x3F' with (c, b, a), leaving its resul"

```
002D7710  mov      rax, qword ptr [rip + 0x1dc3519]  ; -> 0209AC30
002D7717  mov      r9, qword ptr [rax + 0xf0]
002D771E  test     r9, r9
002D7721  je       0x2d7750  ; -> 002D7750
002D7723  cmp      ecx, 7
002D7726  ja       0x2d7750  ; -> 002D7750
002D7728  movsxd   rax, ecx
002D772B  add      rax, 8
002D772F  lea      rax, [rax + rax*2]
002D7733  mov      word ptr [r9 + rax*8 + 0x10], dx
002D7739  mov      word ptr [r9 + rax*8 + 0x12], r8w
002D773F  mov      dword ptr [r9 + rax*8], 0x200020
002D7747  mov      dword ptr [r9 + rax*8 + 4], 0x800080
002D7750  ret      
```

## 002D77C0 (62 B, extent 002D77C0-002D77FE)

Entered from (direct sites whose caller this page cites): `005118D0` + 0x16 (call; `005118D0` is cited on this page); `005119C0` + 0x19 (call; `005119C0` is cited on this page)
Other direct sites: none

Host context: " that value, when '00280120()' returns non-zero; otherwise tail-jumps through '005115B0+0x14' with 'ecx' = -1 | Interior anchor '005115BB'; Interior anchor '005115BD'; Interior anchor '005115C4' | | '005118D0' | 41 B | returns 0 when '00280120()' returns non-zero; otherwise makes the call at '005118D0+0x16' with 0 and returns 1 when it returns 0 and 0 when it returns non-zero | Interior anchor '005118DB'; Interior anchor '005118E4'; Int" / "118D0+0x16' with 0 and returns 1 when it returns 0 and 0 when it returns non-zero | Interior anchor '005118DB'; Interior anchor '005118E4'; Interior anchor '005118E6'; Interior anchor '005118EF' | | '005119C0' | 44 B | returns 0 when '00280120()' returns non-zero; otherwise makes the call at '005119C0+0x19' with 1 and returns 1 when it returns 0 and 0 when it returns non-zero | Interior anchor '005119CB'; Interior anchor '005119D4'; Int"

```
002D77C0  mov      rax, qword ptr [rip + 0x1dc3469]  ; -> 0209AC30
002D77C7  mov      rdx, qword ptr [rax + 0xe8]
002D77CE  test     rdx, rdx
002D77D1  je       0x2d77f8  ; -> 002D77F8
002D77D3  cmp      dword ptr [rdx + 0xc8], 0
002D77DA  jne      0x2d77f8  ; -> 002D77F8
002D77DC  xor      eax, eax
002D77DE  test     ecx, ecx
002D77E0  je       0x2d77ed  ; -> 002D77ED
002D77E2  cmp      byte ptr [rdx + 0xc0], 1
002D77E9  sete     al
002D77EC  ret      
002D77ED  cmp      byte ptr [rdx + 0xc0], 2
002D77F4  sete     al
002D77F7  ret      
002D77F8  mov      eax, 1
002D77FD  ret      
```

## 002D7800 (64 B, extent 002D7800-002D7840)

Entered from (direct sites whose caller this page cites): `00510AA0` + 0x21 (call; `00510AA0` is cited on this page); `00510B40` + 0x1E (call; `00510B40` is cited on this page)
Other direct sites: none

Host context: "for any other value tail-jumps to '0026B4E0(rcx, -1)' | Interior anchor '0051010C'; Interior anchor '00510113'; Interior anchor '0051011A'; Interior anchor '0051012C'; Interior anchor '00510140' | | '00510AA0' | 53 B | returns 0 when '00280120()' returns non-zero; otherwise makes the call at '00510AA0+0x21' with (dword '[r8]', 1) and returns 1 when it returns 0 and 0 when it returns non-zero | Interior anchor '00510AA9'; Interior anchor" / "ns 1 when it returns 0 and 0 when it returns non-zero | Interior anchor '00510AA9'; Interior anchor '00510AB0'; Interior anchor '00510ABA'; Interior anchor '00510AC1'; Interior anchor '00510ACA' | | '00510B40' | 50 B | returns 0 when '00280120()' returns non-zero; otherwise makes the call at '00510B40+0x1E' with (dword '[r8]', 0) and returns 1 when it returns 0 and 0 when it returns non-zero | Interior anchor '00510B49'; Interior anchor"

```
002D7800  mov      rax, qword ptr [rip + 0x1dc3429]  ; -> 0209AC30
002D7807  mov      r8, qword ptr [rax + 0xf0]
002D780E  test     r8, r8
002D7811  je       0x2d783a  ; -> 002D783A
002D7813  cmp      ecx, 7
002D7816  ja       0x2d783a  ; -> 002D783A
002D7818  movsxd   rax, ecx
002D781B  add      rax, 8
002D781F  lea      rax, [rax + rax*2]
002D7823  mov      ecx, dword ptr [r8 + rax*8 + 0x14]
002D7828  test     cl, 4
002D782B  jne      0x2d783a  ; -> 002D783A
002D782D  shr      ecx, 1
002D782F  xor      eax, eax
002D7831  and      ecx, 1
002D7834  cmp      ecx, edx
002D7836  sete     al
002D7839  ret      
002D783A  mov      eax, 1
002D783F  ret      
```

## 002E75A0 (96 B, extent 002E75A0-002E7600)

Entered from (direct sites whose caller this page cites): `00348040` + 0x4A (call; `00348040` is cited on this page); `00348750` + 0x4A (call; `00348750` is cited on this page)
Other direct sites: `00349410` + 0x5 (jmp)

Host context: " to the function at site '00347A50' + 0x52 without setting its argument registers | Interior anchor '00347A6A'; Interior anchor '00347A78'; Interior anchor '00347A89'; Interior anchor '00347AA2' | | '00348040' | 123 B | reads three floats by calling '00267DB0(r9)' three times (first, second, third), calls the function at site '00348040' + 0x4A with ('rdx', 1), then tail-jumps to the function at site '00348040' + 0x76 with 'rcx' = the in" / "rst float, 'xmm2' = the third and 'xmm3' = the second | Interior anchor '00348063'; Interior anchor '0034808A'; Interior anchor '00348092'; Interior anchor '00348095'; Interior anchor '003480B6' | | '00348750' | 123 B | reads three floats by calling '00267DB0(r9)' three times (first, second, third), calls the function at site '00348750' + 0x4A with ('rdx', 1), then tail-jumps to the function at site '00348750' + 0x76 with 'rcx' = the in"

```
002E75A0  test     rcx, rcx
002E75A3  je       0x2e75ff  ; -> 002E75FF
002E75A5  mov      rax, qword ptr [rcx + 0xc0]
002E75AC  test     rax, rax
002E75AF  je       0x2e75ff  ; -> 002E75FF
002E75B1  cmp      dword ptr [rax], -1
002E75B4  je       0x2e75ff  ; -> 002E75FF
002E75B6  movzx    ecx, word ptr [rax]
002E75B9  cmp      cx, -1
002E75BD  je       0x2e75ff  ; -> 002E75FF
002E75BF  movsx    rax, cx
002E75C3  imul     rcx, rax, 0x740
002E75CA  add      rcx, qword ptr [rip + 0x1fdf957]  ; -> 022C6F28
002E75D1  je       0x2e75ff  ; -> 002E75FF
002E75D3  cmp      dword ptr [rcx + 0x284], 0
002E75DA  je       0x2e75ff  ; -> 002E75FF
002E75DC  and      dword ptr [rcx + 0x304], 0xfffffeff
002E75E6  neg      edx
002E75E8  sbb      eax, eax
002E75EA  and      eax, 0x100
002E75EF  or       dword ptr [rcx + 0x304], eax
002E75F5  or       dword ptr [rcx + 0x290], 0x20000
002E75FF  ret      
```

## 002EC8B0 (67 B, extent 002EC8B0-002EC8F3)

Entered from (direct sites whose caller this page cites): `00340810` + 0x5A (jmp; `00340810` is cited on this page)
Other direct sites: none

Host context: "03405C0+0x5a' with ('p', 'v4', 'v3', 'v2') and 'v1' as the fifth (stack) argument | Interior anchor '003405DD'; Interior anchor '003405E8'; Interior anchor '0034060E'; Interior anchor '0034061A' | | '00340810' | 95 B | reads two floats 'a' then 'b' by calling '00267DB0(r9)' twice; when 'a' is not below 0.0 ('comiss'/'jb') it replaces 'a' with 'maxss' of 'b' and 'a', otherwise keeps 'a'; calls '00340810+0x40' with the incoming 'rdx' and "

```
002EC8B0  push     rbx
002EC8B2  sub      rsp, 0x20
002EC8B6  test     rcx, rcx
002EC8B9  je       0x2ec8c4  ; -> 002EC8C4
002EC8BB  mov      rbx, qword ptr [rcx + 0xc0]
002EC8C2  jmp      0x2ec8c6  ; -> 002EC8C6
002EC8C4  xor      ebx, ebx
002EC8C6  xorps    xmm0, xmm0
002EC8C9  comiss   xmm1, xmm0
002EC8CC  jbe      0x2ec8de  ; -> 002EC8DE
002EC8CE  cvttss2si ecx, xmm1
002EC8D2  call     0x3da190  ; -> 003DA190 fn
002EC8D7  movd     xmm1, eax
002EC8DB  cvtdq2ps xmm1, xmm1
002EC8DE  test     rbx, rbx
002EC8E1  je       0x2ec8ed  ; -> 002EC8ED
002EC8E3  cmp      dword ptr [rbx], -1
002EC8E6  je       0x2ec8ed  ; -> 002EC8ED
002EC8E8  movss    dword ptr [rbx + 0x1c], xmm1
002EC8ED  add      rsp, 0x20
002EC8F1  pop      rbx
002EC8F2  ret      
```

## 002EC970 (67 B, extent 002EC970-002EC9B3)

Entered from (direct sites whose caller this page cites): `00340810` + 0x40 (call; `00340810` is cited on this page)
Other direct sites: none

Host context: "03405C0+0x5a' with ('p', 'v4', 'v3', 'v2') and 'v1' as the fifth (stack) argument | Interior anchor '003405DD'; Interior anchor '003405E8'; Interior anchor '0034060E'; Interior anchor '0034061A' | | '00340810' | 95 B | reads two floats 'a' then 'b' by calling '00267DB0(r9)' twice; when 'a' is not below 0.0 ('comiss'/'jb') it replaces 'a' with 'maxss' of 'b' and 'a', otherwise keeps 'a'; calls '00340810+0x40' with the incoming 'rdx' and "

```
002EC970  push     rbx
002EC972  sub      rsp, 0x20
002EC976  test     rcx, rcx
002EC979  je       0x2ec984  ; -> 002EC984
002EC97B  mov      rbx, qword ptr [rcx + 0xc0]
002EC982  jmp      0x2ec986  ; -> 002EC986
002EC984  xor      ebx, ebx
002EC986  xorps    xmm0, xmm0
002EC989  comiss   xmm1, xmm0
002EC98C  jbe      0x2ec99e  ; -> 002EC99E
002EC98E  cvttss2si ecx, xmm1
002EC992  call     0x3da190  ; -> 003DA190 fn
002EC997  movd     xmm1, eax
002EC99B  cvtdq2ps xmm1, xmm1
002EC99E  test     rbx, rbx
002EC9A1  je       0x2ec9ad  ; -> 002EC9AD
002EC9A3  cmp      dword ptr [rbx], -1
002EC9A6  je       0x2ec9ad  ; -> 002EC9AD
002EC9A8  movss    dword ptr [rbx + 0x18], xmm1
002EC9AD  add      rsp, 0x20
002EC9B1  pop      rbx
002EC9B2  ret      
```

## 0035A140 (86 B, extent 0035A140-0035A196)

Entered from (direct sites whose caller this page cites): `00344EC0` + 0x13 (call; `00344EC0` is cited on this page)
Other direct sites: `00344610` + 0xE (call); `00344980` + 0xE (call)

Host context: " '0026B4E0(rcx, that result)' with the incoming 'rcx' | Interior anchor '003449BD'; Interior anchor '003449DA'; Interior anchor '003449E6'; Interior anchor '003449EF'; Interior anchor '00344A0D' | | '00344EC0' | 56 B | passes '00267E10(r9)' to the call at '00344EC0+0x13', passes that result to the call at '00344EC0+0x1a', and tail-jumps to '0026B4E0(rcx, 1 when that result is non-zero, else 0)' with the incoming 'rcx' | Interior anchor "

```
0035A140  xor      edx, edx
0035A142  cmp      ecx, 6
0035A145  ja       0x35a193  ; -> 0035A193
0035A147  movsxd   rax, ecx
0035A14A  lea      r8, [rip - 0x23a151]  ; -> 00120000 (image base)
0035A151  mov      ecx, dword ptr [r8 + rax*4 + 0x23a198]  ; image base + 0x23a198 = 0035A198
0035A159  add      rcx, r8
0035A15C  jmp      rcx
0035A15E  mov      edx, 1
0035A163  mov      eax, edx
0035A165  ret      
0035A166  mov      edx, 2
0035A16B  mov      eax, edx
0035A16D  ret      
0035A16E  mov      edx, 4
0035A173  mov      eax, edx
0035A175  ret      
0035A176  mov      edx, 8
0035A17B  mov      eax, edx
0035A17D  ret      
0035A17E  mov      edx, 0x10
0035A183  mov      eax, edx
0035A185  ret      
0035A186  mov      edx, 0x20
0035A18B  mov      eax, edx
0035A18D  ret      
0035A18E  mov      edx, 0x40
0035A193  mov      eax, edx
0035A195  ret      
```

## 003DE9A0 (14 B, extent 003DE9A0-003DE9AE)

Entered from (direct sites whose caller this page cites): `00352130` + 0x38 (jmp; `00352130` is cited on this page)
Other direct sites: `00352780` + 0x44 (jmp)

Host context: "en tail-jumps to the function at '00352040' + 0x34 with the same 'rcx' and 'xmm1' | Interior anchor '00352051'; Interior anchor '0035205F'; Interior anchor '00352064'; Interior anchor '00352074' | | '00352130' | 61 B | pops 'a' then 'b' through '00267E10(r9)', calls '002640C0()' (no 'rcx' loaded after the pops) and tail-jumps to the function at '00352130' + 0x38 with (dword '+0x28' of that result, 'b', 'a') | Interior anchor '00352140';"

```
003DE9A0  test     r8d, r8d
003DE9A3  jne      0x37a880  ; -> 0037A880 fn
003DE9A9  jmp      0x37a7f0  ; -> 0037A7F0 fn
```

## 003DEA00 (14 B, extent 003DEA00-003DEA0E)

Entered from (direct sites whose caller this page cites): `00351210` + 0x38 (jmp; `00351210` is cited on this page)
Other direct sites: `00351D90` + 0x44 (jmp)

Host context: "nction at site '0034D260' + 0x3C with ('rdx', 'xmm1' = f times 0.25 ('01CEBB68')) | Interior anchor '0034D271'; Interior anchor '0034D27F'; Interior anchor '0034D284'; Interior anchor '0034D29C' | | '00351210' | 61 B | reads two ints a, b by calling '00267E10(r9)' twice, calls '002640C0' without setting its argument registers, and tail-jumps to the function at site '00351210' + 0x38 with ('ecx' = dword '+0x28' of that result, 'edx' = b,"

```
003DEA00  test     r8d, r8d
003DEA03  jne      0x37a9b0  ; -> 0037A9B0 fn
003DEA09  jmp      0x37a910  ; -> 0037A910 fn
```

## 003EB860 (82 B, extent 003EB860-003EB8B2)

Entered from (direct sites whose caller this page cites): `003412B0` + 0x8F (call; `003412B0` is cited on this page)
Other direct sites: `00340D00` + 0x75 (jmp)

Host context: " at '00340810+0x5a' with that 'rdx' and 'a' in 'xmm1' | Interior anchor '00340828'; Interior anchor '0034083E'; Interior anchor '00340843'; Interior anchor '00340850'; Interior anchor '0034086A' | | '003412B0' | 167 B | builds a local float array {'f3', 'f2', 'f1', 1.0 ('01CEBBA8')} from three '00267DB0(r9)' calls ('f1' first) and reads 'v' = '00267E10(r9)'; calls '0016D6A0(v)' and 'h' = the function at '003412B0+0x63' with 'v', then '0"

```
003EB860  test     rcx, rcx
003EB863  je       0x3eb8b1  ; -> 003EB8B1
003EB865  cmp      dword ptr [rcx + 0x10], 0
003EB869  jl       0x3eb8b1  ; -> 003EB8B1
003EB86B  movzx    eax, word ptr [rcx + 0x10]
003EB86F  cmp      ax, -1
003EB873  je       0x3eb8b1  ; -> 003EB8B1
003EB875  movsx    rax, ax
003EB879  imul     rcx, rax, 0x740
003EB880  add      rcx, qword ptr [rip + 0x1edb6a1]  ; -> 022C6F28
003EB887  je       0x3eb8b1  ; -> 003EB8B1
003EB889  cmp      dword ptr [rcx + 0x284], 0
003EB890  je       0x3eb8b1  ; -> 003EB8B1
003EB892  or       dword ptr [rcx + 0x290], 8
003EB899  movss    dword ptr [rcx + 0x380], xmm1
003EB8A1  movss    dword ptr [rcx + 0x384], xmm2
003EB8A9  movss    dword ptr [rcx + 0x388], xmm3
003EB8B1  ret      
```

## 0055FED0 (190 B, extent 0055FED0-0055FF8E)

Entered from (direct sites whose caller this page cites): `00511010` + 0xAA (call; `00511010` is cited on this page)
Other direct sites: none

Host context: "ved pointers; the fifth pop's result is left in 'eax' | Interior anchor '00510F45'; Interior anchor '00510F5F'; Interior anchor '00510F78'; Interior anchor '00510FCE'; Interior anchor '00510FD3' | | '00511010' | 232 B | returns at once, with 'eax' still holding that value, when '00280120()' returns non-zero; otherwise calls '002640C0' (no argument set up after the guard) and four times resolves '002650B0(that result, incoming rcx, 00267"

```
0055FED0  mov      r8, qword ptr [rip + 0x1b3ad59]  ; -> 0209AC30
0055FED7  cmp      qword ptr [r8 + 0x158], 0
0055FEDF  je       0x55ff8d  ; -> 0055FF8D
0055FEE5  mov      r8, qword ptr [r8 + 0x320]
0055FEEC  test     r8, r8
0055FEEF  je       0x55ff8d  ; -> 0055FF8D
0055FEF5  mov      r8, qword ptr [r8 + 0x138]
0055FEFC  test     r8, r8
0055FEFF  je       0x55ff8d  ; -> 0055FF8D
0055FF05  cmp      ecx, -1
0055FF08  je       0x55ff56  ; -> 0055FF56
0055FF0A  test     ecx, ecx
0055FF0C  jne      0x55ff8d  ; -> 0055FF8D
0055FF0E  mov      rax, qword ptr [r8 + 0x60]
0055FF12  mov      rcx, qword ptr [rax + 0x18]
0055FF16  movzx    eax, word ptr [r8 + 0x98]
0055FF1E  sub      ax, 6
0055FF22  add      ax, word ptr [rcx + 0xc]
0055FF26  mov      word ptr [rdx], ax
0055FF29  movzx    eax, word ptr [r8 + 0x9a]
0055FF31  sub      ax, 6
0055FF35  add      ax, word ptr [rcx + 0xe]
0055FF39  mov      word ptr [rdx + 2], ax
0055FF3D  movzx    eax, word ptr [rcx + 0x10]
0055FF41  sub      ax, 6
0055FF45  mov      word ptr [rdx + 4], ax
0055FF49  movzx    eax, word ptr [rcx + 0x12]
0055FF4D  add      ax, 0xb
0055FF51  mov      word ptr [rdx + 6], ax
0055FF55  ret      
0055FF56  movzx    eax, word ptr [r8 + 0x98]
0055FF5E  add      ax, 8
0055FF62  mov      word ptr [rdx], ax
0055FF65  movzx    eax, word ptr [r8 + 0x9a]
0055FF6D  mov      word ptr [rdx + 2], ax
0055FF71  movzx    eax, word ptr [r8 + 0x9c]
0055FF79  sub      ax, 0x48
0055FF7D  mov      word ptr [rdx + 4], ax
0055FF81  movzx    eax, word ptr [r8 + 0x9e]
0055FF89  mov      word ptr [rdx + 6], ax
0055FF8D  ret      
```

## 00567AE0 (120 B, extent 00567AE0-00567B58)

Entered from (direct sites whose caller this page cites): `00511B70` + 0x3F (call; `00511B70` is cited on this page)
Other direct sites: none

Host context: "0267E10(r9)' and tail-jumps through '00511B00+0x24' with 'ecx' = that value XOR 1 | Interior anchor '00511B10'; Interior anchor '00511B15'; Interior anchor '00511B1A'; Interior anchor '00511B24' | | '00511B70' | 84 B | returns at once, with 'eax' still holding that value, when '00280120()' returns non-zero; otherwise pops a, b, c in that order through '00267E10(r9)' and makes the call at '00511B70+0x3F' with (c, b, a), leaving its resul"

```
00567AE0  push     rbx
00567AE2  sub      rsp, 0x20
00567AE6  mov      rax, qword ptr [rip + 0x1b33143]  ; -> 0209AC30
00567AED  lea      rbx, [rip + 0x2741bec]  ; -> 02CA96E0
00567AF4  mov      r9, qword ptr [rax + 0x160]
00567AFB  mov      rax, qword ptr [rip + 0x295768e]  ; -> 02EBF190
00567B02  movsxd   r10, dword ptr [r9 + 0xf0]
00567B09  movsxd   r9, dword ptr [rax + r10*4 + 0x7370]
00567B11  mov      rbx, qword ptr [rbx + r9*8]
00567B15  test     rbx, rbx
00567B18  je       0x567b52  ; -> 00567B52
00567B1A  cmp      byte ptr [rbx + 0x331], 0
00567B21  jne      0x567b52  ; -> 00567B52
00567B23  mov      word ptr [rbx + 0x330], 0x101
00567B2C  mov      byte ptr [rbx + 0x336], cl
00567B32  mov      byte ptr [rbx + 0x337], dl
00567B38  mov      word ptr [rbx + 0x33c], r8w
00567B40  mov      byte ptr [rbx + 0x33b], 0
00567B47  call     0x2d6680  ; -> 002D6680 fn
00567B4C  mov      byte ptr [rbx + 0x33a], al
00567B52  add      rsp, 0x20
00567B56  pop      rbx
00567B57  ret      
```
