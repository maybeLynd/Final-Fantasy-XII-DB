# F-interior pack: `17-Presentation-Rendering/Legacy-PS2-GS/texture-mip-local-memory-budget.md`

Generated 2026-10-03 03:15 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/texture-mip-local-memory-budget.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 65f4854dd	SWE2-STRUCT pass-22 debt + OV31 narrowing: 77 crossing bullets across 21 docs (5 lane folders now re; inbox mentions: FABLE.md). OPUS read these before packing.

## 00342910 (71 B, extent 00342910-00342957)

Page context: "stentPayloadBase' ('002EF2B0') and 'SaveWrite_GetBusyFlag' ('00583920'). - **Script_VM_Native_Bridge - MECHANICAL (20 edges).** all 20 edges are script-VM bodies ('003415D0', '00341CB0', '00342250', '00342910', '00342EC0' and fifteen more) calling 'PartyRoster_GetActorBySlot' ('00263750') - fan-in on one roster accessor. - **CombatAI - CLIENT (1 edge).** 'AiOrder_EvaluateAndResolveActionTarget' ('003014C0') calls 'WorldActor_GetDefiniti"

```
00342910  mov      qword ptr [rsp + 8], rbx
00342915  mov      qword ptr [rsp + 0x10], rsi
0034291A  push     rdi
0034291B  sub      rsp, 0x20
0034291F  xor      esi, esi
00342921  lea      rdi, [r8 + 4]
00342925  mov      ebx, esi
00342927  mov      ecx, ebx
00342929  call     0x263750  ; -> 00263750 fn
0034292E  test     rax, rax
00342931  lea      rdi, [rdi + 1]
00342935  mov      ecx, 0xff
0034293A  cmovne   ecx, esi
0034293D  inc      ebx
0034293F  mov      byte ptr [rdi - 1], cl
00342942  cmp      ebx, 4
00342945  jl       0x342927  ; -> 00342927
00342947  mov      rbx, qword ptr [rsp + 0x30]
0034294C  mov      rsi, qword ptr [rsp + 0x38]
00342951  add      rsp, 0x20
00342955  pop      rdi
00342956  ret      
```
