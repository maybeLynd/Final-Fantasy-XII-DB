# F-interior pack: `06-Movement-And-Navigation/how-a-unit-finds-its-way-across-the-navigation-mesh.md`

Generated 2026-10-02 20:18 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/how-a-unit-finds-its-way-across-the-navigation-mesh.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

## 0026E300 (73 B, extent 0026E300-0026E349)

Page context: "'. Otherwise the portal is tested for **this mover class**:  - **an ungated portal** (byte '+4' = '0xFF') is open when bit 'moverClass' of its class mask '+6' is set; - **a gated portal** first asks '0026E300' (73 B, through a five-byte thunk) about its map id '+5'. That body looks the   class up in a six-entry table at '00915760' - '{23, 25, 26, 27, -1, 24}' - to get an attribute bit, then reads the   script's **map-id override table**"

```
0026E300  movsx    rax, dx
0026E304  lea      rdx, [rip - 0x14e30b]  ; -> 00120000 (image base)
0026E30B  movsxd   r8, ecx
0026E30E  mov      ecx, dword ptr [rdx + rax*4 + 0x7f5760]  ; image base + 0x7f5760 = 00915760
0026E315  test     ecx, ecx
0026E317  js       0x26e345  ; -> 0026E345
0026E319  mov      rax, r8
0026E31C  lea      r8, [rdx + 0x1f7a3e0]  ; image base + 0x1f7a3e0 = 0209A3E0
0026E323  lea      r8, [r8 + rax*8]
0026E327  mov      eax, 1
0026E32C  mov      edx, eax
0026E32E  shl      edx, cl
0026E330  test     dword ptr [r8], edx
0026E333  je       0x26e342  ; -> 0026E342
0026E335  test     dword ptr [r8 + 4], edx
0026E339  mov      ecx, 2
0026E33E  cmovne   eax, ecx
0026E341  ret      
0026E342  xor      eax, eax
0026E344  ret      
0026E345  or       eax, 0xffffffff
0026E348  ret      
```
