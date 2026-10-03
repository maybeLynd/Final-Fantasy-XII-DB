# F homing pack: `06-Movement-And-Navigation/the-unit-shape-distance-primitives.md`

Generated 2026-10-02 22:28 by OPUS (homing_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 1. No bearing page cites them and no documented function calls them directly.

## 0022CC50 (765 B, extent 0022CC50-0022CF4D)

Documented callee on this page: `0022CF50`

```
0022CC50  mov      r11, rsp
0022CC53  push     rbx
0022CC54  push     rsi
0022CC55  push     r14
0022CC57  push     r15
0022CC59  sub      rsp, 0xa8
0022CC60  mov      rax, qword ptr [rip + 0x1d17bc9]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0022CC67  xor      rax, rsp
0022CC6A  mov      qword ptr [rsp + 0x60], rax
0022CC6F  xor      r15d, r15d
0022CC72  mov      rbx, rdx
0022CC75  mov      r14, rcx
0022CC78  mov      esi, r15d
0022CC7B  cmp      r15w, word ptr [rdx + 0x40]
0022CC80  jge      0x22cf32  ; -> 0022CF32
0022CC86  mov      qword ptr [r11 - 0x28], rdi
0022CC8A  mov      edx, 0x5000
0022CC8F  mov      qword ptr [r11 - 0x30], r12
0022CC93  mov      r12d, 0x4000
0022CC99  mov      qword ptr [r11 - 0x38], r13
0022CC9D  lea      r13, [rip + 0x1e6d62c]  ; -> 0209A2D0
0022CCA4  movaps   xmmword ptr [rsp + 0x70], xmm7
0022CCA9  xorps    xmm7, xmm7
0022CCAC  mov      qword ptr [r11 + 0x18], rbp
0022CCB0  movaps   xmmword ptr [r11 - 0x48], xmm6
0022CCB5  nop      word ptr [rax + rax]
0022CCC0  movsx    eax, word ptr [rbx + 0x3e]
0022CCC4  add      eax, esi
0022CCC6  movsxd   rcx, eax
0022CCC9  mov      rax, qword ptr [r14 + 0x28]
0022CCCD  movzx    edi, word ptr [rax + rcx*2]
0022CCD1  cmp      di, dx
0022CCD4  jge      0x22cef7  ; -> 0022CEF7
0022CCDA  cmp      di, r12w
0022CCDE  jl       0x22cd84  ; -> 0022CD84
0022CCE4  movsx    eax, di
0022CCE7  sub      eax, r12d
0022CCEA  cdqe     
0022CCEC  lea      r10, [rax + rax*8]
0022CCF0  shl      r10, 4
0022CCF4  add      r10, qword ptr [r14 + 0x18]
0022CCF8  mov      ecx, dword ptr [r10 + 4]
0022CCFC  shr      ecx, 0xd
0022CCFF  and      ecx, 0x1f
0022CD02  add      ecx, 0x20
0022CD05  mov      r8d, ecx
0022CD08  mov      edx, dword ptr [r13 + rcx*8 + 0x110]
0022CD10  mov      ecx, edx
0022CD12  mov      eax, dword ptr [r13 + r8*8 + 0x114]
0022CD1A  not      ecx
0022CD1C  and      ecx, dword ptr [r10 + 4]
0022CD20  and      eax, edx
0022CD22  or       ecx, eax
0022CD24  mov      eax, ecx
0022CD26  and      al, 7
0022CD28  cmp      al, 1
0022CD2A  jne      0x22cd49  ; -> 0022CD49
0022CD2C  cmp      ecx, 0x80000000
0022CD32  jae      0x22cef2  ; -> 0022CEF2
0022CD38  bt       ecx, 0x1e
0022CD3C  jae      0x22cd49  ; -> 0022CD49
0022CD3E  cmp      word ptr [rbx + 0x46], 4
0022CD43  je       0x22cef2  ; -> 0022CEF2
0022CD49  mov      r9, qword ptr [rbx + 0x18]
0022CD4D  lea      rcx, [rsp + 0x50]
0022CD52  mov      r8, qword ptr [rbx + 0x10]
0022CD56  mov      rdx, r10
0022CD59  call     0x380fa0  ; -> 00380FA0 fn
0022CD5E  comiss   xmm0, xmm7
0022CD61  jb       0x22cef2  ; -> 0022CEF2
0022CD67  movss    xmm1, dword ptr [rbx + 0x30]
0022CD6C  comiss   xmm1, xmm0
0022CD6F  jbe      0x22cef2  ; -> 0022CEF2
0022CD75  movss    dword ptr [rbx + 0x30], xmm0
0022CD7A  movaps   xmm0, xmmword ptr [rsp + 0x50]
0022CD7F  jmp      0x22cee1  ; -> 0022CEE1
0022CD84  mov      r10, qword ptr [r14 + 0x10]
0022CD88  movsx    r9, di
0022CD8C  shl      r9, 5
0022CD90  mov      ecx, dword ptr [r9 + r10 + 0xc]
0022CD95  shr      ecx, 0xd
0022CD98  and      ecx, 0x1f
0022CD9B  add      ecx, 0x20
0022CD9E  mov      r8d, ecx
0022CDA1  mov      edx, dword ptr [r13 + rcx*8 + 0x110]
0022CDA9  mov      ecx, edx
0022CDAB  mov      eax, dword ptr [r13 + r8*8 + 0x114]
0022CDB3  not      ecx
0022CDB5  and      ecx, dword ptr [r9 + r10 + 0xc]
0022CDBA  and      eax, edx
0022CDBC  movzx    edx, word ptr [rbx + 0x46]
0022CDC0  or       ecx, eax
0022CDC2  mov      eax, ecx
0022CDC4  and      eax, 7
0022CDC7  je       0x22ce01  ; -> 0022CE01
0022CDC9  sub      eax, 1
0022CDCC  je       0x22cde5  ; -> 0022CDE5
0022CDCE  cmp      eax, 3
0022CDD1  jne      0x22cef2  ; -> 0022CEF2
0022CDD7  cmp      dx, 4
0022CDDB  mov      eax, r15d
0022CDDE  sete     al
0022CDE1  test     eax, eax
0022CDE3  jmp      0x22cdfb  ; -> 0022CDFB
0022CDE5  cmp      ecx, 0x80000000
0022CDEB  jae      0x22cef2  ; -> 0022CEF2
0022CDF1  bt       ecx, 0x1e
0022CDF5  jae      0x22ce01  ; -> 0022CE01
0022CDF7  cmp      dx, 4
0022CDFB  je       0x22cef2  ; -> 0022CEF2
0022CE01  movss    xmm0, dword ptr [r9 + r10]
0022CE07  lea      rax, [rsp + 0x40]
0022CE0C  mov      rbp, qword ptr [rbx + 0x10]
0022CE10  lea      r8, [rsp + 0x30]
0022CE15  movss    dword ptr [rsp + 0x40], xmm0
0022CE1B  mov      rdx, rbx
0022CE1E  movss    xmm1, dword ptr [r9 + r10 + 4]
0022CE25  mov      rcx, rbp
0022CE28  movss    dword ptr [rsp + 0x44], xmm1
0022CE2E  movss    xmm0, dword ptr [r9 + r10 + 8]
0022CE35  mov      qword ptr [rsp + 0x30], rax
0022CE3A  movss    dword ptr [rsp + 0x48], xmm0
0022CE40  movss    xmm1, dword ptr [r9 + r10 + 0xc]
0022CE47  movss    dword ptr [rsp + 0x4c], xmm1
0022CE4D  movsx    rax, word ptr [r9 + r10 + 0x10]
0022CE53  shl      rax, 4
0022CE57  add      rax, qword ptr [r14 + 8]
0022CE5B  mov      qword ptr [rsp + 0x38], rax
0022CE60  call     0x22e6d0  ; -> 0022E6D0 fn
0022CE65  movaps   xmm6, xmm0
0022CE68  comiss   xmm6, xmm7
0022CE6B  jb       0x22cef2  ; -> 0022CEF2
0022CE71  movss    xmm1, dword ptr [rbx + 0x30]
0022CE76  comiss   xmm1, xmm6
0022CE79  jbe      0x22cef2  ; -> 0022CEF2
0022CE7B  movaps   xmm3, xmm0
0022CE7E  lea      r8, [rsp + 0x20]
0022CE83  divss    xmm3, dword ptr [rbx + 0x34]
0022CE88  movzx    edx, di
0022CE8B  mov      rcx, r14
0022CE8E  movss    xmm0, dword ptr [rbx + 0xc]
0022CE93  movaps   xmm2, xmm3
0022CE96  movss    dword ptr [rsp + 0x2c], xmm0
0022CE9C  mulss    xmm2, dword ptr [rbx]
0022CEA0  movaps   xmm1, xmm3
0022CEA3  mulss    xmm1, dword ptr [rbx + 4]
0022CEA8  mulss    xmm3, dword ptr [rbx + 8]
0022CEAD  addss    xmm2, dword ptr [rbp]
0022CEB2  addss    xmm1, dword ptr [rbp + 4]
0022CEB7  addss    xmm3, dword ptr [rbp + 8]
0022CEBC  movss    dword ptr [rsp + 0x20], xmm2
0022CEC2  movss    dword ptr [rsp + 0x24], xmm1
0022CEC8  movss    dword ptr [rsp + 0x28], xmm3
0022CECE  call     0x22cf50  ; -> 0022CF50 fn
0022CED3  test     eax, eax
0022CED5  je       0x22cef2  ; -> 0022CEF2
0022CED7  movaps   xmm0, xmmword ptr [rsp + 0x20]
0022CEDC  movss    dword ptr [rbx + 0x30], xmm6
0022CEE1  mov      rax, qword ptr [rbx + 0x20]
0022CEE5  movups   xmmword ptr [rax], xmm0
0022CEE8  mov      word ptr [rbx + 0x42], di
0022CEEC  cmp      dword ptr [rbx + 0x38], r15d
0022CEF0  jne      0x22cf05  ; -> 0022CF05
0022CEF2  mov      edx, 0x5000
0022CEF7  movsx    eax, word ptr [rbx + 0x40]
0022CEFB  inc      esi
0022CEFD  cmp      esi, eax
0022CEFF  jl       0x22ccc0  ; -> 0022CCC0
0022CF05  movaps   xmm6, xmmword ptr [rsp + 0x80]
0022CF0D  mov      rbp, qword ptr [rsp + 0xe0]
0022CF15  mov      r12, qword ptr [rsp + 0x98]
0022CF1D  mov      rdi, qword ptr [rsp + 0xa0]
0022CF25  mov      r13, qword ptr [rsp + 0x90]
0022CF2D  movaps   xmm7, xmmword ptr [rsp + 0x70]
0022CF32  mov      rcx, qword ptr [rsp + 0x60]
0022CF37  xor      rcx, rsp
0022CF3A  call     0x808c40  ; -> 00808C40 fn
0022CF3F  add      rsp, 0xa8
0022CF46  pop      r15
0022CF48  pop      r14
0022CF4A  pop      rsi
0022CF4B  pop      rbx
0022CF4C  ret      
```
