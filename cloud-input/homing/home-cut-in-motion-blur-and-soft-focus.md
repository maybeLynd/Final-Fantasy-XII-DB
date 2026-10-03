# Homing pack: `17-Presentation-Rendering/Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-cut-in-motion-blur-and-soft-focus.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 003B26D0 (61 B, extent 003B26D0-003B270D)

Entered from (direct sites whose caller this page cites): `0024E910` + 0x56 (call; `0024E910` is cited on this page)
Other direct sites: none

Host context: "the seven fade layers -   [the world tick](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md), 'EX-8') and one   further body not read. - **The effect system's teardown '0024E910' (256 B) ends in the blur clear and then the cut-in clear** ('0024EA02',   '0024EA0B'); the area unload calls it. *Corrected 2026-09-19: this bullet first said only the tail was read while   anchoring the body; it was read whole, a"

```
003B26D0  mov      qword ptr [rsp + 8], rbx
003B26D5  push     rdi
003B26D6  sub      rsp, 0x20
003B26DA  lea      rbx, [rip + 0x2b0beff]  ; -> 02EBE5E0
003B26E1  lea      rdi, [rip + 0x2b0c4f8]  ; -> 02EBEBE0
003B26E8  mov      ecx, dword ptr [rbx]
003B26EA  test     ecx, ecx
003B26EC  je       0x3b2702  ; -> 003B2702
003B26EE  test     byte ptr [rbx + 0x20], 1
003B26F2  jne      0x3b26f9  ; -> 003B26F9
003B26F4  call     0x3b18e0  ; -> 003B18E0 fn
003B26F9  add      rbx, 0x30
003B26FD  cmp      rbx, rdi
003B2700  jl       0x3b26e8  ; -> 003B26E8
003B2702  mov      rbx, qword ptr [rsp + 0x30]
003B2707  add      rsp, 0x20
003B270B  pop      rdi
003B270C  ret      
```

## 003B3E40 (82 B, extent 003B3E40-003B3E92)

Entered from (direct sites whose caller this page cites): `003B3D20` + 0x1E (jmp; `003B3D20` is cited on this page)
Other direct sites: none

Host context: "s page owns what each of those calls does to the three effects. Only the five call sites of the unload were read, not the unload.  **Audio - INCIDENTAL.** The driver '0024D540' calls the Audio-filed '003B3D20' in its first half, before the frame-mode gate. That half was not read for this page and nothing here depends on it.  **Combat AI - MECHANICAL.** The '003B3D20' section cites its callee '003E7DE0', which the CombatAI-filed '0030861"

```
003B3E40  mov      qword ptr [rsp + 8], rbx
003B3E45  mov      qword ptr [rsp + 0x10], rsi
003B3E4A  push     rdi
003B3E4B  sub      rsp, 0x20
003B3E4F  lea      rbx, [rip + 0x2b08e2e]  ; -> 02EBCC84
003B3E56  xor      edi, edi
003B3E58  lea      rsi, [rip + 0x2b08f25]  ; -> 02EBCD84
003B3E5F  nop      
003B3E60  cmp      byte ptr [rbx - 4], dil
003B3E64  je       0x3b3e6f  ; -> 003B3E6F
003B3E66  mov      ecx, dword ptr [rbx]
003B3E68  xor      edx, edx
003B3E6A  call     0x2df0f0  ; -> 002DF0F0 fn
003B3E6F  mov      byte ptr [rbx - 4], dil
003B3E73  mov      word ptr [rbx - 2], di
003B3E77  mov      dword ptr [rbx], edi
003B3E79  add      rbx, 8
003B3E7D  cmp      rbx, rsi
003B3E80  jl       0x3b3e60  ; -> 003B3E60
003B3E82  mov      rbx, qword ptr [rsp + 0x30]
003B3E87  mov      rsi, qword ptr [rsp + 0x38]
003B3E8C  add      rsp, 0x20
003B3E90  pop      rdi
003B3E91  ret      
```
