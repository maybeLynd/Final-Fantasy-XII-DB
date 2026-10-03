# Homing pack: `22-Middleware-PhyreEngine/Post-Process-Chain/the-post-process-passes-and-their-shader-constants.md`

Generated 2026-10-03 15:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h14-the-post-process-passes-and-their-shader-constants.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

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

## 0020B9A0 (197 B, extent 0020B9A0-0020BA65)

Entered from (direct sites whose caller this page cites): `001D6AA0` + 0x1C (call; `001D6AA0` is cited on this page)
Other direct sites: none

Host context: "(+14 more) are called by bodies filed to Resource: '0019EAA0', '0019EE50', '001A0CF0', '001A0E50' (+25 more); '0018D160', '0019CB20', '001F5D70', '00597970' (+6 more) reach bodies filed to Resource: '001D6AA0', '0020B5F0', '002150D0', '002DF980' (+12 more) - shared machinery across the layer boundary, no shared ownership. - **UI - CLIENT (6 edges).** '0018CD90', '0018F8F0', '001EE8E0', '005FEFD0' (+2 more) are called by bodies filed to "

```
0020B9A0  mov      qword ptr [rsp + 0x10], rbx
0020B9A5  mov      qword ptr [rsp + 0x18], rsi
0020B9AA  push     rdi
0020B9AB  sub      rsp, 0x20
0020B9AF  mov      rsi, r8
0020B9B2  mov      ebx, edx
0020B9B4  mov      rdi, rcx
0020B9B7  test     r8, r8
0020B9BA  je       0x20ba53  ; -> 0020BA53
0020B9C0  add      rcx, 0x58
0020B9C4  mov      qword ptr [rsp + 0x30], rbp
0020B9C9  call     0x5cd4f0  ; -> 005CD4F0 fn
0020B9CE  mov      r9, qword ptr [rdi + 0x38]
0020B9D2  lea      rcx, [rdi + 0x28]
0020B9D6  mov      rax, rcx
0020B9D9  test     r9, r9
0020B9DC  je       0x20b9f7  ; -> 0020B9F7
0020B9DE  nop      
0020B9E0  cmp      dword ptr [r9 + 0x20], ebx
0020B9E4  jb       0x20b9ef  ; -> 0020B9EF
0020B9E6  mov      rax, r9
0020B9E9  mov      r9, qword ptr [r9 + 8]
0020B9ED  jmp      0x20b9f2  ; -> 0020B9F2
0020B9EF  mov      r9, qword ptr [r9]
0020B9F2  test     r9, r9
0020B9F5  jne      0x20b9e0  ; -> 0020B9E0
0020B9F7  cmp      rax, rcx
0020B9FA  je       0x20ba01  ; -> 0020BA01
0020B9FC  cmp      ebx, dword ptr [rax + 0x20]
0020B9FF  jae      0x20ba04  ; -> 0020BA04
0020BA01  mov      rax, rcx
0020BA04  lea      rdx, [rdi + 0x28]
0020BA08  cmp      rax, rdx
0020BA0B  je       0x20ba1e  ; -> 0020BA1E
0020BA0D  mov      rdx, qword ptr [rax + 0x28]
0020BA11  movzx    eax, byte ptr [rdx + 0x10]
0020BA15  test     al, al
0020BA17  je       0x20ba1e  ; -> 0020BA1E
0020BA19  dec      al
0020BA1B  mov      byte ptr [rdx + 0x10], al
0020BA1E  lea      rcx, [rdi + 0x58]
0020BA22  call     0x5cd820  ; -> 005CD820 fn
0020BA27  mov      rcx, rsi
0020BA2A  call     0x16d6a0  ; -> 0016D6A0 fn
0020BA2F  mov      edx, 0x10
0020BA34  mov      rcx, rsi
0020BA37  call     0x809950  ; -> 00809950 fn
0020BA3C  mov      rbp, qword ptr [rsp + 0x30]
0020BA41  mov      al, 1
0020BA43  mov      rbx, qword ptr [rsp + 0x38]
0020BA48  mov      rsi, qword ptr [rsp + 0x40]
0020BA4D  add      rsp, 0x20
0020BA51  pop      rdi
0020BA52  ret      
0020BA53  mov      rbx, qword ptr [rsp + 0x38]
0020BA58  xor      al, al
0020BA5A  mov      rsi, qword ptr [rsp + 0x40]
0020BA5F  add      rsp, 0x20
0020BA63  pop      rdi
0020BA64  ret      
```
