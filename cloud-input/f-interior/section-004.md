# F-interior pack: `25-EBP-Script-Container/Sections/section-004.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/section-004.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 01c2429f6	SWE2-CONTRACT: pass-22 debt batch B - 47 Script-VM, Resource, EBP and PKFL pages' cross-subsystem ne; inbox mentions: ASSIGNMENTS.md, repos-4b.md, repos-c9.md). OPUS read these before packing.

## 003DFCC0 (50 B, extent 003DFCC0-003DFCF2)

Page context: "ection's binding has no teardown while 'section_019''s does.  **The consumer module.** '02B59D58' has **six** references, all RIP-relative, all inside one module: '003DFA8A', '003DFA9B', '003DFC14', '003DFCC0', '003DFDA3' and the store at '003DFDC0'. 'FUN_003DFA50' (98 bytes) is the teardown, and its shape confirms the array reading — it loops **twice** ('003DFA66 MOV EDI,2') over 'g_fieldRoots[0]' and '[1]' from '003DFA5F LEA RBX,[02B5"

```
003DFCC0  mov      rdx, qword ptr [rip + 0x277a091]  ; -> 02B59D58
003DFCC7  test     rdx, rdx
003DFCCA  je       0x3dfcef  ; -> 003DFCEF
003DFCCC  cmp      byte ptr [rdx + 7], 0x32
003DFCD0  jb       0x3dfcef  ; -> 003DFCEF
003DFCD2  movzx    eax, word ptr [rdx + 8]
003DFCD6  cmp      ecx, eax
003DFCD8  jge      0x3dfcef  ; -> 003DFCEF
003DFCDA  test     ecx, ecx
003DFCDC  je       0x3dfcef  ; -> 003DFCEF
003DFCDE  lea      eax, [rcx - 1]
003DFCE1  cmp      eax, 8
003DFCE4  ja       0x3dfcef  ; -> 003DFCEF
003DFCE6  movsxd   rax, ecx
003DFCE9  movzx    eax, word ptr [rdx + rax*4 + 0xc]
003DFCEE  ret      
003DFCEF  xor      eax, eax
003DFCF1  ret      
```
