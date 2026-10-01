# F-interior pack: `18-Audio/Audio-Bank-And-Controller-Family/audio-bank-and-controller-family.md`

Generated 2026-10-01 15:28 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/audio-bank-and-controller-family.json`.

Functions: 23. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (inbox mentions: repos-78.md, repos-d2.md). OPUS read these before packing.

## 001DC130 (84 B, extent 001DC130-001DC184)

Page context: " the 'us' bank from slot '0x21' into handle '+0xC', then           the 'jp' bank from slot '0x27' into '+0x10'.         - Each completion callback ('0036EAB0', '0036E9F0') hands the loaded buffer to '001DC130'. That wrapper takes           the audio registry's '+0x20' object, the 'ShoutAudioController' (constructor '0021BDB0', vtable           '00907FF0'), and enters its intake '0021C680'. The intake reuses the bank whose '+0x3C' matche"

```
001DC130  mov      qword ptr [rsp + 8], rbx
001DC135  mov      qword ptr [rsp + 0x10], rbp
001DC13A  mov      qword ptr [rsp + 0x18], rsi
001DC13F  push     rdi
001DC140  sub      rsp, 0x30
001DC144  mov      ebx, r9d
001DC147  mov      rdi, r8
001DC14A  mov      esi, edx
001DC14C  mov      ebp, ecx
001DC14E  call     0x210b30  ; -> 00210B30 fn
001DC153  mov      rcx, rax
001DC156  mov      r9, rdi
001DC159  mov      eax, dword ptr [rsp + 0x60]
001DC15D  mov      r8d, esi
001DC160  mov      dword ptr [rsp + 0x28], eax
001DC164  mov      edx, ebp
001DC166  mov      dword ptr [rsp + 0x20], ebx
001DC16A  call     0x2111f0  ; -> 002111F0 fn
001DC16F  mov      rbx, qword ptr [rsp + 0x40]
001DC174  mov      rbp, qword ptr [rsp + 0x48]
001DC179  mov      rsi, qword ptr [rsp + 0x50]
001DC17E  add      rsp, 0x30
001DC182  pop      rdi
001DC183  ret      
```

## 001DC2E0 (78 B, extent 001DC2E0-001DC32E)

Page context: "e same as the controller's six-bank pool (a numeric agreement;           no code ties the two).       - **'StreamAudioController' takes the event and map voice packs and the BGM stream.** Its intake '001DC2E0'         enters registry '+0x18', the 'StreamAudioController' (constructor '0021CC10', vtable '00908200'), at         '0021D770'. The stream wrapper in front of it has three callers:         - the voice-pack cue start '003E9C10', w"

```
001DC2E0  mov      qword ptr [rsp + 8], rbx
001DC2E5  mov      qword ptr [rsp + 0x10], rbp
001DC2EA  mov      qword ptr [rsp + 0x18], rsi
001DC2EF  push     rdi
001DC2F0  sub      rsp, 0x30
001DC2F4  mov      ebx, r9d
001DC2F7  mov      rdi, r8
001DC2FA  mov      esi, edx
001DC2FC  mov      rbp, rcx
001DC2FF  call     0x210b30  ; -> 00210B30 fn
001DC304  mov      rcx, rax
001DC307  mov      dword ptr [rsp + 0x20], ebx
001DC30B  mov      r9, rdi
001DC30E  mov      r8d, esi
001DC311  mov      rdx, rbp
001DC314  call     0x211270  ; -> 00211270 fn
001DC319  mov      rbx, qword ptr [rsp + 0x40]
001DC31E  mov      rbp, qword ptr [rsp + 0x48]
001DC323  mov      rsi, qword ptr [rsp + 0x50]
001DC328  add      rsp, 0x30
001DC32C  pop      rdi
001DC32D  ret      
```

## 00219970 (77 B, extent 00219970-002199BD)

Page context: "h the '00225690' accessor + '/1000' quotient test on the rdx entry). |  **AudioController:**  | slot | what it is | |---|---| | 0 | scalar deleting destructors (§3 size table). | | 1 | **Sep only** ('00219970'): walk '+0x8' entries and '00223300(node, -1, 0)' every node whose '+0x49' matches the arg byte — a selective entry stop/reset. No other controller overrides it (RTTI matrix). | | 2 | all classes '0021B0D0': walk '+0x8', call each"

```
00219970  mov      qword ptr [rsp + 8], rbx
00219975  mov      qword ptr [rsp + 0x10], rsi
0021997A  push     rdi
0021997B  sub      rsp, 0x20
0021997F  mov      rbx, qword ptr [rcx + 8]
00219983  lea      rdi, [rcx + 8]
00219987  mov      esi, edx
00219989  cmp      rbx, rdi
0021998C  je       0x2199ad  ; -> 002199AD
0021998E  nop      
00219990  mov      rcx, qword ptr [rbx + 0x10]
00219994  test     byte ptr [rcx + 0x49], sil
00219998  je       0x2199a5  ; -> 002199A5
0021999A  xor      r8d, r8d
0021999D  or       edx, 0xffffffff
002199A0  call     0x223300  ; -> 00223300 fn
002199A5  mov      rbx, qword ptr [rbx]
002199A8  cmp      rbx, rdi
002199AB  jne      0x219990  ; -> 00219990
002199AD  mov      rbx, qword ptr [rsp + 0x30]
002199B2  mov      rsi, qword ptr [rsp + 0x38]
002199B7  add      rsp, 0x20
002199BB  pop      rdi
002199BC  ret      
```

## 00219C40 (90 B, extent 00219C40-00219C9A)

Page context: " (the red-black erase: transplant, colour swap at '+0x18', rotations '0016D780' / '0016D7E0'; corrected 2026-09-15, 'OPUS-CONTRA-AUDIO-UNLINK-IS-A-READ') + a release via '[+0x88]' vtable slot 3. Sep '00219C40' logs first ('005CD4F0') then erases; Seb '0021B290' erases then calls '00222170'. | | 4 | '00212860' walks '+0x8' and runs '00221FB0' on each node with '+0x2C == 0' and '+0x30 == 0' — idle-entry housekeeping; Stream has its own '0"

```
00219C40  mov      qword ptr [rsp + 8], rbx
00219C45  mov      qword ptr [rsp + 0x10], rsi
00219C4A  push     rdi
00219C4B  sub      rsp, 0x20
00219C4F  mov      rsi, rcx
00219C52  mov      rbx, rdx
00219C55  add      rcx, 0xb8
00219C5C  call     0x5cd4f0  ; -> 005CD4F0 fn
00219C61  sub      dword ptr [rbx + 0x58], 1
00219C65  mov      eax, dword ptr [rbx + 0x58]
00219C68  jne      0x219c7f  ; -> 00219C7F
00219C6A  mov      rax, qword ptr [rbx]
00219C6D  mov      rcx, rbx
00219C70  call     qword ptr [rax + 0x10]
00219C73  lea      rcx, [rsi + 0x20]
00219C77  mov      rdx, rbx
00219C7A  call     0x219d80  ; -> 00219D80 fn
00219C7F  lea      rcx, [rsi + 0xb8]
00219C86  mov      rbx, qword ptr [rsp + 0x30]
00219C8B  mov      rsi, qword ptr [rsp + 0x38]
00219C90  add      rsp, 0x20
00219C94  pop      rdi
00219C95  jmp      0x5cd820  ; -> 005CD820 fn
```

## 0021B290 (96 B, extent 0021B290-0021B2F0)

Page context: "0x18', rotations '0016D780' / '0016D7E0'; corrected 2026-09-15, 'OPUS-CONTRA-AUDIO-UNLINK-IS-A-READ') + a release via '[+0x88]' vtable slot 3. Sep '00219C40' logs first ('005CD4F0') then erases; Seb '0021B290' erases then calls '00222170'. | | 4 | '00212860' walks '+0x8' and runs '00221FB0' on each node with '+0x2C == 0' and '+0x30 == 0' — idle-entry housekeeping; Stream has its own '0021D4E0' (137 B): counts the '+0x8' list and fires o"

```
0021B290  mov      qword ptr [rsp + 8], rbx
0021B295  mov      qword ptr [rsp + 0x10], rsi
0021B29A  push     rdi
0021B29B  sub      rsp, 0x20
0021B29F  mov      rsi, rcx
0021B2A2  mov      rbx, rdx
0021B2A5  add      rcx, 0xb8
0021B2AC  call     0x5cd4f0  ; -> 005CD4F0 fn
0021B2B1  sub      dword ptr [rbx + 0x90], 1
0021B2B8  mov      eax, dword ptr [rbx + 0x90]
0021B2BE  jne      0x21b2d5  ; -> 0021B2D5
0021B2C0  mov      rax, qword ptr [rbx]
0021B2C3  mov      rcx, rbx
0021B2C6  call     qword ptr [rax + 0x10]
0021B2C9  lea      rcx, [rsi + 0x20]
0021B2CD  mov      rdx, rbx
0021B2D0  call     0x219d80  ; -> 00219D80 fn
0021B2D5  lea      rcx, [rsi + 0xb8]
0021B2DC  mov      rbx, qword ptr [rsp + 0x30]
0021B2E1  mov      rsi, qword ptr [rsp + 0x38]
0021B2E6  add      rsp, 0x20
0021B2EA  pop      rdi
0021B2EB  jmp      0x5cd820  ; -> 005CD820 fn
```

## 0021C3D0 (101 B, extent 0021C3D0-0021C435)

Page context: "turns nothing, call slot 4 and retry the drain ('0021893B'–'0021894D'); then tail-dispatches the popped request through own 'vtable[+0x28]' = **slot 5** ('00218966', 'rdx' = the popped entry). Shout '0021C3D0' same shape; Stream '0021D3D0' does the identical sequence directly on '+0x20' through '0021D280' — consistent with Stream's missing slot 7. | | 7 | the '+0x20' request-queue drain — the adjustor/'161 B'-body family of §2, fully re"

```
0021C3D0  mov      qword ptr [rsp + 8], rbx
0021C3D5  push     rdi
0021C3D6  sub      rsp, 0x20
0021C3DA  mov      rax, qword ptr [rcx]
0021C3DD  mov      rdi, rcx
0021C3E0  call     qword ptr [rax + 0x38]
0021C3E3  xor      ecx, ecx
0021C3E5  mov      rbx, rax
0021C3E8  mov      edx, dword ptr [rax + 0x30]
0021C3EB  test     edx, edx
0021C3ED  sete     cl
0021C3F0  call     0x16d6a0  ; -> 0016D6A0 fn
0021C3F5  xor      ecx, ecx
0021C3F7  test     rbx, rbx
0021C3FA  setne    cl
0021C3FD  call     0x16d6a0  ; -> 0016D6A0 fn
0021C402  test     rbx, rbx
0021C405  jne      0x21c41b  ; -> 0021C41B
0021C407  mov      dword ptr [0], ebx
0021C40E  xor      eax, eax
0021C410  mov      rbx, qword ptr [rsp + 0x30]
0021C415  add      rsp, 0x20
0021C419  pop      rdi
0021C41A  ret      
0021C41B  mov      rax, qword ptr [rdi]
0021C41E  mov      rdx, rbx
0021C421  mov      rcx, rdi
0021C424  call     qword ptr [rax + 0x28]
0021C427  mov      rax, rbx
0021C42A  mov      rbx, qword ptr [rsp + 0x30]
0021C42F  add      rsp, 0x20
0021C433  pop      rdi
0021C434  ret      
```

## 0021C680 (214 B, extent 0021C680-0021C756)

Page context: "loaded buffer to '001DC130'. That wrapper takes           the audio registry's '+0x20' object, the 'ShoutAudioController' (constructor '0021BDB0', vtable           '00907FF0'), and enters its intake '0021C680'. The intake reuses the bank whose '+0x3C' matches the id,           or pops a free one, under a kind-8 handle.         - The voice-pack tables hold 2 + 4 entries, the same as the controller's six-bank pool (a numeric agreement;   "

```
0021C680  mov      qword ptr [rsp + 0x10], rbx
0021C685  mov      qword ptr [rsp + 0x18], rbp
0021C68A  push     rsi
0021C68B  push     rdi
0021C68C  push     r12
0021C68E  push     r14
0021C690  push     r15
0021C692  sub      rsp, 0x40
0021C696  mov      rbx, qword ptr [rcx + 8]
0021C69A  lea      rdi, [rcx + 8]
0021C69E  mov      r15, r9
0021C6A1  mov      r12d, r8d
0021C6A4  mov      esi, edx
0021C6A6  mov      r14, rcx
0021C6A9  cmp      rbx, rdi
0021C6AC  je       0x21c6c1  ; -> 0021C6C1
0021C6AE  nop      
0021C6B0  mov      rax, qword ptr [rbx + 0x10]
0021C6B4  cmp      dword ptr [rax + 0x3c], esi
0021C6B7  je       0x21c6c1  ; -> 0021C6C1
0021C6B9  mov      rbx, qword ptr [rbx]
0021C6BC  cmp      rbx, rdi
0021C6BF  jne      0x21c6b0  ; -> 0021C6B0
0021C6C1  mov      edx, 8
0021C6C6  lea      rcx, [rsp + 0x70]
0021C6CB  call     0x2129f0  ; -> 002129F0 fn
0021C6D0  cmp      dword ptr [rsp + 0x70], 0
0021C6D5  mov      ebp, eax
0021C6D7  jle      0x21c731  ; -> 0021C731
0021C6D9  test     r15, r15
0021C6DC  je       0x21c731  ; -> 0021C731
0021C6DE  cmp      rbx, rdi
0021C6E1  je       0x21c6f4  ; -> 0021C6F4
0021C6E3  mov      rbx, qword ptr [rbx + 0x10]
0021C6E7  or       edx, 0xffffffff
0021C6EA  mov      rcx, rbx
0021C6ED  call     0x225030  ; -> 00225030 fn
0021C6F2  jmp      0x21c700  ; -> 0021C700
0021C6F4  mov      rax, qword ptr [r14]
0021C6F7  mov      rcx, r14
0021C6FA  call     qword ptr [rax + 0x30]
0021C6FD  mov      rbx, rax
0021C700  test     rbx, rbx
0021C703  je       0x21c731  ; -> 0021C731
0021C705  mov      eax, dword ptr [rsp + 0x98]
0021C70C  mov      r9, r15
0021C70F  mov      dword ptr [rsp + 0x30], ebp
0021C713  mov      r8d, r12d
0021C716  mov      dword ptr [rsp + 0x28], eax
0021C71A  mov      edx, esi
0021C71C  mov      eax, dword ptr [rsp + 0x90]
0021C723  mov      rcx, rbx
0021C726  mov      dword ptr [rsp + 0x20], eax
0021C72A  call     0x224dc0  ; -> 00224DC0 fn
0021C72F  jmp      0x21c738  ; -> 0021C738
0021C731  mov      ecx, ebp
0021C733  call     0x212a70  ; -> 00212A70 fn
0021C738  mov      eax, dword ptr [rsp + 0x70]
0021C73C  mov      rbx, qword ptr [rsp + 0x78]
0021C741  mov      rbp, qword ptr [rsp + 0x80]
0021C749  add      rsp, 0x40
0021C74D  pop      r15
0021C74F  pop      r14
0021C751  pop      r12
0021C753  pop      rdi
0021C754  pop      rsi
0021C755  ret      
```

## 0021D3D0 (100 B, extent 0021D3D0-0021D434)

Page context: " retry the drain ('0021893B'–'0021894D'); then tail-dispatches the popped request through own 'vtable[+0x28]' = **slot 5** ('00218966', 'rdx' = the popped entry). Shout '0021C3D0' same shape; Stream '0021D3D0' does the identical sequence directly on '+0x20' through '0021D280' — consistent with Stream's missing slot 7. | | 7 | the '+0x20' request-queue drain — the adjustor/'161 B'-body family of §2, fully read under BD-4 below. |  The +0"

```
0021D3D0  mov      qword ptr [rsp + 8], rbx
0021D3D5  mov      qword ptr [rsp + 0x10], rsi
0021D3DA  push     rdi
0021D3DB  sub      rsp, 0x20
0021D3DF  mov      rbx, rcx
0021D3E2  add      rcx, 0x20
0021D3E6  call     0x21d280  ; -> 0021D280 fn
0021D3EB  mov      rdi, rax
0021D3EE  test     rax, rax
0021D3F1  jne      0x21d408  ; -> 0021D408
0021D3F3  mov      rax, qword ptr [rbx]
0021D3F6  mov      rcx, rbx
0021D3F9  call     qword ptr [rax + 0x20]
0021D3FC  lea      rcx, [rbx + 0x20]
0021D400  call     0x21d280  ; -> 0021D280 fn
0021D405  mov      rdi, rax
0021D408  xor      ecx, ecx
0021D40A  test     rdi, rdi
0021D40D  setne    cl
0021D410  call     0x16d6a0  ; -> 0016D6A0 fn
0021D415  mov      rax, qword ptr [rbx]
0021D418  mov      rdx, rdi
0021D41B  mov      rcx, rbx
0021D41E  call     qword ptr [rax + 0x28]
0021D421  mov      rbx, qword ptr [rsp + 0x30]
0021D426  mov      rax, rdi
0021D429  mov      rsi, qword ptr [rsp + 0x38]
0021D42E  add      rsp, 0x20
0021D432  pop      rdi
0021D433  ret      
```

## 00220C70 (82 B, extent 00220C70-00220CC2)

Page context: "1 update (2026-09-19) - '00222740'  '00222740' (345 B) is the '.win.mab' bank-path builder the page names - '00908930'/'00908940'/'01E027D8'/'01F44830', '"%s%03d%s"'/'".win.mab"' strings, '00221710'/'00220C70'/'0016D6A0' pair/'00861EC0'/'0017D2E0'/'00225C40'/'00221D10'. Interior anchor '00222771' (a '00221710' call).  ## SWE2-EC7-43 update (2026-09-19) - '002238F0'  '002238F0' (292 B) is the 'SebAudioBank' slot-6 row body - '009089BC', "

```
00220C70  push     rdi
00220C72  sub      rsp, 0x30
00220C76  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
00220C7F  mov      qword ptr [rsp + 0x48], rbx
00220C84  mov      rbx, rcx
00220C87  lea      rdi, [rcx + 0x378]
00220C8E  mov      qword ptr [rsp + 0x40], rdi
00220C93  mov      rcx, rdi
00220C96  call     0x5cd4f0  ; -> 005CD4F0 fn
00220C9B  nop      
00220C9C  lea      rcx, [rbx + 0x268]
00220CA3  call     0x2206b0  ; -> 002206B0 fn
00220CA8  mov      rbx, rax
00220CAB  mov      rcx, rdi
00220CAE  call     0x5cd820  ; -> 005CD820 fn
00220CB3  nop      
00220CB4  mov      rax, rbx
00220CB7  mov      rbx, qword ptr [rsp + 0x48]
00220CBC  add      rsp, 0x30
00220CC0  pop      rdi
00220CC1  ret      
```

## 002224F0 (86 B, extent 002224F0-00222546)

Page context: "" is confirmed**: same body, the differing bytes are the constant/field used per slot. | | 6 | base '00657140' = 'ret 0'. Sep '00222D30': get entry '00221E60', require state 1 + '+0x49 & 0x40', then '002224F0' when arg equals '[+0x38]' else '002225B0' (both with '0x120'). Seb '002238F0' (292 B) runs the same predicate family plus driver '007A84A0'. | | 7 | scalar deleting destructors — the 52 B 'free'-calling bodies §2 already proves. |"

```
002224F0  mov      qword ptr [rsp + 8], rbx
002224F5  mov      qword ptr [rsp + 0x10], rbp
002224FA  mov      qword ptr [rsp + 0x18], rsi
002224FF  push     rdi
00222500  sub      rsp, 0x20
00222504  mov      rbx, qword ptr [rcx + 8]
00222508  lea      rdi, [rcx + 8]
0022250C  mov      esi, r8d
0022250F  mov      ebp, edx
00222511  cmp      rbx, rdi
00222514  je       0x222531  ; -> 00222531
00222516  mov      rcx, qword ptr [rbx + 0x10]
0022251A  test     rcx, rcx
0022251D  je       0x222529  ; -> 00222529
0022251F  mov      r8d, esi
00222522  mov      edx, ebp
00222524  call     0x2257e0  ; -> 002257E0 fn
00222529  mov      rbx, qword ptr [rbx]
0022252C  cmp      rbx, rdi
0022252F  jne      0x222516  ; -> 00222516
00222531  mov      rbx, qword ptr [rsp + 0x30]
00222536  mov      rbp, qword ptr [rsp + 0x38]
0022253B  mov      rsi, qword ptr [rsp + 0x40]
00222540  add      rsp, 0x20
00222544  pop      rdi
00222545  ret      
```

## 00222C70 (62 B, extent 00222C70-00222CAE)

Page context: "en a result-switch — arg≠0 and result−1 ≤ 1 tail-jumps '007A8590' ('00222C3C'), arg==0 and result==3 calls '007A7A20' ('00222C41'). It never calls '00210B30'/'00210930' — those are Music **slot 10** '00222C70''s first two calls. | | 1, 3, 4, 5, 8 | **empty in the base** ('ret 0'); only Seb/Sep implement them — they are the sound-effect machinery. Sep slot 1 '00223490' and Seb '00224A30' are driver-backed entry ops ('007A7010'/'007A84A0'"

```
00222C70  push     rbx
00222C72  sub      rsp, 0x20
00222C76  mov      rbx, rcx
00222C79  call     0x210b30  ; -> 00210B30 fn
00222C7E  mov      rcx, rax
00222C81  call     0x210930  ; -> 00210930 fn
00222C86  test     eax, eax
00222C88  je       0x222ca8  ; -> 00222CA8
00222C8A  call     0x210b30  ; -> 00210B30 fn
00222C8F  test     byte ptr [rax + 0x3c], 1
00222C93  je       0x222ca8  ; -> 00222CA8
00222C95  mov      rax, qword ptr [rbx]
00222C98  mov      edx, 1
00222C9D  mov      rcx, rbx
00222CA0  add      rsp, 0x20
00222CA4  pop      rbx
00222CA5  jmp      qword ptr [rax]
00222CA8  add      rsp, 0x20
00222CAC  pop      rbx
00222CAD  ret      
```

## 00222FE0 (72 B, extent 00222FE0-00223028)

Page context: "20]+8' through '007A88F0'. Music '00222BD0' calls '007A84A0' on 'this+0x38' (43 B) then **tail-jumps the base '00222000'** ('00222BF6') — the driver call plus the full teardown, not driver-only; Sep '00222FE0', Seb '00223E60', Shout '00224D40' route their cleanup through '002255B0' + '00809950'. | | 3, 4, 5 | **Sep: three id-range-gated re-dispatches to slot 0.** '00223100' fires when ~~'[+0x38] ≥ 151000' ('0x249F0 + 0x3E8')~~ '[+0x38]'"

```
00222FE0  push     rbx
00222FE2  sub      rsp, 0x20
00222FE6  mov      rbx, rcx
00222FE9  mov      rcx, qword ptr [rcx + 0x20]
00222FED  test     rcx, rcx
00222FF0  je       0x223005  ; -> 00223005
00222FF2  mov      rdx, qword ptr [rbx + 0x50]
00222FF6  test     rdx, rdx
00222FF9  je       0x223005  ; -> 00223005
00222FFB  xor      r8d, r8d
00222FFE  call     0x2255b0  ; -> 002255B0 fn
00223003  jmp      0x223013  ; -> 00223013
00223005  mov      rcx, qword ptr [rbx + 0x50]
00223009  test     rcx, rcx
0022300C  je       0x22301b  ; -> 0022301B
0022300E  call     0x809950  ; -> 00809950 fn
00223013  mov      qword ptr [rbx + 0x50], 0
0022301B  mov      rcx, rbx
0022301E  add      rsp, 0x20
00223022  pop      rbx
00223023  jmp      0x222000  ; -> 00222000 fn
```

## 002230D0 (35 B, extent 002230D0-002230F3)

Page context: " 0x3E8', so ids below 150000 pass as well as ids from 151000 up (*corrected 2026-09-26, FABLE; 's41-opus-replay-bank-family' AC-7 case*). It also needs '+0x50' set and '+0x49 & 0x68 == 0, & 1 == 1'; '002230D0' is the same gate with mask '0x69'; '00223130' fires when '[+0x38]' lies **in** '[0x249F0, 0x249F0+999]', '+0x50 != 0' and '+0x49 & 1 == 0' — ~~the six-digit id space splits at 150999/151000~~ one 1000-id band, 150000–150999, is tr"

```
002230D0  mov      eax, dword ptr [rcx + 0x38]
002230D3  sub      eax, 0x249f0
002230D8  cmp      eax, 0x3e8
002230DD  jb       0x2230f2  ; -> 002230F2
002230DF  cmp      qword ptr [rcx + 0x50], 0
002230E4  je       0x2230f2  ; -> 002230F2
002230E6  test     byte ptr [rcx + 0x49], 0x69
002230EA  jne      0x2230f2  ; -> 002230F2
002230EC  mov      rax, qword ptr [rcx]
002230EF  jmp      qword ptr [rax]
002230F2  ret      
```

## 00223100 (41 B, extent 00223100-00223129)

Page context: " teardown, not driver-only; Sep '00222FE0', Seb '00223E60', Shout '00224D40' route their cleanup through '002255B0' + '00809950'. | | 3, 4, 5 | **Sep: three id-range-gated re-dispatches to slot 0.** '00223100' fires when ~~'[+0x38] ≥ 151000' ('0x249F0 + 0x3E8')~~ '[+0x38]' lies **outside** '[0x249F0, 0x249F0+999]': it computes '[+0x38] − 0x249F0' and returns on an unsigned '< 0x3E8', so ids below 150000 pass as well as ids from 151000 u"

```
00223100  mov      eax, dword ptr [rcx + 0x38]
00223103  sub      eax, 0x249f0
00223108  cmp      eax, 0x3e8
0022310D  jb       0x223128  ; -> 00223128
0022310F  cmp      qword ptr [rcx + 0x50], 0
00223114  je       0x223128  ; -> 00223128
00223116  movzx    eax, byte ptr [rcx + 0x49]
0022311A  test     al, 0x68
0022311C  jne      0x223128  ; -> 00223128
0022311E  test     al, 1
00223120  je       0x223128  ; -> 00223128
00223122  mov      rax, qword ptr [rcx]
00223125  jmp      qword ptr [rax]
00223128  ret      
```

## 00223130 (35 B, extent 00223130-00223153)

Page context: "ds from 151000 up (*corrected 2026-09-26, FABLE; 's41-opus-replay-bank-family' AC-7 case*). It also needs '+0x50' set and '+0x49 & 0x68 == 0, & 1 == 1'; '002230D0' is the same gate with mask '0x69'; '00223130' fires when '[+0x38]' lies **in** '[0x249F0, 0x249F0+999]', '+0x50 != 0' and '+0x49 & 1 == 0' — ~~the six-digit id space splits at 150999/151000~~ one 1000-id band, 150000–150999, is treated apart (slots 3/4 skip it, slot 5 acts on"

```
00223130  mov      eax, dword ptr [rcx + 0x38]
00223133  sub      eax, 0x249f0
00223138  cmp      eax, 0x3e8
0022313D  jae      0x223152  ; -> 00223152
0022313F  cmp      qword ptr [rcx + 0x50], 0
00223144  je       0x223152  ; -> 00223152
00223146  test     byte ptr [rcx + 0x49], 1
0022314A  jne      0x223152  ; -> 00223152
0022314C  mov      rax, qword ptr [rcx]
0022314F  jmp      qword ptr [rax]
00223152  ret      
```

## 00223E60 (80 B, extent 00223E60-00223EB0)

Page context: "007A88F0'. Music '00222BD0' calls '007A84A0' on 'this+0x38' (43 B) then **tail-jumps the base '00222000'** ('00222BF6') — the driver call plus the full teardown, not driver-only; Sep '00222FE0', Seb '00223E60', Shout '00224D40' route their cleanup through '002255B0' + '00809950'. | | 3, 4, 5 | **Sep: three id-range-gated re-dispatches to slot 0.** '00223100' fires when ~~'[+0x38] ≥ 151000' ('0x249F0 + 0x3E8')~~ '[+0x38]' lies **outside*"

```
00223E60  push     rbx
00223E62  sub      rsp, 0x20
00223E66  mov      rbx, rcx
00223E69  mov      rcx, qword ptr [rcx + 0x20]
00223E6D  test     rcx, rcx
00223E70  je       0x223e85  ; -> 00223E85
00223E72  mov      rdx, qword ptr [rbx + 0x50]
00223E76  test     rdx, rdx
00223E79  je       0x223e85  ; -> 00223E85
00223E7B  xor      r8d, r8d
00223E7E  call     0x2255b0  ; -> 002255B0 fn
00223E83  jmp      0x223e93  ; -> 00223E93
00223E85  mov      rcx, qword ptr [rbx + 0x50]
00223E89  test     rcx, rcx
00223E8C  je       0x223e9b  ; -> 00223E9B
00223E8E  call     0x809950  ; -> 00809950 fn
00223E93  mov      qword ptr [rbx + 0x50], 0
00223E9B  mov      rcx, rbx
00223E9E  call     0x223a20  ; -> 00223A20 fn
00223EA3  mov      rcx, rbx
00223EA6  add      rsp, 0x20
00223EAA  pop      rbx
00223EAB  jmp      0x222000  ; -> 00222000 fn
```

## 00224D40 (123 B, extent 00224D40-00224DBB)

Page context: "00222BD0' calls '007A84A0' on 'this+0x38' (43 B) then **tail-jumps the base '00222000'** ('00222BF6') — the driver call plus the full teardown, not driver-only; Sep '00222FE0', Seb '00223E60', Shout '00224D40' route their cleanup through '002255B0' + '00809950'. | | 3, 4, 5 | **Sep: three id-range-gated re-dispatches to slot 0.** '00223100' fires when ~~'[+0x38] ≥ 151000' ('0x249F0 + 0x3E8')~~ '[+0x38]' lies **outside** '[0x249F0, 0x249"

```
00224D40  push     rbx
00224D42  sub      rsp, 0x20
00224D46  mov      rbx, rcx
00224D49  mov      qword ptr [rcx + 0x40], 0xffffffffffffffff
00224D51  call     0x222080  ; -> 00222080 fn
00224D56  mov      rcx, qword ptr [rbx + 0x20]
00224D5A  test     rcx, rcx
00224D5D  je       0x224d8f  ; -> 00224D8F
00224D5F  mov      r8, qword ptr [rbx + 0x48]
00224D63  mov      rdx, qword ptr [rbx + 0x50]
00224D67  call     0x2255b0  ; -> 002255B0 fn
00224D6C  mov      rcx, qword ptr [rbx + 0x20]
00224D70  mov      dl, 1
00224D72  add      rcx, 8
00224D76  call     0x7a88f0  ; -> 007A88F0 fn
00224D7B  xor      eax, eax
00224D7D  mov      qword ptr [rbx + 0x20], rax
00224D81  mov      qword ptr [rbx + 0x48], rax
00224D85  mov      qword ptr [rbx + 0x50], rax
00224D89  add      rsp, 0x20
00224D8D  pop      rbx
00224D8E  ret      
00224D8F  mov      rcx, qword ptr [rbx + 0x50]
00224D93  test     rcx, rcx
00224D96  je       0x224d9d  ; -> 00224D9D
00224D98  call     0x809950  ; -> 00809950 fn
00224D9D  mov      rcx, qword ptr [rbx + 0x48]
00224DA1  test     rcx, rcx
00224DA4  je       0x224dab  ; -> 00224DAB
00224DA6  call     0x809950  ; -> 00809950 fn
00224DAB  xor      eax, eax
00224DAD  mov      qword ptr [rbx + 0x48], rax
00224DB1  mov      qword ptr [rbx + 0x50], rax
00224DB5  add      rsp, 0x20
00224DB9  pop      rbx
00224DBA  ret      
```

## 00225440 (73 B, extent 00225440-00225489)

Page context: " flag byte: Music '00222C70' needs '& 1' and re-dispatches **slot 0**; Sep '00223540' and Seb '00224B30' (the latter also requires '[+0x38] != 0') need '& 2' and re-dispatch **slot 9**; Shout/Stream '00225440' need '& 4', also to slot 9. The byte carries three more commands, all with 'edx = 1': Sep '00223540' continues, but only when bit 2 is clear (bit 2 is a tail jump that ends slot 10), with '& 8' → own 'vtable[+0x18]' (**slot 3**), "

```
00225440  mov      qword ptr [rsp + 8], rbx
00225445  push     rdi
00225446  sub      rsp, 0x20
0022544A  mov      rdi, rdx
0022544D  mov      rbx, rcx
00225450  call     0x210b30  ; -> 00210B30 fn
00225455  mov      rcx, rax
00225458  call     0x210930  ; -> 00210930 fn
0022545D  test     eax, eax
0022545F  je       0x22547e  ; -> 0022547E
00225461  call     0x210b30  ; -> 00210B30 fn
00225466  test     byte ptr [rax + 0x3c], 4
0022546A  je       0x22547e  ; -> 0022547E
0022546C  mov      rax, qword ptr [rbx]
0022546F  mov      r8d, 1
00225475  mov      rdx, rdi
00225478  mov      rcx, rbx
0022547B  call     qword ptr [rax + 0x48]
0022547E  mov      rbx, qword ptr [rsp + 0x30]
00225483  add      rsp, 0x20
00225487  pop      rdi
00225488  ret      
```

## 002255B0 (9 B, extent 002255B0-002255B9)

Page context: "8' (43 B) then **tail-jumps the base '00222000'** ('00222BF6') — the driver call plus the full teardown, not driver-only; Sep '00222FE0', Seb '00223E60', Shout '00224D40' route their cleanup through '002255B0' + '00809950'. | | 3, 4, 5 | **Sep: three id-range-gated re-dispatches to slot 0.** '00223100' fires when ~~'[+0x38] ≥ 151000' ('0x249F0 + 0x3E8')~~ '[+0x38]' lies **outside** '[0x249F0, 0x249F0+999]': it computes '[+0x38] − 0x249F"

```
002255B0  mov      qword ptr [rcx + 0x20], rdx
002255B4  mov      qword ptr [rcx + 0x28], r8
002255B8  ret      
```

## 00225C40 (127 B, extent 00225C40-00225CBF)

Page context: "45 B) is the '.win.mab' bank-path builder the page names - '00908930'/'00908940'/'01E027D8'/'01F44830', '"%s%03d%s"'/'".win.mab"' strings, '00221710'/'00220C70'/'0016D6A0' pair/'00861EC0'/'0017D2E0'/'00225C40'/'00221D10'. Interior anchor '00222771' (a '00221710' call).  ## SWE2-EC7-43 update (2026-09-19) - '002238F0'  '002238F0' (292 B) is the 'SebAudioBank' slot-6 row body - '009089BC', '00225680'/'00225690'/'002256A0'/'002257E0'/'007A"

```
00225C40  push     rdi
00225C42  sub      rsp, 0x30
00225C46  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
00225C4F  mov      qword ptr [rsp + 0x48], rbx
00225C54  mov      qword ptr [rsp + 0x50], rsi
00225C59  mov      rbx, rdx
00225C5C  mov      rdi, rcx
00225C5F  xor      esi, esi
00225C61  mov      ecx, esi
00225C63  cmp      qword ptr [rdi + 0x210], rcx
00225C6A  sete     cl
00225C6D  call     0x16d6a0  ; -> 0016D6A0 fn
00225C72  lea      ecx, [rsi + 0x50]
00225C75  call     0x584740  ; -> 00584740 fn
00225C7A  mov      qword ptr [rsp + 0x40], rax
00225C7F  test     rax, rax
00225C82  je       0x225c8f  ; -> 00225C8F
00225C84  mov      rcx, rax
00225C87  call     0x597a20  ; -> 00597A20 fn
00225C8C  mov      rsi, rax
00225C8F  mov      qword ptr [rdi + 0x210], rsi
00225C96  mov      byte ptr [rsi + 0x38], 2
00225C9A  sub      rdi, rbx
00225C9D  nop      dword ptr [rax]
00225CA0  movzx    eax, byte ptr [rbx]
00225CA3  mov      byte ptr [rdi + rbx + 0x10], al
00225CA7  lea      rbx, [rbx + 1]
00225CAB  test     al, al
00225CAD  jne      0x225ca0  ; -> 00225CA0
00225CAF  mov      rbx, qword ptr [rsp + 0x48]
00225CB4  mov      rsi, qword ptr [rsp + 0x50]
00225CB9  add      rsp, 0x30
00225CBD  pop      rdi
00225CBE  ret      
```

## 0036E9F0 (192 B, extent 0036E9F0-0036EAB0)

Page context: "try's key '+0x14' it sizes and requests the 'us' bank from slot '0x21' into handle '+0xC', then           the 'jp' bank from slot '0x27' into '+0x10'.         - Each completion callback ('0036EAB0', '0036E9F0') hands the loaded buffer to '001DC130'. That wrapper takes           the audio registry's '+0x20' object, the 'ShoutAudioController' (constructor '0021BDB0', vtable           '00907FF0'), and enters its intake '0021C680'. The inta"

```
0036E9F0  mov      qword ptr [rsp + 8], rbx
0036E9F5  mov      qword ptr [rsp + 0x10], rsi
0036E9FA  mov      qword ptr [rsp + 0x18], rdi
0036E9FF  push     r14
0036EA01  sub      rsp, 0x30
0036EA05  cmp      ecx, -1
0036EA08  jne      0x36ea0f  ; -> 0036EA0F
0036EA0A  xor      r14d, r14d
0036EA0D  jmp      0x36ea36  ; -> 0036EA36
0036EA0F  mov      eax, ecx
0036EA11  and      eax, 0xf
0036EA14  test     cl, 0xf0
0036EA17  lea      rcx, [rax + rax*2]
0036EA1B  lea      rax, [rip - 0x24ea22]  ; -> 00120000 (image base)
0036EA22  lea      r14, [rax + 0x21b9ae0]  ; image base + 0x21b9ae0 = 022D9AE0
0036EA29  jne      0x36ea32  ; -> 0036EA32
0036EA2B  lea      r14, [rax + 0x21b9ab0]  ; image base + 0x21b9ab0 = 022D9AB0
0036EA32  lea      r14, [r14 + rcx*8]
0036EA36  mov      ecx, dword ptr [r14 + 0x10]
0036EA3A  call     0x36a0b0  ; -> 0036A0B0 fn
0036EA3F  movsx    edi, byte ptr [r14 + 1]
0036EA44  mov      rcx, rax
0036EA47  movzx    ebx, byte ptr [r14 + 2]
0036EA4C  mov      rsi, rax
0036EA4F  call     0x36c100  ; -> 0036C100 fn
0036EA54  movsx    edx, word ptr [r14 + 0x14]
0036EA59  lea      ecx, [rdi + 2]
0036EA5C  test     bl, bl
0036EA5E  mov      dword ptr [rsp + 0x20], 0
0036EA66  mov      r9d, eax
0036EA69  mov      r8, rsi
0036EA6C  cmove    ecx, edi
0036EA6F  call     0x2df450  ; -> 002DF450 fn
0036EA74  mov      dword ptr [r14 + 8], eax
0036EA78  test     eax, eax
0036EA7A  je       0x36ea85  ; -> 0036EA85
0036EA7C  cmp      dword ptr [r14 + 4], 0
0036EA81  je       0x36ea9a  ; -> 0036EA9A
0036EA83  jmp      0x36ea96  ; -> 0036EA96
0036EA85  mov      ecx, dword ptr [r14 + 0x10]
0036EA89  call     0x369800  ; -> 00369800 fn
0036EA8E  mov      dword ptr [r14 + 0x10], 0
0036EA96  mov      byte ptr [r14], 3
0036EA9A  mov      rbx, qword ptr [rsp + 0x40]
0036EA9F  mov      rsi, qword ptr [rsp + 0x48]
0036EAA4  mov      rdi, qword ptr [rsp + 0x50]
0036EAA9  add      rsp, 0x30
0036EAAD  pop      r14
0036EAAF  ret      
```

## 0036EAB0 (192 B, extent 0036EAB0-0036EB70)

Page context: "  For the entry's key '+0x14' it sizes and requests the 'us' bank from slot '0x21' into handle '+0xC', then           the 'jp' bank from slot '0x27' into '+0x10'.         - Each completion callback ('0036EAB0', '0036E9F0') hands the loaded buffer to '001DC130'. That wrapper takes           the audio registry's '+0x20' object, the 'ShoutAudioController' (constructor '0021BDB0', vtable           '00907FF0'), and enters its intake '0021C68"

```
0036EAB0  mov      qword ptr [rsp + 8], rbx
0036EAB5  mov      qword ptr [rsp + 0x10], rsi
0036EABA  mov      qword ptr [rsp + 0x18], rdi
0036EABF  push     r14
0036EAC1  sub      rsp, 0x30
0036EAC5  cmp      ecx, -1
0036EAC8  jne      0x36eacf  ; -> 0036EACF
0036EACA  xor      r14d, r14d
0036EACD  jmp      0x36eaf6  ; -> 0036EAF6
0036EACF  mov      eax, ecx
0036EAD1  and      eax, 0xf
0036EAD4  test     cl, 0xf0
0036EAD7  lea      rcx, [rax + rax*2]
0036EADB  lea      rax, [rip - 0x24eae2]  ; -> 00120000 (image base)
0036EAE2  lea      r14, [rax + 0x21b9ae0]  ; image base + 0x21b9ae0 = 022D9AE0
0036EAE9  jne      0x36eaf2  ; -> 0036EAF2
0036EAEB  lea      r14, [rax + 0x21b9ab0]  ; image base + 0x21b9ab0 = 022D9AB0
0036EAF2  lea      r14, [r14 + rcx*8]
0036EAF6  mov      ecx, dword ptr [r14 + 0xc]
0036EAFA  call     0x36a0b0  ; -> 0036A0B0 fn
0036EAFF  movsx    edi, byte ptr [r14 + 1]
0036EB04  mov      rcx, rax
0036EB07  movzx    ebx, byte ptr [r14 + 2]
0036EB0C  mov      rsi, rax
0036EB0F  call     0x36c100  ; -> 0036C100 fn
0036EB14  movsx    edx, word ptr [r14 + 0x14]
0036EB19  lea      ecx, [rdi + 2]
0036EB1C  test     bl, bl
0036EB1E  mov      dword ptr [rsp + 0x20], 1
0036EB26  mov      r9d, eax
0036EB29  mov      r8, rsi
0036EB2C  cmove    ecx, edi
0036EB2F  call     0x2df450  ; -> 002DF450 fn
0036EB34  mov      dword ptr [r14 + 4], eax
0036EB38  test     eax, eax
0036EB3A  je       0x36eb45  ; -> 0036EB45
0036EB3C  cmp      dword ptr [r14 + 8], 0
0036EB41  je       0x36eb5a  ; -> 0036EB5A
0036EB43  jmp      0x36eb56  ; -> 0036EB56
0036EB45  mov      ecx, dword ptr [r14 + 0xc]
0036EB49  call     0x369800  ; -> 00369800 fn
0036EB4E  mov      dword ptr [r14 + 0xc], 0
0036EB56  mov      byte ptr [r14], 3
0036EB5A  mov      rbx, qword ptr [rsp + 0x40]
0036EB5F  mov      rsi, qword ptr [rsp + 0x48]
0036EB64  mov      rdi, qword ptr [rsp + 0x50]
0036EB69  add      rsp, 0x30
0036EB6D  pop      r14
0036EB6F  ret      
```

## 00657140 (3 B, extent 00657140-00657143)

Page context: "'002256A0', then probe the '+0x60'/'+0x70' map — **the BD-3 "one operation with a varying parameter" is confirmed**: same body, the differing bytes are the constant/field used per slot. | | 6 | base '00657140' = 'ret 0'. Sep '00222D30': get entry '00221E60', require state 1 + '+0x49 & 0x40', then '002224F0' when arg equals '[+0x38]' else '002225B0' (both with '0x120'). Seb '002238F0' (292 B) runs the same predicate family plus driver '0"

```
00657140  xor      al, al
00657142  ret      
```
