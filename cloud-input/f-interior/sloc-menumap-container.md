# F-interior pack: `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/sloc-menumap-container.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/sloc-menumap-container.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 01c2429f6	SWE2-CONTRACT: pass-22 debt batch B - 47 Script-VM, Resource, EBP and PKFL pages' cross-subsystem ne; bafa49c9f	SWE2-DATA: bucket member formats declared - 53 .bin + 5 .dat members, every entry assigned, each cla; inbox mentions: repos-c7.md). OPUS read these before packing.

## 00377400 (54 B, extent 00377400-00377436)

Page context: "ited container accessors (17, 31 and 1,864 bytes) are called by Presentation bodies of 133, 346 and 1,587 bytes. - **WorldAreaField — CLIENT (2 edges).** 2 inbound (WorldAreaField bodies '00378120', '00377400' call page-cited '00379870'). Substantive edges include '00379870' is called by '00378120'; '00379870' is called by '00377400'. "

```
00377400  push     rbx
00377402  sub      rsp, 0x20
00377406  movsxd   rbx, ecx
00377409  cmp      ebx, 3
0037740C  ja       0x377430  ; -> 00377430
0037740E  lea      rax, [rip + 0x2765bfb]  ; -> 02ADD010
00377415  mov      byte ptr [rip + 0x2765ccd], bl  ; -> 02ADD0E8
0037741B  mov      rcx, qword ptr [rax + rbx*8]
0037741F  call     0x3c63a0  ; -> 003C63A0 fn
00377424  mov      ecx, ebx
00377426  add      rsp, 0x20
0037742A  pop      rbx
0037742B  jmp      0x379870  ; -> 00379870 fn
00377430  add      rsp, 0x20
00377434  pop      rbx
00377435  ret      
```
