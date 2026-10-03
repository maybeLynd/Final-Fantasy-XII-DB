# Homing pack: `16-UI/Unlabelled-Panes/the-unlabelled-procedures.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-the-unlabelled-procedures.json`.

Bodies: 4. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00181BD0 (60 B, extent 00181BD0-00181C0C)

Entered from (direct sites whose caller this page cites): `005701B0` + 0x1A0 (call; `005701B0` is cited on this page)
Other direct sites: none

Host context: "which selections each 0056EF60 kind sets are not established; the 0xC0368C / 0xC036A4 contents decoded 2026-09-18" evidence_tier: 1 tags: [ui, menu-screens, unlabelled] addresses:   - "00560910"   - "005701B0"   - "00571A50"   - "005742D0"   - "005789D0"   - "00579420"   - "00579AF0" verified_against:   gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708   snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36"

```
00181BD0  push     rbx
00181BD2  sub      rsp, 0x20
00181BD6  call     0x1eba40  ; -> 001EBA40 fn
00181BDB  mov      rbx, qword ptr [rax + 0x278]
00181BE2  test     rbx, rbx
00181BE5  je       0x181c06  ; -> 00181C06
00181BE7  call     0x1b6c40  ; -> 001B6C40 fn
00181BEC  test     rax, rax
00181BEF  je       0x181c06  ; -> 00181C06
00181BF1  call     0x1b6c40  ; -> 001B6C40 fn
00181BF6  mov      rcx, rax
00181BF9  mov      rdx, rbx
00181BFC  add      rsp, 0x20
00181C00  pop      rbx
00181C01  jmp      0x1b68d0  ; -> 001B68D0 fn
00181C06  add      rsp, 0x20
00181C0A  pop      rbx
00181C0B  ret      
```

## 00181D50 (43 B, extent 00181D50-00181D7B)

Entered from (direct sites whose caller this page cites): `005701B0` + 0xAF (call; `005701B0` is cited on this page)
Other direct sites: none

Host context: "which selections each 0056EF60 kind sets are not established; the 0xC0368C / 0xC036A4 contents decoded 2026-09-18" evidence_tier: 1 tags: [ui, menu-screens, unlabelled] addresses:   - "00560910"   - "005701B0"   - "00571A50"   - "005742D0"   - "005789D0"   - "00579420"   - "00579AF0" verified_against:   gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708   snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36"

```
00181D50  push     rbx
00181D52  sub      rsp, 0x20
00181D56  movss    xmm0, dword ptr [rip + 0x1b69e4a]  ; -> 01CEBBA8 [f32 1]
00181D5E  movaps   xmm1, xmm0
00181D61  call     0x182be0  ; -> 00182BE0 fn
00181D66  mov      rbx, rax
00181D69  call     0x1eba40  ; -> 001EBA40 fn
00181D6E  mov      qword ptr [rax + 0x270], rbx
00181D75  add      rsp, 0x20
00181D79  pop      rbx
00181D7A  ret      
```

## 00181D80 (43 B, extent 00181D80-00181DAB)

Entered from (direct sites whose caller this page cites): `005701B0` + 0xB4 (call; `005701B0` is cited on this page)
Other direct sites: none

Host context: "which selections each 0056EF60 kind sets are not established; the 0xC0368C / 0xC036A4 contents decoded 2026-09-18" evidence_tier: 1 tags: [ui, menu-screens, unlabelled] addresses:   - "00560910"   - "005701B0"   - "00571A50"   - "005742D0"   - "005789D0"   - "00579420"   - "00579AF0" verified_against:   gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708   snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36"

```
00181D80  push     rbx
00181D82  sub      rsp, 0x20
00181D86  movss    xmm0, dword ptr [rip + 0x1b69e1a]  ; -> 01CEBBA8 [f32 1]
00181D8E  movaps   xmm1, xmm0
00181D91  call     0x182be0  ; -> 00182BE0 fn
00181D96  mov      rbx, rax
00181D99  call     0x1eba40  ; -> 001EBA40 fn
00181D9E  mov      qword ptr [rax + 0x278], rbx
00181DA5  add      rsp, 0x20
00181DA9  pop      rbx
00181DAA  ret      
```

## 0056FEA0 (68 B, extent 0056FEA0-0056FEE4)

Entered from (direct sites whose caller this page cites): `005701B0` + 0x189 (call; `005701B0` is cited on this page)
Other direct sites: none

Host context: "which selections each 0056EF60 kind sets are not established; the 0xC0368C / 0xC036A4 contents decoded 2026-09-18" evidence_tier: 1 tags: [ui, menu-screens, unlabelled] addresses:   - "00560910"   - "005701B0"   - "00571A50"   - "005742D0"   - "005789D0"   - "00579420"   - "00579AF0" verified_against:   gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708   snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36"

```
0056FEA0  push     rbx
0056FEA2  sub      rsp, 0x20
0056FEA6  mov      rbx, rcx
0056FEA9  mov      rcx, qword ptr [rcx + 0xc0]
0056FEB0  call     0x577a00  ; -> 00577A00 fn
0056FEB5  mov      rcx, qword ptr [rbx + 0x140]
0056FEBC  test     rcx, rcx
0056FEBF  je       0x56fec6  ; -> 0056FEC6
0056FEC1  call     0x244f00  ; -> 00244F00 fn
0056FEC6  mov      rcx, qword ptr [rbx + 0x150]
0056FECD  test     rcx, rcx
0056FED0  je       0x56fed7  ; -> 0056FED7
0056FED2  call     0x244f00  ; -> 00244F00 fn
0056FED7  mov      rcx, rbx
0056FEDA  add      rsp, 0x20
0056FEDE  pop      rbx
0056FEDF  jmp      0x244f00  ; -> 00244F00 fn
```
