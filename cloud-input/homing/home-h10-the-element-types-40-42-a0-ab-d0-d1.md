# Homing pack: `17-Presentation-Rendering/Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md`

Generated 2026-10-03 12:18 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h10-the-element-types-40-42-a0-ab-d0-d1.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00264420 (58 B, extent 00264420-0026445A)

Entered from (direct sites whose caller this page cites): `00345430` + 0x3C (call; `00345430` is cited on this page)
Other direct sites: `00345CD0` + 0x89 (call)

Host context: "FA0'/'Movement_IntegratePositionAndMeasureDisplacement' share '003589B0'; ten movement bodies ('Movement_UpdateSteeringTowardTarget', 'BattleUnit_CanAdvanceCombatNavigation', '0026C3E0', '0026D810', '00345430', '00319490', '002E5180', '00326BB0', …) share '003590D0'; '001EDDA0' is shared with 'WorldActor_UpdateRuntimeAndScriptExecutionState'.  **Party — MECHANICAL (SWE2-CONTRACT 2026-09-15, 12 edges).** 'PartyRoster_AssignActorToSlot' s"

```
00264420  sub      rsp, 0x28
00264424  mov      rax, qword ptr [rcx + 0xc0]
0026442B  test     rax, rax
0026442E  je       0x264447  ; -> 00264447
00264430  movzx    edx, byte ptr [rax + 0x154]
00264437  test     dl, 2
0026443A  je       0x264447  ; -> 00264447
0026443C  movzx    eax, dl
0026443F  and      eax, 1
00264442  add      rsp, 0x28
00264446  ret      
00264447  call     0x30bfb0  ; -> 0030BFB0 fn
0026444C  xor      ecx, ecx
0026444E  test     eax, eax
00264450  setne    cl
00264453  mov      eax, ecx
00264455  add      rsp, 0x28
00264459  ret      
```

## 00376990 (71 B, extent 00376990-003769D7)

Entered from (direct sites whose caller this page cites): `00461250` + 0x13 (jmp; `00461250` is cited on this page)
Other direct sites: none

Host context: "3010' | | '0xA1' | step '00461090' (441 B heavy), walk '00461270' **3820 B** — the largest walk in the whole matrix | calls '001827B0'/'00182830' and the '00376350'–'00377100' helper family; seventh '00461250' touches '+0x1B4'/'+0x294'; setup has a resource store + '+0x1B0'/'+0x1B1' flag bytes | | '0xA2' | step '00462480' (177 B, '003D8E50'-family), walk '00462540' 2921 B | '0017FFD0'+'0024E2E0'/'0024E460'/'0024E640' VU0-path calls; set"

```
00376990  test     ecx, ecx
00376992  je       0x3769d6  ; -> 003769D6
00376994  push     rbx
00376995  sub      rsp, 0x20
00376999  movzx    edx, cl
0037699C  lea      rax, [rip + 0x276519d]  ; -> 02ADBB40
003769A3  lea      rbx, [rdx + rdx*8]
003769A7  shl      rbx, 4
003769AB  add      rbx, rax
003769AE  cmp      dword ptr [rbx], ecx
003769B0  jne      0x3769d1  ; -> 003769D1
003769B2  dec      byte ptr [rip + 0x2765178]  ; -> 02ADBB30
003769B8  mov      dword ptr [rbx], 0
003769BE  mov      ecx, dword ptr [rbx + 0x50]
003769C1  test     ecx, ecx
003769C3  je       0x3769ca  ; -> 003769CA
003769C5  call     0x3abca0  ; -> 003ABCA0 fn
003769CA  mov      dword ptr [rbx + 0x50], 0
003769D1  add      rsp, 0x20
003769D5  pop      rbx
003769D6  ret      
```
