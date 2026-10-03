# F homing pack (FABLE): `17-Presentation-Rendering/Character-Rendering/how-a-character-is-lit.md`

Generated 2026-10-03 04:18 by FABLE (callee_pack.py, host choice by OPUS's homing_pack) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 004FDDA0 (1221 B, extent 004FDDA0-004FE265)

Documented callee on this page: `00504450`

```
004FDDA0  mov      qword ptr [rsp + 8], rbx
004FDDA5  mov      qword ptr [rsp + 0x18], rbp
004FDDAA  push     rsi
004FDDAB  push     rdi
004FDDAC  push     r14
004FDDAE  sub      rsp, 0x20
004FDDB2  movaps   xmm0, xmmword ptr [rip + 0x25f00b7]  ; -> 02AEDE70
004FDDB9  mov      ebx, 0x1000
004FDDBE  movaps   xmm1, xmmword ptr [rip + 0x25f00bb]  ; -> 02AEDE80
004FDDC5  mov      edi, ebx
004FDDC7  mov      rsi, qword ptr [rip + 0x1ddb0de]  ; -> 022D8EAC
004FDDCE  mov      rbp, qword ptr [rip + 0x1ddb0df]  ; -> 022D8EB4
004FDDD5  sub      edi, esi
004FDDD7  movaps   xmmword ptr [rip + 0x27aa1a2], xmm0  ; -> 02CA7F80
004FDDDE  sub      ebx, ebp
004FDDE0  movaps   xmm0, xmmword ptr [rip + 0x25f00a9]  ; -> 02AEDE90
004FDDE7  movaps   xmmword ptr [rip + 0x27aa1a2], xmm1  ; -> 02CA7F90
004FDDEE  movaps   xmm1, xmmword ptr [rip + 0x25f00ab]  ; -> 02AEDEA0
004FDDF5  movaps   xmmword ptr [rip + 0x27aa1a4], xmm0  ; -> 02CA7FA0
004FDDFC  movaps   xmm0, xmmword ptr [rip + 0x25eff2d]  ; -> 02AEDD30
004FDE03  movaps   xmmword ptr [rip + 0x27aa1a6], xmm1  ; -> 02CA7FB0
004FDE0A  movaps   xmm1, xmmword ptr [rip + 0x25eff2f]  ; -> 02AEDD40
004FDE11  movaps   xmmword ptr [rip + 0x27aa1a8], xmm0  ; -> 02CA7FC0
004FDE18  movaps   xmm0, xmmword ptr [rip + 0x25eff31]  ; -> 02AEDD50
004FDE1F  movaps   xmmword ptr [rip + 0x27aa1aa], xmm1  ; -> 02CA7FD0
004FDE26  movaps   xmm1, xmmword ptr [rip + 0x25eff33]  ; -> 02AEDD60
004FDE2D  movaps   xmmword ptr [rip + 0x27aa1ac], xmm0  ; -> 02CA7FE0
004FDE34  movaps   xmmword ptr [rip + 0x27aa1b5], xmm1  ; -> 02CA7FF0
004FDE3B  shl      edi, 3
004FDE3E  shl      ebx, 3
004FDE41  call     0x5044b0  ; -> 005044B0 fn
004FDE46  mov      qword ptr [rsp + 0x48], rax
004FDE4B  mov      r10d, dword ptr [rax + 0x10]
004FDE4F  mov      rcx, qword ptr [rax + 8]
004FDE53  shl      r10, 4
004FDE57  add      rcx, 0x20
004FDE5B  add      r10, qword ptr [rax]
004FDE5E  cmp      rcx, r10
004FDE61  jb       0x4fde82  ; -> 004FDE82
004FDE63  lea      rcx, [rsp + 0x48]
004FDE68  call     0x504450  ; -> 00504450 fn
004FDE6D  call     0x5044b0  ; -> 005044B0 fn
004FDE72  mov      qword ptr [rsp + 0x48], rax
004FDE77  mov      r10d, dword ptr [rax + 0x10]
004FDE7B  shl      r10, 4
004FDE7F  add      r10, qword ptr [rax]
004FDE82  mov      rcx, qword ptr [rax + 8]
004FDE86  mov      rax, qword ptr [rip + 0x29bc577]  ; -> 02EBA404
004FDE8D  mov      qword ptr [rcx], rax
004FDE90  mov      rax, qword ptr [rsp + 0x48]
004FDE95  mov      rcx, qword ptr [rax + 8]
004FDE99  mov      dword ptr [rcx + 8], 0x20000000
004FDEA0  mov      rax, qword ptr [rsp + 0x48]
004FDEA5  mov      rcx, qword ptr [rax + 8]
004FDEA9  mov      dword ptr [rcx + 0xc], 0x3f
004FDEB0  mov      rax, qword ptr [rsp + 0x48]
004FDEB5  add      qword ptr [rax + 8], 0x10
004FDEBA  mov      rcx, qword ptr [rsp + 0x48]
004FDEBF  mov      rax, qword ptr [rcx + 8]
004FDEC3  add      rax, 0x150
004FDEC9  cmp      rax, r10
004FDECC  jb       0x4fdef0  ; -> 004FDEF0
004FDECE  lea      rcx, [rsp + 0x48]
004FDED3  call     0x504450  ; -> 00504450 fn
004FDED8  call     0x5044b0  ; -> 005044B0 fn
004FDEDD  mov      qword ptr [rsp + 0x48], rax
004FDEE2  mov      rcx, rax
004FDEE5  mov      r10d, dword ptr [rax + 0x10]
004FDEE9  shl      r10, 4
004FDEED  add      r10, qword ptr [rax]
004FDEF0  mov      rax, qword ptr [rcx + 8]
004FDEF4  xor      r14d, r14d
004FDEF7  movabs   rcx, 0x1000000000008013
004FDF01  movsxd   r8, ebx
004FDF04  shl      r8, 0x20
004FDF08  mov      qword ptr [rax], 0x10000014
004FDF0F  lea      r9, [rax + 0xb0]
004FDF16  mov      dword ptr [rax + 8], r14d
004FDF1A  mov      dword ptr [rax + 0xc], 0x50000014
004FDF21  mov      qword ptr [rax + 0x10], rcx
004FDF25  mov      qword ptr [rax + 0x18], 0xe
004FDF2D  mov      qword ptr [rax + 0x20], 1
004FDF35  mov      qword ptr [rax + 0x28], 0x46
004FDF3D  mov      qword ptr [rax + 0x30], r14
004FDF41  mov      qword ptr [rax + 0x38], 0x45
004FDF49  mov      qword ptr [rax + 0x40], r14
004FDF4D  mov      qword ptr [rax + 0x48], 0x49
004FDF55  mov      qword ptr [rax + 0x50], 1
004FDF5D  mov      qword ptr [rax + 0x58], 0x1a
004FDF65  mov      qword ptr [rax + 0x60], r14
004FDF69  mov      qword ptr [rax + 0x68], 0x22
004FDF71  mov      qword ptr [rax + 0x70], r14
004FDF75  mov      qword ptr [rax + 0x78], 0x22
004FDF7D  mov      qword ptr [rax + 0x80], 0x60
004FDF88  mov      qword ptr [rax + 0x88], 0x14
004FDF93  mov      qword ptr [rax + 0x90], 0x60
004FDF9E  mov      qword ptr [rax + 0x98], 0x15
004FDFA9  mov      qword ptr [rax + 0xa0], r14
004FDFB0  mov      qword ptr [rax + 0xa8], 0x16
004FDFBB  mov      qword ptr [r9], r14
004FDFBE  mov      qword ptr [rax + 0xb8], 0x17
004FDFC9  mov      qword ptr [r9 + 0x10], 0x8080
004FDFD1  mov      qword ptr [r9 + 0x18], 0x3b
004FDFD9  mov      rax, qword ptr [rip + 0x1ddaee8]  ; -> 022D8EC8
004FDFE0  mov      qword ptr [r9 + 0x20], rax
004FDFE4  mov      qword ptr [r9 + 0x28], 0x4c
004FDFEC  mov      rax, qword ptr [rip + 0x1ddaedd]  ; -> 022D8ED0
004FDFF3  mov      qword ptr [r9 + 0x30], rax
004FDFF7  mov      qword ptr [r9 + 0x38], 0x4e
004FDFFF  mov      qword ptr [r9 + 0x48], 0x18
004FE007  movsxd   rax, edi
004FE00A  or       r8, rax
004FE00D  lea      eax, [rbp - 1]
004FE010  mov      qword ptr [r9 + 0x40], r8
004FE014  mov      qword ptr [r9 + 0x58], 0x40
004FE01C  movsxd   rdx, eax
004FE01F  lea      eax, [rsi - 1]
004FE022  movsxd   rcx, eax
004FE025  shl      rdx, 0x20
004FE029  or       rdx, rcx
004FE02C  lea      rcx, [r9 + 0xa0]
004FE033  shl      rdx, 0x10
004FE037  mov      qword ptr [r9 + 0x50], rdx
004FE03B  mov      rax, qword ptr [rip + 0x1ddae86]  ; -> 022D8EC8
004FE042  mov      qword ptr [r9 + 0x60], rax
004FE046  mov      qword ptr [r9 + 0x68], 0x4d
004FE04E  mov      rax, qword ptr [rip + 0x1ddae7b]  ; -> 022D8ED0
004FE055  mov      qword ptr [r9 + 0x70], rax
004FE059  mov      qword ptr [r9 + 0x78], 0x4f
004FE061  mov      qword ptr [r9 + 0x80], r8
004FE068  mov      qword ptr [r9 + 0x88], 0x19
004FE073  mov      qword ptr [r9 + 0x90], rdx
004FE07A  mov      qword ptr [r9 + 0x98], 0x41
004FE085  mov      rax, qword ptr [rsp + 0x48]
004FE08A  mov      qword ptr [rax + 8], rcx
004FE08E  mov      rcx, qword ptr [rsp + 0x48]
004FE093  mov      rax, qword ptr [rcx + 8]
004FE097  add      rax, 0x170
004FE09D  cmp      rax, r10
004FE0A0  jb       0x4fe0b9  ; -> 004FE0B9
004FE0A2  lea      rcx, [rsp + 0x48]
004FE0A7  call     0x504450  ; -> 00504450 fn
004FE0AC  call     0x5044b0  ; -> 005044B0 fn
004FE0B1  mov      rcx, rax
004FE0B4  mov      qword ptr [rsp + 0x48], rax
004FE0B9  mov      rax, qword ptr [rcx + 8]
004FE0BD  mov      edx, 2
004FE0C2  mov      qword ptr [rax], 0x10000015
004FE0C9  mov      rax, qword ptr [rsp + 0x48]
004FE0CE  mov      rcx, qword ptr [rax + 8]
004FE0D2  mov      dword ptr [rcx + 8], r14d
004FE0D6  mov      rax, qword ptr [rsp + 0x48]
004FE0DB  mov      rcx, qword ptr [rax + 8]
004FE0DF  mov      dword ptr [rcx + 0xc], r14d
004FE0E3  mov      rax, qword ptr [rsp + 0x48]
004FE0E8  add      qword ptr [rax + 8], 0x10
004FE0ED  mov      rax, qword ptr [rsp + 0x48]
004FE0F2  mov      rcx, qword ptr [rax + 8]
004FE0F6  lea      rax, [rip + 0x29bc303]  ; -> 02EBA400
004FE0FD  nop      dword ptr [rax]
004FE100  lea      rcx, [rcx + 0x80]
004FE107  movups   xmm0, xmmword ptr [rax]
004FE10A  lea      rax, [rax + 0x80]
004FE111  movups   xmmword ptr [rcx - 0x80], xmm0
004FE115  movups   xmm1, xmmword ptr [rax - 0x70]
004FE119  movups   xmmword ptr [rcx - 0x70], xmm1
004FE11D  movups   xmm0, xmmword ptr [rax - 0x60]
004FE121  movups   xmmword ptr [rcx - 0x60], xmm0
004FE125  movups   xmm1, xmmword ptr [rax - 0x50]
004FE129  movups   xmmword ptr [rcx - 0x50], xmm1
004FE12D  movups   xmm0, xmmword ptr [rax - 0x40]
004FE131  movups   xmmword ptr [rcx - 0x40], xmm0
004FE135  movups   xmm1, xmmword ptr [rax - 0x30]
004FE139  movups   xmmword ptr [rcx - 0x30], xmm1
004FE13D  movups   xmm0, xmmword ptr [rax - 0x20]
004FE141  movups   xmmword ptr [rcx - 0x20], xmm0
004FE145  movups   xmm1, xmmword ptr [rax - 0x10]
004FE149  movups   xmmword ptr [rcx - 0x10], xmm1
004FE14D  sub      rdx, 1
004FE151  jne      0x4fe100  ; -> 004FE100
004FE153  movups   xmm0, xmmword ptr [rax]
004FE156  movups   xmmword ptr [rcx], xmm0
004FE159  movups   xmm1, xmmword ptr [rax + 0x10]
004FE15D  movups   xmmword ptr [rcx + 0x10], xmm1
004FE161  movups   xmm0, xmmword ptr [rax + 0x20]
004FE165  movups   xmmword ptr [rcx + 0x20], xmm0
004FE169  movups   xmm1, xmmword ptr [rax + 0x30]
004FE16D  movups   xmmword ptr [rcx + 0x30], xmm1
004FE171  movups   xmm0, xmmword ptr [rax + 0x40]
004FE175  movups   xmmword ptr [rcx + 0x40], xmm0
004FE179  mov      rcx, qword ptr [rsp + 0x48]
004FE17E  mov      rdx, qword ptr [rcx + 8]
004FE182  lea      rax, [rdx + 0x150]
004FE189  mov      qword ptr [rcx + 8], rax
004FE18D  lea      rcx, [rsp + 0x48]
004FE192  movaps   xmm0, xmmword ptr [rip + 0x27a9de7]  ; -> 02CA7F80
004FE199  movups   xmmword ptr [rdx + 0x50], xmm0
004FE19D  movaps   xmm1, xmmword ptr [rip + 0x27a9dec]  ; -> 02CA7F90
004FE1A4  movups   xmmword ptr [rdx + 0x60], xmm1
004FE1A8  movaps   xmm0, xmmword ptr [rip + 0x27a9df1]  ; -> 02CA7FA0
004FE1AF  movups   xmmword ptr [rdx + 0x70], xmm0
004FE1B3  movaps   xmm1, xmmword ptr [rip + 0x27a9df6]  ; -> 02CA7FB0
004FE1BA  movups   xmmword ptr [rdx + 0x80], xmm1
004FE1C1  movaps   xmm0, xmmword ptr [rip + 0x27a9df8]  ; -> 02CA7FC0
004FE1C8  movups   xmmword ptr [rdx + 0x10], xmm0
004FE1CC  movaps   xmm1, xmmword ptr [rip + 0x27a9dfd]  ; -> 02CA7FD0
004FE1D3  movups   xmmword ptr [rdx + 0x20], xmm1
004FE1D7  movaps   xmm0, xmmword ptr [rip + 0x27a9e02]  ; -> 02CA7FE0
004FE1DE  movups   xmmword ptr [rdx + 0x30], xmm0
004FE1E2  movaps   xmm1, xmmword ptr [rip + 0x27a9e07]  ; -> 02CA7FF0
004FE1E9  movups   xmmword ptr [rdx + 0x40], xmm1
004FE1ED  movss    xmm0, dword ptr [rip + 0x25efd1b]  ; -> 02AEDF10
004FE1F5  movss    dword ptr [rdx + 0xe0], xmm0
004FE1FD  movss    xmm1, dword ptr [rip + 0x25efd0f]  ; -> 02AEDF14
004FE205  movss    dword ptr [rdx + 0xe4], xmm1
004FE20D  movss    xmm0, dword ptr [rip + 0x25efd03]  ; -> 02AEDF18
004FE215  movss    dword ptr [rdx + 0xe8], xmm0
004FE21D  movsd    xmm1, qword ptr [rdx + 0xe0]
004FE225  movsd    qword ptr [rip + 0x29bc283], xmm1  ; -> 02EBA4B0
004FE22D  mov      eax, dword ptr [rdx + 0xe8]
004FE233  mov      dword ptr [rip + 0x29bc27f], eax  ; -> 02EBA4B8
004FE239  mov      dword ptr [rdx + 0xa0], 0x44dfff00
004FE243  mov      dword ptr [rdx + 0xa4], 0x44e3ff00
004FE24D  call     0x504450  ; -> 00504450 fn
004FE252  mov      rbx, qword ptr [rsp + 0x40]
004FE257  mov      rbp, qword ptr [rsp + 0x50]
004FE25C  add      rsp, 0x20
004FE260  pop      r14
004FE262  pop      rdi
004FE263  pop      rsi
004FE264  ret      
```
