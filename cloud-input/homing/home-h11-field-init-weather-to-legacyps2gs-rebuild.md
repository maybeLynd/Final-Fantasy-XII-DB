# Homing pack: `03-World-Area-Field/Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md`

Generated 2026-10-03 12:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h11-field-init-weather-to-legacyps2gs-rebuild.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 003ED7B0 (54 B, extent 003ED7B0-003ED7E6)

Entered from (direct sites whose caller this page cites): `0026E8D0` + 0x81 (jmp; `0026E8D0` is cited on this page)
Other direct sites: none

Host context: "                    |-> 00379860(weatherSlot)                        v [WorldAreaField]     00379290  field-resource bridge                        |         if area runtime exists: 02ADD0E9 = 1, tail 0026E8D0(slot)                        |         else:                   02ADD0E9 = 0, tail 00379630                        v [Movement]           0026E8D0  resource-bank reconfiguration     [AUTHORITY 03 -> 06]                        |-> se"

```
003ED7B0  mov      rdx, qword ptr [rip + 0x2ace039]  ; -> 02EBB7F0
003ED7B7  test     rdx, rdx
003ED7BA  je       0x3ed7e5  ; -> 003ED7E5
003ED7BC  movsxd   rax, ecx
003ED7BF  lea      rcx, [rax + rax*2]
003ED7C3  shl      rcx, 7
003ED7C7  mov      eax, dword ptr [rcx + rdx + 0x10]
003ED7CB  mov      dword ptr [rip + 0x2ace027], eax  ; -> 02EBB7F8
003ED7D1  mov      eax, dword ptr [rcx + rdx + 0x14]
003ED7D5  mov      dword ptr [rip + 0x2ace021], eax  ; -> 02EBB7FC
003ED7DB  mov      eax, dword ptr [rcx + rdx + 0x1c]
003ED7DF  mov      dword ptr [rip + 0x2ace01f], eax  ; -> 02EBB804
003ED7E5  ret      
```
