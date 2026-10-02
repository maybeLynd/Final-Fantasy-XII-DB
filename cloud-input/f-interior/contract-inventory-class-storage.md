# F-interior pack: `12-Items-Equipment-Shops-License/CONTRACT-inventory-class-storage.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/contract-inventory-class-storage.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: c9b951983	EC7 pass-22 debt: crossing-section dispositions - 527 pairs / 65 pages (FRONTIER-REQ-SWE2-EC7-PASS22). OPUS read these before packing.

## 002FD420 (267 B, extent 002FD420-002FD52B)

Page context: "l: L1 readiness: BEHAVIORALLY UNDERSTOOD confidence: PROVEN implements: 12-Items-Equipment-Shops-License/item-id-encoding-and-equipment-compatibility.md entries: ["002FD8D0", "002FD970", "002FD150", "002FD420", "003047F0", "00309440", "00309F30",           "003008A0"] verified_against:   exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8   method: address-resolution verification 2026-09-14 (OPUS) - 41 addresses"

```
002FD420  mov      qword ptr [rsp + 0x10], rbp
002FD425  mov      qword ptr [rsp + 0x18], rsi
002FD42A  mov      qword ptr [rsp + 0x20], rdi
002FD42F  push     r14
002FD431  sub      rsp, 0x20
002FD435  mov      r14d, dword ptr [rsp + 0x50]
002FD43A  mov      edi, edx
002FD43C  movzx    ebp, cx
002FD43F  and      r14d, 1
002FD443  mov      eax, ebp
002FD445  mov      r10d, ebp
002FD448  shr      rax, 0xc
002FD44C  and      r10d, 0xfff
002FD453  imul     r9, rax, 0x58
002FD457  lea      rax, [rip + 0x1bee862]  ; -> 01EEBCC0
002FD45E  mov      esi, r8d
002FD461  mov      rdx, qword ptr [r9 + rax + 8]
002FD466  test     rdx, rdx
002FD469  jne      0x2fd472  ; -> 002FD472
002FD46B  xor      eax, eax
002FD46D  jmp      0x2fd515  ; -> 002FD515
002FD472  mov      eax, r10d
002FD475  shr      rax, 4
002FD479  mov      qword ptr [rsp + 0x30], rbx
002FD47E  xor      ebx, ebx
002FD480  mov      r9d, ebx
002FD483  lea      r8, [rdx + rax*2]
002FD487  movzx    eax, r10b
002FD48B  movsx    edx, word ptr [r8]
002FD48F  and      al, 0xf
002FD491  movzx    ecx, al
002FD494  bt       edx, ecx
002FD497  mov      ecx, edi
002FD499  setb     r9b
002FD49D  test     esi, esi
002FD49F  lea      eax, [r9 + rdi]
002FD4A3  cmove    ecx, eax
002FD4A6  test     ecx, ecx
002FD4A8  js       0x2fd4e1  ; -> 002FD4E1
002FD4AA  test     esi, esi
002FD4AC  lea      eax, [r9 + rdi]
002FD4B0  mov      ecx, edi
002FD4B2  cmove    ecx, eax
002FD4B5  cmp      ecx, 1
002FD4B8  jle      0x2fd4c9  ; -> 002FD4C9
002FD4BA  and      r10d, 0xf
002FD4BE  mov      ebx, 1
002FD4C3  bts      edx, r10d
002FD4C7  jmp      0x2fd4e9  ; -> 002FD4E9
002FD4C9  mov      ebx, edi
002FD4CB  test     esi, esi
002FD4CD  jne      0x2fd4d3  ; -> 002FD4D3
002FD4CF  lea      ebx, [r9 + rdi]
002FD4D3  test     ebx, ebx
002FD4D5  je       0x2fd4e1  ; -> 002FD4E1
002FD4D7  and      r10d, 0xf
002FD4DB  bts      edx, r10d
002FD4DF  jmp      0x2fd4e9  ; -> 002FD4E9
002FD4E1  and      r10d, 0xf
002FD4E5  btr      edx, r10d
002FD4E9  mov      word ptr [r8], dx
002FD4ED  movzx    ecx, bp
002FD4F0  mov      r8d, ebx
002FD4F3  mov      edx, r9d
002FD4F6  call     0x325f40  ; -> 00325F40 fn
002FD4FB  test     esi, esi
002FD4FD  jne      0x2fd50e  ; -> 002FD50E
002FD4FF  test     r14d, r14d
002FD502  je       0x2fd50e  ; -> 002FD50E
002FD504  mov      edx, edi
002FD506  movzx    ecx, bp
002FD509  call     0x46a630  ; -> 0046A630 fn
002FD50E  mov      eax, ebx
002FD510  mov      rbx, qword ptr [rsp + 0x30]
002FD515  mov      rbp, qword ptr [rsp + 0x38]
002FD51A  mov      rsi, qword ptr [rsp + 0x40]
002FD51F  mov      rdi, qword ptr [rsp + 0x48]
002FD524  add      rsp, 0x20
002FD528  pop      r14
002FD52A  ret      
```
