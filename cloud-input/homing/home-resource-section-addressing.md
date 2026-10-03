# Homing pack: `02-Resource-And-Asset-Pipeline/resource-section-addressing.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-resource-section-addressing.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0046C1E0 (91 B, extent 0046C1E0-0046C23B)

Entered from (direct sites whose caller this page cites): `0041FCF0` + 0x367 (call; `0041FCF0` is cited on this page)
Other direct sites: none

Host context: " 17 call sites in 11 functions, not nine* below; 2026-10-02, OPUS)* that > call '004096C0' - 'PresentationEntry_RebuildDerivedReferences' '0041CA70' four times, '00372820', > '0041B4E0', '00504940', '0041FCF0', '0042A390' and two more - have no declared type to disagree > with. **ASTRA asked whether the structured consumers preserve the width. There are none.**  **Why it is not declared here and now:** the entry's **extent is not establ"

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

## 00512C50 (45 B, extent 00512C50-00512C7D)

Entered from (direct sites whose caller this page cites): `003E1C50` + 0x717 (call; `003E1C50` is cited on this page)
Other direct sites: none

Host context: "0' and clears '+0xF0'/'+0x68'/'+0xE0'/'+0xD8'/'+0xF8'; '+0x42C'/'+0x430' re-register through '0020E620' whenever their resolve comes back null. Interior anchor '0042DA78' (the '00409660' tag find).  '003E1C50' (2992 B) is the record walk '003713C0' runs: null 'rcx' bails whole, '0020E600([rcx+0x70])' resolves, 'word[+0x68] = -1' folds to 0, then a 137-call '0020E600' + 95-call '0020E620' walk over the section's records with '0051B850', "

```
00512C50  mov      qword ptr [rsp + 8], rbx
00512C55  push     rdi
00512C56  sub      rsp, 0x20
00512C5A  mov      rdi, rcx
00512C5D  mov      ebx, edx
00512C5F  mov      ecx, dword ptr [rcx + 0x30]
00512C62  call     0x20e600  ; -> 0020E600 fn
00512C67  lea      ecx, [rbx + rax]
00512C6A  call     0x20e620  ; -> 0020E620 fn
00512C6F  mov      rbx, qword ptr [rsp + 0x30]
00512C74  mov      dword ptr [rdi + 0x30], eax
00512C77  add      rsp, 0x20
00512C7B  pop      rdi
00512C7C  ret      
```
