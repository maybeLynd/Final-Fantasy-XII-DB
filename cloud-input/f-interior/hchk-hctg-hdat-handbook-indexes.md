# F-interior pack: `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/hchk-hctg-hdat-handbook-indexes.md`

Generated 2026-10-02 18:41 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/hchk-hctg-hdat-handbook-indexes.json`.

Functions: 4. Each is cited on the page only at its entry and is still in the F frontier.

## 002C2280 (100 B, extent 002C2280-002C22E4)

Page context: "* 155 inbound (UI bodies '00571F60', '00281AE0', '002D70F0' call page-cited '00245020', '0035D330', '0024A5A0'); 11 outbound (page-cited '00281ED0', '0056F5F0', '0056F810' call UI bodies '00291D80', '002C2280', '005678A0'). Read (2026-09-30, SWE2-CONTRACT): the widest fan-ins are UI-wide helpers the page cites ('00247510', '00245020', '0035D330', '002B58B0'), MECHANICAL. The relationship is menu code building image records the way the h"

```
002C2280  sub      rsp, 0x48
002C2284  mov      rax, qword ptr [rip + 0x1c825a5]  ; -> 01F44830 [u64 0x00002B992DDFA232]
002C228B  xor      rax, rsp
002C228E  mov      qword ptr [rsp + 0x38], rax
002C2293  mov      rax, qword ptr [rip + 0x1dd8996]  ; -> 0209AC30
002C229A  cmp      qword ptr [rax + 0x140], 0
002C22A2  jne      0x2c22d2  ; -> 002C22D2
002C22A4  movsxd   rax, ecx
002C22A7  lea      r8, [rsp + 0x20]
002C22AC  mov      qword ptr [rsp + 0x28], rax
002C22B1  mov      ecx, 0x170
002C22B6  movsxd   rax, edx
002C22B9  lea      rdx, [rip + 0x60]  ; -> 002C2320
002C22C0  mov      qword ptr [rsp + 0x30], rax
002C22C5  mov      dword ptr [rsp + 0x20], 0
002C22CD  call     0x244f50  ; -> 00244F50 fn
002C22D2  mov      rcx, qword ptr [rsp + 0x38]
002C22D7  xor      rcx, rsp
002C22DA  call     0x808c40  ; -> 00808C40 fn
002C22DF  add      rsp, 0x48
002C22E3  ret      
```

## 00574080 (213 B, extent 00574080-00574155)

Page context: "     the family descriptor 'out+0x04' (00576061: word>>4) — **dead on                           the data path**: none of '00576030''s three callers ('00570BF0',                           '00571F60', '00574080') ever reads 'out+0x04'. Per-family values                           {story 0x1900, world 0x1901, person 0xF72, knowledge 0x1903,   <- corrected 2026-10-02, OPUS: these are the whole u16 at +0x08, not its high 12 bits              "

```
00574080  mov      qword ptr [rsp + 0x18], rbx
00574085  push     rbp
00574086  push     rsi
00574087  push     rdi
00574088  sub      rsp, 0x40
0057408C  mov      rax, qword ptr [rip + 0x19d079d]  ; -> 01F44830 [u64 0x00002B992DDFA232]
00574093  xor      rax, rsp
00574096  mov      qword ptr [rsp + 0x30], rax
0057409B  mov      rsi, rcx
0057409E  mov      rdi, rdx
005740A1  lea      rcx, [rsp + 0x20]
005740A6  xor      ebx, ebx
005740A8  call     0x576030  ; -> 00576030 fn
005740AD  test     rsi, rsi
005740B0  jne      0x5740b6  ; -> 005740B6
005740B2  mov      ebp, ebx
005740B4  jmp      0x5740bd  ; -> 005740BD
005740B6  mov      rax, qword ptr [rsi + 0x60]
005740BA  mov      rbp, qword ptr [rax]
005740BD  mov      rax, qword ptr [rsi + 0xe0]
005740C4  test     rax, rax
005740C7  je       0x5740dc  ; -> 005740DC
005740C9  mov      rax, qword ptr [rax + 0xc0]
005740D0  test     rax, rax
005740D3  je       0x5740dc  ; -> 005740DC
005740D5  mov      rax, qword ptr [rax + 0x60]
005740D9  mov      rbx, qword ptr [rax]
005740DC  mov      rbp, qword ptr [rbp]
005740E0  movzx    eax, word ptr [rbp + 4]
005740E4  mov      word ptr [rdi], ax
005740E7  movzx    eax, word ptr [rbp + 6]
005740EB  mov      word ptr [rdi + 2], ax
005740EF  test     rbx, rbx
005740F2  je       0x5740fa  ; -> 005740FA
005740F4  movzx    eax, word ptr [rbx + 0x10]
005740F8  jmp      0x5740ff  ; -> 005740FF
005740FA  mov      eax, 0x64
005740FF  mov      word ptr [rdi + 4], ax
00574103  mov      rax, qword ptr [rsi + 0xe8]
0057410A  movzx    ebx, word ptr [rbp + 0xc]
0057410E  mov      ecx, dword ptr [rax + 0x20]
00574111  call     0x20e600  ; -> 0020E600 fn
00574116  lea      rdx, [rbx + rbx*4]
0057411A  movzx    ecx, word ptr [rax + rdx*4 + 0xa]
0057411F  lea      r8, [rax + rdx*4]
00574123  movzx    eax, word ptr [rbp + 0xa]
00574127  xor      edx, edx
00574129  div      ecx
0057412B  mov      byte ptr [rdi + 6], al
0057412E  mov      rax, r8
00574131  movzx    ecx, byte ptr [rbp + 8]
00574135  sub      cl, byte ptr [rdi + 4]
00574138  mov      byte ptr [rdi + 7], cl
0057413B  mov      rcx, qword ptr [rsp + 0x30]
00574140  xor      rcx, rsp
00574143  call     0x808c40  ; -> 00808C40 fn
00574148  mov      rbx, qword ptr [rsp + 0x70]
0057414D  add      rsp, 0x40
00574151  pop      rdi
00574152  pop      rsi
00574153  pop      rbp
00574154  ret      
```

## 005766E0 (89 B, extent 005766E0-00576739)

Page context: "for fam 0–5/7; fam 6 → '0037F060(menuquest.dat, 1)'; else 1) — so 'out+0x0E' is the member count when the tab is active at all, else 0 (a visible/locked toggle, not a per-record progress numerator). '005766E0(recIdx)' is the plain accessor returning 'word[rec+4]' — the record's section index.  **Record table** at 'recTableOff': 'recordCount' × 12-byte records.  ''' +0x00  u32  textId     message/string-table id (story: 70600, 70601, …; "

```
005766E0  mov      rax, qword ptr [rip + 0x2733051]  ; -> 02CA9738
005766E7  movsxd   r8, ecx
005766EA  test     rax, rax
005766ED  je       0x576736  ; -> 00576736
005766EF  mov      rcx, qword ptr [rax + 0x108]
005766F6  cmp      byte ptr [rcx + 0xc9], 1
005766FD  jne      0x576736  ; -> 00576736
005766FF  test     rcx, rcx
00576702  je       0x576736  ; -> 00576736
00576704  mov      rdx, qword ptr [rcx + 0xf0]
0057670B  test     rdx, rdx
0057670E  je       0x576736  ; -> 00576736
00576710  test     r8d, r8d
00576713  js       0x576736  ; -> 00576736
00576715  movzx    eax, word ptr [rdx + 0xe]
00576719  cmp      r8d, eax
0057671C  jge      0x576736  ; -> 00576736
0057671E  movzx    eax, word ptr [rdx + 0xa]
00576722  lea      rcx, [r8 + r8*2]
00576726  add      eax, edx
00576728  lea      rax, [rax + rcx*4]
0057672C  test     rax, rax
0057672F  je       0x576736  ; -> 00576736
00576731  movzx    eax, word ptr [rax + 4]
00576735  ret      
00576736  xor      eax, eax
00576738  ret      
```

## 00576DA0 (100 B, extent 00576DA0-00576E04)

Page context: "75DD0'/'00577970' page requests, '00575F10'/'005776D0'/'00577880'/'005771F0' state, '00576030' family descriptor, '005766E0' group accessor, '00576740' section resolver, '00576A50' caption resolver, '00576DA0' all-loaded check) — so 'v1'/'v2'/'v3' are dead-authored (v3 redundantly encodes the 'rec+0x0A' category flag that IS read).  ### The detail resolver '005760A0(out, recIdx)'  Called for the selected record; fills the detail-panel d"

```
00576DA0  mov      rax, qword ptr [rip + 0x2732991]  ; -> 02CA9738
00576DA7  test     rax, rax
00576DAA  je       0x576e01  ; -> 00576E01
00576DAC  mov      rcx, qword ptr [rax + 0x108]
00576DB3  test     rcx, rcx
00576DB6  je       0x576dcd  ; -> 00576DCD
00576DB8  movzx    ecx, byte ptr [rcx + 0xc9]
00576DBF  sub      cl, 2
00576DC2  cmp      cl, 1
00576DC5  ja       0x576dcd  ; -> 00576DCD
00576DC7  mov      eax, 1
00576DCC  ret      
00576DCD  mov      rcx, qword ptr [rax + 0x110]
00576DD4  test     rcx, rcx
00576DD7  je       0x576de8  ; -> 00576DE8
00576DD9  movzx    ecx, byte ptr [rcx + 0xc9]
00576DE0  sub      cl, 2
00576DE3  cmp      cl, 1
00576DE6  jbe      0x576dc7  ; -> 00576DC7
00576DE8  mov      rcx, qword ptr [rax + 0x118]
00576DEF  test     rcx, rcx
00576DF2  je       0x576e01  ; -> 00576E01
00576DF4  movzx    eax, byte ptr [rcx + 0xc9]
00576DFB  sub      al, 2
00576DFD  cmp      al, 1
00576DFF  jbe      0x576dc7  ; -> 00576DC7
00576E01  xor      eax, eax
00576E03  ret      
```
