# Homing pack: `19-Save-Load-Settings/CONTRACT-save-image-buffers.md`

Generated 2026-10-03 12:18 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h10-contract-save-image-buffers.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 005DCC10 (47 B, extent 005DCC10-005DCC3F)

Entered from (direct sites whose caller this page cites): `00616140` + 0x16 (call; `00616140` is cited on this page)
Other direct sites: `00611340` + 0x23 (call)

Host context: "at '005DE390' + 0x33, otherwise skips it, and returns | Interior anchor '005DE3A2'; Interior anchor '005DE3AF'; Interior anchor '005DE3B4'; Interior anchor '005DE3BE'; Interior anchor '005DE3C3' | | '00616140' | 89 B | '00162370' + 0x21 | passes 'rcx' unchanged to the call at '00616140' + 0x16; stores dword 0 at 'rcx+0x38' and makes the call at '00616140' + 0x2B with 'rcx' = 'rcx+0x38' and 'edx' = 1; then zeroes qwords '+0x88', '+0x68',"

```
005DCC10  lea      rax, [rip + 0x271ae19]  ; -> 02CF7A30
005DCC17  mov      qword ptr [rcx], rax
005DCC1A  xor      eax, eax
005DCC1C  mov      word ptr [rcx + 8], 0x300
005DCC22  mov      qword ptr [rcx + 0xc], rax
005DCC26  mov      dword ptr [rcx + 0x14], eax
005DCC29  mov      qword ptr [rcx + 0x20], rax
005DCC2D  mov      qword ptr [rcx + 0x28], rax
005DCC31  mov      dword ptr [rcx + 0x30], eax
005DCC34  mov      rax, rcx
005DCC37  mov      dword ptr [rcx + 0x18], 2
005DCC3E  ret      
```

## 005DCC40 (43 B, extent 005DCC40-005DCC6B)

Entered from (direct sites whose caller this page cites): `006161A0` + 0x16 (call; `006161A0` is cited on this page)
Other direct sites: none

Host context: "', '+0x78' and '+0x80' and returns the incoming 'rcx' | Interior anchor '00616156'; Interior anchor '00616160'; Interior anchor '0061616B'; Interior anchor '00616170'; Interior anchor '00616190' | | '006161A0' | 102 B | '00162370' + 0x2E | passes 'rcx' unchanged to the call at '006161A0' + 0x16; stores dword 0 at 'rcx+0x30' and makes the call at '006161A0' + 0x2B with 'rcx' = 'rcx+0x30' and 'edx' = 1; then zeroes qwords '+0xA0', '+0x78'"

```
005DCC40  lea      rax, [rip + 0x271ade9]  ; -> 02CF7A30
005DCC47  mov      qword ptr [rcx], rax
005DCC4A  xor      eax, eax
005DCC4C  mov      word ptr [rcx + 8], 0x300
005DCC52  mov      qword ptr [rcx + 0xc], rax
005DCC56  mov      dword ptr [rcx + 0x14], eax
005DCC59  mov      qword ptr [rcx + 0x20], rax
005DCC5D  mov      dword ptr [rcx + 0x28], eax
005DCC60  mov      rax, rcx
005DCC63  mov      dword ptr [rcx + 0x18], 2
005DCC6A  ret      
```
