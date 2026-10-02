# F-interior pack: `13-Rewards-Progression-Economy/CONTRACT-gil-storage-and-movement.md`

Generated 2026-10-02 08:46 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/contract-gil-storage-and-movement.json`.

Functions: 2. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 7903502f7	FABLE: pass-22 debt - crossing sections on 94 pages (FABLE's group; 12 overlay-carrier pages routed ). OPUS read these before packing.

## 0030BAF0 (22 B, extent 0030BAF0-0030BB06)

Page context: "alls '0032F240', a 32-byte lookup that returns a dword from an actor-indexed table when that actor's flag byte is set and −1 otherwise; the bundle fetch '003F4C30' calls 'PackedActorHandle_IsClass8' '0030BAF0'. The verb turns an actor's table value into a counter id before it writes an achievement counter, and the bundle fetch builds a one-item bundle when its key is a class-8 packed handle; neither touches the balance at '+0x08'.  **Co"

```
0030BAF0  mov      eax, 0xf000
0030BAF5  mov      edx, 0x8000
0030BAFA  and      cx, ax
0030BAFD  xor      eax, eax
0030BAFF  cmp      cx, dx
0030BB02  sete     al
0030BB05  ret      
```

## 00473C90 (37 B, extent 00473C90-00473CB5)

Page context: "to its thunk. So the thirteenth writer's gil write is reached from   authored script: the quest-result window. The bundle keys are values the handler computes ('00267E10(r9)' and a   popped integer, '00473C90'); what they select is not read here. - ~~Whether any consumer reconciles the meter against the balance (GL-3).~~ **Closed   2026-09-22 (SWE2-CONTRACT): no consumer does.** The meter '00316A50' writes two sinks: the   per-kind "see"

```
00473C90  mov      rdx, qword ptr [rip + 0x2832fc9]  ; -> 02CA6C60
00473C97  cmp      dword ptr [rdx + 4], ecx
00473C9A  jle      0x473cb1  ; -> 00473CB1
00473C9C  movsxd   rax, ecx
00473C9F  mov      eax, dword ptr [rdx + rax*4 + 8]
00473CA3  shr      eax, 0xd
00473CA6  and      eax, 0x1fff
00473CAB  add      eax, 0xa000
00473CB0  ret      
00473CB1  or       eax, 0xffffffff
00473CB4  ret      
```
