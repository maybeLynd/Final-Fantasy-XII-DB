# F-interior pack: `25-EBP-Script-Container/Sections/section-002-text.md`

Generated 2026-10-03 02:49 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/section-002-text.json`.

Functions: 2. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 01c2429f6	SWE2-CONTRACT: pass-22 debt batch B - 47 Script-VM, Resource, EBP and PKFL pages' cross-subsystem ne; inbox mentions: ASSIGNMENTS.md, repos-3f.md, repos-4b.md, repos-c9.md, repos-d6.md). OPUS read these before packing.

## 002E1D50 (52 B, extent 002E1D50-002E1D84)

Page context: "00265680' is called by '00279E20'; '002E09A0' calls '00254B50'. ## SWE2-EC7-46 update (2026-09-19) - '0050EAB0'  '0050EAB0' (232 B) is a body - '002640C0'/'00264D60'/'002673A0'/'00267E10'/'002E16B0'/'002E1D50'/'002E1D90'. Interior anchor '0050EAD5' (a '002640C0' call).  ## SWE2-EC7-48 update (2026-09-19) - '0033F950'  '0033F950' (205 B) is a body - '00267E10'/'002E1D90'/'002E1E40'/'002E1E70'/'002E1EA0'/'002E1F80'/'002E1FD0'. Interior an"

```
002E1D50  test     ecx, ecx
002E1D52  jns      0x2e1d58  ; -> 002E1D58
002E1D54  xor      ecx, ecx
002E1D56  jmp      0x2e1d62  ; -> 002E1D62
002E1D58  mov      eax, 7
002E1D5D  cmp      ecx, eax
002E1D5F  cmovg    ecx, eax
002E1D62  movsxd   rax, ecx
002E1D65  imul     rcx, rax, 0x68
002E1D69  lea      rax, [rip + 0x1e7d490]  ; -> 0215F200
002E1D70  mov      byte ptr [rcx + rax + 0x3b], 1
002E1D75  mov      dword ptr [rcx + rax + 0x24], edx
002E1D79  mov      dword ptr [rcx + rax + 0x28], r8d
002E1D7E  mov      byte ptr [rcx + rax + 0x39], r9b
002E1D83  ret      
```

## 002E1FD0 (63 B, extent 002E1FD0-002E200F)

Page context: "0'. Interior anchor '0050EAD5' (a '002640C0' call).  ## SWE2-EC7-48 update (2026-09-19) - '0033F950'  '0033F950' (205 B) is a body - '00267E10'/'002E1D90'/'002E1E40'/'002E1E70'/'002E1EA0'/'002E1F80'/'002E1FD0'. Interior anchor '0033F96E' (a '00267E10' call).  ## SWE2-EC7-62 update (2026-09-19) - '002E1EA0'  '002E1EA0' (146 B) is a call-free 'edx'-countdown dispatch - arms 1/2/3/4 each 'movsxd' index x'0x68' into the '0215F23D' table. In"

```
002E1FD0  mov      eax, 7
002E1FD5  test     ecx, ecx
002E1FD7  jns      0x2e1ff2  ; -> 002E1FF2
002E1FD9  xor      ecx, ecx
002E1FDB  cmp      ecx, eax
002E1FDD  cmovg    ecx, eax
002E1FE0  movsxd   rax, ecx
002E1FE3  imul     rcx, rax, 0x68
002E1FE7  lea      rax, [rip + 0x1e7d254]  ; -> 0215F242
002E1FEE  mov      byte ptr [rcx + rax], dl
002E1FF1  ret      
002E1FF2  cmp      ecx, eax
002E1FF4  cmovg    ecx, eax
002E1FF7  test     ecx, ecx
002E1FF9  jns      0x2e1fdb  ; -> 002E1FDB
002E1FFB  xor      ecx, ecx
002E1FFD  movsxd   rax, ecx
002E2000  imul     rcx, rax, 0x68
002E2004  lea      rax, [rip + 0x1e7d237]  ; -> 0215F242
002E200B  mov      byte ptr [rcx + rax], dl
002E200E  ret      
```
