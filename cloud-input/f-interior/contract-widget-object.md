# F-interior pack: `16-UI/Widget-Object-Model/CONTRACT-widget-object.md`

Generated 2026-10-02 12:46 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/contract-widget-object.json`.

Functions: 8. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 65f4854dd	SWE2-STRUCT pass-22 debt + OV31 narrowing: 77 crossing bullets across 21 docs (5 lane folders now re; inbox mentions: ASTRA.md, FABLE.md, SWE2-EC7.md, SWE2-FRONTIER.md). OPUS read these before packing.

## 00296580 (128 B, extent 00296580-00296600)

Page context: " (2026-09-20) - '00290490' measured  '00290490' (28 B) is the '+0x10F78' slot test '002778C0' and '0027E3E0' call: a null '[[0209BE80] + 0x10F78]' returns '-1'; otherwise the slot forwards through a '00296580' tail - the presence-gated widget call the protocol arms share. Interior anchor '00290497' (the slot read).  ## SWE2-EC7-103 update (2026-09-20) - '0027BB70' measured  '0027BB70' (154 B) is the mask-filtered collect '0027D740' and "

```
00296580  sub      rsp, 0x28
00296584  mov      rdx, rcx
00296587  test     rcx, rcx
0029658A  jne      0x296594  ; -> 00296594
0029658C  or       eax, 0xffffffff
0029658F  add      rsp, 0x28
00296593  ret      
00296594  mov      qword ptr [rsp + 0x20], rbx
00296599  mov      rbx, qword ptr [rcx + 0xb50]
002965A0  test     rbx, rbx
002965A3  je       0x2965f3  ; -> 002965F3
002965A5  movsx    r8, byte ptr [rcx + 0xb48]
002965AD  imul     rcx, r8, 0x160
002965B4  test     byte ptr [rcx + rdx + 0x318], 1
002965BC  je       0x2965f3  ; -> 002965F3
002965BE  movsx    ecx, r8b
002965C2  call     0x35bb00  ; -> 0035BB00 fn
002965C7  movsxd   r8, dword ptr [rbx + 0x40]
002965CB  mov      r9d, eax
002965CE  xor      eax, eax
002965D0  mov      edx, eax
002965D2  test     r8, r8
002965D5  jle      0x2965f3  ; -> 002965F3
002965D7  lea      rcx, [rbx + 0x50]
002965DB  nop      dword ptr [rax + rax]
002965E0  cmp      dword ptr [rcx], r9d
002965E3  je       0x2965f6  ; -> 002965F6
002965E5  inc      eax
002965E7  inc      rdx
002965EA  add      rcx, 8
002965EE  cmp      rdx, r8
002965F1  jl       0x2965e0  ; -> 002965E0
002965F3  or       eax, 0xffffffff
002965F6  mov      rbx, qword ptr [rsp + 0x20]
002965FB  add      rsp, 0x28
002965FF  ret      
```

## 0029ECB0 (116 B, extent 0029ECB0-0029ED24)

Page context: "ld pack seen in the typed-list document, and dispatches per-type constructors through the six-case jump table at '[r9 + rax*4 + 0x123514]' over '0029F4C0'/'0029FEB0'/'0029ED40'/'0029F130'/'0029F930'/'0029ECB0'. 64 frontier callers.  NOT claimed here: the page's own per-type semantics — those live on the typed-list document, which owns the full walk.  ## Interior citation — frontier hub '00243260' (2026-09-18, SWE2-EC7)  '00243260' — 75 "

```
0029ECB0  push     rbx
0029ECB2  push     rsi
0029ECB3  push     rdi
0029ECB4  sub      rsp, 0x40
0029ECB8  mov      rax, qword ptr [rip + 0x1ca5b71]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0029ECBF  xor      rax, rsp
0029ECC2  mov      qword ptr [rsp + 0x38], rax
0029ECC7  mov      eax, edx
0029ECC9  mov      rsi, r8
0029ECCC  mov      qword ptr [rsp + 0x28], rax
0029ECD1  lea      r8, [rsp + 0x20]
0029ECD6  mov      rax, qword ptr [rcx]
0029ECD9  mov      rdi, rcx
0029ECDC  mov      dword ptr [rsp + 0x20], 0
0029ECE4  mov      ecx, 0xc0
0029ECE9  mov      edx, dword ptr [rax + 0xc]
0029ECEC  mov      qword ptr [rsp + 0x30], rdx
0029ECF1  lea      rdx, [rip - 0x528]  ; -> 0029E7D0
0029ECF8  call     0x244f50  ; -> 00244F50 fn
0029ECFD  mov      rdx, rax
0029ED00  mov      rcx, rsi
0029ED03  mov      rbx, rax
0029ED06  call     0x244960  ; -> 00244960 fn
0029ED0B  mov      qword ptr [rdi + 0x18], rbx
0029ED0F  mov      rcx, qword ptr [rsp + 0x38]
0029ED14  xor      rcx, rsp
0029ED17  call     0x808c40  ; -> 00808C40 fn
0029ED1C  add      rsp, 0x40
0029ED20  pop      rdi
0029ED21  pop      rsi
0029ED22  pop      rbx
0029ED23  ret      
```

## 002CCCF0 (72 B, extent 002CCCF0-002CCD38)

Page context: "' shifted to the sign bits is positive; otherwise it '00246AD0's the '0208EA28' root with 'rbx' and a stack template '{0x5000000050000000, 0x5000000050000000}', resolves 'word[[rbx+0x48]+2]' through '002CCCF0', and when 'dword[+0x40] & 0x1000000' and the result is non-null runs '00247730(rax, 1)' - cookie-protected ('00808C40').  Interior anchor '002C1A33' (function '002C19E0').  '005386F0' (141 B) is the state-refresh arm the widget's "

```
002CCCF0  sub      rsp, 0x58
002CCCF4  mov      rax, qword ptr [rip + 0x1c77b35]  ; -> 01F44830 [u64 0x00002B992DDFA232]
002CCCFB  xor      rax, rsp
002CCCFE  mov      qword ptr [rsp + 0x40], rax
002CCD03  xor      r8d, r8d
002CCD06  mov      qword ptr [rsp + 0x28], rcx
002CCD0B  mov      eax, edx
002CCD0D  lea      rcx, [rsp + 0x20]
002CCD12  mov      qword ptr [rsp + 0x20], r8
002CCD17  mov      qword ptr [rsp + 0x30], rax
002CCD1C  mov      qword ptr [rsp + 0x38], r8
002CCD21  call     0x2ccd40  ; -> 002CCD40 fn
002CCD26  mov      rcx, qword ptr [rsp + 0x40]
002CCD2B  xor      rcx, rsp
002CCD2E  call     0x808c40  ; -> 00808C40 fn
002CCD33  add      rsp, 0x58
002CCD37  ret      
```

## 002CFD30 (104 B, extent 002CFD30-002CFD98)

Page context: "0' resolves the object, and '00252FA0(word[rbx])' answering <= 1 returns -1; otherwise the '(edi, esi)' pair picks one of five handlers — 'esi' == 0 -> '002CFFE0', 'esi' == 1 dispatches 'edi' {0,3}->'002CFD30' / 1->'002CFEE0' / 2->'002D0100', 'esi' == 2 -> '002D0200' — and '00249CE0(&rec, obj, 2, fn)' registers the pick.  Interior anchor '00565D99' (function '00565CD0').  '005641F0' (259 B) is the '[+0xE0]'-record select '005651E0' runs"

```
002CFD30  mov      qword ptr [rsp + 8], rbx
002CFD35  mov      qword ptr [rsp + 0x10], rbp
002CFD3A  mov      qword ptr [rsp + 0x18], rsi
002CFD3F  push     rdi
002CFD40  sub      rsp, 0x20
002CFD44  movzx    ebx, word ptr [rcx]
002CFD47  mov      rsi, rdx
002CFD4A  movzx    edx, word ptr [rdx]
002CFD4D  mov      rbp, rcx
002CFD50  shl      edx, 0x10
002CFD53  mov      ecx, 1
002CFD58  call     0x35d330  ; -> 0035D330 fn
002CFD5D  shl      ebx, 0x10
002CFD60  mov      ecx, 1
002CFD65  mov      edx, ebx
002CFD67  mov      edi, dword ptr [rax + 0x58]
002CFD6A  call     0x35d330  ; -> 0035D330 fn
002CFD6F  sub      edi, dword ptr [rax + 0x58]
002CFD72  jne      0x2cfd81  ; -> 002CFD81
002CFD74  mov      rdx, rsi
002CFD77  mov      rcx, rbp
002CFD7A  call     0x2cfda0  ; -> 002CFDA0 fn
002CFD7F  jmp      0x2cfd83  ; -> 002CFD83
002CFD81  mov      eax, edi
002CFD83  mov      rbx, qword ptr [rsp + 0x30]
002CFD88  mov      rbp, qword ptr [rsp + 0x38]
002CFD8D  mov      rsi, qword ptr [rsp + 0x40]
002CFD92  add      rsp, 0x20
002CFD96  pop      rdi
002CFD97  ret      
```

## 002CFFE0 (130 B, extent 002CFFE0-002D0062)

Page context: "pairs, '00252F40(tbl.w0)' -> '[+4]' -> '0020E600' resolves the object, and '00252FA0(word[rbx])' answering <= 1 returns -1; otherwise the '(edi, esi)' pair picks one of five handlers — 'esi' == 0 -> '002CFFE0', 'esi' == 1 dispatches 'edi' {0,3}->'002CFD30' / 1->'002CFEE0' / 2->'002D0100', 'esi' == 2 -> '002D0200' — and '00249CE0(&rec, obj, 2, fn)' registers the pick.  Interior anchor '00565D99' (function '00565CD0').  '005641F0' (259 B)"

```
002CFFE0  mov      qword ptr [rsp + 0x10], rbx
002CFFE5  push     rdi
002CFFE6  sub      rsp, 0x20
002CFFEA  mov      rdi, rdx
002CFFED  mov      rbx, rcx
002CFFF0  movzx    edx, word ptr [rcx]
002CFFF3  mov      ecx, 1
002CFFF8  shl      edx, 0x10
002CFFFB  call     0x35d330  ; -> 0035D330 fn
002D0000  cmp      dword ptr [rax], 6
002D0003  jne      0x2d001a  ; -> 002D001A
002D0005  mov      rdx, rdi
002D0008  mov      rcx, rbx
002D000B  mov      rbx, qword ptr [rsp + 0x38]
002D0010  add      rsp, 0x20
002D0014  pop      rdi
002D0015  jmp      0x2cfda0  ; -> 002CFDA0 fn
002D001A  movzx    edi, word ptr [rdi]
002D001D  mov      ecx, 1
002D0022  mov      qword ptr [rsp + 0x30], rsi
002D0027  movzx    esi, word ptr [rbx]
002D002A  mov      edx, esi
002D002C  shl      edx, 0x10
002D002F  call     0x35d330  ; -> 0035D330 fn
002D0034  mov      edx, edi
002D0036  mov      ecx, 1
002D003B  shl      edx, 0x10
002D003E  mov      ebx, dword ptr [rax + 0x30]
002D0041  call     0x35d330  ; -> 0035D330 fn
002D0046  sub      esi, edi
002D0048  sub      ebx, dword ptr [rax + 0x30]
002D004B  test     ebx, ebx
002D004D  cmovne   esi, ebx
002D0050  mov      rbx, qword ptr [rsp + 0x38]
002D0055  mov      eax, esi
002D0057  mov      rsi, qword ptr [rsp + 0x30]
002D005C  add      rsp, 0x20
002D0060  pop      rdi
002D0061  ret      
```

## 002D0100 (145 B, extent 002D0100-002D0191)

Page context: "52FA0(word[rbx])' answering <= 1 returns -1; otherwise the '(edi, esi)' pair picks one of five handlers — 'esi' == 0 -> '002CFFE0', 'esi' == 1 dispatches 'edi' {0,3}->'002CFD30' / 1->'002CFEE0' / 2->'002D0100', 'esi' == 2 -> '002D0200' — and '00249CE0(&rec, obj, 2, fn)' registers the pick.  Interior anchor '00565D99' (function '00565CD0').  '005641F0' (259 B) is the '[+0xE0]'-record select '005651E0' runs — the sibling of '005687F0' on "

```
002D0100  mov      qword ptr [rsp + 8], rbx
002D0105  mov      qword ptr [rsp + 0x10], rbp
002D010A  mov      qword ptr [rsp + 0x18], rsi
002D010F  push     rdi
002D0110  sub      rsp, 0x20
002D0114  movzx    ebx, word ptr [rcx]
002D0117  mov      rsi, rdx
002D011A  movzx    edx, word ptr [rdx]
002D011D  mov      rbp, rcx
002D0120  shl      edx, 0x10
002D0123  mov      ecx, 1
002D0128  call     0x35d330  ; -> 0035D330 fn
002D012D  shl      ebx, 0x10
002D0130  mov      ecx, 1
002D0135  mov      edx, ebx
002D0137  mov      edi, dword ptr [rax + 0x5c]
002D013A  call     0x35d330  ; -> 0035D330 fn
002D013F  sub      edi, dword ptr [rax + 0x5c]
002D0142  jne      0x2d017a  ; -> 002D017A
002D0144  movzx    edx, word ptr [rsi]
002D0147  lea      ecx, [rdi + 1]
002D014A  movzx    ebx, word ptr [rbp]
002D014E  shl      edx, 0x10
002D0151  call     0x35d330  ; -> 0035D330 fn
002D0156  shl      ebx, 0x10
002D0159  mov      ecx, 1
002D015E  mov      edx, ebx
002D0160  mov      edi, dword ptr [rax + 0x60]
002D0163  call     0x35d330  ; -> 0035D330 fn
002D0168  sub      edi, dword ptr [rax + 0x60]
002D016B  jne      0x2d017a  ; -> 002D017A
002D016D  mov      rdx, rsi
002D0170  mov      rcx, rbp
002D0173  call     0x2cfda0  ; -> 002CFDA0 fn
002D0178  jmp      0x2d017c  ; -> 002D017C
002D017A  mov      eax, edi
002D017C  mov      rbx, qword ptr [rsp + 0x30]
002D0181  mov      rbp, qword ptr [rsp + 0x38]
002D0186  mov      rsi, qword ptr [rsp + 0x40]
002D018B  add      rsp, 0x20
002D018F  pop      rdi
002D0190  ret      
```

## 002D0200 (104 B, extent 002D0200-002D0268)

Page context: "g <= 1 returns -1; otherwise the '(edi, esi)' pair picks one of five handlers — 'esi' == 0 -> '002CFFE0', 'esi' == 1 dispatches 'edi' {0,3}->'002CFD30' / 1->'002CFEE0' / 2->'002D0100', 'esi' == 2 -> '002D0200' — and '00249CE0(&rec, obj, 2, fn)' registers the pick.  Interior anchor '00565D99' (function '00565CD0').  '005641F0' (259 B) is the '[+0xE0]'-record select '005651E0' runs — the sibling of '005687F0' on the sibling record: '[+0xE"

```
002D0200  mov      qword ptr [rsp + 8], rbx
002D0205  mov      qword ptr [rsp + 0x10], rbp
002D020A  mov      qword ptr [rsp + 0x18], rsi
002D020F  push     rdi
002D0210  sub      rsp, 0x20
002D0214  movzx    ebx, word ptr [rcx]
002D0217  mov      rsi, rdx
002D021A  movzx    edx, word ptr [rdx]
002D021D  mov      rbp, rcx
002D0220  shl      edx, 0x10
002D0223  mov      ecx, 1
002D0228  call     0x35d330  ; -> 0035D330 fn
002D022D  shl      ebx, 0x10
002D0230  mov      ecx, 1
002D0235  mov      edx, ebx
002D0237  mov      edi, dword ptr [rax + 0x24]
002D023A  call     0x35d330  ; -> 0035D330 fn
002D023F  sub      edi, dword ptr [rax + 0x24]
002D0242  jne      0x2d0251  ; -> 002D0251
002D0244  mov      rdx, rsi
002D0247  mov      rcx, rbp
002D024A  call     0x2cffe0  ; -> 002CFFE0 fn
002D024F  jmp      0x2d0253  ; -> 002D0253
002D0251  mov      eax, edi
002D0253  mov      rbx, qword ptr [rsp + 0x30]
002D0258  mov      rbp, qword ptr [rsp + 0x38]
002D025D  mov      rsi, qword ptr [rsp + 0x40]
002D0262  add      rsp, 0x20
002D0266  pop      rdi
002D0267  ret      
```

## 003F8490 (126 B, extent 003F8490-003F850E)

Page context: "2E0'/'00808C40'. Interior anchor '003FB9AB' (an '00861F0E' call).  ## SWE2-EC7-41 update (2026-09-19) - '003F8640'  '003F8640' (335 B) is a widget body - '009155D8'/'00D11D50'/'01F44830', '00244F00'/'003F8490'/'00245000'/'002F9860' pair/'0029CD00'/'00808C40'. Interior anchor '003F8674' (a '00244F00' call).  ## SWE2-EC7-44 update (2026-09-19) - '002985D0'  '002985D0' (266 B) is the 'r8'-passed proc body of the fourteen-slot table - '0024"

```
003F8490  mov      qword ptr [rsp + 8], rbx
003F8495  mov      qword ptr [rsp + 0x10], rbp
003F849A  mov      qword ptr [rsp + 0x18], rsi
003F849F  push     rdi
003F84A0  sub      rsp, 0x20
003F84A4  xor      ebp, ebp
003F84A6  mov      rbx, rcx
003F84A9  mov      edi, ebp
003F84AB  nop      dword ptr [rax + rax]
003F84B0  mov      eax, dword ptr [rbx + 0x750]
003F84B6  cmp      eax, 8
003F84B9  jae      0x3f84bf  ; -> 003F84BF
003F84BB  test     eax, eax
003F84BD  jns      0x3f84c5  ; -> 003F84C5
003F84BF  mov      dword ptr [rbx + 0x750], ebp
003F84C5  movsxd   rcx, dword ptr [rbx + 0x750]
003F84CC  imul     rsi, rcx, 0xe8
003F84D3  lea      eax, [rcx + 1]
003F84D6  add      rsi, rbx
003F84D9  mov      dword ptr [rbx + 0x750], eax
003F84DF  mov      rcx, rsi
003F84E2  call     0x273a20  ; -> 00273A20 fn
003F84E7  test     eax, eax
003F84E9  je       0x3f84f6  ; -> 003F84F6
003F84EB  inc      edi
003F84ED  cmp      edi, 8
003F84F0  jb       0x3f84b0  ; -> 003F84B0
003F84F2  xor      eax, eax
003F84F4  jmp      0x3f84f9  ; -> 003F84F9
003F84F6  mov      rax, rsi
003F84F9  mov      rbx, qword ptr [rsp + 0x30]
003F84FE  mov      rbp, qword ptr [rsp + 0x38]
003F8503  mov      rsi, qword ptr [rsp + 0x40]
003F8508  add      rsp, 0x20
003F850C  pop      rdi
003F850D  ret      
```
