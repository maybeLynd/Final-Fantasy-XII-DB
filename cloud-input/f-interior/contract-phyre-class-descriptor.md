# F-interior pack: `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/CONTRACT-phyre-class-descriptor.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/contract-phyre-class-descriptor.json`.

Functions: 3. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 6075e3017	SWE2-FRONTIER for FABLE: pass-22 unattributed appends - the other 11 PUBLISHABLE pages (batch 2, 21/). OPUS read these before packing.

## 00164180 (56 B, extent 00164180-001641B8)

Page context: " root is confirmed statically, which is the strongest form this could take.** A live reading and a static derivation are different evidence classes, and here they agree without either being assumed. '00164180' is the root's static constructor and it is eight instructions:  ''' 00164184  lea   rcx, [02CF8270]          ; the descriptor 0016418B  call  006318A0                 ; the PClass constructor 00164190  lea   rax, [00D582D0]       "

```
00164180  sub      rsp, 0x28
00164184  lea      rcx, [rip + 0x2b940e5]  ; -> 02CF8270
0016418B  call     0x6318a0  ; -> 006318A0 fn
00164190  lea      rax, [rip + 0xbf4139]  ; -> 00D582D0
00164197  mov      dword ptr [rip + 0x2b94107], 0  ; -> 02CF82A8
001641A1  lea      rcx, [rip + 0x74afe8]  ; -> 008AF190
001641A8  mov      qword ptr [rip + 0x2b940c1], rax  ; -> 02CF8270
001641AF  add      rsp, 0x28
001641B3  jmp      0x808b90  ; -> 00808B90 fn
```

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

## 00633240 (93 B, extent 00633240-0063329D)

Page context: "**the annotation list** | RTTI puts the 'PAnnotatable' base at '+0x60' here and at '+0x38' in 'PClassDataMember' ('00D580B0'). '006B6700' — the §3 hand-off — is the drain the data-member destructors '00633240'/'00633900' run on their own '+0x38' |    | '+0x80' | the data members, linked through their node at member '+8' | '0062EFD0' |    | '+0x90' | **instance methods** | records that point at a 'PMethodCallerConcrete<Class, Return, Arg"

```
00633240  push     rdi
00633242  sub      rsp, 0x30
00633246  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0063324F  mov      qword ptr [rsp + 0x40], rbx
00633254  mov      rbx, rcx
00633257  lea      rax, [rip + 0x724e52]  ; -> 00D580B0
0063325E  mov      qword ptr [rcx], rax
00633261  lea      rdi, [rcx + 8]
00633265  cmp      qword ptr [rdi], rdi
00633268  je       0x633278  ; -> 00633278
0063326A  mov      rcx, qword ptr [rcx + 0x18]
0063326E  mov      rax, qword ptr [rcx]
00633271  mov      rdx, rbx
00633274  call     qword ptr [rax + 0x48]
00633277  nop      
00633278  lea      rcx, [rbx + 0x38]
0063327C  call     0x6b6700  ; -> 006B6700 fn
00633281  nop      
00633282  test     byte ptr [rdi + 0x20], 1
00633286  je       0x633292  ; -> 00633292
00633288  mov      rcx, qword ptr [rdi + 0x18]
0063328C  call     0x584730  ; -> 00584730 fn
00633291  nop      
00633292  mov      rbx, qword ptr [rsp + 0x40]
00633297  add      rsp, 0x30
0063329B  pop      rdi
0063329C  ret      
```
