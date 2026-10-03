# Homing pack: `17-Presentation-Rendering/Render-Command-List/the-ordered-render-command-list.md`

Generated 2026-10-03 15:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h14-the-ordered-render-command-list.json`.

Bodies: 4. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002E8C10 (88 B, extent 002E8C10-002E8C68)

Entered from (direct sites whose caller this page cites): `00347D90` + 0x1C (call; `00347D90` is cited on this page)
Other direct sites: none

Host context: "esult to '0016D6A0' and then tail-jumps with the same result at '00346750' + 0x1E | Interior anchor '00346759'; Interior anchor '00346762'; Interior anchor '00346767'; Interior anchor '0034676E' | | '00347D90' | 53 B | calls '00267E10(r9)' and then calls the function at '00347D90' + 0x1C and tail-jumps at '00347D90' + 0x30, both with ('rdx', that result) | Interior anchor '00347DA0'; Interior anchor '00347DAC'; Interior anchor '00347DB1"

```
002E8C10  test     rcx, rcx
002E8C13  je       0x2e8c67  ; -> 002E8C67
002E8C15  mov      rax, qword ptr [rcx + 0xc0]
002E8C1C  test     rax, rax
002E8C1F  je       0x2e8c67  ; -> 002E8C67
002E8C21  cmp      dword ptr [rax], -1
002E8C24  je       0x2e8c67  ; -> 002E8C67
002E8C26  movzx    ecx, word ptr [rax]
002E8C29  cmp      cx, -1
002E8C2D  je       0x2e8c67  ; -> 002E8C67
002E8C2F  movsx    rax, cx
002E8C33  imul     rcx, rax, 0x740
002E8C3A  add      rcx, qword ptr [rip + 0x1fde2e7]  ; -> 022C6F28
002E8C41  je       0x2e8c67  ; -> 002E8C67
002E8C43  cmp      dword ptr [rcx + 0x284], 0
002E8C4A  je       0x2e8c67  ; -> 002E8C67
002E8C4C  and      dword ptr [rcx + 0x304], 0xfffffff7
002E8C53  neg      edx
002E8C55  sbb      eax, eax
002E8C57  and      eax, 8
002E8C5A  or       dword ptr [rcx + 0x304], eax
002E8C60  or       dword ptr [rcx + 0x290], 0x40
002E8C67  ret      
```

## 002ED200 (80 B, extent 002ED200-002ED250)

Entered from (direct sites whose caller this page cites): `00347D90` + 0x30 (jmp; `00347D90` is cited on this page)
Other direct sites: `003480F0` + 0x5 (jmp)

Host context: "esult to '0016D6A0' and then tail-jumps with the same result at '00346750' + 0x1E | Interior anchor '00346759'; Interior anchor '00346762'; Interior anchor '00346767'; Interior anchor '0034676E' | | '00347D90' | 53 B | calls '00267E10(r9)' and then calls the function at '00347D90' + 0x1C and tail-jumps at '00347D90' + 0x30, both with ('rdx', that result) | Interior anchor '00347DA0'; Interior anchor '00347DAC'; Interior anchor '00347DB1"

```
002ED200  test     rcx, rcx
002ED203  je       0x2ed24f  ; -> 002ED24F
002ED205  mov      rax, qword ptr [rcx + 0xc0]
002ED20C  test     rax, rax
002ED20F  je       0x2ed24f  ; -> 002ED24F
002ED211  cmp      dword ptr [rax], -1
002ED214  je       0x2ed24f  ; -> 002ED24F
002ED216  movzx    ecx, word ptr [rax]
002ED219  cmp      cx, -1
002ED21D  je       0x2ed24f  ; -> 002ED24F
002ED21F  movsx    rax, cx
002ED223  imul     rcx, rax, 0x740
002ED22A  add      rcx, qword ptr [rip + 0x1fd9cf7]  ; -> 022C6F28
002ED231  je       0x2ed24f  ; -> 002ED24F
002ED233  cmp      dword ptr [rcx + 0x284], 0
002ED23A  je       0x2ed24f  ; -> 002ED24F
002ED23C  and      byte ptr [rcx + 0xd2], 0xef
002ED243  neg      edx
002ED245  sbb      al, al
002ED247  and      al, 0x10
002ED249  or       byte ptr [rcx + 0xd2], al
002ED24F  ret      
```

## 0036E160 (63 B, extent 0036E160-0036E19F)

Entered from (direct sites whose caller this page cites): `00342010` + 0x28 (jmp; `00342010` is cited on this page)
Other direct sites: none

Host context: "3 with -1, then tail-jumps, at '003417C0' + 0x24, with (1, the '00267E10' result) | Interior anchor '003417C9'; Interior anchor '003417CE'; Interior anchor '003417D3'; Interior anchor '003417E4' | | '00342010' | 45 B | calls '00267E10(r9)' and tail-jumps with its result, at '00342010' + 0x1E when byte 'rdx+0x15' equals 3, otherwise at '00342010' + 0x28 | Interior anchor '0034201C'; Interior anchor '00342021'; Interior anchor '0034202E';"

```
0036E160  mov      eax, 0x3f
0036E165  test     ecx, ecx
0036E167  jns      0x36e182  ; -> 0036E182
0036E169  xor      ecx, ecx
0036E16B  cmp      ecx, eax
0036E16D  cmovg    ecx, eax
0036E170  movsxd   rax, ecx
0036E173  lea      rcx, [rip + 0x1f6b636]  ; -> 022D97B0
0036E17A  mov      dword ptr [rcx + rax*4], 0
0036E181  ret      
0036E182  cmp      ecx, eax
0036E184  cmovg    ecx, eax
0036E187  test     ecx, ecx
0036E189  jns      0x36e16b  ; -> 0036E16B
0036E18B  xor      ecx, ecx
0036E18D  movsxd   rax, ecx
0036E190  lea      rcx, [rip + 0x1f6b619]  ; -> 022D97B0
0036E197  mov      dword ptr [rcx + rax*4], 0
0036E19E  ret      
```

## 0036E1A0 (63 B, extent 0036E1A0-0036E1DF)

Entered from (direct sites whose caller this page cites): `00342010` + 0x1E (jmp; `00342010` is cited on this page)
Other direct sites: none

Host context: "3 with -1, then tail-jumps, at '003417C0' + 0x24, with (1, the '00267E10' result) | Interior anchor '003417C9'; Interior anchor '003417CE'; Interior anchor '003417D3'; Interior anchor '003417E4' | | '00342010' | 45 B | calls '00267E10(r9)' and tail-jumps with its result, at '00342010' + 0x1E when byte 'rdx+0x15' equals 3, otherwise at '00342010' + 0x28 | Interior anchor '0034201C'; Interior anchor '00342021'; Interior anchor '0034202E';"

```
0036E1A0  mov      eax, 0x3f
0036E1A5  test     ecx, ecx
0036E1A7  jns      0x36e1c2  ; -> 0036E1C2
0036E1A9  xor      ecx, ecx
0036E1AB  cmp      ecx, eax
0036E1AD  cmovg    ecx, eax
0036E1B0  movsxd   rax, ecx
0036E1B3  lea      rcx, [rip + 0x1f6b7f6]  ; -> 022D99B0
0036E1BA  mov      dword ptr [rcx + rax*4], 0
0036E1C1  ret      
0036E1C2  cmp      ecx, eax
0036E1C4  cmovg    ecx, eax
0036E1C7  test     ecx, ecx
0036E1C9  jns      0x36e1ab  ; -> 0036E1AB
0036E1CB  xor      ecx, ecx
0036E1CD  movsxd   rax, ecx
0036E1D0  lea      rcx, [rip + 0x1f6b7d9]  ; -> 022D99B0
0036E1D7  mov      dword ptr [rcx + rax*4], 0
0036E1DE  ret      
```
