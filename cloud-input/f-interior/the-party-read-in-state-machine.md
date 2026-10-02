# F-interior pack: `01-Script-VM-Native-Bridge/Party-Presentation-Verbs/the-party-read-in-state-machine.md`

Generated 2026-10-02 18:33 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/the-party-read-in-state-machine.json`.

Functions: 7. Each is cited on the page only at its entry and is still in the F frontier.

## 00264EC0 (5 B, extent 00264EC0-00264EC5)

Page context: "slot by 'id & 0xF'), then '0036F0F0' finds-or-evicts an entry for the new key ('+0x14'), bumps its refcount, and returns the entry's packed byte '(+0x02 << 4) \| +0x01'; '002ED910' resolves the key, '00264EC0' reads record byte '+0x12', 'PartyRoster_IsFourSlotIndex' gates the pool choice | 5 ('0037B8A2'); 7 when the lookup is negative ('0037B864' → '0037B86A') | | 5 | waits until '0036ECA0' — the entry's state byte '+0x00' — returns 3 ("

```
00264EC0  movsx    eax, byte ptr [rcx + 0x12]
00264EC4  ret      
```

## 002E8450 (87 B, extent 002E8450-002E84A7)

Page context: "egistryEntry', '0031C540', '0026D610', 'ActorHandle_GetPrimaryFormulaResourceByte26', '002E28E0', '002681D0', '002E5C70' (with the three floats at actor '+0xB8'), '002EAC90', '002E49B0', '002E4A40', '002E8450' | 3 ('0037B75D'), falling into 3's arm | | 3 | — (the matched-keys path from 1 re-dispatches here) | 4 ('0037B816') | | 4 | swaps the actor's **voice-pack reference**: '0036EC10' decrements the refcount ('+0x16') on the entry the "

```
002E8450  mov      rax, qword ptr [rcx + 0xc0]
002E8457  test     rax, rax
002E845A  je       0x2e8462  ; -> 002E8462
002E845C  mov      byte ptr [rax + 0x150], dl
002E8462  mov      rcx, qword ptr [rcx + 0xc0]
002E8469  test     rcx, rcx
002E846C  je       0x2e84a6  ; -> 002E84A6
002E846E  cmp      dword ptr [rcx], -1
002E8471  je       0x2e84a6  ; -> 002E84A6
002E8473  movzx    eax, word ptr [rcx]
002E8476  cmp      ax, -1
002E847A  je       0x2e84a6  ; -> 002E84A6
002E847C  movsx    rax, ax
002E8480  imul     rdx, rax, 0x740
002E8487  add      rdx, qword ptr [rip + 0x1fdea9a]  ; -> 022C6F28
002E848E  je       0x2e84a6  ; -> 002E84A6
002E8490  cmp      dword ptr [rdx + 0x284], 0
002E8497  je       0x2e84a6  ; -> 002E84A6
002E8499  movzx    eax, byte ptr [rcx + 0x150]
002E84A0  mov      byte ptr [rdx + 0x40c], al
002E84A6  ret      
```

## 0031BE30 (133 B, extent 0031BE30-0031BEB5)

Page context: "BF60' and resolved to the row's **'+0x30' dword = the model         resource id**), part **8** → 'dword[defRow + 0x38 + sub*4]' (two authored dwords, '+0x38'/'+0x3C',         'sub' = record '+0xA'). '0031BE30' reads the same parts' second form via def bytes '+0x40'/'+0x41'.       - *So per element:* el '+0x30' = **weapon model** (equip slot 0), el '+0x60' = **off-hand/shield model**         (equip slot 1), el '+0x90' = the **body model*"

```
0031BE30  mov      qword ptr [rsp + 0x10], rbx
0031BE35  mov      qword ptr [rsp + 0x18], rsi
0031BE3A  push     rdi
0031BE3B  sub      rsp, 0x20
0031BE3F  movsxd   rsi, r8d
0031BE42  mov      edi, edx
0031BE44  mov      ebx, 0x10a
0031BE49  test     rcx, rcx
0031BE4C  je       0x31bea3  ; -> 0031BEA3
0031BE4E  call     0x263e30  ; -> 00263E30 fn
0031BE53  test     rax, rax
0031BE56  je       0x31bea3  ; -> 0031BEA3
0031BE58  mov      rdx, qword ptr [rax + 0x698]
0031BE5F  test     rdx, rdx
0031BE62  je       0x31bea3  ; -> 0031BEA3
0031BE64  test     edi, edi
0031BE66  je       0x31bea3  ; -> 0031BEA3
0031BE68  sub      edi, 1
0031BE6B  je       0x31bea3  ; -> 0031BEA3
0031BE6D  cmp      edi, 7
0031BE70  jne      0x31bea3  ; -> 0031BEA3
0031BE72  cmp      byte ptr [rdx + 5], 1
0031BE76  jne      0x31bea3  ; -> 0031BEA3
0031BE78  mov      rcx, qword ptr [rax + 0xe60]
0031BE7F  movzx    eax, byte ptr [rcx + 0x40]
0031BE83  mov      byte ptr [rsp + 0x30], al
0031BE87  movzx    eax, byte ptr [rcx + 0x41]
0031BE8B  mov      byte ptr [rsp + 0x31], al
0031BE8F  cmp      esi, 2
0031BE92  jge      0x31bea3  ; -> 0031BEA3
0031BE94  movzx    ecx, byte ptr [rsp + rsi + 0x30]
0031BE99  lea      rax, [rip + 0x9f4958]  ; -> 00D107F8
0031BEA0  mov      ebx, dword ptr [rax + rcx*4]
0031BEA3  mov      rsi, qword ptr [rsp + 0x40]
0031BEA8  mov      eax, ebx
0031BEAA  mov      rbx, qword ptr [rsp + 0x38]
0031BEAF  add      rsp, 0x20
0031BEB3  pop      rdi
0031BEB4  ret      
```

## 0034E3E0 (40 B, extent 0034E3E0-0034E408)

Page context: "s its model and motions swapped for the ones its current definition calls for, and reappears in place. The waits are the frames spent loading. A script that issues 'partyallread' blocks (its poll is '0034E3E0') until every slot has been through the machine.  ## 2. Mechanism  ### 2.1 The record  ''' party read-in record            12 bytes; three statics are known (§2.2)   +0x00  u32   actor            encoded image pointer (RuntimePoint"

```
0034E3E0  sub      rsp, 0x28
0034E3E4  call     0x37cb50  ; -> 0037CB50 fn
0034E3E9  test     eax, eax
0034E3EB  je       0x34e3f4  ; -> 0034E3F4
0034E3ED  xor      eax, eax
0034E3EF  add      rsp, 0x28
0034E3F3  ret      
0034E3F4  mov      ecx, 1
0034E3F9  call     0x314d40  ; -> 00314D40 fn
0034E3FE  mov      eax, 1
0034E403  add      rsp, 0x28
0034E407  ret      
```

## 00351F40 (65 B, extent 00351F40-00351F81)

Page context: "*verb task steps** — '003523B0' is 'setupbattle' '0x56''s       step and '005101B0' is 'VM_Spawn_ApplySelectedUnit' '0x3001''s step; each sits third in a vtable triple       ('01EEE1C0' = '{00351C00, 00351F40, 003523B0}', '01F281D0' = '{00510440, 00510160, 005101B0}') and receives       **the task's own record**, which embeds a '0037B4D0' machine block at '+0x00'–'+0x0B' plus a task phase       byte at '+0x0C' and its param at '+0x0D' ("

```
00351F40  mov      qword ptr [rsp + 8], rbx
00351F45  push     rdi
00351F46  sub      rsp, 0x20
00351F4A  mov      rcx, r9
00351F4D  mov      rbx, r8
00351F50  mov      rdi, rdx
00351F53  call     0x267e10  ; -> 00267E10 fn
00351F58  mov      ecx, eax
00351F5A  mov      byte ptr [rbx + 0xd], al
00351F5D  call     0x2647c0  ; -> 002647C0 fn
00351F62  test     eax, eax
00351F64  mov      edx, 0xb
00351F69  mov      rcx, rdi
00351F6C  setne    al
00351F6F  mov      byte ptr [rbx + 0xc], al
00351F72  mov      rbx, qword ptr [rsp + 0x30]
00351F77  add      rsp, 0x20
00351F7B  pop      rdi
00351F7C  jmp      0x26b4a0  ; -> 0026B4A0 fn
```

## 00359B10 (100 B, extent 00359B10-00359B74)

Page context: "riant1', 'Actor_SetDesiredMovementHeading', '002E4A40', '002E8060', '002EB030', **'Actor_SetPresentationVisibilityEnabled'** (shown again), 'BattleUnit_ActivateAppliedDefinitionRuntime', '00263560', '00359B10', '002DEB90' | 23 ('0037C0EB') | | 23 | done: returns 1 ('0037C0EE') | — |  **The entries it loads live in the 128 × 64-byte table at '0215FDA0'** ([how a script names a thing in the world](../how-a-script-names-a-thing-in-the-worl"

```
00359B10  mov      qword ptr [rsp + 8], rbx
00359B15  mov      qword ptr [rsp + 0x10], rsi
00359B1A  push     rdi
00359B1B  sub      rsp, 0x20
00359B1F  xor      ecx, ecx
00359B21  call     0x32a060  ; -> 0032A060 fn
00359B26  mov      edi, eax
00359B28  call     0x313590  ; -> 00313590 fn
00359B2D  or       ebx, 0xffffffff
00359B30  mov      esi, ebx
00359B32  test     eax, eax
00359B34  je       0x359b47  ; -> 00359B47
00359B36  mov      ecx, eax
00359B38  call     0x3588b0  ; -> 003588B0 fn
00359B3D  mov      rcx, rax
00359B40  call     0x2e9b60  ; -> 002E9B60 fn
00359B45  mov      ebx, eax
00359B47  test     edi, edi
00359B49  je       0x359b5c  ; -> 00359B5C
00359B4B  mov      ecx, edi
00359B4D  call     0x3588b0  ; -> 003588B0 fn
00359B52  mov      rcx, rax
00359B55  call     0x2e9b60  ; -> 002E9B60 fn
00359B5A  mov      esi, eax
00359B5C  mov      edx, esi
00359B5E  mov      ecx, ebx
00359B60  mov      rbx, qword ptr [rsp + 0x30]
00359B65  mov      rsi, qword ptr [rsp + 0x38]
00359B6A  add      rsp, 0x20
00359B6E  pop      rdi
00359B6F  jmp      0x3b5470  ; -> 003B5470 fn
```

## 0037C980 (113 B, extent 0037C980-0037C9F1)

Page context: "es 13-15 (0037BBEA)   +0x0B  u8    002DEBD0 result  stored at setup (0037C23F / 0037C7F1) '''  ### 2.2 Who runs it  | entry | record | how | |---|---|---| | 'partyallread' '0x3EB' begin '0034CCD0' → '0037C980' | '02EBF3F0' | allocates a 'ScheduledTaskRecord' ('002F16B0' → '022BDEC0 + slot × 0x48', declared 2026-09-18) whose '+0x10' tick callback is **'0037C730'**, start slot '02EBF3FE' = 0, step '02EBF3FD' = +1; then '00233CF0' | | 'par"

```
0037C980  sub      rsp, 0x28
0037C984  call     0x2f16b0  ; -> 002F16B0 fn
0037C989  mov      qword ptr [rip + 0x2b42a70], rax  ; -> 02EBF400
0037C990  mov      byte ptr [rip + 0x2b42a65], 1  ; -> 02EBF3FC
0037C997  test     rax, rax
0037C99A  je       0x37c9ec  ; -> 0037C9EC
0037C99C  lea      rcx, [rip - 0x273]  ; -> 0037C730
0037C9A3  mov      qword ptr [rax + 0x10], rcx
0037C9A7  xor      ecx, ecx
0037C9A9  mov      rax, qword ptr [rip + 0x2b42a50]  ; -> 02EBF400
0037C9B0  mov      qword ptr [rax + 8], rcx
0037C9B4  mov      rax, qword ptr [rip + 0x2b42a45]  ; -> 02EBF400
0037C9BB  mov      dword ptr [rax], ecx
0037C9BD  mov      rax, qword ptr [rip + 0x2b42a3c]  ; -> 02EBF400
0037C9C4  mov      dword ptr [rax + 4], 4
0037C9CB  mov      rax, qword ptr [rip + 0x2b42a2e]  ; -> 02EBF400
0037C9D2  mov      word ptr [rax + 0x1c], cx
0037C9D6  mov      byte ptr [rip + 0x2b42a22], cl  ; -> 02EBF3FE
0037C9DC  mov      byte ptr [rip + 0x2b42a1a], 1  ; -> 02EBF3FD
0037C9E3  add      rsp, 0x28
0037C9E7  jmp      0x233cf0  ; -> 00233CF0 fn
0037C9EC  add      rsp, 0x28
0037C9F0  ret      
```
