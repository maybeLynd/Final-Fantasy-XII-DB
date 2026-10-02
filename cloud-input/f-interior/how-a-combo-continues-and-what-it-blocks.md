# F-interior pack: `07-Combat-Action/how-a-combo-continues-and-what-it-blocks.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/how-a-combo-continues-and-what-it-blocks.json`.

Functions: 2. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: b211e5678	SWE2-DATA: GR-3, GR-8, GR-9, GR-10 ANSWERED and GR-18 PARTIAL (the 4 GB .ard placement is ASTRA's ru; 797b72780	FABLE: DD content work on the 15 gameplay-folder owner-read pages - sections, cited claims, 40 corre; inbox mentions: repos-78.md). OPUS read these before packing.

## 0031B4B0 (52 B, extent 0031B4B0-0031B4E4)

Page context: "uickening or mount presentation in progress ([the mode ladder](../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md) §2d) |  Its only other caller, '0031ADB0' (reached through '0031B4B0', for which no static reference was found by 'E8' / 'E9', 'lea', qword or RVA — only its '.pdata' entry), publishes the answer as bit 1 of its output record's '+0x3C' when asked with flag '0x10' ('0031B0C4'–'0031B0DB').  **Test 3 —"

```
0031B4B0  mov      qword ptr [rsp + 8], rbx
0031B4B5  push     rdi
0031B4B6  sub      rsp, 0x20
0031B4BA  mov      rbx, r8
0031B4BD  mov      edi, edx
0031B4BF  test     rcx, rcx
0031B4C2  jne      0x31b4c8  ; -> 0031B4C8
0031B4C4  xor      eax, eax
0031B4C6  jmp      0x31b4cd  ; -> 0031B4CD
0031B4C8  call     0x263e30  ; -> 00263E30 fn
0031B4CD  mov      r8, rbx
0031B4D0  mov      edx, edi
0031B4D2  mov      rcx, rax
0031B4D5  mov      rbx, qword ptr [rsp + 0x30]
0031B4DA  add      rsp, 0x20
0031B4DE  pop      rdi
0031B4DF  jmp      0x31adb0  ; -> 0031ADB0 fn
```

## 003592C0 (103 B, extent 003592C0-00359327)

Page context: "AndReconcileRoster' '003273D0' call '00236820' (and '003273D0' '00236850'); '0023B040' calls '003272A0', 'PartyControl_SetMovementSuppressionBit' '00359200' and 'PartyControl_SetSuppressionMask1Bit' '003592C0', and '003272A0' calls it back; the gate '0030C010', '0030F760' and '0031ADB0' call 'BattleUnit_ResolveByFocusHandle' '0031B7E0'; '0031ADB0', '00325D90' and '003272A0' call 'PartyFocus_GetCurrentPackedActorHandle' '003590D0'. The c"

```
003592C0  sub      rsp, 0x28
003592C4  test     edx, edx
003592C6  je       0x3592da  ; -> 003592DA
003592C8  movzx    edx, byte ptr [rip + 0x1f6ed36]  ; -> 022C8005
003592CF  bts      edx, ecx
003592D2  mov      byte ptr [rip + 0x1f6ed2d], dl  ; -> 022C8005
003592D8  jmp      0x3592ed  ; -> 003592ED
003592DA  movzx    eax, byte ptr [rip + 0x1f6ed24]  ; -> 022C8005
003592E1  btr      eax, ecx
003592E4  movzx    edx, al
003592E7  mov      byte ptr [rip + 0x1f6ed18], al  ; -> 022C8005
003592ED  movzx    eax, byte ptr [rip + 0x1f6ed10]  ; -> 022C8004
003592F4  or       al, byte ptr [rip + 0x1f6ed0c]  ; -> 022C8006
003592FA  or       al, byte ptr [rip + 0x1f6ed07]  ; -> 022C8007
00359300  or       al, dl
00359302  test     al, 1
00359304  je       0x359322  ; -> 00359322
00359306  mov      ecx, dword ptr [rip + 0x1f6ecd4]  ; -> 022C7FE0
0035930C  call     0x3588b0  ; -> 003588B0 fn
00359311  test     rax, rax
00359314  je       0x359322  ; -> 00359322
00359316  mov      rcx, rax
00359319  add      rsp, 0x28
0035931D  jmp      0x26d6d0  ; -> 0026D6D0 fn
00359322  add      rsp, 0x28
00359326  ret      
```
