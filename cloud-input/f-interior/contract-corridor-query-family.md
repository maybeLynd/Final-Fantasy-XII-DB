# F-interior pack: `06-Movement-And-Navigation/CONTRACT-corridor-query-family.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/contract-corridor-query-family.json`.

Functions: 2. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: c9b951983	EC7 pass-22 debt: crossing-section dispositions - 527 pairs / 65 pages (FRONTIER-REQ-SWE2-EC7-PASS22; inbox mentions: SWE2-FRONTIER.md). OPUS read these before packing.

## 0030BEB0 (63 B, extent 0030BEB0-0030BEEF)

Page context: " shared machinery across the layer boundary, no shared ownership. - **Party - CLIENT (7 edges).** '00236820', '0031B760', '00328370' are also called by bodies filed to party: '003261D0', '003273D0', '0030BEB0' - shared machinery across the layer boundary, no shared ownership. - **Presentation - CLIENT (41 edges).** '0018EE20', '002324F0', '00263FF0' are also called by bodies filed to presentation: '001946E0' (Rendering), '0022FFE0' (Nav"

```
0030BEB0  sub      rsp, 0x28
0030BEB4  call     0x31b760  ; -> 0031B760 fn
0030BEB9  mov      rcx, rax
0030BEBC  test     rax, rax
0030BEBF  je       0x30bee8  ; -> 0030BEE8
0030BEC1  mov      eax, dword ptr [rax]
0030BEC3  test     al, 8
0030BEC5  je       0x30bee8  ; -> 0030BEE8
0030BEC7  mov      rdx, qword ptr [rcx + 0x698]
0030BECE  test     rdx, rdx
0030BED1  je       0x30bee8  ; -> 0030BEE8
0030BED3  movzx    ecx, byte ptr [rdx + 5]
0030BED7  test     ecx, ecx
0030BED9  jne      0x30bee8  ; -> 0030BEE8
0030BEDB  shr      eax, 0x17
0030BEDE  not      eax
0030BEE0  and      eax, 1
0030BEE3  add      rsp, 0x28
0030BEE7  ret      
0030BEE8  xor      eax, eax
0030BEEA  add      rsp, 0x28
0030BEEE  ret      
```

## 0033F7F0 (58 B, extent 0033F7F0-0033F82A)

Page context: "02EF640' - shared machinery across the layer boundary, no shared ownership. - **Script_VM_Native_Bridge - CLIENT (26 edges).** '00263FF0' is also called by bodies filed to script VM / native bridge: '0033F7F0', '00342490', '00342A30' - shared machinery across the layer boundary, no shared ownership. - **Spawn_Encounter_Lifecycle - CLIENT (30 edges).** '00236820', '0031B760' are also called by bodies filed to spawn/encounter lifecycle: '"

```
0033F7F0  mov      qword ptr [rsp + 8], rbx
0033F7F5  push     rdi
0033F7F6  sub      rsp, 0x20
0033F7FA  mov      rdi, rcx
0033F7FD  xor      ecx, ecx
0033F7FF  call     0x263ff0  ; -> 00263FF0 fn
0033F804  mov      rbx, rax
0033F807  call     0x3148b0  ; -> 003148B0 fn
0033F80C  mov      edx, eax
0033F80E  mov      rcx, rbx
0033F811  call     0x264ce0  ; -> 00264CE0 fn
0033F816  mov      edx, eax
0033F818  mov      rcx, rdi
0033F81B  mov      rbx, qword ptr [rsp + 0x30]
0033F820  add      rsp, 0x20
0033F824  pop      rdi
0033F825  jmp      0x26b4e0  ; -> 0026B4E0 fn
```
