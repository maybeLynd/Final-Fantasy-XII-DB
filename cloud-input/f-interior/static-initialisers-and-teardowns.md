# F-interior pack: `24-Compiler-And-CRT-Runtime/Static-Initialization-And-Teardown/static-initialisers-and-teardowns.md`

Generated 2026-10-02 18:41 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/static-initialisers-and-teardowns.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

## 00865550 (7 B, extent 00865550-00865557)

Page context: "026-09-21) - '00865660' measured  '00865660' (73 B) is the '02EB3860' singleton teardown '007980A0' runs: when the global is live the object's vtable relatches to '01CCFBC0' (RTTI '01D496F0', slot 0 '00865550'), a set bit 0 of 'byte[+8]' runs the IAT import '008C3178' ('01CCBFFE') on it, the 0x20 block goes back through '00809950', and the global zeroes - the destruct-and-detach order a static object's teardown needs. Interior anchor '0"

```
00865550  mov      rax, qword ptr [rcx]
00865553  jmp      qword ptr [rax + 8]
```
