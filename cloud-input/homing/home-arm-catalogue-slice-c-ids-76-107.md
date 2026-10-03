# Homing pack: `00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-C-ids-76-107.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-arm-catalogue-slice-c-ids-76-107.json`.

Bodies: 3. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001C2D10 (61 B, extent 001C2D10-001C2D4D)

Entered from (direct sites whose caller this page cites): `001C2980` + 0x111 (call; `001C2980` is cited on this page)
Other direct sites: none

Host context: "alls 'Platform' '005CC930' (1) — the same shared-accessor and arm shape as the sibling slices.)*  ## SWE2-EC7-109 update (2026-09-20) - '001EAD20' measured  '001EAD20' (24 B) is the two-float setter '001C2980' and '001D0390' call: 'float[rcx + 0xF0] = xmm1', 'float[rcx + 0xF4] = xmm2', 'byte[rcx + 0xE9] = 1' - the float twin of '001EAA90''s dword pair, same dirty latch. Interior anchor '001EAD28' (the '+0xF4' store).  ## Cross-subsystem"

```
001C2D10  test     rdx, rdx
001C2D13  je       0x1c2d4c  ; -> 001C2D4C
001C2D15  test     r8, r8
001C2D18  je       0x1c2d4c  ; -> 001C2D4C
001C2D1A  movss    xmm0, dword ptr [rcx + 0x4664]
001C2D22  mulss    xmm0, dword ptr [rdx]
001C2D26  subss    xmm0, dword ptr [rip + 0x7370a2]  ; -> 008F9DD0 [f32 1.65]
001C2D2E  movss    dword ptr [rdx], xmm0
001C2D32  movss    xmm1, dword ptr [rcx + 0x4668]
001C2D3A  mulss    xmm1, dword ptr [r8]
001C2D3F  subss    xmm1, dword ptr [rip + 0x1b28ec1]  ; -> 01CEBC08 [f32 2]
001C2D47  movss    dword ptr [r8], xmm1
001C2D4C  ret      
```

## 001C2D50 (83 B, extent 001C2D50-001C2DA3)

Entered from (direct sites whose caller this page cites): `001C2980` + 0x23C (call; `001C2980` is cited on this page)
Other direct sites: none

Host context: "alls 'Platform' '005CC930' (1) — the same shared-accessor and arm shape as the sibling slices.)*  ## SWE2-EC7-109 update (2026-09-20) - '001EAD20' measured  '001EAD20' (24 B) is the two-float setter '001C2980' and '001D0390' call: 'float[rcx + 0xF0] = xmm1', 'float[rcx + 0xF4] = xmm2', 'byte[rcx + 0xE9] = 1' - the float twin of '001EAA90''s dword pair, same dirty latch. Interior anchor '001EAD28' (the '+0xF4' store).  ## Cross-subsystem"

```
001C2D50  sub      rsp, 0x38
001C2D54  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
001C2D5D  mov      r9, rcx
001C2D60  mov      rcx, qword ptr [rcx + 8]
001C2D64  cmp      rcx, qword ptr [r9 + 0x10]
001C2D68  jae      0x1c2d8c  ; -> 001C2D8C
001C2D6A  mov      qword ptr [rsp + 0x40], rcx
001C2D6F  lea      rax, [rcx + 0x230]
001C2D76  mov      qword ptr [r9 + 8], rax
001C2D7A  mov      qword ptr [rsp + 0x50], rcx
001C2D7F  test     rcx, rcx
001C2D82  je       0x1c2d8a  ; -> 001C2D8A
001C2D84  call     0x1c1c80  ; -> 001C1C80 fn
001C2D89  nop      
001C2D8A  jmp      0x1c2d9e  ; -> 001C2D9E
001C2D8C  mov      r8, rdx
001C2D8F  mov      rdx, rcx
001C2D92  mov      rcx, r9
001C2D95  add      rsp, 0x38
001C2D99  jmp      0x1c2790  ; -> 001C2790 fn
001C2D9E  add      rsp, 0x38
001C2DA2  ret      
```

## 001EE5D0 (123 B, extent 001EE5D0-001EE64B)

Entered from (direct sites whose caller this page cites): `00187950` + 0x6B (call; `00187950` is cited on this page)
Other direct sites: none

Host context: "/Application-Root/game-application.md) lists it as the object pumped three times per tick and its setup '00184F20' as SceneCamera-tagged. The fields are read in one other place, the render pass list '00187950': when the object's byte '+0xC0C' is set it copies '+0xCC4', '+0xCC8' and '+0xCCC' into the camera object's '+0xD0', '+0xC8' and '+0xD4', calling the camera's vtable slot 1 after each store ('0018821B'..'00188263'). Beside them, id"

```
001EE5D0  mov      eax, dword ptr [rsp + 0x28]
001EE5D4  mov      r10, rdx
001EE5D7  mov      edx, dword ptr [rsp + 0x30]
001EE5DB  cmp      r8d, eax
001EE5DE  jne      0x1ee5ed  ; -> 001EE5ED
001EE5E0  cmp      r9d, edx
001EE5E3  jne      0x1ee5ed  ; -> 001EE5ED
001EE5E5  xor      eax, eax
001EE5E7  mov      dword ptr [r10], eax
001EE5EA  mov      dword ptr [rcx], eax
001EE5EC  ret      
001EE5ED  movd     xmm3, eax
001EE5F1  movd     xmm0, edx
001EE5F5  movd     xmm2, r8d
001EE5FA  movd     xmm1, r9d
001EE5FF  cvtdq2ps xmm3, xmm3
001EE602  cvtdq2ps xmm0, xmm0
001EE605  cvtdq2ps xmm2, xmm2
001EE608  cvtdq2ps xmm1, xmm1
001EE60B  divss    xmm3, xmm0
001EE60F  divss    xmm2, xmm1
001EE613  comiss   xmm3, xmm2
001EE616  jbe      0x1ee631  ; -> 001EE631
001EE618  sub      r8d, eax
001EE61B  mov      eax, r8d
001EE61E  cdq      
001EE61F  sub      eax, edx
001EE621  sar      eax, 1
001EE623  mov      dword ptr [rcx], eax
001EE625  jns      0x1ee629  ; -> 001EE629
001EE627  neg      eax
001EE629  mov      dword ptr [rcx], eax
001EE62B  xor      eax, eax
001EE62D  mov      dword ptr [r10], eax
001EE630  ret      
001EE631  xor      eax, eax
001EE633  sub      r9d, edx
001EE636  mov      dword ptr [rcx], eax
001EE638  mov      eax, r9d
001EE63B  cdq      
001EE63C  sub      eax, edx
001EE63E  sar      eax, 1
001EE640  mov      dword ptr [r10], eax
001EE643  jns      0x1ee647  ; -> 001EE647
001EE645  neg      eax
001EE647  mov      dword ptr [r10], eax
001EE64A  ret      
```
