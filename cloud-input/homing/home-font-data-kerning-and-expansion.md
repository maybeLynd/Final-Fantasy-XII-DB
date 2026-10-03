# Homing pack: `16-UI/Text-And-Number-Rendering/font-data-kerning-and-expansion.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-font-data-kerning-and-expansion.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001FDE60 (85 B, extent 001FDE60-001FDEB5)

Entered from (direct sites whose caller this page cites): `001B58E0` + 0x219 (call; `001B58E0` is cited on this page)
Other direct sites: `001B6110` + 0x24 (call)

Host context: "001B5480' (399 B) | the '.ker' / '.fex' requesters §3 describes — format '<dir><name>.<ext>' and queue the request with completion '001B6080' / '001B6030' | '001B5757' / '001B5487' | | font lookup | '001B58E0' (631 B) | ordered-tree walk of the font system's font-id map (head 'rcx+0x30', key 'node+0x20') — the "find the font by id" step both list readers open with | '001B5903' | | font build | '001FC060' (518 B) | the font constructor —"

```
001FDE60  mov      qword ptr [rsp + 8], rbx
001FDE65  push     rdi
001FDE66  sub      rsp, 0x30
001FDE6A  xor      eax, eax
001FDE6C  mov      rdi, rdx
001FDE6F  mov      qword ptr [rdx], rax
001FDE72  mov      rbx, rcx
001FDE75  mov      qword ptr [rdx + 8], rax
001FDE79  mov      qword ptr [rdx + 0x10], rax
001FDE7D  lea      rdx, [rcx + 0x118]
001FDE84  lea      rcx, [rdi + 0x18]
001FDE88  mov      dword ptr [rsp + 0x20], eax
001FDE8C  call     0x1edf00  ; -> 001EDF00 fn
001FDE91  mov      r8, qword ptr [rbx + 0x108]
001FDE98  mov      rcx, rdi
001FDE9B  mov      rdx, qword ptr [rbx + 0x100]
001FDEA2  call     0x1a4bf0  ; -> 001A4BF0 fn
001FDEA7  mov      rbx, qword ptr [rsp + 0x40]
001FDEAC  mov      rax, rdi
001FDEAF  add      rsp, 0x30
001FDEB3  pop      rdi
001FDEB4  ret      
```
