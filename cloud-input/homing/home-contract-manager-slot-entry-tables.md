# Homing pack: `04-Actor-Entity/CONTRACT-manager-slot-entry-tables.md`

Generated 2026-10-02 21:20 by FABLE (homing_pack.py, OPUS's listing code) from the certified executable (sha256 73461D08...21F8). Brief: `docs/cloud-briefs/homing.md`. Write your result to `cloud-reports/homing/home-contract-manager-slot-entry-tables.json`.

Bodies: 1. No page cites any of them yet. Each is called from a function this page already cites; the host page is fixed (do not choose another).

## 0037DD50 (99 B, extent 0037DD50-0037DDB3)

Entered from (direct sites whose caller this page cites): `003DCFB0` + 0xA8 (call; `003DCFB0` is cited on this page)
Other direct sites: none

Host context: "  > and adds it into '[rbx]' ('003DA10A'–'003DA111'), then hands the value to the player    > ('movss xmm2, [rbx]' at '003DA133' → '002555A0'/'00257A00'/'002567B0') as the shot's    > absolute time. '003DCFB0' (B) does the same at 'entry+0x08'+'0x18' stride:    > 'frameStep(02B58190) × rate(+0x10) × const' added into '+0x0C' ('003DD08B'–'003DD0A5')    > and passed to the shake sampler '0037D1F0' ('003DD05D'). **'+0x10' is a per-channel "

```
0037DD50  movsxd   rax, ecx
0037DD53  imul     r9, rax, 0x3d0
0037DD5A  movsxd   rax, r8d
0037DD5D  imul     r8, rax, 0xf0
0037DD64  lea      rax, [rip + 0x275fc25]  ; -> 02ADD990
0037DD6B  add      r8, r9
0037DD6E  add      r8, rax
0037DD71  cmp      edx, -1
0037DD74  jne      0x37dd82  ; -> 0037DD82
0037DD76  mov      dword ptr [r8 + 0xe8], 2
0037DD81  ret      
0037DD82  movsxd   rax, edx
0037DD85  lea      r10, [rip + 0x275fbf4]  ; -> 02ADD980
0037DD8C  lea      rcx, [rax + rax*2]
0037DD90  mov      rax, qword ptr [r9 + r10]
0037DD94  shl      rcx, 5
0037DD98  movzx    ecx, word ptr [rax + rcx + 0x28]
0037DD9D  movd     xmm0, ecx
0037DDA1  cvtdq2ps xmm0, xmm0
0037DDA4  addss    xmm0, dword ptr [rip + 0x196ddfc]  ; -> 01CEBBA8 [f32 1]
0037DDAC  movss    dword ptr [r8 + 8], xmm0
0037DDB2  ret      
```
