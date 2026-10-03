# Homing pack: `17-Presentation-Rendering/Graphics-Thread-Handshake/the-shared-command-state-word.md`

Generated 2026-10-03 12:18 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h10-the-shared-command-state-word.json`.

Bodies: 5. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

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

## 00253A10 (28 B, extent 00253A10-00253A2C)

Entered from (direct sites whose caller this page cites): `0022B6E0` + 0xA6 (call; `0022B6E0` is cited on this page)
Other direct sites: none

Host context: " | loop | owning function | |---|---| | '0022A850', '0022AE50' | '0022A770' | | '0022AFA0' | '0022AF50' | | '0022B040' | '0022B000' | | '0022B2C0' | **'MainLoop_Draw'** ('0022B0B0') | | '0022B720' | '0022B6E0' | | '0022B820' | '0022B7E0' | | '0022BAD0' | **'MainLoop_UpdateAndRenderFrame'** ('0022B8C0') | | '0022BD20' | '0022BC20' | | '00262AE0' | '002628B0' | | '0036F2D0' | 'GraphicsSync_ClearSharedCommandStateBits' ('0036F2C0') |  '002"

```
00253A10  sub      rsp, 0x28
00253A14  call     0x35c0d0  ; -> 0035C0D0 fn
00253A19  call     0x3ca2f0  ; -> 003CA2F0 fn
00253A1E  call     0x35dc60  ; -> 0035DC60 fn
00253A23  add      rsp, 0x28
00253A27  jmp      0x3c8a20  ; -> 003C8A20 fn
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
