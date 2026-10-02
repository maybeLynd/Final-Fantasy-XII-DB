# F-interior pack: `11-Party/CONTRACT-party-slot-assignment.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/contract-party-slot-assignment.json`.

Functions: 3. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: c9b951983	EC7 pass-22 debt: crossing-section dispositions - 527 pairs / 65 pages (FRONTIER-REQ-SWE2-EC7-PASS22). OPUS read these before packing.

## 003415D0 (43 B, extent 003415D0-003415FB)

Page context: "02EF2B0' - shared machinery across the layer boundary, no shared ownership. - **Script_VM_Native_Bridge - CLIENT (23 edges).** '00263750' is also called by bodies filed to script VM / native bridge: '003415D0', '00341CB0', '00342250' - shared machinery across the layer boundary, no shared ownership. - **World - CLIENT (1 edge).** '0026DB30' is also called by bodies filed to World: '00266D10' (NativeSupport) - shared machinery across the"

```
003415D0  push     rbx
003415D2  sub      rsp, 0x20
003415D6  xor      ebx, ebx
003415D8  mov      ecx, ebx
003415DA  call     0x263750  ; -> 00263750 fn
003415DF  test     rax, rax
003415E2  je       0x3415ee  ; -> 003415EE
003415E4  xor      edx, edx
003415E6  mov      rcx, rax
003415E9  call     0x26dc40  ; -> 0026DC40 fn
003415EE  inc      ebx
003415F0  cmp      ebx, 4
003415F3  jl       0x3415d8  ; -> 003415D8
003415F5  add      rsp, 0x20
003415F9  pop      rbx
003415FA  ret      
```

## 00341CB0 (77 B, extent 00341CB0-00341CFD)

Page context: "hared machinery across the layer boundary, no shared ownership. - **Script_VM_Native_Bridge - CLIENT (23 edges).** '00263750' is also called by bodies filed to script VM / native bridge: '003415D0', '00341CB0', '00342250' - shared machinery across the layer boundary, no shared ownership. - **World - CLIENT (1 edge).** '0026DB30' is also called by bodies filed to World: '00266D10' (NativeSupport) - shared machinery across the layer bound"

```
00341CB0  mov      qword ptr [rsp + 8], rbx
00341CB5  push     rdi
00341CB6  sub      rsp, 0x20
00341CBA  call     0x3590d0  ; -> 003590D0 fn
00341CBF  mov      ecx, eax
00341CC1  call     0x3588b0  ; -> 003588B0 fn
00341CC6  mov      rdi, rax
00341CC9  xor      ebx, ebx
00341CCB  nop      dword ptr [rax + rax]
00341CD0  mov      ecx, ebx
00341CD2  call     0x263750  ; -> 00263750 fn
00341CD7  test     rax, rax
00341CDA  je       0x341ceb  ; -> 00341CEB
00341CDC  cmp      rax, rdi
00341CDF  je       0x341ceb  ; -> 00341CEB
00341CE1  xor      edx, edx
00341CE3  mov      rcx, rax
00341CE6  call     0x26dc40  ; -> 0026DC40 fn
00341CEB  inc      ebx
00341CED  cmp      ebx, 4
00341CF0  jl       0x341cd0  ; -> 00341CD0
00341CF2  mov      rbx, qword ptr [rsp + 0x30]
00341CF7  add      rsp, 0x20
00341CFB  pop      rdi
00341CFC  ret      
```

## 00342250 (46 B, extent 00342250-0034227E)

Page context: "ery across the layer boundary, no shared ownership. - **Script_VM_Native_Bridge - CLIENT (23 edges).** '00263750' is also called by bodies filed to script VM / native bridge: '003415D0', '00341CB0', '00342250' - shared machinery across the layer boundary, no shared ownership. - **World - CLIENT (1 edge).** '0026DB30' is also called by bodies filed to World: '00266D10' (NativeSupport) - shared machinery across the layer boundary, no shar"

```
00342250  push     rbx
00342252  sub      rsp, 0x20
00342256  xor      ebx, ebx
00342258  mov      ecx, ebx
0034225A  call     0x263750  ; -> 00263750 fn
0034225F  test     rax, rax
00342262  je       0x342271  ; -> 00342271
00342264  mov      edx, 1
00342269  mov      rcx, rax
0034226C  call     0x26dc40  ; -> 0026DC40 fn
00342271  inc      ebx
00342273  cmp      ebx, 4
00342276  jl       0x342258  ; -> 00342258
00342278  add      rsp, 0x20
0034227C  pop      rbx
0034227D  ret      
```
