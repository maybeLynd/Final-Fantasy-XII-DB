# F-interior pack: `16-UI/Request-Router/ui-request-router.md`

Generated 2026-10-02 23:37 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/ui-request-router.json`.

Functions: 8. Each is cited on the page only at its entry and is still in the F frontier.

## 001986E0 (24 B, extent 001986E0-001986F8)

Page context: "lay_ArbitrateDigitalInputAndModalState ('00253C70'), '00291D90', '002E09A0'; '00182D40', '00226280', '00228C70', '0022A580' (+8 more) reach bodies filed to Input: '0017DE10', '00182D40', '00182D80', '001986E0' (+18 more) - shared machinery across the layer boundary, no shared ownership. - **InputGameplay - CLIENT (2 edges).** '002E1C20', '002E1CA0' are called by bodies filed to InputGameplay: '00313A00' - shared machinery across the lay"

```
001986E0  movsx    edx, byte ptr [rcx + 0x3a]
001986E4  mov      eax, edx
001986E6  shr      eax, 2
001986E9  test     al, 1
001986EB  je       0x1986f7  ; -> 001986F7
001986ED  and      dl, 0xfb
001986F0  mov      byte ptr [rcx + 0x3b], 1
001986F4  mov      byte ptr [rcx + 0x3a], dl
001986F7  ret      
```

## 0020E5C0 (61 B, extent 0020E5C0-0020E5FD)

Page context: "/Widget-Object-Model/the-widget-message-protocol.md)). Request 6's arm ('0027F8DB') prepares the image — parameter 0: '003C60F0', then, if still 0, 'SaveTransition_PrepareRuntimeImageForCapture' and '0020E5C0'; otherwise 'SaveImage_BackupActiveRuntimeBuffer' — and calls **'SaveLoad_OpenController(parameter, 1)'** ('0027F984'), which builds the '0x5A0'-byte controller '00582860' with a boolean '1' that its message 1 turns into '+0xC4' bi"

```
0020E5C0  mov      qword ptr [rsp + 8], rbx
0020E5C5  mov      qword ptr [rsp + 0x10], rsi
0020E5CA  push     rdi
0020E5CB  sub      rsp, 0x20
0020E5CF  mov      rbx, r8
0020E5D2  mov      rdi, rdx
0020E5D5  mov      rsi, rcx
0020E5D8  call     0x1c18e0  ; -> 001C18E0 fn
0020E5DD  mov      rcx, rax
0020E5E0  mov      r9, rbx
0020E5E3  mov      r8, rdi
0020E5E6  mov      rdx, rsi
0020E5E9  mov      rbx, qword ptr [rsp + 0x30]
0020E5EE  mov      rsi, qword ptr [rsp + 0x38]
0020E5F3  add      rsp, 0x20
0020E5F7  pop      rdi
0020E5F8  jmp      0x16d6a0  ; -> 0016D6A0 fn
```

## 0024AB30 (42 B, extent 0024AB30-0024AB5A)

Page context: "'002802D1'–'00280345'): only when '00251D50()' and '003CA0F0()' are non-zero,   context '+0x300'/'+0x308' are null, and roots '0208EA30' and '0208EA20' have no children, '00245020(self)', state 0,   '0024AB30'.  **Its message 18** ('00280184'–'002802A0'), after '0024AB60' if context '+0xDF4', '003667B0(0)', '00365980' and, by the request class message 1 stored at '+0xC8', '00254440(0, 0x80)' or '00254480(0, 0x80)': **bit 9** → clear 9 a"

```
0024AB30  sub      rsp, 0x28
0024AB34  cmp      dword ptr [rip + 0x1e46559], 0  ; -> 02091094
0024AB3B  je       0x24ab55  ; -> 0024AB55
0024AB3D  call     0x37b330  ; -> 0037B330 fn
0024AB42  cmp      eax, 4
0024AB45  je       0x24ab55  ; -> 0024AB55
0024AB47  mov      ecx, 0x80000
0024AB4C  add      rsp, 0x28
0024AB50  jmp      0x16d6a0  ; -> 0016D6A0 fn
0024AB55  add      rsp, 0x28
0024AB59  ret      
```

## 00290780 (97 B, extent 00290780-002907E1)

Page context: "280140' (message   18, '00280286'), request 12's arm '0028E970', request 24's widget, '0035C960', '0035CF50', '0035D8D0', '0035DA80', the   '003C8990'–'003C8B70' bodies (seven sites), '00279E20' and '00290780'. The area   unload '002628B0' runs the reset '00252DE0', which zeroes both words too. Image-wide, '02092734' has exactly these   two writers and the setter '00252B46'. - **R2, R3. Request 24, "party incapacitated".** '0035D6B0' se"

```
00290780  sub      rsp, 0x28
00290784  test     ecx, ecx
00290786  je       0x2907c0  ; -> 002907C0
00290788  cmp      ecx, 1
0029078B  jne      0x2907dc  ; -> 002907DC
0029078D  mov      rax, qword ptr [rip + 0x1e0b6ec]  ; -> 0209BE80
00290794  mov      rcx, qword ptr [rax + 0x10fb0]
0029079B  test     rcx, rcx
0029079E  je       0x2907dc  ; -> 002907DC
002907A0  call     0x245020  ; -> 00245020 fn
002907A5  mov      rax, qword ptr [rip + 0x1e0b6d4]  ; -> 0209BE80
002907AC  mov      qword ptr [rax + 0x10fb0], 0
002907B7  add      rsp, 0x28
002907BB  jmp      0x252d90  ; -> 00252D90 fn
002907C0  mov      rax, qword ptr [rip + 0x1e0b6b9]  ; -> 0209BE80
002907C7  mov      rcx, qword ptr [rax + 0x10fb0]
002907CE  test     rcx, rcx
002907D1  je       0x2907dc  ; -> 002907DC
002907D3  add      rsp, 0x28
002907D7  jmp      0x244dd0  ; -> 00244DD0 fn
002907DC  add      rsp, 0x28
002907E0  ret      
```

## 002E0E30 (236 B, extent 002E0E30-002E0F1C)

Page context: "ng else '0' ('002E1A81'–'002E1AA1') — so they belong to request 22's sub-modes, of which the shipped scripts author '0x42' (once) and '0x40' (once); '0x21''s producer is not among the script calls.  '002E0E30' is the inverse for *current* fullscreen mode: it accepts modes '0..19' and maps them back to request IDs. **Mode 14 maps back to request 14** - which is why request 14 is structurally real even though no ordinary producer emits it"

```
002E0E30  sub      rsp, 0x28
002E0E34  call     0x28f5f0  ; -> 0028F5F0 fn
002E0E39  cmp      eax, 0x13
002E0E3C  ja       0x2e0f15  ; -> 002E0F15
002E0E42  lea      rdx, [rip - 0x1c0e49]  ; -> 00120000 (image base)
002E0E49  cdqe     
002E0E4B  mov      ecx, dword ptr [rdx + rax*4 + 0x1c0f1c]  ; image base + 0x1c0f1c = 002E0F1C
002E0E52  add      rcx, rdx
002E0E55  jmp      rcx
002E0E57  mov      eax, 1
002E0E5C  add      rsp, 0x28
002E0E60  ret      
002E0E61  mov      eax, 2
002E0E66  add      rsp, 0x28
002E0E6A  ret      
002E0E6B  mov      eax, 3
002E0E70  add      rsp, 0x28
002E0E74  ret      
002E0E75  mov      eax, 4
002E0E7A  add      rsp, 0x28
002E0E7E  ret      
002E0E7F  mov      eax, 5
002E0E84  add      rsp, 0x28
002E0E88  ret      
002E0E89  mov      eax, 6
002E0E8E  add      rsp, 0x28
002E0E92  ret      
002E0E93  mov      eax, 7
002E0E98  add      rsp, 0x28
002E0E9C  ret      
002E0E9D  mov      eax, 8
002E0EA2  add      rsp, 0x28
002E0EA6  ret      
002E0EA7  mov      eax, 9
002E0EAC  add      rsp, 0x28
002E0EB0  ret      
002E0EB1  mov      eax, 0xa
002E0EB6  add      rsp, 0x28
002E0EBA  ret      
002E0EBB  mov      eax, 0xb
002E0EC0  add      rsp, 0x28
002E0EC4  ret      
002E0EC5  mov      eax, 0xc
002E0ECA  add      rsp, 0x28
002E0ECE  ret      
002E0ECF  mov      eax, 0xd
002E0ED4  add      rsp, 0x28
002E0ED8  ret      
002E0ED9  mov      eax, 0xe
002E0EDE  add      rsp, 0x28
002E0EE2  ret      
002E0EE3  mov      eax, 0xf
002E0EE8  add      rsp, 0x28
002E0EEC  ret      
002E0EED  mov      eax, 0x10
002E0EF2  add      rsp, 0x28
002E0EF6  ret      
002E0EF7  mov      eax, 0x11
002E0EFC  add      rsp, 0x28
002E0F00  ret      
002E0F01  mov      eax, 0x12
002E0F06  add      rsp, 0x28
002E0F0A  ret      
002E0F0B  mov      eax, 0x13
002E0F10  add      rsp, 0x28
002E0F14  ret      
002E0F15  xor      eax, eax
002E0F17  add      rsp, 0x28
002E0F1B  ret      
```

## 0035BAA0 (47 B, extent 0035BAA0-0035BACF)

Page context: "ly | strong - triggered by raw pad mask '0x1000' (Triangle) with parameter 0 | | 3 | Field party-leader selection | proven - D-pad Up/Down '0x10 \| 0x40', needs >= 2 eligible candidates, commits via '0035BAA0' | | 4 | Battle Menu open by the same route as request 1 ('0035D660') | proven 2026-09-18 (FABLE); UQ-162 | | 5 | Field free-target actor cycle | proven - D-pad Left/Right '0x20 \| 0x80', spatial actor ordering, commits a real targ"

```
0035BAA0  push     rbx
0035BAA2  sub      rsp, 0x20
0035BAA6  cmp      ecx, dword ptr [rip + 0x1f6c5c4]  ; -> 022C8070
0035BAAC  mov      ebx, ecx
0035BAAE  je       0x35bac9  ; -> 0035BAC9
0035BAB0  call     0x3c8950  ; -> 003C8950 fn
0035BAB5  movzx    ecx, bl
0035BAB8  call     0x327850  ; -> 00327850 fn
0035BABD  xor      ecx, ecx
0035BABF  add      rsp, 0x20
0035BAC3  pop      rbx
0035BAC4  jmp      0x35bc50  ; -> 0035BC50 fn
0035BAC9  add      rsp, 0x20
0035BACD  pop      rbx
0035BACE  ret      
```

## 00428F30 (77 B, extent 00428F30-00428F7D)

Page context: " request word ('00252B40' at '0035D825') — so '02092730 = 0x18' while its widget lives; its callees ('002E1B10' the mailbox, '002E1C20' / '002E1CA0', '0035BC50', '0028FD70', '00290450' / '00290500', '00428F30') ~~are unread, and so is what it shows~~ have their roles in this procedure read in §7b R2 (the bodies of '0035BC50', '0028FD70', '00290450', '00290500' and '00428F30' are not read there) *(2026-10-01, SWE2-CONTRACT for OPUS, DD b"

```
00428F30  mov      qword ptr [rsp + 8], rbx
00428F35  push     rdi
00428F36  sub      rsp, 0x20
00428F3A  mov      rdi, qword ptr [rip + 0x1e9dfe7]  ; -> 022C6F28
00428F41  mov      ebx, dword ptr [rdi + 0x48800]
00428F47  cmp      ebx, -1
00428F4A  je       0x428f72  ; -> 00428F72
00428F4C  nop      dword ptr [rax]
00428F50  movsxd   rax, ebx
00428F53  imul     rcx, rax, 0x740
00428F5A  add      rcx, rdi
00428F5D  movsx    ebx, word ptr [rcx + 4]
00428F61  add      rcx, 0x5f0
00428F68  call     0x46d0a0  ; -> 0046D0A0 fn
00428F6D  cmp      ebx, -1
00428F70  jne      0x428f50  ; -> 00428F50
00428F72  mov      rbx, qword ptr [rsp + 0x30]
00428F77  add      rsp, 0x20
00428F7B  pop      rdi
00428F7C  ret      
```

## 0046D0A0 (30 B, extent 0046D0A0-0046D0BE)

Page context: "to '003F80E0' on '[0209BE80] + 0xA0D0' when that singleton exists, and '00428F30' walks the '0x740'-byte records of '022C6F28' from the head index '+0x48800' through each record's word '+4', calling '0046D0A0' on its '+0x5F0'. A stated limit: no claim here rests on what those two do inside. [Record](../../_index/candidates/swe2contract-ddres-b20-1001/README.md) F1-F3.)*: the procedure also serves request 3, shows the dialog text '0x86F'"

```
0046D0A0  cmp      byte ptr [rcx], 1
0046D0A3  jne      0x46d0bd  ; -> 0046D0BD
0046D0A5  cmp      byte ptr [rcx + 7], 0
0046D0A9  jne      0x46d0bd  ; -> 0046D0BD
0046D0AB  cmp      word ptr [rcx + 0x1c], 6
0046D0B0  jne      0x46d0bd  ; -> 0046D0BD
0046D0B2  mov      ecx, dword ptr [rcx + 0x18]
0046D0B5  test     ecx, ecx
0046D0B7  jg       0x2df690  ; -> 002DF690 fn
0046D0BD  ret      
```
