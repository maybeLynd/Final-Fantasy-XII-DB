# Homing pack: `04-Actor-Entity/Actor-Manager-Record/the-actor-manager-record-field-map.md`

Generated 2026-10-03 13:52 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h13-the-actor-manager-record-field-map.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002A2650 (67 B, extent 002A2650-002A2693)

Entered from (direct sites whose caller this page cites): `003E94D0` + 0x45 (call; `003E94D0` is cited on this page)
Other direct sites: none

Host context: "ry 'edx' of the array at that object's qword '+0x3f8' | Interior anchor '003E9490'; Interior anchor '003E94A1'; Interior anchor '003E94A5'; Interior anchor '003E94BA'; Interior anchor '003E94C1' | | '003E94D0' | 85 B | calls '002E1040' with the incoming registers and does nothing more when the returned record's qword '+0' is null or 'edx' is not below its word '+0x54' (signed compare); otherwise makes the call at '003E94D0' + 0x45 with "

```
002A2650  push     rbx
002A2652  movzx    eax, byte ptr [rcx + 0x3f3]
002A2659  mov      r11d, r9d
002A265C  mov      rbx, r8
002A265F  mov      r10, rcx
002A2662  test     al, al
002A2664  js       0x2a2691  ; -> 002A2691
002A2666  mov      r9d, dword ptr [rsp + 0x30]
002A266B  or       al, 4
002A266D  mov      byte ptr [rcx + 0x3f3], al
002A2673  mov      r8d, r11d
002A2676  movsxd   rax, edx
002A2679  mov      rdx, rbx
002A267C  lea      rcx, [rax + rax*2]
002A2680  shl      rcx, 5
002A2684  add      rcx, qword ptr [r10 + 0x3f8]
002A268B  pop      rbx
002A268C  jmp      0x2a7c70  ; -> 002A7C70 fn
002A2691  pop      rbx
002A2692  ret      
```
