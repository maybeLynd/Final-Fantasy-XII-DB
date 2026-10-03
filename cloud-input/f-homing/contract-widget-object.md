# F homing pack: `16-UI/Widget-Object-Model/CONTRACT-widget-object.md`

Generated 2026-10-02 21:56 by OPUS (homing_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 3. No bearing page cites them and no documented function calls them directly.

## 002D6DE0 (242 B, extent 002D6DE0-002D6ED2)

Documented callee on this page: `002CC8D0`

```
002D6DE0  mov      qword ptr [rsp + 0x10], rbx
002D6DE5  push     rsi
002D6DE6  sub      rsp, 0x20
002D6DEA  lea      rbx, [rcx + 0xd4]
002D6DF1  mov      qword ptr [rsp + 0x30], rdi
002D6DF6  mov      esi, 8
002D6DFB  nop      dword ptr [rax + rax]
002D6E00  movzx    ecx, byte ptr [rbx - 0xc]
002D6E04  sub      ecx, 1
002D6E07  je       0x2d6e56  ; -> 002D6E56
002D6E09  cmp      ecx, 1
002D6E0C  jne      0x2d6eb4  ; -> 002D6EB4
002D6E12  test     byte ptr [rbx], 8
002D6E15  je       0x2d6eb4  ; -> 002D6EB4
002D6E1B  mov      rax, qword ptr [rip + 0x1dc3e0e]  ; -> 0209AC30
002D6E22  lea      edx, [rcx + 0x1f]
002D6E25  lea      r9d, [rcx + 1]
002D6E29  lea      ecx, [rdx + 0x60]
002D6E2C  movzx    edi, byte ptr [rax + 0xdec]
002D6E33  mov      byte ptr [rax + 0xdec], 0
002D6E3A  mov      r8d, dword ptr [rbx - 8]
002D6E3E  call     0x2cc8d0  ; -> 002CC8D0 fn
002D6E43  mov      byte ptr [rbx - 0xb], al
002D6E46  mov      rax, qword ptr [rip + 0x1dc3de3]  ; -> 0209AC30
002D6E4D  mov      byte ptr [rax + 0xdec], dil
002D6E54  jmp      0x2d6eb4  ; -> 002D6EB4
002D6E56  movzx    eax, byte ptr [rbx - 0xa]
002D6E5A  test     al, al
002D6E5C  je       0x2d6e84  ; -> 002D6E84
002D6E5E  movsx    ecx, byte ptr [rbx - 9]
002D6E62  dec      al
002D6E64  mov      byte ptr [rbx - 0xa], al
002D6E67  movsx    eax, al
002D6E6A  shl      eax, 7
002D6E6D  cdq      
002D6E6E  idiv     ecx
002D6E70  test     byte ptr [rbx], 2
002D6E73  mov      byte ptr [rbx - 0xb], al
002D6E76  jne      0x2d6eb4  ; -> 002D6EB4
002D6E78  mov      ecx, 0x80
002D6E7D  sub      cl, al
002D6E7F  mov      byte ptr [rbx - 0xb], cl
002D6E82  jmp      0x2d6eb4  ; -> 002D6EB4
002D6E84  mov      eax, dword ptr [rbx]
002D6E86  mov      ecx, eax
002D6E88  not      ecx
002D6E8A  xor      ecx, eax
002D6E8C  and      ecx, 2
002D6E8F  xor      ecx, eax
002D6E91  mov      dword ptr [rbx], ecx
002D6E93  test     cl, 2
002D6E96  jne      0x2d6ea5  ; -> 002D6EA5
002D6E98  and      ecx, 0xfffffffe
002D6E9B  mov      word ptr [rbx - 0xc], 0
002D6EA1  mov      dword ptr [rbx], ecx
002D6EA3  jmp      0x2d6eb4  ; -> 002D6EB4
002D6EA5  mov      eax, dword ptr [rip + 0x1db86c5]  ; -> 0208F570
002D6EAB  mov      dword ptr [rbx - 8], eax
002D6EAE  mov      word ptr [rbx - 0xc], 0x8002
002D6EB4  add      rbx, 0x18
002D6EB8  sub      rsi, 1
002D6EBC  jne      0x2d6e00  ; -> 002D6E00
002D6EC2  mov      rdi, qword ptr [rsp + 0x30]
002D6EC7  mov      rbx, qword ptr [rsp + 0x38]
002D6ECC  add      rsp, 0x20
002D6ED0  pop      rsi
002D6ED1  ret      
```

## 003FACF0 (531 B, extent 003FACF0-003FAF03)

Documented callee on this page: `0035D480`

```
003FACF0  push     rbx
003FACF2  push     rsi
003FACF3  push     rdi
003FACF4  sub      rsp, 0x20
003FACF8  mov      rbx, rcx
003FACFB  mov      ecx, dword ptr [rdx]
003FACFD  sub      ecx, 1
003FAD00  je       0x3fae7e  ; -> 003FAE7E
003FAD06  sub      ecx, 1
003FAD09  je       0x3fae41  ; -> 003FAE41
003FAD0F  sub      ecx, 1
003FAD12  je       0x3fad59  ; -> 003FAD59
003FAD14  sub      ecx, 0xb
003FAD17  je       0x3fad45  ; -> 003FAD45
003FAD19  cmp      ecx, 1
003FAD1C  je       0x3fad2d  ; -> 003FAD2D
003FAD1E  mov      rcx, rbx
003FAD21  add      rsp, 0x20
003FAD25  pop      rdi
003FAD26  pop      rsi
003FAD27  pop      rbx
003FAD28  jmp      0x5c5230  ; -> 005C5230 fn
003FAD2D  mov      r8d, 1
003FAD33  xor      eax, eax
003FAD35  mov      word ptr [rbx + 0xc2], r8w
003FAD3D  add      rsp, 0x20
003FAD41  pop      rdi
003FAD42  pop      rsi
003FAD43  pop      rbx
003FAD44  ret      
003FAD45  mov      ecx, 0x6c
003FAD4A  call     0x249c60  ; -> 00249C60 fn
003FAD4F  xor      eax, eax
003FAD51  add      rsp, 0x20
003FAD55  pop      rdi
003FAD56  pop      rsi
003FAD57  pop      rbx
003FAD58  ret      
003FAD59  call     0x35d480  ; -> 0035D480 fn
003FAD5E  test     rax, rax
003FAD61  je       0x3faef9  ; -> 003FAEF9
003FAD67  mov      rsi, qword ptr [rbx + 0x38]
003FAD6B  movsx    edi, word ptr [rsi + 0x58]
003FAD6F  call     0x35d460  ; -> 0035D460 fn
003FAD74  mov      r8d, 0xfff
003FAD7A  mov      rcx, qword ptr [rax + 0x20]
003FAD7E  movzx    eax, word ptr [rcx + 0x62]
003FAD82  add      rcx, 0x30
003FAD86  movzx    edx, word ptr [rcx + rax*2 + 0x14]
003FAD8B  movzx    eax, word ptr [rcx + 0x10]
003FAD8F  add      rcx, rax
003FAD92  movzx    eax, word ptr [rcx + rdx*8]
003FAD96  mov      word ptr [rsp + 0x48], ax
003FAD9B  movzx    eax, word ptr [rcx + rdx*8 + 2]
003FADA0  mov      word ptr [rsp + 0x4a], ax
003FADA5  movzx    eax, word ptr [rcx + rdx*8 + 4]
003FADAA  and      ax, r8w
003FADAE  mov      word ptr [rsp + 0x4c], ax
003FADB3  mov      eax, dword ptr [rcx + rdx*8 + 4]
003FADB7  shr      eax, 0xc
003FADBA  and      ax, r8w
003FADBE  mov      word ptr [rsp + 0x4e], ax
003FADC3  xor      eax, eax
003FADC5  mov      dword ptr [rsp + 0x40], eax
003FADC9  movzx    eax, word ptr [rbx + 0x9c]
003FADD0  mov      word ptr [rsp + 0x44], ax
003FADD5  movzx    eax, word ptr [rbx + 0x9e]
003FADDC  mov      word ptr [rsp + 0x46], ax
003FADE1  movzx    ebx, byte ptr [rcx + rdx*8 + 7]
003FADE6  call     0x35d460  ; -> 0035D460 fn
003FADEB  mov      r8, qword ptr [rax + 0x20]
003FADEF  mov      eax, ebx
003FADF1  shr      eax, 4
003FADF4  add      r8, 0x30
003FADF8  movzx    eax, al
003FADFB  and      bl, 0xf
003FADFE  add      rax, r8
003FAE01  movzx    edx, word ptr [r8 + 0x12]
003FAE06  movzx    eax, byte ptr [rdx + rax]
003FAE0A  add      al, bl
003FAE0C  mov      byte ptr [rsi + 0x5c], al
003FAE0F  imul     eax, edi, 0x64
003FAE12  sar      eax, 7
003FAE15  mov      word ptr [rsi + 0x58], ax
003FAE19  call     0x35d460  ; -> 0035D460 fn
003FAE1E  mov      rdx, rax
003FAE21  lea      r9, [rsp + 0x40]
003FAE26  lea      r8, [rsp + 0x48]
003FAE2B  mov      rcx, rsi
003FAE2E  call     0x2d8c80  ; -> 002D8C80 fn
003FAE33  xor      eax, eax
003FAE35  mov      word ptr [rsi + 0x58], di
003FAE39  add      rsp, 0x20
003FAE3D  pop      rdi
003FAE3E  pop      rsi
003FAE3F  pop      rbx
003FAE40  ret      
003FAE41  cmp      word ptr [rbx + 0xc2], 0
003FAE49  jne      0x3faef9  ; -> 003FAEF9
003FAE4F  inc      word ptr [rbx + 0xc0]
003FAE56  imul     eax, dword ptr [rip + 0x1a03257], 0x1e  ; -> 01DFE0B4 [u32 0x00000001]
003FAE5D  movzx    ecx, word ptr [rbx + 0xc0]
003FAE64  cmp      ecx, eax
003FAE66  jb       0x3faef9  ; -> 003FAEF9
003FAE6C  mov      rcx, rbx
003FAE6F  call     0x244f00  ; -> 00244F00 fn
003FAE74  xor      eax, eax
003FAE76  add      rsp, 0x20
003FAE7A  pop      rdi
003FAE7B  pop      rsi
003FAE7C  pop      rbx
003FAE7D  ret      
003FAE7E  mov      qword ptr [rsp + 0x50], rbp
003FAE83  call     0x35d3f0  ; -> 0035D3F0 fn
003FAE88  lea      rcx, [rbx + 0x50]
003FAE8C  mov      r9, rbx
003FAE8F  mov      r8d, 1
003FAE95  mov      rdx, rax
003FAE98  call     0x2432b0  ; -> 002432B0 fn
003FAE9D  mov      rdi, rax
003FAEA0  movzx    esi, word ptr [rax + 0xa]
003FAEA4  movzx    ebp, word ptr [rax + 8]
003FAEA8  call     0x28f810  ; -> 0028F810 fn
003FAEAD  movzx    ecx, word ptr [rdi + 0xa]
003FAEB1  sub      eax, ecx
003FAEB3  test     rbx, rbx
003FAEB6  je       0x3faed8  ; -> 003FAED8
003FAEB8  movzx    ecx, word ptr [rdi + 4]
003FAEBC  mov      word ptr [rbx + 0x98], cx
003FAEC3  mov      word ptr [rbx + 0x9a], ax
003FAECA  mov      word ptr [rbx + 0x9c], bp
003FAED1  mov      word ptr [rbx + 0x9e], si
003FAED8  lea      rdx, [rip + 0x9170e9]  ; -> 00D11FC8
003FAEDF  mov      rcx, rbx
003FAEE2  call     0x247570  ; -> 00247570 fn
003FAEE7  mov      edx, 0x59
003FAEEC  mov      rcx, rbx
003FAEEF  call     0x247930  ; -> 00247930 fn
003FAEF4  mov      rbp, qword ptr [rsp + 0x50]
003FAEF9  xor      eax, eax
003FAEFB  add      rsp, 0x20
003FAEFF  pop      rdi
003FAF00  pop      rsi
003FAF01  pop      rbx
003FAF02  ret      
```

## 00568BB0 (1059 B, extent 00568BB0-00568FD3)

Documented callee on this page: `002CC8D0`

```
00568BB0  mov      qword ptr [rsp + 0x10], rbx
00568BB5  mov      qword ptr [rsp + 0x18], rbp
00568BBA  push     rsi
00568BBB  push     rdi
00568BBC  push     r14
00568BBE  sub      rsp, 0x20
00568BC2  mov      rax, qword ptr [rdx + 0x10]
00568BC6  mov      r14, rdx
00568BC9  movsxd   rbp, r9d
00568BCC  mov      rdi, rcx
00568BCF  mov      r8, qword ptr [rax + 0x48]
00568BD3  lea      rsi, [rbp + 0xb]
00568BD7  shl      rsi, 5
00568BDB  add      rsi, rcx
00568BDE  and      dword ptr [r8 + 8], 0xfffffffe
00568BE3  test     r9d, r9d
00568BE6  jne      0x568cfb  ; -> 00568CFB
00568BEC  xor      edx, edx
00568BEE  mov      rcx, r14
00568BF1  call     0x243580  ; -> 00243580 fn
00568BF6  mov      rax, qword ptr [r14 + 0x10]
00568BFA  mov      r8, qword ptr [rax + 0x40]
00568BFE  or       dword ptr [r8 + 8], 1
00568C03  movzx    edx, byte ptr [rsi + 0x14]
00568C07  mov      rax, qword ptr [r8 + 0x20]
00568C0B  movzx    ecx, byte ptr [rax + rdx*8 + 7]
00568C10  mov      rax, qword ptr [r8]
00568C13  mov      byte ptr [r8 + 0x39], cl
00568C17  mov      word ptr [r8 + 0xa], dx
00568C1C  mov      ecx, dword ptr [rax + 0x14]
00568C1F  movzx    eax, byte ptr [rdi + 0x343]
00568C26  mov      dword ptr [rsp + 0x58], ecx
00568C2A  xor      ecx, ecx
00568C2C  mov      byte ptr [rsp + 0x5b], al
00568C30  mov      eax, dword ptr [rsp + 0x58]
00568C34  mov      dword ptr [r8 + 0x34], eax
00568C38  mov      dword ptr [r8 + 0x30], eax
00568C3C  mov      dword ptr [r8 + 0x2c], eax
00568C40  mov      dword ptr [r8 + 0x28], eax
00568C44  mov      rax, qword ptr [r14 + 0x10]
00568C48  mov      rbx, qword ptr [rax + 0x38]
00568C4C  or       dword ptr [rbx + 8], 1
00568C50  mov      rax, qword ptr [rsi]
00568C53  mov      qword ptr [rbx + 0x18], rax
00568C57  call     0x20e620  ; -> 0020E620 fn
00568C5C  mov      dword ptr [rbx + 0x20], eax
00568C5F  mov      rax, qword ptr [rbx]
00568C62  mov      ecx, dword ptr [rax + 0xc]
00568C65  movzx    eax, byte ptr [rdi + 0x343]
00568C6C  mov      dword ptr [rsp + 0x58], ecx
00568C70  mov      byte ptr [rsp + 0x5b], al
00568C74  mov      eax, dword ptr [rsp + 0x58]
00568C78  mov      dword ptr [rbx + 0x24], eax
00568C7B  mov      rax, qword ptr [r14 + 0x10]
00568C7F  mov      rdx, qword ptr [rax + 0x48]
00568C83  or       dword ptr [rdx + 8], 1
00568C87  cmp      byte ptr [rdi + 0x353], 0
00568C8E  je       0x568ce4  ; -> 00568CE4
00568C90  cmp      word ptr [rdi + 0x350], 0
00568C98  mov      rax, qword ptr [rdx]
00568C9B  mov      ecx, dword ptr [rax + 0x14]
00568C9E  mov      dword ptr [rsp + 0x58], ecx
00568CA2  je       0x568cc4  ; -> 00568CC4
00568CA4  movzx    eax, byte ptr [rdi + 0x343]
00568CAB  mov      byte ptr [rsp + 0x5b], al
00568CAF  mov      eax, dword ptr [rsp + 0x58]
00568CB3  mov      dword ptr [rdx + 0x34], eax
00568CB6  mov      dword ptr [rdx + 0x30], eax
00568CB9  mov      dword ptr [rdx + 0x2c], eax
00568CBC  mov      dword ptr [rdx + 0x28], eax
00568CBF  jmp      0x568fbb  ; -> 00568FBB
00568CC4  movzx    eax, byte ptr [rdi + 0x350]
00568CCB  mov      byte ptr [rsp + 0x5b], al
00568CCF  mov      eax, dword ptr [rsp + 0x58]
00568CD3  mov      dword ptr [rdx + 0x34], eax
00568CD6  mov      dword ptr [rdx + 0x30], eax
00568CD9  mov      dword ptr [rdx + 0x2c], eax
00568CDC  mov      dword ptr [rdx + 0x28], eax
00568CDF  jmp      0x568fbb  ; -> 00568FBB
00568CE4  mov      eax, dword ptr [rdi + 0x354]
00568CEA  mov      dword ptr [rdx + 0x34], eax
00568CED  mov      dword ptr [rdx + 0x30], eax
00568CF0  mov      dword ptr [rdx + 0x2c], eax
00568CF3  mov      dword ptr [rdx + 0x28], eax
00568CF6  jmp      0x568fbb  ; -> 00568FBB
00568CFB  movzx    ecx, byte ptr [rsi + 0x15]
00568CFF  add      ecx, 0x77
00568D02  mov      qword ptr [rsp + 0x40], r15
00568D07  call     0x2dd7e0  ; -> 002DD7E0 fn
00568D0C  cmp      byte ptr [rsi + 0x14], 0
00568D10  mov      dword ptr [rsp + 0x58], eax
00568D14  jne      0x568d24  ; -> 00568D24
00568D16  mov      ecx, 0x79
00568D1B  call     0x2dd7e0  ; -> 002DD7E0 fn
00568D20  mov      dword ptr [rsp + 0x58], eax
00568D24  movsxd   rcx, dword ptr [rdi + 0x35c]
00568D2B  lea      r15, [rip + 0x27409ae]  ; -> 02CA96E0
00568D32  mov      rdx, qword ptr [r15 + rcx*8]
00568D36  test     byte ptr [rdx + 0x340], 1
00568D3D  jne      0x568da6  ; -> 00568DA6
00568D3F  cmp      byte ptr [rdx + 0x33e], 0
00568D46  jne      0x568da6  ; -> 00568DA6
00568D48  mov      rdx, qword ptr [rdi + 0xd8]
00568D4F  movsx    ecx, word ptr [rdx + 0xf2]
00568D56  movsx    r8d, word ptr [rdx + 0xf4]
00568D5E  add      r8d, ecx
00568D61  movzx    ecx, byte ptr [rdx + 0xec]
00568D68  imul     r8d, ecx
00568D6C  movsx    ecx, byte ptr [rdx + 0xee]
00568D73  add      r8d, ecx
00568D76  movsx    ecx, byte ptr [rdx + 0xed]
00568D7D  add      r8d, ecx
00568D80  cmp      r8d, ebp
00568D83  jne      0x568da6  ; -> 00568DA6
00568D85  mov      r8d, dword ptr [rdi + 0x344]
00568D8C  mov      r9d, 4
00568D92  lea      edx, [r9 + 0x1c]
00568D96  lea      ecx, [rdx + 0x40]
00568D99  call     0x2cc8d0  ; -> 002CC8D0 fn
00568D9E  mov      byte ptr [rsp + 0x5b], al
00568DA2  mov      eax, dword ptr [rsp + 0x58]
00568DA6  mov      rcx, qword ptr [r14 + 0x10]
00568DAA  mov      rdx, qword ptr [rcx]
00568DAD  mov      dword ptr [rdx + 0x34], eax
00568DB0  mov      dword ptr [rdx + 0x30], eax
00568DB3  mov      dword ptr [rdx + 0x2c], eax
00568DB6  mov      dword ptr [rdx + 0x28], eax
00568DB9  mov      rcx, qword ptr [r14 + 0x10]
00568DBD  mov      rdx, qword ptr [rcx + 8]
00568DC1  mov      dword ptr [rdx + 0x34], eax
00568DC4  mov      dword ptr [rdx + 0x30], eax
00568DC7  mov      dword ptr [rdx + 0x2c], eax
00568DCA  mov      dword ptr [rdx + 0x28], eax
00568DCD  mov      rcx, qword ptr [r14 + 0x10]
00568DD1  mov      rdx, qword ptr [rcx + 0x10]
00568DD5  mov      dword ptr [rdx + 0x34], eax
00568DD8  mov      dword ptr [rdx + 0x30], eax
00568DDB  mov      dword ptr [rdx + 0x2c], eax
00568DDE  mov      dword ptr [rdx + 0x28], eax
00568DE1  mov      rax, qword ptr [r14 + 0x10]
00568DE5  movzx    edx, byte ptr [rsi + 0x14]
00568DE9  mov      r8, qword ptr [rax + 0x18]
00568DED  mov      rax, qword ptr [r8 + 0x20]
00568DF1  movzx    ecx, byte ptr [rax + rdx*8 + 7]
00568DF6  mov      byte ptr [r8 + 0x39], cl
00568DFA  xor      ecx, ecx
00568DFC  mov      word ptr [r8 + 0xa], dx
00568E01  mov      rax, qword ptr [r14 + 0x10]
00568E05  mov      rbx, qword ptr [rax + 0x20]
00568E09  mov      rax, qword ptr [rsi]
00568E0C  mov      qword ptr [rbx + 0x18], rax
00568E10  call     0x20e620  ; -> 0020E620 fn
00568E15  mov      rcx, qword ptr [rbx]
00568E18  mov      dword ptr [rbx + 0x20], eax
00568E1B  movzx    eax, word ptr [rcx + 4]
00568E1F  mov      word ptr [rbx + 0xc], ax
00568E23  movzx    eax, word ptr [rcx + 6]
00568E27  mov      word ptr [rbx + 0xe], ax
00568E2B  cmp      byte ptr [rsi + 0x14], 0
00568E2F  je       0x568e3c  ; -> 00568E3C
00568E31  cmp      byte ptr [rsi + 0x15], 2
00568E35  je       0x568e3c  ; -> 00568E3C
00568E37  mov      eax, dword ptr [rcx + 0xc]
00568E3A  jmp      0x568e46  ; -> 00568E46
00568E3C  mov      ecx, 2
00568E41  call     0x2dd7e0  ; -> 002DD7E0 fn
00568E46  movsxd   rcx, dword ptr [rdi + 0x35c]
00568E4D  mov      dword ptr [rsp + 0x58], eax
00568E51  mov      rdx, qword ptr [r15 + rcx*8]
00568E55  test     byte ptr [rdx + 0x340], 1
00568E5C  jne      0x568ec5  ; -> 00568EC5
00568E5E  cmp      byte ptr [rdx + 0x33e], 1
00568E65  jne      0x568ec5  ; -> 00568EC5
00568E67  mov      rdx, qword ptr [rdi + 0xd8]
00568E6E  movsx    ecx, word ptr [rdx + 0xf2]
00568E75  movsx    r8d, word ptr [rdx + 0xf4]
00568E7D  add      r8d, ecx
00568E80  movzx    ecx, byte ptr [rdx + 0xec]
00568E87  imul     r8d, ecx
00568E8B  movsx    ecx, byte ptr [rdx + 0xee]
00568E92  add      r8d, ecx
00568E95  movsx    ecx, byte ptr [rdx + 0xed]
00568E9C  add      r8d, ecx
00568E9F  cmp      r8d, ebp
00568EA2  jne      0x568ec5  ; -> 00568EC5
00568EA4  mov      r8d, dword ptr [rdi + 0x344]
00568EAB  mov      r9d, 4
00568EB1  lea      edx, [r9 + 0x1c]
00568EB5  lea      ecx, [rdx + 0x60]
00568EB8  call     0x2cc8d0  ; -> 002CC8D0 fn
00568EBD  mov      byte ptr [rsp + 0x5b], al
00568EC1  mov      eax, dword ptr [rsp + 0x58]
00568EC5  cmp      byte ptr [rsi + 0x17], 1
00568EC9  jne      0x568ed5  ; -> 00568ED5
00568ECB  mov      ecx, 6
00568ED0  call     0x2dd7e0  ; -> 002DD7E0 fn
00568ED5  mov      dword ptr [rbx + 0x24], eax
00568ED8  xor      ecx, ecx
00568EDA  mov      rax, qword ptr [r14 + 0x10]
00568EDE  mov      rbx, qword ptr [rax + 0x28]
00568EE2  mov      rax, qword ptr [rsi + 8]
00568EE6  mov      qword ptr [rbx + 0x18], rax
00568EEA  call     0x20e620  ; -> 0020E620 fn
00568EEF  mov      rcx, qword ptr [rbx]
00568EF2  mov      dword ptr [rbx + 0x20], eax
00568EF5  movzx    eax, word ptr [rcx + 4]
00568EF9  mov      word ptr [rbx + 0xc], ax
00568EFD  movzx    eax, word ptr [rcx + 6]
00568F01  mov      word ptr [rbx + 0xe], ax
00568F05  cmp      byte ptr [rsi + 0x14], 0
00568F09  je       0x568f16  ; -> 00568F16
00568F0B  cmp      byte ptr [rsi + 0x15], 2
00568F0F  je       0x568f16  ; -> 00568F16
00568F11  mov      eax, dword ptr [rcx + 0xc]
00568F14  jmp      0x568f20  ; -> 00568F20
00568F16  mov      ecx, 2
00568F1B  call     0x2dd7e0  ; -> 002DD7E0 fn
00568F20  movsxd   rcx, dword ptr [rdi + 0x35c]
00568F27  mov      dword ptr [rsp + 0x58], eax
00568F2B  mov      rdx, qword ptr [r15 + rcx*8]
00568F2F  mov      r15, qword ptr [rsp + 0x40]
00568F34  test     byte ptr [rdx + 0x340], 1
00568F3B  jne      0x568fa8  ; -> 00568FA8
00568F3D  cmp      byte ptr [rdx + 0x33e], 2
00568F44  jne      0x568fa8  ; -> 00568FA8
00568F46  mov      r10, qword ptr [rdi + 0xd8]
00568F4D  movzx    r8d, byte ptr [r10 + 0xec]
00568F55  movsx    r11d, word ptr [r10 + 0xf4]
00568F5D  movsx    ecx, word ptr [r10 + 0xf2]
00568F65  add      r11d, ecx
00568F68  imul     r11d, r8d
00568F6C  movsx    r8d, byte ptr [r10 + 0xee]
00568F74  add      r11d, r8d
00568F77  movsx    r8d, byte ptr [r10 + 0xed]
00568F7F  add      r11d, r8d
00568F82  cmp      r11d, ebp
00568F85  jne      0x568fa8  ; -> 00568FA8
00568F87  mov      r8d, dword ptr [rdi + 0x344]
00568F8E  mov      r9d, 4
00568F94  lea      edx, [r9 + 0x1c]
00568F98  lea      ecx, [rdx + 0x60]
00568F9B  call     0x2cc8d0  ; -> 002CC8D0 fn
00568FA0  mov      byte ptr [rsp + 0x5b], al
00568FA4  mov      eax, dword ptr [rsp + 0x58]
00568FA8  cmp      byte ptr [rsi + 0x17], 2
00568FAC  jne      0x568fb8  ; -> 00568FB8
00568FAE  mov      ecx, 6
00568FB3  call     0x2dd7e0  ; -> 002DD7E0 fn
00568FB8  mov      dword ptr [rbx + 0x24], eax
00568FBB  mov      rbx, qword ptr [rsp + 0x48]
00568FC0  mov      eax, 1
00568FC5  mov      rbp, qword ptr [rsp + 0x50]
00568FCA  add      rsp, 0x20
00568FCE  pop      r14
00568FD0  pop      rdi
00568FD1  pop      rsi
00568FD2  ret      
```
