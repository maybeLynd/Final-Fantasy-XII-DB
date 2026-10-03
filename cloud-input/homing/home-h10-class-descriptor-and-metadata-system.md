# Homing pack: `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`

Generated 2026-10-03 12:18 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h10-class-descriptor-and-metadata-system.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 006B6820 (114 B, extent 006B6820-006B6892)

Entered from (direct sites whose caller this page cites): `00661A70` + 0x7A (call; `00661A70` is cited on this page); `006D5810` + 0x7A (call; `006D5810` is cited on this page)
Other direct sites: `005A65B0` + 0x7A (call); `005D8BE0` + 0x7A (call); `0062CC80` + 0x7A (call); `006B6B60` + 0x7A (call); `006BEAC0` + 0x7A (call); `006C0C90` + 0x7A (call); `006CD270` + 0x7A (call); `006D94E0` + 0x7A (call); `006D98D0` + 0x7A (call); `00875F00` + 0x7A (call); `008762F0` + 0x7A (call); `008766D0` + 0x7A (call); `00876AE0` + 0x7A (call); `00876EC0` + 0x7A (call); `008793D0` + 0x7A (call)

Host context: "body constructs no class descriptor. X is a static data-member object in 15 rows ('PClassDataMember*<…>'), a 'PTypeDefault<unsigned int>' in '006315B0', and a 'PNamedSemanticDescriptorForType<…>' in '00661A70' and '006D5810'. ['fam_rows.py'](../../_index/candidates/opus-ee-guarded-registration-1003/fam_rows.py) re-derives every row and compares it with the committed ['rows.tsv'](../../_index/candidates/opus-ee-guarded-registration-1003/" / " no class descriptor. X is a static data-member object in 15 rows ('PClassDataMember*<…>'), a 'PTypeDefault<unsigned int>' in '006315B0', and a 'PNamedSemanticDescriptorForType<…>' in '00661A70' and '006D5810'. ['fam_rows.py'](../../_index/candidates/opus-ee-guarded-registration-1003/fam_rows.py) re-derives every row and compares it with the committed ['rows.tsv'](../../_index/candidates/opus-ee-guarded-registration-1003/rows.tsv). Two "

```
006B6820  mov      r10, rcx
006B6823  lea      rax, [rcx + 8]
006B6827  mov      qword ptr [rax], rax
006B682A  xor      ecx, ecx
006B682C  mov      qword ptr [rax + 8], rax
006B6830  mov      qword ptr [rax + 0x10], rax
006B6834  mov      dword ptr [rax + 0x18], ecx
006B6837  mov      qword ptr [rax + 0x20], rcx
006B683B  lea      rcx, [r10 + 0x50]
006B683F  mov      rax, qword ptr [rsp + 0x28]
006B6844  mov      qword ptr [r10 + 0x40], rax
006B6848  mov      rax, qword ptr [rsp + 0x30]
006B684D  mov      qword ptr [r10 + 0x48], rax
006B6851  lea      rax, [rip + 0x6ca118]  ; -> 00D80970
006B6858  mov      qword ptr [r10 + 0x30], rdx
006B685C  lea      rdx, [rip + 0x1878355]  ; -> 01F2EBB8
006B6863  mov      dword ptr [r10 + 0x38], r8d
006B6867  mov      dword ptr [r10 + 0x3c], r9d
006B686B  mov      qword ptr [rcx], rcx
006B686E  mov      qword ptr [rcx + 8], rcx
006B6872  mov      qword ptr [r10], rax
006B6875  mov      rax, qword ptr [rip + 0x187833c]  ; -> 01F2EBB8 [u64 0x0000000001F2EBB8]
006B687C  mov      qword ptr [rcx], rax
006B687F  mov      qword ptr [rcx + 8], rdx
006B6883  mov      qword ptr [rip + 0x187832e], rcx  ; -> 01F2EBB8 [u64 0x0000000001F2EBB8]
006B688A  mov      qword ptr [rax + 8], rcx
006B688E  mov      rax, r10
006B6891  ret      
```
