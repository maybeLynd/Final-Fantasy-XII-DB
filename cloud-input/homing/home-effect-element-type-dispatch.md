# Homing pack: `17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-effect-element-type-dispatch.json`.

Bodies: 9. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00366A30 (331 B, extent 00366A30-00366B7B)

Entered from (direct sites whose caller this page cites): `00366B80` + 0x2A6 (call; `00366B80` is cited on this page); `00366B80` + 0x30B (call; `00366B80` is cited on this page)
Other direct sites: none

Host context: "10' | 2,018 B | 'PS2-Image-Data-Formats/loader-bound-bin-families' | | '00449AB0' | 1,741 B | this page — **read above** | | '00522D80' | 1,531 B | this page | | '00523D30' | 1,511 B | this page | | '00366B80' | 1,420 B | 'Widget-Object-Model/the-widget-constructor-and-object-sizes.md' | | '00522300' | 1,268 B | this page | | '002C2F90' | 1,110 B | 'Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md' | | '005742D0' | 1,09" / "10' | 2,018 B | 'PS2-Image-Data-Formats/loader-bound-bin-families' | | '00449AB0' | 1,741 B | this page — **read above** | | '00522D80' | 1,531 B | this page | | '00523D30' | 1,511 B | this page | | '00366B80' | 1,420 B | 'Widget-Object-Model/the-widget-constructor-and-object-sizes.md' | | '00522300' | 1,268 B | this page | | '002C2F90' | 1,110 B | 'Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md' | | '005742D0' | 1,09"

```
00366A30  mov      qword ptr [rsp + 0x18], rbx
00366A35  push     rdi
00366A36  sub      rsp, 0x50
00366A3A  movsx    r11, word ptr [rdx + 0xa]
00366A3F  lea      rax, [rdx + 0x28]
00366A43  mov      r10, qword ptr [rdx + 0x20]
00366A47  mov      rdi, rcx
00366A4A  mov      qword ptr [rsp + 0x38], rax
00366A4F  mov      ecx, 0xfff
00366A54  xor      eax, eax
00366A56  mov      dword ptr [rsp + 0x30], 0
00366A5E  mov      qword ptr [rsp + 0x40], rax
00366A63  xorps    xmm0, xmm0
00366A66  movss    dword ptr [rsp + 0x34], xmm0
00366A6C  mov      rbx, rdx
00366A6F  movzx    eax, word ptr [r10 + r11*8]
00366A74  mov      word ptr [rsp + 0x68], ax
00366A79  movzx    eax, word ptr [r10 + r11*8 + 2]
00366A7F  mov      word ptr [rsp + 0x6a], ax
00366A84  movzx    eax, word ptr [r10 + r11*8 + 4]
00366A8A  and      ax, cx
00366A8D  mov      word ptr [rsp + 0x6c], ax
00366A92  mov      eax, dword ptr [r10 + r11*8 + 4]
00366A97  shr      eax, 0xc
00366A9A  and      ax, cx
00366A9D  mov      ecx, dword ptr [rsp + 0x80]
00366AA4  mov      word ptr [rsp + 0x6e], ax
00366AA9  test     ecx, ecx
00366AAB  jne      0x366abc  ; -> 00366ABC
00366AAD  movzx    eax, word ptr [rdx + 0x10]
00366AB1  mov      word ptr [rsp + 0x64], ax
00366AB6  movzx    eax, word ptr [rdx + 0x12]
00366ABA  jmp      0x366b01  ; -> 00366B01
00366ABC  mov      eax, dword ptr [rsp + 0x88]
00366AC3  sub      r8d, eax
00366AC6  imul     r8d, ecx
00366ACA  shr      r8d, 8
00366ACE  add      r8w, ax
00366AD2  mov      eax, dword ptr [rsp + 0x90]
00366AD9  sub      r9d, eax
00366ADC  imul     r9d, ecx
00366AE0  shr      r9d, 8
00366AE4  add      r9w, ax
00366AE8  movzx    eax, word ptr [rdx + 0x10]
00366AEC  imul     eax, ecx
00366AEF  shr      eax, 8
00366AF2  mov      word ptr [rsp + 0x64], ax
00366AF7  movzx    eax, word ptr [rdx + 0x12]
00366AFB  imul     eax, ecx
00366AFE  shr      eax, 8
00366B01  movss    xmm0, dword ptr [rip + 0x198509f]  ; -> 01CEBBA8 [f32 1]
00366B09  mov      rcx, rdi
00366B0C  mov      word ptr [rsp + 0x66], ax
00366B11  mov      rax, qword ptr [rdx + 0x18]
00366B15  mov      word ptr [rsp + 0x62], r9w
00366B1B  movzx    r9d, byte ptr [rdx + 0x39]
00366B20  mov      word ptr [rsp + 0x60], r8w
00366B26  mov      r8, qword ptr [rax + 0x20]
00366B2A  mov      eax, r9d
00366B2D  shr      eax, 4
00366B30  add      r8, 0x30
00366B34  movzx    eax, al
00366B37  and      r9b, 0xf
00366B3B  add      rax, r8
00366B3E  movss    dword ptr [rsp + 0x28], xmm0
00366B44  movzx    edx, word ptr [r8 + 0x12]
00366B49  lea      r8, [rsp + 0x68]
00366B4E  movzx    eax, byte ptr [rdx + rax]
00366B52  add      al, r9b
00366B55  lea      r9, [rsp + 0x60]
00366B5A  mov      byte ptr [rdi + 0x5c], al
00366B5D  lea      rax, [rsp + 0x30]
00366B62  mov      rdx, qword ptr [rbx + 0x18]
00366B66  mov      qword ptr [rsp + 0x20], rax
00366B6B  call     0x2d8d10  ; -> 002D8D10 fn
00366B70  mov      rbx, qword ptr [rsp + 0x70]
00366B75  add      rsp, 0x50
00366B79  pop      rdi
00366B7A  ret      
```

## 003769F0 (37 B, extent 003769F0-00376A15)

Entered from (direct sites whose caller this page cites): `00461270` + 0x31D (call; `00461270` is cited on this page)
Other direct sites: none

Host context: "'/'00462160'/'001827B0'/'00808C40' run the per-flag arms - the element's flag evaluator.  Interior anchor '004610B0' (function '00461090').  '00377100' (38 B) is the call-free slot writer '00461090'/'00461270' call: 'cl * 0x90' ('r8*9*2*8') indexes the '02ADBB40' table, 'ecx != 0' and 'dword[slot] == ecx' guard, then 'movups' stores the caller's 16 bytes at '+0x70' - the keyed vector write.  Interior anchor '00377116' (function '0037710"

```
003769F0  movzx    edx, cl
003769F3  lea      rax, [rdx + rdx*8]
003769F7  add      rax, rax
003769FA  lea      rdx, [rip + 0x276513f]  ; -> 02ADBB40
00376A01  test     ecx, ecx
00376A03  je       0x376a11  ; -> 00376A11
00376A05  cmp      dword ptr [rdx + rax*8], ecx
00376A08  jne      0x376a11  ; -> 00376A11
00376A0A  movss    xmm0, dword ptr [rdx + rax*8 + 8]
00376A10  ret      
00376A11  xorps    xmm0, xmm0
00376A14  ret      
```

## 003A9AD0 (198 B, extent 003A9AD0-003A9B96)

Entered from (direct sites whose caller this page cites): `003A99F0` + 0x22 (call; `003A99F0` is cited on this page)
Other direct sites: none

Host context: " ('0050050B'–'0050052F'), with a sub-range partner '00538910' for '0x42'–'0xAB' ('00538910'–'00538939'). '003A9A70' writes that byte and then calls it ('003A9A8F', '003A9AAD'). Its other callers are '003A99F0' (after a 'memcpy') and '003A9BA0', reached from the EFX data parse '003EDAD0' / '003ED8A0' and from ~~instance creation~~ the context rebase arms of the per-frame effect pass '0024D540' ('0024D540'+0x114) and of '0024D970' ('0024D"

```
003A9AD0  mov      qword ptr [rsp + 0x10], rbx
003A9AD5  mov      qword ptr [rsp + 0x18], rbp
003A9ADA  push     rsi
003A9ADB  sub      rsp, 0x20
003A9ADF  mov      rax, qword ptr [rip + 0x2b15492]  ; -> 02EBEF78
003A9AE6  test     ecx, ecx
003A9AE8  movsxd   rbx, ecx
003A9AEB  mov      esi, r8d
003A9AEE  mov      ebp, edx
003A9AF0  mov      rcx, qword ptr [rax]
003A9AF3  je       0x3a9b62  ; -> 003A9B62
003A9AF5  mov      qword ptr [rsp + 0x30], rdi
003A9AFA  lea      rdi, [rbx*8]
003A9B02  mov      rcx, qword ptr [rdi + rcx]
003A9B06  test     rcx, rcx
003A9B09  je       0x3a9b22  ; -> 003A9B22
003A9B0B  call     0x3697f0  ; -> 003697F0 fn
003A9B10  mov      rax, qword ptr [rip + 0x2b15461]  ; -> 02EBEF78
003A9B17  mov      rcx, qword ptr [rax]
003A9B1A  mov      qword ptr [rdi + rcx], 0
003A9B22  mov      rdi, qword ptr [rsp + 0x30]
003A9B27  mov      ecx, esi
003A9B29  call     0x36a100  ; -> 0036A100 fn
003A9B2E  mov      r8, rax
003A9B31  test     rax, rax
003A9B34  je       0x3a9b84  ; -> 003A9B84
003A9B36  mov      byte ptr [rax + 0x44], bpl
003A9B3A  mov      word ptr [rax + 0x42], bx
003A9B3E  mov      rax, qword ptr [rip + 0x2b15433]  ; -> 02EBEF78
003A9B45  movsxd   rdx, ebx
003A9B48  mov      rcx, qword ptr [rax]
003A9B4B  mov      rax, r8
003A9B4E  mov      qword ptr [rcx + rdx*8], r8
003A9B52  mov      rbx, qword ptr [rsp + 0x38]
003A9B57  mov      rbp, qword ptr [rsp + 0x40]
003A9B5C  add      rsp, 0x20
003A9B60  pop      rsi
003A9B61  ret      
003A9B62  mov      ebx, 1
003A9B67  nop      word ptr [rax + rax]
003A9B70  movsxd   rax, ebx
003A9B73  cmp      qword ptr [rcx + rax*8], 0
003A9B78  je       0x3a9b27  ; -> 003A9B27
003A9B7A  inc      ebx
003A9B7C  cmp      ebx, 0x300
003A9B82  jl       0x3a9b70  ; -> 003A9B70
003A9B84  mov      rbx, qword ptr [rsp + 0x38]
003A9B89  xor      eax, eax
003A9B8B  mov      rbp, qword ptr [rsp + 0x40]
003A9B90  add      rsp, 0x20
003A9B94  pop      rsi
003A9B95  ret      
```

## 004FE4A0 (60 B, extent 004FE4A0-004FE4DC)

Entered from (direct sites whose caller this page cites): `00538350` + 0x39 (call; `00538350` is cited on this page); `005387B0` + 0x39 (call; `005387B0` is cited on this page); `005387B0` + 0x47 (call; `005387B0` is cited on this page)
Other direct sites: none

Host context: " 13 B | sets bit 0x80 of word 'rcx+0x232' (ORs it with 0x80 loaded at the entry) | '00465685' | | '004FF270' | 55 B | dispatches on byte 'rcx+0xC2': tail-jumps to '00537C80' for 0, '00537FA0' for 1, '00538350' for 2 and '005387B0' for 3, with 'rcx', 'rdx' and 'r9' unchanged ('r8' is overwritten by the selector arithmetic), and returns 'rcx' for any other value | '004FF278', '004FF289', '004FF28F', '004FF293', '004FF2A2' | | '00501440' |" / " of word 'rcx+0x232' (ORs it with 0x80 loaded at the entry) | '00465685' | | '004FF270' | 55 B | dispatches on byte 'rcx+0xC2': tail-jumps to '00537C80' for 0, '00537FA0' for 1, '00538350' for 2 and '005387B0' for 3, with 'rcx', 'rdx' and 'r9' unchanged ('r8' is overwritten by the selector arithmetic), and returns 'rcx' for any other value | '004FF278', '004FF289', '004FF28F', '004FF293', '004FF2A2' | | '00501440' | 108 B | calls '00369"

```
004FE4A0  mov      qword ptr [rsp + 8], rbx
004FE4A5  push     rdi
004FE4A6  sub      rsp, 0x20
004FE4AA  mov      ebx, edx
004FE4AC  mov      rdi, rcx
004FE4AF  call     0x4304f0  ; -> 004304F0 fn
004FE4B4  lea      rcx, [rdi + 0x10]
004FE4B8  mov      edx, ebx
004FE4BA  call     0x4304f0  ; -> 004304F0 fn
004FE4BF  lea      rcx, [rdi + 0x20]
004FE4C3  mov      edx, ebx
004FE4C5  call     0x4304f0  ; -> 004304F0 fn
004FE4CA  mov      rbx, qword ptr [rsp + 0x30]
004FE4CF  lea      rax, [rdi + 0x80]
004FE4D6  add      rsp, 0x20
004FE4DA  pop      rdi
004FE4DB  ret      
```

## 004FF1B0 (59 B, extent 004FF1B0-004FF1EB)

Entered from (direct sites whose caller this page cites): `0052F560` + 0x20A (call; `0052F560` is cited on this page)
Other direct sites: none

Host context: "r '[rsi + 0xB0]'/'[+0x2DC]'/'[+0x31C]', then the shared '00397910'/'00398030'/'00398480'/'00398F90'/'0039ADE0'/'0039AF70'/'003A2440'/'003A2570'/'003A27C0'/'003A2B20'/'003A6E60'/'003D8E50'/'004309C0'/'0052F560' tail publishing through '022D92E0..F0' - arm 0's full pass.  Interior anchor '005307CC' (function '00530770').  '0052FCA0' (1421 B) is a '00442170' post-pass arm: same '00430B90' preamble into the shared '0039xxxx'/'003A2xxx'/'005"

```
004FF1B0  mov      rax, qword ptr [rcx + 0xe0]
004FF1B7  movzx    r8d, byte ptr [rax + 0xc2]
004FF1BF  test     r8d, r8d
004FF1C2  je       0x4ff1e5  ; -> 004FF1E5
004FF1C4  sub      r8d, 1
004FF1C8  je       0x4ff1e0  ; -> 004FF1E0
004FF1CA  sub      r8d, 1
004FF1CE  je       0x4ff1db  ; -> 004FF1DB
004FF1D0  cmp      r8d, 1
004FF1D4  jne      0x4ff1ea  ; -> 004FF1EA
004FF1D6  jmp      0x5382f0  ; -> 005382F0 fn
004FF1DB  jmp      0x5382f0  ; -> 005382F0 fn
004FF1E0  jmp      0x537f10  ; -> 00537F10 fn
004FF1E5  jmp      0x5382f0  ; -> 005382F0 fn
004FF1EA  ret      
```

## 004FF1F0 (59 B, extent 004FF1F0-004FF22B)

Entered from (direct sites whose caller this page cites): `0052F560` + 0x154 (call; `0052F560` is cited on this page)
Other direct sites: none

Host context: "r '[rsi + 0xB0]'/'[+0x2DC]'/'[+0x31C]', then the shared '00397910'/'00398030'/'00398480'/'00398F90'/'0039ADE0'/'0039AF70'/'003A2440'/'003A2570'/'003A27C0'/'003A2B20'/'003A6E60'/'003D8E50'/'004309C0'/'0052F560' tail publishing through '022D92E0..F0' - arm 0's full pass.  Interior anchor '005307CC' (function '00530770').  '0052FCA0' (1421 B) is a '00442170' post-pass arm: same '00430B90' preamble into the shared '0039xxxx'/'003A2xxx'/'005"

```
004FF1F0  mov      rax, qword ptr [rcx + 0xe0]
004FF1F7  movzx    r8d, byte ptr [rax + 0xc2]
004FF1FF  test     r8d, r8d
004FF202  je       0x4ff225  ; -> 004FF225
004FF204  sub      r8d, 1
004FF208  je       0x4ff220  ; -> 004FF220
004FF20A  sub      r8d, 1
004FF20E  je       0x4ff21b  ; -> 004FF21B
004FF210  cmp      r8d, 1
004FF214  jne      0x4ff22a  ; -> 004FF22A
004FF216  jmp      0x538320  ; -> 00538320 fn
004FF21B  jmp      0x538320  ; -> 00538320 fn
004FF220  jmp      0x537f70  ; -> 00537F70 fn
004FF225  jmp      0x5382f0  ; -> 005382F0 fn
004FF22A  ret      
```

## 004FF230 (63 B, extent 004FF230-004FF26F)

Entered from (direct sites whose caller this page cites): `00537C80` + 0xF (call; `00537C80` is cited on this page); `00537FA0` + 0xF (call; `00537FA0` is cited on this page); `00538350` + 0xF (call; `00538350` is cited on this page); `005387B0` + 0xF (call; `005387B0` is cited on this page)
Other direct sites: none

Host context: "464B5A', '00464B61' | | '00465680' | 13 B | sets bit 0x80 of word 'rcx+0x232' (ORs it with 0x80 loaded at the entry) | '00465685' | | '004FF270' | 55 B | dispatches on byte 'rcx+0xC2': tail-jumps to '00537C80' for 0, '00537FA0' for 1, '00538350' for 2 and '005387B0' for 3, with 'rcx', 'rdx' and 'r9' unchanged ('r8' is overwritten by the selector arithmetic), and returns 'rcx' for any other value | '004FF278', '004FF289', '004FF28F', '00" / "' | | '00465680' | 13 B | sets bit 0x80 of word 'rcx+0x232' (ORs it with 0x80 loaded at the entry) | '00465685' | | '004FF270' | 55 B | dispatches on byte 'rcx+0xC2': tail-jumps to '00537C80' for 0, '00537FA0' for 1, '00538350' for 2 and '005387B0' for 3, with 'rcx', 'rdx' and 'r9' unchanged ('r8' is overwritten by the selector arithmetic), and returns 'rcx' for any other value | '004FF278', '004FF289', '004FF28F', '004FF293', '004FF2A2"

```
004FF230  mov      qword ptr [rsp + 8], rbx
004FF235  push     rdi
004FF236  sub      rsp, 0x20
004FF23A  mov      ebx, edx
004FF23C  mov      rdi, rcx
004FF23F  call     0x430af0  ; -> 00430AF0 fn
004FF244  lea      rcx, [rdi + 0x40]
004FF248  mov      edx, ebx
004FF24A  call     0x430af0  ; -> 00430AF0 fn
004FF24F  lea      rcx, [rdi + 0x80]
004FF256  mov      edx, ebx
004FF258  call     0x430af0  ; -> 00430AF0 fn
004FF25D  mov      rbx, qword ptr [rsp + 0x30]
004FF262  lea      rax, [rdi + 0xd0]
004FF269  add      rsp, 0x20
004FF26D  pop      rdi
004FF26E  ret      
```

## 00524790 (46 B, extent 00524790-005247BE)

Entered from (direct sites whose caller this page cites): `00524320` + 0x2DB (call; `00524320` is cited on this page)
Other direct sites: none

Host context: " '+0x870', '+0x87C'/'+0x87D'/'+0x87E' copy into the '[rdi+0x230]' block at '+0', '+0x730', '+8', '+0x744', '+0x794' (1.0f staging via 'xmm6'), '003D8E50' runs four times across the block, '005439A0'/'00524320' close it and '[rbx+0x14]' lands at '[rdi+0xAC0]' - '1' on commit, early-out on the gate.  Interior anchor '00523C39' (function '00523C30').  '00366690' (80 B) is the shared angle wrap: 'xmm0' (degrees) scales by 'pi/180' ('* 3.141"

```
00524790  cmp      cx, -1
00524794  jne      0x52479c  ; -> 0052479C
00524796  mov      eax, 0xffff
0052479B  ret      
0052479C  movsx    rax, cx
005247A0  imul     rcx, rax, 0x740
005247A7  add      rcx, qword ptr [rip + 0x1da277a]  ; -> 022C6F28
005247AE  je       0x524796  ; -> 00524796
005247B0  cmp      dword ptr [rcx + 0x284], 0
005247B7  je       0x524796  ; -> 00524796
005247B9  jmp      0x421d70  ; -> 00421D70 fn
```

## 00623D70 (57 B, extent 00623D70-00623DA9)

Entered from (direct sites whose caller this page cites): `0062B020` + 0x29 (call; `0062B020` is cited on this page); `0062B020` + 0x43 (call; `0062B020` is cited on this page)
Other direct sites: none

Host context: "# SWE2-EC7-126 update (2026-09-21) - the element-list reset and the indexed element fetch measured  '0062B7B0' (183 B) is the list reset the teardown ('005FE200', '00616420') and record paths share: '0062B020' runs first, '+0x48' is zeroed, then each of the '[rbx+0x18]'-count (masked) entries in the inline-or-heap 0x10-stride array at '+0x20' gets its non-null pointer's 'vtable[+0x10]' called and the slot cleared; finally '+0x10' is fre" / "# SWE2-EC7-126 update (2026-09-21) - the element-list reset and the indexed element fetch measured  '0062B7B0' (183 B) is the list reset the teardown ('005FE200', '00616420') and record paths share: '0062B020' runs first, '+0x48' is zeroed, then each of the '[rbx+0x18]'-count (masked) entries in the inline-or-heap 0x10-stride array at '+0x20' gets its non-null pointer's 'vtable[+0x10]' called and the slot cleared; finally '+0x10' is fre"

```
00623D70  mov      eax, dword ptr [rcx + 0x18]
00623D73  btr      eax, 0x1f
00623D77  cmp      eax, 1
00623D7A  jbe      0x623d8e  ; -> 00623D8E
00623D7C  mov      rcx, qword ptr [rcx + 0x20]
00623D80  mov      eax, edx
00623D82  shl      rax, 4
00623D86  add      rax, 0xc
00623D8A  add      rax, rcx
00623D8D  ret      
00623D8E  add      rcx, 0x20
00623D92  xor      r8d, r8d
00623D95  test     eax, eax
00623D97  mov      eax, edx
00623D99  cmove    rcx, r8
00623D9D  shl      rax, 4
00623DA1  add      rax, 0xc
00623DA5  add      rax, rcx
00623DA8  ret      
```
