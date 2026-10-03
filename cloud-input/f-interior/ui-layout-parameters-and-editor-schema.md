# F-interior pack: `16-UI/Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md`

Generated 2026-10-02 20:18 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/ui-layout-parameters-and-editor-schema.json`.

Functions: 12. Each is cited on the page only at its entry and is still in the F frontier.

## 0024B100 (29 B, extent 0024B100-0024B11D)

Page context: "') or 'JsonData/UISize/UISize_sd.json' when it is zero ('001C6D33'–'001C6D5B'). > The byte has **one setter**, '001B24B0', reached through '00184660' (which also re-runs > '0024B120', '00248410' and '0024B100' after the store — the re-layout hooks), and '00184660' has > two callers: the boot function '0022A0B0' at '0022A120', which passes **the dword at '01E0280C'**, > and the debug menu '001D1660' at '001D1F46'–'001D1F50', which passes"

```
0024B100  movzx    eax, word ptr [rip + 0x1bc10d1]  ; -> 01E0C1D8 [u16 0x0200]
0024B107  mov      word ptr [rip + 0x1bc10c6], ax  ; -> 01E0C1D4 [u16 0x0200]
0024B10E  movzx    eax, word ptr [rip + 0x1bc10c7]  ; -> 01E0C1DC [u16 0x01C0]
0024B115  mov      word ptr [rip + 0x1bc10ba], ax  ; -> 01E0C1D6 [u16 0x01C0]
0024B11C  ret      
```

## 0024B120 (46 B, extent 0024B120-0024B14E)

Page context: "ero > ('001C6C4A'–'001C6C8A') or 'JsonData/UISize/UISize_sd.json' when it is zero ('001C6D33'–'001C6D5B'). > The byte has **one setter**, '001B24B0', reached through '00184660' (which also re-runs > '0024B120', '00248410' and '0024B100' after the store — the re-layout hooks), and '00184660' has > two callers: the boot function '0022A0B0' at '0022A120', which passes **the dword at '01E0280C'**, > and the debug menu '001D1660' at '001D1F4"

```
0024B120  test     ecx, ecx
0024B122  je       0x24b139  ; -> 0024B139
0024B124  mov      dword ptr [rip + 0x1bc10aa], 0x780  ; -> 01E0C1D8 [u32 0x00000200]
0024B12E  mov      dword ptr [rip + 0x1bc10a4], 0x438  ; -> 01E0C1DC [u32 0x000001C0]
0024B138  ret      
0024B139  mov      dword ptr [rip + 0x1bc1095], 0x200  ; -> 01E0C1D8 [u32 0x00000200]
0024B143  mov      dword ptr [rip + 0x1bc108f], 0x1c0  ; -> 01E0C1DC [u32 0x000001C0]
0024B14D  ret      
```

## 002716F0 (35 B, extent 002716F0-00271713)

Page context: "es ('00241D40', '00281ED0', '002A3960', '002A6190', '002A70B0', '002C2320', …); the rest are '00249CA0' via '00241D40', '001DBB00'/'002DEBA0' via '001D1660', '002DEE50' via '002814E0' and '00271500'/'002716F0' via '002D5EB0'. '00249C60' is a generic query helper the census attributes to Audio — the same fan-in appears on the menu-screen-atlas row — not an audio relationship the layout schema owns.  **ActorEntity — MECHANICAL (SWE2-CONTR"

```
002716F0  test     ecx, ecx
002716F2  js       0x271712  ; -> 00271712
002716F4  push     rbx
002716F5  sub      rsp, 0x20
002716F9  mov      ebx, ecx
002716FB  call     0x2dee80  ; -> 002DEE80 fn
00271700  test     eax, eax
00271702  je       0x27170d  ; -> 0027170D
00271704  xor      edx, edx
00271706  mov      ecx, ebx
00271708  call     0x2df0f0  ; -> 002DF0F0 fn
0027170D  add      rsp, 0x20
00271711  pop      rbx
00271712  ret      
```

## 0028D260 (497 B, extent 0028D260-0028D451)

Page context: "and '+0xD8' ('0039BB60'), then '0017FA70' and '00473B50'/'00473B60' - the layout record's release sweep.  Interior anchor '0037F87D' (function '0037F860').  '0028CB90' (381 B) is the interval lookup '0028D260'/'0028D460' call: an 'r8d'-bounded bisect over word pairs at 'rbx' - 'word[rbx + 6] > r9d' descends left, 'word[rbx + 0xE] <= r9d' ascends right - then '00861F0E' twice and '002752E0' - the layout's range search.  Interior anchor '"

```
0028D260  mov      qword ptr [rsp + 0x20], rbp
0028D265  push     rdi
0028D266  push     r14
0028D268  push     r15
0028D26A  sub      rsp, 0x30
0028D26E  test     byte ptr [rcx + 0x28], 1
0028D272  mov      rdi, r9
0028D275  mov      r15, r8
0028D278  mov      r14, rdx
0028D27B  mov      rbp, rcx
0028D27E  je       0x28d442  ; -> 0028D442
0028D284  movzx    eax, byte ptr [rcx + 0x2a]
0028D288  mov      qword ptr [rsp + 0x58], rbx
0028D28D  movsx    ebx, word ptr [rdx + 0x76]
0028D291  imul     ebx, eax
0028D294  sar      ebx, 7
0028D297  test     ebx, ebx
0028D299  je       0x28d43d  ; -> 0028D43D
0028D29F  movss    xmm0, dword ptr [rdx + 0x70]
0028D2A4  mov      qword ptr [rsp + 0x60], rsi
0028D2A9  call     0x28cd10  ; -> 0028CD10 fn
0028D2AE  mov      esi, eax
0028D2B0  mov      rcx, rdi
0028D2B3  imul     esi, dword ptr [rbp + 0x2c]
0028D2B7  sar      esi, 8
0028D2BA  sub      esi, -0x80
0028D2BD  call     0x3f0040  ; -> 003F0040 fn
0028D2C2  mov      rdi, rax
0028D2C5  test     rax, rax
0028D2C8  je       0x28d438  ; -> 0028D438
0028D2CE  mov      r9d, dword ptr [rbp + 0x2c]
0028D2D2  lea      rdx, [rip + 0x688cd7]  ; -> 00915FB0
0028D2D9  mov      r8d, 4
0028D2DF  lea      rcx, [rsp + 0x50]
0028D2E4  call     0x28cb90  ; -> 0028CB90 fn
0028D2E9  movss    xmm0, dword ptr [rbp + 0x20]
0028D2EE  mulss    xmm0, dword ptr [rip + 0x638c7a]  ; -> 008C5F70 [f32 1.570796]
0028D2F6  call     0x861f0e  ; -> 00861F0E fn
0028D2FB  movaps   xmm3, xmm0
0028D2FE  lea      r8, [rbp + 0x10]
0028D302  mov      rdx, rbp
0028D305  mov      rcx, rdi
0028D308  call     0x275490  ; -> 00275490 fn
0028D30D  movsx    edx, word ptr [rsp + 0x54]
0028D312  mov      r8d, 0xff
0028D318  movsx    ecx, word ptr [rsp + 0x56]
0028D31D  imul     edx, ebx
0028D320  imul     ecx, esi
0028D323  mov      dword ptr [rdi + 0xc], 0xbf800000
0028D32A  sar      edx, 7
0028D32D  sar      ecx, 7
0028D330  imul     edx, esi
0028D333  mov      eax, ecx
0028D335  mov      dword ptr [rdi + 0x44], ecx
0028D338  mov      dword ptr [rdi + 0x48], ecx
0028D33B  sar      edx, 7
0028D33E  cmp      ecx, r8d
0028D341  mov      dword ptr [rdi + 0x4c], edx
0028D344  cmovg    eax, r8d
0028D348  mov      dword ptr [rdi + 0x40], eax
0028D34B  jle      0x28d355  ; -> 0028D355
0028D34D  mov      dword ptr [rdi + 0x44], r8d
0028D351  mov      dword ptr [rdi + 0x48], r8d
0028D355  cmp      edx, r8d
0028D358  mov      eax, edx
0028D35A  cmovg    eax, r8d
0028D35E  mov      dword ptr [rdi + 0x4c], eax
0028D361  movzx    ebx, word ptr [rbp + 0x28]
0028D365  shr      ebx, 2
0028D368  and      ebx, 1
0028D36B  call     0x35d480  ; -> 0035D480 fn
0028D370  mov      rdx, rax
0028D373  mov      dword ptr [rsp + 0x20], ebx
0028D377  xor      r9d, r9d
0028D37A  mov      r8d, 0x600
0028D380  mov      rcx, rdi
0028D383  call     0x3f1430  ; -> 003F1430 fn
0028D388  mov      rdx, rax
0028D38B  xorps    xmm0, xmm0
0028D38E  mov      ecx, dword ptr [rax + 4]
0028D391  shr      ecx, 1
0028D393  and      ecx, 0x7ff
0028D399  neg      ecx
0028D39B  movd     xmm2, ecx
0028D39F  cvtdq2ps xmm2, xmm2
0028D3A2  movss    dword ptr [rdi + 0x50], xmm2
0028D3A7  mov      ecx, dword ptr [rax + 4]
0028D3AA  shr      ecx, 0xd
0028D3AD  and      ecx, 0x7ff
0028D3B3  neg      ecx
0028D3B5  movd     xmm1, ecx
0028D3B9  lea      rcx, [rdi + 0x50]
0028D3BD  cvtdq2ps xmm1, xmm1
0028D3C0  movss    dword ptr [rdi + 0x54], xmm1
0028D3C5  mov      eax, dword ptr [rax + 4]
0028D3C8  and      eax, 0xfff
0028D3CD  cvtsi2ss xmm0, rax
0028D3D2  addss    xmm0, xmm2
0028D3D6  movd     xmm2, dword ptr [rsp + 0x50]
0028D3DC  cvtdq2ps xmm2, xmm2
0028D3DF  movss    dword ptr [rdi + 0x58], xmm0
0028D3E4  xorps    xmm0, xmm0
0028D3E7  mov      eax, dword ptr [rdx + 4]
0028D3EA  lea      rdx, [rdi + 0x50]
0028D3EE  mulss    xmm2, dword ptr [rip + 0x67b4e2]  ; -> 009088D8 [f32 0.00390625]
0028D3F6  shr      eax, 0xc
0028D3F9  and      eax, 0xfff
0028D3FE  cvtsi2ss xmm0, rax
0028D403  addss    xmm0, xmm1
0028D407  movss    dword ptr [rdi + 0x5c], xmm0
0028D40C  call     0x270880  ; -> 00270880 fn
0028D411  cmp      dword ptr [rsp + 0x70], 0
0028D416  movss    xmm1, dword ptr [r14 + 0x70]
0028D41C  jge      0x28d425  ; -> 0028D425
0028D41E  xorps    xmm1, xmmword ptr [rip + 0x1a5e97b]  ; -> 01CEBDA0 [f32x4 -0, -0, -0, -0]
0028D425  mov      rcx, rdi
0028D428  call     0x3f1230  ; -> 003F1230 fn
0028D42D  mov      rdx, rdi
0028D430  mov      rcx, r15
0028D433  call     0x3f1290  ; -> 003F1290 fn
0028D438  mov      rsi, qword ptr [rsp + 0x60]
0028D43D  mov      rbx, qword ptr [rsp + 0x58]
0028D442  mov      rbp, qword ptr [rsp + 0x68]
0028D447  add      rsp, 0x30
0028D44B  pop      r15
0028D44D  pop      r14
0028D44F  pop      rdi
0028D450  ret      
```

## 00296600 (110 B, extent 00296600-0029666E)

Page context: "or anchor '002D52C7' (function '002D5280').  '002D5170' (270 B) is the label compose '002D5EB0' runs on the signal widget: 'word[rdi+0x140]' resolves through '0035BB20' and 'sword[rax+0x60]' through '00296600' for the suffix string; 'byte[rdi+0x142] & 4' or a nonzero 'esi' selects '002F9860(0x46B4)', otherwise 'ebp' picks one of '0x4669'/'0x466A'/'0x466C'; the chosen string lands at 'rdi+0xC0' with 'rbx' appended, then '[rdi+0x60]''s he"

```
00296600  test     ecx, ecx
00296602  js       0x296620  ; -> 00296620
00296604  cmp      ecx, 7
00296607  jge      0x296625  ; -> 00296625
00296609  movsxd   rax, ecx
0029660C  lea      rdx, [rip - 0x176613]  ; -> 00120000 (image base)
00296613  movsx    ecx, word ptr [rdx + rax*2 + 0x7f61f0]  ; image base + 0x7f61f0 = 009161F0
0029661B  jmp      0x2f9860  ; -> 002F9860 fn
00296620  cmp      ecx, 7
00296623  jl       0x296649  ; -> 00296649
00296625  cmp      ecx, 0x1a
00296628  jge      0x296649  ; -> 00296649
0029662A  add      ecx, -7
0029662D  cmp      ecx, 0xa
00296630  jge      0x29666b  ; -> 0029666B
00296632  movsxd   rax, ecx
00296635  lea      rdx, [rip - 0x17663c]  ; -> 00120000 (image base)
0029663C  movsx    ecx, word ptr [rdx + rax*2 + 0x7f6200]  ; image base + 0x7f6200 = 00916200
00296644  jmp      0x2f9860  ; -> 002F9860 fn
00296649  lea      eax, [rcx - 0x1b]
0029664C  cmp      eax, 0xc
0029664F  ja       0x29666b  ; -> 0029666B
00296651  lea      eax, [rcx - 0x1b]
00296654  movsxd   rcx, eax
00296657  lea      rdx, [rip - 0x17665e]  ; -> 00120000 (image base)
0029665E  movsx    ecx, word ptr [rdx + rcx*2 + 0x7f6218]  ; image base + 0x7f6218 = 00916218
00296666  jmp      0x2f9860  ; -> 002F9860 fn
0029666B  xor      eax, eax
0029666D  ret      
```

## 0029F580 (65 B, extent 0029F580-0029F5C1)

Page context: "F00' ×8, '002F9860' ×7, '00249CA0' ×4 sound calls, first at '00228CC9'); '002BA700' (LocaMap/Na/PartyBlack/BlackBand, 2,077 B — '00273A20' ×8, first call '002BA7AB'); '00292390' (ListItem, 1,920 B — '0029F580'/'0024A1D0'/'00181610' ×3 each, first call '002923DF'; '00181610''s one outward edge is a call on Platform's '001B1960' — a shared leaf helper, mechanical). Three further bodies on the same rows: '00574E80' ('P', PartyBlack, 1,708 "

```
0029F580  mov      rax, qword ptr [rcx]
0029F583  mov      r10, rcx
0029F586  mov      qword ptr [rcx + 0x18], rdx
0029F58A  mov      r9, qword ptr [rdx + 0x20]
0029F58E  add      r9, 0x30
0029F592  movzx    r8d, word ptr [rax + 0xe]
0029F597  mov      eax, r8d
0029F59A  shr      rax, 8
0029F59E  movzx    ecx, word ptr [r9 + 0x10]
0029F5A3  add      rcx, r9
0029F5A6  movzx    edx, word ptr [r9 + rax*2 + 0x14]
0029F5AC  movzx    eax, r8b
0029F5B0  add      edx, eax
0029F5B2  movzx    edx, word ptr [r9 + rdx*2 + 0x14]
0029F5B8  lea      rax, [rcx + rdx*8]
0029F5BC  mov      qword ptr [r10 + 0x20], rax
0029F5C0  ret      
```

## 002C98C0 (46 B, extent 002C98C0-002C98EE)

Page context: "un - the same success-only follow-up shape. Interior anchor '002C221B' (the '00249C60' call).  '0027F2E0' (121 B) is the '0209AC30' '+0x400' state commit: 'ebx' is 1 when bit 11 stands, else '0xC8'; '002C98C0(ebx)', '00250F30()', '002CC960(ebx)' run in order; then '+0x400' bit 9 clear stores byte 2, set stores 'bit10 ? 2 : 1', and bit 11 is cleared - the flag-state advance the layout callers drive. Interior anchor '0027F306' (the '002C9"

```
002C98C0  sub      rsp, 0x28
002C98C4  mov      edx, ecx
002C98C6  xor      ecx, ecx
002C98C8  call     0x2c98f0  ; -> 002C98F0 fn
002C98CD  mov      rax, qword ptr [rip + 0x1dd135c]  ; -> 0209AC30
002C98D4  mov      rcx, qword ptr [rax + 0x280]
002C98DB  test     rcx, rcx
002C98DE  je       0x2c98e9  ; -> 002C98E9
002C98E0  add      rsp, 0x28
002C98E4  jmp      0x244f00  ; -> 00244F00 fn
002C98E9  add      rsp, 0x28
002C98ED  ret      
```

## 002CB8D0 (231 B, extent 002CB8D0-002CB9B7)

Page context: "ords at 'rcx' - the poison pass the '+0xC8' subrecord refresh runs before repopulating. Interior anchor '002D028E' (the '0xFEFE' constant).  '002CAFE0' (361 B) is the four-link flag pass '002CB7F0', '002CB8D0', '002CB9C0' and '002CC2A0' call: bit 0 of '[+8]' is cleared on the '[rbx+0x60]' node's four links ('+0'/'+8'/'+0x10'/'+0x18'), and when 'dword[+0x40]' bit 0 is set, 'edi > 1' and 'dword[+0xF0]' lacks bit 1, two of the four re-arm "

```
002CB8D0  push     rdi
002CB8D2  sub      rsp, 0x30
002CB8D6  mov      rax, qword ptr [rip + 0x1dcf353]  ; -> 0209AC30
002CB8DD  mov      rdi, qword ptr [rax + 0x2e0]
002CB8E4  test     rdi, rdi
002CB8E7  je       0x2cb9b1  ; -> 002CB9B1
002CB8ED  mov      qword ptr [rsp + 0x40], rbx
002CB8F2  mov      qword ptr [rsp + 0x48], rbp
002CB8F7  mov      ebp, 9
002CB8FC  mov      qword ptr [rsp + 0x50], rsi
002CB901  lea      rsi, [rdi + 0xd0]
002CB908  mov      qword ptr [rsp + 0x58], r14
002CB90D  xor      r14d, r14d
002CB910  mov      rbx, qword ptr [rsi]
002CB913  mov      ecx, dword ptr [rbx + 0xd4]
002CB919  call     0x282df0  ; -> 00282DF0 fn
002CB91E  mov      rax, qword ptr [rbx + 0x60]
002CB922  lea      rsi, [rsi + 8]
002CB926  mov      rcx, qword ptr [rax]
002CB929  mov      eax, dword ptr [rbx + 0xc0]
002CB92F  and      eax, 0xffffff45
002CB934  or       eax, 0x45
002CB937  mov      dword ptr [rbx + 0xc0], eax
002CB93D  mov      eax, 0x20
002CB942  movzx    ecx, byte ptr [rcx + 0x3b]
002CB946  sub      ax, cx
002CB949  mov      word ptr [rbx + 0xc4], cx
002CB950  mov      word ptr [rbx + 0xc8], ax
002CB957  mov      word ptr [rbx + 0xc6], r14w
002CB95F  mov      eax, dword ptr [rip + 0x1dc3c0b]  ; -> 0208F570
002CB965  mov      dword ptr [rbx + 0xd0], eax
002CB96B  mov      dword ptr [rbx + 0xcc], 6
002CB975  sub      rbp, 1
002CB979  jne      0x2cb910  ; -> 002CB910
002CB97B  movzx    edx, byte ptr [rdi + 0x168]
002CB982  lea      r9d, [rbp + 1]
002CB986  mov      rcx, qword ptr [rdi + 0xc0]
002CB98D  xor      r8d, r8d
002CB990  mov      dword ptr [rsp + 0x20], 1
002CB998  call     0x2cafe0  ; -> 002CAFE0 fn
002CB99D  mov      r14, qword ptr [rsp + 0x58]
002CB9A2  mov      rsi, qword ptr [rsp + 0x50]
002CB9A7  mov      rbp, qword ptr [rsp + 0x48]
002CB9AC  mov      rbx, qword ptr [rsp + 0x40]
002CB9B1  add      rsp, 0x30
002CB9B5  pop      rdi
002CB9B6  ret      
```

## 002D5030 (46 B, extent 002D5030-002D505E)

Page context: "ontBaseHeight'→'r9d',   'sub r9d, edx', '002D4961' — shared by the action list, battle command, nobu-message and   '002C59D0'-family callers), '002D5EB0' P (the 'NaSPArt' signal widget, installed by '002D5030':   'OffsetY' 'sub'ed, 'OffsetX'→'ecx' → '0029E770', '002D6117'/'002D611D' — the same call the map and   item screens use), '00291D80' P (tail-jump installed; 'mTriangleHelpMessageFontCount'→'r8d' then   'jmp 0028FD00', '00291D80' "

```
002D5030  push     rbx
002D5032  sub      rsp, 0x20
002D5036  xor      r8d, r8d
002D5039  lea      rdx, [rip + 0xe70]  ; -> 002D5EB0
002D5040  mov      ecx, 0x760
002D5045  call     0x244f50  ; -> 00244F50 fn
002D504A  mov      rcx, rax
002D504D  mov      rbx, rax
002D5050  call     0x246ac0  ; -> 00246AC0 fn
002D5055  mov      rax, rbx
002D5058  add      rsp, 0x20
002D505C  pop      rbx
002D505D  ret      
```

## 00345B60 (180 B, extent 00345B60-00345C14)

Page context: " **Script_VM_Native_Bridge - CLIENT (25 edges).** '00229EA0', '00249CA0', '00264150', '002DEE50' (+10 more) are called by bodies filed to Script_VM_Native_Bridge: '0033F310', '0033FD40', '00340260', '00345B60' (+21 more) - shared machinery across the layer boundary, no shared ownership.  ## Cross-subsystem neighbours — FINAL-AUDIT pass 22  **Movement — SERVICE.** '00281AE0' on this page calls 'FUN_00326bb0', owned by that layer. What it"

```
00345B60  mov      qword ptr [rsp + 8], rbx
00345B65  mov      qword ptr [rsp + 0x10], rbp
00345B6A  mov      qword ptr [rsp + 0x18], rsi
00345B6F  mov      qword ptr [rsp + 0x20], rdi
00345B74  push     r14
00345B76  sub      rsp, 0x20
00345B7A  mov      rcx, r9
00345B7D  mov      rbx, r9
00345B80  mov      rbp, rdx
00345B83  call     0x267e10  ; -> 00267E10 fn
00345B88  xor      r14d, r14d
00345B8B  mov      rcx, rbx
00345B8E  test     eax, eax
00345B90  mov      esi, r14d
00345B93  setne    sil
00345B97  call     0x267e10  ; -> 00267E10 fn
00345B9C  mov      rcx, rbx
00345B9F  mov      edi, eax
00345BA1  call     0x267e10  ; -> 00267E10 fn
00345BA6  mov      ebx, eax
00345BA8  test     eax, eax
00345BAA  jns      0x345bb3  ; -> 00345BB3
00345BAC  call     0x2dec00  ; -> 002DEC00 fn
00345BB1  mov      ebx, eax
00345BB3  movzx    ecx, byte ptr [rbp + 0x15]
00345BB7  call     0x267310  ; -> 00267310 fn
00345BBC  test     eax, eax
00345BBE  mov      ecx, ebx
00345BC0  cmovne   edi, r14d
00345BC4  xor      r8d, r8d
00345BC7  mov      edx, edi
00345BC9  call     0x2dee50  ; -> 002DEE50 fn
00345BCE  mov      r8d, esi
00345BD1  mov      edx, edi
00345BD3  mov      ecx, ebx
00345BD5  call     0x361170  ; -> 00361170 fn
00345BDA  call     0x25d5d0  ; -> 0025D5D0 fn
00345BDF  movzx    ecx, byte ptr [rbp + 0x15]
00345BE3  call     0x267310  ; -> 00267310 fn
00345BE8  test     eax, eax
00345BEA  je       0x345bf9  ; -> 00345BF9
00345BEC  xor      r8d, r8d
00345BEF  xor      edx, edx
00345BF1  or       ecx, 0xffffffff
00345BF4  call     0x360960  ; -> 00360960 fn
00345BF9  mov      rbx, qword ptr [rsp + 0x30]
00345BFE  mov      rbp, qword ptr [rsp + 0x38]
00345C03  mov      rsi, qword ptr [rsp + 0x40]
00345C08  mov      rdi, qword ptr [rsp + 0x48]
00345C0D  add      rsp, 0x20
00345C11  pop      r14
00345C13  ret      
```

## 003EEEC0 (388 B, extent 003EEEC0-003EF044)

Page context: "hor '002A03BC' (the proportional-path '002D8D40' call).  ## SWE2-EC7-106 update (2026-09-20) - '00251D90' measured  '00251D90' (105 B) is the conditional one-shot register '002289D0', '0027FB70' and '003EEEC0' call: only when '020927F0' is null does it build a stack descriptor - 'word = cx', 'dword = edx', 'dword = r8d', a count out-slot and a '0x10'-byte buffer pointer - and runs '00244F50(0x140, 002509D0, &desc)'; a live record skips "

```
003EEEC0  mov      qword ptr [rsp + 8], rbx
003EEEC5  push     rdi
003EEEC6  sub      rsp, 0x20
003EEECA  mov      rbx, rcx
003EEECD  mov      rdi, rdx
003EEED0  mov      ecx, dword ptr [rdx]
003EEED2  sub      ecx, 1
003EEED5  je       0x3eefee  ; -> 003EEFEE
003EEEDB  sub      ecx, 1
003EEEDE  je       0x3eef27  ; -> 003EEF27
003EEEE0  sub      ecx, 0xd
003EEEE3  je       0x3eef03  ; -> 003EEF03
003EEEE5  cmp      ecx, 3
003EEEE8  je       0x3eeefc  ; -> 003EEEFC
003EEEEA  mov      rcx, rbx
003EEEED  mov      rbx, qword ptr [rsp + 0x30]
003EEEF2  add      rsp, 0x20
003EEEF6  pop      rdi
003EEEF7  jmp      0x5c5230  ; -> 005C5230 fn
003EEEFC  mov      edx, 0x12
003EEF01  jmp      0x3eef08  ; -> 003EEF08
003EEF03  mov      edx, 0xf
003EEF08  mov      rcx, qword ptr [rbx + 0xc0]
003EEF0F  mov      r8d, 1
003EEF15  call     0x247510  ; -> 00247510 fn
003EEF1A  xor      eax, eax
003EEF1C  mov      rbx, qword ptr [rsp + 0x30]
003EEF21  add      rsp, 0x20
003EEF25  pop      rdi
003EEF26  ret      
003EEF27  mov      ecx, dword ptr [rbx + 0xb4]
003EEF2D  call     0x1edec0  ; -> 001EDEC0 fn
003EEF32  test     eax, eax
003EEF34  je       0x3ef037  ; -> 003EF037
003EEF3A  mov      eax, dword ptr [rbx + 0xcc]
003EEF40  test     eax, eax
003EEF42  je       0x3eef53  ; -> 003EEF53
003EEF44  sub      eax, 1
003EEF47  mov      dword ptr [rbx + 0xcc], eax
003EEF4D  jne      0x3ef037  ; -> 003EF037
003EEF53  movzx    ecx, byte ptr [rbx + 0xc8]
003EEF5A  test     ecx, ecx
003EEF5C  je       0x3eefc6  ; -> 003EEFC6
003EEF5E  sub      ecx, 1
003EEF61  je       0x3eef9a  ; -> 003EEF9A
003EEF63  sub      ecx, 1
003EEF66  je       0x3eef86  ; -> 003EEF86
003EEF68  cmp      ecx, 2
003EEF6B  jne      0x3ef037  ; -> 003EF037
003EEF71  mov      rcx, rbx
003EEF74  call     0x244f00  ; -> 00244F00 fn
003EEF79  xor      eax, eax
003EEF7B  mov      rbx, qword ptr [rsp + 0x30]
003EEF80  add      rsp, 0x20
003EEF84  pop      rdi
003EEF85  ret      
003EEF86  mov      byte ptr [rbx + 0xc8], 3
003EEF8D  xor      eax, eax
003EEF8F  mov      rbx, qword ptr [rsp + 0x30]
003EEF94  add      rsp, 0x20
003EEF98  pop      rdi
003EEF99  ret      
003EEF9A  xor      r8d, r8d
003EEF9D  mov      ecx, 0x3e8
003EEFA2  lea      edx, [r8 + 8]
003EEFA6  call     0x2c99a0  ; -> 002C99A0 fn
003EEFAB  mov      edx, 0x13
003EEFB0  mov      byte ptr [rbx + 0xc8], 2
003EEFB7  mov      dword ptr [rbx + 0xcc], 0x3c
003EEFC1  jmp      0x3eef08  ; -> 003EEF08
003EEFC6  call     0x251d20  ; -> 00251D20 fn
003EEFCB  cmp      eax, 2
003EEFCE  jle      0x3ef037  ; -> 003EF037
003EEFD0  mov      byte ptr [rbx + 0xc8], 1
003EEFD7  xor      eax, eax
003EEFD9  mov      dword ptr [rbx + 0xcc], 0x12
003EEFE3  mov      rbx, qword ptr [rsp + 0x30]
003EEFE8  add      rsp, 0x20
003EEFEC  pop      rdi
003EEFED  ret      
003EEFEE  mov      edx, 0x3c
003EEFF3  lea      ecx, [rdx - 0x3b]
003EEFF6  lea      r8d, [rdx + 0x3c]
003EEFFA  call     0x251d90  ; -> 00251D90 fn
003EEFFF  mov      rax, qword ptr [rdi + 8]
003EF003  mov      edx, 0x64
003EF008  mov      rcx, rbx
003EF00B  mov      qword ptr [rbx + 0xc0], rax
003EF012  mov      byte ptr [rbx + 0xc8], 0
003EF019  mov      dword ptr [rbx + 0xcc], 0
003EF023  call     0x247930  ; -> 00247930 fn
003EF028  mov      rcx, qword ptr [rip + 0x2770199]  ; -> 02B5F1C8
003EF02F  mov      rdx, rbx
003EF032  call     0x246ad0  ; -> 00246AD0 fn
003EF037  xor      eax, eax
003EF039  mov      rbx, qword ptr [rsp + 0x30]
003EF03E  add      rsp, 0x20
003EF042  pop      rdi
003EF043  ret      
```

## 003FE5D0 (259 B, extent 003FE5D0-003FE6D3)

Page context: "lazy registry record measured  '003FE410' (123 B) is the one-time record install the layout callers run: when '[0209AC30]+0x138' is null it packs 'ecx' into a stack descriptor, calls '00244F50(0x118, 003FE5D0, &desc)' so the '003FE5D0' callback builds the 0x118 record, stores it into '[0209AC30]+0x138', and registers it via '00246AD0([0208EA28], record)' - all under a stack cookie. Interior anchor '003FE457' (the '00244F50' builder call"

```
003FE5D0  mov      qword ptr [rsp + 8], rbx
003FE5D5  push     rdi
003FE5D6  sub      rsp, 0x20
003FE5DA  mov      rbx, rcx
003FE5DD  mov      rdi, rdx
003FE5E0  mov      ecx, dword ptr [rdx]
003FE5E2  sub      ecx, 1
003FE5E5  je       0x3fe626  ; -> 003FE626
003FE5E7  sub      ecx, 0xe
003FE5EA  je       0x3fe6c6  ; -> 003FE6C6
003FE5F0  cmp      ecx, 3
003FE5F3  je       0x3fe607  ; -> 003FE607
003FE5F5  mov      rcx, rbx
003FE5F8  mov      rbx, qword ptr [rsp + 0x30]
003FE5FD  add      rsp, 0x20
003FE601  pop      rdi
003FE602  jmp      0x5c5230  ; -> 005C5230 fn
003FE607  mov      rax, qword ptr [rip + 0x1c9c622]  ; -> 0209AC30
003FE60E  mov      qword ptr [rax + 0x138], 0
003FE619  xor      eax, eax
003FE61B  mov      rbx, qword ptr [rsp + 0x30]
003FE620  add      rsp, 0x20
003FE624  pop      rdi
003FE625  ret      
003FE626  mov      rax, qword ptr [rip + 0x1c9c603]  ; -> 0209AC30
003FE62D  lea      rcx, [rbx + 0x50]
003FE631  mov      r9, rbx
003FE634  mov      r8d, 1
003FE63A  mov      rdx, qword ptr [rax + 0x38]
003FE63E  call     0x2432b0  ; -> 002432B0 fn
003FE643  movzx    ecx, word ptr [rax + 0xa]
003FE647  movzx    edx, word ptr [rax + 8]
003FE64B  movsx    r8d, word ptr [rax + 6]
003FE650  test     rbx, rbx
003FE653  je       0x3fe676  ; -> 003FE676
003FE655  movzx    eax, word ptr [rax + 4]
003FE659  mov      word ptr [rbx + 0x98], ax
003FE660  mov      word ptr [rbx + 0x9a], r8w
003FE668  mov      word ptr [rbx + 0x9c], dx
003FE66F  mov      word ptr [rbx + 0x9e], cx
003FE676  lea      rdx, [rip + 0x9139fb]  ; -> 00D12078
003FE67D  mov      rcx, rbx
003FE680  call     0x247570  ; -> 00247570 fn
003FE685  movzx    eax, word ptr [rdi + 8]
003FE689  mov      word ptr [rbx + 0x110], ax
003FE690  mov      rax, qword ptr [rbx + 0x60]
003FE694  mov      rcx, qword ptr [rax + 0x10]
003FE698  mov      rax, qword ptr [rcx + 0x18]
003FE69C  lea      rcx, [rip - 0x213]  ; -> 003FE490
003FE6A3  mov      qword ptr [rbx + 0xc0], rax
003FE6AA  mov      qword ptr [rax + 0x120], rcx
003FE6B1  mov      rax, qword ptr [rbx + 0xc0]
003FE6B8  mov      qword ptr [rax + 0xd8], rbx
003FE6BF  and      dword ptr [rbx + 0x40], 0xfffff7ff
003FE6C6  xor      eax, eax
003FE6C8  mov      rbx, qword ptr [rsp + 0x30]
003FE6CD  add      rsp, 0x20
003FE6D1  pop      rdi
003FE6D2  ret      
```
