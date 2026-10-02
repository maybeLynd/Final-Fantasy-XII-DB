# F-interior pack: `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/mg-worldmap-mesh.md`

Generated 2026-10-02 05:48 by OPUS (f_pack.py) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/f-interior.md`. Write your result to `cloud-reports/f-interior/mg-worldmap-mesh.json`.

Functions: 1. Each is cited on the page only at its entry and is still in the F frontier.

Scope guard: WARN (peer commits 24-72h: 312d1428c	SWE2-FRONTIER: pass 22 for SWE2-DATA - 20 pairs on six DATA pages read and accounted (batch D1, exec; 3198ee367	SWE2-CONTRACT: RC-22..RC-34 incorporated from SWE2-DATA's record (1261e2044) - eleven answered, RC-2). OPUS read these before packing.

## 003C9950 (125 B, extent 003C9950-003C99CD)

Page context: "00561390' calls the list helpers '00291D70' / '00291D80' and the widgets '00558F20', '0055A810' and '0055C690'. The world-map loader '00562F90' is called by '00550540', and '00563110' by '00552250'. '003C9950', '00561390' and '00562F90' claim slots through '00249210', and '00558FB0', '00561390' and '00562F90' request through '002493D0', which calls '00249210' and the label create '0024A4E0'. The UI owns the screens; the mesh is the data"

```
003C9950  mov      qword ptr [rsp + 8], rbx
003C9955  mov      qword ptr [rsp + 0x10], rsi
003C995A  push     rdi
003C995B  sub      rsp, 0x30
003C995F  mov      rdi, rcx
003C9962  call     0x249580  ; -> 00249580 fn
003C9967  mov      rcx, qword ptr [rdi + 0xd0]
003C996E  mov      rsi, rax
003C9971  test     rcx, rcx
003C9974  je       0x3c997b  ; -> 003C997B
003C9976  call     0x3697f0  ; -> 003697F0 fn
003C997B  movzx    r8d, byte ptr [rdi + 0xc1]
003C9983  mov      edx, 7
003C9988  add      r8d, 0xe
003C998C  mov      dword ptr [rsp + 0x20], 0
003C9994  mov      rcx, rsi
003C9997  lea      r9d, [rdx - 4]
003C999B  call     0x249210  ; -> 00249210 fn
003C99A0  mov      rcx, rsi
003C99A3  mov      rbx, rax
003C99A6  call     0x249410  ; -> 00249410 fn
003C99AB  mov      rax, qword ptr [rbx + 8]
003C99AF  or       dword ptr [rdi + 0xc4], 8
003C99B6  mov      rbx, qword ptr [rsp + 0x40]
003C99BB  mov      rsi, qword ptr [rsp + 0x48]
003C99C0  mov      qword ptr [rdi + 0xd0], rax
003C99C7  add      rsp, 0x30
003C99CB  pop      rdi
003C99CC  ret      
```
