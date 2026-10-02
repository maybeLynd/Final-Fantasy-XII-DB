# F-interior pack: `10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/contract-auto-status-rebuild.json`.

Functions: 14. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 1a00debc7	EXP-263: 51BA80 insert front — cap gate + populate-fail arms; 0251f9d15	EXP-262: 51BA40/51F240 mode-0 + &2 arms, 41CF00 block loop + 0x1000 arm (577/577); inbox mentions: SWE2-FRONTIER.md). OPUS read these before packing.

## 001E0C30 (25 B, extent 001E0C30-001E0C49)

Page context: "edges).** 'InputManager_TranslateBindingProfileToControlState' '00197160', '00197790' and '00197800' call the lazy singleton accessor '001D50D0'; the inline-glyph drawer '002AEB20' calls '001E0C10', '001E0C30' and the escape-code dispatch '002AB8F0' (the button-glyph lookup); '00226BE0' and '002E09A0' call the handle resolver '00263FF0', and '00226BE0' also calls 'PartyRoster_GetActorBySlot' '00263750'; 'InputGameplay_ArbitrateDigitalIn"

```
001E0C30  sub      rsp, 0x28
001E0C34  call     0x796e20  ; -> 00796E20 fn
001E0C39  mov      rcx, qword ptr [rax + 0xdf8]
001E0C40  add      rsp, 0x28
001E0C44  jmp      0x225680  ; -> 00225680 fn
```

## 002B3E30 (87 B, extent 002B3E30-002B3E87)

Page context: "0/450, stable ×3, hash '78ec7301…'** ('_experiments/EXP-208-segment-string-walkers-exec.md'). The helper subtree stays bounded — control decode '002AC2F0', interpreter '002AC5F0', tag-'0xE' adjuster '002B3E30', and the '17Fxxx' font shims are scripted boundaries; 'memcmp', '0020E600', 'ceilf' math and the cookie run native.  - '002B2150(&state, cursor, &w, &h)' is the single-line walker: it   saves 'b10FC'/'b10FF', 'q[0209CC48]' (cleare"

```
002B3E30  movss    xmm0, dword ptr [rcx + 0x14]
002B3E35  addss    xmm0, dword ptr [rcx + 0x24]
002B3E3A  movss    xmm1, dword ptr [rcx + 0x10]
002B3E3F  comiss   xmm1, dword ptr [rcx + 0x20]
002B3E43  movss    dword ptr [rcx + 0x24], xmm0
002B3E48  jbe      0x2b3e4f  ; -> 002B3E4F
002B3E4A  movss    dword ptr [rcx + 0x20], xmm1
002B3E4F  movss    xmm1, dword ptr [rcx + 0x20]
002B3E54  comiss   xmm1, dword ptr [rcx + 0x30]
002B3E58  jbe      0x2b3e5f  ; -> 002B3E5F
002B3E5A  movss    dword ptr [rcx + 0x30], xmm1
002B3E5F  comiss   xmm0, dword ptr [rcx + 0x34]
002B3E63  jbe      0x2b3e6a  ; -> 002B3E6A
002B3E65  movss    dword ptr [rcx + 0x34], xmm0
002B3E6A  xor      eax, eax
002B3E6C  mov      qword ptr [rcx + 0x1c], 0x3f800000
002B3E74  mov      qword ptr [rcx + 0x14], rax
002B3E78  mov      dword ptr [rcx + 0x10], eax
002B3E7B  mov      qword ptr [rcx + 0x24], rax
002B3E7F  mov      dword ptr [rcx + 0x2c], 0x3f800000
002B3E86  ret      
```

## 002EBB80 (41 B, extent 002EBB80-002EBBA9)

Page context: "e-identical 'result.json'; 'NATIVE-REPLAY', 'live_game: false'), with twenty-one leaf/helper callees promoted real and the heavy subtrees ('003105D0', '00238BF0', '00311F70', '0023B040', '002ECF10', '002EBB80', the '0024FE70' query, the lock pair) kept scripted as disclosed boundaries:  - **'00300FC0(obj, edx)'** — 'edx==0' + linked rec + 'b5==0' + 'b4∈[0x1B,0x27]' →   '003105D0(obj)' + tail '003138D0(0)'. Otherwise the full teardown:  "

```
002EBB80  movzx    eax, byte ptr [rcx + 3]
002EBB84  and      al, 0xe0
002EBB86  cmp      al, 0x60
002EBB88  jne      0x2ebba8  ; -> 002EBBA8
002EBB8A  mov      rax, qword ptr [rcx + 0xc0]
002EBB91  test     rax, rax
002EBB94  je       0x2ebba8  ; -> 002EBBA8
002EBB96  and      byte ptr [rax + 0x10], 0xf7
002EBB9A  and      dl, 1
002EBB9D  shl      dl, 3
002EBBA0  or       byte ptr [rax + 0x10], dl
002EBBA3  jmp      0x2e8fd0  ; -> 002E8FD0 fn
002EBBA8  ret      
```

## 003241D0 (100 B, extent 003241D0-00324234)

Page context: "pace can reach them.  ### 13a. The three gates, executed — 2026-09-18 (OPUS, consuming SWE2-ORACLE's EXP-100)  EXP-100 ran '00322C50', '0031E9A0' and '00323890' — and their sub-bodies '0031E9F0' and '003241D0' — as shipped bytes inside the subject, **40/40 cases, 13/13 mutants, two processes, 8 real bodies**. The gates are no longer oracles. **Both writers still are**, and §13's live-only paragraph is otherwise unchanged.  **Finding 3 i"

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

## 0033F7F0 (58 B, extent 0033F7F0-0033F82A)

Page context: " handlers, among them '0033FD60', '00344AF0', '0050E060'), 'PartyRoster_GetActorBySlot' '00263750' (20, among them '003415D0', '00342250', '003537D0'), the handle resolver '00263FF0' (20, among them '0033F7F0', '00348130', '0050D0C0'), 'ActorHandle_EncodeRegistryEntry' '003589B0' (12), the unlink leaf '002ECF10' (10), 'BattleStats_GetByMappedBattleSlot' '00320AB0' (7, the '0050FD00' to '0050FF20' run), '002EB430' (6), '00377C20' (4), '0"

```
0033F7F0  mov      qword ptr [rsp + 8], rbx
0033F7F5  push     rdi
0033F7F6  sub      rsp, 0x20
0033F7FA  mov      rdi, rcx
0033F7FD  xor      ecx, ecx
0033F7FF  call     0x263ff0  ; -> 00263FF0 fn
0033F804  mov      rbx, rax
0033F807  call     0x3148b0  ; -> 003148B0 fn
0033F80C  mov      edx, eax
0033F80E  mov      rcx, rbx
0033F811  call     0x264ce0  ; -> 00264CE0 fn
0033F816  mov      edx, eax
0033F818  mov      rcx, rdi
0033F81B  mov      rbx, qword ptr [rsp + 0x30]
0033F820  add      rsp, 0x20
0033F824  pop      rdi
0033F825  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 003415D0 (43 B, extent 003415D0-003415FB)

Page context: "lers call the shared leaves the harness ran: 'Actor_GetWorldPosition' '00265020' (23 handlers, among them '0033FD60', '00344AF0', '0050E060'), 'PartyRoster_GetActorBySlot' '00263750' (20, among them '003415D0', '00342250', '003537D0'), the handle resolver '00263FF0' (20, among them '0033F7F0', '00348130', '0050D0C0'), 'ActorHandle_EncodeRegistryEntry' '003589B0' (12), the unlink leaf '002ECF10' (10), 'BattleStats_GetByMappedBattleSlot' "

```
003415D0  push     rbx
003415D2  sub      rsp, 0x20
003415D6  xor      ebx, ebx
003415D8  mov      ecx, ebx
003415DA  call     0x263750  ; -> 00263750 fn
003415DF  test     rax, rax
003415E2  je       0x3415ee  ; -> 003415EE
003415E4  xor      edx, edx
003415E6  mov      rcx, rax
003415E9  call     0x26dc40  ; -> 0026DC40 fn
003415EE  inc      ebx
003415F0  cmp      ebx, 4
003415F3  jl       0x3415d8  ; -> 003415D8
003415F5  add      rsp, 0x20
003415F9  pop      rbx
003415FA  ret      
```

## 00342250 (46 B, extent 00342250-0034227E)

Page context: "e shared leaves the harness ran: 'Actor_GetWorldPosition' '00265020' (23 handlers, among them '0033FD60', '00344AF0', '0050E060'), 'PartyRoster_GetActorBySlot' '00263750' (20, among them '003415D0', '00342250', '003537D0'), the handle resolver '00263FF0' (20, among them '0033F7F0', '00348130', '0050D0C0'), 'ActorHandle_EncodeRegistryEntry' '003589B0' (12), the unlink leaf '002ECF10' (10), 'BattleStats_GetByMappedBattleSlot' '00320AB0' ("

```
00342250  push     rbx
00342252  sub      rsp, 0x20
00342256  xor      ebx, ebx
00342258  mov      ecx, ebx
0034225A  call     0x263750  ; -> 00263750 fn
0034225F  test     rax, rax
00342262  je       0x342271  ; -> 00342271
00342264  mov      edx, 1
00342269  mov      rcx, rax
0034226C  call     0x26dc40  ; -> 0026DC40 fn
00342271  inc      ebx
00342273  cmp      ebx, 4
00342276  jl       0x342258  ; -> 00342258
00342278  add      rsp, 0x20
0034227C  pop      rbx
0034227D  ret      
```

## 00348130 (37 B, extent 00348130-00348155)

Page context: "mong them '0033FD60', '00344AF0', '0050E060'), 'PartyRoster_GetActorBySlot' '00263750' (20, among them '003415D0', '00342250', '003537D0'), the handle resolver '00263FF0' (20, among them '0033F7F0', '00348130', '0050D0C0'), 'ActorHandle_EncodeRegistryEntry' '003589B0' (12), the unlink leaf '002ECF10' (10), 'BattleStats_GetByMappedBattleSlot' '00320AB0' (7, the '0050FD00' to '0050FF20' run), '002EB430' (6), '00377C20' (4), '0026DAC0' and"

```
00348130  push     rbx
00348132  sub      rsp, 0x20
00348136  mov      ecx, 3
0034813B  call     0x263ff0  ; -> 00263FF0 fn
00348140  mov      rbx, rax
00348143  call     0x3b6f30  ; -> 003B6F30 fn
00348148  mov      rcx, rbx
0034814B  add      rsp, 0x20
0034814F  pop      rbx
00348150  jmp      0x3b72f0  ; -> 003B72F0 fn
```

## 003592C0 (103 B, extent 003592C0-00359327)

Page context: "andle_Thunk' '003272E0' or 'PartyControl_RecomputeSuppressionFromLeaderBattleState' '0023B040'; '0023B040' calls 'BattleUnit_GetPartyLeader' '003272A0' and the two suppression setters '00359200' and '003592C0'; the 'resetJobs' body '00328BD0' calls '0030FED0' and '003138D0'. When a unit is released the carriers re-resolve the leader and focus and recompute party suppression, and the roster bodies share this page's class test and unit ac"

```
003592C0  sub      rsp, 0x28
003592C4  test     edx, edx
003592C6  je       0x3592da  ; -> 003592DA
003592C8  movzx    edx, byte ptr [rip + 0x1f6ed36]  ; -> 022C8005
003592CF  bts      edx, ecx
003592D2  mov      byte ptr [rip + 0x1f6ed2d], dl  ; -> 022C8005
003592D8  jmp      0x3592ed  ; -> 003592ED
003592DA  movzx    eax, byte ptr [rip + 0x1f6ed24]  ; -> 022C8005
003592E1  btr      eax, ecx
003592E4  movzx    edx, al
003592E7  mov      byte ptr [rip + 0x1f6ed18], al  ; -> 022C8005
003592ED  movzx    eax, byte ptr [rip + 0x1f6ed10]  ; -> 022C8004
003592F4  or       al, byte ptr [rip + 0x1f6ed0c]  ; -> 022C8006
003592FA  or       al, byte ptr [rip + 0x1f6ed07]  ; -> 022C8007
00359300  or       al, dl
00359302  test     al, 1
00359304  je       0x359322  ; -> 00359322
00359306  mov      ecx, dword ptr [rip + 0x1f6ecd4]  ; -> 022C7FE0
0035930C  call     0x3588b0  ; -> 003588B0 fn
00359311  test     rax, rax
00359314  je       0x359322  ; -> 00359322
00359316  mov      rcx, rax
00359319  add      rsp, 0x28
0035931D  jmp      0x26d6d0  ; -> 0026D6D0 fn
00359322  add      rsp, 0x28
00359326  ret      
```

## 0042DE90 (45 B, extent 0042DE90-0042DEBD)

Page context: "[022C6F28]+idx*0x740' row → '00426220' signature gate → on ret 0 'd[row+0x284]|=0x100000' + 'b[row+0xC0]&=0xBF'; leaf arm pinned on 'u43f0-ec' ('w[row+8]'==-1 skips the child walk and the '0042EF90'/'0042DE90' enqueue, which faulted on the zeroed fixture — stack-set structure not modelled, arm unclaimed). Result: '556/556, stable ×3', hash '9174099b' ('_experiments/EXP-256-469570-fall-426FA0-exec.md'). Still unclaimed: '00426FA0''s chil"

```
0042DE90  push     rbx
0042DE92  sub      rsp, 0x20
0042DE96  mov      rdx, qword ptr [rdx + 8]
0042DE9A  mov      rbx, rcx
0042DE9D  call     0x426220  ; -> 00426220 fn
0042DEA2  test     eax, eax
0042DEA4  jne      0x42deb7  ; -> 0042DEB7
0042DEA6  or       dword ptr [rbx + 0x284], 0x100000
0042DEB0  and      byte ptr [rbx + 0xc0], 0xbf
0042DEB7  add      rsp, 0x20
0042DEBB  pop      rbx
0042DEBC  ret      
```

## 0050E060 (232 B, extent 0050E060-0050E148)

Page context: ".  **Script_VM_Native_Bridge — CLIENT (116 edges).** Script verb handlers call the shared leaves the harness ran: 'Actor_GetWorldPosition' '00265020' (23 handlers, among them '0033FD60', '00344AF0', '0050E060'), 'PartyRoster_GetActorBySlot' '00263750' (20, among them '003415D0', '00342250', '003537D0'), the handle resolver '00263FF0' (20, among them '0033F7F0', '00348130', '0050D0C0'), 'ActorHandle_EncodeRegistryEntry' '003589B0' (12), "

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

## 0051F150 (17 B, extent 0051F150-0051F161)

Page context: "51BA80' insert front — cap gate + populate-fail arms — EXP-263  The "deeper '0051BA40' body" was misattributed — '0051BA40' ends at '0x51BA76'; '0051BA80' is a distinct 5-arg **insert**: 'edx==-1' → '0051F150' cap gate ('d[C+0x14]>=d[C+0x10]' → '-10') → '0041CB90' stack-record reset → '0041D220(&tmp, src)' populate → 'ebx==-1' → '0051F080' alloc → '0051F240' → '0x390' record copy → '0041CA70' → 'd[rec]=ebx' ret key. Three new 'd51ba80-*"

```
0051F150  mov      eax, dword ptr [rcx + 0x10]
0051F153  cmp      dword ptr [rcx + 0x14], eax
0051F156  mov      eax, 0xfffffff6
0051F15B  jge      0x51f160  ; -> 0051F160
0051F15D  mov      eax, dword ptr [rcx + 0x18]
0051F160  ret      
```

## 0057FB00 (887 B, extent 0057FB00-0057FE77)

Page context: " '00234590' calls '00237260', '0023B040', '00300140', '00313F60', '0031B770', '003272A0', '0032A150' and '0035C8A0'; '005369C0' calls 'MapRef_GetAreaArdFieldResourceIndex' '00264ED0' and '003148F0'; '0057FB00' calls '00264150'. The release, status-change and reward bodies consult the field record's bit 15 before acting, and the field frame is the per-frame caller of several carriers the harness ran. "

```
0057FB00  mov      qword ptr [rsp + 0x20], rbx
0057FB05  push     rbp
0057FB06  push     rsi
0057FB07  push     rdi
0057FB08  push     r12
0057FB0A  push     r13
0057FB0C  push     r14
0057FB0E  push     r15
0057FB10  sub      rsp, 0x60
0057FB14  mov      rax, qword ptr [rip + 0x19c4d15]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0057FB1B  xor      rax, rsp
0057FB1E  mov      qword ptr [rsp + 0x50], rax
0057FB23  or       r12d, 0xffffffff
0057FB27  mov      r15, r8
0057FB2A  test     byte ptr [r8 + 0x57], 1
0057FB2F  mov      r9, rdx
0057FB32  mov      rbx, rcx
0057FB35  lea      r14d, [r12 + 3]
0057FB3A  je       0x57fb94  ; -> 0057FB94
0057FB3C  mov      rcx, qword ptr [rcx + 8]
0057FB40  lea      r8, [rsp + 0x40]
0057FB45  mov      dword ptr [rsp + 0x30], 0x20002
0057FB4D  lea      rdx, [rsp + 0x30]
0057FB52  movzx    eax, word ptr [rcx + 8]
0057FB56  sub      ax, 4
0057FB5A  mov      word ptr [rsp + 0x34], ax
0057FB5F  movzx    eax, word ptr [rcx + 0xa]
0057FB63  mov      rcx, r9
0057FB66  sub      ax, 4
0057FB6A  mov      dword ptr [rsp + 0x4c], 0x4816224a
0057FB72  mov      word ptr [rsp + 0x36], ax
0057FB77  mov      dword ptr [rsp + 0x48], 0x4816224a
0057FB7F  mov      dword ptr [rsp + 0x44], 0x4816224a
0057FB87  mov      dword ptr [rsp + 0x40], 0x4816224a
0057FB8F  call     0x2dc290  ; -> 002DC290 fn
0057FB94  mov      edx, 1
0057FB99  mov      rcx, rbx
0057FB9C  call     0x393190  ; -> 00393190 fn
0057FBA1  mov      rax, qword ptr [rbx + 0x10]
0057FBA5  lea      r9, [rip + 0x7a4300]  ; -> 00D23EAC
0057FBAC  mov      rcx, qword ptr [rax + 0xd8]
0057FBB3  and      dword ptr [rcx + 8], 0xfffffffe
0057FBB7  mov      rax, qword ptr [rbx + 0x10]
0057FBBB  mov      rcx, qword ptr [rax + 0xb0]
0057FBC2  and      dword ptr [rcx + 8], 0xfffffffe
0057FBC6  xor      r13d, r13d
0057FBC9  mov      r8d, r13d
0057FBCC  nop      dword ptr [rax]
0057FBD0  movzx    ecx, byte ptr [r9]
0057FBD4  lea      r9, [r9 + 1]
0057FBD8  mov      rax, qword ptr [rbx + 0x10]
0057FBDC  inc      r8d
0057FBDF  mov      rdx, qword ptr [rax + rcx*8]
0057FBE3  or       dword ptr [rdx + 8], 1
0057FBE7  cmp      r8d, 7
0057FBEB  jb       0x57fbd0  ; -> 0057FBD0
0057FBED  mov      rax, qword ptr [rbx + 0x10]
0057FBF1  mov      rcx, qword ptr [rax + 0xd0]
0057FBF8  and      dword ptr [rcx + 8], 0xfffffffe
0057FBFC  test     byte ptr [r15 + 0x57], 4
0057FC01  je       0x57fc12  ; -> 0057FC12
0057FC03  mov      rax, qword ptr [rbx + 0x10]
0057FC07  mov      rcx, qword ptr [rax + 0xd8]
0057FC0E  or       dword ptr [rcx + 8], 1
0057FC12  test     byte ptr [r15 + 0x57], 1
0057FC17  mov      ecx, dword ptr [r15 + 0x4c]
0057FC1B  mov      esi, ecx
0057FC1D  je       0x57fce5  ; -> 0057FCE5
0057FC23  mov      eax, dword ptr [r15 + 0x80]
0057FC2A  test     eax, eax
0057FC2C  cmove    eax, ecx
0057FC2F  mov      dword ptr [rsp + 0x30], eax
0057FC33  call     0x377b60  ; -> 00377B60 fn
0057FC38  mov      rcx, qword ptr [rbx + 0x10]
0057FC3C  mov      rdi, qword ptr [rcx + 0xb8]
0057FC43  xor      ecx, ecx
0057FC45  mov      qword ptr [rdi + 0x18], rax
0057FC49  call     0x20e620  ; -> 0020E620 fn
0057FC4E  or       dword ptr [rdi + 8], 1
0057FC52  lea      r8, [rsp + 0x3c]
0057FC57  lea      rdx, [rsp + 0x38]
0057FC5C  mov      dword ptr [rdi + 0x20], eax
0057FC5F  mov      rcx, rdi
0057FC62  call     0x29fe20  ; -> 0029FE20 fn
0057FC67  mov      rax, qword ptr [rbx + 0x10]
0057FC6B  movsx    esi, word ptr [rdi + 0xc]
0057FC6F  movsx    ebp, word ptr [rdi + 0xe]
0057FC73  mov      rcx, qword ptr [rax + 0xc8]
0057FC7A  sub      si, word ptr [rcx + 0x10]
0057FC7E  or       dword ptr [rcx + 8], 1
0057FC82  mov      word ptr [rcx + 0xc], si
0057FC86  mov      ecx, dword ptr [r15 + 0x4c]
0057FC8A  call     0x3778b0  ; -> 003778B0 fn
0057FC8F  mov      rcx, qword ptr [rbx + 0x10]
0057FC93  mov      rdi, rax
0057FC96  mov      r14, qword ptr [rcx + 0xc0]
0057FC9D  mov      rcx, r14
0057FCA0  sub      si, word ptr [r14 + 0x10]
0057FCA5  mov      word ptr [r14 + 0xc], si
0057FCAA  mov      word ptr [r14 + 0xe], bp
0057FCAF  call     0x29fb50  ; -> 0029FB50 fn
0057FCB4  mov      rcx, qword ptr [r14]
0057FCB7  or       dword ptr [r14 + 8], 1
0057FCBC  movzx    edx, word ptr [rcx + 4]
0057FCC0  xor      ecx, ecx
0057FCC2  sub      dx, word ptr [rsp + 0x38]
0057FCC7  mov      word ptr [r14 + 0xc], dx
0057FCCC  mov      qword ptr [r14 + 0x18], rdi
0057FCD0  call     0x20e620  ; -> 0020E620 fn
0057FCD5  mov      esi, dword ptr [rsp + 0x30]
0057FCD9  mov      dword ptr [r14 + 0x20], eax
0057FCDD  mov      r14d, 2
0057FCE3  jmp      0x57fd12  ; -> 0057FD12
0057FCE5  mov      rax, qword ptr [rbx + 0x10]
0057FCE9  mov      rcx, qword ptr [rax + 0xc0]
0057FCF0  and      dword ptr [rcx + 8], 0xfffffffe
0057FCF4  mov      rax, qword ptr [rbx + 0x10]
0057FCF8  mov      rcx, qword ptr [rax + 0xc8]
0057FCFF  and      dword ptr [rcx + 8], 0xfffffffe
0057FD03  mov      rax, qword ptr [rbx + 0x10]
0057FD07  mov      rcx, qword ptr [rax + 0xb8]
0057FD0E  and      dword ptr [rcx + 8], 0xfffffffe
0057FD12  mov      ecx, esi
0057FD14  call     0x3778b0  ; -> 003778B0 fn
0057FD19  mov      rbp, rax
0057FD1C  call     0x264150  ; -> 00264150 fn
0057FD21  test     eax, eax
0057FD23  je       0x57fd69  ; -> 0057FD69
0057FD25  mov      ecx, esi
0057FD27  call     0x264f90  ; -> 00264F90 fn
0057FD2C  cmp      eax, 7
0057FD2F  je       0x57fd58  ; -> 0057FD58
0057FD31  cmp      eax, 0x16
0057FD34  je       0x57fd50  ; -> 0057FD50
0057FD36  cmp      eax, 0x19
0057FD39  je       0x57fd48  ; -> 0057FD48
0057FD3B  cmp      eax, 0x1d
0057FD3E  jne      0x57fd69  ; -> 0057FD69
0057FD40  mov      r12d, 0x7ed
0057FD46  jmp      0x57fd5e  ; -> 0057FD5E
0057FD48  mov      r12d, 0x7ee
0057FD4E  jmp      0x57fd5e  ; -> 0057FD5E
0057FD50  mov      r12d, 0x7eb
0057FD56  jmp      0x57fd5e  ; -> 0057FD5E
0057FD58  mov      r12d, 0x7ec
0057FD5E  mov      ecx, r12d
0057FD61  call     0x2f9860  ; -> 002F9860 fn
0057FD66  mov      rbp, rax
0057FD69  mov      rax, qword ptr [rbx + 0x10]
0057FD6D  xor      ecx, ecx
0057FD6F  mov      rdi, qword ptr [rax + 0x90]
0057FD76  mov      qword ptr [rdi + 0x18], rbp
0057FD7A  call     0x20e620  ; -> 0020E620 fn
0057FD7F  mov      dword ptr [rdi + 0x20], eax
0057FD82  mov      rax, qword ptr [rbx + 0x10]
0057FD86  mov      rcx, qword ptr [rax + 0xa0]
0057FD8D  and      dword ptr [rcx + 8], 0xfffffffe
0057FD91  mov      ecx, esi
0057FD93  call     0x377b60  ; -> 00377B60 fn
0057FD98  mov      rcx, qword ptr [rbx + 0x10]
0057FD9C  mov      rdi, qword ptr [rcx + 0x98]
0057FDA3  xor      ecx, ecx
0057FDA5  mov      qword ptr [rdi + 0x18], rax
0057FDA9  call     0x20e620  ; -> 0020E620 fn
0057FDAE  mov      dword ptr [rdi + 0x20], eax
0057FDB1  cmp      r12d, -1
0057FDB5  je       0x57fdbf  ; -> 0057FDBF
0057FDB7  mov      esi, r13d
0057FDBA  mov      edi, r13d
0057FDBD  jmp      0x57fdf9  ; -> 0057FDF9
0057FDBF  movzx    eax, word ptr [r15 + 0x18]
0057FDC4  mov      ecx, 0x3e8
0057FDC9  mov      edi, 0x3b
0057FDCE  cmp      ax, cx
0057FDD1  jb       0x57fddb  ; -> 0057FDDB
0057FDD3  lea      r13d, [rcx - 1]
0057FDD7  mov      esi, edi
0057FDD9  jmp      0x57fdf9  ; -> 0057FDF9
0057FDDB  movzx    r13d, ax
0057FDDF  movzx    eax, byte ptr [r15 + 0x1a]
0057FDE4  movzx    esi, al
0057FDE7  cmp      al, 0x3c
0057FDE9  jb       0x57fded  ; -> 0057FDED
0057FDEB  mov      esi, edi
0057FDED  movzx    eax, byte ptr [r15 + 0x1b]
0057FDF2  cmp      al, 0x3c
0057FDF4  jae      0x57fdf9  ; -> 0057FDF9
0057FDF6  movzx    edi, al
0057FDF9  mov      r9d, 3
0057FDFF  mov      dword ptr [rsp + 0x20], r13d
0057FE04  mov      r8d, r9d
0057FE07  mov      edx, 8
0057FE0C  mov      rcx, rbx
0057FE0F  call     0x393160  ; -> 00393160 fn
0057FE14  mov      rax, qword ptr [rbx + 0x10]
0057FE18  mov      r9d, 1
0057FE1E  mov      r8d, r14d
0057FE21  mov      dword ptr [rsp + 0x20], esi
0057FE25  mov      rcx, rbx
0057FE28  mov      rdx, qword ptr [rax + 0x38]
0057FE2C  and      dword ptr [rdx + 8], 0xfffffffe
0057FE30  lea      edx, [r9 + 0xa]
0057FE34  call     0x393160  ; -> 00393160 fn
0057FE39  mov      r9d, 1
0057FE3F  mov      dword ptr [rsp + 0x20], edi
0057FE43  mov      r8d, r14d
0057FE46  mov      rcx, rbx
0057FE49  lea      edx, [r9 + 0xc]
0057FE4D  call     0x393160  ; -> 00393160 fn
0057FE52  mov      rcx, qword ptr [rsp + 0x50]
0057FE57  xor      rcx, rsp
0057FE5A  call     0x808c40  ; -> 00808C40 fn
0057FE5F  mov      rbx, qword ptr [rsp + 0xb8]
0057FE67  add      rsp, 0x60
0057FE6B  pop      r15
0057FE6D  pop      r14
0057FE6F  pop      r13
0057FE71  pop      r12
0057FE73  pop      rdi
0057FE74  pop      rsi
0057FE75  pop      rbp
0057FE76  ret      
```

## 00863240 (53 B, extent 00863240-00863275)

Page context: " by '00316930'; '008632B0' calls the singleton getter '0020CE00' and '0020CE60' and is called by '003162E0' and '00316440'; '00316760' is called by '00316810' and '00316C60'; '0020CE00' is called by '00863240' and '00863280'; the singleton allocator path '001CCB20' calls the platform timer '005CC930'. A reward or gil change feeds the achievement counters, which test the achieved bit and post through the notify gate '008632B0' (sections "

```
00863240  mov      qword ptr [rsp + 8], rbx
00863245  push     rdi
00863246  sub      rsp, 0x20
0086324A  mov      ebx, edx
0086324C  mov      edi, ecx
0086324E  call     0x20ce00  ; -> 0020CE00 fn
00863253  test     rax, rax
00863256  je       0x86326a  ; -> 0086326A
00863258  call     0x20ce00  ; -> 0020CE00 fn
0086325D  mov      rcx, rax
00863260  mov      r8d, ebx
00863263  mov      edx, edi
00863265  call     0x20cb50  ; -> 0020CB50 fn
0086326A  mov      rbx, qword ptr [rsp + 0x30]
0086326F  add      rsp, 0x20
00863273  pop      rdi
00863274  ret      
```
