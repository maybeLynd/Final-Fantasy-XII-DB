# F-interior pack: `25-EBP-Script-Container/Sections/section-019.md`

Generated 2026-10-03 02:49 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/section-019.json`.

Functions: 2. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 01c2429f6	SWE2-CONTRACT: pass-22 debt batch B - 47 Script-VM, Resource, EBP and PKFL pages' cross-subsystem ne; inbox mentions: repos-1e.md, repos-3f.md, repos-4b.md, repos-c9.md, repos-d6.md). OPUS read these before packing.

## 0020D270 (60 B, extent 0020D270-0020D2AC)

Page context: "erior anchor '0020D8C7' (the 'imul' capacity math).   '0020D7C0' (217 B) is the '0xC'-element vector reassign '0020D8A0' runs on 'rcx''s '{begin, end, cap}' triple: '0020D970' allocates 'r14 * 0xC', '0020D270' elementwise-copies the source range in, the old buffer's '(cap - begin) / 0xC' count is computed through the '0x2AAAAAAAAAAAAAAB' multiply-shift and '001CD050' frees it, then 'begin = new', 'end = new + count*0xC', 'cap = new + r1"

```
0020D270  sub      rsp, 0x38
0020D274  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0020D27D  cmp      rcx, rdx
0020D280  je       0x20d2a4  ; -> 0020D2A4
0020D282  test     r8, r8
0020D285  je       0x20d297  ; -> 0020D297
0020D287  movsd    xmm0, qword ptr [rcx]
0020D28B  movsd    qword ptr [r8], xmm0
0020D290  mov      eax, dword ptr [rcx + 8]
0020D293  mov      dword ptr [r8 + 8], eax
0020D297  add      r8, 0xc
0020D29B  add      rcx, 0xc
0020D29F  cmp      rcx, rdx
0020D2A2  jne      0x20d282  ; -> 0020D282
0020D2A4  mov      rax, r8
0020D2A7  add      rsp, 0x38
0020D2AB  ret      
```

## 0020D970 (128 B, extent 0020D970-0020D9F0)

Page context: "o long"' throw via '008C2618'. Interior anchor '0020D8C7' (the 'imul' capacity math).   '0020D7C0' (217 B) is the '0xC'-element vector reassign '0020D8A0' runs on 'rcx''s '{begin, end, cap}' triple: '0020D970' allocates 'r14 * 0xC', '0020D270' elementwise-copies the source range in, the old buffer's '(cap - begin) / 0xC' count is computed through the '0x2AAAAAAAAAAAAAAB' multiply-shift and '001CD050' frees it, then 'begin = new', 'end ="

```
0020D970  sub      rsp, 0x28
0020D974  test     rdx, rdx
0020D977  jne      0x20d980  ; -> 0020D980
0020D979  xor      eax, eax
0020D97B  add      rsp, 0x28
0020D97F  ret      
0020D980  movabs   rax, 0x1555555555555555
0020D98A  cmp      rdx, rax
0020D98D  jbe      0x20d996  ; -> 0020D996
0020D98F  call     qword ptr [rip + 0x6b4c73]  ; -> 008C2608 [u64 0x0000000001CCCD84]
0020D995  int3     
0020D996  lea      rcx, [rdx + rdx*2]
0020D99A  shl      rcx, 2
0020D99E  cmp      rcx, 0x1000
0020D9A5  jb       0x20d9df  ; -> 0020D9DF
0020D9A7  lea      rax, [rcx + 0x27]
0020D9AB  cmp      rax, rcx
0020D9AE  ja       0x20d9b7  ; -> 0020D9B7
0020D9B0  call     qword ptr [rip + 0x6b4c52]  ; -> 008C2608 [u64 0x0000000001CCCD84]
0020D9B6  int3     
0020D9B7  mov      rcx, rax
0020D9BA  call     0x210ec0  ; -> 00210EC0 fn
0020D9BF  mov      rcx, rax
0020D9C2  test     rax, rax
0020D9C5  jne      0x20d9ce  ; -> 0020D9CE
0020D9C7  call     qword ptr [rip + 0x6b53db]  ; -> 008C2DA8 [u64 0x0000000001CCED90]
0020D9CD  int3     
0020D9CE  add      rax, 0x27
0020D9D2  and      rax, 0xffffffffffffffe0
0020D9D6  mov      qword ptr [rax - 8], rcx
0020D9DA  add      rsp, 0x28
0020D9DE  ret      
0020D9DF  call     0x210ec0  ; -> 00210EC0 fn
0020D9E4  test     rax, rax
0020D9E7  jne      0x20d97b  ; -> 0020D97B
0020D9E9  call     qword ptr [rip + 0x6b53b9]  ; -> 008C2DA8 [u64 0x0000000001CCED90]
0020D9EF  int3     
```
