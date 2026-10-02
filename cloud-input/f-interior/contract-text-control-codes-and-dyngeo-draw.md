# F-interior pack: `16-UI/CONTRACT-text-control-codes-and-dyngeo-draw.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/contract-text-control-codes-and-dyngeo-draw.json`.

Functions: 2. Each is cited on the page only at its entry and is still in the F frontier.

## 001E0C30 (25 B, extent 001E0C30-001E0C49)

Page context: "e DynGeo shapes. The render pipeline they feed is 'CONTRACT-render-command-list-and-graphics-handshake''s.  **Input — DEPENDENCY, three edges.** The inline-glyph drawer '002AEB20' calls '001E0C10' / '001E0C30' and the control-code dispatch '002AB8F0', which ask the input layer which button glyph a control maps to. The mapping is owned by the input binding pages; the language page's 'UQ-177' residue carries which glyph each letter draws."

```
001E0C30  sub      rsp, 0x28
001E0C34  call     0x796e20  ; -> 00796E20 fn
001E0C39  mov      rcx, qword ptr [rax + 0xdf8]
001E0C40  add      rsp, 0x28
001E0C44  jmp      0x225680  ; -> 00225680 fn
```

## 00214890 (24 B, extent 00214890-002148A8)

Page context: "-Rendering/the-text-control-code-language.md, 16-UI/Dynamic-Geometry-Instances/dyngeo-instance-family.md entries: ["002AC5F0", "003FFAB0", "003FFD70", "002142A0", "00214210", "00214540", "002143E0", "00214890", "002148B0"] registry_slots: [] verified_against:   exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8   method: every body and every table named in sections 2, 3, 4 and 7 was read from the authority     "

```
00214890  mov      rax, qword ptr [rdx]
00214893  movzx    r9d, r8b
00214897  mov      rcx, rdx
0021489A  xor      r8d, r8d
0021489D  movzx    edx, r9b
002148A1  jmp      qword ptr [rax + 0x118]
```
