# Homing pack: `18-Audio/Audio-Bank-And-Controller-Family/audio-bank-and-controller-family.md`

Generated 2026-10-03 13:52 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h13-audio-bank-and-controller-family.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00221870 (93 B, extent 00221870-002218CD)

Entered from (direct sites whose caller this page cites): `00222700` + 0x2F (jmp; `00222700` is cited on this page)
Other direct sites: `00218260` + 0xF (call); `00222CF0` + 0x3B (jmp); `00223730` + 0x4E (jmp); `00224C30` + 0xA (jmp); `002251A0` + 0xA (jmp)

Host context: "' via the '0xD1745D1745D1745D' reciprocal | '002188E1' | | '00218380' | 1,093 B | the insert body: '00217CC0' construct-at-end, '00217BA0' hole-open, '002181A0' element copies, '001EDF00' allocate + '00222700' free on the grow path, virtual '+0x10'/'+0x38'/'+0x18' element calls | '00218491' |  '00217F10' (the element ctor — stamps vtable '01E678B0'), '002181A0' (the element sub-copy), '001EDF00'/'002226A0'/'00222700' (allocator) are sha"

```
00221870  push     rdi
00221872  sub      rsp, 0x30
00221876  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0022187F  mov      qword ptr [rsp + 0x40], rbx
00221884  mov      qword ptr [rsp + 0x48], rsi
00221889  lea      rax, [rip + 0x6e6020]  ; -> 009078B0
00221890  mov      qword ptr [rcx], rax
00221893  lea      rdi, [rcx + 8]
00221897  mov      rbx, qword ptr [rdi]
0022189A  cmp      rbx, rdi
0022189D  je       0x2218bd  ; -> 002218BD
0022189F  nop      
002218A0  mov      rdx, rbx
002218A3  mov      rbx, qword ptr [rbx]
002218A6  mov      rax, qword ptr [rdi + 0x10]
002218AA  mov      r8d, 0x18
002218B0  lea      rcx, [rdi + 0x10]
002218B4  call     qword ptr [rax + 0x18]
002218B7  nop      
002218B8  cmp      rbx, rdi
002218BB  jne      0x2218a0  ; -> 002218A0
002218BD  mov      rbx, qword ptr [rsp + 0x40]
002218C2  mov      rsi, qword ptr [rsp + 0x48]
002218C7  add      rsp, 0x30
002218CB  pop      rdi
002218CC  ret      
```
