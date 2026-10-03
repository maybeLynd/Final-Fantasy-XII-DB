# Homing pack: `06-Movement-And-Navigation/Movement-Mode-Selection/setting-the-movement-mode-and-which-way-a-character-turns.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-setting-the-movement-mode-and-which-way-a-character-tu.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002E5B90 (35 B, extent 002E5B90-002E5BB3)

Entered from (direct sites whose caller this page cites): `0026AC70` + 0x5C (jmp; `0026AC70` is cited on this page)
Other direct sites: none

Host context: "re the switch it reads 'turn_step' ('00264750' → '002E4BC0' → '+0x58') and, **when any mode is active, floors it at '0x3C0EFA35' = π/360 = 0.5° per frame** ('002E5806'–'002E5821', through the setter '0026AC70').  | mode | what the integrator does each frame | set by | |---:|---|---| | 0 | nothing | the teardown callers (§7) | | 1 | 'heading += +0x3C', wrapped, through 'Actor_SetFacingHeading_Variant0' ('002E5A9E'–'002E5AED') — **a const"

```
002E5B90  test     rcx, rcx
002E5B93  je       0x2e5bb2  ; -> 002E5BB2
002E5B95  cmp      qword ptr [rcx + 0xc0], 0
002E5B9D  je       0x2e5bb2  ; -> 002E5BB2
002E5B9F  mov      rax, qword ptr [rcx + 0xb8]
002E5BA6  mov      rcx, qword ptr [rax + 0xf0]
002E5BAD  movss    dword ptr [rcx + 0x58], xmm1
002E5BB2  ret      
```

## 003E6AF0 (80 B, extent 003E6AF0-003E6B40)

Entered from (direct sites whose caller this page cites): `002EA780` + 0x45 (call; `002EA780` is cited on this page)
Other direct sites: none

Host context: "02E5931') | the timed turns: 'turnt' / 'rturnt' ('003425D0'), 'rturnt_4b' (second site), 'rturnat' / 'turnat' ('0034D9B0'), 'dira' ('0034E040'), 'dir_4e' ('0034E360') — 5 sites pass 4 | | 5 | waits: '002EA780' is true when the render record's '+0x284' is set and '002EA910' returns 1 (an animation-state test); then '0026C120(actor, 0)' ('002E5853'–'002E5A6E') | **nobody found** — all 29 call sites of '0026C120' pass 0, 2, 3 or 4, re-deri"

```
003E6AF0  push     rbx
003E6AF2  sub      rsp, 0x20
003E6AF6  mov      ebx, dword ptr [rcx + 0x18]
003E6AF9  cmp      ebx, -1
003E6AFC  je       0x3e6b38  ; -> 003E6B38
003E6AFE  mov      ecx, dword ptr [rcx + 0x10]
003E6B01  call     0x20e600  ; -> 0020E600 fn
003E6B06  cmp      ebx, -1
003E6B09  je       0x3e6b38  ; -> 003E6B38
003E6B0B  mov      rcx, qword ptr [rax + 0xd98]
003E6B12  mov      edx, ebx
003E6B14  call     0x2ed570  ; -> 002ED570 fn
003E6B19  test     rax, rax
003E6B1C  je       0x3e6b38  ; -> 003E6B38
003E6B1E  mov      rcx, rax
003E6B21  call     0x370e20  ; -> 00370E20 fn
003E6B26  test     rax, rax
003E6B29  je       0x3e6b38  ; -> 003E6B38
003E6B2B  mov      rcx, rax
003E6B2E  add      rsp, 0x20
003E6B32  pop      rbx
003E6B33  jmp      0x3e2bd0  ; -> 003E2BD0 fn
003E6B38  xor      eax, eax
003E6B3A  add      rsp, 0x20
003E6B3E  pop      rbx
003E6B3F  ret      
```
