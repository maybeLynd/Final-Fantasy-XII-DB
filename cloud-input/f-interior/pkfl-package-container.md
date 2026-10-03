# F-interior pack: `26-PKFL-Package-Container/Container/pkfl-package-container.md`

Generated 2026-10-02 20:34 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/pkfl-package-container.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: de4492e21	SWE2-CONTRACT: pass-22 debt final - six-folder worklist (597 pairs) fully dispositioned, 0 live find; 01c2429f6	SWE2-CONTRACT: pass-22 debt batch B - 47 Script-VM, Resource, EBP and PKFL pages' cross-subsystem ne; inbox mentions: repos-1e.md, repos-4b.md). OPUS read these before packing.

## 0032F320 (55 B, extent 0032F320-0032F357)

Page context: "sts exactly '0x88' bytes of a manager's '.snd' and '.mot' and '0x208' of its '.vpc' and '.vpcjp' into four per-manager tables ('022C6E98', '022C6E70', '022C6EE8', '022C6EC0'; '0032FE60'–'0032FFE2'); '0032F320' returns slot 'k''s **offset** ('[table + 8k + 8]') and '0032F360' its **size** ('[table + 8k + 0xC]'); the voice loader '003E9EF0' issues ~~'0032E620(kind, packId, dest, size)' with that offset as the request's file offset~~ '0032"

```
0032F320  cmp      ecx, 3
0032F323  jg       0x32f353  ; -> 0032F353
0032F325  movsxd   rax, ecx
0032F328  lea      rcx, [rip - 0x20f32f]  ; -> 00120000 (image base)
0032F32F  test     r8d, r8d
0032F332  jne      0x32f33e  ; -> 0032F33E
0032F334  mov      rcx, qword ptr [rcx + rax*8 + 0x21a6ec0]  ; image base + 0x21a6ec0 = 022C6EC0
0032F33C  jmp      0x32f346  ; -> 0032F346
0032F33E  mov      rcx, qword ptr [rcx + rax*8 + 0x21a6ee8]  ; image base + 0x21a6ee8 = 022C6EE8
0032F346  cmp      byte ptr [rcx], 0
0032F349  je       0x32f353  ; -> 0032F353
0032F34B  movsxd   rax, edx
0032F34E  mov      eax, dword ptr [rcx + rax*8 + 8]
0032F352  ret      
0032F353  or       eax, 0xffffffff
0032F356  ret      
```
