# F-interior pack: `17-Presentation-Rendering/Character-Render-Records/render-event-selection-evidence.md`

Generated 2026-10-02 19:59 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/render-event-selection-evidence.json`.

Functions: 4. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 54e8a524e	SWE2-FRONTIER for FABLE: pass-22 unattributed appends - verifier + 23 of 34 PUBLISHABLE pages (batch; inbox mentions: SWE2-EC7.md). OPUS read these before packing.

## 00426870 (90 B, extent 00426870-004268CA)

Page context: "'00520430' | flag work on '+0x290'/'+0x3F4'–'+0x3F6'; '00429500','004288B0','0042B580' | '00520482' | | 0x14 | '00520E70' | ~~tail into '0042DC10' region~~ posts the per-node body '00521050' through '00426870' with 'word[rec + 0]' and the command *(corrected 2026-10-02, OPUS: '00520E70'+0xA 'lea rdx, [00521050]', '00520E70'+0x11 'call 00426870')* | '00520E70' | | 0x15 | '00520740' | 58 B — touches '+0x3D1' | '00520740' | | 0x16 | '00520"

```
00426870  cmp      cx, -1
00426874  je       0x4268c9  ; -> 004268C9
00426876  mov      qword ptr [rsp + 0x10], rsi
0042687B  push     rdi
0042687C  sub      rsp, 0x20
00426880  movsx    rax, cx
00426884  mov      rsi, rdx
00426887  mov      qword ptr [rsp + 0x30], rbx
0042688C  mov      rdx, r8
0042688F  imul     rbx, rax, 0x740
00426896  mov      rdi, r8
00426899  add      rbx, qword ptr [rip + 0x1ea0688]  ; -> 022C6F28
004268A0  mov      rcx, rbx
004268A3  call     rsi
004268A5  movzx    ecx, word ptr [rbx + 8]
004268A9  mov      rbx, qword ptr [rsp + 0x30]
004268AE  cmp      cx, -1
004268B2  je       0x4268bf  ; -> 004268BF
004268B4  mov      r8, rdi
004268B7  mov      rdx, rsi
004268BA  call     0x42ef90  ; -> 0042EF90 fn
004268BF  mov      rsi, qword ptr [rsp + 0x38]
004268C4  add      rsp, 0x20
004268C8  pop      rdi
004268C9  ret      
```

## 0042DC10 (138 B, extent 0042DC10-0042DC9A)

Page context: "5207C0' | '003E6DA0' + '003E29F0' pair | '005207C9' | | 0x13 | '00520430' | flag work on '+0x290'/'+0x3F4'–'+0x3F6'; '00429500','004288B0','0042B580' | '00520482' | | 0x14 | '00520E70' | ~~tail into '0042DC10' region~~ posts the per-node body '00521050' through '00426870' with 'word[rec + 0]' and the command *(corrected 2026-10-02, OPUS: '00520E70'+0xA 'lea rdx, [00521050]', '00520E70'+0x11 'call 00426870')* | '00520E70' | | 0x15 | '005"

```
0042DC10  push     rdi
0042DC12  sub      rsp, 0x20
0042DC16  cmp      word ptr [rcx + 0x2f2], 1
0042DC1E  mov      rdi, rcx
0042DC21  je       0x42dc94  ; -> 0042DC94
0042DC23  mov      rax, qword ptr [rdx + 8]
0042DC27  mov      qword ptr [rsp + 0x30], rbx
0042DC2C  movsx    ebx, word ptr [rax]
0042DC2F  movzx    eax, word ptr [rcx + 6]
0042DC33  cmp      ax, -1
0042DC37  je       0x42dc3c  ; -> 0042DC3C
0042DC39  movsx    ebx, ax
0042DC3C  call     0x3e5cf0  ; -> 003E5CF0 fn
0042DC41  cmp      eax, 0x1c
0042DC44  jl       0x42dc7e  ; -> 0042DC7E
0042DC46  cmp      bx, -1
0042DC4A  jne      0x42dc50  ; -> 0042DC50
0042DC4C  xor      eax, eax
0042DC4E  jmp      0x42dc71  ; -> 0042DC71
0042DC50  movsx    rax, bx
0042DC54  imul     rcx, rax, 0x740
0042DC5B  xor      eax, eax
0042DC5D  add      rcx, qword ptr [rip + 0x1e992c4]  ; -> 022C6F28
0042DC64  cmp      dword ptr [rcx + 0x284], eax
0042DC6A  cmove    rcx, rax
0042DC6E  mov      rax, rcx
0042DC71  movzx    ecx, word ptr [rax + 6]
0042DC75  cmp      cx, -1
0042DC79  je       0x42dc7e  ; -> 0042DC7E
0042DC7B  movsx    ebx, cx
0042DC7E  movzx    ecx, word ptr [rdi]
0042DC81  mov      r8d, 0x10a
0042DC87  movzx    edx, bx
0042DC8A  call     0x42f310  ; -> 0042F310 fn
0042DC8F  mov      rbx, qword ptr [rsp + 0x30]
0042DC94  add      rsp, 0x20
0042DC98  pop      rdi
0042DC99  ret      
```

## 00477610 (38 B, extent 00477610-00477636)

Page context: "90' fields | '00520C8A' | | 0x19 | '00520CE0' | 32 B — calls '0046CC70' | '00520CF4' | | 0x1A | '00520C10' | '00422D50' + '003E6340'; '+0x30'/'+0x370' | '00520C20' | | 0x1D | '00520D30' | '003E55B0','00477610','00428B30','003E7450'; '+0x413'/'+0x4B7' flags | '00520D60' | | 0x1E | '00520DF0' | 50 B — '003E6A20'; '+0x413' | '00520E16' | | 0x1F | '00520140' | 23 B — tail-calls '003E6710' | '0052014B' | | 0x20 | '005207A0' | 23 B — touches "

```
00477610  lea      rax, [rip + 0x282f689]  ; -> 02CA6CA0
00477617  movzx    ecx, dl
0047761A  shl      rcx, 6
0047761E  add      rcx, rax
00477621  xor      eax, eax
00477623  cmp      dword ptr [rcx + 4], edx
00477626  cmovne   rcx, rax
0047762A  test     rcx, rcx
0047762D  je       0x477635  ; -> 00477635
0047762F  lea      eax, [rdx - 1]
00477632  mov      dword ptr [rcx + 0xc], eax
00477635  ret      
```

## 00520E70 (32 B, extent 00520E70-00520E90)

Page context: "'00520160' | | 0x12 | '005207C0' | '003E6DA0' + '003E29F0' pair | '005207C9' | | 0x13 | '00520430' | flag work on '+0x290'/'+0x3F4'–'+0x3F6'; '00429500','004288B0','0042B580' | '00520482' | | 0x14 | '00520E70' | ~~tail into '0042DC10' region~~ posts the per-node body '00521050' through '00426870' with 'word[rec + 0]' and the command *(corrected 2026-10-02, OPUS: '00520E70'+0xA 'lea rdx, [00521050]', '00520E70'+0x11 'call 00426870')* | '"

```
00520E70  sub      rsp, 0x28
00520E74  movzx    ecx, word ptr [rcx]
00520E77  mov      r8, rdx
00520E7A  lea      rdx, [rip + 0x1cf]  ; -> 00521050
00520E81  call     0x426870  ; -> 00426870 fn
00520E86  mov      eax, 1
00520E8B  add      rsp, 0x28
00520E8F  ret      
```
