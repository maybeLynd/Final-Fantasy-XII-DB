# Homing pack: `99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-cutscene-name-slots-and-the-depth-of-field-sidecar.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00276190 (133 B, extent 00276190-00276215)

Entered from (direct sites whose caller this page cites): `00271760` + 0x24 (call; `00271760` is cited on this page)
Other direct sites: none

Host context: "it is the HIGH half of a qword whose low half is '0x10000000',** written by         the immediately preceding instruction at the adjacent lower dword:         '003F2F20' writes '+0x08' then '+0x0C'; '00271760' writes '+0x08' then '+0x0C'; '003C2E60'         writes '+0x08' then '+0x0C'; and this page's own emitter '002DC290' writes '+0x18' then         '+0x1C' ('002DC2F7'–'002DC2FE'), sixteen bytes further in because its command carries "

```
00276190  mov      qword ptr [rsp + 8], rbx
00276195  push     rdi
00276196  sub      rsp, 0x20
0027619A  mov      rbx, rdx
0027619D  mov      dword ptr [rcx + 0x80], 0x44fff000
002761A7  mov      rdi, rcx
002761AA  mov      dword ptr [rcx + 0x84], 0x44fff000
002761B4  mov      dword ptr [rcx + 0x88], 0x44fff000
002761BE  lea      rdx, [rip + 0x2877beb]  ; -> 02AEDDB0
002761C5  mov      dword ptr [rcx + 0x8c], 0x44fff000
002761CF  mov      dword ptr [rcx + 0xc0], 0x3f800000
002761D9  mov      dword ptr [rcx + 0xc4], 0x3f800000
002761E3  mov      dword ptr [rcx + 0xc8], 0x3f800000
002761ED  mov      dword ptr [rcx + 0xcc], 0x3f800000
002761F7  add      rcx, 0x40
002761FB  call     0x202c70  ; -> 00202C70 fn
00276200  mov      rdx, rbx
00276203  mov      rcx, rdi
00276206  mov      rbx, qword ptr [rsp + 0x30]
0027620B  add      rsp, 0x20
0027620F  pop      rdi
00276210  jmp      0x202c70  ; -> 00202C70 fn
```

## 002EC960 (15 B, extent 002EC960-002EC96F)

Entered from (direct sites whose caller this page cites): `003417F0` + 0x3A (call; `003417F0` is cited on this page)
Other direct sites: none

Host context: "'0026D6D0').  **Script_VM_Native_Bridge — MECHANICAL, 136 edges.** '00267310' is called by '0033F330', '00340260', '00340FA0', '00341590' and 52 more; '003EB720' is called by '0033FAD0', '00340530', '003417F0', '00347B00' and 15 more; '002EFA70' is called by '003559B0', '00355EB0', '00356270', '00356650' and 2 more; 'WorldActor_UpdateRuntimeAndScriptExecutionState' ('0025DF00') calls 'WorldActorScriptVM_InterpretBytecode' ('0025E4C0'), "

```
002EC960  test     rcx, rcx
002EC963  je       0x2ec96e  ; -> 002EC96E
002EC965  cmp      dword ptr [rcx], -1
002EC968  je       0x2ec96e  ; -> 002EC96E
002EC96A  mov      word ptr [rcx + 0x2a], dx
002EC96E  ret      
```
