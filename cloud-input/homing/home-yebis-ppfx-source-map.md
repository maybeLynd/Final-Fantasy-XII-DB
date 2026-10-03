# Homing pack: `23-Third-Party-Libraries/PostEffects-Yebis-PPFX/yebis-ppfx-source-map.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-yebis-ppfx-source-map.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001D9D80 (21 B, extent 001D9D80-001D9D95)

Entered from (direct sites whose caller this page cites): `001DADC0` + 0xA3 (call; `001DADC0` is cited on this page)
Other direct sites: none

Host context: "oundary, no shared ownership. - **Resource - CLIENT and SERVICE (17 edges).** '001A52A0', '001A5500', '001A5630', '005CC930' (+1 more) are called by bodies filed to Resource: '001D9F90', '001DA290', '001DADC0', '001F4060' (+4 more); '0079D430', '0079FB10' reach bodies filed to Resource: '00597970', '00598100', '0059BD80', '0059D920' - shared machinery across the layer boundary, no shared ownership.  ## Interior citations for the entry-c"

```
001D9D80  cmp      byte ptr [rcx + 0x130], 0
001D9D87  je       0x1d9d92  ; -> 001D9D92
001D9D89  cmp      byte ptr [rcx + 0x78], 0
001D9D8D  je       0x1d9d92  ; -> 001D9D92
001D9D8F  mov      al, 1
001D9D91  ret      
001D9D92  xor      al, al
001D9D94  ret      
```

## 001DAD30 (41 B, extent 001DAD30-001DAD59)

Entered from (direct sites whose caller this page cites): `001DADC0` + 0x1C9 (call; `001DADC0` is cited on this page)
Other direct sites: none

Host context: "oundary, no shared ownership. - **Resource - CLIENT and SERVICE (17 edges).** '001A52A0', '001A5500', '001A5630', '005CC930' (+1 more) are called by bodies filed to Resource: '001D9F90', '001DA290', '001DADC0', '001F4060' (+4 more); '0079D430', '0079FB10' reach bodies filed to Resource: '00597970', '00598100', '0059BD80', '0059D920' - shared machinery across the layer boundary, no shared ownership.  ## Interior citations for the entry-c"

```
001DAD30  mov      rdx, qword ptr [rcx]
001DAD33  add      rcx, 0x10
001DAD37  mov      r8, qword ptr [rdx + 8]
001DAD3B  mov      rax, qword ptr [rdx]
001DAD3E  mov      qword ptr [r8], rax
001DAD41  mov      r8, qword ptr [rdx]
001DAD44  mov      rax, qword ptr [rdx + 8]
001DAD48  mov      qword ptr [r8 + 8], rax
001DAD4C  mov      r8d, 0x18
001DAD52  mov      rax, qword ptr [rcx]
001DAD55  jmp      qword ptr [rax + 0x18]
```
