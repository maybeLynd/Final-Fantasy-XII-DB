# Homing pack: `18-Audio/the-spatial-audio-object-model.md`

Generated 2026-10-03 08:08 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-spatial-audio-object-model.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00223030 (35 B, extent 00223030-00223053)

Entered from (direct sites whose caller this page cites): `00219BC0` + 0x59 (call; `00219BC0` is cited on this page)
Other direct sites: none

Host context: "very anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*  | function | size | entered from | what the body does | interior anchors | |---|---|---|---|---| | '00219BC0' | 122 B | '00210BE0' + 0x19 | walks the circular list whose sentinel is 'rcx+8', from qword '+8' through qword '+0' of each node, stopping at the first node whose object at qword '+0x10' has dword '+0x38' equal to 'edx'; then call"

```
00223030  sub      rsp, 0x48
00223034  mov      qword ptr [rsp + 0x30], r9
00223039  xor      r9d, r9d
0022303C  mov      byte ptr [rsp + 0x28], 1
00223041  mov      dword ptr [rsp + 0x20], 0
00223049  call     0x223190  ; -> 00223190 fn
0022304E  add      rsp, 0x48
00223052  ret      
```
