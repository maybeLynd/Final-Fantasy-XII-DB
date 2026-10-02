# F-interior pack: `10-Status-Periodic-Terminal/the-thirty-two-statuses.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/the-thirty-two-statuses.json`.

Functions: 2. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 7903502f7	FABLE: pass-22 debt - crossing sections on 94 pages (FABLE's group; 12 overlay-carrier pages routed ; inbox mentions: FABLE.md, SWE2-CONTRACT.md). OPUS read these before packing.

## 00238640 (19 B, extent 00238640-00238653)

Page context: " **What is now open instead, and it is narrower.** Bank 12's slot '02EC3DE0' is written by exactly one body in         the image, '002F7800', which hard-codes the bank number '0xC' and tail-jumps to '00238640', which hands         '&02F973C0[12]' on to a single loader entry — named by role, not by address, because that body's own callers         cross into a layer this page does not discuss. '002F7800' has **no direct call site and no a"

```
00238640  movsxd   rax, ecx
00238643  lea      rcx, [rip + 0x2d5ed76]  ; -> 02F973C0
0023864A  lea      rcx, [rcx + rax*8]
0023864E  jmp      0x3845f0  ; -> 003845F0 fn
```

## 0030AE30 (105 B, extent 0030AE30-0030AE99)

Page context: "0') at '0031C643', '0031C662', '0031C716', '0031C85C'; 'BattleEncodedId_DispatchQueryMode0Value' ('00309EC0') at '0031C828', '0031C98F', '0031CC08', '0031CD6C'; 'BattleEncodedId_DispatchQueryMode1' ('0030AE30') at '0031C836', '0031C9A6', '0031CC16', '0031CD7A'; and 'BattleEncodedId_QueryMode0Positive' ('0030B0E0') at '0031DFD3' and '0031E0C3'. **The mode-0 and mode-1 dispatchers are called in pairs** — each '00309EC0' site is followed w"

```
0030AE30  mov      eax, 0xffff
0030AE35  movzx    r8d, cx
0030AE39  cmp      cx, ax
0030AE3C  jne      0x30ae42  ; -> 0030AE42
0030AE3E  or       eax, 0xffffffff
0030AE41  ret      
0030AE42  mov      ecx, 0xf000
0030AE47  movzx    eax, r8w
0030AE4B  and      ax, cx
0030AE4E  mov      ecx, 0xe000
0030AE53  cmp      ax, cx
0030AE56  ja       0x30ae3e  ; -> 0030AE3E
0030AE58  movzx    eax, r8w
0030AE5C  shr      rax, 0xc
0030AE60  imul     rdx, rax, 0x58
0030AE64  lea      rax, [rip + 0x1be0e55]  ; -> 01EEBCC0
0030AE6B  movzx    ecx, r8w
0030AE6F  add      rdx, rax
0030AE72  and      ecx, 0xfff
0030AE78  mov      eax, dword ptr [rdx + 0x3c]
0030AE7B  dec      eax
0030AE7D  cmp      ecx, eax
0030AE7F  jg       0x30ae96  ; -> 0030AE96
0030AE81  mov      rax, qword ptr [rdx + 0x50]
0030AE85  test     rax, rax
0030AE88  je       0x30ae96  ; -> 0030AE96
0030AE8A  mov      edx, 1
0030AE8F  movzx    ecx, r8w
0030AE93  jmp      rax
0030AE96  xor      eax, eax
0030AE98  ret      
```
