# F-interior pack: `00-Engine-Core-Runtime/ABI-Recovery/derived-call-signatures.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/derived-call-signatures.json`.

Functions: 11. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (inbox mentions: FABLE.md, SWE2-AUDIT-SPEC.md). OPUS read these before packing.

## 00197980 (7 B, extent 00197980-00197987)

Page context: "solved arities live in the table under this box. Static, body reads.        | forwarder | derived | tail target | target reads | verdict | arity | why |       |---|---:|---|---|---|---:|---|       | '00197980' | 2 | '00197990' FUN_00197990 | [1] | EXACT | **2** |  |       | '001C1710' | 1 | '001C1810' SaveloadManager_RequestDisableAutosaveList | [1] | EXACT | **1** |  |       | '002681C0' | 1 | '00269C70' PartyRoster_AssignActorToSlot |"

```
00197980  mov      ecx, edx
00197982  jmp      0x197990  ; -> 00197990 fn
```

## 002681C0 (9 B, extent 002681C0-002681C9)

Page context: "--:|---|       | '00197980' | 2 | '00197990' FUN_00197990 | [1] | EXACT | **2** |  |       | '001C1710' | 1 | '001C1810' SaveloadManager_RequestDisableAutosaveList | [1] | EXACT | **1** |  |       | '002681C0' | 1 | '00269C70' PartyRoster_AssignActorToSlot | [1, 2] | EXACT | **1** | supplies 2 |       | '0026D6D0' | 0 | '0026D6F0' Movement_SetRequestedSpeed | [1, 2, 3] | EXACT | **0** | supplies all three: 'xmm1' from '01DFE0BC', 'xmm0'"

```
002681C0  movsx    edx, byte ptr [rcx + 0x12]
002681C4  jmp      0x269c70  ; -> 00269C70 fn
```

## 002D6640 (61 B, extent 002D6640-002D667D)

Page context: "0323600' 2→3. The three branchy bodies held back on 2026-09-16 were read path-sensitively today: in each, the passed register is written on NO path, so the verdict does not depend on which arm runs. '002D6640''s flag is explained rather than wrong - it has no unconditional 'jmp' but a conditional tail jump 'je 00249840', whose target reads nothing. The 'lower_bound' column therefore means *narrows* for 22 rows and *short by 1* for 5; th"

```
002D6640  test     cx, cx
002D6643  jne      0x2d664d  ; -> 002D664D
002D6645  test     edx, edx
002D6647  je       0x249840  ; -> 00249840 fn
002D664D  movzx    eax, cx
002D6650  test     edx, edx
002D6652  mov      byte ptr [rip + 0x2cc0d47], 1  ; -> 02F973A0
002D6659  setne    byte ptr [rip + 0x2cc0d42]  ; -> 02F973A2
002D6660  mov      word ptr [rip + 0x2cc0d43], ax  ; -> 02F973AA
002D6667  mov      word ptr [rip + 0x2cc0d3a], ax  ; -> 02F973A8
002D666E  mov      word ptr [rip + 0x2cc0d31], ax  ; -> 02F973A6
002D6675  mov      word ptr [rip + 0x2cc0d28], ax  ; -> 02F973A4
002D667C  ret      
```

## 002FD420 (267 B, extent 002FD420-002FD52B)

Page context: " in '001E0AA0' and '00323C60', the 'rax' frame of '001993B0', the early-out prologue of '0057EBB0') read none. Over the 562 rows, **12 read stack parameters**: nine with derived arity 4, one with 3 ('002FD420', position 5), two with 2 ('008628F0', position 5; '0085DDE0', positions 7 to 9); the highest position anywhere is 9. Ten of the twelve lie inside the 75-row at-risk union of the RE-STATED block above and two ('002FD420', '0085DDE0"

```
002FD420  mov      qword ptr [rsp + 0x10], rbp
002FD425  mov      qword ptr [rsp + 0x18], rsi
002FD42A  mov      qword ptr [rsp + 0x20], rdi
002FD42F  push     r14
002FD431  sub      rsp, 0x20
002FD435  mov      r14d, dword ptr [rsp + 0x50]
002FD43A  mov      edi, edx
002FD43C  movzx    ebp, cx
002FD43F  and      r14d, 1
002FD443  mov      eax, ebp
002FD445  mov      r10d, ebp
002FD448  shr      rax, 0xc
002FD44C  and      r10d, 0xfff
002FD453  imul     r9, rax, 0x58
002FD457  lea      rax, [rip + 0x1bee862]  ; -> 01EEBCC0
002FD45E  mov      esi, r8d
002FD461  mov      rdx, qword ptr [r9 + rax + 8]
002FD466  test     rdx, rdx
002FD469  jne      0x2fd472  ; -> 002FD472
002FD46B  xor      eax, eax
002FD46D  jmp      0x2fd515  ; -> 002FD515
002FD472  mov      eax, r10d
002FD475  shr      rax, 4
002FD479  mov      qword ptr [rsp + 0x30], rbx
002FD47E  xor      ebx, ebx
002FD480  mov      r9d, ebx
002FD483  lea      r8, [rdx + rax*2]
002FD487  movzx    eax, r10b
002FD48B  movsx    edx, word ptr [r8]
002FD48F  and      al, 0xf
002FD491  movzx    ecx, al
002FD494  bt       edx, ecx
002FD497  mov      ecx, edi
002FD499  setb     r9b
002FD49D  test     esi, esi
002FD49F  lea      eax, [r9 + rdi]
002FD4A3  cmove    ecx, eax
002FD4A6  test     ecx, ecx
002FD4A8  js       0x2fd4e1  ; -> 002FD4E1
002FD4AA  test     esi, esi
002FD4AC  lea      eax, [r9 + rdi]
002FD4B0  mov      ecx, edi
002FD4B2  cmove    ecx, eax
002FD4B5  cmp      ecx, 1
002FD4B8  jle      0x2fd4c9  ; -> 002FD4C9
002FD4BA  and      r10d, 0xf
002FD4BE  mov      ebx, 1
002FD4C3  bts      edx, r10d
002FD4C7  jmp      0x2fd4e9  ; -> 002FD4E9
002FD4C9  mov      ebx, edi
002FD4CB  test     esi, esi
002FD4CD  jne      0x2fd4d3  ; -> 002FD4D3
002FD4CF  lea      ebx, [r9 + rdi]
002FD4D3  test     ebx, ebx
002FD4D5  je       0x2fd4e1  ; -> 002FD4E1
002FD4D7  and      r10d, 0xf
002FD4DB  bts      edx, r10d
002FD4DF  jmp      0x2fd4e9  ; -> 002FD4E9
002FD4E1  and      r10d, 0xf
002FD4E5  btr      edx, r10d
002FD4E9  mov      word ptr [r8], dx
002FD4ED  movzx    ecx, bp
002FD4F0  mov      r8d, ebx
002FD4F3  mov      edx, r9d
002FD4F6  call     0x325f40  ; -> 00325F40 fn
002FD4FB  test     esi, esi
002FD4FD  jne      0x2fd50e  ; -> 002FD50E
002FD4FF  test     r14d, r14d
002FD502  je       0x2fd50e  ; -> 002FD50E
002FD504  mov      edx, edi
002FD506  movzx    ecx, bp
002FD509  call     0x46a630  ; -> 0046A630 fn
002FD50E  mov      eax, ebx
002FD510  mov      rbx, qword ptr [rsp + 0x30]
002FD515  mov      rbp, qword ptr [rsp + 0x38]
002FD51A  mov      rsi, qword ptr [rsp + 0x40]
002FD51F  mov      rdi, qword ptr [rsp + 0x48]
002FD524  add      rsp, 0x20
002FD528  pop      r14
002FD52A  ret      
```

## 0030BEB0 (63 B, extent 0030BEB0-0030BEEF)

Page context: " different population.) The derived subjects' own callers are       equally spread: '0031B760' is called by **gameplay** '0030BFB0'/'0030B050'/'0030BA30',       **movement** '00239210' and **party** '0030BEB0'; '002EB030' by '003299B0'/'003B7E20';       '003299B0' by '00313500'. That is consistent both with a working detector — most log calls pass       fewer than five arguments — and with a broken one, so it discriminates nothing. **Th"

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

## 0030BFB0 (96 B, extent 0030BFB0-0030C010)

Page context: "_Native_Bridge code; a second control on a       render-path logger would be a different population.) The derived subjects' own callers are       equally spread: '0031B760' is called by **gameplay** '0030BFB0'/'0030B050'/'0030BA30',       **movement** '00239210' and **party** '0030BEB0'; '002EB030' by '003299B0'/'003B7E20';       '003299B0' by '00313500'. That is consistent both with a working detector — most log calls pass       fewer "

```
0030BFB0  sub      rsp, 0x28
0030BFB4  call     0x31b760  ; -> 0031B760 fn
0030BFB9  mov      rcx, rax
0030BFBC  test     rax, rax
0030BFBF  je       0x30c009  ; -> 0030C009
0030BFC1  test     byte ptr [rax], 0x10
0030BFC4  je       0x30c009  ; -> 0030C009
0030BFC6  mov      rdx, qword ptr [rax + 0x698]
0030BFCD  mov      eax, dword ptr [rdx + 0x64]
0030BFD0  or       eax, dword ptr [rdx + 0x3c]
0030BFD3  test     eax, 0x8000201b
0030BFD8  je       0x30bfe8  ; -> 0030BFE8
0030BFDA  mov      eax, dword ptr [rcx]
0030BFDC  shr      rax, 0x17
0030BFE0  and      eax, 1
0030BFE3  add      rsp, 0x28
0030BFE7  ret      
0030BFE8  test     rdx, rdx
0030BFEB  je       0x30bffe  ; -> 0030BFFE
0030BFED  movzx    eax, byte ptr [rdx + 5]
0030BFF1  test     eax, eax
0030BFF3  jne      0x30bffe  ; -> 0030BFFE
0030BFF5  add      rsp, 0x28
0030BFF9  jmp      0x308130  ; -> 00308130 fn
0030BFFE  xor      edx, edx
0030C000  add      rsp, 0x28
0030C004  jmp      0x308040  ; -> 00308040 fn
0030C009  xor      eax, eax
0030C00B  add      rsp, 0x28
0030C00F  ret      
```

## 0032AB50 (14 B, extent 0032AB50-0032AB5E)

Page context: "sses |       | '00323600' | 2 | '00323D10' BattleStats_CheckLicenseNodeAcquireReason | [1, 2, 3] | RAISES | **3** | same two arms as '003235C0' without the 'r9d' store; 'r8' passes on both |       | '0032AB50' | 2 | '0030B570' BattleIdClassD_SetRuntimeFlagBit1IfSupported | [1, 2] | EXACT | **2** |  |       | '00369080' | 0 | '00863520' FUN_00863520 | [2] | EXACT | **0** | supplies 2 |       | '003690F0' | 0 | '00863800' FUN_00863800 | ["

```
0032AB50  mov      eax, edx
0032AB52  xor      edx, edx
0032AB54  test     eax, eax
0032AB56  setne    dl
0032AB59  jmp      0x30b570  ; -> 0030B570 fn
```

## 0057EBB0 (163 B, extent 0057EBB0-0057EC53)

Page context: "nstructors are known to take, and four bodies that would fool a naive scan (epilogue restores after a tail jump in '001E0AA0' and '00323C60', the 'rax' frame of '001993B0', the early-out prologue of '0057EBB0') read none. Over the 562 rows, **12 read stack parameters**: nine with derived arity 4, one with 3 ('002FD420', position 5), two with 2 ('008628F0', position 5; '0085DDE0', positions 7 to 9); the highest position anywhere is 9. Te"

```
0057EBB0  cmp      ecx, 3
0057EBB3  jne      0x57ec52  ; -> 0057EC52
0057EBB9  push     rbx
0057EBBA  sub      rsp, 0x40
0057EBBE  mov      rax, qword ptr [rip + 0x19c5c6b]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0057EBC5  xor      rax, rsp
0057EBC8  mov      qword ptr [rsp + 0x30], rax
0057EBCD  mov      ebx, r8d
0057EBD0  test     edx, edx
0057EBD2  jne      0x57ebdd  ; -> 0057EBDD
0057EBD4  or       dword ptr [rbx + 0xc4], 1
0057EBDB  jmp      0x57ebeb  ; -> 0057EBEB
0057EBDD  and      dword ptr [rbx + 0xc4], 0xfffffffe
0057EBE4  or       dword ptr [rbx + 0xc4], 2
0057EBEB  mov      rcx, qword ptr [rbx + 0xc8]
0057EBF2  test     rcx, rcx
0057EBF5  je       0x57ec2d  ; -> 0057EC2D
0057EBF7  mov      rax, qword ptr [rip + 0x272adc2]  ; -> 02CA99C0
0057EBFE  mov      dword ptr [rsp + 0x20], 3
0057EC06  test     rax, rax
0057EC09  jne      0x57ec0f  ; -> 0057EC0F
0057EC0B  mov      al, 0xff
0057EC0D  jmp      0x57ec16  ; -> 0057EC16
0057EC0F  movzx    eax, byte ptr [rax + 0x39a]
0057EC16  mov      dword ptr [rsp + 0x28], edx
0057EC1A  lea      r8, [rsp + 0x20]
0057EC1F  mov      edx, 0x1d
0057EC24  mov      byte ptr [rsp + 0x24], al
0057EC28  call     0x247510  ; -> 00247510 fn
0057EC2D  mov      eax, dword ptr [rbx + 0xc0]
0057EC33  test     al, 1
0057EC35  jne      0x57ec40  ; -> 0057EC40
0057EC37  and      eax, 0xfffffffd
0057EC3A  mov      dword ptr [rbx + 0xc0], eax
0057EC40  mov      rcx, qword ptr [rsp + 0x30]
0057EC45  xor      rcx, rsp
0057EC48  call     0x808c40  ; -> 00808C40 fn
0057EC4D  add      rsp, 0x40
0057EC51  pop      rbx
0057EC52  ret      
```

## 00792870 (206 B, extent 00792870-0079293E)

Page context: "dress whose '[−8]' is a valid RTTI locator, then the store's base register traced back to 'rcx') finds seven: the 'PFramework' input-device constructors '007927C0' ('PInputDeviceKeyboard', arity 2), '00792870' ('PInputDeviceMouse', 2), '00792940' ('PInputDevicePad', 2, the base the three pad variants call), '00792AB0' ('PInputDevicePadDirectInput', 3), '00792B70' ('PInputDevicePadSteamController', 1), '00792CB0' ('PInputDevicePadXInput'"

```
00792870  mov      qword ptr [rsp + 8], rcx
00792875  push     rbx
00792876  sub      rsp, 0x40
0079287A  mov      qword ptr [rsp + 0x30], 0xfffffffffffffffe
00792883  mov      rbx, rcx
00792886  lea      r8, [rcx + 8]
0079288A  mov      qword ptr [r8], r8
0079288D  mov      qword ptr [r8 + 8], r8
00792891  lea      rax, [rip + 0x151fb28]  ; -> 01CB23C0
00792898  mov      qword ptr [rcx], rax
0079289B  lea      rax, [rcx + 0x18]
0079289F  mov      qword ptr [rax], rax
007928A2  mov      qword ptr [rax + 8], rax
007928A6  mov      qword ptr [rcx + 0x28], rdx
007928AA  mov      rax, qword ptr [rip + 0x17ad93f]  ; -> 01F401F0 [u64 0x0000000001F401E8]
007928B1  lea      rcx, [rip + 0x17ad930]  ; -> 01F401E8
007928B8  mov      qword ptr [r8], rcx
007928BB  mov      qword ptr [r8 + 8], rax
007928BF  mov      qword ptr [rax], r8
007928C2  mov      qword ptr [rip + 0x17ad927], r8  ; -> 01F401F0 [u64 0x0000000001F401E8]
007928C9  lea      rax, [rip + 0x151fb28]  ; -> 01CB23F8
007928D0  mov      qword ptr [rbx], rax
007928D3  lea      rcx, [rbx + 0x30]
007928D7  lea      rax, [rip - 0x62523e]  ; -> 0016D6A0
007928DE  mov      qword ptr [rsp + 0x20], rax
007928E3  lea      r9, [rip + 0x4a6]  ; -> 00792D90
007928EA  mov      edx, 0x48
007928EF  lea      r8d, [rdx - 0x42]
007928F3  call     0x808fe4  ; -> 00808FE4 fn
007928F8  mov      byte ptr [rbx + 0x1e6], 0
007928FF  xor      eax, eax
00792901  mov      qword ptr [rbx + 0x1e8], rax
00792908  mov      dword ptr [rbx + 0x1f0], eax
0079290E  lea      rax, [rbx + 0x1e0]
00792915  mov      ecx, 3
0079291A  nop      word ptr [rax + rax]
00792920  mov      byte ptr [rax + 0x14], 0
00792924  mov      byte ptr [rax], 0
00792927  mov      byte ptr [rax + 3], 0
0079292B  lea      rax, [rax + 1]
0079292F  sub      rcx, 1
00792933  jne      0x792920  ; -> 00792920
00792935  mov      rax, rbx
00792938  add      rsp, 0x40
0079293C  pop      rbx
0079293D  ret      
```

## 0079D620 (10 B, extent 0079D620-0079D62A)

Page context: "r PASSES it (never writes it - the target's read is the forwarder's incoming argument). **22 are EXACT** (the derived arity already covers everything passed through) and **5 RAISE**: '00321840' 0→1, '0079D620' 0→2, '00308010' 1→2, '003235C0' 2→3, '00323600' 2→3. The three branchy bodies held back on 2026-09-16 were read path-sensitively today: in each, the passed register is written on NO path, so the verdict does not depend on which ar"

```
0079D620  mov      ecx, 2
0079D625  jmp      0x796fc0  ; -> 00796FC0 fn
```

## 007A08A0 (65 B, extent 007A08A0-007A08E1)

Page context: "0 | '007998E0' FUN_007998e0 | [] | EXACT | **0** |  |       | '0079D620' | 0 | '00796FC0' FUN_00796fc0 | [1, 2] | RAISES | **2** | 'mov ecx, 2' supplies 1; 'rdx' passes, read at '00796FEA' |       | '007A08A0' | 1 | '0079BDF0' FUN_0079bdf0 | [1] | EXACT | **1** |  |       | '00862670' | 2 | '001E09B0' InputAPI_PollControlState | [1] | EXACT | **2** |  |       | '008628F0' | 2 | '001E1120' InputFeedback_DispatchViaManagerGate | [1, 2, 3]"

```
007A08A0  push     rbx
007A08A2  sub      rsp, 0x20
007A08A6  cmp      byte ptr [rcx + 0x69], 0
007A08AA  mov      rbx, rcx
007A08AD  je       0x7a08ba  ; -> 007A08BA
007A08AF  mov      eax, 9
007A08B4  add      rsp, 0x20
007A08B8  pop      rbx
007A08B9  ret      
007A08BA  cmp      dword ptr [rcx + 0x64], 0
007A08BE  jne      0x7a08ca  ; -> 007A08CA
007A08C0  mov      rax, qword ptr [rcx]
007A08C3  call     qword ptr [rax + 0x48]
007A08C6  test     eax, eax
007A08C8  jne      0x7a08db  ; -> 007A08DB
007A08CA  inc      dword ptr [rbx + 0x64]
007A08CD  mov      rcx, qword ptr [rbx + 0x58]
007A08D1  add      rsp, 0x20
007A08D5  pop      rbx
007A08D6  jmp      0x79bdf0  ; -> 0079BDF0 fn
007A08DB  add      rsp, 0x20
007A08DF  pop      rbx
007A08E0  ret      
```
