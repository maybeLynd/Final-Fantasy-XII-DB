# Homing pack: `03-World-Area-Field/Weather/weather-slot-state-model.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-weather-slot-state-model.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00254480 (42 B, extent 00254480-002544AA)

Entered from (direct sites whose caller this page cites): `00280140` + 0x95 (call; `00280140` is cited on this page)
Other direct sites: none

Host context: "is **1..3**. The persisted domain is **0..2**. Every crossing between them is an explicit '+1' / '-1' in the native code — do not conflate them.  ## 5. Call chain  ''' world reset / transition path   00280140 | 0036FCC0 | 00394130      -> 00268320  (sets payload+0x1061 when dword 0209AC10 == 0; F-3)  authored runtime script   0x021A setweatherslot(int)      -> 003565C0  (ScriptVM handler)         -> 0026D910(slot)      <- apply         "

```
00254480  mov      eax, dword ptr [rip + 0x1bb7e9a]  ; -> 01E0C320 [u32 0x00000040]
00254486  test     dl, 0x80
00254489  mov      r8d, 0
0025448F  mov      dword ptr [rip + 0x1e3e2af], ecx  ; -> 02092744
00254495  cmovne   eax, r8d
00254499  btr      edx, 7
0025449D  mov      dword ptr [rip + 0x1e3e349], edx  ; -> 020927EC
002544A3  mov      dword ptr [rip + 0x1bb7e77], eax  ; -> 01E0C320 [u32 0x00000040]
002544A9  ret      
```
