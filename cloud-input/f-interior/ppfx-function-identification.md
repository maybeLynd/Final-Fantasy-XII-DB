# F-interior pack: `17-Presentation-Rendering/Post-Processing/ppfx-function-identification.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/ppfx-function-identification.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 54e8a524e	SWE2-FRONTIER for FABLE: pass-22 unattributed appends - verifier + 23 of 34 PUBLISHABLE pages (batch; inbox mentions: repos-94.md). OPUS read these before packing.

## 007911E0 (72 B, extent 007911E0-00791228)

Page context: "n set finds, incl. '006F8740'       (section 10). The documented 135 is a floor.~~ **H-7 ANSWERED 2026-09-13 (FABLE):** the floor is replaced by the object — every census entry from '006DA880' up to '007911E0' is Yebis / PPFX (1,766 entries, 1,660 declared; '006F8740' among them), bounded by source-path evidence, edges and controls on [the Yebis / PPFX source map §11](../../23-Third-Party-Libraries/PostEffects-Yebis-PPFX/yebis-ppfx-sour"

```
007911E0  push     rbx
007911E2  sub      rsp, 0x30
007911E6  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
007911EF  mov      rbx, rdx
007911F2  mov      ecx, dword ptr [rdx + 8]
007911F5  mov      eax, ecx
007911F7  shr      eax, 0x1f
007911FA  not      al
007911FC  test     al, 1
007911FE  je       0x791217  ; -> 00791217
00791200  btr      ecx, 0x1f
00791204  cmp      ecx, 1
00791207  jbe      0x791217  ; -> 00791217
00791209  mov      rcx, qword ptr [rdx + 0x10]
0079120D  test     rcx, rcx
00791210  je       0x791217  ; -> 00791217
00791212  call     0x584730  ; -> 00584730 fn
00791217  xor      eax, eax
00791219  mov      qword ptr [rbx + 0x10], rax
0079121D  mov      dword ptr [rbx + 8], eax
00791220  mov      al, 1
00791222  add      rsp, 0x30
00791226  pop      rbx
00791227  ret      
```
