# F-interior pack: `25-EBP-Script-Container/Container/ebp2-container.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/ebp2-container.json`.

Functions: 2. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 01c2429f6	SWE2-CONTRACT: pass-22 debt batch B - 47 Script-VM, Resource, EBP and PKFL pages' cross-subsystem ne; inbox mentions: ASSIGNMENTS.md, FABLE.md, SWE2-CONTRACT.md, repos-1e.md, repos-3f.md, repos-c9.md). OPUS read these before packing.

## 0026B870 (48 B, extent 0026B870-0026B8A0)

Page context: "+0x1D0'–'+0x1DC' counter/'u16' arrays, '+0x17' flags, '+0x108' teardown callback ('ActorManager_SetResourceTeardownCallback' '00268630'), '+0x201', '+0x13', and the wholesale 'rep stosd' slot zeroer '0026B870'. Two of the 63 are notable by role rather than field: '0026CE60' is where 'rbx = base + index*0x288' gets **installed as the cached slot** '[02099D70]' (gated on '+0x10'/'+0x13' flags), and '0025D9F6' is the per-slot pump that iss"

```
0026B870  mov      qword ptr [rsp + 8], rdi
0026B875  movsxd   rax, ecx
0026B878  mov      ecx, 0x10
0026B87D  imul     rdi, rax, 0x288
0026B884  lea      rax, [rip + 0x1e2d585]  ; -> 02098E10
0026B88B  add      rax, 0x204
0026B891  add      rdi, rax
0026B894  neg      edx
0026B896  sbb      eax, eax
0026B898  rep stosd dword ptr [rdi], eax
0026B89A  mov      rdi, qword ptr [rsp + 8]
0026B89F  ret      
```

## 00297640 (167 B, extent 00297640-002976E7)

Page context: "he shipping bytes 2026-09-14 (OPUS).  **UI — CLIENT (SWE2-EC7 batch-150).** The '0029AEF0' flag sweep runs on the shared '0035BB60'/'0035BB00' record accessors the UI layer calls heavily ('002737B0'/'00297640'/'002734F0'/'002964D0' among them), and '00297170' itself sits inside that layer's call neighbourhood ('002904D0'/'00273A20'/'0029AE50') - shared accessor fan-in over container records, not UI ownership of the container.  **Gamepla"

```
00297640  sub      rsp, 0x28
00297644  cmp      edx, 7
00297647  ja       0x29767e  ; -> 0029767E
00297649  movsxd   rax, edx
0029764C  lea      r10, [rip - 0x177653]  ; -> 00120000 (image base)
00297653  mov      edx, dword ptr [r10 + rax*4 + 0x1776e8]  ; image base + 0x1776e8 = 002976E8
0029765B  add      rdx, r10
0029765E  jmp      rdx
00297660  movsxd   rax, r9d
00297663  imul     rdx, rax, 0x160
0029766A  test     byte ptr [rdx + rcx + 0x318], 2
00297672  je       0x297685  ; -> 00297685
00297674  mov      ecx, 5
00297679  call     0x249c60  ; -> 00249C60 fn
0029767E  xor      eax, eax
00297680  add      rsp, 0x28
00297684  ret      
00297685  mov      ecx, 0x15
0029768A  call     0x249c60  ; -> 00249C60 fn
0029768F  mov      eax, 1
00297694  add      rsp, 0x28
00297698  ret      
00297699  mov      ecx, r8d
0029769C  call     0x35bb00  ; -> 0035BB00 fn
002976A1  mov      ecx, eax
002976A3  call     0x29b440  ; -> 0029B440 fn
002976A8  mov      ecx, 1
002976AD  call     0x249c60  ; -> 00249C60 fn
002976B2  mov      eax, 1
002976B7  add      rsp, 0x28
002976BB  ret      
002976BC  call     0x35d320  ; -> 0035D320 fn
002976C1  movsx    ecx, word ptr [rax + 0x14]
002976C5  call     0x299b90  ; -> 00299B90 fn
002976CA  test     eax, eax
002976CC  je       0x297674  ; -> 00297674
002976CE  call     0x35bc30  ; -> 0035BC30 fn
002976D3  mov      ecx, 3
002976D8  call     0x249c60  ; -> 00249C60 fn
002976DD  mov      eax, 1
002976E2  add      rsp, 0x28
002976E6  ret      
```
