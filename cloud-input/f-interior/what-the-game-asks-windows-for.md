# F-interior pack: `24-Compiler-And-CRT-Runtime/Runtime-Service-Surface/what-the-game-asks-windows-for.md`

Generated 2026-10-02 18:33 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/what-the-game-asks-windows-for.json`.

Functions: 9. Each is cited on the page only at its entry and is still in the F frontier.

## 001597E0 (129 B, extent 001597E0-00159861)

Page context: "'ebp = 1' separator flag only when the left part does not already end in '\' and the right part does not begin with one, '(len1 + sep + len2) * 2 + pad' sized allocation through IAT '008C2348', then '001597E0'/'001599D0' copy both halves into the fresh buffer - a manual PathCombineW.  Interior anchor '0015B4D5' (function '0015B440').  '0015A240' (235 B) is the lazy OS-build cache '0015B110'/'0015B820'/'0015BB30' consult: if 'dword[02EAE"

```
001597E0  shr      rdx, 1
001597E3  mov      r11d, 0
001597E9  mov      r9, r8
001597EC  mov      eax, r11d
001597EF  je       0x1597fa  ; -> 001597FA
001597F1  cmp      rdx, 0x7fffffff
001597F8  jbe      0x1597ff  ; -> 001597FF
001597FA  mov      eax, 0x80070057
001597FF  test     eax, eax
00159801  js       0x15985f  ; -> 0015985F
00159803  mov      r10d, r11d
00159806  test     rdx, rdx
00159809  je       0x15984e  ; -> 0015984E
0015980B  mov      r8d, 0x7ffffffe
00159811  sub      r8, rdx
00159814  sub      r9, rcx
00159817  lea      rax, [r8 + rdx]
0015981B  test     rax, rax
0015981E  je       0x159849  ; -> 00159849
00159820  movzx    eax, word ptr [r9 + rcx]
00159825  test     ax, ax
00159828  je       0x159849  ; -> 00159849
0015982A  mov      word ptr [rcx], ax
0015982D  add      rcx, 2
00159831  sub      rdx, 1
00159835  jne      0x159817  ; -> 00159817
00159837  sub      rcx, 2
0015983B  mov      r10d, 0x8007007a
00159841  mov      word ptr [rcx], r11w
00159845  mov      eax, r10d
00159848  ret      
00159849  test     rdx, rdx
0015984C  jne      0x159858  ; -> 00159858
0015984E  sub      rcx, 2
00159852  mov      r10d, 0x8007007a
00159858  mov      word ptr [rcx], r11w
0015985C  mov      eax, r10d
0015985F  repz ret 
```

## 00159AA0 (101 B, extent 00159AA0-00159B05)

Page context: "-167 entries name '00159420', the module-load helper this layer owns, because the Setupapi/Advapi32/Shell32 arms all resolve their DLLs through it; that helper is itself reached from Platform bodies '00159AA0'/'00159F90'/'0015A0E0' and others - the traffic is Platform code consulting the same loader the enumeration arms use, not a shared owner of this surface.  ## SWE2-EC7-44 update (2026-09-19) - '005CCBF0'  '005CCBF0' (265 B) is a bod"

```
00159AA0  mov      qword ptr [rsp + 8], rbx
00159AA5  mov      qword ptr [rsp + 0x10], rbp
00159AAA  mov      qword ptr [rsp + 0x18], rsi
00159AAF  push     rdi
00159AB0  sub      rsp, 0x20
00159AB4  mov      ebp, edx
00159AB6  mov      rbx, rcx
00159AB9  xor      esi, esi
00159ABB  call     0x159420  ; -> 00159420 fn
00159AC0  mov      rdi, rax
00159AC3  test     rbx, rbx
00159AC6  je       0x159acd  ; -> 00159ACD
00159AC8  test     rax, rax
00159ACB  je       0x159ae4  ; -> 00159AE4
00159ACD  and      ebp, 0xffffe0f7
00159AD3  xor      edx, edx
00159AD5  mov      rcx, rax
00159AD8  mov      r8d, ebp
00159ADB  call     qword ptr [rip + 0x768887]  ; -> 008C2368 [u64 0x0000000001CCC748]
00159AE1  mov      rsi, rax
00159AE4  mov      rcx, rdi
00159AE7  call     qword ptr [rip + 0x76870b]  ; -> 008C21F8 [u64 0x0000000001CCC3BA]
00159AED  mov      rbx, qword ptr [rsp + 0x30]
00159AF2  mov      rbp, qword ptr [rsp + 0x38]
00159AF7  mov      rax, rsi
00159AFA  mov      rsi, qword ptr [rsp + 0x40]
00159AFF  add      rsp, 0x20
00159B03  pop      rdi
00159B04  ret      
```

## 00159CA0 (437 B, extent 00159CA0-00159E55)

Page context: "t the end ('01CC6D40') - the 'Class\{GUID}' enumeration used to find display adapters.  Interior anchor '0015B637' (function '0015B5F0').  '00159B10' (387 B) is the lazy 'SHGetFolderPathW' resolver ('00159CA0' calls it): zeroes a 0x20A-byte stack buffer via '00861EC0', and only when the '02EAEAE0' cache slot is empty does it '00159420'-load 'Shell32.dll' ('01CC6C20'), fetch the ordinal target through the two IAT pair-calls '008C2368'/'0"

```
00159CA0  mov      qword ptr [rsp + 0x10], rbx
00159CA5  mov      qword ptr [rsp + 0x18], rbp
00159CAA  push     rdi
00159CAB  push     r12
00159CAD  push     r13
00159CAF  sub      rsp, 0x30
00159CB3  xor      r13d, r13d
00159CB6  mov      r12, rcx
00159CB9  mov      dword ptr [rsp + 0x20], 0x24
00159CC1  mov      rbx, r13
00159CC4  mov      dword ptr [rsp + 0x24], 0x26
00159CCC  mov      dword ptr [rsp + 0x28], 0x2a
00159CD4  mov      rbp, r13
00159CD7  mov      edi, r13d
00159CDA  cmp      dword ptr [rip + 0x2d54ee0], ebx  ; -> 02EAEBC0
00159CE0  jne      0x159d5b  ; -> 00159D5B
00159CE2  lea      edx, [r13 + 2]
00159CE6  mov      r8b, 3
00159CE9  xor      ecx, ecx
00159CEB  call     qword ptr [rip + 0x76868f]  ; -> 008C2380 [u64 0x0000000001CCC784]
00159CF1  lea      edx, [r13 + 1]
00159CF5  mov      r8b, 3
00159CF8  mov      rcx, rax
00159CFB  call     qword ptr [rip + 0x76867f]  ; -> 008C2380 [u64 0x0000000001CCC784]
00159D01  lea      edx, [r13 + 0x20]
00159D05  mov      r8b, 3
00159D08  mov      rcx, rax
00159D0B  call     qword ptr [rip + 0x76866f]  ; -> 008C2380 [u64 0x0000000001CCC784]
00159D11  lea      edx, [r13 + 0x23]
00159D15  lea      rcx, [rip + 0x2d54ea4]  ; -> 02EAEBC0
00159D1C  mov      r8, rax
00159D1F  mov      dword ptr [rip + 0x2d54e97], 0x11c  ; -> 02EAEBC0
00159D29  mov      dword ptr [rip + 0x2d54e91], 6  ; -> 02EAEBC4
00159D33  mov      dword ptr [rip + 0x2d54e8b], 1  ; -> 02EAEBC8
00159D3D  mov      word ptr [rip + 0x2d54f8f], r13w  ; -> 02EAECD4
00159D45  call     qword ptr [rip + 0x76862d]  ; -> 008C2378 [u64 0x0000000001CCC76E]
00159D4B  mov      ecx, r13d
00159D4E  test     eax, eax
00159D50  sete     cl
00159D53  mov      dword ptr [rip + 0x1de824f], ecx  ; -> 01F41FA8 [u32 0x00000001]
00159D59  jmp      0x159d61  ; -> 00159D61
00159D5B  mov      ecx, dword ptr [rip + 0x1de8247]  ; -> 01F41FA8 [u32 0x00000001]
00159D61  test     ecx, ecx
00159D63  je       0x159d6f  ; -> 00159D6F
00159D65  mov      eax, 1
00159D6A  jmp      0x159e41  ; -> 00159E41
00159D6F  test     r12, r12
00159D72  je       0x159e2d  ; -> 00159E2D
00159D78  xor      r9d, r9d
00159D7B  xor      r8d, r8d
00159D7E  xor      edx, edx
00159D80  mov      rcx, r12
00159D83  mov      qword ptr [rsp + 0x50], rsi
00159D88  call     qword ptr [rip + 0x7685e2]  ; -> 008C2370 [u64 0x0000000001CCC75A]
00159D8E  mov      esi, eax
00159D90  test     eax, eax
00159D92  je       0x159e28  ; -> 00159E28
00159D98  mov      rdx, rsi
00159D9B  mov      ecx, 0x40
00159DA0  add      rdx, rdx
00159DA3  call     qword ptr [rip + 0x76859f]  ; -> 008C2348 [u64 0x0000000001CCC700]
00159DA9  mov      rbp, rax
00159DAC  test     rax, rax
00159DAF  je       0x159e28  ; -> 00159E28
00159DB1  xor      r9d, r9d
00159DB4  mov      r8, rax
00159DB7  mov      edx, esi
00159DB9  mov      rcx, r12
00159DBC  call     qword ptr [rip + 0x7685ae]  ; -> 008C2370 [u64 0x0000000001CCC75A]
00159DC2  cmp      esi, eax
00159DC4  jbe      0x159e28  ; -> 00159E28
00159DC6  mov      rsi, r13
00159DC9  nop      dword ptr [rax]
00159DD0  mov      ecx, dword ptr [rsp + rsi*4 + 0x20]
00159DD4  lea      rdx, [rip + 0x1b56b79]  ; -> 01CB0954
00159DDB  call     0x159b10  ; -> 00159B10 fn
00159DE0  mov      rbx, rax
00159DE3  test     rax, rax
00159DE6  je       0x159e28  ; -> 00159E28
00159DE8  or       rcx, 0xffffffffffffffff
00159DEC  xor      eax, eax
00159DEE  mov      rdi, rbx
00159DF1  repne scasw ax, word ptr [rdi]
00159DF4  mov      rdx, rbx
00159DF7  not      rcx
00159DFA  lea      r8, [rcx - 1]
00159DFE  mov      rcx, rbp
00159E01  call     0x861fce  ; -> 00861FCE fn
00159E06  mov      edi, r13d
00159E09  test     eax, eax
00159E0B  sete     dil
00159E0F  test     edi, edi
00159E11  jne      0x159e28  ; -> 00159E28
00159E13  mov      rcx, rbx
00159E16  call     qword ptr [rip + 0x7683dc]  ; -> 008C21F8 [u64 0x0000000001CCC3BA]
00159E1C  inc      rsi
00159E1F  mov      rbx, r13
00159E22  cmp      rsi, 3
00159E26  jl       0x159dd0  ; -> 00159DD0
00159E28  mov      rsi, qword ptr [rsp + 0x50]
00159E2D  mov      rcx, rbx
00159E30  call     qword ptr [rip + 0x7683c2]  ; -> 008C21F8 [u64 0x0000000001CCC3BA]
00159E36  mov      rcx, rbp
00159E39  call     qword ptr [rip + 0x7683b9]  ; -> 008C21F8 [u64 0x0000000001CCC3BA]
00159E3F  mov      eax, edi
00159E41  mov      rbx, qword ptr [rsp + 0x58]
00159E46  mov      rbp, qword ptr [rsp + 0x60]
00159E4B  add      rsp, 0x30
00159E4F  pop      r13
00159E51  pop      r12
00159E53  pop      rdi
00159E54  ret      
```

## 0015A650 (297 B, extent 0015A650-0015A779)

Page context: "- the hardware-key enumeration the batch-167 arms documented at name level.  Interior anchor '0015A3FD' (function '0015A330').  '00159E60' (137 B) is the wide-string heap duplicate the layer shares ('0015A650', '0015A780', '0015AC50', '0015AE60', '0015B440'): null in, null out; else 'repne scasw' for the length, '(len+1)*2' plus the '0x40' base through '008C2348', copy by '00159760', and '008C21F8' frees the buffer and returns null if t"

```
0015A650  mov      qword ptr [rsp + 0x10], rbx
0015A655  push     rdi
0015A656  sub      rsp, 0x20
0015A65A  mov      rbx, rcx
0015A65D  or       rcx, 0xffffffffffffffff
0015A661  xor      eax, eax
0015A663  lea      rdi, [rip + 0x1b6c58e]  ; -> 01CC6BF8
0015A66A  repne scasw ax, word ptr [rdi]
0015A66D  not      rcx
0015A670  lea      r9, [rcx - 1]
0015A674  test     rbx, rbx
0015A677  je       0x15a76e  ; -> 0015A76E
0015A67D  or       rcx, 0xffffffffffffffff
0015A681  mov      rdi, rbx
0015A684  mov      r11d, 0x2e
0015A68A  repne scasw ax, word ptr [rdi]
0015A68D  not      rcx
0015A690  lea      rdi, [rbx + rcx*2 - 2]
0015A695  lea      r8, [rcx - 1]
0015A699  mov      rax, rdi
0015A69C  cmp      rbx, rdi
0015A69F  jae      0x15a6bf  ; -> 0015A6BF
0015A6A1  mov      r10d, 0x5c
0015A6A7  movzx    edx, word ptr [rax]
0015A6AA  cmp      r10w, dx
0015A6AE  je       0x15a6bf  ; -> 0015A6BF
0015A6B0  cmp      r11w, dx
0015A6B4  je       0x15a6bf  ; -> 0015A6BF
0015A6B6  sub      rax, 2
0015A6BA  cmp      rbx, rax
0015A6BD  jb       0x15a6a7  ; -> 0015A6A7
0015A6BF  cmp      r11w, word ptr [rax]
0015A6C3  cmove    rdi, rax
0015A6C7  or       rcx, 0xffffffffffffffff
0015A6CB  xor      eax, eax
0015A6CD  repne scasw ax, word ptr [rdi]
0015A6D0  not      rcx
0015A6D3  sub      rcx, 1
0015A6D7  je       0x15a70f  ; -> 0015A70F
0015A6D9  cmp      rcx, 1
0015A6DD  je       0x15a6f5  ; -> 0015A6F5
0015A6DF  mov      rcx, rbx
0015A6E2  call     0x159e60  ; -> 00159E60 fn
0015A6E7  mov      rdi, rax
0015A6EA  mov      rbx, qword ptr [rsp + 0x38]
0015A6EF  add      rsp, 0x20
0015A6F3  pop      rdi
0015A6F4  ret      
0015A6F5  lea      rdx, [r8 - 1]
0015A6F9  mov      rcx, rbx
0015A6FC  call     0x159ef0  ; -> 00159EF0 fn
0015A701  mov      rdi, rax
0015A704  mov      rbx, qword ptr [rsp + 0x38]
0015A709  add      rsp, 0x20
0015A70D  pop      rdi
0015A70E  ret      
0015A70F  lea      rax, [r8 + r9]
0015A713  mov      qword ptr [rsp + 0x30], rsi
0015A718  mov      ecx, 0x40
0015A71D  lea      rsi, [rax + rax + 2]
0015A722  mov      rdx, rsi
0015A725  call     qword ptr [rip + 0x767c1d]  ; -> 008C2348 [u64 0x0000000001CCC700]
0015A72B  mov      rdi, rax
0015A72E  test     rax, rax
0015A731  je       0x15a766  ; -> 0015A766
0015A733  mov      r8, rbx
0015A736  mov      rdx, rsi
0015A739  mov      rcx, rax
0015A73C  call     0x1597e0  ; -> 001597E0 fn
0015A741  test     eax, eax
0015A743  js       0x15a75b  ; -> 0015A75B
0015A745  lea      r8, [rip + 0x1b6c4ac]  ; -> 01CC6BF8
0015A74C  mov      rdx, rsi
0015A74F  mov      rcx, rdi
0015A752  call     0x1599d0  ; -> 001599D0 fn
0015A757  test     eax, eax
0015A759  jns      0x15a766  ; -> 0015A766
0015A75B  mov      rcx, rdi
0015A75E  call     qword ptr [rip + 0x767a94]  ; -> 008C21F8 [u64 0x0000000001CCC3BA]
0015A764  xor      edi, edi
0015A766  mov      rsi, qword ptr [rsp + 0x30]
0015A76B  mov      rax, rdi
0015A76E  mov      rbx, qword ptr [rsp + 0x38]
0015A773  add      rsp, 0x20
0015A777  pop      rdi
0015A778  ret      
```

## 0015AC50 (506 B, extent 0015AC50-0015AE4A)

Page context: "s, '0017D2E0'/'00808C40'/'00861EC0'. Interior anchor '0079B212' (a '0017D2E0' call).  '001595F0' (356 B) is the wide-string '.dll'-name probe the service/driver enumeration layer shares ('0015A780', '0015AC50', '0015AE60'): '00861EEA' finds the last '\' in the wide name, 'repne scasw' measures the tail, and a backwards walk from the end stops at '\' (0x5C) or '.' (0x2E) so '00861F20' can compare the candidate extension against the '01CC"

```
0015AC50  mov      qword ptr [rsp + 8], rbx
0015AC55  mov      qword ptr [rsp + 0x10], rbp
0015AC5A  mov      qword ptr [rsp + 0x18], rsi
0015AC5F  push     rdi
0015AC60  push     r12
0015AC62  push     r13
0015AC64  push     r14
0015AC66  push     r15
0015AC68  sub      rsp, 0x40
0015AC6C  mov      rdi, qword ptr [rip + 0x2d53ec5]  ; -> 02EAEB38
0015AC73  xor      r15d, r15d
0015AC76  mov      r13, r9
0015AC79  mov      rsi, r8
0015AC7C  mov      rbp, rdx
0015AC7F  mov      r14, rcx
0015AC82  mov      qword ptr [rsp + 0x30], r15
0015AC87  mov      r12, r15
0015AC8A  test     rdi, rdi
0015AC8D  jne      0x15acd7  ; -> 0015ACD7
0015AC8F  mov      rdi, r15
0015AC92  lea      r15, [rip + 0x1b6bfcf]  ; -> 01CC6C68
0015AC99  mov      rcx, r15
0015AC9C  call     0x159420  ; -> 00159420 fn
0015ACA1  mov      rbx, rax
0015ACA4  test     r15, r15
0015ACA7  je       0x15acae  ; -> 0015ACAE
0015ACA9  test     rax, rax
0015ACAC  je       0x15acbf  ; -> 0015ACBF
0015ACAE  xor      r8d, r8d
0015ACB1  xor      edx, edx
0015ACB3  mov      rcx, rax
0015ACB6  call     qword ptr [rip + 0x7676ac]  ; -> 008C2368 [u64 0x0000000001CCC748]
0015ACBC  mov      rdi, rax
0015ACBF  mov      rcx, rbx
0015ACC2  call     qword ptr [rip + 0x767530]  ; -> 008C21F8 [u64 0x0000000001CCC3BA]
0015ACC8  mov      qword ptr [rip + 0x2d53e69], rdi  ; -> 02EAEB38
0015ACCF  test     rdi, rdi
0015ACD2  je       0x15ad51  ; -> 0015AD51
0015ACD4  xor      r15d, r15d
0015ACD7  mov      rax, qword ptr [rip + 0x2d53e62]  ; -> 02EAEB40
0015ACDE  test     rax, rax
0015ACE1  jne      0x15ad06  ; -> 0015AD06
0015ACE3  lea      rdx, [rip + 0x1b6bf6e]  ; -> 01CC6C58 [str "RegOpenKeyExW"]
0015ACEA  mov      rcx, rdi
0015ACED  call     qword ptr [rip + 0x76743d]  ; -> 008C2130 [u64 0x0000000001CCC1FC]
0015ACF3  mov      qword ptr [rip + 0x2d53e46], rax  ; -> 02EAEB40
0015ACFA  test     rax, rax
0015ACFD  je       0x15ad51  ; -> 0015AD51
0015ACFF  mov      rdi, qword ptr [rip + 0x2d53e32]  ; -> 02EAEB38
0015AD06  cmp      qword ptr [rip + 0x2d53e4b], r12  ; -> 02EAEB58
0015AD0D  jne      0x15ad32  ; -> 0015AD32
0015AD0F  lea      rdx, [rip + 0x1b6bf22]  ; -> 01CC6C38 [str "RegCloseKey"]
0015AD16  mov      rcx, rdi
0015AD19  call     qword ptr [rip + 0x767411]  ; -> 008C2130 [u64 0x0000000001CCC1FC]
0015AD1F  mov      qword ptr [rip + 0x2d53e32], rax  ; -> 02EAEB58
0015AD26  test     rax, rax
0015AD29  je       0x15ad51  ; -> 0015AD51
0015AD2B  mov      rax, qword ptr [rip + 0x2d53e0e]  ; -> 02EAEB40
0015AD32  lea      rcx, [rsp + 0x30]
0015AD37  mov      r9d, 1
0015AD3D  xor      r8d, r8d
0015AD40  mov      qword ptr [rsp + 0x20], rcx
0015AD45  mov      rcx, rbp
0015AD48  mov      rdx, rsi
0015AD4B  call     rax
0015AD4D  test     eax, eax
0015AD4F  je       0x15ad60  ; -> 0015AD60
0015AD51  xor      eax, eax
0015AD53  jmp      0x15ae32  ; -> 0015AE32
0015AD58  nop      dword ptr [rax + rax]
0015AD60  mov      rdx, qword ptr [r13]
0015AD64  test     rdx, rdx
0015AD67  je       0x15ae24  ; -> 0015AE24
0015AD6D  mov      rcx, qword ptr [rsp + 0x30]
0015AD72  lea      r9, [rsp + 0x38]
0015AD77  lea      r8, [rsp + 0x88]
0015AD7F  mov      qword ptr [rsp + 0x38], r15
0015AD84  mov      dword ptr [rsp + 0x88], r15d
0015AD8C  call     0x159f90  ; -> 00159F90 fn
0015AD91  mov      rsi, qword ptr [rsp + 0x38]
0015AD96  test     eax, eax
0015AD98  jne      0x15ae0e  ; -> 0015AE0E
0015AD9A  mov      eax, dword ptr [rsp + 0x88]
0015ADA1  mov      rbx, rsi
0015ADA4  sub      eax, 1
0015ADA7  je       0x15adf4  ; -> 0015ADF4
0015ADA9  cmp      eax, 6
0015ADAC  je       0x15adbb  ; -> 0015ADBB
0015ADAE  mov      ecx, 0xd
0015ADB3  call     qword ptr [rip + 0x76759f]  ; -> 008C2358 [u64 0x0000000001CCC724]
0015ADB9  jmp      0x15ae0e  ; -> 0015AE0E
0015ADBB  cmp      r15w, word ptr [rsi]
0015ADBF  je       0x15ade9  ; -> 0015ADE9
0015ADC1  mov      rdx, r14
0015ADC4  mov      rcx, rbx
0015ADC7  call     0x1595f0  ; -> 001595F0 fn
0015ADCC  test     eax, eax
0015ADCE  jne      0x15ade9  ; -> 0015ADE9
0015ADD0  or       rcx, 0xffffffffffffffff
0015ADD4  xor      eax, eax
0015ADD6  mov      rdi, rbx
0015ADD9  repne scasw ax, word ptr [rdi]
0015ADDC  not      rcx
0015ADDF  lea      rbx, [rbx + rcx*2]
0015ADE3  cmp      r15w, word ptr [rbx]
0015ADE7  jne      0x15adc1  ; -> 0015ADC1
0015ADE9  cmp      r15w, word ptr [rbx]
0015ADED  je       0x15ae0e  ; -> 0015AE0E
0015ADEF  mov      rcx, rbx
0015ADF2  jmp      0x15ae06  ; -> 0015AE06
0015ADF4  mov      rdx, r14
0015ADF7  mov      rcx, rsi
0015ADFA  call     0x1595f0  ; -> 001595F0 fn
0015ADFF  test     eax, eax
0015AE01  je       0x15ae0e  ; -> 0015AE0E
0015AE03  mov      rcx, rsi
0015AE06  call     0x159e60  ; -> 00159E60 fn
0015AE0B  mov      r12, rax
0015AE0E  mov      rcx, rsi
0015AE11  call     qword ptr [rip + 0x7673e1]  ; -> 008C21F8 [u64 0x0000000001CCC3BA]
0015AE17  add      r13, 8
0015AE1B  test     r12, r12
0015AE1E  je       0x15ad60  ; -> 0015AD60
0015AE24  mov      rcx, qword ptr [rsp + 0x30]
0015AE29  call     qword ptr [rip + 0x2d53d29]  ; -> 02EAEB58
0015AE2F  mov      rax, r12
0015AE32  mov      rbx, qword ptr [rsp + 0x70]
0015AE37  mov      rbp, qword ptr [rsp + 0x78]
0015AE3C  mov      rsi, qword ptr [rsp + 0x80]
0015AE44  add      rsp, 0x40
0015AE48  pop      r15
```

## 0015AE60 (521 B, extent 0015AE60-0015B069)

Page context: "'/'00808C40'/'00861EC0'. Interior anchor '0079B212' (a '0017D2E0' call).  '001595F0' (356 B) is the wide-string '.dll'-name probe the service/driver enumeration layer shares ('0015A780', '0015AC50', '0015AE60'): '00861EEA' finds the last '\' in the wide name, 'repne scasw' measures the tail, and a backwards walk from the end stops at '\' (0x5C) or '.' (0x2E) so '00861F20' can compare the candidate extension against the '01CC6BF8' litera"

```
0015AE60  mov      qword ptr [rsp + 8], rbx
0015AE65  push     rbp
0015AE66  push     rsi
0015AE67  push     rdi
0015AE68  push     r12
0015AE6A  push     r13
0015AE6C  push     r14
0015AE6E  push     r15
0015AE70  sub      rsp, 0x40
0015AE74  mov      rbx, qword ptr [rip + 0x2d53cbd]  ; -> 02EAEB38
0015AE7B  xor      r15d, r15d
0015AE7E  mov      r12, r8
0015AE81  mov      r14, rdx
0015AE84  mov      r13, rcx
0015AE87  mov      qword ptr [rsp + 0x98], r15
0015AE8F  mov      rdi, r15
0015AE92  test     rbx, rbx
0015AE95  jne      0x15aedc  ; -> 0015AEDC
0015AE97  lea      rbp, [rip + 0x1b6bdca]  ; -> 01CC6C68
0015AE9E  mov      rbx, r15
0015AEA1  mov      rcx, rbp
0015AEA4  call     0x159420  ; -> 00159420 fn
0015AEA9  mov      rsi, rax
0015AEAC  test     rbp, rbp
0015AEAF  je       0x15aeb6  ; -> 0015AEB6
0015AEB1  test     rax, rax
0015AEB4  je       0x15aec7  ; -> 0015AEC7
0015AEB6  xor      r8d, r8d
0015AEB9  xor      edx, edx
0015AEBB  mov      rcx, rax
0015AEBE  call     qword ptr [rip + 0x7674a4]  ; -> 008C2368 [u64 0x0000000001CCC748]
0015AEC4  mov      rbx, rax
0015AEC7  mov      rcx, rsi
0015AECA  call     qword ptr [rip + 0x767328]  ; -> 008C21F8 [u64 0x0000000001CCC3BA]
0015AED0  mov      qword ptr [rip + 0x2d53c61], rbx  ; -> 02EAEB38
0015AED7  test     rbx, rbx
0015AEDA  je       0x15af59  ; -> 0015AF59
0015AEDC  cmp      qword ptr [rip + 0x2d53c5d], rdi  ; -> 02EAEB40
0015AEE3  jne      0x15af08  ; -> 0015AF08
0015AEE5  lea      rdx, [rip + 0x1b6bd6c]  ; -> 01CC6C58 [str "RegOpenKeyExW"]
0015AEEC  mov      rcx, rbx
0015AEEF  call     qword ptr [rip + 0x76723b]  ; -> 008C2130 [u64 0x0000000001CCC1FC]
0015AEF5  mov      qword ptr [rip + 0x2d53c44], rax  ; -> 02EAEB40
0015AEFC  test     rax, rax
0015AEFF  je       0x15af59  ; -> 0015AF59
0015AF01  mov      rbx, qword ptr [rip + 0x2d53c30]  ; -> 02EAEB38
0015AF08  cmp      qword ptr [rip + 0x2d53c39], rdi  ; -> 02EAEB48
0015AF0F  jne      0x15af34  ; -> 0015AF34
0015AF11  lea      rdx, [rip + 0x1b6bd30]  ; -> 01CC6C48 [str "RegEnumValueW"]
0015AF18  mov      rcx, rbx
0015AF1B  call     qword ptr [rip + 0x76720f]  ; -> 008C2130 [u64 0x0000000001CCC1FC]
0015AF21  mov      qword ptr [rip + 0x2d53c20], rax  ; -> 02EAEB48
0015AF28  test     rax, rax
0015AF2B  je       0x15af59  ; -> 0015AF59
0015AF2D  mov      rbx, qword ptr [rip + 0x2d53c04]  ; -> 02EAEB38
0015AF34  cmp      qword ptr [rip + 0x2d53c1d], rdi  ; -> 02EAEB58
0015AF3B  jne      0x15af60  ; -> 0015AF60
0015AF3D  lea      rdx, [rip + 0x1b6bcf4]  ; -> 01CC6C38 [str "RegCloseKey"]
0015AF44  mov      rcx, rbx
0015AF47  call     qword ptr [rip + 0x7671e3]  ; -> 008C2130 [u64 0x0000000001CCC1FC]
0015AF4D  mov      qword ptr [rip + 0x2d53c04], rax  ; -> 02EAEB58
0015AF54  test     rax, rax
0015AF57  jne      0x15af60  ; -> 0015AF60
0015AF59  xor      eax, eax
0015AF5B  jmp      0x15b051  ; -> 0015B051
0015AF60  mov      rdx, qword ptr [r12]
0015AF64  test     rdx, rdx
0015AF67  je       0x15b04e  ; -> 0015B04E
0015AF6D  lea      rax, [rsp + 0x98]
0015AF75  mov      r9d, 0x20019
0015AF7B  xor      r8d, r8d
0015AF7E  mov      rcx, r14
0015AF81  mov      qword ptr [rsp + 0x20], rax
0015AF86  call     qword ptr [rip + 0x2d53bb4]  ; -> 02EAEB40
0015AF8C  test     eax, eax
0015AF8E  jne      0x15b041  ; -> 0015B041
0015AF94  lea      ecx, [rax + 0x40]
0015AF97  mov      edx, 0x10000
0015AF9C  call     qword ptr [rip + 0x7673a6]  ; -> 008C2348 [u64 0x0000000001CCC700]
0015AFA2  mov      rbx, rax
0015AFA5  test     rax, rax
0015AFA8  je       0x15b033  ; -> 0015B033
0015AFAE  mov      ebp, r15d
0015AFB1  xor      edx, edx
0015AFB3  mov      r8d, 0x8000
0015AFB9  mov      rcx, rbx
0015AFBC  mov      dword ptr [rsp + 0x90], 0x7fff
0015AFC7  call     0x861ec0  ; -> 00861EC0 fn
0015AFCC  mov      rcx, qword ptr [rsp + 0x98]
0015AFD4  mov      qword ptr [rsp + 0x38], r15
0015AFD9  mov      qword ptr [rsp + 0x30], r15
0015AFDE  lea      r9, [rsp + 0x90]
0015AFE6  mov      r8, rbx
0015AFE9  mov      edx, ebp
0015AFEB  mov      qword ptr [rsp + 0x28], r15
0015AFF0  mov      qword ptr [rsp + 0x20], r15
0015AFF5  call     qword ptr [rip + 0x2d53b4d]  ; -> 02EAEB48
0015AFFB  inc      ebp
0015AFFD  mov      esi, eax
0015AFFF  test     eax, eax
0015B001  jne      0x15b01d  ; -> 0015B01D
0015B003  mov      rdx, r13
0015B006  mov      rcx, rbx
0015B009  call     0x1595f0  ; -> 001595F0 fn
0015B00E  test     eax, eax
0015B010  je       0x15b01d  ; -> 0015B01D
0015B012  mov      rcx, rbx
0015B015  call     0x159e60  ; -> 00159E60 fn
0015B01A  mov      rdi, rax
0015B01D  test     rdi, rdi
0015B020  jne      0x15b02a  ; -> 0015B02A
0015B022  cmp      esi, 0x103
0015B028  jne      0x15afb1  ; -> 0015AFB1
0015B02A  mov      rcx, rbx
0015B02D  call     qword ptr [rip + 0x7671c5]  ; -> 008C21F8 [u64 0x0000000001CCC3BA]
0015B033  mov      rcx, qword ptr [rsp + 0x98]
0015B03B  call     qword ptr [rip + 0x2d53b17]  ; -> 02EAEB58
0015B041  add      r12, 8
0015B045  test     rdi, rdi
0015B048  je       0x15af60  ; -> 0015AF60
0015B04E  mov      rax, rdi
0015B051  mov      rbx, qword ptr [rsp + 0x80]
0015B059  add      rsp, 0x40
0015B05D  pop      r15
0015B05F  pop      r14
0015B061  pop      r13
0015B063  pop      r12
0015B065  pop      rdi
0015B066  pop      rsi
0015B067  pop      rbp
0015B068  ret      
```

## 0015B820 (779 B, extent 0015B820-0015BB2B)

Page context: "s on 'rdx''s alternate name.  Interior anchor '00159605' (function '001595F0').  '0015B440' (265 B) is the wide path join the enumeration layer calls to glue a directory and a leaf name ('0015B5F0', '0015B820'): two 'repne scasw' lengths, an 'ebp = 1' separator flag only when the left part does not already end in '\' and the right part does not begin with one, '(len1 + sep + len2) * 2 + pad' sized allocation through IAT '008C2348', then"

```
0015B820  mov      qword ptr [rsp + 0x10], rbx
0015B825  mov      qword ptr [rsp + 0x18], rsi
0015B82A  mov      qword ptr [rsp + 0x20], rdi
0015B82F  push     r12
0015B831  sub      rsp, 0x60
0015B835  mov      rdi, rcx
0015B838  xor      r12d, r12d
0015B83B  xor      ecx, ecx
0015B83D  mov      rsi, r12
0015B840  mov      rbx, r12
0015B843  call     qword ptr [rip + 0x766b0f]  ; -> 008C2358 [u64 0x0000000001CCC724]
0015B849  test     rdi, rdi
0015B84C  je       0x15bb07  ; -> 0015BB07
0015B852  mov      rcx, rdi
0015B855  call     0x159520  ; -> 00159520 fn
0015B85A  test     eax, eax
0015B85C  jne      0x15bb07  ; -> 0015BB07
0015B862  lea      rcx, [rip + 0x1b6b37f]  ; -> 01CC6BE8
0015B869  mov      qword ptr [rsp + 0x70], rbp
0015B86E  call     0x15b5f0  ; -> 0015B5F0 fn
0015B873  mov      rbp, rax
0015B876  test     rax, rax
0015B879  je       0x15bac6  ; -> 0015BAC6
0015B87F  mov      rcx, rdi
0015B882  call     0x15a650  ; -> 0015A650 fn
0015B887  mov      rsi, rax
0015B88A  test     rax, rax
0015B88D  je       0x15bac6  ; -> 0015BAC6
0015B893  or       rcx, 0xffffffffffffffff
0015B897  xor      eax, eax
0015B899  mov      rdi, rsi
0015B89C  repne scasw ax, word ptr [rdi]
0015B89F  lea      r8d, [r12 + 0x2e]
0015B8A4  not      rcx
0015B8A7  lea      rdi, [rsi + rcx*2 - 2]
0015B8AC  mov      rcx, rdi
0015B8AF  cmp      rsi, rdi
0015B8B2  jae      0x15b8d7  ; -> 0015B8D7
0015B8B4  mov      edx, 0x5c
0015B8B9  nop      dword ptr [rax]
0015B8C0  movzx    eax, word ptr [rcx]
0015B8C3  cmp      dx, ax
0015B8C6  je       0x15b8d7  ; -> 0015B8D7
0015B8C8  cmp      r8w, ax
0015B8CC  je       0x15b8d7  ; -> 0015B8D7
0015B8CE  sub      rcx, 2
0015B8D2  cmp      rsi, rcx
0015B8D5  jb       0x15b8c0  ; -> 0015B8C0
0015B8D7  cmp      r8w, word ptr [rcx]
0015B8DB  lea      rdx, [rip + 0x1b6b316]  ; -> 01CC6BF8
0015B8E2  cmove    rdi, rcx
0015B8E6  mov      rcx, rdi
0015B8E9  call     0x861f20  ; -> 00861F20 fn
0015B8EE  test     eax, eax
0015B8F0  je       0x15b90e  ; -> 0015B90E
0015B8F2  call     qword ptr [rip + 0x7667b0]  ; -> 008C20A8 [u64 0x0000000001CCC096]
0015B8F8  test     eax, eax
0015B8FA  jne      0x15b90e  ; -> 0015B90E
0015B8FC  lea      rdx, [rip + 0x1b6b2e5]  ; -> 01CC6BE8
0015B903  mov      rcx, rsi
0015B906  call     0x15a9b0  ; -> 0015A9B0 fn
0015B90B  mov      rbx, rax
0015B90E  lea      rdx, [rip + 0x1b6b7cb]  ; -> 01CC70E0
0015B915  mov      rcx, rdi
0015B918  call     0x861f20  ; -> 00861F20 fn
0015B91D  test     eax, eax
0015B91F  je       0x15b9eb  ; -> 0015B9EB
0015B925  test     rbx, rbx
0015B928  jne      0x15bac6  ; -> 0015BAC6
0015B92E  call     qword ptr [rip + 0x766774]  ; -> 008C20A8 [u64 0x0000000001CCC096]
0015B934  test     eax, eax
0015B936  jne      0x15b9ad  ; -> 0015B9AD
0015B938  lea      rax, [rip + 0x1b6b771]  ; -> 01CC70B0
0015B93F  lea      r9, [rsp + 0x40]
0015B944  mov      r8, rbp
0015B947  mov      qword ptr [rsp + 0x20], rax
0015B94C  lea      rax, [rip + 0x1b6b735]  ; -> 01CC7088
0015B953  mov      rdx, 0xffffffff80000002
0015B95A  mov      qword ptr [rsp + 0x28], rax
0015B95F  lea      rax, [rip + 0x1b6b6ea]  ; -> 01CC7050
0015B966  mov      rcx, rsi
0015B969  mov      qword ptr [rsp + 0x30], rax
0015B96E  lea      rax, [rip + 0x1b6b6b3]  ; -> 01CC7028
0015B975  mov      qword ptr [rsp + 0x38], r12
0015B97A  mov      qword ptr [rsp + 0x40], rax
0015B97F  lea      rax, [rip + 0x1b6b67a]  ; -> 01CC7000
0015B986  mov      qword ptr [rsp + 0x58], r12
0015B98B  mov      qword ptr [rsp + 0x48], rax
0015B990  lea      rax, [rip + 0x1b6b639]  ; -> 01CC6FD0
0015B997  mov      qword ptr [rsp + 0x50], rax
0015B99C  call     0x15ac50  ; -> 0015AC50 fn
0015B9A1  mov      rbx, rax
0015B9A4  test     rax, rax
0015B9A7  jne      0x15bac6  ; -> 0015BAC6
0015B9AD  call     qword ptr [rip + 0x7666f5]  ; -> 008C20A8 [u64 0x0000000001CCC096]
0015B9B3  test     eax, eax
0015B9B5  jne      0x15b9f4  ; -> 0015B9F4
0015B9B7  lea      rax, [rip + 0x1b6b5d2]  ; -> 01CC6F90
0015B9BE  lea      r8, [rsp + 0x40]
0015B9C3  mov      rdx, 0xffffffff80000002
0015B9CA  mov      qword ptr [rsp + 0x40], rax
0015B9CF  lea      rax, [rip + 0x1b6b57a]  ; -> 01CC6F50
0015B9D6  mov      rcx, rsi
0015B9D9  mov      qword ptr [rsp + 0x48], rax
0015B9DE  mov      qword ptr [rsp + 0x50], r12
0015B9E3  call     0x15ae60  ; -> 0015AE60 fn
0015B9E8  mov      rbx, rax
0015B9EB  test     rbx, rbx
0015B9EE  jne      0x15bac6  ; -> 0015BAC6
0015B9F4  call     qword ptr [rip + 0x7666ae]  ; -> 008C20A8 [u64 0x0000000001CCC096]
0015B9FA  test     eax, eax
0015B9FC  jne      0x15ba43  ; -> 0015BA43
0015B9FE  lea      rax, [rip + 0x1b6b51b]  ; -> 01CC6F20
0015BA05  lea      r9, [rsp + 0x20]
0015BA0A  mov      r8, rbp
0015BA0D  mov      qword ptr [rsp + 0x40], rax
0015BA12  lea      rax, [rip + 0x1b6b4d7]  ; -> 01CC6EF0
0015BA19  mov      rdx, 0xffffffff80000002
0015BA20  mov      rcx, rsi
0015BA23  mov      qword ptr [rsp + 0x48], r12
0015BA28  mov      qword ptr [rsp + 0x28], r12
0015BA2D  mov      qword ptr [rsp + 0x20], rax
0015BA32  call     0x15ac50  ; -> 0015AC50 fn
0015BA37  mov      rbx, rax
0015BA3A  test     rax, rax
0015BA3D  jne      0x15bac6  ; -> 0015BAC6
0015BA43  call     qword ptr [rip + 0x76665f]  ; -> 008C20A8 [u64 0x0000000001CCC096]
0015BA49  test     eax, eax
0015BA4B  jne      0x15bac6  ; -> 0015BAC6
0015BA4D  mov      ecx, 0x37e4
0015BA52  call     0x15a240  ; -> 0015A240 fn
0015BA57  test     eax, eax
0015BA59  je       0x15ba6c  ; -> 0015BA6C
0015BA5B  lea      rcx, [rip + 0x1b6b186]  ; -> 01CC6BE8
0015BA62  call     0x15b110  ; -> 0015B110 fn
0015BA67  mov      rdi, rax
0015BA6A  jmp      0x15ba74  ; -> 0015BA74
0015BA6C  call     0x159580  ; -> 00159580 fn
0015BA71  mov      rdi, rax
0015BA74  test     rdi, rdi
0015BA77  je       0x15bac6  ; -> 0015BAC6
0015BA79  mov      rdx, rsi
0015BA7C  mov      rcx, rdi
0015BA7F  call     0x15b440  ; -> 0015B440 fn
0015BA84  mov      rbx, rax
0015BA87  test     rax, rax
0015BA8A  je       0x15babd  ; -> 0015BABD
0015BA8C  mov      rcx, rax
0015BA8F  call     qword ptr [rip + 0x7667b3]  ; -> 008C2248 [u64 0x0000000001CCC472]
0015BA95  cmp      eax, -1
0015BA98  je       0x15ba9e  ; -> 0015BA9E
0015BA9A  test     al, 0x50
0015BA9C  je       0x15babd  ; -> 0015BABD
0015BA9E  call     qword ptr [rip + 0x766604]  ; -> 008C20A8 [u64 0x0000000001CCC096]
0015BAA4  cmp      eax, 2
0015BAA7  jne      0x15bab1  ; -> 0015BAB1
0015BAA9  xor      ecx, ecx
0015BAAB  call     qword ptr [rip + 0x7668a7]  ; -> 008C2358 [u64 0x0000000001CCC724]
0015BAB1  mov      rcx, rbx
0015BAB4  call     qword ptr [rip + 0x76673e]  ; -> 008C21F8 [u64 0x0000000001CCC3BA]
0015BABA  mov      rbx, r12
0015BABD  mov      rcx, rdi
0015BAC0  call     qword ptr [rip + 0x766732]  ; -> 008C21F8 [u64 0x0000000001CCC3BA]
0015BAC6  mov      rcx, rbp
0015BAC9  call     qword ptr [rip + 0x766729]  ; -> 008C21F8 [u64 0x0000000001CCC3BA]
0015BACF  mov      rcx, rsi
0015BAD2  call     qword ptr [rip + 0x766720]  ; -> 008C21F8 [u64 0x0000000001CCC3BA]
0015BAD8  mov      rbp, qword ptr [rsp + 0x70]
0015BADD  test     rbx, rbx
0015BAE0  je       0x15baef  ; -> 0015BAEF
0015BAE2  xor      ecx, ecx
0015BAE4  call     qword ptr [rip + 0x76686e]  ; -> 008C2358 [u64 0x0000000001CCC724]
0015BAEA  mov      rax, rbx
0015BAED  jmp      0x15bb14  ; -> 0015BB14
0015BAEF  call     qword ptr [rip + 0x7665b3]  ; -> 008C20A8 [u64 0x0000000001CCC096]
0015BAF5  test     eax, eax
0015BAF7  jne      0x15bb02  ; -> 0015BB02
0015BAF9  lea      ecx, [rax + 0x7e]
0015BAFC  call     qword ptr [rip + 0x766856]  ; -> 008C2358 [u64 0x0000000001CCC724]
0015BB02  mov      rax, rbx
0015BB05  jmp      0x15bb14  ; -> 0015BB14
0015BB07  mov      ecx, 0xa0
0015BB0C  call     qword ptr [rip + 0x766846]  ; -> 008C2358 [u64 0x0000000001CCC724]
0015BB12  xor      eax, eax
0015BB14  lea      r11, [rsp + 0x60]
0015BB19  mov      rbx, qword ptr [r11 + 0x18]
0015BB1D  mov      rsi, qword ptr [r11 + 0x20]
0015BB21  mov      rdi, qword ptr [r11 + 0x28]
0015BB25  mov      rsp, r11
0015BB28  pop      r12
0015BB2A  ret      
```

## 0015BB30 (262 B, extent 0015BB30-0015BC36)

Page context: "E0'/'001599D0' copy both halves into the fresh buffer - a manual PathCombineW.  Interior anchor '0015B4D5' (function '0015B440').  '0015A240' (235 B) is the lazy OS-build cache '0015B110'/'0015B820'/'0015BB30' consult: if 'dword[02EAECE0]' is zero it calls '0015A0E0' with 'rcx = 0xFFFFFFFF80000002' (HKEY_LOCAL_MACHINE) against 'SOFTWARE\Microsoft\Windows NT\CurrentVersion' / 'CurrentBuildNumber' ('01CC6CA0'/'01CC6D00'), and only when th"

```
0015BB30  mov      qword ptr [rsp + 8], rbx
0015BB35  mov      qword ptr [rsp + 0x10], rbp
0015BB3A  mov      qword ptr [rsp + 0x18], rsi
0015BB3F  push     rdi
0015BB40  sub      rsp, 0x20
0015BB44  mov      rsi, rcx
0015BB47  xor      ecx, ecx
0015BB49  mov      ebp, edx
0015BB4B  xor      ebx, ebx
0015BB4D  call     qword ptr [rip + 0x766805]  ; -> 008C2358 [u64 0x0000000001CCC724]
0015BB53  test     rsi, rsi
0015BB56  je       0x15bb91  ; -> 0015BB91
0015BB58  or       rcx, 0xffffffffffffffff
0015BB5C  xor      eax, eax
0015BB5E  mov      rdi, rsi
0015BB61  repne scasw ax, word ptr [rdi]
0015BB64  mov      r8d, ebx
0015BB67  not      rcx
0015BB6A  sub      rcx, 1
0015BB6E  je       0x15bb91  ; -> 0015BB91
0015BB70  mov      rdx, rsi
0015BB73  movzx    eax, word ptr [rdx]
0015BB76  cmp      ax, 0x5c
0015BB7A  je       0x15bbfb  ; -> 0015BBFB
0015BB7C  cmp      ax, 0x2f
0015BB80  je       0x15bbfb  ; -> 0015BBFB
0015BB82  inc      r8d
0015BB85  add      rdx, 2
0015BB89  mov      eax, r8d
0015BB8C  cmp      rax, rcx
0015BB8F  jb       0x15bb73  ; -> 0015BB73
0015BB91  mov      ecx, 0x37e4
0015BB96  call     0x15a240  ; -> 0015A240 fn
0015BB9B  cmp      eax, 1
0015BB9E  jne      0x15bc11  ; -> 0015BC11
0015BBA0  or       rcx, 0xffffffffffffffff
0015BBA4  xor      eax, eax
0015BBA6  lea      rdi, [rip + 0x1b6b53f]  ; -> 01CC70EC
0015BBAD  repne scasw ax, word ptr [rdi]
0015BBB0  lea      rdx, [rip + 0x1b6b535]  ; -> 01CC70EC
0015BBB7  not      rcx
0015BBBA  lea      r8, [rcx - 1]
0015BBBE  mov      rcx, rsi
0015BBC1  call     0x861fce  ; -> 00861FCE fn
0015BBC6  test     eax, eax
0015BBC8  jne      0x15bc11  ; -> 0015BC11
0015BBCA  mov      rcx, rsi
0015BBCD  call     0x15b820  ; -> 0015B820 fn
0015BBD2  mov      rbx, rax
0015BBD5  call     qword ptr [rip + 0x7664cd]  ; -> 008C20A8 [u64 0x0000000001CCC096]
0015BBDB  test     rbx, rbx
0015BBDE  je       0x15bc08  ; -> 0015BC08
0015BBE0  mov      edx, ebp
0015BBE2  mov      rcx, rbx
0015BBE5  call     0x15b550  ; -> 0015B550 fn
0015BBEA  mov      rcx, rbx
0015BBED  mov      rdi, rax
0015BBF0  call     qword ptr [rip + 0x766602]  ; -> 008C21F8 [u64 0x0000000001CCC3BA]
0015BBF6  mov      rax, rdi
0015BBF9  jmp      0x15bc21  ; -> 0015BC21
0015BBFB  mov      ecx, 0xa0
0015BC00  call     qword ptr [rip + 0x766752]  ; -> 008C2358 [u64 0x0000000001CCC724]
0015BC06  jmp      0x15bc1e  ; -> 0015BC1E
0015BC08  cmp      eax, 0x7e
0015BC0B  je       0x15bc11  ; -> 0015BC11
0015BC0D  xor      eax, eax
0015BC0F  jmp      0x15bc21  ; -> 0015BC21
0015BC11  mov      edx, ebp
0015BC13  mov      rcx, rsi
0015BC16  call     0x159aa0  ; -> 00159AA0 fn
0015BC1B  mov      rbx, rax
0015BC1E  mov      rax, rbx
0015BC21  mov      rbx, qword ptr [rsp + 0x30]
0015BC26  mov      rbp, qword ptr [rsp + 0x38]
0015BC2B  mov      rsi, qword ptr [rsp + 0x40]
0015BC30  add      rsp, 0x20
0015BC34  pop      rdi
0015BC35  ret      
```

## 001EDF10 (100 B, extent 001EDF10-001EDF74)

Page context: "' in '00809C40', 'TerminateProcess' in '00809620', 'DestroyWindow' in '0079B190', '_wmkdir' in '001F3EA0', '_lock_file' in '0019B800', '_unlock_file' in '0019B8A0', '_aligned_malloc' in '0019C580' / '001EDF10') | **9** |   | as a loaded value, not a call target: the 'std::locale' facet ids, 'std::cout', 'std::_BADOFF' (data imports), and 'SymGetModuleBase64' / 'SymFunctionTableAccess64', loaded as callback pointers | **8** |    - **Limi"

```
001EDF10  mov      qword ptr [rsp + 8], rbx
001EDF15  push     rdi
001EDF16  sub      rsp, 0x20
001EDF1A  cmp      qword ptr [rip + 0x1d94f26], 0  ; -> 01F82E48
001EDF22  mov      rbx, r8
001EDF25  mov      rdi, rdx
001EDF28  jne      0x1edf5d  ; -> 001EDF5D
001EDF2A  mov      ecx, 0x20
001EDF2F  call     qword ptr [rip + 0x6d4c0b]  ; -> 008C2B40 [u64 0x0000000001CCEE88]
001EDF35  test     rax, rax
001EDF38  je       0x1edf56  ; -> 001EDF56
001EDF3A  mov      dword ptr [rax], 0x2000000
001EDF40  mov      dword ptr [rax + 4], 0x200000
001EDF47  mov      qword ptr [rax + 0x10], 0
001EDF4F  mov      dword ptr [rax + 0x18], 0
001EDF56  mov      qword ptr [rip + 0x1d94eeb], rax  ; -> 01F82E48
001EDF5D  mov      rdx, rbx
001EDF60  mov      rcx, rdi
001EDF63  mov      rbx, qword ptr [rsp + 0x30]
001EDF68  add      rsp, 0x20
001EDF6C  pop      rdi
001EDF6D  jmp      qword ptr [rip + 0x6d4bec]  ; -> 008C2B60 [u64 0x0000000001CCEEB6]
```
