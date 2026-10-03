# Homing pack: `99-Unresolved-Residual/Glyph-Run-Rendering/the-font-painters-public-api.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-font-painters-public-api.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001E9380 (51 B, extent 001E9380-001E93B3)

Entered from (direct sites whose caller this page cites): `0017FC50` + 0x10 (jmp; `0017FC50` is cited on this page)
Other direct sites: none

Host context: "at draws text goes through ~~eighteen~~ twenty-one entry points** *(corrected 2026-10-02, OPUS: a rel32 sweep finds 25 call sites of '001B5FA0' in 23 functions: 21 in the band, including '0017FC00', '0017FC50' and '0017FC70', which §2's table lacks, and the two consumers)*, and they were found by one mechanical test rather than by judgement: **'001B5FA0' is the one-line accessor that returns the font painter singleton 'DAT_01F811F8', so"

```
001E9380  mov      qword ptr [rsp + 8], rbx
001E9385  push     rdi
001E9386  sub      rsp, 0x20
001E938A  lea      rbx, [rcx + 0x1500]
001E9391  mov      edi, 0x40
001E9396  mov      rcx, rbx
001E9399  call     0x213090  ; -> 00213090 fn
001E939E  add      rbx, 0x38
001E93A2  sub      rdi, 1
001E93A6  jne      0x1e9396  ; -> 001E9396
001E93A8  mov      rbx, qword ptr [rsp + 0x30]
001E93AD  add      rsp, 0x20
001E93B1  pop      rdi
001E93B2  ret      
```
