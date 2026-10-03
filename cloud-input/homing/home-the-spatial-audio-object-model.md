# Homing pack: `18-Audio/the-spatial-audio-object-model.md`

Generated 2026-10-02 22:54 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-spatial-audio-object-model.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00210BE0 (30 B, extent 00210BE0-00210BFE)

Entered from (direct sites whose caller this page cites): `001DBE00` + 0x35 (jmp; `001DBE00` is cited on this page)
Other direct sites: none

Host context: "te (2026-09-19) - '002DEFA0' + '002DEF40' gated audio tails measured  '002DEFA0' (104 B) is the '003603C0'-gated two-call chain: the gate failing returns 0; otherwise '002DE800(rsi, rdi)' runs, then '001DBE00' tails with 'ecx = !(ecx >> 31)', 'edx = ecx & 0x7FFFFFFF', 'r8 = 0215E710' - the sign-bit split the audio bodies share. Interior anchor '002DEFD8' (the '002DE800' call).  '002DEF40' (95 B) is the sibling repack: same '003603C0' ga"

```
00210BE0  mov      eax, r8d
00210BE3  test     edx, edx
00210BE5  mov      edx, eax
00210BE7  mov      r8, r9
00210BEA  jne      0x210bf5  ; -> 00210BF5
00210BEC  mov      rcx, qword ptr [rcx + 8]
00210BF0  jmp      0x21b200  ; -> 0021B200 fn
00210BF5  mov      rcx, qword ptr [rcx + 0x10]
00210BF9  jmp      0x219bc0  ; -> 00219BC0 fn
```

## 002DF280 (17 B, extent 002DF280-002DF291)

Entered from (direct sites whose caller this page cites): `003A0E50` + 0x25 (jmp; `003A0E50` is cited on this page)
Other direct sites: none

Host context: " The 'rel32' chain, every edge read from   the bytes and each function having exactly one caller until the last step:    '''   00221940  <- 00224E40 <- 0021C760 <- 00211200 <- 001DC190 <- 002DF460 <- 003A0E50                                                                              |       <- 00332C40 / 003B99D0 / 0046C8F0 / 0046CC70      (four callers, the first bodies that                                                          pa"

```
002DF280  cmp      ecx, -1
002DF283  jne      0x2df288  ; -> 002DF288
002DF285  xor      eax, eax
002DF287  ret      
002DF288  bts      ecx, 0x1f
002DF28C  jmp      0x2defa0  ; -> 002DEFA0 fn
```
