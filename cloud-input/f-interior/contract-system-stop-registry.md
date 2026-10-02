# F-interior pack: `00-Engine-Core-Runtime/System-Stop-Registry/CONTRACT-system-stop-registry.md`

Generated 2026-10-02 08:46 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/contract-system-stop-registry.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 7903502f7	FABLE: pass-22 debt - crossing sections on 94 pages (FABLE's group; 12 overlay-carrier pages routed ; inbox mentions: SWE2-CONTRACT.md). OPUS read these before packing.

## 002EBBF0 (64 B, extent 002EBBF0-002EBC30)

Page context: " the focus handle; the party layer's answer is consumed, not derived, here.  **Presentation — SERVICE (1 edge).** The apply '00226280' calls 'CharacterRenderSystem_SetDistanceCullEnableByRequester' ('002EBBF0'). One combined bit toggles the character renderer's distance cull for the registry as a requester; the renderer's use of it is not claimed.  **SaveLoad — CLIENT (1 edge).** '00280140' calls '00252D90', the UI close path, which map"

```
002EBBF0  movzx    eax, byte ptr [rip + 0x1e7415f]  ; -> 0215FD56
002EBBF7  mov      r8d, 1
002EBBFD  shl      r8d, cl
002EBC00  test     edx, edx
002EBC02  je       0x2ebc0c  ; -> 002EBC0C
002EBC04  not      r8b
002EBC07  and      al, r8b
002EBC0A  jmp      0x2ebc0f  ; -> 002EBC0F
002EBC0C  or       al, r8b
002EBC0F  mov      byte ptr [rip + 0x1e74141], al  ; -> 0215FD56
002EBC15  test     al, al
002EBC17  mov      rax, qword ptr [rip + 0x1fdb30a]  ; -> 022C6F28
002EBC1E  jne      0x2ebc28  ; -> 002EBC28
002EBC20  or       dword ptr [rax + 0x48818], 1
002EBC27  ret      
002EBC28  and      dword ptr [rax + 0x48818], 0xfffffffe
002EBC2F  ret      
```
