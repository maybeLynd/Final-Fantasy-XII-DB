# F-interior pack: `00-Engine-Core-Runtime/Battle-Runtime-Mode/CONTRACT-battle-runtime-mode.md`

Generated 2026-10-02 20:34 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/contract-battle-runtime-mode.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: de4492e21	SWE2-CONTRACT: pass-22 debt final - six-folder worklist (597 pairs) fully dispositioned, 0 live find; f9017b106	SWE2-CONTRACT: repair 807950d2a - restore 18 committed pass-22 section headings it renamed). OPUS read these before packing.

## 00361170 (120 B, extent 00361170-003611E8)

Page context: "k' (00314020) call Audio bodies '0036F460', '00360D30', '002DEE50'). Substantive edges include '0022A770' calls '0036F460'; '00261F90' calls '00360D30'; '00261F90' calls '002DEE50'; '00261F90' calls '00361170'; the remaining edges run through shared helpers the page cites. - **Input — CLIENT and SERVICE (51 edges).** 7 inbound (Input bodies 'InputGameplay_ArbitrateDigitalInputAndModalState' (00253C70), '002E09A0', '00226BE0' call page-c"

```
00361170  mov      qword ptr [rsp + 8], rbx
00361175  mov      qword ptr [rsp + 0x10], rsi
0036117A  push     rdi
0036117B  sub      rsp, 0x20
0036117F  mov      esi, r8d
00361182  mov      ebx, edx
00361184  mov      edi, ecx
00361186  call     0x184950  ; -> 00184950 fn
0036118B  mov      r9d, eax
0036118E  mov      eax, ebx
00361190  cdq      
00361191  idiv     r9d
00361194  lea      ebx, [rax + 1]
00361197  test     edi, edi
00361199  js       0x3611d8  ; -> 003611D8
0036119B  call     0x2f16b0  ; -> 002F16B0 fn
003611A0  test     rax, rax
003611A3  je       0x3611d8  ; -> 003611D8
003611A5  lea      rcx, [rip - 0x12c]  ; -> 00361080
003611AC  mov      dword ptr [rax + 0x1c], 0x10001
003611B3  xor      edx, edx
003611B5  mov      qword ptr [rax + 8], rcx
003611B9  mov      ecx, edi
003611BB  mov      qword ptr [rax + 0x10], rdx
003611BF  mov      dword ptr [rax + 4], ebx
003611C2  mov      dword ptr [rax + 0x28], edi
003611C5  mov      dword ptr [rax + 0x30], esi
003611C8  mov      dword ptr [rax], edx
003611CA  call     0x361030  ; -> 00361030 fn
003611CF  test     rax, rax
003611D2  je       0x3611d8  ; -> 003611D8
003611D4  or       byte ptr [rax + 2], 2
003611D8  mov      rbx, qword ptr [rsp + 0x30]
003611DD  mov      rsi, qword ptr [rsp + 0x38]
003611E2  add      rsp, 0x20
003611E6  pop      rdi
003611E7  ret      
```
