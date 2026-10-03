# Homing pack: `03-World-Area-Field/CONTRACT-weather.md`

Generated 2026-10-03 15:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h14-contract-weather.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 003DE700 (16 B, extent 003DE700-003DE710)

Entered from (direct sites whose caller this page cites): `00379080` + 0x66 (call; `00379080` is cited on this page); `00379110` + 0x2F (call; `00379110` is cited on this page)
Other direct sites: `00378230` + 0x152 (call)

Host context: "LIENT, eleven edges.** - The area initialiser calls '00263560', '002EBE40' and '003DAE30'. - The movement bodies '0033A720', '003ED190' and '003ED3F0' read the field id. - '003DE920' is reached from '00379080' / '00379110'. - '00259B30' calls '00380D30'. - The field pass calls 'WorldActor_UpdateRuntimeAndScriptExecutionState'. - '00379290' calls '0026E8D0'.  **CombatAI, CombatAction, Gameplay and Party — CLIENT, 23 edges through the sel" / " edges.** - The area initialiser calls '00263560', '002EBE40' and '003DAE30'. - The movement bodies '0033A720', '003ED190' and '003ED3F0' read the field id. - '003DE920' is reached from '00379080' / '00379110'. - '00259B30' calls '00380D30'. - The field pass calls 'WorldActor_UpdateRuntimeAndScriptExecutionState'. - '00379290' calls '0026E8D0'.  **CombatAI, CombatAction, Gameplay and Party — CLIENT, 23 edges through the selector and the"

```
003DE700  movsx    edx, byte ptr [rip + 0x277ac49]  ; -> 02B59350
003DE707  xor      eax, eax
003DE709  bt       edx, ecx
003DE70C  setb     al
003DE70F  ret      
```
