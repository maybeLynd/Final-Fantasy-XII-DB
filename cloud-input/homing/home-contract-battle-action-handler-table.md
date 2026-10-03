# Homing pack: `07-Combat-Action/CONTRACT-battle-action-handler-table.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-contract-battle-action-handler-table.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0031A910 (30 B, extent 0031A910-0031A92E)

Entered from (direct sites whose caller this page cites): `002FDDA0` + 0x343 (call; `002FDDA0` is cited on this page)
Other direct sites: `00344610` + 0x19 (jmp)

Host context: "e category: 07-Combat-Action scope: subsystem level: L2 readiness: CONTRACT READY confidence: PROVEN implements: 07-Combat-Action/Action-Dispatch/battle-action-handler-table.md entries: ["00305080", "002FDDA0"] verified_against:   exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8   method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every     one resolving into a known "

```
0031A910  push     rbx
0031A912  sub      rsp, 0x20
0031A916  mov      edx, 1
0031A91B  mov      ebx, ecx
0031A91D  call     0x469c00  ; -> 00469C00 fn
0031A922  or       dword ptr [rip + 0x1fa8824], ebx  ; -> 022C314C
0031A928  add      rsp, 0x20
0031A92C  pop      rbx
0031A92D  ret      
```
