# F-interior pack: `18-Audio/the-music-control-file-and-the-bgm-stream.md`

Generated 2026-10-03 02:32 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/the-music-control-file-and-the-bgm-stream.json`.

Functions: 9. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: cd6bd7f58	SWE2-DATA consolidated publish: progress-report cluster (generation store, R3 semantics, DB_GOAL, me; d0fd168a2	SWE2-DATA: batch-5 review corrections (clamping page's .data vf00 cell restored, SD-190 gate on the ; inbox mentions: FABLE.md). OPUS read these before packing.

## 00220D40 (82 B, extent 00220D40-00220D92)

Page context: "/'00861EBA' pair/'002255B0'/'007A88F0'/'00809950'. Interior anchor '0022503F' (a '00222080' call).  ## SWE2-EC7-48 update (2026-09-19) - '002251B0'  '002251B0' (199 B) is the music-bank start body - '00220D40'/'00221710'/'00221D10'/'00225580'/'00225590'/'002255A0'/'00225CC0'. Interior anchor '002251CF' (a '00220D40' call).  ## SWE2-EC7-48 update (2026-09-19) - '0021D770'  '0021D770' (200 B) is a body - '00212950'/'002129F0'/'00212A70'/'"

```
00220D40  push     rdi
00220D42  sub      rsp, 0x30
00220D46  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
00220D4F  mov      qword ptr [rsp + 0x48], rbx
00220D54  mov      rbx, rcx
00220D57  lea      rdi, [rcx + 0x350]
00220D5E  mov      qword ptr [rsp + 0x40], rdi
00220D63  mov      rcx, rdi
00220D66  call     0x5cd4f0  ; -> 005CD4F0 fn
00220D6B  nop      
00220D6C  lea      rcx, [rbx + 0x1d0]
00220D73  call     0x220600  ; -> 00220600 fn
00220D78  mov      rbx, rax
00220D7B  mov      rcx, rdi
00220D7E  call     0x5cd820  ; -> 005CD820 fn
00220D83  nop      
00220D84  mov      rax, rbx
00220D87  mov      rbx, qword ptr [rsp + 0x48]
00220D8C  add      rsp, 0x30
00220D90  pop      rdi
00220D91  ret      
```

## 002255B0 (9 B, extent 002255B0-002255B9)

Page context: "'001DBD00' directly ('002DEEDE'). Returns the last status.  ## SWE2-EC7-42 update (2026-09-19) - '00225030'  '00225030' (297 B) is a music-control body - '00222080'/'00221770' triple/'00861EBA' pair/'002255B0'/'007A88F0'/'00809950'. Interior anchor '0022503F' (a '00222080' call).  ## SWE2-EC7-48 update (2026-09-19) - '002251B0'  '002251B0' (199 B) is the music-bank start body - '00220D40'/'00221710'/'00221D10'/'00225580'/'00225590'/'002"

```
002255B0  mov      qword ptr [rcx + 0x20], rdx
002255B4  mov      qword ptr [rcx + 0x28], r8
002255B8  ret      
```

## 00225CC0 (9 B, extent 00225CC0-00225CC9)

Page context: " '0022503F' (a '00222080' call).  ## SWE2-EC7-48 update (2026-09-19) - '002251B0'  '002251B0' (199 B) is the music-bank start body - '00220D40'/'00221710'/'00221D10'/'00225580'/'00225590'/'002255A0'/'00225CC0'. Interior anchor '002251CF' (a '00220D40' call).  ## SWE2-EC7-48 update (2026-09-19) - '0021D770'  '0021D770' (200 B) is a body - '00212950'/'002129F0'/'00212A70'/'002251B0' plus a 'call [rax+0x30]' vcall. Interior anchor '0021D7B"

```
00225CC0  mov      qword ptr [rcx + 8], rdx
00225CC4  mov      dword ptr [rcx + 0x10], r8d
00225CC8  ret      
```

## 0032E780 (44 B, extent 0032E780-0032E7AC)

Page context: "he stream submitted or advanced~~ *(narrowed 2026-09-30, OPUS, static: every return path is 'mov eax, esi', and 'esi' is set to 1 only at '003EAE54' and '003EAFA2', each right after a submit through '0032E780'; so **a return of 1 means the stream submitted a piece**, and the advances 2 → 4 and 4 → 5 return 0. Reported by SWE2-ORACLE's [S-08 drain record](../_index/candidates/s08-bgm-machine-drain-0930/README.md))*, and **the state-1 arm"

```
0032E780  sub      rsp, 0x38
0032E784  test     edx, edx
0032E786  jns      0x32e790  ; -> 0032E790
0032E788  or       eax, 0xffffffff
0032E78B  add      rsp, 0x38
0032E78F  ret      
0032E790  mov      rax, qword ptr [rsp + 0x60]
0032E795  mov      dword ptr [rsp + 0x28], 0
0032E79D  mov      qword ptr [rsp + 0x20], rax
0032E7A2  call     0x32e870  ; -> 0032E870 fn
0032E7A7  add      rsp, 0x38
0032E7AB  ret      
```

## 00354690 (33 B, extent 00354690-003546B1)

Page context: "f '0x30000', allocates from heap 2 ('0036C1D0(2)', '0036A190'), tags it with the empty string at '00D51814' ('0036C660'), and '003EB180' records buffer and size | | '0448' | 'bgmstreamread(index)' | '00354690' → '003EB100' | with a buffer present: kind '0x24', the index, counters and handles zeroed, 'requestId = −1', **state 1, active** ('003EB10C'–'003EB139'); then the VM wait byte '00314D40(1)' | | '0449' | 'bgmstreamreadsync' | '0035"

```
00354690  sub      rsp, 0x28
00354694  mov      rcx, r9
00354697  call     0x267e10  ; -> 00267E10 fn
0035469C  mov      ecx, eax
0035469E  call     0x3eb100  ; -> 003EB100 fn
003546A3  mov      ecx, 1
003546A8  add      rsp, 0x28
003546AC  jmp      0x314d40  ; -> 00314D40 fn
```

## 003557C0 (43 B, extent 003557C0-003557EB)

Page context: "ded to 002DF680 at play   +0x33  u8    0x7F             handed to 002DF680 at play '''  ### 3.2 The verbs  | id | verb | handler | what it does | |---|---|---|---| | '044D' | 'usebgmstream(bytes)' | '003557C0' | frees any stream ('003EB010'), then '003EACA0(bytes)': rounds up to a 64 KB multiple with a floor of '0x30000', allocates from heap 2 ('0036C1D0(2)', '0036A190'), tags it with the empty string at '00D51814' ('0036C660'), and '00"

```
003557C0  push     rbx
003557C2  sub      rsp, 0x20
003557C6  mov      rcx, r9
003557C9  call     0x267e10  ; -> 00267E10 fn
003557CE  mov      ebx, eax
003557D0  call     0x3eb010  ; -> 003EB010 fn
003557D5  mov      ecx, ebx
003557D7  call     0x3eaca0  ; -> 003EACA0 fn
003557DC  mov      edx, ebx
003557DE  mov      rcx, rax
003557E1  add      rsp, 0x20
003557E5  pop      rbx
003557E6  jmp      0x3eb180  ; -> 003EB180 fn
```

## 003EB010 (58 B, extent 003EB010-003EB04A)

Page context: "  u8    0x7F             handed to 002DF680 at play '''  ### 3.2 The verbs  | id | verb | handler | what it does | |---|---|---|---| | '044D' | 'usebgmstream(bytes)' | '003557C0' | frees any stream ('003EB010'), then '003EACA0(bytes)': rounds up to a 64 KB multiple with a floor of '0x30000', allocates from heap 2 ('0036C1D0(2)', '0036A190'), tags it with the empty string at '00D51814' ('0036C660'), and '003EB180' records buffer and size"

```
003EB010  sub      rsp, 0x28
003EB014  cmp      qword ptr [rip + 0x27730cc], 0  ; -> 02B5E0E8
003EB01C  je       0x3eb045  ; -> 003EB045
003EB01E  lea      rcx, [rip + 0x27730bb]  ; -> 02B5E0E0
003EB025  call     0x3ead10  ; -> 003EAD10 fn
003EB02A  mov      rcx, qword ptr [rip + 0x27730b7]  ; -> 02B5E0E8
003EB031  call     0x3697f0  ; -> 003697F0 fn
003EB036  xor      eax, eax
003EB038  mov      qword ptr [rip + 0x27730a9], rax  ; -> 02B5E0E8
003EB03F  mov      dword ptr [rip + 0x27730ab], eax  ; -> 02B5E0F0
003EB045  add      rsp, 0x28
003EB049  ret      
```

## 003EB0A0 (34 B, extent 003EB0A0-003EB0C2)

Page context: "ind '0x24', the index, counters and handles zeroed, 'requestId = −1', **state 1, active** ('003EB10C'–'003EB139'); then the VM wait byte '00314D40(1)' | | '0449' | 'bgmstreamreadsync' | '00354920' → '003EB0A0' | keeps waiting while active and the state is neither 0 nor 5 | | '044A' | 'bgmstreamplay' | '003EB150' | active and state 5 → state 6 | | '044B' | 'bgmstreamplaysync' | — | no handler in the table | | '044C' | 'bgmstreamstop' | '"

```
003EB0A0  cmp      byte ptr [rip + 0x277306a], 0  ; -> 02B5E111
003EB0A7  je       0x3eb0bf  ; -> 003EB0BF
003EB0A9  movzx    eax, byte ptr [rip + 0x2773060]  ; -> 02B5E110
003EB0B0  test     eax, eax
003EB0B2  je       0x3eb0bf  ; -> 003EB0BF
003EB0B4  cmp      eax, 5
003EB0B7  je       0x3eb0bf  ; -> 003EB0BF
003EB0B9  mov      eax, 1
003EB0BE  ret      
003EB0BF  xor      eax, eax
003EB0C1  ret      
```

## 003EB150 (35 B, extent 003EB150-003EB173)

Page context: "03EB139'); then the VM wait byte '00314D40(1)' | | '0449' | 'bgmstreamreadsync' | '00354920' → '003EB0A0' | keeps waiting while active and the state is neither 0 nor 5 | | '044A' | 'bgmstreamplay' | '003EB150' | active and state 5 → state 6 | | '044B' | 'bgmstreamplaysync' | — | no handler in the table | | '044C' | 'bgmstreamstop' | '003EADC0' → '003EAD10' | per state: pump the queue to idle ('0032E520(0)'), or poll '002DEE90(soundHandl"

```
003EB150  cmp      byte ptr [rip + 0x2772fba], 0  ; -> 02B5E111
003EB157  je       0x3eb172  ; -> 003EB172
003EB159  movzx    eax, byte ptr [rip + 0x2772fb0]  ; -> 02B5E110
003EB160  mov      edx, 6
003EB165  cmp      al, 5
003EB167  mov      ecx, eax
003EB169  cmove    ecx, edx
003EB16C  mov      byte ptr [rip + 0x2772f9e], cl  ; -> 02B5E110
003EB172  ret      
```
