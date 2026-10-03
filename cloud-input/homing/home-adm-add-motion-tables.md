# Homing pack: `17-Presentation-Rendering/Model-And-Motion-Formats/adm-add-motion-tables.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-adm-add-motion-tables.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002ECCF0 (33 B, extent 002ECCF0-002ECD11)

Entered from (direct sites whose caller this page cites): `00262F50` + 0x20 (call; `00262F50` is cited on this page)
Other direct sites: none

Host context: "001BE430' (235 B) is a body - '0017D2E0'/'00808C40'. Interior anchor '001BE466' (an '0017D2E0' call).  ## SWE2-EC7-58 update (2026-09-19) - '00352FA0'  '00352FA0' (166 B) is an adm-add-motion body - '00262F50'/'00263750'/'00264050'/'002647C0'/'00267E10'/'0026B4E0'/'00377C20'. Interior anchor '00352FB8' (a '00267E10' call).  ## SWE2-EC7-60 update (2026-09-19) - '00344740'  '00344740' (156 B) is an adm-add-motion body - '00233D70'/'002637"

```
002ECCF0  test     rcx, rcx
002ECCF3  je       0x2ecd10  ; -> 002ECD10
002ECCF5  mov      rax, qword ptr [rcx + 0xc0]
002ECCFC  test     rax, rax
002ECCFF  je       0x2ecd10  ; -> 002ECD10
002ECD01  cmp      dword ptr [rax], -1
002ECD04  je       0x2ecd10  ; -> 002ECD10
002ECD06  and      byte ptr [rax + 0x11], 0x7f
002ECD0A  shl      dl, 7
002ECD0D  or       byte ptr [rax + 0x11], dl
002ECD10  ret      
```

## 002EDB80 (72 B, extent 002EDB80-002EDBC8)

Entered from (direct sites whose caller this page cites): `002E7CE0` + 0xCD (call; `002E7CE0` is cited on this page)
Other direct sites: none

Host context: "s body-model **set** operation sends request 1 to the base element's record and request 2 to the body-model element's record; its **clear** operation sends 0 to both. One other body reads the state, '002E7CE0' (226 B): it applies a 16-bit value to the base record and, **only while that record is in state 1**, to the body-model record too. *What that value is was not established.* Interior: '002EDFB5', '002EDFCE', '002EDFEA', '002EDFF9',"

```
002EDB80  sub      rsp, 0x28
002EDB84  cmp      cx, -1
002EDB88  je       0x2edbc3  ; -> 002EDBC3
002EDB8A  mov      qword ptr [rsp + 0x20], rbx
002EDB8F  movsx    rax, cx
002EDB93  imul     rbx, rax, 0x740
002EDB9A  add      rbx, qword ptr [rip + 0x1fd9387]  ; -> 022C6F28
002EDBA1  je       0x2edbbe  ; -> 002EDBBE
002EDBA3  cmp      dword ptr [rbx + 0x284], 0
002EDBAA  je       0x2edbbe  ; -> 002EDBBE
002EDBAC  mov      rcx, rbx
002EDBAF  call     0x3e6ce0  ; -> 003E6CE0 fn
002EDBB4  or       dword ptr [rbx + 0x290], 0x800
002EDBBE  mov      rbx, qword ptr [rsp + 0x20]
002EDBC3  add      rsp, 0x28
002EDBC7  ret      
```
