# F-interior pack: `04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md`

Generated 2026-10-02 09:51 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/the-record-00329220-builds.json`.

Functions: 17. Each is cited on the page only at its entry and is still in the F frontier.

## 00273380 (135 B, extent 00273380-00273407)

Page context: "ndex*0xA8' into 'rbx') stored into the four 32-qword status order tables rooted at '+0x1508'/'+0x1608'/'+0x1708'/'+0x1808' ('+0x1500'..'+0x18FF') - the ordered-status tables the readers ('00273160', '00273380', '00271FB0', '00273410', '00272F80') index by listing key (corrected 2026-09-27, GA-1: earlier called a "link table" and "neighbour table"; the four tables are status order lists, each built with '002D02C0' kind 1-4).  Interior an"

```
00273380  mov      qword ptr [rsp + 8], rbx
00273385  push     rdi
00273386  sub      rsp, 0x20
0027338A  mov      ebx, edx
0027338C  mov      edi, ecx
0027338E  test     ecx, ecx
00273390  je       0x2733ec  ; -> 002733EC
00273392  call     0x35d490  ; -> 0035D490 fn
00273397  sub      ebx, 1
0027339A  je       0x2733bb  ; -> 002733BB
0027339C  sub      ebx, 1
0027339F  je       0x2733b4  ; -> 002733B4
002733A1  cmp      ebx, 1
002733A4  je       0x2733ad  ; -> 002733AD
002733A6  mov      ecx, 0x1500
002733AB  jmp      0x2733c0  ; -> 002733C0
002733AD  mov      ecx, 0x1800
002733B2  jmp      0x2733c0  ; -> 002733C0
002733B4  mov      ecx, 0x1600
002733B9  jmp      0x2733c0  ; -> 002733C0
002733BB  mov      ecx, 0x1700
002733C0  lea      rdx, [rcx + rax]
002733C4  xor      ecx, ecx
002733C6  nop      word ptr [rax + rax]
002733D0  mov      r8, qword ptr [rdx]
002733D3  mov      eax, dword ptr [r8 + 0x98]
002733DA  bt       edi, eax
002733DD  jb       0x2733f9  ; -> 002733F9
002733DF  inc      rcx
002733E2  add      rdx, 8
002733E6  cmp      rcx, 0x20
002733EA  jl       0x2733d0  ; -> 002733D0
002733EC  xor      eax, eax
002733EE  mov      rbx, qword ptr [rsp + 0x30]
002733F3  add      rsp, 0x20
002733F7  pop      rdi
002733F8  ret      
002733F9  mov      rax, r8
002733FC  mov      rbx, qword ptr [rsp + 0x30]
00273401  add      rsp, 0x20
00273405  pop      rdi
00273406  ret      
```

## 00273410 (76 B, extent 00273410-0027345C)

Page context: "rce-side helper, not a shared responsibility. **UI — CLIENT (SWE2-EC7-156, 242 edges).** '002A0440' calls '00181560', '002915C0'/'002917E0'/'002C7660' call '00202C90'; batch-121's '00272F80' helpers '00273410'/'00275E40'/'003178C0' join the same fan-in — the interface layer consults this page's functions, not a shared responsibility.  **Script_VM_Native_Bridge — MECHANICAL (SWE2-EC7-175, 15 edges).** '003588B0' and '00263B80', helpers t"

```
00273410  push     rbx
00273412  sub      rsp, 0x20
00273416  mov      ebx, ecx
00273418  call     0x35d490  ; -> 0035D490 fn
0027341D  sub      ebx, 1
00273420  je       0x273450  ; -> 00273450
00273422  sub      ebx, 1
00273425  je       0x273444  ; -> 00273444
00273427  cmp      ebx, 1
0027342A  je       0x273438  ; -> 00273438
0027342C  add      rax, 0x1500
00273432  add      rsp, 0x20
00273436  pop      rbx
00273437  ret      
00273438  add      rax, 0x1800
0027343E  add      rsp, 0x20
00273442  pop      rbx
00273443  ret      
00273444  add      rax, 0x1600
0027344A  add      rsp, 0x20
0027344E  pop      rbx
0027344F  ret      
00273450  add      rax, 0x1700
00273456  add      rsp, 0x20
0027345A  pop      rbx
0027345B  ret      
```

## 002915C0 (389 B, extent 002915C0-00291745)

Page context: "** '00181350' calls '001B06D0' and is called by '0022FFE0'/'00274CB0'/'003C7xxx' of that layer — a two-way render-helper exchange, not a second owner. **Resource — SERVICE (SWE2-EC7-156, 2 edges).** '002915C0'/'002917E0' call '0024A5A0' of that layer — the record's helpers consume a resource-side helper, not a shared responsibility. **UI — CLIENT (SWE2-EC7-156, 242 edges).** '002A0440' calls '00181560', '002915C0'/'002917E0'/'002C7660' "

```
002915C0  push     rbp
002915C2  push     rsi
002915C3  push     rdi
002915C4  push     r14
002915C6  sub      rsp, 0x48
002915CA  mov      rax, qword ptr [rip + 0x1cb325f]  ; -> 01F44830 [u64 0x00002B992DDFA232]
002915D1  xor      rax, rsp
002915D4  mov      qword ptr [rsp + 0x30], rax
002915D9  mov      rax, qword ptr [rcx + 0x10f20]
002915E0  mov      edi, r9d
002915E3  mov      rbp, r8
002915E6  mov      r14d, edx
002915E9  mov      rsi, rcx
002915EC  test     rax, rax
002915EF  je       0x291609  ; -> 00291609
002915F1  cmp      dword ptr [rax + 0x980], edi
002915F7  je       0x29172e  ; -> 0029172E
002915FD  mov      rax, qword ptr [rax + 0x9b0]
00291604  test     rax, rax
00291607  jne      0x2915f1  ; -> 002915F1
00291609  mov      rdx, qword ptr [rip + 0x1e0a870]  ; -> 0209BE80
00291610  mov      r8d, 0x9d0
00291616  xor      ecx, ecx
00291618  mov      qword ptr [rsp + 0x40], rbx
0029161D  mov      rdx, qword ptr [rdx + 0x10fc0]
00291624  call     0x273a30  ; -> 00273A30 fn
00291629  mov      rbx, rax
0029162C  test     rax, rax
0029162F  je       0x291729  ; -> 00291729
00291635  mov      edx, 0x9d0
0029163A  mov      rcx, rax
0029163D  call     0x275550  ; -> 00275550 fn
00291642  mov      edx, 0x9d0
00291647  mov      rcx, rbx
0029164A  call     0x275550  ; -> 00275550 fn
0029164F  lea      rcx, [rbx + 0x960]
00291656  test     rbp, rbp
00291659  je       0x291665  ; -> 00291665
0029165B  mov      rdx, rbp
0029165E  call     0x202c90  ; -> 00202C90 fn
00291663  jmp      0x291679  ; -> 00291679
00291665  or       byte ptr [rbx + 0x991], 2
0029166C  mov      edx, edi
0029166E  mov      dword ptr [rbx + 0x980], edi
00291674  call     0x2713e0  ; -> 002713E0 fn
00291679  cmp      dword ptr [rsp + 0x90], 0
00291681  mov      byte ptr [rbx + 0x990], r14b
00291688  je       0x291691  ; -> 00291691
0029168A  or       byte ptr [rbx + 0x991], 4
00291691  movss    xmm0, dword ptr [rsp + 0x98]
0029169A  movss    dword ptr [rbx + 0x9a8], xmm0
002916A2  cmp      qword ptr [rsi + 0x10f50], 0
002916AA  jne      0x2916bf  ; -> 002916BF
002916AC  mov      rcx, qword ptr [rip + 0x1b7ab2d]  ; -> 01E0C1E0 [u64 0x00000000009152A0]
002916B3  call     0x24a5a0  ; -> 0024A5A0 fn
002916B8  mov      qword ptr [rsi + 0x10f50], rax
002916BF  mov      r8, qword ptr [rsi + 0x10f50]
002916C6  mov      qword ptr [rbx + 0x988], r8
002916CD  mov      rcx, qword ptr [r8 + 0x20]
002916D1  mov      r8, qword ptr [r8 + 0x30]
002916D5  add      rcx, 0x30
002916D9  movzx    eax, word ptr [rcx + 0x14]
002916DD  movzx    edx, word ptr [rcx + rax*2 + 0x14]
002916E2  movzx    eax, word ptr [rcx + 0x10]
002916E6  add      rcx, rax
002916E9  lea      rdx, [rcx + rdx*8]
002916ED  lea      rcx, [rsp + 0x20]
002916F2  call     0x271140  ; -> 00271140 fn
002916F7  lea      rdx, [rsp + 0x20]
002916FC  mov      rcx, rbx
002916FF  call     0x3f2600  ; -> 003F2600 fn
00291704  mov      eax, 1
00291709  mov      rdx, rbx
0029170C  mov      word ptr [rbx + 0x9c0], ax
00291713  mov      rcx, qword ptr [rsi + 0x10f20]
0029171A  call     0x3f2580  ; -> 003F2580 fn
0029171F  mov      qword ptr [rsi + 0x10f20], rax
00291726  mov      rax, rbx
00291729  mov      rbx, qword ptr [rsp + 0x40]
0029172E  mov      rcx, qword ptr [rsp + 0x30]
00291733  xor      rcx, rsp
00291736  call     0x808c40  ; -> 00808C40 fn
0029173B  add      rsp, 0x48
0029173F  pop      r14
00291741  pop      rdi
00291742  pop      rsi
00291743  pop      rbp
00291744  ret      
```

## 002ED0B0 (125 B, extent 002ED0B0-002ED12D)

Page context: "6-09-30, FABLE, [record](../../_index/candidates/sd125-sd128-fable-0930/README.md)) (caller '002C62B0'): '[rcx+0x1D78]' context, '0035D4F0' getter, '00272DE0' ('003588B0'+'002E7E90'), '00263C20' x2, '002ED0B0', '0037C8F0', '0035BAD0' x2, '00273460', then workbench '00202C90' x4/'00203080' — calls '002C7B10'. Interior verified 2026-09-17 (SWE2-FRONTIER): '00272DE0' first at ['002C76C4'](../../_index/ADDRESS-INDEX.md). Its callee '002C7B1"

```
002ED0B0  mov      qword ptr [rsp + 8], rbx
002ED0B5  push     rdi
002ED0B6  sub      rsp, 0x20
002ED0BA  mov      rbx, r8
002ED0BD  mov      rdi, rdx
002ED0C0  call     0x3588b0  ; -> 003588B0 fn
002ED0C5  test     rax, rax
002ED0C8  je       0x2ed116  ; -> 002ED116
002ED0CA  mov      rax, qword ptr [rax + 0xc0]
002ED0D1  test     rax, rax
002ED0D4  je       0x2ed116  ; -> 002ED116
002ED0D6  cmp      dword ptr [rax], -1
002ED0D9  je       0x2ed116  ; -> 002ED116
002ED0DB  movzx    ecx, word ptr [rax]
002ED0DE  cmp      cx, -1
002ED0E2  je       0x2ed122  ; -> 002ED122
002ED0E4  movsx    rax, cx
002ED0E8  imul     rcx, rax, 0x740
002ED0EF  add      rcx, qword ptr [rip + 0x1fd9e32]  ; -> 022C6F28
002ED0F6  je       0x2ed122  ; -> 002ED122
002ED0F8  cmp      dword ptr [rcx + 0x284], 0
002ED0FF  je       0x2ed122  ; -> 002ED122
002ED101  mov      r8, rbx
002ED104  mov      rdx, rdi
002ED107  mov      rbx, qword ptr [rsp + 0x30]
002ED10C  add      rsp, 0x20
002ED110  pop      rdi
002ED111  jmp      0x3e4ea0  ; -> 003E4EA0 fn
002ED116  mov      dword ptr [rdi], 1
002ED11C  mov      dword ptr [rbx], 0
002ED122  mov      rbx, qword ptr [rsp + 0x30]
002ED127  add      rsp, 0x20
002ED12B  pop      rdi
002ED12C  ret      
```

## 0031FC10 (85 B, extent 0031FC10-0031FC65)

Page context: "d's per-slot flag query.  Interior anchor '003178D2' (function '003178C0').  '002C8310' (449 B) is the field-map op '002C7660' calls: 'r8w' gates, '003F0040' resolves the fifth stack arg into 'r14', '0031FC10'/'00320640' bounds come back in 'ebx'/'rcx' with 'cmovle' taking the smaller, then '002C5F90'/'002C69A0'/'0035D3D0'/'003F1290'/'00202B10' run the range walk - the record's bounded field pass.  Interior anchor '002C833F' (function '"

```
0031FC10  sub      rsp, 0x28
0031FC14  test     rcx, rcx
0031FC17  je       0x31fc5d  ; -> 0031FC5D
0031FC19  call     0x263e30  ; -> 00263E30 fn
0031FC1E  test     rax, rax
0031FC21  je       0x31fc5d  ; -> 0031FC5D
0031FC23  mov      rax, qword ptr [rax + 0x698]
0031FC2A  test     rax, rax
0031FC2D  je       0x31fc5d  ; -> 0031FC5D
0031FC2F  mov      ecx, dword ptr [rax + 0x64]
0031FC32  or       ecx, dword ptr [rax + 0x3c]
0031FC35  bt       ecx, 0x10
0031FC39  jae      0x31fc4d  ; -> 0031FC4D
0031FC3B  mov      eax, dword ptr [rax + 0x48]
0031FC3E  mov      ecx, 1
0031FC43  cmp      eax, ecx
0031FC45  cmovl    eax, ecx
0031FC48  add      rsp, 0x28
0031FC4C  ret      
0031FC4D  mov      eax, dword ptr [rax + 0x24]
0031FC50  bt       ecx, 0x1c
0031FC54  jae      0x31fc60  ; -> 0031FC60
0031FC56  add      eax, eax
0031FC58  add      rsp, 0x28
0031FC5C  ret      
0031FC5D  or       eax, 0xffffffff
0031FC60  add      rsp, 0x28
0031FC64  ret      
```

## 00345800 (46 B, extent 00345800-0034582E)

Page context: "functions, not a shared responsibility.  **Script_VM_Native_Bridge — MECHANICAL (SWE2-EC7-175, 15 edges).** '003588B0' and '00263B80', helpers this page's '002C8820' calls, are reached by '00341CB0'/'00345800'/'00346FA0'/'0034C3D0'/'0034C950'/'0034F800'/'0034FF00'/'00350DD0'/'003516E0'/'00352580'/'003530F0'/'00355830'/'00356570'/'0050E060' and '0034FCC0' of that layer — script-VM bodies share the same object-resolve and field helpers; p"

```
00345800  push     rbx
00345802  sub      rsp, 0x20
00345806  call     0x3590d0  ; -> 003590D0 fn
0034580B  mov      ecx, eax
0034580D  call     0x3588b0  ; -> 003588B0 fn
00345812  xor      ebx, ebx
00345814  test     rax, rax
00345817  je       0x345826  ; -> 00345826
00345819  mov      rcx, rax
0034581C  call     0x264e10  ; -> 00264E10 fn
00345821  test     eax, eax
00345823  setne    bl
00345826  mov      eax, ebx
00345828  add      rsp, 0x20
0034582C  pop      rbx
0034582D  ret      
```

## 00346FA0 (73 B, extent 00346FA0-00346FE9)

Page context: "not a shared responsibility.  **Script_VM_Native_Bridge — MECHANICAL (SWE2-EC7-175, 15 edges).** '003588B0' and '00263B80', helpers this page's '002C8820' calls, are reached by '00341CB0'/'00345800'/'00346FA0'/'0034C3D0'/'0034C950'/'0034F800'/'0034FF00'/'00350DD0'/'003516E0'/'00352580'/'003530F0'/'00355830'/'00356570'/'0050E060' and '0034FCC0' of that layer — script-VM bodies share the same object-resolve and field helpers; pure fan-in,"

```
00346FA0  push     rbx
00346FA2  sub      rsp, 0x20
00346FA6  mov      rcx, r9
00346FA9  call     0x267e10  ; -> 00267E10 fn
00346FAE  mov      ebx, eax
00346FB0  test     eax, eax
00346FB2  js       0x346fc5  ; -> 00346FC5
00346FB4  call     0x2640c0  ; -> 002640C0 fn
00346FB9  mov      rcx, rax
00346FBC  mov      edx, ebx
00346FBE  call     0x358940  ; -> 00358940 fn
00346FC3  jmp      0x346fd1  ; -> 00346FD1
00346FC5  call     0x3590d0  ; -> 003590D0 fn
00346FCA  mov      ecx, eax
00346FCC  call     0x3588b0  ; -> 003588B0 fn
00346FD1  test     rax, rax
00346FD4  je       0x346fe3  ; -> 00346FE3
00346FD6  mov      rcx, rax
00346FD9  add      rsp, 0x20
00346FDD  pop      rbx
00346FDE  jmp      0x3b6f80  ; -> 003B6F80 fn
00346FE3  add      rsp, 0x20
00346FE7  pop      rbx
00346FE8  ret      
```

## 0034C3D0 (75 B, extent 0034C3D0-0034C41B)

Page context: "d responsibility.  **Script_VM_Native_Bridge — MECHANICAL (SWE2-EC7-175, 15 edges).** '003588B0' and '00263B80', helpers this page's '002C8820' calls, are reached by '00341CB0'/'00345800'/'00346FA0'/'0034C3D0'/'0034C950'/'0034F800'/'0034FF00'/'00350DD0'/'003516E0'/'00352580'/'003530F0'/'00355830'/'00356570'/'0050E060' and '0034FCC0' of that layer — script-VM bodies share the same object-resolve and field helpers; pure fan-in, not a shar"

```
0034C3D0  mov      qword ptr [rsp + 8], rbx
0034C3D5  push     rdi
0034C3D6  sub      rsp, 0x20
0034C3DA  mov      rcx, r9
0034C3DD  mov      rdi, rdx
0034C3E0  call     0x267e10  ; -> 00267E10 fn
0034C3E5  mov      ecx, eax
0034C3E7  call     0x3588b0  ; -> 003588B0 fn
0034C3EC  mov      rbx, rax
0034C3EF  test     rax, rax
0034C3F2  je       0x34c410  ; -> 0034C410
0034C3F4  mov      rdx, rax
0034C3F7  mov      rcx, rdi
0034C3FA  call     0x262f50  ; -> 00262F50 fn
0034C3FF  test     eax, eax
0034C401  je       0x34c410  ; -> 0034C410
0034C403  mov      edx, 1
0034C408  mov      rcx, rbx
0034C40B  call     0x35ae10  ; -> 0035AE10 fn
0034C410  mov      rbx, qword ptr [rsp + 0x30]
0034C415  add      rsp, 0x20
0034C419  pop      rdi
0034C41A  ret      
```

## 0034C950 (51 B, extent 0034C950-0034C983)

Page context: "ility.  **Script_VM_Native_Bridge — MECHANICAL (SWE2-EC7-175, 15 edges).** '003588B0' and '00263B80', helpers this page's '002C8820' calls, are reached by '00341CB0'/'00345800'/'00346FA0'/'0034C3D0'/'0034C950'/'0034F800'/'0034FF00'/'00350DD0'/'003516E0'/'00352580'/'003530F0'/'00355830'/'00356570'/'0050E060' and '0034FCC0' of that layer — script-VM bodies share the same object-resolve and field helpers; pure fan-in, not a shared responsi"

```
0034C950  push     rbx
0034C952  sub      rsp, 0x20
0034C956  mov      rcx, r9
0034C959  mov      rbx, rdx
0034C95C  call     0x267e10  ; -> 00267E10 fn
0034C961  mov      ecx, eax
0034C963  call     0x3588b0  ; -> 003588B0 fn
0034C968  test     rax, rax
0034C96B  je       0x34c97d  ; -> 0034C97D
0034C96D  mov      rdx, rax
0034C970  mov      rcx, rbx
0034C973  add      rsp, 0x20
0034C977  pop      rbx
0034C978  jmp      0x262f50  ; -> 00262F50 fn
0034C97D  add      rsp, 0x20
0034C981  pop      rbx
0034C982  ret      
```

## 0034F800 (112 B, extent 0034F800-0034F870)

Page context: "cript_VM_Native_Bridge — MECHANICAL (SWE2-EC7-175, 15 edges).** '003588B0' and '00263B80', helpers this page's '002C8820' calls, are reached by '00341CB0'/'00345800'/'00346FA0'/'0034C3D0'/'0034C950'/'0034F800'/'0034FF00'/'00350DD0'/'003516E0'/'00352580'/'003530F0'/'00355830'/'00356570'/'0050E060' and '0034FCC0' of that layer — script-VM bodies share the same object-resolve and field helpers; pure fan-in, not a shared responsibility.  *A"

```
0034F800  mov      qword ptr [rsp + 8], rbx
0034F805  mov      qword ptr [rsp + 0x10], rsi
0034F80A  push     rdi
0034F80B  sub      rsp, 0x20
0034F80F  mov      rbx, r9
0034F812  mov      rdi, r8
0034F815  mov      rsi, rcx
0034F818  call     0x3590d0  ; -> 003590D0 fn
0034F81D  mov      ecx, eax
0034F81F  call     0x3588b0  ; -> 003588B0 fn
0034F824  test     rax, rax
0034F827  je       0x34f849  ; -> 0034F849
0034F829  mov      r9, rbx
0034F82C  mov      r8, rdi
0034F82F  mov      rdx, rax
0034F832  mov      rcx, rsi
0034F835  mov      rbx, qword ptr [rsp + 0x30]
0034F83A  mov      rsi, qword ptr [rsp + 0x38]
0034F83F  add      rsp, 0x20
0034F843  pop      rdi
0034F844  jmp      0x34ebc0  ; -> 0034EBC0 fn
0034F849  mov      rcx, rbx
0034F84C  call     0x267db0  ; -> 00267DB0 fn
0034F851  mov      rcx, rbx
0034F854  call     0x267db0  ; -> 00267DB0 fn
0034F859  mov      rcx, rbx
0034F85C  mov      rbx, qword ptr [rsp + 0x30]
0034F861  mov      rsi, qword ptr [rsp + 0x38]
0034F866  add      rsp, 0x20
0034F86A  pop      rdi
0034F86B  jmp      0x267db0  ; -> 00267DB0 fn
```

## 0034FF00 (156 B, extent 0034FF00-0034FF9C)

Page context: "tive_Bridge — MECHANICAL (SWE2-EC7-175, 15 edges).** '003588B0' and '00263B80', helpers this page's '002C8820' calls, are reached by '00341CB0'/'00345800'/'00346FA0'/'0034C3D0'/'0034C950'/'0034F800'/'0034FF00'/'00350DD0'/'003516E0'/'00352580'/'003530F0'/'00355830'/'00356570'/'0050E060' and '0034FCC0' of that layer — script-VM bodies share the same object-resolve and field helpers; pure fan-in, not a shared responsibility.  *Added 2026-0"

```
0034FF00  mov      qword ptr [rsp + 8], rbx
0034FF05  mov      qword ptr [rsp + 0x10], rbp
0034FF0A  mov      qword ptr [rsp + 0x18], rsi
0034FF0F  push     rdi
0034FF10  sub      rsp, 0x20
0034FF14  mov      rbx, r9
0034FF17  mov      rsi, r8
0034FF1A  mov      rbp, rcx
0034FF1D  call     0x3590d0  ; -> 003590D0 fn
0034FF22  mov      ecx, eax
0034FF24  call     0x3588b0  ; -> 003588B0 fn
0034FF29  mov      rdi, rax
0034FF2C  mov      rcx, rbx
0034FF2F  test     rax, rax
0034FF32  je       0x34ff46  ; -> 0034FF46
0034FF34  call     0x267db0  ; -> 00267DB0 fn
0034FF39  movaps   xmm1, xmm0
0034FF3C  mov      rcx, rdi
0034FF3F  call     0x26b620  ; -> 0026B620 fn
0034FF44  jmp      0x34ff4b  ; -> 0034FF4B
0034FF46  call     0x267db0  ; -> 00267DB0 fn
0034FF4B  call     0x3590d0  ; -> 003590D0 fn
0034FF50  mov      ecx, eax
0034FF52  call     0x3588b0  ; -> 003588B0 fn
0034FF57  test     rax, rax
0034FF5A  je       0x34ff6f  ; -> 0034FF6F
0034FF5C  mov      r9, rbx
0034FF5F  mov      r8, rsi
0034FF62  mov      rdx, rax
0034FF65  mov      rcx, rbp
0034FF68  call     0x34ebc0  ; -> 0034EBC0 fn
0034FF6D  jmp      0x34ff87  ; -> 0034FF87
0034FF6F  mov      rcx, rbx
0034FF72  call     0x267db0  ; -> 00267DB0 fn
0034FF77  mov      rcx, rbx
0034FF7A  call     0x267db0  ; -> 00267DB0 fn
0034FF7F  mov      rcx, rbx
0034FF82  call     0x267db0  ; -> 00267DB0 fn
0034FF87  mov      rbx, qword ptr [rsp + 0x30]
0034FF8C  mov      rbp, qword ptr [rsp + 0x38]
0034FF91  mov      rsi, qword ptr [rsp + 0x40]
0034FF96  add      rsp, 0x20
0034FF9A  pop      rdi
0034FF9B  ret      
```

## 00350DD0 (238 B, extent 00350DD0-00350EBE)

Page context: " — MECHANICAL (SWE2-EC7-175, 15 edges).** '003588B0' and '00263B80', helpers this page's '002C8820' calls, are reached by '00341CB0'/'00345800'/'00346FA0'/'0034C3D0'/'0034C950'/'0034F800'/'0034FF00'/'00350DD0'/'003516E0'/'00352580'/'003530F0'/'00355830'/'00356570'/'0050E060' and '0034FCC0' of that layer — script-VM bodies share the same object-resolve and field helpers; pure fan-in, not a shared responsibility.  *Added 2026-09-29 (FABLE"

```
00350DD0  mov      qword ptr [rsp + 8], rbx
00350DD5  mov      qword ptr [rsp + 0x10], rbp
00350DDA  mov      qword ptr [rsp + 0x18], rsi
00350DDF  push     rdi
00350DE0  sub      rsp, 0x40
00350DE4  mov      rbp, rcx
00350DE7  movaps   xmmword ptr [rsp + 0x30], xmm6
00350DEC  mov      rcx, r9
00350DEF  mov      rbx, r9
00350DF2  xor      edi, edi
00350DF4  call     0x267db0  ; -> 00267DB0 fn
00350DF9  mov      rcx, rbx
00350DFC  movaps   xmm6, xmm0
00350DFF  call     0x267e10  ; -> 00267E10 fn
00350E04  mov      ebx, eax
00350E06  call     0x2640c0  ; -> 002640C0 fn
00350E0B  mov      edx, ebx
00350E0D  mov      rcx, rax
00350E10  call     0x358940  ; -> 00358940 fn
00350E15  mov      rsi, rax
00350E18  call     0x3590d0  ; -> 003590D0 fn
00350E1D  mov      ecx, eax
00350E1F  call     0x3588b0  ; -> 003588B0 fn
00350E24  test     rax, rax
00350E27  je       0x350e9b  ; -> 00350E9B
00350E29  test     rsi, rsi
00350E2C  je       0x350e9b  ; -> 00350E9B
00350E2E  mov      rbx, qword ptr [rax + 0xb8]
00350E35  lea      r9, [rsp + 0x28]
00350E3A  lea      r8, [rsp + 0x24]
00350E3F  mov      rcx, rsi
00350E42  lea      rdx, [rsp + 0x20]
00350E47  call     0x265020  ; -> 00265020 fn
00350E4C  movss    xmm2, dword ptr [rbx]
00350E50  mov      eax, 1
00350E55  subss    xmm2, dword ptr [rsp + 0x20]
00350E5B  mulss    xmm6, xmm6
00350E5F  movss    dword ptr [rsp + 0x20], xmm2
00350E65  movss    xmm0, dword ptr [rbx + 4]
00350E6A  subss    xmm0, dword ptr [rsp + 0x24]
00350E70  mulss    xmm2, xmm2
00350E74  movss    dword ptr [rsp + 0x24], xmm0
00350E7A  movss    xmm1, dword ptr [rbx + 8]
00350E7F  subss    xmm1, dword ptr [rsp + 0x28]
00350E85  mulss    xmm0, xmm0
00350E89  addss    xmm2, xmm0
00350E8D  mulss    xmm1, xmm1
00350E91  addss    xmm2, xmm1
00350E95  comiss   xmm6, xmm2
00350E98  cmova    edi, eax
00350E9B  mov      edx, edi
00350E9D  mov      rcx, rbp
00350EA0  mov      rbx, qword ptr [rsp + 0x50]
00350EA5  mov      rbp, qword ptr [rsp + 0x58]
00350EAA  mov      rsi, qword ptr [rsp + 0x60]
00350EAF  movaps   xmm6, xmmword ptr [rsp + 0x30]
00350EB4  add      rsp, 0x40
00350EB8  pop      rdi
00350EB9  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 003516E0 (213 B, extent 003516E0-003517B5)

Page context: "AL (SWE2-EC7-175, 15 edges).** '003588B0' and '00263B80', helpers this page's '002C8820' calls, are reached by '00341CB0'/'00345800'/'00346FA0'/'0034C3D0'/'0034C950'/'0034F800'/'0034FF00'/'00350DD0'/'003516E0'/'00352580'/'003530F0'/'00355830'/'00356570'/'0050E060' and '0034FCC0' of that layer — script-VM bodies share the same object-resolve and field helpers; pure fan-in, not a shared responsibility.  *Added 2026-09-29 (FABLE, pass-22 d"

```
003516E0  mov      qword ptr [rsp + 8], rbx
003516E5  mov      qword ptr [rsp + 0x10], rbp
003516EA  mov      qword ptr [rsp + 0x18], rsi
003516EF  push     rdi
003516F0  sub      rsp, 0x40
003516F4  mov      rbp, rcx
003516F7  movaps   xmmword ptr [rsp + 0x30], xmm6
003516FC  mov      rcx, r9
003516FF  mov      rbx, r9
00351702  xor      edi, edi
00351704  call     0x267db0  ; -> 00267DB0 fn
00351709  mov      rcx, rbx
0035170C  movaps   xmm6, xmm0
0035170F  call     0x267e10  ; -> 00267E10 fn
00351714  mov      ebx, eax
00351716  call     0x2640c0  ; -> 002640C0 fn
0035171B  mov      edx, ebx
0035171D  mov      rcx, rax
00351720  call     0x358940  ; -> 00358940 fn
00351725  mov      rsi, rax
00351728  call     0x3590d0  ; -> 003590D0 fn
0035172D  mov      ecx, eax
0035172F  call     0x3588b0  ; -> 003588B0 fn
00351734  test     rax, rax
00351737  je       0x351792  ; -> 00351792
00351739  test     rsi, rsi
0035173C  je       0x351792  ; -> 00351792
0035173E  mov      rbx, qword ptr [rax + 0xb8]
00351745  lea      r9, [rsp + 0x24]
0035174A  lea      r8, [rsp + 0x28]
0035174F  mov      rcx, rsi
00351752  lea      rdx, [rsp + 0x20]
00351757  call     0x265020  ; -> 00265020 fn
0035175C  movss    xmm1, dword ptr [rbx]
00351760  mov      eax, 1
00351765  subss    xmm1, dword ptr [rsp + 0x20]
0035176B  mulss    xmm6, xmm6
0035176F  movss    dword ptr [rsp + 0x20], xmm1
00351775  movss    xmm0, dword ptr [rbx + 8]
0035177A  subss    xmm0, dword ptr [rsp + 0x24]
00351780  mulss    xmm1, xmm1
00351784  mulss    xmm0, xmm0
00351788  addss    xmm1, xmm0
0035178C  comiss   xmm6, xmm1
0035178F  cmova    edi, eax
00351792  mov      edx, edi
00351794  mov      rcx, rbp
00351797  mov      rbx, qword ptr [rsp + 0x50]
0035179C  mov      rbp, qword ptr [rsp + 0x58]
003517A1  mov      rsi, qword ptr [rsp + 0x60]
003517A6  movaps   xmm6, xmmword ptr [rsp + 0x30]
003517AB  add      rsp, 0x40
003517AF  pop      rdi
003517B0  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 00352580 (213 B, extent 00352580-00352655)

Page context: "7-175, 15 edges).** '003588B0' and '00263B80', helpers this page's '002C8820' calls, are reached by '00341CB0'/'00345800'/'00346FA0'/'0034C3D0'/'0034C950'/'0034F800'/'0034FF00'/'00350DD0'/'003516E0'/'00352580'/'003530F0'/'00355830'/'00356570'/'0050E060' and '0034FCC0' of that layer — script-VM bodies share the same object-resolve and field helpers; pure fan-in, not a shared responsibility.  *Added 2026-09-29 (FABLE, pass-22 debt): one p"

```
00352580  mov      qword ptr [rsp + 8], rbx
00352585  push     rdi
00352586  sub      rsp, 0x60
0035258A  movaps   xmmword ptr [rsp + 0x50], xmm6
0035258F  mov      rdi, rcx
00352592  movaps   xmmword ptr [rsp + 0x40], xmm7
00352597  mov      rcx, r9
0035259A  movaps   xmmword ptr [rsp + 0x30], xmm8
003525A0  mov      rbx, r9
003525A3  movaps   xmmword ptr [rsp + 0x20], xmm9
003525A9  call     0x267db0  ; -> 00267DB0 fn
003525AE  mov      rcx, rbx
003525B1  movaps   xmm6, xmm0
003525B4  call     0x267db0  ; -> 00267DB0 fn
003525B9  mov      rcx, rbx
003525BC  movaps   xmm7, xmm0
003525BF  call     0x267db0  ; -> 00267DB0 fn
003525C4  mov      rcx, rbx
003525C7  movaps   xmm8, xmm0
003525CB  call     0x267db0  ; -> 00267DB0 fn
003525D0  movaps   xmm9, xmm0
003525D4  call     0x3590d0  ; -> 003590D0 fn
003525D9  mov      ecx, eax
003525DB  call     0x3588b0  ; -> 003588B0 fn
003525E0  xor      edx, edx
003525E2  test     rax, rax
003525E5  je       0x35262d  ; -> 0035262D
003525E7  mov      rax, qword ptr [rax + 0xb8]
003525EE  mulss    xmm6, xmm6
003525F2  movss    xmm2, dword ptr [rax]
003525F6  movss    xmm0, dword ptr [rax + 4]
003525FB  subss    xmm2, xmm9
00352600  movss    xmm1, dword ptr [rax + 8]
00352605  subss    xmm0, xmm8
0035260A  subss    xmm1, xmm7
0035260E  mov      eax, 1
00352613  mulss    xmm2, xmm2
00352617  mulss    xmm0, xmm0
0035261B  mulss    xmm1, xmm1
0035261F  addss    xmm2, xmm0
00352623  addss    xmm2, xmm1
00352627  comiss   xmm6, xmm2
0035262A  cmova    edx, eax
0035262D  mov      rcx, rdi
00352630  mov      rbx, qword ptr [rsp + 0x70]
00352635  movaps   xmm6, xmmword ptr [rsp + 0x50]
0035263A  movaps   xmm7, xmmword ptr [rsp + 0x40]
0035263F  movaps   xmm8, xmmword ptr [rsp + 0x30]
00352645  movaps   xmm9, xmmword ptr [rsp + 0x20]
0035264B  add      rsp, 0x60
0035264F  pop      rdi
00352650  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 003530F0 (171 B, extent 003530F0-0035319B)

Page context: "dges).** '003588B0' and '00263B80', helpers this page's '002C8820' calls, are reached by '00341CB0'/'00345800'/'00346FA0'/'0034C3D0'/'0034C950'/'0034F800'/'0034FF00'/'00350DD0'/'003516E0'/'00352580'/'003530F0'/'00355830'/'00356570'/'0050E060' and '0034FCC0' of that layer — script-VM bodies share the same object-resolve and field helpers; pure fan-in, not a shared responsibility.  *Added 2026-09-29 (FABLE, pass-22 debt): one paragraph pe"

```
003530F0  mov      qword ptr [rsp + 8], rbx
003530F5  push     rdi
003530F6  sub      rsp, 0x50
003530FA  movaps   xmmword ptr [rsp + 0x40], xmm6
003530FF  mov      rdi, rcx
00353102  movaps   xmmword ptr [rsp + 0x30], xmm7
00353107  mov      rcx, r9
0035310A  movaps   xmmword ptr [rsp + 0x20], xmm8
00353110  mov      rbx, r9
00353113  call     0x267db0  ; -> 00267DB0 fn
00353118  mov      rcx, rbx
0035311B  movaps   xmm6, xmm0
0035311E  call     0x267db0  ; -> 00267DB0 fn
00353123  mov      rcx, rbx
00353126  movaps   xmm7, xmm0
00353129  call     0x267db0  ; -> 00267DB0 fn
0035312E  movaps   xmm8, xmm0
00353132  call     0x3590d0  ; -> 003590D0 fn
00353137  mov      ecx, eax
00353139  call     0x3588b0  ; -> 003588B0 fn
0035313E  xor      edx, edx
00353140  test     rax, rax
00353143  je       0x353179  ; -> 00353179
00353145  mov      rax, qword ptr [rax + 0xb8]
0035314C  mulss    xmm6, xmm6
00353150  movss    xmm1, dword ptr [rax]
00353154  movss    xmm0, dword ptr [rax + 8]
00353159  subss    xmm1, xmm8
0035315E  subss    xmm0, xmm7
00353162  mov      eax, 1
00353167  mulss    xmm1, xmm1
0035316B  mulss    xmm0, xmm0
0035316F  addss    xmm1, xmm0
00353173  comiss   xmm6, xmm1
00353176  cmova    edx, eax
00353179  mov      rcx, rdi
0035317C  mov      rbx, qword ptr [rsp + 0x60]
00353181  movaps   xmm6, xmmword ptr [rsp + 0x40]
00353186  movaps   xmm7, xmmword ptr [rsp + 0x30]
0035318B  movaps   xmm8, xmmword ptr [rsp + 0x20]
00353191  add      rsp, 0x50
00353195  pop      rdi
00353196  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 00356570 (55 B, extent 00356570-003565A7)

Page context: "d '00263B80', helpers this page's '002C8820' calls, are reached by '00341CB0'/'00345800'/'00346FA0'/'0034C3D0'/'0034C950'/'0034F800'/'0034FF00'/'00350DD0'/'003516E0'/'00352580'/'003530F0'/'00355830'/'00356570'/'0050E060' and '0034FCC0' of that layer — script-VM bodies share the same object-resolve and field helpers; pure fan-in, not a shared responsibility.  *Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit stil"

```
00356570  mov      qword ptr [rsp + 8], rbx
00356575  push     rdi
00356576  sub      rsp, 0x20
0035657A  mov      rbx, r9
0035657D  mov      rdi, r8
00356580  call     0x2640c0  ; -> 002640C0 fn
00356585  mov      rcx, rbx
00356588  call     0x267e10  ; -> 00267E10 fn
0035658D  call     0x3590d0  ; -> 003590D0 fn
00356592  mov      ecx, eax
00356594  call     0x3588b0  ; -> 003588B0 fn
00356599  mov      rbx, qword ptr [rsp + 0x30]
0035659E  mov      qword ptr [rdi], rax
003565A1  add      rsp, 0x20
003565A5  pop      rdi
003565A6  ret      
```

## 0035C770 (33 B, extent 0035C770-0035C791)

Page context: "record builds share. Interior anchor '00273A13' (the 'cmp eax, 5').  ## SWE2-EC7-106 update (2026-09-20) - '002547D0' measured  '002547D0' (105 B) is the seven-slot invoke '00254940', '0035BC50' and '0035C770' run: 'ecx != 0' picks '002E1C20', else '002E1CA0', then the chosen thunk is called six times with '(edx, ecx)' pairs '(1,8)', '(2,8)', '(4,8)', '(5,8)', '(6,8)', '(7,8)' and tail-jumped once more with '(9,8)' - the fixed sequence "

```
0035C770  push     rbx
0035C772  sub      rsp, 0x20
0035C776  mov      ebx, ecx
0035C778  call     0x2547d0  ; -> 002547D0 fn
0035C77D  test     ebx, ebx
0035C77F  jne      0x35c78b  ; -> 0035C78B
0035C781  add      rsp, 0x20
0035C785  pop      rbx
0035C786  jmp      0x254e70  ; -> 00254E70 fn
0035C78B  add      rsp, 0x20
0035C78F  pop      rbx
0035C790  ret      
```
