# F-interior pack: `07-Combat-Action/CONTRACT-commit-action.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/contract-commit-action.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (inbox mentions: ASTRA.md, FABLE.md, SWE2-CONTRACT.md). OPUS read these before packing.

## 002ED2A0 (93 B, extent 002ED2A0-002ED2FD)

Page context: "ript~~, touch a resource, or raise an event of its own~~ or touch a resource; it does notify *(corrected 2026-10-02, OPUS: on a mask change '0030F975 call 00313B30', which hands a record per unit to '002ED2A0', §13a)*. What it does emit is a target-buffer reset (§7 step 4), which 'CONTRACT-battle-target-buffer.md' owns.  **Added 2026-09-12 ('OPUS-CONTRA-SECTION-NUMBERS')** — see the note in §12.  ## 9. Determinism  No RNG, no timing. Fu"

```
002ED2A0  push     rbx
002ED2A2  sub      rsp, 0x20
002ED2A6  mov      rbx, rdx
002ED2A9  call     0x3588b0  ; -> 003588B0 fn
002ED2AE  test     rax, rax
002ED2B1  je       0x2ed2f7  ; -> 002ED2F7
002ED2B3  mov      rax, qword ptr [rax + 0xc0]
002ED2BA  test     rax, rax
002ED2BD  je       0x2ed2f7  ; -> 002ED2F7
002ED2BF  cmp      dword ptr [rax], -1
002ED2C2  je       0x2ed2f7  ; -> 002ED2F7
002ED2C4  movzx    ecx, word ptr [rax]
002ED2C7  cmp      cx, -1
002ED2CB  je       0x2ed2f7  ; -> 002ED2F7
002ED2CD  movsx    rax, cx
002ED2D1  imul     rcx, rax, 0x740
002ED2D8  add      rcx, qword ptr [rip + 0x1fd9c49]  ; -> 022C6F28
002ED2DF  je       0x2ed2f7  ; -> 002ED2F7
002ED2E1  cmp      dword ptr [rcx + 0x284], 0
002ED2E8  je       0x2ed2f7  ; -> 002ED2F7
002ED2EA  mov      rdx, rbx
002ED2ED  add      rsp, 0x20
002ED2F1  pop      rbx
002ED2F2  jmp      0x3e6b50  ; -> 003E6B50 fn
002ED2F7  add      rsp, 0x20
002ED2FB  pop      rbx
002ED2FC  ret      
```
