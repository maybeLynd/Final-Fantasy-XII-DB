# F homing pack (FABLE): `00-Engine-Core-Runtime/Ownership-Boundary/intentionally-ownerless-functions-and-shared-scratch.md`

Generated 2026-10-03 04:02 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 13. No bearing page cites them and no documented function calls them directly.

## 00182BE0 (187 B, extent 00182BE0-00182C9B)

Documented callee on this page: `001B66F0`

```
00182BE0  sub      rsp, 0x58
00182BE4  movaps   xmmword ptr [rsp + 0x40], xmm6
00182BE9  movaps   xmm6, xmm1
00182BEC  movaps   xmmword ptr [rsp + 0x30], xmm7
00182BF1  movaps   xmm7, xmm0
00182BF4  call     0x1b6c40  ; -> 001B6C40 fn
00182BF9  test     rax, rax
00182BFC  je       0x182c8a  ; -> 00182C8A
00182C02  call     0x189120  ; -> 00189120 fn
00182C07  test     rax, rax
00182C0A  je       0x182c8a  ; -> 00182C8A
00182C0C  call     0x189120  ; -> 00189120 fn
00182C11  mov      rcx, rax
00182C14  call     0x186aa0  ; -> 00186AA0 fn
00182C19  mov      eax, eax
00182C1B  xorps    xmm0, xmm0
00182C1E  cvtsi2ss xmm0, rax
00182C23  mulss    xmm0, xmm7
00182C27  cvttss2si eax, xmm0
00182C2B  mov      dword ptr [rsp + 0x20], eax
00182C2F  call     0x189120  ; -> 00189120 fn
00182C34  mov      rcx, rax
00182C37  call     0x186a90  ; -> 00186A90 fn
00182C3C  mov      eax, eax
00182C3E  xorps    xmm0, xmm0
00182C41  cvtsi2ss xmm0, rax
00182C46  mulss    xmm0, xmm6
00182C4A  cvttss2si eax, xmm0
00182C4E  mov      dword ptr [rsp + 0x24], eax
00182C52  lea      rax, [rip + 0x2b74827]  ; -> 02CF7480
00182C59  mov      qword ptr [rsp + 0x28], rax
00182C5E  movaps   xmm0, xmmword ptr [rsp + 0x20]
00182C63  movdqa   xmmword ptr [rsp + 0x20], xmm0
00182C69  call     0x1b6c40  ; -> 001B6C40 fn
00182C6E  mov      rcx, rax
00182C71  lea      rdx, [rsp + 0x20]
00182C76  call     0x1b66f0  ; -> 001B66F0 fn
00182C7B  movaps   xmm6, xmmword ptr [rsp + 0x40]
00182C80  movaps   xmm7, xmmword ptr [rsp + 0x30]
00182C85  add      rsp, 0x58
00182C89  ret      
00182C8A  movaps   xmm6, xmmword ptr [rsp + 0x40]
00182C8F  xor      eax, eax
00182C91  movaps   xmm7, xmmword ptr [rsp + 0x30]
00182C96  add      rsp, 0x58
00182C9A  ret      
```

## 0024E0F0 (142 B, extent 0024E0F0-0024E17E)

Documented callee on this page: `00182B40`

```
0024E0F0  sub      rsp, 0x28
0024E0F4  movzx    eax, word ptr [rip + 0x1e445e9]  ; -> 020926E4
0024E0FB  mov      ecx, 0xfffb
0024E100  and      ax, cx
0024E103  mov      rcx, qword ptr [rip + 0x1e445ce]  ; -> 020926D8
0024E10A  or       ax, 2
0024E10E  mov      word ptr [rip + 0x1e445cf], ax  ; -> 020926E4
0024E115  test     rcx, rcx
0024E118  je       0x24e147  ; -> 0024E147
0024E11A  movzx    eax, word ptr [rip + 0x1e44049]  ; -> 0209216A
0024E121  mov      edx, 0x100
0024E126  cmp      ax, dx
0024E129  jb       0x24e132  ; -> 0024E132
0024E12B  call     0x182ca0  ; -> 00182CA0 fn
0024E130  jmp      0x24e147  ; -> 0024E147
0024E132  movzx    eax, ax
0024E135  lea      rdx, [rip + 0x1e43814]  ; -> 02091950
0024E13C  mov      qword ptr [rdx + rax*8], rcx
0024E140  inc      word ptr [rip + 0x1e44023]  ; -> 0209216A
0024E147  movss    xmm0, dword ptr [rip + 0x1a9da59]  ; -> 01CEBBA8 [f32 1]
0024E14F  movaps   xmm1, xmm0
0024E152  call     0x182b40  ; -> 00182B40 fn
0024E157  mov      qword ptr [rip + 0x1e4457a], rax  ; -> 020926D8
0024E15E  mov      dword ptr [rip + 0x1e44578], 0  ; -> 020926E0
0024E168  test     rax, rax
0024E16B  jne      0x24e179  ; -> 0024E179
0024E16D  mov      eax, 0xfff9
0024E172  and      word ptr [rip + 0x1e4456b], ax  ; -> 020926E4
0024E179  add      rsp, 0x28
0024E17D  ret      
```

## 0024F6C0 (179 B, extent 0024F6C0-0024F773)

Documented callee on this page: `00182B40`

```
0024F6C0  sub      rsp, 0x28
0024F6C4  mov      eax, dword ptr [rip + 0x1e4301a]  ; -> 020926E4
0024F6CA  shr      eax, 6
0024F6CD  and      eax, 1
0024F6D0  cmp      ecx, eax
0024F6D2  je       0x24f76e  ; -> 0024F76E
0024F6D8  movzx    eax, word ptr [rip + 0x1e43005]  ; -> 020926E4
0024F6DF  movzx    edx, cx
0024F6E2  shl      dx, 6
0024F6E6  xor      dx, ax
0024F6E9  and      dx, 0x40
0024F6ED  xor      ax, dx
0024F6F0  mov      word ptr [rip + 0x1e42fed], ax  ; -> 020926E4
0024F6F7  test     ecx, ecx
0024F6F9  je       0x24f71c  ; -> 0024F71C
0024F6FB  cmp      ecx, 1
0024F6FE  jne      0x24f76e  ; -> 0024F76E
0024F700  movss    xmm0, dword ptr [rip + 0x1a9c468]  ; -> 01CEBB70 [f32 0.5]
0024F708  movaps   xmm1, xmm0
0024F70B  call     0x182b40  ; -> 00182B40 fn
0024F710  mov      qword ptr [rip + 0x1e42fb9], rax  ; -> 020926D0
0024F717  add      rsp, 0x28
0024F71B  ret      
0024F71C  mov      rcx, qword ptr [rip + 0x1e42fad]  ; -> 020926D0
0024F723  test     rcx, rcx
0024F726  je       0x24f76e  ; -> 0024F76E
0024F728  movzx    eax, word ptr [rip + 0x1e42a3b]  ; -> 0209216A
0024F72F  mov      edx, 0x100
0024F734  cmp      ax, dx
0024F737  jb       0x24f74e  ; -> 0024F74E
0024F739  call     0x182ca0  ; -> 00182CA0 fn
0024F73E  mov      qword ptr [rip + 0x1e42f87], 0  ; -> 020926D0
0024F749  add      rsp, 0x28
0024F74D  ret      
0024F74E  movzx    eax, ax
0024F751  lea      rdx, [rip + 0x1e421f8]  ; -> 02091950
0024F758  mov      qword ptr [rdx + rax*8], rcx
0024F75C  inc      word ptr [rip + 0x1e42a07]  ; -> 0209216A
0024F763  mov      qword ptr [rip + 0x1e42f62], 0  ; -> 020926D0
0024F76E  add      rsp, 0x28
0024F772  ret      
```

## 0029BE50 (1663 B, extent 0029BE50-0029C4CF)

Documented callee on this page: `0029B870`

```
0029BE50  push     rbx
0029BE52  push     rdi
0029BE53  sub      rsp, 0x68
0029BE57  mov      rax, qword ptr [rip + 0x1ca89d2]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0029BE5E  xor      rax, rsp
0029BE61  mov      qword ptr [rsp + 0x50], rax
0029BE66  mov      eax, dword ptr [rdx]
0029BE68  mov      rbx, rcx
0029BE6B  dec      eax
0029BE6D  cmp      eax, 0x1d
0029BE70  ja       0x29c4b3  ; -> 0029C4B3
0029BE76  lea      rdi, [rip - 0x17be7d]  ; -> 00120000 (image base)
0029BE7D  cdqe     
0029BE7F  movzx    eax, byte ptr [rdi + rax + 0x17c4f0]
0029BE87  mov      ecx, dword ptr [rdi + rax*4 + 0x17c4d0]  ; image base + 0x17c4d0 = 0029C4D0
0029BE8E  add      rcx, rdi
0029BE91  jmp      rcx
0029BE93  mov      rax, qword ptr [rip + 0x1dfed96]  ; -> 0209AC30
0029BE9A  lea      rcx, [rbx + 0x50]
0029BE9E  mov      r9, rbx
0029BEA1  mov      r8d, 0x15
0029BEA7  mov      rdx, qword ptr [rax + 8]
0029BEAB  call     0x2432b0  ; -> 002432B0 fn
0029BEB0  movzx    ecx, word ptr [rax + 0xa]
0029BEB4  movzx    edx, word ptr [rax + 8]
0029BEB8  movsx    r8d, word ptr [rax + 6]
0029BEBD  test     rbx, rbx
0029BEC0  je       0x29bee3  ; -> 0029BEE3
0029BEC2  movzx    eax, word ptr [rax + 4]
0029BEC6  mov      word ptr [rbx + 0x98], ax
0029BECD  mov      word ptr [rbx + 0x9a], r8w
0029BED5  mov      word ptr [rbx + 0x9c], dx
0029BEDC  mov      word ptr [rbx + 0x9e], cx
0029BEE3  mov      ecx, 5
0029BEE8  call     0x2735e0  ; -> 002735E0 fn
0029BEED  mov      rdx, rax
0029BEF0  mov      rcx, rbx
0029BEF3  call     0x247570  ; -> 00247570 fn
0029BEF8  call     0x35bb60  ; -> 0035BB60 fn
0029BEFD  xor      r8d, r8d
0029BF00  mov      byte ptr [rbx + 0xb42], al
0029BF06  lea      rdx, [rip - 0x80d]  ; -> 0029B700
0029BF0D  mov      ecx, 0xc0
0029BF12  call     0x244f50  ; -> 00244F50 fn
0029BF17  mov      qword ptr [rbx + 0xb38], rax
0029BF1E  call     0x35bae0  ; -> 0035BAE0 fn
0029BF23  mov      word ptr [rbx + 0xb40], ax
0029BF2A  call     0x35bae0  ; -> 0035BAE0 fn
0029BF2F  movzx    ecx, byte ptr [rbx + 0xb42]
0029BF36  mov      r8, qword ptr [rbx + 0xb38]
0029BF3D  sub      cx, ax
0029BF40  dec      cx
0029BF43  movsx    ecx, cx
0029BF46  mov      rdx, qword ptr [r8 + 0x58]
0029BF4A  movsx    eax, word ptr [rdx + 0xc]
0029BF4E  imul     ecx, eax
0029BF51  movzx    eax, word ptr [rdx + 6]
0029BF55  sub      ax, cx
0029BF58  mov      rcx, rbx
0029BF5B  mov      word ptr [r8 + 0x9a], ax
0029BF63  mov      rdx, qword ptr [rbx + 0xb38]
0029BF6A  call     0x244960  ; -> 00244960 fn
0029BF6F  mov      edx, 0xa0
0029BF74  mov      rcx, rbx
0029BF77  call     0x247930  ; -> 00247930 fn
0029BF7C  call     0x1e0f20  ; -> 001E0F20 fn
0029BF81  xor      eax, eax
0029BF83  jmp      0x29c4bb  ; -> 0029C4BB
0029BF88  mov      rcx, rbx
0029BF8B  call     0x29bb40  ; -> 0029BB40 fn
0029BF90  test     eax, eax
0029BF92  je       0x29c263  ; -> 0029C263
0029BF98  mov      rcx, rbx
0029BF9B  call     0x29bb40  ; -> 0029BB40 fn
0029BFA0  xor      eax, eax
0029BFA2  jmp      0x29c4bb  ; -> 0029C4BB
0029BFA7  test     byte ptr [rbx + 0xb4a], 2
0029BFAE  jne      0x29bfc9  ; -> 0029BFC9
0029BFB0  mov      ecx, 4
0029BFB5  call     0x249c60  ; -> 00249C60 fn
0029BFBA  or       word ptr [rbx + 0xb4a], 2
0029BFC2  xor      eax, eax
0029BFC4  jmp      0x29c4bb  ; -> 0029C4BB
0029BFC9  mov      rcx, rbx
0029BFCC  call     0x29b870  ; -> 0029B870 fn
0029BFD1  mov      byte ptr [rbx + 0xb43], al
0029BFD7  movzx    eax, al
0029BFDA  add      eax, -2
0029BFDD  cmp      eax, 6
0029BFE0  ja       0x29c263  ; -> 0029C263
0029BFE6  cdqe     
0029BFE8  mov      ecx, dword ptr [rdi + rax*4 + 0x17c510]  ; image base + 0x17c510 = 0029C510
0029BFEF  add      rcx, rdi
0029BFF2  jmp      rcx
0029BFF4  cmp      byte ptr [rbx + 0xb49], 1
0029BFFB  jne      0x29c263  ; -> 0029C263
0029C001  movsx    ecx, byte ptr [rbx + 0xb48]
0029C008  call     0x35bb20  ; -> 0035BB20 fn
0029C00D  movsx    ecx, word ptr [rax + 0x60]
0029C011  call     0x35baa0  ; -> 0035BAA0 fn
0029C016  mov      ecx, 1
0029C01B  call     0x35c100  ; -> 0035C100 fn
0029C020  call     0x35da80  ; -> 0035DA80 fn
0029C025  xor      ecx, ecx
0029C027  call     0x3c93e0  ; -> 003C93E0 fn
0029C02C  call     0x35c080  ; -> 0035C080 fn
0029C031  xor      ecx, ecx
0029C033  call     0x35c050  ; -> 0035C050 fn
0029C038  xor      eax, eax
0029C03A  jmp      0x29c4bb  ; -> 0029C4BB
0029C03F  cmp      byte ptr [rbx + 0xb49], 1
0029C046  jne      0x29c263  ; -> 0029C263
0029C04C  call     0x35d8d0  ; -> 0035D8D0 fn
0029C051  xor      ecx, ecx
0029C053  call     0x3c93e0  ; -> 003C93E0 fn
0029C058  call     0x35c080  ; -> 0035C080 fn
0029C05D  xor      eax, eax
0029C05F  jmp      0x29c4bb  ; -> 0029C4BB
0029C064  movzx    eax, word ptr [rbx + 0xb4a]
0029C06B  test     al, al
0029C06D  jns      0x29c0b7  ; -> 0029C0B7
0029C06F  test     al, 0x20
0029C071  je       0x29c084  ; -> 0029C084
0029C073  mov      ecx, 0xff7f
0029C078  and      ax, cx
0029C07B  mov      word ptr [rbx + 0xb4a], ax
0029C082  jmp      0x29c0b7  ; -> 0029C0B7
0029C084  call     0x2906d0  ; -> 002906D0 fn
0029C089  test     eax, eax
0029C08B  je       0x29c0b7  ; -> 0029C0B7
0029C08D  call     0x35d320  ; -> 0035D320 fn
0029C092  movsx    rcx, byte ptr [rbx + 0xb48]
0029C09A  lea      rdx, [rcx + rcx*2]
0029C09E  shl      rdx, 6
0029C0A2  mov      ecx, dword ptr [rax + rdx + 0x24]
0029C0A6  call     0x29b440  ; -> 0029B440 fn
0029C0AB  mov      ecx, 0xff7f
0029C0B0  and      word ptr [rbx + 0xb4a], cx
0029C0B7  test     byte ptr [rbx + 0xb4a], 0x40
0029C0BE  mov      qword ptr [rsp + 0x98], rsi
0029C0C6  je       0x29c154  ; -> 0029C154
0029C0CC  xor      esi, esi
0029C0CE  nop      
0029C0D0  movsxd   rdi, esi
0029C0D3  lea      rcx, [rbx + 0x240]
0029C0DA  imul     rax, rdi, 0x160
0029C0E1  add      rcx, rax
0029C0E4  call     0x273a20  ; -> 00273A20 fn
0029C0E9  test     eax, eax
0029C0EB  jne      0x29c25b  ; -> 0029C25B
0029C0F1  imul     rax, rdi, 0xd8
0029C0F8  lea      rcx, [rbx + 0x7c0]
0029C0FF  add      rcx, rax
0029C102  call     0x273a20  ; -> 00273A20 fn
0029C107  test     eax, eax
0029C109  jne      0x29c25b  ; -> 0029C25B
0029C10F  inc      esi
0029C111  cmp      esi, 4
0029C114  jb       0x29c0d0  ; -> 0029C0D0
0029C116  call     0x35bb60  ; -> 0035BB60 fn
0029C11B  mov      rcx, rbx
0029C11E  mov      byte ptr [rbx + 0xb42], al
0029C124  call     0x29bb40  ; -> 0029BB40 fn
0029C129  test     eax, eax
0029C12B  je       0x29c25b  ; -> 0029C25B
0029C131  mov      rcx, rbx
0029C134  call     0x29bb40  ; -> 0029BB40 fn
0029C139  mov      rsi, qword ptr [rsp + 0x98]
0029C141  mov      eax, 0xffaf
0029C146  and      word ptr [rbx + 0xb4a], ax
0029C14D  xor      eax, eax
0029C14F  jmp      0x29c4bb  ; -> 0029C4BB
0029C154  mov      qword ptr [rsp + 0x90], rbp
0029C15C  mov      qword ptr [rsp + 0x60], r14
0029C161  call     0x35bb60  ; -> 0035BB60 fn
0029C166  movzx    ecx, byte ptr [rbx + 0xb42]
0029C16D  cmp      ecx, eax
0029C16F  je       0x29c26a  ; -> 0029C26A
0029C175  xor      esi, esi
0029C177  mov      r14d, 0xffff
0029C17D  mov      edi, esi
0029C17F  nop      
0029C180  imul     rbp, rdi, 0x160
0029C187  lea      rcx, [rbx + 0x240]
0029C18E  add      rcx, rbp
0029C191  call     0x273a20  ; -> 00273A20 fn
0029C196  test     eax, eax
0029C198  je       0x29c1a9  ; -> 0029C1A9
0029C19A  lea      rcx, [rbx + 0x240]
0029C1A1  add      rcx, rbp
0029C1A4  call     0x245020  ; -> 00245020 fn
0029C1A9  imul     rdi, rdi, 0xd8
0029C1B0  lea      rcx, [rbx + 0x7c0]
0029C1B7  add      rcx, rdi
0029C1BA  call     0x273a20  ; -> 00273A20 fn
0029C1BF  test     eax, eax
0029C1C1  je       0x29c1d2  ; -> 0029C1D2
0029C1C3  lea      rcx, [rbx + 0x7c0]
0029C1CA  add      rcx, rdi
0029C1CD  call     0x245020  ; -> 00245020 fn
0029C1D2  mov      ecx, esi
0029C1D4  call     0x28f830  ; -> 0028F830 fn
0029C1D9  xor      ecx, ecx
0029C1DB  mov      qword ptr [rax], rcx
0029C1DE  mov      qword ptr [rax + 8], rcx
0029C1E2  mov      qword ptr [rax + 0x10], rcx
0029C1E6  mov      qword ptr [rax + 0x18], rcx
0029C1EA  mov      byte ptr [rax], sil
0029C1ED  inc      esi
0029C1EF  movsxd   rdi, esi
0029C1F2  mov      byte ptr [rax + 1], 0xff
0029C1F6  mov      byte ptr [rax + 0x13], 0xff
0029C1FA  mov      word ptr [rax + 4], r14w
0029C1FF  cmp      rdi, 4
0029C203  jb       0x29c180  ; -> 0029C180
0029C209  call     0x35bb60  ; -> 0035BB60 fn
0029C20E  mov      r9, qword ptr [rbx + 0xb38]
0029C215  movsx    ecx, word ptr [rbx + 0xb40]
0029C21C  mov      byte ptr [rbx + 0xb42], al
0029C222  movzx    edx, al
0029C225  mov      r8, qword ptr [r9 + 0x58]
0029C229  sub      edx, ecx
0029C22B  dec      edx
0029C22D  imul     edx, dword ptr [r8 + 0xc]
0029C232  movsx    ecx, word ptr [r8 + 6]
0029C237  sub      ecx, edx
0029C239  test     r9, r9
0029C23C  je       0x29c246  ; -> 0029C246
0029C23E  mov      word ptr [r9 + 0x9a], cx
0029C246  or       word ptr [rbx + 0xb4a], 0x40
0029C24E  mov      rbp, qword ptr [rsp + 0x90]
0029C256  mov      r14, qword ptr [rsp + 0x60]
0029C25B  mov      rsi, qword ptr [rsp + 0x98]
0029C263  xor      eax, eax
0029C265  jmp      0x29c4bb  ; -> 0029C4BB
0029C26A  test     byte ptr [rbx + 0xb4a], 0x20
0029C271  jne      0x29c24e  ; -> 0029C24E
0029C273  call     0x35bae0  ; -> 0035BAE0 fn
0029C278  mov      r10, qword ptr [rbx + 0xb38]
0029C27F  mov      r8d, eax
0029C282  test     r10, r10
0029C285  je       0x29c2de  ; -> 0029C2DE
0029C287  movsx    ecx, word ptr [rbx + 0xb40]
0029C28E  cmp      ecx, eax
0029C290  je       0x29c2de  ; -> 0029C2DE
0029C292  mov      ecx, dword ptr [r10 + 0x80]
0029C299  and      ecx, 1
0029C29C  jne      0x29c2de  ; -> 0029C2DE
0029C29E  movzx    edx, byte ptr [rbx + 0xb42]
0029C2A5  lea      r9d, [rcx + 1]
0029C2A9  mov      word ptr [rbx + 0xb40], r8w
0029C2B1  sub      edx, r8d
0029C2B4  mov      rax, qword ptr [r10 + 0x58]
0029C2B8  dec      edx
0029C2BA  mov      rcx, r10
0029C2BD  mov      dword ptr [rsp + 0x20], 0xc8
0029C2C5  imul     edx, dword ptr [rax + 0xc]
0029C2C9  movsx    r8d, word ptr [rax + 6]
0029C2CE  sub      r8d, edx
0029C2D1  movsx    edx, word ptr [r10 + 0x98]
0029C2D9  call     0x2468a0  ; -> 002468A0 fn
0029C2DE  mov      eax, dword ptr [rbx + 0x7c]
0029C2E1  xor      esi, esi
0029C2E3  and      eax, 0xf
0029C2E6  mov      ecx, esi
0029C2E8  cmp      al, 3
0029C2EA  sete     cl
0029C2ED  test     ecx, ecx
0029C2EF  je       0x29c24e  ; -> 0029C24E
0029C2F5  test     byte ptr [rbx + 0xb4a], 0x10
0029C2FC  jne      0x29c3b9  ; -> 0029C3B9
0029C302  mov      eax, dword ptr [rbx + 0x40]
0029C305  shr      eax, 9
0029C308  and      eax, 1
0029C30B  jne      0x29c3b9  ; -> 0029C3B9
0029C311  xorps    xmm0, xmm0
0029C314  mov      dword ptr [rsp + 0x38], esi
0029C318  movdqu   xmmword ptr [rsp + 0x40], xmm0
0029C31E  cmp      byte ptr [rbx + 0xb42], sil
0029C325  jbe      0x29c3b1  ; -> 0029C3B1
0029C32B  lea      rbp, [rbx + 0x2da]
0029C332  mov      r14d, 0xfffc
0029C338  nop      dword ptr [rax + rax]
0029C340  movsx    rax, word ptr [rbp]
0029C345  lea      r9, [rsp + 0x38]
0029C34A  movsxd   rcx, esi
0029C34D  lea      r8, [rip - 0x32c4]  ; -> 00299090
0029C354  mov      qword ptr [rsp + 0x40], rcx
0029C359  mov      edx, 0xd8
0029C35E  mov      qword ptr [rsp + 0x48], rax
0029C363  imul     rax, rcx, 0xd8
0029C36A  lea      rcx, [rbx + 0x7c0]
0029C371  add      rcx, rax
0029C374  call     0x245000  ; -> 00245000 fn
0029C379  xor      edx, edx
0029C37B  mov      rcx, rax
0029C37E  mov      rdi, rax
0029C381  call     0x247870  ; -> 00247870 fn
0029C386  mov      rdx, rdi
0029C389  mov      rcx, rbx
0029C38C  call     0x244960  ; -> 00244960 fn
0029C391  mov      rax, qword ptr [rdi + 0xc0]
0029C398  lea      rbp, [rbp + 0x160]
0029C39F  inc      esi
0029C3A1  and      word ptr [rax + 2], r14w
0029C3A6  movzx    eax, byte ptr [rbx + 0xb42]
0029C3AD  cmp      esi, eax
0029C3AF  jl       0x29c340  ; -> 0029C340
0029C3B1  or       word ptr [rbx + 0xb4a], 0x10
0029C3B9  test     byte ptr [rbx + 0xb4a], 8
0029C3C0  je       0x29c3ce  ; -> 0029C3CE
0029C3C2  lea      rcx, [rbx + 0xc0]
0029C3C9  call     0x273a20  ; -> 00273A20 fn
0029C3CE  movzx    eax, word ptr [rbx + 0xb4a]
0029C3D5  test     al, 4
0029C3D7  je       0x29c403  ; -> 0029C403
0029C3D9  mov      rcx, rbx
0029C3DC  call     0x29c850  ; -> 0029C850 fn
0029C3E1  test     eax, eax
0029C3E3  je       0x29c44b  ; -> 0029C44B
0029C3E5  mov      eax, 0xfffb
0029C3EA  and      word ptr [rbx + 0xb4a], ax
0029C3F1  or       word ptr [rbx + 0xb4a], 8
0029C3F9  call     0x2962d0  ; -> 002962D0 fn
0029C3FE  jmp      0x29c24e  ; -> 0029C24E
0029C403  test     al, 1
0029C405  je       0x29c429  ; -> 0029C429
0029C407  mov      rcx, rbx
0029C40A  call     0x29c9d0  ; -> 0029C9D0 fn
0029C40F  test     eax, eax
0029C411  je       0x29c44b  ; -> 0029C44B
0029C413  mov      eax, 0xfffe
0029C418  and      word ptr [rbx + 0xb4a], ax
0029C41F  call     0x2962d0  ; -> 002962D0 fn
0029C424  jmp      0x29c24e  ; -> 0029C24E
0029C429  mov      ecx, 0x100
0029C42E  test     cx, ax
0029C431  je       0x29c44b  ; -> 0029C44B
0029C433  mov      rcx, rbx
0029C436  call     0x29c770  ; -> 0029C770 fn
0029C43B  test     eax, eax
0029C43D  je       0x29c44b  ; -> 0029C44B
0029C43F  mov      eax, 0xfeff
0029C444  and      word ptr [rbx + 0xb4a], ax
0029C44B  call     0x2962d0  ; -> 002962D0 fn
0029C450  jmp      0x29c24e  ; -> 0029C24E
0029C455  call     0x290630  ; -> 00290630 fn
0029C45A  xor      ecx, ecx
0029C45C  call     0x3c93e0  ; -> 003C93E0 fn
0029C461  call     0x35c080  ; -> 0035C080 fn
0029C466  xorps    xmm0, xmm0
0029C469  mov      dword ptr [rsp + 0x38], 0x1d
0029C471  lea      rdx, [rsp + 0x38]
0029C476  mov      rcx, rbx
0029C479  movdqu   xmmword ptr [rsp + 0x40], xmm0
0029C47F  call     0x2753f0  ; -> 002753F0 fn
0029C484  or       word ptr [rbx + 0xb4a], 0x20
0029C48C  xor      eax, eax
0029C48E  jmp      0x29c4bb  ; -> 0029C4BB
0029C490  mov      rax, qword ptr [rbx + 0xb28]
0029C497  test     rax, rax
0029C49A  je       0x29c263  ; -> 0029C263
0029C4A0  mov      r8d, dword ptr [rdx + 8]
0029C4A4  mov      rdx, qword ptr [rdx + 0x10]
0029C4A8  mov      rcx, qword ptr [rbx + 0xb30]
0029C4AF  call     rax
0029C4B1  jmp      0x29c4bb  ; -> 0029C4BB
0029C4B3  mov      rcx, rbx
0029C4B6  call     0x5c5230  ; -> 005C5230 fn
0029C4BB  mov      rcx, qword ptr [rsp + 0x50]
0029C4C0  xor      rcx, rsp
0029C4C3  call     0x808c40  ; -> 00808C40 fn
0029C4C8  add      rsp, 0x68
0029C4CC  pop      rdi
0029C4CD  pop      rbx
0029C4CE  ret      
```

## 002E8400 (72 B, extent 002E8400-002E8448)

Documented callee on this page: `00428AF0`

```
002E8400  test     rcx, rcx
002E8403  je       0x2e8447  ; -> 002E8447
002E8405  mov      rax, qword ptr [rcx + 0xc0]
002E840C  test     rax, rax
002E840F  je       0x2e8447  ; -> 002E8447
002E8411  cmp      dword ptr [rax], -1
002E8414  je       0x2e8447  ; -> 002E8447
002E8416  movzx    ecx, word ptr [rax]
002E8419  cmp      cx, -1
002E841D  je       0x2e8447  ; -> 002E8447
002E841F  movsx    rax, cx
002E8423  imul     rcx, rax, 0x740
002E842A  add      rcx, qword ptr [rip + 0x1fdeaf7]  ; -> 022C6F28
002E8431  je       0x2e8447  ; -> 002E8447
002E8433  cmp      dword ptr [rcx + 0x284], 0
002E843A  je       0x2e8447  ; -> 002E8447
002E843C  mov      r9b, 0x40
002E843F  xor      r8d, r8d
002E8442  jmp      0x428af0  ; -> 00428AF0 fn
002E8447  ret      
```

## 003460C0 (46 B, extent 003460C0-003460EE)

Documented callee on this page: `002ECF10`

```
003460C0  push     rbx
003460C2  sub      rsp, 0x20
003460C6  mov      rcx, rdx
003460C9  call     0x263f10  ; -> 00263F10 fn
003460CE  mov      rcx, rax
003460D1  mov      rbx, rax
003460D4  call     0x311f50  ; -> 00311F50 fn
003460D9  mov      edx, 1
003460DE  mov      rcx, rbx
003460E1  mov      r8d, edx
003460E4  add      rsp, 0x20
003460E8  pop      rbx
003460E9  jmp      0x2ecf10  ; -> 002ECF10 fn
```

## 00346EB0 (57 B, extent 00346EB0-00346EE9)

Documented callee on this page: `002ECF10`

```
00346EB0  push     rbx
00346EB2  sub      rsp, 0x20
00346EB6  call     0x311e90  ; -> 00311E90 fn
00346EBB  xor      ebx, ebx
00346EBD  nop      dword ptr [rax]
00346EC0  mov      ecx, ebx
00346EC2  call     0x263750  ; -> 00263750 fn
00346EC7  test     rax, rax
00346ECA  je       0x346edc  ; -> 00346EDC
00346ECC  mov      edx, 1
00346ED1  mov      rcx, rax
00346ED4  mov      r8d, edx
00346ED7  call     0x2ecf10  ; -> 002ECF10 fn
00346EDC  inc      ebx
00346EDE  cmp      ebx, 4
00346EE1  jl       0x346ec0  ; -> 00346EC0
00346EE3  add      rsp, 0x20
00346EE7  pop      rbx
00346EE8  ret      
```

## 0035B460 (71 B, extent 0035B460-0035B4A7)

Documented callee on this page: `0035B1A0`

```
0035B460  mov      qword ptr [rsp + 8], rbx
0035B465  mov      qword ptr [rsp + 0x10], rsi
0035B46A  push     rdi
0035B46B  sub      rsp, 0x20
0035B46F  lea      rbx, [rip + 0x1f6cbba]  ; -> 022C8030
0035B476  mov      edi, 8
0035B47B  xor      esi, esi
0035B47D  nop      dword ptr [rax]
0035B480  mov      ecx, dword ptr [rbx]
0035B482  test     ecx, ecx
0035B484  je       0x35b48d  ; -> 0035B48D
0035B486  call     0x35b1a0  ; -> 0035B1A0 fn
0035B48B  mov      dword ptr [rbx], esi
0035B48D  add      rbx, 4
0035B491  sub      rdi, 1
0035B495  jne      0x35b480  ; -> 0035B480
0035B497  mov      rbx, qword ptr [rsp + 0x30]
0035B49C  mov      rsi, qword ptr [rsp + 0x38]
0035B4A1  add      rsp, 0x20
0035B4A5  pop      rdi
0035B4A6  ret      
```

## 0036D050 (269 B, extent 0036D050-0036D15D)

Documented callee on this page: `0036BFE0`

```
0036D050  sub      rsp, 0x38
0036D054  mov      r10d, r8d
0036D057  mov      r8, rdx
0036D05A  test     r10d, r10d
0036D05D  jne      0x36d075  ; -> 0036D075
0036D05F  test     rdx, rdx
0036D062  je       0x36d06e  ; -> 0036D06E
0036D064  xor      edx, edx
0036D066  mov      rcx, r8
0036D069  call     0x369860  ; -> 00369860 fn
0036D06E  xor      eax, eax
0036D070  add      rsp, 0x38
0036D074  ret      
0036D075  test     r8, r8
0036D078  jne      0x36d099  ; -> 0036D099
0036D07A  mov      rax, qword ptr [rsp + 0x60]
0036D07F  mov      edx, r10d
0036D082  mov      dword ptr [rsp + 0x28], 1
0036D08A  mov      qword ptr [rsp + 0x20], rax
0036D08F  call     0x36bfe0  ; -> 0036BFE0 fn
0036D094  add      rsp, 0x38
0036D098  ret      
0036D099  mov      qword ptr [rsp + 0x40], rbx
0036D09E  lea      eax, [r10 + 0x3f]
0036D0A2  cdq      
0036D0A3  mov      qword ptr [rsp + 0x48], rbp
0036D0A8  movzx    ebp, byte ptr [r8 - 0x2a]
0036D0AD  and      edx, 0x3f
0036D0B0  mov      qword ptr [rsp + 0x50], rsi
0036D0B5  mov      esi, dword ptr [r8 - 0x28]
0036D0B9  mov      qword ptr [rsp + 0x58], rdi
0036D0BE  lea      edi, [rdx + rax]
0036D0C1  mov      qword ptr [rsp + 0x30], r14
0036D0C6  movzx    eax, byte ptr [r8 - 0x3d]
0036D0CB  lea      rdx, [r8 - 0x40]
0036D0CF  and      edi, 0xffffffc0
0036D0D2  cmp      eax, 0xf
0036D0D5  jae      0x36d0ea  ; -> 0036D0EA
0036D0D7  imul     rbx, rax, 0xa8
0036D0DE  lea      rax, [rip + 0x1f6aeeb]  ; -> 022D7FD0
0036D0E5  add      rbx, rax
0036D0E8  jmp      0x36d0ec  ; -> 0036D0EC
0036D0EA  xor      ebx, ebx
0036D0EC  movzx    eax, byte ptr [rdx + 0x17]
0036D0F0  lea      r14, [rip + 0x1f6bd19]  ; -> 022D8E10
0036D0F7  test     al, al
0036D0F9  je       0x36d102  ; -> 0036D102
0036D0FB  movzx    eax, al
0036D0FE  sub      dword ptr [r14 + rax*4], esi
0036D102  mov      rax, qword ptr [rsp + 0x60]
0036D107  mov      rcx, rbx
0036D10A  mov      qword ptr [rsp + 0x28], rax
0036D10F  mov      dword ptr [rsp + 0x20], r9d
0036D114  mov      r9d, edi
0036D117  call     0x36cb00  ; -> 0036CB00 fn
0036D11C  mov      rdx, rax
0036D11F  test     rax, rax
0036D122  je       0x36d13c  ; -> 0036D13C
0036D124  sub      edi, esi
0036D126  add      dword ptr [rbx + rbp*4 + 0x68], edi
0036D12A  movzx    eax, byte ptr [rax - 0x29]
0036D12E  test     al, al
0036D130  je       0x36d13c  ; -> 0036D13C
0036D132  movzx    ecx, al
0036D135  mov      eax, dword ptr [rdx - 0x28]
0036D138  add      dword ptr [r14 + rcx*4], eax
0036D13C  mov      r14, qword ptr [rsp + 0x30]
0036D141  mov      rax, rdx
0036D144  mov      rdi, qword ptr [rsp + 0x58]
0036D149  mov      rsi, qword ptr [rsp + 0x50]
0036D14E  mov      rbp, qword ptr [rsp + 0x48]
0036D153  mov      rbx, qword ptr [rsp + 0x40]
0036D158  add      rsp, 0x38
0036D15C  ret      
```

## 003DDF90 (208 B, extent 003DDF90-003DE060)

Documented callee on this page: `00375900`

```
003DDF90  mov      qword ptr [rsp + 8], rbx
003DDF95  mov      qword ptr [rsp + 0x10], rbp
003DDF9A  mov      qword ptr [rsp + 0x18], rsi
003DDF9F  mov      qword ptr [rsp + 0x20], rdi
003DDFA4  push     r14
003DDFA6  sub      rsp, 0x20
003DDFAA  xor      esi, esi
003DDFAC  mov      ebx, ecx
003DDFAE  mov      ebp, 3
003DDFB3  test     ecx, ecx
003DDFB5  jns      0x3ddfbb  ; -> 003DDFBB
003DDFB7  mov      eax, esi
003DDFB9  jmp      0x3ddfc2  ; -> 003DDFC2
003DDFBB  cmp      ebx, ebp
003DDFBD  mov      eax, ebx
003DDFBF  cmovg    eax, ebp
003DDFC2  cdqe     
003DDFC4  lea      r14, [rip + 0x277aab5]  ; -> 02B58A80
003DDFCB  imul     rdi, rax, 0x68
003DDFCF  mov      ecx, dword ptr [rdi + r14]
003DDFD3  test     ecx, ecx
003DDFD5  je       0x3ddfe0  ; -> 003DDFE0
003DDFD7  call     0x24cff0  ; -> 0024CFF0 fn
003DDFDC  mov      dword ptr [rdi + r14], esi
003DDFE0  test     ebx, ebx
003DDFE2  jns      0x3ddfe8  ; -> 003DDFE8
003DDFE4  mov      ebx, esi
003DDFE6  jmp      0x3ddfed  ; -> 003DDFED
003DDFE8  cmp      ebx, ebp
003DDFEA  cmovg    ebx, ebp
003DDFED  movsxd   rax, ebx
003DDFF0  imul     rbx, rax, 0x68
003DDFF4  add      rbx, r14
003DDFF7  lea      rcx, [rbx + 0x10]
003DDFFB  call     0x375900  ; -> 00375900 fn
003DE000  xor      edx, edx
003DE002  mov      dword ptr [rbx], eax
003DE004  lea      rcx, [rbx + 0x10]
003DE008  lea      r8d, [rdx + 0x58]
003DE00C  call     0x861ec0  ; -> 00861EC0 fn
003DE011  movzx    eax, byte ptr [rbx + 0x2c]
003DE015  mov      rdi, qword ptr [rsp + 0x48]
003DE01A  and      al, 0xe3
003DE01C  mov      dword ptr [rbx + 0x10], 0x13602
003DE023  or       al, bpl
003DE026  mov      rbp, qword ptr [rsp + 0x38]
003DE02B  mov      byte ptr [rbx + 0x2c], al
003DE02E  mov      qword ptr [rbx + 0x30], rsi
003DE032  mov      rsi, qword ptr [rsp + 0x40]
003DE037  mov      dword ptr [rbx + 0x38], 0x3f800000
003DE03E  mov      qword ptr [rbx + 0x3c], 0x3f800000
003DE046  mov      dword ptr [rbx + 0x44], 0x3f000000
003DE04D  mov      dword ptr [rbx + 0x48], 0x80ffffff
003DE054  mov      rbx, qword ptr [rsp + 0x30]
003DE059  add      rsp, 0x20
003DE05D  pop      r14
003DE05F  ret      
```

## 003EB940 (21 B, extent 003EB940-003EB955)

Documented callee on this page: `002EE050`

```
003EB940  test     rcx, rcx
003EB943  je       0x3eb954  ; -> 003EB954
003EB945  cmp      dword ptr [rcx + 0x10], 0
003EB949  jl       0x3eb954  ; -> 003EB954
003EB94B  movzx    ecx, word ptr [rcx + 0x10]
003EB94F  jmp      0x2ee050  ; -> 002EE050 fn
003EB954  ret      
```

## 00423380 (71 B, extent 00423380-004233C7)

Documented callee on this page: `0051B9E0`

```
00423380  push     rbx
00423382  sub      rsp, 0x20
00423386  cmp      dword ptr [rcx + 0xc4], -1
0042338D  mov      rbx, rcx
00423390  je       0x4233be  ; -> 004233BE
00423392  mov      ecx, dword ptr [rcx + 0x10]
00423395  call     0x20e600  ; -> 0020E600 fn
0042339A  mov      edx, dword ptr [rbx + 0xc4]
004233A0  mov      rcx, qword ptr [rax + 0xda8]
004233A7  call     0x51b9e0  ; -> 0051B9E0 fn
004233AC  test     rax, rax
004233AF  je       0x4233be  ; -> 004233BE
004233B1  mov      rcx, rax
004233B4  add      rsp, 0x20
004233B8  pop      rbx
004233B9  jmp      0x41c770  ; -> 0041C770 fn
004233BE  xorps    xmm0, xmm0
004233C1  add      rsp, 0x20
004233C5  pop      rbx
004233C6  ret      
```

## 00423920 (94 B, extent 00423920-0042397E)

Documented callee on this page: `0051B9E0`

```
00423920  push     rbx
00423922  sub      rsp, 0x20
00423926  cmp      dword ptr [rcx + 0xc4], -1
0042392D  mov      rbx, rcx
00423930  je       0x423978  ; -> 00423978
00423932  mov      ecx, dword ptr [rcx + 0x10]
00423935  call     0x20e600  ; -> 0020E600 fn
0042393A  mov      edx, dword ptr [rbx + 0xc4]
00423940  mov      rcx, qword ptr [rax + 0xda8]
00423947  call     0x51b9e0  ; -> 0051B9E0 fn
0042394C  mov      r8, rax
0042394F  test     rax, rax
00423952  je       0x423978  ; -> 00423978
00423954  xor      ecx, ecx
00423956  cmp      cx, word ptr [rax + 0x28]
0042395A  jge      0x423978  ; -> 00423978
0042395C  lea      rdx, [rax + 0x4c]
00423960  mov      dword ptr [rdx], 0x3f800000
00423966  lea      rdx, [rdx + 0xa0]
0042396D  movsx    eax, word ptr [r8 + 0x28]
00423972  inc      ecx
00423974  cmp      ecx, eax
00423976  jl       0x423960  ; -> 00423960
00423978  add      rsp, 0x20
0042397C  pop      rbx
0042397D  ret      
```
