# Homing pack: `09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md`

Generated 2026-10-03 00:35 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-gambit-evaluation-and-enmity.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 003340C0 (87 B, extent 003340C0-00334117)

Entered from (direct sites whose caller this page cites): `003A7AA0` + 0x26 (call; `003A7AA0` is cited on this page)
Other direct sites: none

Host context: "n 'edx') to '003A7A50' + 0x37, and returns 'rcx+0xA4' | Interior anchor '003A7A5E'; Interior anchor '003A7A69'; Interior anchor '003A7A81'; Interior anchor '003A7A87'; Interior anchor '003A7A8C' | | '003A7AA0' | 53 B | '003ED8A0' + 0x1C7 | when qword '02EBEFA8' '+8' + byte 'rcx+1' times 8 holds a non-null qword, calls '003A7AA0' + 0x26 with it and the zero-extended byte 'rcx+2'; returns 'rcx+3' on both paths | Interior anchor '003A7AB9'"

```
003340C0  sub      rsp, 0x28
003340C4  cmp      edx, 0x1d
003340C7  jge      0x334112  ; -> 00334112
003340C9  movsxd   rax, edx
003340CC  mov      qword ptr [rsp + 0x20], rbx
003340D1  lea      rbx, [rcx + rax*4]
003340D5  mov      ecx, dword ptr [rcx + rax*4 + 0x2c]
003340D9  call     0x20e600  ; -> 0020E600 fn
003340DE  test     rax, rax
003340E1  je       0x33410d  ; -> 0033410D
003340E3  mov      ecx, dword ptr [rbx + 0x2c]
003340E6  call     0x20e600  ; -> 0020E600 fn
003340EB  mov      rcx, rax
003340EE  call     0x46f370  ; -> 0046F370 fn
003340F3  mov      ecx, dword ptr [rbx + 0x2c]
003340F6  call     0x20e600  ; -> 0020E600 fn
003340FB  mov      rcx, rax
003340FE  call     0x3697f0  ; -> 003697F0 fn
00334103  xor      ecx, ecx
00334105  call     0x20e620  ; -> 0020E620 fn
0033410A  mov      dword ptr [rbx + 0x2c], eax
0033410D  mov      rbx, qword ptr [rsp + 0x20]
00334112  add      rsp, 0x28
00334116  ret      
```
