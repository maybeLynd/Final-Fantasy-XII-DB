# Homing pack: `99-Unresolved-Residual/the-nine-patch-window-frame.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-nine-patch-window-frame.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0028CF80 (165 B, extent 0028CF80-0028D025)

Entered from (direct sites whose caller this page cites): `0028BB50` + 0x2FE (call; `0028BB50` is cited on this page); `0028BB50` + 0x81C (call; `0028BB50` is cited on this page)
Other direct sites: none

Host context: "t_tag: GN162     basis: additive-annotation across GN161 -> GN162 - REPLACED 2026-09-21 (OPUS), because the snapshot-identity basis this block carried is FALSE at GN162: this document cites record(s) 0028BB50, which batch R30 touched. The weaker basis HOLDS and is measured: the advance changed 30 records in comment and tags ONLY - 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten (check_delta_additivity" / "t_tag: GN162     basis: additive-annotation across GN161 -> GN162 - REPLACED 2026-09-21 (OPUS), because the snapshot-identity basis this block carried is FALSE at GN162: this document cites record(s) 0028BB50, which batch R30 touched. The weaker basis HOLDS and is measured: the advance changed 30 records in comment and tags ONLY - 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten (check_delta_additivity"

```
0028CF80  push     rbx
0028CF82  sub      rsp, 0x40
0028CF86  cmp      dword ptr [rcx + 0xd50], 1
0028CF8D  mov      rbx, rcx
0028CF90  movaps   xmmword ptr [rsp + 0x20], xmm7
0028CF95  movaps   xmm7, xmm1
0028CF98  je       0x28cfc5  ; -> 0028CFC5
0028CF9A  movaps   xmm2, xmm1
0028CF9D  mov      edx, 6
0028CFA2  call     0x3f25d0  ; -> 003F25D0 fn
0028CFA7  lea      rcx, [rbx + 0x5d0]
0028CFAE  movaps   xmm2, xmm7
0028CFB1  mov      edx, 6
0028CFB6  movaps   xmm7, xmmword ptr [rsp + 0x20]
0028CFBB  add      rsp, 0x40
0028CFBF  pop      rbx
0028CFC0  jmp      0x3f25d0  ; -> 003F25D0 fn
0028CFC5  movzx    eax, word ptr [rcx + 0xd48]
0028CFCC  movss    xmm0, dword ptr [rip + 0x1a5eca4]  ; -> 01CEBC78 [f32 6.283185]
0028CFD4  add      eax, eax
0028CFD6  movaps   xmmword ptr [rsp + 0x30], xmm6
0028CFDB  movd     xmm1, eax
0028CFDF  cvtdq2ps xmm1, xmm1
0028CFE2  divss    xmm0, xmm1
0028CFE6  call     0x861f0e  ; -> 00861F0E fn
0028CFEB  movaps   xmm6, xmm0
0028CFEE  mov      edx, 6
0028CFF3  mulss    xmm6, xmm7
0028CFF7  mov      rcx, rbx
0028CFFA  movaps   xmm2, xmm6
0028CFFD  call     0x3f3050  ; -> 003F3050 fn
0028D002  lea      rcx, [rbx + 0x5d0]
0028D009  movaps   xmm2, xmm6
0028D00C  mov      edx, 6
0028D011  movaps   xmm6, xmmword ptr [rsp + 0x30]
0028D016  movaps   xmm7, xmmword ptr [rsp + 0x20]
0028D01B  add      rsp, 0x40
0028D01F  pop      rbx
0028D020  jmp      0x3f3050  ; -> 003F3050 fn
```

## 002A84F0 (88 B, extent 002A84F0-002A8548)

Entered from (direct sites whose caller this page cites): `002A6190` + 0x7A2 (call; `002A6190` is cited on this page)
Other direct sites: none

Host context: "/'0xC' lane, '[rcx + i] = [rdx + i] + ([r8 + i] - [rdx + i]) * xmm3' - the vec4 interpolate the frame arms share. Interior anchor '002754E9' (the first 'mulss').  '002A7720' (552 B) is the mode-step '002A6190' calls: '[rbx+0x3E8]' bits 8-10 dispatch 0/1/2, each arm requires '01E0CDC8' and '[rbx+0x80]' bits 0/1 clear, mode 1 rewrites the field '& 0xFFFFF8FF' and calls '002A3DF0(rbx, 0x50)' after copying '0209C988'->'0209C980', mode 2 doe"

```
002A84F0  sub      rsp, 0x28
002A84F4  test     dword ptr [rcx + 0x3e8], 0x1000
002A84FE  je       0x2a8543  ; -> 002A8543
002A8500  mov      qword ptr [rsp + 0x30], rbx
002A8505  lea      rbx, [rip + 0x1df470c]  ; -> 0209CC18
002A850C  mov      qword ptr [rsp + 0x38], rsi
002A8511  lea      rsi, [rip + 0x1df4718]  ; -> 0209CC30
002A8518  mov      qword ptr [rsp + 0x20], rdi
002A851D  xor      edi, edi
002A851F  nop      
002A8520  mov      rcx, qword ptr [rbx]
002A8523  call     0x245020  ; -> 00245020 fn
002A8528  mov      qword ptr [rbx], rdi
002A852B  add      rbx, 8
002A852F  cmp      rbx, rsi
002A8532  jl       0x2a8520  ; -> 002A8520
002A8534  mov      rdi, qword ptr [rsp + 0x20]
002A8539  mov      rsi, qword ptr [rsp + 0x38]
002A853E  mov      rbx, qword ptr [rsp + 0x30]
002A8543  add      rsp, 0x28
002A8547  ret      
```
