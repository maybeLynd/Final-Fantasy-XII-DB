# F-interior pack: `17-Presentation-Rendering/CONTRACT-render-command-list-and-graphics-handshake.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/contract-render-command-list-and-graphics-handshake.json`.

Functions: 4. Each is cited on the page only at its entry and is still in the F frontier.

## 0018B030 (15 B, extent 0018B030-0018B03F)

Page context: "lk runs; see §14.2   +0x2B  u8      (pad)              never written, never read; aligns reverseMark to +0x2C   +0x2C  s32     reverseMark        0xFFFFFFFF at construction and on every clear; set by 0018B030  RenderCommandOwnerList             [01F7F5E8], 0x20 bytes, malloc'd at 0018C9FE   +0x00  void**  pBegin   +0x08  void**  pEnd   +0x10  void**  pCapacityEnd   +0x18  void*   allocatorVftable   same allocator construction, same disc"

```
0018B030  mov      rax, qword ptr [rcx + 8]
0018B034  sub      rax, qword ptr [rcx]
0018B037  sar      rax, 3
0018B03B  mov      dword ptr [rcx + 0x2c], eax
0018B03E  ret      
```

## 0018CB10 (28 B, extent 0018CB10-0018CB2C)

Page context: "nce per process** | | empty | accumulating | any enqueue; the push_back's capacity test at '0018C660' never takes the grow arm in practice (I-3) | | accumulating | split | '0018B510' via the wrapper '0018CB10' — the only caller | | accumulating | marked | '0018B030' via the wrapper '001829F0' — the only caller | | accumulating | part 1 run | '0018B100(dl != 0)'; entries '[0, split)' whose key ANDs with 'classMask' | | part 1 run | part "

```
0018CB10  push     rbx
0018CB12  sub      rsp, 0x20
0018CB16  mov      ebx, edx
0018CB18  call     0x18b4e0  ; -> 0018B4E0 fn
0018CB1D  mov      rcx, rax
0018CB20  mov      edx, ebx
0018CB22  add      rsp, 0x20
0018CB26  pop      rbx
0018CB27  jmp      0x18b510  ; -> 0018B510 fn
```

## 001A14D0 (9 B, extent 001A14D0-001A14D9)

Page context: "018B040', '0018CA40', '0018B810') and the flush '0018C8F0'. - **The frame reset** '0017D6E0' calls '001E0590'. Both are frame-order bodies filed in the scheduling layer, as are   '001E0590''s leaves '001A14D0' and '001DB620'. - **The handshake clear** 'GraphicsSync_ClearSharedCommandStateBits' ('0036F2C0') is called by   'MainLoop_UpdateAndRenderFrame' and by six scheduler bodies ('0022A770', '0022AF50', '0022B000', '0022B6E0' among   t"

```
001A14D0  mov      rax, qword ptr [rcx + 0x18]
001A14D4  mov      qword ptr [rcx + 8], rax
001A14D8  ret      
```

## 00212C60 (14 B, extent 00212C60-00212C6E)

Page context: "ALUE (GC-3, OPUS;    confirmed SWE2-CONTRACT).** The field is a **nullable execute-target pointer** that two    slot-1 execute bodies read and forward as the callee's 'this':    'MapOrderedObject''s '00212C60' ('mov rcx,[rcx+8]; test rcx,rcx; jne 001E2AF0' — the    null-gated map draw delegate, also base vtable '009010B8' slot 5) and    'CharacterOrderedObject''s '00215320' ('mov rcx,[rcx+8]; jmp 001F5D70' — unconditional,    the routin"

```
00212C60  mov      rcx, qword ptr [rcx + 8]
00212C64  test     rcx, rcx
00212C67  jne      0x1e2af0  ; -> 001E2AF0 fn
00212C6D  ret      
```
