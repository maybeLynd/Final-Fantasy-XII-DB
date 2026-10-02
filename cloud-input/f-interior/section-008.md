# F-interior pack: `25-EBP-Script-Container/Sections/section-008.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/section-008.json`.

Functions: 2. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: b199fc9e1	SWE2-CONTRACT: pass-22 round 2 - five helper-only bullets re-read (3 relabelled MECHANICAL, 5 re-exp; bafa49c9f	SWE2-DATA: bucket member formats declared - 53 .bin + 5 .dat members, every entry assigned, each cla; inbox mentions: ASSIGNMENTS.md, SWE2-CONTRACT.md, repos-4b.md, repos-c7.md, repos-c9.md). OPUS read these before packing.

## 0034E9B0 (90 B, extent 0034E9B0-0034EA0A)

Page context: "0x04' and loads > '[blob + entry·0x10 + 0x14]', entry '+0x04', at '0x003DA456' as the 'section_009' record to play; '0x003DA330', behind > 'camerahitcheck' ('0x0034EDB0') and 'camerahitcheck_33c' ('0x0034E9B0'), loads the same field at '0x003DA35E'. > > The earlier reading below took the gate for a platform predicate that might return either value and did not read > the routine it ends in. Evidence, with the byte reads, the six call-sit"

```
0034E9B0  mov      qword ptr [rsp + 8], rbx
0034E9B5  mov      qword ptr [rsp + 0x10], rsi
0034E9BA  push     rdi
0034E9BB  sub      rsp, 0x20
0034E9BF  mov      rsi, rcx
0034E9C2  mov      rbx, r9
0034E9C5  mov      rcx, r9
0034E9C8  call     0x267e10  ; -> 00267E10 fn
0034E9CD  mov      rcx, rbx
0034E9D0  mov      edi, eax
0034E9D2  call     0x267e10  ; -> 00267E10 fn
0034E9D7  mov      ebx, eax
0034E9D9  call     0x2640c0  ; -> 002640C0 fn
0034E9DE  and      ebx, 0xffffff
0034E9E4  mov      r8d, edi
0034E9E7  mov      edx, ebx
0034E9E9  mov      rcx, rax
0034E9EC  call     0x3da330  ; -> 003DA330 fn
0034E9F1  mov      edx, eax
0034E9F3  mov      rcx, rsi
0034E9F6  mov      rbx, qword ptr [rsp + 0x30]
0034E9FB  mov      rsi, qword ptr [rsp + 0x38]
0034EA00  add      rsp, 0x20
0034EA04  pop      rdi
0034EA05  jmp      0x26b4e0  ; -> 0026B4E0 fn
```

## 0034EDB0 (101 B, extent 0034EDB0-0034EE15)

Page context: "nds the script's entry number against '+0x04' and loads > '[blob + entry·0x10 + 0x14]', entry '+0x04', at '0x003DA456' as the 'section_009' record to play; '0x003DA330', behind > 'camerahitcheck' ('0x0034EDB0') and 'camerahitcheck_33c' ('0x0034E9B0'), loads the same field at '0x003DA35E'. > > The earlier reading below took the gate for a platform predicate that might return either value and did not read > the routine it ends in. Evidenc"

```
0034EDB0  mov      qword ptr [rsp + 8], rbx
0034EDB5  mov      qword ptr [rsp + 0x10], rsi
0034EDBA  push     rdi
0034EDBB  sub      rsp, 0x20
0034EDBF  mov      rsi, rcx
0034EDC2  or       edx, 0xffffffff
0034EDC5  mov      rcx, r9
0034EDC8  mov      rbx, r9
0034EDCB  call     0x267f90  ; -> 00267F90 fn
0034EDD0  mov      rcx, rbx
0034EDD3  call     0x267e10  ; -> 00267E10 fn
0034EDD8  mov      rcx, rbx
0034EDDB  mov      edi, eax
0034EDDD  call     0x267e10  ; -> 00267E10 fn
0034EDE2  mov      ebx, eax
0034EDE4  call     0x2640c0  ; -> 002640C0 fn
0034EDE9  and      ebx, 0xffffff
0034EDEF  mov      r8d, edi
0034EDF2  mov      edx, ebx
0034EDF4  mov      rcx, rax
0034EDF7  call     0x3da330  ; -> 003DA330 fn
0034EDFC  mov      edx, eax
0034EDFE  mov      rcx, rsi
0034EE01  mov      rbx, qword ptr [rsp + 0x30]
0034EE06  mov      rsi, qword ptr [rsp + 0x38]
0034EE0B  add      rsp, 0x20
0034EE0F  pop      rdi
0034EE10  jmp      0x26b4e0  ; -> 0026B4E0 fn
```
