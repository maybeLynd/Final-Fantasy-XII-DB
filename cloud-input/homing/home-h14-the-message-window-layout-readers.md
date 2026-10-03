# Homing pack: `16-UI/Message-Windows/the-message-window-layout-readers.md`

Generated 2026-10-03 15:23 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h14-the-message-window-layout-readers.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 002A84F0 (88 B, extent 002A84F0-002A8548)

Entered from (direct sites whose caller this page cites): `002A6190` + 0x7A2 (call; `002A6190` is cited on this page)
Other direct sites: none

Host context: "6-09-14   last_pass_state: OPUS-eleven-of-twelve-instructions-exact-one-address-off-by-four-installations-censused   last_pass_kind: attack   crossref_clean: false   reopened_count: 0 addresses:   - "002A6190"   - "002A86A0"   - "002A3960"   - "002BE4F0"   - "002BF690"   - "002D66D0"   - "0035E070" ---  # The message-window layout-key readers  **Status:** ~~PARTIAL~~ DOCUMENTED *(corrected 2026-10-02, OPUS: the front matter says 'status"

```
002A84F0  sub      rsp, 0x28
002A84F4  test     dword ptr [rcx + 0x3e8], 0x1000
002A84FE  je       0x2a8543  ; -> 002A8543
002A8500  mov      qword ptr [rsp + 0x30], rbx
002A8505  lea      rbx, [rip + 0x1df470c]  ; -> 0209CC18
002A850C  mov      qword ptr [rsp + 0x38], rsi
002A8511  lea      rsi, [rip + 0x1df4718]  ; -> 0209CC30
002A8518  mov      qword ptr [rsp + 0x20], rdi
002A851D  xor      edi, edi
002A851F  nop      
002A8520  mov      rcx, qword ptr [rbx]
002A8523  call     0x245020  ; -> 00245020 fn
002A8528  mov      qword ptr [rbx], rdi
002A852B  add      rbx, 8
002A852F  cmp      rbx, rsi
002A8532  jl       0x2a8520  ; -> 002A8520
002A8534  mov      rdi, qword ptr [rsp + 0x20]
002A8539  mov      rsi, qword ptr [rsp + 0x38]
002A853E  mov      rbx, qword ptr [rsp + 0x30]
002A8543  add      rsp, 0x28
002A8547  ret      
```
