# Homing pack: `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/how-a-path-is-resolved-to-bytes.md`

Generated 2026-10-03 12:18 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h10-how-a-path-is-resolved-to-bytes.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 001D6BB0 (44 B, extent 001D6BB0-001D6BDC)

Entered from (direct sites whose caller this page cites): `0059A9B0` + 0x1F (call; `0059A9B0` is cited on this page)
Other direct sites: none

Host context: "ommit carries whatever '+0x28' holds.** - On an armed commit the resolver loads the dword at frame '+0x28' ('0059EE90' + 0x320). The arm requires that the   lookup has already missed. - The backfill '0059A9B0' keeps that dword in 'esi' ('0059A9B0' + 0x13) and passes it as the key to the insertion   entry '001D6A20' ('0059A9B0' + 0xF4; section 5a). - The resolver writes nothing at '+0x28' itself. - The backfill inserts only when its firs"

```
001D6BB0  mov      qword ptr [rsp + 8], rbx
001D6BB5  push     rdi
001D6BB6  sub      rsp, 0x20
001D6BBA  movzx    ebx, dl
001D6BBD  mov      edi, ecx
001D6BBF  call     0x20c700  ; -> 0020C700 fn
001D6BC4  mov      rcx, rax
001D6BC7  movzx    r8d, bl
001D6BCB  mov      edx, edi
001D6BCD  mov      rbx, qword ptr [rsp + 0x30]
001D6BD2  add      rsp, 0x20
001D6BD6  pop      rdi
001D6BD7  jmp      0x20bfa0  ; -> 0020BFA0 fn
```

## 00217A60 (15 B, extent 00217A60-00217A6F)

Entered from (direct sites whose caller this page cites): `0020B680` + 0x191 (call; `0020B680` is cited on this page); `0020C300` + 0x11B (call; `0020C300` is cited on this page)
Other direct sites: none

Host context: "a different interface, and nothing on it applies that domain:  - **'001D6A20' takes the key ready-made.** The key arrives in 'ecx' as a 32-bit number, is held in 'ebp' and is   passed on in 'edx' to '0020B680', beside a data pointer ('rdx'), a 32-bit size/value ('r8d') and a 32-bit kind   ('r9d'). There is no hash, prefix scan or bit-31 clear on that path; a key with bit 31 set would pass through   unchanged, where the section 5 produce" / "ess everywhere downstream.**  **What a hit does before it allocates.** Having found the entry, '0020C1B0' writes the entry's size through the caller's size pointer ('0020C1B0' + 0xDC). It then calls '0020C300' ('0020C1B0' + 0xF8), passing the selector and the entry's kind dword '+0x14', while still holding its lock. '0020C300' does four things: - It increments the manager's dword '+0x88' ('0020C300' + 0x28). - It increments the entry's "

```
00217A60  mov      dword ptr [rcx + 8], r8d
00217A64  mov      rax, rcx
00217A67  mov      dword ptr [rcx + 0xc], r9d
00217A6B  mov      qword ptr [rcx], rdx
00217A6E  ret      
```
