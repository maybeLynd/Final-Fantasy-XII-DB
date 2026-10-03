# F-interior pack: `07-Combat-Action/CONTRACT-the-moment-an-action-is-committed.md`

Generated 2026-10-02 20:18 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/contract-the-moment-an-action-is-committed.json`.

Functions: 2. Each is cited on the page only at its entry and is still in the F frontier.

## 003AEF30 (29 B, extent 003AEF30-003AEF4D)

Page context: "Defaults' '0041F730' (calls '003E5D00'; called by '004200A0', 'CharacterRenderSystem_Initialize' '004269A0', '004279B0' and '00429140') and 'CharacterRenderRecord_TeardownAndReset' '004200A0' (calls '003AEF30', '003E69A0', '0041E860', '0041F730' and '00512C80'; called by '00427C90') are cited only in section 14's '+0x718' displacement census: '001D0390', '003714A0' and '004200A0' as hits decoded and rejected because they are other struc"

```
003AEF30  mov      rax, qword ptr [rcx + 0x18]
003AEF34  mov      dword ptr [rcx], 0
003AEF3A  test     rax, rax
003AEF3D  je       0x3aef4c  ; -> 003AEF4C
003AEF3F  nop      
003AEF40  mov      byte ptr [rax], 0
003AEF43  mov      rax, qword ptr [rax + 0x48]
003AEF47  test     rax, rax
003AEF4A  jne      0x3aef40  ; -> 003AEF40
003AEF4C  ret      
```

## 003E69A0 (50 B, extent 003E69A0-003E69D2)

Page context: "041F730' (calls '003E5D00'; called by '004200A0', 'CharacterRenderSystem_Initialize' '004269A0', '004279B0' and '00429140') and 'CharacterRenderRecord_TeardownAndReset' '004200A0' (calls '003AEF30', '003E69A0', '0041E860', '0041F730' and '00512C80'; called by '00427C90') are cited only in section 14's '+0x718' displacement census: '001D0390', '003714A0' and '004200A0' as hits decoded and rejected because they are other structures at tha"

```
003E69A0  push     rbx
003E69A2  sub      rsp, 0x20
003E69A6  mov      rbx, rcx
003E69A9  mov      ecx, dword ptr [rcx + 0x448]
003E69AF  test     ecx, ecx
003E69B1  je       0x3e69b8  ; -> 003E69B8
003E69B3  call     0x3d8300  ; -> 003D8300 fn
003E69B8  mov      ecx, dword ptr [rbx + 0x44c]
003E69BE  test     ecx, ecx
003E69C0  je       0x3e69cc  ; -> 003E69CC
003E69C2  add      rsp, 0x20
003E69C6  pop      rbx
003E69C7  jmp      0x3d8300  ; -> 003D8300 fn
003E69CC  add      rsp, 0x20
003E69D0  pop      rbx
003E69D1  ret      
```
