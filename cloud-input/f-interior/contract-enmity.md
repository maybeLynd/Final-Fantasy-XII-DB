# F-interior pack: `09-Combat-AI-And-Gambits/CONTRACT-enmity.md`

Generated 2026-10-02 20:18 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/contract-enmity.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

## 0030B510 (93 B, extent 0030B510-0030B56D)

Page context: "ipment_Shops_License — MECHANICAL (13 edges).** '00322C50' is called by 'Equipment_CheckMatchingSecondaryPartnerSelectedOrOwned' '003096F0', the class-D purchase-flag helpers '0030B180', '0030B4B0', '0030B510', '0030B570', '0030B630', 'Equipment_CheckItemEligibleForSlot' '00317930', 'BattleStats_SetEquipmentSlotByMappedId' '0031A510', the licence bodies '00323910', '00323C60', '00323D10', '00323EC0' and 'InventoryDerivedIndex_UpdateOnPr"

```
0030B510  push     rbx
0030B512  sub      rsp, 0x20
0030B516  movzx    eax, cx
0030B519  movzx    ebx, cx
0030B51C  mov      ecx, 0xf000
0030B521  and      ax, cx
0030B524  mov      ecx, 0xd000
0030B529  cmp      ax, cx
0030B52C  je       0x30b536  ; -> 0030B536
0030B52E  xor      eax, eax
0030B530  add      rsp, 0x20
0030B534  pop      rbx
0030B535  ret      
0030B536  mov      ecx, 1
0030B53B  movzx    edx, bx
0030B53E  mov      r8d, ecx
0030B541  call     0x322c50  ; -> 00322C50 fn
0030B546  test     eax, eax
0030B548  je       0x30b52e  ; -> 0030B52E
0030B54A  mov      rax, qword ptr [rip + 0x2bb3c3f]  ; -> 02EBF190
0030B551  movzx    ecx, bx
0030B554  and      ecx, 0xfff
0030B55A  movzx    eax, byte ptr [rcx + rax + 0x59c8]
0030B562  shr      eax, 1
0030B564  and      eax, 1
0030B567  add      rsp, 0x20
0030B56B  pop      rbx
0030B56C  ret      
```
