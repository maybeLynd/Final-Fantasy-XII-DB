# F-interior pack: `17-Presentation-Rendering/Model-And-Motion-Formats/adm-add-motion-tables.md`

Generated 2026-10-02 18:41 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/adm-add-motion-tables.json`.

Functions: 2. Each is cited on the page only at its entry and is still in the F frontier.

## 00183240 (32 B, extent 00183240-00183260)

Page context: "'s review): the parsed-'.adm' registry singleton '0x1F81250' is touched by exactly two functions — its installer '001BE3E0' and the getter '001BE420' — and the getter's five callers are '0017FFB0' / '00183240' / '001CD0E0' / '001D1660', which read or write only the registry's own '+0x20' flag dword, and '00863110', which performs the name lookup. 'AddMotion_LookupByModelName' ('001BE430') has exactly one inbound reference under all four"

```
00183240  push     rbx
00183242  sub      rsp, 0x20
00183246  mov      ebx, ecx
00183248  call     0x1be420  ; -> 001BE420 fn
0018324D  test     rax, rax
00183250  je       0x18325a  ; -> 0018325A
00183252  call     0x1be420  ; -> 001BE420 fn
00183257  mov      dword ptr [rax + 0x20], ebx
0018325A  add      rsp, 0x20
0018325E  pop      rbx
0018325F  ret      
```

## 00351F40 (65 B, extent 00351F40-00351F81)

Page context: "tail '004FE2F0(resolved, edx)' runs the forward. Interior anchor '003E6332' (the '004FE2F0' tail).  ## SWE2-EC7-104 update (2026-09-20) - '002647C0' measured  '002647C0' (9 B) is the range predicate '00351F40', '00352FA0', '003537D0', '0037B4D0' and '0050C610' call: 'return ecx <= 3' - the four-slot bound check shared across the motion-table arms and the script bridge. Interior anchor '002647C2' (the 'cmp ecx, 3').  ## SWE2-EC7-105 upda"

```
00351F40  mov      qword ptr [rsp + 8], rbx
00351F45  push     rdi
00351F46  sub      rsp, 0x20
00351F4A  mov      rcx, r9
00351F4D  mov      rbx, r8
00351F50  mov      rdi, rdx
00351F53  call     0x267e10  ; -> 00267E10 fn
00351F58  mov      ecx, eax
00351F5A  mov      byte ptr [rbx + 0xd], al
00351F5D  call     0x2647c0  ; -> 002647C0 fn
00351F62  test     eax, eax
00351F64  mov      edx, 0xb
00351F69  mov      rcx, rdi
00351F6C  setne    al
00351F6F  mov      byte ptr [rbx + 0xc], al
00351F72  mov      rbx, qword ptr [rsp + 0x30]
00351F77  add      rsp, 0x20
00351F7B  pop      rdi
00351F7C  jmp      0x26b4a0  ; -> 0026B4A0 fn
```
