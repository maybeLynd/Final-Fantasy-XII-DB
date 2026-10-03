# F-interior pack: `16-UI/Handbook/the-handbook-screen.md`

Generated 2026-10-03 02:49 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/the-handbook-screen.json`.

Functions: 2. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 85a2ae3ee	GI DD re-status: repair the audit-sem REJECT of c97af7156; 8006a94ef	SWE2-FRONTIER: P22-B8 review corrections - 002EFD20 byte@0x30 stride, 0032E400 kind-FF early -1, 005; inbox mentions: SWE2-CONTRACT.md, SWE2-DATA.md, SWE2-FRONTIER.md). OPUS read these before packing.

## 001B1F80 (31 B, extent 001B1F80-001B1F9F)

Page context: "t predicates, the '0039xxxx' resource/TIM2/font helpers ('003933F0'/'00393460'/'003934F0'/'003938B0'/'00393900'/'00394850'/'003949B0'/'0039BB60'), the text-emit and leaf layer ('0017FA50'/'001816F0'/'001B1F80'/'0036DD90'/'0036DDA0'/'00374930'), '002F9860'/'002F8040'/'002F83E0'/'002FBEF0'/'002EFD20' string fetch and resource-slot test, and '0024A4E0' the 'Resource'-owned text-label create ('0024A536'/'0024A569'), ~~'002527B0'/~~'002CD7D0"

```
001B1F80  mov      eax, dword ptr [rsp + 0x28]
001B1F84  mov      dword ptr [rcx + 0x3a58], eax
001B1F8A  mov      dword ptr [rcx + 0x3a4c], edx
001B1F90  mov      dword ptr [rcx + 0x3a50], r8d
001B1F97  mov      dword ptr [rcx + 0x3a54], r9d
001B1F9E  ret      
```

## 003A7E80 (90 B, extent 003A7E80-003A7EDA)

Page context: "/'003B2AA0'/ '003B2B40'/'003B2BC0'/'003B2D80'/'003B2F50'), the '003A7xxx'/'003A9xxx' effect-record accessors on the '02EBEFxx' tables and the EFX loader ('003A76F0'/'003A79C0'/'003A7B50'/'003A7D00'/ '003A7E80'/'003A9560'/'003A9730'/'003A9920'/'003A9A70'/'003A9CC0', '003EDAD0'/'003EE2D0'), the '00367820'/'00368010'/'00368360'/'003687C0'/'003688E0'/'00368A60' UI transform evaluator with its '001E0A10'/'001E0E30'/'001E0E50' Input predicate"

```
003A7E80  mov      qword ptr [rsp + 8], rbx
003A7E85  push     rdi
003A7E86  sub      rsp, 0x20
003A7E8A  movzx    r8d, byte ptr [rcx]
003A7E8E  mov      rdi, rcx
003A7E91  add      rcx, 4
003A7E95  movsxd   rbx, edx
003A7E98  mov      r9d, r8d
003A7E9B  movzx    eax, byte ptr [rdi + 2]
003A7E9F  mov      byte ptr [rcx + 0xc2], al
003A7EA5  mov      word ptr [rcx + 0xc0], r8w
003A7EAD  mov      rax, qword ptr [rip + 0x2b170ec]  ; -> 02EBEFA0
003A7EB4  mov      r8, qword ptr [rax]
003A7EB7  mov      qword ptr [r8 + r9*8], rcx
003A7EBB  mov      edx, dword ptr [rip + 0x2b13877]  ; -> 02EBB738
003A7EC1  add      edx, ecx
003A7EC3  call     0x4ff270  ; -> 004FF270 fn
003A7EC8  lea      rax, [rdi + 4]
003A7ECC  add      rax, rbx
003A7ECF  mov      rbx, qword ptr [rsp + 0x30]
003A7ED4  add      rsp, 0x20
003A7ED8  pop      rdi
003A7ED9  ret      
```
