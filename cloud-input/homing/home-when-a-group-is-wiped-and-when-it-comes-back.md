# Homing pack: `05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-when-a-group-is-wiped-and-when-it-comes-back.json`.

Bodies: 5. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002739B0 (31 B, extent 002739B0-002739CF)

Entered from (direct sites whose caller this page cites): `003C8B70` + 0x3CF (call; `003C8B70` is cited on this page)
Other direct sites: none

Host context: "F0'/'0028F5B0' ×2); bits **7, 11, 12, 20** reach no direct test at any of the 29 sites — they     are visible only to the callers that test the aggregate against a mask of their own     ('00252B60', '003C8B70'), which is the residue. (Interior read 2026-09-17, SWE2-FRONTIER:     '003C8B70' is a thrice-repeated eight-call sequence — '00249C60' sound-play wrapper →     '0035D060' → '002470C0' → '0035C080' → '0028FFE0' → '00252D90' → '002E"

```
002739B0  sub      rsp, 0x28
002739B4  call     0x3588b0  ; -> 003588B0 fn
002739B9  test     rax, rax
002739BC  jne      0x2739c3  ; -> 002739C3
002739BE  add      rsp, 0x28
002739C2  ret      
002739C3  mov      rcx, rax
002739C6  add      rsp, 0x28
002739CA  jmp      0x2675c0  ; -> 002675C0 fn
```

## 0028FE40 (89 B, extent 0028FE40-0028FE99)

Entered from (direct sites whose caller this page cites): `0035C150` + 0x0 (jmp; `0035C150` is cited on this page)
Other direct sites: none

Host context: "2026-09-17, SWE2-FRONTIER:     '003C8B70' is a thrice-repeated eight-call sequence — '00249C60' sound-play wrapper →     '0035D060' → '002470C0' → '0035C080' → '0028FFE0' → '00252D90' → '002E1CA0' → '0035C150',     first block at ['003C8C42'](../../_index/ADDRESS-INDEX.md) — consistent with a per-member     announce/state pass; '003C9250' ×4 frame it.) (The direct tests at the 29 sites are bits 0 —     the three UI-request mailbox funct"

```
0028FE40  mov      qword ptr [rsp + 8], rbx
0028FE45  push     rdi
0028FE46  sub      rsp, 0x20
0028FE4A  mov      edi, ecx
0028FE4C  mov      ebx, edx
0028FE4E  mov      rcx, qword ptr [rip + 0x1e0c02b]  ; -> 0209BE80
0028FE55  test     rcx, rcx
0028FE58  jne      0x28fe67  ; -> 0028FE67
0028FE5A  xor      eax, eax
0028FE5C  mov      rbx, qword ptr [rsp + 0x30]
0028FE61  add      rsp, 0x20
0028FE65  pop      rdi
0028FE66  ret      
0028FE67  add      rcx, 0x8fa0
0028FE6E  call     0x2be020  ; -> 002BE020 fn
0028FE73  mov      rcx, qword ptr [rip + 0x1e0c006]  ; -> 0209BE80
0028FE7A  or       r9d, 0xffffffff
0028FE7E  add      rcx, 0x8fa0
0028FE85  mov      r8d, ebx
0028FE88  mov      edx, edi
0028FE8A  mov      rbx, qword ptr [rsp + 0x30]
0028FE8F  add      rsp, 0x20
0028FE93  pop      rdi
0028FE94  jmp      0x2be1a0  ; -> 002BE1A0 fn
```

## 002FB250 (71 B, extent 002FB250-002FB297)

Entered from (direct sites whose caller this page cites): `00319B10` + 0x17E (jmp; `00319B10` is cited on this page)
Other direct sites: none

Host context: "'002ED570' - shared machinery across the layer boundary, no shared ownership. - **Rewards_Progression_Economy - SERVICE (2 edges).** '002342F0', '00234590' reach bodies filed to rewards/progression: '00319B10', '00319600' - shared machinery across the layer boundary, no shared ownership. - **SaveLoad - CLIENT (1 edge).** '00252D90' is also called by bodies filed to SaveLoad (save/load settings): '00280140' (RuntimeLifecycleSupport) - sh"

```
002FB250  mov      byte ptr [rip + 0x1fc3599], 0  ; -> 022BE7F0
002FB257  mov      byte ptr [rip + 0x1fc35b2], 0  ; -> 022BE810
002FB25E  mov      byte ptr [rip + 0x1fc35cb], 0  ; -> 022BE830
002FB265  mov      byte ptr [rip + 0x1fc35e4], 0  ; -> 022BE850
002FB26C  mov      byte ptr [rip + 0x1fc35fd], 0  ; -> 022BE870
002FB273  mov      byte ptr [rip + 0x1fc3616], 0  ; -> 022BE890
002FB27A  mov      byte ptr [rip + 0x1fc362f], 0  ; -> 022BE8B0
002FB281  mov      byte ptr [rip + 0x1fc3648], 0  ; -> 022BE8D0
002FB288  mov      byte ptr [rip + 0x1fc3661], 0  ; -> 022BE8F0
002FB28F  mov      byte ptr [rip + 0x1fc367a], 0  ; -> 022BE910
002FB296  ret      
```

## 00363B00 (31 B, extent 00363B00-00363B1F)

Entered from (direct sites whose caller this page cites): `0026C5D0` + 0x174 (call; `0026C5D0` is cited on this page)
Other direct sites: `00340EF0` + 0x6D (call); `00341400` + 0x7 (jmp); `00341780` + 0x8 (jmp); `005701B0` + 0xA1 (call); `005701B0` + 0x1B1 (call)

Host context: "lay-Capability-Policy/capability-inhibition-policy.md) documents rows 1 and 2 only) and what message '0x30B' is to '002E7C10' are not established here ('EE-7', 'EE-8'). All three have other callers ('0026C5D0'; '00359A30', '0035A6F0', '0035AB20'), so they are shared event-lock primitives, not group-specific.  ## 5b. From the script that names a group to the script that wakes when it dies *(synthesis, 2026-09-18, FABLE)*  *No new reading"

```
00363B00  mov      byte ptr [rip + 0x1f67f94], cl  ; -> 022CBA9A
00363B06  cmp      ecx, 1
00363B09  jne      0x363b1e  ; -> 00363B1E
00363B0B  movaps   xmm0, xmmword ptr [rdx]
00363B0E  movdqa   xmmword ptr [rip + 0x1f67ffa], xmm0  ; -> 022CBB10
00363B16  movss    dword ptr [rip + 0x1f67f8e], xmm2  ; -> 022CBAAC
00363B1E  ret      
```

## 003C94A0 (71 B, extent 003C94A0-003C94E7)

Entered from (direct sites whose caller this page cites): `003C8B70` + 0x54B (call; `003C8B70` is cited on this page)
Other direct sites: none

Host context: "F0'/'0028F5B0' ×2); bits **7, 11, 12, 20** reach no direct test at any of the 29 sites — they     are visible only to the callers that test the aggregate against a mask of their own     ('00252B60', '003C8B70'), which is the residue. (Interior read 2026-09-17, SWE2-FRONTIER:     '003C8B70' is a thrice-repeated eight-call sequence — '00249C60' sound-play wrapper →     '0035D060' → '002470C0' → '0035C080' → '0028FFE0' → '00252D90' → '002E"

```
003C94A0  sub      rsp, 0x28
003C94A4  call     0x35baf0  ; -> 0035BAF0 fn
003C94A9  test     rax, rax
003C94AC  je       0x3c94be  ; -> 003C94BE
003C94AE  test     dword ptr [rax], 0x8000
003C94B4  jne      0x3c94e2  ; -> 003C94E2
003C94B6  mov      ecx, dword ptr [rax + 8]
003C94B9  cmp      dword ptr [rax + 4], ecx
003C94BC  jne      0x3c94d9  ; -> 003C94D9
003C94BE  mov      rax, qword ptr [rip + 0x277e26b]  ; -> 02B47730
003C94C5  test     rax, rax
003C94C8  je       0x3c94e2  ; -> 003C94E2
003C94CA  mov      dword ptr [rax + 0xc8], 0
003C94D4  add      rsp, 0x28
003C94D8  ret      
003C94D9  add      rsp, 0x28
003C94DD  jmp      0x3c93e0  ; -> 003C93E0 fn
003C94E2  add      rsp, 0x28
003C94E6  ret      
```
