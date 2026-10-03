# Homing pack: `13-Rewards-Progression-Economy/gil-storage-clamp-and-every-path-that-moves-it.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-gil-storage-clamp-and-every-path-that-moves-it.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002BE290 (100 B, extent 002BE290-002BE2F4)

Entered from (direct sites whose caller this page cites): `002BE490` + 0x4B (call; `002BE490` is cited on this page)
Other direct sites: none

Host context: "0'/'002BE0A0'/'003FA760'), '00274840' ('002446E0'/'002473B0'/'002482E0'), '002A79E0' ('0209C510'), '002B3550' ('008620A0'/'00254A10'/'0024ABC0', '0209D490'), '002BE450' ('00245000'/'00246AC0', table '002BE490') | the second '0209BE80' accessor family in this census (the '002778C0' battle-menu subtree has its own band) — here serving the binder's UI-facing side | | '022Cxxxx'/'022CAxxx' cells | '0035C560' (68 B — '0028F8B0'/'00253480'/'0"

```
002BE290  push     rbx
002BE292  sub      rsp, 0x20
002BE296  test     byte ptr [rcx + 0x57e], 1
002BE29D  mov      rbx, rcx
002BE2A0  je       0x2be2b7  ; -> 002BE2B7
002BE2A2  call     0x2bea40  ; -> 002BEA40 fn
002BE2A7  test     rax, rax
002BE2AA  je       0x2be2b7  ; -> 002BE2B7
002BE2AC  mov      rdx, rax
002BE2AF  mov      rcx, rbx
002BE2B2  call     0x2c0f30  ; -> 002C0F30 fn
002BE2B7  mov      rcx, qword ptr [rbx + 0x570]
002BE2BE  test     rcx, rcx
002BE2C1  je       0x2be2ee  ; -> 002BE2EE
002BE2C3  movzx    eax, word ptr [rcx + 0x280]
002BE2CA  test     al, 1
002BE2CC  jne      0x2be2ee  ; -> 002BE2EE
002BE2CE  test     al, 4
002BE2D0  je       0x2be2ee  ; -> 002BE2EE
002BE2D2  call     0x244f00  ; -> 00244F00 fn
002BE2D7  mov      eax, 0xfffd
002BE2DC  mov      qword ptr [rbx + 0x570], 0
002BE2E7  and      word ptr [rbx + 0x57e], ax
002BE2EE  add      rsp, 0x20
002BE2F2  pop      rbx
002BE2F3  ret      
```
