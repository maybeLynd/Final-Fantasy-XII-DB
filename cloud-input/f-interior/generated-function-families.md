# F-interior pack: `24-Compiler-And-CRT-Runtime/Generated-Families/generated-function-families.md`

Generated 2026-10-02 18:41 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/generated-function-families.json`.

Functions: 2. Each is cited on the page only at its entry and is still in the F frontier.

## 006B6750 (36 B, extent 006B6750-006B6774)

Page context: "ructors call; '005DC6F0' and '005FDCB0' are the name-registry record and entry register shims; '00810640' is a Lua core call and '00812590' the Lua format-string builder. The other five ('00633240', '006B6750', '006B68A0' for the three Phyre reflection teardown families, '003844F0' for the static-handle replace family, '007DF6D0' for the zero-init initialisers) are cited as targets without a read body. So the residue is those five bodie"

```
006B6750  lea      rdx, [rcx + 8]
006B6754  lea      rax, [rip + 0x6ca1d5]  ; -> 00D80930
006B675B  mov      qword ptr [rcx], rax
006B675E  mov      rcx, qword ptr [rdx]
006B6761  mov      rax, qword ptr [rdx + 8]
006B6765  mov      qword ptr [rcx + 8], rax
006B6769  mov      qword ptr [rax], rcx
006B676C  mov      qword ptr [rdx], rdx
006B676F  mov      qword ptr [rdx + 8], rdx
006B6773  ret      
```

## 006B68A0 (46 B, extent 006B68A0-006B68CE)

Page context: "; '005DC6F0' and '005FDCB0' are the name-registry record and entry register shims; '00810640' is a Lua core call and '00812590' the Lua format-string builder. The other five ('00633240', '006B6750', '006B68A0' for the three Phyre reflection teardown families, '003844F0' for the static-handle replace family, '007DF6D0' for the zero-init initialisers) are cited as targets without a read body. So the residue is those five bodies and the le"

```
006B68A0  lea      r8, [rcx + 0x50]
006B68A4  lea      rax, [rip + 0x6ca0c5]  ; -> 00D80970
006B68AB  mov      qword ptr [rcx], rax
006B68AE  mov      rax, qword ptr [r8 + 8]
006B68B2  mov      rdx, qword ptr [r8]
006B68B5  mov      qword ptr [rdx + 8], rax
006B68B9  mov      qword ptr [rax], rdx
006B68BC  lea      rax, [rip + 0x67a8a5]  ; -> 00D31168
006B68C3  mov      qword ptr [r8], r8
006B68C6  mov      qword ptr [r8 + 8], r8
006B68CA  mov      qword ptr [rcx], rax
006B68CD  ret      
```
