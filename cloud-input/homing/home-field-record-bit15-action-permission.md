# Homing pack: `03-World-Area-Field/Field-Record-Table/field-record-bit15-action-permission.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-field-record-bit15-action-permission.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0031E860 (31 B, extent 0031E860-0031E87F)

Entered from (direct sites whose caller this page cites): `00313DB0` + 0xB3 (call; `00313DB0` is cited on this page)
Other direct sites: `00303E90` + 0x15 (jmp); `00313590` + 0x15 (jmp)

Host context: "red machinery across the layer boundary, no shared ownership. - **CombatAction - CLIENT (25 edges).** '0030D9A0', '00313A00', '00313F60' are also called by bodies filed to combat action: '002FFCF0', '00313DB0', '00319F50' - shared machinery across the layer boundary, no shared ownership. - **CombatFormula - CLIENT (2 edges).** '00313F60', '00377C20' are also called by bodies filed to combat formula: '00384F40', '00300530' - shared machi"

```
0031E860  sub      rsp, 0x28
0031E864  call     0x263750  ; -> 00263750 fn
0031E869  test     rax, rax
0031E86C  jne      0x31e873  ; -> 0031E873
0031E86E  add      rsp, 0x28
0031E872  ret      
0031E873  mov      rcx, rax
0031E876  add      rsp, 0x28
0031E87A  jmp      0x3589b0  ; -> 003589B0 fn
```
