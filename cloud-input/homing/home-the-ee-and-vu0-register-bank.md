# Homing pack: `00-Engine-Core-Runtime/Shared-Transform-Workbench/the-ee-and-vu0-register-bank.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-ee-and-vu0-register-bank.json`.

Bodies: 3. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 003AC870 (24 B, extent 003AC870-003AC888)

Entered from (direct sites whose caller this page cites): `00376470` + 0x82 (call; `00376470` is cited on this page)
Other direct sites: none

Host context: "nts) | 20 | | MMI/SIMD-heavy mixed | 16 |  The 20-row 'C-fragment' class is defined by **at most four bank accesses**, not by vf00 alone — eight of them touch non-vf00 registers ('002F67C0' 'Wvf01'; '00376470' 'Rvf00×2 Wvf01'; '003A2B90' '$v0'+'vf21'+'vf20'; '003B4310'/'003B5D40'/'0053DB50' 'W$t0'; '004010A0' 'vf20'+'$t0'; '0044B960' 'vf21'). Rows touching only 'Rvf00' are C routines borrowing the constant.  **Families the caller map al"

```
003AC870  movss    xmm0, dword ptr [rip + 0x193f330]  ; -> 01CEBBA8 [f32 1]
003AC878  movss    dword ptr [rip + 0x2792c9c], xmm0  ; -> 02B3F51C
003AC880  mov      byte ptr [rip + 0x2792c7c], 0  ; -> 02B3F503
003AC887  ret      
```

## 006AA200 (34 B, extent 006AA200-006AA222)

Entered from (direct sites whose caller this page cites): `006BA940` + 0x5E (jmp; `006BA940` is cited on this page); `006BAA40` + 0x60 (call; `006BAA40` is cited on this page); `006CE570` + 0x19 (call; `006CE570` is cited on this page)
Other direct sites: `008B70D0` + 0x15 (jmp)

Host context: "BAA40'. But nothing hands it work: the constructors are called only from the getter (whole-image call sweep), the pool object is referenced only by the getter and the static destructor '008B41F0' (→ '006BA940'), and the getter's two callers are the boot initialiser '005A08E0', which calls slot 2 *start* ('006BAB40', '005A0A99'), and the shutdown '005A0840', which calls slot 3 *terminate* ('006BAED0', '005A0882'). The submit slot 5 — '00" / "e object it is given ('call [rax+8]' at '0086350C'), the slot-1 bodies of every thread class the RTTI names — 'crossThreadImpl' '00863410', 'Phyre::PThreadPool' '006AA230', 'PThreadPoolWorkStealing' '006BAA40', 'PThreadPoolImmediate' '006CE570' ('Sys::Thread''s slot 1 is '_purecall'). **Result: the update loop reaches 183 of the 267 members and the draw loop 40; the 35 they share are one thread, because both loops hang from the same cal"

```
006AA200  sub      rsp, 0x38
006AA204  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
006AA20D  lea      rax, [rip + 0x6d264c]  ; -> 00D7C860
006AA214  mov      qword ptr [rcx], rax
006AA217  call     0x6aa600  ; -> 006AA600 fn
006AA21C  nop      
006AA21D  add      rsp, 0x38
006AA221  ret      
```

## 006AA600 (190 B, extent 006AA600-006AA6BE)

Entered from (direct sites whose caller this page cites): `006AA230` + 0x23 (call; `006AA230` is cited on this page); `006BAED0` + 0xB5 (call; `006BAED0` is cited on this page)
Other direct sites: `006AA200` + 0x17 (call)

Host context: "ine that calls **vtable slot 1** of the object it is given ('call [rax+8]' at '0086350C'), the slot-1 bodies of every thread class the RTTI names — 'crossThreadImpl' '00863410', 'Phyre::PThreadPool' '006AA230', 'PThreadPoolWorkStealing' '006BAA40', 'PThreadPoolImmediate' '006CE570' ('Sys::Thread''s slot 1 is '_purecall'). **Result: the update loop reaches 183 of the 267 members and the draw loop 40; the 35 they share are one thread, bec" / "0' (→ '006BA940'), and the getter's two callers are the boot initialiser '005A08E0', which calls slot 2 *start* ('006BAB40', '005A0A99'), and the shutdown '005A0840', which calls slot 3 *terminate* ('006BAED0', '005A0882'). The submit slot 5 — '006BAAD0', which appends a job object to the queue at pool '+0x28' / '+0x80' and kicks slot 6 when a batch fills; or the immediate pool's '006CE650', which tail-jumps the job's slot 1 on the call"

```
006AA600  push     rdi
006AA602  sub      rsp, 0x30
006AA606  mov      qword ptr [rsp + 0x20], 0xfffffffffffffffe
006AA60F  mov      qword ptr [rsp + 0x48], rbx
006AA614  mov      qword ptr [rsp + 0x50], rbp
006AA619  mov      qword ptr [rsp + 0x58], rsi
006AA61E  mov      rdi, rcx
006AA621  xor      ebp, ebp
006AA623  cmp      qword ptr [rcx + 8], rbp
006AA627  je       0x6aa660  ; -> 006AA660
006AA629  mov      esi, ebp
006AA62B  cmp      dword ptr [rcx + 0x10], ebp
006AA62E  jbe      0x6aa660  ; -> 006AA660
006AA630  mov      eax, esi
006AA632  imul     rbx, rax, 0x38
006AA636  add      rbx, qword ptr [rdi + 8]
006AA63A  mov      dword ptr [rsp + 0x40], ebp
006AA63E  lea      rdx, [rsp + 0x40]
006AA643  lea      rcx, [rbx + 0x10]
006AA647  call     0x5cd330  ; -> 005CD330 fn
006AA64C  lea      rcx, [rbx + 0x10]
006AA650  call     0x5c5230  ; -> 005C5230 fn
006AA655  mov      byte ptr [rbx + 0x28], bpl
006AA659  inc      esi
006AA65B  cmp      esi, dword ptr [rdi + 0x10]
006AA65E  jb       0x6aa630  ; -> 006AA630
006AA660  mov      rcx, qword ptr [rdi + 8]
006AA664  test     rcx, rcx
006AA667  je       0x6aa68b  ; -> 006AA68B
006AA669  lea      rbx, [rcx - 8]
006AA66D  lea      r9, [rip - 0x53cfd4]  ; -> 0016D6A0
006AA674  mov      r8, qword ptr [rbx]
006AA677  mov      edx, 0x38
006AA67C  call     0x809054  ; -> 00809054 fn
006AA681  nop      
006AA682  mov      rcx, rbx
006AA685  call     0x584730  ; -> 00584730 fn
006AA68A  nop      
006AA68B  mov      rcx, qword ptr [rdi + 0x28]
006AA68F  call     0x584730  ; -> 00584730 fn
006AA694  mov      rcx, qword ptr [rdi + 0x18]
006AA698  call     0x584730  ; -> 00584730 fn
006AA69D  mov      qword ptr [rdi + 8], rbp
006AA6A1  mov      qword ptr [rdi + 0x28], rbp
006AA6A5  mov      qword ptr [rdi + 0x18], rbp
006AA6A9  mov      rbx, qword ptr [rsp + 0x48]
006AA6AE  mov      rbp, qword ptr [rsp + 0x50]
006AA6B3  mov      rsi, qword ptr [rsp + 0x58]
006AA6B8  add      rsp, 0x30
006AA6BC  pop      rdi
006AA6BD  ret      
```
