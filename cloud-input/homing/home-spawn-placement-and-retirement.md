# Homing pack: `05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-spawn-placement-and-retirement.json`.

Bodies: 3. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 004068B0 (432 B, extent 004068B0-00406A60)

Entered from (direct sites whose caller this page cites): `004061F0` + 0x291 (call; `004061F0` is cited on this page); `004061F0` + 0x2C1 (call; `004061F0` is cited on this page)
Other direct sites: none

Host context: "ord, a battle unit or a spawn global, so the placement on this page, made from the call signature, does not hold; returned to SWE2-FRONTIER's residual placement. Signature as first recorded (callers '004061F0'/'00406770'): '[rcx+0x48]'/'+0x130'/'+0x178', '[rbx+0x180..0x18C]'; '0035D460' context getter, '004076B0', '00248F40' x2, '00245020' |  ## 30. The '00582860' subtree — 9 exclusive members + one shared callee bound (SWE2-FRONTIER, f" / "ord, a battle unit or a spawn global, so the placement on this page, made from the call signature, does not hold; returned to SWE2-FRONTIER's residual placement. Signature as first recorded (callers '004061F0'/'00406770'): '[rcx+0x48]'/'+0x130'/'+0x178', '[rbx+0x180..0x18C]'; '0035D460' context getter, '004076B0', '00248F40' x2, '00245020' |  ## 30. The '00582860' subtree — 9 exclusive members + one shared callee bound (SWE2-FRONTIER, f"

```
004068B0  mov      qword ptr [rsp + 8], rbx
004068B5  mov      qword ptr [rsp + 0x10], rsi
004068BA  push     rdi
004068BB  sub      rsp, 0x20
004068BF  xor      esi, esi
004068C1  mov      edi, edx
004068C3  mov      rbx, rcx
004068C6  cmp      edx, dword ptr [rcx + 0x174]
004068CC  je       0x406a28  ; -> 00406A28
004068D2  cmp      dword ptr [rcx + 0x118], esi
004068D8  je       0x406927  ; -> 00406927
004068DA  mov      dword ptr [rcx + 0x118], esi
004068E0  mov      dword ptr [rcx + 0xe4], edx
004068E6  movzx    ecx, byte ptr [rcx + 0xc0]
004068ED  test     ecx, ecx
004068EF  je       0x40691f  ; -> 0040691F
004068F1  sub      ecx, 1
004068F4  je       0x406915  ; -> 00406915
004068F6  cmp      ecx, 2
004068F9  jne      0x406927  ; -> 00406927
004068FB  mov      eax, dword ptr [rbx + 0xe0]
00406901  cmp      edx, eax
00406903  jle      0x406907  ; -> 00406907
00406905  sub      edx, eax
00406907  mov      rcx, qword ptr [rbx + 0xd0]
0040690E  call     0x225580  ; -> 00225580 fn
00406913  jmp      0x406927  ; -> 00406927
00406915  mov      rcx, rbx
00406918  call     0x407720  ; -> 00407720 fn
0040691D  jmp      0x406927  ; -> 00406927
0040691F  mov      rcx, rbx
00406922  call     0x407450  ; -> 00407450 fn
00406927  and      dword ptr [rbx + 0x130], 0xffffffdf
0040692E  mov      r9d, 1
00406934  mov      eax, dword ptr [rbx + 0x130]
0040693A  test     al, 0x40
0040693C  je       0x406978  ; -> 00406978
0040693E  cmp      byte ptr [rbx + 0x136], sil
00406945  jne      0x406958  ; -> 00406958
00406947  mov      ecx, 0x28
0040694C  mov      word ptr [rbx + 0x178], cx
00406953  jmp      0x406a25  ; -> 00406A25
00406958  mov      eax, 8
0040695D  mov      word ptr [rbx + 0x178], ax
00406964  movzx    eax, byte ptr [rbx + 0x137]
0040696B  mov      byte ptr [rax + rbx + 0x13c], 0xa
00406973  jmp      0x406a25  ; -> 00406A25
00406978  test     al, al
0040697A  jns      0x4069c1  ; -> 004069C1
0040697C  cmp      byte ptr [rbx + 0x136], sil
00406983  jne      0x406999  ; -> 00406999
00406985  or       dword ptr [rbx + 0x130], 0x20
0040698C  mov      word ptr [rbx + 0x178], r9w
00406994  jmp      0x406a25  ; -> 00406A25
00406999  mov      eax, 8
0040699E  mov      word ptr [rbx + 0x178], ax
004069A5  movzx    eax, byte ptr [rbx + 0x137]
004069AC  dec      eax
004069AE  cdqe     
004069B0  mov      byte ptr [rax + rbx + 0x13c], r9b
004069B8  or       dword ptr [rbx + 0x130], 0x20
004069BF  jmp      0x406a25  ; -> 00406A25
004069C1  mov      r8d, dword ptr [rbx + 0x174]
004069C8  cmp      edi, r8d
004069CB  jge      0x406a07  ; -> 00406A07
004069CD  sub      r8d, edi
004069D0  mov      ecx, 0x28
004069D5  mov      eax, ecx
004069D7  cdq      
004069D8  idiv     r8d
004069DB  test     eax, eax
004069DD  cmovle   eax, r9d
004069E1  add      dword ptr [rbx + 0x17c], eax
004069E7  cmp      dword ptr [rbx + 0x17c], 0xfa0
004069F1  jl       0x40694c  ; -> 0040694C
004069F7  mov      word ptr [rbx + 0x178], r9w
004069FF  mov      dword ptr [rbx + 0x17c], esi
00406A05  jmp      0x406a25  ; -> 00406A25
00406A07  mov      word ptr [rbx + 0x178], r9w
00406A0F  cmp      edi, dword ptr [rbx + 0xe4]
00406A15  jg       0x406a1c  ; -> 00406A1C
00406A17  and      eax, 0xffffffdf
00406A1A  jmp      0x406a1f  ; -> 00406A1F
00406A1C  or       eax, 0x20
00406A1F  mov      dword ptr [rbx + 0x130], eax
00406A25  mov      esi, r9d
00406A28  mov      dword ptr [rbx + 0x174], edi
00406A2E  test     esi, esi
00406A30  je       0x406a50  ; -> 00406A50
00406A32  mov      edx, dword ptr [rbx + 0xe4]
00406A38  mov      eax, dword ptr [rbx + 0xe0]
00406A3E  cmp      edx, eax
00406A40  jle      0x406a44  ; -> 00406A44
00406A42  sub      edx, eax
00406A44  mov      rcx, qword ptr [rbx + 0xd0]
00406A4B  call     0x225580  ; -> 00225580 fn
00406A50  mov      rbx, qword ptr [rsp + 0x30]
00406A55  mov      rsi, qword ptr [rsp + 0x38]
00406A5A  add      rsp, 0x20
00406A5E  pop      rdi
00406A5F  ret      
```

## 00407240 (76 B, extent 00407240-0040728C)

Entered from (direct sites whose caller this page cites): `004061F0` + 0x362 (call; `004061F0` is cited on this page)
Other direct sites: none

Host context: "ord, a battle unit or a spawn global, so the placement on this page, made from the call signature, does not hold; returned to SWE2-FRONTIER's residual placement. Signature as first recorded (callers '004061F0'/'00406770'): '[rcx+0x48]'/'+0x130'/'+0x178', '[rbx+0x180..0x18C]'; '0035D460' context getter, '004076B0', '00248F40' x2, '00245020' |  ## 30. The '00582860' subtree — 9 exclusive members + one shared callee bound (SWE2-FRONTIER, f"

```
00407240  test     rcx, rcx
00407243  je       0x40728b  ; -> 0040728B
00407245  movsx    eax, word ptr [rcx + 0x108]
0040724C  xor      r9d, r9d
0040724F  mov      r8d, dword ptr [rcx + 0xe4]
00407256  sub      edx, r8d
00407259  mov      dword ptr [rcx + 0x120], edx
0040725F  test     eax, eax
00407261  mov      edx, 1
00407266  mov      dword ptr [rcx + 0x11c], r8d
0040726D  cmove    eax, edx
00407270  mov      dword ptr [rcx + 0x114], r9d
00407277  mov      dword ptr [rcx + 0x118], eax
0040727D  mov      dword ptr [rcx + 0x124], r8d
00407284  mov      dword ptr [rcx + 0x128], r9d
0040728B  ret      
```

## 00408140 (76 B, extent 00408140-0040818C)

Entered from (direct sites whose caller this page cites): `00406770` + 0xC1 (call; `00406770` is cited on this page)
Other direct sites: none

Host context: "le unit or a spawn global, so the placement on this page, made from the call signature, does not hold; returned to SWE2-FRONTIER's residual placement. Signature as first recorded (callers '004061F0'/'00406770'): '[rcx+0x48]'/'+0x130'/'+0x178', '[rbx+0x180..0x18C]'; '0035D460' context getter, '004076B0', '00248F40' x2, '00245020' |  ## 30. The '00582860' subtree — 9 exclusive members + one shared callee bound (SWE2-FRONTIER, followup que"

```
00408140  movzx    r8d, byte ptr [rcx + 0xc0]
00408148  mov      dword ptr [rcx + 0x118], 0
00408152  mov      dword ptr [rcx + 0xe4], edx
00408158  test     r8d, r8d
0040815B  je       0x408186  ; -> 00408186
0040815D  sub      r8d, 1
00408161  je       0x408181  ; -> 00408181
00408163  cmp      r8d, 2
00408167  jne      0x40818b  ; -> 0040818B
00408169  mov      eax, dword ptr [rcx + 0xe0]
0040816F  cmp      edx, eax
00408171  jle      0x408175  ; -> 00408175
00408173  sub      edx, eax
00408175  mov      rcx, qword ptr [rcx + 0xd0]
0040817C  jmp      0x225580  ; -> 00225580 fn
00408181  jmp      0x407720  ; -> 00407720 fn
00408186  jmp      0x407450  ; -> 00407450 fn
0040818B  ret      
```
