# F-interior pack: `10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md`

Generated 2026-10-02 08:46 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/two-layer-effect-model.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 7903502f7	FABLE: pass-22 debt - crossing sections on 94 pages (FABLE's group; 12 overlay-carrier pages routed ; inbox mentions: repos-2d.md, repos-78.md). OPUS read these before packing.

## 0046A790 (108 B, extent 0046A790-0046A7FC)

Page context: "USED"* — an unused augment id in the shipped data, tested here       as byte 6 bit 4 of the layers but granted by nothing the tables ship. - [x] ~~What the second function-pointer pair ('0046A720' / '0046A790') does.~~ **Read 2026-09-12       (FABLE):** each maps the status id 'dx' — '0x37', '0x38', '0x39' — to a battle-message id and       posts it through '0046AB10(unit, id, &ctx)': '0046A720' posts '0x3F' / '0x41' / '0x43', '0046A790"

```
0046A790  mov      r11, rsp
0046A793  sub      rsp, 0x58
0046A797  xor      eax, eax
0046A799  mov      qword ptr [r11 - 0x38], rcx
0046A79D  mov      qword ptr [r11 - 0x28], rax
0046A7A1  mov      qword ptr [r11 - 0x20], rax
0046A7A5  mov      qword ptr [r11 - 0x18], rax
0046A7A9  mov      qword ptr [r11 - 0x10], rax
0046A7AD  mov      qword ptr [r11 - 0x30], rcx
0046A7B1  cmp      dx, 0x37
0046A7B5  jne      0x46a7c8  ; -> 0046A7C8
0046A7B7  lea      edx, [rax + 0x3e]
0046A7BA  lea      r8, [r11 - 0x38]
0046A7BE  call     0x46ab10  ; -> 0046AB10 fn
0046A7C3  add      rsp, 0x58
0046A7C7  ret      
0046A7C8  cmp      dx, 0x38
0046A7CC  jne      0x46a7e2  ; -> 0046A7E2
0046A7CE  mov      edx, 0x40
0046A7D3  lea      r8, [rsp + 0x20]
0046A7D8  call     0x46ab10  ; -> 0046AB10 fn
0046A7DD  add      rsp, 0x58
0046A7E1  ret      
0046A7E2  cmp      dx, 0x39
0046A7E6  jne      0x46a7f7  ; -> 0046A7F7
0046A7E8  mov      edx, 0x42
0046A7ED  lea      r8, [rsp + 0x20]
0046A7F2  call     0x46ab10  ; -> 0046AB10 fn
0046A7F7  add      rsp, 0x58
0046A7FB  ret      
```
