# Homing pack: `00-Engine-Core-Runtime/Developer-Tuning-Console/what-the-console-tunes.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-what-the-console-tunes.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001C36F0 (104 B, extent 001C36F0-001C3758)

Entered from (direct sites whose caller this page cites): `002001F0` + 0xA7 (call; `002001F0` is cited on this page)
Other direct sites: none

Host context: " inside its function and decodes to the recorded mnemonic.*  | function | size | what the body does | interior anchors | |---|---|---|---| | '001FF6B0' | 130 B | when dword '[rcx]' is not 3 it calls '002001F0' with the incoming registers, stores 3 to '[rcx]', calls '00210EC0(0x38)' and, when that returns non-null, calls '001EDF00(rsp+0x50, 'EASTL map')' and then '001FE510(block, result)' and stores that call's return to qword '[rcx+8]' "

```
001C36F0  push     rdi
001C36F2  sub      rsp, 0x30
001C36F6  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001C36FF  mov      qword ptr [rsp + 0x40], rbx
001C3704  mov      qword ptr [rsp + 0x48], rsi
001C3709  mov      rsi, rcx
001C370C  mov      rdi, qword ptr [rcx + 8]
001C3710  mov      rbx, qword ptr [rcx]
001C3713  cmp      rbx, rdi
001C3716  jae      0x1c372a  ; -> 001C372A
001C3718  mov      rcx, rbx
001C371B  call     0x1fea00  ; -> 001FEA00 fn
001C3720  nop      
001C3721  add      rbx, 0x10
001C3725  cmp      rbx, rdi
001C3728  jb       0x1c3718  ; -> 001C3718
001C372A  mov      rdx, qword ptr [rsi]
001C372D  test     rdx, rdx
001C3730  je       0x1c3748  ; -> 001C3748
001C3732  lea      rcx, [rsi + 0x18]
001C3736  mov      rax, qword ptr [rcx]
001C3739  mov      r8, qword ptr [rsi + 0x10]
001C373D  sub      r8, rdx
001C3740  and      r8, 0xfffffffffffffff0
001C3744  call     qword ptr [rax + 0x18]
001C3747  nop      
001C3748  mov      rbx, qword ptr [rsp + 0x40]
001C374D  mov      rsi, qword ptr [rsp + 0x48]
001C3752  add      rsp, 0x30
001C3756  pop      rdi
001C3757  ret      
```

## 001EF540 (25 B, extent 001EF540-001EF559)

Entered from (direct sites whose caller this page cites): `001AC7C0` + 0x38 (jmp; `001AC7C0` is cited on this page)
Other direct sites: none

Host context: "cell, '01F812C8', is filled by the   static initializer '0015CC00' from '001F0850' and read by the scene-config loaders '001C3D50' and '001C7940', and   three getters return the pointer ('0015CC00', '001AC7C0', '001FB310'). ORACLE's flow, not bounded by hop count,   follows that cell and those getters and **still finds only the constructor writing '+0x13C'**, so the conclusion   stands. Its stated assumption: code given an element point"

```
001EF540  test     dl, dl
001EF542  je       0x1ef54c  ; -> 001EF54C
001EF544  xor      dword ptr [rcx + 0x130], 2
001EF54B  ret      
001EF54C  mov      eax, dword ptr [rcx + 0x134]
001EF552  mov      dword ptr [rcx + 0x130], eax
001EF558  ret      
```
