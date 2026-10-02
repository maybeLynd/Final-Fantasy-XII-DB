# F-interior pack: `25-EBP-Script-Container/Sections/section-010.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/section-010.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 01c2429f6	SWE2-CONTRACT: pass-22 debt batch B - 47 Script-VM, Resource, EBP and PKFL pages' cross-subsystem ne; bafa49c9f	SWE2-DATA: bucket member formats declared - 53 .bin + 5 .dat members, every entry assigned, each cla; inbox mentions: ASSIGNMENTS.md, repos-1e.md, repos-3f.md, repos-4b.md, repos-c7.md, repos-c9.md). OPUS read these before packing.

## 00269530 (105 B, extent 00269530-00269599)

Page context: "e masks > to '0x60' loads '[[actor + 0xB8] + 0xF0]' and **sets bit 7 of chunk '+0x62'** ('0026338F'–'0026339D') > as the script starts; and '002693D0' (called from 'ActorSystem_ReleaseManagerReco…', '00269530' > and '0026C5D0'), which for the same kind reads and **clears chunk '+0x28'** ('00269448'–'00269453') > and tests chunk '+0x65' to decide a '002EBE50' / '002E8EE0' teardown ('0026945B'–'00269478'). So the > ~~shake directory is li"

```
00269530  mov      qword ptr [rsp + 8], rbx
00269535  mov      qword ptr [rsp + 0x10], rsi
0026953A  push     rdi
0026953B  sub      rsp, 0x20
0026953F  xor      ebx, ebx
00269541  lea      rsi, [rip + 0x1e30ca8]  ; -> 0209A1F0
00269548  cmp      rbx, 3
0026954C  ja       0x269554  ; -> 00269554
0026954E  mov      rdi, qword ptr [rsi + rbx*8]
00269552  jmp      0x269556  ; -> 00269556
00269554  xor      edi, edi
00269556  cmp      byte ptr [rdi + 0x18], 1
0026955A  jne      0x269580  ; -> 00269580
0026955C  movzx    edx, word ptr [rdi + 0x1a]
00269560  movsx    ecx, byte ptr [rdi + 0x19]
00269564  call     0x3587c0  ; -> 003587C0 fn
00269569  test     rax, rax
0026956C  je       0x269580  ; -> 00269580
0026956E  cmp      rax, rdi
00269571  je       0x269580  ; -> 00269580
00269573  mov      edx, 1
00269578  mov      rcx, rax
0026957B  call     0x2693d0  ; -> 002693D0 fn
00269580  inc      rbx
00269583  cmp      rbx, 4
00269587  jl       0x269548  ; -> 00269548
00269589  mov      rbx, qword ptr [rsp + 0x30]
0026958E  mov      rsi, qword ptr [rsp + 0x38]
00269593  add      rsp, 0x20
00269597  pop      rdi
00269598  ret      
```
