# F-interior pack: `18-Audio/CONTRACT-field-music-selection.md`

Generated 2026-10-02 20:44 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/contract-field-music-selection.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: cd6bd7f58	SWE2-DATA consolidated publish: progress-report cluster (generation store, R3 semantics, DB_GOAL, me; inbox mentions: FABLE.md). OPUS read these before packing.

## 00343710 (48 B, extent 00343710-00343740)

Page context: "'00583920' - shared machinery across the layer boundary, no shared ownership. - **Script_VM_Native_Bridge - CLIENT (1 edge).** '0026DEF0' is also called by bodies filed to script VM / native bridge: '00343710' - shared machinery across the layer boundary, no shared ownership. - **Status_Periodic_Terminal - CLIENT (5 edges).** '0031B860' is also called by bodies filed to status/periodic terminal: '002F9400', '0030E360', '0030F690' (+2 mo"

```
00343710  sub      rsp, 0x28
00343714  mov      rcx, r9
00343717  call     0x267e10  ; -> 00267E10 fn
0034371C  mov      ecx, eax
0034371E  call     0x26def0  ; -> 0026DEF0 fn
00343723  test     eax, eax
00343725  jns      0x34373b  ; -> 0034373B
00343727  mov      edx, 1
0034372C  or       ecx, 0xffffffff
0034372F  mov      r8d, edx
00343732  add      rsp, 0x28
00343736  jmp      0x361200  ; -> 00361200 fn
0034373B  add      rsp, 0x28
0034373F  ret      
```
