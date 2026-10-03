# Homing pack: `17-Presentation-Rendering/Effect-File-Formats/the-six-vfx-display-layers.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-six-vfx-display-layers.json`.

Bodies: 3. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001868A0 (66 B, extent 001868A0-001868E2)

Entered from (direct sites whose caller this page cites): `0017FE60` + 0x10 (call; `0017FE60` is cited on this page)
Other direct sites: none

Host context: "function '0036F9F0').  '001B2530' (201 B) is the emit-layer writer '00862C10' tail-jumps into: it stores '!00182560()' at '[rsi+0x98]', refreshes through '00182250'/'001823E0(3)', ~~picks '0017FEE0'/'0017FE60' on 'edi > 5' for three '002D7E00' emits (ids 0xE00, 0xDFF, 0)~~ **makes three '002D7E00' calls (ids 0xE00, 0xDFF, 0). The first takes '0017FEE0' or '0017FE60', picked by '0017D980''s answer ('001B2583'), with 'edi > 5' as their ar"

```
001868A0  push     rbx
001868A2  sub      rsp, 0x20
001868A6  mov      rbx, rcx
001868A9  call     0x1ede70  ; -> 001EDE70 fn
001868AE  test     eax, eax
001868B0  je       0x1868b7  ; -> 001868B7
001868B2  call     0x1edda0  ; -> 001EDDA0 fn
001868B7  cmp      byte ptr [rbx + 0xdbb], 0
001868BE  mov      eax, dword ptr [rbx + 0xdd0]
001868C4  je       0x1868d4  ; -> 001868D4
001868C6  mov      rax, qword ptr [rbx + rax*8 + 0xb50]
001868CE  add      rsp, 0x20
001868D2  pop      rbx
001868D3  ret      
001868D4  mov      rax, qword ptr [rbx + rax*8 + 0xb48]
001868DC  add      rsp, 0x20
001868E0  pop      rbx
001868E1  ret      
```

## 00186A50 (33 B, extent 00186A50-00186A71)

Entered from (direct sites whose caller this page cites): `0017FEE0` + 0x10 (call; `0017FEE0` is cited on this page)
Other direct sites: none

Host context: "0036F9F4' (function '0036F9F0').  '001B2530' (201 B) is the emit-layer writer '00862C10' tail-jumps into: it stores '!00182560()' at '[rsi+0x98]', refreshes through '00182250'/'001823E0(3)', ~~picks '0017FEE0'/'0017FE60' on 'edi > 5' for three '002D7E00' emits (ids 0xE00, 0xDFF, 0)~~ **makes three '002D7E00' calls (ids 0xE00, 0xDFF, 0). The first takes '0017FEE0' or '0017FE60', picked by '0017D980''s answer ('001B2583'), with 'edi > 5' "

```
00186A50  cmp      byte ptr [rcx + 0xdbb], 0
00186A57  mov      eax, dword ptr [rcx + 0xdd0]
00186A5D  je       0x186a68  ; -> 00186A68
00186A5F  mov      rax, qword ptr [rcx + rax*8 + 0xb50]
00186A67  ret      
00186A68  mov      rax, qword ptr [rcx + rax*8 + 0xb48]
00186A70  ret      
```

## 00862C00 (14 B, extent 00862C00-00862C0E)

Entered from (direct sites whose caller this page cites): `003A3740` + 0xF2 (call; `003A3740` is cited on this page)
Other direct sites: none

Host context: "fect emit module, and then **draws the layer's effect groups in a fixed order - 2, 3, 5, 6, 9, 1, 7, 4** - eight calls of one routine with '(layer, group)'; there is no group 0 or 8. Then it calls **'003A3740', the drain of the depth-sorted display list** ([the Gi render command family](../Gi-Render-Commands/gi-render-command-family.md) reads it: sort, then walk), makes a call to an empty function, waits on the same bit again and closes"

```
00862C00  mov      rax, qword ptr [rip + 0x171c8d1]  ; -> 01F7F4D8
00862C07  mov      eax, dword ptr [rax + 0x90]
00862C0D  ret      
```
