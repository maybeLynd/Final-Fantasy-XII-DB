# F-interior pack: `17-Presentation-Rendering/Character-Render-Records/how-a-presentation-entry-picks-its-track.md`

Generated 2026-10-02 08:46 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/how-a-presentation-entry-picks-its-track.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 7903502f7	FABLE: pass-22 debt - crossing sections on 94 pages (FABLE's group; 12 overlay-carrier pages routed ). OPUS read these before packing.

## 0051B970 (96 B, extent 0051B970-0051B9D0)

Page context: "+0x330') and clears bit 10 of its first dword. *The snapshot of section 3 raises bit 2 of the same '+0x2E8'; what reads the three bits and the factor was not read.*  ## 7b. Who updates the entries - '0051B970'  '0051B970' (96 B, read whole) updates the presentation entries of one container in **three passes**. Each pass is one walk of the container's active entries through the same iterator. The first walk uses one callback; the second "

```
0051B970  push     rbx
0051B972  sub      rsp, 0x20
0051B976  mov      r8, rcx
0051B979  lea      rdx, [rip + 0x260]  ; -> 0051BBE0
0051B980  mov      rbx, rcx
0051B983  call     0x51f580  ; -> 0051F580 fn
0051B988  mov      r8, rbx
0051B98B  mov      dword ptr [rip + 0x278ca5f], 1  ; -> 02CA83F4
0051B995  lea      rdx, [rip + 0x254]  ; -> 0051BBF0
0051B99C  mov      rcx, rbx
0051B99F  call     0x51f580  ; -> 0051F580 fn
0051B9A4  mov      r8, rbx
0051B9A7  mov      dword ptr [rip + 0x278ca43], 2  ; -> 02CA83F4
0051B9B1  lea      rdx, [rip + 0x238]  ; -> 0051BBF0
0051B9B8  mov      rcx, rbx
0051B9BB  call     0x51f580  ; -> 0051F580 fn
0051B9C0  mov      dword ptr [rip + 0x278ca2a], 0  ; -> 02CA83F4
0051B9CA  add      rsp, 0x20
0051B9CE  pop      rbx
0051B9CF  ret      
```
