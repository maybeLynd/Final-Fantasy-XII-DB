# F-interior pack: `22-Middleware-PhyreEngine/Phyre-Asset-Container/CONTRACT-phyre-cluster-header.md`

Generated 2026-10-02 10:27 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/contract-phyre-cluster-header.json`.

Functions: 4. Each is cited on the page only at its entry and is still in the F frontier.

## 00584E10 (67 B, extent 00584E10-00584E53)

Page context: "33390', the ordinary MSVC vtable-swap-then-destroy shape. **'00D249A8' is a VTABLE, in '.rdata', and it is complete.** Its eleven slots are all listed functions - '00584C20', '0016D680', '005C5230', '00584E10', '00584D30', '00584C50', '00584C70', '00584E60', '0062EFD0', '0062F080', '00584DB0' - and the qword before it, '00D249A0' = '01CF15C0', is the RTTI Complete Object Locator. **RTTI NAMES THE CLASS.** Locator '01CF15C0' → TypeDescri"

```
00584E10  push     rbx
00584E12  sub      rsp, 0x20
00584E16  mov      rcx, rdx
00584E19  mov      rbx, r8
00584E1C  call     0x599770  ; -> 00599770 fn
00584E21  movups   xmm0, xmmword ptr [rax]
00584E24  movups   xmmword ptr [rbx], xmm0
00584E27  movups   xmm1, xmmword ptr [rax + 0x10]
00584E2B  movups   xmmword ptr [rbx + 0x10], xmm1
00584E2F  movups   xmm0, xmmword ptr [rax + 0x20]
00584E33  movups   xmmword ptr [rbx + 0x20], xmm0
00584E37  movups   xmm1, xmmword ptr [rax + 0x30]
00584E3B  movups   xmmword ptr [rbx + 0x30], xmm1
00584E3F  movups   xmm0, xmmword ptr [rax + 0x40]
00584E43  movups   xmmword ptr [rbx + 0x40], xmm0
00584E47  mov      eax, dword ptr [rax + 0x50]
00584E4A  mov      dword ptr [rbx + 0x50], eax
00584E4D  add      rsp, 0x20
00584E51  pop      rbx
00584E52  ret      
```

## 0062F080 (27 B, extent 0062F080-0062F09B)

Page context: "s a VTABLE, in '.rdata', and it is complete.** Its eleven slots are all listed functions - '00584C20', '0016D680', '005C5230', '00584E10', '00584D30', '00584C50', '00584C70', '00584E60', '0062EFD0', '0062F080', '00584DB0' - and the qword before it, '00D249A0' = '01CF15C0', is the RTTI Complete Object Locator. **RTTI NAMES THE CLASS.** Locator '01CF15C0' → TypeDescriptor '01F498A0' → '.?AV?$PClassDescriptorConcrete@VPClusterHeader@PBinar"

```
0062F080  mov      rcx, qword ptr [rdx + 8]
0062F084  add      rdx, 8
0062F088  mov      rax, qword ptr [rdx + 8]
0062F08C  mov      qword ptr [rcx + 8], rax
0062F090  mov      qword ptr [rax], rcx
0062F093  mov      qword ptr [rdx], rdx
0062F096  mov      qword ptr [rdx + 8], rdx
0062F09A  ret      
```

## 0067ADD0 (89 B, extent 0067ADD0-0067AE29)

Page context: "unction | size | role (call-signature read) | |---|---:|---| | '001C22A0' | 962 | cluster field-pair copy 'rdx'/'rcx' at '+0x10..0x30': '0017D260' x2, '001C19A0', '00584730' x3 (CRT init/finalizer), '0067ADD0' |  ## SWE2-EC7-20 update (2026-09-18) — loader-side fragment set: '005CD5E0', '005CD0E0', '0059BED0', '00599670'  '005CD5E0' (98 B) is an IAT-driven create-probe: 'rcx = [rcx]' dereferences the handle slot, then 'call [008C2198]' "

```
0067ADD0  push     rbx
0067ADD2  sub      rsp, 0x20
0067ADD6  mov      eax, dword ptr [rdx + 0x10]
0067ADD9  mov      rbx, rcx
0067ADDC  mov      dword ptr [rcx + 0x10], eax
0067ADDF  test     eax, eax
0067ADE1  je       0x67ae20  ; -> 0067AE20
0067ADE3  mov      qword ptr [rsp + 0x30], rdi
0067ADE8  xor      edi, edi
0067ADEA  cmp      dword ptr [rdx + 0x10], edi
0067ADED  cmovne   rdi, qword ptr [rdx + 8]
0067ADF2  mov      edx, dword ptr [rdx]
0067ADF4  btr      edx, 0x1f
0067ADF8  call     0x67b100  ; -> 0067B100 fn
0067ADFD  mov      rcx, qword ptr [rbx + 8]
0067AE01  test     rcx, rcx
0067AE04  je       0x67ae12  ; -> 0067AE12
0067AE06  mov      r8d, dword ptr [rbx + 0x10]
0067AE0A  mov      rdx, rdi
0067AE0D  call     0x861eba  ; -> 00861EBA fn
0067AE12  mov      rax, rbx
0067AE15  mov      rdi, qword ptr [rsp + 0x30]
0067AE1A  add      rsp, 0x20
0067AE1E  pop      rbx
0067AE1F  ret      
0067AE20  mov      rax, rbx
0067AE23  add      rsp, 0x20
0067AE27  pop      rbx
0067AE28  ret      
```

## 006CC920 (56 B, extent 006CC920-006CC958)

Page context: "t a deleter. Callers '005FE1A0'/'00600D20'/'00600E30'/'00609720'/'00610210'/'006793E0'/'006794D0'/ '00679BF0'/'0067A240'/'0067A440'/'0067A480'/'0067A970'/'0067A9B0'/'006CC550'/ '006CC670'/'006CC710'/'006CC920' — the movie-loader object family.  '005CD0E0' (126 B) is the event-handle creator: 'edx' bit 1 shifts down as the manual-reset flag and 'not edx & 1' as the initial-state flag ('005CD0E6'.. '005CD0F5'), 'call [008C21A8]' creates t"

```
006CC920  sub      rsp, 0x28
006CC924  movzx    eax, byte ptr [rcx + 0x48]
006CC928  test     al, al
006CC92A  je       0x6cc951  ; -> 006CC951
006CC92C  mov      qword ptr [rsp + 0x20], rbx
006CC931  lea      rbx, [rcx + 0x28]
006CC935  mov      rcx, rbx
006CC938  call     0x5cd840  ; -> 005CD840 fn
006CC93D  mov      rcx, rbx
006CC940  call     0x5cd5e0  ; -> 005CD5E0 fn
006CC945  mov      rbx, qword ptr [rsp + 0x20]
006CC94A  mov      al, 1
006CC94C  add      rsp, 0x28
006CC950  ret      
006CC951  xor      al, al
006CC953  add      rsp, 0x28
006CC957  ret      
```
