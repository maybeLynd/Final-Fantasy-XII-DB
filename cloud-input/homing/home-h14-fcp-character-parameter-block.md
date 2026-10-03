# Homing pack: `17-Presentation-Rendering/Model-And-Motion-Formats/fcp-character-parameter-block.md`

Generated 2026-10-03 15:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h14-fcp-character-parameter-block.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0046C1E0 (91 B, extent 0046C1E0-0046C23B)

Entered from (direct sites whose caller this page cites): `0041FCF0` + 0x367 (call; `0041FCF0` is cited on this page)
Other direct sites: none

Host context: "tching byte selects animation '[record + 0x2FA] + i' of the model container's own '@FMC' motion entry ('+0x2F8' = the model resource id '+0x408', '+0x2FA' = its first '@FMC' entry index, both set by '0041FCF0' at '0041FE66'–'0041FE97') and starts it through '00423B10' ('0042933F'–'0042936E'); no match → the raw event id is the selector into the loaded motion resource at '+0x390' ('00429395'–'004293B5') | '0x7F' or an empty map → no entr"

```
0046C1E0  push     rbx
0046C1E2  sub      rsp, 0x20
0046C1E6  mov      byte ptr [rcx], 0
0046C1E9  mov      rbx, rcx
0046C1EC  cmp      dx, -1
0046C1F0  je       0x46c235  ; -> 0046C235
0046C1F2  xor      ecx, ecx
0046C1F4  movsx    rax, dx
0046C1F8  imul     rax, rax, 0x740
0046C1FF  add      rax, qword ptr [rip + 0x1e5ad22]  ; -> 022C6F28
0046C206  cmp      dword ptr [rax + 0x284], ecx
0046C20C  cmove    rax, rcx
0046C210  test     rax, rax
0046C213  je       0x46c235  ; -> 0046C235
0046C215  mov      byte ptr [rbx], 1
0046C218  mov      ecx, 9
0046C21D  mov      dword ptr [rbx + 8], edx
0046C220  mov      rax, qword ptr [rax + 0x108]
0046C227  mov      qword ptr [rbx + 0x10], rax
0046C22B  call     0x3a6e60  ; -> 003A6E60 fn
0046C230  add      al, 3
0046C232  mov      byte ptr [rbx + 4], al
0046C235  add      rsp, 0x20
0046C239  pop      rbx
0046C23A  ret      
```
