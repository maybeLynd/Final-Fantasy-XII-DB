# Homing pack: `00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md`

Generated 2026-10-03 15:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h14-the-world-tick-and-the-field-frame.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00250960 (64 B, extent 00250960-002509A0)

Entered from (direct sites whose caller this page cites): `0025D580` + 0x18 (call; `0025D580` is cited on this page); `0025D9E0` + 0x476 (call; `0025D9E0` is cited on this page)
Other direct sites: none

Host context: "eader is down** (§2.3 step 20) | | 12 | '00238B00(1)' from '002678C0' (← '0025B600', '0036FCC0') | '00238B00(0)' from 'ActorManager_BindLoadedDefinitionPayload' ('0026C965', when its argument is 0), '0025D580', '002628B0' | the '0x3080' mask | **a definition payload load is in flight** — presentation veto | | 13 | '00238B20(1)' from '0025B740' (← 'ActorManager_RunFieldRuntimePass'): the **focus actor** ('PartyFocus_GetCurrentPackedActor" / "ystem_BindBattleUnitsForEligibleRecords' — installs the callback at record '+0x38' | | '0025DF00' | 1,228 B | 'WorldActor_UpdateRuntimeAndScriptExecutionState' — calls the callback at '0025E222' | | '0025D9E0' | 1,297 B | 'ActorManager_RunFieldRuntimePass(slot)' — [the field runtime pass](../../04-Actor-Entity/the-field-runtime-pass.md) | | '003DB1F0' | 132 B | per-record post-pass: '+0x63' countdown, '+0xA0' state walk, '003DB6E0' | | "

```
00250960  mov      qword ptr [rsp + 8], rbx
00250965  push     rdi
00250966  sub      rsp, 0x20
0025096A  mov      ebx, edx
0025096C  mov      edi, ecx
0025096E  xor      edx, edx
00250970  lea      ecx, [rdx + 1]
00250973  call     0x35c880  ; -> 0035C880 fn
00250978  call     0x35c6f0  ; -> 0035C6F0 fn
0025097D  test     al, 2
0025097F  je       0x25098d  ; -> 0025098D
00250981  mov      edx, 4
00250986  xor      ecx, ecx
00250988  call     0x35c880  ; -> 0035C880 fn
0025098D  mov      edx, ebx
0025098F  mov      ecx, edi
00250991  mov      rbx, qword ptr [rsp + 0x30]
00250996  add      rsp, 0x20
0025099A  pop      rdi
0025099B  jmp      0x28e580  ; -> 0028E580 fn
```

## 002E1630 (43 B, extent 002E1630-002E165B)

Entered from (direct sites whose caller this page cites): `002628B0` + 0x391 (call; `002628B0` is cited on this page)
Other direct sites: `00345E20` + 0xF (call)

Host context: "then zeroes the four party-roster pointers > '0209A1F0'–'0209A20F' ('0025C017' / '0025C01F') — even if a callback has cleared bit 0 meanwhile. Then, with or > without that sweep, it calls the unload '002628B0' for each set bit **4 down to 0**, clearing each bit only after > its call returns ('0025C030'–'0025C052'). Bits 5 and above are never visited. Because the mask is re-read, a > request added during the pass for a lower index runs i"

```
002E1630  sub      rsp, 0x28
002E1634  call     0x290180  ; -> 00290180 fn
002E1639  test     eax, eax
002E163B  je       0x2e1653  ; -> 002E1653
002E163D  sub      eax, 1
002E1640  je       0x2e164c  ; -> 002E164C
002E1642  cmp      eax, 1
002E1645  jne      0x2e164c  ; -> 002E164C
002E1647  add      rsp, 0x28
002E164B  ret      
002E164C  xor      eax, eax
002E164E  add      rsp, 0x28
002E1652  ret      
002E1653  or       eax, 0xffffffff
002E1656  add      rsp, 0x28
002E165A  ret      
```
