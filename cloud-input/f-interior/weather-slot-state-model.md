# F-interior pack: `03-World-Area-Field/Weather/weather-slot-state-model.md`

Generated 2026-10-02 18:41 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/weather-slot-state-model.json`.

Functions: 2. Each is cited on the page only at its entry and is still in the F frontier.

## 002509A0 (46 B, extent 002509A0-002509CE)

Page context: "y, no shared ownership. - **UI - CLIENT and SERVICE (7 edges).** '003148F0' is also called by bodies filed to UI: '0029C530', '003C5F00'; '00237DF0', '002678C0' reach bodies filed to UI: '00313840', '002509A0' - shared machinery across the layer boundary, no shared ownership.  ## 10. The transition contract — '0026D910' read end to end (2026-09-10)  §3 names 'WorldField_ApplyWeatherSlotAndDerivedEnvironmentState' the apply owner and §6 "

```
002509A0  mov      qword ptr [rsp + 8], rbx
002509A5  push     rdi
002509A6  sub      rsp, 0x20
002509AA  mov      ebx, edx
002509AC  mov      edi, ecx
002509AE  mov      edx, 1
002509B3  lea      ecx, [rdx + 0xb]
002509B6  call     0x35c880  ; -> 0035C880 fn
002509BB  mov      edx, ebx
002509BD  mov      ecx, edi
002509BF  mov      rbx, qword ptr [rsp + 0x30]
002509C4  add      rsp, 0x20
002509C8  pop      rdi
002509C9  jmp      0x28e5f0  ; -> 0028E5F0 fn
```

## 0050C990 (54 B, extent 0050C990-0050C9C6)

Page context: "ery across the layer boundary, no shared ownership. - **Script_VM_Native_Bridge - CLIENT (38 edges).** '0017D280' is also called by bodies filed to script VM / native bridge: '0050C670', '0050C8D0', '0050C990' - shared machinery across the layer boundary, no shared ownership. - **Story_Event_Quest_Hunt - CLIENT (12 edges).** '002EF2B0' is also called by bodies filed to story/event: '0032A8A0', '0032A930', '0032A9A0' - shared machinery a"

```
0050C990  mov      qword ptr [rsp + 8], rbx
0050C995  push     rdi
0050C996  sub      rsp, 0x20
0050C99A  mov      rdi, rcx
0050C99D  call     0x3bb420  ; -> 003BB420 fn
0050C9A2  mov      edx, eax
0050C9A4  lea      rcx, [rip + 0x815f25]  ; -> 00D228D0
0050C9AB  mov      ebx, eax
0050C9AD  call     0x17d280  ; -> 0017D280 fn
0050C9B2  mov      edx, ebx
0050C9B4  mov      rcx, rdi
0050C9B7  mov      rbx, qword ptr [rsp + 0x30]
0050C9BC  add      rsp, 0x20
0050C9C0  pop      rdi
0050C9C1  jmp      0x26b4e0  ; -> 0026B4E0 fn
```
