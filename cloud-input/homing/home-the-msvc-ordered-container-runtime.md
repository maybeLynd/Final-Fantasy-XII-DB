# Homing pack: `24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/the-msvc-ordered-container-runtime.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-msvc-ordered-container-runtime.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00799B20 (83 B, extent 00799B20-00799B73)

Entered from (direct sites whose caller this page cites): `00169270` + 0x27 (call; `00169270` is cited on this page)
Other direct sites: none

Host context: "30' and '0079BA10' sit past the span's end, inside the **PhyreEngine 'PFramework'** platform layer: the tree they erase is the static 'std::_Tree' at '02EA5550', constructed and atexit-registered by '00169270'/'008B7940', beside 'PClassDescriptorForType< PFramework::*>' statics and the 'PhyreFrameworkClass' window creation (see §7, MT-2).  ## 6. Modding notes  **Do not confuse the two families when hooking.** A detour written against 'm"

```
00799B20  mov      qword ptr [rsp + 8], rcx
00799B25  sub      rsp, 0x38
00799B29  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
00799B32  mov      ecx, 0x28
00799B37  call     0x210ec0  ; -> 00210EC0 fn
00799B3C  mov      qword ptr [rsp + 0x40], rax
00799B41  test     rax, rax
00799B44  jne      0x799b4d  ; -> 00799B4D
00799B46  call     qword ptr [rip + 0x12925c]  ; -> 008C2DA8 [u64 0x0000000001CCED90]
00799B4C  nop      
00799B4D  mov      qword ptr [rax], rax
00799B50  lea      rcx, [rax + 8]
00799B54  test     rcx, rcx
00799B57  je       0x799b5c  ; -> 00799B5C
00799B59  mov      qword ptr [rcx], rax
00799B5C  lea      rcx, [rax + 0x10]
00799B60  test     rcx, rcx
00799B63  je       0x799b68  ; -> 00799B68
00799B65  mov      qword ptr [rcx], rax
00799B68  mov      word ptr [rax + 0x18], 0x101
00799B6E  add      rsp, 0x38
00799B72  ret      
```
