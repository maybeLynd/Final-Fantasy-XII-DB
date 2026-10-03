# F homing pack (FABLE): `16-UI/Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md`

Generated 2026-10-03 04:02 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 16. No bearing page cites them and no documented function calls them directly.

## 00275CA0 (404 B, extent 00275CA0-00275E34)

Documented callee on this page: `00203080`

```
00275CA0  mov      qword ptr [rsp + 0x18], rbx
00275CA5  push     rsi
00275CA6  push     r14
00275CA8  push     r15
00275CAA  sub      rsp, 0x20
00275CAE  mov      qword ptr [rcx + 0x410], rdx
00275CB5  mov      rsi, rcx
00275CB8  mov      r15d, r9d
00275CBB  mov      rdx, r8
00275CBE  mov      dword ptr [rcx + 0x418], r15d
00275CC5  mov      rbx, r8
00275CC8  add      rcx, 0x400
00275CCF  call     0x202c90  ; -> 00202C90 fn
00275CD4  test     r15d, r15d
00275CD7  jle      0x275d1a  ; -> 00275D1A
00275CD9  mov      qword ptr [rsp + 0x40], rbp
00275CDE  mov      rbp, rsi
00275CE1  mov      qword ptr [rsp + 0x48], rdi
00275CE6  sub      rbp, rbx
00275CE9  mov      edi, r15d
00275CEC  nop      dword ptr [rax]
00275CF0  lea      rcx, [rbp + 0x20]
00275CF4  mov      rdx, rbx
00275CF7  add      rcx, rbx
00275CFA  lea      r8, [rsi + 0x400]
00275D01  call     0x203080  ; -> 00203080 fn
00275D06  add      rbx, 0x10
00275D0A  sub      rdi, 1
00275D0E  jne      0x275cf0  ; -> 00275CF0
00275D10  mov      rdi, qword ptr [rsp + 0x48]
00275D15  mov      rbp, qword ptr [rsp + 0x40]
00275D1A  movss    xmm0, dword ptr [rsi + 0x20]
00275D1F  lea      eax, [r15 + 1]
00275D23  mov      rbx, qword ptr [rsp + 0x50]
00275D28  addss    xmm0, xmm0
00275D2C  movsxd   rcx, eax
00275D2F  mov      rax, rcx
00275D32  mov      rdx, rcx
00275D35  add      rax, rax
00275D38  add      rdx, rdx
00275D3B  inc      rcx
00275D3E  subss    xmm0, dword ptr [rsi + 0x30]
00275D43  add      rcx, rcx
00275D46  movss    dword ptr [rsi + 0x10], xmm0
00275D4B  movss    xmm1, dword ptr [rsi + 0x24]
00275D50  addss    xmm1, xmm1
00275D54  subss    xmm1, dword ptr [rsi + 0x34]
00275D59  movss    dword ptr [rsi + 0x14], xmm1
00275D5E  movss    xmm0, dword ptr [rsi + 0x28]
00275D63  addss    xmm0, xmm0
00275D67  subss    xmm0, dword ptr [rsi + 0x38]
00275D6C  movss    dword ptr [rsi + 0x18], xmm0
00275D71  movss    xmm0, dword ptr [rsi + rax*8]
00275D76  addss    xmm0, xmm0
00275D7A  subss    xmm0, dword ptr [rsi + rdx*8 - 0x10]
00275D80  movss    dword ptr [rsi + rcx*8], xmm0
00275D85  movss    xmm1, dword ptr [rsi + rax*8 + 4]
00275D8B  addss    xmm1, xmm1
00275D8F  subss    xmm1, dword ptr [rsi + rdx*8 - 0xc]
00275D95  movss    dword ptr [rsi + rcx*8 + 4], xmm1
00275D9B  movss    xmm0, dword ptr [rsi + rax*8 + 8]
00275DA1  addss    xmm0, xmm0
00275DA5  subss    xmm0, dword ptr [rsi + rdx*8 - 8]
00275DAB  movss    dword ptr [rsi + rcx*8 + 8], xmm0
00275DB1  movss    xmm0, dword ptr [rsi + 0x20]
00275DB6  addss    xmm0, xmm0
00275DBA  subss    xmm0, dword ptr [rsi + 0x40]
00275DBF  movss    dword ptr [rsi], xmm0
00275DC3  movss    xmm1, dword ptr [rsi + 0x24]
00275DC8  addss    xmm1, xmm1
00275DCC  subss    xmm1, dword ptr [rsi + 0x44]
00275DD1  movss    dword ptr [rsi + 4], xmm1
00275DD6  movss    xmm0, dword ptr [rsi + 0x28]
00275DDB  addss    xmm0, xmm0
00275DDF  subss    xmm0, dword ptr [rsi + 0x48]
00275DE4  movss    dword ptr [rsi + 8], xmm0
00275DE9  movss    xmm0, dword ptr [rsi + rax*8]
00275DEE  addss    xmm0, xmm0
00275DF2  subss    xmm0, dword ptr [rsi + rdx*8 - 0x20]
00275DF8  movss    dword ptr [rsi + rcx*8 + 0x10], xmm0
00275DFE  movss    xmm1, dword ptr [rsi + rax*8 + 4]
00275E04  addss    xmm1, xmm1
00275E08  subss    xmm1, dword ptr [rsi + rdx*8 - 0x1c]
00275E0E  movss    dword ptr [rsi + rcx*8 + 0x14], xmm1
00275E14  movss    xmm0, dword ptr [rsi + rax*8 + 8]
00275E1A  addss    xmm0, xmm0
00275E1E  subss    xmm0, dword ptr [rsi + rdx*8 - 0x18]
00275E24  movss    dword ptr [rsi + rcx*8 + 0x18], xmm0
00275E2A  add      rsp, 0x20
00275E2E  pop      r15
00275E30  pop      r14
00275E32  pop      rsi
00275E33  ret      
```

## 0028F640 (86 B, extent 0028F640-0028F696)

Documented callee on this page: `00273A20`

```
0028F640  sub      rsp, 0x28
0028F644  mov      rcx, qword ptr [rip + 0x1e0c835]  ; -> 0209BE80
0028F64B  test     rcx, rcx
0028F64E  je       0x28f68e  ; -> 0028F68E
0028F650  test     dword ptr [rcx + 0x10f68], 0x2000
0028F65A  jne      0x28f68e  ; -> 0028F68E
0028F65C  add      rcx, 0xab30
0028F663  call     0x273a20  ; -> 00273A20 fn
0028F668  test     eax, eax
0028F66A  je       0x28f68e  ; -> 0028F68E
0028F66C  mov      rcx, qword ptr [rip + 0x1e0c80d]  ; -> 0209BE80
0028F673  add      rcx, 0xab30
0028F67A  call     0x276770  ; -> 00276770 fn
0028F67F  test     eax, eax
0028F681  je       0x28f68e  ; -> 0028F68E
0028F683  mov      ecx, eax
0028F685  add      rsp, 0x28
0028F689  jmp      0x31c200  ; -> 0031C200 fn
0028F68E  or       eax, 0xffffffff
0028F691  add      rsp, 0x28
0028F695  ret      
```

## 00290A90 (119 B, extent 00290A90-00290B07)

Documented callee on this page: `00202C90`

```
00290A90  sub      rsp, 0x28
00290A94  mov      r8d, edx
00290A97  mov      rdx, qword ptr [rip + 0x1e0b3e2]  ; -> 0209BE80
00290A9E  test     rdx, rdx
00290AA1  je       0x290b00  ; -> 00290B00
00290AA3  mov      rax, qword ptr [rdx + 0x10ef0]
00290AAA  test     rax, rax
00290AAD  je       0x290ad5  ; -> 00290AD5
00290AAF  test     r8b, 1
00290AB3  je       0x290ad5  ; -> 00290AD5
00290AB5  cmp      word ptr [rax + 0xd54], 2
00290ABD  jne      0x290ad5  ; -> 00290AD5
00290ABF  lea      rdx, [rax + 0xc70]
00290AC6  call     0x202c90  ; -> 00202C90 fn
00290ACB  mov      eax, 1
00290AD0  add      rsp, 0x28
00290AD4  ret      
00290AD5  movzx    eax, word ptr [rdx + 0x7ec8]
00290ADC  test     al, 1
00290ADE  je       0x290b00  ; -> 00290B00
00290AE0  test     al, 2
00290AE2  jne      0x290b00  ; -> 00290B00
00290AE4  test     r8b, 2
00290AE8  je       0x290b00  ; -> 00290B00
00290AEA  add      rdx, 0x7ea0
00290AF1  call     0x28c9f0  ; -> 0028C9F0 fn
00290AF6  mov      eax, 1
00290AFB  add      rsp, 0x28
00290AFF  ret      
00290B00  xor      eax, eax
00290B02  add      rsp, 0x28
00290B06  ret      
```

## 002C33F0 (249 B, extent 002C33F0-002C34E9)

Documented callee on this page: `002D8CB0`

```
002C33F0  push     rsi
002C33F2  sub      rsp, 0x30
002C33F6  movsxd   rax, r9d
002C33F9  mov      rsi, r8
002C33FC  shl      rax, 5
002C3400  movzx    r10d, byte ptr [rax + rcx + 0xa]
002C3406  cmp      r10b, 0xff
002C340A  je       0x2c34de  ; -> 002C34DE
002C3410  mov      rax, qword ptr [rdx + 0x10]
002C3414  mov      r8d, 0xfff
002C341A  mov      qword ptr [rsp + 0x48], rbx
002C341F  mov      qword ptr [rsp + 0x50], rdi
002C3424  mov      rcx, qword ptr [rax + 8]
002C3428  mov      rax, qword ptr [rcx]
002C342B  movsx    ebx, word ptr [rax + 6]
002C342F  movsx    r9d, word ptr [rax + 4]
002C3434  mov      rax, qword ptr [rip + 0x1dd77f5]  ; -> 0209AC30
002C343B  mov      dword ptr [rsp + 0x20], ebx
002C343F  mov      rdi, qword ptr [rax + 0x378]
002C3446  mov      rcx, qword ptr [rdi + 0x20]
002C344A  add      rcx, 0x30
002C344E  movzx    eax, word ptr [rcx + 0x14]
002C3452  movzx    edx, word ptr [rcx + rax*2 + 0x14]
002C3457  movzx    eax, r10b
002C345B  add      rdx, rax
002C345E  movzx    eax, word ptr [rcx + 0x10]
002C3462  add      rcx, rax
002C3465  movzx    eax, word ptr [rcx + rdx*8]
002C3469  mov      word ptr [rsp + 0x40], ax
002C346E  movzx    eax, word ptr [rcx + rdx*8 + 2]
002C3473  mov      word ptr [rsp + 0x42], ax
002C3478  movzx    eax, word ptr [rcx + rdx*8 + 4]
002C347D  and      ax, r8w
002C3481  mov      word ptr [rsp + 0x44], ax
002C3486  mov      eax, dword ptr [rcx + rdx*8 + 4]
002C348A  shr      eax, 0xc
002C348D  and      ax, r8w
002C3491  mov      word ptr [rsp + 0x46], ax
002C3496  movzx    r11d, byte ptr [rcx + rdx*8 + 7]
002C349C  mov      rdx, rdi
002C349F  mov      r10, qword ptr [rdi + 0x20]
002C34A3  mov      eax, r11d
002C34A6  shr      eax, 4
002C34A9  add      r10, 0x30
002C34AD  movzx    eax, al
002C34B0  and      r11b, 0xf
002C34B4  add      rax, r10
002C34B7  mov      rcx, rsi
002C34BA  movzx    r8d, word ptr [r10 + 0x12]
002C34BF  movzx    eax, byte ptr [r8 + rax]
002C34C4  lea      r8, [rsp + 0x40]
002C34C9  add      al, r11b
002C34CC  mov      byte ptr [rsi + 0x5c], al
002C34CF  call     0x2d8cb0  ; -> 002D8CB0 fn
002C34D4  mov      rdi, qword ptr [rsp + 0x50]
002C34D9  mov      rbx, qword ptr [rsp + 0x48]
002C34DE  mov      eax, 1
002C34E3  add      rsp, 0x30
002C34E7  pop      rsi
002C34E8  ret      
```

## 002C5900 (203 B, extent 002C5900-002C59CB)

Documented callee on this page: `002D02A0`

```
002C5900  mov      qword ptr [rsp + 8], rbx
002C5905  push     rdi
002C5906  sub      rsp, 0x20
002C590A  movsxd   rax, r9d
002C590D  mov      rbx, rdx
002C5910  mov      edx, dword ptr [rcx + 0x148]
002C5916  lea      rdi, [rcx + rax*4]
002C591A  lea      rcx, [rdi + 0xc8]
002C5921  call     0x2d02a0  ; -> 002D02A0 fn
002C5926  test     eax, eax
002C5928  mov      rax, qword ptr [rbx + 0x10]
002C592C  jne      0x2c5951  ; -> 002C5951
002C592E  mov      rcx, qword ptr [rax]
002C5931  and      dword ptr [rcx + 8], 0xfffffffe
002C5935  mov      rax, qword ptr [rbx + 0x10]
002C5939  mov      rcx, qword ptr [rax + 8]
002C593D  mov      eax, 1
002C5942  and      dword ptr [rcx + 8], 0xfffffffe
002C5946  mov      rbx, qword ptr [rsp + 0x30]
002C594B  add      rsp, 0x20
002C594F  pop      rdi
002C5950  ret      
002C5951  mov      r8, qword ptr [rax]
002C5954  movsx    rdx, byte ptr [rdi + 0xc8]
002C595C  mov      rax, qword ptr [r8 + 0x20]
002C5960  movzx    ecx, byte ptr [rax + rdx*8 + 7]
002C5965  mov      byte ptr [r8 + 0x39], cl
002C5969  mov      ecx, 0x1a
002C596E  mov      word ptr [r8 + 0xa], dx
002C5973  mov      rax, qword ptr [rbx + 0x10]
002C5977  movsx    edx, byte ptr [rdi + 0xc8]
002C597E  mov      rbx, qword ptr [rax + 8]
002C5982  call     0x35d330  ; -> 0035D330 fn
002C5987  xor      edx, edx
002C5989  mov      rcx, qword ptr [rax + 0x18]
002C598D  call     0x2b58b0  ; -> 002B58B0 fn
002C5992  xor      ecx, ecx
002C5994  mov      qword ptr [rbx + 0x18], rax
002C5998  call     0x20e620  ; -> 0020E620 fn
002C599D  mov      dword ptr [rbx + 0x20], eax
002C59A0  mov      ecx, 5
002C59A5  cmp      byte ptr [rdi + 0xca], 0
002C59AC  je       0x2c59b3  ; -> 002C59B3
002C59AE  mov      ecx, 4
002C59B3  call     0x2dd7e0  ; -> 002DD7E0 fn
002C59B8  mov      dword ptr [rbx + 0x24], eax
002C59BB  mov      eax, 1
002C59C0  mov      rbx, qword ptr [rsp + 0x30]
002C59C5  add      rsp, 0x20
002C59C9  pop      rdi
002C59CA  ret      
```

## 002D5830 (426 B, extent 002D5830-002D59DA)

Documented callee on this page: `0029F6E0`

```
002D5830  push     rbx
002D5832  sub      rsp, 0x50
002D5836  mov      rax, qword ptr [rip + 0x1c6eff3]  ; -> 01F44830 [u64 0x00002B992DDFA232]
002D583D  xor      rax, rsp
002D5840  mov      qword ptr [rsp + 0x48], rax
002D5845  mov      rbx, rcx
002D5848  mov      ecx, dword ptr [rdx]
002D584A  sub      ecx, 1
002D584D  je       0x2d591d  ; -> 002D591D
002D5853  sub      ecx, 1
002D5856  je       0x2d5889  ; -> 002D5889
002D5858  cmp      ecx, 0x10
002D585B  je       0x2d5878  ; -> 002D5878
002D585D  mov      rcx, rbx
002D5860  call     0x5c5230  ; -> 005C5230 fn
002D5865  mov      rcx, qword ptr [rsp + 0x48]
002D586A  xor      rcx, rsp
002D586D  call     0x808c40  ; -> 00808C40 fn
002D5872  add      rsp, 0x50
002D5876  pop      rbx
002D5877  ret      
002D5878  mov      rax, qword ptr [rbx + 0xd0]
002D587F  xor      ecx, ecx
002D5881  mov      qword ptr [rax], rcx
002D5884  jmp      0x2d59c5  ; -> 002D59C5
002D5889  mov      ecx, dword ptr [rbx + 0xb4]
002D588F  call     0x1edec0  ; -> 001EDEC0 fn
002D5894  test     eax, eax
002D5896  je       0x2d59c5  ; -> 002D59C5
002D589C  mov      eax, dword ptr [rbx + 0xc4]
002D58A2  test     eax, eax
002D58A4  je       0x2d58ba  ; -> 002D58BA
002D58A6  dec      eax
002D58A8  mov      dword ptr [rbx + 0xc4], eax
002D58AE  test     eax, eax
002D58B0  jg       0x2d58ba  ; -> 002D58BA
002D58B2  mov      rcx, rbx
002D58B5  call     0x244f00  ; -> 00244F00 fn
002D58BA  inc      dword ptr [rbx + 0xc8]
002D58C0  cmp      dword ptr [rbx + 0xc8], 0x10
002D58C7  jne      0x2d59c5  ; -> 002D59C5
002D58CD  mov      eax, dword ptr [rbx + 0xc0]
002D58D3  cmp      eax, 3
002D58D6  jl       0x2d59c5  ; -> 002D59C5
002D58DC  xor      ecx, ecx
002D58DE  mov      dword ptr [rsp + 0x30], ecx
002D58E2  mov      qword ptr [rsp + 0x40], rcx
002D58E7  cmp      eax, 5
002D58EA  jl       0x2d58f5  ; -> 002D58F5
002D58EC  cmp      eax, 0xa
002D58EF  setge    cl
002D58F2  inc      rcx
002D58F5  mov      qword ptr [rsp + 0x38], rcx
002D58FA  lea      r8, [rsp + 0x30]
002D58FF  mov      ecx, 0xc8
002D5904  lea      rdx, [rip - 0x37b]  ; -> 002D5590
002D590B  call     0x244f50  ; -> 00244F50 fn
002D5910  mov      rcx, rax
002D5913  call     0x246ac0  ; -> 00246AC0 fn
002D5918  jmp      0x2d59c5  ; -> 002D59C5
002D591D  mov      rcx, qword ptr [rdx + 8]
002D5921  lea      rdx, [rip + 0x641880]  ; -> 009171A8
002D5928  mov      eax, dword ptr [rcx]
002D592A  mov      dword ptr [rbx + 0xc0], eax
002D5930  mov      eax, dword ptr [rcx + 4]
002D5933  mov      dword ptr [rbx + 0xc4], eax
002D5939  mov      rax, qword ptr [rcx + 8]
002D593D  mov      rcx, rbx
002D5940  mov      qword ptr [rbx + 0xd0], rax
002D5947  call     0x247570  ; -> 00247570 fn
002D594C  mov      rax, qword ptr [rip + 0x1dc52dd]  ; -> 0209AC30
002D5953  lea      rcx, [rbx + 0x50]
002D5957  mov      r9, rbx
002D595A  mov      r8d, 2
002D5960  mov      rdx, qword ptr [rax + 0x18]
002D5964  call     0x2432b0  ; -> 002432B0 fn
002D5969  mov      edx, 2
002D596E  movzx    r9d, word ptr [rax + 0xa]
002D5973  movzx    r8d, word ptr [rax + 8]
002D5978  movsx    ecx, word ptr [rax + 6]
002D597C  movzx    eax, word ptr [rax + 4]
002D5980  mov      word ptr [rbx + 0x98], ax
002D5987  mov      rax, qword ptr [rbx + 0x60]
002D598B  mov      word ptr [rbx + 0x9c], r8w
002D5993  lea      r8d, [rdx + 0xe]
002D5997  mov      word ptr [rbx + 0x9e], r9w
002D599F  mov      r9d, 0x80808080
002D59A5  mov      word ptr [rbx + 0x9a], cx
002D59AC  mov      rcx, qword ptr [rax]
002D59AF  mov      eax, dword ptr [rbx + 0xc0]
002D59B5  mov      dword ptr [rsp + 0x20], eax
002D59B9  call     0x29f6e0  ; -> 0029F6E0 fn
002D59BE  and      dword ptr [rbx + 0x40], 0xffffff7f
002D59C5  xor      eax, eax
002D59C7  mov      rcx, qword ptr [rsp + 0x48]
002D59CC  xor      rcx, rsp
002D59CF  call     0x808c40  ; -> 00808C40 fn
002D59D4  add      rsp, 0x50
002D59D8  pop      rbx
002D59D9  ret      
```

## 002D5C80 (382 B, extent 002D5C80-002D5DFE)

Documented callee on this page: `002468A0`

```
002D5C80  mov      qword ptr [rsp + 8], rbx
002D5C85  push     rdi
002D5C86  sub      rsp, 0x30
002D5C8A  mov      rbx, rcx
002D5C8D  mov      rdi, rdx
002D5C90  mov      ecx, dword ptr [rdx]
002D5C92  sub      ecx, 1
002D5C95  je       0x2d5d49  ; -> 002D5D49
002D5C9B  sub      ecx, 1
002D5C9E  je       0x2d5cd9  ; -> 002D5CD9
002D5CA0  cmp      ecx, 1
002D5CA3  je       0x2d5cb7  ; -> 002D5CB7
002D5CA5  mov      rcx, rbx
002D5CA8  mov      rbx, qword ptr [rsp + 0x40]
002D5CAD  add      rsp, 0x30
002D5CB1  pop      rdi
002D5CB2  jmp      0x5c5230  ; -> 005C5230 fn
002D5CB7  test     byte ptr [rbx + 0x142], 4
002D5CBE  mov      rax, qword ptr [rbx + 0x38]
002D5CC2  je       0x2d5df1  ; -> 002D5DF1
002D5CC8  sar      word ptr [rax + 0x5a], 1
002D5CCC  xor      eax, eax
002D5CCE  mov      rbx, qword ptr [rsp + 0x40]
002D5CD3  add      rsp, 0x30
002D5CD7  pop      rdi
002D5CD8  ret      
002D5CD9  mov      ecx, dword ptr [rbx + 0xb4]
002D5CDF  call     0x1edec0  ; -> 001EDEC0 fn
002D5CE4  test     eax, eax
002D5CE6  je       0x2d5df1  ; -> 002D5DF1
002D5CEC  movzx    eax, byte ptr [rbx + 0x142]
002D5CF3  test     al, 1
002D5CF5  je       0x2d5d34  ; -> 002D5D34
002D5CF7  sub      byte ptr [rbx + 0x143], 1
002D5CFE  jns      0x2d5d34  ; -> 002D5D34
002D5D00  movsx    r8d, word ptr [rbx + 0x146]
002D5D08  and      al, 0xfe
002D5D0A  movsx    edx, word ptr [rbx + 0x144]
002D5D11  mov      r9d, 1
002D5D17  mov      rcx, rbx
002D5D1A  mov      byte ptr [rbx + 0x142], al
002D5D20  mov      byte ptr [rbx + 0x143], 0
002D5D27  mov      dword ptr [rsp + 0x20], 0x96
002D5D2F  call     0x2468a0  ; -> 002468A0 fn
002D5D34  mov      rcx, rbx
002D5D37  call     0x2d5c30  ; -> 002D5C30 fn
002D5D3C  xor      eax, eax
002D5D3E  mov      rbx, qword ptr [rsp + 0x40]
002D5D43  add      rsp, 0x30
002D5D47  pop      rdi
002D5D48  ret      
002D5D49  mov      rax, qword ptr [rip + 0x1dc4ee0]  ; -> 0209AC30
002D5D50  lea      rcx, [rbx + 0x50]
002D5D54  mov      r9, rbx
002D5D57  mov      r8d, 7
002D5D5D  mov      rdx, qword ptr [rax + 0x18]
002D5D61  call     0x2432b0  ; -> 002432B0 fn
002D5D66  mov      rcx, qword ptr [rbx + 0x58]
002D5D6A  movzx    r9d, word ptr [rax + 0xa]
002D5D6F  mov      edx, dword ptr [rcx + 0xc]
002D5D72  movsx    ecx, word ptr [rax + 6]
002D5D76  imul     edx, dword ptr [rdi + 8]
002D5D7A  movzx    r8d, word ptr [rax + 8]
002D5D7F  movzx    eax, word ptr [rax + 4]
002D5D83  mov      word ptr [rbx + 0x98], ax
002D5D8A  mov      rax, qword ptr [rbx + 0x150]
002D5D91  sub      ecx, edx
002D5D93  mov      word ptr [rbx + 0x9c], r8w
002D5D9B  mov      word ptr [rbx + 0x9a], cx
002D5DA2  mov      word ptr [rbx + 0x9e], r9w
002D5DAA  movzx    ecx, word ptr [rdi + 0x10]
002D5DAE  mov      word ptr [rbx + 0x140], cx
002D5DB5  test     rax, rax
002D5DB8  je       0x2d5dc0  ; -> 002D5DC0
002D5DBA  movsx    edi, byte ptr [rax + 0x13]
002D5DBE  jmp      0x2d5dc2  ; -> 002D5DC2
002D5DC0  xor      edi, edi
002D5DC2  movsx    ecx, cx
002D5DC5  call     0x35bb20  ; -> 0035BB20 fn
002D5DCA  mov      edx, edi
002D5DCC  mov      rcx, rbx
002D5DCF  movzx    r8d, byte ptr [rax + 0x87]
002D5DD7  call     0x2d5500  ; -> 002D5500 fn
002D5DDC  mov      ecx, 5
002D5DE1  call     0x2735e0  ; -> 002735E0 fn
002D5DE6  mov      rdx, rax
002D5DE9  mov      rcx, rbx
002D5DEC  call     0x247570  ; -> 00247570 fn
002D5DF1  xor      eax, eax
002D5DF3  mov      rbx, qword ptr [rsp + 0x40]
002D5DF8  add      rsp, 0x30
002D5DFC  pop      rdi
002D5DFD  ret      
```

## 002D6CA0 (305 B, extent 002D6CA0-002D6DD1)

Documented callee on this page: `00247730`

```
002D6CA0  mov      qword ptr [rsp + 0x10], rbx
002D6CA5  push     rdi
002D6CA6  sub      rsp, 0x20
002D6CAA  mov      rdi, rcx
002D6CAD  mov      ecx, dword ptr [rdx]
002D6CAF  sub      ecx, 1
002D6CB2  je       0x2d6d73  ; -> 002D6D73
002D6CB8  sub      ecx, 1
002D6CBB  je       0x2d6d37  ; -> 002D6D37
002D6CBD  sub      ecx, 2
002D6CC0  je       0x2d6cf6  ; -> 002D6CF6
002D6CC2  cmp      ecx, 0xe
002D6CC5  je       0x2d6cd9  ; -> 002D6CD9
002D6CC7  mov      rcx, rdi
002D6CCA  mov      rbx, qword ptr [rsp + 0x38]
002D6CCF  add      rsp, 0x20
002D6CD3  pop      rdi
002D6CD4  jmp      0x5c5230  ; -> 005C5230 fn
002D6CD9  mov      rax, qword ptr [rip + 0x1dc3f50]  ; -> 0209AC30
002D6CE0  xor      ebx, ebx
002D6CE2  mov      qword ptr [rax + 0xf0], rbx
002D6CE9  xor      eax, eax
002D6CEB  mov      rbx, qword ptr [rsp + 0x38]
002D6CF0  add      rsp, 0x20
002D6CF4  pop      rdi
002D6CF5  ret      
002D6CF6  mov      qword ptr [rsp + 0x30], rsi
002D6CFB  xor      ebx, ebx
002D6CFD  mov      rsi, qword ptr [rdi + 0x38]
002D6D01  add      rdi, 0xd4
002D6D08  mov      eax, dword ptr [rdi]
002D6D0A  and      al, 0x11
002D6D0C  cmp      al, 1
002D6D0E  jne      0x2d6d1a  ; -> 002D6D1A
002D6D10  mov      edx, ebx
002D6D12  mov      rcx, rsi
002D6D15  call     0x2d6990  ; -> 002D6990 fn
002D6D1A  inc      ebx
002D6D1C  add      rdi, 0x18
002D6D20  cmp      ebx, 8
002D6D23  jl       0x2d6d08  ; -> 002D6D08
002D6D25  mov      rsi, qword ptr [rsp + 0x30]
002D6D2A  xor      eax, eax
002D6D2C  mov      rbx, qword ptr [rsp + 0x38]
002D6D31  add      rsp, 0x20
002D6D35  pop      rdi
002D6D36  ret      
002D6D37  cmp      dword ptr [rdi + 0x180], 0
002D6D3E  jne      0x2d6d5e  ; -> 002D6D5E
002D6D40  call     0x246790  ; -> 00246790 fn
002D6D45  test     eax, eax
002D6D47  je       0x2d6d5e  ; -> 002D6D5E
002D6D49  mov      edx, 1
002D6D4E  mov      rcx, rdi
002D6D51  call     0x247730  ; -> 00247730 fn
002D6D56  xor      ebx, ebx
002D6D58  mov      dword ptr [rdi + 0x180], ebx
002D6D5E  mov      rcx, rdi
002D6D61  call     0x2d6de0  ; -> 002D6DE0 fn
002D6D66  xor      eax, eax
002D6D68  mov      rbx, qword ptr [rsp + 0x38]
002D6D6D  add      rsp, 0x20
002D6D71  pop      rdi
002D6D72  ret      
002D6D73  mov      rax, qword ptr [rip + 0x1dc3eb6]  ; -> 0209AC30
002D6D7A  mov      edx, 0x38
002D6D7F  mov      rcx, rdi
002D6D82  mov      qword ptr [rax + 0xf0], rdi
002D6D89  call     0x247930  ; -> 00247930 fn
002D6D8E  mov      eax, dword ptr [rip + 0x1b35448]  ; -> 01E0C1DC [u32 0x000001C0]
002D6D94  mov      ecx, dword ptr [rip + 0x1b3543e]  ; -> 01E0C1D8 [u32 0x00000200]
002D6D9A  test     rdi, rdi
002D6D9D  je       0x2d6db5  ; -> 002D6DB5
002D6D9F  xor      ebx, ebx
002D6DA1  mov      word ptr [rdi + 0x9c], cx
002D6DA8  mov      dword ptr [rdi + 0x98], ebx
002D6DAE  mov      word ptr [rdi + 0x9e], ax
002D6DB5  mov      rcx, qword ptr [rip + 0x1db7c6c]  ; -> 0208EA28
002D6DBC  mov      rdx, rdi
002D6DBF  call     0x246ad0  ; -> 00246AD0 fn
002D6DC4  mov      rbx, qword ptr [rsp + 0x38]
002D6DC9  xor      eax, eax
002D6DCB  add      rsp, 0x20
002D6DCF  pop      rdi
002D6DD0  ret      
```

## 003C98A0 (62 B, extent 003C98A0-003C98DE)

Documented callee on this page: `00244DD0`

```
003C98A0  push     rbx
003C98A2  sub      rsp, 0x20
003C98A6  mov      rbx, rcx
003C98A9  mov      rcx, qword ptr [rcx + 0xc8]
003C98B0  test     rcx, rcx
003C98B3  je       0x3c98d8  ; -> 003C98D8
003C98B5  mov      eax, dword ptr [rcx + 0x7c]
003C98B8  and      eax, 0x3ff7ff
003C98BD  or       eax, 0x4b000800
003C98C2  mov      dword ptr [rcx + 0x7c], eax
003C98C5  mov      rcx, qword ptr [rbx + 0xc8]
003C98CC  call     0x244dd0  ; -> 00244DD0 fn
003C98D1  and      dword ptr [rbx + 0xc4], 0xfffffffd
003C98D8  add      rsp, 0x20
003C98DC  pop      rbx
003C98DD  ret      
```

## 003C99D0 (96 B, extent 003C99D0-003C9A30)

Documented callee on this page: `00246AC0`

```
003C99D0  sub      rsp, 0x28
003C99D4  mov      rax, qword ptr [rip + 0x277dd65]  ; -> 02B47740
003C99DB  test     rax, rax
003C99DE  jne      0x3c99f6  ; -> 003C99F6
003C99E0  xor      r8d, r8d
003C99E3  lea      rdx, [rip + 0x46]  ; -> 003C9A30
003C99EA  mov      ecx, 0xd8
003C99EF  call     0x244f50  ; -> 00244F50 fn
003C99F4  jmp      0x3c99fc  ; -> 003C99FC
003C99F6  test     byte ptr [rax + 0x7c], 0x20
003C99FA  je       0x3c9a2b  ; -> 003C9A2B
003C99FC  call     0x2544b0  ; -> 002544B0 fn
003C9A01  mov      rcx, qword ptr [rip + 0x277dd38]  ; -> 02B47740
003C9A08  xor      edx, edx
003C9A0A  cmp      eax, 1
003C9A0D  sete     dl
003C9A10  test     rcx, rcx
003C9A13  je       0x3c9a22  ; -> 003C9A22
003C9A15  and      dword ptr [rcx + 0x40], 0xffff7fff
003C9A1C  shl      edx, 0xf
003C9A1F  or       dword ptr [rcx + 0x40], edx
003C9A22  add      rsp, 0x28
003C9A26  jmp      0x246ac0  ; -> 00246AC0 fn
003C9A2B  add      rsp, 0x28
003C9A2F  ret      
```

## 003CAE00 (204 B, extent 003CAE00-003CAECC)

Documented callee on this page: `00245000`

```
003CAE00  push     rdi
003CAE02  sub      rsp, 0x20
003CAE06  mov      rdi, rcx
003CAE09  mov      ecx, dword ptr [rdx]
003CAE0B  sub      ecx, 1
003CAE0E  je       0x3cae65  ; -> 003CAE65
003CAE10  cmp      ecx, 0xd
003CAE13  je       0x3cae22  ; -> 003CAE22
003CAE15  mov      rcx, rdi
003CAE18  add      rsp, 0x20
003CAE1C  pop      rdi
003CAE1D  jmp      0x5c5230  ; -> 005C5230 fn
003CAE22  lea      rcx, [rdi + 0xc0]
003CAE29  mov      qword ptr [rsp + 0x30], rbx
003CAE2E  xor      r9d, r9d
003CAE31  lea      r8, [rip - 0x908]  ; -> 003CA530
003CAE38  mov      edx, 0xd0
003CAE3D  call     0x245000  ; -> 00245000 fn
003CAE42  mov      rdx, rax
003CAE45  mov      rcx, rdi
003CAE48  mov      rbx, rax
003CAE4B  call     0x244960  ; -> 00244960 fn
003CAE50  mov      rcx, rbx
003CAE53  call     0x246ac0  ; -> 00246AC0 fn
003CAE58  mov      rbx, qword ptr [rsp + 0x30]
003CAE5D  xor      eax, eax
003CAE5F  add      rsp, 0x20
003CAE63  pop      rdi
003CAE64  ret      
003CAE65  mov      rax, qword ptr [rip + 0x1ccfdc4]  ; -> 0209AC30
003CAE6C  lea      rcx, [rdi + 0x50]
003CAE70  mov      r9, rdi
003CAE73  mov      r8d, 2
003CAE79  mov      rdx, qword ptr [rax + 0x28]
003CAE7D  call     0x2432b0  ; -> 002432B0 fn
003CAE82  movzx    ecx, word ptr [rax + 0xa]
003CAE86  movzx    edx, word ptr [rax + 8]
003CAE8A  movsx    r8d, word ptr [rax + 6]
003CAE8F  test     rdi, rdi
003CAE92  je       0x3caeb5  ; -> 003CAEB5
003CAE94  movzx    eax, word ptr [rax + 4]
003CAE98  mov      word ptr [rdi + 0x98], ax
003CAE9F  mov      word ptr [rdi + 0x9a], r8w
003CAEA7  mov      word ptr [rdi + 0x9c], dx
003CAEAE  mov      word ptr [rdi + 0x9e], cx
003CAEB5  lea      rdx, [rip + 0x946874]  ; -> 00D11730
003CAEBC  mov      rcx, rdi
003CAEBF  call     0x247570  ; -> 00247570 fn
003CAEC4  xor      eax, eax
003CAEC6  add      rsp, 0x20
003CAECA  pop      rdi
003CAECB  ret      
```

## 003F4B40 (120 B, extent 003F4B40-003F4BB8)

Documented callee on this page: `0037E4F0`

```
003F4B40  sub      rsp, 0x28
003F4B44  mov      rcx, qword ptr [rip + 0x276a6b5]  ; -> 02B5F200
003F4B4B  test     rcx, rcx
003F4B4E  je       0x3f4bb3  ; -> 003F4BB3
003F4B50  cmp      byte ptr [rcx + 0xc0], 0
003F4B57  jne      0x3f4b67  ; -> 003F4B67
003F4B59  xor      ecx, ecx
003F4B5B  call     0x37e4f0  ; -> 0037E4F0 fn
003F4B60  mov      rcx, qword ptr [rip + 0x276a699]  ; -> 02B5F200
003F4B67  mov      rax, qword ptr [rip + 0x276a68a]  ; -> 02B5F1F8
003F4B6E  test     rax, rax
003F4B71  je       0x3f4baa  ; -> 003F4BAA
003F4B73  mov      rcx, qword ptr [rax + 0x110]
003F4B7A  xor      edx, edx
003F4B7C  test     rcx, rcx
003F4B7F  je       0x3f4b88  ; -> 003F4B88
003F4B81  mov      qword ptr [rcx + 0x120], rdx
003F4B88  mov      rcx, qword ptr [rax + 0x118]
003F4B8F  test     rcx, rcx
003F4B92  je       0x3f4b9b  ; -> 003F4B9B
003F4B94  mov      qword ptr [rcx + 0xe8], rdx
003F4B9B  mov      rcx, rax
003F4B9E  call     0x244f00  ; -> 00244F00 fn
003F4BA3  mov      rcx, qword ptr [rip + 0x276a656]  ; -> 02B5F200
003F4BAA  add      rsp, 0x28
003F4BAE  jmp      0x244f00  ; -> 00244F00 fn
003F4BB3  add      rsp, 0x28
003F4BB7  ret      
```

## 003F8250 (562 B, extent 003F8250-003F8482)

Documented callee on this page: `002DC290`

```
003F8250  push     rdi
003F8252  sub      rsp, 0x40
003F8256  mov      rax, qword ptr [rip + 0x1b4c5d3]  ; -> 01F44830 [u64 0x00002B992DDFA232]
003F825D  xor      rax, rsp
003F8260  mov      qword ptr [rsp + 0x38], rax
003F8265  mov      r8, qword ptr [rcx + 0xe0]
003F826C  mov      rdi, rcx
003F826F  mov      ecx, dword ptr [rdx]
003F8271  sub      ecx, 1
003F8274  je       0x3f83ba  ; -> 003F83BA
003F827A  sub      ecx, 1
003F827D  je       0x3f8351  ; -> 003F8351
003F8283  sub      ecx, 2
003F8286  je       0x3f82b5  ; -> 003F82B5
003F8288  sub      ecx, 0xa
003F828B  je       0x3f846d  ; -> 003F846D
003F8291  cmp      ecx, 1
003F8294  je       0x3f846d  ; -> 003F846D
003F829A  mov      rcx, rdi
003F829D  call     0x5c5230  ; -> 005C5230 fn
003F82A2  mov      rcx, qword ptr [rsp + 0x38]
003F82A7  xor      rcx, rsp
003F82AA  call     0x808c40  ; -> 00808C40 fn
003F82AF  add      rsp, 0x40
003F82B3  pop      rdi
003F82B4  ret      
003F82B5  mov      qword ptr [rsp + 0x60], rbx
003F82BA  test     r8, r8
003F82BD  je       0x3f82cc  ; -> 003F82CC
003F82BF  mov      ecx, dword ptr [r8 + 0x754]
003F82C6  mov      dword ptr [rdi + 0x108], ecx
003F82CC  movzx    eax, word ptr [rdi + 0x9c]
003F82D3  lea      rdx, [rdi + 0xe8]
003F82DA  mov      rbx, qword ptr [rdi + 0x38]
003F82DE  xor      ecx, ecx
003F82E0  mov      word ptr [rsp + 0x24], ax
003F82E5  movzx    eax, word ptr [rdi + 0x9e]
003F82EC  mov      dword ptr [rsp + 0x20], ecx
003F82F0  mov      dword ptr [rsp + 0x2c], ecx
003F82F4  mov      dword ptr [rsp + 0x34], ecx
003F82F8  mov      rcx, rbx
003F82FB  mov      word ptr [rsp + 0x26], ax
003F8300  mov      dword ptr [rsp + 0x28], 0x80000000
003F8308  mov      dword ptr [rsp + 0x30], 0x80000000
003F8310  call     0x2dd2f0  ; -> 002DD2F0 fn
003F8315  lea      r8, [rsp + 0x28]
003F831A  mov      rcx, rbx
003F831D  lea      rdx, [rsp + 0x20]
003F8322  call     0x2dc290  ; -> 002DC290 fn
003F8327  mov      dword ptr [rbx + 0x60], 0x3f400000
003F832E  mov      eax, 0x30
003F8333  cmp      dword ptr [rdi + 0x108], 0
003F833A  mov      ecx, 0x80
003F833F  cmovne   ax, cx
003F8343  mov      word ptr [rbx + 0x5a], ax
003F8347  mov      rbx, qword ptr [rsp + 0x60]
003F834C  jmp      0x3f846d  ; -> 003F846D
003F8351  test     r8, r8
003F8354  je       0x3f846d  ; -> 003F846D
003F835A  mov      edx, 1
003F835F  mov      rcx, rdi
003F8362  call     0x3f8790  ; -> 003F8790 fn
003F8367  cmp      dword ptr [rdi + 0x104], eax
003F836D  je       0x3f83a7  ; -> 003F83A7
003F836F  xor      ecx, ecx
003F8371  mov      dword ptr [rdi + 0x104], eax
003F8377  mov      dword ptr [rdi + 0x100], ecx
003F837D  mov      edx, 4
003F8382  mov      rcx, qword ptr [rdi + 0xe8]
003F8389  sub      dx, ax
003F838C  mov      qword ptr [rdi + 0xf8], rcx
003F8393  movzx    ecx, dx
003F8396  shl      cx, 3
003F839A  add      dx, cx
003F839D  add      dx, dx
003F83A0  mov      word ptr [rdi + 0xf2], dx
003F83A7  mov      rcx, rdi
003F83AA  mov      dword ptr [rdi + 0x104], eax
003F83B0  call     0x3f8140  ; -> 003F8140 fn
003F83B5  jmp      0x3f846d  ; -> 003F846D
003F83BA  mov      rax, qword ptr [rdx + 8]
003F83BE  mov      rcx, rdi
003F83C1  mov      edx, 0x65
003F83C6  mov      qword ptr [rdi + 0xe0], rax
003F83CD  call     0x247930  ; -> 00247930 fn
003F83D2  mov      ecx, 6
003F83D7  call     0x2735e0  ; -> 002735E0 fn
003F83DC  mov      rdx, rax
003F83DF  mov      rcx, rdi
003F83E2  call     0x247570  ; -> 00247570 fn
003F83E7  and      dword ptr [rdi + 0x40], 0xffffff7f
003F83EE  xor      edx, edx
003F83F0  mov      rcx, rdi
003F83F3  call     0x3f8790  ; -> 003F8790 fn
003F83F8  mov      dword ptr [rdi + 0x104], eax
003F83FE  xor      ecx, ecx
003F8400  mov      word ptr [rdi + 0xe8], cx
003F8407  mov      edx, 4
003F840C  sub      dx, ax
003F840F  mov      dword ptr [rdi + 0xec], 0x5000b4
003F8419  movzx    eax, dx
003F841C  mov      dword ptr [rdi + 0x100], 0x3f800000
003F8426  shl      ax, 3
003F842A  add      dx, ax
003F842D  add      dx, dx
003F8430  mov      word ptr [rdi + 0xea], dx
003F8437  mov      rax, qword ptr [rdi + 0xe8]
003F843E  mov      qword ptr [rdi + 0xf0], rax
003F8445  mov      qword ptr [rdi + 0xf8], rax
003F844C  mov      eax, dword ptr [rip + 0x1a13d8a]  ; -> 01E0C1DC [u32 0x000001C0]
003F8452  add      eax, -0x5c
003F8455  mov      word ptr [rdi + 0x98], cx
003F845C  mov      word ptr [rdi + 0x9a], ax
003F8463  mov      dword ptr [rdi + 0x9c], 0x5000b4
003F846D  xor      eax, eax
003F846F  mov      rcx, qword ptr [rsp + 0x38]
003F8474  xor      rcx, rsp
003F8477  call     0x808c40  ; -> 00808C40 fn
003F847C  add      rsp, 0x40
003F8480  pop      rdi
003F8481  ret      
```

## 0053F460 (47 B, extent 0053F460-0053F48F)

Documented callee on this page: `00246AC0`

```
0053F460  push     rbx
0053F462  sub      rsp, 0x20
0053F466  mov      rbx, qword ptr [rip + 0x2769613]  ; -> 02CA8A80
0053F46D  test     rbx, rbx
0053F470  je       0x53f489  ; -> 0053F489
0053F472  mov      rcx, rbx
0053F475  call     0x53e580  ; -> 0053E580 fn
0053F47A  mov      rcx, rbx
0053F47D  call     0x246ac0  ; -> 00246AC0 fn
0053F482  mov      byte ptr [rbx + 0xfc], 1
0053F489  add      rsp, 0x20
0053F48D  pop      rbx
0053F48E  ret      
```

## 005617E0 (27 B, extent 005617E0-005617FB)

Documented callee on this page: `00323670`

```
005617E0  sub      rsp, 0x28
005617E4  movzx    ecx, byte ptr [rcx + 0x60]
005617E8  call     0x323670  ; -> 00323670 fn
005617ED  xor      ecx, ecx
005617EF  cmp      al, 0xff
005617F1  setne    cl
005617F4  mov      eax, ecx
005617F6  add      rsp, 0x28
005617FA  ret      
```

## 00568AA0 (137 B, extent 00568AA0-00568B29)

Documented callee on this page: `0029F6E0`

```
00568AA0  mov      qword ptr [rsp + 8], rbx
00568AA5  push     rdi
00568AA6  sub      rsp, 0x30
00568AAA  mov      edi, r9d
00568AAD  mov      rbx, rdx
00568AB0  test     r9d, r9d
00568AB3  jne      0x568acd  ; -> 00568ACD
00568AB5  xor      edx, edx
00568AB7  mov      rcx, rbx
00568ABA  call     0x243580  ; -> 00243580 fn
00568ABF  lea      eax, [rdi + 1]
00568AC2  mov      rbx, qword ptr [rsp + 0x40]
00568AC7  add      rsp, 0x30
00568ACB  pop      rdi
00568ACC  ret      
00568ACD  mov      rcx, qword ptr [rdx + 0x10]
00568AD1  mov      r9d, 0x80808080
00568AD7  mov      edx, 2
00568ADC  mov      dword ptr [rsp + 0x20], edi
00568AE0  mov      rcx, qword ptr [rcx]
00568AE3  lea      r8d, [rdx + 0xe]
00568AE7  call     0x29f6e0  ; -> 0029F6E0 fn
00568AEC  call     0x254a10  ; -> 00254A10 fn
00568AF1  test     eax, eax
00568AF3  jne      0x568b19  ; -> 00568B19
00568AF5  mov      rax, qword ptr [rbx + 0x10]
00568AF9  mov      rdx, qword ptr [rax + 8]
00568AFD  cmp      edi, 0xa
00568B00  jge      0x568b0e  ; -> 00568B0E
00568B02  mov      rax, qword ptr [rax]
00568B05  movzx    ecx, word ptr [rax + 0xc]
00568B09  inc      cx
00568B0C  jmp      0x568b15  ; -> 00568B15
00568B0E  mov      rax, qword ptr [rdx]
00568B11  movzx    ecx, word ptr [rax + 4]
00568B15  mov      word ptr [rdx + 0xc], cx
00568B19  mov      eax, 1
00568B1E  mov      rbx, qword ptr [rsp + 0x40]
00568B23  add      rsp, 0x30
00568B27  pop      rdi
00568B28  ret      
```
