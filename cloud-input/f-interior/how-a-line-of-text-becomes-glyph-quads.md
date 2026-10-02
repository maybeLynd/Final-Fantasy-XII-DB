# F-interior pack: `99-Unresolved-Residual/Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md`

Generated 2026-10-02 09:51 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/how-a-line-of-text-becomes-glyph-quads.json`.

Functions: 10. Each is cited on the page only at its entry and is still in the F frontier.

## 00267BB0 (102 B, extent 00267BB0-00267C16)

Page context: "(1)'). Its only caller         is '0032F966' inside a three-way kind dispatch — selector '5', '13', '14'         each pass a different **resolver-thunk function pointer** as 'r8'         ('00267930'/'00267BB0'/'00267C20'; each thunk does 'ecx = 5'/'0xD'/'0xE'         → '0036B200'/'0036C1D0' — the kind re-selected inside), 'rdx' = the         loaded payload, 'ecx' = slot. 'r8 == 0' in the bind falls back to a         static default targe"

```
00267BB0  mov      qword ptr [rsp + 8], rbx
00267BB5  push     rdi
00267BB6  sub      rsp, 0x20
00267BBA  mov      edi, ecx
00267BBC  mov      ecx, 0xd
00267BC1  call     0x36b200  ; -> 0036B200 fn
00267BC6  mov      edx, 5
00267BCB  lea      ecx, [rdx + 8]
00267BCE  test     eax, eax
00267BD0  jne      0x267bd4  ; -> 00267BD4
00267BD2  mov      ecx, edx
00267BD4  call     0x36c1d0  ; -> 0036C1D0 fn
00267BD9  lea      rcx, [rip + 0x6adb08]  ; -> 009156E8 [str "..\..\katano\ateldecode.c"]
00267BE0  call     0x36c750  ; -> 0036C750 fn
00267BE5  mov      ecx, edi
00267BE7  mov      rbx, rax
00267BEA  call     0x36a100  ; -> 0036A100 fn
00267BEF  mov      rcx, rax
00267BF2  mov      r8d, 0x16c1
00267BF8  mov      rdx, rbx
00267BFB  call     0x36c660  ; -> 0036C660 fn
00267C00  mov      rbx, rax
00267C03  call     0x36c140  ; -> 0036C140 fn
00267C08  mov      rax, rbx
00267C0B  mov      rbx, qword ptr [rsp + 0x30]
00267C10  add      rsp, 0x20
00267C14  pop      rdi
00267C15  ret      
```

## 00267C20 (102 B, extent 00267C20-00267C86)

Page context: "only caller         is '0032F966' inside a three-way kind dispatch — selector '5', '13', '14'         each pass a different **resolver-thunk function pointer** as 'r8'         ('00267930'/'00267BB0'/'00267C20'; each thunk does 'ecx = 5'/'0xD'/'0xE'         → '0036B200'/'0036C1D0' — the kind re-selected inside), 'rdx' = the         loaded payload, 'ecx' = slot. 'r8 == 0' in the bind falls back to a         static default target ('lea' in"

```
00267C20  mov      qword ptr [rsp + 8], rbx
00267C25  push     rdi
00267C26  sub      rsp, 0x20
00267C2A  mov      edi, ecx
00267C2C  mov      ecx, 0xe
00267C31  call     0x36b200  ; -> 0036B200 fn
00267C36  mov      edx, 5
00267C3B  lea      ecx, [rdx + 9]
00267C3E  test     eax, eax
00267C40  jne      0x267c44  ; -> 00267C44
00267C42  mov      ecx, edx
00267C44  call     0x36c1d0  ; -> 0036C1D0 fn
00267C49  lea      rcx, [rip + 0x6ada98]  ; -> 009156E8 [str "..\..\katano\ateldecode.c"]
00267C50  call     0x36c750  ; -> 0036C750 fn
00267C55  mov      ecx, edi
00267C57  mov      rbx, rax
00267C5A  call     0x36a100  ; -> 0036A100 fn
00267C5F  mov      rcx, rax
00267C62  mov      r8d, 0x16e6
00267C68  mov      rdx, rbx
00267C6B  call     0x36c660  ; -> 0036C660 fn
00267C70  mov      rbx, rax
00267C73  call     0x36c140  ; -> 0036C140 fn
00267C78  mov      rax, rbx
00267C7B  mov      rbx, qword ptr [rsp + 0x30]
00267C80  add      rsp, 0x20
00267C84  pop      rdi
00267C85  ret      
```

## 00271380 (39 B, extent 00271380-002713A7)

Page context: "body, after it stores '0209CC40'/'0209CC48' — the text-state globals this page documents | | '003F1E90' | '003F1F9F' | 'movss xmm0 → 01DFE0BC' — first of five writes to the same float global between '00271380' calls | | '002D28E0' | '002D2BB7' | 'call 00249EE0' after '0017F650'/'0017FA10'/'0017FB00' — a glyph-run helper chain ending in '00243E90' |  *(Pass 22 adjacency, 2026-09-14: the quad walk touches three outside layers — **rewards*"

```
00271380  sub      rsp, 0x28
00271384  call     0x3588b0  ; -> 003588B0 fn
00271389  test     rax, rax
0027138C  jne      0x27139b  ; -> 0027139B
0027138E  movss    xmm0, dword ptr [rip + 0x1a7a906]  ; -> 01CEBC9C [f32 -1]
00271396  add      rsp, 0x28
0027139A  ret      
0027139B  mov      rcx, rax
0027139E  add      rsp, 0x28
002713A2  jmp      0x263940  ; -> 00263940 fn
```

## 002A35B0 (66 B, extent 002A35B0-002A35F2)

Page context: "of a       non-zero value is yet cited. "Authored resource data" is the plausible reading, not       yet the proven one.) '002A3250' has zero 'call' sites — it is tail-called       ('jmp') only from '002A35B0', which is called only from '002E1933' inside **'002E16B0' —       the message-window opener** ('002E16DF': 'SetBank2048(actor+0x102, 1)' — 'UQ-138''s       opener). '002E16B0(actor, slot=edx, stream=r8, resref=r9)' stores 'r9'/'r8"

```
002A35B0  mov      qword ptr [rsp + 8], rbx
002A35B5  push     rdi
002A35B6  sub      rsp, 0x20
002A35BA  mov      rdi, r8
002A35BD  mov      qword ptr [rcx + 0x1a8], rdx
002A35C4  mov      rbx, rcx
002A35C7  call     0x39c480  ; -> 0039C480 fn
002A35CC  test     rax, rax
002A35CF  je       0x2a35dd  ; -> 002A35DD
002A35D1  call     0x39c480  ; -> 0039C480 fn
002A35D6  mov      qword ptr [rbx + 0x1a8], rax
002A35DD  mov      rdx, rdi
002A35E0  mov      rcx, rbx
002A35E3  mov      rbx, qword ptr [rsp + 0x30]
002A35E8  add      rsp, 0x20
002A35EC  pop      rdi
002A35ED  jmp      0x2a3250  ; -> 002A3250 fn
```

## 002B2D90 (82 B, extent 002B2D90-002B2DE2)

Page context: "nce the caller is '002A1B00', and       the bytes '00364980' reads never existed as a literal: '002A1BD9' takes the buffer at       '[window + 0x3E0]', '002A1BD3' takes the index '[window + 0x154]', '002B2D90' walks to a slice,       and '00861EBA' copies that slice into the scratch buffer '0209CB90', which is what       '002A1CCA' hands on as 'r9'. **The first two bytes '00364980' compares are the first two bytes       of a run of the "

```
002B2D90  xor      r10d, r10d
002B2D93  xor      r11d, r11d
002B2D96  cmp      byte ptr [rcx], r10b
002B2D99  je       0x2b2dd4  ; -> 002B2DD4
002B2D9B  bt       edx, r10d
002B2D9F  jb       0x2b2da9  ; -> 002B2DA9
002B2DA1  cmp      r11d, r8d
002B2DA4  je       0x2b2dc2  ; -> 002B2DC2
002B2DA6  inc      r11d
002B2DA9  cmp      r10d, r9d
002B2DAC  je       0x2b2dd4  ; -> 002B2DD4
002B2DAE  movzx    eax, byte ptr [rcx]
002B2DB1  inc      r10d
002B2DB4  and      eax, 0x7f
002B2DB7  inc      rcx
002B2DBA  add      rcx, rax
002B2DBD  cmp      byte ptr [rcx], 0
002B2DC0  jmp      0x2b2d99  ; -> 002B2D99
002B2DC2  mov      rax, qword ptr [rsp + 0x28]
002B2DC7  movzx    edx, byte ptr [rcx]
002B2DCA  and      edx, 0x7f
002B2DCD  mov      dword ptr [rax], edx
002B2DCF  lea      rax, [rcx + 1]
002B2DD3  ret      
002B2DD4  mov      rax, qword ptr [rsp + 0x28]
002B2DD9  mov      dword ptr [rax], 0
002B2DDF  xor      eax, eax
002B2DE1  ret      
```

## 003666E0 (88 B, extent 003666E0-00366738)

Page context: "t cosmetic. The graphics hardware this engine still speaks to takes texture dimensions as **log2**, so a glyph cell has to be a power of two to be addressable at all. The routine that converts back, '003666E0', is a bit-scan that returns 'log2(n)' for power-of-two 'n' — and its result is written straight into the texture-descriptor command.  The glyph's pixels are then uploaded to a fixed address in graphics local memory ('0x3440'), whi"

```
003666E0  mov      eax, ecx
003666E2  mov      ecx, 0x3f
003666E7  add      eax, eax
003666E9  movsxd   r8, eax
003666EC  dec      r8
003666EF  mov      rax, r8
003666F2  sar      rax, 0x3f
003666F6  test     al, 1
003666F8  jne      0x366710  ; -> 00366710
003666FA  nop      word ptr [rax + rax]
00366700  test     ecx, ecx
00366702  jle      0x366710  ; -> 00366710
00366704  dec      ecx
00366706  mov      rax, r8
00366709  sar      rax, cl
0036670C  test     al, 1
0036670E  je       0x366700  ; -> 00366700
00366710  mov      rax, r8
00366713  mov      r9d, ecx
00366716  sar      rax, cl
00366719  test     al, 1
0036671B  je       0x366731  ; -> 00366731
0036671D  nop      dword ptr [rax]
00366720  test     ecx, ecx
00366722  jle      0x366731  ; -> 00366731
00366724  dec      ecx
00366726  mov      rdx, r8
00366729  sar      rdx, cl
0036672C  test     dl, 1
0036672F  jne      0x366720  ; -> 00366720
00366731  sub      r9d, ecx
00366734  mov      eax, r9d
00366737  ret      
```

## 003EA6B0 (43 B, extent 003EA6B0-003EA6DB)

Page context: "C8C0') calls 'WorldPersistence_ResetBanksForFieldTransition' ('0026DB30'); 'ActorSystem_InitializeManagerRuntime' ('0026CE60') calls 'BattleSystem_InitializeAreaState' ('002342F0'); '0032F430' calls '003EA6B0'; '003320D0' calls '003EAA00'; '003320E0' calls '003DFE60'; '00332100' calls '003DFDC0'; '00332110' calls '003DFE60'; '00378540' is called by '00377CC0'; '003EAA00' calls '003DCF10'; '003EAA00' is called by '003319D0'; '003F9720' c"

```
003EA6B0  sub      rsp, 0x28
003EA6B4  xorps    xmm0, xmm0
003EA6B7  mov      dword ptr [rip + 0x27739f7], 0xffffffff  ; -> 02B5E0B8
003EA6C1  xor      ecx, ecx
003EA6C3  movdqu   xmmword ptr [rip + 0x27739f5], xmm0  ; -> 02B5E0C0
003EA6CB  call     0x3dcf00  ; -> 003DCF00 fn
003EA6D0  xor      ecx, ecx
003EA6D2  add      rsp, 0x28
003EA6D6  jmp      0x3dcf10  ; -> 003DCF10 fn
```

## 003F7F50 (187 B, extent 003F7F50-003F800B)

Page context: "0027AD70',         billboard emit '0028A090', typed-list '00243860', label-gate         '002C64C0', record-field '002C8BC0', script-side dialog text         '0035C160', widget/frame paths '003EE420'/'003F7F50', menu-selection         '003EE8C0', settings arm '003F9720', map screens '004044D0' +         destination-label '00550A00', menu atlas '005528C0'/'005569F0', and         the confirm window '0057C480'. '002B3C30''s callers are     "

```
003F7F50  push     rdi
003F7F52  sub      rsp, 0x100
003F7F59  mov      rax, qword ptr [rip + 0x1b4c8d0]  ; -> 01F44830 [u64 0x00002B992DDFA232]
003F7F60  xor      rax, rsp
003F7F63  mov      qword ptr [rsp + 0xf0], rax
003F7F6B  cmp      dword ptr [rdx], 4
003F7F6E  mov      rdi, rcx
003F7F71  je       0x3f7f7a  ; -> 003F7F7A
003F7F73  call     0x5c5230  ; -> 005C5230 fn
003F7F78  jmp      0x3f7ff2  ; -> 003F7FF2
003F7F7A  mov      rdx, qword ptr [rcx + 0xc0]
003F7F81  xor      r8d, r8d
003F7F84  mov      qword ptr [rsp + 0x120], rbx
003F7F8C  mov      rbx, qword ptr [rcx + 0x38]
003F7F90  lea      rcx, [rsp + 0x20]
003F7F95  call     0x2b3400  ; -> 002B3400 fn
003F7F9A  test     byte ptr [rdi + 0xd4], 1
003F7FA1  lea      r9, [rsp + 0x20]
003F7FA6  movss    xmm0, dword ptr [rip + 0x18f3bfa]  ; -> 01CEBBA8 [f32 1]
003F7FAE  mov      ecx, 0x40
003F7FB3  movss    dword ptr [rsp + 0x54], xmm0
003F7FB9  movzx    eax, byte ptr [rbx + 0x5c]
003F7FBD  mov      byte ptr [rsp + 0xbf], al
003F7FC4  mov      eax, 0x80
003F7FC9  cmovne   ax, cx
003F7FCD  mov      rcx, rbx
003F7FD0  mov      word ptr [rbx + 0x5a], ax
003F7FD4  movsx    r8d, word ptr [rdi + 0xca]
003F7FDC  movsx    edx, word ptr [rdi + 0xc8]
003F7FE3  call     0x2d8650  ; -> 002D8650 fn
003F7FE8  mov      rbx, qword ptr [rsp + 0x120]
003F7FF0  xor      eax, eax
003F7FF2  mov      rcx, qword ptr [rsp + 0xf0]
003F7FFA  xor      rcx, rsp
003F7FFD  call     0x808c40  ; -> 00808C40 fn
003F8002  add      rsp, 0x100
003F8009  pop      rdi
003F800A  ret      
```

## 0053ED10 (73 B, extent 0053ED10-0053ED59)

Page context: "e set in code, '(+2, +2)' for all three line kinds.**       - **Where the table lives.** '0053E0B0' is called with the widget by its procedure '0053E380' (message 4,         '0053E44B'; installed by '0053ED10'). The table is in the widget's private area past the '0xC0' base         ([the widget object](../../16-UI/Widget-Object-Model/CONTRACT-widget-object.md)).       - **The init path writes it.** On message 1, after allocating and cle"

```
0053ED10  sub      rsp, 0x28
0053ED14  cmp      qword ptr [rip + 0x2769d5c], 0  ; -> 02CA8A78
0053ED1C  jne      0x53ed32  ; -> 0053ED32
0053ED1E  xor      r8d, r8d
0053ED21  lea      rdx, [rip - 0x198]  ; -> 0053EB90
0053ED28  mov      ecx, 0xc8
0053ED2D  call     0x244f50  ; -> 00244F50 fn
0053ED32  cmp      qword ptr [rip + 0x2769d46], 0  ; -> 02CA8A80
0053ED3A  jne      0x53ed54  ; -> 0053ED54
0053ED3C  xor      r8d, r8d
0053ED3F  lea      rdx, [rip - 0x9c6]  ; -> 0053E380
0053ED46  mov      ecx, 0x1498
0053ED4B  add      rsp, 0x28
0053ED4F  jmp      0x244f50  ; -> 00244F50 fn
0053ED54  add      rsp, 0x28
0053ED58  ret      
```

## 00799980 (92 B, extent 00799980-007999DC)

Page context: "Mechanical neighbours introduced by this section's citations: '001CCB20' (one of the constructor's callers) reaches Platform '005CC930' (1 edge), and '005CC930' itself carries an Application caller ('00799980', 1 edge). Those are edges of the caller and its callee, not of the parameter block - noted so the audit accounts for them.  '002A4EE0' (313 B) is the per-glyph walker '002A6190' calls: for 'word[rcx+0x3F0]' entries, 'sbyte[[rcx+0x"

```
00799980  push     rbx
00799982  sub      rsp, 0x20
00799986  mov      rax, rdx
00799989  lea      r8, [rsp + 0x30]
0079998E  mov      rbx, rcx
00799991  lea      rdx, [rip + 0x15d3a8]  ; -> 008F6D40
00799998  mov      rcx, rax
0079999B  call     0x71f970  ; -> 0071F970 fn
007999A0  movss    xmm1, dword ptr [rsp + 0x30]
007999A6  xorps    xmm0, xmm0
007999A9  comiss   xmm0, xmm1
007999AC  movss    dword ptr [rbx + 0x6c], xmm1
007999B1  jb       0x7999d4  ; -> 007999D4
007999B3  call     0x5cc930  ; -> 005CC930 fn
007999B8  subsd    xmm0, qword ptr [rip + 0x251c728]  ; -> 02CB60E8
007999C0  subsd    xmm0, qword ptr [rbx + 0x50]
007999C5  subsd    xmm0, qword ptr [rbx + 0x40]
007999CA  addsd    xmm0, qword ptr [rbx + 0x50]
007999CF  movsd    qword ptr [rbx + 0x50], xmm0
007999D4  xor      eax, eax
007999D6  add      rsp, 0x20
007999DA  pop      rbx
007999DB  ret      
```
