# Homing pack: `02-Resource-And-Asset-Pipeline/the-external-source-owner-and-borrowed-view-lifetime.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-external-source-owner-and-borrowed-view-lifetime.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 003AED50 (23 B, extent 003AED50-003AED67)

Entered from (direct sites whose caller this page cites): `0041FCF0` + 0x210 (call; `0041FCF0` is cited on this page)
Other direct sites: none

Host context: "ller had pinned it before setup. Mode1 setup merely retains the representation and does not pin. This pair cannot be treated as independently nestable retain/release calls.  The complete static body '0041FCF0' calls the view at '0041FFA0', uses the returned value while performing its consumer work, and ends that entry's view at '0041FFF8'. The consumer itself and its callbacks are not executed here, so no assertion is made that all desc"

```
003AED50  xor      eax, eax
003AED52  mov      dword ptr [rcx], 1
003AED58  mov      qword ptr [rcx + 0x18], rax
003AED5C  mov      qword ptr [rcx + 0x20], rax
003AED60  mov      dword ptr [rcx + 0x28], eax
003AED63  mov      dword ptr [rcx + 4], edx
003AED66  ret      
```
