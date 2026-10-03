# F-interior pack: `18-Audio/the-voice-pack-slots-and-the-voice-verbs.md`

Generated 2026-10-03 02:40 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/the-voice-pack-slots-and-the-voice-verbs.json`.

Functions: 5. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: cd6bd7f58	SWE2-DATA consolidated publish: progress-report cluster (generation store, R3 semantics, DB_GOAL, me; d0fd168a2	SWE2-DATA: batch-5 review corrections (clamping page's .data vf00 cell restored, SD-190 gate on the ). OPUS read these before packing.

## 0034E8B0 (114 B, extent 0034E8B0-0034E922)

Page context: "opies 'table[that]' to '+0x30': bit set → table 0, the 'in' '.vpcjp'; clear → table 1, the language '.vpc'.  ### 2.2 Load — 'voiceread'  'voiceread' ('0085', '0034EE40') and 'voiceread_20a' ('020A', '0034E8B0') pop their arguments and call '003EA0D0(manager, slot, flag)' with the manager taken from the running script's context ('002640C0()' '+0x28'); the verb is a no-op when the calling actor's manager (actor '+0x15') has its '+0x201' b"

```
0034E8B0  mov      qword ptr [rsp + 8], rbx
0034E8B5  mov      qword ptr [rsp + 0x10], rbp
0034E8BA  mov      qword ptr [rsp + 0x18], rsi
0034E8BF  push     rdi
0034E8C0  sub      rsp, 0x20
0034E8C4  mov      rbx, r9
0034E8C7  mov      rdi, rdx
0034E8CA  call     0x2640c0  ; -> 002640C0 fn
0034E8CF  mov      rcx, rbx
0034E8D2  mov      esi, dword ptr [rax + 0x28]
0034E8D5  call     0x267e10  ; -> 00267E10 fn
0034E8DA  mov      rcx, rbx
0034E8DD  mov      ebp, eax
0034E8DF  call     0x267e10  ; -> 00267E10 fn
0034E8E4  movzx    ecx, byte ptr [rdi + 0x15]
0034E8E8  mov      ebx, eax
0034E8EA  call     0x267310  ; -> 00267310 fn
0034E8EF  test     eax, eax
0034E8F1  jne      0x34e90d  ; -> 0034E90D
0034E8F3  mov      r8d, ebp
0034E8F6  mov      edx, ebx
0034E8F8  mov      ecx, esi
0034E8FA  call     0x3ea0d0  ; -> 003EA0D0 fn
0034E8FF  test     eax, eax
0034E901  je       0x34e90d  ; -> 0034E90D
0034E903  mov      ecx, 1
0034E908  call     0x314d40  ; -> 00314D40 fn
0034E90D  mov      rbx, qword ptr [rsp + 0x30]
0034E912  mov      rbp, qword ptr [rsp + 0x38]
0034E917  mov      rsi, qword ptr [rsp + 0x40]
0034E91C  add      rsp, 0x20
0034E920  pop      rdi
0034E921  ret      
```

## 0034EE40 (124 B, extent 0034EE40-0034EEBC)

Page context: " [020BE6E0] + 4 == 0' ('002DDE20'), and copies 'table[that]' to '+0x30': bit set → table 0, the 'in' '.vpcjp'; clear → table 1, the language '.vpc'.  ### 2.2 Load — 'voiceread'  'voiceread' ('0085', '0034EE40') and 'voiceread_20a' ('020A', '0034E8B0') pop their arguments and call '003EA0D0(manager, slot, flag)' with the manager taken from the running script's context ('002640C0()' '+0x28'); the verb is a no-op when the calling actor's m"

```
0034EE40  mov      qword ptr [rsp + 8], rbx
0034EE45  mov      qword ptr [rsp + 0x10], rbp
0034EE4A  mov      qword ptr [rsp + 0x18], rsi
0034EE4F  push     rdi
0034EE50  sub      rsp, 0x20
0034EE54  mov      rdi, rdx
0034EE57  mov      rcx, r9
0034EE5A  xor      edx, edx
0034EE5C  mov      rbx, r9
0034EE5F  call     0x267f90  ; -> 00267F90 fn
0034EE64  call     0x2640c0  ; -> 002640C0 fn
0034EE69  mov      rcx, rbx
0034EE6C  mov      esi, dword ptr [rax + 0x28]
0034EE6F  call     0x267e10  ; -> 00267E10 fn
0034EE74  mov      rcx, rbx
0034EE77  mov      ebp, eax
0034EE79  call     0x267e10  ; -> 00267E10 fn
0034EE7E  movzx    ecx, byte ptr [rdi + 0x15]
0034EE82  mov      ebx, eax
0034EE84  call     0x267310  ; -> 00267310 fn
0034EE89  test     eax, eax
0034EE8B  jne      0x34eea7  ; -> 0034EEA7
0034EE8D  mov      r8d, ebp
0034EE90  mov      edx, ebx
0034EE92  mov      ecx, esi
0034EE94  call     0x3ea0d0  ; -> 003EA0D0 fn
0034EE99  test     eax, eax
0034EE9B  je       0x34eea7  ; -> 0034EEA7
0034EE9D  mov      ecx, 1
0034EEA2  call     0x314d40  ; -> 00314D40 fn
0034EEA7  mov      rbx, qword ptr [rsp + 0x30]
0034EEAC  mov      rbp, qword ptr [rsp + 0x38]
0034EEB1  mov      rsi, qword ptr [rsp + 0x40]
0034EEB6  add      rsp, 0x20
0034EEBA  pop      rdi
0034EEBB  ret      
```

## 003522C0 (91 B, extent 003522C0-0035231B)

Page context: "the world tick, '003140B8'), **1** (the field pass, pack '0xD4', '0025DAE1'), **3** ('BattleAction_InitializeGlobalSpecialSequenceMode' '00306C0A', '00353590', '003CA077'), **'clamp(n + 1, 1, 3)'** ('003522C0', '00353080' — the event-load verbs), or the script's own operand — **only in 'debug_eventload''s poll** (verb '0x202D', '0050D110'–'0050D115'), which is also the only caller of manager 4's unload request '00314410'. The 1,114 deco"

```
003522C0  mov      qword ptr [rsp + 8], rbx
003522C5  push     rdi
003522C6  sub      rsp, 0x20
003522CA  mov      edi, dword ptr [r8 + 4]
003522CE  mov      ebx, dword ptr [r8]
003522D1  call     0x264170  ; -> 00264170 fn
003522D6  test     eax, eax
003522D8  je       0x352310  ; -> 00352310
003522DA  call     0x1c3370  ; -> 001C3370 fn
003522DF  cmp      eax, 1
003522E2  je       0x352310  ; -> 00352310
003522E4  test     ebx, ebx
003522E6  js       0x352310  ; -> 00352310
003522E8  inc      ebx
003522EA  cmp      ebx, 1
003522ED  jge      0x3522f6  ; -> 003522F6
003522EF  mov      ebx, 1
003522F4  jmp      0x352300  ; -> 00352300
003522F6  mov      eax, 3
003522FB  cmp      ebx, eax
003522FD  cmovg    ebx, eax
00352300  mov      edx, edi
00352302  mov      ecx, ebx
00352304  call     0x32fc30  ; -> 0032FC30 fn
00352309  mov      ecx, ebx
0035230B  call     0x32ed70  ; -> 0032ED70 fn
00352310  mov      rbx, qword ptr [rsp + 0x30]
00352315  add      rsp, 0x20
00352319  pop      rdi
0035231A  ret      
```

## 00352DB0 (35 B, extent 00352DB0-00352DD3)

Page context: "'64' dead ahead, '0x80' and above behind - and the 18 shipped calls are on [the sound-request page](Audio-Boundary/how-a-sound-request-becomes-a-voice.md) under UQ-242. - **'voicedispose'** ('008C', '00352DB0' → '003E98B0(slot)'): frees the slot; the manager teardown   ('002628B0', and '00360710') calls '003E9970(manager)', which frees every slot whose '+0' byte is   that manager. - 'voicereadsync', 'voicesync', 'voicestandby', 'voicevo"

```
00352DB0  push     rbx
00352DB2  sub      rsp, 0x20
00352DB6  mov      rcx, r9
00352DB9  call     0x267e10  ; -> 00267E10 fn
00352DBE  mov      ecx, eax
00352DC0  mov      ebx, eax
00352DC2  call     0x3ea330  ; -> 003EA330 fn
00352DC7  mov      ecx, ebx
00352DC9  add      rsp, 0x20
00352DCD  pop      rbx
00352DCE  jmp      0x3e98b0  ; -> 003E98B0 fn
```

## 00353080 (107 B, extent 00353080-003530EB)

Page context: "ck, '003140B8'), **1** (the field pass, pack '0xD4', '0025DAE1'), **3** ('BattleAction_InitializeGlobalSpecialSequenceMode' '00306C0A', '00353590', '003CA077'), **'clamp(n + 1, 1, 3)'** ('003522C0', '00353080' — the event-load verbs), or the script's own operand — **only in 'debug_eventload''s poll** (verb '0x202D', '0050D110'–'0050D115'), which is also the only caller of manager 4's unload request '00314410'. The 1,114 decompiled 'us' "

```
00353080  mov      qword ptr [rsp + 8], rbx
00353085  mov      qword ptr [rsp + 0x10], rsi
0035308A  push     rdi
0035308B  sub      rsp, 0x20
0035308F  mov      edi, 1
00353094  mov      rbx, r8
00353097  mov      ecx, edi
00353099  call     0x314d40  ; -> 00314D40 fn
0035309E  mov      esi, dword ptr [rbx + 4]
003530A1  mov      ebx, dword ptr [rbx]
003530A3  call     0x264170  ; -> 00264170 fn
003530A8  test     eax, eax
003530AA  je       0x3530db  ; -> 003530DB
003530AC  call     0x1c3370  ; -> 001C3370 fn
003530B1  cmp      eax, edi
003530B3  je       0x3530db  ; -> 003530DB
003530B5  test     ebx, ebx
003530B7  js       0x3530db  ; -> 003530DB
003530B9  inc      ebx
003530BB  cmp      ebx, edi
003530BD  jl       0x3530cb  ; -> 003530CB
003530BF  mov      eax, 3
003530C4  mov      edi, ebx
003530C6  cmp      ebx, eax
003530C8  cmovg    edi, eax
003530CB  mov      edx, esi
003530CD  mov      ecx, edi
003530CF  call     0x32fc30  ; -> 0032FC30 fn
003530D4  mov      ecx, edi
003530D6  call     0x32ed70  ; -> 0032ED70 fn
003530DB  mov      rbx, qword ptr [rsp + 0x30]
003530E0  mov      rsi, qword ptr [rsp + 0x38]
003530E5  add      rsp, 0x20
003530E9  pop      rdi
003530EA  ret      
```
