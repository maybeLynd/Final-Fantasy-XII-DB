# Homing pack: `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/cl2-menu-colour-tables.md`

Generated 2026-10-03 03:37 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-cl2-menu-colour-tables.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 00616210 (58 B, extent 00616210-0061624A)

Entered from (direct sites whose caller this page cites): `00163D00` + 0x46 (call; `00163D00` is cited on this page)
Other direct sites: `00163110` + 0x46 (call); `00163170` + 0x46 (call); `001631D0` + 0x46 (call); `00163230` + 0x46 (call); `00163290` + 0x38 (call); `001632E0` + 0x38 (call); `00163330` + 0x38 (call); `00163380` + 0x38 (call); `001633D0` + 0x44 (call); `00163430` + 0x44 (call); `00163490` + 0x44 (call); `001634F0` + 0x44 (call); `00163550` + 0x38 (call); `001635A0` + 0x38 (call); `001635F0` + 0x38 (call); `00163640` + 0x46 (call); `001636A0` + 0x46 (call); `00163700` + 0x46 (call); `00163760` + 0x43 (call); `001637C0` + 0x46 (call); `00163820` + 0x46 (call); `00163880` + 0x46 (call); `001638E0` + 0x46 (call); `00163940` + 0x46 (call); `001639A0` + 0x46 (call); `00163A00` + 0x46 (call); `00163A60` + 0x46 (call); `00163AC0` + 0x46 (call); `00163B20` + 0x46 (call); `00163B80` + 0x46 (call); `00163BE0` + 0x46 (call); `00163C40` + 0x46 (call); `00163CA0` + 0x46 (call); `00163D60` + 0x2F (call)

Host context: "lette and count as an external CLUT for a location-map image. The upload '0024A1D0' → '00180E70' / '00181000' → '0017F3B0' builds each palette row as a texture of the format object '02CF7480', which '00163D00' constructs with the name 'RGBA8' and '0x1C' in its four format slots ('0x1C' is the value of 'DXGI_FORMAT_R8G8B8A8_UNORM': an inference from the constant, the Direct3D call itself is not traced). **Component order: R, G, B, A**, b"

```
00616210  push     rbx
00616212  sub      rsp, 0x20
00616216  mov      rbx, rcx
00616219  call     0x62cd40  ; -> 0062CD40 fn
0061621E  mov      eax, dword ptr [rsp + 0x50]
00616222  mov      dword ptr [rbx + 0x20], eax
00616225  mov      eax, dword ptr [rsp + 0x58]
00616229  mov      dword ptr [rbx + 0x24], eax
0061622C  mov      eax, dword ptr [rsp + 0x60]
00616230  mov      dword ptr [rbx + 0x28], eax
00616233  mov      eax, dword ptr [rsp + 0x68]
00616237  mov      dword ptr [rbx + 0x2c], eax
0061623A  mov      eax, dword ptr [rsp + 0x70]
0061623E  mov      dword ptr [rbx + 0x30], eax
00616241  mov      rax, rbx
00616244  add      rsp, 0x20
00616248  pop      rbx
00616249  ret      
```
