# Homing pack: `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md`

Generated 2026-10-03 08:08 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-how-the-ard-loader-binds-area-battle-data.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 003E09B0 (358 B, extent 003E09B0-003E0B16)

Entered from (direct sites whose caller this page cites): `002EA870` + 0x9 (jmp; `002EA870` is cited on this page)
Other direct sites: none

Host context: "02E4000'/'002E3E20' with 'edx=1' ('0025B00B'/'0025B017'), the clearer pair '0035AD40'/'0035AC60'/'0035AB50' ('0025B01C'–'0025B028'), zeroes 'byte[02099DA0]'/'byte[02099DA6]' ('0025B02F'/'0025B036'), '002EA870'/'002EA690', then members '002ECBE0'/'002EBDE0' ('0025B049'/'0025B050'), and restores '02099D70' ('0025B055'). The '0025B070' arm compares 'word[rcx+0x1DA]' vs 'word[rcx+0x1D2]' and rebinds through '00358940' on mismatch ('0025B0A0"

```
003E09B0  sub      rsp, 0x38
003E09B4  mov      rdx, qword ptr [rip + 0x1ee656d]  ; -> 022C6F28
003E09BB  mov      dword ptr [rip + 0x27793a3], ecx  ; -> 02B59D64
003E09C1  test     rdx, rdx
003E09C4  je       0x3e0b11  ; -> 003E0B11
003E09CA  mov      qword ptr [rsp + 0x48], rbp
003E09CF  test     ecx, ecx
003E09D1  mov      eax, 2
003E09D6  mov      ebp, 1
003E09DB  cmovne   ebp, eax
003E09DE  mov      eax, dword ptr [rdx + 0x48800]
003E09E4  cmp      eax, -1
003E09E7  je       0x3e0b0c  ; -> 003E0B0C
003E09ED  mov      qword ptr [rsp + 0x40], rbx
003E09F2  mov      qword ptr [rsp + 0x50], rsi
003E09F7  mov      qword ptr [rsp + 0x28], r14
003E09FC  mov      qword ptr [rsp + 0x20], r15
003E0A01  mov      r15d, 4
003E0A07  mov      qword ptr [rsp + 0x30], rdi
003E0A0C  lea      r14d, [r15 + 0x1a]
003E0A10  cdqe     
003E0A12  imul     rsi, rax, 0x740
003E0A19  lea      rcx, [rsi + rdx]
003E0A1D  call     0x3e6da0  ; -> 003E6DA0 fn
003E0A22  mov      rbx, rax
003E0A25  test     rax, rax
003E0A28  je       0x3e0ade  ; -> 003E0ADE
003E0A2E  mov      ecx, dword ptr [rax]
003E0A30  call     0x20e600  ; -> 0020E600 fn
003E0A35  test     rax, rax
003E0A38  je       0x3e0a61  ; -> 003E0A61
003E0A3A  cmp      dword ptr [rip + 0x2779323], 0  ; -> 02B59D64
003E0A41  mov      edi, ebp
003E0A43  mov      ecx, dword ptr [rbx]
003E0A45  cmovne   edi, r15d
003E0A49  call     0x20e600  ; -> 0020E600 fn
003E0A4E  mov      rcx, rax
003E0A51  mov      edx, edi
003E0A53  call     0x40b5d0  ; -> 0040B5D0 fn
003E0A58  test     eax, eax
003E0A5A  je       0x3e0a61  ; -> 003E0A61
003E0A5C  mov      word ptr [rbx + 0x60], r14w
003E0A61  cmp      dword ptr [rip + 0x27792fc], 0  ; -> 02B59D64
003E0A68  jne      0x3e0ade  ; -> 003E0ADE
003E0A6A  mov      ecx, dword ptr [rbx + 4]
003E0A6D  call     0x20e600  ; -> 0020E600 fn
003E0A72  test     rax, rax
003E0A75  je       0x3e0aa4  ; -> 003E0AA4
003E0A77  mov      ecx, dword ptr [rbx + 4]
003E0A7A  call     0x20e600  ; -> 0020E600 fn
003E0A7F  mov      rcx, rax
003E0A82  call     0x512ad0  ; -> 00512AD0 fn
003E0A87  mov      ecx, dword ptr [rbx + 4]
003E0A8A  call     0x20e600  ; -> 0020E600 fn
003E0A8F  test     rax, rax
003E0A92  je       0x3e0aa4  ; -> 003E0AA4
003E0A94  mov      ecx, dword ptr [rbx + 4]
003E0A97  call     0x20e600  ; -> 0020E600 fn
003E0A9C  mov      rcx, rax
003E0A9F  call     0x512c00  ; -> 00512C00 fn
003E0AA4  mov      ecx, dword ptr [rbx + 0x38]
003E0AA7  call     0x20e600  ; -> 0020E600 fn
003E0AAC  test     rax, rax
003E0AAF  je       0x3e0ade  ; -> 003E0ADE
003E0AB1  mov      ecx, dword ptr [rbx + 0x38]
003E0AB4  call     0x20e600  ; -> 0020E600 fn
003E0AB9  mov      rcx, rax
003E0ABC  call     0x519a30  ; -> 00519A30 fn
003E0AC1  mov      ecx, dword ptr [rbx + 0x38]
003E0AC4  call     0x20e600  ; -> 0020E600 fn
003E0AC9  test     rax, rax
003E0ACC  je       0x3e0ade  ; -> 003E0ADE
003E0ACE  mov      ecx, dword ptr [rbx + 0x38]
003E0AD1  call     0x20e600  ; -> 0020E600 fn
003E0AD6  mov      rcx, rax
003E0AD9  call     0x51a320  ; -> 0051A320 fn
003E0ADE  mov      rdx, qword ptr [rip + 0x1ee6443]  ; -> 022C6F28
003E0AE5  movsx    eax, word ptr [rsi + rdx + 4]
003E0AEA  cmp      eax, -1
003E0AED  jne      0x3e0a10  ; -> 003E0A10
003E0AF3  mov      r15, qword ptr [rsp + 0x20]
003E0AF8  mov      r14, qword ptr [rsp + 0x28]
003E0AFD  mov      rdi, qword ptr [rsp + 0x30]
003E0B02  mov      rsi, qword ptr [rsp + 0x50]
003E0B07  mov      rbx, qword ptr [rsp + 0x40]
003E0B0C  mov      rbp, qword ptr [rsp + 0x48]
003E0B11  add      rsp, 0x38
003E0B15  ret      
```
