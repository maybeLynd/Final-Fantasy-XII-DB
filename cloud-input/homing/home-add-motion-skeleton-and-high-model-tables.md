# Homing pack: `17-Presentation-Rendering/Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-add-motion-skeleton-and-high-model-tables.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0051B120 (45 B, extent 0051B120-0051B14D)

Entered from (direct sites whose caller this page cites): `003E1C50` + 0x818 (call; `003E1C50` is cited on this page)
Other direct sites: none

Host context: "'; when 'word[+0x16] != -1' the '[+0x18]' handle chains '00409F50' + '004096C0' into '+0xA0'/'+0x94', and the '+0x90'-gated tail rebases '+0x84'/'+0x94' by the resolved bases then hands the block to '003E1C50' - the bind pass the motion-table and ramp-channel callers share.  Interior anchor '0037140A' (function '003713C0').  '00520010' (228 B) is the chunked-list walk: '[rcx+0x40]' holds the chain head, each id 'i' rebases '[+0x30]' thr"

```
0051B120  mov      qword ptr [rsp + 8], rbx
0051B125  push     rdi
0051B126  sub      rsp, 0x20
0051B12A  mov      rdi, rcx
0051B12D  mov      ebx, edx
0051B12F  mov      ecx, dword ptr [rcx + 0x10]
0051B132  call     0x20e600  ; -> 0020E600 fn
0051B137  lea      ecx, [rbx + rax]
0051B13A  call     0x20e620  ; -> 0020E620 fn
0051B13F  mov      rbx, qword ptr [rsp + 0x30]
0051B144  mov      dword ptr [rdi + 0x10], eax
0051B147  add      rsp, 0x20
0051B14B  pop      rdi
0051B14C  ret      
```
