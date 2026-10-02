# F-interior pack: `20-Platform-Online-Achievements/CONTRACT-steam-integration-subsystem.md`

Generated 2026-10-02 10:27 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/contract-steam-integration-subsystem.json`.

Functions: 6. Each is cited on the page only at its entry and is still in the F frontier.

## 001F3E10 (131 B, extent 001F3E10-001F3E93)

Page context: "on and achievement catalogue](steam-integration-and-achievement-catalogue.md).  ## 2. The objects (FABLE)  | object | where | role | |---|---|---| | the Steam API context | '01DFE0D0', init callback '001F3E10' | a table of interface pointers, re-fetched through 'SteamInternal_ContextInit' before every call; '+0x28' is the user-stats interface every call below uses | | the achievement manager | '0x80' bytes at '*(01F83450)', created by '"

```
001F3E10  push     rbx
001F3E12  sub      rsp, 0x20
001F3E16  xor      eax, eax
001F3E18  mov      rbx, rcx
001F3E1B  mov      qword ptr [rcx], rax
001F3E1E  mov      qword ptr [rcx + 8], rax
001F3E22  mov      qword ptr [rcx + 0x10], rax
001F3E26  mov      qword ptr [rcx + 0x18], rax
001F3E2A  mov      qword ptr [rcx + 0x20], rax
001F3E2E  mov      qword ptr [rcx + 0x28], rax
001F3E32  mov      qword ptr [rcx + 0x30], rax
001F3E36  mov      qword ptr [rcx + 0x38], rax
001F3E3A  mov      qword ptr [rcx + 0x40], rax
001F3E3E  mov      qword ptr [rcx + 0x48], rax
001F3E42  mov      qword ptr [rcx + 0x58], rax
001F3E46  mov      qword ptr [rcx + 0x50], rax
001F3E4A  mov      qword ptr [rcx + 0x60], rax
001F3E4E  mov      qword ptr [rcx + 0x68], rax
001F3E52  mov      qword ptr [rcx + 0x70], rax
001F3E56  mov      qword ptr [rcx + 0x78], rax
001F3E5A  mov      qword ptr [rcx + 0x80], rax
001F3E61  mov      qword ptr [rcx + 0x88], rax
001F3E68  mov      qword ptr [rcx + 0x90], rax
001F3E6F  mov      qword ptr [rcx + 0x98], rax
001F3E76  call     qword ptr [rip + 0x6cf324]  ; -> 008C31A0 [u64 0x0000000001CCBF72]
001F3E7C  test     eax, eax
001F3E7E  je       0x1f3e8d  ; -> 001F3E8D
001F3E80  mov      rcx, rbx
001F3E83  add      rsp, 0x20
001F3E87  pop      rbx
001F3E88  jmp      0x1f3ae0  ; -> 001F3AE0 fn
001F3E8D  add      rsp, 0x20
001F3E91  pop      rbx
001F3E92  ret      
```

## 0020C8C0 (121 B, extent 0020C8C0-0020C939)

Page context: "s observed live confidence: PROVEN implements:   - 20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md entries: [007980A0, 0020CD30, 0020C730, 007A3110, 0020C940, 0020CB20, 0020C8C0, 008632B0, 0020CE60, 00863240, 0020CB50] verified_against:   exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8   method: read from the authority image on 2026-09-25 (FABLE, Claude Opus 5.5) with capstone."

```
0020C8C0  push     rbx
0020C8C2  sub      rsp, 0x20
0020C8C6  movsxd   rax, dword ptr [rcx]
0020C8C9  mov      rbx, rcx
0020C8CC  cmp      rax, qword ptr [rdx]
0020C8CF  jne      0x20c933  ; -> 0020C933
0020C8D1  mov      eax, dword ptr [rcx + 0x10]
0020C8D4  inc      dword ptr [rcx + 0x14]
0020C8D7  dec      eax
0020C8D9  cmp      dword ptr [rcx + 0x14], eax
0020C8DC  jne      0x20c91d  ; -> 0020C91D
0020C8DE  lea      rcx, [rip + 0x1bf17eb]  ; -> 01DFE0D0
0020C8E5  call     qword ptr [rip + 0x6b68a5]  ; -> 008C3190 [u64 0x0000000001CCBFA6]
0020C8EB  mov      rdx, qword ptr [rbx + 8]
0020C8EF  mov      rcx, qword ptr [rax + 0x28]
0020C8F3  lea      r8, [rdx + 0x190]
0020C8FA  mov      rdx, qword ptr [rdx + 8]
0020C8FE  mov      rax, qword ptr [rcx]
0020C901  call     qword ptr [rax + 0x30]
0020C904  mov      rdx, qword ptr [rbx + 8]
0020C908  cmp      byte ptr [rdx + 0x190], 0
0020C90F  jne      0x20c91d  ; -> 0020C91D
0020C911  mov      rdx, qword ptr [rdx + 8]
0020C915  mov      rcx, rbx
0020C918  call     0x20ce10  ; -> 0020CE10 fn
0020C91D  lea      rdx, [rip + 0x6f9b6c]  ; -> 00906490
0020C924  mov      ecx, 2
0020C929  add      rsp, 0x20
0020C92D  pop      rbx
0020C92E  jmp      0x5cdaa0  ; -> 005CDAA0 fn
0020C933  add      rsp, 0x20
0020C937  pop      rbx
0020C938  ret      
```

## 0020CB20 (48 B, extent 0020CB20-0020CB50)

Page context: "ng here was observed live confidence: PROVEN implements:   - 20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md entries: [007980A0, 0020CD30, 0020C730, 007A3110, 0020C940, 0020CB20, 0020C8C0, 008632B0, 0020CE60, 00863240, 0020CB50] verified_against:   exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8   method: read from the authority image on 2026-09-25 (FABLE, Claude Opus 5.5) with"

```
0020CB20  movsxd   rax, dword ptr [rcx]
0020CB23  cmp      rax, qword ptr [rdx]
0020CB26  jne      0x20cb4f  ; -> 0020CB4F
0020CB28  mov      r8d, dword ptr [rdx + 8]
0020CB2C  mov      ecx, 2
0020CB31  cmp      r8d, 1
0020CB35  jne      0x20cb43  ; -> 0020CB43
0020CB37  lea      rdx, [rip + 0x6f991a]  ; -> 00906458
0020CB3E  jmp      0x5cdaa0  ; -> 005CDAA0 fn
0020CB43  lea      rdx, [rip + 0x6f9926]  ; -> 00906470
0020CB4A  jmp      0x5cdaa0  ; -> 005CDAA0 fn
0020CB4F  ret      
```

## 0020CCC0 (105 B, extent 0020CCC0-0020CD29)

Page context: "sReceived' → '0020C940';    - **1102** 'UserStatsStored' → '0020CB20';    - **1103** 'UserAchievementStored' → '0020C8C0'.     It then makes one user-stats call (slot '+0x48', the stats request) and '0020CCC0'. Next,    '008655E0' registers callback **331** ('GameOverlayActivated', '0x14B'). 4. **Always:** 'SteamAPI_RestartAppIfNecessary(0x91640)' ('0079813C'). '0x91640' is 595520, this    game's Steam application id. **If it returns tr"

```
0020CCC0  sub      rsp, 0x28
0020CCC4  lea      rcx, [rip + 0x1bf1405]  ; -> 01DFE0D0
0020CCCB  call     qword ptr [rip + 0x6b64bf]  ; -> 008C3190 [u64 0x0000000001CCBFA6]
0020CCD1  cmp      qword ptr [rax + 0x28], 0
0020CCD6  je       0x20cd22  ; -> 0020CD22
0020CCD8  lea      rcx, [rip + 0x1bf13f1]  ; -> 01DFE0D0
0020CCDF  call     qword ptr [rip + 0x6b64ab]  ; -> 008C3190 [u64 0x0000000001CCBFA6]
0020CCE5  cmp      qword ptr [rax + 8], 0
0020CCEA  je       0x20cd22  ; -> 0020CD22
0020CCEC  lea      rcx, [rip + 0x1bf13dd]  ; -> 01DFE0D0
0020CCF3  call     qword ptr [rip + 0x6b6497]  ; -> 008C3190 [u64 0x0000000001CCBFA6]
0020CCF9  mov      rcx, qword ptr [rax + 8]
0020CCFD  mov      rax, qword ptr [rcx]
0020CD00  call     qword ptr [rax + 8]
0020CD03  test     al, al
0020CD05  je       0x20cd22  ; -> 0020CD22
0020CD07  lea      rcx, [rip + 0x1bf13c2]  ; -> 01DFE0D0
0020CD0E  call     qword ptr [rip + 0x6b647c]  ; -> 008C3190 [u64 0x0000000001CCBFA6]
0020CD14  mov      rcx, qword ptr [rax + 0x28]
0020CD18  mov      rax, qword ptr [rcx]
0020CD1B  add      rsp, 0x28
0020CD1F  jmp      qword ptr [rax]
0020CD22  xor      al, al
0020CD24  add      rsp, 0x28
0020CD28  ret      
```

## 0020CD30 (77 B, extent 0020CD30-0020CD7D)

Page context: " the failure behaviour are STATIC; nothing here was observed live confidence: PROVEN implements:   - 20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md entries: [007980A0, 0020CD30, 0020C730, 007A3110, 0020C940, 0020CB20, 0020C8C0, 008632B0, 0020CE60, 00863240, 0020CB50] verified_against:   exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8   method: read from the authority image on "

```
0020CD30  sub      rsp, 0x38
0020CD34  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0020CD3D  cmp      qword ptr [rip + 0x1d7670b], 0  ; -> 01F83450
0020CD45  jne      0x20cd78  ; -> 0020CD78
0020CD47  mov      ecx, 0x80
0020CD4C  call     0x210ec0  ; -> 00210EC0 fn
0020CD51  mov      qword ptr [rsp + 0x40], rax
0020CD56  test     rax, rax
0020CD59  je       0x20cd71  ; -> 0020CD71
0020CD5B  mov      r8d, 0x29
0020CD61  lea      rdx, [rip + 0x1bf16a8]  ; -> 01DFE410
0020CD68  mov      rcx, rax
0020CD6B  call     0x20c730  ; -> 0020C730 fn
0020CD70  nop      
0020CD71  mov      qword ptr [rip + 0x1d766d8], rax  ; -> 01F83450
0020CD78  add      rsp, 0x38
0020CD7C  ret      
```

## 0020CE10 (78 B, extent 0020CE10-0020CE5E)

Page context: "hievement(entry0)' and     'StoreStats'. - **1103 'UserAchievementStored' ('0020C8C0').** It increments the achieved count. At n−1 it re-reads   entry 0 and, if that is unachieved, awards it through '0020CE10'. - **1102 'UserStatsStored' ('0020CB20').** It only logs success or failure.  ## 7. Invariants (FABLE)  **I-1 — Without Steam, achievements are silently off.** If 'SteamAPI_Init' fails, '[01F83450]' stays null and every by-index a"

```
0020CE10  push     rbx
0020CE12  sub      rsp, 0x20
0020CE16  cmp      byte ptr [rcx + 0x18], 0
0020CE1A  mov      rbx, rdx
0020CE1D  je       0x20ce56  ; -> 0020CE56
0020CE1F  lea      rcx, [rip + 0x1bf12aa]  ; -> 01DFE0D0
0020CE26  call     qword ptr [rip + 0x6b6364]  ; -> 008C3190 [u64 0x0000000001CCBFA6]
0020CE2C  mov      rdx, rbx
0020CE2F  mov      rcx, qword ptr [rax + 0x28]
0020CE33  mov      rax, qword ptr [rcx]
0020CE36  call     qword ptr [rax + 0x38]
0020CE39  lea      rcx, [rip + 0x1bf1290]  ; -> 01DFE0D0
0020CE40  call     qword ptr [rip + 0x6b634a]  ; -> 008C3190 [u64 0x0000000001CCBFA6]
0020CE46  mov      rcx, qword ptr [rax + 0x28]
0020CE4A  mov      rax, qword ptr [rcx]
0020CE4D  add      rsp, 0x20
0020CE51  pop      rbx
0020CE52  jmp      qword ptr [rax + 0x50]
0020CE56  xor      al, al
0020CE58  add      rsp, 0x20
0020CE5C  pop      rbx
0020CE5D  ret      
```
