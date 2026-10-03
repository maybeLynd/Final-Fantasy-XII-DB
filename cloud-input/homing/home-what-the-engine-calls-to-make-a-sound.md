# Homing pack: `18-Audio/Audio-Boundary/what-the-engine-calls-to-make-a-sound.md`

Generated 2026-10-03 06:31 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-what-the-engine-calls-to-make-a-sound.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 003DEFC0 (112 B, extent 003DEFC0-003DF030)

Entered from (direct sites whose caller this page cites): `003DEC90` + 0x160 (call; `003DEC90` is cited on this page)
Other direct sites: none

Host context: "case it pins the count at 1 ('002DEB50'..'002DEB84'). No instruction sets an id or raises a count, and no 'lea' derives a pointer into the table, so the four release callers ('00363750', '003D7F30', '003DEC90', '003DEE10') always walk sixteen empty entries. *The mask* '0215EFD8' is written only by '002DF370(mask, set, immediate)': with 'immediate' it calls the driver's '001DBA90(mask, set)' and ORs or AND-NOTs the mirror ('002DF383'..'0"

```
003DEFC0  mov      qword ptr [rsp + 8], rbx
003DEFC5  mov      qword ptr [rsp + 0x10], rsi
003DEFCA  push     rdi
003DEFCB  sub      rsp, 0x20
003DEFCF  mov      rbx, rcx
003DEFD2  movsxd   rsi, edx
003DEFD5  mov      rcx, qword ptr [rcx + 8]
003DEFD9  mov      edi, r8d
003DEFDC  test     rcx, rcx
003DEFDF  je       0x3defee  ; -> 003DEFEE
003DEFE1  call     0x3697f0  ; -> 003697F0 fn
003DEFE6  mov      qword ptr [rbx + 8], 0
003DEFEE  mov      rcx, qword ptr [rbx + 0x18]
003DEFF2  test     rcx, rcx
003DEFF5  je       0x3df004  ; -> 003DF004
003DEFF7  call     0x3697f0  ; -> 003697F0 fn
003DEFFC  mov      qword ptr [rbx + 0x18], 0
003DF004  lea      rcx, [rip + 0x277ac15]  ; -> 02B59C20
003DF00B  mov      byte ptr [rbx + 0x10], 0
003DF00F  mov      rbx, qword ptr [rsp + 0x30]
003DF014  lea      rdx, [rcx + rsi*4]
003DF018  mov      rsi, qword ptr [rsp + 0x38]
003DF01D  mov      ecx, edi
003DF01F  mov      eax, 1
003DF024  shl      eax, cl
003DF026  not      eax
003DF028  and      dword ptr [rdx], eax
003DF02A  add      rsp, 0x20
003DF02E  pop      rdi
003DF02F  ret      
```
