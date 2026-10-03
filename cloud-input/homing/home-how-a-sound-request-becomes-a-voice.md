# Homing pack: `18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md`

Generated 2026-10-02 22:54 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-how-a-sound-request-becomes-a-voice.json`.

Bodies: 11. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002033C0 (136 B, extent 002033C0-00203448)

Entered from (direct sites whose caller this page cites): `00203CB0` + 0x89 (call; `00203CB0` is cited on this page)
Other direct sites: none

Host context: "'00203A30').  '00205120' (522 B) is the '='-arm builder '002070A0' runs over the scanned span: for each code 0..255 it '00203B00's the char-name string and '00861ED2'-compares it against the target ('00203CB0' product at '[rax+0x10]/+0x18'); on equality it lazily '00210EC0's a 0x20-byte bitmap at '[r15+0x28]' and 'bts'-sets the code's bit, closing with the '00210EB0' CRT aligned-free on the temporaries - the set of all codes whose name "

```
002033C0  mov      qword ptr [rsp + 8], rcx
002033C5  push     r14
002033C7  sub      rsp, 0x30
002033CB  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
002033D4  mov      qword ptr [rsp + 0x48], rbx
002033D9  mov      qword ptr [rsp + 0x50], rsi
002033DE  mov      qword ptr [rsp + 0x58], rdi
002033E3  mov      rsi, r8
002033E6  mov      r14, rdx
002033E9  mov      rdi, rcx
002033EC  xor      eax, eax
002033EE  mov      qword ptr [rcx], rax
002033F1  mov      qword ptr [rcx + 8], rax
002033F5  mov      qword ptr [rcx + 0x10], rax
002033F9  sub      rsi, rdx
002033FC  je       0x203432  ; -> 00203432
002033FE  mov      rdx, rsi
00203401  call     0x1df990  ; -> 001DF990 fn
00203406  mov      qword ptr [rdi], rax
00203409  mov      qword ptr [rdi + 8], rax
0020340D  mov      rax, qword ptr [rdi]
00203410  lea      rcx, [rsi + rax]
00203414  mov      qword ptr [rdi + 0x10], rcx
00203418  mov      rbx, rax
0020341B  mov      r8, rsi
0020341E  mov      rdx, r14
00203421  mov      rcx, rax
00203424  call     qword ptr [rip + 0x6bf616]  ; -> 008C2A40 [u64 0x0000000001CCEB62]
0020342A  lea      rax, [rsi + rbx]
0020342E  mov      qword ptr [rdi + 8], rax
00203432  mov      rbx, qword ptr [rsp + 0x48]
00203437  mov      rsi, qword ptr [rsp + 0x50]
0020343C  mov      rdi, qword ptr [rsp + 0x58]
00203441  add      rsp, 0x30
00203445  pop      r14
00203447  ret      
```

## 00203520 (137 B, extent 00203520-002035A9)

Entered from (direct sites whose caller this page cites): `00206F60` + 0x64 (call; `00206F60` is cited on this page)
Other direct sites: none

Host context: " calls: 'rcx + 8' gets three zeroed qwords, then '00206B70'/'0020A3D0' build the payload through 'rbp'/'rsi'/'r12' - the voice path's record init.  Interior anchor '00204066' (function '00204010').  '00206F60' (315 B) is the classifying scan '00208710' calls on the 'rcx' request: 'dword[+0xB8]&0x100' runs 'byte[rax]' through the '008C2440' IAT classify into 'bpl'; 'rsi+0x20' nonzero then '00203520(rdi, [rbx+0xA0])' scans for the match p"

```
00203520  mov      qword ptr [rsp + 8], rbx
00203525  mov      qword ptr [rsp + 0x10], rbp
0020352A  mov      qword ptr [rsp + 0x18], rsi
0020352F  mov      qword ptr [rsp + 0x20], rdi
00203534  mov      rbx, r8
00203537  mov      rbp, rcx
0020353A  test     r8, r8
0020353D  je       0x20358c  ; -> 0020358C
0020353F  nop      
00203540  mov      edi, dword ptr [rbx + 0xc]
00203543  xor      r10d, r10d
00203546  test     edi, edi
00203548  je       0x203583  ; -> 00203583
0020354A  mov      r9d, dword ptr [rbx]
0020354D  nop      dword ptr [rax]
00203550  xor      eax, eax
00203552  mov      r8, rbp
00203555  test     r9, r9
00203558  je       0x203576  ; -> 00203576
0020355A  mov      r11d, r10d
0020355D  add      r11, qword ptr [rbx + 0x10]
00203561  movzx    ecx, byte ptr [r8]
00203565  inc      r8
00203568  cmp      cl, byte ptr [r11 + rax]
0020356C  jne      0x203576  ; -> 00203576
0020356E  inc      rax
00203571  cmp      rax, r9
00203574  jb       0x203561  ; -> 00203561
00203576  cmp      r8, rdx
00203579  je       0x2035a4  ; -> 002035A4
0020357B  add      r10d, r9d
0020357E  cmp      r10d, edi
00203581  jb       0x203550  ; -> 00203550
00203583  mov      rbx, qword ptr [rbx + 0x18]
00203587  test     rbx, rbx
0020358A  jne      0x203540  ; -> 00203540
0020358C  mov      rax, rbp
0020358F  mov      rbx, qword ptr [rsp + 8]
00203594  mov      rbp, qword ptr [rsp + 0x10]
00203599  mov      rsi, qword ptr [rsp + 0x18]
0020359E  mov      rdi, qword ptr [rsp + 0x20]
002035A3  ret      
002035A4  mov      rax, rdx
002035A7  jmp      0x20358f  ; -> 0020358F
```

## 00205C70 (227 B, extent 00205C70-00205D53)

Entered from (direct sites whose caller this page cites): `00206E90` + 0x16 (call; `00206E90` is cited on this page)
Other direct sites: none

Host context: " bit '0x1B' with '+0x7C == 0x29' asserts ('008C2430', code 5); bit '0x20' with '+0x7C == 0x3F' double-runs '00208CF0' then switches on '+0x7C' - '0x3A' runs '002076D0' returning 1, '0x21'/'0x3D' run '00206E90' with 'dl' 1/0 returning 0, anything else asserts code '0xE'; otherwise 'dword[+0x70] & 0x200' runs '00208C60(rcx+0x40, 8)' into '00206D30' and '00207E90(rsi+0x40, result)' returning 1, else '00206EE0' returning 1 - the state-keyed"

```
00205C70  push     rsi
00205C72  push     rdi
00205C73  push     r14
00205C75  sub      rsp, 0x30
00205C79  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
00205C82  mov      qword ptr [rsp + 0x50], rbx
00205C87  movzx    r14d, dl
00205C8B  mov      rsi, rcx
00205C8E  mov      ecx, 0x28
00205C93  call     0x210ec0  ; -> 00210EC0 fn
00205C98  mov      rbx, rax
00205C9B  mov      qword ptr [rsp + 0x60], rax
00205CA0  xor      edi, edi
00205CA2  test     rax, rax
00205CA5  je       0x205cd0  ; -> 00205CD0
00205CA7  mov      eax, edi
00205CA9  test     r14b, r14b
00205CAC  setne    al
00205CAF  add      eax, 0xa
00205CB2  mov      dword ptr [rbx + 8], eax
00205CB5  mov      dword ptr [rbx + 0xc], edi
00205CB8  mov      qword ptr [rbx + 0x10], rdi
00205CBC  mov      qword ptr [rbx + 0x18], rdi
00205CC0  lea      rax, [rip + 0x6ffc29]  ; -> 009058F0
00205CC7  mov      qword ptr [rbx], rax
00205CCA  mov      qword ptr [rbx + 0x20], rdi
00205CCE  jmp      0x205cd3  ; -> 00205CD3
00205CD0  mov      rbx, rdi
00205CD3  mov      qword ptr [rsp + 0x60], rbx
00205CD8  mov      ecx, 0x20
00205CDD  call     0x210ec0  ; -> 00210EC0 fn
00205CE2  mov      r8, rax
00205CE5  test     rax, rax
00205CE8  je       0x205d06  ; -> 00205D06
00205CEA  lea      rax, [rip + 0x6ffbcf]  ; -> 009058C0
00205CF1  mov      qword ptr [r8], rax
00205CF4  mov      qword ptr [r8 + 8], 1
00205CFC  mov      qword ptr [r8 + 0x10], rdi
00205D00  mov      qword ptr [r8 + 0x18], rdi
00205D04  jmp      0x205d09  ; -> 00205D09
00205D06  mov      r8, rdi
00205D09  mov      rax, qword ptr [rsi + 8]
00205D0D  mov      qword ptr [rbx + 0x18], rax
00205D11  mov      rax, qword ptr [rsi + 8]
00205D15  mov      rcx, qword ptr [rax + 0x10]
00205D19  test     rcx, rcx
00205D1C  je       0x205d2e  ; -> 00205D2E
00205D1E  mov      qword ptr [rbx + 0x10], rcx
00205D22  mov      rcx, qword ptr [rsi + 8]
00205D26  mov      rdx, qword ptr [rcx + 0x10]
00205D2A  mov      qword ptr [rdx + 0x18], rbx
00205D2E  mov      rcx, qword ptr [rsi + 8]
00205D32  mov      qword ptr [rcx + 0x10], rbx
00205D36  mov      qword ptr [rbx + 0x20], r8
00205D3A  mov      qword ptr [r8 + 0x18], rbx
00205D3E  mov      qword ptr [rsi + 8], r8
00205D42  mov      rax, rbx
00205D45  mov      rbx, qword ptr [rsp + 0x50]
00205D4A  add      rsp, 0x30
00205D4E  pop      r14
00205D50  pop      rdi
00205D51  pop      rsi
00205D52  ret      
```

## 002072C0 (78 B, extent 002072C0-0020730E)

Entered from (direct sites whose caller this page cites): `00206640` + 0x86 (call; `00206640` is cited on this page)
Other direct sites: none

Host context: "08CF0'/'00206C20'/'002054D0' resolve - the voice request's path splitter.  Interior anchor '00208E57' (function '00208DE0').  '00208CF0' (73 B) is the separator scan '00208DE0'/'00205890'/'00206430'/'00206640'/'00209840' call: walks '[rcx]' toward '[rcx + 0x10]' for '0x5C', then unless 'byte[rcx + 0x80]' bit 8 (0x28/0x29 exempt) or bit 0x10 (0x7B-0x7D exempt) applies, stores the found offset back to '[rcx]' - the request path's token ad"

```
002072C0  cmp      dl, 0x66
002072C3  jne      0x2072cf  ; -> 002072CF
002072C5  mov      dword ptr [rcx + 0x74], 0xc
002072CC  mov      al, 1
002072CE  ret      
002072CF  cmp      dl, 0x6e
002072D2  jne      0x2072de  ; -> 002072DE
002072D4  mov      dword ptr [rcx + 0x74], 0xa
002072DB  mov      al, 1
002072DD  ret      
002072DE  cmp      dl, 0x72
002072E1  jne      0x2072ed  ; -> 002072ED
002072E3  mov      dword ptr [rcx + 0x74], 0xd
002072EA  mov      al, 1
002072EC  ret      
002072ED  cmp      dl, 0x74
002072F0  jne      0x2072fc  ; -> 002072FC
002072F2  mov      dword ptr [rcx + 0x74], 9
002072F9  mov      al, 1
002072FB  ret      
002072FC  cmp      dl, 0x76
002072FF  jne      0x20730b  ; -> 0020730B
00207301  mov      dword ptr [rcx + 0x74], 0xb
00207308  mov      al, 1
0020730A  ret      
0020730B  xor      al, al
0020730D  ret      
```

## 00207F50 (96 B, extent 00207F50-00207FB0)

Entered from (direct sites whose caller this page cites): `00205890` + 0x18B (call; `00205890` is cited on this page); `00205890` + 0x1B9 (call; `00205890` is cited on this page)
Other direct sites: none

Host context: "nd-request sibling - '00208220'/'00209E00'. Interior anchor '0020A659' (a '00208220' call).  ## SWE2-EC7-41 update (2026-09-19) - '00206D30'  '00206D30' (350 B) is a sound-request body - '009058C0', '00205890' pair/'00208C60'/'00207E90' pair/'00205DF0'/'00209530'/'00210EC0'. Interior anchor '00206D3F' (an '00205890' call).  ## SWE2-EC7-41 update (2026-09-19) - '0027EA70'  '0027EA70' (328 B) is a sound-request body - '01E0C2A4'/'0209AC20" / "nd-request sibling - '00208220'/'00209E00'. Interior anchor '0020A659' (a '00208220' call).  ## SWE2-EC7-41 update (2026-09-19) - '00206D30'  '00206D30' (350 B) is a sound-request body - '009058C0', '00205890' pair/'00208C60'/'00207E90' pair/'00205DF0'/'00209530'/'00210EC0'. Interior anchor '00206D3F' (an '00205890' call).  ## SWE2-EC7-41 update (2026-09-19) - '0027EA70'  '0027EA70' (328 B) is a sound-request body - '01E0C2A4'/'0209AC20"

```
00207F50  sub      rsp, 0x28
00207F54  cmp      dword ptr [rcx + 0x7c], edx
00207F57  je       0x207f63  ; -> 00207F63
00207F59  mov      ecx, r8d
00207F5C  call     qword ptr [rip + 0x6ba4ce]  ; -> 008C2430 [u64 0x0000000001CCE710]
00207F62  int3     
00207F63  mov      rdx, qword ptr [rcx]
00207F66  mov      rax, qword ptr [rcx + 0x10]
00207F6A  cmp      rdx, rax
00207F6D  je       0x207fa7  ; -> 00207FA7
00207F6F  cmp      byte ptr [rdx], 0x5c
00207F72  jne      0x207fa4  ; -> 00207FA4
00207F74  inc      rdx
00207F77  cmp      rdx, rax
00207F7A  je       0x207fa4  ; -> 00207FA4
00207F7C  mov      r8d, dword ptr [rcx + 0x80]
00207F83  test     r8b, 8
00207F87  jne      0x207f92  ; -> 00207F92
00207F89  movzx    eax, byte ptr [rdx]
00207F8C  sub      al, 0x28
00207F8E  cmp      al, 1
00207F90  jbe      0x207fa1  ; -> 00207FA1
00207F92  test     r8b, 0x10
00207F96  jne      0x207fa4  ; -> 00207FA4
00207F98  movzx    eax, byte ptr [rdx]
00207F9B  sub      al, 0x7b
00207F9D  test     al, 0xfd
00207F9F  jne      0x207fa4  ; -> 00207FA4
00207FA1  mov      qword ptr [rcx], rdx
00207FA4  inc      qword ptr [rcx]
00207FA7  add      rsp, 0x28
00207FAB  jmp      0x209530  ; -> 00209530 fn
```

## 002081A0 (114 B, extent 002081A0-00208212)

Entered from (direct sites whose caller this page cites): `00206430` + 0x207 (jmp; `00206430` is cited on this page)
Other direct sites: none

Host context: "before '00208CF0'/'00206C20'/'002054D0' resolve - the voice request's path splitter.  Interior anchor '00208E57' (function '00208DE0').  '00208CF0' (73 B) is the separator scan '00208DE0'/'00205890'/'00206430'/'00206640'/'00209840' call: walks '[rcx]' toward '[rcx + 0x10]' for '0x5C', then unless 'byte[rcx + 0x80]' bit 8 (0x28/0x29 exempt) or bit 0x10 (0x7B-0x7D exempt) applies, stores the found offset back to '[rcx]' - the request path"

```
002081A0  push     rbx
002081A2  sub      rsp, 0x20
002081A6  mov      rbx, rcx
002081A9  call     0x2085b0  ; -> 002085B0 fn
002081AE  test     al, al
002081B0  je       0x20820a  ; -> 0020820A
002081B2  movsx    eax, byte ptr [rbx + 0x78]
002081B6  mov      rcx, qword ptr [rbx]
002081B9  mov      dword ptr [rbx + 0x74], eax
002081BC  mov      rax, qword ptr [rbx + 0x10]
002081C0  cmp      rcx, rax
002081C3  je       0x2081fa  ; -> 002081FA
002081C5  cmp      byte ptr [rcx], 0x5c
002081C8  jne      0x2081f7  ; -> 002081F7
002081CA  inc      rcx
002081CD  cmp      rcx, rax
002081D0  je       0x2081f7  ; -> 002081F7
002081D2  mov      edx, dword ptr [rbx + 0x80]
002081D8  test     dl, 8
002081DB  jne      0x2081e6  ; -> 002081E6
002081DD  movzx    eax, byte ptr [rcx]
002081E0  sub      al, 0x28
002081E2  cmp      al, 1
002081E4  jbe      0x2081f4  ; -> 002081F4
002081E6  test     dl, 0x10
002081E9  jne      0x2081f7  ; -> 002081F7
002081EB  movzx    eax, byte ptr [rcx]
002081EE  sub      al, 0x7b
002081F0  test     al, 0xfd
002081F2  jne      0x2081f7  ; -> 002081F7
002081F4  mov      qword ptr [rbx], rcx
002081F7  inc      qword ptr [rbx]
002081FA  mov      rcx, rbx
002081FD  call     0x209530  ; -> 00209530 fn
00208202  mov      al, 1
00208204  add      rsp, 0x20
00208208  pop      rbx
00208209  ret      
0020820A  xor      al, al
0020820C  add      rsp, 0x20
00208210  pop      rbx
00208211  ret      
```

## 002109F0 (67 B, extent 002109F0-00210A33)

Entered from (direct sites whose caller this page cites): `001DBAC0` + 0x35 (jmp; `001DBAC0` is cited on this page)
Other direct sites: none

Host context: "'Audio_SetMode' confirmed  '002DF530' (34 B) is the function this page names 'Audio_SetMode': clamps 'ecx' into '[0, 2]' (negative -> 0, '> 2' -> 2), loads 'dword[0215EF44]' as 'rcx', and tail-jumps '001DBAC0' with the clamped mode in 'edx'. Interior anchor '002DF53F' (the 'cmovg' clamp).  ## SWE2-EC7-37 update (2026-09-19) - '0020A800'  '0020A800' (554 B) is the object registrar the page names - '008C2448'/'00905958'/'00905985', the 'p"

```
002109F0  mov      qword ptr [rsp + 8], rbx
002109F5  push     rdi
002109F6  sub      rsp, 0x20
002109FA  mov      ebx, r8d
002109FD  mov      rdi, rcx
00210A00  cmp      dword ptr [rcx + 0x30], r8d
00210A04  je       0x210a25  ; -> 00210A25
00210A06  test     edx, edx
00210A08  js       0x210a25  ; -> 00210A25
00210A0A  test     r9d, r9d
00210A0D  je       0x210a25  ; -> 00210A25
00210A0F  mov      rcx, qword ptr [rcx]
00210A12  call     0x218dc0  ; -> 00218DC0 fn
00210A17  mov      dword ptr [rdi + 0x30], ebx
00210A1A  mov      rbx, qword ptr [rsp + 0x30]
00210A1F  add      rsp, 0x20
00210A23  pop      rdi
00210A24  ret      
00210A25  mov      dword ptr [rcx + 0x30], ebx
00210A28  mov      rbx, qword ptr [rsp + 0x30]
00210A2D  add      rsp, 0x20
00210A31  pop      rdi
00210A32  ret      
```

## 00210A90 (66 B, extent 00210A90-00210AD2)

Entered from (direct sites whose caller this page cites): `001DBCE0` + 0x17 (jmp; `001DBCE0` is cited on this page)
Other direct sites: none

Host context: "ESS-INDEX.md)) then 'int3'. The CRT's sized-delete fast path with its own corruption tripwires.  '002DEE80' — 11 B, 15 callers; the conditional sound-call tail. Interior verified: 'test ecx, ecx; jne 001DBCE0' at ['002DEE82'](../../_index/ADDRESS-INDEX.md) — a nonzero sound handle forwards to the Audio '001DBCE0'; zero returns 0. The guard in front of the voice-verbs' poll.  ### Interior citation — frontier hubs 001A9E10, 002DF0F0 (2026"

```
00210A90  mov      qword ptr [rsp + 8], rbx
00210A95  push     rdi
00210A96  sub      rsp, 0x20
00210A9A  mov      rdi, rcx
00210A9D  mov      ebx, edx
00210A9F  mov      rcx, qword ptr [rcx + 0x10]
00210AA3  call     0x21b2f0  ; -> 0021B2F0 fn
00210AA8  movzx    r8d, al
00210AAC  test     al, al
00210AAE  jne      0x210abf  ; -> 00210ABF
00210AB0  mov      rcx, qword ptr [rdi + 8]
00210AB4  mov      edx, ebx
00210AB6  call     0x21b2f0  ; -> 0021B2F0 fn
00210ABB  movzx    r8d, al
00210ABF  mov      rbx, qword ptr [rsp + 0x30]
00210AC4  xor      eax, eax
00210AC6  test     r8b, r8b
00210AC9  setne    al
00210ACC  add      rsp, 0x20
00210AD0  pop      rdi
00210AD1  ret      
```

## 00211220 (13 B, extent 00211220-0021122D)

Entered from (direct sites whose caller this page cites): `001DC240` + 0x35 (jmp; `001DC240` is cited on this page)
Other direct sites: none

Host context: " as 0 does). *Counted the same day, script side:* the only script verbs that carry a pan byte to this wrapper are 'voicepan' and 'voicechangepan' (both reach '002256F0' through the stream pan setter '001DC240' and '00225280'; 'sebsoundplay' has no pan argument in any of its 6,821 shipped calls). The 1,114 'us' scripts call them **18 times**: '64' eleven times, '96' once, and **six calls in the rear half** - '192' three times ('alc_b0400"

```
00211220  mov      rcx, qword ptr [rcx + 0x18]
00211224  movzx    r9d, r9b
00211228  jmp      0x21d640  ; -> 0021D640 fn
```

## 00217A60 (15 B, extent 00217A60-00217A6F)

Entered from (direct sites whose caller this page cites): `0020B680` + 0x191 (call; `0020B680` is cited on this page); `0020C300` + 0x11B (call; `0020C300` is cited on this page)
Other direct sites: none

Host context: "t '[aligned - 8]'; overflow and null failure both throw through '008C2608' / '008C2DA8'. Interior anchor '00209A27' (the 'add rax, 0x27' align step).  '00209AD0' (114 B) is the matching aligned free '0020B680', '0020C300' and the '00899520' family call: 'r8 * 4 >= 0x1000' selects the big-allocation path - 'rdx & 0x1F' must be 0, the raw block comes back from '[rdx - 8]', and the delta must sit in '8..0x27' before the '00210EB0' tail-fre" / "- 8]'; overflow and null failure both throw through '008C2608' / '008C2DA8'. Interior anchor '00209A27' (the 'add rax, 0x27' align step).  '00209AD0' (114 B) is the matching aligned free '0020B680', '0020C300' and the '00899520' family call: 'r8 * 4 >= 0x1000' selects the big-allocation path - 'rdx & 0x1F' must be 0, the raw block comes back from '[rdx - 8]', and the delta must sit in '8..0x27' before the '00210EB0' tail-free; every vio"

```
00217A60  mov      dword ptr [rcx + 8], r8d
00217A64  mov      rax, rcx
00217A67  mov      dword ptr [rcx + 0xc], r9d
00217A6B  mov      qword ptr [rcx], rdx
00217A6E  ret      
```

## 00218E20 (45 B, extent 00218E20-00218E4D)

Entered from (direct sites whose caller this page cites): `00210A40` + 0x3 (jmp; `00210A40` is cited on this page)
Other direct sites: none

Host context: "k >= 0 || DAT_0215EF44 >= 0) {     DAT_0215EF4D = 0x7F;     Music_SetLevel(newTrack >= 0 ? newTrack : DAT_0215EF44, 0x7F); } '''  '001DBC70' and '001DBCA0', the forward targets of that family, go to '00210A40'/'00210A50', which dereference slot **'+0x00'** — the 'MusicAudioController'. So music has its own controller, its own current-track handle and its own level, and the play call cannot reach any of them. A modder silencing sound eff"

```
00218E20  mov      rax, qword ptr [rcx + 8]
00218E24  lea      r9, [rcx + 8]
00218E28  cmp      rax, r9
00218E2B  je       0x218e4c  ; -> 00218E4C
00218E2D  nop      dword ptr [rax]
00218E30  mov      rcx, qword ptr [rax + 0x10]
00218E34  cmp      edx, -1
00218E37  je       0x218e47  ; -> 00218E47
00218E39  cmp      dword ptr [rcx + 0x50], edx
00218E3C  je       0x218e47  ; -> 00218E47
00218E3E  mov      rax, qword ptr [rax]
00218E41  cmp      rax, r9
00218E44  jne      0x218e30  ; -> 00218E30
00218E46  ret      
00218E47  jmp      0x222b20  ; -> 00222B20 fn
00218E4C  ret      
```
