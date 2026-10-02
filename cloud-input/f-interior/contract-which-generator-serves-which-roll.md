# F-interior pack: `21-RNG-And-Determinism/CONTRACT-which-generator-serves-which-roll.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/contract-which-generator-serves-which-roll.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 6075e3017	SWE2-FRONTIER for FABLE: pass-22 unattributed appends - the other 11 PUBLISHABLE pages (batch 2, 21/). OPUS read these before packing.

## 004005E0 (108 B, extent 004005E0-0040064C)

Page context: " route. LCG inliner '003185D0' and call-site consumer '00239210' both advance '022C256C' identically (I3); MT consumers '0025ABA0(2)'/'0038DB10'/'00389670' advance only '02EB3870'; presentation PRNG '004005E0' advances only '01EF93E8'; the gfxMT seeder chain '0015BCF0'→'0018D680'→'0018D740'→'0018EE20' writes only '01F7F600' (I1 natively, and I5 resolved — the graphics MT state IS fixed); negative control '0025ABA0(1)' touches no generat"

```
004005E0  cmp      dword ptr [rip + 0x1ed8b51], 0  ; -> 022D9138
004005E7  movss    xmm1, dword ptr [rip + 0x18eb5b9]  ; -> 01CEBBA8 [f32 1]
004005EF  jne      0x4005f6  ; -> 004005F6
004005F1  movaps   xmm0, xmm1
004005F4  jmp      0x400625  ; -> 00400625
004005F6  mov      eax, dword ptr [rip + 0x1af8dec]  ; -> 01EF93E8 [f32 1]
004005FC  mov      ecx, eax
004005FE  shr      ecx, 0x12
00400601  xor      ecx, eax
00400603  and      eax, 0x3fffff
00400608  or       eax, 0x1fc00000
0040060D  shr      ecx, 4
00400610  add      eax, eax
00400612  and      ecx, 1
00400615  or       ecx, eax
00400617  mov      dword ptr [rip + 0x1af8dcb], ecx  ; -> 01EF93E8 [f32 1]
0040061D  movss    xmm0, dword ptr [rip + 0x1af8dc3]  ; -> 01EF93E8 [f32 1]
00400625  movss    dword ptr [rip + 0x1ed8cb3], xmm0  ; -> 022D92E0
0040062D  movups   xmm0, xmmword ptr [rip + 0x1ed8cac]  ; -> 022D92E0
00400634  movups   xmmword ptr [rip + 0x1ed8955], xmm0  ; -> 022D8F90
0040063B  movd     dword ptr [rsp + 8], xmm0
00400641  movss    xmm0, dword ptr [rsp + 8]
00400647  subss    xmm0, xmm1
0040064B  ret      
```
