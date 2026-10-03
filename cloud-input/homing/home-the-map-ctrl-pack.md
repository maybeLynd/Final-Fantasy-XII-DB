# Homing pack: `03-World-Area-Field/Map-Pack/the-map-ctrl-pack.md`

Generated 2026-10-03 06:31 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-map-ctrl-pack.json`.

Bodies: 3. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001A5980 (239 B, extent 001A5980-001A5A6F)

Entered from (direct sites whose caller this page cites): `00180280` + 0x1A (jmp; `00180280` is cited on this page)
Other direct sites: none

Host context: "'-counted '0x40' rows releases '+0x14' through '003CD5D0' when '+0x04' is clear and '+0x30' the same way when '+0x10' reads 4, then '003EC8A0' frees both '02CA6010' and '02CA6018' and the tail jumps '00180280' - the full-table teardown the map pack runs on unload.  Interior anchor '0046810E' (function '004680D0').  ## Interior citations for the entry-cited functions (OPUS, 2026-10-01)  *The functions this page named only at their entry."

```
001A5980  push     rbp
001A5982  sub      rsp, 0x20
001A5986  mov      qword ptr [rsp + 0x30], rbx
001A598B  mov      rbp, rcx
001A598E  mov      rbx, qword ptr [rcx + 0x278]
001A5995  mov      qword ptr [rsp + 0x38], rsi
001A599A  mov      qword ptr [rsp + 0x40], rdi
001A599F  lea      rdi, [rcx + 0x270]
001A59A6  cmp      rbx, rdi
001A59A9  je       0x1a59d2  ; -> 001A59D2
001A59AB  nop      dword ptr [rax + rax]
001A59B0  mov      rcx, qword ptr [rbx + 0x28]
001A59B4  call     0x183720  ; -> 00183720 fn
001A59B9  mov      rcx, qword ptr [rbx + 0x30]
001A59BD  call     0x183720  ; -> 00183720 fn
001A59C2  mov      rcx, rbx
001A59C5  call     0x16d6d0  ; -> 0016D6D0 fn
001A59CA  mov      rbx, rax
001A59CD  cmp      rax, rdi
001A59D0  jne      0x1a59b0  ; -> 001A59B0
001A59D2  lea      rsi, [rbp + 0x268]
001A59D9  mov      rdi, qword ptr [rsi + 0x18]
001A59DD  test     rdi, rdi
001A59E0  je       0x1a5a20  ; -> 001A5A20
001A59E2  mov      qword ptr [rsp + 0x48], r14
001A59E7  nop      word ptr [rax + rax]
001A59F0  mov      rdx, qword ptr [rdi]
001A59F3  mov      rcx, rsi
001A59F6  call     0x1a48c0  ; -> 001A48C0 fn
001A59FB  mov      rax, qword ptr [rsi + 0x30]
001A59FF  lea      rcx, [rsi + 0x30]
001A5A03  mov      rbx, qword ptr [rdi + 8]
001A5A07  mov      r8d, 0x38
001A5A0D  mov      rdx, rdi
001A5A10  call     qword ptr [rax + 0x18]
001A5A13  mov      rdi, rbx
001A5A16  test     rbx, rbx
001A5A19  jne      0x1a59f0  ; -> 001A59F0
001A5A1B  mov      r14, qword ptr [rsp + 0x48]
001A5A20  mov      rdi, qword ptr [rsp + 0x40]
001A5A25  lea      rax, [rsi + 8]
001A5A29  mov      rbx, qword ptr [rsp + 0x30]
001A5A2E  mov      qword ptr [rsi + 0x10], rax
001A5A32  mov      qword ptr [rax], rax
001A5A35  xor      eax, eax
001A5A37  mov      qword ptr [rsi + 0x18], rax
001A5A3B  mov      byte ptr [rsi + 0x20], al
001A5A3E  mov      dword ptr [rsi + 0x28], eax
001A5A41  mov      rcx, qword ptr [rbp + 0x2a8]
001A5A48  mov      r8, qword ptr [rbp + 0x2a0]
001A5A4F  mov      rsi, qword ptr [rsp + 0x38]
001A5A54  sub      rcx, r8
001A5A57  sar      rcx, 5
001A5A5B  neg      rcx
001A5A5E  shl      rcx, 5
001A5A62  add      qword ptr [rbp + 0x2a8], rcx
001A5A69  add      rsp, 0x20
001A5A6D  pop      rbp
001A5A6E  ret      
```

## 001E6400 (128 B, extent 001E6400-001E6480)

Entered from (direct sites whose caller this page cites): `00180890` + 0x0 (jmp; `00180890` is cited on this page)
Other direct sites: none

Host context: "else small indices | | '+0x1D' | u8 | variant byte (dedupe key — '002F7380') | | '+0x1E'/'+0x1F' | u8,u8 | a byte pair — '002F4520' multiplies them ('byte[+0x1E]·byte[+0x1F]'), negates, 'cvtdq2ps' → '00180890' arg (float extent/divisor) | | '+0x20' | u64 | per-slot bitmask (≤16 effective bits; '00466CB0' arg) | | '+0x22'–'+0x2F' | — | zero in all 764,018 — dead-authored tail pad ('+0x28'/'+0x2C' explicitly verified 0, no reader in any c"

```
001E6400  mov      rax, qword ptr [rcx + 0x18]
001E6404  movaps   xmm0, xmm2
001E6407  cvtss2sd xmm0, xmm0
001E640B  mov      rdx, qword ptr [rax]
001E640E  mov      eax, dword ptr [rdx + 0x60]
001E6411  neg      eax
001E6413  mov      dword ptr [rcx + 0x1f4], 0
001E641D  mov      dword ptr [rcx + 0x1f8], 0x3f800000
001E6427  jne      0x1e6454  ; -> 001E6454
001E6429  xorps    xmm4, xmm4
001E642C  cvtss2sd xmm4, xmm1
001E6430  xorps    xmm1, xmm1
001E6433  mulsd    xmm4, qword ptr [rip + 0x1b0579d]  ; -> 01CEBBD8 [f64 0.5]
001E643B  cvtss2sd xmm1, xmm3
001E643F  subsd    xmm1, xmm0
001E6443  divsd    xmm4, xmm1
001E6447  cvtpd2ps xmm0, xmm4
001E644B  movss    dword ptr [rcx + 0x1f0], xmm0
001E6453  ret      
001E6454  xorps    xmm1, xmm1
001E6457  movd     xmm2, eax
001E645B  cvtdq2pd xmm2, xmm2
001E645F  cvtss2sd xmm1, xmm3
001E6463  mulsd    xmm2, qword ptr [rip + 0x1b0576d]  ; -> 01CEBBD8 [f64 0.5]
001E646B  subsd    xmm1, xmm0
001E646F  divsd    xmm2, xmm1
001E6473  cvtpd2ps xmm0, xmm2
001E6477  movss    dword ptr [rcx + 0x1f0], xmm0
001E647F  ret      
```

## 0060EC30 (71 B, extent 0060EC30-0060EC77)

Entered from (direct sites whose caller this page cites): `001E5540` + 0x55 (call; `001E5540` is cited on this page)
Other direct sites: none

Host context: "iod)' and subtracts it — leaving the **fractional remainder** — then injects it into the vec3 lanes by axis mask (1 → lane 2 only, 2 → lanes 1+3, 3 → all three) and calls '00180720' — a tail-jump to '001E5540', which stores lane 1 → the runtime entry's '+0x1FC' and lane 2 → '+0x200', then walks the entry's linked list ('[+0x18..+0x20)') calling '0060EC30(node, frameIndex)' — propagating the clamped frame to each linked sub-record. A sep"

```
0060EC30  mov      qword ptr [rsp + 8], rbx
0060EC35  mov      r10, qword ptr [rcx]
0060EC38  xor      eax, eax
0060EC3A  mov      ebx, edx
0060EC3C  mov      r11, rcx
0060EC3F  test     dword ptr [r10], 0x7fffffff
0060EC46  jbe      0x60ec71  ; -> 0060EC71
0060EC48  nop      dword ptr [rax + rax]
0060EC50  mov      rdx, qword ptr [r10 + 8]
0060EC54  lea      r9, [rax + rax*2]
0060EC58  shl      r9, 6
0060EC5C  inc      eax
0060EC5E  mov      dword ptr [r9 + rdx + 0x28], ebx
0060EC63  mov      r10, qword ptr [r11]
0060EC66  mov      ecx, dword ptr [r10]
0060EC69  btr      ecx, 0x1f
0060EC6D  cmp      eax, ecx
0060EC6F  jb       0x60ec50  ; -> 0060EC50
0060EC71  mov      rbx, qword ptr [rsp + 8]
0060EC76  ret      
```
