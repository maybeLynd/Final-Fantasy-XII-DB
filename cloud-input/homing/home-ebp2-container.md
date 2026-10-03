# Homing pack: `25-EBP-Script-Container/Container/ebp2-container.md`

Generated 2026-10-03 08:08 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-ebp2-container.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00474070 (140 B, extent 00474070-004740FC)

Entered from (direct sites whose caller this page cites): `003545B0` + 0x94 (call; `003545B0` is cited on this page)
Other direct sites: none

Host context: "erior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*  | function | size | what the body does | interior anchors | |---|---|---|---| | '003545B0' | 184 B | calls '002640C0' with the incoming registers (result p), then reads five values a, b, c, d, e by the calls at '003545B0+0x2C', '+0x36', '+0x40', '+0x4B', '+0x56' (each with 'r9'); calls '00264D60(p, e)' and '002673A0(p, "

```
00474070  sub      rsp, 0x58
00474074  mov      rax, qword ptr [rip + 0x1ad07b5]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0047407B  xor      rax, rsp
0047407E  mov      qword ptr [rsp + 0x48], rax
00474083  mov      eax, dword ptr [rsp + 0x80]
0047408A  mov      dword ptr [rsp + 0x44], eax
0047408E  lea      rax, [rsp + 0x38]
00474093  mov      qword ptr [rsp + 0x30], rax
00474098  mov      rax, qword ptr [rsp + 0x88]
004740A0  mov      dword ptr [rsp + 0x38], edx
004740A4  lea      rdx, [rip + 0x55]  ; -> 00474100
004740AB  mov      dword ptr [rsp + 0x3c], r8d
004740B0  lea      r8, [rsp + 0x20]
004740B5  mov      qword ptr [rsp + 0x28], rcx
004740BA  mov      ecx, 0x1d8
004740BF  mov      qword ptr [rip + 0x2832bb2], rax  ; -> 02CA6C78
004740C6  mov      dword ptr [rsp + 0x40], r9d
004740CB  mov      dword ptr [rsp + 0x20], 0
004740D3  call     0x244f50  ; -> 00244F50 fn
004740D8  mov      qword ptr [rip + 0x2832ba1], rax  ; -> 02CA6C80
004740DF  mov      qword ptr [rip + 0x2832b8e], 0  ; -> 02CA6C78
004740EA  mov      rcx, qword ptr [rsp + 0x48]
004740EF  xor      rcx, rsp
004740F2  call     0x808c40  ; -> 00808C40 fn
004740F7  add      rsp, 0x58
004740FB  ret      
```
