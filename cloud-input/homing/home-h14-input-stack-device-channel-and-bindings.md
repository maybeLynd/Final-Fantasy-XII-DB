# Homing pack: `15-Input/Input-Stack/input-stack-device-channel-and-bindings.md`

Generated 2026-10-03 15:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h14-input-stack-device-channel-and-bindings.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0025D5D0 (8 B, extent 0025D5D0-0025D5D8)

Entered from (direct sites whose caller this page cites): `00343C60` + 0x36 (call; `00343C60` is cited on this page)
Other direct sites: `00342770` + 0xB8 (jmp); `003437A0` + 0x64 (jmp); `00344410` + 0x1F (jmp); `00345B60` + 0x7A (call); `00346C00` + 0x108 (jmp); `00347A50` + 0x52 (jmp)

Host context: "erior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*  | function | size | what the body does | interior anchors | |---|---|---|---| | '00343C60' | 96 B | calls '00343C60'+0x10('r9') and '00343C60'+0x1B(byte 'rdx+0x15'), and calls '00361200'(first result, 1, 1), passing 0 instead of the first result when the second is non-zero; then calls +0x36 and +0x3F(byte 'rdx+0x15') an"

```
0025D5D0  and      byte ptr [rip + 0x1e3b850], 0x7f  ; -> 02098E27
0025D5D7  ret      
```
