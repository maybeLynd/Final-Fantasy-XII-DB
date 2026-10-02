# F-interior pack: `17-Presentation-Rendering/Model-And-Motion-Formats/fte-fct-texture-colour-tables.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/fte-fct-texture-colour-tables.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 54e8a524e	SWE2-FRONTIER for FABLE: pass-22 unattributed appends - verifier + 23 of 34 PUBLISHABLE pages (batch). OPUS read these before packing.

## 00537AA0 (69 B, extent 00537AA0-00537AE5)

Page context: "*0x20', reader '0053AB50' computes '((idx+2)<<5) + FTE'):  ''' +0x00  u32  VRAM bytes reserved        (multiple of 0x2000 in 2,127/2,127;                                           bottom-up allocator 00537AA0) +0x04  u16  w    pixel width +0x06  u16  h    pixel height +0x08  u16  GS PSM format               (0x13 PSMT8 in 2,081, 0x14 PSMT4 in 46,                                           nothing else; passed through to TEX0             "

```
00537AA0  movsxd   rax, ecx
00537AA3  lea      rcx, [rip + 0x29829b6]  ; -> 02EBA460
00537AAA  mov      r9d, dword ptr [rcx + rax*4]
00537AAE  lea      r10, [rcx + rax*4]
00537AB2  lea      r11, [rcx + rax*4]
00537AB6  mov      ecx, dword ptr [rcx + rax*4 + 8]
00537ABA  mov      eax, ecx
00537ABC  sub      eax, r9d
00537ABF  cmp      eax, edx
00537AC1  jbe      0x537ae2  ; -> 00537AE2
00537AC3  test     r8d, r8d
00537AC6  je       0x537ad7  ; -> 00537AD7
00537AC8  cmp      r8d, 1
00537ACC  jne      0x537ae2  ; -> 00537AE2
00537ACE  sub      ecx, edx
00537AD0  mov      dword ptr [r11 + 8], ecx
00537AD4  mov      eax, ecx
00537AD6  ret      
00537AD7  lea      ecx, [r9 + rdx]
00537ADB  mov      eax, r9d
00537ADE  mov      dword ptr [r10], ecx
00537AE1  ret      
00537AE2  xor      eax, eax
00537AE4  ret      
```
