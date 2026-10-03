# Homing pack: `18-Audio/the-music-control-file-and-the-bgm-stream.md`

Generated 2026-10-03 11:24 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h9-the-music-control-file-and-the-bgm-stream.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 003EACA0 (98 B, extent 003EACA0-003EAD02)

Entered from (direct sites whose caller this page cites): `003557C0` + 0x17 (call; `003557C0` is cited on this page)
Other direct sites: none

Host context: "ded to 002DF680 at play   +0x33  u8    0x7F             handed to 002DF680 at play '''  ### 3.2 The verbs  | id | verb | handler | what it does | |---|---|---|---| | '044D' | 'usebgmstream(bytes)' | '003557C0' | frees any stream ('003EB010'), then '003EACA0(bytes)': rounds up to a 64 KB multiple with a floor of '0x30000', allocates from heap 2 ('0036C1D0(2)', '0036A190'), tags it with the empty string at '00D51814' ('0036C660'), and '00"

```
003EACA0  mov      qword ptr [rsp + 8], rbx
003EACA5  push     rdi
003EACA6  sub      rsp, 0x20
003EACAA  lea      eax, [rcx + 0xffff]
003EACB0  cdq      
003EACB1  movzx    edi, dx
003EACB4  mov      edx, 5
003EACB9  add      edi, eax
003EACBB  mov      eax, 0x30000
003EACC0  and      edi, 0xffff0000
003EACC6  cmp      edi, eax
003EACC8  lea      ecx, [rdx - 3]
003EACCB  cmovl    edi, eax
003EACCE  call     0x36c1d0  ; -> 0036C1D0 fn
003EACD3  mov      ecx, edi
003EACD5  call     0x36a190  ; -> 0036A190 fn
003EACDA  mov      r8d, edi
003EACDD  lea      rdx, [rip + 0x926b30]  ; -> 00D11814 [str "BGMSTR"]
003EACE4  mov      rcx, rax
003EACE7  mov      rbx, rax
003EACEA  call     0x36c660  ; -> 0036C660 fn
003EACEF  call     0x36c140  ; -> 0036C140 fn
003EACF4  mov      rax, rbx
003EACF7  mov      rbx, qword ptr [rsp + 0x30]
003EACFC  add      rsp, 0x20
003EAD00  pop      rdi
003EAD01  ret      
```
