# Homing pack: `00-Engine-Core-Runtime/Battle-Runtime-Mode/CONTRACT-battle-runtime-mode.md`

Generated 2026-10-03 15:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h14-contract-battle-runtime-mode.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00254480 (42 B, extent 00254480-002544AA)

Entered from (direct sites whose caller this page cites): `00280140` + 0x95 (call; `00280140` is cited on this page)
Other direct sites: none

Host context: "hored flag lists ('002EF2D0'→'00379160'). '002EF650' has three      live call sites: the mode-0 boot frame '0022B6E0' (inside the '0209273C == 5' advance      block — the boot→mode-1 transition) and '00280140' ('0028037B'); the '003941E5'/      '003942F2' sites sit in a fully orphaned body. The lazy '00233C10' has four callers —      '00280140' ('002803B8', *after* its own '002EF650'), '00285E60', '0036FCC0', '00394130'      — and is **"

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

## 00265950 (25 B, extent 00265950-00265969)

Entered from (direct sites whose caller this page cites): `0037B4D0` + 0xB81 (call; `0037B4D0` is cited on this page)
Other direct sites: `00342640` + 0x89 (call); `0034A340` + 0x14 (call); `0034E2F0` + 0xC (call)

Host context: "he slot map. '0031B950',    'BattleSlotMap_ResolveMappedBattleSlot' and five more read it; none is read.~~    **ANSWERED 2026-09-22 (SWE2-CONTRACT) — the reader is the party-read-in state machine    '0037B4D0', reached from the 'partyallread' / 'partyallread2' / 'summonread' verb tasks.**    Entry 3 is the class-4 map at '+0x5A90' (nine u16). Its full reader set, re-censused by    displacement ('+0x5A90', 8 sites): the resolver arm '003"

```
00265950  mov      rax, qword ptr [rcx + 0xc0]
00265957  test     rax, rax
0026595A  je       0x265965  ; -> 00265965
0026595C  movss    xmm0, dword ptr [rax + 0x148]
00265964  ret      
00265965  xorps    xmm0, xmm0
00265968  ret      
```
