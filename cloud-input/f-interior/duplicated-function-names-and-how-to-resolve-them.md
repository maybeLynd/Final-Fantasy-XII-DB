# F-interior pack: `00-Engine-Core-Runtime/duplicated-function-names-and-how-to-resolve-them.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/duplicated-function-names-and-how-to-resolve-them.json`.

Functions: 2. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: f9017b106	SWE2-CONTRACT: repair 807950d2a - restore 18 committed pass-22 section headings it renamed; 807950d2a	SWE2-CONTRACT: pass-22 debt batch A - 37 Engine-Core-Runtime pages' cross-subsystem neighbour bullet). OPUS read these before packing.

## 00237690 (81 B, extent 00237690-002376E1)

Page context: "both* edgeless. Three of the seventeen:  | name | body | thunk | |---|---|---| | 'SpawnGroup_TeardownAllGroupedSpawnUnits' | '00234880' | '00510840' | | 'SpawnGroup_TeardownAllUngroupedSpawnUnits' | '00237690' | '00510830' | | 'Spawn_SetAllSpawnBackedUnitsCurrentHPZero' | '002352E0' | '0050F650' |  > **They are not dead, and the reason is the very thing §6 wondered about.** Every one of the six > sampled thunks occurs as an aligned qwor"

```
00237690  push     rbx
00237692  sub      rsp, 0x20
00237696  xor      ebx, ebx
00237698  cmp      dword ptr [rip + 0x1e57002], ebx  ; -> 0208E6A0
0023769E  jle      0x2376db  ; -> 002376DB
002376A0  mov      ecx, ebx
002376A2  call     0x321170  ; -> 00321170 fn
002376A7  test     rax, rax
002376AA  je       0x2376d1  ; -> 002376D1
002376AC  mov      rcx, qword ptr [rax + 0x698]
002376B3  test     rcx, rcx
002376B6  je       0x2376d1  ; -> 002376D1
002376B8  cmp      byte ptr [rcx + 5], 1
002376BC  jne      0x2376d1  ; -> 002376D1
002376BE  cmp      byte ptr [rax + 0xe98], 0
002376C5  ja       0x2376d1  ; -> 002376D1
002376C7  xor      edx, edx
002376C9  mov      rcx, rax
002376CC  call     0x300e40  ; -> 00300E40 fn
002376D1  inc      ebx
002376D3  cmp      ebx, dword ptr [rip + 0x1e56fc7]  ; -> 0208E6A0
002376D9  jl       0x2376a0  ; -> 002376A0
002376DB  add      rsp, 0x20
002376DF  pop      rbx
002376E0  ret      
```

## 00379F20 (7 B, extent 00379F20-00379F27)

Page context: "ction is a 'jmp' to another entry in the same group.** Everything else is the body.  > **Not without ambiguity — the rule misses the one chain §2 counts (2026-09-13, §9).** > 'thunk_FUN_0035b650' is '00379F20' → '0035B450' → '0035B650'. '00379F20''s first instruction is > **'mov dl, 2'**, not a 'jmp', and '0035B450''s 'jmp' leaves the name group. So the group this > document singles out as the chain is exactly the one its resolution rul"

```
00379F20  mov      dl, 2
00379F22  jmp      0x35b450  ; -> 0035B450 fn
```
