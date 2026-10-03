# Homing pack: `17-Presentation-Rendering/Graphics-Thread-Handshake/the-shared-command-state-word.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-shared-command-state-word.json`.

Bodies: 8. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001823E0 (38 B, extent 001823E0-00182406)

Entered from (direct sites whose caller this page cites): `001B2530` + 0x3A (call; `001B2530` is cited on this page)
Other direct sites: `001B2600` + 0x21 (jmp)

Host context: "35' (the '+0xB50' table read).  ## SWE2-EC7-112 update (2026-09-20) - the '0018CA40'/'01F7F538' family measured  '00182250' (34 B) and '00182220' (44 B) are the two arms '0022B0B0' / '0022B8C0' (and '001B2530', '001EC060', '001FBD80' for the first) run: both fetch the '0018CA40' object - '00182250' unconditionally calls '0018B5D0(obj, 0)', '00182220' calls '0018B670(obj, 0)' only when the object is live - and both latch 'dword[01F7F538]"

```
001823E0  push     rbx
001823E2  sub      rsp, 0x20
001823E6  mov      ebx, ecx
001823E8  mov      dword ptr [rip + 0x1dfd146], 0  ; -> 01F7F538
001823F2  call     0x18ca40  ; -> 0018CA40 fn
001823F7  mov      rcx, rax
001823FA  mov      edx, ebx
001823FC  add      rsp, 0x20
00182400  pop      rbx
00182401  jmp      0x18bdd0  ; -> 0018BDD0 fn
```

## 0018D5F0 (49 B, extent 0018D5F0-0018D621)

Entered from (direct sites whose caller this page cites): `00214C30` + 0x36 (call; `00214C30` is cited on this page)
Other direct sites: none

Host context: " clear each byte becomes '0xF9' or '6' per its own bit - the two-byte publish the handshake record carries. Interior anchor '0024781B' (the '+0x44' shift-out).  ## SWE2-EC7-109 update (2026-09-20) - '00214C30' measured  '00214C30' (898 B) is the display-state synchronizer '0022A580' and '0022B0B0' call: stack-cookie guarded, 'ecx' is the mode ('movsxd rbp'), and the '01FD3AE0'..'01FD3B14' block is the shared command state. Mode 0 re-syn"

```
0018D5F0  movzx    eax, byte ptr [rcx + 0x110]
0018D5F7  mov      byte ptr [rdx], al
0018D5F9  mov      eax, dword ptr [rcx + 0x114]
0018D5FF  mov      dword ptr [rdx + 4], eax
0018D602  mov      eax, dword ptr [rcx + 0x118]
0018D608  mov      dword ptr [rdx + 8], eax
0018D60B  mov      eax, dword ptr [rcx + 0x11c]
0018D611  mov      dword ptr [rdx + 0xc], eax
0018D614  mov      eax, dword ptr [rcx + 0x120]
0018D61A  mov      dword ptr [rdx + 0x10], eax
0018D61D  mov      rax, rdx
0018D620  ret      
```

## 001C53B0 (24 B, extent 001C53B0-001C53C8)

Entered from (direct sites whose caller this page cites): `00214C30` + 0x20 (call; `00214C30` is cited on this page)
Other direct sites: none

Host context: " clear each byte becomes '0xF9' or '6' per its own bit - the two-byte publish the handshake record carries. Interior anchor '0024781B' (the '+0x44' shift-out).  ## SWE2-EC7-109 update (2026-09-20) - '00214C30' measured  '00214C30' (898 B) is the display-state synchronizer '0022A580' and '0022B0B0' call: stack-cookie guarded, 'ecx' is the mode ('movsxd rbp'), and the '01FD3AE0'..'01FD3B14' block is the shared command state. Mode 0 re-syn"

```
001C53B0  cmp      byte ptr [rip + 0x1dbbec9], 0  ; -> 01F81280
001C53B7  je       0x1c53c5  ; -> 001C53C5
001C53B9  cmp      byte ptr [rip + 0x1dbbec1], 0  ; -> 01F81281
001C53C0  jne      0x1c53c5  ; -> 001C53C5
001C53C2  mov      al, 1
001C53C4  ret      
001C53C5  xor      al, al
001C53C7  ret      
```

## 001C53D0 (24 B, extent 001C53D0-001C53E8)

Entered from (direct sites whose caller this page cites): `00214C30` + 0x6A (call; `00214C30` is cited on this page)
Other direct sites: none

Host context: " clear each byte becomes '0xF9' or '6' per its own bit - the two-byte publish the handshake record carries. Interior anchor '0024781B' (the '+0x44' shift-out).  ## SWE2-EC7-109 update (2026-09-20) - '00214C30' measured  '00214C30' (898 B) is the display-state synchronizer '0022A580' and '0022B0B0' call: stack-cookie guarded, 'ecx' is the mode ('movsxd rbp'), and the '01FD3AE0'..'01FD3B14' block is the shared command state. Mode 0 re-syn"

```
001C53D0  cmp      byte ptr [rip + 0x1dbbeaa], 0  ; -> 01F81281
001C53D7  je       0x1c53e5  ; -> 001C53E5
001C53D9  cmp      byte ptr [rip + 0x1dbbea0], 0  ; -> 01F81280
001C53E0  jne      0x1c53e5  ; -> 001C53E5
001C53E2  mov      al, 1
001C53E4  ret      
001C53E5  xor      al, al
001C53E7  ret      
```

## 001EBF90 (108 B, extent 001EBF90-001EBFFC)

Entered from (direct sites whose caller this page cites): `00181E30` + 0x10 (jmp; `00181E30` is cited on this page)
Other direct sites: none

Host context: "(an '0016D6A0' call).  ## SWE2-EC7-45 update (2026-09-19) - '0022BEB0'  '0022BEB0' (238 B) is the 'VFXSystem_RenderLayerPass' root - '0017F2F0'/'0017F370'/'00181AB0'/'00181C10'/'00181C70'/'00181DD0'/'00181E30'. Interior anchor '0022BEB4' (an '0017F2F0' call).  ## SWE2-EC7-54 update (2026-09-19) - '001AE550'  '001AE550' (347 B) is a shared-command-state body - '001A4BF0'/'001AEC30'/'001EDF00' plus two vcalls, '008F6600'/'02EBA2E0'/'02EBA"

```
001EBF90  cmp      qword ptr [rcx], 0
001EBF94  je       0x1ebffb  ; -> 001EBFFB
001EBF96  mov      rax, qword ptr [rcx + 0x270]
001EBF9D  xor      r8d, r8d
001EBFA0  cmp      byte ptr [rax + 8], r8b
001EBFA4  jne      0x1ebfab  ; -> 001EBFAB
001EBFA6  mov      rdx, qword ptr [rax]
001EBFA9  jmp      0x1ebfae  ; -> 001EBFAE
001EBFAB  mov      rdx, r8
001EBFAE  mov      qword ptr [rcx], rdx
001EBFB1  cmp      byte ptr [rcx + 0x26e], r8b
001EBFB8  jne      0x1ebff3  ; -> 001EBFF3
001EBFBA  inc      dword ptr [rcx + 8]
001EBFBD  mov      eax, dword ptr [rcx + 8]
001EBFC0  cmp      eax, dword ptr [rcx + 0x10]
001EBFC3  jge      0x1ebfdc  ; -> 001EBFDC
001EBFC5  movss    xmm0, dword ptr [rcx + 0x18]
001EBFCA  mov      rdx, rcx
001EBFCD  addss    xmm0, dword ptr [rcx + 0x14]
001EBFD2  movss    dword ptr [rcx + 0x14], xmm0
001EBFD7  jmp      0x1eb800  ; -> 001EB800 fn
001EBFDC  xorps    xmm0, xmm0
001EBFDF  comiss   xmm0, dword ptr [rcx + 0x14]
001EBFE3  jbe      0x1ebfe9  ; -> 001EBFE9
001EBFE5  mov      dword ptr [rcx + 0x14], r8d
001EBFE9  mov      dword ptr [rcx + 0x10], 0xffffffff
001EBFF0  mov      qword ptr [rcx], r8
001EBFF3  mov      rdx, rcx
001EBFF6  jmp      0x1eb800  ; -> 001EB800 fn
001EBFFB  ret      
```

## 002EF1B0 (83 B, extent 002EF1B0-002EF203)

Entered from (direct sites whose caller this page cites): `001EC060` + 0x3CF (call; `001EC060` is cited on this page)
Other direct sites: none

Host context: "xB50' table read).  ## SWE2-EC7-112 update (2026-09-20) - the '0018CA40'/'01F7F538' family measured  '00182250' (34 B) and '00182220' (44 B) are the two arms '0022B0B0' / '0022B8C0' (and '001B2530', '001EC060', '001FBD80' for the first) run: both fetch the '0018CA40' object - '00182250' unconditionally calls '0018B5D0(obj, 0)', '00182220' calls '0018B670(obj, 0)' only when the object is live - and both latch 'dword[01F7F538] = 1'. The f"

```
002EF1B0  push     rbx
002EF1B2  sub      rsp, 0x30
002EF1B6  movsx    ebx, cx
002EF1B9  mov      ecx, ebx
002EF1BB  movaps   xmmword ptr [rsp + 0x20], xmm6
002EF1C0  movaps   xmm6, xmm1
002EF1C3  call     0x3ec580  ; -> 003EC580 fn
002EF1C8  test     rax, rax
002EF1CB  je       0x2ef1f8  ; -> 002EF1F8
002EF1CD  cmp      bx, -1
002EF1D1  je       0x2ef1f8  ; -> 002EF1F8
002EF1D3  movsx    rax, bx
002EF1D7  imul     rcx, rax, 0x740
002EF1DE  add      rcx, qword ptr [rip + 0x1fd7d43]  ; -> 022C6F28
002EF1E5  je       0x2ef1f8  ; -> 002EF1F8
002EF1E7  cmp      dword ptr [rcx + 0x284], 0
002EF1EE  je       0x2ef1f8  ; -> 002EF1F8
002EF1F0  movaps   xmm1, xmm6
002EF1F3  call     0x420a10  ; -> 00420A10 fn
002EF1F8  movaps   xmm6, xmmword ptr [rsp + 0x20]
002EF1FD  add      rsp, 0x30
002EF201  pop      rbx
002EF202  ret      
```

## 0036CAD0 (38 B, extent 0036CAD0-0036CAF6)

Entered from (direct sites whose caller this page cites): `00251E00` + 0x5D (call; `00251E00` is cited on this page)
Other direct sites: `0050EF00` + 0x2C (call)

Host context: "5E9EC0' constant address into '02C0A444' - the open/close pointer pair the walk's callers rely on. Interior anchors '00370DF7' and '00370DE7' (the two stores).  ## SWE2-EC7-106 update (2026-09-20) - '00251E00' + '002512B0' measured  '00251E00' (117 B) is the backing-buffer resize '0022AF50' and '0022B000' run on the '020927F0' record: gated on 'word[+0xE4] <= 1', it computes 'w = (dword[022D8EAC] + 0xFF) >> 8' and 'h = (dword[022D8EB4] "

```
0036CAD0  sub      rsp, 0x38
0036CAD4  mov      r8d, edx
0036CAD7  mov      qword ptr [rsp + 0x20], 0
0036CAE0  mov      rdx, rcx
0036CAE3  xor      r9d, r9d
0036CAE6  mov      ecx, dword ptr [rip + 0x1f6bed0]  ; -> 022D89BC
0036CAEC  call     0x36d050  ; -> 0036D050 fn
0036CAF1  add      rsp, 0x38
0036CAF5  ret      
```

## 00375F20 (82 B, extent 00375F20-00375F72)

Entered from (direct sites whose caller this page cites): `0022B000` + 0x64 (call; `0022B000` is cited on this page)
Other direct sites: none

Host context: "ist in '.text', and all eleven spin on '0x02EBA3F8'** (corrected 2026-09-13):  | loop | owning function | |---|---| | '0022A850', '0022AE50' | '0022A770' | | '0022AFA0' | '0022AF50' | | '0022B040' | '0022B000' | | '0022B2C0' | **'MainLoop_Draw'** ('0022B0B0') | | '0022B720' | '0022B6E0' | | '0022B820' | '0022B7E0' | | '0022BAD0' | **'MainLoop_UpdateAndRenderFrame'** ('0022B8C0') | | '0022BD20' | '0022BC20' | | '00262AE0' | '002628B0' | "

```
00375F20  lea      rax, [rip + 0x2b49ac9]  ; -> 02EBF9F0
00375F27  lea      rcx, [rip + 0x2b4a8c2]  ; -> 02EC07F0
00375F2E  nop      
00375F30  cmp      dword ptr [rax + 0x58], 0
00375F34  je       0x375f71  ; -> 00375F71
00375F36  or       dword ptr [rax], 1
00375F39  cmp      dword ptr [rax + 0xc8], 0
00375F40  je       0x375f71  ; -> 00375F71
00375F42  or       dword ptr [rax + 0x70], 1
00375F46  cmp      dword ptr [rax + 0x138], 0
00375F4D  je       0x375f71  ; -> 00375F71
00375F4F  or       dword ptr [rax + 0xe0], 1
00375F56  cmp      dword ptr [rax + 0x1a8], 0
00375F5D  je       0x375f71  ; -> 00375F71
00375F5F  or       dword ptr [rax + 0x150], 1
00375F66  add      rax, 0x1c0
00375F6C  cmp      rax, rcx
00375F6F  jl       0x375f30  ; -> 00375F30
00375F71  ret      
```
