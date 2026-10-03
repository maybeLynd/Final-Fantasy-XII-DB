# Homing pack: `17-Presentation-Rendering/Character-Rendering/character-render-object.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-character-render-object.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00186840 (93 B, extent 00186840-0018689D)

Entered from (direct sites whose caller this page cites): `001FA1A0` + 0x104 (call; `001FA1A0` is cited on this page)
Other direct sites: `0017FE60` + 0x1F (call)

Host context: "'+0x4B6' — two instructions | '001FA816' | | 22 | '001F9FE0' | 9 | float setter 'movss [+0x4B8], xmm1' | '001F9FE0' | | 23 | '001F9A70' | 9 | setter '+0x4BC' — two instructions | '001F9A78' | | 24 | '001FA1A0' | 547 | **'MaterialOverrideParameterPropagation'** | '001FA1BD' | | 25 | '001FAD40' | 7 | setter '+0x4B0' — two instructions | '001FAD46' | | 26 | '001FAA10' | 812 | **'NamedTransformPalettePropagation'** | '001FAA29' | | 27 | '00"

```
00186840  mov      qword ptr [rsp + 8], rbx
00186845  push     rdi
00186846  sub      rsp, 0x20
0018684A  mov      rbx, rcx
0018684D  call     0x1ede70  ; -> 001EDE70 fn
00186852  test     eax, eax
00186854  je       0x18685b  ; -> 0018685B
00186856  call     0x1edda0  ; -> 001EDDA0 fn
0018685B  cmp      byte ptr [rbx + 0xdbb], 0
00186862  mov      edi, dword ptr [rbx + 0xdd0]
00186868  je       0x186888  ; -> 00186888
0018686A  call     0x17f280  ; -> 0017F280 fn
0018686F  test     eax, eax
00186871  je       0x186888  ; -> 00186888
00186873  mov      eax, edi
00186875  mov      rax, qword ptr [rbx + rax*8 + 0xb50]
0018687D  mov      rbx, qword ptr [rsp + 0x30]
00186882  add      rsp, 0x20
00186886  pop      rdi
00186887  ret      
00186888  mov      eax, edi
0018688A  mov      rax, qword ptr [rbx + rax*8 + 0xb48]
00186892  mov      rbx, qword ptr [rsp + 0x30]
00186897  add      rsp, 0x20
0018689B  pop      rdi
0018689C  ret      
```
