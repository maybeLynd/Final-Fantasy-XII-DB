# Homing pack: `12-Items-Equipment-Shops-License/the-bazaar-recipe-unlock-and-purchase.md`

Generated 2026-10-02 22:54 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-bazaar-recipe-unlock-and-purchase.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002ABAA0 (126 B, extent 002ABAA0-002ABB1E)

Entered from (direct sites whose caller this page cites): `0029CCD0` + 0xE (jmp; `0029CCD0` is cited on this page)
Other direct sites: none

Host context: " dword[rdi+8],1' marks the node, 'abs(ebx)' (cdq/xor/sub) becomes 'r9d', '0029FF60'/'0029FB50' run on 'rdi', 'dword[rdi+0x24] = r14d', then a '/10' loop ('imul 0x66666667') iterates 'ebx' times over '0029CCD0'/'0029CCF0'/'0020E620' - the per-item stage-commit behind the recipe purchase.  Interior anchor '002CC7EC' (function '002CC780').  '0029FB50' (126 B) is the record field commit '002CC780' (the purchase loop) runs: '(rec+8 <<0x10)>>"

```
002ABAA0  push     rbx
002ABAA2  sub      rsp, 0x20
002ABAA6  mov      ebx, ecx
002ABAA8  call     0x254a10  ; -> 00254A10 fn
002ABAAD  test     eax, eax
002ABAAF  jne      0x2abb03  ; -> 002ABB03
002ABAB1  call     0x229e40  ; -> 00229E40 fn
002ABAB6  cmp      eax, 7
002ABAB9  jne      0x2abae8  ; -> 002ABAE8
002ABABB  test     ebx, ebx
002ABABD  je       0x2abad6  ; -> 002ABAD6
002ABABF  call     0x24aba0  ; -> 0024ABA0 fn
002ABAC4  mulss    xmm0, dword ptr [rip + 0x66a848]  ; -> 00916314 [f32 15]
002ABACC  cvttss2si eax, xmm0
002ABAD0  add      rsp, 0x20
002ABAD4  pop      rbx
002ABAD5  ret      
002ABAD6  movss    xmm0, dword ptr [rip + 0x66a9a6]  ; -> 00916484 [f32 26]
002ABADE  cvttss2si eax, xmm0
002ABAE2  add      rsp, 0x20
002ABAE6  pop      rbx
002ABAE7  ret      
002ABAE8  call     0x24aba0  ; -> 0024ABA0 fn
002ABAED  test     ebx, ebx
002ABAEF  je       0x2abb0c  ; -> 002ABB0C
002ABAF1  mulss    xmm0, dword ptr [rip + 0x66a81b]  ; -> 00916314 [f32 15]
002ABAF9  cvttss2si eax, xmm0
002ABAFD  add      rsp, 0x20
002ABB01  pop      rbx
002ABB02  ret      
002ABB03  call     0x24aba0  ; -> 0024ABA0 fn
002ABB08  test     ebx, ebx
002ABB0A  jne      0x2abac4  ; -> 002ABAC4
002ABB0C  mulss    xmm0, dword ptr [rip + 0x64c66c]  ; -> 008F8180 [f32 10]
002ABB14  cvttss2si eax, xmm0
002ABB18  add      rsp, 0x20
002ABB1C  pop      rbx
002ABB1D  ret      
```
