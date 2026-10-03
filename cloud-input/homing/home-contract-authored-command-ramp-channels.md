# Homing pack: `17-Presentation-Rendering/CONTRACT-authored-command-ramp-channels.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-contract-authored-command-ramp-channels.json`.

Bodies: 8. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00185D80 (23 B, extent 00185D80-00185D97)

Entered from (direct sites whose caller this page cites): `001E0590` + 0xC (call; `001E0590` is cited on this page)
Other direct sites: none

Host context: "       request ('001E0560' at '0022A705': '01F82D30 |= 01F82D31'), and seven sites can clear it first ('001E0580', e.g.         '0022A6C1'). If it is still latched after the pass, '0017D6E0' resets ('001E0590'), zeroes the delta         ('0017D850' 'xorps xmm7, xmm7') and dispatches again ('0017D853'). The request is not re-raised on the second pass         ('0017D731' 'cmp ebx, 1'), so there are at most two passes. Because the ramp ste"

```
00185D80  mov      eax, dword ptr [rcx + 0xdbc]
00185D86  mov      dword ptr [rcx + 0xdc0], eax
00185D8C  mov      dword ptr [rcx + 0xdbc], 0
00185D96  ret      
```

## 002DF170 (17 B, extent 002DF170-002DF181)

Entered from (direct sites whose caller this page cites): `003B3EA0` + 0xE (call; `003B3EA0` is cited on this page)
Other direct sites: `0034D970` + 0x2D (jmp)

Host context: " feeds) calls ten '00360xxx'/'002DFxxx'/'00363xxx' Audio fade-and-mix helpers, '002628B0' calls '00360B50'/'00360DD0'/ '003636A0', '001D1660' calls '001DBB00'/'002DEBA0', '003B8670' calls '002DF660'/'003B3EA0', and the five '003D7Cxx'/'00332C40' callers reach '00181DD0'. Audio fades are ticked by the same frame bodies that advance the authored-command channels — shared cadence, no audio ownership crossing.  **Input — MECHANICAL (SWE2-CO"

```
002DF170  xor      r8d, r8d
002DF173  mov      r9d, edx
002DF176  mov      edx, ecx
002DF178  lea      ecx, [r8 + 1]
002DF17C  jmp      0x1dbf50  ; -> 001DBF50 fn
```

## 002ED530 (56 B, extent 002ED530-002ED568)

Entered from (direct sites whose caller this page cites): `004256E0` + 0x49D (call; `004256E0` is cited on this page); `004256E0` + 0x5F1 (call; `004256E0` is cited on this page)
Other direct sites: none

Host context: " '003E4890''s resolve leg   names '0020E600' (the image-address codec '002ED570'/'00409D60'/'0051FE30'/   '0051FF30' also consume on the Resource layer), '003E6DA0' (itself calling   '002ED570') and '004256E0' ('00409600'/'00409F50') — Resource-layer fan-in on   the codec and the lookup, no resource relationship to the ramp contract.   Edge list from 'edges.tsv' 2026-09-22.  ## Cross-subsystem neighbours — FINAL-AUDIT pass 22  **ActorEn" / " '003E4890''s resolve leg   names '0020E600' (the image-address codec '002ED570'/'00409D60'/'0051FE30'/   '0051FF30' also consume on the Resource layer), '003E6DA0' (itself calling   '002ED570') and '004256E0' ('00409600'/'00409F50') — Resource-layer fan-in on   the codec and the lookup, no resource relationship to the ramp contract.   Edge list from 'edges.tsv' 2026-09-22.  ## Cross-subsystem neighbours — FINAL-AUDIT pass 22  **ActorEn"

```
002ED530  push     rbx
002ED532  sub      rsp, 0x20
002ED536  mov      rbx, rcx
002ED539  test     rcx, rcx
002ED53C  je       0x2ed560  ; -> 002ED560
002ED53E  call     0x265760  ; -> 00265760 fn
002ED543  mov      rcx, rbx
002ED546  test     eax, eax
002ED548  je       0x2ed554  ; -> 002ED554
002ED54A  add      rsp, 0x20
002ED54E  pop      rbx
002ED54F  jmp      0x30beb0  ; -> 0030BEB0 fn
002ED554  xor      edx, edx
002ED556  add      rsp, 0x20
002ED55A  pop      rbx
002ED55B  jmp      0x2637d0  ; -> 002637D0 fn
002ED560  xor      eax, eax
002ED562  add      rsp, 0x20
002ED566  pop      rbx
002ED567  ret      
```

## 0041C200 (91 B, extent 0041C200-0041C25B)

Entered from (direct sites whose caller this page cites): `00418880` + 0x1B5F (call; `00418880` is cited on this page)
Other direct sites: none

Host context: "1D6F0', '0041D180', '0046D380' - the ramp-channel apply behind the fast-forward path.  Interior anchor '0041ADE6' (function '0041ADA0').  '0041D6F0' (154 B) is the channel-record copy '0041ADA0' and '00418880' share: '0020E600([rcx+0xA0])' resolves twice, '00409270' on '[rbx+0x27E]' then '00409300' - copying 'rbx+0xC0' or the stack xmmword into '[rbx+0xF0]' depending on 'byte[rbx+0x28B] & 4' - the slot-field update helper.  Interior anc"

```
0041C200  mov      r10, rcx
0041C203  test     r8, r8
0041C206  je       0x41c25a  ; -> 0041C25A
0041C208  mov      r8, qword ptr [rsp + 0x28]
0041C20D  test     r8, r8
0041C210  je       0x41c25a  ; -> 0041C25A
0041C212  test     byte ptr [rdx + 0x96], 0x20
0041C219  je       0x41c25a  ; -> 0041C25A
0041C21B  xor      edx, edx
0041C21D  cmp      dx, word ptr [rcx + 0x2bc]
0041C224  jge      0x41c25a  ; -> 0041C25A
0041C226  add      r8, 0x100
0041C22D  nop      dword ptr [rax]
0041C230  movsx    rax, word ptr [r8]
0041C234  lea      r8, [r8 + 0x108]
0041C23B  imul     rcx, rax, 0x290
0041C242  inc      edx
0041C244  and      word ptr [rcx + r9 + 0x280], 0xffef
0041C24E  movsx    eax, word ptr [r10 + 0x2bc]
0041C256  cmp      edx, eax
0041C258  jl       0x41c230  ; -> 0041C230
0041C25A  ret      
```

## 0041C6C0 (81 B, extent 0041C6C0-0041C711)

Entered from (direct sites whose caller this page cites): `0041DA90` + 0x1BF (call; `0041DA90` is cited on this page); `0041DA90` + 0x23E (call; `0041DA90` is cited on this page)
Other direct sites: none

Host context: "0x12 at '+0xC', '003E7D10(3)', '+0xC0' bit 0x40, the '+0x340' float, mode '02CA83F4' with '+0x284' bit 0x8000000 and 'word[+6] == -1', then 'word[+0x24] == 1' opens the arm - '0041CFC0', '0041D820', '0041DA90', '0041DD40', '004255B0' run the ramp re-emit under the entry's gates.  Interior anchor '0041C564' (function '0041C410').  '0042F030' (349 B) is the ramp tick '00426090' calls: '02CA48F8' global - '[rbx - 0x1C]' decrements while '[" / "0x12 at '+0xC', '003E7D10(3)', '+0xC0' bit 0x40, the '+0x340' float, mode '02CA83F4' with '+0x284' bit 0x8000000 and 'word[+6] == -1', then 'word[+0x24] == 1' opens the arm - '0041CFC0', '0041D820', '0041DA90', '0041DD40', '004255B0' run the ramp re-emit under the entry's gates.  Interior anchor '0041C564' (function '0041C410').  '0042F030' (349 B) is the ramp tick '00426090' calls: '02CA48F8' global - '[rbx - 0x1C]' decrements while '["

```
0041C6C0  push     rbx
0041C6C2  sub      rsp, 0x20
0041C6C6  mov      eax, 0x2008
0041C6CB  mov      rbx, rcx
0041C6CE  cmp      word ptr [rcx + 0x31c], ax
0041C6D5  jne      0x41c70b  ; -> 0041C70B
0041C6D7  test     dword ptr [rcx + 0xc], 0x200000
0041C6DE  jne      0x41c70b  ; -> 0041C70B
0041C6E0  mov      rax, qword ptr [rip + 0x2887d49]  ; -> 02CA4430
0041C6E7  test     rax, rax
0041C6EA  je       0x41c70b  ; -> 0041C70B
0041C6EC  mov      rcx, qword ptr [rcx + 0x2c0]
0041C6F3  test     rcx, rcx
0041C6F6  je       0x41c70b  ; -> 0041C70B
0041C6F8  lea      rdx, [rsp + 0x30]
0041C6FD  mov      byte ptr [rsp + 0x32], 2
0041C702  call     rax
0041C704  or       dword ptr [rbx + 0xc], 0x200000
0041C70B  add      rsp, 0x20
0041C70F  pop      rbx
0041C710  ret      
```

## 0041C720 (63 B, extent 0041C720-0041C75F)

Entered from (direct sites whose caller this page cites): `004256E0` + 0x5BD (call; `004256E0` is cited on this page)
Other direct sites: none

Host context: " '003E4890''s resolve leg   names '0020E600' (the image-address codec '002ED570'/'00409D60'/'0051FE30'/   '0051FF30' also consume on the Resource layer), '003E6DA0' (itself calling   '002ED570') and '004256E0' ('00409600'/'00409F50') — Resource-layer fan-in on   the codec and the lookup, no resource relationship to the ramp contract.   Edge list from 'edges.tsv' 2026-09-22.  ## Cross-subsystem neighbours — FINAL-AUDIT pass 22  **ActorEn"

```
0041C720  movsx    r8d, word ptr [rcx + 0x28]
0041C725  lea      rax, [rcx + 0x30]
0041C729  xor      r9d, r9d
0041C72C  mov      edx, r9d
0041C72F  test     r8d, r8d
0041C732  jle      0x41c74d  ; -> 0041C74D
0041C734  movsx    ecx, word ptr [rcx + 0x26]
0041C738  cmp      dword ptr [rax + 0x80], ecx
0041C73E  je       0x41c750  ; -> 0041C750
0041C740  inc      edx
0041C742  add      rax, 0xa0
0041C748  cmp      edx, r8d
0041C74B  jl       0x41c738  ; -> 0041C738
0041C74D  xor      eax, eax
0041C74F  ret      
0041C750  cmp      byte ptr [rax + 0x95], 1
0041C757  sete     r9b
0041C75B  mov      eax, r9d
0041C75E  ret      
```

## 00422D90 (70 B, extent 00422D90-00422DD6)

Entered from (direct sites whose caller this page cites): `004256E0` + 0x401 (call; `004256E0` is cited on this page)
Other direct sites: none

Host context: " '003E4890''s resolve leg   names '0020E600' (the image-address codec '002ED570'/'00409D60'/'0051FE30'/   '0051FF30' also consume on the Resource layer), '003E6DA0' (itself calling   '002ED570') and '004256E0' ('00409600'/'00409F50') — Resource-layer fan-in on   the codec and the lookup, no resource relationship to the ramp contract.   Edge list from 'edges.tsv' 2026-09-22.  ## Cross-subsystem neighbours — FINAL-AUDIT pass 22  **ActorEn"

```
00422D90  push     rbx
00422D92  sub      rsp, 0x20
00422D96  call     0x3ab7f0  ; -> 003AB7F0 fn
00422D9B  mov      rbx, rax
00422D9E  test     rax, rax
00422DA1  jne      0x422dab  ; -> 00422DAB
00422DA3  xor      eax, eax
00422DA5  add      rsp, 0x20
00422DA9  pop      rbx
00422DAA  ret      
00422DAB  xor      r8d, r8d
00422DAE  mov      edx, 0x4d524640
00422DB3  mov      rcx, rbx
00422DB6  call     0x408f90  ; -> 00408F90 fn
00422DBB  cmp      eax, -1
00422DBE  je       0x422da3  ; -> 00422DA3
00422DC0  mov      edx, eax
00422DC2  mov      rcx, rbx
00422DC5  call     0x408f80  ; -> 00408F80 fn
00422DCA  cdqe     
00422DCC  add      rax, 0x30
00422DD0  add      rsp, 0x20
00422DD4  pop      rbx
00422DD5  ret      
```

## 00512EC0 (22 B, extent 00512EC0-00512ED6)

Entered from (direct sites whose caller this page cites): `004256E0` + 0x271 (call; `004256E0` is cited on this page)
Other direct sites: none

Host context: " '003E4890''s resolve leg   names '0020E600' (the image-address codec '002ED570'/'00409D60'/'0051FE30'/   '0051FF30' also consume on the Resource layer), '003E6DA0' (itself calling   '002ED570') and '004256E0' ('00409600'/'00409F50') — Resource-layer fan-in on   the codec and the lookup, no resource relationship to the ramp contract.   Edge list from 'edges.tsv' 2026-09-22.  ## Cross-subsystem neighbours — FINAL-AUDIT pass 22  **ActorEn"

```
00512EC0  movzx    eax, byte ptr [rcx + 0xf]
00512EC4  and      al, 0xf
00512EC6  cmp      al, 1
00512EC8  jne      0x512ed2  ; -> 00512ED2
00512ECA  mov      ecx, dword ptr [rcx + 8]
00512ECD  jmp      0x2e9b80  ; -> 002E9B80 fn
00512ED2  or       eax, 0xffffffff
00512ED5  ret      
```
