# Homing pack: `02-Resource-And-Asset-Pipeline/the-resource-owner-from-copy-or-borrow-to-disposal.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-resource-owner-from-copy-or-borrow-to-disposal.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 003EE260 (101 B, extent 003EE260-003EE2C5)

Entered from (direct sites whose caller this page cites): `003EE2D0` + 0x90 (jmp; `003EE2D0` is cited on this page)
Other direct sites: none

Host context: "nempty specialized registration and whole concurrent/reentrant consumer lifetimes remain open. [SECTION-08 review](../_experiments/evidence/continuation-section08-external-source-owners/REVIEW.md).  '003EE2D0' (219 B) is the four-way record dispatch '003EDAD0' runs on '[rcx] - 0x100': every arm first publishes '+4' (s32) to '02EBB738'; kind '3' clears '02096B40'/'02096BA4' and tails '0016D680(rcx+8)' when '+2 == 0x4000'; kind '2' '0024E"

```
003EE260  sub      rsp, 0x28
003EE264  movzx    edx, word ptr [rcx + 2]
003EE268  lea      rax, [rcx + 8]
003EE26C  cmp      edx, 0x540
003EE272  je       0x3ee2a6  ; -> 003EE2A6
003EE274  cmp      edx, 0xb00
003EE27A  je       0x3ee291  ; -> 003EE291
003EE27C  cmp      edx, 0x3000
003EE282  jne      0x3ee2c0  ; -> 003EE2C0
003EE284  mov      rcx, rax
003EE287  call     0x16d680  ; -> 0016D680 fn
003EE28C  add      rsp, 0x28
003EE290  ret      
003EE291  mov      ecx, 2
003EE296  mov      word ptr [rax], cx
003EE299  mov      rcx, rax
003EE29C  call     0x3aa470  ; -> 003AA470 fn
003EE2A1  add      rsp, 0x28
003EE2A5  ret      
003EE2A6  mov      eax, dword ptr [rax]
003EE2A8  mov      ecx, 2
003EE2AD  mov      dword ptr [rsp + 0x30], eax
003EE2B1  mov      word ptr [rsp + 0x30], cx
003EE2B6  lea      rcx, [rsp + 0x30]
003EE2BB  call     0x3a9e00  ; -> 003A9E00 fn
003EE2C0  add      rsp, 0x28
003EE2C4  ret      
```
