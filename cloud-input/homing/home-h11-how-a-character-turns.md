# Homing pack: `06-Movement-And-Navigation/Facing-And-Steering/how-a-character-turns.md`

Generated 2026-10-03 12:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h11-how-a-character-turns.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 003E6AF0 (80 B, extent 003E6AF0-003E6B40)

Entered from (direct sites whose caller this page cites): `002EA780` + 0x45 (call; `002EA780` is cited on this page)
Other direct sites: none

Host context: "12   (FABLE)** — class 3, the steerable actor class of 'BV-4'. §2. - [x] ~~**UQ-101.** **Who sets movement mode 5**, whose arm in the facing integrator '002E5750' waits on an   animation-state test ('002EA780'); none of the 29 call sites of '0026C120' passes a constant 5.~~   **Answered 2026-09-14 (FABLE):** the untimed turn body '002690D0' (the turn verbs 'raturn_25e', 'raturna', 'raturnya', '003578B0', 'unkCall_3092') **stores 5 into "

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
