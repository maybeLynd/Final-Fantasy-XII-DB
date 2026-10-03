# Homing pack: `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/how-the-bigfile-index-loads-and-is-verified.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-how-the-bigfile-index-loads-and-is-verified.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002150B0 (26 B, extent 002150B0-002150CA)

Entered from (direct sites whose caller this page cites): `001F4250` + 0x67 (call; `001F4250` is cited on this page); `001F4250` + 0xC3 (call; `001F4250` is cited on this page)
Other direct sites: none

Host context: "de '{links, key +0x18/+0x20, record +0x28}', signed two-half order | §3a | | '0019AEE0' → '001F47D0' | MD5 of the caller's path, then the digest-tree lookup across the mounted archives | §3a, §7 | | '001F4250' | takes a free reader handle for the record (or makes a sixteenth) | §7 | | '00214FC0' / '00215290' / '00215110' | reader handle: construct (64 KiB cache), 'fopen' the archive, read clamped to the record's size | §3a, §7 | | '0019" / "de '{links, key +0x18/+0x20, record +0x28}', signed two-half order | §3a | | '0019AEE0' → '001F47D0' | MD5 of the caller's path, then the digest-tree lookup across the mounted archives | §3a, §7 | | '001F4250' | takes a free reader handle for the record (or makes a sixteenth) | §7 | | '00214FC0' / '00215290' / '00215110' | reader handle: construct (64 KiB cache), 'fopen' the archive, read clamped to the record's size | §3a, §7 | | '0019"

```
002150B0  mov      rax, qword ptr [rcx + 0x28]
002150B4  mov      qword ptr [rcx + 0x18], rdx
002150B8  xor      edx, edx
002150BA  mov      qword ptr [rcx + 0x20], rdx
002150BE  mov      qword ptr [rax + 0x10], rdx
002150C2  mov      qword ptr [rax + 8], rdx
002150C6  mov      byte ptr [rcx], 1
002150C9  ret      
```
