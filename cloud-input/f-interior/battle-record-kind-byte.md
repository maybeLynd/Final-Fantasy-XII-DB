# F-interior pack: `04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md`

Generated 2026-10-02 18:33 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/battle-record-kind-byte.json`.

Functions: 5. Each is cited on the page only at its entry and is still in the F frontier.

## 00235AB0 (61 B, extent 00235AB0-00235AED)

Page context: "*So the idiom is a two-byte discriminator, not a lone range check:**  '''c if (rec[5] == 0 && (uint8_t)(rec[4] - 0x1B) <= 0x0C) { ... }   /* 13 kinds */ '''  The 22 functions span spawn ('00233A20', '00235AB0', '00237EA0'), rewards ('Reward_ComputeExperienceForRecipient', twice), stats ('BattleStats_RebuildEffectiveStatsAndAffinityState', 'BattleStats_ChangeStatusAndProcessSideEffects', 'BattleStats_ReconcileCurrentHpToEffectiveMaximum'"

```
00235AB0  sub      rsp, 0x28
00235AB4  call     0x3272a0  ; -> 003272A0 fn
00235AB9  test     rax, rax
00235ABC  je       0x235ae6  ; -> 00235AE6
00235ABE  mov      rcx, qword ptr [rax + 0x698]
00235AC5  test     rcx, rcx
00235AC8  je       0x235ae6  ; -> 00235AE6
00235ACA  movzx    eax, byte ptr [rcx + 5]
00235ACE  test     eax, eax
00235AD0  jne      0x235ae6  ; -> 00235AE6
00235AD2  movzx    eax, byte ptr [rcx + 4]
00235AD6  sub      al, 0x1b
00235AD8  cmp      al, 0xc
00235ADA  ja       0x235ae6  ; -> 00235AE6
00235ADC  mov      eax, 1
00235AE1  add      rsp, 0x28
00235AE5  ret      
00235AE6  xor      eax, eax
00235AE8  add      rsp, 0x28
00235AEC  ret      
```

## 0026AA60 (97 B, extent 0026AA60-0026AAC1)

Page context: " resolve units through '0031B760', '0031B770' and '0031B860'. In the service direction, the actor-record initializer '00265FF0', which seeds the nibble to 4 or 5 (AL-3), calls five movement setters: '0026AA60', 'Movement_SetRequestedSpeed' '0026D6F0', '003DA830', '003DA860' and '003DA890'. '00237EA0', one of the '+4'-band functions of §11, calls '002E64E0'. Movement reads unit identity and the target nibble through this page's accessors"

```
0026AA60  movaps   xmm3, xmm1
0026AA63  xorps    xmm0, xmm0
0026AA66  comiss   xmm3, xmm0
0026AA69  jb       0x26aa75  ; -> 0026AA75
0026AA6B  movss    xmm4, dword ptr [rip + 0x1a811dd]  ; -> 01CEBC50 [f32 3.141593]
0026AA73  jmp      0x26aa7d  ; -> 0026AA7D
0026AA75  movss    xmm4, dword ptr [rip + 0x6aaba3]  ; -> 00915620 [f32 -3.141593]
0026AA7D  movzx    eax, byte ptr [rcx + 3]
0026AA81  addss    xmm3, xmm4
0026AA85  and      al, 0xe0
0026AA87  cmp      al, 0x60
0026AA89  jne      0x26aac0  ; -> 0026AAC0
0026AA8B  movaps   xmm0, xmm3
0026AA8E  divss    xmm0, dword ptr [rip + 0x1a811e2]  ; -> 01CEBC78 [f32 6.283185]
0026AA96  cvttss2si eax, xmm0
0026AA9A  movd     xmm1, eax
0026AA9E  mov      rax, qword ptr [rcx + 0xb8]
0026AAA5  cvtdq2ps xmm1, xmm1
0026AAA8  mulss    xmm1, dword ptr [rip + 0x1a811c8]  ; -> 01CEBC78 [f32 6.283185]
0026AAB0  subss    xmm3, xmm1
0026AAB4  subss    xmm3, xmm4
0026AAB8  movss    dword ptr [rax + 0xb0], xmm3
0026AAC0  ret      
```

## 00273910 (56 B, extent 00273910-00273948)

Page context: "either friendly nor hostile — when either side is **5** ('0030AB93'–'0030ABA0');       the field cursor's helpers accept **1–2** ('00273750'), **1–3** ('002734F0'), **3** with       '003229A0 == 0' ('00273910') and **5** ('00273A00'); this page's '002F8E90' maps **3 → 4** and       **1, 2, 7 → 8** for enemy-table units, which is why the loot thief message keys on 8. The       per-value authored meaning beyond that use is not read. *(Nar"

```
00273910  push     rbx
00273912  sub      rsp, 0x20
00273916  mov      ebx, ecx
00273918  call     0x3588b0  ; -> 003588B0 fn
0027391D  mov      rcx, rax
00273920  call     0x263c20  ; -> 00263C20 fn
00273925  cmp      eax, 3
00273928  je       0x273932  ; -> 00273932
0027392A  xor      eax, eax
0027392C  add      rsp, 0x20
00273930  pop      rbx
00273931  ret      
00273932  mov      ecx, ebx
00273934  call     0x3229a0  ; -> 003229A0 fn
00273939  xor      ecx, ecx
0027393B  test     eax, eax
0027393D  sete     cl
00273940  mov      eax, ecx
00273942  add      rsp, 0x20
00273946  pop      rbx
00273947  ret      
```

## 0030BA80 (67 B, extent 0030BA80-0030BAC3)

Page context: "0', 'WorldActor_HasActiveBattleActionOrUnitFlag14' '0030BA30' and 'WorldActor_QueryCombatStanceState' '0030BFB0' resolve units through '0031B760', and 'CombatantId_HasActiveBattleActionOrUnitFlag14' '0030BA80' does the same through '0031B770'. 'BattleSystem_ResetRuntimeState' '00237DF0' calls '0023AC80'. '0023A570' and '002FFCF0' call the Gameplay-filed validator 'BattleEncodedId_IsValidForClass' '00322C50', and '002FFCF0' also calls 'B"

```
0030BA80  sub      rsp, 0x28
0030BA84  call     0x31b770  ; -> 0031B770 fn
0030BA89  mov      rcx, rax
0030BA8C  test     rax, rax
0030BA8F  je       0x30babc  ; -> 0030BABC
0030BA91  mov      eax, dword ptr [rax]
0030BA93  bt       rax, 0xe
0030BA98  jae      0x30baa4  ; -> 0030BAA4
0030BA9A  mov      eax, 1
0030BA9F  add      rsp, 0x28
0030BAA3  ret      
0030BAA4  cmp      qword ptr [rcx + 0x708], 0
0030BAAC  je       0x30babc  ; -> 0030BABC
0030BAAE  mov      eax, 0x21e
0030BAB3  cmp      word ptr [rcx + 0x714], ax
0030BABA  jbe      0x30ba9a  ; -> 0030BA9A
0030BABC  xor      eax, eax
0030BABE  add      rsp, 0x28
0030BAC2  ret      
```

## 003528C0 (44 B, extent 003528C0-003528EC)

Page context: "ActorRuntime_GetClassNibble' ('00263C20') is 'actor[+0x0E] & 0xF' (0 for a null actor). Two       writers give the nibble its authored names: the script verb **'setfreetargettype'** ('0x0265',       '003528C0') pops an integer and stores it through '00269FE0(actor, v)' ('0026A033'–'0026A03B';       for a kind-3 actor 'v == 4' also raises '+0x1C' bits 8 and 13, any other value clears them,       '00269FFE'–'0026A02B'); and 'BattleUnit_Re"

```
003528C0  push     rbx
003528C2  sub      rsp, 0x20
003528C6  mov      rcx, r9
003528C9  mov      rbx, rdx
003528CC  call     0x267e10  ; -> 00267E10 fn
003528D1  mov      edx, eax
003528D3  mov      rcx, rbx
003528D6  call     0x269fe0  ; -> 00269FE0 fn
003528DB  movzx    edx, word ptr [rbx]
003528DE  movzx    ecx, byte ptr [rbx + 0x15]
003528E2  add      rsp, 0x20
003528E6  pop      rbx
003528E7  jmp      0x263a30  ; -> 00263A30 fn
```
