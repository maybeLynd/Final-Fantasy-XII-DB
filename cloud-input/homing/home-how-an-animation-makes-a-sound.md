# Homing pack: `18-Audio/how-an-animation-makes-a-sound.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-how-an-animation-makes-a-sound.json`.

Bodies: 5. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00360670 (39 B, extent 00360670-00360697)

Entered from (direct sites whose caller this page cites): `002E9D90` + 0x28 (call; `002E9D90` is cited on this page)
Other direct sites: none

Host context: "ation     picker 0046C250 (1,090 B) with both jump tables read out of the image, its emission-point routine 0046C6E0 (438 B),     the descriptor build 0046C8F0 (626 B) and the actor-side sound lookup 002E9D90 (586 B) disassembled from the     authority image and read whole, 2026-09-20; the two commands then tallied over every animation container of an     extracted copy of the game, with totals that had to match the authored-command cen"

```
00360670  lea      rcx, [rip + 0x1f6b365]  ; -> 022CB9DC
00360677  lea      rdx, [rip + 0x1f6b366]  ; -> 022CB9E4
0036067E  nop      
00360680  cmp      dword ptr [rcx], 0
00360683  jne      0x360691  ; -> 00360691
00360685  add      rcx, 4
00360689  cmp      rcx, rdx
0036068C  jle      0x360680  ; -> 00360680
0036068E  xor      eax, eax
00360690  ret      
00360691  mov      eax, 1
00360696  ret      
```

## 0036EC50 (76 B, extent 0036EC50-0036EC9C)

Entered from (direct sites whose caller this page cites): `002E9D90` + 0x200 (call; `002E9D90` is cited on this page)
Other direct sites: none

Host context: "ation     picker 0046C250 (1,090 B) with both jump tables read out of the image, its emission-point routine 0046C6E0 (438 B),     the descriptor build 0046C8F0 (626 B) and the actor-side sound lookup 002E9D90 (586 B) disassembled from the     authority image and read whole, 2026-09-20; the two commands then tallied over every animation container of an     extracted copy of the game, with totals that had to match the authored-command cen"

```
0036EC50  cmp      ecx, -1
0036EC53  jne      0x36ec65  ; -> 0036EC65
0036EC55  xor      edx, edx
0036EC57  movsx    ecx, byte ptr [rdx + 1]
0036EC5B  cmp      byte ptr [rdx + 2], dl
0036EC5E  lea      eax, [rcx + 2]
0036EC61  cmove    eax, ecx
0036EC64  ret      
0036EC65  mov      eax, ecx
0036EC67  and      eax, 0xf
0036EC6A  test     cl, 0xf0
0036EC6D  lea      rcx, [rax + rax*2]
0036EC71  lea      rax, [rip - 0x24ec78]  ; -> 00120000 (image base)
0036EC78  lea      rdx, [rax + 0x21b9ae0]  ; image base + 0x21b9ae0 = 022D9AE0
0036EC7F  jne      0x36ec88  ; -> 0036EC88
0036EC81  lea      rdx, [rax + 0x21b9ab0]  ; image base + 0x21b9ab0 = 022D9AB0
0036EC88  cmp      byte ptr [rdx + rcx*8 + 2], 0
0036EC8D  lea      rdx, [rdx + rcx*8]
0036EC91  movsx    ecx, byte ptr [rdx + 1]
0036EC95  lea      eax, [rcx + 2]
0036EC98  cmove    eax, ecx
0036EC9B  ret      
```

## 003A0E80 (31 B, extent 003A0E80-003A0E9F)

Entered from (direct sites whose caller this page cites): `0046CC70` + 0x1AF (call; `0046CC70` is cited on this page)
Other direct sites: none

Host context: " evidence_tier: 1 verified_against:   exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8   method: the two command handlers 00520C50 and 00520D00, the emitter's play routine 0046CC70 (1,069 B), its variation     picker 0046C250 (1,090 B) with both jump tables read out of the image, its emission-point routine 0046C6E0 (438 B),     the descriptor build 0046C8F0 (626 B) and the actor-side sound lookup 002E9D90 (58"

```
003A0E80  mov      r8d, edx
003A0E83  test     ecx, ecx
003A0E85  je       0x3a0e96  ; -> 003A0E96
003A0E87  cmp      ecx, 1
003A0E8A  jne      0x3a0e9e  ; -> 003A0E9E
003A0E8C  xor      edx, edx
003A0E8E  mov      ecx, r8d
003A0E91  jmp      0x2df0f0  ; -> 002DF0F0 fn
003A0E96  mov      ecx, r8d
003A0E99  jmp      0x2df690  ; -> 002DF690 fn
003A0E9E  ret      
```

## 003A10F0 (11 B, extent 003A10F0-003A10FB)

Entered from (direct sites whose caller this page cites): `0046CC70` + 0x3E5 (call; `0046CC70` is cited on this page)
Other direct sites: none

Host context: " evidence_tier: 1 verified_against:   exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8   method: the two command handlers 00520C50 and 00520D00, the emitter's play routine 0046CC70 (1,069 B), its variation     picker 0046C250 (1,090 B) with both jump tables read out of the image, its emission-point routine 0046C6E0 (438 B),     the descriptor build 0046C8F0 (626 B) and the actor-side sound lookup 002E9D90 (58"

```
003A10F0  shr      ecx, 0x1e
003A10F3  not      ecx
003A10F5  and      ecx, 1
003A10F8  mov      eax, ecx
003A10FA  ret      
```

## 003E7CD0 (59 B, extent 003E7CD0-003E7D0B)

Entered from (direct sites whose caller this page cites): `0046CC70` + 0x11B (call; `0046CC70` is cited on this page)
Other direct sites: `003B0C50` + 0x5D (call)

Host context: " evidence_tier: 1 verified_against:   exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8   method: the two command handlers 00520C50 and 00520D00, the emitter's play routine 0046CC70 (1,069 B), its variation     picker 0046C250 (1,090 B) with both jump tables read out of the image, its emission-point routine 0046C6E0 (438 B),     the descriptor build 0046C8F0 (626 B) and the actor-side sound lookup 002E9D90 (58"

```
003E7CD0  xor      eax, eax
003E7CD2  mov      r8d, ecx
003E7CD5  cmp      byte ptr [rip + 0x2772096], al  ; -> 02B59D71
003E7CDB  jne      0x3e7d00  ; -> 003E7D00
003E7CDD  lea      rcx, [rip + 0x277209c]  ; -> 02B59D80
003E7CE4  cmp      word ptr [rcx], 0
003E7CE8  je       0x3e7cf0  ; -> 003E7CF0
003E7CEA  cmp      dword ptr [rcx + 4], r8d
003E7CEE  je       0x3e7d01  ; -> 003E7D01
003E7CF0  inc      eax
003E7CF2  add      rcx, 0x150
003E7CF9  cmp      eax, 0x20
003E7CFC  jb       0x3e7ce4  ; -> 003E7CE4
003E7CFE  xor      eax, eax
003E7D00  ret      
003E7D01  mov      eax, edx
003E7D03  mov      eax, dword ptr [rcx + rax*4 + 0xc0]
003E7D0A  ret      
```
