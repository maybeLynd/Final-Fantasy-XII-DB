# Homing pack: `04-Actor-Entity/Actor-Manager-Record/the-actor-manager-record-field-map.md`

Generated 2026-10-03 15:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h14-the-actor-manager-record-field-map.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00264420 (58 B, extent 00264420-0026445A)

Entered from (direct sites whose caller this page cites): `00345CD0` + 0x89 (call; `00345CD0` is cited on this page)
Other direct sites: `00345430` + 0x3C (call)

Host context: "pt_VM_Native_Bridge — MECHANICAL (SWE2-EC7-170, 207 edges).** The '0046BD60' enumeration's helpers '00263FF0', '00358940' and '002EA6A0' are consumed across the bridge layer ('0033F7F0', '0025E4C0', '00345CD0', '00267420', '0050D5E0', +202 more) — the '0026xxxx'/'0035xxxx' accessor family's fan-in, no bridge relationship to the record map. Edge list from 'edges.tsv' 2026-09-22.  *Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per"

```
00264420  sub      rsp, 0x28
00264424  mov      rax, qword ptr [rcx + 0xc0]
0026442B  test     rax, rax
0026442E  je       0x264447  ; -> 00264447
00264430  movzx    edx, byte ptr [rax + 0x154]
00264437  test     dl, 2
0026443A  je       0x264447  ; -> 00264447
0026443C  movzx    eax, dl
0026443F  and      eax, 1
00264442  add      rsp, 0x28
00264446  ret      
00264447  call     0x30bfb0  ; -> 0030BFB0 fn
0026444C  xor      ecx, ecx
0026444E  test     eax, eax
00264450  setne    cl
00264453  mov      eax, ecx
00264455  add      rsp, 0x28
00264459  ret      
```
