# Homing pack: `00-Engine-Core-Runtime/Shared-Transform-Workbench/the-shared-transform-workbench.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-shared-transform-workbench.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 003B2750 (79 B, extent 003B2750-003B279F)

Entered from (direct sites whose caller this page cites): `0036E9B0` + 0x32 (jmp; `0036E9B0` is cited on this page)
Other direct sites: none

Host context: "said *"BQ-16 (no matrix division: the rows are registers) … answered there."* - [x] ~~What '022D94B0' and '022D94B4' point to. Read 8 bytes wide by 16 functions in one tight family       ('0036DDC0'–'0036E9B0'), never written through a RIP-relative store, so they are set through a       register.~~ **BQ-17 ANSWERED 2026-09-12 (FABLE): not two pointers — the base of a 32-entry       table of 24-byte records, written by the same family th"

```
003B2750  mov      eax, ecx
003B2752  mov      r10d, edx
003B2755  and      eax, 0xf0000000
003B275A  cmp      eax, 0x70000000
003B275F  jne      0x3b279e  ; -> 003B279E
003B2761  xor      r8d, r8d
003B2764  lea      rax, [rip + 0x2b0be75]  ; -> 02EBE5E0
003B276B  lea      r11, [rip + 0x2b0c46e]  ; -> 02EBEBE0
003B2772  mov      edx, dword ptr [rax]
003B2774  mov      r9, rax
003B2777  test     edx, edx
003B2779  je       0x3b279e  ; -> 003B279E
003B277B  cmp      edx, ecx
003B277D  je       0x3b278b  ; -> 003B278B
003B277F  inc      r8d
003B2782  add      rax, 0x30
003B2786  cmp      rax, r11
003B2789  jl       0x3b2772  ; -> 003B2772
003B278B  cmp      r8d, 0x20
003B278F  je       0x3b279e  ; -> 003B279E
003B2791  and      byte ptr [r9 + 0x20], 0xfe
003B2796  and      r10b, 1
003B279A  or       byte ptr [r9 + 0x20], r10b
003B279E  ret      
```
