# F-interior pack: `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/five-small-bin-tables.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/five-small-bin-tables.json`.

Functions: 5. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: bafa49c9f	SWE2-DATA: bucket member formats declared - 53 .bin + 5 .dat members, every entry assigned, each cla; inbox mentions: SWE2-EC7.md). OPUS read these before packing.

## 0029DCD0 (12 B, extent 0029DCD0-0029DCDC)

Page context: " three parts read from its reader.** The request is '0029DC90': when the pointer '0209C4A0' is still null it asks '(7, 0x24)' through '00249180' → '00249210' ('0029DCBF') with the completion handler '0029DCD0', which stores the buffer pointer there. The readers follow the header's three section offsets ('+8', '+0xA', '+0xC'). **Section 0** (27 records '{u32 nameTextId, u32 buttonMask}') is the button table. **Section 1** (24 records) is"

```
0029DCD0  mov      rax, qword ptr [rcx + 8]
0029DCD4  mov      qword ptr [rip + 0x1dfe7c5], rax  ; -> 0209C4A0
0029DCDB  ret      
```

## 0035B3E0 (98 B, extent 0035B3E0-0035B442)

Page context: "ad by 0035C3F0 for 0027DED0, sections 5 and UQ-68"   - "VIB0 | explained | eventvib.bin (.bin member): {VIB0, u32 count, u32 offsets[count], keyframe-pair records} - (kind 9, 7) by 00379E90, bound by 0035B3E0, evaluated by 0035AF20, sections 4 and UQ-67"   - "FOOT | explained | soundfoottable.bin (.bin member): {FOOT01, u32 32, pad, u8 setA[32], u8 setB[32]} (80 B) - (kind 9, 9) by 00378540, blob at 02ADD0C0, read by the footstep choose"

```
0035B3E0  mov      qword ptr [rsp + 0x18], rbx
0035B3E5  push     rdi
0035B3E6  sub      rsp, 0x20
0035B3EA  xor      edi, edi
0035B3EC  mov      rbx, rcx
0035B3EF  cmp      dword ptr [rcx + 4], edi
0035B3F2  jbe      0x35b430  ; -> 0035B430
0035B3F4  mov      qword ptr [rsp + 0x30], rbp
0035B3F9  mov      qword ptr [rsp + 0x38], rsi
0035B3FE  lea      rsi, [rcx + 8]
0035B402  mov      ebp, ebx
0035B404  movsxd   rax, edi
0035B407  mov      ecx, dword ptr [rbx + rax*4 + 8]
0035B40B  call     0x20e600  ; -> 0020E600 fn
0035B410  lea      rcx, [rax + rbp]
0035B414  call     0x20e620  ; -> 0020E620 fn
0035B419  mov      dword ptr [rsi], eax
0035B41B  lea      rsi, [rsi + 4]
0035B41F  inc      edi
0035B421  cmp      edi, dword ptr [rbx + 4]
0035B424  jb       0x35b404  ; -> 0035B404
0035B426  mov      rsi, qword ptr [rsp + 0x38]
0035B42B  mov      rbp, qword ptr [rsp + 0x30]
0035B430  mov      qword ptr [rip + 0x2b65731], rbx  ; -> 02EC0B68
0035B437  mov      rbx, qword ptr [rsp + 0x40]
0035B43C  add      rsp, 0x20
0035B440  pop      rdi
0035B441  ret      
```

## 0035FED0 (89 B, extent 0035FED0-0035FF29)

Page context: " 00' followed by a byte-for-byte copy of the eleventh record; no offset addresses them and the walk stops at 'count', so they are never read. '0035AE30' hands the two motor values to the pad through '0035FED0'. Static, bodies and the extracted file read.* - [x] **UQ-68.** 'bwin': what entry 4 is, and what the two numbers measure.       ***NARROWED 2026-09-17 (FABLE): the reader is not locatable by the three methods that found FOOT and V"

```
0035FED0  sub      rsp, 0x28
0035FED4  test     edx, edx
0035FED6  jns      0x35fedc  ; -> 0035FEDC
0035FED8  xor      edx, edx
0035FEDA  jmp      0x35fee6  ; -> 0035FEE6
0035FEDC  mov      eax, 1
0035FEE1  cmp      edx, eax
0035FEE3  cmovg    edx, eax
0035FEE6  cmp      ecx, 2
0035FEE9  jge      0x35ff24  ; -> 0035FF24
0035FEEB  movsxd   rax, ecx
0035FEEE  mov      qword ptr [rsp + 0x30], rbx
0035FEF3  mov      qword ptr [rsp + 0x20], rdi
0035FEF8  imul     rdi, rax, 0x294
0035FEFF  lea      rax, [rip + 0x1f6af8a]  ; -> 022CAE90
0035FF06  movsxd   rbx, edx
0035FF09  add      rdi, rax
0035FF0C  mov      byte ptr [rbx + rdi + 6], r8b
0035FF11  call     0x35e810  ; -> 0035E810 fn
0035FF16  mov      dword ptr [rdi + rbx*4 + 0x1c], eax
0035FF1A  mov      rdi, qword ptr [rsp + 0x20]
0035FF1F  mov      rbx, qword ptr [rsp + 0x30]
0035FF24  add      rsp, 0x28
0035FF28  ret      
```

## 00379F30 (7 B, extent 00379F30-00379F37)

Page context: "racks of {u8 duration, u8 intensity} pairs, not two u16 intensities, and the tail is an unaddressed duplicate.** 'eventvib.bin' is requested as kind 9 id 7 by '00379E90' ('00379EFE') with completion '00379F30', which hands the blob to '0035B3E0': it rewrites each of the 'count' offsets into a resolved handle through '0020E600'/'0020E620' and publishes the table at '02EC0B68'. A pattern starts through '0035B650(index, flag)': '0035B2F0' "

```
00379F30  mov      ecx, ecx
00379F32  jmp      0x35b3e0  ; -> 0035B3E0 fn
```

## 003C9950 (125 B, extent 003C9950-003C99CD)

Page context: "2CA408', are called by every menu that lays out text; - the menu-set request thunk '00249180' → '00249210' is also reached from the world-map mesh and menu-package   loaders ('00561390', '00562F90', '003C9950'); - the key-signal readers '0029DA70' / '0029DBE0' and the six HUD-mask writers ('00295D20', '0029E110', '002B7B80',   '002BAF80', '002D5EB0', '005789D0') call menu helpers; - '0027DED0' is called from 'BattleMenu_UpdateCommandSel"

```
003C9950  mov      qword ptr [rsp + 8], rbx
003C9955  mov      qword ptr [rsp + 0x10], rsi
003C995A  push     rdi
003C995B  sub      rsp, 0x30
003C995F  mov      rdi, rcx
003C9962  call     0x249580  ; -> 00249580 fn
003C9967  mov      rcx, qword ptr [rdi + 0xd0]
003C996E  mov      rsi, rax
003C9971  test     rcx, rcx
003C9974  je       0x3c997b  ; -> 003C997B
003C9976  call     0x3697f0  ; -> 003697F0 fn
003C997B  movzx    r8d, byte ptr [rdi + 0xc1]
003C9983  mov      edx, 7
003C9988  add      r8d, 0xe
003C998C  mov      dword ptr [rsp + 0x20], 0
003C9994  mov      rcx, rsi
003C9997  lea      r9d, [rdx - 4]
003C999B  call     0x249210  ; -> 00249210 fn
003C99A0  mov      rcx, rsi
003C99A3  mov      rbx, rax
003C99A6  call     0x249410  ; -> 00249410 fn
003C99AB  mov      rax, qword ptr [rbx + 8]
003C99AF  or       dword ptr [rdi + 0xc4], 8
003C99B6  mov      rbx, qword ptr [rsp + 0x40]
003C99BB  mov      rsi, qword ptr [rsp + 0x48]
003C99C0  mov      qword ptr [rdi + 0xd0], rax
003C99C7  add      rsp, 0x30
003C99CB  pop      rdi
003C99CC  ret      
```
