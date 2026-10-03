# F homing pack: `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md`

Generated 2026-10-02 22:03 by OPUS (homing_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`, with ONE extra rule: each body is homed on this page because it calls a function this page documents (named below); the sentence MUST name that callee by address. Report `"mode": "homing"`.

Bodies: 2. No bearing page cites them and no documented function calls them directly.

## 00340450 (48 B, extent 00340450-00340480)

Documented callee on this page: `002E3E20`

```
00340450  push     rbx
00340452  sub      rsp, 0x20
00340456  mov      dword ptr [r8], 0
0034045D  mov      rbx, rdx
00340460  movzx    ecx, byte ptr [rdx + 0x15]
00340464  xor      edx, edx
00340466  call     0x2e3e20  ; -> 002E3E20 fn
0034046B  movzx    ecx, byte ptr [rbx + 0x15]
0034046F  xor      edx, edx
00340471  call     0x2e4000  ; -> 002E4000 fn
00340476  add      rsp, 0x20
0034047A  pop      rbx
0034047B  jmp      0x2ec500  ; -> 002EC500 fn
```

## 00340EC0 (45 B, extent 00340EC0-00340EED)

Documented callee on this page: `002E3E20`

```
00340EC0  push     rbx
00340EC2  sub      rsp, 0x20
00340EC6  mov      dword ptr [r8], 0
00340ECD  mov      rbx, rdx
00340ED0  movzx    ecx, byte ptr [rdx + 0x15]
00340ED4  or       edx, 0xffffffff
00340ED7  call     0x2e3e20  ; -> 002E3E20 fn
00340EDC  movzx    ecx, byte ptr [rbx + 0x15]
00340EE0  or       edx, 0xffffffff
00340EE3  add      rsp, 0x20
00340EE7  pop      rbx
00340EE8  jmp      0x2e4000  ; -> 002E4000 fn
```
