# Homing pack: `01-Script-VM-Native-Bridge/CONTRACT-native-command-lifecycle.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-contract-native-command-lifecycle.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0032A7A0 (65 B, extent 0032A7A0-0032A7E1)

Entered from (direct sites whose caller this page cites): `00342560` + 0x13 (call; `00342560` is cited on this page)
Other direct sites: none

Host context: "ck is 'N < count', which permits 'result(count−1)' to read at 'tbl + 32*count' — one row past the counted rows. Resolved in all five tables, that read yields a **real function pointer** in family 0 ('00342560') and family 7 ('00510970'), and a valid NULL in the other three. **Three tables are packed back to back with exactly the eight bytes that slot needs** — family 3's rows end at '01F29410' and family 5's count begins at '01F29418'; "

```
0032A7A0  cmp      ecx, 5
0032A7A3  ja       0x32a7de  ; -> 0032A7DE
0032A7A5  cmp      cl, 0x27
0032A7A8  jbe      0x32a7ae  ; -> 0032A7AE
0032A7AA  xor      eax, eax
0032A7AC  jmp      0x32a7c6  ; -> 0032A7C6
0032A7AE  movzx    eax, cl
0032A7B1  imul     rcx, rax, 0x1c8
0032A7B8  mov      rax, qword ptr [rip + 0x2b949d1]  ; -> 02EBF190
0032A7BF  add      rax, 8
0032A7C3  add      rax, rcx
0032A7C6  cmp      byte ptr [rax + 0x1c3], 0xff
0032A7CD  jne      0x32a7d8  ; -> 0032A7D8
0032A7CF  cmp      byte ptr [rax + 0x1c4], 0xff
0032A7D6  je       0x32a7de  ; -> 0032A7DE
0032A7D8  mov      eax, 1
0032A7DD  ret      
0032A7DE  xor      eax, eax
0032A7E0  ret      
```
