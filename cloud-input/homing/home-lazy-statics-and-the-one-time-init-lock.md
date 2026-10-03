# Homing pack: `24-Compiler-And-CRT-Runtime/Lazy-Static-Initialization/lazy-statics-and-the-one-time-init-lock.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-lazy-statics-and-the-one-time-init-lock.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001D9F70 (23 B, extent 001D9F70-001D9F87)

Entered from (direct sites whose caller this page cites): `0017D940` + 0x17 (jmp; `0017D940` is cited on this page)
Other direct sites: none

Host context: "body - '005CDA30'/'0080929C'/'008092FC'. Interior anchor '008AADED' (a '005CDA30' call).   ## SWE2-EC7-64 update (2026-09-19) - '00212050'  '00212050' (138 B) is a '0021xxxx' lazy-init-family body - '0017D940'/'0017D960'/'00212260'/'002124C0'/'005CD4F0'/'005CD820' plus one vcall. Interior anchor '00212071' (a '0017D940' call).    ## SWE2-EC7-65 update (2026-09-19) - '00212260'  '00212260' (150 B) is a '0021xxxx' lazy-init-family sibling"

```
001D9F70  cmp      edx, 1
001D9F73  ja       0x1d9f86  ; -> 001D9F86
001D9F75  movsxd   rax, edx
001D9F78  lea      rcx, [rcx + rax*4]
001D9F7C  mov      eax, 1
001D9F81  lock xadd dword ptr [rcx + 0x24], eax
001D9F86  ret      
```
