# F-interior pack: `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/cmap-menumap-common-sublocation-directory.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/cmap-menumap-common-sublocation-directory.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 20da4dbde	SWE2-FRONTIER: pass 22 for SWE2-DATA - 25 pairs on three DATA pages read and accounted (batch D2, ex; bafa49c9f	SWE2-DATA: bucket member formats declared - 53 .bin + 5 .dat members, every entry assigned, each cla). OPUS read these before packing.

## 0029C530 (569 B, extent 0029C530-0029C769)

Page context: " '003161A0' read '00265270'. '00315E90' calls '003160C0', which reads the field id and calls the sub-location accessor '003779F0' (a table read from a global). UI bodies call '0032A8A0' ('00281AE0', '0029C530'), '003779F0' ('003C5E50') and '003C0380' ('003BE950'). The save finaliser '00583D60' calls '0032A8A0', which reads the persistent payload through '002EF2B0', and the script body '0034E0B0' calls '0032A8A0'. They are clients of the"

```
0029C530  push     rbx
0029C532  sub      rsp, 0x20
0029C536  mov      rbx, rcx
0029C539  mov      ecx, dword ptr [rdx]
0029C53B  sub      ecx, 1
0029C53E  je       0x29c589  ; -> 0029C589
0029C540  sub      ecx, 1
0029C543  je       0x29c761  ; -> 0029C761
0029C549  sub      ecx, 1
0029C54C  je       0x29c761  ; -> 0029C761
0029C552  sub      ecx, 0xb
0029C555  je       0x29c579  ; -> 0029C579
0029C557  cmp      ecx, 1
0029C55A  je       0x29c569  ; -> 0029C569
0029C55C  mov      rcx, rbx
0029C55F  add      rsp, 0x20
0029C563  pop      rbx
0029C564  jmp      0x5c5230  ; -> 005C5230 fn
0029C569  or       word ptr [rbx + 0xe6], 4
0029C571  xor      eax, eax
0029C573  add      rsp, 0x20
0029C577  pop      rbx
0029C578  ret      
0029C579  or       word ptr [rbx + 0xe6], 8
0029C581  xor      eax, eax
0029C583  add      rsp, 0x20
0029C587  pop      rbx
0029C588  ret      
0029C589  mov      rax, qword ptr [rip + 0x1dfe6a0]  ; -> 0209AC30
0029C590  lea      rcx, [rbx + 0x50]
0029C594  mov      qword ptr [rsp + 0x30], rbp
0029C599  mov      r9, rbx
0029C59C  mov      qword ptr [rsp + 0x38], rsi
0029C5A1  mov      r8d, 0x14
0029C5A7  mov      qword ptr [rsp + 0x40], rdi
0029C5AC  mov      rdx, qword ptr [rax + 8]
0029C5B0  mov      qword ptr [rsp + 0x48], r14
0029C5B5  call     0x2432b0  ; -> 002432B0 fn
0029C5BA  movzx    ecx, word ptr [rax + 0xa]
0029C5BE  movzx    edx, word ptr [rax + 8]
0029C5C2  movsx    r8d, word ptr [rax + 6]
0029C5C7  test     rbx, rbx
0029C5CA  je       0x29c5ed  ; -> 0029C5ED
0029C5CC  movzx    eax, word ptr [rax + 4]
0029C5D0  mov      word ptr [rbx + 0x98], ax
0029C5D7  mov      word ptr [rbx + 0x9a], r8w
0029C5DF  mov      word ptr [rbx + 0x9c], dx
0029C5E6  mov      word ptr [rbx + 0x9e], cx
0029C5ED  call     0x3148f0  ; -> 003148F0 fn
0029C5F2  mov      ecx, eax
0029C5F4  mov      ebp, eax
0029C5F6  call     0x264f90  ; -> 00264F90 fn
0029C5FB  mov      ecx, eax
0029C5FD  call     0x254380  ; -> 00254380 fn
0029C602  mov      ecx, 0x5e
0029C607  mov      r14d, eax
0029C60A  call     0x32a8a0  ; -> 0032A8A0 fn
0029C60F  test     eax, eax
0029C611  je       0x29c62d  ; -> 0029C62D
0029C613  call     0x314910  ; -> 00314910 fn
0029C618  mov      ecx, eax
0029C61A  call     0x3778b0  ; -> 003778B0 fn
0029C61F  xor      edi, edi
0029C621  mov      rcx, rax
0029C624  test     rbx, rbx
0029C627  jne      0x29c642  ; -> 0029C642
0029C629  mov      esi, edi
0029C62B  jmp      0x29c64a  ; -> 0029C64A
0029C62D  mov      ecx, ebp
0029C62F  call     0x3778b0  ; -> 003778B0 fn
0029C634  xor      edi, edi
0029C636  mov      rcx, rax
0029C639  test     rbx, rbx
0029C63C  jne      0x29c642  ; -> 0029C642
0029C63E  mov      esi, edi
0029C640  jmp      0x29c64a  ; -> 0029C64A
0029C642  mov      rax, qword ptr [rbx + 0x60]
0029C646  mov      rsi, qword ptr [rax + 0x18]
0029C64A  mov      qword ptr [rsi + 0x18], rcx
0029C64E  xor      ecx, ecx
0029C650  call     0x20e620  ; -> 0020E620 fn
0029C655  mov      ecx, ebp
0029C657  mov      dword ptr [rsi + 0x20], eax
0029C65A  call     0x377b60  ; -> 00377B60 fn
0029C65F  mov      rbp, qword ptr [rsp + 0x30]
0029C664  mov      rcx, rax
0029C667  test     rbx, rbx
0029C66A  jne      0x29c671  ; -> 0029C671
0029C66C  mov      rsi, rdi
0029C66F  jmp      0x29c679  ; -> 0029C679
0029C671  mov      rax, qword ptr [rbx + 0x60]
0029C675  mov      rsi, qword ptr [rax + 0x20]
0029C679  mov      qword ptr [rsi + 0x18], rcx
0029C67D  xor      ecx, ecx
0029C67F  call     0x20e620  ; -> 0020E620 fn
0029C684  mov      dword ptr [rsi + 0x20], eax
0029C687  test     rbx, rbx
0029C68A  jne      0x29c691  ; -> 0029C691
0029C68C  mov      rsi, rdi
0029C68F  jmp      0x29c699  ; -> 0029C699
0029C691  mov      rax, qword ptr [rbx + 0x60]
0029C695  mov      rsi, qword ptr [rax + 0x28]
0029C699  mov      ecx, r14d
0029C69C  call     0x2543d0  ; -> 002543D0 fn
0029C6A1  mov      r14, qword ptr [rsp + 0x48]
0029C6A6  mov      word ptr [rsi + 0xa], ax
0029C6AA  mov      rsi, qword ptr [rsp + 0x38]
0029C6AF  test     rbx, rbx
0029C6B2  jne      0x29c6b9  ; -> 0029C6B9
0029C6B4  mov      rcx, rdi
0029C6B7  jmp      0x29c6c1  ; -> 0029C6C1
0029C6B9  mov      rax, qword ptr [rbx + 0x60]
0029C6BD  mov      rcx, qword ptr [rax + 0x18]
0029C6C1  mov      eax, dword ptr [rcx + 0x24]
0029C6C4  mov      edx, 0xa0
0029C6C9  mov      dword ptr [rbx + 0xc0], eax
0029C6CF  movzx    eax, word ptr [rcx + 0xc]
0029C6D3  mov      word ptr [rbx + 0xc4], ax
0029C6DA  movzx    eax, word ptr [rcx + 0xe]
0029C6DE  mov      word ptr [rbx + 0xc6], ax
0029C6E5  movzx    eax, word ptr [rcx + 0x10]
0029C6E9  mov      word ptr [rbx + 0xc8], ax
0029C6F0  movzx    eax, word ptr [rcx + 0x12]
0029C6F4  mov      word ptr [rbx + 0xca], ax
0029C6FB  mov      rax, qword ptr [rbx + 0x60]
0029C6FF  mov      rcx, qword ptr [rax + 0x20]
0029C703  mov      eax, dword ptr [rcx + 0x24]
0029C706  mov      dword ptr [rbx + 0xd0], eax
0029C70C  movzx    eax, word ptr [rcx + 0xc]
0029C710  mov      word ptr [rbx + 0xd4], ax
0029C717  movzx    eax, word ptr [rcx + 0xe]
0029C71B  mov      word ptr [rbx + 0xd6], ax
0029C722  movzx    eax, word ptr [rcx + 0x10]
0029C726  mov      word ptr [rbx + 0xd8], ax
0029C72D  movzx    eax, word ptr [rcx + 0x12]
0029C731  mov      rcx, rbx
0029C734  mov      word ptr [rbx + 0xda], ax
0029C73B  call     0x247930  ; -> 00247930 fn
0029C740  mov      ecx, 3
0029C745  call     0x2735e0  ; -> 002735E0 fn
0029C74A  mov      rdx, rax
0029C74D  mov      rcx, rbx
0029C750  call     0x247570  ; -> 00247570 fn
0029C755  mov      word ptr [rbx + 0xe0], di
0029C75C  mov      rdi, qword ptr [rsp + 0x40]
0029C761  xor      eax, eax
0029C763  add      rsp, 0x20
0029C767  pop      rbx
0029C768  ret      
```
