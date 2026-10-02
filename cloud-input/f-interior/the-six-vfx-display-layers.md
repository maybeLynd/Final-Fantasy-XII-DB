# F-interior pack: `17-Presentation-Rendering/Effect-File-Formats/the-six-vfx-display-layers.md`

Generated 2026-10-02 08:46 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/the-six-vfx-display-layers.json`.

Functions: 5. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 7903502f7	FABLE: pass-22 debt - crossing sections on 94 pages (FABLE's group; 12 overlay-carrier pages routed ). OPUS read these before packing.

## 0017FDE0 (38 B, extent 0017FDE0-0017FE06)

Page context: "00' calls (ids 0xE00, 0xDFF, 0). The first takes '0017FEE0' or '0017FE60', picked by '0017D980''s answer ('001B2583'), with 'edi > 5' as their argument; the second always takes '0017FEE0', the third '0017FDE0' (corrected 2026-09-29, OPUS falsification pass 1, 'CON-180')**, stores '+0x90 = ebp' and '+0x94 = edi & ~0x10', then tail-jumps '001FBD80'  Interior anchor '001B259E' (function '001B2530').  '0039CFF0' (198 B) is the ensure-alloca"

```
0017FDE0  sub      rsp, 0x28
0017FDE4  call     0x189120  ; -> 00189120 fn
0017FDE9  mov      rcx, rax
0017FDEC  call     0x1867b0  ; -> 001867B0 fn
0017FDF1  cmp      byte ptr [rax + 8], 0
0017FDF5  jne      0x17fdff  ; -> 0017FDFF
0017FDF7  mov      rax, qword ptr [rax]
0017FDFA  add      rsp, 0x28
0017FDFE  ret      
0017FDFF  xor      eax, eax
0017FE01  add      rsp, 0x28
0017FE05  ret      
```

## 0017FE60 (57 B, extent 0017FE60-0017FE99)

Page context: "function '0036F9F0').  '001B2530' (201 B) is the emit-layer writer '00862C10' tail-jumps into: it stores '!00182560()' at '[rsi+0x98]', refreshes through '00182250'/'001823E0(3)', ~~picks '0017FEE0'/'0017FE60' on 'edi > 5' for three '002D7E00' emits (ids 0xE00, 0xDFF, 0)~~ **makes three '002D7E00' calls (ids 0xE00, 0xDFF, 0). The first takes '0017FEE0' or '0017FE60', picked by '0017D980''s answer ('001B2583'), with 'edi > 5' as their ar"

```
0017FE60  sub      rsp, 0x28
0017FE64  test     ecx, ecx
0017FE66  je       0x17fe77  ; -> 0017FE77
0017FE68  call     0x189120  ; -> 00189120 fn
0017FE6D  mov      rcx, rax
0017FE70  call     0x1868a0  ; -> 001868A0 fn
0017FE75  jmp      0x17fe84  ; -> 0017FE84
0017FE77  call     0x189120  ; -> 00189120 fn
0017FE7C  mov      rcx, rax
0017FE7F  call     0x186840  ; -> 00186840 fn
0017FE84  cmp      byte ptr [rax + 8], 0
0017FE88  jne      0x17fe92  ; -> 0017FE92
0017FE8A  mov      rax, qword ptr [rax]
0017FE8D  add      rsp, 0x28
0017FE91  ret      
0017FE92  xor      eax, eax
0017FE94  add      rsp, 0x28
0017FE98  ret      
```

## 0017FEE0 (57 B, extent 0017FEE0-0017FF19)

Page context: "0036F9F4' (function '0036F9F0').  '001B2530' (201 B) is the emit-layer writer '00862C10' tail-jumps into: it stores '!00182560()' at '[rsi+0x98]', refreshes through '00182250'/'001823E0(3)', ~~picks '0017FEE0'/'0017FE60' on 'edi > 5' for three '002D7E00' emits (ids 0xE00, 0xDFF, 0)~~ **makes three '002D7E00' calls (ids 0xE00, 0xDFF, 0). The first takes '0017FEE0' or '0017FE60', picked by '0017D980''s answer ('001B2583'), with 'edi > 5' "

```
0017FEE0  sub      rsp, 0x28
0017FEE4  test     ecx, ecx
0017FEE6  je       0x17fef7  ; -> 0017FEF7
0017FEE8  call     0x189120  ; -> 00189120 fn
0017FEED  mov      rcx, rax
0017FEF0  call     0x186a50  ; -> 00186A50 fn
0017FEF5  jmp      0x17ff04  ; -> 0017FF04
0017FEF7  call     0x189120  ; -> 00189120 fn
0017FEFC  mov      rcx, rax
0017FEFF  call     0x186a00  ; -> 00186A00 fn
0017FF04  cmp      byte ptr [rax + 8], 0
0017FF08  jne      0x17ff12  ; -> 0017FF12
0017FF0A  mov      rax, qword ptr [rax]
0017FF0D  add      rsp, 0x28
0017FF11  ret      
0017FF12  xor      eax, eax
0017FF14  add      rsp, 0x28
0017FF18  ret      
```

## 001B2600 (44 B, extent 001B2600-001B262C)

Page context: "oes not depend on that caller.  ## SWE2-EC7-71 update (2026-09-19) - '00862C30' + '00862C10' singleton forwarders measured  '00862C30' (12 B) loads the '01F7F4D8' singleton into 'rcx' and tail-jumps '001B2600' - the no-arg forwarder.  '00862C10' (17 B) is the arg-swapping sibling: '001B2530(global, edx, ecx)' - the singleton prepended, the two caller args reversed. Interior anchors '00862C37' (the 'jmp 001B2600' tail) and '00862C1C' (th"

```
001B2600  push     rbx
001B2602  sub      rsp, 0x20
001B2606  mov      rbx, rcx
001B2609  call     0x1fbe50  ; -> 001FBE50 fn
001B260E  cmp      byte ptr [rbx + 0x98], 0
001B2615  je       0x1b2626  ; -> 001B2626
001B2617  mov      ecx, 3
001B261C  add      rsp, 0x20
001B2620  pop      rbx
001B2621  jmp      0x1823e0  ; -> 001823E0 fn
001B2626  add      rsp, 0x20
001B262A  pop      rbx
001B262B  ret      
```

## 003A3990 (97 B, extent 003A3990-003A39F1)

Page context: "it handshake and '+0x39B'; the '+0x13' lookup; flag bits 4 and 15; '020926E4' bit 11 | | V7 | section 2: layer 3 | **survives**: the bit-2 test of '02F8F310'. It makes no grouped-pass call and calls '003A3990', not '003A3740' | | V8 | the notes that name an instruction and hold | **survives**: the forwarders, '0024C640''s body, the latch, '00376320', '0036F550''s submit, '0036F9F0''s records, '001B2530''s stores |  Corrected in place: t"

```
003A3990  sub      rsp, 0x28
003A3994  mov      eax, dword ptr [rip + 0x274ba7a]  ; -> 02AEF414
003A399A  test     eax, eax
003A399C  je       0x3a39ec  ; -> 003A39EC
003A399E  mov      qword ptr [rsp + 0x30], rbx
003A39A3  xor      ebx, ebx
003A39A5  test     eax, eax
003A39A7  je       0x3a39dd  ; -> 003A39DD
003A39A9  mov      qword ptr [rsp + 0x20], rdi
003A39AE  lea      rdi, [rip + 0x274ba6b]  ; -> 02AEF420
003A39B5  nop      word ptr [rax + rax]
003A39C0  mov      rcx, qword ptr [rdi + rbx*8]
003A39C4  mov      edx, 2
003A39C9  call     0x20e630  ; -> 0020E630 fn
003A39CE  inc      ebx
003A39D0  cmp      ebx, dword ptr [rip + 0x274ba3e]  ; -> 02AEF414
003A39D6  jb       0x3a39c0  ; -> 003A39C0
003A39D8  mov      rdi, qword ptr [rsp + 0x20]
003A39DD  mov      rbx, qword ptr [rsp + 0x30]
003A39E2  mov      dword ptr [rip + 0x274ba28], 0  ; -> 02AEF414
003A39EC  add      rsp, 0x28
003A39F0  ret      
```
