# F-interior pack: `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md`

Generated 2026-10-02 19:59 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/member-registration-and-the-recovered-field-schema.json`.

Functions: 9. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (inbox mentions: SWE2-FRONTIER.md, repos-78.md, repos-94.md, xiionline-8d.md). OPUS read these before packing.

## 005A7B50 (157 B, extent 005A7B50-005A7BED)

Page context: "iom ('lea' of the head, load, compare with the head) finds the destructor '00633390' as the only function that walks '+0xB0', and it only unlinks; the same census finds the name lookups '005A7A40' / '005A7B50' / '00682E30' on '+0x90' and '005A0470' / '005A7AB0' on '+0xA0', and 22 walkers of '+0x80'. Every other touch is a self-link (the base constructors, the ten per-class constructors in '006316C0'-'00632780', the reset '0063D550'). So"

```
005A7B50  mov      qword ptr [rsp + 8], rbx
005A7B55  mov      qword ptr [rsp + 0x10], rdi
005A7B5A  mov      rbx, rdx
005A7B5D  mov      r10, rcx
005A7B60  test     rdx, rdx
005A7B63  je       0x5a7bd2  ; -> 005A7BD2
005A7B65  test     rcx, rcx
005A7B68  je       0x5a7bd2  ; -> 005A7BD2
005A7B6A  xor      edi, edi
005A7B6C  nop      dword ptr [rax]
005A7B70  lea      r11, [r10 + 0x90]
005A7B77  mov      r9, qword ptr [r11]
005A7B7A  cmp      r9, r11
005A7B7D  cmove    r9, rdi
005A7B81  test     r9, r9
005A7B84  je       0x5a7bc9  ; -> 005A7BC9
005A7B86  mov      rax, qword ptr [r9 + 0x18]
005A7B8A  test     rax, rax
005A7B8D  je       0x5a7bb7  ; -> 005A7BB7
005A7B8F  mov      r8, rbx
005A7B92  sub      r8, rax
005A7B95  nop      word ptr [rax + rax]
005A7BA0  movzx    edx, byte ptr [rax]
005A7BA3  movzx    ecx, byte ptr [rax + r8]
005A7BA8  sub      edx, ecx
005A7BAA  jne      0x5a7bb3  ; -> 005A7BB3
005A7BAC  inc      rax
005A7BAF  test     ecx, ecx
005A7BB1  jne      0x5a7ba0  ; -> 005A7BA0
005A7BB3  test     edx, edx
005A7BB5  je       0x5a7bdf  ; -> 005A7BDF
005A7BB7  mov      rax, qword ptr [r9]
005A7BBA  cmp      rax, r11
005A7BBD  mov      r9, rax
005A7BC0  cmove    r9, rdi
005A7BC4  test     r9, r9
005A7BC7  jne      0x5a7b86  ; -> 005A7B86
005A7BC9  mov      r10, qword ptr [r10 + 0x78]
005A7BCD  test     r10, r10
005A7BD0  jne      0x5a7b70  ; -> 005A7B70
005A7BD2  xor      eax, eax
005A7BD4  mov      rbx, qword ptr [rsp + 8]
005A7BD9  mov      rdi, qword ptr [rsp + 0x10]
005A7BDE  ret      
005A7BDF  mov      rbx, qword ptr [rsp + 8]
005A7BE4  mov      rax, r9
005A7BE7  mov      rdi, qword ptr [rsp + 0x10]
005A7BEC  ret      
```

## 006045B0 (22 B, extent 006045B0-006045C6)

Page context: "ember IS, per instantiation.** The header is read from the member classes' own accessors, which are shared across every instantiation: all 59 'PClassDataMemberPhyreArray<T>' vtables use '006065E0' / '006045B0', all 10 'PClassDataMemberPhyreSharray<T>' vtables use '006065E0' / '0063B9B0'.  - '+0x0' u32 element count; bit 31 is stripped by every reader ('btr 0x1f') and, when set, keeps the buffer from release:   ~~the resizes '005C8BF0' /"

```
006045B0  mov      rax, qword ptr [rcx + 0x18]
006045B4  mov      ecx, dword ptr [rcx + 0x48]
006045B7  sub      ecx, dword ptr [rax + 0xf4]
006045BD  movsxd   rax, ecx
006045C0  mov      rax, qword ptr [rax + rdx + 8]
006045C5  ret      
```

## 006065E0 (24 B, extent 006065E0-006065F8)

Page context: "at an array member IS, per instantiation.** The header is read from the member classes' own accessors, which are shared across every instantiation: all 59 'PClassDataMemberPhyreArray<T>' vtables use '006065E0' / '006045B0', all 10 'PClassDataMemberPhyreSharray<T>' vtables use '006065E0' / '0063B9B0'.  - '+0x0' u32 element count; bit 31 is stripped by every reader ('btr 0x1f') and, when set, keeps the buffer from release:   ~~the resizes"

```
006065E0  mov      rax, qword ptr [rcx + 0x18]
006065E4  mov      ecx, dword ptr [rcx + 0x48]
006065E7  sub      ecx, dword ptr [rax + 0xf4]
006065ED  movsxd   rax, ecx
006065F0  mov      eax, dword ptr [rax + rdx]
006065F3  btr      eax, 0x1f
006065F7  ret      
```

## 0062A870 (124 B, extent 0062A870-0062A8EC)

Page context: "065E0' / '0063B9B0'.  - '+0x0' u32 element count; bit 31 is stripped by every reader ('btr 0x1f') and, when set, keeps the buffer from release:   ~~the resizes '005C8BF0' / '006C7A40' and the adopts '0062A870' / '006A5950' call~~ the resizes and adopts (vtable   slots 5 and 8, which are per element type - corrected 2026-09-27, OPUS; see the '+0x4' note at the end of this   section) call '00584730' on the old storage only when   bit 31 i"

```
0062A870  mov      qword ptr [rsp + 8], rbx
0062A875  mov      qword ptr [rsp + 0x10], rsi
0062A87A  push     rdi
0062A87B  sub      rsp, 0x20
0062A87F  mov      rax, qword ptr [rcx + 0x18]
0062A883  mov      edi, r9d
0062A886  mov      ecx, dword ptr [rcx + 0x48]
0062A889  mov      rsi, r8
0062A88C  sub      ecx, dword ptr [rax + 0xf4]
0062A892  movsxd   rbx, ecx
0062A895  add      rbx, rdx
0062A898  test     r9d, r9d
0062A89B  jns      0x62a8b2  ; -> 0062A8B2
0062A89D  mov      eax, 5
0062A8A2  mov      rbx, qword ptr [rsp + 0x30]
0062A8A7  mov      rsi, qword ptr [rsp + 0x38]
0062A8AC  add      rsp, 0x20
0062A8B0  pop      rdi
0062A8B1  ret      
0062A8B2  mov      rcx, qword ptr [rbx + 8]
0062A8B6  cmp      rcx, rsi
0062A8B9  je       0x62a8d0  ; -> 0062A8D0
0062A8BB  mov      eax, dword ptr [rbx]
0062A8BD  shr      eax, 0x1f
0062A8C0  not      al
0062A8C2  test     al, 1
0062A8C4  je       0x62a8d0  ; -> 0062A8D0
0062A8C6  test     rcx, rcx
0062A8C9  je       0x62a8d0  ; -> 0062A8D0
0062A8CB  call     0x584730  ; -> 00584730 fn
0062A8D0  bts      edi, 0x1f
0062A8D4  mov      qword ptr [rbx + 8], rsi
0062A8D8  mov      rsi, qword ptr [rsp + 0x38]
0062A8DD  xor      eax, eax
0062A8DF  mov      dword ptr [rbx], edi
0062A8E1  mov      rbx, qword ptr [rsp + 0x30]
0062A8E6  add      rsp, 0x20
0062A8EA  pop      rdi
0062A8EB  ret      
```

## 0062FB80 (67 B, extent 0062FB80-0062FBC3)

Page context: "the optional post-step dispatch. Interior anchor '0063BBB0' (the 'jmp [rax + 8]').  ## SWE2-EC7-121 update (2026-09-21) - '00632E80' measured  '00632E80' (293 B) is the member-record ctor '0059AC00'/'0062FB80' call. '00632D80' runs the base init with 'rbx''s '+0x38' (negated) and '+0x3C' fields; the vtable becomes '00D58380' ('[0] = 0063E2C0', RTTI '01D14D30') and the '+0x100..+0x130' records zero with '+0x104' left holding 'rbx+0x38'. "

```
0062FB80  mov      qword ptr [rsp + 0x10], rdx
0062FB85  push     rbx
0062FB86  sub      rsp, 0x30
0062FB8A  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0062FB93  mov      rbx, rdx
0062FB96  mov      qword ptr [rsp + 0x50], rdx
0062FB9B  test     rdx, rdx
0062FB9E  je       0x62fbbb  ; -> 0062FBBB
0062FBA0  call     0x6373d0  ; -> 006373D0 fn
0062FBA5  mov      rdx, rax
0062FBA8  lea      r9, [rip + 0x26c86c1]  ; -> 02CF8270
0062FBAF  xor      r8d, r8d
0062FBB2  mov      rcx, rbx
0062FBB5  call     0x632e80  ; -> 00632E80 fn
0062FBBA  nop      
0062FBBB  mov      al, 1
0062FBBD  add      rsp, 0x30
0062FBC1  pop      rbx
0062FBC2  ret      
```

## 0063B9B0 (48 B, extent 0063B9B0-0063B9E0)

Page context: " accessors, which are shared across every instantiation: all 59 'PClassDataMemberPhyreArray<T>' vtables use '006065E0' / '006045B0', all 10 'PClassDataMemberPhyreSharray<T>' vtables use '006065E0' / '0063B9B0'.  - '+0x0' u32 element count; bit 31 is stripped by every reader ('btr 0x1f') and, when set, keeps the buffer from release:   ~~the resizes '005C8BF0' / '006C7A40' and the adopts '0062A870' / '006A5950' call~~ the resizes and adop"

```
0063B9B0  mov      rax, qword ptr [rcx + 0x18]
0063B9B4  mov      ecx, dword ptr [rcx + 0x48]
0063B9B7  sub      ecx, dword ptr [rax + 0xf4]
0063B9BD  movsxd   rax, ecx
0063B9C0  add      rax, rdx
0063B9C3  mov      ecx, dword ptr [rax]
0063B9C5  btr      ecx, 0x1f
0063B9C9  cmp      ecx, 1
0063B9CC  jbe      0x63b9d3  ; -> 0063B9D3
0063B9CE  mov      rax, qword ptr [rax + 8]
0063B9D2  ret      
0063B9D3  add      rax, 8
0063B9D7  xor      edx, edx
0063B9D9  test     ecx, ecx
0063B9DB  cmove    rax, rdx
0063B9DF  ret      
```

## 00672F30 (243 B, extent 00672F30-00673023)

Page context: "The resize   (slot 5) and set-from-buffer (slot 8) are **per element type**:   - 'PArray' has 45 resizes and 21 setters.   - 'PSharray' has five of each. For the two D3D11 buffer elements the setter '00672F30' copies the whole '0x48'-byte     element inline at count one.   - '005C8BF0' / '006C7A40' and '0062A870' / '006A5950' above are one family's functions, not the template's. - **'+0x4' is cleared, never used on its own.**   - The cl"

```
00672F30  mov      qword ptr [rsp + 0x18], rbx
00672F35  push     rdi
00672F36  sub      rsp, 0x20
00672F3A  mov      rdi, rdx
00672F3D  mov      rbx, rcx
00672F40  test     r8d, r8d
00672F43  jns      0x672f55  ; -> 00672F55
00672F45  mov      eax, 5
00672F4A  mov      rbx, qword ptr [rsp + 0x40]
00672F4F  add      rsp, 0x20
00672F53  pop      rdi
00672F54  ret      
00672F55  mov      eax, dword ptr [rcx]
00672F57  btr      eax, 0x1f
00672F5B  mov      qword ptr [rsp + 0x30], rsi
00672F60  mov      qword ptr [rsp + 0x38], r14
00672F65  cmp      eax, 1
00672F68  jbe      0x672f70  ; -> 00672F70
00672F6A  mov      rcx, qword ptr [rcx + 8]
00672F6E  jmp      0x672f7c  ; -> 00672F7C
00672F70  test     eax, eax
00672F72  je       0x672f7a  ; -> 00672F7A
00672F74  add      rcx, 8
00672F78  jmp      0x672f7c  ; -> 00672F7C
00672F7A  xor      ecx, ecx
00672F7C  mov      esi, r8d
00672F7F  bts      esi, 0x1f
00672F83  cmp      r8d, 1
00672F87  jne      0x672fdf  ; -> 00672FDF
00672F89  lea      rdx, [rbx + 8]
00672F8D  test     rdx, rdx
00672F90  je       0x672fd7  ; -> 00672FD7
00672F92  mov      rax, qword ptr [rdi]
00672F95  mov      qword ptr [rdx], rax
00672F98  mov      rax, qword ptr [rdi + 8]
00672F9C  mov      qword ptr [rdx + 8], rax
00672FA0  mov      rax, qword ptr [rdi + 0x10]
00672FA4  mov      qword ptr [rdx + 0x10], rax
00672FA8  mov      rax, qword ptr [rdi + 0x18]
00672FAC  mov      qword ptr [rdx + 0x18], rax
00672FB0  mov      eax, dword ptr [rdi + 0x20]
00672FB3  mov      dword ptr [rdx + 0x20], eax
00672FB6  lea      rax, [rip + 0x6f5e13]  ; -> 00D68DD0
00672FBD  mov      qword ptr [rdx + 0x28], rax
00672FC1  mov      rax, qword ptr [rdi + 0x30]
00672FC5  mov      qword ptr [rdx + 0x30], rax
00672FC9  mov      eax, dword ptr [rdi + 0x38]
00672FCC  mov      dword ptr [rdx + 0x38], eax
00672FCF  mov      rax, qword ptr [rdi + 0x40]
00672FD3  mov      qword ptr [rdx + 0x40], rax
00672FD7  mov      rdi, rdx
00672FDA  mov      esi, 1
00672FDF  lea      r14, [rbx + 8]
00672FE3  cmp      rcx, rdi
00672FE6  je       0x673002  ; -> 00673002
00672FE8  cmp      rcx, r14
00672FEB  je       0x673002  ; -> 00673002
00672FED  mov      eax, dword ptr [rbx]
00672FEF  shr      eax, 0x1f
00672FF2  not      al
00672FF4  test     al, 1
00672FF6  je       0x673002  ; -> 00673002
00672FF8  test     rcx, rcx
00672FFB  je       0x673002  ; -> 00673002
00672FFD  call     0x584730  ; -> 00584730 fn
00673002  cmp      rdi, r14
00673005  je       0x67300a  ; -> 0067300A
00673007  mov      qword ptr [r14], rdi
0067300A  mov      r14, qword ptr [rsp + 0x38]
0067300F  xor      eax, eax
00673011  mov      dword ptr [rbx], esi
00673013  mov      rsi, qword ptr [rsp + 0x30]
00673018  mov      rbx, qword ptr [rsp + 0x40]
0067301D  add      rsp, 0x20
00673021  pop      rdi
00673022  ret      
```

## 006B66F0 (15 B, extent 006B66F0-006B66FF)

Page context: "e list in 'rcx'. Its 70 calls each     attach one annotation built by '006B66C0' or '006315B0' (a 'PAnnotationWithValue<unsigned>', vtable '00D32D50').     The key is the static '02CF8570', built by '006B66F0' with the name '"WriteMask"'. The stored value is     '0x7FFFFFFF'. The census script 'members/annot_census.py' prints 69 on members named 'm_count',     plus one more '0x7FFFFFFF' built in '00635DC0'.   - **Why the earlier searche"

```
006B66F0  mov      qword ptr [rcx], rdx
006B66F3  mov      rax, rcx
006B66F6  mov      qword ptr [rcx + 8], 0
006B66FE  ret      
```

## 006C7A40 (176 B, extent 006C7A40-006C7AF0)

Page context: "array<T>' vtables use '006065E0' / '0063B9B0'.  - '+0x0' u32 element count; bit 31 is stripped by every reader ('btr 0x1f') and, when set, keeps the buffer from release:   ~~the resizes '005C8BF0' / '006C7A40' and the adopts '0062A870' / '006A5950' call~~ the resizes and adopts (vtable   slots 5 and 8, which are per element type - corrected 2026-09-27, OPUS; see the '+0x4' note at the end of this   section) call '00584730' on the old st"

```
006C7A40  mov      qword ptr [rsp + 8], rbx
006C7A45  mov      qword ptr [rsp + 0x10], rbp
006C7A4A  mov      qword ptr [rsp + 0x18], rsi
006C7A4F  mov      qword ptr [rsp + 0x20], rdi
006C7A54  push     r14
006C7A56  sub      rsp, 0x20
006C7A5A  mov      r9d, dword ptr [rcx]
006C7A5D  mov      ebp, edx
006C7A5F  btr      r9d, 0x1f
006C7A64  mov      rsi, rcx
006C7A67  cmp      edx, dword ptr [rcx]
006C7A69  je       0x6c7ad3  ; -> 006C7AD3
006C7A6B  lea      rdi, [rcx + 8]
006C7A6F  cmp      r9d, 1
006C7A73  jbe      0x6c7a7a  ; -> 006C7A7A
006C7A75  mov      rbx, qword ptr [rdi]
006C7A78  jmp      0x6c7a86  ; -> 006C7A86
006C7A7A  xor      eax, eax
006C7A7C  mov      rbx, rdi
006C7A7F  test     r9d, r9d
006C7A82  cmove    rbx, rax
006C7A86  cmp      ebp, r9d
006C7A89  mov      r8, rbx
006C7A8C  cmovb    r9d, ebp
006C7A90  call     0x6c7450  ; -> 006C7450 fn
006C7A95  mov      r14, rax
006C7A98  test     rax, rax
006C7A9B  jne      0x6c7aa7  ; -> 006C7AA7
006C7A9D  test     ebp, ebp
006C7A9F  je       0x6c7aa7  ; -> 006C7AA7
006C7AA1  lea      eax, [r14 + 0xd]
006C7AA5  jmp      0x6c7ad5  ; -> 006C7AD5
006C7AA7  cmp      rbx, r14
006C7AAA  je       0x6c7ac9  ; -> 006C7AC9
006C7AAC  cmp      rbx, rdi
006C7AAF  je       0x6c7ac9  ; -> 006C7AC9
006C7AB1  mov      eax, dword ptr [rsi]
006C7AB3  shr      eax, 0x1f
006C7AB6  not      al
006C7AB8  test     al, 1
006C7ABA  je       0x6c7ac9  ; -> 006C7AC9
006C7ABC  test     rbx, rbx
006C7ABF  je       0x6c7ac9  ; -> 006C7AC9
006C7AC1  mov      rcx, rbx
006C7AC4  call     0x584730  ; -> 00584730 fn
006C7AC9  cmp      r14, rdi
006C7ACC  je       0x6c7ad1  ; -> 006C7AD1
006C7ACE  mov      qword ptr [rdi], r14
006C7AD1  mov      dword ptr [rsi], ebp
006C7AD3  xor      eax, eax
006C7AD5  mov      rbx, qword ptr [rsp + 0x30]
006C7ADA  mov      rbp, qword ptr [rsp + 0x38]
006C7ADF  mov      rsi, qword ptr [rsp + 0x40]
006C7AE4  mov      rdi, qword ptr [rsp + 0x48]
006C7AE9  add      rsp, 0x20
006C7AED  pop      r14
006C7AEF  ret      
```
