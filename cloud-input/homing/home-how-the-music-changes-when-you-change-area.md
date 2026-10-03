# Homing pack: `18-Audio/how-the-music-changes-when-you-change-area.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-how-the-music-changes-when-you-change-area.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0046DE50 (32 B, extent 0046DE50-0046DE70)

Entered from (direct sites whose caller this page cites): `0032EB40` + 0x68 (call; `0032EB40` is cited on this page)
Other direct sites: none

Host context: "this build**. Its only references are the resource initialiser '0032EA90', which zeroes all 256 qwords ('0x20' iterations of 8 stores, '0032EAB1'–'0032EAD8'), and the two size readers '0032E400' and '0032EB40', which fall back to the '.fst' table ('002DF960') whenever the pointer is null. Controls: the RIP scan that finds those three sites finds no other; no absolute displacement and no data qword addresses the array. So every request s"

```
0046DE50  cmp      ecx, 2
0046DE53  jge      0x46de6f  ; -> 0046DE6F
0046DE55  movsxd   rax, ecx
0046DE58  lea      rcx, [rax + rax*4]
0046DE5C  shl      rcx, 5
0046DE60  lea      rax, [rip + 0x2838219]  ; -> 02CA6080
0046DE67  mov      qword ptr [rcx + rax], 0
0046DE6F  ret      
```
