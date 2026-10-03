# F-interior pack: `00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md`

Generated 2026-10-02 19:59 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/what-the-engine-fixes-at-boot.json`.

Functions: 4. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: de4492e21	SWE2-CONTRACT: pass-22 debt final - six-folder worklist (597 pairs) fully dispositioned, 0 live find; f9017b106	SWE2-CONTRACT: repair 807950d2a - restore 18 committed pass-22 section headings it renamed; inbox mentions: FABLE.md, SWE2-FRONTIER.md, repos-78.md, repos-c7.md, repos-c9.md, repos-d6.md, xiionline-8d.md). OPUS read these before packing.

## 003AA240 (60 B, extent 003AA240-003AA27C)

Page context: ") or count*1024 (kind 1) bytes through '0036A100' into '+0x20' and copies them from the stream through '00861EBA'; then calls '00503180' on each record of the list '003AA1F0(1, 0x50)' (stepping with '003AA240'); returns the advanced stream pointer, or 0 for another kind | '00501771', '005017C1', '005017D3', '005017F3' | | '00536120' | 24 B | makes 'rcx' an empty self-linked list head ('+0' and '+8' = 'rcx'), zeroes '+0x14' and '+0x18', "

```
003AA240  push     rbx
003AA242  sub      rsp, 0x20
003AA246  mov      rbx, rcx
003AA249  mov      ecx, dword ptr [rcx]
003AA24B  call     0x20e600  ; -> 0020E600 fn
003AA250  test     rax, rax
003AA253  je       0x3aa274  ; -> 003AA274
003AA255  movzx    edx, word ptr [rbx + 0xc]
003AA259  cmp      word ptr [rax + 0xc], dx
003AA25D  jne      0x3aa268  ; -> 003AA268
003AA25F  movzx    ecx, byte ptr [rbx + 0xe]
003AA263  cmp      byte ptr [rax + 0xe], cl
003AA266  je       0x3aa276  ; -> 003AA276
003AA268  mov      ecx, dword ptr [rax]
003AA26A  call     0x20e600  ; -> 0020E600 fn
003AA26F  test     rax, rax
003AA272  jne      0x3aa255  ; -> 003AA255
003AA274  xor      eax, eax
003AA276  add      rsp, 0x20
003AA27A  pop      rbx
003AA27B  ret      
```

## 00467AD0 (42 B, extent 00467AD0-00467AFA)

Page context: "', '0036EFE7', '0036EFF2' | | '0036F4D0' | 63 B | calls in order '0036D280', '00465F60(0x100)', '003A1D50', '00467BB0', '0026E1D0', '00382910', '003ECF70', '00475310' and '003ED820', then tail-calls '00467AD0' | '0036F4DE', '0036F4E3', '0036F501', '0036F50A' | | '00376A80' | 64 B | zeroes the byte '02ADBB30', the dword '02ADBB34' and the dwords at '02ADBB40' + k*'0x90' for k = 0..7 | '00376A89', '00376A8F', '00376AB9' | | '003773C0' | 5"

```
00467AD0  mov      eax, dword ptr [rip + 0x1e713de]  ; -> 022D8EB4
00467AD6  imul     eax, dword ptr [rip + 0x1e713cf]  ; -> 022D8EAC
00467ADD  mov      dword ptr [rip + 0x283e509], 0x4000  ; -> 02CA5FF0
00467AE7  lea      eax, [rax + rax*2]
00467AEA  cdq      
00467AEB  and      edx, 0x3f
00467AEE  add      eax, edx
00467AF0  sar      eax, 6
00467AF3  mov      dword ptr [rip + 0x283e4fb], eax  ; -> 02CA5FF4
00467AF9  ret      
```

## 00467BB0 (61 B, extent 00467BB0-00467BED)

Page context: "420(1)', sets the byte '022D9B40' to 1 and tail-calls '002DF420(0)' | '0036EFD9', '0036EFE0', '0036EFE7', '0036EFF2' | | '0036F4D0' | 63 B | calls in order '0036D280', '00465F60(0x100)', '003A1D50', '00467BB0', '0026E1D0', '00382910', '003ECF70', '00475310' and '003ED820', then tail-calls '00467AD0' | '0036F4DE', '0036F4E3', '0036F501', '0036F50A' | | '00376A80' | 64 B | zeroes the byte '02ADBB30', the dword '02ADBB34' and the dwords at"

```
00467BB0  sub      rsp, 0x28
00467BB4  lea      rcx, [rip + 0x2a53ae5]  ; -> 02EBB6A0
00467BBB  call     0x536120  ; -> 00536120 fn
00467BC0  lea      rax, [rip - 0xa7]  ; -> 00467B20
00467BC7  mov      dword ptr [rip + 0x2a53adf], 0x28  ; -> 02EBB6B0
00467BD1  mov      qword ptr [rip + 0x2a53ae0], rax  ; -> 02EBB6B8
00467BD8  xor      eax, eax
00467BDA  mov      qword ptr [rip + 0x2a53adf], rax  ; -> 02EBB6C0
00467BE1  mov      qword ptr [rip + 0x2a53ae0], rax  ; -> 02EBB6C8
00467BE8  add      rsp, 0x28
00467BEC  ret      
```

## 00475310 (121 B, extent 00475310-00475389)

Page context: "calls '002DF420(0)' | '0036EFD9', '0036EFE0', '0036EFE7', '0036EFF2' | | '0036F4D0' | 63 B | calls in order '0036D280', '00465F60(0x100)', '003A1D50', '00467BB0', '0026E1D0', '00382910', '003ECF70', '00475310' and '003ED820', then tail-calls '00467AD0' | '0036F4DE', '0036F4E3', '0036F501', '0036F50A' | | '00376A80' | 64 B | zeroes the byte '02ADBB30', the dword '02ADBB34' and the dwords at '02ADBB40' + k*'0x90' for k = 0..7 | '00376A89'"

```
00475310  movss    xmm0, dword ptr [rip + 0x482e68]  ; -> 008F8180 [f32 10]
00475318  xor      eax, eax
0047531A  movss    xmm1, dword ptr [rip + 0x4a02ba]  ; -> 009155DC [f32 150]
00475322  movss    dword ptr [rip + 0x2a4519a], xmm0  ; -> 02EBA4C4
0047532A  movss    xmm0, dword ptr [rip + 0x48c80a]  ; -> 00901B3C [f32 1.5]
00475332  movss    dword ptr [rip + 0x2a4518e], xmm1  ; -> 02EBA4C8
0047533A  movss    xmm1, dword ptr [rip + 0x1876942]  ; -> 01CEBC84 [f32 16]
00475342  movss    dword ptr [rip + 0x2a45182], xmm0  ; -> 02EBA4CC
0047534A  movss    dword ptr [rip + 0x2a4518e], xmm1  ; -> 02EBA4E0
00475352  mov      dword ptr [rip + 0x2a45168], eax  ; -> 02EBA4C0
00475358  mov      dword ptr [rip + 0x2a45172], eax  ; -> 02EBA4D0
0047535E  mov      dword ptr [rip + 0x2a4516c], 5  ; -> 02EBA4D4
00475368  mov      qword ptr [rip + 0x2a45165], 0x40  ; -> 02EBA4D8
00475373  mov      dword ptr [rip + 0x2a45167], 0x40800000  ; -> 02EBA4E4
0047537D  mov      qword ptr [rip + 0x2a45160], 0x40800000  ; -> 02EBA4E8
00475388  ret      
```
