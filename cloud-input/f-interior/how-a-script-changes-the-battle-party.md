# F-interior pack: `01-Script-VM-Native-Bridge/Party-Presentation-Verbs/how-a-script-changes-the-battle-party.md`

Generated 2026-10-02 10:27 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/how-a-script-changes-the-battle-party.json`.

Functions: 8. Each is cited on the page only at its entry and is still in the F frontier.

## 00324360 (23 B, extent 00324360-00324377)

Page context: "d from the authority image and read whole, 2026-09-19 - four begin callbacks     (0034D4E0, 00350CD0, 00350160, 00352AF0), two polls (003506A0, 0034CDF0), the pending test 003596B0 and its callee     00324360, the roster-contains test 003596D0, the two mask builders 00359BA0 and 00359C00 and the non-guest collector     00320800; the verbs located in the dispatch table by the accessor frame (begin at tbl + 0x20n + 8, poll at + 0x10) and "

```
00324360  sub      rsp, 0x28
00324364  call     0x37cb50  ; -> 0037CB50 fn
00324369  xor      ecx, ecx
0032436B  test     eax, eax
0032436D  setne    cl
00324370  mov      eax, ecx
00324372  add      rsp, 0x28
00324376  ret      
```

## 0034CDF0 (97 B, extent 0034CDF0-0034CE51)

Page context: "adb36493d5d1d89721f8   method: eleven bodies disassembled from the authority image and read whole, 2026-09-19 - four begin callbacks     (0034D4E0, 00350CD0, 00350160, 00352AF0), two polls (003506A0, 0034CDF0), the pending test 003596B0 and its callee     00324360, the roster-contains test 003596D0, the two mask builders 00359BA0 and 00359C00 and the non-guest collector     00320800; the verbs located in the dispatch table by the access"

```
0034CDF0  push     rbx
0034CDF2  sub      rsp, 0x20
0034CDF6  mov      ecx, dword ptr [r8]
0034CDF9  mov      rbx, r8
0034CDFC  test     ecx, ecx
0034CDFE  je       0x34ce25  ; -> 0034CE25
0034CE00  sub      ecx, 1
0034CE03  je       0x34ce2c  ; -> 0034CE2C
0034CE05  cmp      ecx, 1
0034CE08  jne      0x34ce46  ; -> 0034CE46
0034CE0A  call     0x3596b0  ; -> 003596B0 fn
0034CE0F  mov      ebx, eax
0034CE11  test     eax, eax
0034CE13  jne      0x34ce4b  ; -> 0034CE4B
0034CE15  lea      ecx, [rax + 0x13]
0034CE18  call     0x3601c0  ; -> 003601C0 fn
0034CE1D  mov      eax, ebx
0034CE1F  add      rsp, 0x20
0034CE23  pop      rbx
0034CE24  ret      
0034CE25  mov      dword ptr [r8], 1
0034CE2C  movzx    ecx, byte ptr [r8 + 4]
0034CE31  call     0x328b20  ; -> 00328B20 fn
0034CE36  mov      ecx, 0x13
0034CE3B  call     0x3601b0  ; -> 003601B0 fn
0034CE40  mov      dword ptr [rbx], 2
0034CE46  mov      eax, 1
0034CE4B  add      rsp, 0x20
0034CE4F  pop      rbx
0034CE50  ret      
```

## 003596B0 (24 B, extent 003596B0-003596C8)

Page context: "d: eleven bodies disassembled from the authority image and read whole, 2026-09-19 - four begin callbacks     (0034D4E0, 00350CD0, 00350160, 00352AF0), two polls (003506A0, 0034CDF0), the pending test 003596B0 and its callee     00324360, the roster-contains test 003596D0, the two mask builders 00359BA0 and 00359C00 and the non-guest collector     00320800; the verbs located in the dispatch table by the accessor frame (begin at tbl + 0x2"

```
003596B0  sub      rsp, 0x28
003596B4  call     0x324360  ; -> 00324360 fn
003596B9  xor      ecx, ecx
003596BB  cmp      eax, 1
003596BE  setne    cl
003596C1  mov      eax, ecx
003596C3  add      rsp, 0x28
003596C7  ret      
```

## 003596D0 (107 B, extent 003596D0-0035973B)

Page context: " whole, 2026-09-19 - four begin callbacks     (0034D4E0, 00350CD0, 00350160, 00352AF0), two polls (003506A0, 0034CDF0), the pending test 003596B0 and its callee     00324360, the roster-contains test 003596D0, the two mask builders 00359BA0 and 00359C00 and the non-guest collector     00320800; the verbs located in the dispatch table by the accessor frame (begin at tbl + 0x20n + 8, poll at + 0x10) and     named from the bundled communit"

```
003596D0  push     rbx
003596D2  sub      rsp, 0x40
003596D6  mov      rax, qword ptr [rip + 0x1beb153]  ; -> 01F44830 [u64 0x00002B992DDFA232]
003596DD  xor      rax, rsp
003596E0  mov      qword ptr [rsp + 0x30], rax
003596E5  mov      ebx, ecx
003596E7  mov      edx, 4
003596EC  lea      rcx, [rsp + 0x20]
003596F1  call     0x31b510  ; -> 0031B510 fn
003596F6  xor      edx, edx
003596F8  movsxd   r8, eax
003596FB  test     eax, eax
003596FD  jle      0x35970e  ; -> 0035970E
003596FF  nop      
00359700  cmp      ebx, dword ptr [rsp + rdx*4 + 0x20]
00359704  je       0x359723  ; -> 00359723
00359706  inc      rdx
00359709  cmp      rdx, r8
0035970C  jl       0x359700  ; -> 00359700
0035970E  xor      eax, eax
00359710  mov      rcx, qword ptr [rsp + 0x30]
00359715  xor      rcx, rsp
00359718  call     0x808c40  ; -> 00808C40 fn
0035971D  add      rsp, 0x40
00359721  pop      rbx
00359722  ret      
00359723  mov      eax, 1
00359728  mov      rcx, qword ptr [rsp + 0x30]
0035972D  xor      rcx, rsp
00359730  call     0x808c40  ; -> 00808C40 fn
00359735  add      rsp, 0x40
00359739  pop      rbx
0035973A  ret      
```

## 00359740 (107 B, extent 00359740-003597AB)

Page context: "oster? collects slots 0-3 and compares | | '00359BA0' (93 B) | bit mask of the runtime roster's selectors | | '00359C00' (93 B) | bit mask of every **non-guest** selector in all nine party slots | | '00359740' (107 B) | is this selector among the non-guest members of all nine slots? the same collection, compared | | '00320800' (144 B) | the collector under it: for slots 0-8, a valid slot's selector is kept when it is 6 or below, or '0x1"

```
00359740  push     rbx
00359742  sub      rsp, 0x50
00359746  mov      rax, qword ptr [rip + 0x1beb0e3]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0035974D  xor      rax, rsp
00359750  mov      qword ptr [rsp + 0x48], rax
00359755  mov      ebx, ecx
00359757  mov      edx, 9
0035975C  lea      rcx, [rsp + 0x20]
00359761  call     0x320800  ; -> 00320800 fn
00359766  xor      edx, edx
00359768  movsxd   r8, eax
0035976B  test     eax, eax
0035976D  jle      0x35977e  ; -> 0035977E
0035976F  nop      
00359770  cmp      ebx, dword ptr [rsp + rdx*4 + 0x20]
00359774  je       0x359793  ; -> 00359793
00359776  inc      rdx
00359779  cmp      rdx, r8
0035977C  jl       0x359770  ; -> 00359770
0035977E  xor      eax, eax
00359780  mov      rcx, qword ptr [rsp + 0x48]
00359785  xor      rcx, rsp
00359788  call     0x808c40  ; -> 00808C40 fn
0035978D  add      rsp, 0x50
00359791  pop      rbx
00359792  ret      
00359793  mov      eax, 1
00359798  mov      rcx, qword ptr [rsp + 0x48]
0035979D  xor      rcx, rsp
003597A0  call     0x808c40  ; -> 00808C40 fn
003597A5  add      rsp, 0x50
003597A9  pop      rbx
003597AA  ret      
```

## 00359BA0 (93 B, extent 00359BA0-00359BFD)

Page context: "callbacks     (0034D4E0, 00350CD0, 00350160, 00352AF0), two polls (003506A0, 0034CDF0), the pending test 003596B0 and its callee     00324360, the roster-contains test 003596D0, the two mask builders 00359BA0 and 00359C00 and the non-guest collector     00320800; the verbs located in the dispatch table by the accessor frame (begin at tbl + 0x20n + 8, poll at + 0x10) and     named from the bundled community catalogue, an external authore"

```
00359BA0  push     rbx
00359BA2  sub      rsp, 0x40
00359BA6  mov      rax, qword ptr [rip + 0x1beac83]  ; -> 01F44830 [u64 0x00002B992DDFA232]
00359BAD  xor      rax, rsp
00359BB0  mov      qword ptr [rsp + 0x30], rax
00359BB5  xor      ebx, ebx
00359BB7  lea      rcx, [rsp + 0x20]
00359BBC  lea      edx, [rbx + 4]
00359BBF  call     0x31b510  ; -> 0031B510 fn
00359BC4  movsxd   r9, eax
00359BC7  mov      edx, ebx
00359BC9  test     eax, eax
00359BCB  jle      0x359be8  ; -> 00359BE8
00359BCD  nop      dword ptr [rax]
00359BD0  mov      ecx, dword ptr [rsp + rdx*4 + 0x20]
00359BD4  mov      r8d, 1
00359BDA  shl      r8d, cl
00359BDD  inc      rdx
00359BE0  or       ebx, r8d
00359BE3  cmp      rdx, r9
00359BE6  jl       0x359bd0  ; -> 00359BD0
00359BE8  mov      eax, ebx
00359BEA  mov      rcx, qword ptr [rsp + 0x30]
00359BEF  xor      rcx, rsp
00359BF2  call     0x808c40  ; -> 00808C40 fn
00359BF7  add      rsp, 0x40
00359BFB  pop      rbx
00359BFC  ret      
```

## 00359C00 (93 B, extent 00359C00-00359C5D)

Page context: " (0034D4E0, 00350CD0, 00350160, 00352AF0), two polls (003506A0, 0034CDF0), the pending test 003596B0 and its callee     00324360, the roster-contains test 003596D0, the two mask builders 00359BA0 and 00359C00 and the non-guest collector     00320800; the verbs located in the dispatch table by the accessor frame (begin at tbl + 0x20n + 8, poll at + 0x10) and     named from the bundled community catalogue, an external authored source last"

```
00359C00  push     rbx
00359C02  sub      rsp, 0x50
00359C06  mov      rax, qword ptr [rip + 0x1beac23]  ; -> 01F44830 [u64 0x00002B992DDFA232]
00359C0D  xor      rax, rsp
00359C10  mov      qword ptr [rsp + 0x48], rax
00359C15  xor      ebx, ebx
00359C17  lea      rcx, [rsp + 0x20]
00359C1C  lea      edx, [rbx + 9]
00359C1F  call     0x320800  ; -> 00320800 fn
00359C24  movsxd   r9, eax
00359C27  mov      edx, ebx
00359C29  test     eax, eax
00359C2B  jle      0x359c48  ; -> 00359C48
00359C2D  nop      dword ptr [rax]
00359C30  mov      ecx, dword ptr [rsp + rdx*4 + 0x20]
00359C34  mov      r8d, 1
00359C3A  shl      r8d, cl
00359C3D  inc      rdx
00359C40  or       ebx, r8d
00359C43  cmp      rdx, r9
00359C46  jl       0x359c30  ; -> 00359C30
00359C48  mov      eax, ebx
00359C4A  mov      rcx, qword ptr [rsp + 0x48]
00359C4F  xor      rcx, rsp
00359C52  call     0x808c40  ; -> 00808C40 fn
00359C57  add      rsp, 0x50
00359C5B  pop      rbx
00359C5C  ret      
```

## 0037CB50 (46 B, extent 0037CB50-0037CB7E)

Page context: "k routine, which was not read.  ## 4. The polls  **'003506A0' (33 B), shared by six verbs.** It asks whether a party mutation is still pending ('003596B0', 24 B: true unless '00324360', a boolean of '0037CB50', answers exactly 1). **'0037CB50' (46 B, read whole 2026-09-19) is the end test of the party read-in task**: it answers 1 when no read-in task exists, or when the task's slot cursor has left the roster - past slot 3 when its step "

```
0037CB50  cmp      qword ptr [rip + 0x2b428a8], 0  ; -> 02EBF400
0037CB58  je       0x37cb6c  ; -> 0037CB6C
0037CB5A  cmp      byte ptr [rip + 0x2b4289c], 0  ; -> 02EBF3FD
0037CB61  jle      0x37cb72  ; -> 0037CB72
0037CB63  cmp      byte ptr [rip + 0x2b42894], 4  ; -> 02EBF3FE
0037CB6A  jl       0x37cb7b  ; -> 0037CB7B
0037CB6C  mov      eax, 1
0037CB71  ret      
0037CB72  cmp      byte ptr [rip + 0x2b42885], 0  ; -> 02EBF3FE
0037CB79  jl       0x37cb6c  ; -> 0037CB6C
0037CB7B  xor      eax, eax
0037CB7D  ret      
```
