# Homing pack: `00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-D-ids-108-139.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-arm-catalogue-slice-d-ids-108-139.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001A7990 (113 B, extent 001A7990-001A7A01)

Entered from (direct sites whose caller this page cites): `001BF8B0` + 0x199 (call; `001BF8B0` is cited on this page)
Other direct sites: none

Host context: "two accessors are also reached from **outside** the dispatch: nine Presentation-layer bodies call '00193D50' ('001CD0E0', '001C7940', '0018B1B0'…) and eleven call '001A9930' ('001CD0E0', '001C3D50', '001BF8B0'…), and '001D1660''s own callees include the Presentation-owned materializers '001D5120'/'001C7360'/'001C7520' — 23 edges in all. The arms and their accessors sit on the render path, not behind it. The catalogue's other crossings a"

```
001A7990  push     rbx
001A7992  sub      rsp, 0x20
001A7996  mov      rbx, rcx
001A7999  call     0x1a76d0  ; -> 001A76D0 fn
001A799E  mov      rdx, rax
001A79A1  test     rax, rax
001A79A4  jne      0x1a79ac  ; -> 001A79AC
001A79A6  add      rsp, 0x20
001A79AA  pop      rbx
001A79AB  ret      
001A79AC  mov      rax, qword ptr [rbx + 0x460]
001A79B3  lea      r8, [rbx + 0x450]
001A79BA  add      rbx, 0x450
001A79C1  mov      rcx, rbx
001A79C4  test     rax, rax
001A79C7  je       0x1a79e7  ; -> 001A79E7
001A79C9  nop      dword ptr [rax]
001A79D0  cmp      qword ptr [rax + 0x20], rdx
001A79D4  jb       0x1a79df  ; -> 001A79DF
001A79D6  mov      rcx, rax
001A79D9  mov      rax, qword ptr [rax + 8]
001A79DD  jmp      0x1a79e2  ; -> 001A79E2
001A79DF  mov      rax, qword ptr [rax]
001A79E2  test     rax, rax
001A79E5  jne      0x1a79d0  ; -> 001A79D0
001A79E7  cmp      rcx, rbx
001A79EA  je       0x1a79f2  ; -> 001A79F2
001A79EC  cmp      rdx, qword ptr [rcx + 0x20]
001A79F0  jae      0x1a79f5  ; -> 001A79F5
001A79F2  mov      rcx, rbx
001A79F5  cmp      rcx, r8
001A79F8  setne    al
001A79FB  add      rsp, 0x20
001A79FF  pop      rbx
001A7A00  ret      
```
