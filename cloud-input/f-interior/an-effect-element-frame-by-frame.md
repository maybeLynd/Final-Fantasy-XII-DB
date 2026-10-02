# F-interior pack: `17-Presentation-Rendering/Effect-File-Formats/an-effect-element-frame-by-frame.md`

Generated 2026-10-02 08:46 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/an-effect-element-frame-by-frame.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 4407f8484	FABLE: pass 22 - 19 of FABLE's 24 UNACCOUNTED NEIGHBOUR pairs read and accounted; 5 on OPUS's CONTRA; 4e32dd8df	FABLE: GI-1..GI-11 and GI-13 answered (GI-12 already at 6facc53bc) - UI screens, dialogs, save/load,; inbox mentions: FABLE.md, SWE2-EC7.md). OPUS read these before packing.

## 002F3890 (122 B, extent 002F3890-002F390A)

Page context: " '+0x20' was found in the bodies the reviewer swept;    that is a bounded negative, not an image-wide one.)* With that byte zero the base itself    shifts the position history and copies the colour ('002F3890'), then runs the child-spawn slots with trigger 2    ('002F2C4D'..'002F2C76') - **with no cull test**; the base never calls '005002E0'. Type '0x09' goes to the    dispatcher's default arm '0043EAB0', which this page does not read. "

```
002F3890  push     rbx
002F3892  sub      rsp, 0x40
002F3896  mov      rax, qword ptr [rip + 0x1c50f93]  ; -> 01F44830 [u64 0x00002B992DDFA232]
002F389D  xor      rax, rsp
002F38A0  mov      qword ptr [rsp + 0x30], rax
002F38A5  mov      eax, dword ptr [rcx + 0x1f0]
002F38AB  mov      rbx, rcx
002F38AE  mov      dword ptr [rcx + 0x1f4], eax
002F38B4  mov      rcx, qword ptr [rcx + 0x10]
002F38B8  test     rcx, rcx
002F38BB  je       0x2f38e2  ; -> 002F38E2
002F38BD  movaps   xmm0, xmmword ptr [rbx + 0x60]
002F38C1  movdqa   xmmword ptr [rsp + 0x20], xmm0
002F38C7  call     0x39af70  ; -> 0039AF70 fn
002F38CC  lea      rdx, [rsp + 0x20]
002F38D1  lea      rcx, [rsp + 0x20]
002F38D6  call     0x398f90  ; -> 00398F90 fn
002F38DB  movaps   xmm1, xmmword ptr [rsp + 0x20]
002F38E0  jmp      0x2f38e6  ; -> 002F38E6
002F38E2  movaps   xmm1, xmmword ptr [rbx + 0x60]
002F38E6  movaps   xmm0, xmmword ptr [rbx + 0x70]
002F38EA  movdqa   xmmword ptr [rbx + 0x80], xmm0
002F38F2  movdqa   xmmword ptr [rbx + 0x70], xmm1
002F38F7  mov      rcx, qword ptr [rsp + 0x30]
002F38FC  xor      rcx, rsp
002F38FF  call     0x808c40  ; -> 00808C40 fn
002F3904  add      rsp, 0x40
002F3908  pop      rbx
002F3909  ret      
```
