# F-interior pack: `17-Presentation-Rendering/Movie-Containers/mh-movie-seek-index.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/mh-movie-seek-index.json`.

Functions: 2. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 54e8a524e	SWE2-FRONTIER for FABLE: pass-22 unattributed appends - verifier + 23 of 34 PUBLISHABLE pages (batch; inbox mentions: FABLE.md). OPUS read these before packing.

## 001D9F90 (64 B, extent 001D9F90-001D9FD0)

Page context: "ccessor’s spread, not a per-caller relationship. - **Resource - SERVICE (10 edges).** '0017D960', '001B7690', '001B7F30', '001B82F0' (+4 more) reach bodies filed to Resource: '0017D940', '0017D960', '001D9F90', '001DADA0' (+3 more) - shared machinery across the layer boundary, no shared ownership. - **Save_Load_Settings - CLIENT (2 edges).** '002E1CA0' is called by bodies filed to Save_Load_Settings: SaveStorageQueue_ControllerStateHand"

```
001D9F90  cmp      edx, 1
001D9F93  ja       0x1d9fcf  ; -> 001D9FCF
001D9F95  push     rbx
001D9F96  sub      rsp, 0x20
001D9F9A  mov      rbx, rcx
001D9F9D  movsxd   rdx, edx
001D9FA0  or       eax, 0xffffffff
001D9FA3  lock xadd dword ptr [rcx + rdx*4 + 0x24], eax
001D9FA9  call     0x5cc930  ; -> 005CC930 fn
001D9FAE  subsd    xmm0, qword ptr [rip + 0x2adc132]  ; -> 02CB60E8
001D9FB6  cvtsd2ss xmm0, xmm0
001D9FBA  addss    xmm0, dword ptr [rip + 0x1c2301e]  ; -> 01DFCFE0 [f32 2]
001D9FC2  movss    dword ptr [rbx + 0x8c], xmm0
001D9FCA  add      rsp, 0x20
001D9FCE  pop      rbx
001D9FCF  ret      
```

## 0035CF50 (66 B, extent 0035CF50-0035CF92)

Page context: "erStateHandler ('005823B0'), SaveLoad_ControllerLifecycleHandler ('00582860') - shared machinery across the layer boundary, no shared ownership. - **UI - CLIENT and SERVICE (33 edges).** '002E1CA0', '0035CF50', '003C8990' are called by bodies filed to UI: '00251F40', '00254AC0', '00254B50', '00279E20' (+5 more); '00279E20', '0035D6B0', '003C8990' reach bodies filed to UI: '00272EE0', '00273460', '00273A20', '00276960' (+19 more) - share"

```
0035CF50  sub      rsp, 0x28
0035CF54  cmp      qword ptr [rip + 0x1f6d50c], 0  ; -> 022CA468
0035CF5C  je       0x35cf67  ; -> 0035CF67
0035CF5E  cmp      dword ptr [rip + 0x1f6d4f7], 0  ; -> 022CA45C
0035CF65  je       0x35cf8d  ; -> 0035CF8D
0035CF67  xor      edx, edx
0035CF69  lea      ecx, [rdx + 8]
0035CF6C  call     0x2e1ca0  ; -> 002E1CA0 fn
0035CF71  mov      edx, 0xb
0035CF76  lea      ecx, [rdx - 3]
0035CF79  call     0x2e1ca0  ; -> 002E1CA0 fn
0035CF7E  call     0x252d90  ; -> 00252D90 fn
0035CF83  mov      dword ptr [rip + 0x1f6d4cf], 0  ; -> 022CA45C
0035CF8D  add      rsp, 0x28
0035CF91  ret      
```
