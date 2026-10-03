# Homing pack: `19-Save-Load-Settings/Game-Settings-Config/CONTRACT-game-setting-config.md`

Generated 2026-10-03 12:43 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h12-contract-game-setting-config.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001DD050 (14 B, extent 001DD050-001DD05E)

Entered from (direct sites whose caller this page cites): `0017E070` + 0x4D (jmp; `0017E070` is cited on this page)
Other direct sites: none

Host context: "efs 01F82D20')* (RIP-relative instrument).  ## 6. Relationships  '00808D78' → '007A3770' → '007980A0' → { '001DE050', '001DED50' } → { '001DE5D0' parse | '001DF240' + '001DFD40' create }. Consumers: '0017E070' is the Config screen's per-row reader — a **23-arm jump table returning one value**, covering **16 distinct settings across all arms** (corrected 2026-09-08; it was described here as reading 16 settings in one pass, which the coun"

```
001DD050  cmp      dword ptr [rcx + 0x18], 0
001DD054  jne      0x1dd05a  ; -> 001DD05A
001DD056  mov      eax, dword ptr [rcx + 0x38]
001DD059  ret      
001DD05A  mov      eax, dword ptr [rcx + 0x24]
001DD05D  ret      
```
