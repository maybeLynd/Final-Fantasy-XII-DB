# F-interior pack: `05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md`

Generated 2026-10-02 20:18 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/when-a-group-is-wiped-and-when-it-comes-back.json`.

Functions: 5. Each is cited on the page only at its entry and is still in the F frontier.

## 00234990 (102 B, extent 00234990-002349F6)

Page context: "run over a different, larger object — excluded by width and context. Readers of '+0xE98': the six ledger functions, '00233EA0', and the four 'SpawnGroup_*ByGroupMask' teardown helpers at '00234880', '00234990', '00234A10', '00234A80', plus '00237690'.)  Both mode bits are consumed: bit 0 selects the completion arm (§5); bit 1 is tested by 'BattleUnit_TeardownAndDespawn' at '00300F89' and, when set, **skips two actor-work calls** ('0025A"

```
00234990  mov      qword ptr [rsp + 8], rbx
00234995  push     rdi
00234996  sub      rsp, 0x20
0023499A  xor      ebx, ebx
0023499C  mov      edi, ecx
0023499E  cmp      dword ptr [rip + 0x1e59cfc], ebx  ; -> 0208E6A0
002349A4  jle      0x2349eb  ; -> 002349EB
002349A6  mov      ecx, ebx
002349A8  call     0x321170  ; -> 00321170 fn
002349AD  mov      rcx, rax
002349B0  test     rax, rax
002349B3  je       0x2349e1  ; -> 002349E1
002349B5  mov      rax, qword ptr [rax + 0x698]
002349BC  test     rax, rax
002349BF  je       0x2349e1  ; -> 002349E1
002349C1  movzx    edx, byte ptr [rax + 5]
002349C5  cmp      edx, 1
002349C8  jne      0x2349e1  ; -> 002349E1
002349CA  test     edx, edx
002349CC  je       0x2349e1  ; -> 002349E1
002349CE  movzx    eax, byte ptr [rcx + 0xe98]
002349D5  bt       edi, eax
002349D8  jae      0x2349e1  ; -> 002349E1
002349DA  xor      edx, edx
002349DC  call     0x300e40  ; -> 00300E40 fn
002349E1  inc      ebx
002349E3  cmp      ebx, dword ptr [rip + 0x1e59cb7]  ; -> 0208E6A0
002349E9  jl       0x2349a6  ; -> 002349A6
002349EB  mov      rbx, qword ptr [rsp + 0x30]
002349F0  add      rsp, 0x20
002349F4  pop      rdi
002349F5  ret      
```

## 002EDCC0 (93 B, extent 002EDCC0-002EDD1D)

Page context: ".  '002EB0D0' (604 B) is the animation-layer event consume the '003299B0 -> 002EB030' write arms: on 'dword[rdx] != -1' it '00269D60'-prepares the record, dispatches 'byte[+0x11]' bit '0x10' through '002EDCC0', then works the '022C6F28' '0x740'-row of 'word[rbx]' (every hop gated on 'dword[+0x284] != 0'): '00427320' on the direct path, '00427880'/'004278B0'/'004272C0' keyed on 'word[+0x2a]''s sign, '00427860' or '004270A0'/'004272E0' ke"

```
002EDCC0  cmp      cx, -1
002EDCC4  je       0x2edd1c  ; -> 002EDD1C
002EDCC6  movsx    rax, cx
002EDCCA  imul     r8, rax, 0x740
002EDCD1  add      r8, qword ptr [rip + 0x1fd9250]  ; -> 022C6F28
002EDCD8  je       0x2edd1c  ; -> 002EDD1C
002EDCDA  mov      r9d, dword ptr [r8 + 0x284]
002EDCE1  test     r9d, r9d
002EDCE4  je       0x2edd1c  ; -> 002EDD1C
002EDCE6  mov      eax, edx
002EDCE8  neg      eax
002EDCEA  sbb      ecx, ecx
002EDCEC  btr      r9d, 0x1f
002EDCF1  and      ecx, 0x80000000
002EDCF7  or       ecx, r9d
002EDCFA  mov      dword ptr [r8 + 0x284], ecx
002EDD01  test     edx, edx
002EDD03  jne      0x2edd11  ; -> 002EDD11
002EDD05  bts      ecx, 0x1c
002EDD09  mov      dword ptr [r8 + 0x284], ecx
002EDD10  ret      
002EDD11  btr      ecx, 0x1c
002EDD15  mov      dword ptr [r8 + 0x284], ecx
002EDD1C  ret      
```

## 0035C880 (17 B, extent 0035C880-0035C891)

Page context: "own helpers '0035D060'/'002470C0'/'0035C080'/'0028FFE0'/'00252D90'/'002E1CA0'; the UI layer calls several of them from its own screen/menu paths ('00279E20'/'0035CF50' calling '00252D90', '0035C7A0'/'0035C880' under '00234590'/'00252B60'). The crossing is the UI layer consulting shared helpers this page names, not UI ownership of the respawn path. Edge list from 'edges.tsv'.  ## The '00427320' exclusive subtree — all 7 members bound (SW"

```
0035C880  not      ecx
0035C882  and      ecx, dword ptr [rip + 0x1f6bb64]  ; -> 022C83EC
0035C888  or       ecx, edx
0035C88A  mov      dword ptr [rip + 0x1f6bb5c], ecx  ; -> 022C83EC
0035C890  ret      
```

## 0035DC90 (44 B, extent 0035DC90-0035DCBC)

Page context: "spawn body: it references no ledger, keep bank or spawn global, and its callers are '003C87B0' and '003C8B70' *(corrected 2026-10-02, OPUS: body read)* - '01F44830'/'02B47730', '0035BAD0'/'0035D3E0'/'0035DC90'/'0035DCC0'/'0035DEB0'/'00808C40'. Interior anchor '003C9276' (a '0035BAD0' call).  ## SWE2-EC7-43 update (2026-09-19) - '003E6770'  *(Corrected 2026-09-19, FABLE: '003E6770' is not a group-respawn body and has no part in respawnin"

```
0035DC90  xor      r9d, r9d
0035DC93  movsxd   r10, edx
0035DC96  mov      eax, r9d
0035DC99  test     edx, edx
0035DC9B  jle      0x35dcb4  ; -> 0035DCB4
0035DC9D  nop      dword ptr [rax]
0035DCA0  cmp      r8d, dword ptr [rcx]
0035DCA3  je       0x35dcb8  ; -> 0035DCB8
0035DCA5  inc      r9d
0035DCA8  inc      rax
0035DCAB  add      rcx, 0xc
0035DCAF  cmp      rax, r10
0035DCB2  jl       0x35dca0  ; -> 0035DCA0
0035DCB4  or       eax, 0xffffffff
0035DCB7  ret      
0035DCB8  mov      eax, r9d
0035DCBB  ret      
```

## 0035DEB0 (108 B, extent 0035DEB0-0035DF1C)

Page context: "ces no ledger, keep bank or spawn global, and its callers are '003C87B0' and '003C8B70' *(corrected 2026-10-02, OPUS: body read)* - '01F44830'/'02B47730', '0035BAD0'/'0035D3E0'/'0035DC90'/'0035DCC0'/'0035DEB0'/'00808C40'. Interior anchor '003C9276' (a '0035BAD0' call).  ## SWE2-EC7-43 update (2026-09-19) - '003E6770'  *(Corrected 2026-09-19, FABLE: '003E6770' is not a group-respawn body and has no part in respawning. It builds, or switc"

```
0035DEB0  mov      qword ptr [rsp + 8], rbx
0035DEB5  lea      eax, [rdx - 1]
0035DEB8  movsxd   rbx, edx
0035DEBB  mov      r8, rcx
0035DEBE  test     eax, eax
0035DEC0  jle      0x35df16  ; -> 0035DF16
0035DEC2  xor      r10d, r10d
0035DEC5  mov      r11d, eax
0035DEC8  cmp      r10, rbx
0035DECB  jge      0x35df09  ; -> 0035DF09
0035DECD  mov      r9, rbx
0035DED0  mov      rax, r8
0035DED3  sub      r9, r10
0035DED6  mov      ecx, dword ptr [rax + 4]
0035DED9  cmp      dword ptr [r8 + 4], ecx
0035DEDD  jle      0x35deff  ; -> 0035DEFF
0035DEDF  movsd    xmm0, qword ptr [rax]
0035DEE3  movsd    xmm1, qword ptr [r8]
0035DEE8  mov      edx, dword ptr [r8 + 8]
0035DEEC  movsd    qword ptr [r8], xmm0
0035DEF1  mov      ecx, dword ptr [rax + 8]
0035DEF4  mov      dword ptr [r8 + 8], ecx
0035DEF8  movsd    qword ptr [rax], xmm1
0035DEFC  mov      dword ptr [rax + 8], edx
0035DEFF  add      rax, 0xc
0035DF03  sub      r9, 1
0035DF07  jne      0x35ded6  ; -> 0035DED6
0035DF09  inc      r10
0035DF0C  add      r8, 0xc
0035DF10  sub      r11, 1
0035DF14  jne      0x35dec8  ; -> 0035DEC8
0035DF16  mov      rbx, qword ptr [rsp + 8]
0035DF1B  ret      
```
