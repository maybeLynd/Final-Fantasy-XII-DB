# F-interior pack: `17-Presentation-Rendering/Character-Render-Records/how-a-status-shows-on-a-character.md`

Generated 2026-10-02 08:46 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/how-a-status-shows-on-a-character.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: bf226bbaa	SWE2-AUDIT-SPEC: promotion sweep - three pages DOCUMENTED -> AUDITED; inbox mentions: FABLE.md). OPUS read these before packing.

## 001EF280 (65 B, extent 001EF280-001EF2C1)

Page context: "' reach for their parameter block. 'byte[rcx]' latches 1, '+8'..'+0x40' and '+0xD8'/'+0xEC'/'+0xF4' zero, 'qword[+0x18]' and '+0x30' latch '0xFF', '+0x138' arms 4, and '00808FE4(rcx + 0x148, 0xD8, 8, 001EF280)' builds an 8-element sub-object array with '001EF280' as the element constructor and '001EF4A0' staged at '[rsp + 0x20]'. The defaults that follow are the weather/display block: '+0x808'/'+0x80C'/'+0x810' = 5.0/10.0/30.0, '+0x828'"

```
001EF280  push     rbx
001EF282  sub      rsp, 0x20
001EF286  mov      rbx, rcx
001EF289  add      rcx, 8
001EF28D  call     0x184e60  ; -> 00184E60 fn
001EF292  lea      rax, [rip + 0x713c3f]  ; -> 00902ED8
001EF299  mov      dword ptr [rbx + 0xc8], 0x3f800000
001EF2A3  mov      rcx, rbx
001EF2A6  mov      qword ptr [rbx], rax
001EF2A9  mov      dword ptr [rbx + 0xd0], 0x3f800000
001EF2B3  call     0x1f0a00  ; -> 001F0A00 fn
001EF2B8  mov      rax, rbx
001EF2BB  add      rsp, 0x20
001EF2BF  pop      rbx
001EF2C0  ret      
```
