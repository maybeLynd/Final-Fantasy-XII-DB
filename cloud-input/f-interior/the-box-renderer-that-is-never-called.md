# F-interior pack: `99-Unresolved-Residual/Dead-Nine-Patch-Renderer/the-box-renderer-that-is-never-called.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/the-box-renderer-that-is-never-called.json`.

Functions: 3. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (inbox mentions: FABLE.md, repos-9e.md). OPUS read these before packing.

## 0029B7D0 (50 B, extent 0029B7D0-0029B802)

Page context: "he '00296360' register/unregister rides the '003F89C0'/'003F8A30'/'003F8A50' registry family and '0028F590' accessor the UI layer shares ('00297C10'/'002962D0' siblings), and the installed callbacks '0029B7D0'/'0029B810' are themselves called by UI's '002973E0' - registry fan-in around the dead renderer, not a live UI dependency.  ### Interior citation — frontier hubs '002DAC70', '002753F0' (2026-09-18, SWE2-EC7)  '002DAC70' — 690 B, 7 "

```
0029B7D0  sub      rsp, 0x28
0029B7D4  mov      rax, r8
0029B7D7  mov      r8, qword ptr [rcx + 0x48]
0029B7DB  cmp      edx, 1
0029B7DE  jne      0x29b7fb  ; -> 0029B7FB
0029B7E0  mov      r9d, dword ptr [rax + 4]
0029B7E4  mov      r8d, dword ptr [r8 + 0x24]
0029B7E8  mov      edx, dword ptr [rax]
0029B7EA  call     0x2973e0  ; -> 002973E0 fn
0029B7EF  test     eax, eax
0029B7F1  jne      0x29b7fb  ; -> 0029B7FB
0029B7F3  or       eax, 0xffffffff
0029B7F6  add      rsp, 0x28
0029B7FA  ret      
0029B7FB  xor      eax, eax
0029B7FD  add      rsp, 0x28
0029B801  ret      
```

## 0029B810 (82 B, extent 0029B810-0029B862)

Page context: "0' register/unregister rides the '003F89C0'/'003F8A30'/'003F8A50' registry family and '0028F590' accessor the UI layer shares ('00297C10'/'002962D0' siblings), and the installed callbacks '0029B7D0'/'0029B810' are themselves called by UI's '002973E0' - registry fan-in around the dead renderer, not a live UI dependency.  ### Interior citation — frontier hubs '002DAC70', '002753F0' (2026-09-18, SWE2-EC7)  '002DAC70' — 690 B, 7 callers: th"

```
0029B810  sub      rsp, 0x28
0029B814  mov      r9, qword ptr [rcx + 0x48]
0029B818  mov      r10, r8
0029B81B  sub      edx, 1
0029B81E  je       0x29b836  ; -> 0029B836
0029B820  cmp      edx, 1
0029B823  jne      0x29b82f  ; -> 0029B82F
0029B825  mov      eax, dword ptr [r9 + 0x2c]
0029B829  shl      eax, 4
0029B82C  mov      dword ptr [rcx + 4], eax
0029B82F  xor      eax, eax
0029B831  add      rsp, 0x28
0029B835  ret      
0029B836  movzx    eax, byte ptr [r9 + 0x87]
0029B83E  mov      r8d, dword ptr [r9 + 0x30]
0029B842  test     eax, eax
0029B844  je       0x29b84a  ; -> 0029B84A
0029B846  imul     r8d, eax
0029B84A  mov      r9d, dword ptr [r10 + 4]
0029B84E  mov      edx, dword ptr [r10]
0029B851  call     0x2973e0  ; -> 002973E0 fn
0029B856  test     eax, eax
0029B858  jne      0x29b82f  ; -> 0029B82F
0029B85A  or       eax, 0xffffffff
0029B85D  add      rsp, 0x28
0029B861  ret      
```

## 002C0B40 (148 B, extent 002C0B40-002C0BD4)

Page context: "d becomes 0 in two ways:         - the node or an ancestor has opacity 0;         - a message-3 handler scales it to 0. Two are read here: '002C0BE0' scales by '+0xEA' when '+0xEC' bit 1 is set, and '002C0B40' scales by '+0xDA'. The other message-3 handlers (28 in [the protocol census](../../16-UI/Widget-Object-Model/the-widget-message-protocol.md)) are not read.       - **Evidence: STATIC + NATIVE-REPLAY** in [uq351-opus-replay-widget-"

```
002C0B40  push     rbx
002C0B42  sub      rsp, 0x20
002C0B46  mov      rbx, rcx
002C0B49  mov      ecx, dword ptr [rdx]
002C0B4B  sub      ecx, 1
002C0B4E  je       0x2c0b98  ; -> 002C0B98
002C0B50  cmp      ecx, 2
002C0B53  je       0x2c0b62  ; -> 002C0B62
002C0B55  mov      rcx, rbx
002C0B58  add      rsp, 0x20
002C0B5C  pop      rbx
002C0B5D  jmp      0x5c5230  ; -> 005C5230 fn
002C0B62  mov      rdx, qword ptr [rbx + 0x38]
002C0B66  movsx    ecx, word ptr [rbx + 0xd8]
002C0B6D  movsx    eax, word ptr [rdx + 0x5a]
002C0B71  imul     ecx, eax
002C0B74  movsx    eax, word ptr [rdx + 0x58]
002C0B78  sar      ecx, 7
002C0B7B  mov      word ptr [rdx + 0x5a], cx
002C0B7F  movsx    ecx, word ptr [rbx + 0xda]
002C0B86  imul     ecx, eax
002C0B89  sar      ecx, 7
002C0B8C  mov      word ptr [rdx + 0x58], cx
002C0B90  xor      eax, eax
002C0B92  add      rsp, 0x20
002C0B96  pop      rbx
002C0B97  ret      
002C0B98  mov      rax, qword ptr [rdx + 8]
002C0B9C  mov      rcx, qword ptr [rax]
002C0B9F  and      dword ptr [rbx + 0x40], 0xffffff7f
002C0BA6  mov      qword ptr [rbx + 0xc0], rcx
002C0BAD  mov      ecx, 1
002C0BB2  call     0x2735e0  ; -> 002735E0 fn
002C0BB7  mov      rdx, rax
002C0BBA  mov      rcx, rbx
002C0BBD  call     0x247570  ; -> 00247570 fn
002C0BC2  xor      eax, eax
002C0BC4  mov      dword ptr [rbx + 0xd8], 0x800080
002C0BCE  add      rsp, 0x20
002C0BD2  pop      rbx
002C0BD3  ret      
```
