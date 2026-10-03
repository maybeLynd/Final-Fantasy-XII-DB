# Homing pack: `16-UI/Message-Windows/the-message-window-layout-readers.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-message-window-layout-readers.json`.

Bodies: 3. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002A2BB0 (61 B, extent 002A2BB0-002A2BED)

Entered from (direct sites whose caller this page cites): `0035E070` + 0x62 (call; `0035E070` is cited on this page)
Other direct sites: none

Host context: "r-installations-censused   last_pass_kind: attack   crossref_clean: false   reopened_count: 0 addresses:   - "002A6190"   - "002A86A0"   - "002A3960"   - "002BE4F0"   - "002BF690"   - "002D66D0"   - "0035E070" ---  # The message-window layout-key readers  **Status:** ~~PARTIAL~~ DOCUMENTED *(corrected 2026-10-02, OPUS: the front matter says 'status: DOCUMENTED')* — this page documents where each 'uisize.json' key of the message families"

```
002A2BB0  test     rcx, rcx
002A2BB3  je       0x2a2bea  ; -> 002A2BEA
002A2BB5  movsx    rax, byte ptr [rcx + 0x3b8]
002A2BBD  lea      r9, [rip + 0x1df990c]  ; -> 0209C4D0
002A2BC4  xor      r8d, r8d
002A2BC7  mov      edx, r8d
002A2BCA  cmp      dword ptr [r9 + rax*8], ecx
002A2BCE  sete     dl
002A2BD1  test     edx, edx
002A2BD3  je       0x2a2bea  ; -> 002A2BEA
002A2BD5  cmp      qword ptr [rcx], r8
002A2BD8  jne      0x2a2be0  ; -> 002A2BE0
002A2BDA  test     byte ptr [rcx + 0x7c], 0xf
002A2BDE  je       0x2a2be6  ; -> 002A2BE6
002A2BE0  mov      r8d, 1
002A2BE6  mov      eax, r8d
002A2BE9  ret      
002A2BEA  xor      eax, eax
002A2BEC  ret      
```

## 002A7D30 (231 B, extent 002A7D30-002A7E17)

Entered from (direct sites whose caller this page cites): `002A36A0` + 0x50 (call; `002A36A0` is cited on this page)
Other direct sites: none

Host context: "to '0x80', a six-arm jump table on 'byte[+0x180] - 1' loops '002ABEC0' dispatches (one arm sets 'word[+0x158] = 1' first) or '002B3950'/'0016D6A0(0x40000)' exits, and a nonzero 'esi' afterwards runs '002A36A0' - the state-byte loop the window refresh drives. Interior anchor '002A3790' (the dispatch loop head).  '002A5CC0' (638 B) is the layout recompute the message-window proc '002A6190' calls: '002D3900' on '[rcx+0xC0]' then '002B3930'"

```
002A7D30  sub      rsp, 0x28
002A7D34  mov      eax, dword ptr [rcx + 8]
002A7D37  test     al, 4
002A7D39  je       0x2a7d4e  ; -> 002A7D4E
002A7D3B  and      eax, 0xfffffffb
002A7D3E  mov      dword ptr [rcx + 8], eax
002A7D41  movzx    eax, byte ptr [rcx + 0x2f]
002A7D45  mov      word ptr [rcx + 0x16], ax
002A7D49  call     0x2a7a60  ; -> 002A7A60 fn
002A7D4E  mov      eax, dword ptr [rcx + 8]
002A7D51  test     al, 0x10
002A7D53  je       0x2a7d79  ; -> 002A7D79
002A7D55  and      eax, 0xffffffef
002A7D58  mov      dword ptr [rcx + 8], eax
002A7D5B  movss    xmm0, dword ptr [rcx + 0x4c]
002A7D60  addss    xmm0, dword ptr [rcx + 0x48]
002A7D65  movss    dword ptr [rcx + 0x24], xmm0
002A7D6A  movss    xmm1, dword ptr [rcx + 0x54]
002A7D6F  addss    xmm1, dword ptr [rcx + 0x50]
002A7D74  movss    dword ptr [rcx + 0x28], xmm1
002A7D79  mov      eax, dword ptr [rcx + 8]
002A7D7C  test     al, 8
002A7D7E  je       0x2a7e12  ; -> 002A7E12
002A7D84  and      eax, 0xfffffff7
002A7D87  mov      dword ptr [rcx + 8], eax
002A7D8A  movsx    eax, word ptr [rcx + 0x38]
002A7D8E  movd     xmm1, eax
002A7D92  movzx    eax, byte ptr [rcx + 0x34]
002A7D96  cvtdq2ps xmm1, xmm1
002A7D99  movd     xmm0, eax
002A7D9D  cvtdq2ps xmm0, xmm0
002A7DA0  addss    xmm1, xmm0
002A7DA4  cvttss2si rax, xmm1
002A7DA9  mov      byte ptr [rcx + 0x20], al
002A7DAC  movsx    eax, word ptr [rcx + 0x3a]
002A7DB0  movd     xmm1, eax
002A7DB4  movzx    eax, byte ptr [rcx + 0x35]
002A7DB8  cvtdq2ps xmm1, xmm1
002A7DBB  movd     xmm0, eax
002A7DBF  cvtdq2ps xmm0, xmm0
002A7DC2  addss    xmm1, xmm0
002A7DC6  cvttss2si rax, xmm1
002A7DCB  mov      byte ptr [rcx + 0x21], al
002A7DCE  movsx    eax, word ptr [rcx + 0x3c]
002A7DD2  movd     xmm1, eax
002A7DD6  movzx    eax, byte ptr [rcx + 0x36]
002A7DDA  cvtdq2ps xmm1, xmm1
002A7DDD  movd     xmm0, eax
002A7DE1  cvtdq2ps xmm0, xmm0
002A7DE4  addss    xmm1, xmm0
002A7DE8  cvttss2si rax, xmm1
002A7DED  mov      byte ptr [rcx + 0x22], al
002A7DF0  movsx    eax, word ptr [rcx + 0x3e]
002A7DF4  movd     xmm1, eax
002A7DF8  movzx    eax, byte ptr [rcx + 0x37]
002A7DFC  cvtdq2ps xmm1, xmm1
002A7DFF  movd     xmm0, eax
002A7E03  cvtdq2ps xmm0, xmm0
002A7E06  addss    xmm1, xmm0
002A7E0A  cvttss2si rax, xmm1
002A7E0F  mov      byte ptr [rcx + 0x23], al
002A7E12  add      rsp, 0x28
002A7E16  ret      
```

## 002A84B0 (55 B, extent 002A84B0-002A84E7)

Entered from (direct sites whose caller this page cites): `002A7F70` + 0x51 (call; `002A7F70` is cited on this page); `002A7F70` + 0xE6 (call; `002A7F70` is cited on this page)
Other direct sites: none

Host context: "nalOffsetY' ('002A6190+0x400') and 'MessageWinMaskTop' ('002A6190+0x738') *(corrected 2026-10-02, OPUS: the 'layout-key-readers.tsv' rows, each read at the bytes)*; its helpers '002A4170'/'002A4430'/'002A7F70'/'002A8100'/'002A8220' feed it (below) | | '002A4170' (→'002A6190') | 'MsgWinCaptionBaseOffsetX/Y', 'SystemWindowCaptionOffsetX/Y', 'NobuMessageItemGetOffsetY' | caption bases → 'xmm7'/'xmm0'/'xmm6'/'xmm1' floats — the caption draw" / "nalOffsetY' ('002A6190+0x400') and 'MessageWinMaskTop' ('002A6190+0x738') *(corrected 2026-10-02, OPUS: the 'layout-key-readers.tsv' rows, each read at the bytes)*; its helpers '002A4170'/'002A4430'/'002A7F70'/'002A8100'/'002A8220' feed it (below) | | '002A4170' (→'002A6190') | 'MsgWinCaptionBaseOffsetX/Y', 'SystemWindowCaptionOffsetX/Y', 'NobuMessageItemGetOffsetY' | caption bases → 'xmm7'/'xmm0'/'xmm6'/'xmm1' floats — the caption draw"

```
002A84B0  test     rcx, rcx
002A84B3  je       0x2a84e6  ; -> 002A84E6
002A84B5  push     rbx
002A84B6  sub      rsp, 0x20
002A84BA  mov      eax, dword ptr [rcx + 0x7c]
002A84BD  lea      rdx, [rip + 0x66dfcc]  ; -> 00916490
002A84C4  and      eax, 0x3ff
002A84C9  mov      rbx, rcx
002A84CC  or       eax, 0x19064c00
002A84D1  mov      dword ptr [rcx + 0x7c], eax
002A84D4  call     0x247570  ; -> 00247570 fn
002A84D9  mov      rcx, rbx
002A84DC  call     0x244f00  ; -> 00244F00 fn
002A84E1  add      rsp, 0x20
002A84E5  pop      rbx
002A84E6  ret      
```
