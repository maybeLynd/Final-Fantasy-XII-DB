# Homing pack: `04-Actor-Entity/Actor-Storage-Record/the-actor-storage-record-field-map.md`

Generated 2026-10-03 12:18 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h10-the-actor-storage-record-field-map.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00423280 (76 B, extent 00423280-004232CC)

Entered from (direct sites whose caller this page cites): `002E9560` + 0x45 (jmp; `002E9560` is cited on this page)
Other direct sites: `002E28E0` + 0x265 (call); `002E95B0` + 0x39 (jmp); `003EB250` + 0x17D (call)

Host context: "he sum is zero or dword '+0x284' of that element is 0 | Interior anchor '002E4F63'; Interior anchor '002E4F6F'; Interior anchor '002E4F75'; Interior anchor '002E4F8E'; Interior anchor '002E4F93' | | '002E9560' | 78 B | '002693D0' + 0xC6 | returns 0.0 when 'rcx' is null, when its qword '+0xC0' is null or when the dword that pointer addresses is -1; returns 30.0 ('008F8D80') when that pointer's word '+0' is '0xFFFF', when qword '022C6F28'"

```
00423280  push     rbx
00423282  sub      rsp, 0x20
00423286  cmp      dword ptr [rcx + 0xc4], -1
0042328D  mov      rbx, rcx
00423290  je       0x4232be  ; -> 004232BE
00423292  mov      ecx, dword ptr [rcx + 0x10]
00423295  call     0x20e600  ; -> 0020E600 fn
0042329A  mov      edx, dword ptr [rbx + 0xc4]
004232A0  mov      rcx, qword ptr [rax + 0xda8]
004232A7  call     0x51b9e0  ; -> 0051B9E0 fn
004232AC  test     rax, rax
004232AF  je       0x4232be  ; -> 004232BE
004232B1  mov      rcx, rax
004232B4  add      rsp, 0x20
004232B8  pop      rbx
004232B9  jmp      0x41c3a0  ; -> 0041C3A0 fn
004232BE  movss    xmm0, dword ptr [rip + 0x4d5aba]  ; -> 008F8D80 [f32 30]
004232C6  add      rsp, 0x20
004232CA  pop      rbx
004232CB  ret      
```
