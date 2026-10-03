# Homing pack: `22-Middleware-PhyreEngine/Post-Process-Chain/the-post-process-passes-and-their-shader-constants.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-post-process-passes-and-their-shader-constants.json`.

Bodies: 5. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0017D900 (36 B, extent 0017D900-0017D924)

Entered from (direct sites whose caller this page cites): `00191130` + 0x1DA (call; `00191130` is cited on this page)
Other direct sites: none

Host context: ", 'g_HBAOResolution', 'g_RChr', 'g_AngleBiasChr', 'g_ContrastChr', 'g_RSce', 'g_AngleBiasSce', 'g_ContrastSce', 'g_fadeoutScale', 'g_maskBorder', 'tLinDepth', 'tNormal', 'projInfo', 'samNearest' | | '00191130' | 1,066 B | **depth mask** | 'MaskDepth' — interior verified 2026-09-17 (SWE2-FRONTIER): '001BC000' first at ['0019119D'](../../_index/ADDRESS-INDEX.md), '0060F6B0' ×5 + '0060B980' ×4 | | '00191560' | 2,101 B | **depth of field** "

```
0017D900  sub      rsp, 0x28
0017D904  call     0x1d50d0  ; -> 001D50D0 fn
0017D909  test     rax, rax
0017D90C  je       0x17d91f  ; -> 0017D91F
0017D90E  call     0x1d50d0  ; -> 001D50D0 fn
0017D913  movzx    eax, byte ptr [rax + 0x10e0]
0017D91A  add      rsp, 0x28
0017D91E  ret      
0017D91F  add      rsp, 0x28
0017D923  ret      
```

## 001EBB70 (128 B, extent 001EBB70-001EBBF0)

Entered from (direct sites whose caller this page cites): `001C6320` + 0x62D (call; `001C6320` is cited on this page)
Other direct sites: none

Host context: "his page's subjects   serve Presentation callers, which are not read here. - **Developer - CLIENT (3 edges).** '00200B50', '00200BE0', '00796E20' are called by bodies filed to Developer: '001C2F50', '001C6320' - shared machinery across the layer boundary, no shared ownership. - **Input - CLIENT and SERVICE (58 edges).** '00584740', '00597970', '00598100', '0059D920' (+5 more) are called by bodies filed to Input: '0017DDC0', '0017DE10', "

```
001EBB70  movups   xmm0, xmmword ptr [rdx]
001EBB73  add      rcx, 0x144
001EBB7A  movups   xmmword ptr [rcx], xmm0
001EBB7D  movups   xmm1, xmmword ptr [rdx + 0x10]
001EBB81  movups   xmmword ptr [rcx + 0x10], xmm1
001EBB85  movups   xmm0, xmmword ptr [rdx + 0x20]
001EBB89  movups   xmmword ptr [rcx + 0x20], xmm0
001EBB8D  movups   xmm1, xmmword ptr [rdx + 0x30]
001EBB91  movups   xmmword ptr [rcx + 0x30], xmm1
001EBB95  movups   xmm0, xmmword ptr [rdx + 0x40]
001EBB99  movups   xmmword ptr [rcx + 0x40], xmm0
001EBB9D  movups   xmm1, xmmword ptr [rdx + 0x50]
001EBBA1  movups   xmmword ptr [rcx + 0x50], xmm1
001EBBA5  movups   xmm0, xmmword ptr [rdx + 0x60]
001EBBA9  movups   xmmword ptr [rcx + 0x60], xmm0
001EBBAD  sub      rcx, -0x80
001EBBB1  movups   xmm0, xmmword ptr [rdx + 0x70]
001EBBB5  movups   xmmword ptr [rcx - 0x10], xmm0
001EBBB9  movups   xmm1, xmmword ptr [rdx + 0x80]
001EBBC0  movups   xmmword ptr [rcx], xmm1
001EBBC3  movups   xmm0, xmmword ptr [rdx + 0x90]
001EBBCA  movups   xmmword ptr [rcx + 0x10], xmm0
001EBBCE  movups   xmm1, xmmword ptr [rdx + 0xa0]
001EBBD5  movups   xmmword ptr [rcx + 0x20], xmm1
001EBBD9  movups   xmm0, xmmword ptr [rdx + 0xb0]
001EBBE0  movups   xmmword ptr [rcx + 0x30], xmm0
001EBBE4  movups   xmm1, xmmword ptr [rdx + 0xc0]
001EBBEB  movups   xmmword ptr [rcx + 0x40], xmm1
001EBBEF  ret      
```

## 001EBC20 (44 B, extent 001EBC20-001EBC4C)

Entered from (direct sites whose caller this page cites): `001C6320` + 0x145 (call; `001C6320` is cited on this page)
Other direct sites: none

Host context: "his page's subjects   serve Presentation callers, which are not read here. - **Developer - CLIENT (3 edges).** '00200B50', '00200BE0', '00796E20' are called by bodies filed to Developer: '001C2F50', '001C6320' - shared machinery across the layer boundary, no shared ownership. - **Input - CLIENT and SERVICE (58 edges).** '00584740', '00597970', '00598100', '0059D920' (+5 more) are called by bodies filed to Input: '0017DDC0', '0017DE10', "

```
001EBC20  mov      r8d, edx
001EBC23  mov      byte ptr [rcx + 0x140], 1
001EBC2A  mov      eax, 0x66666667
001EBC2F  imul     edx
001EBC31  sar      edx, 5
001EBC34  mov      eax, edx
001EBC36  shr      eax, 0x1f
001EBC39  add      edx, eax
001EBC3B  lea      eax, [rdx + rdx*4]
001EBC3E  shl      eax, 4
001EBC41  sub      r8d, eax
001EBC44  mov      dword ptr [rcx + 0x224], r8d
001EBC4B  ret      
```

## 002F1690 (17 B, extent 002F1690-002F16A1)

Entered from (direct sites whose caller this page cites): `001C6320` + 0x27B (call; `001C6320` is cited on this page)
Other direct sites: none

Host context: "his page's subjects   serve Presentation callers, which are not read here. - **Developer - CLIENT (3 edges).** '00200B50', '00200BE0', '00796E20' are called by bodies filed to Developer: '001C2F50', '001C6320' - shared machinery across the layer boundary, no shared ownership. - **Input - CLIENT and SERVICE (58 edges).** '00584740', '00597970', '00598100', '0059D920' (+5 more) are called by bodies filed to Input: '0017DDC0', '0017DE10', "

```
002F1690  subss    xmm0, dword ptr [rip + 0x5d48e0]  ; -> 008C5F78 [f32 1000]
002F1698  movss    dword ptr [rip + 0x1fcc81c], xmm0  ; -> 022BDEBC
002F16A0  ret      
```

## 006560E0 (231 B, extent 006560E0-006561C7)

Entered from (direct sites whose caller this page cites): `00655C10` + 0x60 (call; `00655C10` is cited on this page)
Other direct sites: `00654160` + 0x0 (jmp)

Host context: "family.** 'Phyre::PPostProcessing::PFXAA', 'PFXAABase' and     'PFXAAD3D11' have real vtables with **distinct per-class slots** — slot-0 constructors     '00647530' / '00647590' / '006475F0', slot 1 '00655C10' against '00655DC0', slot 2 '00657430'     against '006575E0' — all in the '006xxxxx' band, with the shader     '/GameData/D3D11/ArtData/shaders/PhyreFXAA.fx.phyre', script accessors for all three classes, and     the method names "

```
006560E0  mov      qword ptr [rsp + 0x10], rbx
006560E5  mov      qword ptr [rsp + 0x18], rbp
006560EA  push     rdi
006560EB  push     r12
006560ED  push     r13
006560EF  push     r14
006560F1  push     r15
006560F3  sub      rsp, 0x30
006560F7  mov      rbp, rdx
006560FA  mov      r12d, r9d
006560FD  xor      r9d, r9d
00656100  mov      r13d, r8d
00656103  mov      r15, rcx
00656106  lea      r8, [rip + 0x26657f3]  ; -> 02CBB900
0065610D  mov      rcx, rbp
00656110  lea      edx, [r9 + 1]
00656114  call     0x63a990  ; -> 0063A990 fn
00656119  mov      r14, rax
0065611C  test     rax, rax
0065611F  jne      0x656128  ; -> 00656128
00656121  xor      ebx, ebx
00656123  mov      rdi, rbx
00656126  jmp      0x65619e  ; -> 0065619E
00656128  mov      rdx, r14
0065612B  mov      rcx, rbp
0065612E  call     0x5d8e40  ; -> 005D8E40 fn
00656133  xor      ebx, ebx
00656135  mov      rdi, rax
00656138  test     rax, rax
0065613B  je       0x656123  ; -> 00656123
0065613D  mov      qword ptr [rsp + 0x60], rsi
00656142  cmp      byte ptr [rax + 8], bl
00656145  jne      0x656180  ; -> 00656180
00656147  mov      rsi, qword ptr [rax]
0065614A  test     rsi, rsi
0065614D  je       0x656180  ; -> 00656180
0065614F  lea      r9, [rip + 0x26a132a]  ; -> 02CF7480
00656156  mov      dword ptr [rsp + 0x20], ebx
0065615A  mov      r8d, r12d
0065615D  mov      edx, r13d
00656160  mov      rcx, rsi
00656163  call     0x60dd70  ; -> 0060DD70 fn
00656168  test     eax, eax
0065616A  jne      0x656180  ; -> 00656180
0065616C  and      dword ptr [rsi + 0x18], 0xfffffffd
00656170  mov      rcx, rsi
00656173  mov      byte ptr [rsi + 9], bl
00656176  call     0x610990  ; -> 00610990 fn
0065617B  mov      byte ptr [rdi + 9], bl
0065617E  jmp      0x656199  ; -> 00656199
00656180  mov      rdx, rdi
00656183  mov      rcx, rbp
00656186  call     0x63abf0  ; -> 0063ABF0 fn
0065618B  mov      rdx, r14
0065618E  mov      rcx, rbp
00656191  call     0x63abf0  ; -> 0063ABF0 fn
00656196  mov      rdi, rbx
00656199  mov      rsi, qword ptr [rsp + 0x60]
0065619E  mov      rbp, qword ptr [rsp + 0x70]
006561A3  mov      eax, 0xd
006561A8  test     rdi, rdi
006561AB  mov      qword ptr [r15 + 0x50], rdi
006561AF  cmove    ebx, eax
006561B2  mov      eax, ebx
006561B4  mov      rbx, qword ptr [rsp + 0x68]
006561B9  add      rsp, 0x30
006561BD  pop      r15
006561BF  pop      r14
006561C1  pop      r13
006561C3  pop      r12
006561C5  pop      rdi
006561C6  ret      
```
