# Homing pack: `16-UI/Config-Screen/the-config-screen-and-what-a-setting-change-runs.md`

Generated 2026-10-03 12:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h11-the-config-screen-and-what-a-setting-change-runs.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001DD050 (14 B, extent 001DD050-001DD05E)

Entered from (direct sites whose caller this page cites): `0017E070` + 0x4D (jmp; `0017E070` is cited on this page)
Other direct sites: none

Host context: "anager, direction, propertyId) 0017DD39   call 0016D6A0()                 ; unread   <- corrected 2026-10-02, OPUS - 0016D6A0 is ret 0, the stub /OPT:ICF folded empty functions onto 0017DD40   return 0017E070(row)            ; read the value back out of the config '''  ''' 001CD040  test dl,dl / mov r9d,r8d / sete r8b / jmp 001D1660   ; 14 B, direction in both polarities    001D1660   282-id dispatcher, 226 arms       001D5120   graphic"

```
001DD050  cmp      dword ptr [rcx + 0x18], 0
001DD054  jne      0x1dd05a  ; -> 001DD05A
001DD056  mov      eax, dword ptr [rcx + 0x38]
001DD059  ret      
001DD05A  mov      eax, dword ptr [rcx + 0x24]
001DD05D  ret      
```
