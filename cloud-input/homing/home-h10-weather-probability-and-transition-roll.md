# Homing pack: `03-World-Area-Field/Weather/weather-probability-and-transition-roll.md`

Generated 2026-10-03 12:18 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h10-weather-probability-and-transition-roll.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00250960 (64 B, extent 00250960-002509A0)

Entered from (direct sites whose caller this page cites): `0025D9E0` + 0x476 (call; `0025D9E0` is cited on this page)
Other direct sites: `0025D580` + 0x18 (call)

Host context: "| '0025ABA0' | 'WorldField_SelectAlternateEligibleWeatherSlot' | 253 B | eligible-alternate picker | | '002620E0' | *(field-runtime init core)* | 231 B | one-shot gate, primary ActorManager only | | '0025D9E0' | 'ActorManager_RunFieldRuntimePass' | — | caller | | '00265920' | 'WorldField_GetCurrentWeatherSlot1To3WithDebugOverride' | 41 B | current slot | | '0026D910' | 'WorldField_ApplyWeatherSlotAndDerivedEnvironmentState' | 418 B | ap"

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
