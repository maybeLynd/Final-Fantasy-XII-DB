# Homing pack: `16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md`

Generated 2026-10-03 12:18 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-h10-numeric-formatting-and-character-mapping.json`.

Bodies: 2. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0028F810 (19 B, extent 0028F810-0028F823)

Entered from (direct sites whose caller this page cites): `002A5520` + 0x12 (call; `002A5520` is cited on this page)
Other direct sites: `0029BC80` + 0xFE (call); `0029BC80` + 0x10B (call); `0029BC80` + 0x11E (call); `0029BC80` + 0x15A (call); `0029BC80` + 0x167 (call); `003FACF0` + 0x1B8 (call); `003FAF10` + 0x45E (call); `003FC3F0` + 0xB1 (call)

Host context: "ths the reads and adds fall on absolute low addresses | Interior anchor '002A4032'; Interior anchor '002A405E'; Interior anchor '002A4062'; Interior anchor '002A40A1'; Interior anchor '002A40A6' | | '002A5520' | 109 B | '002A70B0' + 0x40D | takes 'v' = '002A5520' + 0x12('rcx'), replaced by 0x1C0 ('01E0C1DC') when negative, and calls '002A5520' + 0x25 with bit 11 of dword 'rcx+0x114'; returns the truncated integer of float('v' minus 5 ti"

```
0028F810  mov      rcx, qword ptr [rip + 0x1e0c669]  ; -> 0209BE80
0028F817  mov      rcx, qword ptr [rcx + 0x10f78]
0028F81E  jmp      0x296450  ; -> 00296450 fn
```

## 002A84F0 (88 B, extent 002A84F0-002A8548)

Entered from (direct sites whose caller this page cites): `002A6190` + 0x7A2 (call; `002A6190` is cited on this page)
Other direct sites: none

Host context: "39C4A0' | 24 B | flag bit 11 → target selection | | '00916520' | — | **the power-of-ten table** ('.rdata') | | '003A1DB0' | — | 'RenderCommand_SubmitCurrentBufferAndSwap' — the Presentation exit | | '002A6190' | — | object message handler; **9 labels: 1, 2, 3, 4, 10, 12, 15, 18, 21** + 'default'. Case 1 registers, **case 4 updates** and enters the cluster | | '0209C4D0' | — | **8-slot registry of live message windows** ('.data'), '0209C"

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
