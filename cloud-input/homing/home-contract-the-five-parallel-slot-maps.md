# Homing pack: `11-Party/CONTRACT-the-five-parallel-slot-maps.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-contract-the-five-parallel-slot-maps.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00273800 (78 B, extent 00273800-0027384E)

Entered from (direct sites whose caller this page cites): `0035BC50` + 0x375 (call; `0035BC50` is cited on this page)
Other direct sites: none

Host context: "130', '0030FED0' - shared machinery across the layer boundary, no shared ownership. - **UI - CLIENT (3 edges).** '0031FE70', '00320040', '00322C50' are also called by bodies filed to UI: '00273880', '0035BC50', '0031EB20' - shared machinery across the layer boundary, no shared ownership. - **WorldAreaField - SERVICE (4 edges).** '003266C0', '00329CC0' reach bodies filed to WorldAreaField (world area): '00313F60', '00377C20', '00377C70' "

```
00273800  mov      qword ptr [rsp + 8], rbx
00273805  push     rdi
00273806  sub      rsp, 0x20
0027380A  mov      edi, ecx
0027380C  xor      ebx, ebx
0027380E  nop      
00273810  mov      ecx, ebx
00273812  call     0x35bb20  ; -> 0035BB20 fn
00273817  test     rax, rax
0027381A  je       0x273821  ; -> 00273821
0027381C  cmp      dword ptr [rax + 4], edi
0027381F  je       0x273835  ; -> 00273835
00273821  inc      ebx
00273823  cmp      ebx, 4
00273826  jl       0x273810  ; -> 00273810
00273828  xor      eax, eax
0027382A  mov      rbx, qword ptr [rsp + 0x30]
0027382F  add      rsp, 0x20
00273833  pop      rdi
00273834  ret      
00273835  movzx    eax, byte ptr [rax]
00273838  mov      rbx, qword ptr [rsp + 0x30]
0027383D  not      al
0027383F  movzx    eax, al
00273842  shr      eax, 3
00273845  and      eax, 1
00273848  add      rsp, 0x20
0027384C  pop      rdi
0027384D  ret      
```
