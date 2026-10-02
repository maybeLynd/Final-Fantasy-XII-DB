# F-interior pack: `02-Resource-And-Asset-Pipeline/CONTRACT-resource-entry-tree.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/contract-resource-entry-tree.json`.

Functions: 5. Each is cited on the page only at its entry and is still in the F frontier.

## 00369C60 (133 B, extent 00369C60-00369CE5)

Page context: " The original mover frees the old block, copies the allocation bytes into the selected free region, reissues its header, updates the existing slot/generation and reinserts its membership. The public '00369C60(arena, 0)' can move twice: one exact pass plus one adjacent/search pass. Arena+0x62 records successful compaction until its explicit clear, not completion of all pointer repair.  [Producer/consumer specification](the-source-block-m"

```
00369C60  push     rsi
00369C62  sub      rsp, 0x20
00369C66  mov      eax, dword ptr [rip + 0x1f6ed4c]  ; -> 022D89B8
00369C6C  mov      esi, edx
00369C6E  bt       eax, ecx
00369C71  jb       0x369c7b  ; -> 00369C7B
00369C73  xor      eax, eax
00369C75  add      rsp, 0x20
00369C79  pop      rsi
00369C7A  ret      
00369C7B  mov      qword ptr [rsp + 0x30], rbx
00369C80  xor      ebx, ebx
00369C82  mov      qword ptr [rsp + 0x38], rdi
00369C87  cmp      ecx, 0xe
00369C8A  ja       0x369ca2  ; -> 00369CA2
00369C8C  movsxd   rax, ecx
00369C8F  imul     rdi, rax, 0xa8
00369C96  lea      rax, [rip + 0x1f6e333]  ; -> 022D7FD0
00369C9D  add      rdi, rax
00369CA0  jmp      0x369ca5  ; -> 00369CA5
00369CA2  mov      rdi, rbx
00369CA5  cmp      qword ptr [rdi + 0x50], rbx
00369CA9  je       0x369cd3  ; -> 00369CD3
00369CAB  mov      rcx, rdi
00369CAE  call     0x36aad0  ; -> 0036AAD0 fn
00369CB3  mov      ebx, eax
00369CB5  mov      rcx, rdi
00369CB8  call     0x36abe0  ; -> 0036ABE0 fn
00369CBD  test     eax, eax
00369CBF  je       0x369cc7  ; -> 00369CC7
00369CC1  inc      ebx
00369CC3  test     esi, esi
00369CC5  jne      0x369cb5  ; -> 00369CB5
00369CC7  test     ebx, ebx
00369CC9  je       0x369cd3  ; -> 00369CD3
00369CCB  mov      byte ptr [rdi + 2], 1
00369CCF  mov      byte ptr [rdi + 0x62], 1
00369CD3  mov      rdi, qword ptr [rsp + 0x38]
00369CD8  mov      eax, ebx
00369CDA  mov      rbx, qword ptr [rsp + 0x30]
00369CDF  add      rsp, 0x20
00369CE3  pop      rsi
00369CE4  ret      
```

## 0036B490 (71 B, extent 0036B490-0036B4D7)

Page context: "t's matching   child slot ('+0x24' or '+0x28', chosen by which one resolves to the node) is rewritten to   'right', and '+0x3E' is cleared on **both** 'right' and 'parent'. Non-root without right:   '0036B490(parent, left, 0x4DF)' when the node was the parent's '+0x24', else   '0036B5A0(parent, left, 0x4E3)' — the left subtree is spliced straight into the vacated slot.   So "promotes the right child and reinserts the left" is exact; EXP"

```
0036B490  mov      qword ptr [rsp + 8], rbx
0036B495  mov      qword ptr [rsp + 0x10], rsi
0036B49A  push     rdi
0036B49B  sub      rsp, 0x20
0036B49F  xor      esi, esi
0036B4A1  mov      rbx, rdx
0036B4A4  mov      rdi, rcx
0036B4A7  test     rdx, rdx
0036B4AA  je       0x36b4b8  ; -> 0036B4B8
0036B4AC  call     0x20e620  ; -> 0020E620 fn
0036B4B1  mov      dword ptr [rbx + 0x2c], eax
0036B4B4  mov      word ptr [rbx + 0x3e], si
0036B4B8  mov      rcx, rbx
0036B4BB  call     0x20e620  ; -> 0020E620 fn
0036B4C0  mov      rbx, qword ptr [rsp + 0x30]
0036B4C5  mov      word ptr [rdi + 0x3e], si
0036B4C9  mov      rsi, qword ptr [rsp + 0x38]
0036B4CE  mov      dword ptr [rdi + 0x24], eax
0036B4D1  add      rsp, 0x20
0036B4D5  pop      rdi
0036B4D6  ret      
```

## 0036B5A0 (71 B, extent 0036B5A0-0036B5E7)

Page context: "the node) is rewritten to   'right', and '+0x3E' is cleared on **both** 'right' and 'parent'. Non-root without right:   '0036B490(parent, left, 0x4DF)' when the node was the parent's '+0x24', else   '0036B5A0(parent, left, 0x4E3)' — the left subtree is spliced straight into the vacated slot.   So "promotes the right child and reinserts the left" is exact; EXP-083's execution and the   static body now agree. - ~~**The standalone tree hel"

```
0036B5A0  mov      qword ptr [rsp + 8], rbx
0036B5A5  mov      qword ptr [rsp + 0x10], rsi
0036B5AA  push     rdi
0036B5AB  sub      rsp, 0x20
0036B5AF  xor      esi, esi
0036B5B1  mov      rbx, rdx
0036B5B4  mov      rdi, rcx
0036B5B7  test     rdx, rdx
0036B5BA  je       0x36b5c8  ; -> 0036B5C8
0036B5BC  call     0x20e620  ; -> 0020E620 fn
0036B5C1  mov      dword ptr [rbx + 0x2c], eax
0036B5C4  mov      word ptr [rbx + 0x3e], si
0036B5C8  mov      rcx, rbx
0036B5CB  call     0x20e620  ; -> 0020E620 fn
0036B5D0  mov      rbx, qword ptr [rsp + 0x30]
0036B5D5  mov      word ptr [rdi + 0x3e], si
0036B5D9  mov      rsi, qword ptr [rsp + 0x38]
0036B5DE  mov      dword ptr [rdi + 0x28], eax
0036B5E1  add      rsp, 0x20
0036B5E5  pop      rdi
0036B5E6  ret      
```

## 003AB940 (30 B, extent 003AB940-003AB95E)

Page context: "LLY UNDERSTOOD confidence: PROVEN implements: 02-Resource-And-Asset-Pipeline/authored-reference-lifetime-evidence.md entries: ["0036B4E0", "0036B410", "0036C790", "0036A000", "0036D170", "003AB880", "003AB940"] verified_against:   exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8   method: address-resolution verification 2026-09-14 (OPUS) - 31 addresses cited - 1 data, 9 entry, 21 interior, every one resolving"

```
003AB940  test     rcx, rcx
003AB943  je       0x3ab95d  ; -> 003AB95D
003AB945  test     cl, 3
003AB948  mov      edx, 0
003AB94D  setne    dl
003AB950  test     edx, edx
003AB952  je       0x3ab95d  ; -> 003AB95D
003AB954  cmp      edx, 1
003AB957  je       0x36d170  ; -> 0036D170 fn
003AB95D  ret      
```

## 00409730 (71 B, extent 00409730-00409777)

Page context: "bytes beyond the parsed payload. - **The release chain above this level — bounded SECTION-06 evidence now exists.** The matched   '00409D60' → '003B37E0(entry+0x44)' → '0024F4D0'/'0024F410', per-row '00409730', and   original allocation-release path execute in the new fixture. '00409CA0', all specialized children,   real movement/IO timing and whole-game reference lifetime are not thereby validated. See the   SECTION-06 production secti"

```
00409730  mov      qword ptr [rsp + 8], rbx
00409735  push     rdi
00409736  sub      rsp, 0x20
0040973A  mov      rdi, rcx
0040973D  mov      rcx, qword ptr [rcx + 0x30]
00409741  call     0x427b00  ; -> 00427B00 fn
00409746  lea      rcx, [rdi + 0x10]
0040974A  call     0x51ee80  ; -> 0051EE80 fn
0040974F  or       ecx, 0xffffffff
00409752  xor      eax, eax
00409754  mov      word ptr [rdi], cx
00409757  mov      dword ptr [rdi + 0x44], ecx
0040975A  lea      rcx, [rdi + 0x10]
0040975E  mov      dword ptr [rdi + 4], eax
00409761  mov      qword ptr [rdi + 0x30], rax
00409765  mov      dword ptr [rdi + 0x40], eax
00409768  mov      rbx, qword ptr [rsp + 0x30]
0040976D  add      rsp, 0x20
00409771  pop      rdi
00409772  jmp      0x51ee10  ; -> 0051EE10 fn
```
