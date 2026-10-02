# F-interior pack: `01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md`

Generated 2026-10-02 08:46 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/script-variables-and-their-storage-classes.json`.

Functions: 2. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 01c2429f6	SWE2-CONTRACT: pass-22 debt batch B - 47 Script-VM, Resource, EBP and PKFL pages' cross-subsystem ne; inbox mentions: FABLE.md, SWE2-AUDIT-SPEC.md). OPUS read these before packing.

## 00267560 (85 B, extent 00267560-002675B5)

Page context: "tes/script-vm-arith-consumers/README.md) C) → the 'ucomiss'/'comiss' float path ('cmova'), where any NaN returns +1; stack underflow → '008620C0(1)' | ['0025D813'](../../_index/ADDRESS-INDEX.md) | | '00267560' (85 B) | the "both operands int?" predicate the int-ALU arms call — depth < 2 → '008620C0(1)'; returns 1 iff the two top type bytes are both 1 | — | | '002659F0' (48 B) | the debug/trace marker — 'rec = 02098E10 + byte[+0x15] × 0x"

```
00267560  push     rbx
00267562  sub      rsp, 0x20
00267566  mov      r8d, dword ptr [rcx]
00267569  xor      ebx, ebx
0026756B  mov      rax, rcx
0026756E  cmp      r8d, 2
00267572  jge      0x267584  ; -> 00267584
00267574  lea      ecx, [rbx + 1]
00267577  call     0x8620c0  ; -> 008620C0 fn
0026757C  mov      eax, ebx
0026757E  add      rsp, 0x20
00267582  pop      rbx
00267583  ret      
00267584  lea      ecx, [r8 - 1]
00267588  movsxd   rdx, ecx
0026758B  lea      ecx, [r8 - 2]
0026758F  movzx    r9d, byte ptr [rdx + rax + 4]
00267595  movsxd   rdx, ecx
00267598  movzx    ecx, byte ptr [rdx + rax + 4]
0026759D  cmp      r9d, ecx
002675A0  jne      0x2675ad  ; -> 002675AD
002675A2  mov      eax, 1
002675A7  cmp      r9d, eax
002675AA  cmove    ebx, eax
002675AD  mov      eax, ebx
002675AF  add      rsp, 0x20
002675B3  pop      rbx
002675B4  ret      
```

## 004745B0 (21 B, extent 004745B0-004745C5)

Page context: "sured  '003590E0' (101 B) is the state-block reset '002695A0' and '0026DB30' run: it zeroes the five '02CDBFxx'/'02CDC0xx' dwords and the '02CDC01C' byte, clears a four-byte run at '02CDBF03', calls '004745B0' on the '02CDBE9B' object, and finally clears the '02CDC1E1' qword. Interior anchor '0035912B' (the '004745B0' call).  ## SWE2-EC7-98 update (2026-09-20) - '002E15D0' measured  '002E15D0' (28 B) is the state-block reset '0026A5F0' "

```
004745B0  mov      dword ptr [rcx], 1
004745B6  mov      dword ptr [rcx + 4], 0x12
004745BD  mov      dword ptr [rcx + 0xc], 0
004745C4  ret      
```
