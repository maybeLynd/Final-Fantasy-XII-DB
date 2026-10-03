# Homing pack: `99-Unresolved-Residual/Unowned-Code-Census/why-the-unowned-code-has-no-owner.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-why-the-unowned-code-has-no-owner.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 006D5940 (174 B, extent 006D5940-006D59EE)

Entered from (direct sites whose caller this page cites): `008B75A0` + 0x7 (jmp; `008B75A0` is cited on this page); `008B75E0` + 0x7 (jmp; `008B75E0` is cited on this page)
Other direct sites: `008B75B0` + 0x7 (jmp); `008B75C0` + 0x7 (jmp); `008B75D0` + 0x7 (jmp); `008B7610` + 0x7 (jmp); `008B7620` + 0x7 (jmp); `008B7630` + 0x7 (jmp); `008B7640` + 0x7 (jmp); `008B7650` + 0x7 (jmp); `008B7660` + 0x7 (jmp); `008B7670` + 0x7 (jmp); `008B7680` + 0x7 (jmp); `008B7690` + 0x7 (jmp)

Host context: "**, which is why the same two addresses repeat down the table.  A second strided family sits at '01F32150', stride '0x80', pairs of '006D5xxx'/'006D6xxx' functions, with five per-record accessors at '008B75A0'-'008B75E0' each taking the address of one record. Its extent is **not** established here and it is not claimed.  ### What survived, and one run §16 did not list  All six runs §16 tabulates reproduce exactly: '01F41E98' (26, Audio)" / "s why the same two addresses repeat down the table.  A second strided family sits at '01F32150', stride '0x80', pairs of '006D5xxx'/'006D6xxx' functions, with five per-record accessors at '008B75A0'-'008B75E0' each taking the address of one record. Its extent is **not** established here and it is not claimed.  ### What survived, and one run §16 did not list  All six runs §16 tabulates reproduce exactly: '01F41E98' (26, Audio), '01F003A8"

```
006D5940  push     rdi
006D5942  sub      rsp, 0x30
006D5946  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
006D594F  mov      qword ptr [rsp + 0x40], rbx
006D5954  mov      rbx, rcx
006D5957  lea      rcx, [rip + 0x27ca402]  ; -> 02E9FD60
006D595E  mov      rdx, qword ptr [rip + 0x27ca3fb]  ; -> 02E9FD60
006D5965  xor      edi, edi
006D5967  test     rdx, rdx
006D596A  je       0x6d599f  ; -> 006D599F
006D596C  lea      r9, [rbx + 8]
006D5970  lea      rax, [rdx + 8]
006D5974  test     rdx, rdx
006D5977  cmove    rax, rdi
006D597B  cmp      rax, r9
006D597E  je       0x6d598f  ; -> 006D598F
006D5980  lea      rcx, [rdx + 8]
006D5984  mov      rdx, qword ptr [rdx + 8]
006D5988  test     rdx, rdx
006D598B  jne      0x6d5970  ; -> 006D5970
006D598D  jmp      0x6d599f  ; -> 006D599F
006D598F  test     rdx, rdx
006D5992  je       0x6d599f  ; -> 006D599F
006D5994  mov      rax, qword ptr [rdx + 8]
006D5998  mov      qword ptr [rcx], rax
006D599B  mov      qword ptr [rdx + 8], rdi
006D599F  mov      eax, dword ptr [rbx + 0x20]
006D59A2  shr      eax, 0x1f
006D59A5  not      al
006D59A7  test     al, 1
006D59A9  je       0x6d59ba  ; -> 006D59BA
006D59AB  mov      rcx, qword ptr [rbx + 0x28]
006D59AF  test     rcx, rcx
006D59B2  je       0x6d59ba  ; -> 006D59BA
006D59B4  call     0x584730  ; -> 00584730 fn
006D59B9  nop      
006D59BA  mov      qword ptr [rbx + 0x28], rdi
006D59BE  mov      dword ptr [rbx + 0x20], edi
006D59C1  mov      eax, dword ptr [rbx + 0x10]
006D59C4  shr      eax, 0x1f
006D59C7  not      al
006D59C9  test     al, 1
006D59CB  je       0x6d59dc  ; -> 006D59DC
006D59CD  mov      rcx, qword ptr [rbx + 0x18]
006D59D1  test     rcx, rcx
006D59D4  je       0x6d59dc  ; -> 006D59DC
006D59D6  call     0x584730  ; -> 00584730 fn
006D59DB  nop      
006D59DC  mov      qword ptr [rbx + 0x18], rdi
006D59E0  mov      dword ptr [rbx + 0x10], edi
006D59E3  mov      rbx, qword ptr [rsp + 0x40]
006D59E8  add      rsp, 0x30
006D59EC  pop      rdi
006D59ED  ret      
```
