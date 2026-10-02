# F-interior pack: `22-Middleware-PhyreEngine/Application-Framework-Boundary/the-game-is-a-phyre-application.md`

Generated 2026-10-02 09:51 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/the-game-is-a-phyre-application.json`.

Functions: 12. Each is cited on the page only at its entry and is still in the F frontier.

## 00186820 (30 B, extent 00186820-0018683E)

Page context: "1D9C0' ('PSamplerState'). Interior anchor '0018A86D' (the '001DE540' call).  ## SWE2-EC7-39 update (2026-09-19) - '00187550'  '00187550' (395 B) is the '/capture.tga' screenshot writer - '01F44830', '00186820' triple plus '008C2F40'/'008C2EF8'/'008C2F00' thunks and '00210EB0'/'00808C40'. Interior anchor '00187597' (an '008C2EF8' thunk call).  ## SWE2-EC7-40 update (2026-09-19) - '0079E700'  '0079E700' (383 B) is a Phyre desktop body - t"

```
00186820  cmp      byte ptr [rcx + 0xdb8], 0
00186827  mov      eax, 0x870
0018682C  jne      0x18683d  ; -> 0018683D
0018682E  cmp      dword ptr [rcx + 0xc30], 3
00186835  je       0x18683d  ; -> 0018683D
00186837  mov      eax, dword ptr [rcx + 0xadc]
0018683D  ret      
```

## 0020CD30 (77 B, extent 0020CD30-0020CD7D)

Page context: "uns these steps, in order:  1. 'SetUnhandledExceptionFilter', 'ImmDisableIME' and 'CoInitializeEx'. 2. **PlatformOnlineAchievements:** 'SteamInternal_ContextInit', then 'SteamAPI_Init'. It then runs '0020CD30' and    '008655E0' ('SteamAPI_RegisterCallback'), and finally 'SteamAPI_RestartAppIfNecessary', which is followed by 'exit'    when a restart is due ('00798116'–'0079814B'). 3. '007A0810', a thread-safe static accessor for the obje"

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

## 00793750 (54 B, extent 00793750-00793786)

Page context: " possible. Interior anchor '00873C4B' (the flag-strip subtract).  ## SWE2-EC7-114 update (2026-09-21) - '007A3980' / '007A07C0' / '0079ED60' measured  '007A3980' (49 B) is the six-way vtable install '00793750', '007980A0' and '008A56A0' run on a new object: the '01CB3EF8' table (RTTI '01D3EEA8', slot 0 '007A39C0') lands at '+0x38', '+0x58', '+0x78', '+0x90', '+0xB0' and '+0xC8' while 'qword[+0x30]' zeroes - one interface stamped onto si"

```
00793750  push     rbx
00793752  sub      rsp, 0x30
00793756  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0079375F  mov      rbx, rcx
00793762  lea      rax, [rip + 0x151ecff]  ; -> 01CB2468
00793769  mov      qword ptr [rcx], rax
0079376C  add      rcx, 0x20
00793770  call     0x5cd6d0  ; -> 005CD6D0 fn
00793775  nop      
00793776  lea      rcx, [rbx + 0x48]
0079377A  call     0x7a3980  ; -> 007A3980 fn
0079377F  nop      
00793780  add      rsp, 0x30
00793784  pop      rbx
00793785  ret      
```

## 00796E30 (52 B, extent 00796E30-00796E64)

Page context: "amera' '00794CEB', 'getDebugUtils' '00794DB5') + '00632FB0' bind into record cells at '02EAC3A0'–'02EAC460', each record carrying a vtable ('01CB3A28', RTTI '01D3E828') and its handler pointer (e.g. '00796E30' at '007944DA'). **'00794E80' (1,173 B) read the same day (SWE2-FRONTIER): the second of the four, same shape — '006388C0' registration at ['00794EAA'](../../_index/ADDRESS-INDEX.md), '008092FC'/'0080929C'/'00808B90' driver thunks "

```
00796E30  mov      rdx, qword ptr [rip + 0x270e531]  ; -> 02EA5368
00796E37  test     rdx, rdx
00796E3A  je       0x796e52  ; -> 00796E52
00796E3C  mov      rax, qword ptr [rip + 0x17a92dd]  ; -> 01F40120 [u64 0x0000000002EA5660]
00796E43  add      rdx, 8
00796E47  mov      qword ptr [rcx], rdx
00796E4A  mov      qword ptr [rcx + 8], rax
00796E4E  mov      rax, rcx
00796E51  ret      
00796E52  mov      rax, qword ptr [rip + 0x17a92c7]  ; -> 01F40120 [u64 0x0000000002EA5660]
00796E59  mov      qword ptr [rcx], rdx
00796E5C  mov      qword ptr [rcx + 8], rax
00796E60  mov      rax, rcx
00796E63  ret      
```

## 00798F80 (105 B, extent 00798F80-00798FE9)

Page context: " non-client mouse press. On 'WM_NCLBUTTONDOWN' / 'WM_NCRBUTTONDOWN' it is     called with 1, and a thread mouse hook is installed ('SetWindowsHookExW' '008C2858' with id 7, 'WH_MOUSE', procedure     '00798F80'; '007995A7'–'007995EC'). On 'WM_NCLBUTTONUP' / 'WM_NCRBUTTONUP' it is called with 0 and the hook removed     ('UnhookWindowsHookEx' '008C2850'; '007995F8'–'0079962D');   - **slot 20** (inherited '007A0FB0') on 'WM_MOVE', with no a"

```
00798F80  mov      qword ptr [rsp + 8], rbx
00798F85  mov      qword ptr [rsp + 0x10], rsi
00798F8A  push     rdi
00798F8B  sub      rsp, 0x20
00798F8F  mov      rsi, r8
00798F92  mov      rbx, rdx
00798F95  mov      edi, ecx
00798F97  test     ecx, ecx
00798F99  jne      0x798fc4  ; -> 00798FC4
00798F9B  cmp      rdx, 0x202
00798FA2  jne      0x798fc4  ; -> 00798FC4
00798FA4  cmp      byte ptr [rip + 0x270c29a], cl  ; -> 02EA5244
00798FAA  je       0x798fc4  ; -> 00798FC4
00798FAC  mov      rcx, qword ptr [rip + 0x270c295]  ; -> 02EA5248
00798FB3  xor      r9d, r9d
00798FB6  xor      r8d, r8d
00798FB9  mov      edx, 0xa2
00798FBE  call     qword ptr [rip + 0x12985c]  ; -> 008C2820 [u64 0x0000000001CCC7CE]
00798FC4  mov      rcx, qword ptr [rip + 0x270c28d]  ; -> 02EA5258
00798FCB  mov      r9, rsi
00798FCE  mov      r8, rbx
00798FD1  mov      edx, edi
00798FD3  mov      rbx, qword ptr [rsp + 0x30]
00798FD8  mov      rsi, qword ptr [rsp + 0x38]
00798FDD  add      rsp, 0x20
00798FE1  pop      rdi
00798FE2  jmp      qword ptr [rip + 0x12985f]  ; -> 008C2848 [u64 0x0000000001CCCB94]
```

## 0079F140 (10 B, extent 0079F140-0079F14A)

Page context: "   (Phyre: 007A05D0) slot 10  OVERRIDDEN  0017D120                              (Phyre: 005C5230 stub) slot 11  inherited   005C5230   empty virtual slot 12  inherited   007A0B10 slot 13  inherited   0079F140 slot 14  OVERRIDDEN  0017D160   thunk                      (Phyre: 007A0B40) slot 15  OVERRIDDEN  0017D1A0                              (Phyre: 005C5230 stub) slot 16  OVERRIDDEN  0017D210                              (Phyre: 005C5"

```
0079F140  mov      byte ptr [rcx + 0x21], 1
0079F144  xor      eax, eax
0079F146  mov      byte ptr [rcx + 0x26], dl
0079F149  ret      
```

## 0079F9E0 (31 B, extent 0079F9E0-0079F9FF)

Page context: "by slot 2 at mount time |  ## 4. Data structures and formulas  ### The complete 31-slot boundary  ''' slot  0  OVERRIDDEN  0017CC70   deleting destructor        (Phyre: 00793EB0) slot  1  inherited   0079F9E0 slot  2  OVERRIDDEN  0017CEB0   content root + VBF mount   (Phyre: 005C5230 stub) slot  3  OVERRIDDEN  0017CF30   device/viewport setup      (Phyre: 005C5230 stub) slot  4  OVERRIDDEN  0017CCD0   FRAME TICK                 (Phyre: "

```
0079F9E0  sub      rsp, 0x28
0079F9E4  call     0x7943e0  ; -> 007943E0 fn
0079F9E9  call     0x794e80  ; -> 00794E80 fn
0079F9EE  call     0x795590  ; -> 00795590 fn
0079F9F3  call     0x795320  ; -> 00795320 fn
0079F9F8  xor      eax, eax
0079F9FA  add      rsp, 0x28
0079F9FE  ret      
```

## 007A0AF0 (17 B, extent 007A0AF0-007A0B01)

Page context: "              (Phyre: 005C5230 stub) slot 16  OVERRIDDEN  0017D210                              (Phyre: 005C5230 stub) slot 17  inherited   007A0B30 slot 18  inherited   007A1180 slot 19  inherited   007A0AF0 slot 20  inherited   007A0FB0 slot 21  OVERRIDDEN  0017CFD0                              (Phyre: 00657140) slot 22  OVERRIDDEN  0017D170                              (Phyre: 0016D6A0 empty) slot 23  OVERRIDDEN  0017CDF0            "

```
007A0AF0  xor      eax, eax
007A0AF2  cmp      byte ptr [rcx + 0x23], al
007A0AF5  jne      0x7a0afc  ; -> 007A0AFC
007A0AF7  mov      byte ptr [rcx + 0x22], 1
007A0AFB  ret      
007A0AFC  mov      byte ptr [rcx + 0x23], 0
007A0B00  ret      
```

## 007A0B10 (17 B, extent 007A0B10-007A0B21)

Page context: "0C0                              (Phyre: 007A05D0) slot 10  OVERRIDDEN  0017D120                              (Phyre: 005C5230 stub) slot 11  inherited   005C5230   empty virtual slot 12  inherited   007A0B10 slot 13  inherited   0079F140 slot 14  OVERRIDDEN  0017D160   thunk                      (Phyre: 007A0B40) slot 15  OVERRIDDEN  0017D1A0                              (Phyre: 005C5230 stub) slot 16  OVERRIDDEN  0017D210             "

```
007A0B10  mov      byte ptr [rcx + 0x20], 1
007A0B14  xor      eax, eax
007A0B16  mov      byte ptr [rcx + 0x1e], 1
007A0B1A  mov      byte ptr [rcx + 0xd20], dl
007A0B20  ret      
```

## 007A0B30 (6 B, extent 007A0B30-007A0B36)

Page context: "yre: 007A0B40) slot 15  OVERRIDDEN  0017D1A0                              (Phyre: 005C5230 stub) slot 16  OVERRIDDEN  0017D210                              (Phyre: 005C5230 stub) slot 17  inherited   007A0B30 slot 18  inherited   007A1180 slot 19  inherited   007A0AF0 slot 20  inherited   007A0FB0 slot 21  OVERRIDDEN  0017CFD0                              (Phyre: 00657140) slot 22  OVERRIDDEN  0017D170                              (Phyr"

```
007A0B30  mov      byte ptr [rcx + 0x28], dl
007A0B33  xor      eax, eax
007A0B35  ret      
```

## 007A0FB0 (7 B, extent 007A0FB0-007A0FB7)

Page context: " stub) slot 16  OVERRIDDEN  0017D210                              (Phyre: 005C5230 stub) slot 17  inherited   007A0B30 slot 18  inherited   007A1180 slot 19  inherited   007A0AF0 slot 20  inherited   007A0FB0 slot 21  OVERRIDDEN  0017CFD0                              (Phyre: 00657140) slot 22  OVERRIDDEN  0017D170                              (Phyre: 0016D6A0 empty) slot 23  OVERRIDDEN  0017CDF0                              (Phyre: 0079"

```
007A0FB0  mov      byte ptr [rcx + 0x24], 1
007A0FB4  xor      eax, eax
007A0FB6  ret      
```

## 007A1180 (14 B, extent 007A1180-007A118E)

Page context: "DDEN  0017D1A0                              (Phyre: 005C5230 stub) slot 16  OVERRIDDEN  0017D210                              (Phyre: 005C5230 stub) slot 17  inherited   007A0B30 slot 18  inherited   007A1180 slot 19  inherited   007A0AF0 slot 20  inherited   007A0FB0 slot 21  OVERRIDDEN  0017CFD0                              (Phyre: 00657140) slot 22  OVERRIDDEN  0017D170                              (Phyre: 0016D6A0 empty) slot 23  OV"

```
007A1180  mov      byte ptr [rcx + 0x29], 1
007A1184  xor      eax, eax
007A1186  mov      dword ptr [rcx + 0x2c], edx
007A1189  mov      dword ptr [rcx + 0x30], r8d
007A118D  ret      
```
