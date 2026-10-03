# F-interior pack: `19-Save-Load-Settings/Game-Settings-Config/CONTRACT-game-setting-config.md`

Generated 2026-10-02 20:44 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/contract-game-setting-config.json`.

Functions: 2. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: cd6bd7f58	SWE2-DATA consolidated publish: progress-report cluster (generation store, R3 semantics, DB_GOAL, me; inbox mentions: FABLE.md). OPUS read these before packing.

## 001DDFD0 (119 B, extent 001DDFD0-001DE047)

Page context: "001DEE90' (944 B) is a config-table consumer - '00901098' table lea, two '008C25xx' import-thunk calls, then 10 '00194B00' calls plus '00210EB0'/'001E00D0'/'001DF8C0'. Interior anchor '001DEF3F' (an '001DDFD0' call).  '001DF7D0' (228 B) is the buffer-commit '001DE5D0' runs for an 'r8'-byte payload 'rdx' when 'r8' is non-null and 'r9d & 6 != 6': '+0x70' takes 'r9d' as flags, '001DF990' positions the 'rcx+0x74' region, '00861EBA' copies t"

```
001DDFD0  push     rdi
001DDFD2  sub      rsp, 0x30
001DDFD6  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001DDFDF  mov      qword ptr [rsp + 0x48], rbx
001DDFE4  mov      ebx, edx
001DDFE6  mov      rdi, rcx
001DDFE9  call     qword ptr [rip + 0x6e47a9]  ; -> 008C2798 [u64 0x0000000001CCDA60]
001DDFEF  nop      
001DDFF0  lea      rax, [rip + 0x722f29]  ; -> 00900F20
001DDFF7  mov      qword ptr [rdi], rax
001DDFFA  lea      r8d, [rbx*4]
001DE002  not      r8d
001DE005  and      r8d, 4
001DE009  mov      eax, ebx
001DE00B  mov      ecx, r8d
001DE00E  or       ecx, 2
001DE011  and      al, 2
001DE013  cmovne   ecx, r8d
001DE017  mov      eax, ebx
001DE019  mov      edx, ecx
001DE01B  or       edx, 8
001DE01E  and      al, 8
001DE020  cmove    edx, ecx
001DE023  mov      qword ptr [rdi + 0x68], 0
001DE02B  mov      eax, edx
001DE02D  or       eax, 0x10
001DE030  and      bl, 4
001DE033  cmove    eax, edx
001DE036  mov      dword ptr [rdi + 0x70], eax
001DE039  mov      rax, rdi
001DE03C  mov      rbx, qword ptr [rsp + 0x48]
001DE041  add      rsp, 0x30
001DE045  pop      rdi
001DE046  ret      
```

## 001E00D0 (35 B, extent 001E00D0-001E00F3)

Page context: "A.  ## SWE2-EC7-34 update (2026-09-19) - '001DEE90'  '001DEE90' (944 B) is a config-table consumer - '00901098' table lea, two '008C25xx' import-thunk calls, then 10 '00194B00' calls plus '00210EB0'/'001E00D0'/'001DF8C0'. Interior anchor '001DEF3F' (an '001DDFD0' call).  '001DF7D0' (228 B) is the buffer-commit '001DE5D0' runs for an 'r8'-byte payload 'rdx' when 'r8' is non-null and 'r9d & 6 != 6': '+0x70' takes 'r9d' as flags, '001DF990"

```
001E00D0  push     rbx
001E00D2  sub      rsp, 0x30
001E00D6  add      rcx, 8
001E00DA  mov      dword ptr [rsp + 0x20], 0
001E00E2  mov      rbx, rdx
001E00E5  call     0x1e0100  ; -> 001E0100 fn
001E00EA  mov      rax, rbx
001E00ED  add      rsp, 0x30
001E00F1  pop      rbx
001E00F2  ret      
```
