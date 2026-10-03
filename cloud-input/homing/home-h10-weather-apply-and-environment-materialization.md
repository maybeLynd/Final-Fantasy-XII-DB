# Homing pack: `03-World-Area-Field/Weather/weather-apply-and-environment-materialization.md`

Generated 2026-10-03 12:18 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h10-weather-apply-and-environment-materialization.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 003B7130 (74 B, extent 003B7130-003B717A)

Entered from (direct sites whose caller this page cites): `0025D9E0` + 0x3E8 (call; `0025D9E0` is cited on this page)
Other direct sites: `00349C50` + 0x2D (jmp)

Host context: "ion by reference to it rather than repeating it — duplicating a census in six files is how one rots.   **ActorEntity — SERVICE (SWE2-EC7-156, 43 edges).** This page's '0022A0B0' calls '002368D0' and '0025D9E0' calls '0025B250'/'0025B600'/'0025B82x' of that layer — the weather frame consumes actor helpers, not a shared responsibility. **CoreRuntimeScheduling — CLIENT and SERVICE (SWE2-EC7-156, 11 edges).** '0022A0B0' calls '0022BDF0' and"

```
003B7130  push     rbx
003B7132  sub      rsp, 0x20
003B7136  mov      ebx, ecx
003B7138  test     edx, edx
003B713A  je       0x3b7170  ; -> 003B7170
003B713C  cmp      ecx, 1
003B713F  je       0x3b7148  ; -> 003B7148
003B7141  call     0x313590  ; -> 00313590 fn
003B7146  jmp      0x3b7152  ; -> 003B7152
003B7148  mov      ecx, 1
003B714D  call     0x32a060  ; -> 0032A060 fn
003B7152  mov      ecx, eax
003B7154  call     0x3588b0  ; -> 003588B0 fn
003B7159  test     rax, rax
003B715C  jne      0x3b7161  ; -> 003B7161
003B715E  or       ebx, 0xffffffff
003B7161  mov      edx, ebx
003B7163  mov      rcx, rax
003B7166  add      rsp, 0x20
003B716A  pop      rbx
003B716B  jmp      0x2ea9d0  ; -> 002EA9D0 fn
003B7170  add      rsp, 0x20
003B7174  pop      rbx
003B7175  jmp      0x2eaa30  ; -> 002EAA30 fn
```
