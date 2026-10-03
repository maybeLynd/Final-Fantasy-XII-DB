# Homing pack: `17-Presentation-Rendering/Movie-Containers/mh-movie-seek-index.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-mh-movie-seek-index.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0037B470 (17 B, extent 0037B470-0037B481)

Entered from (direct sites whose caller this page cites): `0035B840` + 0x11 (call; `0035B840` is cited on this page)
Other direct sites: `00347C40` + 0x12 (jmp)

Host context: "e   '.' ('001B7FB4'–'001B7FF7'), and formats '"%s%s.webm"' ('008F8D70') under '/GameData/D3D11/ArtData/video/'   ('008F8D10') — the '.md' path is used only for its name, and no '.md' file ships. - **'0035B840'** (reached through '00356460') fetches index '2m + 1' at '0035B8AE' and **discards the   result**: the next instructions load 'ecx' from its own argument and call '001848A0', which does not   read 'rax'.  | Field | Read by | Rejec"

```
0037B470  test     ecx, ecx
0037B472  mov      eax, 3
0037B477  cmovs    ecx, eax
0037B47A  mov      byte ptr [rip + 0x27624b3], cl  ; -> 02ADD933
0037B480  ret      
```
