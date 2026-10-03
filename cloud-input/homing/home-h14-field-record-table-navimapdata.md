# Homing pack: `03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md`

Generated 2026-10-03 15:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h14-field-record-table-navimapdata.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 003C9900 (66 B, extent 003C9900-003C9942)

Entered from (direct sites whose caller this page cites): `00255330` + 0x41 (call; `00255330` is cited on this page)
Other direct sites: `00251F40` + 0xD1 (call); `00254AC0` + 0x45 (call)

Host context: "erior anchors '002543E9' / '00254399' (the '+1+ecx' byte loads).  ## SWE2-EC7-102 update (2026-09-20) - '0028FF20' measured  '0028FF20' (81 B) is the conditional word-publish '00251F40', '00254AC0', '00255330' and '003C5E50' call on the '[0209BE80 + 0x10F80]' object: when the slot is nonnull '002544B0()' runs; a return of 1 zeroes 'word[+0x1D78]', and 'word[+0x1D7A]' always gains bit 3 - the clear-and-arm sequence the navimap paths post"

```
003C9900  sub      rsp, 0x28
003C9904  cmp      qword ptr [rip + 0x277de34], 0  ; -> 02B47740
003C990C  je       0x3c993d  ; -> 003C993D
003C990E  call     0x2544b0  ; -> 002544B0 fn
003C9913  mov      rcx, qword ptr [rip + 0x277de26]  ; -> 02B47740
003C991A  xor      edx, edx
003C991C  cmp      eax, 1
003C991F  sete     dl
003C9922  test     rcx, rcx
003C9925  je       0x3c9934  ; -> 003C9934
003C9927  and      dword ptr [rcx + 0x40], 0xfffeffff
003C992E  shl      edx, 0x10
003C9931  or       dword ptr [rcx + 0x40], edx
003C9934  add      rsp, 0x28
003C9938  jmp      0x244dd0  ; -> 00244DD0 fn
003C993D  add      rsp, 0x28
003C9941  ret      
```
