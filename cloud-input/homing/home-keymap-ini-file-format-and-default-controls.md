# Homing pack: `15-Input/Binding-Profiles/keymap-ini-file-format-and-default-controls.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-keymap-ini-file-format-and-default-controls.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 003B6C70 (78 B, extent 003B6C70-003B6CBE)

Entered from (direct sites whose caller this page cites): `00314820` + 0xD (jmp; `00314820` is cited on this page)
Other direct sites: none

Host context: "very anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*  | function | size | entered from | what the body does | interior anchors | |---|---|---|---|---| | '00314820' | 18 B | '0022A770' + 0x1D8 | calls '00314820' + 0x4 with the incoming registers unchanged, then tail-jumps (+ 0xD) without setting up any argument or reading the call's result | Interior anchor '00314824'; Interior anchor '003148"

```
003B6C70  sub      rsp, 0x48
003B6C74  mov      rax, qword ptr [rip + 0x1b8dbb5]  ; -> 01F44830 [u64 0x00002B992DDFA232]
003B6C7B  xor      rax, rsp
003B6C7E  mov      qword ptr [rsp + 0x30], rax
003B6C83  call     0x259b00  ; -> 00259B00 fn
003B6C88  test     eax, eax
003B6C8A  je       0x3b6cac  ; -> 003B6CAC
003B6C8C  lea      rcx, [rsp + 0x20]
003B6C91  mov      qword ptr [rsp + 0x20], 0x80
003B6C9A  mov      dword ptr [rsp + 0x28], 0xff
003B6CA2  mov      byte ptr [rsp + 0x2f], 0
003B6CA7  call     0x3ed170  ; -> 003ED170 fn
003B6CAC  mov      rcx, qword ptr [rsp + 0x30]
003B6CB1  xor      rcx, rsp
003B6CB4  call     0x808c40  ; -> 00808C40 fn
003B6CB9  add      rsp, 0x48
003B6CBD  ret      
```
