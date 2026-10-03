# Homing pack: `11-Party/active-party-reserve-and-the-moment-the-leader-changes.md`

Generated 2026-10-02 22:54 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-active-party-reserve-and-the-moment-the-leader-changes.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0036F510 (18 B, extent 0036F510-0036F522)

Entered from (direct sites whose caller this page cites): `0022A770` + 0x12F (call; `0022A770` is cited on this page); `0022A770` + 0x1DD (call; `0022A770` is cited on this page); `0022A770` + 0x4DB (call; `0022A770` is cited on this page); `0022A770` + 0x666 (call; `0022A770` is cited on this page); `0022B8C0` + 0x1BC (call; `0022B8C0` is cited on this page); `0022B8C0` + 0x1F2 (call; `0022B8C0` is cited on this page)
Other direct sites: none

Host context: "thunk '00358BB0' ('jmp 00358BC0'), and that thunk is called from seven sites and referenced by nothing else (no 'lea', no data pointer). Three are the per-mode frame bodies, one call each per frame: '0022A770' ('0022AE3C'), 'MainLoop_UpdateAndRenderFrame' '0022B8C0' ('0022BAF9') and '0022BC20' ('0022BD49'), all three dispatched from '0022A580'; so "later" is the same frame's commit point, once a frame. The other four are the actor syste" / "thunk '00358BB0' ('jmp 00358BC0'), and that thunk is called from seven sites and referenced by nothing else (no 'lea', no data pointer). Three are the per-mode frame bodies, one call each per frame: '0022A770' ('0022AE3C'), 'MainLoop_UpdateAndRenderFrame' '0022B8C0' ('0022BAF9') and '0022BC20' ('0022BD49'), all three dispatched from '0022A580'; so "later" is the same frame's commit point, once a frame. The other four are the actor syste"

```
0036F510  sub      rsp, 0x28
0036F514  call     0x3820c0  ; -> 003820C0 fn
0036F519  add      rsp, 0x28
0036F51D  jmp      0x26eb30  ; -> 0026EB30 fn
```
