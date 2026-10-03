# Homing pack: `15-Input/CONTRACT-input-subsystem.md`

Generated 2026-10-02 22:54 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-contract-input-subsystem.json`.

Bodies: 3. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0025D5D0 (8 B, extent 0025D5D0-0025D5D8)

Entered from (direct sites whose caller this page cites): `00342770` + 0xB8 (jmp; `00342770` is cited on this page)
Other direct sites: `003437A0` + 0x64 (jmp); `00343C60` + 0x36 (call); `00344410` + 0x1F (jmp); `00345B60` + 0x7A (call); `00346C00` + 0x108 (jmp); `00347A50` + 0x52 (jmp)

Host context: "es the same query; the arbiter depends only on the query's answer, not on the save path.  **Script_VM_Native_Bridge — CLIENT, OUT-OF-SCOPE (65 edges).** 56 script-verb bodies, among them '0033F330', '00342770', '00347B00', '00357040' and '003581B0', call '00267310', the 22-byte reader that returns one byte of a slot's '0x288'-byte record; four verbs ('0033F950', '00348DF0', '0034ADA0', '0050EAB0') call the message-window opener '002E16B"

```
0025D5D0  and      byte ptr [rip + 0x1e3b850], 0x7f  ; -> 02098E27
0025D5D7  ret      
```

## 00361480 (61 B, extent 00361480-003614BD)

Entered from (direct sites whose caller this page cites): `00342770` + 0x83 (call; `00342770` is cited on this page)
Other direct sites: `00341C80` + 0x16 (call)

Host context: "es the same query; the arbiter depends only on the query's answer, not on the save path.  **Script_VM_Native_Bridge — CLIENT, OUT-OF-SCOPE (65 edges).** 56 script-verb bodies, among them '0033F330', '00342770', '00347B00', '00357040' and '003581B0', call '00267310', the 22-byte reader that returns one byte of a slot's '0x288'-byte record; four verbs ('0033F950', '00348DF0', '0034ADA0', '0050EAB0') call the message-window opener '002E16B"

```
00361480  xor      edx, edx
00361482  lea      r8, [rip + 0x1f6a567]  ; -> 022CB9F0
00361489  lea      r9d, [rdx - 5]
0036148D  nop      dword ptr [rax]
00361490  cmp      byte ptr [r8], 0
00361494  je       0x3614a2  ; -> 003614A2
00361496  movzx    eax, byte ptr [r8 + 1]
0036149B  cmp      eax, ecx
0036149D  jne      0x3614ae  ; -> 003614AE
0036149F  mov      eax, edx
003614A1  ret      
003614A2  cmp      r9d, -5
003614A6  jne      0x3614ae  ; -> 003614AE
003614A8  mov      r9d, edx
003614AB  not      r9d
003614AE  inc      edx
003614B0  add      r8, 0x18
003614B4  cmp      edx, 4
003614B7  jl       0x361490  ; -> 00361490
003614B9  mov      eax, r9d
003614BC  ret      
```

## 003DD980 (147 B, extent 003DD980-003DDA13)

Entered from (direct sites whose caller this page cites): `00347B00` + 0x95 (call; `00347B00` is cited on this page)
Other direct sites: none

Host context: "query; the arbiter depends only on the query's answer, not on the save path.  **Script_VM_Native_Bridge — CLIENT, OUT-OF-SCOPE (65 edges).** 56 script-verb bodies, among them '0033F330', '00342770', '00347B00', '00357040' and '003581B0', call '00267310', the 22-byte reader that returns one byte of a slot's '0x288'-byte record; four verbs ('0033F950', '00348DF0', '0034ADA0', '0050EAB0') call the message-window opener '002E16B0'; '0034E0B"

```
003DD980  mov      qword ptr [rsp + 8], rbx
003DD985  mov      qword ptr [rsp + 0x10], rbp
003DD98A  mov      qword ptr [rsp + 0x18], rsi
003DD98F  push     rdi
003DD990  sub      rsp, 0x30
003DD994  movsxd   rbx, edx
003DD997  mov      rdi, rcx
003DD99A  mov      r10, rbx
003DD99D  movsxd   rsi, r8d
003DD9A0  shl      r10, 4
003DD9A4  lea      rcx, [rip + 0x277a7f9]  ; -> 02B581A4
003DD9AB  add      r10, rsi
003DD9AE  mov      ebp, r9d
003DD9B1  imul     rax, r10, 0x1c
003DD9B5  cmp      dword ptr [rax + rcx], 4
003DD9B9  jne      0x3dd9fe  ; -> 003DD9FE
003DD9BB  mov      rcx, rdi
003DD9BE  call     0x2e95b0  ; -> 002E95B0 fn
003DD9C3  movaps   xmm1, xmm0
003DD9C6  mov      rcx, rdi
003DD9C9  call     0x2e4fa0  ; -> 002E4FA0 fn
003DD9CE  xor      edx, edx
003DD9D0  mov      rcx, rdi
003DD9D3  call     0x2e81d0  ; -> 002E81D0 fn
003DD9D8  movss    xmm0, dword ptr [rsp + 0x60]
003DD9DE  xor      r9d, r9d
003DD9E1  shl      ebx, 4
003DD9E4  mov      rdx, rdi
003DD9E7  or       ebx, esi
003DD9E9  movss    dword ptr [rsp + 0x20], xmm0
003DD9EF  shl      ebx, 0x10
003DD9F2  xor      ecx, ecx
003DD9F4  or       ebx, ebp
003DD9F6  mov      r8d, ebx
003DD9F9  call     0x2eb0d0  ; -> 002EB0D0 fn
003DD9FE  mov      rbx, qword ptr [rsp + 0x40]
003DDA03  mov      rbp, qword ptr [rsp + 0x48]
003DDA08  mov      rsi, qword ptr [rsp + 0x50]
003DDA0D  add      rsp, 0x30
003DDA11  pop      rdi
003DDA12  ret      
```
