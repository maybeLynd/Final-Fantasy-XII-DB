# F-interior pack: `08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md`

Generated 2026-10-03 02:32 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/the-hp-write-and-the-lethal-transition.json`.

Functions: 6. Each is cited on the page only at its entry and is still in the F frontier.

## 00340CB0 (75 B, extent 00340CB0-00340CFB)

Page context: "gh 'VMValueStack_PopInt32CoerceFloat32' '00267E10' (and '00341B20' pushes through 'VMValueStack_PushInt32' '00267F90'), and they, '00348C50' and '0034A110' call the absolute setter '004738D0', while '00340CB0', '003421D0' and '00349220' call the ratio setter '00473980'; 'btlAtelSetHpLowLimit' '005105E0' pops through '00267E10'; twelve verbs, among them '00342150', '00342D40', '003438F0' and '00349C90', call '003589B0'; '00344740', '0035"

```
00340CB0  mov      qword ptr [rsp + 8], rbx
00340CB5  mov      qword ptr [rsp + 0x10], rsi
00340CBA  push     rdi
00340CBB  sub      rsp, 0x20
00340CBF  mov      rcx, rdx
00340CC2  mov      rsi, r9
00340CC5  call     0x263f10  ; -> 00263F10 fn
00340CCA  mov      rcx, rsi
00340CCD  mov      rdi, rax
00340CD0  call     0x267e10  ; -> 00267E10 fn
00340CD5  mov      rcx, rsi
00340CD8  mov      ebx, eax
00340CDA  call     0x267e10  ; -> 00267E10 fn
00340CDF  mov      r8d, ebx
00340CE2  mov      edx, eax
00340CE4  mov      rcx, rdi
00340CE7  mov      rbx, qword ptr [rsp + 0x30]
00340CEC  mov      rsi, qword ptr [rsp + 0x38]
00340CF1  add      rsp, 0x20
00340CF5  pop      rdi
00340CF6  jmp      0x473980  ; -> 00473980 fn
```

## 003421D0 (91 B, extent 003421D0-0034222B)

Page context: "tack_PopInt32CoerceFloat32' '00267E10' (and '00341B20' pushes through 'VMValueStack_PushInt32' '00267F90'), and they, '00348C50' and '0034A110' call the absolute setter '004738D0', while '00340CB0', '003421D0' and '00349220' call the ratio setter '00473980'; 'btlAtelSetHpLowLimit' '005105E0' pops through '00267E10'; twelve verbs, among them '00342150', '00342D40', '003438F0' and '00349C90', call '003589B0'; '00344740', '00352FA0', '0035"

```
003421D0  mov      qword ptr [rsp + 8], rbx
003421D5  mov      qword ptr [rsp + 0x10], rsi
003421DA  push     rdi
003421DB  sub      rsp, 0x20
003421DF  mov      rbx, rdx
003421E2  mov      rcx, r9
003421E5  mov      edx, 2
003421EA  mov      rsi, r9
003421ED  call     0x267f90  ; -> 00267F90 fn
003421F2  mov      rcx, rbx
003421F5  call     0x263f10  ; -> 00263F10 fn
003421FA  mov      rcx, rsi
003421FD  mov      rdi, rax
00342200  call     0x267e10  ; -> 00267E10 fn
00342205  mov      rcx, rsi
00342208  mov      ebx, eax
0034220A  call     0x267e10  ; -> 00267E10 fn
0034220F  mov      r8d, ebx
00342212  mov      edx, eax
00342214  mov      rcx, rdi
00342217  mov      rbx, qword ptr [rsp + 0x30]
0034221C  mov      rsi, qword ptr [rsp + 0x38]
00342221  add      rsp, 0x20
00342225  pop      rdi
00342226  jmp      0x473980  ; -> 00473980 fn
```

## 00343D10 (124 B, extent 00343D10-00343D8C)

Page context: "005105E0' pops through '00267E10'; twelve verbs, among them '00342150', '00342D40', '003438F0' and '00349C90', call '003589B0'; '00344740', '00352FA0', '003537D0' and '00355680' call '00377C20'; and '00343D10', '00344F80' and '00345C20' call '003A1920'. Authored script sets HP through its own setters, which reach the same HP three calls deeper (§5), and sets the low-HP limit the clamp floor honours; the other verb edges share the page's"

```
00343D10  mov      qword ptr [rsp + 8], rbx
00343D15  mov      qword ptr [rsp + 0x10], rbp
00343D1A  mov      qword ptr [rsp + 0x18], rsi
00343D1F  push     rdi
00343D20  sub      rsp, 0x20
00343D24  mov      rbp, rcx
00343D27  mov      rdi, r9
00343D2A  mov      rcx, r9
00343D2D  call     0x267e10  ; -> 00267E10 fn
00343D32  mov      rcx, rdi
00343D35  mov      ebx, eax
00343D37  call     0x267e10  ; -> 00267E10 fn
00343D3C  mov      ecx, ebx
00343D3E  mov      edi, eax
00343D40  call     0x264010  ; -> 00264010 fn
00343D45  mov      ecx, edi
00343D47  mov      rsi, rax
00343D4A  call     0x264010  ; -> 00264010 fn
00343D4F  mov      rcx, rax
00343D52  call     0x265060  ; -> 00265060 fn
00343D57  mov      rcx, rsi
00343D5A  mov      rbx, rax
00343D5D  call     0x265060  ; -> 00265060 fn
00343D62  mov      rcx, rax
00343D65  mov      rdx, rbx
00343D68  call     0x3a1920  ; -> 003A1920 fn
00343D6D  movaps   xmm1, xmm0
00343D70  mov      rcx, rbp
00343D73  mov      rbx, qword ptr [rsp + 0x30]
00343D78  mov      rbp, qword ptr [rsp + 0x38]
00343D7D  mov      rsi, qword ptr [rsp + 0x40]
00343D82  add      rsp, 0x20
00343D86  pop      rdi
00343D87  jmp      0x26b4c0  ; -> 0026B4C0 fn
```

## 00344F80 (144 B, extent 00344F80-00345010)

Page context: "ps through '00267E10'; twelve verbs, among them '00342150', '00342D40', '003438F0' and '00349C90', call '003589B0'; '00344740', '00352FA0', '003537D0' and '00355680' call '00377C20'; and '00343D10', '00344F80' and '00345C20' call '003A1920'. Authored script sets HP through its own setters, which reach the same HP three calls deeper (§5), and sets the low-HP limit the clamp floor honours; the other verb edges share the page's handle enco"

```
00344F80  mov      qword ptr [rsp + 0x10], rbx
00344F85  push     rdi
00344F86  sub      rsp, 0x40
00344F8A  mov      rax, qword ptr [rip + 0x1bff89f]  ; -> 01F44830 [u64 0x00002B992DDFA232]
00344F91  xor      rax, rsp
00344F94  mov      qword ptr [rsp + 0x30], rax
00344F99  mov      rdi, rcx
00344F9C  mov      rbx, r9
00344F9F  mov      rcx, r9
00344FA2  call     0x267db0  ; -> 00267DB0 fn
00344FA7  mov      rcx, rbx
00344FAA  movss    dword ptr [rsp + 0x28], xmm0
00344FB0  call     0x267db0  ; -> 00267DB0 fn
00344FB5  mov      rcx, rbx
00344FB8  movss    dword ptr [rsp + 0x24], xmm0
00344FBE  call     0x267db0  ; -> 00267DB0 fn
00344FC3  mov      rcx, rbx
00344FC6  movss    dword ptr [rsp + 0x20], xmm0
00344FCC  call     0x267e10  ; -> 00267E10 fn
00344FD1  mov      ecx, eax
00344FD3  call     0x264010  ; -> 00264010 fn
00344FD8  mov      rcx, rax
00344FDB  call     0x265060  ; -> 00265060 fn
00344FE0  mov      rcx, rax
00344FE3  lea      rdx, [rsp + 0x20]
00344FE8  call     0x3a1920  ; -> 003A1920 fn
00344FED  movaps   xmm1, xmm0
00344FF0  mov      rcx, rdi
00344FF3  call     0x26b4c0  ; -> 0026B4C0 fn
00344FF8  mov      rcx, qword ptr [rsp + 0x30]
00344FFD  xor      rcx, rsp
00345000  call     0x808c40  ; -> 00808C40 fn
00345005  mov      rbx, qword ptr [rsp + 0x58]
0034500A  add      rsp, 0x40
0034500E  pop      rdi
0034500F  ret      
```

## 0034A110 (102 B, extent 0034A110-0034A176)

Page context: "' and 'sethpmode' '00340640' pop their arguments through 'VMValueStack_PopInt32CoerceFloat32' '00267E10' (and '00341B20' pushes through 'VMValueStack_PushInt32' '00267F90'), and they, '00348C50' and '0034A110' call the absolute setter '004738D0', while '00340CB0', '003421D0' and '00349220' call the ratio setter '00473980'; 'btlAtelSetHpLowLimit' '005105E0' pops through '00267E10'; twelve verbs, among them '00342150', '00342D40', '003438"

```
0034A110  mov      qword ptr [rsp + 8], rbx
0034A115  mov      qword ptr [rsp + 0x10], rsi
0034A11A  push     rdi
0034A11B  sub      rsp, 0x20
0034A11F  mov      edx, 2
0034A124  mov      rcx, r9
0034A127  mov      rsi, r9
0034A12A  call     0x267f90  ; -> 00267F90 fn
0034A12F  mov      rcx, rsi
0034A132  call     0x267e10  ; -> 00267E10 fn
0034A137  mov      rcx, rsi
0034A13A  mov      edi, eax
0034A13C  call     0x267e10  ; -> 00267E10 fn
0034A141  mov      rcx, rsi
0034A144  mov      ebx, eax
0034A146  call     0x267e10  ; -> 00267E10 fn
0034A14B  mov      ecx, eax
0034A14D  call     0x264010  ; -> 00264010 fn
0034A152  mov      rcx, rax
0034A155  call     0x263f10  ; -> 00263F10 fn
0034A15A  mov      r8d, edi
0034A15D  mov      edx, ebx
0034A15F  mov      rcx, rax
0034A162  mov      rbx, qword ptr [rsp + 0x30]
0034A167  mov      rsi, qword ptr [rsp + 0x38]
0034A16C  add      rsp, 0x20
0034A170  pop      rdi
0034A171  jmp      0x4738d0  ; -> 004738D0 fn
```

## 00473980 (120 B, extent 00473980-004739F8)

Page context: "ABLE): the same HP, three calls deeper.** '004738D0' (absolute, 'sethp' / 'sethp_1f8' / 'sethpmode' / 'sethpmode_391') clamps the amount to '003206E0(handle, 0, 100)' — 100 % of max HP '+0x24' — and '00473980' ('sethpratio' / 'sethpratiomode') passes a percentage; both build a flag word from the verb's option bits (bit 0 → '0x10000000', bit 1 → '0x20000000', bit 2 → '0x40000000'; the absolute forms add bit 31, '0047393A') and call '0032"

```
00473980  mov      qword ptr [rsp + 8], rbx
00473985  mov      qword ptr [rsp + 0x10], rsi
0047398A  push     rdi
0047398B  sub      rsp, 0x20
0047398F  mov      r9d, r8d
00473992  mov      eax, r8d
00473995  and      r9d, 1
00473999  mov      edi, r8d
0047399C  shl      r9d, 0x1c
004739A0  mov      esi, edx
004739A2  mov      ebx, r9d
004739A5  bts      ebx, 0x1d
004739A9  and      al, 2
004739AB  cmove    ebx, r9d
004739AF  and      edi, 4
004739B2  test     rcx, rcx
004739B5  je       0x4739e5  ; -> 004739E5
004739B7  call     0x3589b0  ; -> 003589B0 fn
004739BC  mov      r9d, ebx
004739BF  mov      r8d, esi
004739C2  bts      r9d, 0x1e
004739C7  mov      ecx, eax
004739C9  test     edi, edi
004739CB  cmove    r9d, ebx
004739CF  xor      edx, edx
004739D1  mov      rbx, qword ptr [rsp + 0x30]
004739D6  mov      rsi, qword ptr [rsp + 0x38]
004739DB  add      rsp, 0x20
004739DF  pop      rdi
004739E0  jmp      0x329b70  ; -> 00329B70 fn
004739E5  mov      rbx, qword ptr [rsp + 0x30]
004739EA  or       eax, 0xffffffff
004739ED  mov      rsi, qword ptr [rsp + 0x38]
004739F2  add      rsp, 0x20
004739F6  pop      rdi
004739F7  ret      
```
