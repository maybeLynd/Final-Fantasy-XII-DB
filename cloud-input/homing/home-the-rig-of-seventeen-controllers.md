# Homing pack: `17-Presentation-Rendering/Character-Render-Records/the-rig-of-seventeen-controllers.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-rig-of-seventeen-controllers.json`.

Bodies: 10. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002EB810 (92 B, extent 002EB810-002EB86C)

Entered from (direct sites whose caller this page cites): `002E3110` + 0x1F9 (call; `002E3110` is cited on this page)
Other direct sites: `002E3A60` + 0x45 (call)

Host context: "escribed here by role; the statuses themselves, and everything they do to the rules, belong to the status pages. This page owns only the thirty-two-way fan-out onto the body.  **Movement - CLIENT.** '002E3110', a Movement-filed body that [the party read-in state machine](../../01-Script-VM-Native-Bridge/Party-Presentation-Verbs/the-party-read-in-state-machine.md) describes as the step that applies a read-in model element, is a second, n"

```
002EB810  mov      rax, qword ptr [rip + 0x1e74541]  ; -> 0215FD58
002EB817  test     rax, rax
002EB81A  je       0x2eb82e  ; -> 002EB82E
002EB81C  nop      dword ptr [rax]
002EB820  cmp      dword ptr [rax + 0x14], ecx
002EB823  je       0x2eb84f  ; -> 002EB84F
002EB825  mov      rax, qword ptr [rax + 8]
002EB829  test     rax, rax
002EB82C  jne      0x2eb820  ; -> 002EB820
002EB82E  mov      rax, qword ptr [rip + 0x1e74543]  ; -> 0215FD78
002EB835  test     rax, rax
002EB838  je       0x2eb86b  ; -> 002EB86B
002EB83A  nop      word ptr [rax + rax]
002EB840  cmp      dword ptr [rax + 0x14], ecx
002EB843  je       0x2eb84f  ; -> 002EB84F
002EB845  mov      rax, qword ptr [rax + 8]
002EB849  test     rax, rax
002EB84C  jne      0x2eb840  ; -> 002EB840
002EB84E  ret      
002EB84F  test     rax, rax
002EB852  je       0x2eb86b  ; -> 002EB86B
002EB854  dec      word ptr [rax + 0x1c]
002EB858  cmp      word ptr [rax + 0x1c], 0
002EB85D  jg       0x2eb86b  ; -> 002EB86B
002EB85F  test     byte ptr [rax + 0x19], 3
002EB863  je       0x2eb86b  ; -> 002EB86B
002EB865  xor      ecx, ecx
002EB867  mov      word ptr [rax + 0x1c], cx
002EB86B  ret      
```

## 003E1C10 (55 B, extent 003E1C10-003E1C47)

Entered from (direct sites whose caller this page cites): `00372710` + 0x40 (call; `00372710` is cited on this page)
Other direct sites: none

Host context: "x+0xD98]' gives the target row 'rsi'; a second '0020E600' on '[rcx+0x10]' feeds '0046E420' keyed by '+0x18'; when '+0x284 & 0x20000' was armed, '[rsi+0x94]''s resolve contributes '+0x64' into 'ebx', '00372710(rsi, ebx)' commits it, and both '+0x284' bit '0x20000' and the '+0x40A' byte clear  Interior anchor '003E6FC2' (function '003E6F90').  '003E7040' (170 B) is the conditional child-resolve '0042BED0' runs: a non'-1' '[rcx+0x18]' id l"

```
003E1C10  mov      qword ptr [rsp + 8], rbx
003E1C15  push     rdi
003E1C16  sub      rsp, 0x20
003E1C1A  mov      rbx, rcx
003E1C1D  mov      edi, edx
003E1C1F  mov      ecx, dword ptr [rcx]
003E1C21  call     0x20e600  ; -> 0020E600 fn
003E1C26  test     rax, rax
003E1C29  je       0x3e1c3c  ; -> 003E1C3C
003E1C2B  mov      ecx, dword ptr [rbx]
003E1C2D  call     0x20e600  ; -> 0020E600 fn
003E1C32  cmp      byte ptr [rax + 6], 0
003E1C36  je       0x3e1c3c  ; -> 003E1C3C
003E1C38  mov      word ptr [rbx + 0x60], di
003E1C3C  mov      rbx, qword ptr [rsp + 0x30]
003E1C41  add      rsp, 0x20
003E1C45  pop      rdi
003E1C46  ret      
```

## 0040DB00 (111 B, extent 0040DB00-0040DB6F)

Entered from (direct sites whose caller this page cites): `003E0E70` + 0x5B (call; `003E0E70` is cited on this page); `003E1210` + 0x5B (call; `003E1210` is cited on this page)
Other direct sites: none

Host context: "a long field-copy/resolve pass over the controller record with almost no helper traffic.  Interior anchor '005121BB' (function '005121A0').  '003E0B50' (797 B) is the controller apply '0042BED0' and '003E0E70' call: '0020E600' x17 with '0040ED90' x6 - the rig's resolve-heavy record walker, one of the pair.  Interior anchor '003E0B70' (function '003E0B50').  '003E0F00' (770 B) is the sibling '0042BED0'/'003E1210' call beside '003E0B50': " / "70' call: '0020E600' x17 with '0040ED90' x6 - the rig's resolve-heavy record walker, one of the pair.  Interior anchor '003E0B70' (function '003E0B50').  '003E0F00' (770 B) is the sibling '0042BED0'/'003E1210' call beside '003E0B50': identical '0020E600' x17 + '0040ED90' x6 shape - the second resolve-heavy walker of the pair.  Interior anchor '003E0F20' (function '003E0F00').  '00471B60' (733 B) is the rig body '003E00C0' calls: '0020E6"

```
0040DB00  mov      qword ptr [rsp + 8], rbx
0040DB05  mov      qword ptr [rsp + 0x10], rsi
0040DB0A  push     rdi
0040DB0B  sub      rsp, 0x20
0040DB0F  mov      rbx, rcx
0040DB12  mov      esi, edx
0040DB14  mov      ecx, dword ptr [rcx]
0040DB16  xor      edi, edi
0040DB18  call     0x20e600  ; -> 0020E600 fn
0040DB1D  movzx    r9d, byte ptr [rbx + 4]
0040DB22  mov      r8d, edi
0040DB25  test     r9d, r9d
0040DB28  je       0x40db48  ; -> 0040DB48
0040DB2A  add      rax, 0x2a
0040DB2E  nop      
0040DB30  movzx    ecx, word ptr [rax]
0040DB33  shr      ecx, 4
0040DB36  cmp      esi, ecx
0040DB38  je       0x40db5d  ; -> 0040DB5D
0040DB3A  inc      r8d
0040DB3D  inc      edi
0040DB3F  add      rax, 0x30
0040DB43  cmp      r8d, r9d
0040DB46  jb       0x40db30  ; -> 0040DB30
0040DB48  mov      eax, 0xfff
0040DB4D  mov      rbx, qword ptr [rsp + 0x30]
0040DB52  mov      rsi, qword ptr [rsp + 0x38]
0040DB57  add      rsp, 0x20
0040DB5B  pop      rdi
0040DB5C  ret      
0040DB5D  mov      rbx, qword ptr [rsp + 0x30]
0040DB62  mov      eax, edi
0040DB64  mov      rsi, qword ptr [rsp + 0x38]
0040DB69  add      rsp, 0x20
0040DB6D  pop      rdi
0040DB6E  ret      
```

## 00471310 (18 B, extent 00471310-00471322)

Entered from (direct sites whose caller this page cites): `003E1610` + 0x1E7 (jmp; `003E1610` is cited on this page)
Other direct sites: none

Host context: "ner_layer: PrimaryOwner:Presentation evidence_tier: 1 verified_against:   exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8   method: the two controller switches 003E1350 / 003E1610 read (the first whole, its jump table decoded from the image; the     second by its seventeen arms); the per-frame update 003E00C0 read for its order of calls and the flag each apply call     is gated on; the timed-state countdown "

```
00471310  mov      eax, 1
00471315  mov      word ptr [rcx + 0xc], 0
0047131B  mov      word ptr [rcx + 2], ax
0047131F  mov      byte ptr [rcx], al
00471321  ret      
```

## 00471380 (28 B, extent 00471380-0047139C)

Entered from (direct sites whose caller this page cites): `003E1350` + 0x129 (jmp; `003E1350` is cited on this page)
Other direct sites: none

Host context: "CUMENTED owner_layer: PrimaryOwner:Presentation evidence_tier: 1 verified_against:   exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8   method: the two controller switches 003E1350 / 003E1610 read (the first whole, its jump table decoded from the image; the     second by its seventeen arms); the per-frame update 003E00C0 read for its order of calls and the flag each apply call     is gated on; the timed-state"

```
00471380  cmp      byte ptr [rcx], 0
00471383  je       0x47139b  ; -> 0047139B
00471385  mov      eax, dword ptr [rcx + 0x10]
00471388  mov      dword ptr [rcx + 0x18], eax
0047138B  mov      eax, dword ptr [rcx + 0x14]
0047138E  mov      dword ptr [rcx + 0x1c], eax
00471391  mov      byte ptr [rcx], 0
00471394  mov      dword ptr [rcx + 0xc], 0x3f800000
0047139B  ret      
```

## 004715D0 (31 B, extent 004715D0-004715EF)

Entered from (direct sites whose caller this page cites): `003E1610` + 0x129 (jmp; `003E1610` is cited on this page)
Other direct sites: none

Host context: "ner_layer: PrimaryOwner:Presentation evidence_tier: 1 verified_against:   exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8   method: the two controller switches 003E1350 / 003E1610 read (the first whole, its jump table decoded from the image; the     second by its seventeen arms); the per-frame update 003E00C0 read for its order of calls and the flag each apply call     is gated on; the timed-state countdown "

```
004715D0  cmp      byte ptr [rcx], 0
004715D3  jne      0x4715ee  ; -> 004715EE
004715D5  mov      eax, dword ptr [rcx + 0x10]
004715D8  mov      dword ptr [rcx + 0x18], eax
004715DB  mov      eax, dword ptr [rcx + 0x14]
004715DE  mov      dword ptr [rcx + 0x1c], eax
004715E1  mov      dword ptr [rcx], 0x101
004715E7  mov      dword ptr [rcx + 0xc], 0x3f800000
004715EE  ret      
```

## 004719A0 (9 B, extent 004719A0-004719A9)

Entered from (direct sites whose caller this page cites): `003E1350` + 0x209 (jmp; `003E1350` is cited on this page)
Other direct sites: none

Host context: "CUMENTED owner_layer: PrimaryOwner:Presentation evidence_tier: 1 verified_against:   exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8   method: the two controller switches 003E1350 / 003E1610 read (the first whole, its jump table decoded from the image; the     second by its seventeen arms); the per-frame update 003E00C0 read for its order of calls and the flag each apply call     is gated on; the timed-state"

```
004719A0  and      byte ptr [rcx + 9], 0xf
004719A4  mov      byte ptr [rcx + 8], 0
004719A8  ret      
```

## 00471B20 (63 B, extent 00471B20-00471B5F)

Entered from (direct sites whose caller this page cites): `003E12A0` + 0x3E (jmp; `003E12A0` is cited on this page)
Other direct sites: none

Host context: "byte[+0x40B] bit7', '+0x290' loses '0x8000' - completing the three-bit mirror of the record's flag word. Interior anchor '00429B92' (the first '0042DCD0' call).  ## SWE2-EC7-87 update (2026-09-20) - '003E12A0' two-case mode dispatch measured  '003E12A0' (109 B) is the 'edx'-keyed dispatch the rig callers run: '9' resolves '[rbx+0x24]' through '0020E600' and forwards to '00517610(record, r8d)'; '0xD' resolves '[rbx+0x34]' the same way an"

```
00471B20  and      byte ptr [rcx + 9], 0x3f
00471B24  test     edx, edx
00471B26  je       0x471b56  ; -> 00471B56
00471B28  movzx    eax, byte ptr [rcx + 9]
00471B2C  test     al, 0x30
00471B2E  je       0x471b5e  ; -> 00471B5E
00471B30  and      al, 0xdf
00471B32  or       al, 0x10
00471B34  mov      byte ptr [rcx + 9], al
00471B37  cmp      al, 0x40
00471B39  jae      0x471b5e  ; -> 00471B5E
00471B3B  cmp      byte ptr [rcx + 8], 0
00471B3F  jne      0x471b5e  ; -> 00471B5E
00471B41  mov      eax, 1
00471B46  mov      qword ptr [rcx + 0x10], 8
00471B4E  mov      word ptr [rcx + 0xa], ax
00471B52  mov      byte ptr [rcx + 8], al
00471B55  ret      
00471B56  or       byte ptr [rcx + 9], 0x40
00471B5A  mov      byte ptr [rcx + 8], 0
00471B5E  ret      
```

## 005175C0 (38 B, extent 005175C0-005175E6)

Entered from (direct sites whose caller this page cites): `003E1350` + 0x175 (jmp; `003E1350` is cited on this page)
Other direct sites: none

Host context: "CUMENTED owner_layer: PrimaryOwner:Presentation evidence_tier: 1 verified_against:   exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8   method: the two controller switches 003E1350 / 003E1610 read (the first whole, its jump table decoded from the image; the     second by its seventeen arms); the per-frame update 003E00C0 read for its order of calls and the flag each apply call     is gated on; the timed-state"

```
005175C0  and      byte ptr [rcx + 1], 0xf
005175C4  cmp      byte ptr [rcx], 0
005175C7  je       0x5175e5  ; -> 005175E5
005175C9  mov      eax, dword ptr [rcx + 0x10]
005175CC  mov      dword ptr [rcx + 0x88], eax
005175D2  mov      eax, dword ptr [rcx + 0x4c]
005175D5  mov      dword ptr [rcx + 0x8c], eax
005175DB  mov      byte ptr [rcx], 0
005175DE  mov      dword ptr [rcx + 0xc], 0x3f800000
005175E5  ret      
```

## 0051B950 (20 B, extent 0051B950-0051B964)

Entered from (direct sites whose caller this page cites): `003E1610` + 0x24D (jmp; `003E1610` is cited on this page)
Other direct sites: none

Host context: "ner_layer: PrimaryOwner:Presentation evidence_tier: 1 verified_against:   exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8   method: the two controller switches 003E1350 / 003E1610 read (the first whole, its jump table decoded from the image; the     second by its seventeen arms); the per-frame update 003E00C0 read for its order of calls and the flag each apply call     is gated on; the timed-state countdown "

```
0051B950  movzx    eax, byte ptr [rcx + 0x34]
0051B954  test     al, 1
0051B956  jne      0x51b963  ; -> 0051B963
0051B958  or       al, 1
0051B95A  mov      byte ptr [rcx + 0x34], al
0051B95D  xor      eax, eax
0051B95F  mov      word ptr [rcx + 0x30], ax
0051B963  ret      
```
