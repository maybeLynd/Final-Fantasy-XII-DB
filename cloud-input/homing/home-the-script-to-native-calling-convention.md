# Homing pack: `01-Script-VM-Native-Bridge/Spawn-Verbs/the-script-to-native-calling-convention.md`

Generated 2026-10-03 06:31 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-script-to-native-calling-convention.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 003BB320 (82 B, extent 003BB320-003BB372)

Entered from (direct sites whose caller this page cites): `00393EA0` + 0xBA (call; `00393EA0` is cited on this page); `00393EA0` + 0x103 (call; `00393EA0` is cited on this page)
Other direct sites: none

Host context: "sive-subtree pair — both roots bound (SWE2-FRONTIER, followup queue)  | root | member (target) | role | interior | | --- | --- | --- | --- | | '00511F20' | '00394600' | 'byte[01EFAC10] == 2' gate -> '00393EA0' op 'ecx = 0x108' | ['00394600'](../../_index/ADDRESS-INDEX.md) | | '00512130' | '00394640' | 'qword[02AEE4D0] == 0' gate -> '00394130' op 'ecx = 0xF0' | ['00394640'](../../_index/ADDRESS-INDEX.md) |  Shared callees outside the cen" / "sive-subtree pair — both roots bound (SWE2-FRONTIER, followup queue)  | root | member (target) | role | interior | | --- | --- | --- | --- | | '00511F20' | '00394600' | 'byte[01EFAC10] == 2' gate -> '00393EA0' op 'ecx = 0x108' | ['00394600'](../../_index/ADDRESS-INDEX.md) | | '00512130' | '00394640' | 'qword[02AEE4D0] == 0' gate -> '00394130' op 'ecx = 0xF0' | ['00394640'](../../_index/ADDRESS-INDEX.md) |  Shared callees outside the cen"

```
003BB320  lea      rdx, [rip + 0x2785235]  ; -> 02B4055C
003BB327  sub      rdx, rcx
003BB32A  nop      word ptr [rax + rax]
003BB330  movzx    eax, byte ptr [rcx]
003BB333  mov      byte ptr [rdx + rcx], al
003BB336  lea      rcx, [rcx + 1]
003BB33A  test     al, al
003BB33C  jne      0x3bb330  ; -> 003BB330
003BB33E  xor      eax, eax
003BB340  mov      dword ptr [rip + 0x2785ad2], 9  ; -> 02B40E1C
003BB34A  mov      dword ptr [rip + 0x2785c94], eax  ; -> 02B40FE4
003BB350  mov      dword ptr [rip + 0x27851fe], eax  ; -> 02B40554
003BB356  mov      dword ptr [rip + 0x2785b64], eax  ; -> 02B40EC0
003BB35C  mov      dword ptr [rip + 0x2785aaa], 1  ; -> 02B40E10
003BB366  mov      qword ptr [rip + 0x2785aa3], 1  ; -> 02B40E14
003BB371  ret      
```
