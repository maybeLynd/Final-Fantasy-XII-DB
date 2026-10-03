# F-interior pack: `06-Movement-And-Navigation/the-movement-body-pool-and-the-separation-pass.md`

Generated 2026-10-02 12:46 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/the-movement-body-pool-and-the-separation-pass.json`.

Functions: 8. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (inbox mentions: FABLE.md). OPUS read these before packing.

## 0026BEE0 (115 B, extent 0026BEE0-0026BF53)

Page context: " anchor '00420D5A' (the first 'movss' store).  ## SWE2-EC7-105 update (2026-09-20) - '003DA860' + '0025D480' measured  '003DA860' (42 B) is the scaled-pair writer '00265FF0', '0026B2E0', '0026BBC0', '0026BEE0' and '0026BF60' call: '[rcx] = xmm2 * [rsp + 0x28]' and '[rcx + 4] = xmm3 * [rsp + 0x30]', and when 'rdx' is non-null the unscaled 'xmm2' / 'xmm3' pair is also stored at '[rdx]' / '[rdx + 4]' - one call emitting both the weighted r"

```
0026BEE0  sub      rsp, 0x38
0026BEE4  movzx    edx, byte ptr [rcx + 3]
0026BEE8  shr      edx, 5
0026BEEB  sub      edx, 1
0026BEEE  je       0x26bf22  ; -> 0026BF22
0026BEF0  cmp      edx, 2
0026BEF3  jne      0x26bf4e  ; -> 0026BF4E
0026BEF5  mov      qword ptr [rsp + 0x30], rbx
0026BEFA  movaps   xmm2, xmm1
0026BEFD  mov      rbx, qword ptr [rcx + 0xb8]
0026BF04  lea      rdx, [rbx + 0x50]
0026BF08  lea      rcx, [rbx + 0x60]
0026BF0C  call     0x3da890  ; -> 003DA890 fn
0026BF11  mov      byte ptr [rbx + 0xdf], 1
0026BF18  mov      rbx, qword ptr [rsp + 0x30]
0026BF1D  add      rsp, 0x38
0026BF21  ret      
0026BF22  movss    xmm0, dword ptr [rip + 0x1a7fc7e]  ; -> 01CEBBA8 [f32 1]
0026BF2A  movaps   xmm3, xmm1
0026BF2D  mov      rcx, qword ptr [rcx + 0xb8]
0026BF34  movaps   xmm2, xmm1
0026BF37  movss    dword ptr [rsp + 0x28], xmm0
0026BF3D  add      rcx, 0x30
0026BF41  xor      edx, edx
0026BF43  movss    dword ptr [rsp + 0x20], xmm0
0026BF49  call     0x3da860  ; -> 003DA860 fn
0026BF4E  add      rsp, 0x38
0026BF52  ret      
```

## 0026E130 (22 B, extent 0026E130-0026E146)

Page context: "(index, value, shift, width)' — 'mask |= field', 'value = (value & ~field) | (v << shift)' on the 8-byte entry '{mask, value}' ('0026E8A1'..'0026E8AC') — and its clearer '0026E850', plus the zeroers '0026E130' (one entry) and '0026E150' (a run); each ends in the notify '003278D0'. Their callers are the family '003791D0'..'003795A0', and those are the tails of the script verbs '00F6'..'010B': 'setmapidfloor' / 'setmapidfloorground' / 're"

```
0026E130  movsxd   rax, ecx
0026E133  lea      rcx, [rip + 0x1e2c2a6]  ; -> 0209A3E0
0026E13A  mov      dword ptr [rcx + rax*8], 0
0026E141  jmp      0x3278d0  ; -> 003278D0 fn
```

## 0026E150 (71 B, extent 0026E150-0026E197)

Page context: ")' — 'mask |= field', 'value = (value & ~field) | (v << shift)' on the 8-byte entry '{mask, value}' ('0026E8A1'..'0026E8AC') — and its clearer '0026E850', plus the zeroers '0026E130' (one entry) and '0026E150' (a run); each ends in the notify '003278D0'. Their callers are the family '003791D0'..'003795A0', and those are the tails of the script verbs '00F6'..'010B': 'setmapidfloor' / 'setmapidfloorground' / 'resetmapidfloor*' address ent"

```
0026E150  test     edx, edx
0026E152  jle      0x26e196  ; -> 0026E196
0026E154  push     rdi
0026E155  sub      rsp, 0x20
0026E159  movsxd   rax, ecx
0026E15C  lea      rcx, [rip + 0x1e2c27d]  ; -> 0209A3E0
0026E163  mov      qword ptr [rsp + 0x30], rbx
0026E168  mov      qword ptr [rsp + 0x38], rsi
0026E16D  xor      esi, esi
0026E16F  movsxd   rdi, edx
0026E172  lea      rbx, [rcx + rax*8]
0026E176  mov      dword ptr [rbx], esi
0026E178  call     0x3278d0  ; -> 003278D0 fn
0026E17D  lea      rbx, [rbx + 8]
0026E181  sub      rdi, 1
0026E185  jne      0x26e176  ; -> 0026E176
0026E187  mov      rsi, qword ptr [rsp + 0x38]
0026E18C  mov      rbx, qword ptr [rsp + 0x30]
0026E191  add      rsp, 0x20
0026E195  pop      rdi
0026E196  ret      
```

## 002E9830 (36 B, extent 002E9830-002E9854)

Page context: "n, and what fills the mask table, is **FZ-11**. The allocator zeroes the word ('003DA96E') until the first placement; the neighbouring '+0x8A' also has a setter ('002EBC70', '002EBC88') and readers ('002E9830', '002E9D90'), '+0x86' a reader ('002E9890'), and the mask '+0x110' a setter ('002EC5B0') and reader ('002E9BB0').  ## 3. Key addresses  | Address | Name | Size | Role | |---|---|---|---| | '02B4E4C0' | — | 128 × '0x130' | the pool"

```
002E9830  mov      rax, qword ptr [rcx + 0xc0]
002E9837  test     rax, rax
002E983A  je       0x2e9850  ; -> 002E9850
002E983C  mov      rax, qword ptr [rax + 0x138]
002E9843  test     rax, rax
002E9846  je       0x2e9850  ; -> 002E9850
002E9848  movsx    eax, word ptr [rax + 0x8a]
002E984F  ret      
002E9850  or       eax, 0xffffffff
002E9853  ret      
```

## 002E9890 (36 B, extent 002E9890-002E98B4)

Page context: "1**. The allocator zeroes the word ('003DA96E') until the first placement; the neighbouring '+0x8A' also has a setter ('002EBC70', '002EBC88') and readers ('002E9830', '002E9D90'), '+0x86' a reader ('002E9890'), and the mask '+0x110' a setter ('002EC5B0') and reader ('002E9BB0').  ## 3. Key addresses  | Address | Name | Size | Role | |---|---|---|---| | '02B4E4C0' | — | 128 × '0x130' | the pool | | '02B525C4' / '02B57CC0' | — | 2 / 2 | "

```
002E9890  mov      rax, qword ptr [rcx + 0xc0]
002E9897  test     rax, rax
002E989A  je       0x2e98b0  ; -> 002E98B0
002E989C  mov      rax, qword ptr [rax + 0x138]
002E98A3  test     rax, rax
002E98A6  je       0x2e98b0  ; -> 002E98B0
002E98A8  movsx    eax, word ptr [rax + 0x86]
002E98AF  ret      
002E98B0  or       eax, 0xffffffff
002E98B3  ret      
```

## 00347240 (82 B, extent 00347240-00347292)

Page context: "two of the three fields are named by the script verbs that read them, and the mask table's address is corrected.** Body '+0x86' (attribute bits 13..17) is read by the getter '002E9890', whose caller '00347240' is the handler of ['getmapid_48b'](../01-Script-VM-Native-Bridge/scriptvm-native-dispatch-table.md): the field is the cell's **map id** as the script sees it. Body '+0x8A' ('00231F80''s five bits, attribute bits 18..22 masked) is "

```
00347240  mov      qword ptr [rsp + 8], rbx
00347245  mov      qword ptr [rsp + 0x10], rsi
0034724A  push     rdi
0034724B  sub      rsp, 0x20
0034724F  mov      rsi, rcx
00347252  mov      rcx, r9
00347255  call     0x267e10  ; -> 00267E10 fn
0034725A  xor      ebx, ebx
0034725C  mov      ecx, eax
0034725E  mov      edi, ebx
00347260  call     0x263770  ; -> 00263770 fn
00347265  test     rax, rax
00347268  je       0x347274  ; -> 00347274
0034726A  mov      rcx, rax
0034726D  call     0x2e9890  ; -> 002E9890 fn
00347272  mov      edi, eax
00347274  test     edi, edi
00347276  mov      rcx, rsi
00347279  cmovns   ebx, edi
0034727C  mov      edx, ebx
0034727E  mov      rbx, qword ptr [rsp + 0x30]
00347283  mov      rsi, qword ptr [rsp + 0x38]
00347288  add      rsp, 0x20
0034728C  pop      rdi
0034728D  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 003476B0 (82 B, extent 003476B0-00347702)

Page context: "/scriptvm-native-dispatch-table.md): the field is the cell's **map id** as the script sees it. Body '+0x8A' ('00231F80''s five bits, attribute bits 18..22 masked) is read by '002E9830', whose caller '003476B0' is the handler of 'getmapgroundtype_48c', and directly by the footstep chooser '002E9D90' ('002E9F29') as the surface index into ['soundfoottable.bin'](../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/five-small-bin-tables"

```
003476B0  mov      qword ptr [rsp + 8], rbx
003476B5  mov      qword ptr [rsp + 0x10], rsi
003476BA  push     rdi
003476BB  sub      rsp, 0x20
003476BF  mov      rsi, rcx
003476C2  mov      rcx, r9
003476C5  call     0x267e10  ; -> 00267E10 fn
003476CA  xor      ebx, ebx
003476CC  mov      ecx, eax
003476CE  mov      edi, ebx
003476D0  call     0x263770  ; -> 00263770 fn
003476D5  test     rax, rax
003476D8  je       0x3476e4  ; -> 003476E4
003476DA  mov      rcx, rax
003476DD  call     0x2e9830  ; -> 002E9830 fn
003476E2  mov      edi, eax
003476E4  test     edi, edi
003476E6  mov      rcx, rsi
003476E9  cmovns   ebx, edi
003476EC  mov      edx, ebx
003476EE  mov      rbx, qword ptr [rsp + 0x30]
003476F3  mov      rsi, qword ptr [rsp + 0x38]
003476F8  add      rsp, 0x20
003476FC  pop      rdi
003476FD  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 003791D0 (21 B, extent 003791D0-003791E5)

Page context: "{mask, value}' ('0026E8A1'..'0026E8AC') — and its clearer '0026E850', plus the zeroers '0026E130' (one entry) and '0026E150' (a run); each ends in the notify '003278D0'. Their callers are the family '003791D0'..'003795A0', and those are the tails of the script verbs '00F6'..'010B': 'setmapidfloor' / 'setmapidfloorground' / 'resetmapidfloor*' address entries 0–31, 'setmapidwall*' entries 32–63 ('add ecx, 0x20', '003795C3'), 'setmapidmj*'"

```
003791D0  test     ecx, ecx
003791D2  jns      0x3791e0  ; -> 003791E0
003791D4  mov      edx, 0x20
003791D9  xor      ecx, ecx
003791DB  jmp      0x26e150  ; -> 0026E150 fn
003791E0  jmp      0x26e130  ; -> 0026E130 fn
```
