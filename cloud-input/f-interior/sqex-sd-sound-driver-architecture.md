# F-interior pack: `18-Audio/sqex-sd-sound-driver-architecture.md`

Generated 2026-10-03 02:49 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/sqex-sd-sound-driver-architecture.json`.

Functions: 2. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: cd6bd7f58	SWE2-DATA consolidated publish: progress-report cluster (generation store, R3 semantics, DB_GOAL, me; f7a3292bd	SWE2-DATA: DD owner read of eight Input, Audio and Save pages - sections filled, claims anchored or ; inbox mentions: FABLE.md, SWE2-AUDIT-SPEC.md, repos-78.md). OPUS read these before packing.

## 001DBA60 (45 B, extent 001DBA60-001DBA8D)

Page context: " clamps the value to '0..100', stores it         as a word at '+0x08' / '+0x0A' / '+0x0C' of the saved options record '*(0215E6E0)', and passes 'value / 100.0'         with category **1 / 2 / 3** to '001DBA60' (thunk '002DF2B0') → '00210ED0'. '00210ED0' queues SEAD action         type 3 with layer 0 and fade 0 through '007A45C0'.       - **The category numbers are named.** The debug menu labels its three category mute toggles ('001D1660"

```
001DBA60  push     rbx
001DBA62  sub      rsp, 0x30
001DBA66  movaps   xmmword ptr [rsp + 0x20], xmm6
001DBA6B  mov      ebx, edx
001DBA6D  movaps   xmm6, xmm0
001DBA70  call     0x210b30  ; -> 00210B30 fn
001DBA75  mov      rcx, rax
001DBA78  mov      r8d, ebx
001DBA7B  movaps   xmm1, xmm6
001DBA7E  movaps   xmm6, xmmword ptr [rsp + 0x20]
001DBA83  add      rsp, 0x30
001DBA87  pop      rbx
001DBA88  jmp      0x210ed0  ; -> 00210ED0 fn
```

## 003456E0 (83 B, extent 003456E0-00345733)

Page context: "nery across the layer boundary, no shared ownership. - **Script_VM_Native_Bridge - CLIENT (7 edges).** '003601B0' is also called by bodies filed to script VM / native bridge: '00342C90', '00344C60', '003456E0' (+4 more) - shared machinery across the layer boundary, no shared ownership. - **UI - CLIENT (16 edges).** '00203080', '00202C70', '0036DD80' are also called by bodies filed to UI: '002AF960', '002D2600', '002D28E0' (+13 more) - s"

```
003456E0  mov      qword ptr [rsp + 8], rbx
003456E5  push     rdi
003456E6  sub      rsp, 0x20
003456EA  mov      rcx, r9
003456ED  call     0x267e10  ; -> 00267E10 fn
003456F2  mov      ecx, eax
003456F4  mov      edi, eax
003456F6  call     0x473b90  ; -> 00473B90 fn
003456FB  mov      edx, 3
00345700  xor      ecx, ecx
00345702  mov      ebx, eax
00345704  call     0x2e1cd0  ; -> 002E1CD0 fn
00345709  test     ebx, ebx
0034570B  jns      0x345716  ; -> 00345716
0034570D  xor      ecx, ecx
0034570F  call     0x473b90  ; -> 00473B90 fn
00345714  mov      ebx, eax
00345716  mov      ecx, 0xd
0034571B  call     0x3601b0  ; -> 003601B0 fn
00345720  mov      edx, ebx
00345722  mov      ecx, edi
00345724  mov      rbx, qword ptr [rsp + 0x30]
00345729  add      rsp, 0x20
0034572D  pop      rdi
0034572E  jmp      0x17e7d0  ; -> 0017E7D0 fn
```
