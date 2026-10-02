# F-interior pack: `12-Items-Equipment-Shops-License/the-shop-table-and-its-stock-gates.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/the-shop-table-and-its-stock-gates.json`.

Functions: 2. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: f22b2731b	FABLE: shop page corrected to OPUS's GR-13/14/15 record - one row layout (entry +0x10 price), +0x10 ; 06c849caf	SWE2-DATA: restate batches 0930E and GR - SD-3, SD-23, SD-166, SD-181..SD-184, SD-190, SD-191, SD-19; inbox mentions: SWE2-CONTRACT.md, SWE2-STRUCT.md). OPUS read these before packing.

## 003FD360 (842 B, extent 003FD360-003FD6AA)

Page context: " ptr [rcx + 0x17e], r15b 005647B4   mov byte ptr [rcx + 0x17f], r15b           ; selector = kind 005647BB   lea rcx, [rip + 0x19c83ce]                 ; then a per-kind pointer table, indexed kind*8  003FD360:  mov byte ptr [rcx + 0x17e], dl             ; arg1 = this widget's own kind 003FD36E   lea eax, [rdx + 0x40] 003FD371   mov byte ptr [rcx + 0x17f], al             ; selector = kind + 0x40 '''  **'003FD360''s half of that is alread"

```
003FD360  push     rbx
003FD362  push     rsi
003FD363  push     rdi
003FD364  sub      rsp, 0x30
003FD368  mov      byte ptr [rcx + 0x17e], dl
003FD36E  lea      eax, [rdx + 0x40]
003FD371  mov      byte ptr [rcx + 0x17f], al
003FD377  mov      rsi, rcx
003FD37A  movsx    r10, dl
003FD37E  lea      rax, [rip + 0x1b2f913]  ; -> 01F2CC98
003FD385  mov      qword ptr [rsp + 0x50], rbp
003FD38A  mov      qword ptr [rsp + 0x58], r12
003FD38F  mov      r12d, r9d
003FD392  mov      qword ptr [rsp + 0x60], r13
003FD397  or       r13d, 0xffffffff
003FD39B  mov      rax, qword ptr [rax + r10*8]
003FD39F  and      dword ptr [rcx + 0x180], 0xfbffffff
003FD3A9  or       dword ptr [rcx + 0x180], 0x8000000
003FD3B3  mov      qword ptr [rcx + 0xe8], rax
003FD3BA  mov      byte ptr [rcx + 0x180], r8b
003FD3C1  mov      rax, qword ptr [rip + 0x1c9d868]  ; -> 0209AC30
003FD3C8  shl      r10, 5
003FD3CC  movzx    ecx, word ptr [r10 + rax + 0xd48]
003FD3D5  mov      eax, 0x1000
003FD3DA  mov      word ptr [rsi + 0x17c], cx
003FD3E1  cmp      cx, ax
003FD3E4  jne      0x3fd3ee  ; -> 003FD3EE
003FD3E6  mov      word ptr [rsi + 0x17c], r13w
003FD3EE  mov      rax, qword ptr [rsi + 0xe8]
003FD3F5  xor      ebx, ebx
003FD3F7  and      dword ptr [rsi + 0x180], 0xffe0ffff
003FD401  mov      ebp, ebx
003FD403  cmp      dword ptr [rax], ebx
003FD405  jle      0x3fd5a7  ; -> 003FD5A7
003FD40B  mov      qword ptr [rsp + 0x28], r14
003FD410  mov      qword ptr [rsp + 0x20], r15
003FD415  mov      r15d, 0xffff
003FD41B  nop      dword ptr [rax + rax]
003FD420  mov      rax, qword ptr [rsi + 0xe8]
003FD427  mov      edi, ebx
003FD429  movsxd   rcx, ebp
003FD42C  lea      r14, [rax + rcx*8]
003FD430  movzx    ecx, word ptr [rax + rcx*8 + 4]
003FD435  add      cx, 9
003FD439  call     0x252d10  ; -> 00252D10 fn
003FD43E  test     al, al
003FD440  jne      0x3fd457  ; -> 003FD457
003FD442  movzx    edx, word ptr [r14 + 6]
003FD447  movsx    ecx, byte ptr [rsi + 0x17f]
003FD44E  call     0x57d610  ; -> 0057D610 fn
003FD453  test     eax, eax
003FD455  je       0x3fd45c  ; -> 003FD45C
003FD457  mov      edi, 1
003FD45C  movzx    ecx, word ptr [r14 + 4]
003FD461  cmp      cx, 0xa
003FD465  je       0x3fd484  ; -> 003FD484
003FD467  lea      eax, [rcx - 0x1b]
003FD46A  cmp      ax, 3
003FD46E  jbe      0x3fd484  ; -> 003FD484
003FD470  cmp      cx, 5
003FD474  jne      0x3fd4fc  ; -> 003FD4FC
003FD47A  test     r12d, r12d
003FD47D  je       0x3fd4fc  ; -> 003FD4FC
003FD47F  jmp      0x3fd586  ; -> 003FD586
003FD484  mov      r15, qword ptr [rip + 0x1c9d7a5]  ; -> 0209AC30
003FD48B  movzx    ecx, byte ptr [r15 + 0xd4b]
003FD493  call     0x2cca10  ; -> 002CCA10 fn
003FD498  test     eax, eax
003FD49A  je       0x3fd586  ; -> 003FD586
003FD4A0  movzx    edx, word ptr [r14 + 4]
003FD4A5  cmp      dx, 0xa
003FD4A9  je       0x3fd4f6  ; -> 003FD4F6
003FD4AB  movzx    ecx, byte ptr [r15 + 0xd4b]
003FD4B3  sub      ecx, 7
003FD4B6  je       0x3fd4ec  ; -> 003FD4EC
003FD4B8  sub      ecx, 1
003FD4BB  je       0x3fd4df  ; -> 003FD4DF
003FD4BD  sub      ecx, 1
003FD4C0  je       0x3fd4d2  ; -> 003FD4D2
003FD4C2  cmp      ecx, 8
003FD4C5  jne      0x3fd4f6  ; -> 003FD4F6
003FD4C7  cmp      dx, 0x1e
003FD4CB  je       0x3fd4f6  ; -> 003FD4F6
003FD4CD  jmp      0x3fd586  ; -> 003FD586
003FD4D2  cmp      dx, 0x1d
003FD4D6  mov      eax, ebx
003FD4D8  cmove    eax, edi
003FD4DB  mov      edi, eax
003FD4DD  jmp      0x3fd4f6  ; -> 003FD4F6
003FD4DF  cmp      dx, 0x1c
003FD4E3  mov      eax, ebx
003FD4E5  cmove    eax, edi
003FD4E8  mov      edi, eax
003FD4EA  jmp      0x3fd4f6  ; -> 003FD4F6
003FD4EC  cmp      dx, 0x1b
003FD4F0  jne      0x3fd586  ; -> 003FD586
003FD4F6  mov      r15d, 0xffff
003FD4FC  test     edi, edi
003FD4FE  je       0x3fd586  ; -> 003FD586
003FD504  mov      edx, dword ptr [rsi + 0x180]
003FD50A  mov      eax, edx
003FD50C  shl      eax, 0xb
003FD50F  movsxd   rcx, eax
003FD512  mov      eax, edx
003FD514  and      eax, 0xffff0000
003FD519  sar      rcx, 0x1b
003FD51D  add      eax, 0x10000
003FD522  xor      eax, edx
003FD524  and      eax, 0x1f0000
003FD529  xor      eax, edx
003FD52B  lea      rdi, [rsi + rcx*8]
003FD52F  mov      dword ptr [rsi + 0x180], eax
003FD535  mov      dl, 1
003FD537  movzx    ecx, word ptr [r14 + 4]
003FD53C  add      cx, 9
003FD540  call     0x252d40  ; -> 00252D40 fn
003FD545  movsx    eax, byte ptr [r14 + 4]
003FD54A  mov      ecx, 8
003FD54F  mov      byte ptr [rdi + 0xf7], al
003FD555  mov      byte ptr [rdi + 0xf6], bpl
003FD55C  mov      word ptr [rdi + 0xf2], r13w
003FD564  lea      edx, [rax + 0x20]
003FD567  mov      word ptr [rdi + 0xf4], r13w
003FD56F  lea      r8d, [rcx - 7]
003FD573  call     0x2526f0  ; -> 002526F0 fn
003FD578  test     eax, eax
003FD57A  cmove    ax, r15w
003FD57F  mov      word ptr [rdi + 0xf0], ax
003FD586  mov      rax, qword ptr [rsi + 0xe8]
003FD58D  inc      ebp
003FD58F  mov      r15d, 0xffff
003FD595  cmp      ebp, dword ptr [rax]
003FD597  jl       0x3fd420  ; -> 003FD420
003FD59D  mov      r15, qword ptr [rsp + 0x20]
003FD5A2  mov      r14, qword ptr [rsp + 0x28]
003FD5A7  mov      eax, dword ptr [rsi + 0x180]
003FD5AD  mov      ecx, 8
003FD5B2  shl      eax, 0xb
003FD5B5  movsxd   rdx, eax
003FD5B8  sar      rdx, 0x1b
003FD5BC  lea      r8d, [rcx - 7]
003FD5C0  mov      byte ptr [rsi + rdx*8 + 0xf6], 0xff
003FD5C8  movsx    edx, byte ptr [rsi + 0x17e]
003FD5CF  and      dword ptr [rsi + 0x180], 0xfc1fffff
003FD5D9  add      edx, 0x48
003FD5DC  call     0x2526f0  ; -> 002526F0 fn
003FD5E1  cmp      byte ptr [rsi + 0x17e], 1
003FD5E8  mov      edi, eax
003FD5EA  mov      r13, qword ptr [rsp + 0x60]
003FD5EF  mov      r12, qword ptr [rsp + 0x58]
003FD5F4  jne      0x3fd649  ; -> 003FD649
003FD5F6  mov      rbp, qword ptr [rip + 0x1c9d633]  ; -> 0209AC30
003FD5FD  movzx    ecx, byte ptr [rbp + 0xd4b]
003FD604  call     0x2cca10  ; -> 002CCA10 fn
003FD609  test     eax, eax
003FD60B  je       0x3fd649  ; -> 003FD649
003FD60D  movzx    ecx, byte ptr [rbp + 0xd4b]
003FD614  sub      ecx, 7
003FD617  je       0x3fd644  ; -> 003FD644
003FD619  sub      ecx, 1
003FD61C  je       0x3fd63d  ; -> 003FD63D
003FD61E  sub      ecx, 1
003FD621  je       0x3fd636  ; -> 003FD636
003FD623  cmp      ecx, 8
003FD626  je       0x3fd62f  ; -> 003FD62F
003FD628  mov      edi, 0xa
003FD62D  jmp      0x3fd649  ; -> 003FD649
003FD62F  mov      edi, 0x1e
003FD634  jmp      0x3fd649  ; -> 003FD649
003FD636  mov      edi, 0x1d
003FD63B  jmp      0x3fd649  ; -> 003FD649
003FD63D  mov      edi, 0x1c
003FD642  jmp      0x3fd649  ; -> 003FD649
003FD644  mov      edi, 0x1b
003FD649  mov      r8d, dword ptr [rsi + 0x180]
003FD650  mov      edx, r8d
003FD653  mov      rbp, qword ptr [rsp + 0x50]
003FD658  shl      edx, 0xb
003FD65B  sar      edx, 0x1b
003FD65E  test     edx, edx
003FD660  jle      0x3fd6a2  ; -> 003FD6A2
003FD662  nop      dword ptr [rax]
003FD666  nop      word ptr [rax + rax]
003FD670  movsxd   rax, ebx
003FD673  movsx    ecx, byte ptr [rsi + rax*8 + 0xf7]
003FD67B  cmp      ecx, edi
003FD67D  je       0x3fd68d  ; -> 003FD68D
003FD67F  inc      ebx
003FD681  cmp      ebx, edx
003FD683  jl       0x3fd670  ; -> 003FD670
003FD685  add      rsp, 0x30
003FD689  pop      rdi
003FD68A  pop      rsi
003FD68B  pop      rbx
003FD68C  ret      
003FD68D  shl      ebx, 0x15
003FD690  xor      ebx, r8d
003FD693  and      ebx, 0x3e00000
003FD699  xor      ebx, r8d
003FD69C  mov      dword ptr [rsi + 0x180], ebx
003FD6A2  add      rsp, 0x30
003FD6A6  pop      rdi
003FD6A7  pop      rsi
003FD6A8  pop      rbx
003FD6A9  ret      
```

## 0057CDD0 (57 B, extent 0057CDD0-0057CE09)

Page context: "st reached, and I let a print limit define the > population.** > > **The same re-run also shows the screen I used was too crude in the other direction.** "Advances a cursor by > '0x20'" also matches '0057CDD0', '002497E0' and '00252FA0' — whose 'add …, 0x20' is **'add rsp, 0x20'**, stack > cleanup. Checking *what* is advanced, and whether anything is written through it, separates them: '0057DC30' > steps 'rbx' and writes through it **te"

```
0057CDD0  mov      qword ptr [rsp + 8], rbx
0057CDD5  push     rdi
0057CDD6  sub      rsp, 0x20
0057CDDA  mov      edi, ecx
0057CDDC  mov      ecx, 2
0057CDE1  shl      edi, 5
0057CDE4  mov      edx, edi
0057CDE6  call     0x2497e0  ; -> 002497E0 fn
0057CDEB  mov      r8d, edi
0057CDEE  xor      edx, edx
0057CDF0  mov      rcx, rax
0057CDF3  mov      rbx, rax
0057CDF6  call     0x861ec0  ; -> 00861EC0 fn
0057CDFB  mov      rax, rbx
0057CDFE  mov      rbx, qword ptr [rsp + 0x30]
0057CE03  add      rsp, 0x20
0057CE07  pop      rdi
0057CE08  ret      
```
