# Homing pack: `04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md`

Generated 2026-10-03 15:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h14-the-record-00329220-builds.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 003F2580 (65 B, extent 003F2580-003F25C1)

Entered from (direct sites whose caller this page cites): `002915C0` + 0x15A (call; `002915C0` is cited on this page)
Other direct sites: none

Host context: "** '00181350' calls '001B06D0' and is called by '0022FFE0'/'00274CB0'/'003C7xxx' of that layer — a two-way render-helper exchange, not a second owner. **Resource — SERVICE (SWE2-EC7-156, 2 edges).** '002915C0'/'002917E0' call '0024A5A0' of that layer — the record's helpers consume a resource-side helper, not a shared responsibility. **UI — CLIENT (SWE2-EC7-156, 242 edges).** '002A0440' calls '00181560', '002915C0'/'002917E0'/'002C7660' "

```
003F2580  mov      r8, rcx
003F2583  test     rcx, rcx
003F2586  jne      0x3f258c  ; -> 003F258C
003F2588  mov      rax, rdx
003F258B  ret      
003F258C  mov      rax, qword ptr [rcx + 0x9b0]
003F2593  test     rax, rax
003F2596  je       0x3f25af  ; -> 003F25AF
003F2598  nop      dword ptr [rax + rax]
003F25A0  mov      rcx, rax
003F25A3  mov      rax, qword ptr [rax + 0x9b0]
003F25AA  test     rax, rax
003F25AD  jne      0x3f25a0  ; -> 003F25A0
003F25AF  mov      qword ptr [rcx + 0x9b0], rdx
003F25B6  mov      rax, r8
003F25B9  mov      qword ptr [rdx + 0x9b8], rcx
003F25C0  ret      
```

## 003F2600 (234 B, extent 003F2600-003F26EA)

Entered from (direct sites whose caller this page cites): `002915C0` + 0x13F (call; `002915C0` is cited on this page)
Other direct sites: none

Host context: "** '00181350' calls '001B06D0' and is called by '0022FFE0'/'00274CB0'/'003C7xxx' of that layer — a two-way render-helper exchange, not a second owner. **Resource — SERVICE (SWE2-EC7-156, 2 edges).** '002915C0'/'002917E0' call '0024A5A0' of that layer — the record's helpers consume a resource-side helper, not a shared responsibility. **UI — CLIENT (SWE2-EC7-156, 242 edges).** '002A0440' calls '00181560', '002915C0'/'002917E0'/'002C7660' "

```
003F2600  mov      qword ptr [rsp + 8], rbx
003F2605  push     rdi
003F2606  sub      rsp, 0x20
003F260A  mov      r9d, 0x20
003F2610  mov      rbx, rdx
003F2613  lea      rdx, [rcx + 0x3c0]
003F261A  mov      rdi, rcx
003F261D  lea      r8d, [r9 - 0x1a]
003F2621  call     0x3f2a70  ; -> 003F2A70 fn
003F2626  lea      rcx, [rdi + 0x780]
003F262D  mov      dword ptr [rdi + 0x998], 0x3f800000
003F2637  mov      rdx, rbx
003F263A  call     0x3f2f20  ; -> 003F2F20 fn
003F263F  lea      rcx, [rdi + 0x870]
003F2646  mov      rdx, rbx
003F2649  call     0x3f2f20  ; -> 003F2F20 fn
003F264E  mov      eax, dword ptr [rbx]
003F2650  mov      dword ptr [rdi + 0x970], eax
003F2656  movss    xmm0, dword ptr [rbx + 4]
003F265B  movaps   xmm1, xmm0
003F265E  mulss    xmm1, dword ptr [rip + 0x18f950a]  ; -> 01CEBB70 [f32 0.5]
003F2666  divss    xmm0, dword ptr [rip + 0x505b12]  ; -> 008F8180 [f32 10]
003F266E  subss    xmm1, xmm0
003F2672  movss    dword ptr [rdi + 0x974], xmm1
003F267A  mov      eax, dword ptr [rbx + 8]
003F267D  mov      dword ptr [rdi + 0x978], eax
003F2683  movss    xmm0, dword ptr [rbx + 4]
003F2688  movaps   xmm1, xmm0
003F268B  mulss    xmm1, dword ptr [rip + 0x18f94dd]  ; -> 01CEBB70 [f32 0.5]
003F2693  divss    xmm0, dword ptr [rip + 0x505ae5]  ; -> 008F8180 [f32 10]
003F269B  addss    xmm1, dword ptr [rbx + 0xc]
003F26A0  mov      rbx, qword ptr [rsp + 0x30]
003F26A5  mov      dword ptr [rdi + 0x924], 0x3e570a3d
003F26AF  mov      dword ptr [rdi + 0x92c], 0x3e4ccccd
003F26B9  mov      dword ptr [rdi + 0x930], 0x42fe0000
003F26C3  addss    xmm1, xmm0
003F26C7  mov      dword ptr [rdi + 0x934], 0x42fe0000
003F26D1  mov      qword ptr [rdi + 0x938], 0x42fe0000
003F26DC  movss    dword ptr [rdi + 0x97c], xmm1
003F26E4  add      rsp, 0x20
003F26E8  pop      rdi
003F26E9  ret      
```
