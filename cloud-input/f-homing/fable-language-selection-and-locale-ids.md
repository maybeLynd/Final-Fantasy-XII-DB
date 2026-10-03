# F homing pack (FABLE): `19-Save-Load-Settings/Language-And-Locale/language-selection-and-locale-ids.md`

Generated 2026-10-03 04:02 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 10. No bearing page cites them and no documented function calls them directly.

## 0023EA10 (456 B, extent 0023EA10-0023EBD8)

Documented callee on this page: `002405F0`

```
0023EA10  push     rdi
0023EA12  sub      rsp, 0x30
0023EA16  mov      rdi, rcx
0023EA19  mov      ecx, dword ptr [rdx]
0023EA1B  sub      ecx, 1
0023EA1E  je       0x23ea6e  ; -> 0023EA6E
0023EA20  sub      ecx, 2
0023EA23  je       0x23ea32  ; -> 0023EA32
0023EA25  mov      rcx, rdi
0023EA28  add      rsp, 0x30
0023EA2C  pop      rdi
0023EA2D  jmp      0x5c5230  ; -> 005C5230 fn
0023EA32  movzx    ecx, byte ptr [rdi + 0xc0]
0023EA39  cmp      cl, 0xff
0023EA3C  jne      0x23ea51  ; -> 0023EA51
0023EA3E  xor      edx, edx
0023EA40  lea      rcx, [rdi + 0x50]
0023EA44  call     0x392fc0  ; -> 00392FC0 fn
0023EA49  xor      eax, eax
0023EA4B  add      rsp, 0x30
0023EA4F  pop      rdi
0023EA50  ret      
0023EA51  call     0x2405f0  ; -> 002405F0 fn
0023EA56  xor      edx, edx
0023EA58  lea      rcx, [rdi + 0x50]
0023EA5C  test     eax, eax
0023EA5E  sete     dl
0023EA61  call     0x392fc0  ; -> 00392FC0 fn
0023EA66  xor      eax, eax
0023EA68  add      rsp, 0x30
0023EA6C  pop      rdi
0023EA6D  ret      
0023EA6E  mov      rax, qword ptr [rip + 0x1e5c1bb]  ; -> 0209AC30
0023EA75  lea      rcx, [rdi + 0x50]
0023EA79  mov      qword ptr [rsp + 0x58], rbx
0023EA7E  mov      r9, rdi
0023EA81  mov      rbx, qword ptr [rdx + 8]
0023EA85  mov      r8d, 0x1c
0023EA8B  mov      qword ptr [rsp + 0x28], rbp
0023EA90  mov      rdx, qword ptr [rax + 0x60]
0023EA94  mov      qword ptr [rsp + 0x20], rsi
0023EA99  call     0x2432b0  ; -> 002432B0 fn
0023EA9E  mov      rsi, rax
0023EAA1  movzx    eax, word ptr [rax + 0xa]
0023EAA5  movzx    edx, word ptr [rsi + 8]
0023EAA9  movsx    r8d, word ptr [rsi + 6]
0023EAAE  test     rdi, rdi
0023EAB1  je       0x23ead4  ; -> 0023EAD4
0023EAB3  movzx    ecx, word ptr [rsi + 4]
0023EAB7  mov      word ptr [rdi + 0x98], cx
0023EABE  mov      word ptr [rdi + 0x9a], r8w
0023EAC6  mov      word ptr [rdi + 0x9c], dx
0023EACD  mov      word ptr [rdi + 0x9e], ax
0023EAD4  movzx    eax, byte ptr [rbx]
0023EAD7  lea      r8, [rsp + 0x50]
0023EADC  mov      byte ptr [rdi + 0xc0], al
0023EAE2  lea      rcx, [rdi + 0x50]
0023EAE6  movzx    eax, byte ptr [rbx + 1]
0023EAEA  xor      edx, edx
0023EAEC  mov      byte ptr [rdi + 0xc1], al
0023EAF2  movzx    eax, byte ptr [rbx + 2]
0023EAF6  mov      byte ptr [rdi + 0xc2], al
0023EAFC  call     0x243260  ; -> 00243260 fn
0023EB01  movzx    eax, byte ptr [rdi + 0xc0]
0023EB08  movzx    ecx, byte ptr [rdi + 0xc1]
0023EB0F  mov      rbp, qword ptr [rsp + 0x28]
0023EB14  cmp      eax, 0x2d
0023EB17  jae      0x23ebab  ; -> 0023EBAB
0023EB1D  lea      rdx, [rip + 0x1bcd43c]  ; -> 01E0BF60
0023EB24  mov      rdx, qword ptr [rdx + rax*8]
0023EB28  test     rdx, rdx
0023EB2B  je       0x23ebab  ; -> 0023EBAB
0023EB2D  movzx    eax, word ptr [rdx + 2]
0023EB31  cmp      ecx, eax
0023EB33  jae      0x23ebab  ; -> 0023EBAB
0023EB35  lea      rax, [rcx + 1]
0023EB39  lea      rax, [rcx + rax*2]
0023EB3D  lea      rax, [rdx + rax*2]
0023EB41  test     rax, rax
0023EB44  je       0x23ebab  ; -> 0023EBAB
0023EB46  movzx    ecx, word ptr [rax + 2]
0023EB4A  cmp      ecx, 0xffff
0023EB50  je       0x23ebab  ; -> 0023EBAB
0023EB52  mov      rax, qword ptr [rdi + 0x60]
0023EB56  mov      rbx, qword ptr [rax]
0023EB59  call     0x2f9860  ; -> 002F9860 fn
0023EB5E  xor      ecx, ecx
0023EB60  mov      qword ptr [rbx + 0x18], rax
0023EB64  call     0x20e620  ; -> 0020E620 fn
0023EB69  lea      r8, [rsp + 0x48]
0023EB6E  mov      dword ptr [rbx + 0x20], eax
0023EB71  lea      rdx, [rsp + 0x40]
0023EB76  mov      rcx, rbx
0023EB79  call     0x29fe20  ; -> 0029FE20 fn
0023EB7E  movsx    ecx, word ptr [rdi + 0x9c]
0023EB85  movsx    eax, word ptr [rsp + 0x54]
0023EB8A  sub      ecx, eax
0023EB8C  add      dword ptr [rsp + 0x40], ecx
0023EB90  or       dword ptr [rbx + 8], 1
0023EB94  movzx    ecx, word ptr [rsi + 0xa]
0023EB98  movzx    eax, word ptr [rsp + 0x40]
0023EB9D  mov      word ptr [rdi + 0x9c], ax
0023EBA4  mov      word ptr [rdi + 0x9e], cx
0023EBAB  and      dword ptr [rdi + 0x40], 0xffffff7f
0023EBB2  mov      edx, 0x64
0023EBB7  or       dword ptr [rdi + 0x40], 0x800
0023EBBE  mov      rcx, rdi
0023EBC1  call     0x247930  ; -> 00247930 fn
0023EBC6  mov      rsi, qword ptr [rsp + 0x20]
0023EBCB  xor      eax, eax
0023EBCD  mov      rbx, qword ptr [rsp + 0x58]
0023EBD2  add      rsp, 0x30
0023EBD6  pop      rdi
0023EBD7  ret      
```

## 002BF8C0 (627 B, extent 002BF8C0-002BFB33)

Documented callee on this page: `00275440`

```
002BF8C0  mov      qword ptr [rsp + 0x18], rbx
002BF8C5  push     rdi
002BF8C6  sub      rsp, 0x50
002BF8CA  mov      rax, qword ptr [rip + 0x1c84f5f]  ; -> 01F44830 [u64 0x00002B992DDFA232]
002BF8D1  xor      rax, rsp
002BF8D4  mov      qword ptr [rsp + 0x48], rax
002BF8D9  mov      rbx, rcx
002BF8DC  mov      rdi, rdx
002BF8DF  mov      ecx, dword ptr [rdx]
002BF8E1  sub      ecx, 1
002BF8E4  je       0x2bfa53  ; -> 002BFA53
002BF8EA  sub      ecx, 1
002BF8ED  je       0x2bf9a4  ; -> 002BF9A4
002BF8F3  cmp      ecx, 2
002BF8F6  je       0x2bf905  ; -> 002BF905
002BF8F8  mov      rcx, rbx
002BF8FB  call     0x5c5230  ; -> 005C5230 fn
002BF900  jmp      0x2bfb1b  ; -> 002BFB1B
002BF905  mov      rdi, qword ptr [rbx + 0x38]
002BF909  mov      dword ptr [rdi + 0x60], 0x3f800000
002BF910  mov      byte ptr [rdi + 0x65], 0
002BF914  mov      eax, dword ptr [rbx + 0xf4]
002BF91A  and      eax, 1
002BF91D  test     al, al
002BF91F  je       0x2bf97f  ; -> 002BF97F
002BF921  cmp      dword ptr [rbx + 0xec], 0
002BF928  jne      0x2bf97f  ; -> 002BF97F
002BF92A  mov      edx, dword ptr [rbx + 0xf0]
002BF930  xor      r8d, r8d
002BF933  mov      rax, qword ptr [rbx + 0xe0]
002BF93A  neg      edx
002BF93C  mov      r9, qword ptr [rbx + 0xd8]
002BF943  mov      rcx, rdi
002BF946  mov      qword ptr [rsp + 0x20], rax
002BF94B  call     0x2d8910  ; -> 002D8910 fn
002BF950  mov      edx, dword ptr [rbx + 0xe8]
002BF956  xor      r8d, r8d
002BF959  mov      rax, qword ptr [rbx + 0xe0]
002BF960  mov      rcx, rdi
002BF963  sub      edx, dword ptr [rbx + 0xf0]
002BF969  mov      r9, qword ptr [rbx + 0xd8]
002BF970  mov      qword ptr [rsp + 0x20], rax
002BF975  call     0x2d8910  ; -> 002D8910 fn
002BF97A  jmp      0x2bfb19  ; -> 002BFB19
002BF97F  mov      rax, qword ptr [rbx + 0xe0]
002BF986  xor      r8d, r8d
002BF989  mov      r9, qword ptr [rbx + 0xd8]
002BF990  xor      edx, edx
002BF992  mov      rcx, rdi
002BF995  mov      qword ptr [rsp + 0x20], rax
002BF99A  call     0x2d8910  ; -> 002D8910 fn
002BF99F  jmp      0x2bfb19  ; -> 002BFB19
002BF9A4  mov      r8d, dword ptr [rbx + 0xf4]
002BF9AB  mov      eax, r8d
002BF9AE  and      eax, 1
002BF9B1  test     al, al
002BF9B3  je       0x2bfa1f  ; -> 002BFA1F
002BF9B5  mov      ecx, dword ptr [rbx + 0xec]
002BF9BB  test     ecx, ecx
002BF9BD  jne      0x2bf9fc  ; -> 002BF9FC
002BF9BF  mov      eax, dword ptr [rbx + 0xf8]
002BF9C5  mov      ecx, dword ptr [rip + 0x1dcfba5]  ; -> 0208F570
002BF9CB  cmp      ecx, eax
002BF9CD  jae      0x2bf9d6  ; -> 002BF9D6
002BF9CF  mov      ecx, 1
002BF9D4  jmp      0x2bf9d8  ; -> 002BF9D8
002BF9D6  sub      ecx, eax
002BF9D8  mov      eax, dword ptr [rbx + 0xf0]
002BF9DE  xor      edx, edx
002BF9E0  add      eax, ecx
002BF9E2  div      dword ptr [rbx + 0xe8]
002BF9E8  mov      dword ptr [rbx + 0xf0], edx
002BF9EE  mov      eax, dword ptr [rip + 0x1dcfb7c]  ; -> 0208F570
002BF9F4  mov      dword ptr [rbx + 0xf8], eax
002BF9FA  jmp      0x2bfa1f  ; -> 002BFA1F
002BF9FC  mov      eax, dword ptr [rip + 0x1dcfb6e]  ; -> 0208F570
002BFA02  mov      dword ptr [rbx + 0xf8], eax
002BFA08  mov      eax, dword ptr [rip + 0x1dcfb62]  ; -> 0208F570
002BFA0E  sub      eax, ecx
002BFA10  cmp      eax, 0x3c
002BFA13  jbe      0x2bfa1f  ; -> 002BFA1F
002BFA15  mov      dword ptr [rbx + 0xec], 0
002BFA1F  test     r8b, 2
002BFA23  jne      0x2bfb19  ; -> 002BFB19
002BFA29  xorps    xmm0, xmm0
002BFA2C  mov      dword ptr [rsp + 0x30], 0xc
002BFA34  lea      rdx, [rsp + 0x30]
002BFA39  mov      rcx, rbx
002BFA3C  movdqu   xmmword ptr [rsp + 0x38], xmm0
002BFA42  call     0x275440  ; -> 00275440 fn
002BFA47  or       dword ptr [rbx + 0xf4], 2
002BFA4E  jmp      0x2bfb19  ; -> 002BFB19
002BFA53  mov      rax, qword ptr [rdx + 8]
002BFA57  mov      rcx, qword ptr [rax]
002BFA5A  and      dword ptr [rbx + 0x40], 0xffffff7f
002BFA61  mov      qword ptr [rbx + 0xc0], rcx
002BFA68  mov      ecx, 1
002BFA6D  call     0x2735e0  ; -> 002735E0 fn
002BFA72  mov      rdx, rax
002BFA75  mov      rcx, rbx
002BFA78  call     0x247570  ; -> 00247570 fn
002BFA7D  xor      edx, edx
002BFA7F  mov      rcx, rbx
002BFA82  call     0x247570  ; -> 00247570 fn
002BFA87  mov      r9, qword ptr [rdi + 8]
002BFA8B  movsx    ecx, word ptr [r9 + 0x26]
002BFA90  movzx    eax, word ptr [r9 + 0x24]
002BFA95  mov      edx, dword ptr [r9 + 0x2c]
002BFA99  movsx    r8d, word ptr [r9 + 0x2a]
002BFA9E  mov      word ptr [rbx + 0x98], ax
002BFAA5  mov      word ptr [rbx + 0x9a], cx
002BFAAC  mov      rcx, rbx
002BFAAF  mov      word ptr [rbx + 0x9c], dx
002BFAB6  mov      edx, 0x4f
002BFABB  mov      word ptr [rbx + 0x9e], r8w
002BFAC3  mov      rax, qword ptr [r9 + 0x10]
002BFAC7  mov      qword ptr [rbx + 0xd8], rax
002BFACE  mov      rax, qword ptr [r9 + 0x18]
002BFAD2  mov      qword ptr [rbx + 0xe0], rax
002BFAD9  mov      eax, dword ptr [r9 + 0x30]
002BFADD  xor      eax, dword ptr [rbx + 0xf4]
002BFAE3  and      eax, 1
002BFAE6  xor      dword ptr [rbx + 0xf4], eax
002BFAEC  mov      eax, dword ptr [rip + 0x1dcfa7e]  ; -> 0208F570
002BFAF2  mov      dword ptr [rbx + 0xec], eax
002BFAF8  movsx    eax, word ptr [r9 + 0x28]
002BFAFD  and      dword ptr [rbx + 0x40], 0xffffff7f
002BFB04  mov      dword ptr [rbx + 0xe8], eax
002BFB0A  mov      dword ptr [rbx + 0xf0], 0
002BFB14  call     0x247930  ; -> 00247930 fn
002BFB19  xor      eax, eax
002BFB1B  mov      rcx, qword ptr [rsp + 0x48]
002BFB20  xor      rcx, rsp
002BFB23  call     0x808c40  ; -> 00808C40 fn
002BFB28  mov      rbx, qword ptr [rsp + 0x70]
002BFB2D  add      rsp, 0x50
002BFB31  pop      rdi
002BFB32  ret      
```

## 002CFE40 (148 B, extent 002CFE40-002CFED4)

Documented callee on this page: `0035D330`

```
002CFE40  mov      qword ptr [rsp + 8], rbx
002CFE45  mov      qword ptr [rsp + 0x10], rbp
002CFE4A  mov      qword ptr [rsp + 0x18], rsi
002CFE4F  push     rdi
002CFE50  sub      rsp, 0x20
002CFE54  mov      rbp, rdx
002CFE57  mov      rsi, rcx
002CFE5A  movzx    edx, word ptr [rcx + 8]
002CFE5E  mov      ecx, 1
002CFE63  shl      edx, 0x10
002CFE66  movzx    ebx, word ptr [rbp + 8]
002CFE6A  call     0x35d330  ; -> 0035D330 fn
002CFE6F  shl      ebx, 0x10
002CFE72  mov      ecx, 1
002CFE77  mov      edx, ebx
002CFE79  mov      edi, dword ptr [rax + 0x38]
002CFE7C  call     0x35d330  ; -> 0035D330 fn
002CFE81  sub      edi, dword ptr [rax + 0x38]
002CFE84  jne      0x2cfebd  ; -> 002CFEBD
002CFE86  movzx    esi, word ptr [rsi + 8]
002CFE8A  mov      ecx, 1
002CFE8F  movzx    edi, word ptr [rbp + 8]
002CFE93  mov      edx, esi
002CFE95  shl      edx, 0x10
002CFE98  call     0x35d330  ; -> 0035D330 fn
002CFE9D  mov      edx, edi
002CFE9F  mov      ecx, 1
002CFEA4  shl      edx, 0x10
002CFEA7  mov      ebx, dword ptr [rax + 0x30]
002CFEAA  call     0x35d330  ; -> 0035D330 fn
002CFEAF  sub      esi, edi
002CFEB1  sub      ebx, dword ptr [rax + 0x30]
002CFEB4  test     ebx, ebx
002CFEB6  cmovne   esi, ebx
002CFEB9  mov      eax, esi
002CFEBB  jmp      0x2cfebf  ; -> 002CFEBF
002CFEBD  mov      eax, edi
002CFEBF  mov      rbx, qword ptr [rsp + 0x30]
002CFEC4  mov      rbp, qword ptr [rsp + 0x38]
002CFEC9  mov      rsi, qword ptr [rsp + 0x40]
002CFECE  add      rsp, 0x20
002CFED2  pop      rdi
002CFED3  ret      
```

## 002D0070 (133 B, extent 002D0070-002D00F5)

Documented callee on this page: `0035D330`

```
002D0070  mov      qword ptr [rsp + 0x10], rbx
002D0075  push     rdi
002D0076  sub      rsp, 0x20
002D007A  mov      rdi, rdx
002D007D  mov      rbx, rcx
002D0080  movzx    edx, word ptr [rcx + 8]
002D0084  mov      ecx, 1
002D0089  shl      edx, 0x10
002D008C  call     0x35d330  ; -> 0035D330 fn
002D0091  cmp      dword ptr [rax], 6
002D0094  jne      0x2d00ab  ; -> 002D00AB
002D0096  mov      rdx, rdi
002D0099  mov      rcx, rbx
002D009C  mov      rbx, qword ptr [rsp + 0x38]
002D00A1  add      rsp, 0x20
002D00A5  pop      rdi
002D00A6  jmp      0x2cfe40  ; -> 002CFE40 fn
002D00AB  movzx    edi, word ptr [rdi + 8]
002D00AF  mov      ecx, 1
002D00B4  mov      qword ptr [rsp + 0x30], rsi
002D00B9  movzx    esi, word ptr [rbx + 8]
002D00BD  mov      edx, esi
002D00BF  shl      edx, 0x10
002D00C2  call     0x35d330  ; -> 0035D330 fn
002D00C7  mov      edx, edi
002D00C9  mov      ecx, 1
002D00CE  shl      edx, 0x10
002D00D1  mov      ebx, dword ptr [rax + 0x30]
002D00D4  call     0x35d330  ; -> 0035D330 fn
002D00D9  sub      esi, edi
002D00DB  sub      ebx, dword ptr [rax + 0x30]
002D00DE  test     ebx, ebx
002D00E0  cmovne   esi, ebx
002D00E3  mov      rbx, qword ptr [rsp + 0x38]
002D00E8  mov      eax, esi
002D00EA  mov      rsi, qword ptr [rsp + 0x30]
002D00EF  add      rsp, 0x20
002D00F3  pop      rdi
002D00F4  ret      
```

## 002D5C30 (73 B, extent 002D5C30-002D5C79)

Documented callee on this page: `0035BB20`

```
002D5C30  mov      qword ptr [rsp + 8], rbx
002D5C35  push     rdi
002D5C36  sub      rsp, 0x20
002D5C3A  mov      rax, qword ptr [rcx + 0x150]
002D5C41  mov      rbx, rcx
002D5C44  test     rax, rax
002D5C47  je       0x2d5c4f  ; -> 002D5C4F
002D5C49  movsx    edi, byte ptr [rax + 0x13]
002D5C4D  jmp      0x2d5c51  ; -> 002D5C51
002D5C4F  xor      edi, edi
002D5C51  movsx    ecx, word ptr [rcx + 0x140]
002D5C58  call     0x35bb20  ; -> 0035BB20 fn
002D5C5D  mov      edx, edi
002D5C5F  mov      rcx, rbx
002D5C62  movzx    r8d, byte ptr [rax + 0x87]
002D5C6A  mov      rbx, qword ptr [rsp + 0x30]
002D5C6F  add      rsp, 0x20
002D5C73  pop      rdi
002D5C74  jmp      0x2d5500  ; -> 002D5500 fn
```

## 003CB150 (390 B, extent 003CB150-003CB2D6)

Documented callee on this page: `00275440`

```
003CB150  push     rdi
003CB152  sub      rsp, 0x40
003CB156  mov      rax, qword ptr [rip + 0x1b796d3]  ; -> 01F44830 [u64 0x00002B992DDFA232]
003CB15D  xor      rax, rsp
003CB160  mov      qword ptr [rsp + 0x38], rax
003CB165  mov      eax, dword ptr [rdx]
003CB167  mov      rdi, rcx
003CB16A  dec      eax
003CB16C  cmp      eax, 0x11
003CB16F  ja       0x3cb2bb  ; -> 003CB2BB
003CB175  lea      r8, [rip - 0x2ab17c]  ; -> 00120000 (image base)
003CB17C  cdqe     
003CB17E  mov      ecx, dword ptr [r8 + rax*4 + 0x2ab2d8]  ; image base + 0x2ab2d8 = 003CB2D8
003CB186  add      rcx, r8
003CB189  jmp      rcx
003CB18B  mov      rax, qword ptr [rip + 0x1ccfa9e]  ; -> 0209AC30
003CB192  mov      rcx, qword ptr [rax + 0x28]
003CB196  xor      eax, eax
003CB198  mov      qword ptr [rdi + 0x1c8], rcx
003CB19F  mov      rcx, qword ptr [rsp + 0x38]
003CB1A4  xor      rcx, rsp
003CB1A7  call     0x808c40  ; -> 00808C40 fn
003CB1AC  add      rsp, 0x40
003CB1B0  pop      rdi
003CB1B1  ret      
003CB1B2  mov      rdx, qword ptr [rdi + 0x1c8]
003CB1B9  lea      rcx, [rdi + 0x50]
003CB1BD  or       dword ptr [rdi + 0x1d4], 1
003CB1C4  mov      r9, rdi
003CB1C7  xor      r8d, r8d
003CB1CA  mov      qword ptr [rsp + 0x60], rbx
003CB1CF  call     0x2432b0  ; -> 002432B0 fn
003CB1D4  mov      ecx, 1
003CB1D9  mov      rbx, rax
003CB1DC  call     0x2735e0  ; -> 002735E0 fn
003CB1E1  mov      rdx, rax
003CB1E4  mov      rcx, rdi
003CB1E7  call     0x247570  ; -> 00247570 fn
003CB1EC  movzx    r9d, word ptr [rbx + 0xa]
003CB1F1  mov      rcx, rdi
003CB1F4  movzx    r8d, word ptr [rbx + 8]
003CB1F9  movsx    edx, word ptr [rbx + 6]
003CB1FD  movzx    eax, word ptr [rbx + 4]
003CB201  mov      word ptr [rdi + 0x98], ax
003CB208  mov      word ptr [rdi + 0x9a], dx
003CB20F  mov      word ptr [rdi + 0x9c], r8w
003CB217  mov      word ptr [rdi + 0x9e], r9w
003CB21F  call     0x3cb320  ; -> 003CB320 fn
003CB224  mov      rcx, rdi
003CB227  call     0x246ac0  ; -> 00246AC0 fn
003CB22C  mov      rbx, qword ptr [rsp + 0x60]
003CB231  xor      eax, eax
003CB233  mov      rcx, qword ptr [rsp + 0x38]
003CB238  xor      rcx, rsp
003CB23B  call     0x808c40  ; -> 00808C40 fn
003CB240  add      rsp, 0x40
003CB244  pop      rdi
003CB245  ret      
003CB246  xorps    xmm0, xmm0
003CB249  mov      dword ptr [rsp + 0x20], 0x1d
003CB251  lea      rdx, [rsp + 0x20]
003CB256  mov      rcx, rdi
003CB259  movdqu   xmmword ptr [rsp + 0x28], xmm0
003CB25F  call     0x275440  ; -> 00275440 fn
003CB264  xor      eax, eax
003CB266  mov      rcx, qword ptr [rsp + 0x38]
003CB26B  xor      rcx, rsp
003CB26E  call     0x808c40  ; -> 00808C40 fn
003CB273  add      rsp, 0x40
003CB277  pop      rdi
003CB278  ret      
003CB279  test     byte ptr [rdi + 0x1d4], 1
003CB280  je       0x3cb2a6  ; -> 003CB2A6
003CB282  mov      rcx, rdi
003CB285  call     0x3caed0  ; -> 003CAED0 fn
003CB28A  xor      eax, eax
003CB28C  mov      rcx, qword ptr [rsp + 0x38]
003CB291  xor      rcx, rsp
003CB294  call     0x808c40  ; -> 00808C40 fn
003CB299  add      rsp, 0x40
003CB29D  pop      rdi
003CB29E  ret      
003CB29F  or       dword ptr [rdi + 0x1d4], 2
003CB2A6  xor      eax, eax
003CB2A8  mov      rcx, qword ptr [rsp + 0x38]
003CB2AD  xor      rcx, rsp
003CB2B0  call     0x808c40  ; -> 00808C40 fn
003CB2B5  add      rsp, 0x40
003CB2B9  pop      rdi
003CB2BA  ret      
003CB2BB  mov      rcx, rdi
003CB2BE  call     0x5c5230  ; -> 005C5230 fn
003CB2C3  mov      rcx, qword ptr [rsp + 0x38]
003CB2C8  xor      rcx, rsp
003CB2CB  call     0x808c40  ; -> 00808C40 fn
003CB2D0  add      rsp, 0x40
003CB2D4  pop      rdi
003CB2D5  ret      
```

## 00563560 (398 B, extent 00563560-005636EE)

Documented callee on this page: `0029FF60`

```
00563560  mov      qword ptr [rsp + 0x10], rbx
00563565  mov      qword ptr [rsp + 0x18], rbp
0056356A  mov      qword ptr [rsp + 0x20], rsi
0056356F  push     r14
00563571  sub      rsp, 0x30
00563575  mov      rax, qword ptr [rcx + 0xe0]
0056357C  mov      rsi, rdx
0056357F  movsxd   r14, r9d
00563582  mov      rbp, rcx
00563585  test     rax, rax
00563588  jne      0x5635d4  ; -> 005635D4
0056358A  xor      edx, edx
0056358C  mov      rcx, rsi
0056358F  call     0x243580  ; -> 00243580 fn
00563594  mov      rax, qword ptr [rsi + 0x10]
00563598  mov      ecx, 0x7d8
0056359D  mov      rbx, qword ptr [rax + 8]
005635A1  or       dword ptr [rbx + 8], 1
005635A5  call     0x2f9860  ; -> 002F9860 fn
005635AA  xor      ecx, ecx
005635AC  mov      qword ptr [rbx + 0x18], rax
005635B0  call     0x20e620  ; -> 0020E620 fn
005635B5  mov      rcx, qword ptr [rbx]
005635B8  mov      dword ptr [rbx + 0x20], eax
005635BB  movzx    eax, word ptr [rcx + 4]
005635BF  sub      ax, 0x14
005635C3  mov      word ptr [rbx + 0xc], ax
005635C7  movzx    eax, word ptr [rcx + 6]
005635CB  mov      word ptr [rbx + 0xe], ax
005635CF  jmp      0x5636d3  ; -> 005636D3
005635D4  mov      qword ptr [rsp + 0x40], rdi
005635D9  mov      rdi, r14
005635DC  shl      rdi, 5
005635E0  add      rdi, rax
005635E3  mov      rax, qword ptr [rdx + 0x10]
005635E7  cmp      byte ptr [rdi + 0xa], 0xff
005635EB  mov      r8, qword ptr [rax]
005635EE  jne      0x5635f7  ; -> 005635F7
005635F0  and      dword ptr [r8 + 8], 0xfffffffe
005635F5  jmp      0x563612  ; -> 00563612
005635F7  or       dword ptr [r8 + 8], 1
005635FC  movzx    edx, byte ptr [rdi + 0xa]
00563600  mov      rax, qword ptr [r8 + 0x20]
00563604  movzx    ecx, byte ptr [rax + rdx*8 + 7]
00563609  mov      byte ptr [r8 + 0x39], cl
0056360D  mov      word ptr [r8 + 0xa], dx
00563612  mov      rax, qword ptr [rsi + 0x10]
00563616  xor      ecx, ecx
00563618  mov      rbx, qword ptr [rax + 8]
0056361C  mov      rax, qword ptr [rdi]
0056361F  mov      qword ptr [rbx + 0x18], rax
00563623  call     0x20e620  ; -> 0020E620 fn
00563628  mov      rcx, qword ptr [rbx]
0056362B  mov      dword ptr [rbx + 0x20], eax
0056362E  movzx    eax, word ptr [rcx + 4]
00563632  mov      word ptr [rbx + 0xc], ax
00563636  movzx    eax, word ptr [rcx + 6]
0056363A  mov      word ptr [rbx + 0xe], ax
0056363E  test     dword ptr [rbp + 0x180], 0x100
00563648  je       0x56365d  ; -> 0056365D
0056364A  movsx    eax, word ptr [rbp + 0x17c]
00563651  cmp      eax, r14d
00563654  jne      0x56365d  ; -> 0056365D
00563656  mov      ecx, 6
0056365B  jmp      0x56365f  ; -> 0056365F
0056365D  xor      ecx, ecx
0056365F  call     0x2dd7e0  ; -> 002DD7E0 fn
00563664  mov      dword ptr [rbx + 0x24], eax
00563667  xor      ebp, ebp
00563669  mov      rax, qword ptr [rsi + 0x10]
0056366D  xor      r8d, r8d
00563670  movzx    r9d, word ptr [rdi + 0xe]
00563675  xor      edx, edx
00563677  mov      qword ptr [rsp + 0x28], rbp
0056367C  mov      dword ptr [rsp + 0x20], ebp
00563680  mov      rbx, qword ptr [rax + 0x18]
00563684  movsx    eax, word ptr [rdi + 0xc]
00563688  mov      rcx, rbx
0056368B  sub      r9d, eax
0056368E  call     0x29ff60  ; -> 0029FF60 fn
00563693  mov      rcx, rbx
00563696  call     0x29fb50  ; -> 0029FB50 fn
0056369B  mov      rcx, qword ptr [rsi + 0x10]
0056369F  xor      r8d, r8d
005636A2  movzx    r9d, word ptr [rdi + 0xe]
005636A7  xor      edx, edx
005636A9  mov      qword ptr [rsp + 0x28], rbp
005636AE  mov      dword ptr [rsp + 0x20], ebp
005636B2  mov      rcx, qword ptr [rcx + 0x10]
005636B6  call     0x29ff60  ; -> 0029FF60 fn
005636BB  lea      r9d, [rbp + 0xa]
005636BF  mov      rdx, rdi
005636C2  lea      r8d, [rbp + 5]
005636C6  mov      rcx, rsi
005636C9  call     0x3fcad0  ; -> 003FCAD0 fn
005636CE  mov      rdi, qword ptr [rsp + 0x40]
005636D3  mov      rbx, qword ptr [rsp + 0x48]
005636D8  mov      eax, 1
005636DD  mov      rbp, qword ptr [rsp + 0x50]
005636E2  mov      rsi, qword ptr [rsp + 0x58]
005636E7  add      rsp, 0x30
005636EB  pop      r14
005636ED  ret      
```

## 005637D0 (343 B, extent 005637D0-00563927)

Documented callee on this page: `0029FF60`

```
005637D0  mov      qword ptr [rsp + 0x10], rbx
005637D5  mov      qword ptr [rsp + 0x18], rbp
005637DA  mov      qword ptr [rsp + 0x20], rsi
005637DF  push     r14
005637E1  sub      rsp, 0x30
005637E5  mov      rax, qword ptr [rcx + 0xe0]
005637EC  mov      rbp, rdx
005637EF  movsxd   r14, r9d
005637F2  mov      rsi, rcx
005637F5  test     rax, rax
005637F8  jne      0x563838  ; -> 00563838
005637FA  xor      edx, edx
005637FC  mov      rcx, rbp
005637FF  call     0x243580  ; -> 00243580 fn
00563804  mov      rax, qword ptr [rbp + 0x10]
00563808  mov      ecx, 0x7d8
0056380D  mov      rbx, qword ptr [rax + 8]
00563811  or       dword ptr [rbx + 8], 1
00563815  call     0x2f9860  ; -> 002F9860 fn
0056381A  xor      ecx, ecx
0056381C  mov      qword ptr [rbx + 0x18], rax
00563820  call     0x20e620  ; -> 0020E620 fn
00563825  mov      rcx, qword ptr [rbx]
00563828  mov      dword ptr [rbx + 0x20], eax
0056382B  movzx    eax, word ptr [rcx + 4]
0056382F  sub      ax, 0x14
00563833  jmp      0x563900  ; -> 00563900
00563838  mov      qword ptr [rsp + 0x40], rdi
0056383D  mov      rdi, r14
00563840  shl      rdi, 5
00563844  add      rdi, rax
00563847  mov      rax, qword ptr [rdx + 0x10]
0056384B  cmp      byte ptr [rdi + 0xa], 0xff
0056384F  mov      r8, qword ptr [rax]
00563852  jne      0x56385b  ; -> 0056385B
00563854  and      dword ptr [r8 + 8], 0xfffffffe
00563859  jmp      0x563876  ; -> 00563876
0056385B  or       dword ptr [r8 + 8], 1
00563860  movzx    edx, byte ptr [rdi + 0xa]
00563864  mov      rax, qword ptr [r8 + 0x20]
00563868  movzx    ecx, byte ptr [rax + rdx*8 + 7]
0056386D  mov      byte ptr [r8 + 0x39], cl
00563871  mov      word ptr [r8 + 0xa], dx
00563876  mov      rax, qword ptr [rbp + 0x10]
0056387A  xor      ecx, ecx
0056387C  mov      rbx, qword ptr [rax + 8]
00563880  mov      rax, qword ptr [rdi]
00563883  mov      qword ptr [rbx + 0x18], rax
00563887  call     0x20e620  ; -> 0020E620 fn
0056388C  mov      rcx, qword ptr [rbx]
0056388F  mov      dword ptr [rbx + 0x20], eax
00563892  movzx    eax, word ptr [rcx + 4]
00563896  mov      word ptr [rbx + 0xc], ax
0056389A  movzx    eax, word ptr [rcx + 6]
0056389E  mov      word ptr [rbx + 0xe], ax
005638A2  test     dword ptr [rsi + 0x180], 0x100
005638AC  je       0x5638c1  ; -> 005638C1
005638AE  movsx    eax, word ptr [rsi + 0x17c]
005638B5  cmp      eax, r14d
005638B8  jne      0x5638c1  ; -> 005638C1
005638BA  mov      ecx, 6
005638BF  jmp      0x5638c3  ; -> 005638C3
005638C1  xor      ecx, ecx
005638C3  call     0x2dd7e0  ; -> 002DD7E0 fn
005638C8  mov      dword ptr [rbx + 0x24], eax
005638CB  xor      r8d, r8d
005638CE  mov      rax, qword ptr [rbp + 0x10]
005638D2  xor      edx, edx
005638D4  movzx    r9d, word ptr [rdi + 0xe]
005638D9  mov      rbx, qword ptr [rax + 0x10]
005638DD  xor      eax, eax
005638DF  mov      qword ptr [rsp + 0x28], rax
005638E4  mov      rcx, rbx
005638E7  mov      dword ptr [rsp + 0x20], eax
005638EB  call     0x29ff60  ; -> 0029FF60 fn
005638F0  mov      rcx, qword ptr [rbx]
005638F3  mov      rdi, qword ptr [rsp + 0x40]
005638F8  movzx    eax, word ptr [rcx + 4]
005638FC  add      ax, 0xa
00563900  mov      rbp, qword ptr [rsp + 0x50]
00563905  mov      rsi, qword ptr [rsp + 0x58]
0056390A  mov      word ptr [rbx + 0xc], ax
0056390E  movzx    eax, word ptr [rcx + 6]
00563912  mov      word ptr [rbx + 0xe], ax
00563916  mov      eax, 1
0056391B  mov      rbx, qword ptr [rsp + 0x48]
00563920  add      rsp, 0x30
00563924  pop      r14
00563926  ret      
```

## 0056D870 (201 B, extent 0056D870-0056D939)

Documented callee on this page: `0029FF60`

```
0056D870  mov      qword ptr [rsp + 8], rbx
0056D875  mov      qword ptr [rsp + 0x10], rbp
0056D87A  mov      qword ptr [rsp + 0x18], rsi
0056D87F  push     rdi
0056D880  sub      rsp, 0x30
0056D884  mov      rax, qword ptr [rdx + 0x10]
0056D888  mov      rdi, rcx
0056D88B  movsxd   r9, dword ptr [r8]
0056D88E  mov      rbp, rdx
0056D891  mov      rsi, r8
0056D894  mov      r10, qword ptr [rax + r9*8]
0056D898  xor      r9d, r9d
0056D89B  cmp      byte ptr [rcx + 0xa], 0xff
0056D89F  setne    r9b
0056D8A3  mov      eax, dword ptr [r10 + 8]
0056D8A7  and      eax, 0xfffffffe
0056D8AA  or       r9d, eax
0056D8AD  mov      rax, qword ptr [r10 + 0x20]
0056D8B1  mov      dword ptr [r10 + 8], r9d
0056D8B5  movzx    edx, byte ptr [rcx + 0xa]
0056D8B9  movzx    ecx, byte ptr [rax + rdx*8 + 7]
0056D8BE  mov      byte ptr [r10 + 0x39], cl
0056D8C2  mov      word ptr [r10 + 0xa], dx
0056D8C7  movsxd   rcx, dword ptr [r8 + 4]
0056D8CB  mov      rax, qword ptr [rbp + 0x10]
0056D8CF  mov      rbx, qword ptr [rax + rcx*8]
0056D8D3  xor      ecx, ecx
0056D8D5  mov      rax, qword ptr [rdi]
0056D8D8  mov      qword ptr [rbx + 0x18], rax
0056D8DC  call     0x20e620  ; -> 0020E620 fn
0056D8E1  mov      dword ptr [rbx + 0x20], eax
0056D8E4  xor      r8d, r8d
0056D8E7  movsxd   rax, dword ptr [rsi + 8]
0056D8EB  xor      edx, edx
0056D8ED  mov      rcx, qword ptr [rbp + 0x10]
0056D8F1  mov      r9d, dword ptr [rdi + 0x10]
0056D8F5  btr      r9d, 0x1f
0056D8FA  mov      qword ptr [rsp + 0x28], 0
0056D903  mov      dword ptr [rsp + 0x20], 0
0056D90B  mov      rcx, qword ptr [rcx + rax*8]
0056D90F  call     0x29ff60  ; -> 0029FF60 fn
0056D914  movsxd   rax, dword ptr [rsi + 8]
0056D918  mov      rcx, qword ptr [rbp + 0x10]
0056D91C  mov      rcx, qword ptr [rcx + rax*8]
0056D920  mov      rbx, qword ptr [rsp + 0x40]
0056D925  mov      rbp, qword ptr [rsp + 0x48]
0056D92A  mov      rsi, qword ptr [rsp + 0x50]
0056D92F  add      rsp, 0x30
0056D933  pop      rdi
0056D934  jmp      0x29fb50  ; -> 0029FB50 fn
```

## 0056DA80 (423 B, extent 0056DA80-0056DC27)

Documented callee on this page: `0029FF60`

```
0056DA80  mov      qword ptr [rsp + 8], rbx
0056DA85  mov      qword ptr [rsp + 0x10], rbp
0056DA8A  mov      qword ptr [rsp + 0x18], rsi
0056DA8F  mov      qword ptr [rsp + 0x20], rdi
0056DA94  push     r12
0056DA96  push     r14
0056DA98  push     r15
0056DA9A  sub      rsp, 0x30
0056DA9E  mov      rdi, rdx
0056DAA1  mov      r10d, 1
0056DAA7  mov      edx, dword ptr [r8]
0056DAAA  or       esi, 0xffffffff
0056DAAD  mov      eax, edx
0056DAAF  mov      rbx, r9
0056DAB2  mov      r14, r8
0056DAB5  mov      rbp, rcx
0056DAB8  and      eax, r10d
0056DABB  je       0x56dac2  ; -> 0056DAC2
0056DABD  mov      r9d, dword ptr [r9]
0056DAC0  jmp      0x56dac6  ; -> 0056DAC6
0056DAC2  mov      r9d, dword ptr [r9 + 4]
0056DAC6  xor      r12d, r12d
0056DAC9  test     dl, 2
0056DACC  je       0x56daf4  ; -> 0056DAF4
0056DACE  test     eax, eax
0056DAD0  lea      rax, [rbx + 4]
0056DAD4  jne      0x56dad9  ; -> 0056DAD9
0056DAD6  mov      rax, rbx
0056DAD9  mov      ecx, dword ptr [rax]
0056DADB  test     dl, 4
0056DADE  je       0x56daeb  ; -> 0056DAEB
0056DAE0  movzx    esi, word ptr [r8 + 4]
0056DAE5  mov      r8d, dword ptr [rbx + 8]
0056DAE9  jmp      0x56db09  ; -> 0056DB09
0056DAEB  mov      r8d, dword ptr [rbx + 8]
0056DAEF  mov      r10d, r12d
0056DAF2  jmp      0x56db09  ; -> 0056DB09
0056DAF4  mov      ecx, dword ptr [rbx + 8]
0056DAF7  test     eax, eax
0056DAF9  movzx    esi, word ptr [rbp + 0xe]
0056DAFD  lea      rax, [rbx + 4]
0056DB01  jne      0x56db06  ; -> 0056DB06
0056DB03  mov      rax, rbx
0056DB06  mov      r8d, dword ptr [rax]
0056DB09  movsxd   rax, ecx
0056DB0C  lea      r15, [rax*8]
0056DB14  mov      rax, qword ptr [rdi + 0x10]
0056DB18  mov      rcx, qword ptr [r15 + rax]
0056DB1C  and      dword ptr [rcx + 8], 0xfffffffe
0056DB20  or       dword ptr [rcx + 8], r10d
0056DB24  mov      rax, qword ptr [rdi + 0x10]
0056DB28  movsxd   rcx, dword ptr [rbx + 0xc]
0056DB2C  mov      rdx, qword ptr [rax + rcx*8]
0056DB30  mov      eax, dword ptr [r14]
0056DB33  shr      eax, 2
0056DB36  xor      eax, dword ptr [rdx + 8]
0056DB39  and      eax, 1
0056DB3C  xor      dword ptr [rdx + 8], eax
0056DB3F  mov      rax, qword ptr [rdi + 0x10]
0056DB43  movsxd   rcx, dword ptr [rbx + 0x10]
0056DB47  mov      rdx, qword ptr [rax + rcx*8]
0056DB4B  mov      eax, dword ptr [r14]
0056DB4E  shr      eax, 2
0056DB51  xor      eax, dword ptr [rdx + 8]
0056DB54  and      eax, 1
0056DB57  xor      dword ptr [rdx + 8], eax
0056DB5A  mov      rax, qword ptr [rdi + 0x10]
0056DB5E  movsxd   rcx, dword ptr [rbx + 0x14]
0056DB62  mov      rdx, qword ptr [rax + rcx*8]
0056DB66  mov      eax, dword ptr [r14]
0056DB69  shr      eax, 2
0056DB6C  movsxd   rcx, r9d
0056DB6F  xor      eax, dword ptr [rdx + 8]
0056DB72  and      eax, 1
0056DB75  xor      dword ptr [rdx + 8], eax
0056DB78  mov      rax, qword ptr [rdi + 0x10]
0056DB7C  mov      rdx, qword ptr [rax + rcx*8]
0056DB80  movsxd   rcx, r8d
0056DB83  and      dword ptr [rdx + 8], 0xfffffffe
0056DB87  mov      rax, qword ptr [rdi + 0x10]
0056DB8B  mov      rdx, qword ptr [rax + rcx*8]
0056DB8F  and      dword ptr [rdx + 8], 0xfffffffe
0056DB93  test     r10d, r10d
0056DB96  je       0x56dbc4  ; -> 0056DBC4
0056DB98  mov      rcx, qword ptr [rdi + 0x10]
0056DB9C  mov      r9d, esi
0056DB9F  mov      qword ptr [rsp + 0x28], r12
0056DBA4  xor      r8d, r8d
0056DBA7  xor      edx, edx
0056DBA9  mov      dword ptr [rsp + 0x20], r12d
0056DBAE  mov      rcx, qword ptr [rcx + r15]
0056DBB2  call     0x29ff60  ; -> 0029FF60 fn
0056DBB7  mov      rcx, qword ptr [rdi + 0x10]
0056DBBB  mov      rcx, qword ptr [rcx + r15]
0056DBBF  call     0x29fb50  ; -> 0029FB50 fn
0056DBC4  test     byte ptr [r14], 4
0056DBC8  je       0x56dc08  ; -> 0056DC08
0056DBCA  mov      r9d, dword ptr [rbp + 0x10]
0056DBCE  xor      r8d, r8d
0056DBD1  movsxd   rax, dword ptr [rbx + 0xc]
0056DBD5  btr      r9d, 0x1f
0056DBDA  mov      rcx, qword ptr [rdi + 0x10]
0056DBDE  xor      edx, edx
0056DBE0  imul     r9d, esi
0056DBE4  mov      qword ptr [rsp + 0x28], r12
0056DBE9  mov      dword ptr [rsp + 0x20], r12d
0056DBEE  mov      rcx, qword ptr [rcx + rax*8]
0056DBF2  call     0x29ff60  ; -> 0029FF60 fn
0056DBF7  movsxd   rax, dword ptr [rbx + 0xc]
0056DBFB  mov      rcx, qword ptr [rdi + 0x10]
0056DBFF  mov      rcx, qword ptr [rcx + rax*8]
0056DC03  call     0x29fb50  ; -> 0029FB50 fn
0056DC08  mov      rbx, qword ptr [rsp + 0x50]
0056DC0D  mov      rbp, qword ptr [rsp + 0x58]
0056DC12  mov      rsi, qword ptr [rsp + 0x60]
0056DC17  mov      rdi, qword ptr [rsp + 0x68]
0056DC1C  add      rsp, 0x30
0056DC20  pop      r15
0056DC22  pop      r14
0056DC24  pop      r12
0056DC26  ret      
```
