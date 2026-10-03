# F homing pack: `16-UI/Shop-Screens/the-shop-screens.md`

Generated 2026-10-03 02:21 by OPUS (homing_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 17. No bearing page cites them and no documented function calls them directly.

## 002947F0 (106 B, extent 002947F0-0029485A)

Documented callee on this page: `002AC2E0`

```
002947F0  mov      qword ptr [rsp + 8], rbx
002947F5  mov      qword ptr [rsp + 0x10], rsi
002947FA  push     rdi
002947FB  sub      rsp, 0x20
002947FF  mov      rdi, rcx
00294802  mov      byte ptr [rdx + 4], 1
00294806  mov      edx, dword ptr [rsp + 0x50]
0029480A  mov      ecx, 0x12
0029480F  mov      rsi, r9
00294812  mov      rbx, r8
00294815  call     0x35d330  ; -> 0035D330 fn
0029481A  mov      rdx, qword ptr [rax + 0x10]
0029481E  mov      qword ptr [rbx], rdx
00294821  call     0x2ac2e0  ; -> 002AC2E0 fn
00294826  mov      r8, rax
00294829  mov      rdx, rdi
0029482C  mov      rcx, rsi
0029482F  call     0x17d2e0  ; -> 0017D2E0 fn
00294834  cmp      eax, 0x200
00294839  jb       0x294845  ; -> 00294845
0029483B  mov      ecx, 0x20000
00294840  call     0x16d6a0  ; -> 0016D6A0 fn
00294845  mov      rbx, qword ptr [rsp + 0x30]
0029484A  mov      eax, 1
0029484F  mov      rsi, qword ptr [rsp + 0x38]
00294854  add      rsp, 0x20
00294858  pop      rdi
00294859  ret      
```

## 002CCA40 (190 B, extent 002CCA40-002CCAFE)

Documented callee on this page: `00252F40`

```
002CCA40  push     rbp
002CCA42  push     r14
002CCA44  push     r15
002CCA46  sub      rsp, 0x20
002CCA4A  mov      r15d, ecx
002CCA4D  mov      r14d, edx
002CCA50  mov      ecx, 4
002CCA55  call     0x252fa0  ; -> 00252FA0 fn
002CCA5A  mov      ebp, eax
002CCA5C  test     eax, eax
002CCA5E  jg       0x2cca6c  ; -> 002CCA6C
002CCA60  xor      eax, eax
002CCA62  add      rsp, 0x20
002CCA66  pop      r15
002CCA68  pop      r14
002CCA6A  pop      rbp
002CCA6B  ret      
002CCA6C  mov      qword ptr [rsp + 0x40], rbx
002CCA71  mov      ecx, 4
002CCA76  mov      qword ptr [rsp + 0x48], rsi
002CCA7B  mov      qword ptr [rsp + 0x50], rdi
002CCA80  mov      qword ptr [rsp + 0x58], r12
002CCA85  call     0x252f40  ; -> 00252F40 fn
002CCA8A  mov      ecx, dword ptr [rax + 4]
002CCA8D  call     0x20e600  ; -> 0020E600 fn
002CCA92  xor      ebx, ebx
002CCA94  mov      rdi, rax
002CCA97  test     ebp, ebp
002CCA99  jle      0x2ccad7  ; -> 002CCAD7
002CCA9B  mov      r12d, 0xffff
002CCAA1  movzx    eax, word ptr [rdi]
002CCAA4  cmp      ax, r12w
002CCAA8  je       0x2ccacd  ; -> 002CCACD
002CCAAA  movzx    esi, ax
002CCAAD  mov      ecx, 6
002CCAB2  mov      edx, esi
002CCAB4  shl      edx, 0x10
002CCAB7  call     0x35d330  ; -> 0035D330 fn
002CCABC  cmp      dword ptr [rax + 0x38], r15d
002CCAC0  jne      0x2ccacd  ; -> 002CCACD
002CCAC2  cmp      esi, r14d
002CCAC5  je       0x2ccaf7  ; -> 002CCAF7
002CCAC7  cmp      dword ptr [rax + 0x20], 0
002CCACB  jg       0x2ccaf7  ; -> 002CCAF7
002CCACD  inc      ebx
002CCACF  add      rdi, 2
002CCAD3  cmp      ebx, ebp
002CCAD5  jl       0x2ccaa1  ; -> 002CCAA1
002CCAD7  xor      eax, eax
002CCAD9  mov      rdi, qword ptr [rsp + 0x50]
002CCADE  mov      rsi, qword ptr [rsp + 0x48]
002CCAE3  mov      rbx, qword ptr [rsp + 0x40]
002CCAE8  mov      r12, qword ptr [rsp + 0x58]
002CCAED  add      rsp, 0x20
002CCAF1  pop      r15
002CCAF3  pop      r14
002CCAF5  pop      rbp
002CCAF6  ret      
002CCAF7  mov      eax, 1
002CCAFC  jmp      0x2ccad9  ; -> 002CCAD9
```

## 00342F50 (38 B, extent 00342F50-00342F76)

Documented callee on this page: `00314D40`

```
00342F50  sub      rsp, 0x28
00342F54  call     0x37cb80  ; -> 0037CB80 fn
00342F59  test     eax, eax
00342F5B  jne      0x342f62  ; -> 00342F62
00342F5D  add      rsp, 0x28
00342F61  ret      
00342F62  mov      ecx, 1
00342F67  call     0x314d40  ; -> 00314D40 fn
00342F6C  mov      eax, 1
00342F71  add      rsp, 0x28
00342F75  ret      
```

## 003453D0 (45 B, extent 003453D0-003453FD)

Documented callee on this page: `00314D40`

```
003453D0  sub      rsp, 0x28
003453D4  cmp      word ptr [r8], 0
003453D9  je       0x3453f6  ; -> 003453F6
003453DB  call     0x35a0a0  ; -> 0035A0A0 fn
003453E0  test     eax, eax
003453E2  jne      0x3453f6  ; -> 003453F6
003453E4  lea      ecx, [rax + 1]
003453E7  call     0x314d40  ; -> 00314D40 fn
003453EC  mov      eax, 1
003453F1  add      rsp, 0x28
003453F5  ret      
003453F6  xor      eax, eax
003453F8  add      rsp, 0x28
003453FC  ret      
```

## 00346020 (55 B, extent 00346020-00346057)

Documented callee on this page: `00314D40`

```
00346020  sub      rsp, 0x28
00346024  movzx    eax, word ptr [r8]
00346028  cmp      ax, -1
0034602C  je       0x346050  ; -> 00346050
0034602E  test     ax, ax
00346031  je       0x346050  ; -> 00346050
00346033  call     0x35a0a0  ; -> 0035A0A0 fn
00346038  test     eax, eax
0034603A  je       0x346050  ; -> 00346050
0034603C  mov      ecx, 1
00346041  call     0x314d40  ; -> 00314D40 fn
00346046  mov      eax, 1
0034604B  add      rsp, 0x28
0034604F  ret      
00346050  xor      eax, eax
00346052  add      rsp, 0x28
00346056  ret      
```

## 003491B0 (43 B, extent 003491B0-003491DB)

Documented callee on this page: `00314D40`

```
003491B0  sub      rsp, 0x28
003491B4  mov      ecx, dword ptr [r8]
003491B7  call     0x35a220  ; -> 0035A220 fn
003491BC  test     eax, eax
003491BE  je       0x3491d4  ; -> 003491D4
003491C0  mov      ecx, 1
003491C5  call     0x314d40  ; -> 00314D40 fn
003491CA  mov      eax, 1
003491CF  add      rsp, 0x28
003491D3  ret      
003491D4  xor      eax, eax
003491D6  add      rsp, 0x28
003491DA  ret      
```

## 00349A30 (38 B, extent 00349A30-00349A56)

Documented callee on this page: `00314D40`

```
00349A30  sub      rsp, 0x28
00349A34  call     0x30bad0  ; -> 0030BAD0 fn
00349A39  test     eax, eax
00349A3B  jne      0x349a4f  ; -> 00349A4F
00349A3D  lea      ecx, [rax + 1]
00349A40  call     0x314d40  ; -> 00314D40 fn
00349A45  mov      eax, 1
00349A4A  add      rsp, 0x28
00349A4E  ret      
00349A4F  xor      eax, eax
00349A51  add      rsp, 0x28
00349A55  ret      
```

## 00353720 (43 B, extent 00353720-0035374B)

Documented callee on this page: `00314D40`

```
00353720  sub      rsp, 0x28
00353724  mov      ecx, dword ptr [r8]
00353727  call     0x2e2550  ; -> 002E2550 fn
0035372C  test     eax, eax
0035372E  je       0x353744  ; -> 00353744
00353730  mov      ecx, 1
00353735  call     0x314d40  ; -> 00314D40 fn
0035373A  mov      eax, 1
0035373F  add      rsp, 0x28
00353743  ret      
00353744  xor      eax, eax
00353746  add      rsp, 0x28
0035374A  ret      
```

## 00356050 (40 B, extent 00356050-00356078)

Documented callee on this page: `00314D40`

```
00356050  sub      rsp, 0x28
00356054  call     0x35b7a0  ; -> 0035B7A0 fn
00356059  test     eax, eax
0035605B  je       0x356064  ; -> 00356064
0035605D  xor      eax, eax
0035605F  add      rsp, 0x28
00356063  ret      
00356064  mov      ecx, 1
00356069  call     0x314d40  ; -> 00314D40 fn
0035606E  mov      eax, 1
00356073  add      rsp, 0x28
00356077  ret      
```

## 00357300 (43 B, extent 00357300-0035732B)

Documented callee on this page: `00314D40`

```
00357300  sub      rsp, 0x28
00357304  call     0x35b740  ; -> 0035B740 fn
00357309  dec      eax
0035730B  cmp      eax, 2
0035730E  ja       0x357324  ; -> 00357324
00357310  mov      ecx, 1
00357315  call     0x314d40  ; -> 00314D40 fn
0035731A  mov      eax, 1
0035731F  add      rsp, 0x28
00357323  ret      
00357324  xor      eax, eax
00357326  add      rsp, 0x28
0035732A  ret      
```

## 003C95C0 (630 B, extent 003C95C0-003C9836)

Documented callee on this page: `00394700`

```
003C95C0  push     rbx
003C95C2  sub      rsp, 0x20
003C95C6  mov      rbx, rcx
003C95C9  mov      ecx, dword ptr [rdx]
003C95CB  sub      ecx, 1
003C95CE  je       0x3c97b4  ; -> 003C97B4
003C95D4  sub      ecx, 1
003C95D7  je       0x3c9701  ; -> 003C9701
003C95DD  sub      ecx, 1
003C95E0  je       0x3c9622  ; -> 003C9622
003C95E2  sub      ecx, 0xb
003C95E5  je       0x3c9611  ; -> 003C9611
003C95E7  cmp      ecx, 1
003C95EA  je       0x3c95f9  ; -> 003C95F9
003C95EC  mov      rcx, rbx
003C95EF  add      rsp, 0x20
003C95F3  pop      rbx
003C95F4  jmp      0x5c5230  ; -> 005C5230 fn
003C95F9  mov      word ptr [rbx + 0xc0], 0x507
003C9602  xor      eax, eax
003C9604  mov      byte ptr [rbx + 0xc2], 3
003C960B  add      rsp, 0x20
003C960F  pop      rbx
003C9610  ret      
003C9611  mov      word ptr [rbx + 0xc1], 0xa02
003C961A  xor      eax, eax
003C961C  add      rsp, 0x20
003C9620  pop      rbx
003C9621  ret      
003C9622  movzx    ecx, byte ptr [rbx + 0xc1]
003C9629  mov      r8b, 0x80
003C962C  mov      r9, qword ptr [rbx + 0x38]
003C9630  movzx    edx, r8b
003C9634  test     ecx, ecx
003C9636  je       0x3c96e3  ; -> 003C96E3
003C963C  sub      ecx, 1
003C963F  je       0x3c96bc  ; -> 003C96BC
003C9641  sub      ecx, 1
003C9644  je       0x3c969c  ; -> 003C969C
003C9646  sub      ecx, 3
003C9649  je       0x3c9678  ; -> 003C9678
003C964B  cmp      ecx, 1
003C964E  jne      0x3c96e8  ; -> 003C96E8
003C9654  movzx    ecx, byte ptr [rbx + 0xc2]
003C965B  mov      eax, 0x66666667
003C9660  shl      ecx, 7
003C9663  imul     ecx
003C9665  mov      r8d, edx
003C9668  mov      dl, 0xff
003C966A  sar      r8d, 1
003C966D  mov      eax, r8d
003C9670  shr      eax, 0x1f
003C9673  add      r8d, eax
003C9676  jmp      0x3c96e8  ; -> 003C96E8
003C9678  movzx    eax, byte ptr [rbx + 0xc2]
003C967F  mov      edx, 3
003C9684  sub      edx, eax
003C9686  mov      eax, 0x55555556
003C968B  shl      edx, 7
003C968E  imul     edx
003C9690  mov      eax, edx
003C9692  shr      eax, 0x1f
003C9695  add      edx, eax
003C9697  add      dl, 0x7f
003C969A  jmp      0x3c96e8  ; -> 003C96E8
003C969C  movzx    ecx, byte ptr [rbx + 0xc2]
003C96A3  mov      eax, 0x66666667
003C96A8  shl      ecx, 7
003C96AB  imul     ecx
003C96AD  sar      edx, 2
003C96B0  mov      eax, edx
003C96B2  shr      eax, 0x1f
003C96B5  add      edx, eax
003C96B7  add      dl, 0x7f
003C96BA  jmp      0x3c96e8  ; -> 003C96E8
003C96BC  movzx    eax, byte ptr [rbx + 0xc2]
003C96C3  mov      edx, 3
003C96C8  sub      edx, eax
003C96CA  mov      eax, 0x55555556
003C96CF  shl      edx, 7
003C96D2  imul     edx
003C96D4  mov      eax, edx
003C96D6  shr      eax, 0x1f
003C96D9  add      edx, eax
003C96DB  movzx    r8d, dl
003C96DF  mov      dl, 0xff
003C96E1  jmp      0x3c96e8  ; -> 003C96E8
003C96E3  xor      r8b, r8b
003C96E6  xor      dl, dl
003C96E8  movzx    eax, r8b
003C96EC  mov      word ptr [r9 + 0x58], ax
003C96F1  movzx    eax, dl
003C96F4  mov      word ptr [r9 + 0x5a], ax
003C96F9  xor      eax, eax
003C96FB  add      rsp, 0x20
003C96FF  pop      rbx
003C9700  ret      
003C9701  mov      ecx, dword ptr [rbx + 0xb4]
003C9707  call     0x1edec0  ; -> 001EDEC0 fn
003C970C  test     eax, eax
003C970E  je       0x3c982e  ; -> 003C982E
003C9714  movzx    eax, byte ptr [rbx + 0xc2]
003C971B  test     al, al
003C971D  je       0x3c982e  ; -> 003C982E
003C9723  sub      al, 1
003C9725  mov      byte ptr [rbx + 0xc2], al
003C972B  jne      0x3c982e  ; -> 003C982E
003C9731  movzx    ecx, byte ptr [rbx + 0xc1]
003C9738  lea      rdx, [rip - 0x2a973f]  ; -> 00120000 (image base)
003C973F  movzx    eax, byte ptr [rcx + rdx + 0xbf1728]
003C9747  movzx    edx, byte ptr [rcx + rdx + 0xbf1720]
003C974F  mov      byte ptr [rbx + 0xc1], dl
003C9755  mov      byte ptr [rbx + 0xc2], al
003C975B  sub      edx, 3
003C975E  je       0x3c9772  ; -> 003C9772
003C9760  cmp      edx, 1
003C9763  jne      0x3c982e  ; -> 003C982E
003C9769  mov      byte ptr [rbx + 0xc3], 0
003C9770  jmp      0x3c9779  ; -> 003C9779
003C9772  mov      byte ptr [rbx + 0xc3], 1
003C9779  mov      rax, qword ptr [rbx + 0x60]
003C977D  mov      r8, qword ptr [rax]
003C9780  movzx    eax, byte ptr [rbx + 0xc3]
003C9787  neg      al
003C9789  movzx    eax, byte ptr [rbx + 0xc0]
003C9790  sbb      edx, edx
003C9792  and      edx, 7
003C9795  add      edx, eax
003C9797  mov      rax, qword ptr [r8 + 0x20]
003C979B  movsxd   rcx, edx
003C979E  movzx    ecx, byte ptr [rax + rcx*8 + 7]
003C97A3  xor      eax, eax
003C97A5  mov      byte ptr [r8 + 0x39], cl
003C97A9  mov      word ptr [r8 + 0xa], dx
003C97AE  add      rsp, 0x20
003C97B2  pop      rbx
003C97B3  ret      
003C97B4  mov      rax, qword ptr [rip + 0x1cd1475]  ; -> 0209AC30
003C97BB  lea      rcx, [rbx + 0x50]
003C97BF  mov      r9, rbx
003C97C2  mov      r8d, 4
003C97C8  mov      rdx, qword ptr [rax + 0x10]
003C97CC  call     0x2432b0  ; -> 002432B0 fn
003C97D1  movzx    ecx, word ptr [rax + 0xa]
003C97D5  movzx    edx, word ptr [rax + 8]
003C97D9  movsx    r8d, word ptr [rax + 6]
003C97DE  test     rbx, rbx
003C97E1  je       0x3c9804  ; -> 003C9804
003C97E3  movzx    eax, word ptr [rax + 4]
003C97E7  mov      word ptr [rbx + 0x98], ax
003C97EE  mov      word ptr [rbx + 0x9a], r8w
003C97F6  mov      word ptr [rbx + 0x9c], dx
003C97FD  mov      word ptr [rbx + 0x9e], cx
003C9804  mov      edx, 0x64
003C9809  mov      rcx, rbx
003C980C  call     0x247930  ; -> 00247930 fn
003C9811  mov      edx, 3
003C9816  mov      rcx, rbx
003C9819  call     0x394700  ; -> 00394700 fn
003C981E  mov      word ptr [rbx + 0xc0], 7
003C9827  mov      byte ptr [rbx + 0xc2], 0
003C982E  xor      eax, eax
003C9830  add      rsp, 0x20
003C9834  pop      rbx
003C9835  ret      
```

## 003FCFE0 (494 B, extent 003FCFE0-003FD1CE)

Documented callee on this page: `00282EA0`

```
003FCFE0  mov      qword ptr [rsp + 0x10], rbx
003FCFE5  mov      qword ptr [rsp + 0x18], rbp
003FCFEA  push     rsi
003FCFEB  push     rdi
003FCFEC  push     r14
003FCFEE  sub      rsp, 0x30
003FCFF2  mov      rax, qword ptr [rdx + 0x10]
003FCFF6  mov      rbx, rcx
003FCFF9  xor      ecx, ecx
003FCFFB  movsxd   r14, r9d
003FCFFE  mov      rbp, rdx
003FD001  mov      rdi, qword ptr [rax + 8]
003FD005  call     0x2dd7e0  ; -> 002DD7E0 fn
003FD00A  mov      rcx, qword ptr [rbx + 0xe0]
003FD011  mov      esi, eax
003FD013  test     rcx, rcx
003FD016  jne      0x3fd088  ; -> 003FD088
003FD018  mov      rcx, qword ptr [rbx + 0x60]
003FD01C  xor      edx, edx
003FD01E  movzx    r8d, byte ptr [rbx + 0x180]
003FD026  mov      rbx, qword ptr [rcx + r8*8]
003FD02A  mov      rcx, rbp
003FD02D  call     0x243580  ; -> 00243580 fn
003FD032  or       dword ptr [rdi + 8], 1
003FD036  mov      ecx, 0x867
003FD03B  call     0x2f9860  ; -> 002F9860 fn
003FD040  mov      r9, qword ptr [rbx + 0x18]
003FD044  mov      r8, rax
003FD047  lea      rbx, [rip + 0x27621d2]  ; -> 02B5F220
003FD04E  mov      ecx, 0x80
003FD053  mov      rdx, rbx
003FD056  call     0x2b4090  ; -> 002B4090 fn
003FD05B  xor      ecx, ecx
003FD05D  mov      dword ptr [rdi + 0x24], esi
003FD060  mov      qword ptr [rdi + 0x18], rbx
003FD064  call     0x20e620  ; -> 0020E620 fn
003FD069  mov      rcx, qword ptr [rdi]
003FD06C  mov      dword ptr [rdi + 0x20], eax
003FD06F  movzx    eax, word ptr [rcx + 4]
003FD073  sub      ax, 0x14
003FD077  mov      word ptr [rdi + 0xc], ax
003FD07B  movzx    eax, word ptr [rcx + 6]
003FD07F  mov      word ptr [rdi + 0xe], ax
003FD083  jmp      0x3fd1b6  ; -> 003FD1B6
003FD088  mov      dword ptr [rdi + 0x24], esi
003FD08B  mov      rax, qword ptr [rip + 0x1c9db9e]  ; -> 0209AC30
003FD092  movsx    esi, byte ptr [rbx + 0x17e]
003FD099  shl      r14, 5
003FD09D  add      r14, rcx
003FD0A0  mov      qword ptr [rsp + 0x50], r15
003FD0A5  movsx    ecx, word ptr [rax + 0xde0]
003FD0AC  call     0x282ea0  ; -> 00282EA0 fn
003FD0B1  movzx    ebx, byte ptr [r14 + 0xb]
003FD0B6  mov      ecx, eax
003FD0B8  movzx    edi, word ptr [r14 + 8]
003FD0BD  call     0x31c4c0  ; -> 0031C4C0 fn
003FD0C2  xor      r15d, r15d
003FD0C5  mov      ecx, eax
003FD0C7  mov      r9d, esi
003FD0CA  mov      dword ptr [rsp + 0x20], r15d
003FD0CF  mov      r8d, ebx
003FD0D2  mov      edx, edi
003FD0D4  call     0x27f030  ; -> 0027F030 fn
003FD0D9  cmp      byte ptr [r14 + 0xa], 0xff
003FD0DE  mov      edi, eax
003FD0E0  mov      rcx, qword ptr [rbp + 0x10]
003FD0E4  mov      rdx, qword ptr [rcx]
003FD0E7  jne      0x3fd0ef  ; -> 003FD0EF
003FD0E9  and      dword ptr [rdx + 8], 0xfffffffe
003FD0ED  jmp      0x3fd111  ; -> 003FD111
003FD0EF  or       dword ptr [rdx + 8], 1
003FD0F3  mov      rax, qword ptr [rbp + 0x10]
003FD0F7  movzx    edx, byte ptr [r14 + 0xa]
003FD0FC  mov      r8, qword ptr [rax]
003FD0FF  mov      rax, qword ptr [r8 + 0x20]
003FD103  movzx    ecx, byte ptr [rax + rdx*8 + 7]
003FD108  mov      byte ptr [r8 + 0x39], cl
003FD10C  mov      word ptr [r8 + 0xa], dx
003FD111  mov      rax, qword ptr [rbp + 0x10]
003FD115  xor      ecx, ecx
003FD117  mov      rbx, qword ptr [rax + 8]
003FD11B  mov      rax, qword ptr [r14]
003FD11E  mov      qword ptr [rbx + 0x18], rax
003FD122  call     0x20e620  ; -> 0020E620 fn
003FD127  mov      rcx, qword ptr [rbx]
003FD12A  mov      dword ptr [rbx + 0x20], eax
003FD12D  movzx    eax, word ptr [rcx + 4]
003FD131  mov      word ptr [rbx + 0xc], ax
003FD135  movzx    eax, word ptr [rcx + 6]
003FD139  mov      word ptr [rbx + 0xe], ax
003FD13D  test     edi, edi
003FD13F  je       0x3fd148  ; -> 003FD148
003FD141  mov      ecx, 2
003FD146  jmp      0x3fd14a  ; -> 003FD14A
003FD148  xor      ecx, ecx
003FD14A  call     0x2dd7e0  ; -> 002DD7E0 fn
003FD14F  mov      dword ptr [rbx + 0x24], eax
003FD152  xor      r8d, r8d
003FD155  mov      rcx, qword ptr [rbp + 0x10]
003FD159  xor      edx, edx
003FD15B  movsx    eax, word ptr [r14 + 0xc]
003FD160  movzx    r9d, word ptr [r14 + 0xe]
003FD165  sub      r9d, eax
003FD168  mov      qword ptr [rsp + 0x28], r15
003FD16D  mov      rcx, qword ptr [rcx + 0x18]
003FD171  mov      dword ptr [rsp + 0x20], r15d
003FD176  call     0x29ff60  ; -> 0029FF60 fn
003FD17B  mov      rcx, qword ptr [rbp + 0x10]
003FD17F  xor      r8d, r8d
003FD182  movzx    r9d, word ptr [r14 + 0xe]
003FD187  xor      edx, edx
003FD189  mov      qword ptr [rsp + 0x28], r15
003FD18E  mov      dword ptr [rsp + 0x20], r15d
003FD193  mov      rcx, qword ptr [rcx + 0x10]
003FD197  call     0x29ff60  ; -> 0029FF60 fn
003FD19C  mov      r9d, 0xa
003FD1A2  mov      rdx, r14
003FD1A5  mov      rcx, rbp
003FD1A8  lea      r8d, [r9 - 5]
003FD1AC  call     0x3fcad0  ; -> 003FCAD0 fn
003FD1B1  mov      r15, qword ptr [rsp + 0x50]
003FD1B6  mov      rbx, qword ptr [rsp + 0x58]
003FD1BB  mov      eax, 1
003FD1C0  mov      rbp, qword ptr [rsp + 0x60]
003FD1C5  add      rsp, 0x30
003FD1C9  pop      r14
003FD1CB  pop      rdi
003FD1CC  pop      rsi
003FD1CD  ret      
```

## 003FD1D0 (228 B, extent 003FD1D0-003FD2B4)

Documented callee on this page: `0029FB50`

```
003FD1D0  push     rbx
003FD1D2  sub      rsp, 0x20
003FD1D6  mov      rbx, rcx
003FD1D9  mov      ecx, dword ptr [rdx]
003FD1DB  sub      ecx, 1
003FD1DE  je       0x3fd221  ; -> 003FD221
003FD1E0  sub      ecx, 0xb
003FD1E3  je       0x3fd1fb  ; -> 003FD1FB
003FD1E5  cmp      ecx, 6
003FD1E8  je       0x3fd2ac  ; -> 003FD2AC
003FD1EE  mov      rcx, rbx
003FD1F1  add      rsp, 0x20
003FD1F5  pop      rbx
003FD1F6  jmp      0x5c5230  ; -> 005C5230 fn
003FD1FB  test     rbx, rbx
003FD1FE  je       0x3fd219  ; -> 003FD219
003FD200  mov      rcx, qword ptr [rbx + 0x10]
003FD204  test     rcx, rcx
003FD207  je       0x3fd219  ; -> 003FD219
003FD209  mov      rax, qword ptr [rcx]
003FD20C  test     rax, rax
003FD20F  je       0x3fd219  ; -> 003FD219
003FD211  add      rsp, 0x20
003FD215  pop      rbx
003FD216  jmp      rax
003FD219  xor      eax, eax
003FD21B  add      rsp, 0x20
003FD21F  pop      rbx
003FD220  ret      
003FD221  mov      rax, qword ptr [rip + 0x1c9da08]  ; -> 0209AC30
003FD228  lea      rcx, [rbx + 0x50]
003FD22C  mov      r9, rbx
003FD22F  mov      r8d, 0xb
003FD235  mov      rdx, qword ptr [rax + 0x40]
003FD239  call     0x2432b0  ; -> 002432B0 fn
003FD23E  movzx    ecx, word ptr [rax + 0xa]
003FD242  movzx    edx, word ptr [rax + 8]
003FD246  movsx    r8d, word ptr [rax + 6]
003FD24B  test     rbx, rbx
003FD24E  je       0x3fd27b  ; -> 003FD27B
003FD250  movzx    eax, word ptr [rax + 4]
003FD254  mov      word ptr [rbx + 0x98], ax
003FD25B  mov      rax, qword ptr [rbx + 0x60]
003FD25F  mov      word ptr [rbx + 0x9a], r8w
003FD267  mov      word ptr [rbx + 0x9c], dx
003FD26E  mov      word ptr [rbx + 0x9e], cx
003FD275  mov      rax, qword ptr [rax + 0x20]
003FD279  jmp      0x3fd27d  ; -> 003FD27D
003FD27B  xor      eax, eax
003FD27D  mov      rax, qword ptr [rax + 0x18]
003FD281  lea      rcx, [rip - 0x2a8]  ; -> 003FCFE0
003FD288  mov      qword ptr [rbx + 0xc0], rax
003FD28F  mov      qword ptr [rax + 0x120], rcx
003FD296  call     0x254a10  ; -> 00254A10 fn
003FD29B  test     eax, eax
003FD29D  jne      0x3fd2ac  ; -> 003FD2AC
003FD29F  mov      rax, qword ptr [rbx + 0x60]
003FD2A3  mov      rcx, qword ptr [rax + 0x30]
003FD2A7  call     0x29fb50  ; -> 0029FB50 fn
003FD2AC  xor      eax, eax
003FD2AE  add      rsp, 0x20
003FD2B2  pop      rbx
003FD2B3  ret      
```

## 003FDDE0 (508 B, extent 003FDDE0-003FDFDC)

Documented callee on this page: `00282EA0`

```
003FDDE0  mov      qword ptr [rsp + 0x18], rbx
003FDDE5  mov      qword ptr [rsp + 0x20], rbp
003FDDEA  push     rsi
003FDDEB  push     rdi
003FDDEC  push     r14
003FDDEE  sub      rsp, 0x30
003FDDF2  mov      rax, qword ptr [rdx + 0x10]
003FDDF6  mov      rbx, rcx
003FDDF9  xor      ecx, ecx
003FDDFB  movsxd   rsi, r9d
003FDDFE  mov      rbp, rdx
003FDE01  mov      r14, qword ptr [rax + 8]
003FDE05  call     0x2dd7e0  ; -> 002DD7E0 fn
003FDE0A  mov      rcx, qword ptr [rbx + 0xe0]
003FDE11  mov      edi, eax
003FDE13  test     rcx, rcx
003FDE16  jne      0x3fde8d  ; -> 003FDE8D
003FDE18  mov      rcx, qword ptr [rbx + 0x60]
003FDE1C  xor      edx, edx
003FDE1E  movzx    r8d, byte ptr [rbx + 0x180]
003FDE26  mov      rbx, qword ptr [rcx + r8*8]
003FDE2A  mov      rcx, rbp
003FDE2D  call     0x243580  ; -> 00243580 fn
003FDE32  or       dword ptr [r14 + 8], 1
003FDE37  mov      ecx, 0x867
003FDE3C  call     0x2f9860  ; -> 002F9860 fn
003FDE41  mov      r9, qword ptr [rbx + 0x18]
003FDE45  mov      r8, rax
003FDE48  lea      rbx, [rip + 0x27613d1]  ; -> 02B5F220
003FDE4F  mov      ecx, 0x80
003FDE54  mov      rdx, rbx
003FDE57  call     0x2b4090  ; -> 002B4090 fn
003FDE5C  xor      ecx, ecx
003FDE5E  mov      dword ptr [r14 + 0x24], edi
003FDE62  mov      qword ptr [r14 + 0x18], rbx
003FDE66  call     0x20e620  ; -> 0020E620 fn
003FDE6B  mov      rcx, qword ptr [r14]
003FDE6E  mov      dword ptr [r14 + 0x20], eax
003FDE72  movzx    eax, word ptr [rcx + 4]
003FDE76  sub      ax, 0x14
003FDE7A  mov      word ptr [r14 + 0xc], ax
003FDE7F  movzx    eax, word ptr [rcx + 6]
003FDE83  mov      word ptr [r14 + 0xe], ax
003FDE88  jmp      0x3fdfc4  ; -> 003FDFC4
003FDE8D  mov      dword ptr [r14 + 0x24], edi
003FDE91  mov      rax, qword ptr [rip + 0x1c9cd98]  ; -> 0209AC30
003FDE98  mov      qword ptr [rsp + 0x50], r12
003FDE9D  mov      qword ptr [rsp + 0x58], r15
003FDEA2  mov      r15, rsi
003FDEA5  movsx    esi, byte ptr [rbx + 0x17e]
003FDEAC  shl      r15, 5
003FDEB0  add      r15, rcx
003FDEB3  movsx    ecx, word ptr [rax + 0xde0]
003FDEBA  call     0x282ea0  ; -> 00282EA0 fn
003FDEBF  movzx    ebx, byte ptr [r15 + 0xb]
003FDEC4  mov      ecx, eax
003FDEC6  movzx    edi, word ptr [r15 + 8]
003FDECB  call     0x31c4c0  ; -> 0031C4C0 fn
003FDED0  xor      r12d, r12d
003FDED3  mov      ecx, eax
003FDED5  mov      r9d, esi
003FDED8  mov      dword ptr [rsp + 0x20], r12d
003FDEDD  mov      r8d, ebx
003FDEE0  mov      edx, edi
003FDEE2  call     0x27f030  ; -> 0027F030 fn
003FDEE7  cmp      byte ptr [r15 + 0xa], 0xff
003FDEEC  mov      edi, eax
003FDEEE  jne      0x3fdef7  ; -> 003FDEF7
003FDEF0  and      dword ptr [r14 + 8], 0xfffffffe
003FDEF5  jmp      0x3fdf1a  ; -> 003FDF1A
003FDEF7  or       dword ptr [r14 + 8], 1
003FDEFC  mov      rax, qword ptr [rbp + 0x10]
003FDF00  movzx    edx, byte ptr [r15 + 0xa]
003FDF05  mov      r8, qword ptr [rax]
003FDF08  mov      rax, qword ptr [r8 + 0x20]
003FDF0C  movzx    ecx, byte ptr [rax + rdx*8 + 7]
003FDF11  mov      byte ptr [r8 + 0x39], cl
003FDF15  mov      word ptr [r8 + 0xa], dx
003FDF1A  mov      rax, qword ptr [rbp + 0x10]
003FDF1E  xor      ecx, ecx
003FDF20  mov      rbx, qword ptr [rax + 8]
003FDF24  mov      rax, qword ptr [r15]
003FDF27  mov      qword ptr [rbx + 0x18], rax
003FDF2B  call     0x20e620  ; -> 0020E620 fn
003FDF30  mov      rcx, qword ptr [rbx]
003FDF33  mov      dword ptr [rbx + 0x20], eax
003FDF36  movzx    eax, word ptr [rcx + 4]
003FDF3A  mov      word ptr [rbx + 0xc], ax
003FDF3E  movzx    eax, word ptr [rcx + 6]
003FDF42  mov      word ptr [rbx + 0xe], ax
003FDF46  test     edi, edi
003FDF48  je       0x3fdf51  ; -> 003FDF51
003FDF4A  mov      ecx, 2
003FDF4F  jmp      0x3fdf53  ; -> 003FDF53
003FDF51  xor      ecx, ecx
003FDF53  call     0x2dd7e0  ; -> 002DD7E0 fn
003FDF58  mov      dword ptr [rbx + 0x24], eax
003FDF5B  xor      r8d, r8d
003FDF5E  mov      rcx, qword ptr [rbp + 0x10]
003FDF62  xor      edx, edx
003FDF64  movsx    eax, word ptr [r15 + 0xc]
003FDF69  movzx    r9d, word ptr [r15 + 0xe]
003FDF6E  sub      r9d, eax
003FDF71  mov      qword ptr [rsp + 0x28], r12
003FDF76  mov      rcx, qword ptr [rcx + 0x18]
003FDF7A  mov      dword ptr [rsp + 0x20], r12d
003FDF7F  call     0x29ff60  ; -> 0029FF60 fn
003FDF84  mov      rcx, qword ptr [rbp + 0x10]
003FDF88  xor      r8d, r8d
003FDF8B  movzx    r9d, word ptr [r15 + 0xe]
003FDF90  xor      edx, edx
003FDF92  mov      qword ptr [rsp + 0x28], r12
003FDF97  mov      dword ptr [rsp + 0x20], r12d
003FDF9C  mov      rcx, qword ptr [rcx + 0x10]
003FDFA0  call     0x29ff60  ; -> 0029FF60 fn
003FDFA5  mov      r9d, 0xa
003FDFAB  mov      rdx, r15
003FDFAE  mov      rcx, rbp
003FDFB1  lea      r8d, [r9 - 5]
003FDFB5  call     0x3fcad0  ; -> 003FCAD0 fn
003FDFBA  mov      r15, qword ptr [rsp + 0x58]
003FDFBF  mov      r12, qword ptr [rsp + 0x50]
003FDFC4  mov      rbx, qword ptr [rsp + 0x60]
003FDFC9  mov      eax, 1
003FDFCE  mov      rbp, qword ptr [rsp + 0x68]
003FDFD3  add      rsp, 0x30
003FDFD7  pop      r14
003FDFD9  pop      rdi
003FDFDA  pop      rsi
003FDFDB  ret      
```

## 003FF1F0 (367 B, extent 003FF1F0-003FF35F)

Documented callee on this page: `0029FB50`

```
003FF1F0  mov      qword ptr [rsp + 8], rbx
003FF1F5  mov      qword ptr [rsp + 0x10], rbp
003FF1FA  mov      qword ptr [rsp + 0x18], rsi
003FF1FF  mov      qword ptr [rsp + 0x20], rdi
003FF204  push     r12
003FF206  push     r14
003FF208  push     r15
003FF20A  sub      rsp, 0x40
003FF20E  mov      rax, qword ptr [rdx + 0x10]
003FF212  mov      r15, rdx
003FF215  movsxd   rbp, r9d
003FF218  mov      rsi, rcx
003FF21B  mov      rdx, rbp
003FF21E  xor      r14d, r14d
003FF221  shl      rdx, 5
003FF225  mov      rbx, qword ptr [rax + 0x10]
003FF229  mov      rax, qword ptr [rcx + 0xc8]
003FF230  lea      rdi, [rbp + 0x6a]
003FF234  shl      rdi, 5
003FF238  xor      ecx, ecx
003FF23A  add      rdi, qword ptr [rip + 0x1c9b9ef]  ; -> 0209AC30
003FF241  mov      rdx, qword ptr [rdx + rax + 0x10]
003FF246  mov      qword ptr [rbx + 0x18], rdx
003FF24A  call     0x20e620  ; -> 0020E620 fn
003FF24F  mov      rcx, rbx
003FF252  mov      dword ptr [rbx + 0x20], eax
003FF255  call     0x29fb50  ; -> 0029FB50 fn
003FF25A  cmp      dword ptr [rsi + 0x178], 0x402
003FF264  mov      r12d, 0xffff
003FF26A  movups   xmm0, xmmword ptr [rdi]
003FF26D  movups   xmmword ptr [rsp + 0x20], xmm0
003FF272  movzx    edi, word ptr [rsp + 0x28]
003FF277  jne      0x3ff2ce  ; -> 003FF2CE
003FF279  lea      rax, [rip + 0x275ff90]  ; -> 02B5F210
003FF280  movzx    eax, word ptr [rax + rbp*2]
003FF284  cmp      di, ax
003FF287  je       0x3ff2ce  ; -> 003FF2CE
003FF289  mov      r14d, 1
003FF28F  movzx    edi, ax
003FF292  cmp      ax, r12w
003FF296  je       0x3ff2bd  ; -> 003FF2BD
003FF298  movzx    edx, ax
003FF29B  mov      ecx, r14d
003FF29E  shl      edx, 0x10
003FF2A1  call     0x35d330  ; -> 0035D330 fn
003FF2A6  xor      edx, edx
003FF2A8  mov      rbx, rax
003FF2AB  mov      rcx, qword ptr [rax + 0x18]
003FF2AF  call     0x2b58b0  ; -> 002B58B0 fn
003FF2B4  movzx    ebx, byte ptr [rbx + 0x2c]
003FF2B8  mov      rsi, rax
003FF2BB  jmp      0x3ff2d8  ; -> 003FF2D8
003FF2BD  mov      ecx, 0x3ea
003FF2C2  call     0x2f9860  ; -> 002F9860 fn
003FF2C7  mov      rsi, rax
003FF2CA  mov      bl, 0xff
003FF2CC  jmp      0x3ff2d8  ; -> 003FF2D8
003FF2CE  mov      rsi, qword ptr [rsp + 0x20]
003FF2D3  movzx    ebx, byte ptr [rsp + 0x2a]
003FF2D8  mov      rax, qword ptr [r15 + 0x10]
003FF2DC  neg      r14d
003FF2DF  sbb      ecx, ecx
003FF2E1  and      ecx, 5
003FF2E4  mov      rbp, qword ptr [rax + 8]
003FF2E8  call     0x2dd7e0  ; -> 002DD7E0 fn
003FF2ED  mov      dword ptr [rbp + 0x24], eax
003FF2F0  cmp      bl, 0xff
003FF2F3  jne      0x3ff302  ; -> 003FF302
003FF2F5  mov      ecx, 4
003FF2FA  call     0x2dd7e0  ; -> 002DD7E0 fn
003FF2FF  mov      dword ptr [rbp + 0x24], eax
003FF302  xor      ecx, ecx
003FF304  mov      qword ptr [rbp + 0x18], rsi
003FF308  call     0x20e620  ; -> 0020E620 fn
003FF30D  mov      dword ptr [rbp + 0x20], eax
003FF310  mov      eax, 1
003FF315  mov      rcx, qword ptr [r15 + 0x10]
003FF319  mov      r9, qword ptr [rcx]
003FF31C  cmp      di, r12w
003FF320  je       0x3ff33b  ; -> 003FF33B
003FF322  mov      rcx, qword ptr [r9 + 0x20]
003FF326  movzx    r8d, bl
003FF32A  movzx    edx, byte ptr [rcx + r8*8 + 7]
003FF330  mov      byte ptr [r9 + 0x39], dl
003FF334  mov      word ptr [r9 + 0xa], r8w
003FF339  jmp      0x3ff340  ; -> 003FF340
003FF33B  and      dword ptr [r9 + 8], 0xfffffffe
003FF340  mov      rbx, qword ptr [rsp + 0x60]
003FF345  mov      rbp, qword ptr [rsp + 0x68]
003FF34A  mov      rsi, qword ptr [rsp + 0x70]
003FF34F  mov      rdi, qword ptr [rsp + 0x78]
003FF354  add      rsp, 0x40
003FF358  pop      r15
003FF35A  pop      r14
003FF35C  pop      r12
003FF35E  ret      
```

## 0053EEA0 (273 B, extent 0053EEA0-0053EFB1)

Documented callee on this page: `002F83E0`

```
0053EEA0  mov      qword ptr [rsp + 8], rbx
0053EEA5  push     rdi
0053EEA6  sub      rsp, 0x20
0053EEAA  mov      r8d, dword ptr [rdx]
0053EEAD  mov      rdi, rcx
0053EEB0  sub      r8d, 1
0053EEB4  je       0x53ef15  ; -> 0053EF15
0053EEB6  sub      r8d, 1
0053EEBA  je       0x53eeed  ; -> 0053EEED
0053EEBC  cmp      r8d, 0xe
0053EEC0  je       0x53eed1  ; -> 0053EED1
0053EEC2  mov      rbx, qword ptr [rsp + 0x30]
0053EEC7  add      rsp, 0x20
0053EECB  pop      rdi
0053EECC  jmp      0x5c5230  ; -> 005C5230 fn
0053EED1  call     0x16d6a0  ; -> 0016D6A0 fn
0053EED6  xor      eax, eax
0053EED8  mov      dword ptr [rdi + 0xc0], 1
0053EEE2  mov      rbx, qword ptr [rsp + 0x30]
0053EEE7  add      rsp, 0x20
0053EEEB  pop      rdi
0053EEEC  ret      
0053EEED  cmp      dword ptr [rcx + 0xc0], 0
0053EEF4  je       0x53efa4  ; -> 0053EFA4
0053EEFA  xor      ebx, ebx
0053EEFC  mov      qword ptr [rip + 0x2769b75], rbx  ; -> 02CA8A78
0053EF03  call     0x245020  ; -> 00245020 fn
0053EF08  xor      eax, eax
0053EF0A  mov      rbx, qword ptr [rsp + 0x30]
0053EF0F  add      rsp, 0x20
0053EF13  pop      rdi
0053EF14  ret      
0053EF15  mov      rcx, qword ptr [rip + 0x2769b6c]  ; -> 02CA8A88
0053EF1C  xor      ebx, ebx
0053EF1E  mov      qword ptr [rip + 0x2769b53], rdi  ; -> 02CA8A78
0053EF25  test     rcx, rcx
0053EF28  je       0x53ef39  ; -> 0053EF39
0053EF2A  lea      edx, [rbx + 1]
0053EF2D  call     0x24a680  ; -> 0024A680 fn
0053EF32  mov      qword ptr [rip + 0x2769b4f], rbx  ; -> 02CA8A88
0053EF39  mov      ecx, 0x19
0053EF3E  call     0x2f8040  ; -> 002F8040 fn
0053EF43  test     eax, eax
0053EF45  je       0x53ef51  ; -> 0053EF51
0053EF47  mov      ecx, 0x19
0053EF4C  call     0x2f83e0  ; -> 002F83E0 fn
0053EF51  mov      ecx, 0x1a
0053EF56  call     0x2f8040  ; -> 002F8040 fn
0053EF5B  test     eax, eax
0053EF5D  je       0x53ef70  ; -> 0053EF70
0053EF5F  mov      ecx, 0x1a
0053EF64  call     0x2f83e0  ; -> 002F83E0 fn
0053EF69  nop      dword ptr [rax]
0053EF70  lea      ecx, [rbx + 7]
0053EF73  call     0x365570  ; -> 00365570 fn
0053EF78  inc      ebx
0053EF7A  cmp      ebx, 6
0053EF7D  jl       0x53ef70  ; -> 0053EF70
0053EF7F  mov      rcx, rdi
0053EF82  call     0x249580  ; -> 00249580 fn
0053EF87  mov      rcx, rax
0053EF8A  mov      rbx, rax
0053EF8D  call     0x16d6a0  ; -> 0016D6A0 fn
0053EF92  mov      rcx, rbx
0053EF95  call     0x249410  ; -> 00249410 fn
0053EF9A  xor      edx, edx
0053EF9C  mov      rcx, rdi
0053EF9F  call     0x247950  ; -> 00247950 fn
0053EFA4  xor      eax, eax
0053EFA6  mov      rbx, qword ptr [rsp + 0x30]
0053EFAB  add      rsp, 0x20
0053EFAF  pop      rdi
0053EFB0  ret      
```

## 0057F8C0 (357 B, extent 0057F8C0-0057FA25)

Documented callee on this page: `0057FB00`

```
0057F8C0  push     rbx
0057F8C2  push     rdi
0057F8C3  push     r14
0057F8C5  sub      rsp, 0x40
0057F8C9  mov      qword ptr [rsp + 0x68], rbp
0057F8CE  xor      ebx, ebx
0057F8D0  test     byte ptr [rcx + 0xe0], 1
0057F8D7  mov      rdi, rdx
0057F8DA  mov      qword ptr [rsp + 0x70], rsi
0057F8DF  mov      rbp, rcx
0057F8E2  mov      qword ptr [rsp + 0x38], r12
0057F8E7  mov      r12, r8
0057F8EA  mov      qword ptr [rsp + 0x30], r15
0057F8EF  movsxd   r15, r9d
0057F8F2  movzx    r14d, byte ptr [r15 + rcx + 0xef]
0057F8FB  jne      0x57f932  ; -> 0057F932
0057F8FD  mov      ecx, r14d
0057F900  call     0x3bb3e0  ; -> 003BB3E0 fn
0057F905  mov      rsi, rax
0057F908  cmp      dword ptr [rax], 2
0057F90B  jne      0x57f947  ; -> 0057F947
0057F90D  movzx    eax, byte ptr [r15 + rbp + 0xef]
0057F916  mov      rdx, r12
0057F919  mov      rcx, rdi
0057F91C  lea      r8, [rax + rax*4]
0057F920  shl      r8, 5
0057F924  add      r8, qword ptr [rbp + 0x1c0]
0057F92B  call     0x57fb00  ; -> 0057FB00 fn
0057F930  jmp      0x57f978  ; -> 0057F978
0057F932  mov      dword ptr [rsp + 0x60], 5
0057F93A  lea      rsi, [rsp + 0x60]
0057F93F  mov      dword ptr [rsp + 0x64], 1
0057F947  mov      edx, 1
0057F94C  cmp      byte ptr [rbp + 0xea], bl
0057F952  jne      0x57f95a  ; -> 0057F95A
0057F954  cmp      dword ptr [rsi + 4], ebx
0057F957  cmovne   edx, ebx
0057F95A  mov      rcx, qword ptr [rdi + 0x10]
0057F95E  mov      rcx, qword ptr [rcx + 0xb0]
0057F965  call     0x393240  ; -> 00393240 fn
0057F96A  mov      r8, rsi
0057F96D  mov      rdx, r12
0057F970  mov      rcx, rdi
0057F973  call     0x57fa30  ; -> 0057FA30 fn
0057F978  cmp      byte ptr [rbp + 0xea], 1
0057F97F  mov      rbp, qword ptr [rsp + 0x68]
0057F984  mov      r15, qword ptr [rsp + 0x30]
0057F989  mov      r12, qword ptr [rsp + 0x38]
0057F98E  mov      rsi, qword ptr [rsp + 0x70]
0057F993  jne      0x57f9d9  ; -> 0057F9D9
0057F995  test     r14d, r14d
0057F998  jne      0x57f9d9  ; -> 0057F9D9
0057F99A  lea      r9, [rip + 0x19ad36f]  ; -> 01F2CD10
0057F9A1  movsxd   rdx, dword ptr [r9]
0057F9A4  lea      r9, [r9 + 4]
0057F9A8  mov      rcx, qword ptr [rdi + 0x10]
0057F9AC  inc      ebx
0057F9AE  mov      r8, qword ptr [rcx + rdx*8]
0057F9B2  and      dword ptr [r8 + 8], 0xfffffffe
0057F9B7  cmp      ebx, 6
0057F9BA  jb       0x57f9a1  ; -> 0057F9A1
0057F9BC  mov      rcx, qword ptr [rdi + 0x10]
0057F9C0  mov      eax, 1
0057F9C5  mov      rdx, qword ptr [rcx + 0xd0]
0057F9CC  or       dword ptr [rdx + 8], 1
0057F9D0  add      rsp, 0x40
0057F9D4  pop      r14
0057F9D6  pop      rdi
0057F9D7  pop      rbx
0057F9D8  ret      
0057F9D9  mov      edx, 4
0057F9DE  mov      ebx, 0xc7
0057F9E3  cmp      r14d, ebx
0057F9E6  mov      rcx, rdi
0057F9E9  cmovb    ebx, r14d
0057F9ED  lea      r9d, [rdx + 5]
0057F9F1  mov      dword ptr [rsp + 0x20], ebx
0057F9F5  lea      r8d, [rdx - 1]
0057F9F9  call     0x393160  ; -> 00393160 fn
0057F9FE  mov      edx, 1
0057FA03  mov      dword ptr [rsp + 0x20], ebx
0057FA07  mov      rcx, rdi
0057FA0A  lea      r9d, [rdx + 8]
0057FA0E  lea      r8d, [rdx + 2]
0057FA12  call     0x393160  ; -> 00393160 fn
0057FA17  mov      eax, 1
0057FA1C  add      rsp, 0x40
0057FA20  pop      r14
0057FA22  pop      rdi
0057FA23  pop      rbx
0057FA24  ret      
```
