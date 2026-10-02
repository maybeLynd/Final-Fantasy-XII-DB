# F-interior pack: `10-Status-Periodic-Terminal/where-mp-comes-from.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/where-mp-comes-from.json`.

Functions: 13. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 7903502f7	FABLE: pass-22 debt - crossing sections on 94 pages (FABLE's group; 12 overlay-carrier pages routed ). OPUS read these before packing.

## 00238640 (19 B, extent 00238640-00238653)

Page context: "NDENCY (16 edges).** '00236C30' calls '003845F0' and '003846F0', is called by '00238850', and calls '003847B0'; '003845F0' is called by '00236C30', 'BattleData_SetAreaArdSectionCategory' '0023A160', '00238640' and '003847B0', and calls '003846F0'; the zone-multiplier getter '00377BA0' calls 'WorldTransition_GetActiveOrPendingFieldId' '003148F0', '00314AA0' and '00314AC0'; '00307300' calls 'FieldData_GetActiveFieldRecordBit15' '00377C20'"

```
00238640  movsxd   rax, ecx
00238643  lea      rcx, [rip + 0x2d5ed76]  ; -> 02F973C0
0023864A  lea      rcx, [rcx + rax*8]
0023864E  jmp      0x3845f0  ; -> 003845F0 fn
```

## 00300500 (28 B, extent 00300500-0030051C)

Page context: " 'GameState_GetGil' '00253690' and (all but the check) 'GameState_SetGil' '00254EE0'; those two are also called by 'GameState_AddGilClampedAndNotify' '003004B0', 'GameState_SetGilClampedNonnegative' '00300500', 'BattleUnit_ProcessDefeatRewardsAndLoot' '00312280' and '003F4AA0'. A gil-costed action checks, reserves, spends and refunds through the economy layer's gil balance, the same balance defeat rewards credit.  **Script_VM_Native_Bri"

```
00300500  push     rbx
00300502  sub      rsp, 0x20
00300506  xor      ebx, ebx
00300508  test     ecx, ecx
0030050A  cmovns   ebx, ecx
0030050D  mov      ecx, ebx
0030050F  call     0x254ee0  ; -> 00254EE0 fn
00300514  mov      eax, ebx
00300516  add      rsp, 0x20
0030051A  pop      rbx
0030051B  ret      
```

## 00341140 (75 B, extent 00341140-0034118B)

Page context: "y layer's gil balance, the same balance defeat rewards credit.  **Script_VM_Native_Bridge — CLIENT (20 edges).** The 'setmpratiomode' bodies '00473A00' and '00473A90' are called by the verb handlers '00341140', '00341EE0', '00349620', '0034A4C0', '00341690', '00342500' and '00349AD0'; '003589B0' is called by twelve verb bodies ('00342150', '00342D40', '003438F0' and nine more); '008632B0' is called by one more verb body. Script verbs se"

```
00341140  mov      qword ptr [rsp + 8], rbx
00341145  mov      qword ptr [rsp + 0x10], rsi
0034114A  push     rdi
0034114B  sub      rsp, 0x20
0034114F  mov      rcx, rdx
00341152  mov      rsi, r9
00341155  call     0x263f10  ; -> 00263F10 fn
0034115A  mov      rcx, rsi
0034115D  mov      rdi, rax
00341160  call     0x267e10  ; -> 00267E10 fn
00341165  mov      rcx, rsi
00341168  mov      ebx, eax
0034116A  call     0x267e10  ; -> 00267E10 fn
0034116F  mov      r8d, ebx
00341172  mov      edx, eax
00341174  mov      rcx, rdi
00341177  mov      rbx, qword ptr [rsp + 0x30]
0034117C  mov      rsi, qword ptr [rsp + 0x38]
00341181  add      rsp, 0x20
00341185  pop      rdi
00341186  jmp      0x473a00  ; -> 00473A00 fn
```

## 00341690 (75 B, extent 00341690-003416DB)

Page context: "ewards credit.  **Script_VM_Native_Bridge — CLIENT (20 edges).** The 'setmpratiomode' bodies '00473A00' and '00473A90' are called by the verb handlers '00341140', '00341EE0', '00349620', '0034A4C0', '00341690', '00342500' and '00349AD0'; '003589B0' is called by twelve verb bodies ('00342150', '00342D40', '003438F0' and nine more); '008632B0' is called by one more verb body. Script verbs set the MP-ratio mode this page reads in section 5"

```
00341690  mov      qword ptr [rsp + 8], rbx
00341695  mov      qword ptr [rsp + 0x10], rsi
0034169A  push     rdi
0034169B  sub      rsp, 0x20
0034169F  mov      rcx, rdx
003416A2  mov      rsi, r9
003416A5  call     0x263f10  ; -> 00263F10 fn
003416AA  mov      rcx, rsi
003416AD  mov      rdi, rax
003416B0  call     0x267e10  ; -> 00267E10 fn
003416B5  mov      rcx, rsi
003416B8  mov      ebx, eax
003416BA  call     0x267e10  ; -> 00267E10 fn
003416BF  mov      r8d, ebx
003416C2  mov      edx, eax
003416C4  mov      rcx, rdi
003416C7  mov      rbx, qword ptr [rsp + 0x30]
003416CC  mov      rsi, qword ptr [rsp + 0x38]
003416D1  add      rsp, 0x20
003416D5  pop      rdi
003416D6  jmp      0x473a90  ; -> 00473A90 fn
```

## 00341EE0 (91 B, extent 00341EE0-00341F3B)

Page context: "l balance, the same balance defeat rewards credit.  **Script_VM_Native_Bridge — CLIENT (20 edges).** The 'setmpratiomode' bodies '00473A00' and '00473A90' are called by the verb handlers '00341140', '00341EE0', '00349620', '0034A4C0', '00341690', '00342500' and '00349AD0'; '003589B0' is called by twelve verb bodies ('00342150', '00342D40', '003438F0' and nine more); '008632B0' is called by one more verb body. Script verbs set the MP-rat"

```
00341EE0  mov      qword ptr [rsp + 8], rbx
00341EE5  mov      qword ptr [rsp + 0x10], rsi
00341EEA  push     rdi
00341EEB  sub      rsp, 0x20
00341EEF  mov      rbx, rdx
00341EF2  mov      rcx, r9
00341EF5  mov      edx, 2
00341EFA  mov      rsi, r9
00341EFD  call     0x267f90  ; -> 00267F90 fn
00341F02  mov      rcx, rbx
00341F05  call     0x263f10  ; -> 00263F10 fn
00341F0A  mov      rcx, rsi
00341F0D  mov      rdi, rax
00341F10  call     0x267e10  ; -> 00267E10 fn
00341F15  mov      rcx, rsi
00341F18  mov      ebx, eax
00341F1A  call     0x267e10  ; -> 00267E10 fn
00341F1F  mov      r8d, ebx
00341F22  mov      edx, eax
00341F24  mov      rcx, rdi
00341F27  mov      rbx, qword ptr [rsp + 0x30]
00341F2C  mov      rsi, qword ptr [rsp + 0x38]
00341F31  add      rsp, 0x20
00341F35  pop      rdi
00341F36  jmp      0x473a00  ; -> 00473A00 fn
```

## 00342150 (90 B, extent 00342150-003421AA)

Page context: "e' bodies '00473A00' and '00473A90' are called by the verb handlers '00341140', '00341EE0', '00349620', '0034A4C0', '00341690', '00342500' and '00349AD0'; '003589B0' is called by twelve verb bodies ('00342150', '00342D40', '003438F0' and nine more); '008632B0' is called by one more verb body. Script verbs set the MP-ratio mode this page reads in section 5, and share the handle encoder and the achievement notify gate; only the first is a"

```
00342150  mov      qword ptr [rsp + 8], rbx
00342155  mov      qword ptr [rsp + 0x10], rsi
0034215A  push     rdi
0034215B  sub      rsp, 0x20
0034215F  mov      rsi, rcx
00342162  xor      edi, edi
00342164  mov      rcx, rdx
00342167  call     0x263f10  ; -> 00263F10 fn
0034216C  mov      rbx, rax
0034216F  call     0x3d9fe0  ; -> 003D9FE0 fn
00342174  test     eax, eax
00342176  je       0x342191  ; -> 00342191
00342178  mov      rcx, rbx
0034217B  call     0x3589b0  ; -> 003589B0 fn
00342180  mov      ebx, eax
00342182  call     0x3d9fa0  ; -> 003D9FA0 fn
00342187  cmp      ebx, eax
00342189  mov      ecx, 1
0034218E  cmove    edi, ecx
00342191  mov      edx, edi
00342193  mov      rcx, rsi
00342196  mov      rbx, qword ptr [rsp + 0x30]
0034219B  mov      rsi, qword ptr [rsp + 0x38]
003421A0  add      rsp, 0x20
003421A4  pop      rdi
003421A5  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 00342500 (91 B, extent 00342500-0034255B)

Page context: "t.  **Script_VM_Native_Bridge — CLIENT (20 edges).** The 'setmpratiomode' bodies '00473A00' and '00473A90' are called by the verb handlers '00341140', '00341EE0', '00349620', '0034A4C0', '00341690', '00342500' and '00349AD0'; '003589B0' is called by twelve verb bodies ('00342150', '00342D40', '003438F0' and nine more); '008632B0' is called by one more verb body. Script verbs set the MP-ratio mode this page reads in section 5, and share "

```
00342500  mov      qword ptr [rsp + 8], rbx
00342505  mov      qword ptr [rsp + 0x10], rsi
0034250A  push     rdi
0034250B  sub      rsp, 0x20
0034250F  mov      rbx, rdx
00342512  mov      rcx, r9
00342515  mov      edx, 2
0034251A  mov      rsi, r9
0034251D  call     0x267f90  ; -> 00267F90 fn
00342522  mov      rcx, rbx
00342525  call     0x263f10  ; -> 00263F10 fn
0034252A  mov      rcx, rsi
0034252D  mov      rdi, rax
00342530  call     0x267e10  ; -> 00267E10 fn
00342535  mov      rcx, rsi
00342538  mov      ebx, eax
0034253A  call     0x267e10  ; -> 00267E10 fn
0034253F  mov      r8d, ebx
00342542  mov      edx, eax
00342544  mov      rcx, rdi
00342547  mov      rbx, qword ptr [rsp + 0x30]
0034254C  mov      rsi, qword ptr [rsp + 0x38]
00342551  add      rsp, 0x20
00342555  pop      rdi
00342556  jmp      0x473a90  ; -> 00473A90 fn
```

## 00342D40 (49 B, extent 00342D40-00342D71)

Page context: "0473A00' and '00473A90' are called by the verb handlers '00341140', '00341EE0', '00349620', '0034A4C0', '00341690', '00342500' and '00349AD0'; '003589B0' is called by twelve verb bodies ('00342150', '00342D40', '003438F0' and nine more); '008632B0' is called by one more verb body. Script verbs set the MP-ratio mode this page reads in section 5, and share the handle encoder and the achievement notify gate; only the first is an MP relatio"

```
00342D40  push     rbx
00342D42  sub      rsp, 0x20
00342D46  mov      rbx, rcx
00342D49  mov      rcx, rdx
00342D4C  call     0x263f10  ; -> 00263F10 fn
00342D51  mov      rcx, rax
00342D54  call     0x3589b0  ; -> 003589B0 fn
00342D59  xor      edx, edx
00342D5B  mov      ecx, eax
00342D5D  call     0x320790  ; -> 00320790 fn
00342D62  mov      edx, eax
00342D64  mov      rcx, rbx
00342D67  add      rsp, 0x20
00342D6B  pop      rbx
00342D6C  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 003438F0 (52 B, extent 003438F0-00343924)

Page context: " '00473A90' are called by the verb handlers '00341140', '00341EE0', '00349620', '0034A4C0', '00341690', '00342500' and '00349AD0'; '003589B0' is called by twelve verb bodies ('00342150', '00342D40', '003438F0' and nine more); '008632B0' is called by one more verb body. Script verbs set the MP-ratio mode this page reads in section 5, and share the handle encoder and the achievement notify gate; only the first is an MP relationship.  **Wo"

```
003438F0  push     rbx
003438F2  sub      rsp, 0x20
003438F6  mov      rbx, rcx
003438F9  mov      rcx, rdx
003438FC  call     0x263f10  ; -> 00263F10 fn
00343901  mov      rcx, rax
00343904  call     0x3589b0  ; -> 003589B0 fn
00343909  mov      edx, 1
0034390E  mov      ecx, eax
00343910  call     0x320790  ; -> 00320790 fn
00343915  mov      edx, eax
00343917  mov      rcx, rbx
0034391A  add      rsp, 0x20
0034391E  pop      rbx
0034391F  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 0034A4C0 (102 B, extent 0034A4C0-0034A526)

Page context: "nce defeat rewards credit.  **Script_VM_Native_Bridge — CLIENT (20 edges).** The 'setmpratiomode' bodies '00473A00' and '00473A90' are called by the verb handlers '00341140', '00341EE0', '00349620', '0034A4C0', '00341690', '00342500' and '00349AD0'; '003589B0' is called by twelve verb bodies ('00342150', '00342D40', '003438F0' and nine more); '008632B0' is called by one more verb body. Script verbs set the MP-ratio mode this page reads "

```
0034A4C0  mov      qword ptr [rsp + 8], rbx
0034A4C5  mov      qword ptr [rsp + 0x10], rsi
0034A4CA  push     rdi
0034A4CB  sub      rsp, 0x20
0034A4CF  mov      edx, 2
0034A4D4  mov      rcx, r9
0034A4D7  mov      rsi, r9
0034A4DA  call     0x267f90  ; -> 00267F90 fn
0034A4DF  mov      rcx, rsi
0034A4E2  call     0x267e10  ; -> 00267E10 fn
0034A4E7  mov      rcx, rsi
0034A4EA  mov      edi, eax
0034A4EC  call     0x267e10  ; -> 00267E10 fn
0034A4F1  mov      rcx, rsi
0034A4F4  mov      ebx, eax
0034A4F6  call     0x267e10  ; -> 00267E10 fn
0034A4FB  mov      ecx, eax
0034A4FD  call     0x264010  ; -> 00264010 fn
0034A502  mov      rcx, rax
0034A505  call     0x263f10  ; -> 00263F10 fn
0034A50A  mov      r8d, edi
0034A50D  mov      edx, ebx
0034A50F  mov      rcx, rax
0034A512  mov      rbx, qword ptr [rsp + 0x30]
0034A517  mov      rsi, qword ptr [rsp + 0x38]
0034A51C  add      rsp, 0x20
0034A520  pop      rdi
0034A521  jmp      0x473a00  ; -> 00473A00 fn
```

## 00353530 (86 B, extent 00353530-00353586)

Page context: "89B0' is called by the roster and focus bodies 'PartyRoster_AssignActorToSlot' '00269C70', 'PartyFocus_SelectAndRequestDefaultActor' '00326500', 'VMPartyCommand_SetSecondaryFocusActorFromActorIndex' '00353530', 'PartyRoster_AssignActorAndCommitFocusWhenEligible' '0050C610' and 'PartyFocus_EncodeActorAndSetTemporaryControlledActorOverride' '0050D2F0'. The action-state step resolves the unit's focus and asks whether it is the player's; th"

```
00353530  mov      qword ptr [rsp + 8], rbx
00353535  push     rdi
00353536  sub      rsp, 0x20
0035353A  mov      rcx, r9
0035353D  mov      rbx, r9
00353540  call     0x267e10  ; -> 00267E10 fn
00353545  mov      rcx, rbx
00353548  mov      edi, eax
0035354A  call     0x267e10  ; -> 00267E10 fn
0035354F  test     eax, eax
00353551  je       0x353573  ; -> 00353573
00353553  mov      ecx, edi
00353555  call     0x264010  ; -> 00264010 fn
0035355A  mov      rcx, rax
0035355D  call     0x3589b0  ; -> 003589B0 fn
00353562  mov      ecx, eax
00353564  mov      rbx, qword ptr [rsp + 0x30]
00353569  add      rsp, 0x20
0035356D  pop      rdi
0035356E  jmp      0x359410  ; -> 00359410 fn
00353573  xor      eax, eax
00353575  mov      ecx, eax
00353577  mov      rbx, qword ptr [rsp + 0x30]
0035357C  add      rsp, 0x20
00353580  pop      rdi
00353581  jmp      0x359410  ; -> 00359410 fn
```

## 00473A90 (123 B, extent 00473A90-00473B0B)

Page context: "'), 'BattleStats_ReconcileResourcesToEffectiveCapacity' '0x217' ('0030F5F7').   The one path that can clear it is the script's: 'setmp' / 'setmpmode' / 'setmpratio' /   'setmpratiomode' ('00473A00', '00473A90' → '00329B70' → '00329BD0', mode 1) build the flags from   the verb's option word — bit 0 → suppress flag bit 1, **bit 1 → let the reaction publisher run**   (flag bit 4 clear, '00329C0B'–'00329C15'), bit 2 → suppress flag bit 2 — "

```
00473A90  mov      qword ptr [rsp + 8], rbx
00473A95  mov      qword ptr [rsp + 0x10], rsi
00473A9A  push     rdi
00473A9B  sub      rsp, 0x20
00473A9F  mov      r9d, r8d
00473AA2  mov      eax, r8d
00473AA5  and      r9d, 1
00473AA9  mov      edi, r8d
00473AAC  shl      r9d, 0x1c
00473AB0  mov      esi, edx
00473AB2  mov      ebx, r9d
00473AB5  bts      ebx, 0x1d
00473AB9  and      al, 2
00473ABB  cmove    ebx, r9d
00473ABF  and      edi, 4
00473AC2  test     rcx, rcx
00473AC5  je       0x473af8  ; -> 00473AF8
00473AC7  call     0x3589b0  ; -> 003589B0 fn
00473ACC  mov      r9d, ebx
00473ACF  mov      r8d, esi
00473AD2  bts      r9d, 0x1e
00473AD7  mov      edx, 1
00473ADC  test     edi, edi
00473ADE  mov      ecx, eax
00473AE0  cmove    r9d, ebx
00473AE4  mov      rbx, qword ptr [rsp + 0x30]
00473AE9  mov      rsi, qword ptr [rsp + 0x38]
00473AEE  add      rsp, 0x20
00473AF2  pop      rdi
00473AF3  jmp      0x329b70  ; -> 00329B70 fn
00473AF8  mov      rbx, qword ptr [rsp + 0x30]
00473AFD  or       eax, 0xffffffff
00473B00  mov      rsi, qword ptr [rsp + 0x38]
00473B05  add      rsp, 0x20
00473B09  pop      rdi
00473B0A  ret      
```

## 0050D2F0 (23 B, extent 0050D2F0-0050D307)

Page context: "', 'VMPartyCommand_SetSecondaryFocusActorFromActorIndex' '00353530', 'PartyRoster_AssignActorAndCommitFocusWhenEligible' '0050C610' and 'PartyFocus_EncodeActorAndSetTemporaryControlledActorOverride' '0050D2F0'. The action-state step resolves the unit's focus and asks whether it is the player's; the handle encoder, which the 'setmpratiomode' body '00473A00' also calls, is shared with roster code.  **Resource — SERVICE (2 edges).** '00236"

```
0050D2F0  sub      rsp, 0x28
0050D2F4  mov      rcx, rdx
0050D2F7  call     0x3589b0  ; -> 003589B0 fn
0050D2FC  mov      ecx, eax
0050D2FE  add      rsp, 0x28
0050D302  jmp      0x3593a0  ; -> 003593A0 fn
```
