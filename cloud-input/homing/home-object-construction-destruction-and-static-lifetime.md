# Homing pack: `24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/object-construction-destruction-and-static-lifetime.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-object-construction-destruction-and-static-lifetime.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0019B400 (115 B, extent 0019B400-0019B473)

Entered from (direct sites whose caller this page cites): `0019B500` + 0xF (call; `0019B500` is cited on this page)
Other direct sites: `0019B480` + 0x44 (call); `00202930` + 0x19F (call)

Host context: "nt: 'ec7/dealloc_classes.py'. **BQ-28.**  ## 8. Evidence  | Claim | Evidence | Tier | |---|---|---| | The deleting-destructor idiom and its two spellings | complete bodies of '001D70A0', '00195530', '0019B500' | 1 | | All 226 deleting-destructor labels perform the flag test | whole-image disassembly, flag followed through a register copy from 'edx' | 1 | | The sub-labels record which deallocator is used | all 63 'AlignedOrGuardedFree' r"

```
0019B400  push     rbx
0019B402  sub      rsp, 0x30
0019B406  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0019B40F  mov      rbx, rcx
0019B412  lea      rax, [rip + 0x758aaf]  ; -> 008F3EC8
0019B419  mov      qword ptr [rcx], rax
0019B41C  cmp      qword ptr [rcx + 0x80], 0
0019B424  je       0x19b455  ; -> 0019B455
0019B426  mov      rcx, qword ptr [rcx + 0x18]
0019B42A  lea      rax, [rbx + 0x70]
0019B42E  cmp      qword ptr [rcx], rax
0019B431  jne      0x19b455  ; -> 0019B455
0019B433  mov      r8, qword ptr [rbx + 0x90]
0019B43A  mov      rdx, qword ptr [rbx + 0x88]
0019B441  mov      qword ptr [rcx], rdx
0019B444  mov      rax, qword ptr [rbx + 0x38]
0019B448  mov      qword ptr [rax], rdx
0019B44B  sub      r8d, edx
0019B44E  mov      rax, qword ptr [rbx + 0x50]
0019B452  mov      dword ptr [rax], r8d
0019B455  cmp      byte ptr [rbx + 0x7c], 0
0019B459  je       0x19b464  ; -> 0019B464
0019B45B  mov      rcx, rbx
0019B45E  call     0x19b8c0  ; -> 0019B8C0 fn
0019B463  nop      
0019B464  mov      rcx, rbx
0019B467  add      rsp, 0x30
0019B46B  pop      rbx
0019B46C  jmp      qword ptr [rip + 0x72732d]  ; -> 008C27A0 [u64 0x0000000001CCDA9C]
```

## 0020B9A0 (197 B, extent 0020B9A0-0020BA65)

Entered from (direct sites whose caller this page cites): `001D6AA0` + 0x1C (call; `001D6AA0` is cited on this page)
Other direct sites: none

Host context: "3 edges.**   - The four Phyre serialisation bodies '00597970', '00598100', '0059BD40' and '0059F4A0' are called by the resource     loaders ('0019EAA0', '001A0CF0'-'001A0F80', '001D9A40'), and reach '001D6AA0' / '002150D0'.   - '001A9050', 'AddMotion_LoadResources' and '00210760' call the resource request helpers '001D6E80'-'001D6FA0'.   - The vector grow '001AB570' is also called by the asset-manifest parser.   - The map-table requeste"

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
