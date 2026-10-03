# Homing pack: `19-Save-Load-Settings/Game-Settings-Config/ff12config-and-debglobal.md`

Generated 2026-10-02 22:54 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-ff12config-and-debglobal.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001D6BB0 (44 B, extent 001D6BB0-001D6BDC)

Entered from (direct sites whose caller this page cites): `0059A9B0` + 0x1F (call; `0059A9B0` is cited on this page)
Other direct sites: none

Host context: "ver '0059EE90' with selector 1. The resolver fills only two sources: route 1, the RAM file cache ('01F83440', budget from 'GlobalMemoryStatusEx' at '0020C610'), which route 2's own hits fill through '0059A9B0', and route 2, the package lookup, whose five slots are mounted only by '0019B070' from one call site with '../FFXII_TZA.vbf'. The only 'CreateFile*' import is 'CreateFileA', used by two minidump writers. So 'FF12CONFIG' is the arc"

```
001D6BB0  mov      qword ptr [rsp + 8], rbx
001D6BB5  push     rdi
001D6BB6  sub      rsp, 0x20
001D6BBA  movzx    ebx, dl
001D6BBD  mov      edi, ecx
001D6BBF  call     0x20c700  ; -> 0020C700 fn
001D6BC4  mov      rcx, rax
001D6BC7  movzx    r8d, bl
001D6BCB  mov      edx, edi
001D6BCD  mov      rbx, qword ptr [rsp + 0x30]
001D6BD2  add      rsp, 0x20
001D6BD6  pop      rdi
001D6BD7  jmp      0x20bfa0  ; -> 0020BFA0 fn
```

## 00314D60 (32 B, extent 00314D60-00314D80)

Entered from (direct sites whose caller this page cites): `0050C8A0` + 0x24 (jmp; `0050C8A0` is cited on this page)
Other direct sites: none

Host context: "red ownership. - **Script_VM_Native_Bridge - CLIENT and SERVICE (11 edges).** '0032FC30', '00314440', '00408EC0' are also called by bodies filed to script VM / native bridge: '0034B650', '00355350', '0050C8A0' (+7 more); '0050DFC0' reaches bodies filed to script VM / native bridge: '0026B4E0' - shared machinery across the layer boundary, no shared ownership. ## The '00408C30' exclusive subtree — all 2 members bound (SWE2-FRONTIER, follo"

```
00314D60  push     rbx
00314D62  sub      rsp, 0x20
00314D66  mov      ebx, ecx
00314D68  call     0x5c5230  ; -> 005C5230 fn
00314D6D  xor      edx, edx
00314D6F  test     eax, eax
00314D71  cmovne   edx, ebx
00314D74  mov      dword ptr [rip + 0x1fad7c6], edx  ; -> 022C2540
00314D7A  add      rsp, 0x20
00314D7E  pop      rbx
00314D7F  ret      
```
