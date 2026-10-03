# Homing pack: `16-UI/Dynamic-Geometry-Instances/dyngeo-instance-family.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-dyngeo-instance-family.json`.

Bodies: 4. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00623EB0 (69 B, extent 00623EB0-00623EF5)

Entered from (direct sites whose caller this page cites): `0062A0A0` + 0x45D (call; `0062A0A0` is cited on this page)
Other direct sites: none

Host context: "23FA0' (67 B) is the fifth member of the inline-or-heap getter family '00620F60'/'00622BA0' drive: '+0x30' count under 'btr 0x1f', 'edx' bound-check, 0x58-stride records on '+0x38', returns '+0x10'. '0062A0A0' and '006C8CA0' call it for the dyngeo records. Interior anchor '00623FC2' (the '+0x10' fetch).  '0061D180' (221 B) is the flag-masked resource bind '006C8CA0'/'006CA8D0' call: bit 0 of 'r8d' binds '+0x168' (or '+0x170' when '+0x9C"

```
00623EB0  mov      eax, dword ptr [rcx + 0x18]
00623EB3  btr      eax, 0x1f
00623EB7  mov      r8d, edx
00623EBA  cmp      edx, eax
00623EBC  jae      0x623ef0  ; -> 00623EF0
00623EBE  mov      eax, dword ptr [rcx + 0x18]
00623EC1  btr      eax, 0x1f
00623EC5  cmp      eax, 1
00623EC8  jbe      0x623ed9  ; -> 00623ED9
00623ECA  mov      rcx, qword ptr [rcx + 0x20]
00623ECE  mov      eax, r8d
00623ED1  add      rax, rax
00623ED4  mov      rax, qword ptr [rcx + rax*8]
00623ED8  ret      
00623ED9  add      rcx, 0x20
00623EDD  xor      edx, edx
00623EDF  test     eax, eax
00623EE1  mov      rax, r8
00623EE4  cmove    rcx, rdx
00623EE8  add      rax, rax
00623EEB  mov      rax, qword ptr [rcx + rax*8]
00623EEF  ret      
00623EF0  xor      edx, edx
00623EF2  mov      eax, edx
00623EF4  ret      
```

## 00624040 (73 B, extent 00624040-00624089)

Entered from (direct sites whose caller this page cites): `0062A0A0` + 0x276 (call; `0062A0A0` is cited on this page)
Other direct sites: none

Host context: "23FA0' (67 B) is the fifth member of the inline-or-heap getter family '00620F60'/'00622BA0' drive: '+0x30' count under 'btr 0x1f', 'edx' bound-check, 0x58-stride records on '+0x38', returns '+0x10'. '0062A0A0' and '006C8CA0' call it for the dyngeo records. Interior anchor '00623FC2' (the '+0x10' fetch).  '0061D180' (221 B) is the flag-masked resource bind '006C8CA0'/'006CA8D0' call: bit 0 of 'r8d' binds '+0x168' (or '+0x170' when '+0x9C"

```
00624040  mov      eax, dword ptr [rcx + 0x30]
00624043  btr      eax, 0x1f
00624047  mov      r8d, edx
0062404A  cmp      edx, eax
0062404C  jae      0x624084  ; -> 00624084
0062404E  mov      eax, dword ptr [rcx + 0x30]
00624051  btr      eax, 0x1f
00624055  cmp      eax, 1
00624058  jbe      0x62406b  ; -> 0062406B
0062405A  mov      rcx, qword ptr [rcx + 0x38]
0062405E  mov      eax, r8d
00624061  shl      rax, 6
00624065  mov      rax, qword ptr [rax + rcx + 8]
0062406A  ret      
0062406B  add      rcx, 0x38
0062406F  xor      edx, edx
00624071  test     eax, eax
00624073  mov      rax, r8
00624076  cmove    rcx, rdx
0062407A  shl      rax, 6
0062407E  mov      rax, qword ptr [rax + rcx + 8]
00624083  ret      
00624084  xor      edx, edx
00624086  mov      eax, edx
00624088  ret      
```

## 00624690 (71 B, extent 00624690-006246D7)

Entered from (direct sites whose caller this page cites): `0062A0A0` + 0x363 (call; `0062A0A0` is cited on this page); `0062A0A0` + 0x4AA (call; `0062A0A0` is cited on this page)
Other direct sites: none

Host context: "23FA0' (67 B) is the fifth member of the inline-or-heap getter family '00620F60'/'00622BA0' drive: '+0x30' count under 'btr 0x1f', 'edx' bound-check, 0x58-stride records on '+0x38', returns '+0x10'. '0062A0A0' and '006C8CA0' call it for the dyngeo records. Interior anchor '00623FC2' (the '+0x10' fetch).  '0061D180' (221 B) is the flag-masked resource bind '006C8CA0'/'006CA8D0' call: bit 0 of 'r8d' binds '+0x168' (or '+0x170' when '+0x9C" / "23FA0' (67 B) is the fifth member of the inline-or-heap getter family '00620F60'/'00622BA0' drive: '+0x30' count under 'btr 0x1f', 'edx' bound-check, 0x58-stride records on '+0x38', returns '+0x10'. '0062A0A0' and '006C8CA0' call it for the dyngeo records. Interior anchor '00623FC2' (the '+0x10' fetch).  '0061D180' (221 B) is the flag-masked resource bind '006C8CA0'/'006CA8D0' call: bit 0 of 'r8d' binds '+0x168' (or '+0x170' when '+0x9C"

```
00624690  mov      eax, dword ptr [rcx + 0x20]
00624693  btr      eax, 0x1f
00624697  mov      r8d, edx
0062469A  cmp      edx, eax
0062469C  jae      0x6246d4  ; -> 006246D4
0062469E  test     byte ptr [rcx + 0x74], 1
006246A2  je       0x6246d4  ; -> 006246D4
006246A4  mov      eax, dword ptr [rcx + 0x20]
006246A7  btr      eax, 0x1f
006246AB  cmp      eax, 1
006246AE  jbe      0x6246be  ; -> 006246BE
006246B0  mov      rdx, qword ptr [rcx + 0x28]
006246B4  lea      rax, [r8 + r8*8]
006246B8  mov      rax, qword ptr [rdx + rax*8 + 8]
006246BD  ret      
006246BE  lea      rdx, [rcx + 0x28]
006246C2  xor      ecx, ecx
006246C4  test     eax, eax
006246C6  lea      rax, [r8 + r8*8]
006246CA  cmove    rdx, rcx
006246CE  mov      rax, qword ptr [rdx + rax*8 + 8]
006246D3  ret      
006246D4  xor      eax, eax
006246D6  ret      
```

## 006246E0 (71 B, extent 006246E0-00624727)

Entered from (direct sites whose caller this page cites): `0062A0A0` + 0x56D (call; `0062A0A0` is cited on this page)
Other direct sites: none

Host context: "23FA0' (67 B) is the fifth member of the inline-or-heap getter family '00620F60'/'00622BA0' drive: '+0x30' count under 'btr 0x1f', 'edx' bound-check, 0x58-stride records on '+0x38', returns '+0x10'. '0062A0A0' and '006C8CA0' call it for the dyngeo records. Interior anchor '00623FC2' (the '+0x10' fetch).  '0061D180' (221 B) is the flag-masked resource bind '006C8CA0'/'006CA8D0' call: bit 0 of 'r8d' binds '+0x168' (or '+0x170' when '+0x9C"

```
006246E0  mov      eax, dword ptr [rcx + 0x18]
006246E3  btr      eax, 0x1f
006246E7  mov      r8d, edx
006246EA  cmp      edx, eax
006246EC  jae      0x624724  ; -> 00624724
006246EE  test     byte ptr [rcx + 0x6c], 1
006246F2  je       0x624724  ; -> 00624724
006246F4  mov      eax, dword ptr [rcx + 0x18]
006246F7  btr      eax, 0x1f
006246FB  cmp      eax, 1
006246FE  jbe      0x62470e  ; -> 0062470E
00624700  mov      rdx, qword ptr [rcx + 0x20]
00624704  lea      rax, [r8 + r8*8]
00624708  mov      rax, qword ptr [rdx + rax*8 + 8]
0062470D  ret      
0062470E  lea      rdx, [rcx + 0x20]
00624712  xor      ecx, ecx
00624714  test     eax, eax
00624716  lea      rax, [r8 + r8*8]
0062471A  cmove    rdx, rcx
0062471E  mov      rax, qword ptr [rdx + rax*8 + 8]
00624723  ret      
00624724  xor      eax, eax
00624726  ret      
```
