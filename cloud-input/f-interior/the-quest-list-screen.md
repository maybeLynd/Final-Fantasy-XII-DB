# F-interior pack: `16-UI/Quest-List/the-quest-list-screen.md`

Generated 2026-10-02 18:41 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/the-quest-list-screen.json`.

Functions: 4. Each is cited on the page only at its entry and is still in the F frontier.

## 001B6430 (61 B, extent 001B6430-001B646D)

Page context: "0017FB70', '0017FBC0', '0017FBE0' | CRT tail-call forwarders — already in '24-Compiler-And-CRT-Runtime/Generated-Families/members/nativeadapter-*tailcall.tsv' | | '001B47A0', '001B5330', '001B6350', '001B6430', '001B6510' | the text-object cache — a vector at '+0x250'/'+0x258' of '{ptr}' entries keyed by '{id=+4, kind=+0x10}'; '001B6350' finds-or-allocs ('001BA860' + '00674A00'), '001B47A0' finds-and-assigns, '001B5330' releases, '001B6"

```
001B6430  mov      rax, qword ptr [rcx + 0x250]
001B6437  mov      r9, qword ptr [rcx + 0x258]
001B643E  cmp      rax, r9
001B6441  je       0x1b6461  ; -> 001B6461
001B6443  mov      r8, qword ptr [rax]
001B6446  cmp      dword ptr [r8 + 4], edx
001B644A  jne      0x1b6453  ; -> 001B6453
001B644C  cmp      byte ptr [r8 + 0x10], 0
001B6451  jne      0x1b6459  ; -> 001B6459
001B6453  add      rax, 8
001B6457  jmp      0x1b643e  ; -> 001B643E
001B6459  mov      qword ptr [rcx + 0x270], r8
001B6460  ret      
001B6461  mov      qword ptr [rcx + 0x270], 0
001B646C  ret      
```

## 001B6510 (80 B, extent 001B6510-001B6560)

Page context: "0017FBC0', '0017FBE0' | CRT tail-call forwarders — already in '24-Compiler-And-CRT-Runtime/Generated-Families/members/nativeadapter-*tailcall.tsv' | | '001B47A0', '001B5330', '001B6350', '001B6430', '001B6510' | the text-object cache — a vector at '+0x250'/'+0x258' of '{ptr}' entries keyed by '{id=+4, kind=+0x10}'; '001B6350' finds-or-allocs ('001BA860' + '00674A00'), '001B47A0' finds-and-assigns, '001B5330' releases, '001B6430'/'001B65"

```
001B6510  mov      qword ptr [rsp + 8], rbx
001B6515  push     rdi
001B6516  sub      rsp, 0x20
001B651A  mov      rdi, rcx
001B651D  mov      ebx, edx
001B651F  add      rcx, 0x190
001B6526  call     0x1ba860  ; -> 001BA860 fn
001B652B  xor      ecx, ecx
001B652D  mov      rdx, rax
001B6530  mov      qword ptr [rax + 8], rcx
001B6534  mov      dword ptr [rax + 0x14], ecx
001B6537  mov      byte ptr [rax], 0
001B653A  mov      r8d, dword ptr [rdi]
001B653D  shl      r8d, 5
001B6541  add      r8d, ebx
001B6544  mov      dword ptr [rax + 4], ecx
001B6547  mov      byte ptr [rax + 0x10], cl
001B654A  mov      rcx, rdi
001B654D  mov      dword ptr [rax + 0x18], r8d
001B6551  mov      rbx, qword ptr [rsp + 0x30]
001B6556  add      rsp, 0x20
001B655A  pop      rdi
001B655B  jmp      0x1b4590  ; -> 001B4590 fn
```

## 00274790 (31 B, extent 00274790-002747AF)

Page context: " to '0x100' for the duration of '00403550' (saved and restored), the '0x51EB851F' (/100) scalings of 'word[+0xBBD8]' and 'word[+0xBBDA]' by '[+0xD4]' offset '+0xC8'/'+0xCC' origins into the measure, '00274790' intersects the '+0xBBEC'/'+0xBBEE'-halved '+-0x20' box, and a four-side overflow clamp against '+0xF8'..'+0x104' bounds sets flag bits 1/2/4/8 - both x-sides clamped recentres x, both y-sides recentres y, and '/3' ('0x2AAAAAAB') o"

```
00274790  mov      edx, dword ptr [rcx]
00274792  mov      eax, dword ptr [rcx + 4]
00274795  cmp      edx, eax
00274797  jle      0x27479e  ; -> 0027479E
00274799  mov      dword ptr [rcx], eax
0027479B  mov      dword ptr [rcx + 4], edx
0027479E  mov      edx, dword ptr [rcx + 8]
002747A1  mov      eax, dword ptr [rcx + 0xc]
002747A4  cmp      edx, eax
002747A6  jle      0x2747ae  ; -> 002747AE
002747A8  mov      dword ptr [rcx + 8], eax
002747AB  mov      dword ptr [rcx + 0xc], edx
002747AE  ret      
```

## 00402BF0 (52 B, extent 00402BF0-00402C24)

Page context: "x138]'/'word[+0xBBE0]' mode 2, and each '0x30'- stride result entry gains '(word[+0x13A] & 8) << 0xC'; '00402D20' on 'rbx+0xB140' registers the product into '+0xBBC0', and a '+0xBBE0 == 6' tail runs '00402BF0' on it - the build-and-register the list's refresh issues. Interior anchor '002B74E0' (the per-entry 'or' loop).  '002B66E0' (624 B) is the bounded-position solver the same pair call: 'dword[+0x118]' is pinned to '0x100' for the du"

```
00402BF0  test     rcx, rcx
00402BF3  je       0x402c23  ; -> 00402C23
00402BF5  mov      eax, 0x80
00402BFA  mov      edx, 0xfff9
00402BFF  nop      
00402C00  cmp      byte ptr [rcx + 2], 1
00402C04  jne      0x402c1a  ; -> 00402C1A
00402C06  and      word ptr [rcx + 0x4e], dx
00402C0A  or       word ptr [rcx + 0x4e], 9
00402C0F  mov      dword ptr [rcx + 0x38], 0x3f800000
00402C16  mov      word ptr [rcx + 0x4c], ax
00402C1A  mov      rcx, qword ptr [rcx + 0x60]
00402C1E  test     rcx, rcx
00402C21  jne      0x402c00  ; -> 00402C00
00402C23  ret      
```
