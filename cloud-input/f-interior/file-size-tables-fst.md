# F-interior pack: `02-Resource-And-Asset-Pipeline/Loose-Files-And-Size-Tables/file-size-tables-fst.md`

Generated 2026-10-02 19:59 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/file-size-tables-fst.json`.

Functions: 6. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 69b8ed680	SWE2-EC7: batch 171 (SHARED-HUB-IDENTIFICATION-171) - 18 frontier bodies read and anchored on 11 bea; ac4d7d901	SWE2-FRONTIER: file-size-tables-fst.md - 001D6FB0 runs its read at once, only 001D6D90 queues (corre; inbox mentions: SWE2-EC7.md). OPUS read these before packing.

## 0019A660 (115 B, extent 0019A660-0019A6D3)

Page context: "'008C2EF0' does the underlying reads - the record-side of the FST stream pair.  Interior anchor '0019A7EB' (function '0019A770').  '0019A6E0' (143 B) is the chunk-layout planner '0019A770' consults: '0019A660' mints the record and '+0x88' phase resets, then the (size, granule, offset) triple distributes across the three chunk rows - row '+8' takes a bounded first-chunk length 'min(granule-offset, size)' and the start offset at '+0x14', "

```
0019A660  push     rbx
0019A662  sub      rsp, 0x20
0019A666  mov      rbx, rcx
0019A669  or       edx, 0xffffffff
0019A66C  mov      rcx, qword ptr [rcx + 8]
0019A670  call     qword ptr [rip + 0x727a6a]  ; -> 008C20E0 [u64 0x0000000001CCC13C]
0019A676  xor      r8d, r8d
0019A679  test     eax, eax
0019A67B  jne      0x19a6c6  ; -> 0019A6C6
0019A67D  mov      edx, r8d
0019A680  cmp      dword ptr [rbx + 0x10], edx
0019A683  jbe      0x19a6c6  ; -> 0019A6C6
0019A685  lea      r10d, [r8 + 1]
0019A689  nop      dword ptr [rax]
0019A690  mov      rcx, qword ptr [rbx + 0x18]
0019A694  mov      eax, edx
0019A696  imul     r9, rax, 0x98
0019A69D  xor      eax, eax
0019A69F  lock cmpxchg dword ptr [rcx + r9 + 0x90], r10d
0019A6A9  je       0x19a6bf  ; -> 0019A6BF
0019A6AB  inc      edx
0019A6AD  cmp      edx, dword ptr [rbx + 0x10]
0019A6B0  jb       0x19a690  ; -> 0019A690
0019A6B2  inc      dword ptr [r8 + 0x40]
0019A6B6  mov      rax, r8
0019A6B9  add      rsp, 0x20
0019A6BD  pop      rbx
0019A6BE  ret      
0019A6BF  mov      r8, qword ptr [rbx + 0x18]
0019A6C3  add      r8, r9
0019A6C6  inc      dword ptr [r8 + 0x40]
0019A6CA  mov      rax, r8
0019A6CD  add      rsp, 0x20
0019A6D1  pop      rbx
0019A6D2  ret      
```

## 001D6A20 (77 B, extent 001D6A20-001D6A6D)

Page context: "tion mismatch against '[rcx]' logs the '00D279A0' 'ready byt...' string via '005CDAA0'. It then releases the source — '002150D0' on the object, two IAT calls plus a '-1' store on the handle — writes '001D6A20''s result into '+0x20', and frees the base via '001D6B00' when that result is non-positive.  Interior anchor '0059AA27' (function '0059A9B0').  '00599250' (307 B) is the UTF-8-to-UTF-16 converter '0059EE90' runs on name strings: a "

```
001D6A20  mov      qword ptr [rsp + 8], rbx
001D6A25  mov      qword ptr [rsp + 0x10], rbp
001D6A2A  mov      qword ptr [rsp + 0x18], rsi
001D6A2F  push     rdi
001D6A30  sub      rsp, 0x30
001D6A34  mov      ebx, r9d
001D6A37  mov      edi, r8d
001D6A3A  mov      rsi, rdx
001D6A3D  mov      ebp, ecx
001D6A3F  call     0x20c700  ; -> 0020C700 fn
001D6A44  mov      rcx, rax
001D6A47  mov      dword ptr [rsp + 0x20], ebx
001D6A4B  mov      r9d, edi
001D6A4E  mov      r8, rsi
001D6A51  mov      edx, ebp
001D6A53  call     0x20b680  ; -> 0020B680 fn
001D6A58  mov      rbx, qword ptr [rsp + 0x40]
001D6A5D  mov      rbp, qword ptr [rsp + 0x48]
001D6A62  mov      rsi, qword ptr [rsp + 0x50]
001D6A67  add      rsp, 0x30
001D6A6B  pop      rdi
001D6A6C  ret      
```

## 001F4840 (98 B, extent 001F4840-001F48A2)

Page context: " 0 untouched — a bounded tell/step, not a transfer.  Interior anchor '002150F4' (function '002150E0').  '002150D0' (12 B) is the object-source release '0059A9B0' runs after the commit: tail-jumps to '001F4840' with 'rcx = [rcx+0x10]' (the object) and 'rdx' = the union record — the callee owns the teardown, this stub only rearranges the two pointers.  Interior anchor '002150D3' (function '002150D0').  '001D6CA0' (61 B) is the size-source"

```
001F4840  test     rdx, rdx
001F4843  je       0x1f48a1  ; -> 001F48A1
001F4845  push     rbx
001F4846  sub      rsp, 0x20
001F484A  mov      rbx, rdx
001F484D  xor      eax, eax
001F484F  mov      rdx, qword ptr [rcx + 0xa8]
001F4856  nop      word ptr [rax + rax]
001F4860  movsxd   rcx, eax
001F4863  lea      r8, [rcx + rcx*2]
001F4867  shl      r8, 4
001F486B  add      r8, rdx
001F486E  cmp      rbx, r8
001F4871  je       0x1f4894  ; -> 001F4894
001F4873  inc      eax
001F4875  cmp      eax, 0xf
001F4878  jl       0x1f4860  ; -> 001F4860
001F487A  mov      rcx, rbx
001F487D  call     0x215040  ; -> 00215040 fn
001F4882  mov      edx, 0x30
001F4887  mov      rcx, rbx
001F488A  add      rsp, 0x20
001F488E  pop      rbx
001F488F  jmp      0x809950  ; -> 00809950 fn
001F4894  mov      rcx, rbx
001F4897  call     0x2152d0  ; -> 002152D0 fn
001F489C  add      rsp, 0x20
001F48A0  pop      rbx
001F48A1  ret      
```

## 0020C150 (33 B, extent 0020C150-0020C171)

Page context: "the two pointers.  Interior anchor '002150D3' (function '002150D0').  '001D6CA0' (61 B) is the size-source path '0059A9B0''s '+0x20' arm takes: calls '0020C700' on the size value, then tail-jumps to '0020C150' forwarding '(result, rdx, r8, r9d)' unchanged — a two-stage resolver, so the semantic content lives in the two callees.  Interior anchor '001D6CB8' (function '001D6CA0').  '00215110' (267 B) is the ring-buffer dequeue '002150E0' w"

```
0020C150  mov      r10, r8
0020C153  mov      rax, rdx
0020C156  test     r9d, r9d
0020C159  je       0x20c16e  ; -> 0020C16E
0020C15B  test     rdx, rdx
0020C15E  je       0x20c16e  ; -> 0020C16E
0020C160  mov      r8d, r9d
0020C163  mov      rdx, r10
0020C166  mov      rcx, rax
0020C169  jmp      0x217a70  ; -> 00217A70 fn
0020C16E  xor      eax, eax
0020C170  ret      
```

## 00368F30 (62 B, extent 00368F30-00368F6E)

Page context: "82' (function '00215110').  '0046DD50' (251 B) is the '02CA6068' state stepper the pump '0032E070' runs: after the '0016D6A0' fill, state 4 gates on '0053DD10' and clears, state 3 needs '0053DD10' + '00368F30' quiet then arms '00369050' on '00536F30' and steps to 4, state 2 does '0053DD10' + '00368F30' then zeroes the state, and state 1 sizes the next stage from '02EBB52C'/'02EBB528'/'02EBB520' (each '(x + (x>>31 & 0x7FF))' rounded down"

```
00368F30  test     ecx, ecx
00368F32  js       0x368f48  ; -> 00368F48
00368F34  movsxd   rdx, ecx
00368F37  xor      eax, eax
00368F39  lea      rcx, [rip + 0x1f6f030]  ; -> 022D7F70
00368F40  cmp      qword ptr [rcx + rdx*8], rax
00368F44  setne    al
00368F47  ret      
00368F48  lea      rcx, [rip + 0x1f6f021]  ; -> 022D7F70
00368F4F  lea      rax, [rip + 0x1f6f022]  ; -> 022D7F78
00368F56  cmp      qword ptr [rcx], 0
00368F5A  jne      0x368f68  ; -> 00368F68
00368F5C  add      rcx, 8
00368F60  cmp      rcx, rax
00368F63  jl       0x368f56  ; -> 00368F56
00368F65  xor      eax, eax
00368F67  ret      
00368F68  mov      eax, 1
00368F6D  ret      
```

## 00536F30 (246 B, extent 00536F30-00537026)

Page context: "51 B) is the '02CA6068' state stepper the pump '0032E070' runs: after the '0016D6A0' fill, state 4 gates on '0053DD10' and clears, state 3 needs '0053DD10' + '00368F30' quiet then arms '00369050' on '00536F30' and steps to 4, state 2 does '0053DD10' + '00368F30' then zeroes the state, and state 1 sizes the next stage from '02EBB52C'/'02EBB528'/'02EBB520' (each '(x + (x>>31 & 0x7FF))' rounded down by '>> 0xB') into '02EBA520' via '0016D6"

```
00536F30  push     rbx
00536F32  mov      rbx, qword ptr [rip + 0x29845ff]  ; -> 02EBB538
00536F39  mov      r11d, 0x10
00536F3F  mov      r8, qword ptr [rip + 0x29845ea]  ; -> 02EBB530
00536F46  mov      eax, dword ptr [rbx + 8]
00536F49  mov      ecx, dword ptr [rbx + 4]
00536F4C  and      eax, 0x1ffffff
00536F51  cmp      byte ptr [rbx + 3], 0x64
00536F55  mov      dword ptr [rip + 0x2771b15], eax  ; -> 02CA8A70
00536F5B  mov      eax, 0xc
00536F60  cmove    r11d, eax
00536F64  mov      dword ptr [rip + 0x2771b09], r11d  ; -> 02CA8A74
00536F6B  and      ecx, 3
00536F6E  je       0x536f8a  ; -> 00536F8A
00536F70  sub      ecx, 1
00536F73  je       0x536f84  ; -> 00536F84
00536F75  cmp      ecx, 1
00536F78  jne      0x537024  ; -> 00537024
00536F7E  pop      rbx
00536F7F  jmp      0x537030  ; -> 00537030 fn
00536F84  pop      rbx
00536F85  jmp      0x536dd0  ; -> 00536DD0 fn
00536F8A  mov      r10d, dword ptr [rip + 0x2984597]  ; -> 02EBB528
00536F91  test     r10d, r10d
00536F94  je       0x536ff3  ; -> 00536FF3
00536F96  sub      r10d, r11d
00536F99  mov      ecx, r11d
00536F9C  add      rcx, rbx
00536F9F  mov      edx, r10d
00536FA2  mov      r9, r8
00536FA5  test     r10d, r10d
00536FA8  jle      0x536fc4  ; -> 00536FC4
00536FAA  nop      word ptr [rax + rax]
00536FB0  movzx    eax, byte ptr [rcx]
00536FB3  dec      edx
00536FB5  mov      byte ptr [r9], al
00536FB8  lea      r9, [r9 + 1]
00536FBC  lea      rcx, [rcx + 1]
00536FC0  test     edx, edx
00536FC2  jg       0x536fb0  ; -> 00536FB0
00536FC4  mov      edx, dword ptr [rip + 0x2984562]  ; -> 02EBB52C
00536FCA  movsxd   rcx, r10d
00536FCD  add      rcx, r8
00536FD0  test     edx, edx
00536FD2  jle      0x537024  ; -> 00537024
00536FD4  lea      r9, [rip + 0x2983545]  ; -> 02EBA520
00536FDB  sub      r9, rcx
00536FDE  nop      
00536FE0  movzx    eax, byte ptr [r9 + rcx]
00536FE5  dec      edx
00536FE7  mov      byte ptr [rcx], al
00536FE9  lea      rcx, [rcx + 1]
00536FED  test     edx, edx
00536FEF  jg       0x536fe0  ; -> 00536FE0
00536FF1  pop      rbx
00536FF2  ret      
00536FF3  mov      ecx, dword ptr [rip + 0x2984533]  ; -> 02EBB52C
00536FF9  lea      r9, [rip + 0x2983520]  ; -> 02EBA520
00537000  mov      edx, r11d
00537003  sub      ecx, r11d
00537006  add      rdx, r9
00537009  test     ecx, ecx
0053700B  jle      0x537024  ; -> 00537024
0053700D  nop      dword ptr [rax]
00537010  movzx    eax, byte ptr [rdx]
00537013  dec      ecx
00537015  mov      byte ptr [r8], al
00537018  lea      r8, [r8 + 1]
0053701C  lea      rdx, [rdx + 1]
00537020  test     ecx, ecx
00537022  jg       0x537010  ; -> 00537010
00537024  pop      rbx
00537025  ret      
```
