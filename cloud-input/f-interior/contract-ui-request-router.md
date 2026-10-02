# F-interior pack: `16-UI/CONTRACT-ui-request-router.md`

Generated 2026-10-02 10:27 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/contract-ui-request-router.json`.

Functions: 4. Each is cited on the page only at its entry and is still in the F frontier.

## 002E0DA0 (104 B, extent 002E0DA0-002E0E08)

Page context: "are STATIC; no live capture of a refused request confidence: PROVEN implements:   - Request-Router/ui-request-router.md entries: [00254B50, 002E1B10, 002E09A0, 00280A00, 00252B40, 00252D90, 002E1A60, 002E0DA0] verified_against:   exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8   method: read from the authority image in this session (2026-09-21, FABLE). The dispatch table in §3     is decoded from the two '.r"

```
002E0DA0  mov      edx, ecx
002E0DA2  btr      ecx, 0xf
002E0DA6  and      edx, 0x8000
002E0DAC  cmp      ecx, 6
002E0DAF  ja       0x2e0e00  ; -> 002E0E00
002E0DB1  movsxd   rax, ecx
002E0DB4  lea      r8, [rip - 0x1c0dbb]  ; -> 00120000 (image base)
002E0DBB  mov      ecx, dword ptr [r8 + rax*4 + 0x1c0e08]  ; image base + 0x1c0e08 = 002E0E08
002E0DC3  add      rcx, r8
002E0DC6  jmp      rcx
002E0DC8  mov      eax, 0x11
002E0DCD  or       eax, edx
002E0DCF  ret      
002E0DD0  mov      eax, 0x12
002E0DD5  or       eax, edx
002E0DD7  ret      
002E0DD8  mov      eax, 0xa
002E0DDD  or       eax, edx
002E0DDF  ret      
002E0DE0  mov      eax, 0xf
002E0DE5  or       eax, edx
002E0DE7  ret      
002E0DE8  mov      eax, 0x13
002E0DED  or       eax, edx
002E0DEF  ret      
002E0DF0  mov      eax, 6
002E0DF5  or       eax, edx
002E0DF7  ret      
002E0DF8  mov      eax, 0x16
002E0DFD  or       eax, edx
002E0DFF  ret      
002E0E00  mov      eax, 2
002E0E05  or       eax, edx
002E0E07  ret      
```

## 002E1AE0 (37 B, extent 002E1AE0-002E1B05)

Page context: "' and '0215F1A8' have **five writers and exactly one reader each**, and that reader is the drain '002E09A0'. The five writers are the post '002E1B10', the script path '002E1A60', the request-12 path '002E1AE0', and the two resets '002E09A0' and '002E15D0' — the same five for both cells, which is what makes them one record rather than two. The pending byte '0215F1A0' carries those same five writers and **two** readers, the drain and '002"

```
002E1AE0  cmp      byte ptr [rip + 0x1e7d6ba], 0  ; -> 0215F1A1
002E1AE7  jne      0x2e1b04  ; -> 002E1B04
002E1AE9  mov      byte ptr [rip + 0x1e7d6b0], 1  ; -> 0215F1A0
002E1AF0  mov      dword ptr [rip + 0x1e7d6aa], 0xc  ; -> 0215F1A4
002E1AFA  mov      dword ptr [rip + 0x1e7d6a4], 0  ; -> 0215F1A8
002E1B04  ret      
```

## 003462D0 (81 B, extent 003462D0-00346321)

Page context: "0' calls '00796E20'. A platform body reaches the same application singleton getter; the contract's use of the getter is unrelated.  **Script_VM_Native_Bridge — CLIENT (8 edges).** The begin handlers '003462D0' ('openfullscreenmenu_48d') and '003470D0' pop two script values, post a fullscreen request through '002E1A60' and then call '002E1690'; '0050DAB0' (the developer hook, verb '0x2037') pops one value and tail-jumps into the post '00"

```
003462D0  mov      qword ptr [rsp + 8], rbx
003462D5  push     rdi
003462D6  sub      rsp, 0x20
003462DA  mov      rdi, r9
003462DD  mov      rbx, r8
003462E0  call     0x229eb0  ; -> 00229EB0 fn
003462E5  movzx    eax, al
003462E8  mov      rcx, rdi
003462EB  mov      dword ptr [rbx + 4], eax
003462EE  mov      dword ptr [rbx + 8], 0
003462F5  call     0x267e10  ; -> 00267E10 fn
003462FA  mov      rcx, rdi
003462FD  mov      ebx, eax
003462FF  call     0x267e10  ; -> 00267E10 fn
00346304  mov      edx, ebx
00346306  mov      ecx, eax
00346308  call     0x2e1a60  ; -> 002E1A60 fn
0034630D  call     0x2e1690  ; -> 002E1690 fn
00346312  mov      rbx, qword ptr [rsp + 0x30]
00346317  add      rsp, 0x20
0034631B  pop      rdi
0034631C  jmp      0x2e0650  ; -> 002E0650 fn
```

## 003470D0 (91 B, extent 003470D0-0034712B)

Page context: "es the same application singleton getter; the contract's use of the getter is unrelated.  **Script_VM_Native_Bridge — CLIENT (8 edges).** The begin handlers '003462D0' ('openfullscreenmenu_48d') and '003470D0' pop two script values, post a fullscreen request through '002E1A60' and then call '002E1690'; '0050DAB0' (the developer hook, verb '0x2037') pops one value and tail-jumps into the post '002E1B10'; '0050D0C0' and '0050D240' call th"

```
003470D0  mov      qword ptr [rsp + 8], rbx
003470D5  push     rdi
003470D6  sub      rsp, 0x20
003470DA  xor      edx, edx
003470DC  mov      rcx, r9
003470DF  mov      rdi, r9
003470E2  mov      rbx, r8
003470E5  call     0x267f90  ; -> 00267F90 fn
003470EA  call     0x229eb0  ; -> 00229EB0 fn
003470EF  movzx    eax, al
003470F2  mov      rcx, rdi
003470F5  mov      dword ptr [rbx + 4], eax
003470F8  mov      dword ptr [rbx + 8], 0
003470FF  call     0x267e10  ; -> 00267E10 fn
00347104  mov      rcx, rdi
00347107  mov      ebx, eax
00347109  call     0x267e10  ; -> 00267E10 fn
0034710E  mov      edx, ebx
00347110  mov      ecx, eax
00347112  call     0x2e1a60  ; -> 002E1A60 fn
00347117  call     0x2e1690  ; -> 002E1690 fn
0034711C  mov      rbx, qword ptr [rsp + 0x30]
00347121  add      rsp, 0x20
00347125  pop      rdi
00347126  jmp      0x2e0650  ; -> 002E0650 fn
```
