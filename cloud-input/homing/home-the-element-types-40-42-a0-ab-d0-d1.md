# Homing pack: `17-Presentation-Rendering/Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-element-types-40-42-a0-ab-d0-d1.json`.

Bodies: 7. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00376A20 (37 B, extent 00376A20-00376A45)

Entered from (direct sites whose caller this page cites): `00461270` + 0x33E (call; `00461270` is cited on this page)
Other direct sites: none

Host context: " '00460BC0' 874 B, setup '0053A6F0' | compact record ('+0x80'–'+0x1F0'); walk calls '00398F90' (point transform) + '0039AF70' + '003A2D80'/'003A3010' | | '0xA1' | step '00461090' (441 B heavy), walk '00461270' **3820 B** — the largest walk in the whole matrix | calls '001827B0'/'00182830' and the '00376350'–'00377100' helper family; seventh '00461250' touches '+0x1B4'/'+0x294'; setup has a resource store + '+0x1B0'/'+0x1B1' flag bytes |"

```
00376A20  movzx    edx, cl
00376A23  lea      rax, [rdx + rdx*8]
00376A27  add      rax, rax
00376A2A  lea      rdx, [rip + 0x276510f]  ; -> 02ADBB40
00376A31  test     ecx, ecx
00376A33  je       0x376a41  ; -> 00376A41
00376A35  cmp      dword ptr [rdx + rax*8], ecx
00376A38  jne      0x376a41  ; -> 00376A41
00376A3A  movss    xmm0, dword ptr [rdx + rax*8 + 0x2c]
00376A40  ret      
00376A41  xorps    xmm0, xmm0
00376A44  ret      
```

## 00376A50 (37 B, extent 00376A50-00376A75)

Entered from (direct sites whose caller this page cites): `00461270` + 0x330 (call; `00461270` is cited on this page)
Other direct sites: none

Host context: " '00460BC0' 874 B, setup '0053A6F0' | compact record ('+0x80'–'+0x1F0'); walk calls '00398F90' (point transform) + '0039AF70' + '003A2D80'/'003A3010' | | '0xA1' | step '00461090' (441 B heavy), walk '00461270' **3820 B** — the largest walk in the whole matrix | calls '001827B0'/'00182830' and the '00376350'–'00377100' helper family; seventh '00461250' touches '+0x1B4'/'+0x294'; setup has a resource store + '+0x1B0'/'+0x1B1' flag bytes |"

```
00376A50  movzx    edx, cl
00376A53  lea      rax, [rdx + rdx*8]
00376A57  add      rax, rax
00376A5A  lea      rdx, [rip + 0x27650df]  ; -> 02ADBB40
00376A61  test     ecx, ecx
00376A63  je       0x376a71  ; -> 00376A71
00376A65  cmp      dword ptr [rdx + rax*8], ecx
00376A68  jne      0x376a71  ; -> 00376A71
00376A6A  movss    xmm0, dword ptr [rdx + rax*8 + 0x28]
00376A70  ret      
00376A71  xorps    xmm0, xmm0
00376A74  ret      
```

## 00377090 (52 B, extent 00377090-003770C4)

Entered from (direct sites whose caller this page cites): `00461270` + 0x218 (call; `00461270` is cited on this page); `00461270` + 0x256 (call; `00461270` is cited on this page)
Other direct sites: none

Host context: " '00460BC0' 874 B, setup '0053A6F0' | compact record ('+0x80'–'+0x1F0'); walk calls '00398F90' (point transform) + '0039AF70' + '003A2D80'/'003A3010' | | '0xA1' | step '00461090' (441 B heavy), walk '00461270' **3820 B** — the largest walk in the whole matrix | calls '001827B0'/'00182830' and the '00376350'–'00377100' helper family; seventh '00461250' touches '+0x1B4'/'+0x294'; setup has a resource store + '+0x1B0'/'+0x1B1' flag bytes |" / " '00460BC0' 874 B, setup '0053A6F0' | compact record ('+0x80'–'+0x1F0'); walk calls '00398F90' (point transform) + '0039AF70' + '003A2D80'/'003A3010' | | '0xA1' | step '00461090' (441 B heavy), walk '00461270' **3820 B** — the largest walk in the whole matrix | calls '001827B0'/'00182830' and the '00376350'–'00377100' helper family; seventh '00461250' touches '+0x1B4'/'+0x294'; setup has a resource store + '+0x1B0'/'+0x1B1' flag bytes |"

```
00377090  movzx    r8d, cl
00377094  lea      rax, [r8 + r8*8]
00377098  shl      rax, 4
0037709C  lea      r8, [rip + 0x2764a9d]  ; -> 02ADBB40
003770A3  add      rax, r8
003770A6  test     ecx, ecx
003770A8  je       0x3770c3  ; -> 003770C3
003770AA  cmp      dword ptr [rax], ecx
003770AC  jne      0x3770c3  ; -> 003770C3
003770AE  and      dx, 1
003770B2  mov      ecx, 0xfffb
003770B7  and      word ptr [rax + 0x54], cx
003770BB  shl      dx, 2
003770BF  or       word ptr [rax + 0x54], dx
003770C3  ret      
```

## 00377130 (42 B, extent 00377130-0037715A)

Entered from (direct sites whose caller this page cites): `00461270` + 0x114 (call; `00461270` is cited on this page)
Other direct sites: none

Host context: " '00460BC0' 874 B, setup '0053A6F0' | compact record ('+0x80'–'+0x1F0'); walk calls '00398F90' (point transform) + '0039AF70' + '003A2D80'/'003A3010' | | '0xA1' | step '00461090' (441 B heavy), walk '00461270' **3820 B** — the largest walk in the whole matrix | calls '001827B0'/'00182830' and the '00376350'–'00377100' helper family; seventh '00461250' touches '+0x1B4'/'+0x294'; setup has a resource store + '+0x1B0'/'+0x1B1' flag bytes |"

```
00377130  movzx    r8d, cl
00377134  lea      rax, [r8 + r8*8]
00377138  add      rax, rax
0037713B  lea      r8, [rip + 0x27649fe]  ; -> 02ADBB40
00377142  test     ecx, ecx
00377144  je       0x377159  ; -> 00377159
00377146  cmp      dword ptr [r8 + rax*8], ecx
0037714A  jne      0x377159  ; -> 00377159
0037714C  movaps   xmm0, xmmword ptr [rdx]
0037714F  movdqa   xmmword ptr [r8 + rax*8 + 0x80], xmm0
00377159  ret      
```

## 00377160 (39 B, extent 00377160-00377187)

Entered from (direct sites whose caller this page cites): `00461270` + 0x20B (call; `00461270` is cited on this page)
Other direct sites: none

Host context: " '00460BC0' 874 B, setup '0053A6F0' | compact record ('+0x80'–'+0x1F0'); walk calls '00398F90' (point transform) + '0039AF70' + '003A2D80'/'003A3010' | | '0xA1' | step '00461090' (441 B heavy), walk '00461270' **3820 B** — the largest walk in the whole matrix | calls '001827B0'/'00182830' and the '00376350'–'00377100' helper family; seventh '00461250' touches '+0x1B4'/'+0x294'; setup has a resource store + '+0x1B0'/'+0x1B1' flag bytes |"

```
00377160  movzx    r8d, cl
00377164  lea      rax, [r8 + r8*8]
00377168  add      rax, rax
0037716B  lea      r8, [rip + 0x27649ce]  ; -> 02ADBB40
00377172  test     ecx, ecx
00377174  je       0x377186  ; -> 00377186
00377176  cmp      dword ptr [r8 + rax*8], ecx
0037717A  jne      0x377186  ; -> 00377186
0037717C  movaps   xmm0, xmmword ptr [rdx]
0037717F  movdqa   xmmword ptr [r8 + rax*8 + 0x60], xmm0
00377186  ret      
```

## 003B49E0 (72 B, extent 003B49E0-003B4A28)

Entered from (direct sites whose caller this page cites): `00464BD0` + 0x312 (call; `00464BD0` is cited on this page)
Other direct sites: none

Host context: "): it computes each element's visibility ('0024D4E0' and '0024D770', '00377292'–'003772A7'), stores it in the element's "shown" bit and calls the type's apply body - '004640A0' ('0x40', '00377336'), '00464BD0' ('0x41', '00377317'), '0047BD30' ('0x42', '003772FB'), '00465690' ('0xD0', '003772EA'). The 8-byte walks of these types only set that same bit. (A fifth arm, '0046EDD0' for byte '0xF0', is unreachable: types stop at '0xD1' and not"

```
003B49E0  movzx    edx, cl
003B49E3  lea      r8, [rdx + rdx*2]
003B49E7  shl      r8, 5
003B49EB  add      r8, qword ptr [rip + 0x278baee]  ; -> 02B404E0
003B49F2  cmp      dword ptr [r8], ecx
003B49F5  jne      0x3b4a27  ; -> 003B4A27
003B49F7  movss    xmm1, dword ptr [rip + 0x19371a9]  ; -> 01CEBBA8 [f32 1]
003B49FF  xor      ecx, ecx
003B4A01  mov      dword ptr [r8 + 4], ecx
003B4A05  mov      byte ptr [r8 + 0x2e], cl
003B4A09  movzx    eax, word ptr [r8 + 0x2a]
003B4A0E  mov      dword ptr [r8 + 0x3c], ecx
003B4A12  movd     xmm0, eax
003B4A16  cvtdq2ps xmm0, xmm0
003B4A19  divss    xmm1, xmm0
003B4A1D  movss    dword ptr [r8 + 0x38], xmm1
003B4A23  mov      dword ptr [r8 + 0x34], ecx
003B4A27  ret      
```

## 003B6DE0 (237 B, extent 003B6DE0-003B6ECD)

Entered from (direct sites whose caller this page cites): `003B6F80` + 0xC8 (call; `003B6F80` is cited on this page)
Other direct sites: `003B6F30` + 0x15 (call); `003B6F70` + 0x0 (jmp)

Host context: "rEntity neighbours ('ActorResource_FinalizeManagerRuntimeAfterLoads', 'ActorResource_AllocateAndSubmitEntry', 'ActorManager_RunFieldRuntimePass', 'ActorEntity.ManagerPopulationFiltering' '0046BAC0', '003B6F80', '0035A990', '0035A590', '0035A7A0', '003DB1F0', '00264010', '00268D10', '00264050', 'ActorHandle_ResolveRegistryEntryByPackedId', …) call the same six. Element steps resolve their host actor through the same accessors the whole e"

```
003B6DE0  push     rbx
003B6DE2  push     rbp
003B6DE3  push     rsi
003B6DE4  push     r12
003B6DE6  sub      rsp, 0x28
003B6DEA  mov      qword ptr [rsp + 0x50], rdi
003B6DEF  xor      esi, esi
003B6DF1  mov      qword ptr [rsp + 0x60], r14
003B6DF6  mov      r14, r8
003B6DF9  mov      qword ptr [rsp + 0x20], r15
003B6DFE  mov      ebp, edx
003B6E00  mov      r12d, ecx
003B6E03  test     edx, edx
003B6E05  jns      0x3b6e0b  ; -> 003B6E0B
003B6E07  mov      ebp, esi
003B6E09  jmp      0x3b6e15  ; -> 003B6E15
003B6E0B  mov      eax, 0x20
003B6E10  cmp      ebp, eax
003B6E12  cmovg    ebp, eax
003B6E15  mov      dword ptr [rip + 0x2b05e45], ebp  ; -> 02EBCC60
003B6E1B  mov      rdi, rsi
003B6E1E  movsxd   r15, ebp
003B6E21  lea      rbx, [rip + 0x2b05c98]  ; -> 02EBCAC0
003B6E28  test     ebp, ebp
003B6E2A  jle      0x3b6e6f  ; -> 003B6E6F
003B6E2C  mov      qword ptr [rsp + 0x58], r13
003B6E31  lea      r13, [rip + 0x2b05da8]  ; -> 02EBCBE0
003B6E38  nop      dword ptr [rax + rax]
003B6E40  mov      ecx, dword ptr [r14]
003B6E43  mov      dword ptr [r13 + rdi*4], ecx
003B6E48  call     0x3588b0  ; -> 003588B0 fn
003B6E4D  test     rax, rax
003B6E50  je       0x3b6e5e  ; -> 003B6E5E
003B6E52  and      byte ptr [rax + 9], 0xf7
003B6E56  or       byte ptr [rax + 9], 4
003B6E5A  mov      qword ptr [rbx + rdi*8], rax
003B6E5E  inc      rdi
003B6E61  add      r14, 4
003B6E65  cmp      rdi, r15
003B6E68  jl       0x3b6e40  ; -> 003B6E40
003B6E6A  mov      r13, qword ptr [rsp + 0x58]
003B6E6F  mov      r15, qword ptr [rsp + 0x20]
003B6E74  mov      r14, qword ptr [rsp + 0x60]
003B6E79  mov      rdi, qword ptr [rsp + 0x50]
003B6E7E  test     ebp, ebp
003B6E80  jle      0x3b6ea7  ; -> 003B6EA7
003B6E82  mov      rcx, rbx
003B6E85  mov      edx, ebp
003B6E87  mov      rax, qword ptr [rbx]
003B6E8A  test     byte ptr [rax + 9], 8
003B6E8E  jne      0x3b6e9d  ; -> 003B6E9D
003B6E90  mov      qword ptr [rcx], rax
003B6E93  inc      esi
003B6E95  or       byte ptr [rax + 9], 8
003B6E99  add      rcx, 8
003B6E9D  add      rbx, 8
003B6EA1  sub      rdx, 1
003B6EA5  jne      0x3b6e87  ; -> 003B6E87
003B6EA7  mov      ecx, r12d
003B6EAA  mov      dword ptr [rip + 0x2b05dbf], r12d  ; -> 02EBCC70
003B6EB1  call     0x3588b0  ; -> 003588B0 fn
003B6EB6  mov      qword ptr [rip + 0x2b05dab], rax  ; -> 02EBCC68
003B6EBD  mov      dword ptr [rip + 0x2b05cfd], esi  ; -> 02EBCBC0
003B6EC3  add      rsp, 0x28
003B6EC7  pop      r12
003B6EC9  pop      rsi
003B6ECA  pop      rbp
003B6ECB  pop      rbx
003B6ECC  ret      
```
