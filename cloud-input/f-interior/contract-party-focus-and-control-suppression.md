# F-interior pack: `11-Party/CONTRACT-party-focus-and-control-suppression.md`

Generated 2026-10-02 18:41 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/contract-party-focus-and-control-suppression.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

## 003593A0 (97 B, extent 003593A0-00359401)

Page context: ", rbx+0x7A0, [rbx+0x850])' blends it in, 'word[+0x690]' becomes 4 - the slot's pose install.  Interior anchor '0025A25C' (function '0025A180').  '00259800' (25 B) is the single-slot reset '00358BC0'/'003593A0'/'00359410' call - 'ecx' x 0x860's '02098574' row is zeroed, the same table '0025A280' clears on change.  Interior anchor '00259811' (function '00259800').  '00259510' (270 B) is the blend '0025A180'/'00259B30'/'0025A6A0' call: '00"

```
003593A0  push     rbx
003593A2  sub      rsp, 0x20
003593A6  mov      ebx, ecx
003593A8  mov      ecx, dword ptr [rip + 0x1f6ec3e]  ; -> 022C7FEC
003593AE  test     ecx, ecx
003593B0  jne      0x3593d4  ; -> 003593D4
003593B2  test     ebx, ebx
003593B4  je       0x3593f5  ; -> 003593F5
003593B6  mov      ecx, dword ptr [rip + 0x1f6ec24]  ; -> 022C7FE0
003593BC  call     0x3588b0  ; -> 003588B0 fn
003593C1  test     rax, rax
003593C4  je       0x3593ce  ; -> 003593CE
003593C6  mov      rcx, rax
003593C9  call     0x26d6d0  ; -> 0026D6D0 fn
003593CE  mov      ecx, dword ptr [rip + 0x1f6ec18]  ; -> 022C7FEC
003593D4  cmp      ecx, ebx
003593D6  je       0x3593f5  ; -> 003593F5
003593D8  test     ecx, ecx
003593DA  je       0x3593f5  ; -> 003593F5
003593DC  call     0x3588b0  ; -> 003588B0 fn
003593E1  test     rax, rax
003593E4  je       0x3593ee  ; -> 003593EE
003593E6  mov      rcx, rax
003593E9  call     0x26d6d0  ; -> 0026D6D0 fn
003593EE  xor      ecx, ecx
003593F0  call     0x259800  ; -> 00259800 fn
003593F5  mov      dword ptr [rip + 0x1f6ebf1], ebx  ; -> 022C7FEC
003593FB  add      rsp, 0x20
003593FF  pop      rbx
00359400  ret      
```
