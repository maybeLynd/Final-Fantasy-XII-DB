# F-interior pack: `17-Presentation-Rendering/Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md`

Generated 2026-10-02 12:46 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/the-screen-fade-layers-and-the-movie-fade-schedule.json`.

Functions: 7. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 54e8a524e	SWE2-FRONTIER for FABLE: pass-22 unattributed appends - verifier + 23 of 34 PUBLISHABLE pages (batch). OPUS read these before packing.

## 00264830 (50 B, extent 00264830-00264862)

Page context: "essage body - '00247930'/'00283B30'. Interior anchor '00283A39' (a '00247930' call).  ## SWE2-EC7-51 update (2026-09-19) - '00355350'  '00355350' (174 B) is a body - '001D6AE0'/'002640C0'/'00264180'/'00264830'/'002EF890'/'00314440'. Interior anchor '0035536D' (an '001D6AE0' call).   ## SWE2-EC7-64 update (2026-09-19) - '00360E50'  '00360E50' (141 B) is a '+0xC4'/'+0xC8' by-sign body - '002DEC20'/'002DEDE0' plus '022CB9F0'. Interior anch"

```
00264830  lea      rax, [rip + 0x1e347d9]  ; -> 02099010
00264837  lea      rcx, [rip + 0x1e34ce2]  ; -> 02099520
0026483E  nop      
00264840  test     byte ptr [rax - 0x1f0], 1
00264847  je       0x26484e  ; -> 0026484E
00264849  test     byte ptr [rax], 4
0026484C  jne      0x26485c  ; -> 0026485C
0026484E  add      rax, 0x288
00264854  cmp      rax, rcx
00264857  jle      0x264840  ; -> 00264840
00264859  xor      eax, eax
0026485B  ret      
0026485C  mov      eax, 1
00264861  ret      
```

## 0026C3C0 (30 B, extent 0026C3C0-0026C3DE)

Page context: "x5AE8' floats under '[02EB…]+0x5AE0 bit 1') and from '003CA310''s message-'0x12' arm gated on '+8 == 0x8102'.  | state ('+0xC0' byte) | arm | work | next state | |---|---|---|---| | 1 | '0035CB38' | '0026C3C0(0)', '00303D90(0)', '003CA1C0', '003C58B0', '003634B0(0xF, 0)' | 9 | | 2 | '0035CCEB' | '00282F80()' ('*(0209AC30)+0x408' zero, '0x938' B), '00283270(1)', '002839B0()' | 3 | | 3 | '0035CD19' | two 9-iteration scans of '00282DF0(i)'"

```
0026C3C0  movsxd   rax, ecx
0026C3C3  mov      edx, 1
0026C3C8  imul     rcx, rax, 0x288
0026C3CF  lea      rax, [rip + 0x1e2ca3a]  ; -> 02098E10
0026C3D6  add      rcx, rax
0026C3D9  jmp      0x26c3e0  ; -> 0026C3E0 fn
```

## 0026DE00 (27 B, extent 0026DE00-0026DE1B)

Page context: "1)' wait; then '002DEDE0(+0xC4)' | 11 or 12 ('+0xC4 < 0' picks 12) | | 11 | '0035CC01' | '002DED60(+0xC4)' wait — exits while nonzero | 12 | | 12 | '0035CC2E' | '00360D70'/'00360E50(+0xC4)' by sign; '0026DE00(0)' → '+0xC8'; '00361630(+0xC8)' | 13 or 14 (result <0 picks 14) | | 13 | '0035CCA9' | '00360C20(+0xC8)'; when it reads 5: '002DEC00()'/'002DECE0()' vs '+0xC8' | 2 | | 14 | '0035CC7C' | '00361630(+0xC8)' — exits while <0 | 13 |  Th"

```
0026DE00  push     rbx
0026DE02  sub      rsp, 0x20
0026DE06  mov      ebx, ecx
0026DE08  call     0x3148f0  ; -> 003148F0 fn
0026DE0D  mov      edx, eax
0026DE0F  mov      ecx, ebx
0026DE11  add      rsp, 0x20
0026DE15  pop      rbx
0026DE16  jmp      0x26de20  ; -> 0026DE20 fn
```

## 00283B30 (115 B, extent 00283B30-00283BA3)

Page context: "allback is a kind dispatch: kind 1 snapshots ten 'movsx' words out of the bank's '+0x468..+0xA68' fields (0xC0-stride apart) into 'out+0xC0..+0xE0' with '+0xE4 = 0' and calls '00247930'; kind 2 runs '00283B30'; kind '0x12' returns 0; everything else forwards to '005C5230'. Interior anchor '002839D4' (the 'call 00244F50' allocation).  ## SWE2-EC7-37 update (2026-09-19) - '003CA310'  '003CA310' (536 B) is the fade message body the page na"

```
00283B30  push     rbx
00283B32  sub      rsp, 0x20
00283B36  mov      rbx, rcx
00283B39  mov      ecx, dword ptr [rcx + 0xe4]
00283B3F  sub      ecx, 1
00283B42  je       0x283b85  ; -> 00283B85
00283B44  cmp      ecx, 1
00283B47  jne      0x283b9d  ; -> 00283B9D
00283B49  call     0x324360  ; -> 00324360 fn
00283B4E  test     eax, eax
00283B50  je       0x283b9d  ; -> 00283B9D
00283B52  mov      eax, dword ptr [rbx + 0xe8]
00283B58  test     al, 1
00283B5A  je       0x283b75  ; -> 00283B75
00283B5C  and      eax, 0xfffffffe
00283B5F  mov      dword ptr [rbx + 0xe4], 1
00283B69  mov      dword ptr [rbx + 0xe8], eax
00283B6F  add      rsp, 0x20
00283B73  pop      rbx
00283B74  ret      
00283B75  mov      dword ptr [rbx + 0xe4], 0
00283B7F  add      rsp, 0x20
00283B83  pop      rbx
00283B84  ret      
00283B85  call     0x324360  ; -> 00324360 fn
00283B8A  test     eax, eax
00283B8C  je       0x283b9d  ; -> 00283B9D
00283B8E  call     0x324380  ; -> 00324380 fn
00283B93  mov      dword ptr [rbx + 0xe4], 2
00283B9D  add      rsp, 0x20
00283BA1  pop      rbx
00283BA2  ret      
```

## 002EFD50 (34 B, extent 002EFD50-002EFD72)

Page context: "002EFE50(n)' / '002EFE60(n)' | write '022BDEB4' / '022BDEB0' / '022BDEB8' — the kind and wait words the schedule and the skip set before starting a layer ('5'/'6' and '0xFF' are the values seen) | | '002EFD50' / '002EFD80(n)' / '002EFDC0(n)' | a single **effect fade** handle beside the layers, through '0036E750(0, 0, &params, n, 9)' — the 'efffadein' / 'efffadeout' verbs ('0268' / '0269') |  The layer verbs ~~pop two integers and tail-j"

```
002EFD50  sub      rsp, 0x28
002EFD54  mov      ecx, dword ptr [rip + 0x1fce15e]  ; -> 022BDEB8
002EFD5A  test     ecx, ecx
002EFD5C  je       0x2efd6d  ; -> 002EFD6D
002EFD5E  call     0x24cff0  ; -> 0024CFF0 fn
002EFD63  mov      dword ptr [rip + 0x1fce14b], 0  ; -> 022BDEB8
002EFD6D  add      rsp, 0x28
002EFD71  ret      
```

## 002EFE10 (34 B, extent 002EFE10-002EFE32)

Page context: "CB0') |  **The colour** ('002EFBD5'–'002EFC6F'): when the one-shot byte ~~'022BDD58'~~ '022BDD5C' is set, the four bytes ~~'022BDD59'–'022BDD5C'~~ '022BDD58'–'022BDD5B' *(corrected 2026-10-02, OPUS: '002EFE10'+0x0 'mov byte ptr [022BDD5C], 1', +0x7..+0x1A the four colour bytes; '002EFA70'+0x165 tests '022BDD5C')* are copied in and the byte cleared — a scripted colour override ('002EFE10' sets it); otherwise, when a fade-in follows a run"

```
002EFE10  mov      byte ptr [rip + 0x1fcdf45], 1  ; -> 022BDD5C
002EFE17  mov      byte ptr [rip + 0x1fcdf3b], cl  ; -> 022BDD58
002EFE1D  mov      byte ptr [rip + 0x1fcdf36], dl  ; -> 022BDD59
002EFE23  mov      byte ptr [rip + 0x1fcdf30], r8b  ; -> 022BDD5A
002EFE2A  mov      byte ptr [rip + 0x1fcdf2a], r9b  ; -> 022BDD5B
002EFE31  ret      
```

## 0035D010 (14 B, extent 0035D010-0035D01E)

Page context: " SWE2-EC7-37 update (2026-09-19) - '003CA310'  '003CA310' (536 B) is the fade message body the page names - '01F44830'/'02092730'/'01E0C1D8'/'01E0C1DC', '00249C60'/'00303CC0' triples plus '00244F00'/'0035D010' pairs and '005C5230'/'0035CF50'/'0035CFA0'. Interior anchor '003CA356' (a '005C5230' call).  ## SWE2-EC7-37 update (2026-09-19) - '001DAB30'  '001DAB30' (512 B) is a call-free CRT vector insert sibling - capacity test '[rdi+0x10]-"

```
0035D010  xor      eax, eax
0035D012  test     ecx, ecx
0035D014  sete     al
0035D017  mov      dword ptr [rip + 0x1f6d43f], eax  ; -> 022CA45C
0035D01D  ret      
```
