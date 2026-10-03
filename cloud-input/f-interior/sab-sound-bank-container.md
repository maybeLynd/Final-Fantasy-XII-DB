# F-interior pack: `18-Audio/Sound-Bank-And-Voice-Formats/sab-sound-bank-container.md`

Generated 2026-10-02 20:44 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/sab-sound-bank-container.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: cd6bd7f58	SWE2-DATA consolidated publish: progress-report cluster (generation store, R3 semantics, DB_GOAL, me; d0fd168a2	SWE2-DATA: batch-5 review corrections (clamping page's .data vf00 cell restored, SD-190 gate on the ; inbox mentions: repos-1e.md, repos-4b.md). OPUS read these before packing.

## 001FB770 (133 B, extent 001FB770-001FB7F5)

Page context: "rce-kind path table, whose kind 33 array holds the 'shout' bank paths.  ## SWE2-EC7-109 update (2026-09-20) - '001FB470' measured  '001FB470' (332 B) is the EASTL rbtree insert-with-hint '001A2E50', '001FB770' and '00223AD0' call: the hint node 'qword[r8]' is validated against head/sentinel, '0016D6D0' finds the successor, both orderings around 'dword[node + 0x20]' are compared against 'dword[r9]', a 0x30 node comes out of the 'qword[rc"

```
001FB770  push     rbx
001FB772  sub      rsp, 0x40
001FB776  lea      r11, [rcx + 8]
001FB77A  mov      rbx, rdx
001FB77D  mov      rcx, qword ptr [r11 + 0x18]
001FB781  lea      rdx, [r11 + 8]
001FB785  lea      r10d, [r9 + r8*2]
001FB789  mov      rax, rdx
001FB78C  test     rcx, rcx
001FB78F  je       0x1fb7a8  ; -> 001FB7A8
001FB791  cmp      dword ptr [rcx + 0x20], r10d
001FB795  jl       0x1fb7a0  ; -> 001FB7A0
001FB797  mov      rax, rcx
001FB79A  mov      rcx, qword ptr [rcx + 8]
001FB79E  jmp      0x1fb7a3  ; -> 001FB7A3
001FB7A0  mov      rcx, qword ptr [rcx]
001FB7A3  test     rcx, rcx
001FB7A6  jne      0x1fb791  ; -> 001FB791
001FB7A8  cmp      rax, rdx
001FB7AB  je       0x1fb7b3  ; -> 001FB7B3
001FB7AD  cmp      r10d, dword ptr [rax + 0x20]
001FB7B1  jge      0x1fb7eb  ; -> 001FB7EB
001FB7B3  mov      qword ptr [rsp + 0x50], rax
001FB7B8  lea      r9, [rsp + 0x30]
001FB7BD  movzx    eax, byte ptr [rsp + 0x60]
001FB7C2  lea      r8, [rsp + 0x50]
001FB7C7  lea      rdx, [rsp + 0x58]
001FB7CC  mov      byte ptr [rsp + 0x20], al
001FB7D0  mov      rcx, r11
001FB7D3  mov      dword ptr [rsp + 0x30], r10d
001FB7D8  mov      qword ptr [rsp + 0x38], 0
001FB7E1  call     0x1fb470  ; -> 001FB470 fn
001FB7E6  mov      rax, qword ptr [rsp + 0x58]
001FB7EB  mov      qword ptr [rax + 0x28], rbx
001FB7EF  add      rsp, 0x40
001FB7F3  pop      rbx
001FB7F4  ret      
```
