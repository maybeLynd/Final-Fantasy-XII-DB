# Homing pack: `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md`

Generated 2026-10-03 15:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h14-member-registration-and-the-recovered-field-schema.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

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
