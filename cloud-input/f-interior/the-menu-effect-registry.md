# F-interior pack: `17-Presentation-Rendering/Effect-File-Formats/the-menu-effect-registry.md`

Generated 2026-10-02 10:27 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/the-menu-effect-registry.json`.

Functions: 6. Each is cited on the page only at its entry and is still in the F frontier.

## 00374930 (28 B, extent 00374930-0037494C)

Page context: "C550' (138 B) is the per-kind teardown the registry exposes: 'ecx' in 1..9 ('ecx-1 <= 8') indexes a four-arm jump table at '0x12C5DC' whose precondition calls are '002FBEF0', '003B0130', '003B1310', '00374930'; then the '020910A0 + ecx*8' bucket's '+8'-linked list is drained through '0024F410' per node, the slot head cleared, and a tail 'jmp 0024C460' finishes. Interior anchor '0024C5B4' (the 'call 0024F410' per-node release).  ## SWE2-"

```
00374930  lea      rax, [rip + 0x2b4b111]  ; -> 02EBFA48
00374937  xor      ecx, ecx
00374939  lea      rdx, [rip + 0x2b4bf08]  ; -> 02EC0848
00374940  mov      dword ptr [rax], ecx
00374942  add      rax, 0x70
00374946  cmp      rax, rdx
00374949  jl       0x374940  ; -> 00374940
0037494B  ret      
```

## 003A7420 (56 B, extent 003A7420-003A7458)

Page context: "0'/'0032E520'/'003B21E0'/'0032E590'/'0024F410'/'0024EE10'. Interior anchor '003B1336' (a '0036C1D0' call).  ## SWE2-EC7-46 update (2026-09-19) - '0024D050'  '0024D050' (233 B) is a body - '0024FCF0'/'003A7420'. Interior anchor '0024D102' (a '0024FCF0' call).  ## SWE2-EC7-47 update (2026-09-19) - '00558A10'  '00558A10' (215 B) is a body - '00558960' single call. Interior anchor '00558A4A' (the '00558960' call).  ## SWE2-EC7-50 update (20"

```
003A7420  push     rbx
003A7422  sub      rsp, 0x20
003A7426  xor      ebx, ebx
003A7428  nop      dword ptr [rax + rax]
003A7430  mov      rax, qword ptr [rip + 0x2b17b79]  ; -> 02EBEFB0
003A7437  mov      rcx, qword ptr [rbx + rax]
003A743B  test     rcx, rcx
003A743E  je       0x3a7445  ; -> 003A7445
003A7440  call     0x332fa0  ; -> 00332FA0 fn
003A7445  add      rbx, 8
003A7449  cmp      rbx, 0x80
003A7450  jl       0x3a7430  ; -> 003A7430
003A7452  add      rsp, 0x20
003A7456  pop      rbx
003A7457  ret      
```

## 00460120 (80 B, extent 00460120-00460170)

Page context: "by ten thousand, the shape of a duration or phase in the effect walk's units. The element-type pages read '+0x338' of OTHER effect objects as a pointer pushed to the deferred-free queue ('005294B0', '00460120'), so the field's meaning is per object kind and this instance's own reader is the missing half: a displacement census of '+0x338' over the effect walk's bodies, restricted to the '0024B270'-created instance, not done.*       ***AN"

```
00460120  push     rbx
00460122  sub      rsp, 0x20
00460126  mov      rbx, rcx
00460129  mov      rcx, qword ptr [rcx + 0x338]
00460130  test     rcx, rcx
00460133  je       0x46013a  ; -> 0046013A
00460135  call     0x3697f0  ; -> 003697F0 fn
0046013A  mov      rcx, qword ptr [rbx + 0x3d0]
00460141  test     rcx, rcx
00460144  je       0x46014b  ; -> 0046014B
00460146  call     0x3697f0  ; -> 003697F0 fn
0046014B  test     byte ptr [rbx + 0x3c0], 1
00460152  je       0x46016a  ; -> 0046016A
00460154  mov      rcx, qword ptr [rbx + 0x3b0]
0046015B  test     rcx, rcx
0046015E  je       0x46016a  ; -> 0046016A
00460160  add      rsp, 0x20
00460164  pop      rbx
00460165  jmp      0x24b1c0  ; -> 0024B1C0 fn
0046016A  add      rsp, 0x20
0046016E  pop      rbx
0046016F  ret      
```

## 0050D9A0 (84 B, extent 0050D9A0-0050D9F4)

Page context: "ame commit '00247510' the page cites; this is shared UI-effect machinery, not a save route into the registry.  **Script_VM_Native_Bridge — CLIENT (4 edges).** The verb bodies '0034DB30', '0050D0C0', '0050D9A0' and '0050E1E0' call '0032E520'. Script verbs ask whether the keyed-slot table is busy (or drain it); that is fan-in on a generic wait, not a script route into the registry.  **World and WorldAreaField — CLIENT and SERVICE (4 edges"

```
0050D9A0  push     rbx
0050D9A2  sub      rsp, 0x20
0050D9A6  mov      rcx, r9
0050D9A9  call     0x267e10  ; -> 00267E10 fn
0050D9AE  mov      ecx, 1
0050D9B3  mov      ebx, eax
0050D9B5  call     0x254cb0  ; -> 00254CB0 fn
0050D9BA  call     0x266d00  ; -> 00266D00 fn
0050D9BF  mov      ecx, ebx
0050D9C1  call     0x2ef300  ; -> 002EF300 fn
0050D9C6  xor      ecx, ecx
0050D9C8  call     0x32e520  ; -> 0032E520 fn
0050D9CD  xor      ecx, ecx
0050D9CF  call     0x254cb0  ; -> 00254CB0 fn
0050D9D4  call     0x36fcc0  ; -> 0036FCC0 fn
0050D9D9  xor      ebx, ebx
0050D9DB  nop      dword ptr [rax + rax]
0050D9E0  mov      ecx, ebx
0050D9E2  call     0x26b8e0  ; -> 0026B8E0 fn
0050D9E7  inc      ebx
0050D9E9  cmp      ebx, 3
0050D9EC  jle      0x50d9e0  ; -> 0050D9E0
0050D9EE  add      rsp, 0x20
0050D9F2  pop      rbx
0050D9F3  ret      
```

## 005294B0 (63 B, extent 005294B0-005294EF)

Page context: "byte scaled by ten thousand, the shape of a duration or phase in the effect walk's units. The element-type pages read '+0x338' of OTHER effect objects as a pointer pushed to the deferred-free queue ('005294B0', '00460120'), so the field's meaning is per object kind and this instance's own reader is the missing half: a displacement census of '+0x338' over the effect walk's bodies, restricted to the '0024B270'-created instance, not done.*"

```
005294B0  push     rbx
005294B2  sub      rsp, 0x20
005294B6  mov      rbx, rcx
005294B9  mov      rcx, qword ptr [rcx + 0x338]
005294C0  test     rcx, rcx
005294C3  je       0x5294ca  ; -> 005294CA
005294C5  call     0x24b1c0  ; -> 0024B1C0 fn
005294CA  test     byte ptr [rbx + 0x3c0], 1
005294D1  je       0x5294e9  ; -> 005294E9
005294D3  mov      rcx, qword ptr [rbx + 0x3b0]
005294DA  test     rcx, rcx
005294DD  je       0x5294e9  ; -> 005294E9
005294DF  add      rsp, 0x20
005294E3  pop      rbx
005294E4  jmp      0x24b1c0  ; -> 0024B1C0 fn
005294E9  add      rsp, 0x20
005294ED  pop      rbx
005294EE  ret      
```

## 0057E950 (238 B, extent 0057E950-0057EA3E)

Page context: "_FullImageStorageCompletionCallback' '00580840', 'SaveSlotScan_ControllerCallback' '005819F0', 'SaveSlotProbe_StorageCompletionCallback' '00581B70', 'SaveLoad_ControllerLifecycleHandler' '00582860', '0057E950' and '0057EBB0'. A save-layer body binds and queries the shared effect object with the same get-bind-query-release shape as the achievements pane's init (SWE2-EC7-106 update), and the save and slot-scan callbacks call the same comm"

```
0057E950  push     rbx
0057E952  sub      rsp, 0xe0
0057E959  mov      rax, qword ptr [rip + 0x19c5ed0]  ; -> 01F44830 [u64 0x00002B992DDFA232]
0057E960  xor      rax, rsp
0057E963  mov      qword ptr [rsp + 0xd0], rax
0057E96B  mov      ebx, r8d
0057E96E  sub      ecx, 4
0057E971  je       0x57e997  ; -> 0057E997
0057E973  cmp      ecx, 1
0057E976  jne      0x57ea25  ; -> 0057EA25
0057E97C  mov      rax, qword ptr [rip + 0x272b03d]  ; -> 02CA99C0
0057E983  mov      dword ptr [rsp + 0x80], 0xd
0057E98E  test     rax, rax
0057E991  jne      0x57e9f0  ; -> 0057E9F0
0057E993  mov      al, 0xff
0057E995  jmp      0x57e9f7  ; -> 0057E9F7
0057E997  test     edx, edx
0057E999  jne      0x57e97c  ; -> 0057E97C
0057E99B  test     byte ptr [rbx + 0xc0], 2
0057E9A2  je       0x57e97c  ; -> 0057E97C
0057E9A4  mov      edx, 0x40
0057E9A9  lea      rcx, [rsp + 0x90]
0057E9B1  call     0x393630  ; -> 00393630 fn
0057E9B6  mov      rcx, qword ptr [rip + 0x272b003]  ; -> 02CA99C0
0057E9BD  test     rcx, rcx
0057E9C0  je       0x57ea25  ; -> 0057EA25
0057E9C2  mov      dword ptr [rsp + 0x20], 5
0057E9CA  xor      eax, eax
0057E9CC  nop      dword ptr [rax]
0057E9D0  movzx    edx, byte ptr [rsp + rax + 0x90]
0057E9D8  mov      byte ptr [rsp + rax + 0x28], dl
0057E9DC  lea      rax, [rax + 1]
0057E9E0  test     dl, dl
0057E9E2  jne      0x57e9d0  ; -> 0057E9D0
0057E9E4  lea      rdx, [rsp + 0x20]
0057E9E9  call     0x582540  ; -> 00582540 fn
0057E9EE  jmp      0x57ea25  ; -> 0057EA25
0057E9F0  movzx    eax, byte ptr [rax + 0x39a]
0057E9F7  mov      rcx, qword ptr [rbx + 0xc8]
0057E9FE  lea      r8, [rsp + 0x80]
0057EA06  mov      dword ptr [rsp + 0x88], edx
0057EA0D  mov      edx, 0x1d
0057EA12  mov      byte ptr [rsp + 0x84], al
0057EA19  call     0x247510  ; -> 00247510 fn
0057EA1E  and      dword ptr [rbx + 0xc0], 0xfffffffe
0057EA25  mov      rcx, qword ptr [rsp + 0xd0]
0057EA2D  xor      rcx, rsp
0057EA30  call     0x808c40  ; -> 00808C40 fn
0057EA35  add      rsp, 0xe0
0057EA3C  pop      rbx
0057EA3D  ret      
```
