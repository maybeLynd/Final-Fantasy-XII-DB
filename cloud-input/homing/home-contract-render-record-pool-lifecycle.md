# Homing pack: `17-Presentation-Rendering/CONTRACT-render-record-pool-lifecycle.md`

Generated 2026-10-03 06:31 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-contract-render-record-pool-lifecycle.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00370890 (777 B, extent 00370890-00370B99)

Entered from (direct sites whose caller this page cites): `0046E300` + 0x39 (call; `0046E300` is cited on this page)
Other direct sites: none

Host context: "'0018722F' (the first cofactor difference).  ## SWE2-EC7-53 update (2026-09-19) - '00421B00'  '00421B00' (450 B) is a render-record-pool body - '0020E600'/'002ED570'/'003B30A0'/'003E5CF0'/'004209A0'/'0046E300'/'0046E370' plus '022C6F28'. Interior anchor '00421B15' (a '0020E600' call).  ## SWE2-EC7-54 update (2026-09-19) - '005EB670'  '005EB670' (321 B) is a call-free 4x4 matrix transpose - '[rdx]'/'+0x10'/'+0x20'/'+0x30' rows published "

```
00370890  mov      qword ptr [rsp + 8], rbx
00370895  mov      qword ptr [rsp + 0x10], rbp
0037089A  mov      qword ptr [rsp + 0x18], rsi
0037089F  push     rdi
003708A0  push     r12
003708A2  push     r13
003708A4  push     r14
003708A6  push     r15
003708A8  sub      rsp, 0x50
003708AC  or       r13d, 0xffffffff
003708B0  xor      r12d, r12d
003708B3  mov      rbp, rdx
003708B6  mov      r14, rcx
003708B9  test     rdx, rdx
003708BC  je       0x370956  ; -> 00370956
003708C2  mov      eax, dword ptr [rcx + 4]
003708C5  cmp      dword ptr [rdx + 0x10], eax
003708C8  jne      0x370956  ; -> 00370956
003708CE  mov      ecx, dword ptr [rdx + 0x84]
003708D4  mov      dword ptr [rdx + 0x10], r13d
003708D8  call     0x20e600  ; -> 0020E600 fn
003708DD  mov      ecx, dword ptr [rbp + 0x84]
003708E3  mov      r15, rax
003708E6  call     0x20e600  ; -> 0020E600 fn
003708EB  movsx    rcx, word ptr [rbp + 0x88]
003708F3  mov      edi, r12d
003708F6  imul     rsi, rcx, 0x290
003708FD  add      rsi, rax
00370900  cmp      r12w, word ptr [rbp + 0x8a]
00370908  jge      0x370956  ; -> 00370956
0037090A  nop      word ptr [rax + rax]
00370910  movsx    rcx, word ptr [rsi]
00370914  imul     rbx, rcx, 0x290
0037091B  mov      ecx, dword ptr [rbx + r15 + 0x278]
00370923  call     0x20e600  ; -> 0020E600 fn
00370928  test     rax, rax
0037092B  je       0x370945  ; -> 00370945
0037092D  xor      ecx, ecx
0037092F  call     0x20e620  ; -> 0020E620 fn
00370934  mov      dword ptr [rbx + r15 + 0x278], eax
0037093C  mov      word ptr [rbx + r15 + 0x27c], r13w
00370945  movsx    eax, word ptr [rbp + 0x8a]
0037094C  inc      edi
0037094E  add      rsi, 2
00370952  cmp      edi, eax
00370954  jl       0x370910  ; -> 00370910
00370956  mov      ecx, dword ptr [r14 + 0x84]
0037095D  mov      dword ptr [r14 + 8], r13d
00370961  mov      word ptr [r14 + 0x14], r13w
00370966  call     0x20e600  ; -> 0020E600 fn
0037096B  mov      rbp, rax
0037096E  lea      rcx, [rax + 0x1f0]
00370975  call     0x46d110  ; -> 0046D110 fn
0037097A  mov      ecx, dword ptr [r14 + 0xa0]
00370981  call     0x20e600  ; -> 0020E600 fn
00370986  test     rax, rax
00370989  je       0x370b7b  ; -> 00370B7B
0037098F  mov      ecx, dword ptr [r14 + 0x84]
00370996  call     0x20e600  ; -> 0020E600 fn
0037099B  movsx    rcx, word ptr [r14 + 0x88]
003709A3  imul     rsi, rcx, 0x290
003709AA  mov      ecx, dword ptr [r14 + 0xa0]
003709B1  add      rsi, rax
003709B4  call     0x20e600  ; -> 0020E600 fn
003709B9  lea      r15, [rax + 0x30]
003709BD  cmp      r12w, word ptr [r14 + 0x8a]
003709C5  jge      0x370b46  ; -> 00370B46
003709CB  movaps   xmmword ptr [rsp + 0x40], xmm6
003709D0  movaps   xmmword ptr [rsp + 0x30], xmm7
003709D5  movaps   xmmword ptr [rsp + 0x20], xmm8
003709DB  nop      dword ptr [rax + rax]
003709E0  movsx    rcx, word ptr [rsi]
003709E4  imul     rbx, rcx, 0x290
003709EB  add      rbx, rbp
003709EE  and      word ptr [rbx + 0x280], 0xfff5
003709F6  mov      ecx, dword ptr [r14 + 0xa0]
003709FD  call     0x20e600  ; -> 0020E600 fn
00370A02  test     rax, rax
00370A05  je       0x370b1e  ; -> 00370B1E
00370A0B  movsx    rax, word ptr [rbx + 0x27e]
00370A13  lea      rcx, [rbx + 0x1f0]
00370A1A  imul     rdi, rax, 0x4c
00370A1E  add      rdi, r15
00370A21  movzx    eax, word ptr [rdi + 0x20]
00370A25  mov      word ptr [rbx + 0x270], ax
00370A2C  mov      word ptr [rbx + 0x276], r13w
00370A34  call     0x46d110  ; -> 0046D110 fn
00370A39  test     byte ptr [rbx + 0x280], 2
00370A40  mov      rax, rbx
00370A43  movss    xmm6, dword ptr [rdi + 0x3c]
00370A48  movss    xmm7, dword ptr [rdi + 0x38]
00370A4D  movss    xmm8, dword ptr [rdi + 0x34]
00370A53  jne      0x370a88  ; -> 00370A88
00370A55  movss    dword ptr [rax + 0x190], xmm8
00370A5E  movss    dword ptr [rax + 0x194], xmm7
00370A66  movss    dword ptr [rax + 0x198], xmm6
00370A6E  mov      dword ptr [rax + 0x19c], 0x3f800000
00370A78  mov      ecx, dword ptr [rax + 0x278]
00370A7E  call     0x20e600  ; -> 0020E600 fn
00370A83  test     rax, rax
00370A86  jne      0x370a55  ; -> 00370A55
00370A88  test     byte ptr [rbx + 0x280], 2
00370A8F  mov      rax, rbx
00370A92  movss    xmm6, dword ptr [rdi + 0x30]
00370A97  movss    xmm7, dword ptr [rdi + 0x2c]
00370A9C  movss    xmm8, dword ptr [rdi + 0x28]
00370AA2  jne      0x370ad7  ; -> 00370AD7
00370AA4  movss    dword ptr [rax + 0x1b0], xmm8
00370AAD  movss    dword ptr [rax + 0x1b4], xmm7
00370AB5  movss    dword ptr [rax + 0x1b8], xmm6
00370ABD  mov      dword ptr [rax + 0x1bc], 0x3f800000
00370AC7  mov      ecx, dword ptr [rax + 0x278]
00370ACD  call     0x20e600  ; -> 0020E600 fn
00370AD2  test     rax, rax
00370AD5  jne      0x370aa4  ; -> 00370AA4
00370AD7  test     byte ptr [rbx + 0x280], 2
00370ADE  movss    xmm6, dword ptr [rdi + 0x40]
00370AE3  jne      0x370b1e  ; -> 00370B1E
00370AE5  movss    dword ptr [rbx + 0x1d0], xmm6
00370AED  mov      dword ptr [rbx + 0x1d4], 0x3f800000
00370AF7  mov      dword ptr [rbx + 0x1d8], 0x3f800000
00370B01  mov      dword ptr [rbx + 0x1dc], 0x3f800000
00370B0B  mov      ecx, dword ptr [rbx + 0x278]
00370B11  call     0x20e600  ; -> 0020E600 fn
00370B16  mov      rbx, rax
00370B19  test     rax, rax
00370B1C  jne      0x370ae5  ; -> 00370AE5
00370B1E  movsx    eax, word ptr [r14 + 0x8a]
00370B26  inc      r12d
00370B29  add      rsi, 2
00370B2D  cmp      r12d, eax
00370B30  jl       0x3709e0  ; -> 003709E0
00370B36  movaps   xmm8, xmmword ptr [rsp + 0x20]
00370B3C  movaps   xmm7, xmmword ptr [rsp + 0x30]
00370B41  movaps   xmm6, xmmword ptr [rsp + 0x40]
00370B46  mov      ecx, dword ptr [r14 + 0xa0]
00370B4D  call     0x20e600  ; -> 0020E600 fn
00370B52  test     rax, rax
00370B55  je       0x370b7b  ; -> 00370B7B
00370B57  mov      rcx, r14
00370B5A  call     0x3723b0  ; -> 003723B0 fn
00370B5F  mov      ecx, dword ptr [r14 + 0xa0]
00370B66  call     0x20e600  ; -> 0020E600 fn
00370B6B  mov      rcx, r14
00370B6E  call     0x373d00  ; -> 00373D00 fn
00370B73  mov      rcx, r14
00370B76  call     0x373ea0  ; -> 00373EA0 fn
00370B7B  lea      r11, [rsp + 0x50]
00370B80  mov      rbx, qword ptr [r11 + 0x30]
00370B84  mov      rbp, qword ptr [r11 + 0x38]
00370B88  mov      rsi, qword ptr [r11 + 0x40]
00370B8C  mov      rsp, r11
00370B8F  pop      r15
00370B91  pop      r14
00370B93  pop      r13
00370B95  pop      r12
00370B97  pop      rdi
00370B98  ret      
```

## 00370BA0 (14 B, extent 00370BA0-00370BAE)

Entered from (direct sites whose caller this page cites): `0046E370` + 0x39 (call; `0046E370` is cited on this page)
Other direct sites: none

Host context: "(the first cofactor difference).  ## SWE2-EC7-53 update (2026-09-19) - '00421B00'  '00421B00' (450 B) is a render-record-pool body - '0020E600'/'002ED570'/'003B30A0'/'003E5CF0'/'004209A0'/'0046E300'/'0046E370' plus '022C6F28'. Interior anchor '00421B15' (a '0020E600' call).  ## SWE2-EC7-54 update (2026-09-19) - '005EB670'  '005EB670' (321 B) is a call-free 4x4 matrix transpose - '[rdx]'/'+0x10'/'+0x20'/'+0x30' rows published column-wise"

```
00370BA0  cmp      dword ptr [rcx + 0x9c], 2
00370BA7  je       0x373380  ; -> 00373380 fn
00370BAD  ret      
```
