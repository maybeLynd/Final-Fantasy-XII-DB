# Homing pack: `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md`

Generated 2026-10-03 12:18 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h10-member-registration-and-the-recovered-field-schema.json`.

Bodies: 3. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 005A5B40 (144 B, extent 005A5B40-005A5BD0)

Entered from (direct sites whose caller this page cites): `005C8BF0` + 0x57 (call; `005C8BF0` is cited on this page)
Other direct sites: `005AA3C0` + 0x49 (call); `005C9DD0` + 0x83 (call)

Host context: "MemberPhyreSharray<T>' vtables use '006065E0' / '0063B9B0'.  - '+0x0' u32 element count; bit 31 is stripped by every reader ('btr 0x1f') and, when set, keeps the buffer from release:   ~~the resizes '005C8BF0' / '006C7A40' and the adopts '0062A870' / '006A5950' call~~ the resizes and adopts (vtable   slots 5 and 8, which are per element type - corrected 2026-09-27, OPUS; see the '+0x4' note at the end of this   section) call '00584730' "

```
005A5B40  xor      r11d, r11d
005A5B43  mov      r10d, r8d
005A5B46  cmp      r8d, 4
005A5B4A  jb       0x5a5bad  ; -> 005A5BAD
005A5B4C  lea      eax, [r8 - 4]
005A5B50  shr      eax, 2
005A5B53  inc      eax
005A5B55  mov      r9d, eax
005A5B58  lea      r11d, [rax*4]
005A5B60  test     rcx, rcx
005A5B63  je       0x5a5b6d  ; -> 005A5B6D
005A5B65  mov      eax, dword ptr [rdx]
005A5B67  add      rdx, 4
005A5B6B  mov      dword ptr [rcx], eax
005A5B6D  lea      r8, [rcx + 4]
005A5B71  test     r8, r8
005A5B74  je       0x5a5b7f  ; -> 005A5B7F
005A5B76  mov      eax, dword ptr [rdx]
005A5B78  add      rdx, 4
005A5B7C  mov      dword ptr [r8], eax
005A5B7F  lea      rax, [rcx + 8]
005A5B83  test     rax, rax
005A5B86  je       0x5a5b91  ; -> 005A5B91
005A5B88  mov      eax, dword ptr [rdx]
005A5B8A  add      rdx, 4
005A5B8E  mov      dword ptr [rcx + 8], eax
005A5B91  lea      r8, [rcx + 0xc]
005A5B95  test     r8, r8
005A5B98  je       0x5a5ba3  ; -> 005A5BA3
005A5B9A  mov      eax, dword ptr [rdx]
005A5B9C  add      rdx, 4
005A5BA0  mov      dword ptr [r8], eax
005A5BA3  add      rcx, 0x10
005A5BA7  sub      r9, 1
005A5BAB  jne      0x5a5b60  ; -> 005A5B60
005A5BAD  cmp      r11d, r10d
005A5BB0  jae      0x5a5bcf  ; -> 005A5BCF
005A5BB2  sub      r10d, r11d
005A5BB5  mov      r8d, r10d
005A5BB8  test     rcx, rcx
005A5BBB  je       0x5a5bc5  ; -> 005A5BC5
005A5BBD  mov      eax, dword ptr [rdx]
005A5BBF  add      rdx, 4
005A5BC3  mov      dword ptr [rcx], eax
005A5BC5  add      rcx, 4
005A5BC9  sub      r8, 1
005A5BCD  jne      0x5a5bb8  ; -> 005A5BB8
005A5BCF  ret      
```

## 0063D930 (134 B, extent 0063D930-0063D9B6)

Entered from (direct sites whose caller this page cites): `00639290` + 0x74 (call; `00639290` is cited on this page)
Other direct sites: none

Host context: " — | walks 'cls+0x80' and the base chain at 'cls+0x78', comparing names | | '0063D550' | descriptor list reset | — | re-initialises **six** intrusive lists at 'cls+0x50/0x60/0x80/0x90/0xA0/0xB0' | | '00639290' | attach wrapper | — | the one descriptor whose slot '+0x40' differs; skips a 'PClassDataMemberDynamicDefault*' sentinel | | '00633390' | 'PClassDescriptor' base destructor | 500 B | the descriptor layout, read in the sibling docu"

```
0063D930  mov      qword ptr [rsp + 8], rbx
0063D935  push     rdi
0063D936  sub      rsp, 0x20
0063D93A  mov      rbx, rdx
0063D93D  mov      rdi, rcx
0063D940  call     0x63ae50  ; -> 0063AE50 fn
0063D945  and      dword ptr [rdi + 0xfc], 0x7fffffff
0063D94F  mov      rdx, rbx
0063D952  mov      rcx, rdi
0063D955  call     0x639a60  ; -> 00639A60 fn
0063D95A  mov      rdx, rbx
0063D95D  mov      rcx, rdi
0063D960  call     0x639c80  ; -> 00639C80 fn
0063D965  test     rbx, rbx
0063D968  jne      0x63d9ab  ; -> 0063D9AB
0063D96A  mov      rcx, qword ptr [rdi + 0xc0]
0063D971  test     rcx, rcx
0063D974  je       0x63d9ab  ; -> 0063D9AB
0063D976  mov      rax, rdi
0063D979  lea      rdx, [rip + 0x2810da0]  ; -> 02E4E720
0063D980  cmp      rax, rdx
0063D983  je       0x63d999  ; -> 0063D999
0063D985  mov      rax, qword ptr [rax + 0x78]
0063D989  test     rax, rax
0063D98C  jne      0x63d980  ; -> 0063D980
0063D98E  mov      rbx, qword ptr [rsp + 0x30]
0063D993  add      rsp, 0x20
0063D997  pop      rdi
0063D998  ret      
0063D999  cmp      dword ptr [rdi + 0x38], 0x18
0063D99D  jb       0x63d9ab  ; -> 0063D9AB
0063D99F  movsxd   rax, dword ptr [rdi + 0xf8]
0063D9A6  mov      qword ptr [rax + rcx + 0x10], rdi
0063D9AB  mov      rbx, qword ptr [rsp + 0x30]
0063D9B0  add      rsp, 0x20
0063D9B4  pop      rdi
0063D9B5  ret      
```

## 006C7450 (163 B, extent 006C7450-006C74F3)

Entered from (direct sites whose caller this page cites): `006C7A40` + 0x50 (call; `006C7A40` is cited on this page)
Other direct sites: none

Host context: "array<T>' vtables use '006065E0' / '0063B9B0'.  - '+0x0' u32 element count; bit 31 is stripped by every reader ('btr 0x1f') and, when set, keeps the buffer from release:   ~~the resizes '005C8BF0' / '006C7A40' and the adopts '0062A870' / '006A5950' call~~ the resizes and adopts (vtable   slots 5 and 8, which are per element type - corrected 2026-09-27, OPUS; see the '+0x4' note at the end of this   section) call '00584730' on the old st"

```
006C7450  mov      qword ptr [rsp + 0x10], rbx
006C7455  mov      qword ptr [rsp + 0x18], rbp
006C745A  push     rsi
006C745B  sub      rsp, 0x20
006C745F  mov      ebp, r9d
006C7462  mov      rbx, r8
006C7465  mov      esi, edx
006C7467  lea      r8, [rcx + 8]
006C746B  test     edx, edx
006C746D  jne      0x6c7481  ; -> 006C7481
006C746F  xor      eax, eax
006C7471  mov      rbx, qword ptr [rsp + 0x38]
006C7476  mov      rbp, qword ptr [rsp + 0x40]
006C747B  add      rsp, 0x20
006C747F  pop      rsi
006C7480  ret      
006C7481  cmp      esi, 1
006C7484  jbe      0x6c749a  ; -> 006C749A
006C7486  mov      rcx, rsi
006C7489  mov      edx, 8
006C748E  shl      rcx, 3
006C7492  call     0x17d260  ; -> 0017D260 fn
006C7497  mov      r8, rax
006C749A  test     r8, r8
006C749D  je       0x6c74e0  ; -> 006C74E0
006C749F  mov      qword ptr [rsp + 0x30], rdi
006C74A4  mov      rcx, r8
006C74A7  test     ebp, ebp
006C74A9  je       0x6c74cc  ; -> 006C74CC
006C74AB  mov      rdi, rbp
006C74AE  nop      
006C74B0  mov      rdx, rcx
006C74B3  add      rcx, 8
006C74B7  test     rdx, rdx
006C74BA  je       0x6c74c6  ; -> 006C74C6
006C74BC  mov      rax, qword ptr [rbx]
006C74BF  add      rbx, 8
006C74C3  mov      qword ptr [rdx], rax
006C74C6  sub      rdi, 1
006C74CA  jne      0x6c74b0  ; -> 006C74B0
006C74CC  sub      esi, ebp
006C74CE  je       0x6c74db  ; -> 006C74DB
006C74D0  lea      rdi, [r8 + rbp*8]
006C74D4  mov      ecx, esi
006C74D6  xor      eax, eax
006C74D8  rep stosq qword ptr [rdi], rax
006C74DB  mov      rdi, qword ptr [rsp + 0x30]
006C74E0  mov      rbx, qword ptr [rsp + 0x38]
006C74E5  mov      rax, r8
006C74E8  mov      rbp, qword ptr [rsp + 0x40]
006C74ED  add      rsp, 0x20
006C74F1  pop      rsi
006C74F2  ret      
```
