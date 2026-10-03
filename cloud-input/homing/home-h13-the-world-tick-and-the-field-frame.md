# Homing pack: `00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md`

Generated 2026-10-03 13:52 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h13-the-world-tick-and-the-field-frame.json`.

Bodies: 6. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00287850 (72 B, extent 00287850-00287898)

Entered from (direct sites whose caller this page cites): `002878E0` + 0x11D (call; `002878E0` is cited on this page)
Other direct sites: none

Host context: "'0022A770'/'0022B8C0'/'0022BC20')  '0027E9E0' (142 B) — reached through '0022A770', '0022B8C0' and '0022BC20' — is the '0209AC18' singleton ensure: while the slot is null it allocates '00244F50(0xC0, 002878E0)', publishes the object, sets '0209AC50' and '0209AC14' to 1, initialises via '00247570(obj, 0)', then registers it into the '0208EA40' bank with '00246AD0(bank, obj)' — stack-cookie protected throughout. Interior anchor '0027EA1F'"

```
00287850  push     rbx
00287852  sub      rsp, 0x20
00287856  xor      ebx, ebx
00287858  test     rcx, rcx
0028785B  jne      0x287861  ; -> 00287861
0028785D  mov      eax, ebx
0028785F  jmp      0x287869  ; -> 00287869
00287861  mov      rax, qword ptr [rcx + 0x60]
00287865  mov      rax, qword ptr [rax + 0x50]
00287869  mov      rax, qword ptr [rax + 0x18]
0028786D  test     rax, rax
00287870  je       0x28787a  ; -> 0028787A
00287872  mov      rax, qword ptr [rax + 0x60]
00287876  mov      rbx, qword ptr [rax + 0x10]
0028787A  mov      ecx, 0xd3e
0028787F  call     0x2f9860  ; -> 002F9860 fn
00287884  xor      ecx, ecx
00287886  mov      qword ptr [rbx + 0x18], rax
0028788A  call     0x20e620  ; -> 0020E620 fn
0028788F  mov      dword ptr [rbx + 0x20], eax
00287892  add      rsp, 0x20
00287896  pop      rbx
00287897  ret      
```

## 002EDD70 (67 B, extent 002EDD70-002EDDB3)

Entered from (direct sites whose caller this page cites): `002E4A40` + 0x104 (call; `002E4A40` is cited on this page); `002E4A40` + 0x11D (call; `002E4A40` is cited on this page); `002E4A40` + 0x139 (call; `002E4A40` is cited on this page); `002E4A40` + 0x150 (call; `002E4A40` is cited on this page)
Other direct sites: none

Host context: "5F1AF' — run near the frame's tail | ['002E1BA0'](../../_index/ADDRESS-INDEX.md) | | '0037CF00' (67 B) | 4-iteration clear pass: '00263750(i)' for i in 0..3, non-null entries get '002E49B0(obj,0)' + '002E4A40(obj)' | ['0037CF12'](../../_index/ADDRESS-INDEX.md) |  '001EBA40' (the '0x2E0' lazy singleton) and the '0024B9B0'/'0036C1D0'/'0036C140' helpers are shared callees with other callers — deliberately not census members.   ### The '002" / "5F1AF' — run near the frame's tail | ['002E1BA0'](../../_index/ADDRESS-INDEX.md) | | '0037CF00' (67 B) | 4-iteration clear pass: '00263750(i)' for i in 0..3, non-null entries get '002E49B0(obj,0)' + '002E4A40(obj)' | ['0037CF12'](../../_index/ADDRESS-INDEX.md) |  '001EBA40' (the '0x2E0' lazy singleton) and the '0024B9B0'/'0036C1D0'/'0036C140' helpers are shared callees with other callers — deliberately not census members.   ### The '002"

```
002EDD70  cmp      cx, -1
002EDD74  je       0x2eddb2  ; -> 002EDDB2
002EDD76  movsx    rax, cx
002EDD7A  imul     rcx, rax, 0x740
002EDD81  add      rcx, qword ptr [rip + 0x1fd91a0]  ; -> 022C6F28
002EDD88  je       0x2eddb2  ; -> 002EDDB2
002EDD8A  cmp      dword ptr [rcx + 0x284], 0
002EDD91  je       0x2eddb2  ; -> 002EDDB2
002EDD93  or       dword ptr [rcx + 0x290], 8
002EDD9A  movss    dword ptr [rcx + 0x380], xmm1
002EDDA2  movss    dword ptr [rcx + 0x384], xmm2
002EDDAA  movss    dword ptr [rcx + 0x388], xmm3
002EDDB2  ret      
```

## 003EB250 (533 B, extent 003EB250-003EB465)

Entered from (direct sites whose caller this page cites): `003EB190` + 0x52 (call; `003EB190` is cited on this page)
Other direct sites: `0050E2D0` + 0x1B (call)

Host context: "' on it; returns 1 on every path past the first guard | Interior anchor '002EC639'; Interior anchor '002EC641'; Interior anchor '002EC64B'; Interior anchor '002EC65B'; Interior anchor '002EC664' | | '003EB190' | 111 B | does nothing when 'ecx' is above 0x1f (unsigned); otherwise, when qword slot '02B5EA20[ecx]' (stride 8) is non-null, calls '003EB470' on it and clears the slot, then stores into the slot, and returns, the result of the c"

```
003EB250  push     rbx
003EB252  sub      rsp, 0x30
003EB256  mov      rbx, qword ptr [rip + 0x2773913]  ; -> 02B5EB70
003EB25D  mov      r11d, r8d
003EB260  test     rcx, rcx
003EB263  je       0x3eb45c  ; -> 003EB45C
003EB269  test     rbx, rbx
003EB26C  je       0x3eb45c  ; -> 003EB45C
003EB272  mov      r10, qword ptr [rbx]
003EB275  mov      rax, qword ptr [rbx + 8]
003EB279  mov      qword ptr [rsp + 0x40], rsi
003EB27E  mov      qword ptr [rsp + 0x48], rdi
003EB283  test     r10, r10
003EB286  je       0x3eb28c  ; -> 003EB28C
003EB288  mov      qword ptr [r10 + 8], rax
003EB28C  test     rax, rax
003EB28F  je       0x3eb294  ; -> 003EB294
003EB291  mov      qword ptr [rax], r10
003EB294  xor      esi, esi
003EB296  mov      qword ptr [rbx], rsi
003EB299  mov      qword ptr [rbx + 8], rsi
003EB29D  mov      rax, qword ptr [rip + 0x277387c]  ; -> 02B5EB20
003EB2A4  mov      qword ptr [rip + 0x2773875], rbx  ; -> 02B5EB20
003EB2AB  test     rax, rax
003EB2AE  je       0x3eb2b4  ; -> 003EB2B4
003EB2B0  mov      qword ptr [rax + 8], rbx
003EB2B4  mov      byte ptr [rbx + 0x41], dl
003EB2B7  lea      r8, [rip + 0x2773862]  ; -> 02B5EB20
003EB2BE  mov      qword ptr [rbx + 8], r8
003EB2C2  mov      edx, r11d
003EB2C5  mov      qword ptr [rbx], rax
003EB2C8  mov      r8d, r9d
003EB2CB  mov      byte ptr [rbx + 0x40], 1
003EB2CF  mov      qword ptr [rbx + 0x18], rcx
003EB2D3  inc      word ptr [rcx + 0x1c]
003EB2D7  and      byte ptr [rcx + 0x18], 0xfb
003EB2DB  mov      eax, dword ptr [rcx + 0x14]
003EB2DE  mov      dword ptr [rip + 0x1b94224], eax  ; -> 01F7F508
003EB2E4  mov      ecx, dword ptr [rcx + 0x10]
003EB2E7  call     0x2ed4e0  ; -> 002ED4E0 fn
003EB2EC  mov      dword ptr [rbx + 0x10], eax
003EB2EF  mov      dword ptr [rip + 0x1b94213], esi  ; -> 01F7F508
003EB2F5  movzx    eax, word ptr [rbx + 0x10]
003EB2F9  cmp      ax, -1
003EB2FD  je       0x3eb322  ; -> 003EB322
003EB2FF  movsx    rax, ax
003EB303  imul     rcx, rax, 0x740
003EB30A  add      rcx, qword ptr [rip + 0x1edbc17]  ; -> 022C6F28
003EB311  je       0x3eb322  ; -> 003EB322
003EB313  cmp      dword ptr [rcx + 0x284], esi
003EB319  je       0x3eb322  ; -> 003EB322
003EB31B  mov      qword ptr [rcx + 0x108], rsi
003EB322  movzx    eax, word ptr [rbx + 0x10]
003EB326  mov      rsi, qword ptr [rsp + 0x40]
003EB32B  cmp      ax, -1
003EB32F  je       0x3eb355  ; -> 003EB355
003EB331  movsx    rax, ax
003EB335  imul     rcx, rax, 0x740
003EB33C  add      rcx, qword ptr [rip + 0x1edbbe5]  ; -> 022C6F28
003EB343  je       0x3eb355  ; -> 003EB355
003EB345  cmp      dword ptr [rcx + 0x284], 0
003EB34C  je       0x3eb355  ; -> 003EB355
003EB34E  xor      edx, edx
003EB350  call     0x3e5e20  ; -> 003E5E20 fn
003EB355  movzx    eax, word ptr [rbx + 0x10]
003EB359  cmp      ax, -1
003EB35D  je       0x3eb383  ; -> 003EB383
003EB35F  movsx    rax, ax
003EB363  imul     rcx, rax, 0x740
003EB36A  add      rcx, qword ptr [rip + 0x1edbbb7]  ; -> 022C6F28
003EB371  je       0x3eb383  ; -> 003EB383
003EB373  cmp      dword ptr [rcx + 0x284], 0
003EB37A  je       0x3eb383  ; -> 003EB383
003EB37C  mov      byte ptr [rcx + 0x413], 0
003EB383  movzx    eax, word ptr [rbx + 0x10]
003EB387  movaps   xmmword ptr [rsp + 0x20], xmm6
003EB38C  cmp      ax, -1
003EB390  jne      0x3eb39c  ; -> 003EB39C
003EB392  movss    xmm6, dword ptr [rip + 0x50d9e6]  ; -> 008F8D80 [f32 30]
003EB39A  jmp      0x3eb3d5  ; -> 003EB3D5
003EB39C  movsx    rax, ax
003EB3A0  imul     rcx, rax, 0x740
003EB3A7  add      rcx, qword ptr [rip + 0x1edbb7a]  ; -> 022C6F28
003EB3AE  jne      0x3eb3ba  ; -> 003EB3BA
003EB3B0  movss    xmm6, dword ptr [rip + 0x50d9c8]  ; -> 008F8D80 [f32 30]
003EB3B8  jmp      0x3eb3d5  ; -> 003EB3D5
003EB3BA  cmp      dword ptr [rcx + 0x284], 0
003EB3C1  jne      0x3eb3cd  ; -> 003EB3CD
003EB3C3  movss    xmm6, dword ptr [rip + 0x50d9b5]  ; -> 008F8D80 [f32 30]
003EB3CB  jmp      0x3eb3d5  ; -> 003EB3D5
003EB3CD  call     0x423280  ; -> 00423280 fn
003EB3D2  movaps   xmm6, xmm0
003EB3D5  xor      edx, edx
003EB3D7  lea      rcx, [rbx + 0x10]
003EB3DB  call     0x2e8340  ; -> 002E8340 fn
003EB3E0  movss    xmm1, dword ptr [rip + 0x19007c0]  ; -> 01CEBBA8 [f32 1]
003EB3E8  movzx    ecx, word ptr [rbx + 0x10]
003EB3EC  movaps   xmm3, xmm1
003EB3EF  movaps   xmm2, xmm1
003EB3F2  call     0x2ee050  ; -> 002EE050 fn
003EB3F7  movzx    eax, word ptr [rbx + 0x10]
003EB3FB  cmp      ax, -1
003EB3FF  je       0x3eb426  ; -> 003EB426
003EB401  movsx    rax, ax
003EB405  imul     rcx, rax, 0x740
003EB40C  add      rcx, qword ptr [rip + 0x1edbb15]  ; -> 022C6F28
003EB413  je       0x3eb426  ; -> 003EB426
003EB415  cmp      dword ptr [rcx + 0x284], 0
003EB41C  je       0x3eb426  ; -> 003EB426
003EB41E  movaps   xmm1, xmm6
003EB421  call     0x427300  ; -> 00427300 fn
003EB426  movzx    eax, word ptr [rbx + 0x10]
003EB42A  movaps   xmm6, xmmword ptr [rsp + 0x20]
003EB42F  mov      rdi, qword ptr [rsp + 0x48]
003EB434  cmp      ax, -1
003EB438  je       0x3eb45c  ; -> 003EB45C
003EB43A  movsx    rcx, ax
003EB43E  imul     rcx, rcx, 0x740
003EB445  add      rcx, qword ptr [rip + 0x1edbadc]  ; -> 022C6F28
003EB44C  je       0x3eb45c  ; -> 003EB45C
003EB44E  cmp      dword ptr [rcx + 0x284], 0
003EB455  je       0x3eb45c  ; -> 003EB45C
003EB457  call     0x426e20  ; -> 00426E20 fn
003EB45C  mov      rax, rbx
003EB45F  add      rsp, 0x30
003EB463  pop      rbx
003EB464  ret      
```

## 003ED7F0 (39 B, extent 003ED7F0-003ED817)

Entered from (direct sites whose caller this page cites): `0036F530` + 0x14 (jmp; `0036F530` is cited on this page)
Other direct sites: `0036F410` + 0x17 (jmp)

Host context: " pair '0036C1D0'/'0036C140'), '003D83A0' (2,190 B: '0020E600' ×3 + 'sqrtf' ×2 + '00430B90'/'004309C0'/'0036DD80'), '003D9150' (float step: '00861F1A' + '0025A520'/'0025A500'/'0025A2C0'), '0036F460', '0036F530', '0037A450', '0037D4C0', '0037D970', '003ECAC0', '003ECCA0', '004678E0', '00468520', '003CD820' | the frame's parameter evaluators and camera-bank ('02AED5F0'–'02AED604', '02AEDF10'–'18', '02CA6010'/'20') writers; '003ECCA0'→'003E"

```
003ED7F0  mov      eax, dword ptr [rip + 0x2acdfda]  ; -> 02EBB7D0
003ED7F6  test     eax, eax
003ED7F8  js       0x3ed816  ; -> 003ED816
003ED7FA  movups   xmm0, xmmword ptr [rip + 0x2acdfcf]  ; -> 02EBB7D0
003ED801  or       edx, 0xffffffff
003ED804  test     ecx, ecx
003ED806  movups   xmmword ptr [rip + 0x2acdfd3], xmm0  ; -> 02EBB7E0
003ED80D  cmovne   eax, edx
003ED810  mov      dword ptr [rip + 0x2acdfba], eax  ; -> 02EBB7D0
003ED816  ret      
```

## 00466C80 (47 B, extent 00466C80-00466CAF)

Entered from (direct sites whose caller this page cites): `00473490` + 0x17 (call; `00473490` is cited on this page)
Other direct sites: none

Host context: "ith ('rdx', 'r8d', 'r9d', the fifth (stack) argument) | Interior anchor '003EB193'; Interior anchor '003EB1C9'; Interior anchor '003EB1CE'; Interior anchor '003EB1E2'; Interior anchor '003EB1F1' | | '00473490' | 43 B | calls '00466C40(ecx)', then the call at '00473490' + 0x17 with the same 'ecx', and returns in 'xmm0' the second float minus the first | Interior anchor '0047349D'; Interior anchor '004734A7'; Interior anchor '004734AC' | "

```
00466C80  test     ecx, ecx
00466C82  js       0x466cab  ; -> 00466CAB
00466C84  cmp      ecx, dword ptr [rip + 0x2a54a56]  ; -> 02EBB6E0
00466C8A  jge      0x466cab  ; -> 00466CAB
00466C8C  movsxd   rax, ecx
00466C8F  lea      rcx, [rax + rax*4]
00466C93  shl      rcx, 4
00466C97  add      rcx, qword ptr [rip + 0x2a54a52]  ; -> 02EBB6F0
00466C9E  cmp      qword ptr [rcx + 8], 0
00466CA3  je       0x466cab  ; -> 00466CAB
00466CA5  movss    xmm0, dword ptr [rcx + 0x44]
00466CAA  ret      
00466CAB  xorps    xmm0, xmm0
00466CAE  ret      
```

## 00467620 (61 B, extent 00467620-0046765D)

Entered from (direct sites whose caller this page cites): `00473500` + 0xCA (jmp; `00473500` is cited on this page)
Other direct sites: `00473600` + 0x2 (jmp)

Host context: "that writes '022C7FE0'–'022C8028' | | '003Exxxx' perception update | '003E7EC0' ('02B5D080' gate), '003E8020', '003E8440', '003E85B0', '003E8690', '003E8990', '003EB9A0' | '003E8190' ×N + '004735D0'/'00473500' + '0037A2xx'/'0037Bxxx' + '0026FAxx'/'002700F0' shape; '003E8A10'/'40'/'70' are 38-byte two-arm conditional forwarders ('test edx,edx; je' → call A else call B, 'ecx=0') — '003E8A10' selects between the '0037A3B0' pair, '003E8A40'"

```
00467620  test     ecx, ecx
00467622  js       0x46765c  ; -> 0046765C
00467624  cmp      ecx, dword ptr [rip + 0x2a540b6]  ; -> 02EBB6E0
0046762A  jge      0x46765c  ; -> 0046765C
0046762C  movsxd   rax, ecx
0046762F  lea      rcx, [rax + rax*4]
00467633  shl      rcx, 4
00467637  add      rcx, qword ptr [rip + 0x2a540b2]  ; -> 02EBB6F0
0046763E  cmp      qword ptr [rcx + 8], 0
00467643  je       0x46765c  ; -> 0046765C
00467645  and      dword ptr [rcx + 0x4c], 0xfffffffe
00467649  and      edx, 1
0046764C  mov      eax, edx
0046764E  shl      edx, 4
00467651  or       eax, dword ptr [rcx + 0x4c]
00467654  and      eax, 0xffffffef
00467657  or       eax, edx
00467659  mov      dword ptr [rcx + 0x4c], eax
0046765C  ret      
```
