# F-interior pack: `19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/katano-debug-savedata.md`

Generated 2026-10-02 20:44 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/katano-debug-savedata.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: cd6bd7f58	SWE2-DATA consolidated publish: progress-report cluster (generation store, R3 semantics, DB_GOAL, me; d0fd168a2	SWE2-DATA: batch-5 review corrections (clamping page's .data vf00 cell restored, SD-190 gate on the ; inbox mentions: FABLE.md, SWE2-AUDIT-SPEC.md, SWE2-CONTRACT.md). OPUS read these before packing.

## 001EA380 (64 B, extent 001EA380-001EA3C0)

Page context: "init), '002DDE60', '0016D6A0' (assert). The '+0x3244'/'+0x3245' bit-pair and the '00253240' slot loop's target are left as recorded unknowns.  '001EA1E0' (408 B) is the counted table walk '001D0390'/'001EA380' call: 'dword[rcx+0x28] & 0x7FFFFFFF' counts '[rcx+0x30]' elements, '01CEB638' supplies the stride base, '0017D260' resolves each entry, '00861EBA' copies, '00584730' stores, '001EA6C0' finishes - the debug save's element enumerato"

```
001EA380  push     rbx
001EA382  sub      rsp, 0x20
001EA386  mov      eax, dword ptr [rcx + 0x28]
001EA389  mov      rbx, rcx
001EA38C  btr      eax, 0x1f
001EA390  cmp      edx, eax
001EA392  jae      0x1ea3b3  ; -> 001EA3B3
001EA394  mov      rax, qword ptr [rcx + 0x30]
001EA398  mov      edx, edx
001EA39A  lea      rcx, [rax + rdx*8]
001EA39E  mov      rdx, r8
001EA3A1  call     0x1ead40  ; -> 001EAD40 fn
001EA3A6  mov      byte ptr [rbx + 0xe8], 1
001EA3AD  add      rsp, 0x20
001EA3B1  pop      rbx
001EA3B2  ret      
001EA3B3  mov      rdx, r8
001EA3B6  add      rsp, 0x20
001EA3BA  pop      rbx
001EA3BB  jmp      0x1ea1e0  ; -> 001EA1E0 fn
```
