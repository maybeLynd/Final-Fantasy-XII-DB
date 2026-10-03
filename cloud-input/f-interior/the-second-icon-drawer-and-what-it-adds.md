# F-interior pack: `99-Unresolved-Residual/the-second-icon-drawer-and-what-it-adds.md`

Generated 2026-10-03 02:49 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/the-second-icon-drawer-and-what-it-adds.json`.

Functions: 2. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (inbox mentions: FABLE.md). OPUS read these before packing.

## 00181800 (106 B, extent 00181800-0018186A)

Page context: " calls: '00271450'/'002714A0'/'002714E0'/'002714C0' assemble a '[rbp-0x40]' record whose cursor writes '0x3001'/'0x47' tag pairs, then '002710C0'/'00271100'/'00271080'/'00270FF0' and the '00181560'..'00181800'/'002E0FA0' render helpers run the emit - the drawer's record assembly.  Interior anchor '00401639' (function '00401620').  '00400870' (323 B) is the quad builder '004006A0' calls: for 'edx' elements it loops 3 vertices per quad, r"

```
00181800  mov      qword ptr [rsp + 8], rbx
00181805  mov      qword ptr [rsp + 0x10], rbp
0018180A  mov      qword ptr [rsp + 0x18], rsi
0018180F  push     rdi
00181810  sub      rsp, 0x50
00181814  mov      ebx, r9d
00181817  mov      rdi, r8
0018181A  mov      esi, edx
0018181C  mov      ebp, ecx
0018181E  call     0x1b1c00  ; -> 001B1C00 fn
00181823  mov      rcx, rax
00181826  mov      r9, rdi
00181829  xor      eax, eax
0018182B  mov      r8d, esi
0018182E  mov      dword ptr [rsp + 0x48], eax
00181832  mov      edx, ebp
00181834  mov      dword ptr [rsp + 0x40], 1
0018183C  mov      dword ptr [rsp + 0x38], 1
00181844  mov      dword ptr [rsp + 0x30], eax
00181848  mov      dword ptr [rsp + 0x28], ebx
0018184C  mov      dword ptr [rsp + 0x20], eax
00181850  call     0x1b2410  ; -> 001B2410 fn
00181855  mov      rbx, qword ptr [rsp + 0x60]
0018185A  mov      rbp, qword ptr [rsp + 0x68]
0018185F  mov      rsi, qword ptr [rsp + 0x70]
00181864  add      rsp, 0x50
00181868  pop      rdi
00181869  ret      
```

## 00272310 (127 B, extent 00272310-0027238F)

Page context: "' and branches on whether anything survived. The fifth edge is '003EE420' (interior read 2026-09-17, SWE2-FRONTIER: 1,171 B — '002D8530' first at ['003EE481'](../_index/ADDRESS-INDEX.md), '003EEA80'/'00272310' ×2, carries the 'bt_win_0_c' battle-window texture name), a UI message handler dispatching on 'dword[rdx]', reaching '002DD2F0' itself. So the crossing is **one shared clip primitive with four callers on that layer, plus one calle"

```
00272310  mov      qword ptr [rsp + 0x18], rbx
00272315  push     rdi
00272316  sub      rsp, 0x50
0027231A  mov      rax, qword ptr [rip + 0x1cd250f]  ; -> 01F44830 [u64 0x00002B992DDFA232]
00272321  xor      rax, rsp
00272324  mov      qword ptr [rsp + 0x48], rax
00272329  mov      rdi, rdx
0027232C  mov      rbx, rcx
0027232F  lea      rdx, [rsp + 0x20]
00272334  call     0x246480  ; -> 00246480 fn
00272339  mov      rax, qword ptr [rsp + 0x20]
0027233E  mov      qword ptr [rdi], rax
00272341  test     rbx, rbx
00272344  je       0x272377  ; -> 00272377
00272346  mov      rbx, qword ptr [rbx + 0x10]
0027234A  test     rbx, rbx
0027234D  je       0x272377  ; -> 00272377
0027234F  nop      
00272350  lea      rdx, [rsp + 0x20]
00272355  mov      rcx, rbx
00272358  call     0x246480  ; -> 00246480 fn
0027235D  movzx    eax, word ptr [rsp + 0x20]
00272362  add      word ptr [rdi], ax
00272365  movzx    eax, word ptr [rsp + 0x22]
0027236A  add      word ptr [rdi + 2], ax
0027236E  mov      rbx, qword ptr [rbx + 0x10]
00272372  test     rbx, rbx
00272375  jne      0x272350  ; -> 00272350
00272377  mov      rcx, qword ptr [rsp + 0x48]
0027237C  xor      rcx, rsp
0027237F  call     0x808c40  ; -> 00808C40 fn
00272384  mov      rbx, qword ptr [rsp + 0x70]
00272389  add      rsp, 0x50
0027238D  pop      rdi
0027238E  ret      
```
