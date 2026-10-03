# Homing pack: `08-Combat-Formula/Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md`

Generated 2026-10-03 00:35 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-weather-terrain-element-scaling.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00259B10 (21 B, extent 00259B10-00259B25)

Entered from (direct sites whose caller this page cites): `00336E40` + 0x241 (call; `00336E40` is cited on this page)
Other direct sites: none

Host context: "r that runs this page's scaling step, so the action layer is how the weather and terrain multipliers reach a hit.  **Movement — OUT-OF-SCOPE (2 edges).** '00336AE0' calls '00380C40' and is called by '00336E40'. This page cites '00336AE0' only as one of the eight '0.6f' load sites in the falsification table; its movement edges have nothing to do with element scaling.  **Presentation — OUT-OF-SCOPE (4 edges).** '001DC4C0' is called by '00"

```
00259B10  movsxd   rax, ecx
00259B13  lea      rcx, [rip + 0x1e3d806]  ; -> 02097320
00259B1A  imul     rax, rax, 0x110
00259B21  add      rax, rcx
00259B24  ret      
```
