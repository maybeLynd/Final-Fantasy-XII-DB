# Homing pack: `00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md`

Generated 2026-10-03 13:52 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h13-cross-subsystem-accessor-hubs.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00393190 (65 B, extent 00393190-003931D1)

Entered from (direct sites whose caller this page cites): `0057FA30` + 0x12 (call; `0057FA30` is cited on this page)
Other direct sites: `0057FB00` + 0x9C (call)

Host context: "h the incoming 'rdx' as 'rcx' and that value as 'edx' | Interior anchor '0050E3B8'; Interior anchor '0050E3C3'; Interior anchor '0050E3CB'; Interior anchor '0050E3CD'; Interior anchor '0050E3E5' | | '0057FA30' | 197 B | calls '0057FA30'+0x12 with ('rcx', 0); in the qword table at 'rcx+0x10' clears bit 0 of dword '+8' in entry '+0xd8', sets it in entry '+0xb0' and in the 7 entries indexed by the bytes at '00D23EAC' (index times 8), then "

```
00393190  xor      r8d, r8d
00393193  mov      r10d, edx
00393196  test     dword ptr [rcx], 0x3fffc
0039319C  jbe      0x3931d0  ; -> 003931D0
0039319E  and      r10d, 1
003931A2  nop      dword ptr [rax]
003931A6  nop      word ptr [rax + rax]
003931B0  mov      rax, qword ptr [rcx + 0x10]
003931B4  mov      rdx, qword ptr [rax + r8*8]
003931B8  inc      r8d
003931BB  and      dword ptr [rdx + 8], 0xfffffffe
003931BF  or       dword ptr [rdx + 8], r10d
003931C3  mov      eax, dword ptr [rcx]
003931C5  shr      eax, 2
003931C8  movzx    eax, ax
003931CB  cmp      r8d, eax
003931CE  jb       0x3931b0  ; -> 003931B0
003931D0  ret      
```
