# F-interior pack: `03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md`

Generated 2026-10-02 10:27 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/field-record-table-navimapdata.json`.

Functions: 4. Each is cited on the page only at its entry and is still in the F frontier.

## 00255330 (132 B, extent 00255330-002553B4)

Page context: "erior anchors '002543E9' / '00254399' (the '+1+ecx' byte loads).  ## SWE2-EC7-102 update (2026-09-20) - '0028FF20' measured  '0028FF20' (81 B) is the conditional word-publish '00251F40', '00254AC0', '00255330' and '003C5E50' call on the '[0209BE80 + 0x10F80]' object: when the slot is nonnull '002544B0()' runs; a return of 1 zeroes 'word[+0x1D78]', and 'word[+0x1D7A]' always gains bit 3 - the clear-and-arm sequence the navimap paths post"

```
00255330  sub      rsp, 0x28
00255334  cmp      ecx, 1
00255337  jne      0x25539c  ; -> 0025539C
00255339  mov      eax, dword ptr [rip + 0x1bb6fe1]  ; -> 01E0C320 [u32 0x00000040]
0025533F  and      eax, 0xc0
00255344  cmp      al, 0xc0
00255346  je       0x255387  ; -> 00255387
00255348  call     0x3c8990  ; -> 003C8990 fn
0025534D  call     0x35dac0  ; -> 0035DAC0 fn
00255352  call     0x28ff20  ; -> 0028FF20 fn
00255357  call     0x3c58b0  ; -> 003C58B0 fn
0025535C  call     0x2b6140  ; -> 002B6140 fn
00255361  call     0x35d5a0  ; -> 0035D5A0 fn
00255366  mov      ecx, dword ptr [rip + 0x1e3d480]  ; -> 020927EC
0025536C  call     0x35d0e0  ; -> 0035D0E0 fn
00255371  call     0x3c9900  ; -> 003C9900 fn
00255376  xor      ecx, ecx
00255378  call     0x3bbfa0  ; -> 003BBFA0 fn
0025537D  and      dword ptr [rip + 0x1e3d465], 0xffffff7f  ; -> 020927EC
00255387  mov      eax, 0xfff3
0025538C  and      word ptr [rip + 0x1bb6f19], ax  ; -> 01E0C2AC [u16 0x000F]
00255393  add      rsp, 0x28
00255397  jmp      0x17e7d0  ; -> 0017E7D0 fn
0025539C  mov      ecx, dword ptr [rip + 0x1e3d446]  ; -> 020927E8
002553A2  call     0x251f40  ; -> 00251F40 fn
002553A7  or       word ptr [rip + 0x1bb6efd], 0xc  ; -> 01E0C2AC [u16 0x000F]
002553AF  add      rsp, 0x28
002553B3  ret      
```

## 002AC2C0 (17 B, extent 002AC2C0-002AC2D1)

Page context: "0'/'00255060'/'00255120'/'002F9860'. Interior anchor '00576B65' (a '00309EC0' call).  ## SWE2-EC7-47 update (2026-09-19) - '003F92B0'  '003F92B0' (216 B) is a body - '00254380'/'002543D0'/'00254F30'/'002AC2C0'/'002F9860'/'003148F0'/'00377870'. Interior anchor '003F92D3' (a '00254380' call).  ## SWE2-EC7-47 update (2026-09-19) - '0031C000'  '0031C000' (212 B) is a body - '00313F60'/'0031BDC0'/'00377C70'. Interior anchor '0031C083' (a '00"

```
002AC2C0  or       cl, 0x80
002AC2C3  lea      rax, [rip + 0x1b60b32]  ; -> 01E0CDFC
002AC2CA  mov      byte ptr [rip + 0x1b60b2f], cl  ; -> 01E0CDFF [u8 0x80]
002AC2D0  ret      
```

## 003778B0 (68 B, extent 003778B0-003778F4)

Page context: "0' | | '00377B60' | 'MapName_GetFieldNameById' | 45 B | 'PLMN' field-name reader, bound at '+4' | | '00377870' | 'MapName_GetAreaNameById' | 49 B | 'PLMN' area-name reader, base '+4', bound '+8' | | '003778B0' | 'MapName_GetActiveAreaName' | 68 B | same, for the current area | | '0032E400' | 'Resource_GetFileSizeByKindAndIndex' | 80 B | '(kind, index)' → size | | '0032E620' | 'Resource_SubmitRequest' | 340 B | async request + completion"

```
003778B0  sub      rsp, 0x28
003778B4  call     0x264f90  ; -> 00264F90 fn
003778B9  mov      rcx, qword ptr [rip + 0x2765838]  ; -> 02ADD0F8
003778C0  mov      edx, eax
003778C2  test     rcx, rcx
003778C5  je       0x3778e8  ; -> 003778E8
003778C7  cmp      eax, dword ptr [rcx + 8]
003778CA  jae      0x3778e8  ; -> 003778E8
003778CC  mov      eax, dword ptr [rcx + 4]
003778CF  add      eax, edx
003778D1  cdqe     
003778D3  movzx    edx, word ptr [rcx + rax*2 + 0x10]
003778D8  test     dx, dx
003778DB  je       0x3778e8  ; -> 003778E8
003778DD  movzx    eax, dx
003778E0  add      rax, rcx
003778E3  add      rsp, 0x28
003778E7  ret      
003778E8  lea      rax, [rip + 0x1973d49]  ; -> 01CEB638
003778EF  add      rsp, 0x28
003778F3  ret      
```

## 0050CDE0 (91 B, extent 0050CDE0-0050CE3B)

Page context: "les](../../01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md)). Cited here only   as the area-id source for '003778B0'. The script VM / native bridge callers ('0050CDE0',   '00357450') are ScriptVM verbs asking the engine for the current area id — authored-intent   consumers of the id, not of the field record.  One further edge, '0026A1D0 callee 00226BE0': this document cites '0026A1D0' only as on"

```
0050CDE0  mov      qword ptr [rsp + 8], rbx
0050CDE5  push     rdi
0050CDE6  sub      rsp, 0x20
0050CDEA  mov      rcx, r9
0050CDED  mov      rbx, r9
0050CDF0  call     0x267e10  ; -> 00267E10 fn
0050CDF5  mov      rcx, rbx
0050CDF8  mov      edi, eax
0050CDFA  call     0x267e10  ; -> 00267E10 fn
0050CDFF  mov      ecx, edi
0050CE01  mov      ebx, eax
0050CE03  call     0x264f10  ; -> 00264F10 fn
0050CE08  mov      edx, eax
0050CE0A  mov      ecx, ebx
0050CE0C  call     0x16d6a0  ; -> 0016D6A0 fn
0050CE11  mov      ecx, edi
0050CE13  call     0x264f40  ; -> 00264F40 fn
0050CE18  mov      edx, eax
0050CE1A  mov      ecx, ebx
0050CE1C  call     0x16d6a0  ; -> 0016D6A0 fn
0050CE21  mov      ecx, edi
0050CE23  call     0x264f90  ; -> 00264F90 fn
0050CE28  mov      edx, eax
0050CE2A  mov      ecx, ebx
0050CE2C  mov      rbx, qword ptr [rsp + 0x30]
0050CE31  add      rsp, 0x20
0050CE35  pop      rdi
0050CE36  jmp      0x16d6a0  ; -> 0016D6A0 fn
```
