# F-interior pack: `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md`

Generated 2026-10-03 03:15 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/how-the-ard-loader-binds-area-battle-data.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: de4492e21	SWE2-CONTRACT: pass-22 debt final - six-folder worklist (597 pairs) fully dispositioned, 0 live find; 01c2429f6	SWE2-CONTRACT: pass-22 debt batch B - 47 Script-VM, Resource, EBP and PKFL pages' cross-subsystem ne; inbox mentions: SWE2-AUDIT-SPEC.md, repos-1e.md, repos-4b.md). OPUS read these before packing.

## 003414A0 (57 B, extent 003414A0-003414D9)

Page context: "s include 'BattleUnit_SelectAiOrderSetVariantFromAuthoredUnit' (00239040) is called by 'VM_BattleUnit_SelectAiOrderSetVariant' (00510580); '002E99C0' is called by '00340FA0'; '002E99C0' is called by '003414A0'; the remaining edges run through shared helpers the page cites. - **Spawn_Encounter_Lifecycle — CLIENT and SERVICE (2 edges).** 1 inbound (Spawn_Encounter_Lifecycle bodies 'Spawn_ApplyScriptSelectedUnit' (0023A3B0) call page-cited"

```
003414A0  push     rbx
003414A2  sub      rsp, 0x20
003414A6  mov      rcx, r9
003414A9  mov      rbx, r8
003414AC  call     0x267e10  ; -> 00267E10 fn
003414B1  mov      ecx, eax
003414B3  call     0x2e9a60  ; -> 002E9A60 fn
003414B8  mov      ecx, eax
003414BA  mov      dword ptr [rbx], eax
003414BC  call     0x2e99c0  ; -> 002E99C0 fn
003414C1  mov      rcx, rax
003414C4  call     0x2e9810  ; -> 002E9810 fn
003414C9  mov      dword ptr [rbx + 4], eax
003414CC  mov      dword ptr [rbx + 8], 0
003414D3  add      rsp, 0x20
003414D7  pop      rbx
003414D8  ret      
```
