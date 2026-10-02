# F-interior pack: `22-Middleware-PhyreEngine/Subsystem-Map/phyre-subsystem-map.md`

Generated 2026-10-02 08:46 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/phyre-subsystem-map.json`.

Functions: 6. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 6075e3017	SWE2-FRONTIER for FABLE: pass-22 unattributed appends - the other 11 PUBLISHABLE pages (batch 2, 21/; inbox mentions: FABLE.md, SWE2-FRONTIER.md, repos-94.md). OPUS read these before packing.

## 005AA2C0 (43 B, extent 005AA2C0-005AA2EB)

Page context: "(320 B) and '006A8810' (270 B, Middleware), '006A0B60' (139 B) and '00691DB0' (64 B, Physics), '00646AB0' (81 B, PostProcessing), '007933C0', '00793570', '00793750', '007934E0' (Framework, 11–73 B), '005AA2C0', '005AA260', '005A9F00', '005A9E60' (Animation, 11–43 B), '006A91C0', '006A9280', '006A9150' (GameplayTrigger, 4–62 B), '0018D0E0' and '005DD660' (Rendering, 11 B). Reachable bounds *driven* from above (a slot in a table reachable"

```
005AA2C0  sub      rsp, 0x38
005AA2C4  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
005AA2CD  lea      rax, [rip + 0x786fc4]  ; -> 00D31298
005AA2D4  mov      qword ptr [rcx], rax
005AA2D7  mov      rcx, qword ptr [rcx + 8]
005AA2DB  test     rcx, rcx
005AA2DE  je       0x5aa2e6  ; -> 005AA2E6
005AA2E0  call     0x584730  ; -> 00584730 fn
005AA2E5  nop      
005AA2E6  add      rsp, 0x38
005AA2EA  ret      
```

## 00646AB0 (81 B, extent 00646AB0-00646B01)

Page context: "e static dead-linked floor: '001E2AF0' (4,745 B, Rendering), '005CCD00' (926 B, DebugUtils), '006A8A20' (320 B) and '006A8810' (270 B, Middleware), '006A0B60' (139 B) and '00691DB0' (64 B, Physics), '00646AB0' (81 B, PostProcessing), '007933C0', '00793570', '00793750', '007934E0' (Framework, 11–73 B), '005AA2C0', '005AA260', '005A9F00', '005A9E60' (Animation, 11–43 B), '006A91C0', '006A9280', '006A9150' (GameplayTrigger, 4–62 B), '0018D"

```
00646AB0  push     rbx
00646AB2  sub      rsp, 0x30
00646AB6  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
00646ABF  mov      rbx, rcx
00646AC2  lea      rax, [rip + 0x71b387]  ; -> 00D61E50
00646AC9  mov      qword ptr [rcx], rax
00646ACC  mov      ecx, dword ptr [rcx + 0x30]
00646ACF  mov      eax, ecx
00646AD1  shr      eax, 0x1f
00646AD4  not      al
00646AD6  test     al, 1
00646AD8  je       0x646af2  ; -> 00646AF2
00646ADA  btr      ecx, 0x1f
00646ADE  cmp      ecx, 1
00646AE1  jbe      0x646af2  ; -> 00646AF2
00646AE3  mov      rcx, qword ptr [rbx + 0x38]
00646AE7  test     rcx, rcx
00646AEA  je       0x646af2  ; -> 00646AF2
00646AEC  call     0x584730  ; -> 00584730 fn
00646AF1  nop      
00646AF2  xor      eax, eax
00646AF4  mov      qword ptr [rbx + 0x38], rax
00646AF8  mov      dword ptr [rbx + 0x30], eax
00646AFB  add      rsp, 0x30
00646AFF  pop      rbx
00646B00  ret      
```

## 00691DB0 (64 B, extent 00691DB0-00691DF0)

Page context: " The **20 unreached** are the static dead-linked floor: '001E2AF0' (4,745 B, Rendering), '005CCD00' (926 B, DebugUtils), '006A8A20' (320 B) and '006A8810' (270 B, Middleware), '006A0B60' (139 B) and '00691DB0' (64 B, Physics), '00646AB0' (81 B, PostProcessing), '007933C0', '00793570', '00793750', '007934E0' (Framework, 11–73 B), '005AA2C0', '005AA260', '005A9F00', '005A9E60' (Animation, 11–43 B), '006A91C0', '006A9280', '006A9150' (Game"

```
00691DB0  push     rbx
00691DB2  sub      rsp, 0x20
00691DB6  lea      rax, [rip + 0x6e7a73]  ; -> 00D79830
00691DBD  mov      rbx, rcx
00691DC0  mov      qword ptr [rcx], rax
00691DC3  mov      rcx, qword ptr [rcx + 0x78]
00691DC7  test     rcx, rcx
00691DCA  je       0x691dd6  ; -> 00691DD6
00691DCC  mov      rax, qword ptr [rcx]
00691DCF  mov      edx, 1
00691DD4  call     qword ptr [rax]
00691DD6  xor      eax, eax
00691DD8  mov      qword ptr [rbx + 0x78], rax
00691DDC  mov      qword ptr [rbx + 0x68], rax
00691DE0  lea      rax, [rip + 0x6e79a9]  ; -> 00D79790
00691DE7  mov      qword ptr [rbx], rax
00691DEA  add      rsp, 0x20
00691DEE  pop      rbx
00691DEF  ret      
```

## 007933C0 (69 B, extent 007933C0-00793405)

Page context: "F0' (4,745 B, Rendering), '005CCD00' (926 B, DebugUtils), '006A8A20' (320 B) and '006A8810' (270 B, Middleware), '006A0B60' (139 B) and '00691DB0' (64 B, Physics), '00646AB0' (81 B, PostProcessing), '007933C0', '00793570', '00793750', '007934E0' (Framework, 11–73 B), '005AA2C0', '005AA260', '005A9F00', '005A9E60' (Animation, 11–43 B), '006A91C0', '006A9280', '006A9150' (GameplayTrigger, 4–62 B), '0018D0E0' and '005DD660' (Rendering, 11 "

```
007933C0  push     rbx
007933C2  sub      rsp, 0x30
007933C6  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
007933CF  mov      rbx, rcx
007933D2  lea      rax, [rip + 0x151f0cf]  ; -> 01CB24A8
007933D9  mov      qword ptr [rcx], rax
007933DC  mov      rcx, qword ptr [rcx + 0x28]
007933E0  test     rcx, rcx
007933E3  je       0x7933eb  ; -> 007933EB
007933E5  call     0x584730  ; -> 00584730 fn
007933EA  nop      
007933EB  xor      eax, eax
007933ED  mov      qword ptr [rbx + 0x28], rax
007933F1  mov      qword ptr [rbx + 0x30], rax
007933F5  mov      dword ptr [rbx + 0x40], eax
007933F8  mov      rcx, rbx
007933FB  add      rsp, 0x30
007933FF  pop      rbx
00793400  jmp      0x793410  ; -> 00793410 fn
```

## 00793570 (73 B, extent 00793570-007935B9)

Page context: ", Rendering), '005CCD00' (926 B, DebugUtils), '006A8A20' (320 B) and '006A8810' (270 B, Middleware), '006A0B60' (139 B) and '00691DB0' (64 B, Physics), '00646AB0' (81 B, PostProcessing), '007933C0', '00793570', '00793750', '007934E0' (Framework, 11–73 B), '005AA2C0', '005AA260', '005A9F00', '005A9E60' (Animation, 11–43 B), '006A91C0', '006A9280', '006A9150' (GameplayTrigger, 4–62 B), '0018D0E0' and '005DD660' (Rendering, 11 B). Reachabl"

```
00793570  push     rbx
00793572  sub      rsp, 0x30
00793576  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0079357F  mov      rbx, rcx
00793582  lea      rax, [rip + 0x151ef3f]  ; -> 01CB24C8
00793589  mov      qword ptr [rcx], rax
0079358C  add      rcx, 0xb0
00793593  lea      r9, [rip - 0x625efa]  ; -> 0016D6A0
0079359A  mov      edx, 0x48
0079359F  lea      r8d, [rdx - 0x44]
007935A3  call     0x809054  ; -> 00809054 fn
007935A8  nop      
007935A9  lea      rax, [rip + 0x151ee10]  ; -> 01CB23C0
007935B0  mov      qword ptr [rbx], rax
007935B3  add      rsp, 0x30
007935B7  pop      rbx
007935B8  ret      
```

## 00793750 (54 B, extent 00793750-00793786)

Page context: ", '005CCD00' (926 B, DebugUtils), '006A8A20' (320 B) and '006A8810' (270 B, Middleware), '006A0B60' (139 B) and '00691DB0' (64 B, Physics), '00646AB0' (81 B, PostProcessing), '007933C0', '00793570', '00793750', '007934E0' (Framework, 11–73 B), '005AA2C0', '005AA260', '005A9F00', '005A9E60' (Animation, 11–43 B), '006A91C0', '006A9280', '006A9150' (GameplayTrigger, 4–62 B), '0018D0E0' and '005DD660' (Rendering, 11 B). Reachable bounds *dr"

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
