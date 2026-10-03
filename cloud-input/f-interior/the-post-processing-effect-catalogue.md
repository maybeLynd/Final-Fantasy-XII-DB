# F-interior pack: `17-Presentation-Rendering/Post-Processing/the-post-processing-effect-catalogue.md`

Generated 2026-10-02 20:18 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/the-post-processing-effect-catalogue.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

## 006CC2F0 (63 B, extent 006CC2F0-006CC32F)

Page context: "e '00193DA0' thunk family measured", has each forwarder's shape.  **The order, every frame:**  | step | when | call → library | what it passes | |---|---|---|---| | 1 | 'cfg+0x99' set | '0065E6C0' → '006CC2F0' | nothing from 'cfg': two virtual calls on the library object (slot 1, then slot 0); not named here | | 1′ | otherwise, library object absent ('0065E5B0' false) | '0065E5A0' → '006CBD20' | 'cfg[0]' and the context's first qword: t"

```
006CC2F0  push     rbx
006CC2F2  sub      rsp, 0x20
006CC2F6  mov      rbx, rcx
006CC2F9  mov      rcx, qword ptr [rcx]
006CC2FC  test     rcx, rcx
006CC2FF  je       0x6cc30e  ; -> 006CC30E
006CC301  mov      rax, qword ptr [rcx]
006CC304  call     qword ptr [rax + 8]
006CC307  mov      qword ptr [rbx], 0
006CC30E  mov      rcx, qword ptr [rbx + 8]
006CC312  test     rcx, rcx
006CC315  je       0x6cc329  ; -> 006CC329
006CC317  mov      rax, qword ptr [rcx]
006CC31A  mov      edx, 1
006CC31F  call     qword ptr [rax]
006CC321  mov      qword ptr [rbx + 8], 0
006CC329  add      rsp, 0x20
006CC32D  pop      rbx
006CC32E  ret      
```
