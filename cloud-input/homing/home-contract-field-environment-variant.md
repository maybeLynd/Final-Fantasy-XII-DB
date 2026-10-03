# Homing pack: `03-World-Area-Field/CONTRACT-field-environment-variant.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-contract-field-environment-variant.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 003B7130 (74 B, extent 003B7130-003B717A)

Entered from (direct sites whose caller this page cites): `0025D9E0` + 0x3E8 (call; `0025D9E0` is cited on this page)
Other direct sites: `00349C50` + 0x2D (jmp)

Host context: "rship.  *Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*  **ActorEntity — CLIENT, MECHANICAL (3 edges).** 'ActorManager_RunFieldRuntimePass' ('0025D9E0'), the area unload path '002628B0' and 'ActorManager_BindLoadedDefinitionPayload' ('0026C8C0') call 'SaveImage_GetPersistentPayloadBase' ('002EF2B0'), the 20-byte getter that returns the constant '02164280' plus '0x200' and through"

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
