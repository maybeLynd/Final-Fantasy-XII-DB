# Homing pack: `00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-C-ids-76-107.md`

Generated 2026-10-03 07:51 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-arm-catalogue-slice-c-ids-76-107.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001C1C00 (128 B, extent 001C1C00-001C1C80)

Entered from (direct sites whose caller this page cites): `001C1E70` + 0x44 (call; `001C1E70` is cited on this page)
Other direct sites: none

Host context: "in both cases it adds 0x230 to '[rcx]'; returns 'rcx' | Interior anchor '001C1B1B'; Interior anchor '001C1B3D'; Interior anchor '001C1B63'; Interior anchor '001C1BC0'; Interior anchor '001C1BDB' | | '001C1E70' | 417 B | '001C1C80' + 0x89 | copies from 'rdx' to 'rcx' the 16 bytes at '+0' and qwords '+0x10', '+0x18', '+0x20'; makes the call at '001C1E70' + 0x44 with 'rcx+0x28' and 'rdx+0x28', stores at qword 'rcx+0x38' the result of the c"

```
001C1C00  mov      qword ptr [rsp + 8], rbx
001C1C05  mov      qword ptr [rsp + 0x10], rbp
001C1C0A  mov      qword ptr [rsp + 0x18], rsi
001C1C0F  mov      qword ptr [rsp + 0x20], rdi
001C1C14  push     r14
001C1C16  sub      rsp, 0x20
001C1C1A  xor      edi, edi
001C1C1C  mov      r14, rcx
001C1C1F  mov      dword ptr [rcx], edi
001C1C21  mov      ebx, edi
001C1C23  mov      esi, dword ptr [rdx]
001C1C25  mov      rbp, qword ptr [rdx + 8]
001C1C29  and      esi, 0x7fffffff
001C1C2F  jbe      0x1c1c55  ; -> 001C1C55
001C1C31  mov      ecx, esi
001C1C33  lea      edx, [rdi + 8]
001C1C36  shl      rcx, 3
001C1C3A  call     0x17d260  ; -> 0017D260 fn
001C1C3F  mov      rbx, rax
001C1C42  test     rax, rax
001C1C45  je       0x1c1c55  ; -> 001C1C55
001C1C47  mov      r8d, esi
001C1C4A  mov      rdx, rbp
001C1C4D  mov      rcx, rax
001C1C50  call     0x1c19a0  ; -> 001C19A0 fn
001C1C55  mov      rbp, qword ptr [rsp + 0x38]
001C1C5A  test     rbx, rbx
001C1C5D  mov      qword ptr [r14 + 8], rbx
001C1C61  mov      rax, r14
001C1C64  mov      rbx, qword ptr [rsp + 0x30]
001C1C69  cmovne   edi, esi
001C1C6C  mov      rsi, qword ptr [rsp + 0x40]
001C1C71  mov      dword ptr [r14], edi
001C1C74  mov      rdi, qword ptr [rsp + 0x48]
001C1C79  add      rsp, 0x20
001C1C7D  pop      r14
001C1C7F  ret      
```

## 0067ACF0 (100 B, extent 0067ACF0-0067AD54)

Entered from (direct sites whose caller this page cites): `001C1E70` + 0x69 (call; `001C1E70` is cited on this page)
Other direct sites: none

Host context: "in both cases it adds 0x230 to '[rcx]'; returns 'rcx' | Interior anchor '001C1B1B'; Interior anchor '001C1B3D'; Interior anchor '001C1B63'; Interior anchor '001C1BC0'; Interior anchor '001C1BDB' | | '001C1E70' | 417 B | '001C1C80' + 0x89 | copies from 'rdx' to 'rcx' the 16 bytes at '+0' and qwords '+0x10', '+0x18', '+0x20'; makes the call at '001C1E70' + 0x44 with 'rcx+0x28' and 'rdx+0x28', stores at qword 'rcx+0x38' the result of the c"

```
0067ACF0  mov      qword ptr [rsp + 8], rcx
0067ACF5  push     rdi
0067ACF6  sub      rsp, 0x30
0067ACFA  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
0067AD03  mov      qword ptr [rsp + 0x48], rbx
0067AD08  mov      rbx, rcx
0067AD0B  xor      edi, edi
0067AD0D  mov      dword ptr [rcx], edi
0067AD0F  mov      qword ptr [rcx + 8], rdi
0067AD13  mov      eax, dword ptr [rdx + 0x10]
0067AD16  mov      dword ptr [rcx + 0x10], eax
0067AD19  test     eax, eax
0067AD1B  je       0x67ad46  ; -> 0067AD46
0067AD1D  cmp      dword ptr [rdx + 0x10], edi
0067AD20  cmovne   rdi, qword ptr [rdx + 8]
0067AD25  mov      edx, dword ptr [rdx]
0067AD27  btr      edx, 0x1f
0067AD2B  call     0x67b100  ; -> 0067B100 fn
0067AD30  mov      rcx, qword ptr [rbx + 8]
0067AD34  test     rcx, rcx
0067AD37  je       0x67ad46  ; -> 0067AD46
0067AD39  mov      r8d, dword ptr [rbx + 0x10]
0067AD3D  mov      rdx, rdi
0067AD40  call     0x861eba  ; -> 00861EBA fn
0067AD45  nop      
0067AD46  mov      rax, rbx
0067AD49  mov      rbx, qword ptr [rsp + 0x48]
0067AD4E  add      rsp, 0x30
0067AD52  pop      rdi
0067AD53  ret      
```
