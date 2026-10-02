# F-interior pack: `17-Presentation-Rendering/Model-And-Motion-Formats/fcp-character-parameter-block.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/fcp-character-parameter-block.json`.

Functions: 22. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 29436f1ad	SWE2-DATA UQ-218 pass 18: band->@FMN binding, yaw sign, @FOR tail lists, @FDM desc +0x08 and the @FE; inbox mentions: FABLE.md). OPUS read these before packing.

## 00265240 (43 B, extent 00265240-0026526B)

Page context: "ects float ('002ECE50' → '003E6150') or integer ('002ECE80' → '003E6310' → '004FE2F0') reading, and a second jump table ('003205F0', '00320614') applies a scale: **multiply by the actor's y-scale** ('00265240' → 'movementState + 0x24', '00320570'–'0032057A'), divide by it ('00320560'–'0032056A'), or leave it. 'sel' is true for a unit whose stats record is kind 1 and whose definition's '+0x13' is not '0xFF' ('00239E3D'–'00239E5C').  | un"

```
00265240  movzx    eax, byte ptr [rcx + 3]
00265244  and      al, 0xe0
00265246  cmp      al, 0x60
00265248  jne      0x265268  ; -> 00265268
0026524A  mov      rcx, qword ptr [rcx + 0xb8]
00265251  mov      eax, dword ptr [rcx + 0x20]
00265254  mov      dword ptr [rdx], eax
00265256  mov      eax, dword ptr [rcx + 0x24]
00265259  mov      dword ptr [r8], eax
0026525C  mov      eax, dword ptr [rcx + 0x28]
0026525F  mov      dword ptr [r9], eax
00265262  mov      eax, 1
00265267  ret      
00265268  xor      eax, eax
0026526A  ret      
```

## 0026B2D0 (8 B, extent 0026B2D0-0026B2D8)

Page context: "8 (79 / 80 when 'FieldData_GetActiveFieldRecordBit15' holds) and hands them to '0026B2E0(actor, x, y)' ('002E2F8A'..'002E2F95'), which is also the tail of script verbs '0220 setradius' ('0033F890' → '0026B2D0') and '0221 setradius_221' ('0033FCD0'); and the getter '002E9660' (kind-3 gate, behind the 22-byte adapter '00263860') returns the pair's first value unchanged for verbs '02B1 getdefaultradiusw' / '02B2 getdefaultradiusd' ('003509"

```
0026B2D0  movaps   xmm2, xmm1
0026B2D3  jmp      0x26b2e0  ; -> 0026B2E0 fn
```

## 002E7DD0 (59 B, extent 002E7DD0-002E7E0B)

Page context: "| — | 0 / 0 |  **Other engine reads**, by id (file slot first, default slot in brackets):  | id | section · slot | read by | for | |---|---|---|---| | '0x9000707' / '0x9000101' | 9 · 7 (7) / 1 (1) | '002E7DD0(actor, which)' — 'which == 0' selects slot 7 | a scaled radius pair (party 0.1333 / monster 0.2667 against 0.1333) | | '0x9000808' / '0x9000202' | 9 · 8 / 2 | '002E7E10(actor, which)' | the pair 0.4 / 0.2 | | '0x9000606' / '0x90000"

```
002E7DD0  test     rcx, rcx
002E7DD3  je       0x2e7e07  ; -> 002E7E07
002E7DD5  mov      rax, qword ptr [rcx + 0xc0]
002E7DDC  test     rax, rax
002E7DDF  je       0x2e7e07  ; -> 002E7E07
002E7DE1  mov      ecx, dword ptr [rax]
002E7DE3  cmp      ecx, -1
002E7DE6  je       0x2e7e07  ; -> 002E7E07
002E7DE8  xor      eax, eax
002E7DEA  test     edx, edx
002E7DEC  cmovns   eax, edx
002E7DEF  test     eax, eax
002E7DF1  jne      0x2e7dfd  ; -> 002E7DFD
002E7DF3  mov      edx, 0x9000707
002E7DF8  jmp      0x3e6150  ; -> 003E6150 fn
002E7DFD  mov      edx, 0x9000101
002E7E02  jmp      0x3e6150  ; -> 003E6150 fn
002E7E07  xorps    xmm0, xmm0
002E7E0A  ret      
```

## 002E7E10 (59 B, extent 002E7E10-002E7E4B)

Page context: "000101' | 9 · 7 (7) / 1 (1) | '002E7DD0(actor, which)' — 'which == 0' selects slot 7 | a scaled radius pair (party 0.1333 / monster 0.2667 against 0.1333) | | '0x9000808' / '0x9000202' | 9 · 8 / 2 | '002E7E10(actor, which)' | the pair 0.4 / 0.2 | | '0x9000606' / '0x9000000' | 9 · 6 / 0 | '002E7E50(actor, which)' | the pair 0.1333 / 0.0667 | | '0x9000909' | 9 · 9 | '002E9B10' ('002E9B30') | a scaled angle | | '0x9001D1E' | 9 · 30 (29) | "

```
002E7E10  test     rcx, rcx
002E7E13  je       0x2e7e47  ; -> 002E7E47
002E7E15  mov      rax, qword ptr [rcx + 0xc0]
002E7E1C  test     rax, rax
002E7E1F  je       0x2e7e47  ; -> 002E7E47
002E7E21  mov      ecx, dword ptr [rax]
002E7E23  cmp      ecx, -1
002E7E26  je       0x2e7e47  ; -> 002E7E47
002E7E28  xor      eax, eax
002E7E2A  test     edx, edx
002E7E2C  cmovns   eax, edx
002E7E2F  test     eax, eax
002E7E31  jne      0x2e7e3d  ; -> 002E7E3D
002E7E33  mov      edx, 0x9000808
002E7E38  jmp      0x3e6150  ; -> 003E6150 fn
002E7E3D  mov      edx, 0x9000202
002E7E42  jmp      0x3e6150  ; -> 003E6150 fn
002E7E47  xorps    xmm0, xmm0
002E7E4A  ret      
```

## 002E9630 (39 B, extent 002E9630-002E9657)

Page context: "0.2 | | '0x9000606' / '0x9000000' | 9 · 6 / 0 | '002E7E50(actor, which)' | the pair 0.1333 / 0.0667 | | '0x9000909' | 9 · 9 | '002E9B10' ('002E9B30') | a scaled angle | | '0x9001D1E' | 9 · 30 (29) | '002E9630', 'CharacterRenderRecord_UpdateDistanceFadeAndCull' ('0042EBE7'), '0046C6E0' / '0046C8F0' / '0046CC70' (through '004FE270'), '0053AB50' ('0053AF7C', × record '+0x734') | a scaled height-like length — 1.7 in 217 files (124 distinct "

```
002E9630  test     rcx, rcx
002E9633  je       0x2e9653  ; -> 002E9653
002E9635  mov      rax, qword ptr [rcx + 0xc0]
002E963C  test     rax, rax
002E963F  je       0x2e9653  ; -> 002E9653
002E9641  cmp      dword ptr [rax], -1
002E9644  je       0x2e9653  ; -> 002E9653
002E9646  movzx    ecx, word ptr [rax]
002E9649  mov      edx, 0x9001d1e
002E964E  jmp      0x3e6150  ; -> 003E6150 fn
002E9653  xorps    xmm0, xmm0
002E9656  ret      
```

## 00342640 (163 B, extent 00342640-003426E3)

Page context: "14 (OPUS).  **Script_VM_Native_Bridge — CLIENT (SWE2-CONTRACT 2026-09-15, 18 edges).** Eighteen script-bridge bodies consult this page's parameter-block accessors: '002E28E0' is called by '003409F0'/'00342640'/ '00355210'/'0050D810', '002E5FD0' by '0050E6F0'/'0050E7B0', '002E7DD0'/'002E7E10'/'002E7E50' by the '0034D300'/'0034CB30'/'0034C7A0' family, '002E9B10' by '0034EFE0'/'003578B0'/'0050F6E0'/'0034E710'/ '0034F4F0', and '00377C20' by"

```
00342640  mov      qword ptr [rsp + 8], rbx
00342645  push     rdi
00342646  sub      rsp, 0x30
0034264A  cmp      byte ptr [r8 + 8], 0
0034264F  mov      rdi, r8
00342652  mov      rbx, rdx
00342655  je       0x3426c6  ; -> 003426C6
00342657  movzx    eax, word ptr [r8 + 0xa]
0034265C  cmp      ax, 1
00342660  jne      0x342685  ; -> 00342685
00342662  xor      edx, edx
00342664  mov      rcx, rbx
00342667  lea      r8d, [rdx + 1]
0034266B  call     0x2ebc90  ; -> 002EBC90 fn
00342670  mov      ecx, dword ptr [rdi + 4]
00342673  call     0x2e97c0  ; -> 002E97C0 fn
00342678  mov      rdx, rax
0034267B  mov      rcx, rbx
0034267E  call     0x2e28e0  ; -> 002E28E0 fn
00342683  jmp      0x3426be  ; -> 003426BE
00342685  cmp      ax, 3
00342689  jne      0x3426c6  ; -> 003426C6
0034268B  mov      edx, 3
00342690  mov      rcx, rbx
00342693  lea      r8d, [rdx - 2]
00342697  call     0x2ebc90  ; -> 002EBC90 fn
0034269C  mov      ecx, dword ptr [rdi + 4]
0034269F  call     0x2e97c0  ; -> 002E97C0 fn
003426A4  xor      r8d, r8d
003426A7  mov      dword ptr [rsp + 0x20], 0
003426AF  mov      r9, rax
003426B2  mov      rcx, rbx
003426B5  lea      edx, [r8 + 4]
003426B9  call     0x2e3110  ; -> 002E3110 fn
003426BE  mov      rcx, rbx
003426C1  call     0x2eac90  ; -> 002EAC90 fn
003426C6  mov      rcx, rbx
003426C9  call     0x265950  ; -> 00265950 fn
003426CE  movaps   xmm1, xmm0
003426D1  mov      rcx, rbx
003426D4  mov      rbx, qword ptr [rsp + 0x40]
003426D9  add      rsp, 0x30
003426DD  pop      rdi
003426DE  jmp      0x25b470  ; -> 0025B470 fn
```

## 0034EFE0 (122 B, extent 0034EFE0-0034F05A)

Page context: "2E28E0' is called by '003409F0'/'00342640'/ '00355210'/'0050D810', '002E5FD0' by '0050E6F0'/'0050E7B0', '002E7DD0'/'002E7E10'/'002E7E50' by the '0034D300'/'0034CB30'/'0034C7A0' family, '002E9B10' by '0034EFE0'/'003578B0'/'0050F6E0'/'0034E710'/ '0034F4F0', and '00377C20' by '00352FA0'/'00355680'/'00344740'/'003537D0'. The script VM reads FCP character parameters through these getters — the same shape as the InputGameplay and Rewards rows"

```
0034EFE0  mov      qword ptr [rsp + 8], rbx
0034EFE5  mov      qword ptr [rsp + 0x10], rbp
0034EFEA  mov      qword ptr [rsp + 0x18], rsi
0034EFEF  push     rdi
0034EFF0  sub      rsp, 0x20
0034EFF4  mov      rbp, rdx
0034EFF7  mov      rdi, rcx
0034EFFA  mov      rcx, rbp
0034EFFD  xor      edx, edx
0034EFFF  mov      rbx, r9
0034F002  mov      rsi, r8
0034F005  call     0x26a1a0  ; -> 0026A1A0 fn
0034F00A  mov      r9, rbx
0034F00D  mov      r8, rsi
0034F010  mov      rdx, rbp
0034F013  mov      rcx, rdi
0034F016  call     0x34be50  ; -> 0034BE50 fn
0034F01B  mov      rcx, rbp
0034F01E  call     0x2e9b10  ; -> 002E9B10 fn
0034F023  movaps   xmm1, xmm0
0034F026  mov      rcx, rbp
0034F029  call     0x26ac70  ; -> 0026AC70 fn
0034F02E  mov      r8, qword ptr [rsi]
0034F031  mov      rdx, rbp
0034F034  mov      ecx, 1
0034F039  call     0x2ec510  ; -> 002EC510 fn
0034F03E  mov      rcx, rbp
0034F041  mov      rbx, qword ptr [rsp + 0x30]
0034F046  mov      rbp, qword ptr [rsp + 0x38]
0034F04B  mov      rsi, qword ptr [rsp + 0x40]
0034F050  add      rsp, 0x20
0034F054  pop      rdi
0034F055  jmp      0x2690d0  ; -> 002690D0 fn
```

## 0034F4F0 (125 B, extent 0034F4F0-0034F56D)

Page context: "00355210'/'0050D810', '002E5FD0' by '0050E6F0'/'0050E7B0', '002E7DD0'/'002E7E10'/'002E7E50' by the '0034D300'/'0034CB30'/'0034C7A0' family, '002E9B10' by '0034EFE0'/'003578B0'/'0050F6E0'/'0034E710'/ '0034F4F0', and '00377C20' by '00352FA0'/'00355680'/'00344740'/'003537D0'. The script VM reads FCP character parameters through these getters — the same shape as the InputGameplay and Rewards rows above: the layer consults the block, the blo"

```
0034F4F0  mov      qword ptr [rsp + 8], rbx
0034F4F5  mov      qword ptr [rsp + 0x10], rbp
0034F4FA  mov      qword ptr [rsp + 0x18], rsi
0034F4FF  push     rdi
0034F500  sub      rsp, 0x20
0034F504  mov      rbp, rdx
0034F507  mov      rdi, rcx
0034F50A  mov      rcx, rbp
0034F50D  mov      edx, 1
0034F512  mov      rbx, r9
0034F515  mov      rsi, r8
0034F518  call     0x26a1a0  ; -> 0026A1A0 fn
0034F51D  mov      r9, rbx
0034F520  mov      r8, rsi
0034F523  mov      rdx, rbp
0034F526  mov      rcx, rdi
0034F529  call     0x34be50  ; -> 0034BE50 fn
0034F52E  mov      rcx, rbp
0034F531  call     0x2e9b10  ; -> 002E9B10 fn
0034F536  movaps   xmm1, xmm0
0034F539  mov      rcx, rbp
0034F53C  call     0x26ac70  ; -> 0026AC70 fn
0034F541  mov      r8, qword ptr [rsi]
0034F544  mov      rdx, rbp
0034F547  mov      ecx, 1
0034F54C  call     0x2ec510  ; -> 002EC510 fn
0034F551  mov      rcx, rbp
0034F554  mov      rbx, qword ptr [rsp + 0x30]
0034F559  mov      rbp, qword ptr [rsp + 0x38]
0034F55E  mov      rsi, qword ptr [rsp + 0x40]
0034F563  add      rsp, 0x20
0034F567  pop      rdi
0034F568  jmp      0x2690d0  ; -> 002690D0 fn
```

## 003E4700 (41 B, extent 003E4700-003E4729)

Page context: "der inventory (SWE2-DATA)  | word | section | readers (all instruments: E8/E9 + absolute-dword/qword scans of the whole image) | |---|---|---| | '+0x02' | 1 | '003E56A0' + wrapper '003E6F70'; inline '003E4700', '003E4B71', '003E561B', '003E592F', '003E5A0F', '003E5EFB', '003E60B3' | | '+0x04' | 2 | '003E4B40' — returns the raw word; only callers '0041FE24' / '0041FE3B' (the copy-source computation above) | | '+0x06' | 3 | '003E5CD0' + t"

```
003E4700  mov      rdx, qword ptr [rcx + 0x400]
003E4707  test     rdx, rdx
003E470A  je       0x3e4720  ; -> 003E4720
003E470C  movzx    eax, word ptr [rdx + 2]
003E4710  add      eax, edx
003E4712  movsxd   rcx, eax
003E4715  je       0x3e4720  ; -> 003E4720
003E4717  movss    xmm0, dword ptr [rcx + 0x144]
003E471F  ret      
003E4720  movss    xmm0, dword ptr [rip + 0x1907480]  ; -> 01CEBBA8 [f32 1]
003E4728  ret      
```

## 003E4B40 (12 B, extent 003E4B40-003E4B4C)

Page context: "is the attachment table" at the end of this page.*** ***SUPERSEDED 2026-09-21 (SWE2-DATA) — every offset word now has an inventoried reader fate, and "section 18" was a misread.** '+0x04' is read by '003E4B40', whose only callers ('0041FE24'/'0041FE3B' in the initialiser) compute 'payload + word[2]' as the source of 'memcpy(FTR_tail, src, dword[+0x24])' ('003729B7') — **section 2 is live**: it is appended verbatim into the '@FTR' alloca"

```
003E4B40  mov      rax, qword ptr [rcx + 0x400]
003E4B47  movzx    eax, word ptr [rax + 4]
003E4B4B  ret      
```

## 003E56E0 (25 B, extent 003E56E0-003E56F9)

Page context: "ot 45 | '004256E0' ('00425A28'–'00425BA9') | four bytes packed in slot 48 | | '0x2902032B', '0x6003082D', '0x62060A2D' | dword 9 · 43; bytes 0 and 2 of slot 45 | '00384E50' ('00384EBC', '00384F0A'), '003E56E0' | — |  **Version stamp.** '+0x32' is the only stamp; no shipped id's 'VV' exceeds '0x08', so the file value wins everywhere a section exists. **Nothing normalises the block on load** — '002EDBD0' stores a pointer and the getters r"

```
003E56E0  mov      rcx, qword ptr [rcx + 0x400]
003E56E7  test     rcx, rcx
003E56EA  je       0x3e56f6  ; -> 003E56F6
003E56EC  mov      edx, 0x62060a2d
003E56F1  jmp      0x4fe2f0  ; -> 004FE2F0 fn
003E56F6  xor      eax, eax
003E56F8  ret      
```

## 003E5C90 (49 B, extent 003E5C90-003E5CC1)

Page context: "50' + inline '003E6A2D', '003E7464' | | '+0x10' | 8 | '003E6CF0' / '003E6D10', both called only by the initialiser's copy at '0041F5CE' / '0041F5D9' | | '+0x12' | 9 | '003E56C0' + inline '003E58B0', '003E5C90', '003E5EA0' | | '+0x14' | 10 | '003E6E40', sole caller '003AF3B0' | | '+0x16'..'+0x22' | 11–17 | never present in any block |  ### Section 2 — the '@FTR' tail blob, '1,066 / 1,066' blocks (SWE2-DATA)  '''struct FcpSection2 base=se"

```
003E5C90  mov      rdx, qword ptr [rcx + 0x400]
003E5C97  test     rdx, rdx
003E5C9A  je       0x3e5cb8  ; -> 003E5CB8
003E5C9C  movzx    eax, word ptr [rdx + 0x12]
003E5CA0  test     ax, ax
003E5CA3  je       0x3e5cb8  ; -> 003E5CB8
003E5CA5  movzx    eax, ax
003E5CA8  add      eax, edx
003E5CAA  movsxd   rcx, eax
003E5CAD  je       0x3e5cb8  ; -> 003E5CB8
003E5CAF  movss    xmm0, dword ptr [rcx + 0xa8]
003E5CB7  ret      
003E5CB8  movss    xmm0, dword ptr [rip + 0x92bafc]  ; -> 00D117BC [f32 0.10472]
003E5CC0  ret      
```

## 003E5EA0 (41 B, extent 003E5EA0-003E5EC9)

Page context: " '003E6A2D', '003E7464' | | '+0x10' | 8 | '003E6CF0' / '003E6D10', both called only by the initialiser's copy at '0041F5CE' / '0041F5D9' | | '+0x12' | 9 | '003E56C0' + inline '003E58B0', '003E5C90', '003E5EA0' | | '+0x14' | 10 | '003E6E40', sole caller '003AF3B0' | | '+0x16'..'+0x22' | 11–17 | never present in any block |  ### Section 2 — the '@FTR' tail blob, '1,066 / 1,066' blocks (SWE2-DATA)  '''struct FcpSection2 base=section2 size="

```
003E5EA0  mov      rdx, qword ptr [rcx + 0x400]
003E5EA7  test     rdx, rdx
003E5EAA  je       0x3e5ec6  ; -> 003E5EC6
003E5EAC  movzx    eax, word ptr [rdx + 0x12]
003E5EB0  test     ax, ax
003E5EB3  je       0x3e5ec6  ; -> 003E5EC6
003E5EB5  movzx    eax, ax
003E5EB8  add      eax, edx
003E5EBA  movsxd   rcx, eax
003E5EBD  je       0x3e5ec6  ; -> 003E5EC6
003E5EBF  mov      eax, dword ptr [rcx + 0xa4]
003E5EC5  ret      
003E5EC6  xor      eax, eax
003E5EC8  ret      
```

## 003E66D0 (63 B, extent 003E66D0-003E670F)

Page context: "12 record](../../_index/candidates/swe2struct-ddres-b12-0930/README.md). The lead is check C3: the copy's       offset is the record's '+0x300', read by four accessors, '003E6680' (from '00425DC0'), '003E66D0' (from '00425E10'),       '003E6710' (from '0041FCF0' and '00520140') and '003E6D40' (from the LOD updates '0042CBF0' and '0042D050', and from       '00421280' and '004213E0').)*       *(2026-09-30, SWE2-STRUCT for OPUS, residue 3:"

```
003E66D0  push     rbx
003E66D2  sub      rsp, 0x20
003E66D6  cmp      dword ptr [rcx + 0x300], 0
003E66DD  mov      rbx, rcx
003E66E0  jbe      0x3e6709  ; -> 003E6709
003E66E2  mov      ecx, dword ptr [rcx + 0x2fc]
003E66E8  call     0x20e600  ; -> 0020E600 fn
003E66ED  mov      rcx, rax
003E66F0  call     0x3ab7f0  ; -> 003AB7F0 fn
003E66F5  add      eax, dword ptr [rbx + 0x300]
003E66FB  mov      ecx, eax
003E66FD  je       0x3e6709  ; -> 003E6709
003E66FF  add      rsp, 0x20
003E6703  pop      rbx
003E6704  jmp      0x51d310  ; -> 0051D310 fn
003E6709  add      rsp, 0x20
003E670D  pop      rbx
003E670E  ret      
```

## 003E6710 (88 B, extent 003E6710-003E6768)

Page context: "we2struct-ddres-b12-0930/README.md). The lead is check C3: the copy's       offset is the record's '+0x300', read by four accessors, '003E6680' (from '00425DC0'), '003E66D0' (from '00425E10'),       '003E6710' (from '0041FCF0' and '00520140') and '003E6D40' (from the LOD updates '0042CBF0' and '0042D050', and from       '00421280' and '004213E0').)*       *(2026-09-30, SWE2-STRUCT for OPUS, residue 3: answered. The copy's readers are th"

```
003E6710  mov      qword ptr [rsp + 8], rbx
003E6715  push     rdi
003E6716  sub      rsp, 0x20
003E671A  cmp      dword ptr [rcx + 0x300], 0
003E6721  mov      edi, edx
003E6723  mov      rbx, rcx
003E6726  jbe      0x3e675d  ; -> 003E675D
003E6728  mov      ecx, dword ptr [rcx + 0x2fc]
003E672E  call     0x20e600  ; -> 0020E600 fn
003E6733  mov      rcx, rax
003E6736  call     0x3ab7f0  ; -> 003AB7F0 fn
003E673B  add      eax, dword ptr [rbx + 0x300]
003E6741  mov      ecx, eax
003E6743  je       0x3e675d  ; -> 003E675D
003E6745  test     edi, edi
003E6747  je       0x3e6758  ; -> 003E6758
003E6749  mov      rbx, qword ptr [rsp + 0x30]
003E674E  add      rsp, 0x20
003E6752  pop      rdi
003E6753  jmp      0x51db60  ; -> 0051DB60 fn
003E6758  call     0x519720  ; -> 00519720 fn
003E675D  mov      rbx, qword ptr [rsp + 0x30]
003E6762  add      rsp, 0x20
003E6766  pop      rdi
003E6767  ret      
```

## 003E6D10 (44 B, extent 003E6D10-003E6D3C)

Page context: "elves and add a section-offset word. Direct readers, by header word: '+2' (section 1), **'+6' (section 3: '003E5CD0', 32 B, read whole)**, '+8' (section 4), '+0xE' (section 7), **'+0x10' (section 8: '003E6D10', 44 B, read whole - the section's first word x '0x1D0' + '0x10', a byte size)**, '+0x12' (section 9) and '+0x14' (section 10). None for '+4' (section 2) or '+0xC' (section 6). **Instrument:** a displacement sweep for loads of reco"

```
003E6D10  mov      rdx, qword ptr [rcx + 0x400]
003E6D17  test     rdx, rdx
003E6D1A  je       0x3e6d39  ; -> 003E6D39
003E6D1C  movzx    eax, word ptr [rdx + 0x10]
003E6D20  test     ax, ax
003E6D23  je       0x3e6d39  ; -> 003E6D39
003E6D25  movzx    eax, ax
003E6D28  add      eax, edx
003E6D2A  cdqe     
003E6D2C  movzx    ecx, word ptr [rax]
003E6D2F  imul     eax, ecx, 0x1d0
003E6D35  add      eax, 0x10
003E6D38  ret      
003E6D39  xor      eax, eax
003E6D3B  ret      
```

## 00409240 (15 B, extent 00409240-0040924F)

Page context: "-09-18 (FABLE):* '0041F340(record, modelId, name, flag, base, fcpLen)' finds the '@FTR' entry by the record's model name ('00409660' with tag '0x52544640', '0041F3A1' / '0041F40B'), sizes it through '00409240' and '003712E0' — '(dword +0xC × 0x149 + word +0x38)' sixteen-bit units, plus the FCP length it is handed (UQ-220) — and is called by the render-record initialiser '0041FCF0' once for the model ('0041FF7C') and once per further ent"

```
00409240  cmp      dword ptr [rcx + 4], 2
00409244  je       0x40924a  ; -> 0040924A
00409246  mov      eax, dword ptr [rcx + 0xc]
00409249  ret      
0040924A  movzx    eax, word ptr [rcx + 0x30]
0040924E  ret      
```

## 00425E10 (87 B, extent 00425E10-00425E67)

Page context: "_index/candidates/swe2struct-ddres-b12-0930/README.md). The lead is check C3: the copy's       offset is the record's '+0x300', read by four accessors, '003E6680' (from '00425DC0'), '003E66D0' (from '00425E10'),       '003E6710' (from '0041FCF0' and '00520140') and '003E6D40' (from the LOD updates '0042CBF0' and '0042D050', and from       '00421280' and '004213E0').)*       *(2026-09-30, SWE2-STRUCT for OPUS, residue 3: answered. The co"

```
00425E10  sub      rsp, 0x28
00425E14  mov      rdx, qword ptr [rip + 0x1ea110d]  ; -> 022C6F28
00425E1B  mov      eax, dword ptr [rdx + 0x48800]
00425E21  cmp      eax, -1
00425E24  je       0x425e62  ; -> 00425E62
00425E26  mov      qword ptr [rsp + 0x20], rbx
00425E2B  nop      dword ptr [rax + rax]
00425E30  movsxd   rcx, eax
00425E33  imul     rbx, rcx, 0x740
00425E3A  lea      rcx, [rbx + rdx]
00425E3E  test     byte ptr [rcx + 0x290], 2
00425E45  jne      0x425e53  ; -> 00425E53
00425E47  call     0x3e66d0  ; -> 003E66D0 fn
00425E4C  mov      rdx, qword ptr [rip + 0x1ea10d5]  ; -> 022C6F28
00425E53  movsx    eax, word ptr [rbx + rdx + 4]
00425E58  cmp      eax, -1
00425E5B  jne      0x425e30  ; -> 00425E30
00425E5D  mov      rbx, qword ptr [rsp + 0x20]
00425E62  add      rsp, 0x28
00425E66  ret      
```

## 0050D810 (73 B, extent 0050D810-0050D859)

Page context: "_Native_Bridge — CLIENT (SWE2-CONTRACT 2026-09-15, 18 edges).** Eighteen script-bridge bodies consult this page's parameter-block accessors: '002E28E0' is called by '003409F0'/'00342640'/ '00355210'/'0050D810', '002E5FD0' by '0050E6F0'/'0050E7B0', '002E7DD0'/'002E7E10'/'002E7E50' by the '0034D300'/'0034CB30'/'0034C7A0' family, '002E9B10' by '0034EFE0'/'003578B0'/'0050F6E0'/'0034E710'/ '0034F4F0', and '00377C20' by '00352FA0'/'00355680'/"

```
0050D810  mov      qword ptr [rsp + 8], rbx
0050D815  push     rdi
0050D816  sub      rsp, 0x20
0050D81A  mov      rdi, rdx
0050D81D  mov      rbx, r8
0050D820  xor      edx, edx
0050D822  mov      rcx, rdi
0050D825  lea      r8d, [rdx + 1]
0050D829  call     0x2ebc90  ; -> 002EBC90 fn
0050D82E  mov      rdx, qword ptr [rbx + 8]
0050D832  mov      rcx, rdi
0050D835  call     0x2e28e0  ; -> 002E28E0 fn
0050D83A  mov      rcx, rdi
0050D83D  call     0x2eac90  ; -> 002EAC90 fn
0050D842  mov      edx, 0x1001
0050D847  mov      rcx, rdi
0050D84A  mov      rbx, qword ptr [rsp + 0x30]
0050D84F  add      rsp, 0x20
0050D853  pop      rdi
0050D854  jmp      0x2eb330  ; -> 002EB330 fn
```

## 0051CDE0 (999 B, extent 0051CDE0-0051D1C7)

Page context: "x1A0' through the bone   that '+0xC' names on the owning render record (header '+8'; '00421D70', '004220F0'), counts '+0' up to 16, and rewrites   the history rows '+0xA0'..'+0x19F' and '+0x10'.* - *'0051CDE0', the draw, from '00425DC0' (the after-emission stage of the pass dispatcher '00332440'). While '+6' is set   and bit 1 is clear, it submits at once, through '00540C70' (whose only caller it is), the template packet '02AEC180'   an"

```
0051CDE0  mov      qword ptr [rsp + 0x10], rbx
0051CDE5  mov      qword ptr [rsp + 0x18], rsi
0051CDEA  mov      qword ptr [rsp + 0x20], rdi
0051CDEF  push     rbp
0051CDF0  push     r14
0051CDF2  push     r15
0051CDF4  lea      rbp, [rsp - 0x260]
0051CDFC  sub      rsp, 0x360
0051CE03  mov      rax, qword ptr [rip + 0x1a27a26]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0051CE0A  xor      rax, rsp
0051CE0D  mov      qword ptr [rbp + 0x250], rax
0051CE14  mov      rbx, rcx
0051CE17  mov      r14d, 2
0051CE1D  mov      ecx, r14d
0051CE20  call     0x1fbd80  ; -> 001FBD80 fn
0051CE25  call     0x39d3f0  ; -> 0039D3F0 fn
0051CE2A  movzx    edi, word ptr [rbx + 2]
0051CE2E  xor      esi, esi
0051CE30  movzx    eax, word ptr [rbx + 8]
0051CE34  add      rdi, rbx
0051CE37  cmp      ax, -1
0051CE3B  jne      0x51ce42  ; -> 0051CE42
0051CE3D  mov      r15d, esi
0051CE40  jmp      0x51ce5f  ; -> 0051CE5F
0051CE42  movsx    rax, ax
0051CE46  imul     r15, rax, 0x740
0051CE4D  add      r15, qword ptr [rip + 0x1daa0d4]  ; -> 022C6F28
0051CE54  cmp      dword ptr [r15 + 0x284], esi
0051CE5B  cmove    r15, rsi
0051CE5F  cmp      byte ptr [rbx + 6], 0
0051CE63  je       0x51d19b  ; -> 0051D19B
0051CE69  movzx    eax, byte ptr [rbx + 7]
0051CE6D  or       eax, dword ptr [rip + 0x278b5b5]  ; -> 02CA8428
0051CE73  test     r14b, al
0051CE76  jne      0x51d19b  ; -> 0051D19B
0051CE7C  lea      rax, [rsp + 0x20]
0051CE81  lea      rcx, [rip + 0x25cf2f8]  ; -> 02AEC180
0051CE88  nop      dword ptr [rax + rax]
0051CE90  lea      rax, [rax + 0x80]
0051CE97  movups   xmm0, xmmword ptr [rcx]
0051CE9A  movups   xmm1, xmmword ptr [rcx + 0x10]
0051CE9E  lea      rcx, [rcx + 0x80]
0051CEA5  movups   xmmword ptr [rax - 0x80], xmm0
0051CEA9  movups   xmm0, xmmword ptr [rcx - 0x60]
0051CEAD  movups   xmmword ptr [rax - 0x70], xmm1
0051CEB1  movups   xmm1, xmmword ptr [rcx - 0x50]
0051CEB5  movups   xmmword ptr [rax - 0x60], xmm0
0051CEB9  movups   xmm0, xmmword ptr [rcx - 0x40]
0051CEBD  movups   xmmword ptr [rax - 0x50], xmm1
0051CEC1  movups   xmm1, xmmword ptr [rcx - 0x30]
0051CEC5  movups   xmmword ptr [rax - 0x40], xmm0
0051CEC9  movups   xmm0, xmmword ptr [rcx - 0x20]
0051CECD  movups   xmmword ptr [rax - 0x30], xmm1
0051CED1  movups   xmm1, xmmword ptr [rcx - 0x10]
0051CED5  movups   xmmword ptr [rax - 0x20], xmm0
0051CED9  movups   xmmword ptr [rax - 0x10], xmm1
0051CEDD  sub      r14, 1
0051CEE1  jne      0x51ce90  ; -> 0051CE90
0051CEE3  movups   xmm0, xmmword ptr [rcx]
0051CEE6  xor      r8d, r8d
0051CEE9  lea      edx, [r14 + 0x15]
0051CEED  movups   xmm1, xmmword ptr [rcx + 0x10]
0051CEF1  movups   xmmword ptr [rax], xmm0
0051CEF4  movups   xmm0, xmmword ptr [rcx + 0x20]
0051CEF8  movups   xmmword ptr [rax + 0x10], xmm1
0051CEFC  movups   xmm1, xmmword ptr [rcx + 0x30]
0051CF00  movups   xmmword ptr [rax + 0x20], xmm0
0051CF04  movups   xmm0, xmmword ptr [rcx + 0x40]
0051CF08  movzx    ecx, byte ptr [rip + 0x1a0e43e]  ; -> 01F2B34D [u8 0x00]
0051CF0F  movups   xmmword ptr [rax + 0x30], xmm1
0051CF13  shl      rcx, 0x15
0051CF17  movaps   xmm1, xmmword ptr [rip + 0x25d0f62]  ; -> 02AEDE80
0051CF1E  movups   xmmword ptr [rax + 0x40], xmm0
0051CF22  movzx    eax, byte ptr [rip + 0x1a0e423]  ; -> 01F2B34C [u8 0x06]
0051CF29  movaps   xmm0, xmmword ptr [rip + 0x25d0f40]  ; -> 02AEDE70
0051CF30  or       rcx, rax
0051CF33  movzx    eax, byte ptr [rip + 0x1a0e411]  ; -> 01F2B34B [u8 0x06]
0051CF3A  shl      rcx, 4
0051CF3E  or       rcx, rax
0051CF41  movaps   xmmword ptr [rsp + 0x70], xmm1
0051CF46  movaps   xmm1, xmmword ptr [rip + 0x25d0f53]  ; -> 02AEDEA0
0051CF4D  movzx    eax, byte ptr [rip + 0x1a0e3f6]  ; -> 01F2B34A [u8 0x13]
0051CF54  shl      rcx, 6
0051CF58  or       rcx, rax
0051CF5B  movaps   xmmword ptr [rbp - 0x70], xmm1
0051CF5F  movaps   xmm1, xmmword ptr [rip + 0x25d0dda]  ; -> 02AEDD40
0051CF66  movzx    eax, byte ptr [rip + 0x1a0e3dc]  ; -> 01F2B349 [u8 0x01]
0051CF6D  shl      rcx, 6
0051CF71  or       rcx, rax
0051CF74  movaps   xmmword ptr [rbp - 0x50], xmm1
0051CF78  movaps   xmm1, xmmword ptr [rip + 0x25d0de1]  ; -> 02AEDD60
0051CF7F  movabs   rax, 0x2005c00400002a00
0051CF89  movaps   xmmword ptr [rsp + 0x60], xmm0
0051CF8E  movaps   xmm0, xmmword ptr [rip + 0x25d0efb]  ; -> 02AEDE90
0051CF95  movaps   xmmword ptr [rbp - 0x30], xmm1
0051CF99  shl      rcx, 0xe
0051CF9D  movaps   xmmword ptr [rbp - 0x80], xmm0
0051CFA1  or       rcx, rax
0051CFA4  movaps   xmm0, xmmword ptr [rip + 0x25d0d85]  ; -> 02AEDD30
0051CFAB  shufps   xmm1, xmm1, 0xaa
0051CFAF  addss    xmm1, dword ptr [rip + 0x3f7745]  ; -> 009146FC [f32 30000]
0051CFB7  movaps   xmmword ptr [rbp - 0x60], xmm0
0051CFBB  movaps   xmm0, xmmword ptr [rip + 0x25d0d8e]  ; -> 02AEDD50
0051CFC2  mov      qword ptr [rbp + 0x40], rcx
0051CFC6  lea      rcx, [rsp + 0x20]
0051CFCB  movaps   xmmword ptr [rbp - 0x40], xmm0
0051CFCF  movss    dword ptr [rbp - 0x28], xmm1
0051CFD4  call     0x540c70  ; -> 00540C70 fn
0051CFD9  lea      rax, [rbp + 0x70]
0051CFDD  lea      rcx, [rip + 0x25cf2ec]  ; -> 02AEC2D0
0051CFE4  lea      edx, [r14 + 3]
0051CFE8  nop      dword ptr [rax + rax]
0051CFF0  lea      rax, [rax + 0x80]
0051CFF7  movups   xmm0, xmmword ptr [rcx]
0051CFFA  movups   xmm1, xmmword ptr [rcx + 0x10]
0051CFFE  lea      rcx, [rcx + 0x80]
0051D005  movups   xmmword ptr [rax - 0x80], xmm0
0051D009  movups   xmm0, xmmword ptr [rcx - 0x60]
0051D00D  movups   xmmword ptr [rax - 0x70], xmm1
0051D011  movups   xmm1, xmmword ptr [rcx - 0x50]
0051D015  movups   xmmword ptr [rax - 0x60], xmm0
0051D019  movups   xmm0, xmmword ptr [rcx - 0x40]
0051D01D  movups   xmmword ptr [rax - 0x50], xmm1
0051D021  movups   xmm1, xmmword ptr [rcx - 0x30]
0051D025  movups   xmmword ptr [rax - 0x40], xmm0
0051D029  movups   xmm0, xmmword ptr [rcx - 0x20]
0051D02D  movups   xmmword ptr [rax - 0x30], xmm1
0051D031  movups   xmm1, xmmword ptr [rcx - 0x10]
0051D035  movups   xmmword ptr [rax - 0x20], xmm0
0051D039  movups   xmmword ptr [rax - 0x10], xmm1
0051D03D  sub      rdx, 1
0051D041  jne      0x51cff0  ; -> 0051CFF0
0051D043  movups   xmm0, xmmword ptr [rcx]
0051D046  movups   xmm1, xmmword ptr [rcx + 0x10]
0051D04A  movups   xmmword ptr [rax], xmm0
0051D04D  movups   xmm0, xmmword ptr [rcx + 0x20]
0051D051  movups   xmmword ptr [rax + 0x10], xmm1
0051D055  movups   xmm1, xmmword ptr [rcx + 0x30]
0051D059  movups   xmmword ptr [rax + 0x20], xmm0
0051D05D  movups   xmm0, xmmword ptr [rcx + 0x40]
0051D061  movups   xmmword ptr [rax + 0x30], xmm1
0051D065  movups   xmm1, xmmword ptr [rcx + 0x50]
0051D069  movups   xmmword ptr [rax + 0x40], xmm0
0051D06D  movups   xmmword ptr [rax + 0x50], xmm1
0051D071  cmp      si, word ptr [rbx]
0051D074  jae      0x51d196  ; -> 0051D196
0051D07A  nop      word ptr [rax + rax]
0051D080  mov      rax, rdi
0051D083  lea      rcx, [rbp + 0x80]
0051D08A  mov      edx, 3
0051D08F  nop      
0051D090  lea      rcx, [rcx + 0x80]
0051D097  movups   xmm0, xmmword ptr [rax]
0051D09A  lea      rax, [rax + 0x80]
0051D0A1  movups   xmmword ptr [rcx - 0x80], xmm0
0051D0A5  movups   xmm1, xmmword ptr [rax - 0x70]
0051D0A9  movups   xmmword ptr [rcx - 0x70], xmm1
0051D0AD  movups   xmm0, xmmword ptr [rax - 0x60]
0051D0B1  movups   xmmword ptr [rcx - 0x60], xmm0
0051D0B5  movups   xmm1, xmmword ptr [rax - 0x50]
0051D0B9  movups   xmmword ptr [rcx - 0x50], xmm1
0051D0BD  movups   xmm0, xmmword ptr [rax - 0x40]
0051D0C1  movups   xmmword ptr [rcx - 0x40], xmm0
0051D0C5  movups   xmm1, xmmword ptr [rax - 0x30]
0051D0C9  movups   xmmword ptr [rcx - 0x30], xmm1
0051D0CD  movups   xmm0, xmmword ptr [rax - 0x20]
0051D0D1  movups   xmmword ptr [rcx - 0x20], xmm0
0051D0D5  movups   xmm1, xmmword ptr [rax - 0x10]
0051D0D9  movups   xmmword ptr [rcx - 0x10], xmm1
0051D0DD  sub      rdx, 1
0051D0E1  jne      0x51d090  ; -> 0051D090
0051D0E3  movups   xmm0, xmmword ptr [rax]
0051D0E6  movups   xmmword ptr [rcx], xmm0
0051D0E9  movups   xmm1, xmmword ptr [rax + 0x10]
0051D0ED  movups   xmmword ptr [rcx + 0x10], xmm1
0051D0F1  mov      rcx, r15
0051D0F4  call     0x3e5770  ; -> 003E5770 fn
0051D0F9  movss    xmm1, dword ptr [rbp + 0xac]
0051D101  mov      rcx, r15
0051D104  mulss    xmm1, xmm0
0051D108  movss    dword ptr [rbp + 0xac], xmm1
0051D110  call     0x3e5770  ; -> 003E5770 fn
0051D115  movss    xmm1, dword ptr [rbp + 0xcc]
0051D11D  mulss    xmm1, xmm0
0051D121  movss    xmm0, dword ptr [rbp + 0x90]
0051D129  movss    dword ptr [rbp + 0xcc], xmm1
0051D131  mulss    xmm0, dword ptr [rdi + 0x1c0]
0051D139  movss    dword ptr [rbp + 0x90], xmm0
0051D141  call     0x1edda0  ; -> 001EDDA0 fn
0051D146  movss    xmm0, dword ptr [rbx + 0xc]
0051D14B  cvtps2pd xmm0, xmm0
0051D14E  test     eax, eax
0051D150  jne      0x51d157  ; -> 0051D157
0051D152  call     0x861f5c  ; -> 00861F5C fn
0051D157  movss    xmm1, dword ptr [rbp + 0x94]
0051D15F  lea      rcx, [rbp + 0x70]
0051D163  cvtps2pd xmm1, xmm1
0051D166  xor      r8d, r8d
0051D169  lea      edx, [r8 + 0x1e]
0051D16D  mulsd    xmm1, xmm0
0051D171  cvtpd2ps xmm0, xmm1
0051D175  movss    dword ptr [rbp + 0x94], xmm0
0051D17D  call     0x540c70  ; -> 00540C70 fn
0051D182  movzx    eax, word ptr [rbx]
0051D185  inc      esi
0051D187  add      rdi, 0x1d0
0051D18E  cmp      esi, eax
0051D190  jb       0x51d080  ; -> 0051D080
0051D196  call     0x1fbe50  ; -> 001FBE50 fn
0051D19B  mov      rcx, qword ptr [rbp + 0x250]
0051D1A2  xor      rcx, rsp
0051D1A5  call     0x808c40  ; -> 00808C40 fn
0051D1AA  lea      r11, [rsp + 0x360]
0051D1B2  mov      rbx, qword ptr [r11 + 0x28]
0051D1B6  mov      rsi, qword ptr [r11 + 0x30]
0051D1BA  mov      rdi, qword ptr [r11 + 0x38]
0051D1BE  mov      rsp, r11
0051D1C1  pop      r15
0051D1C3  pop      r14
0051D1C5  pop      rbp
0051D1C6  ret      
```

## 0051D1D0 (78 B, extent 0051D1D0-0051D21E)

Page context: " with the record's first '0x1A0' bytes spliced in. The values are scaled by the   render record's fade product '003E5770' ('+0x260' x '+0x160' x '+0x26C'), by record '+0x1C0' and by header '+0xC'.   '0051D1D0' first binds the two resources that '0051D220' builds once from the image block '01F2B340'.* - *'0051DB60' and '00519720', on and off, from '003E6710'. The promoter path '0041FCF0' passes 1. Command '0x1F''s   handler '00520140' pa"

```
0051D1D0  sub      rsp, 0x28
0051D1D4  xor      edx, edx
0051D1D6  lea      rcx, [rip + 0x1b47c53]  ; -> 02064E30
0051D1DD  mov      r8d, 0x4000
0051D1E3  call     0x861ec0  ; -> 00861EC0 fn
0051D1E8  mov      ecx, 3
0051D1ED  call     0x258ee0  ; -> 00258EE0 fn
0051D1F2  mov      rdx, qword ptr [rip + 0x278b237]  ; -> 02CA8430
0051D1F9  xor      r8d, r8d
0051D1FC  mov      ecx, 0x2a00
0051D201  call     0x2d7e00  ; -> 002D7E00 fn
0051D206  mov      rdx, qword ptr [rip + 0x278b22b]  ; -> 02CA8438
0051D20D  xor      r8d, r8d
0051D210  mov      ecx, 0x2e00
0051D215  add      rsp, 0x28
0051D219  jmp      0x2d7e00  ; -> 002D7E00 fn
```

## 0051DB60 (127 B, extent 0051DB60-0051DBDF)

Page context: "duct '003E5770' ('+0x260' x '+0x160' x '+0x26C'), by record '+0x1C0' and by header '+0xC'.   '0051D1D0' first binds the two resources that '0051D220' builds once from the image block '01F2B340'.* - *'0051DB60' and '00519720', on and off, from '003E6710'. The promoter path '0041FCF0' passes 1. Command '0x1F''s   handler '00520140' passes its word, and no shipped motion authors that command. "On" resets every record ('+0' = 0,   '+0x10' ="

```
0051DB60  mov      qword ptr [rsp + 8], rbx
0051DB65  mov      qword ptr [rsp + 0x10], rbp
0051DB6A  mov      qword ptr [rsp + 0x18], rsi
0051DB6F  push     rdi
0051DB70  sub      rsp, 0x20
0051DB74  movzx    ebx, word ptr [rcx + 2]
0051DB78  xor      ebp, ebp
0051DB7A  add      ebx, ecx
0051DB7C  mov      word ptr [rcx + 6], 1
0051DB82  mov      rdi, rcx
0051DB85  mov      esi, ebp
0051DB87  cmp      bp, word ptr [rcx]
0051DB8A  jae      0x51dbca  ; -> 0051DBCA
0051DB8C  nop      dword ptr [rax]
0051DB90  lea      rcx, [rbx + 0xa0]
0051DB97  mov      dword ptr [rbx + 0x14], 0x3f800000
0051DB9E  xor      edx, edx
0051DBA0  mov      dword ptr [rbx], ebp
0051DBA2  mov      r8d, 0x100
0051DBA8  mov      dword ptr [rbx + 0x1c4], 1
0051DBB2  mov      dword ptr [rbx + 0x10], ebp
0051DBB5  call     0x861ec0  ; -> 00861EC0 fn
0051DBBA  movzx    eax, word ptr [rdi]
0051DBBD  lea      rbx, [rbx + 0x1d0]
0051DBC4  inc      esi
0051DBC6  cmp      esi, eax
0051DBC8  jb       0x51db90  ; -> 0051DB90
0051DBCA  mov      rbx, qword ptr [rsp + 0x30]
0051DBCF  mov      rbp, qword ptr [rsp + 0x38]
0051DBD4  mov      rsi, qword ptr [rsp + 0x40]
0051DBD9  add      rsp, 0x20
0051DBDD  pop      rdi
0051DBDE  ret      
```
