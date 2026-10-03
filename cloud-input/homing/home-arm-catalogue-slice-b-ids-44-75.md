# Homing pack: `00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-B-ids-44-75.md`

Generated 2026-10-02 22:54 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-arm-catalogue-slice-b-ids-44-75.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001FB830 (15 B, extent 001FB830-001FB83F)

Entered from (direct sites whose caller this page cites): `001F16C0` + 0x6E (jmp; `001F16C0` is cited on this page)
Other direct sites: none

Host context: "05CC930' is called by 'Application' '00799980' (1 edge) — same platform-leg shape as slice A.)*  ## SWE2-EC7-49 update (2026-09-19) - '00188DA0'  '00188DA0' (192 B) is a body - '00193D50'/'001EE180'/'001F16C0'/'00610330' plus a 'call [rax+0x10]' vcall. Interior anchor '00188DB4' (an '00193D50' call).  ## SWE2-EC7-49 update (2026-09-19) - '001A97F0'  '001A97F0' (190 B) is a body - '001867B0'/'00189120'/'001AC720'/'001AD440'. Interior anc"

```
001FB830  mov      rdx, qword ptr [rcx]
001FB833  mov      rcx, qword ptr [rip + 0x1d83c96]  ; -> 01F7F4D0
001FB83A  jmp      0x1a1850  ; -> 001A1850 fn
```
