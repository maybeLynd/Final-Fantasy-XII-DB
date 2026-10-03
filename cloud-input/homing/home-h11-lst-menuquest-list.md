# Homing pack: `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/lst-menuquest-list.md`

Generated 2026-10-03 12:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h11-lst-menuquest-list.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0037FA00 (116 B, extent 0037FA00-0037FA74)

Entered from (direct sites whose caller this page cites): `0037F4D0` + 0x47 (call; `0037F4D0` is cited on this page)
Other direct sites: none

Host context: "rectory arithmetic verified on all 9" archive_formats:   - "lst | explained | qstl quest-list string index — sparse u16 id -> variable-length encoded-string blob; requested at 0037F76F by widget proc 0037F4D0." last_reviewed: 2026-09-30 audit:   passes: 1   last_pass: 2026-09-17   last_pass_state: falsification-pass   crossref_clean: false   reopened_count: 0 ---  # The 'qstl' quest-list string index — 'quest/menuquest.lst'  > **The que"

```
0037FA00  mov      qword ptr [rsp + 0x10], rsi
0037FA05  push     rdi
0037FA06  sub      rsp, 0x20
0037FA0A  mov      rsi, rcx
0037FA0D  xor      edi, edi
0037FA0F  mov      rcx, qword ptr [rcx + 0xc8]
0037FA16  test     rcx, rcx
0037FA19  je       0x37fa27  ; -> 0037FA27
0037FA1B  call     0x3697f0  ; -> 003697F0 fn
0037FA20  mov      qword ptr [rsi + 0xc8], rdi
0037FA27  movzx    eax, byte ptr [rsi + 0xee]
0037FA2E  test     al, al
0037FA30  je       0x37fa69  ; -> 0037FA69
0037FA32  mov      qword ptr [rsp + 0x30], rbx
0037FA37  lea      rbx, [rsi + 0xf0]
0037FA3E  nop      
0037FA40  mov      rcx, qword ptr [rbx + 0x10]
0037FA44  call     0x3697f0  ; -> 003697F0 fn
0037FA49  mov      byte ptr [rbx], 0
0037FA4C  lea      rbx, [rbx + 0x18]
0037FA50  movzx    eax, byte ptr [rsi + 0xee]
0037FA57  inc      edi
0037FA59  cmp      edi, eax
0037FA5B  jl       0x37fa40  ; -> 0037FA40
0037FA5D  mov      rbx, qword ptr [rsp + 0x30]
0037FA62  mov      byte ptr [rsi + 0xee], 0
0037FA69  mov      rsi, qword ptr [rsp + 0x38]
0037FA6E  add      rsp, 0x20
0037FA72  pop      rdi
0037FA73  ret      
```
