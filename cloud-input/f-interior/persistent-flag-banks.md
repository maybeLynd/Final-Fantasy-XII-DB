# F-interior pack: `14-Story-Event-Quest-Hunt/persistent-flag-banks.md`

Generated 2026-10-02 20:18 by FABLE (fable_fpack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md` (FABLE verifies instead of OPUS). Write your result to `cloud-reports/f-interior/persistent-flag-banks.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

## 003EC6C0 (59 B, extent 003EC6C0-003EC6FB)

Page context: "02EC3EA0'** (count '02EC3EC8', write index '02EC3EC4', rotated '% 3', '002FA878'–'002FA8F7'), > which is what the trigger walk looks up by field id. **'settrapshowstatus'** ('0x0547', > '00355E00' → '003EC6C0') shows or hides the sixteen marker slots '003EB720' indexes. > > **Who can spring one, and who is hit.** The trigger walk refuses a unit whose stats flags carry > bit 26 or whose **effect id 37 — *"Move safely past traps"*** ('lis"

```
003EC6C0  push     rdi
003EC6C2  sub      rsp, 0x20
003EC6C6  mov      edi, ecx
003EC6C8  call     0x377c20  ; -> 00377C20 fn
003EC6CD  test     eax, eax
003EC6CF  jne      0x3ec6f5  ; -> 003EC6F5
003EC6D1  mov      qword ptr [rsp + 0x30], rbx
003EC6D6  xor      ebx, ebx
003EC6D8  mov      ecx, ebx
003EC6DA  call     0x3eb720  ; -> 003EB720 fn
003EC6DF  mov      edx, edi
003EC6E1  mov      rcx, rax
003EC6E4  call     0x2ed3a0  ; -> 002ED3A0 fn
003EC6E9  inc      ebx
003EC6EB  cmp      ebx, 0x10
003EC6EE  jl       0x3ec6d8  ; -> 003EC6D8
003EC6F0  mov      rbx, qword ptr [rsp + 0x30]
003EC6F5  add      rsp, 0x20
003EC6F9  pop      rdi
003EC6FA  ret      
```
