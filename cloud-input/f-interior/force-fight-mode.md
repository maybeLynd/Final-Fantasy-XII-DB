# F-interior pack: `00-Engine-Core-Runtime/Force-Fight-Mode/force-fight-mode.md`

Generated 2026-10-03 02:40 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/force-fight-mode.json`.

Functions: 3. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: de4492e21	SWE2-CONTRACT: pass-22 debt final - six-folder worklist (597 pairs) fully dispositioned, 0 live find; f9017b106	SWE2-CONTRACT: repair 807950d2a - restore 18 committed pass-22 section headings it renamed; inbox mentions: repos-2d.md). OPUS read these before packing.

## 002734B0 (60 B, extent 002734B0-002734EC)

Page context: "00276D30', '00279E20', '0029C770' call page-cited '00244960', '00245000', '00247870'); 15 outbound (page-cited '00276D30', '00276650', 'SaveLoad_ControllerLifecycleHandler' (00582860) call UI bodies '002734B0', '0035BB50', '002969E0'). Substantive edges include '00245000' is called by '0029C9D0'; '00245000' is called by '0029C770'; '00245000' is called by '002BF4F0'; '00245000' is called by '002BE450'; the remaining edges run through sh"

```
002734B0  push     rbx
002734B2  sub      rsp, 0x20
002734B6  xor      ebx, ebx
002734B8  call     0x35bb60  ; -> 0035BB60 fn
002734BD  test     eax, eax
002734BF  jle      0x2734d8  ; -> 002734D8
002734C1  mov      ecx, ebx
002734C3  call     0x35bb20  ; -> 0035BB20 fn
002734C8  test     byte ptr [rax], 4
002734CB  jne      0x2734e0  ; -> 002734E0
002734CD  inc      ebx
002734CF  call     0x35bb60  ; -> 0035BB60 fn
002734D4  cmp      ebx, eax
002734D6  jl       0x2734c1  ; -> 002734C1
002734D8  xor      eax, eax
002734DA  add      rsp, 0x20
002734DE  pop      rbx
002734DF  ret      
002734E0  mov      ecx, ebx
002734E2  add      rsp, 0x20
002734E6  pop      rbx
002734E7  jmp      0x35bb20  ; -> 0035BB20 fn
```

## 0050EEA0 (61 B, extent 0050EEA0-0050EEDD)

Page context: "calls '00582790'; the remaining edges run through shared helpers the page cites. - **Script_VM_Native_Bridge — CLIENT and SERVICE (45 edges).** 42 inbound (Script_VM_Native_Bridge bodies '0050F0A0', '0050EEA0', '0050D9A0' call page-cited 'Actor_GetWorldPosition' (00265020), 'ActorHandle_EncodeRegistryEntry' (003589B0), '00254CB0'); 3 outbound (page-cited '00266D10', '003444D0', '0050C910' call Script_VM_Native_Bridge bodies 'VMValueStac"

```
0050EEA0  mov      qword ptr [rsp + 8], rbx
0050EEA5  push     rdi
0050EEA6  sub      rsp, 0x20
0050EEAA  mov      rdi, rcx
0050EEAD  call     0x3bb420  ; -> 003BB420 fn
0050EEB2  xor      ecx, ecx
0050EEB4  mov      ebx, eax
0050EEB6  call     0x254cb0  ; -> 00254CB0 fn
0050EEBB  mov      edx, ebx
0050EEBD  lea      rcx, [rip + 0x813c14]  ; -> 00D22AD8
0050EEC4  call     0x17d280  ; -> 0017D280 fn
0050EEC9  mov      edx, ebx
0050EECB  mov      rcx, rdi
0050EECE  mov      rbx, qword ptr [rsp + 0x30]
0050EED3  add      rsp, 0x20
0050EED7  pop      rdi
0050EED8  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 0050F0A0 (61 B, extent 0050F0A0-0050F0DD)

Page context: " (00582860) calls '00582790'; the remaining edges run through shared helpers the page cites. - **Script_VM_Native_Bridge — CLIENT and SERVICE (45 edges).** 42 inbound (Script_VM_Native_Bridge bodies '0050F0A0', '0050EEA0', '0050D9A0' call page-cited 'Actor_GetWorldPosition' (00265020), 'ActorHandle_EncodeRegistryEntry' (003589B0), '00254CB0'); 3 outbound (page-cited '00266D10', '003444D0', '0050C910' call Script_VM_Native_Bridge bodies "

```
0050F0A0  mov      qword ptr [rsp + 8], rbx
0050F0A5  push     rdi
0050F0A6  sub      rsp, 0x20
0050F0AA  mov      rdi, rcx
0050F0AD  call     0x3bb420  ; -> 003BB420 fn
0050F0B2  mov      edx, eax
0050F0B4  lea      rcx, [rip + 0x8137a5]  ; -> 00D22860
0050F0BB  mov      ebx, eax
0050F0BD  call     0x17d280  ; -> 0017D280 fn
0050F0C2  mov      edx, ebx
0050F0C4  mov      rcx, rdi
0050F0C7  call     0x26b4e0  ; -> 0026B4E0 fn
0050F0CC  xor      ecx, ecx
0050F0CE  mov      rbx, qword ptr [rsp + 0x30]
0050F0D3  add      rsp, 0x20
0050F0D7  pop      rdi
0050F0D8  jmp      0x254cb0  ; -> 00254CB0 fn
```
