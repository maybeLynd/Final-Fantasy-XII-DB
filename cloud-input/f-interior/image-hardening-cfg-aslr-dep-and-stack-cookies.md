# F-interior pack: `24-Compiler-And-CRT-Runtime/Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md`

Generated 2026-10-02 20:18 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/image-hardening-cfg-aslr-dep-and-stack-cookies.json`.

Functions: 2. Each is cited on the page only at its entry and is still in the F frontier.

## 003F9270 (58 B, extent 003F9270-003F92AA)

Page context: "250' is called from 'ActorResource_BeginPrimaryPayloadLoad' and '003306E0'. - **UI, 5, and WorldAreaField, 1 — CLIENT.** '003F9720', an untraced cookie site, is a widget body. It calls   '003F8FE0', '003F9270', '003F92B0', '003F9390' and 'WorldTransition_GetActiveOrPendingFieldId', and is called by   '003F8EC0'. - **Presentation — MECHANICAL, two edges.** The item-screen pane '00578450' calls both 'xmlStrchr' ('002B39A0') and the   chai"

```
003F9270  mov      r8, rcx
003F9273  lea      rdx, [rcx + 0x425c]
003F927A  xor      eax, eax
003F927C  nop      dword ptr [rax]
003F9280  test     byte ptr [rdx], 1
003F9283  je       0x3f9296  ; -> 003F9296
003F9285  inc      eax
003F9287  add      rdx, 0x250
003F928E  cmp      eax, 8
003F9291  jb       0x3f9280  ; -> 003F9280
003F9293  xor      eax, eax
003F9295  ret      
003F9296  cdqe     
003F9298  imul     rcx, rax, 0x250
003F929F  lea      rax, [r8 + 0x4020]
003F92A6  add      rax, rcx
003F92A9  ret      
```

## 00896270 (2 B, extent 00896270-00896272)

Page context: " @ 0x8C31C0 [.rdata]  ->  0x0016D6A0     0x0016d6a0   c2 00 00        ret 0            <- the no-op check     0x0016d6a3   cc cc cc ...    int3  __guard_dispatch_icall_fptr @ 0x8C31C8 [.rdata]  ->  0x00896270     0x00896270   ff e0           jmp rax          <- unvalidated indirect jump     0x00896272   cc cc cc ...    int3 '''  'ret 0' is '_guard_check_icall_nop'. 'jmp rax' is a bare indirect branch with no target check.  ### ~~The 145"

```
00896270  jmp      rax
```
