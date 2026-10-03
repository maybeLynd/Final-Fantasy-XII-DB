# F-interior pack: `22-Middleware-PhyreEngine/Phyre-Asset-Container/the-cluster-header-and-what-the-loader-rejects.md`

Generated 2026-10-02 20:18 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/the-cluster-header-and-what-the-loader-rejects.json`.

Functions: 3. Each is cited on the page only at its entry and is still in the F frontier.

## 00597200 (17 B, extent 00597200-00597211)

Page context: "596FC0') | per-type block readers; each descriptor-table row pairs a reader with its class | | byte-swap / stream ops | '00596890' (1,811 B — '0059FFC0' ×6 + '00597400'/'00597560', tables '005971F0'/'00597200' + '00D27A08'/'00D27A38'), '00599500' ('0063E2E0' ×2 + '00599670'/'00686D00', '02CAA0A0'), '00599670' (254 B — '0063BB10' + '0059B090' + '00861EBA'), '0059FCA0' (108 B — '00584730' only), '0059A3B0' (the CONTRACT subject — '0063E2E"

```
00597200  mov      rax, r8
00597203  mov      dword ptr [rcx + 4], edx
00597206  mov      rdx, rax
00597209  mov      r8d, r9d
0059720C  jmp      0x59ffc0  ; -> 0059FFC0 fn
```

## 00597F30 (78 B, extent 00597F30-00597F7E)

Page context: "l - the intrusive-list '_next'. Interior anchor '0067FF6C' (the encoded-link load).  '0067F6F0' (13 B) self-links the three pointers at '+0x18', '+0x20' and '+0x28' to 'rcx' - the sentinel head init '00597F30', '0059F7A0', '005AA080', '005C22B0' and '005C35A0' all run. Interior anchor '0067F6F4' (the '+0x20' store).  ## SWE2-EC7-121 update (2026-09-21) - three '00639510' callees measured  '00639750' (48 B) is the aligned bump-allocator "

```
00597F30  push     rdi
00597F32  sub      rsp, 0x30
00597F36  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
00597F3F  mov      qword ptr [rsp + 0x40], rbx
00597F44  mov      rdi, rcx
00597F47  call     0x67f6f0  ; -> 0067F6F0 fn
00597F4C  nop      
00597F4D  lea      rcx, [rdi + 0x30]
00597F51  call     0x6803d0  ; -> 006803D0 fn
00597F56  nop      
00597F57  lea      rcx, [rdi + 0x30]
00597F5B  call     0x680030  ; -> 00680030 fn
00597F60  nop      
00597F61  mov      rcx, rdi
00597F64  call     0x67f580  ; -> 0067F580 fn
00597F69  nop      
00597F6A  mov      rcx, rdi
00597F6D  call     0x67f580  ; -> 0067F580 fn
00597F72  nop      
00597F73  mov      rbx, qword ptr [rsp + 0x40]
00597F78  add      rsp, 0x30
00597F7C  pop      rdi
00597F7D  ret      
```

## 005AA080 (64 B, extent 005AA080-005AA0C0)

Page context: "_next'. Interior anchor '0067FF6C' (the encoded-link load).  '0067F6F0' (13 B) self-links the three pointers at '+0x18', '+0x20' and '+0x28' to 'rcx' - the sentinel head init '00597F30', '0059F7A0', '005AA080', '005C22B0' and '005C35A0' all run. Interior anchor '0067F6F4' (the '+0x20' store).  ## SWE2-EC7-121 update (2026-09-21) - three '00639510' callees measured  '00639750' (48 B) is the aligned bump-allocator on the '+0x48' block: th"

```
005AA080  push     rdi
005AA082  sub      rsp, 0x30
005AA086  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
005AA08F  mov      qword ptr [rsp + 0x40], rbx
005AA094  mov      rbx, rcx
005AA097  add      rcx, 0x10
005AA09B  call     0x67f6f0  ; -> 0067F6F0 fn
005AA0A0  nop      
005AA0A1  mov      rcx, qword ptr [rbx + 8]
005AA0A5  call     0x584730  ; -> 00584730 fn
005AA0AA  nop      
005AA0AB  lea      rcx, [rbx + 0x10]
005AA0AF  call     0x67f580  ; -> 0067F580 fn
005AA0B4  nop      
005AA0B5  mov      rbx, qword ptr [rsp + 0x40]
005AA0BA  add      rsp, 0x30
005AA0BE  pop      rdi
005AA0BF  ret      
```
