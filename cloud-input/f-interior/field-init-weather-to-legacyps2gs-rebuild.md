# F-interior pack: `03-World-Area-Field/Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/field-init-weather-to-legacyps2gs-rebuild.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: c9b951983	EC7 pass-22 debt: crossing-section dispositions - 527 pairs / 65 pages (FRONTIER-REQ-SWE2-EC7-PASS22; inbox mentions: repos-2d.md, repos-78.md). OPUS read these before packing.

## 00180650 (108 B, extent 00180650-001806BC)

Page context: "025DF00', '003ECFD0', '003ED020' - shared machinery across the layer boundary, no shared ownership. - **Presentation - CLIENT (41 edges).** '001A9930' is also called by bodies filed to presentation: '00180650' (Rendering), '001ACF80' (Rendering), '001BF8B0' (Rendering) - shared machinery across the layer boundary, no shared ownership. - **Script_VM_Native_Bridge - CLIENT (7 edges).** '00265920', '0026D8F0', '0026D910' are also called by"

```
00180650  mov      qword ptr [rsp + 8], rbx
00180655  push     rdi
00180656  sub      rsp, 0x20
0018065A  mov      byte ptr [r8 + 0xc0], r9b
00180661  mov      rbx, r8
00180664  mov      edi, edx
00180666  test     ecx, ecx
00180668  je       0x18067e  ; -> 0018067E
0018066A  call     0x1a9930  ; -> 001A9930 fn
0018066F  mov      rcx, rax
00180672  mov      r8, rbx
00180675  mov      edx, edi
00180677  call     0x1a94c0  ; -> 001A94C0 fn
0018067C  jmp      0x180689  ; -> 00180689
0018067E  mov      rax, qword ptr [r8]
00180681  xor      edx, edx
00180683  mov      rcx, rbx
00180686  call     qword ptr [rax + 8]
00180689  mov      rcx, rbx
0018068C  call     0x1e3e80  ; -> 001E3E80 fn
00180691  test     al, al
00180693  je       0x1806b1  ; -> 001806B1
00180695  mov      rcx, rbx
00180698  call     0x1e3ff0  ; -> 001E3FF0 fn
0018069D  test     eax, eax
0018069F  jne      0x1806b1  ; -> 001806B1
001806A1  call     0x1a9930  ; -> 001A9930 fn
001806A6  mov      rcx, rax
001806A9  mov      rdx, rbx
001806AC  call     0x1a4fe0  ; -> 001A4FE0 fn
001806B1  mov      rbx, qword ptr [rsp + 0x30]
001806B6  add      rsp, 0x20
001806BA  pop      rdi
001806BB  ret      
```
