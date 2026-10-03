# Homing pack: `16-UI/Dynamic-Geometry-Instances/dyngeo-instance-family.md`

Generated 2026-10-03 13:52 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h13-dyngeo-instance-family.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001FDF10 (85 B, extent 001FDF10-001FDF65)

Entered from (direct sites whose caller this page cites): `001B6230` + 0x24 (call; `001B6230` is cited on this page)
Other direct sites: `001B58E0` + 0x109 (call)

Host context: "; no call is made when 'n' is null or no node matches | Interior anchor '001B6134'; Interior anchor '001B6178'; Interior anchor '001B61B0'; Interior anchor '001B6200'; Interior anchor '001B6212' | | '001B6230' | 274 B | returns at once when 'rcx' is null; otherwise calls '001B6230+0x24' with ('rcx', a local 'L'), then 'n' = the call at '001B6230+0x38' with the result of the call at '001B6230+0x2d' and the qword at the first call's retur"

```
001FDF10  mov      qword ptr [rsp + 8], rbx
001FDF15  push     rdi
001FDF16  sub      rsp, 0x30
001FDF1A  xor      eax, eax
001FDF1C  mov      rdi, rdx
001FDF1F  mov      qword ptr [rdx], rax
001FDF22  mov      rbx, rcx
001FDF25  mov      qword ptr [rdx + 8], rax
001FDF29  mov      qword ptr [rdx + 0x10], rax
001FDF2D  lea      rdx, [rcx + 0xf8]
001FDF34  lea      rcx, [rdi + 0x18]
001FDF38  mov      dword ptr [rsp + 0x20], eax
001FDF3C  call     0x1edf00  ; -> 001EDF00 fn
001FDF41  mov      r8, qword ptr [rbx + 0xe8]
001FDF48  mov      rcx, rdi
001FDF4B  mov      rdx, qword ptr [rbx + 0xe0]
001FDF52  call     0x1a4bf0  ; -> 001A4BF0 fn
001FDF57  mov      rbx, qword ptr [rsp + 0x40]
001FDF5C  mov      rax, rdi
001FDF5F  add      rsp, 0x30
001FDF63  pop      rdi
001FDF64  ret      
```
