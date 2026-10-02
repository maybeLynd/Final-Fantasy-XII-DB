# F-interior pack: `12-Items-Equipment-Shops-License/license-board-grid-format.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/license-board-grid-format.json`.

Functions: 2. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: bafa49c9f	SWE2-DATA: bucket member formats declared - 53 .bin + 5 .dat members, every entry assigned, each cla; c9b951983	EC7 pass-22 debt: crossing-section dispositions - 527 pairs / 65 pages (FRONTIER-REQ-SWE2-EC7-PASS22; inbox mentions: repos-c7.md). OPUS read these before packing.

## 003FDAD0 (769 B, extent 003FDAD0-003FDDD1)

Page context: "urce: '00259DF0', '002DF9A0', '0032EAE0' - shared machinery across the layer boundary, no shared ownership. - **UI - CLIENT (12 edges).** '002527B0' is also called by bodies filed to UI: '00280DE0', '003FDAD0', '005651E0' (Widget) - shared machinery across the layer boundary, no shared ownership. - **World - SERVICE (1 edge).** '0022A0B0' reaches bodies filed to World: '00266D10' (NativeSupport) - shared machinery across the layer bound"

```
003FDAD0  mov      qword ptr [rsp + 0x18], rbp
003FDAD5  mov      qword ptr [rsp + 0x20], rsi
003FDADA  push     rdi
003FDADB  push     r12
003FDADD  push     r14
003FDADF  sub      rsp, 0x30
003FDAE3  movzx    r14d, word ptr [rip + 0x2b9987f]  ; -> 02F9736A
003FDAEB  mov      rdi, rcx
003FDAEE  mov      rcx, qword ptr [rcx + 0xd8]
003FDAF5  mov      edx, 1
003FDAFA  movzx    ebp, word ptr [rip + 0x2b9986b]  ; -> 02F9736C
003FDB01  movzx    esi, word ptr [rip + 0x2b99860]  ; -> 02F97368
003FDB08  call     0x2d45c0  ; -> 002D45C0 fn
003FDB0D  mov      r8, qword ptr [rdi + 0xd8]
003FDB14  xor      r12d, r12d
003FDB17  mov      edx, r12d
003FDB1A  cmp      qword ptr [rdi + 0xe0], rdx
003FDB21  mov      eax, dword ptr [r8 + 0xe0]
003FDB28  setne    dl
003FDB2B  shl      edx, 0x1b
003FDB2E  btr      eax, 0x1b
003FDB32  or       edx, eax
003FDB34  mov      dword ptr [r8 + 0xe0], edx
003FDB3B  call     0x2445c0  ; -> 002445C0 fn
003FDB40  mov      rax, qword ptr [rip + 0x1c9d0e9]  ; -> 0209AC30
003FDB47  movsx    ecx, word ptr [rax + 0xde0]
003FDB4E  call     0x282df0  ; -> 00282DF0 fn
003FDB53  mov      r9d, esi
003FDB56  mov      dword ptr [rsp + 0x20], ebp
003FDB5A  xor      r8d, r8d
003FDB5D  mov      edx, r14d
003FDB60  mov      rcx, rax
003FDB63  call     0x2c1a80  ; -> 002C1A80 fn
003FDB68  test     eax, eax
003FDB6A  je       0x3fdb94  ; -> 003FDB94
003FDB6C  mov      rcx, qword ptr [rdi + 0xd8]
003FDB73  xor      edx, edx
003FDB75  call     0x2d45c0  ; -> 002D45C0 fn
003FDB7A  mov      rax, qword ptr [rdi + 0xd8]
003FDB81  and      dword ptr [rax + 0xe0], 0xf7ffffff
003FDB8B  call     0x2445c0  ; -> 002445C0 fn
003FDB90  xor      eax, eax
003FDB92  jmp      0x3fdbf8  ; -> 003FDBF8
003FDB94  mov      qword ptr [rsp + 0x50], rbx
003FDB99  mov      ebx, dword ptr [rdi + 0x180]
003FDB9F  mov      ecx, ebx
003FDBA1  shl      ecx, 0xb
003FDBA4  sar      ecx, 0x1b
003FDBA7  mov      qword ptr [rsp + 0x58], r15
003FDBAC  cmp      ecx, 1
003FDBAF  jle      0x3fdbe0  ; -> 003FDBE0
003FDBB1  shl      ebx, 6
003FDBB4  and      esi, 0xca0
003FDBBA  sar      ebx, 0x1b
003FDBBD  movsxd   r15, ebx
003FDBC0  add      r15, 0x1e
003FDBC4  lea      r15, [rdi + r15*8]
003FDBC8  cmp      esi, 0x400
003FDBCE  jne      0x3fdc0c  ; -> 003FDC0C
003FDBD0  test     esi, ebp
003FDBD2  jne      0x3fdc19  ; -> 003FDC19
003FDBD4  cmp      esi, 0x800
003FDBDA  jne      0x3fdc3a  ; -> 003FDC3A
003FDBDC  test     esi, ebp
003FDBDE  jne      0x3fdc44  ; -> 003FDC44
003FDBE0  mov      rcx, qword ptr [rdi + 0xd8]
003FDBE7  call     0x2d3900  ; -> 002D3900 fn
003FDBEC  xor      eax, eax
003FDBEE  mov      rbx, qword ptr [rsp + 0x50]
003FDBF3  mov      r15, qword ptr [rsp + 0x58]
003FDBF8  mov      rbp, qword ptr [rsp + 0x60]
003FDBFD  mov      rsi, qword ptr [rsp + 0x68]
003FDC02  add      rsp, 0x30
003FDC06  pop      r14
003FDC08  pop      r12
003FDC0A  pop      rdi
003FDC0B  ret      
003FDC0C  cmp      esi, 0x80
003FDC12  jne      0x3fdbd4  ; -> 003FDBD4
003FDC14  test     bpl, bpl
003FDC17  jns      0x3fdbd4  ; -> 003FDBD4
003FDC19  test     ebx, ebx
003FDC1B  jle      0x3fdc27  ; -> 003FDC27
003FDC1D  mov      rcx, rdi
003FDC20  call     0x563ec0  ; -> 00563EC0 fn
003FDC25  jmp      0x3fdc5c  ; -> 003FDC5C
003FDC27  test     r14d, 0x480
003FDC2E  je       0x3fdc5c  ; -> 003FDC5C
003FDC30  mov      rcx, rdi
003FDC33  call     0x563ec0  ; -> 00563EC0 fn
003FDC38  jmp      0x3fdc5c  ; -> 003FDC5C
003FDC3A  cmp      esi, 0x20
003FDC3D  jne      0x3fdbe0  ; -> 003FDBE0
003FDC3F  test     sil, bpl
003FDC42  je       0x3fdbe0  ; -> 003FDBE0
003FDC44  lea      eax, [rcx - 1]
003FDC47  cmp      ebx, eax
003FDC49  jl       0x3fdc54  ; -> 003FDC54
003FDC4B  test     r14d, 0x820
003FDC52  je       0x3fdc5c  ; -> 003FDC5C
003FDC54  mov      rcx, rdi
003FDC57  call     0x564300  ; -> 00564300 fn
003FDC5C  mov      eax, dword ptr [rdi + 0x180]
003FDC62  shl      eax, 6
003FDC65  sar      eax, 0x1b
003FDC68  cmp      ebx, eax
003FDC6A  je       0x3fdbe0  ; -> 003FDBE0
003FDC70  mov      r8, qword ptr [rdi + 0xe0]
003FDC77  test     r8, r8
003FDC7A  je       0x3fdcbd  ; -> 003FDCBD
003FDC7C  mov      rcx, qword ptr [rdi + 0xd8]
003FDC83  movsx    eax, word ptr [rcx + 0xf2]
003FDC8A  movsx    edx, word ptr [rcx + 0xf4]
003FDC91  add      edx, eax
003FDC93  movzx    eax, byte ptr [rcx + 0xec]
003FDC9A  imul     edx, eax
003FDC9D  movsx    eax, byte ptr [rcx + 0xee]
003FDCA4  add      edx, eax
003FDCA6  movsx    eax, byte ptr [rcx + 0xed]
003FDCAD  add      eax, edx
003FDCAF  cdqe     
003FDCB1  shl      rax, 5
003FDCB5  movzx    eax, word ptr [rax + r8 + 8]
003FDCBB  jmp      0x3fdcc2  ; -> 003FDCC2
003FDCBD  mov      eax, 0xffff
003FDCC2  mov      word ptr [r15], ax
003FDCC6  mov      rdx, qword ptr [rdi + 0xd8]
003FDCCD  movsx    ecx, word ptr [rdx + 0xf2]
003FDCD4  movsx    eax, byte ptr [rdx + 0xee]
003FDCDB  movzx    r8d, byte ptr [rdx + 0xec]
003FDCE3  imul     r8d, ecx
003FDCE7  mov      ecx, 8
003FDCEC  add      r8w, ax
003FDCF0  movsx    eax, byte ptr [rdx + 0xed]
003FDCF7  add      r8w, ax
003FDCFB  mov      word ptr [r15 + 2], r8w
003FDD00  mov      r9, qword ptr [rdi + 0xd8]
003FDD07  movzx    edx, word ptr [r9 + 0xf4]
003FDD0F  add      dx, word ptr [r9 + 0xf2]
003FDD17  movzx    eax, byte ptr [r9 + 0xec]
003FDD1F  movsx    r8d, dx
003FDD23  movsx    edx, byte ptr [r15 + 7]
003FDD28  imul     r8d, eax
003FDD2C  add      edx, 0x20
003FDD2F  movsx    eax, byte ptr [r9 + 0xee]
003FDD37  add      r8w, ax
003FDD3B  movsx    eax, byte ptr [r9 + 0xed]
003FDD43  add      r8w, ax
003FDD47  mov      word ptr [r15 + 4], r8w
003FDD4C  movzx    r8d, word ptr [r15]
003FDD50  call     0x2527b0  ; -> 002527B0 fn
003FDD55  mov      eax, dword ptr [rdi + 0x180]
003FDD5B  xor      r8d, r8d
003FDD5E  shl      eax, 6
003FDD61  movsxd   rcx, eax
003FDD64  sar      rcx, 0x1b
003FDD68  lea      rbx, [rdi + rcx*8]
003FDD6C  mov      rcx, rdi
003FDD6F  lea      rdx, [rbx + 0xf0]
003FDD76  call     0x5655f0  ; -> 005655F0 fn
003FDD7B  mov      rcx, qword ptr [rdi + 0xc8]
003FDD82  lea      rdx, [rbx + 0xf0]
003FDD89  call     0x5674b0  ; -> 005674B0 fn
003FDD8E  cmp      qword ptr [rdi + 0xe0], r12
003FDD95  mov      rdx, qword ptr [rdi + 0xd8]
003FDD9C  setne    r12b
003FDDA0  shl      r12d, 0x1b
003FDDA4  mov      ecx, dword ptr [rdx + 0xe0]
003FDDAA  btr      ecx, 0x1b
003FDDAE  or       r12d, ecx
003FDDB1  mov      dword ptr [rdx + 0xe0], r12d
003FDDB8  call     0x2445c0  ; -> 002445C0 fn
003FDDBD  mov      ecx, 0xa
003FDDC2  call     0x249c60  ; -> 00249C60 fn
003FDDC7  mov      eax, 1
003FDDCC  jmp      0x3fdbee  ; -> 003FDBEE
```

## 00511F50 (61 B, extent 00511F50-00511F8D)

Page context: "S); **six functions read cells** with the row-major formula in the table above — '00328990' (called from '00328BD0'), '0055E2C0' and '0055E600' (both called from '0055C530'), '00560070' (called from '00511F50'), '0055F830', and '003FC900', which then indexes the licence data table '02EBF038' by the cell value ('003FC9E8'–'003FC9F0'). *The first pass of this census tracked the blob pointer by register and lost it where '0055F830' and '00"

```
00511F50  push     rdi
00511F52  sub      rsp, 0x20
00511F56  mov      rdi, r9
00511F59  call     0x280120  ; -> 00280120 fn
00511F5E  test     eax, eax
00511F60  jne      0x511f87  ; -> 00511F87
00511F62  mov      rcx, rdi
00511F65  mov      qword ptr [rsp + 0x30], rbx
00511F6A  call     0x267e10  ; -> 00267E10 fn
00511F6F  mov      rcx, rdi
00511F72  mov      ebx, eax
00511F74  call     0x267e10  ; -> 00267E10 fn
00511F79  mov      edx, ebx
00511F7B  mov      ecx, eax
00511F7D  call     0x560070  ; -> 00560070 fn
00511F82  mov      rbx, qword ptr [rsp + 0x30]
00511F87  add      rsp, 0x20
00511F8B  pop      rdi
00511F8C  ret      
```
