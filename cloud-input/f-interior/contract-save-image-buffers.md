# F-interior pack: `19-Save-Load-Settings/CONTRACT-save-image-buffers.md`

Generated 2026-10-02 12:46 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/contract-save-image-buffers.json`.

Functions: 9. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (inbox mentions: ASTRA.md, SWE2-CONTRACT.md, SWE2-EC7.md). OPUS read these before packing.

## 00162370 (81 B, extent 00162370-001623C1)

Page context: "e '00D54348' vtable ('006160F4'/'006160FB'); '+0x30' then marks state 1 ('006160FF'), '+0xB8' and '+0x90..+0xB0' zero ('00616106'..'0061612B'), and 'rax=rbx' returns the object ('00616132'). Callers '00162370'/'0017E8E0'/'0017F3B0'/'00183A00'/'00183C60'/ '00183EE0'/'00184140'/'00184380'/'001B6D90'/'005D38D0'/'006123F0'/'00615840'/ '00874350' — the same '0017Exxx'/'00183xxx' save-buffer caller cluster as '0061E200'/'0062C360'.  ## SWE2-E"

```
00162370  sub      rsp, 0x38
00162374  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0016237D  lea      rcx, [rip + 0x2b59a7c]  ; -> 02CBBE00
00162384  call     0x6160b0  ; -> 006160B0 fn
00162389  nop      
0016238A  lea      rcx, [rip + 0x2b59bf7]  ; -> 02CBBF88
00162391  call     0x616140  ; -> 00616140 fn
00162396  nop      
00162397  lea      rcx, [rip + 0x2b59c7a]  ; -> 02CBC018
0016239E  call     0x6161a0  ; -> 006161A0 fn
001623A3  nop      
001623A4  lea      rcx, [rip + 0x2b59fbd]  ; -> 02CBC368
001623AB  call     0x615cd0  ; -> 00615CD0 fn
001623B0  nop      
001623B1  lea      rcx, [rip + 0x7493e8]  ; -> 008AB7A0
001623B8  add      rsp, 0x38
001623BC  jmp      0x808b90  ; -> 00808B90 fn
```

## 00185A50 (45 B, extent 00185A50-00185A7D)

Page context: "-dispatch'](../_experiments/evidence/texture-async-bank-dispatch/README.md), ACCEPTed by SWE2-AUDIT-SPEC ([review](../_index/candidates/auditspec-review-texture-async-bank-dispatch-0930/REVIEW.md)): '00185A50' submits with the bank current before the call, then sets '01F7F590' to the bank plus one, modulo 4, and returns it whatever the submission returned. '005FEA50' writes a 0x80-byte command (opcode '0x2F' at 0, the callback at '+8', "

```
00185A50  sub      rsp, 0x28
00185A54  mov      r8d, dword ptr [rip + 0x1df9b35]  ; -> 01F7F590
00185A5B  lea      rdx, [rip + 0xbae]  ; -> 00186610
00185A62  call     0x5fea50  ; -> 005FEA50 fn
00185A67  mov      eax, dword ptr [rip + 0x1df9b23]  ; -> 01F7F590
00185A6D  inc      eax
00185A6F  and      eax, 3
00185A72  mov      dword ptr [rip + 0x1df9b18], eax  ; -> 01F7F590
00185A78  add      rsp, 0x28
00185A7C  ret      
```

## 00186230 (125 B, extent 00186230-001862AD)

Page context: "ved fault.   - **The deferred-call queue the title cleanup uses.** Entries are 16-byte '{function, data}' pairs, in four     32-byte banks at 'ctx+0xC38+32*k', indexed by 'ctx[+0xCB8]'. The consumer '00186230' calls 'function(data)'     with RCX = data ('00186230+0x43', '+0x47'). The flush '00185C20' is called by the per-frame pump only when     '01FD4A68' is zero, at most once per pump call. The getter '00189120' takes no argument.   -"

```
00186230  mov      qword ptr [rsp + 8], rbx
00186235  mov      qword ptr [rsp + 0x10], rsi
0018623A  push     rdi
0018623B  sub      rsp, 0x20
0018623F  mov      eax, dword ptr [rcx + 0xcb8]
00186245  mov      rsi, rcx
00186248  inc      eax
0018624A  and      eax, 3
0018624D  mov      dword ptr [rcx + 0xcb8], eax
00186253  movsxd   rbx, eax
00186256  lea      rax, [rbx + 0x62]
0018625A  shl      rbx, 5
0018625E  shl      rax, 5
00186262  mov      rbx, qword ptr [rbx + rcx + 0xc38]
0018626A  mov      rdi, qword ptr [rax + rcx]
0018626E  cmp      rbx, rdi
00186271  je       0x186282  ; -> 00186282
00186273  mov      rcx, qword ptr [rbx + 8]
00186277  call     qword ptr [rbx]
00186279  add      rbx, 0x10
0018627D  cmp      rbx, rdi
00186280  jne      0x186273  ; -> 00186273
00186282  movsxd   rcx, dword ptr [rsi + 0xcb8]
00186289  mov      rbx, qword ptr [rsp + 0x30]
0018628E  shl      rcx, 5
00186292  mov      rax, qword ptr [rcx + rsi + 0xc38]
0018629A  mov      qword ptr [rcx + rsi + 0xc40], rax
001862A2  mov      rsi, qword ptr [rsp + 0x38]
001862A7  add      rsp, 0x20
001862AB  pop      rdi
001862AC  ret      
```

## 00186610 (15 B, extent 00186610-0018661F)

Page context: "ns it whatever the submission returned. '005FEA50' writes a 0x80-byte command (opcode '0x2F' at 0, the callback at '+8', the data at '+0x10'), or returns 0xD when it cannot reserve one. The callback '00186610' reads the bank at '+0x10' and the current context and tails '0062EBC0', which calls each key's virtual slot 0 before taking the tree successor, then frees the tree and resets the bank's count '+0x28'. Which interpreter executes op"

```
00186610  mov      edx, dword ptr [rcx + 0x10]
00186613  mov      rcx, qword ptr [rip + 0x1df8f9e]  ; -> 01F7F5B8
0018661A  jmp      0x62ebc0  ; -> 0062EBC0 fn
```

## 001AA0A0 (116 B, extent 001AA0A0-001AA114)

Page context: "'00180C80'/'001B11D0'/'001B1C00'. Interior anchor '001815A2' (a '001B1C00' call).    ## SWE2-EC7-65 update (2026-09-19) - '00686D40'  '00686D40' (135 B) is the save-image serializer's element body - '001AA0A0'/'001B7CE0'. Interior anchor '00686DAB' (a '001B7CE0' call).   ## SWE2-EC7-67 update - '00679570'  '00679570' (129 B) is a save-buffer helper - single call then tail '00861EBA'. Interior anchor '006795CA' (a '00861EBA' call).  ## S"

```
001AA0A0  mov      r9, qword ptr [rcx + 0x28]
001AA0A4  test     r9, r9
001AA0A7  je       0x1aa103  ; -> 001AA103
001AA0A9  mov      r8, qword ptr [r9 + 0x50]
001AA0AD  mov      r10d, dword ptr [r8 + 0x38]
001AA0B1  mov      dword ptr [rcx + 0x10], r10d
001AA0B5  mov      rax, qword ptr [r9 + 0x60]
001AA0B9  mov      qword ptr [rcx], rax
001AA0BC  mov      edx, dword ptr [r9 + 0x74]
001AA0C0  mov      dword ptr [rcx + 0x14], edx
001AA0C3  mov      eax, dword ptr [r8 + 0xf8]
001AA0CA  mov      dword ptr [rcx + 0x18], eax
001AA0CD  mov      r8, qword ptr [r9 + 0x10]
001AA0D1  mov      qword ptr [rcx + 8], r8
001AA0D5  test     edx, edx
001AA0D7  je       0x1aa113  ; -> 001AA113
001AA0D9  mov      rax, qword ptr [rcx]
001AA0DC  cmp      rax, r8
001AA0DF  jne      0x1aa113  ; -> 001AA113
001AA0E1  nop      dword ptr [rax]
001AA0E5  nop      word ptr [rax + rax]
001AA0F0  add      rax, r10
001AA0F3  mov      qword ptr [rcx], rax
001AA0F6  mov      r8, qword ptr [r8]
001AA0F9  mov      qword ptr [rcx + 8], r8
001AA0FD  cmp      rax, r8
001AA100  je       0x1aa0f0  ; -> 001AA0F0
001AA102  ret      
001AA103  xor      eax, eax
001AA105  mov      qword ptr [rcx], rax
001AA108  mov      qword ptr [rcx + 8], rax
001AA10C  mov      qword ptr [rcx + 0x10], rax
001AA110  mov      dword ptr [rcx + 0x18], eax
001AA113  ret      
```

## 001B11D0 (105 B, extent 001B11D0-001B1239)

Page context: "e. Interior anchor '0060DE2C' (the '+0x28' compare).    ## SWE2-EC7-64 update (2026-09-19) - '00181580'  '00181580' (139 B) is the save-buffer caller of '00180A70' - '0016D6A0'/'00180A70'/'00180C80'/'001B11D0'/'001B1C00'. Interior anchor '001815A2' (a '001B1C00' call).    ## SWE2-EC7-65 update (2026-09-19) - '00686D40'  '00686D40' (135 B) is the save-image serializer's element body - '001AA0A0'/'001B7CE0'. Interior anchor '00686DAB' (a "

```
001B11D0  push     rbx
001B11D2  sub      rsp, 0x20
001B11D6  mov      rbx, rcx
001B11D9  call     0x1b1440  ; -> 001B1440 fn
001B11DE  mov      rdx, qword ptr [rbx + 0x2218]
001B11E5  lea      r8, [rbx + 0x2208]
001B11EC  mov      rcx, r8
001B11EF  test     rdx, rdx
001B11F2  je       0x1b120a  ; -> 001B120A
001B11F4  cmp      dword ptr [rdx + 0x20], eax
001B11F7  jb       0x1b1202  ; -> 001B1202
001B11F9  mov      rcx, rdx
001B11FC  mov      rdx, qword ptr [rdx + 8]
001B1200  jmp      0x1b1205  ; -> 001B1205
001B1202  mov      rdx, qword ptr [rdx]
001B1205  test     rdx, rdx
001B1208  jne      0x1b11f4  ; -> 001B11F4
001B120A  cmp      rcx, r8
001B120D  je       0x1b1214  ; -> 001B1214
001B120F  cmp      eax, dword ptr [rcx + 0x20]
001B1212  jae      0x1b1217  ; -> 001B1217
001B1214  mov      rcx, r8
001B1217  lea      rax, [rbx + 0x2208]
001B121E  cmp      rcx, rax
001B1221  je       0x1b1231  ; -> 001B1231
001B1223  mov      rcx, qword ptr [rcx + 0x28]
001B1227  add      rsp, 0x20
001B122B  pop      rbx
001B122C  jmp      0x6b5c60  ; -> 006B5C60 fn
001B1231  xor      eax, eax
001B1233  add      rsp, 0x20
001B1237  pop      rbx
001B1238  ret      
```

## 0028E630 (37 B, extent 0028E630-0028E655)

Page context: "then '002903D0([+0x3E8])' + '002903F0(6)' and tails '0028E790'; bit 8 clear uses widget '0x6E' with the '01E0C3BC'/'01E0C3E0' constants and a zero-arg '002C9490', then '002903D0([+0x3E8])' and tails '0028E630' - both arms run '002CD7B0' first when bit 9 is set  Interior anchor '0028056B' (function '002804E0').  ## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)  **Presentation — BOTH DIRECTIONS, 156 edges: ~~the save"

```
0028E630  push     rbx
0028E632  sub      rsp, 0x20
0028E636  mov      ebx, ecx
0028E638  mov      edx, 6
0028E63D  xor      ecx, ecx
0028E63F  call     0x2b9d30  ; -> 002B9D30 fn
0028E644  mov      ecx, ebx
0028E646  call     0x2b9fe0  ; -> 002B9FE0 fn
0028E64B  add      rsp, 0x20
0028E64F  pop      rbx
0028E650  jmp      0x2ba040  ; -> 002BA040 fn
```

## 00623DF0 (56 B, extent 00623DF0-00623E28)

Page context: "andidates/astra-returns-title-fable-1002/README.md)). These narrow the list above for channel 0   and say nothing about channels 1 and 2:   - **Count and selector.** n is the low 31 bits of '+0x30' ('00623DF0' clears bit 31 with 'btr' before it     compares). Bit 31 is ignored by the selector and gates '00584730'. Records are '0x58' bytes. '00623DF0'     returns 'base + 0x58 * k + 0x38', the address of a record's '+0x38' field, not a re"

```
00623DF0  mov      eax, dword ptr [rcx + 0x30]
00623DF3  btr      eax, 0x1f
00623DF7  cmp      eax, 1
00623DFA  jbe      0x623e0e  ; -> 00623E0E
00623DFC  mov      r8, qword ptr [rcx + 0x38]
00623E00  mov      eax, edx
00623E02  imul     rax, rax, 0x58
00623E06  add      rax, 0x38
00623E0A  add      rax, r8
00623E0D  ret      
00623E0E  lea      r8, [rcx + 0x38]
00623E12  xor      ecx, ecx
00623E14  test     eax, eax
00623E16  mov      eax, edx
00623E18  cmove    r8, rcx
00623E1C  imul     rax, rax, 0x58
00623E20  add      rax, 0x38
00623E24  add      rax, r8
00623E27  ret      
```

## 0062EBC0 (167 B, extent 0062EBC0-0062EC67)

Page context: "ommand (opcode '0x2F' at 0, the callback at '+8', the data at '+0x10'), or returns 0xD when it cannot reserve one. The callback '00186610' reads the bank at '+0x10' and the current context and tails '0062EBC0', which calls each key's virtual slot 0 before taking the tree successor, then frees the tree and resets the bank's count '+0x28'. Which interpreter executes opcode '0x2F' is open. - Open across all four: real callers, threads and "

```
0062EBC0  mov      qword ptr [rsp + 0x10], rbx
0062EBC5  mov      qword ptr [rsp + 0x18], rsi
0062EBCA  push     rdi
0062EBCB  sub      rsp, 0x20
0062EBCF  mov      eax, edx
0062EBD1  imul     rsi, rax, 0x38
0062EBD5  add      rsi, rcx
0062EBD8  mov      rbx, qword ptr [rsi + 0x10]
0062EBDC  lea      rdi, [rsi + 8]
0062EBE0  cmp      rbx, rdi
0062EBE3  je       0x62ebfe  ; -> 0062EBFE
0062EBE5  mov      rcx, qword ptr [rbx + 0x20]
0062EBE9  mov      rax, qword ptr [rcx]
0062EBEC  call     qword ptr [rax]
0062EBEE  mov      rcx, rbx
0062EBF1  call     0x16d6d0  ; -> 0016D6D0 fn
0062EBF6  mov      rbx, rax
0062EBF9  cmp      rax, rdi
0062EBFC  jne      0x62ebe5  ; -> 0062EBE5
0062EBFE  mov      rdi, qword ptr [rsi + 0x18]
0062EC02  test     rdi, rdi
0062EC05  je       0x62ec40  ; -> 0062EC40
0062EC07  mov      qword ptr [rsp + 0x30], r14
0062EC0C  nop      dword ptr [rax]
0062EC10  mov      rdx, qword ptr [rdi]
0062EC13  mov      rcx, rsi
0062EC16  call     0x220390  ; -> 00220390 fn
0062EC1B  mov      rax, qword ptr [rsi + 0x30]
0062EC1F  lea      rcx, [rsi + 0x30]
0062EC23  mov      rbx, qword ptr [rdi + 8]
0062EC27  mov      r8d, 0x28
0062EC2D  mov      rdx, rdi
0062EC30  call     qword ptr [rax + 0x18]
0062EC33  mov      rdi, rbx
0062EC36  test     rbx, rbx
0062EC39  jne      0x62ec10  ; -> 0062EC10
0062EC3B  mov      r14, qword ptr [rsp + 0x30]
0062EC40  mov      rbx, qword ptr [rsp + 0x38]
0062EC45  lea      rax, [rsi + 8]
0062EC49  mov      qword ptr [rsi + 0x10], rax
0062EC4D  mov      qword ptr [rax], rax
0062EC50  xor      eax, eax
0062EC52  mov      qword ptr [rsi + 0x18], rax
0062EC56  mov      byte ptr [rsi + 0x20], al
0062EC59  mov      dword ptr [rsi + 0x28], eax
0062EC5C  mov      rsi, qword ptr [rsp + 0x40]
0062EC61  add      rsp, 0x20
0062EC65  pop      rdi
0062EC66  ret      
```
