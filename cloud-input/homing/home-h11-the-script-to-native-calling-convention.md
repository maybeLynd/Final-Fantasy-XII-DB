# Homing pack: `01-Script-VM-Native-Bridge/Spawn-Verbs/the-script-to-native-calling-convention.md`

Generated 2026-10-03 12:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h11-the-script-to-native-calling-convention.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0025D460 (20 B, extent 0025D460-0025D474)

Entered from (direct sites whose caller this page cites): `003DBDC0` + 0x3D (call; `003DBDC0` is cited on this page)
Other direct sites: none

Host context: " '+0x0C' | | '002651A0' (26 B) | a **third** writer: stores tag '2', then **returns** 'slot.+0x0C' | | '0026B4C0' 'VMResult_WriteFloat32' | tag '3' | | '0026B4E0' 'VMResult_WriteInt32' | tag '2' | | '003DBDC0' 'ActorResource_StartEntryScriptExecution' | sets the pc and '+0x14 = 1' |  Across all six, '+0x15' takes **'0', '1', '2', '3'** and nothing else. ~~**'1' is written exactly once~~ *(corrected 2026-10-02, OPUS: '1' is also written "

```
0025D460  xor      eax, eax
0025D462  mov      qword ptr [rcx], rax
0025D465  mov      qword ptr [rcx + 8], rax
0025D469  mov      dword ptr [rcx + 0x10], eax
0025D46C  mov      word ptr [rcx + 0x14], ax
0025D470  mov      byte ptr [rcx + 0x16], al
0025D473  ret      
```
