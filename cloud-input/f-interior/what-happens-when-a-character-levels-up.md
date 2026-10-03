# F-interior pack: `13-Rewards-Progression-Economy/what-happens-when-a-character-levels-up.md`

Generated 2026-10-02 23:37 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/what-happens-when-a-character-levels-up.json`.

Functions: 5. Each is cited on the page only at its entry and is still in the F frontier.

## 00290610 (18 B, extent 00290610-00290622)

Page context: " callee the growth loop passes 'r12' into — is a five-byte thunk tail-jumping to '002905D0' ('0035D8C0'). '002905D0' (57 B) is a '[0209BE80]'-manager dispatch: the manager pointer loads ('002905D7', '00290610', '00290634', '00290688', '002906B0', '002906D4'), '002966E0' runs the bounded match ('002905FA'), '00273A20''s '== 1' result gates ('00290653'/'002906A7'), and the tail is '00296960' ('002906C5').  | member | role | interior | | -"

```
00290610  mov      rax, qword ptr [rip + 0x1e0b869]  ; -> 0209BE80
00290617  and      dword ptr [rax + 0x10f68], 0xffffdfff
00290621  ret      
```

## 003A72A0 (56 B, extent 003A72A0-003A72D8)

Page context: "pus 5.5, 2026-09-25, for UQ-136).**   - **The level-up hands its visual to that layer.** '002EACD0' calls '003B02A0', which builds the class-5 effect     record through '0024B270', whose own callees '003A72A0', '003A8000' and '003A8900' belong to Presentation.     '003B0660' loads 'c_all.efx' through the EFX loader '003EDAD0'. The record driver '0024B9B0' calls     Presentation's '003A74F0', '003A7050', '003A7300', '003A7EE0' and '003A9"

```
003A72A0  mov      qword ptr [rsp + 8], rdi
003A72A5  mov      rdi, qword ptr [rip + 0x2b17d04]  ; -> 02EBEFB0
003A72AC  xor      eax, eax
003A72AE  xor      edx, edx
003A72B0  mov      ecx, 0x10
003A72B5  rep stosq qword ptr [rdi], rax
003A72B8  mov      rax, qword ptr [rip + 0x2b17cf1]  ; -> 02EBEFB0
003A72BF  mov      rdi, qword ptr [rsp + 8]
003A72C4  mov      dword ptr [rax + 0x80], edx
003A72CA  mov      rax, qword ptr [rip + 0x2b17cdf]  ; -> 02EBEFB0
003A72D1  mov      dword ptr [rax + 0x84], edx
003A72D7  ret      
```

## 003A8000 (24 B, extent 003A8000-003A8018)

Page context: "6-09-25, for UQ-136).**   - **The level-up hands its visual to that layer.** '002EACD0' calls '003B02A0', which builds the class-5 effect     record through '0024B270', whose own callees '003A72A0', '003A8000' and '003A8900' belong to Presentation.     '003B0660' loads 'c_all.efx' through the EFX loader '003EDAD0'. The record driver '0024B9B0' calls     Presentation's '003A74F0', '003A7050', '003A7300', '003A7EE0' and '003A93F0'.   - **"

```
003A8000  mov      rax, qword ptr [rip + 0x2b16f91]  ; -> 02EBEF98
003A8007  xor      ecx, ecx
003A8009  mov      qword ptr [rax], rcx
003A800C  mov      rax, qword ptr [rip + 0x2b16f85]  ; -> 02EBEF98
003A8013  mov      qword ptr [rax + 8], rcx
003A8017  ret      
```

## 003A8900 (75 B, extent 003A8900-003A894B)

Page context: "-136).**   - **The level-up hands its visual to that layer.** '002EACD0' calls '003B02A0', which builds the class-5 effect     record through '0024B270', whose own callees '003A72A0', '003A8000' and '003A8900' belong to Presentation.     '003B0660' loads 'c_all.efx' through the EFX loader '003EDAD0'. The record driver '0024B9B0' calls     Presentation's '003A74F0', '003A7050', '003A7300', '003A7EE0' and '003A93F0'.   - **Everything else"

```
003A8900  mov      rax, qword ptr [rip + 0x2b16681]  ; -> 02EBEF88
003A8907  xor      ecx, ecx
003A8909  mov      qword ptr [rax + 8], rcx
003A890D  mov      rax, qword ptr [rip + 0x2b16674]  ; -> 02EBEF88
003A8914  mov      qword ptr [rax + 0x10], rcx
003A8918  mov      rax, qword ptr [rip + 0x2b16669]  ; -> 02EBEF88
003A891F  mov      dword ptr [rax], ecx
003A8921  mov      eax, 0x18
003A8926  nop      word ptr [rax + rax]
003A8930  mov      rcx, qword ptr [rip + 0x2b16651]  ; -> 02EBEF88
003A8937  mov      dword ptr [rax + rcx], 0xffffffff
003A893E  add      rax, 8
003A8942  cmp      rax, 0x118
003A8948  jl       0x3a8930  ; -> 003A8930
003A894A  ret      
```

## 0046F330 (62 B, extent 0046F330-0046F36E)

Page context: "0E600' resolution stays live; 'edx == 0' instead scans indices '0..0x1C' for the first dead slot - a found slot '0036A100's a fresh '0x320'-byte record, '0020E620'-publishes the handle into '+0x2C', '0046F330' initialises the record and '0046F290' binds it to the slot index; when all 29 slots are live it returns 0  Interior anchor '0033405C' (function '00334000').  '0046F290' (160 B) is the 192-entry id-table refresh '00334000' runs: ea"

```
0046F330  mov      qword ptr [rsp + 8], rbx
0046F335  push     rdi
0046F336  sub      rsp, 0x20
0046F33A  mov      dword ptr [rcx], 0xc0000000
0046F340  lea      rbx, [rcx + 0x20]
0046F344  mov      edi, 0xc0
0046F349  nop      dword ptr [rax]
0046F350  xor      ecx, ecx
0046F352  call     0x20e620  ; -> 0020E620 fn
0046F357  mov      dword ptr [rbx], eax
0046F359  lea      rbx, [rbx + 4]
0046F35D  sub      rdi, 1
0046F361  jne      0x46f350  ; -> 0046F350
0046F363  mov      rbx, qword ptr [rsp + 0x30]
0046F368  add      rsp, 0x20
0046F36C  pop      rdi
0046F36D  ret      
```
