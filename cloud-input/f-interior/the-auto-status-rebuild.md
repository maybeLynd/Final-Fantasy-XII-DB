# F-interior pack: `08-Combat-Formula/the-auto-status-rebuild.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/the-auto-status-rebuild.json`.

Functions: 7. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 7903502f7	FABLE: pass-22 debt - crossing sections on 94 pages (FABLE's group; 12 overlay-carrier pages routed ; inbox mentions: FABLE.md). OPUS read these before packing.

## 0030BEB0 (63 B, extent 0030BEB0-0030BEEF)

Page context: "order table reads.  **Party — CLIENT and SERVICE (13 edges).** The FC-3 gate '002FA3B0' calls 'BattleUnit_GetPartyLeader' '003272A0'; '00328BD0', which clears a member's equipment, calls '0030FED0'; '0030BEB0' calls 'ActorWork_GetBattleUnit' '0031B760'; 'BattleUnit_SeedPartyCombatStanceRecheckTimer' '003081E0' calls 'RNG_SharedGameplayLCG_NextU32' '00328370'; and nine roster and focus bodies call '00322C50', among them 'PartyConfigurati"

```
0030BEB0  sub      rsp, 0x28
0030BEB4  call     0x31b760  ; -> 0031B760 fn
0030BEB9  mov      rcx, rax
0030BEBC  test     rax, rax
0030BEBF  je       0x30bee8  ; -> 0030BEE8
0030BEC1  mov      eax, dword ptr [rax]
0030BEC3  test     al, 8
0030BEC5  je       0x30bee8  ; -> 0030BEE8
0030BEC7  mov      rdx, qword ptr [rcx + 0x698]
0030BECE  test     rdx, rdx
0030BED1  je       0x30bee8  ; -> 0030BEE8
0030BED3  movzx    ecx, byte ptr [rdx + 5]
0030BED7  test     ecx, ecx
0030BED9  jne      0x30bee8  ; -> 0030BEE8
0030BEDB  shr      eax, 0x17
0030BEDE  not      eax
0030BEE0  and      eax, 1
0030BEE3  add      rsp, 0x28
0030BEE7  ret      
0030BEE8  xor      eax, eax
0030BEEA  add      rsp, 0x28
0030BEEE  ret      
```

## 003241D0 (100 B, extent 003241D0-00324234)

Page context: "xFF' → desired bit 'row.b_1A' | | **licences** | '00310127'–'003102DF' | for node 'i < 0x169': bit 'i' of the record's bitmap '+0x194'; 'entry = 02EBF038 + i × stride'; '00323890(entry.b_05) == 2' — '003241D0' maps byte '+5' **values 15–18** to groups '0x1B' / '0x1C' (table '00324260'), which the jump table at '003238E4' classes as 2 — then each of the eight words 'entry + 8 … + 0x16' that is not '0xFFFF' is a desired bit | | **the diff"

```
003241D0  dec      ecx
003241D2  cmp      ecx, 0x1d
003241D5  ja       0x324231  ; -> 00324231
003241D7  movsxd   rax, ecx
003241DA  lea      rdx, [rip - 0x2041e1]  ; -> 00120000 (image base)
003241E1  movzx    eax, byte ptr [rdx + rax + 0x204260]
003241E9  mov      ecx, dword ptr [rdx + rax*4 + 0x204234]  ; image base + 0x204234 = 00324234
003241F0  add      rcx, rdx
003241F3  jmp      rcx
003241F5  mov      eax, 0x15
003241FA  ret      
003241FB  mov      eax, 0x16
00324200  ret      
00324201  mov      eax, 0x17
00324206  ret      
00324207  mov      eax, 0x18
0032420C  ret      
0032420D  mov      eax, 0x19
00324212  ret      
00324213  mov      eax, 0x1a
00324218  ret      
00324219  mov      eax, 0x1b
0032421E  ret      
0032421F  mov      eax, 0x1c
00324224  ret      
00324225  mov      eax, 0x1d
0032422A  ret      
0032422B  mov      eax, 0x1e
00324230  ret      
00324231  xor      eax, eax
00324233  ret      
```

## 0033F100 (77 B, extent 0033F100-0033F14D)

Page context: "ata resolver '002650B0', among them 'VM_Spawn_SetLaneCandidateTable' '005105A0', 'VM_Spawn_SetEntryMapAndResetTransientEntries' '00510620', 'VM_Spawn_InitializeKeepEntriesFromDefinition' '005106D0', '0033F100' and '0050E060'. A foe's innate-augment word '+0xE80' and authored-status word '+0xE90' are written by two script verbs of the 'btlAtel' family, as the section on the foe's two masks shows; the other edges are the verb layer's shar"

```
0033F100  mov      qword ptr [rsp + 8], rbx
0033F105  mov      qword ptr [rsp + 0x10], rsi
0033F10A  push     rdi
0033F10B  sub      rsp, 0x20
0033F10F  mov      rbx, r9
0033F112  mov      rdi, rdx
0033F115  call     0x2640c0  ; -> 002640C0 fn
0033F11A  mov      rcx, rbx
0033F11D  mov      rsi, rax
0033F120  call     0x267e10  ; -> 00267E10 fn
0033F125  mov      r8d, eax
0033F128  mov      rdx, rdi
0033F12B  mov      rcx, rsi
0033F12E  call     0x2650b0  ; -> 002650B0 fn
0033F133  mov      rdx, rax
0033F136  mov      rcx, rsi
0033F139  mov      rbx, qword ptr [rsp + 0x30]
0033F13E  mov      rsi, qword ptr [rsp + 0x38]
0033F143  add      rsp, 0x20
0033F147  pop      rdi
0033F148  jmp      0x3e92f0  ; -> 003E92F0 fn
```

## 00505560 (16 B, extent 00505560-00505570)

Page context: "d is freed once that counter passes '0x25'. The tick also ramps       the layer alpha '01EFE320' by ±0.2 towards the '01EFE31D' bit-1 state.     - The sweep '003BBB60' hands each non-status entry to '00505560', which jumps through the type table       '00D22790': type 0 → '00505E00', type 1 → '00505570', type 2 → the no-op, because type 2 is the status       label the billboard pass draws.   - **'00505E00' draws the digits.** It resolve"

```
00505560  movsx    rax, byte ptr [rcx + 0x3c]
00505565  lea      rdx, [rip + 0x81d224]  ; -> 00D22790
0050556C  jmp      qword ptr [rdx + rax*8]
```

## 0050E060 (232 B, extent 0050E060-0050E148)

Page context: "02650B0', among them 'VM_Spawn_SetLaneCandidateTable' '005105A0', 'VM_Spawn_SetEntryMapAndResetTransientEntries' '00510620', 'VM_Spawn_InitializeKeepEntriesFromDefinition' '005106D0', '0033F100' and '0050E060'. A foe's innate-augment word '+0xE80' and authored-status word '+0xE90' are written by two script verbs of the 'btlAtel' family, as the section on the foe's two masks shows; the other edges are the verb layer's shared resolver tha"

```
0050E060  mov      qword ptr [rsp + 8], rbx
0050E065  mov      qword ptr [rsp + 0x10], rbp
0050E06A  mov      qword ptr [rsp + 0x18], rsi
0050E06F  mov      qword ptr [rsp + 0x20], rdi
0050E074  push     r14
0050E076  sub      rsp, 0x30
0050E07A  mov      rsi, r9
0050E07D  mov      rbp, rcx
0050E080  call     0x2640c0  ; -> 002640C0 fn
0050E085  mov      r14, rax
0050E088  mov      dword ptr [rsp + 0x20], 0
0050E090  mov      dword ptr [rsp + 0x24], 0
0050E098  mov      dword ptr [rsp + 0x28], 0
0050E0A0  call     0x3590d0  ; -> 003590D0 fn
0050E0A5  test     eax, eax
0050E0A7  je       0x50e0c7  ; -> 0050E0C7
0050E0A9  mov      ecx, eax
0050E0AB  call     0x3588b0  ; -> 003588B0 fn
0050E0B0  lea      r9, [rsp + 0x28]
0050E0B5  mov      rcx, rax
0050E0B8  lea      r8, [rsp + 0x24]
0050E0BD  lea      rdx, [rsp + 0x20]
0050E0C2  call     0x265020  ; -> 00265020 fn
0050E0C7  mov      rcx, rsi
0050E0CA  call     0x267e10  ; -> 00267E10 fn
0050E0CF  mov      r8d, eax
0050E0D2  mov      rdx, rbp
0050E0D5  mov      rcx, r14
0050E0D8  call     0x2650b0  ; -> 002650B0 fn
0050E0DD  mov      rcx, rsi
0050E0E0  mov      rdi, rax
0050E0E3  call     0x267e10  ; -> 00267E10 fn
0050E0E8  mov      r8d, eax
0050E0EB  mov      rdx, rbp
0050E0EE  mov      rcx, r14
0050E0F1  call     0x2650b0  ; -> 002650B0 fn
0050E0F6  mov      rcx, rsi
0050E0F9  mov      rbx, rax
0050E0FC  call     0x267e10  ; -> 00267E10 fn
0050E101  mov      r8d, eax
0050E104  mov      rdx, rbp
0050E107  mov      rcx, r14
0050E10A  call     0x2650b0  ; -> 002650B0 fn
0050E10F  movss    xmm0, dword ptr [rsp + 0x20]
0050E115  mov      rbp, qword ptr [rsp + 0x48]
0050E11A  mov      rsi, qword ptr [rsp + 0x50]
0050E11F  movss    dword ptr [rax], xmm0
0050E123  movss    xmm1, dword ptr [rsp + 0x24]
0050E129  movss    dword ptr [rbx], xmm1
0050E12D  movss    xmm0, dword ptr [rsp + 0x28]
0050E133  mov      rbx, qword ptr [rsp + 0x40]
0050E138  movss    dword ptr [rdi], xmm0
0050E13C  mov      rdi, qword ptr [rsp + 0x58]
0050E141  add      rsp, 0x30
0050E145  pop      r14
0050E147  ret      
```

## 005105A0 (63 B, extent 005105A0-005105DF)

Page context: "rguments with 'VMValueStack_PopInt32CoerceFloat32' '00267E10'; '005102D0' calls '0031B760'; and 29 verb handlers call the script-data resolver '002650B0', among them 'VM_Spawn_SetLaneCandidateTable' '005105A0', 'VM_Spawn_SetEntryMapAndResetTransientEntries' '00510620', 'VM_Spawn_InitializeKeepEntriesFromDefinition' '005106D0', '0033F100' and '0050E060'. A foe's innate-augment word '+0xE80' and authored-status word '+0xE90' are written b"

```
005105A0  mov      qword ptr [rsp + 8], rbx
005105A5  push     rdi
005105A6  sub      rsp, 0x20
005105AA  mov      rcx, r9
005105AD  mov      rdi, rdx
005105B0  call     0x267e10  ; -> 00267E10 fn
005105B5  mov      ebx, eax
005105B7  call     0x2640c0  ; -> 002640C0 fn
005105BC  mov      rcx, rax
005105BF  mov      r8d, ebx
005105C2  mov      rdx, rdi
005105C5  call     0x2650b0  ; -> 002650B0 fn
005105CA  mov      rdx, rax
005105CD  mov      rcx, rdi
005105D0  mov      rbx, qword ptr [rsp + 0x30]
005105D5  add      rsp, 0x20
005105D9  pop      rdi
005105DA  jmp      0x2393e0  ; -> 002393E0 fn
```

## 005106D0 (60 B, extent 005106D0-0051070C)

Page context: "the script-data resolver '002650B0', among them 'VM_Spawn_SetLaneCandidateTable' '005105A0', 'VM_Spawn_SetEntryMapAndResetTransientEntries' '00510620', 'VM_Spawn_InitializeKeepEntriesFromDefinition' '005106D0', '0033F100' and '0050E060'. A foe's innate-augment word '+0xE80' and authored-status word '+0xE90' are written by two script verbs of the 'btlAtel' family, as the section on the foe's two masks shows; the other edges are the verb "

```
005106D0  mov      qword ptr [rsp + 8], rbx
005106D5  push     rdi
005106D6  sub      rsp, 0x20
005106DA  mov      rcx, r9
005106DD  mov      rdi, rdx
005106E0  call     0x267e10  ; -> 00267E10 fn
005106E5  mov      ebx, eax
005106E7  call     0x2640c0  ; -> 002640C0 fn
005106EC  mov      rcx, rax
005106EF  mov      r8d, ebx
005106F2  mov      rdx, rdi
005106F5  call     0x2650b0  ; -> 002650B0 fn
005106FA  mov      rcx, rax
005106FD  mov      rbx, qword ptr [rsp + 0x30]
00510702  add      rsp, 0x20
00510706  pop      rdi
00510707  jmp      0x2395a0  ; -> 002395A0 fn
```
