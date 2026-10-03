# Homing pack: `00-Engine-Core-Runtime/Developer-Tuning-Console/console-command-names.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-console-command-names.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001C0400 (60 B, extent 001C0400-001C043C)

Entered from (direct sites whose caller this page cites): `001CD0E0` + 0x8B8 (call; `001CD0E0` is cited on this page)
Other direct sites: none

Host context: " nine arm-catalogue slices. Regenerate rather than patch.  Every command the developer console exposes, with the name the engine itself prints for it.  ## Where the names come from  The row renderer '001CD0E0' prints '"%s%s%f"' with the label fetched from '[ctx + id*8 + 0x130]', so  ''' id = (displacement - 0x130) / 8 '''  **293 labels, ids 1-294, zero collisions, all 282 action ids covered.** Id 294 — *"Key Kana Test"* — is a **render "

```
001C0400  mov      rdx, qword ptr [rcx + 0x60]
001C0404  movabs   rax, 0x6666666666666667
001C040E  sub      rdx, qword ptr [rcx + 0x58]
001C0412  imul     rdx
001C0415  sar      rdx, 4
001C0419  mov      rax, rdx
001C041C  shr      rax, 0x3f
001C0420  add      rdx, rax
001C0423  test     edx, edx
001C0425  je       0x1c0436  ; -> 001C0436
001C0427  cmp      qword ptr [rcx + 0x10], 0
001C042C  je       0x1c0436  ; -> 001C0436
001C042E  mov      rax, qword ptr [rcx + 0x18]
001C0432  mov      eax, dword ptr [rax + 0x38]
001C0435  ret      
001C0436  mov      eax, 1
001C043B  ret      
```
