# F-interior pack: `02-Resource-And-Asset-Pipeline/CONTRACT-ard-area-binder.md`

Generated 2026-10-02 08:46 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/contract-ard-area-binder.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 7903502f7	FABLE: pass-22 debt - crossing sections on 94 pages (FABLE's group; 12 overlay-carrier pages routed ; inbox mentions: SWE2-AUDIT-SEM.md). OPUS read these before packing.

## 003EA6B0 (43 B, extent 003EA6B0-003EA6DB)

Page context: "2B58178' (the '.ard' slot 7 of AB-7); '003EA820' calls the read request '0032EB40'. From outside the contract, 'WorldSimulation_ProcessDeferredModeRequest' ('0032FC30') calls the refresh '003EA6E0'; '003EA6B0', a 43-byte reset that sets '02B5E0B8' to -1, zeroes the buffer record at '02B5E0C0' and calls '003DCF00' with 0, is the third caller of that store; and the map-name setter '00379A10' calls the path resolver '002DF980'. The binder "

```
003EA6B0  sub      rsp, 0x28
003EA6B4  xorps    xmm0, xmm0
003EA6B7  mov      dword ptr [rip + 0x27739f7], 0xffffffff  ; -> 02B5E0B8
003EA6C1  xor      ecx, ecx
003EA6C3  movdqu   xmmword ptr [rip + 0x27739f5], xmm0  ; -> 02B5E0C0
003EA6CB  call     0x3dcf00  ; -> 003DCF00 fn
003EA6D0  xor      ecx, ecx
003EA6D2  add      rsp, 0x28
003EA6D6  jmp      0x3dcf10  ; -> 003DCF10 fn
```
