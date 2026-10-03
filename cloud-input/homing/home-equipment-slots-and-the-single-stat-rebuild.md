# Homing pack: `12-Items-Equipment-Shops-License/equipment-slots-and-the-single-stat-rebuild.md`

Generated 2026-10-02 22:54 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-equipment-slots-and-the-single-stat-rebuild.json`.

Bodies: 3. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00272400 (99 B, extent 00272400-00272463)

Entered from (direct sites whose caller this page cites): `0027D740` + 0x149 (call; `0027D740` is cited on this page); `0027D740` + 0x24D (call; `0027D740` is cited on this page); `0027D740` + 0x30A (call; `0027D740` is cited on this page); `0027D740` + 0x31E (call; `0027D740` is cited on this page); `0027D740` + 0x35A (call; `0027D740` is cited on this page); `0027D740` + 0x410 (call; `0027D740` is cited on this page)
Other direct sites: none

Host context: " it through '0031FF70' → '00329220' (mode 'full'), and returns '+0xAC >> 16': **the actor's stashed slot-0 item**. Its five callers are all battle-menu bodies ('0027AD70', '0027C3D0', '0027CE70' ×2, '0027D740'); in 'BattleMenu_ClassifySelectedEntryAndHandleImmediateCommands' the selected entry's id ('0027C61C movzx edi, word ptr [rdx + 0x50]', the 8-byte entry at container '+0x50 + index*8') is compared against that return and chooses c" / " it through '0031FF70' → '00329220' (mode 'full'), and returns '+0xAC >> 16': **the actor's stashed slot-0 item**. Its five callers are all battle-menu bodies ('0027AD70', '0027C3D0', '0027CE70' ×2, '0027D740'); in 'BattleMenu_ClassifySelectedEntryAndHandleImmediateCommands' the selected entry's id ('0027C61C movzx edi, word ptr [rdx + 0x50]', the 8-byte entry at container '+0x50 + index*8') is compared against that return and chooses c"

```
00272400  mov      eax, dword ptr [rdx]
00272402  lea      r9, [rdx + 0x40]
00272406  mov      dword ptr [rcx], eax
00272408  mov      r8, rdx
0027240B  movups   xmm0, xmmword ptr [rdx + 8]
0027240F  movups   xmmword ptr [rcx + 8], xmm0
00272413  movups   xmm1, xmmword ptr [rdx + 0x18]
00272417  movups   xmmword ptr [rcx + 0x18], xmm1
0027241B  movups   xmm0, xmmword ptr [rdx + 0x28]
0027241F  movups   xmmword ptr [rcx + 0x28], xmm0
00272423  movsd    xmm1, qword ptr [rdx + 0x38]
00272428  movsd    qword ptr [rcx + 0x38], xmm1
0027242D  mov      eax, dword ptr [r9]
00272430  mov      dword ptr [rcx + 0x40], eax
00272433  mov      eax, dword ptr [rdx + 0x44]
00272436  xor      edx, edx
00272438  mov      dword ptr [rcx + 0x44], eax
0027243B  cmp      dword ptr [r9], edx
0027243E  jle      0x272462  ; -> 00272462
00272440  lea      rax, [rcx + 0x50]
00272444  sub      r8, rcx
00272447  nop      word ptr [rax + rax]
00272450  mov      rcx, qword ptr [r8 + rax]
00272454  inc      edx
00272456  mov      qword ptr [rax], rcx
00272459  lea      rax, [rax + 8]
0027245D  cmp      edx, dword ptr [r9]
00272460  jl       0x272450  ; -> 00272450
00272462  ret      
```

## 0027C220 (95 B, extent 0027C220-0027C27F)

Entered from (direct sites whose caller this page cites): `0027D740` + 0x10E (call; `0027D740` is cited on this page); `0027D740` + 0x1FE (call; `0027D740` is cited on this page)
Other direct sites: none

Host context: " it through '0031FF70' → '00329220' (mode 'full'), and returns '+0xAC >> 16': **the actor's stashed slot-0 item**. Its five callers are all battle-menu bodies ('0027AD70', '0027C3D0', '0027CE70' ×2, '0027D740'); in 'BattleMenu_ClassifySelectedEntryAndHandleImmediateCommands' the selected entry's id ('0027C61C movzx edi, word ptr [rdx + 0x50]', the 8-byte entry at container '+0x50 + index*8') is compared against that return and chooses c" / " it through '0031FF70' → '00329220' (mode 'full'), and returns '+0xAC >> 16': **the actor's stashed slot-0 item**. Its five callers are all battle-menu bodies ('0027AD70', '0027C3D0', '0027CE70' ×2, '0027D740'); in 'BattleMenu_ClassifySelectedEntryAndHandleImmediateCommands' the selected entry's id ('0027C61C movzx edi, word ptr [rdx + 0x50]', the 8-byte entry at container '+0x50 + index*8') is compared against that return and chooses c"

```
0027C220  sub      rsp, 0x28
0027C224  mov      eax, dword ptr [rcx]
0027C226  cmp      eax, 6
0027C229  jl       0x27c278  ; -> 0027C278
0027C22B  cmp      eax, 0xa
0027C22E  jle      0x27c249  ; -> 0027C249
0027C230  cmp      eax, 0xb
0027C233  jne      0x27c278  ; -> 0027C278
0027C235  movsxd   rax, edx
0027C238  test     byte ptr [rcx + rax*8 + 0x54], 1
0027C23D  lea      rdx, [rcx + rax*8]
0027C241  je       0x27c278  ; -> 0027C278
0027C243  movzx    eax, byte ptr [rdx + 0x56]
0027C247  jmp      0x27c25b  ; -> 0027C25B
0027C249  movsxd   rax, edx
0027C24C  test     byte ptr [rcx + rax*8 + 0x53], 2
0027C251  lea      rdx, [rcx + rax*8]
0027C255  je       0x27c278  ; -> 0027C278
0027C257  movzx    eax, byte ptr [rdx + 0x54]
0027C25B  movsx    ecx, al
0027C25E  test     al, al
0027C260  js       0x27c278  ; -> 0027C278
0027C262  je       0x27c278  ; -> 0027C278
0027C264  call     0x27c150  ; -> 0027C150 fn
0027C269  test     eax, eax
0027C26B  js       0x27c278  ; -> 0027C278
0027C26D  mov      ecx, eax
0027C26F  add      rsp, 0x28
0027C273  jmp      0x2f9860  ; -> 002F9860 fn
0027C278  xor      eax, eax
0027C27A  add      rsp, 0x28
0027C27E  ret      
```

## 0035A250 (23 B, extent 0035A250-0035A267)

Entered from (direct sites whose caller this page cites): `0034A300` + 0x4 (call; `0034A300` is cited on this page)
Other direct sites: none

Host context: "efresh after an inventory-affecting equip or a License purchase (§7) | | '00324380' | *(unnamed)* | the party-slot snapshot that restarts the party read-in, called by takeaway and giveback (§11) | | '0034A300' | *(unnamed)* | the poll the takeaway / giveback verbs share: waits for that read-in (§11) |  ## 6. What the rebuild does, as far as it is read  '002FEF30' takes the stats record, captures the slot array pointer ('lea rbx, [rdi + "

```
0035A250  sub      rsp, 0x28
0035A254  call     0x30bad0  ; -> 0030BAD0 fn
0035A259  xor      ecx, ecx
0035A25B  test     eax, eax
0035A25D  sete     cl
0035A260  mov      eax, ecx
0035A262  add      rsp, 0x28
0035A266  ret      
```
