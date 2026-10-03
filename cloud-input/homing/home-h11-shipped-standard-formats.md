# Homing pack: `02-Resource-And-Asset-Pipeline/Standard-Formats/shipped-standard-formats.md`

Generated 2026-10-03 12:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h11-shipped-standard-formats.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00597A20 (67 B, extent 00597A20-00597A63)

Entered from (direct sites whose caller this page cites): `00225C40` + 0x47 (call; `00225C40` is cited on this page)
Other direct sites: none

Host context: "th are shared CRT/runtime plumbing: the crossing is that Platform uses them, not a shared responsibility. - **Audio — CLIENT and SERVICE (10 edges).** 5 inbound (Audio bodies '002125A0', '006794D0', '00225C40' call page-cited '00584740', '005CD330', '005CD700'); 5 outbound (page-cited '00679A50', '006794D0', '0067A480' call Audio bodies '007A4930', '00881830', '00882200'). Substantive edges include '0067A480' calls '006794D0'; the remai"

```
00597A20  xor      eax, eax
00597A22  mov      qword ptr [rcx + 0x28], 0xffffffffffffffff
00597A2A  mov      dword ptr [rcx + 0x20], eax
00597A2D  mov      qword ptr [rcx + 0x30], rax
00597A31  mov      dword ptr [rcx + 0x48], eax
00597A34  mov      qword ptr [rcx + 0x40], 0xffffffffffffffff
00597A3C  mov      byte ptr [rcx + 0x38], 1
00597A40  mov      dword ptr [rcx + 8], 0xb
00597A47  mov      qword ptr [rcx + 0x10], rax
00597A4B  mov      dword ptr [rcx + 0x18], eax
00597A4E  lea      rax, [rip + 0x78f23b]  ; -> 00D26C90
00597A55  mov      qword ptr [rcx], rax
00597A58  mov      rax, rcx
00597A5B  mov      dword ptr [rcx + 0x1c], 0xffffffff
00597A62  ret      
```
