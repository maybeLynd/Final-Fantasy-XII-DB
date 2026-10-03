# Homing pack: `16-UI/Unlabelled-Panes/the-unlabelled-procedures.md`

Generated 2026-10-03 07:51 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-unlabelled-procedures.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00182BE0 (187 B, extent 00182BE0-00182C9B)

Entered from (direct sites whose caller this page cites): `00181D50` + 0x11 (call; `00181D50` is cited on this page); `00181D80` + 0x11 (call; `00181D80` is cited on this page)
Other direct sites: none

Host context: "of the call at + 0x21 and 'rdx' = that '+0x278' qword | Interior anchor '00181BDB'; Interior anchor '00181BE5'; Interior anchor '00181BEF'; Interior anchor '00181BF9'; Interior anchor '00181C01' | | '00181D50' | 43 B | '005701B0' + 0xAF | makes the call at '00181D50' + 0x11 with 'xmm0' and 'xmm1' both 1.0 ('01CEBBA8') and stores its result at qword '+0x270' of the object returned by the call at + 0x19 | Interior anchor '00181D56'; Inter" / " stores its result at qword '+0x270' of the object returned by the call at + 0x19 | Interior anchor '00181D56'; Interior anchor '00181D61'; Interior anchor '00181D69'; Interior anchor '00181D6E' | | '00181D80' | 43 B | '005701B0' + 0xB4 | makes the call at '00181D80' + 0x11 with 'xmm0' and 'xmm1' both 1.0 ('01CEBBA8') and stores its result at qword '+0x278' of the object returned by the call at + 0x19 | Interior anchor '00181D86'; Inter"

```
00182BE0  sub      rsp, 0x58
00182BE4  movaps   xmmword ptr [rsp + 0x40], xmm6
00182BE9  movaps   xmm6, xmm1
00182BEC  movaps   xmmword ptr [rsp + 0x30], xmm7
00182BF1  movaps   xmm7, xmm0
00182BF4  call     0x1b6c40  ; -> 001B6C40 fn
00182BF9  test     rax, rax
00182BFC  je       0x182c8a  ; -> 00182C8A
00182C02  call     0x189120  ; -> 00189120 fn
00182C07  test     rax, rax
00182C0A  je       0x182c8a  ; -> 00182C8A
00182C0C  call     0x189120  ; -> 00189120 fn
00182C11  mov      rcx, rax
00182C14  call     0x186aa0  ; -> 00186AA0 fn
00182C19  mov      eax, eax
00182C1B  xorps    xmm0, xmm0
00182C1E  cvtsi2ss xmm0, rax
00182C23  mulss    xmm0, xmm7
00182C27  cvttss2si eax, xmm0
00182C2B  mov      dword ptr [rsp + 0x20], eax
00182C2F  call     0x189120  ; -> 00189120 fn
00182C34  mov      rcx, rax
00182C37  call     0x186a90  ; -> 00186A90 fn
00182C3C  mov      eax, eax
00182C3E  xorps    xmm0, xmm0
00182C41  cvtsi2ss xmm0, rax
00182C46  mulss    xmm0, xmm6
00182C4A  cvttss2si eax, xmm0
00182C4E  mov      dword ptr [rsp + 0x24], eax
00182C52  lea      rax, [rip + 0x2b74827]  ; -> 02CF7480
00182C59  mov      qword ptr [rsp + 0x28], rax
00182C5E  movaps   xmm0, xmmword ptr [rsp + 0x20]
00182C63  movdqa   xmmword ptr [rsp + 0x20], xmm0
00182C69  call     0x1b6c40  ; -> 001B6C40 fn
00182C6E  mov      rcx, rax
00182C71  lea      rdx, [rsp + 0x20]
00182C76  call     0x1b66f0  ; -> 001B66F0 fn
00182C7B  movaps   xmm6, xmmword ptr [rsp + 0x40]
00182C80  movaps   xmm7, xmmword ptr [rsp + 0x30]
00182C85  add      rsp, 0x58
00182C89  ret      
00182C8A  movaps   xmm6, xmmword ptr [rsp + 0x40]
00182C8F  xor      eax, eax
00182C91  movaps   xmm7, xmmword ptr [rsp + 0x30]
00182C96  add      rsp, 0x58
00182C9A  ret      
```
