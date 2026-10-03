# F-interior pack: `15-Input/how-a-gamepad-becomes-a-controller-object.md`

Generated 2026-10-02 20:18 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/how-a-gamepad-becomes-a-controller-object.json`.

Functions: 2. Each is cited on the page only at its entry and is still in the F frontier.

## 00796230 (75 B, extent 00796230-0079627B)

Page context: "r:Input evidence_tier: 1 verified_against:   exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8   method: the DirectInput initialiser 00797910, the two enumeration callbacks 00796230 and 00798A40, the per-device     body 00797690, the controller base constructor 00792940 and its three derived constructors 00792CB0, 00792AB0 and     00792B70 disassembled from the authority image and read whole, 2026-09-19; the t"

```
00796230  sub      rsp, 0x28
00796234  movzx    edx, byte ptr [rcx + 0x24]
00796238  cmp      dl, 0x12
0079623B  je       0x79626c  ; -> 0079626C
0079623D  cmp      dl, 0x13
00796240  je       0x79625d  ; -> 0079625D
00796242  lea      eax, [rdx - 0x14]
00796245  test     al, 0xfa
00796247  jne      0x796271  ; -> 00796271
00796249  cmp      dl, 0x19
0079624C  je       0x796271  ; -> 00796271
0079624E  call     0x797690  ; -> 00797690 fn
00796253  mov      eax, 1
00796258  add      rsp, 0x28
0079625C  ret      
0079625D  call     0x7973d0  ; -> 007973D0 fn
00796262  mov      eax, 1
00796267  add      rsp, 0x28
0079626B  ret      
0079626C  call     0x797460  ; -> 00797460 fn
00796271  mov      eax, 1
00796276  add      rsp, 0x28
0079627A  ret      
```

## 00798A40 (55 B, extent 00798A40-00798A77)

Page context: "nce_tier: 1 verified_against:   exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8   method: the DirectInput initialiser 00797910, the two enumeration callbacks 00796230 and 00798A40, the per-device     body 00797690, the controller base constructor 00792940 and its three derived constructors 00792CB0, 00792AB0 and     00792B70 disassembled from the authority image and read whole, 2026-09-19; the three log stri"

```
00798A40  sub      rsp, 0x28
00798A44  movzx    edx, byte ptr [rcx + 0x24]
00798A48  cmp      dl, 0x12
00798A4B  je       0x798a68  ; -> 00798A68
00798A4D  lea      eax, [rdx - 0x14]
00798A50  test     al, 0xfa
00798A52  jne      0x798a6d  ; -> 00798A6D
00798A54  cmp      dl, 0x19
00798A57  je       0x798a6d  ; -> 00798A6D
00798A59  call     0x797690  ; -> 00797690 fn
00798A5E  mov      eax, 1
00798A63  add      rsp, 0x28
00798A67  ret      
00798A68  call     0x797460  ; -> 00797460 fn
00798A6D  mov      eax, 1
00798A72  add      rsp, 0x28
00798A76  ret      
```
